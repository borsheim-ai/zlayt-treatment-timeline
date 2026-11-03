"""T-037 additions (backend): CLI on the fixture backend, fixture replay completeness (0 FixtureMiss), eval-facing helpers, persistence.
Golden data only; no key, no network."""
import json
import os
import subprocess
import sys
import time
import pathlib
import pytest
from app.backend import pipeline as PL
from app.db import db as DB
from app.llm import provider as P
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]
FIX = ROOT / "tests" / "fixtures" / "llm"
needs_fixtures = pytest.mark.skipif(not list(FIX.glob("*.json")), reason="no recorded fixtures yet")


@needs_fixtures
def test_cli_sample_on_fixture_backend_under_60s():
    """T-037 AC1: `python -m app.pipeline evals/golden/sample.txt` prints 9 entries, the 73-day gap, $8,390 detected, exit 0, < 60 s."""
    t0 = time.time()
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "LLM_BACKEND")}
    p = subprocess.run([sys.executable, "-m", "app.pipeline", "evals/golden/sample.txt"], cwd=ROOT, env=env, capture_output=True, text=True, timeout=60)
    assert p.returncode == 0 and time.time() - t0 < 60, p.stderr[-500:]
    assert "entries: 9" in p.stdout and "Gap of 73 days" in p.stdout and "$8,390.00" in p.stdout and "ERRORS" not in p.stdout


def replay(case, tmp_path):
    """Run the whole pipeline on the fixture backend against a real DB; returns (output, llm_calls rows)."""
    conn = DB.connect(str(tmp_path / f"{case}.sqlite"))
    cid = DB.create_case(conn, G.raw(case), now=1.0)
    out = PL.run_pipeline(conn, cid, G.raw(case), now=lambda: 1.0)
    return out, DB.list_llm_calls(conn, cid)


@needs_fixtures
@pytest.mark.parametrize("case", ["sample"] + [c for c in G.case_names() if c != "sample"])
def test_replay_has_no_fixture_miss(case, monkeypatch, tmp_path):
    """T-037 AC2/AC7: replaying every golden input on the fixture backend makes 0 failed model calls (llm_calls rows with an error) and leaves no
    JUDGE_UNAVAILABLE / FIXTURE_MISS reason on any item. Fails when a fixture is missing or stale (a prompt changed since recording)."""
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    out, calls = replay(case, tmp_path)
    failed = [c for c in calls if c["error"]]
    assert not failed, f"{case}: {len(failed)} failed calls, steps {sorted({c['step'] for c in failed})}"
    assert out["errors"] == [] and out["status"] == "done"
    items = out["entries"] + out["undated_entries"] + out["amounts"] + out["flags"]
    assert not [i for i in items if {"FIXTURE_MISS", "JUDGE_UNAVAILABLE"} & set(i.get("reasons", []))], case


@needs_fixtures
def test_sample_replay_shows_verified_entries(monkeypatch, tmp_path):
    """The headline demo case replays with its entries verified (not all needs_review)."""
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    out, _ = replay("sample", tmp_path)
    assert len(out["entries"]) == 9 and sum(e["state"] == "verified" for e in out["entries"]) >= 7


@needs_fixtures
def test_injection_record_gets_exactly_one_record_warning(monkeypatch, tmp_path):
    """Review: stage 0 makes the record_warning flag; the per-record flag pass must not add a second one. case_07 -> one for record 3."""
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    out, _ = replay("case_07_prompt_injection", tmp_path)
    ws = [f for f in out["flags"] if f["type"] == "record_warning" and f["category"] == "injection_suspected"]
    assert [f["record_ids"] for f in ws] == [["r3"]]


def test_deadline_applies_inside_the_flags_stage(tmp_path):
    """Review minor: a clock that expires mid-flags-stage stops the remaining records; status is timeout and only finished flags are kept."""
    from tests.unit._fakes import FakeCall, sample_script
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    ticks = {"n": 0}

    def clock():                           # stays under the limit through the stage guards, then jumps past it once flags start
        ticks["n"] += 1
        return 0.0 if ticks["n"] < 12 else 1000.0
    call = FakeCall(sample_script())
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=clock, deadline_s=480)
    assert out["status"] == "timeout" and call.steps().count("flags") < 9


@needs_fixtures
def test_judge_lines_replay(monkeypatch):
    """T-037 AC2/AC6: every hallucination, control and seeded-edit line has a recorded judge-1 answer."""
    from app.llm import record
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    n = 0
    for name in ("hallucinations.jsonl", "hallucinations_controls.jsonl"):
        for line in (P.GOLDEN_DIR / name).read_text().splitlines():
            if line.strip():
                it = json.loads(line)
                label, excerpt = record._parse_record_text(it["record_text"])
                assert PL.judge_summary(it["candidate_summary"], excerpt, label, "fixture") != "unavailable", it["id"]
                n += 1
    assert n == 50


def test_fixtures_come_only_from_golden_text():
    """T-037 AC2: every fixture file is a recorded answer with provenance; the recorder refuses text outside evals/golden."""
    for f in FIX.glob("*.json"):
        d = json.loads(f.read_text())
        assert d["recorded_from"]["backend"] and "output" in d
    with pytest.raises(ValueError, match="evals/golden input"):
        P.assert_recordable("a patient who is not in the golden set")


def test_run_persists_items_pending_and_rerun_keeps_review_status(tmp_path):
    """ADR-002: the run writes entries/amounts/flags to the database, all pending; a decision made after the run survives a rerun."""
    from tests.unit._fakes import FakeCall, sample_script
    conn = DB.connect(str(tmp_path / "p.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 2.0)
    assert len(DB.list_items(conn, cid, "entry")) == 9 and len(DB.list_items(conn, cid, "amount")) == 4
    assert all(i["review_status"] == "pending" for k in ("entry", "amount", "flag") for i in DB.list_items(conn, cid, k))
    gap = [f for f in DB.list_items(conn, cid, "flag") if f["type"] == "gap"][0]
    DB.apply_review(conn, gap["id"], "accept", now=3.0)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 4.0)
    assert DB.get_item(conn, gap["id"])["review_status"] == "accepted"
    assert [f["review_status"] for f in out["flags"] if f["id"] == gap["id"]] == ["accepted"]
    assert DB.get_case(conn, cid)["status"] == "ready"


def test_timeout_marks_case_failed_with_run_deadline(tmp_path):
    from tests.unit._fakes import FakeCall, sample_script
    conn = DB.connect(str(tmp_path / "t.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    t = iter(range(0, 10**6, 100))
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: float(next(t)))
    c = DB.get_case(conn, cid)
    assert out["status"] == "timeout" and c["status"] == "failed" and json.loads(c["error"])["code"] == "run_deadline"
    assert [f for f in out["flags"] if f["type"] == "gap"]          # code results survive the deadline


def test_empty_and_oversize_raise_before_any_llm_call(tmp_path):
    """R-IN-4 through the pipeline entry point: nothing is called."""
    from tests.unit._fakes import FakeCall
    for bad in ("", "x" * 60001):
        conn = DB.connect(str(tmp_path / f"{len(bad)}.sqlite"))
        cid = DB.create_case(conn, bad or " ", now=0.0)
        call = FakeCall({})
        with pytest.raises(ValueError):
            PL.run_pipeline(conn, cid, bad, call=call)
        assert call.log == []


def test_endpoint_not_verified_and_every_flag_has_a_state():
    """T-037 AC8 / ADR-010: an undated encounter record that could sit inside a gap makes the gap flag needs_review (ENDPOINT_NOT_VERIFIED); every flag has a state."""
    t = ('Date: 2026-01-01\nSource: A Clinic, visit 1\nExcerpt: "Pain 5/10."\n---\nDate: 2026-03-01\nSource: A Clinic, visit 2\nExcerpt: "Pain 4/10."\n---\n'
         'Date: 02/04/2026\nSource: A Clinic, visit 3\nExcerpt: "Pain 3/10."')
    out = PL.run_ingest(t)
    gap = [f for f in out["flags"] if f["type"] == "gap"]
    assert len(gap) == 1 and gap[0]["state"] == "needs_review" and "ENDPOINT_NOT_VERIFIED" in gap[0]["reasons"]
    assert all(f["state"] in ("verified", "needs_review", "rejected") for f in out["flags"])
    sample = PL.run_ingest(G.raw("sample"))
    assert [f["state"] for f in sample["flags"] if f["type"] == "gap"] == ["verified"]
