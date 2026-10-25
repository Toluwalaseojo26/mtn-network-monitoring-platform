
from app.detection import detect_incident
from app.event_queue import dequeue_event, event_queue
from app.models import NetworkEvent


def process_event(event: NetworkEvent) -> dict:
    """Process a validated event and return its detection result."""

    result = detect_incident(event)

    return {
        "event_id": event.event_id,
        "processing_status": "processed",
        "incident": result,
    }


def process_next_event() -> dict | None:
    """Process the next queued event, or return None if the queue is empty."""

    if event_queue.empty():
        return None

    event = dequeue_event()
    return process_event(event)

