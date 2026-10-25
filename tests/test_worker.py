from app.models import NetworkEvent
from app.worker import process_event


def test_worker_processes_critical_event():
    event = NetworkEvent(
        event_id="EVT-201",
        event_type="service_outage",
        location="Lagos-Ikeja",
        severity="critical",
        description="Simulated service outage",
    )

    result = process_event(event)

    assert result["event_id"] == "EVT-201"
    assert result["processing_status"] == "processed"
    assert result["incident"]["incident_detected"] is True
    assert result["incident"]["priority"] == "critical"


def test_worker_processes_low_severity_event():
    event = NetworkEvent(
        event_id="EVT-202",
        event_type="dropped_call",
        location="Lagos-Ikeja",
        severity="low",
        description="Simulated low-severity event",
    )

    result = process_event(event)

    assert result["processing_status"] == "processed"
    assert result["incident"]["incident_detected"] is False
