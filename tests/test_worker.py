
from app.detection import detect_incident
from app.event_queue import enqueue_event, event_queue
from app.models import NetworkEvent
from app.worker import process_event, process_next_event


def make_event(event_id: str, severity: str) -> NetworkEvent:
    return NetworkEvent(
        event_id=event_id,
        event_type="dropped_call",
        location="Lagos-Ikeja",
        severity=severity,
        description="Simulated network event",
    )


def test_worker_processes_critical_event():
    event = make_event("EVT-201", "critical")

    result = process_event(event)

    assert result["event_id"] == "EVT-201"
    assert result["processing_status"] == "processed"
    assert result["incident"]["incident_detected"] is True
    assert result["incident"]["priority"] == "critical"


def test_worker_processes_low_severity_event():
    event = make_event("EVT-202", "low")

    result = process_event(event)

    assert result["processing_status"] == "processed"
    assert result["incident"]["incident_detected"] is False


def test_worker_processes_next_queued_event():
    while not event_queue.empty():
        event_queue.get_nowait()

    event = make_event("EVT-203", "critical")
    enqueue_event(event)

    result = process_next_event()

    assert result is not None
    assert result["event_id"] == "EVT-203"
    assert result["processing_status"] == "processed"
    assert result["incident"]["incident_detected"] is True
    assert event_queue.empty()


def test_worker_returns_none_when_queue_is_empty():
    while not event_queue.empty():
        event_queue.get_nowait()

    assert process_next_event() is None

