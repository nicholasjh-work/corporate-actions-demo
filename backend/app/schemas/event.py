"""Pydantic schemas for request/response validation."""
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.models.event import EventStatus, EventType


class EventBase(BaseModel):
    """Base schema for event data."""
    
    event_type: EventType
    symbol: str = Field(..., min_length=1, max_length=20, pattern="^[A-Z0-9]+$")


class DividendEventCreate(EventBase):
    """Schema for creating dividend events."""
    
    event_type: EventType = EventType.DIVIDEND
    amount: Decimal = Field(..., gt=0, decimal_places=4)
    ex_date: date
    record_date: date
    payment_date: date
    currency: str = Field(default="USD", min_length=3, max_length=3)
    
    @field_validator("record_date")
    @classmethod
    def record_after_ex(cls, v: date, info: Any) -> date:
        """Validate record date is after ex-date."""
        if info.data.get("ex_date") and v < info.data["ex_date"]:
            raise ValueError("record_date must be on or after ex_date")
        return v
    
    @field_validator("payment_date")
    @classmethod
    def payment_after_record(cls, v: date, info: Any) -> date:
        """Validate payment date is after record date."""
        if info.data.get("record_date") and v < info.data["record_date"]:
            raise ValueError("payment_date must be on or after record_date")
        return v


class StockSplitEventCreate(EventBase):
    """Schema for creating stock split events."""
    
    event_type: EventType = EventType.STOCK_SPLIT
    split_ratio_from: int = Field(..., gt=0)
    split_ratio_to: int = Field(..., gt=0)
    effective_date: date
    
    @field_validator("split_ratio_to")
    @classmethod
    def valid_split(cls, v: int, info: Any) -> int:
        """Validate split ratio makes sense."""
        ratio_from = info.data.get("split_ratio_from", 1)
        if v == ratio_from:
            raise ValueError("split_ratio_to must differ from split_ratio_from")
        return v


class MergerEventCreate(EventBase):
    """Schema for creating merger events."""
    
    event_type: EventType = EventType.MERGER
    target_symbol: str = Field(..., min_length=1, max_length=20)
    exchange_ratio: Decimal = Field(..., gt=0, decimal_places=4)
    cash_component: Decimal = Field(default=Decimal("0"), ge=0, decimal_places=2)
    effective_date: date


class EventCreate(BaseModel):
    """Generic event creation schema."""
    
    event_type: EventType
    symbol: str = Field(..., min_length=1, max_length=20)
    idempotency_key: str | None = Field(None, max_length=255)
    
    # Event-specific fields stored in payload
    amount: Decimal | None = None
    ex_date: date | None = None
    record_date: date | None = None
    payment_date: date | None = None
    currency: str = Field(default="USD", min_length=3, max_length=3)
    
    split_ratio_from: int | None = None
    split_ratio_to: int | None = None
    effective_date: date | None = None
    
    target_symbol: str | None = None
    exchange_ratio: Decimal | None = None
    cash_component: Decimal | None = None


class EventResponse(BaseModel):
    """Schema for event responses."""
    
    id: int
    event_type: EventType
    symbol: str
    status: EventStatus
    payload: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    error_message: str | None = None
    retry_count: int
    idempotency_key: str | None = None
    created_by: str
    
    model_config = {"from_attributes": True}


class EventList(BaseModel):
    """Paginated list of events."""
    
    events: list[EventResponse]
    total: int
    page: int
    page_size: int


class MetricsResponse(BaseModel):
    """System metrics response."""
    
    total_events: int
    events_by_type: dict[str, int]
    events_by_status: dict[str, int]
    recent_events_1h: int
    recent_events_24h: int
    average_processing_time_seconds: float | None = None
    error_rate: float


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str
    database: str
    timestamp: datetime
