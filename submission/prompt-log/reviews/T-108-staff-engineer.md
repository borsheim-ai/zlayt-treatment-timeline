# T-108 review (staff-engineer-reviewer, r1): quote picker units from the quotable body

Commit d3e127c, `fix(backend): quote picker units come from the quotable body only`. Reviewed on a fresh `git archive d3e127c` copy. The live repo is at 1526a1f with uncommitted edits, so no live-tree result is cited here. Model recorded is the model I actually ran as, claude-haiku-5-5 (the dossier's expected id is claude-sonnet-5-5).

**Verdict: changes** (0 blockers, 2 majors, 5 minors, 1 nit).

## Summary

On the sample and case_01..09 the change works. 59 records and 150 units: no `Excerpt`, `Date:`, `Source:`, `===`, or quote-mark text, every unit is a verbatim slice at its true offset, and every unit plus its trailing hedge chain passes the same check the save routes run. The real-backend Change-the-quote e2e passes 3/3. Reverting the units to the whole block fails 13/13 unit tests and 3/3 e2e tests.

Three gaps remain:
1. A sentence that a hedge qualifies cannot be picked alone. The picker never adds the hedge, but the unit test helper assumes it does, so the test is green while the UI refuses those sentences (F1, major).
2. `quote_body` falls back silently to the whole record block. A record with an `Excerpt:` line and no Date/Source line still shows the label and header lines in the units (F2, major).
3. The offset branch can be deleted without any test failing, and curly quotes are not covered (F3, F4, minor).

## Exercised

- `git archive d3e127c` into the scratchpad copy `T108_verify`. A second copy matched it file for file (the only differences were `__pycache__`).
- `/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit` on that copy: `2077 passed, 4 skipped`. Skips: 3 need a `.git` directory the export lacks, and 1 is the live-judge eval gated by env. Output saved at `artifacts/review-evidence/T-108/unit-run.txt`.
- `pytest tests/unit/test_quote_units.py -v`: 13 passed.
- `artifacts/review-evidence/T-108/probe_units.py` over sample and case_01..09 (10 cases, 59 records, 150 units). Each unit is checked with `spanish.module_for(...).check_excerpt`, the call review.py:300 and :451 make, both alone and with the trailing hedge chain. Output: `artifacts/review-evidence/T-108/probe-units-output.json`.
- `artifacts/review-evidence/T-108/probe_shapes2.py` over six synthetic record shapes (A to F) through `ingest.split_records` and `present.quote_body`. No API call. Output: `artifacts/review-evidence/T-108/probe-shapes-output.txt`.
- Real backend: the archive copy served on 127.0.0.1:7971 with `ZLAYT_DB` set to a scratch sqlite file, `DATA_DIR` set to an empty sentinel directory, `LLM_BACKEND=fixture`, `FIXTURE_SET=curated`. `tests/e2e/test_change_the_quote.py`: 3 passed (`artifacts/review-evidence/T-108/e2e-head-run.txt`). The scratch sqlite file received the writes and the sentinel stayed empty.
- `artifacts/review-evidence/T-108/single_unit.py` against that server: a sample case, entry e8 on r8, `POST .../items/e8/review` with `{"action":"edit","edits":{"excerpt":<unit 0 alone>}}` gave 422 `invalid_edit` with reasons `["EXCERPT_OMITS_QUALIFIER"]`. Output: `artifacts/review-evidence/T-108/single-unit-output.txt`.
- Mutants, scratch copies only, not committed. M1: `quote_body` returns `(0, block)` (the pre-fix behaviour). M2: the label/quote-mark branch disabled at present.py:165 (`if False:`). Results in `mutant-M1-unit.txt`, `mutant-M1-e2e.txt` (run on a second server on :7972) and `mutant-M2-unit.txt`. `artifacts/review-evidence/T-108/mutate.py` is the helper.
- Read in full: `personas/staff-engineer.md`; `app/backend/present.py`; `app/backend/sentences.py`; `app/backend/grounding.py` (`check_excerpt`); `app/backend/spanish_text.py` (`check_excerpt`); `app/backend/review.py` (edit and manual_entry); `app/backend/store.py` (`load_records`); `app/backend/ingest.py` (`_excerpt_extent`); `app/backend/api.py` (demo gate); `app/frontend/excerpt.js`; `app/frontend/manual.js`; `tests/unit/test_quote_units.py`; `tests/e2e/test_change_the_quote.py`; the `tests/e2e/conftest.py` diff.
- Not exercised: a non-demo paste (no API key, no `claude-cli`); the browser DOM outside the e2e spec.

## Findings

**F1 (major). A sentence that a hedge qualifies cannot be picked on its own.** The picker never adds the qualifying hedge. The unit test's `_pick` helper does add it, and its docstring says the picker does. The UI-built quote is refused.
Evidence: `app/frontend/excerpt.js:35` (`pick(i)` only moves `lo`/`hi`) and `:38` (text is `units[lo].start` to `units[hi].end`, no hedge extension). `tests/unit/test_quote_units.py:25` says "The quote the picker builds for unit i: the unit plus any hedge units that immediately follow it"; `_pick` (lines 24-30) implements that rule. Repro: with the archive server on :7971, run `artifacts/review-evidence/T-108/single_unit.py`. Sample r8 unit 0, "C5-C6 disc protrusion with mild right foraminal narrowing.", alone gives 422 `invalid_edit` / `EXCERPT_OMITS_QUALIFIER`. Across 150 units, 3 fail alone: sample r8 (2 units) and case_08 r2, "Signal change in the supraspinatus tendon." (`probe-units-output.json`, `alone_fail`).
Why it matters: the card AC says "picking whole sentences yields a valid verbatim quote on sample and case_01..09". That is false for 3 sentences. The green `test_every_offered_unit_is_a_valid_quote` cannot catch it because `_pick` supplies the hedge. The handoff's "Left" note discloses the rule, but the AC and the docstring say the opposite of what the UI does.
Fix: choose one. (a) `excerpt.js` extends a selection through the trailing hedge run, the same chain `_pick` builds, and checks those boxes. (b) Keep the UI, restate the AC and the docstring, and make the test drive the UI rule: unit alone gives 422 `EXCERPT_OMITS_QUALIFIER`, unit plus hedge chain gives 201.
Acceptance test: for sample r8 unit 0 and case_08 r2 unit 0, the text the picker would submit is saved (201) under (a), or is refused with `EXCERPT_OMITS_QUALIFIER` under (b). The test must submit the UI-built text, not the `_pick` text, and must fail if the picker stops extending.

**F2 (major). `quote_body` falls back silently to the whole record block, so label-only and date-less records leak `Excerpt:` and header lines into the units.** This is the bug the card claims to fix, and it still happens for a reachable record shape.
Evidence: `app/backend/present.py:160-163` (`try: body = ingest.split_records(block)[0]["excerpt"]` / `except Exception: body = block`) and `:167-168` (`i = block.find(body)`; `return (i, body) if i >= 0 else (0, block)`). Verbatim output from `probe-shapes-output.txt`:
`A_excerpt_only | units=['Excerpt: "Pain persists after two weeks.', 'Taking meds daily."']`
`C_source_excerpt | units=['Source: Synthetic Clinic', 'Excerpt: "Pain persists after two weeks.', 'Taking meds daily."']`
Repro: `/Users/arsis/zlayt-pm-project/.venv/bin/python artifacts/review-evidence/T-108/probe_shapes2.py <path to an archive copy of d3e127c>`.
The stored excerpt (`app/backend/store.py:22-25`, same split) also keeps the label for these shapes, so the save route checks quotes against text that includes it. The label comes from upstream, but this commit's fallback is what puts it in the picker.
Reachability: `POST /api/cases` with pasted text returns 409 `demo_mode_unsupported_input` unless live mode is on (`api.py:287-288`; live gate at `api.py:116-120`). I saw that 409 with `ENABLE_LIVE` unset. I did not exercise live mode, so reachability in live mode is inferred from the code.
Why it matters: the commit's invariant (no label, quote marks, or header lines; "cut from the excerpt body") fails silently on an input the golden set does not contain. The broad `except` and the `(0, block)` return turn a split failure into exactly the bug this card fixes, with no status shown. That is a silent fallback (persona 4.12). Not a blocker: no fact is invented and the save route still checks verbatim. Major because the AC is stated generically.
Fix: a record whose body cannot be located gives no units and a visible state (for example a `record_warning`), not the block. Remove the broad `except` so the split error surfaces. Strip the `Excerpt:` label and any `Date:`/`Source:` lines for unsplit records, or classify the record as unsplit with its own state.
Acceptance test: `test_quote_body_cases` (tests/unit/test_quote_units.py:80) gains shapes A and C. Each asserts that no unit starts with `Excerpt` or `Source:` and no unit contains a double quote. A record that cannot be split yields no units plus a reason. The current `(0, block)` branch must fail this test.

**F3 (minor). Removing the label/quote-mark offset branch passes every quote test.** Evidence: present.py:164-166. Mutant M2 (`if False:` at :165) passes 13/13 (`mutant-M2-unit.txt`). For shape F (`Source:` repeats the body), the correct base is 69 and `block.find` gives 25, which is the Source line (`probe-shapes-output.txt`). Without the branch, unit offsets point into the Source line. No golden case or test covers this. The only offset test that touches `quote_body` (line 83) uses a body that appears once.
Why it matters: the card's "at their true offsets" claim is untested for repeated text.
Fix and acceptance: add shape F to `test_quote_body_cases` and assert `raw[u.start:u.end] == u.text` and that `u.start` lies inside the excerpt body. M2 must fail it.

**F4 (minor). Curly quotes survive as wrapper, and the quote-mark assertions cover the sample only.** Evidence: `app/backend/ingest.py:63` strips only straight `"`. Shape D gives `units=['“Pain persists after two weeks.', 'Taking meds daily.”']`. The no-quote-mark check is in `test_sample_units_have_no_wrapper` (test_quote_units.py:59-66) and in e2e `test_change_the_quote.py:27` and `:51`. Both are sample-only. `test_every_offered_unit_is_a_valid_quote` (line 49) checks only `startswith`. Golden cases show no quote marks today (`probe-units-output.json`, `wrapper` = 0 everywhere), so this is a latent gap.
Fix: strip matched curly pairs in the excerpt extent, or give the record a state. Extend the quote-mark assertion to every case at line 49.
Acceptance test: shape D gives units with no `“`, `”`, or `"`, and line 49's assertion covers case_01..09 as well as the sample.

**F5 (minor). The "2110 passed" evidence does not reproduce at the cited commit.** Card T-108 AC says "tests/unit full run 2110 passed". At d3e127c, `pytest --collect-only -q tests/unit` collects 2081 and the run gives `2077 passed, 4 skipped` (`unit-run.txt`). The live tree at 1526a1f, with 1291 untracked files and uncommitted edits, collects 2206. The 2110 figure probably comes from a different tree.
Fix: rerun at d3e127c, and name the commit and the pytest tail line in the AC evidence.

**F6 (minor). The frontend strips the wrapper again in `manual.js`, which can hide a backend regression.** `app/frontend/manual.js:14-23` (`quotable(rec)`) removes `===`/`Date:`/`Source:` lines, the `Excerpt:` label, and a trailing quote from `rec.sentences` on the client. A backend leak would be hidden in the manual-entry tray, and the rule now lives in two places that can drift.
Fix: have the tray take the backend units as they are (or assert on the tray's inputs), and keep one copy of the rule.

**F7 (minor). The "excerpt-error hidden" check in the e2e runs before the save response.** Evidence: `tests/e2e/test_change_the_quote.py:59` (`expect(ed.get_by_test_id("excerpt-error")).to_be_hidden()`) runs straight after the `btn-save-excerpt` click. The error box starts hidden, so the check passes at once. The real check is the poll at lines 60-65.
Fix: wait for the save response (for example `expect_response`) or drop line 59.
Acceptance test: with the line dropped or the wait added, the spec still passes on the fixed build and fails when the picker's submit is broken. (This is also a nit under F7, kept at minor because it sits in a required AC test.)

**F8 (nit). Naming.** `_pick` in `test_quote_units.py` builds the quote the picker should build, not what the picker builds. Rename it `_hedge_chain_quote` (or similar) once F1 is decided.

## What is right

- Units come from the same body the save route checks, at absolute offsets: 150 units with zero not-verbatim, out-of-block, or wrapper hits on sample and case_01..09, and zero pick failures once the trailing hedge is included (`probe-units-output.json`).
- The fix is locked by tests: reverting to whole-block units fails all 13 quote unit tests and all 3 real-backend e2e tests (`mutant-M1-unit.txt`, `mutant-M1-e2e.txt`).
- The picker's quote check is the same call the save routes make (`spanish.module_for(...).check_excerpt`, review.py:300 and :451). No LLM is on this path, and the tests use the fixture backend.

## Questions for Chris

- For F1: should a picked sentence that a hedge qualifies get the hedge added automatically (option a), or keep the refusal and name the hedge in the message (option b)?
- For F2: is a pasted record that starts with `Excerpt: "..."` and has no Date or Source line an expected live input, or out of scope for the prototype?

```json
{"card": "T-108", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit d3e127c (git archive copy, scratchpad T108_verify); app/backend/present.py, tests/unit/test_quote_units.py, tests/e2e/test_change_the_quote.py, tests/e2e/conftest.py; app: archive server on 127.0.0.1:7971 (ZLAYT_DB scratch sqlite, DATA_DIR empty sentinel, LLM_BACKEND=fixture), not :7860; sample and evals/golden case_01..case_09",
 "exercised": [
  "git archive d3e127c copy; second archive copy diff -rq identical (pycache only)",
  ".venv/bin/python -m pytest -q tests/unit on the archive copy: 2077 passed, 4 skipped (artifacts/review-evidence/T-108/unit-run.txt)",
  "pytest tests/unit/test_quote_units.py -v: 13 passed",
  "probe_units.py: 10 cases, 59 records, 150 units through spanish.module_for(...).check_excerpt, alone and with trailing hedge chain (probe-units-output.json)",
  "probe_shapes2.py: synthetic record shapes A-F through ingest.split_records + present.quote_body (probe-shapes-output.txt)",
  "real backend on 127.0.0.1:7971: tests/e2e/test_change_the_quote.py 3 passed; ZLAYT_DB scratch file written, DATA_DIR sentinel empty (e2e-head-run.txt)",
  "single_unit.py: POST /api/cases/{tok}/items/e8/review with unit 0 alone -> 422 invalid_edit EXCERPT_OMITS_QUALIFIER (single-unit-output.txt)",
  "mutant M1 (quote_body returns (0, block)): 13 unit quote tests failed, 3 e2e failed on :7972 (mutant-M1-unit.txt, mutant-M1-e2e.txt)",
  "mutant M2 (present.py:165 if False:): 13 unit quote tests passed (mutant-M2-unit.txt)",
  "pytest --collect-only tests/unit on archive (2081) and on live tree at 1526a1f (2206)",
  "read present.py, sentences.py, grounding.py check_excerpt, spanish_text.py check_excerpt, review.py edit and manual_entry, store.py load_records, ingest.py _excerpt_extent, api.py demo gate, excerpt.js, manual.js, the three test files"
 ],
 "verdict": "changes",
 "scores": {"deterministic_no_llm": 5, "golden_units_clean": 5, "save_route_parity": 3, "edge_shapes_clean": 2, "silent_fallback_honesty": 2, "test_strength": 3, "e2e_real_backend": 4, "evidence_reproducible": 3},
 "findings": [
  {"severity": "major",
   "title": "A sentence that a hedge qualifies cannot be picked alone; the picker never adds the hedge and the unit test helper models a picker that does not exist",
   "evidence": "app/frontend/excerpt.js:35 (pick only moves lo/hi), :38 (text from units[lo].start to units[hi].end); tests/unit/test_quote_units.py:25 docstring and _pick at :24-30; artifacts/review-evidence/T-108/single-unit-output.txt: sample r8 unit 0 alone -> 422 invalid_edit EXCERPT_OMITS_QUALIFIER; probe-units-output.json alone_fail: sample r8 x2, case_08 r2 (3 of 150)",
   "why_it_matters": "The card AC says picking whole sentences yields a valid verbatim quote on sample and case_01..09; it does not for 3 sentences. The green unit test passes only because _pick adds the hedge the UI never adds.",
   "fix": "Either (a) excerpt.js extends a single selection through the trailing hedge run and checks those boxes, or (b) keep the UI, restate the AC and the docstring, and test the UI rule (unit alone -> 422 EXCERPT_OMITS_QUALIFIER; unit plus hedge chain -> 201).",
   "acceptance_test": "For sample r8 unit 0 and case_08 r2 unit 0, the UI-built text is saved (201) under (a) or refused with EXCERPT_OMITS_QUALIFIER under (b). The test submits the UI-built text, not the _pick text, and fails if the picker stops extending."},
  {"severity": "major",
   "title": "quote_body falls back silently to the whole record block; label-only and date-less records leak Excerpt: and header lines into the picker",
   "evidence": "app/backend/present.py:160-163 (try split_records / except Exception: body = block) and :167-168 (block.find(body); return (0, block) on miss); artifacts/review-evidence/T-108/probe-shapes-output.txt: A_excerpt_only units=['Excerpt: \"Pain persists after two weeks.', 'Taking meds daily.\"'], C_source_excerpt units=['Source: Synthetic Clinic', 'Excerpt: \"Pain persists after two weeks.', 'Taking meds daily.\"']; api.py:287-288 demo gate (409 with ENABLE_LIVE unset)",
   "why_it_matters": "The commit's invariant fails silently on a reachable input shape that the golden set does not contain. The broad except and whole-block return turn a split failure into the bug this card fixes, with no status shown. Silent fallback (persona 4.12). Not a blocker: no fact is invented and the save route still checks verbatim. Reachability in live mode is inferred from code; live mode not exercised.",
   "fix": "A record whose body cannot be located yields no units and a visible state (for example record_warning), not the block. Remove the broad except so the split error surfaces. Strip the Excerpt: label and Date:/Source: lines for unsplit records, or classify the record as unsplit with its own state.",
   "acceptance_test": "test_quote_body_cases (tests/unit/test_quote_units.py:80) gains shapes A and C: no unit starts with Excerpt or Source:, no unit contains a double quote; an unsplittable record yields no units plus a reason. The current (0, block) branch must fail it."},
  {"severity": "minor",
   "title": "Removing the label/quote-mark offset branch passes every quote test; header repeating the body gives a wrong offset",
   "evidence": "app/backend/present.py:164-166; artifacts/review-evidence/T-108/mutant-M2-unit.txt: 13 passed with if False: at present.py:165; probe-shapes-output.txt F_header_repeats_body base=69 vs block.find=25",
   "why_it_matters": "The 'at their true offsets' claim is untested for repeated text. Only test_quote_body_cases line 83 touches offsets and its body appears once.",
   "fix": "Add shape F to test_quote_body_cases; assert raw[u.start:u.end] == u.text and u.start inside the excerpt body.",
   "acceptance_test": "Mutant M2 fails the new shape F assertion."},
  {"severity": "minor",
   "title": "Curly quotes survive as wrapper; quote-mark assertions cover the sample only",
   "evidence": "app/backend/ingest.py:63 strips only straight quotes; probe-shapes-output.txt D_curly_quotes units=['“Pain persists after two weeks.', 'Taking meds daily.”']; tests/unit/test_quote_units.py:59-66 and tests/e2e/test_change_the_quote.py:27 and :51 are sample-only; test_quote_units.py:49 checks startswith only",
   "why_it_matters": "The card and brief require no quote marks in units. Word-pasted records keep curly marks. Golden cases are clean today (probe-units-output.json wrapper 0), so this is latent.",
   "fix": "Strip matched curly pairs in the excerpt extent or give the record a state; extend the quote-mark assertion at test_quote_units.py:49 to every case.",
   "acceptance_test": "Shape D yields units with no curly or straight double quote marks, and the line-49 assertion covers case_01..09."},
  {"severity": "minor",
   "title": "The 2110 passed evidence does not reproduce at the cited commit",
   "evidence": "board card T-108 AC evidence 'tests/unit full run 2110 passed'; artifacts/review-evidence/T-108/unit-run.txt: 2077 passed, 4 skipped; pytest --collect-only at d3e127c: 2081 collected; live tree at 1526a1f with 1291 untracked files and uncommitted edits: 2206 collected",
   "why_it_matters": "Evidence must match the commit it cites. The 2110 figure probably comes from a different tree.",
   "fix": "Rerun at d3e127c and name the commit and the pytest tail line in the AC evidence.",
   "acceptance_test": "AC evidence names d3e127c and the tail line that reproduces it."},
  {"severity": "minor",
   "title": "The frontend strips the wrapper again in manual.js, which can hide a backend regression",
   "evidence": "app/frontend/manual.js:14-23 (quotable(rec) drops ===/Date:/Source: lines, the Excerpt: label and a trailing quote from rec.sentences)",
   "why_it_matters": "A backend leak would be hidden in the manual-entry tray, and the rule now lives in two places that can drift.",
   "fix": "The tray takes backend units as they are, and the rule has one copy.",
   "acceptance_test": "A unit fixture with an Excerpt: prefix shown in the tray fails the test."},
  {"severity": "minor",
   "title": "The excerpt-error hidden check in the e2e runs before the save response and passes at once",
   "evidence": "tests/e2e/test_change_the_quote.py:59 expect(excerpt-error).to_be_hidden() right after btn-save-excerpt click; real check is the poll at :60-65",
   "why_it_matters": "A required AC test carries a check that cannot fail at that point. The final assert still protects the outcome.",
   "fix": "Wait for the save response (expect_response) or drop line 59.",
   "acceptance_test": "The spec passes on the fixed build and fails when the picker submit is broken."},
  {"severity": "nit",
   "title": "_pick is misnamed",
   "evidence": "tests/unit/test_quote_units.py:24-30 builds the quote the picker should build",
   "why_it_matters": "Name suggests it mirrors the UI, which F1 shows it does not.",
   "fix": "Rename to _hedge_chain_quote once F1 is decided.",
   "acceptance_test": "None needed beyond F1."}
 ],
 "whats_right": [
  "Units come from the save-route body at absolute offsets: 150 units, zero not-verbatim, out-of-block or wrapper hits on sample and case_01..09; zero pick failures once the trailing hedge is included",
  "Reverting to whole-block units fails all 13 quote unit tests and all 3 real-backend e2e tests (mutant-M1-unit.txt, mutant-M1-e2e.txt)",
  "The picker's quote check is the save routes' own call (spanish.module_for check_excerpt, review.py:300 and :451); no LLM on this path, fixture backend in tests"
 ],
 "questions_for_chris": [
  "F1: should a picked sentence that a hedge qualifies get the hedge added automatically (option a), or keep the refusal and name the hedge in the message (option b)?",
  "F2: is a pasted record that starts with Excerpt: and has no Date or Source line an expected live input, or out of scope for the prototype?"
 ]}
```
