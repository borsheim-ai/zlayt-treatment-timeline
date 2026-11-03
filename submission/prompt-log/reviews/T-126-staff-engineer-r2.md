# T-126 review (round 2) — staff-engineer-reviewer

Scope: commit a44dced (HEAD, confirmed with `git rev-parse --short HEAD` = a44dced), checked on a `git archive HEAD` copy in the scratchpad (`t126r2/a`). Round 1 is `reviews/T-126-staff-engineer.md`.

Verdict: pass. The round-1 major is fixed. `store.export_case` now skips every `state == "rejected"` flag, so no tray flag counts as pending or prints in the notes or the letter. One minor remains (the merge record is incomplete when a lexicon flag pairs with the model flag).

Deterministic results:
- `.venv/bin/python -m pytest tests/unit -q` on the archive: `3126 passed, 4 skipped in 184.47s`. The handoff says 3129; the difference is working-tree-only tests, not a failure.
- `tests/unit/test_t126_filtered_by_rule.py`: 11 tests, all pass.

Round-1 repro (probe1, unchanged script):
- Before: `review.counts.pending` 23, `export_case.pending_count` 24, notes "Items not reviewed: 24", and a PENDING line printed the non-record quote "Discharged from PT after two missed appointments." under record 4.
- Now: `export_case` pending_count 23, notes "Items not reviewed: 23", `f_r4_1` stays in the tray (GROUNDING_EXCERPT_NOT_VERBATIM) and is not in `export_case.flags`. The 23 "- " lines under PENDING ITEMS NOT INCLUDED match the count, and the only "Discharged from PT after two missed appointments." lines are record 6, which does contain it.

Wider probe (probe4): model flags on records 4 and 6 using four quotes that exist nowhere (objective_negative, degenerative_language, prior_condition, scene_facts) plus two verbatim ones.
- Eleven rejected flags in the tray (JUDGE_UNAVAILABLE, LLM_ONLY and FILTERED_BY_RULE, each with GROUNDING_EXCERPT_NOT_VERBATIM; two FILTERED with and without it).
- Before accepting anything and after accepting every live item: UI pending == `export_case.pending_count` (23 and 0). No rejected flag is in `export_case.flags`.
- The marker `ZQ-NV` is absent from the whole `export_case` JSON, `build_export` output and `export_routes.export_payload`.
- Run with the fixture J4 both "disagree" and default; same results.

Mutants (T-126 test file only, 15 mutants, all KILLED): N1 export skip removed, N2 skip only FILTERED (the round-1 bug), N3 skip only JUDGE_UNAVAILABLE, M2 tray keeps filtered, M3 review_view counts filtered, M5 judge rows count filtered, M6 gate counts filtered, M10 `_to_tray` drops other reasons, R1 why loses the not-verbatim note, R2 merge does not record, R3 `ground()` wipes the merge note, R4 and R5 `_note_merged` not called on the two paths, R6 trace step removed, R7 `is_filtered` always False. Round-1 survivors M3-M6 now die in the card's own tests.

Minors from round 1:
- Grounding reason on filtered items: fixed. probe2 gives `['FILTERED_BY_RULE', 'GROUNDING_EXCERPT_NOT_VERBATIM']`, and with an injection tag `INJECTION_SUSPECTED` as well; the `why` says "not word for word".
- Merge trace: recorded (`ladder.code_checks.merged_categories`, trace step `proposals_merged`) but see finding 1.
- api.md: the GET example has `tray_filtered`, and the FILTERED_BY_RULE row covers all tray flags.
- Single marker: `grep FILTERED app` shows one definition (`flag_templates.FILTERED`) and one predicate (`is_filtered`), used in trace.py (2), present.py (2) and flags.py. The remaining literals are `confidence.py:14` (reason-code list) and `why.py:26` (sentence key), which are vocabulary tables, not checks.
- `docs/LLM_VS_CODE.md` rows 11 and 12 still have no D-057 sentence (`grep -c D-057` = 0). The handoff moved it to an open architect card (T-109, in_progress, note at line 60), so I am not filing it again.

## Findings
1. Minor: when a lexicon flag pairs with the model flag, the model's own category is not in the record.
   - `flags.py` `_note_merged` lists only categories other than the first model flag's.
   - probe5 gives `['degenerative_language'] -> category pre_existing, origin both, merged_categories None`, and `['degenerative_language','new_onset'] -> merged_categories ['new_onset']`.
   - The new api.md text says "code keeps one flag and lists the others"; here the first-proposed category is not listed, only the later ones.
   - This is smaller than the round-1 loss. A lexicon flag is the code-confirmed one, and keeping the lexicon category predates this card.
   - Fix: when a lexicon flag pairs, record the model's category in `merged_categories` too, or state in api.md that the list names only the extra categories.

```json
{"card": "T-126", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit a44dced (HEAD); git archive HEAD in scratchpad t126r2/a; reviews/T-126-staff-engineer.md round 1; sample case via FakeCall; memory/contracts/api.md",
 "exercised": ["git rev-parse --short HEAD = a44dced; git show a44dced -- app memory read in full", "pytest tests/unit -q on the archive: 3126 passed, 4 skipped in 184.47s", "round-1 probe1 re-run: pending 23 == export_case pending_count 23, notes 'Items not reviewed: 23', no record-4 non-record quote", "probe4: four non-record quotes across objective_negative/degenerative_language/prior_condition/scene_facts plus verbatim ones; 11 rejected tray flags; before/after accepting every live item; export_case, build_export and export_payload JSON scanned for the marker (absent)", "probe2/probe2b: filtered proposal with non-verbatim quote keeps GROUNDING_EXCERPT_NOT_VERBATIM and INJECTION_SUSPECTED", "probe3/3b/5: same-quote merge, merged_categories, lexicon-paired case", "15 mutants N1-N3, M2, M3, M5, M6, M10, R1-R7 against tests/unit/test_t126_filtered_by_rule.py: all killed", "grep FILTERED/is_filtered across app and evals; read tests/unit/test_t126_filtered_by_rule.py (11 tests); api.md example and reason-code row; docs/LLM_VS_CODE.md grep D-057; board show T-109"],
 "verdict": "pass",
 "scores": {"d057_filter_placement": 5, "no_silent_drop": 4, "tests_pin_behaviour": 5, "contract_docs": 4, "determinism_ids": 5},
 "findings": [
  {"severity": "minor", "title": "merged_categories omits the model's own category when a lexicon flag pairs with it",
   "evidence": "app/backend/flags.py _note_merged: extra = sorted(c for c in lf.get('_merged', []) if c and c != f['category']); probe5 (scratchpad t126r2/probe/probe5.py): ['degenerative_language'] gives (pre_existing, both, None); ['degenerative_language','new_onset'] gives merged_categories ['new_onset'] (degenerative_language not named).",
   "why_it_matters": "api.md and the handoff say the other categories the model proposed for one quote are listed on the kept flag (D-053: nothing proposed is silently lost); on the both path the first one is not.",
   "fix": "In the lexicon-paired path, include the first model flag's category in merged_categories when it differs from the lexicon category, or narrow the api.md sentence to say the list names only the extra categories.",
   "acceptance_test": "A lexicon-paired flag with model categories [degenerative_language, new_onset] yields merged_categories containing both."}
 ],
 "whats_right": ["export_case skips on state == rejected, the one predicate that covers judge-rejected, not-verbatim and rule-filtered flags, and the test builds the export from the stored case", "FT.is_filtered is the single marker predicate and a test pins that no reader carries a literal", "All 15 mutants die in the card's own test file, including the round-1 survivors M3-M6"],
 "questions_for_chris": []}
```
