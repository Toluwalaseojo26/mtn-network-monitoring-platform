from app.detection import detect_incident
from app.models import NetworkEvent


def process_event(event: NetworkEvent) -> dict:
    """Process a validated event and return its detection result."""

    result = detect_incident(event)

    return {
        "event_id": event.event_id,
        "processing_status": "processed",
        "incident": result,
    }
