
from queue import Queue

from app.models import NetworkEvent


# Temporary in-memory queue for local development.
event_queue: Queue[NetworkEvent] = Queue()


def enqueue_event(event: NetworkEvent) -> None:
    """Add a validated network event to the queue."""
    event_queue.put(event)


def dequeue_event() -> NetworkEvent:
    """Retrieve the next event, waiting if the queue is empty."""
    return event_queue.get()
