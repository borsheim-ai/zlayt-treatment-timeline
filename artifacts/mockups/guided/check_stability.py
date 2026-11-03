"""T-180 mockup check: click every in-page control on every page at 1440x900, 390x844, 320x640; assert no box moved, no overflow, no details/menus, no JS errors. Run: .venv/bin/python artifacts/mockups/guided/check_stability.py"""
from pathlib import Path
from playwright.sync_api import sync_playwright
root = Path("/Users/arsis/zlayt-pm-project/artifacts/mockups/guided")
BOX = """() => [...document.querySelectorAll('.steps .step, .btn, .question, .card, .card-f, .tile, .input-box, .count-box, .total-chip, .status')].map(el => {const r = el.getBoundingClientRect(); return [Math.round(r.x + scrollX), Math.round(r.y + scrollY), Math.round(r.width), Math.round(r.height)].join(',')})"""
fails = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for w, h in [(1440, 900), (390, 844), (320, 640)]:
        pg = b.new_page(viewport={"width": w, "height": h}); errs = []
        pg.on("pageerror", lambda ex: errs.append(str(ex)))
        for f in sorted(root.glob("*.html")):
            pg.goto(f.as_uri()); pg.wait_for_timeout(150)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            if sw > w: print("OVERFLOW", f.name, w, sw); fails += 1
            bad = pg.evaluate("() => document.querySelectorAll('details, [role=menu], [role=menubar]').length")
            if bad: print("HIDDEN-UI", f.name, bad); fails += 1
            # every in-page control: checkboxes, tiles, tappable sentences, theme
            ctrls = pg.locator("input[type=checkbox], .tile input, .sent, [data-theme-btn]")
            for i in range(ctrls.count()):
                el = ctrls.nth(i)
                if not el.is_visible() and not el.evaluate("e => e.closest('.tile') !== null"): continue
                target = el.locator("xpath=ancestor::label[1]") if el.evaluate("e => e.closest('label') !== null") else el
                target.scroll_into_view_if_needed(); pg.wait_for_timeout(60)
                y0 = pg.evaluate("scrollY"); before = pg.evaluate(BOX)
                target.click(); pg.wait_for_timeout(60)
                pg.evaluate(f"window.scrollTo(0, {y0})"); pg.wait_for_timeout(30)
                after = pg.evaluate(BOX)
                if before != after:
                    diff = [(x, y) for x, y in zip(before, after) if x != y][:3]
                    print("MOVED", f.name, w, i, diff); fails += 1
        if errs: print("JS ERRORS", w, errs); fails += 1
        pg.close()
    b.close()
print("fails", fails)
