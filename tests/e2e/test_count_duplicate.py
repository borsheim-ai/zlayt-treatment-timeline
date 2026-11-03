"""T-172 r2 (claims adjuster, major): a countable line the code says would double another charge carries `count_confirm` in the case view (contract: memory/contracts/api.md, 'Why an amount is
not counted, and counting it'). The page reads it BEFORE any dialog opens: the row shows the flag, "Count this charge" asks for the flag by name FIRST (the T-154 flagged-charge dialog), and only
then the named separate-charge confirm. The flag is never first met after a separate-charge confirm. No route stub: a real server (tests/e2e/_scripted_server.py: this tree's app with a scripted
call factory) runs a pasted SYNTHETIC two-record ledger, and the amounts, `count_confirm` and the count action are the backend's own."""
import json
import re
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import pathlib
import pytest
from playwright.sync_api import expect

ROOT = pathlib.Path(__file__).resolve().parents[2]
TEXT = "\n".join([
    "SYNTHETIC - invented for evaluation; not real patient data", "",
    "=== Record 1 ===", "Date: 2026-04-16", "Source: Clinic, billing statement", 'Excerpt: "Billing statement. 04/16/2026 manual therapy charge $150.00."', "",
    "=== Record 2 ===", "Date: 2026-05-01", "Source: ", 'Excerpt: "Manual therapy charge $150.00."', ""])
NAMED = "I checked this is a separate charge for a service"


@pytest.fixture(scope="module")
def base():
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    tmp = tempfile.mkdtemp(prefix="zlayt-dup-")
    log = open(tmp + "/server.log", "w")
    proc = subprocess.Popen([sys.executable, str(ROOT / "tests" / "e2e" / "_scripted_server.py"), tmp + "/dup.sqlite3", str(port)], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
    url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(url + "/api/health", timeout=1).read(); break
            except Exception:
                if proc.poll() is not None:
                    pytest.fail("scripted server exited: " + open(tmp + "/server.log").read()[-1500:])
                time.sleep(.5)
        else:
            pytest.fail("scripted server did not start")
        yield url
    finally:
        proc.terminate()
        try: proc.wait(timeout=10)
        except Exception: proc.kill()
        log.close()


def _api(base, method, path, body=None):
    req = urllib.request.Request(base + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read(); return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read(); return e.code, (json.loads(raw) if raw else None)


@pytest.fixture
def ledger(base):
    st, c = _api(base, "POST", "/api/cases", {"text": TEXT}); assert st in (200, 201), (st, c)
    tok = c["token"]; assert _api(base, "POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = _api(base, "GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready", s
    amounts = _api(base, "GET", f"/api/cases/{tok}")[1]["amounts"]
    und = next(a for a in amounts if a["kind"] != "charge" and a["countable"])
    assert und["count_confirm"] and und["count_confirm"]["flag"] == "likely_duplicate", und   # the real API shape (T-171 r2)
    yield tok, und
    _api(base, "DELETE", f"/api/cases/{tok}")


def _open(page, base, tok):
    page.goto(f"{base}/classic/#/case/{tok}"); page.get_by_test_id("timeline").wait_for(timeout=15000)
    page.get_by_test_id("charges-panel").wait_for()


def _loc(page, a):
    return page.get_by_test_id("charges-panel").locator(f'[data-item-id="{a["id"]}"]').first


def _row(page, a):
    r = _loc(page, a); r.scroll_into_view_if_needed(); return r


def _record_posts(page):
    posts = []
    page.on("request", lambda r: posts.append(json.loads(r.post_data or "{}")) if r.method == "POST" and r.url.endswith("/review") else None)
    return posts


def _kind(base, tok, a):
    return next(x for x in _api(base, "GET", f"/api/cases/{tok}")[1]["amounts"] if x["id"] == a["id"])["kind"]


def test_the_flag_is_in_the_row_before_any_click_and_is_asked_for_first(page, base, ledger):
    tok, a = ledger; posts = _record_posts(page)
    _open(page, base, tok)
    row = _row(page, a)
    chip = row.get_by_test_id("charge-flag")
    expect(chip).to_contain_text("Likely duplicate"); expect(chip).to_contain_text("count one service twice")   # the server's own sentence, before any click
    row.get_by_test_id("btn-count-charge").click()
    fd = page.get_by_test_id("charge-confirm")
    expect(fd).to_be_visible()                                                         # the FIRST dialog is the flag dialog, naming the flag
    expect(page.get_by_test_id("count-confirm")).to_be_hidden()
    expect(fd.get_by_test_id("charge-confirm-flag")).to_have_text("Likely duplicate"); expect(fd.get_by_test_id("charge-confirm-msg")).to_contain_text("count one service twice")
    expect(fd.get_by_test_id("btn-charge-cancel")).to_be_focused()
    fd.get_by_test_id("btn-charge-cancel").click(); expect(fd).to_be_hidden()
    assert posts == [] and _kind(base, tok, a) != "charge"                              # Cancel on the flag counts nothing, and the separate-charge dialog never opened
    expect(page.get_by_test_id("count-confirm")).to_be_hidden()
    row.get_by_test_id("btn-count-charge").click()
    fd.get_by_test_id("btn-charge-confirm").click()                                    # the flag, confirmed by name
    cd = page.get_by_test_id("count-confirm"); expect(cd).to_be_visible()              # only then the separate-charge confirm
    assert posts == []                                                                  # still nothing sent
    cd.get_by_test_id("btn-count-cancel").click(); expect(cd).to_be_hidden()
    assert posts == [] and _kind(base, tok, a) != "charge"
    row.get_by_test_id("btn-count-charge").click(); fd.get_by_test_id("btn-charge-confirm").click()
    expect(cd).to_be_visible(); cd.get_by_test_id("btn-count-confirm").click()
    expect(_loc(page, a)).to_have_attribute("data-amount-kind", "charge")
    assert posts == [{"action": "count", "confirm": "separate_charge", "confirm_flag": "likely_duplicate"}]   # one request, both confirms
    expect(_loc(page, a).get_by_test_id("charge-flag")).to_contain_text("You confirmed this flag")
    assert _kind(base, tok, a) == "charge"


def test_the_same_order_by_keyboard_alone(page, base, ledger):
    tok, a = ledger; posts = _record_posts(page)
    _open(page, base, tok)
    btn = _row(page, a).get_by_test_id("btn-count-charge"); btn.focus()
    page.keyboard.press("Enter")
    fd = page.get_by_test_id("charge-confirm"); expect(fd).to_be_visible(); expect(page.get_by_test_id("count-confirm")).to_be_hidden()
    page.keyboard.press("Escape"); expect(fd).to_be_hidden(); expect(btn).to_be_focused()
    assert posts == []
    page.keyboard.press("Enter"); expect(fd.get_by_test_id("btn-charge-cancel")).to_be_focused()
    page.keyboard.press("Tab"); page.keyboard.press("Enter")                           # flag confirmed
    cd = page.get_by_test_id("count-confirm"); expect(cd).to_be_visible(); expect(cd.get_by_test_id("btn-count-cancel")).to_be_focused()
    page.keyboard.press("Escape"); expect(cd).to_be_hidden(); assert posts == []
    page.keyboard.press("Enter"); page.keyboard.press("Tab"); page.keyboard.press("Enter")
    expect(cd).to_be_visible(); page.keyboard.press("Tab"); page.keyboard.press("Enter")
    expect(_loc(page, a)).to_have_attribute("data-amount-kind", "charge")
    assert posts == [{"action": "count", "confirm": "separate_charge", "confirm_flag": "likely_duplicate"}]


def test_the_flag_and_both_dialogs_fit_a_390px_screen(pw, base, ledger):
    tok, a = ledger
    b = pw.chromium.launch()
    try:
        pg = b.new_context(viewport={"width": 390, "height": 844}).new_page()
        _open(pg, base, tok)
        row = _row(pg, a); expect(row.get_by_test_id("charge-flag")).to_be_visible()
        bb = row.get_by_test_id("charge-flag").bounding_box(); assert bb["x"] >= 0 and bb["x"] + bb["width"] <= 390
        row.get_by_test_id("btn-count-charge").click()
        fd = pg.get_by_test_id("charge-confirm"); expect(fd).to_be_visible()
        for t in ("btn-charge-confirm", "btn-charge-cancel"):
            x = fd.get_by_test_id(t).bounding_box(); assert x["x"] >= 0 and x["x"] + x["width"] <= 390 and x["height"] >= 36 and x["y"] + x["height"] <= 844, (t, x)
        fd.get_by_test_id("btn-charge-confirm").click()
        cd = pg.get_by_test_id("count-confirm"); expect(cd).to_be_visible()
        cd.get_by_test_id("btn-count-confirm").click(); expect(cd).to_be_hidden()
        expect(_loc(pg, a)).to_have_attribute("data-amount-kind", "charge")
        assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    finally:
        b.close()
