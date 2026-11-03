"""T-060 round 3 (frontend): shortcut sheet, compact rows, decided rows, 320 px reflow, theme-toggle name, file-input focus, held rechecks (T-096 skip links,
T-114 gap-change notice), and the two coordinator additions from reviews/T-119-staff-engineer.md: (1) a negative test for the row-only key rule and
(2) a Tab/Enter/Space-only review of one item plus an export (R-RV-4, WCAG 2.1.1 / 2.1.4).
New test ids (declared in tests/e2e/conftest.py, 'T-060 round 3'): shortcuts-list, entry-toggle, btn-start-review, checks-card, btn-download-letter, btn-download-notes.
Needs the fixture backend; the library cases need ZLAYT_MODE=local."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, BASE

BAD_TEXT = re.compile(r"\[object|\bundefined\b|\bnull\b")


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
    st, c = api("POST", "/api/cases", {"library": "case_lib09_spanish_interpreter_espalda"})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    _run(c["token"])
    yield c["token"]
    api("DELETE", f"/api/cases/{c['token']}")


def active(page):
    return page.evaluate("(() => { const a = document.activeElement; return a ? { tid: a.getAttribute('data-testid'), item: a.getAttribute('data-item-id'), tag: a.tagName } : null; })()")


def tab_until(page, testid, limit=40):
    for _ in range(limit):
        page.keyboard.press("Tab")
        a = active(page)
        if a and a["tid"] == testid:
            return a
    raise AssertionError(f"Tab never reached {testid}; last {active(page)}")


# ---- 1. the shortcut sheet
def test_shortcut_sheet_lists_the_keys_and_prints_no_object(page, sample_case):
    open_case(page, sample_case)
    page.get_by_test_id("btn-shortcuts").click()
    dlg = page.get_by_test_id("shortcuts-modal"); expect(dlg).to_be_visible()
    lst = dlg.get_by_test_id("shortcuts-list")
    expect(lst.locator("kbd")).to_have_count(11)
    expect(lst.locator("dt")).to_have_count(11); expect(lst.locator("dd")).to_have_count(11)
    txt = dlg.inner_text()
    assert "Accept the selected item" in txt and "Dismiss the selected item" in txt and not BAD_TEXT.search(txt), txt
    page.keyboard.press("Escape"); expect(dlg).to_be_hidden()
    page.wait_for_function("() => document.activeElement && document.activeElement.getAttribute('data-testid') === 'btn-shortcuts'")   # the dialog hands focus back to its opener first; focusing the row before that raced it (flaky at HEAD 078c5ae)
    # '?' from an item row opens the same sheet
    page.get_by_test_id("entry-1").focus(); page.keyboard.press("?"); expect(page.get_by_test_id("shortcuts-modal")).to_be_visible()


def test_no_object_undefined_or_null_text_on_the_review_page(page, sample_case):
    open_case(page, sample_case)
    assert not BAD_TEXT.search(page.locator("body").inner_text()), BAD_TEXT.findall(page.locator("body").inner_text())


# ---- 2. the row-only key rule (negative test): j, a and Shift+A do nothing from the page body, Export or an input
def _snapshot(page):
    return page.evaluate("""() => ({ accepted: document.querySelectorAll('[data-review=accepted],[data-review=dismissed],[data-review=edited]').length,
        dialogs: document.querySelectorAll('dialog[open]').length, active: (document.activeElement || {}).tagName + ':' + ((document.activeElement || {}).getAttribute ? document.activeElement.getAttribute('data-testid') : '') })""")


def test_letter_keys_do_nothing_from_body_export_or_an_input(page, sample_case):
    open_case(page, sample_case)
    before = _snapshot(page)
    # from the page body
    page.evaluate("document.activeElement && document.activeElement.blur()")
    for k in ("j", "a", "d", "Shift+A", "?"):
        page.keyboard.press(k)
    assert _snapshot(page) == {**before, "active": _snapshot(page)["active"]}, "a key acted from the page body"
    assert page.evaluate("!document.activeElement.closest || !document.activeElement.closest('[data-item-id]')")
    # from the Export button
    page.get_by_test_id("btn-export").focus()
    for k in ("j", "a", "d", "Shift+A", "?"):
        page.keyboard.press(k)
    s = _snapshot(page)
    assert s["accepted"] == before["accepted"] and s["dialogs"] == 0 and s["active"].endswith("btn-export"), s
    # from an input: the edit box of an item, and the sort control
    page.get_by_test_id("entry-1").get_by_test_id("btn-edit").click()
    ta = page.get_by_test_id("entry-1").get_by_test_id("edit-summary"); expect(ta).to_be_focused()
    start = ta.input_value()
    for k in ("j", "a", "d", "Shift+A"):
        page.keyboard.press(k)
    s = _snapshot(page)
    assert s["accepted"] == before["accepted"] and s["dialogs"] == 0, s
    assert ta.input_value() == start + "jadA"                       # they were typed, not run
    page.keyboard.press("Escape")
    page.get_by_test_id("sort").focus()
    for k in ("j", "a", "Shift+A"):
        page.keyboard.press(k)
    assert _snapshot(page)["accepted"] == before["accepted"] and _snapshot(page)["dialogs"] == 0


def test_p_focuses_the_record_pane_only_from_an_item_row(page, sample_case):
    """WCAG 2.1.4: 'p' (side-by-side pane) has its own gate in sidebyside.js. Pane on, then p from the body, Export, the header and an input does nothing."""
    open_case(page, sample_case)
    page.get_by_test_id("queue").locator("[data-item-id]").first.focus()
    page.keyboard.press("p")
    expect(page.get_by_test_id("sbs-body")).to_be_focused()           # from an item row it works, and the pane now shows an item
    page.keyboard.press("Escape")
    assert page.evaluate("!!document.activeElement.closest('[data-item-id]')"), "Escape should return focus to the item row"
    focus = lambda: page.evaluate("(() => { const a = document.activeElement; return (a.tagName || '') + ':' + (a.getAttribute('data-testid') || a.id || ''); })()")
    page.evaluate("document.activeElement.blur()")
    before = focus()
    page.keyboard.press("p")
    assert focus() == before, f"p moved focus from the page body: {before} -> {focus()}"
    for tid in ("btn-export", "btn-shortcuts", "sort"):
        page.get_by_test_id(tid).focus(); here = focus()
        page.keyboard.press("p")
        assert focus() == here, f"p moved focus from {tid}: {here} -> {focus()}"
    assert not page.get_by_test_id("sbs-body").evaluate("e => e === document.activeElement")


def test_letter_key_with_a_window_open_says_so(page, sample_case):
    """paralegal F11: o then a used to do nothing, silently."""
    open_case(page, sample_case)
    page.get_by_test_id("entry-1").focus(); page.keyboard.press("o"); expect(page.get_by_test_id("record-modal")).to_be_visible()
    page.keyboard.press("a")
    expect(page.locator("#rv-live")).to_contain_text("Press Escape")
    assert page.locator("[data-review=accepted]").count() == 0


# ---- 3. Tab, Enter and Space only: review one item, then export (R-RV-4)
def test_review_one_item_and_export_with_tab_enter_and_space_only(page, sample_case):
    tok = sample_case
    c = api("GET", f"/api/cases/{tok}")[1]
    ids = [e["id"] for e in c["entries"] if e["state"] == "verified" and e["date"]]
    assert api("POST", f"/api/cases/{tok}/review/batch", {"action": "accept", "item_ids": ids})[0] == 200   # setup by API: the checked entries are in the letter
    open_case(page, tok)
    # (a) one item reviewed by keyboard: Tab to the first skip link, Enter, then Tab to the item's Dismiss button, Enter
    page.evaluate("document.activeElement && document.activeElement.blur()")
    tab_until(page, "skip-review", 6)
    page.keyboard.press("Enter")
    row = active(page); assert row["item"], row
    item = row["item"]
    tab_until(page, "btn-dismiss", 12)
    page.keyboard.press("Enter")
    expect(page.locator(f'[data-item-id="{item}"]').first).to_have_attribute("data-review", "dismissed")
    # (b) the export, from a fresh load, by keyboard only
    page.reload(); page.get_by_test_id("timeline").wait_for()
    page.evaluate("document.activeElement && document.activeElement.blur()")
    tab_until(page, "skip-export", 10)
    page.keyboard.press("Enter")
    assert active(page)["tid"] == "btn-export"
    page.keyboard.press("Enter")
    expect(page.get_by_test_id("export-letter")).to_be_visible()
    tab_until(page, "btn-copy-letter", 6)
    page.keyboard.press("Space")
    expect(page.get_by_test_id("copy-confirm")).to_be_visible()      # 13 items are still pending, so Copy asks first
    assert active(page)["tid"] == "btn-copy-anyway"                  # the confirmation took focus; Enter goes through it
    page.keyboard.press("Enter")
    expect(page.locator("#export-status")).to_contain_text("Copied the treatment section")


# ---- 4. density
def test_first_screen_shows_entries_and_rows_are_compact(pw, sample_case):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, sample_case)
    try:
        rows = pg.locator('[data-testid=queue] > article')
        assert rows.count() >= 5
        boxes = rows.evaluate_all("els => els.map(e => { const r = e.getBoundingClientRect(); return [r.top + scrollY, r.height, e.getAttribute('data-state')]; })")
        assert boxes[0][0] < 520, boxes[:2]                                           # first entry above the fold
        first = pg.get_by_test_id("entry-1").get_by_test_id("btn-accept").bounding_box()
        assert first["y"] + first["height"] < 900, first                              # its Accept is on the first screen
        visible = [bx for bx in boxes if bx[0] + bx[1] <= 900]
        assert len(visible) >= 2, boxes                                               # T-149: the case overview block (about 120 px) now sits above the first entry; it was 3 rows before it
        for top, h, state in boxes:
            assert h <= (200 if state == "needs_review" else 175), boxes   # T-166 F3: the whole quote and the whole reason are shown, so a row is a little taller
    finally:
        b.close()


def test_row_opens_with_more_and_closes_with_less(page, sample_case):
    open_case(page, sample_case); row = page.get_by_test_id("entry-1"); t = row.get_by_test_id("entry-toggle")
    h0 = row.bounding_box()["height"]
    expect(t).to_have_attribute("aria-expanded", "false"); t.click(); expect(t).to_have_attribute("aria-expanded", "true")
    assert "is-open" in row.get_attribute("class")
    t.click(); expect(t).to_have_attribute("aria-expanded", "false"); assert abs(row.bounding_box()["height"] - h0) < 2


def test_390_needs_review_row_is_at_most_420(pw, lib09):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 390, "height": 800}).new_page(); open_case(pg, lib09)
    try:
        hs = pg.locator('[data-testid=queue] > article[data-state=needs_review]').evaluate_all("els => els.map(e => e.getBoundingClientRect().height)")
        assert hs and max(hs) <= 420, hs
        assert pg.evaluate("document.documentElement.scrollWidth") <= 391
    finally:
        b.close()


# ---- 5. decided rows show a state, not a filled Accept
def test_accepted_row_has_no_filled_accept_and_undo_returns(page, sample_case):
    open_case(page, sample_case); row = page.get_by_test_id("entry-1")
    acc = row.get_by_test_id("btn-accept"); expect(acc).to_have_class(re.compile(r"btn--primary"))
    acc.click(); expect(row).to_have_attribute("data-review", "accepted")
    acc = row.get_by_test_id("btn-accept")
    assert "btn--primary" not in acc.get_attribute("class") and acc.inner_text().strip().startswith("Accepted")
    assert page.locator("[data-testid=entry-1] .btn--primary:visible").count() == 0
    row.get_by_test_id("btn-reset").click(); expect(row).to_have_attribute("data-review", "pending")
    expect(row.get_by_test_id("btn-accept")).to_have_class(re.compile(r"btn--primary"))


def test_dismissed_row_keeps_no_filled_accept(page, sample_case):
    open_case(page, sample_case); row = page.get_by_test_id("entry-2")
    row.get_by_test_id("btn-dismiss").click(); expect(row).to_have_attribute("data-review", "dismissed")
    assert row.get_by_test_id("btn-accept").count() == 0     # T-060 r5 (paralegal M1): a dismissed row keeps Undo, not Accept
    assert row.get_by_test_id("btn-dismiss").inner_text().strip().startswith("Dismissed")
    assert row.get_by_test_id("btn-reset").inner_text().strip() == "Undo"


# ---- 6. accessibility
def test_320_reflow_with_case_checks_open(pw, sample_case):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 320, "height": 640}).new_page(); open_case(pg, sample_case)
    try:
        pg.get_by_test_id("case-summary").click()
        pg.get_by_test_id("case-step").first.wait_for()
        pg.get_by_test_id("judge-summary").click()
        assert pg.evaluate("document.documentElement.scrollWidth") == 320
        assert pg.evaluate("[...document.querySelectorAll('.zs-chip')].filter(c => c.getBoundingClientRect().right > 320.5).length") == 0
    finally:
        b.close()


def test_theme_toggle_name_follows_the_visible_state(page, sample_case):
    open_case(page, sample_case); t = page.get_by_test_id("btn-theme")
    seen = []
    for _ in range(3):
        t.click()
        vis = t.inner_text().strip(); name = t.get_attribute("aria-label")
        assert vis.lower() in name.lower(), (vis, name)                              # label in name (2.5.3)
        seen.append(vis)
    assert len(set(seen)) == 3, seen


def test_file_input_focus_shows_a_ring_on_the_upload_control(page):
    page.goto(BASE); page.get_by_test_id("btn-analyze").wait_for()
    page.get_by_test_id("file-input").focus()
    page.keyboard.press("Shift+Tab"); page.keyboard.press("Tab")
    assert active(page)["tid"] == "file-input"
    ring = page.evaluate("getComputedStyle(document.querySelector('label[for=file]')).outlineStyle")
    assert ring != "none"


def test_skip_link_hrefs_resolve_to_elements(page, sample_case):
    open_case(page, sample_case)
    bad = page.evaluate("[...document.querySelectorAll('#skip-nav a')].filter(a => !document.getElementById(a.getAttribute('href').slice(1))).map(a => a.getAttribute('href'))")
    assert bad == []


# ---- 7. held rechecks
def test_t096_dates_skip_link_reaches_the_date_choice(page, lib09):
    """T-096 minors: the skip link to Dates to confirm exists and Enter lands on a date control (Tab, Enter)."""
    open_case(page, lib09)
    page.evaluate("document.activeElement && document.activeElement.blur()")
    tab_until(page, "skip-dates", 4)
    page.keyboard.press("Enter")
    assert page.evaluate("!!document.activeElement.closest('[data-testid=dates-to-confirm]')")


def test_start_review_button_moves_focus_to_the_first_item(page, sample_case):
    open_case(page, sample_case)
    page.get_by_test_id("btn-start-review").click()
    assert page.evaluate("!!document.activeElement.closest('[data-item-id]')")


def test_t114_gap_change_notice_renders_after_a_date_confirm(page, lib09):
    """T-114: confirm_date answers gap_changes[]; the sentence shows above the timeline and is announced."""
    open_case(page, lib09)
    box = page.get_by_test_id("dates-to-confirm")
    # pick the reading the paste does not suggest, so a gap figure moves (lib09 record 4: 42 days -> 40)
    radios = box.get_by_test_id("confirm-date")
    n = radios.count()
    assert n >= 2
    target = None
    for i in range(n):
        if radios.nth(i).get_attribute("data-date") == "2026-03-05":
            target = radios.nth(i)
    assert target is not None
    target.check()
    box.get_by_test_id("btn-confirm-date").first.click()
    note = page.get_by_test_id("gap-change-note")
    expect(note).to_be_visible(timeout=10000)
    expect(note).to_contain_text(re.compile(r"Gap recalculated"))
    assert not BAD_TEXT.search(note.inner_text())


# ---- 8. export view
def test_export_letter_box_fits_its_text_and_can_be_downloaded(page, sample_case):
    tok = sample_case
    ids = [e["id"] for e in api("GET", f"/api/cases/{tok}")[1]["entries"] if e["state"] == "verified" and e["date"]]
    api("POST", f"/api/cases/{tok}/review/batch", {"action": "accept", "item_ids": ids})
    open_case(page, tok); page.get_by_test_id("btn-export").click()
    box = page.get_by_test_id("export-letter"); expect(box).to_be_visible()
    assert page.evaluate("(() => { const e = document.querySelector('[data-testid=export-letter]'); return e.scrollHeight <= e.clientHeight + 1; })()")
    assert page.get_by_test_id("btn-download-letter").count() == 1 and page.get_by_test_id("btn-download-notes").count() == 1
    if page.get_by_test_id("btn-download-letter").is_enabled():
        with page.expect_download() as dl:
            page.get_by_test_id("btn-download-letter").click()
            if page.get_by_test_id("copy-confirm").count():
                page.get_by_test_id("btn-copy-anyway").click()
        assert dl.value.suggested_filename.endswith(".txt")
        text = open(dl.value.path(), encoding="utf-8").read()
        assert text.startswith("TREATMENT CHRONOLOGY")
