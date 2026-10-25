from fastapi.testclient import TestClient
from app.main import app
from app.event_queue import event_queue

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"



def test_receive_valid_event():
    # Clear leftover events so this test starts clean.
    while not event_queue.empty():
        event_queue.get_nowait()

    event = {
        "event_id": "EVT-001",
        "event_type": "dropped_call",
        "location": "Lagos-Ikeja",
        "severity": "high",
        "description": "Elevated dropped-call rate",
    }

    response = client.post("/events", json=event)

    assert response.status_code == 201
    assert response.json()["event"]["event_id"] == "EVT-001"
    assert response.json()["queue_status"] == "queued"
    assert not event_queue.empty()

    queued_event = event_queue.get_nowait()
    assert queued_event.event_id == "EVT-001"


def test_reject_invalid_event_type():
    event = {
        "event_id": "EVT-002",
        "event_type": "alien_event",
        "location": "Lagos-Ikeja",
        "severity": "high",
        "description": "Testing invalid event type",
    }

    response = client.post("/events", json=event)

    assert response.status_code == 422
