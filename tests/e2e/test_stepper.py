"""Vertical steppers (T-081) and the 'How the AI was checked' panel (T-082, D-042). Needs the fixture backend; the library case needs ZLAYT_MODE=local."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE, reveal

CASE_STEPS = ["ingest", "split", "dates", "extract", "grounding", "judges", "flags", "totals", "review", "export_gate"]


def _run(tok):
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


# D-059 (T-140 r2) then D-060 (default-deny charges, 35d8280): code marks "Amount due: $1,150" (a7) and, since default-deny, the undated "office visits $1,100" in the record-4 statement (a2)
# as unclear, and the recorded second check disagrees on each (SHOULD_BE_CHARGE). So L6 has FIVE judge objections (four amounts a2, a3, a4, a7 and one flag f_r5_1); it was three before D-059.
L6_OBJECTIONS = 5


@pytest.fixture
def judged_case():
    """Library L6: five judge objections (four amounts, one flag; D-059 added "Amount due", D-060 default-deny added the undated "office visits $1,100") and several code-vs-AI disagreements. Local mode only."""
    st, c = api("POST", "/api/cases", {"library": "case_lib06_lop_billed_vs_adjusted"})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    _run(c["token"])
    yield c["token"]
    api("DELETE", f"/api/cases/{c['token']}")


def open_rail(page):
    """The case checks are collapsed to one line by default; open them like a user does."""
    cs = page.get_by_test_id("case-stepper"); cs.get_by_test_id("case-summary").wait_for()
    if not cs.locator("details.zs-case-det").evaluate("d => d.open"):
        cs.get_by_test_id("case-summary").click()
    cs.get_by_test_id("case-step").first.wait_for()
    return cs


def open_judges(page):
    jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
    if not jp.locator("details.zj-det").evaluate("d => d.open"):
        jp.get_by_test_id("judge-summary").click()
    jp.get_by_test_id("judge-totals").wait_for()
    return jp


def active_in(page, css):
    return page.evaluate("(c) => !!(document.activeElement && document.activeElement.closest(c))", css)


def open_why(page, n=8):
    reveal(page.get_by_test_id(f"entry-{n}").get_by_test_id("entry-why")).click()
    page.get_by_test_id("item-stepper").wait_for()
    return page.get_by_test_id("item-stepper")


# ---- item stepper
def test_item_stepper_in_why_panel(page, sample_case):
    """Why? shows an ordered list of steps with a status word, a kind chip (Code / AI draft / AI check / You) and the plain-words why."""
    open_case(page, sample_case); st = open_why(page)
    assert st.locator("ol").count() == 1
    steps = st.get_by_test_id("step")
    assert steps.count() >= 8
    kinds = {steps.nth(i).get_by_test_id("step-kind").inner_text() for i in range(steps.count())}
    assert {"Code", "AI check", "You"} <= kinds
    for i in range(steps.count()):
        s = steps.nth(i)
        assert s.get_attribute("data-status") in ("pass", "fail", "skipped", "pending")
        assert s.get_by_test_id("step-why").inner_text().strip()
        assert s.get_by_test_id("step-status").inner_text().strip() in ("Passed", "Failed", "Skipped", "Not done yet", "Needs your decision", "Blocked")
        assert s.get_by_test_id("step-marker").inner_text().strip() in ("✓", "✕", "–", "○")   # glyph plus word, never colour alone


def test_pending_human_step_says_what_to_do(page, sample_case):
    """The human step is pending until you decide, carries aria-current=step, and states what you need to do with a working button."""
    open_case(page, sample_case); st = open_why(page)
    human = st.locator('[data-step-id="human"]')
    expect(human).to_have_attribute("data-status", "pending")
    expect(human).to_have_attribute("aria-current", "step")
    assert st.locator('[aria-current="step"]').count() == 1
    assert "What you need to do" in human.get_by_test_id("step-action").inner_text()
    assert human.get_by_test_id("step-status").inner_text() == "Needs your decision"
    human.get_by_test_id("btn-step-action").focus(); page.keyboard.press("Enter")          # keyboard: lands on the item's own controls
    expect(page.locator("#why-modal")).not_to_be_visible()
    assert page.evaluate("!!document.activeElement.closest('[data-item-id]')")


def test_decision_settles_the_human_step(page, sample_case):
    """After you accept, the human step passes."""
    open_case(page, sample_case)
    page.get_by_test_id("entry-8").get_by_test_id("btn-accept").click()
    expect(page.get_by_test_id("entry-8")).to_have_attribute("data-review", "accepted")
    st = open_why(page)
    expect(st.locator('[data-step-id="human"]')).to_have_attribute("data-status", "pass")


def test_flag_and_charge_cards_open_their_stepper(page, sample_case):
    """Flags and charges have no Why? button; a 'How it was checked' button opens the same stepper (flags: code-made flags skip the judge on purpose)."""
    open_case(page, sample_case)
    reveal(page.get_by_test_id("flags-panel").get_by_test_id("btn-trace")).first.click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    assert st.locator('[data-step-id="human"]').count() == 1
    page.keyboard.press("Escape")
    reveal(page.get_by_test_id("charges-panel").get_by_test_id("btn-trace")).first.click()
    page.get_by_test_id("item-stepper").wait_for()
    assert page.get_by_test_id("item-stepper").locator('[data-step-id="found_in_text"]').count() == 1


def test_failed_step_shows_reason_evidence_and_action(page, judged_case):
    """A judge objection renders as a failed AI-check step with the fixed-sentence reason and a 'What you need to do' line."""
    open_case(page, judged_case)
    tid = page.get_by_test_id("judge-rejection").first.get_attribute("data-target-item")
    reveal(page.locator(f'[data-trace-for="{tid}"]')).first.click()
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    judge = st.locator('[data-step-id^="judge"]')
    expect(judge).to_have_attribute("data-status", "fail")
    assert judge.get_by_test_id("step-kind").inner_text() == "AI check"
    assert "second ai check said" in judge.get_by_test_id("step-judge-reason").inner_text().lower()
    assert "What you need to do" in judge.get_by_test_id("step-action").inner_text()
    assert st.locator('[data-status="fail"]').count() >= 1


# ---- case stepper
def test_case_rail_is_one_line_by_default(page, sample_case):
    """Round 2: the case checks are collapsed to a one-line summary and do not push the review queue down; the judge row is one line too."""
    open_case(page, sample_case)
    cs = page.get_by_test_id("case-stepper"); cs.get_by_test_id("case-summary").wait_for()
    assert cs.locator("details.zs-case-det").evaluate("d => d.open") is False
    cs.get_by_test_id("case-summary-gate").wait_for()
    txt = cs.get_by_test_id("case-summary").inner_text().replace("\n", " ")
    assert re.search(r"\d+/10 checks passed", txt) and re.search(r"\d+ need you", txt) and re.search(r"Export blocked by \d+", txt)
    assert cs.bounding_box()["height"] < 120
    jp = page.get_by_test_id("judge-panel"); assert jp.bounding_box()["height"] < 120
    q = page.locator('[data-testid="queue"] [data-item-id]').first
    assert q.bounding_box()["y"] - (cs.bounding_box()["y"] + cs.bounding_box()["height"]) < 320   # only the judge row and the toolbar sit between
    assert page.evaluate("document.activeElement.closest && !document.activeElement.closest('details.zs-case-det[open]')")


def test_case_stepper_order_progress_and_gate(page, sample_case):
    """Ten case steps in the fixed order, 'x/10 checks passed', and the export gate lists each blocker."""
    open_case(page, sample_case); cs = open_rail(page)
    ids = cs.get_by_test_id("case-step").evaluate_all("els => els.map(e => e.getAttribute('data-step-id'))")
    assert ids == CASE_STEPS
    assert re.fullmatch(r"\d+/10 checks passed", cs.get_by_test_id("case-summary-progress").inner_text())
    gate = cs.locator('[data-step-id="export_gate"]')
    expect(gate).to_have_attribute("data-status", "fail")
    assert gate.get_by_test_id("step-status").inner_text() == "Blocked"
    n = gate.get_by_test_id("gate-blocker").count()
    assert n >= 1
    assert cs.locator('[aria-current="step"]').count() == 1
    prog = cs.get_by_test_id("case-progress").inner_text()
    assert re.search(r"\d+ passed", prog) and "settled" not in prog and "need" in prog


def test_case_steps_that_need_you_have_a_working_action(page, judged_case):
    """Round 2: every failed or pending case step has an action button that moves focus to what the step is about; none is dead."""
    open_case(page, judged_case); cs = open_rail(page)
    targets = {"judges": '[data-panel="judges"]', "totals": '[data-panel="charges"]', "review": '[data-item-id][data-review="pending"]', "export_gate": "[data-item-id]"}
    need = cs.locator('[data-testid="case-step"][data-status="fail"], [data-testid="case-step"][data-status="pending"]')
    ids = need.evaluate_all("els => els.map(e => e.getAttribute('data-step-id'))")
    assert set(targets) <= set(ids)
    for sid in ids:
        step = page.get_by_test_id("case-stepper").locator(f'[data-step-id="{sid}"]')
        btns = step.get_by_test_id("btn-step-action")
        assert btns.count() >= 1, f"{sid} has no action"
        page.evaluate("document.activeElement && document.activeElement.blur()")
        btns.first.click()
        if sid in targets:
            page.wait_for_function("(c) => !!(document.activeElement && document.activeElement.closest(c))", arg=targets[sid], timeout=4000)
        if not page.get_by_test_id("case-stepper").locator("details.zs-case-det").evaluate("d => d.open"):
            page.get_by_test_id("case-stepper").get_by_test_id("case-summary").click()
    judges = page.get_by_test_id("case-stepper").locator('[data-step-id="judges"]')
    assert f"{L6_OBJECTIONS} items the AI objected to" in judges.get_by_test_id("step-action").inner_text()
    assert page.locator("details.zj-det").evaluate("d => d.open")      # the jump opened the collapsed panel


def test_case_stepper_marks_failed_judges_and_links_to_panel(page, judged_case):
    """The judges step needs the human when the AI objected, shows counts, and its button opens the AI-check panel at the questioned items."""
    open_case(page, judged_case); cs = open_rail(page)
    j = cs.locator('[data-step-id="judges"]')
    expect(j).to_have_attribute("data-status", "fail")
    assert j.get_by_test_id("step-status").inner_text() == "Needs your decision"
    assert f"AI objected {L6_OBJECTIONS}" in j.get_by_test_id("step-counts").inner_text()
    j.get_by_test_id("btn-step-action").click()
    expect(page.get_by_test_id("judge-panel").get_by_test_id("judge-totals")).to_be_visible()
    assert page.get_by_test_id("judge-rejection").count() == L6_OBJECTIONS


def test_case_rail_has_no_developer_vocabulary(page, sample_case):
    """Reason codes, rule rows and raw count keys live in Technical details, not in the primary view."""
    open_case(page, sample_case); cs = open_rail(page)
    txt = cs.evaluate("""el => { const c = el.cloneNode(true); c.querySelectorAll('details[data-testid=step-tech]').forEach(d => d.remove()); return c.innerText; }""")
    assert not re.search(r"[A-Z]{3,}_[A-Z_]+|rule row|lexicon|llm ", txt), txt


# ---- judge panel
def test_judge_panel_collapsed_summary_and_labels(page, judged_case):
    """T-082 r2: one summary row with the counts; closed by default; opening shows the label, models and totals; internals stay in Technical details."""
    open_case(page, judged_case)
    jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
    assert jp.locator("details.zj-det").evaluate("d => d.open") is False and jp.bounding_box()["height"] < 120
    expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(rf"\d+ checked, \d+ agreed with the draft, {L6_OBJECTIONS} questioned"))   # counts load after the row (retrying assert, not a snapshot)
    jp = open_judges(page)
    label = jp.get_by_test_id("judge-label").inner_text()
    assert "AI quality checks" in label and "not a verdict" in label
    totals = jp.get_by_test_id("judge-totals").inner_text().lower()
    for w in ("items checked by ai", "agreed with the draft", "ai objected", "could not decide", "unavailable"):
        assert w in totals
    assert re.search(r"claude-\S+", jp.get_by_test_id("judge-model-line").inner_text())
    visible = jp.evaluate("""el => { const c = el.cloneNode(true); c.querySelectorAll('details:not(.zj-det)').forEach(d => d.remove()); return c.innerText; }""")
    assert not re.search(r"[A-Z]{3,}_[A-Z_]+|_v\d|prompt", visible), visible      # reason codes and prompt versions are inside closed Technical details
    jp.get_by_test_id("judge-tech").locator("summary").first.click()
    assert "_v" in jp.get_by_test_id("judge-prompts").inner_text()
    j = api("GET", f"/api/cases/{judged_case}/judges")[1]
    assert str(j["totals"]["items_judged"]) in totals.replace("\n", " ")


def test_judge_panel_one_row_per_item_with_record_cue(page, judged_case):
    """T-082 r2: an item appears once (objection and disagreement merged into chips); every row says which record it is from; no two titles are identical."""
    open_case(page, judged_case); jp = open_judges(page)
    rows = jp.locator("[data-target-item]")
    ids = rows.evaluate_all("els => els.map(e => e.getAttribute('data-target-item'))")
    assert len(ids) == len(set(ids)) and len(ids) >= 4
    assert jp.get_by_test_id("judge-rejection").count() == L6_OBJECTIONS
    titles = jp.get_by_test_id("judge-row-title").evaluate_all("els => els.map(e => e.innerText)")
    assert len(titles) == len(set(titles)), titles
    assert all(re.search(r"Records? \d", t) for t in titles), titles
    assert any(t.startswith("Attorney referral") for t in titles)
    j = api("GET", f"/api/cases/{judged_case}/judges")[1]
    assert len(ids) == len({r["item_id"] for k in ("rejections", "unresolved", "disagreements") for r in j[k]})
    assert {"a2", "a7"} <= {r["item_id"] for r in j["rejections"]}, "T-155 r2 / D-059, D-060: the record-5 'Amount due $1,150' (a7) and the undated 'office visits $1,100' (a2) are among the objections, not just a count"
    for aid in ("a2", "a7"):
        assert jp.locator(f'[data-testid="judge-rejection"][data-target-item="{aid}"]').count() == 1
    assert f"({L6_OBJECTIONS} items)" in jp.get_by_test_id("judge-rejections").locator("h3").inner_text()
    rej = jp.get_by_test_id("judge-rejection").first
    assert "What you need to do" in rej.inner_text()
    assert "primary" in (rej.get_by_test_id("btn-judge-goto").get_attribute("class") or "")


def test_judge_rejection_links_to_item_stepper(page, judged_case):
    """Each rejection opens the item's stepper (via the keyboard) and can jump to the item."""
    open_case(page, judged_case); jp = open_judges(page)
    row = jp.get_by_test_id("judge-rejection").first; row.wait_for()
    tid = row.get_attribute("data-target-item")
    row.get_by_test_id("btn-judge-steps").focus(); page.keyboard.press("Enter")
    st = page.get_by_test_id("item-stepper"); st.wait_for()
    assert st.locator('[data-status="fail"][data-step-id^="judge"]').count() == 1
    page.keyboard.press("Escape")
    row.get_by_test_id("btn-judge-goto").click()
    assert page.evaluate("document.activeElement.getAttribute('data-item-id')") == tid


def test_judge_panel_when_nothing_objected(page, sample_case):
    """A clean case says so plainly in the summary; the panel is still there."""
    open_case(page, sample_case)
    jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
    expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(r"checked \d+, all agreed"))   # counts load after the panel (retrying assert, not a snapshot)
    jp = open_judges(page)
    assert "No objections" in jp.inner_text()
    assert jp.get_by_test_id("judge-rejection").count() == 0


# ---- item dialog and narrative
def test_why_dialog_opens_on_the_step_that_needs_you(pw, judged_case):
    """Round 2: at 390 px the Why dialog shows the step that needs the human and its button without scrolling, and focus is on that step."""
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 390, "height": 844}).new_page(); open_case(pg, judged_case)
    row = pg.locator('[data-testid="queue"] [data-item-id][data-state="needs_review"]').first
    reveal(row.get_by_test_id("entry-why")).click(); pg.get_by_test_id("item-stepper").wait_for()
    pg.wait_for_function("() => document.activeElement && document.activeElement.getAttribute('aria-current') === 'step'")
    st = pg.get_by_test_id("item-stepper")
    assert "Needs your decision" in st.get_by_test_id("item-active").inner_text() or "Failed" in st.get_by_test_id("item-active").inner_text()
    btn = st.locator('[aria-current="step"]').get_by_test_id("btn-step-action").first
    box = btn.bounding_box()
    assert box and 0 <= box["y"] and box["y"] + box["height"] <= 844, box
    prog = st.get_by_test_id("item-progress").inner_text()
    assert "passed" in prog and "settled" not in prog
    st.get_by_test_id("btn-jump-active").click()
    assert pg.evaluate("document.activeElement.getAttribute('aria-current')") == "step"
    b.close()


def test_no_page_offers_the_drafted_paragraph(page, sample_case):
    """T-179 / D-067: the drafted treatment paragraph is cut from the MVP UI. Even with an accepted entry there is no panel, no Draft button and no TREATMENT SUMMARY."""
    assert api("POST", f"/api/cases/{sample_case}/items/e1/review", {"action": "accept"})[0] == 200
    open_case(page, sample_case)
    for tid in ("narrative-panel", "btn-draft-narrative", "btn-accept-narrative", "narrative-sentence"):
        assert page.get_by_test_id(tid).count() == 0, tid
    assert page.locator('[data-panel="narrative"]').count() == 0
    assert "Draft treatment paragraph" not in page.locator("body").inner_text()


# ---- mobile
def test_steppers_usable_at_390(pw, sample_case):
    """At 390 px the case stepper, the item stepper and their buttons fit without horizontal scroll; buttons are touch-sized."""
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 390, "height": 844}).new_page(); open_case(pg, sample_case)
    cs = pg.get_by_test_id("case-stepper"); cs.locator("summary").first.wait_for(); cs.locator("summary").first.click()
    cs.get_by_test_id("case-step").first.wait_for()
    assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
    for btn in cs.get_by_test_id("btn-gate-jump").all()[:3]:
        assert btn.bounding_box()["height"] >= 40
    reveal(pg.get_by_test_id("entry-8").get_by_test_id("entry-why")).click(); pg.get_by_test_id("item-stepper").wait_for()
    assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
    assert pg.evaluate("(() => { const d = document.querySelector('#why-modal'); return d.scrollWidth <= d.clientWidth + 1; })()")
    b.close()
