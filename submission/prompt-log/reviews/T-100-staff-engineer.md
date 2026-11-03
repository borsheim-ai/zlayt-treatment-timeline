# T-100 review (D-047), staff-engineer-reviewer

Reviewed commit 24c18a7 (card T-100). HEAD has moved to f5ddec8 (frontend and e2e only; app/backend and tests/unit are byte-identical to 24c18a7). Verdict: **fail**.

**Blocker.** The route still stores an edit that adds an attribution, hedge or approximation the quote does not have ("patient reports pain 4/10", "possibly improving", "approximately 4/10"). D-047 says qualifier tokens missing from the excerpt are a hard 422; only the reverse direction (qualifier dropped from the summary) is enforced.

**Majors.** (a) The export gate is not an independent second line: it reads stored reasons and never re-runs the checks, so a route that stores no reason passes the gate and the letter exports "left-sided". (b) The negation and side word list is narrower than the module's own list (denies, never, none, negative, absent, neither, bilateral all save). (c) AC 1 is checked done, but at 24c18a7 the frontend 409 branch and the e2e half were not done.

**Checked as asked.**
- No route stores a side or negation edit: confirm_warnings, force, override, confirm, string 'true', manual entry and batch all refuse. Batch edit returns 400; batch accept ignores the edits payload. Refused calls leave the case JSON identical. Holds.
- 422 reasons in plain words: mostly yes. Grammar nit in the two-word case. The qualifier message still uses the speech verbs (minor, below).
- T-098 gate tests: they now write state directly. Removing the gate fails 3 of them, so they exercise the gate's reading of stored state. They do not show the gate as a backstop for the route (major, below).
- D-040 speaker-word string at review.py:119: not reworded at 24c18a7 or at HEAD.
- api.md: updated for the 422 shape and the no-409 rule. Two statements are inaccurate (line 321: "the same checks the export gate runs"; the HIGHLIGHT_NOT_FOUND 422 is outside D-047).
- Judge objection to a human edit saves as needs_review with a warning, and this is consistent across edit (review.py:212) and manual entry (review.py:360).
- Mutation: token check disabled (review.py:136) fails 20 tests. Qualifier-drop check disabled fails 6. Gate disabled fails 3.
- Card-commit archive: the requested selection gives 103 passed. Full tests/unit gives 1814 passed and 4 skipped, not the 1834 the handoff claims (minor, below).

**Exercised.** See the `exercised` list in the JSON. Probe outputs and scripts are in `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-100/` (probe_outputs.txt, probe_*.py). probe_http.py has two mislabelled lines (its "entries unchanged" line is wrong because its accept ran first; its "qualifier drop" row is a "no" token case). probe_http_clean.py is the authoritative route check.

```json
{"card": "T-100", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "Commit 24c18a7 (D-047): app/backend/review.py, store.py, export.py, trace.py; tests/unit (test_review_rules.py, test_manual_and_split.py, test_api_routes.py, test_trace.py, test_export.py, test_ocr_invariant.py); memory/contracts/api.md. HEAD at review time f5ddec8 (backend unchanged since 24c18a7; frontend and tests/e2e changed). Synthetic sample case (golden sample record 5 and record 8 via tests/unit fixtures). HTTP probes ran in-process via FastAPI TestClient against the archive copy; no running app URL was used.",
 "exercised": [
  "Read personas/staff-engineer.md, memory/ORCHESTRATOR_DECISIONS.md (D-040, D-045, D-047), board.py show T-100, git show --stat and the full app/tests/api.md diff of 24c18a7.",
  "git log --oneline -3; git merge-base --is-ancestor 24c18a7 HEAD (ancestor); git diff 24c18a7 HEAD -- app/backend tests/unit memory/contracts (empty); git show --stat f5ddec8.",
  "Working tree (HEAD f5ddec8 plus uncommitted changes from other cards): .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit -k 'edit or manual or d047 or d034' gave 103 passed; full tests/unit gave 2 failed (test_eval_runner.py calibration header tests, outside T-100), 1832 passed, 1 skipped.",
  "git archive 24c18a7 extracted into a scratchpad copy (diff -rq against a second fresh extract: identical except __pycache__). Run with .venv/bin/python -I and the copy appended to sys.path: the same selection gave 103 passed; full tests/unit gave 1814 passed, 4 skipped (3 need a git repository, 1 is the live judge eval).",
  "Mutants of the archive copy, full tests/unit each: review.py:136 'if False and toks' gave 20 failed; review.py:140 'if False and dropped' gave 6 failed (5 of them T-098 tests failing at the route assertion); trace.py:425 code_check_blockers returning [] gave 3 failed (T-098 gate tests).",
  "HTTP probes (TestClient on the archive): POST items/{id}/review with edit + confirm_warnings, force, override+keep_my_wording+confirm, confirm_warnings='true'; POST records/{rid}/entry with confirm_warnings and force; POST review/batch with action edit and accept. Case JSON identical before/after the refused calls (probe_http_clean.py).",
  "Service-level probes (seeded() from tests/unit/test_review_rules.py): side, negation, qualifier-add and approximation summaries with judge unavailable and judge supported; judge verdicts supported/partially/unsupported/unsure/disagrees/unavailable; gate-alone probe on the token-check-disabled mutant (export built with 'left-sided').",
  "Read review.py (full), grounding.py 120-232, spanish_text.py 189-245, trace.py 330-440, case_extras.py 24-64 and 107-120, api.py 347-361, 423-432, 496-506, db.py 215-237, api.md line 321 and line 26, tests/e2e/test_edit.py and test_rerun_judge.py (24c18a7 and HEAD), app/frontend/review.js and manual.js at 24c18a7 and HEAD (git grep for needs_confirm, btn-keep-wording, confirm_warnings).",
  "Evidence: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-100/probe_outputs.txt and the probe_*.py scripts beside it."
 ],
 "verdict": "fail",
 "scores": {"d047_refusal_routes": 3, "d047_token_vocabulary": 2, "gate_as_second_line": 2, "judge_objection_consistency": 4, "plain_422_reasons": 3, "d040_wording": 2, "api_md_accuracy": 3, "tests_mutation_and_behaviour": 4, "llm_code_boundary": 5, "ac_honesty": 2},
 "findings": [
  {"severity": "blocker",
   "title": "D-047 qualifier tokens missing from the quote are saved, not refused (attribution, hedge, approximation added to the summary)",
   "evidence": "app/backend/review.py:136-142 runs only grounding.new_tokens (side and negation words, grounding.py:126 and :146-160) and dropped_qualifiers. dropped_qualifiers (grounding.py:180-195) tests quote-to-summary only, e.g. grounding.py:185 'if _SELF_CARRIED.search(excerpt) and not _SELF_CARRIED.search(summary)'. Repro: probe_added_qual.py (artifacts/review-evidence/T-100/) on the 24c18a7 copy, quote 'Pain 4/10, improving.' (record 5). probe_outputs.txt lines 41-44: 'Visit 8: patient reports pain 4/10, improving.' SAVED state=needs_review; 'Visit 8: pain 4/10, possibly improving.' SAVED; 'Visit 8: pain approximately 4/10, improving.' SAVED; each with judge unavailable and no 422.",
   "why_it_matters": "Spec constraint: D-047 (memory/ORCHESTRATOR_DECISIONS.md:55) says 'side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a hard 422'; the brief says the same. The code enforces the reverse direction only. 'Patient reports' attributes a statement the record does not attribute, so this invents a fact. Under D-045(b) a human edit is exempt from the judge veto, and the gate reads only stored code reasons (trace.py:352-357), so the item exports with a warning on the item only.",
   "fix": "In _check_summary (review.py:136-142), add the reverse check before the judge call, shared by edit and manual entry: for each qualifier kind present in the new summary (self_report via grounding._SELF_CARRIED, hedge via grounding._HEDGE_WORDS, approx via grounding._APPROX) with no matching kind in the new quote, raise _bad(...) with a reason code (SUMMARY_TOKEN_NOT_IN_EXCERPT or a new named code). Keep the existing drop check.",
   "acceptance_test": "test_review_rules.py: parametrize summaries 'Visit 8: patient reports pain 4/10, improving.', 'Visit 8: pain 4/10, possibly improving.', 'Visit 8: pain approximately 4/10, improving.' against quote 'Pain 4/10, improving.'; assert 422 invalid_edit, nothing saved, no event, judge spy never called, for confirm_warnings False and True. Same three through test_manual_and_split.py manual_entry. Existing qualifier-drop test (test_review_rules.py:134) must still pass."},
  {"severity": "major",
   "title": "The export gate is not an independent second line; it trusts stored reasons that the route alone writes",
   "evidence": "app/backend/trace.py:352-357 reads cc.get('summary_tokens_not_in_excerpt') from the stored ladder and 'SUMMARY_DROPS_QUALIFIER' in R from stored state reasons. code_check_blockers (trace.py:425-439) uses those step results only; no call to grounding.new_tokens or dropped_qualifiers on the current text. Repro: probe_gate_alone.py on a scratch copy with the route token check disabled (review.py:136). probe_outputs.txt lines 53-55: 'stored state: verified []', 'gate blockers for item: []', 'export built: summary left-sided in letter/notes: True'. memory/contracts/api.md:321 says 'These are the same checks the export gate (T-098) runs, so an edit the route stores can never be an export blocker for a code reason.' The T-098 tests (test_trace.py:1030-1040, _mixed) write the state directly, so they exercise the reading path only.",
   "why_it_matters": "D-047's rationale is that the gate and the route agree so no item can be confirmed into an unexportable state. A backstop that reads the field it backstops does not catch a route regression that stores no reason. No live bypass exists at 24c18a7 (every route tried refused), so this is major, not blocker. The api.md sentence is inaccurate as written.",
   "fix": "Make the gate recompute the two pure checks from the current summary and quote for each entry it scopes (human-written, edited or accepted), in addition to the stored reasons, using the same helper the route uses. Correct api.md:321 to say what the gate actually reads.",
   "acceptance_test": "A test that writes an edit with 'Visit 8: left-sided pain 4/10, improving.' through DB.apply_review with no stored reasons (judge supported), then asserts trace.export_blockers lists the item with reason_code SUMMARY_TOKEN_NOT_IN_EXCERPT and that export_routes raises ExportBlocked. Removing the recompute must fail it."},
  {"severity": "major",
   "title": "Negation and side words are narrower than the module's own vocabulary; D-047 'negation' is not settled as the enumerated list",
   "evidence": "app/backend/grounding.py:126 _WORDS = left|right|no|not|without; grounding.py:163 _NEG also has none|never|denies|denied|negative|neither|nor; grounding.py:166 _LATERAL also has bilateral(ly); app/backend/review.py:118 _SIDE_NEG (same five words as _WORDS) is defined and never used. Repro: probe_gap.py. probe_outputs.txt lines 26-32 (judge unavailable): 'denies radiating symptoms', 'never worse', 'none reported', 'bilateral pain', 'negative for distress', 'absent distress', 'neither worse nor better' all SAVED state=needs_review, no gate blocker. Lines 33-39 (judge supported): all SAVED state=verified.",
   "why_it_matters": "The enumerated D-047 list (memory/ORCHESTRATOR_DECISIONS.md:55) is met as written, so this is not a blocker by its letter. The card, the brief and the rationale say 'side, negation or qualifier token', and a 'denies' or 'never' the record does not state is the same risk D-047 describes. The module already defines the wider class, so the two lists disagree. See question 1.",
   "fix": "Take the side and negation token set from the same _NEG and _LATERAL definitions that dropped_qualifiers uses, and delete or use _SIDE_NEG so only one list exists. If Chris confirms the enumerated list is intended, record that in D-047 and move this to a note.",
   "acceptance_test": "test_review_rules.py: parametrize 'denies radiating symptoms', 'never worse', 'none reported', 'bilateral pain' against quote 'Pain 4/10, improving.'; assert 422 with the same reason as no/not, nothing saved, judge not called."},
  {"severity": "major",
   "title": "AC 1 is checked done, but at 24c18a7 the frontend 409 branch and the e2e half were not done",
   "evidence": "board.py show T-100: AC 1 text 'no 409 confirm path remains (API + frontend copy)' with done: true, evidence 'e2e not run ... frontend copy removal handed to T-097 note'. At 24c18a7: app/frontend/review.js:126-137 and :176 (showConfirm, btn-keep-wording, needs_confirm branch); app/frontend/manual.js:45-55 (confirm_warnings, needs_confirm, retry button). 'git show --stat 24c18a7 -- tests/e2e' is empty. At HEAD f5ddec8 'git grep -n needs_confirm|btn-keep-wording|confirm_warnings HEAD -- app/frontend' shows only a comment in excerpt.js:2.",
   "why_it_matters": "A checked box says the frontend and e2e halves are done when the card's own handoff says they are not. The gap is closed at HEAD by f5ddec8 (another card, T-097 r2). I read those changes but did not run the e2e specs (Playwright and a live server are needed), so the e2e half is not verified.",
   "fix": "Keep AC 1 open for the frontend and e2e clauses, or split them to T-097 and cite f5ddec8 as their evidence. Run tests/e2e/test_edit.py and test_rerun_judge.py on a live server before closing.",
   "acceptance_test": "git grep -n 'needs_confirm|btn-keep-wording|confirm_warnings' -- app/frontend returns no product match at the commit that closes AC 1; the e2e specs above pass against a live server."},
  {"severity": "minor",
   "title": "The D-040 speaker-word string is still in the user-facing 422 message",
   "evidence": "app/backend/review.py:119 '\"self_report\": \"an attribution phrase (such as complained of or reports)\"', rendered by review.py:141-142 for SUMMARY_DROPS_QUALIFIER. Byte-identical at 24c18a7 and HEAD ('git show 24c18a7:app/backend/review.py | sed -n 119p' equals 'git show HEAD:app/backend/review.py | sed -n 119p'). D-040 (memory/ORCHESTRATOR_DECISIONS.md:48): no code or model labels who is speaking.",
   "why_it_matters": "The brief asked for this string to be reworded and it was not. The message does not label a speaker, so it does not breach D-040 by its letter, but it puts the speech verbs D-040 retired into user-facing text.",
   "fix": "Name the kind without speech verbs, e.g. 'a word that says whose account the quote gives', and keep the example verbs out of the 422 text.",
   "acceptance_test": "A test that drops the self-report kind asserts the message contains neither 'reports' nor 'complained', and still says the qualifier is missing from the summary."},
  {"severity": "minor",
   "title": "HIGHLIGHT_NOT_FOUND is now a hard 422, which D-047 does not cover",
   "evidence": "app/backend/review.py:143-144 raises _bad('The quoted sentences cannot be found in the record...', reason='HIGHLIGHT_NOT_FOUND') before the judge. At 24c18a7 this path appended a code reason and saved as needs_review (see the removed lines in the 24c18a7 diff of review.py). memory/contracts/api.md:321 lists it among the 422 causes.",
   "why_it_matters": "D-047 covers side, negation and qualifier tokens. A summary-only edit on an item whose quote cannot be located is now refused rather than saved for review. That is a behaviour change nobody decided.",
   "fix": "Either restore the needs_review path, or record the decision in ORCHESTRATOR_DECISIONS.md and keep the api.md line.",
   "acceptance_test": "Whichever is chosen, a test pins it: summary-only edit on an item with an unlocatable quote returns the decided result."},
  {"severity": "minor",
   "title": "The handoff test count is not reproducible from the commit",
   "evidence": "Handoff: 'tests/unit 1834 passed (1 skipped)'. On the git archive of 24c18a7 the same command gives 1814 passed, 4 skipped (3 'no git repository here (exported tree)' skips plus the live judge eval). In the working tree at f5ddec8 with other cards' changes: 2 failed, 1832 passed, 1 skipped. The T-100 selection gives 103 passed in both trees.",
   "why_it_matters": "Evidence must reproduce from the cited commit. The 1834 figure matches neither tree.",
   "fix": "Record the commit sha and the exact command with its output in the card evidence, run from a clean archive.",
   "acceptance_test": "Re-running the stated command on git archive 24c18a7 gives the number written on the card."},
  {"severity": "minor",
   "title": "No test pins the JUDGE_PARTIAL warning for a human-written edit",
   "evidence": "git grep -n 'partially' 24c18a7 -- tests/unit/test_review_rules.py tests/unit/test_manual_and_split.py tests/unit/test_api_routes.py is empty. Human-edit judge tests cover 'unsupported' and 'unavailable' only. The branch is review.py:150-151. probe_verdicts.py gives partially -> needs_review, warning JUDGE_PARTIAL, consistent with the code.",
   "why_it_matters": "The orchestrator's judge-objection rule has one untested branch. It works today, but nothing stops it regressing.",
   "fix": "Parametrize the existing judge-objection tests over 'partially' and 'unsupported'.",
   "acceptance_test": "test_seeded_herniation_judge_unsupported_saves_as_needs_review_with_warning passes for judge partially as well, asserting warning JUDGE_PARTIAL."},
  {"severity": "nit",
   "title": "Dead or always-empty fields left behind by the change",
   "evidence": "app/backend/review.py:118 _SIDE_NEG is never used. review.py:128, :155 and :157 keep code_reasons and 'toks' that are now always empty. review.py:207 stores summary_tokens_not_in_excerpt, which is always []; trace.py:352 reads it.",
   "why_it_matters": "The stored field looks like a check result but is always empty, which is misleading to the next reader of the trace.",
   "fix": "Delete the dead constant and the always-empty fields, or make them mean something.",
   "acceptance_test": "No behaviour change: tests/unit passes unchanged after removal."},
  {"severity": "nit",
   "title": "Wording and test-style nits",
   "evidence": "review.py:138 renders 'The summary says “left”, “no”, which the quote does not say.' (two words read as a list). test_api_routes.py:367-374 greps source text for confirm_warnings and keep_my_wording rather than testing behaviour (persona item 13). app/db/db.py:20 still lists keep_my_wording as a writable DB action; no route can reach it (review.py:15 ACTIONS excludes it).",
   "why_it_matters": "Small clarity issues; the DB action is harmless today but is the second place the removed path could come back.",
   "fix": "Say 'and' between two words; keep the behavioural test and drop the source grep; remove keep_my_wording from db.py ACTIONS when that file's owner next touches it.",
   "acceptance_test": "tests/unit still passes; the message for two words contains 'and'."}
 ],
 "whats_right": [
  "Every refusal route tried (confirm_warnings, force, override+keep_my_wording+confirm, string 'true', manual entry, batch edit) returns 422 or 400 and leaves the case JSON identical; batch accept ignores the edits payload (probe_outputs.txt lines 3-6).",
  "A judge objection to a human edit is consistent: edit and manual entry both return chk['warnings'] (review.py:212 and :360), and the warning code equals the state reason for partially, unsupported and unavailable (probe_outputs.txt lines 46-51).",
  "The token check runs before any judge call and is pinned: disabling it fails 20 tests across test_review_rules.py, test_manual_and_split.py and test_api_routes.py."
 ],
 "questions_for_chris": [
  "D-047 'negation': is it the enumerated list (no, not, without) or the class (denies, never, none, negative, absent, neither, nor)? Blocker if class; major if the list. Same question for side words (bilateral).",
  "Is the HIGHLIGHT_NOT_FOUND hard 422 (review.py:143-144) intended, or should it stay a needs_review warning as before 24c18a7?",
  "Pre-D-047 overrides: export.py at 24c18a7 no longer prints 'paralegal confirmed keep my wording (reviewer override: ...)' in internal notes for old items. review_events rows remain in the DB. Should the notes still disclose legacy overrides?"
 ]}
```
