from datetime import datetime, timezone


def log(message: str) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] {message}", flush=True)
