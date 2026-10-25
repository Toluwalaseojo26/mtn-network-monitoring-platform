
from app.models import NetworkEvent, Severity


def detect_incident(event: NetworkEvent) -> dict:
    """
    Apply demonstration rules to decide whether an event
    should trigger a high-priority incident.
    """

    if event.severity == Severity.CRITICAL:
        priority = "critical"
    elif event.severity == Severity.HIGH:
        priority = "high"
    else:
        return {
            "incident_detected": False,
            "event_id": event.event_id,
            "reason": "Event severity does not meet the incident threshold",
        }

    return {
        "incident_detected": True,
        "incident_id": f"INC-{event.event_id}",
        "event_id": event.event_id,
        "event_type": event.event_type.value,
        "location": event.location,
        "priority": priority,
        "description": event.description,
    }
