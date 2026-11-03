# T-003 security review (Hooks + settings) — verdict: fail

Deterministic checks: `pytest tools/tests` passes (37), but the git-guard tests only cover the canonical spelling of each command. Hands-on bypass attempts (evidence under artifacts/review-evidence/T-003-*.txt) show the guard is a literal-string regex applied after quote-stripping, so it is bypassed by quoting, git global options, bundled flags, `+refspec`, path spellings of protected dirs, shell re-entry and variable indirection. The staged-secret check on commit is skipped for `git -c ... commit`. Blockers: 3. Majors: 4. Spec violations are labelled as blockers; hardening beyond the spec is major/minor.

```json
{
 "card": "T-003",
 "persona": "security-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "commit range e37efb3..fbe5690; .claude/settings.json, .claude/hooks/*.sh|*.py, tools/tests/test_hooks.py; contract \u00a71.10, \u00a74.2, \u00a74.3, \u00a712",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -> 37 passed",
  "read settings.json (diffed against CONTRACT \u00a74.2) and all 10 hook files",
  "piped 346 crafted commands into git-guard.sh (results: artifacts/review-evidence/T-003-git-guard-probe.txt)",
  "piped 35 staged-secret commit variants into git-guard.sh in a scratch repo with an sk-ant-shaped string staged (artifacts/review-evidence/T-003-git-guard-commit-secret-probe.txt)",
  "piped 24 path cases into reviewer-write-guard.sh (artifacts/review-evidence/T-003-reviewer-write-guard-probe.txt)",
  "ran stop-guard (incl. 7-block stall), teammate-idle, board-validate and crash/malformed-input cases on a scratch copy of the repo (artifacts/review-evidence/T-003-other-hooks-probe.txt)",
  "read reviewer agent frontmatter (tools list, hook matcher)",
  "git log -p | grep -c sk-ant = 4, all pattern/doc text, no key material; .env not tracked (git check-ignore -v .env -> .gitignore:1)"
 ],
 "verdict": "fail",
 "scores": {
  "git_guard_coverage": 1,
  "secret_commit_block": 2,
  "fail_closed_behavior": 2,
  "reviewer_write_guard": 3,
  "stop_and_idle_hooks": 4,
  "settings_vs_contract": 4
 },
 "findings": [
  {
   "severity": "blocker",
   "title": "git add -A / add . is bypassed by trivially different spellings of the same command",
   "evidence": "git_guard.py:11 regex is applied after strip_quoted() (line 40-44) which turns every quoted token into ''. ALLOW (probe file lines): `git add -- .`, `git add :/`, `git add ./`, `git add *`, `git add \".\"`, `git add \"-A\"`, `git -C . add -A`, `git -c core.x=y add -A`, `git --no-pager add -A`, `git add -fA`, `git add -vA`, `git add -Av`, `git add -n -A`, `git add /Users/arsis/zlayt-pm-project`, `git \"add\" -A`, `\"git\" add -A`. settings.json deny rules are prefix patterns on the literal strings and do not cover these either.",
   "why_it_matters": "CONTRACT \u00a74.3 and \u00a71.10 require `git add -A/.` to be denied by the hook; `-fA` also force-adds ignored files such as .env. The deny is a literal-string match, so an agent that merely quotes an argument or inserts a git global option walks straight past it; every one of these is a form agents emit naturally.",
   "fix": "Tokenize with shlex (after heredoc stripping), drop git global options (-C <p>, -c <kv>, --no-pager, --git-dir=, --work-tree=, --paginate), strip quotes per token, resolve the subcommand, then evaluate rules on (subcommand, args): add with any of -A/--all/-u/./:/ /*/an absolute path equal to ROOT or ancestor, or any short-flag cluster containing A; treat pathspec `.` `./` `:/` `*` `:(top)` as 'everything'.",
   "acceptance_test": "test_hooks.py DENY list gains every ALLOW line above that is a real add-everything form, and the test run fails if any returns allow."
  },
  {
   "severity": "blocker",
   "title": "Staged-secret check on `git commit` is skipped for `git -c ... commit`, `git --no-pager commit`, quoted `git`/`commit`, and aliases",
   "evidence": "git_guard.py:67 `re.search(r\"\\bgit\\s+(-C\\s+\\S+\\s+)?commit\\b\", cmd)` only tolerates `-C <path>`. In a scratch repo with an sk-ant key staged (artifacts/review-evidence/T-003-git-guard-commit-secret-probe.txt): ALLOW for `git -c user.name=x commit -m x`, `git -c user.email=a@b -c user.name=x commit`, `git --no-pager commit`, `git --work-tree=. commit`, `\"git\" commit`, `git \"commit\"`, `git ci`, `git -c alias.c=commit c`, `sh -c \"git -c a=b commit\"`; `git write-tree`/`git update-ref` plumbing never checked. Baseline `git commit -m x` is correctly DENY.",
   "why_it_matters": "Non-negotiable 10 ('Secrets never enter git... a pre-commit check blocks key-shaped strings') and \u00a74.3 ('any git commit while .env or a key-shaped string is staged'). `git -c user.name=... -c user.email=... commit` is the single most common way an agent commits when identity is not configured, so the secret gate is absent in the exact path most likely to be used. There is also no .git/hooks/pre-commit (only .sample files), so nothing else backs it up for a human or non-Bash path.",
   "fix": "(1) Reuse the tokenizer from the finding above to detect subcommand == commit regardless of global options/quotes. (2) Also install a real .git/hooks/pre-commit that runs tools/check_secrets.py --staged (and document install in the runbook) so the gate does not depend on regex-matching the Bash string. (3) Run the secrets check for any command whose subcommand is commit, commit-tree, or an alias defined in git config.",
   "acceptance_test": "With sk-ant key staged in a scratch repo, hook denies each of the commit variants listed; `git commit` run directly in a terminal is rejected by the pre-commit hook."
  },
  {
   "severity": "blocker",
   "title": "Force-push / reset --hard / clean -f guards miss common spellings, including `git push origin +main`",
   "evidence": "ALLOW in artifacts/review-evidence/T-003-git-guard-probe.txt: `git push origin +main`, `git push origin +HEAD:main`, `git push origin +refs/heads/main:refs/heads/main`, `git push -uf origin main`, `git push -fu origin main`, `git push origin main -vf`, `git push --mirror`, `git push origin --delete main`, `git push -c receive.denyNonFastForwards=false origin +main`, `git reset -q --hard`, `git clean --force`, `git clean -d -f`, `git push origin main \"--force\"`, `git push origin main --for''ce`. git_guard.py:7 only matches `\\s--force\\b|\\s-f\\b|--force-with-lease` and git_guard.py:8-9 require `--hard` immediately after `reset` and `-\\w*f` as the first flag after `clean`.",
   "why_it_matters": "\u00a74.3 lists force pushes, reset --hard and clean -f as denied. `+refspec` is the other canonical force push (explicitly in the brief), and bundled short flags / flags in a different order are routine.",
   "fix": "On the tokenized argv: push is a force push if any arg matches -[a-zA-Z]*f[a-zA-Z]*, --force*, or a refspec starting with '+' or '--mirror'; reset is blocked if '--hard' appears anywhere in args; clean is blocked if any short cluster contains f or any arg is --force, unless -n/--dry-run is also present.",
   "acceptance_test": "All listed ALLOW commands move to the DENY list in test_hooks.py; `git push origin main`, `git clean -n`, `git reset --soft HEAD~1` remain allowed."
  },
  {
   "severity": "major",
   "title": "rm -r protection misses -R, wrapped commands, and absolute/relative forms of board/, memory/, reviews/, .git and the project root",
   "evidence": "git_guard.py:61 `toks[:1]==['rm'] and any(t.startswith('-') and 'r' in t ...)` and RM_TARGETS (line 17) are literal-string sets. ALLOW: `rm -R -f board`, `rm -Rf board`, `rm -f -R board`, `rm -rf ./board`, `rm -rf /Users/arsis/zlayt-pm-project/board`, `.../memory`, `.../reviews/`, `rm -rf board/*`, `rm -rf board/cards`, `rm -rf ./.git`, `rm -rf .git/objects`, `rm -rf $PWD`, `rm -rf \"$(pwd)\"`, `rm -rf ${HOME}`, `rm -rf ..`, `rm -rf ./*`, `rm -rf .*`, `sudo rm -rf /`, `env rm -rf board`, `command rm -rf board`, `/bin/rm -rf board`, `xargs rm -rf`, `find . -delete`, `mv board /tmp/x`, `mv .git /tmp/x`. Caught: `rm -rf board`, `rm -fr board`, `rm -r -f board`, `rm -rf /Users/arsis/zlayt-pm-project`.",
   "why_it_matters": "CONTRACT \u00a712: 'Never delete board/, memory/, reviews/'; \u00a74.3 lists `/`, `~`, `.git`, project root. The guard protects the bare name but not the same path spelled differently, and uppercase -R / --recursive is not recognised at all.",
   "fix": "Normalize each rm operand (expanduser, expandvars, realpath relative to cwd) and block if it equals or is an ancestor/descendant-root-of-protected set {/, $HOME, ROOT, ROOT/.git, ROOT/board, ROOT/memory, ROOT/reviews}; recognise -r/-R/--recursive; strip leading env/command/sudo/\\ /absolute path prefixes; deny rm operands containing unresolved $VAR/backtick/$( ) when -r is present.",
   "acceptance_test": "Listed rm/mv ALLOW lines become DENY; `rm -rf artifacts/tmp/x` and `rm -rf app/__pycache__` stay allowed."
  },
  {
   "severity": "major",
   "title": "Shell re-entry bypasses: heredoc bodies piped/redirected into a shell, here-strings, other shells, env-var indirection",
   "evidence": "strip_heredocs() (git_guard.py:21-34) deletes every heredoc body unconditionally. ALLOW: `bash <<EOF\\ngit add -A\\nEOF`, `cat <<EOF | sh\\ngit add -A\\nEOF`, `bash <<<'git add -A'`, `sh <<< \"git reset --hard\"`, `echo 'git add -A' | sh`, `dash -c 'git add -A'`, `ksh -c ...`, `bash --norc -c ...`, `sh -c \"git add .\"` (SHELL_EXEC regex line 37 covers only bash|sh|zsh followed by -\\w*c). Indirection: `CMD=\"git add -A\"; $CMD`, `X=add; git $X -A`, `FORCE=-f; git push $FORCE origin main`, `D=/; rm -rf $D`, `git reset --$(echo hard)`.",
   "why_it_matters": "The brief explicitly asks about env-var indirection; none is detected. A regex hook cannot be complete, so the contract's 'deny rules are defense in depth' only helps if the layers differ, but the settings.json deny rules are the same literal prefixes and share all these holes.",
   "fix": "Do not strip heredoc bodies when the command is fed to a shell (bash/sh/zsh/dash/ksh, source, `.`); treat any unexpanded `$VAR`/`$(...)`/backtick appearing in command position or as a git/rm/push argument as deny-with-explanation ('use literal commands'); extend SHELL_EXEC to any *sh and `-c` anywhere in the flag cluster. Record the residual risk (python -c os.system etc.) in memory/LESSONS.md as accepted.",
   "acceptance_test": "Listed shell-entry and indirection commands are denied; `cat > f.py <<'EOF' ... 'git add -A' ... EOF` (existing allow test) still passes."
  },
  {
   "severity": "major",
   "title": "Guards fail open on internal errors and malformed input; contract's `onFailure: block` was dropped",
   "evidence": "artifacts/review-evidence/T-003-other-hooks-probe.txt tail: `{\"tool_input\":{\"command\":123}}` -> AttributeError traceback, rc=1; `git commit` with unusable CLAUDE_PROJECT_DIR -> FileNotFoundError, rc=1; malformed JSON on stdin -> rc=0 silent allow. _common.py:9-14 read_input() swallows parse errors and returns {}; git_guard.py:68-71 subprocess.run(..., timeout=60) has no TimeoutExpired handler. settings.json PreToolUse entry has no onFailure (CONTRACT \u00a74.2 had `\"onFailure\": \"block\"`).",
   "why_it_matters": "In Claude Code, exit 1 is a non-blocking hook error, so a crash or a >60 s secrets scan lets the command through. A security gate must fail closed (exit 2 / deny) or the first unexpected input silently disables it.",
   "fix": "Wrap git_guard.main() and reviewer_write_guard.main() in try/except that emits a deny (or exit 2) with the exception text; handle TimeoutExpired from check_secrets as deny; treat non-JSON stdin in a PreToolUse guard as deny. If `onFailure` is not a real field, record that in LESSONS.md and rely on the try/except.",
   "acceptance_test": "New tests: non-string command, bad CLAUDE_PROJECT_DIR, check_secrets timeout (monkeypatched) and garbage stdin each produce deny/exit 2 for git-guard."
  },
  {
   "severity": "major",
   "title": "reviewer-write-guard only covers Edit|Write, but every reviewer also has Bash; and the agent-memory carve-out is the whole directory",
   "evidence": ".claude/agents/security-reviewer.md frontmatter: `tools: Read, Grep, Glob, Bash, Write` with hook matcher `Edit|Write` (same in all 13 *-reviewer.md). reviewer_write_guard.py:23 allows anything under .claude/agent-memory (probe: `agent-memory/backend/m.md` ALLOW). A reviewer can `echo x > tools/board.py` or `sed -i` without touching the guard.",
   "why_it_matters": "\u00a71.7/\u00a74.3: 'Reviewers critique; they do not fix' is stated as hook-enforced. As built, the enforcement is honor-system for any Bash write and reviewers can also edit other personas' memory (a prompt-injection / poisoning path).",
   "fix": "Add a Bash PreToolUse matcher to reviewer frontmatter that denies write-looking commands (>, >>, tee, sed -i, mv, cp, rm, git add/commit, python -c open(...,'w')) targeting paths outside the allowed set, or drop Bash from reviewers that don't need it; restrict the memory carve-out to .claude/agent-memory/<own-name>/ (take name from hook input agent_type). Until then, state the limitation in CONTRACT \u00a74.3 so it is not claimed as enforced.",
   "acceptance_test": "Probe: reviewer Bash `echo x > tools/x.py` is denied; writing .claude/agent-memory/backend/x.md as security-reviewer is denied."
  },
  {
   "severity": "minor",
   "title": "board-validate silently skips when CLAUDE_PROJECT_DIR is a symlinked path; crashes on path == root",
   "evidence": "T-003-other-hooks-probe.txt: broken card via symlinked CLAUDE_PROJECT_DIR -> rc=0 (no validation); path == project root -> IndexError rc=1. _common.py:5 ROOT is not .resolve()d while board_validate.py:18 compares against p.resolve().",
   "why_it_matters": "Validation can be silently off depending on how the project is mounted; same ROOT mismatch makes reviewer-write-guard deny everything (fails closed, but unusable).",
   "fix": "ROOT = Path(...).resolve() in _common.py; guard rel.parts non-empty.",
   "acceptance_test": "Test with a symlinked project dir: broken card -> exit 2."
  },
  {
   "severity": "minor",
   "title": "TeammateIdle debug log writes raw hook input to disk with no redaction",
   "evidence": "teammate_idle.py:12-13 writes json.dumps(raw) to board/.hook_debug.log (gitignored at .gitignore:17). Role match (line 14-15) uses \\bbackend\\b on free-text name fields, so a teammate named 'backend-2' or text containing a role word maps to a role.",
   "why_it_matters": "Hook payloads can carry prompts/transcript paths; it is gitignored so low risk, but contract \u00a712 forbids sensitive content in logs. Not verified against real payload (handoff admits input shape is unverified).",
   "fix": "Log only the key names and agent_type/teammate_name values; delete the file after the mapping is confirmed.",
   "acceptance_test": "Debug log contains no values beyond the name fields."
  }
 ],
 "whats_right": [
  "Hooks are thin .sh wrappers over testable Python and resolve scripts via $CLAUDE_PROJECT_DIR; settings.json matches CONTRACT \u00a74.2 deny rules exactly, with a documented reason for dropping `args`",
  "reviewer-write-guard correctly resolves traversal (`reviews/../tools`), prefix siblings (`reviews-evil/`), tilde and out-of-tree cwd to DENY, and stop-guard ignores subagents, honours board/STOP and trips the stall guard at the 6th block",
  "Quoted prose and heredoc file content that merely mention `git add -A` are allowed (no false-positive lockout) and covered by tests"
 ],
 "questions_for_chris": [
  "Is a real .git/hooks/pre-commit acceptable (not only the Claude Code hook)? The contract says 'pre-commit check' but only specifies the hook."
 ]
}
```
