# T-116 round 3 review: paralegal-reviewer (Maria Delgado persona)

Commit under review: 8673326 (HEAD, `python3 tools/board.py show T-116` lists commits c1b44be, ea6ac71, 8673326; `git log` agrees).
Pre-T-116 baseline: 3e3f3b7 (parent of c1b44be, `git rev-parse --short c1b44be^`). Both trees were run from `git archive` copies in the
scratchpad, not from the dirty project tree. D-055 (memory/ORCHESTRATOR_DECISIONS.md:63) is the binding rule.

## Verdict: fail (two blockers, two majors)

Relative to pre-T-116, nothing moved: gap dates, day counts, flags and endpoints are identical on all 25 packets and on every probe label.
The warning works where a gap starts or ends at an intake form. But the change removed the exclusion only in gaps.py. The same label guess
still runs one layer down (ingest.record_kind, whole Source label, via lexicon `non_encounter`) and gap math still reads it. So real visits
still produce invented 40-day gaps with no warning, and F3 (the accident-date baseline stating an intake form as the first recorded
treatment) is still a warning on top of the same false sentence.

## What I checked

1. **Every r1 and r2 label (27 visit labels, plain and headed excerpt, inside a three-visit packet) plus the 3 controls.** Same gap as
   pre-T-116 for all 60 runs: `artifacts/review-evidence/T-116-paralegal-r3-compare.out.txt` section A reports "gap endpoints differing
   pre vs HEAD: none" and "flags differing: none". No label gets a HEAD warning, because none of them is a paperwork-looking endpoint of a
   flagged gap (the warning is exercised by W1 and W2 and by lib09 instead).
2. **No gap invented or dropped relative to pre-T-116:** true for all 60 runs, 10 Appendix A variants and 25 packets (section B and C).
   **Relative to D-055 it fails**, see F1 and F4.
3. **25 packets' gap dates vs pre-T-116:** 25/25 identical (dates, days, flags, record lists) in section C. Against the committed expected
   files, dates, days and flags match for all 25; record lists differ on lib11 only (F3).
4. **Accident-date baseline (F3):** section D of the compare output. HEAD still emits "is later than the first recorded treatment, January 12,
   2026 (Capital PT, intake form)" with a warning appended (F2).
5. **pytest:** `.venv/bin/python -m pytest -q tests/unit -k gap` in the project tree (run with `PYTHONDONTWRITEBYTECODE=1 ... -p no:cacheprovider`
   so the tree is not written): `246 passed, 2397 deselected in 4.67s` (`artifacts/review-evidence/T-116-paralegal-r3-pytest-gap-tree.out.txt`).
   Same on the HEAD archive: `246 passed, 2390 deselected in 4.67s` (`...-pytest-gap-head.out.txt`). The project tree is dirty (other agents'
   uncommitted edits), so the archive run is the authoritative one. The archive has 2390 selected tests because the working tree holds seven
   more uncommitted tests.
6. **Validators on the HEAD archive:** `research/validate_library.py` exit 0 and `evals/golden/check_golden.py` exit 0
   (`T-116-paralegal-r3-validator-HEAD.out.txt`, `T-116-paralegal-r3-check-golden-HEAD.out.txt`). Both pass while the lib11 truth contradicts the product (F3).
7. **Warning where it applies (W1, W2, lib09):** `artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.head.out.txt`. A gap that ends
   at "Capital PT, intake form" (W1) and one that starts there (W2) each carry "This gap ends/starts at record N: Capital PT, intake form, which
   looks like paperwork, not a visit. Check whether treatment continued." in explanation, endpoint_warnings and why. lib09 through the API:
   before confirm 42 days (3 Mar to 14 Apr); after confirming record 4 as 5 March, 40 days, the same as pre-T-116 (`...pre-3e3f3b7.out.txt`),
   and HEAD adds the start warning with record 4 and its verbatim header "Consultorio Médico Aguaclara, formulario de admisión (OCR)". The
   gap_changes sentence reads "Gap recalculated after you confirmed record 4: now 40 days (was 42)."
8. **Read the code:** app/backend/gaps.py (HEAD, 176 lines), conflicts.py:12-14, pipeline.py:257-259, ingest.py:214-221,
   app/llm/lexicon.yaml:1280-1292, test_t116_gap_endpoints.py:60-64 and 163-170, memory/SCOPE_CUTS.md:75, board cards T-113 and T-116.
9. **Did not drive the running app on localhost:7860.** `scores.verify_quickly` is therefore not scored in this round (D-015 applies when the running app is reviewed).

## Findings

**Blocker F1. Visit labels that carry a non-encounter word are still removed from gap math, at ingest. The r3 fix removed only the gaps.py layer.**
The 40-day gap is invented for five visit labels, and one visit that ends a real 40-day span hides it.
- Evidence: `artifacts/review-evidence/T-116-paralegal-r3-compare.out.txt` section A, plain and headed excerpt alike:
  "Capital PT, initial evaluation, correspondence | pre=[40] head=[40]", "Dr. Lee, chiropractic, visit 3 - records request copy | pre=[40] head=[40]",
  "Office visit / records request | pre=[40] head=[40]", "Capital PT, visit 5 (ledger balance reviewed) | pre=[40] head=[40]",
  "Austin Imaging, MRI cervical spine (records request attached) | pre=[40] head=[40]". None carries a warning ("labels with a HEAD warning: none").
  The ingest kinds are records_admin or billing_statement (probe JSON, labels loop). Three of the eight r2 labels fail the r2 acceptance test.
  Hidden gap, W4: `artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.head.out.txt` "[W4 ...] kinds: [(1, '2026-03-01', 'encounter'), (2, '2026-04-10', 'records_admin')] no gap flag".
  Root: `app/backend/ingest.py:214-221` (record_kind reads the whole Source label through lexicon `non_encounter`), `app/backend/gaps.py:104`
  (compute_gaps keeps only kind == "encounter"), `app/llm/lexicon.yaml:1282` ("records whose source label matches are excluded from gap arithmetic").
  Pre-T-116 (3e3f3b7) gives the identical result, so "same as before T-116" is not the test D-055 sets.
- Why it matters: D-055 says gaps never exclude records by guessing and no record is silently dropped. A visit labelled "initial evaluation" or
  "visit 5" is a treatment encounter. The tool reports a 40-day gap that the records do not show and states nothing about the visit. Persona
  section 5: an invented or dropped gap is a blocker. The card's claim that the exclusion is removed holds only for gaps.py, and the r1 F1 and
  r2 F1 blockers are still open in this form.
- Fix: decide the endpoint rule across the whole chain, not one layer. A label naming a visit (visit, evaluation, daily note, new patient,
  follow-up, imaging study) keeps the record a treatment endpoint, whatever trailing word it carries (the r2 ask). Either apply D-055 as written
  (every dated record is an endpoint, paperwork warns) or keep paperwork out with a visible note beside the span (see F4 and question 1). Change
  lexicon.yaml:1282 to match (researcher-owned). Add unit tests that go through ingest.ingest and gaps.gap_flags with a clinical excerpt.
- Acceptance test: re-run `artifacts/review-evidence/T-116-paralegal-r3-probe.py` on the new HEAD. Zero of the 27 visit labels produce an invented
  40-day flag, and W4 shows a 40-day flag from 1 March to 10 April. The 25 packets stay identical to pre-T-116 except for any documented change.

**Blocker F2. F3 is not closed. The accident-date baseline and the accident year still count an intake form as the first recorded treatment, with a warning added.**
- Evidence: `artifacts/review-evidence/T-116-paralegal-r3-compare.out.txt` section D. HEAD kinds `[(1, 'encounter'), (2, 'encounter')]`. Explanation:
  "Stated accident date January 15, 2026 (...) is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form). The records
  disagree; the tool does not choose between them. The earliest recorded date is record 1: Capital PT, intake form, which looks like paperwork,
  not a visit. Check when treatment actually began before relying on this comparison." Code: `app/backend/conflicts.py:12-14` (`_encounters`
  keeps kind == "encounter"), `app/backend/pipeline.py:258` (`_accident_year`, passed to the flag pass at pipeline.py:333-338).
  `memory/SCOPE_CUTS.md:75` defers the year hint to M3. `board show T-113`: the card covers the conflict judge (J3V1, J3V9, J3V13, H3V5); its
  acceptance criteria do not mention the accident-date baseline (`grep -ci accident board/cards/T-113.md` returns 1, from the H3V5 description
  line only). The "conflict part moved to T-113" has no card behind it for this baseline.
- Why it matters: D-017 and R-FL-2 say the tool does not state a non-treatment record as the first recorded treatment. The HEAD sentence still
  does so, and the warning is appended after it, so the headline is the false fact. My r2 F3 asked for the baseline to skip paperwork, and the
  r3 card chose warning-only. A warning beside a false treatment date is still a false treatment date. Persona section 5: blocker. Reach in the
  25 packets is still zero; the defect is reachable with a constructed case.
- Fix: route `_encounters` (conflicts.py:12-14) and `_accident_year` (pipeline.py:258) through the same treatment test as F1, for the baseline only.
  Keep stated-date sources from every record, including an intake form's own accident-date line. If the team keeps warning-only, the sentence must
  not say "first recorded treatment" for a paperwork record. Give the baseline a card with an owner (T-113 does not cover it).
- Acceptance test: `artifacts/review-evidence/T-116-paralegal-r3-probe.py` section D on the new HEAD. The intake form (2026-01-12) raises no
  "later than the first recorded treatment" sentence, and any remaining first-treatment wording cites the 2026-01-20 visit. Unit test: an intake form
  dated before the first visit, with a stated accident date between the two, raises no such conflict.

**Major F3. lib11 committed truth (T-118's five edits) now contradicts the HEAD product.** The validators pass and the gap test does not compare lists.
- Evidence: `git show 8673326:evals/library/case_lib11_priors_and_ledger.expected.json`: line 57 record 6 `"kind": "phone_note"`; line 251 `gap_excluded_records` [4, 6, 9];
  gap rows with `to_records` [5] and `from_records` [5] (lines 276-289). Product at HEAD, `T-116-paralegal-r3-compare.out.txt` section C: gap rows
  `[2, 3] -> [5, 6]` and `[5, 6] -> [7]`, record 6 kind "encounter" (`ingest` keeps it an encounter). The validator and check_golden exit 0 on HEAD
  (`T-116-paralegal-r3-validator-HEAD.out.txt`). `tests/unit/test_t116_gap_endpoints.py:163-170` compares dates, days and flags only.
- Why it matters: the committed truth calls an intake form a phone call, and its excluded list no longer matches anything the product outputs
  (`computed.excluded_records` was removed). The r3 handoff says so ("qa should re-check"), but card AC1 is still ticked done. r1 F2 and r2 F2
  are open, now in reverse.
- Fix: qa restores lib11 to the agreed truth for the chosen rule (record 6 encounter, rows [5, 6] and [5, 6]) and drops or redefines
  `gap_excluded_records`. The gap test compares (from_records, to_records) for all 25 packets. Reopen AC1 until the truth matches the product.
- Acceptance test: the list test fails on 8673326 for lib11 and passes after the fix; `research/validate_library.py` exits 0 with the truth and the
  product's gap rows equal for all 25 packets.

**Major F4. A paperwork-looking record dated inside a span over 30 days splits it, and the 40-day span disappears with no warning.** Pre-T-116 is the same.
- Evidence: `artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.head.out.txt` "[W3 intake form dated INSIDE a 40-day span with no visit]
  kinds: [(1, '2026-03-01', 'encounter'), (2, '2026-03-20', 'encounter'), (3, '2026-04-10', 'encounter')] no gap flag". Record 2 is
  "Capital PT, intake form", which ingest keeps as an encounter (F2). The pre-T-116 output is identical.
- Why it matters: 1 March to 10 April has no treatment visit, and the adjuster will attack exactly that. D-055's warning covers only gaps that start
  or end at paperwork, so a gap that never appears gets no warning. Persona section 3 ("surfaces what the adjuster will attack"). I rate it major, not
  blocker, because no record is invented. The reading of D-055 decides it (question 1).
- Fix: when a paperwork-looking endpoint splits a span over 30 days into pieces of 30 days or fewer, show a visible note on the split (for example "No
  treatment visit between March 1 and April 10 (40 days); the only record inside is an intake form on March 20"). Waiting for the D-055 decision first.
- Acceptance test: W3 shows a visible note naming the span and the paperwork record; W1 and W2 keep their current warnings.

**Minor F5. The "identical to pre-T-116" test cannot see exclusion by kind.** `tests/unit/test_t116_gap_endpoints.py:60-64` (`legacy_gaps`) copies
the same `kind == "encounter"` filter as `gaps.py:104`, so the 25-packet comparison passes whatever the kind filter does. Fix: compare against the
expected files' record lists (see F3) and add a test that runs F1's labels through ingest. Acceptance: the test fails on HEAD for the five labels.

## What is right

1. Pre-T-116 vs HEAD: 25/25 packets, 60/60 label runs and 10/10 Appendix A variants keep identical dates, days, flags and endpoints. The sample's
   73-day flag stays with endpoints 6 and 7, and the 28-day interval is not flagged.
2. A gap that starts or ends at an intake form now carries the record number and verbatim header in explanation, why and endpoint_warnings, and
   lib09 after confirming record 4 reads "This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR)...". This closes r1 F4 and r2 F4.
3. The ", fax" family is fixed in gaps.py. Appendix A treatment records with ", fax" keep the 73-day flag (10/10 SAME), and the r2 bare-delivery-word
   blocker no longer reproduces for those labels. The remaining failures in F1 come from the ingest layer.

## Outside my lens

The choice between "every dated record is an endpoint" and "paperwork is never an endpoint" is a product and spec decision (question 1). Whether
the accident baseline should skip paperwork is a conflict-logic decision for the litigation lead under D-017 (question 2). The lexicon and
classifier architecture (two lists, lexicon.yaml and ingest) is for staff-engineer and researcher.

## Questions for Chris

1. D-055 says "gap math runs over all dated records". The code keeps intake forms as endpoints and drops bills, phone notes, letters and records
   requests by kind. Which do you want? (a) Every dated record is an endpoint, paperwork warns. A bill mid-span can then hide a gap (F4). (b)
   Paperwork is never an endpoint, and a visible note names each paperwork record inside a span over 30 days.
2. F2: is warning-only acceptable for the accident-date baseline, or must it skip paperwork? T-113 does not cover the baseline, so who owns it?
3. lib11 record 6 and `gap_excluded_records` (carried from r1 and r2): restore the pre-T-116 truth (encounter, excluded [4, 9]), or add an intake-form kind to the golden schema?

```json
{"card": "T-116", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 8673326 (HEAD, T-116 r3, D-055) vs pre-T-116 parent 3e3f3b7; git archive copies in the scratchpad (t116r3/head, t116r3/pre-3e3f3b7); app/backend/gaps.py, conflicts.py, pipeline.py, ingest.py record_kind, lexicon.yaml non_encounter, tests/unit/test_t116_gap_endpoints.py, evals/library lib11 truth; 25 golden+library packets plus sample; the running app at localhost:7860 was not driven",
 "exercised": [
  "read personas/paralegal.md in full; memory t116-gap-endpoint-patterns and t118-lib11-truth-patterns; board show T-116 and T-113; board list --status in_progress; git log -12; git rev-parse c1b44be^ (= 3e3f3b7)",
  "git show 8673326 --stat and the diffs of conflicts.py, pipeline.py, present.py, review.py, flag_templates.py, memory/contracts/api.md; git show 8673326:app/backend/gaps.py, ingest.py:214-221, lexicon.yaml:1280-1292, pipeline.py:257-259, conflicts.py:12-14, test_t116 lines 60-64 and 163-170, lib11 expected lines 57 and 251-289",
  ".venv/bin/python -m pytest -q tests/unit -k gap in the project tree (PYTHONDONTWRITEBYTECODE=1, -p no:cacheprovider): 246 passed, 2397 deselected (artifacts/review-evidence/T-116-paralegal-r3-pytest-gap-tree.out.txt); same command on the HEAD archive: 246 passed, 2390 deselected (...-pytest-gap-head.out.txt); collect-only test_t116_gap_endpoints.py: 136 tests",
  "research/validate_library.py and evals/golden/check_golden.py on the HEAD archive: both exit 0 (T-116-paralegal-r3-validator-HEAD.out.txt, T-116-paralegal-r3-check-golden-HEAD.out.txt)",
  "artifacts/review-evidence/T-116-paralegal-r3-probe.py run on pre-T-116 (3e3f3b7) and HEAD (8673326): 27 visit labels + 3 controls x plain and headed excerpt in a three-visit packet through ingest.ingest and gap_flags; Appendix A control + 9 treatment records with ', fax'; the 25 packets through the fixture pipeline (evals.run); the F3 constructed intake-form case",
  "artifacts/review-evidence/T-116-paralegal-r3-compare.py over the two outputs: artifacts/review-evidence/T-116-paralegal-r3-compare.out.txt (sections A to D)",
  "artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.py on both trees: W1 to W4 constructed packets; lib09 through the FastAPI TestClient, confirm_date on record 4 (outputs ...warn-and-api.pre-3e3f3b7.out.txt and ...warn-and-api.head.out.txt)",
  "inline python scan of the HEAD packet records: every non-encounter record in the 25 packets is a bill, phone note, letter, ledger, affidavit or records-retrieval item; no treatment visit is excluded in a packet; encounter-kind labels with paperwork words are the four intake and form labels in lib07, lib09, lib11 and case_04",
  "T-113 and T-116 cards and memory/SCOPE_CUTS.md:73-75 checked for the accident-date baseline owner"
 ],
 "verdict": "fail",
 "scores": {"gap_figures_unchanged_vs_pre_t116": 5, "warning_where_it_applies": 4, "no_invented_or_dropped_gap": 2, "f3_baseline_not_encounter": 1, "lib11_truth_consistency": 2},
 "findings": [
  {"severity": "blocker",
   "title": "Visit labels that carry a non-encounter word are still removed from gap math at ingest (record_kind, whole label); five real visits produce invented 40-day gaps with no warning and one visit hides a 40-day span. The r3 fix removed only the gaps.py layer",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r3-compare.out.txt section A: 'Capital PT, initial evaluation, correspondence | pre=[40] head=[40]'; 'Dr. Lee, chiropractic, visit 3 - records request copy | pre=[40] head=[40]'; 'Office visit / records request | pre=[40] head=[40]'; 'Capital PT, visit 5 (ledger balance reviewed) | pre=[40] head=[40]'; 'Austin Imaging, MRI cervical spine (records request attached) | pre=[40] head=[40]'; 'labels with a HEAD warning: none'. artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.head.out.txt '[W4 ...] kinds: [(1, 2026-03-01, encounter), (2, 2026-04-10, records_admin)] no gap flag'. app/backend/ingest.py:214-221; app/backend/gaps.py:104; app/llm/lexicon.yaml:1282",
   "why_it_matters": "D-055 (binding): gaps never exclude records by guessing and no record is silently dropped. The same label guess that r1 F1 and r2 F1 reported still invents a gap for visits named 'initial evaluation' or 'visit 5', and hides a real span when the visit is the endpoint. The 'same as pre-T-116' result is not the D-055 test. Persona section 5: invented or dropped gap = blocker. Three of the eight r2 labels still fail the r2 acceptance test.",
   "fix": "Decide the endpoint rule across the chain, not one layer: a label naming a visit keeps the record a treatment endpoint whatever trailing word it carries (the r2 ask); paperwork is decided by its record-type head. Either apply D-055 literally (every dated record is an endpoint, paperwork warns) or keep paperwork out with a visible note beside the span (F4, question 1). Change lexicon.yaml:1282 to match (researcher-owned). Add unit tests through ingest.ingest and gaps.gap_flags with a clinical excerpt.",
   "acceptance_test": "Re-run artifacts/review-evidence/T-116-paralegal-r3-probe.py and T-116-paralegal-r3-compare.py on the new HEAD: zero of the 27 visit labels produce an invented 40-day flag; W4 shows a 40-day flag from 2026-03-01 to 2026-04-10; the 25 packets stay identical to pre-T-116 except for a documented change."},
  {"severity": "blocker",
   "title": "F3 not closed: the accident-date baseline (conflicts._encounters) and accident year (pipeline._accident_year) still count an intake form as the first recorded treatment; the r3 warning is appended after the false sentence",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r3-compare.out.txt section D: HEAD kinds [(1, 'encounter'), (2, 'encounter')]; explanation 'Stated accident date January 15, 2026 (...) is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form). ... The earliest recorded date is record 1: Capital PT, intake form, which looks like paperwork, not a visit.' app/backend/conflicts.py:12-14; app/backend/pipeline.py:258 (passed at pipeline.py:333-338); memory/SCOPE_CUTS.md:75 (year hint deferred to M3); board show T-113: the card covers the conflict judge only, no accident-date text.",
   "why_it_matters": "D-017 and R-FL-2: the tool must not state a non-treatment record as the first recorded treatment. The HEAD sentence still does, and a warning beside a false treatment date does not make it true. My r2 F3 asked for the baseline to skip paperwork; r3 chose warning-only. The 'conflict part moved to T-113' has no card behind the baseline. Persona section 5: false fact = blocker. Reach in the 25 packets is zero; reachable with a constructed case.",
   "fix": "Route conflicts._encounters (conflicts.py:12-14) and pipeline._accident_year (pipeline.py:258) through the same treatment test as F1, for the baseline only; keep stated-date sources from every record, including an intake form's own accident-date line. If warning-only is kept, the sentence must not say 'first recorded treatment' for a paperwork record. Give the baseline an owner card.",
   "acceptance_test": "artifacts/review-evidence/T-116-paralegal-r3-probe.py section D on the new HEAD: the 2026-01-12 intake form raises no 'later than the first recorded treatment' sentence, and any first-treatment wording cites the 2026-01-20 visit. Unit test: an intake form dated before the first visit with a stated accident date between the two raises no such conflict."},
  {"severity": "major",
   "title": "lib11 committed truth (T-118 edits) now contradicts the HEAD product: record 6 is phone_note, excluded list [4, 6, 9], gap rows [5] and [5]; product gives [5, 6] and [5, 6]. Validators pass and the gap test does not compare lists",
   "evidence": "git show 8673326:evals/library/case_lib11_priors_and_ledger.expected.json line 57 record 6 'kind': 'phone_note'; line 251 gap_excluded_records [4, 6, 9]; gap rows to_records [5] / from_records [5] (lines 276-289). artifacts/review-evidence/T-116-paralegal-r3-compare.out.txt section C: 'lib11 HEAD gap rows' [2, 3]->[5, 6] and [5, 6]->[7]; record 6 kind 'encounter'. artifacts/review-evidence/T-116-paralegal-r3-validator-HEAD.out.txt exit 0; T-116-paralegal-r3-check-golden-HEAD.out.txt exit 0. tests/unit/test_t116_gap_endpoints.py:163-170 compares dates, days and flags only.",
   "why_it_matters": "The committed truth calls an intake form a phone call and lists exclusions the product no longer makes. Card AC1 is ticked done while the truth disagrees. r1 F2 and r2 F2 are open, now in reverse (the r3 handoff itself says qa should re-check).",
   "fix": "qa sets lib11 to the truth for the rule chosen in F1 (record 6 encounter, rows [5, 6] and [5, 6] if paperwork-endpoint stays), drops or redefines gap_excluded_records, and extends the gap test to compare (from_records, to_records) for all 25 packets. Reopen AC1 until the truth matches the product.",
   "acceptance_test": "The record-list test fails on 8673326 for lib11 and passes after the fix; research/validate_library.py and check_golden.py exit 0; product gap rows equal the committed expected rows for all 25 packets."},
  {"severity": "major",
   "title": "A paperwork-looking record dated inside a span over 30 days splits the span and the 40-day stretch vanishes with no warning (pre-T-116 identical)",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.head.out.txt '[W3 intake form dated INSIDE a 40-day span with no visit] kinds: [(1, 2026-03-01, encounter), (2, 2026-03-20, encounter), (3, 2026-04-10, encounter)] no gap flag'; the pre-T-116 output is identical (artifacts/review-evidence/T-116-paralegal-r3-warn-and-api.pre-3e3f3b7.out.txt).",
   "why_it_matters": "There is no treatment visit between 1 March and 10 April, and the adjuster will attack exactly that (persona section 3). D-055's warning covers only gaps that start or end at paperwork, so a gap that never appears gets no warning. Major, not blocker: no record is invented; the decision depends on the D-055 reading.",
   "fix": "When a paperwork-looking endpoint splits a span over 30 days into pieces of 30 days or fewer, show a visible note on the split naming the span and the paperwork record. Wait for the D-055 reading (question 1) before choosing the wording or the rule.",
   "acceptance_test": "W3 shows a visible note naming 2026-03-01 to 2026-04-10 and the 2026-03-20 intake form; W1 and W2 keep their current warnings."},
  {"severity": "minor",
   "title": "The 'identical to pre-T-116' test copies the same kind filter, so it cannot detect exclusion by kind",
   "evidence": "tests/unit/test_t116_gap_endpoints.py:60-64 (legacy_gaps: 'every dated record of kind encounter is an endpoint') and :163-170 (compares compute_gaps to legacy_gaps, and to the expected dates only).",
   "why_it_matters": "The test passes whatever the kind filter does, so F1 is invisible to the suite. The card's 25-packet evidence therefore proves less than it states.",
   "fix": "Compare against the expected record lists (see F3) and add F1's labels through ingest.ingest.",
   "acceptance_test": "The new test fails on 8673326 for the five labels in F1 and passes after the F1 fix."}
 ],
 "whats_right": [
  "Gap dates, days, flags and endpoints are identical to pre-T-116 on all 25 packets, all 60 label runs and all 10 Appendix A variants; the sample keeps its 73-day flag on records 6 and 7 and the 28-day interval stays unflagged.",
  "A gap that starts or ends at an intake form carries the record number and verbatim header in explanation, why and endpoint_warnings; lib09 after confirming record 4 moves 42 to 40 days with the start warning (closes r1 F4 and r2 F4).",
  "The ', fax' family is fixed in gaps.py: all nine Appendix A treatment records with ', fax' keep the 73-day flag, so the r2 bare-delivery-word failure no longer reproduces."
 ],
 "questions_for_chris": [
  "D-055 says gap math runs over all dated records. The code keeps intake forms as endpoints and drops bills, phone notes, letters and records requests by kind. Which do you want: (a) every dated record is an endpoint and paperwork warns (a bill mid-span can then hide a gap, F4), or (b) paperwork is never an endpoint and a visible note names each paperwork record inside a span over 30 days?",
  "F2: is warning-only acceptable for the accident-date baseline, or must it skip paperwork? T-113 covers the conflict judge, not this baseline; who owns it?",
  "lib11 record 6 and gap_excluded_records (carried from r1 and r2): restore the pre-T-116 truth (encounter, excluded [4, 9]), or add an intake-form kind to the golden schema?"
 ]}
```
