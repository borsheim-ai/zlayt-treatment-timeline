"""T-142 (GATE-M2 legal nurse, major 1): the conflict group never says just "No conflicts found.". It names the conflict types the code checks and says the others are not checked.
The words come from GET case `checks` (T-141: {conflict_types: [...], labels: {type: sentence}, not_checked: [{type, label}]}), so they cannot drift from the code; with no `checks` the
panel says so with a fixed, true fallback (the three checks and the two examples the legal nurse named). Route stubs rewrite GET .../cases/<token> only, so this runs on any backend.
Test ids (declared in conftest): conflict-empty, conflict-coverage (details), conflict-checked-item, conflict-not-checked-item, conflict-coverage-note."""
import re
from playwright.sync_api import expect
from tests.e2e.conftest import open_case

CASE_URL = re.compile(r"/api/cases/[^/?]+$")
CHECKS = {"conflict_types": ["plan_vs_early_end", "denial_vs_history", "accident_date", "provider_name"],
          "labels": {"plan_vs_early_end": "A stated plan of care against a later record where the course ended early",
                     "denial_vs_history": "A denial of prior problems against a prior condition in another record",
                     "accident_date": "A stated accident date against the dates of the records",
                     "provider_name": "The same clinician named under two different practice names"},
          "not_checked": [{"type": "dosage", "label": "Medication doses that differ between records"},
                          {"type": "laterality", "label": "Left versus right across records"}]}


def _stub(page, checks="keep", drop_conflicts=False):
    """checks: 'keep' (the real answer), 'remove' (the field is absent) or a dict (this answer)."""
    def fn(route):
        d = route.fetch().json()
        if checks == "remove":
            d.pop("checks", None)
        elif checks != "keep":
            d["checks"] = checks
        if drop_conflicts:
            d["flags"] = [f for f in d.get("flags", []) if f.get("type") != "conflict"]
        route.fulfill(json=d)
    page.route(CASE_URL, fn)


def _group(page):
    return page.locator('[data-testid="flags-panel"] [data-group="conflict"]')


def _text(loc):
    return re.sub(r"\s+", " ", loc.inner_text())


def test_the_empty_state_names_the_checked_types_and_says_others_are_not_checked(page, sample_case):
    _stub(page, CHECKS, drop_conflicts=True)
    open_case(page, sample_case)
    g = _group(page); empty = g.get_by_test_id("conflict-empty"); expect(empty).to_be_visible()
    t = _text(empty)
    assert t.strip() != "No conflicts found." and "checked" in t, t
    assert "No conflicts found." not in t, t                                                   # never the bare all-clear sentence
    for lab in CHECKS["labels"].values():
        assert lab in _text(g.get_by_test_id("conflict-coverage")), lab
    assert g.get_by_test_id("conflict-checked-item").count() == 4
    assert "not checked" in t.lower() or "not checked" in _text(g.get_by_test_id("conflict-coverage")).lower()
    for nc in CHECKS["not_checked"]:
        assert nc["label"] in _text(g.get_by_test_id("conflict-coverage")), nc
    assert g.get_by_test_id("conflict-not-checked-item").count() == 2
    assert g.get_by_test_id("conflict-coverage").evaluate("d => d.open"), "the list is open when there is nothing else to read"


def test_the_words_come_from_the_api_not_from_the_page(page, sample_case):
    mine = {"conflict_types": ["zebra_vs_dog"], "labels": {"zebra_vs_dog": "Zebra stripes against dog spots"}, "not_checked": [{"type": "x", "label": "Cat whiskers"}]}
    _stub(page, mine, drop_conflicts=True)
    open_case(page, sample_case)
    g = _group(page)
    assert [t.strip() for t in g.get_by_test_id("conflict-checked-item").all_inner_texts()] == ["Zebra stripes against dog spots"]
    assert [t.strip() for t in g.get_by_test_id("conflict-not-checked-item").all_inner_texts()] == ["Cat whiskers"]
    assert "plan of care" not in _text(g), "no checked type is written into the page itself when the API sent its own list"


def test_a_group_with_conflicts_still_says_what_is_and_is_not_checked(page, sample_case):
    _stub(page, CHECKS)
    open_case(page, sample_case)
    g = _group(page); assert g.locator("[data-item-id]").count() >= 1
    assert g.get_by_test_id("conflict-empty").count() == 0
    cov = g.get_by_test_id("conflict-coverage"); expect(cov).to_be_visible()
    assert not cov.evaluate("d => d.open"), "collapsed when conflicts are listed"
    cov.locator("summary").click()
    assert g.get_by_test_id("conflict-checked-item").count() == 4 and g.get_by_test_id("conflict-not-checked-item").count() == 2
    assert "Left versus right across records" in _text(cov)


def test_without_checks_the_panel_still_says_what_it_does_not_cover(page, sample_case):
    _stub(page, "remove", drop_conflicts=True)
    open_case(page, sample_case)
    g = _group(page); t = _text(g.get_by_test_id("conflict-empty") ) + " " + _text(g.get_by_test_id("conflict-coverage"))
    assert t.strip() != "No conflicts found."
    low = t.lower()
    assert "not checked" in low and "left" in low and "right" in low and "loss of consciousness" in low, t
    assert "plan" in low and "denial" in low and "accident date" in low, t
    assert g.get_by_test_id("conflict-coverage-note").count() == 1, "the fallback says the server's list was not available"


def test_the_real_backend_list_is_shown_when_it_sends_one(page, sample_case):
    from tests.e2e.conftest import api
    ch = api("GET", f"/api/cases/{sample_case}")[1].get("checks")
    if not ch:
        import pytest; pytest.skip("this backend does not send `checks` yet (T-141)")
    open_case(page, sample_case)
    g = _group(page); g.get_by_test_id("conflict-coverage").evaluate("d => { d.open = true; }")
    shown = [t.strip() for t in g.get_by_test_id("conflict-checked-item").all_inner_texts()]
    assert shown == [ch["labels"].get(t) or t for t in ch["conflict_types"]]
    assert [t.strip() for t in g.get_by_test_id("conflict-not-checked-item").all_inner_texts()] == [x["label"] for x in ch.get("not_checked", [])]
