
from app.detection import detect_incident
from app.models import NetworkEvent


def make_event(event_id: str, severity: str) -> NetworkEvent:
    return NetworkEvent(
        event_id=event_id,
        event_type="dropped_call",
        location="Lagos-Ikeja",
        severity=severity,
        description="Simulated network event",
    )


def test_critical_event_triggers_critical_incident():
    event = make_event("EVT-101", "critical")

    result = detect_incident(event)

    assert result["incident_detected"] is True
    assert result["priority"] == "critical"
    assert result["incident_id"] == "INC-EVT-101"


def test_high_event_triggers_high_priority_incident():
    event = make_event("EVT-102", "high")

    result = detect_incident(event)

    assert result["incident_detected"] is True
    assert result["priority"] == "high"


def test_medium_event_does_not_trigger_high_priority_incident():
    event = make_event("EVT-103", "medium")

    result = detect_incident(event)

    assert result["incident_detected"] is False
    assert result["event_id"] == "EVT-103"


def test_low_event_does_not_trigger_high_priority_incident():
    event = make_event("EVT-104", "low")

    result = detect_incident(event)

    assert result["incident_detected"] is False
