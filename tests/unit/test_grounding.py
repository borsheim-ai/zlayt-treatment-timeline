"""Grounding verifier. R-TL-2, R-TL-8 (D-021), R-TL-10 (D-006/D-022), R-RV-9, LLM_VS_CODE rows 4, 9 rung 1."""
import re
import pytest
from app.backend import grounding as GR
from tests.unit import _golden as G

R8 = G.record("sample", 8)["excerpt"]
HEDGE_UNITS = "Findings may represent degenerative change; correlate clinically."
FINDING = "C5-C6 disc protrusion with mild right foraminal narrowing."

# ---------- excerpt checks (R-TL-2, R-TL-8)
def test_verbatim_whole_sentence_passes():
    """R-TL-2: a verbatim whole-sentence excerpt has no reasons (sample record 6)."""
    r = G.record("sample", 6)["excerpt"]
    assert GR.check_excerpt(r, "Discharged from PT after two missed appointments. Pain 3/10.") == []

def test_not_verbatim_is_rejected():
    """R-TL-2: model excerpt not in the record -> GROUNDING_EXCERPT_NOT_VERBATIM (rejected)."""
    assert GR.check_excerpt(R8, "C5-C6 disc herniation with mild right foraminal narrowing.") == ["GROUNDING_EXCERPT_NOT_VERBATIM"]

def test_whitespace_normalised_match():
    """R-TL-2: match is whitespace-normalised (extra spaces/newlines ignored)."""
    r = G.record("case_04_duplicates_no_amounts", 4)["excerpt"]
    assert GR.check_excerpt(r, "Fracture alignment satisfactory. Continue splint 3 weeks. No driving.") == []

def test_mid_sentence_excerpt_needs_review():
    """R-TL-2: starts/ends mid-unit -> EXCERPT_NOT_WHOLE_SENTENCE."""
    assert "EXCERPT_NOT_WHOLE_SENTENCE" in GR.check_excerpt(R8, "disc protrusion with mild right foraminal narrowing")

def test_entry8_without_hedge_needs_review():
    """R-TL-8: entry 8 excerpt without the hedge units -> EXCERPT_OMITS_QUALIFIER."""
    assert GR.check_excerpt(R8, FINDING) == ["EXCERPT_OMITS_QUALIFIER"]

def test_entry8_with_hedge_is_clean():
    """R-TL-8: finding + both hedge units -> no reasons."""
    assert GR.check_excerpt(R8, FINDING + " " + HEDGE_UNITS) == []

def test_entry8_with_half_the_hedge_still_omits():
    """R-TL-8 / D-021: 'correlate clinically.' is itself a hedge unit; dropping it still omits a qualifier."""
    assert GR.check_excerpt(R8, FINDING + " Findings may represent degenerative change;") == ["EXCERPT_OMITS_QUALIFIER"]

def test_non_hedge_lexicon_sentences_not_forced_into_excerpt():
    """R-TL-8 / D-021: entry 3 (prior-condition sentence) and entry 5 (damages sentence) stay clean."""
    assert GR.check_excerpt(G.record("sample", 3)["excerpt"], "Persistent neck pain 6/10, daily headaches.") == []
    assert GR.check_excerpt(G.record("sample", 5)["excerpt"], "Pain 4/10, improving.") == []

def test_entry6_default_excerpt_clean():
    """R-TL-8: record 6 has no hedge; entry 6 keeps 'after two missed appointments'."""
    assert GR.check_excerpt(G.record("sample", 6)["excerpt"], "Discharged from PT after two missed appointments.") == []

def test_hedge_set_loads_from_lexicon():
    """R-TL-8: hedge set comes from app/llm/lexicon.yaml (hedge: true) - non-empty, has may_represent and correlate_clinically."""
    import yaml, pathlib
    lex = yaml.safe_load((pathlib.Path(__file__).resolve().parents[2] / "app/llm/lexicon.yaml").read_text())
    entries = lex["entries"] if isinstance(lex, dict) and "entries" in lex else lex
    ids = {e["id"] for e in entries if isinstance(e, dict) and e.get("hedge")}
    assert {"may_represent", "correlate_clinically"} <= ids

# ---------- offsets (R-RV-9)
@pytest.mark.parametrize("case", G.case_names())
def test_offset_round_trip_for_every_unit_run(case):
    """R-RV-9: locate() returns (start,end) with record[start:end] == excerpt (whitespace-normalised) for every whole-sentence excerpt."""
    from app.backend import sentences as S
    for rec in G.records(case):
        text = rec["excerpt"]
        us = S.units(text)
        for i in range(len(us)):
            ex = us[i].strip()
            span = GR.locate(text, ex)
            assert span is not None
            assert GR.normalize(text[span[0]:span[1]]) == GR.normalize(ex)

def test_locate_handles_double_space_in_raw():
    """R-RV-9: excerpt collapsed to single spaces still maps to the raw slice with the double space."""
    t = G.record("case_04_duplicates_no_amounts", 4)["excerpt"]
    s, e = GR.locate(t, "Fracture alignment satisfactory. Continue splint 3 weeks.")
    assert "  " in t[s:e]

def test_locate_mutated_record_returns_none():
    """R-RV-9: mutated record -> offset lookup fails -> None (item drops to needs_review HIGHLIGHT_NOT_FOUND)."""
    assert GR.locate(R8.replace("mild", "severe"), FINDING) is None

# ---------- summary checks (R-TL-10, D-022)
def codes(summary, excerpt, label="", date=""):
    return GR.check_summary(summary, excerpt, label, date)

def test_sample_summary_with_label_digit_passes():
    """R-TL-10: 'Visit 8: pain 4/10, improving.' passes; '8' comes from the source label 'Capital PT, visit 8'."""
    assert codes("Visit 8: pain 4/10, improving.", "Pain 4/10, improving.", "Capital PT, visit 8", "2026-02-20") == []

def test_changed_pain_score_flags():
    """R-TL-10: summary 'pain 3/10' with excerpt 'Pain 4/10.' -> SUMMARY_TOKEN_NOT_IN_EXCERPT."""
    assert codes("Pain 3/10.", "Pain 4/10, improving.") == ["SUMMARY_TOKEN_NOT_IN_EXCERPT"]

def test_added_dollar_flags():
    """R-TL-10 / R-RV-3: summary edited to add '$9,000' -> token reason."""
    assert "SUMMARY_TOKEN_NOT_IN_EXCERPT" in codes("Visit 8: pain 4/10, improving; billed $9,000.", "Pain 4/10, improving.", "Capital PT, visit 8", "2026-02-20")

def test_added_date_flags():
    """R-TL-10: a date absent from the excerpt, label and parsed date is flagged."""
    assert "SUMMARY_TOKEN_NOT_IN_EXCERPT" in codes("Seen on March 3, 2026 with pain 4/10.", "Pain 4/10, improving.", "Capital PT, visit 8", "2026-02-20")

def test_parsed_date_digits_allowed():
    """R-TL-10: the record's parsed date (year/month/day) may appear in the summary."""
    assert codes("On February 20, 2026 pain 4/10.", "Pain 4/10, improving.", "Capital PT, visit 8", "2026-02-20") == []

@pytest.mark.parametrize("word", ["left", "right", "no", "not", "without"])
def test_direction_and_negation_words_must_be_in_quote(word):
    """R-TL-10 (api.md SUMMARY_TOKEN_NOT_IN_EXCERPT): left/right/no/not/without in the summary but not in the quote is flagged."""
    assert "SUMMARY_TOKEN_NOT_IN_EXCERPT" in codes(f"Pain 4/10 {word} improving.", "Pain 4/10, improving.")

def test_masked_pain_score_is_invisible_to_code():
    """R-RV-3 / SE5: 'pain 8/10' reuses digits allowed by the label 'visit 8' -> the digit-token code check is blind (judge #1 must catch it)."""
    assert codes("Visit 8: pain 8/10, improving.", "Pain 4/10, improving.", "Capital PT, visit 8", "2026-02-20") == []

@pytest.mark.parametrize("summary,excerpt", [
    ("Cervical strain and concussion; CT head negative.", "Dx: cervical strain; concussion without loss of consciousness. CT head negative."),
    ("C5-C6 disc protrusion with mild right foraminal narrowing.", FINDING + " " + HEDGE_UNITS),
    ("Neck pain 7/10 and headache.", "C/O neck pain 7/10 and headache."),
    ("Rear-ended at 35 mph.", "41M restrained driver, rear-ended at approx. 35 mph."),
    ("Symptoms began after the January collision.", "Patient states symptoms began after the January collision."),
])
def test_dropped_qualifier_flags(summary, excerpt):
    """R-TL-10(b)/D-022: summary omits a negation / hedge / self-report marker / 'approx.' the excerpt carries -> SUMMARY_DROPS_QUALIFIER."""
    assert "SUMMARY_DROPS_QUALIFIER" in codes(summary, excerpt)

def test_every_golden_export_summary_passes_code_checks():
    """R-TL-10 / R-EX-6: all 9 summaries in sample.export.expected.txt pass check_summary against their own quote, label and date."""
    letter, _ = G.export_blocks()
    from datetime import datetime
    recs = {(r["source"]): r for r in G.records("sample")}
    n = 0
    for blk in letter.split("BILLED CHARGES")[0].strip().split("\n\n")[1:]:
        h, summ, src = blk.split("\n")
        m = re.match(r"([A-Z][a-z]+ \d+, \d{4}) — (.+)$", h)
        quote = re.search(r'"(.+)"', src).group(1)
        iso = datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        assert GR.check_summary(summ, quote, m.group(2), iso) == [], summ
        n += 1
    assert n == 9

def test_seeded_edits_from_golden():
    """R-RV-3: sample seeded_edits - number edits flag in code; control passes; judge-only edits are not a code reason."""
    ex = G.expected("sample")
    rec = {r["record_no"]: r for r in ex["records"]}
    for se in ex["seeded_edits"]:
        r = G.record("sample", se["record_no"]); row = rec[se["record_no"]]
        out = GR.check_summary(se["new_summary"], "Pain 4/10, improving." if se["record_no"] == 5 else r["excerpt"], row["source"], row["date"])
        if se["kind"] == "number":
            assert "SUMMARY_TOKEN_NOT_IN_EXCERPT" in out, se["id"]
        if se["kind"] == "control":
            assert out == [], se["id"]


# ---------- amount grounding (checklist 4, api.md GROUNDING_AMOUNT_NOT_IN_TEXT)
def test_amount_present_in_record_passes():
    """R-CH-1: '$6,240' is in sample record 2 -> no reason."""
    assert GR.check_amount(G.record("sample", 2)["excerpt"], "$6,240") == []

@pytest.mark.parametrize("raw", ["$6,420", "$9,000", "$62,400"])
def test_amount_absent_from_record_is_rejected(raw):
    """R-CH-1 / row 6: an amount the record does not contain -> GROUNDING_AMOUNT_NOT_IN_TEXT (rejected)."""
    assert GR.check_amount(G.record("sample", 2)["excerpt"], raw) == ["GROUNDING_AMOUNT_NOT_IN_TEXT"]

def test_noisy_amount_not_autocorrected():
    """R-CH-1: '$1,2OO' (case_03) is found as written; the corrected '$1,200' is NOT in the text and is rejected."""
    t = G.record("case_03_rate_and_ocr", 2)["excerpt"]
    assert GR.check_amount(t, "$1,2OO") == [] and GR.check_amount(t, "$1,200") == ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
