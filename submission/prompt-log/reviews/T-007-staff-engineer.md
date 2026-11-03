# T-007 review — staff-engineer-reviewer (mechanical evidence check)

**Verdict: changes** (0 blockers, 1 major, 2 minors, 1 nit).

Checked whether each of the 7 §4.8 M0 checks has a PROGRESS entry that names evidence, and whether the named evidence exists and passes. Six of seven hold up. Check 6 is recorded as PASS while its own tag is missing. Checks 2 and 4 name evidence that is not saved anywhere I could read. The heartbeat (cron 0174861c) is unverifiable from this seat and is not counted as a finding; STATE.md does record it.

Exercised: `python3 tools/agent_prompt.py staff-engineer-reviewer` (loaded the fallback persona); `python3 tools/board.py show T-007`; read docs/CONTRACT.md §4.8 items 1–7 (lines 246–254); read memory/PROGRESS.md (2026-11-02T00:20Z entry); `.venv/bin/python -m pytest tools/tests -q` (37 passed); `curl -s localhost:7777/healthz` (`{"ok": true}`); `ls -la artifacts/screenshots/`, `file`, and a PNG-signature check on both files (128219 and 129373 bytes); viewed artifacts/screenshots/m0-board.png; grep memory/STATE.md for 0174861c (line 25); `git log --oneline` (e37efb3, fbe5690); `git tag -l m0` (empty); grep submission/NEEDS_CHRIS.md for the restart row (row 2, P2); counted test functions in tools/tests/test_board.py (8) and test_hooks.py (11).

Not exercised: cron 0174861c itself (scheduler not visible from here); the live activity-feed update claimed for check 2; the mobile screenshot visually; the tailnet URL.

```json
{"card": "T-007", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "git HEAD fbe5690 plus working tree on 2026-11-02; app http://localhost:7777 (healthz only); no sample case (M0); memory/PROGRESS.md 2026-11-02T00:20Z entry",
 "exercised": [
  "python3 tools/agent_prompt.py staff-engineer-reviewer (fallback persona loaded)",
  "python3 tools/board.py show T-007",
  "read docs/CONTRACT.md lines 246-254 (4.8 checks 1-7)",
  "read memory/PROGRESS.md 2026-11-02T00:20Z entry, all 7 checks present with evidence named",
  ".venv/bin/python -m pytest tools/tests -q -> 37 passed",
  "curl -s localhost:7777/healthz -> {\"ok\": true}",
  "ls -la artifacts/screenshots/; file; PNG signature check: m0-board.png 128219 bytes, m0-board-mobile.png 129373 bytes, both valid PNG",
  "Read artifacts/screenshots/m0-board.png (desktop board rendered, 1440x1000)",
  "grep memory/STATE.md -> line 25 'Heartbeat: cron 0174861c at :07/:27/:47 (session-only; recreate after restart)'",
  "git log --oneline -> e37efb3, fbe5690; git tag -l m0 -> empty",
  "grep submission/NEEDS_CHRIS.md -> row 2 'Restart the session once so native agent definitions load'",
  "grep -c 'def test_' tools/tests/test_board.py -> 8; test_hooks.py -> 11"
 ],
 "verdict": "changes",
 "scores": {"s4_8_checks_recorded": 3, "evidence_named_and_reproducible": 3, "screenshots_present_and_valid": 5, "heartbeat_recorded_in_state": 4},
 "findings": [
  {"severity": "major", "title": "Check 6 recorded PASS while the m0 tag does not exist",
   "evidence": "memory/PROGRESS.md 2026-11-02T00:20Z item 6: 'Conventional commits e37efb3, fbe5690; .gitignore complete; tag m0 pending M0 gate -> PASS'; docs/CONTRACT.md:253 (4.8 item 6) requires 'tag m0'; `git tag -l m0` prints nothing; board card T-006 'Secrets scanner + git hygiene (... tag m0)' is still in READY",
   "why_it_matters": "A §4.8 exit check is marked PASS while one of its required parts is open. The PASS line is the milestone record the gate reads, so it overstates what is done. The gap is disclosed in the same line, which limits this to a major rather than a blocker.",
   "fix": "Mark item 6 as open or partial in PROGRESS (commits and .gitignore PASS, tag m0 OPEN) until T-006 creates the tag, then append a PASS line that names the tag.",
   "acceptance_test": "`git tag -l m0` prints m0 before any PROGRESS line marks 4.8 item 6 as PASS"},
  {"severity": "minor", "title": "Check 4 evidence is not saved; the haiku replies can't be re-read",
   "evidence": "memory/PROGRESS.md 2026-11-02T00:20Z item 4: 'haiku load tests of paralegal-reviewer and qa answered correctly -> PASS (fallback)'; artifacts/review-evidence/ holds only T-001-*.txt and T-003-*.txt",
   "why_it_matters": "docs/CONTRACT.md:251 (4.8 item 4) asks for each subagent to report back in 5 lines or fewer. With no saved reply, the claim that the definitions load cannot be checked. The contract does allow the fallback path plus a NEEDS_CHRIS note, and that note exists (row 2), so this is an evidence gap, not a failed check.",
   "fix": "Save the two haiku replies to artifacts/review-evidence/T-007-agent-load-paralegal-reviewer.txt and artifacts/review-evidence/T-007-agent-load-qa.txt and cite those paths in PROGRESS.",
   "acceptance_test": "Both files exist, each at most 5 lines, each names the definition it loaded"},
  {"severity": "minor", "title": "Check 2 live activity-feed claim has no saved evidence",
   "evidence": "memory/PROGRESS.md 2026-11-02T00:20Z item 2: 'activity feed shows a new event on the next poll ... -> PASS'; no screenshot or log file under artifacts/ backs it",
   "why_it_matters": "docs/CONTRACT.md:249 (4.8 item 2) requires the feed to update live. Only the claim is recorded, so the 'live' part is not reproducible from the repo. I did not exercise it.",
   "fix": "Record the poll test (for example, a curl of /api/activity before and after board.py new) with the output saved under artifacts/review-evidence/.",
   "acceptance_test": "Saved output shows a new activity event id appearing after a board.py action"},
  {"severity": "nit", "title": "Board screenshot predates the current card state",
   "evidence": "artifacts/screenshots/m0-board.png shows T-007 in READY with 'AC 0/3', T-004 in progress, T-001 and T-003 in review; `board.py show T-007` now shows status in_review and AC 3/3",
   "why_it_matters": "The file meets AC 2 (it exists and is a valid PNG). It is a point-in-time image and should not be read as the current board state.",
   "fix": "Name the capture time in PROGRESS, or retake the screenshot at the M0 gate.",
   "acceptance_test": "PROGRESS names the capture time, or a newer screenshot exists"}
 ],
 "whats_right": [
  "pytest tools/tests passes 37/37, matching the count in PROGRESS",
  "Both screenshots are valid PNGs and the desktop image shows the real board UI with live counts",
  "STATE.md records the heartbeat as session-only with a recreate-after-restart note, which matches the NEEDS_CHRIS row"
 ],
 "questions_for_chris": []}
```
