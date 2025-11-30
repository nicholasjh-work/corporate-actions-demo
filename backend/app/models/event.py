"""SQLAlchemy models for corporate action events."""
from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import JSON, DateTime, Enum, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class EventType(str, PyEnum):
    """Corporate action event types."""
    
    DIVIDEND = "DIVIDEND"
    STOCK_SPLIT = "STOCK_SPLIT"
    MERGER = "MERGER"
    SPIN_OFF = "SPIN_OFF"
    RIGHTS_ISSUE = "RIGHTS_ISSUE"
    DELISTING = "DELISTING"


class EventStatus(str, PyEnum):
    """Event processing status."""
    
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class CorporateActionEvent(Base):
    """
    Corporate action event entity.
    
    Immutable after creation - updates create audit trail entries.
    """
    
    __tablename__ = "corporate_action_events"
    
    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Event identification
    event_type: Mapped[EventType] = mapped_column(Enum(EventType), nullable=False, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    
    # Status tracking
    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus), nullable=False, default=EventStatus.PENDING, index=True
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    # Event-specific data stored as JSON for flexibility
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    # Processing metadata
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    retry_count: Mapped[int] = mapped_column(default=0, nullable=False)
    
    # Compliance fields
    idempotency_key: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False, default="system")
    
    # Indexes for common queries
    __table_args__ = (
        Index("idx_symbol_created", "symbol", "created_at"),
        Index("idx_status_type", "status", "event_type"),
    )


class AuditLog(Base):
    """
    Immutable audit trail for compliance.
    
    Records all state changes to events.
    """
    
    __tablename__ = "audit_logs"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    # Link to event
    event_id: Mapped[int] = mapped_column(nullable=False, index=True)
    
    # Change tracking
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # CREATE, UPDATE, CANCEL
    old_status: Mapped[str | None] = mapped_column(String(50))
    new_status: Mapped[str] = mapped_column(String(50), nullable=False)
    
    # Change details
    changes: Mapped[dict] = mapped_column(JSON, nullable=False)
    
    # Metadata
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )
    user: Mapped[str] = mapped_column(String(100), nullable=False)
    correlation_id: Mapped[str | None] = mapped_column(String(100), index=True)
    
    __table_args__ = (Index("idx_event_timestamp", "event_id", "timestamp"),)
