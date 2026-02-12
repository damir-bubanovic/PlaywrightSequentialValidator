import os

# Replace these with real test identifiers (15-digit IMEI format is typical).
TEST_IDENTIFIERS = [
    "111111111111111",
    "222222222222222",
    "333333333333333",
    "444444444444444",
    "555555555555555",
]

IDENTIFY_URL = "https://www.att.com/buy/byod/identify?devicetype=phone"

# Timeouts (ms)
NAV_TIMEOUT_MS = 60_000
STATE_TIMEOUT_MS = 30_000

HEADLESS = os.getenv("HEADLESS", "0").strip() in {"1", "true", "TRUE", "yes", "YES"}
SLOWMO_MS = int(os.getenv("SLOWMO_MS", "0").strip() or "0")
