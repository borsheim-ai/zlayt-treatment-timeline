"""T-045 AC3: the whole paralegal journey (paste -> analyze -> review -> export -> reload) with the keyboard only, and again on a 375 px phone.

Real backend, fixture LLM set (a plain `pytest tests/e2e` starts its own server). The journey starts on the home screen and ends on the Export screen; nothing is set up by API
except the final comparison (the letter is checked against the server's own accepted set, never against a copy kept in the test).

Keyboard only (R-RV-4, WCAG 2.1.1): the only input events are Tab and key presses (the paste is `keyboard.insert_text`, which is what the OS paste does). A capture-phase listener counts
every click that came from a pointer (`event.detail > 0`); a keyboard Enter or Space on a button is a click with detail 0. The count must be 0 at the end.
375 px (R-ST-1, mobile): same journey by tap; no sideways scroll on any screen, and the main controls are tap-sized (the 44 px bar the other mobile specs use)."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, golden_text
import tests.e2e.conftest as C

COUNT_POINTER_CLICKS = "window.__ptr = 0; document.addEventListener('click', e => { if (e.detail > 0) window.__ptr++; }, true);"


def _active(pg):
    return pg.evaluate("(() => { const a = document.activeElement; return a ? { tid: a.getAttribute('data-testid'), item: a.getAttribute('data-item-id'), tag: a.tagName } : null; })()")


def _tab_until(pg, testid, limit=60):
    for _ in range(limit):
        pg.keyboard.press("Tab")
        a = _active(pg)
        if a and a["tid"] == testid:
            return a
    raise AssertionError(f"Tab never reached {testid}; last {_active(pg)}")


def _token(pg):
    m = re.search(r"#/case/([^/?#]+)", pg.url); assert m, pg.url
    return m.group(1)


PHONE_W = 375


def _no_sideways_scroll(pg, where):
    """The page is no wider than the 375 px phone. Not `scrollWidth <= innerWidth`: under is_mobile Chromium widens window.innerWidth to the content width, so that compares the page with
    itself and can never fail (T-045 r2, F1). The bound is the viewport the context was built with and the visual viewport the phone really shows; both must hold."""
    m = pg.evaluate("({ scroll: document.documentElement.scrollWidth, body: document.body.scrollWidth, inner: window.innerWidth, visual: window.visualViewport.width })")
    assert abs(m["visual"] - PHONE_W) <= 1, f"the emulated phone is not {PHONE_W} px wide: {m}"                      # guard: the measurement itself is still a 375 px phone
    assert m["scroll"] <= PHONE_W + 1 and m["body"] <= PHONE_W + 1, f"sideways scroll on {where}: {m}"


def _pending(pg):
    """Items still undecided on screen, in every list (entries, flags, charges); the entries queue alone is not the whole review."""
    return pg.locator('[data-item-id][data-review=pending]').evaluate_all("els => new Set(els.map(e => e.getAttribute('data-item-id'))).size")


def _accepted_summaries(tok):
    c = api("GET", f"/api/cases/{tok}")[1]
    return c, [e for e in c["entries"] if e["review_status"] in ("accepted", "edited")]


def _dated(letter):
    return len(re.findall(r"^[A-Z][a-z]+ \d+, 2026 — ", letter, re.M))


@pytest.fixture
def made():
    toks = []
    yield toks
    for t in toks:
        api("DELETE", f"/api/cases/{t}")


def test_whole_journey_with_the_keyboard_only(pw, made):
    """Home -> paste -> Analyze -> Start review -> d on the item Do this first names and on one entry, a on everything else -> x -> Export -> Copy -> reload: no pointer click anywhere, the letter holds exactly the
    accepted entries, and every decision is still there after the reload (ship bar 5; R-RV-1, R-RV-5, R-RV-8, R-EX-1)."""
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    ctx.add_init_script(COUNT_POINTER_CLICKS); pg = ctx.new_page()
    try:
        pg.goto(C.BASE); pg.get_by_test_id("input-text").wait_for(timeout=15000)
        _tab_until(pg, "input-text"); pg.keyboard.insert_text(golden_text("sample.txt"))
        _tab_until(pg, "btn-analyze"); pg.keyboard.press("Enter")
        pg.get_by_test_id("timeline").wait_for(timeout=60000); tok = _token(pg); made.append(tok)
        # the pipeline finished: review starts from the first skip link
        _tab_until(pg, "skip-review", 8); pg.keyboard.press("Enter")
        first = _active(pg)["item"]; assert first, "Start review did not land on an item"      # Do this first names the open rate row (a2), not an entry
        pg.keyboard.press("d")                                                                    # dismiss whatever Do this first named
        expect(pg.locator(f'[data-item-id="{first}"]').first).to_have_attribute("data-review", "dismissed")
        entry_ids = {e["id"] for e in api("GET", f"/api/cases/{tok}")[1]["entries"]}
        for _ in range(40):                                                                       # k up to the last undecided entry (entries sit above flags and charges) and dismiss it too: its summary must stay out of the letter
            cur = _active(pg)["item"]
            if cur in entry_ids and pg.locator(f'[data-item-id="{cur}"]').first.get_attribute("data-review") == "pending":
                break
            pg.keyboard.press("k"); pg.wait_for_timeout(80)
        gone_id = _active(pg)["item"]; assert gone_id in entry_ids, _active(pg)
        gone = next(e for e in api("GET", f"/api/cases/{tok}")[1]["entries"] if e["id"] == gone_id)
        pg.keyboard.press("d")
        expect(pg.locator(f'[data-item-id="{gone_id}"]').first).to_have_attribute("data-review", "dismissed")
        for _ in range(80):
            if _pending(pg) == 0:
                break
            pg.keyboard.press("a")
            pg.wait_for_timeout(120)
        assert _pending(pg) == 0, "the keyboard flow left items undecided"
        pg.keyboard.press("x"); assert _active(pg)["tid"] == "btn-export", _active(pg)
        pg.keyboard.press("Enter")
        expect(pg.get_by_test_id("export-letter")).to_be_visible(timeout=15000)
        letter = pg.get_by_test_id("export-letter").inner_text()
        c, acc = _accepted_summaries(tok)
        assert len(acc) == len(c["entries"]) - 1 == 8 and _dated(letter) == 8
        assert all(e["summary"] in letter for e in acc) and gone["summary"] not in letter
        assert "Billed charges accepted from these records:" in letter
        assert "8 of 9" in pg.get_by_test_id("count-line").inner_text() and "8 of 9" not in letter
        _tab_until(pg, "btn-copy-letter", 12); pg.keyboard.press("Space")
        expect(pg.locator("#export-status")).to_contain_text("Copied the treatment section")
        assert pg.evaluate("navigator.clipboard.readText()").startswith("TREATMENT CHRONOLOGY")
        assert pg.evaluate("window.__ptr") == 0, "a pointer click happened in the keyboard-only journey"
        # decisions survive a reload
        pg.reload(); pg.get_by_test_id("timeline").wait_for(timeout=15000)
        assert pg.locator("[data-item-id][data-review=dismissed]").evaluate_all("els => new Set(els.map(e => e.getAttribute('data-item-id'))).size") == 2
        assert pg.locator(f'[data-item-id="{first}"]').first.get_attribute("data-review") == "dismissed" and pg.locator(f'[data-item-id="{gone_id}"]').first.get_attribute("data-review") == "dismissed"
        assert _pending(pg) == 0
    finally:
        b.close()


def test_the_keyboard_journey_used_no_pointer_click(pw, made):
    """The proof behind the test above: the pointer-click counter sees a real mouse click and stays at 0 for the keyboard path (Enter and Space on buttons are clicks with detail 0)."""
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": 1280, "height": 900}); ctx.add_init_script(COUNT_POINTER_CLICKS); pg = ctx.new_page()
    try:
        pg.goto(C.BASE); pg.get_by_test_id("input-text").wait_for(timeout=15000)
        _tab_until(pg, "btn-sample"); pg.keyboard.press("Enter")
        expect(pg.get_by_test_id("record-count")).to_be_visible(timeout=15000)
        assert pg.evaluate("window.__ptr") == 0
        pg.get_by_test_id("btn-analyze").click()          # a deliberate mouse click is counted
        assert pg.evaluate("window.__ptr") == 1
        pg.get_by_test_id("timeline").wait_for(timeout=60000); made.append(_token(pg))
    finally:
        b.close()


def test_whole_journey_on_a_375_px_phone(pw, made):
    """Home -> paste -> Analyze -> dismiss one entry, accept the rest -> Export -> Copy -> reload at 375 x 812: no sideways scroll on any screen, the main controls are >= 44 px tall,
    the letter holds exactly the accepted entries, the decisions survive the reload (R-ST-1, mobile bar of test_multicase)."""
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": 375, "height": 812}, has_touch=True, is_mobile=True, permissions=["clipboard-read", "clipboard-write"]); pg = ctx.new_page()
    try:
        pg.goto(C.BASE); pg.get_by_test_id("input-text").wait_for(timeout=15000); _no_sideways_scroll(pg, "home")
        pg.get_by_test_id("input-text").fill(golden_text("sample.txt"))
        h = pg.get_by_test_id("btn-analyze").bounding_box()["height"]; assert h >= 44, f"Analyze is {h}px tall"
        pg.get_by_test_id("btn-analyze").tap()
        pg.get_by_test_id("timeline").wait_for(timeout=60000); tok = _token(pg); made.append(tok); _no_sideways_scroll(pg, "timeline")
        c0 = api("GET", f"/api/cases/{tok}")[1]
        first = c0["entries"][0]
        row = pg.get_by_test_id("entry-1")
        assert row.get_by_test_id("btn-dismiss").bounding_box()["height"] >= 44 and row.get_by_test_id("btn-accept").bounding_box()["height"] >= 44
        row.get_by_test_id("btn-dismiss").scroll_into_view_if_needed(); row.get_by_test_id("btn-dismiss").tap()
        expect(row).to_have_attribute("data-review", "dismissed")
        for _ in range(60):
            btn = pg.locator('[data-item-id][data-review=pending]').first.get_by_test_id("btn-accept") if _pending(pg) else None
            if btn is None:
                break
            btn.scroll_into_view_if_needed(); btn.tap(); pg.wait_for_timeout(150)
        assert _pending(pg) == 0; _no_sideways_scroll(pg, "timeline after review")
        ex = pg.get_by_test_id("btn-export"); assert ex.bounding_box()["height"] >= 44
        ex.scroll_into_view_if_needed(); ex.tap()
        expect(pg.get_by_test_id("export-letter")).to_be_visible(timeout=15000); _no_sideways_scroll(pg, "export")
        letter = pg.get_by_test_id("export-letter").inner_text()
        c, acc = _accepted_summaries(tok)
        assert len(acc) == 8 and _dated(letter) == 8 and all(e["summary"] in letter for e in acc) and first["summary"] not in letter
        cp = pg.get_by_test_id("btn-copy-letter"); assert cp.bounding_box()["height"] >= 44
        cp.scroll_into_view_if_needed(); cp.tap()
        expect(pg.locator("#export-status")).to_contain_text("Copied the treatment section")
        pg.reload(); pg.get_by_test_id("timeline").wait_for(timeout=15000); _no_sideways_scroll(pg, "timeline after reload")
        assert pg.get_by_test_id("entry-1").get_attribute("data-review") == "dismissed" and _pending(pg) == 0
    finally:
        b.close()
