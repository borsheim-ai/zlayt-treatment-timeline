"""Audited call wrapper (ADR-003.7, ADR-004, LLM_VS_CODE row 20). The only entry point pipeline code uses.

1 attempt + 2 retries; every retry changes the request (stricter-format note in the user prompt); one llm_calls row per
attempt (prompt hash = sha256 of model+system+user+schema); a fixture miss is final. Never logs prompts, responses or error text.
"""
import contextlib
import logging
import os
import threading
import time

from app.db import db as DB
from app.llm import _types as T, provider as P

log = logging.getLogger("zlayt.llm")
MAX_ATTEMPTS = 3
LENIENT_JSON_STEPS = frozenset({"extract", "extract_es"})   # T-168 r2: the only steps whose reply may be read by its closing object; every judge and other step is strict
_DB_LOCK = threading.Lock()   # one sqlite3 connection is shared by the worker threads; its cursors are not safe to interleave
RETRY_DELAYS_S = (0.5, 1.5)
# Errors that are retried: the provider layer gave up (LLMError: timeout, backend failure, invalid JSON, schema-invalid) or the transport did
# (timeout, connection). Output that fails the caller's `validate` (ValueError) is retried too, but only from the validate step. Anything else
# (TypeError, KeyError, AttributeError ... a bug in our code) is logged as one row and propagates: retrying it three times hides it (T-073).
RETRYABLE_PROVIDER_ERRORS = (P.LLMError, TimeoutError, ConnectionError)
RETRYABLE_VALIDATION_ERRORS = (ValueError,)
_CODE = __import__('re').compile(r"^([A-Z][A-Z_]{2,40})\b")

_RETRY_NOTES = (
    "",
    "\n\n[RETRY 1 of 2: your previous reply was unusable. Reply with exactly one JSON object that satisfies the schema, with no prose and no code fence.]",
    "\n\n[FINAL RETRY: reply with ONLY the raw JSON object, no markdown, no commentary, every required key present, no extra keys.]",
)


class LLMFailed(Exception):
    """The LLM layer gave up (every attempt failed, or a fixture was missing). `last_error` is the last attempt's failure code
    (TIMEOUT, SCHEMA_INVALID, FIXTURE_MISS ...), so a caller can record why without keeping any record text."""
    code = "LLM_FAILED_AFTER_RETRIES"
    last_error = "LLM_ERROR"

    def __init__(self, *args, last_error: str = None):
        super().__init__(*args)
        if last_error:
            self.last_error = last_error


class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""

    last_error = "FIXTURE_MISS"

    def __init__(self, prompt_hash: str = ""):
        P.FixtureMissing.__init__(self, prompt_hash)


def _error_code(e: Exception) -> str:
    """Our own codes only (SCHEMA_INVALID, TIMEOUT, BACKEND_FAILED ...); anything else is reduced to the exception class."""
    if isinstance(e, P.LLMError):
        m = _CODE.match(str(e))
        return m.group(1) if m else "LLM_ERROR"
    return "VALIDATION_FAILED" if isinstance(e, ValueError) else type(e).__name__


def role_for(step: str) -> str:
    s = str(step)
    return "judge" if s.startswith("judge") or (len(s) == 2 and s[0] == "j" and s[1].isdigit()) else "generator"


PREPARED_BACKEND = "curated"      # D-065: recorded_from.backend of a hand-checked fixture (tests/fixtures/llm/curated); it is never model output


def is_prepared(recorded_from) -> bool:
    return isinstance(recorded_from, dict) and recorded_from.get("backend") == PREPARED_BACKEND


def answers_prepared() -> bool:
    """True when the fixture set in use is the curated (hand-checked) one and the backend is the fixture replay: an answer, or a missing answer, is then a prepared-answer matter, never a model's (D-065)."""
    from app.llm.backends import fixture
    return P.backend_name() == "fixture" and fixture.answer_source() == "prepared"


PREPARED_MODEL = "hand-checked (qa)"      # what a prepared answer, or the lack of one, names as its maker (D-065): no model was asked


def _prepared_model(res, step=None):
    """D-065: a curated answer's audit row names who made it (the fixture's own recorded_from.model, 'hand-checked (qa)'), never the model the pipeline asked for.
    D-069: under the curated set a generator step that got no usable answer asked no model either, so its row names the same maker."""
    if res is not None and is_prepared(res.recorded_from):
        return str(res.recorded_from.get("model") or PREPARED_MODEL)
    if res is None and step is not None and role_for(step) == "generator" and answers_prepared():
        return PREPARED_MODEL
    return None


def _t(now):
    return now() if callable(now) else (time.time() if now is None else now)


def audited_call(conn, case_id: str, step: str, model: str, system: str, user: str, json_schema: dict, *,
                 complete_with_meta=None, validate=None, item_id=None, now=None, prompt_version=None, sleep=None):
    cwm = complete_with_meta or P.complete_with_meta
    last_err = "unknown"
    for attempt in range(1, MAX_ATTEMPTS + 1):
        u = user + _RETRY_NOTES[attempt - 1]
        h = P.prompt_hash(model, system, u, json_schema)
        t0 = time.monotonic()
        res, err, fixture_miss, bug = None, None, False, None
        try:
            with (T.lenient_json() if step in LENIENT_JSON_STEPS else contextlib.nullcontext()):
                res = cwm(model, system, u, json_schema)
            if validate is not None:
                try:
                    validate(res.output)
                except RETRYABLE_VALIDATION_ERRORS as e:
                    err = _error_code(e)               # schema-invalid output: a failed attempt, retried with a stricter note
        except P.FixtureMissing as e:
            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
        except RETRYABLE_PROVIDER_ERRORS as e:          # only our own error codes are stored, never model- or record-derived text
            err = _error_code(e)
        except Exception as e:                         # a bug in our code: keep the row (class name only), then let it propagate below
            err, bug = _error_code(e), e
        if err is not None and bug is None and not fixture_miss and role_for(step) == "generator" and answers_prepared():
            err, fixture_miss = f"FIXTURE_MISS {h}", True      # D-069: a malformed or empty prepared answer is a missing one (same row, same outcome), never a model's failure and never retried
        ms = int((time.monotonic() - t0) * 1000)
        fields = dict(role=role_for(step), step=step, backend=(res.backend if res else P.backend_name()), model=(_prepared_model(res, step) or (res.model_resolved if res and res.model_resolved else model)),
                      prompt_version=prompt_version, prompt_sha256=h, attempt=attempt, latency_ms=(res.latency_ms if res and res.latency_ms else ms),
                      parsed_ok=1 if err is None else 0, error=err)
        if item_id:
            fields["item_id"] = item_id
        if res:
            import json as _j
            fields.update(cost_usd=res.cost_usd, tokens_in=res.tokens_in, tokens_out=res.tokens_out,
                          recorded_from_json=_j.dumps(res.recorded_from) if res.recorded_from else None)
        with _DB_LOCK:
            call_id = DB.add_llm_call(conn, case_id, u, (res.raw or _dump(res.output)) if res else None, now=_t(now), system=system, **fields)
        if err is None:
            return res.output, call_id
        if bug is not None:
            log.error("llm call raised a programmer error call_id=%s step=%s class=%s", call_id, step, type(bug).__name__)
            raise bug
        last_err = err
        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
        if fixture_miss:
            raise LLMFailedFixtureMiss(h)
        if sleep is not None and attempt < MAX_ATTEMPTS:
            sleep(RETRY_DELAYS_S[attempt - 1])         # short, capped, code-controlled
    raise LLMFailed(f"{step}: {MAX_ATTEMPTS} attempts failed", last_error=(last_err or "LLM_ERROR").split()[0])


def _dump(o):
    import json
    return json.dumps(o, sort_keys=True)


PROMPT_OF_STEP = {"extract": "extract_v1", "j1": "judge_faithfulness_v1", "j2": "judge_amount_class_v1", "j3": "judge_conflict_v6",
                  "j4": "judge_flag_v3", "flags": "flags_v1", "split": "split_v1", "narrative": "narrative_v1"}
PROMPT_OF_STEP.update({"extract_es": "extract_es_v1", "judge_faithfulness_es": "judge_faithfulness_es_v1"})     # Spanish records (D-042, T-085)


def make_call(conn, case_id: str, *, now=None, models: dict = None, schemas: dict = None):
    """Build the pipeline's `call(step, system, user, schema, *, item_id=None) -> (output, call_id)`.
    Model per role comes from GENERATOR_MODEL / JUDGE_MODEL (ADR-004) unless `models` overrides."""
    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}

    def call(step, system, user, schema, *, item_id=None, validate=None):
        # a live backend that just failed (rate limit, timeout) is retried after a short pause, not at once (T-075); the fixture backend never sleeps
        return audited_call(conn, case_id, step, m[role_for(step)], system, user, schema, item_id=item_id, now=now, validate=validate,
                            prompt_version=PROMPT_OF_STEP.get(step), sleep=None if P.backend_name() == "fixture" else time.sleep)
    return call
