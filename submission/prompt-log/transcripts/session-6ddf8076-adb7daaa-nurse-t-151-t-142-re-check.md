# Subagent: Nurse: T-151 + T-142 re-check (Nurse: T-151 + T-142 re-check)

Source: `agent-adb7daaa9b18a874a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T14:23:16.714Z

As the legal nurse, review T-151 (commits b5f40c0 and 94c30db) and re-check T-142 in /Users/arsis/zlayt-pm-project. Read reviews/T-142-legal-nurse.md and both cards.

Run the app from a `git archive HEAD` copy in your scratchpad on a spare port: fixture backend, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad. On lib08, lib09 (Spanish), lib11 and the sample, check that the Conflicts group:
- names exactly the checks that ran;
- lists skipped checks with plain reasons and record numbers;
- shows notes such as "records predate the accident" as information, never as conflicts;
- always shows a "not checked" line naming side and loss of consciousness;
- when nothing ran, says so with reasons.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-151-legal-nurse.md and reviews/T-142-legal-nurse-r2.md. Each needs a ```json block of real values: card, persona legal-nurse-reviewer, model claude-sonnet-5-5, verdict, findings, exercised. Stop your server by PID. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:18.647Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/legal-nurse.md"
}
````

### User / tool · 2026-11-02T14:23:18.655Z

**tool result**
````
1	# Persona dossier — legal-nurse-reviewer
2	
3	## 1. Identity
4	**Linda Chen, RN (fictional), Legal Nurse Consultant (LNCC-style certification), independent consultant to PI and defense firms — 22 years nursing (ER, ortho), 10 as an LNC.**
5	Firms hire her to read records the way a clinician does and to tell attorneys what the records do and do not say. Her reputation depends on never overstating a finding; she has watched demands fall apart because someone turned "may represent" into "is". She wants extraction strictly separate from interpretation.
6	
7	## 2. Day-to-day context
8	- Tools: PDF records with Bates numbers, her own chronology template, drug and abbreviation references, radiology nomenclature guides.
9	- Pressures: thousands of pages, copy-forward notes, ambiguous abbreviations, attorneys who want a causation answer the records don't give.
10	- A bad day: a summary that upgraded a complaint into a finding, or expanded an abbreviation wrongly, gets quoted back by defense counsel.
11	
12	## 3. Goals and success criteria for this artifact
13	- Every summary preserves the clinical meaning, certainty, and attribution of its excerpt — no added diagnosis, severity, or causation.
14	- Patient reports stay attributed through the record's own markers ("C/O", "Patient reports", "Patient states"); the tool never adds its own subjective/objective labels.
15	- Hedged and degenerative language is preserved verbatim and flagged for the attorney.
16	- Prompts and judges are designed so the model cannot infer what the record does not state.
17	
18	## 4. Review checklist
19	1. Each one-line summary uses only clinical terms present in its excerpt; no new diagnosis appears (e.g., no "whiplash", "radiculopathy", "herniated disc", "TBI" unless written).
20	2. Severity is not escalated or softened: "cervical strain" stays strain; "mild right foraminal narrowing" keeps "mild"; pain scores stay as numbers (7/10, 6/10, 4/10, 3/10).
21	3. "Concussion without loss of consciousness" is preserved in full; "without loss of consciousness" is never dropped.
22	4. Imaging terminology is exact: "disc protrusion" is not changed to "bulge", "herniation", or "extrusion".
23	5. Hedges are kept verbatim: "may represent degenerative change; correlate clinically" is neither converted to "degenerative" nor to "traumatic".
24	6. Subjective content is attributed: "C/O neck pain 7/10", "Patient reports...", "Patient states..." remain the patient's report, not the provider's finding.
25	7. Measured and imaged results are quoted as written ("CT head negative", "Cervical range of motion reduced approx. 40%", the MRI impression) with no added characterization; the tool does not tag any item "objective" or "subjective" — that classification is clinical judgment.
26	8. Patient-stated causation ("symptoms began after the January collision") is flagged as self-report, not a physician's causation opinion.
27	9. "Low back pain in 2023, resolved" is flagged as prior history; the tool does not decide aggravation vs new injury.
28	10. "New onset pain radiating to right arm with numbness in fingers" after the gap is surfaced as new symptoms; the tool does not link it to the C5-C6 finding as cause.
29	11. Orders and recommendations are not reported as completed: "MRI ordered" (then performed 05-29 per record 8), "Recommend cervical epidural steroid injection" (not performed in records).
30	12. Medications are reported as written ("Rx cyclobenzaprine 10 mg") with no added frequency, indication, or cost.
31	13. Abbreviations are expanded only when unambiguous (Dx, Rx, C/O, PCP, ER, PT = physical therapy in context); ambiguous ones are left as written or flagged.
32	14. Approximations stay approximate: "approx. 35 mph", "approx. 40%" keep "approx."
33	15. Plan-of-care vs actual: "12 visits" planned vs discharge at visit 9 is surfaced; the tool does not infer how many visits occurred.
34	16. The faithfulness judge prompt explicitly checks for added diagnosis, severity, causation, and certainty changes, and sees only the record and the candidate.
35	17. The generator prompt instructs: quote, don't infer; leave a field empty rather than guess.
36	18. Lexicon entries feeding the `pre_existing` and `causation` flags (D-013) include radiology hedges ("may represent", "cannot be excluded", "possible", "correlate clinically", "degenerative", "chronic") with rationale.
37	19. Nothing in the UI or export gives a medical opinion (prognosis, permanency, necessity) not stated in a record.
38	
39	## 5. Red flags / dealbreakers
40	Each item here is a **blocker** (rate it so; never major or minor).
41	- Any inferred diagnosis, causation, or severity in a summary or export.
42	- A hedge converted into a conclusion in either direction.
43	- A patient report recast as a provider finding, or the tool adding its own subjective/objective labels.
44	- "Without loss of consciousness" dropped from the concussion diagnosis.
45	
46	## 6. Vocabulary
47	LNC, medical chronology, records summary, DOS, HPI, CC, C/O, Dx, Rx, Hx/PMH, SOAP (subjective/objective/assessment/plan), ROM, LOC, A&O, NAD, impression, findings, "correlate clinically", hedge, disc bulge/protrusion/extrusion/sequestration, foraminal narrowing, degenerative disc disease, radiculopathy, aggravation of pre-existing, new onset, plan of care, copy-forward.
48	
49	## 7. How I review
50	1. Read the nine sample records myself and mark each clause S (subjective), O (objective), A (assessment/diagnosis), P (plan).
51	2. In the app (or the pipeline CLI output), compare each summary to its excerpt clause by clause; mark any added, dropped, or changed term, certainty, or attribution.
52	3. Read the generator and judge prompts in `app/llm/prompts/`; check they forbid inference and that the judge checks diagnosis/severity/causation/certainty.
53	4. Review `app/llm/lexicon.yaml` (if in scope) for clinical accuracy of each phrase and rationale.
54	5. If a stress case is available (the "tempted to infer a diagnosis" record), run it and check the output.
55	6. File findings with the summary text and the excerpt side by side.
56	
57	## 8. Calibration
58	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
59	- **blocker — Diagnosis inferred.** Evidence: record 7 summary "Cervical radiculopathy, MRI ordered." Excerpt says "New onset pain radiating to right arm with numbness in fingers." Fix: "New onset right arm radiating pain with finger numbness; pain 7/10; MRI ordered." Test: judge flags "radiculopathy" as unsupported.
60	- **blocker — LOC qualifier dropped (changes the diagnosis).** Evidence: record 2 summary "Dx: cervical strain; concussion." Fix: keep "concussion without loss of consciousness." Test: golden summary check.
61	- **blocker — Order reads as result (states a fact the record does not).** Evidence: record 7 summary "MRI performed." Fix: "MRI ordered" (results appear in record 8).
62	- **major — Judge cannot catch certainty changes (no wrong output observed yet).** Evidence: `app/llm/prompts/judge_faithfulness.md` asks only "is the summary supported?" and never mentions hedges, severity, or attribution. Fix: add explicit checks for added diagnosis, severity change, dropped hedge ("may represent"), and self-report recast as finding. Test: seeded summary "MRI shows degenerative change" is judged unsupported.
63	
64	## 9. Sources
65	- https://web.archive.org/web/20250526092029/https://www.aalnc.org/Portals/0/Docs/Certification/Legal%20Nurse%20Consulting_A%20Nursing%20Specialty_Final_2018.pdf — AALNC, Legal Nurse Consulting: A Nursing Specialty (4th ed., 2018, archived): LNCs analyze records for pre-existing conditions and completeness; scope excludes practicing law.
66	- https://pmc.ncbi.nlm.nih.gov/articles/PMC4464797/ — Brinjikji et al., AJNR 2015: disc bulges/protrusions/degeneration are common in asymptomatic people and rise with age.
67	- https://pubmed.ncbi.nlm.nih.gov/8208267/ — Jensen et al., NEJM 1994: bulges and protrusions in asymptomatic adults "may frequently be coincidental."
68	- https://pubmed.ncbi.nlm.nih.gov/24768732/ — Fardon et al., Lumbar Disc Nomenclature 2.0 (Spine J 2014): standard terms distinguish bulge/protrusion/extrusion; degeneration and trauma are separate categories.
69	- https://pubmed.ncbi.nlm.nih.gov/32813098/ — Callen et al., J Digit Imaging 2020: radiologists' use of uncertainty terms varies widely and is not explained by experience.
70	- https://pubmed.ncbi.nlm.nih.gov/27065212/ — Panicek & Hricak, AJR 2016: hedge phrases are ambiguous; proposes a standardized certainty lexicon.
71	- https://www.auntminnieeurope.com/clinical-news/article/15646568/banned-top-8-words-or-phrases-to-avoid-in-radiology-reports — on Baker, Eur J Radiol 2013: phrases like "may represent", "cannot be excluded", "clinical correlation" are vague hedges.
72	- https://pubmed.ncbi.nlm.nih.gov/29489268/ — StatPearls, SOAP Notes: subjective/objective/assessment/plan as the standard frame of a clinical note.
73	- https://www.tavrn.ai/blog/medical-chronology-mistakes — Tavrn (vendor): misread abbreviations, entry-time vs event-time dates, missing cites are common chronology errors.
74	- Assumptions: Fardon nomenclature is lumbar but its term definitions are used for cervical reports in practice; no current public AALNC chronology template was found (archive links dead).
75	
76	## 10. Limits
77	Do not give causation or medical-necessity opinions about the fictional patient. Do not grade UI, code structure, legal strategy, or billing law. Judge only whether the tool preserves what the records say.
78	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:19.040Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-142-legal-nurse.md"
}
````

### User / tool · 2026-11-02T14:23:19.047Z

**tool result**
````
1	# T-142 legal-nurse review (legal-nurse-reviewer, Linda Chen, RN, LNC persona)
2	
3	Verdict: **changes** (0 blockers, 1 major, 3 minors). Pinned commit 07c7558 (HEAD at review start; contains c5c18a6). I ran `git archive 07c7558` into the scratchpad (`r2-07c7558`) and served it on 127.0.0.1:7931 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratchpad DB. The server (PID 11479) was stopped by PID: `lsof` exit 1, curl 000. Scripts, screenshots and outputs: `artifacts/review-evidence/T-142-legal-nurse/`. This is a read of what the tool tells the reader about coverage, not a clinical opinion on any record.
4	
5	## What the card asked, and what I saw
6	
7	GATE-M2 major 1 was "No conflicts found." as an all-clear on lib09 (left shoulder in the ED note, right shoulder everywhere after) and lib08 (loss of consciousness denied, then stated).
8	
9	- **Empty state: fixed.** lib09, lib08 and lib02 all read "No conflicts found among the kinds checked. Other kinds of conflict are not checked." with the coverage block open (`n1-run.stdout.txt`; `n1-lib08-conflict-group.png`). A bare "No conflicts found." appears nowhere.
10	- **Text comes from the API, so it cannot drift.** For the sample case, lib09, lib08 and lib02 the checked items and not-checked items on screen are identical to `GET /api/cases/{token}` `checks` (`"UI checked == API labels: True ; UI not_checked == API: True"` four times). The real backend sends `checks` at this commit (`present.py:317`), so the real-backend variant of the test now runs; 23 passed from the archive (`n0-e2e-run.txt`).
11	- **lib09 (the left/right case):** the not-checked list now says "Left versus right across records (checked only inside one summary)". That discloses the gap I raised.
12	- **Sample case with two conflicts** (accident date; plan vs discharge): both cards show with both excerpts. The coverage block is collapsed and its heading reads "What the conflict check covers (4 kinds checked)" (`n1-sample-conflict-group.png`). After I dismissed both, the group reads "No open conflicts among the kinds checked (2 dismissed, below). Other kinds are not checked." (`n1-run.stdout.txt` line 32).
13	- **Fallback with no `checks`:** read from `flags.js:84-86`; covered by the card's route-stub tests. I did not run the UI against a server with `checks` removed.
14	
15	## Findings
16	
17	**F-1 (major). On a Spanish case the panel says the denial and plan checks were run; the code that runs them reads English only.** lib09 lists as checked: "A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record" and "A stated plan of care ... against a later record where the course ended early". The Spanish case's panel is word for word the same as the English cases' (`n1-run.stdout.txt`, lib09 block), and the conflict group has no word about language (`n4-lib09-body.py`: "CONFLICT GROUP mentions English/Spanish: False"). The matchers are English regexes: `_DENIAL` ("denies|denied ... prior|previous", "no prior ..."), `_FORM_STEM` ("Prior accidents?") in `app/backend/conflict_candidates.py:44-50`; `grep -i "niega|spanish|language"` on that file and `conflicts.py` finds nothing. I probed `history_denials` in process on the archive (`n3-spanish-denial-probe.py`, output `n3-spanish-denial-probe.out.txt`):
18	
19	```
20	EN control: denies prior / prior knee surgery        candidates=1
21	EN form control: Prior accidents? No [X]             candidates=1
22	ES denial: Niega lesiones previas en la espalda      candidates=0
23	ES form: Accidentes anteriores? No [X] vs accidente previo   candidates=0
24	ES form vs English prior                             candidates=0
25	```
26	
27	lib09 record 4 is exactly that form ("Accidentes anteriores? Si [ ] No [X]"). A reader of the Spanish case is told a denial check ran and found none. It never read the Spanish. This is the same kind of unsupported assurance as the original major, narrower in scope: "among the kinds checked" is true only for English wording. Fix: when the case has Spanish records (the `SPANISH_RECORDS` warning already exists), the coverage block must say that the denial and plan checks read English wording only and were not applied to the Spanish records (name them: "Records 2 and 4"), or the backend `checks` must carry a per-case `not_checked` entry for it that the panel prints. Acceptance test: on lib09 the conflict group shows a sentence naming the Spanish records as not covered by the denial and plan-of-care checks; on an English-only case that sentence is absent; unit probe of the Spanish denial lines above either yields a candidate or the sentence is shown.
28	
29	**F-2 (minor). The loss of consciousness case (lib08) is not named in the server's not-checked list.** The card's text for this fix names "side, LOC, ..." and the frontend fallback lists "A change in loss of consciousness history between records" (`flags.js:86`). The list the server actually sends (`conflict_candidates.py:234-241`) has dosage, left versus right, diagnosis, pain score, months, and history from a relative. On lib08 the panel therefore never names the LOC contradiction I raised (r9 "Denies LOC per patient" against r12 "Patient states brief loss of consciousness at the second collision"). The generic sentence "anything not listed above, including these, is not looked for" does cover it, so the panel is honest, but it does not give the reader the item that was found missing. Fix: add `{"type": "loc_history", "label": "A change in loss of consciousness or other symptom history between records"}` to `NOT_CHECKED`. Acceptance test: lib08's not-checked list contains an LOC line.
30	
31	**F-3 (minor). With conflicts present, the "others are not checked" statement is behind a collapsed disclosure.** Sample case: the visible line is "What the conflict check covers (4 kinds checked)" and nothing says other kinds are not checked until it is opened (`n1-sample-conflict-group.png`; `flags.js:118,121` passes `open` only when the list is empty). The card's AC says the empty state and the conflict panel both say it. Fix: make the closed summary read "What the conflict check covers (4 kinds checked; others are not checked)". Acceptance test: the summary text contains "not checked" with conflicts present.
32	
33	**F-4 (minor). The export's internal notes carry no coverage line.** For lib09 and lib08, with all entries accepted, the notes headings are FLAGS ACCEPTED, FLAGS DISMISSED, AMOUNTS NOT TOTALED, RECORDS NOT IN THE TREATMENT SECTION, EDITED ITEMS, PENDING ITEMS NOT INCLUDED, and nothing mentions conflicts or what was checked (`n5-export-notes.out.txt`: "lines mentioning conflict/checked in letter+notes: []"). My GATE-M2 fix asked for the sentence on the empty state, the internal notes and the CLI. The card's AC covers only the screen, so this is outside the AC as written; it is the same silence once she leaves the screen. Fix: one internal-notes line, "Conflict check covered: ...; not checked: ...", from the same `checks`. Acceptance test: lib09 export notes contain that line.
34	
35	## What I ran
36	
37	1. `git rev-parse --short HEAD` gave 07c7558; `git archive 07c7558 | tar -x` into `r2-07c7558` in the scratchpad (my first extract landed in the scratchpad root by mistake; no repo file was touched); server on 7931; curl 200.
38	2. `n1-conflict-coverage.py`: sample case (pasted), lib09, lib08 and lib02 (library entries) in a browser at 1440x900. Read the Conflicts group: heading, empty line, coverage open or closed, checked and not-checked items; compared with `GET /api/cases/{token}` `checks`; on the sample dismissed both conflicts and re-read the group.
39	3. `n2-types-fired.py`: all 15 library cases through the API: 14 had no conflict flag; only lib11 had two "Records differ on a fact". So in the fixture set no library case shows the provider-name rule firing; I could not confirm that checked kind from a case.
40	4. `n3-spanish-denial-probe.py`: `conflict_candidates.history_denials` in process on the archive, English controls against Spanish wording.
41	5. `n4-lib09-body.py`: lib09 page text searched for any language caveat near conflicts.
42	6. `n5-export-notes.py`: lib09 and lib08, accept every entry, GET export, search letter and notes for conflict or checked wording.
43	7. `tests/e2e/test_conflict_coverage.py` and `test_edit_to_check.py` from the archive with plain pytest: 23 passed.
44	8. Read: `reviews/GATE-M2-legal-nurse.md`, `app/frontend/flags.js`, `app/backend/conflict_candidates.py`, card T-142 and its handoff. Screenshots read: `n1-lib08-conflict-group.png`, `n1-sample-conflict-group.png`.
45	
46	```json
47	{"card": "T-142", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
48	 "scope": "git archive 07c7558 (HEAD at review start; includes c5c18a6) served on http://127.0.0.1:7931 (PID 11479, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; sample case plus library cases case_lib09_spanish_interpreter_espalda, case_lib08_second_crash_mri_after, case_lib02_slip_fall_prior_knee; all 15 library cases through the API",
49	 "exercised": [
50	  "git archive 07c7558 into a fresh scratchpad dir; server on 7931 under .venv/bin/python -I with the T-060 pass-4 launcher; curl 200; stopped by PID 11479 (lsof exit 1, curl 000)",
51	  "browser at 1440x900: sample (pasted), lib09, lib08, lib02; Conflicts group text, coverage block open or closed, checked and not-checked items compared with GET /api/cases/{token} checks (n1-conflict-coverage.py)",
52	  "sample case: dismissed both conflict flags and re-read the group text (n1-sample-after-dismiss.png)",
53	  "all 15 library cases created and run through the API; conflict flags and presence of checks listed (n2-types-fired.py)",
54	  "in-process probe of conflict_candidates.history_denials with English controls and Spanish denial and form wording (n3-spanish-denial-probe.py)",
55	  "lib09 page text searched for a language caveat near the conflict group (n4-lib09-body.py)",
56	  "lib09 and lib08 with every entry accepted: GET export, letter and internal notes searched for conflict or checked wording (n5-export-notes.py)",
57	  "tests/e2e/test_conflict_coverage.py and test_edit_to_check.py from the archive with plain pytest: 23 passed",
58	  "read reviews/GATE-M2-legal-nurse.md, app/frontend/flags.js, app/backend/conflict_candidates.py, card T-142; screenshots n1-lib08-conflict-group.png and n1-sample-conflict-group.png. Not exercised: UI with checks removed from GET case (fallback read from code only); live-model behavior (fixture backend only)"
59	 ],
60	 "verdict": "changes",
61	 "scores": {"conflict_coverage_disclosure": 3, "empty_state_honesty": 5, "api_sourced_text": 5, "spanish_honesty": 2, "no_inferred_dx_severity_causation": 5},
62	 "findings": [
63	  {"severity": "major", "title": "On a Spanish case the panel lists the denial-vs-history and plan-vs-end checks as run, but they read English wording only",
64	   "evidence": "n1-run.stdout.txt lib09 block: checked list includes 'A denial of prior problems (including a form answered No) against a prior condition...' and the panel is identical to the English cases; n4-lib09-body.py: 'CONFLICT GROUP mentions English/Spanish: False'; app/backend/conflict_candidates.py:44-50 _DENIAL and _FORM_STEM are English regexes, no Spanish terms in conflict_candidates.py or conflicts.py; n3-spanish-denial-probe.out.txt: English controls candidates=1, 'Niega lesiones previas en la espalda' candidates=0, 'Accidentes anteriores? Si [ ] No [X]' candidates=0; lib09 record 4 is that form",
65	   "why_it_matters": "The reader of a Spanish case is told a denial check ran and found nothing when it never read the Spanish. It is the same unsupported assurance as the GATE-M2 major, for Spanish wording.",
66	   "fix": "When the case has Spanish records (SPANISH_RECORDS warning exists), have the coverage block name those records as not covered by the denial and plan-of-care checks, or have the backend checks carry a per-case not_checked entry for it that the panel prints. Do not list them as checked for those records.",
67	   "acceptance_test": "lib09 conflict group contains a sentence naming the Spanish records as not covered by the denial and plan checks; an English-only case does not show it; or the Spanish denial lines in n3-spanish-denial-probe.py yield a candidate."},
68	  {"severity": "minor", "title": "The server's not-checked list does not name loss of consciousness (lib08), though the fallback does",
69	   "evidence": "app/frontend/flags.js:86 FALLBACK_NOT includes 'A change in loss of consciousness history between records'; app/backend/conflict_candidates.py:234-241 NOT_CHECKED has dosage, laterality, diagnosis, pain_score, treatment_duration_months, informant_history; n1-run.stdout.txt lib08 not_checked list has no LOC line",
70	   "why_it_matters": "The lib08 contradiction (r9 'Denies LOC per patient' against r12 'Patient states brief loss of consciousness at the second collision') is the case I raised; the panel covers it only through the generic 'anything not listed above' sentence.",
71	   "fix": "Add a loc_history entry to NOT_CHECKED: 'A change in loss of consciousness or other symptom history between records'.",
72	   "acceptance_test": "GET case checks.not_checked contains an LOC entry and lib08's panel prints it."},
73	  {"severity": "minor", "title": "With conflicts present, 'others are not checked' is behind a collapsed disclosure",
74	   "evidence": "n1-sample-conflict-group.png: closed line 'What the conflict check covers (4 kinds checked)'; app/frontend/flags.js:118,121 open only when the list is empty",
75	   "why_it_matters": "The card says the empty state and the conflict panel both say others are not checked; with two conflicts shown the reader sees only a count.",
76	   "fix": "Closed summary: 'What the conflict check covers (4 kinds checked; others are not checked)'.",
77	   "acceptance_test": "Sample case conflict group summary text contains 'not checked'."},
78	  {"severity": "minor", "title": "Export internal notes carry no coverage line (outside the AC as written)",
79	   "evidence": "n5-export-notes.out.txt: lib09 and lib08 'lines mentioning conflict/checked in letter+notes: []'; reviews/GATE-M2-legal-nurse.md fix asked for the empty state, internal notes and CLI",
80	   "why_it_matters": "Once she leaves the screen, the notes say nothing about what the conflict check covered.",
81	   "fix": "One internal-notes line from the same checks: 'Conflict check covered: ...; not checked: ...'.",
82	   "acceptance_test": "lib09 export internal_notes_text contains that line."}
83	 ],
84	 "whats_right": [
85	  "The empty state never says a bare 'No conflicts found.'; it reads 'among the kinds checked. Other kinds of conflict are not checked.' and the coverage list opens by default.",
86	  "On the sample, lib09, lib08 and lib02 the on-screen checked and not-checked items equal GET case checks word for word, so the text cannot drift.",
87	  "lib09's not-checked list now says 'Left versus right across records (checked only inside one summary)', which discloses the gap I raised."
88	 ],
89	 "questions_for_chris": []}
90	```
91	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:19.462Z

**tool call — Bash**
````
{
 "command": "cat board/cards/T-151.md board/cards/T-142.md; git log --oneline | head -8; git show --stat b5f40c0 94c30db | head -40"
}
````

### User / tool · 2026-11-02T14:23:19.602Z

**tool result**
````
---
id: "T-151"
title: "UI: render checks.skipped[] (why a check did not run for this case) and checks.notes[] ('N records predate the stated accident date') in the Conflicts group (T-141 r2 follow-up to T-142)"
milestone: "M2"
role: "frontend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T13:44:15Z"
updated_at: "2026-11-02T14:22:59Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T14:06:17Z"
rounds: 0
commits: ["94c30db", "b5f40c0"]
reviews: []
ac:
  - {"n": 1, "text": "the Conflicts group lists each skipped check with its plain reason and shows notes as info, never as conflicts; e2e on lib11 and a Spanish case", "done": true, "evidence": "tests/e2e/test_conflict_skipped.py 9 pass (lib11 note, lib09 Spanish skipped, stubs, empty conflict_types); test_conflict_coverage 5 pass"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:44:24Z orchestrator: assigned: frontend
- 2026-11-02T14:06:17Z frontend: claimed
- 2026-11-02T14:22:44Z frontend: AC 1 checked: tests/e2e/test_conflict_skipped.py 9 pass (lib11 note, lib09 Spanish skipped, stubs, empty conflict_types); test_conflict_coverage 5 pass
- 2026-11-02T14:22:45Z frontend: moved in_progress -> in_review
- 2026-11-02T14:22:59Z orchestrator: review dispatched: legal-nurse-reviewer

## Handoff
What changed: Conflicts group lists checks.skipped[] (visible box, server reason, 'Records 2, 4 and 7 were not read'), checks.notes[] as info lines (not cards, not counted), always-visible not-checked line naming left versus right and loss of consciousness history, a skipped type is not in Checked, empty conflict_types says 'No conflict checks ran for this case' with reasons and no empty list. · Verified: tests/e2e/test_conflict_skipped.py 9 pass (lib11, lib09 Spanish, stubs); test_conflict_coverage pass. · Left: coverage line in internal notes is backend.
---
id: "T-142"
title: "GATE-M2 major (legal nurse): conflict empty state overclaims ('No conflicts found') though only plan-vs-early-end and denial-vs-history are checked; laterality (lib09 L vs R shoulder) and LOC (lib08) contradictions are not"
milestone: "M2"
role: "frontend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T13:03:14Z"
updated_at: "2026-11-02T14:23:00Z"
claimed_by: "frontend"
claimed_at: "2026-11-02T13:04:03Z"
rounds: 1
commits: ["c5c18a6"]
reviews:
  - {"persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-142-legal-nurse.md", "at": "2026-11-02T13:46:49Z"}
ac:
  - {"n": 1, "text": "empty state and conflict panel name exactly which conflict types are checked and say others (side, LOC, dates of injury mechanism...) are not checked; text sourced from the API (backend lists checked types) so it cannot drift; e2e", "done": true, "evidence": "tests/e2e/test_conflict_coverage.py 4 pass 1 skip (real-backend variant skips until GET case sends checks); words from case.checks {conflict_types, labels, not_checked}"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:03:19Z orchestrator: assigned: frontend
- 2026-11-02T13:04:03Z frontend: claimed
- 2026-11-02T13:36:55Z frontend: AC 1 checked: tests/e2e/test_conflict_coverage.py 4 pass 1 skip (real-backend variant skips until GET case sends checks); words from case.checks {conflict_types, labels, not_checked}
- 2026-11-02T13:36:56Z frontend: moved in_progress -> in_review
- 2026-11-02T13:37:02Z orchestrator: review dispatched: legal-nurse-reviewer
- 2026-11-02T13:46:49Z orchestrator: review legal-nurse-reviewer (claude-sonnet-5-5): changes — reviews/T-142-legal-nurse.md; round 1; findings:
    - [major] On a Spanish case the panel lists the denial-vs-history and plan-vs-end checks as run, but they read English wording only — fix: When the case has Spanish records (SPANISH_RECORDS warning exists), have the coverage block name those records as not covered by the denial and plan-of-care checks, or have the backend checks carry a per-case not_checked entry for it that the panel prints. 
    - [minor] The server's not-checked list does not name loss of consciousness (lib08), though the fallback does — fix: Add a loc_history entry to NOT_CHECKED: 'A change in loss of consciousness or other symptom history between records'.
    - [minor] With conflicts present, 'others are not checked' is behind a collapsed disclosure — fix: Closed summary: 'What the conflict check covers (4 kinds checked; others are not checked)'.
    - [minor] Export internal notes carry no coverage line (outside the AC as written) — fix: One internal-notes line from the same checks: 'Conflict check covered: ...; not checked: ...'.
- 2026-11-02T13:46:49Z orchestrator: Major (Spanish lib09 lists English-only checks as run) is fixed at the source by T-141 r2 (68b8685: checks per case, Spanish records in skipped[]); the UI side (render skipped[] and notes[]) is T-151. Fold the 3 minors into T-151: name LOC/side as not checked, keep the 'others not checked' line visible when conflicts show, add a coverage line to internal notes (backend note if needed).
- 2026-11-02T13:46:49Z orchestrator: moved changes_requested -> blocked: fixed at source by T-141 r2; UI half in T-151; re-check with T-151
- 2026-11-02T14:23:00Z orchestrator: moved blocked -> in_progress
- 2026-11-02T14:23:00Z orchestrator: moved in_progress -> in_review
- 2026-11-02T14:23:00Z orchestrator: review dispatched: legal-nurse-reviewer

## Handoff
What changed (c5c18a6): Conflicts group has conflict-empty ('No conflicts found among the kinds checked. Other kinds of conflict are not checked.') and a conflict-coverage details (open when empty) listing checked kinds and not-checked kinds from GET case checks {conflict_types, labels, not_checked[{type,label}]} (shape from conflict_candidates.checks()); without checks a fixed fallback (plan vs early end, denial vs history, accident date; not checked: left vs right, loss of consciousness history) plus a note. How verified: e2e route stubs (API list, custom list proves no page-written copy, with conflicts, fallback), 4 pass. Left: backend T-141 must add checks to GET case and the api.md contract (not yet emitted at this commit, the real-backend test skips until then). Surprise: the contract had no checks field yet; I used the shape in conflict_candidates.checks().
25f585c fix(frontend): T-136 r3 e2e private server that fails to start stops the run with its log; never falls back to :7860
b5f40c0 fix(frontend): T-151 empty checks.conflict_types says 'No conflict checks ran for this case' with the skipped reasons, never an empty list or 'No conflicts found'
4abec86 fix(backend): T-139 r2 money written without a dollar sign (TOTAL CHARGE 49100, AMOUNT PAID 0 00, 24F, FL47) is held out and caught by an independent letter check; Bills to request lists treating providers only; the held-out hint offers only actions that clear it
e2bb025 test(frontend): declare data-entry-id and data-flag in the e2e hook contract (T-144, T-154)
611bdcc feat(frontend): T-154 charges are never batch-accepted (note + CHARGES_NOT_BATCHED message); a flagged charge shows its flag and accepts only through a named confirm
f262223 fix(frontend): T-144 the uncovered list opens from a short link in the entry head so compact rows keep their height
ad8b7d1 fix(backend): T-141 r3 pre-accident records are info-only only without injury/mechanism vocabulary; checks notes computed at read time; no stored summary = not run
2a6f40b docs(orchestrator): D-060 charge candidates are default-deny (amends D-059)
commit b5f40c0497f89a5e3f475518255d20eae7caf575
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:22:13 2026 -0600

    fix(frontend): T-151 empty checks.conflict_types says 'No conflict checks ran for this case' with the skipped reasons, never an empty list or 'No conflicts found'
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/frontend/flags.js              | 15 ++++++++++-----
 tests/e2e/test_conflict_skipped.py | 33 +++++++++++++++++++++++++++++++++
 2 files changed, 43 insertions(+), 5 deletions(-)

commit 94c30dbb3152bd021e6ea363b9af199b710445e7
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:05:44 2026 -0600

    feat(frontend): T-151 Conflicts group lists checks.skipped[] with the server's reason and records, shows checks.notes[] as info (not conflicts), keeps the not-checked line visible; a skipped type is not listed as checked
    
    e2e tests/e2e/test_conflict_skipped.py on lib11 (note), lib09 Spanish (three checks only partly ran) and route stubs for the other reason codes.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/frontend/flags.js              |  31 +++++--
 app/frontend/review.css            |   7 ++
 tests/e2e/conftest.py              |   2 +
 tests/e2e/test_conflict_skipped.py | 166 +++++++++++++++++++++++++++++++++++++
 4 files changed, 201 insertions(+), 5 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:20.195Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/legal-nurse-reviewer/project_gate_m2_0c24f5f.md"
}
````

### User / tool · 2026-11-02T14:23:20.204Z

**tool result**
````
1	---
2	name: gate-m2-0c24f5f
3	description: GATE-M2 legal-nurse review at 0c24f5f (verdict changes); recurring gap patterns in conflict coverage and quote omissions, plus how I ran the app
4	metadata:
5	  type: project
6	---
7	
8	GATE-M2 at 0c24f5f: verdict changes (0 blocker, 2 major, 2 minor, 1 nit). Sample case is clinically faithful (LOC, hedge, approx., attribution all kept). Majors: (1) flags.js empty state "No conflicts found." although SCOPE_CUTS row 13 says laterality / LOC-history conflicts are never raised (lib09 left vs right shoulder, lib08 LOC denied vs stated); (2) entries drop unflagged clinical sentences (lib09 r6 "Pain 5/10", interpreter lines, case_06 E3 baseline history) and no code check compares record numbers to the quote.
9	
10	**Why:** quote selection is the model's, judge says "Missing detail alone is fine", and conflict candidates are code-only with three rule types.
11	
12	**How to apply:** in later rounds re-check (a) the empty-state/coverage sentence, (b) a record-number-not-quoted check, (c) lexicon "since the <collision> of <date>". Method: fixture backend + FIXTURE_SET=curated serves library cases too (recorded); launch the app with a tiny launcher script (`python -I launch.py` that sys.path.inserts the archive and chdirs) since `-I` hides cwd; board-guard blocks heredoc redirects that use shell variables, so cd to the scratch dir and use relative paths. POST /api/cases {"library": id} works only with ZLAYT_MODE=local. See [[feedback-spanish-routing-and-cue-gaps]].
13	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:24.068Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git status --short | head -5; ls artifacts/review-evidence/T-142-legal-nurse/; cat artifacts/review-evidence/T-142-legal-nurse/n1-conflict-coverage.py | head -80; ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad | head -30"
}
````

### User / tool · 2026-11-02T14:23:24.313Z

**tool result**
````
25f585c
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
n0-e2e-run.txt
n1-conflict-coverage.out.txt
n1-conflict-coverage.py
n1-lib02-conflict-group-el.png
n1-lib02-conflict-group.png
n1-lib08-conflict-group-el.png
n1-lib08-conflict-group.png
n1-lib09-conflict-group-el.png
n1-lib09-conflict-group.png
n1-run.stdout.txt
n1-sample-after-dismiss.png
n1-sample-conflict-group-el.png
n1-sample-conflict-group.png
n2-types-fired.out.txt
n2-types-fired.py
n3-spanish-denial-probe.out.txt
n3-spanish-denial-probe.py
n4-lib09-body.py
n4-lib09-body.txt
n5-export-notes.out.txt
n5-export-notes.py
"""T-142 legal-nurse check (commit 07c7558, git archive on 127.0.0.1:7931, fixture backend, ZLAYT_MODE=local).
For sample, lib09 (Spanish), lib08 and another library case: open the case as a user, read the Conflicts group (empty line, coverage details, checked/not-checked items),
compare with GET /api/cases/{token} checks, dismiss the conflict flag in the sample case, export notes.
"""
import json
import sys
import urllib.request

from playwright.sync_api import sync_playwright

OUT = "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-142-legal-nurse/"
URL = "http://127.0.0.1:7931/"
SAMPLE = open("/Users/arsis/zlayt-pm-project/evals/golden/sample.txt").read()
LOG = []


def log(m):
    LOG.append(m)
    print(m, flush=True)


def group(pg):
    g = pg.locator("[data-group=conflict]")
    if not g.count():
        return None
    g = g.first
    return {
        "heading": g.locator("h3").inner_text(),
        "empty": g.locator("[data-testid=conflict-empty]").inner_text() if g.locator("[data-testid=conflict-empty]").count() else None,
        "cards": g.locator("[data-flag-id], .rv-flag, article").count(),
        "coverage_open": g.locator("[data-testid=conflict-coverage]").evaluate("(d)=>d.open") if g.locator("[data-testid=conflict-coverage]").count() else None,
        "summary": g.locator("[data-testid=conflict-coverage] summary").inner_text() if g.locator("[data-testid=conflict-coverage]").count() else None,
        "checked": g.locator("[data-testid=conflict-checked-item]").all_text_contents(),
        "not_checked": g.locator("[data-testid=conflict-not-checked-item]").all_text_contents(),
        "note": g.locator("[data-testid=conflict-coverage-note]").all_text_contents(),
        "full": g.inner_text().replace("\n", " | ")[:2500],
    }


def api_checks(tok):
    with urllib.request.urlopen("http://127.0.0.1:7931/api/cases/%s" % tok) as r:
        c = json.loads(r.read())
    return c.get("checks"), [f for f in c.get("flags", []) if f.get("type") == "conflict"]


def open_case(pg, kind):
    pg.goto(URL)
    pg.wait_for_timeout(700)
    if kind == "sample":
        pg.fill("[data-testid=input-text]", SAMPLE)
        pg.click("[data-testid=btn-analyze]")
    else:
        pg.locator("summary:has-text('synthetic library')").first.click()
        pg.wait_for_timeout(300)
        pg.locator("[data-testid=library-%s]" % kind).first.click()
    pg.wait_for_selector("[data-testid=review-counts]", timeout=180000)
    pg.wait_for_timeout(800)
    tok = pg.url.split("/case/")[-1].split("?")[0] if "/case/" in pg.url else None
    return tok


with sync_playwright() as p:
    b = p.chromium.launch()
    for kind in ("sample", "case_lib09_spanish_interpreter_espalda", "case_lib08_second_crash_mri_after", "case_lib02_slip_fall_prior_knee"):
        ctx = b.new_context(viewport={"width": 1440, "height": 900})
        pg = ctx.new_page()
        tok = open_case(pg, kind)
        log("=== %s token=%s" % (kind, tok))
        g = group(pg)
        log("UI group: %s" % json.dumps(g, ensure_ascii=False, indent=1))
        ck, cf = api_checks(tok)
        log("API checks types: %s" % (ck or {}).get("conflict_types"))
        log("API checks labels: %s" % json.dumps((ck or {}).get("labels"), ensure_ascii=False))
        log("API checks not_checked: %s" % json.dumps((ck or {}).get("not_checked"), ensure_ascii=False))
        log("API conflict flags: %s" % [(f["id"], f.get("title") or f.get("summary")) for f in cf])
        # UI items match API
        if ck:
            lab = [ck["labels"].get(t) for t in ck["conflict_types"]]
            log("UI checked == API labels: %s ; UI not_checked == API: %s" % (g["checked"] == lab, g["not_checked"] == [x["label"] for x in ck["not_checked"]]))
        el = pg.locator("[data-group=conflict]").first
641ed.bak
CLAUDE.md
M1
M1_nocombine
M2
M2_find0
MASTER_PROMPT.md
T-047-run1.json
T-060-pass2-head
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
T-124-r1-head
T-124-r1-mut2
T-124-r1-parent
T-133-r1-archive
T-133-r1-source
T-133-r3-archive-4065ef2
T-133-r3-archive-f939ccb
T-133-r3-mutA
T-133-r3-mutB
T-133-r3-mutC
T-133-r3-mutD
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:24.338Z

**tool call — Bash**
````
{
 "command": "git show b5f40c0 94c30db -- app/frontend/flags.js app/frontend/review.css | head -200"
}
````

### User / tool · 2026-11-02T14:23:24.465Z

**tool result**
````
commit b5f40c0497f89a5e3f475518255d20eae7caf575
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:22:13 2026 -0600

    fix(frontend): T-151 empty checks.conflict_types says 'No conflict checks ran for this case' with the skipped reasons, never an empty list or 'No conflicts found'
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/flags.js b/app/frontend/flags.js
index bc05a45..8f866dc 100644
--- a/app/frontend/flags.js
+++ b/app/frontend/flags.js
@@ -105,15 +105,19 @@
   // One line that is always on screen, with or without conflicts: the two kinds the legal nurse named, and everything else not listed under Checked.
   const notCheckedLine = () => el("p", { class: "rv-help rv-notchecked", "data-testid": "conflict-not-checked-line" }, el("strong", {}, "Not checked: "),
     "left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.");
+  // T-151: the server's own list is authoritative even when it is empty: `conflict_types: []` means no conflict check ran on this case (the reasons are in `skipped`). Never an empty list.
+  const hasChecks = (c) => !!(c.checks && Array.isArray(c.checks.conflict_types));
+  const noneRan = (c) => hasChecks(c) && c.checks.conflict_types.length === 0;
+  const NONE_RAN = "No conflict checks ran for this case.";
   function coverage(c, open) {
-    const raw = c.checks, ch = raw && Array.isArray(raw.conflict_types) && (raw.conflict_types.length || (raw.skipped || []).length) ? raw : null;
+    const ch = noneRan(c) || hasChecks(c) ? c.checks : null;
     const skippedTypes = new Set(ch ? (ch.skipped || []).map((x) => x.type) : []);      // a check that did not run (or not on every record) is listed as skipped, never as checked
     const checked = ch ? ch.conflict_types.filter((t) => !skippedTypes.has(t)).map((t) => (ch.labels && ch.labels[t]) || humanType(t)) : FALLBACK_CHECKED;
     const not = ch ? (ch.not_checked || []).map((x) => x.label || humanType(x.type)) : FALLBACK_NOT;
     const d = el("details", { class: "rv-coverage", "data-testid": "conflict-coverage", open: open || null },
-      el("summary", {}, "What the conflict check covers (" + checked.length + (checked.length === 1 ? " kind" : " kinds") + " checked)"),
-      el("p", { class: "rv-help" }, el("strong", {}, "Checked: "), "the code compares records for these kinds of conflict only."),
-      checked.length ? el("ul", { class: "rv-cov-list" }, checked.map((t) => el("li", { "data-testid": "conflict-checked-item" }, t))) : el("p", { class: "rv-help" }, "None ran on every record of this case."),
+      el("summary", {}, "What the conflict check covers (" + (noneRan(c) ? "no checks ran" : checked.length + (checked.length === 1 ? " kind" : " kinds") + " checked") + ")"),
+      el("p", { class: "rv-help" }, el("strong", {}, "Checked: "), noneRan(c) ? NONE_RAN : "the code compares records for these kinds of conflict only."),
+      checked.length ? el("ul", { class: "rv-cov-list" }, checked.map((t) => el("li", { "data-testid": "conflict-checked-item" }, t))) : noneRan(c) ? null : el("p", { class: "rv-help" }, "None ran on every record of this case."),
       el("p", { class: "rv-help" }, el("strong", {}, "Not checked: "), (ch ? "anything not listed above, including these, is not looked for. Read the records for them." : "any other kind of conflict, including these. Read the records for them.")),
       not.length ? el("ul", { class: "rv-cov-list" }, not.map((t) => el("li", { "data-testid": "conflict-not-checked-item" }, t))) : null,
       ch ? null : el("p", { class: "rv-help", "data-testid": "conflict-coverage-note" }, "The server did not send its own list for this case, so this is the standing summary."));
@@ -136,7 +140,8 @@
       if (type === "gap" && ZL.gapChanges) ZL.gapChanges.removed(c).forEach((t) => g.append(el("p", { class: "rv-gap-change", "data-testid": "gap-change-removed" }, t)));
       if (type === "conflict") {
         const dropped = gone.filter((f) => f.type === "conflict").length;
-        if (!list.length) g.append(el("p", { class: "rv-empty", "data-testid": "conflict-empty" }, dropped ? "No open conflicts among the kinds checked (" + dropped + " dismissed, below). Other kinds are not checked." : "No conflicts found among the kinds checked. Other kinds of conflict are not checked."));
+        if (!list.length && noneRan(c)) g.append(el("p", { class: "rv-empty", "data-testid": "conflict-empty" }, NONE_RAN + ((c.checks.skipped || []).length ? " The reasons are listed below." : "")));
+        else if (!list.length) g.append(el("p", { class: "rv-empty", "data-testid": "conflict-empty" }, dropped ? "No open conflicts among the kinds checked (" + dropped + " dismissed, below). Other kinds are not checked." : "No conflicts found among the kinds checked. Other kinds of conflict are not checked."));
       } else if (!list.length) g.append(el("p", { class: "rv-empty" }, empty));
       list.forEach((f) => g.append(card(c, f)));
       if (type === "conflict") g.append(...[notesBox(c.checks), skippedBox(c.checks), notCheckedLine(), coverage(c, !list.length)].filter(Boolean));

commit 94c30dbb3152bd021e6ea363b9af199b710445e7
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:05:44 2026 -0600

    feat(frontend): T-151 Conflicts group lists checks.skipped[] with the server's reason and records, shows checks.notes[] as info (not conflicts), keeps the not-checked line visible; a skipped type is not listed as checked
    
    e2e tests/e2e/test_conflict_skipped.py on lib11 (note), lib09 Spanish (three checks only partly ran) and route stubs for the other reason codes.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/flags.js b/app/frontend/flags.js
index a2cf43f..bc05a45 100644
--- a/app/frontend/flags.js
+++ b/app/frontend/flags.js
@@ -85,14 +85,35 @@
   const FALLBACK_CHECKED = ["A stated plan of care against a later record where the course ended early", "A denial of prior problems against a prior condition, surgery or accident in another record", "A stated accident date against the dates of the records"];
   const FALLBACK_NOT = ["Left versus right across records", "A change in loss of consciousness history between records"];
   const humanType = (t) => { const s = String(t || "").replace(/_/g, " "); return s.charAt(0).toUpperCase() + s.slice(1); };
+  const seqWords = (nos) => (nos.length === 1 ? "Record " + nos[0] + " was" : "Records " + nos.slice(0, -1).join(", ") + " and " + nos[nos.length - 1] + " were");
+  // T-151 (T-141 r2): `checks.skipped[]` says which check did NOT run on this case, or not on every record, in the server's own words; `checks.notes[]` are info lines. Neither is a conflict.
+  function skippedBox(ch) {
+    const sk = ch && Array.isArray(ch.skipped) ? ch.skipped : [];
+    if (!sk.length) return null;
+    return el("div", { class: "rv-skipped", "data-testid": "conflict-skipped" },
+      el("p", { class: "rv-help" }, el("strong", {}, "Did not run on this case, or not on every record (" + sk.length + "): "), "the group above says nothing about these."),
+      el("ul", { class: "rv-cov-list" }, sk.map((x) => el("li", { "data-testid": "conflict-skipped-item", "data-skip-type": x.type, "data-reason-code": x.reason_code || null },
+        el("strong", {}, x.label || humanType(x.type)), " ", x.reason || "",
+        Array.isArray(x.record_nos) && x.record_nos.length ? el("span", { "data-testid": "conflict-skipped-records" }, " " + seqWords(x.record_nos) + " not read.") : null))));
+  }
+  function notesBox(ch) {
+    const ns = ch && Array.isArray(ch.notes) ? ch.notes.filter((n) => n && n.text) : [];
+    if (!ns.length) return null;
+    return el("ul", { class: "rv-notes", "data-testid": "conflict-notes", "aria-label": "Notes about the conflict check, not conflicts" },
+      ns.map((n) => el("li", { class: "rv-note", "data-testid": "conflict-note" }, el("span", { class: "chip chip--info", "data-icon": "info" }, "Note"), " ", n.text)));
+  }
+  // One line that is always on screen, with or without conflicts: the two kinds the legal nurse named, and everything else not listed under Checked.
+  const notCheckedLine = () => el("p", { class: "rv-help rv-notchecked", "data-testid": "conflict-not-checked-line" }, el("strong", {}, "Not checked: "),
+    "left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.");
   function coverage(c, open) {
-    const ch = c.checks && Array.isArray(c.checks.conflict_types) && c.checks.conflict_types.length ? c.checks : null;
-    const checked = ch ? ch.conflict_types.map((t) => (ch.labels && ch.labels[t]) || humanType(t)) : FALLBACK_CHECKED;
+    const raw = c.checks, ch = raw && Array.isArray(raw.conflict_types) && (raw.conflict_types.length || (raw.skipped || []).length) ? raw : null;
+    const skippedTypes = new Set(ch ? (ch.skipped || []).map((x) => x.type) : []);      // a check that did not run (or not on every record) is listed as skipped, never as checked
+    const checked = ch ? ch.conflict_types.filter((t) => !skippedTypes.has(t)).map((t) => (ch.labels && ch.labels[t]) || humanType(t)) : FALLBACK_CHECKED;
     const not = ch ? (ch.not_checked || []).map((x) => x.label || humanType(x.type)) : FALLBACK_NOT;
     const d = el("details", { class: "rv-coverage", "data-testid": "conflict-coverage", open: open || null },
-      el("summary", {}, "What the conflict check covers (" + checked.length + " kinds checked)"),
+      el("summary", {}, "What the conflict check covers (" + checked.length + (checked.length === 1 ? " kind" : " kinds") + " checked)"),
       el("p", { class: "rv-help" }, el("strong", {}, "Checked: "), "the code compares records for these kinds of conflict only."),
-      el("ul", { class: "rv-cov-list" }, checked.map((t) => el("li", { "data-testid": "conflict-checked-item" }, t))),
+      checked.length ? el("ul", { class: "rv-cov-list" }, checked.map((t) => el("li", { "data-testid": "conflict-checked-item" }, t))) : el("p", { class: "rv-help" }, "None ran on every record of this case."),
       el("p", { class: "rv-help" }, el("strong", {}, "Not checked: "), (ch ? "anything not listed above, including these, is not looked for. Read the records for them." : "any other kind of conflict, including these. Read the records for them.")),
       not.length ? el("ul", { class: "rv-cov-list" }, not.map((t) => el("li", { "data-testid": "conflict-not-checked-item" }, t))) : null,
       ch ? null : el("p", { class: "rv-help", "data-testid": "conflict-coverage-note" }, "The server did not send its own list for this case, so this is the standing summary."));
@@ -118,7 +139,7 @@
         if (!list.length) g.append(el("p", { class: "rv-empty", "data-testid": "conflict-empty" }, dropped ? "No open conflicts among the kinds checked (" + dropped + " dismissed, below). Other kinds are not checked." : "No conflicts found among the kinds checked. Other kinds of conflict are not checked."));
       } else if (!list.length) g.append(el("p", { class: "rv-empty" }, empty));
       list.forEach((f) => g.append(card(c, f)));
-      if (type === "conflict") g.append(coverage(c, !list.length));
+      if (type === "conflict") g.append(...[notesBox(c.checks), skippedBox(c.checks), notCheckedLine(), coverage(c, !list.length)].filter(Boolean));
       root.append(g);
     });
     if (gone.length) root.append(RV.dismissedBox("flags", gone.length, el("div", { class: "rv-dismissed-list", "data-testid": "dismissed-flags" }, gone.map((f) => card(c, f)))));   // T-136 (pass 5 F2)
diff --git a/app/frontend/review.css b/app/frontend/review.css
index d3d5e4c..0c3a5eb 100644
--- a/app/frontend/review.css
+++ b/app/frontend/review.css
@@ -134,3 +134,10 @@ form.rv-reason { display: flex; flex-wrap: wrap; gap: var(--s-2); align-items: c
 .rv-coverage { margin: var(--s-2) 0 var(--s-3); max-width: var(--measure); font-size: var(--t-sm); }
 .rv-coverage > summary { cursor: pointer; color: var(--text-muted); }
 .rv-cov-list { margin: 0 0 var(--s-2); padding-left: var(--s-5); color: var(--text-muted); line-height: var(--lh-sm); }
+
+/* T-151: checks that did not run, and info notes, in the Conflicts group. Neither looks like a conflict card. */
+.rv-skipped, .rv-notchecked { max-width: var(--measure); font-size: var(--t-sm); line-height: var(--lh-sm); }
+.rv-skipped { margin: var(--s-2) 0; padding: var(--s-2) var(--s-3); border: 1px dashed var(--border-strong); border-radius: var(--r-1); }
+.rv-skipped .rv-cov-list { margin-bottom: 0; }
+.rv-notes { list-style: none; margin: var(--s-2) 0; padding: 0; max-width: var(--measure); font-size: var(--t-sm); line-height: var(--lh-sm); color: var(--text-muted); }
+.rv-note { padding: var(--s-1) 0; }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:30.107Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && ls | tail -30; ls r2-07c7558 2>/dev/null | head; find . -maxdepth 2 -name 'launch*.py' | head"
}
````

### User / tool · 2026-11-02T14:23:30.256Z

**tool result**
````
walk2.py
why.orig.py
wprobe.py
wt
wt-031a708
wt-7df65fb
wt-golden.txt
wt-head
wt2
wt7944.db
wt7944.log
wt7944.pid
wt7945.db
wt7945.log
wt7945.pid
wt7946.db
wt7946.log
wt7946.pid
wt_final
wt_final2
wt_head
wt_run.sh
wt_t155
x45.py
xc.py
xss.py
zlayt-base
zlayt-head
zlayt-r2
zlayt-r3
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
./out/launch.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:32.401Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cat out/launch.py; ls out | head; cat wt_run.sh | head -20"
}
````

### User / tool · 2026-11-02T14:23:32.494Z

**tool result**
````
import sys, os, runpy
R = os.path.abspath("../gate_m2")
sys.path.insert(0, R)
os.chdir(R)
runpy.run_module("app.main", run_name="__main__")
20261102T044831Z.md
calibration.json
case_case_lib02_slip_fall_prior_knee.json
case_case_lib08_second_crash_mri_after.json
case_case_lib09_spanish_interpreter_espalda.json
case_lib01_er_only_then_gap_audit.json
case_lib01_er_only_then_gap_billing.json
case_lib01_er_only_then_gap_create.json
case_lib01_er_only_then_gap_export_before.json
case_lib01_er_only_then_gap_token.txt
#!/bin/bash
# usage: wt_run.sh <worktree> <port> <pytest args...>   (clean worktree, its own frontend, own server and db; stopped by PID)
S=/tmp/x/sp
W=$1; PORT=$2; shift; shift
cd $W
PORT=$PORT ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$S/wt$PORT.db /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $S/wt$PORT.log 2>&1 &
PID=$!
echo $PID > $S/wt$PORT.pid
sleep 4
cd /Users/arsis/zlayt-pm-project
E2E_BASE_URL=http://localhost:$PORT /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest "$@"
kill $PID
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:36.953Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nmkdir -p $SP/t151-25f585c && cd /Users/arsis/zlayt-pm-project && git archive 25f585c | tar -x -C $SP/t151-25f585c && mkdir -p $SP/t151-scripts $SP/t151-out && cat > $SP/t151-scripts/launch.py <<'EOF'\nimport sys, os, runpy\nR = sys.argv[1]\nsys.path.insert(0, R)\nos.chdir(R)\nrunpy.run_module(\"app.main\", run_name=\"__main__\")\nEOF\ncd $SP/t151-scripts && (PORT=7951 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=$SP/t151-out/t151.db nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -I launch.py $SP/t151-25f585c > $SP/t151-out/server.log 2>&1 & echo $! > $SP/t151-out/server.pid); sleep 5; cat $SP/t151-out/server.pid; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7951/; tail -3 $SP/t151-out/server.log; ls /Users/arsis/zlayt-pm-project/evals/golden | head; ls /Users/arsis/zlayt-pm-project/app/llm/fixtures 2>/dev/null | head -3"
}
````

### User / tool · 2026-11-02T14:23:42.576Z

**tool result**
````
21724
200
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:45.959Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncurl -s http://127.0.0.1:7951/api/library | head -c 1500; echo; ps -p 21724 -o pid,command | cut -c1-150; grep -n \"skipped\\|notes\" /Users/arsis/zlayt-pm-project/memory/contracts/api.md | head -20; grep -n \"reason_code\" -r $SP/t151-25f585c/app/backend/*.py | head"
}
````

### User / tool · 2026-11-02T14:23:46.124Z

**tool result**
````
{"cases":[{"id":"case_lib01_er_only_then_gap","name":"case lib01 er only then gap","description":"Library L1 (mirrors S1). Rear-end collision, ED visit and a negative x-ray, then the first primary-care visit 44 days later with a new arm symptom and a patient-stated reason for the delay. The gap is flagged; the reason is shown as the pat"},{"id":"case_lib02_slip_fall_prior_knee","name":"case lib02 slip fall prior knee","description":"Library L2 (mirrors S2). Store slip-and-fall with a prior knee arthroscopy shown in imaging and in the patient's history; MRI wording that may reflect both acute and prior change. The tool shows the prior-condition language and the hedge an"},{"id":"case_lib03_truck_rear_end_chiro","name":"case lib03 truck rear end chiro","description":"Library L3 (mirrors S3). Passenger car struck from behind by a tractor-trailer; chiropractic plan of 36 visits, no change in pain score at visit 14, discharge at maximum benefit after 31 visits, then an MRI 35 days later with hedged chronic"},{"id":"case_lib04_dog_bite_scar_revision","name":"case lib04 dog bite scar revision","description":"Library L4 (mirrors S4). Facial dog bite repaired in the ED, plastic-surgery follow-ups with scar photographs, a planned 8-week interval that the tool still flags, a $6,500 revision estimate and a later revision with a surgeon fee. The tool"},{"id":"case_lib05_pedestrian_orif_hardware","name":"case lib05 pedestrian orif hardware","description":"Library L5 (mirrors S5). Pedestria
  PID COMMAND
21724 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -I launch.py /pri
26:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an unlocatable quote is a hard `422 invalid_edit` with `detail.reason` and `detail.tokens`/`detail.qualifiers`, no override; a judge objection saves the entry as `pending`/`needs_review` with a `warnings[]` code, no 409); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
29:| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
33:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
39:| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconciled rows, skipped records (an EOB service row is a line); no sums or comparisons of any kind, no provider totals or complete flag; internal view, never in the letter |
102:`checked: false` means at least one page could not be checked (`unchecked_pages`); those pages are held back like hidden text, so show them as pages to confirm, not as skipped. `pdf_pages[].start/end/low_conf[].start/end` are offsets into the case text; a page confirmed for hidden text carries `hidden_text_included: true`. Every record in a PDF case has `ocr_derived: true|false`.
111:`GET` returns `{"exhibit": null|string, "bates_prefix": null|string, "bates_start": null|int}`. `PUT` takes the same keys (all optional; omitted or empty means unset) and returns the stored config; `DELETE` clears it and returns the empty config. Validation: `exhibit` and `bates_prefix` up to 20 characters of `A-Za-z0-9 ._-`; `bates_start` an integer 0 to 99999999 (booleans and strings refused); unknown keys refused; any violation is `422 invalid_edit` and nothing changes. Effect on the export only: every letter citation `Source [Ex. __ / Bates __]` becomes `Source [Ex. <exhibit> / Bates <prefix><NNNN>]` with `NNNN` = first number + record number - 1, zero-padded to 4 digits (first number defaults to 1 when only a prefix is set; an unset part stays `__`). With no config the export is byte-identical to the golden. The internal notes never carry exhibit or Bates numbers.
133:**T-141 / T-142, `checks` (GET case, top level; always present; computed per case from what the run did, no model):** what the conflict check looked for on THIS case and what it did not, so the UI can say it honestly ("Checked for: ... Not checked: ..."; never "no conflicts found" without it). `{conflict_types: [..], labels: {<type>: one plain sentence}, skipped: [{type, label, reason_code, reason, record_nos?}], not_checked: [{type, label}], notes: [{type, code, count, record_nos, stated_date, text}]}`. The four types are `plan_vs_early_end` and `denial_vs_history` (pair rules in `conflict_candidates.py`; a judge classifies each pair), `accident_date` and `provider_name` (structural checks in `conflicts.py`). **`conflict_types` lists only the types that ran on the case**; `labels` has all four. **`skipped`** says why a type did not run, or ran only in part. `reason_code`: `NOT_RUN` (case created, comparison between records not run yet; the two code checks ran at ingest), `STAGE_SKIPPED` (the run hit its time limit before the comparison between records), `RUN_FAILED` (the run stopped; nothing known), `LANGUAGE` (every record is Spanish, uncertain or unsupported: the English wording rules could not find anything; the type is absent from `conflict_types`), `LANGUAGE_PARTIAL` (the type ran, but `record_nos` lists the Spanish/uncertain/unsupported records it did not read), `NO_DATED_RECORD` (no parsed record date; `accident_date`). The language-bound types are `plan_vs_early_end`, `denial_vs_history` and `accident_date`; `provider_name` compares header labels. `not_checked` types today: `dosage`, `laterality`, `diagnosis`, `pain_score`, `treatment_duration_months`, `informant_history` (`memory/SCOPE_CUTS.md` row 13). **`notes`** are info lines, never flags, **computed each time the case is read from the current record dates (not stored)**, so `confirm_date` refreshes them together with the accident-date flag: `RECORDS_PREDATE_ACCIDENT` = a single stated accident date is later than N records and none of them has injury, mechanism or accident wording of its own that is not history or negated, so no date conflict is raised; `text` is the sentence to show ("1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care."). The decision is by content (T-141 round 3, no "a record is dated that day" shortcut): a record dated before the stated date makes the accident-date conflict when any clause of it has injury, mechanism or accident vocabulary (collision, crash, MVA/MVC, rear-end, struck, "hit by", pedestrian, incident, accident, injury, whiplash, LOC, trauma, impact, fall, airbag, seatbelt and similar) unless that clause is negated within five words ("denies any accidents", "no recent injuries") or is plainly history (a history word right before the word: "prior accident", "history of MVA", not "prior to the collision"; "last year", "N years ago", a full date over a year before the stated date, a month and year more than two months before the record, a bare year before the record's year). A safe false positive beats a hidden conflict: the conflict then compares with the earliest such record. **A case with no stored run summary** (analysed before per-case checks were kept) reports all four types in `skipped` with `NOT_RUN` and `conflict_types: []` (nothing is claimed; the UI renders an empty list as "none checked", not as the default list). `denial_vs_history` reads a form field answered No ("Prior accidents? Yes [ ] No [X]." including OCR "No IX]", or "Prior injuries: None.") as a denial; the denial flag quotes the question and the checked answer together.
135:**T-143 (round 2), `records[].uncovered[]` (GET case; review aid, code only):** EVERY sentence of the record that no live entry's excerpt overlaps, so a pain score, a chief complaint, a baseline-history line, a patient-stated mechanism or onset ("Patient states she was struck by a car..."), an exam finding, a medication, a work-status line or an interpreter / history-source line an entry left out does not vanish silently. Each item is `{text, start, end, kinds}`: `text` the verbatim sentence (the shared splitter, over the same quotable body as `sentences[]`), `start`/`end` offsets into the case text (the same frame as `sentences[]`), `kinds` a **hint only** and possibly empty (`number`, `body_part`, `term`, `negation`); it never decides whether a sentence is listed, so the frontend must not filter on it. A form answer carries its question: `Accidentes anteriores? Si [ ] No [X].` is one item. Skipped only when the line is POSITIVELY administrative by an anchored whole-line pattern: a signature line (`Electronically signed by ...`, `Signed: ...`, `Firma de la paciente: ...`, a bare `Name, MD`), a header field (`Date of service: ...`, `Fax: ...`), a page / fax / print stamp, a billing line (a dollar figure or CPT code, a CMS-1500 item with a billing label, `Balance due.`), or a legal / cost boilerplate line without a dollar sign (`No payments posted.`, `Letter of protection requested.`, `Cost of the collar was covered.`); a line with a pain score N/10 is never skipped, and a bare word such as "adjustment", "balance" or "signed" never removes a line (any other wording of a cost or legal sentence stays listed). A duplicate record (`duplicate_of` set; the original carries the entry) and a record with no quotable body (`sentences_reason` set) give `[]`; `[]` also when nothing is left out, and the field is always present. A rejected (tray) entry covers nothing; a dismissed or pending entry does. It is never in `entries`, the review queue, the counts, the letter or the internal notes (an accepted flag may still quote its own evidence sentence in the notes, as before); the frontend may show it as "Also in this record, not in any entry" next to the record, read-only (a sentence is added to the letter only by the existing manual-entry or edit-quote routes).
259:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). **T-108:** units are cut from the quotable excerpt body only (no `Excerpt:` label, quote marks or Date/Source/=== lines), at true offsets, and every unit saves on its own: a sentence that a hedge sentence qualifies is ONE combined unit with the hedge sentence(s) after it (the save route's own check decides, Spanish hedge words included), so the picker never builds a quote the route refuses. A record whose Excerpt label cannot be separated from its text (no Date/Source layout) has `sentences: []` and a plain-words `sentences_reason`; the frontend shows no picker for it. `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
340:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; its class changes only through `POST .../reclassify`, never through `edit`); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so "date not stated" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as "date not confirmed, not exported".
364:- Export: the entry is **not in the letter**, not in `items.entries`, not counted in `counts.entries` or `provenance.edited_count`; it counts in `excluded.pending` and in `excluded.edit_not_confirmed` (subset of pending), and in the notes' "Items not reviewed: N". It does not block export (it is not in the letter, as with a pending item, D-045(a)), unless nothing else is accepted (`NOTHING_ACCEPTED`).
366:- Internal notes: EDITED ITEMS lists it with "(edited; second check not available (JUDGE_UNAVAILABLE); not yet confirmed against the quote, so it is not in the letter (accept it to put it there))" (the reason sentence follows the item's reasons: `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, ...), PENDING ITEMS NOT INCLUDED lists it with the same phrase, and RECORDS NOT IN THE TREATMENT SECTION says "edited, not yet confirmed against the quote". After she accepts, EDITED ITEMS keeps the reason: "(accepted by the paralegal after comparing it with the quote; second check not available (JUDGE_UNAVAILABLE))". The notes never say she accepted an edit she has not accepted.
393:**Amount classes and charge confirms (T-140 + D-059; code only).** The class is decided by code (`amounts.classify`), never by a model or the second check. An amount is class `unclear`, never `charge`, with its reason shown under `AMOUNTS NOT TOTALED` in `internal_notes_text` ("Not totaled ($2,740.00): Total or subtotal line: it repeats the charges listed with it, so it is not totaled."), when: (1) its label (the words just before it in its clause, the words just after it such as "$300 paid", the first cell of its table row, or its column heading) names a total, subtotal, balance, amount due, payment, adjustment, write-off, credit, reversal, void, refund, recoupment, year-to-date or running figure, previous statement or balance forward, or statement-level figure ("New charges"); a table row such as `Total $380 $77 $305` makes every figure on the row a non-charge; (2) it carries a minus sign, parentheses or a CR suffix, or is $0; (3) it comes from an insurer document (EOB, remittance) restating the provider's bill ("Amount billed"). A cue word inside a service description stays a charge ("Chiropractic adjustment charge $65", "Total body MRI charge", "Balance training charge", "Total of 12 visits billed"). A UB-04 `FL47 total charges` line is the column of a revenue-code line and stays a charge; `Rev 0001` is the claim total. Two lines of one record never merge, even at the same price.
396:**`totals.possible_overlaps` (T-110, D-019; every response that carries `totals`).** Array, normally empty. One object per pair of a billing-statement line and a separately stated charge that name the same kind of service (closed family table in `app/backend/overlap.py`: consult, physical therapy, imaging, emergency, ambulance, injection, surgery, laboratory; English and Spanish) when the charge's record date is inside the statement's date range (two dates written in the statement text, else on or before the statement's own date). Fields: `code: "POSSIBLE_OVERLAP"`, `statement_amount_id`, `covered_amount_id`, `statement_record_id`, `covered_record_id`, `statement_text`, `covered_text` (the figures as written), `service`, `range: {from, to, stated}`, `date_known` (false when the charge's record date is not confirmed: it is listed, not ruled out), `both_charges` (both are class `charge`), `both_in_total` (both are accepted, so the accepted total currently contains both), `message` (one of three fixed sentences; never model text). Rates, estimates, damages, dismissed and unreadable figures are never parties, nor are statement balance/total/payment/adjustment lines or two figures of one record. **The warning never changes `totals.accepted`, `pending` or `detected_not_a_total`, and no figure is subtracted, merged or compared: the total still adds stated charges only.** The frontend shows each warning beside the total with both figures and the message; the paralegal dismisses one of the two if the statement line includes the other. **Export (T-110 r2):** when `possible_overlaps` is not empty, `internal_notes_text` gets a section `POSSIBLE OVERLAPS (check before relying on the charges total)` after `AMOUNTS NOT TOTALED`, one plain-words line per pair naming both records and both figures (and whether both are in the total); with none, the notes are byte-for-byte as before. The letter never mentions an overlap.
401:**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. An edit still marked `needs_review` is open and out of the letter, so it does not stop the export either (T-134, see the edit section). Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
408:  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\n[... sections in R-EX-4 order: full text is the INTERNAL_NOTES_TEXT block of the golden file ...]",
522:    "flags_in_notes": 9,
549:Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges stated in these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte; **no dollar amount appears in `letter_text` outside the BILLED CHARGES section (T-139)**: an entry whose summary or quote states an amount is never written into the treatment section, whatever its review status (see "Dollar amounts in entries"), a charge's `Source` line quotes only the clause that holds its own figure when the sentence also states another one (a rate, a balance, another line item), and a dismissed charge is never listed under BILLS TO REQUEST. Rates, estimates, unclear and dismissed amounts appear only in `internal_notes_text`.
582:  "status": "pass",                     // "pass" | "fail" | "skipped" | "pending"
590:`status` meaning: `pass` the check ran and passed (or the human decided to accept); `fail` the check ran and found a problem (the item is then `needs_review` or `rejected`); `skipped` not run on purpose (a step before it already rejected the item, no judge applies to code-made items, the judge did not answer, or the human dismissed it) and `why`/`reason_code` say which; `pending` not done yet (the AI run has not reached this step, or the human has not decided).
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-25f585c/app/backend/case_extras.py:30:    return {"id": item_id, "reason": "code_check_failed", "reason_code": err.detail["reason_code"], "why": err.message, "next_action": err.detail["next_action"]}
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-25f585c/app/backend/case_list.py:56:    return {"ready": step["ready"], "blockers": keep(step["blockers"], ("reason_code", "kind", "item_id", "why")),
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-25f585c/app/backend/case_list.py:57:            "warnings": keep(step["warnings"], ("reason_code", "count", "why"))}
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-25f585c/app/backend/billing.py:902:            skipped.append({"record_no": r["n"], "reason_code": "INJECTION_SUSPECTED"})
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-25f585c/app/backend/billing.py:918:            skipped.append({"record_no": r["n"], "reason_code": "UNRECOGNISED_BILLING_FORM"})
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-25f585c/app/backend/billing.py:966:    unreconciled = [{"provider": l["provider"], "record_no": l["record_no"], "form": l["form"], "class": "unclear", "reason_code": "ROW_NOT_PARSED",
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-25f585c/app/backend/conflict_candidates.py:267:    {conflict_types: [what ran], labels: {type: sentence}, skipped: [{type, label, reason_code, reason, record_nos?}], not_checked: [{type, label}],
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-25f585c/app/backend/conflict_candidates.py:277:        skipped.append({"type": t, "label": CONFLICT_LABELS[t], "reason_code": code, "reason": reason, **({"record_nos": nos} if nos else {})})
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-25f585c/app/backend/generator.py:171:    if jd.get("verdict") in ("partially", "unsupported") and why.judge_detail(jd.get("reason_code")):
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-25f585c/app/backend/generator.py:172:        e["why"] += " " + why.judge_detail(jd["reason_code"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:49.529Z

**tool call — Bash**
````
{
 "command": "curl -s http://127.0.0.1:7951/api/library | python3 -c \"import json,sys; [print(c['id']) for c in json.load(sys.stdin)['cases']]\"; grep -n \"data-testid\\|testid\" /Users/arsis/zlayt-pm-project/tests/e2e/test_conflict_skipped.py | head -30"
}
````

### User / tool · 2026-11-02T14:23:49.657Z

**tool result**
````
case_lib01_er_only_then_gap
case_lib02_slip_fall_prior_knee
case_lib03_truck_rear_end_chiro
case_lib04_dog_bite_scar_revision
case_lib05_pedestrian_orif_hardware
case_lib06_lop_billed_vs_adjusted
case_lib07_parking_lot_fall_outside_records
case_lib08_second_crash_mri_after
case_lib09_spanish_interpreter_espalda
case_lib10_eob_ub04_cms1500
case_lib11_priors_and_ledger
case_lib12_records_review_credibility
case_lib13_cloned_notes_cross_provider
case_lib14_handwritten_chiro_scans
case_lib15_conclusory_letter_mist
47:    return page.locator('[data-testid="flags-panel"] [data-group="conflict"]')
111:        it = box.locator(f'[data-testid=conflict-skipped-item][data-skip-type={t}]')
152:    assert "time limit" in _text(items.nth(0)) and g.locator("[data-skip-type=plan_vs_early_end] [data-testid=conflict-skipped-records]").count() == 0
153:    assert g.locator("[data-skip-type=accident_date] [data-testid=conflict-skipped-records]").count() == 0, "an empty record list says nothing"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:59.274Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncat > $SP/t151-scripts/probe.py <<'EOF'\n\"\"\"T-151 legal-nurse probe: sample + lib08/09/11 (+lib01,lib02 extra) on 127.0.0.1:7951. Reads the Conflicts group as a user; compares with GET case checks.\"\"\"\nimport json, sys, urllib.request\nfrom playwright.sync_api import sync_playwright\nOUT = sys.argv[1]\nURL = \"http://127.0.0.1:7951/\"\nSAMPLE = open(\"/Users/arsis/zlayt-pm-project/evals/golden/sample.txt\").read()\ndef log(m): print(m, flush=True)\ndef api(tok):\n    with urllib.request.urlopen(URL + \"api/cases/%s\" % tok) as r: return json.loads(r.read())\nwith sync_playwright() as p:\n    b = p.chromium.launch()\n    for kind in sys.argv[2:]:\n        ctx = b.new_context(viewport={\"width\": 1440, \"height\": 1000}); pg = ctx.new_page()\n        pg.goto(URL); pg.wait_for_timeout(700)\n        if kind == \"sample\":\n            pg.fill(\"[data-testid=input-text]\", SAMPLE); pg.click(\"[data-testid=btn-analyze]\")\n        else:\n            pg.locator(\"summary:has-text('synthetic library')\").first.click(); pg.wait_for_timeout(300)\n            pg.locator(\"[data-testid=library-%s]\" % kind).first.click()\n        pg.wait_for_selector(\"[data-testid=review-counts]\", timeout=180000); pg.wait_for_timeout(800)\n        tok = pg.url.split(\"/case/\")[-1].split(\"?\")[0]\n        g = pg.locator(\"[data-group=conflict]\").first\n        log(\"=== %s token=%s\" % (kind, tok))\n        log(\"GROUP TEXT:\\n\" + g.inner_text())\n        log(\"cov open=%s\" % g.locator(\"[data-testid=conflict-coverage]\").evaluate(\"(d)=>d.open\"))\n        log(\"conflict cards: %d\" % g.locator(\"[data-flag-id]\").count())\n        for tid in (\"conflict-note\",\"conflict-skipped-item\",\"conflict-checked-item\",\"conflict-not-checked-item\",\"conflict-not-checked-line\",\"conflict-empty\"):\n            log(\"  %s: %s\" % (tid, g.locator(\"[data-testid=%s]\" % tid).all_text_contents()))\n        c = api(tok); ck = c[\"checks\"]\n        log(\"API conflict_types=%s\" % ck[\"conflict_types\"])\n        log(\"API skipped=%s\" % json.dumps(ck.get(\"skipped\"), ensure_ascii=False))\n        log(\"API notes=%s\" % json.dumps(ck.get(\"notes\"), ensure_ascii=False))\n        log(\"API not_checked=%s\" % [x[\"type\"] for x in ck[\"not_checked\"]])\n        log(\"API conflict flags=%s\" % [(f[\"id\"], f.get(\"title\")) for f in c[\"flags\"] if f[\"type\"]==\"conflict\"])\n        log(\"API records=%s\" % [(r.get(\"n\") or r.get(\"record_no\"), r.get(\"source\") or r.get(\"provider\")) for r in c.get(\"records\", [])][:20])\n        g.scroll_into_view_if_needed()\n        pg.screenshot(path=OUT + \"/%s.png\" % kind.replace(\"case_\",\"\"), full_page=True)\n        g.screenshot(path=OUT + \"/%s-group.png\" % kind.replace(\"case_\",\"\"))\n        ctx.close()\n    b.close()\nEOF\ncd $SP/t151-scripts && /Users/arsis/zlayt-pm-project/.venv/bin/python probe.py $SP/t151-out case_lib08_second_crash_mri_after case_lib09_spanish_interpreter_espalda case_lib11_priors_and_ledger sample 2>&1 | tee $SP/t151-out/probe.out.txt"
}
````

### User / tool · 2026-11-02T14:24:30.615Z

**tool result**
````
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-scripts/probe.py", line 18, in <module>
    pg.locator("summary:has-text('synthetic library')").first.click(); pg.wait_for_timeout(300)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 11021, in click
    self._sync(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py", line 174, in click
    return await self._frame._click(self._selector, strict=True, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py", line 598, in _click
    await self._channel.send("click", self._timeout, locals_to_params(locals()))
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 78, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 636, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.TimeoutError: Locator.click: Timeout 30000ms exceeded.
Call log:
  - waiting for locator("summary:has-text('synthetic library')").first
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:24:31.616Z

UI changed since; check how the e2e tests open library cases.

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:24:32.142Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/e2e/test_conflict_skipped.py; grep -n \"def open_library\\|def open_case\\|library\" tests/e2e/conftest.py | head"
}
````

### User / tool · 2026-11-02T14:24:32.245Z

**tool result**
````
"""T-151 (frontend; backend T-141 r2, T-142 legal-nurse review): the Conflicts group says which checks did NOT run on this case and shows info notes apart from conflicts.
GET case `checks`: skipped[] {type, label, reason_code, reason, record_nos?} (a check that did not run, or not on every record), notes[] {type, code, count, record_nos, stated_date, text} (info only).
  - skipped: each one is listed in the group, always visible, with the server's plain reason and, when the server names records, "Records 2, 4 and 7 were not read." A type that is skipped is NOT in the Checked list.
  - notes: info lines (conflict-note), not flag cards: no item id, no accept / dismiss, not counted in the group's count.
  - one line is always visible, also when conflicts are listed: the two kinds the legal nurse named (left versus right, loss of consciousness history) and "any other kind" are not checked.
Real backend on lib11 (a note, nothing skipped) and lib09 (Spanish records: three checks only partly ran); route stubs cover the other reason codes.
Test ids (declared in conftest): conflict-skipped, conflict-skipped-item (data-skip-type, data-reason-code), conflict-skipped-records, conflict-notes, conflict-note, conflict-not-checked-line."""
import re
import time
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case
import tests.e2e.conftest as C

CASE_URL = re.compile(r"/api/cases/[^/?]+$")
CODE = re.compile(r"\b[A-Z]{3,}(?:_[A-Z]+)+\b")


def _make(lib):
    st, c = api("POST", "/api/cases", {"library": lib}); assert st in (200, 201), (st, c)
    tok = c["token"]
    assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.5)
    assert s["status"] == "ready", s
    return tok


@pytest.fixture(scope="module")
def lib11():
    if not C._up():
        pytest.skip("app server not running")
    tok = _make("case_lib11_priors_and_ledger"); yield tok; api("DELETE", f"/api/cases/{tok}")


@pytest.fixture(scope="module")
def spanish():
    if not C._up():
        pytest.skip("app server not running")
    tok = _make("case_lib09_spanish_interpreter_espalda"); yield tok; api("DELETE", f"/api/cases/{tok}")


def _group(page):
    return page.locator('[data-testid="flags-panel"] [data-group="conflict"]')


def _text(loc):
    return re.sub(r"\s+", " ", loc.inner_text())


def _checks(tok):
    return api("GET", f"/api/cases/{tok}")[1]["checks"]


def _seqs(nos):
    return "Record " + str(nos[0]) + " was" if len(nos) == 1 else "Records " + ", ".join(map(str, nos[:-1])) + " and " + str(nos[-1]) + " were"

61:  Wording: a refused number is shown as the paralegal typed it ('$9,000', not '9000'); the AI-check row for a flag the checks left out says 'Left out of the letter' and 'Nothing to accept here', has no decision line, and its button reads 'Why this status'; the row's More / Less control is named 'More of ...' / 'Less of ...'; library cases are titled in plain words (no 'lib09' or 'case ' in case-name).
217:def open_case(page, tok):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:24:33.921Z

**tool call — Bash**
````
{
 "command": "sed -n 205,240p tests/e2e/conftest.py"
}
````

### User / tool · 2026-11-02T14:24:34.015Z

**tool result**
````
        yield p

@pytest.fixture
def page(pw):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    pg = ctx.new_page()
    yield pg
    try: pg.unroute_all(behavior="ignoreErrors")     # route stubs (JudgeNotRun) may still have a fetch in flight
    except Exception: pass
    b.close()

def open_case(page, tok):
    page.goto(f"{BASE}/#/case/{tok}")
    page.get_by_test_id("timeline").wait_for(timeout=15000)



class WordingFails:
    """Route-rewriting stub (T-097 r2, T-098, D-047): an edited summary whose code check fails. Since T-100 the edit route refuses such wording (hard 422), so the only way to see the gate's
    D-045(b) code-check blocker in a browser is to rewrite GET .../trace, .../items/<id>/trace and .../export the way the backend answers for a failing edited summary
    (contract: memory/contracts/api.md, 'Code-check blocker'). The ids are edited or accepted items of the real case; the failure holds while the item's summary is unchanged,
    so editing it (to anything) 'fixes' it, like the real gate. The real backend still answers everything else."""
    import re as _re
    WHY = "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out. You wrote or edited this summary, so the second AI check is not needed, but the code checks on the summary still have to pass before it can go into the letter."
    FIX = "Edit the summary to keep \u2018may represent\u2019; the quote says it and your summary leaves it out. The export stays blocked until it passes."

    def __init__(self, page, token, ids):
        self.page, self.token, self.ids = page, token, list(ids)
        self.base = {i: self._summary(i) for i in self.ids}
        for pat, fn in ((r"/api/cases/[^/]+/trace$", self._case_trace), (r"/api/cases/[^/]+/items/[^/]+/trace$", self._item_trace), (r"/api/cases/[^/]+/export$", self._export)):
            page.route(self._re.compile(pat), fn)

    def _summary(self, i):
        c = api("GET", f"/api/cases/{self.token}")[1]
        e = next((x for x in c["entries"] + c["undated_entries"] if x["id"] == i), None)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:24:40.743Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $SP/t151-scripts && python3 - <<'EOF'\ns=open(\"probe.py\").read()\ns=s.replace('''            pg.locator(\"summary:has-text('synthetic library')\").first.click(); pg.wait_for_timeout(300)\n            pg.locator(\"[data-testid=library-%s]\" % kind).first.click()\n''','''            import time\n            rq = urllib.request.Request(URL+\"api/cases\", data=json.dumps({\"library\": kind}).encode(), headers={\"Content-Type\":\"application/json\"}, method=\"POST\")\n            t0 = json.loads(urllib.request.urlopen(rq).read())[\"token\"]\n            urllib.request.urlopen(urllib.request.Request(URL+\"api/cases/%s/run\" % t0, data=b\"{}\", headers={\"Content-Type\":\"application/json\"}, method=\"POST\"))\n            for _ in range(300):\n                if json.loads(urllib.request.urlopen(URL+\"api/cases/%s/status\" % t0).read())[\"status\"] in (\"ready\",\"failed\"): break\n                time.sleep(0.5)\n            pg.goto(URL + \"#/case/\" + t0)\n''')\ns=s.replace('tok = pg.url.split(\"/case/\")[-1].split(\"?\")[0]','tok = pg.url.split(\"/case/\")[-1].split(\"?\")[0].split(\"/\")[0]')\nopen(\"probe.py\",\"w\").write(s)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python probe.py $SP/t151-out case_lib08_second_crash_mri_after case_lib09_spanish_interpreter_espalda case_lib11_priors_and_ledger sample 2>&1 | tee $SP/t151-out/probe.out.txt"
}
````

### User / tool · 2026-11-02T14:24:52.763Z

**tool result**
````
=== case_lib08_second_crash_mri_after token=_zGDj98RAYbjS312ltzqUw
GROUP TEXT:
Conflicts between records (0)

No conflicts found among the kinds checked. Other kinds of conflict are not checked.

Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.

What the conflict check covers (4 kinds checked)

Checked: the code compares records for these kinds of conflict only.

A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early
A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record
A stated accident date against the dates of the records, or two different stated accident dates
The same clinician named under two different practice names

Not checked: anything not listed above, including these, is not looked for. Read the records for them.

Medication doses that differ between records
Left versus right across records (checked only inside one summary)
A diagnosis that differs or is withdrawn between records
Pain scores that differ on the same day
Plans and outcomes measured in months
Patient history reported by a relative
cov open=True
conflict cards: 0
  conflict-note: []
  conflict-skipped-item: []
  conflict-checked-item: ['A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early', 'A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record', 'A stated accident date against the dates of the records, or two different stated accident dates', 'The same clinician named under two different practice names']
  conflict-not-checked-item: ['Medication doses that differ between records', 'Left versus right across records (checked only inside one summary)', 'A diagnosis that differs or is withdrawn between records', 'Pain scores that differ on the same day', 'Plans and outcomes measured in months', 'Patient history reported by a relative']
  conflict-not-checked-line: ['Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.']
  conflict-empty: ['No conflicts found among the kinds checked. Other kinds of conflict are not checked.']
API conflict_types=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name']
API skipped=[]
API notes=[]
API not_checked=['dosage', 'laterality', 'diagnosis', 'pain_score', 'treatment_duration_months', 'informant_history']
API conflict flags=[]
API records=[(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)]
=== case_lib09_spanish_interpreter_espalda token=w9w_6My2Q0ZRrzEDjMJ8Uw
GROUP TEXT:
Conflicts between records (0)

No conflicts found among the kinds checked. Other kinds of conflict are not checked.

Did not run on this case, or not on every record (3): the group above says nothing about these.

A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read.
A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read.
A stated accident date against the dates of the records, or two different stated accident dates This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read.

Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.

What the conflict check covers (1 kind checked)

Checked: the code compares records for these kinds of conflict only.

The same clinician named under two different practice names

Not checked: anything not listed above, including these, is not looked for. Read the records for them.

Medication doses that differ between records
Left versus right across records (checked only inside one summary)
A diagnosis that differs or is withdrawn between records
Pain scores that differ on the same day
Plans and outcomes measured in months
Patient history reported by a relative
cov open=True
conflict cards: 0
  conflict-note: []
  conflict-skipped-item: ['A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read.', 'A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read.', 'A stated accident date against the dates of the records, or two different stated accident dates This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read.']
  conflict-checked-item: ['The same clinician named under two different practice names']
  conflict-not-checked-item: ['Medication doses that differ between records', 'Left versus right across records (checked only inside one summary)', 'A diagnosis that differs or is withdrawn between records', 'Pain scores that differ on the same day', 'Plans and outcomes measured in months', 'Patient history reported by a relative']
  conflict-not-checked-line: ['Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.']
  conflict-empty: ['No conflicts found among the kinds checked. Other kinds of conflict are not checked.']
API conflict_types=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name']
API skipped=[{"type": "plan_vs_early_end", "label": "A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early", "reason_code": "LANGUAGE_PARTIAL", "reason": "This check reads English wording; the records in Spanish were not read.", "record_nos": [2, 4, 7]}, {"type": "denial_vs_history", "label": "A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record", "reason_code": "LANGUAGE_PARTIAL", "reason": "This check reads English wording; the records in Spanish were not read.", "record_nos": [2, 4, 7]}, {"type": "accident_date", "label": "A stated accident date against the dates of the records, or two different stated accident dates", "reason_code": "LANGUAGE_PARTIAL", "reason": "This check reads English wording; the records in Spanish were not read.", "record_nos": [2, 4, 7]}]
API notes=[]
API not_checked=['dosage', 'laterality', 'diagnosis', 'pain_score', 'treatment_duration_months', 'informant_history']
API conflict flags=[]
API records=[(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)]
=== case_lib11_priors_and_ledger token=pASX53_PV8rGIXOIImrlnQ
GROUP TEXT:
Conflicts between records (2)
Records differ on a fact
Quote matches

Fennimoor Spine Clinic, new patient intake form (OCR text) (March 27, 2026): “Prior accidents? Yes [ ] No [X].” Dr. Hesper Alderton, primary care (March 4, 2026): “History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.”

Record 6 · Fennimoor Spine Clinic, new patient intake form (OCR text)
Prior accidents? Yes [ ] No [X].
Quoted line from this record: How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7.
Record 1 · Dr. Hesper Alderton, primary care
History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.
Open records 6 and 1
Why this status
Accept
Edit note
Dismiss
Dismiss with reason…
Audit
Records differ on a fact
Quote matches

Fennimoor Spine Clinic, new patient intake form (OCR text) (March 27, 2026): “Prior injuries? Yes [ ] No IX].” Dr. Hesper Alderton, primary care (March 4, 2026): “History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.”

Record 6 · Fennimoor Spine Clinic, new patient intake form (OCR text)
Prior injuries? Yes [ ] No IX].
Quoted line from this record: How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7.
Record 1 · Dr. Hesper Alderton, primary care
History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.
Open records 6 and 1
Why this status
Accept
Edit note
Dismiss
Dismiss with reason…
Audit
Note 1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care.

Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.

What the conflict check covers (4 kinds checked)
cov open=False
conflict cards: 0
  conflict-note: ['Note 1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care.']
  conflict-skipped-item: []
  conflict-checked-item: ['A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early', 'A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record', 'A stated accident date against the dates of the records, or two different stated accident dates', 'The same clinician named under two different practice names']
  conflict-not-checked-item: ['Medication doses that differ between records', 'Left versus right across records (checked only inside one summary)', 'A diagnosis that differs or is withdrawn between records', 'Pain scores that differ on the same day', 'Plans and outcomes measured in months', 'Patient history reported by a relative']
  conflict-not-checked-line: ['Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.']
  conflict-empty: []
API conflict_types=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name']
API skipped=[]
API notes=[{"type": "accident_date", "code": "RECORDS_PREDATE_ACCIDENT", "count": 1, "record_nos": [1], "stated_date": "2026-03-18", "text": "1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care."}]
API not_checked=['dosage', 'laterality', 'diagnosis', 'pain_score', 'treatment_duration_months', 'informant_history']
API conflict flags=[('f_cx1', 'Records differ on a fact'), ('f_cx2', 'Records differ on a fact')]
API records=[(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)]
=== sample token=IR_5Ynjp-UMQ5zEp_4oS_g
GROUP TEXT:
Conflicts between records (2)
Stated accident date is later than recorded treatment
Quote matches

Stated accident date January 19, 2026 (“Date of accident per intake form: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Austin EMS run report; Central ER discharge summary). The records disagree; the tool does not choose between them.

Record 7 · Hill Country Pain Management, new patient
Date of accident per intake form: 2026-01-19
Quoted line from this record: New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered.
Record 1 · Austin EMS run report
Date: 2026-01-09
Quoted line from this record: 41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.
Record 2 · Central ER discharge summary
Date: 2026-01-09
Quoted line from this record: Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.
Open records 7, 1 and 2
Why this status
Accept
Edit note
Dismiss
Dismiss with reason…
Audit
Treatment plan and what followed differ
Quote matches

Capital PT, initial evaluation (January 23, 2026): “Plan of care: 12 visits.” Capital PT, visit 9 (March 6, 2026): “Discharged from PT after two missed appointments.”

Record 4 · Capital PT, initial evaluation
Plan of care: 12 visits.
Quoted line from this record: Cervical range of motion reduced approx. 40%. Plan of care: 12 visits.
Record 6 · Capital PT, visit 9
Discharged from PT after two missed appointments.
Quoted line from this record: Discharged from PT after two missed appointments. Pain 3/10.
Open records 4 and 6
Why this status
Accept
Edit note
Dismiss
Dismiss with reason…
Audit

Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.

What the conflict check covers (4 kinds checked)
cov open=False
conflict cards: 0
  conflict-note: []
  conflict-skipped-item: []
  conflict-checked-item: ['A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early', 'A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record', 'A stated accident date against the dates of the records, or two different stated accident dates', 'The same clinician named under two different practice names']
  conflict-not-checked-item: ['Medication doses that differ between records', 'Left versus right across records (checked only inside one summary)', 'A diagnosis that differs or is withdrawn between records', 'Pain scores that differ on the same day', 'Plans and outcomes measured in months', 'Patient history reported by a relative']
  conflict-not-checked-line: ['Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.']
  conflict-empty: []
API conflict_types=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name']
API skipped=[]
API notes=[]
API not_checked=['dosage', 'laterality', 'diagnosis', 'pain_score', 'treatment_duration_months', 'informant_history']
API conflict flags=[('f_accident_date_after_treatment_1_2_7', 'Stated accident date is later than recorded treatment'), ('f_cx1', 'Treatment plan and what followed differ')]
API records=[(None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None), (None, None)]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:25:17.415Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $SP/t151-25f585c && sed -n 255,330p app/backend/conflict_candidates.py; grep -n \"checks(\" app/backend/*.py | head"
}
````

### User / tool · 2026-11-02T14:25:17.521Z

**tool result**
````
    for r in records:
        lang = r.get("lang") or "en"
        if lang != "en":
            unread.setdefault(lang, []).append(r["n"])
    return {"conflicts_stage": stage, "read_records": sum(1 for r in records if (r.get("lang") or "en") == "en"),
            "unread": {k: sorted(v) for k, v in sorted(unread.items())}}


def checks(run: dict = None, state: str = "complete", records: list = None) -> dict:
    """GET case `checks`, computed from what this case actually ran (T-141 r2/r3). `run` is run_summary() as stored; `state` is 'complete', 'not_run'
    (created, not analysed) or 'failed'; `records` are the case's records as they are NOW (store.load_records): the dated-record count and `notes` come from
    them, so confirming a date refreshes both. A case with no stored summary reports every check as not run (NOT_RUN): nothing is claimed about it.
    {conflict_types: [what ran], labels: {type: sentence}, skipped: [{type, label, reason_code, reason, record_nos?}], not_checked: [{type, label}],
    notes: [..]}. A type is in `skipped` without `record_nos` when it did not run at all (and is then absent from conflict_types), and with `record_nos`
    when it ran but could not read those records (Spanish and the like)."""
    from app.backend import conflicts
    run = run or None
    stage = (run or {}).get("conflicts_stage")
    dated = sum(1 for r in records if r.get("date_iso")) if records is not None else None
    skipped = []

    def skip(t, code, reason, nos=None):
        skipped.append({"type": t, "label": CONFLICT_LABELS[t], "reason_code": code, "reason": reason, **({"record_nos": nos} if nos else {})})

    for t in CONFLICT_LABELS:
        if run is None:
            skip(t, "NOT_RUN", "This case was analysed before the record of what ran was kept, so nothing is claimed about this check. Run it again to check.")
        elif t in _PAIR_TYPES and stage != "ran":
            if stage == "skipped":
                skip(t, "STAGE_SKIPPED", "The run reached its time limit before the comparison between records. Run it again to check.")
            elif state == "failed":
                skip(t, "RUN_FAILED", "The run stopped before the comparison between records finished.")
            else:
                skip(t, "NOT_RUN", "The comparison between records has not run yet.")
        elif t == "accident_date" and dated == 0:
            skip(t, "NO_DATED_RECORD", "No record has a date the code could read, so there is nothing to compare a stated accident date with.")
        elif t in _ENGLISH_RULE_TYPES and run.get("unread"):
            unread = run["unread"]
            nos = sorted(n for v in unread.values() for n in v)
            langs = " and ".join(_LANG_WORD.get(k, k) for k in unread)
            if run.get("read_records") == 0:
                skip(t, "LANGUAGE", f"This check reads English wording and every record is in {langs}, so it could not find anything.")
            else:
                skip(t, "LANGUAGE_PARTIAL", f"This check reads English wording; the records in {langs} were not read.", nos)
    whole = {x["type"] for x in skipped if "record_nos" not in x}
    note = conflicts.accident_date_note(records) if records is not None and "accident_date" not in whole else None
    return {"conflict_types": [t for t in CONFLICT_LABELS if t not in whole], "labels": dict(CONFLICT_LABELS), "skipped": skipped,
            "not_checked": [dict(x) for x in NOT_CHECKED], "notes": [note] if note else []}
app/backend/conflict_candidates.py:263:def checks(run: dict = None, state: str = "complete", records: list = None) -> dict:
app/backend/pipeline.py:161:def _store_run_checks(conn, cid: str, recs: list, stage: str) -> None:
app/backend/pipeline.py:305:    _store_run_checks(conn, cid, ing["records"], "pending")
app/backend/pipeline.py:388:    _store_run_checks(conn, cid, recs, "pending")           # a run that dies before the conflict stage leaves 'pending' (GET case: RUN_FAILED)
app/backend/pipeline.py:483:    _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
app/backend/present.py:338:            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete", store.load_records(conn, case_id, raw)), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:25:25.366Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $SP/t151-out && sqlite3 t151.db \".tables\" && sqlite3 t151.db \"select name from pragma_table_info('cases')\" | tr '\\n' ' '; echo; sqlite3 t151.db \"select id, status, substr(config,1,300) from cases limit 3\""
}
````

### User / tool · 2026-11-02T14:25:25.480Z

**tool result (error)**
````
Exit code 1
amounts        entries        llm_calls      review_events
cases          flags          records      
id name source raw_text text_sha256 status stage error backend demo_mode config_json injection_records_json created_at run_started_at run_finished_at 
Error: in prepare, no such column: config
  select id, status, substr(config,1,300) from cases limit 3
              error here ---^
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:25:28.639Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $SP/t151-out && sqlite3 t151.db \"select id, name, status, substr(config_json,1,250) from cases\""
}
````

### User / tool · 2026-11-02T14:25:28.729Z

**tool result**
````
_zGDj98RAYbjS312ltzqUw|case lib08 second crash mri after|ready|{"run_checks": {"conflicts_stage": "ran", "read_records": 12, "unread": {}}}
w9w_6My2Q0ZRrzEDjMJ8Uw|case lib09 spanish interpreter espalda|ready|{"run_checks": {"conflicts_stage": "ran", "read_records": 4, "unread": {"es": [2, 4, 7]}}}
pASX53_PV8rGIXOIImrlnQ|case lib11 priors and ledger|ready|{"run_checks": {"conflicts_stage": "ran", "read_records": 9, "unread": {}}}
IR_5Ynjp-UMQ5zEp_4oS_g||ready|{"run_checks": {"conflicts_stage": "ran", "read_records": 9, "unread": {}}}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:25:35.623Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $SP/t151-scripts && cat > mk.py <<'EOF'\nimport json, sys, time, urllib.request\nU=\"http://127.0.0.1:7951/api/\"\ndef call(m,p,b=None):\n    rq=urllib.request.Request(U+p,data=None if b is None else json.dumps(b).encode(),headers={\"Content-Type\":\"application/json\"},method=m)\n    return json.loads(urllib.request.urlopen(rq).read() or b\"{}\")\nfor lib in sys.argv[1:]:\n    t=call(\"POST\",\"cases\",{\"library\":lib})[\"token\"]; call(\"POST\",\"cases/%s/run\"%t,{})\n    while call(\"GET\",\"cases/%s/status\"%t)[\"status\"] not in (\"ready\",\"failed\"): time.sleep(.5)\n    print(lib,t)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python mk.py case_lib08_second_crash_mri_after case_lib11_priors_and_ledger case_lib09_spanish_interpreter_espalda"
}
````

### User / tool · 2026-11-02T14:25:37.397Z

**tool result**
````
case_lib08_second_crash_mri_after FKjcKEfqY4mGTF7rtKkVOQ
case_lib11_priors_and_ledger fMY9D46F9AZVeZkWXiWhOg
case_lib09_spanish_interpreter_espalda qTbB8oBLqJzelDy5U5uAnA
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:25:47.434Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $SP/t151-out && sqlite3 t151.db \"update cases set config_json='{}' where id='FKjcKEfqY4mGTF7rtKkVOQ'; update cases set config_json='{\\\"run_checks\\\": {\\\"conflicts_stage\\\": \\\"skipped\\\", \\\"read_records\\\": 9, \\\"unread\\\": {}}}' where id='fMY9D46F9AZVeZkWXiWhOg'; update cases set config_json='{\\\"run_checks\\\": {\\\"conflicts_stage\\\": \\\"ran\\\", \\\"read_records\\\": 0, \\\"unread\\\": {\\\"es\\\": [1,2,3,4,5,6,7]}}}' where id='qTbB8oBLqJzelDy5U5uAnA';\" && cd ../t151-scripts && cat > probe2.py <<'EOF'\nimport json, sys, urllib.request\nfrom playwright.sync_api import sync_playwright\nOUT=sys.argv[1]; URL=\"http://127.0.0.1:7951/\"\nwith sync_playwright() as p:\n    b=p.chromium.launch()\n    for name,tok in zip(sys.argv[2::2], sys.argv[3::2]):\n        pg=b.new_context(viewport={\"width\":1440,\"height\":1000}).new_page()\n        pg.goto(URL+\"#/case/\"+tok); pg.wait_for_selector(\"[data-testid=review-counts]\",timeout=60000); pg.wait_for_timeout(800)\n        g=pg.locator(\"[data-group=conflict]\").first\n        print(\"=== \"+name); print(g.inner_text())\n        print(\"cov open:\", g.locator(\"[data-testid=conflict-coverage]\").evaluate(\"(d)=>d.open\"))\n        c=json.loads(urllib.request.urlopen(URL+\"api/cases/\"+tok).read()); ck=c[\"checks\"]\n        print(\"API types\",ck[\"conflict_types\"],\"skipped\",[(s[\"type\"],s[\"reason_code\"],s.get(\"record_nos\")) for s in ck[\"skipped\"]],\"notes\",len(ck[\"notes\"]))\n        g.screenshot(path=OUT+\"/%s-group.png\"%name)\n    b.close()\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python probe2.py $SP/t151-out nonerun FKjcKEfqY4mGTF7rtKkVOQ stageskip fMY9D46F9AZVeZkWXiWhOg allspanish qTbB8oBLqJzelDy5U5uAnA 2>&1 | tee $SP/t151-out/probe2.out.txt"
}
````

### User / tool · 2026-11-02T14:25:51.383Z

**tool result**
````
=== nonerun
Conflicts between records (0)

No conflict checks ran for this case. The reasons are listed below.

Did not run on this case, or not on every record (4): the group above says nothing about these.

A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early This case was analysed before the record of what ran was kept, so nothing is claimed about this check. Run it again to check.
A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record This case was analysed before the record of what ran was kept, so nothing is claimed about this check. Run it again to check.
A stated accident date against the dates of the records, or two different stated accident dates This case was analysed before the record of what ran was kept, so nothing is claimed about this check. Run it again to check.
The same clinician named under two different practice names This case was analysed before the record of what ran was kept, so nothing is claimed about this check. Run it again to check.

Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.

What the conflict check covers (no checks ran)

Checked: No conflict checks ran for this case.

Not checked: anything not listed above, including these, is not looked for. Read the records for them.

Medication doses that differ between records
Left versus right across records (checked only inside one summary)
A diagnosis that differs or is withdrawn between records
Pain scores that differ on the same day
Plans and outcomes measured in months
Patient history reported by a relative
cov open: True
API types [] skipped [('plan_vs_early_end', 'NOT_RUN', None), ('denial_vs_history', 'NOT_RUN', None), ('accident_date', 'NOT_RUN', None), ('provider_name', 'NOT_RUN', None)] notes 0
=== stageskip
Conflicts between records (2)
Records differ on a fact
Quote matches

Fennimoor Spine Clinic, new patient intake form (OCR text) (March 27, 2026): “Prior accidents? Yes [ ] No [X].” Dr. Hesper Alderton, primary care (March 4, 2026): “History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.”

Record 6 · Fennimoor Spine Clinic, new patient intake form (OCR text)
Prior accidents? Yes [ ] No [X].
Quoted line from this record: How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7.
Record 1 · Dr. Hesper Alderton, primary care
History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.
Open records 6 and 1
Why this status
Accept
Edit note
Dismiss
Dismiss with reason…
Audit
Records differ on a fact
Quote matches

Fennimoor Spine Clinic, new patient intake form (OCR text) (March 27, 2026): “Prior injuries? Yes [ ] No IX].” Dr. Hesper Alderton, primary care (March 4, 2026): “History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.”

Record 6 · Fennimoor Spine Clinic, new patient intake form (OCR text)
Prior injuries? Yes [ ] No IX].
Quoted line from this record: How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7.
Record 1 · Dr. Hesper Alderton, primary care
History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.
Open records 6 and 1
Why this status
Accept
Edit note
Dismiss
Dismiss with reason…
Audit
Note 1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care.

Did not run on this case, or not on every record (2): the group above says nothing about these.

A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early The run reached its time limit before the comparison between records. Run it again to check.
A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record The run reached its time limit before the comparison between records. Run it again to check.

Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.

What the conflict check covers (2 kinds checked)
cov open: False
API types ['accident_date', 'provider_name'] skipped [('plan_vs_early_end', 'STAGE_SKIPPED', None), ('denial_vs_history', 'STAGE_SKIPPED', None)] notes 1
=== allspanish
Conflicts between records (0)

No conflicts found among the kinds checked. Other kinds of conflict are not checked.

Did not run on this case, or not on every record (3): the group above says nothing about these.

A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early This check reads English wording and every record is in Spanish, so it could not find anything.
A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record This check reads English wording and every record is in Spanish, so it could not find anything.
A stated accident date against the dates of the records, or two different stated accident dates This check reads English wording and every record is in Spanish, so it could not find anything.

Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.

What the conflict check covers (1 kind checked)

Checked: the code compares records for these kinds of conflict only.

The same clinician named under two different practice names

Not checked: anything not listed above, including these, is not looked for. Read the records for them.

Medication doses that differ between records
Left versus right across records (checked only inside one summary)
A diagnosis that differs or is withdrawn between records
Pain scores that differ on the same day
Plans and outcomes measured in months
Patient history reported by a relative
cov open: True
API types ['provider_name'] skipped [('plan_vs_early_end', 'LANGUAGE', None), ('denial_vs_history', 'LANGUAGE', None), ('accident_date', 'LANGUAGE', None)] notes 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:26:00.241Z

**tool call — Bash**
````
{
 "command": "ls evals/library 2>/dev/null | head -3; f=$(ls evals/*/*lib09* 2>/dev/null | head -3); echo $f; python3 - <<'EOF'\nimport glob,re\nfor f in glob.glob(\"/Users/arsis/zlayt-pm-project/evals/**/*lib09*\", recursive=True)[:3]: print(f)\nEOF"
}
````

### User / tool · 2026-11-02T14:26:00.376Z

**tool result**
````
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
evals/library/case_lib09_spanish_interpreter_espalda.expected.json evals/library/case_lib09_spanish_interpreter_espalda.txt
/Users/arsis/zlayt-pm-project/evals/library/case_lib09_spanish_interpreter_espalda.expected.json
/Users/arsis/zlayt-pm-project/evals/library/case_lib09_spanish_interpreter_espalda.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:26:02.175Z

**tool call — Bash**
````
{
 "command": "grep -n \"^Date\\|^Source\\|^=== \\|Excerpt:\" evals/library/case_lib09_spanish_interpreter_espalda.txt | head -40; grep -n -i \"left\\|right\\|izquierd\\|derech\\|consciencia\\|conocimiento\" evals/library/case_lib09_spanish_interpreter_espalda.txt | head -20"
}
````

### User / tool · 2026-11-02T14:26:02.277Z

**tool result**
````
3:=== Record 1 ===
4:Date: 2026-03-03
5:Source: Quillmere Regional ED
6:Excerpt: "Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940."
8:=== Record 2 ===
9:Date: 14/04/2026
10:Source: Consultorio Médico Aguaclara, nota de consulta
11:Excerpt: "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00."
13:=== Record 3 ===
14:Date: 2026-04-21
15:Source: Dr. Lucan Ostrowe, orthopedics, new patient
16:Excerpt: "Interpreter: patient's daughter. Patient states she fell in the parking lot after a car brushed her. Right shoulder pain 6/10. MRI right shoulder ordered."
18:=== Record 4 ===
19:Date: 03/05/2026
20:Source: Consultorio Médico Aguaclara, formulario de admisión (OCR)
21:Excerpt: "Fecha de ingreso: 03/O5/2026. Motivo de la visita: dolor de espaIda y hombro derecho. Accidentes anteriores? Si [ ] No [X]. Firma de la paciente: illegible."
23:=== Record 5 ===
24:Date: 2026-05-05
25:Source: Cinder Valley Imaging, right shoulder MRI
26:Excerpt: "Partial-thickness supraspinatus tear. MRI charge: $2,150."
28:=== Record 6 ===
29:Date: 2026-05-12
30:Source: Dr. Lucan Ostrowe, orthopedics, follow-up
31:Excerpt: "Interpreter: patient's daughter. MRI reviewed. Recommend physical therapy and subacromial injection. Pain 5/10."
33:=== Record 7 ===
34:Date: 2026-05-20
35:Source: Consultorio Médico Aguaclara, estado de cuenta (billing statement)
36:Excerpt: "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00."
6:Excerpt: "Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940."
11:Excerpt: "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00."
16:Excerpt: "Interpreter: patient's daughter. Patient states she fell in the parking lot after a car brushed her. Right shoulder pain 6/10. MRI right shoulder ordered."
21:Excerpt: "Fecha de ingreso: 03/O5/2026. Motivo de la visita: dolor de espaIda y hombro derecho. Accidentes anteriores? Si [ ] No [X]. Firma de la paciente: illegible."
25:Source: Cinder Valley Imaging, right shoulder MRI
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:26:10.535Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list 2>/dev/null | grep -i \"coverage\\|internal notes\\|conflict\" | head; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat $SP/t151-scripts/n5.py 2>/dev/null | head -2; sed -n 1,60p artifacts/review-evidence/T-142-legal-nurse/n5-export-notes.py"
}
````

### User / tool · 2026-11-02T14:26:10.700Z

**tool result**
````
T-033	M2	backend    	done             	P0	AC 8/8	Amounts, running total, gap rule, accident-date conflict, flag templates
T-036	M2	backend    	done             	P0	AC 10/10	LLM flag passes: per-record pre-existing/causation + lexicon floor, conflicts + judges #3/#4
T-048	M2	qa         	done             	P0	AC 2/2	M2 LLM-stage tests first (provider, audited, schemas, judges, flags, pipeline, conflicts, templates)
T-109	M2	architect  	done             	P1	AC 1/1	LLM_VS_CODE row 11: conflicts are code-proposed candidates classified by judge_conflict_v4; model-only flags rejected by the flag judge are suppressed and listed
T-113	M2	backend    	done             	P0	AC 2/2	Conflict judge false agrees on real candidate variants (J3V1 discontinued medicine, J3V9 other driver, J3V13 general denial vs mother's injury, H3V5 semicolon clause)
T-141	M2	backend    	in_progress      	P1	AC 1/1	GATE-M2 major: lib11 intake 'Prior accidents: No' vs PCP note listing 2019/2022 accidents not flagged as a conflict; a false accident-date 'records disagree' conflict is shown instead
T-142	M2	frontend   	in_review        	P1	AC 1/1	GATE-M2 major (legal nurse): conflict empty state overclaims ('No conflicts found') though only plan-vs-early-end and denial-vs-history are checked; laterality (lib09 L vs R shoulder) and LOC (lib08) contradictions are not
T-151	M2	frontend   	in_review        	P1	AC 1/1	UI: render checks.skipped[] (why a check did not run for this case) and checks.notes[] ('N records predate the stated accident date') in the Conflicts group (T-141 r2 follow-up to T-142)
import json, urllib.request
BASE = "http://127.0.0.1:7931"
def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"null")
out = []
for lib in ("case_lib09_spanish_interpreter_espalda", "case_lib08_second_crash_mri_after"):
    s, c = call("POST", "/api/cases", {"library": lib}); tok = c["token"]
    call("POST", "/api/cases/%s/run" % tok)
    import time
    for _ in range(150):
        s, st = call("GET", "/api/cases/%s/status" % tok)
        if st.get("status") in ("ready", "done_with_errors"): break
        time.sleep(1)
    s, cs = call("GET", "/api/cases/%s" % tok)
    done = 0
    for e in cs["entries"]:
        s, r = call("POST", "/api/cases/%s/items/%s/review" % (tok, e["id"]), {"action": "accept"})
        if s == 200: done += 1
    s, ex = call("GET", "/api/cases/%s/export" % tok)
    out.append("== %s accepted=%d export=%s" % (lib, done, s))
    if s == 200:
        nt = ex["internal_notes_text"]; lt = ex["letter_text"]
        import re
        hits = [l for l in (nt + "\n" + lt).splitlines() if re.search(r"conflict|not checked|checked", l, re.I)]
        out.append("lines mentioning conflict/checked in letter+notes: %s" % hits)
        out.append("notes headings: %s" % [l for l in nt.splitlines() if l.isupper()])
    else:
        out.append(json.dumps(ex)[:500])
open("/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-142-legal-nurse/n5-export-notes.out.txt", "w").write("\n".join(out) + "\n")
print("\n".join(out))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:26:18.950Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $SP/t151-scripts && cat > exp.py <<'EOF'\nimport json, re, urllib.request, urllib.error\nU=\"http://127.0.0.1:7951/api/\"\ndef call(m,p,b=None):\n    rq=urllib.request.Request(U+p,data=None if b is None else json.dumps(b).encode(),headers={\"Content-Type\":\"application/json\"},method=m)\n    try:\n        r=urllib.request.urlopen(rq); return r.status,json.loads(r.read() or b\"null\")\n    except urllib.error.HTTPError as e: return e.code,json.loads(e.read() or b\"null\")\nfor name,tok in ((\"lib09\",\"w9w_6My2Q0ZRrzEDjMJ8Uw\"),(\"lib08\",\"_zGDj98RAYbjS312ltzqUw\"),(\"lib11\",\"pASX53_PV8rGIXOIImrlnQ\")):\n    s,c=call(\"GET\",\"cases/\"+tok); n=0\n    for e in c[\"entries\"]:\n        if call(\"POST\",\"cases/%s/items/%s/review\"%(tok,e[\"id\"]),{\"action\":\"accept\"})[0]==200: n+=1\n    s,ex=call(\"GET\",\"cases/%s/export\"%tok); print(\"==\",name,\"accepted\",n,\"export\",s)\n    if s==200:\n        t=ex[\"internal_notes_text\"]+\"\\n\"+ex[\"letter_text\"]\n        print(\" lines with conflict/checked/not checked:\",[l for l in t.splitlines() if re.search(r\"conflict|checked|did not run|predate\",l,re.I)])\n        print(\" headings:\",[l for l in ex[\"internal_notes_text\"].splitlines() if l.isupper()])\n    else: print(json.dumps(ex)[:400])\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python exp.py 2>&1 | tee $SP/t151-out/export.out.txt"
}
````

### User / tool · 2026-11-02T14:26:19.464Z

**tool result**
````
== lib09 accepted 5 export 200
 lines with conflict/checked/not checked: []
 headings: ['INTERNAL REVIEW NOTES — DO NOT SEND', 'FLAGS ACCEPTED', 'FLAGS DISMISSED', 'AMOUNTS NOT TOTALED', 'RECORDS NOT IN THE TREATMENT SECTION', 'EDITED ITEMS', 'PENDING ITEMS NOT INCLUDED']
== lib08 accepted 12 export 200
 lines with conflict/checked/not checked: []
 headings: ['INTERNAL REVIEW NOTES — DO NOT SEND', 'FLAGS ACCEPTED', 'FLAGS DISMISSED', 'AMOUNTS NOT TOTALED', 'RECORDS NOT IN THE TREATMENT SECTION', 'EDITED ITEMS', 'PENDING ITEMS NOT INCLUDED']
== lib11 accepted 8 export 200
 lines with conflict/checked/not checked: ['- Record 1 (Dr. Hesper Alderton, primary care, March 4, 2026): "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy." Conflict, other fact mismatch; prior condition.', '- Record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026): "Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]." Conflict, other fact mismatch; prior condition.', '- Flag, Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior accidents? Yes [ ] No [X]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."', '- Flag, Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior injuries? Yes [ ] No IX]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."']
 headings: ['INTERNAL REVIEW NOTES — DO NOT SEND', 'FLAGS ACCEPTED', 'FLAGS DISMISSED', 'AMOUNTS NOT TOTALED', 'RECORDS NOT IN THE TREATMENT SECTION', 'EDITED ITEMS', 'PENDING ITEMS NOT INCLUDED']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:26:27.712Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-out/lib09_spanish_interpreter_espalda-group.png"
}
````

### User / tool · 2026-11-02T14:26:27.721Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:26:30.335Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-out/lib11_priors_and_ledger-group.png"
}
````

### User / tool · 2026-11-02T14:26:30.345Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:26:37.328Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $SP/t151-25f585c && grep -n \"E2E_BASE_URL\\|^BASE\" tests/e2e/conftest.py | head -3; E2E_BASE_URL=http://127.0.0.1:7951 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e/test_conflict_skipped.py tests/e2e/test_conflict_coverage.py -q 2>&1 | tail -8 | tee $SP/t151-out/e2e.out.txt"
}
````

### User / tool · 2026-11-02T14:26:59.189Z

**tool result**
````
88:BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
96:    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
97:    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
..............                                                           [100%]
14 passed in 21.52s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:27:07.425Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $SP/t151-scripts && cat > dis.py <<'EOF'\nimport json, urllib.request\nfrom playwright.sync_api import sync_playwright\nU=\"http://127.0.0.1:7951/\"; tok=\"fMY9D46F9AZVeZkWXiWhOg\"\nfor f in (\"f_cx1\",\"f_cx2\"):\n    rq=urllib.request.Request(U+\"api/cases/%s/items/%s/review\"%(tok,f),data=json.dumps({\"action\":\"dismiss\"}).encode(),headers={\"Content-Type\":\"application/json\"},method=\"POST\")\n    print(f, urllib.request.urlopen(rq).status)\nwith sync_playwright() as p:\n    b=p.chromium.launch(); pg=b.new_page(viewport={\"width\":1440,\"height\":1000})\n    pg.goto(U+\"#/case/\"+tok); pg.wait_for_selector(\"[data-testid=review-counts]\"); pg.wait_for_timeout(800)\n    g=pg.locator(\"[data-group=conflict]\").first\n    t=g.inner_text(); print(t[:1500])\n    b.close()\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python dis.py 2>&1 | tee $SP/t151-out/dismiss.out.txt"
}
````

### User / tool · 2026-11-02T14:27:07.693Z

**tool result**
````
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-scripts/dis.py", line 2, in <module>
    from playwright.sync_api import sync_playwright
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/__init__.py", line 26, in <module>
    import playwright.sync_api._generated
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 52, in <module>
    from playwright._impl._assertions import (
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_assertions.py", line 20, in <module>
    from playwright._impl._connection import format_call_log
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 15, in <module>
    import asyncio
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/asyncio/__init__.py", line 8, in <module>
    from .base_events import *
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/asyncio/base_events.py", line 40, in <module>
    from . import coroutines
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/asyncio/coroutines.py", line 4, in <module>
    import inspect
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/inspect.py", line 146, in <module>
    import dis
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t151-scripts/dis.py", line 2, in <module>
    from playwright.sync_api import sync_playwright
ImportError: cannot import name 'sync_playwright' from partially initialized module 'playwright.sync_api' (most likely due to a circular import) (/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/__init__.py)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:27:08.493Z

My script name `dis.py` shadows the stdlib module; rename.

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:27:12.040Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\ncd $SP/t151-scripts && mv dis.py dismiss_probe.py && rm -rf __pycache__ && /Users/arsis/zlayt-pm-project/.venv/bin/python dismiss_probe.py 2>&1 | tee $SP/t151-out/dismiss.out.txt"
}
````

### User / tool · 2026-11-02T14:27:13.625Z

**tool result**
````
f_cx1 200
f_cx2 200
Conflicts between records (0)

No open conflicts among the kinds checked (2 dismissed, below). Other kinds are not checked.

Note 1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care.

Did not run on this case, or not on every record (2): the group above says nothing about these.

A stated plan of care (visit count, or frequency times weeks) against a later record where the course ended early The run reached its time limit before the comparison between records. Run it again to check.
A denial of prior problems (including a form answered No) against a prior condition, surgery or accident in another record The run reached its time limit before the comparison between records. Run it again to check.

Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.

What the conflict check covers (2 kinds checked)

Checked: the code compares records for these kinds of conflict only.

A stated accident date against the dates of the records, or two different stated accident dates
The same clinician named under two different practice names

Not checked: anything not listed above, including these, is not looked for. Read the records for them.

Medication doses that differ between records
Left versus
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:27:28.267Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nPID=$(cat $SP/t151-out/server.pid); kill $PID; sleep 1; ps -p $PID >/dev/null 2>&1; echo \"ps exit $?\"; curl -s -o /dev/null -w \"curl %{http_code}\\n\" http://127.0.0.1:7951/\nE=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-151-legal-nurse; mkdir -p $E\ncp $SP/t151-scripts/probe.py $SP/t151-scripts/probe2.py $SP/t151-scripts/exp.py $SP/t151-scripts/dismiss_probe.py $SP/t151-scripts/mk.py $SP/t151-scripts/launch.py $E/\ncp $SP/t151-out/probe.out.txt $SP/t151-out/probe2.out.txt $SP/t151-out/export.out.txt $SP/t151-out/dismiss.out.txt $SP/t151-out/e2e.out.txt $E/\ncp $SP/t151-out/lib09_spanish_interpreter_espalda-group.png $SP/t151-out/lib11_priors_and_ledger-group.png $SP/t151-out/lib08_second_crash_mri_after-group.png $SP/t151-out/sample-group.png $SP/t151-out/nonerun-group.png $SP/t151-out/allspanish-group.png $E/ ; ls $E | wc -l"
}
````

### User / tool · 2026-11-02T14:27:29.399Z

**tool result**
````
ps exit 1
curl 000
      17
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:28:03.307Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-151-legal-nurse.md",
 "content": "# T-151 legal-nurse review (legal-nurse-reviewer, Linda Chen, RN, LNC persona)\n\nVerdict: **pass** (0 blockers, 0 majors, 3 minors, 2 nits). Pinned commit 25f585c (HEAD at review start; contains b5f40c0 and 94c30db). I ran `git archive 25f585c` into the scratchpad (`t151-25f585c`) and served it on 127.0.0.1:7951 with `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local` and a scratchpad DB. The server (PID 21724) was stopped by PID: `ps` exit 1, curl 000. Scripts, outputs and screenshots: `artifacts/review-evidence/T-151-legal-nurse/`. This reads what the tool tells the reader about what was and was not checked; it is not a clinical opinion on any record.\n\n## The five checks you asked for\n\n1. **Names exactly the checks that ran: yes.** lib08, lib11 and the sample list four checked kinds, and the on-screen list equals `GET case checks.conflict_types` labels (`probe.out.txt`). lib09 lists one (the clinician-name check); the three English-wording checks that read only part of the case are moved out of Checked into the skipped box, never listed as checked (`probe.out.txt` lib09: \"What the conflict check covers (1 kind checked)\", checked item \"The same clinician named under two different practice names\").\n2. **Skipped checks with plain reasons and record numbers: yes.** lib09 shows three skipped items, each with \"This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read.\" The Spanish records in the source are 2 (Consultorio nota), 4 (formulario OCR) and 7 (estado de cuenta) (`evals/library/case_lib09_spanish_interpreter_espalda.txt`), so the numbers are right. This closes my T-142 r1 major (the panel claimed a denial check ran on Spanish wording it cannot read). English-only cases (lib08, lib11, sample) show no skipped box.\n3. **Notes are information, not conflicts: yes.** lib11: heading \"Conflicts between records (2)\" counts the two cards only; the \"records predate the accident\" line is a \"Note\" chip paragraph with no accept or dismiss, no item id, not counted (`lib11_priors_and_ledger-group.png`). It stays after I dismissed both conflicts.\n4. **Always a \"Not checked\" line naming side and loss of consciousness: yes.** Present, always visible (not in a collapsed block) on lib08, lib09, lib11, sample, and on the all-skipped, stage-skipped and all-Spanish variants: \"Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these.\"\n5. **When nothing ran, it says so: yes.** I took a lib08 copy and removed its stored run summary in my scratchpad DB (the \"analysed before the record of what ran was kept\" shape): API `conflict_types: []`, four skipped NOT_RUN; the page reads \"No conflict checks ran for this case. The reasons are listed below.\", the coverage summary reads \"(no checks ran)\", no empty list and no \"No conflicts found\" (`probe2.out.txt` \"nonerun\"). A stage-skipped lib11 copy lists the two pair checks as skipped with \"The run reached its time limit...\" and keeps the two code checks as checked.\n\nDeterministic: `tests/e2e/test_conflict_skipped.py` and `test_conflict_coverage.py` from the archive against my server: 14 passed (`e2e.out.txt`).\n\n## Findings\n\n**F-1 (minor). The lead sentence is the same on lib08 (four kinds ran) and on a case where one kind ran.** On lib09 and on an all-Spanish case the first line under the heading is \"No conflicts found among the kinds checked. Other kinds of conflict are not checked.\" (`probe.out.txt`, `probe2.out.txt` \"allspanish\": one kind checked, three read no record). The skipped box sits right under it, so this is not the bare all-clear from GATE-M2, but a reader who stops at the first line gets the same assurance as on a full run. When nothing ran the page does add \"The reasons are listed below\" (`flags.js` `NONE_RAN` line); the partial case gets no such pointer. Fix: when `skipped` is not empty, end the lead with \"N checks did not run or did not read every record; see below.\" Test: lib09 lead line contains \"did not run\" or \"did not read\"; lib08's does not.\n\n**F-2 (minor). The notes line does not say which record.** lib11: \"1 record predates the stated accident date, March 18, 2026. ...\" The API carries `record_nos: [1]` and the page prints it nowhere (`probe.out.txt` lib11 API notes). The skipped items do print record numbers, so the paralegal gets numbers for one and has to hunt for the other. Fix: append \"Record 1.\" (or \"Records 1 and 3.\") from `record_nos`. Test: lib11 note text contains \"Record 1\".\n\n**F-3 (minor). Two \"not checked\" lists on one screen disagree.** The always-visible line is page-written and names loss of consciousness; the server's `not_checked` list (which the coverage block prints) still has dosage, left versus right, diagnosis, pain score, months and relative history, with no loss of consciousness line (`probe.out.txt` API not_checked). My T-142 F-2 asked for the server list to carry it. T-142's own AC says the text comes from the API so it cannot drift; this line can. Fix: add a `loc_history` entry to `NOT_CHECKED` in `conflict_candidates.py` and render the line from the list, or make the line a literal copy with a test that every named kind is in the server list. Test: lib08 `checks.not_checked` contains an LOC entry.\n\n**F-4 (nit). Label and reason run together.** lib09 skipped item reads \"...a later record where the course ended early This check reads English wording; ...\" with no separator (`lib09_spanish_interpreter_espalda-group.png`). It also says \"were not read\" twice. Add a colon or line break; drop one of the two sentences.\n\n**F-5 (nit). Note wording presumes.** \"read them to check they are earlier care\" assumes the record is earlier care. Server text (api.md T-141 r3). Better: \"read them to check whether they are earlier care.\"\n\n## What I ran\n\n1. `git rev-parse --short HEAD` = 25f585c; `git archive 25f585c | tar -x -C <scratchpad>/t151-25f585c`; server on 7951 under `.venv/bin/python -I launch.py` (launcher in evidence dir); curl 200.\n2. `probe.py`: sample (pasted) and lib08, lib09, lib11 (created through the API, opened at `#/case/<token>`): read the Conflicts group text, notes, skipped items, checked and not-checked items, compared with `GET /api/cases/{token}` `checks` and conflict flags; screenshots of each group.\n3. `probe2.py`: three scratchpad-DB variants (no stored run summary; stage skipped; all records Spanish) for the \"nothing ran\" and partial cases.\n4. `dismiss_probe.py`: dismissed both lib11 conflicts, re-read the group.\n5. `exp.py`: lib09, lib08, lib11 with every entry accepted, export notes searched for conflict or coverage wording (only the lib11 flag lines match; no coverage line on any; see T-142 r2 F-1).\n6. Pytest: 14 passed. Read: `app/frontend/flags.js` diff of b5f40c0 and 94c30db, `app/backend/conflict_candidates.py` `checks()`, `memory/contracts/api.md` checks paragraph, cards T-151 and T-142, `evals/library/case_lib09...txt`. Not exercised: live-model behavior (fixture only); narrow-screen layout (outside my lens).\n\n```json\n{\"card\": \"T-151\", \"persona\": \"legal-nurse-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive 25f585c (HEAD at review start; includes b5f40c0, 94c30db) served on http://127.0.0.1:7951 (PID 21724, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; sample case plus library cases lib08, lib09 (Spanish), lib11 and three scratchpad-DB variants (no stored run summary, stage skipped, all Spanish)\",\n \"exercised\": [\n  \"git archive 25f585c into a fresh scratchpad dir; server on 7951 via -I launcher; curl 200; stopped by PID 21724 (ps exit 1, curl 000)\",\n  \"browser 1440x1000: sample, lib08, lib09, lib11 Conflicts group text, notes, skipped items, checked and not-checked items compared with GET case checks and conflict flags (probe.py); screenshots read: lib09 and lib11 groups\",\n  \"three scratchpad-DB variants of run_checks (removed, stage skipped, all Spanish) to exercise 'no checks ran', STAGE_SKIPPED and LANGUAGE (probe2.py)\",\n  \"dismissed both lib11 conflicts and re-read the group: note, skipped box and not-checked line stay (dismiss_probe.py)\",\n  \"lib09, lib08, lib11 with every entry accepted, GET export, internal notes and letter searched for coverage wording (exp.py)\",\n  \"tests/e2e/test_conflict_skipped.py and test_conflict_coverage.py from the archive against my server: 14 passed\",\n  \"read flags.js diff of b5f40c0 and 94c30db, conflict_candidates.checks(), api.md checks paragraph, cards T-151 and T-142, library case lib09 source. Not exercised: live model (fixture only), narrow-screen layout\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"names_checks_that_ran\": 5, \"skipped_reasons_and_records\": 5, \"notes_as_info_not_conflicts\": 5, \"not_checked_line_side_and_loc\": 5, \"nothing_ran_honesty\": 5, \"lead_sentence_honesty_on_partial_runs\": 3, \"no_inferred_dx_severity_causation\": 5},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"Lead sentence 'No conflicts found among the kinds checked' is identical when four kinds ran and when one ran\",\n   \"evidence\": \"probe.out.txt lib09: 'No conflicts found among the kinds checked. Other kinds of conflict are not checked.' above a box listing 3 skipped; probe2.out.txt allspanish: same line with 1 kind checked and 3 skipped LANGUAGE; flags.js NONE_RAN pointer ('The reasons are listed below.') is added only when conflict_types is empty\",\n   \"why_it_matters\": \"A reader who stops at the first line gets the same assurance as on a full run, for a case where the English-wording checks read few or no records.\",\n   \"fix\": \"When skipped is not empty, end the lead with 'N checks did not run or did not read every record; see below.'\",\n   \"acceptance_test\": \"lib09 lead line contains 'did not run' or 'did not read'; lib08 lead line does not.\"},\n  {\"severity\": \"minor\", \"title\": \"Info note does not name the record it is about, though the API sends record_nos\",\n   \"evidence\": \"probe.out.txt lib11 API notes record_nos [1], page text 'Note 1 record predates the stated accident date, March 18, 2026. ...' with no record number; skipped items do print 'Records 2, 4 and 7 were not read.'\",\n   \"why_it_matters\": \"The paralegal has to search the case for the earlier record the note asks her to read.\",\n   \"fix\": \"Append 'Record N.' from record_nos to the note line.\",\n   \"acceptance_test\": \"lib11 note text contains 'Record 1'.\"},\n  {\"severity\": \"minor\", \"title\": \"Always-visible not-checked line is page-written and names loss of consciousness; the server's not_checked list does not\",\n   \"evidence\": \"flags.js notCheckedLine (literal text); probe.out.txt API not_checked types dosage, laterality, diagnosis, pain_score, treatment_duration_months, informant_history (no loc); coverage block lists six items, none about loss of consciousness\",\n   \"why_it_matters\": \"Two not-checked lists on one screen differ, and the page line can drift from what the server says (T-142 AC: text from the API; my T-142 F-2).\",\n   \"fix\": \"Add a loc_history entry to NOT_CHECKED in conflict_candidates.py and print the line from the list, or test that every kind the line names is in the server list.\",\n   \"acceptance_test\": \"lib08 GET case checks.not_checked contains a loss-of-consciousness entry.\"},\n  {\"severity\": \"nit\", \"title\": \"Skipped item label and reason run together; 'were not read' appears twice\",\n   \"evidence\": \"lib09_spanish_interpreter_espalda-group.png: '...course ended early This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read.'\",\n   \"why_it_matters\": \"Reads as one run-on sentence.\",\n   \"fix\": \"Colon or line break after the label; keep one 'not read' sentence.\",\n   \"acceptance_test\": \"Skipped item text has a separator between label and reason.\"},\n  {\"severity\": \"nit\", \"title\": \"Note wording presumes the record is earlier care\",\n   \"evidence\": \"probe.out.txt lib11 note: 'read them to check they are earlier care.'\",\n   \"why_it_matters\": \"Suggests the answer; the tool should only point to the record.\",\n   \"fix\": \"'read them to check whether they are earlier care.'\",\n   \"acceptance_test\": \"Note text contains 'whether'.\"}\n ],\n \"whats_right\": [\n  \"lib09 names the Spanish records (2, 4 and 7, correct against the source) as not read by each English-wording check and does not list those checks as checked.\",\n  \"Notes render as a Note chip line with no flag controls and are not counted in the Conflicts heading; they survive dismissing the conflicts.\",\n  \"When no check ran the page says 'No conflict checks ran for this case' with each reason and no empty list or 'No conflicts found'.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T14:28:03.472Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-151-legal-nurse.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:28:21.989Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-142-legal-nurse-r2.md",
 "content": "# T-142 legal-nurse re-check, round 2 (legal-nurse-reviewer, Linda Chen, RN, LNC persona)\n\nVerdict: **pass** (0 blockers, 0 majors, 2 minors carried from round 1). Pinned commit 25f585c (HEAD at review start). Same run as T-151: `git archive 25f585c`, fixture backend, `ZLAYT_MODE=local`, scratchpad DB, 127.0.0.1:7951, server PID 21724 stopped by PID (`ps` exit 1, curl 000). Evidence: `artifacts/review-evidence/T-151-legal-nurse/`. Round 1 is `reviews/T-142-legal-nurse.md` (changes: 1 major, 3 minors). This is a read of what the tool tells the reader about coverage, not a clinical opinion.\n\n## Round 1 findings, one by one\n\n- **F-1 major (Spanish case lists English-only checks as run): fixed.** lib09 now lists the plan-vs-early-end, denial-vs-history and accident-date checks under \"Did not run on this case, or not on every record (3)\" with \"This check reads English wording; the records in Spanish were not read. Records 2, 4 and 7 were not read.\" Checked shows one kind (clinician name). Records 2, 4 and 7 are the Spanish ones in the source (`evals/library/case_lib09_spanish_interpreter_espalda.txt`; record 4 is the \"Accidentes anteriores? Si [ ] No [X]\" form I probed in round 1). The same sentence is absent on lib08, lib11 and the sample. An all-Spanish variant says \"every record is in Spanish, so it could not find anything.\" (`probe.out.txt`, `probe2.out.txt`). The fix is at the source (T-141 r2 `checks.skipped[]`) plus the UI render (T-151). Acceptance test from round 1 met.\n- **F-2 minor (loss of consciousness not named): fixed on screen, open at the source.** lib08 shows \"Not checked: left versus right across records, a change in loss of consciousness history between records, ...\" always visible. The server list is unchanged (`not_checked` types: dosage, laterality, diagnosis, pain_score, treatment_duration_months, informant_history), so the coverage block's list still has no loss of consciousness line (see T-151 F-3; open as minor).\n- **F-3 minor (others-not-checked hidden when conflicts show): fixed.** On the sample and lib11 the not-checked line sits outside the collapsed coverage block, visible with two conflicts listed.\n- **F-4 minor (export internal notes carry no coverage line): still open.** lib09, lib08 and lib11 with every entry accepted: internal notes headings are FLAGS ACCEPTED, FLAGS DISMISSED, AMOUNTS NOT TOTALED, RECORDS NOT IN THE TREATMENT SECTION, EDITED ITEMS, PENDING ITEMS NOT INCLUDED; no line mentions what the conflict check covered or skipped (`export.out.txt`). The T-151 handoff says \"coverage line in internal notes is backend\"; no open card I could find in `board.py list` names it (T-141 is in progress, its AC is the lib11 case). It stays minor because the card's AC covers the screen only; the point is unchanged: off the screen the notes say nothing about coverage, including \"Records 2, 4 and 7 were not read\" on lib09.\n\nRound 1 positives still hold: the empty state is never a bare \"No conflicts found.\" (lib08 reads \"No conflicts found among the kinds checked. Other kinds of conflict are not checked.\"), and the checked list on screen equals the API list. Deterministic: `test_conflict_coverage.py` with `test_conflict_skipped.py`: 14 passed against my server; the real-backend variant now runs.\n\nNew observation from T-151 that touches this card (minor, filed there as F-1): on lib09 and an all-Spanish case the lead sentence is the same as on a full run; the skipped box under it carries the difference.\n\n## What I ran\n\nSee `reviews/T-151-legal-nurse.md` and the evidence dir for the full list. For this card: lib08, lib09, lib11 and the sample in a browser (Conflicts group text against `GET case checks`); export of lib09, lib08, lib11 with every entry accepted (`exp.py`, `export.out.txt`); pytest 14 passed; read cards T-142 and T-151, `flags.js`, `conflict_candidates.checks()`.\n\n```json\n{\"card\": \"T-142\", \"persona\": \"legal-nurse-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"round 2 re-check; git archive 25f585c (includes c5c18a6, b5f40c0, 94c30db) served on http://127.0.0.1:7951 (PID 21724, stopped); fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, scratchpad DB; sample case plus lib08, lib09 (Spanish), lib11\",\n \"exercised\": [\n  \"git archive 25f585c into a fresh scratchpad dir; server on 7951; curl 200; stopped by PID 21724 (ps exit 1, curl 000)\",\n  \"browser: sample, lib08, lib09, lib11 Conflicts group text compared with GET /api/cases/{token} checks (probe.py in artifacts/review-evidence/T-151-legal-nurse/)\",\n  \"scratchpad-DB variants: no stored run summary, stage skipped, all-Spanish run summary (probe2.py)\",\n  \"lib09, lib08, lib11 with every entry accepted: GET export, internal notes and letter searched for coverage wording (exp.py, export.out.txt)\",\n  \"tests/e2e/test_conflict_coverage.py and test_conflict_skipped.py from the archive against my server: 14 passed\",\n  \"read reviews/T-142-legal-nurse.md, cards T-142 and T-151, flags.js, conflict_candidates.checks(), lib09 source. Not exercised: live model, narrow-screen layout\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"conflict_coverage_disclosure\": 5, \"empty_state_honesty\": 4, \"api_sourced_text\": 4, \"spanish_honesty\": 5, \"no_inferred_dx_severity_causation\": 5},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"Round 1 F-4 still open: export internal notes carry no conflict-coverage line\",\n   \"evidence\": \"export.out.txt: lib09 and lib08 'lines with conflict/checked/not checked: []'; headings FLAGS ACCEPTED, FLAGS DISMISSED, AMOUNTS NOT TOTALED, RECORDS NOT IN THE TREATMENT SECTION, EDITED ITEMS, PENDING ITEMS NOT INCLUDED; T-151 handoff: 'coverage line in internal notes is backend'; no board card in `board.py list` names it\",\n   \"why_it_matters\": \"Once she leaves the screen the notes say nothing about what the conflict check covered, including the Spanish records it did not read.\",\n   \"fix\": \"One internal-notes line from the same checks: 'Conflict check covered: ...; did not run on: ...; not checked: ...', with record numbers for skipped items. Open a backend card.\",\n   \"acceptance_test\": \"lib09 export internal_notes_text contains that line naming Records 2, 4 and 7; an English-only case lists no skipped records.\"},\n  {\"severity\": \"minor\", \"title\": \"Round 1 F-2 open at the source: server not_checked list has no loss of consciousness entry; the page line is literal text\",\n   \"evidence\": \"probe.out.txt API not_checked types dosage, laterality, diagnosis, pain_score, treatment_duration_months, informant_history; flags.js notCheckedLine literal text names loss of consciousness\",\n   \"why_it_matters\": \"The T-142 AC says the text comes from the API so it cannot drift; the line that names loss of consciousness does not.\",\n   \"fix\": \"Add loc_history to NOT_CHECKED in conflict_candidates.py and render the line from the list.\",\n   \"acceptance_test\": \"lib08 GET case checks.not_checked contains a loss-of-consciousness entry.\"}\n ],\n \"whats_right\": [\n  \"lib09 no longer lists the English-wording checks as checked: three skipped items name Records 2, 4 and 7 (correct against the source).\",\n  \"The not-checked line naming side and loss of consciousness is visible with and without conflicts on every case I opened.\",\n  \"The empty state is never a bare 'No conflicts found.' and the checked list on screen equals the API list.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T14:28:22.132Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-142-legal-nurse-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:28:26.632Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/legal-nurse-reviewer/project_t151_t142_r2.md",
 "content": "---\nname: t151-t142-r2\ndescription: T-151 and T-142 r2 legal-nurse reviews at 25f585c (both pass); residual minors and how I ran/mutated cases\nmetadata:\n  type: project\n---\n\nT-151 + T-142 r2 at 25f585c: both pass (0 blocker, 0 major). The Spanish-coverage major from T-142 r1 is fixed (lib09 skipped box names Records 2, 4 and 7). Residual minors: lead sentence \"No conflicts found among the kinds checked\" is unchanged on partial or all-Spanish runs; note line omits record_nos; page-written \"Not checked\" line names LOC but server `not_checked` has no LOC; export internal notes still carry no coverage line (backend, no card found).\n\n**Why:** the T-141 r2 `checks.skipped[]` / `notes[]` shape is rendered by flags.js; the notes and the LOC entry stay unresolved at the server.\n\n**How to apply:** in a later round re-check (a) lead sentence when skipped is not empty, (b) internal notes coverage line, (c) NOT_CHECKED has loc_history. Method: library cases via POST /api/cases {\"library\"} + /run then `#/case/<token>` (home-page library widget selector changed); mutate `cases.config_json` run_checks in the scratchpad sqlite DB to reach NOT_RUN / STAGE_SKIPPED / all-Spanish; never name a scratch script dis.py (shadows stdlib under playwright). See [[gate-m2-0c24f5f]].\n"
}
````

### User / tool · 2026-11-02T14:28:26.724Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/legal-nurse-reviewer/project_t151_t142_r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:28:28.096Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/legal-nurse-reviewer && echo \"- [T-151/T-142 r2 pass](project_t151_t142_r2.md) — 25f585c pass; residual minors (lead sentence, notes record nos, LOC server list, export coverage line); case-mutation method\" >> MEMORY.md; tail -3 MEMORY.md; cd /Users/arsis/zlayt-pm-project && python3 tools/board.py validate 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T14:28:28.254Z

**tool result**
````
- [GATE-M2 0c24f5f changes](project_gate_m2_0c24f5f.md) — 2 majors: "No conflicts found." false assurance; unflagged quote omissions; app launch method
- [T-143 uncovered list r1-r2](project_t143_uncovered_list.md) — r2 changes: 1 major (admin patterns' open tails swallow clinical lines); probe method
- [T-151/T-142 r2 pass](project_t151_t142_r2.md) — 25f585c pass; residual minors (lead sentence, notes record nos, LOC server list, export coverage line); case-mutation method
ok (155 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:28:31.124Z

T-151 and the T-142 re-check both come out **pass**, with no blockers or majors, at 25f585c. I ran the e2e tests plus lib08, lib09, lib11 and the sample, and stopped the server by PID 21724.

The Spanish-coverage major from T-142 round 1 is fixed: lib09 now names Records 2, 4 and 7 as not read. Open minors:
- **Lead sentence:** it is the same on a full run and on a partial or all-Spanish run.
- **Notes:** the info note doesn't name its record.
- **LOC mismatch:** the page-written "not checked" line names loss of consciousness, but the server list doesn't.
- **Export notes:** they still carry no coverage line, and no backend card owns it.

Files are in /Users/arsis/zlayt-pm-project:
- reviews/T-151-legal-nurse.md
- reviews/T-142-legal-nurse-r2.md
- artifacts/review-evidence/T-151-legal-nurse/
