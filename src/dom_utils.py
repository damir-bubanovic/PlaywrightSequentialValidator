from typing import Optional
from playwright.sync_api import Error as PwError


def first_visible_text(page, candidates) -> Optional[str]:
    for sel in candidates:
        try:
            loc = page.locator(sel)
            if loc.count() > 0 and loc.first.is_visible():
                txt = loc.first.inner_text().strip()
                if txt:
                    return txt
        except PwError:
            continue
    return None


def dismiss_cookie_banner(page) -> None:
    """
    Best-effort dismissal of AT&T cookie banner.
    If it isn't present, does nothing.
    """
    candidates = [
        "button:has-text('Continue without changes')",
        "button:has-text('Accept')",
        "button:has-text('I agree')",
    ]
    for sel in candidates:
        try:
            loc = page.locator(sel)
            if loc.count() > 0 and loc.first.is_visible():
                loc.first.click(timeout=2000)
                page.wait_for_timeout(300)
                return
        except PwError:
            continue
