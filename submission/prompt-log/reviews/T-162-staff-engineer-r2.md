# T-162 r2 review (staff-engineer-reviewer)

Verdict: **changes**. No blocker. One major: `tests/e2e/test_no_console_errors.py` stays green while four of the seven registered side panels are missing, so its stated guard does not catch the failure it was written for.

The round-2 asks hold on HEAD. The closed Dismissed group carries a count marker ("1 has a re-run note.") on both the entries and the amounts summaries. The dismissed note is hidden while the group is closed and visible once it is opened. The assertions in `test_rerun_note.py` have no conditionals. Round-1 blocker 1 (stray `key` guard in `mountSection`) is fixed. Round-1 blocker 2 (evidence does not reproduce) is reproduced: 5 of 5 pass on HEAD.

Evidence commit: fix commit 67be38d. Reviewed on `git archive` of HEAD 985dbd2, because HEAD moved during the review. 67be38d..985dbd2 changes only backend, evals and `tests/unit` files. `diff -rq` confirms `app/frontend` and `tests/e2e` are identical between the two archives.

Results:
- `E2E_BASE_URL=http://127.0.0.1:7893 E2E_REQUIRE_DB=1 pytest tests/e2e/test_rerun_note.py tests/e2e/test_no_console_errors.py -v` gives 5 passed in 7.23s (3/3 and 2/2).
- Playwright probe on :7893, closed group: both summaries read "Dismissed (1) ... 1 has a re-run note."; entry note and amount note both present, `visible=False`. After opening: entry note visible, amount note visible, with the server sentence.
- Mutants on a sandbox copy (:7894, restored and diffed identical after each): M1 (entry marker removed) fails `test_rerun_note.py:73`; M2 (amounts marker removed) fails `:81`; M3 (dismissed notes hidden when open) fails `:76`; M4 (no note on dismissed rows) fails `:73`.
- M5 (throw at top of `mountSection`) fails `test_no_console_errors.py:23`. Page-error and console watchers record nothing.
- M6 (throw at top of the batch panel callback) leaves `test_no_console_errors.py` at 2 passed, with audit, manual, narrative and export-settings absent from the DOM. This is the major finding.
- Non-local server (:7895, `ZLAYT_MODE` unset), `E2E_REQUIRE_DB=1`: the decided fixture fails with "library cases need ZLAYT_MODE=local" (3 errors, not skips). Round-1 minor fixed.

Not run (outside the brief): `pytest tests/unit`, `tests/e2e/test_charge_confirm.py`.

Scripts and probes: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-162-r2/

```json
{
 "card": "T-162",
 "persona": "staff-engineer-reviewer",
 "model": "claude-haiku-5-5",
 "scope": "commit 67be38d (round-2 fix: app/frontend/review.js, app/frontend/timeline.js, tests/e2e/test_rerun_note.py, tests/e2e/conftest.py); evaluated on git archive of HEAD 985dbd2 (HEAD moved from 67be38d during the review; 67be38d..985dbd2 changes no app/frontend or tests/e2e file, checked by diff -rq); own server http://127.0.0.1:7893 (fixture backend, ZLAYT_MODE=local, FIXTURE_SET=curated); decided fixture case_lib06_lop_billed_vs_adjusted; console watcher on sample case",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-162-staff-engineer.md (r1), python3 tools/board.py show T-162 (AC 1 evidence 67be38d, handoff, notes)",
  "git rev-parse HEAD (67be38d at start, 985dbd2 later); git merge-base --is-ancestor 2de5ba9 HEAD -> ancestor; git log 70af4a7..HEAD; git show 67be38d -- app/frontend tests/e2e/conftest.py tests/e2e/test_rerun_note.py (full round-2 diff); git diff --stat 67be38d HEAD (backend, evals, tests/unit only)",
  "git archive 985dbd2 and git archive 67be38d extracted to scratch dirs; diff -rq app/frontend and tests/e2e between them: identical",
  "server PORT=7893 HOST=127.0.0.1 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated from the HEAD archive; listener PID 97570 verified with ps and lsof",
  "E2E_BASE_URL=http://127.0.0.1:7893 ZLAYT_DB=<scratch>/data/head985.sqlite3 E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_rerun_note.py tests/e2e/test_no_console_errors.py -v -> 5 passed in 7.23s (3/3 rerun_note, 2/2 no_console_errors)",
  "Playwright probe on :7893 (decided fixture, entry e1 and amount a5 dismissed, rerun_note stubbed on both as the spec does): closed: both Dismissed summaries read 'Dismissed (1) ... 1 has a re-run note.'; entry note count 1 visible False; amount note count 1 visible False; opened entries: entry note visible True; opened amounts: amount note visible True; #why-modal rerun-note asserted by spec",
  "grep -n 'key === \"a\"' app/frontend/review.js on HEAD: guard at review.js:484 inside the keydown handler; mountSection (review.js:497) has no stray key line",
  "mutation sandbox (copy of HEAD archive) on :7894 (PID 99075): M1 timeline.js:77 marker call replaced by null -> test_rerun_note 1 failed at :73 ('1 has a re-run note'); M2 review.js:106 amounts marker replaced by null -> 1 failed at :81; M3 dismissed rows' notes hidden with hidden attribute -> 1 failed at :76 (to_be_visible after opening); M4 no note on dismissed rows (review.js:372 guard) -> 1 failed at :73; each file restored and diff -rq against HEAD archive identical",
  "M5 on sandbox: 'if (key === \"a\") return;' inserted at top of mountSection -> test_no_console_errors 1 failed at line 23 (charges-panel not visible); probe: pageerror and console.error watchers both empty, charges-panel count 0, flags-panel count 0; restored and identical",
  "M6 on sandbox: undefined name inserted at top of the batch panel callback (batch.js:97) -> test_no_console_errors 2 passed; probe: data-panel present = [judges, flags, charges, batch] versus HEAD [judges, flags, charges, batch, audit, manual, narrative, export-settings]; watcher empty; restored and identical",
  "server PORT=7895 with ZLAYT_MODE unset (PID 8089): E2E_REQUIRE_DB=1 pytest tests/e2e/test_rerun_note.py -> 3 errors 'Failed: library cases need ZLAYT_MODE=local' (fails, does not skip; r1 minor fixed)",
  "servers stopped after the runs: PIDs 97570 (:7893), 99075 (:7894), 8089 (:7895), each verified by ps command line and lsof listener before kill; ports closed afterwards",
  "not run: pytest tests/unit (outside the brief); test_charge_confirm.py (outside the brief); the 67be38d archive was not served separately (frontend and e2e trees identical to HEAD)"
 ],
 "verdict": "changes",
 "scores": {
  "dismissed_note_visible_when_opened": 5,
  "closed_group_marker_or_count": 5,
  "assertions_unconditional": 4,
  "round1_blockers_fixed": 5,
  "evidence_reproduces_at_head": 5,
  "no_console_guard_strength": 2
 },
 "findings": [
  {
   "severity": "major",
   "title": "test_no_console_errors stays green while four of seven registered side panels are missing; its watcher cannot see the failure it was written for",
   "evidence": "Repro on the sandbox: M6 inserts an undefined name at the top of the batch panel callback (app/frontend/batch.js:97). 'E2E_BASE_URL=http://127.0.0.1:7894 ... pytest tests/e2e/test_no_console_errors.py -q' -> '2 passed in 4.03s'. Probe on the same server: data-panel present = ['judges', 'flags', 'charges', 'batch']; on HEAD :7893 = ['judges', 'flags', 'charges', 'batch', 'audit', 'manual', 'narrative', 'export-settings']. The loop that drops them is app/frontend/timeline.js:348 'ZL.hooks.panels.forEach((fn) => fn(c, side));' with no per-panel catch. Seven panels are registered (batch.js:97, audit.js:55, charges.js:180, exportcfg.js:47, flags.js:152, manual.js:65, narrative.js:74). The spec asserts one: tests/e2e/test_no_console_errors.py:7 'PANELS = (\"charges-panel\",)'. The docstring at lines 1-3 says 'the panels that render inside mountSection must be on the page'. Separately, M5 (ReferenceError at the top of mountSection) makes the spec red only at line 23 (charges-panel visible); the watcher lists at lines 10-14 and the assert at line 26 record nothing (probe: pageerror and console.error both empty, URL unchanged).",
   "why_it_matters": "The T-154 lesson this spec cites is that a ReferenceError in the panel path stopped every panel drawing and nothing noticed. Today the spec notices only if charges-panel dies, and it stays green when batch, audit, manual, narrative or export-settings die. The pageerror and console watchers are blind to the failure class, so the spec's stated guard ('no uncaught page error') does not hold. The r1 review's fix asked for a spec that fails on any page error during open_case; the watcher cannot see this error, so that acceptance is met only through the charges-panel check. Rated major, not blocker: at HEAD all seven panels render (probe), so this is a guard gap that must close before the gate, not a present defect. Owner: qa for the spec (tests/**), frontend for the loop at timeline.js:348.",
   "fix": "(a) PANELS lists every registered panel's testid or data-panel name (batch, audit, charges, export-settings, flags, manual, narrative) and the spec asserts each is attached, not only charges. (b) Make a panel's render error visible: wrap each fn(c, side) call in timeline.js:348 in try/catch that records a named error for that panel in state and shows it in the UI, or let the error reach window.onerror so the pageerror watcher sees it. Do not swallow it.",
   "acceptance_test": "On a git archive of the fixed commit, with E2E_REQUIRE_DB=1: (1) mutant M6 (throw at top of batch.js:97 callback) makes test_no_console_errors red; (2) mutant M5 (throw at top of mountSection) makes it red at a line that asserts the watcher or a named panel error, not only charges-panel; (3) the unmodified HEAD stays 2/2 green."
  },
  {
   "severity": "minor",
   "title": "The 'hidden while closed' assertions pass on a missing node",
   "evidence": "tests/e2e/test_rerun_note.py:74 'expect(erow.get_by_test_id(\"rerun-note\")).to_be_hidden()' and :82 'expect(arow.get_by_test_id(\"rerun-note\")).to_be_hidden()'. Playwright's to_be_hidden also passes when the locator matches no node, so the line proves nothing about the row being present. Today the row is present (probe: entry row count 1, amount row count 1), and the marker check at :73 and :81 catches the removal case (M4, M1, M2 above), so the spec is not fooled by this in practice.",
   "why_it_matters": "The card says the assertions are unconditional. The hidden check is unconditional but can be satisfied by absence, which is the same weakness the r1 review flagged for the 'if erow.count()' branch. A later change that drops the row would rely on the marker check alone.",
   "fix": "Insert expect(...).to_have_count(1) before each to_be_hidden (lines 74 and 82).",
   "acceptance_test": "Mutant: remove the dismissed entry row from the closed group (not only its note) while keeping the marker; the spec fails at the to_have_count(1) line, not at a later step."
  },
  {
   "severity": "nit",
   "title": "timeline.js:77 drops the marker silently when the hook is absent",
   "evidence": "app/frontend/timeline.js:77 'ZL.rv && ZL.rv.rerunMarker ? ZL.rv.rerunMarker(body) : null'. Script order (index.html:77 timeline.js before :79 review.js) is harmless because the call runs at render time, and M1 (call removed) shows the spec catches a missing marker. The guard is still the silent-null shape the r1 minor flagged.",
   "why_it_matters": "A future load-order or rename change would hide the entry marker without an error, and only the spec would notice.",
   "fix": "Call ZL.rv.rerunMarker(body) with no guard, or move the helper where timeline.js can use it without an existence check.",
   "acceptance_test": "The entry marker assertion at test_rerun_note.py:73 stays green with the guard removed and the helper present; with the helper deleted, the page throws instead of showing no marker."
  }
 ],
 "whats_right": [
  "The closed Dismissed group now says '1 has a re-run note.' on both the entries and the amounts summaries (probe on :7893), and the note is hidden until the group opens, then visible with the server sentence.",
  "Round-1 blocker 1 is fixed: the stray key guard is gone from mountSection (review.js:497) and sits in the keydown handler at review.js:484; with the stray line reintroduced (M5) the spec goes red.",
  "The E2E_REQUIRE_DB fixture now fails, not skips, against a non-local server (3 errors, 'library cases need ZLAYT_MODE=local')."
 ],
 "questions_for_chris": [
  "Should a decided entry's note also show in its 'Why?' dialog (timeline.js entry-why)? Entries have no 'How this was checked' button at HEAD, so the AC's 'row and trace' is met by the row only for entries. The spec asserts row only for entries and trace only for amounts."
 ]
}
```
