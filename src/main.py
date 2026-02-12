from playwright.sync_api import sync_playwright, TimeoutError
from datetime import datetime, timezone
import sys


TEST_IDENTIFIERS = [
    "111111111111111",
    "222222222222222",
    "333333333333333",
    "444444444444444",
    "555555555555555",
]

TARGET_URL = "https://www.att.com/buy/bring-your-own-device/"


def log(message: str):
    ts = datetime.now(timezone.utc).isoformat()
    print(f"[{ts}] {message}", flush=True)


def abort(message: str):
    log(f"ABORT: {message}")
    sys.exit(1)


def main():
    log("Starting single-session validator")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        log("Navigating to target URL")
        page.goto(TARGET_URL, timeout=60000)

        for idx, identifier in enumerate(TEST_IDENTIFIERS, start=1):
            log(f"Processing identifier {idx}/{len(TEST_IDENTIFIERS)}: {identifier}")

            try:
                # Placeholder: real selectors added in Chapter 5
                page.wait_for_timeout(2000)

                log(f"Identifier {identifier} processed (placeholder)")

            except TimeoutError:
                abort("Timeout waiting for expected page state")

            except Exception as e:
                abort(str(e))

        log("All identifiers processed successfully")

        browser.close()

    log("Session finished cleanly")
    sys.exit(0)


if __name__ == "__main__":
    main()
