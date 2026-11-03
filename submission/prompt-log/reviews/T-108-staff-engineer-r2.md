# T-108 review r2 (staff-engineer-reviewer): every quote-picker unit saves alone

Commit a271014 (`fix(backend): every quote-picker unit saves alone ... (T-108 r2)`), which is HEAD. I reviewed a `git archive a271014` copy and a `git clone` checked out at a271014, both in the scratchpad. The live tree has uncommitted edits and no result here depends on it. Model I ran as: claude-haiku-5-5.

**Verdict: pass.** 0 blockers, 0 majors. Round-1 F1 and F2 (both major) are resolved, and F3, F5 and F8 are resolved. Three new minors (N1 to N3) and three r1 minors still open as the brief allows (F4, F6, F7).

## Brief checks

1. **Hedge-qualified sentences are offered as combined units that save alone: yes.** Sample r8 unit 0 is two sentences ("C5-C6 disc protrusion ... narrowing. Findings may represent degenerative change; correlate clinically."). The text the picker submits (raw[start:end]) on a fresh case returns 201 at POST /api/cases/{tok}/records/r8/entry. The bare first sentence returns 422 invalid_edit. case_08 r2 gives the same result (combined unit 201, bare sentence 422). Six combined units in total across the 25 cases (sample 1, case_08 1, case_lib02 2, case_lib03 1, case_lib07 1). The save rule is unchanged: the bare sentence is still refused.
2. **Label-only record: no units and a plain sentences_reason: yes.** `Excerpt: "..."` alone and `Source:` plus `Excerpt:` (no Date) both give `sentences: []` and `sentences_reason` = NO_UNITS_LAYOUT (present.py:159-160, :174-181). `Date:` plus `Excerpt:` still gives two units. Output in artifacts/review-evidence/T-108/r2/probe-r2-output.txt (last three lines).
3. **Invariant over sample, case_01 to case_09 and all 15 library packets: passes.** 25 cases, 180 records, 591 units. Zero not verbatim, zero failing `check_excerpt` on the unit alone, zero failing `grounding.locate`, zero units with quote marks or a Label/Date/Source/=== prefix. Also `tests/unit/test_quote_units.py`: 35 passed.
4. **Removing the combining logic fails a test: yes.** Scratch copy, not committed: `sed -i '' 's/while j + 1 < len(spans) and "EXCERPT_OMITS_QUALIFIER"/while False and "EXCERPT_OMITS_QUALIFIER"/' app/backend/present.py`, then `.venv/bin/python -m pytest -q tests/unit/test_quote_units.py` gives `8 failed, 27 passed`. The failures are the golden case_08, golden sample, sample-route, library lib02, lib03, lib07, `test_hedge_qualified_sentence_is_one_combined_unit` and `test_golden_hedge_qualified_sentences_are_combined`. Output: artifacts/review-evidence/T-108/r2/mutant-M1-nocombine.txt. The handoff says this mutant "fails 4 tests"; the same one-line change gives 8 here (see N1).

**Unit suite, `/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit`:**
- on the archive copy (no .git): `2236 passed, 4 skipped in 161.76s`. Three of the four skips need a .git directory.
- on the clone at a271014 (with .git): `2239 passed, 1 skipped in 163.32s`. This matches the card's AC, so the r1 F5 count now reproduces.
- Output: artifacts/review-evidence/T-108/r2/unit-run-archive-no-git.txt and unit-run-clone-with-git.txt.

## Round-1 findings

- **F1 (major): resolved.** The picker now receives units that save alone, so the test helper that added the hedge (`_pick`) is gone. excerpt.js was not changed in this commit and does not need to be.
- **F2 (major): resolved in quote_body.** The broad except and the whole-block return are removed from present.py (`quote_body`, :164-182). A record whose label cannot be separated gets no units and a reason. Two remainders are carried as N2 and N3.
- **F3 (minor): resolved.** The offset fix (search for the body from the end of the Excerpt label, present.py:179) is now covered. Mutant M2 (`i = block.find(body)` with no start offset) gives `1 failed, 34 passed` in tests/unit/test_quote_units.py, and the failure is `test_units_sit_at_true_offsets_when_source_repeats_the_body`. Output: artifacts/review-evidence/T-108/r2/mutant-M2-find0.txt.
- **F5 (minor): resolved.** The 2239 passed count reproduces at a271014 with .git.
- **F8 (nit): resolved.** `_pick` no longer exists.
- **F4, F6, F7 (minor): still open, as the brief says.** See below.

## New findings

- **N1 (minor).** The sample route test does not check the quote for most units. For each record it posts the first unit, which creates the entry. Later units get "already has an entry" back, and `tests/unit/test_quote_units.py:81-83` accepts that. That check is at review.py:446 and runs before the quote check at review.py:451. Of 28 sample units, only 9 reach the quote check through the route in the test. The other 19 are checked only by the direct `check_excerpt` call in `_check_all_units`. All 28 pass when each is sent to a fresh case (`artifacts/review-evidence/T-108/r2/route_fresh_sample.py`, output route-fresh-sample-output.txt: `{201: 28}`), so the behaviour is right and the evidence is overstated. The AC sentence "sample units also saved through the real entry/edit routes" and the handoff's "no-merge fails 4 tests" (the mutant gives 8) need correcting.
- **N2 (minor).** The plain-words reason is not shown anywhere in the UI. `grep -rn sentences_reason app/frontend` returns no matches. The tray shows only the generic line at app/frontend/manual.js:55 ("This record has no sentences to pick from."). excerpt.js:20 returns silently when a record has fewer than two units. The handoff already lists this as left. The API has the status, but the user does not see the reason.
- **N3 (minor).** The broad fallback in the stored excerpt is still there. `app/backend/store.py:24-25` is `except Exception:` followed by `body = block`. The r1 F2 fix asked for this to be removed, and this commit changes only quote_body. In the shapes I probed `split_records` does not raise, so I saw no wrong result. Any internal exception would still turn the save-check text into the whole block with no status.

## Still open (r1 minors, as the brief allows)

- **F4 (minor).** Curly quotes stay as wrappers. `app/backend/ingest.py:63` strips only straight quotes. One-off run on the archive: `quote_body` on `Date: ...\nSource: ...\nExcerpt: <curly open>Pain persists after two weeks. Taking meds daily.<curly close>` gives units `['<curly open>Pain persists after two weeks.', 'Taking meds daily.<curly close>']` (artifacts/review-evidence/T-108/r2/curly-shape-output.txt). The golden cases are clean, so this is latent.
- **F6 (minor).** `app/frontend/manual.js:14-23` (`quotable`) still removes `===`, `Date:`, `Source:`, the `Excerpt:` label and a trailing quote on the client.
- **F7 (minor).** `tests/e2e/test_change_the_quote.py:59` (`expect(ed.get_by_test_id("excerpt-error")).to_be_hidden()`) still runs right after the save click, so it passes at once.

## Exercised

- `git show a271014 --stat`, `git show a271014 -- app/backend/present.py memory/contracts/api.md tests/unit/test_quote_units.py`; `git rev-parse HEAD` = a271014.
- `git archive a271014` into the scratchpad copy `T108_r2_verify`.
- `.venv/bin/python -m pytest -q tests/unit` on that copy: 2236 passed, 4 skipped.
- `git clone` of the repo, `git checkout --detach a271014`, then `pytest -q tests/unit`: 2239 passed, 1 skipped; `pytest -q tests/unit/test_quote_units.py`: 35 passed.
- `.venv/bin/python -I artifacts/review-evidence/T-108/probe_r2.py <archive>`: 25 cases, 591 units, 0 failures on each of the checks above; route check for sample r8 and case_08 r2 (fresh cases).
- `.venv/bin/python -I artifacts/review-evidence/T-108/r2/route_fresh_sample.py <archive>`: 28 of 28 sample units 201.
- Label-only, Source-plus-Excerpt and Date-plus-Excerpt shapes through `ingest.split_records` and `present.record_view`.
- Scratch mutants M1 (no combining) and M2 (find from 0): run on `tests/unit/test_quote_units.py`.
- Greps: `sentences_reason` in app/frontend; `already has an entry` in review.py and the test; `except Exception` in store.py; manual.js:14-23 and :55; excerpt.js:20; ingest.py:63; test_change_the_quote.py:59.
- Fixture judge: entries created on the route came back `needs_review` with reason JUDGE_UNAVAILABLE, not verified. That is the expected visible state, though the fixture has no recorded answers for those texts.

**Not exercised:** the e2e `test_change_the_quote.py` was not re-run (the card cites 3 passed on :7966). Live mode was not run, so reachability of the label-only shapes rests on code (api.py:116-120 and :287-288 demo gate). No browser run of the tray or excerpt editor. The CLI `python -m app.pipeline` was not run (not in the brief).

**Outside my lens:** the wording of the tray line in N2.

## What is right

- Each unit the picker can offer saves alone: 591 units across 25 cases, zero failures. The bare hedge-qualified sentence is still refused, so the save rule was not weakened.
- Tests catch the regressions: removing the merge fails 8 tests, and dropping the start offset fails the repeated-body test.
- Label-only and Source-plus-Excerpt records now give no units and a plain reason. No LLM is on this path.

```json
{"card": "T-108", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit a271014 (HEAD): app/backend/present.py (quote_body, quote_units, record_view), tests/unit/test_quote_units.py, memory/contracts/api.md; read-only context: app/backend/store.py:23-25, app/backend/review.py:446 and :451, app/backend/ingest.py:63, app/frontend/manual.js:14-23 and :55, app/frontend/excerpt.js:20, tests/e2e/test_change_the_quote.py:59. Checked on a git archive copy and a git clone at a271014 (scratchpad). App URL not used (no server). Sample case, evals/golden case_01..case_09, 15 library packets in evals/library.",
 "exercised": [
  "git show a271014 (stat and per-file diff); git rev-parse HEAD = a271014",
  "git archive a271014 into scratchpad T108_r2_verify; .venv/bin/python -m pytest -q tests/unit: 2236 passed, 4 skipped (artifacts/review-evidence/T-108/r2/unit-run-archive-no-git.txt)",
  "git clone + checkout a271014 (with .git): pytest -q tests/unit: 2239 passed, 1 skipped (unit-run-clone-with-git.txt); pytest -q tests/unit/test_quote_units.py: 35 passed",
  "artifacts/review-evidence/T-108/probe_r2.py (python -I): 25 cases, 180 records, 591 units; 0 not verbatim, 0 alone check failures, 0 grounding.locate failures, 0 wrapper hits; 6 combined units (probe-r2-output.txt)",
  "route: sample r8 unit 0 picked text on a fresh case -> 201; bare first sentence -> 422 invalid_edit; case_08 r2 the same (probe-r2-output.txt)",
  "artifacts/review-evidence/T-108/r2/route_fresh_sample.py (python -I): 28 of 28 sample units -> 201 on fresh cases (route-fresh-sample-output.txt)",
  "label-only, Source-plus-Excerpt, Date-plus-Excerpt shapes through ingest.split_records and present.record_view: [] + sentences_reason; [] + sentences_reason; 2 units",
  "mutant M1 (scratch copy): while False and at present.py:194: pytest tests/unit/test_quote_units.py -> 8 failed, 27 passed (mutant-M1-nocombine.txt)",
  "mutant M2 (scratch copy): find(body) without the label start: pytest tests/unit/test_quote_units.py -> 1 failed, 34 passed (mutant-M2-find0.txt)",
  "greps: sentences_reason in app/frontend (0 matches); already has an entry (review.py:446, test :83); except Exception (store.py:24); manual.js:55; excerpt.js:20; ingest.py:63; test_change_the_quote.py:59",
  "one-off -I run: curly-quote shape gives units with curly marks at both ends (curly-shape-output.txt)"
 ],
 "verdict": "pass",
 "scores": {"deterministic_no_llm": 5, "golden_units_clean": 5, "save_route_parity": 4, "edge_shapes_clean": 4, "silent_fallback_honesty": 3, "test_strength": 4, "evidence_reproducible": 5},
 "findings": [
  {"severity": "minor",
   "title": "N1: the sample route test checks the quote for 9 of 28 units; the rest pass on the duplicate-entry branch, and the card overstates route coverage and the mutant count",
   "evidence": "tests/unit/test_quote_units.py:81-83 (assert r.status_code == 201 or 'already has an entry' in r.text); app/backend/review.py:446 raises the duplicate error before app/backend/review.py:451 runs check_excerpt; artifacts/review-evidence/T-108/r2/route-fresh-sample-output.txt: status counts {201: 28} on fresh cases; handoff text 'no-merge fails 4 tests' vs mutant-M1-nocombine.txt '8 failed, 27 passed'",
   "why_it_matters": "The behaviour is correct (28 of 28 save on fresh cases), but the test does not show it for 19 units. A later regression in the route's quote check would pass the sample route test. The AC evidence sentence claims more than the test checks.",
   "fix": "In the sample test, submit each unit to the route on a fresh case (or assert that the duplicate response carries no quote-level reason). Correct the AC evidence sentence and the mutant count in the handoff.",
   "acceptance_test": "A fresh-case test over all sample units asserts 201 for each. Removing the check_excerpt call in review.manual_entry (review.py:451) makes that test fail."},
  {"severity": "minor",
   "title": "N2: sentences_reason is not rendered; the tray shows only a generic line",
   "evidence": "grep -rn sentences_reason app/frontend returns no matches; app/frontend/manual.js:55 shows 'This record has no sentences to pick from.'; app/frontend/excerpt.js:20 returns with no message when a record has fewer than two units; handoff lists this as left",
   "why_it_matters": "The backend status exists, but the reviewer and the paralegal never see why no picker is offered. The card's visible-state requirement from r1 F2 is only partly met.",
   "fix": "Render sentences_reason in the tray (manual.js) and in the excerpt editor when sentences is empty.",
   "acceptance_test": "For a record view with sentences [] and a sentences_reason, the tray shows that text (a DOM test or an e2e spec on a label-only input in live mode). Removing the render fails the test."},
  {"severity": "minor",
   "title": "N3: the broad except in store.load_records still turns any split error into the whole block",
   "evidence": "app/backend/store.py:23-25: try: body = ingest.split_records(block)[0]['excerpt'] / except Exception: / body = block; r1 F2 asked for this to be removed and commit a271014 changes only quote_body",
   "why_it_matters": "Any internal exception during the stored-excerpt split silently becomes the whole block, and the save check then runs against header text. No invented fact results (the quote is still verbatim), and the probed shapes do not raise, so I saw no wrong output. It is still the swallow the r1 finding named.",
   "fix": "Remove the try/except in store.load_records, or catch only ingest.IngestError and give that record a visible state.",
   "acceptance_test": "Monkeypatch ingest.split_records to raise RuntimeError: load_records raises instead of returning the block."},
  {"severity": "minor",
   "title": "F4 (r1, still open): curly quotes survive as wrappers in units",
   "evidence": "app/backend/ingest.py:63 strips only straight quotes; artifacts/review-evidence/T-108/r2/curly-shape-output.txt: units ['<curly open>Pain persists after two weeks.', 'Taking meds daily.<curly close>']",
   "why_it_matters": "The card requires no quote marks in units. Golden cases are clean, so this is latent for pasted text with curly quotes.",
   "fix": "Strip matched curly pairs in the excerpt extent, or give the record a state. Extend the quote-mark assertion in test_every_offered_unit_saves_alone_golden to every case.",
   "acceptance_test": "The curly shape yields units with no curly or straight double quote marks."},
  {"severity": "minor",
   "title": "F6 (r1, still open): manual.js strips the wrapper again on the client",
   "evidence": "app/frontend/manual.js:14-23 (quotable): removes === / Date: / Source: lines, the Excerpt: label and a trailing quote from rec.sentences",
   "why_it_matters": "A backend leak would be hidden in the tray, and the rule lives in two places that can drift.",
   "fix": "The tray takes backend units as they are; keep one copy of the rule.",
   "acceptance_test": "A unit fixture with an Excerpt: prefix shown in the tray fails the test."},
  {"severity": "minor",
   "title": "F7 (r1, still open): the excerpt-error hidden check runs before the save response",
   "evidence": "tests/e2e/test_change_the_quote.py:59 expect(ed.get_by_test_id('excerpt-error')).to_be_hidden() runs right after the btn-save-excerpt click",
   "why_it_matters": "The check passes at once, so it proves nothing. The final assertion still protects the outcome.",
   "fix": "Wait for the save response (expect_response), or drop line 59.",
   "acceptance_test": "The spec passes on the fixed build and fails when the picker submit is broken."}
 ],
 "whats_right": [
  "Every unit the picker can offer saves alone: 591 units over 25 cases, zero alone or grounding failures; the bare hedge-qualified sentence is still refused, so the rule was not weakened",
  "The tests catch the regressions: removing the merge fails 8 tests, and dropping the start offset fails the repeated-body test",
  "Label-only and Source-plus-Excerpt records give no units and a plain sentences_reason; no LLM is on this path"
 ],
 "questions_for_chris": []}
```
