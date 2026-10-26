
from app.alerts import create_alert
from app.event_queue import enqueue_event
from app.storage import save_record
from app.worker import process_next_event
from simulator.generate_events import generate_events


def run_pipeline(count: int = 5) -> list[dict]:
    """Generate, process, save, and alert on network events."""

    events = generate_events(count)

    for event in events:
        enqueue_event(event)

    results = []

    for _ in events:
        result = process_next_event()

        if result is not None:
            incident = result["incident"]
            alert = create_alert(incident)

            result["alert"] = alert
            save_record(result)

            results.append(result)

    return results


if __name__ == "__main__":
    results = run_pipeline()

    for result in results:
        print(result)

    alerts_created = sum(
        1 for result in results if result["alert"] is not None
    )

    print(f"\nProcessed events: {len(results)}")
    print(f"Alerts created: {alerts_created}")

