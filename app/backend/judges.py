"""Judges J1-J4 (rung 2 of the validation ladder; LLM_VS_CODE rows 4, 7, 11, 12; ADR-003.8, ADR-008.5).
Each judge sees only the record text and the candidate (never the generator's reasoning), in nonce delimiters, and returns an
enum. A judge failure is "unavailable", never an exception into the pipeline; invalid output (out-of-enum, missing reason_code) is "unavailable", never positive.
`call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is supplied by the pipeline (audited_call bound to a case)."""
import os

from pydantic import ValidationError

from app.backend import injection, schemas
from app.llm import audited as AU, promptlib

DEFAULT_GENERATOR_MODEL = "claude-sonnet-5-5"
DEFAULT_JUDGE_MODEL = "claude-haiku-5-5"


def generator_model() -> str:
    return os.environ.get("GENERATOR_MODEL") or DEFAULT_GENERATOR_MODEL


def judge_model() -> str:
    return os.environ.get("JUDGE_MODEL") or DEFAULT_JUDGE_MODEL


def _run(step: str, prompt: str, model_cls, quotes: list, lines: list, call, nonce, item_id):
    """Returns (verdict, call_id, reason_code). verdict in the model's enum, or 'unavailable' / 'unsure'."""
    n = nonce or promptlib.nonce(step, *quotes, *[x if isinstance(x, str) else x[1] for x in lines])
    p = promptlib.load(prompt)
    blocks = "\n".join(f"{label}:\n{injection.wrap(q, n)}" for label, q in quotes_labelled(quotes, step))
    extra = "\n".join(f"{x[0]}:\n{injection.wrap(x[1], n)}" if isinstance(x, tuple) else x for x in lines)   # (name, text) = record-derived, wrapped
    user = blocks + "\n" + extra + "\nReturn the JSON object."
    try:
        out, call_id = call(step, p.text, user, model_cls.model_json_schema(), item_id=item_id)
    except AU.LLMFailed:
        return "unavailable", None, "NONE"
    try:
        m = model_cls.model_validate(out)
    except (ValidationError, TypeError, ValueError):
        return "unavailable", call_id, "NONE"   # invalid judge output (bad enum, missing reason_code) = judge did not answer
    return m.verdict, call_id, m.reason_code


def quotes_labelled(quotes: list, step: str):
    names = {"j3": ["QUOTE A", "QUOTE B"]}.get(step, ["RECORD TEXT"] * len(quotes))
    return zip(names, quotes)


def run_j1_meta(summary: str, excerpt: str, label: str, *, call, nonce=None, item_id=None):
    return _run("j1", "judge_faithfulness_v1", schemas.Judge1, [excerpt],
                [("SOURCE LABEL", label), f"CANDIDATE SUMMARY: {summary}"], call, nonce, item_id)


def run_j2_meta(excerpt: str, raw_amount: str, code_class: str, *, call, nonce=None, item_id=None):
    return _run("j2", "judge_amount_class_v1", schemas.Judge2, [excerpt],
                [f"AMOUNT: {raw_amount}", f"CLASS: {code_class}"], call, nonce, item_id)


def run_j3_meta(excerpt_a: str, excerpt_b: str, *, call, nonce=None, item_id=None, category=None):
    """`category` (the flag category the software proposed) selects the decision rule in judge_conflict_v6 (T-075, T-094)."""
    return _run("j3", "judge_conflict_v6", schemas.Judge3, [excerpt_a, excerpt_b], [f"FLAG CATEGORY: {category}"] if category else [],
                call, nonce, item_id)


def run_j4_meta(excerpt: str, flag_type: str, category: str, *, call, nonce=None, item_id=None):
    return _run("j4", "judge_flag_v3", schemas.Judge4, [excerpt],
                [f"FLAG TYPE: {flag_type}", f"FLAG CATEGORY: {category}"], call, nonce, item_id)


def run_j1(summary, excerpt, label, *, call, nonce=None, item_id=None):
    return run_j1_meta(summary, excerpt, label, call=call, nonce=nonce, item_id=item_id)[0]


def run_j2(excerpt, raw_amount, code_class, *, call, nonce=None, item_id=None):
    return run_j2_meta(excerpt, raw_amount, code_class, call=call, nonce=nonce, item_id=item_id)[0]


def run_j3(excerpt_a, excerpt_b, *, call, nonce=None, item_id=None, category=None):
    return run_j3_meta(excerpt_a, excerpt_b, call=call, nonce=nonce, item_id=item_id, category=category)[0]


def run_j4(excerpt, flag_type, category, *, call, nonce=None, item_id=None):
    return run_j4_meta(excerpt, flag_type, category, call=call, nonce=nonce, item_id=item_id)[0]


_TO_LADDER = {
    "j1": {"supported": "supported", "partially": "partially", "unsupported": "unsupported"},
    "j2": {"agree": "supported", "disagree": "disagrees", "unsure": "unsure"},
    "j3": {"conflict": "supported", "benign": "disagrees", "unsure": "unsure"},
    "j4": {"agree": "supported", "disagree": "disagrees", "unsure": "unsure"},
}


def to_ladder(step: str, verdict: str) -> str:
    """Map a judge's own enum to the compose_state vocabulary. Only the positive verdict becomes 'supported';
    unknown values become 'unsure' and 'unavailable' stays 'unavailable' (never positive by accident)."""
    if verdict == "unavailable":
        return "unavailable"
    return _TO_LADDER[step].get(verdict, "unsure")


def judge_amounts(items: list, *, call, case_text: str = "") -> dict:
    """Judge 2 on every amount, rule-made or not (R-CH-2, row 7). items: [{'id', 'raw', 'cls', 'excerpt'}].
    Returns {id: {'verdict', 'ladder', 'call_id', 'reason_code', 'fixture_miss', 'model', 'prompt_version'}}. FixtureMiss -> ladder 'unavailable' + fixture_miss True."""
    from app.llm import promptlib as _pl, provider as _P
    out = {}
    for it in items:
        n = _pl.nonce(case_text, "j2", it["id"])
        try:
            v, cid, code = run_j2_meta(it["excerpt"], it["raw"], it["cls"], call=call, nonce=n, item_id=it["id"])
            miss = False
        except _P.FixtureMiss:
            v, cid, code, miss = "unavailable", None, "NONE", True
        out[it["id"]] = {"verdict": v, "ladder": to_ladder("j2", v), "call_id": cid, "reason_code": code, "fixture_miss": miss,
                         "model": judge_model(), "prompt_version": "judge_amount_class_v1"}
    return out
