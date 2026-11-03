"""git-guard regression suite (round 2): every bypass from reviews/T-003-security.md plus legitimate commands."""
import json, os, subprocess
from pathlib import Path
import pytest

REPO = Path(__file__).resolve().parents[2]
HOOK = REPO / ".claude" / "hooks" / "git-guard.sh"
R = str(REPO)

MUST_DENY = [
    "git add -A", "git add --all", "git add .", "git add -u", "git add -- .", "git add :/", "git add ':/'", "git add *",
    "git add ./", "git add ././", 'git add "."', "git add '.'", "git -c core.x=y add -A", "git -C . add -A",
    f"git -C {R} add .", "git --no-pager add -A", "git add -fA", "git add -vA", "git add -Av", "git add -n -A",
    "git add --update", "git add --no-ignore-removal .", "git add -f .env", "git add .env", f"git add {R}", f"git add {R}/",
    "git add ..", "g=git; $g add -A", 'G="git add"; $G -A', "a=-A; git add $a", "git add $'-A'", "git add -\"A\"",
    "git add -'A'", "git ad\\d -A", '"git" add -A', '"git" "add" "-A"', "git \"add\" -A", "git add \"-A\"",
    "git $(echo add) -A", 'sh -c "git add ."', "echo 'git add -A' | sh", "alias ga='git add -A'; ga", "git\tadd -A",
    "bash <<< 'git add -A'", "bash <<'EOF'\ngit add -A\nEOF", "dash -c 'git add -A'", "/usr/bin/git add -A",
    "sudo git add -A", "env FOO=1 git add -A", "command git add -A", "CMD=\"git add -A\"; $CMD",
    "git push --force origin main", "git push -f origin main", "git push origin +main", "git push origin +HEAD:main",
    "git push origin +refs/heads/main:refs/heads/main", "git push origin :main", "git push origin --delete main",
    "git push --mirror", "git push --prune", "git push -uf origin main", "git push -fu origin main", "git push origin main -vf",
    "git push --forc origin main", "FORCE=-f; git push $FORCE origin main", "git push --force-with-lease",
    "git reset --hard HEAD~1", "git reset -q --hard", "git reset --keep HEAD~1", "git reset --merge", "git reset HEAD~5",
    "git reset --soft HEAD~1", "git reset --HARD",
    "git clean -fd", "git clean --force", "git clean -d -f", "git clean -d --force",
    "git checkout -- .", "git checkout .", "git checkout -f", "git checkout HEAD -- .", "git restore .",
    "git restore --staged --worktree .", "git stash drop", "git stash clear", "git branch --delete --force foo",
    "git branch -D foo", "git tag -d m0", "git tag --delete m0", "git rebase -i HEAD~3", "git filter-branch",
    "git commit --amend -m x", "git commit -am x", "git reflog expire --all", "git gc --prune=now", "git update-ref -d HEAD", "git commit-tree abc -p HEAD -m x", "git symbolic-ref HEAD refs/heads/x",
    "rm -rf /", "rm -rf ~", "rm -rf .git", "rm -rf ./.git", f"rm -rf {R}", "rm -Rf board", "rm -r -f memory", "rm -fr reviews",
    "git status\ngit add -A", "echo hi\ngit push --force", "ls\ngit reset --hard", "git add \\\n.",
    "git push origin HEAD:+main", "git push origin HEAD:+refs/heads/main", "{ git add -A; }", "if true; then git add -A; fi",
    "! git add -A", "xargs git push -f", "env -u X git add -A", "nice -n 5 git add -A", "sudo -u x git add -A",
    "timeout -s KILL 5 git add -A", "echo git add -A | bash", "rm -rf $(pwd)", "git -c alias.x='!git add -A' x",
    "git -c core.pager=sh status", "git config alias.z '!git add -A'", "rm -rf board/*", "rm -rf memory/*",
    "rm -rf .git/objects", "rm .git/hooks/pre-commit", "rm -rf .claude/hooks", "find board -name x -delete",
    "git tag -f m0", "git add ./*", "git add .*", "git add $(git diff --name-only)", "git ls-files -m | xargs git add",
    "sudo -n git add -A", "command -p git add -A", "time -p git add -A", "sudo -E git add -A", "git branch -f main HEAD~1", "git add f.txt && git commit -m x", "git commit --no-verify -m x",
    "rm -rf ./board", f"rm -rf {R}/board", f"rm -rf {R}/memory", "rm -rf $PWD", "rm -rf ${HOME}", "rm -rf 'memory'",
    "sudo rm -rf board", "env rm -rf board", "command rm -rf board", "mv board /tmp/x", "mv memory memory.bak",
    "find board -delete", "cd x && rm -rf ../board", "bash -c 'git reset --hard'", "eval git add -A",
]
MUST_ALLOW = [
    "git status", "git add tools/board.py", "git add 'my file.txt' tools/x.py", "git log --oneline", "git diff HEAD~1",
    "git push origin main", "git reset -- tools/board.py", "git reset", "git clean -n -f", "git checkout -b feature",
    "git checkout -- tools/board.py", "git restore --staged tools/board.py", "git branch -d merged", "git tag m0",
    "git stash list", "git show HEAD~1:tools/board.py", "ls -la", "rm -rf artifacts/tmp/x", "rm tools/foo.pyc",
    "mv artifacts/tmp/a artifacts/tmp/b", "B=\"python3 tools/board.py\"; $B status --brief",
    "python3 tools/board.py note T-1 --agent a --text 'blocked git push --force today'",
    "cat > f.py <<'EOF'\nx = 'git add -A'\nrm -rf /\nEOF\necho ok", "echo 'rm -rf board is blocked'",
    "find artifacts/tmp -name '*.png' -delete", "grep -rn 'git add -A' docs/", "rm board/STOP",
    "git status\ngit log --oneline", 'B="python3 tools/board.py"; N=$($B list --role architect | tail -1); echo $N', "echo 'first line\nsecond git add -A line'",
    "python3 tools/board.py note T-1 --agent a --text \"Chris's note: run | sh and git add only owned paths\"",
]


def run(cmd, cwd=R):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=R)
    p = subprocess.run([str(HOOK)], input=json.dumps({"tool_input": {"command": cmd}, "cwd": cwd}),
                       capture_output=True, text=True, env=env, timeout=60)
    return p


@pytest.mark.parametrize("cmd", MUST_DENY)
def test_denies(cmd):
    p = run(cmd)
    assert p.stdout.strip(), f"ALLOWED: {cmd!r} (stderr={p.stderr[:200]})"
    assert json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"


@pytest.mark.parametrize("cmd", MUST_ALLOW)
def test_allows(cmd):
    p = run(cmd)
    assert p.returncode == 0 and p.stdout.strip() == "", f"DENIED: {cmd!r}: {p.stdout[:300]}"


@pytest.mark.parametrize("payload", ["not json", "[]", '{"tool_input": {"command": 42}}'])
def test_fails_closed(payload):
    p = subprocess.run([str(HOOK)], input=payload, capture_output=True, text=True, env=dict(os.environ, CLAUDE_PROJECT_DIR=R))
    assert "deny" in p.stdout


def _run_as(cmd, agent):
    d = {"tool_input": {"command": cmd}, "cwd": R}
    if agent:
        d.update(agent_id="a1", agent_type="backend")
    p = subprocess.run([str(HOOK)], input=json.dumps(d), capture_output=True, text=True,
                       env=dict(os.environ, CLAUDE_PROJECT_DIR=R))
    return "deny" in p.stdout


@pytest.mark.parametrize("cmd,agent,denied", [
    ("git commit -m x", True, True),                       # stale shared index: subagent needs a pathspec
    ("git commit -m x -- app/backend/x.py", True, False),
    ("GIT_INDEX_FILE=/tmp/idx git commit -m x", True, False),
    ("export GIT_INDEX_FILE=/tmp/idx; git commit -m x", True, False),
    ("git commit -m x", False, False),                     # orchestrator keeps plain commit
])
def test_subagent_commit_needs_pathspec_or_temp_index(cmd, agent, denied):
    assert _run_as(cmd, agent) is denied, cmd


@pytest.mark.parametrize("cmd,agent,denied", [
    ("git checkout app/backend/store.py", True, True),         # lesson T-157 r3: wipes others' uncommitted edits
    ("git checkout -- app/backend/store.py", True, True),
    ("git restore app/backend/store.py", True, True),
    ("git restore --staged app/backend/store.py", True, False),  # index only, the worktree is untouched
    ("git show HEAD:app/backend/store.py", True, False),
    ("git checkout -- app/backend/store.py", False, False),    # the orchestrator is not blocked by this rule
])
def test_subagent_may_not_checkout_files_in_shared_tree(cmd, agent, denied):
    assert _run_as(cmd, agent) is denied, cmd


@pytest.mark.parametrize("cmd,agent,denied", [
    ("git add app/backend/x.py", True, True),                       # T-204: stale reverts piled up in the shared index
    ("GIT_INDEX_FILE=/tmp/idx git add app/backend/x.py", True, False),
    ("git add app/backend/x.py", False, False),                     # the orchestrator stages as before
])
def test_subagent_stages_only_into_a_temp_index(cmd, agent, denied):
    assert _run_as(cmd, agent) is denied, cmd
