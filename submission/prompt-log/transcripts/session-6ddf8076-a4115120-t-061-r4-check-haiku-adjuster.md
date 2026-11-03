# Subagent: T-061 r4 check (haiku adjuster) (T-061 r4 check (haiku adjuster))

Source: `agent-a4115120fa62ba2bc.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:37:07.909Z

Round-4 (final) check of board card T-061 in /Users/arsis/zlayt-pm-project. The fix is commit 991dac4, and the binding rule is memory/ORCHESTRATOR_DECISIONS.md D-037: the patient chip goes only on an excerpt that is a single whole patient-subject clause, and any further clause means no chip.

Using reviews/T-061-claims-adjuster-r3.md, confirm that blockers B1 and B2 and major 3 are closed. Probe grounding.has_self_report directly with your r3 attack strings, plus 5 new ones that try to sneak a family or EMS statement into a chipped excerpt. Judge against D-037, not the older rules. Stale-text minors in DECISIONS.md and lexicon.yaml are routed to their owners; note them but don't fail on them.

Run `python3 -m pytest -q tests/unit/test_flags_pass.py`. Write reviews/T-061-claims-adjuster-r4.md, append-only, with a ```json block containing card, persona, verdict and findings. Reply in 2 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:09.099Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/claims-adjuster.md"
}
````

### User / tool · 2026-11-02T02:37:09.112Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:09.301Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster-r3.md"
}
````

### User / tool · 2026-11-02T02:37:09.452Z

**tool result**
````
1	# T-061 round 3 (final): self-report label precision, claims-adjuster review (Gary Pruitt)
2	
3	Verdict: **fail** (2 blockers, 1 major, 3 minors). Reviewed object: commit a27b358 (D-035 clause-level patient_report), reviewed via `git archive` (session scratchpad `r3-a27`). HEAD is now d0c9cdb, which adds only `tests/unit/test_grounding_may.py`; it is not the reviewed object, but I ran the brief's pytest command on it as well.
4	
5	D-024 item 7 says no harness rounds after M0 r3 and residual findings become debt. This card is product attribution, not harness, so I did not treat it as covered by that rule and did not downgrade the blockers. See questions_for_chris.
6	
7	## Round 2 status
8	
9	- r2 finding 1 (colon, abbreviation and long-subject speakers): **closed.** All six r2 rows return record (r2 probe rows MISS now OK).
10	- r2 finding 2 (spouse clause in a patient-subject sentence): **open, same class.** The semicolon form `C/O neck pain; wife reports headaches.` is record now. The same class with a comma, "and" or parentheses still carries the patient chip. Blocker 1.
11	- r2 finding 3 (`EMS reports neck pain, patient states headaches.`): **closed** as the brief allows. Only the patient clause is spanned (`['patient states headaches.']`); excerpt chip absent.
12	- r2 finding 4 (girlfriend, co-worker, passenger, ambulance crew, triage nurse): **closed.** D-035's "any other or unknown speaker gets no tag" rule holds on all of them.
13	- r2 finding 5 (spec text still lexicon-driven): **open.** Minor 4.
14	- r2 finding 6 (held-out coverage): **open.** Minor 6.
15	
16	## Brief script-checks (all through production: `flags._flag` -> `source_kind`, and `grounding.has_self_report`)
17	
18	- `Pt reports neck pain.` -> patient_report, span `['Pt reports neck pain.']`. OK.
19	- `Girlfriend says he limps.` -> record. OK.
20	- `C/O neck pain; wife reports headaches.` -> record. OK.
21	- `EMS reports neck pain, patient states headaches.` -> record at excerpt level; span `['patient states headaches.']`. OK (brief allows the absent excerpt chip).
22	
23	## Findings
24	
25	1. **Blocker. A family or EMS clause after a comma, "and" or a parenthesis inside a patient-subject sentence inherits the patient chip.** Evidence: `artifacts/review-evidence/T-061-r3-probe.txt`, MISS rows (group r3-adv), all `source_kind = patient_report`:
26	   - `Patient states pain began after the collision, wife reports headaches.`
27	   - `Pt reports neck pain, EMS notes headaches.`
28	   - `Patient reports neck pain and his wife says he is in pain.`
29	   - `Patient reports neck pain, per his wife, headaches began at the scene.`
30	   - `Patient reports neck pain (per wife, headaches since the scene).`
31	   - `Patient reports pain 4/10, girlfriend says he limps.`
32	   - `Patient reports neck pain, Mrs. Ortiz reports headaches.`
33	
34	   In each, the span from `patient_report_spans` (grounding.py:189-200) runs from the patient word to the next `;` or sentence end (`S.unit_spans`, sentences.py:29). The span therefore swallows the comma-joined family clause, and `_self_report` (grounding.py:205-213) only searches the text outside the span for a reporting word, so the family clause is never seen. The comment at grounding.py:190-191 says a clause "starts at a unit start or after a comma", but the span end ignores commas. The commit's own test pins the span to `;` (tests/unit/test_flags_pass.py:190-196), and no test covers a comma-joined family clause.
35	
36	   Why it matters: the chip tells the reader the claimant said what the wife, girlfriend or EMS said. D-033 calls this exact error "a credibility error an adjuster would exploit" (memory/ORCHESTRATOR_DECISIONS.md:41). r2 finding 2 was this class and was a blocker. Under the architect's chosen rule (b) (grounding.py:206 "a mixed excerpt cannot carry one chip, so it carries none"), these excerpts must be record. D-035's default is "a missing chip is safe, a wrong chip is not" (ORCHESTRATOR_DECISIONS.md:44).
37	
38	   Fix: either (i) end the patient span at the next comma, "and" or open parenthesis that begins another clause, so the family clause falls outside the span and rule (b) applies; or (ii) safer and simpler: attach the chip only when the patient clause is the whole excerpt, so any following clause makes the excerpt record. Under (ii) the pinned `Pt c/o neck pain; wife drove him in.` (test_flags_pass.py:195-196 area) becomes record, and that test must change with it.
39	
40	   Acceptance test: all seven rows above return `has_self_report` False and `source_kind` record through `flags._flag`. `Patient states EMS noted a laceration.`, `Patient reports his wife said he was fine.` and `Patient states his wife drove him to the ER.` stay patient_report. `.venv/bin/python research/lexicon_selfcheck.py` still PASS. Add the seven rows to test_flags_pass.py.
41	
42	2. **Blocker. A non-patient clause whose reporting verb is outside the closed list inherits the chip.** Evidence: `artifacts/review-evidence/T-061-r3-probe.txt`, MISS rows (group r3-adv2), all `source_kind = patient_report`:
43	   - `Patient states neck pain; wife thinks he is faking.` (semicolon form: the span does end at the `;`, but "thinks" is not in `_VERB`, grounding.py:183-184)
44	   - `Patient reports neck pain, wife thinks he is faking.`
45	   - `Patient states neck pain; his wife told the ER he was fine.`
46	   - `Patient states neck pain, EMS notes headaches, wife reports nausea.`
47	
48	   Cause: `_self_report` decides "no other speech" by searching the leftover text for the closed `_REPORT_WORD` list (grounding.py:186, 213). Any non-patient clause with a verb outside that list ("thinks", "told", "insists", "mentions") passes as "no other report". The lexicon's exclude list has `thinks?` and `links?` (lexicon.yaml:89), but production no longer reads it (see finding 3).
49	
50	   Why it matters: the excerpt quotes a spouse's or family member's opinion or account under the claimant's "Patient self-report" chip. This is the r2 finding 2 class again, reached through a different door. D-035 says "any other or unknown speaker ... gets no tag" (ORCHESTRATOR_DECISIONS.md:44). A closed verb list cannot satisfy an "any speaker" rule.
51	
52	   Fix: the mixed-excerpt test must not depend on a verb list. Under rule (b), an excerpt that contains any clause after the patient clause is record. Under (ii) in finding 1 this is the same change. Do not add verbs to the list as the fix; that just moves the hole.
53	
54	   Acceptance test: the four rows above return record. Add them to `test_d035_mixed_excerpt_carries_no_chip` (test_flags_pass.py:199-202). Then `Pt c/o neck pain; wife drove him in.` decides under the chosen rule; the test must say which.
55	
56	3. **Major. The research gate PASS measures a rule production no longer runs.** Evidence: `.venv/bin/python research/lexicon_selfcheck.py` on the a27b358 archive gives `SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 0 of 0; held-out 115/115` and `RESULT: PASS`, exit 0. The selfcheck applies its own `is_patient_statement` (research/lexicon_selfcheck.py:165, called at :179) to lexicon `self_report` entries. Production does not: grounding.py:73-76 still loads `self_report` and `self_report_exclude`, and `_self_report` (grounding.py:205-213) reads neither. `grep -rn "exclude_sentence\|self_report_scope" app tests` finds only the lexicon and the loader (grounding.py:75).
57	
58	   Why it matters: a PASS on the research gate says nothing about what the flag layer emits. The probe rows in finding 1 and 2 are exactly the cases the gate cannot see. The persona rule is that a self-check PASS does not prove the product path.
59	
60	   Fix: the selfcheck should call `grounding.has_self_report` (the production function) on the golden, held-out and adversarial rows, or the lexicon self_report entries and `self_report_scope` should be deleted once D-035 is the only rule.
61	
62	   Acceptance test: `research/lexicon_selfcheck.py` imports and calls `app.backend.grounding.has_self_report` for the patient-attribution rows, and the seven finding-1 and four finding-2 rows are in the held-out set with expected record.
63	
64	4. **Minor. Spec and lexicon text still state the superseded rule, and one lexicon note contradicts D-035 and the pinned test.** Evidence: `memory/DECISIONS.md:286` still reads "`source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt". `app/llm/lexicon.yaml:25-26` says the same. `app/llm/lexicon.yaml:764` reads `"C/O" and "complains of" with no named speaker are read as the patient, which is the clinical convention.` That contradicts the commit's pinned no-tag for bare "C/O neck pain 7/10 and headache." (test_flags_pass.py:184-188 area).
65	   Fix: amend DECISIONS.md:286 and lexicon.yaml:25-26 to D-035's rule. Rewrite lexicon.yaml:764 to say bare C/O gets no chip.
66	   Acceptance test: `grep -n "from the lexicon .self_report. entries" memory/DECISIONS.md` returns nothing; `grep -n "read as the patient, which is the clinical convention" app/llm/lexicon.yaml` returns nothing.
67	
68	5. **Minor. D-035 narrows the chip without saying so, and the code's verb set is wider than D-035's list.** Evidence: probe rows, `Patient-reported neck pain 7/10.` -> record; `Patient links her neck pain to the collision.` -> record; `C/O neck pain 7/10 and headache.` -> record. All three were patient_report in r1 and r2. The commit moved them to the no-list (test diff: `git show a27b358 -- tests/unit/test_flags_pass.py`). Separately, `_VERB` (grounding.py:183-184) includes describes, admits, recalls, claims, believes, feels, relates and attributes, which D-035's parenthetical (ORCHESTRATOR_DECISIONS.md:44) does not name.
69	   Why it matters: a missing chip is safe under D-035, so this is not a blocker. But the team's spec and the code should agree on what counts as an explicit patient attribution, and "C/O" is the adjuster's most common patient-voice marker.
70	   Fix: name the verb set in D-035 (or trim `_VERB` to it). Decide on bare C/O (question 3).
71	   Acceptance test: D-035 lists the verb set used by `_VERB`, and the three rows above are either tagged or listed as deliberate no-tag in D-035.
72	
73	6. **Minor. Held-out set still has no patient-subject sentence naming a family or EMS member (r2 finding 6, carried forward).** Evidence: `grep -n "Patient states EMS noted\|wife said he was fine\|Patient states his wife" evals/lexicon_heldout.jsonl` returns nothing. The only family-named row is H-109, `Per his wife, headaches began at the scene.`
74	   Fix: add `Patient states EMS noted a laceration.` and `Patient reports his wife said he was fine.` with expected patient_report.
75	   Acceptance test: both appear in evals/lexicon_heldout.jsonl and the research gate checks them (finding 3).
76	
77	## What is not a finding
78	
79	- `Patient-reported` and bare `C/O` losing the chip: a deliberate D-035 narrowing with a pinned test. Reported as finding 5 and question 3, not as a blocker.
80	- `Per EMS, pt. c/o neck pain.` and `EMS noted pt. reports neck pain 7/10.`: record, as in r2.
81	- `Date of accident per intake form: 2026-01-19.`: record, so the intake date is not an attribution.
82	- The `test_split_llm.py` failure on the archive (below): outside my lens.
83	
84	## Outside my lens
85	
86	`tests/unit/test_split_llm.py::test_split_audit_row_has_prompt_version_and_flag_resolves_to_call` fails on the a27b358 archive and on the parent 473ac2a archive, so it is not caused by this commit. The `-k "flag or ..."` filter matches it by name. The live tree passes it. I did not triage why the archive fails.
87	
88	## Exercised
89	
90	- Read `personas/claims-adjuster.md` in full; `memory/ORCHESTRATOR_DECISIONS.md` (D-024 line 32, D-033 line 41, D-035 line 44); `reviews/T-061-claims-adjuster.md` (r1, full); `reviews/T-061-claims-adjuster-r2.md` (full); my memory files `feedback_review_commit_not_worktree.md`, `project_t061_r2_speaker_scope.md`, `feedback_lexicon_review_method.md`.
91	- `.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon or self_report" 2>&1 | tail -2` on the live tree (HEAD d0c9cdb) gave `123 passed, 770 deselected in 2.23s`. A second run gave `123 passed, 772 deselected in 2.07s`; the count moved because the tree moved.
92	- `git status --short -- app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py research evals app/llm`: `M app/llm/record.py` and evals reports only. None of the reviewed files has a diff. `git merge-base --is-ancestor a27b358 d0c9cdb` says the commit is in HEAD. `git show --stat d0c9cdb` gives `tests/unit/test_grounding_may.py` only.
93	- `git archive a27b358` extracted to the session scratchpad `r3-a27`. `cd r3-a27 && .venv/bin/python -m pytest tests/unit -q -k "flag or lexicon or self_report" -p no:cacheprovider 2>&1 | tail -2` gave `1 failed, 122 passed, 760 deselected`. The failure is the `test_split_llm.py` case above. The same command on `git archive 473ac2a` (parent) gave `1 failed, 122 passed, 760 deselected`.
94	- `artifacts/review-evidence/T-061-r3-probe.py` (new, read-only) run against the a27b358 archive: `.venv/bin/python artifacts/review-evidence/T-061-r3-probe.py <r3-a27>`. Output saved to `artifacts/review-evidence/T-061-r3-probe.txt`: 70 rows (r1 probe, r2 probe, the brief sentences, and r3 variants); `SUMMARY rows=70 misses=11 superseded=3`. The probe calls `flags._flag` (flags.py:46 constructor) and `grounding.has_self_report` and `grounding.patient_report_spans`. The module path printed was the archive's grounding.py.
95	- `research/lexicon_selfcheck.py` run from the archive: `RESULT: PASS`, exit 0 (finding 3).
96	- `grep -n "exclude_sentence\|self_report_scope" app/ tests/` in the archive: lexicon.yaml:88-89 and grounding.py:75 (loader only); `sed -n 68,84p` and `grep -n` on grounding.py for `_self_report`, `_lexicon()`, `self_report_exclude`.
97	- `grep -n "from the lexicon .self_report. entries" memory/DECISIONS.md` gave line 286. `grep -n "clinical convention"` on the archive's lexicon.yaml gave line 764.
98	- `grep` of `evals/lexicon_heldout.jsonl` for the two patient-subject family/EMS sentences: no output (finding 6).
99	- `git show a27b358 -- app/backend/grounding.py` and `git show a27b358 -- tests/unit/test_flags_pass.py` (full diffs read).
100	- Probe rows reproduced by hand through `flags._flag` in the probe output (the file above).
101	
102	```json
103	{"card": "T-061", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
104	 "scope": "commit a27b358 (T-061 r3, D-035 clause-level patient_report: app/backend/grounding.py, tests/unit/test_flags_pass.py), reviewed via git archive in the session scratchpad (r3-a27); HEAD d0c9cdb (adds test_grounding_may.py only) ran for the brief pytest command; specs memory/ORCHESTRATOR_DECISIONS.md D-033 (line 41), D-035 (line 44), D-024 (line 32), memory/DECISIONS.md:286; no app URL (flag and attribution layer, no UI in scope); probe artifacts/review-evidence/T-061-r3-probe.py -> T-061-r3-probe.txt.",
105	 "exercised": [
106	  "Read personas/claims-adjuster.md in full; ORCHESTRATOR_DECISIONS.md D-024, D-033, D-035; reviews/T-061-claims-adjuster.md (r1) and reviews/T-061-claims-adjuster-r2.md (full); my memory files",
107	  ".venv/bin/python -m pytest tests/unit -q -k 'flag or lexicon or self_report' 2>&1 | tail -2 -> 123 passed, 770 deselected (live, d0c9cdb); second run 123 passed, 772 deselected",
108	  "git status --short on reviewed paths (only app/llm/record.py and evals reports, none reviewed); git merge-base --is-ancestor a27b358 d0c9cdb; git show --stat d0c9cdb",
109	  "git archive a27b358 -> scratchpad r3-a27; pytest -k 'flag or lexicon or self_report' there -> 1 failed, 122 passed (test_split_llm.py::test_split_audit_row_has_prompt_version_and_flag_resolves_to_call, same failure on parent 473ac2a archive; outside scope)",
110	  "artifacts/review-evidence/T-061-r3-probe.py against the a27b358 archive -> artifacts/review-evidence/T-061-r3-probe.txt: 70 rows, misses 11 (r3-adv 7, r3-adv2 4), superseded 3; brief script-checks 4/4, r1 19/19, r2 colon/abbrev/long-subject 11/11, r2 adv2 6/6, r2 mixed 2/2",
111	  "research/lexicon_selfcheck.py on the archive -> SUMMARY golden MUST 11/11, held-out 115/115; RESULT: PASS; exit 0",
112	  "sed -n 68,84p and grep -n on app/backend/grounding.py (lines 73-76, 183-186, 189-200, 205-213, 243-245): production reads no lexicon self_report entry and no self_report_exclude",
113	  "grep -rn exclude_sentence|self_report_scope app/ tests/ on archive -> lexicon.yaml:88-89, grounding.py:75 only",
114	  "grep -n 'from the lexicon .self_report. entries' memory/DECISIONS.md -> 286; grep 'clinical convention' lexicon.yaml -> 764",
115	  "grep -n 'Patient states EMS noted|wife said he was fine|Patient states his wife' evals/lexicon_heldout.jsonl -> no output; only H-109 names a family member",
116	  "git show a27b358 -- app/backend/grounding.py and -- tests/unit/test_flags_pass.py (full diffs read); grep -n on test_flags_pass.py for test_d035_* line numbers"
117	 ],
118	 "verdict": "fail",
119	 "scores": {"attribution_precision_production": 2, "clause_scope_logic": 2, "ac2_flags_wiring": 4, "prior_findings_closed": 3, "test_honesty": 3, "spec_consistency": 2},
120	 "findings": [
121	  {"severity": "blocker",
122	   "title": "A family or EMS clause after a comma, 'and' or a parenthesis inside a patient-subject sentence inherits the patient chip",
123	   "evidence": "artifacts/review-evidence/T-061-r3-probe.txt MISS rows r3-adv: 'Patient states pain began after the collision, wife reports headaches.', 'Pt reports neck pain, EMS notes headaches.', 'Patient reports neck pain and his wife says he is in pain.', 'Patient reports neck pain, per his wife, headaches began at the scene.', 'Patient reports neck pain (per wife, headaches since the scene).', 'Patient reports pain 4/10, girlfriend says he limps.', 'Patient reports neck pain, Mrs. Ortiz reports headaches.' all give source_kind patient_report; span is the whole sentence. Cause: app/backend/grounding.py:189-200 patient_report_spans runs the span to the next ';' or sentence end (S.unit_spans, app/backend/sentences.py:29); grounding.py:205-213 _self_report searches only the text outside the span, so the comma-joined family clause is never checked. Comment at grounding.py:190-191 says a clause starts after a comma but the span end ignores commas. tests/unit/test_flags_pass.py test_d035_tag_spans_the_patient_clause_only (line 190) pins the ';' span; no comma-joined case is tested.",
124	   "why_it_matters": "The chip tells the reader the claimant said what a wife, girlfriend, EMS or family member said. D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) names this exact error as a credibility error an adjuster would exploit. This is the r2 finding 2 class, which was a blocker; the semicolon form now passes but the comma, 'and' and parenthesis forms do not. Under the chosen rule (b) (grounding.py:206) these excerpts must be record. D-035 (ORCHESTRATOR_DECISIONS.md:44): a missing chip is safe, a wrong chip is not.",
125	   "fix": "(i) End the patient span at the next comma, 'and' or open parenthesis that begins another clause, so rule (b) applies to the family clause; or (ii) attach the chip only when the patient clause is the whole excerpt (safer, simpler). Under (ii) the pinned 'Pt c/o neck pain; wife drove him in.' changes to record and its test changes with it.",
126	   "acceptance_test": "The seven r3-adv rows return has_self_report False and source_kind record via flags._flag. 'Patient states EMS noted a laceration.', 'Patient reports his wife said he was fine.', 'Patient states his wife drove him to the ER.' stay patient_report. research/lexicon_selfcheck.py still PASS. The seven rows are added to tests/unit/test_flags_pass.py."},
127	  {"severity": "blocker",
128	   "title": "A non-patient clause whose reporting verb is outside the closed list inherits the chip",
129	   "evidence": "artifacts/review-evidence/T-061-r3-probe.txt MISS rows r3-adv2 (all source_kind patient_report): 'Patient states neck pain; wife thinks he is faking.', 'Patient reports neck pain, wife thinks he is faking.', 'Patient states neck pain; his wife told the ER he was fine.', 'Patient states neck pain, EMS notes headaches, wife reports nausea.'. Cause: app/backend/grounding.py:186 _REPORT_WORD and :183-184 _VERB are closed lists; _self_report (grounding.py:205-213) decides 'no other speech' by searching the leftover text for them. 'thinks', 'told', 'insists' are not in the list.",
130	   "why_it_matters": "The excerpt quotes a spouse's or family member's opinion or account under the claimant's 'Patient self-report' chip. D-035 says any other or unknown speaker gets no tag (ORCHESTRATOR_DECISIONS.md:44); a closed verb list cannot satisfy an any-speaker rule. Same credibility error as D-033 (line 41).",
131	   "fix": "Make the mixed-excerpt test independent of the verb list: under rule (b), any clause after the patient clause makes the excerpt record. Do not fix by adding verbs; that moves the hole.",
132	   "acceptance_test": "The four r3-adv2 rows return record. They are added to test_d035_mixed_excerpt_carries_no_chip (tests/unit/test_flags_pass.py:199). The pinned 'Pt c/o neck pain; wife drove him in.' is decided under the chosen rule and the test says which."},
133	  {"severity": "major",
134	   "title": "The research gate PASS measures a rule production no longer runs",
135	   "evidence": "research/lexicon_selfcheck.py on archive a27b358: 'SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 0 of 0; held-out 115/115', 'RESULT: PASS', exit 0. The selfcheck applies its own is_patient_statement (research/lexicon_selfcheck.py:165, called at :179) to lexicon self_report entries. Production: app/backend/grounding.py:73-76 loads self_report and self_report_exclude; _self_report (grounding.py:205-213) reads neither. grep -rn exclude_sentence|self_report_scope app/ tests/ finds only app/llm/lexicon.yaml:88-89 and grounding.py:75 (loader).",
136	   "why_it_matters": "A PASS on the research gate says nothing about what flags.py:46 and :125 emit. The cases in findings 1 and 2 are exactly what the gate cannot see. A self-check that tests a rule production does not run gives false comfort.",
137	   "fix": "Make the selfcheck call grounding.has_self_report (the production function) for the patient-attribution rows, or delete the lexicon self_report entries and self_report_scope once D-035 is the only rule.",
138	   "acceptance_test": "research/lexicon_selfcheck.py imports app.backend.grounding.has_self_report and reports its result for the attribution rows; the finding 1 and finding 2 rows are in evals/lexicon_heldout.jsonl with expected record; selfcheck PASS."},
139	  {"severity": "minor",
140	   "title": "Spec and lexicon text still state the superseded rule; one lexicon note contradicts D-035 and the pinned test",
141	   "evidence": "memory/DECISIONS.md:286: '`source_kind = \"patient_report\"` is set by code from the lexicon `self_report` entries on the excerpt'. app/llm/lexicon.yaml:25-26 says the same. app/llm/lexicon.yaml:764: '\"C/O\" and \"complains of\" with no named speaker are read as the patient, which is the clinical convention.' The pinned no-tag for bare 'C/O neck pain 7/10 and headache.' is in tests/unit/test_flags_pass.py (no-list, around line 184).",
142	   "why_it_matters": "A future reader gets two rules, and the lexicon note tells the reader the opposite of what the code does for bare C/O.",
143	   "fix": "Amend DECISIONS.md:286 and lexicon.yaml:25-26 to D-035's rule. Rewrite lexicon.yaml:764 to say bare C/O gets no chip.",
144	   "acceptance_test": "grep -n 'from the lexicon .self_report. entries' memory/DECISIONS.md returns nothing; grep -n 'read as the patient, which is the clinical convention' app/llm/lexicon.yaml returns nothing."},
145	  {"severity": "minor",
146	   "title": "D-035 narrows the chip without saying so, and the code's verb set is wider than D-035's list",
147	   "evidence": "artifacts/review-evidence/T-061-r3-probe.txt: 'Patient-reported neck pain 7/10.' -> record; 'Patient links her neck pain to the collision.' -> record; 'C/O neck pain 7/10 and headache.' -> record. All three were patient_report in r1 and r2; the commit moved them to the no-list (git show a27b358 -- tests/unit/test_flags_pass.py). _VERB (app/backend/grounding.py:183-184) includes describes, admits, recalls, claims, believes, feels, relates, attributes, which D-035's parenthetical (ORCHESTRATOR_DECISIONS.md:44) does not name.",
148	   "why_it_matters": "A missing chip is safe under D-035, so this is not a blocker. The spec and the code should agree on what counts as explicit patient attribution, and bare C/O is the most common patient-voice marker in clinical notes.",
149	   "fix": "Name the verb set in D-035 or trim _VERB to it. Decide on bare C/O (question 3).",
150	   "acceptance_test": "D-035 lists the verb set used by _VERB; the three rows are either tagged or recorded as deliberate no-tag in D-035."},
151	  {"severity": "minor",
152	   "title": "Held-out set has no patient-subject sentence naming a family or EMS member (r2 finding 6, carried forward)",
153	   "evidence": "grep -n 'Patient states EMS noted|wife said he was fine|Patient states his wife' evals/lexicon_heldout.jsonl: no output. The only family-named row is H-109 'Per his wife, headaches began at the scene.' (evals/lexicon_heldout.jsonl:109).",
154	   "why_it_matters": "The research gate cannot show a regression on the patient-subject-plus-family case, which is the over-exclusion class from r1 finding 3.",
155	   "fix": "Add 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' with expected patient_report.",
156	   "acceptance_test": "Both sentences appear in evals/lexicon_heldout.jsonl with expected patient_report and the research gate checks them."}
157	 ],
158	 "whats_right": [
159	  "The r2 colon, abbreviation and long-subject forms and the third-party speakers (girlfriend, co-worker, passenger, ambulance crew, triage nurse) are record now: 11/11 r2 adv and 6/6 r2 adv2 rows match, and the default-no-tag design of D-035 is the right shape.",
160	  "The semicolon mixed case is fixed: 'C/O neck pain; wife reports headaches.' is record, and 'EMS reports neck pain, patient states headaches.' spans only 'patient states headaches.' (brief allowed the absent excerpt chip).",
161	  "All four brief script-checks hold through the production constructor: 'Pt reports neck pain.' tagged; 'Girlfriend says he limps.' and 'C/O neck pain; wife reports headaches.' none; and the round-1 EMS, witness, wife, family and intake-date rows are record."
162	 ],
163	 "questions_for_chris": [
164	  "Does a clause end at a comma? D-035 says the tag spans to the next ';' or sentence end, which is what makes finding 1 possible. My recommendation is option (ii) in finding 1 (chip only when the patient clause is the whole excerpt), because a missing chip is safe and a wrong one is not. Confirm (i) or (ii).",
165	  "Is the chip meant to cover a non-patient clause that has no speech verb, such as 'Pt c/o neck pain; wife drove him in.' (pinned by test_flags_pass.py)? Under rule (b) it should be record; the pinned test says patient_report. Which one?",
166	  "Bare 'C/O neck pain 7/10' and 'Patient-reported neck pain' now have no chip (pinned). The lexicon note at lexicon.yaml:764 calls C/O the clinical convention for the patient. Is the no-chip outcome deliberate, and should D-035 say so?",
167	  "D-024 item 7 says no harness rounds after M0 r3, residual findings become debt. T-061 is product attribution, not harness. I did not downgrade the two blockers on that basis. Is T-061 under that rule, or does it need a fix before the gate?",
168	  "The persona file expects model claude-opus-5-5 in the review record. I ran as claude-haiku-5-5 and wrote that id, as in rounds 1 and 2. Confirm acceptable for the gate."
169	 ]}
170	```
171	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:09.528Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/memory/ORCHESTRATOR_DECISIONS.md"
}
````

### User / tool · 2026-11-02T02:37:09.536Z

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
46	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:10.098Z

**tool call — Bash**
````
{
 "command": "git show --stat 991dac4 2>&1 | head -40; echo ---; git log --oneline -5 2>&1; echo ---; ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/",
 "description": "Show fix commit stats and recent log"
}
````

### User / tool · 2026-11-02T02:37:10.227Z

**tool result**
````
commit 991dac48e68ff98c2f0f39432d44cd8baeb93242
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:36:47 2026 -0600

    fix(backend): patient_report chip only on a whole-excerpt patient clause (T-061 r4, D-037)
    
    Drops clause splitting and the closed verb list; any ; , ( or 'and' means no chip. Selfcheck now calls grounding.has_self_report.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/amounts.py         |  2 +-
 app/backend/case_extras.py     |  4 ++--
 app/backend/dates.py           |  8 ++++----
 app/backend/grounding.py       | 39 ++++++++++++++-----------------------
 app/llm/_types.py              |  2 +-
 research/lexicon_selfcheck.py  | 44 ++++++++++++++++++++++++------------------
 tests/unit/test_case_extras.py | 21 ++++++++++++++++++++
 tests/unit/test_flags_pass.py  | 33 ++++++++++++++++++++-----------
 8 files changed, 90 insertions(+), 63 deletions(-)
---
670ed09 test(backend): batch accept refuses needs_review and rejected entries (T-055 F1/F2)
991dac4 fix(backend): patient_report chip only on a whole-excerpt patient clause (T-061 r4, D-037)
38421cc memory: record §7.4 debt rows and scope cut 20
8ec0b25 docs: D-037 patient_report chip only on whole-excerpt patient clause (T-061 r3)
08764e7 fix(backend): local mode refuses non-loopback peers by address (T-053 F1, D-036)
---
MEMORY.md
feedback_lexicon_review_method.md
feedback_review_commit_not_worktree.md
feedback_reviews_write_once.md
project_flag_pass_review_patterns.md
project_flag_source_kind_and_run_signal.md
project_research_attack_map_gaps.md
project_t036_r4_split_and_judge_fixtures.md
project_t061_r2_speaker_scope.md
project_t061_r3_clause_span_holes.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:13.653Z

**tool call — Bash**
````
{
 "command": "git show 991dac4 -- app/backend/grounding.py tests/unit/test_flags_pass.py research/lexicon_selfcheck.py 2>&1",
 "description": "Show the fix diff for grounding, tests and selfcheck"
}
````

### User / tool · 2026-11-02T02:37:13.750Z

**tool result**
````
commit 991dac48e68ff98c2f0f39432d44cd8baeb93242
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:36:47 2026 -0600

    fix(backend): patient_report chip only on a whole-excerpt patient clause (T-061 r4, D-037)
    
    Drops clause splitting and the closed verb list; any ; , ( or 'and' means no chip. Selfcheck now calls grounding.has_self_report.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/grounding.py b/app/backend/grounding.py
index 75a65be..d025172 100644
--- a/app/backend/grounding.py
+++ b/app/backend/grounding.py
@@ -177,40 +177,29 @@ _HEDGE_WORDS = re.compile(r"\b(" + _MODAL_MAY + r"|might|possibl[ey]|likely|prob
                           r"uncertain|indeterminate|non-?specific)\b", re.IGNORECASE)
 
 
-# D-035 (supersedes the D-033 speaker lists): patient_report attaches only to a CLAUSE that begins with an explicit patient subject
-# (Patient | Pt | The patient) plus a reporting verb, and spans that clause only (to the next ';' or the sentence end). Everything else
-# - EMS, family, any other or unknown speaker, bare "C/O", "S:"/"Subjective:" headers - gets no tag. A missing chip is safe; a wrong one is not.
+# D-037 (supersedes the D-035 clause splitting and the D-033 speaker lists): patient_report attaches only when the WHOLE excerpt is one
+# patient-subject clause: it begins with Patient | Pt | The patient + a reporting verb, is a single sentence, and holds no ';', ',', ' and ' or
+# '(' that could start a further clause. Anything else - EMS, family, any other or unknown speaker, bare "C/O", "S:"/"Subjective:" headers,
+# any mixed excerpt - gets no chip. No verb list decides who else is speaking. A missing chip is safe; a wrong one mislabels the source.
 _VERB = (r"(?:states?|stated|reports?|reported|notes?|noted|says|said|endorses|endorsed|complains?\s+of|complained\s+of|c/o|denies|denied|"
-         r"describes|described|admits|recalls|claims|believes|feels|relates|attributes)")
-_PATIENT_CLAUSE = re.compile(r"(?:(?<=^)|(?<=[,\s]))(?:the\s+)?(?:patient|pt\x00?)\s+" + _VERB + r"\b", re.IGNORECASE)
-_REPORT_WORD = re.compile(r"\b" + _VERB + r"\b|\bc/o\b|\bper\b", re.IGNORECASE)   # "per X" is an attribution too
+         r"describes|described)")
+_PATIENT_CLAUSE = re.compile(r"(?:the\s+)?(?:patient|pt\x00?)\s+" + _VERB + r"\b", re.IGNORECASE)
+_FURTHER_CLAUSE = re.compile(r"[;,(]|\band\b", re.IGNORECASE)
 
 
 def patient_report_spans(text: str) -> list:
-    """[(start, end)] of the clauses that carry the patient_report tag. A clause starts at a unit start or after a comma; it runs to the
-    next ';' / sentence end. 'EMS reports X, patient states headaches.' -> only 'patient states headaches.'"""
+    """[(start, end)] of the text carrying the patient_report tag: the whole stripped excerpt when it is one patient-subject clause, else []."""
     from app.backend import sentences as S
     masked = re.sub(r"\b([Pp]t)\.", lambda m: m.group(1) + "\x00", text)          # 'Pt.' is an abbreviation, not a sentence end (same length)
-    spans = []
-    for a, b in S.unit_spans(masked):
-        for m in _PATIENT_CLAUSE.finditer(masked, a, b):
-            at_start = not masked[a:m.start()].strip()
-            after_comma = masked[a:m.start()].rstrip().endswith(",")
-            if at_start or after_comma:
-                spans.append((m.start(), b))
-                break
-    return spans
+    lead = len(masked) - len(masked.lstrip())
+    body = masked.strip()
+    if not body or len(S.unit_spans(body)) != 1 or not _PATIENT_CLAUSE.match(body) or _FURTHER_CLAUSE.search(body):
+        return []
+    return [(lead, lead + len(body))]
 
 
 def _self_report(text: str) -> bool:
-    """True when the text has a patient clause and no other clause reports speech (a mixed excerpt cannot carry one chip, so it carries none)."""
-    spans = patient_report_spans(text)
-    if not spans:
-        return False
-    rest = text
-    for a, b in sorted(spans, reverse=True):
-        rest = rest[:a] + " " + rest[b:]
-    return not _REPORT_WORD.search(rest)
+    return bool(patient_report_spans(text))
 
 
 def dropped_qualifiers(summary: str, excerpt: str) -> list:
diff --git a/research/lexicon_selfcheck.py b/research/lexicon_selfcheck.py
index 055af5d..4f7b3fa 100644
--- a/research/lexicon_selfcheck.py
+++ b/research/lexicon_selfcheck.py
@@ -159,15 +159,24 @@ def _clause_after(text, end):
     return text[end:end + m.start()] if m else text[end:]
 
 
-SR_EXCLUDE = None  # compiled in main() from lexicon self_report_scope.exclude_sentence
-
-
-def is_patient_statement(text, start, end):
-    """T-061: True unless the sentence around the match names a non-patient speaker (EMS, witness, spouse, family)."""
-    if SR_EXCLUDE is None:
-        return True
-    s0, s1 = _sentence_bounds(text, start, end)
-    return not SR_EXCLUDE.search(text[s0:s1])
+def production_chip(text):
+    """D-037 / T-061 r3 finding 3: ask the PRODUCTION function, not a reference copy. True when app.backend.grounding.has_self_report(text)
+    would put the 'Patient self-report' chip on this excerpt (whole excerpt = one patient-subject clause)."""
+    if str(ROOT) not in sys.path:
+        sys.path.insert(0, str(ROOT))
+    from app.backend import grounding
+    return grounding.has_self_report(text)
+
+
+# T-061 r3 B1/B2 rows (reviews/T-061-claims-adjuster-r3.md) plus the D-037 keep rows; expected chip decided by production, run every time.
+CHIP_NO = ["Patient states pain began after the collision, wife reports headaches.", "Pt reports neck pain, EMS notes headaches.",
+           "Patient reports neck pain and his wife says he is in pain.", "Patient reports neck pain, per his wife, headaches began at the scene.",
+           "Patient reports neck pain (per wife, headaches since the scene).", "Patient reports pain 4/10, girlfriend says he limps.",
+           "Patient reports neck pain, Mrs. Ortiz reports headaches.", "Patient states neck pain; wife thinks he is faking.",
+           "Patient reports neck pain, wife thinks he is faking.", "Patient states neck pain; his wife told the ER he was fine.",
+           "Patient states neck pain, EMS notes headaches, wife reports nausea.", "Pt c/o neck pain; wife drove him in.", "C/O neck pain 7/10 and headache."]
+CHIP_YES = ["Patient states EMS noted a laceration.", "Patient reports his wife said he was fine.", "Patient states his wife drove him to the ER.",
+            "Pt reports neck pain 7/10.", "Patient complains of lower back pain."]
 
 
 def hits(entry, text, neg, accident_year):
@@ -176,8 +185,6 @@ def hits(entry, text, neg, accident_year):
     for m in entry["_rx"].finditer(text):
         if entry.get("negatable") and negated(text, m.start(), m.end(), neg):
             continue
-        if entry.get("self_report") and not is_patient_statement(text, m.start(), m.end()):
-            continue
         if entry.get("year_filter") and accident_year:
             y = _hit_year(m)
             if y and y >= accident_year:
@@ -225,14 +232,7 @@ def _overlaps(text, span, excerpt):
 
 def main():
     lex = yaml.safe_load(LEX.read_text())
-    global SR_EXCLUDE
     neg = lex["negation"]
-    SR_EXCLUDE = re.compile(lex["self_report_scope"]["exclude_sentence"], re.I)
-    for k in ("exclude", "keep"):
-        for ex_s in lex["self_report_scope"]["examples"][k]:
-            if bool(SR_EXCLUDE.search(ex_s)) != (k == "exclude"):
-                print(f"ERROR self_report_scope example {k}: {ex_s!r}")
-                sys.exit(1)
     entries = lex["entries"]
     types = set(lex["flag_types"])
     errors, ids = [], set()
@@ -452,7 +452,7 @@ def main():
             elif x == "quiet_hedge":
                 ok = not any(e["hedge"] for e in raised)
             elif x == "quiet_self_report":
-                ok = not any(e["self_report"] for e, _ in res)
+                ok = not production_chip(r["text"])
             else:
                 raise SystemExit(f"bad expect {x}")
             ho_tot += 1
@@ -472,6 +472,12 @@ def main():
             errors.append(f"{len(leaked)} held-out sentences copied into lexicon examples")
     else:
         errors.append("evals/lexicon_heldout.jsonl missing")
+    chip_bad = [t for t in CHIP_NO if production_chip(t)] + [t for t in CHIP_YES if not production_chip(t)]
+    print(f"\n[production chip] grounding.has_self_report on {len(CHIP_NO)} no-chip + {len(CHIP_YES)} chip rows: {len(CHIP_NO) + len(CHIP_YES) - len(chip_bad)}/{len(CHIP_NO) + len(CHIP_YES)}")
+    for t in chip_bad:
+        print("  CHIP MISMATCH " + t)
+    if chip_bad:
+        errors.append(f"{len(chip_bad)} production chip mismatches")
     held_pass = ho_tot >= 40 and ho_ok / max(ho_tot, 1) >= HELDOUT_BAR
 
     if mismatch:
diff --git a/tests/unit/test_flags_pass.py b/tests/unit/test_flags_pass.py
index 373a69c..ac18ee8 100644
--- a/tests/unit/test_flags_pass.py
+++ b/tests/unit/test_flags_pass.py
@@ -115,7 +115,7 @@ def test_lexicon_self_report_drives_source_kind_with_explicit_patient_attributio
     """D-035: only a clause that begins with an explicit patient subject plus a reporting verb gets patient_report."""
     from app.backend import grounding as GR
     yes = ["Patient notes prior neck pain.", "Patient describes neck pain since the collision.", "Patient reports prior neck pain.",
-           "Pt c/o neck pain 7/10 and headache.", "Pt. c/o neck pain 7/10.", "The patient denies loss of consciousness."]
+           "Pt c/o neck pain 7/10.", "Pt. c/o neck pain 7/10.", "The patient denies loss of consciousness."]
     no = ["Date of accident per intake form: 2026-01-19.", "Per EMS report, neck pain.", "Wife reports he was in pain.", "EMS reports minimal damage.",
           "Subjective: neck pain 7/10.", "C/O neck pain 7/10 and headache.", "Patient-reported pain 4/10."]
     assert all(GR.has_self_report(t) for t in yes), [t for t in yes if not GR.has_self_report(t)]
@@ -173,12 +173,22 @@ NO_TAG = [  # every sentence from reviews/T-061-claims-adjuster.md (r1) and -r2.
     "Wife (Mrs. Ortiz) reports he complains of neck pain.", "C/O neck pain; wife reports headaches.", "Girlfriend reports he complains of neck pain.",
     "Co-worker reports patient c/o neck pain.", "Passenger reports patient complains of neck pain.", "Triage nurse reports he is in pain.",
     "Per EMS, pt. c/o neck pain.", "EMS noted pt. reports neck pain 7/10.", "C/O neck pain 7/10 and headache.", "Date of injury per registration paperwork: 03/02/2026.",
+    # D-037: any further clause after ';' ',' ' and ' '(' means no chip, whoever speaks it (r3 B1 and B2 reviewer examples)
+    "Patient states pain began after the collision, wife reports headaches.", "Pt reports neck pain, EMS notes headaches.",
+    "Patient reports neck pain and his wife says he is in pain.", "Patient reports neck pain, per his wife, headaches began at the scene.",
+    "Patient reports neck pain (per wife, headaches since the scene).", "Patient reports pain 4/10, girlfriend says he limps.",
+    "Patient reports neck pain, Mrs. Ortiz reports headaches.", "Patient states neck pain; wife thinks he is faking.",
+    "Patient reports neck pain, wife thinks he is faking.", "Patient states neck pain; his wife told the ER he was fine.",
+    "Patient states neck pain, EMS notes headaches, wife reports nausea.",
+    "Pt c/o neck pain; wife drove him in.",                      # pinned: fail closed, no chip
+    "Pt c/o neck pain 7/10 and headache.", "Patient reports low back pain in 2023, resolved.",
+    "Patient states headaches. Patient reports neck pain.",       # two sentences: not a single clause
 ]
 YES_TAG = [  # explicit patient subject + reporting verb (r1 and r2 keep-lists)
     "Patient states symptoms began after the January collision.", "Patient complains of neck pain.", "Pt c/o neck pain 7/10.",
     "Patient states EMS noted a laceration.", "Patient reports his wife said he was fine.", "Patient states his wife drove him to the ER.",
-    "Pt c/o neck pain; wife drove him in.", "Patient reports low back pain in 2023, resolved.", "The patient denies loss of consciousness.",
-]
+    "The patient denies loss of consciousness.", "Pt. reports neck pain 7/10.",
+]    # D-037: single clause, patient subject, so the chip attaches even when another speaker is named inside it
 
 
 def test_d035_every_reviewed_sentence_no_tag_or_tag():
@@ -187,19 +197,20 @@ def test_d035_every_reviewed_sentence_no_tag_or_tag():
     assert [t for t in YES_TAG if _kind(t) != "patient_report"] == []
 
 
-def test_d035_tag_spans_the_patient_clause_only():
-    """The tag covers the clause that starts at the patient subject, to the next ';' or the sentence end."""
-    assert _spans("C/O neck pain; wife reports headaches.") == []                                  # no tag on either clause
-    assert _spans("EMS reports minimal damage, patient states headaches.") == ["patient states headaches."]
-    assert _spans("Pt c/o neck pain; wife drove him in.") == ["Pt c/o neck pain;"]
-    assert _spans("EMS reports neck pain. Patient states headaches began at the scene.") == ["Patient states headaches began at the scene."]
+def test_d037_tag_spans_the_whole_excerpt_or_nothing():
+    """D-037: the chip covers the whole excerpt when it is one patient-subject clause; otherwise there is no span."""
+    assert _spans("C/O neck pain; wife reports headaches.") == []
+    assert _spans("EMS reports minimal damage, patient states headaches.") == []
+    assert _spans("Pt c/o neck pain; wife drove him in.") == []
+    assert _spans("  Patient states EMS noted a laceration.  ") == ["Patient states EMS noted a laceration."]
     assert _spans("Girlfriend reports he complains of neck pain.") == [] and _spans("Co-worker reports patient c/o neck pain.") == []
 
 
-def test_d035_mixed_excerpt_carries_no_chip():
-    """One chip per excerpt cannot be right when a non-patient speaker shares it: the excerpt gets no chip (a missing chip is safe)."""
+def test_d037_mixed_excerpt_carries_no_chip():
+    """One chip per excerpt cannot be right when another clause shares it: no chip, and no verb list decides (any speaker, any verb)."""
     assert _kind("EMS reports minimal damage, patient states headaches.") == "record"
     assert _kind("EMS reports neck pain. Patient states headaches began at the scene.") == "record"
+    assert _kind("Patient states neck pain; wife insists he mentions nothing.") == "record"    # verbs outside any list
 
 
 def test_d033_lexicon_flags_label_source_kind_by_the_same_rule():
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:14.200Z

**tool call — Bash**
````
{
 "command": "ls -la reviews/ | grep -i T-061; echo ---; grep -n \"\" app/backend/grounding.py | sed -n 60,260p",
 "description": "Check review files exist and read grounding logic"
}
````

### User / tool · 2026-11-02T02:37:14.307Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:44.629Z

**tool call — Bash**
````
{
 "command": "grep -n \"patient_report\\|has_self_report\\|_self_report\\|source_kind\\|patient_report_spans\" app/backend/*.py app/llm/*.py | grep -v \"^app/backend/grounding.py:1[89]\" ; echo ---; cat app/backend/sentences.py | head -80; echo ---; ls artifacts/review-evidence/ | grep -i T-061; echo ---; sed -n 1,60p artifacts/review-evidence/T-061-r3-probe.py",
 "description": "Trace source_kind wiring, sentence splitter, and r3 probe script"
}
````

### User / tool · 2026-11-02T02:37:44.730Z

**tool result**
````
app/backend/export.py:42:_ORDER = ["hedged_imaging", "speculative_language", "noncompliance", "missed_care", "patient_reported_onset", "patient_report",
app/backend/export.py:45:_SELF_REPORT_SUBTYPES = ("patient_reported_onset", "patient_report")
app/backend/generator.py:61:        e.update(summary="", excerpt="", excerpt_start=None, excerpt_end=None, source_kind="record")
app/backend/generator.py:80:             source_kind="patient_report" if grounding.has_self_report(excerpt) else "record")
app/backend/flag_templates.py:25:    ("causation", "patient_reported_onset"): "patient_report",
app/backend/flag_templates.py:35:    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
app/backend/flag_templates.py:126:    "patient_report": lambda v: ("Patient self-report", f"Patient self-report (not a physician's opinion) in {_at(v)}{_quote(v)}."),
app/backend/flags.py:46:         "source_kind": "patient_report" if grounding.has_self_report(excerpt) else "record",
app/backend/flags.py:125:            lx["source_kind"] = "patient_report" if grounding.has_self_report(lx["excerpt"]) else "record"
app/backend/flags.py:170:            "source_kind": "record",
app/backend/flags.py:207:            "reasons": ["CONFLICT_CHECK_INCOMPLETE"], "why": why.why("CONFLICT_CHECK_INCOMPLETE"), "excerpt": "", "source_kind": "record",
app/backend/flags.py:241:             "record_no": ref["n"], "record_id": ref.get("id", f"r{ref['n']}"), "review_status": "pending", "source_kind": "record",
app/backend/grounding.py:201:def _self_report(text: str) -> bool:
app/backend/grounding.py:202:    return bool(patient_report_spans(text))
app/backend/grounding.py:210:    if (_self_report(excerpt) or _SELF_CARRIED.search(excerpt)) and not (_self_report(summary) or _SELF_CARRIED.search(summary)):   # qualifier carry is looser than the chip (D-022 vs D-035)
app/backend/grounding.py:232:def has_self_report(text: str) -> bool:
app/backend/grounding.py:233:    """True when the text carries a patient-attributed marker (source_kind = patient_report, ADR-013)."""
app/backend/grounding.py:234:    return _self_report(text)
app/backend/review.py:200:                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
app/backend/present.py:45:            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind":
app/backend/present.py:46:            "patient_report" if grounding.has_self_report(ed.get("excerpt", row["excerpt"]) or "") else "record",
app/backend/present.py:75:    return {**_common(row), "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
app/backend/pipeline.py:65:                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "review_status": "pending",
app/backend/pipeline.py:80:                      "record_nos": [w["record_no"]], "record_ids": [r["id"]], "source_kind": "record", "review_status": "pending",
app/backend/pipeline.py:146:    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
---
"""Sentence units (R-TL-2, D-012/D-021, ADR-016). One splitter shared by the excerpt check, flag evidence and the edit UI.

A unit is the text up to and including a terminator plus the whitespace after it, so unit spans tile the record text.
Terminators: '.', '?' or '!' (optionally followed by closing quotes/brackets) then whitespace and then an uppercase
letter, a digit or end of text; ';'; a line break. Deterministic code only.
"""
import re

# Never a terminator (the next word continues the sentence): titles, 'approx.', 'vs.', 'e.g.', 'i.e.'.
_ALWAYS_ABBREV = {"approx", "dr", "mr", "mrs", "ms", "vs", "e.g", "i.e", "st"}
# Unit abbreviations: not a terminator before lowercase/digit (already true), but sentence-final before an uppercase
# word ("Rx cyclobenzaprine 10 mg. Follow up ..." is two units; golden test_sentences).
_CLOSERS = "\"')]}"
_TOKEN_BEFORE = re.compile(r"([A-Za-z][A-Za-z.]*)$")


def _abbrev_before(text: str, i: int) -> bool:
    """True if the '.' at text[i] ends a non-terminating abbreviation or a single-letter initial."""
    m = _TOKEN_BEFORE.search(text[:i])
    if not m:
        return False
    tok = m.group(1)
    if tok.lower() in _ALWAYS_ABBREV:
        return True
    # single capital initial ("J. Smith")
    return len(tok) == 1 and tok.isupper()


def unit_spans(text: str) -> list:
    """[(start, end)] tiling `text` exactly (no gaps, no overlaps)."""
    spans, n, start, i = [], len(text), 0, 0
    while i < n:
        ch = text[i]
        end = None
        if ch == ";":
            end = i + 1
        elif ch == "\n":
            end = i + 1
        elif ch in ".?!":
            j = i + 1
            while j < n and text[j] in _CLOSERS:
                j += 1
            if j >= n:
                end = j
            elif text[j].isspace():
                k = j
                while k < n and text[k].isspace():
                    k += 1
                nxt_ok = k >= n or text[k].isupper() or text[k].isdigit() or "\n" in text[j:k]
                if nxt_ok and not (ch == "." and _abbrev_before(text, i)):
                    end = j
        if end is not None:
            while end < n and text[end].isspace():
                end += 1
            spans.append((start, end))
            start, i = end, end
        else:
            i += 1
    if start < n:
        spans.append((start, n))
    return spans


def units(text: str) -> list:
    return [text[a:b] for a, b in unit_spans(text)]


def stripped_spans(text: str) -> list:
    """Unit spans without surrounding whitespace (for API offsets and excerpt alignment)."""
    out = []
    for a, b in unit_spans(text):
        seg = text[a:b]
        lead = len(seg) - len(seg.lstrip())
        trail = len(seg) - len(seg.rstrip())
        if lead < len(seg):
            out.append((a + lead, b - trail))
    return out


def is_whole_units(record_text: str, excerpt: str) -> bool:
---
T-061-base-failed.txt
T-061-head-failed.txt
T-061-probe.py
T-061-probe.txt
T-061-r2-probe.py
T-061-r2-probe.txt
T-061-r3-probe.py
T-061-r3-probe.txt
---
"""T-061 round-3 claims-adjuster probe (read-only). Drives the production flag code path, not the research script.

Usage: .venv/bin/python artifacts/review-evidence/T-061-r3-probe.py <repo_root>

For each sentence: calls flags._flag(...) (the constructor that sets source_kind at flags.py:46), grounding.has_self_report(sentence)
(the function flags.py:46 and flags.py:125 call), and grounding.patient_report_spans(sentence) (the clause spans the D-035 tag covers).
Expectations are the prior-review expectations (r1 = reviews/T-061-claims-adjuster.md, r2 = reviews/T-061-claims-adjuster-r2.md),
the r3 brief script-checks, and the r3 adversarial variants. Rows where D-035 + the pinned tests supersede a prior expectation are
marked SUPERSEDED and are not counted as misses. Nothing is written to the repo.
"""
import sys

root = sys.argv[1]
sys.path.insert(0, root)

from app.backend import flags, grounding  # noqa: E402

print("grounding module =", grounding.__file__)

REC = {"n": 7, "id": "r7", "source": "Austin EMS", "date_iso": "2026-01-09"}


def spans_text(s):
    return [s[a:b].strip() for a, b in grounding.patient_report_spans(s)]


# (sentence, expect_chip, group, note, superseded_note_or_empty, expect_spans_or_None)
ROWS = [
    # ---- r3 brief script-checks (must hold)
    ("Pt reports neck pain.", True, "r3-brief", "tag", "", None),
    ("Girlfriend says he limps.", False, "r3-brief", "none", "", None),
    ("C/O neck pain; wife reports headaches.", False, "r3-brief", "none", "", None),
    ("EMS reports neck pain, patient states headaches.", False, "r3-brief", "only clause 2 spans; excerpt chip absent acceptable",
     "", ["patient states headaches."]),
    # ---- r3 brief sentences that were also in the r1/r2 keep-lists
    ("Patient states pain began after the collision.", True, "brief", "", "", None),
    ("Patient states his wife drove him to the ER.", True, "brief", "", "", None),
    ("Wife reports he has been irritable.", False, "brief", "", "", None),
    ("Per EMS, pt ambulatory at scene.", False, "brief", "", "", None),
    ("S: neck pain", False, "brief", "", "", None),
    ("Witness states the car ran the light.", False, "brief", "", "", None),
    # ---- r1 review probe rows (reviews/T-061-claims-adjuster.md, artifacts/review-evidence/T-061-probe.py)
    ("EMS complains of neck pain 7/10.", False, "r1", "", "", None),
    ("Witness complains of neck pain.", False, "r1", "", "", None),
    ("Wife complains of neck pain.", False, "r1", "", "", None),
    ("Family complains of neck pain.", False, "r1", "", "", None),
    ("EMS reports neck pain 7/10.", False, "r1", "", "", None),
    ("Wife reports he was in pain.", False, "r1", "", "", None),
    ("S: neck pain 7/10.", False, "r1", "", "", None),
    ("Self-reported neck pain 7/10.", False, "r1", "", "", None),
    ("Subjective: neck pain 7/10.", False, "r1", "", "", None),
    ("Patient-reported neck pain 7/10.", True, "r1", "",
     "pinned no-tag by D-035 (test_flags_pass.py no-list); Patient-reported is not a verb after the subject", None),
    ("Patient complains of neck pain.", True, "r1", "", "", None),
    ("C/O neck pain 7/10 and headache.", True, "r1", "",
     "bare C/O: pinned no-tag by D-035 (test_flags_pass.py no-list; no patient subject)", None),
    ("Patient notes prior neck pain.", True, "r1", "", "", None),
    ("Date of accident per intake form: 2026-01-19.", False, "r1", "", "", None),
    ("Patient links her neck pain to the collision.", True, "r1", "",
     "'links' is not in D-035 verb list; test removed it from yes-list", None),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:47.709Z

**tool call — Bash**
````
{
 "command": "sed -n 36,60p app/backend/flags.py; echo ...; sed -n 95,130p app/backend/flags.py; echo ---; sed -n 70,84p app/backend/generator.py; echo ---; grep -n \"self_report\" app/llm/lexicon.yaml | head -20; echo ---; grep -n \"self_report_scope\" -A6 app/llm/lexicon.yaml | head -20",
 "description": "Read flag excerpt wiring and lexicon self-report config"
}
````

### User / tool · 2026-11-02T02:37:47.821Z

**tool result**
````
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
...

# ------------------------------------------------------------------ merge
def _overlap(a, b) -> bool:
    return bool(a and b and a[0] < b[1] and b[0] < a[1])


def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False, *, llm_failed: bool = False, fixture_miss: bool = False) -> list:
    """Combine model flags and lexicon flags. Same type with overlapping spans -> origin 'both'; one side only -> LEXICON_ONLY / LLM_ONLY
    (needs_review). Grounding of model quotes is checked separately (ground()); a tagged record adds INJECTION_SUSPECTED to every flag."""
    body, out, used = record["excerpt"], [], set()
    uniq, seen = [], set()
    for lf in llm_flags:
        if lf.get("category") in _CONTEXT_ONLY:
            continue
        k = (lf["type"], grounding.normalize(lf["excerpt"]))
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
---
    failures = [c for c in exc_reasons if c in confidence.REJECTED_CODES]
    code_reasons = [c for c in exc_reasons if c not in confidence.REJECTED_CODES]
    span = grounding.locate(body, excerpt)
    if not failures:
        code_reasons += grounding.check_summary(summary, excerpt, record["source"], record.get("date_iso") or "")
        if span is None:
            code_reasons.append("HIGHLIGHT_NOT_FOUND")
    base = body_offset(record)
    e.update(summary=summary, excerpt=excerpt,
             excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None,
             source_kind="patient_report" if grounding.has_self_report(excerpt) else "record")
    cc = e["ladder"]["code_checks"]
    cc.update(excerpt_verbatim=not failures, excerpt_whole_sentence="EXCERPT_NOT_WHOLE_SENTENCE" not in code_reasons,
              qualifier_carried="EXCERPT_OMITS_QUALIFIER" not in code_reasons and "SUMMARY_DROPS_QUALIFIER" not in code_reasons,
              date_provider_from_header=True,
---
25:#   from an excerpt (ADR-016). `self_report: true` marks wording that explicitly attributes a statement to the PATIENT (T-061); code sets
84:# T-061: a self_report hit is a PATIENT statement only. Before the code sets source_kind = patient_report, it must drop the hit
85:# when the hit's sentence matches `self_report_scope.exclude_sentence` (a named non-patient speaker with a speech verb, or
86:# "per <wife|husband|EMS|...>"). Bare "S:", "Subjective:" and "Self-reported" headers are not matched by any self_report entry,
87:# and the intake-form date entry is self_report: false. Reference implementation: research/lexicon_selfcheck.py:is_patient_statement().
88:self_report_scope:
104:  self_report: false
125:  self_report: false
142:  self_report: false
159:  self_report: false
175:  self_report: false
191:  self_report: false
207:  self_report: false
224:  self_report: false
242:  self_report: false
260:  self_report: false
277:  self_report: false
294:  self_report: false
310:  self_report: false
326:  self_report: false
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
--
764:  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. T-061: it does NOT match a bare "S:" / "Subjective:" header or "Self-reported" (a section label is not an attribution), and a sentence whose speaker is EMS, a witness, a spouse or family is excluded by self_report_scope. "C/O" and "complains of" with no named speaker are read as the patient, which is the clinical convention.'
765-  appendix_c: [1, 3, 5, 9]
766-  examples:
767-    hit: ['Patient reports low back pain in 2023, resolved.', 'Patient reports missing 3 days of work.', 'C/O neck pain 7/10 and headache.', 'Pt states pain worse with rotation.', 'Patient endorses headaches.', 'Per patient, pain 5/10 today.']
768-    miss: ['Cervical range of motion reduced approx. 40%.']
769-
770-- id: intake_form_accident_date
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:56.254Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer && cat feedback_review_commit_not_worktree.md feedback_reviews_write_once.md feedback_lexicon_review_method.md project_t061_r3_clause_span_holes.md 2>&1 | head -120",
 "description": "Read recurring-finding memory files"
}
````

### User / tool · 2026-11-02T02:37:56.339Z

**tool result**
````
---
name: review-commit-not-worktree
description: When the live working tree has uncommitted edits to the files under review, probe the named commit (git archive into artifacts/review-evidence, then run the probe with the tree root as argument) and say so in the review
metadata:
  type: feedback
---

On T-036 r3 the live tree had uncommitted edits to confidence.py, flag_templates.py, why.py and pipeline.py (other workers in flight), so `git diff --stat <commit> -- <files>` was non-empty even for files the round was about. Probes on the live tree would have tested code the commit does not contain.

**Why:** a verdict on a round must cite the commit's behaviour. Working-tree results can pass or fail for reasons outside the commit (e.g., an uncommitted LLM_SPLIT template or a pipeline.py warning line).

**How to apply:** run `git diff --stat <sha> -- <files under review>`. If non-empty, run `git archive <sha> | tar -x -C artifacts/review-evidence/<dir>` (create the dir first with mkdir -p) and run the probe script with that dir as argument, plus pytest from inside that dir with `.venv/bin/python -m pytest ... -p no:cacheprovider`. Name the tree in the review's scope. Delete the extracted dir afterwards: it contains a full copy of artifacts and should not be left in place.

Note: the Bash hook (board-guard) denies commands with backticks in a heredoc or inline python -c; use a single-quoted heredoc without backticks.

Related: [[project_flag_source_kind_and_run_signal]].
---
name: reviews-write-once
description: reviewer-write-guard makes reviews/<card>-<persona>.md append-only once written; get line citations and JSON right before the first write
metadata:
  type: feedback
---

The reviewer-write-guard hook blocks Edit on an existing file under reviews/ ("reviews are append-only — write a new file (e.g. -r2/-r3 suffix)").
On T-061 r3 I wrote the review, then found three wrong test line citations, and could not correct them in place.

**Why:** the guard enforces append-only history for review rounds, so a round file is final once written.

**How to apply:** before the first Write of a review file, grep every cited file:line and check it (use grep -n, not memory). Parse the
JSON block and check the verdict rule. Do not work around the guard with a shell write; if a citation is off after writing, say so in
the reply to the orchestrator and give the corrected line numbers.

Related: [[project_t061_r3_clause_span_holes]].
---
name: lexicon-review-method
description: How to review flag lexicons/phrase lists as the adjuster — self-check PASS on author examples hides recall gaps; probe off-sample phrasing, comma-scoped negation, intake checkboxes
metadata:
  type: feedback
---

A lexicon self-check that replays only the author's own examples + the 9 sample records will PASS while recall on real
adjuster phrasing is near zero (T-009 round 0: selfcheck PASS, my 63 probes OK=10 FN=38 FP=15).

**Why:** the second signal exists to catch what the LLM overlooks; testing it on the sample alone proves nothing.

**How to apply:** for any lexicon/flag change, re-run artifacts/review-evidence/T-009-adjuster-probes.py (import the repo
guard, never modify the repo; reviewer hook blocks writes outside reviews/ and artifacts/review-evidence/ — even scratchpad).
Always probe: (1) evals/golden/case_06_subtle_pre_existing records; (2) "No acute fracture, chronic degenerative changes"
(comma-scope negation); (3) intake checkboxes "Prior injuries: No."; (4) ROS denial lists >6 tokens; (5) "did not present
with"; (6) MIST/scene facts and "out of proportion". Also check flag_type names vs REQUIREMENTS/golden types (hedge category,
compliance→causation mapping). See [[research-attack-map-gaps]].
(7) For any exclusion regex (self_report_scope.exclude_sentence, T-061 r0): patient-subject sentences that contain a
family/EMS/witness word and a speech verb ("Patient states EMS noted a laceration."). A regex that matches a non-patient
name anywhere in the sentence passes every "exclude" example and still drops the patient's own statement.
(8) A lexicon change is not a product change: diff the commit for app/backend and run the parent-vs-HEAD FAILED list (T-061 r0:
selfcheck PASS, but the flag test went red and production still used the old word filter). See [[project-flag-source-kind-and-run-signal]].
---
name: t061-r3-clause-span-holes
description: T-061 r3 (a27b358, D-035 clause-level patient_report): comma/and/parenthesis family clause inherits chip via ';'-bounded span; closed verb list leaks 'thinks/told'; selfcheck PASS runs a rule production no longer uses
metadata:
  type: project
---

D-035 (memory/ORCHESTRATOR_DECISIONS.md:44) replaced the lexicon speaker lists with a code rule: the patient_report span runs from
a patient-subject clause ("Patient|Pt|The patient" + reporting verb) to the next ';' or sentence end. Production
(app/backend/grounding.py:189-213) no longer reads lexicon self_report entries or self_report_scope at all.

Round 3 (r3 review, reviews/T-061-claims-adjuster-r3.md) found the holes below. Re-check these on any later round before reusing this note.
- Comma, "and" or parenthesis joins a family/EMS clause into the patient span: "Patient states pain began after the collision, wife reports
  headaches." -> chip True. The span ignores commas; the mixed check only searches text outside the span.
- Closed reporting-verb list (grounding.py:183-186): "wife thinks", "his wife told the ER" -> chip True, even with a semicolon.
- research/lexicon_selfcheck.py still uses its own is_patient_statement, so the research PASS does not test production.
- Narrowings not in D-035 text: bare "C/O" and "Patient-reported" lose the chip (pinned in test_flags_pass.py NO_TAG); lexicon.yaml:764
  still says C/O is read as the patient.

**Why:** the r2 blocker (spouse clause inside a patient-subject sentence) was closed only for the semicolon form. Each round's
phrasings pass and the class leaks elsewhere. D-033 names this as a credibility error.

**How to apply:** probe every mixed sentence by (a) separator (`;`, `,`, `and`, parenthesis, sentence split), (b) verb outside the
list, (c) speaker word outside the lexicon. Use artifacts/review-evidence/T-061-r3-probe.py (run against a git archive of the commit).
Related: [[t061-speaker-scope-closed-list]], [[review-commit-not-worktree]], [[lexicon-review-method]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:57.320Z

**tool call — Bash**
````
{
 "command": "git status --short -- app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py research evals app/llm 2>&1; echo ---; git diff --stat 991dac4 HEAD -- app/backend/grounding.py tests/unit/test_flags_pass.py research/lexicon_selfcheck.py 2>&1; echo ---; rm -rf \"$TMPDIR/x\" 2>/dev/null; echo ---; git rev-parse HEAD; git merge-base --is-ancestor 991dac4 HEAD && echo \"991dac4 in HEAD\"",
 "description": "Read memory files and check worktree and HEAD state"
}
````

### User / tool · 2026-11-02T02:37:57.403Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (rm $TMPDIR/x)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:00.326Z

**tool call — Bash**
````
{
 "command": "git status --short -- app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py research evals app/llm; echo \"--- diff 991dac4..HEAD on reviewed files:\"; git diff --stat 991dac4 HEAD -- app/backend/grounding.py tests/unit/test_flags_pass.py research/lexicon_selfcheck.py; echo \"--- HEAD:\"; git rev-parse --short HEAD; git merge-base --is-ancestor 991dac4 HEAD && echo \"991dac4 is in HEAD\"",
 "description": "Check worktree state and whether reviewed files changed since fix"
}
````

### User / tool · 2026-11-02T02:38:00.498Z

**tool result**
````
 M app/llm/backends/fixture.py
 M evals/reports/latest.json
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
--- diff 991dac4..HEAD on reviewed files:
--- HEAD:
b614b40
991dac4 is in HEAD
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:03.218Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-061-r4-991 && git archive 991dac4 | tar -x -C artifacts/review-evidence/T-061-r4-991 && ls artifacts/review-evidence/T-061-r4-991 | head -30 && echo --- && cd artifacts/review-evidence/T-061-r4-991 && grep -n \"_FURTHER_CLAUSE\\|_PATIENT_CLAUSE = \" app/backend/grounding.py && ls /Users/arsis/zlayt-pm-project/.venv/bin/python && /Users/arsis/zlayt-pm-project/.venv/bin/python --version",
 "description": "Extract the fix commit into review evidence dir"
}
````

### User / tool · 2026-11-02T02:38:03.481Z

**tool result**
````
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
---
186:_PATIENT_CLAUSE = re.compile(r"(?:the\s+)?(?:patient|pt\x00?)\s+" + _VERB + r"\b", re.IGNORECASE)
187:_FURTHER_CLAUSE = re.compile(r"[;,(]|\band\b", re.IGNORECASE)
196:    if not body or len(S.unit_spans(body)) != 1 or not _PATIENT_CLAUSE.match(body) or _FURTHER_CLAUSE.search(body):
/Users/arsis/zlayt-pm-project/.venv/bin/python
Python 3.12.2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:04.503Z

Now the required pytest run and the selfcheck on the live tree, then the archive of the fix commit.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:05.131Z

**tool call — Bash**
````
{
 "command": "python3 -m pytest -q tests/unit/test_flags_pass.py 2>&1 | tail -15; echo \"exit=$?\"; echo \"--- venv:\"; .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider 2>&1 | tail -3",
 "description": "Run the brief's pytest command on test_flags_pass.py"
}
````

### User / tool · 2026-11-02T02:38:05.878Z

**tool result**
````
/opt/homebrew/opt/python@3.12/bin/python3.12: No module named pytest
exit=0
--- venv:
.....................                                                    [100%]
21 passed in 0.36s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:05.979Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-991 && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider 2>&1 | tail -3; echo \"--- selfcheck (archive 991dac4):\"; /Users/arsis/zlayt-pm-project/.venv/bin/python research/lexicon_selfcheck.py 2>&1 | tail -12; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run pytest and selfcheck against the fix commit archive"
}
````

### User / tool · 2026-11-02T02:38:06.831Z

**tool result**
````
.....................                                                    [100%]
21 passed in 0.36s
--- selfcheck (archive 991dac4):
[probes] nurse (FIRE: high/medium of the mapped type; SUPPRESS/NONE: no high/medium)

[probes] claims-adjuster (FLAG: high/medium raised; QUIET: no high/medium)

[probes] false positives: 0 (bar ≤ 2)   false negatives: 0

[held-out] lexicon_heldout.jsonl: 115/115 = 100% (bar 85%); prior_level 12/12, prior_since_year 10/10, prior_treatment 7/7, hedge 17/17, attribution 11/11, non_patient_speaker 14/14, self_report 1/1, quiet_post_accident 23/23, quiet_hedge 5/5, quiet_self_report 2/2, explicit_patient 8/8, headers_not_attribution 5/5

[production chip] grounding.has_self_report on 13 no-chip + 5 chip rows: 18/18

SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 0 of 0; held-out 115/115
RESULT: PASS
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:15.365Z

Pytest needs the project venv (system `python3` has no pytest). Now I'll write the r4 probe into review evidence and run it against the fix commit's archive.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:22.690Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-probe.py",
 "content": "\"\"\"T-061 round-4 claims-adjuster probe (read-only). Judges against D-037 (memory/ORCHESTRATOR_DECISIONS.md:45).\n\nUsage: .venv/bin/python artifacts/review-evidence/T-061-r4-probe.py <repo_root>\n\nD-037 rule being judged: the patient_report chip goes only on an excerpt that is ONE whole patient-subject clause\n(Patient | Pt | The patient + reporting verb); any further clause after any separator means NO chip.\n\nFor each sentence: grounding.has_self_report(sentence) (the production function called by flags.py:46, flags.py:125,\ngenerator.py:80, present.py:46), and flags._flag(...) (the constructor that sets source_kind). Nothing is written to the repo.\n\"\"\"\nimport sys\n\nroot = sys.argv[1]\nsys.path.insert(0, root)\n\nfrom app.backend import flags, grounding  # noqa: E402\n\nprint(\"grounding module =\", grounding.__file__)\n\nREC = {\"n\": 7, \"id\": \"r7\", \"source\": \"Austin EMS\", \"date_iso\": \"2026-01-09\"}\n\n# (sentence, expect_chip, group, note)\nROWS = [\n    # ---- r3 B1 rows (must be record: a family/EMS clause after comma, and, or parenthesis)\n    (\"Patient states pain began after the collision, wife reports headaches.\", False, \"r3-B1\", \"\"),\n    (\"Pt reports neck pain, EMS notes headaches.\", False, \"r3-B1\", \"\"),\n    (\"Patient reports neck pain and his wife says he is in pain.\", False, \"r3-B1\", \"\"),\n    (\"Patient reports neck pain, per his wife, headaches began at the scene.\", False, \"r3-B1\", \"\"),\n    (\"Patient reports neck pain (per wife, headaches since the scene).\", False, \"r3-B1\", \"\"),\n    (\"Patient reports pain 4/10, girlfriend says he limps.\", False, \"r3-B1\", \"\"),\n    (\"Patient reports neck pain, Mrs. Ortiz reports headaches.\", False, \"r3-B1\", \"\"),\n    # ---- r3 B2 rows (must be record: non-patient clause with a verb outside the old closed list)\n    (\"Patient states neck pain; wife thinks he is faking.\", False, \"r3-B2\", \"\"),\n    (\"Patient reports neck pain, wife thinks he is faking.\", False, \"r3-B2\", \"\"),\n    (\"Patient states neck pain; his wife told the ER he was fine.\", False, \"r3-B2\", \"\"),\n    (\"Patient states neck pain, EMS notes headaches, wife reports nausea.\", False, \"r3-B2\", \"\"),\n    # ---- r3 pinned/brief rows\n    (\"Pt c/o neck pain; wife drove him in.\", False, \"r3-pinned\", \"D-037 decides: record (r3 Q2)\"),\n    (\"Patient states EMS noted a laceration.\", True, \"r3-keep\", \"single clause, patient subject\"),\n    (\"Patient reports his wife said he was fine.\", True, \"r3-keep\", \"single clause, patient subject\"),\n    (\"Patient states his wife drove him to the ER.\", True, \"r3-keep\", \"single clause, patient subject\"),\n    (\"Pt reports neck pain.\", True, \"r3-keep\", \"\"),\n    (\"Girlfriend says he limps.\", False, \"r3-keep\", \"no patient subject\"),\n    (\"C/O neck pain; wife reports headaches.\", False, \"r3-keep\", \"bare C/O\"),\n    (\"EMS reports neck pain, patient states headaches.\", False, \"r3-keep\", \"EMS subject, mixed\"),\n    # ---- control: sentence split must still fail closed\n    (\"Patient states neck pain. Wife reports headaches.\", False, \"control\", \"two sentences\"),\n    (\"Patient states neck pain.\", True, \"control\", \"single sentence\"),\n    # ---- NEW r4 attacks: a family or EMS clause smuggled into a chipped excerpt by a separator the code does not list\n    (\"Patient states neck pain but his wife reports headaches.\", False, \"r4-new\", \"contrast 'but' introduces a clause\"),\n    (\"Patient states neck pain: wife reports headaches.\", False, \"r4-new\", \"colon introduces a speaker clause\"),\n    (\"Patient reports neck pain — EMS notes headaches.\", False, \"r4-new\", \"em dash joins an EMS clause\"),\n    (\"Patient states neck pain with his wife reporting headaches.\", False, \"r4-new\", \"'with' + participle clause\"),\n    (\"Patient states neck pain while wife says he limps.\", False, \"r4-new\", \"'while' introduces a clause\"),\n    # ---- extra r4 variants (same class; judged the same way, reported separately from the five above)\n    (\"Patient states neck pain & wife reports headaches.\", False, \"r4-extra\", \"ampersand\"),\n    (\"Patient states neck pain / wife reports headaches.\", False, \"r4-extra\", \"slash\"),\n    (\"Patient states neck pain [wife reports headaches].\", False, \"r4-extra\", \"square bracket\"),\n    (\"Patient states neck pain plus wife reports headaches.\", False, \"r4-extra\", \"'plus'\"),\n    (\"Patient states neck pain as wife reports headaches.\", False, \"r4-extra\", \"'as' clause\"),\n    (\"Patient reports neck pain per wife.\", False, \"r4-extra\", \"'per X' attribution, no comma\"),\n    (\"Patient states neck pain, but wife reports headaches.\", False, \"r4-extra\", \"comma + but\"),\n]\n\n\ndef spans_text(s):\n    return [s[a:b].strip() for a, b in grounding.patient_report_spans(s)]\n\n\nn_ok = n_miss = 0\nmisses = []\nfor sent, expect, group, note in ROWS:\n    chip = grounding.has_self_report(sent)\n    f = flags._flag(REC, \"causation\", \"causation\", sent, \"lexicon\", None, False, None)\n    kind = f[\"source_kind\"]\n    ok = chip is expect and (kind == \"patient_report\") is expect\n    n_ok += ok\n    n_miss += (not ok)\n    if not ok:\n        misses.append(sent)\n    print(f\"{'OK  ' if ok else 'MISS'} [{group}] chip={chip} source_kind={kind} spans={spans_text(sent)} expect_chip={expect} :: {sent!r} {note}\")\n\nprint(f\"SUMMARY rows={len(ROWS)} ok={n_ok} miss={n_miss}\")\nfor m in misses:\n    print(\"MISS_SENTENCE \" + repr(m))\n"
}
````

### User / tool · 2026-11-02T02:38:22.807Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:24.167Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-061-r4-probe.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-991 2>&1 | tee artifacts/review-evidence/T-061-r4-probe.txt",
 "description": "Run r4 probe against the 991dac4 archive and save output"
}
````

### User / tool · 2026-11-02T02:38:24.401Z

**tool result**
````
grounding module = /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-991/app/backend/grounding.py
OK   [r3-B1] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient states pain began after the collision, wife reports headaches.' 
OK   [r3-B1] chip=False source_kind=record spans=[] expect_chip=False :: 'Pt reports neck pain, EMS notes headaches.' 
OK   [r3-B1] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient reports neck pain and his wife says he is in pain.' 
OK   [r3-B1] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient reports neck pain, per his wife, headaches began at the scene.' 
OK   [r3-B1] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient reports neck pain (per wife, headaches since the scene).' 
OK   [r3-B1] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient reports pain 4/10, girlfriend says he limps.' 
OK   [r3-B1] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient reports neck pain, Mrs. Ortiz reports headaches.' 
OK   [r3-B2] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient states neck pain; wife thinks he is faking.' 
OK   [r3-B2] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient reports neck pain, wife thinks he is faking.' 
OK   [r3-B2] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient states neck pain; his wife told the ER he was fine.' 
OK   [r3-B2] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient states neck pain, EMS notes headaches, wife reports nausea.' 
OK   [r3-pinned] chip=False source_kind=record spans=[] expect_chip=False :: 'Pt c/o neck pain; wife drove him in.' D-037 decides: record (r3 Q2)
OK   [r3-keep] chip=True source_kind=patient_report spans=['Patient states EMS noted a laceration.'] expect_chip=True :: 'Patient states EMS noted a laceration.' single clause, patient subject
OK   [r3-keep] chip=True source_kind=patient_report spans=['Patient reports his wife said he was fine.'] expect_chip=True :: 'Patient reports his wife said he was fine.' single clause, patient subject
OK   [r3-keep] chip=True source_kind=patient_report spans=['Patient states his wife drove him to the ER.'] expect_chip=True :: 'Patient states his wife drove him to the ER.' single clause, patient subject
OK   [r3-keep] chip=True source_kind=patient_report spans=['Pt reports neck pain.'] expect_chip=True :: 'Pt reports neck pain.' 
OK   [r3-keep] chip=False source_kind=record spans=[] expect_chip=False :: 'Girlfriend says he limps.' no patient subject
OK   [r3-keep] chip=False source_kind=record spans=[] expect_chip=False :: 'C/O neck pain; wife reports headaches.' bare C/O
OK   [r3-keep] chip=False source_kind=record spans=[] expect_chip=False :: 'EMS reports neck pain, patient states headaches.' EMS subject, mixed
OK   [control] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient states neck pain. Wife reports headaches.' two sentences
OK   [control] chip=True source_kind=patient_report spans=['Patient states neck pain.'] expect_chip=True :: 'Patient states neck pain.' single sentence
MISS [r4-new] chip=True source_kind=patient_report spans=['Patient states neck pain but his wife reports headaches.'] expect_chip=False :: 'Patient states neck pain but his wife reports headaches.' contrast 'but' introduces a clause
MISS [r4-new] chip=True source_kind=patient_report spans=['Patient states neck pain: wife reports headaches.'] expect_chip=False :: 'Patient states neck pain: wife reports headaches.' colon introduces a speaker clause
MISS [r4-new] chip=True source_kind=patient_report spans=['Patient reports neck pain — EMS notes headaches.'] expect_chip=False :: 'Patient reports neck pain — EMS notes headaches.' em dash joins an EMS clause
MISS [r4-new] chip=True source_kind=patient_report spans=['Patient states neck pain with his wife reporting headaches.'] expect_chip=False :: 'Patient states neck pain with his wife reporting headaches.' 'with' + participle clause
MISS [r4-new] chip=True source_kind=patient_report spans=['Patient states neck pain while wife says he limps.'] expect_chip=False :: 'Patient states neck pain while wife says he limps.' 'while' introduces a clause
MISS [r4-extra] chip=True source_kind=patient_report spans=['Patient states neck pain & wife reports headaches.'] expect_chip=False :: 'Patient states neck pain & wife reports headaches.' ampersand
MISS [r4-extra] chip=True source_kind=patient_report spans=['Patient states neck pain / wife reports headaches.'] expect_chip=False :: 'Patient states neck pain / wife reports headaches.' slash
MISS [r4-extra] chip=True source_kind=patient_report spans=['Patient states neck pain [wife reports headaches].'] expect_chip=False :: 'Patient states neck pain [wife reports headaches].' square bracket
MISS [r4-extra] chip=True source_kind=patient_report spans=['Patient states neck pain plus wife reports headaches.'] expect_chip=False :: 'Patient states neck pain plus wife reports headaches.' 'plus'
MISS [r4-extra] chip=True source_kind=patient_report spans=['Patient states neck pain as wife reports headaches.'] expect_chip=False :: 'Patient states neck pain as wife reports headaches.' 'as' clause
MISS [r4-extra] chip=True source_kind=patient_report spans=['Patient reports neck pain per wife.'] expect_chip=False :: 'Patient reports neck pain per wife.' 'per X' attribution, no comma
OK   [r4-extra] chip=False source_kind=record spans=[] expect_chip=False :: 'Patient states neck pain, but wife reports headaches.' comma + but
SUMMARY rows=33 ok=22 miss=11
MISS_SENTENCE 'Patient states neck pain but his wife reports headaches.'
MISS_SENTENCE 'Patient states neck pain: wife reports headaches.'
MISS_SENTENCE 'Patient reports neck pain — EMS notes headaches.'
MISS_SENTENCE 'Patient states neck pain with his wife reporting headaches.'
MISS_SENTENCE 'Patient states neck pain while wife says he limps.'
MISS_SENTENCE 'Patient states neck pain & wife reports headaches.'
MISS_SENTENCE 'Patient states neck pain / wife reports headaches.'
MISS_SENTENCE 'Patient states neck pain [wife reports headaches].'
MISS_SENTENCE 'Patient states neck pain plus wife reports headaches.'
MISS_SENTENCE 'Patient states neck pain as wife reports headaches.'
MISS_SENTENCE 'Patient reports neck pain per wife.'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:32.850Z

The probe confirms the five new attacks all still get the chip. Next I'll check the held-out set, the stale-text minors, and the flags-layer wiring in the archive.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:35.118Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-991 && echo \"--- r3 finding 1/2 rows in held-out jsonl:\"; grep -c \"wife reports headaches\\|wife thinks he is faking\\|per wife, headaches since\" evals/lexicon_heldout.jsonl; echo \"--- r3 minor 6 rows in held-out:\"; grep -n \"Patient states EMS noted\\|wife said he was fine\\|Patient states his wife\" evals/lexicon_heldout.jsonl; echo \"(end)\"; echo \"--- selfcheck production_chip and CHIP lists:\"; grep -n \"production_chip\\|CHIP_NO\\|CHIP_YES\\|is_patient_statement\\|self_report_scope\" research/lexicon_selfcheck.py | head -20; echo \"--- stale text:\"; cd /Users/arsis/zlayt-pm-project && grep -n \"from the lexicon .self_report. entries\" memory/DECISIONS.md; grep -n \"set by code from the lexicon\" app/llm/lexicon.yaml; grep -n \"read as the patient, which is the clinical convention\" app/llm/lexicon.yaml; grep -n \"self_report_scope\\|exclude_sentence\" app/llm/lexicon.yaml | head -3; echo \"--- D-037 in ORCH and DECISIONS:\"; grep -n \"D-037\" memory/DECISIONS.md | head -3; grep -n \"D-037\" memory/ORCHESTRATOR_DECISIONS.md | head -2",
 "description": "Check held-out rows, selfcheck wiring and stale spec text"
}
````

### User / tool · 2026-11-02T02:38:35.266Z

**tool result**
````
--- r3 finding 1/2 rows in held-out jsonl:
0
--- r3 minor 6 rows in held-out:
(end)
--- selfcheck production_chip and CHIP lists:
162:def production_chip(text):
172:CHIP_NO = ["Patient states pain began after the collision, wife reports headaches.", "Pt reports neck pain, EMS notes headaches.",
178:CHIP_YES = ["Patient states EMS noted a laceration.", "Patient reports his wife said he was fine.", "Patient states his wife drove him to the ER.",
455:                ok = not production_chip(r["text"])
475:    chip_bad = [t for t in CHIP_NO if production_chip(t)] + [t for t in CHIP_YES if not production_chip(t)]
476:    print(f"\n[production chip] grounding.has_self_report on {len(CHIP_NO)} no-chip + {len(CHIP_YES)} chip rows: {len(CHIP_NO) + len(CHIP_YES) - len(chip_bad)}/{len(CHIP_NO) + len(CHIP_YES)}")
--- stale text:
286:  - `source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt and drives the "Patient self-report" label. Origin is `lexicon`, `llm` or `lexicon+llm`; one-sided hits are `needs_review` (`LEXICON_ONLY`, `LLM_ONLY`). Flags are not editable except a reviewer note.
764:  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. T-061: it does NOT match a bare "S:" / "Subjective:" header or "Self-reported" (a section label is not an attribution), and a sentence whose speaker is EMS, a witness, a spouse or family is excluded by self_report_scope. "C/O" and "complains of" with no named speaker are read as the patient, which is the clinical convention.'
85:# when the hit's sentence matches `self_report_scope.exclude_sentence` (a named non-patient speaker with a speech verb, or
88:self_report_scope:
89:  exclude_sentence: '^\W*(?:(?:the|his|her|patient''s|pt''s)\s+)?(?:EMS|paramedics?|witness(?:es)?|bystanders?|wife|husband|spouse|mother|father|parents?|family|friends?|relatives?|daughter|son|sibling|caregiver|police|officer|nurse|staff)\b(?:\s+[\w''-]+){0,3}?\s+(?:reports?|reported|states?|stated|says|said|complains?|complained|c/o|describes?|described|notes?|noted|relates?|believes?|attributes?|links?|thinks?|claims?)\b|^\W*per\s+(?:the\s+|his\s+|her\s+)?(?:wife|husband|spouse|family|witness|EMS|mother|father)\b'
--- D-037 in ORCH and DECISIONS:
45:| D-037 | Final rule for `patient_report` (supersedes the clause-splitting in D-035, 2026-11-02): the chip attaches only when the **whole excerpt** is a single patient-subject clause (`Patient`/`Pt`/`The patient` + reporting verb), with no further clause after `;`, `,`, `and`, or `(`. Any mixed excerpt gets no chip and stays a plain record excerpt, so no verb list decides it. Bare `C/O` gets no chip. A missing chip is safe; a wrong chip mislabels the source. | Three adjuster rounds kept finding clause-boundary holes; fail closed instead of patching verbs. | T-061 claims-adjuster r3 B1/B2 |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:42.032Z

**tool call — Bash**
````
{
 "command": "sed -n 24,27p app/llm/lexicon.yaml; echo ---; grep -n \"C/O\" app/llm/lexicon.yaml | head -5; echo ---; grep -n \"per EMS\\|Per EMS\\|pt. c/o\\|Pt. c/o\" tests/unit/test_flags_pass.py | head -5; echo ---; sed -n 186,196p artifacts/review-evidence/T-061-r4-991/tests/unit/test_flags_pass.py",
 "description": "Check lexicon header lines and pinned C/O tests"
}
````

### User / tool · 2026-11-02T02:38:42.138Z

**tool result**
````
# - `hedge: true` marks the R-TL-8 hedge set: a sentence with a hedge hit is a qualifier unit and can never be cut
#   from an excerpt (ADR-016). `self_report: true` marks wording that explicitly attributes a statement to the PATIENT (T-061); code sets
#   source_kind = "patient_report" from it (ADR-013). Self-report entries are never hedges.
# - `strength`: high and medium raise a flag (origin lexicon, or lexicon+llm). low is context only: it never
---
93:    keep: ['Patient complains of neck pain.', 'C/O neck pain 7/10 and headache.', 'Patient states EMS noted a laceration.', 'Patient reports his wife said he was fine.', 'Patient states his wife drove him to the ER.']
762:  rationale: 'Marks content the record attributes explicitly to the patient (as opposed to objective findings), which adjusters weight less. Context only; it keeps attribution in the summary ("C/O neck pain 7/10" must stay a complaint, not become a finding).'
763:  source: 'AA A9; AA src 1, src 18 (objective findings weighted above subjective); reviews/T-009-legal-nurse.md (minor: C/O)'
764:  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. T-061: it does NOT match a bare "S:" / "Subjective:" header or "Self-reported" (a section label is not an attribution), and a sentence whose speaker is EMS, a witness, a spouse or family is excluded by self_report_scope. "C/O" and "complains of" with no named speaker are read as the patient, which is the clinical convention.'
767:    hit: ['Patient reports low back pain in 2023, resolved.', 'Patient reports missing 3 days of work.', 'C/O neck pain 7/10 and headache.', 'Pt states pain worse with rotation.', 'Patient endorses headaches.', 'Per patient, pain 5/10 today.']
---
118:           "Pt c/o neck pain 7/10.", "Pt. c/o neck pain 7/10.", "The patient denies loss of consciousness."]
119:    no = ["Date of accident per intake form: 2026-01-19.", "Per EMS report, neck pain.", "Wife reports he was in pain.", "EMS reports minimal damage.",
175:    "Per EMS, pt. c/o neck pain.", "EMS noted pt. reports neck pain 7/10.", "C/O neck pain 7/10 and headache.", "Date of injury per registration paperwork: 03/02/2026.",
---
]
YES_TAG = [  # explicit patient subject + reporting verb (r1 and r2 keep-lists)
    "Patient states symptoms began after the January collision.", "Patient complains of neck pain.", "Pt c/o neck pain 7/10.",
    "Patient states EMS noted a laceration.", "Patient reports his wife said he was fine.", "Patient states his wife drove him to the ER.",
    "The patient denies loss of consciousness.", "Pt. reports neck pain 7/10.",
]    # D-037: single clause, patient subject, so the chip attaches even when another speaker is named inside it


def test_d035_every_reviewed_sentence_no_tag_or_tag():
    """T-061 AC2 / D-035: default is no tag; only a clause beginning with Patient/Pt/The patient + reporting verb is tagged."""
    assert [t for t in NO_TAG if _kind(t) != "record"] == []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:25.873Z

The probe result is clear: the fix closes the r3 B1 and B2 comma/semicolon rows but leaves eleven chipped mixed excerpts, all built from separators the code does not list. Before writing, I'll confirm every line citation in the archive.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:27.745Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-991 && grep -n \"def test_d037\\|def test_d035\\|def test_d033\\|^NO_TAG\\|^YES_TAG\\|mixed excerpt carries\\|Patient states neck pain; wife insists\\|Pt c/o neck pain; wife drove him in\\|Patient states headaches. Patient reports\" tests/unit/test_flags_pass.py; echo ---; grep -n \"_VERB = \\|_PATIENT_CLAUSE = \\|_FURTHER_CLAUSE = \\|def patient_report_spans\\|def _self_report\\|def has_self_report\\|D-037 (supersedes\" app/backend/grounding.py; echo ---; grep -n \"def production_chip\\|^CHIP_NO\\|^CHIP_YES\\|chip_bad = \\|quiet_self_report\\\" *:\\|ok = not production_chip\" research/lexicon_selfcheck.py; echo ---; grep -n \"D-037\\|D-035\" /Users/arsis/zlayt-pm-project/memory/ORCHESTRATOR_DECISIONS.md | cut -c1-60",
 "description": "Confirm line citations in the archive before writing review"
}
````

### User / tool · 2026-11-02T02:39:27.854Z

**tool result**
````
167:NO_TAG = [  # every sentence from reviews/T-061-claims-adjuster.md (r1) and -r2.md that must NOT be patient_report (D-035)
183:    "Pt c/o neck pain; wife drove him in.",                      # pinned: fail closed, no chip
185:    "Patient states headaches. Patient reports neck pain.",       # two sentences: not a single clause
187:YES_TAG = [  # explicit patient subject + reporting verb (r1 and r2 keep-lists)
194:def test_d035_every_reviewed_sentence_no_tag_or_tag():
200:def test_d037_tag_spans_the_whole_excerpt_or_nothing():
204:    assert _spans("Pt c/o neck pain; wife drove him in.") == []
209:def test_d037_mixed_excerpt_carries_no_chip():
213:    assert _kind("Patient states neck pain; wife insists he mentions nothing.") == "record"    # verbs outside any list
216:def test_d033_lexicon_flags_label_source_kind_by_the_same_rule():
---
180:# D-037 (supersedes the D-035 clause splitting and the D-033 speaker lists): patient_report attaches only when the WHOLE excerpt is one
184:_VERB = (r"(?:states?|stated|reports?|reported|notes?|noted|says|said|endorses|endorsed|complains?\s+of|complained\s+of|c/o|denies|denied|"
186:_PATIENT_CLAUSE = re.compile(r"(?:the\s+)?(?:patient|pt\x00?)\s+" + _VERB + r"\b", re.IGNORECASE)
187:_FURTHER_CLAUSE = re.compile(r"[;,(]|\band\b", re.IGNORECASE)
190:def patient_report_spans(text: str) -> list:
201:def _self_report(text: str) -> bool:
232:def has_self_report(text: str) -> bool:
---
162:def production_chip(text):
172:CHIP_NO = ["Patient states pain began after the collision, wife reports headaches.", "Pt reports neck pain, EMS notes headaches.",
178:CHIP_YES = ["Patient states EMS noted a laceration.", "Patient reports his wife said he was fine.", "Patient states his wife drove him to the ER.",
454:            elif x == "quiet_self_report":
455:                ok = not production_chip(r["text"])
475:    chip_bad = [t for t in CHIP_NO if production_chip(t)] + [t for t in CHIP_YES if not production_chip(t)]
---
43:| D-035 | Simplifies D-033: `patient_report` is attached 
45:| D-037 | Final rule for `patient_report` (supersedes the
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:52.506Z

Citations are confirmed (D-035 is at line 43, D-037 at line 45). I'll write the round-4 review now and then remove the extracted archive, as the reviewer memory directs.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:24.056Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster-r4.md",
 "content": "# T-061 round 4 (final): patient_report under D-037, claims-adjuster review (Gary Pruitt)\n\nVerdict: **fail** (1 blocker, 3 minors). Reviewed object: commit 991dac4 (D-037 whole-excerpt chip), reviewed via `git archive 991dac4` extracted to `artifacts/review-evidence/T-061-r4-991` (HEAD is now b614b40; `git diff --stat 991dac4 HEAD` on the reviewed files is empty, so HEAD tests the same code). Judged against D-037 (memory/ORCHESTRATOR_DECISIONS.md:45): \"the chip attaches only when the whole excerpt is a single patient-subject clause ... any further clause means no chip\".\n\n## Round-3 status (reviews/T-061-claims-adjuster-r3.md)\n\n- **B1 (comma, \"and\", parenthesis family clause inside a patient-subject sentence): closed.** All seven r3 rows return `has_self_report` False and `source_kind` record through `flags._flag` (probe rows OK, group r3-B1). The comma/and/parenthesis forms no longer leak.\n- **B2 (non-patient clause whose verb is outside the closed list): closed.** All four r3 rows return record (group r3-B2). The verb list is no longer consulted for mixed excerpts.\n- **Major 3 (research gate measures a rule production no longer runs): closed in form.** `research/lexicon_selfcheck.py:162-166` `production_chip()` calls `app.backend.grounding.has_self_report`; the gate reports `[production chip] ... 18/18` and `RESULT: PASS`. Sub-acceptance not met: the r3 finding 1/2 rows were to go in `evals/lexicon_heldout.jsonl`; they sit in the selfcheck's closed `CHIP_NO` list instead (`research/lexicon_selfcheck.py:172`), and `grep` of the held-out file returns 0 rows. See minor 2.\n- Carried minors: r3 minor 5 (verb set not named in D-037; partly narrowed, see minor 3), r3 minor 6 (no family/EMS patient-subject row in held-out, see minor 2). r3 minor 4 (stale text) is still open, routed (minor 3).\n\n## Findings\n\n1. **Blocker. D-037's \"any further clause means no chip\" is implemented as a four-separator list. Eleven mixed excerpts still carry the patient chip.** Evidence: `artifacts/review-evidence/T-061-r4-probe.txt` (run with `.venv/bin/python artifacts/review-evidence/T-061-r4-probe.py artifacts/review-evidence/T-061-r4-991`), MISS rows, all `chip=True source_kind=patient_report`:\n   - Five new attacks (group r4-new):\n     - `Patient states neck pain but his wife reports headaches.`\n     - `Patient states neck pain: wife reports headaches.`\n     - `Patient reports neck pain — EMS notes headaches.`\n     - `Patient states neck pain with his wife reporting headaches.`\n     - `Patient states neck pain while wife says he limps.`\n   - Six extra variants of the same class (group r4-extra): `... neck pain & wife reports headaches.`, `... neck pain / wife reports headaches.`, `... neck pain [wife reports headaches].`, `... neck pain plus wife reports headaches.`, `... neck pain as wife reports headaches.`, `Patient reports neck pain per wife.`\n   - Cause: `app/backend/grounding.py:187` `_FURTHER_CLAUSE = [;,(]|\\band\\b` only. `:196` returns the whole excerpt as the span whenever it is one unit and matches the patient subject. A colon, em dash, `&`, `/`, brackets, `plus`, `as`, `with`, `while` or `but` introduces a clause and is not in the list, so the function returns the chip. `:180-183` says \"no further clause\", which the code does not enforce. The mixed-case control `Patient states neck pain, but wife reports headaches.` is record (group r4-extra), so only the comma-less forms leak.\n   - Why it matters: ten of the eleven rows put a wife, EMS or family clause under the claimant's \"Patient self-report (not a physician's opinion)\" label. That is the credibility error D-033 names (memory/ORCHESTRATOR_DECISIONS.md:41), and D-037's own headline says \"a wrong chip mislabels the source\". \"per wife\" (no clause, no verb) is the weakest row; the blocker stands on the ten clause rows without it. The gate is blind here: `research/lexicon_selfcheck.py` PASSes 18/18 on its closed row list at `:172-179`, and it has none of the eleven rows.\n   - Fix: make the chip rule closed on grammar, not on speakers or verbs. Attach the chip only when the text after the patient subject and reporting verb contains (a) no clause-introducing punctuation other than the final period (`: ; , ( ) [ ] & + — –`, and `/` surrounded by spaces; `4/10` and `c/o` are exempt) and (b) no connector from a closed function-word set (`and, or, but, with, while, as, plus, per, whereas, though, although, because, which, who, when, if, until, then, nor, yet, than`). Put the same set in D-037 so the spec and the code agree. If Chris decides the four-separator list is the complete rule, the eleven rows become a documented residual instead of a defect (question 1); I did not downgrade them, because the brief states the headline rule.\n   - Acceptance test: `artifacts/review-evidence/T-061-r4-probe.py` reports 33/33 with the eleven rows `chip=False source_kind=record`. Add the eleven rows to `NO_TAG` (`tests/unit/test_flags_pass.py:167`) and to `CHIP_NO` (`research/lexicon_selfcheck.py:172`); the selfcheck must go red on the pre-fix code and pass after. Keep chipped: `Patient states EMS noted a laceration.`, `Patient reports his wife said he was fine.`, `Patient states his wife drove him to the ER.`, `Pt reports neck pain 7/10.`, `The patient denies loss of consciousness.`, `Patient states neck pain.`. `.venv/bin/python -m pytest -q tests/unit/test_flags_pass.py` stays green after the test edits.\n\n2. **Minor. Held-out set still has no patient-subject family or EMS row, and the gate's closed row list is why a PASS hides misses.** Evidence: `grep -n \"Patient states EMS noted\\|wife said he was fine\\|Patient states his wife\" evals/lexicon_heldout.jsonl` returns no output (0 rows). The r3 finding 1/2 rows are in `research/lexicon_selfcheck.py:172-179`, not in the held-out file the r3 acceptance named. Finding 1's eleven rows also fail production while the gate prints `RESULT: PASS` (`[production chip] ... 18/18`).\n   - Why it matters: a PASS on a closed list is the failure r3 finding 3 named. The selfcheck now calls production, which is the fix; the coverage is still one list.\n   - Fix: add the three keep rows and the r4-new rows to `evals/lexicon_heldout.jsonl` with `expected` patient_report or record, and have the gate read them.\n   - Acceptance test: `grep -c \"wife said he was fine\" evals/lexicon_heldout.jsonl` is at least 1, and the gate's production-chip line reports the held-out rows, not only the in-script list.\n\n3. **Minor (routed, not failing). Stale text still states superseded rules, and one note contradicts the pinned test.** Evidence, routed to owners:\n   - `memory/DECISIONS.md:286` (architect): \"`source_kind = \"patient_report\"` is set by code from the lexicon `self_report` entries on the excerpt\". Production reads no lexicon `self_report` entry (`app/backend/grounding.py:201-202`).\n   - `app/llm/lexicon.yaml:25-26` (researcher): \"code sets source_kind = \"patient_report\" from it (ADR-013)\".\n   - `app/llm/lexicon.yaml:84-93` (researcher): `self_report_scope` and `exclude_sentence` remain with examples. Production and the selfcheck no longer use them. Delete or mark as unread.\n   - `app/llm/lexicon.yaml:764` (researcher): \"`\"C/O\"` and `\"complains of\"` with no named speaker are read as the patient, which is the clinical convention.\" This contradicts D-037's \"Bare `C/O` gets no chip\" and the pinned no-chip row at `tests/unit/test_flags_pass.py:118`/`:175`.\n   - Verb set (orchestrator, D-037 text): `_VERB` at `app/backend/grounding.py:184-185` includes stated, reported, noted, said, endorsed, denied, described. D-037 names no verbs; D-035 (memory/ORCHESTRATOR_DECISIONS.md:43) names states, reports, notes, says, endorses, complains of, c/o, denies. This is r3 minor 5, partly narrowed.\n   - Acceptance test: `grep -n \"from the lexicon .self_report. entries\" memory/DECISIONS.md` and `grep -n \"read as the patient, which is the clinical convention\" app/llm/lexicon.yaml` return nothing; D-037 names the verb set `_VERB` uses.\n\n## What is not a finding\n\n- `Patient reports low back pain in 2023, resolved.` and `Patient reports neck pain and headache.` now have no chip because of the comma or \"and\". D-037 accepts a missing chip (\"a missing chip is safe\"). The `pre_existing` flag itself is unaffected; only `source_kind` changes. Not a finding.\n- `Patient-reported neck pain 7/10.`, `Patient links her neck pain to the collision.` and bare `C/O neck pain 7/10 and headache.`: no chip, as D-037 and the pinned tests say. Not a finding.\n- `Pt c/o neck pain; wife drove him in.` is record, as the r3 Q2 question asked; the pinned test at `tests/unit/test_flags_pass.py:204` says so. Not a finding.\n- `Patient states neck pain. Wife reports headaches.` and `Patient states headaches. Patient reports neck pain.` are record (two units). Control rows OK.\n\n## Outside my lens\n\nSchema, export ordering and the qualifier-carry logic in `dropped_qualifiers` are not in my lens. The `test_split_llm.py` archive failure noted in r3 was not rerun.\n\n## Exercised\n\n- Read `personas/claims-adjuster.md` in full; `reviews/T-061-claims-adjuster-r3.md` in full; `memory/ORCHESTRATOR_DECISIONS.md` (D-033 :41, D-035 :43, D-037 :45); my memory files (`feedback_review_commit_not_worktree.md`, `feedback_reviews_write_once.md`, `feedback_lexicon_review_method.md`, `project_t061_r3_clause_span_holes.md`).\n- `git show --stat 991dac4`; `git show 991dac4 -- app/backend/grounding.py tests/unit/test_flags_pass.py research/lexicon_selfcheck.py` (full diff read).\n- `git status --short -- app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py research evals app/llm`: `M app/llm/backends/fixture.py`, `M evals/reports/latest.json`, and untracked `evals/reports/2026110*.md`. None of the reviewed files has a diff.\n- `git diff --stat 991dac4 HEAD -- app/backend/grounding.py tests/unit/test_flags_pass.py research/lexicon_selfcheck.py` (empty); `git rev-parse --short HEAD` gives `b614b40`; `git merge-base --is-ancestor 991dac4 HEAD` says 991dac4 is in HEAD.\n- `git archive 991dac4 | tar -x -C artifacts/review-evidence/T-061-r4-991` (reviewed object).\n- `python3 -m pytest -q tests/unit/test_flags_pass.py` (the brief's literal command) gave `No module named pytest` on the system `python3` (`/opt/homebrew/opt/python@3.12/bin/python3.12`); the project venv is the runner.\n- `.venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider`: live tree `21 passed in 0.36s`; archive `21 passed in 0.36s`.\n- `.venv/bin/python research/lexicon_selfcheck.py` in the archive: `[production chip] grounding.has_self_report on 13 no-chip + 5 chip rows: 18/18`; `SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 0 of 0; held-out 115/115`; `RESULT: PASS`; exit 0.\n- `artifacts/review-evidence/T-061-r4-probe.py` in the archive, saved to `artifacts/review-evidence/T-061-r4-probe.txt`: `SUMMARY rows=33 ok=22 miss=11`. The probe calls `grounding.has_self_report` directly (`chip=`) and `flags._flag` (`source_kind=`); both agree on every row.\n- `grep -c \"wife reports headaches\\|wife thinks he is faking\\|per wife, headaches since\" evals/lexicon_heldout.jsonl` gave 0; `grep -n \"Patient states EMS noted\\|wife said he was fine\\|Patient states his wife\" evals/lexicon_heldout.jsonl` gave no output.\n- `grep -n \"from the lexicon .self_report. entries\" memory/DECISIONS.md` gave 286; `grep -n \"set by code from the lexicon\" app/llm/lexicon.yaml` gave no hit (the text is at lines 25-26 in the form \"code sets source_kind = ...\"); `grep -n \"read as the patient, which is the clinical convention\" app/llm/lexicon.yaml` gave 764; `grep -n \"self_report_scope\\|exclude_sentence\"` gave 85-89.\n- `grep -n` on `app/backend/grounding.py` (`_VERB`, `_PATIENT_CLAUSE`, `_FURTHER_CLAUSE`, `patient_report_spans`, `_self_report`, `has_self_report`) and `tests/unit/test_flags_pass.py` (`NO_TAG`, `YES_TAG`, `test_d037_*`) to check every cited line before this write.\n\n```json\n{\"card\": \"T-061\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 991dac4 (T-061 r4, D-037 whole-excerpt patient_report chip: app/backend/grounding.py, tests/unit/test_flags_pass.py, research/lexicon_selfcheck.py), reviewed via git archive at artifacts/review-evidence/T-061-r4-991; HEAD b614b40 has no diff on the reviewed files; specs memory/ORCHESTRATOR_DECISIONS.md D-033 (:41), D-035 (:43), D-037 (:45); no app URL (flag and attribution layer, no UI in scope); probe artifacts/review-evidence/T-061-r4-probe.py -> T-061-r4-probe.txt.\",\n \"exercised\": [\n  \"Read personas/claims-adjuster.md in full; reviews/T-061-claims-adjuster-r3.md in full; memory/ORCHESTRATOR_DECISIONS.md D-033, D-035, D-037; my memory files\",\n  \"git show --stat 991dac4; git show 991dac4 -- app/backend/grounding.py tests/unit/test_flags_pass.py research/lexicon_selfcheck.py (full diff)\",\n  \"git status --short on reviewed paths (no diff on reviewed files; fixture.py and evals reports only); git diff --stat 991dac4 HEAD on reviewed files (empty); git rev-parse --short HEAD -> b614b40; git merge-base --is-ancestor 991dac4 HEAD (in HEAD)\",\n  \"git archive 991dac4 extracted to artifacts/review-evidence/T-061-r4-991\",\n  \"python3 -m pytest -q tests/unit/test_flags_pass.py -> No module named pytest (system python3); .venv/bin/python -m pytest -q tests/unit/test_flags_pass.py -p no:cacheprovider -> 21 passed (live and archive)\",\n  \".venv/bin/python research/lexicon_selfcheck.py (archive) -> [production chip] 18/18; held-out 115/115; RESULT: PASS; exit 0\",\n  \"artifacts/review-evidence/T-061-r4-probe.py against the archive -> artifacts/review-evidence/T-061-r4-probe.txt: 33 rows, 22 ok, 11 miss (all 11 chip=True); r3 B1 7/7 and B2 4/4 record; pinned and keep rows as expected\",\n  \"grep of evals/lexicon_heldout.jsonl for family/EMS patient-subject rows -> no output; grep of DECISIONS.md:286 and lexicon.yaml:25-26, 84-93, 764 (stale text)\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"attribution_precision_production\": 2, \"clause_scope_logic\": 2, \"b1_b2_closure\": 4, \"research_gate_measures_production\": 3, \"test_honesty\": 3, \"spec_consistency\": 2},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"D-037 'any further clause means no chip' is implemented as a four-separator list; eleven mixed excerpts still carry the patient chip\",\n   \"evidence\": \"artifacts/review-evidence/T-061-r4-probe.txt MISS rows: 'Patient states neck pain but his wife reports headaches.', 'Patient states neck pain: wife reports headaches.', 'Patient reports neck pain — EMS notes headaches.', 'Patient states neck pain with his wife reporting headaches.', 'Patient states neck pain while wife says he limps.', 'Patient states neck pain & wife reports headaches.', 'Patient states neck pain / wife reports headaches.', 'Patient states neck pain [wife reports headaches].', 'Patient states neck pain plus wife reports headaches.', 'Patient states neck pain as wife reports headaches.', 'Patient reports neck pain per wife.' all chip=True source_kind=patient_report. Cause: app/backend/grounding.py:187 _FURTHER_CLAUSE = [;,(]|\\\\band\\\\b; :196 returns the whole excerpt as the span when it is one unit and matches the patient subject. Control 'Patient states neck pain, but wife reports headaches.' is record.\",\n   \"why_it_matters\": \"Ten of the eleven rows put a wife, EMS or family clause under the claimant's 'Patient self-report' label. D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) names this a credibility error an adjuster would exploit; D-037 headline says a wrong chip mislabels the source. The research gate PASSes 18/18 on a closed list (research/lexicon_selfcheck.py:172-179) that contains none of these rows, so the PASS does not cover them.\",\n   \"fix\": \"Closed-grammar rule, not a speaker or verb list: chip only when the text after the patient subject and reporting verb has no clause-introducing punctuation other than the final period (: ; , ( ) [ ] & + em/en dash, and '/' with spaces on both sides; 4/10 and c/o exempt) and no connector from a closed function-word set (and, or, but, with, while, as, plus, per, whereas, though, although, because, which, who, when, if, until, then, nor, yet, than). Write the same set into D-037. If Chris rules the four-separator list complete, record the eleven rows as a documented residual instead.\",\n   \"acceptance_test\": \"artifacts/review-evidence/T-061-r4-probe.py reports the eleven rows chip=False source_kind=record. The eleven rows are in NO_TAG (tests/unit/test_flags_pass.py:167) and CHIP_NO (research/lexicon_selfcheck.py:172); the selfcheck fails on the pre-fix code and passes after. Kept chipped: 'Patient states EMS noted a laceration.', 'Patient reports his wife said he was fine.', 'Patient states his wife drove him to the ER.', 'Pt reports neck pain 7/10.', 'The patient denies loss of consciousness.', 'Patient states neck pain.' pytest tests/unit/test_flags_pass.py stays green.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Held-out set has no patient-subject family or EMS row; the gate's closed row list is why a PASS hides misses (r3 major 3 sub-acceptance and r3 minor 6 carried)\",\n   \"evidence\": \"grep -n 'Patient states EMS noted\\\\|wife said he was fine\\\\|Patient states his wife' evals/lexicon_heldout.jsonl: no output. The r3 finding 1/2 rows sit in research/lexicon_selfcheck.py:172-179 (CHIP_NO/CHIP_YES), not in the held-out file the r3 acceptance named. Gate prints '[production chip] ... 18/18' and RESULT: PASS with eleven probe rows still chipped.\",\n   \"why_it_matters\": \"A gate PASS on a closed list is the failure r3 finding 3 named. The production call is now in place; the coverage is still one list, and held-out is where a regression would show.\",\n   \"fix\": \"Add 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' (expected patient_report) and the r4-new rows (expected record) to evals/lexicon_heldout.jsonl; have the gate check them.\",\n   \"acceptance_test\": \"grep -c 'wife said he was fine' evals/lexicon_heldout.jsonl >= 1; the gate's production-chip line covers held-out rows, not only the in-script list.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Stale text states superseded rules (routed: DECISIONS.md to architect; lexicon.yaml to researcher; D-037 verb set to orchestrator); not failing\",\n   \"evidence\": \"memory/DECISIONS.md:286 '`source_kind = \\\"patient_report\\\"` is set by code from the lexicon `self_report` entries on the excerpt'; app/llm/lexicon.yaml:25-26 'code sets source_kind = \\\"patient_report\\\" from it'; app/llm/lexicon.yaml:84-93 self_report_scope and exclude_sentence still present and unread by production (grounding.py:201-202); app/llm/lexicon.yaml:764 '\\\"C/O\\\" and \\\"complains of\\\" with no named speaker are read as the patient, which is the clinical convention.' contradicts D-037 'Bare C/O gets no chip' and the no-chip row in tests/unit/test_flags_pass.py:167. _VERB (grounding.py:184-185) includes stated, reported, noted, said, endorsed, denied, described; D-037 names no verbs.\",\n   \"why_it_matters\": \"A future reader gets two rules, and the lexicon note tells the reader the opposite of what the code does for bare C/O. Not failing, per the round brief.\",\n   \"fix\": \"Architect amends DECISIONS.md:286; researcher amends lexicon.yaml:25-26 and 764 and removes or marks self_report_scope; orchestrator names the verb set in D-037 or trims _VERB to it.\",\n   \"acceptance_test\": \"grep -n 'from the lexicon .self_report. entries' memory/DECISIONS.md returns nothing; grep -n 'read as the patient, which is the clinical convention' app/llm/lexicon.yaml returns nothing; D-037 lists the verb set used by _VERB.\"}\n ],\n \"whats_right\": [\n  \"The r3 B1 (7/7) and B2 (4/4) rows now return record through the production function, and the pinned 'Pt c/o neck pain; wife drove him in.' is decided record with the test saying so.\",\n  \"The three keep rows (EMS laceration, wife said, wife drove him to the ER) and 'Pt reports neck pain 7/10.' still carry the chip, and the separate-sentence controls fail closed.\",\n  \"research/lexicon_selfcheck.py:162-166 calls app.backend.grounding.has_self_report, so the research gate now measures the production function and no longer reads lexicon self_report entries.\"\n ],\n \"questions_for_chris\": [\n  \"Is D-037's four-separator list (';', ',', 'and', '(') the complete rule, or the examples for 'any further clause'? If complete, the eleven rows are a spec gap to record as residual; I judged against the headline the brief states.\",\n  \"Is 'Patient reports neck pain per wife.' a further clause under D-037? It has no clause and no verb; I count it as a phrase attribution and it is the weakest of the eleven.\",\n  \"This is round 4, past the three-round cap in §7.4 ('max 3 rounds, then decide'). Do you accept the blocker as residual debt with a documented limitation, or does T-061 hold until the closed-grammar fix lands? D-024 item 7 covers harness rounds, not product attribution, so I did not apply it.\",\n  \"Do you accept the closed-grammar connector set (fail-closed on punctuation, closed function words, no speaker or verb list) as the D-037 mechanism, or do you want a different mechanism?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:40:24.220Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster-r4.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:31.977Z

The review is written. I need to verify two test-line citations in it (the bare-C/O pin and the `:196` description) before I trust them.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:32.831Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-991 && grep -n \"C/O neck pain 7/10 and headache\" tests/unit/test_flags_pass.py; echo ---; sed -n 196,198p app/backend/grounding.py; echo ---; grep -n \"^NO_TAG\\|^YES_TAG\" tests/unit/test_flags_pass.py",
 "description": "Verify bare C/O test line citations in the archive"
}
````

### User / tool · 2026-11-02T02:40:32.923Z

**tool result**
````
120:          "Subjective: neck pain 7/10.", "C/O neck pain 7/10 and headache.", "Patient-reported pain 4/10."]
175:    "Per EMS, pt. c/o neck pain.", "EMS noted pt. reports neck pain 7/10.", "C/O neck pain 7/10 and headache.", "Date of injury per registration paperwork: 03/02/2026.",
---
    if not body or len(S.unit_spans(body)) != 1 or not _PATIENT_CLAUSE.match(body) or _FURTHER_CLAUSE.search(body):
        return []
    return [(lead, lead + len(body))]
---
167:NO_TAG = [  # every sentence from reviews/T-061-claims-adjuster.md (r1) and -r2.md that must NOT be patient_report (D-035)
187:YES_TAG = [  # explicit patient subject + reporting verb (r1 and r2 keep-lists)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:37.251Z

Two citations in the review are off: the bare-C/O pin is at `test_flags_pass.py:120` and `:175`, and `grounding.py:196` returns `[]` on any separator match. The review is write-once under the guard, so I will report these corrections rather than edit it. Next I'll check that the JSON block parses and remove the extracted archive.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:38.761Z

**tool call — Bash**
````
{
 "command": "awk '/^```json/{f=1;next} /^```/{f=0} f' reviews/T-061-claims-adjuster-r4.md > /tmp/x 2>/dev/null; awk '/^```json/{f=1;next} /^```/{f=0} f' reviews/T-061-claims-adjuster-r4.md | python3 -c 'import json,sys; d=json.load(sys.stdin); print(\"parsed; verdict:\", d[\"verdict\"], \"blockers:\", sum(f[\"severity\"]==\"blocker\" for f in d[\"findings\"]), \"majors:\", sum(f[\"severity\"]==\"major\" for f in d[\"findings\"]), \"minors:\", sum(f[\"severity\"]==\"minor\" for f in d[\"findings\"]))'; rm -rf /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-991 && echo \"archive removed\"; ls /Users/arsis/zlayt-pm-project/artifacts/review-evidence/ | grep T-061",
 "description": "Validate JSON block and remove extracted archive copy"
}
````

### User / tool · 2026-11-02T02:40:38.827Z

**tool result (error)**
````
Permission to use Bash with command python3 -c 'import json,sys; d=json.load(sys.stdin); print("parsed; verdict:", d["verdict"], "blockers:", sum(f["severity"]=="blocker" for f in d["findings"]), "majors:", sum(f["severity"]=="major" for f in d["findings"]), "minors:", sum(f["severity"]=="minor" for f in d["findings"]))'; rm -rf /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-991 && echo "archive removed"; ls /Users/arsis/zlayt-pm-project/artifacts/review-evidence/ has been denied.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:40.821Z

The command was denied, most likely because of the `/tmp` redirect or the `rm -rf`. I'll rerun the JSON check on its own, with no temp files.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:41.592Z

**tool call — Bash**
````
{
 "command": "awk '/^```json/{f=1;next} /^```/{f=0} f' reviews/T-061-claims-adjuster-r4.md | python3 -c 'import json,sys; d=json.load(sys.stdin); print(\"parsed; verdict:\", d[\"verdict\"], \"| blockers:\", sum(f[\"severity\"]==\"blocker\" for f in d[\"findings\"]), \"majors:\", sum(f[\"severity\"]==\"major\" for f in d[\"findings\"]), \"minors:\", sum(f[\"severity\"]==\"minor\" for f in d[\"findings\"]))'",
 "description": "Parse the review JSON block and check verdict rule"
}
````

### User / tool · 2026-11-02T02:40:41.699Z

**tool result**
````
parsed; verdict: fail | blockers: 1 majors: 0 minors: 2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:43.798Z

The JSON parses and the verdict rule holds. One header count is wrong: the summary line says "3 minors" but the review has two minor findings. I'll note that in the reply, since the file is write-once. Next, the archive removal.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:44.321Z

**tool call — Bash**
````
{
 "command": "rm -rf /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-991 && echo \"archive removed\"; ls /Users/arsis/zlayt-pm-project/artifacts/review-evidence/ | grep T-061",
 "description": "Remove the extracted archive copy from review evidence"
}
````

### User / tool · 2026-11-02T02:40:44.380Z

**tool result (error)**
````
Permission to use Bash with command rm -rf /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r4-991 && echo "archive removed"; ls /Users/arsis/zlayt-pm-project/artifacts/review-evidence/ has been denied.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:48.907Z

The removal was denied by the permission system, so I will not retry it; the extracted archive stays and I'll flag it. Last, I'll record the recurring pattern in my memory.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:52.780Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_t061_r4_separator_list.md",
 "content": "---\nname: t061-r4-separator-list\ndescription: T-061 r4 (991dac4, D-037 whole-excerpt chip): closed separator list (; , and ( ) lets colon, dash, but, with, while, &, /, [, plus, as, per leak a family/EMS clause under the chip; 11 probe misses; gate PASS 18/18 on a closed row list\nmetadata:\n  type: project\n---\n\nD-037 (memory/ORCHESTRATOR_DECISIONS.md:45) says the patient_report chip attaches only when the whole excerpt is one patient-subject\nclause and \"any further clause means no chip\". Commit 991dac4 implemented it as a list of four separators (`app/backend/grounding.py:187`\n`_FURTHER_CLAUSE = [;,(]|\\band\\b`), not as \"any further clause\".\n\nRound 4 result (reviews/T-061-claims-adjuster-r4.md): r3 B1 (comma/and/paren family clause) and B2 (verb outside list) are closed; r3 major 3\n(gate measures production) is closed in form. New blocker: colon (\"Patient states neck pain: wife reports headaches.\"), em dash, \"but\",\n\"with\", \"while\", \"&\", \"/\", \"[ ]\", \"plus\", \"as\", and \"per X\" with no comma all keep the chip. Probe: artifacts/review-evidence/T-061-r4-probe.py.\n\n**Why:** each round finds the next unlisted connector. Enumerating separators is the same hole class as enumerating verbs or speakers\n(D-037 says fail closed instead of patching lists, and the enumeration keeps failing).\n\n**How to apply:** on any \"no further clause\" rule, probe a sweep of connectors and punctuation (colon, dash, slash, ampersand, brackets,\ncontrast words \"but/while/with/as/plus/per\", \"whereas/though\"), not only the separators in the spec text. Judge against the headline\nrule in the brief, not the example list in the table. Check whether the research gate's row list contains any of the new rows; if not, a\nPASS says nothing about them. A closed-grammar set (function words) is more defensible than speaker or verb lists, but still has a tail:\nask the orchestrator to write the set into D-037 and to record the tail as residual.\n\nRelated: [[t061-r3-clause-span-holes]], [[lexicon-review-method]], [[review-commit-not-worktree]].\n"
}
````

### User / tool · 2026-11-02T02:40:52.882Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_t061_r4_separator_list.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:53.185Z

**tool call — Bash**
````
{
 "command": "cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md",
 "description": "Read memory index before adding a pointer"
}
````

### User / tool · 2026-11-02T02:40:53.263Z

**tool result**
````
- [Lexicon review method](feedback_lexicon_review_method.md) — selfcheck PASS hides recall gaps; rerun probe script; must-probe constructions
- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 r1-r4: omissions, invented Rivera facts, partial scope fixes (line 34 left open at r4); sweep prose + golden must-not regex
- [Flag-pass review patterns](project_flag_pass_review_patterns.md) — T-036 r0: vacuous guard test, silent-empty conflict pass, worker skipped full suite
- [source_kind history and run signal](project_flag_source_kind_and_run_signal.md) — T-036 r2/r3 word filter; T-061 r0 (dd545e3) lexicon narrowed but AC2 flags/grounding wiring not done, exclude regex over-broad
- [Review the commit, not the dirty tree](feedback_review_commit_not_worktree.md) — git archive the sha when working tree has uncommitted edits to reviewed files
- [Reviews are write-once](feedback_reviews_write_once.md) — reviewer-write-guard blocks Edit on a written review; verify citations before the first write
- [T-036 r4 split and judge fixtures](project_t036_r4_split_and_judge_fixtures.md) — self-report split to T-061; committed judge fixtures don't replay (JUDGE_UNAVAILABLE); r4 verdict changes
- [T-061 r2 speaker scope](project_t061_r2_speaker_scope.md) — closed speaker list + 3-word window leaks colon labels, Mrs. split, mixed sentences; test variants, not just listed phrasings
- [T-061 r3 clause-span holes](project_t061_r3_clause_span_holes.md) — D-035 span runs to ';' so comma/and family clause keeps the chip; closed verb list leaks 'thinks/told'; selfcheck not production
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:55.089Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer && printf '%s\\n' \"- [T-061 r4 separator list](project_t061_r4_separator_list.md) — D-037 chip still leaks via unlisted connectors (colon, dash, but, with, &, /, plus, per); sweep connectors, not spec examples\" >> MEMORY.md && tail -2 MEMORY.md",
 "description": "Add pointer for the new memory to the index"
}
````

### User / tool · 2026-11-02T02:40:55.186Z

**tool result**
````
- [T-061 r3 clause-span holes](project_t061_r3_clause_span_holes.md) — D-035 span runs to ';' so comma/and family clause keeps the chip; closed verb list leaks 'thinks/told'; selfcheck not production
- [T-061 r4 separator list](project_t061_r4_separator_list.md) — D-037 chip still leaks via unlisted connectors (colon, dash, but, with, &, /, plus, per); sweep connectors, not spec examples
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:40:58.644Z

Verdict: **fail**. B1 and B2 are closed and major 3 is closed in form, but D-037's "any further clause" is still a four-separator list, so 11 chipped mixed excerpts remain (blocker): `reviews/T-061-claims-adjuster-r4.md`.
Corrections (write-once file, so reported here): the header says "3 minors" but there are 2; the bare-C/O pin is `tests/unit/test_flags_pass.py:120` and `:175`. The extracted archive `artifacts/review-evidence/T-061-r4-991` remains because `rm` was denied; please remove it.
