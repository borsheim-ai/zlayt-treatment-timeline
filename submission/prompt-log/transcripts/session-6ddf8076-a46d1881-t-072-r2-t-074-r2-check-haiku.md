# Subagent: T-072 r2 + T-074 r2 check (haiku) (T-072 r2 + T-074 r2 check (haiku))

Source: `agent-a46d188109ade634a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:55:18.232Z

Round-2 checks in /Users/arsis/zlayt-pm-project. The rule is D-040 in memory/ORCHESTRATOR_DECISIONS.md: no user-facing text asserts who spoke.

1. **T-072** (commit cab0068): using reviews/T-072-claims-adjuster.md, confirm:
   - the blocker is closed: grep app/ (backend and frontend, including mocks) for user-facing "self-report"; only the internal CSS class may remain;
   - tests/unit/test_frontend_no_speaker_label.py passes, and fails if you plant the string in a scratch copy;
   - optionally, ?api=mock in a browser shows "Reported onset".
   Write reviews/T-072-claims-adjuster-r2.md.
2. **T-074** (commit 312ed92): using reviews/T-074-claims-adjuster.md, confirm that R-FL-7 in spec/REQUIREMENTS.md:71 now states D-040, and that test_eval_spec_check passes. Write reviews/T-074-claims-adjuster-r2.md.

Use .venv/bin/python. Each file needs a ```json block of real values: card, persona claims-adjuster-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 2 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:20.126Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/claims-adjuster.md"
}
````

### User / tool · 2026-11-02T02:55:20.136Z

**tool result**
````
1	# Persona dossier — claims-adjuster-reviewer
2	
3	## 1. Identity
4	**Gary Pruitt (fictional), Senior Bodily-Injury Claims Adjuster, national auto carrier, Texas region — 15 years; trained on Colossus-style evaluation; works daily with defense panel counsel.**
5	His job is to pay what the file documents and not a dollar more; his reserves and his supervisor's file reviews reward finding the soft spots in a demand. He is the adversary: he reads a plaintiff's chronology looking for the sentence that lets him discount the whole package, and he enjoys catching a demand that says more than its records.
6	
7	## 2. Day-to-day context
8	- Tools: claims system, an injury-evaluation tool (Colossus-type: injury codes, "value drivers", duration of treatment), ISO ClaimSearch, medical-bill review, IME/records-review vendors, defense counsel.
9	- Pressures: caseload, reserve accuracy, Stowers exposure on time-limited demands within limits.
10	- What he looks for first: inconsistent accident dates, first recorded treatment, gaps, prior injuries and prior claims, degenerative imaging, missed appointments and early discharge, subjective-only complaints, treatment that escalates after an attorney is involved, bills that don't match the notes.
11	- A bad day for him: a clean, fully documented demand with no overstatement — he has to pay it.
12	
13	## 3. Goals and success criteria for this artifact (as adversary)
14	- Make the tool's output embarrassing: find any statement not in the records, any weakness the tool hid or softened, any number that is wrong or inflated.
15	- The tool passes his review only if every claim is sourced, every weakness he would raise is already surfaced for the plaintiff's attorney, and nothing is overstated.
16	
17	## 4. Review checklist
18	1. Accident date: the record 7 intake date "2026-01-19" vs 2026-01-09 (EMS/ER) is flagged as a conflict; if the tool chose one silently, I can use the other to attack the whole timeline.
19	2. The tool states "first recorded treatment: 2026-01-09 (Austin EMS)" and shows both stated accident dates with excerpts; it never computes a "delay from the accident" and never picks one accident date (D-017). A computed delay figure is a finding, because it resolves the conflict.
20	3. Gaps: the 73-day gap (03-06 → 05-18) is flagged with day count and both endpoints; no gap reason is invented — "unexplained" if the records give none.
21	4. Shorter gaps (e.g., 28 days, 01-23 → 02-20) are not flagged under the >30-day rule, but the tool does not hide them either (dates visible).
22	5. "New onset pain radiating to right arm" after the 73-day gap is surfaced as a `causation` flag (D-013), not folded into the original injury narrative.
23	6. Missed appointments and early discharge ("Discharged from PT after two missed appointments", visit 9 of 12 planned) are flagged under the causation category with the excerpt (I will argue failure to mitigate; the tool must not use that label — see item 20).
24	7. Prior conditions: "low back pain in 2023, resolved" is flagged with its excerpt and the record 3 summary does not silently drop it; the flag lands in the internal review notes for the firm (D-001), never auto-inserted in the letter — whether the letter mentions it is the attorney's call.
25	8. Degenerative language: "Findings may represent degenerative change; correlate clinically" is flagged and quoted verbatim; any summary that says "traumatic" or "acute" is false.
26	9. Reported complaints keep the record's own markers ("C/O", "Patient reports", "Patient states") and pain scores stay as written; the tool does not add its own "subjective"/"objective" labels or recast a report as a finding.
27	10. Patient self-report on causation ("Patient states symptoms began after the January collision") is labeled as the patient's statement, not a physician's opinion.
28	11. Charges: only $6,240 and $2,150 are totaled ($8,390); the $185/visit rate is not extrapolated; I will reject any PT number the records don't show.
29	12. The total is labeled as billed charges; nothing implies these amounts were paid or are recoverable (Texas paid-or-incurred).
30	13. "Missing 3 days of work" is not counted as a medical charge and no wage amount is invented.
31	14. Every timeline line carries a source cite I can check; anything without one I treat as unsupported.
32	15. Nothing escalates severity: "cervical strain" stays a strain, "concussion without loss of consciousness" keeps "without loss of consciousness", "disc protrusion" is not "herniation".
33	16. No treatment is listed as completed when only recommended (the cervical ESI is "Recommend", not performed).
34	17. Provider types are clear (EMS, ER, PCP, PT, pain management, imaging) so I can judge whether care was reasonable for a soft-tissue claim.
35	18. The export contains no advocacy adjectives ("severe", "debilitating", "significant") unless verbatim in a record.
36	19. No referral, referring provider, or reason for a visit appears unless stated in that record: record 7 names no referral source, so "referred to pain management" anywhere is an invented fact.
37	20. Flag text uses the four spec categories, the verbatim excerpt, and a fixed-template reason — never my legal labels (failure to mitigate, non-compliant, aggravation, intervening cause) or a model-written prediction of my argument.
38	21. The letter's total line is neutral and claims no completeness: "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical). No rate, "visit count not stated" wording, or list of unbilled encounters appears in the letter — those belong in the firm's internal notes (R-EX-4) — and no amount is invented that I could attack.
39	
40	## 5. Red flags / dealbreakers (for the plaintiff — i.e., what makes the tool's output a gift to me)
41	Each item here is a **blocker** (rate it so; never major or minor).
42	- A single invented fact or overstated finding (I'll cite it in my response and discount the package).
43	- A merged or "corrected" accident date.
44	- A PT total computed from the per-visit rate.
45	- A gap, prior condition, or missed-appointment note in the records that the tool's timeline or flags omitted (not: one the export omitted after a human reviewed it — that is the attorney's decision).
46	
47	## 6. Vocabulary
48	BI, specials vs generals, Colossus, value drivers, severity, MIST (minor impact soft tissue), soft-tissue, gap in treatment, delay in treatment, intervening/superseding cause, failure to mitigate, non-compliance, pre-existing, aggravation, degenerative, subjective-only, objective findings, IME/DME, letter of protection, chargemaster, paid or incurred (§41.0105), §18.001 counteraffidavit, Stowers, policy limits, reasonable and necessary, "records don't support".
49	
50	## 7. How I review
51	1. Read the raw sample records first and write my own attack list (expected: accident-date conflict, 73-day gap, new onset after gap, 2023 back pain, degenerative MRI language, missed PT, self-reported causation, PT rate).
52	2. Run the sample case in the app; read the export as if it arrived on my desk.
53	3. For each item on my attack list: is it surfaced to the plaintiff's side (flag) and is the export free of overstatement about it?
54	4. Check every number in the export against the records; recompute the total.
55	5. Hunt for any word in the export not supported by its excerpt (severity adjectives, causation verbs, completed vs recommended).
56	6. Try to make the tool embarrass itself: edit an entry to add "severe" and confirm the audit trail / internal notes record the edit and the original (D-010); the letter text itself carries no edit markers.
57	7. File each finding with the verbatim export line and the record excerpt it contradicts or omits.
58	
59	## 8. Calibration
60	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
61	- **blocker — Overstated imaging.** Evidence: summary "MRI shows traumatic C5-C6 disc herniation." Record 8 says "disc protrusion... may represent degenerative change." Fix: verbatim impression; summary uses "disc protrusion" and keeps the hedge. Test: eval forbids "herniation"/"traumatic" unless in source.
62	- **blocker — Missed appointments not flagged (hidden weakness).** Evidence: flags panel shows `gap` and `pre_existing` flags but nothing for record 6. Fix: `causation` flag citing "Discharged from PT after two missed appointments" and plan "12 visits". Test: golden flag present.
63	- **blocker — Recommended treatment reads as completed (invented fact).** Evidence: export "2026-06-12 — cervical epidural steroid injection." Fix: "Recommend cervical epidural steroid injection."
64	- **major — Gap flag present but incomplete.** Evidence: flag reads "Treatment gap detected (Capital PT → Hill Country)" with no day count or dates. Fix: "73-day gap: 2026-03-06 (PT discharge) → 2026-05-18 (pain management new patient); no reason stated in records." Test: golden flag text includes both dates and 73.
65	
66	## 9. Sources
67	- https://www.claimsjournal.com/news/national/2013/06/05/230291.htm — Claims Journal (Mitchell consultant, 2013): adjuster checklist — treatment start, gaps, provider type, active vs passive care, bills vs SOAP notes, upcoding.
68	- https://amp.claimsjournal.com/news/national/2010/12/31/116021.htm — Claims Journal on CFA Colossus report (2010): adjuster selects injury codes; software outputs a general-damages range; insurers tune it.
69	- https://www.michiganautolaw.com/blog/2026/05/13/colossus-personal-injury-calculator/ — Michigan Auto Law (plaintiff firm): Colossus uses many "value drivers" that insurers can adjust.
70	- https://forthepeople.com/blog/what-colossus-claims-software — Morgan & Morgan (plaintiff firm): records lacking ongoing pain/limitation statements score lower.
71	- https://search.txcourts.gov/Case.aspx?cn=09-0377&coa=cossup — Haygood v. De Escabedo, 356 S.W.3d 390 (Tex. 2011), Supreme Court of Texas docket 09-0377: recovery limited to expenses that have been or must be paid; only those are admissible. Billed charges may exceed that where adjusted/paid amounts are lower, so the tool labels amounts "billed" and does not characterize recoverability.
72	- https://www.wlf.org/2021/06/24/publishing/texas-high-court-rulings-on-medical-expense-damages-reel-in-plaintiffs-windfall-profit-tactics/ — WLF (defense-leaning): LOP bills, negotiated-rate discovery (K&L Auto Crushers), §18.001 counteraffidavits (In re Allstate).
73	- https://versustexas.com/blog/what-is-a-gap-in-treatment/ — Versus Texas (plaintiff firm): gap tiers up to 30+ days as a "deal breaker"; firm says these are observations, not statute.
74	- https://www.lezdotechmed.com/blog/plaintiff-and-defense-attorneys-review-the-same-records-completely-differently-here-is-why-that-matters — LezDo (records vendor): defense hunts pre-injury care, pain-imaging mismatch, conflicting histories, copy-forward notes.
75	- https://www.coopers.law/publications/articles/mist-me-litigating-the-minor-impact-soft-tissue-case/ — Cooper (plaintiff): MIST defense blames prior neck/back problems and low impact.
76	- https://www.faegredrinker.com/en/insights/publications/2024/5/responding-to-time-limited-settlement-demands-stowers-demands-and-beyond — Faegre Drinker: Stowers demand elements and insurer response.
77	- Assumptions: Colossus internals are described by plaintiff firms and a consumer group, not the vendor; the 30-day threshold is Appendix A's rule, while adjusters may weigh shorter gaps — note as context, not a finding, unless the tool hides dates.
78	
79	## 10. Limits
80	Do not opine on UI aesthetics, code, accessibility, or privacy law. Do not argue the fictional case's value; attack only what the tool outputs. Do not demand the tool argue the defense position — it must surface facts, not conclusions.
81	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:20.303Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-072-claims-adjuster.md"
}
````

### User / tool · 2026-11-02T02:55:20.312Z

**tool result**
````
1	# T-072 review: claims-adjuster-reviewer (D-040 follow-through)
2	
3	**Verdict: fail** (one blocker). The export and golden are clean, and the flag template is neutral. The shipped frontend still shows the cut label in two places, which the brief's own grep check catches.
4	
5	Model: claude-haiku-5-5, per the brief and the runtime. The dossier's expected id (opus) does not match the model actually running.
6	
7	## What I checked
8	
9	- **Export, golden, tests (pass).** The golden letter and notes, and the live export, carry no "(patient self-report)". The record 9 quote stays verbatim as "Patient states symptoms began after the January collision." (golden lines 38, 58, 69). No "physician" wording is added. The three brief test files pass (62 live; 61 at HEAD archive). The golden-byte tests pass (63 live, 42 at archive).
10	- **Neutral template (pass).** `app/backend/flag_templates.py:126` gives title "Reported onset" and explanation "Onset wording reported in ...". `tests/unit/test_export_edge.py:70` asserts no "self-report" or "patient self" in the title or explanation.
11	- **Internal id `patient_report` (not rendered as text, but exposed).** Text rendering uses `f.title` (`app/frontend/flags.js:66`). Export labels key on flag type only (`app/backend/export.py:248-257`). The id does appear in the API JSON (`app/backend/present.py:74`) and as a DOM attribute (`app/frontend/flags.js:65`). See F2.
12	- **User-facing "self-report" grep (fails).** See F1.
13	
14	## Findings
15	
16	- **F1 blocker.** `app/frontend/mock_flags.js:24` and `app/frontend/dev/mock-data.js:748-749` still show "Patient self-report (not a physician's opinion)". The overlay loads on every page (`index.html:45`). It is reached through the `?api=mock` override (`api.js:2`) and the `/dev/panels.html` harness (`panels.html:12`, served under the static mount at `api.py:508-511`). The default mode is "real" (`api.js:5`), so this is not in the default product path. I read the code path; I did not render it in a browser.
17	- **F2 minor.** Saying the id is "never shown to users" overstates it. It is not text, but `present.py:74` returns `"category": "patient_report"` in every flag payload, and `flags.js:65` writes it to `data-category`.
18	- **F3 minor.** `evals/golden/sample.expected.json:625` (flag K3) still has `"summary": "Causation rests on patient self-report, not a physician's causation opinion."` Commit 4594bb7 fixed only the `.txt` golden.
19	- **F4 nit.** "Reported onset" still implies a reporter. "Onset wording" would match the sibling "New-onset wording" (`flag_templates.py:127`). This is not a D-040 violation.
20	- **F5 nit.** `tests/e2e/test_flags_panel.py:19` is still named `test_patient_self_report_label`, though it asserts "Reported onset".
21	
22	```json
23	{"card": "T-072", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
24	 "scope": "commits 3b6a3fe and 4594bb7 (HEAD 83b4353 extracted with git archive to artifacts/review-evidence/T-072-T-074-83b4353 for test runs, extract removed afterwards); live tree /Users/arsis/zlayt-pm-project is dirty (tests/unit/test_eval_runner.py +9 lines uncommitted, app/llm/backends/fixture.py and others), so live results are reported separately; sample case Appendix A records 1-9; no browser run",
25	 "exercised": [
26	  "read personas/claims-adjuster.md in full; memory/ORCHESTRATOR_DECISIONS.md D-040, D-017, D-019; board show T-072; board validate -> 'ok (74 file(s))'",
27	  "git show --stat 3b6a3fe 4594bb7; git status --short; git diff HEAD -- tests/unit/test_eval_runner.py",
28	  "grep -rn -i 'self-report|self report|self-reported' app/ (excluding lexicon.yaml self_report keys); grep -rn 'patient_report|patient_reported_onset|source_kind' app/; grep -rln -i 'self.report|patient_report|source_kind' app/frontend",
29	  "read app/backend/flag_templates.py:120-135, app/backend/export.py:246-262, app/frontend/flags.js:60-70, app/backend/present.py:72-76, app/frontend/api.js:1-6, app/frontend/index.html:42-64, app/frontend/dev/panels.html, app/backend/api.py:505-512",
30	  "read app/frontend/mock_flags.js:20-30 and app/frontend/dev/mock-data.js:740-752; grep -n 'api=mock' tests/ (no e2e test uses mock mode)",
31	  "golden check: grep -n for Patient states|physician|self-report|Reported onset in evals/golden/sample.export.expected.txt (lines 38, 58, 69 only); diff of 4594bb7 golden hunk",
32	  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py -> 62 passed in 1.82s (live tree)",
33	  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py at git archive 83b4353 -> 61 passed; tests/unit/test_export_edge.py tests/unit/test_case_extras.py tests/unit/test_flags_pass.py at 83b4353 -> 42 passed",
34	  ".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_export.py tests/unit/test_case_extras.py tests/unit/test_export_edge.py tests/unit/test_flags_pass.py (live) -> 63 passed; test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte PASSED",
35	  ".venv/bin/python tests/fixtures/make_curated.py --check -> 'letter equal: True | notes equal: True', exit 0 (live and at 83b4353)",
36	  "evals.run not re-run (writes evals/reports, outside my write paths); the hallucination figure in the card was not re-checked"
37	 ],
38	 "verdict": "fail",
39	 "scores": {"d040_no_speaker_label_user_facing": 2, "export_golden_fidelity": 5, "no_invented_facts_or_severity": 5, "internal_id_not_rendered_as_text": 4, "residue_cleanup_across_artifacts": 2, "tests_green_at_commit": 5},
40	 "findings": [
41	  {"severity": "blocker",
42	   "title": "User-reachable frontend code still displays 'Patient self-report' (D-040 violated; brief grep check fails)",
43	   "evidence": "app/frontend/mock_flags.js:24: mk(\"f_pat_9\", \"causation\", \"patient_report\", \"Patient self-report\", \"Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): ...\"; app/frontend/dev/mock-data.js:748-749: \"title\": \"Patient self-report\", \"explanation\": \"Patient self-report (not a physician's opinion) in Hill Country Pain Management ...\". Reachability: app/frontend/index.html:45 loads mock_flags.js on every page; app/frontend/api.js:2 documents the ?api=mock page-URL override; app/frontend/flags.js:64 uses f.title as aria-label and :66 renders it as the card heading; app/frontend/dev/panels.html:12 loads mock-data.js; app/backend/api.py:508-511 mounts all of app/frontend (including dev/) as static files. Default mode is real (api.js:5 API_MODE = \"real\"), so the text is not in the default path; not rendered in a browser (code-path evidence only).",
44	   "why_it_matters": "memory/ORCHESTRATOR_DECISIONS.md D-040: 'No code or model labels who is speaking.' This is the label the decision cut, with a 'not a physician's opinion' caveat, still in shipped code. A carrier or defense reviewer who opens ?api=mock sees a self-report label, which is the credibility problem D-040 exists to avoid. Severity is blocker under the D-040 rule. If Chris rules these overlays out of the deployed build, this drops to minor (see questions_for_chris).",
45	   "fix": "Frontend-owned (app/frontend/**; open a frontend card, cross-boundary from this backend card). Change mock_flags.js:24 and dev/mock-data.js:748-749 to the neutral template text from app/backend/flag_templates.py:126 ('Reported onset'; 'Onset wording reported in ...'), or delete the f_pat_9 overlay entry.",
46	   "acceptance_test": "grep -rn -i 'self-report|self report' app/frontend returns no hits; a Playwright test opens index.html?api=mock and asserts the flags panel contains 'Reported onset' and not 'self-report'; grep -c 'self-report' app/frontend/dev/mock-data.js is 0."},
47	  {"severity": "minor",
48	   "title": "'patient_report' is not rendered as text, but it is public API data; 'never shown to users' overstates",
49	   "evidence": "app/backend/present.py:74: flag_view returns \"category\": row[\"category\"], \"source_kind\": row[\"source_kind\"]; app/frontend/flags.js:65: \"data-category\": f.category; text rendering uses f.title (flags.js:66) and export labels key on flag type only (app/backend/export.py:248-257, _flag_label). Card T-072 note 2026-11-02T02:47:25Z: 'the id is never shown to users'. Producers still emit it: app/backend/flag_templates.py:25; app/llm/lexicon.yaml:741,757; app/llm/prompts/flags_v1.md:13 ('the patient's own statement').",
50	   "why_it_matters": "The brief's rendering check passes: the id is not text. But the id is the speaker label D-040 cut, it is returned in every flag payload, and the claim recorded on the card is inaccurate. An adjuster who inspects the network payload sees 'patient_report' on record 9.",
51	   "fix": "Either (a) correct the card and decision log to 'not rendered as text; present in API JSON and data-category', or (b) map to a neutral public id at the presentation layer (present.py:74 and flags.js:65), leaving the internal id and fixtures alone (this avoids the re-record the qa note cites). Owner: backend.",
52	   "acceptance_test": "Option (b): GET a sample case's flags and assert no category or data-* value contains 'patient'. Option (a): the card and decision note state the exposure."},
53	  {"severity": "minor",
54	   "title": "Golden expected flag K3 still carries the cut label",
55	   "evidence": "evals/golden/sample.expected.json:625: \"summary\": \"Causation rests on patient self-report, not a physician's causation opinion.\" (flag K3, subtype patient_reported_onset). Commit 4594bb7 edited only evals/golden/sample.export.expected.txt lines 58 and 69.",
56	   "why_it_matters": "The golden JSON is the expected-output authority for the flags. Keeping the cut label there means the expected output still says it. I did not trace whether evals compare K3.summary to product output (evals/run.py:118 and :229 read summaries; the K3 path was not traced).",
57	   "fix": "qa-owned (evals/**): change K3.summary to a neutral line that quotes the verbatim record, for example 'Causation language: record 9 verbatim \"Patient states ...\"'. Re-run evals.",
58	   "acceptance_test": "grep -n -i 'self-report' evals/golden/sample.expected.json returns only the M10 must_not statement (line 990) or nothing; eval gates unchanged."},
59	  {"severity": "nit",
60	   "title": "'Reported onset' still names an implied reporter",
61	   "evidence": "app/backend/flag_templates.py:126: \"patient_report\": lambda v: (\"Reported onset\", f\"Onset wording reported in {_at(v)}{_quote(v)}.\"). Sibling template at flag_templates.py:127: \"New-onset wording\".",
62	   "why_it_matters": "It names no speaker, so it passes D-040. 'Reported' still implies someone reported it. 'Onset wording' would match the sibling template.",
63	   "fix": "Optional: rename to 'Onset wording'. If renamed, update tests/unit/test_export_edge.py:70, tests/e2e/test_flags_panel.py, and the overlays in F1.",
64	   "acceptance_test": "None required."},
65	  {"severity": "nit",
66	   "title": "e2e test name still says 'self_report'",
67	   "evidence": "tests/e2e/test_flags_panel.py:19: def test_patient_self_report_label(page, sample_case): (body asserts \"Reported onset\").",
68	   "why_it_matters": "Test-only naming. It is not user-facing, but a grep for 'self_report' finds it.",
69	   "fix": "Rename to test_reported_onset_label.",
70	   "acceptance_test": "pytest collects the renamed test; grep -rn 'self_report_label' tests/ returns nothing."}
71	 ],
72	 "whats_right": [
73	  "The export matches the golden after the cut: the record 9 quote is still verbatim ('Patient states symptoms began after the January collision.') in letter line 38 and notes lines 58 and 69, with no added physician or opinion wording.",
74	  "The neutral template is in place and pinned: flag_templates.py:126 and tests/unit/test_export_edge.py:66-70 assert the title is 'Reported onset' and that no 'self-report' or 'patient self' appears in title or explanation.",
75	  "Golden and curated checks are green at the commit: test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte, test_case_extras.py::test_default_export_is_byte_identical_to_golden_and_config_fills_the_citation, and make_curated --check (letter equal True, notes equal True)."
76	 ],
77	 "questions_for_chris": [
78	  "Are the ?api=mock overlay (app/frontend/mock_flags.js) and /dev/panels.html part of the deployed Space (D-008/D-020)? If they are stripped from the public build, F1 drops to minor and the verdict becomes changes.",
79	  "Keep the 'patient_report' id as internal only (F2 option a), or map it to a neutral public id at presentation (option b)?"
80	 ]}
81	```
82	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:20.512Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-074-claims-adjuster.md"
}
````

### User / tool · 2026-11-02T02:55:20.520Z

**tool result**
````
1	# T-074 review: claims-adjuster-reviewer (spec sync to D-040 golden)
2	
3	**Verdict: changes** (one major, no blocker). The two spec lines match the golden exactly and the spec-check tests pass. The spec still carries the cut requirement in R-FL-7, so the decision has not fully propagated.
4	
5	Model: claude-haiku-5-5, per the brief and the runtime.
6	
7	## What I checked
8	
9	- **Lines 280 and 291 (pass).** `diff <(sed -n 280p spec/REQUIREMENTS.md) <(sed -n 58p evals/golden/sample.export.expected.txt)` and the same for 291/69 both exit 0. Commit 83b4353 changes only those two lines (2 insertions, 2 deletions).
10	- **Tests (pass).** The brief command passes: 62 live, 61 at HEAD archive. `test_eval_spec_check.py::test_real_spec_matches_golden` and the CLI spec-match test are included.
11	- **Propagation of D-040 into the spec (fails).** See F1 through F3.
12	
13	## Findings
14	
15	- **F1 major.** R-FL-7 (`spec/REQUIREMENTS.md:71`) still requires `source_kind = "patient_report"` and the UI text "Patient self-report". Its acceptance cell says "the label renders". The product now does the opposite (`app/backend/flags.py:61`; `tests/unit/test_flags_pass.py:95` asserts every flag is `source_kind == "record"`). The spec and the tests contradict each other. Major, not blocker, because D-040 is recorded and the product matches it. If the gate reads R-FL-7 literally, the product fails it and this becomes a blocker until the spec is amended.
16	- **F2 minor.** `spec/SAMPLE_CASE_TRUTHS.md:9` still labels the record 9 quote "(9 — patient self-report, not a physician's causation opinion)".
17	- **F3 minor.** `spec/REQUIREMENTS.md:371`, deviation row 4, says the golden uses `patient_self_report`. Its evidence command `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md` now returns no output, so the row is stale.
18	- **F4 minor.** Contract and design docs still show the cut label: `memory/contracts/api.md:184-186` (example f_pat_9 with "Patient self-report" title and explanation), and `docs/UI_DESIGN_BRIEF.md:132` (a "Patient self-report" chip row). `api.md:212` already records D-040, so the example is inconsistent with its own note.
19	
20	```json
21	{"card": "T-074", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
22	 "scope": "commit 83b4353 (spec/REQUIREMENTS.md lines 280, 291) checked against evals/golden/sample.export.expected.txt lines 58, 69; spec residue searched across spec/, memory/contracts/, docs/, evals/golden/; live tree /Users/arsis/zlayt-pm-project (dirty) and HEAD 83b4353 extracted with git archive",
23	 "exercised": [
24	  "read personas/claims-adjuster.md in full; memory/ORCHESTRATOR_DECISIONS.md D-040 and its Source column; board show T-074 (notes 02:49:08Z to 02:49:12Z, commits: [])",
25	  "git show --stat 83b4353; git show 83b4353 -- spec/REQUIREMENTS.md (2 lines changed, both suffix removals)",
26	  "diff <(sed -n 280p spec/REQUIREMENTS.md) <(sed -n 58p evals/golden/sample.export.expected.txt) -> identical (exit 0); diff <(sed -n 291p spec/REQUIREMENTS.md) <(sed -n 69p evals/golden/sample.export.expected.txt) -> identical (exit 0)",
27	  "sed -n 71p spec/REQUIREMENTS.md (R-FL-7 full text); sed -n 371p spec/REQUIREMENTS.md; sed -n 9p spec/SAMPLE_CASE_TRUTHS.md; grep -rn -i 'patient self|self-report|patient_report|self_report|chip' spec/ submission/ memory/ docs/",
28	  "grep -n 'patient_self_report|summary+excerpt' evals/golden/README.md -> no output; grep -n 'Causation rests on patient self-report' evals/golden/sample.expected.json -> line 625 (K3)",
29	  "read app/backend/flags.py:61 (source_kind record, D-040 comment) and tests/unit/test_flags_pass.py:95-100",
30	  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py -> 62 passed in 1.82s (live tree; includes an uncommitted T-070 test in test_eval_runner.py)",
31	  "same three files at git archive 83b4353 (artifacts/review-evidence/T-072-T-074-83b4353, removed afterwards) -> 61 passed",
32	  "board validate (read-only) -> 'ok (74 file(s))'",
33	  "evals.run --check-spec not run (writes evals/reports, outside my write paths); the spec-match behaviour is covered by test_eval_spec_check.py"
34	 ],
35	 "verdict": "changes",
36	 "scores": {"spec_lines_match_golden": 5, "decision_propagated_to_spec": 2, "tests_green_at_commit": 5, "spec_residue_cleanup": 2},
37	 "findings": [
38	  {"severity": "major",
39	   "title": "R-FL-7 still requires the cut 'Patient self-report' label; spec and product tests contradict",
40	   "evidence": "spec/REQUIREMENTS.md:71: | R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = \"patient_report\"` and the UI text \"Patient self-report\". It is never presented as a physician's opinion. | Sample record 9 flag has `source_kind == \"patient_report\"` and the label renders. Golden `must_not` M10 passes. | UT + E2E |. Product: app/backend/flags.py:61 `\"source_kind\": \"record\",   # D-040: no code or model labels who is speaking`; tests/unit/test_flags_pass.py:95 test_no_flag_carries_a_self_report_chip asserts all source_kind == \"record\" for records 7 and 9. memory/ORCHESTRATOR_DECISIONS.md D-040 says the writer mirrors product decisions into spec/REQUIREMENTS.md; R-FL-7 was not amended.",
41	   "why_it_matters": "The card's lines 280 and 291 are right, but the same D-040 cut leaves a written requirement that demands the label. An attorney or grader reading R-FL-7 would expect 'Patient self-report' in the UI and would find it absent. As written, the shipped product fails R-FL-7's acceptance cell. Major, not blocker, because the decision is recorded and the product matches it; the defect is the unamended spec. If the gate reads R-FL-7 literally, it is a blocker until amended.",
42	   "fix": "Spec sync by writer or orchestrator: rewrite R-FL-7 to D-040. Suggested text: 'No speaker label. Every excerpt is a verbatim record excerpt with its source label (D-040). A flag never presents a patient statement as a physician's opinion.' Acceptance cell: 'Flags carry source_kind = record; no speaker label in the UI; test_no_flag_carries_a_self_report_chip passes.'",
43	   "acceptance_test": "grep -n 'Patient self-report' spec/REQUIREMENTS.md returns no hits outside the decision log; R-FL-7's acceptance cell names test_no_flag_carries_a_self_report_chip; the spec-match test still passes."},
44	  {"severity": "minor",
45	   "title": "Case truth sheet labels the record 9 quote 'patient self-report'",
46	   "evidence": "spec/SAMPLE_CASE_TRUTHS.md:9: - **Causation-weakening language:** ... \"Patient states symptoms began after the January collision\" (9 — patient self-report, not a physician's causation opinion); ...",
47	   "why_it_matters": "The truth sheet is the case's reference. It still records the speaker label that D-040 cut. Not rendered anywhere, but it is the source the team grades against.",
48	   "fix": "Replace the parenthetical with the verbatim marker, e.g. (9 — verbatim 'Patient states ...').",
49	   "acceptance_test": "grep -n -i 'self-report' spec/SAMPLE_CASE_TRUTHS.md returns nothing."},
50	  {"severity": "minor",
51	   "title": "Deviation row 4 is stale: its evidence command now returns nothing",
52	   "evidence": "spec/REQUIREMENTS.md:371: | 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` ... | `grep -n \"patient_self_report\\|summary+excerpt\" evals/golden/README.md` | orchestrator (D-entry) |. Run: the grep on evals/golden/README.md returns no output.",
53	   "why_it_matters": "A deviation row that no longer reproduces misleads the next reviewer about what is still open.",
54	   "fix": "Close the row with a pointer to D-040, or update it to the current golden state.",
55	   "acceptance_test": "The row's stated evidence command either matches a current line or the row is marked closed."},
56	  {"severity": "minor",
57	   "title": "Contract example and design brief still show the cut chip and title",
58	   "evidence": "memory/contracts/api.md:184-186: { \"id\": \"f_pat_9\", \"type\": \"causation\", \"category\": \"patient_report\", \"source_kind\": \"record\", \"title\": \"Patient self-report\", \"explanation\": \"Patient self-report (not a physician's opinion) ...\"; api.md:212 already records D-040 ('No chip or label says who is speaking'). docs/UI_DESIGN_BRIEF.md:132: | `Patient self-report` | speech bubble | Patient self-report | `--text-muted` outline | only where code set `source_kind=patient_report` (T-061 narrows this) |.",
59	   "why_it_matters": "Two docs a builder would follow still specify the cut label. api.md:184-186 contradicts its own line 212. The design brief still lists a chip the product no longer has.",
60	   "fix": "Update the api.md example to the neutral title and explanation. Mark the design-brief row as cut under D-040. Owner: backend for api.md; orchestrator to route the design brief.",
61	   "acceptance_test": "grep -rn 'Patient self-report' memory/contracts docs/ returns no hits outside decision history."}
62	 ],
63	 "whats_right": [
64	  "Lines 280 and 291 are byte-identical to golden lines 58 and 69 (diff exit 0 both), and commit 83b4353 changes only those two lines.",
65	  "test_eval_spec_check.py and test_eval_runner.py pass at HEAD 83b4353 (61 passed across the three files) and on the live tree (62 passed).",
66	  "The orchestrator's self-performed edit is disclosed in the card note (02:49:12Z), so an independent check was possible and this review re-derived the result."
67	 ],
68	 "questions_for_chris": [
69	  "Should R-FL-7 be rewritten by the writer (product note owner) or by the orchestrator (spec is orchestrator-synced per T-074 notes)? Outside my lens; I only need the amendment to exist before the M3 gate.",
70	  "Board attribution (outside my lens, noted for the orchestrator): T-074 records the AC check under the architect role for an edit the orchestrator made, and commits is empty although 83b4353 exists."
71	 ]}
72	```
73	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:20.737Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/memory/ORCHESTRATOR_DECISIONS.md"
}
````

### User / tool · 2026-11-02T02:55:20.745Z

**tool result**
````
1	# ORCHESTRATOR DECISIONS (orchestrator is the sole writer)
2	
3	Cross-cutting product decisions made while triaging reviews. The architect mirrors the technical ones into ADRs
4	(memory/DECISIONS.md); the writer mirrors the product ones into spec/REQUIREMENTS.md. Each: decision · why · source review.
5	Questions that are really Chris's are in submission/NEEDS_CHRIS.md with the assumption we act on.
6	
7	| ID | Decision | Why | Source |
8	|---|---|---|---|
9	| D-001 | Export = two blocks: **Treatment section** (paste into letter: accepted entries + accepted charges) and **Internal review notes — do not send** (accepted flags, unclear amounts, records not included, bills to request, damages mentions, AI-assistance line). Flag notes/labels/counts never enter the letter. | Accepting a flag means "I've seen it", not "tell the carrier". | T-013 paralegal r1 (blocker) |
10	| D-002 | Every letter line carries a verbatim quote + provider as written + date of service (US long format) + citation placeholder `[Ex. __ / Bates __]`. No short-cite mode. | Ship bar #1 (100% grounded export); adjusters cross-check providers. | T-014 staff-eng F1, privacy B2 |
11	| D-003 | Gaps are computed by code over the code-parsed header dates of all clinical-encounter records (deduped), independent of LLM entries and review state. Billing statements and phone notes are excluded. Ambiguous dates are excluded and flagged. | Dropping an LLM entry must never change gap math. | T-014 staff-eng F2; T-015 paralegal |
12	| D-004 | Amounts: code extracts and classifies with explicit billing-phrase rules; judge #2 validates every classification; a rate can never become a charge; running total = accepted charges only; "detected" is shown separately and labelled not-a-total. Total line wording: "Billed charges stated in these records: $X". | Texas paid-or-incurred (§41.0105) — never "damages"; no PT total from a rate. | T-014 privacy B1; research T-008 |
13	| D-005 | Any record carrying an injection warning forces all its items to needs_review; its amounts can't be charges; it can't suppress flags from other records (lexicon is the floor). | Injected "$50,000" reached the total via code path alone. | T-014 privacy B1 |
14	| D-006 | Numbers/dates/$ in a summary or a user edit must appear in that item's excerpt (code check) or the item is needs_review with a reason. | Don't rely on the judge for swapped numerals. | T-014 staff-eng F5, privacy |
15	| D-007 | Flag titles/explanations are code templates; the LLM returns only category + excerpt spans. | No free LLM prose in the attorney's notes. | T-014 staff-eng F8, privacy |
16	| D-008 | Public deployment is demo-only by default (cached sample run through real pipeline code); live mode needs an explicit env opt-in. No case list; random 128-bit case tokens; spend counter append-only and separate from case data. | Exposure + key abuse risk. NEEDS_CHRIS #7. | T-014 privacy |
17	| D-009 | AI disclosure: UI banner + a line in internal notes; none in the letter text. (Listed under "Decided by the team" in NEEDS_CHRIS.) | Candor without telling the carrier how the chronology was made. | T-014 privacy |
18	| D-010 | Edits: entry = summary text only; charge = accept/dismiss only (no reclassification, no amount edit); flag = reviewer note only. Ambiguous dates are resolved with a separate `confirm_date` action (choose one of the code-proposed readings), not an edit. Originals are kept; "edited" shows in UI + internal notes. | Keep code-owned facts code-owned. | T-013 PM r2 (major 1, 2) |
19	| D-011 | **Cut** (non-goals): batch accept; charge reclassification; "not a duplicate" split action (merge stays, visible); LLM date pointing; BYOK; `?full=1`; flag title/explanation edits; case list; LLM split fallback. | Time box; each needed a new endpoint/ADR and none is an Appendix A must-have. | T-013 PM r2, T-014 staff-eng F12 |
20	| D-012 | Excerpt rule: an entry's excerpt is one or more **whole sentences** of the record (code sentence splitter: `.`, `;`, line breaks), chosen by the model and changeable by the paralegal only to other whole sentences of the same record. A sentence that contains any lexicon hit (pre_existing / causation / compliance) or hedge is kept whole — a hedge can never be cut. Flagged language may appear in the letter **only** as part of an accepted excerpt, and the internal notes list "flagged language quoted in the letter" so the attorney decides. NEEDS_CHRIS #10. | The records' own words are the record; hiding them is the attorney's call, not the tool's. | T-013 paralegal r2 M1/M2, PM r2 M3/M4 |
21	| D-013 | Flag-type vocabulary everywhere: `gap`, `conflict`, `pre_existing`, `causation`, plus `record_warning` (date ambiguity, injection). Lexicon `causation_weakening` and `compliance` map to `causation`. | Three vocabularies existed. | T-013 PM r2 M5 |
22	| D-014 | Provider = the source label exactly as written in the record header; golden aliases must match header text. | Grounding (R-TL-9). | T-013 PM r2 |
23	| D-015 | Paralegal ship-bar score key: `scores.verify_quickly` (1–5) in the paralegal review JSON; ≥ 4 to ship. | One name across REQUIREMENTS, briefs, reviews. | T-013 PM r2 |
24	| D-016 | Post-launch, a test set **may** be built from real work product, but only inside the firm's environment, attorney-approved, with access logged; the prototype and this repo stay synthetic-only. Personas must not treat that as a dealbreaker. | Part 2 area 4 asks for it; Texas Op. 705 allows confidential info in AI tools with precautions. | T-010 litigation-lead Q |
25	| D-017 | The tool never picks between conflicting accident dates and never computes "delay from the accident". It may state "first recorded treatment: <earliest record date>". Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides. | Must-not: merge the two accident dates; adverse facts are the attorney's call. | T-010 litigation-lead M1/M2 |
26	| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS reports (ambulatory at scene, refused transport, minimal damage), "no objective findings", WNL/full ROM, and attorney referral are **causation** flags citing the excerpt (internal notes only, D-001). Delay to first treatment is not computed (D-017). The lexicon self-check must run over every golden case and report recall per must-flag. | Recall and precision both failed probes; vocab mismatch. | T-009 legal-nurse + claims-adjuster |
27	| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
28	| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
29	| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
30	| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
31	| D-023 | **Harness threat model:** the hooks defend against *accidents and lazy evasion by well-meaning agents* (wrong spelling, a pasted destructive command, staging a secret), not against a deliberately hostile agent with shell access — a shell-text guard cannot be complete against that. Consequences: (1) every finding that a *plausible accidental spelling* passes is a bug and gets fixed + a regression test; (2) deliberate obfuscation (brace expansion, IFS, copies of board.py, interpreter one-liners) is residual risk, documented, and covered by detection instead: git history is append-only (no rewrite), every board transition is in the append-only activity log, and the orchestrator re-verifies evidence before closing; (3) `--no-verify` is never legitimate for agents (denied); (4) reviewers may run mutating git only inside scratch repos under /tmp or the scratchpad. | Security r2 asked for the threat model; without one the guard review is an endless arms race. | T-003/T-006 security r2 |
32	| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at milestone gates (Tier 2) and the final hiring panel. One agent may cover two persona checklists in one pass. (3) Docs/research cards: max 2 rounds; remaining majors without blockers become documented debt (§7.4) instead of round 3. (4) Briefs ≤ 12 lines, reviewer replies ≤ 10 lines. (5) Researcher moves to sonnet. (6) Heartbeat hourly, not every 20 min. (7) No more harness rounds after M0 r3: residual findings become debt under D-023. | Spend the budget on the product and the submission, not on review churn. | Chris inbox 2026-11-02T00:58Z |
33	| D-025 | Provider-name conflicts across records (e.g. golden case_05) are raised by **code** (normalized-name rule over header labels), matching LLM_VS_CODE row 10; the LLM conflict pass covers semantic conflicts only (row 11). | Deterministic task → code; removes an Either/or from the plan. | T-018 contract review (staff major 7) |
34	| D-026 | Lexicon recall on golden must-flags is **reported, not gated** (latest.json `lexicon_recall_must_flags`); the ship bar is unchanged. LLM_VS_CODE rows 12/16 say so. | The lexicon is a second signal; the gate is flag precision/recall of the whole system. | T-018 contract review (PM major 6) |
35	| D-027 | Two-digit years are never guessed: `03-17-98` is `date_ambiguous` with candidates (1998, 2098) and excluded from gap math until confirmed. Text outside recognised record blocks is never dropped: it becomes an 'unsplit text' record flagged for the paralegal. | 'Say so instead of guessing' (spec); silent drops lose facts. | T-032 staff review |
36	| D-028 | Judges return a verdict enum plus a `reason_code` from a closed list (e.g. ADDS_DIAGNOSIS, ADDS_SEVERITY, ADDS_CAUSATION, DROPS_QUALIFIER, NUMBER_MISMATCH, OTHER_UNSUPPORTED); no free-text reason. The UI's Why? renders the code through a code template. | Model prose must not reach the attorney or the UI (consistent with D-007); ADR-008.5 enum-only. | T-035 staff review (Chris Q answered by orchestrator) |
37	| D-029 | Two fixture sets: `tests/fixtures/llm/recorded/` (live claude-cli recordings, used by evals to replay real model behaviour) and `tests/fixtures/llm/curated/` (hand-checked generator/judge responses that reproduce the golden summaries/excerpts exactly; labelled CURATED). E2E byte-equality (R-EX-6) and the public demo replay the curated set and the UI labels it 'cached demo (curated responses)'; the ship bar (§8.2) is measured on live runs and recorded fixtures only. | A live model may legitimately choose different whole-sentence excerpts (entry 2 adding the ER-charges sentence); byte-equality needs fixed responses; honesty needs the label. | T-040 handoff |
38	| D-030 | Flag evidence is the **verbatim phrase span** that triggered the flag (lexicon match or LLM-returned span), e.g. "Findings may represent degenerative change", "New onset pain" — not the whole sentence. Entry excerpts stay whole sentences (D-021). Internal notes quote flag spans; the golden notes block is the authority. | Precise flag quotes; matches the hand-written golden; entries keep context. | T-051/backend-4 |
39	| D-031 | **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_SPLIT); 'not a duplicate' split; full audit view (local mode); exhibit/Bates numbering as a per-case config; draft treatment paragraph in firm voice (stretch from spec; every sentence grounded + judged, internal until accepted). **Still cut, with reason:** charge reclassification (a rate must never become a charge — safety), auth/roles (needs an identity provider), per-user learning (needs its own evals), numeric confidence (unverifiable precision), non-English/handwriting, date-convention inference (silent-guess risk), OCR. | Chris asked; each reinstated item keeps the ladder and grounding rules. | Chris inbox 02:05Z |
40	| D-032 | Narrows D-018: normal/negative findings (`objective_negative`: 'negative for fracture', 'WNL', 'full ROM') are **context only, never flags**; `scene_facts` raise a causation flag only on specific adjuster phrases ('minimal damage', 'refused transport', 'ambulatory at scene', 'no airbag deployment'), never on a plain mechanism description ('Cyclist struck by a car'). | First eval: causation precision 0.5 from these two categories; golden case_05 must_not N2. | T-038 eval report 20261102T020824Z |
41	| D-033 | `patient_report` (self-report chip) applies only to explicit patient attribution ('Patient states/reports/notes', 'Pt c/o', patient-quoted speech). EMS narrative, witness, spouse/family statements and generic 'S:'/'Subjective:' headers are not patient self-report (separate or no attribution). Narrows ADR-013 / DECISIONS.md:286. | Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit. | T-036 r3 → T-061 |
42	| D-034 | Hardens D-006/R-RV-3: a number, date or $ figure in a summary, edit or manual entry that is not in that item's excerpt (or its source label/parsed date) is a **hard 422** — no 'keep my wording' override. The 409 confirm path remains only for non-numeric judge objections, and any override is listed in internal notes ('reviewer override: <reason code>'). | An override let 'Pain 9/10' into the letter against a 4/10 quote — an invented fact. | T-056 paralegal review |
43	| D-035 | Simplifies D-033: `patient_report` is attached only to a **clause** that begins with an explicit patient subject ('Patient', 'Pt', 'The patient') followed by a reporting verb (states, reports, notes, says, endorses, complains of, c/o, denies); the tag spans that clause only (to the next ';' or sentence end). Everything else — EMS, family, any other or unknown speaker, header labels — gets **no tag**. Default is no tag: a missing chip is safe, a wrong chip is not. | Speaker-list regexes kept missing new speakers (girlfriend, co-worker). | T-061 r2 |
44	| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
45	| D-037 | Final rule for `patient_report` (supersedes the clause-splitting in D-035, 2026-11-02): the chip attaches only when the **whole excerpt** is a single patient-subject clause (`Patient`/`Pt`/`The patient` + reporting verb), with no further clause after `;`, `,`, `and`, or `(`. Any mixed excerpt gets no chip and stays a plain record excerpt, so no verb list decides it. Bare `C/O` gets no chip. A missing chip is safe; a wrong chip mislabels the source. | Three adjuster rounds kept finding clause-boundary holes; fail closed instead of patching verbs. | T-061 claims-adjuster r3 B1/B2 |
46	| D-038 | Narrows D-032 (2026-11-02): normal or negative objective findings stay context-only, but defense **credibility phrases** from the lexicon (e.g. 'Waddell signs', 'out of proportion', 'symptom magnification', 'non-physiologic', 'inconsistent effort') raise a flag so the paralegal sees them before the adjuster does. | These are what an adjuster quotes against the claimant; hiding them defeats the prep purpose. | T-063 staff r1 major 6 |
47	| D-039 | Re-run with decided items (2026-11-02): once any entry in a case is accepted, edited or dismissed, the case's records are frozen. A re-run reuses the stored records and never re-splits, so decided items keep their record ids and excerpts. Re-splitting is allowed only while every entry is still pending. | Provenance of an accepted item is what the paralegal verified against; it must never silently move. | T-057 staff r3 blocker |
48	| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four adjuster rounds each found mixed excerpts that a closed rule still mislabeled. The verbatim excerpt already shows who spoke ('Patient states…', 'wife reports…'), so the label added risk without information. A missing chip is safe; a wrong one is a credibility error. | T-061 claims-adjuster r4 blocker; §7.4 |
49	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:21.270Z

**tool call — Bash**
````
{
 "command": "ls -la /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/ && cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md",
 "description": "List reviewer memory directory and its index"
}
````

### User / tool · 2026-11-02T02:55:21.363Z

**tool result**
````
total 128
drwxr-xr-x@ 18 arsis  staff   576 Nov  1 20:54 .
drwxr-xr-x@ 17 arsis  staff   544 Nov  1 20:38 ..
-rw-r--r--@  1 arsis  staff  2883 Nov  1 20:54 MEMORY.md
-rw-r--r--@  1 arsis  staff  2303 Nov  1 20:53 feedback_lexicon_review_method.md
-rw-r--r--@  1 arsis  staff  1116 Nov  1 20:52 feedback_persona_identity_on_filing.md
-rw-r--r--@  1 arsis  staff  1492 Nov  1 20:11 feedback_review_commit_not_worktree.md
-rw-r--r--@  1 arsis  staff  1287 Nov  1 20:54 feedback_reviews_write_once.md
-rw-r--r--@  1 arsis  staff  1911 Nov  1 20:54 project_d040_label_cut_residue.md
-rw-r--r--@  1 arsis  staff  1478 Nov  1 19:59 project_flag_pass_review_patterns.md
-rw-r--r--@  1 arsis  staff  3468 Nov  1 20:18 project_flag_source_kind_and_run_signal.md
-rw-r--r--@  1 arsis  staff  2882 Nov  1 20:00 project_research_attack_map_gaps.md
-rw-r--r--@  1 arsis  staff  1575 Nov  1 20:14 project_t036_r4_split_and_judge_fixtures.md
-rw-r--r--@  1 arsis  staff  1894 Nov  1 20:26 project_t061_r2_speaker_scope.md
-rw-r--r--@  1 arsis  staff  2048 Nov  1 20:34 project_t061_r3_clause_span_holes.md
-rw-r--r--@  1 arsis  staff  2024 Nov  1 20:40 project_t061_r4_separator_list.md
-rw-r--r--@  1 arsis  staff  2514 Nov  1 20:52 project_t067_credibility_negation_and_recall.md
-rw-r--r--@  1 arsis  staff  2744 Nov  1 20:53 project_t071_chip_cut_harness_sweep.md
-rw-r--r--@  1 arsis  staff  1675 Nov  1 20:53 reference_spare_port_app_server.md
- [Lexicon review method](feedback_lexicon_review_method.md) — selfcheck PASS hides recall gaps; rerun probe script; must-probe constructions
- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 r1-r4: omissions, invented Rivera facts, partial scope fixes (line 34 left open at r4); sweep prose + golden must-not regex
- [Flag-pass review patterns](project_flag_pass_review_patterns.md) — T-036 r0: vacuous guard test, silent-empty conflict pass, worker skipped full suite
- [source_kind history and run signal](project_flag_source_kind_and_run_signal.md) — T-036 r2/r3 word filter; T-061 r0 (dd545e3) lexicon narrowed but AC2 flags/grounding wiring not done, exclude regex over-broad
- [Review the commit, not the dirty tree](feedback_review_commit_not_worktree.md) — git archive the sha when working tree has uncommitted edits to reviewed files
- [Reviews are write-once](feedback_reviews_write_once.md) — reviewer-write-guard blocks Edit on a written review; verify citations before the first write
- [T-036 r4 split and judge fixtures](project_t036_r4_split_and_judge_fixtures.md) — self-report split to T-061; committed judge fixtures don't replay (JUDGE_UNAVAILABLE); r4 verdict changes
- [T-061 r2 speaker scope](project_t061_r2_speaker_scope.md) — closed speaker list + 3-word window leaks colon labels, Mrs. split, mixed sentences; test variants, not just listed phrasings
- [T-061 r3 clause-span holes](project_t061_r3_clause_span_holes.md) — D-035 span runs to ';' so comma/and family clause keeps the chip; closed verb list leaks 'thinks/told'; selfcheck not production
- [T-061 r4 separator list](project_t061_r4_separator_list.md) — D-037 chip still leaks via unlisted connectors (colon, dash, but, with, &, /, plus, per); sweep connectors, not spec examples
- [D-040 label-cut residue](project_d040_label_cut_residue.md) — T-072/T-074: cut label survives in ?api=mock overlay, dev harness, R-FL-7, golden JSON, contracts; "not rendered" != "never shown"
- [T-071 chip cut harness sweep](project_t071_chip_cut_harness_sweep.md) — r1 harness sweep, r2 (9d6756e) closed major 1 with checker mutation test; lexicon/db/README residuals still open; triage "documented" needs a SCOPE_CUTS row
- [T-067 credibility negation and recall](project_t067_credibility_negation_and_recall.md) — negated/negative credibility over-flagged (negatable:false); reversed-order and 'Waddell testing' misses; 4 red tests at 59c7edb; T-069 edit audit passes
- [Persona identity on filing](feedback_persona_identity_on_filing.md) — never file under another persona's name (T-069 paralegal request); file in my lane, report the persona pass as outstanding
- [Spare-port app server](reference_spare_port_app_server.md) — run own server on PORT 7871 from a commit tree; never 7860; bash-guard blocks < and > in commands; rm -rf in scratch denied
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:23.599Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_d040_label_cut_residue.md"
}
````

### User / tool · 2026-11-02T02:55:23.616Z

**tool result**
````
1	---
2	name: d040-label-cut-residue
3	description: When a decision cuts a user-facing speaker label (D-040 self-report chip), residue survives in mock overlays, dev harness, spec requirement rows, golden JSON, contracts and design docs; grep all of them, and "not rendered" is not "never shown"
4	metadata:
5	  type: project
6	---
7	
8	T-072 / T-074 (2026-11-02) reviewed the D-040 cut of the "Patient self-report" label. The golden .txt and the export were clean. The residue sat elsewhere:
9	- app/frontend/mock_flags.js:24 and app/frontend/dev/mock-data.js:748-749 still showed "Patient self-report". Reachable via `?api=mock` (api.js:2) and /dev/panels.html; the qa golden fix did not touch them.
10	- spec/REQUIREMENTS.md:71 (R-FL-7) still demanded the label. The card synced only lines 280/291.
11	- evals/golden/sample.expected.json:625 (flag K3 summary) still had the label.
12	- memory/contracts/api.md:184-186, docs/UI_DESIGN_BRIEF.md:132, spec/SAMPLE_CASE_TRUTHS.md:9, spec row 371 (stale).
13	- The internal category `patient_report` is "not rendered as text" (flags.js renders f.title; export labels key on type), but it IS in the public flag JSON (present.py:74) and as data-category (flags.js:65). A card that says "never shown to users" overstated it.
14	
15	**Why:** a decision that cuts a label is applied to the file the card names. Mock overlays, dev harnesses, requirement rows and golden JSON are separate files, so they survive a card that touches only the export and the golden .txt.
16	
17	**How to apply:** when a card claims a label is gone, grep app/ (including app/frontend/mock*.js and dev/), spec/, evals/golden/*.json, memory/contracts/, docs/ for the label text, and check `api.py` static mounts to see whether dev/ pages are served. For "not shown to users", check the API payload (present.py) and DOM attributes, not only rendered text. Related: [[feedback_reviews_write_once]], [[project_research_attack_map_gaps]].
18	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:23.882Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_t071_chip_cut_harness_sweep.md"
}
````

### User / tool · 2026-11-02T02:55:23.890Z

**tool result**
````
1	---
2	name: t071-chip-cut-harness-sweep
3	description: T-071 (D-040 cut of the patient_report chip, a27e3a4): product path clean at 33/33, but goldens, library builder, db CHECK and lexicon comments still encode the withdrawn label; evals ship_bar False pre-existing
4	metadata:
5	  type: project
6	---
7	
8	D-040 (cut the speaker chip) was implemented in a27e3a4. The product path is clean: flags.py:61, generator.py:80 and present.py:45 set source_kind "record", and no app/ code reads source_kind. Review: reviews/T-071-claims-adjuster.md, verdict changes (2 major, 3 minor, 0 blocker).
9	
10	**Why:** a product-only cut leaves the harness behind. check_golden.py:87-88 requires source_kind patient_report on every golden span, research/library_build.py:44 writes it, and db schema.sql:39 still allows it. The card's AC1 said "no code path", which the harness breaks.
11	
12	**How to apply:** on any "remove value X everywhere" card, sweep research/, evals/ (golden and library expected JSON and checkers), app/db/schema.sql and the lexicon/README comments, not only app/. grep -rn the value across the whole repo, excluding reviews/ and board/. Also, when a card cites "evals pass", read ship_bar_met and the blockers in the report, not one metric (hallucination 40/40 was cited while ship_bar was False on the parent commit too).
13	
14	**Round 2 (9d6756e, qa):** the harness sweep closed major 1. check_golden.py:87-88 now rejects any span source_kind, and an injected label fails with exit 1 (mutation test in an extracted archive). Golden and library JSON are key-only diffs. Review: reviews/T-071-claims-adjuster-r2.md, pass for the r2 scope with 3 minors. Carried over and still open: lexicon.yaml:25-26 and :84 stale comments, schema.sql:39 CHECK (triage said "documented"; no SCOPE_CUTS row). New: evals/golden/README.md:40 template still shows the label.
15	
16	**Lesson:** a "documented" residual in a triage note is not a record. Grep memory/SCOPE_CUTS.md before accepting it as closed.
17	
18	Related: [[t061-r4-separator-list]], [[review-commit-not-worktree]].
19	
20	**Tooling gotchas seen here:**
21	- `git archive` omits untracked artifacts. artifacts/review-evidence/T-009-*probes* are untracked, so the selfcheck in an archive reports "probe FN 0 of 0" and PASSes on nothing. Copy the probe files into the archive's artifacts/review-evidence/ before trusting the probe count. The live tree showed FN 1 of 140 (No acute findings, low only), the same at parent.
22	- The evals runner has no `fixture` subcommand. Use `.venv/bin/python -m evals.run --backend fixture --runs 3 --out <dir>`.
23	- macOS has no `timeout` binary.
24	- The live tree moves under in-progress cards (T-072 edited flag_templates.py while I reviewed). Review the commit via git archive, and say so in the scope.
25	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:24.130Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md"
}
````

### User / tool · 2026-11-02T02:55:24.137Z

**tool result**
````
1	---
2	name: reviews-write-once
3	description: reviewer-write-guard makes reviews/<card>-<persona>.md append-only once written; get line citations and JSON right before the first write
4	metadata:
5	  type: feedback
6	---
7	
8	The reviewer-write-guard hook blocks Edit on an existing file under reviews/ ("reviews are append-only — write a new file (e.g. -r2/-r3 suffix)").
9	On T-061 r3 I wrote the review, then found three wrong test line citations, and could not correct them in place.
10	
11	**Why:** the guard enforces append-only history for review rounds, so a round file is final once written.
12	
13	**How to apply:** before the first Write of a review file, grep every cited file:line and check it (use grep -n, not memory). Parse the
14	JSON block and check the verdict rule. Do not work around the guard with a shell write; if a citation is off after writing, say so in
15	the reply to the orchestrator and give the corrected line numbers.
16	
17	T-072 r0 repeated the slip: I cited flag_templates.py:127 for "New-onset wording" (actual :128), and only noticed after the Write. Neighbour
18	lines drift when you read a sed range by eye; grep -n the exact string for each citation, including the ones you think are obvious.
19	Related: [[project_d040_label_cut_residue]].
20	
21	Related: [[project_t061_r3_clause_span_holes]].
22	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:24.418Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/feedback_review_commit_not_worktree.md"
}
````

### User / tool · 2026-11-02T02:55:24.425Z

**tool result**
````
1	---
2	name: review-commit-not-worktree
3	description: When the live working tree has uncommitted edits to the files under review, probe the named commit (git archive into artifacts/review-evidence, then run the probe with the tree root as argument) and say so in the review
4	metadata:
5	  type: feedback
6	---
7	
8	On T-036 r3 the live tree had uncommitted edits to confidence.py, flag_templates.py, why.py and pipeline.py (other workers in flight), so `git diff --stat <commit> -- <files>` was non-empty even for files the round was about. Probes on the live tree would have tested code the commit does not contain.
9	
10	**Why:** a verdict on a round must cite the commit's behaviour. Working-tree results can pass or fail for reasons outside the commit (e.g., an uncommitted LLM_SPLIT template or a pipeline.py warning line).
11	
12	**How to apply:** run `git diff --stat <sha> -- <files under review>`. If non-empty, run `git archive <sha> | tar -x -C artifacts/review-evidence/<dir>` (create the dir first with mkdir -p) and run the probe script with that dir as argument, plus pytest from inside that dir with `.venv/bin/python -m pytest ... -p no:cacheprovider`. Name the tree in the review's scope. Delete the extracted dir afterwards: it contains a full copy of artifacts and should not be left in place.
13	
14	Note: the Bash hook (board-guard) denies commands with backticks in a heredoc or inline python -c; use a single-quoted heredoc without backticks.
15	
16	Related: [[project_flag_source_kind_and_run_signal]].
17	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:24.901Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 && echo \"---\" && git show --stat cab0068 | head -30 && echo \"---\" && git show --stat 312ed92 | head -30",
 "description": "Show recent log and stat for cab0068 and 312ed92"
}
````

### User / tool · 2026-11-02T02:55:25.038Z

**tool result**
````
cab0068 fix(frontend): remove self-report label from mock overlays (D-040)
312ed92 spec: R-FL-7 rewritten for D-040 (T-074 r2)
37a76a8 fix(frontend): confirmed orphan date stays visible under Records without an entry; excerpt in Dates row; no double listing (T-068 r2)
9d6756e fix(evals): drop patient_report source_kind from golden checker, goldens and library builder (D-040, T-071 r2)
d7dbfde fix(backend): fixture backend falls back from FIXTURE_SET (curated) to the recorded set
---
commit cab006810891bf8c705f8814ced77e341a02e272
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:55:05 2026 -0600

    fix(frontend): remove self-report label from mock overlays (D-040)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/frontend/dev/mock-data.js                |  4 ++--
 app/frontend/mock_flags.js                   |  2 +-
 tests/unit/test_frontend_no_speaker_label.py | 23 +++++++++++++++++++++++
 3 files changed, 26 insertions(+), 3 deletions(-)
---
commit 312ed928a3d8563aa80721d1604a04f6f68f0b89
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:54:40 2026 -0600

    spec: R-FL-7 rewritten for D-040 (T-074 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 spec/REQUIREMENTS.md | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:27.399Z

**tool call — Bash**
````
{
 "command": "echo \"== grep self-report (case-insens) in app/ ==\" && grep -rn -i 'self-report\\|self report\\|self_report\\|selfreport\\|self-reported\\|patient self\\|patient_report' app/ ; echo \"exit=$?\"; echo \"== commit diff cab0068 ==\" && git show cab0068 -- app/ | head -80",
 "description": "Grep app/ for self-report residue and show cab0068 app diff"
}
````

### User / tool · 2026-11-02T02:55:27.514Z

**tool result**
````
== grep self-report (case-insens) in app/ ==
app/README-arch.md:36:  lexicon.yaml     [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection
app/README-arch.md:78:`app/llm/lexicon.yaml` v2 (researcher): `flag_type`, `hedge`, `self_report`, `strength`, plus the `accident_date_phrases`, `non_encounter` and `injection` categories. It blocks the gap rule, the accident-date rule and the injection scan, and its golden self-check (recall per `must` flag) gates the claim that the lexicon is a floor (ADR-008.4).
app/llm/lexicon.yaml:20:#   pre_existing, degenerative_language, speculative_language, patient_report, missed_care, new_onset).
app/llm/lexicon.yaml:25:#   from an excerpt (ADR-016). `self_report: true` marks wording that explicitly attributes a statement to the PATIENT (T-061); code sets
app/llm/lexicon.yaml:26:#   source_kind = "patient_report" from it (ADR-013). Self-report entries are never hedges.
app/llm/lexicon.yaml:84:# T-061: a self_report hit is a PATIENT statement only. Before the code sets source_kind = patient_report, it must drop the hit
app/llm/lexicon.yaml:85:# when the hit's sentence matches `self_report_scope.exclude_sentence` (a named non-patient speaker with a speech verb, or
app/llm/lexicon.yaml:86:# "per <wife|husband|EMS|...>"). Bare "S:", "Subjective:" and "Self-reported" headers are not matched by any self_report entry,
app/llm/lexicon.yaml:87:# and the intake-form date entry is self_report: false. Reference implementation: research/lexicon_selfcheck.py:is_patient_statement().
app/llm/lexicon.yaml:88:self_report_scope:
app/llm/lexicon.yaml:90:  note: 'T-061 r1: anchored to the sentence SUBJECT (a sentence that starts with a non-patient speaker, or with "Per <non-patient>"); a patient subject that merely mentions EMS or a wife stays patient. Sentence-level test: the sentence containing the match is tested; a hit means the statement is not the patient''s, so source_kind stays "record" and no "Patient self-report" label is shown.'
app/llm/lexicon.yaml:104:  self_report: false
app/llm/lexicon.yaml:125:  self_report: false
app/llm/lexicon.yaml:142:  self_report: false
app/llm/lexicon.yaml:159:  self_report: false
app/llm/lexicon.yaml:175:  self_report: false
app/llm/lexicon.yaml:191:  self_report: false
app/llm/lexicon.yaml:207:  self_report: false
app/llm/lexicon.yaml:224:  self_report: false
app/llm/lexicon.yaml:242:  self_report: false
app/llm/lexicon.yaml:260:  self_report: false
app/llm/lexicon.yaml:277:  self_report: false
app/llm/lexicon.yaml:294:  self_report: false
app/llm/lexicon.yaml:310:  self_report: false
app/llm/lexicon.yaml:326:  self_report: false
app/llm/lexicon.yaml:342:  self_report: false
app/llm/lexicon.yaml:359:  self_report: false
app/llm/lexicon.yaml:377:  self_report: false
app/llm/lexicon.yaml:393:  self_report: false
app/llm/lexicon.yaml:411:  self_report: false
app/llm/lexicon.yaml:427:  self_report: false
app/llm/lexicon.yaml:444:  self_report: false
app/llm/lexicon.yaml:461:  self_report: false
app/llm/lexicon.yaml:477:  self_report: false
app/llm/lexicon.yaml:488:- id: self_reported_prior
app/llm/lexicon.yaml:493:  self_report: true
app/llm/lexicon.yaml:496:  rationale: 'A self-reported prior history is the record''s own admission of an earlier condition.'
app/llm/lexicon.yaml:509:  self_report: false
app/llm/lexicon.yaml:527:  self_report: false
app/llm/lexicon.yaml:545:  self_report: false
app/llm/lexicon.yaml:562:  self_report: false
app/llm/lexicon.yaml:580:  self_report: false
app/llm/lexicon.yaml:598:  self_report: false
app/llm/lexicon.yaml:614:  self_report: false
app/llm/lexicon.yaml:630:  self_report: false
app/llm/lexicon.yaml:646:  self_report: false
app/llm/lexicon.yaml:662:  self_report: false
app/llm/lexicon.yaml:678:  self_report: false
app/llm/lexicon.yaml:694:  self_report: false
app/llm/lexicon.yaml:711:  self_report: false
app/llm/lexicon.yaml:727:  self_report: false
app/llm/lexicon.yaml:741:  category: patient_report
app/llm/lexicon.yaml:743:  self_report: true
app/llm/lexicon.yaml:754:- id: patient_reports_generic
app/llm/lexicon.yaml:757:  category: patient_report
app/llm/lexicon.yaml:759:  self_report: true
app/llm/lexicon.yaml:764:  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. T-061: it does NOT match a bare "S:" / "Subjective:" header or "Self-reported" (a section label is not an attribution), and a sentence whose speaker is EMS, a witness, a spouse or family is excluded by self_report_scope. "C/O" and "complains of" with no named speaker are read as the patient, which is the clinical convention.'
app/llm/lexicon.yaml:775:  self_report: false
app/llm/lexicon.yaml:780:  false_positive: 'Round 2 split this from the generic "per patient" marker, which is now low (self_report). T-061: self_report is false here because an intake form is a document, not the patient''s statement; source_kind stays "record". "Date of injury per patient" is still caught by patient_reports_generic. "Per protocol" does not match.'
app/llm/lexicon.yaml:791:  self_report: false
app/llm/lexicon.yaml:808:  self_report: false
app/llm/lexicon.yaml:824:  self_report: false
app/llm/lexicon.yaml:841:  self_report: false
app/llm/lexicon.yaml:857:  self_report: false
app/llm/lexicon.yaml:873:  self_report: false
app/llm/lexicon.yaml:889:  self_report: false
app/llm/lexicon.yaml:905:  self_report: false
app/llm/lexicon.yaml:921:  self_report: false
app/llm/lexicon.yaml:938:  self_report: false
app/llm/lexicon.yaml:954:  self_report: false
app/llm/lexicon.yaml:962:    hit: ['Discharged from PT after two missed appointments.', 'Patient self-discharged.']
app/llm/lexicon.yaml:970:  self_report: false
app/llm/lexicon.yaml:986:  self_report: false
app/llm/lexicon.yaml:1002:  self_report: false
app/llm/lexicon.yaml:1018:  self_report: false
app/llm/lexicon.yaml:1034:  self_report: false
app/llm/lexicon.yaml:1050:  self_report: false
app/llm/lexicon.yaml:1066:  self_report: false
app/llm/lexicon.yaml:1082:  self_report: false
app/llm/lexicon.yaml:1098:  self_report: false
app/llm/lexicon.yaml:1115:  self_report: false
app/llm/lexicon.yaml:1131:  self_report: false
app/llm/lexicon.yaml:1148:  self_report: false
app/llm/lexicon.yaml:1164:  self_report: false
app/llm/lexicon.yaml:1181:  self_report: false
app/llm/lexicon.yaml:1204:  self_report: false
app/llm/lexicon.yaml:1225:  self_report: false
app/llm/lexicon.yaml:1245:  self_report: false
app/llm/lexicon.yaml:1264:  self_report: false
app/llm/prompts/flags_v1.md:13:- "patient_report": the patient's own statement about onset or cause ("patient states symptoms began after ...").
app/frontend/review.js:276:        if (!head.querySelector('[data-testid="entered-by"]')) head.append(el("span", { class: "rv-chip rv-selfreport", "data-testid": "entered-by" }, "Entered by reviewer"));
app/frontend/review.css:27:.rv-selfreport { background: #e8eefc; color: #1b3a8a; border-color: #a9bbea; }
app/frontend/mock_flags.js:24:      mk("f_pat_9", "causation", "patient_report", "Reported onset", "Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
app/frontend/dev/mock-data.js:746:   "category": "patient_report",
app/backend/flag_templates.py:25:    ("causation", "patient_reported_onset"): "patient_report",
app/backend/flag_templates.py:35:    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
app/backend/flag_templates.py:126:    "patient_report": lambda v: ("Reported onset", f"Onset wording reported in {_at(v)}{_quote(v)}."),
app/backend/narrative.py:4:no dropped hedge / self-report / negation (D-022), no causation or adverse wording that the quote itself does not contain, no flag
app/backend/narrative.py:19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, self-report marker or negation that the cited quote has.",
app/backend/export.py:42:_ORDER = ["hedged_imaging", "speculative_language", "noncompliance", "missed_care", "patient_reported_onset", "patient_report",
app/db/schema.sql:39:  category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),
app/backend/grounding.py:58:# ---------------------------------------------------------------- lexicon (hedge / self-report sets)
app/backend/grounding.py:68:            if e.get("hedge") or e.get("self_report"):
app/backend/grounding.py:69:                raise ValueError(f"lexicon entry {e.get('id')} is a hedge/self_report entry without a pattern")
app/backend/grounding.py:73:        if e.get("self_report"):
app/backend/grounding.py:75:    scope = (data.get("self_report_scope") or {}).get("exclude_sentence") if isinstance(data, dict) else None
app/backend/grounding.py:76:    return {"hedge": hedges, "self_report": selfrep, "self_report_exclude": re.compile(scope, re.IGNORECASE) if scope else None}
app/backend/grounding.py:181:    """Qualifier kinds present in the excerpt and absent from the summary (D-022): hedge, self_report, negation, laterality, approx."""
app/backend/grounding.py:186:        out.append("self_report")
exit=0
== commit diff cab0068 ==
commit cab006810891bf8c705f8814ced77e341a02e272
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:55:05 2026 -0600

    fix(frontend): remove self-report label from mock overlays (D-040)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/dev/mock-data.js b/app/frontend/dev/mock-data.js
index c689002..46a1ff1 100644
--- a/app/frontend/dev/mock-data.js
+++ b/app/frontend/dev/mock-data.js
@@ -745,8 +745,8 @@ window.ZL_MOCK = {
    "type": "causation",
    "category": "patient_report",
    "source_kind": "record",
-   "title": "Patient self-report",
-   "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): \u201cPatient states symptoms began after the January collision.\u201d",
+   "title": "Reported onset",
+   "explanation": "Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): \u201cPatient states symptoms began after the January collision.\u201d",
    "computed": {},
    "evidence": [
     {
diff --git a/app/frontend/mock_flags.js b/app/frontend/mock_flags.js
index f5dcc83..75e5058 100644
--- a/app/frontend/mock_flags.js
+++ b/app/frontend/mock_flags.js
@@ -21,7 +21,7 @@
         [find(recs, 3, "Patient reports low back pain in 2023, resolved.")], { state: "needs_review", reasons: ["LLM_ONLY"], why: "The model found this; the phrase list did not." }),
       mk("f_deg_8", "pre_existing", "degenerative_language", "Degenerative wording in imaging", "Austin Imaging, cervical MRI (May 29, 2026): “Findings may represent degenerative change; correlate clinically.”",
         [find(recs, 8, "Findings may represent degenerative change; correlate clinically.")]),
-      mk("f_pat_9", "causation", "patient_report", "Patient self-report", "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
+      mk("f_pat_9", "causation", "patient_report", "Reported onset", "Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
         [find(recs, 9, "Patient states symptoms began after the January collision.")]),
     ].filter(Boolean);
   }
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:27.620Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_frontend_no_speaker_label.py"
}
````

### User / tool · 2026-11-02T02:55:27.627Z

**tool result**
````
1	"""D-040: no user-facing text in app/frontend may assert who spoke ("self-report").
2	
3	The internal CSS class `.rv-selfreport` (no hyphen) is allowed; it is not user-facing text.
4	"""
5	import re
6	from pathlib import Path
7	
8	FRONTEND = Path(__file__).resolve().parents[2] / "app" / "frontend"
9	BAD = re.compile(r"self[-\s]?report", re.I)
10	ALLOWED = {"rv-selfreport"}
11	
12	
13	def test_no_self_report_in_frontend():
14	    hits = []
15	    for p in FRONTEND.rglob("*"):
16	        if not p.is_file() or p.suffix not in {".js", ".html", ".css", ".json", ".md", ".txt"}:
17	            continue
18	        for n, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
19	            for m in BAD.finditer(line):
20	                if m.group(0).lower() in ALLOWED or "rv-selfreport" in line[max(0, m.start() - 3):m.end()]:
21	                    continue
22	                hits.append(f"{p.relative_to(FRONTEND)}:{n}: {line.strip()[:100]}")
23	    assert not hits, "D-040 violation:\n" + "\n".join(hits)
24	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:42.702Z

**tool call — Bash**
````
{
 "command": "echo \"== narrative.py context ==\" && sed -n 1,30p app/backend/narrative.py | grep -n 'SUMMARY_DROPS_QUALIFIER\\|REASON\\|def \\|^[A-Z_]* = ' ; echo \"== who reads the reason text ==\" && grep -rn 'SUMMARY_DROPS_QUALIFIER\\|REASON_TEXT\\|REASON_LABELS\\|narrative import\\|from .narrative\\|from app.backend.narrative' app/ | head -20; echo \"== reasons dict name at narrative.py:17-20 ==\" && sed -n 15,22p app/backend/narrative.py; echo \"== grounding.py:186 usage ==\" && sed -n 178,190p app/backend/grounding.py; echo \"== lexicon rationale/false_positive reaching UI? ==\" && grep -rn 'rationale\\|false_positive' app/backend app/frontend | head; echo \"== non-ascii hyphen variants in frontend ==\" && grep -rn -P 'self[\\x{2010}-\\x{2015}\\x{2212}\\x{00AD}\\x{2011}\\s_]?report' app/ -i | head; echo \"exit=$?\"",
 "description": "Check whether narrative reason text reaches the UI and scan for unicode hyphen variants"
}
````

### User / tool · 2026-11-02T02:55:42.836Z

**tool result**
````
== narrative.py context ==
16:REASONS = {
19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, self-report marker or negation that the cited quote has.",
27:_CAUSE = re.compile(r"\b(?:caused?|causing|due to|result(?:ed|ing)? (?:of|from|in)|because of|as a result|attributable|secondary to|"
29:_FLAGISH = re.compile(r"\b(?:gaps?|conflicts?|inconsisten\w+|discrepanc\w+|pre-?existing|prior (?:injur\w+|condition)|missed appointments?|"
== who reads the reason text ==
app/backend/why.py:7:    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out.",
app/backend/confidence.py:7:    "SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE",
app/backend/review.py:76:        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
app/backend/review.py:146:                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
app/backend/review.py:256:                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
app/backend/narrative.py:19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, self-report marker or negation that the cited quote has.",
app/backend/narrative.py:62:        reasons.append("SUMMARY_DROPS_QUALIFIER")
app/backend/generator.py:83:              qualifier_carried="EXCERPT_OMITS_QUALIFIER" not in code_reasons and "SUMMARY_DROPS_QUALIFIER" not in code_reasons,
app/backend/grounding.py:203:        reasons.append("SUMMARY_DROPS_QUALIFIER")
== reasons dict name at narrative.py:17-20 ==

REASONS = {
    "NOT_AN_ACCEPTED_ENTRY": "The sentence cites an entry that is not accepted.",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The sentence has a number, side, negation or date that is not in the cited quote.",
    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, self-report marker or negation that the cited quote has.",
    "CAUSATION_NOT_QUOTED": "The sentence uses cause or adverse wording that the cited quote does not contain.",
    "SEVERITY_NOT_QUOTED": "The sentence uses severity, outcome or recommendation wording that the cited quote does not contain.",
    "FLAG_CONTENT": "The sentence talks about gaps, conflicts or other review flags, which stay out of the paragraph.",
== grounding.py:186 usage ==


def dropped_qualifiers(summary: str, excerpt: str) -> list:
    """Qualifier kinds present in the excerpt and absent from the summary (D-022): hedge, self_report, negation, laterality, approx."""
    out = []
    if hedge_ids(excerpt) and not (hedge_ids(summary) or _HEDGE_WORDS.search(summary)):
        out.append("hedge")
    if _SELF_CARRIED.search(excerpt) and not _SELF_CARRIED.search(summary):   # D-022 qualifier carry only; D-040: nothing labels who is speaking
        out.append("self_report")
    ex_neg = {w.lower() for w in _NEG.findall(excerpt)}
    sm_neg = {w.lower() for w in _NEG.findall(summary)}
    if any(w not in sm_neg and not (w in ("no", "not", "none", "never") and sm_neg & {"no", "not", "none", "never"}) for w in ex_neg):
        out.append("negation")
== lexicon rationale/false_positive reaching UI? ==
== non-ascii hyphen variants in frontend ==
app/README-arch.md:78:`app/llm/lexicon.yaml` v2 (researcher): `flag_type`, `hedge`, `self_report`, `strength`, plus the `accident_date_phrases`, `non_encounter` and `injection` categories. It blocks the gap rule, the accident-date rule and the injection scan, and its golden self-check (recall per `must` flag) gates the claim that the lexicon is a floor (ADR-008.4).
app/llm/lexicon.yaml:25:#   from an excerpt (ADR-016). `self_report: true` marks wording that explicitly attributes a statement to the PATIENT (T-061); code sets
app/llm/lexicon.yaml:84:# T-061: a self_report hit is a PATIENT statement only. Before the code sets source_kind = patient_report, it must drop the hit
app/llm/lexicon.yaml:85:# when the hit's sentence matches `self_report_scope.exclude_sentence` (a named non-patient speaker with a speech verb, or
app/llm/lexicon.yaml:86:# "per <wife|husband|EMS|...>"). Bare "S:", "Subjective:" and "Self-reported" headers are not matched by any self_report entry,
app/llm/lexicon.yaml:87:# and the intake-form date entry is self_report: false. Reference implementation: research/lexicon_selfcheck.py:is_patient_statement().
app/llm/lexicon.yaml:88:self_report_scope:
app/llm/lexicon.yaml:104:  self_report: false
app/llm/lexicon.yaml:125:  self_report: false
app/llm/lexicon.yaml:142:  self_report: false
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:55:49.738Z

**tool call — Bash**
````
{
 "command": "echo \"== REASONS users ==\" && grep -rn 'REASONS\\b' app/ | grep -v 'CODE_REASONS\\|_REASONS' | head; echo \"== why.py users ==\" && grep -rn 'why\\.\\|from .why\\|import why\\|from app.backend.why\\|why_text\\|WHY' app/backend app/frontend --include=*.py --include=*.js | head -20; echo \"== why.py lines 1-12 ==\" && sed -n 1,12p app/backend/why.py; echo \"== frontend Why render ==\" && grep -rln 'why' app/frontend | head",
 "description": "Trace where reason text (why.py, narrative.REASONS) is consumed"
}
````

### User / tool · 2026-11-02T02:55:49.861Z

**tool result**
````
== REASONS users ==
app/backend/narrative.py:16:REASONS = {
app/backend/narrative.py:118:        r["message"] = REASONS.get(r["reason"], r["reason"])
== why.py users ==
app/backend/why.py:2:_WHY = {
app/backend/why.py:35:    return _WHY[code]
app/backend/why.py:39:    return list(_WHY)
app/backend/present.py:8:OK_WHY = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
app/backend/present.py:15:            out.append(why.why(c))
app/backend/present.py:18:    return " ".join(out) if out else OK_WHY
app/backend/flags.py:44:    f["why"] = " ".join(why.why(c) for c in f["reasons"]) if f["reasons"] else "Found by the phrase list and the model, and the second check agreed."
app/backend/flags.py:178:            "reasons": ["INJECTION_SUSPECTED"], "why": why.why("INJECTION_SUSPECTED"), "excerpt": hits[0]["phrase"] if hits else "",
app/backend/flags.py:216:            "reasons": ["CONFLICT_CHECK_INCOMPLETE"], "why": why.why("CONFLICT_CHECK_INCOMPLETE"), "excerpt": "", "source_kind": "record",
app/backend/generator.py:108:    e["why"] = " ".join(why.why(c) for c in reasons) if reasons else "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
app/backend/generator.py:110:    if jd.get("verdict") in ("partially", "unsupported") and why.judge_detail(jd.get("reason_code")):
app/backend/generator.py:111:        e["why"] += " " + why.judge_detail(jd["reason_code"])
app/backend/pipeline.py:15:                         judges, split_llm, totals as TT, why as WHY)
app/backend/pipeline.py:66:                "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes) or
app/backend/pipeline.py:81:                      "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes),
app/backend/pipeline.py:215:    a["why"] = " ".join(WHY.why(c) for c in reasons) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
app/frontend/manual.js:60:      msg.textContent = (err.message || "That entry was refused.") + (why.length ? " " + why.join(" ") : "");
== why.py lines 1-12 ==
"""One fixed plain-language sentence per reason code (LLM_VS_CODE row 18, api.md appendix). Never model text."""
_WHY = {
    "GROUNDING_EXCERPT_NOT_VERBATIM": "The quoted text is not word for word in the record, so this item was rejected and cannot be used.",
    "GROUNDING_AMOUNT_NOT_IN_TEXT": "The amount shown does not appear in the record text, so this item was rejected and cannot be used.",
    "SCHEMA_INVALID": "The AI output was malformed after several attempts, so this item was rejected.",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.",
    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out.",
    "EXCERPT_OMITS_QUALIFIER": "The record has a hedge sentence that qualifies this quote, but the quote leaves it out.",
    "EXCERPT_NOT_WHOLE_SENTENCE": "The quote starts or ends in the middle of a sentence.",
    "HIGHLIGHT_NOT_FOUND": "The quote could not be located in the record text, so it cannot be highlighted.",
    "JUDGE_PARTIAL": "A second AI check found the summary only partly supported by the quoted text.",
    "JUDGE_UNSUPPORTED": "A second AI check found the summary not supported by the quoted text.",
== frontend Why render ==
app/frontend/review.css
app/frontend/flags.js
app/frontend/manual.js
app/frontend/index.html
app/frontend/narrative.js
app/frontend/styles.css
app/frontend/charges.js
app/frontend/mock_flags.js
app/frontend/timeline.js
app/frontend/mock.js
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:56:02.170Z

**tool call — Bash**
````
{
 "command": "grep -rn -i 'patient' app/backend/*.py app/frontend/*.js app/frontend/*.html 2>/dev/null | grep -v '^\\s*#' | grep -i \"statement\\|reported\\|report\\|own \\|says\\|states\\|per patient\\|opinion\\|speak\\|said\\|attribut\" | head -60",
 "description": "Sweep backend and frontend for other speaker-asserting patient wording"
}
````

### User / tool · 2026-11-02T02:56:02.289Z

**tool result**
````
app/backend/flag_templates.py:25:    ("causation", "patient_reported_onset"): "patient_report",
app/backend/flag_templates.py:35:    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
app/backend/flag_templates.py:126:    "patient_report": lambda v: ("Reported onset", f"Onset wording reported in {_at(v)}{_quote(v)}."),
app/backend/grounding.py:168:# Summary side only (never used to label): wording that carries the patient attribution into a summary ("complained of", "states").
app/backend/grounding.py:169:_SELF_CARRIED = re.compile(r"\bc/o\b|\bcomplain(?:s|ed|ing|t)?\b|\b(?:patient|pt\.?|he|she|client)\s+(?:states?|stated|reports?|reported|endorses|admits|"
app/backend/grounding.py:170:                           r"recalls|claims|says|said|believes|feels|attributes|relates|denies|complains)\b|\bper\s+(?:the\s+)?(?:patient|pt)\b|"
app/backend/grounding.py:171:                           r"\bpatient-?\s?reported\b", re.IGNORECASE)
app/backend/export.py:42:_ORDER = ["hedged_imaging", "speculative_language", "noncompliance", "missed_care", "patient_reported_onset", "patient_report",
app/backend/why.py:7:    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out.",
app/frontend/mock.js:11:    5: "Pain 4/10, improving; patient reports missing 3 days of work.",
app/frontend/mock.js:15:    9: "Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.",
app/frontend/mock_flags.js:21:        [find(recs, 3, "Patient reports low back pain in 2023, resolved.")], { state: "needs_review", reasons: ["LLM_ONLY"], why: "The model found this; the phrase list did not." }),
app/frontend/mock_flags.js:24:      mk("f_pat_9", "causation", "patient_report", "Reported onset", "Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
app/frontend/mock_flags.js:25:        [find(recs, 9, "Patient states symptoms began after the January collision.")]),
app/frontend/mock_sample.js:2:window.ZL=window.ZL||{};ZL.MOCK_SAMPLE="SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data\n\n=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.\"\n\n=== Record 2 ===\nDate: 2026-01-09\nSource: Central ER discharge summary\nExcerpt: \"Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.\"\n\n=== Record 3 ===\nDate: 2026-01-16\nSource: Dr. Alvarez, primary care\nExcerpt: \"Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved.\"\n\n=== Record 4 ===\nDate: 2026-01-23\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.\"\n\n=== Record 5 ===\nDate: 2026-02-20\nSource: Capital PT, visit 8\nExcerpt: \"Pain 4/10, improving. Patient reports missing 3 days of work.\"\n\n=== Record 6 ===\nDate: 2026-03-06\nSource: Capital PT, visit 9\nExcerpt: \"Discharged from PT after two missed appointments. Pain 3/10.\"\n\n=== Record 7 ===\nDate: 2026-05-18\nSource: Hill Country Pain Management, new patient\nExcerpt: \"New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.\"\n\n=== Record 8 ===\nDate: 2026-05-29\nSource: Austin Imaging, cervical MRI\nExcerpt: \"C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.\"\n\n=== Record 9 ===\nDate: 2026-06-12\nSource: Hill Country Pain Management, follow-up\nExcerpt: \"Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.\"";
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:56:09.490Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git status --short | head -30 && echo \"--- diff HEAD vs cab0068 on reviewed files (should be empty if commit = tree) ---\" && git diff --stat cab0068 -- app/frontend app/backend tests/unit/test_frontend_no_speaker_label.py && echo \"--- T-074 files ---\" && git diff --stat 312ed92 -- spec/REQUIREMENTS.md && git show 312ed92 -- spec/REQUIREMENTS.md | cat",
 "description": "Check HEAD, dirty files, and the T-074 spec commit diff"
}
````

### User / tool · 2026-11-02T02:56:09.711Z

**tool result**
````
b9d3ead
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
 M board/cards/T-065.md
 M board/cards/T-066.md
 M board/cards/T-067.md
 M evals/reports/latest.json
 M memory/LESSONS.md
 M tools/board_ui.html
 M tools/tests/test_board_server.py
?? .claude/agent-memory/claims-adjuster-reviewer/feedback_persona_identity_on_filing.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_d040_label_cut_residue.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t061_r4_separator_list.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t067_credibility_negation_and_recall.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t071_chip_cut_harness_sweep.md
?? .claude/agent-memory/claims-adjuster-reviewer/reference_spare_port_app_server.md
--- diff HEAD vs cab0068 on reviewed files (should be empty if commit = tree) ---
 app/backend/credibility.py    | 57 +++++++++++++++++++++++++++++++++++++++++++
 app/backend/flag_templates.py |  2 +-
 app/backend/flags.py          | 22 +++++------------
 3 files changed, 64 insertions(+), 17 deletions(-)
--- T-074 files ---
commit 312ed928a3d8563aa80721d1604a04f6f68f0b89
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:54:40 2026 -0600

    spec: R-FL-7 rewritten for D-040 (T-074 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/spec/REQUIREMENTS.md b/spec/REQUIREMENTS.md
index 9af2178..958f58b 100644
--- a/spec/REQUIREMENTS.md
+++ b/spec/REQUIREMENTS.md
@@ -68,7 +68,7 @@ Four types: `gap`, `conflict`, `pre_existing`, `causation`. Gap math is code ove
 | R-FL-4 | **Language that weakens causation.** The tool quotes the wording; it never rules on causation. All five Appendix C items are `must` (K1–K5): records 8, 6 and 9, "New onset" in record 7, and the wrong accident date in record 7's intake line. Matching is one-to-one: each golden flag is satisfied by at most one tool flag, matched on type, cited records and overlapping evidence excerpt, so one record-7 flag about "new onset" can't also count for the intake date. | Sample: the tool emits a `causation` flag whose evidence is "New onset pain radiating to right arm" (K4) and a separate `causation` flag whose evidence is "Date of accident per intake form: 2026-01-19." (K5); the K5 line appears in the internal notes. Golden `must_not` every `must_not` item in `evals/golden` all pass (no "herniation", no "degenerative" in the tool's own voice, no "traumatic", no recovery claim). | EV `flag_*[causation]` + negative assertions + PR (claims-adjuster) |
 | R-FL-5 | Every flag cites verbatim excerpt(s) that pass the grounding check. An ungrounded flag is `rejected`. | Verifier test on flags, same as R-TL-2. | UT + EV `grounding_rate` |
 | R-FL-6 | Flags are grouped by type (four groups) with a fifth "Record warnings" group (dates to confirm, injection suspicion). Each shows its state and, when `needs_review`, a one-sentence reason. | E2E: the sample shows at least one flag in each of the four type groups; `case_01` shows a dates-to-confirm item; `case_07` shows an injection warning. | E2E |
-| R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = "patient_report"` and the UI text "Patient self-report". It is never presented as a physician's opinion. | Sample record 9 flag has `source_kind == "patient_report"` and the label renders. Golden `must_not` M10 passes. | UT + E2E |
+| R-FL-7 | **No speaker label (D-040, replaces the self-report label).** Excerpts are verbatim, so the text shows who spoke; no flag, entry or export line asserts the speaker. The sample record 9 onset flag is titled "Reported onset" and is never presented as a physician's opinion. | No user-facing text contains "self-report"; sample record 9 flag carries no `patient_report` source_kind. Golden `must_not` M10 passes. | UT + E2E |
 | R-FL-8 | **Flag text is code (D-007).** Titles and explanations come from code templates. The LLM returns only the category and excerpt spans for a flag. | UT: the LLM output schema for flags has no free-text field; every flag title and explanation equals the template output for its type and computed values. | UT |
 
 ### 1.4 Billed charges
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:56:16.546Z

**tool call — Bash**
````
{
 "command": "git log --oneline -6 && echo \"--- ancestry ---\" && git merge-base --is-ancestor cab0068 HEAD && echo \"cab0068 ancestor of HEAD\" && git merge-base --is-ancestor 312ed92 cab0068 && echo \"312ed92 ancestor of cab0068\" && echo \"--- R-FL-7 line at HEAD and at 312ed92 ---\" && grep -n 'R-FL-7' spec/REQUIREMENTS.md && git show 312ed92:spec/REQUIREMENTS.md | grep -n 'R-FL-7 ' && echo \"--- spec/ changes between 312ed92 and HEAD ---\" && git diff --stat 312ed92 HEAD -- spec/ evals/golden tests/unit/test_eval_spec_check.py tests/unit/test_frontend_no_speaker_label.py; echo \"--- test_eval_spec_check at 312ed92 ---\"; ls tests/unit/test_eval_spec_check.py tests/unit/test_frontend_no_speaker_label.py",
 "description": "Confirm commit ancestry and locate R-FL-7 line"
}
````

### User / tool · 2026-11-02T02:56:16.774Z

**tool result**
````
b9d3ead chore(backend): narrative fixtures for sample and case_01-09 (curated + recorded), make_curated drafts the narrative; A-109
f6fa2dd fix(backend): credibility wording is a negation-aware family match; neutral template (T-067 r2, D-038)
815d616 fix(evals): refuse live backend without ENABLE_LIVE instead of silently running fixture (T-070)
cab0068 fix(frontend): remove self-report label from mock overlays (D-040)
312ed92 spec: R-FL-7 rewritten for D-040 (T-074 r2)
37a76a8 fix(frontend): confirmed orphan date stays visible under Records without an entry; excerpt in Dates row; no double listing (T-068 r2)
--- ancestry ---
cab0068 ancestor of HEAD
312ed92 ancestor of cab0068
--- R-FL-7 line at HEAD and at 312ed92 ---
71:| R-FL-7 | **No speaker label (D-040, replaces the self-report label).** Excerpts are verbatim, so the text shows who spoke; no flag, entry or export line asserts the speaker. The sample record 9 onset flag is titled "Reported onset" and is never presented as a physician's opinion. | No user-facing text contains "self-report"; sample record 9 flag carries no `patient_report` source_kind. Golden `must_not` M10 passes. | UT + E2E |
371:| 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` and checks `required_terms` on summary+excerpt; D-022 and R-FL-7/R-TL-10 say `patient_report` and summary alone. Not a request to qa: the orchestrator records which wins, and the loser is edited by its owner. | `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md` | orchestrator (D-entry) |
71:| R-FL-7 | **No speaker label (D-040, replaces the self-report label).** Excerpts are verbatim, so the text shows who spoke; no flag, entry or export line asserts the speaker. The sample record 9 onset flag is titled "Reported onset" and is never presented as a physician's opinion. | No user-facing text contains "self-report"; sample record 9 flag carries no `patient_report` source_kind. Golden `must_not` M10 passes. | UT + E2E |
--- spec/ changes between 312ed92 and HEAD ---
 tests/unit/test_frontend_no_speaker_label.py | 23 +++++++++++++++++++++++
 1 file changed, 23 insertions(+)
--- test_eval_spec_check at 312ed92 ---
tests/unit/test_eval_spec_check.py
tests/unit/test_frontend_no_speaker_label.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:56:25.529Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/t072\" \"$S/t074\" && cd /Users/arsis/zlayt-pm-project && git archive cab0068 | tar -x -C \"$S/t072\" && git archive 312ed92 | tar -x -C \"$S/t074\" && cd \"$S/t072\" && echo \"== T-072 test at cab0068 archive ==\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_frontend_no_speaker_label.py; echo \"exit=$?\"; cd /Users/arsis/zlayt-pm-project && echo \"== T-072 test on live tree HEAD b9d3ead ==\" && .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_frontend_no_speaker_label.py; echo \"exit=$?\"; echo \"== T-074 spec-check tests at 312ed92 archive ==\" && cd \"$S/t074\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_spec_check.py; echo \"exit=$?\"",
 "description": "Extract cab0068 and 312ed92 archives to scratchpad and run the target tests"
}
````

### User / tool · 2026-11-02T02:56:26.869Z

**tool result**
````
== T-072 test at cab0068 archive ==
.                                                                        [100%]
1 passed in 0.01s
exit=0
== T-072 test on live tree HEAD b9d3ead ==
.                                                                        [100%]
1 passed in 0.01s
exit=0
== T-074 spec-check tests at 312ed92 archive ==
...                                                                      [100%]
3 passed in 0.03s
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:56:32.901Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; rm -rf \"$S/p_fe\" \"$S/p_be\" && cp -R \"$S/t072\" \"$S/p_fe\" && cp -R \"$S/t072\" \"$S/p_be\" && printf '\\n// PLANT\\nconst planted = \"Patient self-report (not a physician opinion)\";\\n' >> \"$S/p_fe/app/frontend/mock_flags.js\" && printf '\\n# PLANT\\nPLANT_TEXT = \"Patient self-report\"\\n' >> \"$S/p_be/app/backend/why.py\" && echo \"== plant frontend ==\" && (cd \"$S/p_fe\" && $PY -m pytest -q -p no:cacheprovider tests/unit/test_frontend_no_speaker_label.py 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\") ; echo \"== plant backend why.py (test scope check) ==\" && (cd \"$S/p_be\" && $PY -m pytest -q -p no:cacheprovider tests/unit/test_frontend_no_speaker_label.py 2>&1 | tail -3; echo \"exit=${PIPESTATUS[0]}\"); echo \"== why text at cab0068 archive ==\" && (cd \"$S/t072\" && $PY -c 'import sys; sys.path.insert(0, \"app/backend\"); import why; print(why.why(\"SUMMARY_DROPS_QUALIFIER\"))'); echo \"== api.py static mount for dev/ ==\" && grep -n 'StaticFiles\\|mount' \"$S/t072/app/backend/api.py\" | head -5; echo \"== flags.js renders f.why? ==\" && grep -n '\\.why' \"$S/t072/app/frontend/flags.js\" | head -5",
 "description": "Plant test strings in scratch copies and confirm why-text reaches the UI code"
}
````

### User / tool · 2026-11-02T02:56:34.647Z

**tool result**
````
== plant frontend ==
E       AssertionError: D-040 violation:
E         mock_flags.js:58: const planted = "Patient self-report (not a physician opinion)";
E       assert not ['mock_flags.js:58: const planted = "Patient self-report (not a physician opinion)";']

tests/unit/test_frontend_no_speaker_label.py:23: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_frontend_no_speaker_label.py::test_no_self_report_in_frontend
1 failed in 0.04s
exit=1
== plant backend why.py (test scope check) ==
.                                                                        [100%]
1 passed in 0.02s
exit=0
== why text at cab0068 archive ==
The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out.
== api.py static mount for dev/ ==
36:STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]
348:            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
371:                    "counts": {"entries": len(DB.list_items(c, token, "entry")), "amounts": len(DB.list_items(c, token, "amount")),
489:                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
490:                              "rejected": sum(1 for k in ("entry", "amount") for r in DB.list_items(c, token, k) if r["state"] == "rejected")}
== flags.js renders f.why? ==
68:      f.state === "needs_review" && f.why ? el("p", { class: "rv-reason-line" }, el("strong", {}, "Needs review: "), f.why) : f.why ? el("p", { class: "rv-why" }, f.why) : null,
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:56:42.084Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; T=\"$S/t072\"; echo \"== narrative.py:110-120 ==\" && sed -n 108,120p \"$T/app/backend/narrative.py\"; echo \"== narrative.js use of message ==\" && grep -n 'message' \"$T/app/frontend/narrative.js\" | head -8; echo \"== grep literal self-report user-facing candidates in cab0068 archive ==\" && grep -rn -i 'self[-\\s]\\?report' \"$T/app/backend\" \"$T/app/frontend\" | grep -v 'lexicon.yaml\\|self_report' ; echo \"== flag why / flags.py path for SUMMARY_DROPS_QUALIFIER reach ==\" && grep -n 'SUMMARY_DROPS_QUALIFIER\\|dropped_qualifiers' \"$T/app/backend/grounding.py\" \"$T/app/backend/pipeline.py\" \"$T/app/backend/flags.py\" | head -6",
 "description": "Confirm narrative message reaches the UI and list literal self-report hits at cab0068"
}
````

### User / tool · 2026-11-02T02:56:42.243Z

**tool result**
````
== narrative.py:110-120 ==
        verdict, jcall, jcode = judges.run_j1_meta(text, e["excerpt"], f"{e['label']} (date of service {export._long_date(e['date_iso'])})",
                                                   call=call, item_id=item["id"])
        lad = judges.to_ladder("j1", verdict)
        item["judge"] = {"model": judges.judge_model(), "prompt_version": "judge_faithfulness_v1", "call_id": jcall, "verdict": lad, "reason_code": jcode}
        if lad != "supported":
            base["removed"].append({**item, "reason": {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED"}.get(lad, "JUDGE_UNAVAILABLE")})
            continue
        item["cite"] = e["cite"]
        base["sentences"].append(item)
    for r in base["removed"]:
        r["message"] = REASONS.get(r["reason"], r["reason"])
    return _save(conn, case_id, case, base)

== narrative.js use of message ==
30:    } catch (e) { msgText = (e && e.message) || "That did not work."; msgErr = true; }
55:          el("ul", {}, nar.removed.map((r) => el("li", {}, "“" + r.text + "” — " + (r.message || r.reason))))));
== grep literal self-report user-facing candidates in cab0068 archive ==
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/backend/grounding.py:58:# ---------------------------------------------------------------- lexicon (hedge / self-report sets)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/backend/narrative.py:4:no dropped hedge / self-report / negation (D-022), no causation or adverse wording that the quote itself does not contain, no flag
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/backend/narrative.py:19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, self-report marker or negation that the cited quote has.",
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/frontend/review.css:27:.rv-selfreport { background: #e8eefc; color: #1b3a8a; border-color: #a9bbea; }
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/frontend/review.js:276:        if (!head.querySelector('[data-testid="entered-by"]')) head.append(el("span", { class: "rv-chip rv-selfreport", "data-testid": "entered-by" }, "Entered by reviewer"));
== flag why / flags.py path for SUMMARY_DROPS_QUALIFIER reach ==
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/backend/grounding.py:180:def dropped_qualifiers(summary: str, excerpt: str) -> list:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/backend/grounding.py:202:    if dropped_qualifiers(summary, excerpt):
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/backend/grounding.py:203:        reasons.append("SUMMARY_DROPS_QUALIFIER")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:56:56.067Z

**tool call — Bash**
````
{
 "command": "echo \"== spec/contracts/docs/golden residue at 312ed92 ==\" && git grep -n -i 'self-report\\|self report\\|patient_self_report' 312ed92 -- spec/ memory/contracts docs/ evals/golden | sed 's/^/  /'; echo \"== same at HEAD b9d3ead (count) ==\" && git grep -c -i 'self-report\\|patient_self_report' b9d3ead -- spec/ memory/contracts docs/ evals/golden; echo \"== R-FL-7 acceptance vs test name ==\" && sed -n 71p spec/REQUIREMENTS.md | cut -c1-400; echo \"== evals/golden README row check (spec row 371 evidence cmd) ==\" && git show 312ed92:evals/golden/README.md | grep -n 'patient_self_report\\|summary+excerpt'; echo \"exit=$?\"; echo \"== golden K3 summary ==\" && git show 312ed92:evals/golden/sample.expected.json | grep -n 'Causation rests on patient self-report'",
 "description": "Grep spec, contracts, docs and golden for remaining self-report residue at 312ed92"
}
````

### User / tool · 2026-11-02T02:56:56.264Z

**tool result**
````
== spec/contracts/docs/golden residue at 312ed92 ==
  312ed92:docs/CONTRACT.md:617:- **Causation-weakening language:** "may represent degenerative change; correlate clinically" (8); "Discharged from PT after two missed appointments" (6); "Patient states symptoms began after the January collision" (9 — patient self-report, not a physician's causation opinion); "New onset" symptoms after a 73-day gap (7); the wrong accident date (7).
  312ed92:docs/LLM_VS_CODE.md:41:| 13 | Language that weakens causation ("may represent degenerative change", "patient states", missed appointments, "new onset", scene facts such as refusing transport, an attorney referral; normal or negative exam findings are context only (D-032); defense credibility wording such as "out of proportion" or Waddell signs raises a flag (D-038), see the second-wave section) | Same as row 12 (per record). No code or model labels who is speaking: the patient self-report chip is cut (D-040), and every excerpt is shown verbatim with its source label. | Same. The tool points at the record's own words; it never rules on causation. | Same, plus golden "must not" checks (no "degenerative" or "traumatic" in the tool's own voice). |
  312ed92:docs/LLM_VS_CODE.md:99:- **Narrower flags (D-032, D-038) and the cut self-report chip (D-040).**
  312ed92:docs/LLM_VS_CODE.md:101:  - *D-040 (supersedes D-033, D-035 and D-037; code removed in T-071, commit a27e3a4):* the **patient self-report chip is cut**. Every excerpt is shown as a verbatim record excerpt with its source label; no code or model labels who is speaking, because four review rounds kept finding mixed excerpts that a closed rule still mislabeled, and the excerpt already shows who spoke. Open: T-072 gives the `patient_reported_onset` flag a neutral title and drops "(patient self-report)" from the export. The qualifier-carry check (a summary must keep "complained of" and similar) is separate and unaffected.
  312ed92:docs/UI_DESIGN_BRIEF.md:6:D-010/D-011 (accept / edit / dismiss, nothing accepted by default, no batch accept); D-019 (one total line); D-022 (self-report per quote);
  312ed92:docs/UI_DESIGN_BRIEF.md:132:| `Patient self-report` | speech bubble | Patient self-report | `--text-muted` outline | only where code set `source_kind=patient_report` (T-061 narrows this) |
  312ed92:evals/golden/README.md:72:* **Entries.** Found when the product emits an entry that covers `record_nos`, has the same `date` (or both ambiguous), `provider` equal to the record's header label after whitespace normalization (code copies it; merged duplicates take the lowest-numbered record's label), an excerpt containing every `must_contain_excerpt` item, and a **summary** that by itself satisfies every `required_terms` item (case-insensitive, whitespace-collapsed). A summary that drops a qualifier its excerpt carries (hedge, negation such as "without loss of consciousness", laterality, "approx.", self-report marker) is `needs_review` with reason `SUMMARY_DROPS_QUALIFIER` (D-022) and counts as not found. **Self-report:** for each `self_report_spans` item the summary must contain ≥ 1 `attribution_any` word, else the same reason. Spans are subjective sentences only (no findings, assessments or measurements). Recall pooled across cases ≥ 95%. More entries than `expected_entry_count` = dedupe failure.
  312ed92:evals/golden/check_golden.py:21:    date; summaries satisfy required_terms (summary alone) and keep self-report attribution; numbers in summaries come from the
  312ed92:evals/golden/check_golden.py:491:                errs.append(f"export letter: summary for record {n} drops the self-report attribution for {sp['excerpt'][:30]!r}")
  312ed92:evals/golden/check_golden.py:543:        exported[int(m.group(1))] = {x.strip().lower().replace(" (patient self-report)", "") for x in m.group(2).split(";")}
  312ed92:evals/golden/hallucinations.jsonl:10:{"id": "H10", "synthetic": true, "category": "causation", "record_text": "Record 9 | 2026-06-12 | Hill Country Pain Management, follow-up | \"Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.\"", "candidate_summary": "The treating physician concluded the symptoms were caused by the January collision.", "why_unsupported": "The record says 'Patient states symptoms began after the January collision': a patient self-report, not a physician's causation opinion."}
  312ed92:evals/golden/sample.expected.json:625:      "summary": "Causation rests on patient self-report, not a physician's causation opinion.",
  312ed92:evals/golden/sample.expected.json:990:      "statement": "Presents the patient's self-report (records 1, 9) as a physician's opinion or examination finding.",
  312ed92:memory/contracts/api.md:185:      "title": "Patient self-report",
  312ed92:memory/contracts/api.md:186:      "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
  312ed92:memory/contracts/api.md:469:| `SUMMARY_DROPS_QUALIFIER` | needs_review | the excerpt has a hedge, self-report marker, negation, laterality or "approx." that the summary leaves out (D-022) |
  312ed92:spec/REQUIREMENTS.md:55:| R-TL-8 | **A hedge travels with its finding (D-018, D-021).** The **hedge set** is the lexicon entries with `hedge: true` in `app/llm/lexicon.yaml` (D-018); today `may_represent`, `correlate_clinically`, `possibility_terms`, `cannot_exclude`, `suggestive_versus_hedges`, `nonspecific_indeterminate`, `likely_alternative_cause`. When a selected sentence unit is qualified by a hedge unit, in the same unit or in the immediately following unit(s) of the same record, the hedge unit(s) must be in the excerpt, or the entry is `needs_review` with reason `EXCERPT_OMITS_QUALIFIER`. Other lexicon sentences (`pre_existing`, `compliance`, self-report) are **not** forced into the excerpt; they surface as flags. A unit is never cut (R-TL-2). | UT: the hedge set loads from `lexicon.yaml` (`hedge: true`), is non-empty and contains `may_represent` and `correlate_clinically`. Seeded entry 8 with excerpt "C5-C6 disc protrusion with mild right foraminal narrowing." → `needs_review` (`EXCERPT_OMITS_QUALIFIER`); with "…narrowing. Findings may represent degenerative change; correlate clinically." → `verified`. Entry 3 with excerpt "Persistent neck pain 6/10, daily headaches." and entry 5 with "Pain 4/10, improving." stay `verified` (their other sentences are `pre_existing` and damages wording, not hedges). Entry 6's default excerpt is checked by `entry_recall` (`must_contain_excerpt`: "Discharged from PT after two missed appointments"). | UT + EV |
  312ed92:spec/REQUIREMENTS.md:57:| R-TL-10 | **Summaries keep the numbers and the qualifiers (D-006, D-022).** (a) A number, date, dollar figure or the word left, right, no, not or without in a summary must appear in the item's excerpt, the record's source label or its parsed date (token set: ADR-012 `grounding.new_tokens`) (so "visit 8" and a heading year don't trip it), or the entry is `needs_review` (`SUMMARY_TOKEN_NOT_IN_EXCERPT`). (b) If the excerpt contains a qualifier (a hedge, a self-report marker, a negation such as "without loss of consciousness", laterality, "approx.") and the **summary** omits it, the entry is `needs_review` (`SUMMARY_DROPS_QUALIFIER`). Both are code checks and don't rely on the judge. | UT: summary "pain 4/10" with excerpt "Pain 3/10." → `needs_review` (a). Summary "Diagnosed with concussion" for entry 2 → `needs_review` (b, drops "without loss of consciousness"). Sample entries pass, including "Visit 8: …" where "8" comes from the label "Capital PT, visit 8". Golden `required_terms` are checked against the summary alone (qa, §8). | UT + EV |
  312ed92:spec/REQUIREMENTS.md:71:| R-FL-7 | **No speaker label (D-040, replaces the self-report label).** Excerpts are verbatim, so the text shows who spoke; no flag, entry or export line asserts the speaker. The sample record 9 onset flag is titled "Reported onset" and is never presented as a physician's opinion. | No user-facing text contains "self-report"; sample record 9 flag carries no `patient_report` source_kind. Golden `must_not` M10 passes. | UT + E2E |
  312ed92:spec/REQUIREMENTS.md:371:| 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` and checks `required_terms` on summary+excerpt; D-022 and R-FL-7/R-TL-10 say `patient_report` and summary alone. Not a request to qa: the orchestrator records which wins, and the loser is edited by its owner. | `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md` | orchestrator (D-entry) |
  312ed92:spec/SAMPLE_CASE_TRUTHS.md:9:- **Causation-weakening language:** "may represent degenerative change; correlate clinically" (8); "Discharged from PT after two missed appointments" (6); "Patient states symptoms began after the January collision" (9 — patient self-report, not a physician's causation opinion); "New onset" symptoms after a 73-day gap (7); the wrong accident date (7).
== same at HEAD b9d3ead (count) ==
b9d3ead:docs/CONTRACT.md:1
b9d3ead:docs/LLM_VS_CODE.md:3
b9d3ead:docs/UI_DESIGN_BRIEF.md:2
b9d3ead:evals/golden/README.md:1
b9d3ead:evals/golden/check_golden.py:3
b9d3ead:evals/golden/hallucinations.jsonl:1
b9d3ead:evals/golden/sample.expected.json:2
b9d3ead:memory/contracts/api.md:3
b9d3ead:spec/REQUIREMENTS.md:4
b9d3ead:spec/SAMPLE_CASE_TRUTHS.md:1
== R-FL-7 acceptance vs test name ==
| R-FL-7 | **No speaker label (D-040, replaces the self-report label).** Excerpts are verbatim, so the text shows who spoke; no flag, entry or export line asserts the speaker. The sample record 9 onset flag is titled "Reported onset" and is never presented as a physician's opinion. | No user-facing text contains "self-report"; sample record 9 flag carries no `patient_report` source_kind. Golden `m
== evals/golden README row check (spec row 371 evidence cmd) ==
exit=1
== golden K3 summary ==
625:      "summary": "Causation rests on patient self-report, not a physician's causation opinion.",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:57:14.099Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; T=\"$S/t072\"; echo \"== does any fixture/golden carry the why text or the reason code? ==\" && grep -rln 'carries a qualifier\\|SUMMARY_DROPS_QUALIFIER' \"$T/tests/fixtures\" \"$T/evals/golden\" \"$T/app/frontend\" 2>/dev/null | head; echo \"== mock_flags.js line 24 + mock-data.js 746-750 at cab0068 ==\" && grep -n 'f_pat_9' \"$T/app/frontend/mock_flags.js\" && sed -n 745,752p \"$T/app/frontend/dev/mock-data.js\"; echo \"== flags.js:64-66 title/aria ==\" && sed -n 62,68p \"$T/app/frontend/flags.js\" | cut -c1-220; echo \"== lines in why.py/narrative.py at cab0068 (for citations) ==\" && grep -n 'SUMMARY_DROPS_QUALIFIER' \"$T/app/backend/why.py\" \"$T/app/backend/narrative.py\"; grep -n 'self-report' \"$T/app/backend/narrative.py\"; echo \"== test scope glob ==\" && grep -n 'FRONTEND =\\|BAD =' \"$T/tests/unit/test_frontend_no_speaker_label.py\"",
 "description": "Check fixture reachability of the qualifier why-text and cite exact lines"
}
````

### User / tool · 2026-11-02T02:57:14.290Z

**tool result**
````
== does any fixture/golden carry the why text or the reason code? ==
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/evals/golden/README.md
== mock_flags.js line 24 + mock-data.js 746-750 at cab0068 ==
24:      mk("f_pat_9", "causation", "patient_report", "Reported onset", "Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
   "type": "causation",
   "category": "patient_report",
   "source_kind": "record",
   "title": "Reported onset",
   "explanation": "Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): \u201cPatient states symptoms began after the January collision.\u201d",
   "computed": {},
   "evidence": [
    {
== flags.js:64-66 title/aria ==
    const seqs = (RV.sourceTargets(f, "flag").ids || []).map((id) => recSeq(c, id));
    const note = f.reviewer_note || (f.edited && f.edited.note);
    const a = el("article", { class: "rv-card rv-flag", tabindex: "0", role: "group", "aria-label": f.title, "data-testid": "flag-" + f.id, "data-item-id": f.id,
      "data-flag-type": f.type, "data-category": f.category, "data-state": f.state, "data-review": f.review_status || "pending" },
      el("div", { class: "rv-head" }, el("h4", { class: "rv-title" }, f.title), RV.chips(f)),
      el("p", { class: "rv-text-body" }, f.explanation),
      f.state === "needs_review" && f.why ? el("p", { class: "rv-reason-line" }, el("strong", {}, "Needs review: "), f.why) : f.why ? el("p", { class: "rv-why" }, f.why) : null,
== lines in why.py/narrative.py at cab0068 (for citations) ==
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/backend/why.py:7:    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out.",
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/backend/narrative.py:19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, self-report marker or negation that the cited quote has.",
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t072/app/backend/narrative.py:62:        reasons.append("SUMMARY_DROPS_QUALIFIER")
4:no dropped hedge / self-report / negation (D-022), no causation or adverse wording that the quote itself does not contain, no flag
19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, self-report marker or negation that the cited quote has.",
== test scope glob ==
8:FRONTEND = Path(__file__).resolve().parents[2] / "app" / "frontend"
9:BAD = re.compile(r"self[-\s]?report", re.I)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:57:24.431Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; T=\"$S/t072\"; cd \"$T\" && grep -n '\\.why' app/frontend/review.js | cut -c1-200; echo \"--- review.py:76 ---\"; sed -n 76p app/backend/review.py | cut -c1-200; echo \"--- pipeline.py:66, generator.py:108 ---\"; sed -n 66p app/backend/pipeline.py | cut -c1-160; sed -n 108p app/backend/generator.py | cut -c1-160; echo \"--- present.py patient_report (API payload) ---\"; grep -n '\"category\"' app/backend/present.py | cut -c1-160; echo \"--- mock_flags.js and dev sample references ---\"; grep -n 'mock_flags' app/frontend/index.html; echo \"--- test file guard lines ---\"; grep -n 'def test' tests/unit/test_frontend_no_speaker_label.py; ls /Users/arsis/zlayt-pm-project/reviews/ | grep -i 'T-072\\|T-074'",
 "description": "Cite exact lines for entry-why rendering, review path and API category"
}
````

### User / tool · 2026-11-02T02:57:24.584Z

**tool result**
````
--- review.py:76 ---
        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
--- pipeline.py:66, generator.py:108 ---
                "state": state, "reasons": why_codes, "why": " ".join(WHY.why(c) for c in why_codes) or
    e["why"] = " ".join(why.why(c) for c in reasons) if reasons else "Quote found word for word, every number in the summary is in the quote, and the second che
--- present.py patient_report (API payload) ---
74:    return {**_common(row), "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
--- mock_flags.js and dev sample references ---
45:<script src="mock_flags.js"></script>
--- test file guard lines ---
13:def test_no_self_report_in_frontend():
T-072-claims-adjuster.md
T-074-claims-adjuster.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:57:27.810Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; T=\"$S/t072\"; cd \"$T\" && grep -n 'why' app/frontend/timeline.js app/frontend/review.js app/frontend/narrative.js | cut -c1-200 | head -12",
 "description": "Find where entry why-text is rendered in the frontend"
}
````

### User / tool · 2026-11-02T02:57:27.914Z

**tool result**
````
app/frontend/timeline.js:31:        el("button", { type: "button", class: "btn small", "data-testid": "entry-why", onclick: () => openWhy(e.id) }, "Why?"),
app/frontend/timeline.js:100:        el("p", { class: "summary" }, t.why),
app/frontend/timeline.js:111:    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
app/frontend/timeline.js:113:    ZL.$("#why-title").textContent = ent ? `Why? ${ent.provider}, ${ent.date || "undated"}` : "Why? this item";
app/frontend/timeline.js:119:        el("p", { class: "why-sentence", "data-testid": "why-text" }, it.why),
app/frontend/timeline.js:120:        el("dl", { class: "kv", "data-testid": "why-ladder" },
app/frontend/timeline.js:121:          el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
app/frontend/timeline.js:122:          el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
app/frontend/timeline.js:123:          lad.generator ? [el("dt", {}, "Drafted by"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
app/frontend/timeline.js:125:          el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) =>
app/frontend/timeline.js:126:          el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.pr
app/frontend/narrative.js:51:          el("p", { class: "rv-text-body" }, s.text), el("p", { class: "rv-why" }, "Source: " + s.cite + (s.judge && s.judge.verdict ? " · second check: " + s.judge.verdi
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:57:43.604Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; T=\"$S/t072\"; cd \"$T\" && echo \"== grep -c self-report mock-data.js (cab0068) ==\" && grep -c -i 'self-report' app/frontend/dev/mock-data.js; echo \"== frontend self[-\\\\s]?report hits (cab0068) ==\" && grep -rn -i -P 'self[-\\s]?report' app/frontend; echo \"== flags.js:65 data-category ==\" && grep -n 'data-category' app/frontend/flags.js | cut -c1-120; echo \"== backend hits (cab0068) ==\" && grep -rn -i -P 'self[-\\s]?report' app/backend | cut -c1-120; echo \"== why.py:7 / narrative.py:19 / narrative.js:55 / timeline.js:119 ==\" && grep -n 'patient statement' app/backend/why.py | cut -c1-60; grep -n 'self-report marker' app/backend/narrative.py | cut -c1-60; sed -n 55p app/frontend/narrative.js | cut -c1-120; sed -n 119p app/frontend/timeline.js | cut -c1-120; echo \"== T-074 spec line 280/291 vs golden 58/69 at 312ed92 ==\" && cd /Users/arsis/zlayt-pm-project && diff <(git show 312ed92:spec/REQUIREMENTS.md | sed -n 280p) <(git show 312ed92:evals/golden/sample.export.expected.txt | sed -n 58p) && diff <(git show 312ed92:spec/REQUIREMENTS.md | sed -n 291p) <(git show 312ed92:evals/golden/sample.export.expected.txt | sed -n 69p) && echo \"both identical\"; echo \"== R-FL-7 at 312ed92 line 71 grep ==\" && git show 312ed92:spec/REQUIREMENTS.md | grep -n 'No speaker label (D-040' | cut -c1-80; echo \"== HEAD pin ==\" && git rev-parse --short HEAD",
 "description": "Final verification counts, citation lines, and T-074 golden alignment"
}
````

### User / tool · 2026-11-02T02:57:43.959Z

**tool result**
````
== grep -c self-report mock-data.js (cab0068) ==
0
== frontend self[-\s]?report hits (cab0068) ==
app/frontend/review.css:27:.rv-selfreport { background: #e8eefc; color: #1b3a8a; border-color: #a9bbea; }
app/frontend/review.js:276:        if (!head.querySelector('[data-testid="entered-by"]')) head.append(el("span", { class: "rv-chip rv-selfreport", "data-testid": "entered-by" }, "Entered by reviewer"));
== flags.js:65 data-category ==
65:      "data-flag-type": f.type, "data-category": f.category, "data-state": f.state, "data-review": f.review_status ||
== backend hits (cab0068) ==
app/backend/narrative.py:4:no dropped hedge / self-report / negation (D-022), no causation or adverse wording that the q
app/backend/narrative.py:19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, self-report marker or negation t
app/backend/grounding.py:58:# ---------------------------------------------------------------- lexicon (hedge / self-rep
== why.py:7 / narrative.py:19 / narrative.js:55 / timeline.js:119 ==
7:    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a 
19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedg
          el("ul", {}, nar.removed.map((r) => el("li", {}, "“" + r.text + "” — " + (r.message || r.reason))))));
        el("p", { class: "why-sentence", "data-testid": "why-text" }, it.why),
== T-074 spec line 280/291 vs golden 58/69 at 312ed92 ==
both identical
== R-FL-7 at 312ed92 line 71 grep ==
71:| R-FL-7 | **No speaker label (D-040, replaces the self-report label).** Exce
== HEAD pin ==
43fc69e
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:58:39.542Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-072-claims-adjuster-r2.md",
 "content": "# T-072 round 2: claims-adjuster-reviewer (D-040 follow-through, commit cab0068)\n\n**Verdict: fail** (two blockers, one major, two minors). The round-1 blocker is closed: the mock overlays now say \"Reported onset\" and the frontend guard test passes. The D-040 rule still fails in two backend strings the card did not touch, and the guard test does not scan the backend, so it cannot catch them.\n\nModel: claude-haiku-5-5 (the running model; the dossier's expected id does not match what is running).\nScope note: HEAD moved during the review (b9d3ead, then 43fc69e). I reviewed cab0068 via `git archive` into the scratchpad, not the live tree.\n\n## What I checked\n\n- **Round-1 blocker closed (pass).** `app/frontend/mock_flags.js:24` now reads `mk(\"f_pat_9\", \"causation\", \"patient_report\", \"Reported onset\", \"Onset wording reported in Hill Country Pain Management, ...\")`. `app/frontend/dev/mock-data.js:748-749` reads `\"title\": \"Reported onset\"` and `\"explanation\": \"Onset wording reported in ...\"`. `grep -c -i 'self-report' app/frontend/dev/mock-data.js` returns 0.\n- **Frontend grep (pass).** `grep -rn -i -P 'self[-\\s]?report' app/frontend` at cab0068 returns only `app/frontend/review.css:27` and `app/frontend/review.js:276`, both the internal class `rv-selfreport`. Those are allowed.\n- **Guard test (passes; scope too narrow).** `tests/unit/test_frontend_no_speaker_label.py` passes at cab0068 and on the live tree. It fails on a planted string in `app/frontend` (finding 3 below), but it only walks `app/frontend` (line 8).\n- **Backend user-facing text (fails).** See findings 1 and 2.\n- **Export and golden (pass, unchanged from r1).** The record 9 quote stays verbatim: \"Patient states symptoms began after the January collision.\"\n\n## Findings\n\n- **F1 blocker. The Why? text for a dropped qualifier names the speaker.** `app/backend/why.py:7` says \"The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out.\" It is user-facing: `app/frontend/timeline.js:119` renders `it.why` as `data-testid=\"why-text\"` in the Why? modal (opened by the button at `timeline.js:31`). Entry `why` is built from it at `app/backend/generator.py:108` and `app/backend/pipeline.py:66`. The reason fires when an edit or a summary drops the quote's qualifier (`app/backend/review.py:76`). D-040: \"No code or model labels who is speaking.\" This sentence tells the paralegal the quoted text is a patient statement. It is the same speaker label in another string. I did not render it in a browser. The default sample outputs do not carry it; it appears on the edit and live path.\n- **F2 blocker. The literal \"self-report\" is still in user-facing text, so the brief's own grep check fails.** `app/backend/narrative.py:19` says \"The sentence drops a hedge, self-report marker or negation that the cited quote has.\" It is rendered at `app/frontend/narrative.js:55` (`r.message || r.reason`), with the message set at `app/backend/narrative.py:118` (`r[\"message\"] = REASONS.get(...)`). The grep at cab0068 returns this line; the other backend hits are comments (`narrative.py:4`, `grounding.py:58`), which are not user-facing. R-FL-7 (`spec/REQUIREMENTS.md:71`) acceptance says \"No user-facing text contains 'self-report'\". At cab0068 the product fails that cell.\n- **F3 major. The guard test does not scan the backend, where F1 and F2 sit.** `tests/unit/test_frontend_no_speaker_label.py:8` sets `FRONTEND = ... / \"app\" / \"frontend\"`. Mutation check in a scratch copy: appending `PLANT_TEXT = \"Patient self-report\"` to `app/backend/why.py` gives `1 passed in 0.02s`, exit 0. The same string appended to `app/frontend/mock_flags.js` gives `1 failed`, `D-040 violation: mock_flags.js:58`, exit 1. A regression of the round-1 blocker in the backend would pass CI.\n- **F4 minor (carried from r1 F3). Golden flag K3 summary still carries the cut label.** `evals/golden/sample.expected.json:625`: `\"summary\": \"Causation rests on patient self-report, not a physician's causation opinion.\"` It is qa-owned and not user-facing text, but the expected output still says it.\n- **F5 minor (carried from r1 F2). The internal id is public API data.** `app/backend/present.py:74` returns `\"category\": row[\"category\"]` in every flag payload, and `app/frontend/flags.js:65` writes `\"data-category\": f.category`. Not rendered as text, so not a blocker, but \"never shown to users\" in the card overstates it.\n\n## Reproduction\n\n```\ngit archive cab0068 | tar -x -C <scratchpad>/t072\ncd <scratchpad>/t072 && .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_frontend_no_speaker_label.py   -> 1 passed, exit 0\n(plant in app/frontend/mock_flags.js, scratch copy)                                                                 -> 1 failed, exit 1\n(plant in app/backend/why.py, scratch copy)                                                                        -> 1 passed, exit 0\n.venv/bin/python -c 'import sys; sys.path.insert(0, \"app/backend\"); import why; print(why.why(\"SUMMARY_DROPS_QUALIFIER\"))'\n  -> The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out.\n```\n\n## Not run\n\nNo browser render of `?api=mock`. The \"Reported onset\" check is the served source text (`app/frontend/index.html:45` loads `mock_flags.js` on every page; `mock_flags.js:24`). The live tree was not used for the verdict.\n\n```json\n{\"card\": \"T-072\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"round 2; commit cab0068 (parent 312ed92) via git archive into the scratchpad (t072); live HEAD moved during review (b9d3ead, then 43fc69e) and was not the verdict basis; no browser run; sample case Appendix A records 1-9\",\n \"exercised\": [\n  \"read personas/claims-adjuster.md in full; reviews/T-072-claims-adjuster.md (r1); reviews/T-074-claims-adjuster.md; memory/ORCHESTRATOR_DECISIONS.md D-040 (line 48)\",\n  \"git log --oneline -5; git merge-base --is-ancestor cab0068 HEAD (ancestor); git show --stat cab0068; git show cab0068 -- app/\",\n  \"git archive cab0068 | tar -x -C <scratchpad>/t072\",\n  \"grep -rn -i -P 'self[-\\\\s]?report' app/ at cab0068 archive (backend hits: narrative.py:4, narrative.py:19, grounding.py:58; frontend hits: review.js:276, review.css:27 only)\",\n  \"grep -c -i 'self-report' app/frontend/dev/mock-data.js -> 0; sed -n 745,752p mock-data.js; grep -n 'f_pat_9' app/frontend/mock_flags.js -> line 24\",\n  \".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_frontend_no_speaker_label.py at cab0068 archive -> 1 passed, exit 0; same on live tree -> 1 passed, exit 0\",\n  \"plant 'Patient self-report' in scratch copy app/frontend/mock_flags.js -> 1 failed (D-040 violation: mock_flags.js:58), exit 1\",\n  \"plant 'Patient self-report' in scratch copy app/backend/why.py -> 1 passed, exit 0 (scope gap)\",\n  \"read app/backend/why.py:7; app/backend/narrative.py:19, :62, :118; app/frontend/narrative.js:55; app/frontend/timeline.js:31, :119; app/backend/review.py:76; app/backend/generator.py:108; app/backend/pipeline.py:66; app/frontend/flags.js:65, :68; app/backend/present.py:74; app/frontend/index.html:45\",\n  \".venv/bin/python -c 'import why; print(why.why(\\\"SUMMARY_DROPS_QUALIFIER\\\"))' in the archive app/backend -> prints the patient-statement sentence\",\n  \"grep -rln 'carries a qualifier|SUMMARY_DROPS_QUALIFIER' tests/fixtures evals/golden app/frontend -> only evals/golden/README.md (no fixture carries the why text)\",\n  \"not run: browser ?api=mock render; evals.run (writes evals/reports, outside write paths)\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"d040_user_facing_text_mock_overlays\": 5, \"d040_user_facing_text_backend_reason_strings\": 1, \"guard_test_scope_covers_backend\": 2, \"export_golden_fidelity\": 5, \"no_invented_facts_or_severity\": 5, \"tests_green_at_commit\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"Backend Why? text names the speaker ('a patient statement') in user-facing text (D-040)\",\n   \"evidence\": \"app/backend/why.py:7: \\\"SUMMARY_DROPS_QUALIFIER\\\": \\\"The quoted text carries a qualifier (a hedge, a patient statement, a negation, a side or an approximation) that the summary leaves out.\\\" Rendered: app/frontend/timeline.js:119 (data-testid why-text, Why? modal opened by timeline.js:31) from entry.why at app/backend/generator.py:108 and app/backend/pipeline.py:66. Triggered by app/backend/review.py:76 when an edit or summary drops the quote's qualifier. Not in any sample fixture (grep).\",\n   \"why_it_matters\": \"memory/ORCHESTRATOR_DECISIONS.md D-040: 'No code or model labels who is speaking.' The sentence tells the paralegal the quoted text is a patient statement. It is the cut speaker label in a different string, so the round-1 fix did not finish the decision. Blocker by the same rule as r1 F1.\",\n   \"fix\": \"Backend owner: rewrite why.py:7 without a speaker word, e.g. 'The quoted text carries a qualifier (a hedge, a negation, a side or an approximation) that the summary leaves out.' Keep the qualifier check (app/backend/grounding.py:186) unchanged; change only the text.\",\n   \"acceptance_test\": \"grep -rn -i -P 'patient statement|self[-\\\\s]?report' app/backend app/frontend returns no user-facing hits; a unit test asserts why.why('SUMMARY_DROPS_QUALIFIER') contains no 'patient' or 'self' word.\"},\n  {\"severity\": \"blocker\",\n   \"title\": \"Literal 'self-report' remains in user-facing reason text; the brief's grep check fails\",\n   \"evidence\": \"app/backend/narrative.py:19: \\\"SUMMARY_DROPS_QUALIFIER\\\": \\\"The sentence drops a hedge, self-report marker or negation that the cited quote has.\\\" Rendered at app/frontend/narrative.js:55 (r.message || r.reason); message set at app/backend/narrative.py:118 (r[\\\"message\\\"] = REASONS.get(r[\\\"reason\\\"], r[\\\"reason\\\"])). grep -rn -i -P 'self[-\\\\s]?report' app/ at cab0068 returns this line; the other backend hits are comments (narrative.py:4, grounding.py:58) and the allowed CSS class (review.js:276, review.css:27).\",\n   \"why_it_matters\": \"The round-2 brief allows only the internal CSS class to remain. R-FL-7 (spec/REQUIREMENTS.md:71) acceptance cell says 'No user-facing text contains self-report', so at cab0068 the product fails the spec row it is meant to satisfy.\",\n   \"fix\": \"Backend owner: change narrative.py:19 to 'The sentence drops a hedge, a marker or a negation that the cited quote has.' (no speaker word). Leave the comments alone; they are not user-facing.\",\n   \"acceptance_test\": \"grep -rn -i -P 'self[-\\\\s]?report' app/backend app/frontend returns only rv-selfreport (review.js:276, review.css:27) and comment lines; REASONS['SUMMARY_DROPS_QUALIFIER'] contains no 'self' word.\"},\n  {\"severity\": \"major\",\n   \"title\": \"The guard test scans app/frontend only, so the backend regression passes\",\n   \"evidence\": \"tests/unit/test_frontend_no_speaker_label.py:8: FRONTEND = Path(...) / \\\"app\\\" / \\\"frontend\\\"; :9 BAD = re.compile(r\\\"self[-\\\\s]?report\\\", re.I). Scratch mutation: 'PLANT_TEXT = \\\"Patient self-report\\\"' appended to app/backend/why.py -> '1 passed in 0.02s', exit 0. Same string in app/frontend/mock_flags.js -> '1 failed', 'D-040 violation: mock_flags.js:58', exit 1.\",\n   \"why_it_matters\": \"The round-1 blocker came back in app/backend (F1, F2) and nothing failed. A guard that only watches the place the last fix touched is not a guard for the rule.\",\n   \"fix\": \"QA owner (tests/**): scan app/backend and app/frontend with the same allowlist, and add the patient-speaker words (patient statement, patient self) to the pattern. Keep the rv-selfreport allowance.\",\n   \"acceptance_test\": \"In a scratch copy, pytest fails when 'Patient self-report' is planted in app/backend/why.py and when 'a patient statement' is planted in app/backend/narrative.py; passes on cab0068 after F1 and F2 are fixed.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Golden flag K3 summary still carries the cut label (carried from r1 F3)\",\n   \"evidence\": \"evals/golden/sample.expected.json:625 (at cab0068 and 312ed92): \\\"summary\\\": \\\"Causation rests on patient self-report, not a physician's causation opinion.\\\"\",\n   \"why_it_matters\": \"The golden JSON is the expected-output authority. It still states the speaker label D-040 cut. Not rendered, so minor.\",\n   \"fix\": \"QA owner (evals/**): replace the summary with a neutral line that quotes record 9 verbatim, e.g. 'Causation language: record 9 verbatim \\\"Patient states symptoms began after the January collision.\\\"'. Re-run the evals before merging.\",\n   \"acceptance_test\": \"grep -n -i 'self-report' evals/golden/sample.expected.json returns only the M10 must_not statement (line 990) or nothing; eval gates unchanged.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The internal id 'patient_report' is public API data (carried from r1 F2)\",\n   \"evidence\": \"app/backend/present.py:74: \\\"category\\\": row[\\\"category\\\"]; app/frontend/flags.js:65: \\\"data-category\\\": f.category. Text rendering uses f.title (flags.js:66).\",\n   \"why_it_matters\": \"Not text, so not a D-040 violation of user-facing wording. But 'never shown to users' in the card is inaccurate; an adjuster inspecting the payload sees the id.\",\n   \"fix\": \"Backend owner: either correct the card and decision log to 'not rendered as text; present in API JSON and data-category', or map to a neutral public id in present.py:74 and flags.js:65.\",\n   \"acceptance_test\": \"Option (a): card and decision note state the exposure. Option (b): GET a sample case's flags and assert no category or data-* value contains 'patient'.\"}\n ],\n \"whats_right\": [\n  \"The round-1 blocker lines are closed: app/frontend/mock_flags.js:24 and app/frontend/dev/mock-data.js:748-749 read 'Reported onset'; grep -c -i 'self-report' app/frontend/dev/mock-data.js is 0.\",\n  \"The frontend guard test passes at cab0068 and fails when 'Patient self-report' is planted in app/frontend (exit 1), with the allowlist limited to the rv-selfreport class.\",\n  \"The record 9 quote stays verbatim in the flag text (mock_flags.js:24, mock-data.js:749) with no added physician or speaker wording.\"\n ],\n \"questions_for_chris\": [\n  \"Is the Why? qualifier text (why.py:7) inside D-040's scope? I read D-040 as covering it. If you read D-040 as chip-only, F1 drops to major and the verdict to changes.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:58:39.756Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-072-claims-adjuster-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:58:54.861Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-074-claims-adjuster-r2.md",
 "content": "# T-074 round 2: claims-adjuster-reviewer (spec sync to D-040, commit 312ed92)\n\n**Verdict: pass** (no blocker, no major). The round-1 major is closed: R-FL-7 in `spec/REQUIREMENTS.md:71` now states D-040, and `test_eval_spec_check` passes. Four minors from round 1 are still open in other spec and golden files; they are listed below as carried.\n\nModel: claude-haiku-5-5 (the running model; the dossier's expected id does not match what is running).\nScope note: HEAD moved during the review (b9d3ead, then 43fc69e). I checked commit 312ed92 with `git show` and `git archive` into the scratchpad.\n\n## What I checked\n\n- **R-FL-7 closed (pass).** `spec/REQUIREMENTS.md:71` at 312ed92 reads \"**No speaker label (D-040, replaces the self-report label).** Excerpts are verbatim, so the text shows who spoke; no flag, entry or export line asserts the speaker. The sample record 9 onset flag is titled \"Reported onset\" and is never presented as a physician's opinion.\" Its acceptance cell is \"No user-facing text contains \"self-report\"; sample record 9 flag carries no `patient_report` source_kind. Golden `must_not` M10 passes.\" The title matches `app/backend/flag_templates.py:126`.\n- **Spec-check test (pass).** `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_spec_check.py` at the 312ed92 archive: 3 passed, exit 0.\n- **Lines 280 and 291 still match the golden (pass).** `diff` of `sed -n 280p spec/REQUIREMENTS.md` against `sed -n 58p evals/golden/sample.export.expected.txt`, and 291 against 69, both identical at 312ed92.\n- **Residue in spec, contracts, docs, golden (fails; carried minors).** See F1 to F3.\n- **Cross-reference, not a T-074 finding.** R-FL-7's own acceptance cell (\"No user-facing text contains self-report\") is false at cab0068 because of `app/backend/narrative.py:19`. That is the T-072 r2 blocker, not a spec defect.\n\n## Findings\n\n- **F1 minor (carried from r1 F2). The case truth sheet still labels the record 9 quote.** `spec/SAMPLE_CASE_TRUTHS.md:9`: \"(9 — patient self-report, not a physician's causation opinion)\". Not rendered; it is the reference the team grades against. Owner: writer or orchestrator.\n- **F2 minor (carried from r1 F3). Deviation row 4 is stale.** `spec/REQUIREMENTS.md:371` says the golden uses `source_kind: patient_self_report`. Its evidence command `grep -n \"patient_self_report\\|summary+excerpt\" evals/golden/README.md` returns nothing at 312ed92 (exit 1). A row that no longer reproduces misleads the next reviewer. Owner: orchestrator; close the row with a pointer to D-040.\n- **F3 minor (carried from r1 F4). Contract example, design brief and golden K3 still show the cut label.** `memory/contracts/api.md:185-186` (title \"Patient self-report\", explanation \"Patient self-report (not a physician's opinion) ...\"), which contradicts that file's own D-040 note at line 212. `docs/UI_DESIGN_BRIEF.md:132` still lists a \"Patient self-report\" chip row. `evals/golden/sample.expected.json:625` (K3 summary) still says \"Causation rests on patient self-report\". Owners: backend (api.md), orchestrator (design brief), qa (golden).\n\n## Reproduction\n\n```\ngit show 312ed92 --stat                                     -> spec/REQUIREMENTS.md, 1 insertion, 1 deletion\ngit show 312ed92:spec/REQUIREMENTS.md | grep -n 'No speaker label (D-040'   -> 71\ndiff <(git show 312ed92:spec/REQUIREMENTS.md | sed -n 280p) <(git show 312ed92:evals/golden/sample.export.expected.txt | sed -n 58p)  -> identical\ndiff <(git show 312ed92:spec/REQUIREMENTS.md | sed -n 291p) <(git show 312ed92:evals/golden/sample.export.expected.txt | sed -n 69p)  -> identical\ngit archive 312ed92 | tar -x -C <scratchpad>/t074 && cd <scratchpad>/t074 && .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_spec_check.py  -> 3 passed, exit 0\ngit grep -n -i 'self-report|patient_self_report' 312ed92 -- spec/ memory/contracts docs/ evals/golden -> residue at SAMPLE_CASE_TRUTHS.md:9, REQUIREMENTS.md:371, api.md:185-186, UI_DESIGN_BRIEF.md:132, sample.expected.json:625\n```\n\n## Not run\n\n`evals.run` (writes `evals/reports`, outside my write paths), so the golden M10 check named in R-FL-7's acceptance cell was not re-run. `docs/CONTRACT.md:617` also carries \"patient self-report\"; CLAUDE.md marks that file as never edited, so it is listed as a question, not a finding.\n\n```json\n{\"card\": \"T-074\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"round 2; commit 312ed92 (spec/REQUIREMENTS.md R-FL-7) checked with git show and git archive into the scratchpad (t074); live HEAD moved during review (b9d3ead, then 43fc69e) and was not the verdict basis; sample case Appendix A\",\n \"exercised\": [\n  \"read personas/claims-adjuster.md in full; reviews/T-074-claims-adjuster.md (r1); memory/ORCHESTRATOR_DECISIONS.md D-040 (line 48)\",\n  \"git show 312ed92 --stat; git show 312ed92 -- spec/REQUIREMENTS.md (1 insertion, 1 deletion, R-FL-7 only); git show 312ed92:spec/REQUIREMENTS.md | grep -n 'No speaker label (D-040' -> line 71\",\n  \"diff of 312ed92 spec line 280 vs golden sample.export.expected.txt line 58, and line 291 vs line 69 -> both identical\",\n  \"git archive 312ed92 | tar -x -C <scratchpad>/t074; .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_spec_check.py -> 3 passed, exit 0\",\n  \"git grep -n -i -E 'self-report|patient_self_report' 312ed92 -- spec/ memory/contracts docs/ evals/golden; git show 312ed92:spec/SAMPLE_CASE_TRUTHS.md (line 9); git show 312ed92:spec/REQUIREMENTS.md (line 371); git show 312ed92:memory/contracts/api.md (lines 185-186); git show 312ed92:docs/UI_DESIGN_BRIEF.md (line 132); git show 312ed92:evals/golden/sample.expected.json (line 625)\",\n  \"git show 312ed92:evals/golden/README.md | grep -n 'patient_self_report|summary+excerpt' -> no output, exit 1\",\n  \"read app/backend/flag_templates.py:126 (title 'Reported onset') to match R-FL-7 text\",\n  \"not run: evals.run (writes evals/reports, outside write paths); golden M10 not re-run\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"r_fl_7_states_d040\": 5, \"spec_lines_match_golden\": 5, \"spec_check_test_green\": 5, \"decision_residue_cleanup_spec_docs_golden\": 2},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Case truth sheet still labels the record 9 quote 'patient self-report' (carried from r1 F2)\",\n   \"evidence\": \"spec/SAMPLE_CASE_TRUTHS.md:9 at 312ed92: \\\"Patient states symptoms began after the January collision\\\" (9 — patient self-report, not a physician's causation opinion)\",\n   \"why_it_matters\": \"The truth sheet is the case reference the team grades against. It still records the speaker label D-040 cut. Not rendered anywhere.\",\n   \"fix\": \"Writer or orchestrator: replace the parenthetical with the verbatim marker, e.g. (9 — verbatim 'Patient states ...').\",\n   \"acceptance_test\": \"grep -n -i 'self-report' spec/SAMPLE_CASE_TRUTHS.md returns nothing.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Deviation row 4 is stale: its evidence command returns nothing (carried from r1 F3)\",\n   \"evidence\": \"spec/REQUIREMENTS.md:371 at 312ed92: | 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` ... | `grep -n \\\"patient_self_report\\\\|summary+excerpt\\\" evals/golden/README.md` | orchestrator (D-entry) |. The command returns no output at 312ed92 (exit 1).\",\n   \"why_it_matters\": \"A deviation row that no longer reproduces misleads the next reviewer about what is still open.\",\n   \"fix\": \"Orchestrator: close the row with a pointer to D-040, or update it to the current golden state.\",\n   \"acceptance_test\": \"The row's evidence command matches a current line, or the row is marked closed.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Contract example, design brief and golden K3 still show the cut label (carried from r1 F4)\",\n   \"evidence\": \"memory/contracts/api.md:185-186 at 312ed92 (title \\\"Patient self-report\\\"; explanation \\\"Patient self-report (not a physician's opinion) ...\\\"), while api.md's own D-040 note is at line 212. docs/UI_DESIGN_BRIEF.md:132: | `Patient self-report` | speech bubble | ... evals/golden/sample.expected.json:625: \\\"summary\\\": \\\"Causation rests on patient self-report, not a physician's causation opinion.\\\"\",\n   \"why_it_matters\": \"Builders following these documents would rebuild the cut chip and the cut speaker wording. api.md contradicts its own decision note.\",\n   \"fix\": \"Backend: update api.md:185-186 to the neutral title and explanation. Orchestrator: mark the design-brief row as cut under D-040. QA: replace the K3 summary with a neutral verbatim line.\",\n   \"acceptance_test\": \"grep -rn 'Patient self-report' memory/contracts docs/ evals/golden returns no hits outside decision history and the M10 must_not statement.\"}\n ],\n \"whats_right\": [\n  \"R-FL-7 at spec/REQUIREMENTS.md:71 now states the D-040 rule, names the neutral 'Reported onset' title that flag_templates.py:126 produces, and keeps the M10 must_not check.\",\n  \"Spec lines 280 and 291 are byte-identical to golden lines 58 and 69 at 312ed92, and test_eval_spec_check passes (3 passed).\",\n  \"The commit is one line in one file, so the spec change is reviewable on its own.\"\n ],\n \"questions_for_chris\": [\n  \"docs/CONTRACT.md:617 carries 'patient self-report' in the case truth copy, and CLAUDE.md says that file is never edited. Should the team record that copy as a known residue in SCOPE_CUTS, or is there a sanctioned way to correct it?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:58:55.045Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-074-claims-adjuster-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:58:58.535Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport json, re\nfor path in [\"reviews/T-072-claims-adjuster-r2.md\", \"reviews/T-074-claims-adjuster-r2.md\"]:\n    txt = open(path, encoding=\"utf-8\").read()\n    blocks = re.findall(r\"```json\\n(.*?)\\n```\", txt, re.S)\n    assert len(blocks) == 1, (path, len(blocks))\n    d = json.loads(blocks[0])\n    sev = [f[\"severity\"] for f in d[\"findings\"]]\n    rule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\n    print(path, \"| card\", d[\"card\"], \"| persona\", d[\"persona\"], \"| model\", d[\"model\"], \"| verdict\", d[\"verdict\"], \"| rule\", rule, \"| ok\" if rule == d[\"verdict\"] else \"| MISMATCH\", \"| sev\", sev, \"| whats_right\", len(d[\"whats_right\"]))\nEOF",
 "description": "Parse both review JSON blocks and check the verdict rule"
}
````

### User / tool · 2026-11-02T02:58:58.670Z

**tool result**
````
reviews/T-072-claims-adjuster-r2.md | card T-072 | persona claims-adjuster-reviewer | model claude-haiku-5-5 | verdict fail | rule fail | ok | sev ['blocker', 'blocker', 'major', 'minor', 'minor'] | whats_right 3
reviews/T-074-claims-adjuster-r2.md | card T-074 | persona claims-adjuster-reviewer | model claude-haiku-5-5 | verdict pass | rule pass | ok | sev ['minor', 'minor', 'minor'] | whats_right 3
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:59:04.279Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_d040_label_cut_residue.md",
 "old_string": "**How to apply:** when a card claims a label is gone, grep app/ (including app/frontend/mock*.js and dev/), spec/, evals/golden/*.json, memory/contracts/, docs/ for the label text, and check `api.py` static mounts to see whether dev/ pages are served. For \"not shown to users\", check the API payload (present.py) and DOM attributes, not only rendered text. Related: [[feedback_reviews_write_once]], [[project_research_attack_map_gaps]].",
 "new_string": "**How to apply:** when a card claims a label is gone, grep app/ (including app/frontend/mock*.js and dev/), spec/, evals/golden/*.json, memory/contracts/, docs/ for the label text, and check `api.py` static mounts to see whether dev/ pages are served. For \"not shown to users\", check the API payload (present.py) and DOM attributes, not only rendered text. Related: [[feedback_reviews_write_once]], [[project_research_attack_map_gaps]].\n\n**Round 2 (cab0068 mocks, 312ed92 spec; reviews/T-072-claims-adjuster-r2.md fail, T-074-claims-adjuster-r2.md pass):**\n- Mock overlays closed (mock_flags.js:24, mock-data.js:748-749 now \"Reported onset\"). R-FL-7 rewritten correctly.\n- Not closed: the speaker wording moved to backend reason strings the frontend-only guard test does not scan. why.py:7 \"a patient statement\" (rendered timeline.js:119 Why? modal); narrative.py:19 literal \"self-report marker\" (narrative.js:55). Planting \"Patient self-report\" in app/backend/why.py passed the test; in app/frontend it failed.\n- Still open residue: spec/SAMPLE_CASE_TRUTHS.md:9, REQUIREMENTS.md:371 (stale), api.md:185-186, UI_DESIGN_BRIEF.md:132, golden K3 line 625, docs/CONTRACT.md:617 (never edited per CLAUDE.md).\n\n**Lesson:** a cut label is a speaker label wherever it appears in user-facing text, including reason/\"Why?\" strings that name the speaker as a category (\"a patient statement\"). Grep backend reason tables (why.py, narrative.py REASONS), not only flag templates. A guard test must scan every layer the rule covers (app/, not only app/frontend). Round-2 checks: archive the commit, plant the string in a scratch copy, and confirm the test fails."
}
````

### User / tool · 2026-11-02T02:59:04.380Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_d040_label_cut_residue.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:59:06.724Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md",
 "old_string": "- [D-040 label-cut residue](project_d040_label_cut_residue.md) — T-072/T-074: cut label survives in ?api=mock overlay, dev harness, R-FL-7, golden JSON, contracts; \"not rendered\" != \"never shown\"",
 "new_string": "- [D-040 label-cut residue](project_d040_label_cut_residue.md) — T-072/T-074 r1+r2: mocks fixed, but backend Why? strings (why.py:7, narrative.py:19) name the speaker and the guard test is frontend-only; spec residue open"
}
````

### User / tool · 2026-11-02T02:59:06.917Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:59:09.289Z

Round 2 is done: T-072 fails, T-074 passes. Both files are written with valid JSON blocks, and the verdicts match the rule.
- **T-072 (fail, 2 blockers):** the mock overlays are fixed and the frontend test passes. The backend still names the speaker in user-facing "Why?" text (`app/backend/why.py:7` "a patient statement"; `app/backend/narrative.py:19` literal "self-report marker"), and the guard test only scans `app/frontend`, so a planted backend string passes. Review: `/Users/arsis/zlayt-pm-project/reviews/T-072-claims-adjuster-r2.md`
- **T-074 (pass):** `spec/REQUIREMENTS.md:71` now states D-040 and `test_eval_spec_check` passes (3 passed). Four round-1 minors are still open (truth sheet, stale row 371, api.md/design brief, golden K3). Review: `/Users/arsis/zlayt-pm-project/reviews/T-074-claims-adjuster-r2.md`
