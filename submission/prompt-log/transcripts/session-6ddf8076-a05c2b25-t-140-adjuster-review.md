# Subagent: T-140 adjuster review (T-140 adjuster review)

Source: `agent-a05c2b25de1246930.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T13:29:02.845Z

As the bodily-injury adjuster and defense-counsel adversary, attack board card T-140 in /Users/arsis/zlayt-pm-project; read it with `python3 tools/board.py show T-140`. It fixes billed totals in the letter: ledger totals and balance-due lines were being counted as charges, and lib11 claimed $10,906 instead of $6,000.

Run the app from a `git archive HEAD` copy in your scratchpad on a spare port: fixture backend, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad. On lib11 and every other library case with billing, accept all charges, export, and check the "Billed charges stated in these records" total against the records by hand.

Then paste a synthetic ledger of your own, labelled SYNTHETIC, built to inflate the total. Include:
- running totals;
- a 'Statement total';
- a prior-balance carry-forward;
- duplicate lines on two statements;
- payments shown as negatives.

Check whether any of these get counted.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-140-claims-adjuster.md with a ```json block of real values: card, persona claims-adjuster-reviewer, model claude-opus-5-5, verdict, findings, exercised. Stop your server by PID. Reply in 2 lines.

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:05.971Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-140; cat .claude/agent-memory/claims-adjuster-reviewer/feedback_reviewer_write_and_parse_guards.md .claude/agent-memory/claims-adjuster-reviewer/reference_spare_port_app_server.md .claude/agent-memory/claims-adjuster-reviewer/project_gate_m2_curated_vs_recorded.md .claude/agent-memory/claims-adjuster-reviewer/feedback_review_commit_not_worktree.md",
 "description": "Show card T-140 and read relevant memory notes"
}
````

### User / tool · 2026-11-02T13:29:06.123Z

**tool result**
````
---
id: "T-140"
title: "GATE-M2 blocker: ledger totals and balance-due lines classified as charges (lib11 $2,740 total + $2,166 balance counted; letter says $10,906 vs true $6,000)"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T13:03:00Z"
updated_at: "2026-11-02T13:28:52Z"
claimed_by: "backend"
claimed_at: "2026-11-02T13:03:28Z"
rounds: 0
commits: ["78554d1a4ef2b442eb6902b6f89517a3ae39b4ad"]
reviews: []
ac:
  - {"n": 1, "text": "code rule: an amount on a total/subtotal/balance/amount due/paid/payment/adjustment/credit line is never class 'charge' (goes to internal notes 'Amounts not totaled' with its reason), whatever the judge says; unit tests incl. lib11", "done": true, "evidence": "tests/unit/test_amounts_t140.py::test_lib11_ledger_classes + test_total_balance_payment_adjustment_labels_are_never_charges (13 labels) + test_word_must_be_the_label_not_anywhere_in_the_sentence + test_column_label_of_a_table pass; reasons in internal notes via amounts.not_totaled_reason (export.py hunk, committed in 5f7ef96)"}
  - {"n": 2, "text": "code cross-check: a charge equal to the sum of other charges in the same record/statement is flagged as a likely total, not totaled; test", "done": true, "evidence": "tests/unit/test_amounts_t140.py::test_cross_check_flags_a_charge_equal_to_the_others, test_cross_check_needs_two_other_charges_and_one_record pass"}
  - {"n": 3, "text": "lib11 accept-all export total = $6,000.00; eval adds a library total check vs expected", "done": true, "evidence": "tests/unit/test_amounts_t140.py::test_lib11_accept_all_export_total_is_6000 (HTTP accept-all -> 'Billed charges stated in these records: $6,000.00') and test_library_accept_all_total_equals_expected pass; evals/library_report.py adds an accept-all total column using export.build_export"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:03:19Z orchestrator: assigned: backend
- 2026-11-02T13:03:28Z backend: claimed
- 2026-11-02T13:28:48Z backend: AC 1 checked: tests/unit/test_amounts_t140.py::test_lib11_ledger_classes + test_total_balance_payment_adjustment_labels_are_never_charges (13 labels) + test_word_must_be_the_label_not_anywhere_in_the_sentence + test_column_label_of_a_table pass; reasons in internal notes via amounts.not_totaled_reason (export.py hunk, committed in 5f7ef96)
- 2026-11-02T13:28:48Z backend: AC 2 checked: tests/unit/test_amounts_t140.py::test_cross_check_flags_a_charge_equal_to_the_others, test_cross_check_needs_two_other_charges_and_one_record pass
- 2026-11-02T13:28:48Z backend: AC 3 checked: tests/unit/test_amounts_t140.py::test_lib11_accept_all_export_total_is_6000 (HTTP accept-all -> 'Billed charges stated in these records: $6,000.00') and test_library_accept_all_total_equals_expected pass; evals/library_report.py adds an accept-all total column using export.build_export
- 2026-11-02T13:28:48Z backend: moved in_progress -> in_review
- 2026-11-02T13:28:52Z orchestrator: review dispatched: staff-engineer-reviewer, claims-adjuster-reviewer

## Handoff
What changed: amounts.classify now returns unclear when the figure's line label or table column heading is a total/subtotal/balance/amount due/payment/adjustment/write-off/credit word (last few words before the figure only; FL47 UB-04 column stays a charge, Rev 0001 is a total); extract_amounts flags a charge equal to the sum of the other >=2 charges of the same record as a likely total; export notes print the reason (amounts.not_totaled_reason, recomputed from the quote, no new stored field; export.py hunk was swept into 5f7ef96). evals/library_report.py: new 'accept-all total' column via build_export; evals/run.py check_must_not amount_value counts only class charge (all bad_examples are class charge; lib11 M1 false hit gone). api.md paragraph added. Commit 78554d1a4ef2b442eb6902b6f89517a3ae39b4ad (+ fixtures: 7 J2 answers recorded with --fill-missing for the changed classes). How verified: new tests (31) + test_amounts/billing/reclassify/export/t114 pass; full unit suite on a HEAD copy with my files: only git-less eval_runner tests and 2 other-worker tests fail; fixture eval amount_recall 1.000, blocker list unchanged (4_no_invented_facts, live-only); library report lib11 accept-all ok $6,000.00, no M1; lib01,02,03,07,08,12,13,14,15 ok. What is left: lib04, 05, 06, 09, 10 show WRONG accept-all totals for older reasons (lib10: EOB 'Amount billed $8,023.50' still charge, M1) not touched; evals/reports/library-latest.md not regenerated (needs clean tree, qa). What surprised me: Haiku J2 answers disagree/SHOULD_BE_CHARGE on the unclear totals and payments, so the code rule is the only guard; reclassify (D-042) can still promote a 'Total billed' wording by the paralegal with the judge, unchanged; test_amounts 'Total billed: $310.00' now expects unclear (reason: total line).

---
name: reviewer-write-and-parse-guards
description: Reviewer tooling limits seen on T-111 - Write to scratchpad is blocked by reviewer-write-guard (probe scripts go in artifacts/review-evidence/); bash-guard fails closed on escaped backticks and on < or > in a command.
metadata:
  type: feedback
---

Probe scripts must be written under artifacts/review-evidence/ (Write to the session scratchpad is denied by reviewer-write-guard,
even though the scratchpad is the normal temp dir). Extracting a git archive into the scratchpad with Bash still works.

Bash commands containing escaped backticks (\`\`\`) or literal < and > are denied: board-guard reports 'could not parse command safely'
and fails closed. Build the fence with chr(96)*3 in a python -c one-liner, and avoid < and > in grep patterns.

**Why:** both hit during T-111 (2026-11-02); the guard blocked a legitimate read-only command.

**How to apply:** before a probe, pick artifacts/review-evidence/ as the script home. For JSON validation of a review, parse it with
python -c and chr(96) fences; do not put backslash-backtick in the command.

Related: [[reference_spare_port_app_server]], [[feedback_reviews_write_once]].
---
name: spare-port-app-server
description: How a reviewer runs its own app server and e2e tests on a spare port without touching the operator's app on 7860; bash-guard and macOS quirks hit on 2026-11-01
metadata:
  type: reference
---

Recipe (worked on T-069, 2026-11-01): from an extracted commit tree (git archive), start the app with
`env HOST=127.0.0.1 PORT=7871 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=<scratch>/app.sqlite3 <repo>/.venv/bin/python -m app.main`
(app/main.py reads HOST and PORT; the default port 7860 belongs to the operator's app, so never use it). Health: GET /api/health.
Point e2e at it with `E2E_BASE_URL=http://127.0.0.1:7871 .venv/bin/python -m pytest tests/e2e/test_edit.py -p no:cacheprovider -v`
(tests/e2e/conftest.py defines its own `page` fixture on sync Playwright, so pytest-playwright is not needed).
Stop it by PID from `lsof -nP -t -iTCP:7871 -sTCP:LISTEN` and confirm the port is down.

**Why:** tools/serve_app.sh hard-codes :7860 in a tmux window, and the operator's app lives there.

**How to apply:** pass the tree root as argv to probe scripts (sys.path.insert); keep ZLAYT_DB in scratch, not in the repo.

Quirks on this machine:
- `timeout` is not installed (macOS). Use the tool timeout parameter instead.
- The board-guard Bash hook reads `<=`, `>=` and `<` in a command as a redirect and blocks the whole call. Use `sed -n N,Mp` or grep without comparison operators.
- `rm -rf` inside the session scratchpad was denied by the permission system on 2026-11-01. Do not try a workaround; leave the scratch copies and say so in the reply.
- `lsof` prints a harmless "child setpgid" error from the shell on some calls.
---
name: gate-m2-curated-vs-recorded
description: GATE-M2 (0c24f5f) adjuster review - curated sample is clean; recorded library output leaks per-visit rates and dismissed charges into letter_text via entry quotes (blocker)
metadata:
  type: project
---

GATE-M2 at 0c24f5f, verdict fail. The sample case replays the CURATED fixture set, which is hand-built to match the golden answers (evals.run refuses it, D-029), so the sample is clean on every attack-list item.
The library cases replay recorded model output. There the extract prompt (extract_v1.md "plan or charge") puts "Charge per visit $140/$120"
and "ED charge $3,915" into entry summaries and quotes. Result: rates appear in letter_text, against R-CH-7's "letter_text has no $185" and against R-EX-8/D-019.
A charge the paralegal dismissed is still quoted in the letter, while the notes list the same provider under "Bills to request".

**Why:** a gate verdict built on the sample alone would have passed. The real model behaviour only shows on non-curated cases.

**How to apply:** at every gate, run at least two library cases (POST /api/cases {library: id}, needs ZLAYT_MODE=local), accept everything,
then dismiss amounts and re-export. Grep letter_text for '$', 'per visit' and any dismissed figure. Next round, check whether rate and dismissed-amount stripping holds on lib01/lib03.
Also open: lib03 notes say "visit count not stated" although record 6 says 31 visits (minor); lib03 plan-vs-31-visits conflict is missing (minor).

Related: [[reference_spare_port_app_server]], [[feedback_review_commit_not_worktree]].
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
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:06.371Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/claims-adjuster.md"
}
````

### User / tool · 2026-11-02T13:29:06.380Z

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

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:08.342Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 && git status --short | head -30 && ls evals/ app/ && ls evals/library* 2>/dev/null; ls app/backend | head -50",
 "description": "Check git HEAD, status and app layout"
}
````

### User / tool · 2026-11-02T13:29:08.510Z

**tool result**
````
78554d1 fix(backend): T-140 a total, balance, payment or adjustment line is never class charge; a charge equal to the others is a likely total; library accept-all total check
5f7ef96 fix(backend): T-139 no dollar amount reaches the carrier letter through entries; CHARGE_TEXT_IN_ENTRY holds them out; dismissed charge not under Bills to request; letter-level eval check
7d3ca35 fix(backend): T-146 a timed-out re-run keeps every previous item and decision
b604ff2 fix(backend): T-145 an entry whose judge 1 never ran is needs_review, JUDGE_NOT_RUN, and batch accept refuses it
5a388d5 fix(backend): T-143 r2 uncovered lists every sentence no entry covers; only anchored administrative lines skipped; form answer carries its question
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
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/lexicon_scan.py
 M app/frontend/dom.js
 M app/frontend/export.js
 M app/frontend/flags.js
 M app/frontend/review.css
 M app/frontend/review.js
 M app/frontend/stepper.js
 M app/frontend/timeline.js
 M board/activity.jsonl
app/:
README-arch.md
__init__.py
__pycache__
backend
db
frontend
llm
main.py
pipeline.py

evals/:
__init__.py
__pycache__
adversarial
golden
heldout_audit.py
j3_controls.py
letter_check.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
reports
run.py
evals/library_build_v2.py
evals/library_report.py

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
__init__.py
__pycache__
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
case_list.py
charge_text.py
confidence.py
conflict_candidates.py
conflicts.py
credibility.py
date_convention.py
dates.py
dismissal_patterns.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judge_guard.py
judges.py
language.py
lexicon.py
lexicon_scan.py
narrative.py
overlap.py
pdf_checks.py
pdf_hidden.py
pdf_ocr.py
pdf_routes.py
pdf_text.py
pipeline.py
present.py
reclassify.py
rejudge.py
review.py
schemas.py
sentences.py
spanish.py
spanish_text.py
speaker.py
split_llm.py
store.py
summary_trim.py
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:12.012Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/tree && cd /Users/arsis/zlayt-pm-project && git archive HEAD | tar -x -C $S/tree && ls $S/tree && git show --stat HEAD | head -40",
 "description": "Extract HEAD tree into scratchpad and show commit stat"
}
````

### User / tool · 2026-11-02T13:29:12.803Z

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
commit 78554d1a4ef2b442eb6902b6f89517a3ae39b4ad
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:28:38 2026 -0600

    fix(backend): T-140 a total, balance, payment or adjustment line is never class charge; a charge equal to the others is a likely total; library accept-all total check
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/amounts.py                             |  86 +++++++++++-
 evals/library_report.py                            |  30 ++++-
 ...632438df628eaad4a04089f7c0933370f01aac673d.json |  11 ++
 ...5cd62fac96106102e1d17b3f2a86e0c988f3ffb97a.json |  11 ++
 ...14e3a7a1f8b426056caeb5ceedaa23fbea62372085.json |  11 ++
 ...974c131ed8db9d24addab2a4b2d2ec802524150626.json |  11 ++
 ...f54380b7b5e13fc01c57edd33623ae5074ec2fbc01.json |  11 ++
 ...3341a62a6ac4a02ea2d394e8f21ad125cea2dbf4a6.json |  11 ++
 ...b958a54f0e9fdcaba1fb11cdc5a07857ab5bfc406e.json |  11 ++
 tests/unit/test_amounts.py                         |   3 +-
 tests/unit/test_amounts_t140.py                    | 146 +++++++++++++++++++++
 11 files changed, 334 insertions(+), 8 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:14.240Z

**tool call — Bash**
````
{
 "command": "git show HEAD -- app/backend/amounts.py",
 "description": "Show T-140 diff to amounts.py"
}
````

### User / tool · 2026-11-02T13:29:14.333Z

**tool result**
````
commit 78554d1a4ef2b442eb6902b6f89517a3ae39b4ad
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:28:38 2026 -0600

    fix(backend): T-140 a total, balance, payment or adjustment line is never class charge; a charge equal to the others is a likely total; library accept-all total check
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/amounts.py b/app/backend/amounts.py
index 00d8004..5ffad15 100644
--- a/app/backend/amounts.py
+++ b/app/backend/amounts.py
@@ -96,10 +96,59 @@ def _label(excerpt: str, start: int) -> str:
     return " ".join((clauses[-1] if clauses else "").split()[-6:])
 
 
+# T-140 (GATE-M2 blocker): an amount on a total, subtotal, balance, amount due, payment, adjustment, write-off or credit line is never a charge, so
+# it never reaches the letter total. The word must BE the amount's label (the last few words before the figure in its clause, or its table column
+# heading), not merely appear in the sentence. Order matters only for the reason shown: a total beats a balance beats a payment beats an adjustment.
+_NC_KINDS = (
+    ("total", r"(?:grand\s+|sub[\s-]?)?total", 3, "Total or subtotal line: it repeats the charges listed with it, so it is not totaled."),
+    ("balance", r"balance|amount\s+(?:due|owed)|amt\.?\s+due|(?:payment|now|total)\s+due|owed|outstanding", 5,
+     "Balance or amount due: worked out from charges, payments and adjustments, not a charge."),
+    ("payment", r"paid|payments?|pmts?|co-?pay(?:ment)?s?", 5, "Payment: money received, not a charge."),
+    ("adjustment", r"adjust(?:ment|ments|ed)?|write-?offs?|credits?|discounts?|contractual|courtesy", 5,
+     "Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges."))
+_NC_RX = [(k, re.compile(rf"\b(?:{w})\b(?:\s+[^\s$\d]+){{0,{n}}}[\s:=(\-]*$", re.IGNORECASE), why) for k, w, n, why in _NC_KINDS]
+_UB_LINE = re.compile(r"\bFL\s?-?47\b", re.IGNORECASE)
+_UB_TOTAL = re.compile(r"\brev(?:enue)?\s+(?:code\s+)?0001\b", re.IGNORECASE)      # UB-04 revenue code 0001 is the claim's total line
+_CELL_SPLIT = re.compile(r"\t|\|| {2,}")
+
+
+def label_reason(label: str):
+    """(kind, reason) when the label text ends in a total, balance, payment or adjustment word, else None. A word earlier in the sentence than the last
+    few label words does not count ('Total of 12 visits billed $2,150' labels a charge)."""
+    t = (label or "").strip()
+    if not t:
+        return None
+    if _UB_TOTAL.search(t):
+        return _NC_KINDS[0][0], _NC_KINDS[0][3]
+    if _UB_LINE.search(t):          # UB-04 field 47 is the 'Total Charges' COLUMN: each revenue-code line carries one, so the words name a column, not a total line
+        return next(((k, why) for k, rx, why in _NC_RX if k != "total" and rx.search(t)), None)
+    return next(((k, why) for k, rx, why in _NC_RX if rx.search(t)), None)
+
+
+def _column_label(excerpt: str, start: int) -> str:
+    """Table heading above the figure: the header line is the nearest non-blank line above the figure's line, with no digits and the same number of
+    cells as the figure's line (cells split at a tab, a bar or two or more spaces). '' when the text is not laid out as columns."""
+    ls = excerpt.rfind("\n", 0, start) + 1
+    le = excerpt.find("\n", start)
+    row = excerpt[ls:len(excerpt) if le < 0 else le]
+    cells = [(m.start(), m.end()) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", row)]
+    idx = next((i for i, (a, b) in enumerate(cells) if a <= start - ls < b), None)
+    prev = [ln for ln in excerpt[:ls].split("\n") if ln.strip()]
+    if idx is None or not prev or len(cells) < 2 or re.search(r"\d", prev[-1]):
+        return ""
+    heads = [h.strip() for h in _CELL_SPLIT.split(prev[-1]) if h.strip()]
+    return heads[idx] if len(heads) == len(cells) else ""
+
+
+def _non_charge(excerpt: str, amount: dict):
+    """(kind, reason) when the amount's line label or column heading names a total, balance, payment or adjustment, else None."""
+    return label_reason(_label(excerpt, amount["start"])) or label_reason(_column_label(excerpt, amount["start"]))
+
+
 def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
     """charge | rate | estimate | damages | unclear. First match wins (ADR-011): injection, unreadable, rate, estimate, damages,
-    billing statement, charge label, else unclear. `source` (the record's header label) is optional; when given, the statement rule
-    needs it to be a billing document."""
+    total/balance/payment/adjustment label (T-140: unclear, never a charge), billing statement, charge label, else unclear. `source` (the record's
+    header label) is optional; when given, the statement rule needs it to be a billing document."""
     if injection or amount.get("cents") is None:
         return "unclear"
     label = _label(excerpt, amount["start"])
@@ -110,6 +159,8 @@ def classify(excerpt: str, amount: dict, injection: bool = False, source: str =
         return "estimate"
     if any(e["regex"].search(label) for e in lexicon.code_list("damages")):
         return "damages"
+    if _non_charge(excerpt, amount):
+        return "unclear"
     if _STATEMENT.search(label) and (source is None or _is_billing_source(source)):
         return "charge"
     if _CHARGE_END.search(label):
@@ -117,6 +168,32 @@ def classify(excerpt: str, amount: dict, injection: bool = False, source: str =
     return "unclear"
 
 
+def _likely_totals(rows: list) -> set:
+    """Indexes (into `rows`, dicts with cls, cents) of charges that equal the sum of the OTHER charges of the same record, when there are at least two
+    others: a total printed without a total word. The check runs on one record's figures, never across records."""
+    ch = [i for i, a in enumerate(rows) if a["cls"] == "charge" and a.get("cents") and not a.get("injection")]
+    total = sum(rows[j]["cents"] for j in ch)
+    return {i for i in ch if len(ch) >= 3 and total - rows[i]["cents"] == rows[i]["cents"]}
+
+
+def _usd(cents: int) -> str:
+    return f"${cents // 100:,}.{cents % 100:02d}"
+
+
+def not_totaled_reason(excerpt: str, raw: str, cents, source: str = None):
+    """Why a figure in `excerpt` is not a charge (plain words for the internal notes): a total, balance, payment or adjustment label, or the equal-to-the-others
+    check. None for an ordinary figure. Recomputed from the quote, so nothing extra is stored."""
+    amts = find_amounts(excerpt or "")
+    for a in amts:
+        if a["raw"] == raw and a["cents"] == cents and _non_charge(excerpt, a):
+            return _non_charge(excerpt, a)[1]
+    rows = [{**a, "cls": classify(excerpt, a, source=source)} for a in amts]
+    for i in _likely_totals(rows):
+        if rows[i]["raw"] == raw and rows[i]["cents"] == cents:
+            return f"Equals the sum of the other charges in this record: likely a total, not totaled ({_usd(cents)})."
+    return None
+
+
 def _is_billing_source(source: str) -> bool:
     return any(e["id"] == "billing_document" and e["regex"].search(source or "") for e in lexicon.code_list("non_encounter"))
 
@@ -169,7 +246,10 @@ def extract_amounts(records: list, separate=frozenset()) -> list:
             continue
         base = (r.get("char_start") or 0) + (r["text"].find(r["excerpt"]) if r.get("text") and r["excerpt"] in r["text"] else 0)
         found = [{**a, "cls": classify(r["excerpt"], a, injection=bool(r.get("injection_tag")), source=r.get("source"))}
-                 for a in find_amounts(r["excerpt"])] + damages_mentions(r["excerpt"])
+                 for a in find_amounts(r["excerpt"])]
+        for i in _likely_totals([{**a, "injection": bool(r.get("injection_tag"))} for a in found]):      # T-140: a charge equal to the others is a total
+            found[i]["cls"] = "unclear"
+        found += damages_mentions(r["excerpt"])
         for a in sorted(found, key=lambda x: x["start"]):
             rows.append({"record_no": r["n"], "text": r["excerpt"], "date": r.get("date_iso"), "provider": r.get("source"), "raw": a["raw"], "cents": a["cents"],
                          "cls": a["cls"], "start": base + a["start"], "end": base + a["end"], "injection": bool(r.get("injection_tag"))})
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:15.135Z

**tool call — Bash**
````
{
 "command": "cat evals/library/case_lib11_priors_and_ledger.txt; cat evals/library/case_lib11_priors_and_ledger.expected.json | head -80",
 "description": "Read lib11 records and expected answers"
}
````

### User / tool · 2026-11-02T13:29:15.223Z

**tool result**
````
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-03-04
Source: Dr. Hesper Alderton, primary care
Excerpt: "Annual visit. History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy. Problem list: hypertension, type 2 diabetes, chronic low back pain. Low back pain 3/10 today."

=== Record 2 ===
Date: 2026-03-18
Source: Ashgrove Fire-Rescue run report
Excerpt: "Passenger vehicle struck from behind. Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED."

=== Record 3 ===
Date: 2026-03-18
Source: Wexcombe Memorial ED
Excerpt: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture. ED charge: $3,260."

=== Record 4 ===
Date: 2026-03-26
Source: Pellingham and Rook PLLC, correspondence (letter of protection)
Excerpt: "Letter of protection to Fennimoor Spine Clinic. This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending. Please send complete records and an itemized statement."

=== Record 5 ===
Date: 2026-03-27
Source: Fennimoor Spine Clinic, new patient
Excerpt: "Patient referred by attorney. Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly."

=== Record 6 ===
Date: 3/27/26
Source: Fennimoor Spine Clinic, new patient intake form (OCR text)
Excerpt: "Date of injury: 3/l8/26. How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7. Signed 3/27/2G."

=== Record 7 ===
Date: 2026-04-24
Source: Fennimoor Spine Clinic, visit 8
Excerpt: "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued."

=== Record 8 ===
Date: 2026-05-29
Source: Fennimoor Spine Clinic, visit 14
Excerpt: "Neck pain 4/10, low back pain 5/10. Care continues."

=== Record 9 ===
Date: 2026-06-15
Source: Fennimoor Spine Clinic, itemized ledger
Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection."
{
  "schema_version": "golden/1",
  "case_id": "case_lib11_priors_and_ledger",
  "synthetic": true,
  "input_file": "case_lib11_priors_and_ledger.txt",
  "description": "Library L11 (P5+P2). Rear-end collision two weeks after an annual primary-care visit that lists two earlier car accidents, a chronic low back problem and a baseline back pain score. Attorney-referred spine clinic under a letter of protection, a scanned intake form (OCR text) answering 'prior accidents: No', and an itemized ledger with charges, a payment, a courtesy adjustment and a balance. Only stated charges count; payment, adjustment and balance are listed unclear.",
  "stress_types": [
    "intake_denies_prior_accidents",
    "prior_accidents_in_older_note",
    "baseline_back_pain_before_accident",
    "itemized_ledger_billed_adjusted_paid",
    "letter_of_protection",
    "ocr_noise_text",
    "attorney_referral",
    "balance_double_count_trap"
  ],
  "records": [
    {
      "record_no": 1,
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
      "kind": "encounter",
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
      "kind": "encounter",
      "source": "Fennimoor Spine Clinic, visit 14"
    },
    {
      "record_no": 9,
      "raw_date": "2026-06-15",
      "date": "2026-06-15",
      "kind": "billing_statement",
      "source": "Fennimoor Spine Clinic, itemized ledger"
    }
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:17.921Z

**tool call — Bash**
````
{
 "command": "sed -n 1,200p evals/library_report.py | grep -n \"def \\|accept\\|build_export\\|post\\|api/\" | head -60; grep -n \"^#\\|^##\\|POST\\|GET\" memory/contracts/api.md | head -80",
 "description": "Survey library report and API contract endpoints"
}
````

### User / tool · 2026-11-02T13:29:18.129Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:19.402Z

**tool call — Bash**
````
{
 "command": "sed -n 14,60p memory/contracts/api.md | cut -c1-260",
 "description": "Read API endpoint index"
}
````

### User / tool · 2026-11-02T13:29:19.483Z

**tool result**
````
## Endpoint index
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | backend, demo mode, models, limits, banner text |
| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
| GET | `/api/cases/{token}` | the whole case for the review screen |
| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
| GET | `/api/cases/{token}/status` | stage and progress |
| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
| GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |
| POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |
| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks a
| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amo
| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judge
| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMAR
| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRME
| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `
| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconciled rows, skipped records (an EOB service row is a line); no s
| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
| GET | `/api/calibration` | T-099 read-only measured calibration (aggregate counts only, no case token, demo-safe): the T-096 shape in `calibration`, or `null` with `status` `missing`/`invalid`. See the section below |

---

## GET /api/health
```json
{ "ok": true, "version": "0.1.0", "synthetic_only": true,
  "banner": "Synthetic data only — never paste real records",
  "backend": "fixture", "demo_mode": true, "live_enabled": false,
  "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
  "limits": {"max_chars": 60000, "max_records": 40},
  "retention_hours": 24,
  "ai_banner": "Summaries and flags are drafted by AI and checked by code; you decide every item",
  "sample_available": true }
```
`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local u

## POST /api/cases
Request: `text` (pasted or file contents; `.txt` only, client-side read) **or** `sample: true`.
```json
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:24.540Z

**tool call — Bash**
````
{
 "command": "grep -n \"environ\\|getenv\" app/main.py app/backend/api.py app/llm/*.py | cut -c1-200 | head -40",
 "description": "Find environment variables the app reads"
}
````

### User / tool · 2026-11-02T13:29:24.629Z

**tool result**
````
app/main.py:14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
app/backend/api.py:80:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:94:    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh
app/backend/api.py:105:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
app/backend/api.py:107:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
app/backend/api.py:117:        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
app/backend/api.py:123:        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
app/backend/api.py:359:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py:384:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py:583:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
app/llm/provider.py:27:    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
app/llm/provider.py:28:    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
app/llm/provider.py:89:    return os.environ.get("RECORD_FIXTURES") == "1" or os.environ.get("LLM_FIXTURE_RECORD") == "1"
app/llm/audited.py:131:    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:28.441Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; lsof -nP -iTCP:7873 -sTCP:LISTEN; cd $S/tree && env HOST=127.0.0.1 PORT=7873 LLM_BACKEND=fixture ZLAYT_MODE=local ZLAYT_DB=$S/app.sqlite3 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main 1>$S/server.log 2>&1 &\nsleep 4; curl -s http://127.0.0.1:7873/api/health; echo; lsof -nP -t -iTCP:7873 -sTCP:LISTEN",
 "description": "Start app from HEAD tree on port 7873 and check health"
}
````

### User / tool · 2026-11-02T13:29:32.738Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every item","sample_available":true}
88162
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:35.921Z

**tool call — Bash**
````
{
 "command": "grep -n \"library\\|\\\"amounts\\\"\\|review_status\\|\\\"action\\\"\" memory/contracts/api.md | cut -c1-240 | head -40; sed -n 20,34p evals/library_report.py",
 "description": "Find case body shapes for library and amount review"
}
````

### User / tool · 2026-11-02T13:29:36.054Z

**tool result**
````
10:- Every item has `state` (system: `verified` | `needs_review` | `rejected`), `reasons[]` (codes), `why` (one template sentence), `review_status` (human: `pending` | `accepted` | `edited` | `dismissed`), and `ladder` (D.4).
26:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwi
40:| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
108:Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entr
123:  "stages": ["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],
125:  "counts": {"entries": 9, "amounts": 3, "flags": 1},
155:      "review_status": "pending", "edited": null, "duplicate_note": null,
166:        "human": {"action": null, "edited_text": null, "at": null} }
168:  "amounts": [
172:      "review_status": "pending", "edited": null, "duplicate_note": null,
177:        "state": "verified", "human": {"action": null, "edited_text": null, "at": null} } },
182:      "review_status": "pending", "edited": null, "duplicate_note": null, "accept_effect": "acknowledge", "judge_required_for_export": false,
186:        "state": "needs_review", "human": {"action": null, "edited_text": null, "at": null}} } ],
206:      "review_status": "pending", "edited": null,
209:        "judge": null, "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} },
220:      "review_status": "pending", "edited": null,
223:        "judge": null, "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} },
231:      "review_status": "pending", "edited": null,
236:        "state": "verified", "human": {"action": null, "edited_text": null, "at": null}} } ],
323:  "events": [ {"action": "accept", "at": "2026-11-02T01:05:00Z"} ] }
331:  { "action": "accept" },
332:  { "action": "dismiss", "note": "false positive" },
333:  { "action": "reset" },
334:  { "action": "edit", "edits": { "summary": "Discharged from physical therapy after two missed appointments; pain 3/10." } },
335:  { "action": "edit", "edits": { "excerpt": "Discharged from PT after two missed appointments. Pain 3/10." } },
336:  { "action": "edit", "edits": { "note": "Ask client about the 2023 episode." } }
339:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; its class changes onl
351:{ "item": { "id": "e3", "review_status": "edited", "state": "needs_review", "reasons": ["JUDGE_UNAVAILABLE"],
360:**An edit that is still `needs_review` is not decided (T-134; D-045b, D-051; paralegal pass 4 M2).** Saving the edit stays as above (`review_status: "edited"`, `state: "needs_review"`), but until the paralegal says she compared it with 
361:- Item view: every entry has `edit_to_check` (bool), true when `review_status` is `edited`, `state` is `needs_review` (any reason: `JUDGE_UNAVAILABLE`, `JUDGE_PARTIAL`, `OCR_DERIVED`, a translation label) and the entry has an edited `su
362:- Her explicit **Accept** on it (the UI's "I compared it with the quote") is `{action: "accept"}`: `review_status` becomes `accepted`, `state` stays `needs_review` with its reasons, `edit_to_check` is false. Accept is bound by the code 
379:- On success the item goes back to `review_status: pending` (a reset event is logged first if she had decided it; her earlier decision was about the old meaning) and must be accepted again. Its state is recomposed: a judged charge is `v
380:- Audit: one `review_events` row per reclassification. The `action` is `edit` (the table's CHECK has no `reclassify` yet; db card requested) and the local-mode `after` payload carries `{event: "reclassify", kind, wording, judge_verdict,
385:{ "item":   { "id": "a2", "kind": "amount", "review_status": "pending", "state": "verified", "reasons": [] },
386:  "amount": { "id": "a2", "text": "$185", "value_cents": 18500, "kind": "charge", "state": "verified", "reasons": [], "why": "...", "review_status": "pending",
400:Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). Optional query `style` (T-121): `standard` (default, the golden layout) or `oneline`, which writes one line per entry, `<long date> — <provider>: 
482:    "amounts": [
558:  "events": [ { "id": "ev1", "item_id": "e2", "action": "accept", "at": "2026-11-02T01:05:00Z" } ],
566:  "events": [ { "id": "ev1", "item_id": "e2", "action": "accept", "before": {"review_status": "pending"}, "after": {"review_status": "accepted"}, "at": "2026-11-02T01:05:00Z" } ] }
597:  "state": "needs_review", "review_status": "pending",
def accept_all_total_cents(out):
    """T-140: the total the letter would print if the paralegal accepted EVERY amount the tool found (charges, unclear, rate, estimate), through the real
    export builder (export.build_export), not a sum of charge-class figures. Items rejected by the code check are not offered for review and are left out.
    None when the letter has no total line (no accepted charge)."""
    from app.backend import export
    case = dict(records=[dict(n=r["n"], source=r.get("source"), date_iso=r.get("date_iso"), excerpt=r["excerpt"], text=r.get("text") or r["excerpt"]) for r in out["records"]],
                entries=[], flags=[], pending_count=0, events=[],
                amounts=[dict(id=a["id"], record_no=a["record_nos"][0], cents=a["cents"], cls=a["kind"], raw=a["raw"], excerpt=a["excerpt"], review_status="accepted")
                         for a in out.get("amounts") or [] if a.get("state") != "rejected"])
    for line in export.build_export(case)["letter_text"].splitlines():
        if line.startswith("Billed charges stated in these records: $"):
            return round(float(line.rsplit("$", 1)[1].replace(",", "")) * 100)
    return None
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:38.377Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/backend/api.py | grep -n \"library\\|def create_case\\|\\\"text\\\"\\|demo_mode()\" | head -30; curl -s http://127.0.0.1:7873/api/library | head -c 1500",
 "description": "Find library case creation in api and list library"
}
````

### User / tool · 2026-11-02T13:29:38.546Z

**tool result**
````
32:LIBRARY = ROOT / "evals" / "library"
62:def library_cases() -> list:
63:    """Synthetic case library (evals/library, same file format as evals/golden: <id>.txt + optional <id>.expected.json). Falls back to
64:    evals/golden until the library exists. [{id, name, description, path}]"""
101:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
119:    def demo_mode():
214:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
228:    @app.get("/api/library")
229:    def library():
232:        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}
235:    async def create_case(request: Request):
239:        if isinstance(b.get("library"), str):
242:            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
244:                raise ApiError(404, "not_found", "No such library case.")
245:        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
251:    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):
254:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
278:        out = make_case(got["text"], name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None})
287:        if demo_mode() and digest(text) not in allowed_hashes():
295:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
308:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
321:            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
357:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
359:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
382:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
384:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
542:                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
{"cases":[{"id":"case_lib01_er_only_then_gap","name":"case lib01 er only then gap","description":"Library L1 (mirrors S1). Rear-end collision, ED visit and a negative x-ray, then the first primary-care visit 44 days later with a new arm symptom and a patient-stated reason for the delay. The gap is flagged; the reason is shown as the pat"},{"id":"case_lib02_slip_fall_prior_knee","name":"case lib02 slip fall prior knee","description":"Library L2 (mirrors S2). Store slip-and-fall with a prior knee arthroscopy shown in imaging and in the patient's history; MRI wording that may reflect both acute and prior change. The tool shows the prior-condition language and the hedge an"},{"id":"case_lib03_truck_rear_end_chiro","name":"case lib03 truck rear end chiro","description":"Library L3 (mirrors S3). Passenger car struck from behind by a tractor-trailer; chiropractic plan of 36 visits, no change in pain score at visit 14, discharge at maximum benefit after 31 visits, then an MRI 35 days later with hedged chronic"},{"id":"case_lib04_dog_bite_scar_revision","name":"case lib04 dog bite scar revision","description":"Library L4 (mirrors S4). Facial dog bite repaired in the ED, plastic-surgery follow-ups with scar photographs, a planned 8-week interval that the tool still flags, a $6,500 revision estimate and a later revision with a surgeon fee. The tool"},{"id":"case_lib05_pedestrian_orif_hardware","name":"case lib05 pedestrian orif hardware","description":"Library L5 (mirrors S5). Pedestria
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:41.217Z

**tool call — Bash**
````
{
 "command": "git show HEAD:app/backend/api.py | sed -n 96,125p; git show HEAD:app/backend/api.py | sed -n 284,300p; git show HEAD:app/backend/api.py | sed -n 350,400p",
 "description": "Read demo-mode and run logic in api.py"
}
````

### User / tool · 2026-11-02T13:29:41.381Z

**tool result**
````
    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.db_path = db_path
    app.state.recorded = recorded_hashes()

    def allowed_hashes():
        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
    runs = {}
    rejudging = set()
    DB.connect(db_path).close()
    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
    purged = {"at": 0.0}

    # -------------------------------------------------- config (read per call so tests can monkeypatch env)
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
        except ingest.IngestError as e:
            raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
        if demo_mode() and digest(text) not in allowed_hashes():
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        c = conn()
        try:
            now = time.time()
            DB.purge_expired(c, now)
            name = name if isinstance(name, str) else ("Sample case" if sample else None)
            cid = DB.create_case(c, text, now=now, name=(name or "")[:120] or None,
                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
            try:
                ing = pipeline_mod().ingest_case(c, cid, text, now)
                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
                flags = DB.list_items(c, cid, "flag")
    async def run_case(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            case = get_case(c, token)
            if case["status"] == "running" or token in runs:
                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
            if decided and b.get("confirm_rerun") is not True:
                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
            now = time.time()
            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
            runs[token].start()
            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
        finally:
            c.close()

    @app.post("/api/cases/{token}/rejudge")
    async def rejudge_case(token: str):
        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
        from app.backend import rejudge as RJ
        c = conn()
        try:
            case = get_case(c, token)
            if case["status"] == "running" or token in runs or token in rejudging:
                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
            rejudging.add(token)
            try:
                return await run_in_threadpool(lambda: RJ.rejudge(c, token, make_call(c, token), now=time.time()))
            finally:
                rejudging.discard(token)
        finally:
            c.close()

    @app.get("/api/cases/{token}/status")
    def status(token: str):
        c = conn()
        try:
            case = get_case(c, token)
            stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
            stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:29:50.063Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat $S/tree/tests/unit/test_amounts_t140.py | sed -n 1,146p",
 "description": "Read the T-140 unit tests"
}
````

### User / tool · 2026-11-02T13:29:50.190Z

**tool result**
````
"""T-140 (GATE-M2 blocker): a total, subtotal, balance, amount due, payment, adjustment, write-off or credit line is never class charge,
whatever the judge says; a charge equal to the sum of the other charges in its record is a likely total. Code only (LLM_VS_CODE rows 6/7)."""
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import amounts as AM, totals as TT
from app.backend.api import create_app

ROOT = pathlib.Path(__file__).resolve().parents[2]
LIB11 = ROOT / "evals" / "library" / "case_lib11_priors_and_ledger.txt"
LEDGER = ("Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; "
          "total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection.")


def _rows(excerpt, source="Fennimoor Spine Clinic, itemized ledger"):
    return {a["raw"]: a for a in AM.extract_amounts([{"n": 1, "excerpt": excerpt, "source": source, "text": excerpt, "date_iso": "2026-06-15"}])}


def test_lib11_ledger_classes():
    r = _rows(LEDGER)
    assert [r[k]["cls"] for k in ("$250.00", "$180.00", "$2,310.00")] == ["charge"] * 3
    for k in ("$2,740.00", "$300.00", "$274.00", "$2,166.00"):
        assert r[k]["cls"] == "unclear", k
    assert TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": "accepted"} for a in r.values()])["accepted_cents"] == 250_00 + 180_00 + 2310_00


@pytest.mark.parametrize("text,word", [
    ("Total $900.00", "total"), ("Subtotal: $900.00", "total"), ("Statement total $900.00", "total"), ("Balance due $900.00", "balance"),
    ("Balance: $900.00", "balance"), ("Amount due $900.00", "balance"), ("Patient paid $900.00", "payment"), ("Payment received $900.00", "payment"),
    ("Payments to date $900.00", "payment"), ("Adjustment -$900.00", "adjustment"), ("Insurance write-off $900.00", "adjustment"),
    ("Courtesy credit $900.00", "adjustment"), ("Contractual adjustment $900.00", "adjustment")])
def test_total_balance_payment_adjustment_labels_are_never_charges(text, word):
    a = next(iter(_rows("Statement of account: " + text + ".").values()))
    assert a["cls"] == "unclear"
    reason = AM.not_totaled_reason("Statement of account: " + text + ".", a["raw"], a["cents"])
    assert reason and word in reason.lower()


@pytest.mark.parametrize("text", ["Office visit charge $150.00", "ER charges: $6,240.", "Charge: $2,150.", "Total of 12 visits billed $2,150.00", "Billed $400.00"])
def test_ordinary_charge_labels_stay_charges(text):
    a = next(iter(_rows(text + ".", source="Clinic, billing statement").values()))
    assert a["cls"] == "charge"
    assert AM.not_totaled_reason(text + ".", a["raw"], a["cents"]) is None


def test_word_must_be_the_label_not_anywhere_in_the_sentence():
    ex = "Payment plan discussed; radiology charge $180.00. Balance of the visit unremarkable, office charge $95.00."
    r = _rows(ex, source="Clinic, billing statement")
    assert r["$180.00"]["cls"] == "charge" and r["$95.00"]["cls"] == "charge"


def test_column_label_of_a_table():
    ex = "Date  Charges  Payments  Adjustments  Balance\n06/01  $500.00  $100.00  $50.00  $350.00"
    r = _rows(ex, source="Clinic, billing statement")
    assert AM.not_totaled_reason(ex, "$500.00", 50000) is None      # the Charges column is not a non-charge label
    assert [r[k]["cls"] for k in ("$100.00", "$50.00", "$350.00")] == ["unclear"] * 3
    assert "payment" in AM.not_totaled_reason(ex, "$100.00", 10000).lower() and "balance" in AM.not_totaled_reason(ex, "$350.00", 35000).lower()


def test_a_judge_cannot_make_a_total_a_charge():
    """The class is decided by code; extract_amounts has no judge input, and the reason is recomputed from the quote at export."""
    assert "judge" not in AM.classify.__code__.co_varnames and "verdict" not in AM.classify.__code__.co_varnames


def test_cross_check_flags_a_charge_equal_to_the_others():
    ex = "Statement: office visit charge $100.00; therapy charge $250.00; imaging charge $300.00; all services charge $650.00."
    r = _rows(ex, source="Clinic, billing statement")
    assert [r[k]["cls"] for k in ("$100.00", "$250.00", "$300.00")] == ["charge"] * 3
    assert r["$650.00"]["cls"] == "unclear"
    why = AM.not_totaled_reason(ex, "$650.00", 65000)
    assert "likely a total" in why and "sum of the other charges" in why


def test_cross_check_needs_two_other_charges_and_one_record():
    two = _rows("Statement: office visit charge $100.00; therapy charge $200.00.", source="Clinic, billing statement")
    assert [a["cls"] for a in two.values()] == ["charge", "charge"]
    recs = [{"n": 1, "excerpt": "Visit charge $100.00; visit charge $200.00.", "source": "Clinic, billing statement", "text": "x", "date_iso": "2026-01-01"},
            {"n": 2, "excerpt": "Bill charge $300.00.", "source": "Clinic, billing statement", "text": "y", "date_iso": "2026-01-02"}]
    assert [a["cls"] for a in AM.extract_amounts(recs)] == ["charge"] * 3          # $300 is the sum, but of lines in another record


def test_total_that_is_not_totaled_keeps_the_three_lines_total():
    ex = "Statement: office visit charge $100.00; therapy charge $250.00; imaging charge $300.00; all services charge $650.00."
    t = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": "accepted"} for a in _rows(ex, source="Clinic, billing statement").values()])
    assert t["accepted_cents"] == 65000


# ---- end to end: accept everything on lib11 and export
@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.setenv("ZLAYT_MODE", "local")
    return TestClient(create_app(str(tmp_path / "t140.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))


def test_lib11_accept_all_export_total_is_6000(client):
    c = client
    tok = c.post("/api/cases", json={"library": LIB11.stem}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready", s
    g = c.get(f"/api/cases/{tok}").json()
    for it in g["entries"] + g["amounts"] + g["flags"]:
        c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "accept"})
    ex = c.get(f"/api/cases/{tok}/export").json()
    assert "letter_text" in ex, ex
    assert "Billed charges stated in these records: $6,000.00" in ex["letter_text"].split("\n")
    assert ex["totals"]["charges_cents"] == 600000
    notes = ex["internal_notes_text"].split("AMOUNTS NOT TOTALED")[1].split("\n\n")[0]
    for fig in ("$2,740", "$300", "$274", "$2,166"):
        assert fig in notes, fig
    assert "total" in notes.lower() and "balance" in notes.lower() and "payment" in notes.lower() and "adjustment" in notes.lower()
    assert "$2,740" not in ex["letter_text"] and "$2,166" not in ex["letter_text"]


# ---- the eval check: accept-all total of a library case vs its expected total
@pytest.mark.parametrize("case", ["case_lib11_priors_and_ledger", "case_lib14_handwritten_chiro_scans", "case_lib15_conclusory_letter_mist", "case_lib02_slip_fall_prior_knee"])
def test_library_accept_all_total_equals_expected(case, monkeypatch):
    import json
    from evals import library_report as LR
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    from app import pipeline
    exp = json.loads((ROOT / "evals" / "library" / f"{case}.expected.json").read_text())
    row = LR.score(case, (ROOT / "evals" / "library" / f"{case}.txt").read_text(), exp, pipeline)
    assert row["accept_all_ok"], row["accept_all"]
    assert LR.accept_all_total_cents(pipeline.run_case((ROOT / "evals" / "library" / f"{case}.txt").read_text(), "fixture")) == round(exp["totals"]["explicit_charges_total"] * 100)


def test_library_check_catches_a_counted_total():
    """The check is not a tautology: a run whose ledger total were classed as a charge reports WRONG with both figures."""
    from evals import library_report as LR
    out = {"records": [{"n": 1, "source": "Clinic, billing statement", "date_iso": "2026-01-01", "excerpt": "Visit charge $100.00; total charges $100.00."}],
           "amounts": [{"id": "a1", "record_nos": [1], "cents": 10000, "kind": "charge", "raw": "$100.00", "excerpt": "Visit charge $100.00; total charges $100.00.", "state": "verified"},
                       {"id": "a2", "record_nos": [1], "cents": 10000, "kind": "charge", "raw": "$100.00", "excerpt": "Visit charge $100.00; total charges $100.00.", "state": "verified"}]}
    assert LR.accept_all_total_cents(out) == 20000      # both offered as charges -> the letter would print $200.00, not the expected $100.00
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:30:04.025Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; sed -n 1,97p $S/tree/app/backend/amounts.py; sed -n 196,262p $S/tree/app/backend/amounts.py",
 "description": "Read amounts.py helpers and extraction"
}
````

### User / tool · 2026-11-02T13:30:04.114Z

**tool result**
````
"""Dollar amounts: find, classify, dedupe (all code; ADR-011, R-CH-1/2/4/6, D-004/D-005, LLM_VS_CODE rows 6 and 7).
Money is whole cents (int). Noisy OCR figures keep their verbatim text with cents None and class unclear, never corrected.
There is no LLM classifier. A rate can never become a charge: classes are decided here and the paralegal can only accept or dismiss."""
import re

from app.backend import injection, lexicon

# '$' + a whole numeric token (extra decimals are kept so to_cents can refuse them: never truncated).
# '$' + a figure. Letters that OCR confuses with digits (O o l I S B) are tolerated so noise is LISTED (unclear), not silently skipped.
_AMT = re.compile(r"\$\s?([0-9OolISB](?:[0-9OolISB,]*[0-9OolISB])?(?:\.[0-9OolISB]+)?)")
_VALID = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?\Z")
_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
# Rate = unit-rate phrasing only. 'Charge per invoice 4471: $400' is NOT a rate (per + a non-unit noun stays a charge or unclear).
_UNIT = r"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?"
# Spanish unit nouns (T-110 r2): "por sesión", "por visita", "cada ...". Accents are optional because pasted records often lose them.
_UNIT_ES = r"(?:sesi[o\u00f3]n|sesiones|visitas?|horas?|d[i\u00ed]as?|unidad(?:es)?|citas?|tratamientos?|procedimientos?)"
_RATE_WORD = re.compile(rf"\b(?:(?:per|each)[\s-]+{_UNIT}|rate\s+of|(?:por|cada)\s+{_UNIT_ES})\b|/\s*{_UNIT}\b|/\s*{_UNIT_ES}\b", re.IGNORECASE)
_RATE_AFTER = re.compile(rf"^\s*(?:(?:per|each|an?)[\s-]+{_UNIT}\b|(?:por|cada)\s+{_UNIT_ES}\b|/\s*{_UNIT}\b|each\b|cada\s+(?:una?|uno)\b|(?:hourly|daily|weekly|monthly|apiece)\b|an?\s+(?:month|week)\b)", re.IGNORECASE)
_ESTIMATE = re.compile(r"\bestimat(?:e|ed|es)\b", re.IGNORECASE)
_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
# ONE rate-cue test for every code path that decides "is this figure a unit price?" (reclassify.py wording gate, billing.py ledger rows and
# sentences). A cue is decisive: "Charge per visit $185" and "Billed $150 per visit" state a rate, whatever else the text says (D-042, T-084 r2).
_RATE_CORE = (r"\bper\b|\beach\b|\bevery\b|\bcada\b|\bpor\s+(?:sesi[o\u00f3]n|sesiones|visitas?|horas?|d[i\u00ed]as?|unidad(?:es)?|citas?|tratamientos?|procedimientos?)\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
              r"|\ban?\s+(?:visit|session|hour|hr|day|treatment|appointment|unit|procedure|month|week)\b|\b(?:daily|hourly|weekly|monthly|session|visit|unit|flat)\s+(?:rate|fee|price|cost)\b|\brate\b"
              r"|\b(?:hourly|daily|weekly|monthly|apiece)\b|\bunit\s+(?:price|cost|charge)\b|@\s*\$"
              r"|\b\d+\s*[x\u00d7]\s*\$?\d")
_RATE_X_COUNT = r"(?<![\w$])[x\u00d7]\s*\d+\b"            # "x 14": a multiplier in a sentence, but plain unit notation ("Manual therapy x1") in a ledger row
RATE_CUE = re.compile(_RATE_CORE + "|" + _RATE_X_COUNT, re.IGNORECASE)
_RATE_CUE_ROW = re.compile(_RATE_CORE, re.IGNORECASE)


def has_rate_cue(text: str, unit_notation: bool = False) -> bool:
    """True when the text carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate, rate of ...). `unit_notation=True` is for a
    ledger row's description, where "x1" / "x2" is the unit count of a normal charge line and not a multiplier."""
    return bool((_RATE_CUE_ROW if unit_notation else RATE_CUE).search(text or ""))


# Spanish charge and balance cues (T-110 r3, D-050). The classifier does NOT use them: a Spanish figure stays `unclear` until the paralegal reads the
# original and reclassifies it, and only the reclassify guard (code cue + judge re-check) reads them. A rate cue above still beats a charge cue.
# PRECEDENCE (r3): a payment, balance, adjustment, copay or insurance word in the sentence beats every charge cue, in English and Spanish, because a
# statement of account lists payments and balances beside charges and a balance restates charges (counting it counts them twice).
CHARGE_CUE_ES = re.compile(r"\b(?:cargos?|honorarios)\b", re.IGNORECASE)
# 'estado de cuenta' names the document, never a charge. It counts only as statement context for a billed-service noun (consultas), never alone.
STATEMENT_CONTEXT_ES = re.compile(r"\bestado\s+de\s+cuenta\b", re.IGNORECASE)
_SERVICE_LINE_ES = re.compile(r"\bconsultas\b", re.IGNORECASE)
_NO_CHARGE_ES = re.compile(r"\bsin\s+(?:cargo|costo|cobro)s?\b|\bno\s+(?:se\s+)?(?:cobr[o\u00f3a]|factur\w*)\b|\bgratis\b|\bgratuit[oa]\b", re.IGNORECASE)
BALANCE_CUE = re.compile(
    r"\b(?:saldos?|balances?|pendientes?|adeudos?|"                                    # balance
    r"pagos?|pag[o\u00f3]|pagad[oa]s?|abonos?|copagos?|payments?|paid|copays?|"         # payment
    r"ajustes?|adjust(?:ment|ments|ed)?|cr[e\u00e9]ditos?|descuentos?|deducibles?|seguro|insurance|insurer|"   # adjustment / insurance
    r"contractual|write-?offs?)\b", re.IGNORECASE)


def charge_cue_es(text: str):
    """The Spanish charged-amount phrase in `text` (cargo, cargos, honorarios, or a statement-context 'consultas' line), or None. A payment, balance,
    adjustment, copay or insurance word (BALANCE_CUE) or a negation ('sin cargo', 'no facturado') in the same text returns None, whatever else it says."""
    t = text or ""
    if _NO_CHARGE_ES.search(t) or BALANCE_CUE.search(t):
        return None
    m = CHARGE_CUE_ES.search(t)
    if m:
        return m.group(0)
    ctx, svc = STATEMENT_CONTEXT_ES.search(t), _SERVICE_LINE_ES.search(t)
    return f"{ctx.group(0)}: {svc.group(0)}" if ctx and svc else None


_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)


def to_cents(figure: str):
    """'6,240' -> 624000, '95.5' -> 9550; None when the figure is not a clean number. Integer arithmetic only."""
    m = _VALID.match(figure)
    if not m:
        return None
    whole = figure.split(".")[0].replace(",", "")
    return int(whole) * 100 + int((m.group(1) or "").ljust(2, "0") or 0)


def find_amounts(excerpt: str) -> list:
    """[{raw, cents, start, end}] for every '$' figure, in text order. Doses, speeds, scores and day counts have no '$' and are never found."""
    out = []
    spans = [(h["start"], h["end"]) for h in injection.scan(excerpt or "")]
    for m in _AMT.finditer(excerpt or ""):
        figure = m.group(1)
        if not any(c.isdigit() for c in figure):
            continue
        injected = any(s <= m.start() and m.end() <= e for s, e in spans)   # a figure inside instruction-like text has no trusted value (D-005)
        out.append({"raw": m.group(0), "cents": None if injected else to_cents(figure), "start": m.start(), "end": m.end()})
    return out


def _label(excerpt: str, start: int) -> str:
    before = _BOUNDARY.split(excerpt[:start])[-1]
    clauses = [c for c in re.split(r"[,;]", before) if c.strip()]   # the amount's own clause: cues in a neighbouring clause do not count
    return " ".join((clauses[-1] if clauses else "").split()[-6:])


def _is_billing_source(source: str) -> bool:
    return any(e["id"] == "billing_document" and e["regex"].search(source or "") for e in lexicon.code_list("non_encounter"))


def damages_mentions(excerpt: str) -> list:
    """Work-loss and similar mentions with no dollar value (lexicon `damages`): [{raw, cents: None, cls: 'damages', start, end}]."""
    out = []
    for e in lexicon.code_list("damages"):
        for m in e["regex"].finditer(excerpt or ""):
            end = m.end()
            t = _WORK_TAIL.match(excerpt, end)
            if t:
                end = t.end()
            if not any(o["start"] < end and m.start() < o["end"] for o in out):
                out.append({"raw": excerpt[m.start():end], "cents": None, "cls": "damages", "start": m.start(), "end": end})
    return sorted(out, key=lambda o: o["start"])


def _norm(s):
    return " ".join((s or "").split()).casefold()


def dedupe_amounts(amounts: list, separate=frozenset()) -> list:
    """Same date + normalised provider + record text (when given) + class + value merges into one amount citing every record (R-CH-6). Unreadable values never merge."""
    out, index = [], {}
    for a in amounts:
        nos = sorted(a.get("record_nos") or [a["record_no"]])
        key = (a.get("date"), _norm(a.get("provider")), _norm(a.get("text")), a.get("cls"), a.get("cents")) if a.get("cents") is not None else None
        if set(nos) & set(separate):        # records the paralegal declared not-a-duplicate never merge (D-031)
            key = None
        if key in index:
            m = out[index[key]]
            m["record_nos"] = sorted(set(m["record_nos"]) | set(nos))
            m["duplicate_note"] = "Same amount, date and provider appears in records " + ", ".join(str(n) for n in m["record_nos"]) + "."
            continue
        row = {**a, "record_nos": nos, "duplicate_note": None}
        if key is not None:
            index[key] = len(out)
        out.append(row)
    return out


def extract_amounts(records: list, separate=frozenset()) -> list:
    """All amounts of a case from ingested records (needs n, excerpt; uses date_iso, source, injection_tag, text, char_start when present).
    Injection-tagged records yield class unclear for every amount (D-005). Duplicate records contribute once (the dedupe is per record).
    `separate` = record numbers the paralegal said are not duplicates: their amounts never merge with another record's and get ids ax<n>_<k>."""
    rows = []
    for r in records:
        if r.get("duplicate_of"):
            continue
        base = (r.get("char_start") or 0) + (r["text"].find(r["excerpt"]) if r.get("text") and r["excerpt"] in r["text"] else 0)
        found = [{**a, "cls": classify(r["excerpt"], a, injection=bool(r.get("injection_tag")), source=r.get("source"))}
                 for a in find_amounts(r["excerpt"])]
        for i in _likely_totals([{**a, "injection": bool(r.get("injection_tag"))} for a in found]):      # T-140: a charge equal to the others is a total
            found[i]["cls"] = "unclear"
        found += damages_mentions(r["excerpt"])
        for a in sorted(found, key=lambda x: x["start"]):
            rows.append({"record_no": r["n"], "text": r["excerpt"], "date": r.get("date_iso"), "provider": r.get("source"), "raw": a["raw"], "cents": a["cents"],
                         "cls": a["cls"], "start": base + a["start"], "end": base + a["end"], "injection": bool(r.get("injection_tag"))})
    out = dedupe_amounts(rows, separate)
    i, k = 0, {}
    for a in out:
        if a["record_no"] in separate:         # stable ids that do not shift the other amounts: a rerun lands on the same rows
            k[a["record_no"]] = k.get(a["record_no"], 0) + 1
            a["id"] = f"ax{a['record_no']}_{k[a['record_no']]}"
        else:
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:30:49.748Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_library.py",
 "content": "\"\"\"T-140 adjuster probe: run every library case on the reviewer's own server, accept everything, export, print the total line\nand every amount (class, state, raw, record) so the total can be checked against the records by hand. Usage: probe_library.py BASE_URL [case ...]\"\"\"\nimport json\nimport sys\nimport time\nimport urllib.error\nimport urllib.request\n\nBASE = sys.argv[1].rstrip(\"/\")\n\n\ndef call(method, path, body=None):\n    data = None if body is None else json.dumps(body).encode()\n    req = urllib.request.Request(BASE + path, data=data, method=method, headers={\"Content-Type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(req, timeout=120) as r:\n            return r.status, json.loads(r.read() or b\"null\")\n    except urllib.error.HTTPError as e:\n        return e.code, json.loads(e.read() or b\"null\")\n\n\ndef run_case(body):\n    st, c = call(\"POST\", \"/api/cases\", body)\n    if st not in (200, 201):\n        return {\"create_error\": [st, c]}\n    tok = c[\"token\"]\n    st, r = call(\"POST\", f\"/api/cases/{tok}/run\", {})\n    if st != 202:\n        return {\"token\": tok, \"run_error\": [st, r]}\n    for _ in range(600):\n        s = call(\"GET\", f\"/api/cases/{tok}/status\")[1]\n        if s.get(\"status\") in (\"ready\", \"failed\"):\n            break\n        time.sleep(0.25)\n    g = call(\"GET\", f\"/api/cases/{tok}\")[1]\n    refused = []\n    for it in g.get(\"entries\", []) + g.get(\"amounts\", []) + g.get(\"flags\", []):\n        st, r = call(\"POST\", f\"/api/cases/{tok}/items/{it['id']}/review\", {\"action\": \"accept\"})\n        if st != 200:\n            refused.append([it[\"id\"], st, (r or {}).get(\"error\", r) if isinstance(r, dict) else r])\n    g = call(\"GET\", f\"/api/cases/{tok}\")[1]\n    st, ex = call(\"GET\", f\"/api/cases/{tok}/export\")\n    letter = (ex or {}).get(\"letter_text\", \"\") if isinstance(ex, dict) else \"\"\n    notes = (ex or {}).get(\"internal_notes_text\", \"\") if isinstance(ex, dict) else \"\"\n    total = [ln for ln in letter.splitlines() if ln.startswith(\"Billed charges\")]\n    nt = notes.split(\"AMOUNTS NOT TOTALED\")[1].split(\"\\n\\n\")[0] if \"AMOUNTS NOT TOTALED\" in notes else \"\"\n    return {\"token\": tok, \"status\": s.get(\"status\"), \"export_status\": st, \"total_line\": total, \"totals\": (ex or {}).get(\"totals\") if isinstance(ex, dict) else None,\n            \"amounts\": [[a[\"id\"], a.get(\"kind\"), a.get(\"state\"), a.get(\"review_status\"), a.get(\"raw\") or a.get(\"text\"), a.get(\"record_nos\"), a.get(\"reasons\")]\n                        for a in g.get(\"amounts\", [])],\n            \"refused\": refused, \"not_totaled_notes\": nt, \"dollar_lines_in_letter\": [ln for ln in letter.splitlines() if \"$\" in ln],\n            \"export_error\": None if st == 200 else ex}\n\n\nif __name__ == \"__main__\":\n    cases = sys.argv[2:]\n    if cases and cases[0].startswith(\"@\"):\n        text = open(cases[0][1:]).read()\n        print(json.dumps(run_case({\"text\": text}), indent=1))\n        sys.exit()\n    if not cases:\n        cases = [x[\"id\"] for x in call(\"GET\", \"/api/library\")[1][\"cases\"]]\n    for cid in cases:\n        print(\"=====\", cid)\n        print(json.dumps(run_case({\"library\": cid}), indent=1))\n"
}
````

### User / tool · 2026-11-02T13:30:49.879Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_library.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:30:51.743Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-140-adjuster/probe_library.py http://127.0.0.1:7873 case_lib11_priors_and_ledger",
 "description": "Run lib11 accept-all export probe on own server",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T13:30:52.487Z

**tool result**
````
===== case_lib11_priors_and_ledger
{
 "token": "KDf6VAbxIcka3iTKGIIK8g",
 "status": "ready",
 "export_status": 200,
 "total_line": [
  "Billed charges stated in these records: $6,000.00"
 ],
 "totals": {
  "charges_cents": 600000,
  "charges_count": 4
 },
 "amounts": [
  [
   "a1",
   "charge",
   "verified",
   "accepted",
   "$3,260",
   null,
   []
  ],
  [
   "a2",
   "charge",
   "verified",
   "accepted",
   "$250.00",
   null,
   []
  ],
  [
   "a3",
   "charge",
   "verified",
   "accepted",
   "$180.00",
   null,
   []
  ],
  [
   "a4",
   "charge",
   "verified",
   "accepted",
   "$2,310.00",
   null,
   []
  ],
  [
   "a5",
   "unclear",
   "needs_review",
   "accepted",
   "$2,740.00",
   null,
   [
    "JUDGE_DISAGREES",
    "AMOUNT_UNCLEAR"
   ]
  ],
  [
   "a6",
   "unclear",
   "needs_review",
   "accepted",
   "$300.00",
   null,
   [
    "JUDGE_DISAGREES",
    "AMOUNT_UNCLEAR"
   ]
  ],
  [
   "a7",
   "unclear",
   "needs_review",
   "accepted",
   "$274.00",
   null,
   [
    "AMOUNT_UNCLEAR"
   ]
  ],
  [
   "a8",
   "unclear",
   "needs_review",
   "accepted",
   "$2,166.00",
   null,
   [
    "JUDGE_DISAGREES",
    "AMOUNT_UNCLEAR"
   ]
  ]
 ],
 "refused": [
  [
   "e3",
   422,
   {
    "code": "CODE_CHECK_FAILED",
    "message": "The quote states a dollar amount ($3,260). Amounts go only in the internal notes, never in the letter. Change the quote to sentences that do not state it, and edit the summary to remove it.",
    "detail": {
     "item_id": "e3",
     "reason_code": "CHARGE_TEXT_IN_ENTRY",
     "step_id": "charge_text",
     "failed_steps": [
      "charge_text"
     ],
     "tokens": [],
     "amounts": [
      "$3,260",
      "$3,260"
     ],
     "next_action": {
      "code": "EDIT_QUOTE",
      "text": "Pick a quote that does not state the amount",
      "target": {
       "item_id": "e3"
      }
     }
    }
   }
  ],
  [
   "e9",
   422,
   {
    "code": "CODE_CHECK_FAILED",
    "message": "The quote states a dollar amount ($250.00, $180.00, $2,310.00, $2,740.00). Amounts go only in the internal notes, never in the letter. Change the quote to sentences that do not state it, and edit the summary to remove it.",
    "detail": {
     "item_id": "e9",
     "reason_code": "CHARGE_TEXT_IN_ENTRY",
     "step_id": "charge_text",
     "failed_steps": [
      "charge_text"
     ],
     "tokens": [],
     "amounts": [
      "$250.00",
      "$180.00",
      "$2,310.00",
      "$2,740.00",
      "$250.00",
      "$180.00",
      "$2,310.00",
      "$2,740.00"
     ],
     "next_action": {
      "code": "EDIT_QUOTE",
      "text": "Pick a quote that does not state the amount",
      "target": {
       "item_id": "e9"
      }
     }
    }
   }
  ]
 ],
 "not_totaled_notes": "\n- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): \"total charges $2,740.00.\" Not totaled ($2,740.00): Total or subtotal line: it repeats the charges listed with it, so it is not totaled.\n- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): \"Payment received $300.00.\" Not totaled ($300.00): Payment: money received, not a charge.\n- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): \"Adjustment (courtesy discount) -$274.00.\" Not totaled ($274.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.\n- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): \"Balance due $2,166.00.\" Not totaled ($2,166.00): Balance or amount due: worked out from charges, payments and adjustments, not a charge.",
 "dollar_lines_in_letter": [
  "Wexcombe Memorial ED, March 18, 2026: $3,260.00",
  "Source [Ex. __ / Bates __]: \"ED charge: $3,260.\"",
  "Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00",
  "Source [Ex. __ / Bates __]: \"New patient exam charge $250.00\"",
  "Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00",
  "Source [Ex. __ / Bates __]: \"x-ray charge $180.00\"",
  "Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $2,310.00",
  "Source [Ex. __ / Bates __]: \"treatment visits 1 through 14 charge $2,310.00\"",
  "Billed charges stated in these records: $6,000.00"
 ],
 "export_error": null
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:30:56.453Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-140-adjuster/probe_library.py http://127.0.0.1:7873 | .venv/bin/python -I -c \"\nimport sys,json,re\ntxt=sys.stdin.read()\nfor blk in txt.split('===== ')[1:]:\n    name,_,js=blk.partition('\\n'); d=json.loads(js)\n    print('##',name,d.get('status'),d.get('export_status'),d.get('total_line'),d.get('totals'))\n    for a in d.get('amounts',[]): print('   ',a[0],a[1],a[2],a[3],a[4])\n    if d.get('export_error'): print('   EXPORT ERR',str(d['export_error'])[:300])\n\" 2>&1 | tee artifacts/review-evidence/T-140-adjuster/library_accept_all.txt",
 "description": "Run all library cases accept-all and summarize totals",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T13:31:02.471Z

**tool result**
````
## case_lib01_er_only_then_gap ready 200 ['Billed charges stated in these records: $3,915.00'] {'charges_cents': 391500, 'charges_count': 1}
    a1 charge verified accepted $3,915
    a2 rate needs_review accepted $140
## case_lib02_slip_fall_prior_knee ready 200 ['Billed charges stated in these records: $2,260.00'] {'charges_cents': 226000, 'charges_count': 2}
    a1 charge verified accepted $410
    a2 charge verified accepted $1,850
    a3 rate needs_review accepted $155
## case_lib03_truck_rear_end_chiro ready 200 ['Billed charges stated in these records: $7,500.00'] {'charges_cents': 750000, 'charges_count': 2}
    a1 charge verified accepted $5,260
    a2 rate needs_review accepted $120
    a3 charge verified accepted $2,240
## case_lib04_dog_bite_scar_revision ready 200 ['Billed charges stated in these records: $4,730.00'] {'charges_cents': 473000, 'charges_count': 1}
    a1 charge verified accepted $4,730
    a2 estimate needs_review accepted $6,500
    a3 unclear needs_review accepted $3,900
## case_lib05_pedestrian_orif_hardware ready 200 ['Billed charges stated in these records: $38,420.00'] {'charges_cents': 3842000, 'charges_count': 1}
    a1 charge verified accepted $38,420
    a2 rate needs_review accepted $175
    a3 unclear needs_review accepted $6,150
## case_lib06_lop_billed_vs_adjusted ready 200 ['Billed charges stated in these records: $6,380.00'] {'charges_cents': 638000, 'charges_count': 3}
    a1 charge verified accepted $2,880
    a2 charge verified accepted $1,100
    a3 unclear needs_review accepted $450
    a4 unclear needs_review accepted $1,550
    a5 charge verified accepted $2,400
    a6 unclear needs_review accepted $1,250
    a7 unclear needs_review accepted $1,150
## case_lib07_parking_lot_fall_outside_records ready 200 ['Billed charges stated in these records: $2,620.00'] {'charges_cents': 262000, 'charges_count': 2}
    a1 charge verified accepted $640
    a2 charge verified accepted $1,980
## case_lib08_second_crash_mri_after ready 200 ['Billed charges stated in these records: $11,240.00'] {'charges_cents': 1124000, 'charges_count': 3}
    a1 charge verified accepted $4,210
    a2 rate needs_review accepted $145
    a3 charge verified accepted $4,680
    a4 charge verified accepted $2,350
## case_lib09_spanish_interpreter_espalda ready 200 ['Billed charges stated in these records: $5,090.00'] {'charges_cents': 509000, 'charges_count': 2}
    a1 charge verified accepted $2,940
    a2 unclear needs_review accepted $650.00
    a3 rate needs_review accepted $400.00
    a4 charge verified accepted $2,150
    a5 unclear needs_review accepted $1,300.00
    a6 rate needs_review accepted $400.00
    a7 unclear needs_review accepted $2,900.00
## case_lib10_eob_ub04_cms1500 ready 200 ['Billed charges stated in these records: $16,147.00'] {'charges_cents': 1614700, 'charges_count': 5}
    a1 rate needs_review accepted $1,640.00
    a2 charge verified accepted $4,920.00
    a3 charge verified accepted $2,105.00
    a4 charge verified accepted $386.50
    a5 charge verified accepted $712.00
    a6 unclear needs_review accepted $8,123.50
    a7 charge verified accepted $8,023.50
    a8 unclear needs_review accepted $3,610.00
    a9 unclear needs_review accepted $4,413.50
    a10 unclear needs_review accepted $3,530.80
    a11 unclear needs_review accepted $882.70
## case_lib11_priors_and_ledger ready 200 ['Billed charges stated in these records: $6,000.00'] {'charges_cents': 600000, 'charges_count': 4}
    a1 charge verified accepted $3,260
    a2 charge verified accepted $250.00
    a3 charge verified accepted $180.00
    a4 charge verified accepted $2,310.00
    a5 unclear needs_review accepted $2,740.00
    a6 unclear needs_review accepted $300.00
    a7 unclear needs_review accepted $274.00
    a8 unclear needs_review accepted $2,166.00
## case_lib12_records_review_credibility ready 200 ['Billed charges stated in these records: $5,790.00'] {'charges_cents': 579000, 'charges_count': 4}
    a1 charge verified accepted $2,780
    a2 charge verified accepted $210.00
    a3 charge verified accepted $2,320.00
    a4 charge verified accepted $480.00
    a5 rate needs_review accepted $145.00
## case_lib13_cloned_notes_cross_provider ready 200 ['Billed charges stated in these records: $5,830.00'] {'charges_cents': 583000, 'charges_count': 2}
    a1 charge verified accepted $3,540
    a2 charge verified accepted $2,290
    a3 estimate needs_review accepted $38,500
## case_lib14_handwritten_chiro_scans ready 200 ['Billed charges stated in these records: $4,527.05'] {'charges_cents': 452705, 'charges_count': 3}
    a1 charge verified accepted $2,960
    a2 charge verified accepted $1,380.00
    a3 unclear needs_review accepted $21.50
    a4 charge verified accepted $187.05
    a5 unclear needs_review accepted $1,567.05
## case_lib15_conclusory_letter_mist ready 200 ['Billed charges stated in these records: $3,295.00'] {'charges_cents': 329500, 'charges_count': 3}
    a1 charge verified accepted $385
    a2 rate needs_review accepted $150.00
    a3 rate needs_review accepted $1,800.00
    a4 charge verified accepted $210.00
    a5 charge verified accepted $2,700.00
    a6 unclear needs_review accepted $2,910.00
    a7 unclear needs_review accepted $250.00
    a8 unclear needs_review accepted $2,660.00
    a9 unclear needs_review accepted $2,910.00
    a10 unclear needs_review accepted $250.00
    a11 unclear needs_review accepted $2,660.00
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:31:05.054Z

**tool call — Bash**
````
{
 "command": "for f in evals/library/case_lib*.txt; do b=$(basename $f .txt); echo \"## $b\"; .venv/bin/python -I -c \"\nimport json,sys; e=json.load(open(sys.argv[1])); print('  expected', e.get('totals'))\" evals/library/$b.expected.json; grep -n '\\$' $f | cut -c1-700; done",
 "description": "List dollar lines and expected totals per library case"
}
````

### User / tool · 2026-11-02T13:31:05.665Z

**tool result**
````
## case_lib01_er_only_then_gap
  expected {'explicit_charges_total': 3915, 'counted_amount_ids': ['A1'], 'amounts_found': 2, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A2', 'reason': 'rate $140/visit; visit count not stated (8 planned); needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $3,915.00', 'ui_line': 'Accepted charges: $3,915.00', 'notes_lines': ['$140: rate $140/visit; visit count not stated (8 planned); needs review']}
11:Excerpt: "Dx: cervical strain. X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Follow up with primary care in 1 week. ED charge: $3,915."
21:Excerpt: "Cervical range of motion reduced approx. 30%. Plan of care: 8 visits. Charge per visit $140."
## case_lib02_slip_fall_prior_knee
  expected {'explicit_charges_total': 2260, 'counted_amount_ids': ['A1', 'A2'], 'amounts_found': 3, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A3', 'reason': 'rate $155/visit; visit count not stated (10 planned; visit 10 note present); needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $2,260.00', 'ui_line': 'Accepted charges: $2,260.00', 'notes_lines': ['$155: rate $155/visit; visit count not stated (10 planned; visit 10 note present); needs review']}
11:Excerpt: "Right knee pain 7/10 with swelling. X-ray right knee: no acute fracture; prior arthroscopic changes noted. Dx: knee contusion. Knee immobilizer provided. Visit charge: $410."
21:Excerpt: "Medial meniscus tear with moderate joint effusion. Mild tricompartmental degenerative change. Findings may reflect both acute injury and prior surgical change. MRI charge: $1,850."
31:Excerpt: "Right knee flexion limited to 100 degrees. Plan of care: 10 visits. Charge per visit $155."
## case_lib03_truck_rear_end_chiro
  expected {'explicit_charges_total': 7500, 'counted_amount_ids': ['A1', 'A3'], 'amounts_found': 3, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A2', 'reason': 'rate $120/visit; billed visit count not stated (36 planned, 31 attended); needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $7,500.00', 'ui_line': 'Accepted charges: $7,500.00', 'notes_lines': ['$120: rate $120/visit; billed visit count not stated (36 planned, 31 attended); needs review']}
11:Excerpt: "Dx: lumbar and cervical sprain. CT cervical spine negative. Rx naproxen. Refer to chiropractic or primary care. ED charge: $5,260."
16:Excerpt: "Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks. Charge per visit $120."
36:Excerpt: "L4-L5 disc bulge without nerve root compression. Mild disc desiccation. Radiology: findings likely chronic. MRI charge: $2,240."
## case_lib04_dog_bite_scar_revision
  expected {'explicit_charges_total': 8630, 'counted_amount_ids': ['A1', 'A3'], 'amounts_found': 3, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A2', 'reason': 'estimate $6,500 for a revision; not a billed charge; needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $8,630.00', 'ui_line': 'Accepted charges: $8,630.00', 'notes_lines': ['$6,500: estimate $6,500 for a revision; not a billed charge; needs review']}
11:Excerpt: "Dx: dog bite, left cheek laceration 4 cm and chin laceration 2 cm. Wounds irrigated and sutured. Amoxicillin-clavulanate prescribed. ED charge: $4,730."
26:Excerpt: "Scar remains raised at 3 months. Revision discussed if no improvement by 12 months. Estimated revision cost: $6,500."
31:Excerpt: "Scar revision performed under local anesthesia. Surgeon fee: $3,900. Photographs taken."
## case_lib05_pedestrian_orif_hardware
  expected {'explicit_charges_total': 44570, 'counted_amount_ids': ['A1', 'A3'], 'amounts_found': 3, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A2', 'reason': 'rate $175/visit; visit count not stated (16 planned); needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $44,570.00', 'ui_line': 'Accepted charges: $44,570.00', 'notes_lines': ['$175: rate $175/visit; visit count not stated (16 planned); needs review']}
11:Excerpt: "Dx: left tibial plateau fracture and left fibular fracture. Splinted. Admitted to orthopedics. ED charges: $38,420."
26:Excerpt: "Left knee flexion limited to 80 degrees. Plan of care: 16 visits. Charge per visit $175."
41:Excerpt: "Removal of hardware, left tibial plateau. Subchondral cyst repaired. Total knee replacement may be needed in the future. Surgeon fee: $6,150."
## case_lib06_lop_billed_vs_adjusted
  expected {'explicit_charges_total': 6830, 'counted_amount_ids': ['A1', 'A2', 'A3', 'A5'], 'amounts_found': 7, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A4', 'reason': 'balance $1,550 equals statement lines A2 + A3; not counted; needs review', 'total_computed': False}, {'amount_id': 'A6', 'reason': 'insurance adjustment -$1,250; not a charge; needs review (billed vs paid/incurred is a legal question, not a tool decision)', 'total_computed': False}, {'amount_id': 'A7', 'reason': 'amount due $1,150 after adjustment; not the billed charge; needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $6,830.00', 'ui_line': 'Accepted charges: $6,830.00', 'notes_lines': ['$1,550: balance $1,550 equals statement lines A2 + A3; not counted; needs review', '$1,250: insurance adjustment -$1,250; not a charge; needs review (billed vs paid/incurred is a legal question, not a tool decision)', '$1,150: amount due $1,150 after adjustment; not the billed charge; needs review']}
11:Excerpt: "Dx: right shoulder contusion. X-ray negative. Sling provided. ED charge: $2,880."
21:Excerpt: "Statement of charges: office visits $1,100; MRI referral fee $450. Balance under letter of protection: $1,550."
26:Excerpt: "Mild supraspinatus tendinosis; no full-thickness tear. Charge: $2,400. Insurance adjustment: -$1,250. Amount due: $1,150."
## case_lib07_parking_lot_fall_outside_records
  expected {'explicit_charges_total': 2620, 'counted_amount_ids': ['A1', 'A2'], 'amounts_found': 2, 'status': 'complete', 'unclear_items': [], 'letter_line': 'Billed charges stated in these records: $2,620.00', 'ui_line': 'Accepted charges: $2,620.00', 'notes_lines': []}
11:Excerpt: "X-ray right wrist: nondisplaced distal radius fracture. X-ray lumbar spine: mild degenerative changes. Charge: $640."
31:Excerpt: "L4-L5 disc protrusion with mild canal narrowing. Postoperative changes at L4-L5. Possible aggravation of a pre-existing condition cannot be excluded. MRI charge: $1,980."
## case_lib08_second_crash_mri_after
  expected {'explicit_charges_total': 11240, 'counted_amount_ids': ['A1', 'A3', 'A4'], 'amounts_found': 4, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A2', 'reason': 'Rate, not a charge: visits billed are never stated (12 weeks planned); needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $11,240.00', 'ui_line': 'Accepted charges: $11,240.00', 'notes_lines': ['$145: Rate, not a charge: visits billed are never stated (12 weeks planned); needs review']}
11:Excerpt: "Dx: cervical strain. CT head negative. Denies LOC per patient. Discharged on cyclobenzaprine. ED charge: $4,210."
21:Excerpt: "Cervical range of motion reduced about 25%. Plan of care: 12 weeks, twice weekly. Charge per visit $145."
46:Excerpt: "Dx: cervical strain. CT cervical spine negative for fracture. Denies LOC per patient. ED charge: $4,680."
51:Excerpt: "C5-C6 disc herniation with mild canal narrowing. No prior imaging available for comparison. MRI charge: $2,350."
## case_lib09_spanish_interpreter_espalda
  expected {'explicit_charges_total': 6390, 'counted_amount_ids': ['A1', 'A4', 'A5'], 'amounts_found': 7, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A2', 'reason': "The note's own consult fee; the statement's plural 'consultas' line is $1,300.00 (2 x $650.00) and the packet holds one consult note, so this fee is probably inside that line. Counted once, through the statement line; needs review", 'total_computed': False}, {'amount_id': 'A3', 'reason': 'Rate per session (costo por sesión), not a charge: sessions billed are not stated; needs review', 'total_computed': False}, {'amount_id': 'A6', 'reason': 'Rate per session; the four sessions have no stated charge total; needs review', 'total_computed': False}, {'amount_id': 'A7', 'reason': 'Balance (saldo) equals $1,300.00 + 4 x $400.00; counting it would double count; needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $6,390.00', 'ui_line': 'Accepted charges: $6,390.00', 'notes_lines': ["$650.00: The note's own consult fee; the statement's plural 'consultas' line is $1,300.00 (2 x $650.00) and the packet holds one consult note, so this fee is probably inside that line. Counted once, through the statement line; needs review", '$400.00: Rate per session (costo por sesión), not a charge: sessions billed are not stated; needs review', '$400.00: Rate per session; the four sessions have no stated charge total; needs review', '$2,900.00: Balance (saldo) equals $1,300.00 + 4 x $400.00; counting it would double count; needs review']}
6:Excerpt: "Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940."
11:Excerpt: "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00."
26:Excerpt: "Partial-thickness supraspinatus tear. MRI charge: $2,150."
36:Excerpt: "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00."
## case_lib10_eob_ub04_cms1500
  expected {'explicit_charges_total': 8123.5, 'counted_amount_ids': ['A2', 'A3', 'A4', 'A5'], 'amounts_found': 15, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A1', 'reason': 'Accommodation rate (FL44), not a charge; the FL47 charge on the same line is rate x days; needs review', 'total_computed': False}, {'amount_id': 'A6', 'reason': '0001 line repeats the sum of the four lines; counting it doubles the bill; needs review', 'total_computed': False}, {'amount_id': 'A7', 'reason': 'EOB restates the provider charge and differs from the UB-04 total by $100.00 (mismatch for review); not a second charge; needs review', 'total_computed': False}, {'amount_id': 'A8', 'reason': 'Network discount; not a charge; needs review', 'total_computed': False}, {'amount_id': 'A9', 'reason': 'Allowed amount, not a charge; needs review', 'total_computed': False}, {'amount_id': 'A10', 'reason': 'Payment by the plan; paid vs incurred is a legal question, not a tool decision; needs review', 'total_computed': False}, {'amount_id': 'A11', 'reason': 'Patient responsibility estimate on an EOB; not a charge; needs review', 'total_computed': False}, {'amount_id': 'A12', 'reason': 'Decimal-less CMS-1500 box; truth 185.00 by position, OCR-derived, needs review; needs review', 'total_computed': False}, {'amount_id': 'A13', 'reason': 'Decimal-less box; truth 210.00; needs review', 'total_computed': False}, {'amount_id': 'A14', 'reason': 'Letter O for zero; truth 96.00 for 4 units; needs review', 'total_computed': False}, {'amount_id': 'A15', 'reason': 'Item 28; truth 491.00. The tool compares the line sum with Item 28 in code; needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $8,123.50', 'ui_line': 'Accepted charges: $8,123.50', 'notes_lines': ['$1,640.00: Accommodation rate (FL44), not a charge; the FL47 charge on the same line is rate x days; needs review', '$8,123.50: 0001 line repeats the sum of the four lines; counting it doubles the bill; needs review', '$8,023.50: EOB restates the provider charge and differs from the UB-04 total by $100.00 (mismatch for review); not a second charge; needs review', '$3,610.00: Network discount; not a charge; needs review', '$4,413.50: Allowed amount, not a charge; needs review', '$3,530.80: Payment by the plan; paid vs incurred is a legal question, not a tool decision; needs review', '$882.70: Patient responsibility estimate on an EOB; not a charge; needs review', '18500: Decimal-less CMS-1500 box; truth 185.00 by position, OCR-derived, needs review; needs review', '21000: Decimal-less box; truth 210.00; needs review', '96 OO: Letter O for zero; truth 96.00 for 4 units; needs review', '49100: Item 28; truth 491.00. The tool compares the line sum with Item 28 in code; needs review']}
21:Excerpt: "UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0120 room and board semi-private, FL44 rate $1,640.00 per day, FL46 3 days, FL47 total charges $4,920.00. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00. Rev 0250 pharmacy, 14 units, FL47 total charges $386.50. Rev 0300 laboratory, 6 units, FL47 total charges $712.00. Rev 0001 total charges $8,123.50."
31:Excerpt: "Explanation of benefits, processed 07/03/2026, for dates of service 06/09/2026 to 06/12/2026. This is not a bill. Amount billed $8,023.50; network discount $3,610.00; allowed amount $4,413.50; plan paid $3,530.80; you may owe $882.70."
## case_lib11_priors_and_ledger
  expected {'explicit_charges_total': 6000, 'counted_amount_ids': ['A1', 'A2', 'A3', 'A4'], 'amounts_found': 8, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A5', 'reason': 'Ledger total repeats the three ledger lines above; counting it double counts; needs review', 'total_computed': False}, {'amount_id': 'A6', 'reason': 'Payment, not a charge; needs review', 'total_computed': False}, {'amount_id': 'A7', 'reason': 'Adjustment with a negative sign; not a charge and never netted from billed; needs review', 'total_computed': False}, {'amount_id': 'A8', 'reason': 'Balance = 2,740.00 - 300.00 - 274.00; derived, not a charge; needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $6,000.00', 'ui_line': 'Accepted charges: $6,000.00', 'notes_lines': ['$2,740.00: Ledger total repeats the three ledger lines above; counting it double counts; needs review', '$300.00: Payment, not a charge; needs review', '$274.00: Adjustment with a negative sign; not a charge and never netted from billed; needs review', '$2,166.00: Balance = 2,740.00 - 300.00 - 274.00; derived, not a charge; needs review']}
16:Excerpt: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture. ED charge: $3,260."
46:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection."
## case_lib12_records_review_credibility
  expected {'explicit_charges_total': 5790, 'counted_amount_ids': ['A1', 'A2', 'A3', 'A4'], 'amounts_found': 5, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A5', 'reason': 'Fee schedule rate with no date of service: a rate, not a charge; needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $5,790.00', 'ui_line': 'Accepted charges: $5,790.00', 'notes_lines': ['$145.00: Fee schedule rate with no date of service: a rate, not a charge; needs review']}
11:Excerpt: "Dx: lumbar strain. X-ray lumbar spine negative for fracture. Discharged on ibuprofen. ED charge: $2,780."
51:Excerpt: "Itemized statement: initial evaluation charge $210.00; treatment visits 1 through 16 charge $2,320.00; functional capacity evaluation charge $480.00. Fee schedule $145.00 per visit."
## case_lib13_cloned_notes_cross_provider
  expected {'explicit_charges_total': 5830, 'counted_amount_ids': ['A1', 'A2'], 'amounts_found': 3, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A3', 'reason': 'Estimate of future surgery, not a charge (D-019); needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $5,830.00', 'ui_line': 'Accepted charges: $5,830.00', 'notes_lines': ['$38,500: Estimate of future surgery, not a charge (D-019); needs review']}
11:Excerpt: "Dx: lumbar strain, cervical strain. X-ray lumbar and cervical spine negative for fracture. Discharged home. ED charge: $3,540."
31:Excerpt: "L5-S1 disc protrusion contacting the left S1 nerve root. MRI charge: $2,290."
36:Excerpt: "MRI reviewed. Low back pain 8/10. Recommend microdiscectomy. Estimated surgical cost $38,500."
## case_lib14_handwritten_chiro_scans
  expected {'explicit_charges_total': 4527.05, 'counted_amount_ids': ['A1', 'A5', 'A7'], 'amounts_found': 8, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A2', 'reason': 'Decimal-less CMS-1500 box; truth 255.00 for 3 days; OCR-derived, needs review; needs review', 'total_computed': False}, {'amount_id': 'A3', 'reason': 'Decimal-less box; truth 75.00; needs review', 'total_computed': False}, {'amount_id': 'A4', 'reason': 'Item 28; truth 330.00; needs review', 'total_computed': False}, {'amount_id': 'A6', 'reason': 'Per-mile rate; only the extended line charge ($187.05 = 8.7 x 21.50) is a charge; needs review', 'total_computed': False}, {'amount_id': 'A8', 'reason': 'Invoice total repeats the two lines above; counting it double counts; needs review', 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $4,527.05', 'ui_line': 'Accepted charges: $4,527.05', 'notes_lines': ['25500: Decimal-less CMS-1500 box; truth 255.00 for 3 days; OCR-derived, needs review; needs review', '7500: Decimal-less box; truth 75.00; needs review', '33000: Item 28; truth 330.00; needs review', '$21.50: Per-mile rate; only the extended line charge ($187.05 = 8.7 x 21.50) is a charge; needs review', '$1,567.05: Invoice total repeats the two lines above; counting it double counts; needs review']}
11:Excerpt: "Dx: cervical strain. X-ray cervical spine negative for fracture. Discharged with a muscle relaxant. ED charge: $2,960."
41:Excerpt: "Invoice for the run of 09/14/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00. A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05. Total charges $1,567.05. No payments posted. Letter of protection requested."
## case_lib15_conclusory_letter_mist
  expected {'explicit_charges_total': 3295, 'counted_amount_ids': ['A1', 'A4', 'A5'], 'amounts_found': 11, 'status': 'partial_unclear', 'unclear_items': [{'amount_id': 'A2', 'reason': 'Per-visit rate in a future-care estimate; not a charge; needs review', 'total_computed': False}, {'amount_id': 'A3', 'reason': 'Future care estimate (12 x 150), not incurred (D-019); needs review', 'total_computed': False}, {'amount_id': 'A6', 'reason': 'Statement total repeats the two lines; counting it double counts; needs review', 'total_computed': False}, {'amount_id': 'A7', 'reason': 'Payment; not a charge; needs review', 'total_computed': False}, {'amount_id': 'A8', 'reason': 'Balance = 2,910.00 - 250.00; derived; needs review', 'total_computed': False}, {'amount_id': 'A9', 'reason': 'Affidavit restates the statement total; the attached bill duplicates records 7-8; not counted again; needs review', 'total_computed': False}, {'amount_id': 'A10', 'reason': 'Payment stated in the affidavit; not a charge; needs review', 'total_computed': False}, {'amount_id': 'A11', 'reason': "Affidavit's unpaid amount; not a charge; needs review", 'total_computed': False}], 'letter_line': 'Billed charges stated in these records: $3,295.00', 'ui_line': 'Accepted charges: $3,295.00', 'notes_lines': ['$150.00: Per-visit rate in a future-care estimate; not a charge; needs review', '$1,800.00: Future care estimate (12 x 150), not incurred (D-019); needs review', '$2,910.00: Statement total repeats the two lines; counting it double counts; needs review', '$250.00: Payment; not a charge; needs review', '$2,660.00: Balance = 2,910.00 - 250.00; derived; needs review', '$2,910.00: Affidavit restates the statement total; the attached bill duplicates records 7-8; not counted again; needs review', '$250.00: Payment stated in the affidavit; not a charge; needs review', "$2,660.00: Affidavit's unpaid amount; not a charge; needs review"]}
11:Excerpt: "Seen the day after a low-speed MVC. Neck pain 4/10. Mild paraspinal tenderness. X-ray cervical spine negative. Dx: cervical strain. Charge: $385."
31:Excerpt: "Letter to the attorney dated 01/11/2027. The patient reports she was rear-ended on 2026-10-04 and developed neck pain and headaches. Diagnoses: cervical sprain; post-traumatic headache. Prognosis: guarded. The collision of 2026-10-04 caused all of the injuries and treatment described in this letter. Future care: an estimated 12 additional visits at $150.00 per visit ($1,800.00)."
36:Excerpt: "Itemized statement: new patient exam charge $210.00; treatment visits 1 through 18 charge $2,700.00; total charges $2,910.00. Payment received $250.00 (med pay). Balance due $2,660.00. Account held under letter of protection."
41:Excerpt: "Itemized statement: new patient exam charge $210.00; treatment visits 1 through 18 charge $2,700.00; total charges $2,910.00. Payment received $250.00 (med pay). Balance due $2,660.00. Account held under letter of protection."
46:Excerpt: "Affidavit concerning cost and necessity of services (CPRC 18.001). The custodian of records states the attached records were kept in the regular course of business. Services provided 10/19/2026 through 12/14/2026. Total amount charged: $2,910.00. Amount paid: $250.00. Amount unpaid that the provider has a right to be paid: $2,660.00. The services were necessary and the charges reasonable. Sworn 02/01/2027."
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:31:41.280Z

**tool call — Bash**
````
{
 "command": "grep -l -i \"EOB\\|amount billed\\|duplicate line\\|carry-forward\\|carried forward\\|prior balance\\|running total\" board/cards/*.md | while read f; do echo \"$f: $(grep -m1 '^title' $f | cut -c1-200) $(grep -m1 '^status' $f)\"; done",
 "description": "Search board cards for related billing issues"
}
````

### User / tool · 2026-11-02T13:31:41.567Z

**tool result**
````
board/cards/T-013.md: title: "spec/REQUIREMENTS.md: testable must-haves, stretch pick, non-goals" status: "done"
board/cards/T-015.md: title: "Eval golden set: sample case + 6-10 synthetic stress cases with hand-written expected outputs" status: "done"
board/cards/T-033.md: title: "Amounts, running total, gap rule, accident-date conflict, flag templates" status: "done"
board/cards/T-103.md: title: "Billing as a cited line listing (D-052): remove provider totals and complete badge; keep lines, classifications, unreconciled" status: "done"
board/cards/T-061.md: title: "Self-report label precision: only the patient's own statements (split from T-036 per §7.4)" status: "cancelled"
board/cards/T-078.md: title: "Research: medical-record and billing document formats for synthetic packets" status: "done"
board/cards/T-083.md: title: "Billing analysis on itemized ledgers: billed, adjusted, paid, LOP/lien (code only, cited)" status: "cancelled"
board/cards/T-087.md: title: "PDF hidden-text detection (render vs text layer)" status: "done"
board/cards/T-116.md: title: "Gap rule: an intake form or other administrative record never ends a treatment gap" status: "done"
board/cards/T-140.md: title: "GATE-M2 blocker: ledger totals and balance-due lines classified as charges (lib11 $2,740 total + $2,166 balance counted; letter says $10,906 vs true $6,000)" status: "in_review"
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:31:43.762Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list --status backlog 2>&1 | head -40; python3 tools/board.py list --status ready 2>&1 | head -20; python3 tools/board.py list --status in_progress 2>&1 | head; grep -n -i \"lib10\\|EOB\\|16,147\\|amount billed\" reviews/GATE-M2*.md | head -20",
 "description": "List open cards and gate notes about lib10 EOB"
}
````

### User / tool · 2026-11-02T13:31:44.081Z

**tool result**
````
T-130	M3	backend    	backlog          	P2	AC 0/1	T-105 leftovers: Waddell count forms in credibility.py, statement-line service nouns as charge context, bare insurance/seguro wording
T-135	M3	qa         	backlog          	P2	AC 0/1	Rename the J3 'agrees' test and fix its docstring to the v6 labels (T-109 r3 minor 7)
T-137	M3	qa         	backlog          	P2	AC 0/1	Held-out audit hardening: kill 7 surviving audit mutants, qualify held-out report cells, audit J4, extend scope cut 13c to the plan side (T-113 r2 minors)
T-150	M3	backend    	backlog          	P1	AC 0/1	extract prompt: stop asking for 'charge' sentences in treatment entries (extract_v1 line 12 -> v2); re-record fixtures live; T-139 recommendation
T-144	M2	frontend   	ready            	P1	AC 0/1	UI: show record.uncovered[] as 'Also in this record, not in an entry' under each entry's source, one click to the sentence (legal-nurse GATE-M2 major 2 UI half)
T-147	M3	backend    	ready            	P1	AC 0/1	Perf: flags._hedge_run is quadratic when many hits share one huge unit (24k-char attribution chain takes ~11 s); add a per-unit memo
T-149	M3	frontend   	ready            	P1	AC 0/1	Multi-case UI (Chris inbox 13:23Z): case Overview (list of cases with status, progress bar, HITL call-outs, export ready; sort/filter; open a case) and case Detail (case overview header: progress, call-outs, gate stepper summary, then the breakdown: timeline, flags, amounts, tray)
T-132	M3	backend    	in_progress      	P1	AC 1/1	Prior-condition flag quote stops at a semicolon after an attribution-only clause ('Hx obtained via patient's son; neck pain and headaches.'), and 'Hx per MS history' loses its flag (MS read as Ms.)
T-136	M3	frontend   	in_progress      	P1	AC 1/1	UI: read item.edit_to_check (not just summary edits) so a quote-picker edit held out of the letter offers 'I compared it with the quote' (T-134 follow-up)
T-139	M2	backend    	in_progress      	P0	AC 3/3	GATE-M2 blocker: per-visit rates and dismissed charges reach the carrier letter through treatment-entry summaries/quotes (lib01 'Charge per visit $140', lib03 '$120'); dismissed ED charge listed under Bills to request
T-141	M2	backend    	in_progress      	P1	AC 1/1	GATE-M2 major: lib11 intake 'Prior accidents: No' vs PCP note listing 2019/2022 accidents not flagged as a conflict; a false accident-date 'records disagree' conflict is shown instead
T-142	M2	frontend   	in_progress      	P1	AC 0/1	GATE-M2 major (legal nurse): conflict empty state overclaims ('No conflicts found') though only plan-vs-early-end and denial-vs-history are checked; laterality (lib09 L vs R shoulder) and LOC (lib08) contradictions are not
T-148	M3	backend    	in_progress      	P1	AC 0/1	Multi-case API (Chris inbox 13:23Z): GET /api/cases summary list - per case title, created, run stage, progress (decided/total by kind), HITL call-outs (needs review, edits to check, could-not-verify tray, gate blockers/warnings with plain reasons), export ready
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:31:46.393Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -i gate; grep -n -i \"lib10\\|EOB\\|10,906\\|ledger\" reviews/GATE-M2-summary.md | cut -c1-400 | head -20",
 "description": "Check GATE-M2 summary for lib10 and ledger notes"
}
````

### User / tool · 2026-11-02T13:31:46.498Z

**tool result**
````
GATE-M0-summary.md
GATE-M1-summary.md
GATE-M2-claims-adjuster.md
GATE-M2-legal-nurse.md
GATE-M2-paralegal.md
GATE-M2-privacy-compliance.md
GATE-M2-qa.md
GATE-M2-round1-triage.md
GATE-M2-staff-engineer.md
ugrep: warning: reviews/GATE-M2-summary.md: No such file or directory
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:31:48.579Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"lib10\\|EOB\\|10,906\\|T-140\\|accept-all\\|16,147\" reviews/GATE-M2-round1-triage.md reviews/GATE-M2-*.md | cut -c1-500 | head -30",
 "description": "Search gate reviews for T-140 scope and lib10"
}
````

### User / tool · 2026-11-02T13:31:48.668Z

**tool result**
````
reviews/GATE-M2-round1-triage.md:9:| blocker | paralegal | Ledger total and balance-due lines classed as charges; lib11 letter total $10,906 vs $6,000 | T-140 |
reviews/GATE-M2-round1-triage.md:9:| blocker | paralegal | Ledger total and balance-due lines classed as charges; lib11 letter total $10,906 vs $6,000 | T-140 |
reviews/GATE-M2-paralegal.md:3:Verdict: **fail** (1 blocker, 1 major, 3 minor). The sample case works the way a paralegal needs: every entry has its verbatim quote beside it, "Open record" highlights the quote inside the record, and the letter matches the golden export. The lib11 ledger case does not. The app labels the ledger total ($2,740) and the balance due ($2,166) as "Charge", says the second check agreed, and a plain accept-all puts "Billed charges stated in these records: $10,906.00" in 
reviews/GATE-M2-paralegal.md:30:   "title": "lib11: ledger total and balance due are labelled Charge, and accept-all puts $10,906.00 in the letter (correct: $6,000.00)",
reviews/GATE-M2-paralegal.md:31:   "evidence": "artifacts/review-evidence/GATE-M2-paralegal/l1-body.txt:447 'Detected charges (6)' lists $250.00, $180.00, $2,310.00, $2,740.00 and $2,166.00 all as 'Charge', each with 'Quote matches' and the line 'Quote found word for word, every number in the summary is in the quote, and the second check agreed.' After accepting all six, l4.out.txt:1 reads 'Accepted charges: $10,906.00' and the last line of l4-letter-all6.txt is 'Billed charges stated in these r
reviews/GATE-M2-paralegal.md:32:   "why_it_matters": "The letter tells the carrier billed charges are $10,906, about 80 percent over the records' own $6,000, and it counts the ledger total on top of its own three lines plus a balance that is already net of a payment and a discount. The adjuster checks arithmetic first. The tool gives the paralegal a green 'second check agreed' on exactly the two numbers it should have held back, so the safety net is the reviewer's attention alone. This is a stat
reviews/GATE-M2-paralegal.md:66:  "Is the library packet set meant to be inside the M2 ship bar? If lib11's $10,906 stays a library-only known failure, the product note should say the charge classifier can count a ledger total and balance."
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:31:55.822Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt",
 "content": "SYNTHETIC — invented by claims-adjuster-reviewer for T-140; not real patient data\n\n=== Record 1 ===\nDate: 2026-04-01\nSource: Larkspur Regional ED\nExcerpt: \"Dx: cervical strain. X-ray cervical spine negative for fracture. ED charge: $1,000.\"\n\n=== Record 2 ===\nDate: 2026-05-01\nSource: Brindlewood Physical Therapy, patient statement\nExcerpt: \"Patient statement, statement date 05/01/2026. 04/02/2026 PT evaluation charge $200.00; running total $200.00. 04/09/2026 therapeutic exercise charge $150.00; running total $350.00. 04/16/2026 manual therapy charge $150.00; cumulative charges $500.00. Insurance remit applied to evaluation charge -$120.00. Statement total $500.00. Balance due $380.00.\"\n\n=== Record 3 ===\nDate: 2026-06-01\nSource: Brindlewood Physical Therapy, patient statement\nExcerpt: \"Patient statement, statement date 06/01/2026. Previous statement $380.00. Prior balance carried forward $380.00. 04/16/2026 manual therapy charge $150.00. 05/07/2026 therapeutic exercise charge $150.00. Reversal of 05/07/2026 exercise charge -$150.00. Payment - thank you -$100.00. New charges $300.00. Statement total $300.00. Total amount due $580.00.\"\n\n=== Record 4 ===\nDate: 2026-07-01\nSource: Brindlewood Physical Therapy, account ledger\nExcerpt: \"Date  Description  Charges  Payments  Balance\n06/10/2026  Manual therapy  $150.00  $0.00  $730.00\n06/17/2026  Ins pmt Acme Mutual  $0.00  -$90.00  $640.00\n06/24/2026  Manual therapy  $150.00  $0.00  $790.00\nYear-to-date charges $1,100.00\"\n"
}
````

### User / tool · 2026-11-02T13:31:55.917Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:32:00.604Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-140-adjuster/probe_library.py http://127.0.0.1:7873 @artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt",
 "description": "Paste synthetic ledger into own server"
}
````

### User / tool · 2026-11-02T13:32:00.763Z

**tool result**
````
{
 "create_error": [
  409,
  {
   "error": {
    "code": "demo_mode_unsupported_input",
    "message": "This demo only runs the recorded sample cases.",
    "detail": {}
   }
  }
 ]
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:32:14.586Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_paste.py",
 "content": "\"\"\"T-140 adjuster probe: paste a SYNTHETIC ledger through the real HTTP app (in-process TestClient on the HEAD tree, fixture backend,\nZLAYT_MODE=local). Demo mode refuses unrecorded text (409), so the probe adds the paste's digest to app.state.recorded: the same allow-list\nthe server uses for library cases. Nothing else is patched. Then accept every item, export, and print the total line and amount classes.\nSecond path: evals.library_report.accept_all_total_cents (real export.build_export) on pipeline.run_case output.\nUsage: probe_paste.py TREE_ROOT DB_PATH LEDGER_TXT\"\"\"\nimport json\nimport os\nimport sys\nimport time\n\ntree, db, path = sys.argv[1:4]\nsys.path.insert(0, tree)\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nos.environ.pop(\"ENABLE_LIVE\", None)\nos.environ.pop(\"ANTHROPIC_API_KEY\", None)\nfrom fastapi.testclient import TestClient  # noqa: E402\n\nfrom app.backend import api  # noqa: E402\n\ntext = open(path).read()\napp = api.create_app(db, static_dir=os.path.dirname(db))\napp.state.recorded = set(app.state.recorded) | {api.digest(text)}\nc = TestClient(app, client=(\"127.0.0.1\", 50000))\nr = c.post(\"/api/cases\", json={\"text\": text})\nprint(\"create\", r.status_code)\ntok = r.json()[\"token\"]\nprint(\"records\", [(x.get(\"n\"), x.get(\"source\"), x.get(\"date_iso\")) for x in r.json().get(\"records\", [])])\nprint(\"run\", c.post(f\"/api/cases/{tok}/run\", json={}).status_code)\nfor _ in range(400):\n    s = c.get(f\"/api/cases/{tok}/status\").json()\n    if s[\"status\"] in (\"ready\", \"failed\"):\n        break\n    time.sleep(0.25)\nprint(\"status\", s.get(\"status\"), s.get(\"error\"))\ng = c.get(f\"/api/cases/{tok}\").json()\nfor it in g[\"entries\"] + g[\"amounts\"] + g[\"flags\"]:\n    rr = c.post(f\"/api/cases/{tok}/items/{it['id']}/review\", json={\"action\": \"accept\"})\n    if rr.status_code != 200:\n        print(\"  refused\", it[\"id\"], rr.status_code, json.dumps(rr.json())[:160])\ng = c.get(f\"/api/cases/{tok}\").json()\nprint(\"AMOUNTS (id, kind, state, review, raw, records, reasons)\")\nfor a in g[\"amounts\"]:\n    print(\"  \", a[\"id\"], a.get(\"kind\"), a.get(\"state\"), a.get(\"review_status\"), a.get(\"raw\") or a.get(\"text\"), a.get(\"record_nos\"), a.get(\"reasons\"))\nex = c.get(f\"/api/cases/{tok}/export\")\nprint(\"export\", ex.status_code)\nj = ex.json()\nif ex.status_code == 200:\n    print(\"TOTALS\", j.get(\"totals\"))\n    print(\"LETTER $ LINES\")\n    for ln in j[\"letter_text\"].splitlines():\n        if \"$\" in ln:\n            print(\"  \", ln)\n    notes = j[\"internal_notes_text\"]\n    if \"AMOUNTS NOT TOTALED\" in notes:\n        print(\"NOTES AMOUNTS NOT TOTALED\", notes.split(\"AMOUNTS NOT TOTALED\")[1].split(\"\\n\\n\")[0])\nelse:\n    print(json.dumps(j)[:1500])\n\nfrom app import pipeline  # noqa: E402\nfrom evals import library_report as LR  # noqa: E402\nout = pipeline.run_case(text, \"fixture\")\nprint(\"library_report.accept_all_total_cents:\", LR.accept_all_total_cents(out))\n"
}
````

### User / tool · 2026-11-02T13:32:14.725Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_paste.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:32:19.890Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/tree && /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_paste.py $S/tree $S/paste.sqlite3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/synthetic_paste_out.txt",
 "description": "Paste synthetic ledger through in-process app and export",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T13:32:21.352Z

**tool result**
````
llm call failed call_id=cd3622fc88e0e step=extract attempt=1 prompt_hash=06cbb20d425df1de480eba784a569b68a89f1d36e26485599518762133e46c49
llm call failed call_id=c89e2ed62aeed step=extract attempt=1 prompt_hash=67210be429d72037ae4bdb44fc8b9d4e55a405ba1608a880884bd79225a35c41
llm call failed call_id=ca33340afa260 step=extract attempt=1 prompt_hash=4cf003aab3e02b56590eb17b13652928f103ab2254a6af37ae4352b5cc7c06d1
llm call failed call_id=c7cd47531d38b step=extract attempt=1 prompt_hash=b237b67580e2e4b2b02f204573d41e039d496783ace8912196e0bbfd12eefeea
llm call failed call_id=cb62aaea7b50b step=extract attempt=1 prompt_hash=573d140e92c0b45fc78baca4b9165acf69d16fd424924b1850043830577e06ff
llm call failed call_id=ce4166df46a60 step=j2 attempt=1 prompt_hash=d9832fc3c49b46d5ae4bc578b15414dc399bfeeada9e1aa58b29836b9e318dd0
llm call failed call_id=cc7af36784d80 step=j2 attempt=1 prompt_hash=781ee6d736c3002efe328ab641195187e3fe469b2f817e98bca70af0bb3c4e42
llm call failed call_id=ca3d4e3f90c8d step=j2 attempt=1 prompt_hash=281f9a4096068498b605c124889c32d58cbe15b6f919e8a3dd1ed582d8c0df52
llm call failed call_id=ce072c346cef2 step=j2 attempt=1 prompt_hash=a1808f2bba9ad0f10faffc5d23d009db02fb04ddafbb06e42e3f8d183d2362d8
llm call failed call_id=cceb5b1191446 step=j2 attempt=1 prompt_hash=e292ad7a24cc3cc640cd76e6bcf188cd417d59ddc21878ed64efb6a51ecf8a5a
llm call failed call_id=c19bdf9284361 step=j2 attempt=1 prompt_hash=2dfc6574c23fa2b43f4eef35eea060a2386a36367a1b52baf7361d3f1d33aaed
llm call failed call_id=c5a8ae8b16bad step=j2 attempt=1 prompt_hash=ead15d555c9930c376844c13b41cb9f343257615736b2aaa3fad35df147eed8a
llm call failed call_id=cc66c951de71c step=j2 attempt=1 prompt_hash=afa969777fffc159e6eea67341cf959e13d03bc2e0d4972daac9551d9823b611
llm call failed call_id=cdc0e95263f26 step=j2 attempt=1 prompt_hash=f6258fff674e7c0a249abd3d3946ea82229fe4370ffb608586e763f920823e4f
llm call failed call_id=c5c9883a66ca0 step=j2 attempt=1 prompt_hash=a66e16cc308387958d705509d38f1080b710bf137cbcc6e93ae1fc086ab6915f
llm call failed call_id=c00b030d9b744 step=j2 attempt=1 prompt_hash=695b7029c1df364fe13dbeabdaef05c246bdfdbd37c74c4d90297b5e8dc4b981
llm call failed call_id=cc41cd22c07d5 step=j2 attempt=1 prompt_hash=273518806512893140bd7ac9a01482367b55db2a700f53937c2832a3a4100762
llm call failed call_id=cc247b2513720 step=j2 attempt=1 prompt_hash=5184926fa5a58e6de5b9ef89a280fa83ea4764a26dec34c62a75fb8f5c97ef5a
llm call failed call_id=c05d372653873 step=j2 attempt=1 prompt_hash=23c7fae22cc9af24d8ca553eab7739c53a2d00c37bc227f0a367ce1b4030590b
llm call failed call_id=c99e4f9520bd6 step=j2 attempt=1 prompt_hash=d62095ce81092bdbfc7c495bf722effe83dce19fdf7292d2d4a1ddc5aa77561f
llm call failed call_id=c54aa0be4646c step=j2 attempt=1 prompt_hash=8a922d93bb23799b02a7543af88faa0cd3ec737c4e09fd9929629f6220b58c85
llm call failed call_id=cea97dc95e8b6 step=j2 attempt=1 prompt_hash=d3a7298ed65a0016960876886d91684d0cff26e74c087a3998c880df1a82ac98
llm call failed call_id=c2ca6ec3c2626 step=j2 attempt=1 prompt_hash=180574cc37e408c39b6d3df7f02af9a5f0facdbc498a0d0d59db16a14a729f49
llm call failed call_id=caaf453559eca step=j2 attempt=1 prompt_hash=342208388839e6b0e72f821286257c2767980966566a4e88bd549813f3acb5e0
llm call failed call_id=c7ba5476247f4 step=j2 attempt=1 prompt_hash=16203041ae6469d82c02649b3077175766f67ccc808bb9f16621b044f2962f96
llm call failed call_id=cdac745d3b53f step=j2 attempt=1 prompt_hash=a80cf824291e0568b9236f35355eb6abe70fffe6d18864478b8243c8025345c0
llm call failed call_id=cac87061b4b33 step=flags attempt=1 prompt_hash=49487aba6deeaa810ffe2e6df4e4bc967e96649d7853a9559efe33df9ae13f7f
llm call failed call_id=c9d48a7e718af step=flags attempt=1 prompt_hash=3c3ce5b3b98efe04738cb6157db68d7e764199d9dacc03a66cce74fb3f770fed
llm call failed call_id=cef105cf2d5a0 step=flags attempt=1 prompt_hash=0991ef56d52b19c21d8287f65b827ae3c33bf3c361de312fc506e6ba47a1cc98
llm call failed call_id=cd0347cee564a step=flags attempt=1 prompt_hash=36ca07597affb30d23161e212d07de1c9f873e6835e19ad5032cb285d6216657
llm call failed call_id=c7449c72025b8 step=flags attempt=1 prompt_hash=1edee8a59e4b88d0ce6750a36dd5369ae235ee7279361e53cbfb68026d255531
llm call failed call_id=cb56840b39ff4 step=extract attempt=1 prompt_hash=06cbb20d425df1de480eba784a569b68a89f1d36e26485599518762133e46c49
llm call failed call_id=c65cf805a499f step=extract attempt=1 prompt_hash=4cf003aab3e02b56590eb17b13652928f103ab2254a6af37ae4352b5cc7c06d1
llm call failed call_id=c151d6aba36bf step=extract attempt=1 prompt_hash=67210be429d72037ae4bdb44fc8b9d4e55a405ba1608a880884bd79225a35c41
llm call failed call_id=c6ff866c3b741 step=extract attempt=1 prompt_hash=b237b67580e2e4b2b02f204573d41e039d496783ace8912196e0bbfd12eefeea
llm call failed call_id=c14af6d61d8a9 step=extract attempt=1 prompt_hash=573d140e92c0b45fc78baca4b9165acf69d16fd424924b1850043830577e06ff
llm call failed call_id=c7f676bb52d08 step=j2 attempt=1 prompt_hash=d9832fc3c49b46d5ae4bc578b15414dc399bfeeada9e1aa58b29836b9e318dd0
llm call failed call_id=c7634ccfb8376 step=j2 attempt=1 prompt_hash=781ee6d736c3002efe328ab641195187e3fe469b2f817e98bca70af0bb3c4e42
llm call failed call_id=c63210f20e89f step=j2 attempt=1 prompt_hash=281f9a4096068498b605c124889c32d58cbe15b6f919e8a3dd1ed582d8c0df52
llm call failed call_id=c684ce23ffcde step=j2 attempt=1 prompt_hash=a1808f2bba9ad0f10faffc5d23d009db02fb04ddafbb06e42e3f8d183d2362d8
llm call failed call_id=c7f69170c7be2 step=j2 attempt=1 prompt_hash=e292ad7a24cc3cc640cd76e6bcf188cd417d59ddc21878ed64efb6a51ecf8a5a
llm call failed call_id=c7f74aa93a88e step=j2 attempt=1 prompt_hash=2dfc6574c23fa2b43f4eef35eea060a2386a36367a1b52baf7361d3f1d33aaed
llm call failed call_id=cf3a29b15b026 step=j2 attempt=1 prompt_hash=ead15d555c9930c376844c13b41cb9f343257615736b2aaa3fad35df147eed8a
llm call failed call_id=ce5f61a0beb76 step=j2 attempt=1 prompt_hash=afa969777fffc159e6eea67341cf959e13d03bc2e0d4972daac9551d9823b611
llm call failed call_id=c0926c31e47f8 step=j2 attempt=1 prompt_hash=f6258fff674e7c0a249abd3d3946ea82229fe4370ffb608586e763f920823e4f
llm call failed call_id=cbc5310f3ed13 step=j2 attempt=1 prompt_hash=a66e16cc308387958d705509d38f1080b710bf137cbcc6e93ae1fc086ab6915f
llm call failed call_id=c53222ddffb39 step=j2 attempt=1 prompt_hash=695b7029c1df364fe13dbeabdaef05c246bdfdbd37c74c4d90297b5e8dc4b981
llm call failed call_id=c9273456dcaed step=j2 attempt=1 prompt_hash=273518806512893140bd7ac9a01482367b55db2a700f53937c2832a3a4100762
llm call failed call_id=c14885a15fc6b step=j2 attempt=1 prompt_hash=5184926fa5a58e6de5b9ef89a280fa83ea4764a26dec34c62a75fb8f5c97ef5a
llm call failed call_id=cf2a58d9e7b89 step=j2 attempt=1 prompt_hash=23c7fae22cc9af24d8ca553eab7739c53a2d00c37bc227f0a367ce1b4030590b
llm call failed call_id=c111bef03dd54 step=j2 attempt=1 prompt_hash=d62095ce81092bdbfc7c495bf722effe83dce19fdf7292d2d4a1ddc5aa77561f
llm call failed call_id=cab781950f4ce step=j2 attempt=1 prompt_hash=8a922d93bb23799b02a7543af88faa0cd3ec737c4e09fd9929629f6220b58c85
llm call failed call_id=c15fc682545f3 step=j2 attempt=1 prompt_hash=d3a7298ed65a0016960876886d91684d0cff26e74c087a3998c880df1a82ac98
llm call failed call_id=c1bb110527f42 step=j2 attempt=1 prompt_hash=180574cc37e408c39b6d3df7f02af9a5f0facdbc498a0d0d59db16a14a729f49
llm call failed call_id=c839c9bf2d89e step=j2 attempt=1 prompt_hash=342208388839e6b0e72f821286257c2767980966566a4e88bd549813f3acb5e0
llm call failed call_id=c4a9b4e0ce7e6 step=j2 attempt=1 prompt_hash=16203041ae6469d82c02649b3077175766f67ccc808bb9f16621b044f2962f96
llm call failed call_id=c19c7852d8ee1 step=j2 attempt=1 prompt_hash=a80cf824291e0568b9236f35355eb6abe70fffe6d18864478b8243c8025345c0
llm call failed call_id=c1a5da0732d37 step=flags attempt=1 prompt_hash=49487aba6deeaa810ffe2e6df4e4bc967e96649d7853a9559efe33df9ae13f7f
llm call failed call_id=cf32a96ab7f1f step=flags attempt=1 prompt_hash=3c3ce5b3b98efe04738cb6157db68d7e764199d9dacc03a66cce74fb3f770fed
llm call failed call_id=ccb2168317b0e step=flags attempt=1 prompt_hash=0991ef56d52b19c21d8287f65b827ae3c33bf3c361de312fc506e6ba47a1cc98
llm call failed call_id=c67dc457355e6 step=flags attempt=1 prompt_hash=36ca07597affb30d23161e212d07de1c9f873e6835e19ad5032cb285d6216657
llm call failed call_id=c6f08773627f9 step=flags attempt=1 prompt_hash=1edee8a59e4b88d0ce6750a36dd5369ae235ee7279361e53cbfb68026d255531
create 201
records [(None, None, '2026-04-01'), (None, None, '2026-05-01'), (None, None, '2026-06-01'), (None, None, '2026-07-01'), (None, None, None)]
run 202
status ready None
AMOUNTS (id, kind, state, review, raw, records, reasons)
   a1 charge needs_review accepted $1,000 None ['JUDGE_UNAVAILABLE']
   a2 charge needs_review accepted $200.00 None ['JUDGE_UNAVAILABLE']
   a3 unclear needs_review accepted $200.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a4 charge needs_review accepted $150.00 None ['JUDGE_UNAVAILABLE']
   a5 unclear needs_review accepted $350.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a6 unclear needs_review accepted $500.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a7 unclear needs_review accepted $120.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a8 unclear needs_review accepted $380.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a9 unclear needs_review accepted $380.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a10 charge needs_review accepted $150.00 None ['JUDGE_UNAVAILABLE']
   a11 unclear needs_review accepted $150.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a12 unclear needs_review accepted $100.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a13 unclear needs_review accepted $300.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a14 unclear needs_review accepted $580.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a15 unclear needs_review accepted $150.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a16 unclear needs_review accepted $0.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a17 unclear needs_review accepted $730.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a18 unclear needs_review accepted $90.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a19 unclear needs_review accepted $640.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a20 unclear needs_review accepted $790.00 None ['JUDGE_UNAVAILABLE', 'AMOUNT_UNCLEAR']
   a21 charge needs_review accepted $1,100.00 None ['JUDGE_UNAVAILABLE']
export 422
{"error": {"code": "judge_not_run", "message": "21 accepted items have not had the second AI check, so the export is blocked. Run the second check again.", "detail": {"blockers": [{"item_id": "a1", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.", "rerun_no_answer": false, "next_action": {"code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a1", "judge": "j2"}}}, {"item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.", "rerun_no_answer": false, "next_action": {"code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"}}}, {"item_id": "a3", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.", "rerun_no_answer": false, "next_action": {"code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a3", "judge": "j2"}}}, {"item_id": "a4", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "You accepted this item, but the second AI check never ran on it. Nothing t
library_report.accept_all_total_cents: 260000
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:32:50.456Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; grep -n -A6 \"billing_document\" $S/tree/app/llm/lexicon.yaml | head -20",
 "description": "Look up billing_document lexicon entry"
}
````

### User / tool · 2026-11-02T13:32:50.559Z

**tool result**
````
1322:      - id: billing_document
1323-        pattern: '\b(?:billing\s+statement|itemi[sz]ed\s+(?:bill|statement|charges)|statement\s+of\s+account|account\s+statement|ledger|invoice|explanation\s+of\s+benefits|EOB|UB-?04|HCFA|CMS-?1500|payment\s+(?:history|record)|balance\s+due\s+notice)\b'
1324-      - id: phone_or_message
1325-        pattern: '\b(?:phone|telephone|tel\.?)\s+(?:note|call|encounter|message|contact)\b|\bportal\s+message\b|\bvoicemail\b|\bmessage\s+(?:note|log)\b'
1326-      - id: records_admin
1327-        pattern: '\b(?:records?\s+request|request\s+for\s+records|medical\s+records\s+(?:request|certification|affidavit)|business\s+records\s+affidavit|custodian\s+(?:of\s+records\s+)?affidavit|18\.001\s+affidavit|authorization\s+form|HIPAA\s+authorization|correspondence|cover\s+letter|fax\s+cover|referral\s+(?:form|letter)|prior\s+authori[sz]ation|no-?\s?show\s+(?:notice|letter))\b'
1328-    examples:
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:33:09.674Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_variants.py",
 "content": "\"\"\"T-140 adjuster probe: which SYNTHETIC ledger phrasings that are NOT billed charges still classify as 'charge' (and so reach the letter total\nwhen accepted). Real amounts.extract_amounts + totals.totals on the HEAD tree. Each variant sits in a statement with two real charge lines\n($200.00, $150.00) so the record looks like a ledger. Usage: probe_variants.py TREE_ROOT\"\"\"\nimport sys\n\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import amounts as AM, totals as TT  # noqa: E402\n\nSOURCES = [\"Brindlewood Physical Therapy, billing statement\", \"Brindlewood Physical Therapy, account ledger\"]\nVARIANTS = {\n    \"running total\": [\"Running total $350.00\", \"Running balance $350.00\", \"Cumulative charges $350.00\", \"Year-to-date charges $350.00\",\n                      \"Charges to date $350.00\", \"Total to date $350.00\", \"Accumulated charges $350.00\", \"Sum of charges $350.00\",\n                      \"All charges $350.00\", \"Charges for all visits $350.00\", \"Combined charges $350.00\", \"Aggregate charges billed $350.00\"],\n    \"statement total\": [\"Statement total $350.00\", \"Total, this statement: $350.00\", \"This statement: $350.00\", \"Statement amount $350.00\",\n                        \"Amount of this statement $350.00\", \"Current statement charges $350.00\", \"New charges this statement $350.00\",\n                        \"Statement charges $350.00\", \"Billed this statement $350.00\", \"Invoice amount $350.00\"],\n    \"prior balance / carry-forward\": [\"Previous balance $380.00\", \"Prior balance carried forward $380.00\", \"Balance forward $380.00\",\n                                      \"Previous statement $380.00\", \"Brought forward $380.00\", \"Carried forward charges $380.00\",\n                                      \"Prior charges $380.00\", \"Previous charges $380.00\", \"Opening balance $380.00\", \"Beginning balance $380.00\",\n                                      \"Carry-over from 05/01/2026 statement $380.00\", \"Charges carried from prior statement $380.00\",\n                                      \"Prior statement charges $380.00\", \"Previously billed $380.00\", \"Unpaid prior charges $380.00\"],\n    \"payment or credit shown negative\": [\"Payment -$100.00\", \"Ins pmt -$100.00\", \"Insurance remit -$100.00\", \"Acme Mutual EOB -$100.00\",\n                                         \"Refund of x-ray charge -$100.00\", \"Exercise charge reversed -$100.00\", \"Charge reversal -$100.00\",\n                                         \"Reversal of exercise charge $100.00 CR\", \"Exercise charge reversed $100.00\", \"Med pay applied to visit charge $100.00\",\n                                         \"Remittance $100.00\", \"Collected $100.00\", \"Received $100.00\", \"Insurance check $100.00\",\n                                         \"Void of 05/07 charge $100.00\", \"Charge voided $100.00\", \"Less insurance $100.00\",\n                                         \"Insurance -$100.00\", \"Acme Mutual paid on x-ray charge $100.00\", \"Refund issued $100.00\",\n                                         \"Recoupment of billed $100.00\", \"Visit charge (credit) -$100.00\"],\n}\n\n\ndef classes(text, source):\n    ex = \"Statement date 06/01/2026. PT evaluation charge $200.00; manual therapy charge $150.00. \" + text + \".\"\n    rows = AM.extract_amounts([{\"n\": 1, \"excerpt\": ex, \"source\": source, \"text\": ex, \"date_iso\": \"2026-06-01\"}])\n    tot = TT.totals([{\"cls\": a[\"cls\"], \"cents\": a[\"cents\"], \"review_status\": \"accepted\"} for a in rows])[\"accepted_cents\"]\n    target = [a for a in rows if a[\"raw\"] not in (\"$200.00\", \"$150.00\")]\n    return (target[0][\"cls\"] if target else \"NOT FOUND\"), tot\n\n\nleaks = 0\nfor group, items in VARIANTS.items():\n    print(\"##\", group)\n    for v in items:\n        res = [classes(v, s) for s in SOURCES]\n        flag = \"LEAK\" if any(c == \"charge\" for c, _ in res) else \"ok  \"\n        leaks += flag == \"LEAK\"\n        print(f\"  {flag} {v!r:52} billing-statement: {res[0][0]:8} total ${res[0][1]/100:,.2f} | ledger: {res[1][0]:8} total ${res[1][1]/100:,.2f}\")\nprint(\"LEAKS:\", leaks, \"(true total of the two charge lines is $350.00)\")\n\nprint(\"## duplicate line on two statements (two records, same provider, same service date in the text)\")\nrecs = [{\"n\": 2, \"excerpt\": \"Statement date 05/01/2026. 04/16/2026 manual therapy charge $150.00; 04/09/2026 exercise charge $120.00.\",\n         \"source\": SOURCES[0], \"date_iso\": \"2026-05-01\"},\n        {\"n\": 3, \"excerpt\": \"Statement date 06/01/2026. 04/16/2026 manual therapy charge $150.00; 05/07/2026 exercise charge $130.00.\",\n         \"source\": SOURCES[0], \"date_iso\": \"2026-06-01\"}]\nfor r in recs:\n    r[\"text\"] = r[\"excerpt\"]\nrows = AM.extract_amounts(recs)\nfor a in rows:\n    print(\"  \", a[\"id\"], a[\"record_nos\"], a[\"raw\"], a[\"cls\"], a.get(\"duplicate_note\"))\nprint(\"  accept-all charge total\", TT.totals([{\"cls\": a[\"cls\"], \"cents\": a[\"cents\"], \"review_status\": \"accepted\"} for a in rows])[\"accepted_cents\"] / 100,\n      \"(distinct services stated: 150 + 120 + 130 = 400.00)\")\n\nprint(\"## two distinct same-price services inside ONE statement\")\nex = \"Statement date 05/01/2026. 04/09/2026 manual therapy charge $150.00; 04/16/2026 manual therapy charge $150.00; 04/23/2026 exercise charge $90.00.\"\nrows = AM.extract_amounts([{\"n\": 1, \"excerpt\": ex, \"source\": SOURCES[0], \"text\": ex, \"date_iso\": \"2026-05-01\"}])\nfor a in rows:\n    print(\"  \", a[\"id\"], a[\"record_nos\"], a[\"raw\"], a[\"cls\"], a.get(\"duplicate_note\"))\nprint(\"  accept-all charge total\", TT.totals([{\"cls\": a[\"cls\"], \"cents\": a[\"cents\"], \"review_status\": \"accepted\"} for a in rows])[\"accepted_cents\"] / 100,\n      \"(stated: 150 + 150 + 90 = 390.00)\")\n"
}
````

### User / tool · 2026-11-02T13:33:09.769Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_variants.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:33:14.237Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/tree && /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_variants.py $S/tree 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/variants_out.txt",
 "description": "Sweep ledger phrasings through the HEAD classifier"
}
````

### User / tool · 2026-11-02T13:33:14.444Z

**tool result**
````
## running total
  ok   'Running total $350.00'                              billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Running balance $350.00'                            billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Cumulative charges $350.00'                         billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Year-to-date charges $350.00'                       billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Charges to date $350.00'                            billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Total to date $350.00'                              billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Accumulated charges $350.00'                        billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Sum of charges $350.00'                             billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'All charges $350.00'                                billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Charges for all visits $350.00'                     billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Combined charges $350.00'                           billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Aggregate charges billed $350.00'                   billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
## statement total
  ok   'Statement total $350.00'                            billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Total, this statement: $350.00'                     billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'This statement: $350.00'                            billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Statement amount $350.00'                           billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Amount of this statement $350.00'                   billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Current statement charges $350.00'                  billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'New charges this statement $350.00'                 billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Statement charges $350.00'                          billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Billed this statement $350.00'                      billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Invoice amount $350.00'                             billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
## prior balance / carry-forward
  ok   'Previous balance $380.00'                           billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Prior balance carried forward $380.00'              billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Balance forward $380.00'                            billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  LEAK 'Previous statement $380.00'                         billing-statement: charge   total $730.00 | ledger: charge   total $730.00
  ok   'Brought forward $380.00'                            billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  LEAK 'Carried forward charges $380.00'                    billing-statement: charge   total $730.00 | ledger: charge   total $730.00
  LEAK 'Prior charges $380.00'                              billing-statement: charge   total $730.00 | ledger: charge   total $730.00
  LEAK 'Previous charges $380.00'                           billing-statement: charge   total $730.00 | ledger: charge   total $730.00
  ok   'Opening balance $380.00'                            billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Beginning balance $380.00'                          billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  LEAK 'Carry-over from 05/01/2026 statement $380.00'       billing-statement: charge   total $730.00 | ledger: charge   total $730.00
  LEAK 'Charges carried from prior statement $380.00'       billing-statement: charge   total $730.00 | ledger: charge   total $730.00
  LEAK 'Prior statement charges $380.00'                    billing-statement: charge   total $730.00 | ledger: charge   total $730.00
  LEAK 'Previously billed $380.00'                          billing-statement: charge   total $730.00 | ledger: charge   total $730.00
  LEAK 'Unpaid prior charges $380.00'                       billing-statement: charge   total $730.00 | ledger: charge   total $730.00
## payment or credit shown negative
  ok   'Payment -$100.00'                                   billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Ins pmt -$100.00'                                   billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Insurance remit -$100.00'                           billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Acme Mutual EOB -$100.00'                           billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Refund of x-ray charge -$100.00'                    billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Exercise charge reversed -$100.00'                  billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Charge reversal -$100.00'                           billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  LEAK 'Reversal of exercise charge $100.00 CR'             billing-statement: charge   total $450.00 | ledger: charge   total $450.00
  ok   'Exercise charge reversed $100.00'                   billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  LEAK 'Med pay applied to visit charge $100.00'            billing-statement: charge   total $450.00 | ledger: charge   total $450.00
  ok   'Remittance $100.00'                                 billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Collected $100.00'                                  billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Received $100.00'                                   billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Insurance check $100.00'                            billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  LEAK 'Void of 05/07 charge $100.00'                       billing-statement: charge   total $450.00 | ledger: charge   total $450.00
  ok   'Charge voided $100.00'                              billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Less insurance $100.00'                             billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Insurance -$100.00'                                 billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Acme Mutual paid on x-ray charge $100.00'           billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  ok   'Refund issued $100.00'                              billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
  LEAK 'Recoupment of billed $100.00'                       billing-statement: charge   total $450.00 | ledger: charge   total $450.00
  ok   'Visit charge (credit) -$100.00'                     billing-statement: unclear  total $350.00 | ledger: unclear  total $350.00
LEAKS: 13 (true total of the two charge lines is $350.00)
## duplicate line on two statements (two records, same provider, same service date in the text)
   a1 [2] $150.00 charge None
   a2 [2] $120.00 charge None
   a3 [3] $150.00 charge None
   a4 [3] $130.00 charge None
  accept-all charge total 550.0 (distinct services stated: 150 + 120 + 130 = 400.00)
## two distinct same-price services inside ONE statement
   a1 [1] $150.00 charge Same amount, date and provider appears in records 1.
   a2 [1] $90.00 charge None
  accept-all charge total 240.0 (stated: 150 + 150 + 90 = 390.00)
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:33:28.476Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_variants2.py",
 "content": "\"\"\"T-140 adjuster probe 2: the same running-total and statement-total phrasings when the figure does NOT equal the sum of the record's\nother charges (a cumulative figure that includes earlier statements, or a statement with one detailed line). Then the label rule alone\ndecides. Usage: probe_variants2.py TREE_ROOT\"\"\"\nimport sys\n\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import amounts as AM, totals as TT  # noqa: E402\n\nSRC = \"Brindlewood Physical Therapy, billing statement\"\nLABELS = [\"Running total\", \"Running balance\", \"Cumulative charges\", \"Year-to-date charges\", \"Charges to date\", \"Total to date\", \"Accumulated charges\",\n          \"Sum of charges\", \"All charges\", \"Charges for all visits\", \"Combined charges\", \"Aggregate charges billed\", \"Statement total\",\n          \"Total, this statement:\", \"This statement:\", \"Statement amount\", \"Amount of this statement\", \"Current statement charges\",\n          \"New charges this statement\", \"Statement charges\", \"Billed this statement\", \"Invoice amount\", \"Account total\", \"Total billed to date\",\n          \"Charges since 04/02/2026\", \"Total charges for treatment 04/02/2026 to 06/24/2026\", \"Total charges (all statements)\", \"Total charges\"]\nleaks = 0\nfor lab in LABELS:\n    ex = \"Statement date 06/01/2026. 05/07/2026 exercise charge $150.00; 05/14/2026 manual therapy charge $150.00. \" + lab + \" $730.00.\"\n    rows = AM.extract_amounts([{\"n\": 1, \"excerpt\": ex, \"source\": SRC, \"text\": ex, \"date_iso\": \"2026-06-01\"}])\n    tot = TT.totals([{\"cls\": a[\"cls\"], \"cents\": a[\"cents\"], \"review_status\": \"accepted\"} for a in rows])[\"accepted_cents\"]\n    c = [a[\"cls\"] for a in rows if a[\"raw\"] == \"$730.00\"][0]\n    leak = c == \"charge\"\n    leaks += leak\n    print(f\"  {'LEAK' if leak else 'ok  '} {lab!r:58} {c:8} accept-all total ${tot/100:,.2f}\")\nprint(\"LEAKS:\", leaks, \"(stated line charges: $150.00 + $150.00 = $300.00; the two lines merge by dedupe, see probe_variants.py)\")\n"
}
````

### User / tool · 2026-11-02T13:33:28.574Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_variants2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:33:35.454Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster && sed -i '' 's/manual therapy charge \\$150.00. \" + lab/manual therapy charge $160.00. \" + lab/; s/\\$150.00 + \\$150.00 = \\$300.00; the two lines merge by dedupe, see probe_variants.py/$150.00 + $160.00 = $310.00/' probe_variants2.py && grep -n \"160\" probe_variants2.py && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd $S/tree && /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/probe_variants2.py $S/tree 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/variants2_out.txt",
 "description": "Fix line values and run mismatched running-total sweep"
}
````

### User / tool · 2026-11-02T13:33:35.663Z

**tool result**
````
17:    ex = "Statement date 06/01/2026. 05/07/2026 exercise charge $150.00; 05/14/2026 manual therapy charge $160.00. " + lab + " $730.00."
24:print("LEAKS:", leaks, "(stated line charges: $150.00 + $160.00 = $310.00)")
  ok   'Running total'                                            unclear  accept-all total $310.00
  ok   'Running balance'                                          unclear  accept-all total $310.00
  LEAK 'Cumulative charges'                                       charge   accept-all total $1,040.00
  LEAK 'Year-to-date charges'                                     charge   accept-all total $1,040.00
  ok   'Charges to date'                                          unclear  accept-all total $310.00
  ok   'Total to date'                                            unclear  accept-all total $310.00
  LEAK 'Accumulated charges'                                      charge   accept-all total $1,040.00
  LEAK 'Sum of charges'                                           charge   accept-all total $1,040.00
  LEAK 'All charges'                                              charge   accept-all total $1,040.00
  ok   'Charges for all visits'                                   unclear  accept-all total $310.00
  LEAK 'Combined charges'                                         charge   accept-all total $1,040.00
  LEAK 'Aggregate charges billed'                                 charge   accept-all total $1,040.00
  ok   'Statement total'                                          unclear  accept-all total $310.00
  LEAK 'Total, this statement:'                                   charge   accept-all total $1,040.00
  LEAK 'This statement:'                                          charge   accept-all total $1,040.00
  LEAK 'Statement amount'                                         charge   accept-all total $1,040.00
  LEAK 'Amount of this statement'                                 charge   accept-all total $1,040.00
  LEAK 'Current statement charges'                                charge   accept-all total $1,040.00
  LEAK 'New charges this statement'                               charge   accept-all total $1,040.00
  LEAK 'Statement charges'                                        charge   accept-all total $1,040.00
  LEAK 'Billed this statement'                                    charge   accept-all total $1,040.00
  ok   'Invoice amount'                                           unclear  accept-all total $310.00
  ok   'Account total'                                            unclear  accept-all total $310.00
  ok   'Total billed to date'                                     unclear  accept-all total $310.00
  ok   'Charges since 04/02/2026'                                 unclear  accept-all total $310.00
  ok   'Total charges for treatment 04/02/2026 to 06/24/2026'     unclear  accept-all total $310.00
  ok   'Total charges (all statements)'                           unclear  accept-all total $310.00
  ok   'Total charges'                                            unclear  accept-all total $310.00
LEAKS: 15 (stated line charges: $150.00 + $160.00 = $310.00)
[This command modified 1 file you've previously read: artifacts/review-evidence/T-140-adjuster/probe_variants2.py. Call Read before editing.]
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:33:45.573Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/tree && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_amounts_t140.py tests/unit/test_amounts.py tests/unit/test_billing.py tests/unit/test_export.py -q -p no:cacheprovider 2>&1 | tail -8",
 "description": "Run T-140 and related amount/export unit tests on HEAD tree",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T13:33:51.782Z

**tool result**
````
........................................................................ [ 15%]
........................................................................ [ 31%]
........................................................................ [ 47%]
........................................................................ [ 63%]
........................................................................ [ 78%]
........................................................................ [ 94%]
.........................                                                [100%]
457 passed in 5.89s
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:33:57.477Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/tree && env LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.library_report --help 2>&1 | head -5; sed -n 67,77p evals/library_report.py",
 "description": "Check library report CLI options"
}
````

### User / tool · 2026-11-02T13:33:57.611Z

**tool result**
````
usage: python -m evals.library_report [-h] [--out OUT]

options:
  -h, --help  show this help message and exit
  --out OUT
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
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:34:02.696Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/tree && env LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.library_report --out $S/library-report.md 2>&1 | grep -v \"llm call failed\" | tail -3; grep \"^| case\" $S/library-report.md | cut -d'|' -f2,7",
 "description": "Run library report eval and show accept-all column",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T13:34:04.154Z

**tool result**
````
| case_lib01_er_only_then_gap | r3 | LLM_FAILED_AFTER_RETRIES | FIXTURE_MISS |

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
 case_lib01_er_only_then_gap | ok 
 case_lib02_slip_fall_prior_knee | ok 
 case_lib03_truck_rear_end_chiro | ok 
 case_lib04_dog_bite_scar_revision | WRONG $4,730.00 vs $8,630.00 
 case_lib05_pedestrian_orif_hardware | WRONG $38,420.00 vs $44,570.00 
 case_lib06_lop_billed_vs_adjusted | WRONG $6,380.00 vs $6,830.00 
 case_lib07_parking_lot_fall_outside_records | ok 
 case_lib08_second_crash_mri_after | ok 
 case_lib09_spanish_interpreter_espalda | WRONG $5,090.00 vs $6,390.00 
 case_lib10_eob_ub04_cms1500 | WRONG $16,147.00 vs $8,123.50 
 case_lib11_priors_and_ledger | ok 
 case_lib12_records_review_credibility | ok 
 case_lib13_cloned_notes_cross_provider | ok 
 case_lib14_handwritten_chiro_scans | ok 
 case_lib15_conclusory_letter_mist | ok 
 case_lib01_er_only_then_gap
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:34:52.331Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; grep -n \"_STATEMENT = \\|_CHARGE_END = \\|(\\\"payment\\\", r\\|(\\\"balance\\\", r\\|if _STATEMENT.search\\|def _likely_totals\\|len(ch) \\|key = (a.get(\\\"date\\\")\" $S/tree/app/backend/amounts.py | cut -c1-160; kill 88162; sleep 1; lsof -nP -t -iTCP:7873 -sTCP:LISTEN; echo \"port check done\"",
 "description": "Get evidence line numbers and stop server by PID"
}
````

### User / tool · 2026-11-02T13:34:53.607Z

**tool result**
````
20:_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
21:_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
104:    ("balance", r"balance|amount\s+(?:due|owed)|amt\.?\s+due|(?:payment|now|total)\s+due|owed|outstanding", 5,
106:    ("payment", r"paid|payments?|pmts?|co-?pay(?:ment)?s?", 5, "Payment: money received, not a charge."),
164:    if _STATEMENT.search(label) and (source is None or _is_billing_source(source)):
171:def _likely_totals(rows: list) -> set:
176:    return {i for i in ch if len(ch) >= 3 and total - rows[i]["cents"] == rows[i]["cents"]}
224:        key = (a.get("date"), _norm(a.get("provider")), _norm(a.get("text")), a.get("cls"), a.get("cents")) if a.get("cents") is not None else None
port check done
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:34:55.774Z

**tool call — Bash**
````
{
 "command": "ls /Users/arsis/zlayt-pm-project/reviews/ | grep T-140; ls /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/",
 "description": "Check for existing T-140 reviews and evidence files"
}
````

### User / tool · 2026-11-02T13:34:55.904Z

**tool result**
````
library_accept_all.txt
probe_library.py
probe_paste.py
probe_variants.py
probe_variants2.py
synthetic_ledger.txt
synthetic_paste_out.txt
variants2_out.txt
variants_out.txt
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:35:52.974Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-140-claims-adjuster.md",
 "content": "# T-140 — claims-adjuster-reviewer (Gary Pruitt, BI adjuster / defense adversary)\n\n**Verdict: fail** (4 blockers, 0 majors, 1 minor). Commit 78554d1 (HEAD), run from a `git archive HEAD` copy in my scratchpad: own server on 127.0.0.1:7873, `LLM_BACKEND=fixture`, `ZLAYT_MODE=local`, `ZLAYT_DB` in the scratchpad. The server was stopped by PID 88162 and the port check came back empty.\n\nlib11 is fixed. If you accept everything, the letter reads \"Billed charges stated in these records: $6,000.00\". The internal notes give the reason each of $2,740 / $300 / $274 / $2,166 was left out. I checked that by hand: $3,260 + $250 + $180 + $2,310 = $6,000.\n\nThe fix depends on a closed list of label words, though, and a ledger that uses other ordinary wording still inflates the letter total:\n- My SYNTHETIC two-statement ledger (`artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt`) puts **$2,600.00** in the letter. The records state $1,950.00 of distinct services. The overstatement comes from a \"Year-to-date charges $1,100.00\" running total that was counted as a charge, plus the 04/16 visit counted on both statements. Two real $150 lines also drop out because they merge with each other.\n- Label sweep: of 28 running/statement-total labels, 15 are classed as a charge when the figure does not happen to equal the sum of the record's other lines. 9 of 15 prior-balance/carry-forward wordings are classed as a charge, and so are 4 of 22 credit/payment wordings.\n- Across the library, lib10 (EOB) still prints **$16,147.00**. The records state $8,123.50.\n\nFor me, an inflated \"billed charges\" figure is the first thing I'd put in a response letter: if one number is wrong, I discount the whole package.\n\nDeterministic checks first: `pytest tests/unit/test_amounts_t140.py tests/unit/test_amounts.py tests/unit/test_billing.py tests/unit/test_export.py -q` on the HEAD tree gave `457 passed in 5.89s`. `python -m evals.library_report` on the HEAD tree reported the accept-all column `WRONG $16,147.00 vs $8,123.50` for lib10 and WRONG for lib04/05/06/09. The other 10 cases were ok.\n\nLibrary accept-all results, checked by hand against the records:\n\n| case | letter | records | note |\n|---|---|---|---|\n| lib01 | $3,915 | $3,915 | ok |\n| lib02 | $2,260 | $2,260 | ok |\n| lib03 | $7,500 | $7,500 | ok |\n| lib04 | $4,730 | $8,630 | under; surgeon fee left unclear |\n| lib05 | $38,420 | $44,570 | under |\n| lib06 | $6,380 | $6,830 | under; balance $1,550, adjustment $1,250 and amount due $1,150 correctly unclear |\n| lib07 | $2,620 | $2,620 | ok |\n| lib08 | $11,240 | $11,240 | ok |\n| lib09 | $5,090 | $6,390 | under |\n| lib10 | **$16,147.00** | $8,123.50 | **over: EOB \"Amount billed $8,023.50\" counted on top of the UB-04 lines** |\n| lib11 | $6,000 | $6,000 | ok |\n| lib12 | $5,790 | $5,790 | ok |\n| lib13 | $5,830 | $5,830 | ok |\n| lib14 | $4,527.05 | $4,527.05 | ok |\n| lib15 | $3,295 | $3,295 | ok; the duplicate statement and the 18.001 affidavit restatement are not counted |\n\nWhere the synthetic paste ran: the paste through my HTTP server returned `409 demo_mode_unsupported_input` (fixture demo mode). I then ran the same paste through the real app in-process (TestClient on the HEAD tree). The only change was adding the paste's digest to `app.state.recorded`, the allow-list the server uses for library cases. With every item accepted, export returned `422 judge_not_run` because the fixture has no recorded judge answers. The letter line therefore comes from the real `export.build_export` via `evals.library_report.accept_all_total_cents`, which returned 260000. Amount classes are code-only, and the handoff says the judge cannot change them.\n\n```json\n{\"card\": \"T-140\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"commit 78554d1 (HEAD) via git archive into the session scratchpad; app on http://127.0.0.1:7873 (LLM_BACKEND=fixture, ZLAYT_MODE=local, ZLAYT_DB in scratchpad); all 15 evals/library cases accept-all + export; SYNTHETIC ledger artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt; app/backend/amounts.py diff\",\n \"exercised\": [\n  \"python3 tools/board.py show T-140; git show HEAD -- app/backend/amounts.py\",\n  \"git archive HEAD | tar -x into scratchpad/tree; server pid 88162 on :7873, /api/health backend=fixture demo_mode=true; stopped with kill 88162, lsof -t -iTCP:7873 empty\",\n  \"pytest tests/unit/test_amounts_t140.py test_amounts.py test_billing.py test_export.py on HEAD tree: 457 passed in 5.89s\",\n  \"python -m evals.library_report on HEAD tree: accept-all WRONG for lib04, lib05, lib06, lib09, lib10 ($16,147.00 vs $8,123.50); ok for the other 10\",\n  \"artifacts/review-evidence/T-140-adjuster/probe_library.py: for each of the 15 library cases, POST /api/cases {library}, run, accept every entry/amount/flag, GET export, read the 'Billed charges stated in these records' line and amount classes (library_accept_all.txt); lib11 = $6,000.00 and the AMOUNTS NOT TOTALED notes give the reasons for $2,740/$300/$274/$2,166\",\n  \"hand-recomputed every library total against the $ lines of evals/library/*.txt\",\n  \"pasted SYNTHETIC ledger (running totals, Statement total, prior balance carried forward, 04/16 line on two statements, negative payments, columned ledger): HTTP paste refused 409 in demo mode; in-process TestClient with the digest allow-listed gave the amount classes, and export.build_export gave $2,600.00 (synthetic_paste_out.txt)\",\n  \"artifacts/review-evidence/T-140-adjuster/probe_variants.py and probe_variants2.py: 93 ledger phrasings through amounts.extract_amounts + totals.totals with a billing-statement and a ledger source (variants_out.txt, variants2_out.txt)\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"lib11_fix\": 5, \"letter_total_not_inflated_beyond_lib11\": 1, \"not_totaled_reasons_in_internal_notes\": 4, \"robustness_to_ledger_wording\": 1},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"Running-total, statement-total and carried-forward lines without the exact words total/balance/paid/adjustment are still classed 'charge' and added to the letter total\",\n   \"evidence\": \"variants2_out.txt: with a figure that is not the sum of the record's lines, 15 of 28 labels are charge: 'Cumulative charges', 'Year-to-date charges', 'Accumulated charges', 'Sum of charges', 'All charges', 'Combined charges', 'Aggregate charges billed', 'Total, this statement:', 'This statement:', 'Statement amount', 'Amount of this statement', 'Current statement charges', 'New charges this statement', 'Statement charges', 'Billed this statement' -> 'charge   accept-all total $1,040.00' where the stated lines are $310.00. variants_out.txt: 'LEAK 'Previous statement $380.00' ... charge total $730.00' (lines $350.00), plus 'Carried forward charges', 'Prior charges', 'Previous charges', 'Carry-over from 05/01/2026 statement', 'Charges carried from prior statement', 'Prior statement charges', 'Previously billed', 'Unpaid prior charges'. End to end: synthetic_paste_out.txt 'a21 charge ... $1,100.00' ('Year-to-date charges $1,100.00') and 'library_report.accept_all_total_cents: 260000' = letter 'Billed charges stated in these records: $2,600.00' vs $1,950.00 of distinct services stated. Causes: the _NC_KINDS word list (amounts.py:103-108) has no running/cumulative/year-to-date/previous/prior/carried/forward/all/combined/statement words; _STATEMENT (amounts.py:20, used at :164) still turns any 'statement' or 'billed' label on a billing source into a charge; the comma split in _label leaves 'this statement:' as the label of 'Total, this statement: $X'; the cross-check (amounts.py:176) only catches a figure exactly equal to the sum of the same record's other charges, and a cumulative figure on statement 2 never is.\",\n   \"why_it_matters\": \"This is the same defect class as the GATE-M2 blocker the card exists to close: a ledger summary line counted as a charge. On my desk a demand that states $2,600 in billed charges when the itemized lines add to $1,950 is overstated, and I would use it to discount the whole specials package. lib11 passes only because its total line happens to use the word 'total'.\",\n   \"fix\": \"Invert the rule on billing documents: an amount is a charge only when its own line names a service, procedure, CPT/HCPCS/revenue code or date of service with a charge word. Statement-, period- and account-level figures (statement, previous/prior, carried/brought forward, cumulative, year-to-date, to date, all, combined, aggregate, sum) are 'unclear' with a reason. Drop 'statement' and 'billed' from the _STATEMENT charge rule, or limit it to a line with a service noun. Do the label check before the clause split, or across the comma.\",\n   \"acceptance_test\": \"Parametrized unit test over these 28 + 15 phrasings (figure not equal to the sum of the other lines, billing-statement and ledger sources): none is class charge. HTTP test: the SYNTHETIC two-statement ledger in artifacts/review-evidence/T-140-adjuster/synthetic_ledger.txt (or a qa copy) accepted in full exports a total with no running, year-to-date or carried-forward figure in it.\"},\n  {\"severity\": \"blocker\",\n   \"title\": \"Credits, reversals, voids, recoupments and med-pay applications written without a minus sign are added as positive charges\",\n   \"evidence\": \"variants_out.txt: 'LEAK 'Reversal of exercise charge $100.00 CR' billing-statement: charge total $450.00', 'LEAK 'Med pay applied to visit charge $100.00' ... charge total $450.00', 'LEAK 'Void of 05/07 charge $100.00' ... charge total $450.00', 'LEAK 'Recoupment of billed $100.00' ... charge total $450.00' (stated charge lines: $350.00). The same wordings with '-$' stay unclear only because the '-' sits between the label and '$' and breaks _CHARGE_END's end anchor (amounts.py:21), not because of a credit rule. find_amounts drops the sign, so a credit counted as a charge is added, never netted. The payment pattern (amounts.py:106) has no 'pay'/'med pay'/'applied'; there is no reversal/void/refund/recoupment/CR word.\",\n   \"why_it_matters\": \"A payment or credit counted as a billed charge inflates the specials and, worse, reads as money the plaintiff was charged twice. Texas paid-or-incurred discovery turns up exactly these ledger lines, and an adjuster who finds a credit summed as a charge has a ready attack on every number in the letter.\",\n   \"fix\": \"Add reversal, void, refund, recoup(ment), 'CR' suffix, '(credit)', 'applied', 'med pay'/'PIP' to the non-charge kinds. A figure with a leading '-' or in parentheses '($X)' on a billing document is never a charge, whatever its label.\",\n   \"acceptance_test\": \"Unit test: the 4 leaking wordings above plus '($100.00)' and '$100.00 CR' are unclear with a payment or adjustment reason; the accept-all total of the test statement stays $350.00.\"},\n  {\"severity\": \"blocker\",\n   \"title\": \"lib10: EOB 'Amount billed $8,023.50' is counted on top of the UB-04 lines; the letter claims $16,147.00 against $8,123.50 in the records\",\n   \"evidence\": \"library_accept_all.txt '## case_lib10_eob_ub04_cms1500 ... ['Billed charges stated in these records: $16,147.00']' with 'a7 charge verified accepted $8,023.50'; evals/library/case_lib10_eob_ub04_cms1500.txt line 31: 'Explanation of benefits ... This is not a bill. Amount billed $8,023.50'; expected.json explicit_charges_total 8123.5, A7 'EOB restates the provider charge ... not a second charge'. library_report on HEAD: 'case_lib10_eob_ub04_cms1500 | WRONG $16,147.00 vs $8,123.50'. Handoff: 'lib10: EOB Amount billed $8,023.50 still charge, M1 ... not touched'. No open card covers it: python3 tools/board.py list --status backlog/ready/in_progress shows none.\",\n   \"why_it_matters\": \"The letter nearly doubles the billed specials. An EOB's 'amount billed' is the claim-level total of the provider's bill restated by the payer, the same 'restated total' the card's AC1 bars, on another document. I would cite the $8,023.50 EOB line and the $8,123.50 UB-04 total line to show the demand counted one hospital bill twice.\",\n   \"fix\": \"On an EOB, remittance or other payer document (lexicon billing_document already matches 'explanation of benefits|EOB'), 'amount billed', 'billed charges', 'total billed' and 'provider charges' are restatements: class unclear with the reason 'Payer restates the provider's bill; not a second charge.' If a separate card owns it, open it as P0 before GATE-M2 reruns.\",\n   \"acceptance_test\": \"Library accept-all for lib10 exports 'Billed charges stated in these records: $8,123.50'; library_report shows lib10 ok.\"},\n  {\"severity\": \"blocker\",\n   \"title\": \"Duplicate service lines on two statements are counted twice; two distinct same-price lines in one statement collapse into one\",\n   \"evidence\": \"variants_out.txt '## duplicate line on two statements': record 2 '04/16/2026 manual therapy charge $150.00' and record 3 '04/16/2026 manual therapy charge $150.00' -> 'a1 [2] $150.00 charge None' and 'a3 [3] $150.00 charge None', 'accept-all charge total 550.0 (distinct services stated: 150 + 120 + 130 = 400.00)'. '## two distinct same-price services inside ONE statement': 04/09 and 04/16 manual therapy $150.00 -> 'a1 [1] $150.00 charge Same amount, date and provider appears in records 1.', 'accept-all charge total 240.0 (stated: 150 + 150 + 90 = 390.00)'. Cause: dedupe key amounts.py:224 is (record date, provider, record text, class, cents). It has no service date, so the same visit on two statements never merges, and two visits in one record always do. Pre-existing; not in the 78554d1 diff.\",\n   \"why_it_matters\": \"Re-listing open charges on the next statement is the normal format for a provider statement. Counting them again is the double-count I check for first, and the merge loses a stated charge. Both make the total wrong, and either one lets me say the demand's arithmetic doesn't match its bills.\",\n   \"fix\": \"Dedupe charge lines by (provider, service date stated in the line, description, cents) across records. Never merge two lines of the same record that have different service dates or positions. When it does merge, the duplicate note names both records and the service date.\",\n   \"acceptance_test\": \"Unit test with the two probe fixtures: cross-statement total 400.00 with one item citing records 2 and 3; same-statement total 390.00 with two $150 items.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Accept-all under-counts on lib04, lib05, lib06, lib09 (fees left unclear); outside my adversary lens\",\n   \"evidence\": \"library_report on HEAD: 'lib04 ... WRONG $4,730.00 vs $8,630.00', 'lib05 ... WRONG $38,420.00 vs $44,570.00', 'lib06 ... WRONG $6,380.00 vs $6,830.00', 'lib09 ... WRONG $5,090.00 vs $6,390.00' (e.g. lib04 'Surgeon fee: $3,900' class unclear).\",\n   \"why_it_matters\": \"An understated total does not help me, but the letter's 'stated in these records' figure is still not what the records state. The handoff lists these cases as known. Context only.\",\n   \"fix\": \"Track on its own card (fee/charge vocabulary), or record it in SCOPE_CUTS.\",\n   \"acceptance_test\": \"library_report accept-all ok for these four, or a SCOPE_CUTS row naming them.\"}\n ],\n \"whats_right\": [\n  \"lib11 accept-all letter is $6,000.00 and the internal notes give each of $2,740/$300/$274/$2,166 a plain reason; no ledger figure reaches the letter\",\n  \"The code rule beats the judge: lib11 $2,740/$300/$2,166 stay unclear with JUDGE_DISAGREES, and explicit Total/Statement total/Balance due/Payment/Adjustment/-$ lines are never charges\",\n  \"lib15's duplicate statement and 18.001 affidavit restatement are not counted again ($3,295.00 correct)\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T13:35:53.168Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-140-claims-adjuster.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:35:55.629Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json,re\nt=open('reviews/T-140-claims-adjuster.md').read(); f=chr(96)*3\nb=t.split(f+'json')[1].split(f)[0]; d=json.loads(b)\nprint(d['verdict'], [x['severity'] for x in d['findings']], len(d['exercised']))\"; python3 tools/board.py validate 2>&1 | tail -3",
 "description": "Validate review JSON block and board"
}
````

### User / tool · 2026-11-02T13:35:55.808Z

**tool result**
````
fail ['blocker', 'blocker', 'blocker', 'blocker', 'minor'] 8
ok (150 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:36:05.259Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_t140_ledger_label_leaks.md",
 "content": "---\nname: t140-ledger-label-leaks\ndescription: T-140 r0 (78554d1) fail - lib11 $6,000 fixed but closed word list leaks running/YTD/previous/statement labels, CR credits, EOB 'Amount billed' (lib10 $16,147), cross-statement duplicates; how to paste unrecorded text in fixture mode\nmetadata:\n  type: project\n---\n\nT-140 r0 at 78554d1, verdict fail (4 blockers). lib11 accept-all is $6,000.00, correct. The non-charge rule is a closed word list (total/balance/paid/adjustment).\nLeaks: 'Cumulative/Year-to-date/All/Combined/Statement charges', 'Previous statement', 'Prior/Previous charges', 'Previously billed', 'Total, this statement:'\n(the comma split leaves 'this statement:'), and credits written without '-' ('$100.00 CR', 'Void of ... charge', 'Med pay applied to ... charge').\nThe cross-check only catches a figure that equals the sum of the same record's other charges exactly, so test the sweep with a NON-matching figure\n(the first sweep looked clean because of that). lib10 still prints $16,147.00 vs $8,123.50 because of the EOB 'Amount billed'. The dedupe key (record date, text, cents)\ncounts a line twice when it appears on two statements, and merges two different same-price visits that sit in one record.\n\n**Why:** a fix keyed on the library wording passes its own fixture; a ledger worded differently inflates the letter again.\n\n**How to apply:** next round, rerun artifacts/review-evidence/T-140-adjuster/probe_variants.py, probe_variants2.py and probe_paste.py on the new commit.\nIn demo mode, unrecorded paste text gets a 409. Put an in-process TestClient on the tree and add api.digest(text) to app.state.recorded (the library allow-list).\nExport then returns 422 judge_not_run, so read the letter line through evals.library_report.accept_all_total_cents (the real build_export).\n\nRelated: [[gate-m2-curated-vs-recorded]], [[spare-port-app-server]], [[reviewer-write-and-parse-guards]].\n"
}
````

### User / tool · 2026-11-02T13:36:05.356Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_t140_ledger_label_leaks.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:36:07.233Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer && printf '%s\\n' \"- [T-140 ledger label leaks](project_t140_ledger_label_leaks.md) — r0 78554d1 fail: word list leaks YTD/previous/statement/CR; lib10 EOB \\$16,147; paste via allow-listed TestClient\" | tee -a MEMORY.md | tail -1",
 "description": "Add T-140 memory pointer to the index"
}
````

### User / tool · 2026-11-02T13:36:07.338Z

**tool result**
````
- [T-140 ledger label leaks](project_t140_ledger_label_leaks.md) — r0 78554d1 fail: word list leaks YTD/previous/statement/CR; lib10 EOB $16,147; paste via allow-listed TestClient
````

### Assistant · claude-opus-5-5 · 2026-11-02T13:36:10.217Z

T-140 fails with 4 blockers, 0 majors and 1 minor. lib11 now prints $6,000.00, but my SYNTHETIC ledger prints $2,600.00 against $1,950.00 of stated services: "Year-to-date charges", "Previous statement", "$100.00 CR" credits and lines repeated on two statements still count. lib10 prints $16,147.00 against $8,123.50.
Review is at /Users/arsis/zlayt-pm-project/reviews/T-140-claims-adjuster.md (evidence in /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-140-adjuster/); my server, PID 88162, is stopped, and the synthetic paste got a 409 in demo mode, so it ran in-process and its total came from the real export builder.
