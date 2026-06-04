from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass

DEFAULT_REQUIRED_TEXT = (
    "public-data anchored benchmark",
    "not linked-data calibrated",
    "not a patient-level forecast",
    "Reference scenarios",
)
GENERIC_ERROR_TEXT = (
    "Oh no.",
    "Error running app",
    "Error installing requirements",
    "Click \"Manage App\"",
)


def collect_frame_text(page, timeout_seconds: int) -> tuple[str, ...]:
    texts: list[str] = []
    for frame in page.frames:
        if frame == page.main_frame:
            continue
        try:
            text = frame.locator("body").inner_text(timeout=timeout_seconds * 1000)
        except Exception:
            continue
        if text:
            texts.append(text)
    return tuple(texts)


def safe_print(text: str) -> None:
    encoding = sys.stdout.encoding or "utf-8"
    print(text.encode(encoding, errors="backslashreplace").decode(encoding))


@dataclass(frozen=True)
class SmokeResult:
    ok: bool
    url: str
    title: str
    body_text: str
    frame_text: tuple[str, ...]
    console_events: tuple[str, ...]
    failed_requests: tuple[str, ...]
    missing_text: tuple[str, ...]
    generic_errors: tuple[str, ...]
    exception: str | None = None


def run_remote_smoke(url: str, settle_seconds: int, timeout_seconds: int) -> SmokeResult:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "playwright is required for remote Streamlit smoke checks. "
            "Install it with `pip install playwright` and `python -m playwright install chromium`."
        ) from exc

    console_events: list[str] = []
    failed_requests: list[str] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(viewport={"width": 1440, "height": 1100})
            page.on("console", lambda msg: console_events.append(f"{msg.type}: {msg.text[:500]}"))
            page.on("pageerror", lambda err: console_events.append(f"pageerror: {str(err)[:500]}"))
            page.on(
                "requestfailed",
                lambda req: failed_requests.append(f"{req.method} {req.url} {req.failure}"),
            )
            page.goto(url, wait_until="domcontentloaded", timeout=timeout_seconds * 1000)
            page.wait_for_timeout(settle_seconds * 1000)
            body_text = page.locator("body").inner_text(timeout=timeout_seconds * 1000)
            frame_text = collect_frame_text(page, timeout_seconds)
            title = page.title()
            final_url = page.url
        except Exception as exc:
            return SmokeResult(
                ok=False,
                url=url,
                title="",
                body_text="",
                frame_text=(),
                console_events=tuple(console_events),
                failed_requests=tuple(failed_requests),
                missing_text=DEFAULT_REQUIRED_TEXT,
                generic_errors=(),
                exception=f"{type(exc).__name__}: {exc}",
            )
        finally:
            browser.close()

    searchable_text = "\n".join((body_text, *frame_text))
    missing_text = tuple(text for text in DEFAULT_REQUIRED_TEXT if text not in searchable_text)
    generic_errors = tuple(text for text in GENERIC_ERROR_TEXT if text in searchable_text)
    return SmokeResult(
        ok=not missing_text and not generic_errors,
        url=final_url,
        title=title,
        body_text=body_text,
        frame_text=frame_text,
        console_events=tuple(console_events),
        failed_requests=tuple(failed_requests),
        missing_text=missing_text,
        generic_errors=generic_errors,
    )


def print_result(result: SmokeResult, attempt: int) -> None:
    print(f"remote Streamlit smoke attempt {attempt}")
    print(f"url: {result.url}")
    print(f"title: {result.title}")
    print(f"ok: {result.ok}")
    print(f"missing_text: {list(result.missing_text)}")
    print(f"generic_errors: {list(result.generic_errors)}")
    if result.exception:
        print(f"exception: {result.exception}")
    if result.console_events:
        print("console_events:")
        for event in result.console_events[:20]:
            safe_print(f"- {event}")
    if result.failed_requests:
        print("failed_requests:")
        for request in result.failed_requests[:20]:
            safe_print(f"- {request}")
    print("body_text_start")
    safe_print(result.body_text[:3000])
    print("body_text_end")
    for index, text in enumerate(result.frame_text[:5], start=1):
        print(f"frame_{index}_text_start")
        safe_print(text[:3000])
        print(f"frame_{index}_text_end")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://gtpcnz.streamlit.app/")
    parser.add_argument("--attempts", type=int, default=6)
    parser.add_argument("--sleep-seconds", type=int, default=60)
    parser.add_argument("--settle-seconds", type=int, default=45)
    parser.add_argument("--timeout-seconds", type=int, default=90)
    args = parser.parse_args()

    last_result: SmokeResult | None = None
    for attempt in range(1, max(1, args.attempts) + 1):
        result = run_remote_smoke(args.url, args.settle_seconds, args.timeout_seconds)
        last_result = result
        print_result(result, attempt)
        if result.ok:
            return 0
        if attempt < args.attempts:
            time.sleep(max(0, args.sleep_seconds))

    if last_result is not None:
        print(
            "remote Streamlit smoke failed: deployed app did not expose the required public dashboard "
            "contract or showed a generic Streamlit error.",
            file=sys.stderr,
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
