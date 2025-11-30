"""Background event processor with retry logic."""
import logging
import random
import threading
import time
from typing import Any

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.event import EventStatus
from app.services.event_service import EventService

logger = logging.getLogger(__name__)


class EventProcessor:
    """
    Background processor for corporate action events.
    
    Simulates async processing with configurable failure rate
    and automatic retry logic.
    """
    
    def __init__(self, failure_rate: float = 0.1, processing_delay: float = 2.0) -> None:
        """
        Initialize processor.
        
        Args:
            failure_rate: Probability of simulated failure (0.0 to 1.0)
            processing_delay: Delay in seconds to simulate processing
        """
        self.failure_rate = failure_rate
        self.processing_delay = processing_delay
        self.running = False
        self.thread: threading.Thread | None = None
    
    def start(self) -> None:
        """Start the background processor thread."""
        if self.running:
            logger.warning("Processor already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._process_loop, daemon=True)
        self.thread.start()
        logger.info("Event processor started")
    
    def stop(self) -> None:
        """Stop the background processor thread."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Event processor stopped")
    
    def _process_loop(self) -> None:
        """Main processing loop."""
        while self.running:
            try:
                db = SessionLocal()
                try:
                    self._process_pending_events(db)
                finally:
                    db.close()
            except Exception as e:
                logger.error(f"Error in processor loop: {e}", exc_info=True)
            
            # Sleep between poll cycles
            time.sleep(1)
    
    def _process_pending_events(self, db: Session) -> None:
        """
        Process all pending events.
        
        Args:
            db: Database session
        """
        service = EventService(db)
        
        # Get pending events (limit to avoid overwhelming system)
        events, _ = service.list_events(
            status=EventStatus.PENDING,
            limit=10,
        )
        
        for event in events:
            try:
                # Mark as processing
                service.update_event_status(
                    event.id,
                    EventStatus.PROCESSING,
                    user="processor",
                )
                
                # Simulate processing
                logger.info(f"Processing event {event.id} ({event.event_type.value})")
                time.sleep(self.processing_delay)
                
                # Simulate random failures
                if random.random() < self.failure_rate and event.retry_count < 3:
                    error_msg = "Simulated processing failure (will retry)"
                    logger.warning(f"Event {event.id} failed: {error_msg}")
                    service.update_event_status(
                        event.id,
                        EventStatus.PENDING,  # Back to pending for retry
                        error_message=error_msg,
                        user="processor",
                    )
                elif event.retry_count >= 3:
                    # Max retries exceeded
                    error_msg = "Max retries (3) exceeded"
                    logger.error(f"Event {event.id} permanently failed: {error_msg}")
                    service.update_event_status(
                        event.id,
                        EventStatus.FAILED,
                        error_message=error_msg,
                        user="processor",
                    )
                else:
                    # Success
                    logger.info(f"Event {event.id} completed successfully")
                    service.update_event_status(
                        event.id,
                        EventStatus.COMPLETED,
                        user="processor",
                    )
                
            except Exception as e:
                logger.error(f"Error processing event {event.id}: {e}", exc_info=True)
                try:
                    service.update_event_status(
                        event.id,
                        EventStatus.FAILED,
                        error_message=str(e),
                        user="processor",
                    )
                except Exception as inner_e:
                    logger.error(f"Failed to update event status: {inner_e}")


# Global processor instance
processor = EventProcessor(failure_rate=0.05, processing_delay=1.5)
