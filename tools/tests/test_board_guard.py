"""board-guard: identity rules for subagents (T-001/T-004 round 2)."""
import json, os, subprocess
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parents[2]
HOOK = REPO / ".claude" / "hooks" / "board-guard.sh"
B = "python3 tools/board.py"


def run(cmd, agent_type=None, agent_id="a1"):
    d = {"tool_input": {"command": cmd}, "cwd": str(REPO), "scratchpad_dir": "/tmp/scratchx"}
    if agent_id:
        d["agent_id"] = agent_id
    if agent_type:
        d["agent_type"] = agent_type
    p = subprocess.run([str(HOOK)], input=json.dumps(d), capture_output=True, text=True,
                       env=dict(os.environ, CLAUDE_PROJECT_DIR=str(REPO)))
    return "deny" in p.stdout


@pytest.mark.parametrize("cmd,atype", [
    (f"{B} move T-1 done --agent backend", "backend"), (f"{B} move T-1 done --agent orchestrator", "general-purpose"),
    (f"{B} note T-1 --agent orchestrator --text x", "backend"), (f"{B} review T-1 --persona p --model m --verdict pass --file f", "qa"),
    (f"{B} gate M1 --record r --result pass", "writer"), (f"{B} claim T-1 --agent frontend", "backend"),
    (f"{B} note T-1 --agent paralegal-reviewer --text x", "paralegal-reviewer"),
    ("echo x > app/backend/x.py", "staff-engineer-reviewer"), ("cat a >> memory/STATE.md", "ux-designer-reviewer"),
    ("tee board/cards/T-001.md < x", "security-reviewer"), ("cp x app/x.py", "security-reviewer"),
    ("sed -i '' s/a/b/ app/x.py", "security-reviewer"), ("git commit -m x", "staff-engineer-reviewer"),
    ("git -c a=b add reviews/x.md", "staff-engineer-reviewer"), ("touch .claude/agent-memory/qa/x", "paralegal-reviewer"),
])
def test_denied(cmd, atype):
    assert run(cmd, atype), cmd


@pytest.mark.parametrize("cmd,atype,aid", [
    (f"{B} move T-1 done --agent orchestrator", None, None),  # main session
    (f"{B} note T-1 --agent backend --text x", "backend", "a1"),
    (f"{B} move T-1 in_review --agent qa", "qa", "a1"),
    (f"{B} note T-1 --agent researcher --text x", "general-purpose", "a1"),
    (f"{B} validate reviews/T-1-x.md", "paralegal-reviewer", "a1"),
    ("echo x > reviews/T-1-x.md", "paralegal-reviewer", "a1"),
    ("python3 x.py > artifacts/review-evidence/out.txt 2>&1", "chaos-tester-reviewer", "a1"),
    ("echo x > /tmp/y; cat /tmp/y", "security-reviewer", "a1"),
    ("mkdir -p .claude/agent-memory/paralegal-reviewer", "paralegal-reviewer", "a1"),
    ("git log --oneline && git diff HEAD~1", "staff-engineer-reviewer", "a1"),
    ("curl -s localhost:7777/healthz 2>/dev/null", "security-reviewer", "a1"),
    ("git diff HEAD -- tools/board.py", "staff-engineer-reviewer", "a1"),
    (".venv/bin/python -m pytest tools/tests/test_board.py -q", "staff-engineer-reviewer", "a1"),
    ("BOARD_ROOT=/tmp/bx python3 tools/board.py move T-1 done --agent orchestrator", "staff-engineer-reviewer", "a1"),
    ("curl -s -o artifacts/review-evidence/x.html http://localhost:7777/", "security-reviewer", "a1"),
    ("cd artifacts/review-evidence && echo x > y.txt", "security-reviewer", "a1"),
    ("cd /tmp/scratchrepo && git init -q && git add -A && git commit -qm x", "security-reviewer", "a1"),
    ("git config --get user.email", "staff-engineer-reviewer", "a1"),
    ("wget -O - http://localhost:7777/ | head", "security-reviewer", "a1"),
])
def test_allowed(cmd, atype, aid):
    assert not run(cmd, atype, aid), cmd


@pytest.mark.parametrize("cmd", ["pkill -f app.main", "killall python3", "/usr/bin/pkill -f uvicorn", "sleep 1 && pkill -f app"])
def test_pattern_kill_denied_for_subagents(cmd):
    assert run(cmd, "frontend"), cmd
    assert not run(cmd, None, None)  # orchestrator may


def test_kill_by_pid_allowed():
    assert not run("kill 12345", "frontend")
