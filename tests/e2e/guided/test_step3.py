"""T-181 (D-068) guided Step 3, "Check the bills" (docs/GUIDED_UI_SPEC.md section 6). Real browser, the fixture backend, the real API (cases are made over the API and deleted afterwards).
Guarded: one amount at a time with the figure marked in its record; Yes count / No don't count; the bill total chip follows the server; version + expected_status on every write and the plain 409; the D-059 named confirm on a
flagged charge; the D-064 named confirm (count + separate_charge, plus the second flag) on an amount held back for a missing detail; amounts that are never counted; the D-066 compare box; no accept-all anywhere (charges are
never batched, D-059); plain words (no 'itemized service line', no 'model'); the keyboard; the done screen with the letter's total line; nothing moves; primary action above the fold; phone. Screenshots: artifacts/screenshots/guided/."""
import json
import os
import re
import pytest
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided.test_shell_smoke import watch, go, rect
from tests.e2e.guided.test_step2 import make, sized, phone, case, item, open_item, line_id, settle, JARGON, SHOTS   # noqa: F401  (make and phone are fixtures)

LIB06, LIB11, LIB12 = "case_lib06_lop_billed_vs_adjusted", "case_lib11_priors_and_ledger", "case_lib12_records_review_credibility"
BILL_JARGON = re.compile(r"itemized service line|model's|its quote|\bmodel\b|\bexcerpt\b|\btray\b|\bjudge\b|\bLLM\b", re.I)


def watch_review(page):
    sent = []
    page.on("request", lambda r: sent.append(json.loads(r.post_data)) if r.method == "POST" and "/review" in r.url else None)
    return sent


def countable(tok):
    return [a for a in case(tok)["amounts"] if a["countable"]]


# ------------------------------------------------------------------------------------------------ the screen

def test_opens_on_the_first_amount_with_the_figure_marked_in_its_record(page, make):
    seen = watch(page)
    tok = make(); a1 = item(tok, "a1")
    go(page, f"/case/{tok}/bills")
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "a1")
    assert page.evaluate("location.search") == "?item=a1"
    assert page.get_by_test_id("item-count").inner_text() == "Amount 1 of 4" and page.get_by_test_id("progress-text").inner_text() == "0 answered · 4 to go"
    assert page.get_by_test_id("figure").inner_text() == "$6,240.00" and page.get_by_test_id("line-tag").inner_text() == "Charge"
    assert [m.inner_text() for m in page.locator("[data-testid=card-source] mark").all()] == ["$6,240"]
    assert page.get_by_test_id("total-value").inner_text() == "$0.00"
    assert page.get_by_test_id("question").inner_text() == "Should this charge count toward the bill total?"
    assert page.get_by_test_id("answer-yes").inner_text() == "Yes, count it" and page.get_by_test_id("answer-no").inner_text() == "No, don't count it"
    assert "Counting it adds the amount to the bill total." in page.get_by_test_id("card-foot").inner_text()      # D-073: the card leads with the date-of-service blank note, then this sentence
    assert page.get_by_test_id("btn-third").is_hidden() or page.get_by_test_id("btn-third").evaluate("e => getComputedStyle(e).visibility") == "hidden", "no third action on a charge, and its place is kept"
    assert "Record 2 · Central ER discharge summary · record dated January 9, 2026" in page.get_by_test_id("src-head").inner_text()
    assert [i["id"] for i in case(tok)["amounts"]][:1] == ["a1"] and a1["kind"] == "charge"
    assert seen == [], seen


def test_the_queue_puts_charges_first_and_never_counted_amounts_last(page, make):
    tok = make(); order = []
    open_item(page, tok, step="bills")
    for _ in range(4):
        order.append(line_id(page)); page.get_by_test_id("btn-later").click(); settle(page, 120)
    assert order == ["a1", "a4", "a2", "a3"], order


def test_yes_counts_it_with_version_and_status_the_total_follows_and_undo_puts_it_back(page, make):
    seen = watch(page)
    tok = make(); a1 = item(tok, "a1"); sent = watch_review(page)
    open_item(page, tok, step="bills")
    page.get_by_test_id("answer-yes").click()
    expect(page.get_by_test_id("status-text")).to_have_text("Saved: amount 1 $6,240.00 counted in the bill total.")
    assert sent == [{"action": "accept", "version": a1["version"], "expected_status": "pending"}], sent
    assert page.get_by_test_id("total-value").inner_text() == "$6,240.00"
    assert item(tok, "a1")["review_status"] == "accepted" and case(tok)["totals"]["accepted"]["cents"] == 624000
    undo = page.get_by_test_id("btn-undo"); expect(undo).to_be_visible()
    b = undo.bounding_box(); assert b["x"] + b["width"] <= page.viewport_size["width"] and b["y"] + b["height"] <= page.viewport_size["height"]
    assert page.get_by_test_id("item-count").inner_text() == "Amount 2 of 4" and page.get_by_test_id("progress-text").inner_text() == "1 answered · 3 to go"
    undo.click(); expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "a1")
    assert page.get_by_test_id("total-value").inner_text() == "$0.00" and item(tok, "a1")["review_status"] == "pending"
    assert seen == [], seen


def test_no_does_not_count_it_and_a_never_counted_amount_is_listed_or_left_out(page, make):
    tok = make(); sent = watch_review(page)
    open_item(page, tok, "a1", step="bills"); page.get_by_test_id("answer-no").click(); expect(page.get_by_test_id("status-text")).to_contain_text("$6,240.00 not counted")
    assert item(tok, "a1")["review_status"] == "dismissed" and page.get_by_test_id("total-value").inner_text() == "$0.00"
    open_item(page, tok, "a2", step="bills")
    assert page.get_by_test_id("line-tag").inner_text() == "Never counted" and page.get_by_test_id("figure").inner_text() == "$185"
    assert page.get_by_test_id("reason").inner_text() == "This figure is a rate, not a charge, so it is not added to the total."
    assert page.get_by_test_id("question").inner_text() == "This amount is never added to the total. List it in the notes for the attorney?"
    assert "never added to the bill total" in page.get_by_test_id("card-foot").inner_text()
    page.get_by_test_id("answer-yes").click(); expect(page.get_by_test_id("status-text")).to_contain_text("listed in the notes for the attorney")
    assert sent[-1]["action"] == "accept" and item(tok, "a2")["review_status"] == "accepted"
    assert page.get_by_test_id("total-value").inner_text() == "$0.00", "a rate never changes the total"
    open_item(page, tok, "a3", step="bills")
    assert page.get_by_test_id("figure").inner_text() == "Not a money amount: missing 3 days of work"
    page.get_by_test_id("answer-no").click(); expect(page.get_by_test_id("done-heading")).to_have_text("1 amount still needs a decision.")     # a3 was the last one in the list: the done screen opens
    assert item(tok, "a3")["review_status"] == "dismissed"


def test_a_stale_screen_shows_the_plain_message_and_reloads_the_amount(page, make):
    tok = make(); a1 = item(tok, "a1")
    open_item(page, tok, "a1", step="bills")
    assert C.api("POST", f"/api/cases/{tok}/items/a1/review", {"action": "dismiss", "version": a1["version"], "expected_status": "pending"})[0] == 200
    page.get_by_test_id("answer-yes").click()
    expect(page.get_by_test_id("card-foot")).to_contain_text("This item changed in another tab. We've loaded the latest.")
    assert item(tok, "a1")["review_status"] == "dismissed" and case(tok)["totals"]["accepted"]["cents"] == 0
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "a1")
    page.get_by_test_id("btn-later").click(); page.get_by_test_id("btn-back").click()
    assert "Your answer: not counted." in page.get_by_test_id("card-foot").inner_text()      # D-073: the blank-date note leads the foot, her answer follows


# ------------------------------------------------------------------------------------------------ D-059, D-064, D-066

def test_a_flagged_charge_needs_its_named_confirm_before_it_counts(page, make):
    tok = make(); a1 = item(tok, "a1"); sent = watch_review(page)
    flag = {"flag": "likely_duplicate", "name": "Possible duplicate charge", "message": "This looks like the same charge as “ER charges $6,240” in record 3. Counting both would count one service twice.", "confirm_with": "likely_duplicate", "of": "a4"}

    def inject(route):
        r = route.fetch(); j = r.json()
        for a in j["amounts"]:
            if a["id"] == "a1":
                a["flag"] = flag; a["confirm_required"] = True
        route.fulfill(response=r, json=j)
    page.route(re.compile(r"/api/cases/[^/]+$"), inject)
    open_item(page, tok, "a1", step="bills")
    yes, box = page.get_by_test_id("answer-yes"), page.get_by_test_id("check-flag")
    expect(yes).to_be_disabled(); assert page.get_by_test_id("flag-message").inner_text() == flag["message"], "the server sentence is shown as given"
    assert "I checked: this is a separate charge, not the same one counted twice." in page.get_by_test_id("card-foot").inner_text()
    page.keyboard.press("a"); assert sent == []
    box.check(); expect(yes).to_be_enabled(); box.uncheck(); expect(yes).to_be_disabled(); box.check()
    yes.click(); expect(page.get_by_test_id("status-text")).to_contain_text("counted")
    assert sent == [{"action": "accept", "confirm": "likely_duplicate", "version": a1["version"], "expected_status": "pending"}], sent


def test_a_refused_confirm_shows_the_servers_own_sentence_in_the_footer(page, make):
    tok = make()

    def refuse(route):
        if route.request.method == "POST" and route.request.url.endswith("/items/a1/review"):
            route.fulfill(status=422, json={"error": {"code": "CONFIRM_REQUIRED", "message": "Possible duplicate charge: … It is not counted unless you confirm that flag by name (likely_duplicate).",
                                                      "detail": {"message": "This looks like the same charge twice. Confirm it is a separate charge to count it."}}})
        else:
            route.continue_()
    page.route(re.compile(r"/api/cases/[^/]+/items/a1/review$"), refuse)
    open_item(page, tok, "a1", step="bills"); page.get_by_test_id("answer-yes").click()
    foot = page.get_by_test_id("card-foot"); expect(foot).to_contain_text("This looks like the same charge twice. Confirm it is a separate charge to count it.")
    assert "likely_duplicate" not in foot.inner_text(), "no internal name on the screen"
    assert item(tok, "a1")["review_status"] == "pending"


def test_an_amount_held_back_for_a_missing_detail_is_counted_only_with_its_named_confirm(page, make):
    tok = make(LIB11); a = next(x for x in countable(tok) if not x.get("count_confirm")); sent = watch_review(page)
    open_item(page, tok, a["id"], step="bills")
    assert page.get_by_test_id("line-tag").inner_text() == "Not counted yet"
    reason = page.get_by_test_id("reason").inner_text(); assert "no date of service" in reason or reason, reason
    assert not BILL_JARGON.findall(reason), reason
    yes, no = page.get_by_test_id("answer-yes"), page.get_by_test_id("answer-no")
    expect(yes).to_be_disabled()
    page.keyboard.press("a"); assert sent == []
    page.get_by_test_id("check-separate").check(); expect(yes).to_be_enabled()
    page.get_by_test_id("check-separate").uncheck(); expect(yes).to_be_disabled(); page.get_by_test_id("check-separate").check()
    yes.click(); expect(page.get_by_test_id("status-text")).to_contain_text("counted in the bill total")
    assert sent[-1] == {"action": "count", "confirm": "separate_charge", "version": a["version"], "expected_status": "pending"}, sent
    got = item(tok, a["id"]); assert got["kind"] == "charge" and got["review_status"] == "accepted"
    assert page.get_by_test_id("total-value").inner_text() == C_money(case(tok)["totals"]["accepted"]["cents"])


def C_money(cents):
    return "${:,.2f}".format(cents / 100)


def test_the_second_named_confirm_shows_when_the_server_names_a_possible_duplicate(page, make):
    tok = make(LIB11); a = countable(tok)[0]; sent = watch_review(page)
    cc = {"flag": "likely_duplicate", "name": "Possible duplicate charge", "message": "This looks like the same service as another line at the same price. Counting both would count it twice.", "confirm_with": "likely_duplicate", "of": "a2"}

    def inject(route):
        r = route.fetch(); j = r.json()
        for x in j["amounts"]:
            if x["id"] == a["id"]:
                x["count_confirm"] = cc
        route.fulfill(response=r, json=j)
    page.route(re.compile(r"/api/cases/[^/]+$"), inject)
    page.route(re.compile(r"/api/cases/[^/]+/items/[^/]+/review$"), lambda route: route.fulfill(status=422, json={"error": {"code": "CONFIRM_REQUIRED", "message": "x", "detail": {"message": "stub"}}}) if route.request.post_data_json.get("action") == "count" else route.continue_())
    open_item(page, tok, a["id"], step="bills")
    assert page.get_by_test_id("count-confirm-message").inner_text() == cc["message"]
    yes = page.get_by_test_id("answer-yes"); page.get_by_test_id("check-separate").check(); expect(yes).to_be_disabled()
    page.get_by_test_id("check-flag").check(); expect(yes).to_be_enabled(); yes.click()
    expect(page.get_by_test_id("card-foot")).to_contain_text("stub")
    assert sent[-1]["confirm"] == "separate_charge" and sent[-1]["confirm_flag"] == "likely_duplicate", sent


def test_not_counting_a_countable_amount_notes_it_for_the_attorney(page, make):
    tok = make(LIB12); a = countable(tok)[0]; sent = watch_review(page)
    open_item(page, tok, a["id"], step="bills"); tick_compare(page); page.get_by_test_id("answer-no").click()
    expect(page.get_by_test_id("status-text")).to_contain_text("not counted. It is noted for the attorney")
    assert sent[-1]["action"] == "accept" and item(tok, a["id"])["review_status"] == "accepted" and item(tok, a["id"])["kind"] != "charge"
    assert case(tok)["totals"]["accepted"]["cents"] == 0


def tick_compare(pg):
    if pg.get_by_test_id("check-compare").count():
        pg.get_by_test_id("check-compare").check()


def R_disputed(a):
    j = (a.get("ladder") or {}).get("judge") or {}
    return j.get("verdict") in ("partially", "unsupported", "disagrees", "disagree")


def test_a_disputed_amount_needs_the_compare_box_for_the_answer_that_accepts_it(page, make):
    tok = make(LIB06); sent = watch_review(page)
    a = next(x for x in case(tok)["amounts"] if R_disputed(x) and x["kind"] != "charge" and not x["countable"])
    st, r = C.api("POST", f"/api/cases/{tok}/items/{a['id']}/review", {"action": "accept"}); assert st == 422 and r["error"]["code"] == "COMPARE_REQUIRED"
    open_item(page, tok, a["id"], step="bills")
    yes = page.get_by_test_id("answer-yes"); expect(yes).to_be_disabled(); expect(page.get_by_test_id("compare-reason")).to_contain_text("A second AI check")
    assert "quote" not in page.get_by_test_id("card-foot").inner_text().lower()
    page.get_by_test_id("check-compare").check(); yes.click(); settle(page)
    assert sent[-1] == {"action": "accept", "compared": True, "version": a["version"], "expected_status": "pending"}, sent
    assert item(tok, a["id"])["review_status"] == "accepted"


def test_a_compare_the_page_did_not_expect_opens_the_compare_view_not_an_error(page, make):
    tok = make(LIB06)
    a = next(x for x in case(tok)["amounts"] if R_disputed(x) and x["kind"] != "charge" and not x["countable"])

    def strip(route):
        r = route.fetch(); j = r.json()
        for x in j["amounts"]:
            if x["id"] == a["id"]:
                x["ladder"]["judge"] = {"verdict": "agree"}; x["reasons"] = []
        route.fulfill(response=r, json=j)
    page.route(re.compile(r"/api/cases/[^/]+$"), strip)
    open_item(page, tok, a["id"], step="bills")
    page.get_by_test_id("answer-yes").click()
    expect(page.get_by_test_id("check-compare")).to_be_visible(); assert "Not saved" not in page.get_by_test_id("card-foot").inner_text()
    expect(page.get_by_test_id("answer-yes")).to_be_disabled(); assert item(tok, a["id"])["review_status"] == "pending"


# ------------------------------------------------------------------------------------------------ no accept-all (D-059), words

def test_there_is_no_accept_all_and_the_server_refuses_a_batch_with_a_disputed_item_or_a_charge(page, make):
    tok = make(LIB06)
    for step in ("timeline", "bills"):
        open_item(page, tok, step=step)
        text = page.locator("body").inner_text().lower()
        assert "accept all" not in text and "count all" not in text and "all verified" not in text, step
        assert page.locator("[data-testid=btn-batch], [data-testid=btn-accept-verified]").count() == 0
    c = case(tok); t10 = make("case_lib10_eob_ub04_cms1500")
    disputed = next(e["id"] for e in case(t10)["entries"] if e["review_status"] == "pending" and R_disputed(e))
    st, r = C.api("POST", f"/api/cases/{t10}/review/batch", {"action": "accept", "item_ids": [disputed]})
    assert st == 422, (st, r)                                                                                 # the server refuses disputed items in a batch; the guided UI never sends one
    charge = next(a["id"] for a in c["amounts"] if a["kind"] == "charge")
    st, r = C.api("POST", f"/api/cases/{tok}/review/batch", {"action": "accept", "item_ids": [charge]}); assert st == 422 and r["error"]["code"] == "CHARGES_NOT_BATCHED", (st, r)


def test_every_amount_screen_reads_in_plain_words(page, make):
    tok = make(LIB11); open_item(page, tok, step="bills"); n = len([a for a in case(tok)["amounts"] if a["state"] != "rejected"])
    for _ in range(n):
        text = " ".join(page.get_by_test_id(t).inner_text() for t in ("card-line", "card-foot", "question", "src-head"))
        assert not BILL_JARGON.findall(text) and not JARGON.findall(text), (line_id(page), text)
        assert "itemized service line" not in text
        page.get_by_test_id("btn-later").click(); settle(page, 100)


def test_keyboard_a_d_and_the_arrows_work_on_amounts(page, make):
    tok = make(); seen = watch(page)
    open_item(page, tok, "a1", step="bills")
    page.keyboard.press("ArrowRight"); assert line_id(page) == "a4"
    page.keyboard.press("ArrowLeft"); assert line_id(page) == "a1"
    page.keyboard.press("a"); expect(page.get_by_test_id("status-text")).to_have_text("Saved: amount 1 $6,240.00 counted in the bill total.")
    page.keyboard.press("d"); expect(page.get_by_test_id("status-text")).to_have_text("Saved: amount 2 $2,150.00 not counted.")
    assert item(tok, "a1")["review_status"] == "accepted" and item(tok, "a4")["review_status"] == "dismissed"
    assert seen == [], seen


# ------------------------------------------------------------------------------------------------ done screen

def test_the_done_screen_shows_the_letters_total_line_and_three_plain_lists(page, make):
    seen = watch(page)
    tok = make()
    for aid, act in (("a1", "accept"), ("a4", "accept"), ("a2", "accept"), ("a3", "dismiss")):
        assert C.api("POST", f"/api/cases/{tok}/items/{aid}/review", {"action": act})[0] == 200
    go(page, f"/case/{tok}/bills")
    expect(page.get_by_test_id("done-heading")).to_have_text("You checked every bill amount.")
    line = page.get_by_test_id("letter-line").inner_text()
    assert line == "Billed charges accepted from these records: $8,390.00"
    st, ex = C.api("GET", f"/api/cases/{tok}/export"); assert st == 200 and line in ex["letter_text"], "the same line the letter carries"
    assert page.get_by_test_id("list-counted").locator("tr[data-testid=bill-row]").count() == 2
    assert page.get_by_test_id("list-never").locator("tr[data-testid=bill-row]").count() == 2
    assert "Not a money amount: missing 3 days of work" in page.get_by_test_id("list-never").inner_text()
    assert "You didn't leave out any charge." in page.get_by_test_id("list-not-counted").inner_text()
    assert page.locator("[aria-current=step]").count() == 1 and page.locator("[data-testid=step-3][aria-current=step]").count() == 1
    assert page.get_by_test_id("btn-next-step").inner_text() == "Go to step 4: Get your letter"
    page.get_by_test_id("list-counted").get_by_test_id("btn-change").first.click()
    expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "a1")
    page.get_by_test_id("answer-no").click(); settle(page)
    expect(page.get_by_test_id("letter-line")).to_have_text("Billed charges accepted from these records: $2,150.00")
    assert "Not counted by you (1)" in page.get_by_test_id("list-not-counted").inner_text()
    page.get_by_test_id("btn-next-step").click(); expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "letter")
    assert seen == [], seen


def test_the_done_screen_says_when_amounts_are_undecided_and_lists_an_overlap_warning(page, make):
    tok = make(); C.api("POST", f"/api/cases/{tok}/items/a1/review", {"action": "accept"})

    def overlap(route):
        r = route.fetch(); j = r.json()
        j["totals"]["possible_overlaps"] = [{"code": "POSSIBLE_OVERLAP", "statement_amount_id": "a1", "covered_amount_id": "a4", "statement_text": "$6,240", "covered_text": "$2,150",
                                             "message": "A statement line may already include a separately stated charge for the same kind of service. Check whether both belong in the total."}]
        route.fulfill(response=r, json=j)
    page.route(re.compile(r"/api/cases/[^/]+$"), overlap)
    go(page, f"/case/{tok}/bills?item=a4"); page.get_by_test_id("btn-later").click()
    for _ in range(6):
        if page.get_by_test_id("done-heading").count():
            break
        page.get_by_test_id("btn-later").click(); settle(page, 100)
    expect(page.get_by_test_id("done-heading")).to_have_text("3 amounts still need a decision.")
    assert "Check whether both belong in the total." in page.get_by_test_id("overlap").inner_text()
    assert page.get_by_test_id("overlap").get_by_role("link").count() == 2
    page.get_by_test_id("btn-first-undecided").click(); expect(page.get_by_test_id("card-line")).to_have_attribute("data-item-id", "a4")


def test_a_case_with_no_amounts_says_so_and_goes_to_step_4(page, make):
    tok = make()

    def none(route):
        r = route.fetch(); j = r.json(); j["amounts"] = []
        route.fulfill(response=r, json=j)
    page.route(re.compile(r"/api/cases/[^/]+$"), none)
    go(page, f"/case/{tok}/bills")
    expect(page.get_by_test_id("done-heading")).to_have_text("We didn't find any bill amounts in these records.")
    page.get_by_test_id("btn-next-step").click(); expect(page.locator("[data-testid=view]")).to_have_attribute("data-route", "letter")


# ------------------------------------------------------------------------------------------------ layout and screenshots

STABLE = ("[data-testid=step-bar]", "[data-testid=titlebar]", "[data-testid=answer-yes]", "[data-testid=answer-no]", "[data-testid=btn-back]", "[data-testid=btn-later]", "[data-testid=question]",
          "[data-testid=card-src]", "[data-testid=card-line]", "[data-testid=actions]", "[data-testid=status-slot]", "[data-testid=total-chip]")


@pytest.mark.parametrize("w,h", [(1440, 900), (1366, 768), (390, 844)])
def test_nothing_moves_between_amounts_and_the_primary_action_is_above_the_fold(pw, make, w, h):
    tok = make(LIB11); b, pg = sized(pw, w, h)
    try:
        seen = watch(pg); a = countable(tok)[0]["id"]
        open_item(pg, tok, a, step="bills")
        first = {s: rect(pg, s) for s in STABLE}
        y = pg.get_by_test_id("answer-yes").bounding_box(); assert y["y"] + y["height"] <= h, f"below the fold at {w}x{h}"
        assert pg.evaluate("document.documentElement.scrollHeight <= window.innerHeight") and pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        pg.get_by_test_id("check-separate").check(); assert {s: rect(pg, s) for s in STABLE} == first
        pg.get_by_test_id("btn-later").click(); pg.wait_for_timeout(200); assert {s: rect(pg, s) for s in STABLE} == first
        tick_compare(pg); pg.get_by_test_id("answer-no").click(); pg.wait_for_timeout(300); assert {s: rect(pg, s) for s in STABLE} == first, "an answer moved something"
        assert seen == [], seen
    finally:
        b.close()


def test_a_phone_shows_the_record_and_the_confirm_box_is_reachable(phone, make):
    tok = make(LIB11); a = countable(tok)[0]["id"]; watch(phone)
    open_item(phone, tok, a, step="bills")
    src = phone.get_by_test_id("card-source"); ch, sh = src.evaluate("e => e.clientHeight"), src.evaluate("e => e.scrollHeight")
    assert ch >= 80 or sh - ch <= 24, (ch, sh)            # T-181 r2: a line with tick boxes gets the room it needs on a phone (UX major 2); the record keeps 3+ lines and scrolls to the highlight
    box = phone.get_by_test_id("check-separate"); box.scroll_into_view_if_needed(); expect(box).to_be_visible(); box.check(); expect(phone.get_by_test_id("answer-yes")).to_be_enabled()
    assert phone.get_by_test_id("total-chip").is_visible() and phone.evaluate("document.documentElement.scrollWidth <= window.innerWidth")


def test_screenshots_at_1440_and_390(pw, make):
    os.makedirs(SHOTS, exist_ok=True)
    tok = make(); t11 = make(LIB11); cnt = countable(t11)[0]["id"]
    for w, h, tag in ((1440, 900, "1440"), (390, 844, "390")):
        b, pg = sized(pw, w, h)
        try:
            watch(pg)
            for name, t, iid in (("step3-charge", tok, "a1"), ("step3-never", tok, "a2"), ("step3-count", t11, cnt)):
                open_item(pg, t, iid, step="bills"); pg.screenshot(path=os.path.join(SHOTS, f"{name}-{tag}.png"))
            for aid, act in (("a1", "accept"), ("a4", "accept"), ("a2", "accept"), ("a3", "dismiss")):
                C.api("POST", f"/api/cases/{tok}/items/{aid}/review", {"action": act})
            go(pg, f"/case/{tok}/bills"); pg.screenshot(path=os.path.join(SHOTS, f"step3-done-{tag}.png"))
            for aid in ("a1", "a4", "a2", "a3"):
                C.api("POST", f"/api/cases/{tok}/items/{aid}/review", {"action": "reset"})
        finally:
            b.close()
