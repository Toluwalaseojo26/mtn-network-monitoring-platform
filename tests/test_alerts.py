
import app.alerts as alerts


def test_create_alert_for_detected_incident(tmp_path, monkeypatch):
    file_path = tmp_path / "alerts.jsonl"

    monkeypatch.setattr(alerts, "ALERTS_PATH", file_path)

    incident = {
        "incident_detected": True,
        "incident_id": "INC-EVT-401",
        "event_id": "EVT-401",
        "priority": "critical",
        "location": "Lagos-Ikeja",
        "description": "Simulated service outage",
    }

    alert = alerts.create_alert(incident)

    assert alert is not None
    assert alert["alert_id"] == "ALERT-EVT-401"
    assert alert["incident_id"] == "INC-EVT-401"
    assert alert["priority"] == "critical"
    assert alert["delivery_status"] == "created"
    assert file_path.exists()


def test_no_alert_is_created_when_no_incident_is_detected(tmp_path, monkeypatch):
    file_path = tmp_path / "alerts.jsonl"

    monkeypatch.setattr(alerts, "ALERTS_PATH", file_path)

    incident = {
        "incident_detected": False,
        "event_id": "EVT-402",
        "reason": "Severity below threshold",
    }

    result = alerts.create_alert(incident)

    assert result is None
    assert not file_path.exists()


def test_alert_contains_a_message_and_timestamp(tmp_path, monkeypatch):
    file_path = tmp_path / "alerts.jsonl"

    monkeypatch.setattr(alerts, "ALERTS_PATH", file_path)

    incident = {
        "incident_detected": True,
        "incident_id": "INC-EVT-403",
        "event_id": "EVT-403",
        "priority": "high",
        "location": "Abuja-Central",
        "description": "Simulated network issue",
    }

    alert = alerts.create_alert(incident)

    assert "Abuja-Central" in alert["message"]
    assert "high" in alert["message"]
    assert alert["created_at"]
