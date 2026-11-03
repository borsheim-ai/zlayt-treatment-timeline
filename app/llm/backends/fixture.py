"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
import json
import os
import pathlib
import time

from app.llm._types import FixtureMiss, LLMError, LLMResult

DEFAULT_DIR = pathlib.Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "llm"


def fixture_dir() -> pathlib.Path:
    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
    if os.environ.get("LLM_FIXTURE_DIR"):
        return pathlib.Path(os.environ["LLM_FIXTURE_DIR"])
    name = os.environ.get("FIXTURE_SET", "").strip()
    return DEFAULT_DIR / name if name and name.isidentifier() else DEFAULT_DIR


def call(model: str, system: str, user: str, json_schema: dict, *, key: str) -> LLMResult:
    p = fixture_dir() / f"{key}.json"
    t0 = time.monotonic()
    if not p.is_file() and not os.environ.get("LLM_FIXTURE_DIR") and fixture_dir() != DEFAULT_DIR:
        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
    if not p.is_file():
        raise FixtureMiss(key)
    try:
        d = json.loads(p.read_text())
        out = d["output"]
    except (ValueError, KeyError, OSError):
        raise LLMError(f"FIXTURE_CORRUPT {key}") from None
    return LLMResult(output=out, backend="fixture", model_resolved=model, latency_ms=int((time.monotonic() - t0) * 1000),
                     raw=json.dumps(out), recorded_from=d.get("recorded_from") or {})


def write(key: str, result: LLMResult, model: str) -> pathlib.Path:
    """Record mode: store a live result keyed by the prompt hash, with provenance."""
    d = fixture_dir()
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{key}.json"
    rec = {"output": result.output,
           "recorded_from": {"backend": result.backend, "model": result.model_resolved or model,
                             "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
    p.write_text(json.dumps(rec, indent=1, sort_keys=True))
    return p


def answer_source() -> str:
    """D-065: `prepared` when the fixture set in use is the curated one (hand-checked answers, not model output), else `recorded` (a replay of real model answers)."""
    return "prepared" if fixture_dir().name == "curated" else "recorded"
