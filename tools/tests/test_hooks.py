"""Hook smoke tests (§4.8.3): each hook run by hand with crafted stdin JSON."""
import json, os, shutil, subprocess, sys
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parents[2]
HOOKS = REPO / ".claude" / "hooks"


@pytest.fixture
def proj(tmp_path):
    (tmp_path / "tools").mkdir()
    shutil.copy(REPO / "tools" / "board.py", tmp_path / "tools" / "board.py")
    shutil.copy(REPO / "tools" / "check_secrets.py", tmp_path / "tools" / "check_secrets.py")
    (tmp_path / "reviews").mkdir()
    env = dict(os.environ, BOARD_ROOT=str(tmp_path), CLAUDE_PROJECT_DIR=str(tmp_path))
    subprocess.run([sys.executable, str(tmp_path / "tools/board.py"), "init"], env=env, check=True, capture_output=True)
    return tmp_path, env


def hook(name, payload, env):
    return subprocess.run([str(HOOKS / name)], input=json.dumps(payload), capture_output=True, text=True, env=env)


def mkcard(proj, env, role="backend"):
    subprocess.run([sys.executable, str(proj / "tools/board.py"), "new", "--title", "x", "--milestone", "M0",
                    "--role", role, "--ac", "a"], env=env, check=True, capture_output=True)


def test_stop_guard_allows_when_nothing_actionable(proj):
    root, env = proj
    mkcard(root, env)
    subprocess.run([sys.executable, str(root / "tools/board.py"), "claim", "T-001", "--agent", "backend"], env=env, check=True)
    r = hook("stop-guard.sh", {"hook_event_name": "Stop"}, env)
    assert r.returncode == 0 and "block" not in r.stdout


def test_stop_guard_blocks_on_ready_card(proj):
    root, env = proj
    mkcard(root, env)
    r = hook("stop-guard.sh", {"hook_event_name": "Stop"}, env)
    out = json.loads(r.stdout)
    assert out["decision"] == "block" and "T-001" in out["reason"]


def test_stop_guard_ignores_subagents(proj):
    root, env = proj
    mkcard(root, env)
    r = hook("stop-guard.sh", {"hook_event_name": "Stop", "agent_id": "abc"}, env)
    assert r.returncode == 0 and r.stdout.strip() == ""


def test_stop_guard_allows_with_STOP(proj):
    root, env = proj
    mkcard(root, env)
    (root / "board" / "STOP").touch()
    r = hook("stop-guard.sh", {"hook_event_name": "Stop"}, env)
    assert r.returncode == 0 and r.stdout.strip() == ""


def test_stop_guard_stall_guard(proj):
    root, env = proj
    mkcard(root, env)
    outs = [hook("stop-guard.sh", {}, env).stdout for _ in range(6)]
    assert all('"block"' in o for o in outs[:5])
    assert "Stall guard" in outs[5] and (root / "board" / "ALERT.md").exists()


def test_teammate_idle(proj):
    root, env = proj
    mkcard(root, env, role="backend")
    r = hook("teammate-idle.sh", {"agent_type": "backend"}, env)
    assert r.returncode == 2 and "T-001" in r.stderr
    r = hook("teammate-idle.sh", {"agent_type": "writer"}, env)
    assert r.returncode == 0
    r = hook("teammate-idle.sh", {"agent_type": "mystery"}, env)
    assert r.returncode == 0


def test_board_validate(proj):
    root, env = proj
    mkcard(root, env)
    good = root / "board/cards/T-001.md"
    r = hook("board-validate.sh", {"tool_input": {"file_path": str(good)}}, env)
    assert r.returncode == 0
    bad = root / "reviews" / "T-001-x.md"
    bad.write_text("no json here")
    r = hook("board-validate.sh", {"tool_input": {"file_path": str(bad)}}, env)
    assert r.returncode == 2 and "json" in r.stderr
    r = hook("board-validate.sh", {"tool_input": {"file_path": "/etc/hosts"}}, env)
    assert r.returncode == 0


DENY = ["git add -A", "git add .", "git reset --hard HEAD", "git push --force origin main",
        "git push origin main -f", "git clean -fd", "rm -rf /", "rm -rf ~", "rm -rf .git",
        "git commit --amend -m x", "cd x && rm -rf ../board", "bash -c 'git reset --hard'", "rm -rf 'memory'"]


@pytest.mark.parametrize("cmd", DENY)
def test_git_guard_denies(proj, cmd):
    root, env = proj
    r = hook("git-guard.sh", {"tool_input": {"command": cmd}, "cwd": str(root)}, env)
    assert json.loads(r.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


@pytest.mark.parametrize("cmd", ["git status", "git add tools/board.py", "ls -la", "rm -rf artifacts/tmp/x",
                                 "git log --oneline", "python3 tools/board.py note T-1 --agent a --text 'blocked git push --force today'", "cat > f.py <<'EOF'\nx = 'git add -A'\nEOF\necho ok"])
def test_git_guard_allows(proj, cmd):
    root, env = proj
    r = hook("git-guard.sh", {"tool_input": {"command": cmd}}, env)
    assert r.returncode == 0 and r.stdout.strip() == ""


def test_git_guard_blocks_staged_secret(proj):
    root, env = proj
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    (root / "leak.txt").write_text("key = sk-ant-" + "a" * 40 + "\n")
    subprocess.run(["git", "add", "leak.txt"], cwd=root, check=True)
    r = hook("git-guard.sh", {"tool_input": {"command": "git commit -m 'feat: x'"}}, env)
    assert "deny" in r.stdout and "secret" in r.stdout
    subprocess.run(["git", "rm", "--cached", "-q", "leak.txt"], cwd=root, check=True)
    (root / ".env").write_text("ANTHROPIC_API_KEY=x\n")
    subprocess.run(["git", "add", "-f", ".env"], cwd=root, check=True)
    r = hook("git-guard.sh", {"tool_input": {"command": "git commit -m 'feat: x'"}}, env)
    assert "deny" in r.stdout


def test_reviewer_write_guard(proj):
    root, env = proj
    r = hook("reviewer-write-guard.sh", {"tool_input": {"file_path": str(root / "reviews/T-001-x.md")}}, env)
    assert r.returncode == 0 and r.stdout.strip() == ""
    r = hook("reviewer-write-guard.sh", {"tool_input": {"file_path": str(root / "app/backend/x.py")}}, env)
    assert "deny" in r.stdout
