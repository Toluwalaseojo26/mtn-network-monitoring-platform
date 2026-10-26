
import pytest

import app.pipeline as pipeline
from app.event_queue import event_queue
from app.storage import read_records, save_record


@pytest.fixture(autouse=True)
def isolate_pipeline_storage(tmp_path, monkeypatch):
    """Keep pipeline tests isolated from real project data."""

    file_path = tmp_path / "processed_events.jsonl"

    monkeypatch.setattr(
        pipeline,
        "save_record",
        lambda record: save_record(record, file_path),
    )

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

    # The fixture redirects storage to a temporary file.
    saved_file = tmp_path / "processed_events.jsonl"
    saved_records = read_records(saved_file)

    assert len(saved_records) == 3
    assert saved_records == results

