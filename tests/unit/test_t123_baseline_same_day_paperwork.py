"""T-123 (T-116 r5 M1): the accident baseline never calls a paperwork-headed record part of the 'first recorded treatment' (D-055),
including when paperwork and a visit share the earliest date (either record order) and for bare questionnaire / authorization headers."""
import pytest

from app.backend import conflicts as CF, gaps as G, ingest as I

HDR = "SYNTHETIC — invented for evaluation; not real patient data\n\n"
PAPER_HEADERS = ["Capital PT, intake form", "Capital PT, questionnaire", "Capital PT, authorization request", "Capital PT, pain questionnaire",
                 "Capital PT, prior authorization request", "Capital PT, new patient questionnaire (faxed)"]


def _rec(n, date, src, txt):
    return f"=== Record {n} ===\nDate: {date}\nSource: {src}\nExcerpt: \"{txt}\"\n\n"


def _conflict(items):
    t = HDR + "".join(_rec(i, d, s, e) for i, (d, s, e) in enumerate(items, 1))
    (c,) = CF.accident_date_conflicts(I.ingest(t)["records"])
    return c


PAPER_TXT = "Date of accident: 2026-01-15."
VISIT_TXT = "Cervical range of motion reduced approx. 40%."


@pytest.mark.parametrize("hdr", PAPER_HEADERS)
def test_bare_questionnaire_and_authorization_headers_are_paperwork(hdr):
    rec = I.ingest(HDR + _rec(1, "2026-01-12", hdr, PAPER_TXT))["records"][0]
    assert G.admin_label(rec)


@pytest.mark.parametrize("hdr", PAPER_HEADERS)
def test_paperwork_alone_on_first_date_is_warned(hdr):
    c = _conflict([("2026-01-12", hdr, PAPER_TXT), ("2026-01-20", "Capital PT, initial evaluation", VISIT_TXT)])
    assert "first recorded treatment" not in c["explanation"]
    assert "looks like paperwork" in c["explanation"]


@pytest.mark.parametrize("hdr", PAPER_HEADERS[:3])
@pytest.mark.parametrize("paper_first", [True, False])
def test_same_day_paperwork_and_visit_never_call_the_paperwork_treatment(hdr, paper_first):
    items = [("2026-01-12", hdr, PAPER_TXT), ("2026-01-12", "Capital PT, initial evaluation", VISIT_TXT)]
    c = _conflict(items if paper_first else items[::-1])
    e = c["explanation"]
    assert "first recorded treatment" not in e
    assert "looks like paperwork" in e
    assert "initial evaluation" in e                       # the visit is named as the first recorded visit
    assert c["first_treatment_date"] == "2026-01-12"


def test_visit_only_first_date_keeps_the_plain_wording():
    c = _conflict([("2026-01-12", "Capital PT, initial evaluation", VISIT_TXT + " Date of accident: 2026-01-15.")])
    assert "first recorded treatment" in c["explanation"]


def test_same_day_two_visits_and_no_paperwork_keeps_plain_wording():
    c = _conflict([("2026-01-12", "Capital PT, initial evaluation", VISIT_TXT + " Date of accident: 2026-01-15."),
                   ("2026-01-12", "Capital PT, daily note", VISIT_TXT)])
    assert "first recorded treatment" in c["explanation"]


def test_same_day_alternative_names_the_visit_and_says_not_later():
    c = _conflict([("2026-01-12", "Capital PT, intake form", PAPER_TXT), ("2026-01-12", "Capital PT, initial evaluation", VISIT_TXT)])
    assert "the first recorded visit is January 12, 2026" in c["explanation"]


@pytest.mark.parametrize("paper_first", [True, False])
def test_the_paperwork_record_is_the_one_named_as_paperwork_in_either_order(paper_first):
    """T-123 staff minor: the sentence names the PAPERWORK record (its number and source), never the visit, as 'looks like paperwork'."""
    items = [("2026-01-12", "Capital PT, intake form", PAPER_TXT), ("2026-01-12", "Capital PT, initial evaluation", VISIT_TXT)]
    c = _conflict(items if paper_first else items[::-1])
    n = 1 if paper_first else 2
    e = c["explanation"]
    assert f"(record {n}: Capital PT, intake form), which looks like paperwork" in e
    assert f"If record {n}: Capital PT, intake form is paperwork, not a visit" in e
    assert "initial evaluation), which looks like paperwork" not in e
