"""Agent definitions stay in sync with the generator and dossiers (T-004 r2)."""
import subprocess, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[2]


def test_agents_in_sync():
    r = subprocess.run([sys.executable, str(REPO / "tools/compile_agents.py"), "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


def test_no_provisional_reviewers():
    assert not [p.name for p in (REPO / ".claude/agents").glob("*-reviewer.md") if "PROVISIONAL" in p.read_text()]


def test_agent_prompt_errors_cleanly():
    for args in (["../../docs/CONTRACT"], ["qa", "--brief-file"], ["qa", "--brief-file", "/nonexistent"]):
        r = subprocess.run([sys.executable, str(REPO / "tools/agent_prompt.py"), *args], capture_output=True, text=True)
        assert r.returncode == 2 and "Traceback" not in r.stderr


def test_reviewer_bodies_carry_rules():
    contract = (REPO / "docs/CONTRACT.md").read_text()
    sk = contract.split("### 7.3 Skepticism rules (embed in every reviewer body)")[1].split("### 7.4")[0].strip()
    bullets = [b.strip() for b in sk.splitlines() if b.startswith("- ")]
    for p in (REPO / ".claude/agents").glob("*-reviewer.md"):
        t = p.read_text()
        assert all(b in t for b in bullets), f"{p.name} lost a §7.3 rule"
        assert '"verdict": "pass|changes|fail"' in t and "First step, every review" in t
