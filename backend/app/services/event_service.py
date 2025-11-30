"""Service layer for corporate action event processing."""
import logging
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.event import AuditLog, CorporateActionEvent, EventStatus, EventType
from app.schemas.event import EventCreate, EventResponse

logger = logging.getLogger(__name__)


class EventService:
    """Business logic for corporate action events."""
    
    def __init__(self, db: Session) -> None:
        """Initialize service with database session."""
        self.db = db
    
    def create_event(
        self, event_data: EventCreate, user: str = "system"
    ) -> CorporateActionEvent:
        """
        Create a new corporate action event.
        
        Args:
            event_data: Event creation schema
            user: User creating the event
            
        Returns:
            Created event entity
            
        Raises:
            ValueError: If idempotency key already exists
        """
        # Build payload from event-specific fields
        payload: dict[str, Any] = {
            "currency": event_data.currency,
        }
        
        # Add type-specific fields
        if event_data.event_type == EventType.DIVIDEND:
            payload.update({
                "amount": str(event_data.amount) if event_data.amount else None,
                "ex_date": event_data.ex_date.isoformat() if event_data.ex_date else None,
                "record_date": (
                    event_data.record_date.isoformat() if event_data.record_date else None
                ),
                "payment_date": (
                    event_data.payment_date.isoformat() if event_data.payment_date else None
                ),
            })
        elif event_data.event_type == EventType.STOCK_SPLIT:
            payload.update({
                "split_ratio_from": event_data.split_ratio_from,
                "split_ratio_to": event_data.split_ratio_to,
                "effective_date": (
                    event_data.effective_date.isoformat() if event_data.effective_date else None
                ),
            })
        elif event_data.event_type == EventType.MERGER:
            payload.update({
                "target_symbol": event_data.target_symbol,
                "exchange_ratio": (
                    str(event_data.exchange_ratio) if event_data.exchange_ratio else None
                ),
                "cash_component": (
                    str(event_data.cash_component) if event_data.cash_component else None
                ),
                "effective_date": (
                    event_data.effective_date.isoformat() if event_data.effective_date else None
                ),
            })
        
        # Create event
        event = CorporateActionEvent(
            event_type=event_data.event_type,
            symbol=event_data.symbol.upper(),
            status=EventStatus.PENDING,
            payload=payload,
            idempotency_key=event_data.idempotency_key,
            created_by=user,
        )
        
        try:
            self.db.add(event)
            self.db.flush()  # Get the ID before audit log
            
            # Create audit log entry
            self._create_audit_log(
                event_id=event.id,
                action="CREATE",
                old_status=None,
                new_status=EventStatus.PENDING.value,
                changes={"payload": payload},
                user=user,
            )
            
            self.db.commit()
            self.db.refresh(event)
            
            logger.info(f"Created event {event.id} for {event.symbol} ({event.event_type.value})")
            return event
            
        except IntegrityError as e:
            self.db.rollback()
            if "idempotency_key" in str(e):
                raise ValueError("Duplicate idempotency key") from e
            raise
    
    def get_event(self, event_id: int) -> CorporateActionEvent | None:
        """Get event by ID."""
        return self.db.query(CorporateActionEvent).filter(
            CorporateActionEvent.id == event_id
        ).first()
    
    def list_events(
        self,
        skip: int = 0,
        limit: int = 100,
        event_type: EventType | None = None,
        status: EventStatus | None = None,
        symbol: str | None = None,
    ) -> tuple[list[CorporateActionEvent], int]:
        """
        List events with filters and pagination.
        
        Returns:
            Tuple of (events, total_count)
        """
        query = self.db.query(CorporateActionEvent)
        
        if event_type:
            query = query.filter(CorporateActionEvent.event_type == event_type)
        if status:
            query = query.filter(CorporateActionEvent.status == status)
        if symbol:
            query = query.filter(CorporateActionEvent.symbol == symbol.upper())
        
        total = query.count()
        events = query.order_by(CorporateActionEvent.created_at.desc()).offset(skip).limit(
            limit
        ).all()
        
        return events, total
    
    def update_event_status(
        self,
        event_id: int,
        new_status: EventStatus,
        error_message: str | None = None,
        user: str = "system",
    ) -> CorporateActionEvent | None:
        """
        Update event status with audit trail.
        
        Args:
            event_id: Event ID
            new_status: New status
            error_message: Optional error message for failed events
            user: User making the change
            
        Returns:
            Updated event or None if not found
        """
        event = self.get_event(event_id)
        if not event:
            return None
        
        old_status = event.status
        event.status = new_status
        event.updated_at = datetime.utcnow()
        
        if error_message:
            event.error_message = error_message
            event.retry_count += 1
        
        # Create audit log
        changes = {"status": {"from": old_status.value, "to": new_status.value}}
        if error_message:
            changes["error_message"] = error_message
            changes["retry_count"] = event.retry_count
        
        self._create_audit_log(
            event_id=event.id,
            action="UPDATE",
            old_status=old_status.value,
            new_status=new_status.value,
            changes=changes,
            user=user,
        )
        
        self.db.commit()
        self.db.refresh(event)
        
        logger.info(f"Updated event {event_id} status: {old_status.value} -> {new_status.value}")
        return event
    
    def get_metrics(self) -> dict[str, Any]:
        """
        Calculate system metrics.
        
        Returns:
            Dictionary with aggregated metrics
        """
        now = datetime.utcnow()
        one_hour_ago = now - timedelta(hours=1)
        one_day_ago = now - timedelta(days=1)
        
        # Total events
        total = self.db.query(func.count(CorporateActionEvent.id)).scalar() or 0
        
        # Events by type
        type_counts = dict(
            self.db.query(CorporateActionEvent.event_type, func.count(CorporateActionEvent.id))
            .group_by(CorporateActionEvent.event_type)
            .all()
        )
        events_by_type = {k.value: v for k, v in type_counts.items()}
        
        # Events by status
        status_counts = dict(
            self.db.query(CorporateActionEvent.status, func.count(CorporateActionEvent.id))
            .group_by(CorporateActionEvent.status)
            .all()
        )
        events_by_status = {k.value: v for k, v in status_counts.items()}
        
        # Recent events
        recent_1h = (
            self.db.query(func.count(CorporateActionEvent.id))
            .filter(CorporateActionEvent.created_at >= one_hour_ago)
            .scalar()
            or 0
        )
        
        recent_24h = (
            self.db.query(func.count(CorporateActionEvent.id))
            .filter(CorporateActionEvent.created_at >= one_day_ago)
            .scalar()
            or 0
        )
        
        # Error rate
        failed_count = events_by_status.get(EventStatus.FAILED.value, 0)
        error_rate = failed_count / total if total > 0 else 0.0
        
        return {
            "total_events": total,
            "events_by_type": events_by_type,
            "events_by_status": events_by_status,
            "recent_events_1h": recent_1h,
            "recent_events_24h": recent_24h,
            "average_processing_time_seconds": None,  # Would need timing data
            "error_rate": round(error_rate, 4),
        }
    
    def _create_audit_log(
        self,
        event_id: int,
        action: str,
        old_status: str | None,
        new_status: str,
        changes: dict[str, Any],
        user: str,
        correlation_id: str | None = None,
    ) -> None:
        """Create immutable audit log entry."""
        audit = AuditLog(
            event_id=event_id,
            action=action,
            old_status=old_status,
            new_status=new_status,
            changes=changes,
            user=user,
            correlation_id=correlation_id,
        )
        self.db.add(audit)
