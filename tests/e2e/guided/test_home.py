"""T-181 (D-068) guided UI, Your cases (/): spec section 3. Builder A.
Test ids: btn-new-case, btn-sample-case, cases-list, cases-finished, cases-empty, cases-loading, cases-mode, case-card (data-token, data-title, data-finished), case-next, btn-continue, btn-rename, btn-delete,
btn-delete-yes, btn-delete-keep, rename-input, btn-rename-save, btn-rename-cancel, btn-remove-gone, find-case, page-error, btn-retry.
Real cases are made over the API (the guided Step 2 and 3 belong to another builder); list shapes the fixture cannot produce (running, failed, a stale summary, six or more cases) are served by a
route stub of GET /api/cases that keeps the real response shape (memory/contracts/api.md)."""
import json
import re
import pytest
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided._helpers import api, make_case, decide_all, uid, browser, shot, in_view, no_h_scroll, go, jbody, err
from tests.e2e.guided.test_shell_smoke import watch


@pytest.fixture
def made():
    toks = []
    yield toks
    for t in toks:
        api("DELETE", f"/api/cases/{t}")


def card(page, title):
    return page.locator(f"[data-testid=case-card][data-title={json.dumps(title)}]")


def row(token, title, status="ready", **kw):
    """One /api/cases summary row (api.md 'GET /api/cases')."""
    r = {"token": token, "title": title, "name": title, "source": "sample", "status": status, "record_count": 9, "created_at": "2026-11-02T10:00:00Z", "updated_at": "2026-11-02T10:00:00Z",
         "last_activity_at": "2026-11-02T10:00:00Z", "run": {"stage": "finalize", "steps_done": 7, "steps_total": 8, "running": False, "error": False},
         "progress": {"entries": {"decided": 0, "total": 9}, "flags": {"decided": 0, "total": 10}, "amounts": {"decided": 0, "total": 4}},
         "counts": {"pending": 23}, "hitl": {"pending": 23, "needs_review": 3, "needs_review_open": 3, "edits_to_check": 0, "could_not_verify": 0, "gate_blockers": [], "gate_warnings": []},
         "export_ready": False, "next_action": None, "status_error": False, "status_error_message": None}
    r.update(kw)
    return r


def stub_list(page, rows):
    def h(route):
        if route.request.method != "GET":
            return route.continue_()
        jbody(route, 200, {"cases": rows})
    page.route("**/api/cases", h)


def test_real_cases_show_the_next_line_the_track_and_where_continue_goes(pw, made):
    a = make_case(f"Home A {uid()}", run=False); b = make_case(f"Home B {uid()}"); c = make_case(f"Home C {uid()}", decide=True); made += [a, b, c]
    ta, tb, tc = (api("GET", f"/api/cases/{t}")[1]["title"] for t in (a, b, c))
    left = sum(1 for i in api("GET", f"/api/cases/{b}")[1]["entries"] + api("GET", f"/api/cases/{b}")[1]["undated_entries"] + api("GET", f"/api/cases/{b}")[1]["flags"] if i["review_status"] == "pending")
    br, page = browser(pw, 1440, 900)
    try:
        seen = watch(page)
        go(page, "/")
        expect(page.get_by_test_id("page-title")).to_have_text("Your cases")
        ca, cb, cc = card(page, ta), card(page, tb), card(page, tc)
        # a case only read: next is to draft it, Continue opens step 1
        expect(ca.get_by_test_id("case-next")).to_have_text("Next: Draft the timeline.")
        assert ca.get_by_test_id("btn-continue").get_attribute("href") == f"/case/{a}/records"
        assert ca.locator(".track li").evaluate_all("els => els.map(e => e.className)") == ["current", "", "", ""]
        # drafted, nothing decided: step 2 with the count; the first track bar is done and the second is current
        expect(cb.get_by_test_id("case-next")).to_have_text(f"Next: Check the timeline. {left} of {left} items left.")
        assert cb.get_by_test_id("btn-continue").get_attribute("href") == f"/case/{b}/timeline"
        assert cb.locator(".track li").evaluate_all("els => els.map(e => e.className)") == ["done", "current", "", ""]
        # everything decided and the gate open: it moves to Finished with a green Letter ready and Open letter
        fin = page.get_by_test_id("cases-finished")
        expect(fin.locator(f'[data-token="{c}"]')).to_have_count(1)
        assert cc.get_attribute("data-finished") == "1"
        expect(cc.get_by_test_id("case-next")).to_contain_text("Finished. Your letter is ready.")
        expect(cc.get_by_test_id("btn-continue")).to_have_text("Open letter")
        assert cc.get_by_test_id("btn-continue").get_attribute("href") == f"/case/{c}/letter"
        assert cc.locator(".track li").evaluate_all("els => els.map(e => e.className)") == ["done"] * 4
        assert page.get_by_test_id("cases-list").locator(f'[data-token="{c}"]').count() == 0
        # Continue is a real link: it opens that step
        cb.get_by_test_id("btn-continue").click()
        expect(page).to_have_url(re.compile(rf"/case/{b}/timeline$"))
        assert seen == [], seen
    finally:
        br.close()


def test_primary_button_is_above_the_fold_and_nothing_scrolls_sideways(pw, made):
    made.append(make_case(f"Home fold {uid()}", run=False))
    for w, h in ((1440, 900), (1366, 768), (390, 844)):
        br, page = browser(pw, w, h)
        try:
            go(page, "/")
            assert in_view(page, page.get_by_test_id("btn-new-case").first), (w, h)
            assert no_h_scroll(page), (w, h)
            shot(page, "home", w) if h in (900, 844) else None
        finally:
            br.close()


def test_rename_in_place_with_the_server_message_and_delete_with_one_confirm(pw, made):
    tok = make_case(f"Home rename {uid()}", run=False); made.append(tok)
    title = api("GET", f"/api/cases/{tok}")[1]["title"]
    br, page = browser(pw, 1440, 900)
    try:
        go(page, "/")
        c = card(page, title)
        before = c.bounding_box(); kids = lambda: c.evaluate("e => [...e.children].map(x => x.className + ':' + Math.round(x.getBoundingClientRect().height))"); k0 = kids()
        c.get_by_test_id("btn-rename").click()
        box = c.get_by_test_id("rename-input"); expect(box).to_be_focused()
        box.fill("Bad <name>"); c.get_by_test_id("btn-rename-save").click()
        expect(c.locator("[data-slot=meta]")).to_contain_text("Remove the angle brackets")        # the server's 422 sentence, shown in the card's reserved line, not as a banner
        expect(c.locator("[data-slot=meta]")).to_have_class(re.compile("bad"))
        assert api("GET", f"/api/cases/{tok}")[1]["title"] == title        # nothing saved
        assert c.bounding_box()["height"] == before["height"], (k0, kids())              # the card did not grow or shrink
        box.fill("Renamed " + uid()); newname = box.input_value()
        c.get_by_test_id("btn-rename-save").click()
        expect(card(page, newname)).to_have_count(1)
        assert api("GET", f"/api/cases/{tok}")[1]["title"] == newname
        c = card(page, newname)
        c.get_by_test_id("btn-rename").click(); c.get_by_test_id("rename-input").fill("Nope"); page.keyboard.press("Escape")
        expect(c.locator("h3")).to_have_text(newname)                      # Escape cancels
        # delete: one confirm in the same row; Keep it changes nothing
        c.get_by_test_id("btn-delete").click()
        expect(c.get_by_test_id("btn-delete-yes")).to_be_visible(); expect(c.get_by_test_id("btn-delete-keep")).to_be_focused()
        assert c.bounding_box()["height"] == before["height"]
        c.get_by_test_id("btn-delete-keep").click(); expect(c.get_by_test_id("btn-delete")).to_be_visible()
        assert api("GET", f"/api/cases/{tok}")[0] == 200
        c.get_by_test_id("btn-delete").click(); c.get_by_test_id("btn-delete-yes").click()
        expect(card(page, newname)).to_have_count(0)
        assert api("GET", f"/api/cases/{tok}")[0] == 404
    finally:
        br.close()


def test_empty_loading_and_error_states(pw):
    br, page = browser(pw, 1440, 900)
    try:
        seen = watch(page)
        # loading: three skeleton cards in the final card size while the list is on its way
        def slow(route):
            if route.request.method != "GET":
                return route.continue_()
            page.wait_for_timeout(900); jbody(route, 200, {"cases": []})
        page.route("**/api/cases", slow)
        page.goto(C.SERVER + "/")
        expect(page.get_by_test_id("cases-loading").locator(".skeleton")).to_have_count(3)
        sk = page.get_by_test_id("cases-loading").locator(".skeleton").first.bounding_box()
        expect(page.get_by_test_id("cases-empty")).to_be_visible(timeout=10000)
        assert sk["height"] >= 236
        # empty: the explanation and the two buttons; no second "new case" button above it
        expect(page.get_by_test_id("cases-empty")).to_contain_text("You don't have any cases yet.")
        expect(page.get_by_test_id("cases-empty")).to_contain_text("A case is one client's medical records. We'll guide you through 4 steps")
        expect(page.get_by_test_id("btn-new-case")).to_have_count(1)
        expect(page.get_by_test_id("btn-sample-case")).to_have_text("Open the sample case")
        shot(page, "home-empty", 1440)
        page.get_by_test_id("btn-sample-case").click()
        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
        tok = page.url.split("/case/")[1].split("/")[0]
        assert api("GET", f"/api/cases/{tok}")[1]["status"] == "ingested"
        api("DELETE", f"/api/cases/{tok}")
        # error: a plain sentence, the server's message when it has one, Try again; no status code or stack on screen
        page.unroute("**/api/cases")
        page.route("**/api/cases", lambda r: jbody(r, 500, err("internal", "boom")) if r.request.method == "GET" else r.continue_())
        go(page, "/")
        e = page.get_by_test_id("page-error"); expect(e).to_be_visible()
        expect(e).to_contain_text("We couldn't load your cases.")
        t = e.inner_text(); assert "500" not in t and "boom" not in t and "Failed to fetch" not in t
        page.unroute("**/api/cases")
        page.get_by_test_id("btn-retry").click()
        expect(page.get_by_test_id("page-error")).to_have_count(0)
        expect(page.get_by_test_id("page-title")).to_have_text("Your cases")
        assert [s for s in seen if "500" not in s] == [], seen        # the only noise allowed is the stubbed 500 resource line
    finally:
        br.close()


def test_stubbed_list_follows_the_next_line_rules_search_and_sort(pw):
    na = {"item_id": "f_gap_r6_r7", "kind": "flag", "reason": "The gap between record 6 and 7 needs a decision."}
    rows = [
        row("t1", "Alpha running", status="running", run={"stage": "judge_entries", "steps_done": 3, "steps_total": 8, "running": True, "error": False}, last_activity_at="2026-11-02T12:00:00Z"),
        row("t2", "Bravo failed", status="failed", run={"stage": "extract", "steps_done": 1, "steps_total": 8, "running": False, "error": True}, last_activity_at="2026-11-02T11:00:00Z"),
        row("t3", "Charlie bills", progress={"entries": {"decided": 9, "total": 9}, "flags": {"decided": 10, "total": 10}, "amounts": {"decided": 1, "total": 4}}, last_activity_at="2026-11-02T10:30:00Z"),
        row("t4", "Delta blocker", progress={"entries": {"decided": 9, "total": 9}, "flags": {"decided": 10, "total": 10}, "amounts": {"decided": 4, "total": 4}}, next_action=na,
            hitl={"pending": 0, "needs_review": 0, "needs_review_open": 0, "edits_to_check": 0, "could_not_verify": 0, "gate_blockers": [{"reason_code": "X", "kind": "flag", "item_id": "f_gap_r6_r7", "why": "x"}], "gate_warnings": []},
            last_activity_at="2026-11-02T10:20:00Z"),
        row("t5", "Echo stale", status="ready", record_count=None, counts=None, progress=None, hitl=None, next_action=None, status_error=True, status_error_message="We couldn't load this case's status", last_activity_at="2026-11-02T10:10:00Z"),
        row("t6", "Foxtrot done", progress={"entries": {"decided": 9, "total": 9}, "flags": {"decided": 10, "total": 10}, "amounts": {"decided": 4, "total": 4}}, export_ready=True, last_activity_at="2026-11-02T10:00:00Z"),
    ]
    br, page = browser(pw, 1440, 900)
    try:
        stub_list(page, rows); go(page, "/")
        nxt = lambda t: card(page, t).get_by_test_id("case-next")
        expect(nxt("Alpha running")).to_have_text("Next: Wait while the timeline is drafted (stage 4 of 8).")
        assert card(page, "Alpha running").get_by_test_id("btn-continue").get_attribute("href") == "/case/t1/records"
        expect(nxt("Bravo failed")).to_have_text("Next: Drafting stopped. Run it again.")
        expect(nxt("Charlie bills")).to_have_text("Next: Check the bills. 3 of 4 amounts left.")
        assert card(page, "Charlie bills").get_by_test_id("btn-continue").get_attribute("href") == "/case/t3/bills"
        expect(nxt("Delta blocker")).to_have_text("Next: Fix 1 problem before the letter. The gap between record 6 and 7 needs a decision.")
        assert card(page, "Delta blocker").get_by_test_id("btn-continue").get_attribute("href") == "/case/t4/timeline?item=f_gap_r6_r7"
        expect(nxt("Echo stale")).to_have_text("We couldn't load this case's status")            # the server's sentence, in place of the track and the next line
        expect(card(page, "Echo stale").get_by_test_id("btn-continue")).to_have_text("Open case")
        expect(card(page, "Echo stale").locator(".track")).to_have_count(0)
        expect(card(page, "Foxtrot done").get_by_test_id("btn-continue")).to_have_text("Open letter")
        # newest activity first, in two sections
        titles = page.get_by_test_id("cases-list").locator("h3").all_inner_texts()
        assert titles == ["Alpha running", "Bravo failed", "Charlie bills", "Delta blocker", "Echo stale"], titles
        expect(page.get_by_test_id("cases-finished").locator("h3")).to_have_text(["Foxtrot done"])
        # six or more cases: a search box that filters as she types and updates the section counts
        f = page.get_by_test_id("find-case"); expect(f).to_be_visible()
        f.fill("bills")
        expect(page.locator("[data-testid=case-card]:not([hidden])")).to_have_count(1)
        expect(page.locator("section[aria-label='In progress'] .c")).to_have_text("1")
        f.fill(""); expect(page.locator("[data-testid=case-card]:not([hidden])")).to_have_count(6)
        # 390 px: nothing clips or scrolls sideways
        page.set_viewport_size({"width": 390, "height": 844}); page.wait_for_timeout(200)
        assert no_h_scroll(page)
        for c in page.get_by_test_id("case-card").all():
            b = c.bounding_box(); assert b["x"] >= 0 and b["x"] + b["width"] <= 390
    finally:
        br.close()


def test_running_card_follows_its_stage_without_moving(pw):
    state = {"n": 0}
    def h(route):
        if route.request.method != "GET":
            return route.continue_()
        state["n"] += 1
        steps = min(state["n"], 6)
        jbody(route, 200, {"cases": [row("t1", "Streaming", status="running", run={"stage": "extract", "steps_done": steps, "steps_total": 8, "running": True, "error": False})]})
    br, page = browser(pw, 1440, 900)
    try:
        page.route("**/api/cases", h); go(page, "/")
        c = card(page, "Streaming"); expect(c.get_by_test_id("case-next")).to_contain_text("stage 2 of 8")
        box = c.bounding_box()
        expect(c.get_by_test_id("case-next")).to_contain_text("stage 4 of 8", timeout=9000)
        assert c.bounding_box() == box
    finally:
        br.close()


def test_public_mode_lists_the_cases_this_browser_started(pw, made):
    """GET /api/cases is 404 in public mode: the list is the tokens kept in localStorage, each read with GET /api/cases/{token}."""
    tok = make_case(f"Home public {uid()}"); made.append(tok)
    title = api("GET", f"/api/cases/{tok}")[1]["title"]
    br, page = browser(pw, 1440, 900)
    try:
        page.route("**/api/cases", lambda r: jbody(r, 404, err("not_found", "Not found.")) if r.request.method == "GET" else r.continue_())
        page.add_init_script(f"try {{ if (!sessionStorage.getItem('seeded')) {{ sessionStorage.setItem('seeded', '1'); localStorage.setItem('zl.guided.cases', JSON.stringify([{json.dumps(tok)}, 'a-token-that-is-gone'])); }} }} catch (e) {{}}")
        go(page, "/")
        expect(page.get_by_test_id("cases-mode")).to_have_text("These are the cases started in this browser. Keep the case link to open it elsewhere.")
        expect(card(page, title).get_by_test_id("case-next")).to_have_text(re.compile(r"^Next: Check the timeline\. \d+ of \d+ items left\.$"))
        gone = page.locator('[data-testid=case-card][data-token="a-token-that-is-gone"]')
        expect(gone.get_by_test_id("case-next")).to_contain_text("This case is no longer here. Cases are kept for 24 hours.")
        gone.get_by_test_id("btn-remove-gone").click()
        expect(gone).to_have_count(0)
        assert json.loads(page.evaluate("localStorage.getItem('zl.guided.cases')")) == [tok]
        # a case started in this browser is remembered (Step 1 stores it) and shows up here
        page.evaluate("localStorage.removeItem('zl.guided.cases')")
        page.add_init_script("void 0")
        go(page, "/new"); page.get_by_test_id("btn-read").click()
        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=15000)
        new = page.url.split("/case/")[1].split("/")[0]; made.append(new)
        assert json.loads(page.evaluate("localStorage.getItem('zl.guided.cases')")) == [new]
        go(page, "/")
        expect(page.locator(f'[data-token="{new}"]')).to_have_count(1)
    finally:
        br.close()


def test_dark_mode_and_390_screenshots(pw, made):
    made.append(make_case(f"Home dark {uid()}", run=False))
    br, page = browser(pw, 1440, 900, "dark")
    try:
        go(page, "/"); assert page.evaluate("getComputedStyle(document.body).backgroundColor") != "rgb(244, 246, 249)"
    finally:
        br.close()
    br, page = browser(pw, 390, 844)
    try:
        go(page, "/"); shot(page, "home", 390)
    finally:
        br.close()
