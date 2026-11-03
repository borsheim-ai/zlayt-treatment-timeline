#!/usr/bin/env python3
"""PreToolUse(Bash) hook: identity-based rules the board CLI cannot enforce on a self-declared `--agent`.

Hook events from subagents carry `agent_id` + `agent_type`; the main session (orchestrator) carries neither
(verified in board/.hook_input_keys.log). Rules:
- subagents may not: move a card to done, record reviews, run gates/milestones, assign/dispatch, or act as orchestrator;
- a worker running as a native agent type must use its own role in --agent;
- reviewers (*-reviewer): board.py is read-only for them; no mutating git; shell writes only under reviews/,
  artifacts/review-evidence/, their own .claude/agent-memory/<type>/, the scratchpad, /tmp, /dev/null.
Fails closed on errors. Residual risk: files written by interpreters (python -c) are not detected.
"""
from __future__ import annotations
import json
import os
import re
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from git_guard import ROOT, strip_heredocs, segments, expand_vars, deny_json, strip_wrappers  # noqa: E402

ROLES = {"architect", "backend", "db", "frontend", "qa", "release", "writer", "researcher"}
READONLY_BOARD = {"validate", "show", "list", "status", "next", "inbox", "--help", "-h"}
MUTATING_GIT = {"add", "commit", "push", "reset", "checkout", "restore", "stash", "rm", "mv", "tag", "branch", "merge",
                "apply", "cherry-pick", "revert", "switch", "rebase", "am", "pull", "clean", "worktree", "init",
                "update-ref", "gc", "prune", "reflog", "notes", "replace", "filter-branch", "fetch"}
WRITE_CMDS = {"cp", "mv", "install", "ln", "touch", "mkdir", "rm", "rmdir", "chmod", "truncate", "tee", "rsync"}


class Deny(Exception):
    pass


def allowed_write(path: str, cwd: Path, data: dict) -> bool:
    p = Path(os.path.normpath(os.path.expanduser(path) if os.path.isabs(os.path.expanduser(path)) else str(cwd / path)))
    p = Path(os.path.realpath(p))
    bases = [ROOT / "reviews", ROOT / "artifacts" / "review-evidence", Path("/tmp"), Path("/private/tmp"),
             Path(os.path.realpath("/tmp")), Path("/dev")]
    if data.get("scratchpad_dir"):
        bases.append(Path(os.path.realpath(data["scratchpad_dir"])))
    if data.get("agent_type"):
        bases.append(ROOT / ".claude" / "agent-memory" / data["agent_type"])
    return any(p == b or b in p.parents for b in bases)


def board_args(seg: list[str]) -> list[str] | None:
    """Only an actual invocation counts: `board.py ...` or `python[3] [-flags] .../board.py ...` (env prefixes allowed)."""
    lead = [t for t in seg[:len(seg) - len(strip_wrappers(seg))] if t.startswith("BOARD_ROOT=")]
    seg = lead + strip_wrappers(seg)
    i = 0
    while i < len(seg) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", seg[i]):
        i += 1
    if i < len(seg) and Path(seg[i]).name == "board.py":
        return seg[i + 1:]
    if i < len(seg) and re.fullmatch(r"python(3(\.\d+)?)?", Path(seg[i]).name):
        j = i + 1
        while j < len(seg) and seg[j].startswith("-"):
            j += 2 if seg[j] in ("-W", "-X", "-Q") else 1
        if j < len(seg) and Path(seg[j]).name == "board.py":
            return seg[j + 1:]
    return None


def board_root_outside(seg: list[str], cwd: Path, data: dict) -> bool:
    for t in seg:
        if t.startswith("BOARD_ROOT="):
            return allowed_write(t.split("=", 1)[1], cwd, data) and not t.split("=", 1)[1].startswith(str(ROOT))
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", t):
            break
    return False


SHELL_EXEC = re.compile(r"\b(sh|bash|zsh|dash|ksh|fish)\b|\beval\b|\bxargs\b|<<<|\$\(|`")


def flag(args: list[str], name: str):
    for i, t in enumerate(args):
        if t == name and i + 1 < len(args):
            return args[i + 1]
        if t.startswith(name + "="):
            return t.split("=", 1)[1]
    return None


def check(cmd: str, data: dict, depth: int = 0):
    agent_type = data.get("agent_type") or ""
    is_reviewer = agent_type.endswith("-reviewer")
    cwd = Path(data.get("cwd") or os.getcwd())
    body, _ = strip_heredocs(cmd)
    if depth < 4 and SHELL_EXEC.search(body):  # strings executed by a shell are commands too
        for q in re.findall(r"'([^']*)'|\"((?:[^\"\\\\]|\\\\.)*)\"", body):
            q = q[0] or q[1]
            if q.strip():
                try:
                    check(q, data, depth + 1)
                except Deny:
                    raise
                except Exception:
                    pass
        for m in re.finditer(r"\$\(([^()]*)\)|`([^`]*)`", body):
            check(m.group(1) or m.group(2), data, depth + 1)
    for seg in segments(expand_vars(body)):
        if not seg:
            continue
        if seg[0] == "cd" and len(seg) > 1:
            cwd = Path(os.path.normpath(str(cwd / seg[1])))
            continue
        ba = board_args(seg)
        if ba is not None and ba and not board_root_outside(seg, cwd, data):
            sub = ba[0]
            agent = flag(ba, "--agent") or flag(ba, "--by")
            if agent == "orchestrator":
                raise Deny("subagents may not act as --agent orchestrator")
            if sub in ("review", "gate", "milestone", "assign", "dispatch"):
                raise Deny(f"`board.py {sub}` is orchestrator-only")
            if sub == "move" and "done" in [t for t in ba[1:] if not t.startswith("-")]:
                raise Deny("only the orchestrator moves cards to done (no self-approval)")
            if is_reviewer and sub not in READONLY_BOARD:
                raise Deny(f"reviewers use board.py read-only (validate/show/list/status); `{sub}` is not allowed")
            if agent_type in ROLES and agent and agent != agent_type:
                raise Deny(f"you are running as '{agent_type}'; use --agent {agent_type}")
        # any subagent: never kill processes by pattern (shared dev servers, other workers' instances)
        if Path(seg[0]).name in ("pkill", "killall"):
            raise Deny("subagents may not pkill/killall by pattern; stop only your own server by PID (kill $!)")
        # any subagent: never rewind shared state files
        if Path(seg[0]).name == "git":
            rest = seg[1:]
            while rest and rest[0].startswith("-"):
                rest = rest[2:] if rest[0] in ("-C", "-c") else rest[1:]
            if rest and rest[0] == "stash":
                raise Deny("subagents may not run git stash (it rewinds shared board/memory files of other agents)")
            if rest and rest[0] in ("checkout", "restore") and any(
                    t.startswith(("board", "./board", "memory", "./memory")) or "/board/" in t or "/memory/" in t for t in rest[1:]):
                raise Deny("subagents may not checkout/restore board/ or memory/ files")
        if not is_reviewer:
            continue
        # redirections, with cwd tracking (tokens like '>' 'f', '>f', '2>>f', '&>f', '>&f')
        for k, t in enumerate(seg):
            if ">" in t and not t.startswith((">", "&>", "1>", "2>")) and not re.match(r"^\d>", t):
                t = t[t.index(">"):]  # 'x>app/x' (no space)
            m = re.fullmatch(r"(?:\d|&)?>>?&?\|?(.*)", t)
            if not m:
                continue
            tgt = m.group(1) or (seg[k + 1] if k + 1 < len(seg) else "")
            if not tgt or re.fullmatch(r"&?\d|-", tgt):
                continue
            if not allowed_write(tgt, cwd, data):
                raise Deny(f"reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to {tgt})")
        seg = strip_wrappers([t for t in seg if not re.fullmatch(r"(?:\d|&)?>>?&?\|?.*", t)])
        if not seg:
            continue
        prog = Path(seg[0]).name
        if prog == "git":
            rest = [t for t in seg[1:]]
            gcwd = cwd
            while rest and rest[0].startswith("-"):
                if rest[0] == "-C" and len(rest) > 1:
                    gcwd = Path(os.path.normpath(str(cwd / rest[1])))
                rest = rest[2:] if rest[0] in ("-C", "-c") else rest[1:]
            scratch = allowed_write(str(gcwd), cwd, data) and not str(gcwd).startswith(str(ROOT))
            if rest and rest[0] in MUTATING_GIT and not scratch:
                raise Deny(f"reviewers may not run `git {rest[0]}` in the project (allowed only in scratch repos under /tmp)")
            for t in rest:
                if t.startswith("--output") :
                    tgt = t.split("=", 1)[1] if "=" in t else ""
                    if not tgt or not allowed_write(tgt, cwd, data):
                        raise Deny("reviewers may not write files via git --output")
        if prog in WRITE_CMDS:
            args = [t for t in seg[1:] if not t.startswith("-")]
            targets = args if prog in ("rm", "rmdir", "touch", "mkdir", "chmod", "truncate", "tee") else args[-1:]
            for t in targets:
                if not allowed_write(t, cwd, data):
                    raise Deny(f"reviewers may only write under reviews/ or artifacts/review-evidence/ ({prog} {t})")
        if prog == "perl" and any(re.fullmatch(r"-[A-Za-z]*i.*", t) for t in seg[1:]):
            files = [t for t in seg[1:] if not t.startswith("-")][1:]
            if not files or any(not allowed_write(t, cwd, data) for t in files):
                raise Deny("reviewers may not edit files in place with perl -i")
        if prog == "unzip" or (prog == "7z" and "x" in seg[1:2]):
            dest = next((seg[k + 1] for k, t in enumerate(seg) if t in ("-d", "-o") and k + 1 < len(seg)), ".")
            if not allowed_write(dest, cwd, data):
                raise Deny(f"reviewers may not extract archives into {dest}")
        if prog == "sed" and any(re.fullmatch(r"-[A-Za-z]*i.*", t) or t.startswith("--in-place") for t in seg[1:]):
            files = [t for t in seg[1:] if not t.startswith("-")][1:]
            for t in files:
                if not allowed_write(t, cwd, data):
                    raise Deny(f"reviewers may not edit {t} in place")
        if prog == "curl":
            for k, t in enumerate(seg[1:], 1):
                m = re.fullmatch(r"-[A-Za-z]*o(.*)", t) if not t.startswith("--") else None
                if t in ("--output",) or (m is not None):
                    tgt = (m.group(1) if m and m.group(1) else (seg[k + 1] if k + 1 < len(seg) else ""))
                    if tgt != "-" and not allowed_write(tgt, cwd, data):
                        raise Deny(f"reviewers may not download into {tgt}")
                if (re.fullmatch(r"-[A-Za-z]*O[A-Za-z]*", t) or t == "--remote-name") and not allowed_write(".", cwd, data):
                    raise Deny("reviewers may not download into the project tree")
        if prog == "wget":
            out = next((seg[k + 1] for k, t in enumerate(seg) if t in ("-O", "--output-document") and k + 1 < len(seg)), None)
            if out != "-" and not allowed_write(out or ".", cwd, data):
                raise Deny("reviewers may not download into the project tree")
        if prog == "tar" and any(re.fullmatch(r"-?[A-Za-z]*x[A-Za-z]*", t) or t == "--extract" for t in seg[1:2] + seg[1:]):
            dest = next((seg[k + 1] for k, t in enumerate(seg) if t in ("-C", "--directory") and k + 1 < len(seg)), ".")
            if not allowed_write(dest, cwd, data):
                raise Deny(f"reviewers may not extract archives into {dest}")
        if prog == "dd":
            for t in seg[1:]:
                if t.startswith("of=") and not allowed_write(t[3:], cwd, data):
                    raise Deny(f"reviewers may not write {t[3:]}")


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict):
            raise ValueError("hook input is not an object")
        if not data.get("agent_id"):
            return 0  # main session = orchestrator
        cmd = (data.get("tool_input") or {}).get("command") or ""
        if not isinstance(cmd, str):
            raise ValueError("command is not a string")
        check(cmd, data)
        return 0
    except Deny as e:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                 "permissionDecisionReason": "board-guard: " + str(e)}}))
        return 0
    except Exception as e:
        deny_json(f"board-guard error ({type(e).__name__}: {e}); denying to fail closed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
