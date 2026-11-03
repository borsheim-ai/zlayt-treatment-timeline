"""T-151 (frontend; backend T-141 r2, T-142 legal-nurse review): the Conflicts group says which checks did NOT run on this case and shows info notes apart from conflicts.
GET case `checks`: skipped[] {type, label, reason_code, reason, record_nos?} (a check that did not run, or not on every record), notes[] {type, code, count, record_nos, stated_date, text} (info only).
  - skipped: each one is listed in the group, always visible, with the server's plain reason and, when the server names records, "Records 2, 4 and 7 were not read." A type that is skipped is NOT in the Checked list.
  - notes: info lines (conflict-note), not flag cards: no item id, no accept / dismiss, not counted in the group's count.
  - one line is always visible, also when conflicts are listed: the two kinds the legal nurse named (left versus right, loss of consciousness history) and "any other kind" are not checked.
Real backend on lib11 (a note, nothing skipped) and lib09 (Spanish records: three checks only partly ran); route stubs cover the other reason codes.
Test ids (declared in conftest): conflict-skipped, conflict-skipped-item (data-skip-type, data-reason-code), conflict-skipped-records, conflict-notes, conflict-note, conflict-not-checked-line."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case
import tests.e2e.conftest as C

CASE_URL = re.compile(r"/api/cases/[^/?]+$")
CODE = re.compile(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b")


def _make(lib):
    st, c = api("POST", "/api/cases", {"library": lib}); assert st in (200, 201), (st, c)
    tok = c["token"]
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.5)
    assert s["status"] == "ready", s
    return tok


@pytest.fixture(scope="module")
def lib11():
    if not C._up():
        pytest.skip("app server not running")
    tok = _make("case_lib11_priors_and_ledger"); yield tok; api("DELETE", f"/api/cases/{tok}")


@pytest.fixture(scope="module")
def spanish():
    if not C._up():
        pytest.skip("app server not running")
    tok = _make("case_lib09_spanish_interpreter_espalda"); yield tok; api("DELETE", f"/api/cases/{tok}")


def _group(page):
    return page.locator('[data-testid="flags-panel"] [data-group="conflict"]')


def _text(loc):
    return re.sub(r"\s+", " ", loc.inner_text())


def _checks(tok):
    return api("GET", f"/api/cases/{tok}")[1]["checks"]


def _seqs(nos):
    return "Record " + str(nos[0]) + " was" if len(nos) == 1 else "Records " + ", ".join(map(str, nos[:-1])) + " and " + str(nos[-1]) + " were"


# ---- lib11: an info note, nothing skipped --------------------------------------------------------------------------------------------------------
def test_lib11_note_is_shown_as_info_in_the_conflicts_group_and_not_as_a_conflict(page, lib11):
    ch = _checks(lib11)
    assert ch["notes"] and not ch["skipped"], ch                      # the backend gives lib11 one note and no skipped check
    open_case(page, lib11)
    g = _group(page)
    notes = g.get_by_test_id("conflict-note")
    expect(notes).to_have_count(len(ch["notes"]))
    for i, n in enumerate(ch["notes"]):
        expect(notes.nth(i)).to_have_text(re.compile(re.escape(n["text"])))
    assert notes.first.evaluate("n => !n.closest('[data-item-id]') && !n.querySelector('button')"), "a note is not an item: no id, no accept or dismiss"
    heading = g.get_by_role("heading", level=3).first.inner_text()
    n_cards = g.locator("[data-item-id]").count()
    assert re.search(rf"\({n_cards}\)\s*$", heading.strip()), (heading, n_cards)           # the count is conflicts only; the note is not one
    assert g.get_by_test_id("conflict-skipped").count() == 0, "nothing was skipped, so no skipped list"
    assert not CODE.search(_text(g.get_by_test_id("conflict-notes"))), "no reason code on screen"


def test_lib11_the_not_checked_line_is_visible_while_conflicts_are_listed(page, lib11):
    open_case(page, lib11)
    g = _group(page)
    assert g.locator("[data-item-id]").count() >= 1 and g.get_by_test_id("conflict-empty").count() == 0
    line = g.get_by_test_id("conflict-not-checked-line")
    expect(line).to_be_visible()
    t = _text(line).lower()
    assert "not checked" in t and "left versus right" in t and "loss of consciousness" in t and "other kind" in t, t
    assert not g.get_by_test_id("conflict-coverage").evaluate("d => d.open"), "the details stay collapsed; the line does not depend on them"


def test_the_not_checked_line_is_also_visible_when_the_group_is_empty(page, sample_case):
    def fn(route):
        d = route.fetch().json(); d["flags"] = [f for f in d["flags"] if f.get("type") != "conflict"]; route.fulfill(json=d)
    page.route(CASE_URL, fn)
    open_case(page, sample_case)
    expect(_group(page).get_by_test_id("conflict-not-checked-line")).to_be_visible()
    expect(_group(page).get_by_test_id("conflict-empty")).to_be_visible()


# ---- a Spanish case: three checks ran only in part -------------------------------------------------------------------------------------------------
def test_spanish_case_lists_the_denial_plan_and_accident_checks_under_skipped_with_the_server_reason(page, spanish):
    ch = _checks(spanish)
    skipped = {s["type"]: s for s in ch["skipped"]}
    assert {"plan_vs_early_end", "denial_vs_history"} <= set(skipped), ch["skipped"]
    open_case(page, spanish)
    g = _group(page)
    box = g.get_by_test_id("conflict-skipped"); expect(box).to_be_visible()                  # visible without opening anything
    items = box.get_by_test_id("conflict-skipped-item")
    expect(items).to_have_count(len(skipped))
    for t, s in skipped.items():
        it = box.locator(f'[data-testid=conflict-skipped-item][data-skip-type={t}]')
        expect(it).to_have_count(1)
        txt = _text(it)
        assert s["label"] in txt and s["reason"] in txt, txt                                  # the server's own words
        assert it.get_attribute("data-reason-code") == s["reason_code"]
        if s.get("record_nos"):
            assert _seqs(s["record_nos"]) + " not read" in _text(it.get_by_test_id("conflict-skipped-records")), _text(it)
    assert not CODE.search(_text(box)), "no reason code on screen"


def test_spanish_case_does_not_list_a_skipped_check_as_checked(page, spanish):
    ch = _checks(spanish)
    skipped = {s["type"] for s in ch["skipped"]}
    open_case(page, spanish)
    cov = _group(page).get_by_test_id("conflict-coverage")
    cov.evaluate("d => { d.open = true; }")
    checked = [t.strip() for t in cov.get_by_test_id("conflict-checked-item").all_inner_texts()]
    for t in skipped:
        assert ch["labels"][t] not in checked, (t, checked)
    ran = [ch["labels"][t] for t in ch["conflict_types"] if t not in skipped]
    assert checked == ran, (checked, ran)
    assert f"({len(ran)} kind{'' if len(ran) == 1 else 's'} checked)" in _text(cov.locator("summary"))


# ---- stubs: reason codes the fixture backend does not produce ---------------------------------------------------------------------------------------
def test_each_skipped_reason_is_shown_in_the_servers_words_without_records_when_none_are_named(page, sample_case):
    stub = {"conflict_types": ["provider_name"], "labels": {"plan_vs_early_end": "Plan against an early end", "denial_vs_history": "Denial against history", "accident_date": "Accident date against records", "provider_name": "Clinician under two practice names"},
            "skipped": [{"type": "plan_vs_early_end", "label": "Plan against an early end", "reason_code": "STAGE_SKIPPED", "reason": "The run hit its time limit before the records were compared."},
                        {"type": "accident_date", "label": "Accident date against records", "reason_code": "NO_DATED_RECORD", "reason": "No record has a date that could be read.", "record_nos": []},
                        {"type": "denial_vs_history", "label": "Denial against history", "reason_code": "LANGUAGE", "reason": "Every record is in a language this check does not read.", "record_nos": [1]}],
            "not_checked": [{"type": "dosage", "label": "Medication doses that differ between records"}],
            "notes": [{"type": "accident_date", "code": "RECORDS_PREDATE_ACCIDENT", "count": 2, "record_nos": [1, 2], "stated_date": "2026-03-18", "text": "2 records predate the stated accident date, March 18, 2026. None describes a collision."}]}

    def fn(route):
        d = route.fetch().json(); d["checks"] = stub; route.fulfill(json=d)
    page.route(CASE_URL, fn)
    open_case(page, sample_case)
    g = _group(page)
    items = g.get_by_test_id("conflict-skipped-item")
    expect(items).to_have_count(3)
    assert [i.get_attribute("data-reason-code") for i in items.all()] == ["STAGE_SKIPPED", "NO_DATED_RECORD", "LANGUAGE"]
    assert "time limit" in _text(items.nth(0)) and g.locator("[data-skip-type=plan_vs_early_end] [data-testid=conflict-skipped-records]").count() == 0
    assert g.locator("[data-skip-type=accident_date] [data-testid=conflict-skipped-records]").count() == 0, "an empty record list says nothing"
    assert "Record 1 was not read" in _text(g.locator("[data-skip-type=denial_vs_history]"))
    cov = g.get_by_test_id("conflict-coverage"); cov.evaluate("d => { d.open = true; }")
    assert [t.strip() for t in cov.get_by_test_id("conflict-checked-item").all_inner_texts()] == ["Clinician under two practice names"]
    expect(g.get_by_test_id("conflict-note")).to_have_text(re.compile("2 records predate the stated accident date"))


def test_no_skipped_or_notes_means_no_empty_boxes(page, sample_case):
    def fn(route):
        d = route.fetch().json(); ch = d.get("checks") or {}; ch["skipped"] = []; ch["notes"] = []; d["checks"] = ch; route.fulfill(json=d)
    page.route(CASE_URL, fn)
    open_case(page, sample_case)
    g = _group(page)
    assert g.get_by_test_id("conflict-skipped").count() == 0 and g.get_by_test_id("conflict-notes").count() == 0


def test_when_no_conflict_check_ran_the_group_says_so_with_the_reasons_and_shows_no_empty_list(page, sample_case):
    stub = {"conflict_types": [], "labels": {"plan_vs_early_end": "Plan against an early end", "denial_vs_history": "Denial against history"},
            "skipped": [{"type": "plan_vs_early_end", "label": "Plan against an early end", "reason_code": "LANGUAGE", "reason": "Every record is Spanish or unreadable, so this check, which reads English wording, could not run."},
                        {"type": "denial_vs_history", "label": "Denial against history", "reason_code": "RUN_FAILED", "reason": "The run stopped before the records were compared."}],
            "not_checked": [{"type": "dosage", "label": "Medication doses that differ between records"}], "notes": []}

    def fn(route):
        d = route.fetch().json(); d["checks"] = stub; d["flags"] = [f for f in d["flags"] if f.get("type") != "conflict"]; route.fulfill(json=d)
    page.route(CASE_URL, fn)
    open_case(page, sample_case)
    g = _group(page)
    empty = g.get_by_test_id("conflict-empty"); expect(empty).to_contain_text("No conflict checks ran for this case")
    assert "No conflicts found" not in _text(empty), _text(empty)
    expect(g.get_by_test_id("conflict-skipped-item")).to_have_count(2)
    for r in stub["skipped"]:
        assert r["reason"] in _text(g.get_by_test_id("conflict-skipped")), r
    cov = g.get_by_test_id("conflict-coverage")
    assert "no checks ran" in _text(cov.locator("summary")), _text(cov.locator("summary"))
    assert g.get_by_test_id("conflict-checked-item").count() == 0
    assert g.locator("ul:empty").count() == 0, "never an empty list"
    assert "0 kinds" not in _text(g)


def test_an_empty_conflict_types_without_reasons_still_says_no_check_ran(page, sample_case):
    def fn(route):
        d = route.fetch().json(); d["checks"] = {"conflict_types": [], "labels": {}, "skipped": [], "not_checked": [], "notes": []}; d["flags"] = [f for f in d["flags"] if f.get("type") != "conflict"]; route.fulfill(json=d)
    page.route(CASE_URL, fn)
    open_case(page, sample_case)
    g = _group(page)
    expect(g.get_by_test_id("conflict-empty")).to_have_text("No conflict checks ran for this case.")
    assert g.get_by_test_id("conflict-skipped").count() == 0 and g.locator("ul:empty").count() == 0
