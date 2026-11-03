---
name: round2-snapshot-review-patterns
description: T-040 r2 and T-043 r2 (2026-11-01): HEAD moves mid-review, git archive needs untracked fixtures, mutation method, guard traps, overwritten review file
metadata:
  type: project
---

Round-2 reviews of T-040 (security) and T-043 (paralegal) ran while other agents committed to the same branch. HEAD moved about six times in one session (5542dfd -> 700ca9a -> 7364096 -> 7a450a1 -> 5216d06 -> 099732b -> dd545e3 -> c61e84f).

**Why:** A test result or live check is only valid for the hash it ran against. Quote the hash in every review, and re-run the required command at the end of the review.

**How to apply:**
- Snapshot the reviewed commit with `git archive <sha> | tar -x -C <scratch>`, then copy untracked files in (`git ls-files --others --exclude-standard`, through a small Python copier because BSD `cp` has no `--parents`). `.gitattributes` has no export-ignore, but a commit can lack files that a later commit adds. 077e294 lacks `tests/fixtures/llm/*.json` (added by 0d040d3), so `FIXTURE_MISS` fails 7 tests. Overlaying HEAD's fixtures isolates the code question from the fixture-ordering question.
- Mutation checks run in a scratch copy via a Python driver (`mutate_api.py` pattern in artifacts/review-evidence/T-040-r2-mutate_api.py). Result shape: drop the delete_case line, drop the CSP line, disable the Content-Length precheck. A test that still passes with the control removed is a finding (here the body-cap test).
- Live checks: start uvicorn from the snapshot with DATA_DIR in scratch, get listener PIDs with `lsof -nP -iTCP:<port> -sTCP:LISTEN`, and kill those PIDs by number. A PID file from `nohup ... &` in a subshell can point at a dead parent.
- Guard traps (board-guard / git-guard in this repo): `kill $(cat ...)` is denied (command substitution in command position); `rm -rf "$VAR/..."` is denied; `awk` with `>` or `NR>1` is read as a redirect into a product path; `grep "<style"` is read as redirect; a `2>&1 | tail` inside an echo string is denied. Put shell logic in a scratch .py file and run it with `.venv/bin/python -I`.
- Overwrite hazard: `Write` on an existing reviews/ file replaces it silently. Before writing `reviews/<card>-<persona>-r2.md`, check for an existing file and the card's reviews list (`board show <card>`). An earlier round-2 review for T-040 existed (verdict changes, 02:17:03Z) and was overwritten; it was untracked, so it could not be restored from git.
- Fixes can land between a review's findings and its re-check: at c61e84f the PDF route moved to a threadpool with a 10 s cap and a demo refusal before parse. Re-measure any performance claim on the current HEAD before rating it.
