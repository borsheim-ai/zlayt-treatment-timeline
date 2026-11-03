"""T-205 (D-071 + amendment + T-202 r2 clarification): guided Step 3 shows the date of service the letter prints (amounts[].service_date.text, byte for byte) and the plain confirm note when the date is not
certain. Never the statement date as the service date. Real browser, the fixture backend, the real API. case_09 (record dated Mar 1, service Feb 2), lib10 (one UB-04 period, June 9-12, statement June 19),
a charge she counted for a missing date (D-064: real, not stated, no note), and a not-stated charge WITH a note: the fixture set has no bill that parses to a doubtful date, so that one stub-rewrites the case
response's service_date with the backend's own sentences (service_date.confirm_note / not_stated_text), everything else on the page is real."""
import re
import time
import pytest
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided.test_shell_smoke import watch, go
from tests.e2e.guided.test_step2 import make, phone, case, item, open_item, line_id, settle   # noqa: F401  (make and phone are fixtures)
from app.backend import service_date as SD

LIB10, LIB11 = "case_lib10_eob_ub04_cms1500", "case_lib11_priors_and_ledger"
GOLD09 = C.ROOT + "/evals/golden/case_09_nonvisit_hides_gap.txt"


@pytest.fixture
def made_text():
    made = []

    def _make(text):
        st, c = C.api("POST", "/api/cases", {"text": text}); assert st == 201, (st, c)
        tok = c["token"]; made.append(tok)
        assert C.api("POST", f"/api/cases/{tok}/run", {})[0] == 202
        for _ in range(300):
            s = C.api("GET", f"/api/cases/{tok}/status")[1]
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(.5)
        assert s["status"] == "ready", s
        return tok
    yield _make
    for t in made:
        C.api("DELETE", f"/api/cases/{t}")


def letter_dates(tok):
    """The real export's letter text (each charge line is `<provider>, <date text>: $X`)."""
    for a in case(tok)["amounts"]:          # the letter lists accepted charges only
        if a["kind"] == "charge" and a["review_status"] == "pending":
            assert C.api("POST", f"/api/cases/{tok}/items/{a['id']}/review", {"action": "accept"})[0] == 200
    st, ex = C.api("GET", f"/api/cases/{tok}/export"); assert st == 200, ex
    return ex["letter_text"]


def test_case_09_shows_the_blank_not_the_statement_date_as_the_service_date(page, made_text):
    """D-073 (T-202 r5): 'Statement for visit of 2026-02-02' is a sentence, which the code does not read, so the bill line shows the fillable blank and names the statement date as the statement's."""
    seen = watch(page)
    tok = made_text(open(GOLD09).read()); a = item(tok, "a1"); sd = a["service_date"]
    assert sd["state"] == "not_stated" and sd["date_iso"] is None and sd["statement_date_iso"] == "2026-03-01" and sd["confirm_note"]
    assert sd["text"] == "date of service [__________] (record dated March 1, 2026)"
    open_item(page, tok, "a1", step="bills")
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    assert page.get_by_test_id("service-date").get_attribute("data-state") == "not_stated"
    assert "record dated March 1, 2026" in page.get_by_test_id("src-head").inner_text(), "the record's own date is named as the statement's, never bare"
    assert page.get_by_test_id("confirm-note").count() == 1, "a line with no certain date asks for the paralegal's confirmation"
    assert "billing statement, date of service [__________] (record dated March 1, 2026): $275.00" in letter_dates(tok), "the same text the letter prints"
    assert seen == [], seen


def test_lib10_shows_the_blank_for_every_charge(page, make):
    """D-073 fallback: no charge carries a service date; every charge shows the letter's blank (the UB-04 period is not read) with the confirm note."""
    seen = watch(page)
    tok = make(LIB10); charges = [a for a in case(tok)["amounts"] if a["kind"] == "charge"]
    assert [a["id"] for a in charges] == ["a2", "a3", "a4", "a5"]
    letter = letter_dates(tok)
    blank = "date of service [__________] (record dated June 19, 2026)"
    for a in charges:
        sd = a["service_date"]; assert sd["text"] == blank and sd["state"] == "not_stated" and sd["date_iso"] is None and sd["statement_date_iso"] == "2026-06-19"
        open_item(page, tok, a["id"], step="bills")
        assert page.get_by_test_id("service-date-text").inner_text() == blank, a["id"]
        assert "record dated June 19, 2026" in page.get_by_test_id("src-head").inner_text()
        assert page.get_by_test_id("confirm-note").count() == 1
        assert f"{blank}: {a['text']}" in letter, "the letter carries the same blank"
    # a rate is not a charge: it has no date of service to show
    open_item(page, tok, "a1", step="bills"); assert page.get_by_test_id("service-date").count() == 0
    assert seen == [], seen


def test_a_charge_with_no_stated_date_shows_the_not_stated_text_and_never_the_statement_date_as_the_service_date(page, make):
    """Real: a ledger line she counted (D-064) has no date of service and no note (she already knows). Step 3 and the done list show the letter's own text."""
    seen = watch(page)
    tok = make(LIB11); a = item(tok, "a2"); assert a["kind"] == "unclear" and a["countable"]
    st, r = C.api("POST", f"/api/cases/{tok}/items/a2/review", {"action": "count", "confirm": "separate_charge", "version": a["version"], "expected_status": "pending",
                                                              **({"confirm_flag": a["count_confirm"]["confirm_with"]} if a.get("count_confirm") else {})}); assert st == 200, r
    a = item(tok, "a2"); sd = a["service_date"]
    assert a["kind"] == "charge" and sd["state"] == "not_stated" and sd["date_iso"] is None and sd["confirm_note"] is None
    open_item(page, tok, "a2", step="bills")
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    assert re.fullmatch(r"date of service \[_{10}\] \(record dated [A-Z][a-z]+ \d{1,2}, \d{4}\)|date of service \[_{10}\]", sd["text"]), sd["text"]
    assert page.get_by_test_id("service-date").get_attribute("data-state") == "not_stated"
    assert page.get_by_test_id("confirm-note").count() == 0
    assert f"{sd['text']}: " in letter_dates(tok), "the letter prints this very text"
    assert "record dated" in page.get_by_test_id("src-head").inner_text() or "no date" in page.get_by_test_id("src-head").inner_text()
    # done list: decide the rest over the API, the Date of service column carries the same text
    for i in case(tok)["amounts"]:
        if i["review_status"] == "pending" and i["id"] != "a2":
            C.api("POST", f"/api/cases/{tok}/items/{i['id']}/review", {"action": "accept"})
    go(page, f"/case/{tok}/bills")
    if page.get_by_test_id("list-counted").count():
        expect(page.get_by_test_id("list-counted")).to_contain_text("Date of service")
        assert sd["text"] in page.get_by_test_id("list-counted").inner_text()
    assert seen == [], seen


def test_a_not_stated_charge_with_a_note_shows_the_note_in_plain_words_beside_the_quote(page, make):
    """The fixture set has no bill that parses to a doubtful date, so the case response's service_date for one charge is replaced with the backend's own sentences."""
    seen = watch(page)
    tok = make(LIB10); a = item(tok, "a2")
    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="ambiguous_numeric", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("ambiguous_numeric", "04/05/2026"))

    def rewrite(route):
        r = route.fetch(); body = r.json()
        for x in body.get("amounts", []):
            if x["id"] == "a2":
                x["service_date"] = sd
        route.fulfill(response=r, json=body)
    page.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
    open_item(page, tok, "a2", step="bills")
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    assert page.get_by_test_id("service-date").get_attribute("data-state") == "not_stated"
    note = page.get_by_test_id("confirm-note"); expect(note).to_be_visible(); assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-note]").count() == 1
    t = note.inner_text()
    assert "04/05/2026" in t and "The letter prints no service date for this line." in t and "Confirm the date from the highlighted words" in t, t      # the server's sentence, in the plain vocabulary
    assert not re.search(r"\bquote\b|\bmodel\b|\bexcerpt\b", t, re.I), t
    assert note.get_attribute("role") == "note"
    assert "record dated June 19, 2026" in page.get_by_test_id("src-head").inner_text()
    assert page.get_by_test_id("statement-date").count() == 0, "the not-stated text already names the statement date"
    # nothing about the decision changes: the human still answers Yes or No
    expect(page.get_by_test_id("answer-yes")).to_be_enabled()
    assert page.locator("[data-testid=card-source] mark").count() >= 1, "the quote is on the same screen"
    assert seen == [], seen


def test_the_date_and_note_fit_a_phone(phone, make):
    tok = make(LIB10); a = item(tok, "a2")
    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="no_year", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("no_year", "April 5"))
    def rewrite(route):
        r = route.fetch(); body = r.json()
        for x in body.get("amounts", []):
            if x["id"] == "a2":
                x["service_date"] = sd
        route.fulfill(response=r, json=body)
    phone.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
    open_item(phone, tok, "a2", step="bills")
    expect(phone.get_by_test_id("confirm-note")).to_be_visible()
    assert phone.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), "no sideways scroll"
    assert phone.get_by_test_id("answer-yes").is_visible()
