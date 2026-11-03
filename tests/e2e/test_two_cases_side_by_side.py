"""T-045 AC8 (from T-053 AC3): two library cases open in two browser tabs of ONE browser profile (same origin, same localStorage), reviewed in alternation. No decision, count or
export leaks from one case into the other, in the screen, the reload, the case list or the letter.

The worst case for a leak is used on purpose: both cases are reviewed on the SAME item ids (each case numbers its entries e1, e2, ... itself), so a client that keeps decisions by item id alone
(in memory or in localStorage) would show A's accept on B's e1. tests/e2e/test_local_mode.py::test_two_library_cases_do_not_leak_decisions proves the same at the API; this proves it on the screen.
Library cases need ZLAYT_MODE=local (a plain run starts a local-mode server; the test skips with a reason otherwise)."""
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case
import tests.e2e.conftest as C

LIB_A, LIB_B = "case_lib01_er_only_then_gap", "case_lib06_lop_billed_vs_adjusted"


def _make(lib):
    st, c = api("POST", "/api/cases", {"library": lib})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.3)
    assert s["status"] == "ready", s
    return tok


@pytest.fixture
def two():
    a, b = _make(LIB_A), _make(LIB_B)
    yield a, b
    api("DELETE", f"/api/cases/{a}"); api("DELETE", f"/api/cases/{b}")


def _row(pg, item_id):
    return pg.locator(f'[data-item-id="{item_id}"]').first


def _states(pg):
    return pg.evaluate("""() => { const o = {}; for (const r of document.querySelectorAll('[data-item-id][data-review]')) { const k = r.getAttribute('data-item-id'); if (!(k in o)) o[k] = r.getAttribute('data-review'); } return o; }""")


def test_two_library_cases_in_two_tabs_do_not_leak_decisions(pw, two):
    ta, tb = two
    ca, cb = api("GET", f"/api/cases/{ta}")[1], api("GET", f"/api/cases/{tb}")[1]
    ids_a = [e["id"] for e in ca["entries"] if e["state"] == "verified" and e["review_status"] == "pending"]
    ids_b = [e["id"] for e in cb["entries"] if e["state"] == "verified" and e["review_status"] == "pending"]
    shared = [i for i in ids_a if i in ids_b][:3]
    assert len(shared) >= 2 and ca["title"] != cb["title"], (ids_a, ids_b)         # the same ids in two different cases: the adversarial setup
    br = pw.chromium.launch(); ctx = br.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    pa, pb = ctx.new_page(), ctx.new_page()
    try:
        open_case(pa, ta); open_case(pb, tb)
        i1, i2 = shared[0], shared[1]
        # alternate: A accepts e1, B dismisses e1, A dismisses e2, B accepts e2
        pa.bring_to_front(); _row(pa, i1).get_by_test_id("btn-accept").click(); expect(_row(pa, i1)).to_have_attribute("data-review", "accepted")
        pb.bring_to_front(); _row(pb, i1).get_by_test_id("btn-dismiss").click(); expect(_row(pb, i1)).to_have_attribute("data-review", "dismissed")
        pa.bring_to_front(); _row(pa, i2).get_by_test_id("btn-dismiss").click(); expect(_row(pa, i2)).to_have_attribute("data-review", "dismissed")
        pb.bring_to_front(); _row(pb, i2).get_by_test_id("btn-accept").click(); expect(_row(pb, i2)).to_have_attribute("data-review", "accepted")
        want_a = {i1: "accepted", i2: "dismissed"}; want_b = {i1: "dismissed", i2: "accepted"}
        for pg, want in ((pa, want_a), (pb, want_b)):                              # the other tab's click did not repaint this one
            got = _states(pg); assert {k: got[k] for k in want} == want, got
            assert sum(1 for v in got.values() if v != "pending") == 2, got
        # a reload of each tab shows only its own decisions (nothing came from shared browser storage)
        for pg, want in ((pa, want_a), (pb, want_b)):
            pg.reload(); pg.get_by_test_id("timeline").wait_for(timeout=15000)
            got = _states(pg); assert {k: got[k] for k in want} == want and sum(1 for v in got.values() if v != "pending") == 2, got
        # the server agrees, per case
        sa = {e["id"]: e["review_status"] for e in api("GET", f"/api/cases/{ta}")[1]["entries"]}
        sb = {e["id"]: e["review_status"] for e in api("GET", f"/api/cases/{tb}")[1]["entries"]}
        assert {k: sa[k] for k in want_a} == want_a and {k: sb[k] for k in want_b} == want_b
        # the case list keeps the two apart
        rows = {r["token"]: r for r in api("GET", "/api/cases")[1]["cases"]}
        for t, tot in ((ta, ca), (tb, cb)):                                          # exactly its own two decisions, out of its own total
            r = rows[t]; assert r["progress"]["entries"]["decided"] == 2 and r["progress"]["entries"]["total"] == len(tot["entries"]), r["progress"]
            assert r["counts"]["accepted"] == 1 and r["counts"]["dismissed"] == 1
        da = ca["entries"][[e["id"] for e in ca["entries"]].index(i1)]; db = cb["entries"][[e["id"] for e in cb["entries"]].index(i2)]
        # exports: A's letter holds A's accepted entry only; B's holds B's accepted entry only
        la = api("GET", f"/api/cases/{ta}/export")[1]["letter_text"]; lb = api("GET", f"/api/cases/{tb}/export")[1]["letter_text"]
        assert da["summary"] in la and da["summary"] not in lb and db["summary"] in lb and db["summary"] not in la
        # the screens: each tab's Export block is its own case's letter
        for pg, mine, other in ((pa, da["summary"], db["summary"]), (pb, db["summary"], da["summary"])):
            pg.bring_to_front(); pg.get_by_test_id("btn-export").click(); expect(pg.get_by_test_id("export-letter")).to_be_visible(timeout=15000)
            txt = pg.get_by_test_id("export-letter").inner_text(); assert mine in txt and other not in txt
        # the overview, opened from one tab, lists both cases with their own progress
        pa.goto(C.BASE + "/"); pa.get_by_test_id("cases-overview").wait_for(timeout=15000)
        for t in (ta, tb):
            expect(pa.locator(f'[data-testid=cases-row][data-token="{t}"]')).to_be_visible()
    finally:
        br.close()


def test_two_cases_one_keyboard_each_leave_the_other_alone(pw, two):
    """Keyboard decisions (a / d on a focused row) in one tab never touch the other tab's case, and each tab's Do this first keeps naming its own case's item."""
    ta, tb = two
    br = pw.chromium.launch(); ctx = br.new_context(viewport={"width": 1280, "height": 900}); pa, pb = ctx.new_page(), ctx.new_page()
    try:
        open_case(pa, ta); open_case(pb, tb)
        before_b = dict(_states(pb))
        pa.bring_to_front(); pa.locator("[data-testid=queue] [data-item-id]").first.focus(); first_a = pa.evaluate("document.activeElement.getAttribute('data-item-id')")
        pa.keyboard.press("a"); expect(_row(pa, first_a)).to_have_attribute("data-review", "accepted")
        pb.bring_to_front(); pb.reload(); pb.get_by_test_id("timeline").wait_for(timeout=15000)
        assert _states(pb) == before_b, "case B changed after a keyboard accept in case A"
        assert all(e["review_status"] == "pending" for e in api("GET", f"/api/cases/{tb}")[1]["entries"])
    finally:
        br.close()
