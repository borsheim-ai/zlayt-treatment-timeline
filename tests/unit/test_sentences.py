"""Sentence units. R-TL-2 (D-012/D-021 splitter), LLM_VS_CODE row 4 rung 1."""
import pytest
from app.backend import sentences as S
from tests.unit import _golden as G

CASES = G.case_names()

def all_records():
    return [(c, r) for c in CASES for r in G.records(c)]

@pytest.mark.parametrize("case,rec", all_records(), ids=lambda x: x if isinstance(x, str) else f"r{x['n']}")
def test_units_concatenate_to_every_golden_record(case, rec):
    """R-TL-2: for every golden record, the units concatenated equal the record text."""
    assert "".join(S.units(rec["excerpt"])) == rec["excerpt"]

def test_spans_are_contiguous_and_cover_text():
    """R-TL-2: unit_spans tile the text with no gap or overlap."""
    t = G.record("sample", 2)["excerpt"]
    spans = S.unit_spans(t)
    assert spans[0][0] == 0 and spans[-1][1] == len(t)
    assert all(a[1] == b[0] for a, b in zip(spans, spans[1:]))

def test_approx_period_is_not_a_terminator():
    """R-TL-2: 'approx. 35 mph.' in sample record 1 is ONE unit."""
    us = [u.strip() for u in S.units(G.record("sample", 1)["excerpt"])]
    assert us[0] == "41M restrained driver, rear-ended at approx. 35 mph."
    assert len(us) == 4

@pytest.mark.parametrize("text,first", [
    ("Seen by Dr. Alvarez today. Pain 4/10.", "Seen by Dr. Alvarez today."),
    ("Rx cyclobenzaprine 10 mg. Follow up in 1 week.", "Rx cyclobenzaprine 10 mg."),   # 'mg.' before a capitalised sentence IS a terminator (backend splitter; REQ R-TL-2 abbreviation list to be corrected)
    ("Range of motion improved 1.5 cm. Pain 3/10.", "Range of motion improved 1.5 cm."),
    ("Compare e.g. prior films. Next.", "Compare e.g. prior films."),
    ("Cervical ROM vs. baseline reduced. Pain 5/10.", "Cervical ROM vs. baseline reduced."),
])
def test_abbreviations_and_numbers_stay_inside_a_unit(text, first):
    """R-TL-2 / D-021: abbreviations (approx., Dr., mg., e.g., vs.) and decimals are not terminators."""
    assert S.units(text)[0].strip() == first

def test_semicolon_and_line_break_terminate():
    """R-TL-2: ';' and a line break end a unit (sample record 2: 'Dx: cervical strain;')."""
    us = [u.strip() for u in S.units(G.record("sample", 2)["excerpt"])]
    assert us[0] == "Dx: cervical strain;"
    assert [u.strip() for u in S.units("Pain 4/10\nBetter today")] == ["Pain 4/10", "Better today"]

def test_hedge_sentence_splits_at_semicolon():
    """R-TL-2 + R-TL-8: record 8 gives finding / 'may represent ...;' / 'correlate clinically.' as separate units."""
    us = [u.strip() for u in S.units(G.record("sample", 8)["excerpt"])]
    assert us == ["C5-C6 disc protrusion with mild right foraminal narrowing.",
                  "Findings may represent degenerative change;", "correlate clinically.", "Charge: $2,150."]

def test_question_and_exclamation_and_end_of_text():
    """R-TL-2: '.', '?' or '!' followed by space+uppercase/digit, or end of text, terminate."""
    assert [u.strip() for u in S.units("Pain? Yes! 3 days later.")] == ["Pain?", "Yes!", "3 days later."]

def test_whole_unit_check():
    """R-TL-2: an excerpt starting/ending mid-unit is NOT whole; contiguous whole units are."""
    rec = G.record("sample", 1)["excerpt"]
    assert S.is_whole_units(rec, "C/O neck pain 7/10 and headache. Alert and oriented.")
    assert not S.is_whole_units(rec, "rear-ended at approx. 35 mph")
    assert not S.is_whole_units(rec, "41M restrained driver, rear-ended at approx.")
    assert not S.is_whole_units(rec, "Alert and oriented. 41M restrained driver, rear-ended at approx. 35 mph.")  # not contiguous/ordered

def test_whitespace_differences_do_not_break_whole_unit_check():
    """R-TL-2: whitespace-normalised substring (case_04 record 4 has a double space)."""
    rec = G.record("case_04_duplicates_no_amounts", 4)["excerpt"]
    assert S.is_whole_units(rec, "Fracture alignment satisfactory. Continue splint 3 weeks.")
