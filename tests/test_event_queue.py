
from app.event_queue import enqueue_event, dequeue_event, event_queue
from app.models import NetworkEvent


def make_event(event_id: str) -> NetworkEvent:
    return NetworkEvent(
        event_id=event_id,
        event_type="dropped_call",
        location="Lagos-Ikeja",
        severity="high",
        description="Simulated dropped call",
    )


def test_queue_returns_events_in_first_in_first_out_order():
    # Clear leftover events so the test starts clean.
    while not event_queue.empty():
        event_queue.get_nowait()

    first = make_event("EVT-301")
    second = make_event("EVT-302")

    enqueue_event(first)
    enqueue_event(second)

    assert dequeue_event().event_id == "EVT-301"
    assert dequeue_event().event_id == "EVT-302"
    assert event_queue.empty()
