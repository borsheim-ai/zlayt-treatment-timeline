"""Screenshot the board UI (M0 smoke §4.8.5). Usage: .venv/bin/python tools/screenshot_board.py [out.png] [--mobile]"""
import sys
from playwright.sync_api import sync_playwright

out = next((a for a in sys.argv[1:] if a.endswith(".png")), "artifacts/screenshots/m0-board.png")
mobile = "--mobile" in sys.argv
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844} if mobile else {"width": 1440, "height": 1000})
    pg.goto("http://localhost:7777/", wait_until="networkidle")
    pg.wait_for_selector(".card", timeout=10000)
    pg.screenshot(path=out, full_page=True)
    b.close()
print(out)
