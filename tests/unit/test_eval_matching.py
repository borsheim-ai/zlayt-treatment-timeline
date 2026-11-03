"""evals.matching parity with the reference fixtures in evals/golden/check_golden.py (README 'Flags': overlap + one-to-one). CONTRACT 8.2 flag precision/recall."""
from evals.matching import assign
from tests.unit import _golden as G

def cand(typ, ev, **kw):
    d = dict(type=typ, evidence=[dict(record_no=r, excerpt=x) for r, x in ev]); d.update(kw); return d

GF = G.expected("sample")["flags"]
K4 = cand("causation", [(7, "New onset pain")])
K5 = cand("causation", [(7, "Date of accident per intake form: 2026-01-19.")])

def test_new_onset_candidate_is_k4_only():
    assert assign(GF, [K4]) == {"K4"}

def test_two_distinct_candidates_satisfy_both():
    assert assign(GF, [K4, K5]) == {"K4", "K5"}

def test_candidate_with_two_spans_counts_once():
    both = cand("causation", [(7, "New onset pain"), (7, "Date of accident per intake form: 2026-01-19.")])
    assert len(assign(GF, [both])) == 1

def test_other_types_never_satisfy_causation():
    gap = cand("gap", [(6, "x"), (7, "y")], from_date="2026-03-06", to_date="2026-05-18", days=73)
    assert assign(GF, [gap, cand("conflict", [(7, "Date of accident per intake form: 2026-01-19."), (1, "rear-ended at approx. 35 mph")])]) == {"G1", "C1"}

def test_fragment_and_wrong_gap_dates_earn_nothing():
    assert assign(GF, [cand("causation", [(7, "pain")])]) == set()
    assert assign(GF, [cand("gap", [(6, "x"), (7, "y")], from_date="2026-02-20", to_date="2026-03-06", days=14)]) == set()
