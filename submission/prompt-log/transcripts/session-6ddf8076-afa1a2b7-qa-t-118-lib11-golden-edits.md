# Subagent: QA: T-118 lib11 golden edits (QA: T-118 lib11 golden edits)

Source: `agent-afa1a2b71b14ba5db.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T09:55:20.371Z

You own board card T-118 (claimed by "qa") in /Users/arsis/zlayt-pm-project. Read the T-116 card note with the five lib11 edits (`python3 tools/board.py show T-116`) and apply all five together to the lib11 expected file under evals/library.

Then run:
- `python3 research/validate_library.py`;
- `python3 evals/golden/check_golden.py`, if it exists;
- `.venv/bin/python -m evals.run` (fixture backend). Confirm the library report changes only lib11's gap endpoints.

Commit with `git add <paths>` then `git commit -m "..." -- <paths>` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-118 in_review --agent qa`. Reply in 1 line.

### User / tool · 2026-11-02T09:55:20.376Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:25.195Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-116 && echo ---- && python3 tools/board.py show T-118",
 "description": "Show cards T-116 and T-118"
}
````

### User / tool · 2026-11-02T09:55:25.382Z

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
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T09:55:10Z"
updated_at: "2026-11-02T09:55:17Z"
claimed_by: "qa"
claimed_at: "2026-11-02T09:55:17Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "The five lib11 edits from the T-116 card note are applied together; research/validate_library.py and evals/golden/check_golden.py pass; evals.run library report unchanged except lib11 gap endpoints", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T09:55:17Z qa: claimed

## Handoff (filled when moving to in_review)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:25.598Z

**tool call — Bash**
````
{
 "command": "ls evals/library evals/golden 2>&1; ls research | head -50; git status --short | head -30",
 "description": "List eval, research dirs and git status"
}
````

### User / tool · 2026-11-02T09:55:25.718Z

**tool result**
````
evals/golden:
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

evals/library:
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
case_lib06_lop_billed_vs_adjusted.expected.json
case_lib06_lop_billed_vs_adjusted.txt
case_lib07_parking_lot_fall_outside_records.expected.json
case_lib07_parking_lot_fall_outside_records.txt
case_lib08_second_crash_mri_after.expected.json
case_lib08_second_crash_mri_after.txt
case_lib09_spanish_interpreter_espalda.expected.json
case_lib09_spanish_interpreter_espalda.txt
case_lib10_eob_ub04_cms1500.expected.json
case_lib10_eob_ub04_cms1500.txt
case_lib11_priors_and_ledger.expected.json
case_lib11_priors_and_ledger.txt
case_lib12_records_review_credibility.expected.json
case_lib12_records_review_credibility.txt
case_lib13_cloned_notes_cross_provider.expected.json
case_lib13_cloned_notes_cross_provider.txt
case_lib14_handwritten_chiro_scans.expected.json
case_lib14_handwritten_chiro_scans.txt
case_lib15_conclusory_letter_mist.expected.json
case_lib15_conclusory_letter_mist.txt
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
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/pipeline.py
 M app/frontend/app.js
 M app/frontend/audit.js
 M app/frontend/batch.js
 M app/frontend/charges.js
 M app/frontend/excerpt.js
 M app/frontend/export.js
 M app/frontend/exportcfg.js
 M app/frontend/flags.js
 M app/frontend/index.html
 M app/frontend/input.js
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:28.435Z

**tool call — Bash**
````
{
 "command": "F=evals/library/case_lib11_priors_and_ledger.expected.json && sed -n '55,59p;188,192p;250,255p;274,290p' $F && echo ---- && python3 -c \"import json;json.load(open('$F'));print('json ok')\"",
 "description": "Show lines targeted by the five lib11 edits"
}
````

### User / tool · 2026-11-02T09:55:28.548Z

**tool result**
````
      "raw_date": "3/27/26",
      "date": "2026-03-27",
      "kind": "encounter",
      "source": "Fennimoor Spine Clinic, new patient intake form (OCR text)"
    },
      "date": "2026-03-27",
      "date_status": "parsed",
      "encounter": true,
      "provider": "Fennimoor Spine Clinic, new patient intake form (OCR text)",
      "must_contain_excerpt": "Prior accidents? Yes [ ] No [X]",
  "expected_entry_count": 9,
  "gap_excluded_records": [
    4,
    9
  ],
  "gap_table": [
        3
      ],
      "to_records": [
        5,
        6
      ],
      "days": 9,
      "flag": false
    },
    {
      "from_date": "2026-03-27",
      "to_date": "2026-04-24",
      "from_records": [
        5,
        6
      ],
      "to_records": [
----
json ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:31.566Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json\nd=json.load(open('evals/library/case_lib11_priors_and_ledger.expected.json'))\nprint(d.keys())\nfor i,r in enumerate(d.get('records',[]),1): print(i, r.get('kind'), r.get('source'))\nfor e in d.get('entries',[]): \n  if e.get('id')=='E6' or e.get('entry_id')=='E6': print(e)\nprint([x for x in d.get('entries',[]) if 'E6' in json.dumps(x)][:1])\n\"",
 "description": "Inspect lib11 records and entries structure"
}
````

### User / tool · 2026-11-02T09:55:31.667Z

**tool result**
````
dict_keys(['schema_version', 'case_id', 'synthetic', 'input_file', 'description', 'stress_types', 'records', 'entries', 'expected_entry_count', 'gap_excluded_records', 'gap_table', 'amounts', 'totals', 'flags', 'must_not_flag', 'tolerated', 'record_warnings', 'must_not', 'notes'])
1 encounter Dr. Hesper Alderton, primary care
2 encounter Ashgrove Fire-Rescue run report
3 encounter Wexcombe Memorial ED
4 phone_note Pellingham and Rook PLLC, correspondence (letter of protection)
5 encounter Fennimoor Spine Clinic, new patient
6 encounter Fennimoor Spine Clinic, new patient intake form (OCR text)
7 encounter Fennimoor Spine Clinic, visit 8
8 encounter Fennimoor Spine Clinic, visit 14
9 billing_statement Fennimoor Spine Clinic, itemized ledger
{'id': 'E6', 'record_nos': [6], 'date': '2026-03-27', 'date_status': 'parsed', 'encounter': True, 'provider': 'Fennimoor Spine Clinic, new patient intake form (OCR text)', 'must_contain_excerpt': 'Prior accidents? Yes [ ] No [X]', 'required_terms': [['prior accident', 'previous accident', 'accidents']], 'note': 'Scanned form as OCR text: l for 1, I for l, G for 6 are kept as scanned. Header date 3/27/26 is unambiguous (27 > 12). The accident date inside the form is evidence for conflict checks only, never a service date.'}
[{'id': 'E6', 'record_nos': [6], 'date': '2026-03-27', 'date_status': 'parsed', 'encounter': True, 'provider': 'Fennimoor Spine Clinic, new patient intake form (OCR text)', 'must_contain_excerpt': 'Prior accidents? Yes [ ] No [X]', 'required_terms': [['prior accident', 'previous accident', 'accidents']], 'note': 'Scanned form as OCR text: l for 1, I for l, G for 6 are kept as scanned. Header date 3/27/26 is unambiguous (27 > 12). The accident date inside the form is evidence for conflict checks only, never a service date.'}]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:33.703Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json"
}
````

### User / tool · 2026-11-02T09:55:33.844Z

**tool result**
````
1	{
2	  "schema_version": "golden/1",
3	  "case_id": "case_lib11_priors_and_ledger",
4	  "synthetic": true,
5	  "input_file": "case_lib11_priors_and_ledger.txt",
6	  "description": "Library L11 (P5+P2). Rear-end collision two weeks after an annual primary-care visit that lists two earlier car accidents, a chronic low back problem and a baseline back pain score. Attorney-referred spine clinic under a letter of protection, a scanned intake form (OCR text) answering 'prior accidents: No', and an itemized ledger with charges, a payment, a courtesy adjustment and a balance. Only stated charges count; payment, adjustment and balance are listed unclear.",
7	  "stress_types": [
8	    "intake_denies_prior_accidents",
9	    "prior_accidents_in_older_note",
10	    "baseline_back_pain_before_accident",
11	    "itemized_ledger_billed_adjusted_paid",
12	    "letter_of_protection",
13	    "ocr_noise_text",
14	    "attorney_referral",
15	    "balance_double_count_trap"
16	  ],
17	  "records": [
18	    {
19	      "record_no": 1,
20	      "raw_date": "2026-03-04",
21	      "date": "2026-03-04",
22	      "kind": "encounter",
23	      "source": "Dr. Hesper Alderton, primary care"
24	    },
25	    {
26	      "record_no": 2,
27	      "raw_date": "2026-03-18",
28	      "date": "2026-03-18",
29	      "kind": "encounter",
30	      "source": "Ashgrove Fire-Rescue run report"
31	    },
32	    {
33	      "record_no": 3,
34	      "raw_date": "2026-03-18",
35	      "date": "2026-03-18",
36	      "kind": "encounter",
37	      "source": "Wexcombe Memorial ED"
38	    },
39	    {
40	      "record_no": 4,
41	      "raw_date": "2026-03-26",
42	      "date": "2026-03-26",
43	      "kind": "phone_note",
44	      "source": "Pellingham and Rook PLLC, correspondence (letter of protection)"
45	    },
46	    {
47	      "record_no": 5,
48	      "raw_date": "2026-03-27",
49	      "date": "2026-03-27",
50	      "kind": "encounter",
51	      "source": "Fennimoor Spine Clinic, new patient"
52	    },
53	    {
54	      "record_no": 6,
55	      "raw_date": "3/27/26",
56	      "date": "2026-03-27",
57	      "kind": "encounter",
58	      "source": "Fennimoor Spine Clinic, new patient intake form (OCR text)"
59	    },
60	    {
61	      "record_no": 7,
62	      "raw_date": "2026-04-24",
63	      "date": "2026-04-24",
64	      "kind": "encounter",
65	      "source": "Fennimoor Spine Clinic, visit 8"
66	    },
67	    {
68	      "record_no": 8,
69	      "raw_date": "2026-05-29",
70	      "date": "2026-05-29",
71	      "kind": "encounter",
72	      "source": "Fennimoor Spine Clinic, visit 14"
73	    },
74	    {
75	      "record_no": 9,
76	      "raw_date": "2026-06-15",
77	      "date": "2026-06-15",
78	      "kind": "billing_statement",
79	      "source": "Fennimoor Spine Clinic, itemized ledger"
80	    }
81	  ],
82	  "entries": [
83	    {
84	      "id": "E1",
85	      "record_nos": [
86	        1
87	      ],
88	      "date": "2026-03-04",
89	      "date_status": "parsed",
90	      "encounter": true,
91	      "provider": "Dr. Hesper Alderton, primary care",
92	      "must_contain_excerpt": "car accidents in 2019 and 2022",
93	      "required_terms": [
94	        "2019",
95	        "2022",
96	        "chronic low back pain"
97	      ],
98	      "self_report_spans": [
99	        {
100	          "excerpt": "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.",
101	          "attribution_any": [
102	            "patient states",
103	            "per patient",
104	            "patient reports"
105	          ]
106	        }
107	      ]
108	    },
109	    {
110	      "id": "E2",
111	      "record_nos": [
112	        2
113	      ],
114	      "date": "2026-03-18",
115	      "date_status": "parsed",
116	      "encounter": true,
117	      "provider": "Ashgrove Fire-Rescue run report",
118	      "must_contain_excerpt": "Passenger vehicle struck from behind",
119	      "required_terms": [
120	        "low back pain"
121	      ],
122	      "self_report_spans": [
123	        {
124	          "excerpt": "Pt states neck and low back pain 7/10.",
125	          "attribution_any": [
126	            "pt states",
127	            "patient states",
128	            "per patient",
129	            "patient reports",
130	            "reports"
131	          ]
132	        }
133	      ]
134	    },
135	    {
136	      "id": "E3",
137	      "record_nos": [
138	        3
139	      ],
140	      "date": "2026-03-18",
141	      "date_status": "parsed",
142	      "encounter": true,
143	      "provider": "Wexcombe Memorial ED",
144	      "must_contain_excerpt": "X-ray cervical and lumbar spine negative for fracture",
145	      "required_terms": [
146	        "cervical strain",
147	        "lumbar strain"
148	      ]
149	    },
150	    {
151	      "id": "E4",
152	      "record_nos": [
153	        4
154	      ],
155	      "date": "2026-03-26",
156	      "date_status": "parsed",
157	      "encounter": false,
158	      "provider": "Pellingham and Rook PLLC, correspondence (letter of protection)",
159	      "must_contain_excerpt": "Letter of protection to Fennimoor Spine Clinic",
160	      "required_terms": [
161	        [
162	          "letter of protection",
163	          "lop"
164	        ]
165	      ]
166	    },
167	    {
168	      "id": "E5",
169	      "record_nos": [
170	        5
171	      ],
172	      "date": "2026-03-27",
173	      "date_status": "parsed",
174	      "encounter": true,
175	      "provider": "Fennimoor Spine Clinic, new patient",
176	      "must_contain_excerpt": "Patient referred by attorney",
177	      "required_terms": [
178	        "referred by attorney",
179	        "letter of protection",
180	        "7/10"
181	      ]
182	    },
183	    {
184	      "id": "E6",
185	      "record_nos": [
186	        6
187	      ],
188	      "date": "2026-03-27",
189	      "date_status": "parsed",
190	      "encounter": true,
191	      "provider": "Fennimoor Spine Clinic, new patient intake form (OCR text)",
192	      "must_contain_excerpt": "Prior accidents? Yes [ ] No [X]",
193	      "required_terms": [
194	        [
195	          "prior accident",
196	          "previous accident",
197	          "accidents"
198	        ]
199	      ],
200	      "note": "Scanned form as OCR text: l for 1, I for l, G for 6 are kept as scanned. Header date 3/27/26 is unambiguous (27 > 12). The accident date inside the form is evidence for conflict checks only, never a service date."
201	    },
202	    {
203	      "id": "E7",
204	      "record_nos": [
205	        7
206	      ],
207	      "date": "2026-04-24",
208	      "date_status": "parsed",
209	      "encounter": true,
210	      "provider": "Fennimoor Spine Clinic, visit 8",
211	      "must_contain_excerpt": "Neck pain 5/10, low back pain 6/10",
212	      "required_terms": [
213	        "5/10",
214	        "6/10"
215	      ]
216	    },
217	    {
218	      "id": "E8",
219	      "record_nos": [
220	        8
221	      ],
222	      "date": "2026-05-29",
223	      "date_status": "parsed",
224	      "encounter": true,
225	      "provider": "Fennimoor Spine Clinic, visit 14",
226	      "must_contain_excerpt": "Neck pain 4/10, low back pain 5/10",
227	      "required_terms": [
228	        "4/10",
229	        "5/10"
230	      ]
231	    },
232	    {
233	      "id": "E9",
234	      "record_nos": [
235	        9
236	      ],
237	      "date": "2026-06-15",
238	      "date_status": "parsed",
239	      "encounter": false,
240	      "provider": "Fennimoor Spine Clinic, itemized ledger",
241	      "must_contain_excerpt": "Account held under letter of protection",
242	      "required_terms": [
243	        [
244	          "letter of protection",
245	          "lop"
246	        ]
247	      ]
248	    }
249	  ],
250	  "expected_entry_count": 9,
251	  "gap_excluded_records": [
252	    4,
253	    9
254	  ],
255	  "gap_table": [
256	    {
257	      "from_date": "2026-03-04",
258	      "to_date": "2026-03-18",
259	      "from_records": [
260	        1
261	      ],
262	      "to_records": [
263	        2,
264	        3
265	      ],
266	      "days": 14,
267	      "flag": false
268	    },
269	    {
270	      "from_date": "2026-03-18",
271	      "to_date": "2026-03-27",
272	      "from_records": [
273	        2,
274	        3
275	      ],
276	      "to_records": [
277	        5,
278	        6
279	      ],
280	      "days": 9,
281	      "flag": false
282	    },
283	    {
284	      "from_date": "2026-03-27",
285	      "to_date": "2026-04-24",
286	      "from_records": [
287	        5,
288	        6
289	      ],
290	      "to_records": [
291	        7
292	      ],
293	      "days": 28,
294	      "flag": false
295	    },
296	    {
297	      "from_date": "2026-04-24",
298	      "to_date": "2026-05-29",
299	      "from_records": [
300	        7
301	      ],
302	      "to_records": [
303	        8
304	      ],
305	      "days": 35,
306	      "flag": true
307	    }
308	  ],
309	  "amounts": [
310	    {
311	      "id": "A1",
312	      "record_no": 3,
313	      "raw": "$3,260",
314	      "value": 3260,
315	      "class": "charge",
316	      "excerpt": "ED charge: $3,260",
317	      "in_total": true,
318	      "required": true,
319	      "needs_review": false
320	    },
321	    {
322	      "id": "A2",
323	      "record_no": 9,
324	      "raw": "$250.00",
325	      "value": 250,
326	      "class": "charge",
327	      "excerpt": "New patient exam charge $250.00",
328	      "in_total": true,
329	      "required": true,
330	      "needs_review": false
331	    },
332	    {
333	      "id": "A3",
334	      "record_no": 9,
335	      "raw": "$180.00",
336	      "value": 180,
337	      "class": "charge",
338	      "excerpt": "x-ray charge $180.00",
339	      "in_total": true,
340	      "required": true,
341	      "needs_review": false
342	    },
343	    {
344	      "id": "A4",
345	      "record_no": 9,
346	      "raw": "$2,310.00",
347	      "value": 2310,
348	      "class": "charge",
349	      "excerpt": "charge $2,310.00",
350	      "in_total": true,
351	      "required": true,
352	      "needs_review": false
353	    },
354	    {
355	      "id": "A5",
356	      "record_no": 9,
357	      "raw": "$2,740.00",
358	      "value": null,
359	      "class": "unclear",
360	      "excerpt": "total charges $2,740.00",
361	      "in_total": false,
362	      "required": true,
363	      "needs_review": true,
364	      "note": "Ledger total repeats the three ledger lines above; counting it double counts."
365	    },
366	    {
367	      "id": "A6",
368	      "record_no": 9,
369	      "raw": "$300.00",
370	      "value": null,
371	      "class": "unclear",
372	      "excerpt": "Payment received $300.00",
373	      "in_total": false,
374	      "required": true,
375	      "needs_review": true,
376	      "note": "Payment, not a charge."
377	    },
378	    {
379	      "id": "A7",
380	      "record_no": 9,
381	      "raw": "$274.00",
382	      "value": null,
383	      "class": "unclear",
384	      "excerpt": "Adjustment (courtesy discount) -$274.00",
385	      "in_total": false,
386	      "required": true,
387	      "needs_review": true,
388	      "note": "Adjustment with a negative sign; not a charge and never netted from billed."
389	    },
390	    {
391	      "id": "A8",
392	      "record_no": 9,
393	      "raw": "$2,166.00",
394	      "value": null,
395	      "class": "unclear",
396	      "excerpt": "Balance due $2,166.00",
397	      "in_total": false,
398	      "required": true,
399	      "needs_review": true,
400	      "note": "Balance = 2,740.00 - 300.00 - 274.00; derived, not a charge."
401	    }
402	  ],
403	  "totals": {
404	    "explicit_charges_total": 6000,
405	    "counted_amount_ids": [
406	      "A1",
407	      "A2",
408	      "A3",
409	      "A4"
410	    ],
411	    "amounts_found": 8,
412	    "status": "partial_unclear",
413	    "unclear_items": [
414	      {
415	        "amount_id": "A5",
416	        "reason": "Ledger total repeats the three ledger lines above; counting it double counts; needs review",
417	        "total_computed": false
418	      },
419	      {
420	        "amount_id": "A6",
421	        "reason": "Payment, not a charge; needs review",
422	        "total_computed": false
423	      },
424	      {
425	        "amount_id": "A7",
426	        "reason": "Adjustment with a negative sign; not a charge and never netted from billed; needs review",
427	        "total_computed": false
428	      },
429	      {
430	        "amount_id": "A8",
431	        "reason": "Balance = 2,740.00 - 300.00 - 274.00; derived, not a charge; needs review",
432	        "total_computed": false
433	      }
434	    ],
435	    "letter_line": "Billed charges stated in these records: $6,000.00",
436	    "ui_line": "Accepted charges: $6,000.00",
437	    "notes_lines": [
438	      "$2,740.00: Ledger total repeats the three ledger lines above; counting it double counts; needs review",
439	      "$300.00: Payment, not a charge; needs review",
440	      "$274.00: Adjustment with a negative sign; not a charge and never netted from billed; needs review",
441	      "$2,166.00: Balance = 2,740.00 - 300.00 - 274.00; derived, not a charge; needs review"
442	    ]
443	  },
444	  "flags": [
445	    {
446	      "id": "G1",
447	      "type": "gap",
448	      "level": "must",
449	      "from_date": "2026-04-24",
450	      "to_date": "2026-05-29",
451	      "days": 35,
452	      "cite": {
453	        "all": [
454	          7,
455	          8
456	        ],
457	        "any": []
458	      },
459	      "evidence": [
460	        {
461	          "record_no": 7,
462	          "field": "excerpt",
463	          "excerpt": "Manual therapy and exercises continued"
464	        },
465	        {
466	          "record_no": 8,
467	          "field": "excerpt",
468	          "excerpt": "Neck pain 4/10, low back pain 5/10"
469	        }
470	      ],
471	      "summary": "Treatment gap of 35 days (2026-04-24 to 2026-05-29), longer than 30."
472	    },
473	    {
474	      "id": "P1",
475	      "type": "pre_existing",
476	      "level": "must",
477	      "cite": {
478	        "all": [
479	          1
480	        ],
481	        "any": []
482	      },
483	      "evidence": [
484	        {
485	          "record_no": 1,
486	          "field": "excerpt",
487	          "excerpt": "chronic low back pain"
488	        }
489	      ],
490	      "summary": "Problem list entry before the collision; stated as the record's wording only.",
491	      "subtype": "prior_condition_listed"
492	    },
493	    {
494	      "id": "P2",
495	      "type": "pre_existing",
496	      "level": "must",
497	      "cite": {
498	        "all": [
499	          1
500	        ],
501	        "any": []
502	      },
503	      "evidence": [
504	        {
505	          "record_no": 1,
506	          "field": "excerpt",
507	          "excerpt": "car accidents in 2019 and 2022"
508	        }
509	      ],
510	      "summary": "Two earlier car accidents reported by the patient in a note dated two weeks before the collision.",
511	      "subtype": "prior_accidents_reported"
512	    },
513	    {
514	      "id": "P3",
515	      "type": "pre_existing",
516	      "level": "should",
517	      "cite": {
518	        "all": [
519	          1
520	        ],
521	        "any": []
522	      },
523	      "evidence": [
524	        {
525	          "record_no": 1,
526	          "field": "excerpt",
527	          "excerpt": "Low back pain 3/10 today"
528	        }
529	      ],
530	      "summary": "Back pain score recorded before the collision.",
531	      "subtype": "baseline_symptom_before_accident"
532	    },
533	    {
534	      "id": "C1",
535	      "type": "conflict",
536	      "level": "must",
537	      "cite": {
538	        "all": [
539	          1,
540	          6
541	        ],
542	        "any": []
543	      },
544	      "evidence": [
545	        {
546	          "record_no": 1,
547	          "field": "excerpt",
548	          "excerpt": "car accidents in 2019 and 2022"
549	        },
550	        {
551	          "record_no": 6,
552	          "field": "excerpt",
553	          "excerpt": "Prior accidents? Yes [ ] No [X]"
554	        }
555	      ],
556	      "summary": "The intake form answers 'Prior accidents? No' while the primary-care note of 2026-03-04 lists accidents in 2019 and 2022. Both cited; the tool does not say which is right.",
557	      "subtype": "intake_denies_prior_accidents"
558	    },
559	    {
560	      "id": "K1",
561	      "type": "causation",
562	      "level": "should",
563	      "cite": {
564	        "all": [
565	          5
566	        ],
567	        "any": []
568	      },
569	      "evidence": [
570	        {
571	          "record_no": 5,
572	          "field": "excerpt",
573	          "excerpt": "Patient referred by attorney"
574	        }
575	      ],
576	      "summary": "Attorney referral and letter-of-protection treatment (internal notes only, D-001/D-018); the record wording is stated and no inference is drawn about charges.",
577	      "subtype": "litigation_referral"
578	    }
579	  ],
580	  "must_not_flag": [
581	    {
582	      "id": "N1",
583	      "type": "gap",
584	      "statement": "No gap flag for the 14, 9 and 28-day intervals; the letter of protection (record 4) and the ledger (record 9) are not gap endpoints."
585	    }
586	  ],
587	  "tolerated": [],
588	  "record_warnings": [],
589	  "must_not": [
590	    {
591	      "id": "M1",
592	      "statement": "Counts the ledger total, payment, adjustment or balance as a charge, or adds the total line to the lines (values 2,740 / 2,166 / 274 / 300 / 8,740).",
593	      "check": "amount_value",
594	      "bad_examples": [
595	        {
596	          "raw": "$2,740",
597	          "value": 2740,
598	          "class": "charge"
599	        },
600	        {
601	          "raw": "$2,166",
602	          "value": 2166,
603	          "class": "charge"
604	        },
605	        {
606	          "raw": "$274",
607	          "value": 274,
608	          "class": "charge"
609	        }
610	      ],
611	      "good_examples": [
612	        {
613	          "raw": "$6,240",
614	          "value": 6240,
615	          "class": "charge"
616	        },
617	        {
618	          "raw": "$185",
619	          "value": 185,
620	          "class": "rate"
621	        },
622	        {
623	          "raw": "$1,2OO",
624	          "value": null,
625	          "class": "unclear"
626	        }
627	      ],
628	      "values": [
629	        2740,
630	        2166,
631	        274,
632	        300,
633	        8740
634	      ]
635	    },
636	    {
637	      "id": "M2",
638	      "statement": "Nets the payment or adjustment into the billed figure, calls the charges reduced, reasonable or inflated, or states what was incurred.",
639	      "check": "judge",
640	      "bad_examples": [
641	        "Charges after the courtesy discount total $5,726.",
642	        "The clinic reduced its bill to $2,166.00.",
643	        "The amount incurred is $2,166.00."
644	      ],
645	      "good_examples": [
646	        "Ledger lists total charges $2,740.00, payment $300.00, a courtesy discount and a balance due; none netted.",
647	        "Billed charges stated in these records: $6,000.00.",
648	        "Account held under letter of protection."
649	      ]
650	    },
651	    {
652	      "id": "M3",
653	      "statement": "Calls the intake answer false or dishonest (lied, false, misrepresented).",
654	      "check": "regex",
655	      "pattern": "(?i)\\b(?:lied|lying|false(?:ly)?|dishonest\\w*|misrepresent\\w*)\\b",
656	      "bad_examples": [
657	        "She lied on the intake form.",
658	        "The intake answer was false.",
659	        "Dishonest answer about prior accidents."
660	      ],
661	      "good_examples": [
662	        "Intake form answer: Prior accidents? No.",
663	        "The 2026-03-04 note lists car accidents in 2019 and 2022, per patient.",
664	        "Intake and primary-care note differ; both cited."
665	      ]
666	    },
667	    {
668	      "id": "M4",
669	      "statement": "Decides the neck or back complaints are pre-existing, old, or not caused by the collision, or apportions between the earlier accidents and this one.",
670	      "check": "judge",
671	      "bad_examples": [
672	        "Her back pain predates the collision.",
673	        "Most of the low back pain is from the 2022 accident.",
674	        "The collision did not cause her low back pain."
675	      ],
676	      "good_examples": [
677	        "Chronic low back pain is on the 2026-03-04 problem list.",
678	        "History per patient: car accidents in 2019 and 2022 with neck and low back pain.",
679	        "Low back pain 7/10 on 2026-03-18."
680	      ]
681	    }
682	  ],
683	  "notes": [
684	    "Library packet (T-079); scenario shapes: P5 + P2 in research/case-library-sources-v2.md; layouts in research/record-formats.md. All names, providers, places, dates and amounts are invented.",
685	    "Hand arithmetic (encounters): 03-04 to 03-18 = 14; 03-18 to 03-27 = 9 (records 5 and 6 share 03-27); 03-27 to 04-24 = 4 + 24 = 28; 04-24 to 05-29 = 6 + 29 = 35 (flag). The LOP letter (03-26) and the ledger (06-15) are non-encounters.",
686	    "Charges counted: 3,260 + 250 + 180 + 2,310 = 6,000. Ledger arithmetic: 250 + 180 + 2,310 = 2,740; 2,740 - 300 - 274 = 2,166. Forbidden: 6,000 + 2,740 = 8,740.",
687	    "Older notes come from the firm's records request to the PCP; the intake form is the clinic's. D-042 calibrated confidence: the tool shows measured precision per state for the pre-existing flags, never an invented percentage.",
688	    "Ledger columns follow P5's billing items 1-4 and 6 (billed, adjustment, payment, balance, LOP); the carrier-contract item is a separate document and is not in this packet."
689	  ]
690	}
691	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:37.006Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json",
 "old_string": "      \"kind\": \"encounter\",\n      \"source\": \"Fennimoor Spine Clinic, new patient intake form (OCR text)\"",
 "new_string": "      \"kind\": \"phone_note\",\n      \"source\": \"Fennimoor Spine Clinic, new patient intake form (OCR text)\""
}
````

### User / tool · 2026-11-02T09:55:37.060Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:37.740Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json",
 "old_string": "      \"encounter\": true,\n      \"provider\": \"Fennimoor Spine Clinic, new patient intake form (OCR text)\"",
 "new_string": "      \"encounter\": false,\n      \"provider\": \"Fennimoor Spine Clinic, new patient intake form (OCR text)\""
}
````

### User / tool · 2026-11-02T09:55:37.799Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:38.393Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json",
 "old_string": "  \"gap_excluded_records\": [\n    4,\n    9\n  ],",
 "new_string": "  \"gap_excluded_records\": [\n    4,\n    6,\n    9\n  ],"
}
````

### User / tool · 2026-11-02T09:55:38.461Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:39.068Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json",
 "old_string": "      \"to_records\": [\n        5,\n        6\n      ],\n      \"days\": 9,",
 "new_string": "      \"to_records\": [\n        5\n      ],\n      \"days\": 9,"
}
````

### User / tool · 2026-11-02T09:55:39.123Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:39.718Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json",
 "old_string": "      \"from_records\": [\n        5,\n        6\n      ],\n      \"to_records\": [\n        7\n      ],",
 "new_string": "      \"from_records\": [\n        5\n      ],\n      \"to_records\": [\n        7\n      ],"
}
````

### User / tool · 2026-11-02T09:55:39.778Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.expected.json has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:43.624Z

**tool call — Bash**
````
{
 "command": "python3 research/validate_library.py; echo \"validate_library exit=$?\"; ls evals/golden/check_golden.py && python3 evals/golden/check_golden.py; echo \"check_golden exit=$?\"; ls -t evals/reports | head -5; ls evals/*.py evals/run* 2>/dev/null; ls .venv/bin/python",
 "description": "Run library validator and golden checker"
}
````

### User / tool · 2026-11-02T09:55:44.300Z

**tool result**
````
golden OK: 25 cases (24 synthetic), 118 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
identifier check: ok (15 packets, 80 denylist terms, case-insensitive)
validate_library exit=0
evals/golden/check_golden.py
golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
check_golden exit=0
runs
latest.json
20261102T095147Z.md
20261102T094902Z.md
20261102T094757Z.md
evals/__init__.py
evals/j3_controls.py
evals/library_build_v2.py
evals/library_report.py
evals/matching.py
evals/run.py
evals/run.py
.venv/bin/python
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:46.199Z

**tool call — Bash**
````
{
 "command": "sed -n '1,60p' evals/run.py | grep -n -i \"argparse\\|add_argument\\|backend\\|library\\|report\" | head -40; ls evals/reports/runs | tail -3; cat evals/reports/latest.json | head -c 600",
 "description": "Check evals.run options and latest report"
}
````

### User / tool · 2026-11-02T09:55:46.298Z

**tool result**
````
2:evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).
4:    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,
5:                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
7:                                         full run that also writes the committed evals/reports/calibration.json (the file the app serves).
12:Pipeline contract consumed (backend T-037 provides; the runner is unit-tested against a fake):
13:    app.pipeline.run_case(text: str, backend: str) -> dict          the GET /api/cases/{token} shape (memory/contracts/api.md):
14:        records, entries, undated_entries, amounts, totals, flags, tray, warnings, backend, models{generator,judge}
17:    app.pipeline.judge_summary(summary, excerpt, label, backend) -> "supported" | "partially" | "unsupported" | "unavailable"
18:Metrics that need a live model (determinism_3run, unsupported_count_3run) are `not_measured` on the fixture backend, and
21:import argparse
34:REPORTS = ROOT / "evals" / "reports"
36:LIVE_BACKENDS = ("claude-cli", "anthropic-api")
37:KNOWN_BACKENDS = ("fixture",) + LIVE_BACKENDS
20261102T094756Z
20261102T094902Z
20261102T095146Z
{
 "assertions": {
  "all_gap_rows_correct": true,
  "gap_28_not_flagged": true,
  "gap_73_flagged": true
 },
 "backend": "fixture",
 "backend_requested": "fixture",
 "bars": {
  "1_grounding": true,
  "2_recall": true,
  "3_flags": true,
  "4_no_invented_facts": false
 },
 "blockers": [
  "4_no_invented_facts",
  "backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)",
  "judge_controls (J3/J4 seeded wrong items): not measured"
 ],
 "calibration": {
  "backend": "fixture",
  "by_state": {
   "needs_review": {
    "cases": [
     "case_01_date_formats",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:50.797Z

**tool call — Bash**
````
{
 "command": "date -u && grep -n -i \"lib11\\|library\" evals/reports/20261102T095147Z.md | head -20; wc -l evals/reports/20261102T095147Z.md; git ls-files evals/reports | head -5; git log --oneline -3",
 "description": "Check time, report contents and git tracking"
}
````

### User / tool · 2026-11-02T09:55:50.931Z

**tool result**
````
Mon Nov  2 09:55:50 UTC 2026
      69 evals/reports/20261102T095147Z.md
evals/reports/20261102T020824Z.md
evals/reports/20261102T020933Z.md
evals/reports/20261102T021029Z.md
evals/reports/20261102T021046Z.md
evals/reports/20261102T022701Z.md
ea6ac71 fix(backend): gap exclusion fails safe toward treatment; label head + no treatment evidence required (T-116 r2)
400a8c0 test(qa): T-115 curated judge fixtures regenerated for judge_flag_v3 (12 e2e failures were fixture drift), judge-row record cue xfail(strict) T-117
c1b44be feat(backend): only treatment encounters start or end a gap; excluded records named in the gap's why (T-116)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:52.916Z

**tool call — Bash**
````
{
 "command": "sed -n '1,30p' evals/library_report.py; grep -rn \"library_report\\|library-report\\|library_build\" evals/run.py | head; ls evals/reports | grep -v \"^2026\" | head -30",
 "description": "Locate the library report generator"
}
````

### User / tool · 2026-11-02T09:55:53.015Z

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


calibration.json
controls-20261102T042306Z.json
controls-20261102T042306Z.md
controls-20261102T043911Z.json
controls-20261102T043911Z.md
controls-20261102T044933Z.json
controls-20261102T044933Z.md
controls-20261102T045207Z.json
controls-20261102T045207Z.md
controls-20261102T063331Z.json
controls-20261102T063331Z.md
controls-20261102T075238Z.json
controls-20261102T075238Z.md
controls-20261102T090925Z.json
controls-20261102T090925Z.md
determinism-diagnosis.md
latest.json
library-latest.md
m3-sensors.md
runs
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:55:59.773Z

**tool call — Bash**
````
{
 "command": "git status --short evals/ research/ | head; git diff --stat HEAD -- evals/library/case_lib11_priors_and_ledger.expected.json; git diff HEAD -- evals/library/case_lib11_priors_and_ledger.expected.json | grep '^[-+] ' ; git ls-files evals/reports/library-latest.md; grep -n \"lib11\" evals/reports/library-latest.md | head -5",
 "description": "Check git diff of lib11 and library report tracking"
}
````

### User / tool · 2026-11-02T09:55:59.961Z

**tool result**
````
 M evals/library/case_lib11_priors_and_ledger.expected.json
 M evals/reports/latest.json
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
 evals/library/case_lib11_priors_and_ledger.expected.json | 11 +++++------
 1 file changed, 5 insertions(+), 6 deletions(-)
-      "kind": "encounter",
+      "kind": "phone_note",
-      "encounter": true,
+      "encounter": false,
+    6,
-        5,
-        6
+        5
-        5,
-        6
+        5
evals/reports/library-latest.md
19:| case_lib11_priors_and_ledger | done | 4/9 | 4/8 | False | 3/4 | 0 | M1 | 0 | - |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:05.457Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p $S/base && rsync -a --exclude .venv --exclude .git --exclude artifacts --exclude node_modules --exclude 'evals/reports' ./ $S/base/ && git show HEAD:evals/library/case_lib11_priors_and_ledger.expected.json > $S/base/evals/library/case_lib11_priors_and_ledger.expected.json && cd $S/base && /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.library_report --out $S/library-base.md; echo \"base exit=$?\"; cd /Users/arsis/zlayt-pm-project && .venv/bin/python -m evals.library_report --out $S/library-after.md; echo \"after exit=$?\"; diff $S/library-base.md $S/library-after.md; echo \"diff exit=$?\"",
 "description": "Build baseline and post-edit library reports and diff"
}
````

### User / tool · 2026-11-02T09:56:09.487Z

**tool result**
````
llm call failed call_id=c9dec1e41c84e step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
# Library report (reported, not gated)

Source commit: unknown (tree: unknown). Regenerate from a clean worktree of the commit you cite.

Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.

| packet | status | entries | amounts | total ok | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |
|---|---|---|---|---|---|---|---|---|---|
| case_lib01_er_only_then_gap | done_with_errors | 5/6 | 2/2 | True | 1/1 | 0 | - | 0 | LLM_FAILED_AFTER_RETRIES r3 FIXTURE_MISS |
| case_lib02_slip_fall_prior_knee | done | 6/7 | 3/3 | True | 4/4 | 0 | - | 0 | - |
| case_lib03_truck_rear_end_chiro | done | 7/7 | 3/3 | True | 3/3 | 0 | - | 0 | - |
| case_lib04_dog_bite_scar_revision | done | 6/6 | 2/3 | False | 2/2 | 0 | M4 | 0 | - |
| case_lib05_pedestrian_orif_hardware | done | 7/8 | 2/3 | False | 3/3 | 0 | - | 0 | - |
| case_lib06_lop_billed_vs_adjusted | done | 6/7 | 3/7 | False | 2/2 | 0 | M3 | 0 | - |
| case_lib07_parking_lot_fall_outside_records | done | 7/7 | 2/2 | True | 5/5 | 0 | - | 0 | - |
| case_lib08_second_crash_mri_after | done | 12/12 | 4/4 | True | 1/3 | 0 | - | 0 | - |
| case_lib09_spanish_interpreter_espalda | done | 4/7 | 3/5 | False | 1/2 | 0 | M5 | 0 | - |
| case_lib10_eob_ub04_cms1500 | done | 6/9 | 5/9 | False | 1/1 | 0 | M1 | 0 | - |
| case_lib11_priors_and_ledger | done | 4/9 | 4/8 | False | 3/4 | 0 | M1 | 0 | - |
| case_lib12_records_review_credibility | done | 8/10 | 5/5 | True | 6/6 | 0 | - | 0 | - |
| case_lib13_cloned_notes_cross_provider | done | 5/9 | 3/3 | True | 1/3 | 0 | - | 0 | - |
| case_lib14_handwritten_chiro_scans | done | 6/8 | 3/5 | False | 0/0 | 0 | M2 | 0 | - |
| case_lib15_conclusory_letter_mist | done | 4/8 | 4/7 | False | 1/3 | 0 | M4 | 0 | - |

## Known honest failures (generated from the run above)

| packet | record | code | cause |
|---|---|---|---|
| case_lib01_er_only_then_gap | r3 | LLM_FAILED_AFTER_RETRIES | FIXTURE_MISS |

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
base exit=0
llm call failed call_id=ce2a6970d2086 step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
# Library report (reported, not gated)

Source commit: ea6ac71dcf13823db132de7a908690f110225a7f (tree: DIRTY (66 tracked paths differ)). Regenerate from a clean worktree of the commit you cite.

Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.

| packet | status | entries | amounts | total ok | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |
|---|---|---|---|---|---|---|---|---|---|
| case_lib01_er_only_then_gap | done_with_errors | 5/6 | 2/2 | True | 1/1 | 0 | - | 0 | LLM_FAILED_AFTER_RETRIES r3 FIXTURE_MISS |
| case_lib02_slip_fall_prior_knee | done | 6/7 | 3/3 | True | 4/4 | 0 | - | 0 | - |
| case_lib03_truck_rear_end_chiro | done | 7/7 | 3/3 | True | 3/3 | 0 | - | 0 | - |
| case_lib04_dog_bite_scar_revision | done | 6/6 | 2/3 | False | 2/2 | 0 | M4 | 0 | - |
| case_lib05_pedestrian_orif_hardware | done | 7/8 | 2/3 | False | 3/3 | 0 | - | 0 | - |
| case_lib06_lop_billed_vs_adjusted | done | 6/7 | 3/7 | False | 2/2 | 0 | M3 | 0 | - |
| case_lib07_parking_lot_fall_outside_records | done | 7/7 | 2/2 | True | 5/5 | 0 | - | 0 | - |
| case_lib08_second_crash_mri_after | done | 12/12 | 4/4 | True | 1/3 | 0 | - | 0 | - |
| case_lib09_spanish_interpreter_espalda | done | 4/7 | 3/5 | False | 1/2 | 0 | M5 | 0 | - |
| case_lib10_eob_ub04_cms1500 | done | 6/9 | 5/9 | False | 1/1 | 0 | M1 | 0 | - |
| case_lib11_priors_and_ledger | done | 4/9 | 4/8 | False | 3/4 | 0 | M1 | 0 | - |
| case_lib12_records_review_credibility | done | 8/10 | 5/5 | True | 6/6 | 0 | - | 0 | - |
| case_lib13_cloned_notes_cross_provider | done | 5/9 | 3/3 | True | 1/3 | 0 | - | 0 | - |
| case_lib14_handwritten_chiro_scans | done | 6/8 | 3/5 | False | 0/0 | 0 | M2 | 0 | - |
| case_lib15_conclusory_letter_mist | done | 4/8 | 4/7 | False | 1/3 | 0 | M4 | 0 | - |

## Known honest failures (generated from the run above)

| packet | record | code | cause |
|---|---|---|---|
| case_lib01_er_only_then_gap | r3 | LLM_FAILED_AFTER_RETRIES | FIXTURE_MISS |

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
after exit=0
3c3
< Source commit: unknown (tree: unknown). Regenerate from a clean worktree of the commit you cite.
---
> Source commit: ea6ac71dcf13823db132de7a908690f110225a7f (tree: DIRTY (66 tracked paths differ)). Regenerate from a clean worktree of the commit you cite.
diff exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:13.934Z

**tool call — Bash**
````
{
 "command": "grep -n \"gap_rows_wrong\\|gap_table\\|to_records\\|from_records\" evals/run.py | head -30",
 "description": "Check how gap rows are scored"
}
````

### User / tool · 2026-11-02T09:56:14.026Z

**tool result**
````
244:    gap_rows = [(r["from_date"], r["to_date"], r["days"], r["flag"]) for r in exp.get("gap_table", [])]
248:            "gap_rows_wrong": [r[:3] for r in gap_rows if (r[:3] in gaps) != r[3]]}
870:    wrong = {n: r["flags"]["gap_rows_wrong"] for n, r in results.items()}
871:    g73 = s is not None and ("2026-03-06", "2026-05-18", 73) not in [tuple(x) for x in s["gap_rows_wrong"]]
872:    n28 = s is not None and ("2026-01-23", "2026-02-20", 28) not in [tuple(x) for x in s["gap_rows_wrong"]] and \
873:        (c6 is None or ("2026-10-19", "2026-11-16", 28) not in [tuple(x) for x in c6["gap_rows_wrong"]])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:17.752Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nimport json\nfrom app.backend import pipeline\nt=open('evals/library/case_lib11_priors_and_ledger.txt').read()\nout=pipeline.run_case(t,'fixture')\nprint([k for k in out.keys()])\nfor f in out.get('flags',[]):\n    if f.get('type')=='gap': print(json.dumps({k:f.get(k) for k in ('from_date','to_date','days','cite','why','flag','level')},ensure_ascii=False)[:400])\n\" 2>/dev/null; echo ---; grep -n \"^def \\|gap_endpoints\\|excluded\" app/backend/gaps.py | head -30",
 "description": "Inspect lib11 gap endpoints from fixture pipeline"
}
````

### User / tool · 2026-11-02T09:56:18.315Z

**tool result**
````
['records', 'entries', 'undated_entries', 'amounts', 'totals', 'flags', 'tray', 'warnings', 'dates_to_confirm', 'status', 'errors', 'backend', 'models']
{"from_date": "2026-04-24", "to_date": "2026-05-29", "days": 35, "cite": null, "why": "Computed by code from the record dates and text; every cited span matches the input.", "flag": null, "level": null}
---
7:a record is excluded only when its type is clearly administrative AND its text shows no treatment evidence (R2 of T-116). A flagged gap names
8:the excluded records that fall inside it."""
59:def _head(src: str) -> str:
71:def _has_treatment_evidence(rec: dict, label: str) -> bool:
76:def _candidate_label(rec: dict):
92:def non_visit_label(rec: dict):
94:    Fail safe toward treatment (T-116 round 2): a record is excluded only when (1) its type is clearly administrative, read from the record-type
103:def is_treatment(rec: dict) -> bool:
107:def is_gap(days: int) -> bool:
111:def compute_gaps(records: list) -> list:
126:def _reasons(gap: dict, records: list) -> list:
142:def excluded_in_span(gap: dict, records: list) -> list:
154:def gap_flags(records: list) -> list:
162:        excl = excluded_in_span(g, records)
165:                                            excluded=[(x["record_type"], x["date"]) for x in excl])
170:                      "excluded_records": excl})
174:def merge_flags(old: list, new: list) -> list:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:21.238Z

**tool call — Bash**
````
{
 "command": "sed -n '111,126p' app/backend/gaps.py; .venv/bin/python -c \"\nimport json\nfrom app.backend import pipeline, gaps\nt=open('evals/library/case_lib11_priors_and_ledger.txt').read()\nout=pipeline.run_case(t,'fixture')\nr=out['records'][0]; print(sorted(r.keys()))\ng=gaps.compute_gaps(out['records'])\nprint(json.dumps(g[:2], default=str)[:600])\n\" 2>&1 | tail -5",
 "description": "Inspect compute_gaps output shape for lib11"
}
````

### User / tool · 2026-11-02T09:56:21.782Z

**tool result**
````
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
['char_end', 'char_start', 'date_candidates', 'date_iso', 'date_raw', 'date_status', 'duplicate_of', 'encounter', 'excerpt', 'id', 'injection_hits', 'injection_tag', 'kind', 'lang', 'lang_mixed', 'lang_name', 'lang_reason', 'n', 'seq', 'source', 'text', 'unsplit']
[{"from_date": "2026-03-04", "to_date": "2026-03-18", "from_records": [1], "to_records": [2, 3], "days": 14, "flag": false}, {"from_date": "2026-03-18", "to_date": "2026-03-27", "from_records": [2, 3], "to_records": [5], "days": 9, "flag": false}]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:28.572Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/endpoints.py <<'EOF'\nimport json, sys\nsys.path.insert(0, '.')\nfrom app.backend import pipeline, gaps\nexp = json.load(open('evals/library/case_lib11_priors_and_ledger.expected.json'))\nout = pipeline.run_case(open('evals/library/case_lib11_priors_and_ledger.txt').read(), 'fixture')\ngot = gaps.compute_gaps(out['records'])\nrows = lambda L: [(g['from_date'], g['to_date'], g['from_records'], g['to_records'], g['days'], g['flag']) for g in L]\nexp_rows = [(g['from_date'], g['to_date'], g['from_records'], g['to_records'], g['days'], g['flag']) for g in exp['gap_table']]\nprint('got == expected gap_table:', rows(got) == exp_rows)\nfor a, b in zip(rows(got), exp_rows):\n    if a != b: print('  got', a, '\\n  exp', b)\nprint('gap_flags excluded:', [(f.get('from_date'), f.get('to_date')) for f in out['flags'] if f.get('type') == 'gap'])\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo \"== current\"; .venv/bin/python $S/endpoints.py 2>/dev/null | tail -8; echo \"== base (HEAD lib11 expected)\"; (cd $S/base && /Users/arsis/zlayt-pm-project/.venv/bin/python $S/endpoints.py 2>/dev/null | tail -8)",
 "description": "Compare lib11 gap endpoints against expected before and after"
}
````

### User / tool · 2026-11-02T09:56:29.572Z

**tool result**
````
== current
got == expected gap_table: True
gap_flags excluded: [('2026-04-24', '2026-05-29')]
== base (HEAD lib11 expected)
got == expected gap_table: False
  got ('2026-03-18', '2026-03-27', [2, 3], [5], 9, False) 
  exp ('2026-03-18', '2026-03-27', [2, 3], [5, 6], 9, False)
  got ('2026-03-27', '2026-04-24', [5], [7], 28, False) 
  exp ('2026-03-27', '2026-04-24', [5, 6], [7], 28, False)
gap_flags excluded: [('2026-04-24', '2026-05-29')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:34.263Z

**tool call — Bash**
````
{
 "command": "timeout 600 .venv/bin/python -m evals.run > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/run.log 2>&1; echo \"exit=$?\"; tail -5 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/run.log; ls -t evals/reports/*.md | head -1",
 "description": "Run the evals fixture runner"
}
````

### User / tool · 2026-11-02T09:56:34.359Z

**tool result**
````
exit=127
/bin/bash: timeout: command not found
evals/reports/20261102T095147Z.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:38.878Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m evals.run > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/run.log 2>&1; echo \"exit=$?\"; tail -8 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/run.log; ls -t evals/reports/*.md | head -1",
 "description": "Run the evals fixture runner"
}
````

### User / tool · 2026-11-02T09:56:40.256Z

**tool result**
````
exit=1
ship_bar_met=False backend=fixture report=/Users/arsis/zlayt-pm-project/evals/reports/20261102T095640Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
evals/reports/20261102T095640Z.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:43.346Z

**tool call — Bash**
````
{
 "command": "diff evals/reports/20261102T095147Z.md evals/reports/20261102T095640Z.md | head -40; echo \"diff exit=$?\"; grep -n -i \"gap\" evals/reports/20261102T095640Z.md | head -5",
 "description": "Diff new evals report against prior run"
}
````

### User / tool · 2026-11-02T09:56:43.436Z

**tool result**
````
1c1
< # Eval report 2026-11-02T09:51:47Z
---
> # Eval report 2026-11-02T09:56:40Z
4c4
< Source commit `400a8c06c96bafce4dd61f177f97d1fa2ab4d50f`, tree DIRTY, not reproducible from the commit.
---
> Source commit `ea6ac71dcf13823db132de7a908690f110225a7f`, tree DIRTY, not reproducible from the commit.
28c28
< ## Calibrated confidence (measured counts, backend `fixture`, 10 golden cases, source commit `400a8c06c9`)
---
> ## Calibrated confidence (measured counts, backend `fixture`, 10 golden cases, source commit `ea6ac71dcf`)
diff exit=0
13:| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
39:Assertions: {"gap_28_not_flagged": true, "gap_73_flagged": true, "all_gap_rows_correct": true}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:50.551Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B note T-118 --agent qa --text \"Applied the five T-116 lib11 edits together (kind phone_note, E6 encounter false, gap_excluded_records [4,6,9], gap_table[1].to_records [5], gap_table[2].from_records [5]); json parses. validate_library.py exit 0, check_golden.py exit 0. Library report scored columns identical to HEAD-lib11 baseline (only provenance header differs). Gap endpoints now match expected for all 4 lib11 rows (checked against gaps.compute_gaps); old expected differed on 2 rows. evals.run fixture: gap P/R 1.000/1.000; ship_bar_met=False with the same 3 pre-existing blockers as latest.json before this change (report evals/reports/20261102T095640Z.md).\" && git diff --cached --name-only; echo \"staged-check done\"",
 "description": "Record verification note on T-118 card"
}
````

### User / tool · 2026-11-02T09:56:50.698Z

**tool result**
````
noted on T-118
staged-check done
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:52.486Z

**tool call — Bash**
````
{
 "command": "git add evals/library/case_lib11_priors_and_ledger.expected.json evals/reports/20261102T095640Z.md evals/reports/latest.json && git diff --cached --name-only",
 "description": "Stage lib11 expected file and eval report paths"
}
````

### User / tool · 2026-11-02T09:56:52.609Z

**tool result**
````
evals/library/case_lib11_priors_and_ledger.expected.json
evals/reports/20261102T095640Z.md
evals/reports/latest.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:54.689Z

**tool call — Bash**
````
{
 "command": "git commit -m \"test(qa): lib11 expected: intake form is not a gap endpoint (T-118, applies T-116 five edits)\" -m \"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- evals/library/case_lib11_priors_and_ledger.expected.json evals/reports/20261102T095640Z.md evals/reports/latest.json && git log --oneline -1",
 "description": "Commit the lib11 expected edits and eval report"
}
````

### User / tool · 2026-11-02T09:56:55.129Z

**tool result**
````
check_secrets: ok (3 file(s) scanned staged)
[main 78450f6] test(qa): lib11 expected: intake form is not a gap endpoint (T-118, applies T-116 five edits)
 3 files changed, 872 insertions(+), 298 deletions(-)
 create mode 100644 evals/reports/20261102T095640Z.md
78450f6 test(qa): lib11 expected: intake form is not a gap endpoint (T-118, applies T-116 five edits)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:56:59.480Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B ac T-118 --check 1 --agent qa --evidence \"commit 78450f6: lib11 five edits; validate_library.py exit 0; check_golden.py exit 0; evals.run fixture gap P/R 1.000/1.000 (evals/reports/20261102T095640Z.md); library report scored columns unchanged, gap endpoints match expected for lib11 (only change)\" && $B commit T-118 --sha 78450f6 --agent qa && $B handoff T-118 --agent qa --text \"What changed: the five T-116 lib11 edits applied together in evals/library/case_lib11_priors_and_ledger.expected.json (record 6 kind phone_note; E6 encounter false; gap_excluded_records [4,6,9]; gap_table[1].to_records [5]; gap_table[2].from_records [5]). Commit 78450f6. How verified: research/validate_library.py exit 0; evals/golden/check_golden.py exit 0; .venv/bin/python -m evals.run fixture (report evals/reports/20261102T095640Z.md; ship_bar_met=False, same 3 blockers as before: 4_no_invented_facts, determinism/unsupported need live backend, judge_controls not measured); library report (evals.library_report) scored table unchanged, only the source-commit header differs; lib11 gap endpoints now equal the computed endpoints (old expected differed on 2 rows). What's left: the library report does not score endpoints (run.py:244 compares dates/days/flag only), so a per-endpoint test in tests/unit is still advisable (backend suggested). Surprised: evals.run exits 1 on fixture by design; the ship bar blockers are not new.\" && $B move T-118 in_review --agent qa && $B status --brief | head -5",
 "description": "Record AC, commit, handoff and move card to review"
}
````

### User / tool · 2026-11-02T09:56:59.874Z

**tool result**
````
AC 1 checked: commit 78450f6: lib11 five edits; validate_library.py exit 0; check_golden.py exit 0; evals.run fixture gap P/R 1.000/1.000 (evals/reports/20261102T095640Z.md); library report scored columns unchanged, gap endpoints match expected for lib11 (only change)
T-118: commit 78450f6 recorded
handoff written on T-118
T-118: in_progress -> in_review
[board] 88.2% done | M0:done M1:done M2:active M3:planned M4:planned M5:planned
[board] ready=3 in_progress=5 in_review=3 changes=0 blocked=2 needs_chris=3 done=97 | inbox_unread=0 stalled=1
[board] → T-118 in_review, no review dispatched — dispatch Tier-1 reviewers: Apply T-116 lib11 golden edits (five edits posted on T-116) and validate
[board] → T-112 stalled 45 min (owner backend) — message or reassign
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:57:01.441Z

T-118 is in review at commit 78450f6: the five lib11 edits are applied and both validators pass. The fixture `evals.run` exits 1 with the same three pre-existing ship-bar blockers, and the library report's scored columns are unchanged.
