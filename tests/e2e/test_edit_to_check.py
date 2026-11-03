"""T-136 (frontend; backend T-134, D-045b, D-051): the UI reads the item's own `edit_to_check` and the review's `counts.edit_to_check`, not a summary-only guess.
An edit made with the quote picker (excerpt only, no edited summary) on an entry that is still Needs review is open: its Accept reads "I compared it with the quote", the header,
the Open-decisions strip and the copy-confirm count it, the export stepper shows the gate warning EDIT_NOT_CONFIRMED in its plain reason, and the Accept clears all of it.
Real backend; needs ZLAYT_DB (the SQLite file of the server under test) to put the entry into Needs review the way a missing second check does (the fixture set verifies every entry).
No new test ids: btn-edit-excerpt, excerpt-unit, btn-save-excerpt, btn-accept, edit-check-hint, todo-list, need-review-count, case-next-action, copy-confirm, gate-warning,
btn-gate-warning-jump (all declared in conftest). New (declared in conftest): edit-compare-prompt, dismissed-group-flags / dismissed-group-amounts, dismissed-summary-flags / dismissed-summary-amounts,
dismissed-flags, dismissed-amounts."""
import os
import re
import sys
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, needs_db, reveal
from tests.e2e.test_stepper import open_rail

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RAW_CODE = re.compile(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b")


def _case(tok):
    return api("GET", f"/api/cases/{tok}")[1]


def _needs_review_entry_with_picker(tok):
    """Put a dated, pending entry whose record has several sentences into Needs review (store write, like a missing second check) and return it."""
    path = needs_db()
    c = _case(tok); recs = {r["id"]: r for r in c["records"]}
    e = next(x for x in c["entries"] if x["id"] != "e1" and x["state"] == "verified" and x["date"] and x["review_status"] == "pending" and len(x["record_ids"]) == 1
             and len([s for s in recs[x["record_ids"][0]]["sentences"] if s["start"] >= x["excerpt_start"] and s["end"] <= x["excerpt_end"]]) >= 2)
    sys.path.insert(0, ROOT)
    from app.db import db as DB
    conn = DB.connect(path)
    try:
        DB.update_item(conn, e["id"], now=9e9, case=tok, state="needs_review")
    finally:
        conn.close()
    return e


def _progress(page):
    t = page.locator("#progress-text").inner_text()
    m = re.match(r"(\d+) of (\d+) decided", t)
    assert m, t
    pt = page.locator("#progress-text")   # T-166 F2: the visible line is short ('4 of 23 decided · 3 to review'); the counts are data attributes
    return int(m.group(1)), int(m.group(2)), int(pt.get_attribute("data-needs") or 0), int(pt.get_attribute("data-edits") or 0)


def _row(page, eid):
    return page.locator(f'[data-testid=queue] [data-item-id="{eid}"], [data-testid=timeline] [data-item-id="{eid}"]').first


def _quote_edit(row):
    """Use the quote picker the way a paralegal does: Change quote, drop the last chosen sentence, Use these sentences. No summary is edited."""
    reveal(row.get_by_test_id("btn-edit-excerpt")).click()
    ed = row.get_by_test_id("excerpt-editor"); expect(ed).to_be_visible()
    units = ed.get_by_test_id("excerpt-unit")
    last = max(i for i in range(units.count()) if units.nth(i).is_checked())
    units.nth(last).click()
    ed.get_by_test_id("btn-save-excerpt").click()


@pytest.fixture
def edited_quote(page, sample_case):
    e = _needs_review_entry_with_picker(sample_case)
    open_case(page, sample_case)
    row = _row(page, e["id"]); row.scroll_into_view_if_needed()
    before = _progress(page)
    _quote_edit(row)
    expect(row).to_have_attribute("data-review", "edited")
    return {"tok": sample_case, "id": e["id"], "before": before, "orig": e["excerpt"]}


def _accept_something_else(t):
    assert api("POST", f"/api/cases/{t['tok']}/items/e1/review", {"action": "accept"})[0] == 200      # the letter has one entry, so the gate is ready with a warning


def test_a_quote_only_edit_is_open_and_offers_the_compare_accept(page, edited_quote):
    t = edited_quote; row = _row(page, t["id"])
    got = next(x for x in _case(t["tok"])["entries"] if x["id"] == t["id"])
    assert got["excerpt"] != t["orig"] and got["edit_to_check"] is True and not (got.get("edited") or {}).get("summary"), "the setup is a quote-only edit"
    assert row.get_attribute("data-edit-check") is not None
    ok = row.get_by_test_id("btn-accept"); expect(ok).to_contain_text("I compared it with the quote"); assert "btn--primary" in ok.get_attribute("class")
    hint = row.get_by_test_id("edit-check-hint"); expect(hint).to_be_visible()
    assert "quote" in hint.inner_text().lower() and not RAW_CODE.search(hint.inner_text())


def test_header_and_strip_use_the_servers_edit_count(page, edited_quote):
    t = edited_quote
    server = _case(t["tok"])["review"]["counts"]["edit_to_check"]; assert server == 1
    d0, _, n0, _ = t["before"]
    d1, _, n1, k1 = _progress(page)
    assert d1 == d0, "an edit that is still Needs review was counted as decided"
    assert k1 == server and n1 >= 1, (n1, k1)
    assert re.search(rf"{server} edit to check", page.get_by_test_id("todo-list").inner_text())
    assert page.get_by_test_id("need-review-count").inner_text().startswith(str(n1))


def test_the_export_stepper_shows_the_gate_warning_in_plain_words(page, edited_quote):
    t = edited_quote; _accept_something_else(t)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    cs = open_rail(page)
    gate = cs.locator('[data-step-id="export_gate"]'); expect(gate).to_have_attribute("data-status", "pass")
    w = gate.locator('[data-warning-code="EDIT_NOT_CONFIRMED"]'); expect(w).to_have_count(1)
    txt = w.inner_text().lower()
    assert "not in the letter" in txt and "quote" in txt and "does not block" in txt, txt
    assert not RAW_CODE.search(w.inner_text()), txt
    w.get_by_test_id("btn-gate-warning-jump").click()
    assert page.evaluate("(() => { const r = document.activeElement.closest('[data-item-id]'); return !!r && r.hasAttribute('data-edit-check'); })()"), "the jump lands on the edit to check"


def test_the_next_step_names_the_edit_not_a_pending_item(page, edited_quote):
    t = edited_quote; c = _case(t["tok"])
    for it in c["entries"] + c["amounts"] + c["flags"]:                        # decide everything else, so only the edit waits
        if it["id"] != t["id"] and it["review_status"] == "pending" and it["state"] != "rejected":
            api("POST", f"/api/cases/{t['tok']}/items/{it['id']}/review", {"action": "dismiss"})
    def settled_judges(route):      # the store write that put the entry into Needs review also leaves its second check unrun: show that step as passed so the review step is the one waiting on her
        d = route.fetch().json()
        for st in d.get("steps", []):
            if st["id"] == "judges":
                st.update(status="pass", next_action=None, counts=dict(st.get("counts") or {}, unavailable=0), reason_code=None)
        route.fulfill(json=d)
    page.route(re.compile(r"/api/cases/[^/]+/trace$"), settled_judges)
    def settled_next(route):        # T-149 r2: the server's next_action would still name the unrun second check; with the judges shown as settled it names nothing, and the case rail says what to do
        d = route.fetch().json()
        if isinstance(d, dict) and "cases" in d:
            for c in d["cases"]:
                c["next_action"] = None
        elif isinstance(d, dict):
            d["next_action"] = None
        route.fulfill(json=d)
    page.route(re.compile(r"/api/cases(/[^/]+)?$"), lambda r: settled_next(r) if r.request.method == "GET" else r.continue_())
    page.reload(); page.get_by_test_id("timeline").wait_for()
    nxt = page.get_by_test_id("case-next-action"); expect(nxt).to_be_visible()
    txt = nxt.inner_text().lower()
    assert "0 pending" not in txt and "edit" in txt and "quote" in txt, txt


def test_the_edit_is_named_before_the_letter_is_copied(page, edited_quote):
    t = edited_quote; _accept_something_else(t)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    page.get_by_test_id("btn-export").click(); page.get_by_test_id("btn-copy-letter").click()
    expect(page.get_by_test_id("copy-confirm")).to_contain_text("1 edited entry still marked Needs review")


def test_comparing_it_with_the_quote_closes_everything(page, edited_quote):
    t = edited_quote; _accept_something_else(t)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"])
    d0, _, n0, k0 = _progress(page); assert k0 == 1
    row.get_by_test_id("btn-accept").click()
    expect(row).to_have_attribute("data-review", "accepted"); assert row.get_attribute("data-edit-check") is None
    d1, _, n1, k1 = _progress(page)
    assert d1 == d0 + 1 and k1 == 0 and n1 == n0 - 1, ((d0, n0, k0), (d1, n1, k1))
    assert _case(t["tok"])["review"]["counts"]["edit_to_check"] == 0
    assert "edit to check" not in page.get_by_test_id("todo-list").inner_text()
    page.reload(); page.get_by_test_id("timeline").wait_for()
    assert open_rail(page).locator('[data-warning-code="EDIT_NOT_CONFIRMED"]').count() == 0


# ---- paralegal pass 5 F1: one `a` never records the comparison
def test_one_a_press_does_not_record_the_comparison(page, edited_quote):
    t = edited_quote; _accept_something_else(t)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"]); d0, _, n0, k0 = _progress(page); assert k0 == 1
    row.focus(); page.keyboard.press("a"); page.wait_for_timeout(400)
    assert row.get_attribute("data-review") == "edited" and row.get_attribute("data-edit-check") is not None, "a recorded the comparison"
    assert next(x for x in _case(t["tok"])["entries"] if x["id"] == t["id"])["edit_to_check"] is True
    d1, _, n1, k1 = _progress(page); assert (d1, n1, k1) == (d0, n0, k0), "the header did not move"
    prompt = row.get_by_test_id("edit-compare-prompt"); expect(prompt).to_be_visible()
    assert "not recorded" in prompt.inner_text().lower() and "i compared it with the quote" in prompt.inner_text().lower()
    assert page.evaluate("document.activeElement.getAttribute('data-testid')") == "btn-accept", "focus is on the confirm button"
    page.get_by_test_id("btn-export").click(); page.get_by_test_id("btn-copy-letter").click()
    expect(page.get_by_test_id("copy-confirm")).to_contain_text("1 edited entry still marked Needs review")      # the copy warning is still there
    page.get_by_test_id("btn-copy-cancel").click()


def test_enter_on_the_focused_confirm_button_records_it(page, edited_quote):
    t = edited_quote; _accept_something_else(t)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"]); row.focus(); page.keyboard.press("a")
    expect(row.get_by_test_id("edit-compare-prompt")).to_be_visible()
    page.keyboard.press("Enter")
    expect(row).to_have_attribute("data-review", "accepted"); assert row.get_attribute("data-edit-check") is None
    assert _case(t["tok"])["review"]["counts"]["edit_to_check"] == 0


def test_start_review_then_a_does_not_confirm_either(page, edited_quote):
    t = edited_quote
    page.reload(); page.get_by_test_id("timeline").wait_for()
    page.get_by_test_id("btn-start-review").click()
    page.keyboard.press("a"); page.wait_for_timeout(400)
    after = next(x for x in _case(t["tok"])["entries"] if x["id"] == t["id"])
    assert after["edit_to_check"] is True and after["review_status"] == "edited", "Start review then a confirmed the edit"


# ---- paralegal pass 5 F2: dismissed flags and amounts wait under Dismissed (n)
def test_dismissed_flags_and_amounts_wait_under_dismissed_n(page, sample_case):
    c = _case(sample_case)
    flag = next(f for f in c["flags"] if f["state"] != "rejected"); amt = next(a for a in c["amounts"] if a["state"] != "rejected")
    open_case(page, sample_case)
    fp, cp = page.get_by_test_id("flags-panel"), page.get_by_test_id("charges-panel")
    n_open_flags = fp.locator("[data-item-id]").count(); n_open_amts = cp.locator("[data-item-id]").count()
    fp.locator(f'[data-item-id="{flag["id"]}"]').get_by_test_id("btn-dismiss").click()
    cp.locator(f'[data-item-id="{amt["id"]}"]').get_by_test_id("btn-dismiss").click()
    g = fp.get_by_test_id("dismissed-group-flags"); expect(g.get_by_test_id("dismissed-summary-flags")).to_have_text(re.compile(r"^Dismissed \(1\)"))
    a = cp.get_by_test_id("dismissed-group-amounts"); expect(a.get_by_test_id("dismissed-summary-amounts")).to_have_text(re.compile(r"^Dismissed \(1\)"))
    assert g.locator(f'[data-item-id="{flag["id"]}"]').count() == 1 and fp.locator(f'[data-group] [data-item-id="{flag["id"]}"]').count() == 0, "not in the open list"
    assert a.locator(f'[data-item-id="{amt["id"]}"]').count() == 1 and cp.locator(f'[data-group] [data-item-id="{amt["id"]}"]').count() == 0
    assert fp.locator("[data-item-id]").count() == n_open_flags and cp.locator("[data-item-id]").count() == n_open_amts, "rows moved, none lost"
    d0 = _progress(page)
    for grp, iid in ((g, flag["id"]), (a, amt["id"])):
        r = grp.locator(f'[data-item-id="{iid}"]'); expect(r).to_have_attribute("data-review", "dismissed")
        assert r.get_by_test_id("btn-accept").count() == 0
        r.focus(); page.keyboard.press("a"); page.wait_for_timeout(250)
        expect(r).to_have_attribute("data-review", "dismissed")
    assert _progress(page) == d0
    g.locator(f'[data-item-id="{flag["id"]}"]').get_by_test_id("btn-reset").click()                     # Undo brings it back to the open list
    expect(fp.locator(f'[data-group] [data-item-id="{flag["id"]}"]')).to_have_count(1)
    expect(fp.get_by_test_id("dismissed-group-flags")).to_have_count(0)


# ================= round 2 (paralegal re-check + staff review of 671f054) =================
def _stub_edit_count(page, n):
    """Make GET .../cases/<token> report review.counts.edit_to_check = n while the items still say one edit: the UI must follow the SERVER's count (api.md, T-134), not recount the items."""
    def fn(route):
        d = route.fetch().json(); d["review"]["counts"]["edit_to_check"] = n; route.fulfill(json=d)
    page.route(re.compile(r"/api/cases/[^/?]+$"), fn)
    page.route(re.compile(r"/api/cases/[^/]+/items/[^/]+/review$"), fn)


def test_header_strip_and_copy_warning_follow_the_servers_count_not_a_recount(page, sample_case):
    """Mutation guard (staff review F2): ZL.editCount ignoring review.counts.edit_to_check must fail this test."""
    _stub_edit_count(page, 3)
    e = _needs_review_entry_with_picker(sample_case)
    open_case(page, sample_case)
    row = _row(page, e["id"]); row.scroll_into_view_if_needed(); _quote_edit(row)
    expect(row).to_have_attribute("data-review", "edited")
    assert sum(1 for x in _case(sample_case)["entries"] if x.get("edit_to_check")) == 1, "the items still say one edit"
    assert _progress(page)[3] == 3, "the header shows the server's count"
    assert "3 edits to check" in page.get_by_test_id("todo-list").inner_text()
    _accept_something_else({"tok": sample_case})
    page.reload(); page.get_by_test_id("timeline").wait_for()
    assert _progress(page)[3] == 3
    page.get_by_test_id("btn-export").click(); page.get_by_test_id("btn-copy-letter").click()
    expect(page.get_by_test_id("copy-confirm")).to_contain_text("3 edited entries still marked Needs review")


def test_a_second_a_press_does_not_record_the_comparison_either(page, edited_quote):
    """Mutation guard (staff review F3): 'ask first, then do it on the next press' is not allowed. Key auto-repeat on a held a must not record a statement she has not made."""
    t = edited_quote; _accept_something_else(t)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"]); d0, _, n0, k0 = _progress(page); assert k0 == 1
    row.focus(); page.keyboard.press("a"); page.keyboard.press("a"); page.keyboard.press("a"); page.wait_for_timeout(500)
    assert next(x for x in _case(t["tok"])["entries"] if x["id"] == t["id"])["edit_to_check"] is True, "a second a recorded the comparison"
    assert row.get_attribute("data-review") == "edited" and row.get_attribute("data-edit-check") is not None
    assert _progress(page)[:1] + _progress(page)[2:] == (d0, n0, k0)
    assert page.evaluate("document.activeElement.getAttribute('data-testid')") == "btn-accept"
    expect(row.get_by_test_id("edit-compare-prompt")).to_be_visible()


def test_after_the_comparison_the_row_does_not_read_needs_review(page, edited_quote):
    """Paralegal F-1 (major): 'Needs review' beside 'Accepted' contradicts her decision. The machine chip says she compared it; the reason line says the second AI check did not run."""
    t = edited_quote; _accept_something_else(t)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"]); d0, _, n0, k0 = _progress(page)
    expect(row.get_by_test_id("entry-state")).to_have_text("Needs review")                 # before: still open, so it says so
    row.get_by_test_id("btn-accept").click()
    expect(row).to_have_attribute("data-review", "accepted")
    chips = row.locator(".entry-chips").inner_text()
    assert "Needs review" not in chips and "Accepted" in chips and "Compared by you" in chips, chips
    why = row.get_by_test_id("entry-reasons").inner_text()
    assert "Compared by you" in why and "second AI check" in why and "Needs review" not in why, why
    d1, _, n1, k1 = _progress(page); assert (d1, n1, k1) == (d0 + 1, n0 - 1, 0), "the header agrees"
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"]); assert "Needs review" not in row.locator(".entry-chips").inner_text(), "still true after a reload"
    assert not RAW_CODE.search(row.inner_text())


def test_a_dismissed_or_never_compared_entry_keeps_its_machine_chip(page, sample_case):
    """The 'Compared by you' chip belongs to a compared edit only: an accepted item that was never edited keeps what the checks said."""
    c = _case(sample_case); e = next(x for x in c["entries"] if x["id"] != "e1" and x["state"] == "verified" and x["date"])
    open_case(page, sample_case); row = _row(page, e["id"])
    assert "Compared by you" not in row.locator(".entry-chips").inner_text()
    row.get_by_test_id("btn-accept").click(); expect(row).to_have_attribute("data-review", "accepted")
    assert "Compared by you" not in row.locator(".entry-chips").inner_text() and "Quote matches" in row.locator(".entry-chips").inner_text()


def test_a_re_picked_quote_under_the_ai_summary_says_so_and_offers_to_write_the_summary(page, edited_quote):
    """D-058 / paralegal F-2 (major): a re-picked quote keeps the AI summary, and its second AI check has no answer on the new quote, so accepting alone does not put it in the letter.
    The row hint, the key prompt and the gate warning say so BEFORE she accepts (the server's words); AFTER she accepts, the row offers the action that clears the gate: Write the summary
    (not a rerun that cannot clear it). No text may say the comparison puts the entry in the letter."""
    t = edited_quote; _accept_something_else(t)
    got = next(x for x in _case(t["tok"])["entries"] if x["id"] == t["id"])
    assert got["ai_drafted"] and "JUDGE_UNAVAILABLE" in got["reasons"] and "summary" not in (got.get("edited") or {}), "the setup: an AI draft, quote re-picked, second check never answered"
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"])
    # the server's own item-step sentence is the one on the row (not a page-written copy). The page paints a fallback first and swaps the server's sentence in when it arrives,
    # so wait for the server's words before reading the row: with a prepared answer (D-065 / D-069) they say "second check", with a recorded live answer "second AI check"
    why = next(s for s in api("GET", f"/api/cases/{t['tok']}/items/{t['id']}/trace")[1]["steps"] if s["id"] == "human")["why"]
    expect(row.get_by_test_id("edit-check-hint")).to_contain_text(why)
    hint = row.get_by_test_id("edit-check-hint").inner_text().lower()
    assert "stays blocked" not in hint, hint                      # T-134 r4b: the gate passes before she accepts, so the card never says the export is blocked now
    assert re.search(r"second (ai )?check", hint) and "edit the summary" in hint and "if you accept it" in hint, hint
    assert not re.search(r"\b(goes?|put|puts|added|adds) (in|into|to) the letter", hint), hint
    assert "accepting alone" in hint, hint
    row.focus(); page.keyboard.press("a")
    expect(row.get_by_test_id("edit-compare-prompt")).to_contain_text(why)
    pr = row.get_by_test_id("edit-compare-prompt").inner_text().lower()
    assert "stays blocked" not in pr and "will be blocked" in pr and re.search(r"second (ai )?check", pr) and "not recorded yet" in pr, pr
    w = open_rail(page).locator('[data-warning-code="EDIT_NOT_CONFIRMED"]'); expect(w).to_have_count(1)
    wt = w.inner_text().lower()
    assert "accepting alone will not put" in wt and "your own words" in wt and "does not block" in wt, wt      # the backend's sentence (T-134 r3/r4, D-058), shown as given
    expect(row.get_by_test_id("edit-check-hint")).to_contain_text(why)                           # as given, whatever its words
    # after the comparison: the row names the blocker and offers the matching action
    row = _row(page, t["id"]); row.get_by_test_id("btn-accept").click(); expect(row).to_have_attribute("data-review", "accepted")
    note = row.get_by_test_id("compare-export-note"); expect(note).to_be_visible()
    nt = note.inner_text().lower(); assert "blocked" in nt and re.search(r"second (ai )?check", nt), nt
    assert note.get_by_test_id("btn-rerun-judge").count() == 0, "a rerun is not the action that clears this"
    note.get_by_test_id("btn-write-summary").click()
    expect(row.get_by_test_id("edit-summary")).to_be_visible()
    page.reload(); page.get_by_test_id("timeline").wait_for()
    expect(_row(page, t["id"]).get_by_test_id("compare-export-note")).to_be_visible()          # derived from the item, not from this page's memory
    # the gate's blocker row offers the same action
    cs = open_rail(page); b = cs.locator('[data-testid="gate-blocker"][data-blocker-code="JUDGE_NOT_RUN"]').first
    expect(b.get_by_test_id("btn-gate-write-summary")).to_be_visible()


def test_a_reworded_summary_does_not_claim_the_export_is_blocked(page, sample_case):
    """D-045(b): her own summary wording is exempt from the second check, so nothing on the row says the export is blocked."""
    e = _needs_review_entry_with_picker(sample_case)
    open_case(page, sample_case); row = _row(page, e["id"]); row.scroll_into_view_if_needed()
    row.get_by_test_id("btn-edit").click()
    row.get_by_test_id("edit-summary").fill(e["summary"].rstrip(".") + " (as recorded).")
    row.get_by_test_id("btn-save-edit").click()
    page.wait_for_timeout(800)
    got = next(x for x in _case(sample_case)["entries"] if x["id"] == e["id"])
    assert got.get("edit_to_check") and (got.get("edited") or {}).get("summary"), "the setup: a reworded summary still waiting for her comparison"
    ctl = _row(page, e["id"]).locator(".rv-controls").inner_text().lower()
    assert "blocked" not in ctl and "write the summary" not in ctl, ctl
    assert _row(page, e["id"]).get_by_test_id("btn-write-summary").count() == 0


def test_a_quote_only_edit_never_prints_undefined_and_shows_the_original(page, edited_quote):
    """Paralegal F-4: 'Original: undefined' on the row. A quote-only edit says the quote changed and shows the original excerpt."""
    t = edited_quote; row = _row(page, t["id"])
    note = row.get_by_test_id("edited-note"); expect(note).to_be_visible()
    txt = note.inner_text()
    assert "undefined" not in txt and "Quote changed by you" in txt and t["orig"][:40] in txt, txt


def test_the_copy_warning_names_the_record(page, edited_quote):
    """Paralegal F-5: the warning says which entry is still open ('Record 3, <provider>'), so she can go back to it."""
    t = edited_quote; _accept_something_else(t)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    c = _case(t["tok"]); e = next(x for x in c["entries"] if x["id"] == t["id"]); rec = next(r for r in c["records"] if r["id"] == e["record_ids"][0])
    page.get_by_test_id("btn-export").click(); page.get_by_test_id("btn-copy-letter").click()
    txt = page.get_by_test_id("copy-confirm").inner_text()
    assert f"Record {rec['seq']}" in txt and e["provider"] in txt, txt
