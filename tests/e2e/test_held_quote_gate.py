"""T-136 round 3 (paralegal r2 F-1, D-058; backend T-134 r3/r4): a re-picked quote under the AI's own summary, compared and accepted, is held by the export gate (JUDGE_NOT_RUN).
Before any rerun has tried the new quote, a rerun CAN clear it, so the case-level places offer it beside "Write the summary" (the server's own sentence says both) and never say "dismiss it".
After a rerun that gave no answer the server marks the blocker `rerun_no_answer`: a rerun can no longer clear it, so none is offered anywhere, nothing says "run it again", "try again" or
"dismiss it", and each place offers "Write the summary" (the same action as the blocker row). The places are the case rail's "Second AI check on every AI-made item" step, the "Ready to export?"
step, the "How the AI was checked" panel, and the sentence under the rerun button. Another accepted item the second check never ran on keeps its rerun (route stub: the fixture backend cannot produce that).
Also: the item field `second_check_pending` (T-134 r4) is what the page reads; the page does not infer it. Test ids (declared in conftest): btn-write-summary-case (the case-level Write the summary button).
Real backend, fixture set; edits the quote through the UI like test_edit_to_check."""
import re
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, JudgeNotRun, LiveRerun
from tests.e2e.test_edit_to_check import edited_quote, _accept_something_else, _row, _case   # noqa: F401  (edited_quote is a fixture)
from tests.e2e.test_stepper import open_rail

OLD = re.compile(r"run the second check again|dismiss (that|those|the) items?|run it again|try again", re.I)      # what a rerun-that-cannot-clear must never say
DISMISS = re.compile(r"dismiss (that|those|the) items?", re.I)


def _held(page, t):
    """The held state: the quote was re-picked (UI), something else is accepted so the gate has a letter, then she compares and accepts the re-picked entry."""
    LiveRerun(page)                       # T-157: plays a live backend until a rerun has been pressed
    _accept_something_else(t)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"]); row.get_by_test_id("btn-accept").click()
    expect(row).to_have_attribute("data-review", "accepted")
    got = next(x for x in _case(t["tok"])["entries"] if x["id"] == t["id"])
    assert got["second_check_pending"] is True, "the server says the second check has no answer on this item"
    page.reload(); page.get_by_test_id("timeline").wait_for()
    return got


def _gate_steps(page):
    cs = open_rail(page)
    return cs, cs.locator('[data-testid="case-step"][data-step-id="export_gate"]'), cs.locator('[data-testid="case-step"][data-step-id="judges"]')


def test_the_server_flag_is_what_the_row_reads(page, edited_quote):
    t = edited_quote; _held(page, t)
    expect(_row(page, t["id"]).get_by_test_id("compare-export-note")).to_be_visible()
    # a page that inferred the state would follow ladder / reasons; this one follows the field: answer with the flag false and the held note must go
    page.route(re.compile(r"/api/cases/[^/?]+$"), lambda r: r.fulfill(json=_flip(r.fetch().json(), t["id"])))
    page.reload(); page.get_by_test_id("timeline").wait_for()
    expect(_row(page, t["id"]).get_by_test_id("compare-export-note")).to_have_count(0)


def _flip(d, item_id):
    for e in d["entries"] + d["undated_entries"]:
        if e["id"] == item_id:
            e["second_check_pending"] = False
    return d




def _rerun_with_no_answer(page, t):
    """Press the case-level rerun once: the fixture backend has no recorded answer for the new quote, so the server marks the blocker rerun_no_answer."""
    cs, gate, _ = _gate_steps(page)
    gate.get_by_test_id("btn-rerun-judge").click()
    page.wait_for_function("() => { const t = [...document.querySelectorAll('[data-testid=rerun-status]')].map(n => n.textContent.trim()).filter(Boolean); return t.length > 0 && !t.some(x => /^Running/.test(x)); }", timeout=30000)
    g = next(s for s in api("GET", f"/api/cases/{t['tok']}/trace")[1]["steps"] if s["id"] == "export_gate")
    b = next(x for x in g["blockers"] if x["item_id"] == t["id"])
    assert b.get("rerun_no_answer") is True, b
    page.reload(); page.get_by_test_id("timeline").wait_for()
    return b


def test_before_a_rerun_the_case_steps_offer_it_beside_write_the_summary_and_never_say_dismiss(page, edited_quote):
    t = edited_quote; _held(page, t)
    cs, gate, judges = _gate_steps(page)
    for step, name in ((gate, "Ready to export?"), (judges, "Second AI check")):
        expect(step).to_have_count(1)
        txt = step.inner_text()
        assert not DISMISS.search(txt), (name, txt)
        assert "own words" in txt.lower(), (name, txt)
        expect(step.get_by_test_id("btn-write-summary-case")).to_be_visible()
    expect(gate.get_by_test_id("btn-rerun-judge")).to_have_count(1)
    assert "for this item" in gate.get_by_test_id("btn-rerun-judge").inner_text().lower()


def test_after_a_rerun_gave_no_answer_no_place_offers_a_rerun_or_says_dismiss_and_each_offers_write_the_summary(page, edited_quote):
    t = edited_quote; _held(page, t); _rerun_with_no_answer(page, t)
    cs, gate, judges = _gate_steps(page)
    for step, name in ((gate, "Ready to export?"), (judges, "Second AI check")):
        expect(step).to_have_count(1)
        txt = step.inner_text()
        assert not OLD.search(txt), (name, txt)
        assert "own words" in txt.lower(), (name, txt)
        expect(step.get_by_test_id("btn-write-summary-case")).to_be_visible()
        assert step.get_by_test_id("btn-rerun-judge").count() == 0, name
    nx = page.get_by_test_id("case-next-action")
    if nx.count():
        assert not OLD.search(nx.inner_text()), nx.inner_text()
    assert page.get_by_test_id("btn-rerun-judge").count() == 0, "the held quote is the only blocker: there is no rerun button anywhere on the page"
    panel = page.get_by_test_id("judge-panel"); panel.scroll_into_view_if_needed(); panel.locator("summary").first.click(); page.wait_for_timeout(300)
    assert not OLD.search(panel.inner_text()), panel.inner_text()
    expect(panel.get_by_test_id("btn-write-summary-case").first).to_be_visible()


def test_the_sentence_after_a_rerun_with_no_answer_points_to_the_summary_not_to_try_again(page, edited_quote):
    t = edited_quote; _held(page, t)
    cs, gate, _ = _gate_steps(page)
    gate.get_by_test_id("btn-rerun-judge").click()
    page.wait_for_function("() => { const t = [...document.querySelectorAll('[data-testid=rerun-status]')].map(n => n.textContent.trim()).filter(Boolean); return t.length > 0 && !t.some(x => /^Running/.test(x)); }", timeout=30000)
    said = " ".join(n.inner_text() for n in page.get_by_test_id("rerun-status").all())
    assert "own words" in said.lower() and not re.search(r"try again|dismiss", said, re.I), said


def test_write_the_summary_at_case_level_focuses_that_entrys_summary_box(page, edited_quote):
    t = edited_quote; _held(page, t); _rerun_with_no_answer(page, t)
    cs, gate, _ = _gate_steps(page)
    gate.get_by_test_id("btn-write-summary-case").click()
    ta = _row(page, t["id"]).get_by_test_id("edit-summary")
    expect(ta).to_be_visible(); expect(ta).to_be_focused()


def test_the_blocker_row_shows_the_servers_why_as_given_and_the_same_write_the_summary_action(page, edited_quote):
    t = edited_quote; _held(page, t); b = _rerun_with_no_answer(page, t)
    cs, gate, _ = _gate_steps(page)
    row = cs.get_by_test_id("gate-blocker").filter(has_text=b["why"][:60]); expect(row).to_have_count(1)     # the server's sentence, as given
    expect(row.get_by_test_id("btn-gate-write-summary")).to_be_visible()


def test_a_rerun_that_can_clear_is_still_offered_for_another_accepted_item_and_counts_only_that_one(page, edited_quote):
    """Mixed list: the held quote after a rerun that gave no answer, plus one other accepted item the second check never ran on. Only the other item gets the rerun, and the label counts one."""
    t = edited_quote; _held(page, t); _rerun_with_no_answer(page, t)
    JudgeNotRun(page, t["tok"], ["e1"], mode="still")
    page.reload(); page.get_by_test_id("timeline").wait_for()
    cs, gate, _ = _gate_steps(page)
    btn = gate.get_by_test_id("btn-rerun-judge"); expect(btn).to_have_count(1)
    assert "for this item" in btn.inner_text().lower(), btn.inner_text()
    expect(gate.get_by_test_id("btn-write-summary-case")).to_be_visible()
