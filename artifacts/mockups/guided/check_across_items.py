"""T-180 mockup check: step bar, answers, small buttons, question and cards sit at identical boxes on every review page (item to item moves nothing). Run: .venv/bin/python artifacts/mockups/guided/check_across_items.py"""
from pathlib import Path
from playwright.sync_api import sync_playwright
root = Path("/Users/arsis/zlayt-pm-project/artifacts/mockups/guided")
pages = ["step2-entry", "step2-fix", "step2-flag", "step2-gap", "step2-disputed", "step2-cannot-check", "step2-write", "step2-date", "step2-date-confirmed", "step3-charge", "step3-never", "step3-count"]
SEL = """() => [...document.querySelectorAll('.steps .step, .big .btn, .small .btn, .question, .card')].map(el => {const r = el.getBoundingClientRect(); return [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)].join(',')})"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(1440, 900), (390, 844)]:
        pg = b.new_page(viewport={"width": w, "height": h}); ref = None
        for n in pages:
            pg.goto((root / f"{n}.html").as_uri()); pg.wait_for_timeout(100)
            boxes = pg.evaluate(SEL)
            if ref is None: ref = boxes; continue
            if boxes != ref: print("DIFF", w, n, [(i, a, c) for i, (a, c) in enumerate(zip(ref, boxes)) if a != c][:4])
        pg.close()
    b.close()
print("done")
