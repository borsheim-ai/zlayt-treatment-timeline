"""T-181 (D-068) guided Step 2, "Check the timeline" (docs/GUIDED_UI_SPEC.md section 5). Real browser, the fixture backend (curated set), the real API: every case is made over the API and deleted afterwards.
What is guarded: one item at a time with the highlighted record beside it; Yes / No / Fix / Add a note / pick a date / could-not-check; Undo fully visible; version + expected_status on every write (T-178) and
the plain 409 message; the D-066 compare box (disabled until ticked, compared:true sent, a COMPARE_REQUIRED the page did not expect becomes the box); D-065 tags; no jargon; the keyboard (A, D, E, arrows);
the done screen and its link to step 3; nothing moves when she answers; the primary action is above the fold at 1440x900 and 1366x768; a phone shows enough of the record. Screenshots go to artifacts/screenshots/guided/."""
import json
import os
import re
import pytest
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided.test_shell_smoke import watch, go, rect

SHOTS = os.path.join(C.ROOT, "artifacts", "screenshots", "guided")
LIB10, LIB09, LIB03, LIB02 = "case_lib10_eob_ub04_cms1500", "case_lib09_spanish_interpreter_espalda", "case_lib03_truck_rear_end_chiro", "case_lib02_slip_fall_prior_knee"
JARGON = re.compile(r"\b(model's|its quote|checked by code|itemized service line|tray|excerpt|judge|LLM|J[1-4])\b|\bflags?\b|\bpending\b|\bverified\b", re.I)


@pytest.fixture
def make():
    made = []

    def _make(lib=None):
        import time
        st, c = C.api("POST", "/api/cases", {"sample": True} if lib is None else {"library": lib}); assert st in (200, 201), (st, c)
        tok = c["token"]; made.append(tok)
        assert C.api("POST", f"/api/cases/{tok}/run", {})[0] == 202
        for _ in range(300):
            s = C.api("GET", f"/api/cases/{tok}/status")[1]
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(0.5)
        assert s["status"] == "ready", s
        return tok
    yield _make
    for t in made:
        C.api("DELETE", f"/api/cases/{t}")


def case(tok):
    return C.api("GET", f"/api/cases/{tok}")[1]


def item(tok, iid):
    c = case(tok)
    return next(i for g in ("entries", "undated_entries", "flags", "amounts", "tray") for i in c[g] if i["id"] == iid)


def open_item(page, tok, iid=None, step="timeline"):
    go(page, f"/case/{tok}/{step}" + (f"?item={iid}" if iid else ""))
    page.get_by_test_id("card-line").wait_for()


def line_id(page):
    return page.get_by_test_id("card-line").get_attribute("data-item-id")


def settle(page, ms=350):
    page.wait_for_timeout(ms)


@pytest.fixture
def phone(pw):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True); pg = ctx.new_page()
    yield pg
    b.close()


def sized(pw, w, h):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}); return b, ctx.new_page()


# ------------------------------------------------------------------------------------------------ the screen

def test_opens_on_the_first_item_with_the_record_words_beside_it(page, make):
    seen = watch(page)
    tok = make(); e1 = item(tok, "e1")
    go(page, f"/case/{tok}/timeline")
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e1")
    assert page.evaluate("location.search") == "?item=e1", "the open item is in the address, so a reload lands on it"
    assert page.get_by_test_id("item-count").inner_text() == "Item 1 of 19" and page.get_by_test_id("progress-text").inner_text() == "0 answered · 19 to go"
    assert page.get_by_test_id("line-text").inner_text() == e1["summary"]
    marks = page.locator("[data-testid=card-source] mark")
    assert marks.count() == 1 and marks.first.inner_text() == e1["excerpt"], "the highlighted words are exactly the quote"
    assert "Record 1 · Austin EMS run report · January 9, 2026" in page.get_by_test_id("src-head").inner_text()
    assert page.get_by_test_id("question").inner_text() == "Does this line say the same thing as the highlighted words?"
    assert page.get_by_test_id("answer-yes").inner_text() == "Yes, this matches" and page.get_by_test_id("answer-no").inner_text() == "No, leave it out"
    assert page.get_by_test_id("btn-third").inner_text() == "Fix the wording"
    foot = page.get_by_test_id("card-foot").inner_text()
    assert "word for word" in foot and "a second AI check agreed" in foot, foot
    tag = page.get_by_test_id("line-tag")
    expect(tag).to_have_text("Prepared answer")                                    # D-065: a prepared answer says so, never "AI draft"
    assert "not written by an AI model" in tag.get_attribute("title")
    assert page.get_by_test_id("btn-undo").is_hidden()
    page.reload(); page.locator("[data-testid=view][data-ready]").wait_for(state="attached")
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e1")
    assert seen == [], seen


def test_every_item_screen_has_plain_words_and_no_provenance_leak(page, make):
    tok = make()
    open_item(page, tok)
    for n in range(19):
        page.wait_for_timeout(60)
        text = " ".join(page.get_by_test_id(t).inner_text() for t in ("card-line", "card-foot", "question", "src-head", "actions"))
        bad = JARGON.findall(text)
        assert not bad, (line_id(page), bad, text)
        assert "AI draft" not in text or "Prepared answer" not in text
        body = page.locator("body").inner_text()
        assert "model" not in page.get_by_test_id("card-line").inner_text().lower(), body
        page.get_by_test_id("btn-later").click(); settle(page, 80)
    assert page.get_by_test_id("done-heading").count() == 1 or line_id(page)


def test_a_warning_is_one_plain_card_with_its_evidence_marked(page, make):
    tok = make(); f = item(tok, "f_gap_r6_r7")
    open_item(page, tok, "f_gap_r6_r7")
    assert page.get_by_test_id("warning-heading").inner_text() == "A break in treatment"
    assert page.get_by_test_id("line-tag").inner_text() == "Warning for the attorney"
    assert page.get_by_test_id("warning-text").inner_text().startswith("Gap of 73 days between March 6, 2026"), "the title is not said twice"
    assert page.get_by_test_id("question").inner_text() == "Should the attorney be told about this?"
    assert page.get_by_test_id("answer-yes").inner_text() == "Yes, tell the attorney" and page.get_by_test_id("answer-no").inner_text() == "No, not needed"
    assert page.get_by_test_id("btn-third").inner_text() == "Add a note"
    assert [m.inner_text() for m in page.locator("[data-testid=card-source] mark").all()] == [e["excerpt"] for e in f["evidence"]]
    assert "Records 6 and 7" == page.get_by_test_id("src-head").inner_text()
    assert page.locator("[data-testid=record-text]").count() == 2
    assert "never in the letter" in page.get_by_test_id("card-foot").inner_text()


# ------------------------------------------------------------------------------------------------ answering

def test_yes_saves_with_version_and_expected_status_moves_on_and_undo_is_whole(page, make):
    seen = watch(page)
    tok = make(); e1 = item(tok, "e1"); sent = []
    page.on("request", lambda r: sent.append(json.loads(r.post_data)) if r.method == "POST" and r.url.endswith("/items/e1/review") else None)
    open_item(page, tok)
    page.get_by_test_id("answer-yes").click()
    expect(page.get_by_test_id("card-line")).not_to_have_attribute("data-item-id", "e1")
    assert sent == [{"action": "accept", "version": e1["version"], "expected_status": "pending"}], sent       # T-178: the version and the status the screen was showing
    assert item(tok, "e1")["review_status"] == "accepted"
    assert page.get_by_test_id("status-text").inner_text() == "Saved: item 1 kept in the letter."
    undo = page.get_by_test_id("btn-undo"); expect(undo).to_be_visible()
    box = undo.bounding_box(); vp = page.viewport_size
    assert box and 0 <= box["x"] and box["x"] + box["width"] <= vp["width"] and box["y"] + box["height"] <= vp["height"], "Undo is fully on screen"
    assert page.get_by_test_id("item-count").inner_text() == "Item 2 of 19" and page.get_by_test_id("progress-text").inner_text() == "1 answered · 18 to go"
    assert page.get_by_test_id("step-2").inner_text().count("18 of 19 left") == 1, "the step bar follows"
    assert page.evaluate("document.activeElement && document.activeElement.dataset.testid") == "answer-yes", "focus is on the first answer of the next item"
    undo.click()
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e1")
    assert item(tok, "e1")["review_status"] == "pending"
    assert "Undone" in page.get_by_test_id("status-text").inner_text()
    assert page.get_by_test_id("btn-undo").is_hidden()
    assert seen == [], seen


def test_no_leaves_it_out_and_a_flag_no_lists_it_as_ruled_out(page, make):
    tok = make()
    open_item(page, tok, "e1")
    page.get_by_test_id("answer-no").click(); expect(page.get_by_test_id("status-text")).to_have_text("Saved: item 1 left out of the letter.")
    assert item(tok, "e1")["review_status"] == "dismissed"
    open_item(page, tok, "f_r3_1")
    page.get_by_test_id("answer-no").click(); expect(page.get_by_test_id("status-text")).to_contain_text("marked not needed")
    assert item(tok, "f_r3_1")["review_status"] == "dismissed"
    open_item(page, tok, "f_r6_1")
    page.get_by_test_id("answer-yes").click(); expect(page.get_by_test_id("status-text")).to_contain_text("will go in the notes for the attorney")
    assert item(tok, "f_r6_1")["review_status"] == "accepted"


def test_back_and_decide_later_move_without_saving_and_a_decided_item_shows_the_answer(page, make):
    tok = make()
    open_item(page, tok, "e2")
    page.get_by_test_id("btn-later").click(); expect(page.get_by_test_id("card-line")).not_to_have_attribute("data-item-id", "e2")
    page.get_by_test_id("btn-back").click(); expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e2")
    assert item(tok, "e2")["review_status"] == "pending" and C.api("GET", f"/api/cases/{tok}/audit")[1].get("events", []) == []
    page.get_by_test_id("answer-yes").click(); settle(page)
    page.get_by_test_id("btn-back").click(); expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e2")
    foot = page.get_by_test_id("card-foot").inner_text(); assert foot.startswith("Your answer: kept in the letter.") and "You can change it" in foot, foot
    page.get_by_test_id("answer-no").click(); settle(page)
    assert item(tok, "e2")["review_status"] == "dismissed"


def test_a_note_on_a_warning_is_saved_in_the_page_and_cancel_sends_nothing(page, make):
    tok = make(); sent = []
    page.on("request", lambda r: sent.append(json.loads(r.post_data)) if r.method == "POST" and "/review" in r.url else None)
    open_item(page, tok, "f_r8_1")
    page.get_by_test_id("btn-third").click()
    ta = page.get_by_test_id("edit-note"); expect(ta).to_be_focused()
    ta.fill("Ask for the 2019 MRI."); page.get_by_test_id("answer-no").click()
    assert page.get_by_test_id("edit-note").count() == 0 and sent == []
    page.get_by_test_id("btn-third").click(); page.get_by_test_id("edit-note").fill("Ask for the 2019 MRI.")
    page.get_by_test_id("answer-yes").click()
    expect(page.get_by_test_id("status-text")).to_contain_text("with your note")
    assert [s["action"] for s in sent] == ["edit"] and sent[0]["edits"] == {"note": "Ask for the 2019 MRI."} and "version" in sent[0] and sent[0]["expected_status"] == "pending"
    f = item(tok, "f_r8_1"); assert f["review_status"] == "edited" and f["reviewer_note"] == "Ask for the 2019 MRI."
    open_item(page, tok, "f_r8_1"); assert "Ask for the 2019 MRI." in page.get_by_test_id("line-body").inner_text()


# ------------------------------------------------------------------------------------------------ a second tab changed it (T-178)

def test_a_stale_screen_shows_the_plain_message_and_reloads_the_item(page, make):
    tok = make(); e1 = item(tok, "e1")
    open_item(page, tok, "e1")
    assert C.api("POST", f"/api/cases/{tok}/items/e1/review", {"action": "dismiss", "version": e1["version"], "expected_status": "pending"})[0] == 200     # the other tab
    page.get_by_test_id("answer-yes").click()
    foot = page.get_by_test_id("card-foot")
    expect(foot).to_contain_text("This item changed in another tab. We've loaded the latest.")
    assert foot.get_attribute("role") == "alert"
    assert item(tok, "e1")["review_status"] == "dismissed", "nothing was overwritten"
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e1")                          # stays on the item
    expect(page.get_by_test_id("btn-third")).to_be_visible()
    page.get_by_test_id("btn-later").click(); page.get_by_test_id("btn-back").click()                           # back to it: the latest answer is shown
    assert page.get_by_test_id("card-foot").inner_text().startswith("Your answer: left out of the letter.")
    page.get_by_test_id("answer-yes").click(); settle(page)                                                     # and a fresh click now works from the loaded version
    assert item(tok, "e1")["review_status"] == "accepted"


# ------------------------------------------------------------------------------------------------ D-066

def test_a_disputed_line_cannot_be_accepted_until_she_says_she_read_it(page, make):
    tok = make(LIB10); e = item(tok, "e1"); sent = []
    assert e["ladder"]["judge"]["verdict"] in ("partially", "unsupported", "disagrees")
    st, r = C.api("POST", f"/api/cases/{tok}/items/e1/review", {"action": "accept"})
    assert st == 422 and r["error"]["code"] == "COMPARE_REQUIRED", (st, r)                                      # the server refuses it too
    page.on("request", lambda r: sent.append(json.loads(r.post_data)) if r.method == "POST" and "/review" in r.url else None)
    open_item(page, tok, "e1")
    yes, box = page.get_by_test_id("answer-yes"), page.get_by_test_id("check-compare")
    expect(yes).to_be_disabled(); expect(page.get_by_test_id("compare-reason")).to_contain_text("A second AI check")
    assert "second check found" not in page.get_by_test_id("card-foot").inner_text() and "quote" not in page.get_by_test_id("card-foot").inner_text().lower()
    assert not box.is_checked() and box.bounding_box()["width"] >= 26
    page.keyboard.press("a"); assert sent == [], "the A key does not get around the box"
    expect(page.get_by_test_id("check-compare")).to_be_focused()
    page.get_by_test_id("answer-no").hover()                                                                    # No and Fix are always available
    assert page.get_by_test_id("answer-no").is_enabled() and page.get_by_test_id("btn-third").is_enabled()
    box.check(); expect(yes).to_be_enabled()
    box.uncheck(); expect(yes).to_be_disabled(); box.check()
    yes.click(); expect(page.get_by_test_id("status-text")).to_contain_text("Saved: item 1")
    assert sent == [{"action": "accept", "compared": True, "version": e["version"], "expected_status": "pending"}], sent
    assert item(tok, "e1")["review_status"] == "accepted"
    nxt = line_id(page); assert not page.get_by_test_id("check-compare").count() or not page.get_by_test_id("check-compare").is_checked(), "the box is never pre-ticked on the next item"


def test_a_compare_the_page_did_not_expect_still_becomes_the_box(page, make):
    """Degrades gracefully: when the page does not know the item is disputed (a payload without the ladder verdict), the server's 422 COMPARE_REQUIRED puts the box up instead of a raw error."""
    tok = make(LIB10)

    def strip(route):
        r = route.fetch(); j = r.json()
        for g in ("entries", "flags", "amounts"):
            for i in j[g]:
                if i["id"] == "e1":
                    i["ladder"]["judge"] = {"verdict": "supported"}; i["reasons"] = []
        route.fulfill(response=r, json=j)
    page.route(re.compile(r"/api/cases/[^/]+$"), strip)
    open_item(page, tok, "e1")
    expect(page.get_by_test_id("check-compare")).to_have_count(0)
    page.get_by_test_id("answer-yes").click()
    expect(page.get_by_test_id("check-compare")).to_be_visible()
    foot = page.get_by_test_id("card-foot").inner_text(); assert "A second AI check found this only partly supported" in foot and "Not saved" not in foot, foot      # the verdict comes from the server's 422
    expect(page.get_by_test_id("answer-yes")).to_be_disabled()
    assert item(tok, "e1")["review_status"] == "pending"
    page.get_by_test_id("check-compare").check(); page.get_by_test_id("answer-yes").click(); settle(page)
    assert item(tok, "e1")["review_status"] == "accepted"


def test_a_disputed_warning_asks_for_the_same_box(page, make):
    tok = make(LIB03); f = item(tok, "f_r7_1")
    assert f["ladder"]["judge"]["verdict"] in ("partially", "unsupported", "disagrees", "disagree")
    open_item(page, tok, "f_r7_1")
    expect(page.get_by_test_id("answer-yes")).to_be_disabled(); page.get_by_test_id("check-compare").check(); page.get_by_test_id("answer-yes").click(); settle(page)
    assert item(tok, "f_r7_1")["review_status"] == "accepted"


def test_a_refusal_from_the_code_checks_disables_yes_and_offers_the_way_out(page, make):
    tok = make()

    def refuse(route):
        r = route.fetch(); j = r.json()
        for i in j["entries"]:
            if i["id"] == "e4":
                i["state"] = "needs_review"; i["reasons"] = ["SUMMARY_NUMBER_NOT_IN_EXCERPT"]; i["why"] = "The summary has a number, date or dollar figure that is not in the quoted text."
        route.fulfill(response=r, json=j)
    page.route(re.compile(r"/api/cases/[^/]+$"), refuse)
    open_item(page, tok, "e4")
    expect(page.get_by_test_id("answer-yes")).to_be_disabled()
    assert "highlighted words" in page.get_by_test_id("refusal").inner_text() and "quoted" not in page.get_by_test_id("refusal").inner_text()
    assert "hint" in page.get_by_test_id("btn-third").get_attribute("class")
    page.get_by_test_id("btn-third").click(); expect(page.get_by_test_id("edit-summary")).to_be_visible()


# ------------------------------------------------------------------------------------------------ fix the wording

def test_fix_the_wording_refusal_stays_in_the_footer_and_a_good_edit_asks_for_the_compare(page, make):
    tok = make(); e4 = item(tok, "e4"); sent = []
    page.on("request", lambda r: sent.append(json.loads(r.post_data)) if r.method == "POST" and "/review" in r.url else None)
    open_item(page, tok, "e4")
    page.get_by_test_id("btn-third").click()
    ta = page.get_by_test_id("edit-summary"); expect(ta).to_be_focused(); assert ta.input_value() == e4["summary"]
    assert page.get_by_test_id("question").inner_text() == "Change the line, then save it."
    assert page.get_by_test_id("answer-yes").inner_text() == "Save my wording" and page.get_by_test_id("answer-no").inner_text() == "Cancel"
    assert "tap whole sentences" in page.get_by_test_id("card-source").inner_text()
    sents = page.get_by_test_id("sentence"); assert sents.count() == 3
    assert [s.get_attribute("aria-pressed") for s in sents.all()] == ["true", "true", "false"]
    ta.fill("Neck pain 9/10; plan of care 12 visits."); page.get_by_test_id("answer-yes").click()
    foot = page.get_by_test_id("card-foot"); expect(foot).to_contain_text("Not saved"); assert "9" in foot.inner_text() and "highlighted words" in foot.inner_text() and "quote" not in foot.inner_text().lower()
    assert page.get_by_test_id("edit-summary").input_value() == "Neck pain 9/10; plan of care 12 visits.", "her text stays in the box"
    assert item(tok, "e4")["summary"] == e4["summary"]
    page.get_by_test_id("edit-summary").fill(e4["summary"] + " Reviewed."); page.get_by_test_id("answer-yes").click()
    expect(page.get_by_test_id("edit-summary")).to_have_count(0)
    assert sent[-1]["action"] == "edit" and sent[-1]["edits"] == {"summary": e4["summary"] + " Reviewed."} and sent[-1]["expected_status"] == "pending" and sent[-1]["version"] == e4["version"]
    assert page.get_by_test_id("line-tag").inner_text() == "Written by you"
    expect(page.get_by_test_id("compare-reason")).to_have_text("You changed the wording. Read it against the highlighted words once more.")
    expect(page.get_by_test_id("answer-yes")).to_be_disabled()
    assert page.get_by_test_id("item-count").inner_text().startswith("Item ") and "answered" in page.get_by_test_id("progress-text").inner_text()
    page.get_by_test_id("check-compare").check(); page.get_by_test_id("answer-yes").click(); settle(page)
    assert sent[-1]["action"] == "accept" and sent[-1]["compared"] is True
    assert item(tok, "e4")["review_status"] == "accepted"


def test_changing_the_highlighted_sentences_sends_the_quote_and_wording_together(page, make):
    tok = make(); e4 = item(tok, "e4"); sent = []
    page.on("request", lambda r: sent.append(json.loads(r.post_data)) if r.method == "POST" and "/review" in r.url else None)
    open_item(page, tok, "e4"); page.get_by_test_id("btn-third").click()
    sents = page.get_by_test_id("sentence")
    sents.nth(1).click(); assert sents.nth(1).get_attribute("aria-pressed") == "false" and sents.nth(0).get_attribute("aria-pressed") == "true"
    sents.nth(2).click(); page.get_by_test_id("answer-yes").click()                                              # sentences 1 and 3 are picked, 2 is not: they do not follow each other
    expect(page.get_by_test_id("card-foot")).to_contain_text("Pick sentences that follow each other."); assert sent == []
    sents.nth(2).click()                                                                                          # back to the first sentence only
    page.get_by_test_id("edit-summary").fill("Cervical range of motion reduced approx. 40%.")
    page.get_by_test_id("answer-yes").click(); expect(page.get_by_test_id("edit-summary")).to_have_count(0)
    assert len(sent) == 1 and sent[0]["edits"] == {"excerpt": "Cervical range of motion reduced approx. 40%.", "summary": "Cervical range of motion reduced approx. 40%."}, sent
    assert [m.inner_text() for m in page.locator("[data-testid=card-source] mark").all()] == ["Cervical range of motion reduced approx. 40%."], "the new words are highlighted"
    assert item(tok, "e4")["edit_to_check"] is True


def test_cancel_sends_nothing_and_leaves_the_card_as_it_was(page, make):
    tok = make(); sent = []
    page.on("request", lambda r: sent.append(r.url) if r.method == "POST" else None)
    open_item(page, tok, "e4"); before = page.get_by_test_id("line-text").inner_text()
    page.get_by_test_id("btn-third").click(); page.get_by_test_id("edit-summary").fill("something else"); page.get_by_test_id("answer-no").click()
    assert page.get_by_test_id("line-text").inner_text() == before and sent == []


# ------------------------------------------------------------------------------------------------ a date to pick, and items we could not check

def test_a_date_to_pick_shows_both_readings_a_suggestion_and_then_the_line(page, make):
    tok = make(LIB09); c = case(tok); dtc = c["dates_to_confirm"][0]; eid = c["undated_entries"][0]["id"]
    open_item(page, tok, eid)
    assert page.get_by_test_id("question").inner_text() == "Which date is right for this record?"
    assert page.get_by_test_id("line-tag").inner_text() == "Pick the date"
    marks = page.locator("[data-testid=card-source] mark"); assert marks.count() == 1 and marks.first.inner_text() == "Date: " + dtc["raw"]
    yes, no = page.get_by_test_id("answer-yes"), page.get_by_test_id("answer-no")
    assert "Suggested" in (yes.inner_text() + no.inner_text()) and (yes.inner_text() + no.inner_text()).count("Suggested") == 1
    assert "month first" in (yes.inner_text() + no.inner_text()) and "day first" in (yes.inner_text() + no.inner_text())
    assert dtc["suggestion"]["reason"] in page.get_by_test_id("card-foot").inner_text()
    assert yes.is_enabled() and not item(tok, eid)["date"], "nothing is chosen on load"
    sug = dtc["suggestion"]["iso"]
    (yes if sug and "Suggested" in yes.inner_text() else no).click()
    expect(page.get_by_test_id("line-tag")).not_to_have_text("Pick the date")
    assert line_id(page) == eid and item(tok, eid)["date"] == sug
    assert page.get_by_test_id("question").inner_text() == "Does this line say the same thing as the highlighted words?"
    assert "Part 2 of 2" in page.get_by_test_id("card-foot").inner_text()


def test_a_flag_that_could_not_be_confirmed_is_optional_and_can_be_left_out(page, make):
    tok = make(LIB02); t = case(tok)["tray"]
    assert t, "lib02 has a suggestion we could not confirm"
    tid = t[0]["id"]; open_item(page, tok, tid)
    assert page.get_by_test_id("line-tag").inner_text() == "We couldn't confirm this warning"
    assert page.get_by_test_id("item-count").inner_text() == "Optional"
    assert page.get_by_test_id("answer-yes").inner_text() == "OK, leave it out" and page.get_by_test_id("answer-no").inner_text() == "Decide later"
    why = page.get_by_test_id("tray-why").inner_text(); assert not JARGON.findall(why) and "quote" not in why.lower(), why
    left = page.get_by_test_id("progress-text").inner_text()
    page.get_by_test_id("answer-yes").click(); settle(page)
    assert "skipped" in page.get_by_test_id("status-text").inner_text()
    assert page.get_by_test_id("progress-text").inner_text().split("·")[1] == left.split("·")[1], "an optional item never counts in 'to go'"


def test_a_record_with_no_line_can_be_written_by_hand_from_whole_sentences(page, make):
    tok = make(); eid = C.tray_entry_for_record(tok, "r4")
    open_item(page, tok, eid)
    assert page.get_by_test_id("line-tag").inner_text() == "We couldn't check this one" and page.get_by_test_id("item-count").inner_text() == "Optional"
    assert page.get_by_test_id("question").inner_text() == "Read the record. Do you want to write this line yourself?"
    assert page.locator("[data-testid=card-source] mark").count() == 0, "nothing is highlighted: there was no usable quote"
    page.get_by_test_id("answer-yes").click()
    assert page.get_by_test_id("answer-yes").inner_text() == "Save my line" and page.get_by_test_id("answer-no").inner_text() == "Cancel"
    sents = page.get_by_test_id("sentence"); assert sents.count() == 3
    page.get_by_test_id("answer-yes").click(); expect(page.get_by_test_id("card-foot")).to_contain_text("Pick at least one sentence.")
    sents.nth(0).click(); page.get_by_test_id("answer-yes").click(); expect(page.get_by_test_id("card-foot")).to_contain_text("Write the line first.")
    page.get_by_test_id("edit-line").fill("Neck range of motion reduced about 40%.")
    page.get_by_test_id("answer-yes").click()
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", eid + "_m")
    assert page.get_by_test_id("question").inner_text() == "Does this line say the same thing as the highlighted words?"
    assert [m.inner_text() for m in page.locator("[data-testid=card-source] mark").all()] == ["Cervical range of motion reduced approx. 40%."]
    page.get_by_test_id("answer-yes").click(); settle(page)
    assert item(tok, eid + "_m")["review_status"] == "accepted"


# ------------------------------------------------------------------------------------------------ keyboard

def test_keyboard_a_d_e_and_the_arrow_keys(page, make):
    tok = make(); seen = watch(page)
    open_item(page, tok, "e1")
    page.keyboard.press("ArrowRight"); assert line_id(page) != "e1"
    page.keyboard.press("ArrowLeft"); assert line_id(page) == "e1"
    page.keyboard.press("a"); expect(page.get_by_test_id("status-text")).to_have_text("Saved: item 1 kept in the letter.")
    assert item(tok, "e1")["review_status"] == "accepted"
    open_item(page, tok, "e2"); page.keyboard.press("d"); expect(page.get_by_test_id("status-text")).to_have_text("Saved: item 3 left out of the letter.")        # e2 is the third item: a warning sits between e1 and e2
    open_item(page, tok, "e4"); page.keyboard.press("e")
    ta = page.get_by_test_id("edit-summary"); expect(ta).to_be_focused()
    page.keyboard.type("add dxa"); assert "add dxa" in ta.input_value() and item(tok, "e4")["review_status"] == "pending", "typing in the box is never a shortcut"
    page.keyboard.press("ArrowLeft"); assert page.get_by_test_id("edit-summary").count() == 1, "arrows move the cursor while she types"
    page.get_by_test_id("answer-no").click()
    page.keyboard.press("Control+a"); assert item(tok, "e4")["review_status"] == "pending"
    page.get_by_test_id("answer-yes").focus(); page.keyboard.press("Enter"); settle(page)
    assert item(tok, "e4")["review_status"] == "accepted", "Enter on the focused answer works"
    assert seen == [], seen


def test_tab_order_reaches_every_control_in_a_sensible_order(page, make):
    tok = make(); open_item(page, tok, "e1")
    page.get_by_test_id("answer-yes").focus(); order = []
    for _ in range(5):
        page.keyboard.press("Tab"); order.append(page.evaluate("document.activeElement.dataset.testid"))
    assert order[:4] == ["answer-no", "btn-back", "btn-third", "btn-later"], order


# ------------------------------------------------------------------------------------------------ done screen

def decide_everything(tok, dismiss=()):
    c = case(tok)
    for i in c["entries"] + c["undated_entries"] + c["flags"]:
        if i["review_status"] == "pending" and i["state"] != "rejected":
            body = {"action": "dismiss" if i["id"] in dismiss else "accept"}
            if body["action"] == "accept" and C.api("POST", f"/api/cases/{tok}/items/{i['id']}/review", body)[0] == 422:
                body["compared"] = True
                assert C.api("POST", f"/api/cases/{tok}/items/{i['id']}/review", body)[0] == 200, i["id"]
            elif body["action"] == "dismiss":
                assert C.api("POST", f"/api/cases/{tok}/items/{i['id']}/review", body)[0] == 200


def test_the_done_screen_counts_lists_every_answer_and_links_to_step_3(page, make):
    seen = watch(page)
    tok = make(); decide_everything(tok, dismiss=("e2", "f_r3_1"))
    go(page, f"/case/{tok}/timeline")
    expect(page.get_by_test_id("done-heading")).to_have_text("You checked every item on the timeline.")
    assert page.get_by_test_id("done-counts").inner_text() == "8 kept in the letter · 1 left out · 9 warnings for the attorney · 1 not needed"
    rows = page.get_by_test_id("answer-row"); assert rows.count() == 19
    chips = [c.inner_text() for c in page.get_by_test_id("answer-chip").all()]
    assert chips.count("Kept") == 8 and chips.count("Left out") == 1 and chips.count("Tell the attorney") == 9 and chips.count("Not needed") == 1, chips
    assert page.locator("[data-testid=step-2][aria-current=step]").count() == 1 and page.locator("[aria-current=step]").count() == 1, "one current step, and it is step 2"
    assert "We checked for" in page.get_by_test_id("checks-panel").inner_text() and "Not checked" in page.get_by_test_id("checks-panel").inner_text()
    assert page.locator("body.page").count() == 1 and page.get_by_test_id("btn-next-step").inner_text() == "Go to step 3: Check the bills"
    rows.nth(0).get_by_test_id("btn-change").click()
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e1"); assert page.evaluate("location.search") == "?item=e1"
    page.get_by_test_id("answer-no").click(); settle(page)
    assert item(tok, "e1")["review_status"] == "dismissed"
    expect(page.get_by_test_id("done-heading")).to_have_text("You checked every item on the timeline.")
    page.get_by_test_id("btn-next-step").click(); expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "bills")
    assert seen == [], seen


def test_the_done_screen_says_when_some_items_are_still_undecided(page, make):
    tok = make(); c = case(tok)
    for i in c["entries"]:
        if i["id"] not in ("e3", "e7"):
            C.api("POST", f"/api/cases/{tok}/items/{i['id']}/review", {"action": "accept"})
    for i in c["flags"]:
        C.api("POST", f"/api/cases/{tok}/items/{i['id']}/review", {"action": "dismiss"})
    go(page, f"/case/{tok}/timeline")
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e3")
    for _ in range(25):                                                                                           # Decide later walks the list; its end is the done screen
        if page.get_by_test_id("done-heading").count():
            break
        page.get_by_test_id("btn-later").click(); settle(page, 100)
    expect(page.get_by_test_id("done-heading")).to_have_text("2 items still need a decision.")
    assert page.get_by_test_id("step-2").get_attribute("data-state") in ("todo", "attn")
    page.get_by_test_id("btn-first-undecided").click(); expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "e3")


# ------------------------------------------------------------------------------------------------ layout: nothing moves, above the fold, phones

STABLE = ("[data-testid=step-bar]", "[data-testid=titlebar]", "[data-testid=answer-yes]", "[data-testid=answer-no]", "[data-testid=btn-back]", "[data-testid=btn-third]", "[data-testid=btn-later]",
          "[data-testid=question]", "[data-testid=card-src]", "[data-testid=card-line]", "[data-testid=card-foot]", "[data-testid=actions]", "[data-testid=status-slot]")


def boxes(page, skip=()):
    return {s: rect(page, s) for s in STABLE if s not in skip}


@pytest.mark.parametrize("w,h", [(1440, 900), (1366, 768), (390, 844)])
def test_nothing_moves_when_she_answers_or_changes_mode_and_the_primary_action_is_above_the_fold(pw, make, w, h):
    tok = make(LIB10); b, pg = sized(pw, w, h)
    try:
        seen = watch(pg)
        open_item(pg, tok, "e1")
        skip = ("[data-testid=card-foot]",) if w < 761 else ()               # on a phone the line card scrolls as one box, so its footer may move inside it
        first = boxes(pg, skip)
        y = pg.get_by_test_id("answer-yes").bounding_box(); assert y["y"] + y["height"] <= h, f"the primary action is below the fold at {w}x{h}"
        assert rect(pg, "[data-testid=actions]")[1] + rect(pg, "[data-testid=actions]")[3] == h, "the action bar sits at the bottom of the window"
        assert pg.evaluate("document.documentElement.scrollHeight <= window.innerHeight") and pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        pg.get_by_test_id("check-compare").check(); assert boxes(pg, skip) == first, "ticking the box moved something"
        pg.get_by_test_id("check-compare").uncheck(); assert boxes(pg, skip) == first
        pg.get_by_test_id("btn-third").click(); assert boxes(pg, skip) == first, "Fix the wording moved something"
        pg.get_by_test_id("answer-no").click(); assert boxes(pg, skip) == first, "Cancel moved something"
        pg.get_by_test_id("btn-later").click(); pg.wait_for_timeout(200)
        assert boxes(pg, skip) == first, "the next item sits in the same boxes"
        pg.get_by_test_id("answer-no").click(); pg.wait_for_timeout(300)
        assert boxes(pg, skip) == first, "an answer moved something (a Saved line, Undo)"
        pg.get_by_test_id("btn-back").click(); pg.wait_for_timeout(200); assert boxes(pg, skip) == first
        assert seen == [], seen
    finally:
        b.close()


def test_a_phone_shows_enough_of_the_record_keeps_undo_whole_and_folds_the_step_bar(phone, make):
    tok = make(); watch(phone)
    open_item(phone, tok, "e4")
    src = phone.get_by_test_id("card-source")
    ch, sh = src.evaluate("e => e.clientHeight"), src.evaluate("e => e.scrollHeight")
    assert ch >= 200 or sh - ch <= 24, f"the record shows {ch}px of {sh}px"
    assert phone.get_by_test_id("step-bar").evaluate("e => e.getBoundingClientRect().height") == 0, "the step bar is folded"
    t = phone.get_by_test_id("btn-steps"); assert t.inner_text().startswith("Step 2 of 4") and t.get_attribute("aria-expanded") == "false"
    before = boxes(phone)
    t.click(); expect(phone.get_by_test_id("step-3")).to_be_visible(); assert t.get_attribute("aria-expanded") == "true"
    assert {k: v for k, v in boxes(phone).items() if k != "[data-testid=step-bar]"} == {k: v for k, v in before.items() if k != "[data-testid=step-bar]"}, "opening the steps moved the page"
    phone.keyboard.press("Escape"); expect(phone.get_by_test_id("step-3")).to_be_hidden()
    phone.get_by_test_id("answer-yes").click()
    undo = phone.get_by_test_id("btn-undo"); expect(undo).to_be_visible()
    b = undo.bounding_box(); assert b["x"] >= 0 and b["x"] + b["width"] <= 390 and b["y"] + b["height"] <= 844
    assert phone.get_by_test_id("status-text").inner_text().startswith("Saved: item")
    assert phone.evaluate("document.documentElement.scrollWidth <= window.innerWidth")


def test_the_disputed_footer_is_reachable_on_a_phone_and_checking_it_enables_yes(phone, make):
    tok = make(LIB10); open_item(phone, tok, "e1")
    box = phone.get_by_test_id("check-compare"); box.scroll_into_view_if_needed(); expect(box).to_be_visible()
    bb = box.bounding_box(); assert bb["y"] + bb["height"] <= 844 - 170
    box.check(); expect(phone.get_by_test_id("answer-yes")).to_be_enabled()


# ------------------------------------------------------------------------------------------------ screenshots

def test_screenshots_at_1440_and_390(pw, make):
    os.makedirs(SHOTS, exist_ok=True)
    tok = make(); tok10 = make(LIB10); tok9 = make(LIB09)
    for w, h, tag in ((1440, 900, "1440"), (390, 844, "390")):
        b, pg = sized(pw, w, h)
        try:
            watch(pg)
            shots = [("step2-entry", tok, "e4", None), ("step2-warning", tok, "f_gap_r6_r7", None), ("step2-disputed", tok10, "e1", None), ("step2-date", tok9, case(tok9)["undated_entries"][0]["id"], None), ("step2-fix", tok, "e4", "btn-third")]
            for name, t, iid, click in shots:
                open_item(pg, t, iid)
                if click:
                    pg.get_by_test_id(click).click(); pg.wait_for_timeout(200)
                pg.screenshot(path=os.path.join(SHOTS, f"{name}-{tag}.png"))
            decide_everything(tok)
            go(pg, f"/case/{tok}/timeline"); pg.screenshot(path=os.path.join(SHOTS, f"step2-done-{tag}.png"))
            if tag == "390":
                open_item(pg, tok10, "e1"); pg.get_by_test_id("btn-steps").click(); pg.screenshot(path=os.path.join(SHOTS, "step2-steps-open-390.png"))
        finally:
            b.close()
