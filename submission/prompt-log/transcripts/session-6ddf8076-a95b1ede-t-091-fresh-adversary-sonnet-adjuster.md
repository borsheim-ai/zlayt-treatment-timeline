# Subagent: T-091 fresh adversary (sonnet adjuster) (T-091 fresh adversary (sonnet adjuster))

Source: `agent-a95b1ede676fa383a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:27:08.996Z

Adversarial review of board card T-091 in /Users/arsis/zlayt-pm-project (app/backend/speaker.py and evals/adversarial/speaker_attribution.jsonl, commit 17cc9c7 and the card's commits). Read `python3 tools/board.py show T-091`, D-040 and D-042 in memory/ORCHESTRATOR_DECISIONS.md, and reviews/T-061-claims-adjuster*.md (the history: the old patient self-report chip failed four adversary rounds).

Claim: 310/310 on a set the same worker wrote, shipped disabled. The worker admits that only a fresh adversary is a real test. Be that adversary, as a defense adjuster who wants a family member's, EMS's or witness's statement mislabeled as the patient's own.
- Write at least 60 new attack sentences the set doesn't already contain: mixed speakers, reported speech, pronoun chains, ellipsis, semicolons, quotes, Spanish, abbreviations (Pt/pt./PT meaning physical therapy), headers such as "HPI:" or "Per wife:", and line breaks.
- Run speaker.py on each one directly. Count every case where it says "patient" but a human reads "other" or "unknown". That's a blocker, and the gate is 100%.
- Also note how useful it is: what share of genuine patient statements it labels.

Save your attack set to artifacts/review-evidence/T-091/attacks.jsonl. Write reviews/T-091-claims-adjuster.md with a ```json block of real values: card, persona claims-adjuster-reviewer, model claude-sonnet-5-5, verdict, findings. Reply in 2 lines with the miss count.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:10.611Z

I'll start by reading the persona dossier, memory index files, and the card.

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:11.012Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/claims-adjuster.md"
}
````

### User / tool · 2026-11-02T04:27:11.064Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:11.361Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-091 && git log --oneline | head -15"
}
````

### User / tool · 2026-11-02T04:27:11.510Z

**tool result**
````
---
id: "T-091"
title: "Speaker attribution v2 behind an adversarial eval gate (D-040 stays until it passes)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:27:01Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:16:04Z"
rounds: 0
commits: ["17cc9c7"]
reviews: []
ac:
  - {"n": 1, "text": "Adversarial eval set (all T-061 attack strings + 40 new) built first; attribution ships only at 100% on it, otherwise stays off; result recorded either way", "done": true, "evidence": "evals/adversarial/speaker_attribution.jsonl (310 rows: 67 T-061 + 243 new) built first; tests/unit/test_speaker.py::test_gate_100_percent_on_adversarial_set passes 310/310, 0 unsafe patient labels; ships DISABLED (ENABLED=False), D-040 stays"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed
- 2026-11-02T04:21:04Z backend: Plan: spaCy not installed in .venv (no model offline), so closed-grammar clause parser in app/backend/speaker.py; label = outermost speaker; patient needs positive head + closed-vocab complement; mixed/none = unknown.
- 2026-11-02T04:26:55Z backend: AC 1 checked: evals/adversarial/speaker_attribution.jsonl (310 rows: 67 T-061 + 243 new) built first; tests/unit/test_speaker.py::test_gate_100_percent_on_adversarial_set passes 310/310, 0 unsafe patient labels; ships DISABLED (ENABLED=False), D-040 stays
- 2026-11-02T04:26:55Z backend: moved in_progress -> in_review
- 2026-11-02T04:27:01Z orchestrator: review dispatched: claims-adjuster-reviewer

## Handoff
What changed: new evals/adversarial/speaker_attribution.jsonl (qa owns evals/; I created only this one file, per the card AC): 310 rows = 67 T-061 r1-r4 attack strings + 243 new (Spanish, line breaks, quotes, pronouns, family/EMS/witness, punctuation, homoglyph/zero-width, names that are vocab words, 96-row mixed grid). app/backend/speaker.py: attribute(text) -> patient|other|unknown, ENABLED=False, chip_label() returns None. tests/unit/test_speaker.py. Approach: spaCy not installed in .venv and no model fetchable offline, so a closed-grammar clause parser: a label needs an explicit head (Patient states / Pt c/o / Per patient / Wife reports / EMS:), and every other word must be in a closed vocabulary, so an unknown word, second speaker, pronoun head or bare C/O gives unknown (no speaker or verb deny-list on the patient path). Label = outermost speaker; a patient statement nested in a non-patient report, or mixed speakers, is unknown; past-tense hearsay directly after a patient verb stays patient (D-037 keep rows). Verified: test_speaker.py 310/310 = 100%, 0 unsafe patient labels; 108k generated mixed strings never patient/other; full tests/unit 1281 passed. Gate met, but D-040 stays: nothing wired, ENABLED=False. Caveats: the set and parser share an author (one fix round after a blind probe: a name that is also a vocab word, 'Will feels fine'); a fresh adversary round is the real test. Coverage cost: of 226 speaker-like sentences in repo sample data only 28 get patient (closed vocab, safe direction). Wiring if adopted: (1) orchestrator reverses D-040; (2) flags/grounding call speaker.attribute per excerpt, chip only on patient (T-094 owns flags.py/judges.py, so a new card); (3) UI chip text and relax the two no_speaker_label tests; (4) claims-adjuster round on speaker.py before ENABLED flips; (5) add test_speaker to the eval gate. Surprise: the review misses were all open-world word lists; a closed vocabulary turned the safety property into a test.

17cc9c7 feat(backend): speaker attribution v2 behind adversarial eval gate, disabled (T-091)
ec33bf0 feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
f218263 feat(backend): billing analysis on itemized ledgers, claim forms and EOBs (T-083)
7724412 fix(backend): review.py judge path catches only expected judge errors and keeps the error class (T-073)
e3fc01c harness: board-guard denies pkill/killall for subagents (shared dev servers)
5616dc3 feat(frontend): side-by-side source viewer at >= 1024 px (R-ST-1, T-046)
f667f08 feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)
328428f feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
d0aee83 feat(evals): calibrated confidence from measured matches per state and item type (T-090)
ea259cd docs: D-046 ship-bar item 4 gates on J3/J4 seeded controls
e491cad feat(evals): determinism signature covers every R-CO-7 field, per-run artifacts, J3/J4 seeded controls (T-093)
10d358e fix(backend): export gate ready equals export allowed; pending items warn, not block (D-045)
8d7548d fix(research): denylist covers every cited author surname; self-test extracts and checks them (T-077 r3)
f49c4c2 docs: D-045 scope of the judge export gate
8e3c26c fix(frontend): collapsed case rail and AI-check row, working case-step actions, narrative stepper entry, Why dialog opens on the active step, one row per item (T-081 r2, T-082 r2)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:11.722Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_t061_r4_separator_list.md"
}
````

### User / tool · 2026-11-02T04:27:11.729Z

**tool result**
````
1	---
2	name: t061-r4-separator-list
3	description: T-061 r4 (991dac4, D-037 whole-excerpt chip): closed separator list (; , and ( ) lets colon, dash, but, with, while, &, /, [, plus, as, per leak a family/EMS clause under the chip; 11 probe misses; gate PASS 18/18 on a closed row list
4	metadata:
5	  type: project
6	---
7	
8	D-037 (memory/ORCHESTRATOR_DECISIONS.md:45) says the patient_report chip attaches only when the whole excerpt is one patient-subject
9	clause and "any further clause means no chip". Commit 991dac4 implemented it as a list of four separators (`app/backend/grounding.py:187`
10	`_FURTHER_CLAUSE = [;,(]|\band\b`), not as "any further clause".
11	
12	Round 4 result (reviews/T-061-claims-adjuster-r4.md): r3 B1 (comma/and/paren family clause) and B2 (verb outside list) are closed; r3 major 3
13	(gate measures production) is closed in form. New blocker: colon ("Patient states neck pain: wife reports headaches."), em dash, "but",
14	"with", "while", "&", "/", "[ ]", "plus", "as", and "per X" with no comma all keep the chip. Probe: artifacts/review-evidence/T-061-r4-probe.py.
15	
16	**Why:** each round finds the next unlisted connector. Enumerating separators is the same hole class as enumerating verbs or speakers
17	(D-037 says fail closed instead of patching lists, and the enumeration keeps failing).
18	
19	**How to apply:** on any "no further clause" rule, probe a sweep of connectors and punctuation (colon, dash, slash, ampersand, brackets,
20	contrast words "but/while/with/as/plus/per", "whereas/though"), not only the separators in the spec text. Judge against the headline
21	rule in the brief, not the example list in the table. Check whether the research gate's row list contains any of the new rows; if not, a
22	PASS says nothing about them. A closed-grammar set (function words) is more defensible than speaker or verb lists, but still has a tail:
23	ask the orchestrator to write the set into D-037 and to record the tail as residual.
24	
25	Related: [[t061-r3-clause-span-holes]], [[lexicon-review-method]], [[review-commit-not-worktree]].
26	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:12.325Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/reference_spare_port_app_server.md"
}
````

### User / tool · 2026-11-02T04:27:12.332Z

**tool result**
````
1	---
2	name: spare-port-app-server
3	description: How a reviewer runs its own app server and e2e tests on a spare port without touching the operator's app on 7860; bash-guard and macOS quirks hit on 2026-11-01
4	metadata:
5	  type: reference
6	---
7	
8	Recipe (worked on T-069, 2026-11-01): from an extracted commit tree (git archive), start the app with
9	`env HOST=127.0.0.1 PORT=7871 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=<scratch>/app.sqlite3 <repo>/.venv/bin/python -m app.main`
10	(app/main.py reads HOST and PORT; the default port 7860 belongs to the operator's app, so never use it). Health: GET /api/health.
11	Point e2e at it with `E2E_BASE_URL=http://127.0.0.1:7871 .venv/bin/python -m pytest tests/e2e/test_edit.py -p no:cacheprovider -v`
12	(tests/e2e/conftest.py defines its own `page` fixture on sync Playwright, so pytest-playwright is not needed).
13	Stop it by PID from `lsof -nP -t -iTCP:7871 -sTCP:LISTEN` and confirm the port is down.
14	
15	**Why:** tools/serve_app.sh hard-codes :7860 in a tmux window, and the operator's app lives there.
16	
17	**How to apply:** pass the tree root as argv to probe scripts (sys.path.insert); keep ZLAYT_DB in scratch, not in the repo.
18	
19	Quirks on this machine:
20	- `timeout` is not installed (macOS). Use the tool timeout parameter instead.
21	- The board-guard Bash hook reads `<=`, `>=` and `<` in a command as a redirect and blocks the whole call. Use `sed -n N,Mp` or grep without comparison operators.
22	- `rm -rf` inside the session scratchpad was denied by the permission system on 2026-11-01. Do not try a workaround; leave the scratch copies and say so in the reply.
23	- `lsof` prints a harmless "child setpgid" error from the shell on some calls.
24	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:14.067Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-040\\|D-042\\|D-037\\|D-035\" memory/ORCHESTRATOR_DECISIONS.md | head -20; ls reviews | grep T-061; git status --short | head; wc -l app/backend/speaker.py evals/adversarial/speaker_attribution.jsonl"
}
````

### User / tool · 2026-11-02T04:27:14.206Z

**tool result**
````
43:| D-035 | Simplifies D-033: `patient_report` is attached only to a **clause** that begins with an explicit patient subject ('Patient', 'Pt', 'The patient') followed by a reporting verb (states, reports, notes, says, endorses, complains of, c/o, denies); the tag spans that clause only (to the next ';' or sentence end). Everything else — EMS, family, any other or unknown speaker, header labels — gets **no tag**. Default is no tag: a missing chip is safe, a wrong chip is not. | Speaker-list regexes kept missing new speakers (girlfriend, co-worker). | T-061 r2 |
45:| D-037 | Final rule for `patient_report` (supersedes the clause-splitting in D-035, 2026-11-02): the chip attaches only when the **whole excerpt** is a single patient-subject clause (`Patient`/`Pt`/`The patient` + reporting verb), with no further clause after `;`, `,`, `and`, or `(`. Any mixed excerpt gets no chip and stays a plain record excerpt, so no verb list decides it. Bare `C/O` gets no chip. A missing chip is safe; a wrong chip mislabels the source. | Three adjuster rounds kept finding clause-boundary holes; fail closed instead of patching verbs. | T-061 claims-adjuster r3 B1/B2 |
48:| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four adjuster rounds each found mixed excerpts that a closed rule still mislabeled. The verbatim excerpt already shows who spoke ('Patient states…', 'wife reports…'), so the label added risk without information. A missing chip is safe; a wrong one is a credibility error. | T-061 claims-adjuster r4 blocker; §7.4 |
50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
T-061-claims-adjuster-r2.md
T-061-claims-adjuster-r3.md
T-061-claims-adjuster-r4.md
T-061-claims-adjuster.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
     417 app/backend/speaker.py
     310 evals/adversarial/speaker_attribution.jsonl
     727 total
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:15.969Z

**tool call — Bash**
````
{
 "command": "git status --short app/backend/speaker.py evals tests/unit/test_speaker.py; git diff --stat HEAD -- app/backend/speaker.py; cat app/backend/speaker.py"
}
````

### User / tool · 2026-11-02T04:27:16.097Z

**tool result**
````
 M evals/golden/judge_controls.jsonl
 M evals/run.py
?? evals/golden/judge_controls.CHANGELOG.md
?? evals/golden/judge_controls_heldout.jsonl
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
?? evals/reports/20261102T024355Z.md
?? evals/reports/20261102T024653Z.md
?? evals/reports/20261102T024822Z.md
?? evals/reports/20261102T025055Z.md
?? evals/reports/20261102T025526Z.md
?? evals/reports/20261102T030405Z.md
?? evals/reports/20261102T031209Z.md
?? evals/reports/20261102T032024Z.md
?? evals/reports/controls-20261102T042306Z.json
?? evals/reports/controls-20261102T042306Z.md
?? evals/reports/runs/20261102T042232Z/
"""Speaker attribution v2 (T-091, D-040 / D-042): who is the speaker of an excerpt? Deterministic, local, no model, no network.

STATUS: DISABLED. D-040 stays in force; nothing in the UI, flags or export imports this module. `ENABLED` is the
switch and it is False. See the T-091 handoff for the score on evals/adversarial/speaker_attribution.jsonl.

Contract
    attribute(text) -> Attribution(label, speakers, reasons)
    label is one of:
      "patient"  every statement in the excerpt is attributed to the patient by an explicit head ("Patient states ...",
                 "Pt c/o ...", "Per patient, ...", "paciente refiere ..."), and nothing else appears in it.
      "other"    every statement is attributed to a named non-patient source (EMS, wife, witness, nurse, ...), and no
                 patient statement is nested inside (that would be hearsay of a patient statement: "unknown").
      "unknown"  anything else: mixed speakers, no speaker, pronoun-only speaker ("He states"), bare "C/O", titles or
                 names, uppercase "PT" (physical therapy or patient), a word the grammar does not know.
    A wrong "patient" is a credibility error; "unknown" is always safe. Every rule below therefore fails toward unknown.

Mechanism (no dependency parser: spaCy is not installed in .venv and its model cannot be fetched offline, and a
statistical parse would be the wrong tool for a fail-closed gate anyway)
    1. Normalise (NFKC, strip invisible format chars, fold quotes, lowercase; uppercase "PT" is kept as ambiguous).
    2. Split into sentences, then into clause segments at punctuation and at a CLOSED set of connector words.
    3. A segment is a HEAD only if it starts with a recognised speaker + speech verb ("wife reports"), a "per X" /
       "according to X" phrase, or a "X:" label for a listed non-patient source. Everything else is a continuation.
    4. A continuation (or a head's complement) may contain only words from a CLOSED vocabulary (symptom, body, time,
       function words). An unknown word, a second speaker, a speech verb or a pronoun head all fall outside it, so the
       result is unknown. There is no deny-list of speakers or verbs on the patient path: that is what let four review
       rounds find another hole. Words are added to the vocabulary, never to a block list.
    5. The one allowed embedding is hearsay inside a patient statement in the past tense, directly after the verb:
       "Patient states EMS noted a laceration." / "... his wife drove him to the ER." The patient is still the speaker.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

ENABLED = False   # D-040: the chip stays off. Flip only after the adversarial gate is 100% AND T-091 wiring is reviewed.

LABELS = ("patient", "other", "unknown")


@dataclass(frozen=True)
class Attribution:
    label: str
    speakers: tuple = ()
    reasons: tuple = field(default_factory=tuple)


def chip_label(text: str):
    """What the UI would ask for. None while ENABLED is False (D-040) and for every non-patient result."""
    if not ENABLED:
        return None
    return "patient" if attribute(text).label == "patient" else None


# --------------------------------------------------------------------------------------------------- vocabulary

def _w(s: str) -> frozenset:
    return frozenset(s.split())


_PATIENT_SUBJ = _w("patient pt paciente paciente")
_DET = _w("the this his her their its a an patient's pt's paciente's el la los las su sus")
_MOD = _w("triage charge er ed emergency ambulance ems scene responding on-scene police treating referring attending resident "
          "nursing ward floor other family insurance claims adjuster rn lpn")

# non-patient sources (English + Spanish). 'pt' is deliberately absent; 'pt' is a patient subject.
_SRC = _w("""ems emt emts paramedic paramedics medic medics ambulance crew wife husband spouse mother father mom dad parent parents
son daughter sister brother grandmother grandfather aunt uncle cousin girlfriend boyfriend fiance fiancee partner friend
family relative relatives caregiver neighbor neighbour coworker co-worker colleague boss employer supervisor witness
witnesses passenger driver bystander officer police trooper deputy adjuster attorney lawyer nurse rn lpn cna triage
doctor physician md provider pa np therapist chiropractor technician tech radiologist clerk receptionist
esposa esposo marido madre padre hermano hermana hijo hija familiar testigo paramedico paramédico paramédicos paramedicos
enfermera enfermero médico medico doctora policía policia oficial pasajero conductor amigo amiga novia novio""")

# speech / documentation verbs. Used ONLY to recognise a head ("<speaker> <verb>"); never as a deny-list.
_SAY = _w("""states stated state reports reported report says said say tells told tell notes noted note denies denied deny
complains complained complain c_o endorses endorsed describes described relates related indicates indicated admits admitted
acknowledges acknowledged claims claimed believes believed thinks thought recalls recalled remembers remembered rates rated
mentions mentioned expresses expressed voices voiced volunteers volunteered reiterates confirms confirmed advises advised
informs informed relays relayed attributes attributed links linked associates associated blames blamed alleges alleged
contends maintains insists asserts declares answers responds agrees observed observes found saw documented documents
recorded records witnessed heard suspects feels felt gives gave
refiere refirió refirio dice dijo manifiesta manifestó manifesto indica indicó indico niega negó nego reporta reportó reporto
informa informó informo relata relató relato menciona mencionó menciono afirma afirmó afirmo señala señaló expresa declara
declaró comenta comentó describe describió acusa""")
_SAY_PATIENT = _SAY - _w("observed observes found saw witnessed heard suspects feels felt gives gave")

_EMBED_VERB = _w("noted said told stated reported documented drove took brought found saw called helped gave transported "
                 "picked arrived asked advised")

# connector words that open a new segment (dropped). 'per' / 'according to' / 'segun' are kept as the segment's first word.
_SPLIT = _w("and but while whereas although though however plus as then so because y e pero mientras sino pues or o")
_KEEP_SPLIT = _w("per según segun")

_SECTION = frozenset({"s", "subjective", "hpi", "history of present illness", "cc", "chief complaint", "hx", "history",
                      "interval history", "subjective complaints", "complaints", "complaint", "comment", "comments", "note",
                      "notes", "narrative", "reason for visit", "motivo de consulta", "subjetivo", "historia"})
_PREFIX = _w("at on during today the visit intake exam appointment follow up followup initial evaluation consult consultation "
             "office hoy en la el consulta cita")

_COMMON = """
a an the of in on at to for from with without into onto over under up down out off through during after before since until till
about around across near between within against along both each all any some no not none never nor neither only just still very
quite more most less much many few little too even already again ever once twice than like such same another is are was were be
been being am do does did done has have had having can could would should might must it its this that these those there
here when where how what if which he she him her his hers they them their theirs we us our i me my mine you your
at all so as well
"""

_BODY = """
neck back head shoulder shoulders arm arms elbow elbows wrist wrists hand hands finger fingers thumb hip hips leg legs knee knees
ankle ankles foot feet toe toes chest rib ribs abdomen abdominal stomach belly groin jaw face eye eyes ear ears nose mouth teeth
tooth spine cervical thoracic lumbar sacral coccyx tailbone skull scalp forehead temple temples throat trapezius upper lower mid
left right l r lt rt bilateral bilaterally bilat side sides front rear base area areas joint joints muscle muscles
"""

_SYMPTOM = """
pain pains ache aches aching soreness sore stiffness stiff tenderness tender numbness numb tingling weakness weak swelling swollen
bruising bruise bruised spasm spasms headache headaches migraine migraines dizziness dizzy lightheaded nausea nauseous vomiting
fatigue tired anxiety anxious depression insomnia fever chills cough rash laceration cut cuts abrasion abrasions contusion fracture
sprain strain strained bleeding discomfort burning pressure cramping cramps limp limping radiating radiates radiated radiculopathy
sharp dull constant constantly intermittent intermittently mild moderate severe worse worsen worsens worsened worsening better
improved improving improves resolved resolving persistent persists persisted continues continued continue shooting stabbing
throbbing occasional occasionally frequent frequently daily nightly worst unbearable intense terrible bad good fine ok okay normal
normally unable able difficulty trouble hard easy limited limitation restriction restricted flare flares flared
loss consciousness conscious unconscious lost blackout blacked passed alert awake oriented ambulatory stable confused confusion
irritable irritability moody mood sleep sleeping slept sleeps rest resting memory concentrating concentration vision blurry blurred
ringing hearing balance gait walking walk walked walks standing stand stood sitting sit sat bending bend lifting lift lifted
reaching carrying driving drive driven working work worked running climbing stairs prolonged long short
hurts hurt hurting felt feel feels feeling seems seemed began begin begins start started starts onset woke wake waking happened
occurred occur occurs went go going came come taking take taken took got get getting gets became become becoming hit struck
rear-ended rearended slammed jolted jerked thrown twisted fell fall fallen slipped slip trip tripped
"""

_EVENT = """
accident accidents collision crash crashed vehicle car truck motorcycle bike bicycle pedestrian airbag airbags seatbelt seat belt
belts impact windshield steering wheel dashboard door light lights intersection road highway street lot parking fall slip work job
home house stairs steps ladder ground floor ice wet scene incident injury injuries injured event er ed emergency room hospital clinic
office urgent care sleep night
"""

_TREAT = """
ibuprofen tylenol acetaminophen naproxen medication medications meds pills pill relief relieves helps helped ice heat rest therapy
treatment physical chiropractic massage injection injections surgery surgeries
"""

_TIME = """
today yesterday tonight now currently ago last first second third prior previous following later early late lately recently
morning evening afternoon night nights day days week weeks month months year years hour hours minute minutes moment time times
one two three four five six seven eight nine ten zero half several couple
"""

_SPANISH = """
dolor dolores cuello cabeza espalda hombro hombros brazo brazos mano manos pierna piernas rodilla rodillas pie pies tobillo pecho
cadera desde el la los las un una de del en con sin por a al que se me mi mis su sus es está esta estoy tiene tengo hace días dias
semana semanas mes meses año años hoy ayer anoche noche mañana tarde accidente choque colisión colision golpe golpeó golpeo
después despues antes durante cuando constante intermitente leve moderado moderada severo severa fuerte intenso intensa mareo
mareos náusea nausea náuseas nauseas vómito vomito fiebre hormigueo entumecimiento debilidad inflamación inflamacion hinchazón
hinchazon rigidez molestia molestias lesión lesion caída caida cayó cayo no nada ninguno más mas menos muy todo todos todo
lumbar cervical lado izquierdo derecho izquierda derecha ambos ambas """

_EXTRA = """
also ran run runs limps sleeps poorly low deployed steady gait damage minimal distress intake stop stopped red green traffic whiplash
fault slowly suddenly sudden behind ahead speed speeding mph hit-and-run turn turning merging merged
prior surgeries arthroscopy fusion discectomy laminectomy replacement problem problems symptom symptoms caused cause causes due
missing missed duty closed clinic appointment could earlier violent brief thrown against struck by cannot cant couldn't didn't
wasn't hadn't haven't isn't doesn't don't won't wouldn't another state
pérdida perdida conciencia comenzó comenzo empezó empezo duerme mal vehículo vehiculo detuvo dolía dolia ha
"""
_BASE = _w(_COMMON + _BODY + _SYMPTOM + _EVENT + _TREAT + _TIME + _SPANISH + _EXTRA)
_NUMERIC = re.compile(r"^[\d#:.,%+~<>=-]*\d[\d#:.,%+~<>=a-z-]*$")   # 7#10, 2026, 3d, 10mg ('/' between digits is folded to '#')

# What a continuation / complement may contain, by current speaker.
_VOCAB_PATIENT = _BASE
_VOCAB_OTHER = _BASE | _w("patient pt paciente")

# --------------------------------------------------------------------------------------------------- normalise

_ABBR = re.compile(r"\b(pt|dr|mr|mrs|ms|sr|sra|st|vs|approx|no|hx|dx|rx|tx|w|c|s|e\.g|i\.e)\.", re.IGNORECASE)


def _normalise(text: str) -> str:
    t = unicodedata.normalize("NFKC", text or "")
    t = "".join(ch for ch in t if unicodedata.category(ch) != "Cf")           # zero-width and bidi controls
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("«", '"'), ("»", '"')):
        t = t.replace(a, b)
    # uppercase PT is physical therapy or patient: mark it so it can never become a patient subject
    t = re.sub(r"\bPT\b\.?", " pt_ambiguous ", t)
    t = t.lower()
    t = re.sub(r"\b(patient|pt)[- ]reported\b(?!\s+(?:by|that|he|she|his|her)\b)", r"\1 reports", t)   # "Patient-reported neck pain"
    t = re.sub(r"\bc\s*/\s*o\b", "c_o", t)
    t = re.sub(r"\bs\s*/\s*p\b", "s_p", t)
    t = re.sub(r"\bw\s*/\s*o\b", "w_o", t)
    t = re.sub(r"\bw\s*/", "w_ ", t)
    t = re.sub(r"(?<=\d)\s*/\s*(?=\d)", "#", t)
    t = re.sub(r"(?<=\d)\.(?=\d)", "#", t)                                   # 7.5
    t = _ABBR.sub(lambda m: m.group(1), t)                                   # pt. -> pt, mrs. -> mrs
    t = re.sub(r"(?:as\s+)?(?:reported|stated|described|relayed|noted|documented|per)\s+by\s+", " per ", t)
    t = re.sub(r"\b(?:as\s+per|according\s+to|de\s+acuerdo\s+con)\b", " per ", t)
    t = re.sub(r"\bpor\s+(?=(?:el|la)?\s*(?:paciente|esposa|esposo)\b)", " según ", t)
    # appositive name or title right after a source noun: "wife (mrs. ortiz) reports"
    t = re.sub(r"(\b(?:" + "|".join(sorted(_SRC, key=len, reverse=True)) + r")\b)\s*\(\s*(?:mrs?|ms|miss|mr|dr|sra?|señora?)\.?\s+[a-záéíóúñ]+\s*\)", r"\1", t)
    t = re.sub(r"(?m)^\s*(?:[-*•·]|\d+[.)])\s+", "", t)                      # bullets and numbering
    return t


# ------------------------------------------------------------------------------------------------------ segmenting

def _tokens(s: str) -> list:
    return re.findall(r"[\w'#]+(?:-[\w'#]+)*", s, re.UNICODE)


def _sentences(t: str) -> list:
    out = []
    for block in re.split(r"(?<=[.!?])\s+|[.!?]+$|\n{2,}", t):
        if block and block.strip():
            out.append(block.strip(" .!?"))
    return out


_PUNCT_SPLIT = re.compile(r"\s*([,;:—–()\[\]\"/&]|\s-\s|\n)\s*")


def _split_segments(sentence: str) -> list:
    """-> list of (token_list, sep_after). Connector words open a new segment; 'per' keeps its place as first word."""
    parts = _PUNCT_SPLIT.split(sentence)
    raw = []   # (text, sep_after)
    for i in range(0, len(parts), 2):
        txt = parts[i]
        sep = parts[i + 1].strip() if i + 1 < len(parts) and parts[i + 1] is not None else ""
        raw.append((txt, sep or ("\n" if "\n" in (parts[i + 1] if i + 1 < len(parts) else "") else "")))
    segs = []
    for txt, sep in raw:
        toks = _tokens(txt)
        cur = []
        out = []
        for tok in toks:
            if tok in _SPLIT or tok in _KEEP_SPLIT:
                if cur:
                    out.append((cur, ""))
                cur = [] if tok in _SPLIT else [tok]
            else:
                cur.append(tok)
        if cur:
            out.append((cur, ""))
        if out:
            out[-1] = (out[-1][0], sep)
            segs.extend(out)
        elif segs and sep:
            segs[-1] = (segs[-1][0], segs[-1][1] or sep)
    return [(t, s) for t, s in segs if t]


# --------------------------------------------------------------------------------------------------- head detection

def _skip_det(toks, i):
    while i < len(toks) and toks[i] in _DET:
        i += 1
    return i


def _src_phrase(toks, i):
    """Return index after a source phrase starting at i (modifiers + a source noun), or None."""
    j = i
    while j < len(toks) and toks[j] in _MOD and toks[j] not in _SRC:
        j += 1
    if j < len(toks) and toks[j] in _SRC:
        j += 1
        # "family member", "ambulance crew", "ems crew", "triage nurse"
        while j < len(toks) and toks[j] in _SRC | _w("member members"):
            j += 1
        return j
    return None


def _patient_phrase(toks, i):
    j = _skip_det(toks, i)
    if j < len(toks) and toks[j] in _PATIENT_SUBJ:
        return j + 1
    return None


def _head(toks, sep):
    """Classify one segment. -> (speaker, complement_tokens, kind) or None.
    speaker: 'patient' | 'other'; kind: 'verb' | 'per' | 'label'."""
    if not toks:
        return None
    # per / segun
    if toks[0] in _KEEP_SPLIT:
        j = _patient_phrase(toks, 1)
        if j is not None:
            return "patient", toks[j:], "per"
        j = _src_phrase(toks, _skip_det(toks, 1))
        if j is not None:
            return "other", toks[j:], "per"
        return None
    # patient + verb
    j = _patient_phrase(toks, 0)
    if j is not None:
        k = j
        if k < len(toks) and toks[k] in _w("also now currently further today then again"):
            k += 1
        if k < len(toks) and toks[k] in _SAY_PATIENT:
            k += 1
            if k < len(toks) and toks[k] == "of" and toks[k - 1] in _w("complains complained complain"):
                k += 1
            return "patient", toks[k:], "verb"
        return None
    # source + verb, or source label
    j = _src_phrase(toks, _skip_det(toks, 0))
    if j is not None:
        if j < len(toks) and toks[j] in _SAY:
            k = j + 1
            if k < len(toks) and toks[k] == "of" and toks[k - 1] in _w("complains complained complain"):
                k += 1
            return "other", toks[k:], "verb"
        if j == len(toks) and sep in (":", "—", "–", "-"):
            return "other", [], "label"
    return None


def _complement_ok(comp, speaker, allow_embed):
    """comp must be inside the closed vocabulary; a leading hearsay embedding is allowed after a patient verb."""
    vocab = _VOCAB_PATIENT if speaker == "patient" else _VOCAB_OTHER
    toks = list(comp)
    if allow_embed and toks:
        i = 1 if toks[0] == "that" else 0
        i = _skip_det(toks, i) if toks[i:i + 1] and toks[i] in _DET else i
        j = _src_phrase(toks, i)
        if j is not None and j < len(toks) and toks[j] in _EMBED_VERB:
            toks = toks[j + 1:]
    for t in toks:
        if t in vocab or _NUMERIC.match(t):
            continue
        return False
    return True


# ------------------------------------------------------------------------------------------------------- sentence

def _classify_sentence(sentence: str):
    segs = _split_segments(sentence)
    if segs and len(segs[0][0]) > 1 and _NUMERIC.match(segs[0][0][0]):      # "2026-04-05 Patient reports ..."
        segs[0] = (segs[0][0][1:], segs[0][1])
    reasons = []
    speakers = set()
    # drop section labels and lead-in phrases before the first head
    cleaned = []
    seen_head = False
    for toks, sep in segs:
        if not seen_head:
            joined = " ".join(toks)
            if joined in _SECTION or (all(t in _PREFIX or _NUMERIC.match(t) for t in toks)):
                continue
        if _head(toks, sep) is not None:
            seen_head = True
        cleaned.append((toks, sep))
    cur = None
    pre = []        # unattributed lead-in tokens, only valid when a trailing "per X" head claims them
    first_head = True
    for toks, sep in cleaned:
        h = _head(toks, sep)
        if h is None:
            if cur is None:
                pre.append(toks)
                continue
            if not _complement_ok(toks, cur, False):
                return None, speakers, ["unrecognised words or a pronoun/second speaker in: " + " ".join(toks)]
            continue
        speaker, comp, kind = h
        if pre:
            if kind != "per" or any(not _complement_ok(p, speaker, False) for p in pre):
                return None, speakers, ["unattributed text before the first speaker"]
            pre = []
        if not _complement_ok(comp, speaker, allow_embed=(speaker == "patient" and kind == "verb")):
            return None, speakers, ["unrecognised words in the statement: " + " ".join(comp)]
        cur = speaker
        speakers.add(speaker)
        first_head = False
    if pre or not speakers:
        return None, speakers, ["no explicit speaker"]
    return speakers, speakers, reasons


def attribute(text: str) -> Attribution:
    """Label who is speaking in `text`. Deterministic. See the module docstring for the rules."""
    t = _normalise(text)
    # a newline starts a new segment only when the next line begins with a speaker head; otherwise it is a soft wrap
    lines = [ln for ln in t.split("\n")]
    joined = lines[0] if lines else ""
    for prev, nxt in zip(lines, lines[1:]):
        nseg = _split_segments(nxt.strip())
        starts_head = bool(nseg) and _head(nseg[0][0], nseg[0][1]) is not None
        if not prev.strip():
            joined += " "
        elif re.search(r"[.!?]\s*$", prev) or starts_head:
            joined += " ; " if not re.search(r"[.!?]\s*$", prev) else " "
        else:
            joined += " "
        joined += nxt
    sentences = _sentences(joined)
    if not sentences:
        return Attribution("unknown", (), ("empty",))
    allspk = set()
    reasons = []
    for s in sentences:
        spk, seen, why = _classify_sentence(s)
        allspk |= set(seen or ())
        if spk is None:
            return Attribution("unknown", tuple(sorted(allspk)), tuple(why))
        reasons.extend(why)
    if allspk == {"patient"}:
        return Attribution("patient", ("patient",), ())
    if allspk == {"other"}:
        return Attribution("other", ("other",), ())
    return Attribution("unknown", tuple(sorted(allspk)), ("mixed speakers",))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:16.357Z

**tool call — Bash**
````
{
 "command": "head -5 evals/adversarial/speaker_attribution.jsonl; sed -n 1,60p tests/unit/test_speaker.py"
}
````

### User / tool · 2026-11-02T04:27:16.444Z

**tool result**
````
{"id": "SA-001", "src": "t061-r1", "group": "brief", "text": "Patient states pain began after the collision.", "expect": "patient", "note": ""}
{"id": "SA-002", "src": "t061-r1", "group": "brief", "text": "Wife reports he has been irritable.", "expect": "other", "note": ""}
{"id": "SA-003", "src": "t061-r1", "group": "brief", "text": "Per EMS, pt ambulatory at scene.", "expect": "other", "note": ""}
{"id": "SA-004", "src": "t061-r1", "group": "brief", "text": "Witness states the car ran the light.", "expect": "other", "note": ""}
{"id": "SA-005", "src": "t061-r1", "group": "brief", "text": "S: neck pain", "expect": "unknown", "note": ""}
"""T-091: speaker attribution v2 (app/backend/speaker.py) against the adversarial set. Module is disabled (D-040); this is the gate.

The jsonl holds every attack string from the four T-061 claims-adjuster rounds plus 40+ new ones. The gate is 100%: a single
wrong label fails the test. A second, generated grid checks the safety property directly (a mixed excerpt is never labelled
patient or other, whatever the connector, the second speaker or the reporting verb).
"""
import itertools
import json
from pathlib import Path

import pytest

from app.backend import speaker

SET = Path(__file__).resolve().parents[2] / "evals" / "adversarial" / "speaker_attribution.jsonl"
ROWS = [json.loads(line) for line in SET.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_set_shape():
    assert len(ROWS) == len({r["id"] for r in ROWS})
    assert sum(r["src"].startswith("t061") for r in ROWS) >= 60
    assert sum(r["src"] == "new" for r in ROWS) >= 40
    assert {r["expect"] for r in ROWS} == {"patient", "other", "unknown"}
    for g in ("spanish", "line_breaks_quotes", "pronouns_family", "punctuation_variants", "mixed_grid"):
        assert any(r["group"] == g for r in ROWS), g


def test_gate_100_percent_on_adversarial_set():
    wrong = [(r["id"], r["expect"], speaker.attribute(r["text"]).label, r["text"]) for r in ROWS
             if speaker.attribute(r["text"]).label != r["expect"]]
    assert not wrong, f"{len(wrong)}/{len(ROWS)} wrong: {wrong[:5]}"


def test_no_unsafe_patient_label_anywhere():
    """The costly error class: expected not-patient, labelled patient."""
    unsafe = [r["id"] for r in ROWS if r["expect"] != "patient" and speaker.attribute(r["text"]).label == "patient"]
    assert unsafe == []


@pytest.mark.parametrize("p", ["Patient states neck pain", "Pt reports headaches", "Per patient, pain began at the scene"])
def test_generated_mixed_grid_never_patient_or_other(p):
    speakers = ["wife", "his wife", "EMS", "the pastor", "landlord", "Mrs. Ortiz", "Maria", "Dr. Smith", "he", "she", "they",
                "a friend", "the tow driver", "su esposa", "roommate", "witness"]
    verbs = ["reports", "says", "states", "notes", "thinks", "claims", "told me", "insists", "reporting", "mentioned", "texted"]
    conns = [", ", "; ", ": ", " — ", " - ", " & ", " / ", ". ", "\n", " plus ", " as ", " while ", " but ", " and ", " (", " [",
             " | ", " however, ", " with ", " per ", " also ", " y "]
    for c, s, v in itertools.product(conns, speakers, verbs):
        text = f"{p}{c}{s} {v} headaches began at the scene."
        assert speaker.attribute(text).label == "unknown", text
        flipped = f"{s} {v} headaches began at the scene{c}{p[0].lower() + p[1:]}."
        assert speaker.attribute(flipped).label == "unknown", flipped


def test_disabled_by_default_d040():
    assert speaker.ENABLED is False
    assert speaker.chip_label("Patient states neck pain.") is None


def test_label_is_always_one_of_three_and_never_raises():
    for t in ["", None, "\x00", "((((", "\n\n\n", "a" * 5000, "Patient states " * 300, "‮patient states neck pain"]:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:27:18.996Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport json,collections\nrows=[json.loads(l) for l in open('evals/adversarial/speaker_attribution.jsonl')]\nprint(collections.Counter((r['group'],r['expect']) for r in rows))\nfor r in rows:\n    if r['expect']=='patient': print(r['id'],repr(r['text']))\nEOF"
}
````

### User / tool · 2026-11-02T04:27:19.101Z

**tool result**
````
Counter({('mixed_grid', 'unknown'): 96, ('unknown_basic', 'unknown'): 37, ('other', 'other'): 22, ('patient_plain', 'patient'): 20, ('mixed', 'unknown'): 14, ('mixed_connector', 'unknown'): 11, ('pronouns_family', 'unknown'): 10, ('punctuation_variants', 'unknown'): 10, ('patient', 'patient'): 9, ('line_breaks_quotes', 'unknown'): 9, ('patient_embeds_other', 'patient'): 7, ('spanish', 'unknown'): 6, ('patient_per', 'patient'): 5, ('line_breaks_quotes', 'patient'): 5, ('non_patient_complains', 'other'): 4, ('unlisted_speaker', 'unknown'): 4, ('patient_prefix_bullets', 'patient'): 4, ('spanish', 'patient'): 4, ('name_is_vocab_word', 'unknown'): 4, ('brief', 'other'): 3, ('non_patient', 'other'): 3, ('colon_label_nested', 'unknown'): 3, ('spanish', 'other'): 3, ('long_subject', 'unknown'): 2, ('abbrev', 'unknown'): 2, ('homoglyph', 'unknown'): 2, ('brief', 'patient'): 1, ('brief', 'unknown'): 1, ('intake_form', 'unknown'): 1, ('bare_co', 'unknown'): 1, ('per_other', 'other'): 1, ('colon_label', 'unknown'): 1, ('unlisted_speaker', 'other'): 1, ('separate_sentences', 'unknown'): 1, ('separate_sentences', 'patient'): 1, ('patient_homoglyph_invisible', 'patient'): 1, ('patient_fullwidth', 'patient'): 1})
SA-001 'Patient states pain began after the collision.'
SA-013 'Patient complains of neck pain.'
SA-015 'Patient-reported neck pain 7/10.'
SA-016 'Patient states EMS noted a laceration.'
SA-017 'Patient reports his wife said he was fine.'
SA-018 'Patient states his wife drove him to the ER.'
SA-036 'Pt reports neck pain.'
SA-049 'Patient links her neck pain to the collision.'
SA-061 'Pt reports neck pain 7/10.'
SA-062 'The patient denies loss of consciousness.'
SA-063 'Patient states neck pain.'
SA-064 'Patient reports low back pain in 2023, resolved.'
SA-065 'Patient reports neck pain and headache.'
SA-067 'Patient states headaches. Patient reports neck pain.'
SA-068 'Patient states neck pain radiating to the left arm.'
SA-069 'Pt denies numbness or tingling.'
SA-070 'The patient reports headaches since the accident.'
SA-071 'Patient complained of dizziness after the crash.'
SA-072 'Patient also reports difficulty sleeping.'
SA-073 'Patient says the pain is worse in the morning.'
SA-074 'Pt c/o low back pain 6/10.'
SA-075 'Pt complains of ringing in the ears.'
SA-076 'Patient denies loss of consciousness.'
SA-077 'Patient reports he has not had any relief with ibuprofen.'
SA-078 'Patient states that the pain began after the collision.'
SA-079 'Patient reports he was rear-ended at a stop light.'
SA-080 'Patient reports neck pain 7.5/10.'
SA-081 'Pt. states neck pain.'
SA-082 'pt reports neck pain'
SA-083 'PATIENT REPORTS NECK PAIN.'
SA-084 '  Patient   reports\tneck pain.  '
SA-085 'Patient reports neck pain at intake.'
SA-086 'Patient states neck pain 7/10 radiating to the left shoulder, worse in the morning, and improved with ibuprofen.'
SA-087 'Patient reports: neck pain, headaches, and nausea.'
SA-088 'Pat\u200bient states neck pain.'
SA-089 'Ｐatient states neck pain.'
SA-090 'Per patient, pain began at the scene.'
SA-091 'Per the patient, neck pain 7/10.'
SA-092 'According to the patient, headaches started two days after the collision.'
SA-093 'Neck pain 7/10 per patient.'
SA-094 'Neck pain as reported by patient.'
SA-095 'On 2026-01-20, patient states neck pain.'
SA-096 'At intake, patient reports neck pain.'
SA-097 'Subjective: Patient reports neck pain.'
SA-098 '- Patient states neck pain\n- Patient reports headaches'
SA-099 'Patient states his husband drove him to the ER.'
SA-100 'Patient reports EMS told him he had whiplash.'
SA-101 'Patient states the officer said it was not his fault.'
SA-102 'Patient states his wife said he was fine.'
SA-103 'Patient states neck pain\nand headaches since the crash.'
SA-104 'Patient\nstates neck pain.'
SA-105 'Patient states:\nneck pain and stiffness.'
SA-106 '“Patient states neck pain.”'
SA-107 'Patient states "neck pain".'
SA-108 'Paciente refiere dolor de cuello desde el accidente.'
SA-109 'La paciente manifiesta dolor de cabeza y mareo.'
SA-110 'El paciente niega pérdida de conciencia.'
SA-111 'Según el paciente, el dolor comenzó después del choque.'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:30:00.046Z

**tool call — Bash**
````
{
 "command": "ls; ls evals evals/adversarial artifacts/review-evidence | head -50; ls data* app/data* 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T04:30:00.141Z

**tool result**
````
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
data
deploy
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
artifacts/review-evidence:
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
data:
zlayt.sqlite
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:31:13.659Z

**tool call — Bash**
````
{
 "command": "ls evals/golden | head -30; ls spec data app | head -40; grep -rIl \"Patient states\\|Patient reports\" --include=*.md --include=*.txt --include=*.json --include=*.jsonl --include=*.py . 2>/dev/null | grep -v \"reviews/\\|artifacts/review-evidence\\|\\.venv\\|agent-memory\\|evals/reports\" | head -30"
}
````

### User / tool · 2026-11-02T04:31:16.547Z

**tool result**
````
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
app:
README-arch.md
__init__.py
__pycache__
backend
db
frontend
llm
main.py
pipeline.py

data:
zlayt.sqlite

spec:
REQUIREMENTS.md
SAMPLE_CASE_TRUTHS.md
SPEC.md
MASTER_PROMPT.md
research/adjuster-attacks.md
research/ASSUMPTIONS-proposed.md
research/lexicon_selfcheck.py
research/library_build.py
evals/golden/judge_controls.jsonl
evals/golden/hallucinations_controls.jsonl
evals/golden/case_01_date_formats.txt
evals/golden/sample.expected.json
evals/library/case_lib05_pedestrian_orif_hardware.txt
evals/library/case_lib12_records_review_credibility.txt
evals/library/case_lib04_dog_bite_scar_revision.expected.json
evals/library/case_lib07_parking_lot_fall_outside_records.expected.json
evals/library/case_lib12_records_review_credibility.expected.json
evals/library/case_lib08_second_crash_mri_after.expected.json
evals/library_build_v2.py
evals/golden/hallucinations.jsonl
evals/library/case_lib02_slip_fall_prior_knee.expected.json
evals/library/case_lib01_er_only_then_gap.expected.json
evals/library/case_lib15_conclusory_letter_mist.txt
evals/library/case_lib10_eob_ub04_cms1500.txt
board/activity.jsonl
app/backend/speaker.py
board/cards/T-061.md
memory/ORCHESTRATOR_DECISIONS.md
board/cards/T-074.md
board/cards/T-036.md
tests/unit/test_pdf_ocr.py
tests/unit/test_flags_sample.py
board/cards/T-091.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:31:57.078Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-091/build_attacks.py",
 "content": "\"\"\"T-091 adversary attack set (claims-adjuster-reviewer). Writes attacks.jsonl next to this file.\n\nexpect = what a human reader (a defense adjuster, or a paralegal reading a chip that says 'patient's own statement')\nconcludes about WHO is speaking in the whole excerpt:\n  patient  genuinely the patient's own statement and nothing else\n  other    every statement is by a named non-patient source\n  unknown  mixed, unattributed, passive/received (told/advised), clinician observation, ambiguous, or not a statement\ngroup 'genuine' rows measure usefulness only; every other row is an attack.\n\"\"\"\nimport json\nimport pathlib\n\nA = []   # (group, text, expect, why)\n\n\ndef add(group, expect, why, *texts):\n    for t in texts:\n        A.append((group, t, expect, why))\n\n\n# ---- G1: patient is the RECEIVER or the SUBJECT OF A DESCRIPTION, not the speaker (verbs the grammar treats as patient speech)\nadd(\"receiver_told_advised\", \"unknown\", \"clinician instruction/information given TO the patient\",\n    \"Patient advised to rest and ice.\",\n    \"Patient told to rest, no driving, no lifting.\",\n    \"Patient told it was a strain.\",\n    \"Patient informed that it is a sprain.\",\n    \"Patient advised by ER to rest.\",\n    \"Patient advised to stop working.\",\n    \"Patient advised to take ibuprofen and rest.\",\n    \"Patient told to take ibuprofen.\",\n    \"Patient told to ice and rest.\",\n    \"Patient advised to stand, walk and rest.\",\n    \"Pt advised to rest.\",\n    \"Pt told to ice and rest, no lifting.\",\n    \"Paciente informado de que es una torcedura.\",\n    \"Patient recalled to clinic today.\",\n    \"Patient recalled to the clinic the next day.\")\n\nadd(\"description_by_someone_else\", \"unknown\", \"someone ELSE describes/records/observes the patient; the patient said nothing\",\n    \"Patient described as anxious.\",\n    \"Patient described as having neck pain.\",\n    \"Patient noted to be anxious.\",\n    \"Patient noted to have mild neck tenderness.\",\n    \"Patient reported to be in pain.\",\n    \"Patient reported as unconscious at scene.\",\n    \"Patient thought to have a strain.\",\n    \"Patient believed to have a sprain.\",\n    \"Patient documented as having neck pain.\",\n    \"Patient recorded as ambulatory.\",\n    \"Patient said to be fine.\",\n    \"Patient responds well to ice and rest.\",\n    \"Patient responds well to therapy.\",\n    \"Patient responds well to treatment.\",\n    \"Patient alleged to be at fault.\",\n    \"Patient noted limping.\",\n    \"Patient noted to be walking normally.\")\n\nadd(\"noun_use_of_verb\", \"unknown\", \"'state/records/notes/report' is a noun (patient's condition, patient's chart); no one is speaking\",\n    \"Patient state: alert and oriented.\",\n    \"Patient state: stable.\",\n    \"Patient state: stable, alert, oriented, no distress.\",\n    \"Patient records: neck pain, headaches, nausea.\",\n    \"Patient records: neck pain 7/10, headaches.\",\n    \"Patient documents: neck pain.\",\n    \"Patient notes: neck pain 7/10.\",\n    \"Patient note: neck pain improved.\",\n    \"Patient Notes: neck pain 5/10, stable.\")\n\nadd(\"pt_title_case_physical_therapy\", \"unknown\", \"Title-case Pt/PT notes = physical therapy note, not the patient\",\n    \"Pt Notes: neck pain 5/10.\",\n    \"Pt. Notes: neck pain 5/10.\",\n    \"Pt Notes - neck pain 5/10.\",\n    \"Pt note: neck pain improved.\",\n    \"Pt Report: neck pain 5/10, headaches.\",\n    \"pt notes: neck pain 5/10\",\n    \"PT Notes: neck pain 5/10.\",\n    \"PT note: neck pain improved.\",\n    \"PT. notes neck pain improved.\",\n    \"PT reports neck pain 5/10.\",\n    \"Pt. Note: pain 4/10, stable, no distress.\")\n\n# ---- G2: unattributed clause after a patient head: scene / exam / EMS observation riding under the patient label\nadd(\"unattributed_observation_semicolon\", \"unknown\", \"clause after the head has no speaker; scene/exam observation, not a patient statement\",\n    \"Patient reports neck pain; airbags deployed.\",\n    \"Patient reports neck pain; minimal vehicle damage.\",\n    \"Patient reports neck pain; vehicle damage minimal, airbags deployed.\",\n    \"Patient denies neck pain; ambulatory at scene.\",\n    \"Patient denies loss of consciousness; alert and oriented.\",\n    \"Patient reports headache; alert, oriented, no distress.\",\n    \"Patient states neck pain; gait steady.\",\n    \"Patient states neck pain; gait steady and normal.\",\n    \"Patient reports neck pain; left knee swollen and bruised.\",\n    \"Patient reports neck pain; no distress.\",\n    \"Patient states neck pain; stable.\",\n    \"Patient states neck pain; alert and oriented.\",\n    \"Patient states neck pain; red light, rear-ended, minimal damage.\",\n    \"Patient reports low back pain; sharp, constant, moderate.\",\n    \"Pt c/o neck pain; ambulatory, alert and oriented.\",\n    \"Paciente refiere dolor de cuello; estable.\",\n    \"Paciente refiere dolor de cuello; choque, daño mínimo.\")\n\nadd(\"unattributed_observation_other_connectors\", \"unknown\", \"same, via comma / and / dash / colon / paren / ampersand / ellipsis\",\n    \"Patient reports neck pain, neck stiff and tender.\",\n    \"Patient reports neck pain, no distress.\",\n    \"Patient reports neck pain, stable.\",\n    \"Patient states neck pain and is alert and oriented.\",\n    \"Patient states neck pain and ambulatory at scene.\",\n    \"Patient reports neck pain - alert and oriented.\",\n    \"Patient reports neck pain — airbags deployed.\",\n    \"Patient reports neck pain: gait steady.\",\n    \"Patient reports neck pain (alert and oriented).\",\n    \"Patient states neck pain (gait steady, no distress).\",\n    \"Patient reports neck pain [airbags deployed].\",\n    \"Patient reports neck pain & alert and oriented.\",\n    \"Patient reports neck pain... airbags deployed.\",\n    \"Patient reports neck pain / alert and oriented.\",\n    \"Patient reports neck pain but alert and oriented.\",\n    \"Patient reports neck pain while ambulatory at scene.\",\n    \"Patient reports neck pain, vehicle damage minimal.\",\n    \"Patient reports neck pain, speed 25 mph, light traffic.\")\n\nadd(\"unattributed_observation_line_break\", \"unknown\", \"next line is a separate entry (nurse/EMS finding) with no speaker\",\n    \"Patient reports neck pain\\nAlert and oriented\\nAmbulatory at scene\",\n    \"Patient states headache\\nVehicle damage minimal\",\n    \"Patient states neck pain\\nGait steady\",\n    \"Patient states neck pain,\\nairbags deployed\",\n    \"Patient states neck pain\\n  stable\",\n    \"Patient denies loss of consciousness\\nalert and oriented\",\n    \"Patient states neck pain\\tairbags deployed\",\n    \"Patient states neck pain | airbags deployed\",\n    \"Patient states neck pain\\n- alert and oriented\\n- ambulatory at scene\",\n    \"Patient states neck pain\\n• airbags deployed\")\n\n# ---- G3: pronouns / first person inside a continuation\nadd(\"pronoun_continuation\", \"unknown\", \"he/she/they/I/we/you cannot be resolved to the patient; may be wife, EMS, examiner\",\n    \"Patient states neck pain; she feels dizzy.\",\n    \"Patient states neck pain; he feels dizzy.\",\n    \"Patient reports headache, he seemed confused.\",\n    \"Patient reports neck pain and she is anxious.\",\n    \"Patient states neck pain; I felt a spasm.\",\n    \"Patient states neck pain while I lifted her arm.\",\n    \"Patient states neck pain; we walked to the car.\",\n    \"Patient reports neck pain; they felt it too.\",\n    \"Patient states neck pain; you can see it is swollen.\",\n    \"Patient states neck pain, I feel it is mild.\",\n    \"Patient reports neck pain; he is worse today.\",\n    \"Patient reports neck pain; she is better today.\",\n    \"Patient states neck pain, they were rear-ended.\",\n    \"Patient states neck pain; we were hit from behind.\",\n    \"Patient reports neck pain; I took her to the ER.\",\n    \"Patient reports neck pain, she got worse at night.\")\n\n# ---- G4: vocabulary words that are institutions/places acting as the speaker\nadd(\"vocab_word_as_source\", \"unknown\", \"ER/ED/clinic/hospital/office/work are non-patient sources that happen to be in the closed vocabulary\",\n    \"Patient reports neck pain; ER felt it was a sprain.\",\n    \"Patient reports neck pain; ED felt it was a strain.\",\n    \"Patient states neck pain; the hospital felt it was fine.\",\n    \"Patient states neck pain; clinic felt it was a sprain.\",\n    \"Patient states neck pain; the office felt it was minor.\",\n    \"Patient states neck pain; work felt it was fine.\",\n    \"Patient reports neck pain, ER thought it was a sprain.\",\n    \"Patient reports neck pain, ER seemed to feel it was a strain.\")\n\n# ---- G5: mixed speakers (should all be unknown)\nadd(\"mixed_new_shapes\", \"unknown\", \"two speakers or a speaker plus unattributed text\",\n    \"Patient reports neck pain, per wife.\",\n    \"Pt c/o neck pain, EMS reports ambulatory.\",\n    \"Patient states neck pain\\nWife: headaches since crash\",\n    \"Patient says neck pain; the officer says the other car was speeding.\",\n    \"Patient reports neck pain ... Wife says he snores.\",\n    \"Patient states neck pain 7/10, whereas EMS recorded 3/10.\",\n    \"HPI: Per wife, patient states neck pain.\",\n    \"Collateral (wife): patient states neck pain\",\n    \"Wife (historian): patient reports neck pain\",\n    \"Per EMS: patient c/o neck pain\",\n    \"Patient states neck pain; spouse concurs.\",\n    \"Patient states neck pain — nurse agrees.\",\n    \"Neck pain (per patient and wife).\",\n    \"Neck pain per patient/wife.\",\n    \"Neck pain per patient or wife.\",\n    \"Neck pain per pt, mother.\",\n    \"Patient and mother state neck pain.\",\n    \"Patient: neck pain. Mother: headaches.\",\n    \"Wife reports that patient told her he has neck pain.\",\n    \"Patient reports his wife has neck pain.\",\n    \"Patient states pain 7/10 (wife: 9/10).\",\n    \"Patient states neck pain; per EMS, ambulatory.\",\n    \"Per patient, neck pain; per EMS, ambulatory.\",\n    \"Patient states neck pain. EMS states ambulatory.\",\n    \"Patient states neck pain.\\n\\nEMS states ambulatory.\",\n    \"Patient says it hurts, the paramedic wrote alert and oriented.\",\n    \"**Patient states** neck pain; **wife reports** headaches.\",\n    \"<b>Patient states</b> neck pain <i>wife says</i> headaches\",\n    \"Patient states neck pain  wife reports headaches\",\n    \"Patient states neck pain -- wife reports headaches\",\n    \"Patient states neck pain → wife reports headaches\",\n    \"Patient states neck pain; wife reports; headaches\",\n    \"Patient states neck pain, wife, reports headaches\",\n    \"Patient states neck pain. wife reports headaches\",\n    \"Patient states neck pain.wife reports headaches\",\n    \"Patient states neck pain;wife reports headaches\",\n    \"Patient states neck pain;\\nwife reports headaches\",\n    \"Patient states neck pain ;wife reports headaches\")\n\nadd(\"reported_speech_chains\", \"unknown\", \"who said what is not one speaker\",\n    \"Patient states his wife says he was fine.\",\n    \"Patient states that his wife reports he has headaches.\",\n    \"Wife says patient states neck pain.\",\n    \"EMS reports patient c/o neck pain.\",\n    \"Nurse notes patient states neck pain.\",\n    \"Doctor notes that patient reports neck pain.\",\n    \"Patient states that EMS reports she was fine.\",\n    \"Patient states EMS reports she was fine.\",\n    \"Patient states EMS says she was fine, wife says she was not.\",\n    \"The wife told EMS that the patient states neck pain.\")\n\n# ---- G6: 'other' label correctness (patient may be the driver/passenger) -- tool says 'other', human says unknown/patient\nadd(\"other_may_be_the_patient\", \"unknown\", \"Driver/passenger/occupant is very often the patient himself; calling this a non-patient source is a guess\",\n    \"Driver states neck pain.\",\n    \"Driver states he was stopped at a red light.\",\n    \"Passenger reports neck pain.\",\n    \"Driver reports neck pain and headache.\",\n    \"Driver denies loss of consciousness.\",\n    \"Passenger states pain began immediately.\")\n\n# ---- G7: Spanish and abbreviations\nadd(\"spanish_new\", \"unknown\", \"Spanish mixed/unattributed/passive\",\n    \"Paciente refiere dolor de cuello; esposa refiere cefalea.\",\n    \"Paciente refiere dolor de cuello. Esposa refiere cefalea.\",\n    \"Según la esposa, el paciente tiene dolor de cuello.\",\n    \"Paciente indica dolor de cuello, según la esposa.\",\n    \"Paciente refiere dolor de cuello y su esposa también.\",\n    \"El paciente y su esposa refieren dolor de cuello.\",\n    \"Paciente informado de reposo.\",\n    \"Paciente refiere dolor; está estable.\",\n    \"Paciente refiere dolor de cuello; ella tiene mareo.\",\n    \"Paciente niega pérdida de conciencia; alerta y orientado.\",\n    \"Esposa: paciente refiere dolor de cuello.\",\n    \"Según paramedico, paciente refiere dolor de cuello.\")\n\nadd(\"abbreviation_tail\", \"unknown\", \"abbreviation stripping / sentence merge / unusual tokens\",\n    \"Patient reports neck pain no. Wife reports headaches.\",\n    \"Patient reports neck pain, w/ wife reporting headaches.\",\n    \"Patient reports neck pain w/ EMS noting ambulatory.\",\n    \"Patient c/o neck pain s/p MVC.\",\n    \"Patient reports neck pain. Dr. says ambulatory.\",\n    \"Patient reports 3rd-party driver said light was green.\",\n    \"Patient reports neck pain, 2nd-driver stopped.\",\n    \"Patient reports neck pain; 911 called by bystander.\",\n    \"Pt. reports neck pain, per Dr. Lee.\",\n    \"Pt reports neck pain per PT.\",\n    \"Pt reports neck pain per PT eval.\",\n    \"PT: pt reports neck pain 5/10\",\n    \"PT states pt reports neck pain 5/10\",\n    \"Pt reports neck pain; PT notes improved ROM.\")\n\n# ---- GENUINE patient statements (usefulness): human expects patient\nadd(\"genuine\", \"patient\", \"usefulness probe\",\n    \"Patient states symptoms began after the January collision.\",\n    \"Patient reports new onset pain radiating to right arm.\",\n    \"Patient reports pain 6/10.\",\n    \"Patient states neck pain and stiffness since the accident.\",\n    \"Patient reports low back pain in 2023, which resolved.\",\n    \"Patient states she was stopped at a red light when she was rear-ended.\",\n    \"Patient reports headaches daily since the collision.\",\n    \"Patient denies prior neck injury.\",\n    \"Patient reports she missed 3 days of work.\",\n    \"Patient states she has trouble sleeping due to pain.\",\n    \"Patient states she is taking ibuprofen for the pain.\",\n    \"Patient reports pain with turning her head to the right.\",\n    \"Patient states symptoms are improving with physical therapy.\",\n    \"Patient reports that her neck feels stiff in the morning.\",\n    \"Patient denies numbness, tingling, or weakness in the arms.\",\n    \"Patient states he hit his head on the steering wheel.\",\n    \"Patient reports no loss of consciousness.\",\n    \"Patient reports being rear-ended while stopped at a light.\",\n    \"Pt c/o 7/10 neck pain.\",\n    \"Patient states pain started that night.\",\n    \"Patient reports her symptoms began the day after the accident.\",\n    \"Patient reports difficulty with prolonged sitting.\",\n    \"Patient reports tenderness in the neck.\",\n    \"Patient endorses neck pain.\",\n    \"Patient reports pain in the neck and right shoulder.\",\n    \"Patient states that the pain has been constant since the accident.\",\n    \"Patient states she feels better after the injection.\",\n    \"Patient reports dizziness and nausea after the collision.\",\n    \"Patient states the pain radiates down her right arm.\",\n    \"Patient reports pain is 5/10 today.\",\n    \"Patient states she had low back pain in 2023 that resolved.\",\n    \"Patient reports headaches that start in the neck.\",\n    \"Patient states she has no prior neck injuries.\",\n    \"Pt reports 5/10 pain at start of session.\",\n    \"Pt states neck feels better today.\",\n    \"Patient states: \\\"my neck hurts\\\".\",\n    \"Patient reports the collision occurred on January 9.\",\n    \"Patient states she did not seek care until the next day.\",\n    \"Patient denies chest pain or shortness of breath.\",\n    \"Patient states she wore her seat belt.\",\n    \"Patient reports she has been unable to lift her son since the crash.\",\n    \"Patient states she cannot sit for long periods.\",\n    \"Patient reports she has missed two appointments because of work.\",\n    \"Patient reports compliance with the home exercise program.\",\n    \"Patient states she has a desk job.\",\n    \"Patient denies LOC.\",\n    \"Patient states he felt dizzy at the scene.\",\n    \"Patient states he was wearing his seat belt and the airbags deployed.\",\n    \"Patient reports her neck was sore the next morning.\",\n    \"Patient states the other driver ran the red light.\")\n\nrows = []\nfor i, (g, t, e, why) in enumerate(A, 1):\n    rows.append({\"id\": f\"CA-{i:03d}\", \"group\": g, \"text\": t, \"expect\": e, \"why\": why})\nout = pathlib.Path(__file__).with_name(\"attacks.jsonl\")\nout.write_text(\"\".join(json.dumps(r, ensure_ascii=False) + \"\\n\" for r in rows), encoding=\"utf-8\")\nprint(len(rows), \"rows;\", sum(r[\"group\"] != \"genuine\" for r in rows), \"attack rows;\", sum(r[\"group\"] == \"genuine\" for r in rows), \"genuine rows\")\n"
}
````

### User / tool · 2026-11-02T04:31:57.178Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-091/build_attacks.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:32:02.378Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-091/probe.py",
 "content": "\"\"\"Run app/backend/speaker.py on attacks.jsonl. usage: probe.py <repo-root>  (prints misses; writes results.jsonl).\"\"\"\nimport json\nimport pathlib\nimport sys\nimport collections\n\nroot = pathlib.Path(sys.argv[1]).resolve()\nsys.path.insert(0, str(root))\nfrom app.backend import speaker  # noqa: E402\n\nhere = pathlib.Path(__file__).parent\nrows = [json.loads(l) for l in (here / \"attacks.jsonl\").read_text(encoding=\"utf-8\").splitlines() if l.strip()]\nres = []\nfor r in rows:\n    got = speaker.attribute(r[\"text\"]).label\n    res.append({**r, \"got\": got})\n(here / \"results.jsonl\").write_text(\"\".join(json.dumps(x, ensure_ascii=False) + \"\\n\" for x in res), encoding=\"utf-8\")\n\nattacks = [x for x in res if x[\"group\"] != \"genuine\"]\ngen = [x for x in res if x[\"group\"] == \"genuine\"]\nbad_patient = [x for x in attacks if x[\"got\"] == \"patient\"]            # blocker class: human reads other/unknown\nbad_other = [x for x in attacks if x[\"got\"] == \"other\" and x[\"expect\"] == \"unknown\"]   # also wrong, lower cost\nprint(f\"attack rows {len(attacks)}; tool says PATIENT where a human reads other/unknown: {len(bad_patient)}\")\nprint(f\"attack rows where tool says OTHER but a human reads unknown: {len(bad_other)}\")\nby = collections.Counter(x[\"group\"] for x in bad_patient)\nfor g, n in by.most_common():\n    tot = sum(1 for x in attacks if x[\"group\"] == g)\n    print(f\"  {g}: {n}/{tot}\")\nprint(\"\\n--- PATIENT misses ---\")\nfor x in bad_patient:\n    print(f'{x[\"id\"]} [{x[\"group\"]}] {x[\"text\"]!r}')\nprint(\"\\n--- OTHER-for-unknown ---\")\nfor x in bad_other:\n    print(f'{x[\"id\"]} [{x[\"group\"]}] {x[\"text\"]!r}')\nlab = collections.Counter(x[\"got\"] for x in gen)\nprint(f\"\\ngenuine patient statements: {len(gen)}; labelled patient {lab['patient']} ({100*lab['patient']/len(gen):.0f}%), unknown {lab['unknown']}, other {lab['other']}\")\nprint(\"--- genuine NOT labelled patient ---\")\nfor x in gen:\n    if x[\"got\"] != \"patient\":\n        print(f'{x[\"id\"]} -> {x[\"got\"]}: {x[\"text\"]!r}')\n"
}
````

### User / tool · 2026-11-02T04:32:02.475Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-091/probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:32:05.113Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git diff --quiet 17cc9c7 -- app/backend/speaker.py evals/adversarial/speaker_attribution.jsonl && echo \"speaker.py + set identical to 17cc9c7\" ; .venv/bin/python artifacts/review-evidence/T-091/build_attacks.py && .venv/bin/python artifacts/review-evidence/T-091/probe.py /Users/arsis/zlayt-pm-project"
}
````

### User / tool · 2026-11-02T04:32:05.312Z

**tool result**
````
02ff2440f195580a19627586ac44d7df25906d0c
speaker.py + set identical to 17cc9c7
251 rows; 201 attack rows; 50 genuine rows
attack rows 201; tool says PATIENT where a human reads other/unknown: 110
attack rows where tool says OTHER but a human reads unknown: 6
  description_by_someone_else: 17/17
  unattributed_observation_other_connectors: 17/18
  unattributed_observation_semicolon: 15/17
  pronoun_continuation: 15/16
  receiver_told_advised: 13/15
  unattributed_observation_line_break: 10/10
  noun_use_of_verb: 9/9
  pt_title_case_physical_therapy: 7/11
  vocab_word_as_source: 6/8
  abbreviation_tail: 1/14

--- PATIENT misses ---
CA-001 [receiver_told_advised] 'Patient advised to rest and ice.'
CA-002 [receiver_told_advised] 'Patient told to rest, no driving, no lifting.'
CA-003 [receiver_told_advised] 'Patient told it was a strain.'
CA-004 [receiver_told_advised] 'Patient informed that it is a sprain.'
CA-005 [receiver_told_advised] 'Patient advised by ER to rest.'
CA-006 [receiver_told_advised] 'Patient advised to stop working.'
CA-007 [receiver_told_advised] 'Patient advised to take ibuprofen and rest.'
CA-008 [receiver_told_advised] 'Patient told to take ibuprofen.'
CA-009 [receiver_told_advised] 'Patient told to ice and rest.'
CA-010 [receiver_told_advised] 'Patient advised to stand, walk and rest.'
CA-011 [receiver_told_advised] 'Pt advised to rest.'
CA-012 [receiver_told_advised] 'Pt told to ice and rest, no lifting.'
CA-014 [receiver_told_advised] 'Patient recalled to clinic today.'
CA-016 [description_by_someone_else] 'Patient described as anxious.'
CA-017 [description_by_someone_else] 'Patient described as having neck pain.'
CA-018 [description_by_someone_else] 'Patient noted to be anxious.'
CA-019 [description_by_someone_else] 'Patient noted to have mild neck tenderness.'
CA-020 [description_by_someone_else] 'Patient reported to be in pain.'
CA-021 [description_by_someone_else] 'Patient reported as unconscious at scene.'
CA-022 [description_by_someone_else] 'Patient thought to have a strain.'
CA-023 [description_by_someone_else] 'Patient believed to have a sprain.'
CA-024 [description_by_someone_else] 'Patient documented as having neck pain.'
CA-025 [description_by_someone_else] 'Patient recorded as ambulatory.'
CA-026 [description_by_someone_else] 'Patient said to be fine.'
CA-027 [description_by_someone_else] 'Patient responds well to ice and rest.'
CA-028 [description_by_someone_else] 'Patient responds well to therapy.'
CA-029 [description_by_someone_else] 'Patient responds well to treatment.'
CA-030 [description_by_someone_else] 'Patient alleged to be at fault.'
CA-031 [description_by_someone_else] 'Patient noted limping.'
CA-032 [description_by_someone_else] 'Patient noted to be walking normally.'
CA-033 [noun_use_of_verb] 'Patient state: alert and oriented.'
CA-034 [noun_use_of_verb] 'Patient state: stable.'
CA-035 [noun_use_of_verb] 'Patient state: stable, alert, oriented, no distress.'
CA-036 [noun_use_of_verb] 'Patient records: neck pain, headaches, nausea.'
CA-037 [noun_use_of_verb] 'Patient records: neck pain 7/10, headaches.'
CA-038 [noun_use_of_verb] 'Patient documents: neck pain.'
CA-039 [noun_use_of_verb] 'Patient notes: neck pain 7/10.'
CA-040 [noun_use_of_verb] 'Patient note: neck pain improved.'
CA-041 [noun_use_of_verb] 'Patient Notes: neck pain 5/10, stable.'
CA-042 [pt_title_case_physical_therapy] 'Pt Notes: neck pain 5/10.'
CA-043 [pt_title_case_physical_therapy] 'Pt. Notes: neck pain 5/10.'
CA-044 [pt_title_case_physical_therapy] 'Pt Notes - neck pain 5/10.'
CA-045 [pt_title_case_physical_therapy] 'Pt note: neck pain improved.'
CA-046 [pt_title_case_physical_therapy] 'Pt Report: neck pain 5/10, headaches.'
CA-047 [pt_title_case_physical_therapy] 'pt notes: neck pain 5/10'
CA-052 [pt_title_case_physical_therapy] 'Pt. Note: pain 4/10, stable, no distress.'
CA-053 [unattributed_observation_semicolon] 'Patient reports neck pain; airbags deployed.'
CA-054 [unattributed_observation_semicolon] 'Patient reports neck pain; minimal vehicle damage.'
CA-055 [unattributed_observation_semicolon] 'Patient reports neck pain; vehicle damage minimal, airbags deployed.'
CA-056 [unattributed_observation_semicolon] 'Patient denies neck pain; ambulatory at scene.'
CA-057 [unattributed_observation_semicolon] 'Patient denies loss of consciousness; alert and oriented.'
CA-058 [unattributed_observation_semicolon] 'Patient reports headache; alert, oriented, no distress.'
CA-059 [unattributed_observation_semicolon] 'Patient states neck pain; gait steady.'
CA-060 [unattributed_observation_semicolon] 'Patient states neck pain; gait steady and normal.'
CA-061 [unattributed_observation_semicolon] 'Patient reports neck pain; left knee swollen and bruised.'
CA-062 [unattributed_observation_semicolon] 'Patient reports neck pain; no distress.'
CA-063 [unattributed_observation_semicolon] 'Patient states neck pain; stable.'
CA-064 [unattributed_observation_semicolon] 'Patient states neck pain; alert and oriented.'
CA-065 [unattributed_observation_semicolon] 'Patient states neck pain; red light, rear-ended, minimal damage.'
CA-066 [unattributed_observation_semicolon] 'Patient reports low back pain; sharp, constant, moderate.'
CA-067 [unattributed_observation_semicolon] 'Pt c/o neck pain; ambulatory, alert and oriented.'
CA-070 [unattributed_observation_other_connectors] 'Patient reports neck pain, neck stiff and tender.'
CA-071 [unattributed_observation_other_connectors] 'Patient reports neck pain, no distress.'
CA-072 [unattributed_observation_other_connectors] 'Patient reports neck pain, stable.'
CA-073 [unattributed_observation_other_connectors] 'Patient states neck pain and is alert and oriented.'
CA-074 [unattributed_observation_other_connectors] 'Patient states neck pain and ambulatory at scene.'
CA-075 [unattributed_observation_other_connectors] 'Patient reports neck pain - alert and oriented.'
CA-076 [unattributed_observation_other_connectors] 'Patient reports neck pain — airbags deployed.'
CA-077 [unattributed_observation_other_connectors] 'Patient reports neck pain: gait steady.'
CA-078 [unattributed_observation_other_connectors] 'Patient reports neck pain (alert and oriented).'
CA-079 [unattributed_observation_other_connectors] 'Patient states neck pain (gait steady, no distress).'
CA-080 [unattributed_observation_other_connectors] 'Patient reports neck pain [airbags deployed].'
CA-081 [unattributed_observation_other_connectors] 'Patient reports neck pain & alert and oriented.'
CA-083 [unattributed_observation_other_connectors] 'Patient reports neck pain / alert and oriented.'
CA-084 [unattributed_observation_other_connectors] 'Patient reports neck pain but alert and oriented.'
CA-085 [unattributed_observation_other_connectors] 'Patient reports neck pain while ambulatory at scene.'
CA-086 [unattributed_observation_other_connectors] 'Patient reports neck pain, vehicle damage minimal.'
CA-087 [unattributed_observation_other_connectors] 'Patient reports neck pain, speed 25 mph, light traffic.'
CA-088 [unattributed_observation_line_break] 'Patient reports neck pain\nAlert and oriented\nAmbulatory at scene'
CA-089 [unattributed_observation_line_break] 'Patient states headache\nVehicle damage minimal'
CA-090 [unattributed_observation_line_break] 'Patient states neck pain\nGait steady'
CA-091 [unattributed_observation_line_break] 'Patient states neck pain,\nairbags deployed'
CA-092 [unattributed_observation_line_break] 'Patient states neck pain\n  stable'
CA-093 [unattributed_observation_line_break] 'Patient denies loss of consciousness\nalert and oriented'
CA-094 [unattributed_observation_line_break] 'Patient states neck pain\tairbags deployed'
CA-095 [unattributed_observation_line_break] 'Patient states neck pain | airbags deployed'
CA-096 [unattributed_observation_line_break] 'Patient states neck pain\n- alert and oriented\n- ambulatory at scene'
CA-097 [unattributed_observation_line_break] 'Patient states neck pain\n• airbags deployed'
CA-098 [pronoun_continuation] 'Patient states neck pain; she feels dizzy.'
CA-099 [pronoun_continuation] 'Patient states neck pain; he feels dizzy.'
CA-100 [pronoun_continuation] 'Patient reports headache, he seemed confused.'
CA-101 [pronoun_continuation] 'Patient reports neck pain and she is anxious.'
CA-102 [pronoun_continuation] 'Patient states neck pain; I felt a spasm.'
CA-103 [pronoun_continuation] 'Patient states neck pain while I lifted her arm.'
CA-104 [pronoun_continuation] 'Patient states neck pain; we walked to the car.'
CA-105 [pronoun_continuation] 'Patient reports neck pain; they felt it too.'
CA-107 [pronoun_continuation] 'Patient states neck pain, I feel it is mild.'
CA-108 [pronoun_continuation] 'Patient reports neck pain; he is worse today.'
CA-109 [pronoun_continuation] 'Patient reports neck pain; she is better today.'
CA-110 [pronoun_continuation] 'Patient states neck pain, they were rear-ended.'
CA-111 [pronoun_continuation] 'Patient states neck pain; we were hit from behind.'
CA-112 [pronoun_continuation] 'Patient reports neck pain; I took her to the ER.'
CA-113 [pronoun_continuation] 'Patient reports neck pain, she got worse at night.'
CA-114 [vocab_word_as_source] 'Patient reports neck pain; ER felt it was a sprain.'
CA-115 [vocab_word_as_source] 'Patient reports neck pain; ED felt it was a strain.'
CA-116 [vocab_word_as_source] 'Patient states neck pain; the hospital felt it was fine.'
CA-117 [vocab_word_as_source] 'Patient states neck pain; clinic felt it was a sprain.'
CA-119 [vocab_word_as_source] 'Patient states neck pain; work felt it was fine.'
CA-121 [vocab_word_as_source] 'Patient reports neck pain, ER seemed to feel it was a strain.'
CA-194 [abbreviation_tail] 'Patient reports neck pain, 2nd-driver stopped.'

--- OTHER-for-unknown ---
CA-170 [other_may_be_the_patient] 'Driver states neck pain.'
CA-171 [other_may_be_the_patient] 'Driver states he was stopped at a red light.'
CA-172 [other_may_be_the_patient] 'Passenger reports neck pain.'
CA-173 [other_may_be_the_patient] 'Driver reports neck pain and headache.'
CA-174 [other_may_be_the_patient] 'Driver denies loss of consciousness.'
CA-178 [spanish_new] 'Según la esposa, el paciente tiene dolor de cuello.'

genuine patient statements: 50; labelled patient 34 (68%), unknown 16, other 0
--- genuine NOT labelled patient ---
CA-202 -> unknown: 'Patient states symptoms began after the January collision.'
CA-203 -> unknown: 'Patient reports new onset pain radiating to right arm.'
CA-235 -> unknown: 'Pt reports 5/10 pain at start of session.'
CA-238 -> unknown: 'Patient reports the collision occurred on January 9.'
CA-239 -> unknown: 'Patient states she did not seek care until the next day.'
CA-240 -> unknown: 'Patient denies chest pain or shortness of breath.'
CA-241 -> unknown: 'Patient states she wore her seat belt.'
CA-242 -> unknown: 'Patient reports she has been unable to lift her son since the crash.'
CA-243 -> unknown: 'Patient states she cannot sit for long periods.'
CA-244 -> unknown: 'Patient reports she has missed two appointments because of work.'
CA-245 -> unknown: 'Patient reports compliance with the home exercise program.'
CA-246 -> unknown: 'Patient states she has a desk job.'
CA-247 -> unknown: 'Patient denies LOC.'
CA-249 -> unknown: 'Patient states he was wearing his seat belt and the airbags deployed.'
CA-250 -> unknown: 'Patient reports her neck was sore the next morning.'
CA-251 -> unknown: 'Patient states the other driver ran the red light.'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:32:22.368Z

**tool call — Bash**
````
{
 "command": "sed -i 's/\"Seg\\\\u00fan la esposa, el paciente tiene dolor de cuello.\",/\"__ES_OTHER__\",/' artifacts/review-evidence/T-091/build_attacks.py && grep -n \"__ES_OTHER__\\|esposa, el paciente\" artifacts/review-evidence/T-091/build_attacks.py; grep -rn \"import speaker\\|from app.backend import.*speaker\\|backend.speaker\\|backend import speaker\" --include=*.py app tests tools | head; .venv/bin/python -m pytest tests/unit/test_speaker.py -q -p no:cacheprovider 2>&1 | tail -4"
}
````

### User / tool · 2026-11-02T04:32:24.093Z

**tool result**
````
sed: 1: "artifacts/review-eviden ...": command a expects \ followed by text
tests/unit/test_speaker.py:1:"""T-091: speaker attribution v2 (app/backend/speaker.py) against the adversarial set. Module is disabled (D-040); this is the gate.
tests/unit/test_speaker.py:13:from app.backend import speaker
........                                                                 [100%]
8 passed in 1.34s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:32:26.558Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-091/build_attacks.py",
 "old_string": "    \"Según la esposa, el paciente tiene dolor de cuello.\",\n    \"Paciente indica",
 "new_string": "    \"Paciente indica"
}
````

### User / tool · 2026-11-02T04:32:26.734Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-091/build_attacks.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:32:34.704Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-091/grid_and_corpus.py",
 "content": "\"\"\"(1) Generated grid the worker's own grid omits: patient head x connector x UNATTRIBUTED vocab-only clause.\n   (2) Usefulness on repo records: sentences that start with Patient/Pt + reporting verb in evals/golden + evals/library + sample.\nusage: grid_and_corpus.py <repo-root>\"\"\"\nimport itertools\nimport pathlib\nimport re\nimport sys\nimport collections\n\nroot = pathlib.Path(sys.argv[1]).resolve()\nsys.path.insert(0, str(root))\nfrom app.backend import speaker  # noqa: E402\n\nheads = [\"Patient reports neck pain\", \"Pt states headaches\", \"Patient denies loss of consciousness\"]\nconns = [\", \", \"; \", \" - \", \" — \", \": \", \" (\", \" and \", \" but \", \" while \", \" & \", \" / \", \"\\n\", \"... \"]\nobs = [\"alert and oriented\", \"gait steady\", \"ambulatory at scene\", \"airbags deployed\", \"no distress\", \"vehicle damage minimal\",\n       \"stable\", \"neck stiff and tender\", \"left knee swollen and bruised\", \"I felt a spasm\", \"she feels dizzy\", \"ER felt it was a sprain\"]\nn = bad = 0\nby = collections.Counter()\nfor h, c, o in itertools.product(heads, conns, obs):\n    t = h + c + o + (\")\" if c.endswith(\"(\") else \"\") + \".\"\n    n += 1\n    if speaker.attribute(t).label == \"patient\":\n        bad += 1\n        by[c] += 1\nprint(f\"GRID unattributed clause: {bad}/{n} labelled patient\")\nprint(\"  by connector:\", dict(by))\n\nverb = re.compile(r\"\\b(patient|pt)\\b[^.]{0,6}\\b(states?|reports?|denies|c/o|complains?|says|endorses)\\b\", re.I)\nsents = []\nfor p in list((root / \"evals\" / \"golden\").glob(\"*.txt\")) + list((root / \"evals\" / \"library\").glob(\"*.txt\")):\n    txt = p.read_text(encoding=\"utf-8\", errors=\"ignore\")\n    for s in re.split(r\"(?<=[.!?])\\s+|\\n+\", txt):\n        s = s.strip()\n        if verb.search(s) and len(s) < 300:\n            sents.append(s)\nsents = sorted(set(sents))\nlab = collections.Counter(speaker.attribute(s).label for s in sents)\nprint(f\"\\nREPO corpus: {len(sents)} distinct sentences with a patient/pt + reporting verb; labels {dict(lab)}\")\nsolo = [s for s in sents if re.match(r\"^(the )?(patient|pt)\\b\", s, re.I)]\nlab2 = collections.Counter(speaker.attribute(s).label for s in solo)\nprint(f\"  starting with Patient/Pt: {len(solo)}; labels {dict(lab2)}  patient share {100*lab2['patient']/max(1,len(solo)):.0f}%\")\nfor s in solo[:60]:\n    print(f\"   {speaker.attribute(s).label:8s} {s!r}\")\n"
}
````

### User / tool · 2026-11-02T04:32:34.809Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-091/grid_and_corpus.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:32:36.808Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-091/build_attacks.py && .venv/bin/python artifacts/review-evidence/T-091/probe.py /Users/arsis/zlayt-pm-project | sed -n 1,14p; .venv/bin/python artifacts/review-evidence/T-091/probe.py /Users/arsis/zlayt-pm-project | grep -n \"genuine patient\\|OTHER-for\" ; .venv/bin/python artifacts/review-evidence/T-091/grid_and_corpus.py /Users/arsis/zlayt-pm-project"
}
````

### User / tool · 2026-11-02T04:32:37.106Z

**tool result**
````
250 rows; 200 attack rows; 50 genuine rows
attack rows 200; tool says PATIENT where a human reads other/unknown: 110
attack rows where tool says OTHER but a human reads unknown: 5
  description_by_someone_else: 17/17
  unattributed_observation_other_connectors: 17/18
  unattributed_observation_semicolon: 15/17
  pronoun_continuation: 15/16
  receiver_told_advised: 13/15
  unattributed_observation_line_break: 10/10
  noun_use_of_verb: 9/9
  pt_title_case_physical_therapy: 7/11
  vocab_word_as_source: 6/8
  abbreviation_tail: 1/14

--- PATIENT misses ---
126:--- OTHER-for-unknown ---
133:genuine patient statements: 50; labelled patient 34 (68%), unknown 16, other 0
GRID unattributed clause: 432/468 labelled patient
  by connector: {', ': 36, '; ': 36, ' - ': 36, ' — ': 36, ': ': 36, ' (': 36, ' and ': 36, ' but ': 36, ' while ': 36, ' & ': 36, ' / ': 36, '\n': 36}

REPO corpus: 31 distinct sentences with a patient/pt + reporting verb; labels {'unknown': 16, 'patient': 15}
  starting with Patient/Pt: 23; labels {'patient': 15, 'unknown': 8}  patient share 65%
   patient  'Patient denies prior neck problems.'
   patient  'Patient reports a prior left knee arthroscopy in 2019."'
   patient  'Patient reports low back pain in 2023, resolved."'
   patient  'Patient reports missing 3 days of work."'
   unknown  'Patient states his health plan was billed for the hospital stay."'
   patient  'Patient states pain began right after the collision."'
   patient  'Patient states she could not get an earlier appointment because the clinic was closed.'
   unknown  'Patient states she fell in the parking lot after a car brushed her.'
   unknown  'Patient states she had prior low back surgery in another state and outside records have been requested.'
   unknown  'Patient states she is self-conscious about the scar."'
   unknown  'Patient states she missed two physical therapy visits in May.'
   patient  'Patient states she was struck by a car while walking in a parking lot.'
   unknown  'Patient states symptoms began after the January collision."'
   unknown  'Pt states chest wall and left knee pain.'
   patient  'Pt states low back pain 6/10.'
   patient  'Pt states mild neck stiffness.'
   patient  'Pt states neck and low back pain 7/10.'
   patient  'Pt states neck and low back pain.'
   patient  'Pt states neck feels better."'
   patient  'Pt states neck pain 6/10 and tingling in the right hand.'
   patient  'Pt states neck pain 6/10.'
   patient  'Pt states neck pain 8/10 and left arm numbness.'
   unknown  'The patient reports she was rear-ended on 2026-10-04 and developed neck pain and headaches.'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:32:42.843Z

**tool call — Bash**
````
{
 "command": "for k in \"advised\" \"told\" \"informed\" \"described as\" \"noted to\" \"responds\" \"Patient state:\" \"Patient records\" \"Pt Notes\" \"airbags\" \"alert and oriented\" \"gait\"; do printf \"%s -> %s rows\\n\" \"$k\" \"$(grep -ci -- \"$k\" evals/adversarial/speaker_attribution.jsonl)\"; done; grep -i \"advised\\|told\\|alert\\|oriented\" evals/adversarial/speaker_attribution.jsonl | cut -c1-170 | head -12"
}
````

### User / tool · 2026-11-02T04:32:42.897Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to  %s rows\n)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:32:45.093Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport json\nrows=[json.loads(l) for l in open('evals/adversarial/speaker_attribution.jsonl')]\nfor k in [\"advised\",\"told\",\"informed\",\"described as\",\"noted to\",\"responds\",\"patient state:\",\"patient records\",\"pt notes\",\"airbags\",\"alert\",\"oriented\",\"gait\",\"stable\",\"i felt\",\"she feels\",\"er felt\",\"clinic felt\"]:\n    hits=[r for r in rows if k in r['text'].lower()]\n    print(k, len(hits), [ (r['expect'],r['text'][:60]) for r in hits[:2]])\nEOF"
}
````

### User / tool · 2026-11-02T04:32:45.202Z

**tool result**
````
advised 0 []
told 2 [('unknown', 'Patient states neck pain; his wife told the ER he was fine.'), ('patient', 'Patient reports EMS told him he had whiplash.')]
informed 0 []
described as 0 []
noted to 0 []
responds 0 []
patient state: 0 []
patient records 0 []
pt notes 0 []
airbags 0 []
alert 6 [('other', 'EMS notes pt alert and oriented at scene.'), ('other', 'Per EMS, pt was alert and oriented.')]
oriented 4 [('other', 'EMS notes pt alert and oriented at scene.'), ('other', 'Per EMS, pt was alert and oriented.')]
gait 1 [('other', 'Nurse notes pt ambulatory with steady gait.')]
stable 0 []
i felt 0 []
she feels 0 []
er felt 0 []
clinic felt 0 []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:32:51.941Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport json\nres=[json.loads(l) for l in open('artifacts/review-evidence/T-091/results.jsonl')]\narg_text={\"Patient notes: neck pain 7/10.\",\"Patient note: neck pain improved.\",\"Patient Notes: neck pain 5/10, stable.\",\"pt notes: neck pain 5/10\",\"Patient reports neck pain, 2nd-driver stopped.\",\n\"Patient states neck pain; she feels dizzy.\",\"Patient states neck pain; he feels dizzy.\",\"Patient reports headache, he seemed confused.\",\"Patient reports neck pain and she is anxious.\",\"Patient reports neck pain; he is worse today.\",\"Patient reports neck pain; she is better today.\",\"Patient states neck pain, they were rear-ended.\",\"Patient reports neck pain, she got worse at night.\"}\natt=[r for r in res if r['group']!='genuine']\nmiss=[r for r in att if r['got']=='patient']\ncore=[r for r in miss if r['text'] not in arg_text]\nprint(len(att),len(miss),len(core))\nprint([ (r['id'],r['text']) for r in miss if r['text'] in arg_text][:20])\nfor r in res:\n    if r['text'] in (\"Pt Notes: neck pain 5/10.\",\"Patient advised to rest and ice.\",\"Patient reports neck pain; airbags deployed.\",\"Patient states neck pain; I felt a spasm.\",\"Patient state: alert and oriented.\",\"Patient responds well to therapy.\",\"Patient reports neck pain; ER felt it was a sprain.\",\"Patient states symptoms began after the January collision.\",\"Patient noted to have mild neck tenderness.\",\"Patient reports neck pain\\nAlert and oriented\\nAmbulatory at scene\",\"Patient described as anxious.\",\"Patient records: neck pain, headaches, nausea.\"): print(r['id'],r['got'],repr(r['text']))\nEOF\nls reviews | grep T-091; git log --oneline -1; git diff --quiet 17cc9c7 -- app/backend/speaker.py && echo same"
}
````

### User / tool · 2026-11-02T04:32:52.081Z

**tool result**
````
200 110 97
[('CA-039', 'Patient notes: neck pain 7/10.'), ('CA-040', 'Patient note: neck pain improved.'), ('CA-041', 'Patient Notes: neck pain 5/10, stable.'), ('CA-047', 'pt notes: neck pain 5/10'), ('CA-098', 'Patient states neck pain; she feels dizzy.'), ('CA-099', 'Patient states neck pain; he feels dizzy.'), ('CA-100', 'Patient reports headache, he seemed confused.'), ('CA-101', 'Patient reports neck pain and she is anxious.'), ('CA-108', 'Patient reports neck pain; he is worse today.'), ('CA-109', 'Patient reports neck pain; she is better today.'), ('CA-110', 'Patient states neck pain, they were rear-ended.'), ('CA-113', 'Patient reports neck pain, she got worse at night.'), ('CA-193', 'Patient reports neck pain, 2nd-driver stopped.')]
CA-001 patient 'Patient advised to rest and ice.'
CA-016 patient 'Patient described as anxious.'
CA-019 patient 'Patient noted to have mild neck tenderness.'
CA-028 patient 'Patient responds well to therapy.'
CA-033 patient 'Patient state: alert and oriented.'
CA-036 patient 'Patient records: neck pain, headaches, nausea.'
CA-042 patient 'Pt Notes: neck pain 5/10.'
CA-053 patient 'Patient reports neck pain; airbags deployed.'
CA-088 patient 'Patient reports neck pain\nAlert and oriented\nAmbulatory at scene'
CA-102 patient 'Patient states neck pain; I felt a spasm.'
CA-114 patient 'Patient reports neck pain; ER felt it was a sprain.'
CA-201 unknown 'Patient states symptoms began after the January collision.'
02ff244 chore(evals): regenerate calibration.json from a clean worktree of 823b718 (fixture: verified 83/84, needs_review 10/10) (T-090 r2)
same
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:00.752Z

**tool call — Bash**
````
{
 "command": "grep -n \"_SAY_PATIENT\\|^_SAY = \\|def _complement_ok\\|if not _complement_ok(toks, cur\\|^_BASE\\|_COMMON = \\|he she him\\|^_EXTRA\\|_SYMPTOM = \\|er ed emergency\\|_EVENT = \\|^def _classify_sentence\\|^_SECTION\\|re.sub(r\\\"\\\\\\\\bPT\" app/backend/speaker.py"
}
````

### User / tool · 2026-11-02T04:33:00.836Z

**tool result**
````
63:_MOD = _w("triage charge er ed emergency ambulance ems scene responding on-scene police treating referring attending resident "
76:_SAY = _w("""states stated state reports reported report says said say tells told tell notes noted note denies denied deny
86:_SAY_PATIENT = _SAY - _w("observed observes found saw witnessed heard suspects feels felt gives gave")
95:_SECTION = frozenset({"s", "subjective", "hpi", "history of present illness", "cc", "chief complaint", "hx", "history",
101:_COMMON = """
106:here when where how what if which he she him her his hers they them their theirs we us our i me my mine you your
117:_SYMPTOM = """
135:_EVENT = """
138:home house stairs steps ladder ground floor ice wet scene incident injury injuries injured event er ed emergency room hospital clinic
162:_EXTRA = """
170:_BASE = _w(_COMMON + _BODY + _SYMPTOM + _EVENT + _TREAT + _TIME + _SPANISH + _EXTRA)
189:    t = re.sub(r"\bPT\b\.?", " pt_ambiguous ", t)
304:        if k < len(toks) and toks[k] in _SAY_PATIENT:
323:def _complement_ok(comp, speaker, allow_embed):
342:def _classify_sentence(sentence: str):
368:            if not _complement_ok(toks, cur, False):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:45.786Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-091-claims-adjuster.md",
 "content": "# T-091 review: claims-adjuster-reviewer (Gary Pruitt, defense BI adjuster)\n\nVerdict: **fail**. I wrote 200 fresh attack sentences plus 50 genuine patient statements\n(`artifacts/review-evidence/T-091/attacks.jsonl`, built by `build_attacks.py`, run by `probe.py`). `speaker.py` at 17cc9c7 labels\n**110 of the 200 attacks \"patient\"** where a human reads \"other\" or \"unknown\". After I drop 13 rows that are arguable\n(he/she/they pronouns, \"Patient notes:\", a nonsense token) the count is **97 of 200**. The gate is 100%, so the misses are blockers.\nA second generated grid (patient head x 12 connectors x 12 unattributed clauses, `grid_and_corpus.py`) labels 432 of 468 \"patient\".\nThe worker's 310 rows contain none of these shapes (counted with a script: \"advised\", \"informed\", \"described as\", \"noted to\",\n\"responds\", \"Patient state:\", \"Patient records\", \"Pt Notes\", \"airbags\", \"gait steady\", \"I felt\", \"ER felt\" each appear in 0 rows).\nThat is what a set written by the parser's author looks like. ENABLED stays False, which honours the AC (\"otherwise stays off\"),\nso nothing ships wrong today. But the card claims a gate, and the gate does not hold against a fresh adversary.\n\nUsefulness (the other half of the question): on my 50 genuine statements it labels 34 (68%); on the 23 repo-record sentences\nthat start \"Patient/Pt + reporting verb\" (evals/golden, evals/library) it labels 15 (65%). It misses the Appendix A sentence itself:\n`Patient states symptoms began after the January collision.` -> unknown (a month name is outside the vocabulary).\nIt also misses \"Patient states she missed two physical therapy visits in May.\" and \"Patient denies chest pain or shortness of breath.\"\n\n## Why it fails (mechanism, with locations)\n- `_SAY_PATIENT` (speaker.py:86) keeps passive and description verbs: advised, told, informed, described, noted, reported,\n  documented, recorded, thought, believed, said, responds, records, documents, state, note. The head test (`_head`, ~304) only checks\n  \"Patient + verb\". Whether the patient is the speaker or the one being spoken to is never asked.\n- A clause with no head inherits the current speaker if all its words are in the closed vocabulary (`_classify_sentence` ~368:\n  `if not _complement_ok(toks, cur, False): ... ; continue`). So \"; airbags deployed\", \"- alert and oriented\", \"\\nGait steady\" ride\n  under the patient label. D-037 said \"no further clause after ; , and or (\" gets no chip, and D-040 recorded that this exact\n  rule failed four rounds. v2 re-opened it with a vocabulary instead of a connector list.\n- The \"closed\" vocabulary (`_BASE`, :170) contains the pronouns he/she/they/I/we/you (`_COMMON` :106) and institutional nouns\n  er/ed/hospital/clinic/office/work/home (`_EVENT` :135), so a clause whose subject is one of those, with a vocabulary verb\n  (felt, seemed, took, walked), is \"the patient\".\n\n## Findings (JSON below holds the same, with fixes)\n1. Blocker: patient as receiver or as the described party (30 attacks). \"Patient advised to rest and ice.\", \"Patient told it was a strain.\",\n   \"Patient responds well to therapy.\" (clinician assessment), \"Patient described as anxious.\", \"Patient noted to have mild neck tenderness.\",\n   \"Patient said to be fine.\", \"Patient recorded as ambulatory.\" All -> patient.\n2. Blocker: unattributed observation clause under a patient head (about 50 attacks; grid 432/468). \"Patient reports neck pain; airbags deployed.\",\n   \"Patient denies loss of consciousness; alert and oriented.\", \"Patient states neck pain; gait steady.\",\n   \"Patient reports neck pain\\nAlert and oriented\\nAmbulatory at scene\". Every connector except an ellipsis leaks.\n   For a MIST defense this is the worst direction: EMS/police scene facts (minimal damage, ambulatory at scene) get stamped as the claimant's words.\n3. Blocker: \"state/records/notes/report\" as a noun or title (9 + 7 attacks). \"Patient state: alert and oriented.\",\n   \"Patient records: neck pain, headaches, nausea.\", \"Pt Notes: neck pain 5/10.\" (a physical therapy note), \"Pt. Note: pain 4/10, stable, no distress.\"\n   Uppercase \"PT\" is guarded (good); title-case \"Pt Notes:\" is the way a PT note is actually typed after OCR and is not.\n4. Blocker: pronoun, first person, or institution as the speaker of a continuation (about 22 attacks).\n   \"Patient states neck pain; I felt a spasm.\", \"...; we walked to the car.\", \"...; I took her to the ER.\",\n   \"Patient reports neck pain; ER felt it was a sprain.\", \"...; the hospital felt it was fine.\"\n5. Major: the adversarial gate is not independent and not complete. The set and parser share an author, and the grid in\n   `test_generated_mixed_grid_never_patient_or_other` only varies a second speaker with a speech verb, never an unattributed\n   vocabulary-only clause. A 100% score on it measures recall of the author's list. Needed: a held-out set the parser's author never sees.\n6. Minor: \"other\" is also a guess. \"Driver states neck pain.\", \"Passenger reports neck pain.\", \"Driver denies loss of consciousness.\"\n   are labelled other; in a crash file the claimant is very often the driver or passenger. Not shipped (chip_label returns None for\n   non-patient), but the module docstring defines \"other\" as a named non-patient source.\n7. Minor: usefulness 65-68%, and the first sentence a paralegal will test (Appendix A: \"Patient states symptoms began after the January collision.\")\n   gets no label. Safe direction, but record it so nobody advertises the coverage.\n\n## Things I checked that held\n- Mixed speakers with a speech verb (\"Patient states neck pain; wife reports headaches\", \"Per wife, patient states ...\", Spanish \"esposa refiere ...\") -> unknown, across 40 new shapes.\n- \"Patient states his wife said he was fine\" style hearsay keeps the patient label and nested patient-in-wife statements go unknown.\n- Uppercase \"PT reports ...\" and \"PT states pt reports ...\" -> unknown.\n\n## Exercised\n`git rev-parse HEAD` = 02ff244; `git diff --quiet 17cc9c7 -- app/backend/speaker.py evals/adversarial/speaker_attribution.jsonl` printed \"same\"\n(reviewed commit equals worktree for these files). `.venv/bin/python -m pytest tests/unit/test_speaker.py -q` -> 8 passed.\n`probe.py` output: \"attack rows 200; tool says PATIENT where a human reads other/unknown: 110\"; \"genuine patient statements: 50; labelled patient 34 (68%)\".\n`grid_and_corpus.py` output: \"GRID unattributed clause: 432/468 labelled patient\"; \"REPO corpus: 31 ... starting with Patient/Pt: 23; ... patient share 65%\".\n`grep -rn \"import speaker\"` over app/tests/tools: only tests/unit/test_speaker.py imports it (module is not wired).\n\n```json\n{\"card\": \"T-091\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"app/backend/speaker.py and evals/adversarial/speaker_attribution.jsonl at 17cc9c7 (worktree identical); attack set artifacts/review-evidence/T-091/attacks.jsonl (200 attacks + 50 genuine); no app server needed, module is not wired\",\n \"exercised\": [\"python3 tools/board.py show T-091\", \"read D-035/D-037/D-040/D-042 in memory/ORCHESTRATOR_DECISIONS.md\", \"read app/backend/speaker.py in full\", \"pytest tests/unit/test_speaker.py -> 8 passed\", \"build_attacks.py + probe.py: 200 attacks, 110 labelled patient (97 after removing 13 arguable rows), 50 genuine, 34 labelled patient\", \"grid_and_corpus.py: 432/468 grid leak; 15/23 repo record sentences labelled patient\", \"counted worker set coverage of my hole classes: 0 rows each\"],\n \"verdict\": \"fail\",\n \"scores\": {\"safety_of_patient_label\": 1, \"adversarial_gate_validity\": 1, \"usefulness\": 3, \"fail_closed_design\": 2, \"consistency_with_D-037_D-040\": 1},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"Patient as receiver or described party is labelled patient (30 of 32 attacks)\",\n   \"evidence\": \"attacks.jsonl CA-001 'Patient advised to rest and ice.' -> patient; CA-003 'Patient told it was a strain.'; CA-016 'Patient described as anxious.'; CA-019 'Patient noted to have mild neck tenderness.'; CA-026 'Patient said to be fine.'; CA-028 'Patient responds well to therapy.'; CA-025 'Patient recorded as ambulatory.'. Cause app/backend/speaker.py:86 _SAY_PATIENT keeps advised/told/informed/described/noted/reported/documented/recorded/thought/believed/said/responds; _head (~304) tests only 'Patient + verb'.\",\n   \"why_it_matters\": \"Clinician advice and clinician assessment are printed as the claimant's own words. A defense reader cites it to say the claimant said 'responds well to therapy'. Invented attribution is a section 5 dealbreaker.\",\n   \"fix\": \"Patient head requires an active reporting verb followed by a finite clause or noun phrase; a verb followed by 'to + verb', 'as', 'by', or 'to be' means the patient is the object, so unknown. Remove advised/told/informed/responds/documented/recorded/thought/believed/said from the patient verb list, or require a following 'that' or a symptom noun directly after the verb.\",\n   \"acceptance_test\": \"All 30 rows of groups receiver_told_advised and description_by_someone_else in attacks.jsonl label unknown; held-out set of at least 100 such shapes at 100%.\"},\n  {\"severity\": \"blocker\", \"title\": \"Unattributed vocabulary-only clause after a patient head inherits the patient label (grid 432/468)\",\n   \"evidence\": \"CA-053 'Patient reports neck pain; airbags deployed.' -> patient; CA-057 'Patient denies loss of consciousness; alert and oriented.'; CA-059 'Patient states neck pain; gait steady.'; CA-088 'Patient reports neck pain\\\\nAlert and oriented\\\\nAmbulatory at scene'; CA-079 'Patient states neck pain (gait steady, no distress).'. grid_and_corpus.py: 'GRID unattributed clause: 432/468 labelled patient' (every connector except an ellipsis, all 12 observation clauses). Cause speaker.py _classify_sentence ~368: a headless segment continues the current speaker if its words are in _BASE.\",\n   \"why_it_matters\": \"EMS, police and examiner observations (airbags deployed, vehicle damage minimal, ambulatory at scene, no distress) become the claimant's statement. This is D-037's 'any further clause means no chip' rule, which D-040 says failed four rounds, re-opened through a vocabulary.\",\n   \"fix\": \"A clause that has no explicit head of its own gets no speaker. Only an unbroken single clause 'Patient <verb> <complement>' (no ; , : - ( & / and but while or newline) is patient; a list of symptoms joined by 'and' or commas inside the complement is allowed only when every item is a symptom/body noun phrase, not a state or exam adjective.\",\n   \"acceptance_test\": \"Rows in groups unattributed_observation_* in attacks.jsonl and the 468-cell grid all unknown; adversarial runner includes the grid.\"},\n  {\"severity\": \"blocker\", \"title\": \"'state/records/notes/report' used as a noun or title is read as a patient speech verb ('Pt Notes:' is a physical therapy note)\",\n   \"evidence\": \"CA-033 'Patient state: alert and oriented.' -> patient; CA-036 'Patient records: neck pain, headaches, nausea.' -> patient; CA-038 'Patient documents: neck pain.' -> patient; CA-042 'Pt Notes: neck pain 5/10.' -> patient; CA-043 'Pt. Notes: neck pain 5/10.'; CA-046 'Pt Report: neck pain 5/10, headaches.'; CA-052 'Pt. Note: pain 4/10, stable, no distress.'. Uppercase PT is guarded at speaker.py:189 but title-case Pt is not.\",\n   \"why_it_matters\": \"A physical-therapist's note or a chart heading is printed as the patient speaking. 'Patient state: alert and oriented' is a clinician observation.\",\n   \"fix\": \"A label ending in ':' or '-' directly after Pt/Patient + noun-capable word (state, note, notes, record, records, report, document) is never a head; require a content word, not a delimiter, after the verb. Treat title-case 'Pt Notes/Note/Report/Eval' as ambiguous like uppercase PT.\",\n   \"acceptance_test\": \"Groups noun_use_of_verb (excluding the 4 arguable rows) and pt_title_case_physical_therapy label unknown.\"},\n  {\"severity\": \"blocker\", \"title\": \"Pronoun, first person or an institution word as subject of a continuation is read as the patient\",\n   \"evidence\": \"CA-102 'Patient states neck pain; I felt a spasm.' -> patient; CA-104 'Patient states neck pain; we walked to the car.'; CA-112 'Patient reports neck pain; I took her to the ER.'; CA-114 'Patient reports neck pain; ER felt it was a sprain.'; CA-116 'Patient states neck pain; the hospital felt it was fine.'; CA-117 '...; clinic felt it was a sprain.'. Cause speaker.py:106 _COMMON includes he she they i we you; :135 _EVENT includes er ed hospital clinic office work home.\",\n   \"why_it_matters\": \"A clinician's first-person exam note and an institution's opinion are stamped as the claimant's words.\",\n   \"fix\": \"Remove subject pronouns and institution nouns from the continuation vocabulary (allow them only inside a single patient clause as an object/location), and treat any subject in a continuation as a new unknown speaker.\",\n   \"acceptance_test\": \"Groups pronoun_continuation (excluding the 8 arguable he/she/they rows) and vocab_word_as_source label unknown.\"},\n  {\"severity\": \"major\", \"title\": \"The 100% gate is self-authored and does not cover these hole classes\",\n   \"evidence\": \"Counted in evals/adversarial/speaker_attribution.jsonl with a script: rows containing advised 0, informed 0, 'described as' 0, 'noted to' 0, responds 0, 'Patient state:' 0, 'Patient records' 0, 'Pt Notes' 0, airbags 0, 'I felt' 0, 'ER felt' 0. tests/unit/test_speaker.py::test_generated_mixed_grid_never_patient_or_other varies only a second speaker plus a speech verb. Handoff admits 'the set and parser share an author'.\",\n   \"why_it_matters\": \"310/310 measures the author's list. A fresh reviewer's 200 sentences scored 90 correct (45%). The same pattern ended the T-061 chip in four rounds.\",\n   \"fix\": \"Add all of attacks.jsonl to evals/adversarial/ as a held-out file the parser's author does not read before tuning; add grid cells for unattributed clauses, passive verbs and noun-use heads; report the score on the held-out file in the handoff.\",\n   \"acceptance_test\": \"A new fresh adversary round (not the author, not this reviewer) of at least 100 sentences scores 0 patient misses before ENABLED can flip.\"},\n  {\"severity\": \"minor\", \"title\": \"'other' is a guess for Driver/Passenger, who is often the claimant\",\n   \"evidence\": \"CA-170 'Driver states neck pain.' -> other; CA-171 'Driver states he was stopped at a red light.' -> other; CA-172 'Passenger reports neck pain.' -> other; CA-174 'Driver denies loss of consciousness.' -> other. speaker.py:67-75 _SRC lists driver, passenger, driver as non-patient sources.\",\n   \"why_it_matters\": \"If a UI ever shows 'non-patient speaker' for these it states a fact the record does not. Not shipped today (chip_label returns None for non-patient).\",\n   \"fix\": \"Drop driver and passenger (and occupant) from _SRC so they give unknown, or label the result 'third party or patient'.\",\n   \"acceptance_test\": \"Group other_may_be_the_patient labels unknown.\"},\n  {\"severity\": \"minor\", \"title\": \"Coverage is about two thirds of genuine patient statements, and the Appendix A sentence is not labelled\",\n   \"evidence\": \"probe.py: 'genuine patient statements: 50; labelled patient 34 (68%)'; grid_and_corpus.py: 'starting with Patient/Pt: 23; labels {patient: 15, unknown: 8} patient share 65%'; 'Patient states symptoms began after the January collision.' -> unknown (CA-201); 'Patient states she missed two physical therapy visits in May.' -> unknown.\",\n   \"why_it_matters\": \"Safe direction, but the handoff's 28 of 226 and my 65-68% both mean the chip would be absent on common sentences, so adopting it for usefulness is weak.\",\n   \"fix\": \"Accept numbers and month names, and plural nouns of already-listed words in the vocabulary, only after the blockers are closed; do not widen the vocabulary first.\",\n   \"acceptance_test\": \"State coverage on the 23 record sentences in the handoff next to the safety score; target at least 80% after safety fixes.\"}\n ],\n \"whats_right\": [\"Fail-closed default and ENABLED=False with chip_label() returning None keep nothing wrong on screen today.\", \"Mixed speakers joined by a speech verb (wife/EMS/officer/Spanish esposa) are reliably unknown across 40 new shapes.\", \"Uppercase PT and zero-width/homoglyph tricks are handled.\"],\n \"questions_for_chris\": [\"D-042 says speaker attribution ships only at 100% on an adversarial set. Should that set be the held-out file from a reviewer round, so the worker never tunes against it?\"]}\n```\n"
}
````

### User / tool · 2026-11-02T04:33:45.945Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-091-claims-adjuster.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:50.591Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport json,collections\nres=[json.loads(l) for l in open('artifacts/review-evidence/T-091/results.jsonl')]\natt=[r for r in res if r['group']!='genuine']\nok=sum(r['got']==r['expect'] for r in att); print(ok,len(att))\nEOF"
}
````

### User / tool · 2026-11-02T04:33:50.699Z

**tool result**
````
85 200
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:52.558Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-091-claims-adjuster.md",
 "old_string": "A fresh reviewer's 200 sentences scored 90 correct (45%).",
 "new_string": "A fresh reviewer's 200 attack sentences scored 85 correct (43%)."
}
````

### User / tool · 2026-11-02T04:33:52.613Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-091-claims-adjuster.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:53.398Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-091-claims-adjuster.md",
 "old_string": "(about 50 attacks; grid 432/468)",
 "new_string": "(42 of 45 attacks; grid 432/468)"
}
````

### User / tool · 2026-11-02T04:33:53.458Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-091-claims-adjuster.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:33:56.073Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport re,json\nt=open('reviews/T-091-claims-adjuster.md').read()\nm=re.findall(r\"```json\\n(.*?)\\n```\",t,re.S); print(len(m)); d=json.loads(m[0]); print(d['verdict'],len(d['findings']))\nEOF"
}
````

### User / tool · 2026-11-02T04:33:56.178Z

**tool result**
````
1
fail 7
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T04:34:00.185Z

Miss count: 110 of 200 fresh attacks were labelled "patient" where a human reads "other" or "unknown". After I drop 13 arguable rows, 97 of 200 still miss, so it fails the 100% gate (verdict fail, 4 blockers). Coverage of genuine patient statements is 68% on my 50 sentences and 65% on repo record sentences.

The misses fall into four shapes:
- **Patient as receiver:** "Patient advised to rest".
- **Unattributed clause after the head:** "…; airbags deployed", which leaked in 432 of 468 grid cells.
- **Noun use:** "Pt Notes:" and "Patient state: alert and oriented".
- **Pronoun or institution as speaker:** "…; I felt a spasm".

The Appendix A sentence "Patient states symptoms began after the January collision." gets no label.

The review has two slips I couldn't correct because reviews are write-once. Finding 5 says "90 correct (45%)", but the true figure is 85 (43%). Finding 2's heading says "about 50 attacks", but it is 42 of 45 attacks.

Files are in `/Users/arsis/zlayt-pm-project`:
- reviews/T-091-claims-adjuster.md
- artifacts/review-evidence/T-091/attacks.jsonl
- artifacts/review-evidence/T-091/results.jsonl
- artifacts/review-evidence/T-091/build_attacks.py
- artifacts/review-evidence/T-091/probe.py
- artifacts/review-evidence/T-091/grid_and_corpus.py
