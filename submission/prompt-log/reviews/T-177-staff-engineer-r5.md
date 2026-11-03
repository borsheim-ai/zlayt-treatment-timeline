# T-177 round 5 (final, narrow; D-069 / D-065): staff-engineer-reviewer

**Verdict: pass (0 blockers, 0 majors, 0 minors).** The round-4 F1 major is closed. My three surviving mutants (B2, B4, C5) now each turn the property test red. Two fresh mutants of my own, one in an edit-path message and one in a manual-entry message, are also red, and the test fails on the model name in each. The live demo is clean on the edit, manual-entry and code-removed paths. A differential run of the same probe on the round-4 build (3feb096) finds the real leak the worker fixed, so the probe can see it. The unit suite gives the figure the handoff quotes.

**Scope.** Fix commit e425534 (touches `app/backend/review.py`, `app/backend/why.py`, `tests/unit/test_prepared_property.py`), reviewed from `git archive e425534` (`artifacts/review-evidence/T-177-staff-engineer-r5/archive-source-sha.txt`). Evidence is under `artifacts/review-evidence/T-177-staff-engineer-r5/`. HEAD moved to bd72d5b during the review. `git log e425534..HEAD` shows T-200, T-187/T-198 and T-181 only, and `git diff --stat e425534 HEAD` on the three T-177 files is empty. I mutated only archive copies and restored each from `git show e425534:<path>`, byte-compared. After all mutants and the unit run, the source tree matches a fresh archive of e425534 (`diff -rq`, no output).

## Round-4 status

| Round-4 item | Status at e425534 |
|---|---|
| F1 major: property test never reaches unsupported-summary, edit and accept-without-judge families; twins deletable | Fixed. `FAULTS` now includes `unsupported`; `actions()` edits a quote then accepts, accepts an entry with no second-check answer, and writes a manual entry for each record with no live entry; a static test checks twin completeness. B2, B4, C5 are killed (below) |
| F5 nit: `INJECTION_SUSPECTED` has no twin | Fixed. `why.py` `_WHY_PREPARED["INJECTION_SUSPECTED"]`; mutant T1 (twin removed) is killed by the static test |
| F2 minor, F3 minor, F4 nit (exemptions, evidence counts, disclosure line) | Accepted minors, not graded. For the record, the handoff figures now reproduce: 34 passed, 3 skipped for the property file and 5865 passed, 11 skipped for the unit suite (my runs) |

The worker's handoff also reports a new live leak that the extended test found in `review._check_summary` (the edit and manual-entry second-check warning had no provenance argument). I confirmed it as a real fix. On the round-4 build, the edit warning reads "The AI second check is not available in this demo" on a prepared item (`probe-r5-http-control-on-3feb096.out`: 1 hit by my scan, 0 by the round-4 scanner). At e425534 it reads "The second check is not available in this demo".

## What I exercised

- **Mutants B2, B4, C5 (item 1).** Applied one at a time to a `git archive e425534` copy with `run_mutants_r5.py` (the r4 harness, SHA retargeted), `pytest tests/unit/test_prepared_property.py -x`, restored and byte-compared (`mutants-batch1.out`). Baseline first: 34 passed, 3 skipped (`baseline-property.out`).
  - B2 (`trace.py` skipped step for SUMMARY_NOT_IN_QUOTE says "whole AI summary"): KILLED, `test_no_prepared_text_names_an_ai_or_a_model[sample-unsupported-one]`.
  - B4 (`why.py` twin for SUMMARY_NOT_IN_QUOTE says "AI summary"): KILLED, same test id.
  - C5 (`trace.py:128` drops all seven `TRACE_WHY_PREPARED` twins): KILLED, `[sample-valid-one]`.
- **Fresh mutants (item 2).** `mutants-batch1.out`, `mutants-batch2.out`, `mutants-batch3.out`:
  - N1, edit path: `_edit` returns a warning "The edited quote was checked again with claude-sonnet-5-5." KILLED, `[sample-valid-one]`.
  - N2, manual-entry path: `manual_entry` returns a warning "Entered by hand; claude-sonnet-5-5 was not used." KILLED, `[sample-malformed-one]`.
  - `why-N1-N2.out` shows both fail for the right reason: `('edit', '.warnings[].message', 'claude')` and `('manual', '.warnings[].message', 'claude')`, quoting my inserted sentences.
  - N3 and N4 (the real fix reverted: the `prep=` argument removed from the `_edit` and `manual_entry` calls): both KILLED.
  - T1 (remove the `INJECTION_SUSPECTED` twin): KILLED by `test_every_sentence_that_names_an_ai_has_a_prepared_twin_and_no_twin_names_one`. T2 (remove the `JUDGE_NOT_RUN` trace twin): KILLED. T3 (misspell the `SUMMARY_NOT_IN_QUOTE` twin key, so the prepared text is gone): KILLED. These three cover the "remove one prepared twin" part of item 2 in three different tables.
  - N5 (bonus; `compare_error` uses `_DISPUTE_SENTENCE[v]` instead of the prepared table): KILLED, via `case_lib10_eob_ub04_cms1500-valid-one`.
  - All 12 mutants (B2, B4, C5, N1 to N5, T1 to T3) were killed. None survived.
- **Live probe (item 3).** My own demo-mode servers (no `ZLAYT_MODE`, `LLM_BACKEND=fixture`) from a `git archive e425534` copy, over HTTP, on loopback ports 54451 to 54454 with `probe_r5_http.py`.
  - `unsupported` (e1's prepared summary replaced by one its quote lacks; port 54452, `probe-r5-http-unsupported.out`): code-removed path: e1 item is `prepared: True` with why "Every part of the prepared summary added something its quote does not contain ... so code removed all of it and no entry was made", and the trace steps read "Not run: code removed the whole prepared summary...". Edit path: edit of e2 and e3 returns 200 with warning "The second check is not available in this demo...", the item `why` and the `human` trace step say "the summary is still the prepared wording and its second check has no answer on the new quote". Manual path: hand entry on record r1 returns 201 with the same prepared warning. My scan of the 20 explicit-path responses: 0 hits for `AI`, `claude`, `sonnet`, "Drafted by" and the authorship phrases. The worker's `collect()` and `offenders()` over a second case (92 responses, 16 prepared items, edit:e2, edit:e3 and manual:r1 present): 0 offenders. `case.models` is `hand-checked (qa)` / `claude-haiku-5-5` / `generator_prepared: True`. `/classic` answers 307 to `/`.
  - `control` (shipped `FIXTURE_SET=curated`; port 54453, `probe-r5-http-control.out`): edit e1 and e2 return 200 with the prepared warning; my scan 0 hits; worker scanner 0 offenders over 89 responses.
  - Differential run on the round-4 build 3feb096 (port 54454, `probe-r5-http-control-on-3feb096.out`): my scan finds 1 hit, `('edit', '.warnings[].message', 'The AI ')`, in the edit response. The worker's scanner found 0 there because the round-4 `collect` had no edit pass. So the probe separates the two builds.
  - PIDs: the probe checks `lsof` (listening port) and cwd (the archive) before `terminate()`. Output shows "stop: pid 51803, 51964, 52020, 52201 ... cwd is archive: True" and "listener after stop: none" for each. `lsof -iTCP:54440-54460 -sTCP:LISTEN` returns nothing now. I stopped only my own PIDs.
- **Suites (item 4).** `pytest tests/unit -q` in the e425534 archive: 5865 passed, 11 skipped in 410.26 s (`unit-suite.out`), the same counts the handoff reports. `pytest tests/unit/test_prepared_property.py`: 34 passed, 3 skipped (the three are the valid/all combinations, `test_prepared_property.py` `pytest.skip("valid has no scope")`).
- Read in full: `reviews/T-177-staff-engineer-r4.md`, the card handoff and notes, `git show e425534` (all three files), the property test (all 369 lines), `review.py` around `_check_summary`, `_edit`, `manual_entry`, `compare_error`, `why.unavailable_sentence`.
- Not run: the guided E2E (`E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_demo_provenance.py`, handoff says 130 passed; not in the brief), the eval runner, a browser. The accepted minors (shape-based exemptions, the unpinned disclosure line, the classic tooltip at `timeline.js:22`) were not graded.

## Verdict rule

No blocker, no major, no minor, so `pass`.

```json
{"card": "T-177", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive e425534 (fix commit; app/backend/review.py, app/backend/why.py, tests/unit/test_prepared_property.py); own demo-mode servers on loopback ports 54451-54454; sample case, curated set and an unsupported-summary fault; edit, manual-entry and code-removed paths",
 "exercised": [
  "git archive e425534 into a unique scratch dir; diff -rq against a second fresh archive after all mutants and the unit run: no difference",
  "pytest tests/unit/test_prepared_property.py baseline in the archive: 34 passed, 3 skipped",
  "r4 mutants B2, B4, C5 re-applied via run_mutants_r5.py: all three KILLED (sample-unsupported-one, sample-unsupported-one, sample-valid-one)",
  "fresh mutants: N1 model name in an edit-path warning (KILLED), N2 model name in a manual-entry warning (KILLED), N3/N4 prep argument reverted on _edit/manual_entry (KILLED), T1/T2/T3 one prepared twin removed in why.py and trace.py (KILLED), N5 dispute sentence twin unused (KILLED); each restored from git show e425534 and byte-compared",
  "why_mutant_r5.py on N1 and N2: failure text quotes the inserted sentence at .warnings[].message",
  "probe_r5_http.py on my own demo-mode servers (ports 54451-54454): unsupported fault and shipped curated set; edit, manual-entry and code-removed paths printed; my authorship regex 0 hits; worker offenders() 0 over 92 and 89 responses; /classic 307 to /",
  "same probe on a git archive of 3feb096: 1 hit in the edit warning ('The AI second check is not available in this demo'), so the probe separates the builds",
  "lsof + cwd check before every terminate(); lsof -iTCP:54440-54460 -sTCP:LISTEN empty afterwards",
  "pytest tests/unit -q in the archive: 5865 passed, 11 skipped in 410.26 s",
  "git log e425534..HEAD and git diff --stat e425534 HEAD on the three T-177 files: HEAD moved to bd72d5b, no T-177 file changed",
  "read reviews/T-177-staff-engineer-r4.md, the card handoff, git show e425534, the property test, review.py/why.py around the changed lines"
 ],
 "verdict": "pass",
 "scores": {"d069_structural_fix_in_product": 5, "property_test_strength": 5, "edit_manual_code_removed_paths_live": 5, "failure_visibility": 5, "evidence_reproducibility": 5},
 "findings": [],
 "whats_right": [
  "The property test now injects an unsupported-summary fault and runs an edit, accept-plain and hand-entry pass; 12 of 12 mutants across the twin tables and the edit/manual messages turn it red.",
  "Static twin test (every AI-wording why/trace/next sentence has a twin, no twin names an AI, no orphan code) closes the silent twin-or-AI fallback; the non-vacuity test pins that the edit and unavailable twins actually appear.",
  "The worker followed the probe to the real leak (review._check_summary warning without a provenance argument) instead of only patching the lines I had mutated; the fix is small and the handoff counts reproduce (34/3 and 5865/11)."
 ],
 "questions_for_chris": []}
```
