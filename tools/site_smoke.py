"""Load the public pages in headless Chromium and check layout, errors, and redirects.

Local helper (needs Playwright, not used in CI):
    python tools/site_smoke.py --out /tmp/site-shots
"""

from __future__ import annotations

import argparse
import functools
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGES = ["index.html", "open-problems.html", "negative-results.html", "how-it-works.html"]
REDIRECTS = {
    "methodology.html": "how-it-works.html",
    "repomap.html": "how-it-works.html",
    "frontier.html": "open-problems.html",
    "proof-debt.html": "open-problems.html",
}


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args: object) -> None:
        pass


def serve(root: Path) -> ThreadingHTTPServer:
    handler = functools.partial(QuietHandler, directory=str(root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


def check_page(browser, base: str, name: str, width: int, out: Path | None) -> list[str]:
    page = browser.new_page(viewport={"width": width, "height": 900})
    errors: list[str] = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    page.goto(f"{base}/{name}", wait_until="networkidle")
    page.wait_for_timeout(400)
    problems = [f"{name} @{width}px: console error: {error}" for error in errors]
    if page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1"):
        problems.append(f"{name} @{width}px: horizontal overflow")
    if "Loading" in page.inner_text("body"):
        problems.append(f"{name} @{width}px: still shows a loading message")
    if out is not None:
        page.screenshot(path=str(out / f"{Path(name).stem}-{width}.png"), full_page=True)
    page.close()
    return problems


def check_redirect(browser, base: str, source: str, target: str) -> list[str]:
    page = browser.new_page()
    page.goto(f"{base}/{source}")
    try:
        page.wait_for_url(f"**/{target}*", timeout=5000)
        problems: list[str] = []
    except Exception:
        problems = [f"{source}: did not redirect to {target} (ended at {page.url})"]
    page.close()
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--pages", default=",".join(PAGES))
    parser.add_argument("--widths", default="1440,390")
    parser.add_argument("--out", type=Path, default=None, help="Directory for full-page screenshots.")
    parser.add_argument("--no-redirects", action="store_true")
    args = parser.parse_args(argv)
    if args.out is not None:
        args.out.mkdir(parents=True, exist_ok=True)

    server = serve(ROOT)
    base = f"http://127.0.0.1:{server.server_address[1]}"
    problems: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for name in [p for p in args.pages.split(",") if p]:
            for width in [int(w) for w in args.widths.split(",")]:
                problems += check_page(browser, base, name, width, args.out)
        if not args.no_redirects:
            for source, target in REDIRECTS.items():
                problems += check_redirect(browser, base, source, target)
        browser.close()
    server.shutdown()

    for problem in problems:
        print(problem)
    print("Smoke checks passed." if not problems else f"{len(problems)} problem(s).")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
