# Subagent: T-061 r2 check (haiku) (T-061 r2 check (haiku))

Source: `agent-ac12812494daf68ce.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:20:52.973Z

Working directory: /Users/arsis/zlayt-pm-project. Round 2 of T-061 vs reviews/T-061-claims-adjuster.md (blocker: AC2 flags.py; majors: test_flags_pass red; exclude_sentence drops patient-subject sentences naming family/EMS). D-033 is binding. Run `.venv/bin/python research/lexicon_selfcheck.py | tail -3` and `.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon" 2>&1 | tail -2`. Script-check: "Patient states pain began after the collision." → patient_report; "Patient states his wife drove him to the ER." → patient_report; "Wife reports he has been irritable.", "Per EMS, pt ambulatory at scene.", "S: neck pain", "Witness states the car ran the light." → not patient_report (through the production flags code). Write reviews/T-061-claims-adjuster-r2.md (new file; D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:54.971Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/claims-adjuster.md"
}
````

### User / tool · 2026-11-02T02:20:54.981Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:55.431Z

**tool call — Bash**
````
{
 "command": "ls -la /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/ && cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md",
 "description": "List reviewer memory dir and read its index"
}
````

### User / tool · 2026-11-02T02:20:55.522Z

**tool result**
````
total 56
drwxr-xr-x@  9 arsis  staff   288 Nov  1 20:18 .
drwxr-xr-x@ 16 arsis  staff   512 Nov  1 19:47 ..
-rw-r--r--@  1 arsis  staff  1071 Nov  1 20:18 MEMORY.md
-rw-r--r--@  1 arsis  staff  1890 Nov  1 20:18 feedback_lexicon_review_method.md
-rw-r--r--@  1 arsis  staff  1492 Nov  1 20:11 feedback_review_commit_not_worktree.md
-rw-r--r--@  1 arsis  staff  1478 Nov  1 19:59 project_flag_pass_review_patterns.md
-rw-r--r--@  1 arsis  staff  3468 Nov  1 20:18 project_flag_source_kind_and_run_signal.md
-rw-r--r--@  1 arsis  staff  2882 Nov  1 20:00 project_research_attack_map_gaps.md
-rw-r--r--@  1 arsis  staff  1575 Nov  1 20:14 project_t036_r4_split_and_judge_fixtures.md
- [Lexicon review method](feedback_lexicon_review_method.md) — selfcheck PASS hides recall gaps; rerun probe script; must-probe constructions
- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 r1-r4: omissions, invented Rivera facts, partial scope fixes (line 34 left open at r4); sweep prose + golden must-not regex
- [Flag-pass review patterns](project_flag_pass_review_patterns.md) — T-036 r0: vacuous guard test, silent-empty conflict pass, worker skipped full suite
- [source_kind history and run signal](project_flag_source_kind_and_run_signal.md) — T-036 r2/r3 word filter; T-061 r0 (dd545e3) lexicon narrowed but AC2 flags/grounding wiring not done, exclude regex over-broad
- [Review the commit, not the dirty tree](feedback_review_commit_not_worktree.md) — git archive the sha when working tree has uncommitted edits to reviewed files
- [T-036 r4 split and judge fixtures](project_t036_r4_split_and_judge_fixtures.md) — self-report split to T-061; committed judge fixtures don't replay (JUDGE_UNAVAILABLE); r4 verdict changes
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:55.612Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster.md"
}
````

### User / tool · 2026-11-02T02:20:55.619Z

**tool result**
````
1	# T-061 Self-report label precision: claims-adjuster review (Gary Pruitt), round 0
2	
3	Verdict: **fail** (1 blocker, 2 major, 1 minor).
4	
5	What the commit does: dd545e3 narrows the lexicon `self_report` entries to explicit patient attribution, adds a `self_report_scope.exclude_sentence` regex (lexicon.yaml:88-93), marks `intake_form_accident_date` `self_report: false`, and adds 26 held-out probes. The lexicon side holds up. The product side does not: no file under `app/backend/` changed in dd545e3, so AC2 (flags.py/grounding.py label only from those entries, with tests) is not done, and the production label still attributes EMS, witness, wife and family complaints to the patient.
6	
7	Checks against the card and D-033:
8	
9	- AC1 (lexicon): the selfcheck passes and the scope-aware lexicon gets the brief's five sentences right. Two over-exclusion cases remain (finding 2).
10	- AC2 (flags.py/grounding.py + tests): **not done.** `git show --stat dd545e3` lists only `app/llm/lexicon.yaml`, `evals/lexicon_heldout.jsonl` and `research/lexicon_selfcheck.py`. Production still calls `grounding.has_self_report` (flags.py:46 and flags.py:125), which still uses the old `_SELF` complain verb (grounding.py:167) and the `_PATIENT_WORDS` word filter (grounding.py:177). `exclude_sentence` is referenced nowhere in `app/` or `tests/`.
11	- AC3 (spec note or D-entry): D-033 exists (ORCHESTRATOR_DECISIONS.md:41), which meets the "or" clause. DECISIONS.md:286 and lexicon.yaml:25-26 still state the superseded rule (finding 3).
12	- Brief sentences: "Patient states pain began after the collision." is patient_report in the lexicon and in production. "Wife reports he has been irritable.", "Per EMS, pt ambulatory at scene.", "S: neck pain" and "Witness states the car ran the light." are record in both. No sentence I fed was invented or altered.
13	
14	Why finding 1 is a blocker when T-036 r3 rated the same behaviour major: D-033 now names this case as a credibility error ("Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit"). At r3 there was no such decision. The production code contradicts a recorded decision, so it is a spec violation.
15	
16	Findings:
17	
18	1. **Blocker.** AC2 not done: production still labels EMS, witness, wife and family complaints as "Patient self-report". Evidence: `artifacts/review-evidence/T-061-probe.txt`, rows "EMS complains of neck pain 7/10.", "Witness complains of neck pain.", "Wife complains of neck pain.", "Family complains of neck pain." each show `production has_self_report: patient_report` and `lexicon(scope-aware): record`. Cause: grounding.py:167 `\bcomplain(?:s|ed|ing|t)?\b` in `_SELF`, and grounding.py:177 `complain\w*` in `_PATIENT_WORDS`. flags.py:46 and flags.py:125 use the result as `source_kind`. `git show --stat dd545e3` has no app/backend entry. Card AC2 is `done: false`.
19	   Why it matters: the chip "Patient self-report" tells the reader the claimant said it. A family member's or EMS's statement carries the claimant's name on it, and I would use that to discount the package.
20	   Fix: in grounding.has_self_report, replace `_SELF` and `_PATIENT_WORDS` with "any lexicon self_report hit AND NOT self_report_scope.exclude_sentence" (read from lexicon.yaml, as research/lexicon_selfcheck.py:is_patient_statement does). Set the intake date through `self_report: false` and delete `_NOT_PATIENT_STATEMENT` (grounding.py:175). Fix finding 2 in the same change.
21	   Acceptance test: has_self_report is False for "EMS complains of neck pain 7/10.", "Witness complains of neck pain.", "Wife complains of neck pain.", "Family complains of neck pain.", "EMS reports neck pain 7/10.", "Wife reports he was in pain.", "Date of accident per intake form: 2026-01-19."; True for "Patient states pain began after the collision.", "Patient complains of neck pain.", "C/O neck pain 7/10 and headache.", "Patient-reported neck pain 7/10."; and `grep -n "_SELF\|_PATIENT_WORDS\|_NOT_PATIENT_STATEMENT" app/backend/grounding.py` returns nothing.
22	
23	2. **Major.** The commit leaves `tests/unit/test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution` red, a regression from the parent. Evidence: `.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon" 2>&1 | tail -2` on the live tree (equal to dd545e3 for these paths) gives `1 failed, 113 passed, 699 deselected`. On the git archive of parent 099732b the same command gives `114 passed, 697 deselected`. The full suite diff (`artifacts/review-evidence/T-061-base-failed.txt` vs `T-061-head-failed.txt`) adds exactly this test. The failing assertion is the yes-list entry "Subjective: neck pain 7/10.", which the lexicon no longer matches (lexicon.yaml:754-759, pattern now without `^\s*(?:subjective|S)\s*:`). The test is the r2 contract, which D-033 supersedes for bare S:/Subjective: headers. The card's evidence line ("selfcheck PASS ... golden MUST 11/11") does not mention a pytest run, so the red test was not reported.
24	   Why it matters: a red flag test on the commit means the worker did not run the suite it touched, and the stale test would hide a regression in the next round.
25	   Fix: update the test to D-033 (Subjective: and S: are record; a bare header is not an attribution) and add the AC2 tests from finding 1 to tests/unit/test_flags_pass.py.
26	   Acceptance test: `.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon"` reports 0 failed, and the full `tests/unit` run shows no FAILED line that is not also in the parent archive.
27	
28	3. **Major.** `exclude_sentence` drops explicit patient statements whenever a family or EMS word and a speech verb share the sentence. Evidence: `artifacts/review-evidence/T-061-probe.txt`, "Patient states EMS noted a laceration." and "Patient reports his wife said he was fine." both give lexicon `record` (`LEX` mismatch) while the patient is the speaker. Cause: lexicon.yaml:89 matches `\b(?:EMS|...|wife|...)\b(?:\s+[\w'-]+){0,3}?\s+(?:...|noted|said|...)\b` anywhere in the sentence, not only at the grammatical subject. Held-out coverage gap: none of the 26 new probes pairs a patient subject with a family or EMS word (grep of evals/lexicon_heldout.jsonl), so selfcheck PASS cannot show it.
29	   Why it matters: a patient-attributed statement loses its "Patient self-report" attribution (D-033: "patient-quoted speech" stays patient_report). This is latent today because production does not read exclude_sentence yet. Finding 1's fix would make it live.
30	   Fix: anchor the exclusion to the sentence subject (sentence-initial "EMS/Wife/Witness/Family ... <verb>", or a "Per <non-patient>" clause), and exclude any sentence that starts with or names "Patient"/"Pt"/"C/O". Add both sentences to self_report_scope.examples.keep and to evals/lexicon_heldout.jsonl.
31	   Acceptance test: "Patient states EMS noted a laceration.", "Patient reports his wife said he was fine." are patient_report; "EMS reports minimal damage.", "Wife complains of neck pain.", "Per his wife, headaches began at the scene." stay record; `research/lexicon_selfcheck.py` still PASS.
32	
33	4. **Minor.** The spec still states the superseded rule. DECISIONS.md:286 still says "`source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt". lexicon.yaml:25-26 still says "code sets source_kind = "patient_report" from it (ADR-013)" (the header was edited only on line 25). D-033 says it "Narrows ADR-013 / DECISIONS.md:286", so AC3's "or" clause is met, but the spec text now contradicts the code's exclusion rule.
34	   Fix: architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to "self_report entries that name the patient, minus self_report_scope.exclude_sentence". The card's AC3 `done` flag can then be set true.
35	   Acceptance test: `grep -n "set by code from the lexicon" memory/DECISIONS.md` shows the amended text and no line still reads "from the lexicon `self_report` entries on the excerpt".
36	
37	Things I did not treat as findings, for Chris:
38	- D-033 labels a bare "S:" or "Subjective:" header as record. In a SOAP note that header is the clinician's marker for the patient's report. The verbatim marker stays in the excerpt, so nothing is invented. I accept D-033 as the decision, and I note the adjuster would give subjective-only weight to these lines.
39	
40	Exercised (live tree; `git diff --stat HEAD -- app/backend app/llm/lexicon.yaml research evals tests/unit` shows only evals/reports/latest.json, outside my scope, so live == dd545e3 for reviewed paths):
41	- Read personas/claims-adjuster.md in full; `python3 tools/board.py show T-061`; `grep -n "D-033" -A 15 memory/ORCHESTRATOR_DECISIONS.md`; reviews/T-036-claims-adjuster-r3.md; my memory dir.
42	- `git log --oneline -5`; `git show --stat dd545e3`; `git show dd545e3 -- app/llm/lexicon.yaml research/lexicon_selfcheck.py` (diff read in full).
43	- `.venv/bin/python research/lexicon_selfcheck.py` -> `RESULT: PASS`, golden MUST 11/11, held-out 115/115, adjuster probes 62/63 (the one FN, "No acute findings." low only, is pre-existing), EXIT=0.
44	- `.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon" 2>&1 | tail -2` -> `1 failed, 113 passed, 699 deselected`; full failure text read (`pytest ... -k lexicon_self_report` -> 1 failed, assertion at tests/unit/test_flags_pass.py:121).
45	- Same subset on `git archive 099732b` (parent) -> `114 passed, 697 deselected`.
46	- Full `tests/unit` on live tree -> `2 failed, 811 passed` (flags test plus test_t037_backend.py::test_replay_has_no_fixture_miss[case_09_nonvisit_hides_gap]); on archives: parent `3 failed, 808 passed`, dd545e3 `4 failed, 807 passed`; the failing-test lists differ only by the flags test. The three test_t037 replay failures exist at parent and are not attributable to dd545e3; the live tree and archives disagree on case_09, which I did not triage.
47	- `artifacts/review-evidence/T-061-probe.py /Users/arsis/zlayt-pm-project` -> `artifacts/review-evidence/T-061-probe.txt`: 27 sentences (the five brief sentences, the researcher's test list, EMS/witness/wife/family complaints, S:/Subjective:/Self-reported headers, two over-exclusion candidates) through the lexicon (scope-aware) and `grounding.has_self_report`.
48	- `grep -n "has_self_report\|self_report_scope\|exclude_sentence" app/backend/flags.py app/backend/grounding.py` -> flags.py:46, flags.py:125, grounding.py:219 only; `grep -rn "exclude_sentence\|self_report_scope" app/ tests/` -> lexicon.yaml only.
49	- `grep -n "^_SELF\|^_NOT_PATIENT_STATEMENT\|^_PATIENT_WORDS" app/backend/grounding.py` -> 167, 175, 177.
50	- `grep` of evals/lexicon_heldout.jsonl for patient subjects with family/EMS words -> none (coverage gap, finding 3).
51	- `git archive` extractions were deleted after use; the failing-test lists are kept as artifacts.
52	
53	Outside my lens: the test-runner setup and the t037 replay failures (not triaged); the commit message's co-author line.
54	
55	```json
56	{"card": "T-061", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
57	 "scope": "commit dd545e3 (HEAD; parent 099732b) on the live tree (equal to dd545e3 for app/backend, app/llm/lexicon.yaml, research, evals, tests/unit); spec memory/DECISIONS.md:286; decision memory/ORCHESTRATOR_DECISIONS.md D-033; no app URL (lexicon and flag-layer change, no UI in scope); sample probes as listed.",
58	 "exercised": [
59	  "Read personas/claims-adjuster.md in full; python3 tools/board.py show T-061; D-033 (ORCHESTRATOR_DECISIONS.md:41); reviews/T-036-claims-adjuster-r3.md; my memory dir",
60	  "git log --oneline -5; git show --stat dd545e3 (lexicon.yaml, lexicon_heldout.jsonl, lexicon_selfcheck.py only; no app/backend)",
61	  "git show dd545e3 -- app/llm/lexicon.yaml research/lexicon_selfcheck.py (full diff read)",
62	  "git diff --stat HEAD -- app/backend app/llm/lexicon.yaml research evals tests/unit (only evals/reports/latest.json, out of scope)",
63	  ".venv/bin/python research/lexicon_selfcheck.py -> RESULT: PASS; golden MUST 11/11; held-out 115/115; EXIT=0",
64	  ".venv/bin/python -m pytest tests/unit -q -k 'flag or lexicon' 2>&1 | tail -2 -> 1 failed, 113 passed, 699 deselected",
65	  "same subset on git archive 099732b (parent) -> 114 passed, 697 deselected",
66	  "full tests/unit: live 2 failed/811 passed; parent archive 3 failed/808 passed; dd545e3 archive 4 failed/807 passed; FAILED-list diff = test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution only (artifacts/review-evidence/T-061-base-failed.txt, T-061-head-failed.txt)",
67	  "artifacts/review-evidence/T-061-probe.py <repo> -> artifacts/review-evidence/T-061-probe.txt (27 sentences through lexicon scope-aware and grounding.has_self_report)",
68	  "grep -n has_self_report|self_report_scope|exclude_sentence app/backend/flags.py app/backend/grounding.py -> flags.py:46, 125; grounding.py:219; grep -rn exclude_sentence app/ tests/ -> lexicon.yaml only",
69	  "grep -n ^_SELF|^_NOT_PATIENT_STATEMENT|^_PATIENT_WORDS app/backend/grounding.py -> 167, 175, 177",
70	  "grep evals/lexicon_heldout.jsonl for patient-subject sentences containing EMS/wife/witness/family -> none",
71	  "sed -n 284,288p memory/DECISIONS.md (line 286 text); grep self_report_scope / lexicon header lines 13, 25-26"
72	 ],
73	 "verdict": "fail",
74	 "scores": {"attribution_precision_production": 1, "lexicon_scope_logic": 3, "ac2_flags_wiring": 1, "test_honesty": 2, "spec_consistency": 3, "no_invented_or_altered_text": 5},
75	 "findings": [
76	  {"severity": "blocker",
77	   "title": "AC2 not done: production still labels EMS, witness, wife and family complaints as Patient self-report",
78	   "evidence": "artifacts/review-evidence/T-061-probe.txt rows 'EMS complains of neck pain 7/10.', 'Witness complains of neck pain.', 'Wife complains of neck pain.', 'Family complains of neck pain.': production has_self_report=patient_report, lexicon(scope-aware)=record. Cause: app/backend/grounding.py:167 (_SELF, complain verb) and grounding.py:177 (_PATIENT_WORDS, complain\\w*); flags.py:46 and flags.py:125 use the result as source_kind. git show --stat dd545e3 touches no app/backend file. Card AC2 done=false.",
79	   "why_it_matters": "D-033 (ORCHESTRATOR_DECISIONS.md:41) says EMS, witness and spouse/family statements are not patient self-report and calls the mislabel a credibility error. Production contradicts that recorded decision on four live phrasings, and the chip tells the reader the claimant said it. T-036 r3 rated the same behaviour major; D-033 now makes it a spec violation, so it is a blocker.",
80	   "fix": "In grounding.has_self_report: replace _SELF and _PATIENT_WORDS with 'any lexicon self_report hit AND NOT self_report_scope.exclude_sentence' (read from lexicon.yaml, as research/lexicon_selfcheck.py:is_patient_statement does). Mark the intake date self_report false (done in lexicon) and delete _NOT_PATIENT_STATEMENT (grounding.py:175). Fix finding 3 in the same change.",
81	   "acceptance_test": "has_self_report False for 'EMS complains of neck pain 7/10.', 'Witness complains of neck pain.', 'Wife complains of neck pain.', 'Family complains of neck pain.', 'EMS reports neck pain 7/10.', 'Wife reports he was in pain.', 'Date of accident per intake form: 2026-01-19.'; True for 'Patient states pain began after the collision.', 'Patient complains of neck pain.', 'C/O neck pain 7/10 and headache.', 'Patient-reported neck pain 7/10.'; grep -n '_SELF\\|_PATIENT_WORDS\\|_NOT_PATIENT_STATEMENT' app/backend/grounding.py returns nothing."},
82	  {"severity": "major",
83	   "title": "Commit leaves test_flags_pass.py red (regression from parent): stale r2 assertion on 'Subjective:' header",
84	   "evidence": "'.venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\" 2>&1 | tail -2' -> '1 failed, 113 passed, 699 deselected' (live, equal to dd545e3). Same subset on git archive 099732b -> '114 passed, 697 deselected'. Failing test tests/unit/test_flags_pass.py:114-121, assertion at :121, yes-list entry 'Subjective: neck pain 7/10.' (probe row: record). Full-suite FAILED-list diff against parent: only this test (artifacts/review-evidence/T-061-base-failed.txt vs T-061-head-failed.txt). Card evidence line does not mention a pytest run.",
85	   "why_it_matters": "The lexicon change flipped a tested behaviour and the test was not updated, so the commit is red on the flag suite it touches. The stale assertion would hide the next regression. The card's evidence cites only selfcheck and golden runs.",
86	   "fix": "Update the yes/no lists in test_flags_pass.py to D-033 (bare Subjective:/S: header is record; Patient-reported stays patient) and add the AC2 tests from finding 1 in the same file. Report the pytest subset result in the card evidence.",
87	   "acceptance_test": "'.venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\"' reports 0 failed; the full tests/unit FAILED list contains no test that is absent from the parent archive."},
88	  {"severity": "major",
89	   "title": "exclude_sentence drops explicit patient statements when a family or EMS word and a speech verb share the sentence",
90	   "evidence": "artifacts/review-evidence/T-061-probe.txt: 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' -> lexicon(scope-aware)=record (expect patient). Cause: app/llm/lexicon.yaml:89 exclude_sentence matches a non-patient name, up to 3 words, then a speech verb anywhere in the sentence (not at the grammatical subject). evals/lexicon_heldout.jsonl: no probe pairs a patient subject with a family/EMS word (grep).",
91	   "why_it_matters": "D-033 keeps patient-quoted speech as patient_report. The exclusion removes the patient's own attribution on a sentence the patient authored. It is latent today because production does not read exclude_sentence, and it becomes live when AC2 is fixed as finding 1 requires. Selfcheck PASS cannot show it because the held-out set has no such case.",
92	   "fix": "Anchor the exclusion to the sentence subject (sentence-initial 'EMS|Wife|Witness|Family ... <verb>' or a 'Per <non-patient>' clause) and never exclude a sentence that starts with or names Patient/Pt/C/O. Add both sentences to self_report_scope.examples.keep and to evals/lexicon_heldout.jsonl.",
93	   "acceptance_test": "'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' are patient_report; 'EMS reports minimal damage.', 'Wife complains of neck pain.', 'Per his wife, headaches began at the scene.' stay record; .venv/bin/python research/lexicon_selfcheck.py still PASS."},
94	  {"severity": "minor",
95	   "title": "Spec text still states the superseded rule (DECISIONS.md:286, lexicon.yaml:25-26)",
96	   "evidence": "memory/DECISIONS.md:286: '`source_kind = \"patient_report\"` is set by code from the lexicon `self_report` entries on the excerpt'. app/llm/lexicon.yaml:25-26: 'code sets source_kind = \"patient_report\" from it (ADR-013)'. D-033 (ORCHESTRATOR_DECISIONS.md:41) says it 'Narrows ADR-013 / DECISIONS.md:286'.",
97	   "why_it_matters": "AC3's 'or' clause is met by D-033, but the contract text now omits the exclusion rule that the code applies. A future reader gets two rules.",
98	   "fix": "Architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to 'self_report entries that name the patient, minus self_report_scope.exclude_sentence'. Then set card AC3 done.",
99	   "acceptance_test": "grep -n 'set by code from the lexicon' memory/DECISIONS.md shows the amended text; the header in lexicon.yaml:25-26 names self_report_scope."}
100	 ],
101	 "whats_right": [
102	  "Lexicon scope works on the brief's non-patient sentences: 'Wife reports he has been irritable.', 'Per EMS, pt ambulatory at scene.', 'Witness states the car ran the light.' and 'S: neck pain' are record, and 'Patient states pain began after the collision.' is patient_report in both lexicon and production.",
103	  "Intake date is self_report: false (lexicon.yaml:775) and production gives record for 'Date of accident per intake form: 2026-01-19.'; no excerpt text is altered in any probe.",
104	  "Selfcheck, held-out 115/115 and golden MUST 11/11 all pass on the commit."
105	 ],
106	 "questions_for_chris": [
107	  "D-033 makes a bare 'S:' or 'Subjective:' header record, not patient self-report. In a SOAP note that header marks the patient's report. I accept D-033, but confirm you want the chip off those lines, since the subjective-only weight they carry is what a defense adjuster would use.",
108	  "Is 'Patient-reported' an explicit patient attribution for D-033? I counted it as patient_report (production and lexicon agree); D-033 does not name it.",
109	  "The persona file expects model claude-opus-5-5 in the review record; I ran as claude-haiku-5-5 and wrote that id. Confirm that is acceptable for the gate."
110	 ]}
111	```
112	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:57.747Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python research/lexicon_selfcheck.py | tail -3; echo \"EXIT=$?\"",
 "description": "Run lexicon selfcheck and show last 3 lines"
}
````

### User / tool · 2026-11-02T02:20:57.983Z

**tool result**
````
SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 1 of 140; held-out 115/115
RESULT: PASS
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:58.283Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\" 2>&1 | tail -2",
 "description": "Run flag and lexicon unit tests, show summary"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:58.928Z

**tool call — Bash**
````
{
 "command": "git log --oneline -6 && echo \"---STATUS---\" && git status --short | head -40 && echo \"---SHOW---\" && git show --stat HEAD | head -30",
 "description": "Show recent git log, working tree status, and HEAD stat"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:20:59.440Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-033\" -A 15 memory/ORCHESTRATOR_DECISIONS.md | head -40; echo \"---BOARD---\"; python3 tools/board.py show T-061 2>&1 | head -80",
 "description": "Read D-033 decision and T-061 card"
}
````

### User / tool · 2026-11-02T02:21:00.503Z

**tool result**
````
................................................                         [100%]
120 passed, 731 deselected in 1.79s
````

### User / tool · 2026-11-02T02:21:00.646Z

**tool result**
````
4eebb2d feat(frontend): export view, change-quote editor, D-029 demo label (T-044 wip)
e1400d4 feat(backend): patient_report only from explicit patient attribution, scoped exclusion (T-061, D-033)
a79358c feat(frontend): batch accept for verified entries, audit drawer, exhibit/Bates settings (T-055, T-058)
c61e84f fix(db): bump schema version to 3, real v2 rebuild test (T-062 r2)
d548ccd feat(backend): manual entry for a rejected record and 'not a duplicate' split (T-056, D-031)
c143c4b docs(research): UI reference study and UI design brief draft (T-060 pass 1)
---STATUS---
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/feedback_lexicon_recall_and_negation.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md
 M .claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md
 M .claude/agent-memory/product-manager-reviewer/project_t013_review_history.md
 M .claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_hook_guard_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/hooks/reviewer_write_guard.py
 M app/backend/api.py
 M app/backend/export.py
 M app/backend/schemas.py
 M app/backend/store.py
 M app/llm/provider.py
 M app/llm/record.py
 M board/activity.jsonl
 M board/cards/T-040.md
 M board/cards/T-043.md
 M board/cards/T-044.md
 M board/cards/T-050.md
 M board/cards/T-052.md
 M board/cards/T-053.md
 M board/cards/T-054.md
 M board/cards/T-055.md
 M board/cards/T-056.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-060.md
 M board/cards/T-061.md
---SHOW---
commit 4eebb2d8dfd3fae1eae87d97a1a9aa0442e20d86
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:20:41 2026 -0600

    feat(frontend): export view, change-quote editor, D-029 demo label (T-044 wip)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/frontend/app.js      |  2 +-
 app/frontend/excerpt.js  | 37 ++++++++++++++++++++++++++++++++
 app/frontend/export.js   | 55 ++++++++++++++++++++++++++++++++++++++++++++++++
 app/frontend/styles.css  |  7 ++++++
 app/frontend/timeline.js |  1 +
 5 files changed, 101 insertions(+), 1 deletion(-)
````

### User / tool · 2026-11-02T02:21:00.783Z

**tool result**
````
41:| D-033 | `patient_report` (self-report chip) applies only to explicit patient attribution ('Patient states/reports/notes', 'Pt c/o', patient-quoted speech). EMS narrative, witness, spouse/family statements and generic 'S:'/'Subjective:' headers are not patient self-report (separate or no attribution). Narrows ADR-013 / DECISIONS.md:286. | Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit. | T-036 r3 → T-061 |
---BOARD---
---
id: "T-061"
title: "Self-report label precision: only the patient's own statements (split from T-036 per §7.4)"
milestone: "M2"
role: "researcher"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:12:03Z"
updated_at: "2026-11-02T02:20:49Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:19:23Z"
rounds: 1
commits: ["dd545e3", "e1400d4"]
reviews:
  - {"persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-061-claims-adjuster.md", "at": "2026-11-02T02:19:00Z"}
ac:
  - {"n": 1, "text": "lexicon self_report entries only match explicit patient attribution; EMS/witness/spouse/family phrasings have a separate non-patient attribution or none (held-out probes)", "done": true, "evidence": "selfcheck PASS: 26 new probes (explicit_patient 8/8, non_patient_speaker 12/12, headers_not_attribution 5/5 + 2 reclassified) in evals/lexicon_heldout.jsonl; self_report_scope.exclude_sentence added; intake entry self_report false; golden MUST 11/11"}
  - {"n": 2, "text": "flags.py labels patient_report only from those entries; tests cover EMS, wife, witness, 'S:' header", "done": true, "evidence": "grounding._self_report = any lexicon self_report hit minus self_report_scope.exclude_sentence (sentence-subject anchored); tests/unit/test_flags_pass.py d033 tests: EMS, wife, witness, family, S:/Subjective:, Self-reported -> record; Patient states/c/o -> patient_report; patient subject mentioning EMS/wife stays patient. unit suite 835 passed; make_curated --check equal; lexicon_selfcheck PASS (held-out 115/115, MUST 11/11)"}
  - {"n": 3, "text": "memory/DECISIONS.md:286 amended (architect note) or ORCHESTRATOR_DECISIONS entry records the narrowing", "done": true, "evidence": "memory/ORCHESTRATOR_DECISIONS.md D-033 records the narrowing of ADR-013 / DECISIONS.md:286"}
---
## Description
From reviews/T-036-claims-adjuster-r3.md. Lexicon self_report entries + flags labelling: 'S:'/'Self-reported' headers, EMS/witness/spouse/family statements must not be labelled 'Patient self-report'. Researcher amends lexicon; backend-1 adjusts flags.py; ADR-013 note via architect card note.

## Notes (append-only, newest last)
- 2026-11-02T02:12:06Z orchestrator: assigned: researcher-c
- 2026-11-02T02:13:03Z researcher: claimed
- 2026-11-02T02:14:13Z researcher: Lexicon narrowed (commit pending). For backend-1 (flags.py/grounding.py): (1) self_report entries are now only self_reported_prior, patient_attributes_causation, patient_reports_generic; patient_reports_generic no longer matches wife|husband|spouse|family|witness|EMS subjects, a bare 'S:'/'Subjective:' header or 'Self-reported' (patient-reported stays). (2) intake_form_accident_date is self_report: false, so you can delete _NOT_PATIENT_STATEMENT in grounding.py:175. (3) NEW top-level lexicon key self_report_scope.exclude_sentence: if the sentence containing a self_report hit matches that regex (EMS/witness/wife/husband/family/... + speech verb, or 'per his wife/EMS'), the statement is not the patient's -> source_kind stays 'record'. Reference: research/lexicon_selfcheck.py is_patient_statement(). Please replace _PATIENT_WORDS/_SELF word lists with 'any self_report entry hit AND NOT exclude_sentence'. Tests to add: has_self_report False for 'EMS reports neck pain 7/10.', 'Wife complains of neck pain.', 'Witness states the sedan was stopped.', 'S: neck pain 7/10.', 'Self-reported neck pain 7/10.', 'Date of accident per intake form: 2026-01-19.'; True for 'Patient complains of neck pain.', 'C/O neck pain 7/10 and headache.', 'Patient states symptoms began after the January collision.' Probes: evals/lexicon_heldout.jsonl groups explicit_patient, non_patient_speaker, headers_not_attribution (26 rows). Judgement call for the D-entry: T-036 r3 blocker 1 asked S:/Self-reported lines to be labelled patient_report; the coordinator brief asked for none. I followed the brief (a section header is not an explicit attribution); summaries still keep the verbatim marker. For architect: DECISIONS.md:286 and lexicon header lines 25-26 should say 'self_report entries that name the patient, minus self_report_scope.exclude_sentence'.
- 2026-11-02T02:14:18Z researcher: AC 1 checked: selfcheck PASS: 26 new probes (explicit_patient 8/8, non_patient_speaker 12/12, headers_not_attribution 5/5 + 2 reclassified) in evals/lexicon_heldout.jsonl; self_report_scope.exclude_sentence added; intake entry self_report false; golden MUST 11/11
- 2026-11-02T02:14:21Z researcher: moved in_progress -> in_review: AC2 (flags.py/grounding.py + tests) belongs to backend-1 (see card note); AC3 awaits orchestrator D-entry and architect note on DECISIONS.md:286. Lexicon side (AC1) done.
- 2026-11-02T02:14:34Z orchestrator: review dispatched: adjuster (haiku)
- 2026-11-02T02:18:03Z orchestrator: AC 3 checked: memory/ORCHESTRATOR_DECISIONS.md D-033 records the narrowing of ADR-013 / DECISIONS.md:286
- 2026-11-02T02:18:03Z orchestrator: flags.py side assigned to backend-3 (backend-1 busy re-recording). Review held until AC2 lands.
- 2026-11-02T02:19:00Z orchestrator: review claims-adjuster-reviewer (claude-haiku-5-5): fail — reviews/T-061-claims-adjuster.md; round 1; findings:
    - [blocker] AC2 not done: production still labels EMS, witness, wife and family complaints as Patient self-report — fix: In grounding.has_self_report: replace _SELF and _PATIENT_WORDS with 'any lexicon self_report hit AND NOT self_report_scope.exclude_sentence' (read from lexicon.yaml, as research/lexicon_selfcheck.py:is_patient_statement does). Mark the intake date self_report false (done in 
    - [major] Commit leaves test_flags_pass.py red (regression from parent): stale r2 assertion on 'Subjective:' header — fix: Update the yes/no lists in test_flags_pass.py to D-033 (bare Subjective:/S: header is record; Patient-reported stays patient) and add the AC2 tests from finding 1 in the same file. Report the pytest subset result in the card evidence.
    - [major] exclude_sentence drops explicit patient statements when a family or EMS word and a speech verb share the sentence — fix: Anchor the exclusion to the sentence subject (sentence-initial 'EMS|Wife|Witness|Family ... <verb>' or a 'Per <non-patient>' clause) and never exclude a sentence that starts with or names Patient/Pt/C/O. Add both sentences to self_report_scope.examples.keep and to 
    - [minor] Spec text still states the superseded rule (DECISIONS.md:286, lexicon.yaml:25-26) — fix: Architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to 'self_report entries that name the patient, minus self_report_scope.exclude_sentence'. Then set card AC3 done.
- 2026-11-02T02:19:00Z orchestrator: assigned: backend-3
- 2026-11-02T02:19:23Z backend: claimed
- 2026-11-02T02:20:18Z backend: AC 2 checked: grounding._self_report = any lexicon self_report hit minus self_report_scope.exclude_sentence (sentence-subject anchored); tests/unit/test_flags_pass.py d033 tests: EMS, wife, witness, family, S:/Subjective:, Self-reported -> record; Patient states/c/o -> patient_report; patient subject mentioning EMS/wife stays patient. unit suite 835 passed; make_curated --check equal; lexicon_selfcheck PASS (held-out 115/115, MUST 11/11)
- 2026-11-02T02:20:18Z backend: backend (T-061 AC2 + adjuster r1): (1) grounding.py: removed _SELF/_PATIENT_WORDS/_NOT_PATIENT_STATEMENT; has_self_report now reads the lexicon (self_report entries + self_report_scope.exclude_sentence, tested on the hit's sentence). A looser _SELF_CARRIED regex remains for the SUMMARY side only (does the summary carry the attribution, e.g. 'complained of'); it never labels. (2) EDITED app/llm/lexicon.yaml exclude_sentence (allowed for this card): now anchored to the sentence subject (^ optional his/her/the/patient's + EMS|wife|... up to 3 words + speech verb, or sentence-initial 'Per <non-patient>'), so 'Patient states EMS noted a laceration.' / 'Patient reports his wife said he was fine.' / 'Patient states his wife drove him to the ER.' stay patient_report; examples.keep extended. selfcheck PASS. (3) test_flags_pass.py updated to D-033 ('Subjective:' now record) + new tests. Not done: held-out jsonl probes for the patient-subject-mentions-family case (evals/ is qa/researcher-owned) and the architect amendment of DECISIONS.md:286 / lexicon.yaml:25-26 wording.
- 2026-11-02T02:20:18Z backend: moved in_progress -> in_review
- 2026-11-02T02:20:49Z orchestrator: review dispatched: adjuster haiku r2

## Handoff
AC2 done in grounding.py with tests; lexicon exclude_sentence anchored to sentence subject (adjuster major); test_flags_pass updated to D-033. Verified: unit 835 passed, make_curated --check equal, lexicon_selfcheck PASS. Left: heldout probes for the new keep cases (researcher), architect wording of DECISIONS.md:286.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:21:05.948Z

**tool call — Bash**
````
{
 "command": "git merge-base --is-ancestor dd545e3 HEAD && echo \"dd545e3 is ancestor of HEAD\"; git log --oneline -8 -- app/backend/grounding.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py; echo \"---SHOW e1400d4 STAT---\"; git show --stat e1400d4 | head -30; echo \"---SHOW 4eebb2d touches backend?---\"; git show --stat --format= 4eebb2d | grep -E \"backend|lexicon|tests\" || echo \"none\"",
 "description": "Check commit ancestry and files changed by round-2 commit"
}
````

### User / tool · 2026-11-02T02:21:06.144Z

**tool result**
````
dd545e3 is ancestor of HEAD
e1400d4 feat(backend): patient_report only from explicit patient attribution, scoped exclusion (T-061, D-033)
dd545e3 feat(research): narrow lexicon self_report to explicit patient attribution (T-061)
5216d06 fix(backend): D-032 objective_negative context only, scene_facts need phrase list, one flag per prior-condition sentence
3f37141 fix(backend): source_kind from lexicon self_report with explicit patient attribution, case-level conflict-check warning, single-period templates (T-036 r3)
cd4bc60 fix(backend): neutral flag templates, visible conflict-pass failure, patient_report only on explicit attribution (T-036 r2)
199785f feat(backend): LLM flag passes with lexicon floor, conflict pass, J3/J4 wiring (T-036)
1365926 fix(backend): check_amount, endpoint_unverified, strict keys (T-030 r2)
217e243 feat(backend): grounding verifier, sentence splitter, confidence, why templates (T-030)
---SHOW e1400d4 STAT---
commit e1400d4e1fe7e3a2a7443fa7227ce82f2044d631
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:20:21 2026 -0600

    feat(backend): patient_report only from explicit patient attribution, scoped exclusion (T-061, D-033)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/grounding.py      | 41 ++++++++++++++++++++++++---------------
 app/llm/lexicon.yaml          |  6 +++---
 tests/unit/test_flags_pass.py | 45 +++++++++++++++++++++++++++++++++++++++++--
 3 files changed, 71 insertions(+), 21 deletions(-)
---SHOW 4eebb2d touches backend?---
none
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:21:06.707Z

**tool call — Bash**
````
{
 "command": "grep -n \"has_self_report\\|_self_report\\|self_report_scope\\|exclude_sentence\\|_SELF\\|_PATIENT_WORDS\\|_NOT_PATIENT_STATEMENT\" app/backend/flags.py app/backend/grounding.py; echo \"---\"; grep -n \"self_report_scope\" -A 40 app/llm/lexicon.yaml | head -80",
 "description": "Locate self-report code paths and scope config in lexicon"
}
````

### User / tool · 2026-11-02T02:21:06.800Z

**tool result**
````
app/backend/grounding.py:75:    scope = (data.get("self_report_scope") or {}).get("exclude_sentence") if isinstance(data, dict) else None
app/backend/grounding.py:169:_SELF_CARRIED = re.compile(r"\bc/o\b|\bcomplain(?:s|ed|ing|t)?\b|\b(?:patient|pt\.?|he|she|client)\s+(?:states?|stated|reports?|reported|endorses|admits|"
app/backend/grounding.py:188:def _self_report(text: str) -> bool:
app/backend/grounding.py:190:    attribution only. A hit whose sentence names another speaker (EMS, witness, wife, family: `self_report_scope.exclude_sentence`)
app/backend/grounding.py:206:    if _self_report(excerpt) and not (_self_report(summary) or _SELF_CARRIED.search(summary)):
app/backend/grounding.py:228:def has_self_report(text: str) -> bool:
app/backend/grounding.py:230:    return _self_report(text)
app/backend/flags.py:46:         "source_kind": "patient_report" if grounding.has_self_report(excerpt) else "record",
app/backend/flags.py:125:            lx["source_kind"] = "patient_report" if grounding.has_self_report(lx["excerpt"]) else "record"
---
85:# when the hit's sentence matches `self_report_scope.exclude_sentence` (a named non-patient speaker with a speech verb, or
86-# "per <wife|husband|EMS|...>"). Bare "S:", "Subjective:" and "Self-reported" headers are not matched by any self_report entry,
87-# and the intake-form date entry is self_report: false. Reference implementation: research/lexicon_selfcheck.py:is_patient_statement().
88:self_report_scope:
89-  exclude_sentence: '^\W*(?:(?:the|his|her|patient''s|pt''s)\s+)?(?:EMS|paramedics?|witness(?:es)?|bystanders?|wife|husband|spouse|mother|father|parents?|family|friends?|relatives?|daughter|son|sibling|caregiver|police|officer|nurse|staff)\b(?:\s+[\w''-]+){0,3}?\s+(?:reports?|reported|states?|stated|says|said|complains?|complained|c/o|describes?|described|notes?|noted|relates?|believes?|attributes?|links?|thinks?|claims?)\b|^\W*per\s+(?:the\s+|his\s+|her\s+)?(?:wife|husband|spouse|family|witness|EMS|mother|father)\b'
90-  note: 'T-061 r1: anchored to the sentence SUBJECT (a sentence that starts with a non-patient speaker, or with "Per <non-patient>"); a patient subject that merely mentions EMS or a wife stays patient. Sentence-level test: the sentence containing the match is tested; a hit means the statement is not the patient''s, so source_kind stays "record" and no "Patient self-report" label is shown.'
91-  examples:
92-    exclude: ['EMS reports neck pain 7/10.', 'Wife complains of neck pain.', 'Per his wife, headaches began at the scene.']
93-    keep: ['Patient complains of neck pain.', 'C/O neck pain 7/10 and headache.', 'Patient states EMS noted a laceration.', 'Patient reports his wife said he was fine.', 'Patient states his wife drove him to the ER.']
94-
95-entries:
96-
97-# ───────────────────────── pre_existing ─────────────────────────
98-
99-- id: prior_history_year_resolved
100-  pattern: '\b(?P<year>(?:19|20)\d{2})\b(?!-\d)\s*[,;:-]?\s*(?:now\s+|since\s+|which\s+(?:has\s+)?|and\s+(?:has\s+)?)?(?:fully\s+|completely\s+)?(?:resolved|healed|recovered)\b|\b(?:resolved|healed|recovered)\s+(?:in|by)\s+(?P<year2>(?:19|20)\d{2})\b'
101-  flag_type: pre_existing
102-  category: pre_existing
103-  hedge: false
104-  self_report: false
105-  strength: high
106-  negatable: false
107-  year_filter: true
108-  rationale: >
109-    A dated prior condition described as resolved ("low back pain in 2023, resolved") is still a documented prior
110-    condition. Adjusters and ISO ClaimSearch hunt for exactly these, and concealing one costs credibility.
111-    "Resolved" helps the claimant, but the paralegal must see it and decide relevance (here a different body region).
112-  source: 'AA A3; AA src 2 (Verisk ISO ClaimSearch), src 15; Appendix C record 3'
113-  false_positive: 'A year equal to or after the accident year ("headache 2026, resolved") is post-accident recovery, not a prior; the year filter drops it. ISO dates are not read as years.'
114-  appendix_c: [3]
115-  examples:
116-    hit: ['Patient reports low back pain in 2023, resolved.', 'neck strain 2019 - fully resolved', 'Neck pain resolved in 2024.']
117-    miss: ['Seen 2026-01-16 for neck pain.', 'Symptoms improving since visit 3.']
118-    negated: ['Headache 2026, resolved.']
119-
120-- id: history_of
121-  pattern: '\b(?<!family\s)(?:past\s+|prior\s+|previous\s+)?(?:medical\s+)?history\s+of\b(?!\s+(?:the\s+)?present\s+illness)'
122-  flag_type: pre_existing
123-  category: pre_existing
124-  hedge: false
125-  self_report: false
126-  strength: medium
127-  negatable: true
128-  rationale: '"History of X" is the standard clinical way to record a prior condition (AA A3).'
--
764:  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. T-061: it does NOT match a bare "S:" / "Subjective:" header or "Self-reported" (a section label is not an attribution), and a sentence whose speaker is EMS, a witness, a spouse or family is excluded by self_report_scope. "C/O" and "complains of" with no named speaker are read as the patient, which is the clinical convention.'
765-  appendix_c: [1, 3, 5, 9]
766-  examples:
767-    hit: ['Patient reports low back pain in 2023, resolved.', 'Patient reports missing 3 days of work.', 'C/O neck pain 7/10 and headache.', 'Pt states pain worse with rotation.', 'Patient endorses headaches.', 'Per patient, pain 5/10 today.']
768-    miss: ['Cervical range of motion reduced approx. 40%.']
769-
770-- id: intake_form_accident_date
771-  pattern: '\bper\s+(?:the\s+)?(?:intake(?:\s+form)?|patient\s+intake(?:\s+form)?|registration(?:\s+form)?|questionnaire|patient\s+paperwork)\b|\b(?:date\s+of\s+(?:accident|injury|loss)|accident\s+date|DOA|DOI)\s+(?:per|according\s+to|as\s+reported\s+by)\s+(?:the\s+)?(?:patient|pt|intake|form|client)\b'
772-  flag_type: causation
773-  category: accident_date_provenance
774-  hedge: false
775-  self_report: false
776-  strength: high
777-  negatable: false
778-  rationale: 'An accident date or history taken from an intake form or the patient, not the clinician. Record 7''s "Date of accident per intake form: 2026-01-19" conflicts with the EMS/ER treatment dates (2026-01-09). The defense uses a second date to suggest a different incident (JLG Trucking). The code conflict rule (ADR-014) owns the conflict; this entry flags the provenance wording.'
779-  source: 'AA A7; AA src 10 (JLG Trucking), src 17 (impeachment with intake forms); Appendix C record 7'
780-  false_positive: 'Round 2 split this from the generic "per patient" marker, which is now low (self_report). T-061: self_report is false here because an intake form is a document, not the patient''s statement; source_kind stays "record". "Date of injury per patient" is still caught by patient_reports_generic. "Per protocol" does not match.'
781-  appendix_c: [7]
782-  examples:
783-    hit: ['Date of accident per intake form: 2026-01-19.', 'Date of injury per patient: 03/02/2026.']
784-    miss: ['Per protocol, ice applied.', 'Per patient, pain 5/10 today.']
785-
786-- id: new_onset
787-  pattern: '\bnew(?:ly)?[-\s]+(?:onset|developed|complaints?|symptoms?|pain)\b'
788-  flag_type: causation
789-  category: new_onset
790-  hedge: false
791-  self_report: false
792-  strength: high
793-  negatable: true
794-  rationale: 'New symptoms after a treatment gap invite the intervening-cause argument. Record 7 documents "pain radiating to right arm with numbness in fingers" 73 days after PT discharge and 129 days after the first recorded treatment. Plaintiffs answer with progression; the tool keeps "new onset" verbatim and flags it.'
795-  source: 'AA A1, A8; AA src 1 (timing), src 16; Appendix C record 7'
796-  false_positive: '"No new complaints" is negated. "New patient evaluation" does not match.'
797-  appendix_c: [7]
798-  examples:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:21:08.410Z

**tool call — Bash**
````
{
 "command": "sed -n 55,100p app/backend/grounding.py; echo \".....\"; sed -n 160,235p app/backend/grounding.py",
 "description": "Read production self-report code in grounding.py"
}
````

### User / tool · 2026-11-02T02:21:08.504Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:21:08.922Z

**tool call — Bash**
````
{
 "command": "sed -n 30,60p app/backend/flags.py; echo \".....\"; sed -n 110,135p app/backend/flags.py",
 "description": "Read flags.py call sites for source_kind"
}
````

### User / tool · 2026-11-02T02:21:09.022Z

**tool result**
````
def _compose(f: dict) -> dict:
    st = f["_stage"]
    ladder = {"grounding_failures": st["grounding_failures"], "schema_valid": True, "code_reasons": [], "judge": st.get("judge")}
    ctx = {"injection": st["injection"], "agreement": st.get("agreement"), "fixture_miss": st.get("fixture_miss", False),
           "llm_failed": st.get("llm_failed", False)}
    f["state"], f["reasons"] = confidence.compose_state(ladder, ctx)
    f["why"] = " ".join(why.why(c) for c in f["reasons"]) if f["reasons"] else "Found by the phrase list and the model, and the second check agreed."
    return f


def _flag(record: dict, ftype: str, category: str, excerpt: str, origin: str, span, tagged: bool, agreement) -> dict:
    base = _base(record)
    f = {"type": ftype, "category": category, "excerpt": excerpt, "origin": origin, "record_no": record["n"],
         "record_id": record.get("id", f"r{record['n']}"), "review_status": "pending",
         "source_kind": "patient_report" if grounding.has_self_report(excerpt) else "record",
         "evidence": [{"record_no": record["n"], "text": excerpt,
                       "start": base + span[0] if span else None, "end": base + span[1] if span else None}],
         "ladder": {"item_id": None, "generator": None, "judge": None, "code_checks": {}},
         "_stage": {"grounding_failures": [], "injection": tagged, "agreement": agreement,
                    # model-involved flags are not verified until judge 4 has agreed ("unavailable" = not double-checked yet)
                    "judge": "unavailable" if origin != "lexicon" else None}}
    _render(f, record)
    return _compose(f)


# ------------------------------------------------------------------ lexicon floor
def _hedge_run(text: str, units: list, a: int, b: int):
    """A hedge unit travels with the adjacent hedge units (R-TL-8): the flag quotes the whole run, never half a hedge."""
    if not grounding.is_hedge_unit(text[a:b]):
.....
        if k not in seen:
            seen.add(k)
            uniq.append(lf)
    llm_spans = [grounding.locate(body, lf["excerpt"]) for lf in uniq]
    for lx in lex_flags:
        lx = dict(lx)
        lx["_stage"] = dict(lx["_stage"], injection=tagged)
        match = next((i for i, lf in enumerate(uniq) if i not in used and lf["type"] == lx["type"] and _overlap(llm_spans[i], lx.get("_span"))), None)
        if match is not None:
            used.add(match)
            lx["origin"], lx["_stage"]["agreement"], lx["_stage"]["judge"] = "both", "both", "unavailable"
            lx["ladder"] = dict(lx["ladder"], judge=None)
            # D-030: evidence is the verbatim phrase span the model returned (still grounded by ground()); the lexicon sentence is
            # only the fallback quote for phrase-list-only flags
            lx["excerpt"] = uniq[match]["excerpt"]
            lx["source_kind"] = "patient_report" if grounding.has_self_report(lx["excerpt"]) else "record"
            sp = llm_spans[match]
            base = _base(record)
            lx["evidence"] = [{"record_no": record["n"], "text": lx["excerpt"],
                               "start": base + sp[0] if sp else None, "end": base + sp[1] if sp else None}]
            lx["_span"] = sp or lx.get("_span")
            _render(lx, record)
        else:
            lx["origin"], lx["_stage"]["agreement"] = "lexicon", "lexicon_only"
            lx["_stage"]["llm_failed"], lx["_stage"]["fixture_miss"] = llm_failed, fixture_miss
            if llm_failed or fixture_miss:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:21:09.384Z

**tool call — Bash**
````
{
 "command": "git show e1400d4 -- app/backend/grounding.py app/llm/lexicon.yaml | head -200",
 "description": "Show round-2 backend and lexicon diff"
}
````

### User / tool · 2026-11-02T02:21:09.482Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:21:39.920Z

**tool call — Bash**
````
{
 "command": "sed -n 1,30p app/backend/flags.py; echo \".....\"; grep -n \"^def \\|^from\\|^import\" app/backend/flags.py | head -60; echo \".....\"; grep -n \"def _base\\|def _render\" -A 8 app/backend/flags.py | head -40; echo \".....\"; grep -n \"self_report: true\" -B 12 app/llm/lexicon.yaml | grep -E \"^\\S*-?\\s*(- id|pattern|self_report)|id:\" | head -60",
 "description": "Inspect flags.py helpers and self_report lexicon entries"
}
````

### User / tool · 2026-11-02T02:21:40.038Z

**tool result**
````
"""LLM flag engines with the lexicon as the floor (ADR-008, ADR-013; R-FL-3..5, R-FL-7, R-FL-8; LLM_VS_CODE rows 11-13, 16).
Per-record pre_existing/causation pass (one call per record, so an injected record cannot suppress another record's flags) merged
with the code lexicon scan; one cross-record pass for semantic conflicts (accident-date and provider-name conflicts are code, conflicts.py).
The model returns only type, category and quoted text; titles and explanations are code templates. Flags never get a review_status
other than 'pending'. `call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is supplied by the pipeline."""
from pydantic import ValidationError

from app.backend import sentences, confidence, flag_templates as FT, generator, grounding, injection, judges, lexicon_scan, schemas, why
from app.llm import audited as AU, promptlib, provider as P

_PER_RECORD_TYPES = ("pre_existing", "causation")
# D-032: normal/negative findings are context only and never become flags (from either signal); a scene_facts flag needs a phrase-list
# hit on a specific adjuster phrase, never just a model's reading of a mechanism description.
_CONTEXT_ONLY = ("objective_negative",)
_NEEDS_LEXICON = ("scene_facts",)
_CONFLICT_CATEGORIES = ("treatment_plan_vs_actual", "other_fact_mismatch")


# ------------------------------------------------------------------ helpers
def _base(record: dict) -> int:
    return generator.body_offset(record) if record.get("text") else 0


def _render(f: dict, record: dict):
    try:
        f["title"], f["explanation"] = FT.render(f["type"], f["category"], provider=record.get("source"), date=record.get("date_iso"),
                                                 quote=f.get("excerpt"))
    except KeyError:    # a category outside the closed list: ground() rejects it; no model text is used as a title
        f["title"], f["explanation"] = "Unrecognised flag category", "The model proposed a category that is not on the closed list."

.....
6:from pydantic import ValidationError
8:from app.backend import sentences, confidence, flag_templates as FT, generator, grounding, injection, judges, lexicon_scan, schemas, why
9:from app.llm import audited as AU, promptlib, provider as P
20:def _base(record: dict) -> int:
24:def _render(f: dict, record: dict):
32:def _compose(f: dict) -> dict:
42:def _flag(record: dict, ftype: str, category: str, excerpt: str, origin: str, span, tagged: bool, agreement) -> dict:
58:def _hedge_run(text: str, units: list, a: int, b: int):
73:def lexicon_flags(record: dict, accident_year=None) -> list:
97:def _overlap(a, b) -> bool:
101:def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False, *, llm_failed: bool = False, fixture_miss: bool = False) -> list:
148:def ground(flags: list, record: dict) -> list:
162:def _record_warning(record: dict) -> dict:
176:def run_flag_pass(record: dict, *, call, tagged: bool = False, accident_year=None, case_text: str = "") -> list:
201:def _incomplete(records: list) -> dict:
212:def run_conflict_pass(records: list, *, call, any_tagged: bool = False, case_text: str = "") -> list:
259:def judge_flags(flags: list, *, call, case_text: str = "") -> list:
.....
20:def _base(record: dict) -> int:
21-    return generator.body_offset(record) if record.get("text") else 0
22-
23-
24:def _render(f: dict, record: dict):
25-    try:
26-        f["title"], f["explanation"] = FT.render(f["type"], f["category"], provider=record.get("source"), date=record.get("date_iso"),
27-                                                 quote=f.get("excerpt"))
28-    except KeyError:    # a category outside the closed list: ground() rejects it; no model text is used as a title
29-        f["title"], f["explanation"] = "Unrecognised flag category", "The model proposed a category that is not on the closed list."
30-
31-
32-def _compose(f: dict) -> dict:
.....
488-- id: self_reported_prior
489-  pattern: '\b(?:patient|pt\.?|he|she|client)\s+(?:reports|reported|states|stated|notes|endorses|admits|recalls)\s+(?:(?:a|an|some)\s+)?(?:prior|previous|past|old|earlier|history)\b'
493:  self_report: true
738-- id: patient_attributes_causation
739-  pattern: '(?:\b(?:patient|pt\.?|he|she|client)\s+(?:states|stated|reports|reported|believes|attributes|relates|related|feels|claims|says|said|thinks)\b|\bper\s+(?:the\s+)?(?:patient|pt)\b|\bcomplain(?:s|ing)?\s+of\b|\bc/o\b)[^.;]{0,80}?\b(?:after|since|from|due\s+to|because\s+of|caused\s+by|following|began\s+with)\b[^.;]{0,40}?\b(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\b|\b(?:patient|pt\.?|he|she|client)\s+(?:attributes?|relates?|links?|ascribes?|connects?|associates?|blames?)\b[^.;]{0,80}?\b(?:to|on|with)\s+(?:the\s+|this\s+|that\s+|a\s+)?(?:\w+\s+){0,2}(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\b|\b(?:patient|pt\.?|he|she|client)\s+(?:believes|feels|thinks|states|claims|says|reports)\s+(?:that\s+)?(?:the\s+|this\s+)?(?:\w+\s+)?(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\s+(?:caused|led\s+to|resulted\s+in|is\s+(?:the\s+)?(?:cause|reason|why|responsible)|triggered|brought\s+on)\b|\b(?:after|since|from|due\s+to|following)\b[^.;]{0,60}?\b(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impact)\b[^.;]{0,40}?,?\s*per\s+(?:the\s+)?(?:patient|pt)\b'
743:  self_report: true
754-- id: patient_reports_generic
755-  pattern: '\b(?:patient|pt\.?|he|she|client)\s+(?:reports|reported|states|stated|endorses|complains|c/o|describes|relates|notes|admits|recalls)\b|\bc/o\b|\bcomplain(?:s|ing)?\s+of\b|\bper\s+(?:the\s+)?(?:patient|pt)\b|\bpatient-?\s?reported\b'
759:  self_report: true
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:21:40.801Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/ | head -50; echo \".....\"; python3 - <<'EOF'\nimport yaml\nd=yaml.safe_load(open('/Users/arsis/zlayt-pm-project/app/llm/lexicon.yaml'))\nfor e in d['entries']:\n    if e.get('self_report'):\n        print(e['id'], '|', e['pattern'][:400])\n        print()\nEOF",
 "description": "List review evidence dir and self_report entry patterns"
}
````

### User / tool · 2026-11-02T02:21:40.905Z

**tool result (error)**
````
Exit code 1
M0-r2-staff-resolution.md
T-001-exercise-1.txt
T-001-exercise-2.txt
T-001-exercise-3.txt
T-001-r2-readonly-repros.txt
T-001-r3-repro.out.txt
T-001-r3-repro.sh
T-002-curl.txt
T-002-r2-activity-390.png
T-002-r2-board-390.png
T-002-r2-csrf-curl.txt
T-002-r2-inbox-390.png
T-002-r2-milestones-390.png
T-002-r2-personas-390.png
T-002-r2-state-390.png
T-002-r2-xss.json
T-002-r3-404.py
T-002-r3-activity-390.png
T-002-r3-board-390.png
T-002-r3-inbox-390.png
T-002-r3-milestones-390.png
T-002-r3-personas-390.png
T-002-r3-probe.out.txt
T-002-r3-probe.py
T-002-r3-state-390.png
T-002-r3-ui.out.txt
T-002-r3-ui.py
T-003-git-guard-commit-secret-probe.txt
T-003-git-guard-probe.txt
T-003-other-hooks-probe.txt
T-003-r2-commit-secret-probe.out.txt
T-003-r2-commit-secret-probe.py
T-003-r2-git-guard-results.txt
T-003-r2-probe-board2.out.txt
T-003-r2-probe-board2.py
T-003-r2-probe-corpus.txt
T-003-r2-probe-direct.out.txt
T-003-r2-probe-direct.out2.txt
T-003-r2-probe-direct.py
T-003-r3-probe-board2.out.txt
T-003-r3-probe-corpus.out.txt
T-003-r3-probe-corpus.py
T-003-r3-probe-direct.out.txt
T-003-r3-probe-legit.out.txt
T-003-r3-probe-legit.py
T-003-r3-probe-pwd.out.txt
T-003-r3-probe-pwd.py
T-003-r3-probe-rwg.out.txt
T-003-r3-probe-rwg.py
T-003-r3-probe-targeted.out.txt
.....
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'yaml'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:21:49.347Z

**tool call — Bash**
````
{
 "command": "echo \"live diff vs HEAD for reviewed paths:\"; git status --short -- app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py research evals app/llm; echo \"(end)\"; git diff --stat HEAD -- app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit research evals | tail -3; echo \"(end diff)\"; git rev-parse --short HEAD e1400d4; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$SCR/e1400d4\" && git archive e1400d4 | tar -x -C \"$SCR/e1400d4\" && echo \"archive at $SCR/e1400d4\" && ls \"$SCR/e1400d4\" | head -30",
 "description": "Check live vs commit diff and extract e1400d4 archive to scratchpad"
}
````

### User / tool · 2026-11-02T02:21:49.636Z

**tool result**
````
live diff vs HEAD for reviewed paths:
 M app/llm/provider.py
 M app/llm/record.py
 M evals/reports/latest.json
?? app/llm/prompts/narrative_v1.md
?? evals/reports/20261102T020933Z.md
?? evals/reports/20261102T021029Z.md
?? evals/reports/20261102T021046Z.md
(end)
 evals/reports/latest.json | 78 +++++++++++++++++++++++++----------------------
 1 file changed, 41 insertions(+), 37 deletions(-)
(end diff)
fatal: Needed a single revision
archive at /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/e1400d4
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
research
reviews
spec
submission
tests
tools
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:21:53.633Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for f in app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py research/lexicon_selfcheck.py; do cmp -s \"$f\" \"$SCR/e1400d4/$f\" && echo \"same as e1400d4: $f\" || echo \"DIFFERS: $f\"; done; .venv/bin/python - <<'EOF'\nimport yaml\nd=yaml.safe_load(open('app/llm/lexicon.yaml'))\nfor e in d['entries']:\n    if e.get('self_report'):\n        print(e['id'], 'self_report=', e.get('self_report'))\nprint(d['self_report_scope']['exclude_sentence'])\nEOF",
 "description": "Confirm live files match e1400d4 and list self_report entries"
}
````

### User / tool · 2026-11-02T02:21:53.845Z

**tool result**
````
same as e1400d4: app/backend/grounding.py
same as e1400d4: app/backend/flags.py
same as e1400d4: app/llm/lexicon.yaml
same as e1400d4: tests/unit/test_flags_pass.py
same as e1400d4: research/lexicon_selfcheck.py
self_reported_prior self_report= True
patient_attributes_causation self_report= True
patient_reports_generic self_report= True
^\W*(?:(?:the|his|her|patient's|pt's)\s+)?(?:EMS|paramedics?|witness(?:es)?|bystanders?|wife|husband|spouse|mother|father|parents?|family|friends?|relatives?|daughter|son|sibling|caregiver|police|officer|nurse|staff)\b(?:\s+[\w'-]+){0,3}?\s+(?:reports?|reported|states?|stated|says|said|complains?|complained|c/o|describes?|described|notes?|noted|relates?|believes?|attributes?|links?|thinks?|claims?)\b|^\W*per\s+(?:the\s+|his\s+|her\s+)?(?:wife|husband|spouse|family|witness|EMS|mother|father)\b
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:22:19.032Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r2-probe.py",
 "content": "\"\"\"T-061 round-2 claims-adjuster probe (read-only). Drives the production flag code path, not the research script.\n\nUsage: .venv/bin/python artifacts/review-evidence/T-061-r2-probe.py <repo_root>\n\nFor each sentence: calls flags._flag(...) (the exact constructor that sets source_kind at flags.py:46) and reports the\nsource_kind it produces, plus grounding.has_self_report(sentence) (the function flags.py:46 and flags.py:125 call).\nAlso reports lexicon.self_report_scope match state for transparency. Nothing is written to the repo.\n\"\"\"\nimport sys\n\nroot = sys.argv[1]\nsys.path.insert(0, root)\n\nfrom app.backend import flags, grounding  # noqa: E402\n\nprint(\"grounding._LEXICON =\", grounding._LEXICON)\n\nREC = {\"n\": 7, \"id\": \"r7\", \"source\": \"Austin EMS\", \"date_iso\": \"2026-01-09\"}\n\n# (sentence, expected source_kind, group, note)\nCASES = [\n    # --- brief script-check (must hold)\n    (\"Patient states pain began after the collision.\", \"patient_report\", \"brief\", \"\"),\n    (\"Patient states his wife drove him to the ER.\", \"patient_report\", \"brief\", \"\"),\n    (\"Wife reports he has been irritable.\", \"record\", \"brief\", \"\"),\n    (\"Per EMS, pt ambulatory at scene.\", \"record\", \"brief\", \"\"),\n    (\"S: neck pain\", \"record\", \"brief\", \"\"),\n    (\"Witness states the car ran the light.\", \"record\", \"brief\", \"\"),\n    # --- round-1 acceptance list (adjuster finding 1 and 3)\n    (\"EMS complains of neck pain 7/10.\", \"record\", \"r1-acc\", \"\"),\n    (\"Witness complains of neck pain.\", \"record\", \"r1-acc\", \"\"),\n    (\"Wife complains of neck pain.\", \"record\", \"r1-acc\", \"\"),\n    (\"Family complains of neck pain.\", \"record\", \"r1-acc\", \"\"),\n    (\"EMS reports neck pain 7/10.\", \"record\", \"r1-acc\", \"\"),\n    (\"Wife reports he was in pain.\", \"record\", \"r1-acc\", \"\"),\n    (\"Date of accident per intake form: 2026-01-19.\", \"record\", \"r1-acc\", \"\"),\n    (\"Patient complains of neck pain.\", \"patient_report\", \"r1-acc\", \"\"),\n    (\"C/O neck pain 7/10 and headache.\", \"patient_report\", \"r1-acc\", \"\"),\n    (\"Patient-reported neck pain 7/10.\", \"patient_report\", \"r1-acc\", \"\"),\n    (\"Patient states EMS noted a laceration.\", \"patient_report\", \"r1-f3\", \"over-exclusion (r1 f3)\"),\n    (\"Patient reports his wife said he was fine.\", \"patient_report\", \"r1-f3\", \"over-exclusion (r1 f3)\"),\n    (\"EMS reports minimal damage.\", \"record\", \"r1-f3\", \"\"),\n    (\"Per his wife, headaches began at the scene.\", \"record\", \"r1-f3\", \"\"),\n    # --- D-033 header and speaker cases named in the brief and the card\n    (\"Subjective: neck pain 7/10.\", \"record\", \"d033\", \"D-033 header is record\"),\n    (\"Self-reported neck pain 7/10.\", \"record\", \"d033\", \"D-033 header; no attribution\"),\n    (\"Witness states the sedan was stopped.\", \"record\", \"d033\", \"\"),\n    # --- adversarial: speaker-label style and abbreviation boundaries (clinical notes)\n    (\"EMS: pt c/o neck pain.\", \"record\", \"adv\", \"speaker-label colon; EMS is the speaker\"),\n    (\"Per EMS, pt. c/o neck pain.\", \"record\", \"adv\", \"'pt.' splits the sentence before the hit\"),\n    (\"EMS noted pt. reports neck pain 7/10.\", \"record\", \"adv\", \"'pt.' splits the sentence before the hit\"),\n    (\"Pt. reports EMS noted a laceration.\", \"patient_report\", \"adv\", \"patient subject; 'Pt.' abbreviation\"),\n    # --- adversarial: speakers not on the closed exclusion list\n    (\"Passenger reports patient complained of neck pain.\", \"record\", \"adv\", \"passenger = witness-type speaker\"),\n    (\"Other driver states patient complained of neck pain.\", \"record\", \"adv\", \"non-patient party\"),\n    (\"Girlfriend reports he complains of neck pain.\", \"record\", \"adv\", \"family-type speaker not listed\"),\n    (\"Co-worker reports patient c/o neck pain.\", \"record\", \"adv\", \"non-patient speaker not listed\"),\n    (\"Ambulance crew reports patient complained of neck pain.\", \"record\", \"adv\", \"EMS-type speaker not listed\"),\n    (\"Triage nurse reports he is in pain.\", \"record\", \"adv\", \"'nurse' not at subject position\"),\n    (\"Wife of 20 years and mother of two reports he complains of neck pain.\", \"record\", \"adv\", \"word window > 3\"),\n    # --- adversarial: mixed sentences (one sentence, two speakers)\n    (\"EMS reports neck pain, patient states headaches.\", \"patient_report\", \"adv\", \"patient clause in EMS sentence (lost)\"),\n    (\"C/O neck pain; wife reports headaches.\", \"record\", \"adv\", \"patient clause then wife clause; whole sentence labelled\"),\n]\n\nfails = []\nrows = []\nfor sent, expect, group, note in CASES:\n    f = flags._flag(dict(REC), \"causation\", \"causation\", sent, \"lexicon\", None, False, None)\n    got = f[\"source_kind\"]\n    hs = grounding.has_self_report(sent)\n    ok = (got == expect)\n    rows.append((group, ok, got, expect, hs, sent, note))\n    if not ok:\n        fails.append((group, sent, got, expect, note))\n\nfor group, ok, got, expect, hs, sent, note in rows:\n    tag = \"OK  \" if ok else \"MISS\"\n    print(f\"{tag} [{group}] flags._flag source_kind={got:<15} expect={expect:<15} has_self_report={hs!s:<5} | {sent!r}\" + (f\"  ({note})\" if note else \"\"))\n\nn_ok = sum(1 for r in rows if r[1])\nprint(f\"SUMMARY {n_ok}/{len(rows)} match expected\")\nfor g in (\"brief\", \"r1-acc\", \"r1-f3\", \"d033\", \"adv\"):\n    sub = [r for r in rows if r[0] == g]\n    print(f\"  {g}: {sum(1 for r in sub if r[1])}/{len(sub)}\")\n"
}
````

### User / tool · 2026-11-02T02:22:19.131Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r2-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:22:21.277Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python artifacts/review-evidence/T-061-r2-probe.py \"$SCR/e1400d4\" 2>&1 | tee artifacts/review-evidence/T-061-r2-probe.txt",
 "description": "Run round-2 probe against the e1400d4 archive and save output"
}
````

### User / tool · 2026-11-02T02:22:21.580Z

**tool result**
````
grounding._LEXICON = /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/e1400d4/app/llm/lexicon.yaml
OK   [brief] flags._flag source_kind=patient_report  expect=patient_report  has_self_report=True  | 'Patient states pain began after the collision.'
OK   [brief] flags._flag source_kind=patient_report  expect=patient_report  has_self_report=True  | 'Patient states his wife drove him to the ER.'
OK   [brief] flags._flag source_kind=record          expect=record          has_self_report=False | 'Wife reports he has been irritable.'
OK   [brief] flags._flag source_kind=record          expect=record          has_self_report=False | 'Per EMS, pt ambulatory at scene.'
OK   [brief] flags._flag source_kind=record          expect=record          has_self_report=False | 'S: neck pain'
OK   [brief] flags._flag source_kind=record          expect=record          has_self_report=False | 'Witness states the car ran the light.'
OK   [r1-acc] flags._flag source_kind=record          expect=record          has_self_report=False | 'EMS complains of neck pain 7/10.'
OK   [r1-acc] flags._flag source_kind=record          expect=record          has_self_report=False | 'Witness complains of neck pain.'
OK   [r1-acc] flags._flag source_kind=record          expect=record          has_self_report=False | 'Wife complains of neck pain.'
OK   [r1-acc] flags._flag source_kind=record          expect=record          has_self_report=False | 'Family complains of neck pain.'
OK   [r1-acc] flags._flag source_kind=record          expect=record          has_self_report=False | 'EMS reports neck pain 7/10.'
OK   [r1-acc] flags._flag source_kind=record          expect=record          has_self_report=False | 'Wife reports he was in pain.'
OK   [r1-acc] flags._flag source_kind=record          expect=record          has_self_report=False | 'Date of accident per intake form: 2026-01-19.'
OK   [r1-acc] flags._flag source_kind=patient_report  expect=patient_report  has_self_report=True  | 'Patient complains of neck pain.'
OK   [r1-acc] flags._flag source_kind=patient_report  expect=patient_report  has_self_report=True  | 'C/O neck pain 7/10 and headache.'
OK   [r1-acc] flags._flag source_kind=patient_report  expect=patient_report  has_self_report=True  | 'Patient-reported neck pain 7/10.'
OK   [r1-f3] flags._flag source_kind=patient_report  expect=patient_report  has_self_report=True  | 'Patient states EMS noted a laceration.'  (over-exclusion (r1 f3))
OK   [r1-f3] flags._flag source_kind=patient_report  expect=patient_report  has_self_report=True  | 'Patient reports his wife said he was fine.'  (over-exclusion (r1 f3))
OK   [r1-f3] flags._flag source_kind=record          expect=record          has_self_report=False | 'EMS reports minimal damage.'
OK   [r1-f3] flags._flag source_kind=record          expect=record          has_self_report=False | 'Per his wife, headaches began at the scene.'
OK   [d033] flags._flag source_kind=record          expect=record          has_self_report=False | 'Subjective: neck pain 7/10.'  (D-033 header is record)
OK   [d033] flags._flag source_kind=record          expect=record          has_self_report=False | 'Self-reported neck pain 7/10.'  (D-033 header; no attribution)
OK   [d033] flags._flag source_kind=record          expect=record          has_self_report=False | 'Witness states the sedan was stopped.'
MISS [adv] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'EMS: pt c/o neck pain.'  (speaker-label colon; EMS is the speaker)
OK   [adv] flags._flag source_kind=record          expect=record          has_self_report=False | 'Per EMS, pt. c/o neck pain.'  ('pt.' splits the sentence before the hit)
OK   [adv] flags._flag source_kind=record          expect=record          has_self_report=False | 'EMS noted pt. reports neck pain 7/10.'  ('pt.' splits the sentence before the hit)
OK   [adv] flags._flag source_kind=patient_report  expect=patient_report  has_self_report=True  | 'Pt. reports EMS noted a laceration.'  (patient subject; 'Pt.' abbreviation)
OK   [adv] flags._flag source_kind=record          expect=record          has_self_report=False | 'Passenger reports patient complained of neck pain.'  (passenger = witness-type speaker)
OK   [adv] flags._flag source_kind=record          expect=record          has_self_report=False | 'Other driver states patient complained of neck pain.'  (non-patient party)
MISS [adv] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'Girlfriend reports he complains of neck pain.'  (family-type speaker not listed)
MISS [adv] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'Co-worker reports patient c/o neck pain.'  (non-patient speaker not listed)
OK   [adv] flags._flag source_kind=record          expect=record          has_self_report=False | 'Ambulance crew reports patient complained of neck pain.'  (EMS-type speaker not listed)
OK   [adv] flags._flag source_kind=record          expect=record          has_self_report=False | 'Triage nurse reports he is in pain.'  ('nurse' not at subject position)
MISS [adv] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'Wife of 20 years and mother of two reports he complains of neck pain.'  (word window > 3)
MISS [adv] flags._flag source_kind=record          expect=patient_report  has_self_report=False | 'EMS reports neck pain, patient states headaches.'  (patient clause in EMS sentence (lost))
MISS [adv] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'C/O neck pain; wife reports headaches.'  (patient clause then wife clause; whole sentence labelled)
SUMMARY 30/36 match expected
  brief: 6/6
  r1-acc: 10/10
  r1-f3: 4/4
  d033: 3/3
  adv: 7/13
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:22:29.428Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$SCR/e1400d4\" && /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nimport sys; sys.path.insert(0, '.')\nfrom app.backend import grounding as g\nt = \"Per EMS, pt. c/o neck pain.\"\nlex = g._lexicon()\nfor rid, rx in lex[\"self_report\"].items():\n    for m in rx.finditer(t):\n        s = g._sentence_around(t, m.start(), m.end())\n        print(rid, repr(m.group(0)), 'sentence=', repr(s), 'excluded=', bool(lex['self_report_exclude'].search(s)))\nprint(\"has_self_report:\", g.has_self_report(t))\nEOF",
 "description": "Debug why 'Per EMS, pt. c/o' sentence is not labelled"
}
````

### User / tool · 2026-11-02T02:22:29.612Z

**tool result**
````
patient_reports_generic 'pt. c/o' sentence= 'Per EMS, pt. c/o neck pain' excluded= True
has_self_report: False
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:23:06.603Z

**tool call — Bash**
````
{
 "command": "echo \"--- _SELF/_PATIENT_WORDS/_NOT_PATIENT_STATEMENT in grounding.py:\"; grep -n \"_SELF\\b\\|_PATIENT_WORDS\\|_NOT_PATIENT_STATEMENT\" app/backend/grounding.py || echo \"(none)\"; echo \"--- DECISIONS.md:286:\"; sed -n 286p memory/DECISIONS.md | cut -c1-400; echo \"--- lexicon header 20-30:\"; sed -n 20,30p app/llm/lexicon.yaml; echo \"--- heldout: patient-subject with family/EMS word:\"; grep -n -i \"patient\\(\\W\\|\\s\\)*\\(states\\|reports\\|c/o\\|complains\\)[^\\\"]*\\(EMS\\|wife\\|witness\\|family\\|husband\\|spouse\\)\" evals/lexicon_heldout.jsonl || echo \"(none)\"; grep -c \"\" evals/lexicon_heldout.jsonl; echo \"--- test_flags_pass d033 tests:\"; grep -n \"def test_\\|d033\" tests/unit/test_flags_pass.py | sed -n 1,80p",
 "description": "Check round-1 acceptance greps, spec text, held-out and test coverage"
}
````

### User / tool · 2026-11-02T02:23:06.792Z

**tool result**
````
--- _SELF/_PATIENT_WORDS/_NOT_PATIENT_STATEMENT in grounding.py:
(none)
--- DECISIONS.md:286:
  - `source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt and drives the "Patient self-report" label. Origin is `lexicon`, `llm` or `lexicon+llm`; one-sided hits are `needs_review` (`LEXICON_ONLY`, `LLM_ONLY`). Flags are not editable except a reviewer note.
--- lexicon header 20-30:
#   pre_existing, degenerative_language, speculative_language, patient_report, missed_care, new_onset).
#   Lexicon-only categories (no LLM counterpart; the flag is origin `lexicon`, so needs_review LEXICON_ONLY):
#   prior_surgery, alternative_cause, scene_facts, objective_negative, litigation_referral, recovery_context,
#   accident_date_provenance.
# - `hedge: true` marks the R-TL-8 hedge set: a sentence with a hedge hit is a qualifier unit and can never be cut
#   from an excerpt (ADR-016). `self_report: true` marks wording that explicitly attributes a statement to the PATIENT (T-061); code sets
#   source_kind = "patient_report" from it (ADR-013). Self-report entries are never hedges.
# - `strength`: high and medium raise a flag (origin lexicon, or lexicon+llm). low is context only: it never
#   raises a flag alone. It can still attach to an LLM flag, keep attribution in a summary, or mark a qualifier unit.
# - `negatable: true` → apply the negation guard below. A negated hit is suppressed and logged in the audit.
# - `year_filter: true` → the hit's year (named group `year`, else the first 19xx/20xx in the match) must be
--- heldout: patient-subject with family/EMS word:
(none)
115
--- test_flags_pass d033 tests:
16:def test_ungrounded_model_flag_is_rejected_not_repaired():
24:def test_wrong_category_for_type_is_rejected():
30:def test_model_and_lexicon_agree_then_j4_decides():
44:def test_lexicon_only_flags_get_no_judge_call():
51:def test_model_outage_keeps_lexicon_flags_with_reason():
57:def test_conflict_pass_grounds_both_quotes_and_j3_decides():
70:def test_conflict_pass_failure_is_visible_not_silent():
80:def test_single_quote_conflict_is_rejected():
86:def test_templates_quote_the_record_and_never_say_objective():
95:def test_intake_form_date_is_not_patient_self_report():
101:def test_no_flag_is_ever_accepted_and_patient_report_is_set_by_code():
107:def test_flag_prompt_has_no_model_prose_fields_and_one_block():
114:def test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution():
124:def test_no_template_ends_with_double_period():
130:def test_pipeline_surfaces_conflict_pass_failure_as_run_warning(tmp_path):
140:def test_d032_objective_negative_is_context_only_and_scene_facts_need_the_phrase_list():
150:def test_prior_condition_sentence_does_not_also_raise_alternative_cause():
162:def test_d033_non_patient_speakers_and_headers_are_not_patient_report():
173:def test_d033_mixed_sentences_decide_per_sentence():
179:def test_d033_patient_subject_that_mentions_ems_or_family_stays_patient_report():
189:def test_d033_lexicon_flags_label_source_kind_by_the_same_rule():
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:23:07.393Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\" 2>&1 | tail -2; echo \"---- full unit suite (live) ----\"; timeout 500 .venv/bin/python -m pytest tests/unit -q 2>&1 | tail -6",
 "description": "Run flag/lexicon tests and full unit suite on live tree",
 "timeout": 560000
}
````

### User / tool · 2026-11-02T02:23:09.864Z

**tool result**
````
.................................................                        [100%]
121 passed, 745 deselected in 2.06s
---- full unit suite (live) ----
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:23:13.387Z

**tool call — Bash**
````
{
 "command": "sed -n 95,125p tests/unit/test_flags_pass.py; echo \".....\"; sed -n 160,200p tests/unit/test_flags_pass.py",
 "description": "Read the D-033 unit tests in test_flags_pass.py"
}
````

### User / tool · 2026-11-02T02:23:13.477Z

**tool result**
````
def test_intake_form_date_is_not_patient_self_report():
    """Review T-036 major: only explicit patient attribution sets patient_report."""
    fl = F.lexicon_flags(rec(7))
    assert fl and all(f["source_kind"] == "record" for f in fl)
    assert any(f["source_kind"] == "patient_report" for f in F.lexicon_flags(rec(9)))

def test_no_flag_is_ever_accepted_and_patient_report_is_set_by_code():
    """R-FL-7 / invariant: every flag starts pending; record 9's flag is patient_report from the lexicon, not the model."""
    fl = F.run_flag_pass(rec(9), call=FakeCall({"flags": {"flags": []}}))
    assert all(f["review_status"] == "pending" for f in fl)
    assert any(f["source_kind"] == "patient_report" for f in fl)

def test_flag_prompt_has_no_model_prose_fields_and_one_block():
    """Row 16: only type/category/excerpt cross the schema; the objective_negative category never becomes a UI title with that word."""
    from app.backend import schemas
    assert set(schemas.FlagOutput.model_fields) == {"type", "category", "excerpt", "excerpt_b"}
    assert all("objective_negative" not in f["title"] + f["explanation"] for f in F.lexicon_flags(rec(2)))


def test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution():
    """Review T-036 r2 blocker: ADR-013 - source_kind comes from lexicon self_report entries; intake form / EMS / wife do not qualify."""
    from app.backend import grounding as GR
    yes = ["Patient notes prior neck pain.", "Patient links her neck pain to the collision.",
           "Patient describes neck pain since the collision.", "Patient-reported neck pain 7/10.", "Patient reports prior neck pain.",
           "C/O neck pain 7/10 and headache."]
    no = ["Date of accident per intake form: 2026-01-19.", "Per EMS report, neck pain.", "Wife reports he was in pain.", "EMS reports minimal damage.",
          "Subjective: neck pain 7/10."]            # D-033: a bare Subjective:/S: header is not attribution
    assert all(GR.has_self_report(t) for t in yes) and not any(GR.has_self_report(t) for t in no)

def test_no_template_ends_with_double_period():
    from app.backend import flag_templates as FT
.....


def test_d033_non_patient_speakers_and_headers_are_not_patient_report():
    """T-061 AC2 / D-033: EMS, wife, witness, family and bare S:/Subjective: headers never get patient_report; explicit patient attribution does."""
    for t in ["EMS reports neck pain 7/10.", "Paramedics state the patient was ambulatory at the scene.", "Wife complains of neck pain.",
              "Per his wife, headaches began at the scene.", "Witness states the vehicle was struck from behind.", "Family reports he has been irritable since.",
              "S: neck pain 7/10, worse with rotation.", "Subjective: pain 6/10.", "Self-reported pain 5/10."]:
        assert _kind(t) == "record", t
    for t in ["Patient states symptoms began after the January collision.", "Patient complains of neck pain.", "Pt c/o neck pain 7/10.",
              "C/O neck pain 7/10 and headache.", "Patient-reported pain 4/10."]:
        assert _kind(t) == "patient_report", t


def test_d033_mixed_sentences_decide_per_sentence():
    """The exclusion is sentence-level: an EMS sentence does not cancel a separate patient sentence in the same excerpt."""
    assert _kind("EMS reports minimal damage. Patient states neck pain began at the scene.") == "patient_report"
    assert _kind("Per his wife, headaches began at the scene. Patient states neck pain began at the scene.") == "patient_report"


def test_d033_patient_subject_that_mentions_ems_or_family_stays_patient_report():
    """T-061 adjuster r1 major: the exclusion is anchored to the sentence subject, so the patient's own statement about EMS/family keeps its label."""
    for t in ["Patient states EMS noted a laceration.", "Patient reports his wife said he was fine.", "Patient states his wife drove him to the ER.",
              "Pt c/o neck pain; wife drove him in."]:
        assert _kind(t) == "patient_report", t
    for t in ["EMS reports minimal damage.", "Wife complains of neck pain.", "Per his wife, headaches began at the scene.",
              "Patient's wife states he had headaches."]:
        assert _kind(t) == "record", t


def test_d033_lexicon_flags_label_source_kind_by_the_same_rule():
    """flags.lexicon_flags uses grounding.has_self_report, so a wife/EMS statement never becomes a 'Patient self-report' flag."""
    import re
    from app.backend import flags as F
    src = open(F.__file__).read()
    assert "has_self_report" in src and "_PATIENT_WORDS" not in src
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:23:14.133Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q 2>&1 | tail -6; echo \"---- git status tests ----\"; git status --short tests/ app/backend/ app/llm/lexicon.yaml | head; git log --oneline -3",
 "description": "Run full unit suite on live tree and recheck git state",
 "timeout": 500000
}
````

### User / tool · 2026-11-02T02:23:31.464Z

**tool result**
````
........................................................................ [ 74%]
........................................................................ [ 83%]
........................................................................ [ 91%]
........................................................................ [ 99%]
..                                                                       [100%]
866 passed in 16.52s
---- git status tests ----
 M app/backend/pdf_text.py
 M tests/fixtures/llm/003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
 M tests/fixtures/llm/010db3ae8de16d72ea8905cdaa07781591d70092d358c0d5e73424940e3cfb33.json
 M tests/fixtures/llm/06ba451c413e5628f554f915316d53a63820f262b930020da1cd2ecb147c5fea.json
 M tests/fixtures/llm/06bbeeec2801064baeb024b1338ce8a0263644a7a2dca09efdaeed154ed50299.json
 M tests/fixtures/llm/070338b4178e1104318ebbd4481be4bca1fed8df4ac2c0acbb4fd7cc09278f46.json
 M tests/fixtures/llm/07aab6f4f7a87ed2477b3cb9ebdb02449815ddf270c7f8aafdfa3c2338c9be19.json
 M tests/fixtures/llm/0a7eff512ada0b23f5a97cb0617eb0eecc95c4a443273eaa7f2f8c60676fba86.json
 M tests/fixtures/llm/0cee28a9faf640b117982bccb05b874c1bc8b7359cd3ff5dc846f1ac8db9c8c9.json
 M tests/fixtures/llm/0e7db52d0c5b7b4b77cced05c5e9bae39d5038d4866d2baa759dd0396aa9707e.json
709397e docs(contract): review/batch and export_config (T-055, T-058)
20d866f feat(backend): draft treatment paragraph in firm voice, grounded and judged (T-059, D-031)
dbb2c66 feat(backend): batch accept of verified entries and per-case export config (T-055, T-058)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:23:49.964Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport re\np='/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r2-probe.py'\ns=open(p).read()\nanchor='    # --- adversarial: mixed sentences (one sentence, two speakers)\\n'\nextra='''    # --- adversarial: more speaker-label, abbreviation and open-set forms (second pass)\n    (\"Passenger reports patient complains of neck pain.\", \"record\", \"adv2\", \"passenger; 'complains' is a patient verb\"),\n    (\"Wife (Mrs. Ortiz) reports he complains of neck pain.\", \"record\", \"adv2\", \"'Mrs.' splits the sentence before the subject\"),\n    (\"EMS: he complains of neck pain.\", \"record\", \"adv2\", \"EMS speaker label with colon\"),\n    (\"Witness: patient states the car ran the light.\", \"record\", \"adv2\", \"witness speaker label with colon\"),\n    (\"Family: neck pain 7/10, C/O headache.\", \"record\", \"adv2\", \"family speaker label with colon; C/O hit\"),\n    (\"Per EMS report: pt c/o neck pain.\", \"record\", \"adv2\", \"'Per EMS' with colon\"),\n'''\nassert anchor in s\ns=s.replace(anchor, extra+anchor)\ns=s.replace('for g in (\"brief\", \"r1-acc\", \"r1-f3\", \"d033\", \"adv\"):','for g in (\"brief\", \"r1-acc\", \"r1-f3\", \"d033\", \"adv\", \"adv2\"):')\nopen(p,'w').write(s)\nprint(\"ok\")\nEOF\nSCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python artifacts/review-evidence/T-061-r2-probe.py \"$SCR/e1400d4\" > artifacts/review-evidence/T-061-r2-probe.txt 2>&1; echo \"exit=$?\"; grep -E \"MISS|SUMMARY|^  \" artifacts/review-evidence/T-061-r2-probe.txt; echo \"--- selfcheck reference is_patient_statement on the same adversarial set:\"; cd \"$SCR/e1400d4\" && /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nimport sys; sys.path.insert(0,'.'); sys.path.insert(0,'research')\nimport importlib.util\nspec=importlib.util.spec_from_file_location('sc','research/lexicon_selfcheck.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\nfor t in [\"EMS: pt c/o neck pain.\",\"Girlfriend reports he complains of neck pain.\",\"Co-worker reports patient c/o neck pain.\",\"Wife of 20 years and mother of two reports he complains of neck pain.\",\"C/O neck pain; wife reports headaches.\",\"EMS reports neck pain, patient states headaches.\",\"Wife (Mrs. Ortiz) reports he complains of neck pain.\",\"Passenger reports patient complains of neck pain.\"]:\n    print(m.is_patient_statement(t), '|', t)\nEOF",
 "description": "Extend probe with second adversarial set and rerun against e1400d4"
}
````

### User / tool · 2026-11-02T02:23:50.351Z

**tool result (error)**
````
Exit code 1
ok
exit=0
MISS [adv] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'EMS: pt c/o neck pain.'  (speaker-label colon; EMS is the speaker)
MISS [adv] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'Girlfriend reports he complains of neck pain.'  (family-type speaker not listed)
MISS [adv] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'Co-worker reports patient c/o neck pain.'  (non-patient speaker not listed)
MISS [adv] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'Wife of 20 years and mother of two reports he complains of neck pain.'  (word window > 3)
MISS [adv2] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'Passenger reports patient complains of neck pain.'  (passenger; 'complains' is a patient verb)
MISS [adv2] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'Wife (Mrs. Ortiz) reports he complains of neck pain.'  ('Mrs.' splits the sentence before the subject)
MISS [adv2] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'EMS: he complains of neck pain.'  (EMS speaker label with colon)
MISS [adv2] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'Witness: patient states the car ran the light.'  (witness speaker label with colon)
MISS [adv2] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'Family: neck pain 7/10, C/O headache.'  (family speaker label with colon; C/O hit)
MISS [adv] flags._flag source_kind=record          expect=patient_report  has_self_report=False | 'EMS reports neck pain, patient states headaches.'  (patient clause in EMS sentence (lost))
MISS [adv] flags._flag source_kind=patient_report  expect=record          has_self_report=True  | 'C/O neck pain; wife reports headaches.'  (patient clause then wife clause; whole sentence labelled)
SUMMARY 31/42 match expected
  brief: 6/6
  r1-acc: 10/10
  r1-f3: 4/4
  d033: 3/3
  adv: 7/13
  adv2: 1/6
--- selfcheck reference is_patient_statement on the same adversarial set:
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
TypeError: is_patient_statement() missing 2 required positional arguments: 'start' and 'end'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:24:17.372Z

**tool call — Bash**
````
{
 "command": "grep -n \"def _sentence_around\\|def _self_report\\|def has_self_report\\|_SENT_END = \\|self_report_exclude\\\": re\" app/backend/grounding.py; grep -n \"exclude_sentence:\" app/llm/lexicon.yaml; grep -n \"id: patient_reports_generic\\|id: self_reported_prior\\|id: patient_attributes_causation\" app/llm/lexicon.yaml; grep -n \"test_d033_mixed_sentences_decide_per_sentence\\|test_d033_patient_subject_that\" tests/unit/test_flags_pass.py; grep -n \"D-033\" memory/ORCHESTRATOR_DECISIONS.md | head -2; cd /Users/arsis/zlayt-pm-project && .venv/bin/python research/lexicon_selfcheck.py > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/selfcheck-r2.txt 2>&1; echo \"selfcheck exit=$?\"; tail -3 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/selfcheck-r2.txt; ls reviews/ | grep -i \"T-061\" ; test -e reviews/T-061-claims-adjuster-r2.md && echo EXISTS || echo \"r2 file absent (ok to create)\"",
 "description": "Get exact line numbers, selfcheck exit code, and check review file path"
}
````

### User / tool · 2026-11-02T02:24:17.668Z

**tool result**
````
76:    return {"hedge": hedges, "self_report": selfrep, "self_report_exclude": re.compile(scope, re.IGNORECASE) if scope else None}
177:_SENT_END = re.compile(r"[.!?](?=\s|$)|\n")
180:def _sentence_around(text: str, start: int, end: int) -> str:
188:def _self_report(text: str) -> bool:
228:def has_self_report(text: str) -> bool:
89:  exclude_sentence: '^\W*(?:(?:the|his|her|patient''s|pt''s)\s+)?(?:EMS|paramedics?|witness(?:es)?|bystanders?|wife|husband|spouse|mother|father|parents?|family|friends?|relatives?|daughter|son|sibling|caregiver|police|officer|nurse|staff)\b(?:\s+[\w''-]+){0,3}?\s+(?:reports?|reported|states?|stated|says|said|complains?|complained|c/o|describes?|described|notes?|noted|relates?|believes?|attributes?|links?|thinks?|claims?)\b|^\W*per\s+(?:the\s+|his\s+|her\s+)?(?:wife|husband|spouse|family|witness|EMS|mother|father)\b'
488:- id: self_reported_prior
738:- id: patient_attributes_causation
754:- id: patient_reports_generic
173:def test_d033_mixed_sentences_decide_per_sentence():
179:def test_d033_patient_subject_that_mentions_ems_or_family_stays_patient_report():
41:| D-033 | `patient_report` (self-report chip) applies only to explicit patient attribution ('Patient states/reports/notes', 'Pt c/o', patient-quoted speech). EMS narrative, witness, spouse/family statements and generic 'S:'/'Subjective:' headers are not patient self-report (separate or no attribution). Narrows ADR-013 / DECISIONS.md:286. | Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit. | T-036 r3 → T-061 |
selfcheck exit=0

SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 1 of 140; held-out 115/115
RESULT: PASS
T-061-claims-adjuster.md
r2 file absent (ok to create)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:24:59.148Z

**tool call — Bash**
````
{
 "command": "grep -n 'code sets source_kind' app/llm/lexicon.yaml; grep -n \"source_kind = \\\"patient_report\\\" is set by code\" memory/DECISIONS.md; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$SCR/e1400d4\" && /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nimport sys; sys.path.insert(0,'.')\nfrom app.backend import grounding as g\nfor t in [\"Wife (Mrs. Ortiz) reports he complains of neck pain.\", \"EMS: he complains of neck pain.\", \"Family: neck pain 7/10, C/O headache.\"]:\n    lex=g._lexicon()\n    for rid, rx in lex[\"self_report\"].items():\n        for m in rx.finditer(t):\n            s=g._sentence_around(t,m.start(),m.end())\n            print(repr(t), '| hit', repr(m.group(0)), '| sentence', repr(s), '| excluded', bool(lex[\"self_report_exclude\"].search(s)))\nEOF",
 "description": "Confirm exact spec-text lines and sentence-split mechanism for two probe cases"
}
````

### User / tool · 2026-11-02T02:24:59.348Z

**tool result**
````
84:# T-061: a self_report hit is a PATIENT statement only. Before the code sets source_kind = patient_report, it must drop the hit
'Wife (Mrs. Ortiz) reports he complains of neck pain.' | hit 'he complains' | sentence ' Ortiz) reports he complains of neck pain' | excluded False
'EMS: he complains of neck pain.' | hit 'he complains' | sentence 'EMS: he complains of neck pain' | excluded False
'Family: neck pain 7/10, C/O headache.' | hit 'C/O' | sentence 'Family: neck pain 7/10, C/O headache' | excluded False
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:25:03.563Z

**tool call — Bash**
````
{
 "command": "sed -n 23,27p app/llm/lexicon.yaml; echo ...; sed -n 82,88p app/llm/lexicon.yaml",
 "description": "Read the lexicon header lines that state the source_kind rule"
}
````

### User / tool · 2026-11-02T02:25:03.656Z

**tool result**
````
#   accident_date_provenance.
# - `hedge: true` marks the R-TL-8 hedge set: a sentence with a hedge hit is a qualifier unit and can never be cut
#   from an excerpt (ADR-016). `self_report: true` marks wording that explicitly attributes a statement to the PATIENT (T-061); code sets
#   source_kind = "patient_report" from it (ADR-013). Self-report entries are never hedges.
# - `strength`: high and medium raise a flag (origin lexicon, or lexicon+llm). low is context only: it never
...
    The no-show entry matches only "did not show up/for".

# T-061: a self_report hit is a PATIENT statement only. Before the code sets source_kind = patient_report, it must drop the hit
# when the hit's sentence matches `self_report_scope.exclude_sentence` (a named non-patient speaker with a speech verb, or
# "per <wife|husband|EMS|...>"). Bare "S:", "Subjective:" and "Self-reported" headers are not matched by any self_report entry,
# and the intake-form date entry is self_report: false. Reference implementation: research/lexicon_selfcheck.py:is_patient_statement().
self_report_scope:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:25:53.275Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster-r2.md",
 "content": "# T-061 round 2: self-report label precision, claims-adjuster review (Gary Pruitt)\n\nVerdict: **fail** (2 blockers, 2 majors, 2 minors). Reviewed object: commit e1400d4 (backend round 2, on top of dd545e3). Git archive of e1400d4 and the live tree are identical for every reviewed file (grounding.py, flags.py, lexicon.yaml, test_flags_pass.py, research/lexicon_selfcheck.py). HEAD has since moved to 709397e; the live tree is still moving, so this review pins e1400d4.\n\nRound 1 status (reviews/T-061-claims-adjuster.md):\n- r1 blocker, EMS/witness/wife/family complaints labelled \"Patient self-report\": **closed for the phrasings r1 listed** (probe rows: 10/10 expected). The class is not closed: findings 1 and 2 below.\n- r1 major, test_flags_pass.py red: **closed**. `-k \"flag or lexicon\"` gives 121 passed; full `tests/unit` gives 866 passed on the live tree.\n- r1 major, over-exclusion of patient sentences naming EMS or a wife: **closed** for both r1 sentences (4/4 r1-f3 rows). Finding 3 is the mirror image.\n- r1 minor, superseded spec text: **still open** (finding 5).\n\nWhat e1400d4 does: `grounding._self_report` now returns True only when a lexicon self_report hit exists AND the hit's sentence does not match `self_report_scope.exclude_sentence` (grounding.py:188-197; lexicon.yaml:89). `_SELF`, `_PATIENT_WORDS` and `_NOT_PATIENT_STATEMENT` are gone (grep: none). `flags.py:46` and `flags.py:125` call `has_self_report`. The brief's six script-checks pass through the production constructor (6/6).\n\nFindings:\n\n1. **Blocker. Non-patient speakers in colon, abbreviation and long-subject forms are labelled patient_report.** Evidence: `artifacts/review-evidence/T-061-r2-probe.txt`, rows MISS:\n   - `EMS: pt c/o neck pain.` gives patient_report.\n   - `EMS: he complains of neck pain.` gives patient_report.\n   - `Witness: patient states the car ran the light.` gives patient_report.\n   - `Family: neck pain 7/10, C/O headache.` gives patient_report.\n   - `Wife of 20 years and mother of two reports he complains of neck pain.` gives patient_report.\n   - `Wife (Mrs. Ortiz) reports he complains of neck pain.` gives patient_report.\n   Cause: lexicon.yaml:89 needs `\\s+` directly after the speaker word, so a colon fails it, and it allows at most three words before the verb. grounding.py:177 `_SENT_END` splits at \"Mrs.\"; for the Mrs. row the anchored sentence is ` Ortiz) reports he complains of neck pain`, and `excluded` is False (run on the e1400d4 archive).\n   Why it matters: D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) says EMS narrative, witness and spouse/family statements are not patient self-report. The round-1 blocker was this same mislabel, and its acceptance list only covered the no-colon forms. The \"EMS:\" and \"Witness:\" speaker-label forms are standard in clinical notes, so the chip still tells the reader the claimant said what EMS or a witness said.\n   Fix: anchor the exclusion to the clause, not to a whitespace-and-three-word window. Allow `:` or `-` after the speaker word and a parenthesised descriptor before the verb. Split sentences at abbreviations (Mr., Mrs., Ms., Dr., Pt.) before the anchor is applied.\n   Acceptance test: the six rows above return record in flags._flag. `Patient states EMS noted a laceration.`, `Pt c/o neck pain; wife drove him in.` and `Patient states his wife drove him to the ER.` stay patient_report. `.venv/bin/python research/lexicon_selfcheck.py` still PASS.\n\n2. **Blocker. A spouse or family clause inside a patient-subject sentence inherits \"Patient self-report\".** Evidence: probe row `C/O neck pain; wife reports headaches.` gives source_kind patient_report. The sentence contains a wife statement, and the excerpt carries the chip. The team's test `tests/unit/test_flags_pass.py:173-177` (test_d033_mixed_sentences_decide_per_sentence) pins per-sentence behaviour only with separate sentences, so the same-sentence case is not covered.\n   Why it matters: D-033 says spouse and family statements are not patient self-report, and it names this exact error (\"Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit\"). The wife's headache complaint is quoted verbatim in an excerpt that tells the reader the claimant reported it.\n   Fix: one boolean per excerpt cannot be right for a mixed excerpt. The architect chooses one of two. (a) Split the flag so each excerpt has one speaker; this is preferred. (b) Label any excerpt containing a non-patient speaker clause as record. Under (b) the patient's own clause loses its chip, which is finding 3's harm and which I accept as the lesser harm.\n   Acceptance test: under (a), `C/O neck pain; wife reports headaches.` yields no patient_report flag whose text contains \"wife reports headaches\", and the \"C/O neck pain\" flag stays patient_report. Under (b), the same sentence yields record. test_flags_pass.py:173-177 is updated to match whichever is chosen.\n\n3. **Major. A patient clause inside an EMS-subject sentence loses its attribution.** Evidence: probe row `EMS reports neck pain, patient states headaches.` gives record. The clause `patient states headaches` is explicit patient attribution (D-033 lists 'Patient states' as patient_report).\n   Cause: lexicon.yaml:89 anchors on the sentence start `EMS reports` and excludes the whole sentence, so the patient clause is dropped (grounding.py:188-197).\n   Why it matters: this is the opposite direction from round-1 finding 3. Under-attribution is the lesser harm, so this is major and not blocker. It is the same design gap as finding 2 and is resolved by the same choice: under (a) the patient clause gets its own flag.\n   Fix: as finding 2. Acceptance test: under (a), `patient states headaches` is patient_report on its own flag. Under (b), the sentence is record and the trade-off is written into the D-entry.\n\n4. **Major, pending Chris's ruling. Third-party speakers outside the closed list are labelled patient_report.** Evidence: probe rows `Girlfriend reports he complains of neck pain.`, `Co-worker reports patient c/o neck pain.` and `Passenger reports patient complains of neck pain.` all give patient_report. Several records pass only by accident: `Passenger reports patient complained of neck pain.` gives record only because 'complained' is not in patient_reports_generic (lexicon.yaml:754-755), and `Triage nurse reports he is in pain.` has no self_report hit at all. Neither result comes from the exclusion.\n   Why it matters: the exclusion is a closed word list (lexicon.yaml:89). D-033's positive rule is that patient_report \"applies only to explicit patient attribution\". If that rule means the clause's speaker must be the patient or a quoted patient, these three rows are a blocker. If D-033's list (EMS, witness, spouse/family) is closed, they are not covered and need a ruling. I have rated this major and put the question to Chris.\n   Fix: either state the rule as subject-based (the speaker of the clause is the patient or a quoted patient) and apply it to any speaker, or add the named speakers after a ruling. Acceptance test: the three rows return record, or Chris's ruling is written into D-033 and the test pins it.\n\n5. **Minor. Spec text still states the superseded rule (round-1 finding 4, unchanged).** Evidence: memory/DECISIONS.md:286 reads \"`source_kind = \"patient_report\"` is set by code from the lexicon `self_report` entries on the excerpt\". app/llm/lexicon.yaml:25-26 reads \"code sets source_kind = \"patient_report\" from it (ADR-013)\". The exclusion rule appears only in the T-061 note at lexicon.yaml:84-87.\n   Fix: architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to \"self_report entries that name the patient, minus self_report_scope.exclude_sentence\".\n   Acceptance test: `grep -n \"from the lexicon \\`self_report\\` entries on the excerpt\" memory/DECISIONS.md` returns nothing, and the lexicon header names self_report_scope.\n\n6. **Minor. The held-out set has no patient-subject sentence naming a family or EMS member (round-1 finding 3, coverage half).** Evidence: `grep -n -i` for a patient subject followed by EMS, wife, witness, family, husband or spouse in evals/lexicon_heldout.jsonl (115 rows) returns none. The unit test at test_flags_pass.py:179-187 covers it, so the regression is caught, but selfcheck PASS cannot show it.\n   Fix: add 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' to evals/lexicon_heldout.jsonl (researcher-owned).\n   Acceptance test: both sentences appear in evals/lexicon_heldout.jsonl with expected patient_report, and selfcheck PASS.\n\nWhat is not a finding: `Per EMS, pt. c/o neck pain.` and `EMS noted pt. reports neck pain 7/10.` both give record. I expected the \"pt.\" abbreviation to split the sentence, but the match starts at \"pt. c/o\", so the anchor still sees \"Per EMS\". Checked by running the function directly.\n\nOutside my lens: the selfcheck's is_patient_statement reference implementation (I did not compare its output on the adversarial set); the rest of the test suite beyond the 866-pass count.\n\nExercised:\n- Read personas/claims-adjuster.md (full); my memory index and the round-1 memory files; reviews/T-061-claims-adjuster.md (round 1, full); `python3 tools/board.py show T-061`; D-033 at memory/ORCHESTRATOR_DECISIONS.md:41.\n- `.venv/bin/python research/lexicon_selfcheck.py | tail -3` gave `SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 1 of 140; held-out 115/115` and `RESULT: PASS`. A separate run with output to a file gave exit 0.\n- `.venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\" 2>&1 | tail -2` gave `121 passed, 745 deselected in 2.06s`. An earlier run in this review, at HEAD 4eebb2d, gave `120 passed, 731 deselected in 1.79s`; the count moved because the tree moved.\n- `.venv/bin/python -m pytest tests/unit -q` gave `866 passed in 16.52s` (live tree).\n- `git log --oneline -6`; `git show --stat e1400d4` (grounding.py, lexicon.yaml, test_flags_pass.py only); `git merge-base --is-ancestor dd545e3 HEAD` (ancestor); `git status --short -- app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py research evals app/llm` (no diffs on reviewed paths); `cmp` of the five reviewed files, live vs the e1400d4 archive (identical).\n- `git archive e1400d4` extracted to the session scratchpad; the probe ran against that archive.\n- `.venv/bin/python artifacts/review-evidence/T-061-r2-probe.py <archive>` gave `SUMMARY 31/42 match expected`, with brief 6/6, r1-acc 10/10, r1-f3 4/4, d033 3/3, adv 7/13, adv2 1/6. The probe calls flags._flag (flags.py:42, the constructor that sets source_kind at flags.py:46) and grounding.has_self_report. Output: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r2-probe.txt`.\n- Ran `_sentence_around` and the exclusion regex directly on the three misses (Mrs., EMS colon, Family colon) to confirm the mechanism.\n- `grep -n \"_SELF\\b\\|_PATIENT_WORDS\\|_NOT_PATIENT_STATEMENT\" app/backend/grounding.py` gave no output. `grep -n` for \"code sets source_kind\" gave lexicon.yaml:84 and lines 25-26 (wrapped). DECISIONS.md:286 read with `sed`.\n- `grep -n -i` on evals/lexicon_heldout.jsonl for patient-subject sentences naming EMS, wife, witness, family, husband or spouse: no output.\n- Read tests/unit/test_flags_pass.py:95-190 and lexicon.yaml lines 23-27 and 82-93.\n\n```json\n{\"card\": \"T-061\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit e1400d4 (T-061 round 2 backend: grounding.py, lexicon.yaml exclude_sentence, test_flags_pass.py), reviewed via git archive; live tree identical for those paths; HEAD 709397e not reviewed; spec memory/DECISIONS.md:286 and D-033 at memory/ORCHESTRATOR_DECISIONS.md:41; no app URL (flag and lexicon layer, no UI in scope); sample probes in artifacts/review-evidence/T-061-r2-probe.py.\",\n \"exercised\": [\n  \"Read personas/claims-adjuster.md in full; memory index and round-1 memory files; reviews/T-061-claims-adjuster.md in full; python3 tools/board.py show T-061; D-033 (ORCHESTRATOR_DECISIONS.md:41)\",\n  \".venv/bin/python research/lexicon_selfcheck.py | tail -3 -> SUMMARY golden MUST 11/11, held-out 115/115, FN 1 of 140; RESULT: PASS; separate run exit 0\",\n  \".venv/bin/python -m pytest tests/unit -q -k 'flag or lexicon' 2>&1 | tail -2 -> 121 passed, 745 deselected\",\n  \".venv/bin/python -m pytest tests/unit -q -> 866 passed (live tree)\",\n  \"git log --oneline -6; git show --stat e1400d4; git merge-base --is-ancestor dd545e3 HEAD; git status --short on reviewed paths (no diffs); cmp of five reviewed files live vs git archive e1400d4 (identical)\",\n  \"git archive e1400d4 extracted to session scratchpad; artifacts/review-evidence/T-061-r2-probe.py run against it -> artifacts/review-evidence/T-061-r2-probe.txt (42 sentences through flags._flag and grounding.has_self_report: 31/42; 11 misses = findings 1-4)\",\n  \"direct run of grounding._sentence_around and lexicon self_report_exclude on 'Wife (Mrs. Ortiz) reports he complains of neck pain.', 'EMS: he complains of neck pain.', 'Family: neck pain 7/10, C/O headache.'\",\n  \"grep -n _SELF|_PATIENT_WORDS|_NOT_PATIENT_STATEMENT app/backend/grounding.py -> none; grep -n 'code sets source_kind' app/llm/lexicon.yaml -> 84 (+ wrapped 25-26); sed -n 286p memory/DECISIONS.md\",\n  \"grep -n -i patient-subject + EMS/wife/witness/family/husband/spouse evals/lexicon_heldout.jsonl -> none (115 rows)\",\n  \"read tests/unit/test_flags_pass.py:95-190 and app/llm/lexicon.yaml:23-27, 82-93, 488-493, 738-759\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"attribution_precision_production\": 2, \"lexicon_scope_logic\": 2, \"ac2_flags_wiring\": 4, \"test_honesty\": 3, \"spec_consistency\": 3},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"Non-patient speakers in colon, abbreviation and long-subject forms still labelled patient_report\",\n   \"evidence\": \"artifacts/review-evidence/T-061-r2-probe.txt MISS rows: 'EMS: pt c/o neck pain.', 'EMS: he complains of neck pain.', 'Witness: patient states the car ran the light.', 'Family: neck pain 7/10, C/O headache.', 'Wife of 20 years and mother of two reports he complains of neck pain.', 'Wife (Mrs. Ortiz) reports he complains of neck pain.' each give source_kind patient_report. Cause: app/llm/lexicon.yaml:89 requires \\\\s+ directly after the speaker word (colon fails) and allows at most 3 words before the verb; app/backend/grounding.py:177 _SENT_END splits at 'Mrs.', so the anchored sentence is ' Ortiz) reports he complains of neck pain' and excluded is False (archive e1400d4).\",\n   \"why_it_matters\": \"D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) says EMS narrative, witness and spouse/family statements are not patient self-report. This is the round-1 blocker class in forms its acceptance list did not cover. The chip tells the reader the claimant said what EMS, a witness or a spouse said.\",\n   \"fix\": \"Anchor the exclusion to the clause rather than a whitespace-and-3-word window: allow ':' or '-' after the speaker word and a parenthesised descriptor before the verb; split sentences at abbreviations (Mr., Mrs., Ms., Dr., Pt.) before the anchor.\",\n   \"acceptance_test\": \"The six rows above return record via flags._flag. 'Patient states EMS noted a laceration.', 'Pt c/o neck pain; wife drove him in.' and 'Patient states his wife drove him to the ER.' stay patient_report. .venv/bin/python research/lexicon_selfcheck.py still PASS.\"},\n  {\"severity\": \"blocker\",\n   \"title\": \"A spouse or family clause inside a patient-subject sentence inherits 'Patient self-report'\",\n   \"evidence\": \"artifacts/review-evidence/T-061-r2-probe.txt: 'C/O neck pain; wife reports headaches.' gives source_kind patient_report. tests/unit/test_flags_pass.py:173-177 (test_d033_mixed_sentences_decide_per_sentence) pins per-sentence behaviour only for separate sentences.\",\n   \"why_it_matters\": \"D-033 says spouse and family statements are not patient self-report and names this error: 'Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit.' The wife's headache complaint is quoted verbatim in an excerpt whose chip credits the claimant.\",\n   \"fix\": \"Architect chooses: (a) split the flag so each excerpt has one speaker (preferred); or (b) label any excerpt containing a non-patient speaker clause as record, accepting that the patient clause loses its chip (finding 3).\",\n   \"acceptance_test\": \"Under (a): 'C/O neck pain; wife reports headaches.' yields no patient_report flag whose text contains 'wife reports headaches', and the 'C/O neck pain' flag stays patient_report. Under (b): the sentence yields record. test_flags_pass.py:173-177 updated to the chosen rule.\"},\n  {\"severity\": \"major\",\n   \"title\": \"A patient clause inside an EMS-subject sentence loses its attribution\",\n   \"evidence\": \"artifacts/review-evidence/T-061-r2-probe.txt: 'EMS reports neck pain, patient states headaches.' gives record. Cause: app/llm/lexicon.yaml:89 anchors on the sentence start 'EMS reports' and excludes the whole sentence (grounding.py:188-197).\",\n   \"why_it_matters\": \"Explicit patient attribution ('Patient states') is dropped. This is the opposite direction from round-1 finding 3; under-attribution is the lesser harm, so major and not blocker. Same design gap as finding 2.\",\n   \"fix\": \"Resolved by the same choice as finding 2: under (a) the patient clause gets its own flag.\",\n   \"acceptance_test\": \"Under (a): 'patient states headaches' is patient_report on its own flag. Under (b): the sentence is record and the trade-off is written into the D-entry.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Third-party speakers outside the closed word list are labelled patient_report (pending Chris's ruling)\",\n   \"evidence\": \"artifacts/review-evidence/T-061-r2-probe.txt: 'Girlfriend reports he complains of neck pain.', 'Co-worker reports patient c/o neck pain.', 'Passenger reports patient complains of neck pain.' each give patient_report. lexicon.yaml:89 is a closed word list. 'Passenger reports patient complained of neck pain.' passes only because 'complained' is absent from patient_reports_generic (lexicon.yaml:754-755), not because of the exclusion.\",\n   \"why_it_matters\": \"D-033 says patient_report 'applies only to explicit patient attribution'. If that means the clause's speaker must be the patient or a quoted patient, these rows are a blocker. If D-033's named list (EMS, witness, spouse/family) is closed, the question is open and needs a ruling.\",\n   \"fix\": \"Either state the rule as subject-based and apply it to any speaker, or add named speakers after Chris's ruling and write it into D-033.\",\n   \"acceptance_test\": \"The three rows return record, or Chris's ruling is in D-033 and the test pins it.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Spec text still states the superseded rule (round-1 finding 4, unchanged)\",\n   \"evidence\": \"memory/DECISIONS.md:286: '`source_kind = \\\\\\\"patient_report\\\\\\\"` is set by code from the lexicon `self_report` entries on the excerpt'. app/llm/lexicon.yaml:25-26: 'code sets source_kind = \\\\\\\"patient_report\\\\\\\" from it (ADR-013)'. The exclusion rule appears only in the T-061 note at lexicon.yaml:84-87.\",\n   \"why_it_matters\": \"A future reader gets two rules: the spec says every self_report hit counts, and the code applies an exclusion the spec does not mention.\",\n   \"fix\": \"Architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to 'self_report entries that name the patient, minus self_report_scope.exclude_sentence'.\",\n   \"acceptance_test\": \"grep for 'from the lexicon `self_report` entries on the excerpt' in memory/DECISIONS.md returns nothing; the lexicon header names self_report_scope.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Held-out set has no patient-subject sentence naming a family or EMS member (round-1 finding 3, coverage half)\",\n   \"evidence\": \"grep -n -i for patient subject + EMS/wife/witness/family/husband/spouse in evals/lexicon_heldout.jsonl (115 rows): no output. Unit test test_flags_pass.py:179-187 covers the case.\",\n   \"why_it_matters\": \"The unit test catches a regression, but selfcheck PASS cannot show one, so the research gate is blind to this class.\",\n   \"fix\": \"Add 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' to evals/lexicon_heldout.jsonl (researcher-owned).\",\n   \"acceptance_test\": \"Both sentences appear in evals/lexicon_heldout.jsonl with expected patient_report, and selfcheck PASS.\"}\n ],\n \"whats_right\": [\n  \"Round-1 blocker phrasings are record through the production constructor: 'EMS complains of neck pain 7/10.', 'Witness complains of neck pain.', 'Wife complains of neck pain.', 'Family complains of neck pain.', 'Date of accident per intake form: 2026-01-19.' (10/10 r1 rows), and the brief's six script-checks pass (6/6).\",\n  \"Round-1 over-exclusion is fixed: 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' stay patient_report, and the full tests/unit run is green at 866 passed.\",\n  \"Bare 'S:', 'Subjective:' and 'Self-reported' headers are record, and the intake-form date is self_report: false, so the D-033 header rule holds with the verbatim marker still in the excerpt.\"\n ],\n \"questions_for_chris\": [\n  \"Is D-033's speaker list closed? Are a girlfriend or partner, a co-worker and a passenger 'family' or 'witness' for D-033 (finding 4)? If D-033 means the clause's speaker must be the patient, finding 4 is a blocker.\",\n  \"For mixed excerpts (findings 2 and 3), do you prefer per-speaker flag splitting (a) or labelling mixed excerpts record (b), accepting that the patient clause loses its chip?\",\n  \"The review object is e1400d4 via git archive, identical to the live tree for reviewed paths. HEAD is now 709397e and the live tree is moving (the -k count moved from 120 to 121 between two runs in this review). Should the gate review e1400d4 or a later commit?\",\n  \"The persona file expects model claude-opus-5-5 in the review record. I ran as claude-haiku-5-5 and wrote that id, as in round 1. Confirm that is acceptable for the gate.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:25:53.430Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:25:57.192Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport json,re\ns=open('reviews/T-061-claims-adjuster-r2.md',encoding='utf-8').read()\nblocks=re.findall(r\"```json\\n(.*?)\\n```\", s, re.S)\nprint(\"json blocks:\", len(blocks))\nd=json.loads(blocks[0])\nsev=[f[\"severity\"] for f in d[\"findings\"]]\nprint(\"verdict:\", d[\"verdict\"], \"| severities:\", sev, \"| model:\", d[\"model\"], \"| card:\", d[\"card\"])\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict rule expects:\", exp, \"OK\" if exp==d[\"verdict\"] else \"MISMATCH\")\nprint(\"whats_right:\", len(d[\"whats_right\"]))\nEOF\ngrep -c \"\" reviews/T-061-claims-adjuster-r2.md",
 "description": "Validate the JSON block and verdict rule in the r2 review"
}
````

### User / tool · 2026-11-02T02:25:57.307Z

**tool result**
````
json blocks: 1
verdict: fail | severities: ['blocker', 'blocker', 'major', 'major', 'minor', 'minor'] | model: claude-haiku-5-5 | card: T-061
verdict rule expects: fail OK
whats_right: 3
132
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:26:03.832Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_t061_r2_speaker_scope.md",
 "content": "---\nname: t061-speaker-scope-closed-list\ndescription: T-061 r2 (e1400d4): patient_report exclusion is a closed speaker word list with a 3-word window and sentence split; colon labels, Mrs. split, mixed sentences still leak\nmetadata:\n  type: project\n---\n\nThe self-report exclusion (`self_report_scope.exclude_sentence`, app/llm/lexicon.yaml:89) only recognises a short closed list of\nnon-patient speakers, requires whitespace right after the speaker word, allows at most 3 words before the speech verb, and is applied to\nthe sentence found by grounding `_SENT_END` (which splits at \"Mrs.\", \"Dr.\", \"Pt.\"). Round 2 (e1400d4) still labels as patient_report:\n\"EMS: pt c/o neck pain.\", \"Family: neck pain 7/10, C/O headache.\", \"Wife (Mrs. Ortiz) reports he complains of neck pain.\", \"C/O neck pain;\nwife reports headaches.\", plus unlisted speakers \"Girlfriend reports he complains...\", \"Co-worker reports patient c/o...\".\nIt also drops the patient clause in \"EMS reports neck pain, patient states headaches.\" (record).\n\n**Why:** D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) binds: spouse/family/EMS/witness statements are not patient self-report. The\nround-1 blocker was the EMS/wife mislabel; its acceptance list only covered no-colon phrasings, so the class leaked in other forms.\n\n**How to apply:** when re-reviewing T-061 or any attribution/label fix, do not stop at the phrasings the card's acceptance test lists.\nGenerate variants (speaker-label colon, abbreviation before the subject, descriptor before the verb, mixed clause in one sentence,\nunlisted noun) and run them through the production constructor (flags._flag -> grounding.has_self_report). Probe script:\nartifacts/review-evidence/T-061-r2-probe.py (run against a `git archive` of the commit). Still open at last review: findings 1-6 in\nreviews/T-061-claims-adjuster-r2.md; check whether a later round closed them before reusing this.\n"
}
````

### User / tool · 2026-11-02T02:26:03.975Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_t061_r2_speaker_scope.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:26:06.365Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer && .venv/bin/python - <<'EOF' 2>/dev/null || python3 - <<'EOF2'\nEOF\nimport pathlib\np=pathlib.Path('/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md')\ns=p.read_text()\nline=\"- [T-061 r2 speaker scope](project_t061_r2_speaker_scope.md) — closed speaker list + 3-word window leaks colon labels, Mrs. split, mixed sentences; test variants, not just listed phrasings\\n\"\nif \"project_t061_r2_speaker_scope.md\" not in s:\n    s=s.rstrip(\"\\n\")+\"\\n\"+line\n    p.write_text(s)\nprint(s)\nEOF2",
 "description": "Add index line for new reviewer memory entry"
}
````

### User / tool · 2026-11-02T02:26:06.476Z

**tool result**
````
- [Lexicon review method](feedback_lexicon_review_method.md) — selfcheck PASS hides recall gaps; rerun probe script; must-probe constructions
- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 r1-r4: omissions, invented Rivera facts, partial scope fixes (line 34 left open at r4); sweep prose + golden must-not regex
- [Flag-pass review patterns](project_flag_pass_review_patterns.md) — T-036 r0: vacuous guard test, silent-empty conflict pass, worker skipped full suite
- [source_kind history and run signal](project_flag_source_kind_and_run_signal.md) — T-036 r2/r3 word filter; T-061 r0 (dd545e3) lexicon narrowed but AC2 flags/grounding wiring not done, exclude regex over-broad
- [Review the commit, not the dirty tree](feedback_review_commit_not_worktree.md) — git archive the sha when working tree has uncommitted edits to reviewed files
- [T-036 r4 split and judge fixtures](project_t036_r4_split_and_judge_fixtures.md) — self-report split to T-061; committed judge fixtures don't replay (JUDGE_UNAVAILABLE); r4 verdict changes
- [T-061 r2 speaker scope](project_t061_r2_speaker_scope.md) — closed speaker list + 3-word window leaks colon labels, Mrs. split, mixed sentences; test variants, not just listed phrasings
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:26:09.702Z

T-061 r2 verdict: **fail**. Two blockers: "EMS: pt c/o…", "Family: …", and "Wife (Mrs. Ortiz) reports…" are still labelled patient_report, and "C/O neck pain; wife reports headaches." labels the wife clause as patient. Majors: "EMS reports…, patient states headaches." loses the patient attribution, and unlisted speakers (girlfriend, co-worker) are labelled patient. Full review: /Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster-r2.md
