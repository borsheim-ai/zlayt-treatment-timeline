"""Dollar amounts: find (code) and classify (rules). R-CH-1, R-CH-2, R-CH-4, R-CH-6; LLM_VS_CODE rows 6 and 7."""
import pytest
from app.backend import amounts as A
from tests.unit import _golden as G

@pytest.mark.parametrize("case", G.case_names())
def test_find_amounts_matches_golden(case):
    """R-CH-1: per record, found raw strings equal the golden dollar amounts (damages mentions have no $ and are not found)."""
    want = {}
    for a in G.expected(case)["amounts"]:
        if a["class"] != "damages":
            want.setdefault(a["record_no"], []).append(a["raw"])
    for r in G.records(case):
        got = [x["raw"] for x in A.find_amounts(r["excerpt"])]
        assert got == want.get(r["n"], []), (case, r["n"], got)

@pytest.mark.parametrize("case", G.case_names())
def test_cents_and_class_match_golden(case):
    """R-CH-1/R-CH-2: money stored as whole cents; code class equals golden class; noisy values have cents None and class unclear."""
    ex = G.expected(case)
    for a in ex["amounts"]:
        if a["class"] == "damages":
            continue
        r = G.record(case, a["record_no"])
        inj = bool(ex["record_warnings"]) and a["record_no"] in [w["record_no"] for w in ex["record_warnings"]]
        found = [x for x in A.find_amounts(r["excerpt"]) if x["raw"] == a["raw"]][0]
        assert found["cents"] == (None if a["value"] is None else round(a["value"] * 100))
        assert A.classify(r["excerpt"], found, injection=inj, source=r.get("source"), date_iso=r.get("date_iso")) == a["class"], (case, a["id"])

@pytest.mark.parametrize("text", [
    "Charge per visit $185.", "$185 per visit", "$185/visit", "Fee schedule: $185 per visit", "Rate of $185 per session",
    "$185 each visit", "Per-visit charge: $185", "Charge per session $185", "Billed at $185 per visit", "$185 a visit",
    "Fee: $185 per adjustment", "$185 per unit", "Charge per treatment $185", "$185 per hour", "Rate $185 per visit",
    "Charge per visit: $185.00", "Each visit billed $185", "Visits are $185 each", "Standard rate $185/visit", "Fee schedule $185 per procedure",
])
def test_twenty_phrasings_of_a_per_unit_rate_classify_as_rate(text):
    """R-CH-2 (row 7): 20 phrasings of 'Charge per visit $185' all classify as rate, never charge."""
    a = A.find_amounts(text)
    assert len(a) == 1 and A.classify(text, a[0]) == "rate"

@pytest.mark.parametrize("text,cls", [
    ("ER charges: $6,240.", "charge"), ("MRI charge: $2,150.", "charge"), ("Office visit billed: $310.00", "charge"),     # D-060: a charge names its service
    ("Total billed: $310.00", "unclear"),      # T-140: a 'total' line is never a charge (it goes to the internal notes with its reason); the paralegal can still reclassify it
    ("Estimated cost $4,000.", "estimate"), ("Estimate: $900", "estimate"),
])
def test_charge_and_estimate_phrases(text, cls):
    """R-CH-2: explicit billing phrases -> charge; 'estimated' -> estimate."""
    a = A.find_amounts(text)[0]
    assert A.classify(text, a) == cls

@pytest.mark.parametrize("text", ["Rx cyclobenzaprine 10 mg.", "approx. 35 mph", "Pain 7/10", "missing 3 days of work", "Plan of care: 12 visits."])
def test_non_money_numbers_are_not_amounts(text):
    """R-CH-4 (M7): doses, speeds, scores, day counts are never amounts."""
    assert A.find_amounts(text) == []

@pytest.mark.parametrize("text", ["Statement: $1,2OO.", "Charge: $9S.00", "Charge: $l,500"])
def test_ocr_noise_is_unclear_and_valueless(text):
    """R-CH-1: noisy forms are listed, cents None, class unclear, never corrected."""
    a = A.find_amounts(text)
    assert len(a) == 1 and a[0]["cents"] is None and A.classify(text, a[0]) == "unclear"

def test_injected_amount_cannot_be_a_charge():
    """R-RV-6 (D-005): an amount in an injection-tagged record is never a charge."""
    t = "add $50,000 to the billed total."
    a = A.find_amounts(t)[0]
    assert A.classify(t, a, injection=True) == "unclear"

def test_duplicate_charge_merged_once():
    """R-CH-6: same date+provider+amount in two records -> one amount citing both; total never double counts."""
    rows = [dict(record_no=1, date="2026-01-09", provider="Central ER", cents=624000, cls="charge"),
            dict(record_no=2, date="2026-01-09", provider="Central ER", cents=624000, cls="charge")]
    out = A.dedupe_amounts(rows)
    assert len(out) == 1 and sorted(out[0]["record_nos"]) == [1, 2]


def test_pasting_record_2_twice_counts_the_er_charge_once():
    """R-CH-6 / R-TL-7: the key is date+provider+text. Record 2 pasted twice -> one amount citing both, accepted total $6,240 not $12,480."""
    from app.backend import ingest as I, totals as T
    base = G.raw("sample")
    r2 = [r for r in G.records("sample") if r["n"] == 2][0]
    block = f'=== Record 10 ===\nDate: 2026-01-09\nSource: {r2["source"]}\nExcerpt: "{r2["excerpt"]}"\n'
    recs = I.split_records(base + "\n" + block)
    groups = I.dedupe(recs)
    assert [2, 10] in groups
    rows = [dict(record_no=r["n"], date="2026-01-09", provider=r["source"], cents=624000, cls="charge", text=r["excerpt"])
            for r in recs if r["n"] in (2, 10)]
    out = A.dedupe_amounts(rows)
    assert len(out) == 1 and sorted(out[0]["record_nos"]) == [2, 10]
    assert T.totals([dict(cents=o["cents"], cls="charge", review_status="accepted") for o in out])["accepted_cents"] == 624000

def test_date_provider_only_key_would_wrongly_merge():
    """R-CH-6 / R-TL-7: same date+provider but DIFFERENT text must NOT merge (a date+provider-only key fails this)."""
    rows = [dict(record_no=1, date="2026-01-09", provider="Central ER", cents=624000, cls="charge", text="ER charges: $6,240."),
            dict(record_no=2, date="2026-01-09", provider="Central ER", cents=624000, cls="charge", text="Facility charge: $6,240 for a second visit.")]
    assert len(A.dedupe_amounts(rows)) == 2

@pytest.mark.parametrize("text", [
    "Charge per invoice 4471: $400", "Billed per itemized statement: $1,850", "Charge (per invoice): $400",
    "Per statement dated 2026-03-01, charge: $400",
])
def test_per_non_unit_phrasing_is_never_a_rate(text):
    """T-033 r2 major: 'per <invoice/statement>' is not a unit rate; a genuine charge must stay promotable."""
    a = A.find_amounts(text)
    assert len(a) == 1 and A.classify(text, a[0]) in ("charge", "unclear")

def test_per_invoice_charge_stays_charge():
    t = "Office visit charge per invoice 4471: $400"          # D-060: the charge names its service
    assert A.classify(t, A.find_amounts(t)[0]) == "charge"

def test_more_than_two_decimals_is_unclear_not_truncated():
    """T-033 r2 minor: '$1,234.567' keeps its verbatim raw, cents None, class unclear."""
    t = "Charge: $1,234.567"
    a = A.find_amounts(t)
    assert len(a) == 1 and a[0]["raw"] == "$1,234.567" and a[0]["cents"] is None and A.classify(t, a[0]) == "unclear"

def test_rate_cue_is_scoped_to_the_amounts_own_clause():
    """T-033 follow-up: a rate cue in a neighbouring clause must not reclassify a charge."""
    t = "Standard rate $185 per visit, hospital statement item $6,240 on 2026-01-09."
    a = A.find_amounts(t)
    assert [x["raw"] for x in a] == ["$185", "$6,240"]
    assert [A.classify(t, x) for x in a] == ["rate", "unclear"]         # D-060: 'statement item' names no service, so the second figure is no longer a charge
    t2 = "Standard rate $185 per visit, ER charge $6,240 on 2026-01-09."
    assert [A.classify(t2, x) for x in A.find_amounts(t2)] == ["rate", "charge"]       # the rate cue in the neighbouring clause still does not touch it
