"""T-081 / T-082 round 3 (D-044, D-045): 'Run the second check again', the refused export shown beside the Export button, and pending items as a gate warning.
The fixture backend cannot leave an accepted recorded item without a judge answer, so those states are produced by the JudgeNotRun route-rewriting stub (conftest);
the pending-warning tests use the real backend."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, JudgeNotRun, WordingFails, reveal
from tests.e2e.test_stepper import open_rail, open_judges, active_in


def _accept(tok, n=3):
    c = api("GET", f"/api/cases/{tok}")[1]
    ids = [e["id"] for e in c["entries"] if e["state"] != "rejected" and e["date"]][:n]
    assert len(ids) == n
    for i in ids:
        assert api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "accept"})[0] == 200
    return ids


@pytest.fixture
def unrun(page, sample_case):
    """Three accepted entries whose second check 'never ran'; rejudge clears them."""
    ids = _accept(sample_case)
    return JudgeNotRun(page, sample_case, ids)


def in_view(page, loc):
    b = loc.bounding_box(); vh = page.viewport_size["height"]
    return b is not None and b["y"] >= 0 and b["y"] + min(b["height"], 40) <= vh


# ---- D-045: pending items are a warning, not a blocker
def test_pending_items_are_a_warning_not_a_blocker(page, sample_case):
    _accept(sample_case)
    open_case(page, sample_case); cs = open_rail(page)
    gate = cs.locator('[data-step-id="export_gate"]')
    expect(gate).to_have_attribute("data-status", "pass")
    assert gate.get_by_test_id("gate-blocker").count() == 0
    w = gate.get_by_test_id("gate-warning"); expect(w).to_have_attribute("data-warning-code", "ITEMS_NOT_REVIEWED")
    txt = w.inner_text().lower()
    assert "not reviewed" in txt and "will not be in the letter" in txt and "disclosure" in txt and "does not block" in txt
    assert re.search(r"Can export \u2014 \d+ not reviewed", cs.get_by_test_id("case-summary-gate").inner_text())
    w.get_by_test_id("btn-gate-warning-jump").click()
    assert page.evaluate("document.activeElement.getAttribute('data-review')") == "pending"
    page.get_by_test_id("btn-export").click()                      # the export opens even though items are pending
    expect(page.get_by_test_id("export-letter")).to_be_visible()
    assert page.get_by_test_id("export-blocked").is_hidden()


def test_export_with_nothing_accepted_says_so_beside_the_button(page, sample_case):
    """422 export_blocked (nothing accepted): the message sits right under the toolbar, in view, focused; the rail stays as the human left it."""
    open_case(page, sample_case)
    page.get_by_test_id("btn-export").click()
    box = page.get_by_test_id("export-blocked"); expect(box).to_be_visible()
    assert "nothing is accepted" in box.get_by_test_id("export-blocked-msg").inner_text().lower()
    assert in_view(page, box) and active_in(page, '[data-testid="export-blocked"]')
    assert page.get_by_test_id("btn-export").is_visible() and in_view(page, page.get_by_test_id("btn-export"))
    assert page.locator("#view-export").is_hidden()
    assert page.get_by_test_id("case-stepper").locator("details.zs-case-det").evaluate("d => d.open") is False
    box.get_by_test_id("btn-export-blocked-close").click(); expect(box).to_be_hidden()


# ---- D-044: the rerun button wherever a JUDGE_NOT_RUN blocker or step appears
def test_rerun_button_in_rail_gate_and_blocker_rows(page, unrun):
    open_case(page, unrun.token); cs = open_rail(page)
    assert re.search(r"Export blocked by 3", cs.get_by_test_id("case-summary-gate").inner_text())
    gate = cs.locator('[data-step-id="export_gate"]')
    assert gate.get_by_test_id("gate-blocker").count() == 3
    rows = gate.get_by_test_id("gate-blocker")
    for i in range(3):
        assert rows.nth(i).get_by_test_id("btn-rerun-judge").count() == 0, "T-097 r3 m-2: one POST reruns every item, so a per-row button would promise one and do three"
    assert "never got the second AI check" in gate.get_by_test_id("step-action").inner_text()
    gb = gate.get_by_test_id("btn-rerun-judge"); assert gb.count() == 1
    assert gb.inner_text() == "Run the second check again for these 3", "the group button says how many items its one POST covers"
    judges = cs.locator('[data-step-id="judges"]')
    assert judges.get_by_test_id("step-action").get_by_test_id("btn-rerun-judge").count() == 1
    assert judges.get_by_test_id("btn-rerun-judge").inner_text() == "Run the second check again for these 3"
    assert "did not run on 3 items" in judges.get_by_test_id("step-action").inner_text()


def test_rerun_shows_busy_posts_once_and_clears_the_gate(page, sample_case):
    stub = JudgeNotRun(page, sample_case, _accept(sample_case), hold=True)
    open_case(page, sample_case); cs = open_rail(page)
    btn = cs.locator('[data-step-id="export_gate"]').get_by_test_id("step-action").get_by_test_id("btn-rerun-judge")
    btn.click()
    page.wait_for_function("() => document.querySelectorAll('[data-testid=btn-rerun-judge]').length > 0 && [...document.querySelectorAll('[data-testid=btn-rerun-judge]')].every(b => b.disabled)")
    assert "Running the second check on 3 items" in page.get_by_test_id("rerun-status").first.inner_text()
    stub.release()
    page.wait_for_function("() => document.querySelectorAll('[data-testid=gate-blocker]').length === 0", timeout=8000)
    assert stub.posts == 1
    assert re.search("Ready to export|Can export", page.get_by_test_id("case-summary-gate").inner_text())
    expect(cs.locator('[data-step-id="export_gate"]').get_by_test_id("rerun-status")).to_contain_text("ran on 3 items and answered for all of them")


def test_rerun_that_still_gets_no_answer_says_so(page, sample_case):
    stub = JudgeNotRun(page, sample_case, _accept(sample_case), mode="still")
    open_case(page, sample_case); cs = open_rail(page)
    cs.locator('[data-step-id="export_gate"]').get_by_test_id("step-action").get_by_test_id("btn-rerun-judge").click()
    st = cs.locator('[data-step-id="export_gate"]').get_by_test_id("rerun-status")
    expect(st).to_contain_text("still did not answer for 3 items of 3")
    assert "dismiss them" in st.inner_text()
    assert cs.locator('[data-step-id="export_gate"]').get_by_test_id("gate-blocker").count() == 3 and stub.posts == 1
    expect(page.get_by_test_id("btn-rerun-judge").first).to_be_enabled()


@pytest.mark.parametrize("w,h", [(1280, 900), (390, 844)])
def test_refused_export_shows_beside_the_button_with_blockers_and_rerun(pw, sample_case, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        stub = JudgeNotRun(pg, sample_case, _accept(sample_case))
        open_case(pg, sample_case)
        pg.get_by_test_id("btn-export").click()
        box = pg.get_by_test_id("export-blocked"); expect(box).to_be_visible()
        assert in_view(pg, box), "the message must be on screen, not far below"
        assert in_view(pg, pg.get_by_test_id("btn-export")), "T-097 r3 n-1: the Export button it explains stays on screen with the message"
        assert active_in(pg, '[data-testid="export-blocked"]')
        assert pg.locator("#view-export").is_hidden()
        msg = box.get_by_test_id("export-blocked-msg").inner_text()
        assert "3 accepted items have not had the second AI check" in msg
        assert box.get_by_test_id("gate-blocker").count() == 3
        assert box.get_by_test_id("btn-gate-jump").count() == 3
        pg.evaluate("document.activeElement.blur()")
        assert box.get_by_test_id("btn-rerun-judge").count() == 1 and box.get_by_test_id("btn-rerun-judge").inner_text() == "Run the second check again for these 3"
        box.get_by_test_id("btn-rerun-judge").first.click()
        expect(box.get_by_test_id("export-blocked-msg")).to_contain_text("Nothing blocks the export now")
        assert stub.posts == 1
        pg.get_by_test_id("btn-export").click()
        expect(pg.get_by_test_id("export-letter")).to_be_visible()
        assert pg.get_by_test_id("export-blocked").is_hidden()
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


def test_item_stepper_offers_the_rerun_on_the_skipped_judge_step(page, unrun):
    i = unrun.ids[0]
    open_case(page, unrun.token)
    reveal(page.locator(f'[data-testid="queue"] [data-item-id="{i}"]').get_by_test_id("entry-why")).click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    assert st.get_by_test_id("item-verdict").inner_text() == "Accepted, second check missing"
    j = st.locator('[data-step-id="judge_1"]')
    assert j.get_by_test_id("step-status").inner_text() == "Did not run"
    assert j.get_attribute("aria-current") == "step"
    j.get_by_test_id("btn-rerun-judge").click()
    page.wait_for_function("() => document.querySelector('[data-testid=item-verdict]').textContent !== 'Accepted, second check missing'", timeout=8000)
    assert unrun.posts == 1
    assert page.get_by_test_id("item-stepper").locator('[data-step-id="judge_1"]').get_by_test_id("btn-rerun-judge").count() == 0


# ---- T-082: the AI-check panel
def test_judge_panel_rows_for_accepted_unchecked_items_match_the_gate(page, unrun):
    open_case(page, unrun.token); jp = open_judges(page)
    assert "blocks export" in jp.get_by_test_id("judge-summary-counts").inner_text()
    rows = jp.get_by_test_id("judge-unresolved"); assert rows.count() == 3
    for i in range(3):
        t = rows.nth(i).inner_text()
        assert "then accept" not in t and "can't go in the letter yet" in t
        assert rows.nth(i).get_by_test_id("btn-rerun-judge").count() == 0, "one group button covers the list; rows would only repeat it"
    grp = jp.get_by_test_id("judge-rerun-group"); assert "Run the second check again for these 3" in grp.inner_text()
    assert jp.get_by_test_id("btn-rerun-judge").count() == 1
    grp.get_by_test_id("btn-rerun-judge").click()
    page.wait_for_function("() => document.querySelectorAll('[data-testid=judge-unresolved]').length === 0", timeout=8000)
    assert "blocks export" not in page.get_by_test_id("judge-summary-counts").inner_text()


def test_judge_panel_without_unchecked_items_is_unchanged(page, sample_case):
    open_case(page, sample_case); jp = open_judges(page)
    assert "blocks export" not in jp.get_by_test_id("judge-summary-counts").inner_text()
    assert jp.get_by_test_id("btn-rerun-judge").count() == 0


# ---- gate blockers: jump and update (moved here from test_stepper, now that only JUDGE_NOT_RUN items block)
def test_gate_blocker_jump_and_update(page, unrun):
    open_case(page, unrun.token); cs = open_rail(page)
    gate = cs.locator('[data-step-id="export_gate"]'); gate.wait_for()
    names = gate.get_by_test_id("btn-gate-jump").evaluate_all("els => els.map(e => e.getAttribute('aria-label'))")
    assert all(n and n.startswith("Go to item ") for n in names) and len(set(names)) == len(names)
    first = gate.get_by_test_id("gate-blocker").first; tid = first.get_attribute("data-jump-item"); before = gate.get_by_test_id("gate-blocker").count()
    first.get_by_test_id("btn-gate-jump").focus(); page.keyboard.press("Enter")
    assert page.evaluate("document.activeElement.getAttribute('data-item-id')") == tid
    page.keyboard.press("d")
    expect(page.locator(f'[data-item-id="{tid}"]').first).to_have_attribute("data-review", "dismissed")
    page.wait_for_function("(n) => document.querySelectorAll('[data-testid=gate-blocker]').length < n", arg=before, timeout=8000)


def test_first_blocking_item_is_the_first_in_the_queue(page, unrun):
    open_case(page, unrun.token); cs = open_rail(page)
    cs.locator('[data-step-id="export_gate"]').get_by_test_id("btn-step-action").filter(has_text="first blocking item").click()
    focused = page.evaluate("document.activeElement.getAttribute('data-item-id')")
    queue = page.locator('[data-testid="queue"] [data-item-id]').evaluate_all("els => els.map(e => e.getAttribute('data-item-id'))")
    assert focused == next(i for i in queue if i in unrun.ids)


# ---- T-097: where the rerun answer shows, and the panel agreeing with the gate
def vis(page, loc):
    b = loc.bounding_box(); vh = page.viewport_size["height"]
    return b is not None and b["y"] >= 0 and b["y"] + b["height"] <= vh


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_rerun_pressed_in_the_refused_export_message_answers_beside_the_button(pw, sample_case, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        stub = JudgeNotRun(pg, sample_case, _accept(sample_case, 8), mode="still", hold=True)
        open_case(pg, sample_case)
        pg.get_by_test_id("btn-export").click()
        box = pg.get_by_test_id("export-blocked"); expect(box).to_be_visible()
        btn = box.get_by_test_id("btn-rerun-judge"); assert btn.count() == 1, "the message has one rerun button; its rows only offer Go to item"
        st = box.get_by_test_id("rerun-status"); assert st.count() == 1
        btn.click()
        expect(st).to_contain_text("Running the second check on 8 items")
        expect(btn).to_be_disabled()
        assert vis(pg, st) and vis(pg, btn), "Running… must be on screen beside the button"
        assert abs(st.bounding_box()["y"] - btn.bounding_box()["y"]) < 120
        stub.release()
        expect(st).to_contain_text("still did not answer for 8 items of 8")
        assert vis(pg, st) and abs(st.bounding_box()["y"] - btn.bounding_box()["y"]) < 120
        expect(btn).to_be_enabled(); assert box.get_by_test_id("gate-blocker").count() == 8 and stub.posts == 1
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


@pytest.mark.parametrize("w,h", [(1440, 900), (390, 844)])
def test_failed_rerun_pressed_in_the_ai_check_panel_says_so_beside_the_button(pw, sample_case, w, h):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": w, "height": h}).new_page()
    try:
        stub = JudgeNotRun(pg, sample_case, _accept(sample_case), mode="still", hold=True)
        open_case(pg, sample_case); jp = open_judges(pg)
        grp = jp.get_by_test_id("judge-rerun-group"); btn = grp.get_by_test_id("btn-rerun-judge"); btn.scroll_into_view_if_needed(); btn.click()
        expect(grp.get_by_test_id("rerun-status")).to_contain_text("Running the second check on 3 items")
        stub.release()
        st = jp.get_by_test_id("judge-rerun-group").get_by_test_id("rerun-status")
        expect(st).to_contain_text("still did not answer for 3 items of 3")
        assert vis(pg, st) and abs(st.bounding_box()["y"] - jp.get_by_test_id("judge-rerun-group").get_by_test_id("btn-rerun-judge").bounding_box()["y"]) < 120
        assert jp.get_by_test_id("judge-unresolved").count() == 3 and "blocks export" in jp.get_by_test_id("judge-summary-counts").inner_text()
    finally:
        pg.unroute_all(behavior="ignoreErrors"); b.close()


def test_judge_panel_follows_the_gate_for_an_edited_item(page, sample_case):
    """D-045(b): the gate lists only the accepted AI-made items; the edited one is ready, so the panel must not say it blocks and must not offer a rerun for it."""
    ids = _accept(sample_case, 3)
    c = api("GET", f"/api/cases/{sample_case}")[1]
    edited = next(e for e in c["entries"] if e["state"] != "rejected" and e["date"] and e["id"] not in ids)
    st, _ = api("POST", f"/api/cases/{sample_case}/items/{edited['id']}/review", {"action": "edit", "edits": {"summary": edited["summary"].rstrip(".") + " per the record."}})
    assert st == 200
    JudgeNotRun(page, sample_case, ids, exempt=[edited["id"]])
    open_case(page, sample_case); jp = open_judges(page)
    summ = jp.get_by_test_id("judge-summary-counts").inner_text()
    assert summ.count("blocks export") == 1 and "blocks export: 3" in summ, "the summary counts the gate's 3 blockers, not the edited item"
    assert "1 edited by you, not AI-checked" in summ and "4 not checked" not in summ, "T-097 r3 m-1: each kind of item is named once"
    row = jp.locator(f'[data-testid="judge-unresolved"][data-target-item="{edited["id"]}"]')
    expect(row).to_have_count(1)
    t = row.inner_text()
    assert "Edited by you, not AI-checked" in t and "Blocks the export" not in t and "can't go in the letter" not in t
    assert row.get_by_test_id("btn-rerun-judge").count() == 0
    assert jp.get_by_test_id("judge-rerun-group").inner_text().count("these 3") == 1
    blocked_rows = jp.locator('[data-testid="judge-unresolved"]:has-text("Blocks the export")')
    assert blocked_rows.count() == 3


# ---- T-097 round 2 (D-045 b, T-098, D-047): the summary and the Why dialog read the gate and the item trace; a failing code check on an edited summary is a named blocker.
# Since T-100 the edit route refuses wording that fails a code check, so that gate state is produced by the WordingFails route stub (conftest); everything else is the real backend.
WORDING = "Your wording doesn't match the quote:"
# T-134 r2 (stale-test update): an edit that passes the code checks but that she has not yet compared with the quote and accepted is `edit_to_check`; the item trace words the verdict
# "Edited; waiting for your check" (memory/contracts/api.md, Item trace), not "Edited by you, not AI-checked" (that wording stays in the AI-check panel row and the judge step).
EDIT_WAITING = "Edited; waiting for your check"


def _edit(tok, i, summary):
    st, r = api("POST", f"/api/cases/{tok}/items/{i}/review", {"action": "edit", "edits": {"summary": summary}})
    assert st == 200, r
    return r


@pytest.fixture
def mixed(page, sample_case):
    """One accepted AI item; one edited summary the gate holds (stub: fails a code check); one edited summary that passes."""
    ids = _accept(sample_case, 1)
    pend = [e for e in api("GET", f"/api/cases/{sample_case}")[1]["entries"] if e["id"] not in ids and e["state"] != "rejected" and e["date"] and e["review_status"] == "pending"]
    bad, ok = pend[0], pend[1]
    _edit(sample_case, bad["id"], bad["summary"].rstrip(".") + " per the record.")
    _edit(sample_case, ok["id"], ok["summary"].rstrip(".") + " per the record.")
    stub = WordingFails(page, sample_case, [bad["id"]])
    return {"tok": sample_case, "bad": bad, "ok": ok, "accepted": ids[0], "stub": stub}


def test_failing_edit_is_a_named_blocker_in_the_panel_summary_and_row(page, mixed):
    t = mixed
    open_case(page, t["tok"]); jp = open_judges(page)
    summ = jp.get_by_test_id("judge-summary-counts").inner_text()
    assert "1 summary fails a check, blocks export: 1" in summ, "T-097 r3 m-1: named once, with the gate's count"
    assert summ.count("blocks export") == 1 and "2 not checked" not in summ and "3 not checked" not in summ
    cs = open_rail(page)
    assert "Export blocked by 1" in cs.get_by_test_id("case-summary-gate").inner_text(), "the rail and the panel summary agree"
    assert cs.get_by_test_id("case-verdict").text_content() == "1 summary fails a check", "T-098 r2: the case verdict exactly as the backend words it"
    assert jp.get_by_test_id("judge-case-verdict").text_content() == "1 summary fails a check", "the panel shows the same words"
    row = jp.locator(f'[data-testid="judge-wording"][data-target-item="{t["bad"]["id"]}"]')
    expect(row).to_have_count(1)
    txt = row.inner_text()
    assert WORDING in txt and "qualifier" in txt and "Blocks the export" in txt and "Edited by you, not AI-checked" not in txt
    assert "The export stays blocked until it passes" in txt, "the server's fix sentence is shown as the next step"
    assert jp.locator(f'[data-testid="judge-unresolved"][data-target-item="{t["bad"]["id"]}"]').count() == 0, "one row per item"
    row.get_by_test_id("btn-judge-edit").click()
    ta = page.locator(f'[data-item-id="{t["bad"]["id"]}"]').first.get_by_test_id("edit-summary")
    expect(ta).to_be_visible(); assert active_in(page, f'[data-item-id="{t["bad"]["id"]}"]')


def test_passing_edit_says_edited_by_you_in_panel_and_judge_step_and_waiting_in_why(page, mixed):
    """D-045(b) wording in the panel and the judge step; T-134 r2: the Why dialog verdict of an edit she has not yet accepted is EDIT_WAITING (edit_to_check)."""
    t = mixed
    open_case(page, t["tok"]); jp = open_judges(page)
    row = jp.locator(f'[data-testid="judge-unresolved"][data-target-item="{t["ok"]["id"]}"]')
    if row.count():   # the report lists the edited item as unchecked; the row follows the gate, which does not hold it
        assert "Edited by you, not AI-checked" in row.inner_text() and "Blocks the export" not in row.inner_text() and row.get_by_test_id("btn-rerun-judge").count() == 0
    assert jp.get_by_test_id("judge-summary-counts").inner_text().count("blocks export") == 1, "only the failing edit blocks"
    reveal(page.locator(f'[data-testid="queue"] [data-item-id="{t["ok"]["id"]}"]').get_by_test_id("entry-why")).click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    assert st.get_by_test_id("item-verdict").inner_text() == EDIT_WAITING
    j = st.locator('[data-step-id="judge_1"]')
    assert j.get_by_test_id("step-status").inner_text() == "Not needed" and j.get_by_test_id("btn-rerun-judge").count() == 0
    assert "said:" not in j.inner_text() and "Unavailable" not in j.inner_text(), "T-097 r3 m-new-1: a Not-needed step prints no second-check verdict"
    assert "second check missing" not in st.inner_text().lower() and st.locator('[data-status="fail"]').count() == 0
    assert st.get_by_test_id("item-wording-fail").count() == 0


def test_why_dialog_for_a_failing_edit_says_the_wording_does_not_match_with_an_edit_action(page, mixed):
    t = mixed
    open_case(page, t["tok"])
    reveal(page.locator(f'[data-testid="queue"] [data-item-id="{t["bad"]["id"]}"]').get_by_test_id("entry-why")).click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    w = st.get_by_test_id("item-wording-fail")
    assert WORDING in w.inner_text() and "qualifier" in w.inner_text().lower()
    assert st.get_by_test_id("item-verdict").inner_text() != "Edited by you, not AI-checked"
    assert "second check missing" not in st.inner_text().lower() and st.get_by_test_id("btn-rerun-judge").count() == 0
    w.get_by_test_id("btn-wording-edit").click()
    expect(page.locator("#why-modal")).not_to_be_visible()
    expect(page.locator(f'[data-item-id="{t["bad"]["id"]}"]').first.get_by_test_id("edit-summary")).to_be_visible()


def test_rail_blocker_row_names_the_wording_problem_with_an_edit_button(page, mixed):
    t = mixed
    open_case(page, t["tok"]); cs = open_rail(page)
    row = cs.locator(f'[data-testid="gate-blocker"][data-jump-item="{t["bad"]["id"]}"]')
    expect(row).to_have_count(1); assert WORDING in row.inner_text()
    assert row.get_by_test_id("btn-gate-edit").count() == 1 and row.get_by_test_id("btn-rerun-judge").count() == 0
    page.get_by_test_id("btn-export").click()   # the refused export lists the same blocker with the same words
    box = page.get_by_test_id("export-blocked"); expect(box).to_be_visible()
    assert WORDING in box.get_by_test_id("gate-blocker").inner_text() and box.get_by_test_id("btn-rerun-judge").count() == 0


def test_fixing_the_wording_clears_panel_dialog_and_rail(page, mixed):
    """T-134 r2: once the failing wording is replaced, the Why dialog reads EDIT_WAITING (edited, not yet accepted by her), not a failure."""
    t = mixed
    _edit(t["tok"], t["bad"]["id"], t["bad"]["summary"].rstrip(".") + " as recorded.")   # any new wording ends the stub's failure, as a passing edit ends the real one
    open_case(page, t["tok"]); page.reload(); page.get_by_test_id("timeline").wait_for(); jp = open_judges(page)
    assert jp.get_by_test_id("judge-wording").count() == 0
    assert "fails a check" not in jp.get_by_test_id("judge-summary-counts").inner_text() and jp.get_by_test_id("judge-case-verdict").count() == 0
    assert re.search("Ready to export|Can export", open_rail(page).get_by_test_id("case-summary-gate").inner_text())
    reveal(page.locator(f'[data-testid="queue"] [data-item-id="{t["bad"]["id"]}"]').get_by_test_id("entry-why")).click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    assert st.get_by_test_id("item-verdict").inner_text() == EDIT_WAITING and st.get_by_test_id("item-wording-fail").count() == 0


@pytest.mark.parametrize("typed,shown", [("Visit 8: pain 4/10, improving; billed $9,000.", "$9,000"), ("Pain 4/10, improving in the left arm.", "left"), ("Pain 4/10, improving.", None)])
def test_refused_edit_shows_the_reason_inline_and_keeps_the_typed_text_no_confirm_dialog(page, sample_case, typed, shown):
    """D-047: a number, side or negation that is not in the quote is a hard 422: the reason sits under the edit box, the text stays, there is no 'keep my wording' choice.
    (The third case is the unchanged summary: it saves, so no error line.)"""
    open_case(page, sample_case); e = page.get_by_test_id("entry-5"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill(typed); e.get_by_test_id("btn-save-edit").click()
    if shown is None:
        expect(e).to_have_attribute("data-review", "edited"); return
    err = e.locator(".rv-error"); expect(err).to_contain_text(shown); expect(err).to_contain_text("quote")
    assert e.get_by_test_id("edit-summary").input_value() == typed and e.get_by_test_id("edit-summary").is_visible()
    assert e.get_attribute("data-review") != "edited"
    assert page.get_by_test_id("btn-keep-wording").count() == 0 and page.get_by_test_id("warning-list").count() == 0
