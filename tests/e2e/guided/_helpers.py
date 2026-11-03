"""Shared helpers for the guided specs of Builder A (home, step 1, step 4). T-181 (D-068). Not a test module."""
import json
import os
import re
import time
import uuid
import tests.e2e.conftest as C

SHOTS = os.path.join(C.ROOT, "artifacts", "screenshots", "guided")


def uid():
    return uuid.uuid4().hex[:6]


def api(method, path, body=None):
    return C.api(method, path, body)


def make_case(title, run=True, decide=False, sample=True):
    """A sample case over the API: ingested, or drafted (ready), or drafted with every item accepted."""
    st, c = api("POST", "/api/cases", {"sample": True, "title": title}); assert st == 201, c
    tok = c["token"]
    if run:
        assert api("POST", f"/api/cases/{tok}/run", {"confirm_rerun": False})[0] == 202
        for _ in range(240):
            s = api("GET", f"/api/cases/{tok}/status")[1]
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(.5)
        assert s["status"] == "ready", s
    if decide:
        decide_all(tok)
    return tok


def decide_all(tok, action="accept"):
    """Step 2 and 3 are another builder's: answer every item over the API (accept)."""
    c = api("GET", f"/api/cases/{tok}")[1]
    for i in c["entries"] + c["undated_entries"] + c["flags"] + c["amounts"]:
        st, r = api("POST", f"/api/cases/{tok}/items/{i['id']}/review", {"action": action})
        assert st == 200, (i["id"], st, r)


def golden_letter():
    txt = open(os.path.join(C.SAMPLE_PATH, "sample.export.expected.txt")).read()
    return txt.split("=== LETTER_TEXT (block 1: paste into letter) ===\n")[1].split("=== INTERNAL_NOTES_TEXT")[0].rstrip("\n")


def golden_notes():
    txt = open(os.path.join(C.SAMPLE_PATH, "sample.export.expected.txt")).read()
    notes = txt.split("=== INTERNAL_NOTES_TEXT (block 2: do not send) ===\n")[1].rstrip("\n")
    from app.backend import export      # D-069: the golden predates the prepared disclosure line the curated demo now prints
    return notes.replace(export.AI_LINE.split("{n}")[0], export.AI_LINE_PREPARED.split("{n}")[0])


def browser(pw, w, h, scheme="light", **kw):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme, permissions=["clipboard-read", "clipboard-write"], accept_downloads=True, **kw)
    return b, ctx.new_page()


def shot(page, name, w):
    os.makedirs(SHOTS, exist_ok=True)
    page.screenshot(path=os.path.join(SHOTS, f"{name}-{w}.png"))


def in_view(page, loc):
    """True when the element's whole box is inside the viewport with the page scrolled to the top (nothing to scroll to reach it)."""
    page.evaluate("window.scrollTo(0, 0)")
    b = loc.bounding_box(); vh = page.viewport_size["height"]; vw = page.viewport_size["width"]
    return bool(b) and b["y"] >= 0 and b["y"] + b["height"] <= vh and b["x"] >= 0 and b["x"] + b["width"] <= vw


def no_h_scroll(page):
    return page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")


def go(page, path="/"):
    page.goto(C.SERVER + path)
    page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=15000)


def jbody(route, status=200, payload=None):
    route.fulfill(status=status, content_type="application/json", body=json.dumps(payload))


def err(code, message, detail=None):
    return {"error": {"code": code, "message": message, "detail": detail or {}}}
