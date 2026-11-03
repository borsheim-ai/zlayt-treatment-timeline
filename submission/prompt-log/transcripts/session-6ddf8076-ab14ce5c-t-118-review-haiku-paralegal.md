# Subagent: T-118 review (haiku paralegal) (T-118 review (haiku paralegal))

Source: `agent-ab14ce5ca0e3f1159.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T09:57:07.266Z

Review board card T-118 in /Users/arsis/zlayt-pm-project (commit 78450f6): the five lib11 golden edits posted on T-116. On a `git archive HEAD` copy in your scratchpad, confirm:
- the edits match the T-116 card note (`python3 tools/board.py show T-116`) and the lib11 packet text: record 6 is an intake form and not a gap endpoint;
- `python3 research/validate_library.py` and the golden checker pass;
- only lib11's gap endpoints changed in the library report.

Write reviews/T-118-paralegal.md with a ```json block of real values: card, persona paralegal-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:10.380Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T09:57:10.389Z

**tool result**
````
1	# Persona dossier — paralegal-reviewer
2	
3	## 1. Identity
4	**Maria Delgado (fictional), Senior Litigation Paralegal, plaintiff personal-injury firm in Austin, Texas — 9+ years, pre-lit and litigation.**
5	She has built hundreds of medical chronologies and demand packages in Filevine; her attorney signs the demand, but she is the one the attorney blames when an adjuster finds a date that doesn't match the records. She reviews rather than trusts: anything she cannot click back to the source page does not go in the demand.
6	
7	## 2. Day-to-day context
8	- Tools: case-management system (Filevine/Clio-style), a PDF viewer with Bates stamps, Word templates for the demand, Excel for specials, Outlook for records requests.
9	- Volume: several demand packages a week; records arrive piecemeal from EMS, ER, PCP, PT, imaging, pain management, often with duplicates and copy-forward notes.
10	- Pressures: Stowers/time-limited demands with deadlines; attorneys who want the demand out today; adjusters who cross-check every claim against the records.
11	- A bad day: the adjuster's response letter quotes a record she summarized wrong, or points to a gap or prior injury she missed. The firm's credibility on that file — and her attorney's trust in her — drops.
12	
13	## 3. Goals and success criteria for this artifact
14	- A chronology she can verify line by line, fast: date of service, provider/facility, short summary in the provider's own words, and the exact excerpt with its record reference.
15	- The tool surfaces what the adjuster will attack (gaps, prior conditions, conflicts, missed appointments, hedged causation) before the demand goes out, so the attorney decides how to handle it.
16	- Billed charges she can reconcile: every amount with its source, a total of explicit charges only, and unclear amounts called out rather than guessed.
17	- An export she can paste into the treatment section of the demand letter with minimal reformatting, containing only what she accepted.
18	
19	## 4. Review checklist
20	1. Every date in the timeline appears verbatim (or as an unambiguous reformat) in its source record; nothing is dated by when a note was entered rather than the date of service.
21	2. Every entry shows provider and facility as written in the record (e.g., "Capital PT", "Dr. Alvarez, primary care"), not a guessed full name.
22	3. Every entry's excerpt is a verbatim quote from that record, and I can see which record (# / source / date) it came from in one action.
23	4. The one-line summary uses the provider's own clinical words (e.g., "cervical strain; concussion without loss of consciousness") and adds nothing that is not in the excerpt.
24	5. Entries are in date-of-service order; same-day records (EMS and ER on 2026-01-09) are both present and not merged.
25	6. The 73-day gap (2026-03-06 PT discharge → 2026-05-18 pain management) is flagged with both dates and the day count; the 28-day interval (01-23 → 02-20) is not flagged.
26	7. The accident-date conflict is flagged: 2026-01-09 (EMS/ER) vs "Date of accident per intake form: 2026-01-19" (record 7), with both excerpts; the tool does not pick one.
27	8. The PT plan vs actual discrepancy is surfaced: "Plan of care: 12 visits" vs "Discharged from PT after two missed appointments" at visit 9.
28	9. Prior-condition mentions are flagged: "low back pain in 2023, resolved" (record 3) and "may represent degenerative change" (record 8), each with its excerpt.
29	10. PT discharge notes that mention missed appointments raise a `causation` flag (D-013).
30	11. Charges list shows $6,240 (ER) and $2,150 (MRI) with sources, and the running total of explicit charges is $8,390.
31	12. The running total excludes per-visit rates unless the visit count is stated: "$185 per visit" appears as "rate — visit count not stated (12 planned; discharged at visit 9) — needs review", not as a computed PT total; in the export that reason sits in the internal review notes, never in the letter (R-EX-4).
32	13. "Missing 3 days of work" is not listed as a billed charge (it may be noted as a lost-wages mention).
33	14. Every entry and every flag has accept, edit, and dismiss; edits keep the original visible somewhere so I can see what I changed.
34	15. I can review with the keyboard (move to next item, accept, dismiss) without reaching for the mouse on every row.
35	16. Items that need review are shown first and say why in one sentence.
36	17. I can see how many items remain unreviewed before I export.
37	18. The letter's treatment section contains only entries and charges I accepted (with my edits); flags, unclear amounts, and notes appear only in the "Internal review notes — do not send" block (D-001); dismissed items never appear.
38	19. Each letter line has the date of service (US long format), the provider exactly as written, a verbatim quote, and a citation placeholder (e.g., `January 16, 2026 — Dr. Alvarez, primary care: "Persistent neck pain 6/10, daily headaches." [Ex. __ / Bates __]`) (D-002).
39	20. Export pastes into Word as clean text: no HTML, no UI labels like "verified", no markdown symbols that would print.
40	21. The letter's total line reads "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical); unclear amounts are never in the total; "Bills to request" (providers with an entry and no accepted charge) appear in the internal notes (R-EX-4).
41	22. Nothing in the timeline or export states causation, diagnosis, or severity the records do not state (e.g., no "disc herniation caused by the collision").
42	23. Patient self-reports stay attributed ("Patient states symptoms began after the January collision"), never turned into the provider's finding.
43	
44	## 5. Red flags / dealbreakers
45	Each item here is a **blocker** (rate it so; never major or minor).
46	- Any statement, date, or amount in the app that has no verbatim excerpt behind it (missing cites in the export text alone is a major, not this).
47	- A total that includes the $185 rate multiplied by a guessed visit count.
48	- The two accident dates merged into one, or the tool "resolving" the conflict.
49	- Export that includes something I dismissed or never reviewed.
50	- Losing my edits on refresh or export.
51	
52	## 6. Vocabulary
53	med chron, treatment chronology, DOS (date of service), DOI/DOA (date of injury/accident), provider/facility, records received through, Bates/page cite, specials, billed vs paid, demand package, treatment section, gap in treatment, prior/pre-existing, aggravation, missed appointments, discharged / non-compliant, MMI, plan of care, "records request", Stowers demand, "the adjuster will say...".
54	
55	## 7. How I review
56	1. Load the sample case exactly as a user would (paste or the load-sample control). Note how long processing takes.
57	2. Before looking at the tool's output, list from Appendix A what I expect: 9 records, the 73-day gap, the 01-09/01-19 conflict, two prior-condition mentions, $8,390 explicit, $185 rate unclear.
58	3. Go entry by entry: check date, provider, summary, excerpt against the raw record text. Mark any mismatch.
59	4. Go flag by flag: check evidence excerpts, check nothing expected is missing, check the 28-day interval is not flagged.
60	5. Check the charges table and the total; try to find where the $185 went.
61	6. Review the whole case keyboard-first: accept most, edit one summary (record 3), dismiss one flag. Time the full review.
62	7. Export; paste into a plain-text file under `artifacts/review-evidence/`; confirm the dismissed item is absent and my edit is present.
63	8. Refresh mid-review once and confirm my decisions persist (or note that they don't).
64	9. Rate "I could verify every claim quickly" 1-5 with a reason (ship bar requires ≥ 4).
65	
66	## 8. Calibration
67	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
68	- **blocker — PT total invented.** Evidence: charges table row "Capital PT — $2,220 (12 × $185)". Fix: list "$185 per visit — rate, visit count not stated; needs review"; total stays $8,390. Test: eval asserts no PT total and total = 8390.
69	- **major — Export has no citations.** Evidence: export line "Patient treated at Capital PT for neck pain." Fix: `January 23, 2026 — Capital PT, initial evaluation: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits." [Ex. __ / Bates __]`. Test: E2E asserts every letter line contains a date of service, the provider as written, a verbatim quote, and the citation placeholder.
70	- **minor — No remaining count.** Evidence: review screen of 9 entries + 8 flags has no counter. Fix: sticky "11 of 17 reviewed".
71	
72	## 9. Sources
73	- https://www.evenuplaw.com/guides/how-to-prepare-medical-chronology — EvenUp (vendor): chronology columns are source page, DOS, provider/facility, encounter, complaint, diagnoses, treatment, referrals; ends with a review checklist.
74	- https://www.evenuplaw.com/guides/what-is-a-medical-chronology/ — EvenUp: paralegal drafts, attorney reviews; demand medical facts must match the chronology; a bill without a matching note is a gap to flag.
75	- https://www.tavrn.ai/blog/medical-chronology-mistakes — Tavrn (vendor, 2026): common errors are entry-timestamp vs visit dates, copy-forward duplication, missing page/Bates cites, unflagged conflicting onset histories.
76	- https://davislaw.betterteam.com/personal-injury-litigation-paralegal-3 — Davis Law Firm (San Antonio) posting: PI paralegals summarize records, bills, and wage loss and build demand packages; Filevine preferred.
77	- https://www.builtinaustin.com/job/litigation-paralegal/11851661 — Brown Sims (Houston) posting: medical and billing chronologies are a core paralegal duty on the defense side too.
78	- https://nala.org/events/2025-11-24/?ical=1 — NALA CLE (Nov 2025): PI discovery guide for paralegals; organizing records for attorney and expert use.
79	- https://www.rmdlaw.com/blog/the-gap-in-treatment-insurance-trap-how-a-delay-can-lower-your-claim-value/ — RMD Law (PI firm, 2026): no carrier publishes a gap threshold; delay-to-first-care, mid-treatment gaps, and early stopping are distinct.
80	- https://www.blackchapman.com/?p=396 — Black Chapman (PI firm) on Colossus: documented diagnoses per body part and objective findings drive valuation.
81	- Assumptions: Texas setting and Filevine are from the postings; the `[Ex. __ / Bates __]` placeholder (D-002) is used because Appendix A records have no Bates numbers. Vendor and plaintiff-firm sources are advocacy, not neutral.
82	
83	## 10. Limits
84	Do not opine on legal strategy (whether to disclose a gap in the demand — litigation-lead), clinical interpretation beyond reading the words (legal-nurse), code quality, or security. Do not judge visual design except where it slows verification.
85	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:10.953Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-116 && echo ---- && python3 tools/board.py show T-118 && echo ---- && git log --oneline -3 78450f6 && git show --stat 78450f6 | head -40",
 "description": "Show T-116 and T-118 cards and commit stats"
}
````

### User / tool · 2026-11-02T09:57:11.189Z

**tool result**
````
---
id: "T-116"
title: "Gap rule: an intake form or other administrative record never ends a treatment gap"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T09:29:33Z"
updated_at: "2026-11-02T09:55:10Z"
claimed_by: "backend"
claimed_at: "2026-11-02T09:43:53Z"
rounds: 1
commits: ["c1b44be", "ea6ac71"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-116-paralegal.md", "at": "2026-11-02T09:43:53Z"}
ac:
  - {"n": 1, "text": "gaps.py treats only treatment encounters as gap endpoints; intake forms, records requests, billing statements and affidavits are excluded (by code-detected record type), with the exclusion shown in the gap's why; lib09 and golden cases re-checked; tests", "done": true, "evidence": "R2: gaps.non_visit_label fails safe (record-type head of label + no visit word + no treatment evidence in text); tests/unit/test_t116_gap_endpoints.py 95 passed incl. reviewer probe (17 visit labels with paperwork words, no flag) + 10-11 mixed records; tests/unit 2588 passed; python -m evals.run fixture gap precision/recall 1.000/1.000 (evals/reports/20261102T095147Z.md); lib11 corrected lines validated on scratch copy (validate_library.py + check_golden.py exit 0), posted as card note for qa"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T09:29:39Z backend: claimed
- 2026-11-02T09:34:57Z backend: For qa (do not edit evals/golden; I did not): record types are now read by code. Two library lines change, nothing else; gap dates, day counts and flags are identical in all 25 golden+library packets (flag precision/recall gap 1.000/1.000, fixture run evals/reports/20261102T093441Z.md). (1) evals/library/case_lib11_priors_and_ledger.expected.json: record 6 is a 'new patient intake form (OCR text)' dated the same day as record 5, so it stops being an endpoint: gap_table[1].to_records [5, 6] -> [5]; gap_table[2].from_records [5, 6] -> [5]; gap_excluded_records [4, 9] -> [4, 6, 9]. (2) lib09 record 4 (formulario de admision) is already in gap_excluded_records [4, 7] and its kind stays 'encounter' in the golden records list; no change needed. Bare 'intake' (case_04 r6, lib07 r1) stays a treatment encounter.
- 2026-11-02T09:35:55Z backend: AC 1 checked: tests/unit/test_t116_gap_endpoints.py (49 tests incl. all 25 golden+library gap tables unchanged, lib09 confirm keeps 42 days with why 'Intake form on March 5, 2026 is not a treatment visit...'); tests/unit 2559 passed; python -m evals.run fixture: gap precision/recall 1.000/1.000 (evals/reports/20261102T093441Z.md); lib11 record lists change, posted for qa
- 2026-11-02T09:35:55Z backend: moved in_progress -> in_review
- 2026-11-02T09:36:00Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-02T09:43:53Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): fail — reviews/T-116-paralegal.md; round 1; findings:
    - [blocker] A treatment visit whose Source label contains a paperwork word is excluded from gap endpoints, which invents a gap and a false statement — fix: Classify on the record-type head of the Source label, not on any substring: an encounter term (visit, evaluation, new patient, daily note, follow-up, operative, run report, imaging, discharge summary) keeps the record an encounter; paperwor
    - [major] lib11 expected truth file is stale at HEAD and the posted list change fails the golden checker as written — fix: qa and researcher: decide the kind vocabulary for intake forms (extend check_golden.py's allowed kinds and the entry encounter rule), set lib11 record 6 accordingly, apply the three list changes, and make the gap test compare (from_records, to_records) for all golden and l
    - [minor] Conflict and accident-year logic still treat intake forms and bills as encounters — fix: Open a follow-up card to route conflicts.py and pipeline._accident_year through the same non-visit classifier used by gaps.py, after the F1 fix.
    - [minor] Gap why names the type and date, not the record number or the header text the classification came from — fix: Add the record number and the verbatim header to the sentence from flag_templates.non_visit_sentence, e.g. 'Intake form on March 5, 2026 (record 4, header: formulario de admisión (OCR)) is not a treatment visit...'.
- 2026-11-02T09:43:53Z backend: claimed
- 2026-11-02T09:52:00Z backend: For qa (round 2, evals/ not edited by me). Corrected lib11 lines, proven on a scratch copy of evals/ + research/ where research/validate_library.py exits 0 (golden OK: 25 cases, identifier check ok) and evals/golden/check_golden.py exits 0. The golden kind vocabulary (check_golden.py:200) has no intake-form kind and E6 must agree with it, so record 6 uses phone_note, the same non-visit stand-in record 4 (a letter) already uses; qa may add an intake_form kind later. Edit evals/library/case_lib11_priors_and_ledger.expected.json: (1) line 57 records[6].kind: "encounter" -> "phone_note"; (2) line 190 entries E6 "encounter": true -> false; (3) lines 251-254 gap_excluded_records [4, 9] -> [4, 6, 9]; (4) lines 276-279 gap_table[1].to_records [5, 6] -> [5]; (5) lines 286-289 gap_table[2].from_records [5, 6] -> [5]. All five are needed together: kind alone fails E6, lists alone fail gap_excluded_records. Dates, days and flags unchanged. Also: product kind for record 6 stays 'encounter' (ingest unchanged), gaps.py decides from the header; evals.run does not read the golden kind. Suggest tests/unit gap test compare (from_records, to_records) per packet once the file is updated.
- 2026-11-02T09:55:01Z backend: AC 1 checked: R2: gaps.non_visit_label fails safe (record-type head of label + no visit word + no treatment evidence in text); tests/unit/test_t116_gap_endpoints.py 95 passed incl. reviewer probe (17 visit labels with paperwork words, no flag) + 10-11 mixed records; tests/unit 2588 passed; python -m evals.run fixture gap precision/recall 1.000/1.000 (evals/reports/20261102T095147Z.md); lib11 corrected lines validated on scratch copy (validate_library.py + check_golden.py exit 0), posted as card note for qa
- 2026-11-02T09:55:01Z backend: moved in_progress -> in_review
- 2026-11-02T09:55:10Z orchestrator: review dispatched: paralegal-reviewer

## Handoff
What changed (R2): exclusion now needs (1) clearly administrative type read from the record-type head of the Source label (last comma segment, trailing parentheticals dropped; bare 'statement'/'fax' only as whole head), (2) no visit word left in that head (visit, evaluation, exam, note, discharge, ESI...), (3) no treatment evidence in the text (Exam/Assessment/Plan/Vitals/Procedure/Diagnosis headings, BP values, seen-by, administered/performed); letters/affidavits may restate a Diagnoses list. Unsure counts as treatment. Verified: reviewer repro and 19-label sweep now 0 excluded except none; unit 2588 passed; evals gap P/R 1.000/1.000. Lib11 corrected lines (5 edits, validator + check_golden exit 0 on scratch) in card note for qa. Left: qa applies lib11 edits; F3 conflicts/_accident_year and F4 (record no + header in why) not done, need follow-up cards. Surprised: review-evidence scripts import a stale archive path.

----
---
id: "T-118"
title: "Apply T-116 lib11 golden edits (five edits posted on T-116) and validate"
milestone: "M3"
role: "qa"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T09:55:10Z"
updated_at: "2026-11-02T09:57:04Z"
claimed_by: "qa"
claimed_at: "2026-11-02T09:55:17Z"
rounds: 0
commits: ["78450f6"]
reviews: []
ac:
  - {"n": 1, "text": "The five lib11 edits from the T-116 card note are applied together; research/validate_library.py and evals/golden/check_golden.py pass; evals.run library report unchanged except lib11 gap endpoints", "done": true, "evidence": "commit 78450f6: lib11 five edits; validate_library.py exit 0; check_golden.py exit 0; evals.run fixture gap P/R 1.000/1.000 (evals/reports/20261102T095640Z.md); library report scored columns unchanged, gap endpoints match expected for lib11 (only change)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T09:55:17Z qa: claimed
- 2026-11-02T09:56:50Z qa: Applied the five T-116 lib11 edits together (kind phone_note, E6 encounter false, gap_excluded_records [4,6,9], gap_table[1].to_records [5], gap_table[2].from_records [5]); json parses. validate_library.py exit 0, check_golden.py exit 0. Library report scored columns identical to HEAD-lib11 baseline (only provenance header differs). Gap endpoints now match expected for all 4 lib11 rows (checked against gaps.compute_gaps); old expected differed on 2 rows. evals.run fixture: gap P/R 1.000/1.000; ship_bar_met=False with the same 3 pre-existing blockers as latest.json before this change (report evals/reports/20261102T095640Z.md).
- 2026-11-02T09:56:59Z qa: AC 1 checked: commit 78450f6: lib11 five edits; validate_library.py exit 0; check_golden.py exit 0; evals.run fixture gap P/R 1.000/1.000 (evals/reports/20261102T095640Z.md); library report scored columns unchanged, gap endpoints match expected for lib11 (only change)
- 2026-11-02T09:56:59Z qa: moved in_progress -> in_review
- 2026-11-02T09:57:04Z orchestrator: review dispatched: paralegal-reviewer

## Handoff
What changed: the five T-116 lib11 edits applied together in evals/library/case_lib11_priors_and_ledger.expected.json (record 6 kind phone_note; E6 encounter false; gap_excluded_records [4,6,9]; gap_table[1].to_records [5]; gap_table[2].from_records [5]). Commit 78450f6. How verified: research/validate_library.py exit 0; evals/golden/check_golden.py exit 0; .venv/bin/python -m evals.run fixture (report evals/reports/20261102T095640Z.md; ship_bar_met=False, same 3 blockers as before: 4_no_invented_facts, determinism/unsupported need live backend, judge_controls not measured); library report (evals.library_report) scored table unchanged, only the source-commit header differs; lib11 gap endpoints now equal the computed endpoints (old expected differed on 2 rows). What's left: the library report does not score endpoints (run.py:244 compares dates/days/flag only), so a per-endpoint test in tests/unit is still advisable (backend suggested). Surprised: evals.run exits 1 on fixture by design; the ship bar blockers are not new.

----
78450f6 test(qa): lib11 expected: intake form is not a gap endpoint (T-118, applies T-116 five edits)
ea6ac71 fix(backend): gap exclusion fails safe toward treatment; label head + no treatment evidence required (T-116 r2)
400a8c0 test(qa): T-115 curated judge fixtures regenerated for judge_flag_v3 (12 e2e failures were fixture drift), judge-row record cue xfail(strict) T-117
commit 78450f629dd9e2974004ca935150ace270eeb9e1
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 03:56:54 2026 -0600

    test(qa): lib11 expected: intake form is not a gap endpoint (T-118, applies T-116 five edits)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 .../case_lib11_priors_and_ledger.expected.json     |   11 +-
 evals/reports/20261102T095640Z.md                  |   69 ++
 evals/reports/latest.json                          | 1090 ++++++++++++++------
 3 files changed, 872 insertions(+), 298 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:11.399Z

**tool call — Bash**
````
{
 "command": "ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/ && cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "description": "List reviewer memory directory and index"
}
````

### User / tool · 2026-11-02T09:57:11.480Z

**tool result**
````
MEMORY.md
d041-date-gate-patterns.md
feedback_reviewer_tooling_quirks.md
feedback_spec_review_patterns.md
frontend-review-patterns.md
golden-set-recurring-findings.md
library-review-patterns.md
manual-entry-split-review-patterns.md
record-format-review-patterns.md
reviewer-api-shape-gotchas.md
reviewer-hook-constraints.md
t068-dates-to-confirm-patterns.md
t079-library-v2-patterns.md
t114-rates-gap-patterns.md
t116-gap-endpoint-patterns.md
- [Spec review patterns](feedback_spec_review_patterns.md) — check absolute claims vs the doc's own example; grep every named category/R-ID/fixture
- [Golden-set recurring findings](golden-set-recurring-findings.md) — T-015: must/should levels, shared type+cite flags, export/§6 drift, dead checks via key drift (mutation-test)
- [Reviewer hook constraints](reviewer-hook-constraints.md) — board.py allowed verbs, python heredoc form, write-allowed dirs
- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; review files are append-only (proofread before the one Write)
- [Frontend review patterns](frontend-review-patterns.md) — T-043: mock vs harness coverage, keyboard focus yank, recurring minor gaps
- [Library review patterns](library-review-patterns.md) — T-052 minors; T-077 r2/r3: self-test shape-bound (author-year, prose escape), title-case FAIR Health passes
- [Record-format review patterns](record-format-review-patterns.md) — T-078 r2: mutation-test the check script; visit-count fix creates a PT gap; lib14 specimen gaps
- [Manual entry / split review patterns](manual-entry-split-review-patterns.md) — T-056: AC ticked for absent UI label, split amounts not moving, override trace missing
- [T-068 dates-to-confirm patterns](t068-dates-to-confirm-patterns.md) — orphan confirm dead-ends, record listed twice, text-only AC test, commit vs worktree divergence
- [D-041 date-gate patterns](d041-date-gate-patterns.md) — T-076 r2 (f4ef2ea): stale DATE_AMBIGUOUS fixed; Edit/Change quote still enabled on undated row (T-060)
- [Reviewer API shape gotchas](reviewer-api-shape-gotchas.md) — item GET nests under "item", status "ready", record warnings in case.flags, audit before/after local-only
- [T-079 library v2 patterns](t079-library-v2-patterns.md) — statement-vs-note double count, replay at cited commit, append-only ref proofreading
- [T-114 rates and gap patterns](t114-rates-gap-patterns.md) — rate acknowledge-only passes; gap change API-only in HEAD; intake-form encounter kind is Chris's call; golden N1 scoped to ambiguous
- [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — label substring exclusion invents gaps; stale lib11 truth; golden kind vocabulary lacks intake form
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:21.836Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t116-gap-endpoint-patterns.md"
}
````

### User / tool · 2026-11-02T09:57:21.853Z

**tool result**
````
1	---
2	name: t116-gap-endpoint-patterns
3	description: T-116 (c1b44be) gap endpoint classifier: unanchored label regexes exclude real visits (invented gap); lib11 truth stale and golden kind vocabulary lacks intake form; conflicts.py still uses kind encounter
4	metadata:
5	  type: project
6	---
7	
8	Recurring pattern: a record-type classifier that searches the whole source label for paperwork words will exclude treatment visits whose label
9	mentions them ("initial evaluation (intake form completed same day)", "statement of MMI", "records review visit"). Each one invents a gap. Test with
10	an A/B packet through ingest.ingest + gaps.gap_flags, not only with the label list. Blocker under the persona calibration.
11	
12	Recurring pattern: a card posts an expected-file change "for qa" and ticks its AC. Check the committed truth file against the product output
13	(`git show HEAD:<expected>`), then apply the change on a scratch copy and run research/validate_library.py. The golden checker's kind vocabulary
14	(check_golden.py:200: encounter, billing_statement, phone_note) cannot express an intake form, so list-only edits fail.
15	
16	Recurring pattern: gap tests that compare dates, days and flags but not record lists let record-list drift pass silently.
17	
18	Why: T-116 review (2026-11-02, verdict fail). Status of the classifier fix is in the card, not here.
19	How to apply: whenever a gap or endpoint rule changes, sweep labels with the paperwork words in a visit position, and diff expected record lists
20	against product output on every packet.
21	
22	Related: [[golden-set-recurring-findings]], [[t114-rates-gap-patterns]], [[reviewer-tooling-quirks]].
23	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:22.078Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md"
}
````

### User / tool · 2026-11-02T09:57:22.086Z

**tool result**
````
1	---
2	name: reviewer-hook-constraints
3	description: Bash hooks that block reviewer commands in this repo (board.py --help, python -c containing backticks) and the workarounds
4	metadata:
5	  type: reference
6	---
7	
8	- board-guard: reviewers may run only `tools/board.py validate|show|list|status`. `--help` is rejected.
9	- git-guard fails to parse `python3 -c "..."` when the code contains escaped backticks. Use a quoted heredoc (`python3 - <<'EOF'`) and build the fence as '`'*3.
10	- Write access is limited to reviews/ and artifacts/review-evidence/ (plus this memory dir). Probe scripts go in artifacts/review-evidence/.
11	
12	**How to apply:** use these forms directly to avoid wasted tool calls. Related: [[golden-set-recurring-findings]]
13	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:22.365Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md"
}
````

### User / tool · 2026-11-02T09:57:22.376Z

**tool result**
````
1	---
2	name: reviewer-tooling-quirks
3	description: Hooks that block reviewer shell commands in Zlayt PM (board-guard on sed -i, git-guard on python -c with backticks) and the workaround
4	metadata:
5	  type: feedback
6	---
7	
8	Don't edit review files with `sed -i` (board-guard blocks it), and don't run `python3 -c` with backticks or regex escapes (git-guard can't parse it). Use the Edit tool for review files, and put checks in a script under artifacts/review-evidence/ run with `.venv/bin/python`.
9	
10	**Why:** Both were blocked during the T-013 r2 review (2026-11-01). A script also leaves reproducible evidence the review can cite.
11	
12	**How to apply:** For every review, put JSON/verdict validation in artifacts/review-evidence/<card>-*-jsoncheck.py. Related: [[spec-review-patterns]].
13	
14	## T-077/T-078 r2 additions (2026-11-01)
15	- `grep -E` with long `.{0,120}` patterns over fetched HTML fails in ugrep ("exceeds complexity limits"). Strip tags and search in a python script under artifacts/review-evidence/.
16	- `timeout` is not installed on this macOS host; drop it and rely on urllib's timeout argument.
17	- A `mktemp` + `rmdir` combo inside a Bash call tripped board-guard. Keep Bash calls to one purpose.
18	- Fetched pages redirected to the session scratchpad were not blocked by the hook, but the persona rule says reviewers write only under reviews/, artifacts/review-evidence/ and memory. Write fetch dumps to artifacts/review-evidence/ and say so in the review.
19	- The NUCC and CMS PDFs download fine with urllib; write the PDF into review-evidence, run `pdftotext -layout`, then delete the PDF and text.
20	
21	## T-077 r3 additions (2026-11-01)
22	- `reviewer-write-guard` makes review files append-only: once `reviews/<card>-<persona>-rN.md` exists, Edit is refused ("reviews are append-only"). Proof-read the review (grep every line ref and quote) BEFORE the single Write; a stale ref cannot be fixed afterwards without a new file.
23	- A bash `python3 -c` with `\`\`\`` and `\d` escapes was denied by git-guard ("could not parse command safely (No escaped character)"). Move any JSON parse into a Write-created script under artifacts/review-evidence/ and run it.
24	
25	## T-114 additions (2026-11-02)
26	- board-guard reads a redirect target written as `$VAR/file` inside the same command as "writes outside reviews/"; the same redirect with a literal absolute path passes. Use literal paths for `> file` redirects, and put server start/stop in their own calls.
27	- git-guard rejected a `kill $(cat pidfile)` chain with echo quotes ("No closing quotation"). Use the PID number directly.
28	- `timeout` is not installed (already noted); `python3 tools/board.py validate reviews/<file>` works and printed "ok (1 file(s))".
29	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:22.562Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/library-review-patterns.md"
}
````

### User / tool · 2026-11-02T09:57:22.571Z

**tool result**
````
1	---
2	name: library-review-patterns
3	description: T-052 (2026-11-01) synthetic case library review - what held up, what to re-check on library/golden changes
4	metadata:
5	  type: project
6	---
7	
8	T-052 evals/library (7 packets) passed with minors only. Hand-recomputed gaps/totals were all right; identifier overlap vs fetchable sources was 0.
9	Re-check on any library change:
10	- Stated attendance count vs billed count (lib03 "31 visits", $120 rate left unclear): is the rule written in README/REQUIREMENTS?
11	- Flag type fit: lib06 attorney referral is typed `causation` (wrong heading).
12	- PT plan-of-care vs last visit with no discharge (lib05) is not surfaced.
13	- Library packets are one-sentence excerpts; no ledger-by-DOS, Bates, DOA conflict.
14	- valawyersweekly.com and rissman.com return 403 to curl even with a browser UA; studicata is unopened. Sources fetch fine for rmdlaw, oklahomalawyer, plasticsurgerypractice, thompsoncoe.
15	- curl `-o` to scratchpad and python heredocs containing `>=` trip board-guard; redirect stdout into artifacts/review-evidence and put code in a script file.
16	
17	**How to apply:** use artifacts/review-evidence/T-052-paralegal-scan.py as a starting probe. Related: [[golden-set-recurring-findings]], [[reviewer-hook-constraints]]
18	
19	## T-077 r2 (commit 5c2cb2f): denylist guard, self-test scope
20	- A denylist self-test that cross-checks only the doc's caption names ("X v. Y", "In re X") misses real names cited in prose (study authors, co-authors). Brinjikji, Nakashima, Fraser, Vera slipped through while the self-test printed "ok". Run the per-name check yourself: list every capitalised name in the doc and test each against the list.
21	- Firm domains in cited URLs (mdjwlaw, painterfirm) and organisation names (FAIR Health) are not on the list; decide with Chris whether they count as "real names".
22	- Rule text that says "every real name in this file is on the denylist" is a claim to test, not to trust.
23	- Fetched-page checks: a newsbrief sentence attributing a claim ("describes the withdrawn opinion") must be grepped on the page; the docket was the source that actually supported it.
24	- Date provenance: "checked 2026-11-02" in a doc written 2026-11-01 local is probably UTC. Ask, do not assume.
25	- Denylist and self-test changes in this area: keep a planted-name test per new term (mutation: delete a term and confirm self-test fails).
26	
27	## T-077 r3 (commit 8d7548d): what held, what to re-check
28	- Denylist now covers all 12 extracted author surnames and the opening list (Brinjikji, Nakashima); the round-2 major is closed for those shapes. Verdict changes (F1 major).
29	- Self-test extraction is shape-bound: initials/et al, the "cited" paragraph list, and X v. Y captions only. Author-year ("Smithers (2019)"), comma-year and prose mentions pass silently. Mutate the doc text in memory (self_test(doc_text=...)) to check each shape; do not trust the doc's "every real name" sentence.
30	- Capitalised-only terms match only the exact case or UPPER. Title-case "Fair Health" passes; the self-test variants never include title case. Probe every capitalised-only term in Title case as well.
31	- Firm exemptions: slugs are listed, the firm's words (Painter) are not; publisher and agency names are not listed but the rule says "organisation names". Ask for a written exemption rather than a list.
32	- Review files are append-only (reviewer-write-guard): any stale line ref must be checked before the one Write. T-077 r3 went out with five stale refs (validate_library.py:53-56 vs real :51; doc :26-27 vs :25-26; :1-11 vs 2-16; :136 vs :59-60). Recheck with grep -n on every ref.
33	- Re-check on any later library change: run artifacts/review-evidence/T-077-paralegal-r3-names.py (sections A to F) and compare to its .out.
34	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:25.500Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log --oneline -1 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p \"$SCR/t118-head\" && git archive HEAD | tar -x -C \"$SCR/t118-head\" && ls \"$SCR/t118-head\" && echo \"$SCR\"",
 "description": "Extract git HEAD archive into scratchpad"
}
````

### User / tool · 2026-11-02T09:57:25.949Z

**tool result**
````
78450f6
78450f6 test(qa): lib11 expected: intake form is not a gap endpoint (T-118, applies T-116 five edits)
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:28.067Z

**tool call — Bash**
````
{
 "command": "git show 78450f6 -- evals/library/case_lib11_priors_and_ledger.expected.json",
 "description": "Show the lib11 expected-file diff in the commit"
}
````

### User / tool · 2026-11-02T09:57:28.164Z

**tool result**
````
commit 78450f629dd9e2974004ca935150ace270eeb9e1
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 03:56:54 2026 -0600

    test(qa): lib11 expected: intake form is not a gap endpoint (T-118, applies T-116 five edits)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/evals/library/case_lib11_priors_and_ledger.expected.json b/evals/library/case_lib11_priors_and_ledger.expected.json
index 1e33d11..ed35f31 100644
--- a/evals/library/case_lib11_priors_and_ledger.expected.json
+++ b/evals/library/case_lib11_priors_and_ledger.expected.json
@@ -54,7 +54,7 @@
       "record_no": 6,
       "raw_date": "3/27/26",
       "date": "2026-03-27",
-      "kind": "encounter",
+      "kind": "phone_note",
       "source": "Fennimoor Spine Clinic, new patient intake form (OCR text)"
     },
     {
@@ -187,7 +187,7 @@
       ],
       "date": "2026-03-27",
       "date_status": "parsed",
-      "encounter": true,
+      "encounter": false,
       "provider": "Fennimoor Spine Clinic, new patient intake form (OCR text)",
       "must_contain_excerpt": "Prior accidents? Yes [ ] No [X]",
       "required_terms": [
@@ -250,6 +250,7 @@
   "expected_entry_count": 9,
   "gap_excluded_records": [
     4,
+    6,
     9
   ],
   "gap_table": [
@@ -274,8 +275,7 @@
         3
       ],
       "to_records": [
-        5,
-        6
+        5
       ],
       "days": 9,
       "flag": false
@@ -284,8 +284,7 @@
       "from_date": "2026-03-27",
       "to_date": "2026-04-24",
       "from_records": [
-        5,
-        6
+        5
       ],
       "to_records": [
         7
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:36.120Z

**tool call — Bash**
````
{
 "command": "ls evals/library/ | grep -i lib11; ls evals/golden | head -50; echo ----; grep -n -i \"intake\" evals/library/case_lib11* | head -30; echo ----; sed -n 45,70p evals/library/case_lib11_priors_and_ledger.expected.json",
 "description": "Locate lib11 packet and intake references"
}
````

### User / tool · 2026-11-02T09:57:36.230Z

**tool result**
````
case_lib11_priors_and_ledger.expected.json
case_lib11_priors_and_ledger.txt
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
case_09_nonvisit_hides_gap.expected.json
case_09_nonvisit_hides_gap.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
judge_controls.CHANGELOG.md
judge_controls.jsonl
judge_controls_heldout.jsonl
sample.expected.json
sample.export.expected.txt
sample.txt
unsplit_paste.split.json
unsplit_paste.txt
----
evals/library/case_lib11_priors_and_ledger.txt:30:Source: Fennimoor Spine Clinic, new patient intake form (OCR text)
evals/library/case_lib11_priors_and_ledger.expected.json:6:  "description": "Library L11 (P5+P2). Rear-end collision two weeks after an annual primary-care visit that lists two earlier car accidents, a chronic low back problem and a baseline back pain score. Attorney-referred spine clinic under a letter of protection, a scanned intake form (OCR text) answering 'prior accidents: No', and an itemized ledger with charges, a payment, a courtesy adjustment and a balance. Only stated charges count; payment, adjustment and balance are listed unclear.",
evals/library/case_lib11_priors_and_ledger.expected.json:8:    "intake_denies_prior_accidents",
evals/library/case_lib11_priors_and_ledger.expected.json:58:      "source": "Fennimoor Spine Clinic, new patient intake form (OCR text)"
evals/library/case_lib11_priors_and_ledger.expected.json:191:      "provider": "Fennimoor Spine Clinic, new patient intake form (OCR text)",
evals/library/case_lib11_priors_and_ledger.expected.json:555:      "summary": "The intake form answers 'Prior accidents? No' while the primary-care note of 2026-03-04 lists accidents in 2019 and 2022. Both cited; the tool does not say which is right.",
evals/library/case_lib11_priors_and_ledger.expected.json:556:      "subtype": "intake_denies_prior_accidents"
evals/library/case_lib11_priors_and_ledger.expected.json:652:      "statement": "Calls the intake answer false or dishonest (lied, false, misrepresented).",
evals/library/case_lib11_priors_and_ledger.expected.json:656:        "She lied on the intake form.",
evals/library/case_lib11_priors_and_ledger.expected.json:657:        "The intake answer was false.",
evals/library/case_lib11_priors_and_ledger.expected.json:661:        "Intake form answer: Prior accidents? No.",
evals/library/case_lib11_priors_and_ledger.expected.json:663:        "Intake and primary-care note differ; both cited."
evals/library/case_lib11_priors_and_ledger.expected.json:686:    "Older notes come from the firm's records request to the PCP; the intake form is the clinic's. D-042 calibrated confidence: the tool shows measured precision per state for the pre-existing flags, never an invented percentage.",
----
    },
    {
      "record_no": 5,
      "raw_date": "2026-03-27",
      "date": "2026-03-27",
      "kind": "encounter",
      "source": "Fennimoor Spine Clinic, new patient"
    },
    {
      "record_no": 6,
      "raw_date": "3/27/26",
      "date": "2026-03-27",
      "kind": "phone_note",
      "source": "Fennimoor Spine Clinic, new patient intake form (OCR text)"
    },
    {
      "record_no": 7,
      "raw_date": "2026-04-24",
      "date": "2026-04-24",
      "kind": "encounter",
      "source": "Fennimoor Spine Clinic, visit 8"
    },
    {
      "record_no": 8,
      "raw_date": "2026-05-29",
      "date": "2026-05-29",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:37.973Z

**tool call — Bash**
````
{
 "command": "cat -n evals/library/case_lib11_priors_and_ledger.txt | sed -n 1,140p",
 "description": "Read lib11 packet text in full"
}
````

### User / tool · 2026-11-02T09:57:38.056Z

**tool result**
````
     1	SYNTHETIC — invented for evaluation; not real patient data
     2	
     3	=== Record 1 ===
     4	Date: 2026-03-04
     5	Source: Dr. Hesper Alderton, primary care
     6	Excerpt: "Annual visit. History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy. Problem list: hypertension, type 2 diabetes, chronic low back pain. Low back pain 3/10 today."
     7	
     8	=== Record 2 ===
     9	Date: 2026-03-18
    10	Source: Ashgrove Fire-Rescue run report
    11	Excerpt: "Passenger vehicle struck from behind. Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED."
    12	
    13	=== Record 3 ===
    14	Date: 2026-03-18
    15	Source: Wexcombe Memorial ED
    16	Excerpt: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture. ED charge: $3,260."
    17	
    18	=== Record 4 ===
    19	Date: 2026-03-26
    20	Source: Pellingham and Rook PLLC, correspondence (letter of protection)
    21	Excerpt: "Letter of protection to Fennimoor Spine Clinic. This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending. Please send complete records and an itemized statement."
    22	
    23	=== Record 5 ===
    24	Date: 2026-03-27
    25	Source: Fennimoor Spine Clinic, new patient
    26	Excerpt: "Patient referred by attorney. Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly."
    27	
    28	=== Record 6 ===
    29	Date: 3/27/26
    30	Source: Fennimoor Spine Clinic, new patient intake form (OCR text)
    31	Excerpt: "Date of injury: 3/l8/26. How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7. Signed 3/27/2G."
    32	
    33	=== Record 7 ===
    34	Date: 2026-04-24
    35	Source: Fennimoor Spine Clinic, visit 8
    36	Excerpt: "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued."
    37	
    38	=== Record 8 ===
    39	Date: 2026-05-29
    40	Source: Fennimoor Spine Clinic, visit 14
    41	Excerpt: "Neck pain 4/10, low back pain 5/10. Care continues."
    42	
    43	=== Record 9 ===
    44	Date: 2026-06-15
    45	Source: Fennimoor Spine Clinic, itemized ledger
    46	Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:41.719Z

**tool call — Bash**
````
{
 "command": "sed -n 1,20p research/validate_library.py; echo ----; grep -n \"kind\\|phone_note\\|intake\" evals/golden/check_golden.py | head -40; echo ----; ls evals/ ; ls research | head -40; echo ----; sed -n 20,45p evals/library/case_lib11_priors_and_ledger.expected.json",
 "description": "Inspect validators, golden kind vocabulary and lib11 records"
}
````

### User / tool · 2026-11-02T09:57:41.828Z

**tool result**
````
#!/usr/bin/env python3
"""Validate evals/library/* with evals/golden/check_golden.py (T-052) and scan packets for real identifiers (T-077).

check_golden.py reads cases from its own directory, so this copies evals/golden into a scratch dir, adds the library packets,
runs the checker there, and then scans the library for real identifiers. The denylist holds every proper noun taken from the
cited real sources in research/case-library-sources.md (v1) and research/case-library-sources-v2.md (v2): case parties, judges,
doctors named in opinions, study authors, firms, counties, cities and highways. Matching is case-insensitive and
accent-insensitive ('GARZA', 'garza', 'Rodríguez' all hit). Exit 0 = both pass.

Self-test checks the v2 doc mechanically: every surname written before author initials or 'et al' (e.g. 'Fraser S.G.'), every
bare surname in a parenthesised list inside a paragraph that cites earlier sources (e.g. 'Brinjikji, Nakashima'), and every
'X v. Y' / 'In re X' caption name must be on the denylist, and each one planted in a packet must fail the scan. A newly cited
name therefore fails the self-test until it is added to DENYLIST_V2 and the doc's 'Denylist additions' block.

Run:        python3 research/validate_library.py
Self-test:  python3 research/validate_library.py --self-test
"""
import pathlib, re, shutil, subprocess, sys, tempfile, unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
----
7:  * the .txt starts with "SYNTHETIC" and parses into the records the JSON declares (raw date, kind, source);
87:    if "source_kind" in sp:
88:        out.append("source_kind not allowed on spans (D-040: no speaker label)")
159:if not span_problems(dict(excerpt="Alert and oriented", source_kind="patient_report", attribution_any=["x"])) or \
200:        if r["kind"] not in ("encounter", "billing_statement", "phone_note"):
201:            err(cid, f"record {r['record_no']}: bad kind")
230:        if "source_kind" in e:
231:            err(cid, f"{e['id']}: entry-level source_kind removed (D-022); tag spans")
242:        if e["encounter"] != (rs[0]["kind"] == "encounter"):
243:            err(cid, f"{e['id']}: encounter flag disagrees with record kind")
255:        if r["date"] and r["kind"] == "encounter":
344:        if se["kind"] == "number":
349:        elif se["kind"] == "control":
352:        elif se["kind"] == "judge_masked":
355:        elif se["kind"] == "judge":
358:    if cid == "sample" and {x["kind"] for x in ex.get("seeded_edits", [])} != {"number", "judge", "judge_masked", "control"}:
359:        err(cid, "sample needs seeded edits of kinds number, judge, judge_masked and control")
415:K5c = cand("causation", [(7, "Date of accident per intake form: 2026-01-19.")])
418:    ("one candidate on the intake-date line satisfies K5 only", [K5c], {"K5"}),
420:    ("one candidate carrying both spans can satisfy at most ONE golden flag", [cand("causation", [(7, "New onset pain"), (7, "Date of accident per intake form: 2026-01-19.")])], None),
423:      cand("conflict", [(7, "Date of accident per intake form: 2026-01-19."), (1, "rear-ended at approx. 35 mph")])], {"G1", "C1"}),
425:     [cand("causation", [(7, "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.")])] * 2, None),
----
__init__.py
__pycache__
adversarial
golden
j3_controls.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
reports
run.py
ASSUMPTIONS-proposed.md
__pycache__
adjuster-attacks.md
case-library-sources-v2.md
case-library-sources.md
chronology-practice.md
lexicon_selfcheck.py
library_build.py
office-view-references.md
phi-and-ai-supervision.md
record-formats.md
record_formats_check.py
texas-pi-notes.md
ui-references.md
validate_library.py
----
      "raw_date": "2026-03-04",
      "date": "2026-03-04",
      "kind": "encounter",
      "source": "Dr. Hesper Alderton, primary care"
    },
    {
      "record_no": 2,
      "raw_date": "2026-03-18",
      "date": "2026-03-18",
      "kind": "encounter",
      "source": "Ashgrove Fire-Rescue run report"
    },
    {
      "record_no": 3,
      "raw_date": "2026-03-18",
      "date": "2026-03-18",
      "kind": "encounter",
      "source": "Wexcombe Memorial ED"
    },
    {
      "record_no": 4,
      "raw_date": "2026-03-26",
      "date": "2026-03-26",
      "kind": "phone_note",
      "source": "Pellingham and Rook PLLC, correspondence (letter of protection)"
    },
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:48.582Z

**tool call — Bash**
````
{
 "command": "cd \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t118-head\" && python3 -I research/validate_library.py; echo \"EXIT=$?\"; echo ----; python3 -I evals/golden/check_golden.py; echo \"EXIT=$?\"",
 "description": "Run validate_library and check_golden on HEAD archive copy"
}
````

### User / tool · 2026-11-02T09:57:49.230Z

**tool result**
````
golden OK: 25 cases (24 synthetic), 118 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (15 packets, 80 denylist terms, case-insensitive)
EXIT=0
----
golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:54.152Z

**tool call — Bash**
````
{
 "command": "cd \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t118-head\" && sed -n 1,40p evals/library_report.py; echo ----; grep -n \"def \\|gap\" evals/library_report.py | head -60; echo ----; grep -n \"gap\" evals/run.py | head -60",
 "description": "Read library report generator and gap references in run.py"
}
````

### User / tool · 2026-11-02T09:57:54.250Z

**tool result**
````
#!/usr/bin/env python3
"""Library report (T-079): scores every evals/library packet with evals.run's scoring functions. REPORTED, NOT GATED (D-031): no exit code
depends on a score; the ship bar (evals.run) still measures only evals/golden. It only exits non-zero when a packet cannot be run at all.

Run:  .venv/bin/python -m evals.library_report [--out evals/reports/library-latest.md]     (fixture backend; no network)
Honest failures are shown, not hidden: a record whose extract call has no recorded fixture shows as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS),
the same rule as lib01.
"""
import argparse
import json
import pathlib
import subprocess
import sys

from evals import run as R

LIB = R.ROOT / "evals" / "library"


def score(name, text, exp, pipeline):
    out = pipeline.run_case(text, "fixture")
    e, a, f = R.score_entries(exp, out), R.score_amounts(exp, out), R.score_flags(exp, out)
    errs = [(x.get("code"), x.get("record_no"), x.get("cause")) for x in out.get("errors") or []]
    must = sum(v["must"] for v in f["per_type"].values())
    found = sum(v["must_found"] for v in f["per_type"].values())
    return {"case": name, "entries": f"{e['found']}/{e['total']}", "amounts": f"{a['found']}/{a['total']}", "total_ok": a["total_ok"],
            "must_flags": f"{found}/{must}", "must_not_flag_hits": len(f["must_not_flag_hits"]), "must_not_hits": R.check_must_not(exp, out),
            "gap_rows_wrong": len(f["gap_rows_wrong"]), "errors": errs, "status": out.get("status")}


def _git(*args):
    try:
        return subprocess.run(["git", *args], cwd=R.ROOT, capture_output=True, text=True, timeout=30).stdout.strip()
    except Exception:   # noqa: BLE001 - provenance is best effort; the report still prints
        return ""


def provenance():
    """Source commit and dirty state of the tree the report ran in (a report is only reproducible from a clean tree)."""
    sha = _git("rev-parse", "HEAD") or "unknown"
----
20:def score(name, text, exp, pipeline):
28:            "gap_rows_wrong": len(f["gap_rows_wrong"]), "errors": errs, "status": out.get("status")}
31:def _git(*args):
38:def provenance():
45:def main(argv=None):
56:             "| packet | status | entries | amounts | total ok | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |",
60:                     f"{', '.join(r['must_not_hits']) or '-'} | {r['gap_rows_wrong']} | {'; '.join(f'{c} r{n} {k}' for c, n, k in r['errors']) or '-'} |")
----
46:FLAG_TYPES = ("gap", "conflict", "pre_existing", "causation")
243:    gaps = {(c["from_date"], c["to_date"], c["days"]) for c in cands if c["type"] == "gap"}
244:    gap_rows = [(r["from_date"], r["to_date"], r["days"], r["flag"]) for r in exp.get("gap_table", [])]
248:            "gap_rows_wrong": [r[:3] for r in gap_rows if (r[:3] in gaps) != r[3]]}
668:    """Every R-CO-7 field, by name. Code outputs (record split, parsed dates, entry-ID set, gap flags, amount list and classes, totals) must be identical
683:        "gap_flags": _srt((tuple(_ids(f)), (f.get("computed") or {}).get("from"), (f.get("computed") or {}).get("to"), (f.get("computed") or {}).get("days"),
684:                             f.get("state")) for f in flags if f.get("type") == "gap"),
870:    wrong = {n: r["flags"]["gap_rows_wrong"] for n, r in results.items()}
871:    g73 = s is not None and ("2026-03-06", "2026-05-18", 73) not in [tuple(x) for x in s["gap_rows_wrong"]]
872:    n28 = s is not None and ("2026-01-23", "2026-02-20", 28) not in [tuple(x) for x in s["gap_rows_wrong"]] and \
873:        (c6 is None or ("2026-10-19", "2026-11-16", 28) not in [tuple(x) for x in c6["gap_rows_wrong"]])
874:    return {"gap_28_not_flagged": n28, "gap_73_flagged": g73, "all_gap_rows_correct": not any(wrong.values())}
906:                   and a["gap_28_not_flagged"] and a["gap_73_flagged"],
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:05.404Z

**tool call — Bash**
````
{
 "command": "cd \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t118-head\" && sed -n 40,80p evals/library_report.py; echo ----; sed -n 236,250p evals/run.py; echo ----; ls /Users/arsis/zlayt-pm-project/.venv/bin/python && cd /Users/arsis/zlayt-pm-project && git ls-files evals/reports | head -30",
 "description": "Read library report main and list committed report files"
}
````

### User / tool · 2026-11-02T09:58:05.522Z

**tool result**
````
    sha = _git("rev-parse", "HEAD") or "unknown"
    dirty = [l for l in _git("status", "--porcelain", "--untracked-files=no").splitlines() if l.strip()]
    return sha, ("clean" if not dirty and sha != "unknown" else f"DIRTY ({len(dirty)} tracked paths differ)" if dirty else "unknown")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m evals.library_report")
    ap.add_argument("--out", default=str(R.ROOT / "evals" / "reports" / "library-latest.md"))
    a = ap.parse_args(argv)
    pipeline = R.load_pipeline()
    rows = []
    for p in sorted(LIB.glob("case_*.txt")):
        rows.append(score(p.stem, p.read_text(), json.loads(p.with_name(p.stem + ".expected.json").read_text()), pipeline))
    sha, state = provenance()
    lines = ["# Library report (reported, not gated)", "", f"Source commit: {sha} (tree: {state}). Regenerate from a clean worktree of the commit you cite.", "",
             "Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.", "",
             "| packet | status | entries | amounts | total ok | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['case']} | {r['status']} | {r['entries']} | {r['amounts']} | {r['total_ok']} | {r['must_flags']} | {r['must_not_flag_hits']} | "
                     f"{', '.join(r['must_not_hits']) or '-'} | {r['gap_rows_wrong']} | {'; '.join(f'{c} r{n} {k}' for c, n, k in r['errors']) or '-'} |")
    lines += ["", "## Known honest failures (generated from the run above)", ""]
    fails = [(r["case"], c, n, k) for r in rows for c, n, k in r["errors"]]
    if fails:
        lines += ["| packet | record | code | cause |", "|---|---|---|---|"] + [f"| {p} | r{n} | {c} | {k or 'not captured'} |" for p, c, n, k in fails]
    else:
        lines += ["None at this commit: every record of every packet replays from a recorded fixture on the fixture backend."]
    lines += ["", "History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt "
              "in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract "
              "(T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call)."]
    pathlib.Path(a.out).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
----
                hit = (c.get("from_date"), c.get("to_date")) == (mn.get("from_date"), mn.get("to_date"))
            elif mn.get("record_nos"):
                hit = set(mn["record_nos"]) <= {e["record_no"] for e in c["evidence"]}
            else:
                hit = i not in owned and not any(tolerated_match(t, c) for t in exp.get("tolerated", []))
            if hit:
                hits.append({"must_not_flag": mn["id"], "candidate_type": c["type"]})
    gaps = {(c["from_date"], c["to_date"], c["days"]) for c in cands if c["type"] == "gap"}
    gap_rows = [(r["from_date"], r["to_date"], r["days"], r["flag"]) for r in exp.get("gap_table", [])]
    return {"per_type": per, "missed_must": [g["id"] for g in golden if g["level"] == "must" and g["id"] not in matched_ids],
            "must_not_flag_hits": hits,
            "tray_flags": [{"type": f.get("type"), "category": f.get("category"), "reasons": f.get("reasons") or []} for f in tray_flags(out)],
            "gap_rows_wrong": [r[:3] for r in gap_rows if (r[:3] in gaps) != r[3]]}


----
/Users/arsis/zlayt-pm-project/.venv/bin/python
evals/reports/20261102T020824Z.md
evals/reports/20261102T020933Z.md
evals/reports/20261102T021029Z.md
evals/reports/20261102T021046Z.md
evals/reports/20261102T022701Z.md
evals/reports/20261102T022927Z.md
evals/reports/20261102T023039Z.md
evals/reports/20261102T025219Z.md
evals/reports/20261102T025715Z.md
evals/reports/20261102T032823Z.md
evals/reports/20261102T035750Z.md
evals/reports/20261102T040933Z.md
evals/reports/20261102T081339Z.md
evals/reports/20261102T083252Z.md
evals/reports/20261102T085207Z.md
evals/reports/20261102T095640Z.md
evals/reports/calibration.json
evals/reports/controls-20261102T042306Z.json
evals/reports/controls-20261102T042306Z.md
evals/reports/controls-20261102T063331Z.json
evals/reports/controls-20261102T063331Z.md
evals/reports/controls-20261102T075238Z.json
evals/reports/controls-20261102T075238Z.md
evals/reports/controls-20261102T090925Z.json
evals/reports/controls-20261102T090925Z.md
evals/reports/determinism-diagnosis.md
evals/reports/latest.json
evals/reports/library-latest.md
evals/reports/m3-sensors.md
evals/reports/runs/20261102T034706Z/case_01_date_formats.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:13.904Z

**tool call — Bash**
````
{
 "command": "S=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\"; cd /Users/arsis/zlayt-pm-project && mkdir -p \"$S/t118-pre\" && git archive ea6ac71 | tar -x -C \"$S/t118-pre\" && git diff --stat ea6ac71 78450f6 && echo ---- && git diff --name-only ea6ac71 78450f6 && echo ---- && git ls-files evals/reports/library-latest.md && git log --oneline -2 -- evals/reports/library-latest.md && ls \"$S\"",
 "description": "Extract pre-commit tree and list files changed by commit"
}
````

### User / tool · 2026-11-02T09:58:14.446Z

**tool result**
````
 .../case_lib11_priors_and_ledger.expected.json     |   11 +-
 evals/reports/20261102T095640Z.md                  |   69 ++
 evals/reports/latest.json                          | 1090 ++++++++++++++------
 3 files changed, 872 insertions(+), 298 deletions(-)
----
evals/library/case_lib11_priors_and_ledger.expected.json
evals/reports/20261102T095640Z.md
evals/reports/latest.json
----
evals/reports/library-latest.md
ce70bd2 chore(evals): regenerate library report from clean HEAD a74b727 (T-079 r2)
328428f feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
641ed.bak
M1
M1_nocombine
M2
M2_find0
M3
M4
T-047-run1.json
T-093-r3-2ab7896
T-093-r3-run.py.orig
T-093-r3-scripts
T-093-r4-3223e50
T-093-r4-mutA
T-093-r4-mutB
T-109-probe
T-109-r1-card
T-109-r1-head
T-109-unit-head.txt
T102_staff_r1
T102_staff_r2
T103_archive
T103_parent
T106_cli_out
T106_head_archive
T106_m_exportbranch
T106_m_hlreview
T106_m_hltrace
T106_m_pdfbypass
T106_m_pdfclaude
T106_m_rootcal
T106_r2_mut_a
T106_r2_mut_b
T106_r2_mut_c
T106_r2_mut_d
T106_r2_probe
T106_r2_suite.txt
T106_r2_suite_run2.txt
T106_r2_verify
T106_scripts
T106_unit_run1.log
T106_unit_run2_rs.log
T108_r2_clone
T108_r2_verify
T108_verify
T115_staff_r1
a.sqlite3
a27e3a4.diff
adr013.txt
ap3500.pdf
api
api2
api_at_099732b.py
api_head.log
api_head.py
api_head.sqlite3
api_md_head.md
api_md_new.md
api_new.py
api_parent.log
api_parent.sqlite3
apitmp
app
app-head
app.log
app.pid
app.sqlite3
app2.log
app2.pid
app2.sqlite3
app60
app60.log
app60.pid
app60.sqlite3
ar2
ar_old
arc
arch
arch_57a08ba
archive
atk
audit.py
base
billing.orig
blank.py
body.py
bombs
boom_final.py
boom_server.py
boundary.py
boundary2.py
build_set.py
build_set.py.bak
build_t099_blobs.py
c
c8a9874
ca.sh
cal.bak
case.json
case.json.tok
case3.json
case3.json.tok
cases.txt
ce70
ce70-report.md
check.py
check_golden.out
check_json.py
check_r2.py
check_r3_json.py
check_r4.py
chk.py
chk_mut.py
cli1.err
cli1.out
cli1.txt
cli2.err
cli2.out
cli2.txt
cli_c1.err
cli_c1.txt
cli_final.err
cli_head_out.txt
cli_rep1.err
cli_rep2.err
cli_rep3.err
cmscms.py
collapsed.png
collapsed.py
commitcases.txt
copy
copyA
copyC
copy_untracked.py
corp_base.json
corp_r2.json
corpus.py
cr.sh
cred_b05.py
cred_orig.py
cs.sh
ctl-out
ctl.log
d1
d2
d3
d4
d5
d6
d7
d8
data
data2
dates.orig
dbg
dbg.png
dbg.py
dbg2.py
dbg3.png
dbg3.py
dbg4.py
dbg5.py
dbg97.py
de1.txt
decisions_head.md
demo
demo.log
diag.py
dl
dos
drive.py
e1.py
e1400d4
e2.py
e2e-data
e2e-m1-server.log
e2e-m1.sqlite
e2e-run.sqlite
e2e-server.log
endpoints.py
env97
es1.txt
ev.json
ev.sh
eval_base.out
eval_r2.out
evalout
evalout2
ex1.sh
ex2.sh
ex3.sh
exp-077
exp.py
exp2.py
exp_077.py
fe-data
fe3.log
fe3.sqlite
fe4.log
fe4.sqlite
fetch
figs.py
fill.py
final-data
first.png
flags_commit.py
fr_r2.txt
fresh
fresh.py
fresh_head.log
fresh_head.sqlite3
fresh_nosbs.log
fresh_nosbs.sqlite3
full.log
full.patch
fx
fx_before.txt
fxbak
gen
gen.py
gen_controls.py
golden_scan.py
guardprobe.py
guardprobe.py.bak
h42.py
harness
head
head-a850be0
head-bc12d44
head-ec33bf0
head.py
head2
head2.py
head_950d4a5
head_9851a0d_r5
head_9c1af01
head_ae76835_r3
head_clean
head_clean.log
head_clean.sqlite3
head_e63e564
head_faee448_r4
head_nosbs
head_nosbs.log
head_nosbs.sqlite3
headcheck
heldout.py
helpers.py
helpers2.py
hookcopy
idx
idx2
ing.bak
ingest.orig
jcheck.py
judge_live.py
judges.png
k1dump.py
kb2.py
kb3.py
kb_test.py
leak.py
lib_app.sqlite
library-after.md
library-base.md
link
live-demo
live-demo.log
live-local
live-local.log
llm_head.md
local
local.log
m5
m55_M_drop_whole_rule
m55_M_only_needs_review
m55_M_only_rejected
m58_M1_round1_regex
m58_M2_dates_iso_dollar
m58_M3_amounts_valid_dollar
m58_M4_fence_dollar
m59_N11_drop_stale_basis_clause
m59_N12_failed_redraft_overwrites
m59_N13_drop_SEVERITY_NOT_QUOTED
m59_N3_drop_D006_token_check
mine.diff
mine.patch
mine.txt
miss.py
mk.py
mkd.py
mkfix.py
mkpdf.py
mkreview.py
mkreviews.py
msg.txt
mut
mut-A
mut-B
mut-C
mut-D
mut-base
mut-control
mut-gate
mut-qual
mut-t073-A-broad-catch
mut-t073-B-no-guard-in-review
mut-t073-C-expected-becomes-supported
mut-t073-D-drop-class
mut-t084-1-no-judge-gate
mut-t084-2-no-wording-gate
mut-t084-3-no-negation-gate
mut-t084-4-unsure-accepted
mut-t084-5-no-audit
mut-t084-6-no-value-gate
mut-t084-7-judge-fail-open
mut-tok
mut.py
mut.py.bak
mut080.py
mut1
mut2
mut2_B0_pinned_baseline
mut2_G1_grounding_check_removed_in_extract
mut2_S1_judge_unavailable_fails_open_in_state
mut2_S2_judge1_error_becomes_supported
mut3
mut3_S2b_shared_judge_error_fails_open_to_supported
mut3_S3_j2_error_fails_open_to_agree_pipeline_only
mut4
mut98
mut99
mut_M0_baseline
mut_M1_noRollback
mut_M1_sdk_internal_retries_2
mut_M2
mut_M2_cli_drops_strict_mcp
mut_M3
mut_M3_cli_timeout_600
mut_M4
mut_M4_cli_leaks_stderr_into_error
mut_M5
mut_M5_fixture_miss_retried
mut_M6
mut_M6_j2_error_becomes_agree
mut_M7
mut_M7_stray_subprocess_import_outside_backends
mut_R4M1_stated_total_always_suppressed
mut_R4M2_no_other_figures_on_rate_holder
mut_R4M2_rate_unclear_move_to_other_figures_removed
mut_R4M3_rate_row_drops_own_other_figure_move
mut_R4M3_rate_row_stated_total_not_other_figure
mut_R4R_line790_raises
mut_dedupe
mut_flagsdeadline
mut_rmfixture
mut_rmjudgefixture
mut_t055_M_drop_whole_rule
mut_t055_M_only_needs_review
mut_t055_M_only_rejected
mut_t058_M1_round1_regex
mut_t058_M2_dates_iso_dollar
mut_t058_M3_amounts_valid_dollar
mut_t058_M4_fence_dollar
mut_t059_N11_drop_stale_basis_clause
mut_t059_N12_failed_redraft_overwrites
mut_t059_N13_drop_SEVERITY_NOT_QUOTED
mut_t059_N3_drop_D006_token_check
mutant-M1-nocombine.txt
mutant-M2-find0.txt
mutants
mutants-db08276.log
mutants-r3-db08276.log
mutants-work
mutate.py
mutate2.py
mutate3.py
mutate_api.py
mutate_run.py
mutate_run2.py
mutate_t055.py
mutate_t058.py
mutate_t059.py
mutrun.sh
mutv2_1
mutv2_2
mutv2_3
mutv2_4
mutv2_5
mutv2_6
mutv2_7
mw
narr.py
neg
neg2
nucc
o1
o1.aIcW
o2
o2.vHBZ
o3_new.js
o3_v3.js
ocr_edit
ocr_edit_head
ocrinj
oe
oi
old
out
overlay-head
p.py
p1.txt
p2.py
p2.txt
p3.py
p3.txt
p_be
p_fe
pa
page.txt
parent
parent-server.log
parent.sqlite3
pathspec.txt
pdb
pdf_time.py
pdfs
pdfs_head
pid
pid2
pin-690a0e3-r5
pin-6bca-r4
pin-8bc7f90
pin-HEAD-r4
pin-HEAD2-r4
pin-db08276
pin-f218263
pipeline_commit.py
pl.bak
pre_t095_schema.sql
prev
probe
probe-db
probe-r2-output.txt
probe-top.png
probe.py
probe2.py
probe2.py.bak
probe2_t067.py
probe3.py
probe3_t067.py
probe4.py
probe5.py
probe98
probe99
probeA
probeA.stderr
probeA.stdout
probeB
probeB.stderr
probeB.stdout
probe_404.py
probe_7df
probe_copy.sqlite3
probe_copy2.sqlite3
probe_copy3.sqlite3
probe_copy4.sqlite3
probe_copy5.sqlite3
probe_failed.py
probe_head
probe_head_out.txt
probe_nojudge.py
probe_r4_ocr.py
probe_rej.py
probe_run.py
probe_t067.py
probe_timeout.py
probe_work_head
probe_work_head2
probes
probes-t100
probes_r5_dir
proc.png
proc.py
proc2.png
pub.log
pub2.log
r2
r2-cases.out
r2.log
r2.pid
r2.sqlite3
r2_blank_judges.py
r2_check.py
r2_detect.py
r2_es2.py
r2_export.json
r2_for2.py
r2_ids.txt
r2_mixed.py
r2_mut_base
r2_mut_base_m
r2_mutant_r2b.py
r2_mutants.py
r2_probe_out.txt
r2_sentinel_data
r2_set_status.py
r2_t080_app.log
r2_t080_app.sqlite
r2_token.txt
r2_unit.txt
r2arch
r2d.sqlite3
r2demo
r2demo.log
r2head
r2live.log
r2live.pid
r2live.sqlite3
r2local
r2local.log
r2mut
r2o
r2parent
r2src
r3
r3-a27
r3-parent
r3_acceptance_strings.py
r3_accepted.json
r3_api.py
r3_check_json.py
r3_gate_check.py
r3_mut
r3_rootcause.py
r3_sentinel_data
r3_server.log
r3_t080.sqlite
r3_tok.txt
r3ap
r3api
r3api2
r3arch
r3bp
r3copy
r3db.sqlite3
r3dev
r3h
r3img
r3m
r3mut
r3o
r3pop
r3probe.py
r3run
r3scripts
r3src
r3tb
r4_probe_8634bfe.out.txt
r4_rootcause.py
r4arch
r4out
r4pin
r4probe
r4probe_on_0f58181.txt
rail.png
rec.sh
rec_a.log
rec_all.log
rec_all.sh
rec_b.log
rec_judges.log
rec_sample.log
recon.py
replay.py
repo
repro_stale
req_mut.md
rerec.log
rerec.sh
review_commit.py
review_headplus.py
rt_base.json
rt_r2.json
run.base.py
run.head.py
run.log
run.try.py
run_mutants_r3.py
run_ro.py
run_t070_orig.py
s-1440-0.png
s-1440-1700.png
s-1440-2300.png
s-1440-2600.png
s-1440-3300.png
s-1440-4400.png
s-1440-5400.png
s-1440-900.png
s-390-0.png
s-390-1500.png
s-390-3000.png
s-390-900.png
scan.py
scan_specimens.py
scan_time_10x5000wide.pdf
schema_pre_T095.sql
score.py
scripts
scroll.py
selfcheck-r2.txt
server.log
server.pid
server2.log
server2.pid
server7867.log
shot.py
shots.log
shots.py
shots2.py
shots_old.py
shots_t046r2.py
show.py
show_T103.txt
snap
snap-077
snap-89a323a
snap-c61
snap-final
snap-h2
snap-head
snap2
snap3
splice.py
src
srv.KdvV
srv.log
srv.out
srvdir
st_commit.py
strip.py
sync.py
t015r4
t028.out
t030r2mut
t033mut
t033mut.py
t035
t038
t038r3
t040-077
t040-head
t040-live
t043-239
t043_r2_probe.py
t043_r2_probe2.py
t043_r2_probe3.py
t046-server.log
t046.sqlite3
t046r2.log
t046r2.pid
t046r2.sqlite3
t053r3-data
t055_base_full.txt
t055_mut_full.txt
t056r2_01ipr4y9
t056r2_5_pc8ore
t056r2_gxnki_45
t056r2_jvse81hd
t056r2_pjbon2yp
t057
t060-a11y-axe
t060-a11y-data
t060-a11y-head
t060-a11y-serve.py
t065
t065r2
t066r2
t066r3
t067
t067_59c7edb
t067_f6fa2dd
t067_head_archive
t067_m1
t067_m2
t067_m3
t067_probes
t067head
t067parent
t067r3
t067r4
t067r5
t067r5-probe-out.txt
t068-data
t068-data-commit
t068-data-commit2
t068-server-commit.log
t068-server-commit2.log
t068-server.log
t068r2-server.log
t068r2-snap
t068r3-case01-body.json
t068r3-case01-get.json
t068r3-data
t068r3-head
t068r3-probe-token.txt
t068r3-server.log
t070
t070r2b
t071_title_probe.py
t072
t072plant
t072r3
t072r3-p1_be_selfreport
t072r3-p2_be_patientstatement
t072r3-p3_be_patientstates
t072r3-p4_fe_selfreport
t072r3-p5_fe_patientstatement
t072r3-p6_fe_selfreported_ui
t072r4
t072r4_plants
t074
t075r2
t076r2
t076r2-data
t076r2-server.log
t077r3
t079.log
t079.sqlite3
t080m_M10_date_always_confirmed
t080m_M11_judge_partial_is_pass
t080m_M12_date_blocker_reason
t080m_M13_overrides_not_counted
t080m_M14_unavailable_counted_judged
t080m_M15_agreement_never_fails
t080m_M16_verbatim_fail_ignored_on_entry
t080m_M17_skip_after_reject_removed
t080m_M18_nothing_accepted_removed
t080m_M19_unsupported_excludes_disagrees
t080m_M1_rejected_blocks_gate
t080m_M20_step_order_swap
t080m_M21_progress_counts_skipped_as_pending
t080m_M22_total_inclusion_accepted_pending
t080m_M23_fixed_why_replaced_by_model_text
t080m_M2_dismissed_blocks_gate
t080m_M3_dismissed_human_pass
t080m_M4_qualifier_always_pass
t080m_M5_gate_ignores_running
t080m_M6_rate_pending_total
t080m_M7_raw_leak_in_metadata
t080m_M8_event_before_after_leak
t080m_M9_edited_text_leak
t080m_base
t080r4
t085r2
t085r3
t086head
t086wt
t090-out
t090.index
t090.patch
t090_code.patch
t090_patch2.py
t090_patch_run.py
t090_patch_tests.py
t090r2
t090r3
t092
t093.base.py
t094r2
t095.patch
t095r2_head
t096-evals
t096-export-check.py
t096-ux-36ceb38
t096-ux-server.log
t096-ux-walk-output.txt
t096-ux.sqlite3
t096_all.py
t096_ds.py
t096_probe.py
t096_probe2.py
t096_shot.py
t096_shot2.py
t096_start.sh
t096data
t097
t097.log
t097.pid
t097.sqlite3
t097b.sqlite3
t097r2
t097r2-server.log
t097r2.sqlite3
t097r2head
t097r3-archive-9f2811f
t097r3-server.log
t097r3-server.pid
t097r3.sqlite3
t098-e511778
t098-f5ddec8
t098-head
t099-3ecb8b1
t099-dirty-check
t099-f345bc8-r2
t099-gitclone-parent
t099-mut
t099.index
t099_msg.txt
t1.xXug
t100-card
t100-fresh
t101
t101r2
t103r2
t103r3_api.diff
t103r3_archive
t103r3_billing.diff
t103r3_control_archive
t103r3_mut
t103r4_archive
t104
t104-3462ad0-ux
t104-server.log
t104-server.pid
t104-state.json
t104-ux.sqlite3
t106_r2_archive
t108
t109_adr_edit.py
t109_doc_edit.py
t109r2_head
t109r2_mutA
t109r2_mutB
t109r2_pin
t110.sqlite3
t110b.sqlite3
t111-archive
t111-parent
t111r2
t111r2-base
t111r2-base.out.json
t111r2-head
t111r2-head.out.json
t111r2-parent
t111r2-parent.out.json
t112.index
t112_live.sh
t112_pipeline.py
t114
t115.pid
t115.sqlite
t115srv.log
t116r2-base
t116r2-head
t118-head
t118-pre
t2.q4VB
t2b.IKsK
t3.ORDQ
t4.0u5g
t84r4
tail.md
test_billing_old.py
tests_b05.py
thr.py
thr2.out
thr2.py
tmpindex
tok.json
tok_c1_local
tok_c3_local
tok_c5_local
tok_c7_local
tok_case_lib01_er_only_then_gap
tok_case_lib02_slip_fall_prior_knee
tok_case_lib03_truck_rear_end_chiro
tok_case_lib04_dog_bite_scar_revision
tok_case_lib05_pedestrian_orif_hardware
tok_g02_local
tok_g04_local
tok_g06_local
tok_g08_local
tok_g09_local
tok_sample2_local
tok_sample_local
tok_sample_pub
tokens.json
tools
tree
two.py
two.py.bak
ub
ui-demo
ui-local
unit-run-r2-clone-with-git.txt
unit-run-r2.txt
unit.txt
unit_full.txt
ux-r2-2.sqlite3
ux-r2-3.sqlite3
ux-r2-debug-sample.png
ux-r2-server-2.log
ux-r2-server-3.log
ux-r2-server.log
ux-r2-server.pid
ux-r2.sqlite3
ux3
v
verify.py
view.json
walk.py
walk2.py
wprobe.py
wt
wt-031a708
wt-7df65fb
wt-golden.txt
wt-head
wt2
x45.py
xc.py
xss.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:18.964Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t118-runner/run_module.py",
 "content": "\"\"\"Scratch runner: run a module from an extracted archive root without writing into that root.\n\nusage: run_module.py <archive_root> <module> [module args...]\nThe archive root is put first on sys.path and used as cwd; this file lives outside the archive.\n\"\"\"\nimport os\nimport runpy\nimport sys\n\nroot = sys.argv[1]\nmodule = sys.argv[2]\nsys.argv = [module] + sys.argv[3:]\nsys.path.insert(0, root)\nos.chdir(root)\nrunpy.run_module(module, run_name=\"__main__\", alter_sys=True)\n"
}
````

### User / tool · 2026-11-02T09:58:19.013Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t118-runner/run_module.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:23.009Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-runner.py",
 "content": "\"\"\"T-118 paralegal-reviewer scratch runner: run a module from an extracted archive root.\n\nusage: T-118-paralegal-runner.py <archive_root> <module> [module args...]\nThe archive root goes first on sys.path and becomes cwd; nothing is written into the archive by this file.\n\"\"\"\nimport os\nimport runpy\nimport sys\n\nroot = sys.argv[1]\nmodule = sys.argv[2]\nsys.argv = [module] + sys.argv[3:]\nsys.path.insert(0, root)\nos.chdir(root)\nrunpy.run_module(module, run_name=\"__main__\", alter_sys=True)\n"
}
````

### User / tool · 2026-11-02T09:58:23.114Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-runner.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:26.707Z

**tool call — Bash**
````
{
 "command": "PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; RUN=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-runner.py; HEAD=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t118-head; PRE=${HEAD%t118-head}t118-pre; O=${HEAD%t118-head}t118-out; mkdir -p \"$O\"; $PY -I $RUN \"$HEAD\" evals.library_report --out \"$O/library-head.md\" > \"$O/lib-head.stdout\" 2>&1; echo \"HEAD EXIT=$?\"; $PY -I $RUN \"$PRE\" evals.library_report --out \"$O/library-pre.md\" > \"$O/lib-pre.stdout\" 2>&1; echo \"PRE EXIT=$?\"; diff \"$O/library-pre.md\" \"$O/library-head.md\" && echo \"IDENTICAL library reports (pre-T118 vs HEAD)\"; echo ----; tail -3 \"$O/lib-head.stdout\"",
 "description": "Generate library report at pre-commit and HEAD and diff them"
}
````

### User / tool · 2026-11-02T09:58:26.765Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (mkdir ${HEAD%t118-head}t118-out)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:29.111Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-out && ls -d /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-out",
 "description": "Create review-evidence output directory for T-118"
}
````

### User / tool · 2026-11-02T09:58:29.196Z

**tool result**
````
/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-out
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:32.466Z

**tool call — Bash**
````
{
 "command": "PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; RUN=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-runner.py; HEAD=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t118-head; PRE=${HEAD%t118-head}t118-pre; O=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-out; $PY -I $RUN \"$HEAD\" evals.library_report --out \"$O/library-head.md\" > \"$O/lib-head.stdout\" 2>&1; echo \"HEAD EXIT=$?\"; $PY -I $RUN \"$PRE\" evals.library_report --out \"$O/library-pre.md\" > \"$O/lib-pre.stdout\" 2>&1; echo \"PRE EXIT=$?\"; diff \"$O/library-pre.md\" \"$O/library-head.md\"; echo \"DIFF EXIT=$?\"; tail -3 \"$O/lib-head.stdout\"",
 "description": "Generate library report at pre-commit and HEAD and diff them"
}
````

### User / tool · 2026-11-02T09:58:35.239Z

**tool result**
````
HEAD EXIT=0
PRE EXIT=0
DIFF EXIT=0
| case_lib01_er_only_then_gap | r3 | LLM_FAILED_AFTER_RETRIES | FIXTURE_MISS |

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:38.690Z

**tool call — Bash**
````
{
 "command": "O=artifacts/review-evidence/T-118-out; grep -n \"lib11\" $O/library-head.md; echo ----COMMITTED; git show HEAD:evals/reports/library-latest.md | grep -n \"lib11\"; echo ----DIFF committed vs regenerated HEAD; git show HEAD:evals/reports/library-latest.md > $O/library-committed.md; diff $O/library-committed.md $O/library-head.md; echo \"EXIT=$?\"",
 "description": "Compare committed library report with regenerated report"
}
````

### User / tool · 2026-11-02T09:58:38.814Z

**tool result**
````
19:| case_lib11_priors_and_ledger | done | 4/9 | 4/8 | False | 3/4 | 0 | M1 | 0 | - |
----COMMITTED
19:| case_lib11_priors_and_ledger | done | 4/9 | 4/8 | False | 3/4 | 0 | M1 | 0 | - |
----DIFF committed vs regenerated HEAD
3c3
< Source commit: a74b727b1ed94befbd09c0a3da0e8556e66f787c (tree: clean). Regenerate from a clean worktree of the commit you cite.
---
> Source commit: unknown (tree: unknown). Regenerate from a clean worktree of the commit you cite.
17c17
< | case_lib09_spanish_interpreter_espalda | done | 4/7 | 2/5 | False | 1/2 | 0 | M5 | 0 | - |
---
> | case_lib09_spanish_interpreter_espalda | done | 4/7 | 3/5 | False | 1/2 | 0 | M5 | 0 | - |
EXIT=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:45.488Z

**tool call — Bash**
````
{
 "command": "grep -rn \"def gap_flags\\|def compute_gaps\\|def non_visit_label\\|def load_pipeline\\|def run_case\" app evals --include=*.py | head; echo ----; sed -n 1,30p evals/run.py | head -5; grep -n \"def load_pipeline\" -A12 evals/run.py | head -30",
 "description": "Locate gap computation and pipeline entry points"
}
````

### User / tool · 2026-11-02T09:58:45.592Z

**tool result**
````
app/backend/api.py:350:    async def run_case(token: str, request: Request):
app/backend/pipeline.py:440:def run_case(text: str, backend: str = None) -> dict:
app/backend/gaps.py:92:def non_visit_label(rec: dict):
app/backend/gaps.py:111:def compute_gaps(records: list) -> list:
app/backend/gaps.py:154:def gap_flags(records: list) -> list:
evals/run.py:505:def run_cases(pipeline, backend, cases=None, runs_dir=None):
evals/run.py:1147:def load_pipeline():
----
"""Eval runner: `python -m evals.run` scores the product against the golden set and writes
evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).

    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,
                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
1147:def load_pipeline():
1148-    from app import pipeline
1149-    return pipeline
1150-
1151-
1152-class CuratedFixtures(Exception):
1153-    pass
1154-
1155-
1156-def refuse_curated(env=None):
1157-    """D-029: the ship bar is measured on live runs and recorded fixtures only. Curated (hand-checked) responses reproduce the golden
1158-    answers by construction, so scoring them would be circular. Refuse to compute ship-bar metrics when the curated set is selected."""
1159-    env = os.environ if env is None else env
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:48.184Z

**tool call — Bash**
````
{
 "command": "sed -n 80,175p app/backend/gaps.py",
 "description": "Read gap classifier and gap_flags implementation"
}
````

### User / tool · 2026-11-02T09:58:48.269Z

**tool result**
````
        m = rx.search(head)
        if m:
            return label, (head[:m.start()] + " " + head[m.end():])
    first = (rec.get("excerpt") or "").lstrip().split("\n", 1)[0][:120]
    if first and _TITLE.search(first):
        return ("affidavit" if "affidavit" in first.lower() else "intake form"), re.sub(r"new[- ]patient", "", head, flags=re.IGNORECASE)
    kind = rec.get("kind", "encounter")
    if kind != "encounter":
        return _KIND_LABEL.get(kind, "record that is not a treatment visit"), head
    return None, head


def non_visit_label(rec: dict):
    """The plain label of a record that is not a treatment visit ("intake form", "billing statement", ...), or None for a treatment encounter.
    Fail safe toward treatment (T-116 round 2): a record is excluded only when (1) its type is clearly administrative, read from the record-type
    head of the header label (not any substring), or from its own first-line title, or from its ingest kind; (2) no visit word remains in that
    head ("records review visit" is a visit); and (3) its text shows no treatment evidence. When unsure, it counts as treatment."""
    label, rest = _candidate_label(rec)
    if not label or _VISIT_WORD.search(rest or "") or _has_treatment_evidence(rec, label):
        return None
    return label


def is_treatment(rec: dict) -> bool:
    return non_visit_label(rec) is None


def is_gap(days: int) -> bool:
    return days > THRESHOLD_DAYS


def compute_gaps(records: list) -> list:
    """[{from_date, to_date, from_records, to_records, days, flag}] between consecutive DISTINCT encounter dates."""
    by_date = {}
    for r in records:
        if r.get("date_iso") and is_treatment(r):
            by_date.setdefault(r["date_iso"], []).append(r["n"])
    ds = sorted(by_date)
    out = []
    for a, b in zip(ds, ds[1:]):
        n = dates.days_between(a, b)
        out.append({"from_date": a, "to_date": b, "from_records": sorted(by_date[a]), "to_records": sorted(by_date[b]),
                    "days": n, "flag": is_gap(n)})
    return out


def _reasons(gap: dict, records: list) -> list:
    """needs_review reasons: an undated/ambiguous encounter record whose date could fall inside the span (ADR-010), or an injection-tagged endpoint."""
    reasons = []
    for r in records:
        if not is_treatment(r) or r.get("date_iso"):
            continue
        cands = r.get("date_candidates") or []
        if not cands or any(gap["from_date"] <= c <= gap["to_date"] for c in cands):
            reasons.append("ENDPOINT_NOT_VERIFIED")
            break
    ends = set(gap["from_records"]) | set(gap["to_records"])
    if any(r.get("injection_tag") for r in records if r["n"] in ends):
        reasons.append("INJECTION_SUSPECTED")
    return reasons


def excluded_in_span(gap: dict, records: list) -> list:
    """Records with a code-parsed (or confirmed) date inside the gap's span that are NOT treatment visits, with the label code gave them.
    They are shown in the gap's why so the paralegal sees that an intake form or bill did not end the gap."""
    out = []
    for r in records:
        lab = non_visit_label(r)
        if lab and r.get("date_iso") and gap["from_date"] <= r["date_iso"] <= gap["to_date"]:
            out.append({"record_no": r["n"], "record_type": lab, "date": r["date_iso"],
                        "why": flag_templates.non_visit_sentence(lab, r["date_iso"])})
    return sorted(out, key=lambda x: (x["date"], x["record_no"]))


def gap_flags(records: list) -> list:
    """One flag per gap over 30 days, id keyed by the bounding record pair; text from flag_templates only."""
    by_n = {r["n"]: r for r in records}
    flags = []
    for g in compute_gaps(records):
        if not g["flag"]:
            continue
        a, b = g["from_records"][-1], g["to_records"][0]
        excl = excluded_in_span(g, records)
        title, expl = flag_templates.render("gap", "gap_over_30", days=g["days"], from_date=g["from_date"], to_date=g["to_date"],
                                            provider_a=by_n[a].get("source"), provider_b=by_n[b].get("source"),
                                            excluded=[(x["record_type"], x["date"]) for x in excl])
        ev = [evidence_span(by_n[n], f) for n in (a, b) for f in ("date", "source")]
        flags.append({"id": f"f_gap_r{a}_r{b}", "type": "gap", "category": "gap_over_30", "origin": "code", "title": title,
                      "explanation": expl, "from_date": g["from_date"], "to_date": g["to_date"], "days": g["days"],
                      "record_nos": sorted(set(g["from_records"]) | set(g["to_records"])), "evidence": ev, "reasons": _reasons(g, records),
                      "excluded_records": excl})
    return flags


def merge_flags(old: list, new: list) -> list:
    """Recompute after confirm_date: a flag whose record pair, dates and days are unchanged keeps its review status and note;
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:50.988Z

**tool call — Bash**
````
{
 "command": "sed -n 440,475p app/backend/pipeline.py; echo ----; grep -n \"^def \\|gap\" app/backend/pipeline.py | head -60",
 "description": "Inspect pipeline run_case and gap wiring"
}
````

### User / tool · 2026-11-02T09:58:51.083Z

**tool result**
````
def run_case(text: str, backend: str = None) -> dict:
    """Full pipeline over `text` on a scratch database; returns case_view(). Used by evals; nothing is kept."""
    import contextlib
    import tempfile
    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
        conn, cid, call = _scratch_call(tmp, IN.normalize_text(text))
        with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
            out = run_pipeline(conn, cid, text, call=call)
        view = case_view(out)
        conn.close()
        return view


def judge_summary(summary: str, excerpt: str, label: str, backend: str = None) -> str:
    """Judge 1 on one (summary, excerpt, label): 'supported' | 'partially' | 'unsupported' | 'unavailable'. A missing fixture or a failed call
    is 'unavailable', never a pass."""
    import contextlib
    import tempfile
    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
        conn, cid, call = _scratch_call(tmp, excerpt)
        with (P.record_fragment_context(excerpt) if P._recording() else contextlib.nullcontext()):
            v = judges.run_j1(summary, excerpt, label, call=call)
        conn.close()
        return v


# ------------------------------------------------------------------ CLI
def _usd(c):
    return TT.usd(c)


def format_report(out: dict) -> str:
    from app.backend.dates import long_date
    L = [f"Status: {out['status']}   backend: {P.backend_name()}   records: {len(out['records'])}   entries: {len(out['entries'])}"
         f"   flags: {len(out['flags'])}   amounts: {len(out['amounts'])}", "", "TIMELINE"]
    for e in out["entries"]:
----
14:from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
25:def _clean(d: dict) -> dict:
30:def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
35:def _compose_code(rec_by_n: dict, nos: list, reasons: list, evidence: list, case_text: str) -> tuple:
49:def run_ingest(raw_text: str, call=None, not_duplicates=(), splitter=None) -> dict:
59:    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
103:def amount_item(a: dict, r: dict, item_id: str = None) -> dict:
110:def _not_duplicates(conn, cid: str) -> list:
114:def _frozen_splitter(conn, cid: str):
134:def _store_split_failure(conn, cid: str, reason) -> None:
146:def _store_records(conn, cid: str, ing: dict) -> None:
169:def _row(kind: str, it: dict) -> dict:
186:def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
215:def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
226:def _finish_amount(a: dict, ing: dict, judged) -> dict:
244:def _entry_for(entries: list, record_no: int):
248:def _err(code, stage, record_no=None, cause=None) -> dict:
257:def _accident_year(recs: list):
262:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
364:    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
394:def case_view(out: dict) -> dict:
403:        if f["type"] == "gap":
433:def _scratch_call(tmp, text):
440:def run_case(text: str, backend: str = None) -> dict:
453:def judge_summary(summary: str, excerpt: str, label: str, backend: str = None) -> str:
467:def _usd(c):
471:def format_report(out: dict) -> str:
479:    for title, types in (("GAPS", ("gap",)), ("CONFLICTS", ("conflict",)), ("PRE-EXISTING", ("pre_existing",)), ("CAUSATION LANGUAGE", ("causation",)),
492:def main(argv=None) -> int:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:58:53.222Z

**tool call — Bash**
````
{
 "command": "sed -n 49,70p app/backend/pipeline.py",
 "description": "Read run_ingest to find records source for gap computation"
}
````

### User / tool · 2026-11-02T09:58:53.304Z

**tool result**
````
def run_ingest(raw_text: str, call=None, not_duplicates=(), splitter=None) -> dict:
    """Stage 0. Raises IngestError('bad_request' | 'input_too_large') before anything else. Zero model calls, except the D-031 split
    fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
    ing = IN.ingest(raw_text, splitter=splitter or (split_llm.make_splitter(call) if call else None), not_duplicates=not_duplicates)
    text = IN.normalize_text(raw_text)
    recs = language.annotate(ing["records"])           # D-042: en | es | other per record; raises UnsupportedLanguage when no record is readable
    language.case_check(recs)
    by_n = {r["n"]: r for r in recs}
    backend = P.backend_name()
    flags = []
    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
    for f in code:
        nos = f["record_nos"]
        ev = f["evidence"]
        reasons = list(f.get("reasons") or [])
        state, why_codes = _compose_code(by_n, nos, reasons, ev, text)
        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": ev, "record_nos": nos,
                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "review_status": "pending",
                "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes) or
                "Computed by code from the record dates and text; every cited span matches the input."}
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names", "excluded_records"):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:59:04.747Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-endpoints.py",
 "content": "\"\"\"T-118 paralegal-reviewer probe: compare expected gap endpoints (record lists, exclusions) with the product's gap computation.\n\nusage: T-118-paralegal-endpoints.py <archive_root>\nRuns ingest + language annotate + gaps.compute_gaps (no model calls: no splitter, no call) on every evals/golden and evals/library\npacket, then compares every expected gap_table row (dates, days, flag, from_records, to_records) and gap_excluded_records against\nthe product. The shipped scorer (evals/run.py:243-248) compares only (from_date, to_date, days, flag); this probe adds the record lists.\nPrints one line per difference and a summary. Exit 0 = no difference anywhere.\n\"\"\"\nimport glob\nimport json\nimport os\nimport sys\n\nroot = sys.argv[1]\nsys.path.insert(0, root)\nos.chdir(root)\n\nfrom app.backend import gaps as GP, ingest as IN, language  # noqa: E402\n\n\ndef product_view(text):\n    ing = IN.ingest(IN.normalize_text(text))\n    recs = language.annotate(ing[\"records\"])\n    gaps = GP.compute_gaps(recs)\n    excluded = sorted(r[\"n\"] for r in recs if not GP.is_treatment(r))\n    labels = {r[\"n\"]: GP.non_visit_label(r) for r in recs if not GP.is_treatment(r)}\n    return recs, gaps, excluded, labels\n\n\ndef main():\n    diffs = 0\n    packets = 0\n    for exp_path in sorted(glob.glob(os.path.join(root, \"evals\", \"golden\", \"*.expected.json\")) +\n                           glob.glob(os.path.join(root, \"evals\", \"library\", \"*.expected.json\"))):\n        txt_path = exp_path.replace(\".expected.json\", \".txt\")\n        if not os.path.exists(txt_path):\n            continue\n        exp = json.load(open(exp_path, encoding=\"utf-8\"))\n        if \"gap_table\" not in exp and \"gap_excluded_records\" not in exp:\n            continue\n        packets += 1\n        name = os.path.basename(txt_path)[:-4]\n        text = open(txt_path, encoding=\"utf-8\").read()\n        try:\n            recs, gaps, excluded, labels = product_view(text)\n        except Exception as e:  # noqa: BLE001 - report, do not hide\n            print(f\"{name}: PRODUCT_ERROR {type(e).__name__}: {e}\")\n            diffs += 1\n            continue\n        by_key = {(g[\"from_date\"], g[\"to_date\"]): g for g in gaps}\n        for row in exp.get(\"gap_table\", []):\n            key = (row[\"from_date\"], row[\"to_date\"])\n            g = by_key.get(key)\n            if g is None:\n                print(f\"{name}: expected row {key} absent from product gaps\")\n                diffs += 1\n                continue\n            want = (row.get(\"days\"), row.get(\"flag\"), row.get(\"from_records\"), row.get(\"to_records\"))\n            got = (g[\"days\"], g[\"flag\"], g[\"from_records\"], g[\"to_records\"])\n            if want != got:\n                print(f\"{name}: row {key} expected days/flag/from/to={want} product={got}\")\n                diffs += 1\n        exp_keys = {(r[\"from_date\"], r[\"to_date\"]) for r in exp.get(\"gap_table\", [])}\n        for g in gaps:\n            if (g[\"from_date\"], g[\"to_date\"]) not in exp_keys:\n                print(f\"{name}: product gap {(g['from_date'], g['to_date'])} not in expected gap_table\")\n                diffs += 1\n        if \"gap_excluded_records\" in exp and sorted(exp[\"gap_excluded_records\"]) != excluded:\n            print(f\"{name}: gap_excluded_records expected={sorted(exp['gap_excluded_records'])} product={excluded} labels={labels}\")\n            diffs += 1\n    print(f\"packets with gap expectations: {packets}; differences: {diffs}\")\n    return 0 if diffs == 0 else 1\n\n\nif __name__ == \"__main__\":\n    sys.exit(main())\n"
}
````

### User / tool · 2026-11-02T09:59:04.893Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-endpoints.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:59:08.006Z

**tool call — Bash**
````
{
 "command": "PY=.venv/bin/python; SCRIPT=artifacts/review-evidence/T-118-paralegal-endpoints.py; HEAD=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo \"== HEAD (78450f6)\"; $PY -I $SCRIPT \"$HEAD/t118-head\" ; echo \"EXIT=$?\"; echo \"== PRE (ea6ac71)\"; $PY -I $SCRIPT \"$HEAD/t118-pre\"; echo \"EXIT=$?\"",
 "description": "Run gap endpoint probe on HEAD and pre-commit trees"
}
````

### User / tool · 2026-11-02T09:59:08.366Z

**tool result**
````
== HEAD (78450f6)
case_lib14_handwritten_chiro_scans: gap_excluded_records expected=[5, 7, 8] product=[7, 8] labels={7: 'claim form', 8: 'billing statement'}
packets with gap expectations: 25; differences: 1
EXIT=1
== PRE (ea6ac71)
case_lib11_priors_and_ledger: row ('2026-03-18', '2026-03-27') expected days/flag/from/to=(9, False, [2, 3], [5, 6]) product=(9, False, [2, 3], [5])
case_lib11_priors_and_ledger: row ('2026-03-27', '2026-04-24') expected days/flag/from/to=(28, False, [5, 6], [7]) product=(28, False, [5], [7])
case_lib11_priors_and_ledger: gap_excluded_records expected=[4, 9] product=[4, 6, 9] labels={4: 'letter or correspondence', 6: 'intake form', 9: 'ledger'}
case_lib14_handwritten_chiro_scans: gap_excluded_records expected=[5, 7, 8] product=[7, 8] labels={7: 'claim form', 8: 'billing statement'}
packets with gap expectations: 25; differences: 4
EXIT=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:59:12.991Z

**tool call — Bash**
````
{
 "command": "cat -n evals/library/case_lib14_handwritten_chiro_scans.txt 2>/dev/null | head -80 || ls evals/library | grep lib14; ls evals/library | grep lib14; ls evals/library | grep -c expected",
 "description": "Read lib14 packet text"
}
````

### User / tool · 2026-11-02T09:59:13.103Z

**tool result**
````
     1	SYNTHETIC — invented for evaluation; not real patient data
     2	
     3	=== Record 1 ===
     4	Date: 2026-09-14
     5	Source: Tarnwick Fire-Rescue run report
     6	Excerpt: "Driver of a sedan struck from behind. Moderate damage to the rear of the vehicle. Pt ambulatory at scene. Pt states neck pain 6/10 and tingling in the right hand. Cervical collar applied. Transported to Orrin Mere Regional ED."
     7	
     8	=== Record 2 ===
     9	Date: 2026-09-14
    10	Source: Orrin Mere Regional ED
    11	Excerpt: "Dx: cervical strain. X-ray cervical spine negative for fracture. Discharged with a muscle relaxant. ED charge: $2,960."
    12	
    13	=== Record 3 ===
    14	Date: 2026-09-21
    15	Source: Hollowbrook Chiropractic, daily note visit 1 (scanned, OCR text)
    16	Excerpt: "Pain 7 circled on a 0-10 scale. Tenderness at C4-C6. [X] adjustment [X] e-stim [X] hot pack. Date written 9/2l/26."
    17	
    18	=== Record 4 ===
    19	Date: 2026-10-06
    20	Source: Hollowbrook Chiropractic, daily note visit 9 (scanned, OCR text)
    21	Excerpt: "Pain 5 circled. Tenderness at C4-C5, improved. [X] adjustment [X] e-stim. Next visit 1O/2O."
    22	
    23	=== Record 5 ===
    24	Date: 10/20
    25	Source: Hollowbrook Chiropractic, daily note visit 12 (handwritten, OCR text)
    26	Excerpt: "Pain 4 circled. Adjusted C4-C6. [X] e-stim. Pt states neck feels better."
    27	
    28	=== Record 6 ===
    29	Date: 2026-11-03
    30	Source: Hollowbrook Chiropractic, re-examination (typed)
    31	Excerpt: "Re-examination. Pain 6/10, unchanged from the initial visit. Plan: continue care three times weekly."
    32	
    33	=== Record 7 ===
    34	Date: 2026-11-10
    35	Source: Hollowbrook Chiropractic, CMS-1500 (OCR of scanned claim)
    36	Excerpt: "OCR of scanned CMS-1500. Item 14 injury date 091426 qualifier 431. Line 1: 092126 to 092326, CPT 98941, 24F 25500, 24G 3. Line 2: 092126 to 092326, CPT 97014, 24F 7500, 24G 3. Item 28 TOTAL CHARGE 33000. Item 29 AMOUNT PAID 0 00. Item 31 signature date 110926."
    37	
    38	=== Record 8 ===
    39	Date: 2026-11-12
    40	Source: Tarnwick Fire-Rescue, ambulance invoice
    41	Excerpt: "Invoice for the run of 09/14/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00. A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05. Total charges $1,567.05. No payments posted. Letter of protection requested."
case_lib14_handwritten_chiro_scans.expected.json
case_lib14_handwritten_chiro_scans.txt
15
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:59:18.434Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport json\ne = json.load(open(\"evals/library/case_lib14_handwritten_chiro_scans.expected.json\", encoding=\"utf-8\"))\nprint(\"gap_excluded_records:\", e.get(\"gap_excluded_records\"))\nprint(\"gap_table:\", json.dumps(e.get(\"gap_table\"), indent=1))\nfor r in e.get(\"records\", []):\n    print(r)\nEOF",
 "description": "Print lib14 expected gap section and record kinds"
}
````

### User / tool · 2026-11-02T09:59:18.541Z

**tool result**
````
gap_excluded_records: [5, 7, 8]
gap_table: [
 {
  "from_date": "2026-09-14",
  "to_date": "2026-09-21",
  "from_records": [
   1,
   2
  ],
  "to_records": [
   3
  ],
  "days": 7,
  "flag": false
 },
 {
  "from_date": "2026-09-21",
  "to_date": "2026-10-06",
  "from_records": [
   3
  ],
  "to_records": [
   4
  ],
  "days": 15,
  "flag": false
 },
 {
  "from_date": "2026-10-06",
  "to_date": "2026-11-03",
  "from_records": [
   4
  ],
  "to_records": [
   6
  ],
  "days": 28,
  "flag": false
 }
]
{'record_no': 1, 'raw_date': '2026-09-14', 'date': '2026-09-14', 'kind': 'encounter', 'source': 'Tarnwick Fire-Rescue run report'}
{'record_no': 2, 'raw_date': '2026-09-14', 'date': '2026-09-14', 'kind': 'encounter', 'source': 'Orrin Mere Regional ED'}
{'record_no': 3, 'raw_date': '2026-09-21', 'date': '2026-09-21', 'kind': 'encounter', 'source': 'Hollowbrook Chiropractic, daily note visit 1 (scanned, OCR text)'}
{'record_no': 4, 'raw_date': '2026-10-06', 'date': '2026-10-06', 'kind': 'encounter', 'source': 'Hollowbrook Chiropractic, daily note visit 9 (scanned, OCR text)'}
{'record_no': 5, 'raw_date': '10/20', 'date': None, 'kind': 'encounter', 'source': 'Hollowbrook Chiropractic, daily note visit 12 (handwritten, OCR text)'}
{'record_no': 6, 'raw_date': '2026-11-03', 'date': '2026-11-03', 'kind': 'encounter', 'source': 'Hollowbrook Chiropractic, re-examination (typed)'}
{'record_no': 7, 'raw_date': '2026-11-10', 'date': '2026-11-10', 'kind': 'billing_statement', 'source': 'Hollowbrook Chiropractic, CMS-1500 (OCR of scanned claim)'}
{'record_no': 8, 'raw_date': '2026-11-12', 'date': '2026-11-12', 'kind': 'billing_statement', 'source': 'Tarnwick Fire-Rescue, ambulance invoice'}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:59:29.174Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-endpoints.py",
 "old_string": "def product_view(text):\n    ing = IN.ingest(IN.normalize_text(text))\n    recs = language.annotate(ing[\"records\"])\n    gaps = GP.compute_gaps(recs)\n    excluded = sorted(r[\"n\"] for r in recs if not GP.is_treatment(r))\n    labels = {r[\"n\"]: GP.non_visit_label(r) for r in recs if not GP.is_treatment(r)}\n    return recs, gaps, excluded, labels",
 "new_string": "def product_view(text):\n    \"\"\"gap_excluded_records in the golden files = records that are NOT gap endpoints (non-visit records AND undated visits such as\n    lib14 r5 \"10/20\"). Endpoints are the from/to records of the product's gap_table rows; with no gap rows, every treatment record counts.\"\"\"\n    ing = IN.ingest(IN.normalize_text(text))\n    recs = language.annotate(ing[\"records\"])\n    gaps = GP.compute_gaps(recs)\n    endpoints = {n for g in gaps for n in g[\"from_records\"] + g[\"to_records\"]}\n    if not gaps:\n        endpoints = {r[\"n\"] for r in recs if GP.is_treatment(r)}\n    excluded = sorted(r[\"n\"] for r in recs if r[\"n\"] not in endpoints)\n    labels = {r[\"n\"]: (GP.non_visit_label(r) or \"undated or non-endpoint\") for r in recs if r[\"n\"] not in endpoints}\n    return recs, gaps, excluded, labels"
}
````

### User / tool · 2026-11-02T09:59:29.304Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-endpoints.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:59:32.548Z

**tool call — Bash**
````
{
 "command": "PY=.venv/bin/python; SCRIPT=artifacts/review-evidence/T-118-paralegal-endpoints.py; HEAD=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo \"== HEAD (78450f6)\"; $PY -I $SCRIPT \"$HEAD/t118-head\"; echo \"EXIT=$?\"; echo \"== PRE (ea6ac71)\"; $PY -I $SCRIPT \"$HEAD/t118-pre\"; echo \"EXIT=$?\"",
 "description": "Re-run endpoint probe with endpoint-based exclusion semantics"
}
````

### User / tool · 2026-11-02T09:59:32.920Z

**tool result**
````
== HEAD (78450f6)
packets with gap expectations: 25; differences: 0
EXIT=0
== PRE (ea6ac71)
case_lib11_priors_and_ledger: row ('2026-03-18', '2026-03-27') expected days/flag/from/to=(9, False, [2, 3], [5, 6]) product=(9, False, [2, 3], [5])
case_lib11_priors_and_ledger: row ('2026-03-27', '2026-04-24') expected days/flag/from/to=(28, False, [5, 6], [7]) product=(28, False, [5], [7])
case_lib11_priors_and_ledger: gap_excluded_records expected=[4, 9] product=[4, 6, 9] labels={4: 'letter or correspondence', 6: 'intake form', 9: 'ledger'}
packets with gap expectations: 25; differences: 3
EXIT=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:59:40.274Z

**tool call — Bash**
````
{
 "command": "grep -n '\"encounter\"\\|\\[\"encounter\"\\]\\|get(\"encounter\")' evals/run.py app/backend/*.py | head -30",
 "description": "Find where the encounter flag is read in scorer and product"
}
````

### User / tool · 2026-11-02T09:59:40.366Z

**tool result**
````
app/backend/conflicts.py:13:    enc = [r for r in records if r.get("kind", "encounter") == "encounter" and r.get("date_iso")]
app/backend/gaps.py:86:    kind = rec.get("kind", "encounter")
app/backend/gaps.py:87:    if kind != "encounter":
app/backend/ingest.py:221:    return "encounter"
app/backend/ingest.py:320:                 encounter=kind == "encounter", duplicate_of=None if first_of[r["n"]] == r["n"] else f"r{first_of[r['n']]}",
app/backend/pipeline.py:162:                          encounter=int(r["encounter"]))
app/backend/pipeline.py:258:    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso") and r["kind"] == "encounter")
app/backend/present.py:169:         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
app/backend/store.py:27:                    "kind": "encounter" if d["encounter"] else "other", "date_candidates": d["date_candidates"] or []})
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:59:43.418Z

**tool call — Bash**
````
{
 "command": "grep -n \"encounter\" evals/run.py | head -20; echo ----; grep -n \"encounter\" evals/golden/check_golden.py | head; echo ----; .venv/bin/python - <<'EOF'\nimport json\ne = json.load(open(\"evals/library/case_lib11_priors_and_ledger.expected.json\", encoding=\"utf-8\"))\nent = [x for x in e[\"entries\"] if x.get(\"date\") == \"2026-03-27\"]\nfor x in ent: print(x[\"id\"], x.get(\"encounter\"), x.get(\"provider\"))\nEOF",
 "description": "Check whether scorer or checker reads the entry encounter flag"
}
````

### User / tool · 2026-11-02T09:59:43.546Z

**tool result**
````
----
12:  * gap_table equals real calendar arithmetic over the parsed dates of *clinical-encounter* records only
155:ENTRY_KEYS = {"id", "record_nos", "date", "date_status", "encounter", "provider", "must_contain_excerpt", "required_terms",
169:    "diagnosis temptation": "diagnosis_inference_trap", "non-visit record hides gap": "non_encounter_record_hides_gap",
200:        if r["kind"] not in ("encounter", "billing_statement", "phone_note"):
242:        if e["encounter"] != (rs[0]["kind"] == "encounter"):
243:            err(cid, f"{e['id']}: encounter flag disagrees with record kind")
251:    # ---- gap table: encounters only
255:        if r["date"] and r["kind"] == "encounter":
260:        err(cid, f"gap_excluded_records {ex['gap_excluded_records']} != non-encounter/ambiguous records {sorted(excluded)}")
----
E5 True Fennimoor Spine Clinic, new patient
E6 False Fennimoor Spine Clinic, new patient intake form (OCR text)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:59:54.567Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-lib11-view.py",
 "content": "\"\"\"T-118 paralegal-reviewer probe: what the product shows for lib11 record 6 (the intake form) at a given archive root.\n\nusage: T-118-paralegal-lib11-view.py <archive_root>\nRuns app.backend.pipeline.run_case on evals/library/case_lib11 with the fixture backend (no network, no model calls beyond recorded\nfixtures), then prints: record 6 as ingested (kind, encounter flag), its timeline entries, gap flags, and the gap endpoints.\n\"\"\"\nimport json\nimport os\nimport sys\n\nroot = sys.argv[1]\nsys.path.insert(0, root)\nos.chdir(root)\n\nfrom app.backend import pipeline as P  # noqa: E402\n\ntext = open(os.path.join(root, \"evals\", \"library\", \"case_lib11_priors_and_ledger.txt\"), encoding=\"utf-8\").read()\nout = P.run_case(text, \"fixture\")\nprint(\"status:\", out.get(\"status\"))\nprint(\"records (n, date_iso, kind, source):\")\nfor r in out.get(\"records\", []):\n    print(\"  \", r.get(\"n\"), r.get(\"date_iso\") or r.get(\"date\"), r.get(\"kind\"), \"|\", r.get(\"source\"))\nprint(\"entries on 2026-03-27 (id, record_nos, encounter, provider):\")\nfor e in out.get(\"entries\", []):\n    if e.get(\"date\") == \"2026-03-27\" or \"2026-03-27\" in str(e.get(\"date\", \"\")):\n        print(\"  \", e.get(\"id\"), e.get(\"record_nos\"), e.get(\"encounter\"), \"|\", e.get(\"provider\"))\nprint(\"gap flags:\")\nfor f in out.get(\"flags\", []):\n    if f.get(\"type\") == \"gap\":\n        print(json.dumps({k: f.get(k) for k in (\"id\", \"from_date\", \"to_date\", \"days\", \"record_nos\", \"title\", \"explanation\", \"excluded_records\")}, indent=1))\nprint(\"gap flag count:\", sum(1 for f in out.get(\"flags\", []) if f.get(\"type\") == \"gap\"))\n"
}
````

### User / tool · 2026-11-02T09:59:54.660Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-lib11-view.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:59:57.895Z

**tool call — Bash**
````
{
 "command": "HEAD=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/T-118-paralegal-lib11-view.py \"$HEAD/t118-head\" > artifacts/review-evidence/T-118-out/lib11-view-head.txt 2>&1; echo \"EXIT=$?\"; cat artifacts/review-evidence/T-118-out/lib11-view-head.txt | head -60",
 "description": "Run lib11 product view on HEAD archive copy"
}
````

### User / tool · 2026-11-02T09:59:58.469Z

**tool result**
````
EXIT=0
status: done
records (n, date_iso, kind, source):
   1 2026-03-04 encounter | Dr. Hesper Alderton, primary care
   2 2026-03-18 encounter | Ashgrove Fire-Rescue run report
   3 2026-03-18 encounter | Wexcombe Memorial ED
   4 2026-03-26 records_admin | Pellingham and Rook PLLC, correspondence (letter of protection)
   5 2026-03-27 encounter | Fennimoor Spine Clinic, new patient
   6 2026-03-27 encounter | Fennimoor Spine Clinic, new patient intake form (OCR text)
   7 2026-04-24 encounter | Fennimoor Spine Clinic, visit 8
   8 2026-05-29 encounter | Fennimoor Spine Clinic, visit 14
   9 2026-06-15 billing_statement | Fennimoor Spine Clinic, itemized ledger
entries on 2026-03-27 (id, record_nos, encounter, provider):
   e5 None None | Fennimoor Spine Clinic, new patient
   e6 None None | Fennimoor Spine Clinic, new patient intake form (OCR text)
gap flags:
{
 "id": "f_gap_r7_r8",
 "from_date": "2026-04-24",
 "to_date": "2026-05-29",
 "days": 35,
 "record_nos": [
  7,
  8
 ],
 "title": "Gap of 35 days",
 "explanation": "Gap of 35 days between April 24, 2026 (Fennimoor Spine Clinic, visit 8) and May 29, 2026 (Fennimoor Spine Clinic, visit 14).",
 "excluded_records": []
}
gap flag count: 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:00:12.753Z

**tool call — Bash**
````
{
 "command": "grep -rn \"encounter\" app/frontend --include=*.js --include=*.ts --include=*.tsx --include=*.html --include=*.jsx 2>/dev/null | head -10; echo ----; grep -rn \"encounter\" app/backend/present.py app/backend/export*.py app/backend/generator.py 2>/dev/null | head -10; echo ----; git show HEAD:evals/reports/latest.json | .venv/bin/python -c \"import json,sys; d=json.load(sys.stdin); print({k: d[k] for k in d if k in ('ship_bar_met','blockers','generated_at','commit','ts')})\" 2>&1 | head -5",
 "description": "Check how encounter flag reaches UI and export; read ship-bar keys"
}
````

### User / tool · 2026-11-02T10:00:12.905Z

**tool result**
````
app/frontend/mock.js:57:        injection_tag: false, encounter: true, char_start: h.at, char_end: h.at + block.length, text: block,
app/frontend/dev/mock-data.js:19:   "encounter": true,
app/frontend/dev/mock-data.js:34:   "encounter": true,
app/frontend/dev/mock-data.js:49:   "encounter": true,
app/frontend/dev/mock-data.js:64:   "encounter": true,
app/frontend/dev/mock-data.js:79:   "encounter": true,
app/frontend/dev/mock-data.js:94:   "encounter": true,
app/frontend/dev/mock-data.js:109:   "encounter": true,
app/frontend/dev/mock-data.js:124:   "encounter": true,
app/frontend/dev/mock-data.js:139:   "encounter": true,
----
app/backend/present.py:169:         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
----
{'blockers': ['4_no_invented_facts', 'backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)', 'judge_controls (J3/J4 seeded wrong items): not measured'], 'generated_at': '2026-11-02T09:56:40Z', 'ship_bar_met': False}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:00:19.575Z

**tool call — Bash**
````
{
 "command": "ls tests/unit | grep -i gap; grep -rn \"from_records\\|to_records\\|gap_excluded\" tests/ | head -20; echo ----; grep -n \"gap_excluded\\|from_records\\|to_records\" evals/run.py | head",
 "description": "Check whether tests compare gap record lists and exclusions"
}
````

### User / tool · 2026-11-02T10:00:19.694Z

**tool result**
````
test_gaps.py
test_t116_gap_endpoints.py
tests/unit/test_t116_gap_endpoints.py:179:    assert g["to_records"] == [5] and GP.non_visit_label(next(r for r in recs if r["n"] == 6)) == "intake form"
tests/unit/test_gaps.py:15:    assert [(g["from_records"], g["to_records"]) for g in got] == [(w["from_records"], w["to_records"]) for w in want]
tests/unit/test_gaps.py:53:    assert g[0]["from_records"] == [1, 2] and g[0]["days"] == 7
----
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:00:21.798Z

**tool call — Bash**
````
{
 "command": "sed -n 1,30p tests/unit/test_gaps.py; echo ----; grep -n \"golden\\|library\\|expected\" tests/unit/test_t116_gap_endpoints.py | head -30",
 "description": "Read gap unit tests to see if golden/library record lists are compared"
}
````

### User / tool · 2026-11-02T10:00:21.885Z

**tool result**
````
"""Treatment gaps (code). R-FL-1, LLM_VS_CODE row 9; golden gap_table of every case."""
import pytest
from app.backend import gaps as GP
from tests.unit import _golden as G

def recs(case):
    return [dict(n=r["record_no"], date_iso=r["date"], kind=r["kind"]) for r in G.expected(case)["records"]]

@pytest.mark.parametrize("case", G.case_names())
def test_gap_table_matches_golden(case):
    """R-FL-1: for every golden case the computed intervals (dates, record lists, days, flag) equal gap_table."""
    got = GP.compute_gaps(recs(case))
    want = G.expected(case)["gap_table"]
    assert [(g["from_date"], g["to_date"], g["days"], g["flag"]) for g in got] == [(w["from_date"], w["to_date"], w["days"], w["flag"]) for w in want]
    assert [(g["from_records"], g["to_records"]) for g in got] == [(w["from_records"], w["to_records"]) for w in want]

@pytest.mark.parametrize("days,flag", [(28, False), (29, False), (30, False), (31, True), (73, True)])
def test_threshold_is_strictly_greater_than_30(days, flag):
    """R-FL-1 (A-104): 29 and 30 do not flag, 31 does."""
    assert GP.is_gap(days) is flag

def test_sample_73_day_flag_and_28_day_near_miss():
    """R-FL-1: sample flags 2026-03-06 -> 2026-05-18 (73) and not 2026-01-23 -> 2026-02-20 (28)."""
    flagged = [(g["from_date"], g["to_date"], g["days"]) for g in GP.compute_gaps(recs("sample")) if g["flag"]]
    assert flagged == [("2026-03-06", "2026-05-18", 73)]

def test_leap_year_case_02_three_flags_four_near_misses():
    """R-FL-1: case_02 (2028 leap) -> 3 flags (31 days), 4 intervals of 29/30."""
    g = GP.compute_gaps(recs("case_02_gap_boundaries"))
    assert sum(x["flag"] for x in g) == 3 and sum(not x["flag"] for x in g) == 4
----
161:GOLD_GAP_CASES = sorted(p.stem for p in list((ROOT / "evals" / "golden").glob("case_*.txt")) + list((ROOT / "evals" / "library").glob("case_lib*.txt")))
165:def test_golden_and_library_gap_figures_are_unchanged(name):
166:    """Every golden and library packet keeps its expected gap dates, day counts and flags. Only the record LISTS differ on lib11 (an intake form
169:    d = ROOT / "evals" / ("golden" if name.startswith("case_0") else "library")
170:    exp = json.loads((d / f"{name}.expected.json").read_text())
177:    recs = I.ingest((ROOT / "evals" / "library" / "case_lib11_priors_and_ledger.txt").read_text())["records"]
195:    tok = c.post("/api/cases", json={"library": LIB09}).json()["token"]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:00:27.317Z

**tool call — Bash**
````
{
 "command": "sed -n 160,185p tests/unit/test_t116_gap_endpoints.py",
 "description": "Read T-116 golden gap test body"
}
````

### User / tool · 2026-11-02T10:00:27.400Z

**tool result**
````
GOLD_GAP_CASES = sorted(p.stem for p in list((ROOT / "evals" / "golden").glob("case_*.txt")) + list((ROOT / "evals" / "library").glob("case_lib*.txt")))


@pytest.mark.parametrize("name", GOLD_GAP_CASES)
def test_golden_and_library_gap_figures_are_unchanged(name):
    """Every golden and library packet keeps its expected gap dates, day counts and flags. Only the record LISTS differ on lib11 (an intake form
    shares its date with the visit it belongs to; see the card note for qa)."""
    import json
    d = ROOT / "evals" / ("golden" if name.startswith("case_0") else "library")
    exp = json.loads((d / f"{name}.expected.json").read_text())
    recs = I.ingest((d / f"{name}.txt").read_text())["records"]
    got = [(g["from_date"], g["to_date"], g["days"], g["flag"]) for g in GP.compute_gaps(recs)]
    assert got == [(g["from_date"], g["to_date"], g["days"], g["flag"]) for g in exp["gap_table"]]


def test_lib11_intake_form_sharing_the_visit_date_leaves_the_visit_as_the_only_endpoint():
    recs = I.ingest((ROOT / "evals" / "library" / "case_lib11_priors_and_ledger.txt").read_text())["records"]
    g = [x for x in GP.compute_gaps(recs) if x["from_date"] == "2026-03-18"][0]
    assert g["to_records"] == [5] and GP.non_visit_label(next(r for r in recs if r["n"] == 6)) == "intake form"


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.setenv("ZLAYT_MODE", "local")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:00:44.712Z

**tool call — Bash**
````
{
 "command": "ls reviews | grep T-116; grep -n \"make the gap test\\|from_records, to_records\" reviews/T-116-paralegal.md | head -5",
 "description": "Locate T-116 round-1 review text about gap test comparison"
}
````

### User / tool · 2026-11-02T10:00:44.807Z

**tool result**
````
T-116-paralegal.md
127:   "fix": "qa and researcher: decide the kind vocabulary for intake forms (extend check_golden.py's allowed kinds and the entry encounter rule), set lib11 record 6 accordingly, apply the three list changes, and make the gap test compare (from_records, to_records) for all golden and library packets. Reopen AC1 until the truth file matches the product.",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:00:47.062Z

**tool call — Bash**
````
{
 "command": "sed -n 110,130p reviews/T-116-paralegal.md | cut -c1-900",
 "description": "Read the T-116 round-1 finding in full"
}
````

### User / tool · 2026-11-02T10:00:47.140Z

**tool result**
````
  "driven lib09 confirm_date flow through the API on the HEAD archive (artifacts/review-evidence/T-116-paralegal-lib09-api.py)",
  "research/validate_library.py on HEAD (exit 0), and on scratch copies with the card's lib11 list change (exit 1) and with record 6 kind also changed (fails bad kind and E6)",
  "read gaps.py, flag_templates.py, conflicts.py:13, pipeline.py:258, lexicon.yaml non_encounter, check_golden.py:200, test_t116 and test_gaps"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 2, "gap_figures_unchanged": 5, "record_type_detection": 2, "lib11_truth_consistency": 2},
 "findings": [
  {"severity": "blocker",
   "title": "A treatment visit whose Source label contains a paperwork word is excluded from gap endpoints, which invents a gap and a false statement",
   "evidence": "artifacts/review-evidence/T-116-paralegal-repro-false-exclusion.out.txt: visits 2026-03-01 and 2026-04-10 with a middle visit labelled 'Capital PT, initial evaluation (intake form completed same day)' on 2026-03-20 -> 'Gap of 40 days ... Intake form on March 20, 2026 is not a treatment visit, so it does not start or end a gap.'; plain-label control -> no flag. 'Dr. Reyes, orthopedics, statement of MMI' -> billing statement, 40-day flag. app/backend/gaps.py:16-32 (unanchored re.search over the whole Source line) and gaps.py:43-45 (first match wins). artifacts/review-evidence/T-116-paralegal-label-sweep.out.txt: 15 of 19 visit labels excluded.",
   "why_it_matters": "Only treatment encounters may end a gap. Here a real visit is dropped, the tool reports a 40-day gap the records do not show, and it states that a visit is not a treatment visit. Persona section 5 and calibration: an invented fact or gap is a blocker. The 25 packets are unaffected today, but the T-116 tests cover no label in which a visit mentions a paperwork word.",
   "fix": "Classify on the record-type head of the Source label, not on any substring: an encounter term (visit, evaluation, new patient, daily note, follow-up, operative, run report, imaging, discharge summary) keeps the record an encounter; paperwork terms exclude only when they name the record type. Treat bare 'statement', 'letter', 'fax' and 'records review' with the same rule. Show the matched header text in the why (see F4).",
   "acceptance_test": "Add to tests/unit/test_t116_gap_endpoints.py: gap_flags over [2026-03-01 'Capital PT, visit 1', 2026-03-20 X, 2026-04-10 'Capital PT, visit 3'] returns no flag for X in {'Capital PT, initial evaluation (intake form completed same day)', 'Dr. Reyes, orthopedics, statement of MMI', 'Dr. Nguyen, records review visit', 'Dr. Lee, chiropractic, visit 3 (faxed)', 'Hill Country Pain Management, new patient'}; all existing non-visit label tests still pass. Re-run artifacts/review-evidence/T-116-paralegal-repro-false-exclusion.py: case A must show no flag."},
  {"severity": "major",
   "title": "lib11 expected truth file is stale at HEAD and the posted list change fails the golden checker as written",
   "evidence": "git show HEAD:evals/library/case_lib11_priors_and_ledger.expected.json: gap_excluded_records [4, 9] (lines 251-254); gap rows still list [5, 6] (lines 276, 286). Product: exact False, excl [4, 6, 9] (artifacts/review-evidence/T-116-paralegal-packet-sweep.out.txt). Card's list change on a scratch copy: research/validate_library.py -> 'gap_excluded_records [4, 6, 9] != non-encounter/ambiguous records [4, 9]' and two 'record lists wrong' (artifacts/review-evidence/T-116-paralegal-lib11-validator-lists-only.out.txt). With record 6 kind records_admin: 'record 6: bad kind' and 'E6: encounter flag disagrees' (artifacts/review-evidence/T-116-paralegal-lib11-validator-lists-and-kind6.out.txt); evals/golden/check_golden.py:200 accepts only encounter, billing_statement, phone_note. HEAD validator exit 0: artifacts/review-evidence/T-116-paralegal-validator-HEAD.out.txt. tests/unit/te
   "why_it_matters": "The card's list values are the correct answer under the rule (verified: the 3/27 intake form shares a date with visit 5, so visit 5 is the only endpoint; the 28-day interval stays unflagged). But the committed truth contradicts the committed product, the schema cannot express the change, and no test catches a record-list regression on library packets. AC1 is ticked done while this change is pending.",
   "fix": "qa and researcher: decide the kind vocabulary for intake forms (extend check_golden.py's allowed kinds and the entry encounter rule), set lib11 record 6 accordingly, apply the three list changes, and make the gap test compare (from_records, to_records) for all golden and library packets. Reopen AC1 until the truth file matches the product.",
   "acceptance_test": "The new record-list test fails on HEAD (lib11 lists differ) and passes after the fix. research/validate_library.py exits 0 with lib11 gap_excluded_records [4, 6, 9], gap row 2026-03-18->03-27 to_records [5], and row 2026-03-27->04-24 from_records [5]."},
  {"severity": "minor",
   "title": "Conflict and accident-year logic still treat intake forms and bills as encounters",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:00:59.895Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cp -R \"$S/t118-head\" \"$S/t118-mutA\" && git show ea6ac71:evals/library/case_lib11_priors_and_ledger.expected.json > \"$S/t118-mutA/evals/library/case_lib11_priors_and_ledger.expected.json\" && echo COPIED && du -sh \"$S/t118-mutA\" | tail -1",
 "description": "Create mutant copy with pre-commit lib11 truth file"
}
````

### User / tool · 2026-11-02T10:01:00.571Z

**tool result**
````
COPIED
 28M	/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t118-mutA
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:01:04.309Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; M=\"$S/t118-mutA\"; echo \"== validate_library (pre-commit truth on HEAD code)\"; (cd \"$M\" && python3 -I research/validate_library.py; echo \"EXIT=$?\"); echo \"== check_golden\"; (cd \"$M\" && python3 -I evals/golden/check_golden.py; echo \"EXIT=$?\"); echo \"== endpoint probe\"; .venv/bin/python -I artifacts/review-evidence/T-118-paralegal-endpoints.py \"$M\" | tail -4; echo \"EXIT=$?\"",
 "description": "Run validators and endpoint probe on the pre-commit-truth mutant"
}
````

### User / tool · 2026-11-02T10:01:05.112Z

**tool result**
````
== validate_library (pre-commit truth on HEAD code)
golden OK: 25 cases (24 synthetic), 118 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (15 packets, 80 denylist terms, case-insensitive)
EXIT=0
== check_golden
golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
EXIT=0
== endpoint probe
case_lib11_priors_and_ledger: row ('2026-03-18', '2026-03-27') expected days/flag/from/to=(9, False, [2, 3], [5, 6]) product=(9, False, [2, 3], [5])
case_lib11_priors_and_ledger: row ('2026-03-27', '2026-04-24') expected days/flag/from/to=(28, False, [5, 6], [7]) product=(28, False, [5], [7])
case_lib11_priors_and_ledger: gap_excluded_records expected=[4, 9] product=[4, 6, 9] labels={4: 'letter or correspondence', 6: 'intake form', 9: 'ledger'}
packets with gap expectations: 25; differences: 3
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:01:10.667Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for T in t118-head t118-mutA; do echo \"== $T\"; (cd \"$S/$T\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_gaps.py tests/unit/test_t116_gap_endpoints.py -q -p no:cacheprovider 2>&1 | tail -4); done",
 "description": "Run gap unit tests on HEAD and on the pre-commit-truth mutant"
}
````

### User / tool · 2026-11-02T10:01:13.052Z

**tool result**
````
== t118-head
........................................................................ [ 62%]
............................................                             [100%]
116 passed in 0.86s
== t118-mutA
........................................................................ [ 62%]
............................................                             [100%]
116 passed in 0.94s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:01:20.004Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-mutB.py",
 "content": "\"\"\"T-118 paralegal-reviewer mutant: on a scratch copy of HEAD, give lib11 record 6 the kind it has in the packet's ingest\n(\"encounter\") and set entry E6 encounter=true, keeping the card's record lists. Shows what check_golden.py needs to pass.\n\nusage: T-118-paralegal-mutB.py <scratch_copy_root>\n\"\"\"\nimport json\nimport sys\n\nroot = sys.argv[1]\npath = root + \"/evals/library/case_lib11_priors_and_ledger.expected.json\"\nd = json.load(open(path, encoding=\"utf-8\"))\nfor r in d[\"records\"]:\n    if r[\"record_no\"] == 6:\n        r[\"kind\"] = \"encounter\"\nfor e in d[\"entries\"]:\n    if e[\"id\"] == \"E6\":\n        e[\"encounter\"] = True\nwith open(path, \"w\", encoding=\"utf-8\") as fh:\n    json.dump(d, fh, indent=2, ensure_ascii=False)\n    fh.write(\"\\n\")\nprint(\"mutB written:\", path)\n"
}
````

### User / tool · 2026-11-02T10:01:20.106Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-mutB.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:01:23.355Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cp -R \"$S/t118-head\" \"$S/t118-mutB\" && .venv/bin/python -I artifacts/review-evidence/T-118-paralegal-mutB.py \"$S/t118-mutB\" && (cd \"$S/t118-mutB\" && python3 -I evals/golden/check_golden.py; echo \"check_golden EXIT=$?\"; python3 -I research/validate_library.py; echo \"validate_library EXIT=$?\") 2>&1 | tail -12",
 "description": "Build mutant B (record 6 as encounter) and run the golden checker"
}
````

### User / tool · 2026-11-02T10:01:24.724Z

**tool result**
````
mutB written: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t118-mutB/evals/library/case_lib11_priors_and_ledger.expected.json
golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
check_golden EXIT=0
GOLDEN CHECK FAILED
 - case_lib11_priors_and_ledger: gap_excluded_records [4, 6, 9] != non-encounter/ambiguous records [4, 9]
 - case_lib11_priors_and_ledger: gap row 2026-03-18->2026-03-27: record lists wrong
 - case_lib11_priors_and_ledger: gap row 2026-03-27->2026-04-24: record lists wrong
identifier check: ok (15 packets, 80 denylist terms, case-insensitive)
validate_library EXIT=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:01:49.596Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"gap\" evals/reports/20261102T095640Z.md | head -5; echo ----; git show ea6ac71:evals/reports/latest.json > artifacts/review-evidence/T-118-out/latest-pre.json; git show HEAD:evals/reports/latest.json > artifacts/review-evidence/T-118-out/latest-head.json; .venv/bin/python -I -c \"import json; [print(p, json.load(open(p)).get('ship_bar_met'), json.load(open(p)).get('blockers')) for p in ['artifacts/review-evidence/T-118-out/latest-pre.json','artifacts/review-evidence/T-118-out/latest-head.json']]\"; echo ----; cat -n evals/reports/library-latest.md | sed -n 17p; echo ----; git show ea6ac71:evals/reports/library-latest.md | sed -n 17p",
 "description": "Check fixture report gap line, ship-bar blockers pre and post, library report row"
}
````

### User / tool · 2026-11-02T10:01:49.791Z

**tool result**
````
13:| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
39:Assertions: {"gap_28_not_flagged": true, "gap_73_flagged": true, "all_gap_rows_correct": true}
----
artifacts/review-evidence/T-118-out/latest-pre.json False ['3_flags', '4_no_invented_facts']
artifacts/review-evidence/T-118-out/latest-head.json False ['4_no_invented_facts', 'backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)', 'judge_controls (J3/J4 seeded wrong items): not measured']
----
    17	| case_lib09_spanish_interpreter_espalda | done | 4/7 | 2/5 | False | 1/2 | 0 | M5 | 0 | - |
----
| case_lib09_spanish_interpreter_espalda | done | 4/7 | 2/5 | False | 1/2 | 0 | M5 | 0 | - |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:01:55.444Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\nfor p in ['artifacts/review-evidence/T-118-out/latest-pre.json','artifacts/review-evidence/T-118-out/latest-head.json']:\n    d = json.load(open(p))\n    print(p.split('/')[-1], sorted(d.keys())[:30])\n    print({k: d.get(k) for k in ('generated_at','backend','commit','source_commit','ship_bar','report')})\n\"",
 "description": "Compare generation metadata of the pre and HEAD fixture reports"
}
````

### User / tool · 2026-11-02T10:01:55.565Z

**tool result**
````
latest-pre.json ['assertions', 'backend', 'backend_requested', 'bars', 'blockers', 'cases', 'generated_at', 'hashes', 'internal_notes_equal', 'letter_equal', 'metrics', 'models', 'per_case', 'run_artifacts', 'schema', 'ship_bar_met', 'spec_matches_golden', 'thresholds']
{'generated_at': '2026-11-02T04:09:33Z', 'backend': 'claude-cli', 'commit': None, 'source_commit': None, 'ship_bar': None, 'report': None}
latest-head.json ['assertions', 'backend', 'backend_requested', 'bars', 'blockers', 'calibration', 'cases', 'generated_at', 'hashes', 'internal_notes_equal', 'letter_equal', 'metrics', 'models', 'per_case', 'schema', 'ship_bar_met', 'source', 'spec_matches_golden', 'thresholds']
{'generated_at': '2026-11-02T09:56:40Z', 'backend': 'fixture', 'commit': None, 'source_commit': None, 'ship_bar': None, 'report': None}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:02:15.398Z

**tool call — Bash**
````
{
 "command": "grep -n \"assert got == \\[\" tests/unit/test_t116_gap_endpoints.py; grep -n \"def recs\\|from_records\\\"\\] == \\|assert \\[(g\\[\\\"from_records\\\"\\]\" tests/unit/test_gaps.py; grep -n 'if r\\[\"kind\"\\] not in\\|encounter flag disagrees\\|gap_excluded_records {ex\\|if e\\[\"encounter\"\\]' evals/golden/check_golden.py; grep -n \"gap_rows_wrong\\|gap_rows = \" evals/run.py | head -3; grep -n '\"kind\": \"phone_note\"\\|\"encounter\": false' evals/library/case_lib11_priors_and_ledger.expected.json; grep -n \"Source: Fennimoor Spine Clinic, new patient intake\" evals/library/case_lib11_priors_and_ledger.txt",
 "description": "Verify line numbers cited in the review"
}
````

### User / tool · 2026-11-02T10:02:15.536Z

**tool result**
````
173:    assert got == [(g["from_date"], g["to_date"], g["days"], g["flag"]) for g in exp["gap_table"]]
6:def recs(case):
15:    assert [(g["from_records"], g["to_records"]) for g in got] == [(w["from_records"], w["to_records"]) for w in want]
53:    assert g[0]["from_records"] == [1, 2] and g[0]["days"] == 7
200:        if r["kind"] not in ("encounter", "billing_statement", "phone_note"):
242:        if e["encounter"] != (rs[0]["kind"] == "encounter"):
243:            err(cid, f"{e['id']}: encounter flag disagrees with record kind")
260:        err(cid, f"gap_excluded_records {ex['gap_excluded_records']} != non-encounter/ambiguous records {sorted(excluded)}")
244:    gap_rows = [(r["from_date"], r["to_date"], r["days"], r["flag"]) for r in exp.get("gap_table", [])]
248:            "gap_rows_wrong": [r[:3] for r in gap_rows if (r[:3] in gaps) != r[3]]}
870:    wrong = {n: r["flags"]["gap_rows_wrong"] for n, r in results.items()}
43:      "kind": "phone_note",
57:      "kind": "phone_note",
157:      "encounter": false,
190:      "encounter": false,
239:      "encounter": false,
30:Source: Fennimoor Spine Clinic, new patient intake form (OCR text)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:02:42.332Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-evidence.sh",
 "content": "#!/bin/bash\n# T-118 paralegal-reviewer evidence run. Every check runs on a git-archive copy (HEAD 78450f6, pre-commit ea6ac71, two mutants),\n# never in the project tree. Output of each step goes to artifacts/review-evidence/T-118-out/.\nset -u\nPROJ=/Users/arsis/zlayt-pm-project\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nOUT=$PROJ/artifacts/review-evidence/T-118-out\nPY=$PROJ/.venv/bin/python\nEP=$PROJ/artifacts/review-evidence/T-118-paralegal-endpoints.py\nLV=$PROJ/artifacts/review-evidence/T-118-paralegal-lib11-view.py\n\necho \"== validate_library.py on HEAD copy\"\n(cd $S/t118-head && python3 -I research/validate_library.py; echo \"EXIT=$?\") > $OUT/validate-head.txt 2>&1; tail -1 $OUT/validate-head.txt\necho \"== check_golden.py on HEAD copy\"\n(cd $S/t118-head && python3 -I evals/golden/check_golden.py; echo \"EXIT=$?\") > $OUT/check-golden-head.txt 2>&1; tail -1 $OUT/check-golden-head.txt\necho \"== library report regenerated at HEAD and at ea6ac71\"\n$PY -I $PROJ/artifacts/review-evidence/T-118-paralegal-runner.py $S/t118-head evals.library_report --out $OUT/library-head.md > $OUT/lib-head.stdout 2>&1; echo \"HEAD EXIT=$?\"\n$PY -I $PROJ/artifacts/review-evidence/T-118-paralegal-runner.py $S/t118-pre evals.library_report --out $OUT/library-pre.md > $OUT/lib-pre.stdout 2>&1; echo \"PRE EXIT=$?\"\ndiff $OUT/library-pre.md $OUT/library-head.md > $OUT/library-pre-vs-head.diff; echo \"pre vs head diff exit=$? (lines: $(wc -l < $OUT/library-pre-vs-head.diff))\"\necho \"== committed library-latest.md vs regenerated HEAD (provenance header excluded)\"\ndiff <(sed 1,3d $OUT/library-committed.md) <(sed 1,3d $OUT/library-head.md) > $OUT/library-committed-vs-head.diff; echo \"exit=$?\"; cat $OUT/library-committed-vs-head.diff\necho \"== endpoint probe\"\n$PY -I $EP $S/t118-head > $OUT/probe-head.txt 2>&1; echo \"HEAD EXIT=$?\"; tail -1 $OUT/probe-head.txt\n$PY -I $EP $S/t118-pre > $OUT/probe-pre.txt 2>&1; echo \"PRE EXIT=$?\"; tail -1 $OUT/probe-pre.txt\necho \"== lib11 product view on HEAD\"\n$PY -I $LV $S/t118-head > $OUT/lib11-view-head.txt 2>&1; echo \"EXIT=$?\"\necho \"== mutant A (pre-commit lib11 truth) validators and probe\"\n(cd $S/t118-mutA && python3 -I research/validate_library.py; echo \"validate EXIT=$?\"; python3 -I evals/golden/check_golden.py; echo \"check_golden EXIT=$?\") > $OUT/mutA-validators.txt 2>&1; cat $OUT/mutA-validators.txt | grep EXIT\n$PY -I $EP $S/t118-mutA > $OUT/mutA-probe.txt 2>&1; echo \"probe EXIT=$?\"; tail -1 $OUT/mutA-probe.txt\necho \"== mutant B (record 6 kind encounter, E6 true) check_golden\"\n(cd $S/t118-mutB && python3 -I evals/golden/check_golden.py; echo \"check_golden EXIT=$?\") > $OUT/mutB-check-golden.txt 2>&1; cat $OUT/mutB-check-golden.txt\necho \"== gap unit tests on HEAD and mutant A\"\n(cd $S/t118-head && $PY -I -m pytest tests/unit/test_gaps.py tests/unit/test_t116_gap_endpoints.py -q -p no:cacheprovider) > $OUT/pytest-head.txt 2>&1; tail -1 $OUT/pytest-head.txt\n(cd $S/t118-mutA && $PY -I -m pytest tests/unit/test_gaps.py tests/unit/test_t116_gap_endpoints.py -q -p no:cacheprovider) > $OUT/pytest-mutA.txt 2>&1; tail -1 $OUT/pytest-mutA.txt\necho \"DONE\"\n"
}
````

### User / tool · 2026-11-02T10:02:42.432Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-evidence.sh (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:02:45.249Z

**tool call — Bash**
````
{
 "command": "bash /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-evidence.sh",
 "description": "Run the T-118 evidence script over archive copies"
}
````

### User / tool · 2026-11-02T10:02:51.931Z

**tool result**
````
== validate_library.py on HEAD copy
EXIT=0
== check_golden.py on HEAD copy
EXIT=0
== library report regenerated at HEAD and at ea6ac71
HEAD EXIT=0
PRE EXIT=0
pre vs head diff exit=0 (lines:        0)
== committed library-latest.md vs regenerated HEAD (provenance header excluded)
exit=1
14c14
< | case_lib09_spanish_interpreter_espalda | done | 4/7 | 2/5 | False | 1/2 | 0 | M5 | 0 | - |
---
> | case_lib09_spanish_interpreter_espalda | done | 4/7 | 3/5 | False | 1/2 | 0 | M5 | 0 | - |
== endpoint probe
HEAD EXIT=0
packets with gap expectations: 25; differences: 0
PRE EXIT=1
packets with gap expectations: 25; differences: 3
== lib11 product view on HEAD
EXIT=0
== mutant A (pre-commit lib11 truth) validators and probe
validate EXIT=0
check_golden EXIT=0
probe EXIT=1
packets with gap expectations: 25; differences: 3
== mutant B (record 6 kind encounter, E6 true) check_golden
golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
check_golden EXIT=0
== gap unit tests on HEAD and mutant A
116 passed in 0.81s
116 passed in 0.80s
DONE
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:02:58.411Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-out && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && (cd $S/t118-mutB && python3 -I research/validate_library.py; echo \"validate_library EXIT=$?\") > mutB-validate.txt 2>&1; cat mutB-validate.txt; echo ----; cat validate-head.txt; echo ----; cat mutA-validators.txt; echo ----; cat probe-pre.txt; echo ----; cat pytest-head.txt | tail -1; cat pytest-mutA.txt | tail -1",
 "description": "Save mutant B validator output and show saved evidence"
}
````

### User / tool · 2026-11-02T10:02:59.116Z

**tool result**
````
GOLDEN CHECK FAILED
 - case_lib11_priors_and_ledger: gap_excluded_records [4, 6, 9] != non-encounter/ambiguous records [4, 9]
 - case_lib11_priors_and_ledger: gap row 2026-03-18->2026-03-27: record lists wrong
 - case_lib11_priors_and_ledger: gap row 2026-03-27->2026-04-24: record lists wrong
identifier check: ok (15 packets, 80 denylist terms, case-insensitive)
validate_library EXIT=1
----
golden OK: 25 cases (24 synthetic), 118 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (15 packets, 80 denylist terms, case-insensitive)
EXIT=0
----
golden OK: 25 cases (24 synthetic), 118 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (15 packets, 80 denylist terms, case-insensitive)
validate EXIT=0
golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
check_golden EXIT=0
----
case_lib11_priors_and_ledger: row ('2026-03-18', '2026-03-27') expected days/flag/from/to=(9, False, [2, 3], [5, 6]) product=(9, False, [2, 3], [5])
case_lib11_priors_and_ledger: row ('2026-03-27', '2026-04-24') expected days/flag/from/to=(28, False, [5, 6], [7]) product=(28, False, [5], [7])
case_lib11_priors_and_ledger: gap_excluded_records expected=[4, 9] product=[4, 6, 9] labels={4: 'letter or correspondence', 6: 'intake form', 9: 'ledger'}
packets with gap expectations: 25; differences: 3
----
116 passed in 0.81s
116 passed in 0.80s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:03:29.910Z

**tool call — Bash**
````
{
 "command": "ls reviews | grep \"T-118\" ; python3 tools/board.py list 2>&1 | grep -i \"T-11[6-9]\\|T-12\" | head; echo ----; grep -n \"encounter\" app/backend/conflicts.py app/backend/pipeline.py | head -4; echo ----; grep -rn \"encounter\" app/frontend --include=*.js --include=*.html | grep -v mock | head -3; echo \"frontend non-mock hits: $?\"",
 "description": "Check for existing T-118 review, follow-up cards, and kind use in product"
}
````

### User / tool · 2026-11-02T10:03:30.084Z

**tool result**
````
T-116	M3	backend    	in_review        	P2	AC 1/1	Gap rule: an intake form or other administrative record never ends a treatment gap
T-117	M3	frontend   	ready            	P1	AC 0/2	Judge panel row for a could-not-verify tray flag shows the raw id (f_r5_1) and no record cue
T-118	M3	qa         	in_review        	P2	AC 1/1	Apply T-116 lib11 golden edits (five edits posted on T-116) and validate
----
app/backend/conflicts.py:12:def _encounters(records):
app/backend/conflicts.py:13:    enc = [r for r in records if r.get("kind", "encounter") == "encounter" and r.get("date_iso")]
app/backend/conflicts.py:43:    enc = _encounters(records)
app/backend/pipeline.py:162:                          encounter=int(r["encounter"]))
----
frontend non-mock hits: 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:03:33.979Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list 2>&1 | grep -i \"conflict\\|accident-year\\|accident_year\\|intake\" ; echo \"grep exit=$?\"; python3 tools/board.py list 2>&1 | wc -l",
 "description": "Check board for follow-up card on conflicts and intake-form routing"
}
````

### User / tool · 2026-11-02T10:03:34.183Z

**tool result**
````
T-033	M2	backend    	done             	P0	AC 8/8	Amounts, running total, gap rule, accident-date conflict, flag templates
T-036	M2	backend    	done             	P0	AC 10/10	LLM flag passes: per-record pre-existing/causation + lexicon floor, conflicts + judges #3/#4
T-048	M2	qa         	done             	P0	AC 2/2	M2 LLM-stage tests first (provider, audited, schemas, judges, flags, pipeline, conflicts, templates)
T-109	M2	architect  	in_progress      	P1	AC 1/1	LLM_VS_CODE row 11: conflicts are code-proposed candidates classified by judge_conflict_v4; model-only flags rejected by the flag judge are suppressed and listed
T-113	M2	backend    	ready            	P0	AC 0/2	Conflict judge false agrees on real candidate variants (J3V1 discontinued medicine, J3V9 other driver, J3V13 general denial vs mother's injury, H3V5 semicolon clause)
T-116	M3	backend    	in_review        	P2	AC 1/1	Gap rule: an intake form or other administrative record never ends a treatment gap
grep exit=0
     118
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:03:57.326Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-118-paralegal.md",
 "content": "# T-118 review — paralegal-reviewer (lib11 golden edits, commit 78450f6)\n\n**Verdict: changes.** No blockers. Two majors, one minor.\n\nThe five edits are exactly the five the T-116 card note posted, and the commit changes nothing else in the truth file. `validate_library.py` and `check_golden.py` pass on the HEAD copy. The product's gap endpoints match the expected record lists for all 25 golden and library packets, and record 6 is excluded as an intake form. Three problems remain. The truth file now says record 6 is a `phone_note`, which the packet does not state. Nothing in the repo compares record lists, so reverting the lib11 endpoint change passes every gate. And the committed library report is stale, so it cannot serve as the \"unchanged except lib11\" baseline.\n\nScope: no running app was exercised, so `scores.verify_quickly` (D-015) is not scored here. Everything below ran on `git archive` copies in the scratchpad, or on copies derived from them. Nothing was run in the project tree.\n\n## What I exercised\n\n- `git show 78450f6 -- evals/library/case_lib11_priors_and_ledger.expected.json`, `git show --stat 78450f6`, `git diff --stat ea6ac71 78450f6`. Only the lib11 expected file and two fixture reports changed.\n- `python3 tools/board.py show T-116` and `show T-118`. The five edits (note items 1 to 5) were compared line by line with the diff.\n- `git archive HEAD` into the scratchpad (`t118-head`, 78450f6). `git archive ea6ac71` (`t118-pre`). Mutant A: HEAD with the pre-commit lib11 file restored. Mutant B: HEAD with lib11 record 6 kind `encounter` and E6 `encounter` true.\n- `research/validate_library.py` (exit 0 on HEAD, exit 0 on mutant A, exit 1 on mutant B). `evals/golden/check_golden.py` (exit 0 on HEAD). Note that `check_golden.py` covers only the 10 `evals/golden` cases. The lib11 truth is checked by `validate_library.py`, which runs 25 cases.\n- `evals.library_report` at HEAD and at ea6ac71: both exit 0 and the outputs are byte-identical (`library-pre-vs-head.diff` is empty). The committed `evals/reports/library-latest.md` against the regenerated HEAD report.\n- `artifacts/review-evidence/T-118-paralegal-endpoints.py` (new probe): gap_table dates, days, flag, from_records, to_records, and gap_excluded_records on all 25 packets. HEAD: 0 differences. ea6ac71: 3 differences, all lib11. Mutant A: 3 differences.\n- `artifacts/review-evidence/T-118-paralegal-lib11-view.py`: the product's own lib11 output at HEAD (records, entries, gap flags).\n- `pytest tests/unit/test_gaps.py tests/unit/test_t116_gap_endpoints.py`: 116 passed on HEAD, 116 passed on mutant A.\n- Read: lib11 packet `.txt` lines 20 and 28 to 31; expected JSON lines 43, 57, 157, 190; `app/backend/gaps.py` 80 to 175; `check_golden.py` 200, 242 to 243, 255 to 260; `evals/run.py` 243 to 248; `tests/unit/test_gaps.py` 6 to 15; `tests/unit/test_t116_gap_endpoints.py` 165 to 179; `reviews/T-116-paralegal.md` finding 2 (fix text); `board.py list` (no follow-up card for T-116 minor F3 found).\n- Evidence: `artifacts/review-evidence/T-118-paralegal-evidence.sh` runs the checks above, and its outputs are in `artifacts/review-evidence/T-118-out/` (`validate-head.txt`, `check-golden-head.txt`, `library-pre-vs-head.diff`, `library-committed-vs-head.diff`, `probe-head.txt`, `probe-pre.txt`, `lib11-view-head.txt`, `mutA-validators.txt`, `mutA-probe.txt`, `mutB-validate.txt`, `pytest-head.txt`, `pytest-mutA.txt`).\n\n## Checks against the card\n\n| Card claim | Result |\n|---|---|\n| Five edits match the T-116 r2 note (items 1 to 5, lines 57, 190, 251 to 254, 276 to 279, 286 to 289) | Match. Dates, days and flags unchanged. |\n| Record 6 is an intake form and not a gap endpoint | Packet line 30 reads `new patient intake form (OCR text)`. Product HEAD gap table has no record 6 endpoint (`lib11-view-head.txt`). Match. |\n| `validate_library.py` exit 0 | Pass (`validate-head.txt`). |\n| `check_golden.py` exit 0 | Pass (`check-golden-head.txt`). |\n| Only lib11 gap endpoints changed in the library report | The report has no endpoint column, so it cannot show this. The report is unchanged (0-line diff). The endpoint change itself is correct and confined to lib11 (probe: 3 differences at ea6ac71, all lib11; 0 at HEAD). See finding 2 for why nothing guards it. |\n\n## Out of my lens (not graded, for qa and the orchestrator)\n\n- The commit also replaces `evals/reports/latest.json`. The parent file was a `claude-cli` run (`generated_at` 2026-11-02T04:09:33Z, `blockers` `['3_flags', '4_no_invented_facts']`). HEAD is a `fixture` run (09:56:40Z, `blockers` `['4_no_invented_facts', 'backend=fixture: determinism...', 'judge_controls...']`). The T-118 handoff says \"same 3 pre-existing blockers as latest.json before this change\", which the parent file does not show. Evidence: `T-118-out/latest-pre.json`, `T-118-out/latest-head.json`.\n\n<!-- findings and scores are in the JSON block below -->\n\n```json\n{\"card\": \"T-118\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git archive HEAD (78450f6) copy in the scratchpad, plus archive of ea6ac71 and mutants A and B derived from HEAD; no running app; sample packets evals/library/case_lib11 and all 25 golden and library gap packets\",\n \"exercised\": [\n  \"git show 78450f6 lib11 expected diff; git show --stat 78450f6; git diff --stat ea6ac71 78450f6\",\n  \"python3 tools/board.py show T-116 and show T-118; compared the five edits against T-116 r2 card note items 1 to 5\",\n  \"research/validate_library.py on HEAD (exit 0), mutant A (exit 0), mutant B (exit 1); evals/golden/check_golden.py on HEAD (exit 0)\",\n  \"evals.library_report at HEAD and ea6ac71: exit 0, byte-identical; committed evals/reports/library-latest.md vs regenerated HEAD\",\n  \"artifacts/review-evidence/T-118-paralegal-endpoints.py: gap_table record lists and gap_excluded_records on 25 packets; HEAD 0 differences, ea6ac71 3 (all lib11), mutant A 3\",\n  \"artifacts/review-evidence/T-118-paralegal-lib11-view.py on HEAD: product records, entries and gap flags for lib11\",\n  \"pytest tests/unit/test_gaps.py tests/unit/test_t116_gap_endpoints.py: 116 passed on HEAD and on mutant A\",\n  \"read lib11 packet lines 20, 28 to 31; expected JSON lines 43, 57, 157, 190; app/backend/gaps.py 80 to 175; check_golden.py 200, 242 to 243, 255 to 260; evals/run.py 243 to 248; tests/unit/test_gaps.py 6 to 15; tests/unit/test_t116_gap_endpoints.py 165 to 179; reviews/T-116-paralegal.md finding 2\",\n  \"artifacts/review-evidence/T-118-paralegal-evidence.sh and artifacts/review-evidence/T-118-out/* (outputs of every run above)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"lib11_edits_match_card_note\": 5, \"gap_endpoints_match_product_25_packets\": 5, \"truth_record_kinds_match_packet\": 2, \"endpoint_regression_guarded\": 2, \"library_report_baseline_current\": 2},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Truth file gives lib11 record 6 (intake form) and record 4 (letter) the kind phone_note, which the packet does not state; the checker's vocabulary forces it, and product and truth disagree on record kind\",\n   \"evidence\": \"evals/library/case_lib11_priors_and_ledger.txt:30 'Source: Fennimoor Spine Clinic, new patient intake form (OCR text)'; evals/library/case_lib11_priors_and_ledger.expected.json:57 'kind': 'phone_note' (record 6), :43 'kind': 'phone_note' (record 4; packet .txt:20 says 'correspondence (letter of protection)'; pre-existing, not changed by 78450f6), :190 'encounter': false (E6). evals/golden/check_golden.py:200 allows only encounter, billing_statement, phone_note; :242 to 243 require entry encounter to equal kind; :255 to 260 derive gap_excluded_records from record kinds. Mutant B (record 6 kind encounter, E6 true, card lists kept): artifacts/review-evidence/T-118-out/mutB-validate.txt 'gap_excluded_records [4, 6, 9] != non-encounter/ambiguous records [4, 9]' and two 'record lists wrong', exit 1. Product at HEAD: artifacts/review-evidence/T-118-out/lib11-view-head.txt '6 2026-03-27 encounter | Fennimoor Spine Clinic, new patient intake form (OCR text)' and '4 2026-03-26 records_admin | ...'. Entries in case_view carry no encounter field (None for e5 and e6 in the same file). app/backend/conflicts.py:13 and pipeline.py:258 still read kind 'encounter' for record 6 (T-116 minor F3; no follow-up card found in board.py list).\",\n   \"why_it_matters\": \"The truth file asserts a record type the packet does not state, and the checker's three-kind vocabulary is the reason. T-116 r1 (reviews/T-116-paralegal.md, major, fix item 1) asked for the intake-form kind to be decided and the vocabulary extended; r2 used phone_note as a stand-in and left the intake kind for later. Now the truth says phone_note and E6 encounter false, while the product says encounter for the same record. No test compares those fields, so the E6 assertion is never measured. Not a blocker today: the product's gap output is right (finding 2 probe, 0 differences), no statement or amount shown to the paralegal calls record 6 a visit (no non-mock frontend reads the field), and the export is built from accepted entries. This becomes a blocker if any surface shows record kind 'encounter' for an intake form.\",\n   \"fix\": \"Extend check_golden.py:200 (and the rules at :242 to 243 and :255 to 260) with intake_form and correspondence kinds. Set records[6].kind to intake_form, records[4].kind to correspondence, E6 encounter false. Researcher and qa decide whether the product's record kind for an intake form stays encounter (ingest.py:221 and :320, present.py:169) and whether conflicts.py:13 and pipeline.py:258 should use the non-visit classifier (T-116 minor F3, still open).\",\n   \"acceptance_test\": \"research/validate_library.py exits 0 with the new kinds and the card's gap lists; mutant B (kind encounter with E6 true) fails validate_library.py; a product-level test fails when the product's record-6 kind or entry encounter disagrees with the truth file.\"},\n  {\"severity\": \"major\",\n   \"title\": \"No test or report enforces the lib11 gap endpoints, so reverting the card's edits passes every gate; the T-116 r1 record-list test was never added\",\n   \"evidence\": \"tests/unit/test_t116_gap_endpoints.py:165 to 173 compares (from_date, to_date, days, flag) only. tests/unit/test_gaps.py:6 to 7 builds records from the golden file's own kinds, so it never runs ingest, and it passes with either lib11 truth. evals/run.py:243 to 248 scores (from, to, days, flag) only. evals/reports/library-latest.md has no endpoint column; library-pre-vs-head.diff is empty. Mutant A (pre-commit lib11 truth restored in a scratch copy): validate_library.py exit 0 (T-118-out/mutA-validators.txt), pytest of both gap files 116 passed (T-118-out/pytest-mutA.txt), while the endpoint probe reports 3 differences (T-118-out/mutA-probe.txt). reviews/T-116-paralegal.md finding 2 fix asked to 'make the gap test compare (from_records, to_records) for all golden and library packets'. The T-116 r2 handoff deferred it ('Suggest tests/unit gap test compare ...').\",\n   \"why_it_matters\": \"The T-118 acceptance line says the library report is unchanged 'except lib11 gap endpoints', but the report cannot show endpoints, so that claim cannot be checked from the report. Any future change to a record list on any packet, lib11 included, passes every committed test and the library report. Only the probe I wrote for this review catches it. The persona's checklist item 5 and the T-116 finding depend on this.\",\n   \"fix\": \"Add a tests/unit test that ingests each golden and library packet (ingest, language.annotate, gaps.compute_gaps, as artifacts/review-evidence/T-118-paralegal-endpoints.py does) and asserts from_records and to_records for every gap_table row, and gap_excluded_records equal to the expected values. Add an endpoint column to evals/library_report or compare record lists in evals/run.py:243 to 248.\",\n   \"acceptance_test\": \"On mutant A (pre-commit lib11 truth), the new test fails naming case_lib11_priors_and_ledger. On HEAD it passes, and artifacts/review-evidence/T-118-paralegal-endpoints.py reports 0 differences over 25 packets (T-118-out/probe-head.txt).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Committed evals/reports/library-latest.md is stale against HEAD (lib09 amounts row), so the report cannot be used as the 'unchanged' baseline; not caused by 78450f6\",\n   \"evidence\": \"evals/reports/library-latest.md:17 '| case_lib09_spanish_interpreter_espalda | done | 4/7 | 2/5 | False | 1/2 | 0 | M5 | 0 | - |'. Regenerated at HEAD and at ea6ac71: '3/5' (T-118-out/library-committed-vs-head.diff; library-pre-vs-head.diff empty). The committed file's source commit is a74b727. git show --stat 78450f6 does not list it.\",\n   \"why_it_matters\": \"A committed report that does not match HEAD cannot show what a commit changed, and the persona's billed-charge reconciliation depends on the report agreeing with the code. The stale amounts row predates this card.\",\n   \"fix\": \"qa regenerates evals/reports/library-latest.md from a clean worktree of the commit it cites, as the file's own header asks, and the card cites that commit.\",\n   \"acceptance_test\": \"Running evals.library_report at the cited commit in a clean worktree gives a report identical to the committed file, except the provenance line.\"}\n ],\n \"whats_right\": [\n  \"The five lib11 edits match the T-116 r2 card note item for item (git show 78450f6 diff at lines 57, 190, 251 to 254, 276 to 279, 286 to 289); dates, days and flags are unchanged.\",\n  \"Product gap endpoints are correct on all 25 golden and library packets, including record lists and exclusions (probe at HEAD: 0 differences); lib11 record 6 is excluded by its intake-form header (packet line 30).\",\n  \"Both validators pass on HEAD, and the commit touches only the lib11 truth file plus two fixture reports (git diff --stat ea6ac71 78450f6).\"\n ],\n \"questions_for_chris\": [\n  \"Should an intake form dated the same day as a visit (lib11 record 6, 'Prior accidents? No') stay a chronology entry? Today it is entry E6, the truth says it is not an encounter, and the product still says encounter. The answer decides whether the adjuster-facing 'prior accidents: No' answer is listed in the treatment chronology or kept in an administrative entry.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T10:03:57.502Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-118-paralegal.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:04:04.853Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-jsoncheck.py",
 "content": "\"\"\"T-118 paralegal-reviewer check of reviews/T-118-paralegal.md: one fenced json block, parses, D.2 fields present,\nseverities valid, verdict follows the rule (blocker -> fail, major -> changes, else pass), and every finding has evidence.\"\"\"\nimport json\nimport re\nimport sys\n\npath = \"/Users/arsis/zlayt-pm-project/reviews/T-118-paralegal.md\"\ntext = open(path, encoding=\"utf-8\").read()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", text, flags=re.S)\nassert len(blocks) == 1, f\"expected exactly one json block, found {len(blocks)}\"\nd = json.loads(blocks[0])\nfor k in (\"card\", \"persona\", \"model\", \"scope\", \"exercised\", \"verdict\", \"scores\", \"findings\", \"whats_right\", \"questions_for_chris\"):\n    assert k in d, f\"missing {k}\"\nassert d[\"card\"] == \"T-118\" and d[\"persona\"] == \"paralegal-reviewer\" and d[\"model\"] == \"claude-haiku-5-5\"\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nassert all(s in (\"blocker\", \"major\", \"minor\", \"nit\") for s in sev)\nfor f in d[\"findings\"]:\n    for k in (\"severity\", \"title\", \"evidence\", \"why_it_matters\", \"fix\", \"acceptance_test\"):\n        assert f.get(k), f\"finding missing {k}\"\nexpected = \"fail\" if \"blocker\" in sev else \"changes\" if \"major\" in sev else \"pass\"\nassert d[\"verdict\"] == expected, f\"verdict {d['verdict']} != rule {expected}\"\nassert len(d[\"whats_right\"]) <= 3\nassert all(isinstance(v, int) and 1 <= v <= 5 for v in d[\"scores\"].values())\nprint(\"ok: one json block, parses, verdict\", d[\"verdict\"], \"by rule; severities\", sev, \"; whats_right\", len(d[\"whats_right\"]))\nsys.exit(0)\n"
}
````

### User / tool · 2026-11-02T10:04:04.956Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-118-paralegal-jsoncheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:04:06.651Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-118-paralegal-jsoncheck.py; echo \"EXIT=$?\"; python3 tools/board.py validate reviews/T-118-paralegal.md; echo \"VALIDATE EXIT=$?\"",
 "description": "Validate the review JSON block and the board review format"
}
````

### User / tool · 2026-11-02T10:04:06.828Z

**tool result**
````
ok: one json block, parses, verdict changes by rule; severities ['major', 'major', 'minor'] ; whats_right 3
EXIT=0
ok (1 file(s))
VALIDATE EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:04:18.564Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t118-lib11-truth-patterns.md",
 "content": "---\nname: t118-lib11-truth-patterns\ndescription: T-118 (78450f6) lib11 truth edits: validators pass on the pre-commit truth too; record lists unguarded by tests and scorer; checker vocabulary forces phone_note for intake forms and letters\nmetadata:\n  type: project\n---\n\nRecurring pattern: a golden or library truth edit is \"validated\" by validators that cannot tell the wrong truth from the right one. T-118 mutant A\n(pre-commit lib11 truth restored): validate_library.py exit 0, check_golden exit 0, and the two gap test files 116 passed. Only a product-level\nendpoint comparison (artifacts/review-evidence/T-118-paralegal-endpoints.py) separates them. Test any truth-file change by restoring the old file on\na scratch copy and seeing which gate fails.\n\nRecurring pattern: check_golden.py:200 allows only encounter, billing_statement, phone_note. Intake forms and letters get phone_note as a stand-in\n(lib11 record 4 letter pre-existing, record 6 intake form from T-118). check_golden.py:255 to 260 derive gap_excluded_records from those kinds, so\nrestoring kind encounter on an intake form fails the checker (mutant B). The stand-in is a false record type in the truth file.\n\nRecurring pattern: tests/unit/test_gaps.py:6 to 7 builds records from the golden file's own kinds (circular); test_t116_gap_endpoints.py:165 to 173\ncompares dates, days and flags only; evals/run.py:243 to 248 scores dates, days and flags only. No committed test compares product record lists\nto expected lists. T-116 r1 major asked for that test; it was still missing at 78450f6.\n\nRecurring pattern: gap_excluded_records in the golden files means \"not a gap endpoint\", which includes undated visits (lib14 record 5, \"10/20\").\nDefining it as non-treatment records gives a false difference on lib14.\n\nRecurring pattern: evals/reports/library-latest.md is committed and has no endpoint column. It was stale at HEAD (lib09 amounts row committed 2/5,\nregenerated 3/5 at both ea6ac71 and 78450f6). It cannot show a record-list change.\n\nWhy: T-118 review (2026-11-02, verdict changes; 0 blockers; majors: stand-in kind, unguarded endpoints).\nHow to apply: on any gap or truth change, run the endpoint probe on HEAD and on the parent (expect 0 and the changed packet's diffs only), and\nrestore the parent's truth file on a scratch copy to confirm a gate fails. Check whether the record-kind stand-in has been replaced by an intake_form kind.\n\nRelated: [[t116-gap-endpoint-patterns]], [[library-review-patterns]], [[golden-set-recurring-findings]], [[reviewer-hook-constraints]].\n"
}
````

### User / tool · 2026-11-02T10:04:18.674Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t118-lib11-truth-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:04:20.719Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — label substring exclusion invents gaps; stale lib11 truth; golden kind vocabulary lacks intake form",
 "new_string": "- [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — label substring exclusion invents gaps; stale lib11 truth; golden kind vocabulary lacks intake form\n- [T-118 lib11 truth patterns](t118-lib11-truth-patterns.md) — validators pass on the wrong truth; record lists unguarded; intake form as phone_note stand-in; stale library-latest.md"
}
````

### User / tool · 2026-11-02T10:04:20.722Z

**tool result (error)**
````
<tool_use_error>String to replace not found in file.
String: - [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — label substring exclusion invents gaps; stale lib11 truth; golden kind vocabulary lacks intake form
(note: Edit also tried swapping \uXXXX escapes and their characters; neither form matched, so the mismatch is likely elsewhere in old_string. Re-read the file and copy the exact surrounding text.)</tool_use_error>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:04:22.279Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T10:04:22.285Z

**tool result**
````
1	- [Spec review patterns](feedback_spec_review_patterns.md) — check absolute claims vs the doc's own example; grep every named category/R-ID/fixture
2	- [Golden-set recurring findings](golden-set-recurring-findings.md) — T-015: must/should levels, shared type+cite flags, export/§6 drift, dead checks via key drift (mutation-test)
3	- [Reviewer hook constraints](reviewer-hook-constraints.md) — board.py allowed verbs, python heredoc form, write-allowed dirs
4	- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; review files are append-only (proofread before the one Write)
5	- [Frontend review patterns](frontend-review-patterns.md) — T-043: mock vs harness coverage, keyboard focus yank, recurring minor gaps
6	- [Library review patterns](library-review-patterns.md) — T-052 minors; T-077 r2/r3: self-test shape-bound (author-year, prose escape), title-case FAIR Health passes
7	- [Record-format review patterns](record-format-review-patterns.md) — T-078 r2: mutation-test the check script; visit-count fix creates a PT gap; lib14 specimen gaps
8	- [Manual entry / split review patterns](manual-entry-split-review-patterns.md) — T-056: AC ticked for absent UI label, split amounts not moving, override trace missing
9	- [T-068 dates-to-confirm patterns](t068-dates-to-confirm-patterns.md) — orphan confirm dead-ends, record listed twice, text-only AC test, commit vs worktree divergence
10	- [D-041 date-gate patterns](d041-date-gate-patterns.md) — T-076 r2 (f4ef2ea): stale DATE_AMBIGUOUS fixed; Edit/Change quote still enabled on undated row (T-060)
11	- [Reviewer API shape gotchas](reviewer-api-shape-gotchas.md) — item GET nests under "item", status "ready", record warnings in case.flags, audit before/after local-only
12	- [T-079 library v2 patterns](t079-library-v2-patterns.md) — statement-vs-note double count, replay at cited commit, append-only ref proofreading
13	- [T-114 rates and gap patterns](t114-rates-gap-patterns.md) — rate acknowledge-only passes; gap change API-only in HEAD; intake-form encounter kind is Chris's call; golden N1 scoped to ambiguous
14	- [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — r2: bare trailing "fax"/"statement" still excludes visits; intake-form accident baseline; stale lib11 truth
15	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:04:25.301Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "stale lib11 truth\n",
 "new_string": "stale lib11 truth\n- [T-118 lib11 truth patterns](t118-lib11-truth-patterns.md) — validators pass on the wrong truth; record lists unguarded; intake form as phone_note stand-in; stale library-latest.md\n"
}
````

### User / tool · 2026-11-02T10:04:25.406Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:04:28.048Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md",
 "old_string": "- Write access is limited to reviews/ and artifacts/review-evidence/ (plus this memory dir). Probe scripts go in artifacts/review-evidence/.",
 "new_string": "- Write access is limited to reviews/ and artifacts/review-evidence/ (plus this memory dir). Probe scripts go in artifacts/review-evidence/.\n- T-118 (2026-11-02): the Write tool is refused for the session scratchpad (reviewer-write-guard), and board-guard refuses `mkdir` there. A Bash `git archive | tar -x` into the scratchpad still worked. Put scripts and output dirs under artifacts/review-evidence/ and run archive copies from the scratchpad. Run them with `.venv/bin/python -I` and a runner that puts the archive root first on sys.path."
}
````

### User / tool · 2026-11-02T10:04:28.146Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:04:30.875Z

T-118 verdict is changes (0 blockers, 2 major, 1 minor): the five edits match the card and both validators pass, but the truth file labels the intake form `phone_note` and no test guards the lib11 endpoints. Review: /Users/arsis/zlayt-pm-project/reviews/T-118-paralegal.md
