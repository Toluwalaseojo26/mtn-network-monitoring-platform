
from app.pipeline import run_pipeline
from app.event_queue import event_queue


def test_pipeline_processes_requested_number_of_events():
    while not event_queue.empty():
        event_queue.get_nowait()

    results = run_pipeline(5)

    assert len(results) == 5
    assert all(
        result["processing_status"] == "processed"
        for result in results
    )


def test_pipeline_processes_ten_events():
    while not event_queue.empty():
        event_queue.get_nowait()

    results = run_pipeline(10)

    assert len(results) == 10
