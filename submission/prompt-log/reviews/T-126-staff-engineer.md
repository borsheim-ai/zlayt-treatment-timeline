# T-126 review (round 1) — staff-engineer-reviewer

Scope: commit 6d01774 (D-057, rule-filtered model flags), checked on a `git archive` copy of c559ce2 (card files unchanged at HEAD f7829c1; the later diff touches only an unrelated `gap_changes_removed` key). Exercised: full unit suite, the 5 new tests, ten mutants, three probes, code-path grep, api.md.

Verdict: changes. The feature works: the filtered proposals are listed, collapsed and counted with the rule named (D-032), and they stay out of flags, queue, counts, gate and the letter. One major remains. A rejected tray flag of any other kind still leaks into the export notes and the pending count, which the contract says it must not (api.md, D-053). The card narrowed its exclusion to `FILTERED_BY_RULE` instead of all rejected flags.

Deterministic results (archive of c559ce2, `.venv/bin/python -m pytest tests/unit -q`): `2939 passed, 4 skipped in 191.40s`.

Mutants (T-126 test file plus `test_flags_pass.py`):
- Killed: M1 (merge drops filtered again), M2 (tray keeps filtered), M7 (filtered not last), M8 (`collapsed` False), M9 (dedupe key without category), M10 (reasons not set).
- Survived in the card's own tests: M3 (`review_view` counts filtered), M4 (`export_case` includes filtered), M5 (trace judge rows count filtered), M6 (trace gate counts filtered).
- Whole suite: M3-M6 are killed, but only by incidental tests (`test_trace.py`, `test_lib09_t110*.py`), not by anything that names D-057.

## Findings
1. **Major: other rejected tray flags still count as pending and print in the internal notes.**
   - Repro: `probe/probe1.py` runs the sample case with a model flag on record 4 whose quote is not in the record.
   - `review.counts.pending` is 23. `store.export_case` returns `pending_count 24` because `f_r4_1` (state `rejected`, review_status `pending`) is in `flags`.
   - The notes say "Items not reviewed: 24" and "PENDING ITEMS NOT INCLUDED" lists `Flag, Causation language: record 4 ... "Discharged from PT after two missed appointments."`, a quote that is not in record 4.
   - api.md D-053 says a tray flag "is never in `flags`, `review.queue` or the export". The card added the skip at `store.py:69` for `FILTERED_BY_RULE` only; the same bug exists for `JUDGE_DISAGREES`, `LLM_ONLY` and grounding-rejected flags.
2. **Minor: the FILTERED branch of `_to_tray` discards the other reasons.**
   - `flags.py:~346` sets `reasons=[FILTERED]` and returns early. A non-verbatim model quote loses `GROUNDING_EXCERPT_NOT_VERBATIM` (probe2: `reasons ['FILTERED_BY_RULE']`, `excerpt_verbatim False`), and `INJECTION_SUSPECTED` is likely lost too.
   - The quote then shows in `tray_filtered` as "the AI's proposal" with no mark that it is not in the record.
   - The comment at `flags.py:~253` ("a rung-1 failure keeps its own reason") is no longer true for this path.
3. **Minor: the card's tests do not pin the exclusions they claim.**
   - The letter assertion in `test_case_payload_has_a_collapsed_counted_group...` builds the export from an empty case (`{"records": [], "entries": [], ...}`), so it passes whatever the code does.
   - Nothing in the T-126 file asserts `review.counts`, the trace gate or judge counts, or `export_case`. Mutants M3-M6 survive it.
   - Fix: assert `counts.rejected`, `pending_count`, `case_trace` `gate` and `judges` counts and `export_case(...)["flags"]` with and without the filtered item on the stored case.
4. **Minor: two model proposals for the same quote collapse into one without a trace.**
   - The dedupe key in `merge` (`flags.py:~122`) is `(type, excerpt)` with no category (probe3: prior_condition and degenerative_language on one quote gives one `pre_existing` flag).
   - D-053 says nothing the model proposes is silently dropped. At minimum, record the collapsed category in the audit. Same-category duplicates collapsing is fine.
5. **Minor: docs are only partly updated.**
   - The api.md paragraph and the reason-code row are good, but the GET example JSON has no `tray_filtered` key (`api.md:232-250`).
   - `docs/LLM_VS_CODE.md` rows 11 and 12 describe D-053 and say nothing about D-057 or rule-filtered proposals (architect-owned, so this needs a card).
6. **Nit: the rule marker is copied as a literal.**
   - `[:1] == ["FILTERED_BY_RULE"]` appears in `store.py`, `trace.py` (twice) and `present.py`. Add one helper, `is_filtered(row)`, next to `FT.FILTERED`.
   - `api.py:407` run-progress `counts.flags` counts tray and filtered rows. It is a progress counter and not a "needs review" count, so low value.

Right: (a) the filtered id order is protected, with filtered items placed last so recorded judge prompts keep their ids (test 2 plus mutant M7); (b) a per-item dedupe key that includes the category; (c) the contract paragraph and the reason-code row are specific.

```json
{"card": "T-126", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 6d01774 (D-057 filtered-by-rule tray group); git archive of c559ce2 in scratchpad t126r1/a (card files same at HEAD f7829c1); memory/contracts/api.md; sample case via FakeCall",
 "exercised": ["pytest tests/unit on git archive of c559ce2: 2939 passed, 4 skipped", "read git show 6d01774 in full (flags, present, store, trace, why, confidence, flag_templates, api.md, tests)", "10 mutants M1-M10 against the T-126 test file plus test_flags_pass (M3-M6 survive; M3-M6 each killed only by incidental tests in the full suite: test_trace.py, test_lib09_t110.py, test_lib09_t110_r2.py)", "probe1: sample case with a model flag on record 4 plus an objective_negative flag; case_view, store.export_case, build_export notes", "probe2: filtered proposal with non-verbatim quote (reasons lose GROUNDING_EXCERPT_NOT_VERBATIM)", "probe3: two model proposals, same quote, different category (collapse to one flag)", "grep of list_items, rejected, flag readers in app/backend, evals/run.py tray handling, api.py progress counts, pipeline finalize", "read memory/contracts/api.md and docs/LLM_VS_CODE.md for D-057"],
 "verdict": "changes",
 "scores": {"d057_filter_placement": 4, "no_silent_drop": 3, "tests_pin_behaviour": 3, "contract_docs": 4, "determinism_ids": 5},
 "findings": [
  {"severity": "major", "title": "Rejected tray flags other than FILTERED_BY_RULE are still counted as pending and printed in the export notes",
   "evidence": "probe1 (scratchpad t126r1/probe/probe1.py) on archive: review.counts.pending 23 but export_case pending_count 24; flags list contains f_r4_1 state rejected, review_status pending; internal_notes_text 'Items not reviewed: 24' and PENDING ITEMS NOT INCLUDED lists 'Flag, Causation language: record 4 ... \"Discharged from PT after two missed appointments.\"' (quote not in record 4). store.py:69 skips only FILTERED_BY_RULE; api.md D-053: tray flag 'is never in flags, review.queue or the export'.",
   "why_it_matters": "D-053 tray items must not be review work or export content; the notes count disagrees with the UI and print a non-verbatim quote. The card touched this exact loop and chose the narrow predicate.",
   "fix": "In store.export_case skip every flag with state == 'rejected' (and keep the filtered skip only as a subset); same for trace allitems/judge rows if any other rejected flag is counted as pending.",
   "acceptance_test": "Run a case with a J4-disagree model-only flag and a grounding-rejected model flag; assert export_case flags exclude both, pending_count == review.counts.pending, and the notes pending list has no flag line for them."},
  {"severity": "minor", "title": "FILTERED branch of _to_tray drops other reasons (grounding failure, injection)",
   "evidence": "flags.py _to_tray: 'if code == FILTERED: ... f[\"reasons\"] = [FILTERED]; return'. probe2: filtered proposal with a quote not in the record shows reasons ['FILTERED_BY_RULE'], ladder.code_checks.excerpt_verbatim False. Comment in run_flag_pass says a rung-1 failure keeps its own reason.",
   "why_it_matters": "The tray_filtered group then shows a quote that is not in the record with no marker, and the audit loses why the ladder would have rejected it.",
   "fix": "Keep reasons = [FILTERED] + the rung-1 and injection reasons (as the LLM_ONLY branch does), and render a 'not found in the record' note for such items.",
   "acceptance_test": "Unit test: objective_negative proposal with a non-verbatim quote gives reasons[0] FILTERED_BY_RULE and GROUNDING_EXCERPT_NOT_VERBATIM in reasons."},
  {"severity": "minor", "title": "T-126 tests do not pin counts, gate or export exclusions; the letter assertion is vacuous",
   "evidence": "tests/unit/test_t126_filtered_by_rule.py: 'case = {\"records\": [], \"entries\": [], \"amounts\": [], \"flags\": []}; assert \"Plan of care: 12 visits.\" not in export.build_export(case)[\"letter_text\"]' passes for any code. Mutants M3 (present.py review_view), M4 (store.py:69), M5 (trace.py:751), M6 (trace.py:901) all survive test_t126_filtered_by_rule.py plus test_flags_pass.py.",
   "why_it_matters": "AC says not in counts, gate or letter; those guarantees ride on unrelated tests and would regress silently if those tests change.",
   "fix": "Add assertions on review.counts.rejected, case_trace gate/judges counts, and store.export_case flags/pending_count for the stored case with a filtered item; build the export from export_case, not an empty dict.",
   "acceptance_test": "Mutants M3-M6 each make a T-126 test fail."},
  {"severity": "minor", "title": "Model proposals with the same quote and different category collapse silently in merge",
   "evidence": "flags.py merge dedupe key k = (lf['type'], grounding.normalize(lf['excerpt'])) (no category). probe3: prior_condition and degenerative_language on one quote give one flag ('pre_existing','both','needs_review'); the second category is not recorded anywhere.",
   "why_it_matters": "D-053/D-057 say nothing the model proposes is silently dropped; the filtered path keys on category, the main path does not.",
   "fix": "Record collapsed categories in the kept flag's ladder/audit (or keep both when categories differ).",
   "acceptance_test": "Two proposals, same quote, different category: output carries both categories or a ladder note naming the second."},
  {"severity": "minor", "title": "Docs partly updated: api.md example lacks tray_filtered; LLM_VS_CODE rows 11/12 do not mention D-057",
   "evidence": "memory/contracts/api.md:232-250 example has 'tray' but no 'tray_filtered'; docs/LLM_VS_CODE.md row 11 and row 12 cover D-053 only; grep D-057 docs/*.md returns nothing.",
   "why_it_matters": "The frontend and graders read the example and the table; the table is the graded LLM/code boundary.",
   "fix": "Add tray_filtered to the example JSON; open an architect card to add one sentence on rule-filtered proposals to rows 11-12.",
   "acceptance_test": "grep tray_filtered in the api.md example block and D-057 in docs/LLM_VS_CODE.md both match."},
  {"severity": "nit", "title": "FILTERED_BY_RULE marker repeated as string literals; progress counter includes tray rows",
   "evidence": "store.py:69, trace.py:752, trace.py:901 each test [:1] == ['FILTERED_BY_RULE'], present.py uses FT.FILTERED; api.py:407 counts.flags = len(list_items flag).",
   "why_it_matters": "A fourth reader that forgets the check is how the first review missed three counters.",
   "fix": "One is_filtered(row) helper beside FT.FILTERED; optional: exclude rejected rows from the progress count.",
   "acceptance_test": "grep FILTERED_BY_RULE app/backend shows one literal definition."}
 ],
 "whats_right": ["Filtered items are placed after every other tray item so recorded judge prompts keep their f_r<n>_<k> ids (test plus mutant M7 kill)", "tray_filtered carries rule, ref D-032, label, explanation and count per rule, with needs_action false, and the full unit suite stays green (2939 passed)", "api.md documents the payload and adds a FILTERED_BY_RULE reason-code row"],
 "questions_for_chris": []}
```
