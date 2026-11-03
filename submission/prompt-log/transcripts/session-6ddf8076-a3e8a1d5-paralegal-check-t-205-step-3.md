# Subagent: Paralegal check: T-205 Step 3 (Paralegal check: T-205 Step 3)

Source: `agent-a3e8a1d589c4850e9.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T00:32:26.334Z

Check T-205 in /Users/arsis/zlayt-pm-project as the senior PI paralegal, starting from a fresh context. The card is commit 203ac6a; read the handoff and D-071.

Extract a fresh `git archive 203ac6a` into an empty directory and run demo mode on your own port; stop your PID afterward. In guided Step 3 for case_09, lib10 and lib11, check:
- the date of service shown matches what the letter prints;
- the statement date is labeled as a statement date;
- where a line's date isn't certain, the confirm note is plain and tells you what to do.

T-202 round 3 may later change which lines are certain; grade only the display. Report private values only as <redacted>. Write reviews/T-205-paralegal.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:32:27.687Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-03T00:32:27.695Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:32:28.344Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-205 | head -80; grep -n \"D-071\" -A25 memory/ORCHESTRATOR_DECISIONS.md | head -60"
}
````

### User / tool · 2026-11-03T00:32:28.497Z

**tool result**
````
---
id: "T-205"
title: "Guided Step 3 shows the same service date the letter prints (amounts[].service_date.text) and the confirm note when the date is not certain"
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T00:19:55Z"
updated_at: "2026-11-03T00:32:23Z"
claimed_by: "frontend"
claimed_at: "2026-11-03T00:20:14Z"
rounds: 0
commits: ["203ac6a"]
reviews: []
ac:
  - {"n": 1, "text": "Step 3 charge view shows service_date.text (never the statement date as the service date); when confirm_note is present it is shown in plain words next to the quote; e2e on case_09, lib10 and a not-stated line; full guided suite green from a fresh archive", "done": true, "evidence": "tests/e2e/guided/test_t205.py (case_09, lib10, counted no-date line, stubbed note, phone) + full guided suite and test_no_console_errors: 143 passed from git archive of tree 3433a29 with E2E_REQUIRE_DB=1"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T00:20:14Z frontend: claimed
- 2026-11-03T00:24:50Z frontend: Step 3 charge screen: Date of service line = service_date.text verbatim (statement date named as such in sub/src head), confirm_note leads the card foot (attn) in plain words; done list column Date of service. step3.js/css only, review.js untouched. New tests/e2e/guided/test_t205.py (case_09, lib10, D-064 counted no-date, stubbed note case, phone). Running archive suite.
- 2026-11-03T00:32:15Z frontend: AC 1 checked: tests/e2e/guided/test_t205.py (case_09, lib10, counted no-date line, stubbed note, phone) + full guided suite and test_no_console_errors: 143 passed from git archive of tree 3433a29 with E2E_REQUIRE_DB=1
- 2026-11-03T00:32:15Z frontend: moved in_progress -> in_review
- 2026-11-03T00:32:23Z orchestrator: review dispatched: paralegal-reviewer

## Handoff
What changed: Step 3 charge card shows 'Date of service' = service_date.text verbatim; the record's own date reads 'statement dated X' in the card sub and source head when it is not the service day; confirm_note leads the card foot (attn, role=note, plain words via R.plain); done-list column is Date of service. step3.js/css only (review.js untouched); test_round2 assertion updated to the new text. · Verified: new tests/e2e/guided/test_t205.py (5) + guided suite + test_no_console_errors = 143 passed from git archive, E2E_REQUIRE_DB=1. · Left: nothing. · Surprised: the fixture set has no bill with a doubtful date, so the note test stubs service_date on the GET case response (backend's own sentences); also the card body scrolls, so a note placed there was clipped: moved to the foot. Others' staged deletions (test_round2/3.py, tests/unit/_githist.py) sit in the shared index, not mine. Commit 203ac6a.

84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
85-T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.
86-
87:## D-071 amendment — when the service date is not certain, print none and ask the human
88-T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.
89-
90-## D-072 — The prompt log is built and privacy-reviewed once, last
91-Every review round adds new transcripts (including the reviewer's own), so a per-round clean prompt log cannot stay clean (T-187 r4: the reviewer's own session carries private stems). Binding: (1) QA fixes the rule gaps now (bare work-email domain, hostname stems without suffix, job-folder names; a 'term' entry never overrides the outside-name switch; path tails redacted); (2) the final prompt log is rebuilt once, after the last agent has finished (inside T-188), then one independent privacy sweep runs on that build and on the snapshot, and its own transcript is excluded from the published set (listed in the README as the one omitted file); (3) every reviewer brief from now on says: report private values only as <redacted> with a count, never quote them, not even partially.
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:32:28.746Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t200-undated-charge-label.md"
}
````

### User / tool · 2026-11-03T00:32:28.753Z

**tool result**
````
1	---
2	name: t200-undated-charge-label
3	description: T-200 (bd72d5b) pass: counted undated lib11 ledger lines print "(statement dated June 15, 2026; service date not stated)"; D-071 binds that form; minors = notes silent, no count-walk eval
4	metadata:
5	  type: project
6	---
7	
8	T-200 review (reviews/T-200-paralegal.md, bd72d5b): pass, 2 minors + 1 nit. My T-181 r2 letter-date major is closed.
9	- D-071 (ORCHESTRATOR_DECISIONS.md:84) makes the T-200 wording binding for undated charges and moves dated charge lines (statement date vs service date: case_09, lib14, lib10) to another card. Grade that card on per-line service dates and period ranges.
10	- Open minors: the internal notes say nothing about counted charges that have no date of service (no "request dated itemized bill"). letter_check walks accept only, never D-064 count, so no eval produces the line.
11	- Mechanics: "demo mode" means a fixture backend; ZLAYT_MODE=local is still demo_mode true and gives /api/library. Reuse artifacts/review-evidence/T-200-paralegal/h.py + p01_lib11.py (port 7963, about 26 s end to end). The draft-then-cp flow with T-116-paralegal-r2-jsoncheck.py worked.
12	
13	**Why:** next round on the D-071 card, check the dated lines against the D-071 rules above.
14	**How to apply:** related [[t181-r2-patterns]], [[reviewer-run-pitfalls-pass4]].
15	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:32:29.216Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md"
}
````

### User / tool · 2026-11-03T00:32:29.223Z

**tool result**
````
1	---
2	name: reviewer-run-pitfalls-pass4
3	description: T-060/T-114 pass-4 run pitfalls: HEAD moves mid-review (pin by hash, run both if brief says HEAD and card names a commit); venv path relative from subdirs (exit 127); sed -i blocked again; Playwright selectors for case list, disclosure, confirm-date radios; reload restores the case
4	metadata:
5	  type: reference
6	---
7	
8	- HEAD moved during the review: 433ac1c became f7829c1 while I worked (other agents commit). Record the hash you archived with `git rev-parse --short HEAD` at the start AND `git archive <hash>`. When the brief says HEAD and the card names a commit (e293daa), run both and say which commit each finding applies to. Check `git diff --stat <card-commit> HEAD -- app/frontend` (empty = same UI).
9	- Server launch: `env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch db> PORT=<p> HOST=127.0.0.1 .venv/bin/python -I artifacts/review-evidence/<card>-paralegal-pass4-serve.py <archive_root>` (runpy, puts the archive root first on sys.path). Background launch: the launcher task exits 0 while the listener lives; get the listener PID with `lsof -iTCP:<p> -sTCP:LISTEN -nP`, kill by number, confirm curl = 000. Port 7860 is the live dev app; never touch it.
10	- `.venv/bin/python` is relative: from artifacts/review-evidence/<card>/ it exits 127. Run from repo root.
11	- `sed -i` is refused by board-guard again (pass 4). Use the Edit tool on scripts and memory; check `grep -c` after.
12	- Playwright selectors (e293daa/HEAD): case list buttons are `[data-testid=case-<token>]`; library entries `[data-testid=library-case_lib09_spanish_interpreter_espalda]` sit inside a collapsed disclosure: click `summary:has-text('synthetic library')` first. The lib09 names repeat ("Spanish-language records, back pain") and differ only by token: never pick by name. Date step: `button:has-text('1 date to confirm')`; radios via `get_by_label("March 5, 2026")`; confirm `get_by_role("button", name="Confirm date")`; there is NO `form[data-testid=confirm-date]` in this build. Gap notice `[data-testid=gap-change-note]`; dismiss it `[data-testid=btn-dismiss-gap-note]`. Dismissed entries group `[data-testid=dismissed-summary]`. Export `[data-testid=btn-export]`, letter `[data-testid=export-letter]` (a PRE, read innerText not value), copy `[data-testid=btn-copy-letter]`, download `[data-testid=btn-download-letter]`.
13	- Keyboard: `a` on a flag or amount acts on it; `d` on a flag dismisses without a reason prompt; `e` opens the textarea only when focus is on the row, and Ctrl+Enter saves.
14	- Reload restores the last case view (no paste page), so a probe that expects the paste box after reload will time out. Use the case list or continue on the restored case.
15	- Output discipline: write every probe's output with `> file` in the same call; console-only numbers do not count as evidence when the review quotes them.
16	- Review files are write-once: proofread every line reference with grep before the single Write (api.md:341 D-045b checked; the erratum route is the final reply).
17	
18	Why: all of these cost a probe rerun or an unfixable review line during the T-060/T-114 pass-4 run.
19	How to apply: start each Playwright run with `curl` on the port, confirm the archive hash, and keep one helper module per card. Related: [[reviewer-tooling-quirks]], [[reviewer-api-shape-gotchas]], [[t060-pass4-state-patterns]], [[t114-r3-gap-change-persistence]].
20	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:32:31.342Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD; git cat-file -t 203ac6a; D=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal; mkdir -p $D 2>&1; ls artifacts/review-evidence | grep -i -E \"T-200|T-202\" | head -20; ls artifacts/review-evidence/T-200-paralegal 2>/dev/null; git show --stat 203ac6a | head -20"
}
````

### User / tool · 2026-11-03T00:32:31.529Z

**tool result**
````
105d212
commit
T-200-paralegal
T-202-paralegal
T-202-paralegal-r2
T-202-staff
T-202-staff-r2
db
draft-T-200-paralegal.md
h.py
letter_check.out
lib-s2-00-e1.png
lib-s2-05-e2.png
lib-s2-08-e4.png
lib-s2-19-e9.png
lib-s3-00-a1.png
lib-s3-01-a2.png
lib-s3-02-a3.png
lib-s3-03-a4.png
lib-s3-04-a5.png
lib-s3-05-a6.png
lib-s3-06-a7.png
lib-s3-07-a8.png
lib-step2-done.png
lib-step3-done.png
lib-step3-revisit.png
lib-step4.png
lib11-letter-onscreen.txt
lib11-letter.txt
lib11-notes.txt
p01.out
p01_lib11.py
profile
pytest-t200.out
run.log
server.log
commit 203ac6a421e2aba911e8e91395d0b402e3ea0d08
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 18:31:44 2026 -0600

    feat(frontend): T-205 guided Step 3 shows the date of service the letter prints (service_date.text) and the confirm note when it is not certain
    
    The record's own date is named the statement date; the not-stated form and the note show in plain words. e2e: case_09, lib10, a counted no-date line, a stubbed doubtful date, phone.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/frontend/guided/step3.css   |   4 ++
 app/frontend/guided/step3.js    |  28 +++++---
 tests/e2e/guided/test_round2.py |   2 +-
 tests/e2e/guided/test_t205.py   | 149 ++++++++++++++++++++++++++++++++++++++++
 4 files changed, 174 insertions(+), 9 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:32:32.941Z

**tool call — Bash**
````
{
 "command": "git show 203ac6a -- app/frontend | head -150; cat artifacts/review-evidence/T-200-paralegal/h.py | head -80; sed -n 1,80p artifacts/review-evidence/T-200-paralegal/p01_lib11.py; ls artifacts/review-evidence/T-202-paralegal-r2 | head -30"
}
````

### User / tool · 2026-11-03T00:32:33.056Z

**tool result**
````
commit 203ac6a421e2aba911e8e91395d0b402e3ea0d08
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 18:31:44 2026 -0600

    feat(frontend): T-205 guided Step 3 shows the date of service the letter prints (service_date.text) and the confirm note when it is not certain
    
    The record's own date is named the statement date; the not-stated form and the note show in plain words. e2e: case_09, lib10, a counted no-date line, a stubbed doubtful date, phone.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/guided/step3.css b/app/frontend/guided/step3.css
index 8d418c7..3d082f6 100644
--- a/app/frontend/guided/step3.css
+++ b/app/frontend/guided/step3.css
@@ -13,3 +13,7 @@
   .panel .mini td:last-child { padding-top: 8px; }
   .panel .mini td:last-child .btn { width: 100%; }
 }
+
+/* T-205: the date of service the letter prints, and the plain note when it is not certain */
+.card-b .svc-date { overflow-wrap: anywhere; }
+.card-f .svc-note { display: block; overflow-wrap: anywhere; }
diff --git a/app/frontend/guided/step3.js b/app/frontend/guided/step3.js
index f1e74ea..fa0bf20 100644
--- a/app/frontend/guided/step3.js
+++ b/app/frontend/guided/step3.js
@@ -15,17 +15,28 @@
   const find = (c, id) => (c.amounts || []).find((a) => a.id === id) || null;
   const cents = (a) => (a.value_cents == null ? null : a.value_cents);
   const hasDollar = (t) => /\$\s*\d|\d\s*(?:USD|dollars)/i.test(t || "");
-  const recLabel = (r) => `Record ${r.seq} · ${r.source_label || "Record"} · ${r.date_iso ? R.longDate(r.date_iso) : r.date_raw || "no date"}`;
+  /* T-205 (D-071): a charge's date is the service date the letter prints (amounts[].service_date.text, byte for byte); the record's own date is called the statement date whenever it is not that day. Code only, no guessing. */
+  const sdOf = (a) => (a && a.kind === "charge" && a.service_date && typeof a.service_date === "object" ? a.service_date : null);
+  const stmtOnly = (sd) => !!sd && !!sd.statement_date_iso && !(sd.state === "stated" && sd.date_iso === sd.statement_date_iso && !sd.end_iso);      // a bill's date, not the day of the service
+  const recDate = (r, sd) => { const d = r.date_iso ? R.longDate(r.date_iso) : r.date_raw || ""; return d ? (stmtOnly(sd) ? "statement dated " + d : d) : "no date"; };
+  const recLabel = (r, sd) => `Record ${r.seq} · ${r.source_label || "Record"} · ${recDate(r, sd)}`;
   const figure = (a) => (cents(a) != null ? R.money(cents(a)) : a.text || "");
   const FLAG_BOX = { likely_duplicate: "I checked: this is a separate charge, not the same one counted twice.", likely_total: "I checked: this is a charge of its own, not a total of the others." };
   const flagBox = (f) => FLAG_BOX[f.flag] || `I checked: ${String(f.name || f.flag || "this is right").replace(/\.$/, "")}.`;
 
+  /* the date of service exactly as the letter prints it; the statement date, when different, is named as that */
+  const dateLine = (sd) => h("p", { class: "svc-date gap-top", "data-testid": "service-date", "data-state": sd.state },
+    h("span", { class: "label-cap" }, "Date of service"), " ", h("b", { "data-testid": "service-date-text" }, sd.text || ""),
+    sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · statement dated ${R.longDate(sd.statement_date_iso)}`) : null);
+  const confirmNote = (sd) => h("strong", { class: "svc-note", role: "note", "data-testid": "confirm-note" }, R.plain(sd.confirm_note));
+
   function present(S, item) {
     const kind = kindOf(item), recs = (item.record_ids || []).map((id) => S.record(id)).filter(Boolean), rec = recs[0];
+    const sd = sdOf(item);
     const marks = item.excerpt_start != null ? [[item.excerpt_start, item.excerpt_end]] : [];
-    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r) : null }));
-    const src = { head: many ? "Records " + recs.slice(0, -1).map((r) => r.seq).join(", ") + " and " + recs[recs.length - 1].seq : rec ? recLabel(rec) : "", nodes: srcNodes };
-    const sub = rec ? [rec.source_label, rec.date_iso ? R.longDate(rec.date_iso) : rec.date_raw].filter(Boolean).join(" · ") : "";
+    const many = recs.length > 1, srcNodes = () => recs.flatMap((r) => R.recBlock(r, { marks: marks.filter(([a]) => a >= r.char_start && a < r.char_end), head: many ? recLabel(r, sd) : null }));
+    const src = { head: many ? "Records " + recs.slice(0, -1).map((r) => r.seq).join(", ") + " and " + recs[recs.length - 1].seq : rec ? recLabel(rec, sd) : "", nodes: srcNodes };
+    const sub = rec ? [rec.source_label, rec.date_iso ? (stmtOnly(sd) ? "statement dated " + R.longDate(rec.date_iso) : R.longDate(rec.date_iso)) : rec.date_raw].filter(Boolean).join(" · ") : "";
     const disp = R.dispute(item) || (S.forceCompare.get(item.id) || null);
     const decided = item.review_status === "accepted" || item.review_status === "dismissed" || item.review_status === "edited";
     const flag = item.flag && item.confirm_required ? item.flag : null;
@@ -40,11 +51,11 @@
       if (disp) { cls = "attn"; if (flag) foot.push(h("hr", { class: "foot-rule" })); foot.push(...compareFoot()); }
       if (!flag && !disp) {
         if (decided) { cls = "ok"; foot.push(h("strong", {}, "Your answer: "), item.review_status === "dismissed" ? "not counted." : "counted in the bill total.", " You can change it."); }
-        else foot.push("If you count it, it's added to the bill total in the letter, with the highlighted words as its source.");
+        else if (!(sd && sd.confirm_note)) foot.push("If you count it, it's added to the bill total in the letter, with the highlighted words as its source.");
       }
       return { tag: { cls: "ok", text: "Charge" }, sub, src,
-        body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), h("p", { class: "explain muted gap-top" }, "Written in the record as ", h("b", {}, item.text || ""), "."), note],
-        foot: { cls, nodes: foot },
+        body: [h("p", { class: "money", "data-testid": "figure" }, figure(item)), sd ? dateLine(sd) : null, h("p", { class: "explain muted gap-top" }, "Written in the record as ", h("b", {}, item.text || ""), "."), note],
+        foot: sd && sd.confirm_note ? { cls: "attn", nodes: [confirmNote(sd), ...(foot.length ? [h("div", { class: "gap-top" }, ...foot)] : [])] } : { cls, nodes: foot },          // T-205: the date is not certain: the note leads the foot, in plain words, under the highlighted quote
         question: "Should this charge count toward the bill total?",
         yes: { label: "Yes, count it", disabled: () => (!!flag && !ticked("flag")) || (!!disp && !ticked("compare")),
           run: () => S.decide(item, "accept", { ...(flag ? { confirm: flag.confirm_with } : {}), ...(disp && ticked("compare") ? { compared: true } : {}) }) },
@@ -93,6 +104,7 @@
     const c = S.c, items = S.counted().map((q) => S.item(q.id)), recs = Object.fromEntries((c.records || []).map((r) => [r.id, r]));
     const left = items.filter(G.steps.undecided), changeHref = (a) => G.url.bills(S.token, a.id);
     const from = (a) => { const r = recs[(a.record_ids || [])[0]]; return r ? r.source_label || "" : ""; }, when = (a) => {
+      const sd = sdOf(a); if (sd && sd.text) return sd.text;          // the letter's own date text
       const r = recs[(a.record_ids || [])[0]], d = r && r.date_iso ? R.longDate(r.date_iso) : "", by = a.ladder && a.ladder.code_checks && a.ladder.code_checks.classified_by;
       return d && /^reviewer:counted/.test(by || "") ? `No date of service (statement dated ${d})` : d;          // a ledger line she counted states no date of service: the record's date is the statement's
     };
@@ -115,7 +127,7 @@
       ...overlaps.map((o) => h("div", { class: "note-box overlap", "data-testid": "overlap" }, h("div", { class: "nb-text" }, "Check these two amounts", h("span", {}, R.plain(o.message))),
         h("div", { class: "row-actions tight" }, [o.statement_amount_id, o.covered_amount_id].map((id, i) => h("a", { class: "btn", href: G.url.bills(S.token, id) }, `Change ${i ? o.covered_text : o.statement_text}`))))),
       h("div", { class: "panel", "data-testid": "list-counted" }, h("h2", {}, `Counted (${counted.length})`),
-        counted.length ? table(["Amount", "From", "Date"], counted.map((a) => row(a, [from(a), when(a)]))) : h("p", { class: "muted" }, "You didn't count any charge.")),
+        counted.length ? table(["Amount", "From", "Date of service"], counted.map((a) => row(a, [from(a), when(a)]))) : h("p", { class: "muted" }, "You didn't count any charge.")),
       h("div", { class: "panel", "data-testid": "list-not-counted" }, h("h2", {}, `Not counted by you (${notCounted.length})`),
         notCounted.length ? table(["Amount", "From", "Why"], notCounted.map((a) => row(a, [from(a), a.kind === "charge" ? "You chose not to count it." : R.plain(a.not_counted_reason || "")]))) : h("p", { class: "muted" }, "You didn't leave out any charge.")),
       h("div", { class: "panel", "data-testid": "list-never" }, h("h2", {}, `Never counted (${never.length})`), h("p", { class: "muted" }, "These are never added to the total. The ones you listed go in the notes for the attorney."),
"""T-200 paralegal review helper (copied from T-181 r2): persistent Chromium profile on the archive app (bd72d5b, demo/fixture, local mode, port 7963).

Usage: .venv/bin/python -I artifacts/review-evidence/T-200-paralegal/h.py <step-script.py>
The step script gets `pg` (page), `shot(name)`, `dump(label)`, `log(...)`, `BASE`, `OUT` in its globals.
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7963")
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
PROFILE = os.path.join(OUT, os.environ.get("T181_PROFILE", "profile"))
LOG = os.path.join(OUT, "run.log")


def main(script):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE, headless=True, viewport={"width": 1440, "height": 900})
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        errors = []
        pg.on("console", lambda m: errors.append(f"console.{m.type}: {m.text}") if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))
        pg.on("response", lambda r: errors.append(f"http {r.status} {r.request.method} {r.url}") if r.status >= 400 else None)
        logf = open(LOG, "a")

        def log(*a):
            s = " ".join(str(x) for x in a)
            print(s)
            logf.write(s + "\n")
            logf.flush()

        def shot(name, full=False):
            path = os.path.join(OUT, name + ".png")
            pg.screenshot(path=path, full_page=full)
            log("[shot]", path)

        def dump(label=""):
            pg.wait_for_timeout(250)
            t = pg.evaluate("() => document.body.innerText")
            log(f"===== {label} url={pg.url}")
            log(t)
            log("=====")
            return t

        g = {"pg": pg, "shot": shot, "dump": dump, "log": log, "BASE": BASE, "OUT": OUT, "time": time, "ctx": ctx}
        log(f"### run {os.path.basename(script)} at {time.strftime('%H:%M:%S')}")
        try:
            exec(compile(open(script).read(), script, "exec"), g)
        finally:
            if errors:
                log("ERRORS:\n  " + "\n  ".join(errors))
            ctx.close()
            logf.close()


if __name__ == "__main__":
    main(sys.argv[1])
"""T-200 (copied from T-181 r2 r03_lib11.py): lib11 (priors and ledger) on the bd72d5b archive, demo/fixture backend, local mode, port 7963.
Accept Step 2; in Step 3 count the three undated ledger lines (tick 'separate charge' + compare); Step 4 letter and notes.
Run: .venv/bin/python -I artifacts/review-evidence/T-200-paralegal/h.py artifacts/review-evidence/T-200-paralegal/p01_lib11.py
"""
import re
T0 = time.time()
pg.goto(BASE + "/new")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.click("[data-testid=tile-library]")
pg.wait_for_timeout(300)
pg.check("[data-testid=library-case_lib11_priors_and_ledger]")
pg.click("[data-testid=btn-read]")
pg.wait_for_selector("[data-testid=btn-draft]", timeout=20000)
pg.wait_for_timeout(300)
dump("lib11 records")
pg.click("[data-testid=btn-draft]")
for i in range(80):
    pg.wait_for_timeout(250)
    if pg.query_selector("text=Go to step 2") or "/timeline" in pg.url:
        break
log("draft took", round(time.time() - T0, 1), "s")
if "/timeline" not in pg.url:
    pg.get_by_text("Go to step 2").first.click()
    pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(500)

def iid():
    m = re.search(r"item=([^&]+)", pg.url)
    return m.group(1) if m else None

n = 0
for step in range(40):
    i = iid()
    if not i or "/timeline" not in pg.url:
        break
    right = pg.evaluate("() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }")
    marks = pg.evaluate("() => Array.from(document.querySelectorAll('mark')).map(m => m.innerText)")
    outs = pg.evaluate("() => Array.from(document.querySelectorAll('[data-testid=outside-word]')).map(m => m.innerText)")
    note = pg.evaluate("() => { const u = document.querySelector('[data-testid=outside-note]'); return u ? u.innerText : null }")
    unc = pg.evaluate("() => { const u = document.querySelector('[data-testid=uncovered]'); return u ? u.innerText.replace(/\\n/g, ' / ') : null }")
    yes = pg.query_selector("[data-testid=answer-yes]")
    yd = yes.is_disabled() if yes else None
    cmp_box = pg.query_selector("[data-testid=check-compare]")
    log(f"######## {n} item={i} yes_disabled={yd} compare_box={bool(cmp_box)}")
    log("CARD:", right.replace("\n", " / "))
    log("MARKS:", marks)
    log("OUTSIDE-WORDS:", outs, "| NOTE:", note)
    log("UNCOVERED:", unc)
    if cmp_box or yd:
        shot(f"lib-s2-{n:02d}-{i}")
    n += 1
    if cmp_box:
        pg.keyboard.press("a"); pg.wait_for_timeout(200)
        pg.keyboard.press("Space"); pg.wait_for_timeout(200)
        pg.keyboard.press("a")
    elif yd:
        pg.keyboard.press("a"); pg.wait_for_timeout(250)
        log("  after A on refused: focus", pg.evaluate("() => document.activeElement.getAttribute('data-testid') || document.activeElement.tagName"),
            "| msg:", pg.evaluate("() => (document.querySelector('.actions') || {innerText:''}).innerText").replace("\n", " | ")[-200:])
        pg.keyboard.press("d")
    else:
        pg.keyboard.press("a")
    pg.wait_for_timeout(450)
dump("lib11 step 2 done")
shot("lib-step2-done", full=True)

pg.click("[data-testid=btn-next-step]")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(500)
n = 0
for step in range(15):
    i = iid()
    if not i or "/bills" not in pg.url:
        break
    right = pg.evaluate("() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }")
    boxes = [b.get_attribute("data-testid") for b in pg.query_selector_all("input[type=checkbox]") if b.is_visible()]
    log(f"######## bills {n} item={i} boxes={boxes}")
    log("CARD:", right.replace("\n", " / "))
    shot(f"lib-s3-{n:02d}-{i}")
    n += 1
api_service_date.out
api_service_date.py
case_09-s3-00-a1.png
case_09-step2-done.png
case_09-step3-done.png
case_09-step4.png
db
draft-T-202-paralegal-r2.md
h.py
letter_check.out
letters
letters_dump_r2.out
letters_dump_r2.py
lib10-s3-00-a2.png
lib10-s3-01-a3.png
lib10-s3-02-a4.png
lib10-s3-03-a5.png
lib10-s3-04-a1.png
lib10-s3-05-a6.png
lib10-s3-06-a7.png
lib10-s3-07-a8.png
lib10-s3-08-a9.png
lib10-s3-09-a10.png
lib10-s3-10-a11.png
lib10-step2-done.png
lib10-step3-done.png
lib10-step4.png
lib14-s3-00-a1.png
lib14-s3-01-a2.png
lib14-s3-02-a4.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:32:35.288Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && ls T-202-paralegal-r2 | sed -n 30,80p; ls T-202-paralegal-r2/*.py; head -30 T-200-paralegal/server.log; ls | grep -i serve; grep -rn \"serve\" T-200-paralegal/*.py | head; ls T-202-paralegal"
}
````

### User / tool · 2026-11-03T00:32:35.417Z

**tool result**
````
lib14-s3-02-a4.png
lib14-s3-03-a3.png
lib14-s3-04-a5.png
lib14-step2-done.png
lib14-step3-done.png
lib14-step4.png
p01.out
p01_cases.py
probe_eval_teeth_r2.out
probe_eval_teeth_r2.py
probe_r2.out
probe_r2.py
probe_r2b.out
probe_r2b.py
probe_r2b_on_f0921e4.out
probe_r2b_prev.py
profile
pytest-t202.out
run.log
sample-s3-00-a1.png
sample-s3-01-a4.png
sample-s3-02-a2.png
sample-s3-03-a3.png
sample-step2-done.png
sample-step3-done.png
sample-step4.png
server.log
ui-case_09-letter-onscreen.txt
ui-case_09-letter.txt
ui-case_09-notes.txt
ui-lib10-letter-onscreen.txt
ui-lib10-letter.txt
ui-lib10-notes.txt
ui-lib14-letter-onscreen.txt
ui-lib14-letter.txt
ui-lib14-notes.txt
ui-sample-letter-onscreen.txt
ui-sample-letter.txt
ui-sample-notes.txt
T-202-paralegal-r2/api_service_date.py
T-202-paralegal-r2/h.py
T-202-paralegal-r2/letters_dump_r2.py
T-202-paralegal-r2/p01_cases.py
T-202-paralegal-r2/probe_eval_teeth_r2.py
T-202-paralegal-r2/probe_r2.py
T-202-paralegal-r2/probe_r2b.py
T-202-paralegal-r2/probe_r2b_prev.py
Serving on http://127.0.0.1:7963  (Ctrl-C to stop)
T-049-served-index.html
T-060-paralegal-pass4-serve.py
T-120-r2-paralegal-server.log
all_charge_lines.out
all_charge_lines.py
api-amount-fields.out
case09-paste-probe.out
case_09-all_accepted-letter.txt
case_09-all_accepted-notes.txt
case_09-counted-letter.txt
case_09-counted-notes.txt
case_09-s3-00-a1.png
case_09-step2-done.png
case_09-step3-done.png
case_09-step4.png
db
draft-T-202-paralegal.md
h.py
letter_check.out
letters_dump.out
letters_dump.py
letters_dump_parent.py
lib10-all_accepted-letter.txt
lib10-all_accepted-notes.txt
lib10-counted-letter.txt
lib10-counted-notes.txt
lib10-s3-00-a2.png
lib10-s3-01-a3.png
lib10-s3-02-a4.png
lib10-s3-03-a5.png
lib10-s3-04-a1.png
lib10-s3-05-a6.png
lib10-s3-06-a7.png
lib10-s3-07-a8.png
lib10-s3-08-a9.png
lib10-s3-09-a10.png
lib10-s3-10-a11.png
lib10-step2-done.png
lib10-step3-done.png
lib10-step4.png
lib14-all_accepted-letter.txt
lib14-all_accepted-notes.txt
lib14-counted-letter.txt
lib14-counted-notes.txt
lib14-s3-00-a1.png
lib14-s3-01-a2.png
lib14-s3-02-a4.png
lib14-s3-03-a3.png
lib14-s3-04-a5.png
lib14-step2-done.png
lib14-step3-done.png
lib14-step4.png
p01.out
p01_cases.py
p02.out
parent-a44cfa7
parent-vs-f0921e4.diff
probe_dates.out
probe_dates.py
probe_dates2.out
probe_dates2.py
probe_eval_teeth.out
probe_eval_teeth.py
profile
pytest-t202.out
run.log
sample-all_accepted-letter.txt
sample-all_accepted-notes.txt
sample-counted-letter.txt
sample-counted-notes.txt
sample-s3-00-a1.png
sample-s3-01-a4.png
sample-s3-02-a2.png
sample-s3-03-a3.png
sample-step2-done.png
sample-step3-done.png
sample-step4.png
server.log
ui-case_09-letter-onscreen.txt
ui-case_09-letter.txt
ui-case_09-notes.txt
ui-lib10-letter-onscreen.txt
ui-lib10-letter.txt
ui-lib10-notes.txt
ui-lib14-letter-onscreen.txt
ui-lib14-letter.txt
ui-lib14-notes.txt
ui-sample-letter-onscreen.txt
ui-sample-letter.txt
ui-sample-notes.txt
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:32:37.313Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && cat T-202-paralegal-r2/p01_cases.py; cat T-202-paralegal-r2/h.py | head -20; head -5 T-202-paralegal-r2/server.log; cat T-060-paralegal-pass4-serve.py; grep -rn \"ZLAYT_MODE\\|FIXTURE_SET\\|T202.*serv\" T-202-paralegal-r2/*.py T-202-paralegal-r2/draft* | head"
}
````

### User / tool · 2026-11-03T00:32:37.411Z

**tool result**
````
"""T-202 r2 paralegal (copied from r1): 986fc55 archive, demo/fixture backend, local mode, port 7976.
For each case (env CASES, default sample,case_09,lib14,lib10): open it as a user (sample tile / paste / library), draft, Step 2 accept with the
keyboard (compare box ticked where asked), Step 3 accept every bill item and tick 'count' boxes where offered, Step 4 download letter + notes.
Run: .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/h.py artifacts/review-evidence/T-202-paralegal/p01_cases.py
"""
import os
import re

CASES = os.environ.get("CASES", "sample,case_09,lib14,lib10").split(",")
PASTE = {"case_09": "/Users/arsis/zlayt-pm-project/evals/golden/case_09_nonvisit_hides_gap.txt"}
LIB = {"lib14": "case_lib14_handwritten_chiro_scans", "lib10": "case_lib10_eob_ub04_cms1500"}


def iid():
    m = re.search(r"item=([^&]+)", pg.url)
    return m.group(1) if m else None


def card():
    return pg.evaluate("() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }")


for name in CASES:
    T0 = time.time()
    pg.goto(BASE + "/new")
    pg.wait_for_selector("[data-testid=view][data-ready]")
    if name == "sample":
        pg.click("[data-testid=tile-sample]")
    elif name in PASTE:
        # demo UI turns the paste tile off (step1.js:40 off: demo); the API accepts the golden text (201), so create it there and open it in the UI
        import json, urllib.request
        req = urllib.request.Request(BASE + "/api/cases", data=json.dumps({"text": open(PASTE[name]).read()}).encode(),
                                     headers={"Content-Type": "application/json"}, method="POST")
        tok = json.loads(urllib.request.urlopen(req, timeout=20).read())["token"]
        log(f"[{name}] created via POST /api/cases token={tok}")
        pg.goto(f"{BASE}/case/{tok}/records")
        pg.wait_for_selector("[data-testid=view][data-ready]")
        pg.wait_for_timeout(500)
    else:
        pg.click("[data-testid=tile-library]")
        pg.wait_for_timeout(300)
        pg.check(f"[data-testid=library-{LIB[name]}]")
    pg.wait_for_timeout(300)
    if name not in PASTE:
        pg.click("[data-testid=btn-read]")
    pg.wait_for_selector("[data-testid=btn-draft]", timeout=20000)
    pg.wait_for_timeout(300)
    pg.click("[data-testid=btn-draft]")
    for i in range(120):
        pg.wait_for_timeout(250)
        if pg.query_selector("text=Go to step 2") or "/timeline" in pg.url:
            break
    log(f"[{name}] draft took", round(time.time() - T0, 1), "s")
    if "/timeline" not in pg.url:
        pg.get_by_text("Go to step 2").first.click()
        pg.wait_for_selector("[data-testid=view][data-ready]")
    pg.wait_for_timeout(500)
    # Step 2
    for step in range(60):
        i = iid()
        if not i or "/timeline" not in pg.url:
            break
        yes = pg.query_selector("[data-testid=answer-yes]")
        yd = yes.is_disabled() if yes else None
        cmp_box = pg.query_selector("[data-testid=check-compare]")
        radios = pg.query_selector_all("input[type=radio]")
        log(f"[{name}] s2 item={i} yes_disabled={yd} compare={bool(cmp_box)} radios={len(radios)} :: {card().replace(chr(10), ' / ')[:300]}")
        if radios and pg.query_selector("button:has-text('Confirm date')"):
            radios[0].check(); pg.wait_for_timeout(200)
            pg.get_by_role("button", name="Confirm date").click(); pg.wait_for_timeout(600)
            log(f"[{name}]   confirmed first date reading")
            continue
        if cmp_box:
            pg.keyboard.press("a"); pg.wait_for_timeout(200)
            pg.keyboard.press("Space"); pg.wait_for_timeout(200)
            pg.keyboard.press("a")
        elif yd:
            pg.keyboard.press("d")
        else:
            pg.keyboard.press("a")
        pg.wait_for_timeout(450)
        if iid() == i:
            pg.keyboard.press("j"); pg.wait_for_timeout(300)
            if iid() == i:
                break
    shot(f"{name}-step2-done", full=True)
    if "/timeline" in pg.url:
        pg.click("[data-testid=btn-next-step]")
        pg.wait_for_selector("[data-testid=view][data-ready]")
        pg.wait_for_timeout(500)
    # Step 3
    seen = {}
    for step in range(40):
        i = iid()
        if not i or "/bills" not in pg.url:
            break
        seen[i] = seen.get(i, 0) + 1
        if seen[i] > 3:
            break
        boxes = [b.get_attribute("data-testid") for b in pg.query_selector_all("input[type=checkbox]") if b.is_visible()]
        log(f"[{name}] s3 item={i} boxes={boxes} :: {card().replace(chr(10), ' / ')}")
        shot(f"{name}-s3-{step:02d}-{i}")
        if boxes:
            pg.keyboard.press("a"); pg.wait_for_timeout(200)
            for _ in boxes:
                pg.keyboard.press("Space"); pg.wait_for_timeout(200)
                pg.keyboard.press("a"); pg.wait_for_timeout(300)
                if iid() != i:
                    break
        else:
            pg.keyboard.press("a")
        pg.wait_for_timeout(450)
    dump(f"[{name}] step 3 done")
    shot(f"{name}-step3-done", full=True)
    pg.get_by_text("Go to step 4").first.click()
    pg.wait_for_selector("[data-testid=letter-text]", timeout=15000)
    pg.wait_for_timeout(600)
    with pg.expect_download() as d:
        pg.click("[data-testid=btn-download-letter]")
    d.value.save_as(f"{OUT}/ui-{name}-letter.txt")
    with pg.expect_download() as d2:
        pg.click("[data-testid=btn-download-notes]")
    d2.value.save_as(f"{OUT}/ui-{name}-notes.txt")
    open(f"{OUT}/ui-{name}-letter-onscreen.txt", "w").write(pg.inner_text("[data-testid=letter-text]"))
    shot(f"{name}-step4", full=True)
    log(f"[{name}] done in", round(time.time() - T0, 1), "s")
"""T-200 paralegal review helper (copied from T-181 r2): persistent Chromium profile on the archive app (bd72d5b, demo/fixture, local mode, port 7963).

Usage: .venv/bin/python -I artifacts/review-evidence/T-200-paralegal/h.py <step-script.py>
The step script gets `pg` (page), `shot(name)`, `dump(label)`, `log(...)`, `BASE`, `OUT` in its globals.
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7976")  # T-202 r2: 986fc55 archive, port 7976
OUT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
PROFILE = os.path.join(OUT, os.environ.get("T181_PROFILE", "profile"))
LOG = os.path.join(OUT, "run.log")


def main(script):
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(PROFILE, headless=True, viewport={"width": 1440, "height": 900})
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
Serving on http://127.0.0.1:7976  (Ctrl-C to stop)
"""Start the app from a git-archive copy (commit e293daa) for the paralegal pass-4 / T-114 r3 review.

Usage (env vars set by the caller: LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch db> PORT=7897 HOST=127.0.0.1):
    .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py <archive_root>
Runs under -I (isolated), so the archive root is put first on sys.path explicitly.
"""
import os
import runpy
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
runpy.run_module("app.main", run_name="__main__")
T-202-paralegal-r2/letters_dump_r2.py:15:os.environ.setdefault("FIXTURE_SET", "curated")
T-202-paralegal-r2/draft-T-202-paralegal-r2.md:23:- **Server:** fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local (health: demo_mode true), http://127.0.0.1:7976.
T-202-paralegal-r2/draft-T-202-paralegal-r2.md:46: "scope": "commit 986fc55 (git archive, commit id 986fc551078a6ed6274cc9dd7a6a9efd0af357e3, extracted to session scratchpad pr2_986fc55/); f0921e4 archive (round 1) for the before/after on the new probes. Demo mode: fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, http://127.0.0.1:7976 (health demo_mode true); listener PID 49534 stopped (lsof exit 1, curl 000). Cases: sample (load-sample tile), case_09 (POST /api/cases with the golden text, then opened in the UI), lib14 and lib10 (library tile); lib11 and two SYNTHETIC case_09 variants in-process. Evidence: artifacts/review-evidence/T-202-paralegal-r2/. Private values seen: 0.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:32:40.768Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"demo\" docs/RUNBOOK.md | head -20; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/a203; git archive 203ac6a | tar -x -C $S/a203; ls $S/a203 | head -30; lsof -iTCP:7981 -sTCP:LISTEN -nP | head -2"
}
````

### User / tool · 2026-11-03T00:32:42.044Z

**tool result**
````
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:32:45.296Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; \nenv LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$S/t205.db PORT=7981 HOST=127.0.0.1 nohup .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py $S/a203 > artifacts/review-evidence/T-205-paralegal/server.log 2>&1 &\nsleep 6; curl -s http://127.0.0.1:7981/api/health; echo; lsof -iTCP:7981 -sTCP:LISTEN -nP | tail -1"
}
````

### User / tool · 2026-11-03T00:32:51.500Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
Python  63090 arsis    9u  IPv4 0xbb5974a2a985937c      0t0  TCP 127.0.0.1:7981 (LISTEN)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:33:00.617Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && D=T-205-paralegal && sed 's#7976#7981#; s#T-202 r2: 986fc55 archive, port 7981#T-205: 203ac6a archive, port 7981#' T-202-paralegal-r2/h.py > $D/h.py && grep -n \"7981\\|jsondump\" $D/h.py | head; python3 - <<'EOF'\nsrc = open(\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/p01_cases.py\").read()\nsrc = src.replace('CASES = os.environ.get(\"CASES\", \"sample,case_09,lib14,lib10\")', 'CASES = os.environ.get(\"CASES\", \"case_09,lib10,lib11\")')\nsrc = src.replace('LIB = {\"lib14\": \"case_lib14_handwritten_chiro_scans\", \"lib10\": \"case_lib10_eob_ub04_cms1500\"}', 'LIB = {\"lib14\": \"case_lib14_handwritten_chiro_scans\", \"lib10\": \"case_lib10_eob_ub04_cms1500\", \"lib11\": \"case_lib11_priors_and_ledger\"}')\nold = '''        log(f\"[{name}] s3 item={i} boxes={boxes} :: {card().replace(chr(10), ' / ')}\")'''\nnew = '''        log(f\"[{name}] s3 item={i} boxes={boxes} :: {card().replace(chr(10), ' / ')}\")\n        probe = pg.evaluate(\"\"\"() => { const q = (s) => { const e = document.querySelector(s); return e ? e.innerText : null; };\n          const sub = document.querySelector('.work .card .card-h, .work .card .sub');\n          return {svc: q('[data-testid=service-date-text]'), svcState: (document.querySelector('[data-testid=service-date]')||{getAttribute:()=>null}).getAttribute('data-state'), stmt: q('[data-testid=statement-date]'), note: q('[data-testid=confirm-note]'), figure: q('[data-testid=figure]'), noteRole: (document.querySelector('[data-testid=confirm-note]')||{getAttribute:()=>null}).getAttribute('role'), yesLabel: q('[data-testid=answer-yes]'), card: (document.querySelectorAll('.work .card')[document.querySelectorAll('.work .card').length-1]||{innerText:''}).innerText}; }\"\"\")\n        log(f\"[{name}] PROBE item={i} \" + json.dumps(probe))\n        pg.evaluate(\"() => { const c = document.querySelector('[data-testid=confirm-note]'); if (c) c.scrollIntoView(); }\")'''\nassert old in src\nsrc = src.replace(old, new)\nsrc = src.replace(\"import os\\nimport re\\n\", \"import os\\nimport re\\nimport json\\n\", 1)\nopen(\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/p01.py\", \"w\").write(src)\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-205-paralegal/h.py artifacts/review-evidence/T-205-paralegal/p01.py > artifacts/review-evidence/T-205-paralegal/p01.out 2>&1; tail -5 artifacts/review-evidence/T-205-paralegal/p01.out; grep -c PROBE artifacts/review-evidence/T-205-paralegal/p01.out"
}
````

### User / tool · 2026-11-03T00:33:51.920Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:33:53.277Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal && grep -n \"PROBE\\|ERRORS\\|\\] done in\\|http 4\\|http 5\" p01.out | cut -c1-900"
}
````

### User / tool · 2026-11-03T00:33:53.365Z

**tool result**
````
12:[case_09] PROBE item=a1 {"svc": "February 2, 2026", "svcState": "stated", "stmt": " \u00b7 statement dated March 1, 2026", "note": null, "figure": "$275.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nHobbleton Family Clinic, billing statement \u00b7 statement dated March 1, 2026\n\n$275.00\n\nDate of service February 2, 2026 \u00b7 statement dated March 1, 2026\n\nWritten in the record as $275.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
64:[case_09] done in 7.4 s
79:[lib10] PROBE item=a2 {"svc": "June 9\u201312, 2026", "svcState": "stated", "stmt": " \u00b7 statement dated June 19, 2026", "note": null, "figure": "$4,920.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026\n\n$4,920.00\n\nDate of service June 9\u201312, 2026 \u00b7 statement dated June 19, 2026\n\nWritten in the record as $4,920.00.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
82:[lib10] PROBE item=a3 {"svc": "June 9\u201312, 2026", "svcState": "stated", "stmt": " \u00b7 statement dated June 19, 2026", "note": null, "figure": "$2,105.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026\n\n$2,105.00\n\nDate of service June 9\u201312, 2026 \u00b7 statement dated June 19, 2026\n\nWritten in the record as $2,105.00.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
85:[lib10] PROBE item=a4 {"svc": "June 9\u201312, 2026", "svcState": "stated", "stmt": " \u00b7 statement dated June 19, 2026", "note": null, "figure": "$386.50", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026\n\n$386.50\n\nDate of service June 9\u201312, 2026 \u00b7 statement dated June 19, 2026\n\nWritten in the record as $386.50.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
88:[lib10] PROBE item=a5 {"svc": "June 9\u201312, 2026", "svcState": "stated", "stmt": " \u00b7 statement dated June 19, 2026", "note": null, "figure": "$712.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026\n\n$712.00\n\nDate of service June 9\u201312, 2026 \u00b7 statement dated June 19, 2026\n\nWritten in the record as $712.00.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
91:[lib10] PROBE item=a1 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$1,640.00", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 June 19, 2026\n\n$1,640.00\n\nThis figure is a rate, not a charge, so it is not added to the total.\n\nEither way, it is never added to the bill total."}
94:[lib10] PROBE item=a6 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$8,123.50", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 June 19, 2026\n\n$8,123.50\n\nTotal or subtotal line: it repeats the charges listed with it, so it is not totaled.\n\nA second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide.\nI read this amount against the highlighted words myself."}
97:[lib10] PROBE item=a7 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$8,023.50", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nQuoinmere Mutual Health Plan, EOB \u00b7 July 3, 2026\n\n$8,023.50\n\nInsurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.\n\nA second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide.\nI read this amount against the highlighted words myself."}
100:[lib10] PROBE item=a8 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$3,610.00", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nQuoinmere Mutual Health Plan, EOB \u00b7 July 3, 2026\n\n$3,610.00\n\nAdjustment, write-off or credit: not a charge, and never subtracted from the billed charges.\n\nEither way, it is never added to the bill total."}
103:[lib10] PROBE item=a9 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$4,413.50", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nQuoinmere Mutual Health Plan, EOB \u00b7 July 3, 2026\n\n$4,413.50\n\nInsurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.\n\nA second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide.\nI read this amount against the highlighted words myself."}
106:[lib10] PROBE item=a10 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$3,530.80", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nQuoinmere Mutual Health Plan, EOB \u00b7 July 3, 2026\n\n$3,530.80\n\nPayment: money received, not a charge.\n\nEither way, it is never added to the bill total."}
109:[lib10] PROBE item=a11 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$882.70", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nQuoinmere Mutual Health Plan, EOB \u00b7 July 3, 2026\n\n$882.70\n\nInsurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.\n\nA second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide.\nI read this amount against the highlighted words myself."}
172:[lib10] done in 19.2 s
197:[lib11] PROBE item=a1 {"svc": "March 18, 2026", "svcState": "stated", "stmt": null, "note": null, "figure": "$3,260.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nWexcombe Memorial ED \u00b7 March 18, 2026\n\n$3,260.00\n\nDate of service March 18, 2026\n\nWritten in the record as $3,260.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
200:[lib11] PROBE item=a2 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$250.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Not counted yet\nFennimoor Spine Clinic, itemized ledger \u00b7 June 15, 2026\n\n$250.00\n\nThe line states no date of service, so it is not a single dated bill line and is not totaled.\n\nYou can still count it if you checked the ledger yourself.\nI checked this is a separate charge for a service.\nA second AI check thought this may be a billed charge, not what it was first sorted as.\nI read this amount against the highlighted words myself."}
203:[lib11] PROBE item=a3 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$180.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Not counted yet\nFennimoor Spine Clinic, itemized ledger \u00b7 June 15, 2026\n\n$180.00\n\nThe line states no date of service, so it is not a single dated bill line and is not totaled.\n\nYou can still count it if you checked the ledger yourself.\nI checked this is a separate charge for a service.\nA second AI check thought this may be a billed charge, not what it was first sorted as.\nI read this amount against the highlighted words myself."}
206:[lib11] PROBE item=a4 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$2,310.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Not counted yet\nFennimoor Spine Clinic, itemized ledger \u00b7 June 15, 2026\n\n$2,310.00\n\nThe line states no date of service, so it is not a single dated bill line and is not totaled.\n\nYou can still count it if you checked the ledger yourself.\nI checked this is a separate charge for a service.\nA second AI check thought this may be a billed charge, not what it was first sorted as.\nI read this amount against the highlighted words myself."}
209:[lib11] PROBE item=a5 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$2,740.00", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 June 15, 2026\n\n$2,740.00\n\nTotal or subtotal line: it repeats the charges listed with it, so it is not totaled.\n\nA second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide.\nI read this amount against the highlighted words myself."}
212:[lib11] PROBE item=a6 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$300.00", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 June 15, 2026\n\n$300.00\n\nPayment: money received, not a charge.\n\nA second AI check thought this may be a damages figure (for example lost wages), not what it was first sorted as. Read it against the highlighted words before you decide.\nI read this amount against the highlighted words myself."}
215:[lib11] PROBE item=a7 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$274.00", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 June 15, 2026\n\n$274.00\n\nAdjustment, write-off or credit: not a charge, and never subtracted from the billed charges.\n\nEither way, it is never added to the bill total."}
218:[lib11] PROBE item=a8 {"svc": null, "svcState": null, "stmt": null, "note": null, "figure": "$2,166.00", "noteRole": null, "yesLabel": "Yes, list it", "card": "Never counted\nFennimoor Spine Clinic, itemized ledger \u00b7 June 15, 2026\n\n$2,166.00\n\nBalance or amount due: worked out from charges, payments and adjustments, not a charge.\n\nA second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide.\nI read this amount against the highlighted words myself."}
278:[lib11] done in 24.2 s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:33:59.783Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && cat T-202-paralegal-r2/api_service_date.py | head -40; grep -n \"token=\\|created via\" T-205-paralegal/p01.out | head"
}
````

### User / tool · 2026-11-03T00:33:59.875Z

**tool result**
````
"""T-202 r2: GET /api/cases/{token} on the running 986fc55 app (port 7976) and print amounts[].service_date per charge next to the record's date
the Step 3 card shows. Tokens from p01.out.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/api_service_date.py
"""
import json
import urllib.request

BASE = "http://127.0.0.1:7976"
TOKENS = {"sample": "SfT5YaCLeW3v9bKQxQEmIQ", "case_09": "sGgv7E88x0beSaB09PVPEg", "lib14": "ewizSiIR767-uxwAss5e3A", "lib10": "OySGH-nh4pkbSNh6FIhvUg"}
for name, tok in TOKENS.items():
    c = json.loads(urllib.request.urlopen(f"{BASE}/api/cases/{tok}", timeout=20).read())
    print(f"== {name}")
    for a in c.get("amounts", []):
        sd = a.get("service_date")
        print(f"   {a.get('id'):>4} kind={a.get('kind'):<8} {str(a.get('display') or a.get('value') or a.get('raw') or ''):<12} service_date={json.dumps(sd, ensure_ascii=False)}")
2:[case_09] created via POST /api/cases token=Rb_-aRcu7JXIMZ90rAiyHA
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:34:01.227Z

**tool call — Bash**
````
{
 "command": "curl -s http://127.0.0.1:7981/api/cases | head -c 1500; echo; ls ~/ >/dev/null; grep -n \"url=\" artifacts/review-evidence/T-205-paralegal/p01.out | head -3"
}
````

### User / tool · 2026-11-03T00:34:01.385Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:34:05.676Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal && cat > api.py <<'EOF'\n\"\"\"T-205: GET /api/cases/{token} on the 203ac6a app (port 7981); print amounts[].service_date per amount next to the record date.\"\"\"\nimport json, urllib.request\nBASE = \"http://127.0.0.1:7981\"\nTOKENS = {\"case_09\": \"Rb_-aRcu7JXIMZ90rAiyHA\", \"lib10\": \"_HdnjAt2eCEWDdnvroHTEw\", \"lib11\": \"WMUiPxizxiRAqdrprp3a9Q\"}\nfor name, tok in TOKENS.items():\n    c = json.loads(urllib.request.urlopen(f\"{BASE}/api/cases/{tok}\", timeout=20).read())\n    recs = {r[\"id\"]: r for r in c.get(\"records\", [])}\n    print(f\"== {name}\")\n    for a in c.get(\"amounts\", []):\n        r = recs.get((a.get(\"record_ids\") or [None])[0]) or {}\n        print(f\"  {a['id']:>4} kind={a['kind']:<8} text={a.get('text')!r:<14} rec#{r.get('seq')} {r.get('source_label')!r} rec_date={r.get('date_iso')} status={a.get('review_status')}\")\n        print(f\"       service_date={json.dumps(a.get('service_date'), ensure_ascii=False)}\")\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-205-paralegal/api.py > artifacts/review-evidence/T-205-paralegal/api.out 2>&1; cut -c1-600 artifacts/review-evidence/T-205-paralegal/api.out"
}
````

### User / tool · 2026-11-03T00:34:05.935Z

**tool result**
````
== case_09
    a1 kind=charge   text='$275'         rec#2 'Hobbleton Family Clinic, billing statement' rec_date=2026-03-01 status=accepted
       service_date={"state": "stated", "date_iso": "2026-02-02", "end_iso": null, "text": "February 2, 2026", "statement_date_iso": "2026-03-01", "reason": null, "confirm_note": null}
== lib10
    a1 kind=rate     text='$1,640.00'    rec#4 'Saltmarrow General Hospital, UB-04 itemized bill' rec_date=2026-06-19 status=accepted
       service_date=null
    a2 kind=charge   text='$4,920.00'    rec#4 'Saltmarrow General Hospital, UB-04 itemized bill' rec_date=2026-06-19 status=accepted
       service_date={"state": "stated", "date_iso": "2026-06-09", "end_iso": "2026-06-12", "text": "June 9–12, 2026", "statement_date_iso": "2026-06-19", "reason": null, "confirm_note": null}
    a3 kind=charge   text='$2,105.00'    rec#4 'Saltmarrow General Hospital, UB-04 itemized bill' rec_date=2026-06-19 status=accepted
       service_date={"state": "stated", "date_iso": "2026-06-09", "end_iso": "2026-06-12", "text": "June 9–12, 2026", "statement_date_iso": "2026-06-19", "reason": null, "confirm_note": null}
    a4 kind=charge   text='$386.50'      rec#4 'Saltmarrow General Hospital, UB-04 itemized bill' rec_date=2026-06-19 status=accepted
       service_date={"state": "stated", "date_iso": "2026-06-09", "end_iso": "2026-06-12", "text": "June 9–12, 2026", "statement_date_iso": "2026-06-19", "reason": null, "confirm_note": null}
    a5 kind=charge   text='$712.00'      rec#4 'Saltmarrow General Hospital, UB-04 itemized bill' rec_date=2026-06-19 status=accepted
       service_date={"state": "stated", "date_iso": "2026-06-09", "end_iso": "2026-06-12", "text": "June 9–12, 2026", "statement_date_iso": "2026-06-19", "reason": null, "confirm_note": null}
    a6 kind=unclear  text='$8,123.50'    rec#4 'Saltmarrow General Hospital, UB-04 itemized bill' rec_date=2026-06-19 status=accepted
       service_date=null
    a7 kind=unclear  text='$8,023.50'    rec#6 'Quoinmere Mutual Health Plan, EOB' rec_date=2026-07-03 status=accepted
       service_date=null
    a8 kind=unclear  text='$3,610.00'    rec#6 'Quoinmere Mutual Health Plan, EOB' rec_date=2026-07-03 status=accepted
       service_date=null
    a9 kind=unclear  text='$4,413.50'    rec#6 'Quoinmere Mutual Health Plan, EOB' rec_date=2026-07-03 status=accepted
       service_date=null
   a10 kind=unclear  text='$3,530.80'    rec#6 'Quoinmere Mutual Health Plan, EOB' rec_date=2026-07-03 status=accepted
       service_date=null
   a11 kind=unclear  text='$882.70'      rec#6 'Quoinmere Mutual Health Plan, EOB' rec_date=2026-07-03 status=accepted
       service_date=null
== lib11
    a1 kind=charge   text='$3,260'       rec#3 'Wexcombe Memorial ED' rec_date=2026-03-18 status=accepted
       service_date={"state": "stated", "date_iso": "2026-03-18", "end_iso": null, "text": "March 18, 2026", "statement_date_iso": "2026-03-18", "reason": null, "confirm_note": null}
    a2 kind=charge   text='$250.00'      rec#9 'Fennimoor Spine Clinic, itemized ledger' rec_date=2026-06-15 status=accepted
       service_date={"state": "not_stated", "date_iso": null, "end_iso": null, "text": "(statement dated June 15, 2026; service date not stated)", "statement_date_iso": "2026-06-15", "reason": "no_date", "confirm_note": null}
    a3 kind=charge   text='$180.00'      rec#9 'Fennimoor Spine Clinic, itemized ledger' rec_date=2026-06-15 status=accepted
       service_date={"state": "not_stated", "date_iso": null, "end_iso": null, "text": "(statement dated June 15, 2026; service date not stated)", "statement_date_iso": "2026-06-15", "reason": "no_date", "confirm_note": null}
    a4 kind=charge   text='$2,310.00'    rec#9 'Fennimoor Spine Clinic, itemized ledger' rec_date=2026-06-15 status=accepted
       service_date={"state": "not_stated", "date_iso": null, "end_iso": null, "text": "(statement dated June 15, 2026; service date not stated)", "statement_date_iso": "2026-06-15", "reason": "no_date", "confirm_note": null}
    a5 kind=unclear  text='$2,740.00'    rec#9 'Fennimoor Spine Clinic, itemized ledger' rec_date=2026-06-15 status=accepted
       service_date=null
    a6 kind=unclear  text='$300.00'      rec#9 'Fennimoor Spine Clinic, itemized ledger' rec_date=2026-06-15 status=accepted
       service_date=null
    a7 kind=unclear  text='$274.00'      rec#9 'Fennimoor Spine Clinic, itemized ledger' rec_date=2026-06-15 status=accepted
       service_date=null
    a8 kind=unclear  text='$2,166.00'    rec#9 'Fennimoor Spine Clinic, itemized ledger' rec_date=2026-06-15 status=accepted
       service_date=null
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:34:10.550Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal && sed -n 111,135p p01.out | cut -c1-700; grep -n \"Counted\\|Date of service\" p01.out | head -20; grep -rn \"confirm_note\" /private/tmp/claude-501/*/*/*/*/*/*/scratchpad/a203/app --include=*.py | head"
}
````

### User / tool · 2026-11-03T00:34:22.699Z

**tool result**
````
===== [lib10] step 3 done url=http://127.0.0.1:7981/case/_HdnjAt2eCEWDdnvroHTEw/bills
Skip to the main content
Synthetic data only — never paste real records
‹
Your cases
Eob ub04 cms1500
9 records
Demo: recorded AI answers
Dark mode
✓
1 Add records
Done
(step 1 of 4)
✓
2 Check the timeline
Done
(step 2 of 4)
✓
3 Check the bills
Done
(step 3 of 4)
4
4 Get your letter
Ready
(step 4 of 4)
11:[case_09] s3 item=a1 boxes=[] :: Charge / Hobbleton Family Clinic, billing statement · statement dated March 1, 2026 /  / $275.00 /  / Date of service February 2, 2026 · statement dated March 1, 2026 /  / Written in the record as $275. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
12:[case_09] PROBE item=a1 {"svc": "February 2, 2026", "svcState": "stated", "stmt": " \u00b7 statement dated March 1, 2026", "note": null, "figure": "$275.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nHobbleton Family Clinic, billing statement \u00b7 statement dated March 1, 2026\n\n$275.00\n\nDate of service February 2, 2026 \u00b7 statement dated March 1, 2026\n\nWritten in the record as $275.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
49:Counted (1)
50:Amount	From	Date of service	
78:[lib10] s3 item=a2 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $4,920.00 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $4,920.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
79:[lib10] PROBE item=a2 {"svc": "June 9\u201312, 2026", "svcState": "stated", "stmt": " \u00b7 statement dated June 19, 2026", "note": null, "figure": "$4,920.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026\n\n$4,920.00\n\nDate of service June 9\u201312, 2026 \u00b7 statement dated June 19, 2026\n\nWritten in the record as $4,920.00.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
81:[lib10] s3 item=a3 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $2,105.00 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $2,105.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
82:[lib10] PROBE item=a3 {"svc": "June 9\u201312, 2026", "svcState": "stated", "stmt": " \u00b7 statement dated June 19, 2026", "note": null, "figure": "$2,105.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026\n\n$2,105.00\n\nDate of service June 9\u201312, 2026 \u00b7 statement dated June 19, 2026\n\nWritten in the record as $2,105.00.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
84:[lib10] s3 item=a4 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $386.50 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $386.50. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
85:[lib10] PROBE item=a4 {"svc": "June 9\u201312, 2026", "svcState": "stated", "stmt": " \u00b7 statement dated June 19, 2026", "note": null, "figure": "$386.50", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026\n\n$386.50\n\nDate of service June 9\u201312, 2026 \u00b7 statement dated June 19, 2026\n\nWritten in the record as $386.50.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
87:[lib10] s3 item=a5 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $712.00 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $712.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
88:[lib10] PROBE item=a5 {"svc": "June 9\u201312, 2026", "svcState": "stated", "stmt": " \u00b7 statement dated June 19, 2026", "note": null, "figure": "$712.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nSaltmarrow General Hospital, UB-04 itemized bill \u00b7 statement dated June 19, 2026\n\n$712.00\n\nDate of service June 9\u201312, 2026 \u00b7 statement dated June 19, 2026\n\nWritten in the record as $712.00.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
146:Counted (4)
147:Amount	From	Date of service	
196:[lib11] s3 item=a1 boxes=[] :: Charge / Wexcombe Memorial ED · March 18, 2026 /  / $3,260.00 /  / Date of service March 18, 2026 /  / Written in the record as $3,260. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
197:[lib11] PROBE item=a1 {"svc": "March 18, 2026", "svcState": "stated", "stmt": null, "note": null, "figure": "$3,260.00", "noteRole": null, "yesLabel": "Yes, count it", "card": "Charge\nWexcombe Memorial ED \u00b7 March 18, 2026\n\n$3,260.00\n\nDate of service March 18, 2026\n\nWritten in the record as $3,260.\n\nIf you count it, it's added to the bill total in the letter, with the highlighted words as its source."}
255:Counted (4)
256:Amount	From	Date of service	
ugrep: warning: /private/tmp/claude-501/*/*/*/*/*/*/scratchpad/a203/app: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:34:25.912Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal && sed -n 40,62p p01.out; sed -n 144,170p p01.out; sed -n 250,277p p01.out | cut -c1-300; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; grep -rn \"confirm_note\" $S/a203/app --include=*.py | head"
}
````

### User / tool · 2026-11-03T00:34:26.029Z

**tool result**
````
Check the bills
✓
You checked every bill amount.

This is the total line your letter will carry:

Billed charges accepted from these records: $275.00

Go to step 4: Get your letter
Counted (1)
Amount	From	Date of service	
$275.00	Hobbleton Family Clinic, billing statement	February 2, 2026	Change
Not counted by you (0)

You didn't leave out any charge.

Never counted (0)

These are never added to the total. The ones you listed go in the notes for the attorney.

Demo: recorded AI answers. These are real AI answers recorded earlier; nothing new is sent to an AI.
=====
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/case_09-step3-done.png

Go to step 4: Get your letter
Counted (4)
Amount	From	Date of service	
$4,920.00	Saltmarrow General Hospital, UB-04 itemized bill	June 9–12, 2026	Change
$2,105.00	Saltmarrow General Hospital, UB-04 itemized bill	June 9–12, 2026	Change
$386.50	Saltmarrow General Hospital, UB-04 itemized bill	June 9–12, 2026	Change
$712.00	Saltmarrow General Hospital, UB-04 itemized bill	June 9–12, 2026	Change
Not counted by you (0)

You didn't leave out any charge.

Never counted (7)

These are never added to the total. The ones you listed go in the notes for the attorney.

Amount	From	Why it's never counted	
$1,640.00	Saltmarrow General Hospital, UB-04 itemized bill	This figure is a rate, not a charge, so it is not added to the total.	Change
$8,123.50	Saltmarrow General Hospital, UB-04 itemized bill	Total or subtotal line: it repeats the charges listed with it, so it is not totaled.	Change
$8,023.50	Quoinmere Mutual Health Plan, EOB	Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.	Change
$3,610.00	Quoinmere Mutual Health Plan, EOB	Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.	Change
$4,413.50	Quoinmere Mutual Health Plan, EOB	Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.	Change
$3,530.80	Quoinmere Mutual Health Plan, EOB	Payment: money received, not a charge.	Change
$882.70	Quoinmere Mutual Health Plan, EOB	Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.	Change
Demo: recorded AI answers. These are real AI answers recorded earlier; nothing new is sent to an AI.
=====
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/lib10-step3-done.png
This is the total line your letter will carry:

Billed charges accepted from these records: $6,000.00

Go to step 4: Get your letter
Counted (4)
Amount	From	Date of service	
$3,260.00	Wexcombe Memorial ED	March 18, 2026	Change
$250.00	Fennimoor Spine Clinic, itemized ledger	(statement dated June 15, 2026; service date not stated)	Change
$180.00	Fennimoor Spine Clinic, itemized ledger	(statement dated June 15, 2026; service date not stated)	Change
$2,310.00	Fennimoor Spine Clinic, itemized ledger	(statement dated June 15, 2026; service date not stated)	Change
Not counted by you (0)

You didn't leave out any charge.

Never counted (4)

These are never added to the total. The ones you listed go in the notes for the attorney.

Amount	From	Why it's never counted	
$2,740.00	Fennimoor Spine Clinic, itemized ledger	Total or subtotal line: it repeats the charges listed with it, so it is not totaled.	Change
$300.00	Fennimoor Spine Clinic, itemized ledger	Payment: money received, not a charge.	Change
$274.00	Fennimoor Spine Clinic, itemized ledger	Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.	Change
$2,166.00	Fennimoor Spine Clinic, itemized ledger	Balance or amount due: worked out from charges, payments and adjustments, not a charge.	Change
Demo: recorded AI answers. These are real AI answers recorded earlier; nothing new is sent to an AI.
=====
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/lib11-step3-done.png
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/lib11-step4.png
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a203/app/backend/store.py:121:    not stated)'), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a203/app/backend/store.py:140:        note = SD.confirm_note(r["reason"], r["raw"])
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a203/app/backend/store.py:143:            "statement_date_iso": rd, "reason": r["reason"], "confirm_note": note}
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a203/app/backend/service_date.py:76:def confirm_note(reason, raw) -> str:
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:34:36.775Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; sed -n 1,120p $S/a203/app/backend/service_date.py"
}
````

### User / tool · 2026-11-03T00:34:36.872Z

**tool result**
````
"""The service date a charge line prints, only when code is certain (D-071 amendment, T-202 round 2). Code only, no LLM (LLM_VS_CODE rows 2 and 3).

The letter's charge line carries a date of service. A date there is a claim to an adjuster, so it is printed only when exactly ONE unambiguous service date (or one complete
period) is tied to THAT line, by its own sentence, by its table row and column header, or (for a coded line with no date of its own) by the one period the bill states for its
services ('statement period 06/09/2026 to 06/12/2026', 'the run of 09/14/2026'). Everything else is `not_stated`, with a reason the Step 3 screen shows as a note asking the
paralegal to confirm the date from the quote:
  - a numeric date that can be read two ways (04/05/2026), unless one reading falls after the record's own date (a service cannot follow its statement), or the other end of
    the same period fixes the order (06/28/2026-07/02/2026);
  - a two-digit year, a date with no year, a date that is not on the calendar, a period whose end is missing or before its start;
  - several candidate dates for the line (a CMS-1500 'dates of service 06/24/2026 and 07/08/2026', 'exam 03/27/2026 and x-ray 03/28/2026 charge $250.00');
  - a row with two dates and no header that says which is the date of service, or whose only date sits under Posted, Statement, Billed ...;
  - no date at all on a bill line (a dated encounter note, not a bill, keeps the note's own date).
Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
import datetime as _dt
import re

from app.backend import amounts as AM

_MON = AM._MON
_ORD = r"(?:st|nd|rd|th)?"
_DASH = "–—"
_TOK = re.compile(
    r"(?<![\w/$])(?:"
    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
    r"|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2}))"
    rf"|(?P<mper>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}\s*[-{_DASH}]\s*(?:(?:{_MON})\.?\s+)?\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
    rf"|(?P<mdy>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
    rf"|(?P<dmy>\d{{1,2}}{_ORD}[\s-]+(?:of\s+)?(?:{_MON})\.?[\s-]*,?\s*\d{{4}})"
    r"|(?P<md>\d{1,2}/\d{1,2}(?!\s*(?:hrs?|hours?|units?|miles?|mins?|visits?|sessions?)\b))"
    r")(?![\w/]|\.\d)", re.IGNORECASE)
_JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
_LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
# the word right before a date that makes it a billing-side date, never a date of service
_NON_SVC_LEAD = re.compile(r"\b(?:statements?|stmt|invoice|billing|billed|bill|printed|issued|mailed|as[\s-]of|due|posted|post|paid|received|payment|processed|balance|created|generated|sent)\b"
                           r"(?:\s+(?:date|dated|on|of))?\s*[:#]?\s*$", re.IGNORECASE)
_H_DOS = re.compile(r"\bdos\b|date\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter", re.IGNORECASE)
_H_NON = re.compile(r"post|statement|stmt|bill|invoice|paid|payment|due|receiv|process|entered|created|balance|adjust|insur|submitted|mailed", re.IGNORECASE)

REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "non_service_date", "no_date")


def display(first, last=None) -> str:
    """'June 9, 2026' for one day; a period as a range: 'June 9–12, 2026', 'June 28–July 2, 2026', 'December 30, 2026–January 2, 2027' (D-071)."""
    def lng(iso):
        d = _dt.date.fromisoformat(iso)
        return f"{d.strftime('%B')} {d.day}, {d.year}"
    if not last or last == first:
        return lng(first)
    a, b = _dt.date.fromisoformat(first), _dt.date.fromisoformat(last)
    if (a.year, a.month) == (b.year, b.month):
        return f"{a.strftime('%B')} {a.day}–{b.day}, {a.year}"
    if a.year == b.year:
        return f"{a.strftime('%B')} {a.day}–{b.strftime('%B')} {b.day}, {a.year}"
    return f"{lng(first)}–{lng(last)}"


def not_stated_text(statement_iso) -> str:
    """The text the letter puts after the provider when no service date is certain (T-200)."""
    if statement_iso:
        return f"(statement dated {display(statement_iso)}; service date not stated)"
    return "(service date not stated)"


_WHY = {
    "ambiguous_numeric": "The date written as {raw} can be read as month/day or day/month, and the record does not settle which.",
    "two_digit_year": "The date {raw} has a two-digit year, which the code does not guess.",
    "no_year": "The date {raw} states no year, which the code does not borrow from the statement.",
    "invalid": "{raw} is not a complete date on the calendar.",
    "several_dates": "This line or its bill states more than one date ({raw}) and the record does not say which one belongs to this charge.",
    "non_service_date": "The only date near this line ({raw}) is a posting, statement or billing date, not a date of service.",
    "no_date": "The line states no date of service.",
}


def confirm_note(reason, raw) -> str:
    """The Step 3 note for a charge whose service date is not certain: why, and the ask (D-071 amendment)."""
    return (_WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") +
            " The letter prints no service date for this line. Confirm the date from the quote before you rely on it.")


def _iso(y, mo, d):
    try:
        return _dt.date(y, mo, d).isoformat() if 1900 <= y <= 2100 else None
    except ValueError:
        return None


class _Tok:
    __slots__ = ("start", "end", "raw", "kind", "fixed", "ambiguous", "order", "flaw", "first", "last")

    def __init__(self, m):
        self.start, self.end, self.raw, self.kind = m.start(), m.end(), m.group(0), m.lastgroup
        self.fixed, self.ambiguous, self.order, self.flaw, self.first, self.last = None, None, None, None, None, None
        getattr(self, "_" + self.kind)(m.group(0))
        if self.flaw is None and not (self.fixed or self.ambiguous or self.first):
            self.flaw = "invalid"

    def _iso(self, s):
        y, mo, d = (int(x) for x in s.split("-"))
        self.fixed = _iso(y, mo, d)

    def _num(self, s):
        a, b, y = re.split(r"[/.-]", s)
        if len(y) == 2:
            self.flaw = "two_digit_year"
            return
        a, b, y = int(a), int(b), int(y)
        md, dm = _iso(y, a, b), _iso(y, b, a)
        if md and dm and md != dm:
            self.ambiguous = {"MD": md, "DM": dm}
        elif md or dm:
            self.fixed = md or dm
            self.order = None if (md and dm) else ("MD" if md else "DM")

    def _mdy(self, s):
        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}}))?$", s, re.IGNORECASE)
        if not m.group(3):
            self.flaw = "no_year"
            return
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:34:44.489Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; sed -n 112,150p $S/a203/app/backend/store.py; grep -n \"plain\" $S/a203/app/frontend/guided/*.js | grep -n \"plain =\\|function plain\\|plain:\" | head; cd /Users/arsis/zlayt-pm-project; sed -n 1,200p tests/e2e/guided/test_t205.py 2>/dev/null | head -5; sed -n 1,200p $S/a203/tests/e2e/guided/test_t205.py | sed -n 60,149p"
}
````

### User / tool · 2026-11-03T00:34:44.610Z

**tool result**
````
        return None
    from app.backend import generator          # lazy: generator imports store
    i = start - generator.body_offset(rec)
    return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None


def charge_service_date(item: dict, rec, pos) -> dict:
    """D-071 (extends T-200, amended in T-202 r2): what a charge line prints as its date, and why, for the letter AND the case view (Step 3 shows exactly this).
    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or '(statement dated June 15, 2026; service date
    not stated)'), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
    A date is stated only when code is certain (service_date.resolve): the bill line's own single date or complete period, tied to the line by its sentence, its row and column
    header, or the one period its bill states. The record's date of a ledger, invoice or UB-04 is the statement's, never a fallback: a bill line the code cannot read has no
    service date. A dated encounter record's (visit note, imaging report) date is the visit. A charge the paralegal counted for a missing date of service (D-064) is
    not stated, with no note (she counted it knowing). Code only."""
    from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
    rd = (rec or {}).get("date_iso")
    bill = AM.billing_document((rec or {}).get("source"), item.get("excerpt") or "")
    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
    if counted_undated:
        r = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""}
    elif rec is None or pos is None or not item.get("excerpt"):
        r = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""} if bill else (
            {"state": "stated", "first": rd, "last": None, "reason": None, "raw": ""} if rd else {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""})
    else:
        r = SD.resolve(item["excerpt"], pos, rec.get("source"), rd)
    stated = r["state"] == "stated"
    note = None
    if not stated and not counted_undated:
        note = SD.confirm_note(r["reason"], r["raw"])
    return {"state": r["state"], "date_iso": r["first"], "end_iso": r["last"] if stated else None,
            "text": SD.display(r["first"], r["last"]) if stated else SD.not_stated_text(rd),
            "statement_date_iso": rd, "reason": r["reason"], "confirm_note": note}


def charge_service_dates(item: dict, rec, pos) -> tuple:
    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
    d = charge_service_date(item, rec, pos)
    return d["date_iso"], d["end_iso"]

1:/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a203/app/frontend/guided/core.js:49:      const plain = err && typeof err.message === "string" && err.message && status < 500 ? err.message : null;     // server sentences are shown as given (spec section 0)
7:/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a203/app/frontend/guided/review.js:15:  R.plain = function (text) {
24:/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a203/app/frontend/guided/step2.js:232:    const ans = (iso) => ({ label: R.longDate(iso), sub: [reading(iso), iso === sug ? "Suggested" : ""].filter(Boolean).join(" · "), plain: true, run: () => pick(iso) });
41:/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a203/app/frontend/guided/step1.js:102:    function plain(e, pdf) {
"""T-205 (D-071 + amendment + T-202 r2 clarification): guided Step 3 shows the date of service the letter prints (amounts[].service_date.text, byte for byte) and the plain confirm note when the date is not
certain. Never the statement date as the service date. Real browser, the fixture backend, the real API. case_09 (statement dated Mar 1, service Feb 2), lib10 (one UB-04 period, June 9-12, statement June 19),
a charge she counted for a missing date (D-064: real, not stated, no note), and a not-stated charge WITH a note: the fixture set has no bill that parses to a doubtful date, so that one stub-rewrites the case
response's service_date with the backend's own sentences (service_date.confirm_note / not_stated_text), everything else on the page is real."""
import re
    assert seen == [], seen


def test_lib10_shows_the_one_stated_period_for_every_charge(page, make):
    seen = watch(page)
    tok = make(LIB10); charges = [a for a in case(tok)["amounts"] if a["kind"] == "charge"]
    assert [a["id"] for a in charges] == ["a2", "a3", "a4", "a5"]
    letter = letter_dates(tok)
    for a in charges:
        sd = a["service_date"]; assert sd["text"] == "June 9–12, 2026" and sd["statement_date_iso"] == "2026-06-19"
        open_item(page, tok, a["id"], step="bills")
        assert page.get_by_test_id("service-date-text").inner_text() == "June 9–12, 2026", a["id"]
        assert "statement dated June 19, 2026" in page.get_by_test_id("service-date").inner_text()
        assert "statement dated June 19, 2026" in page.get_by_test_id("src-head").inner_text()
        assert page.get_by_test_id("confirm-note").count() == 0
        assert f"June 9–12, 2026: {a['text']}" in letter, "the letter carries the same period"
    # a rate is not a charge: it has no date of service to show
    open_item(page, tok, "a1", step="bills"); assert page.get_by_test_id("service-date").count() == 0
    assert seen == [], seen


def test_a_charge_with_no_stated_date_shows_the_not_stated_text_and_never_the_statement_date_as_the_service_date(page, make):
    """Real: a ledger line she counted (D-064) has no date of service and no note (she already knows). Step 3 and the done list show the letter's own text."""
    seen = watch(page)
    tok = make(LIB11); a = item(tok, "a2"); assert a["kind"] == "unclear" and a["countable"]
    st, r = C.api("POST", f"/api/cases/{tok}/items/a2/review", {"action": "count", "confirm": "separate_charge", "version": a["version"], "expected_status": "pending",
                                                              **({"confirm_flag": a["count_confirm"]["confirm_with"]} if a.get("count_confirm") else {})}); assert st == 200, r
    a = item(tok, "a2"); sd = a["service_date"]
    assert a["kind"] == "charge" and sd["state"] == "not_stated" and sd["date_iso"] is None and sd["confirm_note"] is None
    open_item(page, tok, "a2", step="bills")
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    assert re.fullmatch(r"\(statement dated [A-Z][a-z]+ \d{1,2}, \d{4}; service date not stated\)|\(service date not stated\)", sd["text"]), sd["text"]
    assert page.get_by_test_id("service-date").get_attribute("data-state") == "not_stated"
    assert page.get_by_test_id("confirm-note").count() == 0
    assert f"{sd['text']}: " in letter_dates(tok), "the letter prints this very text"
    assert "statement dated" in page.get_by_test_id("src-head").inner_text() or "no date" in page.get_by_test_id("src-head").inner_text()
    # done list: decide the rest over the API, the Date of service column carries the same text
    for i in case(tok)["amounts"]:
        if i["review_status"] == "pending" and i["id"] != "a2":
            C.api("POST", f"/api/cases/{tok}/items/{i['id']}/review", {"action": "accept"})
    go(page, f"/case/{tok}/bills")
    if page.get_by_test_id("list-counted").count():
        expect(page.get_by_test_id("list-counted")).to_contain_text("Date of service")
        assert sd["text"] in page.get_by_test_id("list-counted").inner_text()
    assert seen == [], seen


def test_a_not_stated_charge_with_a_note_shows_the_note_in_plain_words_beside_the_quote(page, make):
    """The fixture set has no bill that parses to a doubtful date, so the case response's service_date for one charge is replaced with the backend's own sentences."""
    seen = watch(page)
    tok = make(LIB10); a = item(tok, "a2")
    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="ambiguous_numeric", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("ambiguous_numeric", "04/05/2026"))

    def rewrite(route):
        r = route.fetch(); body = r.json()
        for x in body.get("amounts", []):
            if x["id"] == "a2":
                x["service_date"] = sd
        route.fulfill(response=r, json=body)
    page.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
    open_item(page, tok, "a2", step="bills")
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    assert page.get_by_test_id("service-date").get_attribute("data-state") == "not_stated"
    note = page.get_by_test_id("confirm-note"); expect(note).to_be_visible(); assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-note]").count() == 1
    t = note.inner_text()
    assert "04/05/2026" in t and "The letter prints no service date for this line." in t and "Confirm the date from the highlighted words" in t, t      # the server's sentence, in the plain vocabulary
    assert not re.search(r"\bquote\b|\bmodel\b|\bexcerpt\b", t, re.I), t
    assert note.get_attribute("role") == "note"
    assert "statement dated June 19, 2026" in page.get_by_test_id("src-head").inner_text()
    assert page.get_by_test_id("statement-date").count() == 0, "the not-stated text already names the statement date"
    # nothing about the decision changes: the human still answers Yes or No
    expect(page.get_by_test_id("answer-yes")).to_be_enabled()
    assert page.locator("[data-testid=card-source] mark").count() >= 1, "the quote is on the same screen"
    assert seen == [], seen


def test_the_date_and_note_fit_a_phone(phone, make):
    tok = make(LIB10); a = item(tok, "a2")
    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="no_year", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("no_year", "April 5"))
    def rewrite(route):
        r = route.fetch(); body = r.json()
        for x in body.get("amounts", []):
            if x["id"] == "a2":
                x["service_date"] = sd
        route.fulfill(response=r, json=body)
    phone.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), rewrite)
    open_item(phone, tok, "a2", step="bills")
    expect(phone.get_by_test_id("confirm-note")).to_be_visible()
    assert phone.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), "no sideways scroll"
    assert phone.get_by_test_id("answer-yes").is_visible()
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:35:01.113Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal && cat > p02_notes.py <<'EOF'\n\"\"\"T-205 paralegal: render every confirm_note reason in the Step 3 card (stub of GET /api/cases/{token} service_date only, as the worker's own test does;\nthe fixture set has no bill that parses to a doubtful date). Wording is the backend's own SD.confirm_note. Run via h.py.\"\"\"\nimport json, re, sys\nsys.path.insert(0, \"SCRATCH_ROOT\")\nfrom app.backend import service_date as SD\nTOK = {\"case_09\": (\"Rb_-aRcu7JXIMZ90rAiyHA\", \"a1\", \"2026-03-01\"), \"lib10\": (\"_HdnjAt2eCEWDdnvroHTEw\", \"a2\", \"2026-06-19\")}\nRAW = {\"ambiguous_numeric\": \"04/05/2026\", \"two_digit_year\": \"04/05/26\", \"no_year\": \"April 5\", \"invalid\": \"02/30/2026\", \"several_dates\": \"06/24/2026 and 07/08/2026\",\n       \"non_service_date\": \"03/01/2026\", \"no_date\": \"\"}\nfor case, (tok, aid, stmt) in TOK.items():\n    for reason, raw in RAW.items():\n        sd = {\"state\": \"not_stated\", \"date_iso\": None, \"end_iso\": None, \"reason\": reason, \"text\": SD.not_stated_text(stmt), \"statement_date_iso\": stmt, \"confirm_note\": SD.confirm_note(reason, raw)}\n        def rewrite(route, sd=sd, aid=aid):\n            r = route.fetch(); body = r.json()\n            for x in body.get(\"amounts\", []):\n                if x[\"id\"] == aid:\n                    x[\"service_date\"] = sd\n            route.fulfill(response=r, json=body)\n        pat = re.compile(rf\"/api/cases/{tok}(\\?.*)?$\")\n        pg.route(pat, rewrite)\n        pg.goto(f\"{BASE}/case/{tok}/bills?item={aid}\")\n        pg.wait_for_selector(\"[data-testid=view][data-ready]\")\n        pg.wait_for_selector(\"[data-testid=confirm-note]\", timeout=8000)\n        pg.wait_for_timeout(300)\n        info = pg.evaluate(\"\"\"() => { const n = document.querySelector('[data-testid=confirm-note]'); const r = n.getBoundingClientRect();\n          const y = document.querySelector('[data-testid=answer-yes]').getBoundingClientRect();\n          return {note: n.innerText, noteTop: Math.round(r.top), noteBottom: Math.round(r.bottom), vh: innerHeight, yesTop: Math.round(y.top), svc: document.querySelector('[data-testid=service-date]').innerText,\n                  head: (document.querySelector('[data-testid=src-head]')||{innerText:''}).innerText, tag: (document.querySelector('.work .card')||{innerText:''}).innerText.split('\\\\n')[0]}; }\"\"\")\n        log(f\"[{case}/{reason}] \" + json.dumps(info, ensure_ascii=False))\n        if reason in (\"ambiguous_numeric\", \"no_date\") and case == \"lib10\":\n            shot(f\"note-{case}-{reason}\", full=False)\n        pg.unroute(pat)\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\npython3 - <<EOF\np=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/p02_notes.py\"\ns=open(p).read().replace(\"SCRATCH_ROOT\",\"$S/a203\"); open(p,\"w\").write(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-205-paralegal/h.py artifacts/review-evidence/T-205-paralegal/p02_notes.py > artifacts/review-evidence/T-205-paralegal/p02.out 2>&1; grep -n \"^\\[\\(case_09\\|lib10\\)/\\|ERRORS\\|Error\\|Traceback\" artifacts/review-evidence/T-205-paralegal/p02.out | cut -c1-1100"
}
````

### User / tool · 2026-11-03T00:35:31.704Z

**tool result**
````
1:Error occurred in event listener
2:Traceback (most recent call last):
45:    raise TypeError(f'Object of type {o.__class__.__name__} '
46:TypeError: Object of type Request is not JSON serializable
48:Traceback (most recent call last):
67:TypeError: BrowserContext.close: Object of type Request is not JSON serializable
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:35:33.693Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal && sed -n 1,50p p02.out | cut -c1-200"
}
````

### User / tool · 2026-11-03T00:35:33.773Z

**tool result**
````
Error occurred in event listener
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_page.py", line 312, in _on_route
    handled = await route_handler.handle(route)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_helper.py", line 456, in handle
    raise e
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_helper.py", line 443, in handle
    return await self._handle_internal(route)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_helper.py", line 479, in _handle_internal
    await handler_finished_future
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_helper.py", line 470, in _handler
    self.handler(route, route.request)  # type: ignore
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_impl_to_api_mapping.py", line 140, in wrapper_func
    return handler(
           ^^^^^^^^
  File "artifacts/review-evidence/T-205-paralegal/p02_notes.py", line 17, in rewrite
    route.fulfill(response=r, json=body)
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 22711, in fulfill
    self._sync(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_network.py", line 430, in fulfill
    await self._handle_route(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_network.py", line 508, in _handle_route
    raise e
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_network.py", line 504, in _handle_route
    await callback()
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_network.py", line 451, in _inner_fulfill
    body = json_utils.dumps(json)
           ^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 231, in dumps
    return _default_encoder.encode(obj)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 200, in encode
    chunks = self.iterencode(o, _one_shot=True)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 258, in iterencode
    return _iterencode(o, 0)
           ^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type Request is not JSON serializable
### run p02_notes.py at 18:35:01
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/h.py", line 58, in <module>
    main(sys.argv[1])
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:35:37.664Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal && python3 - <<'EOF'\np=\"p02_notes.py\"\ns=open(p).read()\ns=s.replace(\"\"\"        def rewrite(route, sd=sd, aid=aid):\n            r = route.fetch(); body = r.json()\n            for x in body.get(\"amounts\", []):\n                if x[\"id\"] == aid:\n                    x[\"service_date\"] = sd\n            route.fulfill(response=r, json=body)\n\"\"\",\"\"\"        def mk(sd, aid):\n            def rewrite(route):\n                r = route.fetch(); body = r.json()\n                for x in body.get(\"amounts\", []):\n                    if x[\"id\"] == aid:\n                        x[\"service_date\"] = sd\n                route.fulfill(response=r, json=body)\n            return rewrite\n        rewrite = mk(sd, aid)\n\"\"\")\nopen(p,\"w\").write(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-205-paralegal/h.py artifacts/review-evidence/T-205-paralegal/p02_notes.py > artifacts/review-evidence/T-205-paralegal/p02.out 2>&1; grep -n \"^\\[\\(case_09\\|lib10\\)/\\|ERRORS\\|Error\\|Traceback\" artifacts/review-evidence/T-205-paralegal/p02.out | cut -c1-1000"
}
````

### User / tool · 2026-11-03T00:35:44.013Z

**tool result**
````
2:[case_09/ambiguous_numeric] {"note": "The date written as 04/05/2026 can be read as month/day or day/month, and the record does not settle which. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 643, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated March 1, 2026; service date not stated)", "head": "Record 2 · Hobbleton Family Clinic, billing statement · statement dated March 1, 2026", "tag": "From the record"}
3:[case_09/two_digit_year] {"note": "The date 04/05/26 has a two-digit year, which the code does not guess. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 643, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated March 1, 2026; service date not stated)", "head": "Record 2 · Hobbleton Family Clinic, billing statement · statement dated March 1, 2026", "tag": "From the record"}
4:[case_09/no_year] {"note": "The date April 5 states no year, which the code does not borrow from the statement. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 643, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated March 1, 2026; service date not stated)", "head": "Record 2 · Hobbleton Family Clinic, billing statement · statement dated March 1, 2026", "tag": "From the record"}
5:[case_09/invalid] {"note": "02/30/2026 is not a complete date on the calendar. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 643, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated March 1, 2026; service date not stated)", "head": "Record 2 · Hobbleton Family Clinic, billing statement · statement dated March 1, 2026", "tag": "From the record"}
6:[case_09/several_dates] {"note": "This line or its bill states more than one date (06/24/2026 and 07/08/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 667, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated March 1, 2026; service date not stated)", "head": "Record 2 · Hobbleton Family Clinic, billing statement · statement dated March 1, 2026", "tag": "From the record"}
7:[case_09/non_service_date] {"note": "The only date near this line (03/01/2026) is a posting, statement or billing date, not a date of service. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 643, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated March 1, 2026; service date not stated)", "head": "Record 2 · Hobbleton Family Clinic, billing statement · statement dated March 1, 2026", "tag": "From the record"}
8:[case_09/no_date] {"note": "The line states no date of service. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 619, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated March 1, 2026; service date not stated)", "head": "Record 2 · Hobbleton Family Clinic, billing statement · statement dated March 1, 2026", "tag": "From the record"}
9:[lib10/ambiguous_numeric] {"note": "The date written as 04/05/2026 can be read as month/day or day/month, and the record does not settle which. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 643, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated June 19, 2026; service date not stated)", "head": "Record 4 · Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026", "tag": "From the record"}
11:[lib10/two_digit_year] {"note": "The date 04/05/26 has a two-digit year, which the code does not guess. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 643, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated June 19, 2026; service date not stated)", "head": "Record 4 · Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026", "tag": "From the record"}
12:[lib10/no_year] {"note": "The date April 5 states no year, which the code does not borrow from the statement. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 643, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated June 19, 2026; service date not stated)", "head": "Record 4 · Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026", "tag": "From the record"}
13:[lib10/invalid] {"note": "02/30/2026 is not a complete date on the calendar. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 643, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated June 19, 2026; service date not stated)", "head": "Record 4 · Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026", "tag": "From the record"}
14:[lib10/several_dates] {"note": "This line or its bill states more than one date (06/24/2026 and 07/08/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 667, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated June 19, 2026; service date not stated)", "head": "Record 4 · Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026", "tag": "From the record"}
15:[lib10/non_service_date] {"note": "The only date near this line (03/01/2026) is a posting, statement or billing date, not a date of service. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 643, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated June 19, 2026; service date not stated)", "head": "Record 4 · Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026", "tag": "From the record"}
16:[lib10/no_date] {"note": "The line states no date of service. The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.", "noteTop": 571, "noteBottom": 619, "vh": 900, "yesTop": 782, "svc": "Date of service (statement dated June 19, 2026; service date not stated)", "head": "Record 4 · Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026", "tag": "From the record"}
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:35:46.181Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/note-lib10-ambiguous_numeric.png"
}
````

### User / tool · 2026-11-03T00:35:46.192Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:35:46.480Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/lib11-s3-01-a2.png"
}
````

### User / tool · 2026-11-03T00:35:46.487Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:35:52.234Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal && for c in case_09 lib10 lib11; do echo \"=== $c letter\"; grep -n -i \"statement dated\\|service date\\|\\\\$\" ui-$c-letter.txt | cut -c1-260; echo \"--- notes\"; grep -n -i \"date\\|bill\" ui-$c-notes.txt | cut -c1-260 | head -20; done"
}
````

### User / tool · 2026-11-03T00:35:52.396Z

**tool result**
````
=== case_09 letter
21:Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00
22:Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."
24:Billed charges accepted from these records: $275.00
--- notes
24:BILLS TO REQUEST (entry in the letter, no accepted charge)
28:- Record 2 (Hobbleton Family Clinic, billing statement, March 1, 2026) — dismissed
=== lib10 letter
37:Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00
38:Source [Ex. __ / Bates __]: "FL47 total charges $4,920.00."
39:Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00
40:Source [Ex. __ / Bates __]: "Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
41:Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $386.50
42:Source [Ex. __ / Bates __]: "Rev 0250 pharmacy, 14 units, FL47 total charges $386.50."
43:Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $712.00
44:Source [Ex. __ / Bates __]: "Rev 0300 laboratory, 6 units, FL47 total charges $712.00."
46:Billed charges accepted from these records: $8,123.50
--- notes
16:- Record 4 (Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026): "FL44 rate $1,640.00 per day" Rate $1,640; visit count not stated. Request itemized ledger from Saltmarrow General Hospital.
17:- Record 4 (Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026): "Rev 0001 total charges $8,123.50." Not totaled ($8,123.50): Total or subtotal line: it repeats the charges listed with it, so it is not totaled.
19:- Record 6 (Quoinmere Mutual Health Plan, EOB, July 3, 2026): "you may owe $882.70." Not totaled ($882.70): Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.
20:- Record 6 (Quoinmere Mutual Health Plan, EOB, July 3, 2026): "Amount billed $8,023.50" Not totaled ($8,023.50): Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.
21:- Record 6 (Quoinmere Mutual Health Plan, EOB, July 3, 2026): "network discount $3,610.00" Not totaled ($3,610.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.
22:- Record 6 (Quoinmere Mutual Health Plan, EOB, July 3, 2026): "allowed amount $4,413.50" Not totaled ($4,413.50): Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.
30:BILLS TO REQUEST (entry in the letter, no accepted charge)
=== lib11 letter
37:Wexcombe Memorial ED, March 18, 2026: $3,260.00
38:Source [Ex. __ / Bates __]: "ED charge: $3,260."
39:Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00
40:Source [Ex. __ / Bates __]: "New patient exam charge $250.00"
41:Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $180.00
42:Source [Ex. __ / Bates __]: "x-ray charge $180.00"
43:Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $2,310.00
44:Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"
46:Billed charges accepted from these records: $6,000.00
--- notes
26:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Adjustment (courtesy discount) -$274.00." Not totaled ($274.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.
35:BILLS TO REQUEST (entry in the letter, no accepted charge)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:35:59.835Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal && cat > p03_revisit.py <<'EOF'\n\"\"\"T-205: revisit the counted lib11 ledger line a2 (kind now charge, service date not stated, no note) and a1 on lib11; read the card.\"\"\"\nimport json\ntok = \"WMUiPxizxiRAqdrprp3a9Q\"\nfor aid in (\"a2\", \"a1\"):\n    pg.goto(f\"{BASE}/case/{tok}/bills?item={aid}\")\n    pg.wait_for_selector(\"[data-testid=view][data-ready]\"); pg.wait_for_timeout(500)\n    c = pg.evaluate(\"() => { const c = document.querySelectorAll('.work .card'); return Array.from(c).map(x => x.innerText).join('\\\\n#####\\\\n') }\")\n    log(f\"[lib11 revisit {aid}] \" + c.replace(\"\\n\", \" / \"))\n    shot(f\"lib11-revisit-{aid}\")\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-205-paralegal/h.py artifacts/review-evidence/T-205-paralegal/p03_revisit.py > artifacts/review-evidence/T-205-paralegal/p03.out 2>&1; grep -n \"revisit\\|ERRORS\" artifacts/review-evidence/T-205-paralegal/p03.out | cut -c1-900"
}
````

### User / tool · 2026-11-03T00:36:01.615Z

**tool result**
````
1:### run p03_revisit.py at 18:36:00
2:[lib11 revisit a2] From the record / Record 9 · Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026 / === Record 9 === / Date: 2026-06-15 / Source: Fennimoor Spine Clinic, itemized ledger / Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection." / ##### / Charge / Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026 /  / $250.00 /  / Date of service (statement dated June 15, 2026; service date not stated) /  / Written in the record as $250.00. /  / Your answer: counted in the bill total. You can change it.
3:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/lib11-revisit-a2.png
4:[lib11 revisit a1] From the record / Record 3 · Wexcombe Memorial ED · March 18, 2026 / === Record 3 === / Date: 2026-03-18 / Source: Wexcombe Memorial ED / Excerpt: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture. ED charge: $3,260." / ##### / Charge / Wexcombe Memorial ED · March 18, 2026 /  / $3,260.00 /  / Date of service March 18, 2026 /  / Written in the record as $3,260. /  / Your answer: counted in the bill total. You can change it.
5:[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-205-paralegal/lib11-revisit-a1.png
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:36:07.131Z

**tool call — Bash**
````
{
 "command": "kill 63090; sleep 1; lsof -iTCP:7981 -sTCP:LISTEN -nP; echo \"lsof exit $?\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7981/api/health; grep -c \"ERRORS\" artifacts/review-evidence/T-205-paralegal/p01.out artifacts/review-evidence/T-205-paralegal/p02.out artifacts/review-evidence/T-205-paralegal/p03.out; ls reviews/T-205* 2>&1 | head -3; git status --short | head -3"
}
````

### User / tool · 2026-11-03T00:36:08.370Z

**tool result**
````
lsof exit 1
000
artifacts/review-evidence/T-205-paralegal/p03.out:0
artifacts/review-evidence/T-205-paralegal/p02.out:0
artifacts/review-evidence/T-205-paralegal/p01.out:0
ls: reviews/T-205*: No such file or directory
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:36:38.237Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-205-paralegal.md",
 "content": "# T-205 review — paralegal-reviewer (Maria Delgado)\n\nCommit 203ac6a, fresh `git archive` in an empty scratch directory, demo mode (fixture backend, `ZLAYT_MODE=local`, health `demo_mode: true`) on port 7981. Listener PID 63090 stopped afterward (`lsof` exit 1, `curl` = 000). Private values seen: 0 (<redacted> count 0).\n\n**Verdict: pass (2 minors, 1 nit).** The service date on the Step 3 charge card equals what the letter prints on all three cases. The statement date is labeled \"statement dated\" wherever a charge card shows one, with one gap on uncounted ledger lines.\n\n- case_09: card \"Date of service February 2, 2026 · statement dated March 1, 2026\". Letter: \"Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00\". Match.\n- lib10: all four charges show \"Date of service June 9–12, 2026 · statement dated June 19, 2026\". Letter prints \"June 9–12, 2026\" on each line. Match.\n- lib11: ED line \"Date of service March 18, 2026\" (no statement label, correct for a dated visit note). Counted ledger lines show \"(statement dated June 15, 2026; service date not stated)\" in the Step 3 done list, on revisit, and in the letter. Match.\n- Confirm note: the fixture set has no bill with a doubtful date, so no real note appeared on any of the three cases. I rendered all 7 backend reasons by rewriting only `service_date` in the GET case response (the worker's own method). The note shows in the card foot, in plain words, visible without scrolling at 1440x900, and says what the letter will do and what to do. Wording gaps are in the findings. Grade-only-the-display applies; T-202 r3 may change which lines are certain.\n\n```json\n{\"card\": \"T-205\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit 203ac6a (git archive extracted to session scratchpad a203/); app http://127.0.0.1:7981 demo mode (fixture backend, curated set, ZLAYT_MODE=local, health demo_mode true); case_09 (POST /api/cases with golden text, opened in UI), lib10 and lib11 (library tile). Display only; T-202 r3 parse changes not graded. Private values seen: 0.\",\n \"exercised\": [\"Read personas/paralegal.md, board show T-205 (handoff), D-071 and its amendment/clarification in memory/ORCHESTRATOR_DECISIONS.md:84-92, git show 203ac6a (step3.js/css diff)\",\n  \"git archive 203ac6a into scratchpad a203; started server on 7981; health check demo_mode true; later killed PID 63090 and confirmed lsof exit 1 and curl 000\",\n  \"artifacts/review-evidence/T-205-paralegal/p01.py via h.py: for case_09, lib10, lib11 did Step 2 by keyboard, walked every Step 3 card (DOM probe of service-date-text, statement-date, confirm-note, card text), counted charges, Step 4 download of letter and notes; output p01.out, letters ui-*-letter.txt, ui-*-notes.txt\",\n  \"api.py / api.out: GET /api/cases/{token} amounts[].service_date for all three cases next to the record date\",\n  \"p02_notes.py / p02.out: all 7 confirm_note reasons rendered on case_09 a1 and lib10 a2 with service_date stubbed in the GET response (fixtures have no real doubtful-date bill); measured note position vs viewport; screenshots note-lib10-ambiguous_numeric.png, note-lib10-no_date.png\",\n  \"p03_revisit.py / p03.out: revisited counted lib11 a2 and a1; screenshots lib11-revisit-a2.png, lib11-s3-01-a2.png (pre-count card)\",\n  \"Compared Step 3 date text with letter lines by grep (case_09 line 21, lib10 lines 37-44, lib11 lines 37-44); console/http errors: none (ERRORS count 0 in p01/p02/p03 outputs)\"],\n \"verdict\": \"pass\",\n \"scores\": {\"verify_quickly\": 4, \"step3_date_matches_letter\": 5, \"statement_date_labeled\": 4, \"confirm_note_plain_and_actionable\": 3},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"Uncounted lib11 ledger lines show the statement date bare, with no Date of service line and no 'statement dated' label\",\n   \"evidence\": \"p01.out:200 (PROBE lib11 a2): card 'Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 / $250.00 / The line states no date of service...', svc null; same for a3, a4. Screenshot artifacts/review-evidence/T-205-paralegal/lib11-s3-01-a2.png (card head and source head read 'June 15, 2026'). After counting, the same line reads 'statement dated June 15, 2026' (p03.out:2, lib11-revisit-a2.png) and the letter prints '(statement dated June 15, 2026; service date not stated)' (ui-lib11-letter.txt:39). sdOf in app/frontend/guided/step3.js requires kind === 'charge', and an uncounted ledger line is kind unclear, so service_date is null (api.out lib11 a5 shows the same for unclear rows).\",\n   \"why_it_matters\": \"Those are the lines I am most careful with. Before I count them the card shows a bare June 15, 2026 in two places, which reads like a date of service, and it differs from what the letter will print. The body sentence says no date of service, so the risk is low, but the label I was asked to check is missing on this state. Never-counted UB-04 and ledger cards (lib10 a1/a6, lib11 a5-a8) show a bare record date too, though those carry no service-date claim.\",\n   \"fix\": \"Apply the same 'statement dated X' wording to the card head, source head and sub for any amount whose record is a bill document (ledger, invoice, UB-04, billing statement), whatever its kind, and show the letter's not-stated text as the Date of service line on a countable ledger line before it is counted.\",\n   \"acceptance_test\": \"E2E on lib11 a2 before counting: card head and src-head contain 'statement dated June 15, 2026', no bare 'June 15, 2026' without that prefix; the card shows '(statement dated June 15, 2026; service date not stated)' and it equals the text the letter prints after counting.\"},\n  {\"severity\": \"minor\", \"title\": \"The confirm note says to confirm the date but gives me nowhere to use it\",\n   \"evidence\": \"p02.out:2 (and 16 variants): note text ends 'The letter prints no service date for this line. Confirm the date from the highlighted words before you rely on it.' The card offers only 'Yes, count it' / 'No, don't count it' / 'Decide later'; screenshot note-lib10-ambiguous_numeric.png. The note does not say what to do once I have confirmed: add the date by hand in the Word letter, ask for the bill, or just count it.\",\n   \"why_it_matters\": \"Plain wording and placement are good, but the instruction is half of one: I confirm the date from the highlighted words, and then the tool cannot take it and the letter still prints none. I need one sentence of next step so I do not guess.\",\n   \"fix\": \"Append the next step to confirm_note, e.g. 'Counting the charge keeps it in the total; type the date into your letter yourself, or request the itemized bill.' Or tell me this tool cannot record a confirmed date.\",\n   \"acceptance_test\": \"Unit test on service_date.confirm_note for all 7 reasons: each ends with a sentence naming the next action (not just 'confirm'); E2E asserts the foot note shows it beside the quote.\"},\n  {\"severity\": \"nit\", \"title\": \"Two notes say 'the code' to a paralegal\",\n   \"evidence\": \"p02.out:3-4: 'The date 04/05/26 has a two-digit year, which the code does not guess.' and 'The date April 5 states no year, which the code does not borrow from the statement.' (app/backend/service_date.py _WHY).\",\n   \"why_it_matters\": \"I do not know which code is meant; 'the tool' or no subject reads the same and is clearer.\",\n   \"fix\": \"Reword: 'a two-digit year, which is not guessed' / 'no year, which is not taken from the statement date'.\",\n   \"acceptance_test\": \"Unit test: no confirm_note contains the word 'code'.\"}\n ],\n \"whats_right\": [\"Date of service on the Step 3 card is the letter's own text on case_09, lib10 and lib11 (period 'June 9–12, 2026' kept as a range), and the done-list column is now 'Date of service'.\",\n  \"'statement dated March 1, 2026' / 'June 19, 2026' is named as a statement date in the card head, the Date of service line and the source head; the ED visit date is left unlabeled, correctly.\",\n  \"The note sits in the card foot under the highlighted quote, is visible without scrolling, keeps Yes/No enabled, and states the letter will print no date.\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-03T00:36:38.400Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-205-paralegal.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:36:39.714Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-205-paralegal.md 2>&1 | tail -3"
}
````

### User / tool · 2026-11-03T00:36:39.849Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T00:36:41.808Z

T-205 passes (verdict pass; 2 minors, 1 nit): Step 3 shows the same service date the letter prints on case_09, lib10 and lib11, with "statement dated" labeled on charge cards, except on uncounted lib11 ledger lines, where a bare June 15, 2026 shows, and the confirm note, which I could only check by stubbing (the fixtures have no doubtful-date bill), tells you to confirm the date but not what to do next; my demo server (PID 63090) is stopped, and the review is at `/Users/arsis/zlayt-pm-project/reviews/T-205-paralegal.md`.
