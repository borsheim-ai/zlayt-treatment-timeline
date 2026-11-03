"""T-060 round 5 + T-131 (frontend): HITL correctness and the ux pass-4 minors.
M1 a dismissed flag / amount keeps no Accept and `a` never flips it; M2 a reworded entry still marked Needs review is not decided, is named at export and has a control that clears it;
F3 after a / d focus stays in the same list; F2 one need-review count; F1/F5 plain reason sentences, each reason once; m6 long dates in <time datetime>; D-057 the Filtered-by-rule group;
T-121 the one-line letter control. New hooks (QA adds them to tests/e2e/conftest.py docstring): need-review-count, edit-check-hint, letter-style, letter-style-standard, letter-style-oneline,
tray-filtered, tray-filtered-summary, tray-filtered-rule, tray-filtered-item; data-edit-check, data-group."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, tray_entry_for_record

RAW_CODE = re.compile(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b|summary token|\btoken\b|\bjudge unavailable\b|\blexicon\b|\bfixture\b", re.I)


def _progress(page):
    t = page.locator("#progress-text").inner_text()
    m = re.match(r"(\d+) of (\d+) decided", t)
    assert m, t
    return int(m.group(1)), int(m.group(2)), int(page.locator("#progress-text").get_attribute("data-needs") or 0)   # T-166 F2: the line is short; the counts are data attributes


def _flag(page, kind="conflict"):
    return page.locator(f'[data-testid=flags-panel] [data-flag-type={kind}]').first


def _edit_entry_3(page):
    e = page.get_by_test_id("entry-3"); e.get_by_test_id("btn-edit").click()
    e.get_by_test_id("edit-summary").fill("Persistent neck pain 6/10 with daily headaches noted."); e.get_by_test_id("btn-save-edit").click()
    expect(e).to_have_attribute("data-review", "edited")
    return e


# ---- M1: a dismissed flag keeps no Accept, and `a` does not reverse it
def test_dismissed_flag_has_no_accept_and_a_key_does_nothing(page, sample_case):
    open_case(page, sample_case)
    fid = _flag(page).get_attribute("data-item-id")
    _flag(page).get_by_test_id("btn-dismiss").click()
    f = page.locator(f'[data-item-id="{fid}"]'); expect(f).to_have_attribute("data-review", "dismissed")
    assert f.get_by_test_id("btn-accept").count() == 0 and f.get_by_test_id("btn-edit").count() == 0, "a dismissed flag still offers Accept or Edit"
    assert f.get_by_role("button", name=re.compile(r"^(Accept|Edit note|Keep in notes)")).count() == 0
    assert f.get_by_test_id("btn-reset").inner_text().strip() == "Undo"
    assert "Needs review" not in f.inner_text() and "Dismissed" in f.inner_text()
    before = _progress(page)
    f.focus(); page.keyboard.press("a"); page.wait_for_timeout(300); page.keyboard.press("d"); page.wait_for_timeout(300)
    expect(f).to_have_attribute("data-review", "dismissed"); assert _progress(page) == before
    expect(page.locator("#rv-live")).to_contain_text("Undo")
    f.get_by_test_id("btn-reset").click(); expect(page.locator(f'[data-item-id="{fid}"]')).to_have_attribute("data-review", "pending")
    assert page.locator(f'[data-item-id="{fid}"]').get_by_test_id("btn-accept").count() == 1


def test_dismissed_amount_has_no_accept_and_a_key_does_nothing(page, sample_case):
    open_case(page, sample_case)
    row = page.get_by_test_id("unclear-tray").locator("[data-item-id]").first; aid = row.get_attribute("data-item-id")
    row.get_by_test_id("btn-dismiss").click()
    r = page.locator(f'[data-item-id="{aid}"]'); expect(r).to_have_attribute("data-review", "dismissed")
    assert r.get_by_test_id("btn-accept").count() == 0, "a dismissed amount still offers Keep in notes / Accept"
    assert "Needs review" not in r.inner_text() and r.get_by_test_id("btn-reset").inner_text().strip() == "Undo"
    before = _progress(page)
    r.focus(); page.keyboard.press("a"); page.wait_for_timeout(300)
    expect(r).to_have_attribute("data-review", "dismissed"); assert _progress(page) == before


def test_dismissing_a_flag_lowers_the_one_need_review_count(page, sample_case):
    open_case(page, sample_case)
    d0, t0, n0 = _progress(page); assert n0 > 0
    fid = _flag(page).get_attribute("data-item-id"); needs = _flag(page).get_attribute("data-state") == "needs_review"
    _flag(page).get_by_test_id("btn-dismiss").click(); expect(page.locator(f'[data-item-id="{fid}"]')).to_have_attribute("data-review", "dismissed")
    d1, t1, n1 = _progress(page)
    assert d1 == d0 + 1 and n1 == n0 - (1 if needs else 0)


# ---- F2: header, Open-decisions strip and Timeline chip show the same number and move together
def test_one_need_review_count_everywhere(page, sample_case):
    open_case(page, sample_case)
    def counts():
        h = _progress(page)[2]
        strip = int(re.match(r"(\d+)", page.get_by_test_id("need-review-count").inner_text()).group(1))
        chip = int(re.match(r"(\d+)", page.get_by_test_id("review-counts").locator(".chip--warn").inner_text()).group(1))
        return h, strip, chip
    h, s, c = counts(); assert h > 0 and h == s == c, (h, s, c)
    fid = _flag(page).get_attribute("data-item-id")
    _flag(page).get_by_test_id("btn-dismiss").click(); expect(page.locator(f'[data-item-id="{fid}"]')).to_have_attribute("data-review", "dismissed")
    h2, s2, c2 = counts(); assert h2 == s2 == c2, (h2, s2, c2)
    page.get_by_test_id("entry-1").get_by_test_id("btn-dismiss").click()
    h3, s3, c3 = counts(); assert h3 == s3 == c3, (h3, s3, c3)


# ---- M2: a reworded entry that is still marked Needs review is not decided
def test_edited_needs_review_entry_is_open_until_she_says_she_compared_it(page, sample_case):
    open_case(page, sample_case)
    d0, t0, n0 = _progress(page)
    e = _edit_entry_3(page)
    if e.get_attribute("data-state") != "needs_review":
        pytest.skip("this backend verified the edit; the case needs the judge to be unavailable (fixture backend)")
    assert e.get_attribute("data-edit-check") is not None
    d1, t1, n1 = _progress(page); assert d1 == d0, "an edit that is still Needs review was counted as decided"
    assert n1 >= 1 and page.get_by_test_id("need-review-count").inner_text().startswith(str(n1))
    ok = e.get_by_test_id("btn-accept"); expect(ok).to_contain_text("I compared it with the quote"); assert "btn--primary" in ok.get_attribute("class")
    expect(page.get_by_test_id("todo-list")).to_contain_text("1 edit to check")
    ok.click(); expect(page.get_by_test_id("entry-3")).to_have_attribute("data-review", "accepted")
    d2, t2, n2 = _progress(page); assert d2 == d0 + 1


def test_edit_to_check_is_named_before_the_letter_is_copied(page, sample_case):
    open_case(page, sample_case)
    if _edit_entry_3(page).get_attribute("data-state") != "needs_review":
        pytest.skip("this backend verified the edit")
    page.get_by_test_id("entry-1").get_by_test_id("btn-accept").click()          # something is in the letter
    page.get_by_test_id("btn-export").click(); page.get_by_test_id("btn-copy-letter").click()
    expect(page.get_by_test_id("copy-confirm")).to_contain_text("1 edited entry still marked Needs review")


def test_nothing_left_message_does_not_come_while_an_edit_is_open(page, sample_case):
    open_case(page, sample_case)
    if _edit_entry_3(page).get_attribute("data-state") != "needs_review":
        pytest.skip("this backend verified the edit")
    c = api("GET", f"/api/cases/{sample_case}")[1]
    for it in c["entries"] + c["amounts"] + c["flags"]:                       # decide everything else over the API
        if it["id"] != [e for e in c["entries"] if "r3" in e["record_ids"]][0]["id"] and it["state"] != "rejected" and it["review_status"] == "pending":
            api("POST", f"/api/cases/{sample_case}/items/{it['id']}/review", {"action": "dismiss"})
    page.reload(); page.get_by_test_id("timeline").wait_for()
    d, t, n = _progress(page); assert d == t - 1, (d, t)
    page.get_by_test_id("entry-3").focus(); page.keyboard.press("a")                    # T-136: a only asks; the confirm button records it
    expect(page.get_by_test_id("entry-3").get_by_test_id("edit-compare-prompt")).to_be_visible()
    page.keyboard.press("Enter")
    expect(page.locator("#rv-live")).to_contain_text("Nothing left to decide")


# ---- F3: a / d stay inside one list; a second `a` never accepts a flag the reviewer did not choose
def test_second_a_never_accepts_a_conflict_flag(page, sample_case):
    open_case(page, sample_case)
    page.get_by_test_id("entry-1").focus()
    page.keyboard.press("a"); page.wait_for_timeout(500)
    in_queue = page.evaluate("!!document.activeElement.closest('[data-testid=queue]')")
    assert in_queue, "focus left the timeline after the first accept"
    page.keyboard.press("a"); page.wait_for_timeout(500)
    assert page.locator("[data-testid=flags-panel] [data-review=accepted]").count() == 0, "a conflict flag was accepted by the second a"
    assert page.evaluate("!!document.activeElement.closest('[data-testid=queue]')")
    assert page.locator("[data-testid=queue] [data-review=accepted]").count() == 2


def test_a_run_down_the_timeline_stays_in_the_timeline(page, sample_case):
    open_case(page, sample_case)
    n = page.locator("[data-testid=queue] [data-item-id]").count()
    page.get_by_test_id("entry-1").focus()
    for _ in range(n):                                                       # one press per entry; the last one moves focus on to the flags (T-166 F6) and decides nothing there
        page.keyboard.press("a"); page.wait_for_timeout(250)
    assert page.evaluate("!document.activeElement.closest('[data-testid=queue]')"), "after the last entry focus should have moved on to the next list"
    assert page.locator("[data-testid=flags-panel] [data-review=accepted]").count() == 0
    assert page.locator("[data-testid=charges-panel] [data-review=accepted]").count() == 0
    assert page.locator("[data-testid=queue] [data-review=accepted]").count() == n


def test_flag_decision_moves_to_the_next_flag_of_the_same_kind_only(page, sample_case):
    open_case(page, sample_case)
    kinds = page.locator("[data-testid=flags-panel] [data-group]").evaluate_all("els => els.map(e => [e.getAttribute('data-group'), e.querySelectorAll('[data-item-id]').length])")
    kind = next(k for k, n in kinds if n >= 1)
    grp = page.locator(f'[data-testid=flags-panel] [data-group="{kind}"]'); n = grp.locator("[data-item-id]").count()
    grp.locator("[data-item-id]").first.focus()
    for _ in range(n + 1):
        page.keyboard.press("d"); page.wait_for_timeout(300)
        assert page.evaluate("(k) => { const a = document.activeElement.closest('[data-item-id]'); return !a || !!a.closest('[data-group=\"' + k + '\"]') || !!document.querySelector('#rv-live') }", kind)
    others = page.locator(f'[data-testid=flags-panel] [data-group]:not([data-group="{kind}"]) [data-review=dismissed]').count()
    assert others == 0, "d moved on to a flag of another kind"


# ---- F1 / F5: plain sentences, each reason once
def test_row_reasons_are_sentences_not_codes(page, sample_case):
    open_case(page, sample_case)
    _edit_entry_3(page)
    for r in page.get_by_test_id("entry-reasons").all():
        t = r.inner_text(); assert not RAW_CODE.search(t) and not t.lower().startswith("check:"), t
        assert t.strip().endswith("."), t


def test_tray_item_states_its_reason_once(page, cases_lib01):
    """Entry tray item says its reason once. T-173 (T-168): lib01 record 3 is in the tray by injection (see cases_lib01), because T-168 recorded that record's extract answer and
    the library case has no tray item of its own now. Assertions unchanged."""
    tray = page.get_by_test_id("rejected-tray").get_by_test_id("tray-item").first
    txt = tray.inner_text().lower()
    assert txt.count("no recorded") == 1, txt
    assert tray.get_by_test_id("tray-why").count() == 0 and tray.get_by_test_id("tray-reason").count() == 1


# ---- m6: long dates, machine date kept
def test_row_dates_are_long_and_keep_the_iso_date_in_datetime(page, sample_case):
    open_case(page, sample_case)
    d = page.get_by_test_id("entry-7").get_by_test_id("entry-date")
    assert d.evaluate("e => e.tagName") == "TIME" and d.get_attribute("datetime") == "2026-05-18" and d.inner_text() == "May 18, 2026"
    dts = [page.get_by_test_id(f"entry-{i}").get_by_test_id("entry-date").get_attribute("datetime") for i in range(1, 10)]
    assert dts == sorted(dts)


# ---- T-121: the one-line style has a control
def test_letter_style_control_gives_one_line_per_entry(page, sample_case):
    open_case(page, sample_case)
    page.get_by_test_id("entry-1").get_by_test_id("btn-accept").click()
    page.get_by_test_id("btn-export").click()
    expect(page.get_by_test_id("letter-style-standard")).to_be_checked()
    std = page.get_by_test_id("export-letter").inner_text()
    page.get_by_test_id("letter-style-oneline").check()
    expect(page.get_by_test_id("letter-style-oneline")).to_be_checked()
    expect(page.get_by_test_id("export-letter")).not_to_have_text(std)
    one = page.get_by_test_id("export-letter").inner_text()
    assert "[Ex. __ / Bates __]" in one and "Source [Ex." not in one.split("\n")[1] if len(one.split("\n")) > 1 else True
    assert len(one.splitlines()) < len(std.splitlines())
    assert one == api("GET", f"/api/cases/{sample_case}/export?style=oneline")[1]["letter_text"]
    page.get_by_test_id("letter-style-standard").check()
    expect(page.get_by_test_id("export-letter")).to_have_text(std)


# ---- D-057: the Filtered-by-rule group (the backend sends tray_filtered; the case body is rewritten here so the group is there whatever the fixture holds)
FILTERED = {"label": "Filtered by rule", "collapsed": True, "needs_action": False, "count": 1, "rules": [{"rule": "objective_negative", "ref": "D-032", "label": "Normal or negative findings",
            "explanation": "A normal or negative finding is context, not a flag, so the rule filtered it out. Nothing is needed from you.", "count": 1,
            "items": [{"id": "f_r2_3", "kind": "flag", "record_ids": ["r2"], "state": "rejected", "reasons": ["FILTERED_BY_RULE"], "why": "The AI proposed this as a flag, but a fixed rule filtered it out.",
                       "flag": {"type": "causation", "category": "objective_negative"}, "attempt": {"summary": None, "excerpt": "X-ray negative for fracture."}}]}]}


def test_filtered_by_rule_group_is_collapsed_names_the_rule_and_has_no_accept(page, sample_case):
    def add(route):
        r = route.fetch(); body = r.json(); body["tray_filtered"] = FILTERED; route.fulfill(response=r, json=body)
    page.route(re.compile(r"/api/cases/[^/?]+$"), lambda route: add(route) if route.request.method == "GET" else route.continue_())
    open_case(page, sample_case)
    g = page.get_by_test_id("tray-filtered"); expect(g).to_be_visible()
    assert g.get_attribute("open") is None
    expect(page.get_by_test_id("tray-filtered-summary")).to_contain_text("Filtered by rule (1)")
    g.locator("summary").click()
    expect(g.get_by_test_id("tray-filtered-rule").first).to_contain_text("Normal or negative findings")
    expect(g.get_by_test_id("tray-filtered-item").first).to_contain_text("X-ray negative for fracture.")
    assert g.get_by_test_id("btn-accept").count() == 0 and g.locator("[data-item-id]").count() == 0
    assert "objective_negative" not in g.inner_text()


@pytest.fixture
def cases_lib01(page):
    """T-173 (T-168): lib01 record 3's extract answer is recorded since T-168, so the case has no tray item from the backend. This fixture puts record 3's entry into the tray
    (tray_entry_for_record: the state a missing answer leaves) before the page opens, so the tray specs keep covering the tray."""
    st, c = api("POST", "/api/cases", {"library": "case_lib01_er_only_then_gap"})
    if st not in (200, 201):
        pytest.skip("library cases need ZLAYT_MODE=local")
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(.5)
    tray_entry_for_record(tok, "r3")
    open_case(page, tok)
    yield tok
    api("DELETE", f"/api/cases/{tok}")
