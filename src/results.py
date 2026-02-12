import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict


def generate_run_id() -> str:
    """
    Generates a deterministic UTC timestamp for this run.
    Example: 20260212-191455
    """
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def ensure_output_dir() -> Path:
    """
    Ensures the output directory exists.
    """
    path = Path("output")
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json_results(run_id: str, results: List[Dict]) -> Path:
    """
    Writes structured results to:
        output/run-<run_id>.json
    """
    output_dir = ensure_output_dir()
    file_path = output_dir / f"run-{run_id}.json"

    payload = {
        "run_id": run_id,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "results": results,
    }

    json_text = json.dumps(payload, indent=2)

    with file_path.open("w", encoding="utf-8") as f:
        f.write(json_text)

    return file_path

