"""T-149 (frontend; backend T-148): multi-case management. The home screen is a case Overview (GET /api/cases); a case opens into a Detail view that starts with a case overview block.

Real backend (fixture LLM set, ZLAYT_MODE=local; a plain `pytest tests/e2e` starts its own server). Written before the UI.
The numbers on screen are the server's: every assertion compares the screen with GET /api/cases, GET /api/cases/{token} or GET /api/cases/{token}/trace.
Hooks are listed in tests/e2e/conftest.py (T-149 paragraph)."""
import os
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, JudgeNotRun
import tests.e2e.conftest as C

LIB = {"a": "case_lib01_er_only_then_gap", "b": "case_lib06_lop_billed_vs_adjusted", "c": "case_lib02_slip_fall_prior_knee", "d": "case_lib03_truck_rear_end_chiro"}
TITLE = {"a": "ER visit, then a treatment gap", "b": "Letter of protection, billed vs. adjusted", "c": "Slip and fall, prior knee surgery", "d": "Truck rear-end, chiropractic plan"}
KINDS = ("entries", "flags", "amounts")
ROWS = '[data-testid="cases-row"]'
CODE = re.compile(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b")


def _base():
    return C.BASE            # pytest_configure may have replaced it after import


def _make(lib, run=True):
    st, c = api("POST", "/api/cases", {"library": LIB[lib]}); assert st in (200, 201), (st, c)
    tok = c["token"]
    if run:
        assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
        for _ in range(300):
            s = api("GET", f"/api/cases/{tok}/status")[1]
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(0.5)
        assert s["status"] == "ready", s
    return tok


@pytest.fixture(scope="module")
def cs():
    """a: untouched (export blocked: nothing accepted). b: one entry accepted (export ready, with warnings). c: ingested only (never analyzed). d: untouched, for the spec that decides an item."""
    if not C._up():
        pytest.skip("app server not running")
    t = {"a": _make("a"), "b": _make("b"), "c": _make("c", run=False), "d": _make("d"), "e": _make("b")}
    e1 = next(e for e in api("GET", f"/api/cases/{t['b']}")[1]["entries"] if e["date"] and e["state"] == "verified")
    assert api("POST", f"/api/cases/{t['b']}/items/{e1['id']}/review", {"action": "accept"})[0] == 200
    _decide_everything(t["e"])
    yield t
    for tok in t.values():
        api("DELETE", f"/api/cases/{tok}")


def _decide_everything(tok):
    """e: one entry accepted, every other item dismissed: nothing pending, no edit to check (the server's needs_review count is state-based and stays above zero)."""
    c = api("GET", f"/api/cases/{tok}")[1]
    keep = next(e for e in c["entries"] if e["date"] and e["state"] == "verified")
    assert api("POST", f"/api/cases/{tok}/items/{keep['id']}/review", {"action": "accept"})[0] == 200
    for i in c["entries"] + c["undated_entries"] + c["flags"] + c["amounts"]:
        if i["id"] != keep["id"] and i.get("review_status") == "pending" and i.get("state") != "rejected":
            assert api("POST", f"/api/cases/{tok}/items/{i['id']}/review", {"action": "dismiss"})[0] == 200, i["id"]
    h = _list()[tok]["hitl"]
    assert h["pending"] == 0 and h["edits_to_check"] == 0, h


def _list():
    st, b = api("GET", "/api/cases"); assert st == 200, (st, b)
    return {x["token"]: x for x in b["cases"]}


def _home(page, cs):
    page.goto(_base() + "/")
    page.get_by_test_id("cases-overview").wait_for(timeout=15000)
    expect(page.locator(f'{ROWS}[data-token="{cs["a"]}"]')).to_be_visible()
    page.locator('[data-testid=cases-list][data-ready="true"]').wait_for(state="attached")      # keys are bound before the rows paint; this marks the first settled paint


def _row(page, tok):
    return page.locator(f'{ROWS}[data-token="{tok}"]')


def _tokens(page):
    return page.locator(ROWS).evaluate_all("els => els.map(e => e.getAttribute('data-token'))")


def _nums(text):
    m = re.match(r"\s*(\d+) of (\d+)", text); assert m, text
    return int(m.group(1)), int(m.group(2))


def _stub_list(page, fn):
    """Answer GET /api/cases with fn(real_json) (or a dict). Other methods and other paths pass through."""
    def h(route):
        if route.request.method != "GET":
            return route.continue_()
        out = fn(route.fetch().json()) if callable(fn) else fn
        return route.fulfill(**out) if "status" in out else route.fulfill(json=out)
    page.route(re.compile(r"/api/cases$"), h)


# ---- the overview ------------------------------------------------------------------------------------------------------------------------------
def test_home_is_the_overview_with_one_row_per_case_and_the_paste_box_below(page, cs):
    _home(page, cs)
    assert set(_tokens(page)) == set(_list()), "every case the server lists has a row, and no other"
    assert page.get_by_test_id("input-text").is_visible()                      # adding records is still one step away
    ov, box = page.get_by_test_id("cases-overview").bounding_box(), page.get_by_test_id("input-text").bounding_box()
    assert ov["y"] < box["y"], "the case list comes first"


def test_row_shows_readable_title_dates_stage_progress_and_chips_from_the_api(page, cs):
    _home(page, cs)
    L = _list()
    for key in ("a", "b"):
        s, row = L[cs[key]], _row(page, cs[key])
        expect(row.get_by_test_id("cases-title")).to_have_text(TITLE[key])
        t = row.get_by_test_id("cases-dates").locator("time").first
        assert re.match(r"\d{4}-\d{2}-\d{2}T", t.get_attribute("datetime")) and re.search(r"\b20\d\d\b", t.inner_text()), t.inner_text()
        expect(row.get_by_test_id("cases-stage")).to_contain_text("Analysis done")
        for k in KINDS:
            bar = row.get_by_test_id(f"cases-progress-{k}")
            assert int(float(bar.get_attribute("value"))) == s["progress"][k]["decided"] and int(float(bar.get_attribute("max"))) == max(s["progress"][k]["total"], 1)
            assert _nums(row.get_by_test_id(f"cases-progress-text-{k}").inner_text()) == (s["progress"][k]["decided"], s["progress"][k]["total"])
        h = s["hitl"]
        expect(row.get_by_test_id("cases-chip-needs-review")).to_have_text(re.compile(rf"^{h['needs_review']} need"))
        if h["could_not_verify"]:
            expect(row.get_by_test_id("cases-chip-tray")).to_have_text(f"{h['could_not_verify']} could not be verified")
    a, b = L[cs["a"]], L[cs["b"]]
    assert not a["export_ready"] and a["hitl"]["gate_blockers"] and b["export_ready"]
    ra = _row(page, cs["a"])
    expect(ra.get_by_test_id("cases-chip-blocked")).to_be_visible()
    expect(ra.get_by_test_id("cases-chip-ready")).to_have_count(0)
    expect(ra.get_by_test_id("cases-blocker-reason").first).to_have_text(a["hitl"]["gate_blockers"][0]["why"])     # the server's own plain sentence, not a code
    assert not CODE.search(ra.inner_text()), "no raw reason code on screen"
    rb = _row(page, cs["b"])
    expect(rb.get_by_test_id("cases-chip-can-export")).to_be_visible()          # T-149 r2: export passes but items are undecided: amber, never green
    expect(rb.get_by_test_id("cases-chip-ready")).to_have_count(0)
    expect(rb.get_by_test_id("cases-chip-blocked")).to_have_count(0)


def test_ingested_case_row_says_it_was_not_analyzed_and_opens_with_its_analyze_button(page, cs):
    _home(page, cs)
    row = _row(page, cs["c"])
    expect(row.get_by_test_id("cases-stage")).to_have_text("Not analyzed yet")
    row.get_by_test_id("cases-open").click()
    expect(page.get_by_test_id("btn-analyze")).to_be_visible()


def test_filters_split_cases_that_need_attention_from_cases_that_are_ready_to_send(page, cs):
    _home(page, cs)
    L = _list()
    ready = {t for t, s in L.items() if s["export_ready"] and s["status"] == "ready" and s["hitl"]["pending"] == 0 and s["hitl"]["edits_to_check"] == 0}
    assert cs["e"] in ready and cs["b"] not in ready and cs["a"] not in ready, "ready means export passes AND nothing is undecided"
    expect(page.get_by_test_id("cases-filter-all")).to_have_attribute("aria-pressed", "true")
    page.get_by_test_id("cases-filter-ready").click()
    assert set(_tokens(page)) == ready
    expect(page.get_by_test_id("cases-filter-ready")).to_have_attribute("aria-pressed", "true")
    expect(page.get_by_test_id("cases-filter-ready")).to_contain_text(f"({len(ready)})")
    expect(page.get_by_test_id("cases-count")).to_contain_text(f"Showing {len(ready)} of {len(L)}")
    page.get_by_test_id("cases-filter-attention").click()
    got = set(_tokens(page))
    assert cs["a"] in got and cs["d"] in got and cs["b"] in got
    assert not (got & ready), "Needs attention and Ready to send never overlap"
    assert cs["e"] not in got, "a finished case is not in Needs attention"
    page.get_by_test_id("cases-filter-all").click()
    assert set(_tokens(page)) == set(L)


def test_a_finished_case_shows_everything_decided_and_no_stale_needs_review_call_out(page, cs):
    _home(page, cs)
    row = _row(page, cs["e"])
    expect(row.get_by_test_id("cases-chip-needs-review")).to_have_count(0)
    expect(row.get_by_test_id("cases-chip-ready")).to_have_text("Everything decided")
    expect(row.get_by_test_id("cases-chip-can-export")).to_have_count(0)
    assert _nums(row.get_by_test_id("cases-decided").inner_text())[0] == _nums(row.get_by_test_id("cases-decided").inner_text())[1]


def test_can_export_is_amber_and_says_what_stays_out_of_the_letter(page, cs):
    _home(page, cs)
    h = _list()[cs["b"]]["hitl"]
    n = sum(w.get("count", 0) for w in h["gate_warnings"] if w["reason_code"] == "ITEMS_NOT_REVIEWED") or h["pending"]
    chip = _row(page, cs["b"]).get_by_test_id("cases-chip-can-export")
    expect(chip).to_have_text(f"Can export \u2014 {n} not reviewed (they stay out of the letter)")
    assert "chip--warn" in chip.get_attribute("class") and "chip--ok" not in chip.get_attribute("class")


def test_a_filter_with_no_match_says_so_and_all_cases_brings_them_back(page, cs):
    def none_ready(body):
        for c in body["cases"]:
            c["export_ready"] = False
        return body
    _stub_list(page, none_ready)
    _home(page, cs)
    page.get_by_test_id("cases-filter-ready").click()
    expect(page.get_by_test_id("cases-empty")).to_contain_text("No case has everything decided yet")
    page.get_by_test_id("cases-filter-all").click()
    expect(page.get_by_test_id("cases-empty")).to_be_hidden()
    assert len(_tokens(page)) >= 4


def test_sort_by_title_by_needs_attention_first_and_by_least_decided(page, cs):
    _home(page, cs)
    L = _list()
    page.get_by_test_id("cases-sort").select_option("title")
    titles = page.locator(f'{ROWS} [data-testid="cases-title"]').all_inner_texts()
    assert titles == sorted(titles, key=str.casefold), titles
    page.get_by_test_id("cases-sort").select_option("attention")
    order = _tokens(page)
    assert order.index(cs["a"]) < order.index(cs["b"]), "an export-blocked case comes before one that is ready"
    page.get_by_test_id("cases-sort").select_option("least_done")
    shares = [(L[t]["progress"]["entries"]["decided"] + L[t]["progress"]["flags"]["decided"] + L[t]["progress"]["amounts"]["decided"]) /
              max(1, sum(L[t]["progress"][k]["total"] for k in KINDS)) for t in _tokens(page)]
    assert shares == sorted(shares), shares


def test_call_outs_for_running_failed_edits_tray_and_blockers_come_from_the_list_response(page, cs):
    def mk(tok, ttl, **kw):
        s = {"token": tok, "title": ttl, "name": ttl, "source": "paste", "status": "ready", "record_count": 5, "created_at": "2026-11-01T15:04:00Z", "updated_at": "2026-11-01T15:09:00Z",
             "last_activity_at": "2026-11-02T09:30:00Z", "run": {"stage": "finalize", "steps_done": 7, "steps_total": 8, "running": False, "error": False},
             "progress": {"entries": {"decided": 3, "total": 5}, "flags": {"decided": 0, "total": 0}, "amounts": {"decided": 1, "total": 2}},
             "counts": {"pending": 2, "accepted": 3, "edited": 0, "dismissed": 0, "needs_review": 0},
             "hitl": {"pending": 1, "needs_review": 0, "edits_to_check": 0, "could_not_verify": 0, "gate_blockers": [], "gate_warnings": []}, "export_ready": True}
        s.update(kw)
        return s
    jn = [{"reason_code": "JUDGE_NOT_RUN", "kind": "entry", "item_id": f"e{i}", "why": f"Entry {i} was accepted but the second AI check did not run on it."} for i in (1, 2, 3)]
    stub = [mk("tkrun", "Running case", status="running", export_ready=False, run={"stage": "extract", "steps_done": 1, "steps_total": 8, "running": True, "error": False},
               hitl={"pending": 0, "needs_review": 0, "edits_to_check": 0, "could_not_verify": 0, "gate_blockers": [{"reason_code": "RUN_IN_PROGRESS", "kind": "case", "item_id": None, "why": "The AI run is still going."}], "gate_warnings": []}),
            mk("tkfail", "Failed case", status="failed", export_ready=False, run={"stage": "judge_entries", "steps_done": 3, "steps_total": 8, "running": False, "error": True}),
            mk("tkedit", "Edits and tray", hitl={"pending": 5, "needs_review": 4, "needs_review_open": 4, "edits_to_check": 2, "could_not_verify": 3, "gate_blockers": [], "gate_warnings": [{"reason_code": "EDIT_NOT_CONFIRMED", "count": 2, "why": "2 edits are not compared with the quote yet."}]}),
            mk("tkblock", "Blocked three ways", export_ready=False, hitl={"pending": 0, "needs_review": 0, "edits_to_check": 0, "could_not_verify": 0, "gate_blockers": jn, "gate_warnings": []}),
            mk("tkold", "smith_records-2024.pdf", title="Smith records 2024", name="smith_records-2024.pdf")]
    _stub_list(page, {"cases": stub})
    page.goto(_base() + "/"); page.get_by_test_id("cases-overview").wait_for()
    assert set(_tokens(page)) == {s["token"] for s in stub}
    run = _row(page, "tkrun")
    expect(run.get_by_test_id("cases-stage")).to_contain_text("Analyzing")
    expect(run.get_by_test_id("cases-stage")).to_contain_text("step 2 of 8")
    expect(_row(page, "tkfail").get_by_test_id("cases-stage")).to_contain_text("Analysis failed")
    fl = _row(page, "tkfail")
    expect(fl.get_by_test_id("cases-next")).to_contain_text("run it again")        # a failed row says what to do
    for t in ("cases-chip-needs-review", "cases-chip-edits", "cases-chip-can-export", "cases-chip-ready"):
        expect(fl.get_by_test_id(t)).to_have_count(0)
        expect(run.get_by_test_id(t)).to_have_count(0)                             # nor does a case that is still running
    ed = _row(page, "tkedit")
    expect(ed.get_by_test_id("cases-chip-needs-review")).to_have_text("4 need review")
    expect(ed.get_by_test_id("cases-chip-edits")).to_have_text("2 edits to check")
    expect(ed.get_by_test_id("cases-chip-tray")).to_have_text("3 could not be verified")
    expect(ed.get_by_test_id("cases-chip-can-export")).to_be_visible()
    expect(ed.get_by_test_id("cases-chip-ready")).to_have_count(0)
    assert "chip--warn" not in ed.get_by_test_id("cases-chip-tray").get_attribute("class"), "could not be verified is a quiet note, not an amber call-out"
    expect(ed).to_contain_text("2 edits are not compared with the quote yet.")        # a warning on a ready case is said in the server's words
    bl = _row(page, "tkblock")
    expect(bl.get_by_test_id("cases-chip-blocked")).to_have_text("Export blocked (3)")
    expect(bl.get_by_test_id("cases-blocker-reason")).to_have_count(2)                  # two reasons, then "and 1 more"
    expect(bl).to_contain_text("and 1 more")
    expect(bl.get_by_test_id("cases-blocker-reason").first).to_have_text(jn[0]["why"])
    old = _row(page, "tkold")
    expect(old.get_by_test_id("cases-title")).to_have_text("Smith records 2024")
    expect(old.get_by_test_id("cases-chip-needs-review")).to_have_count(0)               # nothing to say, nothing shown (no "0 need review")


def test_needs_review_chip_counts_only_open_items_even_before_the_server_sends_the_open_count(page, cs):
    """T-157 adds hitl.needs_review_open. Until then: nothing pending -> no needs-review call-out (the state-based count would stay above zero forever)."""
    def strip_field(body):
        for c in body["cases"]:
            c["hitl"].pop("needs_review_open", None)
            if c["token"] == cs["e"]:
                c["hitl"]["needs_review"] = 9
            if c["token"] == cs["a"]:
                c["hitl"]["pending"], c["hitl"]["needs_review"] = 3, 9
        return body
    _stub_list(page, strip_field)
    _home(page, cs)
    expect(_row(page, cs["e"]).get_by_test_id("cases-chip-needs-review")).to_have_count(0)
    expect(_row(page, cs["a"]).get_by_test_id("cases-chip-needs-review")).to_have_text("3 need review")      # never more than what is pending


def test_not_analyzed_row_has_one_call_out_to_press_analyze_and_no_review_or_blocker_chips(page, cs):
    _home(page, cs)
    row = _row(page, cs["c"])
    expect(row.get_by_test_id("cases-next")).to_contain_text("Analyze")
    for t in ("cases-chip-needs-review", "cases-chip-blocked", "cases-chip-edits", "cases-chip-can-export", "cases-chip-ready"):
        expect(row.get_by_test_id(t)).to_have_count(0)
    for k in KINDS:
        expect(row.get_by_test_id(f"cases-progress-text-{k}")).to_have_text("Not started")


def test_each_row_has_one_status_pill_and_one_overall_decided_count_and_last_activity_only(page, cs):
    _home(page, cs)
    L = _list()
    for key in ("a", "b", "e"):
        row, s = _row(page, cs[key]), L[cs[key]]
        expect(row.get_by_test_id("cases-stage")).to_have_count(1)
        d = sum(s["progress"][k]["decided"] for k in KINDS); t = sum(s["progress"][k]["total"] for k in KINDS)
        assert _nums(row.get_by_test_id("cases-decided").inner_text()) == (d, t)
        txt = row.get_by_test_id("cases-dates").inner_text()
        assert "Last activity" in txt and "Created" not in txt, txt
        assert "Created" in (row.get_by_test_id("cases-dates").get_attribute("title") or ""), "the created date is on hover"


def test_title_search_narrows_the_list_and_j_k_do_not_fire_while_typing(page, cs):
    _home(page, cs)
    box = page.get_by_test_id("cases-search")
    box.fill("slip and fall")
    assert _tokens(page) == [] or all("slip" in _row(page, t).get_by_test_id("cases-title").inner_text().lower() for t in _tokens(page))
    box.fill("letter of protection")
    assert cs["b"] in _tokens(page) and cs["a"] not in _tokens(page)
    box.fill("zzzz nothing")
    expect(page.get_by_test_id("cases-empty")).to_contain_text("No case matches")
    box.fill("j"); box.press("k")
    expect(box).to_have_value("jk")
    box.fill("")
    assert set(_tokens(page)) == set(_list())


def test_overview_is_absent_when_the_server_has_no_case_list(page):
    _stub_list(page, {"status": 404, "json": {"error": {"code": "not_found", "message": "Not found"}}})
    page.goto(_base() + "/"); page.get_by_test_id("input-text").wait_for()
    expect(page.get_by_test_id("cases-overview")).to_be_hidden()
    expect(page.get_by_test_id("btn-all-cases")).to_be_hidden()


# ---- loading and failing -----------------------------------------------------------------------------------------------------------------------
def test_overview_says_loading_until_the_list_answers(page, cs):
    held = []
    page.route(re.compile(r"/api/cases$"), lambda route: held.append(route) if route.request.method == "GET" else route.continue_())
    page.goto(_base() + "/")
    expect(page.get_by_test_id("cases-loading")).to_have_text(re.compile("Loading cases"))
    expect(page.get_by_test_id("cases-overview")).to_be_visible()
    assert not page.locator(ROWS).count()
    for r in held:
        r.continue_()
    expect(page.locator(ROWS).first).to_be_visible()
    expect(page.get_by_test_id("cases-loading")).to_be_hidden()


def test_a_failed_list_load_shows_a_sentence_and_a_retry_button_in_the_same_place(page, cs):
    state = {"fail": True}
    def h(route):
        if route.request.method == "GET" and state["fail"]:
            return route.fulfill(status=500, json={"error": {"code": "internal", "message": "The server stumbled."}})
        route.continue_()
    page.route(re.compile(r"/api/cases$"), h)
    page.goto(_base() + "/")
    err = page.get_by_test_id("cases-load-error")
    expect(err).to_be_visible()
    expect(err).to_contain_text("We could not load your cases")
    assert "server answered" not in err.inner_text() and "Request failed" not in err.inner_text()
    expect(page.get_by_test_id("cases-filter-all")).to_be_hidden()          # nothing to filter while the list failed
    expect(page.get_by_test_id("cases-search")).to_be_hidden()
    assert not page.locator(ROWS).count()
    state["fail"] = False
    page.get_by_test_id("cases-retry").click()
    expect(page.locator(ROWS).first).to_be_visible()
    expect(err).to_be_hidden()
    expect(page.get_by_role("heading", name="Cases", exact=True)).to_be_focused()     # the pressed button is gone: focus goes to the list heading
    expect(page.get_by_test_id("cases-filter-all")).to_be_visible()


def test_a_case_that_cannot_be_opened_says_so_and_keeps_saying_it(page, cs):
    _home(page, cs)
    page.route(re.compile(rf"/api/cases/{cs['a']}$"), lambda route: route.fulfill(status=500, json={"error": {"code": "internal", "message": "boom"}}) if route.request.method == "GET" else route.continue_())
    _row(page, cs["a"]).get_by_test_id("cases-open").click()
    msg = page.get_by_test_id("cases-open-error")
    expect(msg).to_be_visible()
    expect(msg).to_contain_text("could not be opened")
    page.wait_for_timeout(700)                                   # the list reloads in the background; the message must survive that
    expect(msg).to_be_visible()
    expect(page.get_by_test_id("cases-overview")).to_be_visible()


# ---- opening a case ----------------------------------------------------------------------------------------------------------------------------
def test_clicking_anywhere_on_the_row_opens_the_case(page, cs):
    _home(page, cs)
    _row(page, cs["a"]).get_by_test_id("cases-dates").click()
    page.get_by_test_id("case-overview").wait_for()
    assert page.url.endswith("#/case/" + cs["a"]), page.url
    expect(page.get_by_test_id("case-name")).to_have_text(TITLE["a"])
    expect(page.get_by_test_id("cases-overview")).to_be_hidden()


def test_back_button_returns_to_the_overview_and_forward_reopens_the_case(page, cs):
    _home(page, cs)
    _row(page, cs["a"]).get_by_test_id("cases-open").click()
    page.get_by_test_id("case-overview").wait_for()
    page.go_back()
    page.get_by_test_id("cases-overview").wait_for()
    expect(page.get_by_test_id("case-overview")).to_have_count(0)
    page.go_forward()
    page.get_by_test_id("case-overview").wait_for()
    expect(page.get_by_test_id("case-name")).to_have_text(TITLE["a"])


def test_j_and_k_move_between_rows_like_the_arrow_keys(page, cs):
    _home(page, cs)
    tok_at = "document.activeElement.closest('[data-testid=cases-row]') && document.activeElement.closest('[data-testid=cases-row]').getAttribute('data-token')"
    first = _tokens(page)[0]
    _row(page, first).get_by_test_id("cases-open").focus()
    page.keyboard.press("j")
    assert page.evaluate(tok_at) == _tokens(page)[1]
    page.keyboard.press("k")
    assert page.evaluate(tok_at) == first
    page.keyboard.press("k")
    assert page.evaluate(tok_at) == first, "k on the first row stays there"
    page.evaluate("document.activeElement.blur()")
    page.keyboard.press("j")                                       # no row focused: j starts at the first row
    assert page.evaluate(tok_at) == first


def test_keyboard_only_open_move_between_rows_and_return_with_focus_on_the_case(page, cs):
    _home(page, cs)
    tok_at = "document.activeElement.closest('[data-testid=cases-row]') && document.activeElement.closest('[data-testid=cases-row]').getAttribute('data-token')"
    first, second = _tokens(page)[:2]
    _row(page, first).get_by_test_id("cases-open").focus()
    page.keyboard.press("ArrowDown")
    assert page.evaluate(tok_at) == second, "ArrowDown moves to the next row's link"
    page.keyboard.press("ArrowUp")
    assert page.evaluate(tok_at) == first
    page.keyboard.press("Enter")
    page.get_by_test_id("case-overview").wait_for()
    page.get_by_test_id("btn-all-cases").focus(); page.keyboard.press("Enter")
    page.get_by_test_id("cases-overview").wait_for()
    expect(_row(page, first).get_by_test_id("cases-open")).to_be_focused()


def test_filter_and_sort_keep_their_choice_after_opening_a_case_and_coming_back(page, cs):
    _home(page, cs)
    page.get_by_test_id("cases-sort").select_option("title")
    page.get_by_test_id("cases-filter-attention").click()
    _row(page, cs["a"]).get_by_test_id("cases-open").click()
    page.get_by_test_id("case-overview").wait_for()
    page.get_by_test_id("btn-all-cases").click()
    page.get_by_test_id("cases-overview").wait_for()
    expect(page.get_by_test_id("cases-sort")).to_have_value("title")
    expect(page.get_by_test_id("cases-filter-attention")).to_have_attribute("aria-pressed", "true")


# ---- the detail view -----------------------------------------------------------------------------------------------------------------------------
def test_detail_is_one_case_overview_block_that_holds_progress_decisions_and_the_case_checks_before_the_timeline(page, cs):
    open_case(page, cs["a"])
    ok = page.evaluate("""() => { const o = document.querySelector('[data-testid=case-overview]'), t = document.querySelector('[data-testid=timeline]');
        const inside = (sel) => { const e = document.querySelector(sel); return !e || o.contains(e); };
        const after = (sel) => { const e = document.querySelector(sel); return !e || !!(o.compareDocumentPosition(e) & Node.DOCUMENT_POSITION_FOLLOWING && !o.contains(e)); };
        return t.firstElementChild === o && inside('[data-testid=todo-strip]') && inside('[data-testid=case-stepper]') && after('[data-testid=queue]') && after('[data-testid=flags-panel]') && after('[data-testid=charges-panel]'); }""")
    assert ok, "one block first: progress, what to do, the case checks; the breakdown comes after it"
    expect(page.get_by_test_id("case-overview").get_by_role("heading", name="Case overview")).to_be_visible()
    assert not page.locator("[data-testid=case-stepper] details.zs-case-det").evaluate("d => d.open"), "the case checks start collapsed"
    assert page.get_by_test_id("case-overview").get_by_test_id("co-gate-steps").count() == 0, "the export checks are not drawn twice"
    assert page.locator("[data-testid=todo-strip] [data-testid=need-review-count]").count() == 0 and page.locator('[data-testid=case-overview] [data-testid=need-review-count]').count() == 1, "one need-review count, not three"


def test_the_first_entry_is_above_the_fold_on_a_phone_with_the_overview_block_open(page, cs):
    page.set_viewport_size({"width": 390, "height": 844})
    open_case(page, cs["a"])
    page.evaluate("window.scrollTo(0, 0)")
    first = page.locator("[data-testid=queue] [data-item-id]").first
    first.wait_for()
    top = first.bounding_box()["y"]
    assert top <= 844 - 30, f"the first entry starts at {top}px on a 390x844 phone: its date line must be on the first screen"
    acc = page.locator("[data-testid=queue] [data-item-id]").first.get_by_test_id("btn-accept").first
    if acc.count():
        assert acc.bounding_box()["y"] <= 900, f"the first Accept is at {acc.bounding_box()['y']}px on a 390x844 phone"
    # the jump strip and the case checks sit under the entries, not above them
    assert page.get_by_test_id("case-stepper").bounding_box()["y"] > top if page.get_by_test_id("case-stepper").count() else True


def test_detail_overview_progress_chips_and_the_case_checks_match_the_server(page, cs):
    L = _list()
    for key in ("a", "b"):
        page.goto("about:blank")                   # a hash-only change would keep the previous case's timeline on screen
        open_case(page, cs[key])
        s, ov = L[cs[key]], page.get_by_test_id("case-overview")
        for k in KINDS:
            bar = ov.get_by_test_id(f"co-progress-{k}")
            assert (int(float(bar.get_attribute("value"))), int(float(bar.get_attribute("max")))) == (s["progress"][k]["decided"], max(s["progress"][k]["total"], 1)), k
            assert _nums(ov.get_by_test_id(f"co-progress-text-{k}").inner_text()) == (s["progress"][k]["decided"], s["progress"][k]["total"]), k
        h = s["hitl"]
        open_needs = min(h["needs_review"], h["pending"])
        expect(ov.get_by_test_id("need-review-count")).to_have_text(re.compile(rf"^{open_needs} need"))
        if h["could_not_verify"]:
            expect(ov.get_by_test_id("co-chip-tray")).to_have_text(f"{h['could_not_verify']} could not be verified")
        tr = api("GET", f"/api/cases/{cs[key]}/trace")[1]
        ov.get_by_test_id("case-summary").click()
        steps = ov.get_by_test_id("case-step")
        expect(steps).to_have_count(len(tr["steps"]))
        for i, st in enumerate(tr["steps"]):
            assert steps.nth(i).get_attribute("data-step-id") == st["id"] and steps.nth(i).get_attribute("data-status") == st["status"]
        if s["export_ready"]:
            expect(ov.get_by_test_id("co-chip-can-export")).to_have_text(re.compile(r"^Can export \u2014 \d+ not reviewed \(they stay out of the letter\)$"))
            expect(ov.get_by_test_id("co-chip-ready")).to_have_count(0)
        else:
            expect(ov.get_by_test_id("co-chip-blocked")).to_be_visible()
            expect(ov.get_by_test_id("co-blocker-reason").first).to_have_text(s["hitl"]["gate_blockers"][0]["why"])


def test_detail_overview_updates_after_a_decision_and_the_list_agrees_when_you_go_back(page, cs):
    open_case(page, cs["d"])
    ov = page.get_by_test_id("case-overview")
    before = _nums(ov.get_by_test_id("co-progress-text-entries").inner_text())
    page.locator('[data-testid=queue] [data-item-id][data-review=pending]').first.get_by_test_id("btn-accept").click()
    expect(ov.get_by_test_id("co-progress-text-entries")).to_have_text(re.compile(rf"^{before[0] + 1} of {before[1]}"), timeout=20000)
    page.get_by_test_id("btn-all-cases").click()
    page.get_by_test_id("cases-overview").wait_for()
    assert _list()[cs["d"]]["progress"]["entries"]["decided"] == before[0] + 1
    expect(_row(page, cs["d"]).get_by_test_id("cases-progress-text-entries")).to_have_text(re.compile(rf"^{before[0] + 1} of {before[1]}"))


def test_opening_a_case_moves_focus_to_its_heading_which_names_the_case(page, cs):
    _home(page, cs)
    _row(page, cs["a"]).get_by_test_id("cases-open").focus(); page.keyboard.press("Enter")
    page.get_by_test_id("case-overview").wait_for()
    h = page.get_by_test_id("case-heading")
    expect(h).to_be_focused()
    assert TITLE["a"] in (h.get_attribute("aria-label") or h.inner_text())


# ---- "Do this first" (T-157 next_action), naming a case, and the second-check offer -----------------------------------------------------------
def _with_next_action(page, tok, na):
    def f(body):
        for c in body["cases"]:
            if c["token"] == tok:
                c["next_action"] = na
        return body
    _stub_list(page, f)


def test_do_this_first_is_one_line_built_from_next_action_and_its_button_goes_to_that_item(page, cs):
    c = api("GET", f"/api/cases/{cs['a']}")[1]
    item = next(e for e in c["entries"] if e.get("review_status") == "pending")
    _with_next_action(page, cs["a"], {"item_id": item["id"], "kind": "entry", "reason": "Decide this entry: its quote does not match the record word for word."})
    open_case(page, cs["a"])
    line = page.get_by_test_id("case-overview").get_by_test_id("do-first")
    expect(line).to_have_count(1)
    expect(line).to_contain_text("Do this first")
    expect(line).to_contain_text("its quote does not match the record word for word")
    line.get_by_test_id("btn-do-first").click()
    expect(page.locator(f'[data-item-id="{item["id"]}"]').first).to_be_focused()
    for n in page.get_by_test_id("case-next-action").all():
        expect(n).to_be_hidden()                                  # the case checks do not give a second, different first step


def test_without_next_action_a_case_with_pending_items_still_has_one_do_this_first_line_and_a_decided_case_has_none(page, cs):
    _with_next_action(page, cs["a"], None)
    open_case(page, cs["a"])
    box = page.get_by_test_id("case-overview"); line = box.get_by_test_id("do-first")
    # T-174: a case with pending items always has ONE line that says what to do. It is "Do this first: Review the remaining ..." unless a case check already says it (the export gate asks for a first
    # decision on a case with nothing accepted), and then that check's own "What you need to do" line is the one.
    page.wait_for_timeout(1500)                                                                     # the case checks arrive after the case
    if line.count():
        expect(line).to_have_count(1); expect(line).to_contain_text("Review the remaining")
        line.get_by_test_id("btn-do-first").click()
        expect(page.locator("[data-testid=queue] [data-item-id]").first).to_be_visible()
    else:
        expect(page.get_by_test_id("case-next-action")).to_have_count(1)
    page.goto("about:blank")
    _with_next_action(page, cs["e"], None)
    open_case(page, cs["e"])
    expect(page.get_by_test_id("case-overview").get_by_test_id("do-first")).to_have_count(0)


def test_do_this_first_names_the_item_by_date_flag_or_amount_and_record_and_go_to_it_is_the_only_first_step(page, cs):
    page.goto("about:blank")
    open_case(page, cs["a"])
    c = api("GET", f"/api/cases/{cs['a']}")[1]
    na = c["next_action"]; assert na and na["item_id"], na
    recs = {r["id"]: r["seq"] for r in c["records"]}
    item = next(i for k in ("entries", "undated_entries", "flags", "amounts") for i in c[k] if i["id"] == na["item_id"])
    line = page.get_by_test_id("case-overview").get_by_test_id("do-first")
    expect(line).to_have_count(1)
    name = line.get_by_test_id("do-first-item").inner_text()
    assert name and re.search(r"record", name, re.I), name
    if item.get("record_ids"):
        assert str(recs[item["record_ids"][0]]) in name, (name, item["record_ids"])
    if item.get("date"):
        assert re.search(r"\b20\d\d\b", name), name
    line.get_by_test_id("btn-do-first").click()
    expect(page.locator(f'[data-item-id="{item["id"]}"]').first).to_be_focused()
    page.evaluate("document.activeElement.blur(); window.scrollTo(0, 0)")
    page.get_by_test_id("btn-start-review").click()                         # one first step: Start review lands on the same item
    expect(page.locator(f'[data-item-id="{item["id"]}"]').first).to_be_focused()


def test_new_case_button_is_in_the_first_screen_and_puts_the_cursor_in_the_name_field(page, cs):
    for vw in ({"width": 1440, "height": 900}, {"width": 390, "height": 844}):
        page.set_viewport_size(vw)
        page.goto("about:blank")
        _home(page, cs)
        btn = page.get_by_test_id("btn-new-case")
        expect(btn).to_be_visible()
        assert btn.bounding_box()["y"] + btn.bounding_box()["height"] <= vw["height"]
        btn.focus(); page.keyboard.press("Enter")
        expect(page.get_by_test_id("input-title")).to_be_focused()
        expect(page.get_by_role("heading", name="New case", exact=True)).to_be_in_viewport()


def test_the_overview_chip_equals_the_open_needs_review_count_the_server_sends_and_the_detail_agrees(page, cs):
    L = _list()[cs["d"]]["hitl"]
    assert "needs_review_open" in L, "the list must send needs_review_open (T-157)"
    page.goto("about:blank")
    _home(page, cs)
    row = _row(page, cs["d"])
    want = L["needs_review_open"]
    if want:
        expect(row.get_by_test_id("cases-chip-needs-review")).to_have_text(re.compile(rf"^{want} need"))
    else:
        expect(row.get_by_test_id("cases-chip-needs-review")).to_have_count(0)
    row.get_by_test_id("cases-open").click()
    ov = page.get_by_test_id("case-overview")
    if want:
        expect(ov.get_by_test_id("need-review-count")).to_have_text(re.compile(rf"^{want} need"))


def test_overview_names_the_j_and_k_keys_on_screen(page, cs):
    page.goto("about:blank")
    _home(page, cs)
    keys = page.get_by_test_id("cases-keys")
    expect(keys).to_be_visible()
    expect(keys).to_contain_text("j")
    expect(keys).to_contain_text("k")
    expect(keys).to_contain_text("Enter")


def test_no_green_ready_to_export_in_the_block_or_the_case_checks_while_items_are_undecided(page, cs):
    page.goto("about:blank")
    open_case(page, cs["b"])                        # one entry accepted: the gate passes with many items undecided
    ov = page.get_by_test_id("case-overview")
    expect(ov.get_by_test_id("co-chip-can-export")).to_be_visible()
    page.get_by_test_id("case-summary").click()
    verdict = ov.get_by_test_id("case-verdict")
    expect(verdict).to_be_visible()
    expect(verdict).to_contain_text("Can export")
    expect(verdict).to_contain_text("not reviewed")
    assert "zs-v-ready" not in (verdict.get_attribute("class") or "").split() and "zs-v-accepted" not in (verdict.get_attribute("class") or "").split()
    assert ov.locator(".zs-v-ready").count() == 0
    assert not re.search(r"Ready to export(?!\?)", ov.inner_text())     # "Ready to export?" is the name of the gate step
    assert "Can export" in ov.get_by_test_id("case-summary-gate").inner_text()
    page.goto("about:blank")
    open_case(page, cs["e"])                        # everything decided: the green words are right
    ov = page.get_by_test_id("case-overview")
    expect(ov.get_by_test_id("co-chip-ready")).to_be_visible()
    expect(ov.get_by_test_id("case-summary-gate")).to_contain_text("Ready to export")
    assert ov.get_by_test_id("case-summary-gate").inner_text().count("not reviewed") == 0
    for n in ov.get_by_test_id("case-next-action").all():
        expect(n).to_be_hidden()                    # nothing waits: no leftover "What you need to do"


def _accept_three(tok):
    c = api("GET", f"/api/cases/{tok}")[1]
    ids = [e["id"] for e in c["entries"] if e["state"] != "rejected" and e["date"]][:3]
    for i in ids:
        assert api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "accept"})[0] == 200
    return ids


def test_the_second_check_rerun_is_offered_only_when_an_item_says_rerun_available(page, sample_case):
    JudgeNotRun(page, sample_case, _accept_three(sample_case))             # plays a live backend: items say rerun_available true
    open_case(page, sample_case)
    page.get_by_test_id("btn-export").click()
    expect(page.get_by_test_id("export-blocked-msg")).to_be_visible()
    expect(page.get_by_test_id("export-blocked").get_by_test_id("btn-rerun-judge")).to_be_visible()
    expect(page.get_by_test_id("rerun-unavailable")).to_have_count(0)
    def none_available(route):                                              # the real fixture backend: nothing can answer
        if route.request.method != "GET":
            return route.continue_()
        d = route.fetch().json()
        for k in ("entries", "undated_entries", "flags", "amounts"):
            for i in d.get(k) or []:
                i["rerun_available"] = False
        route.fulfill(json=d)
    page.route(re.compile(rf"/api/cases/{sample_case}$"), none_available)   # registered later: wins over the stub's
    page.reload(); page.get_by_test_id("timeline").wait_for()
    page.get_by_test_id("btn-export").click()
    expect(page.get_by_test_id("export-blocked-msg")).to_be_visible()
    expect(page.get_by_test_id("btn-rerun-judge")).to_have_count(0)
    expect(page.get_by_test_id("export-blocked").get_by_test_id("rerun-unavailable")).to_be_visible()
    expect(page.get_by_test_id("rerun-unavailable").first).to_contain_text("cannot be run again here")


def test_a_name_typed_beside_analyze_is_sent_as_the_case_title(page):
    seen = []
    def h(route):
        if route.request.method == "POST":
            seen.append(route.request.post_data_json)
        route.continue_()
    page.route(re.compile(r"/api/cases$"), h)
    page.goto(_base() + "/"); page.get_by_test_id("input-text").wait_for()
    page.get_by_test_id("input-title").fill("Rivera, knee")
    page.get_by_test_id("btn-sample").click()
    page.get_by_test_id("case-name").wait_for()
    assert seen and seen[0].get("title") == "Rivera, knee", seen


def test_rename_in_the_detail_header_sends_a_patch_and_shows_the_new_name(page, cs):
    sent = []
    def h(route):
        if route.request.method == "PATCH":
            sent.append(route.request.post_data_json)
            return route.fulfill(json={"token": cs["a"], "title": sent[-1]["title"]})
        route.continue_()
    page.route(re.compile(rf"/api/cases/{cs['a']}$"), h)
    open_case(page, cs["a"])
    page.get_by_test_id("btn-rename-case").click()
    box = page.get_by_test_id("case-rename-input")
    expect(box).to_be_focused()
    box.fill("Smith, back"); box.press("Enter")
    expect(page.get_by_test_id("case-name")).to_have_text("Smith, back")
    assert sent == [{"title": "Smith, back"}]


def _paste(lib):
    """The fixture backend only reads the recorded texts, so the two unnamed pastes are two library texts (no name sent): each case's default title must come from its own first record."""
    import glob
    text = open(glob.glob(os.path.join(C.ROOT, "evals", "library", f"{lib}*.txt"))[0]).read()
    st, c = api("POST", "/api/cases", {"text": text})
    assert st in (200, 201), (st, c)
    return c["token"]


def test_unnamed_pasted_cases_are_told_apart_by_their_own_records_and_a_rename_survives_reload(page, cs):
    t1, t2 = _paste("case_lib02"), _paste("case_lib01")
    try:
        _home(page, cs)
        a, b = (_row(page, t).get_by_test_id("cases-title").inner_text() for t in (t1, t2))
        assert a != b and "Sablewood Market" in a and "Dunmarrow" in b and "Untitled" not in a + b, (a, b)
        _row(page, t1).get_by_test_id("cases-open").click()                       # never analyzed: it opens on its Analyze button, not on a timeline
        expect(page.get_by_test_id("case-name")).to_contain_text("Sablewood Market")
        page.get_by_test_id("btn-rename-case").click()
        page.get_by_test_id("case-rename-input").fill("Rivera, neck"); page.keyboard.press("Enter")
        expect(page.get_by_test_id("case-name")).to_have_text("Rivera, neck")
        page.reload(); page.get_by_test_id("case-name").wait_for()
        expect(page.get_by_test_id("case-name")).to_have_text("Rivera, neck")
        page.get_by_test_id("btn-all-cases").click(); page.get_by_test_id("cases-overview").wait_for()
        expect(_row(page, t1).get_by_test_id("cases-title")).to_have_text("Rivera, neck")
    finally:
        for t in (t1, t2):
            api("DELETE", f"/api/cases/{t}")


def test_rename_failure_keeps_the_old_name_and_says_why(page, cs):
    page.route(re.compile(rf"/api/cases/{cs['a']}$"), lambda route: route.fulfill(status=422, json={"error": {"code": "bad_request", "message": "That name is too long."}}) if route.request.method == "PATCH" else route.continue_())
    open_case(page, cs["a"])
    page.get_by_test_id("btn-rename-case").click()
    page.get_by_test_id("case-rename-input").fill("x"); page.keyboard.press("Enter")
    expect(page.get_by_test_id("case-rename-error")).to_contain_text("too long")
    page.keyboard.press("Escape")
    expect(page.get_by_test_id("case-name")).to_have_text(TITLE["a"])


# ---- phone ---------------------------------------------------------------------------------------------------------------------------------------
def _no_h_scroll(page):
    return page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")


def test_phone_390_overview_and_detail_have_no_sideways_scroll_and_44px_targets(page, cs):
    page.set_viewport_size({"width": 390, "height": 844})
    _home(page, cs)
    assert _no_h_scroll(page), "overview scrolls sideways"
    for tid in ("cases-filter-all", "cases-filter-attention", "cases-filter-ready", "cases-sort"):
        assert page.get_by_test_id(tid).bounding_box()["height"] >= 43.5, tid
    assert _row(page, cs["a"]).get_by_test_id("cases-open").bounding_box()["height"] >= 43.5
    bar = _row(page, cs["a"]).get_by_test_id("cases-progress-entries").bounding_box()
    assert bar["width"] > 60 and bar["x"] + bar["width"] <= 390
    _row(page, cs["a"]).get_by_test_id("cases-open").click()
    page.get_by_test_id("case-overview").wait_for()
    assert _no_h_scroll(page), "detail scrolls sideways"
    ov = page.locator("[data-testid=case-overview] > .co-main").bounding_box()      # on a phone the block's slot sits under the entries (display: contents)
    assert ov["x"] >= 0 and ov["x"] + ov["width"] <= 391
    assert page.get_by_test_id("btn-all-cases").bounding_box()["height"] >= 43.5
    det = page.locator("[data-testid=case-stepper] details.zs-case-det")
    assert not det.evaluate("d => d.open"), "collapsed to one line on a phone"
    page.get_by_test_id("case-summary").click()
    assert det.evaluate("d => d.open")
    assert _no_h_scroll(page), "case checks scroll sideways"


# ---- screenshots (ZLAYT_SCREENSHOTS=1 writes artifacts/screenshots/multicase-*.png) -------------------------------------------------------------
@pytest.mark.skipif(os.environ.get("ZLAYT_SCREENSHOTS") != "1", reason="set ZLAYT_SCREENSHOTS=1 to write artifacts/screenshots/multicase-*.png")
def test_screenshots(page, cs):
    out = os.path.join(C.ROOT, "artifacts", "screenshots"); os.makedirs(out, exist_ok=True)
    for name, vw in (("1440", {"width": 1440, "height": 1000}), ("390", {"width": 390, "height": 844})):
        page.set_viewport_size(vw)
        _home(page, cs)
        page.screenshot(path=os.path.join(out, f"multicase-overview-{name}.png"), full_page=(name == "390"))
        open_case(page, cs["b"])
        expect(page.get_by_test_id("case-summary-gate")).to_be_visible()        # the case checks have loaded
        page.evaluate("window.scrollTo(0, 0)")
        page.screenshot(path=os.path.join(out, f"multicase-detail-{name}.png"), full_page=False)
        page.get_by_test_id("case-summary").click()                                # the case checks, step by step: pass / fail and why
        (page.get_by_test_id("case-overview") if name == "1440" else page.get_by_test_id("checks-card")).screenshot(path=os.path.join(out, f"multicase-detail-steps-{name}.png"))
