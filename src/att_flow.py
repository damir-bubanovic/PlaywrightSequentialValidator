import time
from typing import Optional, Tuple

from playwright.sync_api import TimeoutError as PwTimeoutError, Error as PwError

from .types import Outcome
from .dom_utils import first_visible_text, dismiss_cookie_banner


def detect_unexpected_state(page) -> Optional[str]:
    """
    Abort on *visible* block/error states only, to avoid false positives from hidden HTML.
    """
    checks = [
        ("access denied", "text=/access denied/i"),
        ("request blocked", "text=/request blocked/i"),
        ("unusual activity", "text=/unusual activity/i"),
        ("captcha/robot", "text=/captcha|robot|verify you are a human/i"),
        ("temporarily unavailable", "text=/temporarily unavailable/i"),
        ("something went wrong", "text=/something went wrong/i"),
        ("service unavailable", "text=/service unavailable|\\b503\\b/i"),
    ]

    for label, selector in checks:
        try:
            loc = page.locator(selector)
            if loc.count() > 0 and loc.first.is_visible():
                return f"Detected unexpected block/error state (visible): '{label}'"
        except PwError:
            continue

    try:
        if "att.com" not in page.url:
            return f"Unexpected domain in URL: {page.url}"
    except PwError:
        pass

    return None


def wait_for_one_of(page, conditions: Tuple[Tuple[str, str], ...], timeout_ms: int) -> str:
    deadline = time.time() + (timeout_ms / 1000.0)
    last_err: Optional[str] = None

    while time.time() < deadline:
        unexpected = detect_unexpected_state(page)
        if unexpected:
            raise RuntimeError(unexpected)

        for name, selector in conditions:
            try:
                loc = page.locator(selector)
                if loc.count() > 0 and loc.first.is_visible():
                    return name
            except PwError as e:
                last_err = str(e)

        time.sleep(0.2)

    raise PwTimeoutError(last_err or "Timed out waiting for expected DOM state")


def find_imei_input(page):
    try:
        return page.get_by_label("IMEI", exact=False)
    except PwError:
        return page.locator(
            "input[aria-label*='IMEI' i], input[placeholder*='IMEI' i], "
            "input[id*='imei' i], input[name*='imei' i]"
        )


def find_continue_button(page):
    try:
        return page.get_by_role("button", name="Continue")
    except PwError:
        return page.locator("button:has-text('Continue'), input[type='submit']")


def extract_outcome(page, state_timeout_ms: int) -> Outcome:
    state = wait_for_one_of(
        page,
        conditions=(
            (
                "EID_PROMPT",
                "text=/\\bEID\\b/i, input[aria-label*='EID' i], input[id*='eid' i], input[name*='eid' i]",
            ),
            ("INVALID_IMEI", "text=/imei\\s*(not found)|try\\s*re-?entering|invalid|enter.*imei|15\\s*digit|digits/i"),
            (
                "INCOMPATIBLE",
                "text=/not compatible|incompatible|can\\x27t be activated|cannot be activated|not supported/i",
            ),
            ("NEXT_STEP", "text=/Step\\s*3\\s*of\\s*4|Choose your plan/i"),
        ),
        timeout_ms=state_timeout_ms,
    )

    if state == "EID_PROMPT":
        return Outcome(kind="NEEDS_EID", details="EID prompt detected after IMEI submission")

    if state == "INVALID_IMEI":
        msg = first_visible_text(
            page,
            candidates=(
                "[role='alert']",
                ".error, .errors, .form-error, .error-message",
                "text=/imei\\s*not found|try\\s*re-?entering/i",
                "text=/invalid|enter.*imei|15\\s*digit|digits/i",
            ),
        ) or "Validation error detected"
        return Outcome(kind="INVALID", details=msg)

    if state == "INCOMPATIBLE":
        msg = first_visible_text(
            page,
            candidates=(
                "[role='alert']",
                ".error, .errors, .form-error, .error-message",
                "text=/not compatible|incompatible|can\\x27t be activated|cannot be activated|not supported/i",
            ),
        ) or "Incompatible message detected"
        return Outcome(kind="INCOMPATIBLE", details=msg)

    if state == "NEXT_STEP":
        device_name = first_visible_text(
            page,
            candidates=(
                "h1",
                "h2",
                "[data-testid*='device' i]",
                "text=/Device|Model/i",
            ),
        )
        details = "Advanced to next step (Choose your plan)"
        if device_name:
            details = f"{details}; visible heading: {device_name}"
        return Outcome(kind="OK", details=details)

    raise RuntimeError(f"Unhandled state returned by detector: {state}")


def process_identifier(page, identify_url: str, identifier: str, nav_timeout_ms: int, state_timeout_ms: int) -> Outcome:
    page.goto(identify_url, timeout=nav_timeout_ms, wait_until="domcontentloaded")
    dismiss_cookie_banner(page)

    unexpected = detect_unexpected_state(page)
    if unexpected:
        raise RuntimeError(unexpected)

    imei_input = find_imei_input(page)
    if imei_input.count() == 0:
        raise RuntimeError("Could not find IMEI input (DOM selector failure)")

    imei_input.first.click()

    try:
        imei_input.first.fill("")
    except PwError:
        imei_input.first.press("Control+A")
        imei_input.first.press("Backspace")

    imei_input.first.type(identifier, delay=25)

    continue_btn = find_continue_button(page)
    if continue_btn.count() == 0:
        raise RuntimeError("Could not find Continue button (DOM selector failure)")

    try:
        continue_btn.first.click(timeout=2000)
    except PwError:
        # If disabled, the DOM should still show the validation error.
        pass

    try:
        page.wait_for_load_state("domcontentloaded", timeout=10_000)
    except PwError:
        pass

    return extract_outcome(page, state_timeout_ms)
