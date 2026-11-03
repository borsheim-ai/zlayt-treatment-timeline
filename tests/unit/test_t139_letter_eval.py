"""T-139: the letter-level eval check (evals/letter_check.py) and the charge-line quote narrowing. Fixture backend, no key."""
import pytest

from app.backend import charge_text as CT
from app.backend import export as X
from evals import letter_check as LC

# The reviewer's lib01 export (artifacts/review-evidence/gate_m2_adjuster/case_lib01_er_only_then_gap_after_accept.json), shortened to the offending entries
BAD_LETTER = """TREATMENT CHRONOLOGY

April 13, 2026 — Plumtree Physical Therapy, initial evaluation
Cervical range of motion reduced approx. 30%. Plan of care: 8 visits. Charge per visit $140.
Source [Ex. __ / Bates __]: "Cervical range of motion reduced approx. 30%. Plan of care: 8 visits. Charge per visit $140."

BILLED CHARGES

Marrowgate General ED, February 14, 2026: $3,915.00
Source [Ex. __ / Bates __]: "ED charge: $3,915."

Billed charges accepted from these records: $3,915.00"""


def test_the_check_catches_the_gate_m2_letter():
    bad = LC.violations(BAD_LETTER, [391500])
    assert len(bad) == 2 and all("$140" in b for b in bad)


def test_the_check_passes_a_clean_letter_and_names_a_charge_that_is_not_accepted():
    clean = BAD_LETTER.replace(" Charge per visit $140.", "").replace(' Charge per visit $140."', '"')
    assert LC.violations(clean, [391500]) == []
    assert any("$3,915" in v for v in LC.violations(clean, [100]))              # an amount that is not an accepted charge or the total
    assert any("total line" in v for v in LC.violations(clean.replace("$3,915.00\"", "$3,915.00 (excludes rates)\"").replace("records: $3,915.00", "records: $3,915.00 (excludes rates)"), [391500]))


def test_nothing_accepted_as_a_charge_means_no_currency_anywhere():
    assert LC.violations("TREATMENT CHRONOLOGY\n\nPain 3/10.", (), expect_none=True) == []
    assert LC.violations(BAD_LETTER, (), expect_none=True)


def test_lib01_and_the_sample_pass_the_letter_check_end_to_end():
    cases = [(n, t) for n, t in LC.cases() if n in ("sample", "case_lib01_er_only_then_gap")]
    assert len(cases) == 2
    m = LC.measure(cases)
    assert m["value"] == 0 and m["held_out_entries"] == 0, m          # narrowing: lib01 e2/e4 and the sample e2/e4 keep their entry without the charge sentence


def test_every_golden_and_library_case_passes_the_letter_check():
    m = LC.measure()
    assert m["cases"] == 25 and m["value"] == 0, m["per_case"]


def _v(excerpt, raw, cents):
    rec = dict(n=1, source="Gannet and Moor Injury Clinic, billing statement", date_iso="2026-06-03", excerpt=excerpt)
    amt = dict(id="a1", record_no=1, cents=cents, cls="charge", raw=raw, excerpt=excerpt, review_status="accepted")
    return X._View(dict(records=[rec], entries=[], amounts=[amt], flags=[])), amt


@pytest.mark.parametrize("excerpt,raw,cents,want", [
    ("Statement of charges: office visits $1,100; MRI referral fee $450. Balance under letter of protection: $1,550.", "$1,100", 110000, "Statement of charges: office visits $1,100"),
    ("A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05.", "$187.05", 18705, "charge $187.05."),
    ("ER charges: $6,240.", "$6,240", 624000, "ER charges: $6,240."),                       # one figure: the sentence is quoted whole
])
def test_a_charge_line_quotes_only_the_clause_with_its_own_figure(excerpt, raw, cents, want):
    v, amt = _v(excerpt, raw, cents)
    q = X._amount_quote(v, amt)
    assert q == want and q in excerpt
    assert [f for f in CT.currency_strings(q) if f != raw] == []


def test_a_figure_with_no_clean_clause_is_cut_after_its_own_figure_or_quoted_as_the_sentence():
    """T-139 r5: the line up to the charge's own figure is a clean clause when nothing before it is money; with other money before the figure the sentence stays (the gate blocks)."""
    v, amt = _v("Amount billed $8,023.50 and plan paid $3,530.80.", "$8,023.50", 802350)
    assert X._amount_quote(v, amt) == "Amount billed $8,023.50"
    v, amt = _v("Plan paid $3,530.80 of the amount billed $8,023.50.", "$8,023.50", 802350)
    assert X._amount_quote(v, amt) == "Plan paid $3,530.80 of the amount billed $8,023.50."
