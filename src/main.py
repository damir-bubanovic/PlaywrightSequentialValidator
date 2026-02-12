from playwright.sync_api import sync_playwright, TimeoutError as PwTimeoutError, Error as PwError

from .config import (
    TEST_IDENTIFIERS,
    IDENTIFY_URL,
    NAV_TIMEOUT_MS,
    STATE_TIMEOUT_MS,
    HEADLESS,
    SLOWMO_MS,
)
from .logging_utils import log
from .debug_utils import debug_dump
from .dom_utils import dismiss_cookie_banner
from .att_flow import process_identifier, detect_unexpected_state
from .results import generate_run_id, write_json_results


def main() -> int:
    run_id = generate_run_id()

    log("Starting single-session validator")
    log(f"RUN_ID={run_id}")
    log(f"HEADLESS={HEADLESS} SLOWMO_MS={SLOWMO_MS}")
    log(f"Target: {IDENTIFY_URL}")

    structured_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS, slow_mo=SLOWMO_MS)
        context = browser.new_context()
        page = context.new_page()

        page.goto(IDENTIFY_URL, timeout=NAV_TIMEOUT_MS, wait_until="domcontentloaded")
        dismiss_cookie_banner(page)

        unexpected = detect_unexpected_state(page)
        if unexpected:
            log(f"ABORT: {unexpected}")
            return 1

        for idx, identifier in enumerate(TEST_IDENTIFIERS, start=1):
            log(f"Processing identifier {idx}/{len(TEST_IDENTIFIERS)}: {identifier}")

            try:
                outcome = process_identifier(
                    page=page,
                    identify_url=IDENTIFY_URL,
                    identifier=identifier,
                    nav_timeout_ms=NAV_TIMEOUT_MS,
                    state_timeout_ms=STATE_TIMEOUT_MS,
                )

                log(f"Result: {identifier} -> {outcome.kind} | {outcome.details}")

                structured_results.append(
                    {
                        "identifier": identifier,
                        "kind": outcome.kind,
                        "details": outcome.details,
                    }
                )

            except PwTimeoutError:
                debug_dump(page, "timeout")
                log("ABORT: Timeout waiting for expected DOM state")
                return 1

            except PwError as e:
                debug_dump(page, "playwright-error")
                log(f"ABORT: Playwright error: {e!r}")
                return 1

            except RuntimeError as e:
                debug_dump(page, "runtime-error")
                log(f"ABORT: {e}")
                return 1

        log("All identifiers processed successfully")
        browser.close()

    out_path = write_json_results(run_id, structured_results)
    log(f"Saved results JSON: {out_path}")

    log("Session finished cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
