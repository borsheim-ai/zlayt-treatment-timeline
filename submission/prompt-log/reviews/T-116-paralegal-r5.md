# T-116 round 5 review: paralegal-reviewer (Maria Delgado persona)

Commit under review: f8f358e (HEAD; `git log --oneline -1` = f8f358e, subject "fix(backend): T-116 r5 paperwork warning is header-only; text evidence never suppresses it (D-055)"). The diff touches app/backend/gaps.py (the text-evidence test is removed from admin_label), tests/unit/test_t116_r4_all_dated_records.py and tests/unit/test_t116_r5_header_only_warning.py. Both trees were extracted with git archive into the scratchpad (t116r5/head = f8f358e, t116r5/pre = 3e3f3b7). Nothing was run against the dirty project tree except the pytest line noted below.

## Verdict: changes (0 blockers, 1 major, 1 minor carried, 1 nit)

The r4 blocker (F1) is closed. A paperwork record now shows the 40-day span, the alternative and the conditional flag whether or not its text carries a diagnosis line, 'performed' or 'seen by'. lib06 keeps its 35-day flag with the Diagnosis line. The r1 to r3 invented-gap checks still pass.

The accident baseline is only partly fixed. It is right for a single paperwork record, but it still calls a paperwork-headed record part of the "first recorded treatment" in two cases the fix does not reach (M1). That is a major, not a blocker: no date, visit or amount is invented, and the flag is internal for the paralegal to decide.

## Chris's four checks

1. **All 8 paperwork variants show the span and the alternative, including diagnosis, 'performed' and 'seen by' lines: PASS.** Eight of eight rows MID-SPAN `[(40, True, ['inside'])]` and ENDS-GAP `[(40, False, ['end'])]`. At 8b4ff11 six of those rows were NONE. My own probe covers five paperwork headers times four text variants (plain, Dx line, 'performed', 'seen by'): 20 of 20 carry the alternative sentence ("the gap would be 40 days" mid-span, "there would be no visit after it" at the end).
2. **lib06 keeps its 35-day flag with the Diagnosis line: PASS.** With 'Diagnosis: M25.511 pain in right shoulder.' added to record 4, the flag is still `('2026-05-13', '2026-06-17', 35, True, ['inside'])`, the same as the committed packet.
3. **Accident baseline never calls a paperwork-headed record 'first recorded treatment': PARTIAL, FAIL on two cases.** Single paperwork record, 20 of 20 variants: pass. Same-day paperwork plus visit, and some paperwork headers outside the admin list: fail (M1).
4. **r1 to r3 probes still create no invented gaps: PASS.** 60 of 60 label runs count gap rows [19, 21] and no visit label draws a flag. The Appendix A 73-day flag is in 10 of 10 fax variants. The r3 warning-and-API output is identical to the r4 record after path normalisation.

Also run: pytest on the HEAD copy, `-k gap`: 270 passed (also 270 passed in the project tree). The three T-116 test files by path: 184 passed on the HEAD copy and in the project tree. The r5 test file's accident-baseline test passes but covers only one record on its own date; that is why M1 is not caught.

## Findings

**M1 (major). The accident baseline still calls a paperwork-headed record part of the "first recorded treatment" when (a) a paperwork record and a visit share the earliest date, or (b) the header is not on the admin list.**
- Evidence: `artifacts/review-evidence/T-116-paralegal-r5-probe.out.txt` section B2. Paperwork first: "Stated accident date January 15, 2026 (“Date of accident: 2026-01-15”) is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form; Capital PT, initial evaluation)." Visit first: "...the first recorded treatment, January 12, 2026 (Capital PT, initial evaluation; Capital PT, intake form)." For (b), `artifacts/review-evidence/T-116-paralegal-r5-headers.out.txt`: "Capital PT, questionnaire admin_label=None first_recorded_treatment=True looks_like_paperwork=False"; the same for "Capital PT, authorization request". Code: `app/backend/conflicts.py:64-65` takes the paperwork branch only when every record on the earliest date is admin (`if all(gaps.admin_label(r) for r in first_recs):`); otherwise `app/backend/flag_templates.py:146` names every first-date source in the "first recorded treatment" sentence. The admin header list is `app/backend/gaps.py:19-22`, which has no bare 'questionnaire' or 'authorization request'. `tests/unit/test_t116_r5_header_only_warning.py`, last test, uses one paperwork record with no visit on its date, so it cannot see either case.
- Why it matters: the check Chris set is that the baseline never calls a paperwork-headed record the first recorded treatment. The reading of D-017 and R-FL-2 used in r4 (a non-treatment record is not stated as the first recorded treatment) and D-055 both say the same. An adjuster who reads "first recorded treatment, Capital PT, intake form" will point at it. I rate it major because the date is a real encounter date and no fact is invented; the flag is internal and the paralegal decides before export. I escalate r4 F2 from minor to part of this major because the header-only change does not reach this branch and the new test is shape-bound (one record, one date).
- Fix: (a) in `conflicts.py:64-65`, when the earliest date holds a paperwork-headed record and a visit, do not name the paperwork record in the "first recorded treatment" sentence. Either name only the visit source, or use the `_acc_after_paperwork` wording (the record looks like paperwork, the first recorded visit is ..., the stated date is ... later than it). (b) add the bare headers 'questionnaire' and 'authorization request' (and any others qa lists) to the header-only admin list at `gaps.py:19-22`. Keep the decision header-only. (c) add unit tests through `conflicts.accident_date_conflicts` for the same-day case in both record orders and for a 'Capital PT, questionnaire' header.
- Acceptance test: re-run `artifacts/review-evidence/T-116-paralegal-r5-probe.py` on the new HEAD: section B2 prints no sentence that names 'Capital PT, intake form' as part of the first recorded treatment, in either order. Re-run `T-116-paralegal-r5-headers.py`: `first_recorded_treatment=False` for all 11 headers. The new unit tests pass.

**m2 (minor, carried from r4 F3, still open). The committed golden truth and the lexicon text still encode the exclusion the product dropped.**
- Evidence: `app/llm/lexicon.yaml:1282` is unchanged: "ADR-010 / D-003: records whose source label matches are excluded from gap arithmetic. They still become entries." `artifacts/review-evidence/T-116-paralegal-r5-packet-flags.out.txt` line 2: "case_lib10_eob_ub04_cms1500 OK pre [('2026-07-08', '2026-08-26', 49)] exp [('2026-07-08', '2026-08-26', 49)] head [('2026-07-14', '2026-08-26', 43)]". The expected truth still counts 49; HEAD counts 43 and shows 49 as the alternative.
- Why it matters: a future check can pass a wrong counted row. The visit-only reading is still what the product shows as its alternative, so no flagged gap is lost today. This does not drive the verdict.
- Fix: qa names the visit-only table as such and adds a counted table that the product test compares; researcher rewrites the consumer text at `lexicon.yaml:1282` to match the header-only rule.
- Acceptance test: `rg 'excluded from gap arithmetic' app/llm/lexicon.yaml` returns nothing; a unit test compares the counted rows of all 25 packets to a committed counted table.

**n3 (nit, carried from r4 F4). When the paperwork's own text states the service dates, the headline still leads with the counted number.**
- Evidence: `T-116-paralegal-r5-packet-flags.out.txt` line 52: "# case_lib10_eob_ub04_cms1500 2026-07-14 2026-08-26 43 [8, 9]". Record 8 in `evals/library/case_lib10_eob_ub04_cms1500.txt` reads "dates of service 06/24/2026 and 07/08/2026".
- Why it matters: I have to open record 8 to see which reading the records support. D-055 forbids the tool choosing, so a pointer is enough.
- Fix: optional. A one-line pointer to the stated service dates next to the alternative.

## What is right

1. The header-only change does what D-055 asks. Eight of eight r4 paperwork rows and 20 of 20 header-by-text variants show the span, the alternative and the conditional flag, with no change in the wording of the warning. The r3 warning-and-API output is identical to the r4 record.
2. lib06's 35-day conditional flag survives the added Diagnosis line, and the 60-run visit-label sweep still counts every dated record with no invented gap. Appendix A keeps its 73-day flag in all 10 fax variants, and the 28-day interval is not flagged.
3. The baseline sentence for a single paperwork record names the paperwork record, gives the first-visit alternative, and does not choose a date: `artifacts/review-evidence/T-116-paralegal-r4-baseline.out.txt` B1 and B2 both now read "looks like paperwork, not a visit".

## Outside my lens

- The r3 probe prints "llm call failed ... step=extract" on stderr for both trees. The packet statuses (done, done_with_errors for case_lib01) are the same on 3e3f3b7 and f8f358e, so this is not a T-116 change. Not scored.
- Whether the same-day sentence should name the paperwork record at all is wording for Chris and the litigation lead. I only say it must not call paperwork treatment.

## Not done

- The running app at localhost:7860 was not driven. `scores.verify_quickly` is therefore not scored (D-015 applies to reviews of the running app).

```json
{"card": "T-116", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f8f358e (HEAD, T-116 r5, D-055 header-only) vs pre-T-116 parent 3e3f3b7; git archive copies in the scratchpad (t116r5/head, t116r5/pre); app/backend/gaps.py, conflicts.py, flag_templates.py, lexicon.yaml:1282; tests/unit/test_t116_r5_header_only_warning.py; sample case and 25 golden and library packets; the running app at localhost:7860 was not driven",
 "exercised": [
  "read personas/paralegal.md, reviews/T-116-paralegal-r4.md, D-055 (memory/ORCHESTRATOR_DECISIONS.md:63), D-017 (memory/ORCHESTRATOR_DECISIONS.md:25), R-FL-2 (spec/REQUIREMENTS.md:66), memory t116-gap-endpoint-patterns",
  "git log --oneline -1 -> f8f358e; git show --stat f8f358e (gaps.py, test_t116_r4_all_dated_records.py, test_t116_r5_header_only_warning.py); git show f8f358e -- app/backend/gaps.py",
  "git archive f8f358e -> scratchpad t116r5/head; git archive 3e3f3b7 -> scratchpad t116r5/pre",
  "artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py on HEAD: all 8 rows MID-SPAN [(40, True, ['inside'])] and ENDS-GAP [(40, False, ['end'])] (six rows were NONE at 8b4ff11)",
  "T-116-paralegal-r4-packet-dx-line.py on HEAD: lib10 unchanged; lib06 record 4 with 'Diagnosis: M25.511 pain in right shoulder.' keeps ('2026-05-13', '2026-06-17', 35, True, ['inside'])",
  "T-116-paralegal-r4-baseline.py on HEAD: B1 and B2 both print 'looks like paperwork, not a visit'; no 'first recorded treatment' sentence",
  "NEW artifacts/review-evidence/T-116-paralegal-r5-probe.py (out.txt): section A 20 of 20 header-by-text variants show MID [(40, True, ['inside'])] with alternative 40 and the sentence 'the gap would be 40 days', and ENDS [(40, False, ['end'])] with 'there would be no visit after it'; section B 20 of 20 single-record baselines pass; section B2 same-day case FAILS (M1)",
  "NEW artifacts/review-evidence/T-116-paralegal-r5-headers.py (out.txt): 11 paperwork-looking headers as earliest record; 'Capital PT, questionnaire' and 'Capital PT, authorization request' give admin_label=None and first_recorded_treatment=True (M1 b)",
  "T-116-paralegal-r3-probe.py run on HEAD and 3e3f3b7 (JSON in the scratchpad); NEW T-116-paralegal-r5-labels-check.py (out.txt): 60 of 60 label runs count gap rows [19, 21]; visit labels draw no flag; controls 'Capital PT, intake form' and 'Dr. Lee, chiropractic, billing statement' warn 40 inside",
  "NEW T-116-paralegal-r5-appx-check.py (out.txt): Appendix A control and 9 treatment records with ', fax': 73-day flag 2026-03-06 to 2026-05-18 in 10 of 10; 28-day interval unflagged",
  "T-116-paralegal-r3-warn-and-api.py on HEAD: output identical to artifacts/review-evidence/T-116-paralegal-r4-warn-and-api.head.out.txt after path normalisation (diff exit 0)",
  "T-116-paralegal-r4-packet-flags.py over HEAD and pre JSON -> NEW T-116-paralegal-r5-packet-flags.out.txt: 0 MISSING rows; 22 of 25 counted lists identical; lib10 49 to 43 with 49 shown as alternative; case_09 and lib06 now conditional",
  "pytest, HEAD copy: .venv/bin/python -I -m pytest -q tests/unit -k gap -p no:cacheprovider -> '270 passed, 2500 deselected in 3.12s' (T-116-paralegal-r5-pytest-gap-head.out.txt); project tree, same command -> '270 passed, 2500 deselected in 4.73s'",
  "pytest, HEAD copy: test_t116_gap_endpoints.py + test_t116_r4_all_dated_records.py + test_t116_r5_header_only_warning.py -> '184 passed in 1.46s' (T-116-paralegal-r5-pytest-t116-files-head.out.txt); project tree -> '184 passed in 1.49s'",
  "app/llm/lexicon.yaml:1282 grep on HEAD: 'excluded from gap arithmetic' still present (r4 F3 open)",
  "NOT DONE: running app at localhost:7860 not driven; scores.verify_quickly not scored"
 ],
 "verdict": "changes",
 "scores": {"paperwork_text_never_suppresses_warning": 5, "lib06_35_day_flag_with_dx_line": 5, "accident_baseline_never_calls_paperwork_treatment": 2, "no_invented_gap_r1_r3": 5, "golden_truth_consistency": 3},
 "findings": [
  {"severity": "major",
   "title": "Accident baseline still calls a paperwork-headed record part of the first recorded treatment when a paperwork record and a visit share the earliest date, or the header is not on the admin list",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r5-probe.out.txt section B2: 'is later than the first recorded treatment, January 12, 2026 (Capital PT, intake form; Capital PT, initial evaluation)' (paperwork first) and '(Capital PT, initial evaluation; Capital PT, intake form)' (visit first). artifacts/review-evidence/T-116-paralegal-r5-headers.out.txt: 'Capital PT, questionnaire admin_label=None first_recorded_treatment=True looks_like_paperwork=False'; same for 'Capital PT, authorization request'. app/backend/conflicts.py:64-65 (paperwork branch only if all first-date records are admin); app/backend/flag_templates.py:146 (names every first-date source); app/backend/gaps.py:19-22 (no bare questionnaire or authorization request); tests/unit/test_t116_r5_header_only_warning.py last test covers one record only.",
   "why_it_matters": "The check is that the accident baseline never calls a paperwork-headed record the first recorded treatment. The single-record cases pass (20 of 20), but the same-day case names the intake form as part of the treatment, and a questionnaire or authorization request is called first treatment with no caveat. The r4 reading of D-017 and R-FL-2, and D-055, say a non-treatment record is not stated as treatment. Rated major, not blocker: the date is a real encounter date, no fact is invented, and the flag is internal for the paralegal to decide. r4 F2 is escalated into this finding because the header-only change does not reach this branch and the new test is shape-bound.",
   "fix": "(a) conflicts.py:64-65: when the earliest date holds a paperwork-headed record and a visit, do not name the paperwork record in the first-recorded-treatment sentence; name only the visit source, or use the _acc_after_paperwork wording. (b) gaps.py:19-22: add bare 'questionnaire' and 'authorization request' (and any others qa lists) to the header-only admin list; keep it header-only. (c) unit tests through conflicts.accident_date_conflicts for the same-day case in both record orders and for a 'Capital PT, questionnaire' header.",
   "acceptance_test": "Re-run artifacts/review-evidence/T-116-paralegal-r5-probe.py on the new HEAD: section B2 prints no sentence naming 'Capital PT, intake form' as part of the first recorded treatment, in either order. Re-run T-116-paralegal-r5-headers.py: first_recorded_treatment=False for all 11 headers. New unit tests for both cases pass."},
  {"severity": "minor",
   "title": "Committed golden truth and lexicon text still encode the exclusion the product dropped (carried from r4 F3, still open)",
   "evidence": "app/llm/lexicon.yaml:1282 unchanged: 'ADR-010 / D-003: records whose source label matches are excluded from gap arithmetic.' artifacts/review-evidence/T-116-paralegal-r5-packet-flags.out.txt line 2: 'case_lib10_eob_ub04_cms1500 OK pre [(2026-07-08, 2026-08-26, 49)] exp [(2026-07-08, 2026-08-26, 49)] head [(2026-07-14, 2026-08-26, 43)]'.",
   "why_it_matters": "The expected counted truth for lib10 still reads 49; HEAD counts 43 and shows 49 as the alternative. A future check can pass a wrong counted row. No flagged gap is lost today, so this does not drive the verdict.",
   "fix": "qa names the visit-only table as such and adds a counted table the product test compares; researcher rewrites the consumer text at lexicon.yaml:1282 to match the header-only rule.",
   "acceptance_test": "rg 'excluded from gap arithmetic' app/llm/lexicon.yaml returns nothing; a unit test compares the counted rows of all 25 packets to a committed counted table."},
  {"severity": "nit",
   "title": "When the paperwork's own text states the service dates, the headline still leads with the counted number (carried from r4 F4)",
   "evidence": "artifacts/review-evidence/T-116-paralegal-r5-packet-flags.out.txt line 52: '# case_lib10_eob_ub04_cms1500 2026-07-14 2026-08-26 43 [8, 9]'. evals/library/case_lib10_eob_ub04_cms1500.txt record 8: 'dates of service 06/24/2026 and 07/08/2026'.",
   "why_it_matters": "The paralegal has to open record 8 to see which reading the records support. A pointer would be enough; D-055 forbids the tool choosing.",
   "fix": "Optional: a one-line pointer to the stated service dates beside the alternative.",
   "acceptance_test": "Optional: lib10 explanation names the 07/08/2026 service date from record 8."}
 ],
 "whats_right": [
  "The header-only change closes r4 F1: 8 of 8 r4 paperwork rows and 20 of 20 header-by-text variants show the span, the alternative and the conditional flag; the lib06 35-day flag survives the Diagnosis line.",
  "No invented gap: 60 of 60 visit-label runs count gap rows [19, 21] with no flag; Appendix A keeps its 73-day flag in 10 of 10 fax variants; the r3 warning and API output is identical to the r4 record.",
  "A single paperwork record in the accident baseline names the paperwork record, gives the first-visit alternative, and does not choose a date."
 ],
 "questions_for_chris": [
  "M1: when a paperwork record and a visit share the earliest date, should the baseline name the paperwork record at all, or only the visit? I only require that it never calls the paperwork record treatment.",
  "M1(b): is the admin header list closed by design? 'questionnaire' and 'authorization request' are paperwork headers a paralegal would call paperwork."
 ]}
```
