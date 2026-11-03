# T-151 legal-nurse review (legal-nurse-reviewer, Linda Chen, RN, LNC persona)

Verdict: **pass** (0 blockers, 0 majors, 3 minors, 2 nits). Pinned commit 25f585c (HEAD at review start; contains b5f40c0 and 94c30db). I ran `git archive 25f585c` into the scratchpad (`t151-25f585c`) and served it on 127.0.0.1:7951 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratchpad DB. The server (PID 21724) was stopped by PID: `ps` exit 1, curl 000. Scripts, outputs and screenshots: `artifacts/review-evidence/T-151-legal-nurse/`. This reads what the tool tells the reader about what was and was not checked; it is not a clinical opinion on any record.

## The five checks you asked for

1. **Names exactly the checks that ran: yes.** lib08, lib11 and the sample list four checked kinds, and the on-screen list equals `GET case checks.conflict_types` labels (`probe.out.txt`). lib09 lists one (the clinician-name check); the three English-wording checks that read only part of the case are moved out of Checked into the skipped box, never listed as checked (`probe.out.txt` lib09: "What the conflict check covers (1 kind checked)", checked item "The same clinician named under two different practice names").
2. **Skipped checks with plain reasons and record numbers: yes.** lib09 shows three skipped items, each with "This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read." The Spanish records in the source are 2 (Consultorio nota), 4 (formulario OCR) and 7 (estado de cuenta) (`evals/library/case_lib09_spanish_interpreter_espalda.txt`), so the numbers are right. This closes my T-142 r1 major (the panel claimed a denial check ran on Spanish wording it cannot read). English-only cases (lib08, lib11, sample) show no skipped box.
3. **Notes are information, not conflicts: yes.** lib11: heading "Conflicts between records (2)" counts the two cards only; the "records predate the accident" line is a "Note" chip paragraph with no accept or dismiss, no item id, not counted (`lib11_priors_and_ledger-group.png`). It stays after I dismissed both conflicts.
4. **Always a "Not checked" line naming side and loss of consciousness: yes.** Present, always visible (not in a collapsed block) on lib08, lib09, lib11, sample, and on the all-skipped, stage-skipped and all-Spanish variants: "Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these."
5. **When nothing ran, it says so: yes.** I took a lib08 copy and removed its stored run summary in my scratchpad DB (the "analysed before the record of what ran was kept" shape): API `conflict_types: []`, four skipped NOT_RUN; the page reads "No conflict checks ran for this case. The reasons are listed below.", the coverage summary reads "(no checks ran)", no empty list and no "No conflicts found" (`probe2.out.txt` "nonerun"). A stage-skipped lib11 copy lists the two pair checks as skipped with "The run reached its time limit..." and keeps the two code checks as checked.

Deterministic: `tests/e2e/test_conflict_skipped.py` and `test_conflict_coverage.py` from the archive against my server: 14 passed (`e2e.out.txt`).

## Findings

**F-1 (minor). The lead sentence is the same on lib08 (four kinds ran) and on a case where one kind ran.** On lib09 and on an all-Spanish case the first line under the heading is "No conflicts found among the kinds checked. Other kinds of conflict are not checked." (`probe.out.txt`, `probe2.out.txt` "allspanish": one kind checked, three read no record). The skipped box sits right under it, so this is not the bare all-clear from GATE-M2, but a reader who stops at the first line gets the same assurance as on a full run. When nothing ran the page does add "The reasons are listed below" (`flags.js` `NONE_RAN` line); the partial case gets no such pointer. Fix: when `skipped` is not empty, end the lead with "N checks did not run or did not read every record; see below." Test: lib09 lead line contains "did not run" or "did not read"; lib08's does not.

**F-2 (minor). The notes line does not say which record.** lib11: "1 record predates the stated accident date, March 18, 2026. ..." The API carries `record_nos: [1]` and the page prints it nowhere (`probe.out.txt` lib11 API notes). The skipped items do print record numbers, so the paralegal gets numbers for one and has to hunt for the other. Fix: append "Record 1." (or "Records 1 and 3.") from `record_nos`. Test: lib11 note text contains "Record 1".

**F-3 (minor). Two "not checked" lists on one screen disagree.** The always-visible line is page-written and names loss of consciousness; the server's `not_checked` list (which the coverage block prints) still has dosage, left versus right, diagnosis, pain score, months and relative history, with no loss of consciousness line (`probe.out.txt` API not_checked). My T-142 F-2 asked for the server list to carry it. T-142's own AC says the text comes from the API so it cannot drift; this line can. Fix: add a `loc_history` entry to `NOT_CHECKED` in `conflict_candidates.py` and render the line from the list, or make the line a literal copy with a test that every named kind is in the server list. Test: lib08 `checks.not_checked` contains an LOC entry.

**F-4 (nit). Label and reason run together.** lib09 skipped item reads "...a later record where the course ended early This check reads English wording; ..." with no separator (`lib09_spanish_interpreter_espalda-group.png`). It also says "were not read" twice. Add a colon or line break; drop one of the two sentences.

**F-5 (nit). Note wording presumes.** "read them to check they are earlier care" assumes the record is earlier care. Server text (api.md T-141 r3). Better: "read them to check whether they are earlier care."

## What I ran

1. `git rev-parse --short HEAD` = 25f585c; `git archive 25f585c | tar -x -C <scratchpad>/t151-25f585c`; server on 7951 under `.venv/bin/python -I launch.py` (launcher in evidence dir); curl 200.
2. `probe.py`: sample (pasted) and lib08, lib09, lib11 (created through the API, opened at `#/case/<token>`): read the Conflicts group text, notes, skipped items, checked and not-checked items, compared with `GET /api/cases/{token}` `checks` and conflict flags; screenshots of each group.
3. `probe2.py`: three scratchpad-DB variants (no stored run summary; stage skipped; all records Spanish) for the "nothing ran" and partial cases.
4. `dismiss_probe.py`: dismissed both lib11 conflicts, re-read the group.
5. `exp.py`: lib09, lib08, lib11 with every entry accepted, export notes searched for conflict or coverage wording (only the lib11 flag lines match; no coverage line on any; see T-142 r2 F-1).
6. Pytest: 14 passed. Read: `app/frontend/flags.js` diff of b5f40c0 and 94c30db, `app/backend/conflict_candidates.py` `checks()`, `memory/contracts/api.md` checks paragraph, cards T-151 and T-142, `evals/library/case_lib09...txt`. Not exercised: live-model behavior (fixture only); narrow-screen layout (outside my lens).

```json
{"card": "T-151", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive 25f585c (HEAD at review start; includes b5f40c0, 94c30db) served on http://127.0.0.1:7951 (PID 21724, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; sample case plus library cases lib08, lib09 (Spanish), lib11 and three scratchpad-DB variants (no stored run summary, stage skipped, all Spanish)",
 "exercised": [
  "git archive 25f585c into a fresh scratchpad dir; server on 7951 via -I launcher; curl 200; stopped by PID 21724 (ps exit 1, curl 000)",
  "browser 1440x1000: sample, lib08, lib09, lib11 Conflicts group text, notes, skipped items, checked and not-checked items compared with GET case checks and conflict flags (probe.py); screenshots read: lib09 and lib11 groups",
  "three scratchpad-DB variants of run_checks (removed, stage skipped, all Spanish) to exercise 'no checks ran', STAGE_SKIPPED and LANGUAGE (probe2.py)",
  "dismissed both lib11 conflicts and re-read the group: note, skipped box and not-checked line stay (dismiss_probe.py)",
  "lib09, lib08, lib11 with every entry accepted, GET export, internal notes and letter searched for coverage wording (exp.py)",
  "tests/e2e/test_conflict_skipped.py and test_conflict_coverage.py from the archive against my server: 14 passed",
  "read flags.js diff of b5f40c0 and 94c30db, conflict_candidates.checks(), api.md checks paragraph, cards T-151 and T-142, library case lib09 source. Not exercised: live model (fixture only), narrow-screen layout"
 ],
 "verdict": "pass",
 "scores": {"names_checks_that_ran": 5, "skipped_reasons_and_records": 5, "notes_as_info_not_conflicts": 5, "not_checked_line_side_and_loc": 5, "nothing_ran_honesty": 5, "lead_sentence_honesty_on_partial_runs": 3, "no_inferred_dx_severity_causation": 5},
 "findings": [
  {"severity": "minor", "title": "Lead sentence 'No conflicts found among the kinds checked' is identical when four kinds ran and when one ran",
   "evidence": "probe.out.txt lib09: 'No conflicts found among the kinds checked. Other kinds of conflict are not checked.' above a box listing 3 skipped; probe2.out.txt allspanish: same line with 1 kind checked and 3 skipped LANGUAGE; flags.js NONE_RAN pointer ('The reasons are listed below.') is added only when conflict_types is empty",
   "why_it_matters": "A reader who stops at the first line gets the same assurance as on a full run, for a case where the English-wording checks read few or no records.",
   "fix": "When skipped is not empty, end the lead with 'N checks did not run or did not read every record; see below.'",
   "acceptance_test": "lib09 lead line contains 'did not run' or 'did not read'; lib08 lead line does not."},
  {"severity": "minor", "title": "Info note does not name the record it is about, though the API sends record_nos",
   "evidence": "probe.out.txt lib11 API notes record_nos [1], page text 'Note 1 record predates the stated accident date, March 18, 2026. ...' with no record number; skipped items do print 'Records 2, 4 and 7 were not read.'",
   "why_it_matters": "The paralegal has to search the case for the earlier record the note asks her to read.",
   "fix": "Append 'Record N.' from record_nos to the note line.",
   "acceptance_test": "lib11 note text contains 'Record 1'."},
  {"severity": "minor", "title": "Always-visible not-checked line is page-written and names loss of consciousness; the server's not_checked list does not",
   "evidence": "flags.js notCheckedLine (literal text); probe.out.txt API not_checked types dosage, laterality, diagnosis, pain_score, treatment_duration_months, informant_history (no loc); coverage block lists six items, none about loss of consciousness",
   "why_it_matters": "Two not-checked lists on one screen differ, and the page line can drift from what the server says (T-142 AC: text from the API; my T-142 F-2).",
   "fix": "Add a loc_history entry to NOT_CHECKED in conflict_candidates.py and print the line from the list, or test that every kind the line names is in the server list.",
   "acceptance_test": "lib08 GET case checks.not_checked contains a loss-of-consciousness entry."},
  {"severity": "nit", "title": "Skipped item label and reason run together; 'were not read' appears twice",
   "evidence": "lib09_spanish_interpreter_espalda-group.png: '...course ended early This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read.'",
   "why_it_matters": "Reads as one run-on sentence.",
   "fix": "Colon or line break after the label; keep one 'not read' sentence.",
   "acceptance_test": "Skipped item text has a separator between label and reason."},
  {"severity": "nit", "title": "Note wording presumes the record is earlier care",
   "evidence": "probe.out.txt lib11 note: 'read them to check they are earlier care.'",
   "why_it_matters": "Suggests the answer; the tool should only point to the record.",
   "fix": "'read them to check whether they are earlier care.'",
   "acceptance_test": "Note text contains 'whether'."}
 ],
 "whats_right": [
  "lib09 names the Spanish records (2, 4 and 7, correct against the source) as not read by each English-wording check and does not list those checks as checked.",
  "Notes render as a Note chip line with no flag controls and are not counted in the Conflicts heading; they survive dismissing the conflicts.",
  "When no check ran the page says 'No conflict checks ran for this case' with each reason and no empty list or 'No conflicts found'."
 ],
 "questions_for_chris": []}
```
