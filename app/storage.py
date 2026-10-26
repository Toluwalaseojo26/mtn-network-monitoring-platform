
import json
from pathlib import Path


DEFAULT_STORAGE_PATH = Path("data/processed_events.jsonl")


def save_record(
    record: dict,
    file_path: Path = DEFAULT_STORAGE_PATH,
) -> None:
    """Append one record to a JSON Lines file."""

    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")


def read_records(
    file_path: Path = DEFAULT_STORAGE_PATH,
) -> list[dict]:
    """Read all records from a JSON Lines file."""

    if not file_path.exists():
        return []

    records = []

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records
