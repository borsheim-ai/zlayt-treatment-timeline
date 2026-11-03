"""Integrity of the curated fixture set (D-029; T-115 round 2).

Rule: a CURATED answer may stand in for a generator/narrative response (it reproduces the golden letter byte for byte), but a JUDGE answer
(any output with a "verdict") must be a real recorded model answer. So in tests/fixtures/llm/curated/:
  1. no judge file may exist under the same key as a recording in tests/fixtures/llm/ (it would shadow what the model really said; the
     fixture backend reads curated first), and
  2. no judge file may exist without a recorded counterpart,
unless the key is on JUDGE_ALLOW_LIST below with a documented reason. The list is empty on purpose: every judge answer is recorded
(claude-cli, claude-haiku-5-5) and tests/fixtures/make_curated.py writes none. Adding an entry needs a card and a DECISIONS/ASSUMPTIONS note.
"""
import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
RECORDED = ROOT / "tests" / "fixtures" / "llm"
CURATED = RECORDED / "curated"

# key (full sha256) -> reason it may be a curated judge answer with no recorded counterpart. Keep empty.
JUDGE_ALLOW_LIST: dict = {}


def _is_judge(path: pathlib.Path) -> bool:
    out = json.loads(path.read_text()).get("output")
    return isinstance(out, dict) and "verdict" in out


def judge_problems(curated: pathlib.Path, recorded: pathlib.Path, allow: dict) -> list:
    """Human-readable problems for the curated dir: shadowed recordings, and curated judge answers with no recording (not allow-listed)."""
    problems = []
    for p in sorted(curated.glob("*.json")):
        if not _is_judge(p):
            continue
        key = p.stem
        if (recorded / p.name).is_file():
            problems.append(f"SHADOWS_RECORDING {key[:12]}: curated judge answer overrides the recorded model answer")
        elif key not in allow:
            problems.append(f"SCRIPTED_JUDGE {key[:12]}: curated judge answer with no recorded counterpart and not on the allow-list")
    return problems


def _write(d: pathlib.Path, key: str, output: dict):
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{key}.json").write_text(json.dumps({"output": output, "recorded_from": {"backend": "x", "model": "m", "recorded_at": "t"}}))


JUDGE_OUT = {"verdict": "supported", "reason_code": "NONE"}


def test_shipped_curated_set_has_no_shadowing_or_scripted_judge_answers():
    assert CURATED.is_dir() and any(CURATED.glob("*.json"))
    assert judge_problems(CURATED, RECORDED, JUDGE_ALLOW_LIST) == []


def test_allow_list_entries_are_documented_and_still_needed():
    for key, reason in JUDGE_ALLOW_LIST.items():
        assert isinstance(reason, str) and len(reason) >= 20, f"{key[:12]}: the allow-list needs a written reason"
        p = CURATED / f"{key}.json"
        assert p.is_file() and _is_judge(p), f"{key[:12]}: allow-listed key is not a curated judge file; remove it"
        assert not (RECORDED / p.name).is_file(), f"{key[:12]}: now recorded; remove it from the allow-list and the curated file"


def test_detector_fails_when_curated_judge_shadows_a_recording(tmp_path):
    cur, rec = tmp_path / "curated", tmp_path
    _write(rec, "a" * 64, JUDGE_OUT)
    _write(cur, "a" * 64, {"verdict": "supported", "reason_code": "ADDS_CAUSATION"})
    assert [p.split()[0] for p in judge_problems(cur, rec, {})] == ["SHADOWS_RECORDING"]
    assert [p.split()[0] for p in judge_problems(cur, rec, {"a" * 64: "allow-listing must not hide a shadow of a recording"})] == ["SHADOWS_RECORDING"]


def test_detector_fails_on_scripted_judge_without_recording_unless_allow_listed(tmp_path):
    cur, rec = tmp_path / "curated", tmp_path
    _write(cur, "b" * 64, JUDGE_OUT)
    assert [p.split()[0] for p in judge_problems(cur, rec, {})] == ["SCRIPTED_JUDGE"]
    assert judge_problems(cur, rec, {"b" * 64: "documented: no live model available for this prompt"}) == []


def test_detector_ignores_non_judge_curated_answers(tmp_path):
    cur, rec = tmp_path / "curated", tmp_path
    _write(cur, "c" * 64, {"summary": "s", "excerpt": "e"})
    _write(rec, "c" * 64, {"summary": "other", "excerpt": "e"})
    assert judge_problems(cur, rec, {}) == []


def test_make_curated_check_is_current():
    """The curated set must still replay to the golden letter and notes at this HEAD (a prompt change re-keys judge prompts and
    leaves the set stale; the failure then names the missing keys). Runs in a subprocess because the check edits os.environ."""
    r = subprocess.run([sys.executable, str(ROOT / "tests" / "fixtures" / "make_curated.py"), "--check"], cwd=ROOT, capture_output=True,
                       text=True, timeout=240, env={**__import__("os").environ, "LLM_BACKEND": "fixture", "ENABLE_LIVE": "0"})
    assert r.returncode == 0, (r.stdout[-1500:] + r.stderr[-1500:])
    assert "letter equal: True | notes equal: True" in r.stdout
