"""Stretch: two-pane source viewer. R-ST-1 (T-046). At >= 1024 px the record pane sits beside the queue and follows the selected item;
below 1024 px the R-RV-9 modal is the only viewer. The explicit "Open record" button always opens the modal (core R-RV-9)."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE

norm = lambda s: re.sub(r"\s+", " ", s).strip()


def test_record_pane_visible_at_1280(page, sample_case):
    """R-ST-1: at >= 1024 px the record pane sits beside the queue (no modal) and shows the clicked item's highlighted excerpt."""
    open_case(page, sample_case)
    pane = page.get_by_test_id("sbs-pane"); expect(pane).to_be_visible()
    q = page.get_by_test_id("queue").bounding_box(); p = pane.bounding_box()
    assert p["x"] >= q["x"] + q["width"] - 1, (p, q)          # beside, not below
    page.get_by_test_id("entry-8").click()
    expect(page.get_by_test_id("sbs-highlight")).to_be_visible(); expect(page.get_by_test_id("record-modal")).not_to_be_visible()
    ex = page.get_by_test_id("entry-8").get_by_test_id("entry-excerpt").inner_text()
    assert norm(page.get_by_test_id("sbs-highlight").inner_text()) == norm(ex)


def test_stepping_updates_the_highlight(page, sample_case):
    """R-ST-1: moving through three queue items by keyboard (j) updates the pane each time; the highlight equals the focused row's excerpt."""
    open_case(page, sample_case); seen = []
    page.get_by_test_id("entry-1").focus()      # start in the entry queue; j/k walk the entries from here
    for _ in range(3):
        page.keyboard.press("j")
        ex = page.evaluate("""() => { const r = document.activeElement.closest('[data-item-id]'); const q = r && r.querySelector('[data-testid=entry-excerpt]'); return q ? q.innerText : null; }""")
        assert ex, "focused item should be an entry with an excerpt"
        expect(page.get_by_test_id("sbs-highlight")).to_have_text(re.compile(r"\S"))
        hl = page.get_by_test_id("sbs-highlight").inner_text(); assert norm(hl) == norm(ex)
        seen.append(norm(hl))
    assert len(set(seen)) == 3, seen


def test_highlight_in_view_without_moving_page(page, sample_case):
    """The pane scrolls itself to the highlight; the page does not jump. Records are inserted as text (no markup)."""
    open_case(page, sample_case); page.get_by_test_id("entry-8").click()
    hl = page.get_by_test_id("sbs-highlight"); body = page.get_by_test_id("sbs-body")
    b = body.bounding_box(); h = hl.bounding_box(); assert b["y"] <= h["y"] and h["y"] + h["height"] <= b["y"] + b["height"] + 1
    assert page.get_by_test_id("sbs-pane").locator("script, img, iframe").count() == 0


def test_flag_shows_both_records(page, sample_case):
    """Selecting the 73-day gap flag shows records 6 and 7 in the pane, with no modal."""
    open_case(page, sample_case); page.get_by_test_id("flags-panel").locator("[data-flag-type=gap]").first.click()
    t = page.get_by_test_id("sbs-pane").inner_text(); assert "Record 6" in t and "Record 7" in t
    expect(page.get_by_test_id("record-modal")).not_to_be_visible()


def test_open_record_button_still_opens_modal(page, sample_case):
    """R-RV-9 stays core: the explicit Open record button opens the modal even at 1280 px."""
    open_case(page, sample_case); page.get_by_test_id("entry-8").get_by_test_id("btn-source").click()
    expect(page.get_by_test_id("record-modal")).to_be_visible()


def test_p_moves_focus_into_pane_and_escape_returns(page, sample_case):
    """Keyboard access: p focuses the scrollable pane, Esc returns to the selected row."""
    open_case(page, sample_case)
    page.get_by_test_id("queue").locator("[data-item-id]").first.focus()      # WCAG 2.1.4: letter keys act only from an item row (T-060)
    page.keyboard.press("p")
    expect(page.get_by_test_id("sbs-body")).to_be_focused()
    page.keyboard.press("Escape"); expect(page.locator(":focus")).to_have_attribute("data-item-id", re.compile(r".+"))


def test_mobile_fallback(page, sample_case):
    """R-ST-1: at 375 px there is no pane and the R-RV-9 modal opens instead."""
    page.set_viewport_size({"width": 375, "height": 800}); open_case(page, sample_case)
    expect(page.get_by_test_id("sbs-pane")).not_to_be_visible()
    page.get_by_test_id("entry-8").get_by_test_id("btn-source").click()
    expect(page.get_by_test_id("record-modal")).to_be_visible(); expect(page.get_by_test_id("record-highlight")).to_be_visible()


# ---- round 2 (ux-designer review) ----

def test_pane_floats_and_does_not_push_the_queue_down(page, sample_case):
    """The pane is a fixed overlay in the right margin: the queue keeps its single-column width at 1440 and the page height barely changes
    when the pane's body class is removed."""
    page.set_viewport_size({"width": 1440, "height": 900}); open_case(page, sample_case)
    assert page.get_by_test_id("sbs-pane").evaluate("e => getComputedStyle(e).position") == "fixed"
    q = page.get_by_test_id("queue").bounding_box(); assert q["width"] >= 880, q          # was 788 when the pane was a grid column
    h_on = page.evaluate("document.documentElement.scrollHeight")
    page.evaluate("document.body.classList.remove('sbs-on')"); page.wait_for_timeout(100)
    h_off = page.evaluate("document.documentElement.scrollHeight")
    assert h_on <= h_off + 40, (h_on, h_off)          # the pane adds no meaningful height (only the main-column margin differs)
    page.evaluate("document.body.classList.add('sbs-on')")


def test_gap_flag_one_action_away_at_1440x900(page, sample_case):
    """ux-designer finding 1: the pane is visible without scrolling at 1440x900 and carries a flag summary whose button focuses the first gap flag."""
    page.set_viewport_size({"width": 1440, "height": 900}); open_case(page, sample_case)
    btn = page.get_by_test_id("sbs-show-flag"); expect(btn).to_be_visible()
    b = btn.bounding_box(); assert 0 <= b["y"] and b["y"] + b["height"] <= 900, b
    assert "gap" in page.get_by_test_id("sbs-flags").inner_text()
    btn.click()
    gap = page.get_by_test_id("flags-panel").locator("[data-flag-type=gap]").first
    expect(gap).to_be_focused()
    g = gap.bounding_box(); assert g["y"] < 900 and g["y"] + g["height"] > 0, g          # scrolled into the viewport
    t = page.get_by_test_id("sbs-pane").inner_text(); assert "Record 6" in t and "Record 7" in t


def test_single_record_item_has_one_record_heading(page, sample_case):
    """ux-designer finding 3: for entry-8 the pane shows exactly one heading that starts with 'Record 8'."""
    open_case(page, sample_case); page.get_by_test_id("entry-8").click()
    expect(page.get_by_test_id("sbs-highlight")).to_be_visible()
    n = page.get_by_test_id("sbs-pane").evaluate("e => [...e.querySelectorAll('h1,h2,h3,h4')].filter(h => h.textContent.trim().startsWith('Record 8')).length")
    assert n == 1, n


def test_enter_on_a_focused_row_selects_it_into_the_pane(page, sample_case):
    """ux-designer finding 2: Enter on a focused queue row shows that row's record, even after the pane followed another item."""
    open_case(page, sample_case); page.get_by_test_id("entry-3").focus(); page.get_by_test_id("entry-8").focus()
    page.evaluate("document.querySelector('[data-testid=entry-3]').focus()")      # pane now follows entry-3
    row = page.get_by_test_id("entry-8"); row.focus()
    ex = row.get_by_test_id("entry-excerpt").inner_text()
    page.get_by_test_id("sbs-body").evaluate("e => { e.innerHTML = ''; }")         # blank the pane so only Enter can refill it
    row.press("Enter")
    expect(page.get_by_test_id("sbs-highlight")).to_be_visible(); assert norm(page.get_by_test_id("sbs-highlight").inner_text()) == norm(ex)
