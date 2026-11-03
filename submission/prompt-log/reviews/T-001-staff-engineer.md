# T-001 staff-engineer-reviewer review

**Verdict: changes (0 blockers, 4 majors, 6 minors).** The CLI is solid on the happy path and on the four tested ACs:
`.venv/bin/python -m pytest tools/tests -q` gives 37 passed, concurrent claims leave exactly one winner (8 real processes), illegal
transitions are refused with the allowed set, `done` without review or AC is refused, parse errors become INVALID cards in `list`/`status`.
The problems are all in the integrity of the controls the card exists to provide: a review entry is not verified against its file,
`validate` silently says ok for paths it did not check, and the out-of-band-status check is cleared by the next CLI write to the card.
Behaviour was identical at fbe5690 and at the working tree (re-ran the repros against `git show fbe5690:tools/board.py`).
Evidence: `artifacts/review-evidence/T-001-exercise-{1,2,3}.txt`.

```json
{
 "card": "T-001",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git diff e37efb3..fbe5690 -- tools/board.py tools/tests/test_board.py; repros run in BOARD_ROOT=<tmp> against both fbe5690 and HEAD copies of board.py; no real board cards touched",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -> 37 passed (test_board.py 8, test_hooks.py rest)",
  "read all 1054 lines of tools/board.py and test_board.py",
  "8 concurrent `claim` processes on one card -> exactly 1 success, 7 'already claimed' (T-001-exercise-1.txt)",
  "8 concurrent `new` -> T-001..T-008 unique; 8 concurrent `note` -> 8 notes kept (exercise-3.txt)",
  "illegal transitions (in_progress->done, ->backlog, bogus status, in_review with unchecked AC, cancel without note, reopen done without note)",
  "ac --check without evidence / nonexistent AC; handoff gate on in_review; done without review; done with 'pass' registered against a junk review file",
  "self-approval: claimant `backend` refused; same claimant with --agent orchestrator succeeds (exercise-2.txt A)",
  "validate: nonexistent path, /etc/hosts, findings:null review, wrong-card review, hand-edited status before and after a CLI write, 6 malformed card variants (exercise-2.txt B-E)",
  "stale-pass-survives-rework scenario, gate with stub record, milestone done without gate, inbox/lesson/next/status --json (exercise-3.txt)",
  "simulated stale claim lock (lock file left behind) -> card stranded (exercise-3.txt tail)"
 ],
 "scores": {
  "correctness_happy_path": 4,
  "gate_integrity": 2,
  "error_handling": 2,
  "determinism_atomicity": 4,
  "test_quality": 3
 },
 "findings": [
  {
   "severity": "major",
   "title": "`board.py review` records any verdict against any file; a junk file unlocks `done`",
   "evidence": "tools/board.py:680-700 (cmd_review only checks the file exists; never calls validate_review_file or review_json). Repro: `echo junk > reviews/junk.md; board.py review T-001 --persona anyone --model m --verdict pass --file reviews/junk.md` -> rc 0; then `move T-001 done` -> done. Also a file whose own JSON says {\"verdict\":\"fail\"} was registered as pass (T-001-exercise-1.txt section 5-6; exercise-2.txt section A).",
   "why_it_matters": "Rule 7 (no self-approval, every card reviewed in a fresh context) is enforced only by the review entry, and the entry is whatever the caller typed. One wrong --verdict copy-paste (or a reviewer that never wrote its file) lets a card reach done with no real review. `validate` would catch the file, but nothing makes `review` run it.",
   "fix": "In cmd_review: run validate_review_file(rp); require JSON verdict == --verdict, JSON card == id, normalized JSON persona == --persona; refuse otherwise with the reason.",
   "acceptance_test": "pytest: registering a junk file, a file with verdict!=--verdict, and a file whose card is another id each exit 2 and leave meta['reviews'] unchanged."
  },
  {
   "severity": "major",
   "title": "`validate` prints 'ok' and exits 0 for paths it did not check (nonexistent, outside ROOT, relative with BOARD_ROOT)",
   "evidence": "tools/board.py:846-852: `if not p.exists(): continue` and `except ValueError: continue`, then `print(f\"ok ({len(targets)} file(s))\")` at :876. Repro: `board.py validate reviews/typo-does-not-exist.md` -> `ok (1 file(s))` rc 0; `validate /etc/hosts` -> ok; with BOARD_ROOT=<tmp> and cwd elsewhere `validate reviews/x.md` resolves against cwd (Path.cwd() / t, :845) so every relative path is skipped (exercise-2.txt section B; first run of exercise-2 printed ok for all malformed cards for this reason). `BOARD_ROOT` is not resolve()d, so a symlinked root (macOS /tmp -> /private/tmp) also skips everything.",
   "why_it_matters": "This is the command the brief, the board-validate hook and every worker use to prove a file is valid. A typo'd path, or any path outside the project, reports success. A silent fallback in the validator makes a green result meaningless.",
   "fix": "Resolve relative paths against ROOT (fall back to cwd only if that exists); resolve ROOT once; error 'no such file' and 'path outside project' with exit 2; report the count of files actually checked.",
   "acceptance_test": "pytest: validate of a nonexistent path, of /etc/hosts, and of a relative bad card path with cwd != ROOT each exit 2; a symlinked BOARD_ROOT still validates."
  },
  {
   "severity": "major",
   "title": "Out-of-band status edit is laundered by the next CLI write; the shadow state is overwritten without checking it",
   "evidence": "tools/board.py:238-247: save() unconditionally sets shadow[id] = meta['status'] (the possibly hand-edited value). Repro (exercise-2.txt D): hand-edit T-003 ready->in_review; `validate` -> INVALID 'status changed ready -> in_review outside board.py'; run `board.py note T-003 ...` (any agent); `validate` -> ok; `move T-003 changes_requested` is then accepted from the forged in_review. Same for ready->in_progress on T-002. The only test (test_validate_catches_bad_card_and_out_of_band_status) validates immediately after the edit.",
   "why_it_matters": "AC3 and the contract's 'single system of record' depend on detecting status changed outside the CLI. The detection expires as soon as anyone touches the card, and every transition rule (illegal-transition table, claim, done gate) then runs from the forged status.",
   "fix": "In load() (or every mutating command) compare the on-disk status to the shadow and refuse with 'status changed outside board.py' unless the shadow is absent; update the shadow only from cmd_* after the check. Add a `board.py accept-edit T-### --note` escape hatch if hand edits must be legitimized.",
   "acceptance_test": "pytest: hand-edit status, then `note`/`move`/`ac` on the card each exit 2 with 'outside board.py'; `validate` still reports it afterwards."
  },
  {
   "severity": "major",
   "title": "Self-approval guard is a string compare on a self-declared --agent, with an orchestrator exemption; any agent can mutate any card",
   "evidence": "tools/board.py:599 `if a.agent == meta.get('claimed_by') and a.agent != 'orchestrator'`. Repro (exercise-2.txt A): card claimed by `backend`; `move T-001 done --agent backend` -> refused; `move T-001 done --agent orchestrator` -> `in_review -> done`. In exercise-1.txt section 6 a non-claimant `w1` checked the ACs, wrote the handoff and then moved the card done. ac/note/move/handoff accept any --agent with no check against claimed_by.",
   "why_it_matters": "Contract rule 7 says workers never mark their own cards done. The test (test_round_trip) only proves the honest path: the worker that types its own name is stopped. Combined with the first finding, a worker can self-review, self-approve and close a card with three commands.",
   "fix": "Decide and document the trust model. Minimum: `done` only when --agent == 'orchestrator' (not 'anyone but the claimant'); ac/handoff/move-to-in_review only by claimed_by or orchestrator; log a warning event for any other pair. If it stays honor-system, say so in docs/CONTRACT §4.4 and CLAUDE.md so reviewers know the control is advisory.",
   "acceptance_test": "pytest: `move done --agent backend_other` on a backend-claimed card exits 2; `ac --check --agent stranger` on a card claimed by someone else exits 2."
  },
  {
   "severity": "minor",
   "title": "Unhandled exceptions and exit 1 (contract says exit 2) on malformed review/card contents",
   "evidence": "`validate` on a review with \"findings\": null -> TypeError at tools/board.py:825 (rc 1); a done card with `reviews: [\"junk\"]` -> TypeError at :312 in _reviews_pass (rc 1), reached from check_meta :304 even though :298-300 already flagged the entry (exercise-2.txt C and E, T-015).",
   "why_it_matters": "§4.4: validate exits 2 on error. A traceback is not a diagnostic, and callers that special-case rc 2 miss rc 1. (board_validate.py maps any nonzero to exit 2, so the hook is safe; direct callers are not.)",
   "fix": "Wrap per-file validation in try/except Exception -> 'INVALID: <file>: unexpected <type>: <msg>', rc 2; make _reviews_pass skip non-dict entries.",
   "acceptance_test": "pytest: findings:null and reviews:['junk'] on a done card both exit 2 with an INVALID line, no traceback."
  },
  {
   "severity": "minor",
   "title": "Review-file validation is shallower than Appendix D.2 / §7.4",
   "evidence": "tools/board.py:811-837 requires only card, persona, verdict, findings, exercised. Accepted with rc 0: JSON `card` T-777 in file T-001-wrongcard.md with persona 'zzz'; verdict 'fail' with zero findings; no model/scope/scores/whats_right; multiple JSON blocks (review_json :703-712 silently takes the first block containing 'verdict'). Verdict rule is enforced only in the blocker->fail / major->changes direction (:831-834).",
   "why_it_matters": "§7.4 says the validator rejects files that break the verdict rule, and D.2 says exactly one JSON block with these fields. A wrong-card or wrong-persona file passes and feeds the persona stats on the board UI.",
   "fix": "Check card == id parsed from filename, persona matches filename suffix, required D.2 keys present, exactly one json block, verdict consistent with severities in both directions.",
   "acceptance_test": "pytest cases for each rejected shape above."
  },
  {
   "severity": "minor",
   "title": "A pass from before rework still counts after the card returns to in_review",
   "evidence": "tools/board.py:309-313 (_reviews_pass uses the latest verdict per persona, no round or timestamp). Repro (exercise-3.txt G): persona A passes, B says changes, card reworked, only B re-reviews and passes -> `move done` succeeds; A never saw the changed code.",
   "why_it_matters": "Tier-1 review is meant to cover the code that ships; after rework the earlier persona's approval is of a different artifact.",
   "fix": "Count only reviews whose `at` is later than the most recent move into in_review (or tag each review with the round and require current-round reviews from every persona that reviewed earlier).",
   "acceptance_test": "pytest: A pass, B changes, rework, B pass -> done refused until A re-reviews."
  },
  {
   "severity": "minor",
   "title": "Claim lock has no stale recovery; a crash strands a ready card that `next` keeps offering",
   "evidence": "tools/board.py:545-572: the claim lock is created at :551 and removed only by in-process except/finally or by moves to ready/done/cancelled; FileLock has stale recovery (:128) but the claim lock does not. Repro (exercise-3.txt tail): leftover board/.locks/claim-T-001.lock -> `claim` rc 2 'already claimed (lock held by w1)', `move ready` -> 'already ready', `next --role backend` still prints T-001.",
   "why_it_matters": "TeammateIdle (§4.3) keeps telling the idle worker to claim a card it can never claim, with no CLI way out.",
   "fix": "In cmd_claim, treat a claim lock as stale when the card is ready and unclaimed (claimed_by null) or the lock is older than N minutes; or drop the redundant lock, since the status check under FileLock(a.id) is what actually prevents double claims.",
   "acceptance_test": "pytest: pre-create the claim lock file on a ready card; `claim` succeeds."
  },
  {
   "severity": "minor",
   "title": "Max-3-rounds rule (§7.4) is not surfaced anywhere",
   "evidence": "tools/board.py:693 increments rounds without bound; compute_status/actionable (:411-480) never mention rounds >= 3.",
   "why_it_matters": "The orchestrator is meant to stop a fourth identical retry and record a decision; nothing on the board or the stop-guard text prompts it.",
   "fix": "Add an actionable line and a `rounds_exceeded` list in status when rounds >= 3 and status is changes_requested/in_review.",
   "acceptance_test": "pytest: a card at rounds=3 in changes_requested appears in status --json under rounds_exceeded."
  },
  {
   "severity": "minor",
   "title": "`gate --result pass` accepts a stub record",
   "evidence": "tools/board.py:907 checks only that the record file exists; the >=50-char check lives in validate_review_file (:813-815) and is never run by cmd_gate. Repro: reviews/GATE-M0-summary.md containing the word 'gate' -> `gate M0 ... --result pass` rc 0 (exercise-3.txt H).",
   "why_it_matters": "A milestone can be marked passing against an empty record; gates are the milestone control.",
   "fix": "Run the gate-record validation in cmd_gate and refuse a stub.",
   "acceptance_test": "pytest: a 4-byte record is refused with 'gate summary is empty'."
  }
 ],
 "whats_right": [
  "Claim race is genuinely safe: 8 concurrent processes, one winner; the status check under the per-card FileLock is the real guard.",
  "Atomic writes (mkstemp + os.replace), unique ids under concurrent `new`, and no lost notes under concurrent `note`.",
  "Illegal-transition refusals print the reason and the allowed set; save() refuses to persist an invalid card."
 ],
 "questions_for_chris": [
  "Is the board's trust model honor-system (agents declare their own --agent) by design, or should the CLI enforce who may mark done?"
 ],
 "verdict": "changes"
}
```
