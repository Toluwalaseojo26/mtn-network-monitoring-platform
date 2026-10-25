
import random
from uuid import uuid4

from app.models import EventType, NetworkEvent, Severity


LOCATIONS = [
    "Lagos-Ikeja",
    "Lagos-Lekki",
    "Abuja-Central",
    "Kano-Central",
    "Port-Harcourt",
]

EVENT_DESCRIPTIONS = {
    EventType.DROPPED_CALL: "Elevated dropped-call rate",
    EventType.HIGH_LATENCY: "Network latency above normal levels",
    EventType.SERVICE_OUTAGE: "Simulated service outage",
    EventType.FAILED_TRANSACTION: "Elevated failed transaction rate",
    EventType.DEVICE_FAILURE: "Network device failure detected",
}


def generate_event() -> NetworkEvent:
    """Generate one random, simulated network event."""

    event_type = random.choice(list(EventType))
    severity = random.choice(list(Severity))

    return NetworkEvent(
        event_id=f"EVT-{uuid4().hex[:8].upper()}",
        event_type=event_type,
        location=random.choice(LOCATIONS),
        severity=severity,
        description=EVENT_DESCRIPTIONS[event_type],
    )


def generate_events(count: int = 5) -> list[NetworkEvent]:
    """Generate a requested number of simulated network events."""

    if count < 1:
        raise ValueError("count must be at least 1")

    return [generate_event() for _ in range(count)]


if __name__ == "__main__":
    for event in generate_events():
        print(event.model_dump_json())
