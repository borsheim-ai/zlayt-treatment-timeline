# Subagent: T-114 review (haiku paralegal) (T-114 review (haiku paralegal))

Source: `agent-aa93b03e39c9c3e75.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T09:29:36.783Z

Review board card T-114 in /Users/arsis/zlayt-pm-project (commit b5fb35c). Read reviews/T-060-paralegal-pass1.md (the rate-row and gap-figure majors).

On a `git archive HEAD` copy in your scratchpad, with your own server on a spare port (fixture backend, ZLAYT_MODE=local, ZLAYT_DB in your scratchpad), confirm:
- accepting a lib09 rate row means "acknowledged", never blocks export, and never adds to the total;
- every acceptable item on the demo library packets exports with no JUDGE_NOT_RUN;
- confirm_date returns gap_changes, e.g. lib09 going from 42 to 40 days.

Run tests/unit/test_t114_rates_and_demo_judges.py, then stop the server by PID. Write reviews/T-114-paralegal.md with a ```json block of real values: card, persona paralegal-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T09:29:38.951Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T09:29:38.958Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T09:29:39.159Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-060-paralegal-pass1.md"
}
````

### User / tool · 2026-11-02T09:29:39.288Z

**tool result**
````
1	# T-060 pass 1 — paralegal-reviewer (Maria Delgado persona)
2	
3	Verdict: **changes** (0 blockers, 5 majors, 8 minors). The trust machinery is better than most tools I use: every row has its quote, a sticky source pane highlights the excerpt, edits keep the original, batch accept has an Undo, and decisions survive a refresh. The weak part is the review flow: keyboard navigation breaks across panels, needs-review items are not first on the page, and the hand-off text is hidden. It reads as a careful prototype, not yet an enterprise tool.
4	
5	## What I ran
6	App: `git archive HEAD` (f187a30) copied into my scratchpad, `LLM_BACKEND=fixture FIXTURE_SET=curated`, port 7871 with `ZLAYT_MODE=local`, own SQLite file. A second instance on 7872 without `ZLAYT_MODE` showed the public landing (`21-public-landing.png`: no library wall, no case list). Both servers were stopped by PID (79540, 1598); curl to both ports then returned 000. Playwright, Chromium, 1440x900 (one pass at 1280x720). Scripts are `p0-*.py` to `p25-*.py` next to the screenshots in `artifacts/review-evidence/T-060-pass1/`. That folder is shared with the ux-designer's `ux-*` files; mine have no `ux-` prefix.
7	
8	### Task 1: case_01 (evals/golden/case_01_date_formats.txt), paste to export
9	- Route used: paste (1), Analyze click (1), then keys `j`, `Tab`, `Enter` (confirm "April 5, 2026"), `Shift+A`, `j`, `a` (the $310 charge), then Export click and Copy letter click. Total: 1 paste, 3 clicks, 6 keypresses. Script time to ready-to-export: 9.2 s, including about 5 s of fixed waits. Results were on screen at my 3.5 s check, so processing is not the cost. These are script numbers; I did not time a human reader.
10	- This route reviewed no row individually. `Shift+A` accepted all 8 entries in one keystroke. When I tried the honest way (read each row, accept each), keyboard-only in-order review was not possible: pressing `a` on row 1 moved focus to row 8, about 1,800 px away, skipping rows 2 to 7 (`12-after-advance.png`). In practice that is one click per row. I did not time that path.
11	- Clipboard check: Copy letter put 1,732 characters of plain text on the clipboard, no HTML, no markdown, and the status line said "Copied the treatment section." Saved as `task1-clipboard.txt`, letter and notes as `task1-export-letter.txt` and `task1-export-notes.txt`.
12	
13	### Task 2: library lib09 (Spanish), load to export
14	- 1 load click, 10 clicks in total, 17 keypresses, 0 pastes. Script time 19.5 s. Six of the 10 clicks were forced re-positioning clicks, because `j` and `a` cannot cross panels (F1). The first export attempt was blocked (F3) and I had to dismiss two rows I had just accepted. Letter and notes: `task2-export-letter.txt`, `task2-export-notes.txt`.
15	
16	### Also exercised
17	Edit with original kept (`20b-edit-saved.png`), reload mid-review (state kept, scroll lost), `o` open-record, "Export while nothing accepted", the stepper expanded in two states, and the unclear-amount, flag and dates-to-confirm panels.
18	
19	## Enterprise or prototype?
20	- **Information density:** prototype. Two timeline rows per screen, seven buttons per row, 11,133 px for a 7-record case (lib09), 5,271 px for 8 records in public mode. The chronology tools I use show a row per encounter, and a page of 10 or more rows fits on screen.
21	- **Review queue order:** does not make sense. The label says "Needs review first". The page lists verified rows first, the undated needs-review row sits below seven of them, and the keyboard queue follows yet another order (F1, F2).
22	- **HITL hand-offs:** the wording is good ("What you need to do: Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted."), but it is collapsed behind a "Show the checks" link, so I would never see it (F2).
23	- **Export fit:** the letter text is close to what I want to paste. The surrounding workflow (where Export is, no done cue, a small scrolling text box, no file download) is not (F8).
24	
25	## Findings
26	
27	### Major
28	
29	**F1. Keyboard review breaks across panels (checklist 15).** Evidence:
30	- `25a-lib09-first-j.png`: on lib09 the first `j` from a fresh page lands on the "$650.00 Unclear" charge at about 8,214 px down. It skips the 3 needs-review entries, the undated record and the 6 flags.
31	- Inside the charges panel `j` never leaves: 24 presses ended stuck on `a7` ($2,900.00) from press 5 on (`p16-task2-order.py` output).
32	- `25b-lib09-a-yank.png`: accepting needs-review entry e2 with `a` sends focus to the $650 charge, 6,000 px away, instead of the next needs-review entry e7.
33	- After confirming a date, focus drops to `<body>` in both tasks, so the next `j` starts over.
34	- From a fresh page `j` skips verified-but-unreviewed rows entirely.
35	- Code: `app/frontend/review.js:285` (panel walking, siloed), `:292` (first `j` uses `c.review.queue[0]`), `:299` (`advance: true`).
36	Why it matters: I cannot read and accept a case in order without the mouse, and the queue order is not the page order.
37	Fix: one linear queue in page order (needs-review entries, dates, flags, charges, then verified). `j`/`k` cross panels; `a`/`d` advance to the next unreviewed item in that order; after a date confirm, focus moves to that entry's Accept button.
38	Acceptance test: Playwright on lib09: after load press `j` and assert the focused item is the first needs-review entry; press `a` 3 times and assert focus visits e2, e7, e4 in that order; press `j` repeatedly and assert focus enters the flags panel and then the charges panel without a mouse event.
39	
40	**F2. Needs-review items are not first, and the hand-off is hidden (checklist 16).** Evidence:
41	- `22b-public-timeline.png`: the order control says "Needs review first", yet the first row is a "Verified" green row. The only needs-review row (record 8, undated) sits in "Dates to confirm" below all seven verified rows (`01-after-analyze-full.png`).
42	- `04-stepper.png`: the summary bar reads "6/10 checks passed · 4 need you · Export blocked by 1" and does not say what to do. The instruction exists only inside the collapsed trace (`05-stepper-open.png`, "What you need to do: Choose the right reading under Dates to confirm…").
43	- In that trace the date decision has a red X, the same icon as a failure, though it is a normal paralegal decision.
44	Why it matters: the first screen after Analyze does not tell me what stops the export. "6/10 checks passed" is engineering language.
45	Fix: put a "To do" strip above the timeline that lists the open decisions in plain words and counts ("1 date to confirm", "1 flag", "1 charge"), each a link/button; render needs-review rows above verified rows; keep the 10-step trace as a secondary view; show a decision step in amber with a "your call" icon, not a red X.
46	Acceptance test: on case_01 the first element after Analyze (before any scroll) contains the text "Confirm the date for record 8" with a working jump control, and the first timeline row has state "Needs review". Same assertion on lib09 for its three needs-review entries.
47	
48	**F3. Accept is offered on items whose acceptance blocks export, and the recovery is a dead end (lib09).** Evidence:
49	- After I accepted everything, the bar read "8/10 checks passed · 2 need you · Export blocked by 2" (`18b-all-reviewed.png`, `19b-export-blocked.png`). The message: "You accepted this item, but the second AI check never ran on it… accepting does not replace it." The two items are the "$400.00 Rate" rows whose own card said "The second AI check did not run or did not finish" and which offered "Accept as noted".
50	- Clicking "Run the second check again for these 2" returned "The second check still did not answer for 2 items of 2. Try again, or dismiss them." (`19c-after-rerun.png`). The fixture backend never answers, so the only exit was to dismiss both rows.
51	Why it matters: I was told to accept, then punished for it, with no step that says "the AI check is missing, so this one cannot be accepted".
52	Fix: when the second check is absent, replace Accept with a disabled button plus the reason ("Can't accept: the second check hasn't run. Run it, or dismiss."); or accept it into the internal notes only and keep export unblocked. Name the check in plain words.
53	Acceptance test: on lib09 the two Rate rows show Accept disabled (or a different label) with the reason text; accepting every enabled item leaves "Ready to export".
54	
55	**F4. The gap number changes silently when a date is confirmed (checklist 6, trust).** Evidence: `25c-gap-42-before-confirm.png` shows "Gap of 42 days between March 3, 2026 (Quillmere Regional ED) and April 14, 2026". After I confirmed record 4 (an intake form, "formulario de admisión (OCR)") as March 5, `25e-gap-40-after-confirm.png` reads "Gap of 40 days between March 5, 2026 (…formulario de admisión (OCR)) and April 14, 2026", and the accepted flag in the internal notes carries the same text (`task2-export-notes.txt`). `evals/library/case_lib09_spanish_interpreter_espalda.expected.json` lists `gap_excluded_records: [4, 7]` and a 42-day gap.
56	Why it matters: the adjuster counts days between treatment encounters; an intake form is paperwork. The figure moved with no note telling me why.
57	Fix: backend card: an intake or billing form never starts or ends a gap, even after its date is confirmed. UI: if a flag's figures change after a decision, say so ("Gap recalculated after you confirmed record 4: now 40 days").
58	Acceptance test: lib09 after confirming record 4 still shows "Gap of 42 days" ending at record 2, and the intake record is not named as an endpoint.
59	
60	**F5. Charges and unclear amounts are too tall to reconcile.** Evidence: `14b-unclear.png`. Five unclear rows at about 400 px each (1,958 px for the tray). The whole 400-character excerpt wraps in a column about 215 px wide, the amount inside it is not highlighted, and the same two sentences of Spanish-record boilerplate ("AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it.") repeat in every row. The status text "unclear; not a bill; needs review" sits beside a quote that says "Consulta: $650.00".
61	Why it matters: reconciling billed charges is my Excel step; this table makes me read the same paragraph five times to find a number.
62	Fix: one row per amount (about 56 px): amount | provider and date | the 8 words around the amount with the amount highlighted | status | actions; the full quote in a drawer or the sticky source pane; the Spanish notice once at the top of the tray; plain status words ("Not counted: can't tell if this is a bill").
63	Acceptance test: lib09 unclear tray height under 700 px; the boilerplate string appears once; the highlighted amount equals the Amount cell on every row.
64	
65	### Minor
66	
67	**F6. Timeline row density.** `22b-public-timeline.png`: two rows per 900 px viewport. Each row repeats the same fact twice (summary, then italic quote) and carries seven buttons (Why?, Open record, Change quote, Accept, Edit, Dismiss, Audit), and Accept stays full blue after it is accepted (`24a-final-accept-viewport.png`). Fix: a compact row of date | provider | summary | quote on hover or click | state chip | one Accept; the secondary actions behind a "..." menu; accepted rows collapse to one line. Test: 8 rows visible in one 900 px screen on case_01.
68	
69	**F7. The "Verified" chip and the "Accept all verified" button invite trust.** The green "Verified" chip means code found the quote; to me "verified" means a person checked it, and the export rules say no "verified" labels in the letter. The first big blue button above the rows is "Accept all verified entries (7)" and one `Shift+A` accepted 8 entries without my looking at any (`06b-after-shiftA.png`). Undo (`Undo last batch (8)`) exists, which is good. Fix: rename the chip "Quote matches record"; label the batch button with a count of rows I have actually opened ("Accept 7 rows you haven't opened"). Test: chip text is not "Verified"; button copy names what is being accepted.
70	
71	**F8. Export placement and finish.** `24a-final-accept-viewport.png`: after the last accept nothing says "Done, 0 left, Export". Export is a button at the top of the timeline; from the last charge it took 74 `Shift+Tab` presses (`p24-to-export.py`). The letter sits in a text box 418 px high with 881 px of text (a scroll inside a scroll, `09-after-export-click.png`), there is no file download (copy only), and the Bates settings are below the internal notes. Early Export with nothing accepted says "The export is blocked. … The export is blocked." (`23a-export-early.png`). Fix: a sticky footer "0 left to review · Export" that stays at the bottom; letter box sized to its text; Bates fields above the letter; download .txt and .docx; one sentence per message. Test: after the last accept, a visible Export control is within one screen of the focus and reachable in at most 2 Tab presses.
72	
73	**F9. Letter format.** `task1-export-letter.txt` / `task2-export-letter.txt`: each entry prints a summary line and then `Source [Ex. __ / Bates __]: "quote"`, so the same fact is on the page twice (D-002's one-line format `date — provider: "quote" [Ex. __ / Bates __]` would be shorter). Spanish entries print "AI translation:" in front of the summary and the OCR slip "espaIda" in the quote. Both are honest, but I would not send "AI translation:" to an adjuster without a decision. Fix: an option for the one-line form; make the translation prefix a bracketed note I can drop. Test: a letter option exists that gives one line per entry.
74	
75	**F10. Dev panel in local mode.** `00-landing.png`: a case switcher and a 15-button library push the real task, the paste box, to about 1,520 px down. After loading lib09 the viewport stays on the library list (scrollY 671 of 11,133, `13-lib09-loaded.png`), so the result is off screen. The case buttons are labelled "Open now: null", "Open: null" and a dozen identical "Open: case lib09 spanish interpreter espalda" (`20c-after-reload.png`); a reload returns to scrollY 0 (was 4,144), although my decisions were kept. Public mode is clean (`21-public-landing.png`), so this is local only. Fix: put the library under a collapsed "Developer tools" control at the bottom; scroll to the case after load; give cases a real label and the load time; restore scroll after reload. Test: after loading a library case the first timeline row is in the viewport.
76	
77	**F11. `o` opens a modal that swallows the next key.** `17a2-modal-e2.png`: `o` opens a blocking dialog; pressing `a` while it is open does nothing (the handler returns when the record modal is open, `review.js:280`), with no message. The sticky source pane already shows the same record and follows selection. Fix: `o` focuses the source pane (or scrolls it) instead of a modal; or show "Close the record first (Esc)". Test: `o` then `a` accepts or shows a message.
78	
79	**F12. Formatting inconsistencies and repeated messages.** "Accepted charges: $310" above a row "$310.00" (`24a-final-accept-viewport.png`); rows use 2026-02-03 while flags and the letter use "February 3, 2026" and the source pane shows the raw "04/05/2026" or "Feb 24, 2026"; the undated entry says "Confirm the date first" three times (`03c-a-on-undated.png`). Edit and Dismiss are still enabled on that undated row. Fix: one currency format (always cents), US long dates in the UI, one message per state, disable Edit and Dismiss until the date is confirmed. Test: no text node matches `\$\d+(?!\.)` in the charges panel; the undated row shows the string once.
80	
81	**F13. A prior-condition flag on an interpreter sentence.** `25d-preexisting-false-positive.png`: "Mention of a prior or pre-existing condition" quoting "Hx obtained via patient's son, who interpreted." The card's own reason is "The phrase list found this flag but the AI did not". Dismissal worked and is listed correctly under FLAGS DISMISSED in the notes. Fix: do not raise a prior-condition flag on "Hx obtained via …" (backend); in the UI say "No prior condition named in this quote" when the two checkers disagree. Test: lib09 raises no prior-condition flag.
82	
83	## Prioritized top 10
84	1. F1 one linear queue; `j`/`k`/`a` cross panels and advance in page order; focus never drops to body.
85	2. F3 do not offer Accept where acceptance blocks export; recovery must not be a dead end.
86	3. F2 plain "To do" strip above the timeline; needs-review rows first; amber decision icon.
87	4. F4 gap must not move to the intake date; tell me when a figure changes.
88	5. F5 one-line unclear and charge rows; amount highlighted; boilerplate once.
89	6. F8 sticky "N left · Export", letter box sized to its text, Bates fields above it, .txt/.docx download.
90	7. F6 compact timeline rows (8+ per screen); actions behind a menu.
91	8. F7 rename "Verified"; honest wording on batch accept.
92	9. F12 one currency format, US long dates, single messages, disable Edit and Dismiss on undated rows.
93	10. F10 collapse the dev library and case list; scroll to the case after load; restore scroll on reload.
94	(F9, F11 and F13 follow after these.)
95	
96	## Right already
97	- Sticky source pane highlights the quoted words and follows the selected row; this is the fastest way I have seen to check a claim.
98	- Edit keeps the original visible ("Edited by you. Original: …") and review state survives a refresh.
99	- Export copy is clean plain text, the dismissed flag is absent from the letter, and the letter total reads "Billed charges stated in these records: $5,090.00" with unclear amounts only in the internal notes.
100	
101	```json
102	{"card": "T-060", "persona": "paralegal-reviewer", "model": "claude-sonnet-5-5",
103	 "scope": "git archive HEAD f187a30 in scratchpad; app http://127.0.0.1:7871 (fixture, curated, ZLAYT_MODE=local) and http://127.0.0.1:7872 (public landing); case_01_date_formats.txt pasted, library lib09; 1440x900 and 1280x720; pass 1, review only",
104	 "exercised": ["case_01 paste to export by keyboard (1 paste, 3 clicks, 6 keys, 9.2 s scripted)", "case_01 in-order accept attempt (focus jumps to row 8)", "lib09 load to export (10 clicks, 17 keys, 19.5 s scripted, export blocked once)", "stepper expanded in 2 states", "Edit with original kept, reload mid-review, o open-record modal", "Copy letter clipboard check", "public vs local landing", "export while nothing accepted", "read app/frontend/review.js lines 85-125 and 270-305"],
105	 "verdict": "changes",
106	 "scores": {"verify_quickly": 3, "keyboard_flow": 2, "handoff_clarity": 3, "information_density": 2, "export_fit": 4, "trust_cues": 4},
107	 "findings": [
108	  {"severity": "major", "title": "Keyboard review breaks across panels; queue order is not page order", "evidence": "artifacts/review-evidence/T-060-pass1/25a-lib09-first-j.png; 25b-lib09-a-yank.png; 12-after-advance.png; app/frontend/review.js:285,292,299; lib09 first j lands on $650 unclear charge at ~8,214 px and 24 presses stay on a7", "why_it_matters": "Checklist 15: I cannot read and accept in order without the mouse; 6 of 10 clicks in lib09 were re-positioning", "fix": "One linear queue in page order; j/k cross panels; a/d advance to next unreviewed; focus to the entry after a date confirm", "acceptance_test": "Playwright on lib09: first j focuses first needs-review entry; a x3 visits e2, e7, e4; j reaches flags then charges"},
109	  {"severity": "major", "title": "Needs-review items not first; hand-off hidden in a collapsed stepper", "evidence": "22b-public-timeline.png; 01-after-analyze-full.png; 04-stepper.png; 05-stepper-open.png; bar text '6/10 checks passed - 4 need you - Export blocked by 1'", "why_it_matters": "Checklist 16: the first screen does not say what blocks export", "fix": "Plain 'To do' strip above the timeline with jump controls; needs-review rows first; amber decision icon not red X", "acceptance_test": "case_01: before scrolling the page shows 'Confirm the date for record 8' with a working jump; first timeline row is Needs review"},
110	  {"severity": "major", "title": "Accept offered where acceptance blocks export; recovery is a dead end", "evidence": "18b-all-reviewed.png; 19b-export-blocked.png; 19c-after-rerun.png; 'The second check still did not answer for 2 items of 2. Try again, or dismiss them.'", "why_it_matters": "I accepted what the card offered and was blocked, with no way to rerun in the demo", "fix": "Disable Accept with the reason when the second check is absent, or route to internal notes only; name the check in plain words", "acceptance_test": "lib09 Rate rows show Accept disabled with a reason; accepting every enabled item leaves Ready to export"},
111	  {"severity": "major", "title": "Gap figure changes from 42 to 40 days after confirming an intake form date", "evidence": "25c-gap-42-before-confirm.png; 25e-gap-40-after-confirm.png; task2-export-notes.txt; evals/library/case_lib09_spanish_interpreter_espalda.expected.json gap_excluded_records [4,7]", "why_it_matters": "The adjuster counts days between treatment; the intake form is paperwork and the change is unexplained", "fix": "Backend: intake and billing records never end a gap; UI: say when a figure is recalculated after a decision", "acceptance_test": "lib09 after confirming record 4 still shows Gap of 42 days ending at record 2"},
112	  {"severity": "major", "title": "Charges and unclear-amount rows are too tall to reconcile", "evidence": "14b-unclear.png; unclear tray 1,958 px for 5 rows; boilerplate repeated per row; amount not highlighted", "why_it_matters": "Reconciling billed charges is a core paralegal step and this makes it slow", "fix": "One-line rows with the amount highlighted in a short snippet; notice once per tray; plain status words", "acceptance_test": "lib09 unclear tray under 700 px; boilerplate string appears once; highlighted amount equals the Amount cell"},
113	  {"severity": "minor", "title": "Timeline rows show two entries per screen with seven buttons each", "evidence": "22b-public-timeline.png; 24a-final-accept-viewport.png", "why_it_matters": "Slows scanning; Accept stays primary after accepting", "fix": "Compact rows, secondary actions in a menu, accepted rows collapse", "acceptance_test": "8 rows visible in one 900 px screen on case_01"},
114	  {"severity": "minor", "title": "Verified chip and Accept-all button invite trust", "evidence": "06b-after-shiftA.png; 22a-public-after-analyze.png ('Accept all verified entries (7)'; Verified chip)", "why_it_matters": "Verified reads as human-checked; one key accepted 8 unopened rows", "fix": "Rename chip 'Quote matches record'; batch label says how many rows were opened", "acceptance_test": "No chip text 'Verified'; batch button copy names what is accepted"},
115	  {"severity": "minor", "title": "Export placement and finish: no done cue, 74 Shift+Tabs to Export, 418 px letter box, no download", "evidence": "24a-final-accept-viewport.png; p24-to-export.py output 74; 09-after-export-click.png; 23a-export-early.png ('The export is blocked.' twice)", "why_it_matters": "The last step of the demand workflow is hard to find and to use", "fix": "Sticky 'N left - Export' footer; letter box sized to text; Bates fields above the letter; .txt/.docx download", "acceptance_test": "After the last accept an Export control is reachable within 2 Tab presses and visible without scrolling"},
116	  {"severity": "minor", "title": "Letter repeats summary and quote; 'AI translation:' prefix printed in the letter", "evidence": "task1-export-letter.txt; task2-export-letter.txt ('AI translation: Reason for visit...'; quote 'espaIda')", "why_it_matters": "Longer letter text to edit; a UI-style label would go to the adjuster", "fix": "Optional one-line format per D-002; bracketed removable translation note", "acceptance_test": "A letter option gives one line per entry"},
117	  {"severity": "minor", "title": "Local-mode dev panel pushes the work down; result off screen after load; null case labels", "evidence": "00-landing.png; 13-lib09-loaded.png (scrollY 671 of 11,133); 20c-after-reload.png; public landing 21-public-landing.png is clean", "why_it_matters": "A reviewer using local mode starts 1,500 px from the task and cannot tell cases apart", "fix": "Collapse library under Developer tools; scroll to the case after load; real case labels; restore scroll on reload", "acceptance_test": "After loading a library case the first timeline row is in the viewport"},
118	  {"severity": "minor", "title": "o opens a modal that swallows the next key", "evidence": "17a2-modal-e2.png; app/frontend/review.js:280", "why_it_matters": "o then a silently does nothing; the sticky source pane already shows the record", "fix": "o focuses the source pane or shows 'Close the record first (Esc)'", "acceptance_test": "o then a accepts or shows a message"},
119	  {"severity": "minor", "title": "Inconsistent currency and date formats; repeated messages; Edit/Dismiss enabled on undated rows", "evidence": "24a-final-accept-viewport.png ('$310' vs '$310.00'); 03c-a-on-undated.png ('Confirm the date first' x3); 22b-public-timeline.png (ISO dates)", "why_it_matters": "Looks unfinished and the repeated text hides the one instruction", "fix": "Always show cents; US long dates; one message per state; disable Edit and Dismiss until the date is confirmed", "acceptance_test": "No dollar amount without cents in the charges panel; the undated row shows its instruction once"},
120	  {"severity": "minor", "title": "Prior-condition flag raised on an interpreter sentence", "evidence": "25d-preexisting-false-positive.png ('Hx obtained via patient's son, who interpreted.')", "why_it_matters": "Adjuster-facing noise that makes me distrust the flags", "fix": "Backend: no prior-condition flag on 'Hx obtained via ...'; UI: say when the checkers disagree", "acceptance_test": "lib09 raises no prior-condition flag"}
121	 ],
122	 "whats_right": ["Sticky source pane highlights the quoted words and follows the selected row", "Edit keeps the original visible and decisions survive a refresh", "Export copy is clean plain text with dismissed items absent and unclear amounts only in the internal notes"],
123	 "questions_for_chris": ["Is the library and case list meant to appear in the demo build, or only in local mode?", "Should a confirmed intake-form date ever count as an encounter for the gap check?"]}
124	```
125	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:29:39.705Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-114 && git -C /Users/arsis/zlayt-pm-project log --oneline -3 && git -C /Users/arsis/zlayt-pm-project cat-file -t b5fb35c",
 "description": "Show card T-114 and verify commit b5fb35c"
}
````

### User / tool · 2026-11-02T09:29:39.870Z

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
updated_at: "2026-11-02T09:29:33Z"
claimed_by: "backend"
claimed_at: "2026-11-02T09:21:17Z"
rounds: 0
commits: ["b5fb35c"]
reviews: []
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

## Handoff
What changed: a rate (D-019/D-042) is acknowledge-only: amounts carry accept_effect + judge_required_for_export=false, trace.judge_not_run_blockers skips them (gate and GET /export agree), item trace says the check is optional; confirm_date returns gap_changes[] (lib09 r4 -> 5 Mar: 42 -> 40 days, with a sentence); lib09 rate judge fixtures (a3, a6) recorded with claude-cli (2 calls, 1 attempt each). How verified: tests/unit/test_t114_rates_and_demo_judges.py (20 tests incl. all 15 library packets walked, no JUDGE_NOT_RUN); full tests/unit 2491 pass before two test_trace updates for rates, which now pass (105 in test_trace+t114). Left: F4 'an intake form never ends a gap' is NOT done (gaps.py has no such rule; needs its own card); estimate/unclear accepts still need a judge; frontend note on T-060. Surprised: only the two lib09 rate judges were missing across all 15 packets.

b5fb35c feat(backend): a rate is acknowledged, never a JUDGE_NOT_RUN blocker; lib09 rate judge fixtures; confirm_date reports gap_changes (T-114)
36ceb38 feat(frontend): T-096 pre-selected date suggestion, dismissal banner, measured precision (with stale note), overlap warning, flag tray wording
03206ca fix(qa): calibration staleness compares on-disk prompts; score_unsplit replays the whole case
commit
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:29:47.301Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git rev-parse --short b5fb35c && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p \"$SCR/t114/archive\" && git archive HEAD | tar -x -C \"$SCR/t114/archive\" && ls \"$SCR/t114/archive\" && echo \"SCR=$SCR\" && ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/ && cat /Users/arsis/zlayt-pm-project/docs/RUNBOOK.md | head -80",
 "description": "Verify HEAD, extract git archive into scratchpad, read runbook"
}
````

### User / tool · 2026-11-02T09:29:47.841Z

**tool result**
````
b5fb35c743dced9cad3f3dc700e853dc42f4da8e
b5fb35c
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
SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
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
t068-dates-to-confirm-patterns.md
t079-library-v2-patterns.md
# RUNBOOK (for Chris)

## URLs
| What | URL | Notes |
|---|---|---|
| Board (tailnet) | https://<redacted-private>:7777 | open on your phone (Tailscale on). Kanban, personas, milestones, activity, inbox, STOP. |
| Board (local) | http://localhost:7777 | also in the Desktop Browser pane (`.claude/launch.json` → "board") |
| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |

Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
We restored those and gave the board and app their own ports so nothing of yours was clobbered.

## Steer
- **Inbox:** Board → Inbox → type a note → Send. It lands in `board/inbox/` and the orchestrator acts on it next cycle.
- **Direct:** type into this Claude session (Remote Control / Desktop). Treated exactly like an inbox note.
- **Your items:** `submission/NEEDS_CHRIS.md` and the `needs_chris` column. Nothing there blocks the team.

## Stop
- Board → Inbox → **STOP** (type STOP to confirm) → creates `board/STOP`. The orchestrator finishes its current handoff and stops.
- Or on the Mac: `touch ~/zlayt-pm-project/board/STOP`.
- **Resume after STOP:** from the phone, type into this Claude session (Remote Control): "Delete board/STOP and continue the loop." On the Mac: `rm ~/zlayt-pm-project/board/STOP`, then continue the session.

## Restart (after a crash, reboot, or closing the session)
1. `cd ~/zlayt-pm-project`
2. Board server: `./tools/serve_board.sh` (also installs the native git pre-commit secret scan if missing) (tmux session `zlayt`, window `board`). Check: `curl -s localhost:7777/healthz`.
3. Session — either:
   - Desktop app: reopen this session from the sidebar (it keeps bypass-permissions mode), or
   - Terminal: `claude --continue --dangerously-skip-permissions --remote-control` (without the first flag the run stalls on permission prompts nobody answers; the second lets you steer and resume from your phone).
4. Say:
   > Re-read CLAUDE.md, memory/STATE.md and `python3 tools/board.py status`. Re-spawn the worker agents (general-purpose subagents whose first step is `python3 tools/agent_prompt.py <role>` unless native agent types are available), recreate the heartbeat cron (text in memory/STATE.md), continue the loop.
5. Tailnet exposure persists across restarts (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.

## Useful commands
```
python3 tools/board.py status          # where are we
python3 tools/board.py list --status in_review
tail -f board/activity.jsonl           # raw event log
.venv/bin/python -m pytest tools/tests -q   # harness tests
```
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:29:49.704Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/paralegal-reviewer/reviewer-api-shape-gotchas.md .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md; echo ----; cat tools/serve_app.sh 2>/dev/null | head -60; echo ----; ls app/backend | head -50",
 "description": "Read reviewer memory notes and serve script"
}
````

### User / tool · 2026-11-02T09:29:49.803Z

**tool result**
````
---
name: reviewer-api-shape-gotchas
description: Zlayt app response shapes that trip review scripts (item GET nests under "item", case status "ready", record warnings live in case.flags, audit before/after only in local mode)
metadata:
  type: reference
---

- `GET /api/cases/{t}/items/{id}` returns `{item, source, calls, events}`. Read the item from `["item"]`. A `.get("reasons")` on the top level returns None and makes "no DATE_AMBIGUOUS" checks pass vacuously.
- Case status terminal success is `"ready"` (not "done"); `"done_with_errors"` is the other OK terminal.
- Record warnings are not a top-level `record_warning_flags` key. They are in `case.flags` with `type == "record_warning"` (e.g. `f_date_r8` before a date confirm).
- `GET audit` events carry `before`/`after` only with `ZLAYT_MODE=local`. Outside local mode they have only id, item_id, action, at.
- Accept/Edit/Change quote controls: `data-testid` btn-accept (has aria-pressed), btn-edit; entry rows are `[data-entry-id="<id>"]`, state chip `entry-state`, reason line `entry-reasons` (only when needs_review).
- Dates-to-confirm picker: `form[data-testid="confirm-date"]` with radio labels like "April 5, 2026 (2026-04-05)" and `btn-confirm-date`.

**Why:** found while writing T-076 r2 checks (2026-11-01). Two checks passed only because the key was missing, and the status check failed on "ready" until corrected.

**How to apply:** before writing a check that reads a field, print the response keys once. Each check should assert the key is present (non-vacuous) before testing its value. Related: [[d041-date-gate-patterns]], [[reviewer-tooling-quirks]].
---
name: reviewer-hook-constraints
description: Bash hooks that block reviewer commands in this repo (board.py --help, python -c containing backticks) and the workarounds
metadata:
  type: reference
---

- board-guard: reviewers may run only `tools/board.py validate|show|list|status`. `--help` is rejected.
- git-guard fails to parse `python3 -c "..."` when the code contains escaped backticks. Use a quoted heredoc (`python3 - <<'EOF'`) and build the fence as '`'*3.
- Write access is limited to reviews/ and artifacts/review-evidence/ (plus this memory dir). Probe scripts go in artifacts/review-evidence/.

**How to apply:** use these forms directly to avoid wasted tool calls. Related: [[golden-set-recurring-findings]]
---
name: reviewer-tooling-quirks
description: Hooks that block reviewer shell commands in Zlayt PM (board-guard on sed -i, git-guard on python -c with backticks) and the workaround
metadata:
  type: feedback
---

Don't edit review files with `sed -i` (board-guard blocks it), and don't run `python3 -c` with backticks or regex escapes (git-guard can't parse it). Use the Edit tool for review files, and put checks in a script under artifacts/review-evidence/ run with `.venv/bin/python`.

**Why:** Both were blocked during the T-013 r2 review (2026-11-01). A script also leaves reproducible evidence the review can cite.

**How to apply:** For every review, put JSON/verdict validation in artifacts/review-evidence/<card>-*-jsoncheck.py. Related: [[spec-review-patterns]].

## T-077/T-078 r2 additions (2026-11-01)
- `grep -E` with long `.{0,120}` patterns over fetched HTML fails in ugrep ("exceeds complexity limits"). Strip tags and search in a python script under artifacts/review-evidence/.
- `timeout` is not installed on this macOS host; drop it and rely on urllib's timeout argument.
- A `mktemp` + `rmdir` combo inside a Bash call tripped board-guard. Keep Bash calls to one purpose.
- Fetched pages redirected to the session scratchpad were not blocked by the hook, but the persona rule says reviewers write only under reviews/, artifacts/review-evidence/ and memory. Write fetch dumps to artifacts/review-evidence/ and say so in the review.
- The NUCC and CMS PDFs download fine with urllib; write the PDF into review-evidence, run `pdftotext -layout`, then delete the PDF and text.

## T-077 r3 additions (2026-11-01)
- `reviewer-write-guard` makes review files append-only: once `reviews/<card>-<persona>-rN.md` exists, Edit is refused ("reviews are append-only"). Proof-read the review (grep every line ref and quote) BEFORE the single Write; a stale ref cannot be fixed afterwards without a new file.
- A bash `python3 -c` with `\`\`\`` and `\d` escapes was denied by git-guard ("could not parse command safely (No escaped character)"). Move any JSON parse into a Write-created script under artifacts/review-evidence/ and run it.
----
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
----
__init__.py
__pycache__
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
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
totals.py
trace.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:29:53.394Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive && wc -l tests/unit/test_t114_rates_and_demo_judges.py && grep -n \"^def \\|^async def \" tests/unit/test_t114_rates_and_demo_judges.py && ls /Users/arsis/zlayt-pm-project/.venv/bin/python && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"import sys; print(sys.version)\"",
 "description": "List tests in T-114 test file and check venv python"
}
````

### User / tool · 2026-11-02T09:29:53.518Z

**tool result**
````
     155 tests/unit/test_t114_rates_and_demo_judges.py
19:def client(tmp_path, monkeypatch):
28:def _load(c, lib_id):
39:def _gate(c, tok):
43:def _blank_judge(conn, tok, item_id):
52:def test_a_rate_accepted_without_a_judge_does_not_block_export_but_a_charge_still_does(client):
82:def test_a_rate_is_never_in_the_letter_total_even_when_accepted(client):
96:def test_walking_every_acceptable_item_on_a_library_packet_never_hits_judge_not_run(client, lib):
118:def test_confirm_date_reports_the_gap_figures_that_changed(client):
132:def test_confirm_date_on_a_phone_note_changes_no_gap(client):
147:def test_gap_changes_pairs_a_moved_endpoint_into_one_change():
/Users/arsis/zlayt-pm-project/.venv/bin/python
3.12.2 (main, Feb  6 2024, 20:19:44) [Clang 15.0.0 (clang-1500.1.0.2.5)]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:29:55.770Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/tests/unit/test_t114_rates_and_demo_judges.py"
}
````

### User / tool · 2026-11-02T09:29:55.794Z

**tool result**
````
1	"""T-114 (T-060 pass 1 F3/F4): a rate is acknowledged, never offered as a letter accept that later blocks export (D-019/D-042, accept needs no judge);
2	every acceptable item on every demo library packet has its judge fixture (no JUDGE_NOT_RUN dead end); confirm_date reports which gap figures moved.
3	Fixture backend, no network."""
4	import os
5	import pathlib
6	import time
7	
8	import pytest
9	from fastapi.testclient import TestClient
10	
11	from app.backend import trace
12	from app.backend.api import create_app, library_cases
13	from app.db import db as DB
14	
15	LIB09 = "case_lib09_spanish_interpreter_espalda"
16	
17	
18	@pytest.fixture
19	def client(tmp_path, monkeypatch):
20	    monkeypatch.setenv("LLM_BACKEND", "fixture")
21	    monkeypatch.setenv("ZLAYT_MODE", "local")
22	    for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"):
23	        monkeypatch.delenv(k, raising=False)
24	    path = str(tmp_path / "t114.sqlite")
25	    return TestClient(create_app(path, static_dir=str(tmp_path)), client=("127.0.0.1", 50000)), path
26	
27	
28	def _load(c, lib_id):
29	    tok = c.post("/api/cases", json={"library": lib_id}).json()["token"]
30	    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
31	    for _ in range(480):
32	        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed", "done_with_errors"):
33	            break
34	        time.sleep(0.25)
35	    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready", lib_id
36	    return tok
37	
38	
39	def _gate(c, tok):
40	    return {s["id"]: s for s in c.get(f"/api/cases/{tok}/trace").json()["steps"]}["export_gate"]
41	
42	
43	def _blank_judge(conn, tok, item_id):
44	    row = DB.get_item(conn, item_id, tok)
45	    lad = row["ladder"]
46	    lad["judge"] = None
47	    DB.update_item(conn, item_id, case=tok, state="needs_review", state_reasons_json=sorted(set(row["state_reasons"]) | {"JUDGE_UNAVAILABLE"}), ladder=lad)
48	    conn.execute("DELETE FROM llm_calls WHERE case_id=? AND item_id=? AND step IN ('j1','j2','j3','j4')", (tok, item_id))
49	
50	
51	# ------------------------------------------------------------ 1. a rate is acknowledged, not a letter accept
52	def test_a_rate_accepted_without_a_judge_does_not_block_export_but_a_charge_still_does(client):
53	    c, path = client
54	    tok = _load(c, LIB09)
55	    conn = DB.connect(path)
56	    amounts = {a["id"]: a for a in c.get(f"/api/cases/{tok}").json()["amounts"]}
57	    rates = [i for i, a in amounts.items() if a["kind"] == "rate"]
58	    charge = next(i for i, a in amounts.items() if a["kind"] == "charge")
59	    assert rates
60	    for i in rates:
61	        assert amounts[i]["accept_effect"] == "acknowledge" and amounts[i]["judge_required_for_export"] is False
62	    assert amounts[charge]["accept_effect"] == "letter_total" and amounts[charge]["judge_required_for_export"] is True
63	    for i in rates:
64	        _blank_judge(conn, tok, i)
65	    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
66	    for i in rates:
67	        assert c.post(f"/api/cases/{tok}/items/{i}/review", json={"action": "accept"}).status_code == 200
68	    g = _gate(c, tok)
69	    assert [b for b in g["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"] == [] and g["counts"]["judge_not_run"] == 0 and g["ready"] is True
70	    assert c.get(f"/api/cases/{tok}/export").status_code == 200
71	    tr = c.get(f"/api/cases/{tok}/items/{rates[0]}/trace").json()
72	    j2 = next(s for s in tr["steps"] if s["id"] == "judge_2")
73	    assert "optional for a rate" in j2["why"]
74	    # the same blank on an accepted charge is still a blocker (D-044 is unchanged for everything that can reach the letter)
75	    _blank_judge(conn, tok, charge)
76	    assert c.post(f"/api/cases/{tok}/items/{charge}/review", json={"action": "accept"}).status_code == 200
77	    got = [b["item_id"] for b in _gate(c, tok)["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
78	    assert got == [charge]
79	    assert c.get(f"/api/cases/{tok}/export").status_code == 422
80	
81	
82	def test_a_rate_is_never_in_the_letter_total_even_when_accepted(client):
83	    c, path = client
84	    tok = _load(c, LIB09)
85	    items = c.get(f"/api/cases/{tok}").json()
86	    for x in [*items["entries"], *items["amounts"]]:
87	        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
88	    r = c.get(f"/api/cases/{tok}/export")
89	    assert r.status_code == 200
90	    letter = r.json()["letter_text"]
91	    assert "Billed charges stated in these records: $5,090.00" in letter      # $2,940 + $2,150; the two $400.00 rate rows add nothing (D-019)
92	
93	
94	# ------------------------------------------------------------ 2. every acceptable item on every demo packet has its judge
95	@pytest.mark.parametrize("lib", [x["id"] for x in library_cases()])
96	def test_walking_every_acceptable_item_on_a_library_packet_never_hits_judge_not_run(client, lib):
97	    c, path = client
98	    tok = _load(c, lib)
99	    conn = DB.connect(path)
100	    for d in c.get(f"/api/cases/{tok}").json()["dates_to_confirm"]:
101	        if d.get("candidates"):
102	            c.post(f"/api/cases/{tok}/records/{d['record_id']}/confirm_date", json={"date": d["candidates"][0]})
103	    case = c.get(f"/api/cases/{tok}").json()
104	    accepted = []
105	    for x in [*case["entries"], *case["undated_entries"], *case["amounts"], *case["flags"]]:
106	        if c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"}).status_code == 200:
107	            accepted.append(x["id"])
108	    assert accepted, lib
109	    g = _gate(c, tok)
110	    jnr = [b["item_id"] for b in g["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
111	    assert jnr == [], f"{lib}: accepted but no judge fixture: {jnr}"
112	    # stricter than the gate: no accepted item (a rate included) is missing its judge answer, so the demo needs no 'run the second check' step
113	    missing = [u["item_id"] for u in trace.unjudged_items(conn, tok) if u["item_id"] in accepted]
114	    assert missing == [], f"{lib}: judge fixture missing for {missing}"
115	
116	
117	# ------------------------------------------------------------ 3. confirm_date reports which gap figures moved
118	def test_confirm_date_reports_the_gap_figures_that_changed(client):
119	    """lib09 record 4 (an intake form): reading it as 5 March moves the one gap from 42 to 40 days; the response says so, old to new."""
120	    c, path = client
121	    tok = _load(c, LIB09)
122	    assert [f["computed"]["days"] for f in c.get(f"/api/cases/{tok}").json()["flags"] if f["type"] == "gap"] == [42]
123	    out = c.post(f"/api/cases/{tok}/records/r4/confirm_date", json={"date": "2026-03-05"}).json()
124	    assert len(out["gap_changes"]) == 1
125	    ch = out["gap_changes"][0]
126	    assert (ch["change"], ch["old_days"], ch["new_days"]) == ("changed", 42, 40)
127	    assert (ch["old_from"], ch["old_to"], ch["new_from"], ch["new_to"]) == ("2026-03-03", "2026-04-14", "2026-03-05", "2026-04-14")
128	    assert ch["sentence"] == "Gap recalculated after you confirmed record 4: now 40 days (was 42)."
129	    assert ch["flag_id"] in out["gap_flags"]
130	
131	
132	def test_confirm_date_on_a_phone_note_changes_no_gap(client):
133	    """golden case_01 record 8 is a phone note (not an encounter): confirming its date moves no gap, so gap_changes is an empty list (not missing)."""
134	    c, path = client
135	    text = (pathlib.Path(__file__).resolve().parents[2] / "evals" / "golden" / "case_01_date_formats.txt").read_text()
136	    tok = c.post("/api/cases", json={"text": text}).json()["token"]
137	    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
138	    for _ in range(480):
139	        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
140	            break
141	        time.sleep(0.25)
142	    d = next(x for x in c.get(f"/api/cases/{tok}").json()["dates_to_confirm"] if x["candidates"])
143	    out = c.post(f"/api/cases/{tok}/records/{d['record_id']}/confirm_date", json={"date": d["candidates"][0]}).json()
144	    assert out["gap_changes"] == []
145	
146	
147	def test_gap_changes_pairs_a_moved_endpoint_into_one_change():
148	    from app.backend import review as RV
149	    old = {"f_a": {"flag_id": "f_a", "from": "2026-03-03", "to": "2026-04-14", "days": 42, "record_nos": [2, 3]}}
150	    new = {"f_b": {"flag_id": "f_b", "from": "2026-03-05", "to": "2026-04-14", "days": 40, "record_nos": [3, 4]}}
151	    got = RV._gap_changes(old, new)
152	    assert len(got) == 1 and got[0]["change"] == "changed" and (got[0]["old_days"], got[0]["new_days"]) == (42, 40)
153	    assert RV._gap_changes(old, old) == []
154	    assert RV._gap_changes(old, {})[0]["change"] == "removed" and RV._gap_changes({}, new)[0]["change"] == "added"
155	    assert "now 40 days (was 42)" in RV._gap_change_sentence(got[0], 4)
156	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:29:59.454Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_t114_rates_and_demo_judges.py -q -p no:cacheprovider 2>&1 | tail -40",
 "description": "Run the T-114 unit test file on the archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T09:30:07.650Z

**tool result**
````
....................                                                     [100%]
20 passed in 7.82s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:30:10.966Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive && cat app/main.py | head -60; grep -rn \"FIXTURE_SET\\|ZLAYT_MODE\" app/backend/api.py | head; ls /Users/arsis/zlayt-pm-project/artifacts/review-evidence | head -5; lsof -nP -iTCP:7871-7880 -sTCP:LISTEN 2>/dev/null | head",
 "description": "Inspect app entrypoint and env handling; check spare ports"
}
````

### User / tool · 2026-11-02T09:30:11.178Z

**tool result**
````
"""Entry point: `python -m app.main` serves the API and app/frontend/ on :7860 (access log off: URLs carry case tokens)."""
import os

import uvicorn

from app.backend.api import create_app

def create():
    """uvicorn app.main:create --factory"""
    return create_app()


if __name__ == "__main__":
    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
app/backend/api.py:80:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:108:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
app/backend/api.py:548:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
app/backend/api.py:582:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
M0-r2-staff-resolution.md
T-001-exercise-1.txt
T-001-exercise-2.txt
T-001-exercise-3.txt
T-001-r2-readonly-repros.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:30:14.478Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive && grep -rn \"ZLAYT_DB\\|FIXTURE_SET\" app/ --include=*.py | head -8; grep -n \"def create_app\" -A6 app/backend/api.py | head -12",
 "description": "Find ZLAYT_DB and FIXTURE_SET usage in backend"
}
````

### User / tool · 2026-11-02T09:30:14.582Z

**tool result**
````
app/llm/backends/fixture.py:13:    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
app/llm/backends/fixture.py:16:    name = os.environ.get("FIXTURE_SET", "").strip()
app/llm/backends/fixture.py:24:        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
app/backend/api.py:94:    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
93:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
94-    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
95-    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
96-    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
97-    app.state.db_path = db_path
98-    app.state.recorded = recorded_hashes()
99-
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:30:19.253Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; cd $S/archive && ( env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$S/app.sqlite3 HOST=127.0.0.1 PORT=7881 PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $S/server.log 2>&1 & echo $! > $S/server.pid ); sleep 3; cat $S/server.pid; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7881/; cat $S/server.log | tail -5",
 "description": "Start T-114 review server on port 7881 with scratch DB"
}
````

### User / tool · 2026-11-02T09:30:22.388Z

**tool result**
````
32148
200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:30:25.012Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive && grep -n \"@app\\.\\(get\\|post\\)\" app/backend/api.py | head -60",
 "description": "List API routes"
}
````

### User / tool · 2026-11-02T09:30:25.109Z

**tool result**
````
212:    @app.get("/api/health")
218:    @app.get("/api/cases")
228:    @app.get("/api/library")
234:    @app.post("/api/cases", status_code=201)
250:    @app.post("/api/cases/pdf", status_code=201)
316:    @app.get("/api/cases/{token}")
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:30:28.552Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive && sed -n 212,250p app/backend/api.py && sed -n 413,425p app/backend/api.py && sed -n 498,520p app/backend/api.py",
 "description": "Read library, case create, confirm_date, review, export routes"
}
````

### User / tool · 2026-11-02T09:30:28.656Z

**tool result**
````
    @app.get("/api/health")
    def health():
        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}

    @app.get("/api/cases")
    def list_cases():
        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
            raise ApiError(404, "not_found", "Not found.")
        c = conn()
        try:
            return {"cases": present.case_list(c)}
        finally:
            c.close()

    @app.get("/api/library")
    def library():
        if not local_mode():
            raise ApiError(404, "not_found", "Not found.")
        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}

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
    @app.post("/api/cases/{token}/items/{item_id}/review")
    async def review_item(token: str, item_id: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            return review.apply_review(c, token, item_id, b, call=make_call(c, token))
        finally:
            c.close()

    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
    from app.backend import pdf_routes
    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
    from app.backend import billing
    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
    from app.backend import reclassify
    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
    from app.backend import calibration_route
    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)

    @app.get("/api/cases/{token}/export")
    def export(token: str):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:30:32.078Z

**tool call — Bash**
````
{
 "command": "cd /tmp && curl -s http://127.0.0.1:7881/api/library | /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json,sys\nd=json.load(sys.stdin)\nprint(len(d['cases']))\nfor c in d['cases']: print(c['id'], '|', c.get('name'))\n\" ; curl -s -X POST -H 'content-type: application/json' -d '{\"library\":\"case_lib09_spanish_interpreter_espalda\"}' http://127.0.0.1:7881/api/cases | head -c 400",
 "description": "List library packets and create a lib09 case"
}
````

### User / tool · 2026-11-02T09:30:32.306Z

**tool result**
````
15
case_lib01_er_only_then_gap | case lib01 er only then gap
case_lib02_slip_fall_prior_knee | case lib02 slip fall prior knee
case_lib03_truck_rear_end_chiro | case lib03 truck rear end chiro
case_lib04_dog_bite_scar_revision | case lib04 dog bite scar revision
case_lib05_pedestrian_orif_hardware | case lib05 pedestrian orif hardware
case_lib06_lop_billed_vs_adjusted | case lib06 lop billed vs adjusted
case_lib07_parking_lot_fall_outside_records | case lib07 parking lot fall outside records
case_lib08_second_crash_mri_after | case lib08 second crash mri after
case_lib09_spanish_interpreter_espalda | case lib09 spanish interpreter espalda
case_lib10_eob_ub04_cms1500 | case lib10 eob ub04 cms1500
case_lib11_priors_and_ledger | case lib11 priors and ledger
case_lib12_records_review_credibility | case lib12 records review credibility
case_lib13_cloned_notes_cross_provider | case lib13 cloned notes cross provider
case_lib14_handwritten_chiro_scans | case lib14 handwritten chiro scans
case_lib15_conclusory_letter_mist | case lib15 conclusory letter mist
{"token":"ZKA85Fpq5FSw5Xy92PPIqQ","name":"case lib09 spanish interpreter espalda","status":"ingested","source":"paste","demo_mode":true,"record_count":7,"split_method":"code","records":[{"id":"r1","seq":1,"source_label":"Quillmere Regional ED","date_raw":"2026-03-03","date_iso":"2026-03-03","date_status":"parsed","date_candidates":[],"duplicate_of":null,"injection_tag":false,"encounter":true,"char
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:30:37.134Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; cat > $S/explore.py <<'EOF'\nimport json, sys, time, urllib.request\nB = \"http://127.0.0.1:7881\"\ndef req(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(B + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(r, timeout=60) as resp:\n            return resp.status, json.loads(resp.read() or b\"null\")\n    except urllib.error.HTTPError as e:\n        return e.code, json.loads(e.read() or b\"null\")\ntok = sys.argv[1]\nreq(\"POST\", f\"/api/cases/{tok}/run\", {})\nfor _ in range(240):\n    s = req(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"]\n    if s in (\"ready\", \"failed\", \"done_with_errors\"): break\n    time.sleep(0.25)\nprint(\"status\", s)\ncode, case = req(\"GET\", f\"/api/cases/{tok}\")\nprint(\"keys\", sorted(case.keys()))\nprint(\"amounts\", json.dumps(case[\"amounts\"], indent=1, ensure_ascii=False)[:3000])\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/explore.py ZKA85Fpq5FSw5Xy92PPIqQ",
 "description": "Run lib09 case and inspect amounts payload",
 "timeout": 180000
}
````

### User / tool · 2026-11-02T09:30:37.707Z

**tool result**
````
status ready
keys ['amounts', 'backend', 'created_at', 'dates_to_confirm', 'demo_mode', 'entries', 'error', 'flags', 'injection', 'models', 'name', 'records', 'review', 'status', 'token', 'totals', 'tray', 'undated_entries', 'updated_at', 'warnings']
amounts [
 {
  "id": "a1",
  "state": "verified",
  "reasons": [],
  "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
  "review_status": "pending",
  "edited": null,
  "ladder": {
   "backend": "fixture",
   "code_checks": {
    "amount_in_text": true,
    "classified_by": "code:amounts"
   },
   "generator": null,
   "human": {
    "action": null,
    "edited_text": null,
    "at": null
   },
   "item_id": "a1",
   "judge": {
    "call_id": "c1885906b5677",
    "model": "claude-haiku-5-5",
    "prompt_version": "judge_amount_class_v1",
    "reason_code": "NONE",
    "verdict": "agree"
   },
   "state": "verified"
  },
  "record_ids": [
   "r1"
  ],
  "entry_id": "e1",
  "text": "$2,940",
  "value_cents": 294000,
  "kind": "charge",
  "excerpt": "Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940.",
  "excerpt_start": 361,
  "excerpt_end": 367,
  "duplicate_note": null,
  "accept_effect": "letter_total",
  "judge_required_for_export": true
 },
 {
  "id": "a2",
  "state": "needs_review",
  "reasons": [
   "JUDGE_DISAGREES",
   "AMOUNT_UNCLEAR",
   "AI_TRANSLATION"
  ],
  "why": "A second AI check disagreed with the first result for this item. This figure could not be read or labelled with confidence, so it is not added to the total. AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it.",
  "review_status": "pending",
  "edited": null,
  "ladder": {
   "backend": "fixture",
   "code_checks": {
    "amount_in_text": true,
    "classified_by": "code:amounts"
   },
   "generator": null,
   "human": {
    "action": null,
    "edited_text": null,
    "at": null
   },
   "item_id": "a2",
   "judge": {
    "call_id": "cc276f84ff25e",
    "model": "claude-haiku-5-5",
    "prompt_version": "judge_amount_class_v1",
    "reason_code": "SHOULD_BE_CHARGE",
    "verdict": "disagree"
   },
   "state": "needs_review"
  },
  "record_ids": [
   "r2"
  ],
  "entry_id": "e2",
  "text": "$650.00",
  "value_cents": 65000,
  "kind": "unclear",
  "excerpt": "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00.",
  "excerpt_start": 751,
  "excerpt_end": 758,
  "duplicate_note": null,
  "accept_effect": "internal_notes",
  "judge_required_for_export": true
 },
 {
  "id": "a3",
  "state": "needs_review",
  "reasons": [
   "AMOUNT_RATE_NOT_TOTALED",
   "AI_TRANSLATION"
  ],
  "why": "This figure is a rate, not a charge, so it is n
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:30:42.435Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; cat > $S/summ.py <<'EOF'\nimport json, sys, urllib.request\nB = \"http://127.0.0.1:7881\"\ntok = sys.argv[1]\ncase = json.load(urllib.request.urlopen(f\"{B}/api/cases/{tok}\"))\nfor a in case[\"amounts\"]:\n    j = (a.get(\"ladder\") or {}).get(\"judge\") or {}\n    print(\"AMT\", a[\"id\"], a[\"kind\"], a[\"text\"], a[\"value_cents\"], \"state=\", a[\"state\"], \"review=\", a[\"review_status\"], \"effect=\", a[\"accept_effect\"], \"judge_req=\", a[\"judge_required_for_export\"], \"judge=\", j.get(\"verdict\"), j.get(\"reason_code\"), \"reasons=\", a[\"reasons\"])\nprint(\"ENTRIES\", [(e[\"id\"], e[\"state\"], e.get(\"review_status\")) for e in case[\"entries\"]])\nprint(\"UNDATED\", [(e[\"id\"], e[\"state\"]) for e in case[\"undated_entries\"]])\nprint(\"FLAGS\", [(f[\"id\"], f[\"type\"], f.get(\"state\"), f.get(\"review_status\")) for f in case[\"flags\"]])\nprint(\"TOTALS\", json.dumps(case[\"totals\"], ensure_ascii=False)[:800])\nprint(\"DATES\", [(d[\"record_id\"], d.get(\"candidates\")) for d in case[\"dates_to_confirm\"]])\nprint(\"REVIEW\", json.dumps(case[\"review\"], ensure_ascii=False)[:600])\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/summ.py ZKA85Fpq5FSw5Xy92PPIqQ",
 "description": "Summarize lib09 amounts, entries, flags, totals"
}
````

### User / tool · 2026-11-02T09:30:42.594Z

**tool result**
````
AMT a1 charge $2,940 294000 state= verified review= pending effect= letter_total judge_req= True judge= agree NONE reasons= []
AMT a2 unclear $650.00 65000 state= needs_review review= pending effect= internal_notes judge_req= True judge= disagree SHOULD_BE_CHARGE reasons= ['JUDGE_DISAGREES', 'AMOUNT_UNCLEAR', 'AI_TRANSLATION']
AMT a3 rate $400.00 40000 state= needs_review review= pending effect= acknowledge judge_req= False judge= agree NONE reasons= ['AMOUNT_RATE_NOT_TOTALED', 'AI_TRANSLATION']
AMT a4 charge $2,150 215000 state= verified review= pending effect= letter_total judge_req= True judge= agree NONE reasons= []
AMT a5 unclear $1,300.00 130000 state= needs_review review= pending effect= internal_notes judge_req= True judge= disagree SHOULD_BE_CHARGE reasons= ['JUDGE_DISAGREES', 'AMOUNT_UNCLEAR', 'AI_TRANSLATION']
AMT a6 rate $400.00 40000 state= needs_review review= pending effect= acknowledge judge_req= False judge= agree NONE reasons= ['AMOUNT_RATE_NOT_TOTALED', 'AI_TRANSLATION']
AMT a7 unclear $2,900.00 290000 state= needs_review review= pending effect= internal_notes judge_req= True judge= disagree SHOULD_BE_CHARGE reasons= ['JUDGE_DISAGREES', 'AMOUNT_UNCLEAR', 'AI_TRANSLATION']
ENTRIES [('e1', 'verified', 'pending'), ('e2', 'needs_review', 'pending'), ('e3', 'verified', 'pending'), ('e5', 'verified', 'pending'), ('e6', 'verified', 'pending'), ('e7', 'needs_review', 'pending')]
UNDATED [('e4', 'needs_review')]
FLAGS [('f_gap_r1_r2', 'gap', 'needs_review', 'pending'), ('f_date_r4', 'record_warning', 'needs_review', 'pending'), ('f_r1_1', 'pre_existing', 'needs_review', 'pending'), ('f_r1_2', 'causation', 'needs_review', 'pending'), ('f_r2_1', 'causation', 'needs_review', 'pending'), ('f_r3_1', 'causation', 'needs_review', 'pending')]
TOTALS {"accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 509000, "count": 2, "label": "Pending review"}, "detected_not_a_total": {"cents": 509000, "count": 2, "label": "Detected (not a total)"}, "not_totaled": [{"id": "a2", "kind": "unclear", "text": "$650.00"}, {"id": "a3", "kind": "rate", "text": "$400.00"}, {"id": "a5", "kind": "unclear", "text": "$1,300.00"}, {"id": "a6", "kind": "rate", "text": "$400.00"}, {"id": "a7", "kind": "unclear", "text": "$2,900.00"}], "possible_overlaps": [{"code": "POSSIBLE_OVERLAP", "statement_amount_id": "a5", "covered_amount_id": "a2", "service": "consult", "statement_record_id": "r7", "covered_record_id": "r2", "statement_text": "$1,300.00", "covered_text": "$650.00", "range": {"from": null, "to": "2026-05-20", "stated": f
DATES [('r4', ['2026-03-05', '2026-05-03'])]
REVIEW {"counts": {"pending": 20, "accepted": 0, "edited": 0, "dismissed": 0, "needs_review": 14, "verified": 6, "rejected": 0}, "queue": ["a2", "a3", "a5", "a6", "a7", "e4", "e2", "e7", "f_date_r4", "f_gap_r1_r2", "f_r1_1", "f_r1_2", "f_r2_1", "f_r3_1", "a1", "a4", "e1", "e3", "e5", "e6"], "ready_to_export": false}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:30:49.277Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; cat > $S/rate1.py <<'EOF'\nimport json, sys, urllib.request\nB = \"http://127.0.0.1:7881\"\ntok = sys.argv[1]\ndef req(m, p, body=None):\n    r = urllib.request.Request(B + p, data=json.dumps(body).encode() if body is not None else None, method=m, headers={\"content-type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(r, timeout=60) as x: return x.status, json.loads(x.read() or b\"null\")\n    except urllib.error.HTTPError as e: return e.code, json.loads(e.read() or b\"null\")\nst, r = req(\"POST\", f\"/api/cases/{tok}/items/a3/review\", {\"action\": \"accept\"})\nprint(\"ACCEPT a3\", st, json.dumps(r, ensure_ascii=False)[:1500])\nst, case = req(\"GET\", f\"/api/cases/{tok}\")\nprint(\"TOTALS\", json.dumps(case[\"totals\"][\"accepted\"]), json.dumps(case[\"totals\"][\"not_totaled\"]))\nprint(\"a3 now\", [ (a[\"id\"], a[\"state\"], a[\"review_status\"], a[\"accept_effect\"]) for a in case[\"amounts\"] if a[\"id\"]==\"a3\"])\nst, ex = req(\"GET\", f\"/api/cases/{tok}/export\")\nprint(\"EXPORT\", st, json.dumps(ex, ensure_ascii=False)[:300] if st!=200 else \"ok\")\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/rate1.py ZKA85Fpq5FSw5Xy92PPIqQ",
 "description": "Accept rate a3 on lib09 and inspect response, totals, export"
}
````

### User / tool · 2026-11-02T09:30:49.459Z

**tool result**
````
ACCEPT a3 200 {"item": {"id": "a3", "state": "needs_review", "reasons": ["AMOUNT_RATE_NOT_TOTALED", "AI_TRANSLATION"], "why": "This figure is a rate, not a charge, so it is not added to the total. AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it.", "review_status": "accepted", "edited": null, "ladder": {"backend": "fixture", "code_checks": {"amount_in_text": true, "classified_by": "code:amounts"}, "generator": null, "human": {"action": "accept", "edited_text": null, "at": null}, "item_id": "a3", "judge": {"call_id": "c094b3f6c6a1d", "model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "reason_code": "NONE", "verdict": "agree"}, "state": "needs_review"}, "record_ids": ["r2"], "entry_id": "e2", "text": "$400.00", "value_cents": 40000, "kind": "amount", "excerpt": "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00.", "excerpt_start": 796, "excerpt_end": 803, "duplicate_note": null, "accept_effect": "acknowledge", "judge_required_for_export": false}, "totals": {"accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 509000, 
TOTALS {"cents": 0, "count": 0, "label": "Accepted charges"} [{"id": "a2", "kind": "unclear", "text": "$650.00"}, {"id": "a3", "kind": "rate", "text": "$400.00"}, {"id": "a5", "kind": "unclear", "text": "$1,300.00"}, {"id": "a6", "kind": "rate", "text": "$400.00"}, {"id": "a7", "kind": "unclear", "text": "$2,900.00"}]
a3 now [('a3', 'needs_review', 'accepted', 'acknowledge')]
EXPORT 200 ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:30:54.039Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive && sed -n 519,546p app/backend/api.py",
 "description": "Read export route"
}
````

### User / tool · 2026-11-02T09:30:54.124Z

**tool result**
````
    @app.get("/api/cases/{token}/export")
    def export(token: str):
        from app.backend import export_routes as XR
        c = conn()
        try:
            get_case(c, token)
            case = store.export_case(c, token)
            try:
                ex = XR.export_payload(token, case)
            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
            calls = DB.list_llm_calls(c, token)
            ok = ("accepted", "edited")
            tv = present.totals_view(c, token)
            ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
            ex["excluded"] = {"pending": case["pending_count"],
                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
                              "rejected": present.rejected_count(c, token)}
            ex["provenance"] = {"generator_model": models()["generator"], "judge_model": models()["judge"], "backend": backend(),
                                "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
                                "edited_count": sum(1 for x in case["entries"] if x["review_status"] == "edited")}
            return ex
        finally:
            c.close()

    @app.get("/api/cases/{token}/items/{item_id}/trace")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:31:17.500Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; cat > $S/lettercheck.py <<'EOF'\nimport json, sys, time, urllib.request\nB = \"http://127.0.0.1:7881\"\ndef req(m, p, body=None):\n    r = urllib.request.Request(B + p, data=json.dumps(body).encode() if body is not None else None, method=m, headers={\"content-type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(r, timeout=120) as x: return x.status, json.loads(x.read() or b\"null\")\n    except urllib.error.HTTPError as e: return e.code, json.loads(e.read() or b\"null\")\ntok = sys.argv[1]\nst, ex = req(\"GET\", f\"/api/cases/{tok}/export\")\nprint(\"export status\", st, \"keys\", sorted(ex.keys()) if st == 200 else ex)\nprint(json.dumps(ex.get(\"letter_text\", \"\"), ensure_ascii=False)[:1500])\nprint(\"NOTES\", json.dumps(ex.get(\"notes_text\", ex.get(\"internal_notes\", \"\")), ensure_ascii=False)[:2500])\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/lettercheck.py ZKA85Fpq5FSw5Xy92PPIqQ; grep -n \"acknowledg\" -r /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app --include=*.py --include=*.js | head -20",
 "description": "Inspect export payload and grep acknowledge wording"
}
````

### User / tool · 2026-11-02T09:31:17.676Z

**tool result**
````
export status 200 keys ['counts', 'excluded', 'generated_at', 'internal_notes_text', 'items', 'letter_text', 'provenance', 'token', 'totals', 'warnings']
"TREATMENT CHRONOLOGY"
NOTES ""
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/backend/trace.py:504:        if acknowledge_only("amount", row) and js["status"] == SKIPPED and (js.get("evidence") or {}).get("judge_verdict") == "unavailable":
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/backend/trace.py:505:            js["why"] = "The second check did not run. It is optional for a rate: accepting a rate only acknowledges it, and a rate never reaches the letter."   # T-114
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/backend/trace.py:792:def acknowledge_only(kind: str, row: dict) -> bool:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/backend/trace.py:793:    """T-114 (D-019/D-042): a figure classified `rate` is never a letter charge, so accepting it only acknowledges it (it is listed in the internal notes, never totaled).
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/backend/trace.py:800:    A rate (`acknowledge_only`) is the one exception: accepting it only acknowledges it, nothing of it reaches the letter (T-114)."""
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/backend/trace.py:802:            if u["review_status"] in ("accepted", "edited") and not acknowledge_only(u["kind"], u["row"])]
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/backend/present.py:58:    """What Accept does to an amount (T-114): `letter_total` (a charge: counted in the billed-charges total), `acknowledge` (a rate: noted in the internal notes only,
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/backend/present.py:60:    return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/backend/speaker.py:78:acknowledges acknowledged claims claimed believes believed thinks thought recalls recalled remembers remembered rates rated
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:31:24.289Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; grep -rn \"accept_effect\\|judge_required\\|gap_changes\\|Acknowledged\\|acknowledged\\|rate\" $A/app/frontend/*.js | grep -v \"generate\\|iterate\\|separate\\|moderate\\|rated\\b\" | head -30; echo ---; grep -n \"T-114\\|rate\" $A/app/backend/present.py | head -20; echo; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"import playwright; print('playwright ok')\"",
 "description": "Check frontend handling of rate accept effect and playwright availability"
}
````

### User / tool · 2026-11-02T09:31:24.422Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/charges.js:2:   unclear tray for rates / estimates / damages / unreadable amounts (R-CH-3, R-CH-5, D-019). Charges: accept or dismiss only (D-010). */
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/charges.js:6:  const KIND = { charge: "Charge", rate: "Rate", estimate: "Estimate", damages: "Damages mention", unclear: "Unclear" };
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/charges.js:10:  // "12 planned; discharged at visit 9" for a per-visit rate, read from the record headers/text the API returned (or a.rate_note when the backend sends it).
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/charges.js:11:  function rateContext(c, a) {
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/charges.js:12:    const n = a.rate_note || {};
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/charges.js:29:    if (a.kind === "rate") {
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/charges.js:32:      bits.push("rate " + a.text + (unit ? "/" + unit : "") + "; " + (unit ? unit + " count" : "count") + " not stated");
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/charges.js:33:      const ctx = a.note || a.detail || rateContext(c, a);
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/mock.js:99:        const rate = /per visit|\/visit/i.test(sent.text);
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/mock.js:100:        amounts.push({ id: "a" + (amounts.length + 1), record_ids: [r.id], entry_id: "e" + r.seq, text: t, value_cents: Math.round(parseFloat(t.replace(/[$,]/g, "")) * 100), kind: rate ? "rate" : "charge",
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/mock.js:101:          excerpt: sent.text, excerpt_start: sent.start, excerpt_end: sent.end, state: rate ? "needs_review" : "verified", reasons: rate ? ["AMOUNT_RATE_NOT_TOTALED"] : [],
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/mock.js:102:          why: rate ? "This is a per-visit rate; the records never say how many visits were billed, so it is not totaled." : "Labelled as a charge in the record, the figure is in the record, and the second check agreed.",
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/mock.js:103:          review_status: "pending", edited: null, duplicate_note: null, ladder: { item_id: "a" + (amounts.length + 1), state: rate ? "needs_review" : "verified", backend: "fixture", generator: null,
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/mock.js:104:            code_checks: { amount_in_text: true, classified_by: rate ? "rule:per_unit" : "rule:charge_label" }, judge: { model: "claude-haiku-5-5", verdict: "agrees" }, human: { action: null } } });
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/state.js:15:        if (i >= 0) { // the review response labels items with a generic kind ("amount"); an amount's own kind (charge / rate / ...) must survive
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/timeline.js:10:    LLM_CALL_FAILED: "could not process", GROUNDING_EXCERPT_NOT_VERBATIM: "the model's quote is not word for word in the record", AMOUNT_RATE_NOT_TOTALED: "a rate, not totaled",
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/suggestions.js:163:          el("li", {}, "Separate charge: " + o.covered_text + " (Record " + b + ")")),
---
58:    """What Accept does to an amount (T-114): `letter_total` (a charge: counted in the billed-charges total), `acknowledge` (a rate: noted in the internal notes only,
60:    return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")
66:            "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate"}
124:            "possible_overlaps": overlap.view(conn, case_id)}      # T-110: a statement line that may include a separately stated charge; warns, never changes the total

playwright ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:31:28.076Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; wc -l $A/app/frontend/charges.js; sed -n 1,80p $A/app/frontend/charges.js",
 "description": "Read charges.js rate rendering and accept wiring"
}
````

### User / tool · 2026-11-02T09:31:28.167Z

**tool result**
````
      93 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/charges.js
/* Charges panel (T-043): accepted total from the API (never summed here), "detected, not yet accepted" labelled as not a total,
   unclear tray for rates / estimates / damages / unreadable amounts (R-CH-3, R-CH-5, D-019). Charges: accept or dismiss only (D-010). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const RV = ZL.rv, el = (...a) => ZL.el(...a);
  const KIND = { charge: "Charge", rate: "Rate", estimate: "Estimate", damages: "Damages mention", unclear: "Unclear" };
  const recSeq = (c, id) => { const r = (c.records || []).find((x) => x.id === id); return r ? r.seq : String(id).replace(/^r/, ""); };
  const reasonIs = (a, code) => (a.reasons || []).includes(code);

  // "12 planned; discharged at visit 9" for a per-visit rate, read from the record headers/text the API returned (or a.rate_note when the backend sends it).
  function rateContext(c, a) {
    const n = a.rate_note || {};
    let planned = n.planned, last = n.last_visit;
    if (planned == null && last == null) {
      const prefix = (s) => String(s || "").split(",")[0].trim().toLowerCase();
      const me = (c.records || []).find((r) => r.id === (a.record_ids || [])[0]);
      const same = me ? (c.records || []).filter((r) => prefix(r.source_label) === prefix(me.source_label)) : [];
      same.forEach((r) => {
        const p = /Plan of care:\s*(\d+)\s*visits?/i.exec(r.text || ""); if (p && planned == null) planned = p[1];
        const v = /\bvisit\s+(\d+)/i.exec(r.source_label || ""); if (v && (last == null || +v[1] > +last)) last = v[1];
      });
    }
    const bits = (planned != null ? [planned + " planned"] : []).concat(last != null ? ["discharged at visit " + last] : []);
    return bits.join("; ");
  }
  // One-line description for the unclear tray. Wording comes from the amount's kind and the quoted line; nothing is computed.
  function unclearNote(c, a) {
    const bits = [];
    if (a.kind === "rate") {
      const m = /\bper\s+([A-Za-z]+)/i.exec(a.excerpt || "") || /\/\s*([A-Za-z]+)/.exec(a.excerpt || "");
      const unit = m ? m[1].toLowerCase() : null;
      bits.push("rate " + a.text + (unit ? "/" + unit : "") + "; " + (unit ? unit + " count" : "count") + " not stated");
      const ctx = a.note || a.detail || rateContext(c, a);
      if (ctx) bits[0] += " (" + ctx + ")";
    } else if (a.kind === "estimate") bits.push("estimate; not a bill");
    else if (a.kind === "damages") bits.push("mention of damages; not a bill");
    else if (a.value_cents == null) bits.push("unreadable amount; request clean copy of bill");
    else bits.push("unclear; not a bill");
    if (a.state === "needs_review") bits.push("needs review");
    if (reasonIs(a, "INJECTION_SUSPECTED")) bits.push("appears inside instruction-like text");
    return bits.join("; ");
  }

  function row(c, a, inTray) {
    const isCharge = a.kind === "charge";
    const rs = a.review_status || "pending";
    const tr = el("tr", { class: "rv-card rv-amount", tabindex: "0", "data-testid": "amount-" + a.text, "data-item-id": a.id, "data-amount-kind": a.kind,
      "data-state": a.state, "data-review": rs, "aria-label": "Amount " + a.text });
    const first = el("td", { class: "rv-c-amount", "data-label": "Amount" }, el("strong", { class: "rv-money" }, a.text), el("span", { class: "rv-kind" }, KIND[a.kind] || a.kind));
    if (inTray) first.append(el("span", { class: "rv-unclear-note" }, unclearNote(c, a)));
    const src = el("td", { class: "rv-c-src", "data-label": "From the record" },
      el("blockquote", { class: "rv-quote" }, a.excerpt || ""),
      el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-source", onclick: () => RV.openSource(a, "amount") }, "Open record " + recSeq(c, (a.record_ids || [])[0])),
      ZL.stepper ? ZL.stepper.traceButton(a.id) : null);
    const status = el("td", { class: "rv-c-status", "data-label": "Status" }, RV.chips(a),
      !isCharge && (rs === "accepted") ? el("span", { class: "rv-noted" }, "Noted for the internal notes only; not in the letter or the total.") : null,
      a.why ? el("p", { class: a.state === "needs_review" ? "rv-reason-line" : "rv-why" }, a.why) : null);
    const act = el("td", { class: "rv-c-act", "data-label": "Decision" }, RV.controls(a, "amount"));
    tr.append(first, src, status, act);
    return tr;
  }

  function table(c, list, caption, inTray) {
    const t = el("table", { class: "rv-table" }, el("caption", { class: "rv-sr" }, caption),
      el("thead", {}, el("tr", {}, ["Amount", "From the record", "Status", "Decision"].map((h) => el("th", { scope: "col" }, h)))),
      el("tbody", {}, RV.needsReviewFirst(list).map((a) => row(c, a, inTray))));
    return t;
  }

  function render(root, c) {
    ZL.clear(root);
    root.setAttribute("data-testid", "charges-panel");
    root.setAttribute("aria-labelledby", "rv-charges-h");
    const amounts = c.amounts || [], t = c.totals || {};
    const charges = amounts.filter((a) => a.kind === "charge"), unclear = amounts.filter((a) => a.kind !== "charge");
    const acc = (t.accepted && t.accepted.cents) != null ? t.accepted.cents : 0;
    const pendObj = t.pending || t.detected_not_a_total || { cents: 0 };
    root.append(el("h2", { id: "rv-charges-h" }, "Charges"),
      el("p", { class: "rv-help" }, "Only charges you accept are counted. Rates, estimates, damages and unreadable amounts are listed below and never added."),
      el("div", { class: "rv-totals" },
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:31:37.885Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; grep -n \"gap\" $A/evals/library/case_lib09_spanish_interpreter_espalda.expected.json | head -20; grep -n \"\\\"4\\\"\\|r4\\|formulario\" $A/evals/library/case_lib09_spanish_interpreter_espalda.txt 2>/dev/null | head; ls $A/evals/library | grep lib09; grep -n \"def confirm_date\" -A30 $A/app/backend/review.py | grep -n \"gap\" | head",
 "description": "Check golden expectation for lib09 gap and record 4"
}
````

### User / tool · 2026-11-02T09:31:38.001Z

**tool result**
````
219:  "gap_excluded_records": [
223:  "gap_table": [
400:      "type": "gap",
424:      "summary": "Treatment gap of 42 days (2026-03-03 to 2026-04-14), longer than 30."
482:      "type": "gap",
483:      "statement": "No gap flag for the 7, 14 and 7-day intervals; the ambiguous-date intake (record 4) and the statement of account (record 7) are not gap endpoints."
653:    "Gap in the product (no flag type): the statement bills 4 therapy sessions at $400.00 ($1,600.00) but the packet holds no PT note. The product has no billed-without-a-note flag type (flag types are gap, conflict, pre_existing, causation; billing analysis is not a flag), so expected.json lists it only as tolerated T2 and the card records the gap.",
20:Source: Consultorio Médico Aguaclara, formulario de admisión (OCR)
case_lib09_spanish_interpreter_espalda.expected.json
case_lib09_spanish_interpreter_espalda.txt
24:353-    gap_changes = []
25:354-    removed += _recompute_gaps(conn, case_id, t, gap_changes)
26:355-    for ch in gap_changes:
27:356-        ch["sentence"] = _gap_change_sentence(ch, rec["seq"])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:31:40.975Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; sed -n 215,235p $A/evals/library/case_lib09_spanish_interpreter_espalda.expected.json; sed -n 478,486p $A/evals/library/case_lib09_spanish_interpreter_espalda.expected.json; sed -n 18,24p $A/evals/library/case_lib09_spanish_interpreter_espalda.txt",
 "description": "Read golden expectations for lib09 gap and record 4 header"
}
````

### User / tool · 2026-11-02T09:31:41.070Z

**tool result**
````
      "required_terms": []
    }
  ],
  "expected_entry_count": 7,
  "gap_excluded_records": [
    4,
    7
  ],
  "gap_table": [
    {
      "from_date": "2026-03-03",
      "to_date": "2026-04-14",
      "from_records": [
        1
      ],
      "to_records": [
        2
      ],
      "days": 42,
      "flag": true
    },
  ],
  "must_not_flag": [
    {
      "id": "N1",
      "type": "gap",
      "statement": "No gap flag for the 7, 14 and 7-day intervals; the ambiguous-date intake (record 4) and the statement of account (record 7) are not gap endpoints."
    }
  ],
  "tolerated": [
=== Record 4 ===
Date: 03/05/2026
Source: Consultorio Médico Aguaclara, formulario de admisión (OCR)
Excerpt: "Fecha de ingreso: 03/O5/2026. Motivo de la visita: dolor de espaIda y hombro derecho. Accidentes anteriores? Si [ ] No [X]. Firma de la paciente: illegible."

=== Record 5 ===
Date: 2026-05-05
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:31:48.131Z

**tool call — Bash**
````
{
 "command": "grep -rn -i \"gap\" spec/SPEC.md spec/REQUIREMENTS.md spec/SAMPLE_CASE_TRUTHS.md memory/ORCHESTRATOR_DECISIONS.md 2>/dev/null | grep -i \"intake\\|endpoint\\|encounter\\|phone\\|form\\|billing\" | head -15",
 "description": "Check spec wording on gap endpoints and intake forms"
}
````

### User / tool · 2026-11-02T09:31:48.229Z

**tool result**
````
memory/ORCHESTRATOR_DECISIONS.md:11:| D-003 | Gaps are computed by code over the code-parsed header dates of all clinical-encounter records (deduped), independent of LLM entries and review state. Billing statements and phone notes are excluded. Ambiguous dates are excluded and flagged. | Dropping an LLM entry must never change gap math. | T-014 staff-eng F2; T-015 paralegal |
spec/REQUIREMENTS.md:40:| R-IN-5 | **Dates to confirm.** An entry with an ambiguous date is excluded from ordering and gap math, shown in a "Dates to confirm" group placed after the timeline (a `record_warning`), and is `needs_review`. She resolves it with the `confirm_date` action (R-RV-2), choosing one of the code-proposed readings. An undated entry sits in the same group with "no date found"; this build offers no way to type one in. | `case_01` record 8: absent from the timeline order until confirmed; after `confirm_date` 2026-05-04 it sorts into the timeline after 03-25. The gap table is unchanged because record 8 is a phone note (D-003 counts clinical encounters only). With no readings (no date found) an entry can't be confirmed and stays excluded. | UT + E2E |
spec/REQUIREMENTS.md:61:Four types: `gap`, `conflict`, `pre_existing`, `causation`. Gap math is code over the header dates of clinical-encounter records (D-003): billing statements and phone notes are excluded, duplicates collapsed, ambiguous dates excluded, and the result does not change when the paralegal dismisses or edits an entry. Every flag shows its evidence.
spec/REQUIREMENTS.md:65:| R-FL-1 | **Treatment gap.** Flag when days between consecutive dates of service across all providers (A-102) is **greater than 30** (A-104). Only clinical-encounter records count (D-003): billing statements and phone notes are excluded. Evidence is the two bounding entries (date, provider, excerpt). | Sample: flag 2026-03-06 → 2026-05-18, 73 days, citing entries 6 and 7. No flag on 2026-01-23 → 2026-02-20 (28 days). `case_02_gap_boundaries`: 29 and 30 do not flag, 31 does (3 flags, 4 near-misses). UT: dismissing entry 6 leaves the gap flag and its days unchanged. | UT (29/30/31) + EV `flag_*[gap]` |
spec/REQUIREMENTS.md:122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first appearance in the chronology, omitting any provider with an accepted charge, with " (itemized ledger)" appended when the provider has a non-dismissed rate. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 1, 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (entry 1 because the accident-date conflict cites its "rear-ended" sentence) (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); the accident-date conflict citing records 1 and 2 (header date, no choice between dates, D-017) and record 7's intake line; the K5 causation item for record 7's intake line; the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; the bills-to-request line is exactly "Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management." UT: every match of the case-insensitive pattern `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
spec/REQUIREMENTS.md:370:| 3 | `memory/contracts/api.md` / `memory/DECISIONS.md` | `confirm_date` with a non-candidate date must be `422 date_invalid`; the AI line in DECISIONS must match R-EX-4(1); the gap example for a phone note must follow D-003 (excluded from gap math). | `grep -n "date_invalid" memory/contracts/api.md`; `grep -n "AI assistance" memory/DECISIONS.md`; `grep -n "phone" memory/contracts/api.md memory/DECISIONS.md` | T-028 (architect) |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:32:10.377Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-paralegal-api-checks.py",
 "content": "\"\"\"T-114 paralegal-reviewer API checks (stdlib only; run with: .venv/bin/python -I <this file> [base_url]).\n\nTargets a server started from a `git archive HEAD` copy (b5fb35c) on its own port, fixture backend, ZLAYT_MODE=local.\nChecks:\n  A. lib09 rate rows: accepting a rate is an acknowledge (accept_effect), never a JUDGE_NOT_RUN blocker, never in the total.\n  B. every acceptable item on all 15 library packets: no JUDGE_NOT_RUN at the gate, export status, two variants\n     (dates confirmed to the first candidate; dates left unconfirmed).\n  C. confirm_date on lib09 record 4 returns gap_changes (42 -> 40) and the flag endpoints.\nPrints a JSON summary to stdout and writes the same to artifacts/review-evidence/T-114-paralegal-api-checks.out.json.\n\"\"\"\nimport json\nimport os\nimport sys\nimport time\nimport urllib.error\nimport urllib.request\n\nBASE = sys.argv[1] if len(sys.argv) > 1 else \"http://127.0.0.1:7881\"\nLIB09 = \"case_lib09_spanish_interpreter_espalda\"\nHERE = os.path.dirname(os.path.abspath(__file__))\nOUT = os.path.join(HERE, \"T-114-paralegal-api-checks.out.json\")\n\n\ndef req(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(BASE + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(r, timeout=120) as x:\n            return x.status, json.loads(x.read() or b\"null\")\n    except urllib.error.HTTPError as e:\n        return e.code, json.loads(e.read() or b\"null\")\n\n\ndef load(lib_id):\n    st, body = req(\"POST\", \"/api/cases\", {\"library\": lib_id})\n    assert st == 201, (lib_id, st, body)\n    tok = body[\"token\"]\n    assert req(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\n    for _ in range(480):\n        s = req(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"]\n        if s in (\"ready\", \"failed\", \"done_with_errors\"):\n            break\n        time.sleep(0.25)\n    assert s == \"ready\", (lib_id, s)\n    return tok\n\n\ndef gate(tok):\n    steps = {x[\"id\"]: x for x in req(\"GET\", f\"/api/cases/{tok}/trace\")[1][\"steps\"]}\n    return steps[\"export_gate\"]\n\n\ndef jnr(tok):\n    return [b[\"item_id\"] for b in gate(tok)[\"blockers\"] if b[\"reason_code\"] == \"JUDGE_NOT_RUN\"]\n\n\ndef letter_lines(ex, needle):\n    return [ln for ln in ex[\"letter_text\"].splitlines() if needle in ln]\n\n\nout = {\"base\": BASE, \"A_lib09_rates\": {}, \"B_library_packets\": {\"dates_confirmed\": {}, \"dates_unconfirmed\": {}}, \"C_gap\": {}}\n\n# ---------------------------------------------------------------- A. lib09 rate rows\ntok = load(LIB09)\ncase = req(\"GET\", f\"/api/cases/{tok}\")[1]\namts = {a[\"id\"]: a for a in case[\"amounts\"]}\nrates = [i for i, a in amts.items() if a[\"kind\"] == \"rate\"]\nout[\"A_lib09_rates\"][\"rates\"] = [{\"id\": i, \"text\": amts[i][\"text\"], \"accept_effect\": amts[i][\"accept_effect\"],\n                                  \"judge_required_for_export\": amts[i][\"judge_required_for_export\"],\n                                  \"judge_verdict\": ((amts[i].get(\"ladder\") or {}).get(\"judge\") or {}).get(\"verdict\"),\n                                  \"judge_call_id\": ((amts[i].get(\"ladder\") or {}).get(\"judge\") or {}).get(\"call_id\")} for i in rates]\nout[\"A_lib09_rates\"][\"total_before\"] = case[\"totals\"][\"accepted\"]\nout[\"A_lib09_rates\"][\"jnr_before_any_accept\"] = jnr(tok)\nst, r = req(\"POST\", f\"/api/cases/{tok}/items/a3/review\", {\"action\": \"accept\"})\nout[\"A_lib09_rates\"][\"accept_a3\"] = {\"http\": st, \"review_status\": r[\"item\"][\"review_status\"], \"state\": r[\"item\"][\"state\"],\n                                     \"accept_effect\": r[\"item\"][\"accept_effect\"], \"judge_required_for_export\": r[\"item\"][\"judge_required_for_export\"],\n                                     \"total_accepted_cents\": r[\"totals\"][\"accepted\"][\"cents\"]}\nst, r = req(\"POST\", f\"/api/cases/{tok}/items/a6/review\", {\"action\": \"accept\"})\nout[\"A_lib09_rates\"][\"accept_a6\"] = {\"http\": st, \"review_status\": r[\"item\"][\"review_status\"], \"accept_effect\": r[\"item\"][\"accept_effect\"]}\nout[\"A_lib09_rates\"][\"after_both_rates\"] = {\"jnr\": jnr(tok), \"gate_ready\": gate(tok)[\"ready\"]}\nst, ex = req(\"GET\", f\"/api/cases/{tok}/export\")\nout[\"A_lib09_rates\"][\"export_after_both_rates\"] = {\"http\": st,\n                                                   \"letter_total_lines\": letter_lines(ex, \"Billed charges\") if st == 200 else None,\n                                                   \"rate_in_letter\": (st == 200 and \"$400\" in ex[\"letter_text\"]),\n                                                   \"rate_lines_in_internal_notes\": [ln for ln in (ex.get(\"internal_notes_text\") or \"\").splitlines() if \"$400\" in ln] if st == 200 else None}\n# accept the two verified charges; the letter total must be the charges only (2,940 + 2,150), rates excluded\nfor i in (\"a1\", \"a4\"):\n    req(\"POST\", f\"/api/cases/{tok}/items/{i}/review\", {\"action\": \"accept\"})\nst, ex = req(\"GET\", f\"/api/cases/{tok}/export\")\nout[\"A_lib09_rates\"][\"export_after_charges\"] = {\"http\": st, \"letter_total_lines\": letter_lines(ex, \"Billed charges\") if st == 200 else None,\n                                               \"totals\": ex.get(\"totals\") if st == 200 else None}\n\n# ---------------------------------------------------------------- B. every acceptable item on the 15 packets\nlibs = [x[\"id\"] for x in req(\"GET\", \"/api/library\")[1][\"cases\"]]\nout[\"B_library_packets\"][\"count\"] = len(libs)\nfor variant in (\"dates_confirmed\", \"dates_unconfirmed\"):\n    for lib in libs:\n        tok = load(lib)\n        if variant == \"dates_confirmed\":\n            for d in req(\"GET\", f\"/api/cases/{tok}\")[1][\"dates_to_confirm\"]:\n                if d.get(\"candidates\"):\n                    req(\"POST\", f\"/api/cases/{tok}/records/{d['record_id']}/confirm_date\", {\"date\": d[\"candidates\"][0]})\n        case = req(\"GET\", f\"/api/cases/{tok}\")[1]\n        accepted, refused = [], []\n        for x in [*case[\"entries\"], *case[\"undated_entries\"], *case[\"amounts\"], *case[\"flags\"]]:\n            st, _ = req(\"POST\", f\"/api/cases/{tok}/items/{x['id']}/review\", {\"action\": \"accept\"})\n            (accepted if st == 200 else refused).append(x[\"id\"] if st == 200 else f\"{x['id']}:{st}\")\n        g = gate(tok)\n        st, ex = req(\"GET\", f\"/api/cases/{tok}/export\")\n        out[\"B_library_packets\"][variant][lib] = {\"accepted\": len(accepted), \"refused\": refused, \"jnr_blockers\": jnr(tok),\n                                                  \"gate_ready\": g[\"ready\"], \"other_blocker_codes\": sorted({b[\"reason_code\"] for b in g[\"blockers\"] if b[\"reason_code\"] != \"JUDGE_NOT_RUN\"}),\n                                                  \"export_http\": st}\n\n# ---------------------------------------------------------------- C. confirm_date gap_changes on lib09 record 4\ntok = load(LIB09)\nflags_before = [f for f in req(\"GET\", f\"/api/cases/{tok}\")[1][\"flags\"] if f[\"type\"] == \"gap\"]\nout[\"C_gap\"][\"before\"] = [{\"id\": f[\"id\"], \"from\": f[\"computed\"].get(\"from\"), \"to\": f[\"computed\"].get(\"to\"), \"days\": f[\"computed\"][\"days\"],\n                           \"record_nos\": f[\"computed\"].get(\"record_nos\")} for f in flags_before]\nst, r = req(\"POST\", f\"/api/cases/{tok}/records/r4/confirm_date\", {\"date\": \"2026-03-05\"})\nout[\"C_gap\"][\"confirm_http\"] = st\nout[\"C_gap\"][\"gap_changes\"] = r.get(\"gap_changes\")\nout[\"C_gap\"][\"gap_flags_returned\"] = r.get(\"gap_flags\")\nflags_after = [f for f in req(\"GET\", f\"/api/cases/{tok}\")[1][\"flags\"] if f[\"type\"] == \"gap\"]\nout[\"C_gap\"][\"after\"] = [{\"id\": f[\"id\"], \"from\": f[\"computed\"].get(\"from\"), \"to\": f[\"computed\"].get(\"to\"), \"days\": f[\"computed\"][\"days\"],\n                          \"record_nos\": f[\"computed\"].get(\"record_nos\")} for f in flags_after]\n\ntext = json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True)\nwith open(OUT, \"w\", encoding=\"utf-8\") as fh:\n    fh.write(text + \"\\n\")\nprint(text)\n"
}
````

### User / tool · 2026-11-02T09:32:10.488Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-paralegal-api-checks.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:32:15.787Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-114-paralegal-api-checks.py > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/run1.stdout 2>&1; echo \"exit $?\"; head -c 300 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/run1.stdout",
 "description": "Run the T-114 API check script against the scratch server",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T09:32:28.678Z

**tool result**
````
exit 0
{
 "A_lib09_rates": {
  "accept_a3": {
   "accept_effect": "acknowledge",
   "http": 200,
   "judge_required_for_export": false,
   "review_status": "accepted",
   "state": "needs_review",
   "total_accepted_cents": 0
  },
  "accept_a6": {
   "accept_effect": "acknowledge",
   "http": 200,
   "revie
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:32:30.548Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-paralegal-api-checks.out.json"
}
````

### User / tool · 2026-11-02T09:32:30.559Z

**tool result**
````
1	{
2	 "A_lib09_rates": {
3	  "accept_a3": {
4	   "accept_effect": "acknowledge",
5	   "http": 200,
6	   "judge_required_for_export": false,
7	   "review_status": "accepted",
8	   "state": "needs_review",
9	   "total_accepted_cents": 0
10	  },
11	  "accept_a6": {
12	   "accept_effect": "acknowledge",
13	   "http": 200,
14	   "review_status": "accepted"
15	  },
16	  "after_both_rates": {
17	   "gate_ready": true,
18	   "jnr": []
19	  },
20	  "export_after_both_rates": {
21	   "http": 200,
22	   "letter_total_lines": [],
23	   "rate_in_letter": false,
24	   "rate_lines_in_internal_notes": [
25	    "- Record 2 (Consultorio Médico Aguaclara, nota de consulta, April 14, 2026): \"Costo por sesión de terapia física: $400.00.\" Rate $400; visit count not stated. Request itemized ledger from Consultorio Médico Aguaclara.",
26	    "- Record 7 (Consultorio Médico Aguaclara, estado de cuenta (billing statement), May 20, 2026): \"Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión.\" Rate $400; visit count not stated. Request itemized ledger from Consultorio Médico Aguaclara.",
27	    "- Entry, record 7 (Consultorio Médico Aguaclara, estado de cuenta (billing statement), May 20, 2026): \"Account statement: consultations $1,300.00; physical therapy, 4 sessions at $400.00 per session. Balance: $2,900.00.\"",
28	    "- Amount $1,300 (unclear), record 7 (Consultorio Médico Aguaclara, estado de cuenta (billing statement), May 20, 2026): \"Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión.\""
29	   ]
30	  },
31	  "export_after_charges": {
32	   "http": 200,
33	   "letter_total_lines": [
34	    "Billed charges stated in these records: $5,090.00"
35	   ],
36	   "totals": {
37	    "charges_cents": 509000,
38	    "charges_count": 2
39	   }
40	  },
41	  "jnr_before_any_accept": [],
42	  "rates": [
43	   {
44	    "accept_effect": "acknowledge",
45	    "id": "a3",
46	    "judge_call_id": "c323ea5028bda",
47	    "judge_required_for_export": false,
48	    "judge_verdict": "agree",
49	    "text": "$400.00"
50	   },
51	   {
52	    "accept_effect": "acknowledge",
53	    "id": "a6",
54	    "judge_call_id": "ca318f9189638",
55	    "judge_required_for_export": false,
56	    "judge_verdict": "agree",
57	    "text": "$400.00"
58	   }
59	  ],
60	  "total_before": {
61	   "cents": 0,
62	   "count": 0,
63	   "label": "Accepted charges"
64	  }
65	 },
66	 "B_library_packets": {
67	  "count": 15,
68	  "dates_confirmed": {
69	   "case_lib01_er_only_then_gap": {
70	    "accepted": 9,
71	    "export_http": 200,
72	    "gate_ready": true,
73	    "jnr_blockers": [],
74	    "other_blocker_codes": [],
75	    "refused": []
76	   },
77	   "case_lib02_slip_fall_prior_knee": {
78	    "accepted": 17,
79	    "export_http": 200,
80	    "gate_ready": true,
81	    "jnr_blockers": [],
82	    "other_blocker_codes": [],
83	    "refused": [
84	     "e4:422"
85	    ]
86	   },
87	   "case_lib03_truck_rear_end_chiro": {
88	    "accepted": 14,
89	    "export_http": 200,
90	    "gate_ready": true,
91	    "jnr_blockers": [],
92	    "other_blocker_codes": [],
93	    "refused": []
94	   },
95	   "case_lib04_dog_bite_scar_revision": {
96	    "accepted": 11,
97	    "export_http": 200,
98	    "gate_ready": true,
99	    "jnr_blockers": [],
100	    "other_blocker_codes": [],
101	    "refused": []
102	   },
103	   "case_lib05_pedestrian_orif_hardware": {
104	    "accepted": 16,
105	    "export_http": 200,
106	    "gate_ready": true,
107	    "jnr_blockers": [],
108	    "other_blocker_codes": [],
109	    "refused": []
110	   },
111	   "case_lib06_lop_billed_vs_adjusted": {
112	    "accepted": 18,
113	    "export_http": 200,
114	    "gate_ready": true,
115	    "jnr_blockers": [],
116	    "other_blocker_codes": [],
117	    "refused": [
118	     "e5:422"
119	    ]
120	   },
121	   "case_lib07_parking_lot_fall_outside_records": {
122	    "accepted": 15,
123	    "export_http": 200,
124	    "gate_ready": true,
125	    "jnr_blockers": [],
126	    "other_blocker_codes": [],
127	    "refused": []
128	   },
129	   "case_lib08_second_crash_mri_after": {
130	    "accepted": 21,
131	    "export_http": 200,
132	    "gate_ready": true,
133	    "jnr_blockers": [],
134	    "other_blocker_codes": [],
135	    "refused": []
136	   },
137	   "case_lib09_spanish_interpreter_espalda": {
138	    "accepted": 19,
139	    "export_http": 200,
140	    "gate_ready": true,
141	    "jnr_blockers": [],
142	    "other_blocker_codes": [],
143	    "refused": []
144	   },
145	   "case_lib10_eob_ub04_cms1500": {
146	    "accepted": 22,
147	    "export_http": 200,
148	    "gate_ready": true,
149	    "jnr_blockers": [],
150	    "other_blocker_codes": [],
151	    "refused": []
152	   },
153	   "case_lib11_priors_and_ledger": {
154	    "accepted": 28,
155	    "export_http": 200,
156	    "gate_ready": true,
157	    "jnr_blockers": [],
158	    "other_blocker_codes": [],
159	    "refused": []
160	   },
161	   "case_lib12_records_review_credibility": {
162	    "accepted": 25,
163	    "export_http": 200,
164	    "gate_ready": true,
165	    "jnr_blockers": [],
166	    "other_blocker_codes": [],
167	    "refused": []
168	   },
169	   "case_lib13_cloned_notes_cross_provider": {
170	    "accepted": 14,
171	    "export_http": 200,
172	    "gate_ready": true,
173	    "jnr_blockers": [],
174	    "other_blocker_codes": [],
175	    "refused": []
176	   },
177	   "case_lib14_handwritten_chiro_scans": {
178	    "accepted": 15,
179	    "export_http": 200,
180	    "gate_ready": true,
181	    "jnr_blockers": [],
182	    "other_blocker_codes": [],
183	    "refused": [
184	     "e5:422"
185	    ]
186	   },
187	   "case_lib15_conclusory_letter_mist": {
188	    "accepted": 27,
189	    "export_http": 200,
190	    "gate_ready": true,
191	    "jnr_blockers": [],
192	    "other_blocker_codes": [],
193	    "refused": []
194	   }
195	  },
196	  "dates_unconfirmed": {
197	   "case_lib01_er_only_then_gap": {
198	    "accepted": 9,
199	    "export_http": 200,
200	    "gate_ready": true,
201	    "jnr_blockers": [],
202	    "other_blocker_codes": [],
203	    "refused": []
204	   },
205	   "case_lib02_slip_fall_prior_knee": {
206	    "accepted": 17,
207	    "export_http": 200,
208	    "gate_ready": true,
209	    "jnr_blockers": [],
210	    "other_blocker_codes": [],
211	    "refused": [
212	     "e4:422"
213	    ]
214	   },
215	   "case_lib03_truck_rear_end_chiro": {
216	    "accepted": 14,
217	    "export_http": 200,
218	    "gate_ready": true,
219	    "jnr_blockers": [],
220	    "other_blocker_codes": [],
221	    "refused": []
222	   },
223	   "case_lib04_dog_bite_scar_revision": {
224	    "accepted": 11,
225	    "export_http": 200,
226	    "gate_ready": true,
227	    "jnr_blockers": [],
228	    "other_blocker_codes": [],
229	    "refused": []
230	   },
231	   "case_lib05_pedestrian_orif_hardware": {
232	    "accepted": 16,
233	    "export_http": 200,
234	    "gate_ready": true,
235	    "jnr_blockers": [],
236	    "other_blocker_codes": [],
237	    "refused": []
238	   },
239	   "case_lib06_lop_billed_vs_adjusted": {
240	    "accepted": 18,
241	    "export_http": 200,
242	    "gate_ready": true,
243	    "jnr_blockers": [],
244	    "other_blocker_codes": [],
245	    "refused": [
246	     "e5:422"
247	    ]
248	   },
249	   "case_lib07_parking_lot_fall_outside_records": {
250	    "accepted": 15,
251	    "export_http": 200,
252	    "gate_ready": true,
253	    "jnr_blockers": [],
254	    "other_blocker_codes": [],
255	    "refused": []
256	   },
257	   "case_lib08_second_crash_mri_after": {
258	    "accepted": 21,
259	    "export_http": 200,
260	    "gate_ready": true,
261	    "jnr_blockers": [],
262	    "other_blocker_codes": [],
263	    "refused": []
264	   },
265	   "case_lib09_spanish_interpreter_espalda": {
266	    "accepted": 19,
267	    "export_http": 200,
268	    "gate_ready": true,
269	    "jnr_blockers": [],
270	    "other_blocker_codes": [],
271	    "refused": [
272	     "e4:422"
273	    ]
274	   },
275	   "case_lib10_eob_ub04_cms1500": {
276	    "accepted": 22,
277	    "export_http": 200,
278	    "gate_ready": true,
279	    "jnr_blockers": [],
280	    "other_blocker_codes": [],
281	    "refused": []
282	   },
283	   "case_lib11_priors_and_ledger": {
284	    "accepted": 28,
285	    "export_http": 200,
286	    "gate_ready": true,
287	    "jnr_blockers": [],
288	    "other_blocker_codes": [],
289	    "refused": []
290	   },
291	   "case_lib12_records_review_credibility": {
292	    "accepted": 25,
293	    "export_http": 200,
294	    "gate_ready": true,
295	    "jnr_blockers": [],
296	    "other_blocker_codes": [],
297	    "refused": []
298	   },
299	   "case_lib13_cloned_notes_cross_provider": {
300	    "accepted": 14,
301	    "export_http": 200,
302	    "gate_ready": true,
303	    "jnr_blockers": [],
304	    "other_blocker_codes": [],
305	    "refused": []
306	   },
307	   "case_lib14_handwritten_chiro_scans": {
308	    "accepted": 15,
309	    "export_http": 200,
310	    "gate_ready": true,
311	    "jnr_blockers": [],
312	    "other_blocker_codes": [],
313	    "refused": [
314	     "e5:422"
315	    ]
316	   },
317	   "case_lib15_conclusory_letter_mist": {
318	    "accepted": 27,
319	    "export_http": 200,
320	    "gate_ready": true,
321	    "jnr_blockers": [],
322	    "other_blocker_codes": [],
323	    "refused": []
324	   }
325	  }
326	 },
327	 "C_gap": {
328	  "after": [
329	   {
330	    "days": 40,
331	    "from": "2026-03-05",
332	    "id": "f_gap_r4_r2",
333	    "record_nos": [
334	     2,
335	     4
336	    ],
337	    "to": "2026-04-14"
338	   }
339	  ],
340	  "before": [
341	   {
342	    "days": 42,
343	    "from": "2026-03-03",
344	    "id": "f_gap_r1_r2",
345	    "record_nos": [
346	     1,
347	     2
348	    ],
349	    "to": "2026-04-14"
350	   }
351	  ],
352	  "confirm_http": 200,
353	  "gap_changes": [
354	   {
355	    "change": "changed",
356	    "flag_id": "f_gap_r4_r2",
357	    "new_days": 40,
358	    "new_from": "2026-03-05",
359	    "new_to": "2026-04-14",
360	    "old_days": 42,
361	    "old_from": "2026-03-03",
362	    "old_to": "2026-04-14",
363	    "sentence": "Gap recalculated after you confirmed record 4: now 40 days (was 42)."
364	   }
365	  ],
366	  "gap_flags_returned": [
367	   "f_gap_r4_r2"
368	  ]
369	 },
370	 "base": "http://127.0.0.1:7881"
371	}
372	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:32:39.579Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport re\np = \"artifacts/review-evidence/T-114-paralegal-api-checks.py\"\ns = open(p, encoding=\"utf-8\").read()\nold = '''            st, _ = req(\"POST\", f\"/api/cases/{tok}/items/{x['id']}/review\", {\"action\": \"accept\"})\n            (accepted if st == 200 else refused).append(x[\"id\"] if st == 200 else f\"{x['id']}:{st}\")'''\nnew = '''            st, body = req(\"POST\", f\"/api/cases/{tok}/items/{x['id']}/review\", {\"action\": \"accept\"})\n            if st == 200:\n                accepted.append(x[\"id\"])\n            else:\n                refused.append({\"id\": x[\"id\"], \"http\": st, \"code\": (body or {}).get(\"error\", {}).get(\"code\") if isinstance(body, dict) else None,\n                                \"message\": (body or {}).get(\"error\", {}).get(\"message\") if isinstance(body, dict) else None, \"kind\": x.get(\"kind\") or x.get(\"type\")})'''\nassert s.count(old) == 1\ns = s.replace(old, new)\nopen(p, \"w\", encoding=\"utf-8\").write(s)\nprint(\"patched\")\nEOF\nPYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-114-paralegal-api-checks.py > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/run2.stdout 2>&1; echo \"exit $?\"; .venv/bin/python -I -c \"\nimport json\nd=json.load(open('artifacts/review-evidence/T-114-paralegal-api-checks.out.json'))\nfor v in ('dates_confirmed','dates_unconfirmed'):\n  for k,x in d['B_library_packets'][v].items():\n    if x['refused']: print(v, k, x['refused'])\nprint('jnr any:', [ (v,k) for v in ('dates_confirmed','dates_unconfirmed') for k,x in d['B_library_packets'][v].items() if x['jnr_blockers'] ])\nprint('export non200:', [ (v,k) for v in ('dates_confirmed','dates_unconfirmed') for k,x in d['B_library_packets'][v].items() if x['export_http']!=200 ])\nprint('gate not ready:', [ (v,k) for v in ('dates_confirmed','dates_unconfirmed') for k,x in d['B_library_packets'][v].items() if not x['gate_ready'] ])\nprint('sum accepted confirmed', sum(x['accepted'] for x in d['B_library_packets']['dates_confirmed'].values()))\n\"",
 "description": "Patch refusal capture to record 422 codes and rerun checks",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T09:32:52.512Z

**tool result**
````
patched
exit 0
dates_confirmed case_lib02_slip_fall_prior_knee [{'code': 'CODE_CHECK_FAILED', 'http': 422, 'id': 'e4', 'kind': None, 'message': 'The summary says “right”, which the quote does not say. Edit the summary to match the quote.'}]
dates_confirmed case_lib06_lop_billed_vs_adjusted [{'code': 'CODE_CHECK_FAILED', 'http': 422, 'id': 'e5', 'kind': None, 'message': 'The summary says “right”, which the quote does not say. Edit the summary to match the quote.'}]
dates_confirmed case_lib14_handwritten_chiro_scans [{'code': 'DATE_UNCONFIRMED', 'http': 422, 'id': 'e5', 'kind': None, 'message': "Confirm this entry's date first (Dates to confirm). An entry with no confirmed date cannot be accepted into the letter."}]
dates_unconfirmed case_lib02_slip_fall_prior_knee [{'code': 'CODE_CHECK_FAILED', 'http': 422, 'id': 'e4', 'kind': None, 'message': 'The summary says “right”, which the quote does not say. Edit the summary to match the quote.'}]
dates_unconfirmed case_lib06_lop_billed_vs_adjusted [{'code': 'CODE_CHECK_FAILED', 'http': 422, 'id': 'e5', 'kind': None, 'message': 'The summary says “right”, which the quote does not say. Edit the summary to match the quote.'}]
dates_unconfirmed case_lib09_spanish_interpreter_espalda [{'code': 'DATE_UNCONFIRMED', 'http': 422, 'id': 'e4', 'kind': None, 'message': "Confirm this entry's date first (Dates to confirm). An entry with no confirmed date cannot be accepted into the letter."}]
dates_unconfirmed case_lib14_handwritten_chiro_scans [{'code': 'DATE_UNCONFIRMED', 'http': 422, 'id': 'e5', 'kind': None, 'message': "Confirm this entry's date first (Dates to confirm). An entry with no confirmed date cannot be accepted into the letter."}]
jnr any: []
export non200: []
gate not ready: []
sum accepted confirmed 271
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:01.956Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; grep -rln \"library\" $A/app/frontend/*.js $A/app/frontend/*.html | head; grep -rn \"data-testid\\|testid\" $A/app/frontend/app.js 2>/dev/null | head -3; grep -rn \"\\\"Open\\|'Open\\|Open: \\|Load sample\\|data-testid\\\", \\\"btn-\\|btn-lib\\|lib-\" $A/app/frontend/*.js | head -12",
 "description": "Locate library load and testids in frontend"
}
````

### User / tool · 2026-11-02T09:33:02.074Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/switcher.js
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/audit.js:55:      el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-audit-case", onclick: () => RV.openAudit(null) }, "Open full audit"));
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/charges.js:53:      el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-source", onclick: () => RV.openSource(a, "amount") }, "Open record " + recSeq(c, (a.record_ids || [])[0])),
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/flags.js:64:        seqs.length > 1 ? "Open records " + joinList(seqs) : "Open record " + seqs[0])));
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/manual.js:89:        el("div", { class: "rv-actions" }, el("button", { type: "button", class: "rv-btn rv-secondary", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], "Record " + r.seq + ": " + r.source_label) }, "Open record " + r.seq)));
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/sidebyside.js:3:   Below 1024 px this module does nothing and the R-RV-9 modal (source.js) is the only source viewer. The explicit "Open record" buttons and
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/review.js:213:    const d = drafts[id] || (drafts[id] = { open: false, text: initial, reasonOpen: false, reason: "" });
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/suggestions.js:158:      const openRec = (rid, seq) => el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-overlap-record", onclick: () => ZL.openSource([{ record_id: rid, start: null, end: null }], "Record " + seq) }, "Open record " + seq);
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/switcher.js:40:        (c.token === cur ? "Open now: " : "Open: ") + c.name, el("span", { class: "cs-meta" }, `${c.status} · ${c.record_count} records` + (k.pending != null ? ` · ${k.pending} pending` : "")))));
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/timeline.js:33:        el("button", { type: "button", class: "btn small", "data-testid": "btn-source", onclick: () => ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : ""}: ${e.provider}`) }, !e.date && rec ? `Open record ${rec.seq}` : "Open record"))].filter(Boolean));
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/stepper.js:226:    judges: ["Open the AI checks", () => gotoPanel("judges")],
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/stepper.js:295:        if (view && !itemId) btn(view[0], view[1]); else if (itemId || recId) btn("Open the record", () => openRecord(itemId, recId), { "aria-label": "Open " + ((itemId && S.cue(itemId)) || "the record").toLowerCase() }); break;
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/stepper.js:302:        if (t.view === "judges" && !(st && st.id === "judges")) btn("Open the AI checks", () => gotoPanel("judges"));
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:05.864Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; ls $A/app/frontend/; grep -rn \"location.hash\\|localStorage\\|sessionStorage\\|searchParams\\|?case=\\|#case\" $A/app/frontend/*.js | head -10; sed -n 1,30p $A/app/frontend/switcher.js | cut -c1-220",
 "description": "Find how the frontend restores a case token"
}
````

### User / tool · 2026-11-02T09:33:05.969Z

**tool result**
````
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
suggestions.js
switcher.js
timeline.js
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/app.js:1:/* Bootstrap: health -> banners; restore case from #case=<token>; poll run status; render on every state change. */
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/app.js:42:    const m = /#\/case\/([^&/]+)/.exec(location.hash);
/* Case switcher (T-053 AC2, local mode only). Shown only when GET /api/cases answers 200 (404 in demo/public mode).
   Lists cases (open with one click) and the synthetic library (POST /cases {library:id}, then run). Text via ZL.el only. */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let root = null, lastToken = undefined, busy = false;

  async function get(path) {
    if (ZL.API_MODE === "mock") return ZL.mock.handle("GET", path);
    const res = await fetch("/api" + path); let body = null;
    try { body = await res.json(); } catch (_) { /* no body */ }
    return { status: res.status, body };
  }
  function say(msg, isError) { const p = root && root.querySelector(".cs-msg"); if (p) { p.textContent = msg || ""; p.setAttribute("role", isError ? "alert" : "status"); } }

  async function openCase(token) {
    const c = await ZL.api.getCase(token);
    history.replaceState(null, "", "#/case/" + encodeURIComponent(token));
    ZL.state.set({ token, created: c.status === "ingested" ? Object.assign({}, c, { record_count: (c.records || []).length }) : null, case: c, status: null });
    if (c.status === "running") ZL.pollRun();
  }
  async function guarded(fn) {
    if (busy) return; busy = true; say("");
    try { await fn(); } catch (e) { say((e && e.message) || "That did not work.", true); } finally { busy = false; }
  }
  const open = (token) => guarded(() => openCase(token));
  const loadLibrary = (id) => guarded(async () => {
    const resp = await ZL.api.createCase({ library: id });
    await openCase(resp.token);
    ZL.state.set({ status: { status: "running", progress: { label: "Starting…" } } });
    await ZL.api.run(resp.token, false); ZL.pollRun();
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:15.935Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-paralegal-ui-rates.py",
 "content": "\"\"\"T-114 paralegal-reviewer UI check: accept the two lib09 rate rows in the browser on the scratch server (b5fb35c archive, :7881).\nRecords what the paralegal sees on the rate row and the summary bar after accept, and whether Export stays open.\nRun: .venv/bin/python artifacts/review-evidence/T-114-paralegal-ui-rates.py [base_url]\nWrites T-114-ui-*.png and T-114-paralegal-ui-rates.out.json next to this file.\n\"\"\"\nimport json\nimport os\nimport re\nimport sys\nimport time\nimport urllib.request\n\nfrom playwright.sync_api import sync_playwright\n\nBASE = sys.argv[1] if len(sys.argv) > 1 else \"http://127.0.0.1:7881\"\nHERE = os.path.dirname(os.path.abspath(__file__))\nLIB09 = \"case_lib09_spanish_interpreter_espalda\"\n\n\ndef api(method, path, body=None):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(BASE + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    with urllib.request.urlopen(r, timeout=120) as x:\n        return json.loads(x.read() or b\"null\")\n\n\ntok = api(\"POST\", \"/api/cases\", {\"library\": LIB09})[\"token\"]\napi(\"POST\", f\"/api/cases/{tok}/run\", {})\nfor _ in range(480):\n    if api(\"GET\", f\"/api/cases/{tok}/status\")[\"status\"] in (\"ready\", \"failed\", \"done_with_errors\"):\n        break\n    time.sleep(0.25)\n\nout = {\"token_prefix\": tok[:6], \"steps\": []}\n\n\ndef row_state(page, item_id):\n    row = page.locator(f'tr[data-item-id=\"{item_id}\"]')\n    return {\"data_review\": row.get_attribute(\"data-review\"), \"data_state\": row.get_attribute(\"data-state\"),\n            \"row_text\": re.sub(r\"\\s+\", \" \", row.inner_text())[:600]}\n\n\ndef summary(page):\n    body = re.sub(r\"\\s+\", \" \", page.inner_text(\"body\"))\n    hits = re.findall(r\"[^.]{0,80}(?:need you|Export blocked|Ready to export|checks passed|blocked by)[^.]{0,60}\", body)\n    return hits[:6]\n\n\nwith sync_playwright() as p:\n    browser = p.chromium.launch()\n    page = browser.new_page(viewport={\"width\": 1440, \"height\": 900})\n    page.goto(f\"{BASE}/#/case/{tok}\")\n    page.wait_for_selector('[data-testid=\"charges-panel\"]', timeout=60000)\n    time.sleep(0.5)\n    out[\"before\"] = {\"a3\": row_state(page, \"a3\"), \"a6\": row_state(page, \"a6\"), \"summary\": summary(page)}\n    page.locator('tr[data-item-id=\"a3\"]').scroll_into_view_if_needed()\n    page.screenshot(path=os.path.join(HERE, \"T-114-ui-1-rates-before-accept.png\"), full_page=False)\n    for item in (\"a3\", \"a6\"):\n        btn = page.locator(f'tr[data-item-id=\"{item}\"] [data-testid=\"btn-accept\"]').first\n        btn.click()\n        time.sleep(1.2)\n        out[\"steps\"].append({\"clicked_accept\": item, a: None} if False else {\"clicked_accept\": item, \"row\": row_state(page, item), \"summary\": summary(page)})\n    page.locator('tr[data-item-id=\"a3\"]').scroll_into_view_if_needed()\n    page.screenshot(path=os.path.join(HERE, \"T-114-ui-2-rates-after-accept.png\"), full_page=False)\n    out[\"after_rates\"] = {\"a3\": row_state(page, \"a3\"), \"a6\": row_state(page, \"a6\"), \"summary\": summary(page),\n                          \"charges_total_text\": re.sub(r\"\\s+\", \" \", page.locator('[data-testid=\"charges-panel\"]').inner_text())[:300]}\n    browser.close()\n\nwith open(os.path.join(HERE, \"T-114-paralegal-ui-rates.out.json\"), \"w\", encoding=\"utf-8\") as fh:\n    json.dump(out, fh, ensure_ascii=False, indent=1)\nprint(json.dumps(out, ensure_ascii=False, indent=1))\n"
}
````

### User / tool · 2026-11-02T09:33:16.036Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-paralegal-ui-rates.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:18.503Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-paralegal-ui-rates.py",
 "old_string": "        out[\"steps\"].append({\"clicked_accept\": item, a: None} if False else {\"clicked_accept\": item, \"row\": row_state(page, item), \"summary\": summary(page)})",
 "new_string": "        out[\"steps\"].append({\"clicked_accept\": item, \"row\": row_state(page, item), \"summary\": summary(page)})"
}
````

### User / tool · 2026-11-02T09:33:18.611Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-paralegal-ui-rates.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:24.677Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 timeout 300 .venv/bin/python artifacts/review-evidence/T-114-paralegal-ui-rates.py > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/ui.stdout 2>&1; echo \"exit $?\"; tail -c 4000 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/ui.stdout",
 "description": "Run Playwright rate-row check against the scratch server",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T09:33:24.766Z

**tool result**
````
exit 127
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:28.852Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python artifacts/review-evidence/T-114-paralegal-ui-rates.py > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/ui.stdout 2>&1; echo \"exit $?\"; tail -c 5000 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/ui.stdout",
 "description": "Run Playwright rate-row check against the scratch server",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T09:33:33.078Z

**tool result**
````
exit 0
or the internal notes only; not in the letter or the total. This figure is a rate, not a charge, so it is not added to the total. AI translation —"
   },
   "summary": [
    " Records (7) Start over Review Case checks 6/10 checks passed 4 need you Ready to export, 19 not reviewed Show How the AI was checked 17 checked, 14",
    " Charges, flags and anything marked needs review always need your own decision"
   ]
  },
  {
   "clicked_accept": "a6",
   "row": {
    "data_review": "accepted",
    "data_state": "needs_review",
    "row_text": "$400.00 Rate rate $400.00; count not stated; needs review Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00. Open record 7How it was checked Needs review Accepted Noted for the internal notes only; not in the letter or the total. This figure is a rate, not a charge, so it is not added to the total. AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it. Accept as noted Dismiss Reset Audit"
   },
   "summary": [
    " Records (7) Start over Review Case checks 6/10 checks passed 4 need you Ready to export, 18 not reviewed Show How the AI was checked 17 checked, 14",
    " Charges, flags and anything marked needs review always need your own decision"
   ]
  }
 ],
 "before": {
  "a3": {
   "data_review": "pending",
   "data_state": "needs_review",
   "row_text": "$400.00 Rate rate $400.00; count not stated; needs review Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00. Open record 2How it was checked Needs review Not reviewed This figure is a rate, not a charge, so it is not added to the total. AI translation — check against the original. This comes from a Spanish (or unid"
  },
  "a6": {
   "data_review": "pending",
   "data_state": "needs_review",
   "row_text": "$400.00 Rate rate $400.00; count not stated; needs review Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00. Open record 7How it was checked Needs review Not reviewed This figure is a rate, not a charge, so it is not added to the total. AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it. Accept as noted Dismiss Audit"
  },
  "summary": [
   " Records (7) Start over Review Case checks 5/10 checks passed 5 need you Export blocked by 1 Show How the AI was checked 17 checked, 14 agreed with th",
   " Charges, flags and anything marked needs review always need your own decision"
  ]
 },
 "after_rates": {
  "a3": {
   "data_review": "accepted",
   "data_state": "needs_review",
   "row_text": "$400.00 Rate rate $400.00; count not stated; needs review Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00. Open record 2How it was checked Needs review Accepted Noted for the internal notes only; not in the letter or the total. This figure is a rate, not a charge, so it is not added to the total. AI translation —"
  },
  "a6": {
   "data_review": "accepted",
   "data_state": "needs_review",
   "row_text": "$400.00 Rate rate $400.00; count not stated; needs review Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00. Open record 7How it was checked Needs review Accepted Noted for the internal notes only; not in the letter or the total. This figure is a rate, not a charge, so it is not added to the total. AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it. Accept as noted Dismiss Reset Audit"
  },
  "summary": [
   " Records (7) Start over Review Case checks 6/10 checks passed 4 need you Ready to export, 18 not reviewed Show How the AI was checked 17 checked, 14",
   " Charges, flags and anything marked needs review always need your own decision"
  ],
  "charges_total_text": "Charges Only charges you accept are counted. Rates, estimates, damages and unreadable amounts are listed below and never added. Accepted charges: $0 Detected, not yet accepted: $5,090 (not a total) Possible double-counting (1) The total above only adds the charges you accepted. It does not remove or"
 }
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:38.998Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nimport json\nd=json.load(open('artifacts/review-evidence/T-114-paralegal-ui-rates.out.json'))\ns=d['steps'][0]\nprint('STEP a3 summary:', s['summary'][0][:260])\nprint('STEP a3 row data_review:', s['row']['data_review'])\nprint('BEFORE summary:', d['before']['summary'][0][:260])\n\"; ls artifacts/review-evidence/ | grep T-114",
 "description": "Print step-by-step summary bar text after each rate accept"
}
````

### User / tool · 2026-11-02T09:33:39.140Z

**tool result**
````
STEP a3 summary:  Records (7) Start over Review Case checks 6/10 checks passed 4 need you Ready to export, 19 not reviewed Show How the AI was checked 17 checked, 14
STEP a3 row data_review: accepted
BEFORE summary:  Records (7) Start over Review Case checks 5/10 checks passed 5 need you Export blocked by 1 Show How the AI was checked 17 checked, 14 agreed with th
T-114-paralegal-api-checks.out.json
T-114-paralegal-api-checks.py
T-114-paralegal-ui-rates.out.json
T-114-paralegal-ui-rates.py
T-114-ui-1-rates-before-accept.png
T-114-ui-2-rates-after-accept.png
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:45.653Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; grep -rn \"blocked by\" $A/app/frontend/*.js | cut -c1-400 | head -5; grep -n \"need you\" $A/app/frontend/stepper.js | cut -c1-300 | head -5",
 "description": "Find the frontend logic behind Export blocked by N"
}
````

### User / tool · 2026-11-02T09:33:45.756Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/judges.js:120:  // gate does not hold is counted as "edited by you, not AI-checked" and never as blocking, so the panel and the rail ("
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/stepper.js:460:  // Collapsed by default at every width to ONE line ("7/10 checks passed · 3 need you · Export blocked by 2") so the 
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive/app/frontend/stepper.js:523:    else if (gate) gateText = "Export blocked by " + (n || 1);
31:    const bits = [[n.pass, "passed"], [n.fail, "failed"], [n.need, n.need === 1 ? "needs you" : "need you"], [n.wait, "not done yet"], [n.skipped, "skipped"]].filter(([k]) => k).map(([k, w]) => k + " " + w);
460:  // Collapsed by default at every width to ONE line ("7/10 checks passed · 3 need you · Export blocked by 2") so the review queue stays on the first screen.
532:        sb.need ? el("span", { class: "zs-sumv", "data-testid": "case-summary-need" }, sb.need + " need you") : null,
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:48.473Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; sed -n 512,526p $A/app/frontend/stepper.js | cut -c1-330",
 "description": "Read gate text logic in stepper.js"
}
````

### User / tool · 2026-11-02T09:33:48.566Z

**tool result**
````
      el("p", { class: "zs-legend" }, "✓ passed · ✕ failed or blocked · – skipped · ○ not done yet. “Needs your decision” means the next move is yours. “Code” steps are done by a program, “AI” steps by a model, “You” steps are your decisions."));
  }
  // The one-line summary: how many checks passed, how many need the human, and what the export is waiting for.
  function summaryBits(steps) {
    const passed = steps.filter((s) => s.status === "pass").length, need = steps.filter((s) => s.status === "fail" || s.status === "pending").length;
    const gate = steps.find((s) => s.id === "export_gate"), bl = (gate && gate.blockers) || [];
    const n = gate ? (gate.counts && gate.counts.blocking) || bl.length : 0;
    let gateText = "";
    const warned = ((gate && gate.warnings) || []).reduce((t, w) => t + (w.count || 0), 0);
    if (gate && gate.status === "pass") gateText = "Ready to export" + (warned ? ", " + warned + " not reviewed" : "");
    else if (bl.length && bl.every((b) => b.reason_code === "RUN_IN_PROGRESS")) gateText = "Export waits for the run to finish";
    else if (gate) gateText = "Export blocked by " + (n || 1);
    return { passed, need, gateText, total: steps.length };
  }
  function paintCase(host, tr) {
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:53.546Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-114-paralegal-gate-before.py <<'EOF'\n\"\"\"T-114 paralegal-reviewer: the export gate's blockers and status on lib09 before any accept, and after accepting only a3 (rate).\nRun: .venv/bin/python -I artifacts/review-evidence/T-114-paralegal-gate-before.py [base_url]\n\"\"\"\nimport json, sys, time, urllib.request\nBASE = sys.argv[1] if len(sys.argv) > 1 else \"http://127.0.0.1:7881\"\ndef req(m, p, body=None):\n    r = urllib.request.Request(BASE + p, data=json.dumps(body).encode() if body is not None else None, method=m, headers={\"content-type\": \"application/json\"})\n    with urllib.request.urlopen(r, timeout=120) as x:\n        return json.loads(x.read() or b\"null\")\ntok = req(\"POST\", \"/api/cases\", {\"library\": \"case_lib09_spanish_interpreter_espalda\"})[\"token\"]\nreq(\"POST\", f\"/api/cases/{tok}/run\", {})\nfor _ in range(480):\n    if req(\"GET\", f\"/api/cases/{tok}/status\")[\"status\"] in (\"ready\", \"failed\", \"done_with_errors\"): break\n    time.sleep(0.25)\ndef gate():\n    g = {s[\"id\"]: s for s in req(\"GET\", f\"/api/cases/{tok}/trace\")[\"steps\"]}[\"export_gate\"]\n    return {\"status\": g[\"status\"], \"counts\": g.get(\"counts\"), \"blockers\": g.get(\"blockers\"), \"warnings\": g.get(\"warnings\")}\nprint(json.dumps({\"before_any_accept\": gate()}, ensure_ascii=False, indent=1))\nreq(\"POST\", f\"/api/cases/{tok}/items/a3/review\", {\"action\": \"accept\"})\nprint(json.dumps({\"after_accept_a3_only\": gate()}, ensure_ascii=False, indent=1))\nEOF\nPYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-114-paralegal-gate-before.py",
 "description": "Print export gate blockers before and after accepting one rate",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T09:33:54.026Z

**tool result**
````
{
 "before_any_accept": {
  "status": "fail",
  "counts": {
   "blocking": 1,
   "pending_items": 20,
   "date_unconfirmed": 1,
   "accepted": 0,
   "dismissed": 0,
   "rejected_not_blocking": 0,
   "judge_not_run": 0,
   "code_check_failed": 0
  },
  "blockers": [
   {
    "item_id": null,
    "kind": "case",
    "reason_code": "NOTHING_ACCEPTED",
    "why": "Nothing is accepted or edited yet, so the letter would be empty.",
    "next_action": {
     "code": "DECIDE",
     "text": "Accept, edit or dismiss this item.",
     "target": {
      "view": "queue"
     }
    }
   }
  ],
  "warnings": [
   {
    "reason_code": "ITEMS_NOT_REVIEWED",
    "count": 20,
    "why": "20 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.",
    "next_action": {
     "code": "DECIDE",
     "text": "Accept, edit or dismiss this item.",
     "target": {
      "view": "queue"
     },
     "options": [
      "accept",
      "edit",
      "dismiss"
     ]
    }
   }
  ]
 }
}
{
 "after_accept_a3_only": {
  "status": "pass",
  "counts": {
   "blocking": 0,
   "pending_items": 19,
   "date_unconfirmed": 1,
   "accepted": 1,
   "dismissed": 0,
   "rejected_not_blocking": 0,
   "judge_not_run": 0,
   "code_check_failed": 0
  },
  "blockers": [],
  "warnings": [
   {
    "reason_code": "ITEMS_NOT_REVIEWED",
    "count": 19,
    "why": "19 items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.",
    "next_action": {
     "code": "DECIDE",
     "text": "Accept, edit or dismiss this item.",
     "target": {
      "view": "queue"
     },
     "options": [
      "accept",
      "edit",
      "dismiss"
     ]
    }
   }
  ]
 }
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:33:58.248Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-ui-2-rates-after-accept.png"
}
````

### User / tool · 2026-11-02T09:33:58.263Z

**tool result**
````
[image]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:34:14.160Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; ls tests/fixtures/llm/ | head; grep -rl \"7328ae58\\|75686283\" tests/fixtures 2>/dev/null | head -5; grep -rl \"7328ae58\" tests/fixtures 2>/dev/null | xargs -I{} grep -o \"\\\"recorded_from\\\"[^}]*\" {} 2>/dev/null | head -3; cd /Users/arsis/zlayt-pm-project && git show --stat b5fb35c | head -30",
 "description": "Check T-114 commit files and the lib09 rate judge fixtures"
}
````

### User / tool · 2026-11-02T09:34:14.323Z

**tool result**
````
00335ec113c1f7234011ea2005f91965f2cc9dcf64aa50c61a8a35672c2b4cf3.json
003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
00c97f20c9cf54c24c8b3275a7382a44877f7bd89ccb0a419716cb030e564104.json
00e8d38a3d50d7d1d7a9b7431c6c2c1970b32930a2583c8a3acd58fdced43d2f.json
010db3ae8de16d72ea8905cdaa07781591d70092d358c0d5e73424940e3cfb33.json
0115c20756060b7547d09ea7174734c62c4d2c54f0cc9840da3f4be1c00e19bb.json
03b065e9490648fde69d807c3f2719201ad149f6e41700f46c81c4258230b20a.json
03dca54059c1c53788cc6e6b66442c557959bc4443f86f86120412b8a7cf4b29.json
03f7de3945171cd4ccf7eed0a80ad8642913484686561e412ec1b8ee9a064d66.json
045838e062f32a8011ad9b74cb5cb6d55f3557d26fd6e1186e3f0fd4e2e6ac86.json
commit b5fb35c743dced9cad3f3dc700e853dc42f4da8e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 03:29:17 2026 -0600

    feat(backend): a rate is acknowledged, never a JUDGE_NOT_RUN blocker; lib09 rate judge fixtures; confirm_date reports gap_changes (T-114)
    
    Rate amounts (D-019/D-042) carry accept_effect=acknowledge and judge_required_for_export=false; trace.judge_not_run_blockers skips them.
    Every acceptable item on all 15 library packets is walked in fixture mode (no JUDGE_NOT_RUN). confirm_date returns gap_changes[] (old to new days).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/present.py                             |   8 +-
 app/backend/review.py                              |  52 ++++++-
 app/backend/trace.py                               |  17 ++-
 memory/contracts/api.md                            |   6 +-
 ...8974f673de7444f5651256517f6dd58ad750210c1e.json |  11 ++
 ...e1d218b48aa43739edead71bb43992d6ddf233f99e.json |  11 ++
 tests/unit/test_t114_rates_and_demo_judges.py      | 155 +++++++++++++++++++++
 tests/unit/test_trace.py                           |   6 +-
 8 files changed, 253 insertions(+), 13 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:34:15.980Z

**tool call — Bash**
````
{
 "command": "git show --name-only --format= b5fb35c | grep fixtures | while read f; do echo \"== $f\"; git show b5fb35c:\"$f\" | head -c 700; echo; done",
 "description": "Show the two new lib09 rate judge fixture files from the commit"
}
````

### User / tool · 2026-11-02T09:34:16.129Z

**tool result**
````
== tests/fixtures/llm/7328ae58fec5ce898068fc8974f673de7444f5651256517f6dd58ad750210c1e.json
{
 "output": {
  "reason_code": "NONE",
  "verdict": "agree"
 },
 "recorded_from": {
  "backend": "claude-cli",
  "model": "claude-haiku-5-5",
  "recorded_at": "2026-11-02T09:22:31Z"
 }
}
== tests/fixtures/llm/756862835a70981555a683e1d218b48aa43739edead71bb43992d6ddf233f99e.json
{
 "output": {
  "reason_code": "NONE",
  "verdict": "agree"
 },
 "recorded_from": {
  "backend": "claude-cli",
  "model": "claude-haiku-5-5",
  "recorded_at": "2026-11-02T09:22:29Z"
 }
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:34:19.250Z

**tool call — Bash**
````
{
 "command": "git show b5fb35c -- tests/unit/test_trace.py | head -60; git show b5fb35c -- app/backend/trace.py | head -80",
 "description": "Show test_trace and trace.py diffs in the T-114 commit"
}
````

### User / tool · 2026-11-02T09:34:19.367Z

**tool result**
````
commit b5fb35c743dced9cad3f3dc700e853dc42f4da8e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 03:29:17 2026 -0600

    feat(backend): a rate is acknowledged, never a JUDGE_NOT_RUN blocker; lib09 rate judge fixtures; confirm_date reports gap_changes (T-114)
    
    Rate amounts (D-019/D-042) carry accept_effect=acknowledge and judge_required_for_export=false; trace.judge_not_run_blockers skips them.
    Every acceptable item on all 15 library packets is walked in fixture mode (no JUDGE_NOT_RUN). confirm_date returns gap_changes[] (old to new days).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_trace.py b/tests/unit/test_trace.py
index a85941f..776f2a5 100644
--- a/tests/unit/test_trace.py
+++ b/tests/unit/test_trace.py
@@ -703,7 +703,8 @@ def test_accepted_items_whose_judge_never_ran_are_gate_blockers_with_a_next_acti
     gate = _gate(c, tok)
     got = _jnr(gate)
     accepted_blanked = {r["id"] for k in ("entry", "amount") for r in DB.list_items(conn, tok, k)
-                        if r["review_status"] in ("accepted", "edited") and "JUDGE_UNAVAILABLE" in r["state_reasons"]}
+                        if r["review_status"] in ("accepted", "edited") and "JUDGE_UNAVAILABLE" in r["state_reasons"]
+                        and not trace.acknowledge_only(k, r)}      # T-114: an accepted rate only acknowledges, it never needs a judge
     assert len(got) >= 5 and n >= len(got)
     assert {b["item_id"] for b in got} == accepted_blanked
     for b in got:
@@ -938,7 +939,8 @@ def test_rejudge_failure_leaves_the_item_unjudged_and_the_gate_closed(env, tmp_p
     app = create_app(str(tmp_path / "copy.sqlite"), call_factory=_fake_factory({s: AU.LLMFailed("x") for s in ("j1", "j2", "j3", "j4")}), static_dir=str(tmp_path))
     c2 = TestClient(app, client=("127.0.0.1", 50000))
     r = c2.post(f"/api/cases/{tok}/rejudge")
-    assert r.status_code == 200 and r.json()["rejudged"] == [] and sorted(x["item_id"] for x in r.json()["still_unavailable"]) == todo
+    rates = sorted(x["id"] for x in DB.list_items(conn, tok, "amount") if x["kind"] == "rate" and x["state"] != "rejected")      # T-114: still re-asked, but never a blocker
+    assert r.status_code == 200 and r.json()["rejudged"] == [] and sorted(x["item_id"] for x in r.json()["still_unavailable"]) == sorted(todo + rates)
     assert r.json()["export_gate"]["ready"] is False and sorted(b["item_id"] for b in r.json()["export_gate"]["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN") == todo
     assert c2.get(f"/api/cases/{tok}/export").status_code == 422
     e = DB.get_item(conn, todo[0], tok)
commit b5fb35c743dced9cad3f3dc700e853dc42f4da8e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 03:29:17 2026 -0600

    feat(backend): a rate is acknowledged, never a JUDGE_NOT_RUN blocker; lib09 rate judge fixtures; confirm_date reports gap_changes (T-114)
    
    Rate amounts (D-019/D-042) carry accept_effect=acknowledge and judge_required_for_export=false; trace.judge_not_run_blockers skips them.
    Every acceptable item on all 15 library packets is walked in fixture mode (no JUDGE_NOT_RUN). confirm_date returns gap_changes[] (old to new days).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/trace.py b/app/backend/trace.py
index 0079329..f46e66c 100644
--- a/app/backend/trace.py
+++ b/app/backend/trace.py
@@ -500,7 +500,10 @@ def _amount_steps(cx, row):
         st.append(step("judge_2", "Second AI check: is this figure a charge, rate or estimate?", "llm", SKIPPED, "Damages and other non-bill figures are not sent to the second check.",
                        reason="AMOUNT_DAMAGES", rule="row 7"))
     else:
-        st.append(_judge_step(cx, row["id"], lad.get("judge"), "j2", R, rule="row 7"))
+        js = _judge_step(cx, row["id"], lad.get("judge"), "j2", R, rule="row 7")
+        if acknowledge_only("amount", row) and js["status"] == SKIPPED and (js.get("evidence") or {}).get("judge_verdict") == "unavailable":
+            js["why"] = "The second check did not run. It is optional for a rate: accepting a rate only acknowledges it, and a rate never reaches the letter."   # T-114
+        st.append(js)
     rs = row["review_status"]
     if kind != "charge" or gfail or row["state"] == "rejected":
         why_t = reason_text(_AMOUNT_CODE[kind]) if kind in _AMOUNT_CODE else "Not a billed charge, so it is not added to the total."
@@ -786,9 +789,17 @@ def unjudged_items(conn, case_id: str) -> list:
     return out
 
 
+def acknowledge_only(kind: str, row: dict) -> bool:
+    """T-114 (D-019/D-042): a figure classified `rate` is never a letter charge, so accepting it only acknowledges it (it is listed in the internal notes, never totaled).
+    No second AI check is needed for that, so a missing one never blocks export. The one source for the amount view's `accept_effect` and the gate."""
+    return kind == "amount" and row.get("kind") == "rate"
+
+
 def judge_not_run_blockers(conn, case_id: str) -> list:
-    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one."""
-    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id) if u["review_status"] in ("accepted", "edited")]
+    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one.
+    A rate (`acknowledge_only`) is the one exception: accepting it only acknowledges it, nothing of it reaches the letter (T-114)."""
+    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id)
+            if u["review_status"] in ("accepted", "edited") and not acknowledge_only(u["kind"], u["row"])]
 
 
 def _jnr_blocker(u):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:34:42.368Z

**tool call — Bash**
````
{
 "command": "grep -n \"gap_changes\\|gap_flags\" app/backend/review.py | head; echo ---FRONTEND; grep -rn \"gap_changes\\|gap_flags\" app/frontend/ | head -5; echo \"(frontend hits above, if any)\"; echo ---; grep -n \"def acknowledge_only\\|def judge_not_run_blockers\\|return \\[_jnr_blocker\" app/backend/trace.py; grep -n \"optional for a rate\" app/backend/trace.py; grep -n \"def accept_effect\" -A3 app/backend/present.py | head -5; grep -n \"\\\"accept_effect\\\"\" app/backend/present.py; echo ---; grep -n \"must_not_flag\" -A3 evals/library/case_lib09_spanish_interpreter_espalda.expected.json | head -6; grep -n \"\\\"gap_excluded_records\\\"\" evals/library/case_lib09_spanish_interpreter_espalda.expected.json; echo ---; grep -n \"R-IN-5\" spec/REQUIREMENTS.md | cut -c1-80",
 "description": "Collect exact line references for the review citations"
}
````

### User / tool · 2026-11-02T09:34:42.516Z

**tool result**
````
353:    gap_changes = []
354:    removed += _recompute_gaps(conn, case_id, t, gap_changes)
355:    for ch in gap_changes:
362:            "entry": moved, "gap_flags": [f["id"] for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"],
363:            "removed_flag_ids": removed, "gap_changes": gap_changes,
400:def _gap_changes(old: dict, new: dict) -> list:
442:    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
471:        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
---FRONTEND
app/frontend/timeline.js:50:  // ---- confirm a date reading (used by Dates to confirm, the flag card's date form and the pre-selected form). T-114: the backend answers with gap_changes[]; every
app/frontend/timeline.js:56:    const changes = (resp && Array.isArray(resp.gap_changes) ? resp.gap_changes : []).map((g) => g && g.sentence).filter(Boolean);
app/frontend/mock.js:157:          records: clone(c.records), dates_to_confirm: clone(c.dates_to_confirm), gap_flags: c.flags.filter((f) => f.type === "gap").map((f) => f.id), record_warning_flags: [], warnings: [] }, 201);
app/frontend/mock.js:211:        return ok({ record: { id: r.id, date_iso: d, date_status: "confirmed", date_raw: r.date_raw }, entry: { id: e.id, date: d, moved_from: "undated_entries" }, gap_flags: [], removed_flag_ids: [], dates_to_confirm: clone(c.dates_to_confirm), warnings: [] });
(frontend hits above, if any)
---
792:def acknowledge_only(kind: str, row: dict) -> bool:
798:def judge_not_run_blockers(conn, case_id: str) -> list:
801:    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id)
505:            js["why"] = "The second check did not run. It is optional for a rate: accepting a rate only acknowledges it, and a rate never reaches the letter."   # T-114
57:def accept_effect(row) -> str:
58-    """What Accept does to an amount (T-114): `letter_total` (a charge: counted in the billed-charges total), `acknowledge` (a rate: noted in the internal notes only,
59-    never totaled, and no second AI check is needed), `internal_notes` (estimate, unclear: noted for the paralegal, never in the total)."""
60-    return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")
66:            "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate"}
---
479:  "must_not_flag": [
480-    {
481-      "id": "N1",
482-      "type": "gap",
219:  "gap_excluded_records": [
---
40:| R-IN-5 | **Dates to confirm.** An entry with an ambiguous date is excluded 
350:| A-105 | Each pasted record carries its date and source on its first line o
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:34:46.848Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; grep -n \"gap_changes\" $A/app/frontend/timeline.js | cut -c1-200; cd /Users/arsis/zlayt-pm-project && git status --short | head -10; git log --oneline -1 -- app/frontend/timeline.js; git show b5fb35c:app/frontend/timeline.js | grep -n \"gap_changes\" | cut -c1-120",
 "description": "Confirm gap_changes handling in HEAD timeline.js and working-tree status"
}
````

### User / tool · 2026-11-02T09:34:47.008Z

**tool result**
````
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
36ceb38 feat(frontend): T-096 pre-selected date suggestion, dismissal banner, measured precision (with stale note), overlap warning, flag tray wording
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:34:53.319Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; cd $A && grep -n \"gap_changes\\|def confirm_date\\|def _gap_changes\\|def _gap_change_sentence\" app/backend/review.py | head -12; grep -n \"def acknowledge_only\\|optional for a rate\\|return \\[_jnr_blocker\\|not acknowledge_only\\|acknowledge_only(u\" app/backend/trace.py; grep -n \"accept_effect\\|judge_required_for_export\" app/backend/present.py; grep -n \"must_not_flag\\|\\\"N1\\\"\\|gap_excluded_records\" evals/library/case_lib09_spanish_interpreter_espalda.expected.json; grep -n \"Gap recalculated\" app/backend/review.py; grep -n \"T-114\" tests/unit/test_t114_rates_and_demo_judges.py | head -3; grep -n \"^def test_\" tests/unit/test_t114_rates_and_demo_judges.py",
 "description": "Collect exact HEAD line numbers for review citations"
}
````

### User / tool · 2026-11-02T09:34:53.492Z

**tool result**
````
330:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
353:    gap_changes = []
354:    removed += _recompute_gaps(conn, case_id, t, gap_changes)
355:    for ch in gap_changes:
363:            "removed_flag_ids": removed, "gap_changes": gap_changes,
400:def _gap_changes(old: dict, new: dict) -> list:
423:def _gap_change_sentence(ch: dict, seq) -> str:
471:        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
505:            js["why"] = "The second check did not run. It is optional for a rate: accepting a rate only acknowledges it, and a rate never reaches the letter."   # T-114
792:def acknowledge_only(kind: str, row: dict) -> bool:
801:    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id)
802:            if u["review_status"] in ("accepted", "edited") and not acknowledge_only(u["kind"], u["row"])]
57:def accept_effect(row) -> str:
66:            "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate"}
219:  "gap_excluded_records": [
479:  "must_not_flag": [
481:      "id": "N1",
429:    return f"Gap recalculated after you confirmed record {seq}: now {ch['new_days']} days (was {ch['old_days']})."
1:"""T-114 (T-060 pass 1 F3/F4): a rate is acknowledged, never offered as a letter accept that later blocks export (D-019/D-042, accept needs no judge);
52:def test_a_rate_accepted_without_a_judge_does_not_block_export_but_a_charge_still_does(client):
82:def test_a_rate_is_never_in_the_letter_total_even_when_accepted(client):
96:def test_walking_every_acceptable_item_on_a_library_packet_never_hits_judge_not_run(client, lib):
118:def test_confirm_date_reports_the_gap_figures_that_changed(client):
132:def test_confirm_date_on_a_phone_note_changes_no_gap(client):
147:def test_gap_changes_pairs_a_moved_endpoint_into_one_change():
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:34:58.547Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json,urllib.request\nB='http://127.0.0.1:7881'\ntok=json.load(urllib.request.urlopen(B+'/api/library'))['cases'][8]\n\" 2>/dev/null; /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<'EOF'\nimport json, urllib.request\nB = \"http://127.0.0.1:7881\"\ndef req(m, p, body=None):\n    r = urllib.request.Request(B + p, data=json.dumps(body).encode() if body is not None else None, method=m, headers={\"content-type\": \"application/json\"})\n    with urllib.request.urlopen(r, timeout=60) as x: return json.loads(x.read() or b\"null\")\ntok = req(\"POST\", \"/api/cases\", {\"library\": \"case_lib09_spanish_interpreter_espalda\"})[\"token\"]\nreq(\"POST\", f\"/api/cases/{tok}/run\", {})\nimport time\nfor _ in range(240):\n    if req(\"GET\", f\"/api/cases/{tok}/status\")[\"status\"] == \"ready\": break\n    time.sleep(0.25)\nc = req(\"GET\", f\"/api/cases/{tok}\")\nfor r in c[\"records\"]:\n    print(r[\"id\"], r[\"seq\"], r[\"source_label\"], \"| date_iso\", r.get(\"date_iso\"), \"| status\", r.get(\"date_status\"), \"| encounter\", r.get(\"encounter\"), \"| dup\", r.get(\"duplicate_of\"))\nEOF",
 "description": "List lib09 records with encounter and date status flags",
 "timeout": 120000
}
````

### User / tool · 2026-11-02T09:34:59.059Z

**tool result**
````
r1 1 Quillmere Regional ED | date_iso 2026-03-03 | status parsed | encounter True | dup None
r2 2 Consultorio Médico Aguaclara, nota de consulta | date_iso 2026-04-14 | status parsed | encounter True | dup None
r3 3 Dr. Lucan Ostrowe, orthopedics, new patient | date_iso 2026-04-21 | status parsed | encounter True | dup None
r4 4 Consultorio Médico Aguaclara, formulario de admisión (OCR) | date_iso None | status ambiguous | encounter True | dup None
r5 5 Cinder Valley Imaging, right shoulder MRI | date_iso 2026-05-05 | status parsed | encounter True | dup None
r6 6 Dr. Lucan Ostrowe, orthopedics, follow-up | date_iso 2026-05-12 | status parsed | encounter True | dup None
r7 7 Consultorio Médico Aguaclara, estado de cuenta (billing statement) | date_iso 2026-05-20 | status parsed | encounter False | dup None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:35:04.032Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; PID=$(cat $S/server.pid); echo \"PID=$PID\"; ps -p $PID -o pid,command | tail -1; kill $PID; sleep 2; ps -p $PID -o pid= || echo \"PID $PID gone\"; curl -s -o /dev/null -w \"port 7881 http=%{http_code}\\n\" http://127.0.0.1:7881/ ; curl -s -o /dev/null -w \"port 7860 http=%{http_code}\\n\" http://127.0.0.1:7860/ ; tail -3 $S/server.log",
 "description": "Stop the scratch review server by PID and confirm the port is closed"
}
````

### User / tool · 2026-11-02T09:35:06.163Z

**tool result**
````
PID=32148
32148 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
PID 32148 gone
port 7881 http=000
port 7860 http=200
llm call failed call_id=c86fe3b87c870 step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
llm call failed call_id=c66e67661d8ac step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
llm call failed call_id=c32ceef29608a step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:35:10.859Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; wc -l < $S/server.log; grep -c \"llm call failed\" $S/server.log; grep -v \"llm call failed\" $S/server.log | head -5; grep \"llm call failed\" $S/server.log | sed 's/call_id=[^ ]*//; s/prompt_hash=[^ ]*//' | sort | uniq -c | head -5",
 "description": "Summarize scratch server log warnings from the walk"
}
````

### User / tool · 2026-11-02T09:35:10.972Z

**tool result**
````
       4
4
   4 llm call failed  step=extract attempt=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:35:18.427Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<EOF\nimport sqlite3, json\ncon = sqlite3.connect(\"file:$S/app.sqlite3?mode=ro\", uri=True)\ncols = [r[1] for r in con.execute(\"PRAGMA table_info(llm_calls)\")]\nprint(\"llm_calls cols\", cols)\nrows = con.execute(\"SELECT * FROM llm_calls\").fetchall()\nidx = {c: i for i, c in enumerate(cols)}\nfails = [r for r in rows if (r[idx.get(\"status\")] if \"status\" in idx else None) not in (None, \"ok\", \"success\")]\nprint(\"total calls\", len(rows), \"non-ok\", len(fails))\nfor r in fails[:6]:\n    print({c: (str(r[idx[c]])[:80]) for c in cols if c in (\"case_id\",\"step\",\"status\",\"attempt\",\"error\",\"item_id\",\"reason_code\")})\nEOF",
 "description": "Inspect scratch DB llm_calls for the failed extract attempts"
}
````

### User / tool · 2026-11-02T09:35:18.548Z

**tool result**
````
llm_calls cols ['id', 'case_id', 'item_id', 'role', 'step', 'backend', 'model', 'prompt_version', 'prompt_sha256', 'system_text', 'user_text', 'response_raw', 'parsed_ok', 'verdict', 'attempt', 'latency_ms', 'cost_usd', 'tokens_in', 'tokens_out', 'recorded_from_json', 'error', 'created_at']
total calls 2184 non-ok 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:35:21.600Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<EOF\nimport sqlite3\ncon = sqlite3.connect(\"file:$S/app.sqlite3?mode=ro\", uri=True)\nrows = con.execute(\"SELECT case_id, step, attempt, parsed_ok, verdict, substr(coalesce(error,''),1,120) FROM llm_calls WHERE error IS NOT NULL AND error != '' OR parsed_ok = 0 LIMIT 12\").fetchall()\nprint(\"error-or-unparsed rows:\", len(rows))\nfor r in rows: print(r)\nprint(\"extract rows\", con.execute(\"SELECT count(*), sum(attempt>1) FROM llm_calls WHERE step='extract'\").fetchall())\nEOF",
 "description": "Query scratch DB for errored or unparsed LLM calls"
}
````

### User / tool · 2026-11-02T09:35:21.709Z

**tool result**
````
error-or-unparsed rows: 4
('OGXlCms0sfkJ-jyhEl_15A', 'extract', 1, 0, None, 'FIXTURE_MISS 83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557')
('9EBVpGfcbJrSXwPb9mKBBA', 'extract', 1, 0, None, 'FIXTURE_MISS 83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557')
('eNlw4yZ05T_pU8BDtHXAnw', 'extract', 1, 0, None, 'FIXTURE_MISS 83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557')
('Eis0l7pJ2IUXv9Gd-Qjf9w', 'extract', 1, 0, None, 'FIXTURE_MISS 83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557')
extract rows [(500, 0)]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:35:27.304Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<EOF\nimport sqlite3\ncon = sqlite3.connect(\"file:$S/app.sqlite3?mode=ro\", uri=True)\ntabs = [r[0] for r in con.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")]\nprint(tabs)\ncols = [r[1] for r in con.execute(\"PRAGMA table_info(cases)\")]\nprint(cols)\nids = [\"OGXlCms0sfkJ-jyhEl_15A\",\"9EBVpGfcbJrSXwPb9mKBBA\",\"eNlw4yZ05T_pU8BDtHXAnw\",\"Eis0l7pJ2IUXv9Gd-Qjf9w\"]\nfor i in ids:\n    r = con.execute(\"SELECT * FROM cases WHERE token=? OR id=?\", (i, i)).fetchone()\n    if r: print({c: str(v)[:60] for c, v in zip(cols, r) if c in (\"name\",\"status\",\"source\",\"record_count\",\"token\",\"id\")})\n    else: print(\"no case row for\", i)\nEOF",
 "description": "Map the four FIXTURE_MISS calls to case names"
}
````

### User / tool · 2026-11-02T09:35:27.412Z

**tool result (error)**
````
Exit code 1
['cases', 'records', 'entries', 'amounts', 'flags', 'llm_calls', 'review_events']
['id', 'name', 'source', 'raw_text', 'text_sha256', 'status', 'stage', 'error', 'backend', 'demo_mode', 'config_json', 'injection_records_json', 'created_at', 'run_started_at', 'run_finished_at']
Traceback (most recent call last):
  File "<stdin>", line 9, in <module>
sqlite3.OperationalError: no such column: token
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:35:30.539Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<EOF\nimport sqlite3\ncon = sqlite3.connect(\"file:$S/app.sqlite3?mode=ro\", uri=True)\nrows = con.execute(\"SELECT l.case_id, c.name, c.status, c.stage, count(*) FROM llm_calls l LEFT JOIN cases c ON c.id = l.case_id WHERE l.error LIKE 'FIXTURE_MISS%' GROUP BY l.case_id\").fetchall()\nfor r in rows: print(r)\nprint(\"cases with status != ready:\", con.execute(\"SELECT name, status, stage, substr(coalesce(error,''),1,100) FROM cases WHERE status NOT IN ('ready')\").fetchall())\nEOF",
 "description": "Map FIXTURE_MISS calls to case names and statuses"
}
````

### User / tool · 2026-11-02T09:35:30.650Z

**tool result**
````
('9EBVpGfcbJrSXwPb9mKBBA', 'case lib01 er only then gap', 'ready', 'finalize', 1)
('Eis0l7pJ2IUXv9Gd-Qjf9w', 'case lib01 er only then gap', 'ready', 'finalize', 1)
('OGXlCms0sfkJ-jyhEl_15A', 'case lib01 er only then gap', 'ready', 'finalize', 1)
('eNlw4yZ05T_pU8BDtHXAnw', 'case lib01 er only then gap', 'ready', 'finalize', 1)
cases with status != ready: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:35:37.697Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<EOF\nimport sqlite3\ncon = sqlite3.connect(\"file:$S/app.sqlite3?mode=ro\", uri=True)\nfor cid in (\"OGXlCms0sfkJ-jyhEl_15A\",\"9EBVpGfcbJrSXwPb9mKBBA\"):\n    n = con.execute(\"SELECT count(*) FROM records WHERE case_id=?\", (cid,)).fetchone()[0]\n    e = con.execute(\"SELECT count(*) FROM entries WHERE case_id=?\", (cid,)).fetchone()[0]\n    print(cid, \"records\", n, \"entries\", e)\nprint(\"lib01 record count in the library listing:\", open(\"/dev/null\").read() or \"see next\")\nEOF\ncurl -s http://127.0.0.1:7881/ >/dev/null 2>&1; cd /Users/arsis/zlayt-pm-project && grep -rn \"record_count\\|lib01\" tests/fixtures/llm/curated* 2>/dev/null | head -2; ls tests/fixtures/llm | grep -v \"^[0-9a-f]\\{64\\}\" | head; grep -c \"\" /dev/null; grep -n \"^Source:\\|^=== Record\" evals/library/case_lib01*.txt | head -12",
 "description": "Compare lib01 stored record counts with the source packet"
}
````

### User / tool · 2026-11-02T09:35:37.849Z

**tool result**
````
OGXlCms0sfkJ-jyhEl_15A records 6 entries 6
9EBVpGfcbJrSXwPb9mKBBA records 6 entries 6
lib01 record count in the library listing: see next
curated
narrative
split
0
3:=== Record 1 ===
5:Source: Dunmarrow Fire-Rescue run report
8:=== Record 2 ===
10:Source: Marrowgate General ED
13:=== Record 3 ===
15:Source: Dr. Imelda Quarrington, primary care
18:=== Record 4 ===
20:Source: Plumtree Physical Therapy, initial evaluation
23:=== Record 5 ===
25:Source: Plumtree Physical Therapy, visit 6
28:=== Record 6 ===
30:Source: Plumtree Physical Therapy, discharge
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:35:55.847Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; grep -rn \"must_not_flag\\|gap_excluded_records\" --include=*.py . | cut -c1-220 | head -8",
 "description": "Check whether any runner enforces the lib09 gap exclusion rule"
}
````

### User / tool · 2026-11-02T09:35:55.966Z

**tool result**
````
research/lexicon_selfcheck.py:8:   hit of the same type overlapping the evidence excerpt), must_not_flag checks, code-list scans
research/lexicon_selfcheck.py:346:        for mn in exp.get("must_not_flag", []):
research/library_build.py:96:    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 14, 21 and 14-day intervals (records 3-4, 4-5, 5-6)."},
research/library_build.py:165:    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 7, 14, 14 and 21-day intervals."}],
research/library_build.py:220:    must_not_flag=[{"id": "N1", "type": "gap", "from_date": "2026-04-09", "to_date": "2026-05-07", "days": 28, "statement": "28-day interval (records 3 to 4) is a near-miss and must NOT be f
research/library_build.py:273:    must_not_flag=[{"id": "N1", "type": "pre_existing", "statement": "No prior-condition flag: the record names none."},
research/library_build.py:335:    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 2, 26, 14 and 21-day intervals."},
research/library_build.py:396:    must_not_flag=[{"id": "N1", "type": "gap", "statement": "No gap flag for the 11 and 21-day intervals; the 2026-06-03 billing statement is not a gap endpoint."}],
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:35:58.737Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; sed -n 340,352p research/lexicon_selfcheck.py | cut -c1-200; grep -rn \"gap_table\\|gap_excluded\" --include=*.py evals research tools tests 2>/dev/null | cut -c1-160 | head -6",
 "description": "Read the must_not_flag enforcement in the lexicon self-check runner"
}
````

### User / tool · 2026-11-02T09:35:58.839Z

**tool result**
````
                should_total += 1
                should_hit += ok
            line = f"  {case} {fl['id']} {fl['type']} {fl['level']}: {'HIT' if ok else 'MISS'}"
            print(line)
            if not ok and fl["level"] == "must":
                golden_fail.append(line.strip())
        for mn in exp.get("must_not_flag", []):
            if mn.get("type") not in ("pre_existing", "causation"):
                continue
            scope = mn.get("record_nos") or list(recs)
            bad = [(n, e["id"], h[2]) for n in scope for e, h in scan(entries, recs[n]["text"], neg, ay)
                   if e["flag_type"] == mn["type"] and e["strength"] in RAISES]
            status = "OK" if not bad else f"VIOLATED {bad}"
evals/run.py:244:    gap_rows = [(r["from_date"], r["to_date"], r["days"], r["flag"]) for r in exp.get("gap_table", [])]
evals/library_build_v2.py:86:    gap_table = []
evals/library_build_v2.py:89:        gap_table.append({"from_date": a, "to_date": b, "from_records": by[a], "to_records": by[b], "days": days, "flag": days > 30
evals/library_build_v2.py:101:    assert {(g["from_date"], g["to_date"]) for g in gap_table if g["flag"]} == {(f["from_date"], f["to_date"]) for f in flags}, sp
evals/library_build_v2.py:125:          "expected_entry_count": len(entries), "gap_excluded_records": excluded, "gap_table": gap_table, "amounts": amounts,
evals/library_build_v2.py:654:              "gaps", [g["days"] for g in ex["gap_table"]])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:36:03.682Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\np = \"artifacts/review-evidence/T-114-paralegal-api-checks.py\"\ns = open(p, encoding=\"utf-8\").read()\nold = 'out[\"C_gap\"][\"confirm_http\"] = st'\nnew = '''out[\"C_gap\"][\"confirm_http\"] = st\nout[\"C_gap\"][\"records_before_confirm\"] = [{\"id\": x[\"id\"], \"seq\": x[\"seq\"], \"source_label\": x[\"source_label\"], \"date_status\": x.get(\"date_status\"),\n                                           \"encounter\": x.get(\"encounter\")} for x in req(\"GET\", f\"/api/cases/{tok}\")[1][\"records\"] if x[\"seq\"] in (1, 2, 4, 7)]'''\nassert s.count(old) == 1\ns = s.replace(old, new)\n# the records read must happen before the confirm; move the list into a pre-confirm read\ns = s.replace('st, r = req(\"POST\", f\"/api/cases/{tok}/records/r4/confirm_date\", {\"date\": \"2026-03-05\"})\\n', 'pre = req(\"GET\", f\"/api/cases/{tok}\")[1][\"records\"]\\nst, r = req(\"POST\", f\"/api/cases/{tok}/records/r4/confirm_date\", {\"date\": \"2026-03-05\"})\\n', 1)\ns = s.replace('out[\"C_gap\"][\"records_before_confirm\"] = [{\"id\": x[\"id\"], \"seq\": x[\"seq\"], \"source_label\": x[\"source_label\"], \"date_status\": x.get(\"date_status\"),\\n                                           \"encounter\": x.get(\"encounter\")} for x in req(\"GET\", f\"/api/cases/{tok}\")[1][\"records\"] if x[\"seq\"] in (1, 2, 4, 7)]',\n              'out[\"C_gap\"][\"records_before_confirm\"] = [{\"id\": x[\"id\"], \"seq\": x[\"seq\"], \"source_label\": x[\"source_label\"], \"date_status\": x.get(\"date_status\"),\\n                                           \"encounter\": x.get(\"encounter\")} for x in pre if x[\"seq\"] in (1, 2, 4, 7)]')\nopen(p, \"w\", encoding=\"utf-8\").write(s)\nprint(\"ok\")\nEOF\ngrep -n \"records_before_confirm\\|pre = req\\|confirm_date\\\"\" artifacts/review-evidence/T-114-paralegal-api-checks.py",
 "description": "Add record encounter flags to the gap section of the API check script"
}
````

### User / tool · 2026-11-02T09:36:03.788Z

**tool result**
````
ok
102:                    req("POST", f"/api/cases/{tok}/records/{d['record_id']}/confirm_date", {"date": d["candidates"][0]})
123:pre = req("GET", f"/api/cases/{tok}")[1]["records"]
124:st, r = req("POST", f"/api/cases/{tok}/records/r4/confirm_date", {"date": "2026-03-05"})
126:out["C_gap"]["records_before_confirm"] = [{"id": x["id"], "seq": x["seq"], "source_label": x["source_label"], "date_status": x.get("date_status"),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:36:08.650Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114; rm -f $S/app2.sqlite3; cd $S/archive && ( env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$S/app2.sqlite3 HOST=127.0.0.1 PORT=7881 PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $S/server2.log 2>&1 & echo $! > $S/server2.pid ); sleep 3; echo \"PID $(cat $S/server2.pid)\"; curl -s -o /dev/null -w \"7881 http=%{http_code}\\n\" http://127.0.0.1:7881/; cd /Users/arsis/zlayt-pm-project && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-114-paralegal-api-checks.py > $S/run3.stdout 2>&1; echo \"checks exit $?\"; .venv/bin/python -I -c \"\nimport json\nd=json.load(open('artifacts/review-evidence/T-114-paralegal-api-checks.out.json'))\nprint('rates accept', d['A_lib09_rates']['accept_a3'])\nprint('export total', d['A_lib09_rates']['export_after_charges']['letter_total_lines'])\nfor v in ('dates_confirmed','dates_unconfirmed'):\n  print(v, 'packets', len(d['B_library_packets'][v]), 'jnr', [k for k,x in d['B_library_packets'][v].items() if x['jnr_blockers']], 'export!=200', [k for k,x in d['B_library_packets'][v].items() if x['export_http']!=200], 'accepted total', sum(x['accepted'] for x in d['B_library_packets'][v].values()))\nprint('C gap_changes', d['C_gap']['gap_changes'])\nprint('C records', d['C_gap']['records_before_confirm'])\nprint('C after', d['C_gap']['after'])\n\"",
 "description": "Restart scratch server, rerun API checks, print key results",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T09:36:08.704Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to $S/run3.stdout)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:36:12.911Z

**tool call — Bash**
````
{
 "command": "curl -s -o /dev/null -w \"7881 http=%{http_code}\\n\" http://127.0.0.1:7881/; ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/ | head -20",
 "description": "Check whether the scratch server restarted"
}
````

### User / tool · 2026-11-02T09:36:13.012Z

**tool result**
````
7881 http=000
app.sqlite3
archive
explore.py
lettercheck.py
rate1.py
run1.stdout
run2.stdout
server.log
server.pid
summ.py
ui.stdout
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:36:23.353Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive && rm -f /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/app2.sqlite3 && ( env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/app2.sqlite3 HOST=127.0.0.1 PORT=7881 PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/server2.log 2>&1 & echo $! > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/server2.pid ); sleep 3; cat /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/server2.pid; curl -s -o /dev/null -w \"7881 http=%{http_code}\\n\" http://127.0.0.1:7881/",
 "description": "Restart the scratch review server on port 7881 with a fresh DB"
}
````

### User / tool · 2026-11-02T09:36:26.496Z

**tool result**
````
41378
7881 http=200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:36:29.037Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-114-paralegal-api-checks.py > artifacts/review-evidence/T-114-api-checks-run.log 2>&1; echo \"checks exit $?\"; .venv/bin/python -I artifacts/review-evidence/T-114-paralegal-api-checks.py >/dev/null 2>&1 ; .venv/bin/python -I -c \"print('noop')\" ; cat artifacts/review-evidence/T-114-paralegal-api-checks.out.json | .venv/bin/python -I -c \"\nimport json,sys\nd=json.load(sys.stdin)\nprint('rate accept a3', d['A_lib09_rates']['accept_a3'])\nprint('export after charges total', d['A_lib09_rates']['export_after_charges']['letter_total_lines'])\nfor v in ('dates_confirmed','dates_unconfirmed'):\n  P=d['B_library_packets'][v]\n  print(v, 'packets', len(P), 'jnr', [k for k,x in P.items() if x['jnr_blockers']], 'export!=200', [k for k,x in P.items() if x['export_http']!=200], 'accepted sum', sum(x['accepted'] for x in P.values()))\nprint('C gap_changes', d['C_gap']['gap_changes'])\nprint('C records', d['C_gap']['records_before_confirm'])\nprint('C after', d['C_gap']['after'])\n\"",
 "description": "Run the API check script on the fresh server and print results",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T09:36:54.596Z

**tool result**
````
checks exit 0
noop
rate accept a3 {'accept_effect': 'acknowledge', 'http': 200, 'judge_required_for_export': False, 'review_status': 'accepted', 'state': 'needs_review', 'total_accepted_cents': 0}
export after charges total ['Billed charges stated in these records: $5,090.00']
dates_confirmed packets 15 jnr [] export!=200 [] accepted sum 271
dates_unconfirmed packets 15 jnr [] export!=200 [] accepted sum 271
C gap_changes [{'change': 'changed', 'flag_id': 'f_gap_r4_r2', 'new_days': 40, 'new_from': '2026-03-05', 'new_to': '2026-04-14', 'old_days': 42, 'old_from': '2026-03-03', 'old_to': '2026-04-14', 'sentence': 'Gap recalculated after you confirmed record 4: now 40 days (was 42).'}]
C records [{'date_status': 'parsed', 'encounter': True, 'id': 'r1', 'seq': 1, 'source_label': 'Quillmere Regional ED'}, {'date_status': 'parsed', 'encounter': True, 'id': 'r2', 'seq': 2, 'source_label': 'Consultorio Médico Aguaclara, nota de consulta'}, {'date_status': 'ambiguous', 'encounter': True, 'id': 'r4', 'seq': 4, 'source_label': 'Consultorio Médico Aguaclara, formulario de admisión (OCR)'}, {'date_status': 'parsed', 'encounter': False, 'id': 'r7', 'seq': 7, 'source_label': 'Consultorio Médico Aguaclara, estado de cuenta (billing statement)'}]
C after [{'days': 40, 'from': '2026-03-05', 'id': 'f_gap_r4_r2', 'record_nos': [2, 4], 'to': '2026-04-14'}]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:36:58.050Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114 && PID=$(cat server2.pid) && echo \"stopping PID $PID\" && ps -p $PID -o pid,command | tail -1 && kill $PID && sleep 2 && (ps -p $PID -o pid= || echo \"PID $PID gone\") && curl -s -o /dev/null -w \"7881 http=%{http_code}\\n\" http://127.0.0.1:7881/ && curl -s -o /dev/null -w \"7860 http=%{http_code} (team app, untouched)\\n\" http://127.0.0.1:7860/",
 "description": "Stop the scratch review server by PID and confirm the port is closed"
}
````

### User / tool · 2026-11-02T09:36:58.104Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No closing quotation) | command: cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf80
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:36:59.845Z

**tool call — Bash**
````
{
 "command": "ps -p 41378 -o pid,command | tail -1; kill 41378; sleep 2; ps -p 41378 -o pid= || echo \"PID 41378 gone\"; curl -s -o /dev/null -w \"7881 http=%{http_code}\\n\" http://127.0.0.1:7881/; curl -s -o /dev/null -w \"7860 http=%{http_code}\\n\" http://127.0.0.1:7860/",
 "description": "Stop review server PID 41378 and confirm port 7881 closed"
}
````

### User / tool · 2026-11-02T09:37:01.975Z

**tool result**
````
41378 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
PID 41378 gone
7881 http=000
7860 http=200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:37:37.995Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\nd=json.load(open('artifacts/review-evidence/T-114-paralegal-api-checks.out.json'))\nrows=[(v,k,x) for v in ('dates_confirmed','dates_unconfirmed') for k,x in d['B_library_packets'][v].items()]\nprint('rows', len(rows))\nprint('gate_ready all true', all(x['gate_ready'] for _,_,x in rows))\nprint('export 200 all', all(x['export_http']==200 for _,_,x in rows))\nprint('jnr empty all', all(x['jnr_blockers']==[] for _,_,x in rows))\nprint('other blocker codes', sorted({c for _,_,x in rows for c in x['other_blocker_codes']}))\nprint('refused', [(v,k,r['id'],r['code']) for v,k,x in rows for r in x['refused']])\nprint('A rates', [(r['id'],r['accept_effect'],r['judge_required_for_export'],r['judge_verdict']) for r in d['A_lib09_rates']['rates']])\nprint('A jnr before/after', d['A_lib09_rates']['jnr_before_any_accept'], d['A_lib09_rates']['after_both_rates'])\nprint('A export after rates', d['A_lib09_rates']['export_after_both_rates']['http'], d['A_lib09_rates']['export_after_both_rates']['rate_in_letter'], d['A_lib09_rates']['export_after_both_rates']['letter_total_lines'])\nprint('total_before', d['A_lib09_rates']['total_before'])\n\"",
 "description": "Verify gate, export, and blocker claims from the saved check output"
}
````

### User / tool · 2026-11-02T09:37:38.104Z

**tool result**
````
rows 30
gate_ready all true True
export 200 all True
jnr empty all True
other blocker codes []
refused [('dates_confirmed', 'case_lib02_slip_fall_prior_knee', 'e4', 'CODE_CHECK_FAILED'), ('dates_confirmed', 'case_lib06_lop_billed_vs_adjusted', 'e5', 'CODE_CHECK_FAILED'), ('dates_confirmed', 'case_lib14_handwritten_chiro_scans', 'e5', 'DATE_UNCONFIRMED'), ('dates_unconfirmed', 'case_lib02_slip_fall_prior_knee', 'e4', 'CODE_CHECK_FAILED'), ('dates_unconfirmed', 'case_lib06_lop_billed_vs_adjusted', 'e5', 'CODE_CHECK_FAILED'), ('dates_unconfirmed', 'case_lib09_spanish_interpreter_espalda', 'e4', 'DATE_UNCONFIRMED'), ('dates_unconfirmed', 'case_lib14_handwritten_chiro_scans', 'e5', 'DATE_UNCONFIRMED')]
A rates [('a3', 'acknowledge', False, 'agree'), ('a6', 'acknowledge', False, 'agree')]
A jnr before/after [] {'gate_ready': True, 'jnr': []}
A export after rates 200 False []
total_before {'cents': 0, 'count': 0, 'label': 'Accepted charges'}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:37:46.894Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; cd $A && echo \"== must_not_flag / gap_excluded readers (HEAD archive)\"; grep -rn \"gap_excluded_records\" --include=*.py . ; grep -rn \"must_not_flag\" --include=*.py tests evals | head -5; echo \"== gap_changes consumers in HEAD frontend\"; grep -rn \"gap_changes\" app/frontend/ ; echo \"(end)\"; echo \"== run.py gap check\"; sed -n 240,250p evals/run.py | cut -c1-160",
 "description": "Confirm no HEAD runner reads gap_excluded_records or consumes gap_changes"
}
````

### User / tool · 2026-11-02T09:37:47.021Z

**tool result**
````
== must_not_flag / gap_excluded readers (HEAD archive)
research/library_build.py:539:          "expected_entry_count": len(entries), "gap_excluded_records": excluded, "gap_table": gap_table, "amounts": amounts,
evals/library_build_v2.py:125:          "expected_entry_count": len(entries), "gap_excluded_records": excluded, "gap_table": gap_table, "amounts": amounts,
evals/golden/check_golden.py:259:    if sorted(excluded) != sorted(ex["gap_excluded_records"]):
evals/golden/check_golden.py:260:        err(cid, f"gap_excluded_records {ex['gap_excluded_records']} != non-encounter/ambiguous records {sorted(excluded)}")
tests/unit/test_flags_sample.py:74:def test_no_spurious_must_not_flags(n):
tests/unit/test_flags_sample.py:75:    """Golden must_not_flag: records 1, 2, 4, 5 carry no pre_existing flag from the floor."""
evals/run.py:231:    for mn in exp.get("must_not_flag", []):
evals/run.py:242:                hits.append({"must_not_flag": mn["id"], "candidate_type": c["type"]})
evals/run.py:246:            "must_not_flag_hits": hits,
== gap_changes consumers in HEAD frontend
(end)
== run.py gap check
                hit = i not in owned and not any(tolerated_match(t, c) for t in exp.get("tolerated", []))
            if hit:
                hits.append({"must_not_flag": mn["id"], "candidate_type": c["type"]})
    gaps = {(c["from_date"], c["to_date"], c["days"]) for c in cands if c["type"] == "gap"}
    gap_rows = [(r["from_date"], r["to_date"], r["days"], r["flag"]) for r in exp.get("gap_table", [])]
    return {"per_type": per, "missed_must": [g["id"] for g in golden if g["level"] == "must" and g["id"] not in matched_ids],
            "must_not_flag_hits": hits,
            "tray_flags": [{"type": f.get("type"), "category": f.get("category"), "reasons": f.get("reasons") or []} for f in tray_flags(out)],
            "gap_rows_wrong": [r[:3] for r in gap_rows if (r[:3] in gaps) != r[3]]}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:37:56.242Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; sed -n 250,262p $A/evals/golden/check_golden.py | cut -c1-220; echo ---; sed -n 479,484p $A/evals/library/case_lib09_spanish_interpreter_espalda.expected.json",
 "description": "Read the golden gap-exclusion check and the N1 wording"
}
````

### User / tool · 2026-11-02T09:37:56.331Z

**tool result**
````
    # ---- gap table: encounters only
    by = {}
    excluded = []
    for r in ex["records"]:
        if r["date"] and r["kind"] == "encounter":
            by.setdefault(r["date"], []).append(r["record_no"])
        else:
            excluded.append(r["record_no"])
    if sorted(excluded) != sorted(ex["gap_excluded_records"]):
        err(cid, f"gap_excluded_records {ex['gap_excluded_records']} != non-encounter/ambiguous records {sorted(excluded)}")
    ds = sorted(by)
    if len(ex["gap_table"]) != max(len(ds) - 1, 0):
---
  "must_not_flag": [
    {
      "id": "N1",
      "type": "gap",
      "statement": "No gap flag for the 7, 14 and 7-day intervals; the ambiguous-date intake (record 4) and the statement of account (record 7) are not gap endpoints."
    }
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:37:59.964Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json\ne=json.load(open('$A/evals/library/case_lib09_spanish_interpreter_espalda.expected.json'))\nfor r in e['records']: print(r.get('record_no'), r.get('kind'), r.get('date'), r.get('date_status', ''), (r.get('source_label') or r.get('source') or '')[:60])\n\" 2>&1 | head -12",
 "description": "Show golden record kinds for lib09 (record 4 classification)"
}
````

### User / tool · 2026-11-02T09:38:00.077Z

**tool result**
````
1 encounter 2026-03-03  Quillmere Regional ED
2 encounter 2026-04-14  Consultorio Médico Aguaclara, nota de consulta
3 encounter 2026-04-21  Dr. Lucan Ostrowe, orthopedics, new patient
4 encounter None  Consultorio Médico Aguaclara, formulario de admisión (OCR)
5 encounter 2026-05-05  Cinder Valley Imaging, right shoulder MRI
6 encounter 2026-05-12  Dr. Lucan Ostrowe, orthopedics, follow-up
7 billing_statement 2026-05-20  Consultorio Médico Aguaclara, estado de cuenta (billing stat
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:38:15.908Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -i \"T-114\" ; echo \"exists-check done\"; ls artifacts/review-evidence/ | grep \"T-114\"",
 "description": "Check whether a T-114 review file already exists"
}
````

### User / tool · 2026-11-02T09:38:16.004Z

**tool result**
````
exists-check done
T-114-api-checks-run.log
T-114-paralegal-api-checks.out.json
T-114-paralegal-api-checks.py
T-114-paralegal-gate-before.py
T-114-paralegal-ui-rates.out.json
T-114-paralegal-ui-rates.py
T-114-ui-1-rates-before-accept.png
T-114-ui-2-rates-after-accept.png
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:38:28.012Z

**tool call — Bash**
````
{
 "command": "grep -c \"^=== Record\" evals/library/case_lib01_er_only_then_gap.txt; ls evals/library | grep lib01",
 "description": "Count record headers in the lib01 source packet"
}
````

### User / tool · 2026-11-02T09:38:28.107Z

**tool result**
````
6
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:38:45.984Z

**tool call — Bash**
````
{
 "command": "A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; cd $A && awk 'NR>=792 && NR<=796 {print NR\": \"substr($0,1,110)}' app/backend/trace.py; awk 'NR==505 {print NR\": \"substr($0,1,110)}' app/backend/trace.py; awk 'NR==429 || NR==363 {print FILENAME\":\"NR\": \"substr($0,1,110)}' app/backend/review.py; awk 'NR>=402 && NR<=404 {print NR\": \"substr($0,1,100)}' app/backend/review.py",
 "description": "Verify exact line numbers for review citations in HEAD"
}
````

### User / tool · 2026-11-02T09:38:46.089Z

**tool result**
````
792: def acknowledge_only(kind: str, row: dict) -> bool:
793:     """T-114 (D-019/D-042): a figure classified `rate` is never a letter charge, so accepting it only acknowle
794:     No second AI check is needed for that, so a missing one never blocks export. The one source for the amount
795:     return kind == "amount" and row.get("kind") == "rate"
796: 
505:             js["why"] = "The second check did not run. It is optional for a rate: accepting a rate only acknow
app/backend/review.py:363:             "removed_flag_ids": removed, "gap_changes": gap_changes,
app/backend/review.py:429:     return f"Gap recalculated after you confirmed record {seq}: now {ch['new_days']} days (was {ch['old_days']
402:     old gap that vanished and a new one that shares a record number with it are ONE `changed` entry 
403:     Each: {flag_id, change, old_days, new_days, old_from, old_to, new_from, new_to}; the side that d
404:     rows = []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:39:11.936Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-114-paralegal.md",
 "content": "# T-114 review: paralegal-reviewer (Maria Delgado persona)\n\nVerdict: **changes** (0 blockers, 1 major, 1 minor, 1 nit). The three asks hold on the running backend. The rate row is acknowledge-only, never blocks export, never reaches the total, and every acceptable item on all 15 library packets exports without JUDGE_NOT_RUN. confirm_date reports the lib09 gap as 42 to 40 days. What is still open is the part of T-060 F4 that is a UI job: the new figure appears with no notice in HEAD.\n\n## What I ran\n\nDeterministic first.\n\n- `git rev-parse HEAD` printed `b5fb35c743dced9cad3f3dc700e853dc42f4da8e`. I extracted `git archive HEAD` into `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive`.\n- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest tests/unit/test_t114_rates_and_demo_judges.py -q -p no:cacheprovider` on that copy printed `20 passed in 7.82s`.\n- Server from the copy: `LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local`, `ZLAYT_DB` in my scratchpad, `HOST=127.0.0.1 PORT=7881`. Started twice (PID 32148, then PID 41378). Both stopped by PID. `curl` to 7881 returns 000 afterwards. The team app on 7860 was not touched (still 200).\n\nLive checks (scripts in `artifacts/review-evidence/`):\n\n- `T-114-paralegal-api-checks.py` (stdlib, run `.venv/bin/python -I`), output `T-114-paralegal-api-checks.out.json`, log `T-114-api-checks-run.log`. Covers the rate accept, the 15 packets in two date variants (dates confirmed to the first candidate; left unconfirmed), and confirm_date on lib09 record 4.\n- `T-114-paralegal-gate-before.py`: lib09 gate before any accept shows `NOTHING_ACCEPTED` (status fail, blocking 1). That explains the \"Export blocked by 1\" the UI shows before any accept. After accepting only a3 the gate is `pass` with `blocking 0` and `judge_not_run 0`. Printed to terminal, not saved.\n- `T-114-paralegal-ui-rates.py` (Playwright, Chromium, 1440x900): opened the lib09 case, accepted both rate rows, read the rows and the summary bar. Screenshots `T-114-ui-1-rates-before-accept.png` and `T-114-ui-2-rates-after-accept.png`; output `T-114-paralegal-ui-rates.out.json`.\n- Code read at HEAD: `app/backend/trace.py:505, 792-801`; `app/backend/present.py:57-66`; `app/backend/review.py:330-363, 400-429`; `evals/library/case_lib09_spanish_interpreter_espalda.expected.json:219-222, 479-483`; `evals/golden/check_golden.py:250-260`.\n- Grep at HEAD: `grep -rn gap_changes app/frontend/` returns nothing. `git show b5fb35c:app/frontend/timeline.js` has no `gap_changes`. The working tree does have a consumer at `app/frontend/timeline.js:50-56`, but it is uncommitted and not in b5fb35c. I did not review it.\n\nResults against the three asks:\n\n1. **lib09 rate row.** Accepting a3 and a6 returns 200 each, with `review_status` accepted, `accept_effect` acknowledge, `judge_required_for_export` false. Accepted total stays 0 cents. Gate after both rates: `ready` true, JUDGE_NOT_RUN list empty, export 200. After also accepting the two verified charges (a1 $2,940 and a4 $2,150), the letter total line is `Billed charges stated in these records: $5,090.00`. The two $400.00 rates appear only in `internal_notes_text`. In the UI the accepted row shows the chips \"Needs review\" and \"Accepted\", and the sentence \"Noted for the internal notes only; not in the letter or the total.\" (see finding 2).\n2. **Every acceptable item on the demo packets.** 15 packets x 2 variants = 30 exports. All 30 gates `ready`, JUDGE_NOT_RUN empty, no other blocker code, export 200. Accepted items: 271 per variant. Seven server refusals in total, all with plain messages and none a judge block: `CODE_CHECK_FAILED` on lib02 e4 and lib06 e5 (summary word not in the quote); `DATE_UNCONFIRMED` on lib14 e5 (both variants) and lib09 e4 (unconfirmed variant only).\n3. **confirm_date gap_changes.** Confirming lib09 record 4 as 2026-03-05 returns `gap_changes` with one entry: `change` changed, `old_days` 42, `new_days` 40, `old_from` 2026-03-03, `new_from` 2026-03-05, both `to` 2026-04-14, and `sentence` \"Gap recalculated after you confirmed record 4: now 40 days (was 42).\" The flag id moves to `f_gap_r4_r2` with `record_nos` [2, 4].\n\nNot exercised: whether the UI offers Accept on the seven refused items; the blank-judge path on the live server (covered only by the unit test, which passed); the rest of the T-060 list.\n\n## Findings\n\n### Major: the 42 to 40 change is reported by the API only; HEAD's UI shows the new figure with no notice\n\nEvidence: `artifacts/review-evidence/T-114-paralegal-api-checks.out.json` (C_gap). `grep -rn gap_changes app/frontend/` on b5fb35c returns nothing. The uncommitted consumer in the working tree is not part of this card.\n\nWhy it matters: T-060 F4 asked that a figure that changes after a decision say so. The backend AC is met, and the handoff says the frontend note stays on T-060. In the build as committed, a paralegal who confirms record 4 sees \"Gap of 40 days\" with no reason, ending at an intake form. The adjuster counts days between treatment encounters, and she needs to know why the number moved.\n\nFix: frontend (under T-060): render `gap_changes[].sentence` beside the gap flag and in the flags tray after confirm_date. The open question of whether an intake form should ever be an endpoint is in questions_for_chris.\n\nAcceptance test: Playwright on lib09 after the frontend commit: confirm record 4 as 2026-03-05. The gap flag card shows \"Gap recalculated after you confirmed record 4: now 40 days (was 42).\" and names the 2026-03-05 start.\n\n### Minor: an accepted rate row still reads \"Needs review\" and keeps a primary \"Accept as noted\" button\n\nEvidence: `artifacts/review-evidence/T-114-ui-2-rates-after-accept.png` (the $400.00 Rate rows show chips \"Needs review\" and \"Accepted\"; primary button \"Accept as noted\"). `T-114-paralegal-ui-rates.out.json` after_rates.a3: `data_review` accepted, `data_state` needs_review.\n\nWhy it matters: the money side is right; the rate is out of the total and does not block export. But an accepted row that still says \"Needs review\" and invites a second Accept looks unfinished, the same pattern as T-060 F6 and F7. The code says \"acknowledge\", the row says \"Accepted\", the sentence says \"Noted\". Pick one.\n\nFix: after acknowledge, the state chip reads something like \"Noted, not in letter\" and the primary control becomes Undo or Reset. Keep the internal-notes sentence.\n\nAcceptance test: lib09 after accepting a3: the row has no \"Needs review\" chip and its primary control is not \"Accept as noted\".\n\n### Nit: the lib01 extract step misses its demo fixture on every run; the case still reaches ready and no record is dropped\n\nEvidence: scratch DB on the first server, `SELECT ... FROM llm_calls WHERE error LIKE 'FIXTURE_MISS%'` returns 4 rows: step extract, attempt 1, parsed_ok 0, error \"FIXTURE_MISS 83bcee077841...\", all on cases named \"case lib01 er only then gap\" (status ready). The lib01 case stored 6 records and 6 entries. `grep -c \"^=== Record\" evals/library/case_lib01_er_only_then_gap.txt` returns 6. I did not trace which path produced the lib01 extraction.\n\nWhy it matters: nothing is lost here, but the demo leans on a logged miss for lib01, which is the kind of demo dead end T-114 set out to close.\n\nFix: record the lib01 extract response in `tests/fixtures/llm/` (curated set), or note the fallback on the card.\n\nAcceptance test: a fixture-mode walk of the 15 packets writes zero FIXTURE_MISS rows to llm_calls.\n\n## Right already\n\n- Accepting a rate is acknowledge-only at every layer I checked. The API says so (`accept_effect` acknowledge, `judge_required_for_export` false). The gate agrees. The letter total excludes it. The UI says it is in the internal notes only.\n- Every acceptable item on the 15 demo packets exports with no JUDGE_NOT_RUN, in both date variants, and every refusal names the next step.\n- The confirm_date response carries old and new endpoints, old and new days, and a plain sentence. The backend side of gap_changes is complete.\n\n```json\n{\"card\": \"T-114\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git archive HEAD = b5fb35c, extracted to /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t114/archive; app http://127.0.0.1:7881 (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local, scratch DB, stopped by PID); sample case: library case_lib09_spanish_interpreter_espalda plus all 15 library packets in two date variants\",\n \"exercised\": [\n  \"git rev-parse HEAD and git cat-file -t b5fb35c (board show T-114 handoff read)\",\n  \"pytest tests/unit/test_t114_rates_and_demo_judges.py on the archive copy: 20 passed in 7.82s\",\n  \"API: lib09 accept a3 and a6 (200, acknowledge, total 0 cents), gate after rates (ready, no JUDGE_NOT_RUN), export letter total with a1 and a4 accepted ($5,090.00), internal notes with the rate lines\",\n  \"API: all 15 library packets, two variants (dates confirmed, dates unconfirmed): 30 gates ready, 0 JUDGE_NOT_RUN, 30 exports 200, 7 plain 422 refusals recorded\",\n  \"API: lib09 confirm_date r4 to 2026-03-05: gap_changes 42 to 40 with sentence; gap flag endpoints before and after; records encounter and date_status\",\n  \"Playwright on lib09 (1440x900): accepted both rate rows in the UI; read the row text and the summary bar; two screenshots\",\n  \"Gate before and after one rate accept (NOTHING_ACCEPTED explains the pre-accept 'Export blocked by 1')\",\n  \"Scratch DB llm_calls query for FIXTURE_MISS rows; lib01 record count versus packet headers\",\n  \"Read app/backend/trace.py, present.py, review.py, evals/golden/check_golden.py, the lib09 expected.json; grep for gap_changes in HEAD frontend (none)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"verify_quickly\": 3, \"rate_row_clarity\": 3, \"export_jnr_free_demo_packets\": 5, \"rate_never_in_total\": 5, \"gap_change_reported_by_api\": 5, \"gap_change_visible_in_head_ui\": 1},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"The lib09 gap change (42 to 40 days) is returned by the API, but HEAD's UI shows the new figure with no notice\",\n   \"evidence\": \"artifacts/review-evidence/T-114-paralegal-api-checks.out.json C_gap.gap_changes[0].sentence = Gap recalculated after you confirmed record 4: now 40 days (was 42).; C_gap.after = f_gap_r4_r2, days 40, from 2026-03-05, record_nos [2,4]. grep -rn gap_changes app/frontend/ on b5fb35c returns nothing. Working-tree consumer app/frontend/timeline.js:50-56 is uncommitted and not in b5fb35c (not reviewed).\",\n   \"why_it_matters\": \"T-060 F4 asked that a figure which changes after a decision say so. The backend AC is met, but in the committed build a paralegal who confirms record 4 sees Gap of 40 days with no reason, ending at an intake form. The adjuster counts days between treatment encounters and needs to see why the figure moved.\",\n   \"fix\": \"Frontend, under T-060: render gap_changes[].sentence beside the gap flag and in the flags tray after confirm_date. Whether an intake form should ever be a gap endpoint is a decision for Chris (questions_for_chris 1).\",\n   \"acceptance_test\": \"Playwright on lib09 after the frontend commit: confirm record 4 as 2026-03-05; the gap flag card shows Gap recalculated after you confirmed record 4: now 40 days (was 42). and names 2026-03-05 as the start.\"},\n  {\"severity\": \"minor\", \"title\": \"An accepted rate row still reads Needs review and keeps a primary Accept as noted button\",\n   \"evidence\": \"artifacts/review-evidence/T-114-ui-2-rates-after-accept.png (chips Needs review and Accepted; primary button Accept as noted; text Noted for the internal notes only; not in the letter or the total.). artifacts/review-evidence/T-114-paralegal-ui-rates.out.json after_rates.a3: data_review accepted, data_state needs_review. app/backend/present.py:57-66 (accept_effect acknowledge).\",\n   \"why_it_matters\": \"The money side is right: the rate is out of the total and does not block export. An accepted row that still says Needs review and invites a second Accept looks unfinished (T-060 F6/F7 pattern). The code says acknowledge, the chip says Accepted, the sentence says Noted.\",\n   \"fix\": \"After acknowledge, the state chip reads something like Noted, not in letter, and the primary control becomes Undo or Reset. Keep the internal-notes sentence.\",\n   \"acceptance_test\": \"lib09 after accepting a3: the row has no Needs review chip and its primary control is not Accept as noted.\"},\n  {\"severity\": \"nit\", \"title\": \"The lib01 extract step misses its demo fixture on every run; the case still reaches ready and no record is dropped\",\n   \"evidence\": \"Scratch DB (first server) query on llm_calls WHERE error LIKE FIXTURE_MISS%: 4 rows, step extract, attempt 1, parsed_ok 0, error FIXTURE_MISS 83bcee077841..., all on case lib01 er only then gap (status ready). Stored 6 records and 6 entries; grep -c ^=== Record evals/library/case_lib01_er_only_then_gap.txt returns 6.\",\n   \"why_it_matters\": \"Nothing is lost, but the lib01 demo depends on a logged fixture miss, the kind of demo dead end T-114 set out to close. I did not trace which path produced the lib01 extraction.\",\n   \"fix\": \"Record the lib01 extract response in tests/fixtures/llm (curated set), or note the fallback on the card.\",\n   \"acceptance_test\": \"Fixture-mode walk of the 15 packets writes zero FIXTURE_MISS rows to llm_calls.\"}\n ],\n \"whats_right\": [\n  \"Accepting a rate is acknowledge-only at every layer checked: API accept_effect acknowledge with judge_required_for_export false, gate agrees, letter total excludes it, UI says it is in the internal notes only.\",\n  \"All 15 library packets export with no JUDGE_NOT_RUN in both date variants (30 of 30 gates ready), and every refusal names the next step.\",\n  \"confirm_date returns old and new endpoints, old and new days, and a plain sentence; the backend side of gap_changes is complete.\"\n ],\n \"questions_for_chris\": [\n  \"Should a dated admission or intake form ever be a gap endpoint? evals/library/case_lib09_spanish_interpreter_espalda.expected.json records entry 4 has kind encounter with date null, and must_not_flag N1 excludes it only as an ambiguous-date intake. Once confirmed, the product counts it (encounter true), so the lib09 figure goes 42 to 40. T-060 F4 says an intake form must never be an endpoint. This changes the number the adjuster sees, so it needs a decision. Whether the gap goes in the demand is litigation-lead's call, outside my lens.\",\n  \"A rate whose second check disagrees (for example SHOULD_BE_CHARGE) still gets acknowledge-only treatment: acknowledge_only() is kind-based (app/backend/trace.py:792-795) and does not read the judge verdict. Should a disagreeing check on a rate force a decision before Accept?\",\n  \"Seven refusals on the demo packets (lib02 e4 and lib06 e5 CODE_CHECK_FAILED; lib14 e5 and lib09 e4 DATE_UNCONFIRMED in one variant). The server messages name the next step. I did not check whether the UI offers Accept on them. Does the T-060 F3 rule (offer only what can be accepted) cover them?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T09:39:12.086Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-114-paralegal.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:39:17.203Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-paralegal-jsoncheck.py",
 "content": "\"\"\"T-114 paralegal-reviewer: parse the single json fence in reviews/T-114-paralegal.md and check the D.2 fields and the verdict rule.\nRun: .venv/bin/python -I artifacts/review-evidence/T-114-paralegal-jsoncheck.py\n\"\"\"\nimport json\nimport os\nimport re\nimport sys\n\nROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\nPATH = os.path.join(ROOT, \"reviews\", \"T-114-paralegal.md\")\nFENCE = \"`\" * 3\ntext = open(PATH, encoding=\"utf-8\").read()\nblocks = re.findall(FENCE + r\"json\\n(.*?)\\n\" + FENCE, text, re.S)\nassert len(blocks) == 1, f\"expected exactly one json fence, found {len(blocks)}\"\nd = json.loads(blocks[0])\nneed = [\"card\", \"persona\", \"model\", \"scope\", \"exercised\", \"verdict\", \"scores\", \"findings\", \"whats_right\", \"questions_for_chris\"]\nmissing = [k for k in need if k not in d]\nassert not missing, missing\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nassert all(s in (\"blocker\", \"major\", \"minor\", \"nit\") for s in sev), sev\nfor f in d[\"findings\"]:\n    for k in (\"title\", \"evidence\", \"why_it_matters\", \"fix\", \"acceptance_test\"):\n        assert f.get(k), (f.get(\"title\"), k)\nexpected = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nassert d[\"verdict\"] == expected, (d[\"verdict\"], expected)\nassert len(d[\"whats_right\"]) <= 3\nassert d[\"persona\"] == \"paralegal-reviewer\" and d[\"card\"] == \"T-114\"\nprint(json.dumps({\"ok\": True, \"verdict\": d[\"verdict\"], \"severities\": sev, \"scores\": d[\"scores\"], \"model\": d[\"model\"]}))\n"
}
````

### User / tool · 2026-11-02T09:39:17.311Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-114-paralegal-jsoncheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:39:18.450Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-114-paralegal-jsoncheck.py",
 "description": "Validate the review JSON block against the D.2 fields and verdict rule"
}
````

### User / tool · 2026-11-02T09:39:18.556Z

**tool result**
````
{"ok": true, "verdict": "changes", "severities": ["major", "minor", "nit"], "scores": {"verify_quickly": 3, "rate_row_clarity": 3, "export_jnr_free_demo_packets": 5, "rate_never_in_total": 5, "gap_change_reported_by_api": 5, "gap_change_visible_in_head_ui": 1}, "model": "claude-haiku-5-5"}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:39:19.704Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-114-paralegal.md 2>&1 | tail -5; echo \"exit=$?\"",
 "description": "Run the board validator on the T-114 review file"
}
````

### User / tool · 2026-11-02T09:39:19.839Z

**tool result**
````
ok (1 file(s))
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:39:23.403Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer && cat MEMORY.md && tail -5 feedback_reviewer_tooling_quirks.md",
 "description": "Read current reviewer memory index and tooling quirks tail"
}
````

### User / tool · 2026-11-02T09:39:23.497Z

**tool result**
````
- [Spec review patterns](feedback_spec_review_patterns.md) — check absolute claims vs the doc's own example; grep every named category/R-ID/fixture
- [Golden-set recurring findings](golden-set-recurring-findings.md) — T-015: must/should levels, shared type+cite flags, export/§6 drift, dead checks via key drift (mutation-test)
- [Reviewer hook constraints](reviewer-hook-constraints.md) — board.py allowed verbs, python heredoc form, write-allowed dirs
- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; review files are append-only (proofread before the one Write)
- [Frontend review patterns](frontend-review-patterns.md) — T-043: mock vs harness coverage, keyboard focus yank, recurring minor gaps
- [Library review patterns](library-review-patterns.md) — T-052 minors; T-077 r2/r3: self-test shape-bound (author-year, prose escape), title-case FAIR Health passes
- [Record-format review patterns](record-format-review-patterns.md) — T-078 r2: mutation-test the check script; visit-count fix creates a PT gap; lib14 specimen gaps
- [Manual entry / split review patterns](manual-entry-split-review-patterns.md) — T-056: AC ticked for absent UI label, split amounts not moving, override trace missing
- [T-068 dates-to-confirm patterns](t068-dates-to-confirm-patterns.md) — orphan confirm dead-ends, record listed twice, text-only AC test, commit vs worktree divergence
- [D-041 date-gate patterns](d041-date-gate-patterns.md) — T-076 r2 (f4ef2ea): stale DATE_AMBIGUOUS fixed; Edit/Change quote still enabled on undated row (T-060)
- [Reviewer API shape gotchas](reviewer-api-shape-gotchas.md) — item GET nests under "item", status "ready", record warnings in case.flags, audit before/after local-only
- [T-079 library v2 patterns](t079-library-v2-patterns.md) — statement-vs-note double count, replay at cited commit, append-only ref proofreading
- The NUCC and CMS PDFs download fine with urllib; write the PDF into review-evidence, run `pdftotext -layout`, then delete the PDF and text.

## T-077 r3 additions (2026-11-01)
- `reviewer-write-guard` makes review files append-only: once `reviews/<card>-<persona>-rN.md` exists, Edit is refused ("reviews are append-only"). Proof-read the review (grep every line ref and quote) BEFORE the single Write; a stale ref cannot be fixed afterwards without a new file.
- A bash `python3 -c` with `\`\`\`` and `\d` escapes was denied by git-guard ("could not parse command safely (No escaped character)"). Move any JSON parse into a Write-created script under artifacts/review-evidence/ and run it.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:39:28.008Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t114-rates-gap-patterns.md",
 "content": "---\nname: t114-rates-gap-patterns\ndescription: T-114 (b5fb35c) review: rate acknowledge-only and demo-packet JNR walk pass; gap change is API-only in HEAD; intake-form encounter classification is a Chris decision; UI leaves accepted rate rows showing Needs review\nmetadata:\n  type: project\n---\n\nT-114 (commit b5fb35c, reviewed 2026-11-02, verdict changes: 1 major, 1 minor, 1 nit) fixed the T-060 F3 rate dead end and the F4 \"say so\" half at the API level.\n\n- Accepting a lib09 rate is `accept_effect` acknowledge and `judge_required_for_export` false (present.py:57-66, trace.py:792-795). It never adds to the total and never blocks export. The UI row still shows chip \"Needs review\" after accept (screenshot T-114-ui-2-rates-after-accept.png).\n- All 15 library packets exported with zero JUDGE_NOT_RUN in both date variants. Refusals are plain 422s: CODE_CHECK_FAILED (lib02 e4, lib06 e5) and DATE_UNCONFIRMED (lib14 e5, lib09 e4 unconfirmed).\n- confirm_date record 4 gives gap_changes 42 to 40. No frontend in HEAD reads gap_changes. The only consumer is uncommitted in the working tree (timeline.js:50-56), so I reviewed HEAD only.\n\n**Why:** the lib09 golden classifies record 4 (formulario de admisión) as kind \"encounter\" with date null. N1 excludes it only as an \"ambiguous-date intake\". Once the date is confirmed it is an endpoint by the golden's own classification. So the 40-day figure is consistent with the golden, and the real question is whether intake forms are encounters. That is Chris's call, not a reviewer's. Also: evals/golden/check_golden.py:259 computes exclusions from kind and ambiguity at ingest only, so no gate checks the post-confirm state.\n\n**How to apply:** when a T-060-style \"intake must never be an endpoint\" finding comes up, check the golden kind first. Do not call it a must_not_flag violation; the N1 text is scoped to ambiguous dates. Related: [[t060-pass1-findings]] is not a file; T-060 lives in reviews/T-060-paralegal-pass1.md.\n"
}
````

### User / tool · 2026-11-02T09:39:28.124Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t114-rates-gap-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:39:30.178Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t114-rates-gap-patterns.md",
 "old_string": "**How to apply:** when a T-060-style \"intake must never be an endpoint\" finding comes up, check the golden kind first. Do not call it a must_not_flag violation; the N1 text is scoped to ambiguous dates. Related: [[t060-pass1-findings]] is not a file; T-060 lives in reviews/T-060-paralegal-pass1.md.",
 "new_string": "**How to apply:** when a T-060-style \"intake must never be an endpoint\" finding comes up, check the golden kind first. Do not call it a must_not_flag violation; the N1 text is scoped to ambiguous dates. The T-060 pass-1 findings are in reviews/T-060-paralegal-pass1.md (F3, F4 are the rate and gap items). Related: [[golden-set-recurring-findings]]."
}
````

### User / tool · 2026-11-02T09:39:30.285Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t114-rates-gap-patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:39:32.870Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md",
 "old_string": "- A bash `python3 -c` with `\\`\\`\\`` and `\\d` escapes was denied by git-guard (\"could not parse command safely (No escaped character)\"). Move any JSON parse into a Write-created script under artifacts/review-evidence/ and run it.",
 "new_string": "- A bash `python3 -c` with `\\`\\`\\`` and `\\d` escapes was denied by git-guard (\"could not parse command safely (No escaped character)\"). Move any JSON parse into a Write-created script under artifacts/review-evidence/ and run it.\n\n## T-114 additions (2026-11-02)\n- board-guard reads a redirect target written as `$VAR/file` inside the same command as \"writes outside reviews/\"; the same redirect with a literal absolute path passes. Use literal paths for `> file` redirects, and put server start/stop in their own calls.\n- git-guard rejected a `kill $(cat pidfile)` chain with echo quotes (\"No closing quotation\"). Use the PID number directly.\n- `timeout` is not installed (already noted); `python3 tools/board.py validate reviews/<file>` works and printed \"ok (1 file(s))\"."
}
````

### User / tool · 2026-11-02T09:39:32.975Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:39:34.659Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-079 library v2 patterns](t079-library-v2-patterns.md) — statement-vs-note double count, replay at cited commit, append-only ref proofreading",
 "new_string": "- [T-079 library v2 patterns](t079-library-v2-patterns.md) — statement-vs-note double count, replay at cited commit, append-only ref proofreading\n- [T-114 rates and gap patterns](t114-rates-gap-patterns.md) — rate acknowledge-only passes; gap change API-only in HEAD; intake-form encounter kind is Chris's call; golden N1 scoped to ambiguous"
}
````

### User / tool · 2026-11-02T09:39:34.761Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T09:39:36.859Z

T-114 verdict is changes (0 blockers, 1 major: the 42→40 gap change has no UI notice in HEAD; plus 1 minor and 1 nit), with rate acknowledge, zero JUDGE_NOT_RUN across 15 packets and the 42→40 API change all confirmed; review at /Users/arsis/zlayt-pm-project/reviews/T-114-paralegal.md.
