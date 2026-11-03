# T-142 legal-nurse re-check, round 2 (legal-nurse-reviewer, Linda Chen, RN, LNC persona)

Verdict: **pass** (0 blockers, 0 majors, 2 minors carried from round 1). Pinned commit 25f585c (HEAD at review start). Same run as T-151: `git archive 25f585c`, fixture backend, `ZLAYT_MODE=local`, scratchpad DB, 127.0.0.1:7951, server PID 21724 stopped by PID (`ps` exit 1, curl 000). Evidence: `artifacts/review-evidence/T-151-legal-nurse/`. Round 1 is `reviews/T-142-legal-nurse.md` (changes: 1 major, 3 minors). This is a read of what the tool tells the reader about coverage, not a clinical opinion.

## Round 1 findings, one by one

- **F-1 major (Spanish case lists English-only checks as run): fixed.** lib09 now lists the plan-vs-early-end, denial-vs-history and accident-date checks under "Did not run on this case, or not on every record (3)" with "This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read." Checked shows one kind (clinician name). Records 2, 4 and 7 are the Spanish ones in the source (`evals/library/case_lib09_spanish_interpreter_espalda.txt`; record 4 is the "Accidentes anteriores? Si [ ] No [X]" form I probed in round 1). The same sentence is absent on lib08, lib11 and the sample. An all-Spanish variant says "every record is in Spanish, so it could not find anything." (`probe.out.txt`, `probe2.out.txt`). The fix is at the source (T-141 r2 `checks.skipped[]`) plus the UI render (T-151). Acceptance test from round 1 met.
- **F-2 minor (loss of consciousness not named): fixed on screen, open at the source.** lib08 shows "Not checked: left versus right across records, a change in loss of consciousness history between records, ..." always visible. The server list is unchanged (`not_checked` types: dosage, laterality, diagnosis, pain_score, treatment_duration_months, informant_history), so the coverage block's list still has no loss of consciousness line (see T-151 F-3; open as minor).
- **F-3 minor (others-not-checked hidden when conflicts show): fixed.** On the sample and lib11 the not-checked line sits outside the collapsed coverage block, visible with two conflicts listed.
- **F-4 minor (export internal notes carry no coverage line): still open.** lib09, lib08 and lib11 with every entry accepted: internal notes headings are FLAGS ACCEPTED, FLAGS DISMISSED, AMOUNTS NOT TOTALED, RECORDS NOT IN THE TREATMENT SECTION, EDITED ITEMS, PENDING ITEMS NOT INCLUDED; no line mentions what the conflict check covered or skipped (`export.out.txt`). The T-151 handoff says "coverage line in internal notes is backend"; no open card I could find in `board.py list` names it (T-141 is in progress, its AC is the lib11 case). It stays minor because the card's AC covers the screen only; the point is unchanged: off the screen the notes say nothing about coverage, including "Records 2, 4 and 7 were not read" on lib09.

Round 1 positives still hold: the empty state is never a bare "No conflicts found." (lib08 reads "No conflicts found among the kinds checked. Other kinds of conflict are not checked."), and the checked list on screen equals the API list. Deterministic: `test_conflict_coverage.py` with `test_conflict_skipped.py`: 14 passed against my server; the real-backend variant now runs.

New observation from T-151 that touches this card (minor, filed there as F-1): on lib09 and an all-Spanish case the lead sentence is the same as on a full run; the skipped box under it carries the difference.

## What I ran

See `reviews/T-151-legal-nurse.md` and the evidence dir for the full list. For this card: lib08, lib09, lib11 and the sample in a browser (Conflicts group text against `GET case checks`); export of lib09, lib08, lib11 with every entry accepted (`exp.py`, `export.out.txt`); pytest 14 passed; read cards T-142 and T-151, `flags.js`, `conflict_candidates.checks()`.

```json
{"card": "T-142", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "round 2 re-check; git archive 25f585c (includes c5c18a6, b5f40c0, 94c30db) served on http://127.0.0.1:7951 (PID 21724, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; sample case plus lib08, lib09 (Spanish), lib11",
 "exercised": [
  "git archive 25f585c into a fresh scratchpad dir; server on 7951; curl 200; stopped by PID 21724 (ps exit 1, curl 000)",
  "browser: sample, lib08, lib09, lib11 Conflicts group text compared with GET /api/cases/{token} checks (probe.py in artifacts/review-evidence/T-151-legal-nurse/)",
  "scratchpad-DB variants: no stored run summary, stage skipped, all-Spanish run summary (probe2.py)",
  "lib09, lib08, lib11 with every entry accepted: GET export, internal notes and letter searched for coverage wording (exp.py, export.out.txt)",
  "tests/e2e/test_conflict_coverage.py and test_conflict_skipped.py from the archive against my server: 14 passed",
  "read reviews/T-142-legal-nurse.md, cards T-142 and T-151, flags.js, conflict_candidates.checks(), lib09 source. Not exercised: live model, narrow-screen layout"
 ],
 "verdict": "pass",
 "scores": {"conflict_coverage_disclosure": 5, "empty_state_honesty": 4, "api_sourced_text": 4, "spanish_honesty": 5, "no_inferred_dx_severity_causation": 5},
 "findings": [
  {"severity": "minor", "title": "Round 1 F-4 still open: export internal notes carry no conflict-coverage line",
   "evidence": "export.out.txt: lib09 and lib08 'lines with conflict/checked/not checked: []'; headings FLAGS ACCEPTED, FLAGS DISMISSED, AMOUNTS NOT TOTALED, RECORDS NOT IN THE TREATMENT SECTION, EDITED ITEMS, PENDING ITEMS NOT INCLUDED; T-151 handoff: 'coverage line in internal notes is backend'; no board card in `board.py list` names it",
   "why_it_matters": "Once she leaves the screen the notes say nothing about what the conflict check covered, including the Spanish records it did not read.",
   "fix": "One internal-notes line from the same checks: 'Conflict check covered: ...; did not run on: ...; not checked: ...', with record numbers for skipped items. Open a backend card.",
   "acceptance_test": "lib09 export internal_notes_text contains that line naming Records 2, 4 and 7; an English-only case lists no skipped records."},
  {"severity": "minor", "title": "Round 1 F-2 open at the source: server not_checked list has no loss of consciousness entry; the page line is literal text",
   "evidence": "probe.out.txt API not_checked types dosage, laterality, diagnosis, pain_score, treatment_duration_months, informant_history; flags.js notCheckedLine literal text names loss of consciousness",
   "why_it_matters": "The T-142 AC says the text comes from the API so it cannot drift; the line that names loss of consciousness does not.",
   "fix": "Add loc_history to NOT_CHECKED in conflict_candidates.py and render the line from the list.",
   "acceptance_test": "lib08 GET case checks.not_checked contains a loss-of-consciousness entry."}
 ],
 "whats_right": [
  "lib09 no longer lists the English-wording checks as checked: three skipped items name Records 2, 4 and 7 (correct against the source).",
  "The not-checked line naming side and loss of consciousness is visible with and without conflicts on every case I opened.",
  "The empty state is never a bare 'No conflicts found.' and the checked list on screen equals the API list."
 ],
 "questions_for_chris": []}
```
