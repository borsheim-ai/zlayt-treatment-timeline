# Subagent: T-072 + T-074 review (haiku adjuster) (T-072 + T-074 review (haiku adjuster))

Source: `agent-a8188c11451c71993.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:49:17.254Z

Review two board cards in /Users/arsis/zlayt-pm-project. Both follow D-040 in memory/ORCHESTRATOR_DECISIONS.md, which says no user-facing label asserts who spoke.

1. **T-072** (commits 3b6a3fe and 4594bb7): confirm that
   - the patient_reported_onset flag title is now neutral ("Reported onset");
   - the export has no "(patient self-report)";
   - flag_templates' patient_report template is neutralized, and no user-facing text says "self-report" (grep app/ and app/frontend);
   - the export golden tests pass.
   The internal category id `patient_report` is kept on purpose, because it's never shown to users; check that it really isn't rendered.
2. **T-074** (commit 83b4353): spec/REQUIREMENTS.md lines 280 and 291 match evals/golden/sample.export.expected.txt lines 58 and 69. The orchestrator made this edit itself, so check it independently.

Run `.venv/bin/python -m pytest -q tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py`.

Write reviews/T-072-claims-adjuster.md and reviews/T-074-claims-adjuster.md. Each needs a ```json block of real values: card, persona claims-adjuster-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 2 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:49:18.936Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/claims-adjuster.md"
}
````

### User / tool · 2026-11-02T02:49:18.953Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:49:19.573Z

**tool call — Bash**
````
{
 "command": "ls .claude/agent-memory/claims-adjuster-reviewer/ && cat memory/ORCHESTRATOR_DECISIONS.md | head -c 20000 && echo ---- && python3 tools/board.py show T-072 && echo ---- && python3 tools/board.py show T-074",
 "description": "List memory dir, read decisions, show T-072 and T-074 cards"
}
````

### User / tool · 2026-11-02T02:49:19.790Z

**tool result**
````
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
project_t061_r4_separator_list.md
# ORCHESTRATOR DECISIONS (orchestrator is the sole writer)

Cross-cutting product decisions made while triaging reviews. The architect mirrors the technical ones into ADRs
(memory/DECISIONS.md); the writer mirrors the product ones into spec/REQUIREMENTS.md. Each: decision · why · source review.
Questions that are really Chris's are in submission/NEEDS_CHRIS.md with the assumption we act on.

| ID | Decision | Why | Source |
|---|---|---|---|
| D-001 | Export = two blocks: **Treatment section** (paste into letter: accepted entries + accepted charges) and **Internal review notes — do not send** (accepted flags, unclear amounts, records not included, bills to request, damages mentions, AI-assistance line). Flag notes/labels/counts never enter the letter. | Accepting a flag means "I've seen it", not "tell the carrier". | T-013 paralegal r1 (blocker) |
| D-002 | Every letter line carries a verbatim quote + provider as written + date of service (US long format) + citation placeholder `[Ex. __ / Bates __]`. No short-cite mode. | Ship bar #1 (100% grounded export); adjusters cross-check providers. | T-014 staff-eng F1, privacy B2 |
| D-003 | Gaps are computed by code over the code-parsed header dates of all clinical-encounter records (deduped), independent of LLM entries and review state. Billing statements and phone notes are excluded. Ambiguous dates are excluded and flagged. | Dropping an LLM entry must never change gap math. | T-014 staff-eng F2; T-015 paralegal |
| D-004 | Amounts: code extracts and classifies with explicit billing-phrase rules; judge #2 validates every classification; a rate can never become a charge; running total = accepted charges only; "detected" is shown separately and labelled not-a-total. Total line wording: "Billed charges stated in these records: $X". | Texas paid-or-incurred (§41.0105) — never "damages"; no PT total from a rate. | T-014 privacy B1; research T-008 |
| D-005 | Any record carrying an injection warning forces all its items to needs_review; its amounts can't be charges; it can't suppress flags from other records (lexicon is the floor). | Injected "$50,000" reached the total via code path alone. | T-014 privacy B1 |
| D-006 | Numbers/dates/$ in a summary or a user edit must appear in that item's excerpt (code check) or the item is needs_review with a reason. | Don't rely on the judge for swapped numerals. | T-014 staff-eng F5, privacy |
| D-007 | Flag titles/explanations are code templates; the LLM returns only category + excerpt spans. | No free LLM prose in the attorney's notes. | T-014 staff-eng F8, privacy |
| D-008 | Public deployment is demo-only by default (cached sample run through real pipeline code); live mode needs an explicit env opt-in. No case list; random 128-bit case tokens; spend counter append-only and separate from case data. | Exposure + key abuse risk. NEEDS_CHRIS #7. | T-014 privacy |
| D-009 | AI disclosure: UI banner + a line in internal notes; none in the letter text. (Listed under "Decided by the team" in NEEDS_CHRIS.) | Candor without telling the carrier how the chronology was made. | T-014 privacy |
| D-010 | Edits: entry = summary text only; charge = accept/dismiss only (no reclassification, no amount edit); flag = reviewer note only. Ambiguous dates are resolved with a separate `confirm_date` action (choose one of the code-proposed readings), not an edit. Originals are kept; "edited" shows in UI + internal notes. | Keep code-owned facts code-owned. | T-013 PM r2 (major 1, 2) |
| D-011 | **Cut** (non-goals): batch accept; charge reclassification; "not a duplicate" split action (merge stays, visible); LLM date pointing; BYOK; `?full=1`; flag title/explanation edits; case list; LLM split fallback. | Time box; each needed a new endpoint/ADR and none is an Appendix A must-have. | T-013 PM r2, T-014 staff-eng F12 |
| D-012 | Excerpt rule: an entry's excerpt is one or more **whole sentences** of the record (code sentence splitter: `.`, `;`, line breaks), chosen by the model and changeable by the paralegal only to other whole sentences of the same record. A sentence that contains any lexicon hit (pre_existing / causation / compliance) or hedge is kept whole — a hedge can never be cut. Flagged language may appear in the letter **only** as part of an accepted excerpt, and the internal notes list "flagged language quoted in the letter" so the attorney decides. NEEDS_CHRIS #10. | The records' own words are the record; hiding them is the attorney's call, not the tool's. | T-013 paralegal r2 M1/M2, PM r2 M3/M4 |
| D-013 | Flag-type vocabulary everywhere: `gap`, `conflict`, `pre_existing`, `causation`, plus `record_warning` (date ambiguity, injection). Lexicon `causation_weakening` and `compliance` map to `causation`. | Three vocabularies existed. | T-013 PM r2 M5 |
| D-014 | Provider = the source label exactly as written in the record header; golden aliases must match header text. | Grounding (R-TL-9). | T-013 PM r2 |
| D-015 | Paralegal ship-bar score key: `scores.verify_quickly` (1–5) in the paralegal review JSON; ≥ 4 to ship. | One name across REQUIREMENTS, briefs, reviews. | T-013 PM r2 |
| D-016 | Post-launch, a test set **may** be built from real work product, but only inside the firm's environment, attorney-approved, with access logged; the prototype and this repo stay synthetic-only. Personas must not treat that as a dealbreaker. | Part 2 area 4 asks for it; Texas Op. 705 allows confidential info in AI tools with precautions. | T-010 litigation-lead Q |
| D-017 | The tool never picks between conflicting accident dates and never computes "delay from the accident". It may state "first recorded treatment: <earliest record date>". Adverse facts are never auto-included in the letter; they live in internal notes (D-001), and the attorney decides. | Must-not: merge the two accident dates; adverse facts are the attorney's call. | T-010 litigation-lead M1/M2 |
| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and handles field-style answers ("Prior injuries: No."). Scene facts from EMS reports (ambulatory at scene, refused transport, minimal damage), "no objective findings", WNL/full ROM, and attorney referral are **causation** flags citing the excerpt (internal notes only, D-001). Delay to first treatment is not computed (D-017). The lexicon self-check must run over every golden case and report recall per must-flag. | Recall and precision both failed probes; vocab mismatch. | T-009 legal-nurse + claims-adjuster |
| D-019 | The letter's total line is exactly `Billed charges stated in these records: $X` (X = accepted charges). **No parenthetical, no "excludes …" clause**, ever. Unclear, excluded, rate and injection-tagged amounts appear only in internal notes. | Any clause built from unaccepted or injected amounts leaks into the carrier letter. | T-014 privacy r2 N1 (blocker) |
| D-020 | Public build is demo-only (D-008): `POST /api/cases` in demo mode accepts only text whose normalized hash (CRLF→LF, trimmed) equals a recorded fixture; anything else is rejected and **not stored**. Live mode is local-only with a key; no in-app spend ledger or per-IP limiter — use the provider-side spend limit (documented in README). | Don't store arbitrary pasted text on a public Space; cut code the demo never runs. | T-014 privacy r2 N2, staff r2 R2-5/6/7 |
| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
| D-023 | **Harness threat model:** the hooks defend against *accidents and lazy evasion by well-meaning agents* (wrong spelling, a pasted destructive command, staging a secret), not against a deliberately hostile agent with shell access — a shell-text guard cannot be complete against that. Consequences: (1) every finding that a *plausible accidental spelling* passes is a bug and gets fixed + a regression test; (2) deliberate obfuscation (brace expansion, IFS, copies of board.py, interpreter one-liners) is residual risk, documented, and covered by detection instead: git history is append-only (no rewrite), every board transition is in the append-only activity log, and the orchestrator re-verifies evidence before closing; (3) `--no-verify` is never legitimate for agents (denied); (4) reviewers may run mutating git only inside scratch repos under /tmp or the scratchpad. | Security r2 asked for the threat model; without one the guard review is an endless arms race. | T-003/T-006 security r2 |
| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at milestone gates (Tier 2) and the final hiring panel. One agent may cover two persona checklists in one pass. (3) Docs/research cards: max 2 rounds; remaining majors without blockers become documented debt (§7.4) instead of round 3. (4) Briefs ≤ 12 lines, reviewer replies ≤ 10 lines. (5) Researcher moves to sonnet. (6) Heartbeat hourly, not every 20 min. (7) No more harness rounds after M0 r3: residual findings become debt under D-023. | Spend the budget on the product and the submission, not on review churn. | Chris inbox 2026-11-02T00:58Z |
| D-025 | Provider-name conflicts across records (e.g. golden case_05) are raised by **code** (normalized-name rule over header labels), matching LLM_VS_CODE row 10; the LLM conflict pass covers semantic conflicts only (row 11). | Deterministic task → code; removes an Either/or from the plan. | T-018 contract review (staff major 7) |
| D-026 | Lexicon recall on golden must-flags is **reported, not gated** (latest.json `lexicon_recall_must_flags`); the ship bar is unchanged. LLM_VS_CODE rows 12/16 say so. | The lexicon is a second signal; the gate is flag precision/recall of the whole system. | T-018 contract review (PM major 6) |
| D-027 | Two-digit years are never guessed: `03-17-98` is `date_ambiguous` with candidates (1998, 2098) and excluded from gap math until confirmed. Text outside recognised record blocks is never dropped: it becomes an 'unsplit text' record flagged for the paralegal. | 'Say so instead of guessing' (spec); silent drops lose facts. | T-032 staff review |
| D-028 | Judges return a verdict enum plus a `reason_code` from a closed list (e.g. ADDS_DIAGNOSIS, ADDS_SEVERITY, ADDS_CAUSATION, DROPS_QUALIFIER, NUMBER_MISMATCH, OTHER_UNSUPPORTED); no free-text reason. The UI's Why? renders the code through a code template. | Model prose must not reach the attorney or the UI (consistent with D-007); ADR-008.5 enum-only. | T-035 staff review (Chris Q answered by orchestrator) |
| D-029 | Two fixture sets: `tests/fixtures/llm/recorded/` (live claude-cli recordings, used by evals to replay real model behaviour) and `tests/fixtures/llm/curated/` (hand-checked generator/judge responses that reproduce the golden summaries/excerpts exactly; labelled CURATED). E2E byte-equality (R-EX-6) and the public demo replay the curated set and the UI labels it 'cached demo (curated responses)'; the ship bar (§8.2) is measured on live runs and recorded fixtures only. | A live model may legitimately choose different whole-sentence excerpts (entry 2 adding the ER-charges sentence); byte-equality needs fixed responses; honesty needs the label. | T-040 handoff |
| D-030 | Flag evidence is the **verbatim phrase span** that triggered the flag (lexicon match or LLM-returned span), e.g. "Findings may represent degenerative change", "New onset pain" — not the whole sentence. Entry excerpts stay whole sentences (D-021). Internal notes quote flag spans; the golden notes block is the authority. | Precise flag quotes; matches the hand-written golden; entries keep context. | T-051/backend-4 |
| D-031 | **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_SPLIT); 'not a duplicate' split; full audit view (local mode); exhibit/Bates numbering as a per-case config; draft treatment paragraph in firm voice (stretch from spec; every sentence grounded + judged, internal until accepted). **Still cut, with reason:** charge reclassification (a rate must never become a charge — safety), auth/roles (needs an identity provider), per-user learning (needs its own evals), numeric confidence (unverifiable precision), non-English/handwriting, date-convention inference (silent-guess risk), OCR. | Chris asked; each reinstated item keeps the ladder and grounding rules. | Chris inbox 02:05Z |
| D-032 | Narrows D-018: normal/negative findings (`objective_negative`: 'negative for fracture', 'WNL', 'full ROM') are **context only, never flags**; `scene_facts` raise a causation flag only on specific adjuster phrases ('minimal damage', 'refused transport', 'ambulatory at scene', 'no airbag deployment'), never on a plain mechanism description ('Cyclist struck by a car'). | First eval: causation precision 0.5 from these two categories; golden case_05 must_not N2. | T-038 eval report 20261102T020824Z |
| D-033 | `patient_report` (self-report chip) applies only to explicit patient attribution ('Patient states/reports/notes', 'Pt c/o', patient-quoted speech). EMS narrative, witness, spouse/family statements and generic 'S:'/'Subjective:' headers are not patient self-report (separate or no attribution). Narrows ADR-013 / DECISIONS.md:286. | Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit. | T-036 r3 → T-061 |
| D-034 | Hardens D-006/R-RV-3: a number, date or $ figure in a summary, edit or manual entry that is not in that item's excerpt (or its source label/parsed date) is a **hard 422** — no 'keep my wording' override. The 409 confirm path remains only for non-numeric judge objections, and any override is listed in internal notes ('reviewer override: <reason code>'). | An override let 'Pain 9/10' into the letter against a 4/10 quote — an invented fact. | T-056 paralegal review |
| D-035 | Simplifies D-033: `patient_report` is attached only to a **clause** that begins with an explicit patient subject ('Patient', 'Pt', 'The patient') followed by a reporting verb (states, reports, notes, says, endorses, complains of, c/o, denies); the tag spans that clause only (to the next ';' or sentence end). Everything else — EMS, family, any other or unknown speaker, header labels — gets **no tag**. Default is no tag: a missing chip is safe, a wrong chip is not. | Speaker-list regexes kept missing new speakers (girlfriend, co-worker). | T-061 r2 |
| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
| D-037 | Final rule for `patient_report` (supersedes the clause-splitting in D-035, 2026-11-02): the chip attaches only when the **whole excerpt** is a single patient-subject clause (`Patient`/`Pt`/`The patient` + reporting verb), with no further clause after `;`, `,`, `and`, or `(`. Any mixed excerpt gets no chip and stays a plain record excerpt, so no verb list decides it. Bare `C/O` gets no chip. A missing chip is safe; a wrong chip mislabels the source. | Three adjuster rounds kept finding clause-boundary holes; fail closed instead of patching verbs. | T-061 claims-adjuster r3 B1/B2 |
| D-038 | Narrows D-032 (2026-11-02): normal or negative objective findings stay context-only, but defense **credibility phrases** from the lexicon (e.g. 'Waddell signs', 'out of proportion', 'symptom magnification', 'non-physiologic', 'inconsistent effort') raise a flag so the paralegal sees them before the adjuster does. | These are what an adjuster quotes against the claimant; hiding them defeats the prep purpose. | T-063 staff r1 major 6 |
| D-039 | Re-run with decided items (2026-11-02): once any entry in a case is accepted, edited or dismissed, the case's records are frozen. A re-run reuses the stored records and never re-splits, so decided items keep their record ids and excerpts. Re-splitting is allowed only while every entry is still pending. | Provenance of an accepted item is what the paralegal verified against; it must never silently move. | T-057 staff r3 blocker |
| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four adjuster rounds each found mixed excerpts that a closed rule still mislabeled. The verbatim excerpt already shows who spoke ('Patient states…', 'wife reports…'), so the label added risk without information. A missing chip is safe; a wrong one is a credibility error. | T-061 claims-adjuster r4 blocker; §7.4 |
----
---
id: "T-072"
title: "Neutral title for patient_reported_onset flag; drop '(patient self-report)' from export (D-040 follow-through)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:45:10Z"
updated_at: "2026-11-02T02:48:50Z"
claimed_by: "backend"
claimed_at: "2026-11-02T02:45:23Z"
rounds: 0
commits: ["3b6a3fe", "4594bb7"]
reviews: []
ac:
  - {"n": 1, "text": "Flag title no longer asserts the speaker (e.g. 'Reported onset'); export no longer appends '(patient self-report)'; flag templates, export tests and golden expectations updated (qa note for golden lines); hallucination catch 40/40", "done": true, "evidence": "commit 3b6a3fe; tests/unit/test_export_edge.py::test_patient_report_flag_title_is_neutral passes; unit 940 pass, 2 fail only on byte-exact export golden (qa note posted) + 1 unrelated frontend; evals.run hallucination_catch 40/40 (evals/reports/20261102T024653Z.md)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:45:23Z backend: claimed
- 2026-11-02T02:47:12Z backend: QA ACTION (golden is yours, not edited): evals/golden/sample.export.expected.txt remove the suffix ' (patient self-report)' on line 58 (INTERNAL REVIEW causation entry for record 9: ...January collision." (patient self-report); record 7 -> ...January collision."; record 7) and on line 69 ('Causation language (patient self-report).' -> 'Causation language.'). Until then tests/unit/test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte, test_case_extras.py::test_default_export_is_byte_identical_to_golden... and make_curated --check ('notes equal: False', letter equal True) fail. check_golden.py:543 .replace(' (patient self-report)','') is now a harmless no-op, can be dropped. Unrelated pre-existing failure: tests/unit/test_e2e_contract.py::test_every_test_id_is_declared ('btn-undo-batch', frontend). evals.run: hallucination_catch 40/40; blocker 4_no_invented_facts + fixture-determinism were already present in the prior report. Coordinator ask re patient_report template: neutralized (key kept as internal category id; title 'Reported onset', explanation 'Onset wording reported in ...'). Renaming the category id would change prompts/flags_v1.md (hash -> fixture re-record), lexicon.yaml (researcher), curated fixtures, frontend mocks; and flags_v1.md:13 still defines it as 'the patient's own statement' - propose follow-up card if wanted.
- 2026-11-02T02:47:12Z backend: AC 1 checked: commit 3b6a3fe; tests/unit/test_export_edge.py::test_patient_report_flag_title_is_neutral passes; unit 940 pass, 2 fail only on byte-exact export golden (qa note posted) + 1 unrelated frontend; evals.run hallucination_catch 40/40 (evals/reports/20261102T024653Z.md)
- 2026-11-02T02:47:13Z backend: moved in_progress -> in_review
- 2026-11-02T02:47:25Z orchestrator: assigned: qa
- 2026-11-02T02:47:25Z orchestrator: Review held until qa updates export golden lines 58/69. Internal category id patient_report in prompts/flags_v1.md and lexicon is kept: renaming forces a fixture re-record, and the id is never shown to users (D-040 covers user-facing labels).
- 2026-11-02T02:47:34Z orchestrator: review dispatched: claims-adjuster-reviewer
- 2026-11-02T02:48:50Z qa: Golden done in 4594bb7 (lines 58, 69; btn-undo-batch declared in tests/e2e/conftest.py). make_curated --check: letter+notes equal True. unit: 938 pass, 6 fail; export golden tests pass. evals.run hallucination_catch 40/40 (evals/reports/20261102T024822Z.md), ship_bar false only on live-only/spec blockers. REMAINING: spec/REQUIREMENTS.md lines 280 and 291 still carry '(patient self-report)' so check_spec spec_matches_golden=false (fails test_eval_spec_check x2, test_eval_runner x3): not qa-owned, filed T-074 (architect). Separate: test_narrative::test_recorded_sample_paragraph_replays... fails LLM_FAILED_AFTER_RETRIES (fixture miss, not golden-related; fixture.py has uncommitted edits by another worker).

## Handoff
Changed: patient_report template title -> 'Reported onset' (explanation 'Onset wording reported in ...'); removed both '(patient self-report)' suffixes and _SELF_REPORT_SUBTYPES from export.py; updated export/e2e tests, added neutral-title test. Verified: pytest tests/unit (940 pass; export golden byte-exact tests fail until qa edits sample.export.expected.txt lines 58 and 69, listed in note); evals.run hallucination 40/40. Left: qa golden edit; optional follow-up to rename category id/prompt line (needs fixture re-record). Surprised: category id patient_report is wired through prompt, lexicon, fixtures, so only user-facing text was neutralized.

----
---
id: "T-074"
title: "Update spec/REQUIREMENTS.md section 6 blocks (lines 280, 291) to match D-040 export golden: drop '(patient self-report)'"
milestone: "M3"
role: "architect"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:48:44Z"
updated_at: "2026-11-02T02:49:12Z"
claimed_by: "architect"
claimed_at: "2026-11-02T02:49:08Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "REQUIREMENTS.md line 280 drops ' (patient self-report)' after the record 9 causation quote; line 291 reads 'Causation language.'; evals.run --check-spec returns spec_matches_golden true; tests/unit/test_eval_spec_check.py and test_eval_runner.py pass", "done": true, "evidence": "spec/REQUIREMENTS.md:280,291 now equal golden lines 58/69 (commit 83b4353); test_eval_spec_check + test_eval_runner 41 passed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T02:49:08Z architect: claimed
- 2026-11-02T02:49:08Z architect: AC 1 checked: spec/REQUIREMENTS.md:280,291 now equal golden lines 58/69 (commit 83b4353); test_eval_spec_check + test_eval_runner 41 passed
- 2026-11-02T02:49:09Z architect: moved in_progress -> in_review
- 2026-11-02T02:49:09Z orchestrator: review dispatched: claims-adjuster-reviewer
- 2026-11-02T02:49:12Z orchestrator: Transparency: the orchestrator made this 2-line spec sync itself (spec is orchestrator-synced) and recorded the AC/handoff under the card role; an independent reviewer verifies it with T-072.

## Handoff
Orchestrator synced spec §6 export lines 280/291 to golden 58/69 (spec is orchestrator-synced since M1). Tests green.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:49:23.703Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md && echo ---- && cat .claude/agent-memory/claims-adjuster-reviewer/feedback_review_commit_not_worktree.md .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md && echo ---- && git rev-parse --is-inside-work-tree 2>&1; git status --short 2>&1 | head -40; git log --oneline -5 2>&1",
 "description": "Read reviewer memory index and feedback notes, check git state"
}
````

### User / tool · 2026-11-02T02:49:23.860Z

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
- [T-061 r4 separator list](project_t061_r4_separator_list.md) — D-037 chip still leaks via unlisted connectors (colon, dash, but, with, &, /, plus, per); sweep connectors, not spec examples
----
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
----
true
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M app/llm/backends/fixture.py
 M board/activity.jsonl
 M board/cards/T-045.md
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
 M evals/run.py
 M memory/LESSONS.md
 M tests/fixtures/llm/056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d.json
 M tests/fixtures/llm/067240d96709b57638faad6e55ccb4a12af21dd382baec8516eeff30ae621cdd.json
 M tests/fixtures/llm/06bbeeec2801064baeb024b1338ce8a0263644a7a2dca09efdaeed154ed50299.json
 M tests/fixtures/llm/07aab6f4f7a87ed2477b3cb9ebdb02449815ddf270c7f8aafdfa3c2338c9be19.json
 M tests/fixtures/llm/096042ca0286b135b1ff8db5f6d20a32cbf7c3989c5e10fc7ef5bf33da0670c2.json
 M tests/fixtures/llm/0cee28a9faf640b117982bccb05b874c1bc8b7359cd3ff5dc846f1ac8db9c8c9.json
 M tests/fixtures/llm/0e7db52d0c5b7b4b77cced05c5e9bae39d5038d4866d2baa759dd0396aa9707e.json
 M tests/fixtures/llm/0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
 M tests/fixtures/llm/11245ae85d4b50423fb2ce331e7adbe7b3436e8dccf11252c833ecfa6e11db67.json
 M tests/fixtures/llm/128383b890348cd75ed0f2eb15f8516ffb0e90785d18225192c7a1b405bcf58d.json
 M tests/fixtures/llm/12c7d9209cd3664ab6d186c3019b41db44960c32d1e3116c3cab75b6940d40d1.json
 M tests/fixtures/llm/152ed320bc8b26db404098b64d8e04e44f8c0a292aad0ca4bf5cab5627bd0380.json
 M tests/fixtures/llm/15676bbd3a5dfcc0ea008d7ce5df7d39df233a249a11548075e4595d1556399c.json
 M tests/fixtures/llm/15bbdc084a71365c8cbeb7dcce6bb8aa8661e71cdff83f73c613fea855ed21a2.json
 M tests/fixtures/llm/15c4f6ccae6fb8f35eed3f6750b0091a1941dcd442d3c97e10e73a628b5a4c5a.json
 M tests/fixtures/llm/15c7ae87456fa60ab428c113c44b7f324ea39b9d76ce7907c811a7f2768177a3.json
 M tests/fixtures/llm/1620d4b2ce4e8303351c7e5dbefd076a3b74842fcf745e687c80c9950e7a7ffc.json
 M tests/fixtures/llm/17192447ebba593e241115cf34fe99c33e6051f6236dbd62ec8308365d2c243a.json
 M tests/fixtures/llm/17ba1e45346d1f4b42edcc19e3012b72cdf6c0e95181231310148679957b4320.json
83b4353 spec: sync §6 export lines to golden after D-040 (T-074)
4594bb7 fix(qa): export golden drops patient self-report suffix (D-040); declare btn-undo-batch test id
3b6a3fe feat(backend): neutral 'Reported onset' flag title; drop '(patient self-report)' from export (D-040, T-072)
4808b77 docs(architect): T-063 r3: D-038 credibility flags decided, D-040 cuts self-report chip, split reasons, batch and judge wording
1c0bae2 test(backend): pin each D-039 freeze trigger (entry accept/edit/dismiss, amount, flag) (T-057 r4 minor, T-066)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:49:27.206Z

**tool call — Bash**
````
{
 "command": "echo \"== commits\" && git show --stat --format='%h %s' 3b6a3fe 4594bb7 83b4353 | grep -v '^$' && echo \"== diff of reviewed files: working tree vs HEAD\" && git diff --stat HEAD -- app/backend app/frontend app/llm/prompts spec/REQUIREMENTS.md evals/golden app/llm/lexicon.yaml tests/unit/test_export.py tests/unit/test_export_edge.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py 2>&1; echo \"== grep users-facing patient self-report in app/ (live tree)\"; grep -rn -i \"self-report\\|self report\\|selfreport\\|self_report\" app/ --include=*.py --include=*.ts --include=*.tsx --include=*.js --include=*.jsx --include=*.html --include=*.md --include=*.yaml --include=*.json --include=*.txt --include=*.vue 2>/dev/null | head -80",
 "description": "Show commit stats, live-vs-HEAD diffs, and grep app/ for self-report"
}
````

### User / tool · 2026-11-02T02:49:27.349Z

**tool result**
````
== commits
3b6a3fe feat(backend): neutral 'Reported onset' flag title; drop '(patient self-report)' from export (D-040, T-072)
 app/backend/export.py          | 5 -----
 app/backend/flag_templates.py  | 2 +-
 tests/e2e/test_flags_panel.py  | 4 ++--
 tests/unit/test_export_edge.py | 9 ++++++++-
 4 files changed, 11 insertions(+), 9 deletions(-)
4594bb7 fix(qa): export golden drops patient self-report suffix (D-040); declare btn-undo-batch test id
 evals/golden/sample.export.expected.txt | 4 ++--
 tests/e2e/conftest.py                   | 2 +-
 2 files changed, 3 insertions(+), 3 deletions(-)
83b4353 spec: sync §6 export lines to golden after D-040 (T-074)
 spec/REQUIREMENTS.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
== diff of reviewed files: working tree vs HEAD
 tests/unit/test_eval_runner.py | 9 +++++++++
 1 file changed, 9 insertions(+)
== grep users-facing patient self-report in app/ (live tree)
app/README-arch.md:78:`app/llm/lexicon.yaml` v2 (researcher): `flag_type`, `hedge`, `self_report`, `strength`, plus the `accident_date_phrases`, `non_encounter` and `injection` categories. It blocks the gap rule, the accident-date rule and the injection scan, and its golden self-check (recall per `must` flag) gates the claim that the lexicon is a floor (ADR-008.4).
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
app/llm/lexicon.yaml:743:  self_report: true
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:49:29.799Z

**tool call — Bash**
````
{
 "command": "echo \"== A: 'self-report'/'self report' prose anywhere in app/ (excluding lexicon.yaml booleans)\" && grep -rn -i \"self-report\\|self report\\|self-reported\" app/ --exclude-dir=node_modules --exclude-dir=dist | grep -v \"app/llm/lexicon.yaml\" ; echo \"== B: patient_report occurrences in app/ (all)\" && grep -rn \"patient_report\\|patient_reported\\|source_kind\" app/ --exclude-dir=node_modules --exclude-dir=dist ; echo \"== C: frontend tree\" && ls app/frontend && grep -rln -i \"self.report\\|patient_report\\|source_kind\\|Reported onset\\|patient_reported_onset\" app/frontend --exclude-dir=node_modules --exclude-dir=dist 2>/dev/null",
 "description": "Grep app/ for self-report prose and patient_report identifiers"
}
````

### User / tool · 2026-11-02T02:49:29.939Z

**tool result**
````
== A: 'self-report'/'self report' prose anywhere in app/ (excluding lexicon.yaml booleans)
app/frontend/mock_flags.js:24:      mk("f_pat_9", "causation", "patient_report", "Patient self-report", "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
app/frontend/dev/mock-data.js:748:   "title": "Patient self-report",
app/frontend/dev/mock-data.js:749:   "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): \u201cPatient states symptoms began after the January collision.\u201d",
app/backend/narrative.py:4:no dropped hedge / self-report / negation (D-022), no causation or adverse wording that the quote itself does not contain, no flag
app/backend/narrative.py:19:    "SUMMARY_DROPS_QUALIFIER": "The sentence drops a hedge, self-report marker or negation that the cited quote has.",
app/backend/grounding.py:58:# ---------------------------------------------------------------- lexicon (hedge / self-report sets)
== B: patient_report occurrences in app/ (all)
app/README-arch.md:36:  lexicon.yaml     [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection
app/llm/lexicon.yaml:20:#   pre_existing, degenerative_language, speculative_language, patient_report, missed_care, new_onset).
app/llm/lexicon.yaml:26:#   source_kind = "patient_report" from it (ADR-013). Self-report entries are never hedges.
app/llm/lexicon.yaml:84:# T-061: a self_report hit is a PATIENT statement only. Before the code sets source_kind = patient_report, it must drop the hit
app/llm/lexicon.yaml:90:  note: 'T-061 r1: anchored to the sentence SUBJECT (a sentence that starts with a non-patient speaker, or with "Per <non-patient>"); a patient subject that merely mentions EMS or a wife stays patient. Sentence-level test: the sentence containing the match is tested; a hit means the statement is not the patient''s, so source_kind stays "record" and no "Patient self-report" label is shown.'
app/llm/lexicon.yaml:741:  category: patient_report
app/llm/lexicon.yaml:754:- id: patient_reports_generic
app/llm/lexicon.yaml:757:  category: patient_report
app/llm/lexicon.yaml:780:  false_positive: 'Round 2 split this from the generic "per patient" marker, which is now low (self_report). T-061: self_report is false here because an intake form is a document, not the patient''s statement; source_kind stays "record". "Date of injury per patient" is still caught by patient_reports_generic. "Per protocol" does not match.'
app/frontend/dev/mock-data.js:158:   "source_kind": "record",
app/frontend/dev/mock-data.js:190:   "source_kind": "record",
app/frontend/dev/mock-data.js:222:   "source_kind": "record",
app/frontend/dev/mock-data.js:254:   "source_kind": "record",
app/frontend/dev/mock-data.js:286:   "source_kind": "record",
app/frontend/dev/mock-data.js:318:   "source_kind": "record",
app/frontend/dev/mock-data.js:350:   "source_kind": "record",
app/frontend/dev/mock-data.js:382:   "source_kind": "record",
app/frontend/dev/mock-data.js:414:   "source_kind": "record",
app/frontend/dev/mock-data.js:532:   "source_kind": "record",
app/frontend/dev/mock-data.js:589:   "source_kind": "record",
app/frontend/dev/mock-data.js:635:   "source_kind": "record",
app/frontend/dev/mock-data.js:677:   "source_kind": "record",
app/frontend/dev/mock-data.js:713:   "source_kind": "record",
app/frontend/dev/mock-data.js:746:   "category": "patient_report",
app/frontend/dev/mock-data.js:747:   "source_kind": "record",
app/backend/present.py:45:            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
app/backend/present.py:74:    return {**_common(row), "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
app/llm/prompts/flags_v1.md:13:- "patient_report": the patient's own statement about onset or cause ("patient states symptoms began after ...").
app/backend/review.py:200:                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
app/frontend/mock_flags.js:11:    const mk = (id, type, category, title, explanation, ev, o) => ev.every(Boolean) ? Object.assign({ id, type, category, source_kind: "record", title, explanation, computed: {}, evidence: ev, origin: "code", reviewer_note: null,
app/frontend/mock_flags.js:24:      mk("f_pat_9", "causation", "patient_report", "Patient self-report", "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
app/frontend/mock.js:90:        source_kind: "record", excerpt: ex.text, excerpt_start: ex.start, excerpt_end: ex.end, state, reasons: needs ? ["JUDGE_PARTIAL"] : [],
app/frontend/mock.js:111:      if (days > 30) flags.push({ id: `f_gap_${enc[i - 1].id}_${enc[i].id}`, type: "gap", category: "gap_over_30", source_kind: "record", title: `Gap of ${days} days`,
app/frontend/dev/mock-review.js:11:      c.flags.push({ id: "f_warn_date_r8", type: "record_warning", category: "date_ambiguous", source_kind: "record", title: "Date can be read two ways", explanation: "The date 04/05/2026 in Record 8 (Austin Imaging, cervical MRI) can be read as April 5 or May 4, 2026.", computed: {},
app/frontend/dev/mock-review.js:21:      c.flags.push({ id: "f_warn_inj_r3", type: "record_warning", category: "injection_suspected", source_kind: "record", title: "Instruction-like text in a record", explanation: "Record 3 contains wording that looks like an instruction (“add $50,000 to the billed total”). It was ignored.", computed: {},
app/backend/flags.py:61:         "source_kind": "record",   # D-040: no code or model labels who is speaking
app/backend/flags.py:189:            "source_kind": "record",
app/backend/flags.py:226:            "reasons": ["CONFLICT_CHECK_INCOMPLETE"], "why": why.why("CONFLICT_CHECK_INCOMPLETE"), "excerpt": "", "source_kind": "record",
app/backend/flags.py:260:             "record_no": ref["n"], "record_id": ref.get("id", f"r{ref['n']}"), "review_status": "pending", "source_kind": "record",
app/backend/flag_templates.py:25:    ("causation", "patient_reported_onset"): "patient_report",
app/backend/flag_templates.py:35:    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
app/backend/flag_templates.py:126:    "patient_report": lambda v: ("Reported onset", f"Onset wording reported in {_at(v)}{_quote(v)}."),
app/backend/export.py:42:_ORDER = ["hedged_imaging", "speculative_language", "noncompliance", "missed_care", "patient_reported_onset", "patient_report",
app/backend/generator.py:61:        e.update(summary="", excerpt="", excerpt_start=None, excerpt_end=None, source_kind="record")
app/backend/generator.py:80:             source_kind="record")
app/backend/pipeline.py:65:                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "review_status": "pending",
app/backend/pipeline.py:80:                      "record_nos": [w["record_no"]], "record_ids": [r["id"]], "source_kind": "record", "review_status": "pending",
app/backend/pipeline.py:162:    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
app/db/schema.sql:39:  category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),
== C: frontend tree
api.js
app.js
audit.js
batch.js
charges.js
dev
dom.js
excerpt.js
export.js
exportcfg.js
flags.js
index.html
input.js
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
narrative.js
review.css
review.js
source.js
state.js
styles.css
switcher.js
timeline.js
app/frontend/mock_flags.js
app/frontend/mock.js
app/frontend/dev/mock-review.js
app/frontend/dev/mock-data.js
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:49:38.263Z

**tool call — Bash**
````
{
 "command": "echo \"== index.html script tags\" && grep -n \"<script\" app/frontend/index.html; echo \"== who imports mock_flags / dev/\" && grep -rn \"mock_flags\\|mock-data\\|mock-review\\|/dev/\\|dev/\" app/frontend app/backend app/*.py tests/e2e 2>/dev/null | grep -v node_modules | head -30; echo \"== flag_templates.py patient_report region\" && sed -n 20,40p app/backend/flag_templates.py && sed -n 118,135p app/backend/flag_templates.py; echo \"== export.py _SELF / category rendering\" && grep -n \"self\\|SELF\\|category\" app/backend/export.py | head -40",
 "description": "Check frontend script loading, mock imports, template and export code"
}
````

### User / tool · 2026-11-02T02:49:38.381Z

**tool result**
````
== index.html script tags
42:<script src="dom.js"></script>
43:<script src="mock_sample.js"></script>
44:<script src="mock.js"></script>
45:<script src="mock_flags.js"></script>
46:<script src="mock_extra.js"></script>
47:<script src="api.js"></script>
48:<script src="state.js"></script>
49:<script src="input.js"></script>
50:<script src="source.js"></script>
51:<script src="timeline.js"></script>
53:<script src="review.js"></script>
54:<script src="flags.js"></script>
55:<script src="charges.js"></script>
56:<script src="batch.js"></script>
57:<script src="audit.js"></script>
58:<script src="manual.js"></script>
59:<script src="narrative.js"></script>
60:<script src="exportcfg.js"></script>
61:<script src="excerpt.js"></script>
62:<script src="export.js"></script>
63:<script src="switcher.js"></script>
64:<script src="app.js"></script>
== who imports mock_flags / dev/
app/frontend/index.html:45:<script src="mock_flags.js"></script>
app/frontend/dev/panels.html:12:<script src="mock-data.js"></script><script src="mock-review.js"></script>
== flag_templates.py patient_report region
    ("pre_existing", "prior_other_region"): "pre_existing",
    ("pre_existing", "baseline_symptom"): "pre_existing",
    ("pre_existing", "prior_surgery_same_region"): "prior_surgery",
    ("causation", "hedged_imaging"): "speculative_language",
    ("causation", "noncompliance"): "missed_care",
    ("causation", "patient_reported_onset"): "patient_report",
    ("causation", "temporal_after_gap"): "new_onset",
    ("causation", "accident_date_inconsistency"): "accident_date_provenance",
}

TYPE_OF = {
    "gap_over_30": "gap",
    "accident_date_after_treatment": "conflict", "accident_dates_differ": "conflict", "provider_name_variant": "conflict",
    "treatment_plan_vs_actual": "conflict", "other_fact_mismatch": "conflict",
    "pre_existing": "pre_existing", "degenerative_language": "pre_existing", "prior_surgery": "pre_existing",
    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
    "scene_facts": "causation", "alternative_cause": "causation", "litigation_referral": "causation",
    "objective_negative": "causation", "accident_date_provenance": "causation", "credibility_language": "causation",
    "date_ambiguous": "record_warning", "injection_suspected": "record_warning", "analysis_incomplete": "record_warning", "llm_split": "record_warning",
}

    "accident_dates_differ": _acc_differ,
    "provider_name_variant": _provider_variant,
    "treatment_plan_vs_actual": _pair("Treatment plan and what followed differ"),
    "other_fact_mismatch": _pair("Records differ on a fact"),
    "pre_existing": lambda v: ("Mention of a prior or pre-existing condition", f"{_at(v)} mentions a prior or pre-existing condition{_quote(v)}."),
    "degenerative_language": lambda v: ("Degenerative wording", f"{_at(v)} uses degenerative wording{_quote(v)}."),
    "prior_surgery": lambda v: ("Mention of prior surgery or repair", f"{_at(v)} mentions prior surgery or repair{_quote(v)}."),
    "speculative_language": lambda v: ("Hedged wording", f"Hedged wording in {_at(v)}{_quote(v)}."),
    "patient_report": lambda v: ("Reported onset", f"Onset wording reported in {_at(v)}{_quote(v)}."),
    "missed_care": lambda v: ("Missed or ended care", f"Wording about missed appointments or ending care in {_at(v)}{_quote(v)}."),
    "new_onset": lambda v: ("New-onset wording", f"New-onset wording in {_at(v)}{_quote(v)}."),
    "scene_facts": lambda v: ("Scene facts", f"Scene facts recorded by {_at(v)}{_quote(v)}."),
    "alternative_cause": lambda v: ("Mention of another injury or event", f"Mention of another injury or event in {_at(v)}{_quote(v)}."),
    "litigation_referral": lambda v: ("Attorney referral", f"Referral wording in {_at(v)}{_quote(v)}."),
    "objective_negative": lambda v: ("Normal or absent findings wording", f"Wording about normal or absent findings in {_at(v)}{_quote(v)}."),
    "credibility_language": lambda v: ("Credibility wording a defense reviewer may quote", f"Wording in {_at(v)} that questions effort or symptom credibility{_quote(v)}."),
    "accident_date_provenance": lambda v: ("Accident date source", f"Accident date as stated in {_at(v)}{_quote(v)}."),
    "date_ambiguous": _date_amb,
== export.py _SELF / category rendering
41:# Order inside a merged flag line (most adjuster-actionable first); both the lexicon subtypes and the closed category names.
113:    def __init__(self, case):
114:        self.records = {r["n"]: r for r in case.get("records", [])}
116:        self.export_config = cfg if any(cfg.get(k) is not None for k in ("exhibit", "bates_prefix", "bates_start")) else None
117:        self.entries = sorted(case.get("entries", []), key=lambda e: (self._date(e), e["record_no"], str(e.get("id"))))
118:        self.amounts = sorted(case.get("amounts", []), key=lambda a: (self._date(a), a["record_no"], str(a.get("id"))))
119:        self.flags = list(case.get("flags", []))
120:        self.narrative = case.get("narrative")
121:        self.keep_wording = {ev.get("item_id") for ev in case.get("events", []) if ev.get("type") == "keep_my_wording"}
123:    def verbatim(self, item):
125:        return _norm(item.get("excerpt")) in _norm(self.text(item["record_no"]))
128:    def in_entries(self):
129:        return [e for e in self.entries if _status(e) == "in" and self.verbatim(e)]
132:    def narrative_sentences(self):
134:        n = self.narrative
137:        live = {e["id"]: e for e in self.in_entries}
141:    def in_charges(self):
142:        return [a for a in self.amounts if a["cls"] == "charge" and a.get("cents") is not None
143:                and _status(a) == "in" and self.verbatim(a)]
145:    def _date(self, item):
146:        return self.date_of(item) or "9999-12-31"
148:    def date_of(self, item):
149:        return item.get("date_iso") or (self.records.get(item["record_no"]) or {}).get("date_iso")
151:    def source_prefix(self, n):
153:        pg = (self.records.get(n) or {}).get("page")
154:        head = SOURCE_PREFIX[:-2] if self.export_config is None else self._bracket(n)
157:    def _bracket(self, n):
159:        c = self.export_config
165:    def source(self, n):
166:        return (self.records.get(n) or {}).get("source", "")
168:    def text(self, n):
169:        return (self.records.get(n) or {}).get("excerpt", "")
171:    def rec_date(self, n):
172:        return (self.records.get(n) or {}).get("date_iso")
174:    def cite(self, n):
175:        return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"
177:    def cite_dated(self, n):
178:        return f"record {n} ({self.source(n)}, dated {_long_date(self.rec_date(n))})"
180:    def quote(self, n, ev, whole_sentence=False):
183:        text = self.text(n)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:49:41.423Z

**tool call — Bash**
````
{
 "command": "echo \"== mock_flags.js head\" && sed -n 1,30p app/frontend/mock_flags.js | cut -c1-400; echo \"== usages of MOCK globals\" && grep -rn \"MOCK_FLAGS\\|mockFlags\\|MOCK_\\|window.MOCK\\|__MOCK\" app/frontend/*.js | grep -v \"^app/frontend/mock\" | head -20; echo \"== api.js fallback\" && grep -n -i \"mock\\|fallback\" app/frontend/api.js | head -20; echo \"== mock_flags.js line 24 exact\" && sed -n 24,25p app/frontend/mock_flags.js; echo \"== dev mock-data.js 740-752\" && sed -n 740,752p app/frontend/dev/mock-data.js",
 "description": "Inspect mock_flags.js reachability and api.js fallback"
}
````

### User / tool · 2026-11-02T02:49:41.535Z

**tool result**
````
== mock_flags.js head
/* Mock-only overlay (T-043): adds the sample's conflict / pre-existing / causation flags to ZL.mock so ?api=mock shows all four groups.
   Wraps ZL.mock.handle; flags it adds keep their own review state here. Not used when API_MODE is "real". */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  if (!ZL.mock || !ZL.mock.handle) return;
  const orig = ZL.mock.handle.bind(ZL.mock);
  const extra = {};   // token -> flags
  const clone = (o) => JSON.parse(JSON.stringify(o));
  const find = (recs, rn, sub) => { const r = recs.find((x) => x.seq === rn); const i = r ? r.text.indexOf(sub) : -1; if (i < 0) return null; return { record_id: r.id, excerpt: sub, start: r.char_start + i, end: r.char_start + i + sub.length }; };
  function build(recs) {
    const mk = (id, type, category, title, explanation, ev, o) => ev.every(Boolean) ? Object.assign({ id, type, category, source_kind: "record", title, explanation, computed: {}, evidence: ev, origin: "code", reviewer_note: null,
      state: "verified", reasons: [], why: "Calculated by code; every quote is word for word in the records.", review_status: "pending", edited: null, ladder: { item_id: id, state: "verified", backend: "fixture", generator: null, judge: null, human: { action: null } } }, o || {}) : null;
    return [
      mk("f_acc_1", "conflict", "accident_date_after_treatment", "Stated accident date is later than recorded treatment",
        "Stated accident date 2026-01-19 (“Date of accident per intake form: 2026-01-19.”) is later than the first recorded treatment, 2026-01-09 (Austin EMS run report; Central ER discharge summary). The records disagree; the tool does not choose between them.",
        [find(recs, 7, "Date of accident per intake form: 2026-01-19."), find(recs, 1, "Date: 2026-01-09"), find(recs, 2, "Date: 2026-01-09")]),
      mk("f_plan_4_6", "conflict", "treatment_plan_vs_actual", "Planned visits differ from visits attended",
        "Plan of care lists 12 visits (Capital PT, initial evaluation); discharge is recorded at visit 9 after two missed appointments.",
        [find(recs, 4, "Plan of care: 12 visits."), find(recs, 6, "Discharged from PT after two missed appointments.")], { state: "needs_review", reasons: ["LEXICON_ONLY"], why: "The phrase list and the model disagree on this flag." }),
      mk("f_pre_3", "pre_existing", "pre_existing", "Earlier complaint mentioned", "Dr. Alvarez, primary care (January 16, 2026) mentions low back pain in 2023.",
        [find(recs, 3, "Patient reports low back pain in 2023, resolved.")], { state: "needs_review", reasons: ["LLM_ONLY"], why: "The model found this; the phrase list did not." }),
      mk("f_deg_8", "pre_existing", "degenerative_language", "Degenerative wording in imaging", "Austin Imaging, cervical MRI (May 29, 2026): “Findings may represent degenerative change; correlate clinically.”",
        [find(recs, 8, "Findings may represent degenerative change; correlate clinically.")]),
      mk("f_pat_9", "causation", "patient_report", "Patient self-report", "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
        [find(recs, 9, "Patient states symptoms began after the January collision.")]),
    ].filter(Boolean);
  }
  ZL.mock.handle = async function (method, path, body) {
    const m = /^\/cases\/([^/]+)(\/.*)?$/.exec(path);
    const token = m ? decodeURIComponent(m[1]) : "", sub = m ? m[2] || "" : "";
== usages of MOCK globals
== api.js fallback
1:/* API client. ONE switch: API_MODE. "mock" uses mock.js (in-memory, contract-shaped); "real" calls the FastAPI backend under /api.
2:   `?api=real` / `?api=mock` in the page URL overrides the constant (used by tests). */
5:  const API_MODE = "real"; // <-- the ONE switch: "real" (FastAPI under /api) or "mock" (in-memory, mock.js)
16:    if (mode === "mock") {
17:      ({ status, body: data } = await ZL.mock.handle(method, path, body));
== mock_flags.js line 24 exact
      mk("f_pat_9", "causation", "patient_report", "Patient self-report", "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
        [find(recs, 9, "Patient states symptoms began after the January collision.")]),
== dev mock-data.js 740-752
    }
   }
  },
  {
   "id": "f_pat_9",
   "type": "causation",
   "category": "patient_report",
   "source_kind": "record",
   "title": "Patient self-report",
   "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): \u201cPatient states symptoms began after the January collision.\u201d",
   "computed": {},
   "evidence": [
    {
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:49:56.140Z

**tool call — Bash**
````
{
 "command": "echo \"== frontend uses of .category / category\" && grep -rn \"category\" app/frontend/*.js | grep -v \"^app/frontend/mock\" | head -30; echo \"== static mount / dev served?\" && grep -rn \"StaticFiles\\|frontend\" app/backend/*.py | grep -i \"static\\|mount\\|frontend\" | head; echo \"== golden lines 50-72\" && sed -n 50,72p evals/golden/sample.export.expected.txt; echo \"== export.py label map for categories\" && grep -n \"Causation language\\|_CAT\\|LABEL\\|label\" app/backend/export.py | head -30",
 "description": "Check frontend category rendering, static serving, golden lines and export labels"
}
````

### User / tool · 2026-11-02T02:49:56.255Z

**tool result**
````
== frontend uses of .category / category
app/frontend/flags.js:65:      "data-flag-type": f.type, "data-category": f.category, "data-state": f.state, "data-review": f.review_status || "pending" },
app/frontend/flags.js:70:    if (f.category === "date_ambiguous") { const dc = dateControl(c, f); if (dc) a.append(dc); }
== static mount / dev served?
app/backend/api.py:27:# index.html has one inline onclick (dialog Close); allowed by hash until the frontend moves it to a listener.
app/backend/api.py:508:    sd = pathlib.Path(static_dir) if static_dir else ROOT / "app" / "frontend"
app/backend/api.py:510:        from fastapi.staticfiles import StaticFiles
app/backend/api.py:511:        app.mount("/", StaticFiles(directory=str(sd), html=True), name="frontend")
== golden lines 50-72

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.

FLAGS ACCEPTED
- Gap: 73 days, March 6, 2026 to May 18, 2026: record 6 (Capital PT, visit 9, March 6, 2026) to record 7 (Hill Country Pain Management, new patient, May 18, 2026).
- Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
- Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
- Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Conflict, accident date.
- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Plan of care: 12 visits." Conflict, PT plan.
- Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
- Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
- Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.

AMOUNTS NOT TOTALED
- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.
== export.py label map for categories
248:def _flag_label(f):
257:        return "Causation language"
268:    """One flag as a note sentence: '<label>: <body>'."""
270:    label = _flag_label(f)
278:        return _terminate(f"{label}: {span}: " + " to ".join(v.cite(n) for n in recs))
300:            return f"{label}: " + " ".join(segs + [tail])
303:        return _terminate(f"{label}: " + "; ".join(items))
309:    return f"{label}: " + "; ".join(items)
330:            line = _terminate(f"{_flag_label(group[0])}: " + "; ".join(_flag_line(v, f).split(": ", 1)[1] for f in group))
346:                hits.append(_flag_label(f)) if _flag_label(f) not in hits else None   # a gap bounds these records' entries
352:                    if _flag_label(f) not in hits:
353:                        hits.append(_flag_label(f))
360:                lab = _flag_label(f)
373:def _ledger_label(v, n):
406:            body = f"Rate {m}{per}; visit count not stated{_plan_note(v, n)}. Request itemized {_ledger_label(v, n)}."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:50:02.786Z

**tool call — Bash**
````
{
 "command": "echo \"== golden lines 58,69 (numbered)\" && grep -n \"\" evals/golden/sample.export.expected.txt | sed -n '58p;69p' | cut -c1-600; echo \"== spec lines 280,291\" && grep -n \"\" spec/REQUIREMENTS.md | sed -n '280p;291p' | cut -c1-600; echo \"== git show 83b4353 diff\" && git show 83b4353 -- spec/REQUIREMENTS.md | cut -c1-400; echo \"== git show 4594bb7 golden diff\" && git show 4594bb7 -- evals/golden/sample.export.expected.txt | cut -c1-400; echo \"== export label fn\" && sed -n 246,262p app/backend/export.py",
 "description": "Compare spec and golden lines and show diffs and label function"
}
````

### User / tool · 2026-11-02T02:50:02.956Z

**tool result**
````
== golden lines 58,69 (numbered)
58:- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
69:- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.
== spec lines 280,291
280:- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain"; record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
291:- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.
== git show 83b4353 diff
commit 83b4353d1eba35aad357815fb0a1266f25be4320
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:49:08 2026 -0600

    spec: sync §6 export lines to golden after D-040 (T-074)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/spec/REQUIREMENTS.md b/spec/REQUIREMENTS.md
index 92496f5..9af2178 100644
--- a/spec/REQUIREMENTS.md
+++ b/spec/REQUIREMENTS.md
@@ -277,7 +277,7 @@ FLAGS ACCEPTED
 - Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
 - Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
 - Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
-- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill 
+- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."; record 7 (Hill Country Pain Managemen
 
 FLAGS DISMISSED
 - none
@@ -288,7 +288,7 @@ FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the e
 - Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
 - Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
 - Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
-- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language (patient self-report).
+- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.
 
 AMOUNTS NOT TOTALED
 - Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.
== git show 4594bb7 golden diff
commit 4594bb7bda9df44aa4e883d7e6cc595c6c721a02
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:48:46 2026 -0600

    fix(qa): export golden drops patient self-report suffix (D-040); declare btn-undo-batch test id
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/evals/golden/sample.export.expected.txt b/evals/golden/sample.export.expected.txt
index 913358b..6a0c38a 100644
--- a/evals/golden/sample.export.expected.txt
+++ b/evals/golden/sample.export.expected.txt
@@ -55,7 +55,7 @@ FLAGS ACCEPTED
 - Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): "41M restrained driver, rear-ended at approx. 35 mph." Record 2 (Central ER discharge summary, dated January 9, 2026). The tool does not choose between the dates. First recorded treatment: January 9, 2026.
 - Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
 - Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."; record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change".
-- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision." (patient self-report); record 7 (Hill 
+- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."; record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."; record 7 (Hill Country Pain Managemen
 
 FLAGS DISMISSED
 - none
@@ -66,7 +66,7 @@ FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the e
 - Record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from PT after two missed appointments." Gap; conflict, PT plan; causation language.
 - Record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers." Gap; causation language.
 - Record 8 (Austin Imaging, cervical MRI, May 29, 2026): "Findings may represent degenerative change; correlate clinically." Prior condition; causation language.
-- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language (patient self-report).
+- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.
 
 AMOUNTS NOT TOTALED
 - Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.
== export label fn

# ---------------------------------------------------------------- internal notes
def _flag_label(f):
    t, sub = f.get("type"), f.get("subtype")
    if t == "gap":
        return "Gap"
    if t == "conflict":
        return "Conflict, " + _CONFLICT_SUB.get(sub, (sub or "other").replace("_", " "))
    if t == "pre_existing":
        return "Prior condition"
    if t == "causation":
        return "Causation language"
    if t == "record_warning":
        return "Record warning"
    return _cap((t or "flag").replace("_", " "))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:50:08.520Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py 2>&1 | tail -40",
 "description": "Run the brief's three test files on the live tree",
 "timeout": 300000
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:50:10.029Z

**tool call — Bash**
````
{
 "command": "echo \"== uncommitted diff in test_eval_runner.py\" && git diff HEAD -- tests/unit/test_eval_runner.py && echo \"== spec vs golden exact line compare\" && diff <(sed -n 280p spec/REQUIREMENTS.md) <(sed -n 58p evals/golden/sample.export.expected.txt) && echo \"L280==G58 identical\" ; diff <(sed -n 291p spec/REQUIREMENTS.md) <(sed -n 69p evals/golden/sample.export.expected.txt) && echo \"L291==G69 identical\"; echo \"== spec/submission/memory mentions of self-report / patient_report chip\" && grep -rn -i \"self-report\\|self report\\|patient_report\\|self_report\\|chip\" spec/ submission/ memory/ docs/ 2>/dev/null | cut -c1-260 | head -40",
 "description": "Compare spec and golden lines exactly and grep spec for leftover self-report wording"
}
````

### User / tool · 2026-11-02T02:50:10.664Z

**tool result**
````
..............................................................           [100%]
62 passed in 1.82s
````

### User / tool · 2026-11-02T02:50:10.786Z

**tool result**
````
== uncommitted diff in test_eval_runner.py
diff --git a/tests/unit/test_eval_runner.py b/tests/unit/test_eval_runner.py
index e0a2d5f..735f8cc 100644
--- a/tests/unit/test_eval_runner.py
+++ b/tests/unit/test_eval_runner.py
@@ -357,3 +357,12 @@ def test_unsplit_paste_wrong_date_or_one_record_fails():
         if n == "unsplit_paste":
             o["records"][1]["date_iso"] = "2026-05-12"
     assert report(Perfect(mutate=bad_date))["metrics"]["unsplit_paste"]["value"] is False
+
+
+def test_live_backend_without_enable_live_is_refused(monkeypatch, tmp_path, capsys):
+    """T-070: LLM_BACKEND=claude-cli without ENABLE_LIVE=1 used to run on the fixture backend and report backend=fixture; now it exits 2."""
+    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
+    monkeypatch.delenv("ENABLE_LIVE", raising=False)
+    assert R.main(["--out", str(tmp_path)]) == 2
+    assert "ENABLE_LIVE=1" in capsys.readouterr().err
+    assert not list(tmp_path.glob("*.json"))
== spec vs golden exact line compare
L280==G58 identical
L291==G69 identical
== spec/submission/memory mentions of self-report / patient_report chip
spec/REQUIREMENTS.md:55:| R-TL-8 | **A hedge travels with its finding (D-018, D-021).** The **hedge set** is the lexicon entries with `hedge: true` in `app/llm/lexicon.yaml` (D-018); today `may_represent`, `correlate_clinically`, `possibility_terms`, `cannot_e
spec/REQUIREMENTS.md:57:| R-TL-10 | **Summaries keep the numbers and the qualifiers (D-006, D-022).** (a) A number, date, dollar figure or the word left, right, no, not or without in a summary must appear in the item's excerpt, the record's source label or its
spec/REQUIREMENTS.md:71:| R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = "patient_report"` and the UI text "Patient self-report". It is never presented as a physician's opinion. | Sample re
spec/REQUIREMENTS.md:371:| 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` and checks `required_terms` on summary+excerpt; D-022 and R-FL-7/R-TL-10 say `patient_report` and summary alone. Not a request to q
spec/SAMPLE_CASE_TRUTHS.md:9:- **Causation-weakening language:** "may represent degenerative change; correlate clinically" (8); "Discharged from PT after two missed appointments" (6); "Patient states symptoms began after the January collision" (9 — patient s
memory/SCOPE_CUTS.md:31:| debt | T-015 accepted with documented debt after 4 rounds (§7.4) | r3 blocker + self-report major resolved (haiku r4); remaining AI-line mismatch was in REQUIREMENTS R-EX-4(1), fixed by orchestrator to golden text; minor carried | se
memory/SCOPE_CUTS.md:44:| debt | T-036 accepted with documented debt after 3 rounds (§7.4) | r4: stale judge fixtures (backend-1 re-record in progress, verified at M2 gate eval); judge-outage run status minor carried; self-report items split to T-061 | see ca
memory/SCOPE_CUTS.md:49:| 21 | Patient self-report chip (`patient_report` source_kind) | Excerpts are verbatim, so the speaker is visible in the text; a speaker label failed four adversarial rounds (D-040). | ~2 days: a dependency-parse speaker attribution plu
memory/ORCHESTRATOR_DECISIONS.md:26:| D-018 | Lexicon contract: each entry has `flag_type` ∈ {pre_existing, causation, record_warning} (D-013 mapping) plus booleans `hedge` and `self_report`; `strength` high/medium raise flags, low is context only. Negation 
memory/ORCHESTRATOR_DECISIONS.md:30:| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `
memory/ORCHESTRATOR_DECISIONS.md:41:| D-033 | `patient_report` (self-report chip) applies only to explicit patient attribution ('Patient states/reports/notes', 'Pt c/o', patient-quoted speech). EMS narrative, witness, spouse/family statements and generic 'S:'/
memory/ORCHESTRATOR_DECISIONS.md:43:| D-035 | Simplifies D-033: `patient_report` is attached only to a **clause** that begins with an explicit patient subject ('Patient', 'Pt', 'The patient') followed by a reporting verb (states, reports, notes, says, endorses
memory/ORCHESTRATOR_DECISIONS.md:45:| D-037 | Final rule for `patient_report` (supersedes the clause-splitting in D-035, 2026-11-02): the chip attaches only when the **whole excerpt** is a single patient-subject clause (`Patient`/`Pt`/`The patient` + reporting
memory/ORCHESTRATOR_DECISIONS.md:48:| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four a
memory/GLOSSARY.md:39:- **Patient self-report** — history recorded as "patient states/reports"; records what the patient said, not a physician's causation opinion. Source: AA src 9.
memory/contracts/api.md:184:    { "id": "f_pat_9", "type": "causation", "category": "patient_report", "source_kind": "record",
memory/contracts/api.md:185:      "title": "Patient self-report",
memory/contracts/api.md:186:      "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
memory/contracts/api.md:193:        "generator": {"model": "claude-sonnet-5-5", "prompt_version": "flags_v1", "call_id": "c40", "output": {"type": "causation", "category": "patient_report", "record_id": "r9", "excerpt": "Patient states symptoms began after the
memory/contracts/api.md:194:        "code_checks": {"excerpt_verbatim": true, "lexicon_hit": "patient_report", "highlight_found": true, "injection_tag": false},
memory/contracts/api.md:212:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker lab
memory/contracts/api.md:469:| `SUMMARY_DROPS_QUALIFIER` | needs_review | the excerpt has a hedge, self-report marker, negation, laterality or "approx." that the summary leaves out (D-022) |
memory/DECISIONS.md:87:flags         id, case_id, type('gap'|'conflict'|'pre_existing'|'causation'|'record_warning', D-013), category (closed list, ADR-013), source_kind('record'|'patient_report'),
memory/DECISIONS.md:244:- **Dropped qualifiers (D-022, round 4).** A second function `grounding.dropped_qualifiers(summary, excerpt)` finds qualifiers in the excerpt (lexicon hedge set, `self_report` entries, negation words such as "without", laterality, "appr
memory/DECISIONS.md:251:  - **Lexicon contract (D-018).** `app/llm/lexicon.yaml` entries have `flag_type` (`pre_existing` | `causation` | `record_warning`), booleans `hedge` and `self_report`, and `strength` (`high`/`medium` raise flags; `low` is context only)
memory/DECISIONS.md:255:    - causation: `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (no objective findings, normal exam, WNL/full ROM), `recovery_context
memory/DECISIONS.md:272:    | patient_report | Patient self-report | Patient self-report (not a physician's opinion) in {provider} ({date}): “{quote}”. |
memory/DECISIONS.md:286:  - `source_kind = "patient_report"` and the "Patient self-report" chip are **cut (D-040)**, which supersedes the lexicon-driven rule first written here and D-033/D-035/D-037; the code setter was removed in T-071 (commit a27e3a4). Every
memory/DECISIONS.md:334:  11. **Lexicon v2 dependency.** `lexicon.yaml` (flag_type, hedge, self_report, strength, `accident_date_phrases`, `non_encounter`, `injection`) is a researcher deliverable that blocks gaps, the accident-date conflict and the injection 
memory/DECISIONS.md:341:- Decision: the LLM split fallback is allowed only when the code split finds one record that is unsplit or lacks a date or source label; it returns offsets only, is validated by `ingest.validate_split` and marks records `LLM_SPLIT`; on 
docs/UI_DESIGN_BRIEF.md:6:D-010/D-011 (accept / edit / dismiss, nothing accepted by default, no batch accept); D-019 (one total line); D-022 (self-report per quote);
docs/UI_DESIGN_BRIEF.md:23:| `--t-caption` | 12 / 16 | 400 | metadata, record numbers, chip text, helper text |
docs/UI_DESIGN_BRIEF.md:24:| `--t-caption-strong` | 12 / 16 | 600 | chip text, column headers (sentence case, no all-caps) |
docs/UI_DESIGN_BRIEF.md:39:Radius: 4 px on controls, chips and inputs; 6 px on cards; none on table rows. Borders instead of shadows: 1 px `--border`; one shadow token only for
docs/UI_DESIGN_BRIEF.md:69:| `--border-strong` | `#6F7B8B` | `#7A8696` | input, button and chip outlines |
docs/UI_DESIGN_BRIEF.md:105:`forced-colors` mode: chips keep their outline and icon, highlight uses `Highlight`/`HighlightText`; `prefers-reduced-motion`: no transitions longer than
docs/UI_DESIGN_BRIEF.md:132:| `Patient self-report` | speech bubble | Patient self-report | `--text-muted` outline | only where code set `source_kind=patient_report` (T-061 narrows this) |
docs/UI_DESIGN_BRIEF.md:134:"Verified" is never styled as approval: no green row background, no check on the primary action. Machine verification and human acceptance are two separate chips.
docs/UI_DESIGN_BRIEF.md:142:2. **Line 1:** `--t-body-strong` long date ("January 9, 2026") · provider label exactly as written (D-014) in `--t-body` · record number chip `Rec 2` (`--t-caption`).
docs/UI_DESIGN_BRIEF.md:143:   Right side: state chip(s) (section 6), at most two visible, overflow into "+1".
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:50:33.369Z

**tool call — Bash**
````
{
 "command": "echo \"== frontend/e2e/CSS: 'patient report' or speaker labels (case-insens.)\" && grep -rn -i \"patient report\\|patient-report\\|patient_report\\|self.report\\|patient self\\|speech bubble\" app/frontend tests/e2e styles 2>/dev/null | grep -v \"mock_flags.js\\|dev/mock-data.js\" | head; echo \"== data-category selectors in CSS\" && grep -rn \"data-category\" app/frontend/*.css app/frontend/*.js | head; echo \"== export.py: any 'patient' / 'self' / category/title use in flag body\" && grep -n -i \"patient\\|\\\"self\\|title\\|subtype\\|\\.get(\\\"category\\|\\[\\\"category\\\"\\]\" app/backend/export.py | head -30; echo \"== flag_templates _at/_quote and how title is produced\" && grep -n \"def _at\\|def _quote\\|def render\\|def title_and_explanation\\|return (\" app/backend/flag_templates.py | head; echo \"== 3b6a3fe e2e diff\" && git show 3b6a3fe -- tests/e2e/test_flags_panel.py app/backend/flag_templates.py | cut -c1-260",
 "description": "Check frontend, CSS, e2e, export for speaker labels and category rendering"
}
````

### User / tool · 2026-11-02T02:50:33.528Z

**tool result**
````
== frontend/e2e/CSS: 'patient report' or speaker labels (case-insens.)
app/frontend/mock.js:11:    5: "Pain 4/10, improving; patient reports missing 3 days of work.",
app/frontend/mock_sample.js:2:window.ZL=window.ZL||{};ZL.MOCK_SAMPLE="SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data\n\n=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: \"41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.\"\n\n=== Record 2 ===\nDate: 2026-01-09\nSource: Central ER discharge summary\nExcerpt: \"Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.\"\n\n=== Record 3 ===\nDate: 2026-01-16\nSource: Dr. Alvarez, primary care\nExcerpt: \"Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved.\"\n\n=== Record 4 ===\nDate: 2026-01-23\nSource: Capital PT, initial evaluation\nExcerpt: \"Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.\"\n\n=== Record 5 ===\nDate: 2026-02-20\nSource: Capital PT, visit 8\nExcerpt: \"Pain 4/10, improving. Patient reports missing 3 days of work.\"\n\n=== Record 6 ===\nDate: 2026-03-06\nSource: Capital PT, visit 9\nExcerpt: \"Discharged from PT after two missed appointments. Pain 3/10.\"\n\n=== Record 7 ===\nDate: 2026-05-18\nSource: Hill Country Pain Management, new patient\nExcerpt: \"New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.\"\n\n=== Record 8 ===\nDate: 2026-05-29\nSource: Austin Imaging, cervical MRI\nExcerpt: \"C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.\"\n\n=== Record 9 ===\nDate: 2026-06-12\nSource: Hill Country Pain Management, follow-up\nExcerpt: \"Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.\"";
tests/e2e/test_flags_panel.py:19:def test_patient_self_report_label(page, sample_case):
== data-category selectors in CSS
app/frontend/flags.js:65:      "data-flag-type": f.type, "data-category": f.category, "data-state": f.state, "data-review": f.review_status || "pending" },
== export.py: any 'patient' / 'self' / category/title use in flag body
10:    flags:   [{id, type, subtype, evidence:[{record_no, field, excerpt}], review_status, [days, from_date, to_date], [note], [reason]}]
21:LETTER_TITLE = "TREATMENT CHRONOLOGY"
22:CHARGES_TITLE = "BILLED CHARGES"
23:SUMMARY_TITLE = "TREATMENT SUMMARY"
24:NOTES_TITLE = "INTERNAL REVIEW NOTES — DO NOT SEND"
41:# Order inside a merged flag line (most adjuster-actionable first); both the lexicon subtypes and the closed category names.
42:_ORDER = ["hedged_imaging", "speculative_language", "noncompliance", "missed_care", "patient_reported_onset", "patient_report",
228:    out = [LETTER_TITLE, ""]
233:        out += [SUMMARY_TITLE, ""] + [f"{x['text']} ({_cite_tail(v, x['entry_id'])})" for x in sents] + [""]
236:        out += [CHARGES_TITLE, ""]
249:    t, sub = f.get("type"), f.get("subtype")
282:        if f.get("subtype") == "accident_date":
321:            merged[t][2].sort(key=lambda g: _ORDER.index(g.get("subtype")) if g.get("subtype") in _ORDER else 99)
347:            if f.get("type") == "conflict" and f.get("subtype") in _ACCIDENT_SUBS and not any(
543:        NOTES_TITLE, "",
== flag_templates _at/_quote and how title is produced
55:def _quote(v, key="quote"):
59:def _at(v, key="provider", dkey="date"):
88:    return ("Stated accident date is later than recorded treatment",
111:    return ("Instruction-like text in a record",
151:def render(flag_type: str, subtype: str, **vars) -> tuple:
== 3b6a3fe e2e diff
commit 3b6a3fec601b35657a7c90690d78902215855b74
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:47:04 2026 -0600

    feat(backend): neutral 'Reported onset' flag title; drop '(patient self-report)' from export (D-040, T-072)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/flag_templates.py b/app/backend/flag_templates.py
index 6ae05f0..6600be8 100644
--- a/app/backend/flag_templates.py
+++ b/app/backend/flag_templates.py
@@ -123,7 +123,7 @@ TEMPLATES = {
     "degenerative_language": lambda v: ("Degenerative wording", f"{_at(v)} uses degenerative wording{_quote(v)}."),
     "prior_surgery": lambda v: ("Mention of prior surgery or repair", f"{_at(v)} mentions prior surgery or repair{_quote(v)}."),
     "speculative_language": lambda v: ("Hedged wording", f"Hedged wording in {_at(v)}{_quote(v)}."),
-    "patient_report": lambda v: ("Patient self-report", f"Patient self-report (not a physician's opinion) in {_at(v)}{_quote(v)}."),
+    "patient_report": lambda v: ("Reported onset", f"Onset wording reported in {_at(v)}{_quote(v)}."),
     "missed_care": lambda v: ("Missed or ended care", f"Wording about missed appointments or ending care in {_at(v)}{_quote(v)}."),
     "new_onset": lambda v: ("New-onset wording", f"New-onset wording in {_at(v)}{_quote(v)}."),
     "scene_facts": lambda v: ("Scene facts", f"Scene facts recorded by {_at(v)}{_quote(v)}."),
diff --git a/tests/e2e/test_flags_panel.py b/tests/e2e/test_flags_panel.py
index 25882a9..67a97d1 100644
--- a/tests/e2e/test_flags_panel.py
+++ b/tests/e2e/test_flags_panel.py
@@ -17,8 +17,8 @@ def test_both_conflicts_present_not_merged(page, sample_case):
     assert "2026-01-19" in t and "rear-ended" in t and "12 visits" in t
 
 def test_patient_self_report_label(page, sample_case):
-    """R-FL-7: the record-9 causation flag shows 'Patient self-report'."""
-    open_case(page, sample_case); assert "Patient self-report" in flags(page).inner_text()
+    """R-FL-7: the record-9 causation flag shows 'Reported onset'."""
+    open_case(page, sample_case); assert "Reported onset" in flags(page).inner_text()
 
 def test_flag_edit_is_note_only(page, sample_case):
     """R-RV-2: the only editable field on a flag is the reviewer note."""
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:50:39.039Z

**tool call — Bash**
````
{
 "command": "echo \"== e2e uses mock mode?\" && grep -rn \"api=mock\" tests/ | head -5; echo \"== golden-related tests\" && grep -rln \"sample.export.expected\\|expected.txt\" tests/ | head; echo \"== make_curated location\" && ls tools/ | grep -i curat; ls evals/ | head -30; echo \"== test names referencing self-report\" && grep -rn -i \"self_report\\|self-report\\|patient_self\" tests/ | cut -c1-220 | head -20",
 "description": "Locate golden-related tests and mock-mode usage in tests"
}
````

### User / tool · 2026-11-02T02:50:39.184Z

**tool result**
````
== e2e uses mock mode?
== golden-related tests
tests/unit/test_grounding.py
tests/unit/_golden.py
tests/unit/test_export.py
tests/fixtures/make_curated.py
tests/fixtures/llm/curated/bc66f801341fe95dcff0620870e5237a7cf8ee1b1630413bf59f24a34b10f5fb.json
tests/fixtures/llm/curated/056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d.json
tests/fixtures/llm/curated/9477789eaee295aff7a0f64647f29266fe8fc7b275e2519b02d9d5a3dc5b59e7.json
tests/fixtures/llm/curated/664c59ebfe49e6a09404138fe7cd6d77ba2306b53dfe431bc7ead34b14de3c4c.json
tests/fixtures/llm/curated/f5212e784cce54b0dd547f184cd405c56e7ebec814f8257f091fe60ffe2eda10.json
tests/fixtures/llm/curated/bde3b432c62b6dd09e7d4e18309d7d874292d52854fcd3d186de68b03933ce91.json
== make_curated location
__init__.py
golden
lexicon_heldout.jsonl
library
matching.py
reports
run.py
== test names referencing self-report
tests/unit/test_grounding.py:124:    """R-TL-10(b)/D-022: summary omits a negation / hedge / self-report marker / 'approx.' the excerpt carries -> SUMMARY_DROPS_QUALIFIER."""
tests/unit/test_export_edge.py:63:    assert "Conflict, PT plan:" in n and '"Charge per visit $185."' in n and "self-report" not in n
tests/unit/test_export_edge.py:70:    assert title == "Reported onset" and "self-report" not in (title + expl).lower() and "patient self" not in expl.lower()
tests/unit/test_flags_pass.py:95:def test_no_flag_carries_a_self_report_chip():
tests/unit/test_flags_pass.py:151:    assert not hasattr(GR, "has_self_report") and not hasattr(GR, "patient_report_spans")
tests/unit/test_narrative.py:50:E5 = "On February 20, 2026, Capital PT recorded pain 4/10, improving"     # e5 quote: 'Pain 4/10, improving.' (no hedge, no self-report marker)
tests/unit/test_eval_runner.py:31:            attrib = [sp["attribution_any"][0] for sp in e.get("self_report_spans", [])]
tests/e2e/test_flags_panel.py:19:def test_patient_self_report_label(page, sample_case):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:50:42.260Z

**tool call — Bash**
````
{
 "command": "ls tests/unit/test_case_extras.py tests/unit/test_export_edge.py 2>&1; echo \"== live: golden/export tests\" && .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_export_edge.py tests/unit/test_case_extras.py tests/unit/test_flags_pass.py 2>&1 | tail -15; echo \"== live: make_curated --check\" && .venv/bin/python tests/fixtures/make_curated.py --check 2>&1 | tail -8; echo \"exit=$?\"",
 "description": "Run export, golden, and curated-fixture checks on live tree",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:50:45.467Z

**tool result**
````
tests/unit/test_case_extras.py
tests/unit/test_export_edge.py
== live: golden/export tests
...............................................................          [100%]
63 passed in 2.40s
== live: make_curated --check
entries: 9 non-verified: []
narrative: 9 sentences, removed: []
letter equal: True | notes equal: True
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:50:49.091Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python tests/fixtures/make_curated.py --check >/dev/null 2>&1; echo \"make_curated --check exit=$?\"; .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte tests/unit/test_case_extras.py::test_default_export_is_byte_identical_to_golden tests/unit/test_export_edge.py::test_patient_report_flag_title_is_neutral -v 2>&1 | tail -8; echo \"== HEAD archive (83b4353) for commit-based evidence\"; D=artifacts/review-evidence/T-072-T-074-83b4353; mkdir -p $D && git archive 83b4353 | tar -x -C $D && cd $D && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py 2>&1 | tail -5; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export_edge.py tests/unit/test_case_extras.py tests/unit/test_flags_pass.py 2>&1 | tail -5; /Users/arsis/zlayt-pm-project/.venv/bin/python tests/fixtures/make_curated.py --check >/dev/null 2>&1; echo \"archive make_curated --check exit=$?\"",
 "description": "Run named golden tests live, then test HEAD 83b4353 from a git archive",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:50:55.716Z

**tool result**
````
make_curated --check exit=0

============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0
rootdir: /Users/arsis/zlayt-pm-project
plugins: anyio-4.16.0
collected 2 items

============================ no tests ran in 0.24s =============================
== HEAD archive (83b4353) for commit-based evidence
.............................................................            [100%]
61 passed in 1.91s
..........................................                               [100%]
42 passed in 2.53s
archive make_curated --check exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:50:58.910Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_export.py tests/unit/test_case_extras.py tests/unit/test_export_edge.py -v 2>&1 | grep -i \"golden\\|neutral\\|byte\\|passed\\|failed\\|error\" | head -20; echo \"== grep test names\"; grep -n \"def test_sample_all_accepted_equals_golden_byte_for_byte\\|def test_default_export_is_byte_identical_to_golden\\|def test_patient_report_flag_title_is_neutral\" tests/unit/*.py",
 "description": "Run golden test ids verbosely and confirm their definitions",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T02:51:01.604Z

**tool result**
````
tests/unit/test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte PASSED [  2%]
tests/unit/test_export.py::test_deterministic PASSED                     [  4%]
tests/unit/test_export.py::test_total_line_has_no_parenthetical PASSED   [  7%]
tests/unit/test_export.py::test_letter_has_no_flag_content PASSED        [  9%]
tests/unit/test_export.py::test_dismissed_entry_absent_and_reconciled PASSED [ 12%]
tests/unit/test_export.py::test_dismissed_charge_changes_total PASSED    [ 14%]
tests/unit/test_export.py::test_rate_and_unclear_only_in_notes PASSED    [ 17%]
tests/unit/test_export.py::test_only_accepted_or_edited_exported_subset_equality PASSED [ 19%]
tests/unit/test_export.py::test_edited_marker_never_in_letter PASSED     [ 21%]
tests/unit/test_export.py::test_no_double_dot_and_money_format PASSED    [ 24%]
tests/unit/test_export.py::test_letter_builder_takes_no_flags_argument PASSED [ 26%]
tests/unit/test_export.py::test_every_letter_line_is_an_allowed_kind PASSED [ 29%]
tests/unit/test_export.py::test_total_line_unchanged_with_rate_non_dismissed PASSED [ 31%]
tests/unit/test_export.py::test_case_07_total_line_is_420 PASSED         [ 34%]
tests/unit/test_export.py::test_notes_sections_in_r_ex_4_order PASSED    [ 36%]
tests/unit/test_export.py::test_every_record_citation_has_provider_and_date PASSED [ 39%]
tests/unit/test_export.py::test_bills_to_request_line_exact PASSED       [ 41%]
tests/unit/test_export.py::test_dismiss_5_pending_6_reconciliation_and_counts PASSED [ 43%]
tests/unit/test_export.py::test_edited_items_section PASSED              [ 46%]
tests/unit/test_export.py::test_edited_then_accepted_entry_still_listed_in_edited_items PASSED [ 48%]
== grep test names
tests/unit/test_case_extras.py:104:def test_default_export_is_byte_identical_to_golden_and_config_fills_the_citation():
tests/unit/test_export.py:31:def test_sample_all_accepted_equals_golden_byte_for_byte():
tests/unit/test_export_edge.py:66:def test_patient_report_flag_title_is_neutral():
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:51:10.983Z

**tool call — Bash**
````
{
 "command": "grep -n \"Patient states\\|physician\\|self-report\\|Reported onset\" evals/golden/sample.export.expected.txt | cut -c1-200; echo \"== golden letter section lines 1-49 (grep for record 9 entry)\"; grep -n \"Record 9\\|record 9\\|2026-06-12\" evals/golden/sample.export.expected.txt | cut -c1-220 | head; echo \"== hallucination/evals report named in T-072 AC\"; ls evals/reports/ | tail -5; test -f evals/reports/20261102T024822Z.md && echo \"report 20261102T024822Z.md exists\" ; test -f evals/reports/20261102T024653Z.md && echo \"report 20261102T024653Z.md exists\"; grep -n -i \"hallucination\" evals/reports/20261102T024822Z.md 2>/dev/null | head -5",
 "description": "Check golden letter for remaining patient-statement markers and eval report evidence"
}
````

### User / tool · 2026-11-02T02:51:11.112Z

**tool result**
````
38:Source [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."
58:- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from
69:- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.
== golden letter section lines 1-49 (grep for record 9 entry)
58:- Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "may represent degenerative change; correlate clinically"; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed
69:- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Patient states symptoms began after the January collision." Causation language.
78:- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Recommend cervical epidural steroid injection." Request cost estimate.
== hallucination/evals report named in T-072 AC
20261102T024653Z.md
20261102T024822Z.md
20261102T025055Z.md
latest.json
m3-sensors.md
report 20261102T024822Z.md exists
report 20261102T024653Z.md exists
16:| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
33:- seeded hallucinations not caught: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:51:46.638Z

**tool call — Bash**
````
{
 "command": "echo \"== spec R-FL-7 (line 71) full\" && sed -n 71p spec/REQUIREMENTS.md; echo \"== spec line 371 (full)\" && sed -n 371p spec/REQUIREMENTS.md | cut -c1-500; echo \"== spec 55/57 self-report context\" && sed -n 55p spec/REQUIREMENTS.md | grep -o \".\\{120\\}self-report.\\{80\\}\"; sed -n 57p spec/REQUIREMENTS.md | grep -o \".\\{100\\}self-report.\\{60\\}\"; echo \"== SAMPLE_CASE_TRUTHS line 9\" && sed -n 9p spec/SAMPLE_CASE_TRUTHS.md | cut -c1-500; echo \"== any 'patient self' in spec/submission\" && grep -rn -i \"patient self\" spec/ submission/ 2>/dev/null | cut -c1-160; echo \"== leftover _SELF_REPORT in app/backend\" && grep -rn \"_SELF_REPORT\\|has_self_report\" app/backend | head -5; echo \"== dev/ reachable via static mount? panels.html exists:\" && ls app/frontend/dev/ && grep -n \"\\\"/dev\\|'/dev\\|dev/\" app/backend/api.py | head -3; echo \"== present.py line 74 category exposure\" && sed -n 72,76p app/backend/present.py | cut -c1-250; echo \"== board validate (read-only)\" && python3 tools/board.py validate 2>&1 | tail -15",
 "description": "Inspect spec R-FL-7 and truth doc, leftover refs, API exposure, and board validate",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T02:51:46.852Z

**tool result**
````
== spec R-FL-7 (line 71) full
| R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = "patient_report"` and the UI text "Patient self-report". It is never presented as a physician's opinion. | Sample record 9 flag has `source_kind == "patient_report"` and the label renders. Golden `must_not` M10 passes. | UT + E2E |
== spec line 371 (full)
| 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` and checks `required_terms` on summary+excerpt; D-022 and R-FL-7/R-TL-10 say `patient_report` and summary alone. Not a request to qa: the orchestrator records which wins, and the loser is edited by its owner. | `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md` | orchestrator (D-entry) |
== spec 55/57 self-report context
e entry is `needs_review` with reason `EXCERPT_OMITS_QUALIFIER`. Other lexicon sentences (`pre_existing`, `compliance`, self-report) are **not** forced into the excerpt; they surface as flags. A unit is never cu
needs_review` (`SUMMARY_TOKEN_NOT_IN_EXCERPT`). (b) If the excerpt contains a qualifier (a hedge, a self-report marker, a negation such as "without loss of consciousness",
== SAMPLE_CASE_TRUTHS line 9
- **Causation-weakening language:** "may represent degenerative change; correlate clinically" (8); "Discharged from PT after two missed appointments" (6); "Patient states symptoms began after the January collision" (9 — patient self-report, not a physician's causation opinion); "New onset" symptoms after a 73-day gap (7); the wrong accident date (7).
== any 'patient self' in spec/submission
spec/SAMPLE_CASE_TRUTHS.md:9:- **Causation-weakening language:** "may represent degenerative change; correlate clinically" (8); "Discharged from PT after two mi
spec/REQUIREMENTS.md:71:| R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = "patient_report"
== leftover _SELF_REPORT in app/backend
== dev/ reachable via static mount? panels.html exists:
harness.js
mock-data.js
mock-review.js
panels.html
== present.py line 74 category exposure

def flag_view(row, recs):
    return {**_common(row), "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
            "explanation": row["explanation"], "computed": _computed(row["computed"]), "evidence": _evidence(row["evidence"], recs),
            "origin": row["origin"], "reviewer_note": row["reviewer_note"]}
== board validate (read-only)
ok (74 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:52:11.032Z

**tool call — Bash**
````
{
 "command": "grep -n \"api=mock\\|api=real\" app/frontend/api.js | head -3; grep -n \"patient self-report\\|Patient self-report\" app/frontend/mock_flags.js app/frontend/dev/mock-data.js | cut -c1-120; grep -n \"\\\"title\\\": \\\"Patient\\|\\\"explanation\\\": \\\"Patient\" app/frontend/dev/mock-data.js | cut -c1-100; grep -n \"\\\"patient_report\\\": lambda\\|Reported onset\" app/backend/flag_templates.py; grep -n \"def flag_view\\|\\\"category\\\": row\" app/backend/present.py; grep -n \"data-category\\|f.title\\|\\.title\" app/frontend/flags.js | cut -c1-160 | head -5; grep -n \"def test_no_flag_carries_a_self_report_chip\" tests/unit/test_flags_pass.py; grep -n \"self_report\\|self-report\\|patient\" tests/unit/test_eval_spec_check.py | head -5; grep -n \"def test_\" tests/unit/test_eval_spec_check.py | head -5; grep -n \"source_kind\" app/backend/flags.py | head -3; grep -n \"M10\" evals/golden/*.json 2>/dev/null | head -3; ls reviews/ | grep -i \"T-07[24]\" ; echo \"reviews-check exit=$?\"",
 "description": "Confirm exact citation lines and check spec-check test coverage and existing review files"
}
````

### User / tool · 2026-11-02T02:52:11.223Z

**tool result**
````
2:   `?api=real` / `?api=mock` in the page URL overrides the constant (used by tests). */
app/frontend/mock_flags.js:24:      mk("f_pat_9", "causation", "patient_report", "Patient self-report", "Patient self-re
app/frontend/dev/mock-data.js:748:   "title": "Patient self-report",
app/frontend/dev/mock-data.js:749:   "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pai
748:   "title": "Patient self-report",
749:   "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pain Manageme
126:    "patient_report": lambda v: ("Reported onset", f"Onset wording reported in {_at(v)}{_quote(v)}."),
73:def flag_view(row, recs):
74:    return {**_common(row), "type": row["type"], "category": row["category"], "source_kind": row["source_kind"], "title": row["title"],
64:    const a = el("article", { class: "rv-card rv-flag", tabindex: "0", role: "group", "aria-label": f.title, "data-testid": "flag-" + f.id, "data-item-id": f
65:      "data-flag-type": f.type, "data-category": f.category, "data-state": f.state, "data-review": f.review_status || "pending" },
66:      el("div", { class: "rv-head" }, el("h4", { class: "rv-title" }, f.title), RV.chips(f)),
95:def test_no_flag_carries_a_self_report_chip():
5:def test_real_spec_matches_golden():
10:def test_changing_one_character_in_a_temp_copy_makes_it_false(tmp_path):
20:def test_cli_writes_spec_matches_golden_to_latest_json(tmp_path):
61:         "source_kind": "record",   # D-040: no code or model labels who is speaking
189:            "source_kind": "record",
226:            "reasons": ["CONFLICT_CHECK_INCOMPLETE"], "why": why.why("CONFLICT_CHECK_INCOMPLETE"), "excerpt": "", "source_kind": "record",
evals/golden/sample.expected.json:989:      "id": "M10",
reviews-check exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:52:14.281Z

**tool call — Bash**
````
{
 "command": "sed -n 986,996p evals/golden/sample.expected.json | cut -c1-240; echo ---; grep -n \"self-report\\|patient_report\\|self_report\" evals/golden/sample.expected.json | cut -c1-200 | head -8",
 "description": "Read golden M10 must_not entry and any self-report references in golden JSON"
}
````

### User / tool · 2026-11-02T02:52:14.380Z

**tool result**
````
      "unless_context": "(?i)\\b(not|no|without|rather than|nor|n't)\\b[^.;:]{0,20}$"
    },
    {
      "id": "M10",
      "statement": "Presents the patient's self-report (records 1, 9) as a physician's opinion or examination finding.",
      "check": "judge",
      "bad_examples": [
        "The treating physician concluded the symptoms were caused by the January collision.",
        "Dr. at Hill Country attributes the symptoms to the collision.",
        "Examination revealed neck injury with 7/10 pain.",
        "Patient states the collision caused his symptoms.",
---
109:      "self_report_spans": []
261:      "self_report_spans": [
625:      "summary": "Causation rests on patient self-report, not a physician's causation opinion.",
626:      "subtype": "patient_reported_onset"
990:      "statement": "Presents the patient's self-report (records 1, 9) as a physician's opinion or examination finding.",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:52:18.717Z

**tool call — Bash**
````
{
 "command": "sed -n 612,630p evals/golden/sample.expected.json | cut -c1-220; echo ---; sed -n 255,268p evals/golden/sample.expected.json | cut -c1-220; echo ---; grep -rn \"sample.expected.json\" tests/ evals/*.py 2>/dev/null | head -5",
 "description": "Read golden JSON entry around line 625 and its consumers"
}
````

### User / tool · 2026-11-02T02:52:18.824Z

**tool result**
````
      "cite": {
        "all": [
          9
        ],
        "any": []
      },
      "evidence": [
        {
          "record_no": 9,
          "field": "excerpt",
          "excerpt": "Patient states symptoms began after the January collision"
        }
      ],
      "summary": "Causation rests on patient self-report, not a physician's causation opinion.",
      "subtype": "patient_reported_onset"
    },
    {
      "id": "K4",
      "type": "causation",
---
          "patient states",
          "per patient",
          "patient reports",
          "patient-reported"
        ]
      ],
      "self_report_spans": [
        {
          "excerpt": "Patient states symptoms began after the January collision",
          "attribution_any": [
            "patient states",
            "per patient",
            "patient reports",
            "patient-reported"
---
tests/fixtures/make_curated.py:2:excerpts. Every answer below is derived from evals/golden (sample.export.expected.txt and sample.expected.json), never from a model.
tests/fixtures/make_curated.py:14:          "sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).")
tests/fixtures/make_curated.py:24:# per-record LLM flags (type, category, verbatim span) taken from sample.expected.json evidence
tests/fixtures/llm/curated/bc66f801341fe95dcff0620870e5237a7cf8ee1b1630413bf59f24a34b10f5fb.json:2: "CURATED": "CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).",
tests/fixtures/llm/curated/f5212e784cce54b0dd547f184cd405c56e7ebec814f8257f091fe60ffe2eda10.json:2: "CURATED": "CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:52:24.447Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'PY'\nimport json\nd=json.load(open(\"evals/golden/sample.expected.json\"))\ndef walk(o,path):\n    if isinstance(o,dict):\n        if o.get(\"summary\",\"\").startswith(\"Causation rests on patient self-report\"):\n            print(\"FOUND at\", path, \"id=\", o.get(\"id\"), \"keys=\", sorted(o.keys()))\n        for k,v in o.items(): walk(v,path+\"/\"+str(k))\n    elif isinstance(o,list):\n        for i,v in enumerate(o): walk(v,path+\"[%d]\"%i)\nwalk(d,\"\")\nprint(\"top keys:\", list(d.keys())[:20])\nPY\ngrep -rn \"\\\"summary\\\"\\|'summary'\" evals/run.py evals/golden/*.py 2>/dev/null | head -5; grep -rln \"expected_flags\\|must_flags\" evals/ tests/unit/ 2>/dev/null | head -5",
 "description": "Locate the golden JSON entry that carries the self-report summary and its parent key"
}
````

### User / tool · 2026-11-02T02:52:24.580Z

**tool result**
````
FOUND at /flags[7] id= K3 keys= ['cite', 'evidence', 'id', 'level', 'subtype', 'summary', 'type']
top keys: ['schema_version', 'case_id', 'synthetic', 'input_file', 'description', 'stress_types', 'records', 'entries', 'expected_entry_count', 'gap_excluded_records', 'gap_table', 'amounts', 'totals', 'flags', 'must_not_flag', 'tolerated', 'record_warnings', 'seeded_edits', 'must_not', 'notes']
evals/run.py:118:        summ = low(e.get("summary"))
evals/run.py:229:    tool_text = "\n".join([e.get("summary", "") for e in product_entries(out)] + [out.get("letter_text", "") or ""] +
evals/run.py
evals/reports/latest.json
evals/reports/20261102T024653Z.md
evals/reports/20261102T024355Z.md
evals/reports/20261102T023203Z.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:52:56.543Z

**tool call — Bash**
````
{
 "command": "echo \"== golden README\" && (grep -n \"patient_self_report\\|summary+excerpt\" evals/golden/README.md 2>&1 | head -3); echo \"== flags_pass test body\" && sed -n 95,100p tests/unit/test_flags_pass.py | cut -c1-200; echo \"== cleanup extracted archive\" && rm -rf artifacts/review-evidence/T-072-T-074-83b4353 && ls artifacts/review-evidence/ | head -20; echo \"== api.md 184-186 lines\" && sed -n 184,186p memory/contracts/api.md | cut -c1-160",
 "description": "Check golden README residue, test body, remove extracted archive, and confirm api.md lines"
}
````

### User / tool · 2026-11-02T02:52:56.749Z

**tool result**
````
== golden README
== flags_pass test body
def test_no_flag_carries_a_self_report_chip():
    """D-040: no code or model labels who is speaking, so every flag (including record 9's patient-statement flag) is a plain record flag."""
    for n in (7, 9):
        fl = F.lexicon_flags(rec(n))
        assert fl and all(f["source_kind"] == "record" for f in fl)

== cleanup extracted archive
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
== api.md 184-186 lines
    { "id": "f_pat_9", "type": "causation", "category": "patient_report", "source_kind": "record",
      "title": "Patient self-report",
      "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms beg
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:53:46.636Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-072-claims-adjuster.md",
 "content": "# T-072 review: claims-adjuster-reviewer (D-040 follow-through)\n\n**Verdict: fail** (one blocker). The export and golden are clean, and the flag template is neutral. The shipped frontend still shows the cut label in two places, which the brief's own grep check catches.\n\nModel: claude-haiku-5-5, per the brief and the runtime. The dossier's expected id (opus) does not match the model actually running.\n\n## What I checked\n\n- **Export, golden, tests (pass).** The golden letter and notes, and the live export, carry no \"(patient self-report)\". The record 9 quote stays verbatim as \"Patient states symptoms began after the January collision.\" (golden lines 38, 58, 69). No \"physician\" wording is added. The three brief test files pass (62 live; 61 at HEAD archive). The golden-byte tests pass (63 live, 42 at archive).\n- **Neutral template (pass).** `app/backend/flag_templates.py:126` gives title \"Reported onset\" and explanation \"Onset wording reported in ...\". `tests/unit/test_export_edge.py:70` asserts no \"self-report\" or \"patient self\" in the title or explanation.\n- **Internal id `patient_report` (not rendered as text, but exposed).** Text rendering uses `f.title` (`app/frontend/flags.js:66`). Export labels key on flag type only (`app/backend/export.py:248-257`). The id does appear in the API JSON (`app/backend/present.py:74`) and as a DOM attribute (`app/frontend/flags.js:65`). See F2.\n- **User-facing \"self-report\" grep (fails).** See F1.\n\n## Findings\n\n- **F1 blocker.** `app/frontend/mock_flags.js:24` and `app/frontend/dev/mock-data.js:748-749` still show \"Patient self-report (not a physician's opinion)\". The overlay loads on every page (`index.html:45`). It is reached through the `?api=mock` override (`api.js:2`) and the `/dev/panels.html` harness (`panels.html:12`, served under the static mount at `api.py:508-511`). The default mode is \"real\" (`api.js:5`), so this is not in the default product path. I read the code path; I did not render it in a browser.\n- **F2 minor.** Saying the id is \"never shown to users\" overstates it. It is not text, but `present.py:74` returns `\"category\": \"patient_report\"` in every flag payload, and `flags.js:65` writes it to `data-category`.\n- **F3 minor.** `evals/golden/sample.expected.json:625` (flag K3) still has `\"summary\": \"Causation rests on patient self-report, not a physician's causation opinion.\"` Commit 4594bb7 fixed only the `.txt` golden.\n- **F4 nit.** \"Reported onset\" still implies a reporter. \"Onset wording\" would match the sibling \"New-onset wording\" (`flag_templates.py:127`). This is not a D-040 violation.\n- **F5 nit.** `tests/e2e/test_flags_panel.py:19` is still named `test_patient_self_report_label`, though it asserts \"Reported onset\".\n\n```json\n{\"card\": \"T-072\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commits 3b6a3fe and 4594bb7 (HEAD 83b4353 extracted with git archive to artifacts/review-evidence/T-072-T-074-83b4353 for test runs, extract removed afterwards); live tree /Users/arsis/zlayt-pm-project is dirty (tests/unit/test_eval_runner.py +9 lines uncommitted, app/llm/backends/fixture.py and others), so live results are reported separately; sample case Appendix A records 1-9; no browser run\",\n \"exercised\": [\n  \"read personas/claims-adjuster.md in full; memory/ORCHESTRATOR_DECISIONS.md D-040, D-017, D-019; board show T-072; board validate -> 'ok (74 file(s))'\",\n  \"git show --stat 3b6a3fe 4594bb7; git status --short; git diff HEAD -- tests/unit/test_eval_runner.py\",\n  \"grep -rn -i 'self-report|self report|self-reported' app/ (excluding lexicon.yaml self_report keys); grep -rn 'patient_report|patient_reported_onset|source_kind' app/; grep -rln -i 'self.report|patient_report|source_kind' app/frontend\",\n  \"read app/backend/flag_templates.py:120-135, app/backend/export.py:246-262, app/frontend/flags.js:60-70, app/backend/present.py:72-76, app/frontend/api.js:1-6, app/frontend/index.html:42-64, app/frontend/dev/panels.html, app/backend/api.py:505-512\",\n  \"read app/frontend/mock_flags.js:20-30 and app/frontend/dev/mock-data.js:740-752; grep -n 'api=mock' tests/ (no e2e test uses mock mode)\",\n  \"golden check: grep -n for Patient states|physician|self-report|Reported onset in evals/golden/sample.export.expected.txt (lines 38, 58, 69 only); diff of 4594bb7 golden hunk\",\n  \".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py -> 62 passed in 1.82s (live tree)\",\n  \".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py at git archive 83b4353 -> 61 passed; tests/unit/test_export_edge.py tests/unit/test_case_extras.py tests/unit/test_flags_pass.py at 83b4353 -> 42 passed\",\n  \".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_export.py tests/unit/test_case_extras.py tests/unit/test_export_edge.py tests/unit/test_flags_pass.py (live) -> 63 passed; test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte PASSED\",\n  \".venv/bin/python tests/fixtures/make_curated.py --check -> 'letter equal: True | notes equal: True', exit 0 (live and at 83b4353)\",\n  \"evals.run not re-run (writes evals/reports, outside my write paths); the hallucination figure in the card was not re-checked\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"d040_no_speaker_label_user_facing\": 2, \"export_golden_fidelity\": 5, \"no_invented_facts_or_severity\": 5, \"internal_id_not_rendered_as_text\": 4, \"residue_cleanup_across_artifacts\": 2, \"tests_green_at_commit\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"User-reachable frontend code still displays 'Patient self-report' (D-040 violated; brief grep check fails)\",\n   \"evidence\": \"app/frontend/mock_flags.js:24: mk(\\\"f_pat_9\\\", \\\"causation\\\", \\\"patient_report\\\", \\\"Patient self-report\\\", \\\"Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): ...\\\"; app/frontend/dev/mock-data.js:748-749: \\\"title\\\": \\\"Patient self-report\\\", \\\"explanation\\\": \\\"Patient self-report (not a physician's opinion) in Hill Country Pain Management ...\\\". Reachability: app/frontend/index.html:45 loads mock_flags.js on every page; app/frontend/api.js:2 documents the ?api=mock page-URL override; app/frontend/flags.js:64 uses f.title as aria-label and :66 renders it as the card heading; app/frontend/dev/panels.html:12 loads mock-data.js; app/backend/api.py:508-511 mounts all of app/frontend (including dev/) as static files. Default mode is real (api.js:5 API_MODE = \\\"real\\\"), so the text is not in the default path; not rendered in a browser (code-path evidence only).\",\n   \"why_it_matters\": \"memory/ORCHESTRATOR_DECISIONS.md D-040: 'No code or model labels who is speaking.' This is the label the decision cut, with a 'not a physician's opinion' caveat, still in shipped code. A carrier or defense reviewer who opens ?api=mock sees a self-report label, which is the credibility problem D-040 exists to avoid. Severity is blocker under the D-040 rule. If Chris rules these overlays out of the deployed build, this drops to minor (see questions_for_chris).\",\n   \"fix\": \"Frontend-owned (app/frontend/**; open a frontend card, cross-boundary from this backend card). Change mock_flags.js:24 and dev/mock-data.js:748-749 to the neutral template text from app/backend/flag_templates.py:126 ('Reported onset'; 'Onset wording reported in ...'), or delete the f_pat_9 overlay entry.\",\n   \"acceptance_test\": \"grep -rn -i 'self-report|self report' app/frontend returns no hits; a Playwright test opens index.html?api=mock and asserts the flags panel contains 'Reported onset' and not 'self-report'; grep -c 'self-report' app/frontend/dev/mock-data.js is 0.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"'patient_report' is not rendered as text, but it is public API data; 'never shown to users' overstates\",\n   \"evidence\": \"app/backend/present.py:74: flag_view returns \\\"category\\\": row[\\\"category\\\"], \\\"source_kind\\\": row[\\\"source_kind\\\"]; app/frontend/flags.js:65: \\\"data-category\\\": f.category; text rendering uses f.title (flags.js:66) and export labels key on flag type only (app/backend/export.py:248-257, _flag_label). Card T-072 note 2026-11-02T02:47:25Z: 'the id is never shown to users'. Producers still emit it: app/backend/flag_templates.py:25; app/llm/lexicon.yaml:741,757; app/llm/prompts/flags_v1.md:13 ('the patient's own statement').\",\n   \"why_it_matters\": \"The brief's rendering check passes: the id is not text. But the id is the speaker label D-040 cut, it is returned in every flag payload, and the claim recorded on the card is inaccurate. An adjuster who inspects the network payload sees 'patient_report' on record 9.\",\n   \"fix\": \"Either (a) correct the card and decision log to 'not rendered as text; present in API JSON and data-category', or (b) map to a neutral public id at the presentation layer (present.py:74 and flags.js:65), leaving the internal id and fixtures alone (this avoids the re-record the qa note cites). Owner: backend.\",\n   \"acceptance_test\": \"Option (b): GET a sample case's flags and assert no category or data-* value contains 'patient'. Option (a): the card and decision note state the exposure.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Golden expected flag K3 still carries the cut label\",\n   \"evidence\": \"evals/golden/sample.expected.json:625: \\\"summary\\\": \\\"Causation rests on patient self-report, not a physician's causation opinion.\\\" (flag K3, subtype patient_reported_onset). Commit 4594bb7 edited only evals/golden/sample.export.expected.txt lines 58 and 69.\",\n   \"why_it_matters\": \"The golden JSON is the expected-output authority for the flags. Keeping the cut label there means the expected output still says it. I did not trace whether evals compare K3.summary to product output (evals/run.py:118 and :229 read summaries; the K3 path was not traced).\",\n   \"fix\": \"qa-owned (evals/**): change K3.summary to a neutral line that quotes the verbatim record, for example 'Causation language: record 9 verbatim \\\"Patient states ...\\\"'. Re-run evals.\",\n   \"acceptance_test\": \"grep -n -i 'self-report' evals/golden/sample.expected.json returns only the M10 must_not statement (line 990) or nothing; eval gates unchanged.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"'Reported onset' still names an implied reporter\",\n   \"evidence\": \"app/backend/flag_templates.py:126: \\\"patient_report\\\": lambda v: (\\\"Reported onset\\\", f\\\"Onset wording reported in {_at(v)}{_quote(v)}.\\\"). Sibling template at flag_templates.py:127: \\\"New-onset wording\\\".\",\n   \"why_it_matters\": \"It names no speaker, so it passes D-040. 'Reported' still implies someone reported it. 'Onset wording' would match the sibling template.\",\n   \"fix\": \"Optional: rename to 'Onset wording'. If renamed, update tests/unit/test_export_edge.py:70, tests/e2e/test_flags_panel.py, and the overlays in F1.\",\n   \"acceptance_test\": \"None required.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"e2e test name still says 'self_report'\",\n   \"evidence\": \"tests/e2e/test_flags_panel.py:19: def test_patient_self_report_label(page, sample_case): (body asserts \\\"Reported onset\\\").\",\n   \"why_it_matters\": \"Test-only naming. It is not user-facing, but a grep for 'self_report' finds it.\",\n   \"fix\": \"Rename to test_reported_onset_label.\",\n   \"acceptance_test\": \"pytest collects the renamed test; grep -rn 'self_report_label' tests/ returns nothing.\"}\n ],\n \"whats_right\": [\n  \"The export matches the golden after the cut: the record 9 quote is still verbatim ('Patient states symptoms began after the January collision.') in letter line 38 and notes lines 58 and 69, with no added physician or opinion wording.\",\n  \"The neutral template is in place and pinned: flag_templates.py:126 and tests/unit/test_export_edge.py:66-70 assert the title is 'Reported onset' and that no 'self-report' or 'patient self' appears in title or explanation.\",\n  \"Golden and curated checks are green at the commit: test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte, test_case_extras.py::test_default_export_is_byte_identical_to_golden_and_config_fills_the_citation, and make_curated --check (letter equal True, notes equal True).\"\n ],\n \"questions_for_chris\": [\n  \"Are the ?api=mock overlay (app/frontend/mock_flags.js) and /dev/panels.html part of the deployed Space (D-008/D-020)? If they are stripped from the public build, F1 drops to minor and the verdict becomes changes.\",\n  \"Keep the 'patient_report' id as internal only (F2 option a), or map it to a neutral public id at presentation (option b)?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:53:46.786Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-072-claims-adjuster.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:54:03.919Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-074-claims-adjuster.md",
 "content": "# T-074 review: claims-adjuster-reviewer (spec sync to D-040 golden)\n\n**Verdict: changes** (one major, no blocker). The two spec lines match the golden exactly and the spec-check tests pass. The spec still carries the cut requirement in R-FL-7, so the decision has not fully propagated.\n\nModel: claude-haiku-5-5, per the brief and the runtime.\n\n## What I checked\n\n- **Lines 280 and 291 (pass).** `diff <(sed -n 280p spec/REQUIREMENTS.md) <(sed -n 58p evals/golden/sample.export.expected.txt)` and the same for 291/69 both exit 0. Commit 83b4353 changes only those two lines (2 insertions, 2 deletions).\n- **Tests (pass).** The brief command passes: 62 live, 61 at HEAD archive. `test_eval_spec_check.py::test_real_spec_matches_golden` and the CLI spec-match test are included.\n- **Propagation of D-040 into the spec (fails).** See F1 through F3.\n\n## Findings\n\n- **F1 major.** R-FL-7 (`spec/REQUIREMENTS.md:71`) still requires `source_kind = \"patient_report\"` and the UI text \"Patient self-report\". Its acceptance cell says \"the label renders\". The product now does the opposite (`app/backend/flags.py:61`; `tests/unit/test_flags_pass.py:95` asserts every flag is `source_kind == \"record\"`). The spec and the tests contradict each other. Major, not blocker, because D-040 is recorded and the product matches it. If the gate reads R-FL-7 literally, the product fails it and this becomes a blocker until the spec is amended.\n- **F2 minor.** `spec/SAMPLE_CASE_TRUTHS.md:9` still labels the record 9 quote \"(9 — patient self-report, not a physician's causation opinion)\".\n- **F3 minor.** `spec/REQUIREMENTS.md:371`, deviation row 4, says the golden uses `patient_self_report`. Its evidence command `grep -n \"patient_self_report\\|summary+excerpt\" evals/golden/README.md` now returns no output, so the row is stale.\n- **F4 minor.** Contract and design docs still show the cut label: `memory/contracts/api.md:184-186` (example f_pat_9 with \"Patient self-report\" title and explanation), and `docs/UI_DESIGN_BRIEF.md:132` (a \"Patient self-report\" chip row). `api.md:212` already records D-040, so the example is inconsistent with its own note.\n\n```json\n{\"card\": \"T-074\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 83b4353 (spec/REQUIREMENTS.md lines 280, 291) checked against evals/golden/sample.export.expected.txt lines 58, 69; spec residue searched across spec/, memory/contracts/, docs/, evals/golden/; live tree /Users/arsis/zlayt-pm-project (dirty) and HEAD 83b4353 extracted with git archive\",\n \"exercised\": [\n  \"read personas/claims-adjuster.md in full; memory/ORCHESTRATOR_DECISIONS.md D-040 and its Source column; board show T-074 (notes 02:49:08Z to 02:49:12Z, commits: [])\",\n  \"git show --stat 83b4353; git show 83b4353 -- spec/REQUIREMENTS.md (2 lines changed, both suffix removals)\",\n  \"diff <(sed -n 280p spec/REQUIREMENTS.md) <(sed -n 58p evals/golden/sample.export.expected.txt) -> identical (exit 0); diff <(sed -n 291p spec/REQUIREMENTS.md) <(sed -n 69p evals/golden/sample.export.expected.txt) -> identical (exit 0)\",\n  \"sed -n 71p spec/REQUIREMENTS.md (R-FL-7 full text); sed -n 371p spec/REQUIREMENTS.md; sed -n 9p spec/SAMPLE_CASE_TRUTHS.md; grep -rn -i 'patient self|self-report|patient_report|self_report|chip' spec/ submission/ memory/ docs/\",\n  \"grep -n 'patient_self_report|summary+excerpt' evals/golden/README.md -> no output; grep -n 'Causation rests on patient self-report' evals/golden/sample.expected.json -> line 625 (K3)\",\n  \"read app/backend/flags.py:61 (source_kind record, D-040 comment) and tests/unit/test_flags_pass.py:95-100\",\n  \".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py -> 62 passed in 1.82s (live tree; includes an uncommitted T-070 test in test_eval_runner.py)\",\n  \"same three files at git archive 83b4353 (artifacts/review-evidence/T-072-T-074-83b4353, removed afterwards) -> 61 passed\",\n  \"board validate (read-only) -> 'ok (74 file(s))'\",\n  \"evals.run --check-spec not run (writes evals/reports, outside my write paths); the spec-match behaviour is covered by test_eval_spec_check.py\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"spec_lines_match_golden\": 5, \"decision_propagated_to_spec\": 2, \"tests_green_at_commit\": 5, \"spec_residue_cleanup\": 2},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"R-FL-7 still requires the cut 'Patient self-report' label; spec and product tests contradict\",\n   \"evidence\": \"spec/REQUIREMENTS.md:71: | R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = \\\"patient_report\\\"` and the UI text \\\"Patient self-report\\\". It is never presented as a physician's opinion. | Sample record 9 flag has `source_kind == \\\"patient_report\\\"` and the label renders. Golden `must_not` M10 passes. | UT + E2E |. Product: app/backend/flags.py:61 `\\\"source_kind\\\": \\\"record\\\",   # D-040: no code or model labels who is speaking`; tests/unit/test_flags_pass.py:95 test_no_flag_carries_a_self_report_chip asserts all source_kind == \\\"record\\\" for records 7 and 9. memory/ORCHESTRATOR_DECISIONS.md D-040 says the writer mirrors product decisions into spec/REQUIREMENTS.md; R-FL-7 was not amended.\",\n   \"why_it_matters\": \"The card's lines 280 and 291 are right, but the same D-040 cut leaves a written requirement that demands the label. An attorney or grader reading R-FL-7 would expect 'Patient self-report' in the UI and would find it absent. As written, the shipped product fails R-FL-7's acceptance cell. Major, not blocker, because the decision is recorded and the product matches it; the defect is the unamended spec. If the gate reads R-FL-7 literally, it is a blocker until amended.\",\n   \"fix\": \"Spec sync by writer or orchestrator: rewrite R-FL-7 to D-040. Suggested text: 'No speaker label. Every excerpt is a verbatim record excerpt with its source label (D-040). A flag never presents a patient statement as a physician's opinion.' Acceptance cell: 'Flags carry source_kind = record; no speaker label in the UI; test_no_flag_carries_a_self_report_chip passes.'\",\n   \"acceptance_test\": \"grep -n 'Patient self-report' spec/REQUIREMENTS.md returns no hits outside the decision log; R-FL-7's acceptance cell names test_no_flag_carries_a_self_report_chip; the spec-match test still passes.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Case truth sheet labels the record 9 quote 'patient self-report'\",\n   \"evidence\": \"spec/SAMPLE_CASE_TRUTHS.md:9: - **Causation-weakening language:** ... \\\"Patient states symptoms began after the January collision\\\" (9 — patient self-report, not a physician's causation opinion); ...\",\n   \"why_it_matters\": \"The truth sheet is the case's reference. It still records the speaker label that D-040 cut. Not rendered anywhere, but it is the source the team grades against.\",\n   \"fix\": \"Replace the parenthetical with the verbatim marker, e.g. (9 — verbatim 'Patient states ...').\",\n   \"acceptance_test\": \"grep -n -i 'self-report' spec/SAMPLE_CASE_TRUTHS.md returns nothing.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Deviation row 4 is stale: its evidence command now returns nothing\",\n   \"evidence\": \"spec/REQUIREMENTS.md:371: | 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` ... | `grep -n \\\"patient_self_report\\\\|summary+excerpt\\\" evals/golden/README.md` | orchestrator (D-entry) |. Run: the grep on evals/golden/README.md returns no output.\",\n   \"why_it_matters\": \"A deviation row that no longer reproduces misleads the next reviewer about what is still open.\",\n   \"fix\": \"Close the row with a pointer to D-040, or update it to the current golden state.\",\n   \"acceptance_test\": \"The row's stated evidence command either matches a current line or the row is marked closed.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Contract example and design brief still show the cut chip and title\",\n   \"evidence\": \"memory/contracts/api.md:184-186: { \\\"id\\\": \\\"f_pat_9\\\", \\\"type\\\": \\\"causation\\\", \\\"category\\\": \\\"patient_report\\\", \\\"source_kind\\\": \\\"record\\\", \\\"title\\\": \\\"Patient self-report\\\", \\\"explanation\\\": \\\"Patient self-report (not a physician's opinion) ...\\\"; api.md:212 already records D-040 ('No chip or label says who is speaking'). docs/UI_DESIGN_BRIEF.md:132: | `Patient self-report` | speech bubble | Patient self-report | `--text-muted` outline | only where code set `source_kind=patient_report` (T-061 narrows this) |.\",\n   \"why_it_matters\": \"Two docs a builder would follow still specify the cut label. api.md:184-186 contradicts its own line 212. The design brief still lists a chip the product no longer has.\",\n   \"fix\": \"Update the api.md example to the neutral title and explanation. Mark the design-brief row as cut under D-040. Owner: backend for api.md; orchestrator to route the design brief.\",\n   \"acceptance_test\": \"grep -rn 'Patient self-report' memory/contracts docs/ returns no hits outside decision history.\"}\n ],\n \"whats_right\": [\n  \"Lines 280 and 291 are byte-identical to golden lines 58 and 69 (diff exit 0 both), and commit 83b4353 changes only those two lines.\",\n  \"test_eval_spec_check.py and test_eval_runner.py pass at HEAD 83b4353 (61 passed across the three files) and on the live tree (62 passed).\",\n  \"The orchestrator's self-performed edit is disclosed in the card note (02:49:12Z), so an independent check was possible and this review re-derived the result.\"\n ],\n \"questions_for_chris\": [\n  \"Should R-FL-7 be rewritten by the writer (product note owner) or by the orchestrator (spec is orchestrator-synced per T-074 notes)? Outside my lens; I only need the amendment to exist before the M3 gate.\",\n  \"Board attribution (outside my lens, noted for the orchestrator): T-074 records the AC check under the architect role for an edit the orchestrator made, and commits is empty although 83b4353 exists.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:54:04.080Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-074-claims-adjuster.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:54:09.239Z

**tool call — Bash**
````
{
 "command": "grep -n \"\\\"new_onset\\\": lambda\" app/backend/flag_templates.py | cut -c1-80; grep -n \"\\\"missed_care\\\": lambda\" app/backend/flag_templates.py | cut -c1-60; echo \"== json parse + verdict rule\"; .venv/bin/python - <<'PY'\nimport json,re\nfor c in [\"T-072\",\"T-074\"]:\n    t=open(f\"/Users/arsis/zlayt-pm-project/reviews/{c}-claims-adjuster.md\").read()\n    blocks=re.findall(r\"```json\\n(.*?)```\", t, re.S)\n    assert len(blocks)==1, (c,len(blocks))\n    d=json.loads(blocks[0])\n    sev=[f[\"severity\"] for f in d[\"findings\"]]\n    rule=\"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\n    print(c, \"parsed ok; verdict\", d[\"verdict\"], \"rule says\", rule, \"match\" if rule==d[\"verdict\"] else \"MISMATCH\", sev, d[\"model\"], d[\"persona\"])\nPY\ngrep -n \"self-report\" tests/e2e/test_flags_panel.py | head -2; sed -n 19,21p tests/e2e/test_flags_panel.py | cut -c1-120",
 "description": "Verify two cited line numbers, parse both review JSON blocks, check verdict rule"
}
````

### User / tool · 2026-11-02T02:54:09.384Z

**tool result**
````
128:    "new_onset": lambda v: ("New-onset wording", f"New-onset wording in {_at
127:    "missed_care": lambda v: ("Missed or ended care", f"
== json parse + verdict rule
T-072 parsed ok; verdict fail rule says fail match ['blocker', 'minor', 'minor', 'nit', 'nit'] claude-haiku-5-5 claims-adjuster-reviewer
T-074 parsed ok; verdict changes rule says changes match ['major', 'minor', 'minor', 'minor'] claude-haiku-5-5 claims-adjuster-reviewer
def test_patient_self_report_label(page, sample_case):
    """R-FL-7: the record-9 causation flag shows 'Reported onset'."""
    open_case(page, sample_case); assert "Reported onset" in flags(page).inner_text()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:54:18.258Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_d040_label_cut_residue.md",
 "content": "---\nname: d040-label-cut-residue\ndescription: When a decision cuts a user-facing speaker label (D-040 self-report chip), residue survives in mock overlays, dev harness, spec requirement rows, golden JSON, contracts and design docs; grep all of them, and \"not rendered\" is not \"never shown\"\nmetadata:\n  type: project\n---\n\nT-072 / T-074 (2026-11-02) reviewed the D-040 cut of the \"Patient self-report\" label. The golden .txt and the export were clean. The residue sat elsewhere:\n- app/frontend/mock_flags.js:24 and app/frontend/dev/mock-data.js:748-749 still showed \"Patient self-report\". Reachable via `?api=mock` (api.js:2) and /dev/panels.html; the qa golden fix did not touch them.\n- spec/REQUIREMENTS.md:71 (R-FL-7) still demanded the label. The card synced only lines 280/291.\n- evals/golden/sample.expected.json:625 (flag K3 summary) still had the label.\n- memory/contracts/api.md:184-186, docs/UI_DESIGN_BRIEF.md:132, spec/SAMPLE_CASE_TRUTHS.md:9, spec row 371 (stale).\n- The internal category `patient_report` is \"not rendered as text\" (flags.js renders f.title; export labels key on type), but it IS in the public flag JSON (present.py:74) and as data-category (flags.js:65). A card that says \"never shown to users\" overstated it.\n\n**Why:** a decision that cuts a label is applied to the file the card names. Mock overlays, dev harnesses, requirement rows and golden JSON are separate files, so they survive a card that touches only the export and the golden .txt.\n\n**How to apply:** when a card claims a label is gone, grep app/ (including app/frontend/mock*.js and dev/), spec/, evals/golden/*.json, memory/contracts/, docs/ for the label text, and check `api.py` static mounts to see whether dev/ pages are served. For \"not shown to users\", check the API payload (present.py) and DOM attributes, not only rendered text. Related: [[feedback_reviews_write_once]], [[project_research_attack_map_gaps]].\n"
}
````

### User / tool · 2026-11-02T02:54:18.366Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_d040_label_cut_residue.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:54:19.979Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer && .venv/bin/python - <<'PY' 2>/dev/null || python3 - <<'PY2'\nPY\nPY2\necho \"placeholder\"; cd /Users/arsis/zlayt-pm-project && ls artifacts/review-evidence | grep -c \"T-072-T-074\" ",
 "description": "Confirm extracted evidence directory was removed"
}
````

### User / tool · 2026-11-02T02:54:20.096Z

**tool result (error)**
````
Exit code 1
placeholder
0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:54:23.665Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md",
 "old_string": "**How to apply:** before the first Write of a review file, grep every cited file:line and check it (use grep -n, not memory). Parse the\nJSON block and check the verdict rule. Do not work around the guard with a shell write; if a citation is off after writing, say so in\nthe reply to the orchestrator and give the corrected line numbers.",
 "new_string": "**How to apply:** before the first Write of a review file, grep every cited file:line and check it (use grep -n, not memory). Parse the\nJSON block and check the verdict rule. Do not work around the guard with a shell write; if a citation is off after writing, say so in\nthe reply to the orchestrator and give the corrected line numbers.\n\nT-072 r0 repeated the slip: I cited flag_templates.py:127 for \"New-onset wording\" (actual :128), and only noticed after the Write. Neighbour\nlines drift when you read a sed range by eye; grep -n the exact string for each citation, including the ones you think are obvious.\nRelated: [[project_d040_label_cut_residue]]."
}
````

### User / tool · 2026-11-02T02:54:23.767Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:54:25.653Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md",
 "old_string": "- [T-061 r4 separator list](project_t061_r4_separator_list.md) — D-037 chip still leaks via unlisted connectors (colon, dash, but, with, &, /, plus, per); sweep connectors, not spec examples",
 "new_string": "- [T-061 r4 separator list](project_t061_r4_separator_list.md) — D-037 chip still leaks via unlisted connectors (colon, dash, but, with, &, /, plus, per); sweep connectors, not spec examples\n- [D-040 label-cut residue](project_d040_label_cut_residue.md) — T-072/T-074: cut label survives in ?api=mock overlay, dev harness, R-FL-7, golden JSON, contracts; \"not rendered\" != \"never shown\""
}
````

### User / tool · 2026-11-02T02:54:25.793Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:54:28.859Z

T-072: **fail**, one blocker. The export, golden and template checks pass, but "Patient self-report" still appears in `app/frontend/mock_flags.js:24` and `app/frontend/dev/mock-data.js:748-749`. T-074: **changes**, one major. Spec lines 280 and 291 match golden 58 and 69 exactly, but R-FL-7 (`spec/REQUIREMENTS.md:71`) still requires the cut label.
Reviews: `/Users/arsis/zlayt-pm-project/reviews/T-072-claims-adjuster.md` and `/Users/arsis/zlayt-pm-project/reviews/T-074-claims-adjuster.md`. One citation in T-072 is off (`flag_templates.py:127` should be `:128`); the review is write-once, so I did not edit it.
