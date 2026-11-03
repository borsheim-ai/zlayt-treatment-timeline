# T-004 staff-engineer-reviewer review, round 2

**Verdict: changes (0 blockers, 3 majors, 3 minors).** Round-1 major (native load never exercised) is resolved: this review itself ran as a native
`staff-engineer-reviewer`, my attempted Write to `memory/_r2_probe_staff.txt` was denied by `reviewer-write-guard`, and my Bash was denied by the new `board-guard`
keyed on agent_type. The 13 reviewer files are now byte-identical to compiler output and contain their `personas/*.md` dossier verbatim, with no PROVISIONAL
(`artifacts/review-evidence/T-004-r2-agent-sync.txt`). A crafted native-reviewer `board.py move T-1 done` event is denied.

The new `board-guard` is the problem. It is a token matcher with three defects I hit or reproduced directly: it denies legitimate read-only reviewer
commands (it blocked my own `git diff` and `pytest` calls), it is evaded by `bash -c` / `sh -c` / `eval` while the persona body now claims shell writes
are hook-enforced, and it crashes open on the system Python 3.9. Evidence in `artifacts/review-evidence/T-004-r2-*`.

```json
{
 "card": "T-004",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git diff fbe5690..9e759a2 -- .claude tools/compile_agents.py tools/agent_prompt.py; HEAD f413e84 (recompile commit landed during the review); no product files modified",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -> 251 passed in 18.51s",
  "imported tools/compile_agents.py and compared reviewer()/worker() output to every .claude/agents/*.md; grep -l PROVISIONAL .claude/agents/*.md -> 0 files (T-004-r2-agent-sync.txt). Observed that at 9e759a2 the files were stale vs the dossiers (15-line diff for staff-engineer) until f413e84 recompiled",
  "piped 19 crafted events into .claude/hooks/board-guard.sh (agent_type staff-engineer-reviewer, backend, general-purpose, and a main-session event without agent_id): T-004-r2-board-guard-probe.txt",
  "piped 14 shell-write shapes as a reviewer event: T-004-r2-shell-write-probe.txt",
  "ran the hook with PATH=/usr/bin:/bin (python3 = 3.9.6) and with Homebrew python 3.12 first",
  "native checks on myself: Write to memory/_r2_probe_staff.txt -> denied by reviewer-write-guard; ordinary git diff / pytest commands denied by board-guard (false positives, reproduced three times)",
  "ran tools/agent_prompt.py with no arg, unknown name, ../../docs/CONTRACT, qa --brief-file, qa --brief-file /nonexistent, qa; ran compile_agents.py --only typo (wrote 0 files, git status clean)",
  "read .claude/hooks/board_guard.py, board-guard.sh, settings.json hook wiring, tools/tests/test_board_guard.py, the compile_agents.py diff; read artifacts/m0-smoke/"
 ],
 "verdict": "changes",
 "scores": {"spec_conformance": 4, "correctness": 3, "error_handling": 2, "test_quality": 3, "control_integrity": 2},
 "findings": [
  {
   "severity": "major",
   "title": "board-guard false positives: any argument after a path ending in `board.py` is treated as a board subcommand, blocking legitimate reviewer commands",
   "evidence": "board_guard.py board_args(): `if t.endswith(\"board.py\"): return seg[i + 1:]` matches test_board.py, tools/board.py as a file argument, etc. Reproduced live and via the hook (T-004-r2-board-guard-probe.txt): `git diff HEAD~1 -- tools/board.py tools/board_ui.html` -> `DENY: ... reviewers use board.py read-only ... \\`tools/board_ui.html\\` is not allowed`; `.venv/bin/python -m pytest tools/tests/test_board.py -q` -> DENY on `-q`; `wc -l tools/board.py tools/board_server.py` -> DENY. Three of my own commands in this review were blocked this way (`git diff ... tools/board.py tools/board_server.py ...`, `git diff ... test_board.py ...`, `pytest tools/tests/test_board.py -q`). tools/tests/test_board_guard.py has no case for any of them.",
   "why_it_matters": "Reviewers are the ones who diff and test board.py; the guard denies the main thing T-001/T-002 reviewers must do, and the error message is misleading. A guard that blocks normal work gets disabled or worked around, which is worse than none.",
   "fix": "Treat a token as a board.py invocation only when its basename is exactly `board.py` AND it is the script argument of a python/sh interpreter or is executed directly (first token); ignore it when it is an argument to git/pytest/grep/cat/wc/etc. Match subcommands against the known list rather than 'first token after'.",
   "acceptance_test": "test_board_guard.py allow-cases: `git diff HEAD~1 -- tools/board.py tools/board_ui.html`, `pytest tools/tests/test_board.py -q`, `wc -l tools/board.py tools/board_server.py`, `grep x tools/board.py tools/y.py` for a reviewer; deny-cases for `python3 tools/board.py note ...` still pass."
  },
  {
   "severity": "major",
   "title": "Wrapper shells and common writers bypass both the identity rules and the shell-write rules, while the persona body says hooks enforce shell writes",
   "evidence": "T-004-r2-board-guard-probe.txt: for a native reviewer, `bash -c 'python3 tools/board.py move T-1 done'` -> allow; `sh -c \"...\"` -> allow; `eval '...'` -> allow; `python3 tools/boar*.py move T-1 done` -> allow; `python3 -c \"import board; board.main(['move','T-1','done'])\"` -> allow. T-004-r2-shell-write-probe.txt: `bash -c 'echo x > tools/y.txt'`, `sh -c \"echo x > tools/y.txt\"`, `python3 -c open(...,'w')`, `perl -e`, `awk 'BEGIN{print 1 > \"tools/y.txt\"}'`, `eval '...'`, `curl -o tools/y.txt`, `tar xf ... -C tools` -> allow; plain redirect, cp, install, sed -i, git apply -> deny. compile_agents.py (9e759a2) now writes into every reviewer body: 'hooks enforce this for Edit/Write and for shell writes'; board_guard.py docstring admits only 'files written by interpreters (python -c) are not detected'.",
   "why_it_matters": "The persona prompt overstates enforcement, and `bash -c` is the first thing a model reaches for when a direct command is denied. It defeats the no-self-approval (`done`, `--agent orchestrator`) and read-only-reviewer rules at once (see T-001 r2 major).",
   "fix": "Either (a) recursively parse payloads of `bash|sh|zsh -c`, `eval`, `xargs`, `env`, `command`, `nohup` and deny when the interpreter cannot be statically resolved, and add curl -o / tar -C / awk redirects to the checked set; or (b) reword the persona body and docstring to 'Edit/Write are hook-guarded; most shell writes are blocked; interpreter and wrapper writes are not' and record the residual risk in memory/DECISIONS.md. Do (a) for the identity rules regardless.",
   "acceptance_test": "test_board_guard.py: `bash -c '<board.py move X done>'`, `sh -c`, `eval` are denied for subagents; `bash -c 'echo x > tools/y'` is denied for reviewers; or the body text no longer claims shell-write enforcement."
  },
  {
   "severity": "major",
   "title": "board-guard (and the other hooks) fail open on the system Python 3.9 despite the docstring claiming 'Fails closed on errors'",
   "evidence": "board-guard.sh: `exec python3 \"$(dirname \"$0\")/board_guard.py\"`. With `env -i PATH=/usr/bin:/bin ... .claude/hooks/board-guard.sh < event.json`: `File \".../board_guard.py\", line 20, in <module> from git_guard import ...  File \".../git_guard.py\", line 140 def git_alias(sub: str) -> list[str] | None: TypeError: unsupported operand type(s) for |: 'types.GenericAlias' and 'NoneType'`, rc=1, empty stdout. `/usr/bin/python3 --version` -> 3.9.6; `/opt/homebrew/bin/python3` -> 3.12.2. `grep -c 'from __future__ import annotations' .claude/hooks/*.py` -> 0 in all seven files. The import runs outside main()'s try/except, so the 'fail closed' path (deny_json) is never reached. Per Claude Code hook semantics a non-2 non-zero exit is a non-blocking error (stated from documentation, not exercised here).",
   "why_it_matters": "On a machine whose PATH resolves python3 to the macOS system Python (the fresh-install case the installer reviewer cares about), every Bash and git guard silently stops guarding. This is a silent fallback in the safety harness.",
   "fix": "Have each .sh wrapper prefer `$CLAUDE_PROJECT_DIR/.venv/bin/python` then python3 >= 3.10, and print a deny JSON / exit 2 when none is found; add `from __future__ import annotations` to the hook modules; wrap the imports in main() so import errors produce deny_json.",
   "acceptance_test": "A test runs each hook wrapper with PATH limited to /usr/bin:/bin and asserts either a deny decision (exit 2 or deny JSON) or correct operation, never rc 1 with empty stdout."
  },
  {
   "severity": "minor",
   "title": "No test detects agent files drifting from the generator or dossiers (round-1 finding 3, not resolved) and it already happened once",
   "evidence": "tools/tests has no test_agents.py. At 9e759a2 the committed .claude/agents/staff-engineer-reviewer.md differed from compile output by 15 lines (stale dossier text, e.g. file line 56 'Names describe domain meaning' vs dossier 'Currency extraction has unit tests...'); f413e84 ('recompile reviewer bodies from revised dossiers') fixed it by hand. Also, the reviewer prompt I was launched with still began `<!-- PROVISIONAL -->`, i.e. native agent definitions are a start-of-session snapshot.",
   "why_it_matters": "A persona whose checklist is out of date silently reviews against old criteria; the only guard was the orchestrator remembering to recompile.",
   "fix": "Add tools/tests/test_agents.py: every .claude/agents/*.md equals compile_agents output, and no reviewer file contains PROVISIONAL when personas/<slug>.md exists. Document in RUNBOOK that agent changes require a session restart.",
   "acceptance_test": "pytest fails after editing a personas/*.md without recompiling."
  },
  {
   "severity": "minor",
   "title": "agent_prompt.py: usage errors exit 1 not 2, `--brief-file` still tracebacks, frontmatter fallback is still silent (round-1 finding 2, half fixed)",
   "evidence": "tools/agent_prompt.py:8-9 `sys.exit(f\"agent_prompt.py: unknown agent {name!r}...\")` exits 1 (rc=1 for no-arg, unknown, ../../docs/CONTRACT; traversal now refused, good). `agent_prompt.py qa --brief-file` -> `IndexError` traceback at line 20; `--brief-file /nonexistent` -> FileNotFoundError traceback, rc=120. Line 12 `head, body = (m.group(1), m.group(2)) if m else (\"\", txt)` unchanged.",
   "why_it_matters": "The fallback path is what workers use when native loading fails; it should fail with a one-line message and the contract's exit 2.",
   "fix": "argparse with `name` choices from the agents dir and `--brief-file` type=Path; exit 2; treat a missing frontmatter match as an error.",
   "acceptance_test": "`agent_prompt.py qa --brief-file` and `--brief-file /nonexistent` exit 2 with one line, no traceback."
  },
  {
   "severity": "minor",
   "title": "No saved native-load transcript; AC evidence for T-004 still points at the fallback test (round-1 finding 0, resolved in fact, not in the record)",
   "evidence": "ls -la artifacts/m0-smoke/ -> agent-load-tests.md and live-feed.md only, both dated 18:20 (before the restart). board/cards/T-004.md AC 3 evidence: 'haiku subagents loaded paralegal-reviewer and qa via tools/agent_prompt.py fallback ... (native load unavailable mid-session ...)'. The round-2 note cites board/.hook_input_keys.log instead of a saved transcript.",
   "why_it_matters": "Acceptance evidence must be re-checkable by someone who was not in the session; the card's own AC text still says native load was unavailable.",
   "fix": "Save one native worker spawn and one native reviewer spawn (name/model/tools report) plus the denied out-of-bounds Write under artifacts/m0-smoke/, and update AC 3's evidence line.",
   "acceptance_test": "artifacts/m0-smoke/ contains a native transcript citing the agent type resolved by name and a denied Write."
  }
 ],
 "whats_right": [
  "compile_agents.py is a true single generator: all 13 reviewer files and 8 worker files equal its output, each reviewer embeds its personas/*.md dossier verbatim, and none contains PROVISIONAL.",
  "The native reviewer guards attach and fire: reviewer-write-guard denied my Write outside the allowed dirs and board-guard resolved my agent_type, so the identity-based design works for the normal path.",
  "board-guard denies the crafted native-reviewer `board.py move T-1 done` (with and without --agent), `--agent orchestrator` from a general-purpose subagent, and any mutating subcommand for a reviewer, while the main session (no agent_id) is allowed."
 ],
 "questions_for_chris": [
  "Which python3 does the hook shell resolve on your machine in a fresh Claude Code launch (Homebrew 3.12 or /usr/bin 3.9.6)? It decides whether the fail-open finding is live today or only on a fresh install."
 ]
}
```
