
from app.event_queue import enqueue_event
from app.worker import process_next_event
from simulator.generate_events import generate_events


def run_pipeline(count: int = 5) -> list[dict]:
    """Generate events, queue them, and process each one."""

    events = generate_events(count)

    for event in events:
        enqueue_event(event)

    results = []

    for _ in events:
        result = process_next_event()
        if result is not None:
            results.append(result)

    return results


if __name__ == "__main__":
    results = run_pipeline()

    for result in results:
        print(result)
