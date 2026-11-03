"""T-144 (GATE-M2 legal-nurse major 2, UI half): under each entry, a "Not in an entry (n)" link in the row's link bar (it costs the compact row no height) opens "Also in this record, not in an entry (n)": the record's sentences no entry quote covers
(records[].uncovered[], T-143). Closed by default, each sentence verbatim, one click opens the source record with that sentence highlighted; never in the letter or the copy text.
Needs ZLAYT_MODE=local (library case lib09, Spanish interpreter). New test ids (declared in conftest): uncovered-summary (the link, aria-expanded), uncovered-list (the list, hidden until opened, data-record-count), uncovered-heading (the full wording), uncovered-item
(one <li> per sentence, data-record-id), uncovered-text (the verbatim sentence), btn-uncovered-jump ('Show in record')."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE, reveal

LIB = "case_lib09_spanish_interpreter_espalda"
norm = lambda s: re.sub(r"\s+", " ", s).strip()


def _run(tok):
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    assert s["status"] == "ready"


@pytest.fixture
def lib09():
    st, c = api("POST", "/api/cases", {"library": LIB})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    _run(c["token"])
    yield c["token"]
    api("DELETE", f"/api/cases/{c['token']}")


def _entry_of(case, record_id):
    return next(e for e in case["entries"] + case["undated_entries"] if e["record_ids"] == [record_id])


def _row(page, entry):
    return page.locator(f'[data-testid^="entry-"][data-entry-id="{entry["id"]}"]').first


def test_collapsed_list_with_count_and_verbatim_sentences(page, lib09):
    case = api("GET", f"/api/cases/{lib09}")[1]
    r1 = next(r for r in case["records"] if r["seq"] == 1)
    assert len(r1["uncovered"]) == 2
    open_case(page, lib09)
    row = _row(page, _entry_of(case, r1["id"]))
    box, summ = row.get_by_test_id("uncovered-list"), row.get_by_test_id("uncovered-summary")
    expect(summ).to_be_visible(); expect(summ).to_have_text("Not in an entry (2)")
    expect(summ).to_have_attribute("aria-expanded", "false")                       # closed
    expect(box).to_be_hidden(); expect(box.get_by_test_id("uncovered-text").first).to_be_hidden()   # the sentences wait behind the link
    summ.click()
    expect(summ).to_have_attribute("aria-expanded", "true")
    expect(box.get_by_test_id("uncovered-heading")).to_have_text("Also in this record, not in an entry (2)")
    texts = [t for t in box.get_by_test_id("uncovered-text").all_inner_texts()]
    assert texts == [u["text"] for u in r1["uncovered"]]                          # verbatim, in record order, nothing filtered by kinds
    assert box.get_by_test_id("uncovered-item").count() == 2


def test_an_entry_whose_record_is_fully_covered_has_no_list(page, lib09):
    case = api("GET", f"/api/cases/{lib09}")[1]
    r5 = next(r for r in case["records"] if r["seq"] == 5)
    assert r5["uncovered"] == []
    open_case(page, lib09)
    row = _row(page, _entry_of(case, r5["id"]))
    expect(row.get_by_test_id("uncovered-list")).to_have_count(0); expect(row.get_by_test_id("uncovered-summary")).to_have_count(0)


def test_one_click_opens_the_record_with_that_sentence_highlighted(page, lib09):
    case = api("GET", f"/api/cases/{lib09}")[1]
    r1 = next(r for r in case["records"] if r["seq"] == 1)
    target = next(u for u in r1["uncovered"] if u["text"].startswith("Patient states she was struck by a car"))
    open_case(page, lib09)
    row = _row(page, _entry_of(case, r1["id"])); box = row.get_by_test_id("uncovered-list")
    row.get_by_test_id("uncovered-summary").click()
    box.get_by_test_id("uncovered-item").filter(has_text=target["text"]).get_by_test_id("btn-uncovered-jump").click()
    expect(page.get_by_test_id("record-modal")).to_be_visible()
    hl = page.get_by_test_id("record-highlight")
    expect(hl).to_have_count(1)
    assert norm(hl.inner_text()) == norm(target["text"])
    expect(hl).to_be_in_viewport()


def test_keyboard_only(page, lib09):
    case = api("GET", f"/api/cases/{lib09}")[1]
    r3 = next(r for r in case["records"] if r["seq"] == 3)
    target = r3["uncovered"][0]
    open_case(page, lib09)
    row = _row(page, _entry_of(case, r3["id"])); box = row.get_by_test_id("uncovered-list")
    summ = row.get_by_test_id("uncovered-summary")
    summ.focus()
    page.keyboard.press("Enter")
    expect(summ).to_have_attribute("aria-expanded", "true"); expect(box).to_be_visible()
    jump = box.get_by_test_id("btn-uncovered-jump").first
    for _ in range(4):                                                            # More, then the list: the jump is the next stop after the row's own links
        page.keyboard.press("Tab")
        if jump.evaluate("n => n === document.activeElement"):
            break
    expect(jump).to_be_focused()
    expect(jump).to_have_accessible_name(re.compile(r"Show in record 3"))
    page.keyboard.press("Enter")
    expect(page.get_by_test_id("record-modal")).to_be_visible()
    assert norm(page.get_by_test_id("record-highlight").inner_text()) == norm(target["text"])
    page.keyboard.press("Escape")
    expect(page.get_by_test_id("record-modal")).to_be_hidden()
    expect(jump).to_be_focused()                                                  # focus comes back to the button she used


def test_usable_at_390px(pw, lib09):
    case = api("GET", f"/api/cases/{lib09}")[1]
    r6 = next(r for r in case["records"] if r["seq"] == 6)
    b = pw.chromium.launch()
    try:
        pg = b.new_context(viewport={"width": 390, "height": 844}).new_page()
        open_case(pg, lib09)
        row = _row(pg, _entry_of(case, r6["id"])); box = row.get_by_test_id("uncovered-list")
        row.scroll_into_view_if_needed()
        sb = row.get_by_test_id("uncovered-summary").bounding_box(); assert sb["height"] >= 24 and sb["x"] >= 0 and sb["x"] + sb["width"] <= 390
        row.get_by_test_id("uncovered-summary").click()
        assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")   # no sideways scroll
        for j in box.get_by_test_id("btn-uncovered-jump").all():
            bb = j.bounding_box()
            assert bb["height"] >= 36 and bb["x"] >= 0 and bb["x"] + bb["width"] <= 390
        for t in box.get_by_test_id("uncovered-text").all():
            bb = t.bounding_box(); assert bb["x"] >= 0 and bb["x"] + bb["width"] <= 390
        box.get_by_test_id("btn-uncovered-jump").nth(1).click()
        expect(pg.get_by_test_id("record-modal")).to_be_visible()
        assert norm(pg.get_by_test_id("record-highlight").inner_text()) == r6["uncovered"][1]["text"]
    finally:
        b.close()


def test_changing_the_quote_updates_the_list(page, lib09):
    """A sentence she adds to the quote leaves the list; the list comes from the server, so it is re-read after the save."""
    case = api("GET", f"/api/cases/{lib09}")[1]
    r1 = next(r for r in case["records"] if r["seq"] == 3)                         # record 3: adding its interpreter line to the quote is accepted by the save route
    n0 = len(r1["uncovered"])
    open_case(page, lib09)
    row = _row(page, _entry_of(case, r1["id"]))
    reveal(row.get_by_test_id("btn-edit-excerpt")).click()
    ed = row.get_by_test_id("excerpt-editor")
    units = ed.get_by_test_id("excerpt-unit")
    for i in range(units.count()):
        if not units.nth(i).is_checked():
            units.nth(i).click()
    ed.get_by_test_id("btn-save-excerpt").click()
    expect(row.get_by_test_id("edited-note")).to_be_visible()                      # the save landed
    now = api("GET", f"/api/cases/{lib09}")[1]
    after = next(r for r in now["records"] if r["seq"] == 3)["uncovered"]
    assert len(after) < n0
    row = _row(page, _entry_of(now, r1["id"]))
    if after:
        expect(row.get_by_test_id("uncovered-summary")).to_have_text(f"Not in an entry ({len(after)})")
    else:
        expect(row.get_by_test_id("uncovered-summary")).to_have_count(0); expect(row.get_by_test_id("uncovered-list")).to_have_count(0)


def test_never_in_the_letter_or_the_copy_text(page, sample_case):
    case = api("GET", f"/api/cases/{sample_case}")[1]
    texts = [u["text"] for r in case["records"] for u in r["uncovered"]]
    assert texts, "the sample has sentences no entry covers"
    open_case(page, sample_case)
    assert page.get_by_test_id("uncovered-summary").count() >= 1
    for b in page.get_by_test_id("btn-accept").all():
        b.click()
    page.get_by_test_id("btn-export").click()
    letter = page.get_by_test_id("export-letter")
    expect(letter).to_be_visible()
    page.get_by_test_id("btn-copy-letter").click()
    clip = page.evaluate("navigator.clipboard.readText()")
    # (an accepted flag may quote its own evidence sentence in the internal notes, by contract; the notes are not checked here)
    shown = norm(letter.inner_text()) + " " + norm(clip)
    for t in texts:
        assert norm(t) not in shown, t
    assert letter.get_by_test_id("uncovered-list").count() == 0 and letter.get_by_test_id("uncovered-summary").count() == 0
    exp = api("GET", f"/api/cases/{sample_case}/export")
    if exp[0] == 200:
        for t in texts:
            assert norm(t) not in norm(exp[1]["letter_text"]), t
