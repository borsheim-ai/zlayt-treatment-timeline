# T-072 round 3: claims-adjuster-reviewer (D-040 follow-through, commit 72bf940)

**Verdict: fail** (one blocker, one major, two minors).

The brief's three literal checks mostly pass. The word "self-report" is gone from user-facing text, the frontend and backend guard tests pass, and each planted "self-report" or "patient statement" string makes the matching guard fail. But the reworded reasons still name the patient as the speaker of the quoted text ("an attribution such as 'patient states'"), which is the D-040 label in a new form. The new backend guard does not cover that wording, and the frontend guard was not widened (the r2 F3 fix asked for both).

Model: claude-haiku-5-5 (the running model). Scope: commit 72bf940 read through `git archive` into the scratchpad (`t072r3`); the live tree agrees for why.py, narrative.py and both guard tests. No browser run.

## Brief checks

1. **why.py and narrative.py name no speaker (fail on substance, pass on wording).** Both now read "an attribution such as 'patient states'" (why.py:7, narrative.py:19). That is the wording the triage asked for. It still names the speaker in a user-facing per-item reason (F1).
2. **No user-facing "self-report" in app/ (pass).** `git grep -n -i -P 'self[-\s]?report' 72bf940 -- app/` returns: narrative.py:4 (module docstring), grounding.py:58 (comment), review.css:27 and review.js:276 (internal class `rv-selfreport`), and app/llm/lexicon.yaml comment and metadata lines (26, 86, 90, 496, 764). No code reads the lexicon `rationale`, `false_positive` or `note` fields (`git grep` in app/*.py returns no hits; app/backend/lexicon.py:12-24 exposes only `code_list` and `load`, and no route returns them). None is user-facing.
3. **Both guard tests pass (pass).** `5 passed` at the commit archive and on the live tree.
4. **Each guard fails when the string is planted (partial).** Results in section "Plant results" below. Backend "self-report" and "a patient statement" fail (good). Frontend "self-report" fails (good). Frontend "a patient statement" passes (F2). Backend "patient states" passes (F2).

## Plant results (scratch copies of the archive, string appended with python3)

| Copy | File | Planted text | Result |
|---|---|---|---|
| p1 | app/backend/why.py | `PLANT_P1 = "Patient self-report"` | backend guard FAILS (`why.py:71`); exit 1 |
| p2 | app/backend/narrative.py | `PLANT_P2 = "a patient statement"` | backend guard FAILS (`narrative.py:162`); exit 1 |
| p3 | app/backend/why.py | `PLANT_P3 = "an attribution such as patient states"` | 5 passed, exit 0 (gap) |
| p4 | app/frontend/mock_flags.js | `// PLANT_P4 Patient self-report` | frontend guard FAILS (`mock_flags.js:57`); exit 1 |
| p5 | app/frontend/mock_flags.js | `// PLANT_P5 a patient statement` | 5 passed, exit 0 (gap) |
| p6 | app/frontend/review.js | `// PLANT_P6 self-reported` | frontend guard FAILS (`review.js:282`); exit 1 |

## Findings

- **F1 blocker. The reason sentences still name the patient as the speaker.** `app/backend/why.py:7` at 72bf940: `"SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, an attribution such as 'patient states', a negation, a side or an approximation) that the summary leaves out."` `app/backend/narrative.py:19`: `"SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, attribution such as 'patient states' or negation that the cited quote has."` Both are user-facing: `app/frontend/timeline.js:119` renders `it.why` as `data-testid="why-text"` in the Why? modal, and `app/frontend/narrative.js:55` renders `r.message` for each removed sentence. The sentence is per item ("the quoted text carries ... 'patient states'"), so the paralegal reads that this quote carries a patient-speaker attribution. That is the label D-040 cuts. D-040 (memory/ORCHESTRATOR_DECISIONS.md:48): "No code or model labels who is speaking." It also says the verbatim excerpt is where "Patient states..." belongs. The r2 blocker (F1) was this same sentence with "a patient statement". Changing the example to "patient states" keeps the speaker label. The triage's reading (a generic rule, not a label on an excerpt) is arguable, but the string is per-item and user-facing. I am holding the r2 reading. See the question for Chris.
- **F2 major. The guard does not cover the wording it was added to guard (r2 F3 only partly closed).** The backend BAD pattern (`tests/unit/test_backend_no_speaker_label.py:13`) is `self[-\s]?report|patient\s+statement|patient\s+self`. It does not match "patient states", so p3 passes with the exact phrase now in why.py:7. The frontend guard was not widened (`tests/unit/test_frontend_no_speaker_label.py:9`: `BAD = re.compile(r"self[-\s]?report", re.I)`), so p5 passes. The r2 F3 fix text asked for the patient-speaker words in both scans. The r2 acceptance test (planted backend strings fail) is met. Fix must not add a bare "patient states" to the frontend pattern: mock data holds record excerpts with "Patient states ..." that D-040 allows (`app/frontend/dev/mock-data.js:415`, `:754`; `app/frontend/mock_flags.js:25`).
- **F3 minor (carried from r2 F4). Golden K3 summary still carries the cut label.** `evals/golden/sample.expected.json:625` at 72bf940: `"summary": "Causation rests on patient self-report, not a physician's causation opinion."` It is qa-owned and not rendered, so minor. `evals/golden/check_golden.py:491` also has an evaluator message "drops the self-report attribution" (not user-facing).
- **F4 minor (carried from r1 F2 and r2 F5). The internal id `patient_report` is in API data.** `app/backend/present.py:74`: `"category": row["category"]` in `flag_view`; `app/frontend/flags.js:65`: `"data-category": f.category`. Not rendered as text. The card's "never shown to users" is inaccurate. `app/llm/prompts/flags_v1.md:13` also defines the category as "the patient's own statement" (model-facing prompt text, not user-facing). Nothing in this round changed these lines.

## Reproduction

```
git archive 72bf940 | tar -x -C <scratchpad>/t072r3
cd <scratchpad>/t072r3 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_backend_no_speaker_label.py tests/unit/test_frontend_no_speaker_label.py -v
  -> 5 passed in 0.12s
/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit
  -> 957 passed in 19.18s
(plants p1 to p6 as in the table, each in a fresh cp -R copy)
git grep -n -i -P 'self[-\s]?report' 72bf940 -- app/      -> only the allowed hits listed in brief check 2
git grep -n -i -E 'patient (statement|states|self)' 72bf940 -- app/ -> why.py:7, narrative.py:19, and verbatim record excerpts in app/frontend (mock.js:15, mock-data.js:412, :415, :749, :754, mock_flags.js:24, :25)
```

## Not run

- Browser render of `?api=mock` (no UI check of the Why? modal).
- `evals.run` (writes `evals/reports/`, outside my write paths).
- I did not read the r1 review file this round; the carried items come from the r2 file and the card notes.

```json
{"card": "T-072", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 3; commit 72bf940 read via git archive into the scratchpad (t072r3); live tree checked for why.py, narrative.py and the two guard tests; app/ grep via git grep at 72bf940; sample case Appendix A (golden K3 and flag payloads read, no browser run)",
 "exercised": [
  "read personas/claims-adjuster.md in full; read reviews/T-072-claims-adjuster-r2.md in full; read memory/ORCHESTRATOR_DECISIONS.md D-040 (line 48) and D-022 (line 30)",
  "python3 tools/board.py show T-072 (status in_review, rounds 2, commits include 72bf940; triage note 2026-11-02T02:59:27Z)",
  "git status --short; git show --stat 72bf940; git merge-base --is-ancestor 72bf940 HEAD (ancestor); git rev-parse --short HEAD -> 72bf940",
  "git show 72bf940:app/backend/why.py (lines 1-20, line 7 read); git show 72bf940:app/backend/narrative.py (lines 1-30, 110-125; line 19 and 62 read)",
  "git grep -n -i -P 'self[-\\s]?report' 72bf940 -- app/ (exit 0; hit list as in brief check 2)",
  "git grep -n -i -E 'patient (statement|states|self)' 72bf940 -- app/",
  "git grep -n -E 'rationale|false_positive|note' 72bf940 -- 'app/*.py' (no lexicon metadata reads); app/backend/lexicon.py read (lines 1-24)",
  "git grep -n -E 'carries a qualifier|drops a hedge' 72bf940 -- evals tests (no fixture or golden pins the old reason text)",
  "git grep -n -i 'self-report' 72bf940 -- evals spec memory/ORCHESTRATOR_DECISIONS.md (sample.expected.json:625 and :990; check_golden.py:21, :491, :543)",
  "git show 72bf940:app/backend/present.py (lines 72-76); git show 72bf940:app/frontend/flags.js (lines 63-68); timeline.js:117-120; narrative.js:53-56",
  "git archive 72bf940 | tar -x -C <scratchpad>/t072r3; cd there; .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_backend_no_speaker_label.py tests/unit/test_frontend_no_speaker_label.py -v -> 5 passed, exit 0",
  "read tests/unit/test_backend_no_speaker_label.py (75 lines) and tests/unit/test_frontend_no_speaker_label.py (23 lines) at 72bf940",
  "scratch copies (cp -R of the archive): p1 why.py 'Patient self-report' -> backend guard fails exit 1; p2 narrative.py 'a patient statement' -> backend guard fails exit 1; p3 why.py 'an attribution such as patient states' -> 5 passed exit 0; p4 mock_flags.js '// Patient self-report' -> frontend guard fails exit 1; p5 mock_flags.js '// a patient statement' -> 5 passed exit 0; p6 review.js '// self-reported' -> frontend guard fails exit 1",
  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit in the archive -> 957 passed in 19.18s",
  "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_backend_no_speaker_label.py tests/unit/test_frontend_no_speaker_label.py in the live tree -> 5 passed"
 ],
 "verdict": "fail",
 "scores": {"d040_reason_strings_no_speaker": 2, "d040_user_facing_grep_clean": 4, "guard_coverage_matches_wording": 2, "export_golden_fidelity": 3, "no_invented_facts_or_severity": 5, "tests_green_at_commit": 5},
 "findings": [
  {"severity": "blocker",
   "title": "Why? and removed-sentence reasons still name the patient as the speaker ('an attribution such as patient states') (D-040)",
   "evidence": "app/backend/why.py:7 at 72bf940: 'SUMMARY_DROPS_QUALIFIER': 'The quoted text carries a qualifier (a hedge, an attribution such as patient states, a negation, a side or an approximation) that the summary leaves out.' app/backend/narrative.py:19: 'The sentence drops a hedge, attribution such as patient states or negation that the cited quote has.' Rendered: app/frontend/timeline.js:119 (data-testid why-text, Why? modal) and app/frontend/narrative.js:55 (r.message). Reachable via app/backend/generator.py:108, pipeline.py:66, review.py:76.",
   "why_it_matters": "memory/ORCHESTRATOR_DECISIONS.md D-040 (line 48): 'No code or model labels who is speaking.' The sentence is per item and says the quoted text carries a patient-speaker attribution, which is the speaker label D-040 cut. The r2 blocker F1 was the same sentence with 'a patient statement'; renaming the example to 'patient states' keeps the label. The brief's wording check passes, but the D-040 substance does not. If Chris reads D-040 as chip-only, this drops to major (see questions_for_chris).",
   "fix": "Backend owner: delete the speaker example. why.py:7 -> 'The quoted text carries a qualifier (a hedge, a negation, a side or an approximation) that the summary leaves out.' narrative.py:19 -> 'The sentence drops a hedge or a negation that the cited quote has.' Keep the qualifier check at app/backend/grounding.py:186 unchanged; change text only.",
   "acceptance_test": "git grep -n -i -E 'patient (states|statement|self)|self[- ]?report' -- app/backend returns only docstrings and comments (narrative.py:4, grounding.py:58 are allowed). In a scratch copy, planting 'an attribution such as patient states' in app/backend/why.py makes the backend guard fail (p3 passes today)."},
  {"severity": "major",
   "title": "Guard does not cover the wording it guards; frontend guard not widened (r2 F3 only partly closed)",
   "evidence": "tests/unit/test_backend_no_speaker_label.py:13 BAD = 'self[-\\s]?report|patient\\s+statement|patient\\s+self' (no 'patient states'): plant p3 (why.py 'an attribution such as patient states') -> 5 passed, exit 0. tests/unit/test_frontend_no_speaker_label.py:9 BAD = 'self[-\\s]?report' only: plant p5 (mock_flags.js '// a patient statement') -> 5 passed, exit 0. r2 F3 fix asked for the patient-speaker words in both scans.",
   "why_it_matters": "The guard passes on the exact phrase that now sits in why.py:7 and narrative.py:19, so a regression of this label would not fail CI. The frontend scan has the same gap for 'patient statement' and 'patient self'. The r2 acceptance test (backend planted strings fail) is met; the frontend half of the fix is not.",
   "fix": "QA owner (tests/**): backend BAD add 'patient\\s+states'. Frontend BAD add 'patient\\s+(statement|self)' only, and do NOT add bare 'patient states': app/frontend/dev/mock-data.js:415 and :754 and app/frontend/mock_flags.js:25 hold verbatim record excerpts 'Patient states ...' that D-040 allows. Keep the rv-selfreport allowance.",
   "acceptance_test": "Scratch copies: planting 'patient states' in app/backend/why.py fails the backend guard; planting 'a patient statement' in app/frontend/mock_flags.js fails the frontend guard; both guards still pass on the fixed tree (mock-data.js verbatim excerpts unchanged)."},
  {"severity": "minor",
   "title": "Golden K3 summary still carries the cut label (carried from r2 F4)",
   "evidence": "evals/golden/sample.expected.json:625 at 72bf940: 'summary': 'Causation rests on patient self-report, not a physician's causation opinion.' evaluator message evals/golden/check_golden.py:491 'drops the self-report attribution' (not user-facing).",
   "why_it_matters": "The golden JSON is the expected-output authority and still states the speaker label D-040 cut. Not rendered, so minor. Outside app/, so outside the brief's grep, but it is the same residue.",
   "fix": "QA owner (evals/**): replace the summary with a neutral line that quotes record 9, e.g. 'Causation language: record 9 verbatim \"Patient states symptoms began after the January collision.\"'. Re-run the evals before merging; keep eval gates unchanged.",
   "acceptance_test": "git grep -n -i 'self-report' -- evals/golden/sample.expected.json returns only the must_not statement at line 990, or nothing."},
  {"severity": "minor",
   "title": "The internal id 'patient_report' is public API data (carried from r1 F2 and r2 F5)",
   "evidence": "app/backend/present.py:74 at 72bf940: '\"category\": row[\"category\"]' in flag_view; app/frontend/flags.js:65: 'data-category': f.category. Text uses f.title (flags.js:66). app/llm/prompts/flags_v1.md:13 defines the id as 'the patient's own statement' (model-facing).",
   "why_it_matters": "Not rendered as text, so not a D-040 wording violation. But the card's 'never shown to users' is inaccurate: an adjuster inspecting the payload sees the id, and the card and decision note should say so.",
   "fix": "Backend owner: correct the card and decision note to 'not rendered as text; present in API JSON and data-category', or map to a neutral public id at present.py:74 and flags.js:65.",
   "acceptance_test": "Option (a): card and decision note state the exposure. Option (b): GET a sample case flags payload and assert no category or data-category value contains 'patient'."}
 ],
 "whats_right": [
  "No user-facing 'self-report' remains in app/: the only hits are a docstring, comments, the internal class rv-selfreport and lexicon.yaml comment and metadata lines that no code reads.",
  "The backend guard is AST-based and skips docstrings and comments, so narrative.py:4 does not trip it; it fails on planted 'Patient self-report' in why.py and 'a patient statement' in narrative.py.",
  "The full unit suite passes at the commit (957 passed) and the export and golden text is unchanged by this commit."
 ],
 "questions_for_chris": [
  "Does D-040 ('No code or model labels who is speaking') cover per-item Why? and removed-sentence reason text, or only the chip and the excerpt label? My reading is that it covers the reason text, so F1 is a blocker. If you read it as chip-only, F1 drops to major and the verdict becomes changes."
 ]}
```
