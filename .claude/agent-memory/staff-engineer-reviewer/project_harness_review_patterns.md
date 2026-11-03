---
name: harness-review-patterns
description: Recurring defects in the board CLI / board server / hook guards seen in M0 reviews (rounds 1-2), plus reviewer-environment gotchas
metadata:
  type: project
---

Recurring patterns (M0 round 2, HEAD f413e84):
- Hook guards are token/regex denylists: `board_guard.py` treats ANY token ending in `board.py` as an invocation (false-positives on `test_board.py`, `git diff -- tools/board.py x`); evaded by `bash -c`, `sh -c`, `eval`, globs, `python -c`. Always probe wrappers.
- Hook entry scripts `exec python3`; on system Python 3.9 the `X | None` annotations crash at import (outside try) -> rc 1 -> fail-open. Check `.claude/hooks/*.py` for `from __future__ import annotations` and import-time errors.
- Fixes tend to cover the implemented attack and skip the sibling (CSRF fixed via Origin==Host but no Host allowlist -> DNS rebinding passes). Test the round-1 acceptance line literally.
- Tests mirror the implementation (no Host test, no agent-sync test, no wrong-card/persona test). Agent files drifted from dossiers once between commits; no test.
- Free-text note markers (`assigned:`) used as machine state can be forged by any `note`.

Round 3 (e3fbb08) additions:
- board_guard checks `ba[2] == "done"` positionally; `move T-1 --agent x done` (valid argparse) bypasses it. Always probe flag order, not just wrappers.
- Sentinel-in-review-list pattern (`orchestrator-§7.4` debt entry) short-circuits `_reviews_pass` forever; test "accept -> reopen -> later fail" for any bypass flag.
- Reviewer-guard false positives: `git tag -l`, `branch --show-current`, `stash list`, `reflog`, `chmod +x`; Write tool denies scratchpad while Bash allows it.
- Working tree gets uncommitted orchestrator edits mid-review (D-024); say which tree was tested.
- D-023 threat model (memory/ORCHESTRATOR_DECISIONS.md): plausible accidental spelling = finding; deliberate obfuscation = residual/nit.

**Why:** these recurred across T-001/T-002/T-004 round 1 and 2.
**How to apply:** when re-reviewing harness code, re-run each round-1 acceptance test verbatim, then try the wrapper/sibling variant.

Reviewer-environment gotchas:
- As a native `*-reviewer`, board-guard denies all non-read-only `board.py` subcommands even with a temp BOARD_ROOT; write-path repros cannot be run by reviewers (do not route around with python wrappers; ask the orchestrator). Read-only (`validate/show/list/status/next/inbox`) work with BOARD_ROOT set.
- Bash redirects are checked against the initial cwd and unexpanded `$VAR` paths: use literal absolute scratchpad paths, or put the work in a script file in the scratchpad. `... | tee path` followed by another command on the next line was also falsely denied.
- Agent definitions are a session-start snapshot (my prompt was PROVISIONAL while files were COMPILED); HEAD can move mid-review (orchestrator commits) so re-check `git log -1` before claiming file state.
- A chained shell mutation check in a scratch copy (`rm -rf` + `rsync` + `sed -i` + regenerate) was denied by the permission guard on T-016 (2026-11-01). Do not split the chain to get around it; reason from code and label the finding "not reproduced".
- Generator `--check` compares generated output to files, so regenerating after a generator change passes it. Content invariants (rules present, D.2 keys, 13 files) need explicit asserts (T-016 r1 minor).
- (T-028, 2026-11-01) board-guard fails closed on any Bash command it cannot tokenise ("could not parse command safely (No escaped character)") when a `python3 -c` one-liner contains backslash-escaped backticks or quotes. Put such logic in a script file under artifacts/review-evidence/ and run that file.
- (T-028) reviewer-write-guard denies the Write tool outside reviews/ and artifacts/review-evidence/, including the session scratchpad. Bash redirects to the scratchpad are allowed.
- (T-028) the session header said "not a git repository" but `git rev-parse --is-inside-work-tree` returned true at the repo root. Verify with git, quote the output, do not trust the header.
- (T-028) at f454c41 `app/backend/`, `app/pipeline.py` and `tests/unit/` are empty: `pytest tests/unit -q` exits 5 (no tests), `python -m app.pipeline` exits 1. Doc-stage cards cannot exercise the CLI; say so in `exercised`.
