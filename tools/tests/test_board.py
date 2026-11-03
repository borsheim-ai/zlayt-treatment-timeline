"""Harness tests for tools/board.py (M0 smoke test §4.8.1). Run: .venv/bin/python -m pytest tools/tests -q"""
import json, os, subprocess, sys, threading
from pathlib import Path
import pytest

BOARD = Path(__file__).resolve().parents[1] / "board.py"


def run(root, *args):
    env = dict(os.environ, BOARD_ROOT=str(root))
    return subprocess.run([sys.executable, str(BOARD), *args], capture_output=True, text=True, env=env)


@pytest.fixture
def root(tmp_path):
    (tmp_path / "reviews").mkdir()
    assert run(tmp_path, "init").returncode == 0
    return tmp_path


def new(root, **kw):
    r = run(root, "new", "--title", kw.get("title", "t"), "--milestone", "M0", "--role", "backend", "--ac", "a1", "--ac", "a2")
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def write_review(root, cid, verdict="pass", findings=None):
    p = root / "reviews" / f"{cid}-staff-engineer.md"
    d = {"card": cid, "persona": "staff-engineer-reviewer", "verdict": verdict, "exercised": ["ran tests"],
         "findings": findings or []}
    p.write_text("# review\n```json\n" + json.dumps(d) + "\n```\n")
    return str(p.relative_to(root))


def test_round_trip(root):
    cid = new(root)
    assert run(root, "claim", cid, "--agent", "backend").returncode == 0
    assert run(root, "note", cid, "--agent", "backend", "--text", "working").returncode == 0
    assert run(root, "ac", cid, "--agent", "backend", "--check", "1", "--evidence", "tests/x.py::t1 passes").returncode == 0
    assert run(root, "ac", cid, "--agent", "backend", "--check", "2", "--evidence", "tests/x.py::t2 passes").returncode == 0
    assert run(root, "move", cid, "in_review", "--agent", "backend").returncode != 0  # empty handoff
    assert run(root, "handoff", cid, "--agent", "backend", "--text", "changed x; verified y").returncode == 0
    assert run(root, "move", cid, "in_review", "--agent", "backend").returncode == 0
    f = write_review(root, cid)
    assert run(root, "review", cid, "--persona", "staff-engineer-reviewer", "--model", "claude-sonnet-5-5", "--verdict", "pass", "--file", f).returncode == 0
    r = run(root, "move", cid, "done", "--agent", "backend")
    assert r.returncode != 0 and "self-approval" in r.stderr
    assert run(root, "move", cid, "done", "--agent", "orchestrator").returncode == 0
    assert "done" in run(root, "show", cid).stdout


def test_illegal_transition_refused(root):
    cid = new(root)
    r = run(root, "move", cid, "done", "--agent", "orchestrator")
    assert r.returncode == 2 and "illegal transition" in r.stderr


def test_done_requires_review_and_ac(root):
    cid = new(root)
    run(root, "claim", cid, "--agent", "backend")
    run(root, "handoff", cid, "--agent", "backend", "--text", "h")
    assert run(root, "move", cid, "in_review", "--agent", "backend", "--note", "AC pending").returncode == 0
    r = run(root, "move", cid, "done", "--agent", "orchestrator")
    assert r.returncode == 2 and "AC" in r.stderr


def test_changes_verdict_requeues(root):
    cid = new(root)
    run(root, "claim", cid, "--agent", "backend")
    run(root, "handoff", cid, "--agent", "backend", "--text", "h")
    run(root, "move", cid, "in_review", "--agent", "backend", "--note", "x")
    f = write_review(root, cid, "changes", [{"severity": "major", "title": "bug", "evidence": "a.py:1", "fix": "fix it"}])
    assert run(root, "review", cid, "--persona", "staff-engineer-reviewer", "--model", "m", "--verdict", "changes", "--file", f).returncode == 0
    out = run(root, "show", cid).stdout
    assert '"changes_requested"' in out and "rounds: 1" in out and "fix it" in out
    assert run(root, "next", "--role", "backend").stdout.startswith(cid)
    assert run(root, "claim", cid, "--agent", "backend").returncode == 0


def test_validate_catches_bad_card_and_out_of_band_status(root):
    cid = new(root)
    p = root / "board" / "cards" / f"{cid}.md"
    p.write_text(p.read_text().replace('status: "ready"', 'status: "done"'))
    r = run(root, "validate", str(p))
    assert r.returncode == 2 and "outside board.py" in r.stderr
    p.write_text("no frontmatter")
    assert run(root, "validate", str(p)).returncode == 2


def test_validate_review_schema(root):
    cid = new(root)
    f = write_review(root, cid, "pass", [{"severity": "major", "title": "x", "evidence": "y"}])
    r = run(root, "validate", str(root / f))
    assert r.returncode == 2 and "requires verdict 'changes'" in r.stderr


def test_concurrent_claims(root):
    cid = new(root)
    results = []
    def go(n):
        results.append(run(root, "claim", cid, "--agent", f"w{n}").returncode)
    ts = [threading.Thread(target=go, args=(i,)) for i in range(6)]
    [t.start() for t in ts]; [t.join() for t in ts]
    assert results.count(0) == 1


def test_status_json(root):
    new(root)
    s = json.loads(run(root, "status", "--json").stdout)
    assert s["ready_unclaimed"] == 1 and s["done_definition_met"] is False


def test_assign_and_dispatch_silence_actionable(root):
    cid = new(root)
    s = json.loads(run(root, "status", "--json").stdout)
    assert s["ready_unclaimed"] == 1
    assert run(root, "assign", cid, "--to", "backend-1").returncode == 0
    s = json.loads(run(root, "status", "--json").stdout)
    assert s["ready_unclaimed"] == 0
    run(root, "claim", cid, "--agent", "backend")
    run(root, "handoff", cid, "--agent", "backend", "--text", "h")
    run(root, "move", cid, "in_review", "--agent", "backend", "--note", "x")
    assert json.loads(run(root, "status", "--json").stdout)["in_review"] == 1
    assert run(root, "dispatch", cid, "--personas", "staff-engineer").returncode == 0
    s = json.loads(run(root, "status", "--json").stdout)
    assert s["in_review"] == 0 and s["in_review_total"] == 1


def test_review_must_match_file(root):
    cid = new(root)
    run(root, "claim", cid, "--agent", "backend")
    run(root, "handoff", cid, "--agent", "backend", "--text", "h")
    run(root, "move", cid, "in_review", "--agent", "backend", "--note", "x")
    f = write_review(root, cid, "changes", [{"severity": "major", "title": "b", "evidence": "e"}])
    r = run(root, "review", cid, "--persona", "staff-engineer-reviewer", "--model", "m", "--verdict", "pass", "--file", f)
    assert r.returncode == 2 and "does not match" in r.stderr
    junk = root / "reviews" / "junk.md"; junk.write_text("nothing")
    r = run(root, "review", cid, "--persona", "x", "--model", "m", "--verdict", "pass", "--file", "reviews/junk.md")
    assert r.returncode == 2


def test_out_of_band_status_survives_next_write(root):
    cid = new(root)
    p = root / "board" / "cards" / f"{cid}.md"
    p.write_text(p.read_text().replace('status: "ready"', 'status: "in_review"'))
    r = run(root, "note", cid, "--agent", "x", "--text", "launder")
    assert r.returncode == 2 and "outside board.py" in r.stderr


def test_validate_rejects_bad_paths(root):
    assert run(root, "validate", str(root / "nope.md")).returncode == 2
    assert run(root, "validate", "/etc/hosts").returncode == 2


def test_findings_null_no_traceback(root):
    cid = new(root)
    p = root / "reviews" / f"{cid}-x.md"
    p.write_text('```json\n{"card":"%s","persona":"x","verdict":"pass","exercised":["a"],"findings":null}\n```' % cid)
    r = run(root, "validate", str(p))
    assert r.returncode == 2 and "Traceback" not in r.stderr


def test_forged_assigned_marker_ignored(root):
    cid = new(root)
    run(root, "note", cid, "--agent", "qa", "--text", "assigned: me")
    assert json.loads(run(root, "status", "--json").stdout)["ready_unclaimed"] == 1


def test_junk_review_entry_no_traceback(root):
    cid = new(root)
    p = root / "board" / "cards" / f"{cid}.md"
    p.write_text(p.read_text().replace("reviews: []", 'reviews:\n  - "junk"'))
    r = run(root, "validate", str(p))
    assert r.returncode == 2 and "Traceback" not in r.stderr


def test_accept_debt_after_three_rounds(root):
    cid = new(root)
    run(root, "claim", cid, "--agent", "backend")
    run(root, "ac", cid, "--agent", "backend", "--check", "1", "--evidence", "tests/x.py::t passes")
    run(root, "ac", cid, "--agent", "backend", "--check", "2", "--evidence", "tests/x.py::t passes")
    for i in range(2):
        run(root, "handoff", cid, "--agent", "backend", "--text", f"r{i}")
        run(root, "move", cid, "in_review", "--agent", "backend")
        f = write_review(root, cid, "changes", [{"severity": "major", "title": "b", "evidence": "e"}])
        run(root, "review", cid, "--persona", "staff-engineer-reviewer", "--model", "m", "--verdict", "changes", "--file", f)
        if i < 1:
            r = run(root, "move", cid, "done", "--agent", "orchestrator", "--accept-debt", "x")
            assert r.returncode == 2
            run(root, "claim", cid, "--agent", "backend")
    r = run(root, "move", cid, "done", "--agent", "orchestrator", "--accept-debt", "two majors moved to T-999")
    assert r.returncode == 0, r.stderr
    assert "accepted with documented debt" in (root / "memory" / "SCOPE_CUTS.md").read_text()


def test_stale_dispatch_marker_ignored_after_resubmit(root):
    cid = new(root)
    run(root, "claim", cid, "--agent", "backend")
    run(root, "handoff", cid, "--agent", "backend", "--text", "h")
    run(root, "move", cid, "in_review", "--agent", "backend", "--note", "x")
    run(root, "dispatch", cid, "--personas", "p")
    f = write_review(root, cid, "changes", [{"severity": "major", "title": "b", "evidence": "e"}])
    run(root, "review", cid, "--persona", "staff-engineer-reviewer", "--model", "m", "--verdict", "changes", "--file", f)
    run(root, "claim", cid, "--agent", "backend")
    import time; time.sleep(1.1)
    run(root, "move", cid, "in_review", "--agent", "backend", "--note", "r2")
    assert json.loads(run(root, "status", "--json").stdout)["in_review"] == 1


def test_debt_does_not_mask_later_fail(root):
    cid = new(root)
    p = root / "board" / "cards" / f"{cid}.md"
    import re as _re
    sys.path.insert(0, str(BOARD.parent)); import importlib, board as bmod
    meta = {"reviews": [{"persona": "orchestrator-§7.4", "verdict": "pass", "debt": "x"},
                        {"persona": "staff-engineer-reviewer", "verdict": "fail"}]}
    assert bmod._reviews_pass(meta) is False
    meta["reviews"].append({"persona": "staff-engineer-reviewer", "verdict": "pass"})
    assert bmod._reviews_pass(meta) is True
