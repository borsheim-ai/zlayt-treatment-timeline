# T-004 staff-engineer-reviewer review, round 3 (final, §7.4)

**Verdict: changes (0 blockers, 1 major, 4 minors, 1 nit).** `.venv/bin/python -m pytest tools/tests -q` -> `303 passed in 25.08s`;
`python3 tools/compile_agents.py --check` -> `agent definitions in sync` rc 0.
I exercised the hook by piping crafted PreToolUse events into `.claude/hooks/board-guard.sh` (`artifacts/review-evidence/T-004-r3-board-guard-probe.py`, output
`...-r3-board-guard-probe.out.txt`) and by being the live subject: my own Bash tool is wrapped by the same hook as a native `staff-engineer-reviewer`.
Threat model D-023 applied: only plausible accidental spellings are findings; deliberate obfuscation is listed as residual.

## Round-2 resolution
| r2 finding | status | evidence |
|---|---|---|
| fail-open on system Python 3.9 (my r2 pattern) | RESOLVED | run: `/usr/bin/python3` is 3.9.6; board_guard.py, reviewer_write_guard.py run and emit a deny; the other hooks import clean; `from __future__ import annotations` present in all of them. The `*.sh` wrappers for the three PreToolUse guards now fail closed (deny JSON) when Python exits non-zero without output |
| 1 Bash gap | RESOLVED for plausible spellings | run: crafted native-reviewer event `bash -c 'python3 tools/board.py move T-1 done --agent x'` -> deny; also `bash -lc`, `sh -c`, `eval`, `env`, `timeout`, `nohup`, full interpreter paths, `;`-chains, subshell parens, `cd tools && ./board.py`, quoted `'done'`, `--agent=orchestrator`, `--by orchestrator` -> all denied. `BOARD_ROOT=/tmp/bx ... claim` allowed; `BOARD_ROOT=/tmp/../Users/...` (resolves into the project) denied |
| 2 agent_prompt.py | RESOLVED | run: no arg, unknown, `../../docs/CONTRACT`, `qa --brief-file`, `qa --brief-file /nonexistent` -> one-line message, rc 2, no traceback; test_agents.py covers it |
| 3 no sync check | RESOLVED | `compile_agents.py --check` rc 0; `tools/tests/test_agents.py` runs it and asserts no PROVISIONAL reviewer |
| 4 compile_agents CLI | NOT RESOLVED | run: `python3 tools/compile_agents.py --only typo` -> `wrote 0 agent definition(s) to .claude/agents` rc 0 |
| 5 ADR-000c pointer | NOT RESOLVED | docstring (compile_agents.py:1-6) still says PROVISIONAL and its Usage line omits `--check` |

Legitimate reviewer commands: `git diff 9e759a2..e3fbb08 -- tools .claude`, `git log`, `git show --stat`, `pytest tools/tests/test_board.py -q`, `board.py show/validate/status`,
heredocs and redirects into `artifacts/review-evidence/` were all allowed (no more `test_board.py` false positive). A few read-only forms are still refused (finding 2).

## Findings (see JSON)
One major: the done-closure rule in the hook is positional.

```json
{"card": "T-004", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git diff 9e759a2..e3fbb08 -- .claude tools/agent_prompt.py tools/compile_agents.py tools/tests/test_agents.py tools/tests/test_board_guard.py; native agent session; hook probes",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -> 303 passed in 25.08s",
  "python3 tools/compile_agents.py --check -> agent definitions in sync, rc 0; compile_agents.py --only typo -> wrote 0, rc 0",
  "python3 artifacts/review-evidence/T-004-r3-board-guard-probe.py: 38 crafted events (native reviewer and backend) against .claude/hooks/board-guard.sh incl. the brief's bash -c move-done case and D-023 plausible spellings",
  "/usr/bin/python3 (3.9.6) run of board_guard.py, git_guard.py, reviewer_write_guard.py, stop_guard.py, teammate_idle.py, board_validate.py and board.py status --brief",
  "tools/agent_prompt.py with 5 bad-argument shapes",
  "live hook behaviour on my own tool calls: `git tag -l`, `git branch --show-current`, `git stash list`, `git reflog -3`, `chmod +x`, and a Write into the scratchpad were denied; git log/diff/pytest/curl allowed",
  "BOARD_ROOT=<scratch> python3 tools/board.py move T-004 --agent qa done -> reached application logic (`already done`), proving argparse accepts flag-before-positional order",
  "read board_guard.py, the three .sh wrappers, settings.json hook wiring, git diff of agents/*.md"],
 "verdict": "changes",
 "scores": {"guard_coverage_plausible_spellings": 3, "fail_closed_behaviour": 4, "agent_definition_integrity": 4, "false_positive_rate": 3},
 "findings": [
  {"severity": "major", "title": "board-guard's 'only the orchestrator moves cards to done' rule only matches the positional spelling `move <id> done`",
   "evidence": ".claude/hooks/board_guard.py:117 `if sub == \"move\" and len(ba) > 2 and ba[2] == \"done\":`. Probe output (T-004-r3-board-guard-probe.out.txt): `A (want D) flag-before-positional: move T-1 --agent backend done` and `A (want D) flag-first: move --agent backend T-1 done`, both from agent_type backend; the same command with `done` in third position is denied. `python3 tools/board.py move T-004 --agent qa done` is parsed by the real CLI (reached `T-004 already done`).",
   "why_it_matters": "Flags before the status are an ordinary way to write an argparse command, so this is a plausible accident, not obfuscation: D-023 item (1) says it must be fixed with a regression test. It defeats the only identity-based control on closing cards. The CLI still requires all AC, a passing review set and agent != claimer, so the reachable harm is a non-claiming worker closing a reviewed card, not forging reviews; that is why this is major and not blocker.",
   "fix": "Parse the move arguments the way argparse does: drop the flags and their values (`--agent X`, `--note X`, `--accept-debt X`, `--agent=X`) from the arg list, then take positionals [id, status]; deny when status == 'done' or when `--accept-debt` appears. Better: build the same argparse parser (or reuse board.build_parser) in the hook.",
   "acceptance_test": "tools/tests/test_board_guard.py adds cases `move T-1 --agent backend done`, `move --agent backend T-1 done`, `move T-1 --note x done --agent backend` for agent_type backend and qa, all expecting deny; `move T-1 in_review --agent backend --note done` stays allowed."},
  {"severity": "minor", "title": "Read-only git forms and `chmod +x` are denied for reviewers",
   "evidence": "Probe lines `D (want A) git tag -l`, `git branch --show-current`, `git stash list`, `git reflog -3`, `chmod +x /tmp/x.sh`, `chmod +x artifacts/review-evidence/p.sh`; live: `board-guard: reviewers may not run `git tag` in the project`, and `reviewers may only write under reviews/ ... (chmod +x)`. Code: board_guard.py:25 MUTATING_GIT lists whole subcommands (tag, branch, stash, reflog); board_guard.py:155 treats the mode `+x` as a path because it does not start with '-'. `git reflog` is also refused by git-guard.",
   "why_it_matters": "The persona rules require reviewers to quote git tags/log as evidence; the false positives push reviewers toward workarounds. D-023 item (1) covers accidental over-blocking of ordinary commands only loosely, but this blocks routine, legitimate review work (I hit it three times).",
   "fix": "Allow read-only flag forms: `tag -l/--list`, `branch --list/--show-current/-a/-v`, `stash list/show`, `reflog show`; skip a leading mode operand (`+x`, `u+x`, `755`) for chmod and check only the file operands.",
   "acceptance_test": "probe: those five commands allowed for a reviewer; `git tag v1`, `git branch x`, `git stash`, `chmod +x tools/board.py` still denied."},
  {"severity": "minor", "title": "Write tool and Bash guard disagree about where reviewers may write",
   "evidence": "Write to the scratchpad under /private/tmp/claude-501/... -> `reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/`; the same path via a Bash redirect is allowed by board_guard.allowed_write (bases include /tmp, /private/tmp, scratchpad_dir, /dev). The agent body (compiled) says only reviews/, artifacts/review-evidence/ and the own memory dir.",
   "why_it_matters": "Two hooks, two policies, and the written policy matches only one; reviewers and the orchestrator cannot predict outcomes.",
   "fix": "Pick one policy; if scratch is allowed, add it to reviewer_write_guard.py and the agent text, otherwise remove /tmp and the scratchpad from allowed_write.",
   "acceptance_test": "a test table in test_board_guard.py / test_reviewer_write_guard asserting the same verdict from both hooks for the same target paths."},
  {"severity": "minor", "title": "`compile_agents.py --only <typo>` succeeds with 0 files; docstring stale (r2 #4/#5 unresolved)",
   "evidence": "Run: `python3 tools/compile_agents.py --only typo` -> `wrote 0 agent definition(s) to .claude/agents`, rc 0. compile_agents.py:1-6 docstring still says reviewer bodies are PROVISIONAL and the Usage line omits --check.",
   "why_it_matters": "A mistyped name looks like success (silent no-op).",
   "fix": "Exit 2 when an --only name matches no agent; update the docstring and add the ADR pointer.",
   "acceptance_test": "`--only typo` exits 2 with 'unknown agent'."},
  {"severity": "minor", "title": "Runtime lock file with session id and pid is committed",
   "evidence": "`git ls-files .claude/scheduled_tasks.lock` -> listed; content `{\"sessionId\":\"6ddf8076-...\",\"pid\":2007,...}`; not in .gitignore. Added in the 9e759a2..e3fbb08 range.",
   "why_it_matters": "A per-session runtime artifact in history will churn on every session and records host process data.",
   "fix": "git rm --cached it and add `.claude/scheduled_tasks.lock` to .gitignore.",
   "acceptance_test": "`git ls-files .claude | grep lock` is empty after a session starts."},
  {"severity": "nit", "title": "D-023 residual (not counted as findings): interpreters, globs and unparseable quoted text",
   "evidence": "Probe: `python3 -c \"import board...\"`, `python3 tools/boar*.py move ...`, `python3 -m board ...` allowed; board_guard.py:99 `except Exception: pass` skips nested quoted strings that fail to parse.",
   "why_it_matters": "Documented residual under D-023, covered by append-only activity log and orchestrator re-verification; listed so the gate record has it. The hook docstring says 'Residual risk: python -c' but does not cite D-023, globs, -m or the swallowed parse error.",
   "fix": "Name D-023 and the residual list in the board_guard.py docstring; log (stderr) when a nested string cannot be parsed.",
   "acceptance_test": "docstring lists the residuals; a nested unparseable string produces a log line."}
 ],
 "whats_right": [
  "Python 3.9 fail-open is closed and the three PreToolUse wrappers deny when the interpreter crashes without a decision.",
  "A native reviewer's wrapped `bash -c`/`sh -c`/`eval`/env/timeout move-done attempts are denied, while git diff, pytest and board.py show/validate are allowed.",
  "test_agents.py makes agent drift and PROVISIONAL bodies a test failure (`--check` rc 0 now)."],
 "questions_for_chris": []}
```
