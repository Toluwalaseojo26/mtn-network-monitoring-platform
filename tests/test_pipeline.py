
import pytest

import app.pipeline as pipeline
import app.alerts as alerts
from app.event_queue import event_queue
from app.models import EventType, NetworkEvent, Severity
from app.storage import read_records, save_record


@pytest.fixture(autouse=True)
def isolate_pipeline_storage(tmp_path, monkeypatch):
    """Keep pipeline tests isolated from real project data."""

    processed_file = tmp_path / "processed_events.jsonl"
    alerts_file = tmp_path / "alerts.jsonl"

    monkeypatch.setattr(
        pipeline,
        "save_record",
        lambda record: save_record(record, processed_file),
    )
    monkeypatch.setattr(alerts, "ALERTS_PATH", alerts_file)

    while not event_queue.empty():
        event_queue.get_nowait()

    yield

    while not event_queue.empty():
        event_queue.get_nowait()


def test_pipeline_processes_requested_number_of_events():
    results = pipeline.run_pipeline(5)

    assert len(results) == 5
    assert all(
        result["processing_status"] == "processed"
        for result in results
    )


def test_pipeline_processes_ten_events():
    results = pipeline.run_pipeline(10)

    assert len(results) == 10


def test_pipeline_saves_processed_results(tmp_path):
    results = pipeline.run_pipeline(3)

    saved_file = tmp_path / "processed_events.jsonl"
    saved_records = read_records(saved_file)

    assert len(saved_records) == 3
    assert saved_records == results


def test_pipeline_creates_alert_for_critical_event(
    tmp_path, monkeypatch
):
    event = NetworkEvent(
        event_id="EVT-TEST-CRITICAL",
        event_type=EventType.FAILED_TRANSACTION,
        location="Lagos-Ikeja",
        severity=Severity.CRITICAL,
        description="Test critical transaction failure",
    )

    monkeypatch.setattr(
        pipeline,
        "generate_events",
        lambda count: [event],
    )

    results = pipeline.run_pipeline(1)

    assert len(results) == 1
    assert results[0]["incident"]["incident_detected"] is True
    assert results[0]["alert"] is not None
    assert results[0]["alert"]["priority"] == "critical"

    saved_file = tmp_path / "processed_events.jsonl"
    saved_records = read_records(saved_file)

    assert saved_records == results


def test_pipeline_does_not_create_alert_for_low_severity_event(
    monkeypatch,
):
    event = NetworkEvent(
        event_id="EVT-TEST-LOW",
        event_type=EventType.DROPPED_CALL,
        location="Lagos-Ikeja",
        severity=Severity.LOW,
        description="Test low-severity dropped call",
    )

    monkeypatch.setattr(
        pipeline,
        "generate_events",
        lambda count: [event],
    )

    results = pipeline.run_pipeline(1)

    assert len(results) == 1
    assert results[0]["incident"]["incident_detected"] is False
    assert results[0]["alert"] is None

