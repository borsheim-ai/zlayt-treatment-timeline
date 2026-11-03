"""LLM output schemas. R-TL-9 (no provider/date from the model), ADR-016, ADR-013 (no prose in flag schemas), LLM_VS_CODE rules 2 and 7."""
import pytest
from pydantic import ValidationError
from app.backend import schemas as S

def test_extract_output_accepts_summary_and_excerpt():
    """R-TL-4: the generator returns only a one-line summary and an exact excerpt."""
    o = S.ExtractOutput(summary="Pain 4/10.", excerpt="Pain 4/10, improving.")
    assert o.summary and o.excerpt

@pytest.mark.parametrize("extra", ["provider", "date", "dx", "diagnosis", "amount"])
def test_generator_schema_minimal(extra):
    """R-TL-9 / rule 2: the model may not supply provider, date, amount or clinical fields; extras are rejected."""
    with pytest.raises(ValidationError):
        S.ExtractOutput(summary="x", excerpt="y", **{extra: "z"})

def test_extract_output_requires_both_fields():
    """R-TL-4: missing excerpt or summary is SCHEMA_INVALID."""
    with pytest.raises(ValidationError):
        S.ExtractOutput(summary="x")

def test_generator_schema_properties_are_exactly_summary_and_excerpt():
    """T-035 AC1: the schema handed to the generator has exactly {summary, excerpt}."""
    assert set(S.ExtractOutput.model_json_schema()["properties"]) == {"summary", "excerpt"}

def test_json_schema_forbids_additional_properties():
    """ADR-004: the schema handed to the provider is closed (additionalProperties false)."""
    assert S.ExtractOutput.model_json_schema().get("additionalProperties") is False

@pytest.mark.parametrize("v", ["supported", "partially", "unsupported"])
def test_judge1_enum_ok(v):
    """LLM_VS_CODE row 4: judge 1 returns supported|partially|unsupported (+ a one-sentence reason)."""
    assert S.Judge1(verdict=v, reason_code="NONE").verdict == v

def test_judge_enum_rejects_other_values():
    """ADR-008.5: judges return an enum only."""
    with pytest.raises(ValidationError):
        S.Judge1(verdict="maybe", reason_code="NONE")

@pytest.mark.parametrize("model,v", [("Judge2", "agree"), ("Judge2", "disagree"), ("Judge2", "unsure"), ("Judge3", "conflict"), ("Judge3", "benign"), ("Judge3", "unsure"), ("Judge4", "agree"), ("Judge4", "disagree"), ("Judge4", "unsure")])
def test_other_judge_enums(model, v):
    """LLM_VS_CODE rows 7, 11, 12: judges 2-4 enums."""
    assert getattr(S, model)(verdict=v, reason_code="NONE").verdict == v

def test_flag_schema_no_prose():
    """ADR-013 / row 16: flag schema carries type, category, record_id and a quoted excerpt - no title/explanation/note field."""
    fields = set(S.FlagOutput.model_fields)
    assert {"type", "category", "excerpt"} <= fields
    assert not ({"title", "explanation", "note", "summary", "reason"} & fields)

def test_flag_type_closed_list():
    """ADR-013: flag types gap|conflict|pre_existing|causation only from the model (no 'gap' from LLM is allowed either)."""
    with pytest.raises(ValidationError):
        S.FlagOutput(type="fraud", category="x", excerpt="y")

@pytest.mark.parametrize("extra", ["title", "explanation", "note", "summary"])
def test_flag_schema_rejects_prose_fields(extra):
    """T-036 AC1 / R-FL-8: an extra or prose field on a flag output is rejected."""
    with pytest.raises(ValidationError):
        S.FlagOutput(type="pre_existing", category="pre_existing", excerpt="y", **{extra: "z"})
