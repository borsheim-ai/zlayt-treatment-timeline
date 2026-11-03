# T-201 staff-engineer review (commit 9611f02, tests/e2e only)

Verdict: pass (no blocker, no major). The three edits keep their intent; none weakens a check that the old text really made. Four minor/nit gaps, none introduced by this commit except the provenance XOR (finding 2).

Per test:
- test_letter_matrix: the old `"AI assistance" in notes` was wrong for a prepared case (D-065/D-069), so replacing it was needed. The new XOR (`("AI assistance" in notes) != ("answers the team prepared for this demo" in notes)`) catches "both" and "neither", but not "the wrong line for the case kind". See finding 2. The letter-side check (`_leaks`, TYPE_WORDS) was not touched by the commit.
- test_edit_to_check: waiting on the server's own `why` (`expect(...).to_contain_text(why)`) is a real wait on a condition, not a sleep, and it is itself an assertion that the server sentence reached the row. The `second (ai )?check` regex keeps the other assertions. Residual in finding 3.
- test_mvp_finish: the wait for `library-list button` is a condition wait (30 s cap), the library button is still asserted afterwards. It hides the late-library race in the product; that race is tracked on T-204 (in_review), so it is not lost.

Can the letter carry AI or model text with no test catching it? Not repo-wide. In tests/e2e the letter-specific tests are blind to it, though: the matrix and the isolation test ban only the literal "AI assistance". Mutants (full table in artifacts/review-evidence/T-201/mutants.md):
- M1, "Drafted by an AI model (claude-sonnet-5-5)." in the sample letter: test_letter_matrix + test_letter_isolation 17 passed; caught by 3 e2e golden-compare tests and a unit golden test.
- M2, same text on every non-sample case: letter/export e2e subset 49 passed; caught only by unit tests (test_prepared_property for lib10, plus an incidental line-number test).

Baseline: fresh `git archive 9611f02`, `E2E_REQUIRE_DB=1 pytest tests/e2e`: 554 collected, 553 passed, 1 skipped, 0 failed (another agent's pytest was running on the machine at the same time, so this ran under load).

```json
{"card": "T-201", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 9611f02: tests/e2e/test_letter_matrix.py, test_edit_to_check.py, test_mvp_finish.py; fresh git archive 9611f02; private fixture-backend server started by tests/e2e/conftest.py; sample case and case_01..09",
 "exercised": [
  "read personas/staff-engineer.md, the T-201 card and handoff, and git show 9611f02 -- tests/e2e in full",
  "git archive 9611f02, then E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e -q: 554 collected, 553 passed, 1 skipped, 0 failed",
  "git archive 986fc55 --collect-only: 554 (AC evidence implies 548)",
  "mutant M1 (AI/model sentence in the sample letter): letter_matrix + letter_isolation 17 passed; -k golden/step4/export_ui/letter/copy subset 3 failed 43 passed; unit test_case_extras golden failed",
  "mutant M2 (same text, non-sample cases only): letter_matrix + letter_isolation 17 passed; e2e letter/export subset 49 passed; full tests/unit 2 failed 5930 passed",
  "mutant M3 (same text, live/non-prepared only): full tests/unit 5 failed 5927 passed",
  "mutant M4 (notes always use AI_LINE, prepared case): test_letter_matrix 14 passed; guided/test_step4 notes-vs-golden 1 failed",
  "read tests/e2e/test_letter_matrix.py, test_edit_to_check.py around the changed lines, app/backend/export.py _letter and AI_LINE/AI_LINE_PREPARED, app/frontend/review.js AI_HELD, input.js demoRefusal; board show T-204",
  "grep of the commit's added lines for emails, key patterns and absolute home paths: 0 private values found (<redacted> count 0)"],
 "verdict": "pass",
 "scores": {"intent_preserved": 4, "determinism_of_waits": 4, "mutation_resistance_e2e_letter": 2, "evidence_accuracy": 3},
 "findings": [
  {"severity": "minor", "title": "E2E letter tests ban only the literal 'AI assistance'; an AI or model sentence in the letter passes test_letter_matrix and test_letter_isolation",
   "evidence": "tests/e2e/test_letter_matrix.py:23 TYPE_WORDS has 'AI assistance' only; tests/e2e/test_letter_isolation.py:7 BAD likewise. In a fresh archive of 9611f02 with _letter changed to out = [LETTER_TITLE, \"\", \"Drafted by an AI model (claude-sonnet-5-5).\", \"\"]: `pytest tests/e2e/test_letter_matrix.py tests/e2e/test_letter_isolation.py` -> '17 passed'. With the same text skipped for the 9-entry sample (M2) the e2e letter/export subset gives '49 passed'. Not introduced by 9611f02 (it did not touch the letter check), but the card's AC 1 says 'letter carries no AI/model text for prepared or live cases' and the matrix docstring claims the property.",
   "why_it_matters": "D-065/D-069 say a prepared letter never names an AI or a model. In tests/e2e only the sample-golden byte compare and the unit suite would notice a different wording ('Drafted by an AI model', a model id, 'Claude'); for non-sample cases the e2e letter tests stay green.",
   "fix": "Add model-id and word-boundary 'AI' / 'model' / 'Claude' / 'drafted' patterns to the letter ban in _leaks (applied to the residue, so a quote that says 'AI' inside an accepted entry is still allowed), and have test_the_check_catches_a_planted_leak plant one of them.",
   "acceptance_test": "Planting 'Drafted by an AI model (claude-sonnet-5-5).' into the letter of any one of the 10 matrix cases makes test_letter_never_carries_flag_note_count_or_ai_text fail, and test_the_check_catches_a_planted_leak includes that planted string."},
  {"severity": "minor", "title": "Provenance XOR in test_letter_matrix does not bind the line to the case kind",
   "evidence": "tests/e2e/test_letter_matrix.py:118 `assert (\"AI assistance\" in notes) != (\"answers the team prepared for this demo\" in notes)`. Mutant M4 (export.py:766 always AI_LINE): test_letter_matrix '14 passed'. Only guided/test_step4 (sample only) failed: 'FAILED tests/e2e/guided/test_step4.py::test_letter_ready_copy_and_download_match_the_export_and_nothing_moves'.",
   "why_it_matters": "These matrix cases come from the curated (prepared) fixture set, so the prepared line is the only right answer; D-069 says the notes of a prepared case never say an AI drafted it. The XOR also accepts that regression for case_01..09, which the old (wrong) assertion could not distinguish either.",
   "fix": "Derive the expected line from the case (prepared flag in GET case, or 'curated' set) and assert present and the other absent, instead of 'exactly one'.",
   "acceptance_test": "With export.py always returning AI_LINE for a prepared case, test_letter_matrix fails for every case that has flags."},
  {"severity": "nit", "title": "test_edit_to_check now accepts either wording of 'second (AI )?check' and follows the server sentence, so it no longer pins prepared vs live wording",
   "evidence": "tests/e2e/test_edit_to_check.py (changed lines): `re.search(r\"second (ai )?check\", hint)` and `expect(...).to_contain_text(why)`. If the backend's trace why for a prepared item said 'second AI check' this test still passes.",
   "why_it_matters": "The edit is correct for the intent 'the row shows the server's words'; the D-069 no-AI-wording guarantee for prepared items lives elsewhere (unit test_prepared_property, and the T-204 e2e). It is a backstop, not a gap, but this test used to fail on the wrong wording and now cannot.",
   "fix": "Optional: when the fixture item is prepared, assert `'ai' not in why.lower().split()` here, or cite the T-204 test that does.",
   "acceptance_test": "A backend returning 'second AI check' in the human step why of a prepared item fails this test or the cited one."},
  {"severity": "minor", "title": "AC evidence count does not match any archive",
   "evidence": "T-201 AC 1 evidence: '547 passed, 1 skipped'. My fresh archives: `git archive 9611f02` and `git archive 986fc55` both collect 554 tests; the 9611f02 run is 553 passed, 1 skipped. The handoff also ran 'HEAD (pre-fix) + 3 edits overlaid', not the commit's own archive.",
   "why_it_matters": "The AC asks for 'exact count' from a fresh archive; a count that cannot be reproduced undermines the evidence trail for a card whose whole point is a trustworthy green run.",
   "fix": "Re-record AC 1 with the count of the commit's own archive (553 passed, 1 skipped, 554 collected) and name the skipped test.",
   "acceptance_test": "`git archive <commit> | tar -x -C <dir>; cd <dir>; E2E_REQUIRE_DB=1 pytest tests/e2e -q -rs` reproduces the recorded numbers and names the one skip."}
 ],
 "whats_right": [
  "The waits are on conditions (server why text, library button attached) with a cap, not sleeps, and the assertions that follow them are unchanged.",
  "The product was not touched; the commit message and handoff say which side was stale test versus timing, and T-204 tracks the product flash and late-library race.",
  "tests/unit plus the sample-golden e2e tests do fail on an AI sentence in the letter for both prepared and live cases (M1, M3)."],
 "questions_for_chris": []}
```
