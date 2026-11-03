"""T-206 (D-071 follow-up to T-205, paralegal review minors): a Step 3 card shows a bare date only when it is a certain service date. An uncounted ledger line (lib11 a2-a4) and every other amount
taken from a bill document (the rest of the ledger) names its record's date "record dated ...", on the card head, the line under it and the source head; the confirm note ends with what to do next in
the words of the buttons the card has. Real browser, fixture backend, real API; the doubtful-date note is the backend's own sentence put into the case response (the fixture set has no such bill)."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.guided.test_shell_smoke import watch, go
from tests.e2e.guided.test_step2 import make, phone, case, item, open_item   # noqa: F401  (make and phone are fixtures)
from tests.e2e.guided.test_t205 import LIB10, LIB11, SD
import tests.e2e.conftest as C

BARE = re.compile(r"(?<!record dated )(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}")


def texts(page):
    return {k: page.get_by_test_id(k).inner_text() for k in ("card-line", "line-sub", "src-head")}


def test_lib11_uncounted_ledger_lines_never_show_a_bare_statement_date(page, make):
    seen = watch(page)
    tok = make(LIB11); amounts = {a["id"]: a for a in case(tok)["amounts"]}
    uncounted = [i for i, a in amounts.items() if a["kind"] != "charge"]
    assert {"a2", "a3", "a4"} <= set(uncounted) and amounts["a2"]["countable"] and amounts["a2"]["service_date"] is None
    for iid in uncounted:         # the three countable lines and the four never counted: all of them are the ledger
        open_item(page, tok, iid, step="bills")
        t = texts(page)
        assert "record dated June 15, 2026" in t["src-head"] and "record dated June 15, 2026" in t["line-sub"], (iid, t)
        for k, v in t.items():
            assert not BARE.search(v), (iid, k, v)
        assert page.get_by_test_id("confirm-note").count() == 0
    # the ED charge's source label names only the provider (D-073): no document type, so its header date is not lent and the blank prints with the statement date named
    open_item(page, tok, "a1", step="bills")
    assert page.get_by_test_id("service-date-text").inner_text() == "date of service [__________] (record dated March 18, 2026)"          # T-202 r6 rule 4: an ED record is a record, not a statement 
    assert "record dated March 18, 2026" in page.get_by_test_id("src-head").inner_text()          # T-211: the card heads read service_date.date_label too
    assert seen == [], seen


def test_lib11_a_counted_ledger_line_keeps_the_label_and_matches_the_letter(page, make):
    seen = watch(page)
    tok = make(LIB11); a = item(tok, "a2")
    st, r = C.api("POST", f"/api/cases/{tok}/items/a2/review", {"action": "count", "confirm": "separate_charge", "version": a["version"], "expected_status": "pending",
                                                              **({"confirm_flag": a["count_confirm"]["confirm_with"]} if a.get("count_confirm") else {})}); assert st == 200, r
    open_item(page, tok, "a2", step="bills")
    sd = item(tok, "a2")["service_date"]
    assert sd["state"] == "not_stated" and "record dated June 15, 2026" in sd["text"]
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    for k, v in texts(page).items():
        assert not BARE.search(v), (k, v)
    assert seen == [], seen


REASONS = [("ambiguous_numeric", "04/05/2026"), ("two_digit_year", "04/05/26"), ("no_year", "April 5"), ("invalid", "02/30/2026"), ("several_dates", "04/06/2026 and 04/20/2026"),
           ("implausible", "09/14/2026"), ("no_date", ""), ("non_service_date", "03/04/1980")]
NEXT = "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank"


def inject(page, tok, reason, raw):
    """Put the backend's own not-certain service_date (its sentences, SD.confirm_note) into a2's case response; the fixture set has no such bill."""
    a = item(tok, "a2")
    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason=reason, text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note(reason, raw))

    def rewrite(route):
        r = route.fetch(); body = r.json()
        for x in body.get("amounts", []):
            if x["id"] == "a2":
                x["service_date"] = sd
        route.fulfill(response=r, json=body)
    page.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
    return sd


def seen_ok(page, el):
    """The element's rect lies inside the card body's visible area and nothing else covers its centre (is_visible() passes for an element a scroll box has pushed under the foot)."""
    return page.evaluate("""(sel) => { const e = document.querySelector(sel), b = document.querySelector('[data-testid=card-body]') || e.closest('.card-b'); if (!e || !b) return 'missing';
      const r = e.getBoundingClientRect(), br = b.getBoundingClientRect();
      if (r.top < br.top - 1 || r.bottom > br.bottom + 1) return 'outside body ' + [r.top, r.bottom, br.top, br.bottom].join(',');
      const t = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return e.contains(t) || t.contains(e) ? 'ok' : 'covered by ' + t.tagName + '.' + t.className; }""", el)


@pytest.mark.parametrize("reason,raw", REASONS)
def test_every_not_certain_reason_gets_the_same_next_step_that_cannot_contradict_the_note(page, make, reason, raw):
    seen = watch(page)
    tok = make(LIB10); sd = inject(page, tok, reason, raw)
    open_item(page, tok, "a2", step="bills")
    nxt = page.get_by_test_id("confirm-next"); expect(nxt).to_be_visible()
    t = nxt.inner_text()
    assert NEXT in t and "\u201Cdate of service [__________]\u201D in your letter" in t, t
    assert "Counting it adds the amount to the bill total." in t and "If you don't," not in t, t
    assert "Fill the blank" not in t and "check the date" not in t.lower() and "you checked" not in t.lower() and "yourself" not in t, t
    assert "The date in parentheses is the record date, not the service date." in t
    note = page.get_by_test_id("confirm-note").inner_text()
    assert "highlighted words labels" not in note and " labels " not in note, note
    if "labels" in SD.confirm_note(reason, raw):
        assert "The highlighted words label " in note, note
    assert page.get_by_test_id("service-date").inner_text().lower().count("date of service") == 1
    labels = [page.get_by_test_id("answer-yes").inner_text().strip(), page.get_by_test_id("answer-no").inner_text().strip()]
    assert labels == ["Yes, count it", "No, don't count it"], "the sentence names the buttons the card really has"
    assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-next]").count() == 1
    assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-note]").count() == 1
    for k, v in texts(page).items():
        assert not BARE.search(v), (k, v)
    assert seen == [], seen


@pytest.mark.parametrize("size", [(1280, 900), (1366, 768)])
@pytest.mark.parametrize("reason,raw", [REASONS[0], REASONS[6], REASONS[4]])
def test_the_confirm_box_never_hides_the_amount_or_the_date_line(page, make, reason, raw, size):
    seen = watch(page)
    page.set_viewport_size({"width": size[0], "height": size[1]})
    tok = make(LIB10); inject(page, tok, reason, raw)
    open_item(page, tok, "a2", step="bills")
    expect(page.get_by_test_id("confirm-next")).to_be_visible()
    assert page.evaluate("(() => { const f = document.querySelector('[data-testid=card-foot]'); return f.scrollHeight <= f.clientHeight + 1; })()"), "the foot clips the next step"
    bb = page.get_by_test_id("answer-yes").bounding_box()
    assert bb and bb["y"] + bb["height"] <= size[1], "the answer buttons stay on screen"
    assert page.get_by_test_id("src-head").is_visible()
    assert seen_ok(page, "[data-testid=figure]") == "ok", seen_ok(page, "[data-testid=figure]")
    assert seen_ok(page, "[data-testid=service-date]") == "ok", seen_ok(page, "[data-testid=service-date]")
    assert seen == [], seen


def test_the_next_step_fits_a_phone(phone, make):
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
    expect(phone.get_by_test_id("confirm-next")).to_be_visible()
    assert phone.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
    assert phone.get_by_test_id("answer-yes").is_visible()
