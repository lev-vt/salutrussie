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
    for localised in ("en/index.html", "en/services/index.html", "en/migration/index.html", "en/migration/decree-702/index.html", "en/migration/rvp/index.html", "en/migration/vnzh/index.html", "en/migration/citizenship/index.html", "en/migration/visas/index.html", "en/migration/family/index.html", "en/migration/students/index.html", "en/migration/disputes/index.html", "en/real-estate/index.html", "en/real-estate/rent/index.html", "en/real-estate/buy/index.html", "en/real-estate/legal-check/index.html", "en/business/index.html", "en/business/company-registration/index.html", "en/business/legal-support/index.html", "en/business/tax-consulting/index.html", "en/investments/index.html", "en/investments/project-selection/index.html", "en/investments/legal-due-diligence/index.html", "en/investments/project-support/index.html", "en/legal/index.html", "en/legal/document-preparation/index.html", "en/legal/disputes/index.html", "en/relocation/index.html", "en/relocation/administrative-procedures/index.html", "en/relocation/everyday-life/index.html", "en/relocation/russian-language/index.html", "en/for-business/index.html", "en/for-business/employers/index.html", "en/for-business/foreign-companies/index.html", "en/for-business/recruitment-partners/index.html", "en/consultations/index.html", "en/about/index.html", "en/contacts/index.html", "en/payment/index.html", "en/pricing/index.html", "en/offer/index.html", "en/privacy/index.html", "en/knowledge/index.html", "en/knowledge/articles/visa-expires-after-rvp-vnzh-filing/index.html", "en/knowledge/articles/rvp-shared-values-702/index.html", "en/knowledge/articles/vnzh-annual-notification-2027/index.html", "en/knowledge/articles/vnzh-red-diploma/index.html", "en/knowledge/articles/registration-foreigner-landlord/index.html", "en/knowledge/articles/hqs-dismissal-visa/index.html", "en/knowledge/articles/how-to-choose-residence/index.html", "en/knowledge/articles/renting-a-home/index.html", "fr/consultations/index.html"):
        page_path = ROOT / "v3" / localised
        if page_path.is_file():
            pages.append(page_path)
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
                                # Legacy alias uses a zero-delay HTML refresh; wait for its real destination.
                                if rel == "v3/ru/migration/decree-702-design/index.html":
                                    page.wait_for_url(base + "v3/ru/migration/decree-702/", wait_until="load", timeout=10000)
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
                                    offenders = page.evaluate("""() => [...document.querySelectorAll('body *')]
                                      .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.right > document.documentElement.clientWidth + 2; })
                                      .map(el => ({tag:el.tagName, cls:typeof el.className === 'string' ? el.className : '', right:Math.round(el.getBoundingClientRect().right)}))
                                      .sort((a,b)=>b.right-a.right).slice(0,12)""")
                                    found.append("Overflow candidates: " + json.dumps(offenders, ensure_ascii=False))
                                if data["broken"]:
                                    found.append("Broken loaded image(s): " + ", ".join(data["broken"]))
                                if rel == "v3/en/knowledge/index.html":
                                    if page.locator(".sr-result:not(.sr-hidden)").count() != 12:
                                        found.append("English catalogue does not show all 12 publications")
                                    page.locator("#sr-search").fill("Decree 702")
                                    if page.locator(".sr-result:not(.sr-hidden)").count() == 0:
                                        found.append("English catalogue search returned no Decree 702 results")
                                    page.locator("#sr-search").fill("zzzz-no-matching-article")
                                    if not page.locator("#sr-empty").is_visible() or page.locator("#sr-count").inner_text() != "0 results":
                                        found.append("English catalogue empty search state incorrect")
                                    page.locator("#sr-search").fill("")
                                    page.locator('[data-topic-filter="business"]').click()
                                    if page.locator('.sr-result:not(.sr-hidden)[data-topic]:not([data-topic="business"])').count() or page.locator(".sr-result:not(.sr-hidden)").count() != 4:
                                        found.append("English catalogue business filter incorrect")
                                    page.locator('[data-topic-filter="all"]').click()
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
