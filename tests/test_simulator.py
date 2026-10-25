
import pytest

from app.models import EventType, NetworkEvent, Severity
from simulator.generate_events import generate_event, generate_events


def test_generate_event_returns_valid_network_event():
    event = generate_event()

    assert isinstance(event, NetworkEvent)
    assert event.event_id.startswith("EVT-")
    assert event.event_type in list(EventType)
    assert event.severity in list(Severity)
    assert event.location
    assert event.description
    assert event.timestamp is not None


def test_generate_events_returns_requested_count():
    events = generate_events(10)

    assert len(events) == 10
    assert all(isinstance(event, NetworkEvent) for event in events)


def test_generate_events_have_unique_ids():
    events = generate_events(20)
    event_ids = [event.event_id for event in events]

    assert len(event_ids) == len(set(event_ids))


def test_generate_events_rejects_zero_count():
    with pytest.raises(ValueError, match="count must be at least 1"):
        generate_events(0)


def test_generate_events_rejects_negative_count():
    with pytest.raises(ValueError, match="count must be at least 1"):
        generate_events(-1)
