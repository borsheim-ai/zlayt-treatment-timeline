"""T-060 round 4 (frontend) + T-114 r3: the gap-change line that survives a reload, readable library titles, dismissed rows leave the queue, the edit re-check
notice and the typed-dollar 422 message, the AI-check row for a flag the checks left out, the doubled no-sentences copy, and the cheap accessibility fixes.
New test ids (QA adds them to the tests/e2e/conftest.py docstring): gap-change-card, gap-change-removed, dismissed-group, dismissed-summary, dismissed-queue, edit-recheck-hint,
edit-recheck-note, edit-original. Library cases need ZLAYT_MODE=local; the fixture backend replays recorded answers."""
import json
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


def _lib(lib_id):
    st, c = api("POST", "/api/cases", {"library": lib_id})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    _run(c["token"])
    return c["token"]


@pytest.fixture
def lib09():
    tok = _lib("case_lib09_spanish_interpreter_espalda")
    yield tok
    api("DELETE", f"/api/cases/{tok}")


@pytest.fixture
def lib06():
    tok = _lib("case_lib06_lop_billed_vs_adjusted")
    yield tok
    api("DELETE", f"/api/cases/{tok}")


def _confirm_record4_as_march_5(page):
    box = page.get_by_test_id("dates-to-confirm")
    radios = box.get_by_test_id("confirm-date")
    target = None
    for i in range(radios.count()):
        if radios.nth(i).get_attribute("data-date") == "2026-03-05":
            target = radios.nth(i)
    assert target is not None
    target.check()
    box.get_by_test_id("btn-confirm-date").first.click()


# ---- T-114 major: the gap-change line is on the gap card and survives Got it and a reload
def test_t114_gap_change_stays_on_the_gap_card_after_got_it_and_reload(page, lib09):
    open_case(page, lib09)
    gap = page.locator('[data-testid=flags-panel] [data-flag-type=gap]').first
    assert "was 42" not in gap.inner_text()                       # before the confirm there is nothing to explain
    _confirm_record4_as_march_5(page)
    note = page.get_by_test_id("gap-change-note"); expect(note).to_be_visible(timeout=10000)
    card = page.get_by_test_id("gap-change-card"); expect(card).to_have_count(1)
    expect(card).to_contain_text("now 40 days (was 42)")
    expect(card).to_contain_text("March 5, 2026"); expect(card).to_contain_text("March 3, 2026"); expect(card).to_contain_text("April 14, 2026")
    assert page.locator('[data-testid=flags-panel] [data-flag-type=gap]').first.get_by_test_id("gap-change-card").count() == 1   # it sits on the gap card, not elsewhere
    page.get_by_test_id("btn-dismiss-gap-note").click(); expect(note).to_have_count(0)
    expect(page.get_by_test_id("gap-change-card")).to_contain_text("now 40 days (was 42)")      # Got it removes the announcement, not the card line
    page.reload(); page.get_by_test_id("timeline").wait_for(timeout=15000)
    assert page.get_by_test_id("gap-change-note").count() == 0
    card = page.get_by_test_id("gap-change-card"); expect(card).to_have_count(1)
    expect(card).to_contain_text("now 40 days (was 42)"); expect(card).to_contain_text("March 5, 2026")
    assert not BAD_TEXT.search(card.inner_text())


def test_t114_gap_change_line_is_not_shown_on_a_case_that_never_changed(page, lib09):
    open_case(page, lib09)
    assert page.get_by_test_id("gap-change-card").count() == 0 and page.get_by_test_id("gap-change-removed").count() == 0


def test_t114_accepted_rate_row_reads_one_status_chip(page, sample_case):
    open_case(page, sample_case)
    row = page.locator('tr[data-amount-kind=rate]').first
    row.get_by_test_id("btn-accept").click()
    expect(row).to_have_attribute("data-review", "accepted")
    txt = row.inner_text()
    assert "Needs review" not in txt and "Accepted" in txt, txt
    assert row.locator("[data-chip]").count() == 1


# ---- T-060 r4: library cases show readable titles
def test_library_case_header_and_buttons_show_titles_not_file_slugs(page, lib09):
    open_case(page, lib09)
    name = page.get_by_test_id("case-name").inner_text()
    assert "lib09" not in name and not name.lower().startswith("case ") and "_" not in name, name
    assert "lib09" not in page.title()
    page.get_by_test_id("btn-all-cases").click()                      # T-174 F16: the synthetic-case card belongs to the overview
    page.locator("details.cs-details > summary").click()
    labels = page.locator('[data-testid^="library-"]').all_inner_texts()
    assert labels and not any(re.search(r"\blib\d+\b|^Add:", t) for t in labels), labels
    assert not any(t.strip().startswith("L1 ·") for t in labels)


# ---- T-060 r4: a dismissed entry leaves the queue and waits in the Dismissed group
def test_dismissed_entry_leaves_the_queue_for_the_dismissed_group_and_undo_returns_it(page, sample_case):
    open_case(page, sample_case)
    row = page.get_by_test_id("entry-2")
    row.get_by_test_id("btn-dismiss").click()
    group = page.get_by_test_id("dismissed-group"); expect(group).to_have_count(1)
    expect(page.get_by_test_id("dismissed-summary")).to_contain_text("Dismissed (1)")
    assert page.locator('[data-testid=queue] [data-testid=entry-2]').count() == 0
    assert page.locator('[data-testid=dismissed-queue] [data-testid=entry-2]').count() == 1
    dis = page.get_by_test_id("entry-2"); expect(dis).to_be_visible()          # opened for the entry just dismissed, so Undo is in reach
    assert page.evaluate("getComputedStyle(document.querySelector('[data-testid=entry-2] [data-testid=entry-excerpt]')).textDecorationLine") == "none"   # the record's own quote is never struck through
    dis.get_by_test_id("btn-reset").click()
    expect(page.locator('[data-testid=queue] [data-testid=entry-2]')).to_have_count(1)
    expect(page.get_by_test_id("dismissed-group")).to_have_count(0)


def test_dismissed_group_is_collapsed_after_a_reload(page, sample_case):
    tok = sample_case
    e = api("GET", f"/api/cases/{tok}")[1]["entries"][1]["id"]
    assert api("POST", f"/api/cases/{tok}/items/{e}/review", {"action": "dismiss"})[0] == 200
    open_case(page, tok)
    expect(page.get_by_test_id("dismissed-summary")).to_contain_text("Dismissed (1)")
    assert page.get_by_test_id("dismissed-group").get_attribute("open") is None
    assert page.locator(f'[data-testid=queue] [data-item-id="{e}"]').count() == 0
    page.get_by_test_id("dismissed-summary").click()
    expect(page.locator(f'[data-testid=dismissed-queue] [data-item-id="{e}"]')).to_be_visible()


# ---- AC5: the re-check line on edit, and the 422 message in the paralegal's own dollars
def _open_edit(page, n=1):
    row = page.get_by_test_id(f"entry-{n}"); row.get_by_test_id("btn-edit").click()
    return row


def test_edit_box_says_the_wording_is_re_checked_and_a_saved_edit_reports_it(page, sample_case):
    open_case(page, sample_case)
    row = _open_edit(page, 1)
    hint = row.get_by_test_id("edit-recheck-hint"); expect(hint).to_be_visible()
    assert "checks every number, date and negation" in hint.inner_text()
    ta = row.get_by_test_id("edit-summary"); old = ta.input_value()
    ta.fill(old.rstrip(".") + ".")                                  # same words: nothing new to refuse
    row.get_by_test_id("btn-save-edit").click()
    expect(row).to_have_attribute("data-review", "edited")
    note = page.get_by_test_id("entry-1").get_by_test_id("edit-recheck-note"); expect(note).to_be_visible()
    assert "re-checked" in note.inner_text() and not BAD_TEXT.search(note.inner_text())
    page.get_by_test_id("entry-1").get_by_test_id("btn-reset").click()
    page.get_by_test_id("entry-1").get_by_test_id("btn-discard-edit").click()                         # T-166 F12: Undo on an edited row asks first
    expect(page.get_by_test_id("entry-1").get_by_test_id("edit-recheck-note")).to_have_count(0)     # the note ends with the decision


def test_refused_dollar_figure_is_shown_as_typed(page, sample_case):
    open_case(page, sample_case)
    row = _open_edit(page, 5)
    ta = row.get_by_test_id("edit-summary"); ta.fill(ta.input_value().rstrip(".") + ", billed $9,000.")
    row.get_by_test_id("btn-save-edit").click()
    err = row.locator(".rv-error"); expect(err).to_contain_text("$9,000", timeout=10000)
    assert not re.search(r"(?<![\d$,])9000", err.inner_text()), err.inner_text()
    assert "$9,000" in row.get_by_test_id("edit-summary").input_value()      # her text stays in the box


# ---- T-117 minor: the AI-check row for a flag the checks left out does not say "accept"
def test_ai_check_row_for_a_tray_flag_agrees_with_the_tray(page, lib06):
    open_case(page, lib06)
    tray = page.locator('[data-testid=tray-item][data-tray-kind=flag]')
    assert tray.count() >= 1
    expect(tray.first).to_contain_text("Nothing to accept here")
    tid = tray.first.get_attribute("data-item-id")
    page.get_by_test_id("judge-panel").locator("summary").first.click()
    row = page.locator(f'[data-testid=judge-panel] [data-target-item="{tid}"]').first
    if row.count() == 0:
        pytest.skip("the AI check did not list the tray flag in this fixture")
    txt = row.inner_text()
    assert not re.search(r"\baccept it\b|Your decision", txt, re.I), txt
    assert "Left out of the letter" in txt and "Nothing to accept here" in txt
    assert "See the steps" not in txt and "Why this status" in txt


# ---- T-096 minor: the no-sentences message is one sentence
def test_no_sentences_message_is_not_doubled(page, sample_case):
    tok = sample_case
    reason = "No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text. Read the record text instead."

    def rewrite(route):
        r = route.fetch(); body = r.json()
        gone = body["entries"][0]
        body["entries"] = [e for e in body["entries"] if e["id"] != gone["id"]]
        for rec in body["records"]:
            rec["sentences"] = []; rec["sentences_reason"] = reason
        route.fulfill(response=r, body=json.dumps(body))
    page.route(re.compile(rf"/api/cases/{re.escape(tok)}$"), rewrite)
    open_case(page, tok)
    page.get_by_test_id("btn-manual-entry").first.click()
    msg = page.get_by_test_id("manual-no-sentences").first
    expect(msg).to_be_visible()
    t = msg.inner_text()
    assert t.lower().count("no sentences") == 1 and "Why:" not in t, t


# ---- accessibility: label in name, the group's role, skip links that resolve in the export view, a visible focus on the Export heading
def test_row_toggle_name_contains_its_visible_word_in_both_states(page, sample_case):
    open_case(page, sample_case)
    t = page.get_by_test_id("entry-1").get_by_test_id("entry-toggle")
    assert t.get_attribute("aria-label").startswith("More")
    t.click(); assert t.inner_text() == "Less" and t.get_attribute("aria-label").startswith("Less") and t.get_attribute("aria-expanded") == "true"
    page.get_by_role("button", name=re.compile(r"^Less actions")).first.click()


def test_queue_has_a_role_that_allows_its_name(page, sample_case):
    open_case(page, sample_case)
    q = page.get_by_test_id("queue")
    assert q.get_attribute("role") == "group" and q.get_attribute("aria-labelledby") == "h-timeline"


def test_every_skip_link_resolves_in_the_review_and_in_the_export_view(page, sample_case):
    ids = [e["id"] for e in api("GET", f"/api/cases/{sample_case}")[1]["entries"] if e["state"] == "verified" and e["date"]]
    api("POST", f"/api/cases/{sample_case}/review/batch", {"action": "accept", "item_ids": ids})      # something accepted, so the export opens
    open_case(page, sample_case)
    def hrefs():
        return page.evaluate("[...document.querySelectorAll('[data-testid=skip-nav] a')].map(a => [a.getAttribute('href'), !!document.querySelector(a.getAttribute('href'))])")
    assert hrefs() and all(ok for _, ok in hrefs()), hrefs()
    page.get_by_test_id("btn-export").click(); expect(page.locator("#h-export")).to_be_focused()
    page.wait_for_timeout(400)
    assert all(ok for _, ok in hrefs()), hrefs()
    ring = page.evaluate("getComputedStyle(document.querySelector('#h-export')).outlineStyle")
    assert ring != "none", ring


def test_translation_caution_is_not_clipped_at_1440(pw, lib09):
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 1440, "height": 900}).new_page(); open_case(pg, lib09)
    try:
        cautions = pg.locator('[data-testid=queue] .reason--caution')
        assert cautions.count() >= 1
        assert cautions.evaluate_all("els => els.every(e => e.scrollWidth <= e.clientWidth + 1)")
    finally:
        b.close()
