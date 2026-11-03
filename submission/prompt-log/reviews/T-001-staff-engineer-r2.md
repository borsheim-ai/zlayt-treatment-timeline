# T-001 staff-engineer-reviewer review, round 2

**Verdict: changes (0 blockers, 1 major, 6 minors).** Full suite: `.venv/bin/python -m pytest tools/tests -q` -> `251 passed in 18.51s`.
Of my four round-1 majors: `validate` path handling and the out-of-band-status laundering are fixed; the `review` file check is mostly fixed (junk
and verdict-mismatch refused); the self-approval/trust-model finding is only partly addressed (a bypassable hook, no CLI change, no docs).
Of the round-1 minors, findings 4 (partly), 5, 6 and 7 are untouched; 8 and 9 are fixed.

Limit on what I ran: `board-guard` (T-004) denies every non-read-only `board.py` subcommand to reviewers, so I did not re-run `review`/`claim`/`note`/`move`/`gate`
repros and did not route around the hook (no `python -c` wrapper). Those items are marked "read" in `artifacts/review-evidence/M0-r2-staff-resolution.md`.
Read-only repros (validate/show/next/status) ran in a temp BOARD_ROOT: `artifacts/review-evidence/T-001-r2-readonly-repros.txt`.

```json
{
 "card": "T-001",
 "persona": "staff-engineer-reviewer",
 "model": "claude-sonnet-5-5",
 "scope": "git diff fbe5690..9e759a2 -- tools/board.py tools/tests/test_board.py (plus f413e84 delta to board.py); read-only repros in temp BOARD_ROOT; no real board cards touched",
 "exercised": [
  ".venv/bin/python -m pytest tools/tests -q -> 251 passed in 18.51s",
  "read the full diff of tools/board.py and tools/tests/test_board.py (fbe5690..9e759a2, 9e759a2..f413e84)",
  "temp BOARD_ROOT fixture (4 cards, shadow state, stale claim lock, 4 review files): validate on nonexistent path, /etc/hosts, missing card, findings:null review, wrong-card review, two-json-block review, review without model/scope, done card with reviews:['junk'], hand-edited status card; validate (all files); show; next; status --json (T-001-r2-readonly-repros.txt)",
  "piped crafted hook events into .claude/hooks/board-guard.sh (13 board.py invocation shapes) to judge the identity control that replaced the CLI self-approval check (T-004-r2-board-guard-probe.txt)",
  "attempted pytest tools/tests/test_board.py -q and git diff with two board paths: both denied by board-guard (false positive, see T-004 r2)",
  "NOT run (guard-denied for reviewers): review, claim, note, move, gate, assign, dispatch. Verified by reading code and tests only."
 ],
 "verdict": "changes",
 "scores": {"correctness": 4, "error_handling": 3, "test_quality": 4, "control_integrity": 3, "determinism": 4},
 "findings": [
  {
   "severity": "major",
   "title": "Self-approval / identity control still lives only in a bypassable regex hook; the CLI trust model is unchanged and undocumented (round-1 finding 3, partially resolved)",
   "evidence": "tools/board.py cmd_move check unchanged by 9e759a2 (git diff shows no hunk near the `--agent` / claimed_by comparison). Round-1 acceptance test `move done --agent backend_other` on a backend-claimed card still exits 0 at the CLI. Enforcement was added only in .claude/hooks/board_guard.py. Probe (artifacts/review-evidence/T-004-r2-board-guard-probe.txt): `bash -c 'python3 tools/board.py move T-1 done'` -> allow; `sh -c \"...\"` -> allow; `eval '...'` -> allow; `python3 tools/boar*.py move T-1 done` -> allow; `python3 -c \"import board; board.main([...])\"` -> allow. The same wrappers defeat the `--agent orchestrator` deny. grep -n -i 'honor|trust model|board_guard' docs/CONTRACT.md CLAUDE.md memory/DECISIONS.md -> only the generic 'No self-approval' principle lines (CLAUDE.md:17, CONTRACT.md:24).",
   "why_it_matters": "'No self-approval' is a Hard Rule. The CLI still treats --agent as a self-declared string with an orchestrator exemption, and the only thing between a subagent and `done` is a token matcher that a one-word wrapper evades. Nobody reading the contract can tell the control is advisory at the CLI layer.",
   "fix": "Pick one and write it down: (a) make the CLI refuse `done`/`review`/`gate` unless an env marker the orchestrator session sets is present (the hook strips or never sets it for subagents), or (b) keep the hook but document in CONTRACT 4.4 and CLAUDE.md that identity is enforced only by board-guard for Bash-tool calls, list the known bypasses, and make board-guard resolve `bash -c`/`sh -c`/`eval` payloads recursively (see T-004 r2). In either case add the CLI-level rule `done` only by --agent orchestrator.",
   "acceptance_test": "pytest: `board.py move <claimed card> done --agent backend_other` exits 2; board_guard test cases for `bash -c '<board.py move X done>'`, `sh -c`, `eval` are denied; CONTRACT 4.4 states where identity is enforced and where it is not."
  },
  {
   "severity": "minor",
   "title": "`reviews: [\"junk\"]` on a done card still crashes validate with a traceback, and a single bad card blinds the whole-board `validate` (round-1 finding 4, half fixed)",
   "evidence": "Fixture card board/cards/T-003.md (status done, `reviews: [\"junk\"]`): `board.py validate board/cards/T-003.md` -> `File \".../tools/board.py\", line 318, in _reviews_pass ... latest[r[\"persona\"]] = r[\"verdict\"] TypeError: string indices must be integers, not 'str'` [rc=1]; `board.py validate` (no args) -> same traceback, rc 1, so no other file is reported. The `findings: null` half is fixed (`INVALID: ... 'findings' must be a list`, rc 2).",
   "why_it_matters": "Exit 1 with a traceback violates the contract's exit-2 rule and one malformed card hides every other validation result from the board-validate hook.",
   "fix": "Make _reviews_pass skip non-dict entries (check_meta already flags them) and wrap per-file validation in try/except Exception -> INVALID line, continue.",
   "acceptance_test": "pytest: done card with reviews:['junk'] -> validate exits 2 with an INVALID line, no 'Traceback'; whole-board validate still reports the other cards."
  },
  {
   "severity": "minor",
   "title": "`review` still does not bind the persona or the card id strictly (round-1 finding 0 residual)",
   "evidence": "tools/board.py:719-720: `if d.get(\"card\") not in (a.id, None) and not str(d.get(\"card\", \"\")).startswith(a.id): raise` -> a file for card 'T-0011' registers against T-001. `--persona` is stored as typed (board.py:722) and never compared with the file's `persona`. test_review_must_match_file covers verdict mismatch and junk only.",
   "why_it_matters": "A pass can be registered under any persona name, so the 'different personas passed' record on the card is not tied to who wrote the review.",
   "fix": "Require d['card'] == a.id exactly and normalized d['persona'] == normalized --persona (strip '-reviewer'); refuse otherwise.",
   "acceptance_test": "pytest: file whose card is T-0011 registered against T-001 exits 2; `--persona security` with a file whose persona is staff-engineer-reviewer exits 2."
  },
  {
   "severity": "minor",
   "title": "Review-file validation still shallower than Appendix D.2 (round-1 finding 5, unchanged)",
   "evidence": "Fixture, `board.py validate`: reviews/T-001-wrong.md (card T-777, persona zzz, verdict fail, findings []) -> `ok (1 file(s))` rc 0; reviews/T-001-two.md (two json blocks, pass then fail) -> ok; reviews/T-001-nomodel.md (no model, scope, scores, whats_right) -> ok. See T-001-r2-readonly-repros.txt.",
   "why_it_matters": "Verdict and card come from the first block that contains 'verdict'; the second block is invisible to the gate. Board validator is the stated mechanical backstop for review format.",
   "fix": "Require card == id from the filename, persona == filename suffix, the D.2 keys, exactly one json block, and the verdict rule in both directions (fail with no blocker is refused).",
   "acceptance_test": "pytest: each of the three fixtures above exits 2."
  },
  {
   "severity": "minor",
   "title": "A pass from before rework still counts after the card returns to in_review (round-1 finding 6, unchanged)",
   "evidence": "tools/board.py _reviews_pass (around :314-318) still keys the latest verdict per persona with no round or timestamp; no hunk in the 9e759a2 diff touches it. Round-1 repro in artifacts/review-evidence/T-001-exercise-3.txt section G.",
   "why_it_matters": "Reviewer A never saw the reworked code but its old pass satisfies the done gate.",
   "fix": "Count only reviews whose `at` is later than the last transition into in_review, or require a fresh review from every persona that previously reviewed.",
   "acceptance_test": "pytest: A pass, B changes, rework, B pass -> `move done` refused until A re-reviews."
  },
  {
   "severity": "minor",
   "title": "Claim lock still has no stale recovery (round-1 finding 7, unchanged)",
   "evidence": "cmd_claim (board.py ~:575-600) is unchanged by 9e759a2; it only unlinks the lock for changes_requested/blocked cards. Fixture with board/.locks/claim-T-001.lock on a ready, unclaimed card: `board.py status --json` still lists T-001 under actionable ('T-001 ready for backend (P1)'), so the card is offered and then unclaimable.",
   "why_it_matters": "A crash between lock creation and save strands a card forever and `next`/status keep advertising it.",
   "fix": "Treat the lock as stale when the card is ready and claimed_by is null (the FileLock(a.id) status check already prevents double claims), or add an age cutoff.",
   "acceptance_test": "pytest: pre-create claim-T-001.lock on a ready card; claim succeeds."
  },
  {
   "severity": "minor",
   "title": "`assigned:` / `review dispatched:` markers are free-text note matches that any agent can write, and they silence the 3-round-cap line",
   "evidence": "tools/board.py handled() (new in 9e759a2) matches r\"^- (\\S+) \\S+: assigned:\" in the card body; append_note (board.py:322-323) writes `- {ts} {agent}: {text}`, so `board.py note T-x --agent anyone --text 'assigned: me'` creates a matching line. After f413e84, changes_pending (board.py:470) excludes any card with a recent assigned marker, which includes cards with rounds >= 3, so the cap warning disappears for 180 minutes. Read only (note is guard-denied for me).",
   "why_it_matters": "The marker feeds actionable, ready_unclaimed and the stop guard; a stray or deliberate note makes the orchestrator think work is queued. Silent suppression of the work queue is the failure class the contract forbids.",
   "fix": "Only count markers written by cmd_assign/cmd_dispatch (e.g. record them in frontmatter or reject note texts starting with these prefixes); keep the 3-round-cap line independent of the assigned marker.",
   "acceptance_test": "pytest: `note --text 'assigned: x'` does not change ready_unclaimed; a round-3 changes_requested card with an assign marker still appears in actionable."
  }
 ],
 "whats_right": [
  "load() now refuses any write on a card whose on-disk status differs from the shadow, with a message that tells the operator how to recover (board.py:236-241) and a regression test.",
  "validate now fails loudly for nonexistent, outside-project and non-board paths and resolves relative paths against BOARD_ROOT.",
  "251 tests pass, and the new tests assert on exit codes and stderr text rather than just 'no crash'."
 ],
 "questions_for_chris": [
  "The brief asks reviewers to re-run write-path repros in a temp BOARD_ROOT, but board-guard denies reviewers every mutating board.py subcommand regardless of BOARD_ROOT. Should the guard allow mutating commands when BOARD_ROOT points outside the project, or should round-2 write-path verification be done by the orchestrator/qa?"
 ]
}
```
