"""Shared provider types, JSON parsing and a small JSON-Schema checker (no jsonschema dependency). ADR-004."""
import contextlib
import contextvars
import json
import re
from dataclasses import dataclass, field


class LLMError(Exception):
    """Timeout, backend failure, invalid JSON or schema-invalid output. Messages must never contain record text."""


class FixtureMissing(LLMError):
    """No recorded answer for this prompt hash. Never retried, never answered with a default."""

    def __init__(self, prompt_hash: str = ""):
        super().__init__(f"FIXTURE_MISS {prompt_hash}")
        self.prompt_hash = prompt_hash


FixtureMiss = FixtureMissing   # old spelling, kept as an alias


@dataclass
class LLMResult:
    output: dict
    backend: str = "fixture"
    model_resolved: str = ""
    latency_ms: int = 0
    cost_usd: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    raw: str = ""
    recorded_from: dict = field(default_factory=dict)


_FENCE = re.compile(r"^```(?:json)?\s*\n(.*)\n```\Z", re.S)

# T-168 r2: the lenient "take the closing object" read is OPT-IN and belongs to the extract call only (audited_call turns it on for the extract
# steps). A contextvar, not a parameter, so the 4-argument complete_with_meta seam (and every fake of it) is unchanged; it is per thread/context,
# set and reset around exactly one provider call, and defaults to off.
_LENIENT = contextvars.ContextVar("lenient_json_reply", default=False)


@contextlib.contextmanager
def lenient_json():
    """Within this block parse_json_reply may take the closing object of a reply that drafted, said 'Wait', and corrected itself. Extract call only."""
    tok = _LENIENT.set(True)
    try:
        yield
    finally:
        _LENIENT.reset(tok)


def lenient_json_enabled() -> bool:
    return _LENIENT.get()


def parse_json_reply(text: str, *, lenient: bool = None) -> dict:
    """STRICT by default: the reply must be exactly one JSON object, bare or in one ```json fence; anything else (a second object, prose, a
    truncated object) is LLMError INVALID_JSON. Every judge (j1-j4) and every non-extract step parses this way: a reply holding two objects with
    different verdicts is a judge that is unavailable, never a silent choice of the later one.
    lenient=True (or inside `with lenient_json():`, which the extract call alone uses) also accepts a reply that drafts an object, thinks aloud, and
    ends with its corrected object; see _closing_object for exactly what counts."""
    t = (text or "").strip()
    m = _FENCE.match(t)
    if m:
        t = m.group(1).strip()
    try:
        obj = json.loads(t)
    except (ValueError, TypeError):
        obj = _closing_object(t) if (_LENIENT.get() if lenient is None else lenient) else None
        if obj is None:
            raise LLMError("INVALID_JSON: reply is not a single JSON object") from None
    if not isinstance(obj, dict):
        raise LLMError("INVALID_JSON: reply is not a JSON object")
    return obj


def _closing_object(t: str):
    """Lenient (extract-only) read, T-168: a reply that thinks aloud and then states its final answer ("{...} Wait, that is wrong. Corrected output: {...}")
    ends with one JSON object. That closing object is the answer; earlier complete objects are the model's own discarded drafts. Rules:
      - scan left to right; a complete object that does not end the reply is skipped whole (its inner braces are never tried);
      - a '{' that is not valid JSON in the middle of prose ("Wait {see above}") is skipped;
      - a '{' whose object runs out of text (truncated reply, or a cut-off closing object) ends the scan: INVALID_JSON, no inner object is salvaged;
      - the answer is an object that runs to the very end of the reply; trailing prose after it, or a non-object, is INVALID_JSON.
    Schema, grounding and the judges still check what comes out. Never used for a judge."""
    dec = json.JSONDecoder()
    i = t.find("{")
    while i != -1:
        try:
            obj, end = dec.raw_decode(t, i)
        except json.JSONDecodeError as e:
            if e.pos >= len(t):          # ran out of text: an unterminated object, not a stray brace
                return None
            i = t.find("{", i + 1)
            continue
        if isinstance(obj, dict) and end == len(t):
            return obj
        i = t.find("{", end)
    return None


_ANNOTATIONS = {"title", "description", "default", "examples", "$schema", "$id", "$defs", "definitions", "format"}
_KEYWORDS = _ANNOTATIONS | {"type", "enum", "const", "required", "properties", "additionalProperties", "items", "$ref", "anyOf",
                            "maxLength", "minLength", "maximum", "minimum", "maxItems", "minItems"}


def _type_ok(v, x):
    if x == "object":
        return isinstance(v, dict)
    if x == "array":
        return isinstance(v, list)
    if x == "string":
        return isinstance(v, str)
    if x == "boolean":
        return isinstance(v, bool)
    if x == "null":
        return v is None
    if x == "integer":
        return isinstance(v, int) and not isinstance(v, bool)
    if x == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    raise LLMError(f"SCHEMA_UNSUPPORTED type {str(x)[:20]}")


def _check(v, s, path, root):
    """Fail closed: a schema keyword outside _KEYWORDS raises LLMError instead of being silently ignored."""
    if s is True or s == {}:
        return
    bad = set(s) - _KEYWORDS
    if bad:
        raise LLMError(f"SCHEMA_UNSUPPORTED keyword {sorted(bad)}")
    if "$ref" in s:
        ref = s["$ref"]
        if not ref.startswith("#/") or ref.count("/") != 2:
            raise LLMError("SCHEMA_UNSUPPORTED $ref")
        target = (root.get(ref.split("/")[1]) or {}).get(ref.split("/")[2])
        if target is None:
            raise LLMError("SCHEMA_UNSUPPORTED $ref target")
        return _check(v, target, path, root)
    if "anyOf" in s:
        errs = 0
        for sub in s["anyOf"]:
            try:
                _check(v, sub, path, root)
            except ValueError:
                errs += 1
        if errs == len(s["anyOf"]):
            raise ValueError(f"{path or '$'}: matches no anyOf branch")
    t = s.get("type")
    if t:
        ts = t if isinstance(t, list) else [t]
        if not any(_type_ok(v, x) for x in ts):
            raise ValueError(f"{path or '$'}: expected {t}")
    if "enum" in s and v not in s["enum"]:
        raise ValueError(f"{path or '$'}: not in enum")
    if "const" in s and v != s["const"]:
        raise ValueError(f"{path or '$'}: not const")
    if isinstance(v, str):
        if "maxLength" in s and len(v) > s["maxLength"]:
            raise ValueError(f"{path or '$'}: too long")
        if "minLength" in s and len(v) < s["minLength"]:
            raise ValueError(f"{path or '$'}: too short")
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if "maximum" in s and v > s["maximum"]:
            raise ValueError(f"{path or '$'}: above maximum")
        if "minimum" in s and v < s["minimum"]:
            raise ValueError(f"{path or '$'}: below minimum")
    if isinstance(v, dict):
        props = s.get("properties", {})
        for r in s.get("required", []):
            if r not in v:
                raise ValueError(f"{path or '$'}: missing {r}")
        ap = s.get("additionalProperties")
        if ap is False and set(v) - set(props):
            raise ValueError(f"{path or '$'}: unexpected key")      # key names are model output: not echoed
        for k, sub in props.items():
            if k in v:
                _check(v[k], sub, f"{path}.{k}", root)
        if isinstance(ap, dict):
            for k in set(v) - set(props):
                _check(v[k], ap, f"{path}.*", root)
    if isinstance(v, list):
        if "maxItems" in s and len(v) > s["maxItems"]:
            raise ValueError(f"{path or '$'}: too many items")
        if "minItems" in s and len(v) < s["minItems"]:
            raise ValueError(f"{path or '$'}: too few items")
        if "items" in s:
            for i, x in enumerate(v):
                _check(x, s["items"], f"{path}[{i}]", root)


def validate_schema(output, schema: dict) -> None:
    """Raise LLMError if output does not satisfy the schema (supported subset; anything else is refused)."""
    root = {"$defs": (schema or {}).get("$defs", {}), "definitions": (schema or {}).get("definitions", {})}
    try:
        _check(output, schema or {}, "", root)
    except ValueError as e:
        raise LLMError(f"SCHEMA_INVALID {e}") from None
