"""API routes for corporate action events."""
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.event import EventStatus, EventType
from app.schemas.event import EventCreate, EventList, EventResponse, MetricsResponse
from app.services.event_service import EventService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["events"])


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new corporate action event",
)
def create_event(
    event_data: EventCreate,
    db: Annotated[Session, Depends(get_db)],
) -> EventResponse:
    """
    Create a new corporate action event.
    
    Validates input, creates event record, and initiates processing.
    Supports idempotency via optional idempotency_key.
    
    **Event Types:**
    - DIVIDEND: Requires amount, ex_date, record_date, payment_date
    - STOCK_SPLIT: Requires split_ratio_from, split_ratio_to, effective_date
    - MERGER: Requires target_symbol, exchange_ratio, effective_date
    """
    service = EventService(db)
    
    try:
        event = service.create_event(event_data, user="api_user")
        return EventResponse.model_validate(event)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error(f"Error creating event: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create event",
        ) from e


@router.get(
    "",
    response_model=EventList,
    summary="List corporate action events",
)
def list_events(
    db: Annotated[Session, Depends(get_db)],
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    event_type: EventType | None = None,
    status: EventStatus | None = None,
    symbol: str | None = None,
) -> EventList:
    """
    List events with optional filters and pagination.
    
    **Filters:**
    - event_type: Filter by event type
    - status: Filter by processing status
    - symbol: Filter by security symbol
    
    **Pagination:**
    - skip: Number of records to skip
    - limit: Maximum records to return (1-100)
    """
    service = EventService(db)
    
    try:
        events, total = service.list_events(
            skip=skip,
            limit=limit,
            event_type=event_type,
            status=status,
            symbol=symbol,
        )
        
        return EventList(
            events=[EventResponse.model_validate(e) for e in events],
            total=total,
            page=skip // limit + 1,
            page_size=limit,
        )
    except Exception as e:
        logger.error(f"Error listing events: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list events",
        ) from e


@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary="Get event by ID",
)
def get_event(
    event_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> EventResponse:
    """
    Retrieve a specific event by ID.
    
    Returns complete event details including payload and processing status.
    """
    service = EventService(db)
    
    event = service.get_event(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event {event_id} not found",
        )
    
    return EventResponse.model_validate(event)


@router.post(
    "/{event_id}/cancel",
    response_model=EventResponse,
    summary="Cancel an event",
)
def cancel_event(
    event_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> EventResponse:
    """
    Cancel a pending or processing event.
    
    Completed or already cancelled events cannot be cancelled.
    """
    service = EventService(db)
    
    event = service.get_event(event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event {event_id} not found",
        )
    
    if event.status in (EventStatus.COMPLETED, EventStatus.CANCELLED):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot cancel event with status {event.status.value}",
        )
    
    updated = service.update_event_status(
        event_id,
        EventStatus.CANCELLED,
        user="api_user",
    )
    
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel event",
        )
    
    return EventResponse.model_validate(updated)
