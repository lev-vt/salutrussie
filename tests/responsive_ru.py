#!/usr/bin/env python3
"""Responsive smoke test for every RU HTML page. Run from a checked-out branch.
Install: python3 -m pip install playwright; python3 -m playwright install chromium firefox webkit
Run: python3 tests/responsive_ru.py --browsers chromium firefox webkit
"""
import argparse
import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
VIEWPORTS = [(320,568),(375,667),(390,844),(430,932),(480,800),
             (600,960),(768,1024),(820,1180),(1024,768),(1280,800),
             (1440,900),(1920,1080),(2560,1440),(667,375),(844,390)]
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--browsers", nargs="+", choices=["chromium","firefox","webkit"], default=["chromium"])
    parser.add_argument("--out", type=Path, default=Path("responsive-ru-results"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    pages = sorted((ROOT / "v3" / "ru").rglob("*.html"))
    if not pages:
        raise SystemExit("No RU HTML pages found")
    server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}/"
    issues, checked = [], 0
    try:
        with sync_playwright() as pw:
            for name in args.browsers:
                browser = getattr(pw, name).launch()
                try:
                    for width, height in VIEWPORTS:
                        context = browser.new_context(viewport={"width":width,"height":height}, reduced_motion="reduce", is_mobile=(name != "firefox" and width < 600), has_touch=width < 1024)
                        page = context.new_page()
                        errors = []
                        page.on("pageerror", lambda exc: errors.append(str(exc)))
                        for path in pages:
                            rel = path.relative_to(ROOT).as_posix()
                            errors.clear()
                            found = []
                            try:
                                response = page.goto(base + rel, wait_until="load", timeout=30000)
                                if not response or not response.ok:
                                    found.append("Page failed to load")
                                page.evaluate("document.fonts.ready")
                                data = page.evaluate("""() => {
                                  const root = document.documentElement;
                                  const body = document.body;
                                  const w = root.clientWidth;
                                  return {width:w, scroll:Math.max(root.scrollWidth,body.scrollWidth),
                                    viewport:!!document.querySelector('meta[name=viewport]'),
                                    broken:[...document.images].filter(i=>i.complete && !i.naturalWidth && (i.currentSrc||i.src)).map(i=>i.getAttribute('src'))};
                                }""")
                                if not data["viewport"]:
                                    found.append("Missing viewport meta")
                                if data["scroll"] > data["width"] + 2:
                                    found.append(f"Horizontal overflow: {data['scroll']} > {data['width']}")
                                if data["broken"]:
                                    found.append("Broken loaded image(s): " + ", ".join(data["broken"]))
                                burger = page.locator("#burger")
                                if burger.count() and burger.is_visible():
                                    burger.click(timeout=4000)
                                    if burger.get_attribute("aria-expanded") != "true" or not page.locator("#navLinks").is_visible():
                                        found.append("Mobile menu did not open")
                                    page.keyboard.press("Escape")
                                    if burger.get_attribute("aria-expanded") == "true":
                                        found.append("Mobile menu did not close with Escape")
                            except Exception as exc:
                                found.append(str(exc))
                            found.extend("JS: " + error for error in errors)
                            checked += 1
                            if found:
                                shot = args.out / f"{name}-{width}x{height}-{checked}.png"
                                try:
                                    page.screenshot(path=str(shot), timeout=5000)
                                except Exception:
                                    pass
                                issues.append({"browser":name,"viewport":[width,height],"page":rel,"issues":found})
                                print(name, width, height, rel, found, flush=True)
                        context.close()
                finally:
                    browser.close()
    finally:
        server.shutdown()
        server.server_close()
    report = {"pages":len(pages),"viewports":VIEWPORTS,"browsers":args.browsers,"checks":checked,"issues":issues}
    (args.out / "report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"{checked} checks; {len(issues)} page/viewport combinations flagged.")
    return bool(issues)

if __name__ == "__main__":
    raise SystemExit(main())
