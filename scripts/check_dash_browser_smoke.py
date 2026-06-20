from __future__ import annotations

import argparse
import os
import socket
import subprocess
import sys
import time
from collections.abc import Iterable
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAST_ROUTES = (
    "/",
    "/reference-scenarios",
    "/model-surface",
    "/calibration-diagnostics",
    "/runtime-health",
)
FULL_ROUTES = (
    *FAST_ROUTES,
    "/live-model",
    "/scenario-builder?scheduled_benefit_level=90&quality_outcome_weight=70&seed=123",
    "/advanced-visuals",
)
VIEWPORTS = (
    ("desktop", {"width": 1440, "height": 1100}),
    ("mobile", {"width": 390, "height": 844}),
)
REQUIRED_TEXT = (
    "public-data anchored benchmark",
    "not linked-data calibrated",
    "not a patient-level forecast",
)
ROUTE_REQUIRED_TEXT = {
    "/reference-scenarios": ("Download CSV", "Table fallback"),
    "/live-model": ("Run simulation", "Run provenance", "Table fallback"),
    "/guided": ("Guided mode",),
    "/scenario-builder": ("Custom scenario comparison", "not calibrated and not a policy forecast"),
    "/model-surface": ("Model surface", "Surface coverage status"),
    "/calibration-diagnostics": ("Calibration diagnostics", "Posterior predictive checks"),
    "/advanced-visuals": ("Advanced visuals", "Value of information"),
    "/runtime-health": ("Runtime health", "not model-validation evidence"),
    "/public-cockpit": ("Public cockpit",),
}
ROUTE_MIN_GRAPHS = {
    "/reference-scenarios": 1,
    "/model-surface": 1,
    "/calibration-diagnostics": 1,
    "/live-model": 1,
    "/scenario-builder": 1,
    "/advanced-visuals": 1,
}


@dataclass(frozen=True)
class BrowserSmokeResult:
    ok: bool
    route: str
    viewport: str
    missing_text: tuple[str, ...]
    console_events: tuple[str, ...]
    failed_requests: tuple[str, ...]
    graph_count: int
    download_ok: bool | None = None
    provenance_ok: bool | None = None
    exception: str | None = None


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _wait_for_server(base_url: str, timeout_seconds: int) -> None:
    import urllib.request

    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(base_url, timeout=2) as response:
                if response.status == 200:
                    return
        except Exception as exc:
            last_error = exc
            time.sleep(0.5)
    raise RuntimeError(f"Dash server did not become ready at {base_url}: {last_error}")


def _route_key(route: str) -> str:
    return route.split("?", 1)[0]


def _screenshot_name(viewport_name: str, route: str) -> str:
    slug = _route_key(route).strip("/").replace("/", "-") or "start"
    return f"{viewport_name}-{slug}.png"


def _check_route(
    page,
    base_url: str,
    route: str,
    viewport_name: str,
    viewport: dict[str, int],
    timeout_seconds: int,
    screenshot_dir: Path | None,
) -> BrowserSmokeResult:
    console_events: list[str] = []
    failed_requests: list[str] = []
    page.set_viewport_size(viewport)
    page.on("console", lambda msg: console_events.append(f"{msg.type}: {msg.text[:500]}"))
    page.on("pageerror", lambda err: console_events.append(f"pageerror: {str(err)[:500]}"))
    page.on("requestfailed", lambda req: failed_requests.append(f"{req.method} {req.url} {req.failure}"))

    step_timeout_ms = min(timeout_seconds * 1000, 15_000)
    try:
        page.goto(f"{base_url}{route}", wait_until="domcontentloaded", timeout=step_timeout_ms)
        route_required = [*REQUIRED_TEXT, *ROUTE_REQUIRED_TEXT.get(_route_key(route), ())]
        for anchor_text in route_required:
            with suppress(Exception):
                page.wait_for_function(
                    "text => document.body && document.body.innerText.includes(text)",
                    arg=anchor_text,
                    timeout=min(timeout_seconds * 1000, 20_000),
                )
        if ROUTE_MIN_GRAPHS.get(_route_key(route), 0) > 0:
            with suppress(Exception):
                page.locator(".js-plotly-plot").first.wait_for(timeout=min(timeout_seconds * 1000, 20_000))
        page.wait_for_timeout(500)
        body_text = page.locator("body").inner_text(timeout=min(timeout_seconds * 1000, 20_000))
        graph_count = page.locator(".js-plotly-plot").count()
        download_ok: bool | None = None
        provenance_ok: bool | None = None
        route_key = _route_key(route)
        if route_key == "/reference-scenarios" and viewport_name == "desktop":
            with suppress(Exception):
                page.locator("summary", has_text="Run provenance").first.click(timeout=3_000)
                provenance_ok = page.locator("text=Calculation mode").first.is_visible(timeout=3_000)
            try:
                with page.expect_download(timeout=8_000) as download_info:
                    page.locator("#compare-download-button").click(timeout=5_000)
                download = download_info.value
                download_ok = download.suggested_filename.endswith(".csv")
            except Exception:
                download_ok = False
        if screenshot_dir is not None:
            screenshot_dir.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(screenshot_dir / _screenshot_name(viewport_name, route)), full_page=False)
    except Exception as exc:
        return BrowserSmokeResult(
            ok=False,
            route=route,
            viewport=viewport_name,
            missing_text=REQUIRED_TEXT,
            console_events=tuple(console_events),
            failed_requests=tuple(failed_requests),
            graph_count=0,
            exception=f"{type(exc).__name__}: {exc}",
        )

    required = [*REQUIRED_TEXT, *ROUTE_REQUIRED_TEXT.get(_route_key(route), ())]
    missing_text = tuple(text for text in required if text not in body_text)
    serious_console = tuple(event for event in console_events if event.startswith(("error:", "pageerror:")))
    interaction_failures = (download_ok is False) or (provenance_ok is False)
    graph_failure = graph_count < ROUTE_MIN_GRAPHS.get(_route_key(route), 0)
    return BrowserSmokeResult(
        ok=not missing_text and not serious_console and not failed_requests and not interaction_failures and not graph_failure,
        route=route,
        viewport=viewport_name,
        missing_text=missing_text,
        console_events=serious_console,
        failed_requests=tuple(failed_requests),
        graph_count=graph_count,
        download_ok=download_ok,
        provenance_ok=provenance_ok,
    )


def run_browser_smoke(
    base_url: str,
    routes: Iterable[str],
    timeout_seconds: int,
    screenshot_dir: Path | None,
) -> tuple[BrowserSmokeResult, ...]:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError(
            "playwright is required for Dash browser smoke checks. "
            "Install it in the active environment and run `python -m playwright install chromium`."
        ) from exc

    results: list[BrowserSmokeResult] = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for viewport_name, viewport in VIEWPORTS:
                for route in routes:
                    page = browser.new_page()
                    try:
                        print(f"checking {viewport_name} {route}", flush=True)
                        results.append(
                            _check_route(page, base_url, route, viewport_name, viewport, timeout_seconds, screenshot_dir)
                        )
                    finally:
                        page.close()
        finally:
            with suppress(Exception):
                browser.close()
    return tuple(results)


def _start_server(port: int) -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, "-m", "dash_app.app"],
        cwd=ROOT,
        env={**os.environ, "PORT": str(port)},
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run browser smoke checks against the Dash public surface.")
    parser.add_argument("--base-url")
    parser.add_argument("--timeout-seconds", type=int, default=30)
    parser.add_argument("--full", action="store_true", help="Include heavier live-model and scenario-builder routes.")
    parser.add_argument("--screenshot-dir", type=Path, help="Optional directory for viewport screenshots.")
    args = parser.parse_args(argv)

    process: subprocess.Popen | None = None
    if args.base_url:
        base_url = args.base_url.rstrip("/")
    else:
        port = _free_port()
        base_url = f"http://127.0.0.1:{port}"
        process = _start_server(port)
        _wait_for_server(base_url, args.timeout_seconds)

    try:
        routes = FULL_ROUTES if args.full else FAST_ROUTES
        results = run_browser_smoke(base_url, routes, args.timeout_seconds, args.screenshot_dir)
    finally:
        if process is not None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()

    ok = all(result.ok for result in results)
    for result in results:
        print(
            f"{result.viewport} {result.route}: ok={result.ok} "
            f"graphs={result.graph_count} missing={list(result.missing_text)} "
            f"download_ok={result.download_ok} provenance_ok={result.provenance_ok} "
            f"failed_requests={len(result.failed_requests)} console_errors={len(result.console_events)} "
            f"exception={result.exception or ''}"
        )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
