"""T-203 (phone): at 375x667 the tick box of a disputed line can sit below the action bar. The greyed Yes must say why, in the status slot beside it.
Also: a payment's second-check wording names the damages way, and chart shorthand ('Pt') is not underlined as an outside word."""
from playwright.sync_api import expect

from tests.e2e.guided.test_round2 import LIB10, phone, item, make, open_item   # noqa: F401  (make is a fixture)

HINT = "Tick the box to say you compared them."


def test_375x667_disabled_yes_says_why_in_the_status_slot_beside_the_buttons(pw, make):
    tok = make(LIB10); b, page = phone(pw, 375, 667)
    try:
        open_item(page, tok, "e1")
        expect(page.get_by_test_id("check-compare")).to_be_attached()
        yes, st = page.get_by_test_id("answer-yes"), page.get_by_test_id("status-text")
        expect(yes).to_be_disabled()
        expect(st).to_have_text(HINT)
        r = page.evaluate("""() => { const q = (s) => document.querySelector('[data-testid=' + s + ']').getBoundingClientRect(), y = q('answer-yes'), s = q('status-text'), bar = q('actions');
            return { yes: [y.top, y.bottom], st: [s.top, s.bottom, s.left, s.right], bar: [bar.top, bar.bottom], vh: innerHeight, vw: innerWidth, lines: Math.round(s.height / parseFloat(getComputedStyle(document.querySelector('[data-testid=status-text]')).lineHeight)) }; }""")
        assert r["st"][0] >= r["bar"][0] - 0.5 and r["st"][1] <= r["vh"] and r["st"][2] >= 0 and r["st"][3] <= r["vw"], ("the hint is not fully on screen inside the action bar", r)
        assert r["yes"][0] >= r["bar"][0] - 0.5 and r["yes"][1] <= r["vh"], ("the Yes button is not on screen with the hint", r)
        assert r["lines"] <= 2 and r["bar"][0] > 470, ("the hint is more than two lines, or the bar grew", r)
        page.get_by_test_id("check-compare").check(force=True)
        expect(yes).to_be_enabled()
        expect(st).not_to_have_text(HINT)
        page.get_by_test_id("check-compare").uncheck(force=True)
        expect(yes).to_be_disabled(); expect(st).to_have_text(HINT)
    finally:
        b.close()


def test_the_hint_is_not_shown_on_a_line_with_no_tick_box(pw, make):
    tok = make(); b, page = phone(pw, 375, 667)
    try:
        open_item(page, tok, "e2")
        expect(page.get_by_test_id("answer-yes")).to_be_enabled()
        expect(page.get_by_test_id("status-text")).not_to_contain_text("Tick the box")
    finally:
        b.close()


def test_chart_shorthand_pt_is_not_underlined_and_the_damages_way_is_named(pw, make):
    from tests.e2e.guided.test_round2 import LIB11
    tok = make(LIB11); b, page = phone(pw, 390, 844)
    try:
        open_item(page, tok, "e2")
        out = set(page.get_by_test_id("outside-word").all_inner_texts())
        assert "Patient" not in out and "struck" in out, out
        open_item(page, tok, "a6", step="bills")
        reason = page.get_by_test_id("compare-reason")
        expect(reason).to_contain_text("damages figure")
        assert "lost pay" not in reason.inner_text()
        assert "not a bill" not in reason.inner_text()
    finally:
        b.close()


# ------------------------------------------------------------------ round 2: the reworded line, position-neutral words, PT is not a patient

def _words(page, summary, quote):
    return page.evaluate("""([s, q]) => { const p = window.G.step2.outsideParts(s, q); return p ? p.filter((n) => n && n.nodeType === 1).map((n) => n.textContent) : []; }""", [summary, quote])


def test_pt_in_capitals_is_physical_therapy_not_a_patient_but_pt_alone_still_reads_as_patient(pw, make):
    tok = make(); b, page = phone(pw, 390, 844)
    try:
        open_item(page, tok, "e1")
        assert "Patient" in _words(page, "Patient attended physical therapy 3 times a week", "PT 3x/week, attended physical therapy"), "PT is not the word patient"
        assert _words(page, "Patient states chest pain", "Pt states chest pain") == [], "Pt is the chart shorthand for patient"
        assert _words(page, "Patient states chest pain", "PATIENT states chest pain") == []
    finally:
        b.close()


def test_375x667_after_fixing_the_wording_the_reason_for_the_greyed_yes_stays_until_she_ticks(pw, make):
    tok = make(); b, page = phone(pw, 375, 667)
    try:
        open_item(page, tok, "e4")
        page.get_by_test_id("btn-third").click()
        page.get_by_test_id("edit-summary").fill(page.get_by_test_id("edit-summary").input_value() + " Reviewed.")
        page.get_by_test_id("answer-yes").click()
        yes, st, show = page.get_by_test_id("answer-yes"), page.get_by_test_id("status-text"), page.get_by_test_id("btn-show-box")
        expect(page.get_by_test_id("check-compare")).to_be_attached(); expect(yes).to_be_disabled()
        expect(st).to_contain_text("Saved"); expect(st).to_contain_text("Tick the box to say you compared them.")
        assert "above" not in st.inner_text().lower() and "below" not in st.inner_text().lower()
        page.wait_for_timeout(1500)
        expect(st).to_contain_text("Tick the box")                       # it stays; it does not time out
        bar = page.evaluate("document.querySelector('[data-testid=actions]').getBoundingClientRect().top")
        box_in_view = lambda: page.evaluate("""(bar) => { const r = document.querySelector('[data-testid=check-compare]').getBoundingClientRect(); return r.top >= 0 && r.bottom <= bar - 2; }""", bar)
        if show.is_visible():                                             # the box is under the bar or below the screen: one tap brings it into view
            show.click(); page.wait_for_timeout(300)
            assert box_in_view(), "Show box did not bring the tick box above the bar"
            assert page.evaluate("document.activeElement && document.activeElement.dataset.testid") == "check-compare"
        else:
            assert box_in_view(), "no Show box button, yet the tick box is not in view"
        page.get_by_test_id("check-compare").check(force=True)
        expect(yes).to_be_enabled(); expect(st).not_to_contain_text("Tick the box"); expect(show).to_be_hidden()
        expect(st).to_contain_text("Saved: your wording is in")
        page.get_by_test_id("check-compare").uncheck(force=True)
        expect(yes).to_be_disabled(); expect(st).to_contain_text("Tick the box to say you compared them.")
    finally:
        b.close()


def test_375x667_the_show_box_button_is_there_when_the_box_is_hidden_and_the_hint_stays_one_line_at_rest(pw, make):
    tok = make(LIB10); b, page = phone(pw, 375, 667)
    try:
        open_item(page, tok, "e1")
        st, show = page.get_by_test_id("status-text"), page.get_by_test_id("btn-show-box")
        expect(st).to_have_text(HINT)
        hidden = page.evaluate("""() => { const r = document.querySelector('[data-testid=check-compare]').getBoundingClientRect(), b = document.querySelector('[data-testid=actions]').getBoundingClientRect(); return r.bottom > b.top - 4; }""")
        assert hidden, "this size is expected to hide the box"
        expect(show).to_be_visible()
        show.click(); page.wait_for_timeout(300)
        assert page.evaluate("""() => { const r = document.querySelector('[data-testid=check-compare]').getBoundingClientRect(), b = document.querySelector('[data-testid=actions]').getBoundingClientRect(); return r.top >= 0 && r.bottom <= b.top; }""")
    finally:
        b.close()
