#!/usr/bin/env python3
"""PreToolUse(Bash) hook (§4.3): deny destructive git / rm / mv commands and commits with staged secrets.

Defense in depth, not a sandbox. Approach (round 2, after the T-003 security review):
- tokenize with shlex (handles quotes, escapes, tabs), split on ; && || | & newlines and subshell parens;
- expand simple `VAR=value` assignments made in the same command, plus $HOME/$PWD/~;
- strip wrappers (sudo, env, command, exec, nice, nohup, time, builtin) and path prefixes (/usr/bin/git);
- parse git's global options (-C, -c, --no-pager, --git-dir=...), resolve git aliases, then check per subcommand;
- anything executed as a string (sh/bash/zsh/dash/ksh -c, `| sh`, eval, alias, <<<, heredoc into a shell,
  $(...)/backticks) is analysed recursively;
- fail closed: any exception, malformed input, or secret-scan timeout denies.
Residual risk (documented in memory/LESSONS.md): variables from the inherited environment and code executed by
interpreters (python -c, node -e) are not analysed.
"""
from __future__ import annotations
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path

try:
    from _common import ROOT
except Exception:  # pragma: no cover
    ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2])

ROOT = Path(os.path.realpath(ROOT))
HOME = os.path.realpath(os.path.expanduser("~"))
PROTECTED = {Path("/"), Path(HOME), ROOT, ROOT / ".git", ROOT / "board", ROOT / "memory", ROOT / "reviews",
             ROOT / "board" / "cards"}
SHELLS = {"sh", "bash", "zsh", "dash", "ksh", "fish"}
WRAPPERS = {"sudo", "env", "command", "exec", "nice", "nohup", "time", "builtin", "doas", "stdbuf", "timeout", "xargs",
            "{", "}", "then", "do", "else", "elif", "if", "while", "until", "!", "caffeinate"}
WRAPPER_OPTS_WITH_ARG = {  # per wrapper: which options consume the next token
    "sudo": {"-u", "-g", "-C", "-p", "-h", "-r", "-t", "-U"}, "doas": {"-u", "-C"}, "env": {"-u", "-C", "-S"},
    "nice": {"-n"}, "timeout": {"-s", "-k", "--signal", "--kill-after"}, "xargs": {"-I", "-L", "-P", "-n", "-s", "-E", "-d"},
    "stdbuf": {"-i", "-o", "-e"}}
GIT_GLOBAL_WITH_ARG = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path", "--super-prefix",
                       "--config-env"}
SAFE_GIT = {"status", "log", "diff", "show", "add", "rm", "mv", "branch", "tag", "fetch", "pull", "push", "reset",
            "clean", "checkout", "switch", "restore", "stash", "init", "clone", "config", "ls-files", "rev-parse",
            "blame", "grep", "describe", "shortlog", "remote", "help", "version", "worktree", "check-ignore",
            "cat-file", "rev-list", "merge-base", "for-each-ref", "ls-tree", "name-rev", "show-ref", "notes", "archive"}
HISTORY_REWRITE = {"rebase", "filter-branch", "filter-repo", "replace", "reflog", "gc", "prune", "update-ref",
                   "commit-tree", "symbolic-ref"}  # T-204: a commit was swapped on HEAD by plumbing; commit only via `git commit`


class Deny(Exception):
    pass


def deny_json(reason: str):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                             "permissionDecisionReason": "git-guard: " + reason}}))


# ------------------------------------------------------------------ helpers
def strip_heredocs(cmd: str) -> tuple[str, list[str]]:
    """Remove heredoc bodies that are file content; return (command, bodies fed to a shell)."""
    out, shell_bodies, lines, i = [], [], cmd.split("\n"), 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        m = re.search(r"<<-?\s*['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?", line)
        if m and "<<<" not in line[: m.start() + 3]:
            tag = m.group(1)
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != tag:
                body.append(lines[i])
                i += 1
            first = line[: m.start()].strip().split()
            feeds_shell = any(Path(t).name in SHELLS for t in first) or re.search(r"\|\s*(\S*/)?(sh|bash|zsh|dash|ksh)\b", line)
            if feeds_shell or (first and Path(first[0]).name in {"eval", "xargs"}):
                shell_bodies.append("\n".join(body))
        i += 1
    return "\n".join(out), shell_bodies


def expand_vars(cmd: str) -> str:
    assigns = {}
    for m in re.finditer(r"(?:^|[;&|\s(])([A-Za-z_][A-Za-z0-9_]*)=(\"[^\"]*\"|'[^']*'|[^\s;&|]*)", cmd):
        v = m.group(2)
        if v[:1] in "\"'":
            v = v[1:-1]
        assigns[m.group(1)] = v
    assigns.setdefault("HOME", HOME)
    assigns.setdefault("PWD", os.getcwd())
    for _ in range(3):
        cmd = re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)",
                     lambda m: assigns.get(m.group(1) or m.group(2), m.group(0)), cmd)
    return cmd


def unquoted_newlines_to_semicolons(cmd: str) -> str:
    """Line continuations join lines; an unquoted newline separates commands (like `;`)."""
    cmd = re.sub(r"\\\r?\n", " ", cmd)
    out, q = [], None
    for ch in cmd:
        if q:
            if ch == q:
                q = None
        elif ch in "'\"":
            q = ch
        elif ch == "\n":
            ch = ";"
        out.append(ch)
    return "".join(out)


def segments(cmd: str) -> list[list[str]]:
    cmd = unquoted_newlines_to_semicolons(cmd.replace("$'", "'").replace('$"', '"'))
    lex = shlex.shlex(cmd, posix=True, punctuation_chars=";&|()")
    lex.whitespace_split = True
    lex.commenters = ""
    try:
        toks = list(lex)
    except ValueError as e:
        raise Deny(f"could not parse command safely ({e})")
    segs, cur = [], []
    for t in toks:
        if t and set(t) <= set(";&|()"):
            if cur:
                segs.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        segs.append(cur)
    return segs


def quoted_strings(cmd: str) -> list[str]:
    return [m.group(0)[1:-1] for m in re.finditer(r"'[^']*'|\"(?:[^\"\\]|\\.)*\"", cmd)]


def resolve(p: str, cwd: Path) -> Path:
    p = os.path.expanduser(p)
    return Path(os.path.normpath(p if os.path.isabs(p) else str(cwd / p)))


PROTECTED_TREES = [ROOT / ".git", ROOT / "board", ROOT / "memory", ROOT / "reviews", ROOT / ".claude" / "hooks"]
REMOVABLE = {ROOT / "board" / "STOP", ROOT / "board" / "ALERT.md", ROOT / "board" / ".stop_guard_state", ROOT / "board" / ".locks"}


def inside_protected_tree(p: Path) -> bool:
    if p in REMOVABLE or any(r in p.parents for r in REMOVABLE):
        return False
    return any(p == t or t in p.parents for t in PROTECTED_TREES)


def is_protected(p: Path) -> bool:
    return any(p == x or (p in x.parents) for x in PROTECTED)  # the path itself or an ancestor of a protected path


def short_flags(tok: str) -> str:
    return tok[1:] if re.fullmatch(r"-[A-Za-z]+", tok) else ""


def is_long(tok: str, name: str) -> bool:
    """--forc matches --force (git accepts unambiguous prefixes)."""
    if not tok.startswith("--") or "=" in tok and not name.endswith("="):
        t = tok.split("=", 1)[0]
    else:
        t = tok
    t = t.split("=", 1)[0].lower()
    return len(t) >= 4 and name.startswith(t)


# ------------------------------------------------------------------ checks
def git_alias(sub: str) -> list[str] | None:
    try:
        r = subprocess.run(["git", "-C", str(ROOT), "config", "--get", f"alias.{sub}"], capture_output=True, text=True, timeout=5)
        return shlex.split(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else None
    except Exception:
        return None


def check_git(args: list[str], cwd: Path, scan_flag: list):
    i = 0
    while i < len(args):
        a = args[i]
        if a in GIT_GLOBAL_WITH_ARG:
            if a == "-C" and i + 1 < len(args):
                cwd = resolve(args[i + 1], cwd)
            i += 2
            continue
        if a.startswith("-"):
            i += 1
            continue
        break
    if i >= len(args):
        return
    globals_ = args[:i]
    for k, g in enumerate(globals_):
        if g == "-c" and k + 1 < len(globals_):
            key = globals_[k + 1].split("=", 1)[0].lower()
            if key.startswith("alias.") or key in ("core.pager", "core.fsmonitor", "core.hookspath", "core.sshcommand",
                                                   "core.editor", "pager.diff", "diff.external", "core.askpass"):
                raise Deny(f"git -c {key} can execute arbitrary commands; blocked")
    sub, rest = args[i], args[i + 1:]
    if "--no-verify" in rest or ("-n" in rest and sub == "commit"):
        raise Deny("--no-verify skips the secret scan; never legitimate for agents")
    if sub == "config" and any(re.match(r"(alias\.|core\.(pager|fsmonitor|hookspath|sshcommand|editor))", t.lower()) for t in rest):
        raise Deny("setting git aliases/core command hooks is blocked")
    scan_flag.append("git:" + sub)
    if "$" in sub or "`" in sub:
        raise Deny("dynamic git subcommand is not allowed")
    if sub not in SAFE_GIT and sub not in HISTORY_REWRITE:
        al = git_alias(sub)
        if al:
            if al[0].startswith("!"):
                raise Deny(f"shell git alias '{sub}' is not allowed")
            return check_git(al + rest, cwd, scan_flag)
        scan_flag.append(sub)  # unknown subcommand (e.g. alias-like 'ci'): run the secret scan
    if sub == "add" and getattr(check_git, "_via_xargs", False):
        raise Deny("`xargs git add` stages an unreviewed list; add explicit paths you own")
    if sub in HISTORY_REWRITE:
        raise Deny(f"git {sub} rewrites or prunes history; blocked")
    shorts = "".join(short_flags(t) for t in rest)
    after_dd = rest[rest.index("--") + 1:] if "--" in rest else []
    paths = [t for t in rest if not t.startswith("-")]

    def broad(t: str) -> bool:
        if t in (".", "./", "*", ":/", ":(top)", ":/:", "..", ":(glob)**") or re.fullmatch(r"(\./)+\.?", t):
            return True
        if t == "$" or re.fullmatch(r"(\./)*\.?\*.*|\.\*", t) or "$(" in t or "`" in t:  # ./*  .*  *.py at root, $(…) lists
            return True
        if t.startswith(":/") or t.startswith(":(top)"):
            return True
        p = resolve(t, cwd)
        return p == ROOT or p in ROOT.parents

    if sub == "add":
        if getattr(check_git, "_subagent", False) and not getattr(check_git, "_temp_index", False):
            # T-201/T-204: the shared index kept holding stale staged reverts of other workers' commits
            raise Deny("subagents stage only into a temp index: GIT_INDEX_FILE=<tmp> git read-tree HEAD, then "
                       "GIT_INDEX_FILE=<tmp> git add <paths> (or commit with a pathspec: git commit -m msg -- <paths>)")
        if any(is_long(t, "--all") or is_long(t, "--update") or is_long(t, "--no-ignore-removal") for t in rest) or \
                set(shorts) & {"A", "u"}:
            raise Deny("git add -A/-u/--all is blocked: add explicit paths you own")
        if any(broad(t) for t in paths):
            raise Deny("git add of '.', ':/', '*' or the repo root is blocked: add explicit paths you own")
        if any(Path(t).name.lower().startswith(".env") and Path(t).name.lower() != ".env.example" for t in paths):
            raise Deny("adding .env files is blocked")
    elif sub == "push":
        if "f" in shorts or "d" in shorts or any(is_long(t, "--force") or is_long(t, "--force-with-lease") or is_long(t, "--mirror")
                                                 or is_long(t, "--delete") or is_long(t, "--prune") for t in rest):
            raise Deny("force/mirror/delete/prune push is blocked")
        if any(t.startswith("+") or ":+" in t or (t.startswith(":") and len(t) > 1) for t in paths):
            raise Deny("push refspec with '+' (force) or ':' (delete) is blocked")
    elif sub == "reset":
        if any(t.lower() in ("--hard", "--keep", "--merge", "--soft") for t in rest) or any(is_long(t, "--hard") for t in rest):
            raise Deny("git reset --hard/--keep/--merge/--soft is blocked")
        revs = [t for t in (rest[: rest.index("--")] if "--" in rest else rest) if not t.startswith("-")]
        if any(re.search(r"HEAD|[~^@]|^[0-9a-f]{7,40}$", t) for t in revs):
            raise Deny("git reset to a revision moves history; blocked (unstage with `git reset -- <path>`)")
    elif sub == "clean":
        dry = "n" in shorts or any(is_long(t, "--dry-run") for t in rest)
        if not dry and ("f" in shorts or any(is_long(t, "--force") for t in rest)):
            raise Deny("git clean -f is blocked")
    elif sub in ("checkout", "restore", "switch"):
        if "f" in shorts or any(is_long(t, "--force") or is_long(t, "--discard-changes") for t in rest):
            raise Deny(f"git {sub} --force discards work; blocked")
        if any(broad(t) for t in (after_dd or paths if sub == "restore" else after_dd or [p for p in paths if p in (".", "./", ":/")])):
            raise Deny(f"git {sub} of '.'/root discards everyone's changes; blocked")
        # lesson T-157 r3: a subagent's `git checkout <file>` wiped another worker's uncommitted edits in the shared tree
        if getattr(check_git, "_subagent", False):
            worktree_restore = sub == "restore" and not (any(is_long(t, "--staged") for t in rest) and not any(is_long(t, "--worktree") for t in rest))
            file_checkout = sub == "checkout" and (after_dd or any(Path(p).exists() for p in paths))
            if worktree_restore or file_checkout:
                raise Deny(f"subagents may not git {sub} files in the shared tree (it discards other workers' uncommitted edits); "
                           "read the committed version with `git show HEAD:<path>` into your scratchpad instead")
    elif sub == "stash":
        if rest[:1] and rest[0] in ("drop", "clear"):
            raise Deny("git stash drop/clear is blocked")
    elif sub == "branch":
        if "D" in shorts or "f" in shorts or "M" in shorts or any(is_long(t, "--force") for t in rest) or \
                (any(is_long(t, "--delete") for t in rest) and any(is_long(t, "--force") for t in rest)):
            raise Deny("force-deleting branches is blocked")
    elif sub == "tag":
        if "d" in shorts or "f" in shorts or any(is_long(t, "--delete") or is_long(t, "--force") for t in rest):
            raise Deny("deleting or moving tags is blocked")
    elif sub == "commit":
        if any(is_long(t, "--amend") for t in rest):
            raise Deny("amending commits is blocked (never rewrite history)")
        if "a" in shorts or any(is_long(t, "--all") for t in rest):
            raise Deny("git commit -a/--all is blocked: stage explicit paths you own")
        if getattr(check_git, "_subagent", False) and "--" not in rest and not getattr(check_git, "_temp_index", False):
            raise Deny("subagents commit with a pathspec (git commit -m msg -- <paths>) or a temp index "
                       "(GIT_INDEX_FILE): the shared index may be stale and would revert other workers' files")
        scan_flag.append("commit")
    elif sub == "rm":
        if "r" in shorts and any(broad(t) or is_protected(resolve(t, cwd)) for t in paths):
            raise Deny("git rm -r of protected paths is blocked")


def strip_wrappers(seg: list[str]) -> list[str]:
    """Drop VAR=val prefixes, shell reserved words and wrapper commands (with their options/args)."""
    while seg:
        t = seg[0]
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", t):
            seg = seg[1:]
            continue
        if Path(t).name not in WRAPPERS:
            break
        name = Path(t).name
        seg = seg[1:]
        while seg and (seg[0].startswith("-") or (name in ("env",) and "=" in seg[0])
                       or (name in ("timeout",) and re.fullmatch(r"[\d.]+[smhd]?", seg[0]))):
            opt = seg[0]
            seg = seg[1:]
            if opt in WRAPPER_OPTS_WITH_ARG.get(name, set()) and seg:
                seg = seg[1:]
    return seg


def check_segment(seg: list[str], cwd: Path, scan_flag: list, depth: int):
    check_git._via_xargs = any(Path(t).name == "xargs" for t in seg[:3])
    # strip env assignments and wrappers
    seg = strip_wrappers(seg)
    if not seg:
        return
    prog = Path(seg[0]).name
    if seg[0].startswith("$") or seg[0].startswith("`"):
        raise Deny(f"unresolved variable or substitution in command position ({seg[0]})")
    if prog in SHELLS or prog == "eval":
        for j, t in enumerate(seg[1:], 1):
            if prog == "eval" or (t.startswith("-") and "c" in t[1:]):
                body = " ".join(seg[j + 1:]) if prog != "eval" else " ".join(seg[1:])
                analyse(body, cwd, scan_flag, depth + 1)
                break
        return
    if prog == "git":
        return check_git(seg[1:], cwd, scan_flag)
    if prog == "cd" and len(seg) > 1:
        return
    if prog in ("rm", "rmdir", "unlink", "shred", "truncate"):
        flags = "".join(short_flags(t) for t in seg[1:] if t != "--")
        recursive = bool(set(flags) & {"r", "R"}) or any(t in ("--recursive",) for t in seg[1:])
        for t in seg[1:]:
            if t.startswith("-") and t != "-":
                continue
            if "$" in t or "`" in t:
                raise Deny(f"{prog} with an unresolved expansion ({t}) is blocked")
            p = resolve(t, cwd)
            if re.search(r"[*?\[]", t) and inside_protected_tree(resolve(re.split(r"[*?\[]", t)[0] or ".", cwd)):
                raise Deny(f"{prog} with a glob inside a protected tree ({t}) is blocked")
            if re.search(r"[*?\[]", t) and resolve(re.split(r"[*?\[]", t)[0] or ".", cwd) in (ROOT, Path("/"), Path(HOME)):
                raise Deny(f"{prog} with a glob at the project/home/root ({t}) is blocked")
            if inside_protected_tree(p):
                raise Deny(f"{prog} inside a protected tree ({t}) is blocked")
            if (recursive and is_protected(p)) or p == ROOT / ".git" or "*" in t and resolve(t.replace("*", ""), cwd) in (ROOT, Path("/"), Path(HOME)):
                raise Deny(f"rm on protected path '{t}' is blocked")
    if prog == "mv":
        for t in [x for x in seg[1:] if not x.startswith("-")][:-1]:
            if is_protected(resolve(t, cwd)) or inside_protected_tree(resolve(t, cwd)):
                raise Deny(f"mv of protected path '{t}' is blocked")
    if prog == "find" and ("-delete" in seg or "-exec" in seg and "rm" in seg):
        for t in seg[1:]:
            if t.startswith("-"):
                break
            if is_protected(resolve(t, cwd)) or inside_protected_tree(resolve(t, cwd)):
                raise Deny("find -delete on a protected path is blocked")


def analyse(cmd: str, cwd: Path, scan_flag: list, depth: int = 0):
    if depth > 4:
        raise Deny("command nesting too deep to analyse")
    cmd, shell_bodies = strip_heredocs(cmd)
    cmd = expand_vars(cmd)  # expand same-command assignments before analysing nested $(...) bodies
    for body in shell_bodies:
        analyse(body, cwd, scan_flag, depth + 1)
    exec_like = re.search(r"\b(sh|bash|zsh|dash|ksh|fish)\b|\beval\b|\bxargs\b|\bssh\b|\balias\b|<<<|\$\(|`", cmd)
    if exec_like:
        for q in quoted_strings(cmd):
            if re.search(r"\b(git|rm|mv|find)\b", q):
                try:  # heuristic pass over quoted text: prose that doesn't parse as shell is not a command
                    analyse(q, cwd, scan_flag, depth + 1)
                except Deny as e:
                    if "could not parse" not in str(e):
                        raise
        for m in re.finditer(r"\$\(([^()]*)\)|`([^`]*)`", cmd):
            analyse(m.group(1) or m.group(2), cwd, scan_flag, depth + 1)
    cmd = expand_vars(cmd)
    segs = segments(cmd)
    for k, seg in enumerate(segs):
        if seg and seg[0] == "cd" and len(seg) > 1:
            cwd = resolve(seg[1], cwd)
            continue
        core = strip_wrappers(seg)
        if core and Path(core[0]).name in SHELLS and all(t.startswith("-") and "c" not in t for t in core[1:]) and k > 0:
            prev = strip_wrappers(segs[k - 1])  # `echo <cmd> | bash` executes <cmd>
            if prev and Path(prev[0]).name in ("echo", "printf", "cat"):
                analyse(" ".join(prev[1:]), cwd, scan_flag, depth + 1)
        check_segment(seg, cwd, scan_flag, depth)
    if depth == 0 and "git:add" in scan_flag and "git:commit" in scan_flag:
        raise Deny("stage and commit in separate commands, so the secret scan sees the staged set")


def secret_scan():
    try:
        r = subprocess.run([sys.executable, str(ROOT / "tools" / "check_secrets.py"), "--staged"],
                           capture_output=True, text=True, cwd=str(ROOT), timeout=90)
    except subprocess.TimeoutExpired:
        raise Deny("secret scan timed out; commit blocked (fail closed)")
    if r.returncode != 0:
        raise Deny("secret check failed on staged files:\n" + (r.stdout + r.stderr).strip()[:800])


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict):
            raise ValueError("hook input is not an object")
        try:  # record which identity fields hook events carry (keys + agent_type only, never the command)
            with open(ROOT / "board" / ".hook_input_keys.log", "a") as f:
                f.write(json.dumps({"keys": sorted(data), "agent_type": data.get("agent_type"),
                                    "has_agent_id": "agent_id" in data}) + "\n")
        except OSError:
            pass
        cmd = (data.get("tool_input") or {}).get("command")
        if cmd is None or cmd == "":
            return 0
        if not isinstance(cmd, str):
            raise ValueError("command is not a string")
        cwd = Path(data.get("cwd") or os.getcwd())
        scan_flag: list = []
        # subagents share one index that goes stale after temp-index commits: require a pathspec or a temp index
        check_git._subagent = "agent_id" in data
        check_git._temp_index = "GIT_INDEX_FILE" in cmd
        analyse(cmd, cwd, scan_flag)
        if any(f == "commit" or not f.startswith("git:") for f in scan_flag):
            secret_scan()
        return 0
    except Deny as e:
        deny_json(str(e) + f" | command: {str(cmd)[:200] if 'cmd' in dir() else ''}")
        return 0
    except Exception as e:  # fail closed
        deny_json(f"guard error ({type(e).__name__}: {e}); denying to fail closed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
