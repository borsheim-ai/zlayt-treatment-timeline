# Subagent: Backend: one neutral date label (Backend: one neutral date label)

Source: `agent-a641ccf0183c9acdf.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T15:08:30.285Z

You are a backend worker in /Users/arsis/zlayt-pm-project on T-202 (fast, D-075). Read "D-073 label simplification" in memory/ORCHESTRATOR_DECISIONS.md and reviews/T-202-paralegal-r7.md.

Every charge line's blank must read exactly "date of service [__________] (record dated X)". Remove the "statement dated" variant and the bill/record classification behind it. Update:
- `service_date.date_label` (always "record dated");
- export.py;
- evals/letter_check.py (accept only that exact form);
- the sample golden;
- spec/REQUIREMENTS.md §6, so `--check-spec` stays true. Run it from an archive copy, since it rewrites latest.json;
- api.md;
- the frontend Step 3 copy, if it hard-codes "statement dated"; the orchestrator authorizes that edit.

Run targeted tests from a `git archive`: letter_check, the date unit files, the export goldens, the guided test_step3/t205/t206, and the spec check. Stage with a temp index and commit with `git commit`. Move the card to in_review and reply in 1 line.

### User / tool · 2026-11-03T15:08:30.292Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:08:32.133Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-073 label simplification\" -A25 memory/ORCHESTRATOR_DECISIONS.md | head -60; grep -rn \"statement dated\" --include=* -l . 2>/dev/null | grep -v \"^./.git/\" | head -40"
}
````

### User / tool · 2026-11-03T15:08:44.544Z

**tool result**
````
113:- D-073 label simplification (T-202 r7): the blank's parenthetical no longer classifies the source; every charge line reads "date of service [__________] (record dated X)". Classifying bill vs clinical record from excerpt words misfired ("ER charges:" on a clinical record printed "statement dated"); one neutral label cannot be wrong.
artifacts/review-evidence/T-015-r2-paralegal-probe.out.txt
artifacts/review-evidence/GATE-M3M4-paralegal-case09-trace.txt
artifacts/review-evidence/T-209-r4-paralegal-draft.md
artifacts/review-evidence/T-209-r4-paralegal-summary.txt
artifacts/review-evidence/GATE-M3M4-paralegal-lib10-letter.txt
artifacts/review-evidence/T-209-step3-walk.json
artifacts/review-evidence/T-209-paralegal-note-probe.json
artifacts/review-evidence/T-209-r3-paralegal-body-clip.json
artifacts/review-evidence/T-209-r3-paralegal-draft.md
artifacts/review-evidence/GATE-M3M4-paralegal-lib11-trace.txt
artifacts/review-evidence/T-209-r3-paralegal-walk.json
artifacts/review-evidence/GATE-M3M4-paralegal-lib11-letter.txt
artifacts/review-evidence/T-209-r3-paralegal-body-clip.py
artifacts/review-evidence/GATE-M3M4-paralegal-case09-letter.txt
artifacts/review-evidence/GATE-M3M4-paralegal-lib10-trace.txt
artifacts/review-evidence/T-055-security-r2/head_670ed09/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-209-r4-paralegal-walk.json
artifacts/review-evidence/T-055-security-r2/head_670ed09/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/tree/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/tree/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/mut_imbgri0q/t/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/mut_imbgri0q/t/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/mut_1t21rje5/t/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/mut_1t21rje5/t/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/mut_qckojlrz/t/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/mut_qckojlrz/t/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/mut_d4rb06f3/t/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/mut_d4rb06f3/t/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/mut_ycbac4d9/t/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/mut_ycbac4d9/t/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/mut_pxrrbjqz/t/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/mut_pxrrbjqz/t/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/mut_g4uj8ykw/t/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/mut_g4uj8ykw/t/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/mut_cpkf6rlj/t/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/mut_cpkf6rlj/t/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/mut_ly_zzj54/t/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/mut_ly_zzj54/t/tests/unit/test_amounts.py
artifacts/review-evidence/T-057-staff-engineer-r2/mut_da2gkblv/t/evals/golden/case_09_nonvisit_hides_gap.expected.json
artifacts/review-evidence/T-057-staff-engineer-r2/mut_da2gkblv/t/tests/unit/test_amounts.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:08:48.525Z

**tool call — Bash**
````
{
 "command": "git status --short | head; grep -rn \"statement dated\\|date_label\\|record dated\" app evals/*.py spec/REQUIREMENTS.md memory/contracts/api.md tests --include=* -I 2>/dev/null | grep -v \"\\.json:\" | head -80; python3 tools/board.py show T-202 | head -5"
}
````

### User / tool · 2026-11-03T15:08:48.823Z

**tool result**
````
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
app/llm/lexicon.yaml:1339:      - id: accident_date_label
app/frontend/guided/step3.js:24:  /* T-211 (T-202 r6): service_date.date_label says what the record's date is called: "statement" for a bill, "record" for any other record. No service_date (a ledger line not counted yet) is a bill document's: "statement". */
app/frontend/guided/step3.js:25:  const dateWord = (sd) => (sd && sd.date_label === "record" ? "record" : "statement");
app/frontend/guided/step3.js:128:      return d && /^reviewer:counted/.test(by || "") ? `No date of service (statement dated ${d})` : d;          // a ledger line she counted states no date of service: the record's date is the statement's
app/backend/store.py:120:    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or the fillable blank 'date of service [__________] (statement dated June 15, 2026)'
app/backend/store.py:144:            "statement_date_iso": rd, "date_label": SD.date_label(kind), "reason": r["reason"], "confirm_note": note}
app/backend/export.py:212:        date of service [__________] (statement dated June 15, 2026)' (a bill's own date is its statement date, any other record's its record date). The code extracts no service date for
app/backend/conflicts.py:11:# T-141 r6 / D-061: one closed exemption. A stated accident date later than the earliest record is a conflict when a record dated before it has ANY accident or
app/backend/service_date.py:12:'date of service [__________] (statement dated X)' on a bill, '(record dated X)' on any other record, and the Step 3 note; the paralegal fills it from the quote. The result of `resolve` is one of:
app/backend/service_date.py:114:def date_label(kind: str) -> str:
app/backend/service_date.py:121:    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)' on a bill, '(record dated June 15, 2026)' on any other record."""
app/backend/service_date.py:123:        return f"{BLANK} ({date_label(kind)} dated {display(statement_iso)})"
evals/letter_check.py:16:form, 'date of service [__________] (statement dated X)' on a bill or '(record dated X)' on any other record, X the record's own date. A printed date, period or any other form is a violation.
evals/letter_check.py:215:    '<source label>, date of service [__________] (statement dated June 15, 2026)' when the record is a bill, '(record dated June 15, 2026)' for any other record, and no parenthesis when the
tests/unit/test_t200_undated_charge_label.py:3:chronology that puts the clinic's visit on March 27. The letter now says 'itemized ledger, date of service [__________] (statement dated June 15, 2026)'. A charge that states
tests/unit/test_t200_undated_charge_label.py:13:STATEMENT = "Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): "
tests/unit/test_t200_undated_charge_label.py:34:    assert "Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026): $3,260.00" in lines          # D-073: an ED provider name is not a document type, so no record date
tests/unit/test_t200_undated_charge_label.py:78:    assert line(dos_iso=None, dos_end_iso=None) == "Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00"
tests/unit/test_t200_undated_charge_label.py:79:    blank = "Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00"
spec/REQUIREMENTS.md:260:Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00
spec/REQUIREMENTS.md:262:Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00
tests/unit/test_amounts.py:99:    "Per statement dated 2026-03-01, charge: $400",
tests/unit/test_t141_r3_variants.py:1:"""T-141 round 3: a record dated before the stated accident date is an earlier visit (info only) when it has no injury, mechanism or accident vocabulary, or
tests/unit/test_t202_r7_all_blank.py:2:every charge line prints the fillable blank 'date of service [__________] (statement|record dated X)', Step 3 carries the same text, and evals/letter_check accepts that form and nothing else.
tests/unit/test_t202_r7_all_blank.py:29:    assert d["text"] == f"date of service [__________] ({kind} dated June 15, 2026)" and d["date_label"] == kind
tests/unit/test_t202_r7_all_blank.py:48:    assert f"{LEDGER}, date of service [__________] (statement dated June 15, 2026): $250.00" in out["letter_text"].split("\n")
tests/unit/test_t202_r7_all_blank.py:58:BLANK_OK = f"{LEDGER}, date of service [__________] (statement dated June 15, 2026)"
tests/unit/test_t202_r7_all_blank.py:64:    assert _check(f"{NOTE}, date of service [__________] (record dated June 15, 2026)", NOTE, "Exam charge $250.00.") == []
tests/unit/test_t202_r7_all_blank.py:65:    for bad in (f"{LEDGER}, June 15, 2026", f"{LEDGER}, March 27, 2026", f"{LEDGER}, June 9–12, 2026", f"{LEDGER}, date of service [__________] (statement dated June 16, 2026)",
tests/unit/test_t202_r7_all_blank.py:66:                f"{LEDGER}, date of service [__________] (record dated June 15, 2026)", f"{LEDGER}, date of service [__________]", f"{LEDGER}, date of service [__________] (statement dated June 15, 2026) x",
tests/unit/test_t202_r7_all_blank.py:67:                f"{LEDGER}, date of service [_________] (statement dated June 15, 2026)", f"Other, date of service [__________] (statement dated June 15, 2026)"):
tests/unit/test_t202_r7_all_blank.py:69:    assert _check(f"{NOTE}, date of service [__________] (statement dated June 15, 2026)", NOTE, "Exam charge $250.00.")          # an encounter record's date is its record date
tests/unit/test_t202_r7_all_blank.py:77:    dated = got["letters"]["standard"].replace("date of service [__________] (record dated January 9, 2026)", "January 9, 2026")
tests/unit/test_t141_d061_closed_exemption.py:1:"""T-141 r6 / D-061: a record dated before the stated accident date is info-only ONLY when every accident or mechanism word in it is governed by an explicit
memory/contracts/api.md:141:**T-141 / T-142, `checks` (GET case, top level; always present; computed per case from what the run did, no model):** what the conflict check looked for on THIS case and what it did not, so the UI can say it honestly ("Checked for: ... Not checked: ..."; never "no conflicts found" without it). `{conflict_types: [..], labels: {<type>: one plain sentence}, skipped: [{type, label, reason_code, reason, record_nos?}], not_checked: [{type, label}], notes: [{type, code, count, record_nos, stated_date, text}]}`. The four types are `plan_vs_early_end` and `denial_vs_history` (pair rules in `conflict_candidates.py`; a judge classifies each pair), `accident_date` and `provider_name` (structural checks in `conflicts.py`). **`conflict_types` lists only the types that ran on the case**; `labels` has all four. **`skipped`** says why a type did not run, or ran only in part. `reason_code`: `NOT_RUN` (case created, comparison between records not run yet; the two code checks ran at ingest), `STAGE_SKIPPED` (the run hit its time limit before the comparison between records), `RUN_FAILED` (the run stopped; nothing known), `LANGUAGE` (every record is Spanish, uncertain or unsupported: the English wording rules could not find anything; the type is absent from `conflict_types`), `LANGUAGE_PARTIAL` (the type ran, but `record_nos` lists the Spanish/uncertain/unsupported records it did not read), `NO_DATED_RECORD` (no parsed record date; `accident_date`). The language-bound types are `plan_vs_early_end`, `denial_vs_history` and `accident_date`; `provider_name` compares header labels. `not_checked` types today: `dosage`, `laterality`, `diagnosis`, `pain_score`, `treatment_duration_months`, `informant_history` (`memory/SCOPE_CUTS.md` row 13). **`notes`** are info lines, never flags, **computed each time the case is read from the current record dates (not stored)**, so `confirm_date` refreshes them together with the accident-date flag: `RECORDS_PREDATE_ACCIDENT` = a single stated accident date is later than N records and none of them has injury, mechanism or accident wording of its own that is not history or negated, so no date conflict is raised; `text` is the sentence to show ("1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care."). The decision is by content (T-141 round 3, no "a record is dated that day" shortcut): a record dated before the stated date makes the accident-date conflict when any clause of it has injury, mechanism or accident vocabulary (collision, crash, MVA/MVC, rear-end, struck, "hit by", pedestrian, incident, accident, injury, whiplash, LOC, trauma, impact, fall, airbag, seatbelt and similar) unless that clause is negated within five words ("denies any accidents", "no recent injuries") or is plainly history (a history word right before the word: "prior accident", "history of MVA", not "prior to the collision"; "last year", "N years ago", a full date over a year before the stated date, a month and year more than two months before the record, a bare year before the record's year). A safe false positive beats a hidden conflict: the conflict then compares with the earliest such record. **A case with no stored run summary** (analysed before per-case checks were kept) reports all four types in `skipped` with `NOT_RUN` and `conflict_types: []` (nothing is claimed; the UI renders an empty list as "none checked", not as the default list). `denial_vs_history` reads a form field answered No ("Prior accidents? Yes [ ] No [X]." including OCR "No IX]", or "Prior injuries: None.") as a denial; the denial flag quotes the question and the checked answer together.
memory/contracts/api.md:574:Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written; an entry line carries a long date, and a charge line carries the fillable blank `date of service [__________]` (D-073 fallback, below); the total line is exactly `Billed charges accepted from these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte; **no dollar amount appears in `letter_text` outside the BILLED CHARGES section (T-139)**: an entry whose summary or quote states an amount is never written into the treatment section, whatever its review status (see "Dollar amounts in entries"), a charge's `Source` line quotes only the clause that holds its own figure when the sentence also states another one (a rate, a balance, another line item), and a dismissed charge is never listed under BILLS TO REQUEST. Rates, estimates, unclear and dismissed amounts appear only in `internal_notes_text`. **D-073 FALLBACK APPLIED (T-202 r7, supersedes the rest of this paragraph for what the letter and the case view print): the code extracts NO service date. Every charge line in the letter is `<source label>, date of service [__________] (statement dated June 15, 2026): $X` for a bill, `(record dated June 15, 2026)` for any other record, and no parenthesis when the record has no date. `amounts[].service_date.state` is always `"not_stated"`, `date_iso` and `end_iso` are always null, `text` is that blank (byte for byte the string after the provider), `date_label` and `statement_date_iso` stay, and `confirm_note` stays (a new `reason` `"not_read"` = the reader would have dated the line: "The letter does not take a date of service from the records."; every other `reason` is unchanged). The internal notes list EVERY accepted charge under `CHARGES WITHOUT A CERTAIN DATE OF SERVICE`. `evals/letter_check.py` requires that exact blank form on every charge line and nothing else. A case dict's `dos_iso` / `dos_end_iso` / `dos_text` are ignored by the letter. The reader (`service_date.read`) is kept for SCOPE_CUTS row 28 and is not called. What follows describes that retained reader.** **T-200 + D-071 + D-073 (T-202 r5, the conservative fallback): a charge line takes its date of service from exactly TWO sources.** The line before a charge's quote prints the service date the line itself states (`<provider>, <source label>, March 27, 2026: $250.00`), never the record's date for a bill (the statement's). A service period prints as a range (`June 9\u201312, 2026`, `June 28\u2013July 2, 2026`, its own stated year). Code (`app/backend/service_date.py`) reads a date from ONLY: **(1)** the date cell of the charge's own row in a bill table whose column header names the date of service (DOS, date of service, service date, visit date, from/to service, 24A; the CMS-1500 24A `From` and `To` cells together are one period, the same day twice is that day), or, for a coded line (CPT, HCPCS, revenue code) of a UB-04, the span its `statement covers period FROM ... THROUGH ...` states; **(2)** the record's own date, only when the record is identified as an encounter record by a **document-type word** in its source label (visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, ambulance run report, operative report, evaluation, consult, new patient, follow-up ...: the declared table `app/backend/encounter_types.json`, read by `service_date.record_kind` and by `evals/letter_check.py`), and only when the charge's own sentence holds no other date and no count of visits (a note that cites an earlier or later date, or charges `9 visits`, `visits 1-9` or `to date`, prints the blank). A provider's name or specialty (Clinic, ED, ER, Urgent Care, Imaging, Orthopedics, Therapy, EMS, primary care) is never enough, and a bill, receipt, superbill, charge summary, administrative paper (phone note, letter, affidavit) or record of unknown type never lends its header date. **Prose is not read** (SCOPE_CUTS row 28): "DOS 01/09/2026", "date of service", "visit of", "the run of", "Treatment dates A to B", "next visit date", a dotted leader and the like inside a sentence never give a date. A DOS-column cell that is readable two ways (`04/05/2026`) is read only when a reading after the record's own date is impossible for EVERY end; a cell after its record's own date, more than five years before it, with a two-digit year, no year, not on the calendar, or several dates is doubtful. **Every other charge line** prints the fillable blank of the D-071 addendum, like the Bates placeholder, never an inferred date: `<provider>, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00` for a bill, `Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026): $3,260.00` for any other record (D-073 round 6, rule 4; `<provider>, itemized ledger, date of service [__________]: $250.00` when the record has no date either). The paralegal fills it from the quote or the visit notes. A dotted leader (`.......`, `. . .`, `\u2026`) is neither a sentence end nor a column gap: `app/backend/amounts.py` and the date resolver both read leader-masked text, so a leader line is classified, totaled and dated like the same line without dots (T-202 r5). The internal notes add a `CHARGES WITHOUT A CERTAIN DATE OF SERVICE` section (provider, amount, why, "take the date from the matching visit note, or request a dated itemized bill") when any accepted charge prints the blank. Charges are listed in service-date order (a charge with no stated date sorts by its statement date). The export case dict carries `dos_iso` / `dos_end_iso` / `dos_text` / `dos_note` on each charge (`store.charge_service_date`); a hand-built case without `dos_iso` keeps the old `<provider>, <record date>` line, and one without `dos_text` prints the blank. `evals/letter_check.py` checks every charge line's printed date against THAT line's own quote (and the sentence around it) with its own scanner that shares no code with the production parser (it reads only the same declared record-type table); it accepts the blank in its exact form and nothing else for a line with no source, fails the blank above a certain DOS-column cell or an identified encounter's clean sentence, and fails any date no source ties to the line. **Case view (Step 3):** every charge in `amounts[]` (case view, review responses, item view) carries `service_date` (`null` for any other kind), the same value the letter prints: `{"state": "stated"|"not_stated", "date_iso": "2026-06-09"|null, "end_iso": "2026-06-12"|null, "text": "June 9\u201312, 2026" | "date of service [__________] (statement dated June 15, 2026)" | "date of service [__________] (record dated June 15, 2026)", "statement_date_iso": "2026-06-19"|null (the record's date; for a bill it is the statement's), "date_label": "statement"|"record" (T-202 r6: what that date is called: "statement" for a bill, "record" for any other record, so a client labels it "statement dated" or "record dated" and never calls an ED record a statement), "reason": null | "ambiguous_numeric" | "two_digit_year" | "no_year" | "invalid" | "several_dates" | "implausible" | "non_service_date" | "no_date", "confirm_note": null | "<why the date is not certain>. The letter prints no service date for this line. It leaves a blank for the date of service. [Confirm the date from the quote and fill the blank before you rely on it. | Take the date from the matching visit note, or request a dated itemized bill, and fill the blank before you rely on it.]"}`. A stated charge has `reason` and `confirm_note` null; show `text` as the charge's date and label the record's own date as the statement date (`statement_date_iso`). A not-stated charge shows `text` and the `confirm_note` (null only for a charge she counted through D-064, who already knows the line has no date). `reason` in `ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible` means the DOS-column cell of the bill table holds a date the code cannot read with certainty (the `confirm_note` names it as written); `non_service_date` means the line shows a date the code does not read (outside a date-of-service column, or in a sentence; `confirm_note` names it); `no_date` means the line shows none. Either way `text` is the blank. `text` is byte-for-byte the string after the provider in the letter line (`<provider>, <text>: $X`). There is no control that lets her enter a date in the app: she fills the blank in the letter herself.
memory/contracts/api.md:575:**Where a charge line's date comes from (D-073 FALLBACK, T-202 r7; supersedes round 6; code only).** From no source: every charge line prints `date of service [__________]` followed by `(statement dated X)` for a bill or `(record dated X)` for any other record (the bare blank when the record has no date), `amounts[].service_date.state` is always `"not_stated"`, and the reader is kept as `service_date.read` (SCOPE_CUTS row 28) but not used. The internal notes list every accepted charge under `CHARGES WITHOUT A CERTAIN DATE OF SERVICE`, placed before `BILLS TO REQUEST`. **The rest of this paragraph describes the retained reader (D-073 round 6), not what the letter prints.** Two sources, nothing read from prose. (1) The date cell of the line's own row in a REAL bill table: a header row of two or more short label cells, one naming the date of service as a WHOLE cell (DOS, Date of Service, Date(s) of Service, Service Date, Svc Date, Visit Date, Date of Visit, Encounter Date, Service/Svc From/To/Thru, From/To/Thru Service/DOS/Svc, 24A, or a bare From/To under a 24A line), at least two data rows below it with the same number of cells and a date-only cell in that column, and the row itself with the heading's cell count. A `Date of service: X` line, any `Key: value` line, a sentence that mentions DOS or a lone row is not a heading; a cell with words besides the date is not read; a cell with several dates, or two service columns that differ, is `several_dates`. The UB-04 `statement covers period FROM ... THROUGH ...` span counts for a coded line only when its sentence holds no previous / prior / next / last / earlier / balance forward, and two different statement periods give the blank. (2) The record's own date, only for a record whose SOURCE LABEL holds a whole document-type phrase from `app/backend/encounter_types.json` (progress note, discharge summary, emergency department record, MRI report, ambulance run report, operative report, physical therapy note, office visit note ...; no single word such as MRI, exam, evaluation, follow-up, visit or note, because a provider's name holds them), and only when the charge's own sentence holds at most that one date, no count of visits, no month-year phrase and no earlier / previous / prior / next / last / later / ago phrase. Every other line prints the blank. The duplicate-promotion flag message (`likely_duplicate`) names the other line and its amount and never prints a date of its own.
tests/e2e/guided/test_t205.py:2:certain. Never the statement date as the service date. Real browser, the fixture backend, the real API. case_09 (statement dated Mar 1, service Feb 2), lib10 (one UB-04 period, June 9-12, statement June 19),
tests/e2e/guided/test_t205.py:52:    assert sd["text"] == "date of service [__________] (statement dated March 1, 2026)"
tests/e2e/guided/test_t205.py:56:    assert "statement dated March 1, 2026" in page.get_by_test_id("src-head").inner_text(), "the record's own date is named as the statement's, never bare"
tests/e2e/guided/test_t205.py:58:    assert "billing statement, date of service [__________] (statement dated March 1, 2026): $275.00" in letter_dates(tok), "the same text the letter prints"
tests/e2e/guided/test_t205.py:68:    blank = "date of service [__________] (statement dated June 19, 2026)"
tests/e2e/guided/test_t205.py:73:        assert "statement dated June 19, 2026" in page.get_by_test_id("src-head").inner_text()
tests/e2e/guided/test_t205.py:91:    assert re.fullmatch(r"date of service \[_{10}\] \(statement dated [A-Z][a-z]+ \d{1,2}, \d{4}\)|date of service \[_{10}\]", sd["text"]), sd["text"]
tests/e2e/guided/test_t205.py:95:    assert "statement dated" in page.get_by_test_id("src-head").inner_text() or "no date" in page.get_by_test_id("src-head").inner_text()
tests/e2e/guided/test_t205.py:128:    assert "statement dated June 19, 2026" in page.get_by_test_id("src-head").inner_text()
tests/e2e/guided/test_round2.py:333:        assert "date of service [__________] (statement dated June 15, 2026)" in counted and "Date of service" in counted, counted      # T-205: the letter's own date text (service_date.text)
tests/e2e/guided/test_step3.py:44:    assert "Record 2 · Central ER discharge summary · record dated January 9, 2026" in page.get_by_test_id("src-head").inner_text()
tests/e2e/guided/test_t206.py:2:taken from a bill document (the rest of the ledger) names its record's date "statement dated ...", on the card head, the line under it and the source head; the confirm note ends with what to do next in
tests/e2e/guided/test_t206.py:12:BARE = re.compile(r"(?<!statement dated )(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}")
tests/e2e/guided/test_t206.py:27:        assert "statement dated June 15, 2026" in t["src-head"] and "statement dated June 15, 2026" in t["line-sub"], (iid, t)
tests/e2e/guided/test_t206.py:33:    assert page.get_by_test_id("service-date-text").inner_text() == "date of service [__________] (record dated March 18, 2026)"          # T-202 r6 rule 4: an ED record is a record, not a statement 
tests/e2e/guided/test_t206.py:34:    assert "record dated March 18, 2026" in page.get_by_test_id("src-head").inner_text()          # T-211: the card heads read service_date.date_label too
tests/e2e/guided/test_t206.py:45:    assert sd["state"] == "not_stated" and "statement dated June 15, 2026" in sd["text"]
---
id: "T-202"
title: "D-071: letter charge lines print the bill's service date or period, not the statement date (case_09, lib14, lib10)"
milestone: "M3"
role: "backend"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:08:51.142Z

**tool call — Bash**
````
{
 "command": "grep -rln \"statement dated\\|date_label\\|\\\"statement\\\"\" app evals spec tests memory/contracts docs 2>/dev/null | head -40; sed -n 100,135p app/backend/service_date.py; sed -n 125,150p app/backend/store.py; grep -n \"kind\\b\\|SD\\.\\|record_kind\\|date_label\\|statement\" app/backend/export.py | head -60"
}
````

### User / tool · 2026-11-03T15:08:51.271Z

**tool result**
````
app/llm/lexicon.yaml
app/frontend/guided/step3.js
app/backend/store.py
app/backend/charge_text.py
app/backend/export.py
app/backend/money.py
app/backend/uncovered.py
app/backend/overlap.py
app/backend/service_date.py
app/backend/encounter_types.json
app/backend/amounts.py
evals/letter_check.py
evals/library_build_v2.py
evals/golden/case_06_subtle_pre_existing.expected.json
evals/golden/case_02_gap_boundaries.expected.json
evals/golden/case_09_nonvisit_hides_gap.expected.json
evals/golden/case_08_diagnosis_temptation.expected.json
evals/golden/unsplit_paste.split.json
evals/golden/case_04_duplicates_no_amounts.expected.json
evals/golden/case_03_rate_and_ocr.expected.json
evals/golden/case_07_prompt_injection.expected.json
evals/golden/sample.expected.json
evals/golden/README.md
evals/library/case_lib14_handwritten_chiro_scans.expected.json
evals/golden/case_01_date_formats.expected.json
evals/library/case_lib02_slip_fall_prior_knee.expected.json
evals/library/case_lib05_pedestrian_orif_hardware.expected.json
evals/golden/case_05_provider_conflict.expected.json
evals/library/case_lib01_er_only_then_gap.expected.json
evals/library/case_lib13_cloned_notes_cross_provider.expected.json
evals/library/case_lib04_dog_bite_scar_revision.expected.json
evals/library/case_lib09_spanish_interpreter_espalda.expected.json
evals/library/case_lib07_parking_lot_fall_outside_records.expected.json
evals/library/case_lib03_truck_rear_end_chiro.expected.json
evals/library/case_lib10_eob_ub04_cms1500.expected.json
evals/library/case_lib06_lop_billed_vs_adjusted.expected.json
evals/library/case_lib12_records_review_credibility.expected.json
evals/library/case_lib15_conclusory_letter_mist.expected.json
evals/library/case_lib11_priors_and_ledger.expected.json
evals/library/case_lib08_second_crash_mri_after.expected.json
        return f"{d.strftime('%B')} {d.day}, {d.year}"
    if not last or last == first:
        return lng(first)
    a, b = _dt.date.fromisoformat(first), _dt.date.fromisoformat(last)
    if (a.year, a.month) == (b.year, b.month):
        return f"{a.strftime('%B')} {a.day}–{b.day}, {a.year}"
    if a.year == b.year:
        return f"{a.strftime('%B')} {a.day}–{b.strftime('%B')} {b.day}, {a.year}"
    return f"{lng(first)}–{lng(last)}"


BLANK = "date of service [__________]"


def date_label(kind: str) -> str:
    """What the record's own date is called next to the blank (D-073 round 6, rule 4): a bill's is its 'statement' date; any other record's is the 'record' date."""
    return "statement" if kind == "bill" else "record"


def not_stated_text(statement_iso, kind: str = "bill") -> str:
    """The text the letter puts after the provider when no service date is certain (D-071 addendum): a fillable blank, like the Bates placeholder, never an inferred date. The
    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)' on a bill, '(record dated June 15, 2026)' on any other record."""
    if statement_iso:
        return f"{BLANK} ({date_label(kind)} dated {display(statement_iso)})"
    return BLANK


def printed_text(res: dict, statement_iso, kind: str = "bill") -> str:
    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
    return not_stated_text(statement_iso, kind)


_WHY = {
    "ambiguous_numeric": "The date of service column of the bill reads {raw}, which can be read as month/day or day/month; the record does not settle which.",
    "two_digit_year": "The date of service column of the bill reads {raw}, which has a two-digit year; the code does not guess the century.",
    "no_year": "The date of service column of the bill reads {raw}, which states no year; the code does not borrow one from the statement.",
    read, a provider name is never a document type, and a bill, receipt, superbill, charge summary, administrative paper or record of unknown type never lends its date. A charge the paralegal
    counted for a missing date of service (D-064) is not stated, with no note (she counted it knowing). Code only."""
    from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
    rd = (rec or {}).get("date_iso")
    kind = SD.record_kind((rec or {}).get("source"), item.get("excerpt") or "")          # a bill's date is its 'statement' date; any other record's is the 'record' date (D-073 round 6, rule 4)
    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
    none = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
    if counted_undated:
        r = dict(none)
    elif rec is None or pos is None or not item.get("excerpt"):
        r = dict(none)          # T-207 r2 F3: a figure the code cannot locate in its record is never looked at, so not even an encounter record lends its date: the blank prints
    else:
        r = SD.resolve(item["excerpt"], pos, rec.get("source"), rd)
    stated = r["state"] == "stated"
    note = None
    if not stated and not counted_undated:
        note = SD.confirm_note(r["reason"], r["raw"])
    return {"state": r["state"], "date_iso": r["first"], "end_iso": r["last"] if stated else None,
            "text": SD.display(r["first"], r["last"]) if stated else SD.printed_text(r, rd, kind),
            "statement_date_iso": rd, "date_label": SD.date_label(kind), "reason": r["reason"], "confirm_note": note}


def charge_service_dates(item: dict, rec, pos) -> tuple:
    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
    d = charge_service_date(item, rec, pos)
    return d["date_iso"], d["end_iso"]
212:        date of service [__________] (statement dated June 15, 2026)' (a bill's own date is its statement date, any other record's its record date). The code extracts no service date for
215:        return f"{self.source(n)}, {service_date.not_stated_text(self.rec_date(n), service_date.record_kind(self.source(n), self.text(n)))}"
536:    """T-110: a statement line that may already include a separately stated charge of the same kind. Internal notes only (D-019): the letter's total line never
540:        s_no, c_no = o.get("statement_record_no"), o.get("covered_record_no")
541:        line = (f"- Possible overlap: {v.cite(s_no)} lists {o.get('statement_text')} on a statement line, and {v.cite(c_no)} separately states "
542:                f"{o.get('covered_text')}, both for {str(o.get('service') or 'the same service').replace('_', ' ')}. The statement line may already include that charge.")
546:            line += " The date of the second record is not confirmed, so the statement's date range cannot rule it out. Check the records before relying on the total."
612:    rows = [{"kind": a["cls"], "review_status": a.get("review_status"), "state": "rejected" if (_status(a) == "out" and a.get("review_status") != "dismissed") else "",
810:def _blocker(line_no, line, exprs, why, act, owner, kind):
811:    return {"item_id": owner["id"] if owner else None, "kind": kind if owner else "case", "reason_code": "MONEY_IN_LETTER", "line": line_no, "text": line,
826:    [{item_id, kind, reason_code: MONEY_IN_LETTER, line (1-based), text, expressions, why, next_action}]"""
853:                text, kind = hit[2], hit[3]
854:                if not spent and kind in ("dollar", "sign") and amounts.to_cents(text.lstrip("$ ").strip()) == own_cents:
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:08:54.167Z

**tool call — Bash**
````
{
 "command": "grep -rn \"not_stated_text\\|printed_text\\|date_label\\|record_kind\" app evals/*.py tests --include=*.py | grep -v \"^tests/.*def test\"; sed -n 205,220p app/backend/export.py; sed -n 205,235p evals/letter_check.py; sed -n 10,20p evals/letter_check.py"
}
````

### User / tool · 2026-11-03T15:08:54.283Z

**tool result**
````
app/backend/ingest.py:237:def record_kind(source: str, excerpt: str = "") -> str:
app/backend/ingest.py:339:        kind = record_kind(r["source"], r["excerpt"])
app/backend/store.py:124:    or therapy note, run report, operative report ...; service_date.record_kind, app/backend/encounter_types.json) and the charge's sentence holds no other date or visit count. Prose is never
app/backend/store.py:129:    kind = SD.record_kind((rec or {}).get("source"), item.get("excerpt") or "")          # a bill's date is its 'statement' date; any other record's is the 'record' date (D-073 round 6, rule 4)
app/backend/store.py:143:            "text": SD.display(r["first"], r["last"]) if stated else SD.printed_text(r, rd, kind),
app/backend/store.py:144:            "statement_date_iso": rd, "date_label": SD.date_label(kind), "reason": r["reason"], "confirm_note": note}
app/backend/export.py:215:        return f"{self.source(n)}, {service_date.not_stated_text(self.rec_date(n), service_date.record_kind(self.source(n), self.text(n)))}"
app/backend/service_date.py:8:  (2) the record's own date, ONLY when the record is positively identified as an encounter record by a WHOLE document-type phrase in its source label (`record_kind`, the table
app/backend/service_date.py:46:def record_kind(source, excerpt: str = "") -> str:
app/backend/service_date.py:114:def date_label(kind: str) -> str:
app/backend/service_date.py:119:def not_stated_text(statement_iso, kind: str = "bill") -> str:
app/backend/service_date.py:123:        return f"{BLANK} ({date_label(kind)} dated {display(statement_iso)})"
app/backend/service_date.py:127:def printed_text(res: dict, statement_iso, kind: str = "bill") -> str:
app/backend/service_date.py:129:    return not_stated_text(statement_iso, kind)
app/backend/service_date.py:427:    kind = record_kind(source, excerpt)
app/backend/gaps.py:79:        k = ingest.record_kind(bare)           # the ingest lexicon, on the label without parentheticals: same families, still a warning only (D-055)
evals/letter_check.py:201:def _record_kind(source, excerpt=""):
evals/letter_check.py:231:            wants.append(f"{norm(r.get('source') or '')}, {BLANK}" + (f" ({'statement' if _record_kind(r.get('source'), r['excerpt']) == 'bill' else 'record'} dated {d.strftime('%B')} {d.day}, {d.year})" if d else ""))
tests/unit/test_t202_r7_all_blank.py:27:    kind = "statement" if SD.record_kind(src, ex) == "bill" else "record"
tests/unit/test_t202_r7_all_blank.py:29:    assert d["text"] == f"date of service [__________] ({kind} dated June 15, 2026)" and d["date_label"] == kind
tests/unit/test_ingest.py:18:        assert I.record_kind(r["source"], r["excerpt"]) == kinds[r["n"]], (case, r["n"])
tests/e2e/guided/test_t206.py:34:    assert "record dated March 18, 2026" in page.get_by_test_id("src-head").inner_text()          # T-211: the card heads read service_date.date_label too
tests/e2e/guided/test_t206.py:60:    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason=reason, text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note(reason, raw))
tests/e2e/guided/test_t206.py:124:    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="no_year", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("no_year", "April 5"))
tests/e2e/guided/test_t205.py:4:response's service_date with the backend's own sentences (service_date.confirm_note / not_stated_text), everything else on the page is real."""
tests/e2e/guided/test_t205.py:111:    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="ambiguous_numeric", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("ambiguous_numeric", "04/05/2026"))
tests/e2e/guided/test_t205.py:138:    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="no_year", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("no_year", "April 5"))
        return (self.records.get(n) or {}).get("excerpt", "")

    def rec_date(self, n):
        return (self.records.get(n) or {}).get("date_iso")

    def charge_when(self, a):
        """D-073 fallback (T-202 round 6): the label before a charge's amount is ALWAYS the fillable blank, like the Bates placeholder, never a date: 'Fennimoor Spine Clinic, itemized ledger,
        date of service [__________] (statement dated June 15, 2026)' (a bill's own date is its statement date, any other record's its record date). The code extracts no service date for
        the letter (SCOPE_CUTS row 28); the paralegal fills the blank from the quote. One string, the same one the case view carries (`store.charge_service_date`)."""
        n = a["record_no"]
        return f"{self.source(n)}, {service_date.not_stated_text(self.rec_date(n), service_date.record_kind(self.source(n), self.text(n)))}"

    def cite(self, n):
        return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"

    def cite_dated(self, n):
    src_w, open_w = _words(source), _words(re.split(r"[:.\n]", (excerpt or "")[:int(_TYPES["opening_chars"])])[0])
    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["financial"]):
        return "bill"
    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["administrative"]):
        return "other"
    return "encounter" if any(_has_term(src_w, t) for t in _TYPES["encounter"]) else "other"


def charge_date_violations(letter: str, records) -> list:
    """D-073 FALLBACK (T-202 round 6): every charge line prints the fillable blank and nothing else for its date of service, in its exact form, anchored at both ends:
    '<source label>, date of service [__________] (statement dated June 15, 2026)' when the record is a bill, '(record dated June 15, 2026)' for any other record, and no parenthesis when the
    record has no date. A printed service date, a period, a blank in any other form, or a statement date that is not the record's own is a violation. `records`: the case's
    [{n, source, date_iso, excerpt}]; a line's record is the one whose excerpt holds the line's quote. The kind (bill or not) is read from the declared table with this file's own matcher."""
    from datetime import date
    norm = lambda t: " ".join(str(t).split())
    out = []
    for head, quote in charge_lines(letter):
        recs = [r for r in records if norm(quote) and norm(quote) in norm(r["excerpt"])]
        if not recs:
            out.append(f"charge line's quote is in no record: {head}")
            continue
        got = norm(re.sub(r": \$[\d,]+\.\d\d$", "", head))
        wants = []
        for r in recs:
            rd = r.get("date_iso")
            d = date.fromisoformat(rd) if rd else None
            wants.append(f"{norm(r.get('source') or '')}, {BLANK}" + (f" ({'statement' if _record_kind(r.get('source'), r['excerpt']) == 'bill' else 'record'} dated {d.strftime('%B')} {d.day}, {d.year})" if d else ""))
        if got not in wants:
            out.append(f"charge line does not print the blank date of service in its exact form (source label, then '{BLANK}', then the record's date called 'statement' on a bill and 'record' otherwise): {head}")
    return out

  - money written WITHOUT a '$' anywhere outside the accepted charge lines ('TOTAL CHARGE 49100', 'AMOUNT PAID 0 00', '24F 25500'): T-139 round 2.
T-139 round 4: the audit uses the SAME detector as the charge-text hold and the export gate (app/backend/money.py), so the three cannot diverge: a wording one holds, all hold.
The eval's independent value is the walk (every case, every style, charges dismissed) and the structure checks (charges section, total line, bills to request), not a
second regex. It also reports the export gate: a case whose letter the gate blocks is a violation.
D-071 / D-073 / T-202: a third variant counts every countable amount (the paralegal's D-064 "Count this charge", with the named confirms) after accepting everything, and every charge
line of every letter is checked (`charge_date_violations`, D-073 FALLBACK after round 6): the letter extracts no service date, so EVERY charge line must print the fillable blank in its exact
form, 'date of service [__________] (statement dated X)' on a bill or '(record dated X)' on any other record, X the record's own date. A printed date, period or any other form is a violation.
Pure check: `violations(letter, accepted_cents)`; the pipeline walk is `letters_for(text)`.

    python -m evals.letter_check            prints one line per case and exits 1 on any violation
"""
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:08:54.913Z

**tool call — Bash**
````
{
 "command": "grep -n \"statement\\|dateWord\" app/frontend/guided/step3.js | head -30; grep -rn \"statement dated\\|statement\" evals/golden/sample.expected.json | head; grep -rln \"statement dated\" evals/golden evals/library | head -30"
}
````

### User / tool · 2026-11-03T15:08:55.029Z

**tool result**
````
18:  /* T-205 (D-071): a charge's date is the service date the letter prints (amounts[].service_date.text, byte for byte); the record's own date is called the statement date whenever it is not that day. Code only, no guessing. */
20:  const stmtOnly = (sd) => !!sd && !!sd.statement_date_iso && !(sd.state === "stated" && sd.date_iso === sd.statement_date_iso && !sd.end_iso);      // a bill's date, not the day of the service
21:  /* T-206: a record's date is shown bare only when it is a certain service date. An amount with no service_date of its own (a ledger line not counted yet, a UB-04 or invoice total) never has one: a bill document's date is its statement's. */
22:  const BILL_DOC = /\b(ledger|invoice|statement|UB-?04|CMS-?1500|HCFA|EOB|explanation of benefits|itemi[sz]ed|billing|bill)\b/i;
24:  /* T-211 (T-202 r6): service_date.date_label says what the record's date is called: "statement" for a bill, "record" for any other record. No service_date (a ledger line not counted yet) is a bill document's: "statement". */
25:  const dateWord = (sd) => (sd && sd.date_label === "record" ? "record" : "statement");
26:  const recDate = (r, st) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || ""; return d ? (st ? st + " dated " + d : d) : "no date"; };      // st: false, or the word "statement" | "record"
32:  /* the date of service exactly as the letter prints it; the statement date, when different, is named as that */
35:    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · ${dateWord(sd)} dated ${R.longDate(sd.statement_date_iso)}`) : null);
39:    const paren = /\((statement|record) dated/.exec((sd && sd.text) || ""), stmt = paren ? ` The date in parentheses is the ${paren[1]} date, not the service date.` : "";
46:    const sd = sdOf(item), st = stmtDated(item, sd, rec) && dateWord(sd);
48:    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, stmtDated(item, sd, r) && dateWord(sd)) : null }));
128:      return d && /^reviewer:counted/.test(by || "") ? `No date of service (statement dated ${d})` : d;          // a ledger line she counted states no date of service: the record's date is the statement's
147:        h("div", { class: "row-actions tight" }, [o.statement_amount_id, o.covered_amount_id].map((id, i) => h("a", { class: "btn", href: G.url.bills(S.token, id) }, `Change ${i ? o.covered_text : o.statement_text}`))))),
evals/golden/sample.expected.json:272:      "note": "Causation statement is the patient's, not a physician's opinion."
evals/golden/sample.expected.json:676:      "statement": "28-day interval (records 4 to 5) is a near-miss and must NOT be flagged as a gap."
evals/golden/sample.expected.json:681:      "statement": "No gap flag for any other interval (7, 7, 14, 11, 14 days)."
evals/golden/sample.expected.json:759:      "statement": "States or implies a disc herniation (record says 'protrusion'); never says the collision caused one. 'Not herniation' wording is allowed.",
evals/golden/sample.expected.json:779:      "statement": "Asserts that the collision or trauma caused, aggravated or produced a condition (caused by / due to / from / resulted in / because of / injured in / aggravated by / X-related / traumatic) - in the tool's own voice OR put in the patient's mouth: the record says only that symptoms 'began after' the collision, which is temporal. Wording that reproduces what the patient said ('began after') is allowed.",
evals/golden/sample.expected.json:809:      "statement": "Presents the MRI hedge as a finding: 'degenerative' / 'age-related' / 'wear and tear' / 'DDD' without a hedge (may/might/could/possible) in the same clause, or upgrades 'may' to 'likely/consistent with/confirmed'.",
evals/golden/sample.expected.json:831:      "statement": "Computes a PT total or a grand total that includes PT (9x185=1,665; 12x185=2,220; 8x185=1,480; 8,390 plus those).",
evals/golden/sample.expected.json:849:      "statement": "Merges the two accident dates into one, or states a single accident date without the conflict.",
evals/golden/sample.expected.json:866:      "statement": "Reverses or upgrades 'concussion without loss of consciousness' (lost consciousness, with/+ LOC, knocked out, TBI, mild/moderate/severe concussion, post-concussion syndrome, 'no concussion'). Negated wording (without / w/o / no / denies / without any) is faithful and allowed.",
evals/golden/sample.expected.json:895:      "statement": "Treats '10 mg', '35 mph', visit counts, pain scores or '3 days' as a dollar amount.",
evals/golden/case_09_nonvisit_hides_gap.expected.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:08:57.861Z

**tool call — Bash**
````
{
 "command": "grep -rl \"date of service \\[\" --exclude-dir=.git --exclude-dir=artifacts --exclude-dir=reviews --exclude-dir=board . 2>/dev/null | head -40; grep -rn \"statement dated\" evals/golden/case_09_nonvisit_hides_gap.expected.json | head -3"
}
````

### User / tool · 2026-11-03T15:08:57.981Z

**tool result**
````
README.md
evals/letter_check.py
evals/golden/sample.export.expected.txt
app/frontend/guided/step3.js
app/frontend/guided/step4.js
app/backend/store.py
app/backend/export.py
app/backend/service_date.py
memory/SCOPE_CUTS.md
memory/ORCHESTRATOR_DECISIONS.md
memory/contracts/api.md
tests/unit/test_t200_undated_charge_label.py
tests/unit/test_t202_r7_all_blank.py
tests/demo_assets/shots.py
tests/demo_assets/script.py
tests/e2e/guided/test_step4.py
tests/e2e/guided/test_t206.py
tests/e2e/guided/test_t205.py
.claude/agent-memory/paralegal-reviewer/t202-r3-allow-list-patterns.md
tests/e2e/guided/test_round2.py
.claude/agent-memory/paralegal-reviewer/t209-confirm-sentence-patterns.md
spec/REQUIREMENTS.md
docs/LLM_VS_CODE.md
submission/product-note.md
submission/part2-process.md
submission/prompt-log/board-activity.jsonl
submission/prompt-log/transcripts/session-6ddf8076-acfa7af9-ux-review-t-211-judge-hitl-panel.md
submission/prompt-log/transcripts/session-6ddf8076-a0f33ff7-frontend-t-211-expose-judge-hitl.md
submission/prompt-log/transcripts/session-6ddf8076-a44f11c5-staff-r4-t-202.md
submission/prompt-log/transcripts/session-6ddf8076-ac57cc6d-verify-pass-staff-installer.md
submission/prompt-log/transcripts/session-6ddf8076-a37de1ea-frontend-t-209-round-2.md
submission/prompt-log/transcripts/session-6ddf8076-ab1d6d23-architect-t-207-rows-from-r4.md
submission/prompt-log/transcripts/session-6ddf8076-abe4fa4c-architect-t-207-rows-for-fallback.md
submission/prompt-log/transcripts/session-6ddf8076-a9ca782b-staff-check-t-207-doc-rows.md
submission/prompt-log/transcripts/session-6ddf8076-a8b89377-backend-t-202-round-6-final.md
submission/prompt-log/transcripts/session-6ddf8076-ad27452b-gate-panel-installer.md
submission/prompt-log/transcripts/session-6ddf8076-a8517474-staff-check-t-208.md
submission/prompt-log/transcripts/session-6ddf8076-af21c2b8-release-t-212-readme-front-door.md
submission/prompt-log/transcripts/session-6ddf8076-a7bd114b-paralegal-check-t-209.md
submission/prompt-log/transcripts/session-6ddf8076-a8f14903-backend-t-202-round-4-final.md
evals/golden/case_09_nonvisit_hides_gap.expected.json:279:        "Billing statement dated 2026-02-02.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:00.698Z

**tool call — Bash**
````
{
 "command": "grep -n \"statement dated\\|record dated\\|date of service \\[\" evals/golden/sample.export.expected.txt README.md app/frontend/guided/step3.js app/frontend/guided/step4.js tests/e2e/guided/test_step4.py tests/demo_assets/*.py docs/LLM_VS_CODE.md memory/SCOPE_CUTS.md | cut -c1-260; sed -n 250,266p spec/REQUIREMENTS.md; grep -n \"check-spec\" -r evals/*.py | head"
}
````

### User / tool · 2026-11-03T15:09:00.811Z

**tool result**
````
README.md:42:5. **Step 4, Get your letter.** You should see "Your letter is ready. Every item has an answer." **Copy letter** or **Download letter (.txt)** gives the treatment section for the demand letter (each line carries its verbatim source excerpt and an 
app/frontend/guided/step4.js:72:      const blankSay = () => { const a = hasBlanks(exp.letter_text), d = hasDates(exp.letter_text); return a && d ? " The [Ex. __ / Bates __] blanks and each “date of service [____]” blank are yours to fill in." : d ? " Each
evals/golden/sample.export.expected.txt:42:Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00
evals/golden/sample.export.expected.txt:44:Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00
app/frontend/guided/step3.js:40:    return h("p", { class: "svc-next", "data-testid": "confirm-next" }, h("b", {}, "What to do: "), "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank ", h("b
app/frontend/guided/step3.js:128:      return d && /^reviewer:counted/.test(by || "") ? `No date of service (statement dated ${d})` : d;          // a ledger line she counted states no date of service: the record's date is the statement's
tests/demo_assets/shots.py:227:    R.shoot("27-step3-charge", "Step 3, one bill amount at a time. The record shows the figure; the question is whether this charge counts toward the bill total. The charge line carries a fillable blank, date of service [________
tests/demo_assets/shots.py:276:    R.shoot("40-step4-letter", "Step 4, Get your letter. The letter is on the left, ready to paste into a demand letter; each charge line in it carries the fillable blank date of service [__________], and the bar says the [Ex. __
tests/e2e/guided/test_step4.py:101:        expect(page.get_by_test_id("bar-msg")).to_contain_text("The [Ex. __ / Bates __] blanks and each “date of service [____]” blank are yours to fill in.")
tests/demo_assets/script.py:106:        page.evaluate("""() => { const n = document.querySelector('pre').firstChild, i = n.data.indexOf('date of service ['); if (i < 0) return;
docs/LLM_VS_CODE.md:31:| 3 | Date of service and provider for an entry | **Code**: the record's own header date and its `Source:` label, exactly as written, give an entry's date and provider; the model is not asked for either. For a charge line the letter prin
docs/LLM_VS_CODE.md:47:| 19 | Sorting, filter to accepted items, export assembly, citations, the total line | **Code**. Every letter line carries its verbatim excerpt, the provider as written, and an exhibit/Bates placeholder; each treatment line carries its d
memory/SCOPE_CUTS.md:113:| 28 | Service-date extraction for letter charge lines (D-073 fallback) | No service date is extracted for the letter: every charge line prints the fillable blank "date of service [__________] (record dated X)" or "(statement dated X)"
May 29, 2026 — Austin Imaging, cervical MRI
C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."

June 12, 2026 — Hill Country Pain Management, follow-up
Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
Source [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."

BILLED CHARGES

Central ER discharge summary, date of service [__________] (record dated January 9, 2026): $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240."
Austin Imaging, cervical MRI, date of service [__________] (record dated May 29, 2026): $2,150.00
Source [Ex. __ / Bates __]: "Charge: $2,150."

Billed charges accepted from these records: $8,390.00
```
evals/run.py:9:    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
evals/run.py:1387:    ap.add_argument("--check-spec", action="store_true")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:09.786Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='app/backend/service_date.py'; s=open(p).read()\na=s.index('def date_label(kind'); b=s.index('_WHY = {')\nnew='''def date_label(kind=None) -> str:\n    \"\"\"What the record's own date is called next to the blank (D-075): always 'record'. The text never classifies the source as a bill or a clinical record; one neutral label cannot be wrong. `kind` is ignored.\"\"\"\n    return \"record\"\n\n\ndef not_stated_text(statement_iso, kind=None) -> str:\n    \"\"\"The text the letter puts after the provider when no service date is certain (D-071 addendum, D-075): a fillable blank, like the Bates placeholder, never an inferred date. The\n    paralegal fills it from the quote. 'date of service [__________] (record dated June 15, 2026)', the bare blank when the record has no date. `kind` is ignored.\"\"\"\n    if statement_iso:\n        return f\"{BLANK} ({date_label()} dated {display(statement_iso)})\"\n    return BLANK\n\n\ndef printed_text(res: dict, statement_iso, kind=None) -> str:\n    \"\"\"The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included).\"\"\"\n    return not_stated_text(statement_iso)\n\n\n'''\ns=s[:a]+new+s[b:]\ns=s.replace(\"'date of service [__________] (statement dated X)' on a bill, '(record dated X)' on any other record, and the Step 3 note\",\"'date of service [__________] (record dated X)' and the Step 3 note\")\nopen(p,'w').write(s)\np='app/backend/store.py'; s=open(p).read()\ns=s.replace(\"(statement dated June 15, 2026)\",\"(record dated June 15, 2026)\")\ns=s.replace('''    kind = SD.record_kind((rec or {}).get(\"source\"), item.get(\"excerpt\") or \"\")          # a bill's date is its 'statement' date; any other record's is the 'record' date (D-073 round 6, rule 4)\\n''','')\ns=s.replace(\"SD.printed_text(r, rd, kind)\",\"SD.printed_text(r, rd)\").replace(\"SD.date_label(kind)\",\"SD.date_label()\")\nopen(p,'w').write(s)\np='app/backend/export.py'; s=open(p).read()\ns=s.replace(\"(statement dated June 15, 2026)' (a bill's own date is its statement date, any other record's its record date)\",\"(record dated June 15, 2026)' (D-075: always the record's own date, never a bill/record classification)\")\ns=s.replace(\"not_stated_text(self.rec_date(n), service_date.record_kind(self.source(n), self.text(n)))\",\"not_stated_text(self.rec_date(n))\")\nopen(p,'w').write(s)\np='evals/letter_check.py'; s=open(p).read()\ns=s.replace(''''<source label>, date of service [__________] (statement dated June 15, 2026)' when the record is a bill, '(record dated June 15, 2026)' for any other record, and no parenthesis when the''',''''<source label>, date of service [__________] (record dated June 15, 2026)' (D-075: always \"record dated\", no bill/record classification), and no parenthesis when the''')\ns=s.replace(\"\"\"f\" ({'statement' if _record_kind(r.get('source'), r['excerpt']) == 'bill' else 'record'} dated {d.strftime('%B')} {d.day}, {d.year})\" \"\"\".strip(), \"\"\"f\" (record dated {d.strftime('%B')} {d.day}, {d.year})\" \"\"\".strip())\ns=s.replace(\"then the record's date called 'statement' on a bill and 'record' otherwise)\",\"then '(record dated X)', X the record's own date)\")\ns=s.replace(\" The kind (bill or not) is read from the declared table with this file's own matcher.\",\"\")\ns=s.replace(\"'date of service [__________] (statement dated X)' on a bill or '(record dated X)' on any other record, X the record's own date.\",\"'date of service [__________] (record dated X)', X the record's own date.\")\nopen(p,'w').write(s)\nEOF\ngit diff --stat -- app evals | tail -8; grep -n \"_record_kind\\|statement dated\" evals/letter_check.py app/backend/export.py app/backend/store.py app/backend/service_date.py"
}
````

### User / tool · 2026-11-03T15:09:09.932Z

**tool result**
````
 app/backend/export.py       |  4 ++--
 app/backend/service_date.py | 20 ++++++++++----------
 app/backend/store.py        |  7 +++----
 evals/letter_check.py       | 10 +++++-----
 4 files changed, 20 insertions(+), 21 deletions(-)
evals/letter_check.py:201:def _record_kind(source, excerpt=""):
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:12.550Z

**tool call — Bash**
````
{
 "command": "grep -n \"_TYPES\\|_words\\|_has_term\\|_record_kind\" evals/letter_check.py evals/*.py tests -r | head -20; sed -n 170,210p evals/letter_check.py"
}
````

### User / tool · 2026-11-03T15:09:12.639Z

**tool result**
````
evals/letter_check.py:189:_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))
evals/letter_check.py:192:def _words(text):
evals/letter_check.py:196:def _has_term(text_words, term):
evals/letter_check.py:197:    t = _words(term)
evals/letter_check.py:198:    return any(text_words[i:i + len(t)] == t for i in range(len(text_words) - len(t) + 1))
evals/letter_check.py:201:def _record_kind(source, excerpt=""):
evals/letter_check.py:205:    src_w, open_w = _words(source), _words(re.split(r"[:.\n]", (excerpt or "")[:int(_TYPES["opening_chars"])])[0])
evals/letter_check.py:206:    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["financial"]):
evals/letter_check.py:208:    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["administrative"]):
evals/letter_check.py:210:    return "encounter" if any(_has_term(src_w, t) for t in _TYPES["encounter"]) else "other"
evals/letter_check.py:189:_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))
evals/letter_check.py:192:def _words(text):
evals/letter_check.py:196:def _has_term(text_words, term):
evals/letter_check.py:197:    t = _words(term)
evals/letter_check.py:198:    return any(text_words[i:i + len(t)] == t for i in range(len(text_words) - len(t) + 1))
evals/letter_check.py:201:def _record_kind(source, excerpt=""):
evals/letter_check.py:205:    src_w, open_w = _words(source), _words(re.split(r"[:.\n]", (excerpt or "")[:int(_TYPES["opening_chars"])])[0])
evals/letter_check.py:206:    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["financial"]):
evals/letter_check.py:208:    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["administrative"]):
evals/letter_check.py:210:    return "encounter" if any(_has_term(src_w, t) for t in _TYPES["encounter"]) else "other"
            if it["kind"] == "charge" and it["review_status"] in ("accepted", "edited") and it.get("value_cents") is not None and it["state"] != "rejected"]


BLANK = "date of service [__________]"          # D-073 fallback: the ONLY printed form of a charge line's date


def charge_lines(letter: str) -> list:
    """[(header, quote)] of the BILLED CHARGES section, by structure (a header ends ': $X.XX'; the next line is its Source line)."""
    from app.backend import export
    _, tail = export.split_letter(letter)
    out = []
    for i, line in enumerate(tail):
        if re.search(r": \$[\d,]+\.\d\d$", line) and not line.startswith(TOTAL) and i + 1 < len(tail):
            q = tail[i + 1]
            out.append((line, q[q.index('"') + 1:q.rindex('"')] if '"' in q else q))
    return out


TYPES_PATH = ROOT / "app" / "backend" / "encounter_types.json"          # D-071 amendment 2: the ONE declared table of record types (production reads the same file)
_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))


def _words(text):
    return re.findall(r"[^\W_]+", (text or "").lower())


def _has_term(text_words, term):
    t = _words(term)
    return any(text_words[i:i + len(t)] == t for i in range(len(text_words) - len(t) + 1))


def _record_kind(source, excerpt=""):
    """'bill' | 'encounter' | 'other', read from the declared table with this file's own matcher: financial words in the source label or the opening of the excerpt (its first characters up to the first colon or full stop) make a bill,
    administrative words make 'other', and a record is an ENCOUNTER only when its source label names one (a visit, ER, clinic, therapy, imaging, ambulance-run note ...). Only an encounter
    lends the line its own date."""
    src_w, open_w = _words(source), _words(re.split(r"[:.\n]", (excerpt or "")[:int(_TYPES["opening_chars"])])[0])
    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["financial"]):
        return "bill"
    if any(_has_term(w, t) for w in (src_w, open_w) for t in _TYPES["administrative"]):
        return "other"
    return "encounter" if any(_has_term(src_w, t) for t in _TYPES["encounter"]) else "other"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:15.221Z

Remove the dead classifier from letter_check (lines 186–210).

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:16.457Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='evals/letter_check.py'; s=open(p).read()\na=s.index('TYPES_PATH = ROOT'); b=s.index('def charge_date_violations')\ns=s[:a]+s[b:]\nopen(p,'w').write(s)\nEOF\npython3 -c \"import ast;ast.parse(open('evals/letter_check.py').read())\"; grep -n \"ROOT\\|^import\\|^from\\|json\\.\" evals/letter_check.py | head -20"
}
````

### User / tool · 2026-11-03T15:09:16.599Z

**tool result**
````
21:import contextlib
22:import json
23:import pathlib
24:import re
25:import sys
26:import tempfile
28:ROOT = pathlib.Path(__file__).resolve().parents[1]
29:GOLD, LIB = ROOT / "evals" / "golden", ROOT / "evals" / "library"
282:    print(json.dumps({k: v for k, v in m.items() if k != "per_case"}))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:17.747Z

Now docs, frontend, tests.

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:19.053Z

**tool call — Bash**
````
{
 "command": "sed -n 28,42p app/frontend/guided/step3.js | cut -c1-420; sed -n 120,130p app/frontend/guided/step3.js | cut -c1-300; grep -n \"stmtDated\\|stmtOnly\\|dateWord\" app/frontend/guided/*.js | cut -c1-200; grep -n \"statement\" spec/REQUIREMENTS.md | sed -n 1,20p | cut -c1-200; sed -n 113p memory/SCOPE_CUTS.md | cut -c1-500"
}
````

### User / tool · 2026-11-03T15:09:19.159Z

**tool result**
````
  const figure = (a) => (cents(a) != null ? R.money(cents(a)) : a.text || "");
  const FLAG_BOX = { likely_duplicate: "I checked: this is a separate charge, not the same one counted twice.", likely_total: "I checked: this is a charge of its own, not a total of the others." };
  const flagBox = (f) => FLAG_BOX[f.flag] || `I checked: ${String(f.name || f.flag || "this is right").replace(/\.$/, "")}.`;

  /* the date of service exactly as the letter prints it; the statement date, when different, is named as that */
  const dateLine = (sd) => h("p", { class: "svc-date gap-top", "data-testid": "service-date", "data-state": sd.state },
    /^date of service/i.test(sd.text || "") ? null : h("span", { class: "label-cap" }, "Date of service "), h("b", { "data-testid": "service-date-text" }, sd.text || ""),
    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · ${dateWord(sd)} dated ${R.longDate(sd.statement_date_iso)}`) : null);
  const confirmNote = (sd) => h("strong", { class: "svc-note", role: "note", "data-testid": "confirm-note" }, R.plain(sd.confirm_note));
  /* T-206/T-209 r3: the note above states the specific reason; this sentence is the same for every reason that is not certain, so it can never contradict the note: find the date outside this card's guess, write it in the letter's blank. The card has no control to type a date. */
  const confirmNext = (sd) => {
    const paren = /\((statement|record) dated/.exec((sd && sd.text) || ""), stmt = paren ? ` The date in parentheses is the ${paren[1]} date, not the service date.` : "";
    return h("p", { class: "svc-next", "data-testid": "confirm-next" }, h("b", {}, "What to do: "), "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank ", h("b", {}, "\u201Cdate of service [__________]\u201D"), " in your letter." + stmt,
      " Counting it adds the amount to the bill total.");
  };
  /* ---------- 6.4 done ---------- */
  function letterLine(c) { const t = c.totals || {}; return t.letter_line || `Billed charges accepted from these records: ${R.money((t.accepted || {}).cents || 0)}`; }
  function done(S) {
    const c = S.c, items = S.counted().map((q) => S.item(q.id)), recs = Object.fromEntries((c.records || []).map((r) => [r.id, r]));
    const left = items.filter(G.steps.undecided), changeHref = (a) => G.url.bills(S.token, a.id);
    const from = (a) => { const r = recs[(a.record_ids || [])[0]]; return r ? r.source_label || "" : ""; }, when = (a) => {
      const sd = sdOf(a); if (sd && sd.text) return sd.text;          // the letter's own date text
      const r = recs[(a.record_ids || [])[0]], d = r && r.date_iso ? R.longDate(r.date_iso) : "", by = a.ladder && a.ladder.code_checks && a.ladder.code_checks.classified_by;
      return d && /^reviewer:counted/.test(by || "") ? `No date of service (statement dated ${d})` : d;          // a ledger line she counted states no date of service: the record's date is the statement's
    };
    const counted = items.filter((a) => a.kind === "charge" && (a.review_status === "accepted" || a.review_status === "edited") && !a.edit_to_check);
app/frontend/guided/step3.js:20:  const stmtOnly = (sd) => !!sd && !!sd.statement_date_iso && !(sd.state === "stated" && sd.date_iso === sd.statement_date_iso && !sd.end_iso);      // a bill's date, n
app/frontend/guided/step3.js:23:  const stmtDated = (item, sd, rec) => stmtOnly(sd) || (!sd && !!item && (kindOf(item) === "count" || BILL_DOC.test((rec && rec.source_label) || "")));
app/frontend/guided/step3.js:25:  const dateWord = (sd) => (sd && sd.date_label === "record" ? "record" : "statement");
app/frontend/guided/step3.js:35:    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · ${dateWord(sd)} dated ${R.longDate(sd.statement_date_iso
app/frontend/guided/step3.js:46:    const sd = sdOf(item), st = stmtDated(item, sd, rec) && dateWord(sd);
app/frontend/guided/step3.js:48:    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? r
8:**User.** A paralegal at a personal-injury firm. She reviews rather than trusts. Every statement the tool makes must be checkable against its source (A-101: she builds the chronology, the attorney s
12:2. **Internal review notes — do not send**: accepted flags, flagged language quoted in the letter, amounts not totaled, damages mentions, future treatment recommended, bills to request, records l
61:Four types: `gap`, `conflict`, `pre_existing`, `causation`. Gap math is code over the header dates of clinical-encounter records (D-003): billing statements and phone notes are excluded, duplicates
65:| R-FL-1 | **Treatment gap.** Flag when days between consecutive dates of service across all providers (A-102) is **greater than 30** (A-104). Only clinical-encounter records count (D-003): billing
120:| R-EX-2 | Every entry and charge in the letter carries a source line with the verbatim excerpt. No short-cite mode (D-002). | UT: for every statement and amount line in `letter_text`, the quoted 
196:6. **Medical or legal judgment.** No diagnosis, severity rating, causation opinion or statement of what a record "means." Flags point at the record's own words. Whether a flagged sentence goes out
329:| 1 | **Grounding** | 100% of exported statements and amounts carry a verbatim excerpt present in the input. Any miss is a blocker. | Eval metric `grounding_rate` (excerpts, providers, amounts, da
332:| 4 | **No invented facts** | 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding). Judge recall on seeded hallucinations ≥ 95% of every item in `hallucinations
| 28 | Service-date extraction for letter charge lines (D-073 fallback) | No service date is extracted for the letter: every charge line prints the fillable blank "date of service [__________] (record dated X)" or "(statement dated X)" and Step 3 asks the user to fill it from the record. Six review rounds showed that reading dates from tables, encounter records and prose kept printing wrong dates on new layouts. | A labelled-span parser with an adversarial corpus and a paralegal-built test set;
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:25.551Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/frontend/guided/step3.js'; s=open(p).read()\ns=s.replace('''/* T-211 (T-202 r6): service_date.date_label says what the record's date is called: \"statement\" for a bill, \"record\" for any other record. No service_date (a ledger line not counted yet) is a bill document's: \"statement\". */\n  const dateWord = (sd) => (sd && sd.date_label === \"record\" ? \"record\" : \"statement\");''','''/* D-075 (T-202 r7): the record's own date is always called \"record dated\"; the app never classifies a source as a bill or a clinical record. */\n  const dateWord = () => \"record\";''')\ns=s.replace('''const paren = /\\\\((statement|record) dated/.exec((sd && sd.text) || \"\"), stmt = paren ? ` The date in parentheses is the ${paren[1]} date, not the service date.` : \"\";''','''const paren = /\\\\(record dated/.test((sd && sd.text) || \"\"), stmt = paren ? \" The date in parentheses is the record date, not the service date.\" : \"\";''')\ns=s.replace(\"No date of service (statement dated ${d})` : d;          // a ledger line she counted states no date of service: the record's date is the statement's\",\"No date of service (record dated ${d})` : d;          // a ledger line she counted states no date of service\")\ns=s.replace('the record\\'s own date is called the statement date whenever it is not that day','the record\\'s own date is called the record date whenever it is not that day')\nopen(p,'w').write(s)\nEOF\ngit diff app/frontend | grep '^[+-]' | cut -c1-200; grep -n \"statement\" tests/e2e/guided/test_step3.py | head"
}
````

### User / tool · 2026-11-03T15:09:25.681Z

**tool result**
````
--- a/app/frontend/guided/step3.js
+++ b/app/frontend/guided/step3.js
-  /* T-205 (D-071): a charge's date is the service date the letter prints (amounts[].service_date.text, byte for byte); the record's own date is called the statement date whenever it is not that day.
+  /* T-205 (D-071): a charge's date is the service date the letter prints (amounts[].service_date.text, byte for byte); the record's own date is called the record date whenever it is not that day. Co
-  /* T-211 (T-202 r6): service_date.date_label says what the record's date is called: "statement" for a bill, "record" for any other record. No service_date (a ledger line not counted yet) is a bill 
-  const dateWord = (sd) => (sd && sd.date_label === "record" ? "record" : "statement");
+  /* D-075 (T-202 r7): the record's own date is always called "record dated"; the app never classifies a source as a bill or a clinical record. */
+  const dateWord = () => "record";
-    const paren = /\((statement|record) dated/.exec((sd && sd.text) || ""), stmt = paren ? ` The date in parentheses is the ${paren[1]} date, not the service date.` : "";
+    const paren = /\(record dated/.test((sd && sd.text) || ""), stmt = paren ? " The date in parentheses is the record date, not the service date." : "";
-      return d && /^reviewer:counted/.test(by || "") ? `No date of service (statement dated ${d})` : d;          // a ledger line she counted states no date of service: the record's date is the state
+      return d && /^reviewer:counted/.test(by || "") ? `No date of service (record dated ${d})` : d;          // a ledger line she counted states no date of service
300:        j["totals"]["possible_overlaps"] = [{"code": "POSSIBLE_OVERLAP", "statement_amount_id": "a1", "covered_amount_id": "a4", "statement_text": "$6,240", "covered_text": "$2,150",
301:                                             "message": "A statement line may already include a separately stated charge for the same kind of service. Check whether both belong in the total."}]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:29.105Z

**tool call — Bash**
````
{
 "command": "sed -n 20,75p tests/unit/test_t202_r7_all_blank.py; sed -n 25,40p tests/unit/test_t200_undated_charge_label.py; sed -n 70,82p tests/unit/test_t200_undated_charge_label.py"
}
````

### User / tool · 2026-11-03T15:09:29.194Z

**tool result**
````
@pytest.mark.parametrize("src,ex,fig", SHAPES)
def test_nothing_is_stated_but_the_reader_still_reads(src, ex, fig):
    pos = ex.index(fig)
    assert SD.read(ex, pos, src, "2026-06-15")["state"] == "stated"          # the dormant reader: the control that the fixtures are real
    assert SD.resolve(ex, pos, src, "2026-06-15")["state"] == "not_stated"
    d = store.charge_service_date(_item(ex, fig), {"source": src, "date_iso": "2026-06-15"}, pos)
    kind = "statement" if SD.record_kind(src, ex) == "bill" else "record"
    assert d["state"] == "not_stated" and d["date_iso"] is None and d["end_iso"] is None
    assert d["text"] == f"date of service [__________] ({kind} dated June 15, 2026)" and d["date_label"] == kind
    assert d["confirm_note"] and "leaves a blank" in d["confirm_note"]
    assert store.charge_service_dates(_item(ex, fig), {"source": src, "date_iso": "2026-06-15"}, pos) == (None, None)


def test_a_line_the_reader_would_have_dated_gets_the_reason_not_read():
    ex = VISIT
    assert SD.resolve(ex, ex.index("$250.00"), NOTE, "2026-06-15")["reason"] == "not_read"
    assert "does not take a date of service" in SD.confirm_note("not_read", "")


def _case(**ch):
    return {"records": [{"n": 1, "source": LEDGER, "date_iso": "2026-06-15", "excerpt": "New patient exam charge $250.00."}], "entries": [], "flags": [], "pending_count": 0, "events": [],
            "amounts": [dict(id="a1", record_no=1, cents=25000, cls="charge", raw="$250.00", excerpt="New patient exam charge $250.00.", review_status="accepted", **ch)]}


@pytest.mark.parametrize("extra", [{}, {"dos_iso": None}, {"dos_iso": "2026-03-27"}, {"dos_iso": "2026-06-09", "dos_end_iso": "2026-06-12"}, {"dos_iso": "2026-03-27", "dos_text": "March 27, 2026"}])
def test_the_letter_prints_the_blank_whatever_the_case_dict_carries(extra):
    out = export.build_export(_case(**extra), None)
    assert f"{LEDGER}, date of service [__________] (statement dated June 15, 2026): $250.00" in out["letter_text"].split("\n")
    assert "March 27" not in out["letter_text"] and "June 9" not in out["letter_text"]
    assert "CHARGES WITHOUT A CERTAIN DATE OF SERVICE" in out["internal_notes_text"]


def _check(head, source=LEDGER, ex="New patient exam charge $250.00.", rd="2026-06-15"):
    letter = f"BILLED CHARGES\n\n{head}: $250.00\nSource [Ex. __ / Bates __]: \"{ex}\"\n\nBilled charges accepted from these records: $250.00"
    return LC.charge_date_violations(letter, [{"n": 1, "source": source, "date_iso": rd, "excerpt": ex}])


BLANK_OK = f"{LEDGER}, date of service [__________] (statement dated June 15, 2026)"


def test_letter_check_accepts_the_exact_blank_only():
    assert _check(BLANK_OK) == []
    assert _check(f"{LEDGER}, date of service [__________]", rd=None) == []
    assert _check(f"{NOTE}, date of service [__________] (record dated June 15, 2026)", NOTE, "Exam charge $250.00.") == []
    for bad in (f"{LEDGER}, June 15, 2026", f"{LEDGER}, March 27, 2026", f"{LEDGER}, June 9–12, 2026", f"{LEDGER}, date of service [__________] (statement dated June 16, 2026)",
                f"{LEDGER}, date of service [__________] (record dated June 15, 2026)", f"{LEDGER}, date of service [__________]", f"{LEDGER}, date of service [__________] (statement dated June 15, 2026) x",
                f"{LEDGER}, date of service [_________] (statement dated June 15, 2026)", f"Other, date of service [__________] (statement dated June 15, 2026)"):
        assert _check(bad), bad
    assert _check(f"{NOTE}, date of service [__________] (statement dated June 15, 2026)", NOTE, "Exam charge $250.00.")          # an encounter record's date is its record date
    assert _check(BLANK_OK, rd=None)          # the record has no date, so no parenthesis


def test_letter_check_fails_a_dated_letter_over_the_corpus_sample():
    letters = LC.letters_for(open("evals/golden/sample.txt").read())
    got = letters["all_accepted"]
    am = by_text(c, tok)
    ed = next(a for a in am.values() if a["kind"] == "charge")
    assert c.post(f"/api/cases/{tok}/items/{ed['id']}/review", json={"action": "accept"}).status_code == 200
    for fig in ("$250.00", "$180.00", "$2,310.00"):
        assert count(c, tok, am[fig]["id"], confirm="separate_charge").status_code == 200
    lines = _letter(c, tok, style).split("\n")
    for fig in ("$250.00", "$180.00", "$2,310.00"):
        assert STATEMENT + fig in lines, (fig, [l for l in lines if fig in l])
    assert not any(BARE.search(l) for l in lines), [l for l in lines if BARE.search(l)]          # no bare statement date in the charge section
    assert "Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026): $3,260.00" in lines          # D-073: an ED provider name is not a document type, so no record date
    assert "Billed charges accepted from these records: $6,000.00" in lines
    assert "March 27, 2026" in "\n".join(lines)                                                  # the visit date the old line contradicted is still in the chronology


def test_a_counted_line_keeps_its_citation_and_quote(lib11):
    c, tok = lib11
    return {"records": [{"n": 1, "source": "Fennimoor Spine Clinic, itemized ledger", "date_iso": "2026-06-15", "excerpt": "New patient exam charge $250.00."}],
            "entries": [], "flags": [], "pending_count": 0, "events": [],
            "amounts": [dict(id="a1", record_no=1, cents=25000, cls="charge", raw="$250.00", excerpt="New patient exam charge $250.00.", review_status="accepted", **charge)]}


def test_export_label_rules_on_a_hand_built_case():
    def line(**ch):
        return next(l for l in export.build_export(_case(**ch), None)["letter_text"].split("\n") if l.endswith("$250.00"))
    assert line(dos_iso=None, dos_end_iso=None) == "Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00"
    blank = "Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00"
    assert line(dos_iso="2026-03-27", dos_end_iso=None) == blank          # D-073 fallback: a hand-built case's date is not printed either
    assert line(dos_iso="2026-06-09", dos_end_iso="2026-06-12") == blank
    assert line() == blank
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:30.020Z

Edit the tests.

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:34.407Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\n# simple replace in tests\nfor p in ['tests/unit/test_t200_undated_charge_label.py','tests/e2e/guided/test_round2.py','tests/e2e/guided/test_t205.py']:\n    s=open(p).read(); s=s.replace(\"(statement dated\",\"(record dated\").replace(\"statement dated\",\"record dated\"); open(p,'w').write(s)\np='tests/unit/test_t202_r7_all_blank.py'; s=open(p).read()\ns=s.replace('''    kind = \"statement\" if SD.record_kind(src, ex) == \"bill\" else \"record\"\\n''','')\ns=s.replace('({kind} dated June 15, 2026)\" and d[\"date_label\"] == kind','(record dated June 15, 2026)\" and d[\"date_label\"] == \"record\"')\ns=s.replace(\"(statement dated June 15, 2026)\",\"(record dated June 15, 2026)\")\ns=s.replace(\"(statement dated June 16, 2026)\",\"(record dated June 16, 2026)\")\ns=s.replace(\"(statement|record dated X)\",\"(record dated X)\")\n# the bad-list: now the statement variant is the bad form\ns=s.replace('''f\"{LEDGER}, date of service [__________] (record dated June 15, 2026)\", f\"{LEDGER}, date of service [__________]\", f\"{LEDGER}, date of service [__________] (record dated June 15, 2026) x\",''','''f\"{LEDGER}, date of service [__________] (statement dated June 15, 2026)\", f\"{LEDGER}, date of service [__________]\", f\"{LEDGER}, date of service [__________] (record dated June 15, 2026) x\",''')\ns=s.replace('''    assert _check(f\"{NOTE}, date of service [__________] (record dated June 15, 2026)\", NOTE, \"Exam charge $250.00.\")          # an encounter record's date is its record date''','''    assert _check(f\"{NOTE}, date of service [__________] (statement dated June 15, 2026)\", NOTE, \"Exam charge $250.00.\")          # D-075: the statement variant is gone for every source''')\nopen(p,'w').write(s)\nEOF\ngrep -n \"statement\" tests/unit/test_t202_r7_all_blank.py tests/e2e/guided/test_t206.py tests/e2e/guided/test_t205.py tests/e2e/guided/test_step3.py | cut -c1-240"
}
````

### User / tool · 2026-11-03T15:09:34.527Z

**tool result**
````
tests/unit/test_t202_r7_all_blank.py:65:                f"{LEDGER}, date of service [__________] (statement dated June 15, 2026)", f"{LEDGER}, date of service [__________]", f"{LEDGER}, date of service [__________] (record dated June 15, 20
tests/unit/test_t202_r7_all_blank.py:68:    assert _check(f"{NOTE}, date of service [__________] (statement dated June 15, 2026)", NOTE, "Exam charge $250.00.")          # D-075: the statement variant is gone for every source
tests/e2e/guided/test_step3.py:300:        j["totals"]["possible_overlaps"] = [{"code": "POSSIBLE_OVERLAP", "statement_amount_id": "a1", "covered_amount_id": "a4", "statement_text": "$6,240", "covered_text": "$2,150",
tests/e2e/guided/test_step3.py:301:                                             "message": "A statement line may already include a separately stated charge for the same kind of service. Check whether both belong in the total."}]
tests/e2e/guided/test_t206.py:2:taken from a bill document (the rest of the ledger) names its record's date "statement dated ...", on the card head, the line under it and the source head; the confirm note ends with what to do next in
tests/e2e/guided/test_t206.py:12:BARE = re.compile(r"(?<!statement dated )(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}")
tests/e2e/guided/test_t206.py:19:def test_lib11_uncounted_ledger_lines_never_show_a_bare_statement_date(page, make):
tests/e2e/guided/test_t206.py:27:        assert "statement dated June 15, 2026" in t["src-head"] and "statement dated June 15, 2026" in t["line-sub"], (iid, t)
tests/e2e/guided/test_t206.py:31:    # the ED charge's source label names only the provider (D-073): no document type, so its header date is not lent and the blank prints with the statement date named
tests/e2e/guided/test_t206.py:33:    assert page.get_by_test_id("service-date-text").inner_text() == "date of service [__________] (record dated March 18, 2026)"          # T-202 r6 rule 4: an ED record is a record, not a statement 
tests/e2e/guided/test_t206.py:45:    assert sd["state"] == "not_stated" and "statement dated June 15, 2026" in sd["text"]
tests/e2e/guided/test_t206.py:90:    assert "The date in parentheses is the statement date, not the service date." in t
tests/e2e/guided/test_t205.py:2:certain. Never the statement date as the service date. Real browser, the fixture backend, the real API. case_09 (record dated Mar 1, service Feb 2), lib10 (one UB-04 period, June 9-12, statement June 19),
tests/e2e/guided/test_t205.py:47:def test_case_09_shows_the_blank_not_the_statement_date_as_the_service_date(page, made_text):
tests/e2e/guided/test_t205.py:48:    """D-073 (T-202 r5): 'Statement for visit of 2026-02-02' is a sentence, which the code does not read, so the bill line shows the fillable blank and names the statement date as the statement's."""
tests/e2e/guided/test_t205.py:51:    assert sd["state"] == "not_stated" and sd["date_iso"] is None and sd["statement_date_iso"] == "2026-03-01" and sd["confirm_note"]
tests/e2e/guided/test_t205.py:56:    assert "record dated March 1, 2026" in page.get_by_test_id("src-head").inner_text(), "the record's own date is named as the statement's, never bare"
tests/e2e/guided/test_t205.py:58:    assert "billing statement, date of service [__________] (record dated March 1, 2026): $275.00" in letter_dates(tok), "the same text the letter prints"
tests/e2e/guided/test_t205.py:70:        sd = a["service_date"]; assert sd["text"] == blank and sd["state"] == "not_stated" and sd["date_iso"] is None and sd["statement_date_iso"] == "2026-06-19"
tests/e2e/guided/test_t205.py:81:def test_a_charge_with_no_stated_date_shows_the_not_stated_text_and_never_the_statement_date_as_the_service_date(page, make):
tests/e2e/guided/test_t205.py:129:    assert page.get_by_test_id("statement-date").count() == 0, "the not-stated text already names the statement date"
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:38.195Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/guided/test_t206.py'; s=open(p).read()\ns=s.replace('(?<!statement dated )','(?<!record dated )').replace('\"statement dated ...\", on','\"record dated ...\", on')\ns=s.replace('\"statement dated June 15, 2026\"','\"record dated June 15, 2026\"')\ns=s.replace(\"is the statement date, not the service date.\",\"is the record date, not the service date.\")\nopen(p,'w').write(s)\nEOF\nsed -n 14,32p tests/e2e/guided/test_t206.py | cut -c1-260; sed -n 85,100p tests/e2e/guided/test_t205.py | cut -c1-260; sed -n 120,130p tests/e2e/guided/test_t205.py | cut -c1-200"
}
````

### User / tool · 2026-11-03T15:09:38.309Z

**tool result**
````
def texts(page):
    return {k: page.get_by_test_id(k).inner_text() for k in ("card-line", "line-sub", "src-head")}


def test_lib11_uncounted_ledger_lines_never_show_a_bare_statement_date(page, make):
    seen = watch(page)
    tok = make(LIB11); amounts = {a["id"]: a for a in case(tok)["amounts"]}
    uncounted = [i for i, a in amounts.items() if a["kind"] != "charge"]
    assert {"a2", "a3", "a4"} <= set(uncounted) and amounts["a2"]["countable"] and amounts["a2"]["service_date"] is None
    for iid in uncounted:         # the three countable lines and the four never counted: all of them are the ledger
        open_item(page, tok, iid, step="bills")
        t = texts(page)
        assert "record dated June 15, 2026" in t["src-head"] and "record dated June 15, 2026" in t["line-sub"], (iid, t)
        for k, v in t.items():
            assert not BARE.search(v), (iid, k, v)
        assert page.get_by_test_id("confirm-note").count() == 0
    # the ED charge's source label names only the provider (D-073): no document type, so its header date is not lent and the blank prints with the statement date named
    open_item(page, tok, "a1", step="bills")
    st, r = C.api("POST", f"/api/cases/{tok}/items/a2/review", {"action": "count", "confirm": "separate_charge", "version": a["version"], "expected_status": "pending",
                                                              **({"confirm_flag": a["count_confirm"]["confirm_with"]} if a.get("count_confirm") else {})}); assert st == 200, r
    a = item(tok, "a2"); sd = a["service_date"]
    assert a["kind"] == "charge" and sd["state"] == "not_stated" and sd["date_iso"] is None and sd["confirm_note"] is None
    open_item(page, tok, "a2", step="bills")
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    assert re.fullmatch(r"date of service \[_{10}\] \(record dated [A-Z][a-z]+ \d{1,2}, \d{4}\)|date of service \[_{10}\]", sd["text"]), sd["text"]
    assert page.get_by_test_id("service-date").get_attribute("data-state") == "not_stated"
    assert page.get_by_test_id("confirm-note").count() == 0
    assert f"{sd['text']}: " in letter_dates(tok), "the letter prints this very text"
    assert "record dated" in page.get_by_test_id("src-head").inner_text() or "no date" in page.get_by_test_id("src-head").inner_text()
    # done list: decide the rest over the API, the Date of service column carries the same text
    for i in case(tok)["amounts"]:
        if i["review_status"] == "pending" and i["id"] != "a2":
            C.api("POST", f"/api/cases/{tok}/items/{i['id']}/review", {"action": "accept"})
    go(page, f"/case/{tok}/bills")
    open_item(page, tok, "a2", step="bills")
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    assert page.get_by_test_id("service-date").get_attribute("data-state") == "not_stated"
    note = page.get_by_test_id("confirm-note"); expect(note).to_be_visible(); assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-note]").count() == 1
    t = note.inner_text()
    assert "04/05/2026" in t and "The letter prints no service date for this line." in t and "Confirm the date from the highlighted words" in t, t      # the server's sentence, in the plain vocabulary
    assert not re.search(r"\bquote\b|\bmodel\b|\bexcerpt\b", t, re.I), t
    assert note.get_attribute("role") == "note"
    assert "record dated June 19, 2026" in page.get_by_test_id("src-head").inner_text()
    assert page.get_by_test_id("statement-date").count() == 0, "the not-stated text already names the statement date"
    # nothing about the decision changes: the human still answers Yes or No
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:39.506Z

Now api.md.

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:45.395Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='memory/contracts/api.md'; s=open(p).read()\nn=s.count('statement dated')\nreps=[\n(\"**D-073 FALLBACK APPLIED (T-202 r7, supersedes the rest of this paragraph for what the letter and the case view print): the code extracts NO service date. Every charge line in the letter is `<source label>, date of service [__________] (statement dated June 15, 2026): $X` for a bill, `(record dated June 15, 2026)` for any other record, and no parenthesis when the record has no date.\",\n \"**D-073 FALLBACK APPLIED (T-202 r7, supersedes the rest of this paragraph for what the letter and the case view print; D-075 simplified the label): the code extracts NO service date. Every charge line in the letter is `<source label>, date of service [__________] (record dated June 15, 2026): $X` whatever the source (the label never says bill or statement; the code does not classify a source as a bill), and no parenthesis when the record has no date.\"),\n(\"`<provider>, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00` for a bill, `Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026): $3,260.00` for any other record (D-073 round 6, rule 4; `<provider>, itemized ledger, date of service [__________]: $250.00` when the record has no date either)\",\n \"`<provider>, itemized ledger, date of service [__________] (record dated June 15, 2026): $250.00` (D-075: always \\\"record dated\\\"; `<provider>, itemized ledger, date of service [__________]: $250.00` when the record has no date)\"),\n('\"date of service [__________] (statement dated June 15, 2026)\" | \"date of service [__________] (record dated June 15, 2026)\", \"statement_date_iso\": \"2026-06-19\"|null (the record\\'s date; for a bill it is the statement\\'s), \"date_label\": \"statement\"|\"record\" (T-202 r6: what that date is called: \"statement\" for a bill, \"record\" for any other record, so a client labels it \"statement dated\" or \"record dated\" and never calls an ED record a statement)',\n '\"date of service [__________] (record dated June 15, 2026)\", \"statement_date_iso\": \"2026-06-19\"|null (the record\\'s own date; the field name is kept), \"date_label\": \"record\" (D-075: always; a client labels the date \"record dated\" and never classifies the source)'),\n(\"followed by `(statement dated X)` for a bill or `(record dated X)` for any other record (the bare blank when the record has no date)\",\n \"followed by `(record dated X)` (D-075; the bare blank when the record has no date)\"),\n]\nfor a,b in reps:\n    assert a in s, a[:60]\n    s=s.replace(a,b)\nprint(n, s.count('statement dated'))\nopen(p,'w').write(s)\nEOF\ngrep -n \"statement dated\" memory/contracts/api.md | cut -c1-300"
}
````

### User / tool · 2026-11-03T15:09:45.510Z

**tool result**
````
5 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:49.981Z

**tool call — Bash**
````
{
 "command": "T=/private/tmp/claude-501/t202r8 && rm -rf $T && mkdir -p $T && git archive HEAD | tar -x -C $T && for f in app/backend/service_date.py app/backend/store.py app/backend/export.py evals/letter_check.py app/frontend/guided/step3.js memory/contracts/api.md tests/unit/test_t200_undated_charge_label.py tests/unit/test_t202_r7_all_blank.py tests/e2e/guided/test_round2.py tests/e2e/guided/test_t205.py tests/e2e/guided/test_t206.py; do cp $f $T/$f; done; ls -a .env 2>/dev/null; ls $T | head -30; cd $T && ls tests/unit | grep -i \"date\\|export\\|service\\|t202\\|t200\\|letter\" "
}
````

### User / tool · 2026-11-03T15:09:51.761Z

**tool result**
````
.env
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
app
artifacts
board
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
run.sh
spec
submission
tests
tools
test_conflict_candidates.py
test_date_convention.py
test_date_unconfirmed.py
test_dates.py
test_export.py
test_export_edge.py
test_t116_r4_all_dated_records.py
test_t121_letter_styles.py
test_t139_letter_eval.py
test_t200_undated_charge_label.py
test_t202_r7_all_blank.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:54.956Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/t202r8 && ls tests/unit | grep -i \"t20[0-9]\\|service\"; (python3 -m pytest -q -x tests/unit/test_t200_undated_charge_label.py tests/unit/test_t202_r7_all_blank.py tests/unit/test_export.py tests/unit/test_export_edge.py tests/unit/test_dates.py tests/unit/test_date_convention.py tests/unit/test_date_unconfirmed.py tests/unit/test_t121_letter_styles.py tests/unit/test_t139_letter_eval.py $(ls tests/unit/test_t202*.py tests/unit/test_service*.py tests/unit/test_t20[0-9]*.py 2>/dev/null | sort -u) 2>&1 | tail -15)"
}
````

### User / tool · 2026-11-03T15:09:55.076Z

**tool result**
````
test_t200_undated_charge_label.py
test_t202_r7_all_blank.py
test_t208_ai_wording.py
/opt/homebrew/opt/python@3.12/bin/python3.12: No module named pytest
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:09:58.101Z

**tool call — Bash**
````
{
 "command": "ls -d .venv venv 2>/dev/null; cat Makefile | grep -n \"pytest\\|python\" | head -5"
}
````

### User / tool · 2026-11-03T15:09:58.187Z

**tool result**
````
.venv
15:	@.venv/bin/python -m evals.run --out data/evals; rc=$$?; \
21:	.venv/bin/python -m app.config
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:10:00.252Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/t202r8 && P=/Users/arsis/zlayt-pm-project/.venv/bin/python && timeout 580 $P -m pytest -q tests/unit/test_t200_undated_charge_label.py tests/unit/test_t202_r7_all_blank.py tests/unit/test_export.py tests/unit/test_export_edge.py tests/unit/test_dates.py tests/unit/test_date_convention.py tests/unit/test_date_unconfirmed.py tests/unit/test_t121_letter_styles.py tests/unit/test_t139_letter_eval.py tests/unit/test_t208_ai_wording.py 2>&1 | tail -15"
}
````

### User / tool · 2026-11-03T15:10:00.337Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:10:11.361Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/t202r8 && P=/Users/arsis/zlayt-pm-project/.venv/bin/python && $P -m pytest -q tests/unit/test_t200_undated_charge_label.py tests/unit/test_t202_r7_all_blank.py tests/unit/test_export.py tests/unit/test_export_edge.py tests/unit/test_dates.py tests/unit/test_date_convention.py tests/unit/test_date_unconfirmed.py tests/unit/test_t121_letter_styles.py tests/unit/test_t139_letter_eval.py tests/unit/test_t208_ai_wording.py 2>&1 | tail -15",
 "timeout": 580000
}
````

### User / tool · 2026-11-03T15:10:32.126Z

**tool result**
````
........................................................................ [ 58%]
....................................................                     [100%]
124 passed in 20.33s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:10:37.153Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/t202r8 && P=/Users/arsis/zlayt-pm-project/.venv/bin/python && $P -m evals.letter_check 2>&1 | tail -8; $P -m evals.run --check-spec 2>&1 | tail -5; grep -rl \"service_date\\|statement dated\" tests --include=*.py | head -20",
 "timeout": 580000
}
````

### User / tool · 2026-11-03T15:10:47.842Z

**tool result**
````
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
{"spec_matches_golden": true, "letter_equal": true, "internal_notes_equal": true}
tests/unit/test_t200_undated_charge_label.py
tests/unit/test_t202_r7_all_blank.py
tests/unit/test_amounts.py
tests/unit/test_export.py
tests/e2e/guided/test_t205.py
tests/e2e/guided/test_t206.py
tests/e2e/guided/test_round2.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:10:52.579Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/t202r8 && P=/Users/arsis/zlayt-pm-project/.venv/bin/python && $P -m pytest -q tests/e2e/guided/test_step3.py tests/e2e/guided/test_t205.py tests/e2e/guided/test_t206.py tests/unit/test_amounts.py 2>&1 | tail -20",
 "timeout": 590000
}
````

### User / tool · 2026-11-03T15:11:44.068Z

**tool result**
````
........................................................................ [ 65%]
......................................                                   [100%]
110 passed in 50.41s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:11:51.511Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/t202r8 && P=/Users/arsis/zlayt-pm-project/.venv/bin/python && $P -m pytest -q tests/e2e/guided/test_round2.py 2>&1 | tail -5; cd /Users/arsis/zlayt-pm-project && git status --short evals/golden evals/reports 2>/dev/null | head -3; git log --oneline -1",
 "timeout": 590000
}
````

### User / tool · 2026-11-03T15:12:25.107Z

**tool result**
````
.......................                                                  [100%]
23 passed in 32.58s
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
be257c9 docs(release): drop OWNER placeholder clone step from README (T-212)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:12:26.010Z

Commit with temp index, then board.

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:12:28.293Z

**tool call — Bash**
````
{
 "command": "F=\"app/backend/service_date.py app/backend/store.py app/backend/export.py evals/letter_check.py app/frontend/guided/step3.js memory/contracts/api.md tests/unit/test_t200_undated_charge_label.py tests/unit/test_t202_r7_all_blank.py tests/e2e/guided/test_round2.py tests/e2e/guided/test_t205.py tests/e2e/guided/test_t206.py\"\nexport GIT_INDEX_FILE=/private/tmp/claude-501/t202r8.idx; cp .git/index $GIT_INDEX_FILE; git add $F && git commit -q -m \"feat(backend): D-075 charge blank always reads (record dated X); drop statement variant (T-202)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" -- $F; unset GIT_INDEX_FILE; git log --oneline -1; git show --stat HEAD | tail -14"
}
````

### User / tool · 2026-11-03T15:12:28.364Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: F="app/backend/service_date.py app/backend/store.py app/backend/export.py evals/letter_check.py app/frontend/guided/step3.js memory/contracts/api.md tests/unit/test_t200_undated_charge_label.py tests/
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:12:30.349Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/t202r8.idx; cp .git/index $GIT_INDEX_FILE; git add app/backend/service_date.py app/backend/store.py app/backend/export.py evals/letter_check.py app/frontend/guided/step3.js memory/contracts/api.md tests/unit/test_t200_undated_charge_label.py tests/unit/test_t202_r7_all_blank.py tests/e2e/guided/test_round2.py tests/e2e/guided/test_t205.py tests/e2e/guided/test_t206.py; git diff --cached --stat | tail -3"
}
````

### User / tool · 2026-11-03T15:12:30.497Z

**tool result**
````
 tests/unit/test_t200_undated_charge_label.py |  8 +++----
 tests/unit/test_t202_r7_all_blank.py         | 17 +++++++-------
 11 files changed, 54 insertions(+), 81 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:12:32.312Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/t202r8.idx; git commit -q -m \"feat(backend): D-075 charge blank always reads (record dated X); drop statement variant (T-202)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\"; unset GIT_INDEX_FILE; git log --oneline -1; git show --stat HEAD | tail -3; git status --short app tests evals/letter_check.py memory/contracts | head"
}
````

### User / tool · 2026-11-03T15:12:59.140Z

**tool result**
````
check_secrets: ok (11 file(s) scanned staged)
cd7fd27 feat(backend): D-075 charge blank always reads (record dated X); drop statement variant (T-202)
 tests/unit/test_t200_undated_charge_label.py |  8 +++----
 tests/unit/test_t202_r7_all_blank.py         | 17 +++++++-------
 11 files changed, 54 insertions(+), 81 deletions(-)
MM app/backend/export.py
MM app/backend/service_date.py
MM app/backend/store.py
MM app/frontend/guided/step3.js
MM evals/letter_check.py
MM memory/contracts/api.md
MM tests/e2e/guided/test_round2.py
MM tests/e2e/guided/test_t205.py
MM tests/e2e/guided/test_t206.py
MM tests/unit/test_t200_undated_charge_label.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:05.620Z

**tool call — Bash**
````
{
 "command": "git reset -q -- app/backend/service_date.py app/backend/store.py app/backend/export.py evals/letter_check.py app/frontend/guided/step3.js memory/contracts/api.md tests/unit/test_t200_undated_charge_label.py tests/unit/test_t202_r7_all_blank.py tests/e2e/guided/test_round2.py tests/e2e/guided/test_t205.py tests/e2e/guided/test_t206.py; git status --short app tests evals/letter_check.py memory/contracts | head -3; B=\"python3 tools/board.py\"; $B commit T-202 --sha cd7fd27 --agent backend; $B note T-202 --agent backend --text \"D-075 done: date_label always record; export/store/letter_check/api.md/step3.js/tests updated; letter_check 0 violations; check-spec true (archive copy); 124 unit + 110 guided e2e + test_round2 pass. SCOPE_CUTS row 28 and docs/LLM_VS_CODE.md still mention '(statement dated X)' (not my paths).\"; $B handoff T-202 --agent backend --text \"What changed: charge blank is always 'date of service [__________] (record dated X)'; statement/bill classification removed (service_date.date_label, store, export, letter_check dead classifier, step3.js copy, api.md, tests). How verified: from git archive overlay, letter_check 0 violations, --check-spec true, unit date/export/letter files 124 pass, guided step3/t205/t206/amounts 110 pass, round2 23 pass. Left: SCOPE_CUTS row 28 + docs/LLM_VS_CODE.md rows 3/47 still say statement dated (orchestrator/architect). Sample golden and REQUIREMENTS §6 already read record dated; unchanged. Surprise: none.\"; $B move T-202 in_review --agent backend"
}
````

### User / tool · 2026-11-03T15:13:05.983Z

**tool result**
````
?? tests/fixtures/llm/0cc7a873e16a2f0572848c8c047cc0aeb4d32e2b42dfc81274ea28ca63fa3b84.json
?? tests/fixtures/llm/11a811729af462550cae9432916cf92b314ef5912bdbf4fa459763a20caf03b7.json
?? tests/fixtures/llm/2044a87296034da2ca563dedde30cd3b1a42f41df16d53bcbdba36770368e9b7.json
T-202: commit cd7fd27 recorded
noted on T-202
handoff written on T-202
T-202: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T15:13:08.387Z

T-202 is in_review (commit cd7fd27). Every charge blank now reads exactly "date of service [__________] (record dated X)", and the statement variant and the bill/record classification are gone.

- **Verified from a `git archive` overlay:** `letter_check` reports 0 violations and `--check-spec` is true. The date, export, `letter_check` and guided step3/t205/t206/round2 test files pass.
- **Sample golden and REQUIREMENTS §6:** both already read "record dated", so neither needed an edit.
- **Frontend:** `step3.js` had "statement dated" hard-coded, so I changed it.
- **Still stale:** `memory/SCOPE_CUTS.md` row 28 and `docs/LLM_VS_CODE.md` rows 3 and 47 still mention "(statement dated X)". They are outside my paths, so the orchestrator or architect needs to update them.
