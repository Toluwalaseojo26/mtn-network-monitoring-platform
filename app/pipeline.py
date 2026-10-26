
from app.event_queue import enqueue_event
from app.storage import save_record
from app.worker import process_next_event
from simulator.generate_events import generate_events


def run_pipeline(count: int = 5) -> list[dict]:
    """Generate, queue, process, and save network event results."""

    events = generate_events(count)

    for event in events:
        enqueue_event(event)

    results = []

    for _ in events:
        result = process_next_event()

        if result is not None:
            save_record(result)
            results.append(result)

    return results


if __name__ == "__main__":
    results = run_pipeline()

    for result in results:
        print(result)

    print(f"\nProcessed and saved {len(results)} events.")

