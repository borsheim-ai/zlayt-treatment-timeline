"""compose_state table + why templates. R-TL-5, ADR-005, LLM_VS_CODE rows 17 and 18.

Ladder:  {"grounding_failures": [codes], "schema_valid": bool, "code_reasons": [codes], "judge": None|"supported"|"partially"|
          "unsupported"|"disagrees"|"unsure"|"unavailable"}
Context: {"injection": bool, "date_status": "parsed"|"confirmed"|"ambiguous"|"missing", "amount_class": None|"charge"|"rate"|
          "estimate"|"damages"|"unclear", "agreement": None|"both"|"lexicon_only"|"llm_only", "fixture_miss": bool,
          "split_ambiguous": bool, "llm_failed": bool, "endpoint_unverified": bool}
Returns (state, reasons). Precedence rejected > needs_review > verified.
"""
import pathlib, re
import pytest
from app.backend import confidence as C, why as W

OK = dict(grounding_failures=[], schema_valid=True, code_reasons=[], judge="supported")
CTX = dict(injection=False, date_status="parsed", amount_class=None, agreement=None, fixture_miss=False, split_ambiguous=False, llm_failed=False, endpoint_unverified=False)

def L(**kw):
    return {**OK, **kw}
def X(**kw):
    return {**CTX, **kw}

def test_all_clear_is_verified():
    """R-TL-5: every code check passed, judge positive, no context doubt -> verified with no reasons."""
    assert C.compose_state(L(), X()) == ("verified", [])

def test_no_judge_required_item_is_verified():
    """R-TL-5 / row 17: items without a judge (judge None) with clean checks are verified."""
    assert C.compose_state(L(judge=None), X()) == ("verified", [])

def test_confirmed_date_is_verified():
    """R-IN-5: a date the paralegal confirmed no longer needs review."""
    assert C.compose_state(L(), X(date_status="confirmed")) == ("verified", [])

@pytest.mark.parametrize("ladder,code", [
    (L(grounding_failures=["GROUNDING_EXCERPT_NOT_VERBATIM"]), "GROUNDING_EXCERPT_NOT_VERBATIM"),
    (L(grounding_failures=["GROUNDING_AMOUNT_NOT_IN_TEXT"]), "GROUNDING_AMOUNT_NOT_IN_TEXT"),
    (L(schema_valid=False), "SCHEMA_INVALID"),
])
def test_rejected_cases(ladder, code):
    """ADR-005: grounding failure or schema-invalid output -> rejected, reason listed."""
    st, rs = C.compose_state(ladder, X())
    assert st == "rejected" and code in rs

@pytest.mark.parametrize("ladder,ctx,code", [
    (L(code_reasons=["SUMMARY_TOKEN_NOT_IN_EXCERPT"]), X(), "SUMMARY_TOKEN_NOT_IN_EXCERPT"),
    (L(code_reasons=["SUMMARY_DROPS_QUALIFIER"]), X(), "SUMMARY_DROPS_QUALIFIER"),
    (L(code_reasons=["EXCERPT_OMITS_QUALIFIER"]), X(), "EXCERPT_OMITS_QUALIFIER"),
    (L(code_reasons=["EXCERPT_NOT_WHOLE_SENTENCE"]), X(), "EXCERPT_NOT_WHOLE_SENTENCE"),
    (L(code_reasons=["HIGHLIGHT_NOT_FOUND"]), X(), "HIGHLIGHT_NOT_FOUND"),
    (L(judge="partially"), X(), "JUDGE_PARTIAL"),
    (L(judge="unsupported"), X(), "JUDGE_UNSUPPORTED"),
    (L(judge="disagrees"), X(), "JUDGE_DISAGREES"),
    (L(judge="unsure"), X(), "JUDGE_UNSURE"),
    (L(judge="unavailable"), X(), "JUDGE_UNAVAILABLE"),
    (L(), X(fixture_miss=True), "FIXTURE_MISS"),
    (L(), X(date_status="ambiguous"), "DATE_AMBIGUOUS"),
    (L(), X(date_status="missing"), "DATE_MISSING"),
    (L(), X(amount_class="rate"), "AMOUNT_RATE_NOT_TOTALED"),
    (L(), X(amount_class="estimate"), "AMOUNT_ESTIMATE"),
    (L(), X(amount_class="damages"), "AMOUNT_DAMAGES"),
    (L(), X(amount_class="unclear"), "AMOUNT_UNCLEAR"),
    (L(), X(agreement="lexicon_only"), "LEXICON_ONLY"),
    (L(), X(agreement="llm_only"), "LLM_ONLY"),
    (L(), X(split_ambiguous=True), "SPLIT_AMBIGUOUS"),
    (L(), X(injection=True), "INJECTION_SUSPECTED"),
    (L(), X(endpoint_unverified=True), "ENDPOINT_NOT_VERIFIED"),   # R-FL-1: a gap whose span could contain an unconfirmed date
    (L(), X(llm_failed=True), "LLM_FAILED_AFTER_RETRIES"),
])
def test_needs_review_cases(ladder, ctx, code):
    """ADR-005 / R-TL-5: each doubt yields needs_review with its reason code."""
    st, rs = C.compose_state(ladder, ctx)
    assert st == "needs_review" and code in rs

def test_charge_amount_class_is_not_a_doubt():
    """R-CH-2: amount_class 'charge' adds no reason."""
    assert C.compose_state(L(), X(amount_class="charge")) == ("verified", [])

def test_agreement_both_is_not_a_doubt():
    """ADR-008.4: lexicon and model agree -> no LEXICON_ONLY / LLM_ONLY."""
    assert C.compose_state(L(), X(agreement="both")) == ("verified", [])

def test_rejected_beats_needs_review():
    """ADR-005 precedence: rejected > needs_review; the rejecting reason is kept."""
    st, rs = C.compose_state(L(grounding_failures=["GROUNDING_EXCERPT_NOT_VERBATIM"], judge="unsupported"), X(injection=True))
    assert st == "rejected" and "GROUNDING_EXCERPT_NOT_VERBATIM" in rs

def test_multiple_doubts_all_listed_once_each():
    """R-TL-5: several doubts -> needs_review with each reason exactly once."""
    st, rs = C.compose_state(L(judge="partially", code_reasons=["SUMMARY_DROPS_QUALIFIER"]), X(injection=True, date_status="ambiguous"))
    assert st == "needs_review"
    assert sorted(rs) == sorted(["JUDGE_PARTIAL", "SUMMARY_DROPS_QUALIFIER", "INJECTION_SUSPECTED", "DATE_AMBIGUOUS"])

def test_deterministic_and_pure():
    """Row 17: same ladder -> same state; inputs are not mutated."""
    l, c = L(judge="partially"), X(injection=True)
    l0, c0 = dict(l), dict(c)
    assert C.compose_state(l, c) == C.compose_state(l, c)
    assert l == l0 and c == c0

def test_context_optional():
    """Row 17: context may be omitted (treated as no doubt)."""
    assert C.compose_state(L()) == ("verified", [])

def test_unknown_code_is_a_bug():
    """Closed list: an unknown reason code raises instead of passing silently."""
    with pytest.raises((ValueError, KeyError)):
        C.compose_state(L(code_reasons=["MADE_UP_CODE"]), X())

# ---------- reason-code list and why templates (row 18)
def api_codes():
    t = (pathlib.Path(__file__).resolve().parents[2] / "memory/contracts/api.md").read_text()
    app = t.split("## Appendix: reason codes")[1]
    codes = set()
    for line in app.splitlines():
        if line.startswith("| `"):
            codes |= set(re.findall(r"`([A-Z][A-Z_]+)`", line.split("|")[1]))
    return codes

def test_reason_codes_match_api_appendix():
    """Row 18 / api.md appendix: confidence.REASON_CODES equals the closed list (22+ codes)."""
    assert set(C.REASON_CODES) == api_codes()
    assert len(api_codes()) >= 22

@pytest.mark.parametrize("code", sorted(api_codes()))
def test_every_reason_code_has_a_why_template(code):
    """Row 18: every reason code has a fixed, non-empty, plain-language template (no braces left over, no model text)."""
    s = W.why(code)
    assert isinstance(s, str) and 15 < len(s) < 300 and "{" not in s and "}" not in s

def test_why_unknown_code_raises():
    """Row 18: unknown code -> KeyError (templates are a closed list)."""
    with pytest.raises(KeyError):
        W.why("NOT_A_CODE")

def test_why_is_deterministic():
    """Row 18: same code -> byte-identical sentence."""
    assert W.why("JUDGE_PARTIAL") == W.why("JUDGE_PARTIAL")
