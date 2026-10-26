
import json

from app.storage import read_records, save_record


def test_save_record_creates_file_and_saves_record(tmp_path):
    file_path = tmp_path / "events.jsonl"
    record = {
        "event_id": "EVT-301",
        "processing_status": "processed",
    }

    save_record(record, file_path)

    assert file_path.exists()
    assert read_records(file_path) == [record]


def test_save_record_appends_multiple_records(tmp_path):
    file_path = tmp_path / "events.jsonl"

    first = {"event_id": "EVT-301"}
    second = {"event_id": "EVT-302"}

    save_record(first, file_path)
    save_record(second, file_path)

    assert read_records(file_path) == [first, second]


def test_read_records_returns_empty_list_for_missing_file(tmp_path):
    file_path = tmp_path / "missing.jsonl"

    assert read_records(file_path) == []


def test_storage_file_contains_one_json_record_per_line(tmp_path):
    file_path = tmp_path / "events.jsonl"
    record = {"event_id": "EVT-303", "priority": "critical"}

    save_record(record, file_path)

    lines = file_path.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 1
    assert json.loads(lines[0]) == record
