# Subagent: T-114 paralegal re-check (T-114 paralegal re-check)

Source: `agent-ac309c84989003d6e.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T10:55:33.123Z

This is a round-2 re-check of board card T-114 in /Users/arsis/zlayt-pm-project. Read `python3 tools/board.py show T-114` and reviews/T-114-paralegal.md. The open major was that confirming a date which changes a gap must show a visible notice (gap_changes).

Run the app from a `git archive HEAD` copy in your scratchpad on a spare port: fixture backend, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad. Find a case where a date confirm changes a gap; lib09 may no longer change it after T-116. Confirm the date, and check that the notice is visible and clear and that it names the old and new numbers. Also confirm the round-1 minors.

Write reviews/T-114-paralegal-r2.md with a ```json block of real values: card, persona paralegal-reviewer, model claude-haiku-5-5, verdict, findings. Stop your server by PID. Reply in 2 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:34.963Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T10:55:34.973Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:35.253Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-114",
 "description": "Show board card T-114"
}
````

### User / tool · 2026-11-02T10:55:35.397Z

**tool result**
````
---
id: "T-114"
title: "Backend items from T-060 pass 1: rate rows must not offer an accept that later blocks export; demo has judge fixtures for every acceptable lib09 item; gap recompute after a date confirm is reported"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T09:21:16Z"
updated_at: "2026-11-02T10:55:22Z"
claimed_by: "backend"
claimed_at: "2026-11-02T09:39:42Z"
rounds: 1
commits: ["b5fb35c"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-114-paralegal.md", "at": "2026-11-02T09:39:42Z"}
ac:
  - {"n": 1, "text": "An amount classified rate is not accept-able into the letter (or accepting it needs no judge), so it can never create a JUDGE_NOT_RUN export block; every item a paralegal can accept on the demo library packets has its judge fixture (no demo dead end); confirm_date returns which gap figures changed (old->new) so the UI can say so; tests", "done": true, "evidence": "tests/unit/test_t114_rates_and_demo_judges.py: rate accepted without judge is not a JUDGE_NOT_RUN blocker (charge still is); accept_effect/judge_required_for_export on amounts; all 15 library packets walked in fixture mode with zero JUDGE_NOT_RUN (lib09 rate judge fixtures 7328ae58..., 75686283... recorded via claude-cli, 2 calls); confirm_date gap_changes lib09 42->40"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T09:21:17Z backend: claimed
- 2026-11-02T09:27:55Z backend: AC 1 checked: tests/unit/test_t114_rates_and_demo_judges.py: rate accepted without judge is not a JUDGE_NOT_RUN blocker (charge still is); accept_effect/judge_required_for_export on amounts; all 15 library packets walked in fixture mode with zero JUDGE_NOT_RUN (lib09 rate judge fixtures 7328ae58..., 75686283... recorded via claude-cli, 2 calls); confirm_date gap_changes lib09 42->40
- 2026-11-02T09:29:25Z backend: moved in_progress -> in_review
- 2026-11-02T09:29:33Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-02T09:39:42Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): changes — reviews/T-114-paralegal.md; round 1; findings:
    - [major] The lib09 gap change (42 to 40 days) is returned by the API, but HEAD's UI shows the new figure with no notice — fix: Frontend, under T-060: render gap_changes[].sentence beside the gap flag and in the flags tray after confirm_date. Whether an intake form should ever be a gap endpoint is a decision for Chris (questions_for_chris 1).
    - [minor] An accepted rate row still reads Needs review and keeps a primary Accept as noted button — fix: After acknowledge, the state chip reads something like Noted, not in letter, and the primary control becomes Undo or Reset. Keep the internal-notes sentence.
- 2026-11-02T09:39:42Z backend: claimed
- 2026-11-02T09:39:42Z orchestrator: Backend part confirmed by review. The remaining major (UI notice for gap_changes) is T-060 frontend work; re-check after T-060 lands. Note T-116 changed lib09: the intake form no longer ends the gap, so the 42->40 example may now read 42->42; use another case to test the notice.
- 2026-11-02T09:39:42Z orchestrator: assigned: backend
- 2026-11-02T10:55:22Z orchestrator: moved in_progress -> in_review
- 2026-11-02T10:55:22Z orchestrator: review dispatched: paralegal-reviewer

## Handoff
The gap_changes UI notice landed in T-060 r3 (c8e36fb/5d975ed); E2E in tests/e2e/test_polish_r3.py. Backend part already confirmed in round 1.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:35.438Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-114-paralegal.md"
}
````

### User / tool · 2026-11-02T10:55:35.445Z

**tool result**
````
1	# T-114 review: paralegal-reviewer (Maria Delgado persona)
2	
3	Verdict: **changes** (0 blockers, 1 major, 1 minor, 1 nit). The three asks hold on the running backend. The rate row is acknowledge-only, never blocks export, never reaches the total, and every acceptable item on all 15 library packets exports without JUDGE_NOT_RUN. confirm_date reports the lib09 gap as 42 to 40 days. What is still open is the part of T-060 F4 that is a UI job: the new figure appears with no notice in HEAD.
4	
5	## What I ran
6	
7	Deterministic first.
8	
9	- `git rev-parse HEAD` printed `b5fb35c743dced9cad3f3dc700e853dc42f4da8e`. I extracted `git archive HEAD` into `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive`.
10	- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest tests/unit/test_t114_rates_and_demo_judges.py -q -p no:cacheprovider` on that copy printed `20 passed in 7.82s`.
11	- Server from the copy: `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, `ZLAYT_DB` in my scratchpad, `HOST=127.0.0.1 PORT=7881`. Started twice (PID 32148, then PID 41378). Both stopped by PID. `curl` to 7881 returns 000 afterwards. The team app on 7860 was not touched (still 200).
12	
13	Live checks (scripts in `artifacts/review-evidence/`):
14	
15	- `T-114-paralegal-api-checks.py` (stdlib, run `.venv/bin/python -I`), output `T-114-paralegal-api-checks.out.json`, log `T-114-api-checks-run.log`. Covers the rate accept, the 15 packets in two date variants (dates confirmed to the first candidate; left unconfirmed), and confirm_date on lib09 record 4.
16	- `T-114-paralegal-gate-before.py`: lib09 gate before any accept shows `NOTHING_ACCEPTED` (status fail, blocking 1). That explains the "Export blocked by 1" the UI shows before any accept. After accepting only a3 the gate is `pass` with `blocking 0` and `judge_not_run 0`. Printed to terminal, not saved.
17	- `T-114-paralegal-ui-rates.py` (Playwright, Chromium, 1440x900): opened the lib09 case, accepted both rate rows, read the rows and the summary bar. Screenshots `T-114-ui-1-rates-before-accept.png` and `T-114-ui-2-rates-after-accept.png`; output `T-114-paralegal-ui-rates.out.json`.
18	- Code read at HEAD: `app/backend/trace.py:505, 792-801`; `app/backend/present.py:57-66`; `app/backend/review.py:330-363, 400-429`; `evals/library/case_lib09_spanish_interpreter_espalda.expected.json:219-222, 479-483`; `evals/golden/check_golden.py:250-260`.
19	- Grep at HEAD: `grep -rn gap_changes app/frontend/` returns nothing. `git show b5fb35c:app/frontend/timeline.js` has no `gap_changes`. The working tree does have a consumer at `app/frontend/timeline.js:50-56`, but it is uncommitted and not in b5fb35c. I did not review it.
20	
21	Results against the three asks:
22	
23	1. **lib09 rate row.** Accepting a3 and a6 returns 200 each, with `review_status` accepted, `accept_effect` acknowledge, `judge_required_for_export` false. Accepted total stays 0 cents. Gate after both rates: `ready` true, JUDGE_NOT_RUN list empty, export 200. After also accepting the two verified charges (a1 $2,940 and a4 $2,150), the letter total line is `Billed charges stated in these records: $5,090.00`. The two $400.00 rates appear only in `internal_notes_text`. In the UI the accepted row shows the chips "Needs review" and "Accepted", and the sentence "Noted for the internal notes only; not in the letter or the total." (see finding 2).
24	2. **Every acceptable item on the demo packets.** 15 packets x 2 variants = 30 exports. All 30 gates `ready`, JUDGE_NOT_RUN empty, no other blocker code, export 200. Accepted items: 271 per variant. Seven server refusals in total, all with plain messages and none a judge block: `CODE_CHECK_FAILED` on lib02 e4 and lib06 e5 (summary word not in the quote); `DATE_UNCONFIRMED` on lib14 e5 (both variants) and lib09 e4 (unconfirmed variant only).
25	3. **confirm_date gap_changes.** Confirming lib09 record 4 as 2026-03-05 returns `gap_changes` with one entry: `change` changed, `old_days` 42, `new_days` 40, `old_from` 2026-03-03, `new_from` 2026-03-05, both `to` 2026-04-14, and `sentence` "Gap recalculated after you confirmed record 4: now 40 days (was 42)." The flag id moves to `f_gap_r4_r2` with `record_nos` [2, 4].
26	
27	Not exercised: whether the UI offers Accept on the seven refused items; the blank-judge path on the live server (covered only by the unit test, which passed); the rest of the T-060 list.
28	
29	## Findings
30	
31	### Major: the 42 to 40 change is reported by the API only; HEAD's UI shows the new figure with no notice
32	
33	Evidence: `artifacts/review-evidence/T-114-paralegal-api-checks.out.json` (C_gap). `grep -rn gap_changes app/frontend/` on b5fb35c returns nothing. The uncommitted consumer in the working tree is not part of this card.
34	
35	Why it matters: T-060 F4 asked that a figure that changes after a decision say so. The backend AC is met, and the handoff says the frontend note stays on T-060. In the build as committed, a paralegal who confirms record 4 sees "Gap of 40 days" with no reason, ending at an intake form. The adjuster counts days between treatment encounters, and she needs to know why the number moved.
36	
37	Fix: frontend (under T-060): render `gap_changes[].sentence` beside the gap flag and in the flags tray after confirm_date. The open question of whether an intake form should ever be an endpoint is in questions_for_chris.
38	
39	Acceptance test: Playwright on lib09 after the frontend commit: confirm record 4 as 2026-03-05. The gap flag card shows "Gap recalculated after you confirmed record 4: now 40 days (was 42)." and names the 2026-03-05 start.
40	
41	### Minor: an accepted rate row still reads "Needs review" and keeps a primary "Accept as noted" button
42	
43	Evidence: `artifacts/review-evidence/T-114-ui-2-rates-after-accept.png` (the $400.00 Rate rows show chips "Needs review" and "Accepted"; primary button "Accept as noted"). `T-114-paralegal-ui-rates.out.json` after_rates.a3: `data_review` accepted, `data_state` needs_review.
44	
45	Why it matters: the money side is right; the rate is out of the total and does not block export. But an accepted row that still says "Needs review" and invites a second Accept looks unfinished, the same pattern as T-060 F6 and F7. The code says "acknowledge", the row says "Accepted", the sentence says "Noted". Pick one.
46	
47	Fix: after acknowledge, the state chip reads something like "Noted, not in letter" and the primary control becomes Undo or Reset. Keep the internal-notes sentence.
48	
49	Acceptance test: lib09 after accepting a3: the row has no "Needs review" chip and its primary control is not "Accept as noted".
50	
51	### Nit: the lib01 extract step misses its demo fixture on every run; the case still reaches ready and no record is dropped
52	
53	Evidence: scratch DB on the first server, `SELECT ... FROM llm_calls WHERE error LIKE 'FIXTURE_MISS%'` returns 4 rows: step extract, attempt 1, parsed_ok 0, error "FIXTURE_MISS 83bcee077841...", all on cases named "case lib01 er only then gap" (status ready). The lib01 case stored 6 records and 6 entries. `grep -c "^=== Record" evals/library/case_lib01_er_only_then_gap.txt` returns 6. I did not trace which path produced the lib01 extraction.
54	
55	Why it matters: nothing is lost here, but the demo leans on a logged miss for lib01, which is the kind of demo dead end T-114 set out to close.
56	
57	Fix: record the lib01 extract response in `tests/fixtures/llm/` (curated set), or note the fallback on the card.
58	
59	Acceptance test: a fixture-mode walk of the 15 packets writes zero FIXTURE_MISS rows to llm_calls.
60	
61	## Right already
62	
63	- Accepting a rate is acknowledge-only at every layer I checked. The API says so (`accept_effect` acknowledge, `judge_required_for_export` false). The gate agrees. The letter total excludes it. The UI says it is in the internal notes only.
64	- Every acceptable item on the 15 demo packets exports with no JUDGE_NOT_RUN, in both date variants, and every refusal names the next step.
65	- The confirm_date response carries old and new endpoints, old and new days, and a plain sentence. The backend side of gap_changes is complete.
66	
67	```json
68	{"card": "T-114", "persona": "paralegal-reviewer", "model": "claude-haiku-5-5",
69	 "scope": "git archive HEAD = b5fb35c, extracted to /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; app http://127.0.0.1:7881 (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch DB, stopped by PID); sample case: library case_lib09_spanish_interpreter_espalda plus all 15 library packets in two date variants",
70	 "exercised": [
71	  "git rev-parse HEAD and git cat-file -t b5fb35c (board show T-114 handoff read)",
72	  "pytest tests/unit/test_t114_rates_and_demo_judges.py on the archive copy: 20 passed in 7.82s",
73	  "API: lib09 accept a3 and a6 (200, acknowledge, total 0 cents), gate after rates (ready, no JUDGE_NOT_RUN), export letter total with a1 and a4 accepted ($5,090.00), internal notes with the rate lines",
74	  "API: all 15 library packets, two variants (dates confirmed, dates unconfirmed): 30 gates ready, 0 JUDGE_NOT_RUN, 30 exports 200, 7 plain 422 refusals recorded",
75	  "API: lib09 confirm_date r4 to 2026-03-05: gap_changes 42 to 40 with sentence; gap flag endpoints before and after; records encounter and date_status",
76	  "Playwright on lib09 (1440x900): accepted both rate rows in the UI; read the row text and the summary bar; two screenshots",
77	  "Gate before and after one rate accept (NOTHING_ACCEPTED explains the pre-accept 'Export blocked by 1')",
78	  "Scratch DB llm_calls query for FIXTURE_MISS rows; lib01 record count versus packet headers",
79	  "Read app/backend/trace.py, present.py, review.py, evals/golden/check_golden.py, the lib09 expected.json; grep for gap_changes in HEAD frontend (none)"
80	 ],
81	 "verdict": "changes",
82	 "scores": {"verify_quickly": 3, "rate_row_clarity": 3, "export_jnr_free_demo_packets": 5, "rate_never_in_total": 5, "gap_change_reported_by_api": 5, "gap_change_visible_in_head_ui": 1},
83	 "findings": [
84	  {"severity": "major", "title": "The lib09 gap change (42 to 40 days) is returned by the API, but HEAD's UI shows the new figure with no notice",
85	   "evidence": "artifacts/review-evidence/T-114-paralegal-api-checks.out.json C_gap.gap_changes[0].sentence = Gap recalculated after you confirmed record 4: now 40 days (was 42).; C_gap.after = f_gap_r4_r2, days 40, from 2026-03-05, record_nos [2,4]. grep -rn gap_changes app/frontend/ on b5fb35c returns nothing. Working-tree consumer app/frontend/timeline.js:50-56 is uncommitted and not in b5fb35c (not reviewed).",
86	   "why_it_matters": "T-060 F4 asked that a figure which changes after a decision say so. The backend AC is met, but in the committed build a paralegal who confirms record 4 sees Gap of 40 days with no reason, ending at an intake form. The adjuster counts days between treatment encounters and needs to see why the figure moved.",
87	   "fix": "Frontend, under T-060: render gap_changes[].sentence beside the gap flag and in the flags tray after confirm_date. Whether an intake form should ever be a gap endpoint is a decision for Chris (questions_for_chris 1).",
88	   "acceptance_test": "Playwright on lib09 after the frontend commit: confirm record 4 as 2026-03-05; the gap flag card shows Gap recalculated after you confirmed record 4: now 40 days (was 42). and names 2026-03-05 as the start."},
89	  {"severity": "minor", "title": "An accepted rate row still reads Needs review and keeps a primary Accept as noted button",
90	   "evidence": "artifacts/review-evidence/T-114-ui-2-rates-after-accept.png (chips Needs review and Accepted; primary button Accept as noted; text Noted for the internal notes only; not in the letter or the total.). artifacts/review-evidence/T-114-paralegal-ui-rates.out.json after_rates.a3: data_review accepted, data_state needs_review. app/backend/present.py:57-66 (accept_effect acknowledge).",
91	   "why_it_matters": "The money side is right: the rate is out of the total and does not block export. An accepted row that still says Needs review and invites a second Accept looks unfinished (T-060 F6/F7 pattern). The code says acknowledge, the chip says Accepted, the sentence says Noted.",
92	   "fix": "After acknowledge, the state chip reads something like Noted, not in letter, and the primary control becomes Undo or Reset. Keep the internal-notes sentence.",
93	   "acceptance_test": "lib09 after accepting a3: the row has no Needs review chip and its primary control is not Accept as noted."},
94	  {"severity": "nit", "title": "The lib01 extract step misses its demo fixture on every run; the case still reaches ready and no record is dropped",
95	   "evidence": "Scratch DB (first server) query on llm_calls WHERE error LIKE FIXTURE_MISS%: 4 rows, step extract, attempt 1, parsed_ok 0, error FIXTURE_MISS 83bcee077841..., all on case lib01 er only then gap (status ready). Stored 6 records and 6 entries; grep -c ^=== Record evals/library/case_lib01_er_only_then_gap.txt returns 6.",
96	   "why_it_matters": "Nothing is lost, but the lib01 demo depends on a logged fixture miss, the kind of demo dead end T-114 set out to close. I did not trace which path produced the lib01 extraction.",
97	   "fix": "Record the lib01 extract response in tests/fixtures/llm (curated set), or note the fallback on the card.",
98	   "acceptance_test": "Fixture-mode walk of the 15 packets writes zero FIXTURE_MISS rows to llm_calls."}
99	 ],
100	 "whats_right": [
101	  "Accepting a rate is acknowledge-only at every layer checked: API accept_effect acknowledge with judge_required_for_export false, gate agrees, letter total excludes it, UI says it is in the internal notes only.",
102	  "All 15 library packets export with no JUDGE_NOT_RUN in both date variants (30 of 30 gates ready), and every refusal names the next step.",
103	  "confirm_date returns old and new endpoints, old and new days, and a plain sentence; the backend side of gap_changes is complete."
104	 ],
105	 "questions_for_chris": [
106	  "Should a dated admission or intake form ever be a gap endpoint? evals/library/case_lib09_spanish_interpreter_espalda.expected.json records entry 4 has kind encounter with date null, and must_not_flag N1 excludes it only as an ambiguous-date intake. Once confirmed, the product counts it (encounter true), so the lib09 figure goes 42 to 40. T-060 F4 says an intake form must never be an endpoint. This changes the number the adjuster sees, so it needs a decision. Whether the gap goes in the demand is litigation-lead's call, outside my lens.",
107	  "A rate whose second check disagrees (for example SHOULD_BE_CHARGE) still gets acknowledge-only treatment: acknowledge_only() is kind-based (app/backend/trace.py:792-795) and does not read the judge verdict. Should a disagreeing check on a rate force a decision before Accept?",
108	  "Seven refusals on the demo packets (lib02 e4 and lib06 e5 CODE_CHECK_FAILED; lib14 e5 and lib09 e4 DATE_UNCONFIRMED in one variant). The server messages name the next step. I did not check whether the UI offers Accept on them. Does the T-060 F3 rule (offer only what can be accepted) cover them?"
109	 ]}
110	```
111	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:35.680Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t114-rates-gap-patterns.md"
}
````

### User / tool · 2026-11-02T10:55:35.689Z

**tool result**
````
1	---
2	name: t114-rates-gap-patterns
3	description: T-114 (b5fb35c) review: rate acknowledge-only and demo-packet JNR walk pass; gap change is API-only in HEAD; intake-form encounter classification is a Chris decision; UI leaves accepted rate rows showing Needs review
4	metadata:
5	  type: project
6	---
7	
8	T-114 (commit b5fb35c, reviewed 2026-11-02, verdict changes: 1 major, 1 minor, 1 nit) fixed the T-060 F3 rate dead end and the F4 "say so" half at the API level.
9	
10	- Accepting a lib09 rate is `accept_effect` acknowledge and `judge_required_for_export` false (present.py:57-66, trace.py:792-795). It never adds to the total and never blocks export. The UI row still shows chip "Needs review" after accept (screenshot T-114-ui-2-rates-after-accept.png).
11	- All 15 library packets exported with zero JUDGE_NOT_RUN in both date variants. Refusals are plain 422s: CODE_CHECK_FAILED (lib02 e4, lib06 e5) and DATE_UNCONFIRMED (lib14 e5, lib09 e4 unconfirmed).
12	- confirm_date record 4 gives gap_changes 42 to 40. No frontend in HEAD reads gap_changes. The only consumer is uncommitted in the working tree (timeline.js:50-56), so I reviewed HEAD only.
13	
14	**Why:** the lib09 golden classifies record 4 (formulario de admisión) as kind "encounter" with date null. N1 excludes it only as an "ambiguous-date intake". Once the date is confirmed it is an endpoint by the golden's own classification. So the 40-day figure is consistent with the golden, and the real question is whether intake forms are encounters. That is Chris's call, not a reviewer's. Also: evals/golden/check_golden.py:259 computes exclusions from kind and ambiguity at ingest only, so no gate checks the post-confirm state.
15	
16	**How to apply:** when a T-060-style "intake must never be an endpoint" finding comes up, check the golden kind first. Do not call it a must_not_flag violation; the N1 text is scoped to ambiguous dates. The T-060 pass-1 findings are in reviews/T-060-paralegal-pass1.md (F3, F4 are the rate and gap items). Related: [[golden-set-recurring-findings]].
17	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:39.432Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git log --oneline -12 && git cat-file -t c8e36fb 2>&1; git cat-file -t 5d975ed 2>&1; git merge-base --is-ancestor c8e36fb HEAD && echo \"c8e36fb in HEAD\"; git merge-base --is-ancestor 5d975ed HEAD && echo \"5d975ed in HEAD\"; git status --short | head -30; ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/",
 "description": "Check HEAD, recent log, and T-060 commits ancestry"
}
````

### User / tool · 2026-11-02T10:55:39.695Z

**tool result**
````
e1ce8dc620e6ec0778320456ac79a25f1832bfee
e1ce8dc fix(backend): a never-judged LLM_ONLY tray item carries its real reason, not JUDGE_UNAVAILABLE (T-122; case_05 f_r1_1 judge_unavailable 1 -> 0)
7d5a45f fix(frontend): refusal, edit box and blocked notice span the full row inside the compact grid (T-060 r3)
f8f358e fix(backend): T-116 r5 paperwork warning is header-only; text evidence never suppresses it (D-055)
1b93582 fix(backend): D-054 trims only salient new content; split-off and tray-trace fixes (T-112 r2)
d9efc5c test(e2e): T-060 round 3 - shortcut sheet, row-only key rule (negative), Tab/Enter/Space-only review and export, compact rows, decided rows, 320 px reflow, theme-toggle name, held rechecks (T-060 r3, T-119)
5d975ed feat(frontend): compact review rows, one checks card, batch button in the Timeline toolbar, Start review, compact charges rows with cents, letter box sized to its text and Download .txt (T-060 r3)
c8e36fb fix(frontend): shortcut sheet prints its keys; theme toggle name follows state; skip-link targets exist; Tab start reset after a case opens; decided rows show Accepted/Dismissed and Undo; tray items named with a record cue in the AI-check panel (T-060 r3, T-117)
8b4ff11 fix(backend): every dated record reaches gap math; paperwork-looking records warn with both numbers (T-116 r4, D-055)
af5621b test(backend): T-113 controls from a clean worktree of b66e748: J3 16/16 and J4 12/12 caught, 0 false agrees (controls-20261102T102626Z)
b66e748 fix(backend): T-113 conflict candidates drop other-person and paperwork pairs, model-proposed conflicts and scene_facts go to the tray (D-053), judge_conflict_v6, controls updated before the run (D-046)
b0a2b51 docs: D-056 judge answers are never scripted (amends D-029)
158809b memory: §7.4 debt rows; revert lib11 expected to pre-T-118 (D-055 makes record 6 a gap endpoint again)
commit
commit
c8e36fb in HEAD
5d975ed in HEAD
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
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/pipeline.py
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-060.md
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
t060-ui-polish-patterns.md
t068-dates-to-confirm-patterns.md
t079-library-v2-patterns.md
t114-rates-gap-patterns.md
t116-gap-endpoint-patterns.md
t118-lib11-truth-patterns.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:39.718Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/reviewer-api-shape-gotchas.md"
}
````

### User / tool · 2026-11-02T10:55:39.734Z

**tool result**
````
1	---
2	name: reviewer-api-shape-gotchas
3	description: Zlayt app response shapes that trip review scripts (item GET nests under "item", case status "ready", record warnings live in case.flags, audit before/after only in local mode)
4	metadata:
5	  type: reference
6	---
7	
8	- `GET /api/cases/{t}/items/{id}` returns `{item, source, calls, events}`. Read the item from `["item"]`. A `.get("reasons")` on the top level returns None and makes "no DATE_AMBIGUOUS" checks pass vacuously.
9	- Case status terminal success is `"ready"` (not "done"); `"done_with_errors"` is the other OK terminal.
10	- Record warnings are not a top-level `record_warning_flags` key. They are in `case.flags` with `type == "record_warning"` (e.g. `f_date_r8` before a date confirm).
11	- `GET audit` events carry `before`/`after` only with `ZLAYT_MODE=local`. Outside local mode they have only id, item_id, action, at.
12	- Accept/Edit/Change quote controls: `data-testid` btn-accept (has aria-pressed), btn-edit; entry rows are `[data-entry-id="<id>"]`, state chip `entry-state`, reason line `entry-reasons` (only when needs_review).
13	- Dates-to-confirm picker: `form[data-testid="confirm-date"]` with radio labels like "April 5, 2026 (2026-04-05)" and `btn-confirm-date`.
14	
15	**Why:** found while writing T-076 r2 checks (2026-11-01). Two checks passed only because the key was missing, and the status check failed on "ready" until corrected.
16	
17	**How to apply:** before writing a check that reads a field, print the response keys once. Each check should assert the key is present (non-vacuous) before testing its value. Related: [[d041-date-gate-patterns]], [[reviewer-tooling-quirks]].
18	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:39.986Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md"
}
````

### User / tool · 2026-11-02T10:55:39.994Z

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
30	## T-116 r2 additions (2026-11-02)
31	- `reviewer-write-guard` also refuses Write to the session scratchpad ("reviewers write only under reviews/ or artifacts/review-evidence/").
32	  Put probe copies, extracted archives and JSON checkers under artifacts/review-evidence/ (run with `.venv/bin/python -I`). `git archive`
33	  extraction into the scratchpad via Bash worked.
34	- The review file was refused a second write once it existed, so a wrong body sentence (I wrote "a scratchpad archive path that no longer
35	  exists" without checking it, and mislabeled a record) could not be fixed. Before the single Write: `ls` every path and grep every record
36	  label you quote.
37	- `bash python3 -c "... \`\`\` ..."` was denied again by git-guard. The JSON check now lives in artifacts/review-evidence/<card>-paralegal-r2-jsoncheck.py.
38	
39	## T-116 r3 additions (2026-11-02)
40	- The r3 review was written once and then contained one wrong claim (a grep "returns 1 from the H3V5 line only" that was actually the line-29
41	  orchestrator note). Edit on the existing review was refused by `reviewer-write-guard`, so the erratum went into the final reply instead.
42	  Rule: before the single Write, run the exact grep again and quote its line numbers; do not describe a match you have not printed.
43	- `python3 -c` with `\`\`\`json` in the string was denied by git-guard again (parse error). The JSON check is `artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py`
44	  run with `.venv/bin/python -I <script> <review>`; it works for any review path.
45	- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider` keeps the dirty project tree free of new .pytest_cache and .pyc writes.
46	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:40.189Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t060-ui-polish-patterns.md"
}
````

### User / tool · 2026-11-02T10:55:40.197Z

**tool result**
````
1	---
2	name: t060-ui-polish-patterns
3	description: T-060 pass 2 (b89b9d9): what to re-check on the review UI (keyboard queue, density, export box, F13 false positive); review-file slips to avoid
4	metadata:
5	  type: feedback
6	---
7	
8	Pass 1 majors (keyboard across panels, needs-review first, accept-blocks-export, gap 42 to 40, tall charge rows) were fixed or reduced by 3e3f3b7/eabe2b8/9fcae9b. Still open at b89b9d9: summary+Source letter lines with "AI translation:" prefix, interpreter-sentence prior-condition flag (lib09), 133 px charge rows, accepted rows keep blue Accept, mouse batch button skips the confirm Shift+A shows, `o` modal swallows `a`, no download.
9	
10	**Why:** pass 2 used a fixed script set (q0-q13 under artifacts/review-evidence/T-060-pass2/); reuse them for a pass 3.
11	
12	**How to apply:** after a library load by mouse, Tab starts at the page bottom (sequential focus start is the clicked button); start keyboard runs from the "N date to confirm" chip. The server's first Tab/`j` from a radio is ignored (typing guard).
13	
14	**Review-file slip to avoid:** the file is append-only. Before the single Write, count severities with the jsoncheck script (I wrote "9 minors" in prose, JSON had 11) and recount list items you describe ("5 panels" listed 6). Do not cite pass-1 numbers you did not measure. Related: [[reviewer-tooling-quirks]], [[frontend-review-patterns]].
15	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:45.367Z

**tool call — Bash**
````
{
 "command": "git show --stat e1ce8dc | head -5; git grep -n \"gap_changes\" HEAD -- app/frontend | head; echo ---; grep -n -i -E \"uvicorn|PORT|HOST|python|start|fixture|ZLAYT_MODE|ZLAYT_DB\" docs/RUNBOOK.md | head -40; echo ---; ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad 2>&1 | head; echo ---; curl -s -o /dev/null -w \"%{http_code}\\n\" http://localhost:7860/ ; lsof -iTCP -sTCP:LISTEN -nP 2>/dev/null | grep -E \"78[0-9][0-9]\" | head",
 "description": "Inspect HEAD commit, frontend gap_changes, runbook start commands, and ports"
}
````

### User / tool · 2026-11-02T10:55:45.632Z

**tool result**
````
commit e1ce8dc620e6ec0778320456ac79a25f1832bfee
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 04:51:14 2026 -0600

    fix(backend): a never-judged LLM_ONLY tray item carries its real reason, not JUDGE_UNAVAILABLE (T-122; case_05 f_r1_1 judge_unavailable 1 -> 0)
HEAD:app/frontend/timeline.js:70:  // ---- confirm a date reading (used by Dates to confirm, the flag card's date form and the pre-selected form). T-114: the backend answers with gap_changes[]; every
HEAD:app/frontend/timeline.js:76:    const changes = (resp && Array.isArray(resp.gap_changes) ? resp.gap_changes : []).map((g) => g && g.sentence).filter(Boolean);
---
7:| Board (local) | http://localhost:7777 | also in the Desktop Browser pane (`.claude/launch.json` → "board") |
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
9:| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |
11:Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
12:We restored those and gave the board and app their own ports so nothing of yours was clobbered.
24:## Restart (after a crash, reboot, or closing the session)
26:2. Board server: `./tools/serve_board.sh` (also installs the native git pre-commit secret scan if missing) (tmux session `zlayt`, window `board`). Check: `curl -s localhost:7777/healthz`.
31:   > Re-read CLAUDE.md, memory/STATE.md and `python3 tools/board.py status`. Re-spawn the worker agents (general-purpose subagents whose first step is `python3 tools/agent_prompt.py <role>` unless native agent types are available), recreate the heartbeat cron (text in memory/STATE.md), continue the loop.
32:5. Tailnet exposure persists across restarts (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.
36:python3 tools/board.py status          # where are we
37:python3 tools/board.py list --status in_review
39:.venv/bin/python -m pytest tools/tests -q   # harness tests
---
641ed.bak
M1
M1_nocombine
M2
M2_find0
M3
M4
T-047-run1.json
T-060-pass2-head
T-093-r3-2ab7896
---
200
qemu-syst 23935 arsis   54u  IPv4 0x77863d93745b0252      0t0  TCP 127.0.0.1:49773 (LISTEN)
Python    49599 arsis    9u  IPv4   0x2927837656a6aa      0t0  TCP 127.0.0.1:7895 (LISTEN)
Python    83954 arsis    9u  IPv4 0xe15a7c6871390c24      0t0  TCP 127.0.0.1:7860 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:47.199Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh; echo ---; git show HEAD:tools/serve_app.sh | head -60 | diff - tools/serve_app.sh && echo same-as-head",
 "description": "Read the app launch script"
}
````

### User / tool · 2026-11-02T10:55:47.300Z

**tool result**
````
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
---
same-as-head
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:48.738Z

**tool call — Bash**
````
{
 "command": "grep -n -E \"environ|getenv|port|PORT|HOST\" app/main.py | head -20; grep -rn \"ZLAYT_MODE\" app/*.py app/backend/*.py | head -5",
 "description": "Find port and mode env handling in app entrypoint"
}
````

### User / tool · 2026-11-02T10:55:48.840Z

**tool result**
````
2:import os
4:import uvicorn
6:from app.backend.api import create_app
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
app/backend/api.py:80:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:108:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
app/backend/api.py:548:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
app/backend/api.py:582:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
app/backend/dismissal_patterns.py:5:ZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:49.775Z

Now I'll extract HEAD (e1ce8dc, which includes the T-060 r3 frontend commits) into the scratchpad and start the server on a spare port.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:51.257Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/t114r2/archive\" && cd /Users/arsis/zlayt-pm-project && git archive HEAD | tar -x -C \"$S/t114r2/archive\" && ls \"$S/t114r2/archive\" | head -30 && ls \"$S/t114r2/archive/app/frontend\" | head -30",
 "description": "Extract git archive of HEAD into scratchpad"
}
````

### User / tool · 2026-11-02T10:55:51.857Z

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
judges.js
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
narrative.js
review.css
review.js
sidebyside.css
sidebyside.js
source.js
state.js
stepper.css
stepper.js
styles.css
suggestions.css
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:54.266Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t114r2/archive\" && grep -rln \"gap_changes\" app/frontend app/backend | head; echo ---; ls evals/library | head -40",
 "description": "Confirm gap_changes consumer in archive and list library packets"
}
````

### User / tool · 2026-11-02T10:55:54.366Z

**tool result**
````
app/frontend/timeline.js
app/backend/review.py
---
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:55:59.861Z

**tool call — Bash**
````
{
 "command": "lsof -iTCP:7881 -sTCP:LISTEN -nP 2>/dev/null | head -2; echo \"port-check-done\"; ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/archive/tests/fixtures/llm 2>&1 | head -3",
 "description": "Check spare port 7881 is free and fixtures exist"
}
````

### User / tool · 2026-11-02T10:56:00.037Z

**tool result**
````
port-check-done
00335ec113c1f7234011ea2005f91965f2cc9dcf64aa50c61a8a35672c2b4cf3.json
003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
00c97f20c9cf54c24c8b3275a7382a44877f7bd89ccb0a419716cb030e564104.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:04.785Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/archive && PYTHONDONTWRITEBYTECODE=1 LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local HOST=127.0.0.1 PORT=7881 ZLAYT_DB=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/app.sqlite3 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/server.log 2>&1 &\necho \"started pid=$!\"; sleep 3; curl -s -o /dev/null -w \"7881 http %{http_code}\\n\" http://127.0.0.1:7881/",
 "description": "Start HEAD app copy on port 7881 with fixture backend"
}
````

### User / tool · 2026-11-02T10:56:07.911Z

**tool result**
````
started pid=51899
7881 http 200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:09.230Z

The server is up on PID 51899. Next I need the API routes for loading a library case and confirming a date.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:10.698Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/archive && grep -n -E \"@app\\.(get|post|put|patch|delete)|\\\"/api\" app/backend/api.py | head -60; echo ---; grep -n -i \"library\" app/backend/api.py | head -20",
 "description": "List API routes and library load endpoints"
}
````

### User / tool · 2026-11-02T10:56:10.805Z

**tool result**
````
171:        if request.url.path.startswith("/api") and time.time() - purged["at"] > 60:     # expired cases vanish even with no create
189:        resp.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api") else resp.headers.get("Cache-Control", "no-cache")
212:    @app.get("/api/health")
218:    @app.get("/api/cases")
228:    @app.get("/api/library")
234:    @app.post("/api/cases", status_code=201)
250:    @app.post("/api/cases/pdf", status_code=201)
316:    @app.get("/api/cases/{token}")
325:    @app.delete("/api/cases/{token}", status_code=204)
349:    @app.post("/api/cases/{token}/run", status_code=202)
372:    @app.post("/api/cases/{token}/rejudge")
394:    @app.get("/api/cases/{token}/status")
413:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
425:    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
436:    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
449:    @app.get("/api/cases/{token}/narrative")
458:    @app.post("/api/cases/{token}/narrative")
471:    @app.post("/api/cases/{token}/narrative/review")
486:    @app.get("/api/cases/{token}/items/{item_id}")
498:    @app.post("/api/cases/{token}/items/{item_id}/review")
519:    @app.get("/api/cases/{token}/export")
546:    @app.get("/api/cases/{token}/items/{item_id}/trace")
559:    @app.get("/api/cases/{token}/trace")
568:    @app.get("/api/cases/{token}/judges")
577:    @app.get("/api/cases/{token}/audit")
---
32:LIBRARY = ROOT / "evals" / "library"
62:def library_cases() -> list:
63:    """Synthetic case library (evals/library, same file format as evals/golden: <id>.txt + optional <id>.expected.json). Falls back to
64:    evals/golden until the library exists. [{id, name, description, path}]"""
65:    base = LIBRARY if any(LIBRARY.glob("*.txt")) else GOLDEN
101:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
228:    @app.get("/api/library")
229:    def library():
232:        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}
239:        if isinstance(b.get("library"), str):
242:            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
244:                raise ApiError(404, "not_found", "No such library case.")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:13.173Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/archive && sed -n 234,250p app/backend/api.py; sed -n 316,324p app/backend/api.py; sed -n 394,435p app/backend/api.py; echo ---; grep -n \"gap_changes\" -A12 app/backend/review.py | head -60",
 "description": "Read case create, status, confirm_date and gap_changes code"
}
````

### User / tool · 2026-11-02T10:56:13.285Z

**tool result**
````
    @app.post("/api/cases", status_code=201)
    async def create_case(request: Request):
        b = await body_of(request)
        sample = b.get("sample") is True
        lib = None
        if isinstance(b.get("library"), str):
            if not local_mode():
                raise ApiError(404, "not_found", "Not found.")
            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
            if lib is None:
                raise ApiError(404, "not_found", "No such library case.")
        text = (GOLDEN / "sample.txt").read_text() if sample else (lib["path"].read_text() if lib else b.get("text"))
        if not isinstance(text, str):
            raise ApiError(400, "bad_request", "Provide text or sample: true.")
        return make_case(text, b.get("name") if isinstance(b.get("name"), str) else (lib["name"] if lib else None), sample)

    @app.post("/api/cases/pdf", status_code=201)
    @app.get("/api/cases/{token}")
    def get_case_view(token: str):
        c = conn()
        try:
            get_case(c, token)
            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
        finally:
            c.close()

    @app.get("/api/cases/{token}/status")
    def status(token: str):
        c = conn()
        try:
            case = get_case(c, token)
            stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
            stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
            stages = list(stages) if not callable(stages) else STAGES
            done = stages.index(stage) if stage in stages else 0
            end = case["run_finished_at"] or time.time()
            return {"token": token, "status": case["status"], "stage": stage, "stages": stages,
                    "progress": {"done": done, "total": len(stages), "label": f"Step {done + 1} of {len(stages)}: {stage}" if stage else ""},
                    "counts": {"entries": len(DB.list_items(c, token, "entry")), "amounts": len(DB.list_items(c, token, "amount")),
                               "flags": len(DB.list_items(c, token, "flag"))},
                    "error": json.loads(case["error"]) if case["error"] else None,
                    "elapsed_ms": int((end - case["run_started_at"]) * 1000) if case["run_started_at"] else 0}
        finally:
            c.close()

    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
    async def confirm_date(token: str, rid: str, request: Request):
        b = await body_of(request)
        if not isinstance(b.get("date"), str):
            raise ApiError(400, "bad_request", "Provide the chosen date.")
        c = conn()
        try:
            get_case(c, token)
            return review.confirm_date(c, token, rid, b["date"])
        finally:
            c.close()

    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
    async def manual_entry(token: str, rid: str, request: Request):
        """D-031: the reviewer writes the entry for a record the AI could not make one for. Quote = whole verbatim sentences (422 otherwise)."""
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            return review.manual_entry(c, token, rid, b, call=make_call(c, token))
        finally:
            c.close()

---
353:    gap_changes = []
354:    removed += _recompute_gaps(conn, case_id, t, gap_changes)
355:    for ch in gap_changes:
356-        ch["sentence"] = _gap_change_sentence(ch, rec["seq"])
357-    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
358-    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t)
359-    enforce_ocr(conn, case_id, t)
360-    from app.backend import present
361-    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
362-            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
363:            "removed_flag_ids": removed, "gap_changes": gap_changes,
364-            "dates_to_confirm": present.dates_to_confirm(conn, case_id), "warnings": []}
365-
366-
367-def _without_date_doubt(item: dict) -> dict:
368-    """The date was confirmed: drop DATE_AMBIGUOUS from the item's reasons and recompute its state. Other doubts (judge, injection...)
369-    stay, so the item is `verified` only when the date was the only reason it was `needs_review`. Rejected items stay rejected."""
370-    reasons = [c for c in (item.get("state_reasons") or []) if c != "DATE_AMBIGUOUS"]
371-    if (item.get("ladder") or {}).get("translation") is not None and "AI_TRANSLATION" not in reasons:      # D-050: confirming a date never verifies a translation
372-        reasons.append("AI_TRANSLATION")
373-    state = item["state"]
374-    if state == "needs_review" and not reasons:
375-        state = "verified"
--
400:def _gap_changes(old: dict, new: dict) -> list:
401-    """Which gap figures a recompute changed (T-114). `old`/`new` map flag id -> _gap_figures. A gap whose id survives and whose figures moved is `changed`; an
402-    old gap that vanished and a new one that shares a record number with it are ONE `changed` entry (an endpoint moved); the rest are `removed` / `added`.
403-    Each: {flag_id, change, old_days, new_days, old_from, old_to, new_from, new_to}; the side that does not exist is null. Code over the figures, never a model."""
404-    rows = []
405-    fresh = [n for i, n in new.items() if i not in old]
406-    for i, n in new.items():
407-        o = old.get(i)
408-        if o is not None and any(o[k] != n[k] for k in ("from", "to", "days")):
409-            rows.append(("changed", o, n))
410-    for i, o in old.items():
411-        if i in new:
412-            continue
--
471:        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
472-    return removed
473-
474-
475-# ---------------------------------------------------------------- manual entry (D-031, T-056)
476-def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
477-    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
478-    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
479-    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
480-    t = _now(now)
481-    case = DB.get_case(conn, case_id)
482-    recs = store.load_records(conn, case_id, case["raw_text"])
483-    rec = next((r for r in recs if r["id"] == record_id), None)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:16.693Z

Round 1 used Playwright scripts under `artifacts/review-evidence/`. I'll reuse that pattern, so I'm reading the existing UI script first.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:17.151Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/ | grep -i \"T-114\" ; echo ---; sed -n 1,60p artifacts/review-evidence/T-114-paralegal-ui-rates.py",
 "description": "List round-1 T-114 evidence and read UI script header"
}
````

### User / tool · 2026-11-02T10:56:17.274Z

**tool result**
````
T-114-api-checks-run.log
T-114-paralegal-api-checks.out.json
T-114-paralegal-api-checks.py
T-114-paralegal-gate-before.py
T-114-paralegal-jsoncheck.py
T-114-paralegal-ui-rates.out.json
T-114-paralegal-ui-rates.py
T-114-ui-1-rates-before-accept.png
T-114-ui-2-rates-after-accept.png
---
"""T-114 paralegal-reviewer UI check: accept the two lib09 rate rows in the browser on the scratch server (b5fb35c archive, :7881).
Records what the paralegal sees on the rate row and the summary bar after accept, and whether Export stays open.
Run: .venv/bin/python artifacts/review-evidence/T-114-paralegal-ui-rates.py [base_url]
Writes T-114-ui-*.png and T-114-paralegal-ui-rates.out.json next to this file.
"""
import json
import os
import re
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:7881"
HERE = os.path.dirname(os.path.abspath(__file__))
LIB09 = "case_lib09_spanish_interpreter_espalda"


def api(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method, headers={"content-type": "application/json"})
    with urllib.request.urlopen(r, timeout=120) as x:
        return json.loads(x.read() or b"null")


tok = api("POST", "/api/cases", {"library": LIB09})["token"]
api("POST", f"/api/cases/{tok}/run", {})
for _ in range(480):
    if api("GET", f"/api/cases/{tok}/status")["status"] in ("ready", "failed", "done_with_errors"):
        break
    time.sleep(0.25)

out = {"token_prefix": tok[:6], "steps": []}


def row_state(page, item_id):
    row = page.locator(f'tr[data-item-id="{item_id}"]')
    return {"data_review": row.get_attribute("data-review"), "data_state": row.get_attribute("data-state"),
            "row_text": re.sub(r"\s+", " ", row.inner_text())[:600]}


def summary(page):
    body = re.sub(r"\s+", " ", page.inner_text("body"))
    hits = re.findall(r"[^.]{0,80}(?:need you|Export blocked|Ready to export|checks passed|blocked by)[^.]{0,60}", body)
    return hits[:6]


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(f"{BASE}/#/case/{tok}")
    page.wait_for_selector('[data-testid="charges-panel"]', timeout=60000)
    time.sleep(0.5)
    out["before"] = {"a3": row_state(page, "a3"), "a6": row_state(page, "a6"), "summary": summary(page)}
    page.locator('tr[data-item-id="a3"]').scroll_into_view_if_needed()
    page.screenshot(path=os.path.join(HERE, "T-114-ui-1-rates-before-accept.png"), full_page=False)
    for item in ("a3", "a6"):
        btn = page.locator(f'tr[data-item-id="{item}"] [data-testid="btn-accept"]').first
        btn.click()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:20.098Z

I'll write a probe that loads lib09, prints the response shapes, and lists its gap flags and dates to confirm before I touch anything.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:22.440Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-probe.py",
 "content": "\"\"\"T-114 r2 paralegal-reviewer probe: load lib09 on the HEAD scratch server (:7881) and print the shapes needed for the gap-notice check.\nRead-only apart from creating a scratch case. Run: .venv/bin/python -I artifacts/review-evidence/T-114-r2-paralegal-probe.py [base_url]\n\"\"\"\nimport json\nimport sys\nimport time\nimport urllib.request\n\nBASE = sys.argv[1] if len(sys.argv) > 1 else \"http://127.0.0.1:7881\"\nLIB09 = \"case_lib09_spanish_interpreter_espalda\"\n\n\ndef api(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(BASE + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    with urllib.request.urlopen(r, timeout=120) as x:\n        return json.loads(x.read() or b\"null\")\n\n\ntok = api(\"POST\", \"/api/cases\", {\"library\": LIB09})[\"token\"]\napi(\"POST\", f\"/api/cases/{tok}/run\", {})\nfor _ in range(480):\n    st = api(\"GET\", f\"/api/cases/{tok}/status\")[\"status\"]\n    if st in (\"ready\", \"failed\", \"done_with_errors\"):\n        break\n    time.sleep(0.25)\nprint(\"status\", st, \"token_prefix\", tok[:6])\nview = api(\"GET\", f\"/api/cases/{tok}\")\nprint(\"view keys\", sorted(view.keys()))\nprint(\"dates_to_confirm\", json.dumps(view.get(\"dates_to_confirm\"), indent=1)[:1500])\ngap_flags = [f for f in view.get(\"flags\", []) if \"gap\" in json.dumps(f.get(\"type\", \"\")).lower()]\nprint(\"gap flags\", json.dumps(gap_flags, indent=1)[:2000])\nprint(\"flag types\", sorted({str(f.get(\"type\")) for f in view.get(\"flags\", [])}))\n"
}
````

### User / tool · 2026-11-02T10:56:22.543Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:23.723Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-114-r2-paralegal-probe.py 2>&1 | head -150",
 "description": "Run the lib09 shape probe against the scratch server"
}
````

### User / tool · 2026-11-02T10:56:24.381Z

**tool result**
````
status ready token_prefix 0nLaxq
view keys ['amounts', 'backend', 'created_at', 'dates_to_confirm', 'demo_mode', 'entries', 'error', 'flags', 'injection', 'models', 'name', 'records', 'review', 'status', 'token', 'totals', 'tray', 'undated_entries', 'updated_at', 'warnings']
dates_to_confirm [
 {
  "record_id": "r4",
  "raw": "03/05/2026",
  "candidates": [
   "2026-03-05",
   "2026-05-03"
  ],
  "status": "ambiguous",
  "suggestion": {
   "convention": "DMY",
   "label": "DD/MM",
   "iso": "2026-05-03",
   "reason": "Another date in this packet uses day first (Record 2: 14/04/2026)",
   "evidence": [
    {
     "record_id": "r2",
     "raw": "14/04/2026"
    }
   ],
   "evidence_count": 1,
   "auto_applied": false
  }
 }
]
gap flags [
 {
  "id": "f_gap_r1_r2",
  "state": "needs_review",
  "reasons": [
   "ENDPOINT_NOT_VERIFIED",
   "AI_TRANSLATION"
  ],
  "why": "One end of this gap could involve a date that has not been confirmed. AI translation \u2014 check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it.",
  "review_status": "pending",
  "edited": null,
  "ladder": {
   "backend": "fixture",
   "code_checks": {
    "computed_by": "code",
    "spans_match_input": true
   },
   "generator": null,
   "human": {
    "action": null,
    "edited_text": null,
    "at": null
   },
   "item_id": "f_gap_r1_r2",
   "judge": null,
   "state": "needs_review"
  },
  "type": "gap",
  "category": "gap_over_30",
  "source_kind": "record",
  "title": "Gap of 42 days",
  "explanation": "Gap of 42 days between March 3, 2026 (Quillmere Regional ED) and April 14, 2026 (Consultorio M\u00e9dico Aguaclara, nota de consulta).",
  "computed": {
   "days": 42,
   "endpoint_warnings": [],
   "record_ids": [
    "r1",
    "r2"
   ],
   "record_nos": [
    1,
    2
   ],
   "from": "2026-03-03",
   "to": "2026-04-14",
   "threshold": 30,
   "from_record": "r1",
   "to_record": "r2"
  },
  "evidence": [
   {
    "record_id": "r1",
    "excerpt": "Date: 2026-03-03",
    "start": 77,
    "end": 93
   },
   {
    "record_id": "r1",
    "excerpt": "Source: Quillmere Regional ED",
    "start": 94,
    "end": 123
   },
   {
    "record_id": "r2",
    "excerpt": "Date: 14/04/2026",
    "start": 388,
    "end": 404
   },
   {
    "record_id": "r2",
    "excerpt": "Source: Consultorio M\u00e9dico Aguaclara, nota de consulta",
    "start": 405,
    "end": 459
   }
  ],
  "origin": "code",
  "reviewer_note": null
 }
]
flag types ['causation', 'gap', 'pre_existing', 'record_warning']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:27.036Z

The lib09 gap is still 42 days (r1 to r2), and record 4 (03/05/2026) is ambiguous. Before choosing a case I'll sweep every library packet: confirm each candidate date on a fresh case and record which gap figures move.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:31.496Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-sweep.py",
 "content": "\"\"\"T-114 r2 paralegal-reviewer sweep: for every library packet and every date-to-confirm candidate, load a fresh scratch case, confirm that\ncandidate and record which gap figures the backend says changed (gap_changes). Scratch server only (HEAD archive, :7881).\nRun: .venv/bin/python -I artifacts/review-evidence/T-114-r2-paralegal-sweep.py [base_url]\nWrites T-114-r2-paralegal-sweep.out.json next to this file.\n\"\"\"\nimport json\nimport os\nimport sys\nimport time\nimport urllib.request\n\nBASE = sys.argv[1] if len(sys.argv) > 1 else \"http://127.0.0.1:7881\"\nHERE = os.path.dirname(os.path.abspath(__file__))\n\n\ndef api(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(BASE + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    with urllib.request.urlopen(r, timeout=120) as x:\n        return json.loads(x.read() or b\"null\")\n\n\ndef load(lib):\n    tok = api(\"POST\", \"/api/cases\", {\"library\": lib})[\"token\"]\n    api(\"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(480):\n        st = api(\"GET\", f\"/api/cases/{tok}/status\")[\"status\"]\n        if st in (\"ready\", \"failed\", \"done_with_errors\"):\n            break\n        time.sleep(0.25)\n    return tok, st\n\n\ndef gap_figs(view):\n    out = {}\n    for f in view.get(\"flags\", []):\n        if f.get(\"type\") == \"gap\":\n            c = f.get(\"computed\") or {}\n            out[f[\"id\"]] = {\"days\": c.get(\"days\"), \"from\": c.get(\"from\"), \"to\": c.get(\"to\"), \"record_nos\": c.get(\"record_nos\")}\n    return out\n\n\nlibs = sorted(x[\"id\"] for x in api(\"GET\", \"/api/library\")[\"cases\"])\nrows = []\nfor lib in libs:\n    tok, st = load(lib)\n    view = api(\"GET\", f\"/api/cases/{tok}\")\n    for d in view.get(\"dates_to_confirm\", []):\n        before = gap_figs(view)\n        for cand in d.get(\"candidates\", []):\n            t2, st2 = load(lib)\n            v2 = api(\"GET\", f\"/api/cases/{t2}\")\n            # the record id may differ per fresh case only if the pipeline is nondeterministic; match by record_id\n            resp = api(\"POST\", f\"/api/cases/{t2}/records/{d['record_id']}/confirm_date\", {\"date\": cand})\n            after = gap_figs(api(\"GET\", f\"/api/cases/{t2}\"))\n            rows.append({\"lib\": lib, \"status\": st, \"record_id\": d[\"record_id\"], \"raw\": d.get(\"raw\"), \"candidate\": cand,\n                         \"suggested_iso\": (d.get(\"suggestion\") or {}).get(\"iso\"),\n                         \"gap_changes\": resp.get(\"gap_changes\"), \"gap_before\": before, \"gap_after\": after,\n                         \"pre_confirm_probe_status\": st2})\n            _ = v2\nrows_changed = [r for r in rows if r[\"gap_changes\"]]\nout = {\"libs\": len(libs), \"confirm_attempts\": len(rows), \"with_gap_changes\": len(rows_changed), \"rows\": rows}\nwith open(os.path.join(HERE, \"T-114-r2-paralegal-sweep.out.json\"), \"w\") as fh:\n    json.dump(out, fh, indent=1, ensure_ascii=False)\nprint(\"libs\", len(libs), \"confirm attempts\", len(rows), \"with gap_changes\", len(rows_changed))\nfor r in rows_changed:\n    print(json.dumps({k: r[k] for k in (\"lib\", \"record_id\", \"raw\", \"candidate\", \"suggested_iso\", \"gap_changes\")}, ensure_ascii=False))\n"
}
````

### User / tool · 2026-11-02T10:56:31.616Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-sweep.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:32.699Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-114-r2-paralegal-sweep.py 2>&1 | tail -40",
 "description": "Sweep all library packets for date confirms that change a gap"
}
````

### User / tool · 2026-11-02T10:56:38.036Z

**tool result**
````
libs 15 confirm attempts 2 with gap_changes 1
{"lib": "case_lib09_spanish_interpreter_espalda", "record_id": "r4", "raw": "03/05/2026", "candidate": "2026-03-05", "suggested_iso": "2026-05-03", "gap_changes": [{"flag_id": "f_gap_r4_r2", "change": "changed", "old_days": 42, "new_days": 40, "old_from": "2026-03-03", "old_to": "2026-04-14", "new_from": "2026-03-05", "new_to": "2026-04-14", "sentence": "Gap recalculated after you confirmed record 4: now 40 days (was 42)."}]}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:42.851Z

Only two confirm attempts exist across all 15 packets, and both are lib09 record 4. The 2026-03-05 candidate still moves the gap 42 to 40, so the T-116 concern did not apply at HEAD. Next I'll read how the frontend renders `gap_changes` so the browser check targets the right elements.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:44.424Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/archive && sed -n 66,100p app/frontend/timeline.js; echo ---; grep -rn \"gapNotice\\|gap-notice\\|gapChange\\|gap_change\\|recalculated\" app/frontend/*.js | head -20",
 "description": "Read frontend confirm-date handler and notice rendering"
}
````

### User / tool · 2026-11-02T10:56:44.529Z

**tool result**
````
    const m = /(?:^|\n)Excerpt:\s*"?([\s\S]*?)"?\s*$/.exec(rec.text || "");
    return m ? m[1].trim() : "";
  }
  ZL.recordExcerpt = recordExcerpt;
  // ---- confirm a date reading (used by Dates to confirm, the flag card's date form and the pre-selected form). T-114: the backend answers with gap_changes[]; every
  // one is shown in plain words above the timeline (it stays until dismissed) and announced, so a figure never changes silently. Focus then moves to the
  // entry's Accept button (a date that was just confirmed is the next thing to decide), or to the "no entry yet" card.
  let gapNote = null;   // {token, items: [sentence]}
  ZL.confirmDate = async function (recordId, cand) {
    const s = ZL.state.get(), resp = await ZL.api.confirmDate(s.token, recordId, cand);
    const changes = (resp && Array.isArray(resp.gap_changes) ? resp.gap_changes : []).map((g) => g && g.sentence).filter(Boolean);
    gapNote = changes.length ? { token: s.token, items: changes } : null;
    ZL.state.set({ case: await ZL.api.getCase(s.token) });
    const c = ZL.state.get().case, rec = c.records.find((r) => r.id === recordId), say = ZL.rv && ZL.rv.say ? ZL.rv.say : () => {};
    const en = c.entries.concat(c.undated_entries).find((x) => (x.record_ids || [])[0] === recordId);
    const left = ZL.$('[data-testid="missing-entry"][data-record-id="' + recordId + '"]');
    let msg = "Date confirmed: " + ZL.fmtDate(cand) + ".";
    if (left) msg += " Record " + (rec ? rec.seq : "") + " has no entry yet; it is listed under Records without an entry.";
    if (changes.length) msg += " " + changes.join(" ");
    say(msg);
    requestAnimationFrame(() => {
      const b = en && document.querySelector('[data-testid="queue"] [data-controls-for="' + en.id + '"] [data-action="accept"]');
      if (b) { b.focus({ preventScroll: true }); b.scrollIntoView({ block: "center" }); }
      else if (left) left.scrollIntoView({ block: "center" });
    });
    return resp;
  };
  function gapNoteNode(c) {
    if (!gapNote || gapNote.token !== c.token) return null;
    return el("section", { class: "notice notice--info", "data-testid": "gap-change-note", role: "status", "aria-label": "Gap figures changed" },
      el("div", { class: "notice-body" }, el("strong", {}, "A gap figure changed. "), gapNote.items.map((t) => el("span", { class: "gap-sentence" }, t + " "))),
      el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-dismiss-gap-note", onclick: (ev) => { gapNote = null; ev.target.closest("section").remove(); } }, "Got it"));
  }
  function datesToConfirm(c) {
    const none = !c.undated_entries.length && !c.dates_to_confirm.some((d) => d.candidates.length);
---
app/frontend/timeline.js:70:  // ---- confirm a date reading (used by Dates to confirm, the flag card's date form and the pre-selected form). T-114: the backend answers with gap_changes[]; every
app/frontend/timeline.js:76:    const changes = (resp && Array.isArray(resp.gap_changes) ? resp.gap_changes : []).map((g) => g && g.sentence).filter(Boolean);
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:54.159Z

The banner is `[data-testid="gap-change-note"]`, shown above the timeline and kept in memory only. Before writing the browser script I need the confirm-date form and rate-row selectors.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:56.293Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/archive && grep -rn -o -E \"data-testid\\\": \\\"(confirm-date|btn-confirm-date|dates-to-confirm|flags-tray|tray[a-z-]*|flag[a-z-]*|gap[a-z-]*)\\\"\" app/frontend/*.js | sort | uniq | head -30; echo ---; grep -rn -E \"Needs review|Accept as noted|Noted\" app/frontend/*.js | grep -v \"^.*//\" | head -12",
 "description": "Find confirm-date, tray, and rate-row selectors in frontend"
}
````

### User / tool · 2026-11-02T10:56:56.394Z

**tool result**
````
app/frontend/charges.js:114:data-testid": "tray-notice"
app/frontend/flags.js:21:data-testid": "flag-evidence"
app/frontend/flags.js:55:data-testid": "flag-"
app/frontend/flags.js:62:data-testid": "flag-note-text"
app/frontend/suggestions.js:27:data-testid": "btn-confirm-date"
app/frontend/suggestions.js:30:data-testid": "confirm-date"
app/frontend/timeline.js:101:data-testid": "dates-to-confirm"
app/frontend/timeline.js:110:data-testid": "confirm-date"
app/frontend/timeline.js:153:data-testid": "tray-item"
app/frontend/timeline.js:155:data-testid": "tray-flag-lead"
app/frontend/timeline.js:156:data-testid": "tray-reason"
app/frontend/timeline.js:158:data-testid": "tray-why"
app/frontend/timeline.js:159:data-testid": "tray-why"
app/frontend/timeline.js:160:data-testid": "tray-attempt"
app/frontend/timeline.js:95:data-testid": "gap-change-note"
---
app/frontend/review.js:45:  const STATE_LABEL = { verified: "Quote matches", needs_review: "Needs review", rejected: "Could not verify" };
app/frontend/timeline.js:8:  const STATE_LABEL = { verified: "Quote matches", needs_review: "Needs review", rejected: "Could not verify" };
app/frontend/timeline.js:258:            el("option", { value: "review", selected: sortMode === "review" }, "Needs review first"), el("option", { value: "date", selected: sortMode === "date" }, "By date")))),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:56:59.182Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/archive && sed -n 98,125p app/frontend/timeline.js; echo ---; sed -n 20,40p app/frontend/suggestions.js",
 "description": "Read dates-to-confirm and confirm-date form rendering"
}
````

### User / tool · 2026-11-02T10:56:59.299Z

**tool result**
````
  }
  function datesToConfirm(c) {
    const none = !c.undated_entries.length && !c.dates_to_confirm.some((d) => d.candidates.length);
    const box = el("section", { class: "group" + (none ? " group--empty" : ""), "data-testid": "dates-to-confirm", "aria-labelledby": "h-dates" }, el("h2", { id: "h-dates" }, "Dates to confirm"));
    if (none) { box.append(el("p", { class: "muted" }, "None. Every record has a readable date.")); return box; }
    box.append(el("p", { class: "muted small" }, "These records are left off the timeline and the gap check until you pick the right date. The tool never guesses."));
    const confirmDate = (d, cand) => ZL.confirmDate(d.record_id, cand);
    const confirmBar = (d) => {
      const raw = d.raw || d.date_raw || "";
      // T-088/T-096: a suggested reading is pre-selected with its reason, and still needs the paralegal's Confirm click.
      if (ZL.sg && ZL.sg.usableSuggestion(d)) return ZL.sg.dateForm(d, { legend: `Written as “${raw}”. Which date?`, onConfirm: (cand) => confirmDate(d, cand) });
      const bar = el("div", { class: "row", role: "group", "aria-label": "Choose the date" }, el("span", {}, `Written as “${raw}”. Which date?`));
      d.candidates.forEach((cand) => bar.append(el("button", { type: "button", class: "btn", "data-testid": "confirm-date", "data-date": cand, onclick: async () => {
        try { await confirmDate(d, cand); } catch (er) { alert(er.message); }
      } }, ZL.fmtDate(cand))));
      if (d.suggestion && d.suggestion.reason) bar.append(el("p", { class: "muted small", "data-testid": "date-suggestion-reason" }, "Hint: " + d.suggestion.reason + ". It does not point to one date, so none is selected."));
      return bar;
    };
    const shown = {};
    c.undated_entries.forEach((e) => {
      const d = c.dates_to_confirm.find((x) => x.record_id === e.record_ids[0]);
      const rec = c.records.find((r) => r.id === e.record_ids[0]);
      const row = entryRow(e, c); row.classList.add("undated");
      if (d) shown[d.record_id] = true;
      if (d && d.candidates.length) row.insertBefore(confirmBar(d), row.querySelector(".row-actions"));
      else if (rec) row.insertBefore(el("p", { class: "reason" }, "No readable date in this record header; it stays off the timeline."), row.querySelector(".row-actions"));
      box.append(row);
    });
---
  };
  let formSeq = 0;
  // d = a dates_to_confirm row; onConfirm(date) is async and may throw (its message is shown, the choice stays).
  sg.dateForm = function (d, opts) {
    opts = opts || {};
    const sug = sg.usableSuggestion(d), n = ++formSeq, raw = d.raw || d.date_raw || "";
    const err = el("p", { class: "rv-error sg-error", role: "alert", "data-testid": "confirm-date-error" });
    const submit = el("button", { type: "submit", class: "btn btn--primary sg-confirm", "data-testid": "btn-confirm-date", disabled: !sug }, "Confirm date");
    const reasonId = "sg-reason-" + n;
    const radios = (d.candidates || []).map((cand) => {
      const input = el("input", { type: "radio", name: "cd-" + n, value: cand, "data-testid": "confirm-date", "data-date": cand, checked: !!sug && sug.iso === cand,
        onchange: () => { submit.disabled = false; } });
      return el("label", { class: "rv-radio sg-radio" }, input, el("span", {}, ZL.fmtDate(cand) + " (" + cand + ")"),
        sug && sug.iso === cand ? el("span", { class: "sg-tag", "data-testid": "date-suggested-tag" }, "Suggested" + (sug.label ? " · " + sug.label : "")) : null);
    });
    const hint = d.suggestion && d.suggestion.reason ? d.suggestion.reason : "";
    const form = el("form", { class: "rv-datefix sg-dateform", "data-record-id": d.record_id, onsubmit: (ev) => ev.preventDefault() },
      el("fieldset", { class: "rv-fieldset", "aria-describedby": hint ? reasonId : null },
        el("legend", {}, opts.legend || "Written as “" + raw + "”. Which date?"), radios),
      hint ? el("p", { class: "sg-reason", id: reasonId, "data-testid": "date-suggestion-reason" },
        el("strong", {}, sug ? "Why this reading is suggested: " : "Hint: "), hint + ".",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:57:07.235Z

The confirm form has pre-checked suggested radio 2026-05-03, so I need to select 2026-03-05 myself. I'll also check whether the banner stays in the viewport after the focus move, since the handler scrolls the entry's Accept button to center. Writing the browser script now.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:57:16.925Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-ui-gap.py",
 "content": "\"\"\"T-114 r2 paralegal-reviewer UI check on the HEAD scratch server (e1ce8dc archive, :7881).\nCase: case_lib09_spanish_interpreter_espalda. Confirm record 4 as 2026-03-05 in the browser (the \"Dates to confirm\" form),\nthen read the gap-change notice, the gap flag card and the flags tray, check whether the notice is in the viewport after focus moves,\ndismiss it, reload, and look again. Then accept rate row a3 on a second load and read its state.\nRun: .venv/bin/python artifacts/review-evidence/T-114-r2-paralegal-ui-gap.py [base_url]\nWrites T-114-r2-ui-*.png and T-114-r2-paralegal-ui-gap.out.json next to this file.\n\"\"\"\nimport json\nimport os\nimport re\nimport sys\nimport time\nimport urllib.request\n\nfrom playwright.sync_api import sync_playwright\n\nBASE = sys.argv[1] if len(sys.argv) > 1 else \"http://127.0.0.1:7881\"\nHERE = os.path.dirname(os.path.abspath(__file__))\nLIB09 = \"case_lib09_spanish_interpreter_espalda\"\nout = {\"base\": BASE, \"steps\": {}}\n\n\ndef api(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(BASE + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    with urllib.request.urlopen(r, timeout=120) as x:\n        return json.loads(x.read() or b\"null\")\n\n\ndef new_case():\n    tok = api(\"POST\", \"/api/cases\", {\"library\": LIB09})[\"token\"]\n    api(\"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(480):\n        if api(\"GET\", f\"/api/cases/{tok}/status\")[\"status\"] in (\"ready\", \"failed\", \"done_with_errors\"):\n            break\n        time.sleep(0.25)\n    return tok\n\n\ndef norm(s):\n    return re.sub(r\"\\s+\", \" \", s or \"\").strip()\n\n\ndef in_viewport(loc, page):\n    box = loc.bounding_box()\n    if not box:\n        return False\n    vh = page.viewport_size[\"height\"]\n    return box[\"y\"] + box[\"height\"] > 0 and box[\"y\"] < vh\n\n\ndef gap_cards(page):\n    \"\"\"Every flag card or tray row whose text names a gap (any state).\"\"\"\n    hits = []\n    for sel in ['[data-testid^=\"flag-\"]', '[data-testid=\"tray-item\"]']:\n        for i in range(page.locator(sel).count()):\n            el = page.locator(sel).nth(i)\n            t = norm(el.inner_text())\n            if \"Gap\" in t or \"gap\" in t:\n                hits.append({\"sel\": sel, \"testid\": el.get_attribute(\"data-testid\"), \"text\": t[:500]})\n    return hits\n\n\ntok = new_case()\nout[\"token_prefix\"] = tok[:6]\n\nwith sync_playwright() as p:\n    browser = p.chromium.launch()\n    page = browser.new_page(viewport={\"width\": 1440, \"height\": 900})\n    page.goto(f\"{BASE}/#/case/{tok}\")\n    page.wait_for_selector('[data-testid=\"dates-to-confirm\"]', timeout=60000)\n    time.sleep(0.5)\n    out[\"steps\"][\"before_confirm\"] = {\"gap_cards\": gap_cards(page), \"gap_note_count\": page.locator('[data-testid=\"gap-change-note\"]').count()}\n    page.screenshot(path=os.path.join(HERE, \"T-114-r2-ui-1-before-confirm.png\"), full_page=False)\n\n    # Choose 2026-03-05 (not the pre-checked suggestion 2026-05-03) and confirm.\n    form = page.locator('form[data-testid=\"confirm-date\"], form.sg-dateform').first\n    form.locator('input[data-testid=\"confirm-date\"][value=\"2026-03-05\"]').check()\n    page.locator('[data-testid=\"btn-confirm-date\"]').first.click()\n    page.wait_for_selector('[data-testid=\"gap-change-note\"]', timeout=20000)\n    time.sleep(0.8)\n    note = page.locator('[data-testid=\"gap-change-note\"]')\n    out[\"steps\"][\"after_confirm\"] = {\n        \"note_text\": norm(note.inner_text()),\n        \"note_in_viewport\": in_viewport(note, page),\n        \"note_box\": note.bounding_box(),\n        \"scroll_y\": page.evaluate(\"window.scrollY\"),\n        \"gap_cards\": gap_cards(page),\n        \"live_region_text\": norm(\" \".join(page.locator('[role=\"status\"]').all_inner_texts()))[:600],\n    }\n    page.screenshot(path=os.path.join(HERE, \"T-114-r2-ui-2-after-confirm.png\"), full_page=False)\n\n    # The viewport after focus move: where is the note relative to the top of the page?\n    page.evaluate(\"window.scrollTo(0, 0)\")\n    time.sleep(0.3)\n    out[\"steps\"][\"after_confirm_scrolled_top\"] = {\"note_in_viewport\": in_viewport(note, page), \"note_box\": note.bounding_box()}\n    page.screenshot(path=os.path.join(HERE, \"T-114-r2-ui-3-note-top.png\"), full_page=False)\n\n    # Dismiss, then reload: is the notice still there, and what does the gap card say after a reload?\n    page.locator('[data-testid=\"btn-dismiss-gap-note\"]').click()\n    time.sleep(0.3)\n    out[\"steps\"][\"after_dismiss\"] = {\"note_count\": page.locator('[data-testid=\"gap-change-note\"]').count()}\n    page.reload()\n    page.wait_for_selector('[data-testid=\"dates-to-confirm\"], [data-testid=\"charges-panel\"]', timeout=60000)\n    time.sleep(0.8)\n    out[\"steps\"][\"after_reload\"] = {\"note_count\": page.locator('[data-testid=\"gap-change-note\"]').count(), \"gap_cards\": gap_cards(page),\n                                    \"body_has_recalc\": \"Gap recalculated\" in page.inner_text(\"body\"),\n                                    \"body_has_was_42\": \"was 42\" in page.inner_text(\"body\")}\n    page.screenshot(path=os.path.join(HERE, \"T-114-r2-ui-4-after-reload.png\"), full_page=False)\n    browser.close()\n\n# Rate row check on a fresh lib09 case (round-1 minor): accept a3 and read the row.\ntok2 = new_case()\nwith sync_playwright() as p:\n    browser = p.chromium.launch()\n    page = browser.new_page(viewport={\"width\": 1440, \"height\": 900})\n    page.goto(f\"{BASE}/#/case/{tok2}\")\n    page.wait_for_selector('[data-testid=\"charges-panel\"]', timeout=60000)\n    time.sleep(0.5)\n    row = page.locator('tr[data-item-id=\"a3\"]')\n    before = {\"data_review\": row.get_attribute(\"data-review\"), \"text\": norm(row.inner_text())[:400],\n              \"btns\": [norm(b.inner_text()) for b in row.locator(\"button\").all()]}\n    row.locator('[data-testid=\"btn-accept\"]').first.click()\n    time.sleep(1.0)\n    row = page.locator('tr[data-item-id=\"a3\"]')\n    after = {\"data_review\": row.get_attribute(\"data-review\"), \"data_state\": row.get_attribute(\"data-state\"),\n             \"text\": norm(row.inner_text())[:400], \"btns\": [norm(b.inner_text()) for b in row.locator(\"button\").all()],\n             \"has_needs_review_chip\": row.locator(':text-is(\"Needs review\")').count(),\n             \"has_accept_as_noted\": row.locator(':text-is(\"Accept as noted\")').count()}\n    out[\"steps\"][\"rate_a3_before\"] = before\n    out[\"steps\"][\"rate_a3_after\"] = after\n    page.locator('tr[data-item-id=\"a3\"]').scroll_into_view_if_needed()\n    page.screenshot(path=os.path.join(HERE, \"T-114-r2-ui-5-rate-a3-after-accept.png\"), full_page=False)\n    browser.close()\n\nwith open(os.path.join(HERE, \"T-114-r2-paralegal-ui-gap.out.json\"), \"w\") as fh:\n    json.dump(out, fh, indent=1, ensure_ascii=False)\nprint(json.dumps(out, indent=1, ensure_ascii=False)[:6000])\n"
}
````

### User / tool · 2026-11-02T10:57:17.024Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-ui-gap.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:57:18.317Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-114-r2-paralegal-ui-gap.py 2>&1 | head -220",
 "description": "Run the browser check for the gap notice and rate row"
}
````

### User / tool · 2026-11-02T10:57:24.929Z

**tool result**
````
{
 "base": "http://127.0.0.1:7881",
 "steps": {
  "before_confirm": {
   "gap_cards": [
    {
     "sel": "[data-testid^=\"flag-\"]",
     "testid": "flag-f_gap_r1_r2",
     "text": "Gap of 42 days Needs review Gap of 42 days between March 3, 2026 (Quillmere Regional ED) and April 14, 2026 (Consultorio Médico Aguaclara, nota de consulta). Needs review: One end of this gap could involve a date that has not been confirmed. AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it. Record 1 · Quillmere Regional ED Date: 2026-03-03 Source: Quillme"
    },
    {
     "sel": "[data-testid^=\"flag-\"]",
     "testid": "flag-f_date_r4",
     "text": "Date to confirm Needs review The date “03/05/2026” in Consultorio Médico Aguaclara, formulario de admisión (OCR) can be read more than one way; choose one reading. Needs review: The date can be read two ways; confirm which one is right. It is left out of gap checks until then. AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it. Record 4 · Consultorio Médico"
    }
   ],
   "gap_note_count": 0
  },
  "after_confirm": {
   "note_text": "A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42). Got it",
   "note_in_viewport": true,
   "note_box": {
    "x": 24,
    "y": 128,
    "width": 985.609375,
    "height": 54
   },
   "scroll_y": 155,
   "gap_cards": [
    {
     "sel": "[data-testid^=\"flag-\"]",
     "testid": "flag-f_gap_r4_r2",
     "text": "Gap of 40 days Needs review Gap of 40 days between March 5, 2026 (Consultorio Médico Aguaclara, formulario de admisión (OCR)) and April 14, 2026 (Consultorio Médico Aguaclara, nota de consulta). This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued. If record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR) is paperwork, not a visit, the gap would be 42 days (March 3, 2026 t"
    }
   ],
   "live_region_text": "0 of 19 decided · 13 need review 7 records found A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42). Got it Date confirmed: March 5, 2026. Gap recalculated after you confirmed record 4: now 40 days (was 42)."
  },
  "after_confirm_scrolled_top": {
   "note_in_viewport": true,
   "note_box": {
    "x": 24,
    "y": 283,
    "width": 985.609375,
    "height": 54
   }
  },
  "after_dismiss": {
   "note_count": 0
  },
  "after_reload": {
   "note_count": 0,
   "gap_cards": [
    {
     "sel": "[data-testid^=\"flag-\"]",
     "testid": "flag-f_gap_r4_r2",
     "text": "Gap of 40 days Needs review Gap of 40 days between March 5, 2026 (Consultorio Médico Aguaclara, formulario de admisión (OCR)) and April 14, 2026 (Consultorio Médico Aguaclara, nota de consulta). This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued. If record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR) is paperwork, not a visit, the gap would be 42 days (March 3, 2026 t"
    }
   ],
   "body_has_recalc": false,
   "body_has_was_42": false
  },
  "rate_a3_before": {
   "data_review": "pending",
   "text": "$400.00 Rate … en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00. Open record 2 Why this status Needs review Not counted: a rate, not a bill. rate $400.00; count not stated; needs review Keep in notes Dismiss Audit",
   "btns": [
    "Open record 2",
    "Why this status",
    "Keep in notes",
    "Dismiss",
    "Audit"
   ]
  },
  "rate_a3_after": {
   "data_review": "accepted",
   "data_state": "needs_review",
   "text": "$400.00 Rate … en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00. Open record 2 Why this status Needs review Accepted Not counted: a rate, not a bill. rate $400.00; count not stated; needs review Kept in the internal notes only; not in the letter or the total. Kept in notes Dismiss Undo Audit",
   "btns": [
    "Open record 2",
    "Why this status",
    "Kept in notes",
    "Dismiss",
    "Undo",
    "Audit"
   ],
   "has_needs_review_chip": 1,
   "has_accept_as_noted": 0
  }
 },
 "token_prefix": "366WnJ"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:57:39.408Z

The browser run shows the notice appears right after confirm and names both numbers. It is gone after dismiss or reload, and the gap card does not carry the sentence. I'll read the full gap-card text after reload, check whether the "Kept in notes" control is disabled, and query the scratch DB for the lib01 fixture-miss nit.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:57:46.057Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-checks2.py",
 "content": "\"\"\"T-114 r2 paralegal-reviewer follow-up checks on the HEAD scratch server (e1ce8dc archive, :7881).\n1. Full text of the lib09 gap card after confirm, dismiss and reload (no notice): does the card say why the figure moved?\n2. The accepted rate row a3: is the \"Kept in notes\" control disabled, and what does its state chip say?\n3. Round-1 nit: FIXTURE_MISS rows in the scratch DB's llm_calls table (lib01 extract step).\nRun: .venv/bin/python -I artifacts/review-evidence/T-114-r2-paralegal-checks2.py [base_url] [db_path]\n\"\"\"\nimport json\nimport os\nimport re\nimport sqlite3\nimport sys\nimport time\nimport urllib.request\n\nfrom playwright.sync_api import sync_playwright\n\nBASE = sys.argv[1] if len(sys.argv) > 1 else \"http://127.0.0.1:7881\"\nDB = sys.argv[2] if len(sys.argv) > 2 else None\nHERE = os.path.dirname(os.path.abspath(__file__))\nLIB09 = \"case_lib09_spanish_interpreter_espalda\"\nout = {\"base\": BASE}\n\n\ndef api(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(BASE + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    with urllib.request.urlopen(r, timeout=120) as x:\n        return json.loads(x.read() or b\"null\")\n\n\ndef new_case():\n    tok = api(\"POST\", \"/api/cases\", {\"library\": LIB09})[\"token\"]\n    api(\"POST\", f\"/api/cases/{tok}/run\", {})\n    for _ in range(480):\n        if api(\"GET\", f\"/api/cases/{tok}/status\")[\"status\"] in (\"ready\", \"failed\", \"done_with_errors\"):\n            break\n        time.sleep(0.25)\n    return tok\n\n\ndef norm(s):\n    return re.sub(r\"\\s+\", \" \", s or \"\").strip()\n\n\ntok = new_case()\nwith sync_playwright() as p:\n    browser = p.chromium.launch()\n    page = browser.new_page(viewport={\"width\": 1440, \"height\": 900})\n    page.goto(f\"{BASE}/#/case/{tok}\")\n    page.wait_for_selector('[data-testid=\"dates-to-confirm\"]', timeout=60000)\n    time.sleep(0.5)\n    form = page.locator('form.sg-dateform').first\n    form.locator('input[data-testid=\"confirm-date\"][value=\"2026-03-05\"]').check()\n    page.locator('[data-testid=\"btn-confirm-date\"]').first.click()\n    page.wait_for_selector('[data-testid=\"gap-change-note\"]', timeout=20000)\n    time.sleep(0.5)\n    card = page.locator('[data-testid=\"flag-f_gap_r4_r2\"]')\n    out[\"card_full_after_confirm\"] = norm(card.inner_text())\n    page.locator('[data-testid=\"btn-dismiss-gap-note\"]').click()\n    page.reload()\n    page.wait_for_selector('[data-testid=\"dates-to-confirm\"], [data-testid=\"charges-panel\"]', timeout=60000)\n    time.sleep(0.8)\n    card = page.locator('[data-testid=\"flag-f_gap_r4_r2\"]')\n    out[\"card_full_after_reload\"] = norm(card.inner_text())\n    out[\"card_has_was_or_recalc_after_reload\"] = bool(re.search(r\"was 42|Gap recalculated|changed\", out[\"card_full_after_reload\"]))\n    browser.close()\n\ntok2 = new_case()\nwith sync_playwright() as p:\n    browser = p.chromium.launch()\n    page = browser.new_page(viewport={\"width\": 1440, \"height\": 900})\n    page.goto(f\"{BASE}/#/case/{tok2}\")\n    page.wait_for_selector('[data-testid=\"charges-panel\"]', timeout=60000)\n    time.sleep(0.5)\n    row = page.locator('tr[data-item-id=\"a3\"]')\n    row.locator('[data-testid=\"btn-accept\"]').first.click()\n    time.sleep(1.0)\n    row = page.locator('tr[data-item-id=\"a3\"]')\n    kept = row.locator('button', has_text=\"Kept in notes\").first\n    out[\"rate_a3_kept_button\"] = {\"text\": norm(kept.inner_text()), \"disabled\": kept.is_disabled()}\n    out[\"rate_a3_chips\"] = [norm(x.inner_text()) for x in row.locator('[data-testid=\"entry-state\"], .chip, .state, .badge').all()][:6]\n    out[\"rate_a3_needs_review_text_count\"] = row.locator(':text-is(\"Needs review\")').count()\n    page.locator('tr[data-item-id=\"a3\"]').scroll_into_view_if_needed()\n    page.screenshot(path=os.path.join(HERE, \"T-114-r2-ui-6-rate-a3-kept.png\"), full_page=False)\n    browser.close()\n\nif DB:\n    c = sqlite3.connect(DB)\n    cols = [r[1] for r in c.execute(\"PRAGMA table_info(llm_calls)\")]\n    rows = c.execute(\"SELECT * FROM llm_calls WHERE error LIKE 'FIXTURE_MISS%'\").fetchall()\n    out[\"fixture_miss_columns\"] = cols\n    out[\"fixture_miss_count\"] = len(rows)\n    out[\"fixture_miss_rows\"] = [{k: (str(v)[:120] if v is not None else None) for k, v in zip(cols, r) if k in (\"step\", \"attempt\", \"parsed_ok\", \"error\", \"case_id\", \"name\", \"created_at\", \"at\", \"case_token\", \"token\")} for r in rows[:12]]\n    c.close()\n\nwith open(os.path.join(HERE, \"T-114-r2-paralegal-checks2.out.json\"), \"w\") as fh:\n    json.dump(out, fh, indent=1, ensure_ascii=False)\nprint(json.dumps(out, indent=1, ensure_ascii=False)[:8000])\n"
}
````

### User / tool · 2026-11-02T10:57:46.168Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-checks2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:57:48.695Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-114-r2-paralegal-checks2.py http://127.0.0.1:7881 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/app.sqlite3 2>&1 | head -150",
 "description": "Run gap-card full-text, rate-row, and FIXTURE_MISS checks"
}
````

### User / tool · 2026-11-02T10:57:54.136Z

**tool result**
````
{
 "base": "http://127.0.0.1:7881",
 "card_full_after_confirm": "Gap of 40 days Needs review Gap of 40 days between March 5, 2026 (Consultorio Médico Aguaclara, formulario de admisión (OCR)) and April 14, 2026 (Consultorio Médico Aguaclara, nota de consulta). This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued. If record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR) is paperwork, not a visit, the gap would be 42 days (March 3, 2026 to April 14, 2026). Needs review: AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it. This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued. If record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR) is paperwork, not a visit, the gap would be 42 days (March 3, 2026 to April 14, 2026). Record 4 · Consultorio Médico Aguaclara, formulario de admisión (OCR) Date: 03/05/2026 Source: Consultorio Médico Aguaclara, formulario de admisión (OCR) Record 2 · Consultorio Médico Aguaclara, nota de consulta Date: 14/04/2026 Source: Consultorio Médico Aguaclara, nota de consulta Open records 4 and 2 Why this status Accept Edit note Dismiss Dismiss with reason… Audit",
 "card_full_after_reload": "Gap of 40 days Needs review Gap of 40 days between March 5, 2026 (Consultorio Médico Aguaclara, formulario de admisión (OCR)) and April 14, 2026 (Consultorio Médico Aguaclara, nota de consulta). This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued. If record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR) is paperwork, not a visit, the gap would be 42 days (March 3, 2026 to April 14, 2026). Needs review: AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it. This gap starts at record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR), which looks like paperwork, not a visit. Check whether treatment continued. If record 4: Consultorio Médico Aguaclara, formulario de admisión (OCR) is paperwork, not a visit, the gap would be 42 days (March 3, 2026 to April 14, 2026). Record 4 · Consultorio Médico Aguaclara, formulario de admisión (OCR) Date: 03/05/2026 Source: Consultorio Médico Aguaclara, formulario de admisión (OCR) Record 2 · Consultorio Médico Aguaclara, nota de consulta Date: 14/04/2026 Source: Consultorio Médico Aguaclara, nota de consulta Open records 4 and 2 Why this status Accept Edit note Dismiss Dismiss with reason… Audit",
 "card_has_was_or_recalc_after_reload": false,
 "rate_a3_kept_button": {
  "text": "Kept in notes",
  "disabled": false
 },
 "rate_a3_chips": [
  "Needs review",
  "Accepted"
 ],
 "rate_a3_needs_review_text_count": 1,
 "fixture_miss_columns": [
  "id",
  "case_id",
  "item_id",
  "role",
  "step",
  "backend",
  "model",
  "prompt_version",
  "prompt_sha256",
  "system_text",
  "user_text",
  "response_raw",
  "parsed_ok",
  "verdict",
  "attempt",
  "latency_ms",
  "cost_usd",
  "tokens_in",
  "tokens_out",
  "recorded_from_json",
  "error",
  "created_at"
 ],
 "fixture_miss_count": 1,
 "fixture_miss_rows": [
  {
   "case_id": "K35VlBs8_p18UES0Rfpohg",
   "step": "extract",
   "parsed_ok": "0",
   "attempt": "1",
   "error": "FIXTURE_MISS 83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557",
   "created_at": "1793616992.8711019"
  }
 ]
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:57:58.491Z

The gap card after reload still says "Gap of 40 days" with no "was 42" or "recalculated" wording, and the rate row still carries a "Needs review" chip. The lib01 fixture miss is still there. I'll confirm that miss belongs to lib01, then look at the screenshots.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:58:00.327Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/app.sqlite3; which sqlite3 && sqlite3 \"$D\" \"SELECT c.name, COUNT(*) FROM llm_calls l JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY c.name;\" ; echo \"exit=$?\"; sqlite3 \"$D\" \"SELECT COUNT(*) FROM llm_calls WHERE error LIKE 'FIXTURE_MISS%';\"",
 "description": "Map FIXTURE_MISS rows to case names in scratch DB"
}
````

### User / tool · 2026-11-02T10:58:00.466Z

**tool result**
````
/usr/bin/sqlite3
case lib01 er only then gap|1
exit=0
1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:58:02.562Z

The lib01 fixture miss is still present at HEAD. It is the only FIXTURE_MISS row across the scratch DB. Now the screenshots, starting with the notice right after confirm.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:58:02.909Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-ui-2-after-confirm.png"
}
````

### User / tool · 2026-11-02T10:58:02.919Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:58:03.142Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-ui-4-after-reload.png"
}
````

### User / tool · 2026-11-02T10:58:03.152Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:58:03.376Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-ui-6-rate-a3-kept.png"
}
````

### User / tool · 2026-11-02T10:58:03.386Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:58:45.578Z

The screenshots match the JSON. The notice is clear right after confirm, the accepted rate row still shows a "Needs review" chip, and the reloaded page has no change wording on the gap card. Before writing the review file, I'll check every line reference and quote I plan to cite, since the review file can only be written once.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:58:48.392Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/archive && grep -n \"let gapNote\\|gap-change-note\\|btn-dismiss-gap-note\\|gapNote = \" app/frontend/timeline.js; echo ---; grep -rn \"Accept as noted\\|Kept in notes\\|Kept in the internal notes\\|Needs review\\\" *:\" app/frontend/*.js | head -8; echo ---; grep -n \"gap_changes\" app/backend/review.py; echo ---; cd /Users/arsis/zlayt-pm-project && grep -n \"Kept in the internal\\|Noted for the internal\\|acknowledge\" app/backend/present.py | head -5; echo ---; python3 -c \"import json;d=json.load(open('/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-sweep.out.json'));print([ (r['candidate'], bool(r['gap_changes'])) for r in d['rows']])\"",
 "description": "Verify line references and quotes for the review"
}
````

### User / tool · 2026-11-02T10:58:48.569Z

**tool result**
````
73:  let gapNote = null;   // {token, items: [sentence]}
77:    gapNote = changes.length ? { token: s.token, items: changes } : null;
95:    return el("section", { class: "notice notice--info", "data-testid": "gap-change-note", role: "status", "aria-label": "Gap figures changed" },
97:      el("button", { type: "button", class: "btn btn--sm", "data-testid": "btn-dismiss-gap-note", onclick: (ev) => { gapNote = null; ev.target.closest("section").remove(); } }, "Got it"));
---
app/frontend/charges.js:77:      !isCharge && (rs === "accepted") ? el("span", { class: "rv-noted" }, "Kept in the internal notes only; not in the letter or the total.") : null,
app/frontend/review.js:233:    const acceptText = accepted ? (noted ? "Kept in notes" : st === "edited" ? "Edited" : "Accepted") : noted ? "Keep in notes" : "Accept";
---
353:    gap_changes = []
354:    removed += _recompute_gaps(conn, case_id, t, gap_changes)
355:    for ch in gap_changes:
363:            "removed_flag_ids": removed, "gap_changes": gap_changes,
400:def _gap_changes(old: dict, new: dict) -> list:
471:        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
---
58:    """What Accept does to an amount (T-114): `letter_total` (a charge: counted in the billed-charges total), `acknowledge` (a rate: noted in the internal notes only,
60:    return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")
---
[('2026-03-05', True), ('2026-05-03', False)]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:58:50.380Z

Line references check out. Next I'll see how the board validator reads a review file, so I can test the JSON block before the one allowed write.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:58:50.785Z

**tool call — Bash**
````
{
 "command": "grep -n \"validate\" tools/board.py | head -20",
 "description": "Find the board validate command implementation"
}
````

### User / tool · 2026-11-02T10:58:50.881Z

**tool result**
````
740:    errs = validate_review_file(rp)
896:def validate_review_file(p: Path) -> list[str]:
927:def cmd_validate(a):
949:            errors += [f"{rel}: {e}" for e in validate_review_file(p)]
1119:    s = sub.add_parser("validate"); s.add_argument("path", nargs="?"); s.set_defaults(fn=cmd_validate)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:58:51.887Z

**tool call — Bash**
````
{
 "command": "sed -n 896,952p tools/board.py",
 "description": "Read the review file validator rules"
}
````

### User / tool · 2026-11-02T10:58:51.967Z

**tool result**
````
def validate_review_file(p: Path) -> list[str]:
    errs = []
    if p.name.startswith("GATE-") or p.name.startswith("CONTRACT-"):
        if len(p.read_text(encoding="utf-8").strip()) < 50:
            errs.append("gate summary is empty")
        return errs
    d = review_json(p)
    if d is None:
        return ["review must contain a ```json block (Appendix D.2) with a verdict"]
    for k in ("card", "persona", "verdict", "findings", "exercised"):
        if k not in d:
            errs.append(f"review JSON missing '{k}'")
    if d.get("verdict") not in VERDICTS:
        errs.append(f"verdict must be one of {VERDICTS}")
    if not isinstance(d.get("findings"), list):
        return ["review JSON 'findings' must be a list (use [] for none)"]
    sev = [f.get("severity") for f in d.get("findings", []) if isinstance(f, dict)]
    for f in d.get("findings", []):
        if not isinstance(f, dict) or f.get("severity") not in ("blocker", "major", "minor", "nit"):
            errs.append(f"finding has bad severity: {str(f)[:80]}")
        elif not f.get("evidence"):
            errs.append(f"finding without evidence: {f.get('title')}")
    if "blocker" in sev and d.get("verdict") != "fail":
        errs.append("a blocker finding requires verdict 'fail' (§7.4)")
    elif "major" in sev and "blocker" not in sev and d.get("verdict") != "changes":
        errs.append("a major finding (no blockers) requires verdict 'changes' (§7.4)")
    if not d.get("exercised"):
        errs.append("'exercised' is empty — a review that didn't exercise the artifact is invalid")
    return errs


def cmd_validate(a):
    targets = [Path(a.path)] if a.path else sorted(CARDS.glob("T-*.md"))
    errors = []
    shadow = _read_shadow()
    for t in targets:
        p = t if t.is_absolute() else (Path.cwd() / t)
        if not p.exists() and not t.is_absolute() and (ROOT / t).exists():
            p = ROOT / t
        p = Path(os.path.realpath(p))
        if not p.exists():
            errors.append(f"{t}: no such file")
            continue
        try:
            rel = p.relative_to(Path(os.path.realpath(ROOT)))
        except ValueError:
            errors.append(f"{t}: not inside the project")
            continue
        if not rel.parts or rel.parts[0] not in ("board", "reviews"):
            errors.append(f"{t}: not a board or review file")
            continue
        parts = rel.parts
        if parts[0] == "reviews" and p.suffix == ".md":
            errors += [f"{rel}: {e}" for e in validate_review_file(p)]
        elif parts[:2] == ("board", "cards") and p.suffix == ".md":
            try:
                meta, body = parse(p.read_text(encoding="utf-8"), str(rel))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:59:17.125Z

The validator only reads files under `reviews/`, so I'll check the JSON with my own script first. I'm writing a draft JSON block to review-evidence, checking it against the validator rules and the paperwork-repeat count in the card text, then the single Write.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:59:29.809Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-draft.json",
 "content": "{\"card\": \"T-114\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git archive HEAD = e1ce8dc620e6ec0778320456ac79a25f1832bfee (T-060 r3 commits c8e36fb and 5d975ed are ancestors), extracted to the session scratchpad t114r2/archive; app http://127.0.0.1:7881 (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch DB, PID 51899, stopped at the end); sample case: library case_lib09_spanish_interpreter_espalda, plus the 15 library packets for the confirm-date sweep\",\n \"exercised\": [\n  \"git rev-parse HEAD printed e1ce8dc620e6ec0778320456ac79a25f1832bfee; git merge-base --is-ancestor c8e36fb HEAD and 5d975ed HEAD both printed as ancestors\",\n  \"git archive HEAD into the scratchpad; grep gap_changes in the archive: app/frontend/timeline.js and app/backend/review.py\",\n  \"server from the archive on 127.0.0.1:7881 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, ZLAYT_DB in scratchpad); GET / returned 200\",\n  \"artifacts/review-evidence/T-114-r2-paralegal-probe.py: lib09 dates_to_confirm r4 candidates 2026-03-05 and 2026-05-03 (suggested 2026-05-03); gap flag 42 days r1 to r2\",\n  \"artifacts/review-evidence/T-114-r2-paralegal-sweep.py: all 15 library packets; 2 confirm attempts (both lib09 r4); 2026-03-05 returns gap_changes 42 to 40, 2026-05-03 returns none\",\n  \"artifacts/review-evidence/T-114-r2-paralegal-ui-gap.py (Playwright, Chromium, 1440x900): confirm r4 as 2026-03-05 in the Dates to confirm form; read the gap-change notice text and its viewport position; scroll to top; Got it; reload; accept rate a3 on a second load\",\n  \"artifacts/review-evidence/T-114-r2-paralegal-checks2.py: full gap card text after confirm and after reload; rate a3 chips and Kept in notes control; FIXTURE_MISS rows in the scratch DB\",\n  \"sqlite3 on the scratch DB: SELECT c.name, COUNT(*) FROM llm_calls l JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY c.name printed 'case lib01 er only then gap|1'\",\n  \"read app/frontend/timeline.js:73, 77, 95, 97 (gapNote in memory; Got it clears it); app/frontend/review.js:233; app/frontend/charges.js:77; app/backend/review.py:353-364 and 400\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"verify_quickly\": 3, \"gap_change_notice_at_confirm\": 4, \"gap_change_on_card_after_reload\": 2, \"rate_row_clarity\": 3},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"The gap-change notice lives only in page memory; after Got it or a reload the gap card does not say the figure changed\",\n   \"evidence\": \"artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json steps.after_confirm.note_text = 'A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42). Got it'; steps.after_dismiss.note_count 0; steps.after_reload.note_count 0 with body_has_recalc false and body_has_was_42 false. artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json card_full_after_reload begins 'Gap of 40 days Needs review Gap of 40 days between March 5, 2026' and card_has_was_or_recalc_after_reload is false; the only 42 on the card is 'the gap would be 42 days (March 3, 2026 to April 14, 2026)' in the paperwork sentence. app/frontend/timeline.js:73 (let gapNote = null), timeline.js:97 (Got it sets gapNote = null and removes the node). Screenshots: artifacts/review-evidence/T-114-r2-ui-2-after-confirm.png, artifacts/review-evidence/T-114-r2-ui-4-after-reload.png.\",\n   \"why_it_matters\": \"Round 1 asked that a figure which changes after a decision say so beside the gap flag and in the flags tray (acceptance test: the gap flag card shows 'Gap recalculated after you confirmed record 4: now 40 days (was 42).'). At e1ce8dc the notice appears at the moment of confirm and is clear, but a paralegal who clicks Got it, reloads, or comes back later sees 40 days with no reason it moved. The card's only 42 means something else (what the gap would be if record 4 is paperwork). The adjuster counts days between encounters and asks why a number changed; the paralegal needs the answer after the banner is gone. The round-1 acceptance test is not met.\",\n   \"fix\": \"Show the change on the gap flag card from data the case keeps (the old and new days and the confirmed record), not from page memory: one line under the title such as 'Changed after you confirmed record 4: now 40 days (was 42).' It stays until the gap changes again. The banner may stay as the immediate announcement, but dismissing it must not remove the line from the card.\",\n   \"acceptance_test\": \"lib09: confirm record 4 as 2026-03-05, then reload the page. The element flag-f_gap_r4_r2 contains 'now 40 days (was 42)' and 'March 5, 2026'. Repeat after clicking Got it on the banner.\"},\n  {\"severity\": \"minor\", \"title\": \"An accepted rate row still shows a Needs review chip beside Accepted\",\n   \"evidence\": \"artifacts/review-evidence/T-114-r2-ui-6-rate-a3-kept.png; artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json rate_a3_chips ['Needs review', 'Accepted'] and rate_a3_needs_review_text_count 1. Fixed part: artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json steps.rate_a3_after.has_accept_as_noted 0; the control is now 'Kept in notes' (app/frontend/review.js:233) with Undo, and the text 'Kept in the internal notes only; not in the letter or the total.' (app/frontend/charges.js:77).\",\n   \"why_it_matters\": \"The Accept as noted button that invited a second accept is gone, and the money side is unchanged. The chip still says Needs review on a row the paralegal has already decided, so the row contradicts itself and looks unfinished (the T-060 F6/F7 pattern). Round 1's acceptance test fails on the chip.\",\n   \"fix\": \"After acknowledge, drop the Needs review chip from the row and keep one status chip (Accepted or Noted). Keep the internal-notes sentence. The Kept in notes control is still enabled (is_disabled false); I did not click it. If it does nothing, it should not look like a button.\",\n   \"acceptance_test\": \"lib09, accept rate a3: the row contains no 'Needs review' text (count 0) and its status reads Accepted or Noted only.\"},\n  {\"severity\": \"nit\", \"title\": \"The lib01 extract step still misses its demo fixture on every run\",\n   \"evidence\": \"sqlite3 on the scratch DB, SELECT c.name, COUNT(*) FROM llm_calls l JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY c.name printed 'case lib01 er only then gap|1'. Row: step extract, attempt 1, parsed_ok 0, error 'FIXTURE_MISS 83bcee077841...'. Round 1 saw four such rows across its lib01 runs.\",\n   \"why_it_matters\": \"Nothing is lost (lib01 still stores its records), but the lib01 demo still runs on a logged fixture miss, the kind of demo dead end T-114 set out to close.\",\n   \"fix\": \"Record the lib01 extract response under tests/fixtures/llm/ (curated set), or note the fallback on the card.\",\n   \"acceptance_test\": \"A fixture-mode run of case_lib01 writes no FIXTURE_MISS row to llm_calls.\"},\n  {\"severity\": \"nit\", \"title\": \"The paperwork sentence appears twice in the lib09 gap card\",\n   \"evidence\": \"artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json card_full_after_reload: 'which looks like paperwork, not a visit' occurs twice; each occurrence is followed by the 'If record 4 ... the gap would be 42 days (March 3, 2026 to April 14, 2026)' sentence, with the 'Needs review: AI translation' text between them.\",\n   \"why_it_matters\": \"The gap card is where the paralegal checks the figure. A repeated sentence costs verification time and reads like a copy error. It is on the card this card touches, so I flag it here.\",\n   \"fix\": \"Render the paperwork note once in the gap card.\",\n   \"acceptance_test\": \"lib09 gap card after confirm of record 4: the text 'looks like paperwork' occurs once.\"}\n ],\n \"whats_right\": [\n  \"The notice right after confirm is in view (top at y 128 on a 900 px viewport), names record 4, gives both numbers ('now 40 days (was 42)'), and is announced in the status region.\",\n  \"The accepted rate row has no Accept as noted button and says 'Kept in the internal notes only; not in the letter or the total.'\",\n  \"The backend figure holds at e1ce8dc: confirming 2026-03-05 on lib09 returns gap_changes 42 to 40 with new start 2026-03-05; the suggested 2026-05-03 reading changes no gap (artifacts/review-evidence/T-114-r2-paralegal-sweep.out.json).\"\n ],\n \"questions_for_chris\": [\n  \"Still open from round 1: the lib09 gap card now says record 4 'looks like paperwork, not a visit', and the 40-day figure still starts there. T-060 F4 says an intake form is never an endpoint. Should an intake form ever be a gap endpoint? The number the adjuster sees depends on the answer. Whether the gap goes in the demand is litigation-lead's call.\"\n ]}\n"
}
````

### User / tool · 2026-11-02T10:59:29.917Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-draft.json (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:59:34.964Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-jsoncheck.py",
 "content": "\"\"\"T-114 r2 paralegal-reviewer pre-write check. Applies the board validator's rules (tools/board.py validate_review_file) to a draft JSON\nfile, and counts the quoted strings in the scratch evidence so the review text can be checked before its single Write.\nRun: .venv/bin/python -I artifacts/review-evidence/T-114-r2-paralegal-jsoncheck.py <draft.json>\n\"\"\"\nimport json\nimport os\nimport sys\n\nHERE = os.path.dirname(os.path.abspath(__file__))\nVERDICTS = (\"pass\", \"changes\", \"fail\")\ndraft = json.load(open(sys.argv[1], encoding=\"utf-8\"))\nerrs = []\nfor k in (\"card\", \"persona\", \"verdict\", \"findings\", \"exercised\"):\n    if k not in draft:\n        errs.append(f\"missing {k}\")\nif draft.get(\"verdict\") not in VERDICTS:\n    errs.append(\"bad verdict\")\nsev = [f.get(\"severity\") for f in draft[\"findings\"]]\nfor f in draft[\"findings\"]:\n    if f.get(\"severity\") not in (\"blocker\", \"major\", \"minor\", \"nit\"):\n        errs.append(f\"bad severity {f.get('title')}\")\n    elif not f.get(\"evidence\"):\n        errs.append(f\"no evidence {f.get('title')}\")\nif \"blocker\" in sev and draft[\"verdict\"] != \"fail\":\n    errs.append(\"blocker needs fail\")\nelif \"major\" in sev and \"blocker\" not in sev and draft[\"verdict\"] != \"changes\":\n    errs.append(\"major needs changes\")\nprint(\"findings\", {s: sev.count(s) for s in (\"blocker\", \"major\", \"minor\", \"nit\")}, \"verdict\", draft[\"verdict\"])\nprint(\"scores\", draft.get(\"scores\"))\nprint(\"exercised items\", len(draft[\"exercised\"]), \"whats_right items\", len(draft[\"whats_right\"]), \"questions\", len(draft[\"questions_for_chris\"]))\nprint(\"errors\", errs or \"none\")\n\nev = json.load(open(os.path.join(HERE, \"T-114-r2-paralegal-checks2.out.json\"), encoding=\"utf-8\"))\ncard = ev[\"card_full_after_reload\"]\nprint(\"paperwork sentence count in reloaded gap card:\", card.count(\"looks like paperwork\"))\nprint(\"'was 42' or 'recalculated' in reloaded gap card:\", (\"was 42\" in card) or (\"recalculated\" in card))\nprint(\"'Needs review' text count on rate a3:\", ev[\"rate_a3_needs_review_text_count\"])\nui = json.load(open(os.path.join(HERE, \"T-114-r2-paralegal-ui-gap.out.json\"), encoding=\"utf-8\"))\nprint(\"note text after confirm:\", ui[\"steps\"][\"after_confirm\"][\"note_text\"])\nprint(\"note top y after confirm:\", ui[\"steps\"][\"after_confirm\"][\"note_box\"][\"y\"], \"in viewport:\", ui[\"steps\"][\"after_confirm\"][\"note_in_viewport\"])\n"
}
````

### User / tool · 2026-11-02T10:59:35.096Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-r2-paralegal-jsoncheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:59:36.223Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-114-r2-paralegal-jsoncheck.py artifacts/review-evidence/T-114-r2-paralegal-draft.json",
 "description": "Check the draft review JSON against validator rules and evidence"
}
````

### User / tool · 2026-11-02T10:59:36.339Z

**tool result**
````
findings {'blocker': 0, 'major': 1, 'minor': 1, 'nit': 2} verdict changes
scores {'verify_quickly': 3, 'gap_change_notice_at_confirm': 4, 'gap_change_on_card_after_reload': 2, 'rate_row_clarity': 3}
exercised items 9 whats_right items 3 questions 1
errors none
paperwork sentence count in reloaded gap card: 2
'was 42' or 'recalculated' in reloaded gap card: False
'Needs review' text count on rate a3: 1
note text after confirm: A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42). Got it
note top y after confirm: 128 in viewport: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:59:41.181Z

The draft passes the validator rules and matches the evidence: 1 major, 1 minor, 2 nits, verdict changes, and the paperwork sentence appears twice. Now the single Write of the review file.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:05.320Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-114-paralegal-r2.md",
 "content": "# T-114 r2 review: paralegal-reviewer (Maria Delgado persona)\n\nVerdict: **changes** (0 blockers, 1 major, 1 minor, 2 nits). The gap-change notice now appears when a date is confirmed and names both numbers, but it is held only in page memory. After Got it or a reload the gap card reads \"Gap of 40 days\" with no reason, so the round-1 major is still open. The round-1 minor is partly fixed: the \"Accept as noted\" button is gone, but an accepted rate row still shows a \"Needs review\" chip. The round-1 nit (lib01 fixture miss) is still there.\n\nThe scope is HEAD, not b5fb35c. HEAD is e1ce8dc, which includes the T-060 r3 frontend commits (c8e36fb, 5d975ed), so the round-1 \"no UI consumer\" finding had to be re-tested on the committed code.\n\n## Round-1 items\n\n| Round-1 item | Status at e1ce8dc | Evidence |\n|---|---|---|\n| Major: gap change must show in the UI | Partly. Banner at confirm: yes. Gap card and after reload: no. | artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json; artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json |\n| Minor: accepted rate row reads unfinished | Partly. \"Accept as noted\" gone; \"Needs review\" chip still on the row. | artifacts/review-evidence/T-114-r2-ui-6-rate-a3-kept.png |\n| Nit: lib01 extract misses its fixture | Still open. One FIXTURE_MISS row for case lib01. | sqlite3 query output in the exercised list |\n\n## What I ran\n\nDeterministic first.\n\n- `git rev-parse HEAD` printed `e1ce8dc620e6ec0778320456ac79a25f1832bfee`. `git merge-base --is-ancestor c8e36fb HEAD` and the same for `5d975ed` both succeeded.\n- `git archive HEAD` extracted to the session scratchpad `t114r2/archive`. `grep -rln gap_changes app/frontend app/backend` returned `app/frontend/timeline.js` and `app/backend/review.py`.\n- Server from the archive: `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local HOST=127.0.0.1 PORT=7881`, ZLAYT_DB in the scratchpad, PID 51899. `GET /` returned 200. Stopped by PID at the end. The team app on 7860 was not touched.\n\nLive checks. Scripts are in `artifacts/review-evidence/`, run with `.venv/bin/python` (`-I` for the JSON check).\n\n- `T-114-r2-paralegal-probe.py`: lib09 has one date to confirm (record 4, \"03/05/2026\"), candidates 2026-03-05 and 2026-05-03, suggested 2026-05-03. The gap is 42 days, record 1 to record 2.\n- `T-114-r2-paralegal-sweep.py` (out: `T-114-r2-paralegal-sweep.out.json`): all 15 library packets, fresh cases. Two confirm attempts in total, both lib09 record 4. Confirming 2026-03-05 returns `gap_changes` 42 to 40 (new start 2026-03-05). Confirming 2026-05-03 returns none.\n- `T-114-r2-paralegal-ui-gap.py` (Playwright, Chromium, 1440x900; out: `T-114-r2-paralegal-ui-gap.out.json`): confirmed record 4 as 2026-03-05 in the Dates to confirm form, read the banner text and position, scrolled to top, clicked Got it, reloaded, then accepted rate a3 on a second load.\n- `T-114-r2-paralegal-checks2.py` (out: `T-114-r2-paralegal-checks2.out.json`): full gap-card text after confirm and after reload, rate a3 chips and the Kept in notes control, FIXTURE_MISS rows.\n- `sqlite3` on the scratch DB: `SELECT c.name, COUNT(*) FROM llm_calls l JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY c.name;` printed `case lib01 er only then gap|1`. The same query without the join printed `1`.\n- `T-114-r2-paralegal-jsoncheck.py` on the draft JSON: `findings {'blocker': 0, 'major': 1, 'minor': 1, 'nit': 2} verdict changes`, `errors none`, `paperwork sentence count in reloaded gap card: 2`, `'was 42' or 'recalculated' in reloaded gap card: False`.\n\nCode read at HEAD: `app/frontend/timeline.js:73, 77, 95, 97`; `app/frontend/review.js:233`; `app/frontend/charges.js:77`; `app/backend/review.py:353-364, 400`.\n\nNot exercised: I did not click \"Kept in notes\" or Undo on the rate row. I did not walk the 30 exports or the 7 refusals again (round 1 covered them, and this round's scope is the notice and the minors). The working tree has uncommitted changes (for example `app/backend/api.py` and `app/backend/pipeline.py` in `git status --short`), so this review covers the HEAD archive only.\n\n## Findings\n\n### Major: the gap-change notice lives only in page memory; after Got it or a reload the gap card does not say the figure changed\n\nEvidence: `artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json` steps.after_confirm.note_text is \"A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42). Got it\". steps.after_dismiss.note_count is 0. steps.after_reload.note_count is 0, body_has_recalc is false and body_has_was_42 is false. `artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json` card_full_after_reload begins \"Gap of 40 days Needs review Gap of 40 days between March 5, 2026\", and the check reports no \"was 42\" or \"recalculated\" on the card. The only 42 on the card is in the paperwork sentence: \"the gap would be 42 days (March 3, 2026 to April 14, 2026)\". Source: `app/frontend/timeline.js:73` (`let gapNote = null`) and `timeline.js:97` (Got it clears it). Screenshots: `artifacts/review-evidence/T-114-r2-ui-2-after-confirm.png` and `artifacts/review-evidence/T-114-r2-ui-4-after-reload.png`.\n\nWhy it matters: round 1 asked that a figure which changes after a decision say so beside the gap flag and in the flags tray. Its acceptance test was that the gap flag card shows \"Gap recalculated after you confirmed record 4: now 40 days (was 42).\" At e1ce8dc the notice is clear at the moment of confirm, but a paralegal who clicks Got it, reloads, or comes back later sees 40 days with no reason it moved. The adjuster counts days between encounters and asks why a number changed. The round-1 acceptance test is not met.\n\nFix: show the change on the gap flag card from data the case keeps (the old and new days and the confirmed record), not from page memory. One line under the title, for example \"Changed after you confirmed record 4: now 40 days (was 42).\" It stays until the gap changes again. The banner may stay as the immediate announcement, but dismissing it must not remove the line from the card.\n\nAcceptance test: lib09, confirm record 4 as 2026-03-05, then reload. The element `flag-f_gap_r4_r2` contains \"now 40 days (was 42)\" and \"March 5, 2026\". Repeat after clicking Got it on the banner.\n\n### Minor: an accepted rate row still shows a \"Needs review\" chip beside \"Accepted\"\n\nEvidence: `artifacts/review-evidence/T-114-r2-ui-6-rate-a3-kept.png`. `artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json` rate_a3_chips is [\"Needs review\", \"Accepted\"], and rate_a3_needs_review_text_count is 1. Fixed part: `artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json` steps.rate_a3_after.has_accept_as_noted is 0. The control is now \"Kept in notes\" (`app/frontend/review.js:233`) with Undo, and the text reads \"Kept in the internal notes only; not in the letter or the total.\" (`app/frontend/charges.js:77`).\n\nWhy it matters: the Accept as noted button that invited a second accept is gone, and the money side is unchanged. The chip still says Needs review on a row the paralegal has already decided, so the row contradicts itself and looks unfinished (the T-060 F6/F7 pattern). Round 1's acceptance test fails on the chip.\n\nFix: after acknowledge, drop the Needs review chip and keep one status chip (Accepted or Noted). Keep the internal-notes sentence. The Kept in notes control is still enabled (is_disabled false). I did not click it; if it does nothing, it should not look like a button.\n\nAcceptance test: lib09, accept rate a3. The row contains no \"Needs review\" text (count 0), and its status reads Accepted or Noted only.\n\n### Nit: the lib01 extract step still misses its demo fixture on every run\n\nEvidence: the sqlite3 query in the exercised list printed `case lib01 er only then gap|1`. The row is step extract, attempt 1, parsed_ok 0, error \"FIXTURE_MISS 83bcee077841...\". Round 1 saw four such rows across its lib01 runs.\n\nWhy it matters: nothing is lost (lib01 still stores its records), but the lib01 demo still runs on a logged fixture miss, the kind of demo dead end T-114 set out to close.\n\nFix: record the lib01 extract response under `tests/fixtures/llm/` (curated set), or note the fallback on the card.\n\nAcceptance test: a fixture-mode run of case_lib01 writes no FIXTURE_MISS row to llm_calls.\n\n### Nit: the paperwork sentence appears twice in the lib09 gap card\n\nEvidence: `artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json` card_full_after_reload. \"which looks like paperwork, not a visit\" occurs twice (the jsoncheck count is 2). Each occurrence is followed by \"If record 4 ... the gap would be 42 days (March 3, 2026 to April 14, 2026)\", with the \"Needs review: AI translation\" text between them.\n\nWhy it matters: the gap card is where the paralegal checks the figure. A repeated sentence costs verification time and reads like a copy error. It sits on the card this card touches, so I flag it here.\n\nFix: render the paperwork note once in the gap card.\n\nAcceptance test: lib09 gap card after confirming record 4: the text \"looks like paperwork\" occurs once.\n\n## Right already\n\n- The notice right after confirm is in view (top at y 128 on a 900 px viewport), names record 4, gives both numbers (\"now 40 days (was 42)\"), and is announced in the status region.\n- The accepted rate row has no Accept as noted button and says \"Kept in the internal notes only; not in the letter or the total.\"\n- The backend figure holds at e1ce8dc: confirming 2026-03-05 on lib09 returns gap_changes 42 to 40 with new start 2026-03-05. The suggested 2026-05-03 reading changes no gap (`artifacts/review-evidence/T-114-r2-paralegal-sweep.out.json`).\n\n## Questions for Chris\n\nStill open from round 1: the lib09 gap card now says record 4 \"looks like paperwork, not a visit\", and the 40-day figure still starts there. T-060 F4 says an intake form is never an endpoint. Should an intake form ever be a gap endpoint? The number the adjuster sees depends on the answer. Whether the gap goes in the demand is litigation-lead's call.\n\n```json\n{\"card\": \"T-114\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git archive HEAD = e1ce8dc620e6ec0778320456ac79a25f1832bfee (T-060 r3 commits c8e36fb and 5d975ed are ancestors), extracted to the session scratchpad t114r2/archive; app http://127.0.0.1:7881 (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch DB, PID 51899, stopped at the end); sample case: library case_lib09_spanish_interpreter_espalda, plus the 15 library packets for the confirm-date sweep\",\n \"exercised\": [\n  \"git rev-parse HEAD printed e1ce8dc620e6ec0778320456ac79a25f1832bfee; git merge-base --is-ancestor c8e36fb HEAD and 5d975ed HEAD both printed as ancestors\",\n  \"git archive HEAD into the scratchpad; grep gap_changes in the archive: app/frontend/timeline.js and app/backend/review.py\",\n  \"server from the archive on 127.0.0.1:7881 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, ZLAYT_DB in scratchpad); GET / returned 200\",\n  \"artifacts/review-evidence/T-114-r2-paralegal-probe.py: lib09 dates_to_confirm r4 candidates 2026-03-05 and 2026-05-03 (suggested 2026-05-03); gap flag 42 days r1 to r2\",\n  \"artifacts/review-evidence/T-114-r2-paralegal-sweep.py: all 15 library packets; 2 confirm attempts (both lib09 r4); 2026-03-05 returns gap_changes 42 to 40, 2026-05-03 returns none\",\n  \"artifacts/review-evidence/T-114-r2-paralegal-ui-gap.py (Playwright, Chromium, 1440x900): confirm r4 as 2026-03-05 in the Dates to confirm form; read the gap-change notice text and its viewport position; scroll to top; Got it; reload; accept rate a3 on a second load\",\n  \"artifacts/review-evidence/T-114-r2-paralegal-checks2.py: full gap card text after confirm and after reload; rate a3 chips and Kept in notes control; FIXTURE_MISS rows in the scratch DB\",\n  \"sqlite3 on the scratch DB: SELECT c.name, COUNT(*) FROM llm_calls l JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY c.name printed 'case lib01 er only then gap|1'\",\n  \"read app/frontend/timeline.js:73, 77, 95, 97 (gapNote in memory; Got it clears it); app/frontend/review.js:233; app/frontend/charges.js:77; app/backend/review.py:353-364 and 400\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"verify_quickly\": 3, \"gap_change_notice_at_confirm\": 4, \"gap_change_on_card_after_reload\": 2, \"rate_row_clarity\": 3},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"The gap-change notice lives only in page memory; after Got it or a reload the gap card does not say the figure changed\",\n   \"evidence\": \"artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json steps.after_confirm.note_text = 'A gap figure changed. Gap recalculated after you confirmed record 4: now 40 days (was 42). Got it'; steps.after_dismiss.note_count 0; steps.after_reload.note_count 0 with body_has_recalc false and body_has_was_42 false. artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json card_full_after_reload begins 'Gap of 40 days Needs review Gap of 40 days between March 5, 2026' and card_has_was_or_recalc_after_reload is false; the only 42 on the card is 'the gap would be 42 days (March 3, 2026 to April 14, 2026)' in the paperwork sentence. app/frontend/timeline.js:73 (let gapNote = null), timeline.js:97 (Got it sets gapNote = null and removes the node). Screenshots: artifacts/review-evidence/T-114-r2-ui-2-after-confirm.png, artifacts/review-evidence/T-114-r2-ui-4-after-reload.png.\",\n   \"why_it_matters\": \"Round 1 asked that a figure which changes after a decision say so beside the gap flag and in the flags tray (acceptance test: the gap flag card shows 'Gap recalculated after you confirmed record 4: now 40 days (was 42).'). At e1ce8dc the notice appears at the moment of confirm and is clear, but a paralegal who clicks Got it, reloads, or comes back later sees 40 days with no reason it moved. The card's only 42 means something else (what the gap would be if record 4 is paperwork). The adjuster counts days between encounters and asks why a number changed; the paralegal needs the answer after the banner is gone. The round-1 acceptance test is not met.\",\n   \"fix\": \"Show the change on the gap flag card from data the case keeps (the old and new days and the confirmed record), not from page memory: one line under the title such as 'Changed after you confirmed record 4: now 40 days (was 42).' It stays until the gap changes again. The banner may stay as the immediate announcement, but dismissing it must not remove the line from the card.\",\n   \"acceptance_test\": \"lib09: confirm record 4 as 2026-03-05, then reload the page. The element flag-f_gap_r4_r2 contains 'now 40 days (was 42)' and 'March 5, 2026'. Repeat after clicking Got it on the banner.\"},\n  {\"severity\": \"minor\", \"title\": \"An accepted rate row still shows a Needs review chip beside Accepted\",\n   \"evidence\": \"artifacts/review-evidence/T-114-r2-ui-6-rate-a3-kept.png; artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json rate_a3_chips ['Needs review', 'Accepted'] and rate_a3_needs_review_text_count 1. Fixed part: artifacts/review-evidence/T-114-r2-paralegal-ui-gap.out.json steps.rate_a3_after.has_accept_as_noted 0; the control is now 'Kept in notes' (app/frontend/review.js:233) with Undo, and the text 'Kept in the internal notes only; not in the letter or the total.' (app/frontend/charges.js:77).\",\n   \"why_it_matters\": \"The Accept as noted button that invited a second accept is gone, and the money side is unchanged. The chip still says Needs review on a row the paralegal has already decided, so the row contradicts itself and looks unfinished (the T-060 F6/F7 pattern). Round 1's acceptance test fails on the chip.\",\n   \"fix\": \"After acknowledge, drop the Needs review chip and keep one status chip (Accepted or Noted). Keep the internal-notes sentence. The Kept in notes control is still enabled (is_disabled false); I did not click it. If it does nothing, it should not look like a button.\",\n   \"acceptance_test\": \"lib09, accept rate a3: the row contains no 'Needs review' text (count 0) and its status reads Accepted or Noted only.\"},\n  {\"severity\": \"nit\", \"title\": \"The lib01 extract step still misses its demo fixture on every run\",\n   \"evidence\": \"sqlite3 on the scratch DB, SELECT c.name, COUNT(*) FROM llm_calls l JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY c.name printed 'case lib01 er only then gap|1'. Row: step extract, attempt 1, parsed_ok 0, error 'FIXTURE_MISS 83bcee077841...'. Round 1 saw four such rows across its lib01 runs.\",\n   \"why_it_matters\": \"Nothing is lost (lib01 still stores its records), but the lib01 demo still runs on a logged fixture miss, the kind of demo dead end T-114 set out to close.\",\n   \"fix\": \"Record the lib01 extract response under tests/fixtures/llm/ (curated set), or note the fallback on the card.\",\n   \"acceptance_test\": \"A fixture-mode run of case_lib01 writes no FIXTURE_MISS row to llm_calls.\"},\n  {\"severity\": \"nit\", \"title\": \"The paperwork sentence appears twice in the lib09 gap card\",\n   \"evidence\": \"artifacts/review-evidence/T-114-r2-paralegal-checks2.out.json card_full_after_reload: 'which looks like paperwork, not a visit' occurs twice; each occurrence is followed by the 'If record 4 ... the gap would be 42 days (March 3, 2026 to April 14, 2026)' sentence, with the 'Needs review: AI translation' text between them.\",\n   \"why_it_matters\": \"The gap card is where the paralegal checks the figure. A repeated sentence costs verification time and reads like a copy error. It is on the card this card touches, so I flag it here.\",\n   \"fix\": \"Render the paperwork note once in the gap card.\",\n   \"acceptance_test\": \"lib09 gap card after confirm of record 4: the text 'looks like paperwork' occurs once.\"}\n ],\n \"whats_right\": [\n  \"The notice right after confirm is in view (top at y 128 on a 900 px viewport), names record 4, gives both numbers ('now 40 days (was 42)'), and is announced in the status region.\",\n  \"The accepted rate row has no Accept as noted button and says 'Kept in the internal notes only; not in the letter or the total.'\",\n  \"The backend figure holds at e1ce8dc: confirming 2026-03-05 on lib09 returns gap_changes 42 to 40 with new start 2026-03-05; the suggested 2026-05-03 reading changes no gap (artifacts/review-evidence/T-114-r2-paralegal-sweep.out.json).\"\n ],\n \"questions_for_chris\": [\n  \"Still open from round 1: the lib09 gap card now says record 4 'looks like paperwork, not a visit', and the 40-day figure still starts there. T-060 F4 says an intake form is never an endpoint. Should an intake form ever be a gap endpoint? The number the adjuster sees depends on the answer. Whether the gap goes in the demand is litigation-lead's call.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T11:00:05.474Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-114-paralegal-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:07.952Z

The review file is written. Next I'll run the board validator on it, a read-only check.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:08.402Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-114-paralegal-r2.md",
 "description": "Validate the round-2 review file with the board validator"
}
````

### User / tool · 2026-11-02T11:00:08.543Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:09.691Z

**tool call — Bash**
````
{
 "command": "kill 51899; sleep 1; curl -s -o /dev/null -w \"7881 after stop: %{http_code}\\n\" http://127.0.0.1:7881/; curl -s -o /dev/null -w \"7860 team app: %{http_code}\\n\" http://127.0.0.1:7860/",
 "description": "Stop the scratch server by PID and confirm ports"
}
````

### User / tool · 2026-11-02T11:00:10.810Z

**tool result**
````
7881 after stop: 200
7860 team app: 200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:12.421Z

Port 7881 still answers after the kill, so I'll check whether PID 51899 is still alive and what holds the port.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:12.920Z

**tool call — Bash**
````
{
 "command": "ps -p 51899 -o pid,ppid,stat,command 2>&1; echo \"---\"; lsof -iTCP:7881 -sTCP:LISTEN -nP 2>&1 | head -5",
 "description": "Check whether the scratch server PID is still alive and who listens on 7881"
}
````

### User / tool · 2026-11-02T11:00:13.098Z

**tool result**
````
  PID  PPID STAT COMMAND
---
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  51901 arsis    9u  IPv4 0x37318231dec3a5f2      0t0  TCP 127.0.0.1:7881 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:14.805Z

PID 51899 has exited, but its child 51901 is still listening on 7881. I'll confirm that child is this scratch server before stopping it by PID.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:15.238Z

**tool call — Bash**
````
{
 "command": "ps -p 51901 -o pid,ppid,stat,command 2>&1; lsof -p 51901 -a -d cwd -nP 2>/dev/null | tail -1",
 "description": "Identify the surviving listener process and its working directory"
}
````

### User / tool · 2026-11-02T11:00:15.385Z

**tool result**
````
  PID  PPID STAT COMMAND
51901     1 S    /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
Python  51901 arsis  cwd    DIR   1,18      672 235404279 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114r2/archive
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:16.668Z

The surviving process is the scratch server (cwd is the archive, `python -m app.main`), re-parented to launchd. Stopping it by PID now.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:17.255Z

**tool call — Bash**
````
{
 "command": "kill 51901; sleep 1; curl -s -o /dev/null -w \"7881 after stop: %{http_code}\\n\" http://127.0.0.1:7881/; lsof -iTCP:7881 -sTCP:LISTEN -nP 2>&1 | head -2; curl -s -o /dev/null -w \"7860 team app: %{http_code}\\n\" http://127.0.0.1:7860/",
 "description": "Stop the orphaned scratch server by PID and confirm ports"
}
````

### User / tool · 2026-11-02T11:00:18.446Z

**tool result**
````
7881 after stop: 000
7860 team app: 200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:21.291Z

The scratch server is stopped and the team app on 7860 is untouched. The review names only PID 51899, but the listener was 51901, so I'll correct both places in the review file.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:22.171Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-114-paralegal-r2.md",
 "old_string": "ZLAYT_DB in the scratchpad, PID 51899. `GET /` returned 200. Stopped by PID at the end.",
 "new_string": "ZLAYT_DB in the scratchpad, launcher PID 51899 and listener PID 51901 (the listener was re-parented to launchd after the launcher exited). `GET /` returned 200. Both stopped by PID at the end; 7881 then returned 000."
}
````

### User / tool · 2026-11-02T11:00:22.231Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-114-paralegal-r2.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:22.724Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-114-paralegal-r2.md",
 "old_string": "scratch DB, PID 51899, stopped at the end)",
 "new_string": "scratch DB, launcher PID 51899 and listener PID 51901, both stopped at the end)"
}
````

### User / tool · 2026-11-02T11:00:22.774Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-114-paralegal-r2.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:26.229Z

The Edit was refused because reviews are append-only, so the PID detail stays as written and I'll disclose it in my reply. Next I'll update my memory with the round-2 patterns.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:31.403Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t114-rates-gap-patterns.md",
 "content": "---\nname: t114-rates-gap-patterns\ndescription: T-114 r1 (b5fb35c) and r2 (e1ce8dc) reviews: gap-change notice is page-memory only and not on the gap card; accepted rate row keeps a Needs review chip; lib09 still 42 to 40; intake-form endpoint is Chris's call\nmetadata:\n  type: project\n---\n\nT-114 history. r1 (b5fb35c, verdict changes: 1 major, 1 minor, 1 nit). r2 (e1ce8dc, verdict changes: 1 major, 1 minor, 2 nits; review file reviews/T-114-paralegal-r2.md).\n\n- Accepting a lib09 rate is `accept_effect` acknowledge and `judge_required_for_export` false (present.py:57-66, trace.py:792-795). Never in the total, never blocks export. Still true at e1ce8dc.\n- All 15 library packets exported with zero JUDGE_NOT_RUN in both date variants at b5fb35c (r1). At e1ce8dc a fresh sweep of 15 packets found only 2 confirm attempts (both lib09 record 4).\n- lib09 record 4 (\"03/05/2026\", suggested 2026-05-03, candidate 2026-03-05): confirming 2026-03-05 gives gap_changes 42 to 40 at e1ce8dc. The T-116 note in the card (\"may now read 42 to 42\") was wrong. The 2026-05-03 candidate changes no gap.\n- r2 round-1 major (gap change visible in UI): PARTLY fixed at e1ce8dc. The banner `[data-testid=\"gap-change-note\"]` appears on confirm, is in view, and reads \"now 40 days (was 42)\". It lives in `gapNote` (timeline.js:73) and is cleared by Got it (timeline.js:97) or a reload. The gap card (`flag-f_gap_r4_r2`) never carries \"was 42\" or \"recalculated\"; after reload its only 42 is the paperwork sentence (\"would be 42 days\").\n- r2 round-1 minor (rate row): PARTLY fixed. \"Accept as noted\" gone; \"Kept in notes\" + Undo added; the accepted row still shows a \"Needs review\" chip beside \"Accepted\".\n- r2 round-1 nit (lib01 FIXTURE_MISS): still present, one row per lib01 run.\n- r2 new nit: the paperwork sentence appears twice in the lib09 gap card.\n\n**Why:** the intake form (record 4, \"formulario de admision\") is classified kind encounter with a date null in the golden, so once confirmed it is an endpoint. The card now says \"looks like paperwork, not a visit\" and still counts it. That is Chris's decision (T-060 F4 says intake forms are never endpoints). Not a must_not_flag violation; N1 is scoped to ambiguous dates. Also: evals/golden/check_golden.py:259 computes exclusions at ingest only.\n\n**How to apply:** when checking a gap change, read the card text after a reload, not only the banner. A banner is not persistence. When a card says a figure is \"now\" N, confirm the card says what it was before. The intake-form question goes to questions_for_chris, not to a finding. Related: [[golden-set-recurring-findings]], [[t060-ui-polish-patterns]], [[reviewer-tooling-quirks]].\n"
}
````

### User / tool · 2026-11-02T11:00:31.499Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t114-rates-gap-patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:31.748Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T11:00:31.755Z

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
14	- [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — r3 fail; r4 fail (warning gated by text regex); r5 (f8f358e) changes: same-day and header-list gaps in baseline wording
15	- [T-118 lib11 truth patterns](t118-lib11-truth-patterns.md) — validators pass on the wrong truth; record lists unguarded; intake form as phone_note stand-in; stale library-latest.md
16	- [T-060 UI polish patterns](t060-ui-polish-patterns.md) — pass 2 open items; reuse q0-q13 scripts; recount severities before the single Write
17	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:33.313Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-114 rates and gap patterns](t114-rates-gap-patterns.md) — rate acknowledge-only passes; gap change API-only in HEAD; intake-form encounter kind is Chris's call; golden N1 scoped to ambiguous",
 "new_string": "- [T-114 rates and gap patterns](t114-rates-gap-patterns.md) — r2 (e1ce8dc): gap notice is page-memory only, not on the gap card; rate row keeps Needs review chip; lib09 still 42 to 40"
}
````

### User / tool · 2026-11-02T11:00:33.451Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:35.283Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md",
 "old_string": "## T-116 r3 additions (2026-11-02)",
 "new_string": "## T-114 r2 additions (2026-11-02)\n- `nohup .venv/bin/python -m app.main ... &` then `kill $!` left the listener alive: the launcher PID exited, and the server\n  (a child, re-parented to launchd, ppid 1) kept 7881 open and returned 200. Always `lsof -iTCP:<port> -sTCP:LISTEN -nP` after a\n  kill, kill the listener PID too, and confirm `curl` returns 000. Name both PIDs in the review scope.\n- reviewer-write-guard refused an Edit on reviews/T-114-paralegal-r2.md (append-only). A wrong scope PID could not be fixed; it went into the final reply.\n  Before the single Write, check every PID, path and count with a command, not from memory.\n- The board validator only checks files under reviews/. Pre-check a draft JSON with a script in artifacts/review-evidence/ (T-114-r2-paralegal-jsoncheck.py).\n\n## T-116 r3 additions (2026-11-02)"
}
````

### User / tool · 2026-11-02T11:00:35.392Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:00:38.428Z

Verdict changes (0 blockers, 1 major, 1 minor, 2 nits); the round-1 gap-notice major is still open, since the notice vanishes on dismiss or reload and never appears on the gap card. Review: `/Users/arsis/zlayt-pm-project/reviews/T-114-paralegal-r2.md` (board validate ok).
Scratch server at e1ce8dc is stopped: launcher PID 51899 had exited, so I killed listener PID 51901 (7881 now 000, 7860 untouched); erratum, the review names only 51899 because the append-only guard refused the fix.
