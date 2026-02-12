from datetime import datetime, timezone
from playwright.sync_api import Error as PwError

from .logging_utils import log


def debug_dump(page, label: str) -> None:
    """
    Minimal debug capture to support DOM selector tuning:
    - screenshot
    - url/title
    - visible headings (h1/h2)
    """
    try:
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        path = f"docs/runs/debug-{label}-{ts}.png"
        page.screenshot(path=path, full_page=True)
        log(f"DEBUG screenshot saved: {path}")
    except PwError as e:
        log(f"DEBUG screenshot failed: {e!r}")

    try:
        log(f"DEBUG url: {page.url}")
    except PwError:
        pass

    try:
        title = page.title()
        if title:
            log(f"DEBUG title: {title}")
    except PwError:
        pass

    try:
        headings = page.locator("h1, h2").all_inner_texts()
        headings = [h.strip() for h in headings if h and h.strip()]
        if headings:
            log(f"DEBUG headings: {headings[:5]}")
    except PwError:
        pass
