# T-001 staff-engineer-reviewer review, round 3 (final, §7.4)

**Verdict: changes (0 blockers, 1 major, 5 minors, 1 nit).** `.venv/bin/python -m pytest tools/tests -q` -> `303 passed in 25.08s`.
Reviewed `git diff 9e759a2..e3fbb08 -- tools .claude` and exercised the CLI. Write-path repros ran with `BOARD_ROOT=<scratch fixture>`; the real
repo's `git status --porcelain` hash was identical before and after (script: `artifacts/review-evidence/T-001-r3-repro.sh`, output `...-r3-repro.out.txt`).
Note: the working tree held uncommitted edits (D-024 `--accept-debt` threshold, Office view) that appeared mid-review; findings below are against `e3fbb08`
and the touched lines are unchanged in the working tree.

## Round-2 resolution
| r2 finding | status | evidence |
|---|---|---|
| 0 `review` persona/card/verdict | RESOLVED | run: wrong `--persona` -> `does not match the review file's persona`; wrong card -> `review file is for card 'T-002', not T-001`; file without persona -> `review JSON missing 'persona'` |
| 3 self-approval / trust model | RESOLVED as residual under D-023 | CLI still trusts `--agent`; the hook layer is T-004's finding (flag-order bypass there). D-023 documents the model in memory/ORCHESTRATOR_DECISIONS.md only |
| 4 malformed `reviews` traceback | RESOLVED | run: `reviews:["junk"]` done card -> `INVALID: ... bad review entry junk` rc 2, no traceback; all-files `validate` completes |
| 5 shallow review-file validation | NOT RESOLVED | run: two ```json blocks (pass then fail) accepted, first wins; no `model`/`scope` required |
| 6 pre-rework pass counts | NOT RESOLVED | `_reviews_pass` is still latest-verdict-per-persona with no round awareness |
| 7 stale claim lock | NOT RESOLVED | run: `ready` card + leftover `claim-T-001.lock` -> `already claimed (lock held by w1)` rc 2, no recovery path |
| 8, 9 | RESOLVED | previously verified; `gate` stub refusal at board.py:1000 |

New in this round and verified by run: forged `assigned:` note from a worker no longer suppresses the actionable (test + code), a stale dispatch marker
is ignored after resubmission, `--accept-debt` refuses non-orchestrator and `<3` rounds and writes SCOPE_CUTS.

## Findings (see JSON)
- **major** The debt-acceptance review entry makes the done gate pass forever. Repro F: close T-004 with `--accept-debt`, reopen it, file a `fail` review,
  rework, `move done` succeeds and `validate` is clean while the persona's latest verdict is `fail`.
- minor `review --file` accepts any path (absolute path outside `reviews/` recorded as a review).
- minor `needs_chris -> done` skips the review gate in `cmd_move` and relies on a title-substring sentinel in `check_meta`; no test covers it.
- minor r2 #5 / #6 / #7 carried over (grouped as one finding each in JSON where evidence differs).
- minor `test_stale_dispatch_marker_ignored_after_resubmit` uses `time.sleep(1.1)` (wall-clock dependent).
- nit D-023 residual: a newline inside `note --text` forges an `orchestrator: assigned:` line.

```json
{"card": "T-001", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git diff 9e759a2..e3fbb08 -- tools .claude (board.py focus); temp BOARD_ROOT fixtures; round 3",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -> 303 passed in 25.08s",
  "bash artifacts/review-evidence/T-001-r3-repro.sh (temp BOARD_ROOT; real repo git-status hash unchanged): review persona/card mismatch, review file outside reviews/, two json blocks, needs_chris->done, --accept-debt (backend refused, orchestrator ok, SCOPE_CUTS row), debt-accepted card reopened with a later FAIL review then done, newline-injected orchestrator marker, reviews:[junk] validate",
  "claim on a ready card with a leftover claim lock in a second temp fixture",
  "python3 tools/compile_agents.py --check; /usr/bin/python3 (3.9.6) status --brief",
  "git diff 9e759a2..e3fbb08 -- tools/board.py tools/tests/test_board.py read line by line"],
 "verdict": "changes",
 "scores": {"correctness": 3, "failure_visibility": 4, "determinism_and_tests": 3, "trust_model_clarity": 3},
 "findings": [
  {"severity": "major", "title": "Debt-acceptance entry permanently satisfies the review gate; a later FAIL review no longer blocks done",
   "evidence": "board.py:318 `if any(... r.get('persona') == 'orchestrator-§7.4' and r.get('debt') ...): return True` runs before the per-persona latest-verdict check; entry appended at board.py:643. Repro (artifacts/review-evidence/T-001-r3-repro.out.txt, section F): `move T-004 done --agent orchestrator --accept-debt ...` ok; `move T-004 in_progress --agent orchestrator --note ...`; `review ... --verdict fail` (T-004 now changes_requested, round 4); claim, `move in_review`; `move T-004 done --agent orchestrator` -> `T-004: in_review -> done`; card frontmatter then lists the fail review as the persona's latest, and `validate` stays ok because check_meta calls the same _reviews_pass.",
   "why_it_matters": "The done gate (>=1 pass and every persona's latest verdict = pass) is a spec constraint; after one debt acceptance the card silently loses it for its whole life, and the orchestrator believes it is still enforced. D-024 (uncommitted) lowers the debt threshold to 2 rounds, so this path gets used more.",
   "fix": "Scope the debt entry to the round it was granted: honour it only if no review entry is newer than it (compare `at`), or store the round number and require meta['rounds'] == that round; otherwise fall through to the latest-verdict check.",
   "acceptance_test": "test: accept debt after N rounds, reopen, record a fail review, rework to in_review -> `move done` exits 2 with 'cannot move to done' and `validate` reports 'status done without a passing review set' if the frontmatter is forced to done."},
  {"severity": "minor", "title": "`review --file` accepts a path outside reviews/",
   "evidence": "board.py:734 `rp = ROOT / a.file` (absolute path wins). Repro: `review T-002 --persona staff-engineer-reviewer --model m --verdict pass --file <scratch>/outside.md` -> `review staff-engineer-reviewer (m): pass` rc 0, recorded in card.",
   "why_it_matters": "The recorded review file is the audit evidence; a review that lives in /tmp is not in the repo and cannot be re-read by the gate.",
   "fix": "Resolve the path and require it to be a file under ROOT/reviews/ (same realpath check validate already does).",
   "acceptance_test": "`review T-1 ... --file /tmp/x.md` and `--file ../x.md` exit 2 with 'must be inside reviews/'."},
  {"severity": "minor", "title": "needs_chris -> done skips the review gate; exemption is a title substring and untested",
   "evidence": "board.py:645 `elif cur == 'needs_chris': if not a.note ...` (no review check) and board.py:310 `meta.get('created_by') == 'orchestrator' and 'NEEDS_CHRIS' in str(meta.get('title'))`. `grep -n needs_chris tools/tests/*.py` -> no hits. Repro: worker-created card in needs_chris, `move done --agent frontend --note ...` is refused only by the save-time check_meta with the misleading message `refusing to write invalid card: status done without a passing review set`.",
   "why_it_matters": "Two layers disagree about the same rule and the real gate is a magic string in a title; nothing proves a --note is Chris's answer.",
   "fix": "Make the rule explicit in cmd_move (only cards whose `needs_chris` reason is an owner question, e.g. a `needs_chris_answer` field) and give the refusal a direct message; add tests for both outcomes.",
   "acceptance_test": "tests: orchestrator-created needs_chris card + --note -> done; worker card in needs_chris -> done refused with a message naming needs_chris."},
  {"severity": "minor", "title": "Review-file validation still shallow (r2 #5 unresolved)",
   "evidence": "Repro: reviews/T-002-nomodel.md with two ```json blocks (verdict pass, then fail) and no model/scope -> `review ... --verdict pass` accepted. board.py:765-774 review_json returns the first block with a verdict; validate_review_file (board.py:893-921) requires card/persona/verdict/findings/exercised only.",
   "why_it_matters": "The second block says fail; which one the gate reads depends on file order. Appendix D.2 requires model and scope.",
   "fix": "Reject files with more than one json block carrying a verdict; require model and scope keys.",
   "acceptance_test": "validate on a two-block file and on a file without `model` both exit 2."},
  {"severity": "minor", "title": "Stale claim lock has no recovery path; pre-rework pass still counts (r2 #7, #6 unresolved)",
   "evidence": "Repro (fixture): ready card + board/.locks/claim-T-001.lock -> `claim` exits 2 `already claimed (lock held by w1)`. board.py:317-325 _reviews_pass keeps persona A's round-1 pass after the code changed in rework.",
   "why_it_matters": "A crashed claimer wedges a card until someone deletes a hidden file; an approval of superseded code satisfies the final gate.",
   "fix": "Claim should reclaim a lock whose card is `ready` with claimed_by null (or whose age exceeds the stall limit); reset or timestamp-compare reviews against the last move to in_review.",
   "acceptance_test": "test: lock present, card ready, claimed_by null -> claim succeeds; pass(A) in round 1, changes(B), rework, B pass without A re-review -> done refused (or documented as intended)."},
  {"severity": "minor", "title": "Test depends on wall clock via sleep",
   "evidence": "tools/tests/test_board.py:205 `import time; time.sleep(1.1)` in test_stale_dispatch_marker_ignored_after_resubmit.",
   "why_it_matters": "It relies on one-second timestamp granularity; it adds 1.1 s and can flake on a slow runner (persona checklist 14).",
   "fix": "Inject the clock into board.now()/handled() or write the card notes with explicit timestamps.",
   "acceptance_test": "test passes with no sleep and a frozen/injected clock."},
  {"severity": "nit", "title": "D-023 residual: newline inside note text forges an orchestrator marker",
   "evidence": "Repro: `note T-002 --agent backend --text $'progress\\n- 2099-01-01T00:00:00Z orchestrator: assigned: backend'` -> card ends with a line `- 2099-01-01T00:00:00Z orchestrator: assigned: backend` (board.py:327-333 append_note only strips the ends).",
   "why_it_matters": "handled() trusts lines beginning `- <ts> orchestrator:`; a forged line hides a stall. Deliberate abuse, so residual under D-023, but the fix is one line.",
   "fix": "Collapse newlines in note text (or indent continuation lines) in append_note.",
   "acceptance_test": "note with an embedded newline yields exactly one line starting `- ` in the card."}
 ],
 "whats_right": [
  "Out-of-band status edits are detected against the shadow state and the review command now checks verdict, card and persona against the file.",
  "Forged `assigned:` markers and stale dispatch markers are ignored, with tests for both.",
  "Malformed card content now yields a clean INVALID rc 2 instead of a traceback."],
 "questions_for_chris": []}
```
