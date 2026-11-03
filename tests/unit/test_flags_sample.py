"""Per-record flag pass + lexicon floor on the sample case. R-FL-3, R-FL-4, R-FL-5, R-FL-7, ADR-008.3/.4, ADR-013; fake `call` only."""
import pytest
from app.backend import flags as F
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, which_record

SAMPLE = G.records("sample")
GOLD = G.expected("sample")
MUST = [f for f in GOLD["flags"] if f["type"] in ("pre_existing", "causation") and f["level"] == "must"]

def rec(n):
    r = G.record("sample", n)
    return dict(n=n, source=r["source"], excerpt=r["excerpt"], date_iso=GOLD["records"][n - 1]["date"])

def covers(flags, g):
    """Reference overlap rule (golden README): some flag cites record g's record with evidence overlapping a golden evidence span."""
    spans = [e["excerpt"].lower() for e in g["evidence"] if e["record_no"] in g["cite"]["all"] and e.get("field", "excerpt") == "excerpt"]
    return any(any(s in f["excerpt"].lower() or f["excerpt"].lower() in s for s in spans) and f["type"] == g["type"] for f in flags)

def test_lexicon_alone_recovers_every_must_pre_existing_and_causation_flag():
    """ADR-008.4 / R-FL-3, R-FL-4: with the model returning nothing, the lexicon floor yields every golden must pre_existing/causation flag (recall 1.0)."""
    for g in MUST:
        n = g["cite"]["all"][0]
        flags = F.merge([], F.lexicon_flags(rec(n)), rec(n))
        assert covers(flags, g), g["id"]

def test_lexicon_only_flag_is_needs_review():
    """ADR-005 LEXICON_ONLY: a lexicon hit the model missed carries origin 'lexicon' and reason LEXICON_ONLY."""
    flags = F.merge([], F.lexicon_flags(rec(8)), rec(8))
    assert flags and all(f["origin"] == "lexicon" and "LEXICON_ONLY" in f["reasons"] for f in flags)

def test_llm_only_flag_is_needs_review():
    """ADR-005 LLM_ONLY: a model flag with no lexicon counterpart is LLM_ONLY."""
    llm = [dict(type="pre_existing", category="pre_existing", excerpt="Neck pain persists.")]
    out = F.merge(llm, [], rec(2))
    assert out and "LLM_ONLY" in out[0]["reasons"]

def test_both_agree_has_no_agreement_doubt():
    """ADR-005: when lexicon and model both flag the same span, origin is 'both' and neither doubt reason is present."""
    lex = F.lexicon_flags(rec(8))
    llm = [dict(type=f["type"], category=f["category"], excerpt=f["excerpt"]) for f in lex]
    out = F.merge(llm, lex, rec(8))
    assert out and all(f["origin"] == "both" and not {"LEXICON_ONLY", "LLM_ONLY"} & set(f["reasons"]) for f in out)

def test_flag_pass_is_one_call_per_record_and_isolated():
    """ADR-008.3 / D-021: nine records -> nine flag calls; each prompt contains only its own record's text."""
    call = FakeCall({"flags": {"flags": []}})
    for n in range(1, 10):
        F.run_flag_pass(rec(n), call=call)
    prompts = call.prompts("flags")
    assert len(prompts) == 9
    for n, p in zip(range(1, 10), prompts):
        assert which_record(p) == [n]
        assert p.count("<record-") == 1 and p.count("</record-") == 1     # T-036 AC4: exactly one nonce block

def test_patient_report_flag_has_no_speaker_chip():
    """D-040: the record-9 causation flag is a plain record flag (source_kind 'record')."""
    out = F.merge([], F.lexicon_flags(rec(9)), rec(9))
    k3 = [f for f in out if "Patient states symptoms began after the January collision" in f["excerpt"]]
    assert k3 and k3[0]["source_kind"] == "record"

def test_flag_titles_come_from_templates_not_model():
    """Row 16 / R-FL-5: the model schema has no prose; merged flags expose code-rendered title/explanation."""
    out = F.merge([], F.lexicon_flags(rec(8)), rec(8))
    assert all(f["title"] and f["explanation"] for f in out)

def test_evidence_is_verbatim_from_the_record():
    """R-FL-5: every flag excerpt is a verbatim substring of its record."""
    for n in range(1, 10):
        for f in F.merge([], F.lexicon_flags(rec(n)), rec(n)):
            assert f["excerpt"] in rec(n)["excerpt"]

@pytest.mark.parametrize("n", [1, 2, 4, 5])
def test_no_spurious_must_not_flags(n):
    """Golden must_not_flag: records 1, 2, 4, 5 carry no pre_existing flag from the floor."""
    assert not [f for f in F.merge([], F.lexicon_flags(rec(n)), rec(n)) if f["type"] == "pre_existing"]


def test_lexicon_floor_gives_distinct_one_to_one_matches_for_k1_to_k5():
    """T-036 AC2 / R-FL-3/4: pooled over the nine records, the lexicon floor's pre_existing + causation candidates satisfy ALL golden must flags under the one-to-one check_golden matcher (K4 and K5 need two distinct record-7 flags)."""
    from evals.matching import assign
    cands = []
    for n in range(1, 10):
        for f in F.merge([], F.lexicon_flags(rec(n)), rec(n)):
            cands.append(dict(type=f["type"], evidence=[dict(record_no=n, excerpt=f["excerpt"])]))
    got = assign(MUST, cands)
    assert got == {g["id"] for g in MUST} == {"P1", "P2", "K1", "K2", "K3", "K4", "K5"}
