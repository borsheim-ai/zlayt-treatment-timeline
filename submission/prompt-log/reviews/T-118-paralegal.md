# T-118 review — paralegal-reviewer (lib11 golden edits, commit 78450f6)

**Verdict: changes.** No blockers. Two majors, one minor.

The five edits are exactly the five the T-116 card note posted, and the commit changes nothing else in the truth file. `validate_library.py` and `check_golden.py` pass on the HEAD copy. The product's gap endpoints match the expected record lists for all 25 golden and library packets, and record 6 is excluded as an intake form. Three problems remain. The truth file now says record 6 is a `phone_note`, which the packet does not state. Nothing in the repo compares record lists, so reverting the lib11 endpoint change passes every gate. And the committed library report is stale, so it cannot serve as the "unchanged except lib11" baseline.

Scope: no running app was exercised, so `scores.verify_quickly` (D-015) is not scored here. Everything below ran on `git archive` copies in the scratchpad, or on copies derived from them. Nothing was run in the project tree.

## What I exercised

- `git show 78450f6 -- evals/library/case_lib11_priors_and_ledger.expected.json`, `git show --stat 78450f6`, `git diff --stat ea6ac71 78450f6`. Only the lib11 expected file and two fixture reports changed.
- `python3 tools/board.py show T-116` and `show T-118`. The five edits (note items 1 to 5) were compared line by line with the diff.
- `git archive HEAD` into the scratchpad (`t118-head`, 78450f6). `git archive ea6ac71` (`t118-pre`). Mutant A: HEAD with the pre-commit lib11 file restored. Mutant B: HEAD with lib11 record 6 kind `encounter` and E6 `encounter` true.
- `research/validate_library.py` (exit 0 on HEAD, exit 0 on mutant A, exit 1 on mutant B). `evals/golden/check_golden.py` (exit 0 on HEAD). Note that `check_golden.py` covers only the 10 `evals/golden` cases. The lib11 truth is checked by `validate_library.py`, which runs 25 cases.
- `evals.library_report` at HEAD and at ea6ac71: both exit 0 and the outputs are byte-identical (`library-pre-vs-head.diff` is empty). The committed `evals/reports/library-latest.md` against the regenerated HEAD report.
- `artifacts/review-evidence/T-118-paralegal-endpoints.py` (new probe): gap_table dates, days, flag, from_records, to_records, and gap_excluded_records on all 25 packets. HEAD: 0 differences. ea6ac71: 3 differences, all lib11. Mutant A: 3 differences.
- `artifacts/review-evidence/T-118-paralegal-lib11-view.py`: the product's own lib11 output at HEAD (records, entries, gap flags).
- `pytest tests/unit/test_gaps.py tests/unit/test_t116_gap_endpoints.py`: 116 passed on HEAD, 116 passed on mutant A.
- Read: lib11 packet `.txt` lines 20 and 28 to 31; expected JSON lines 43, 57, 157, 190; `app/backend/gaps.py` 80 to 175; `check_golden.py` 200, 242 to 243, 255 to 260; `evals/run.py` 243 to 248; `tests/unit/test_gaps.py` 6 to 15; `tests/unit/test_t116_gap_endpoints.py` 165 to 179; `reviews/T-116-paralegal.md` finding 2 (fix text); `board.py list` (no follow-up card for T-116 minor F3 found).
- Evidence: `artifacts/review-evidence/T-118-paralegal-evidence.sh` runs the checks above, and its outputs are in `artifacts/review-evidence/T-118-out/` (`validate-head.txt`, `check-golden-head.txt`, `library-pre-vs-head.diff`, `library-committed-vs-head.diff`, `probe-head.txt`, `probe-pre.txt`, `lib11-view-head.txt`, `mutA-validators.txt`, `mutA-probe.txt`, `mutB-validate.txt`, `pytest-head.txt`, `pytest-mutA.txt`).

## Checks against the card

| Card claim | Result |
|---|---|
| Five edits match the T-116 r2 note (items 1 to 5, lines 57, 190, 251 to 254, 276 to 279, 286 to 289) | Match. Dates, days and flags unchanged. |
| Record 6 is an intake form and not a gap endpoint | Packet line 30 reads `new patient intake form (OCR text)`. Product HEAD gap table has no record 6 endpoint (`lib11-view-head.txt`). Match. |
| `validate_library.py` exit 0 | Pass (`validate-head.txt`). |
| `check_golden.py` exit 0 | Pass (`check-golden-head.txt`). |
| Only lib11 gap endpoints changed in the library report | The report has no endpoint column, so it cannot show this. The report is unchanged (0-line diff). The endpoint change itself is correct and confined to lib11 (probe: 3 differences at ea6ac71, all lib11; 0 at HEAD). See finding 2 for why nothing guards it. |

## Out of my lens (not graded, for qa and the orchestrator)

- The commit also replaces `evals/reports/latest.json`. The parent file was a `claude-cli` run (`generated_at` 2026-11-02T04:09:33Z, `blockers` `['3_flags', '4_no_invented_facts']`). HEAD is a `fixture` run (09:56:40Z, `blockers` `['4_no_invented_facts', 'backend=fixture: determinism...', 'judge_controls...']`). The T-118 handoff says "same 3 pre-existing blockers as latest.json before this change", which the parent file does not show. Evidence: `T-118-out/latest-pre.json`, `T-118-out/latest-head.json`.

<!-- findings and scores are in the JSON block below -->

```json
{"card": "T-118", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "git archive HEAD (78450f6) copy in the scratchpad, plus archive of ea6ac71 and mutants A and B derived from HEAD; no running app; sample packets evals/library/case_lib11 and all 25 golden and library gap packets",
 "exercised": [
  "git show 78450f6 lib11 expected diff; git show --stat 78450f6; git diff --stat ea6ac71 78450f6",
  "python3 tools/board.py show T-116 and show T-118; compared the five edits against T-116 r2 card note items 1 to 5",
  "research/validate_library.py on HEAD (exit 0), mutant A (exit 0), mutant B (exit 1); evals/golden/check_golden.py on HEAD (exit 0)",
  "evals.library_report at HEAD and ea6ac71: exit 0, byte-identical; committed evals/reports/library-latest.md vs regenerated HEAD",
  "artifacts/review-evidence/T-118-paralegal-endpoints.py: gap_table record lists and gap_excluded_records on 25 packets; HEAD 0 differences, ea6ac71 3 (all lib11), mutant A 3",
  "artifacts/review-evidence/T-118-paralegal-lib11-view.py on HEAD: product records, entries and gap flags for lib11",
  "pytest tests/unit/test_gaps.py tests/unit/test_t116_gap_endpoints.py: 116 passed on HEAD and on mutant A",
  "read lib11 packet lines 20, 28 to 31; expected JSON lines 43, 57, 157, 190; app/backend/gaps.py 80 to 175; check_golden.py 200, 242 to 243, 255 to 260; evals/run.py 243 to 248; tests/unit/test_gaps.py 6 to 15; tests/unit/test_t116_gap_endpoints.py 165 to 179; reviews/T-116-paralegal.md finding 2",
  "artifacts/review-evidence/T-118-paralegal-evidence.sh and artifacts/review-evidence/T-118-out/* (outputs of every run above)"
 ],
 "verdict": "changes",
 "scores": {"lib11_edits_match_card_note": 5, "gap_endpoints_match_product_25_packets": 5, "truth_record_kinds_match_packet": 2, "endpoint_regression_guarded": 2, "library_report_baseline_current": 2},
 "findings": [
  {"severity": "major",
   "title": "Truth file gives lib11 record 6 (intake form) and record 4 (letter) the kind phone_note, which the packet does not state; the checker's vocabulary forces it, and product and truth disagree on record kind",
   "evidence": "evals/library/case_lib11_priors_and_ledger.txt:30 'Source: Fennimoor Spine Clinic, new patient intake form (OCR text)'; evals/library/case_lib11_priors_and_ledger.expected.json:57 'kind': 'phone_note' (record 6), :43 'kind': 'phone_note' (record 4; packet .txt:20 says 'correspondence (letter of protection)'; pre-existing, not changed by 78450f6), :190 'encounter': false (E6). evals/golden/check_golden.py:200 allows only encounter, billing_statement, phone_note; :242 to 243 require entry encounter to equal kind; :255 to 260 derive gap_excluded_records from record kinds. Mutant B (record 6 kind encounter, E6 true, card lists kept): artifacts/review-evidence/T-118-out/mutB-validate.txt 'gap_excluded_records [4, 6, 9] != non-encounter/ambiguous records [4, 9]' and two 'record lists wrong', exit 1. Product at HEAD: artifacts/review-evidence/T-118-out/lib11-view-head.txt '6 2026-03-27 encounter | Fennimoor Spine Clinic, new patient intake form (OCR text)' and '4 2026-03-26 records_admin | ...'. Entries in case_view carry no encounter field (None for e5 and e6 in the same file). app/backend/conflicts.py:13 and pipeline.py:258 still read kind 'encounter' for record 6 (T-116 minor F3; no follow-up card found in board.py list).",
   "why_it_matters": "The truth file asserts a record type the packet does not state, and the checker's three-kind vocabulary is the reason. T-116 r1 (reviews/T-116-paralegal.md, major, fix item 1) asked for the intake-form kind to be decided and the vocabulary extended; r2 used phone_note as a stand-in and left the intake kind for later. Now the truth says phone_note and E6 encounter false, while the product says encounter for the same record. No test compares those fields, so the E6 assertion is never measured. Not a blocker today: the product's gap output is right (finding 2 probe, 0 differences), no statement or amount shown to the paralegal calls record 6 a visit (no non-mock frontend reads the field), and the export is built from accepted entries. This becomes a blocker if any surface shows record kind 'encounter' for an intake form.",
   "fix": "Extend check_golden.py:200 (and the rules at :242 to 243 and :255 to 260) with intake_form and correspondence kinds. Set records[6].kind to intake_form, records[4].kind to correspondence, E6 encounter false. Researcher and qa decide whether the product's record kind for an intake form stays encounter (ingest.py:221 and :320, present.py:169) and whether conflicts.py:13 and pipeline.py:258 should use the non-visit classifier (T-116 minor F3, still open).",
   "acceptance_test": "research/validate_library.py exits 0 with the new kinds and the card's gap lists; mutant B (kind encounter with E6 true) fails validate_library.py; a product-level test fails when the product's record-6 kind or entry encounter disagrees with the truth file."},
  {"severity": "major",
   "title": "No test or report enforces the lib11 gap endpoints, so reverting the card's edits passes every gate; the T-116 r1 record-list test was never added",
   "evidence": "tests/unit/test_t116_gap_endpoints.py:165 to 173 compares (from_date, to_date, days, flag) only. tests/unit/test_gaps.py:6 to 7 builds records from the golden file's own kinds, so it never runs ingest, and it passes with either lib11 truth. evals/run.py:243 to 248 scores (from, to, days, flag) only. evals/reports/library-latest.md has no endpoint column; library-pre-vs-head.diff is empty. Mutant A (pre-commit lib11 truth restored in a scratch copy): validate_library.py exit 0 (T-118-out/mutA-validators.txt), pytest of both gap files 116 passed (T-118-out/pytest-mutA.txt), while the endpoint probe reports 3 differences (T-118-out/mutA-probe.txt). reviews/T-116-paralegal.md finding 2 fix asked to 'make the gap test compare (from_records, to_records) for all golden and library packets'. The T-116 r2 handoff deferred it ('Suggest tests/unit gap test compare ...').",
   "why_it_matters": "The T-118 acceptance line says the library report is unchanged 'except lib11 gap endpoints', but the report cannot show endpoints, so that claim cannot be checked from the report. Any future change to a record list on any packet, lib11 included, passes every committed test and the library report. Only the probe I wrote for this review catches it. The persona's checklist item 5 and the T-116 finding depend on this.",
   "fix": "Add a tests/unit test that ingests each golden and library packet (ingest, language.annotate, gaps.compute_gaps, as artifacts/review-evidence/T-118-paralegal-endpoints.py does) and asserts from_records and to_records for every gap_table row, and gap_excluded_records equal to the expected values. Add an endpoint column to evals/library_report or compare record lists in evals/run.py:243 to 248.",
   "acceptance_test": "On mutant A (pre-commit lib11 truth), the new test fails naming case_lib11_priors_and_ledger. On HEAD it passes, and artifacts/review-evidence/T-118-paralegal-endpoints.py reports 0 differences over 25 packets (T-118-out/probe-head.txt)."},
  {"severity": "minor",
   "title": "Committed evals/reports/library-latest.md is stale against HEAD (lib09 amounts row), so the report cannot be used as the 'unchanged' baseline; not caused by 78450f6",
   "evidence": "evals/reports/library-latest.md:17 '| case_lib09_spanish_interpreter_espalda | done | 4/7 | 2/5 | False | 1/2 | 0 | M5 | 0 | - |'. Regenerated at HEAD and at ea6ac71: '3/5' (T-118-out/library-committed-vs-head.diff; library-pre-vs-head.diff empty). The committed file's source commit is a74b727. git show --stat 78450f6 does not list it.",
   "why_it_matters": "A committed report that does not match HEAD cannot show what a commit changed, and the persona's billed-charge reconciliation depends on the report agreeing with the code. The stale amounts row predates this card.",
   "fix": "qa regenerates evals/reports/library-latest.md from a clean worktree of the commit it cites, as the file's own header asks, and the card cites that commit.",
   "acceptance_test": "Running evals.library_report at the cited commit in a clean worktree gives a report identical to the committed file, except the provenance line."}
 ],
 "whats_right": [
  "The five lib11 edits match the T-116 r2 card note item for item (git show 78450f6 diff at lines 57, 190, 251 to 254, 276 to 279, 286 to 289); dates, days and flags are unchanged.",
  "Product gap endpoints are correct on all 25 golden and library packets, including record lists and exclusions (probe at HEAD: 0 differences); lib11 record 6 is excluded by its intake-form header (packet line 30).",
  "Both validators pass on HEAD, and the commit touches only the lib11 truth file plus two fixture reports (git diff --stat ea6ac71 78450f6)."
 ],
 "questions_for_chris": [
  "Should an intake form dated the same day as a visit (lib11 record 6, 'Prior accidents? No') stay a chronology entry? Today it is entry E6, the truth says it is not an encounter, and the product still says encounter. The answer decides whether the adjuster-facing 'prior accidents: No' answer is listed in the treatment chronology or kept in an administrative entry."
 ]}
```
