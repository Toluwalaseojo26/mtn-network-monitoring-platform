
from datetime import datetime, timezone
from pathlib import Path

from app.storage import save_record


ALERTS_PATH = Path("data/alerts.jsonl")


def create_alert(incident: dict) -> dict | None:
    """Create and save an alert for a detected incident."""

    if not incident.get("incident_detected"):
        return None

    alert = {
        "alert_id": f"ALERT-{incident['event_id']}",
        "event_id": incident["event_id"],
        "incident_id": incident["incident_id"],
        "priority": incident["priority"],
        "location": incident["location"],
        "message": (
            f"Network incident detected in {incident['location']}. "
            f"Priority: {incident['priority']}."
        ),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "delivery_status": "created",
    }

    save_record(alert, file_path=ALERTS_PATH)

    return alert

