"""API routes for metrics and health checks."""
import logging
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.event import HealthResponse, MetricsResponse
from app.services.event_service import EventService

logger = logging.getLogger(__name__)

router = APIRouter(tags=["system"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check endpoint",
)
def health_check(
    db: Annotated[Session, Depends(get_db)],
) -> HealthResponse:
    """
    System health check.
    
    Verifies:
    - API is responsive
    - Database connection is working
    
    Returns 200 if healthy, 503 if any component is unhealthy.
    """
    # Check database
    db_status = "healthy"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed",
        ) from e
    
    return HealthResponse(
        status="healthy",
        database=db_status,
        timestamp=datetime.utcnow(),
    )


@router.get(
    "/metrics",
    response_model=MetricsResponse,
    summary="System metrics",
)
def get_metrics(
    db: Annotated[Session, Depends(get_db)],
) -> MetricsResponse:
    """
    Get aggregated system metrics.
    
    Returns:
    - Total event counts
    - Breakdown by type and status
    - Recent activity (1h, 24h)
    - Error rate
    
    Useful for monitoring and dashboards.
    """
    service = EventService(db)
    
    try:
        metrics = service.get_metrics()
        return MetricsResponse(**metrics)
    except Exception as e:
        logger.error(f"Error calculating metrics: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate metrics",
        ) from e
