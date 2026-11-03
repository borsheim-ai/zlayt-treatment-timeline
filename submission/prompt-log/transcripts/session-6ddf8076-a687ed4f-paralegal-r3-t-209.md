# Subagent: Paralegal r3: T-209 (Paralegal r3: T-209)

Source: `agent-a687ed4fe2a68e6f4.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T02:04:39.136Z

Re-check T-209, round 3 (final), in /Users/arsis/zlayt-pm-project as the senior PI paralegal, starting from a fresh context. The fix commit is 1b3c58a; read reviews/T-209-paralegal-r3.md and the handoff.

Every not-certain reason now shows one next-step sentence. Run a fresh `git archive` in demo mode on your own port and stop your PID afterward.
- Check, for each reason, that the sentence never contradicts the backend note above it. That note still says "Confirm the date from the quote". If it clashes with the new sentence, judge how severe that is.
- Check that the amount and date line stay visible at 1280x900 and 1366x768.

Write reviews/T-209-paralegal-r4.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-opus-5-5 · 2026-11-03T02:04:41.847Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat personas/paralegal.md | head -5; wc -l personas/paralegal.md; cat .claude/agent-memory/paralegal-reviewer/t209-confirm-sentence-patterns.md .claude/agent-memory/paralegal-reviewer/t209-r3-patterns.md .claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md; ls reviews | grep T-209",
 "description": "Read dossier header, memory, list T-209 reviews"
}
````

### User / tool · 2026-11-03T02:04:41.946Z

**tool result**
````
# Persona dossier — paralegal-reviewer

## 1. Identity
**Maria Delgado (fictional), Senior Litigation Paralegal, plaintiff personal-injury firm in Austin, Texas — 9+ years, pre-lit and litigation.**
She has built hundreds of medical chronologies and demand packages in Filevine; her attorney signs the demand, but she is the one the attorney blames when an adjuster finds a date that doesn't match the records. She reviews rather than trusts: anything she cannot click back to the source page does not go in the demand.
      84 personas/paralegal.md
---
name: t209-confirm-sentence-patterns
description: T-209 (88c73dd) Step 3 confirm sentence review: static fill instruction vs no-date lines, dotted-leader resolver miss, unreachable in curated set, card clip; r2 file written because reviews are append-only
metadata:
  type: project
---

T-209 (88c73dd, Step 3 `confirmNext`): verdict changes (2 majors, 5 minors), written as reviews/T-209-paralegal.md and corrected in reviews/T-209-paralegal-r2.md.

- The confirm sentence is static (step3.js:36) and does not branch on sd.reason. For no_date / non_service_date it says "fill in from the highlighted words" while the note above says "request a dated bill, or fill the blank from the record". Highlighted words hold no DOS there. Major.
- Backend resolver misses a labeled DOS when a dotted leader ("99213 ... $250.00") sits between label and amount: reason no_date, so the note says "The line states no date of service." Pre-existing at HEAD (service_date.py), outside the diff. Major.
- Letter prints "date of service [__________] (statement dated X)"; the note names only the blank. Card line doubles the label ("Date of service date of service [...]").
- Foot suppresses "added to the bill total" when confirm_note is set (step3.js:59). Sentence never says counting adds the amount to the total.
- Foot clipped at 1280x900 (clientHeight 149 vs scrollHeight 174) — the last clause is cut.
- Reach: 0 of 16 curated cases produce a confirm note; the guided test injects it via route rewrite.

**Why:** the review is about what Maria copies into the letter. The fill instruction is the trap (birth or statement date copied into the DOS blank).
**How to apply:** on any Step 3 / confirm-note review, branch the wording by reason, check the parenthetical, check the total line, and measure the foot at 1280x900.

Process lessons (tooling):
- reviewer-write-guard blocks Edit on an existing review file ("reviews are append-only — write a new file (e.g. -r2/-r3 suffix)"). I wrote a summary headline with wrong severity counts ("four majors and three minors" vs 2 and 5) and could not fix it in place. Recount severities from the JSON BEFORE the one Write; the JSON is authoritative.
- Playwright route callbacks receive (route, request): a def rewrite(route, sd=sd) default arg gets overwritten by the Request object. Use a closure factory.
- localhost:7860 listener (PID 22647 at the time) returned 404 for POST /api/cases: stale process. Serve the commit under review from `git archive <sha>` on a free port (7871 was taken by someone else; 7893 free) with `PORT=... ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_DB=<scratch> .venv/bin/python -m app.main` from the export dir.
- The library list endpoint returns {"cases":[{"id":...}]}; use the id, not the human name.
- Reviewer ran as claude-haiku-5-5 this time (persona expects Opus for judgment reviewers): flagged as a question, not hidden.

Related: [[t202-r2-non-service-date-patterns]], [[t200-undated-charge-label]], [[t181-r2-patterns]], [[reviewer-run-pitfalls-pass4]]
---
name: t209-r3-patterns
description: T-209 r3 (8521562) changes: one DOUBTFUL branch says fill from highlight for 6 written reasons; note says record does not settle; taller foot hides body date line
metadata:
  type: project
---

T-209 r3 (8521562, frontend step3.js confirmNext branches on sd.reason): verdict changes, 1 major / 4 minor / 1 nit, reviews/T-209-paralegal-r3.md.

- The no_date and non_service_date branch is good: it never mentions the highlighted words and agrees with the note.
- Major: all six written reasons share one sentence, "Fill the blank with the date you checked in the highlighted words". The notes for ambiguous_numeric ("record does not settle which"), several_dates, no_year, invalid and implausible say the highlight cannot supply the date. Only two_digit_year can be filled from it. My own r1 fix wording caused this. Lesson: when I propose fix wording, test it against every sub-reason before I write it.
- Regression from the r2 clip fix: `.card-f:has(.svc-next)` grows to 300px, so the card body shrinks to 40-56px. The date line, which the sentence calls "the date in parentheses", and the amount are hidden at 1280x900 and 1366x768. Playwright is_visible() does not catch covered elements; use elementFromPoint.
- "If you don't, it stays out of the letter" comes right after "Fill the blank": the antecedent is ambiguous.
- Demo mode = fixture backend (health demo_mode true). Library cases still need ZLAYT_MODE=local, which keeps demo_mode true.

**Why:** the brief's bar is that each reason's sentence is exact and never contradicts the note. **How to apply:** for any confirm-note review, walk all 8 REASONS (artifacts/review-evidence/T-209-r3-paralegal-walk.py, body-clip.py) and check occlusion, not only scroll.

Related: [[t209-confirm-sentence-patterns]], [[t202-r3-allow-list-patterns]]
---
name: reviewer-run-pitfalls-pass4
description: T-060/T-114 pass-4 run pitfalls: HEAD moves mid-review (pin by hash, run both if brief says HEAD and card names a commit); venv path relative from subdirs (exit 127); sed -i blocked again; Playwright selectors for case list, disclosure, confirm-date radios; reload restores the case
metadata:
  type: reference
---

- HEAD moved during the review: 433ac1c became f7829c1 while I worked (other agents commit). Record the hash you archived with `git rev-parse --short HEAD` at the start AND `git archive <hash>`. When the brief says HEAD and the card names a commit (e293daa), run both and say which commit each finding applies to. Check `git diff --stat <card-commit> HEAD -- app/frontend` (empty = same UI).
- Server launch: `env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=<scratch db> PORT=<p> HOST=127.0.0.1 .venv/bin/python -I artifacts/review-evidence/<card>-paralegal-pass4-serve.py <archive_root>` (runpy, puts the archive root first on sys.path). Background launch: the launcher task exits 0 while the listener lives; get the listener PID with `lsof -iTCP:<p> -sTCP:LISTEN -nP`, kill by number, confirm curl = 000. Port 7860 is the live dev app; never touch it.
- `.venv/bin/python` is relative: from artifacts/review-evidence/<card>/ it exits 127. Run from repo root.
- `sed -i` is refused by board-guard again (pass 4). Use the Edit tool on scripts and memory; check `grep -c` after.
- Playwright selectors (e293daa/HEAD): case list buttons are `[data-testid=case-<token>]`; library entries `[data-testid=library-case_lib09_spanish_interpreter_espalda]` sit inside a collapsed disclosure: click `summary:has-text('synthetic library')` first. The lib09 names repeat ("Spanish-language records, back pain") and differ only by token: never pick by name. Date step: `button:has-text('1 date to confirm')`; radios via `get_by_label("March 5, 2026")`; confirm `get_by_role("button", name="Confirm date")`; there is NO `form[data-testid=confirm-date]` in this build. Gap notice `[data-testid=gap-change-note]`; dismiss it `[data-testid=btn-dismiss-gap-note]`. Dismissed entries group `[data-testid=dismissed-summary]`. Export `[data-testid=btn-export]`, letter `[data-testid=export-letter]` (a PRE, read innerText not value), copy `[data-testid=btn-copy-letter]`, download `[data-testid=btn-download-letter]`.
- Keyboard: `a` on a flag or amount acts on it; `d` on a flag dismisses without a reason prompt; `e` opens the textarea only when focus is on the row, and Ctrl+Enter saves.
- Reload restores the last case view (no paste page), so a probe that expects the paste box after reload will time out. Use the case list or continue on the restored case.
- Output discipline: write every probe's output with `> file` in the same call; console-only numbers do not count as evidence when the review quotes them.
- Review files are write-once: proofread every line reference with grep before the single Write (api.md:341 D-045b checked; the erratum route is the final reply).

Why: all of these cost a probe rerun or an unfixable review line during the T-060/T-114 pass-4 run.
How to apply: start each Playwright run with `curl` on the port, confirm the archive hash, and keep one helper module per card. Related: [[reviewer-tooling-quirks]], [[reviewer-api-shape-gotchas]], [[t060-pass4-state-patterns]], [[t114-r3-gap-change-persistence]].
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

## T-114 additions (2026-11-02)
- board-guard reads a redirect target written as `$VAR/file` inside the same command as "writes outside reviews/"; the same redirect with a literal absolute path passes. Use literal paths for `> file` redirects, and put server start/stop in their own calls.
- git-guard rejected a `kill $(cat pidfile)` chain with echo quotes ("No closing quotation"). Use the PID number directly.
- `timeout` is not installed (already noted); `python3 tools/board.py validate reviews/<file>` works and printed "ok (1 file(s))".

## T-116 r2 additions (2026-11-02)
- `reviewer-write-guard` also refuses Write to the session scratchpad ("reviewers write only under reviews/ or artifacts/review-evidence/").
  Put probe copies, extracted archives and JSON checkers under artifacts/review-evidence/ (run with `.venv/bin/python -I`). `git archive`
  extraction into the scratchpad via Bash worked.
- The review file was refused a second write once it existed, so a wrong body sentence (I wrote "a scratchpad archive path that no longer
  exists" without checking it, and mislabeled a record) could not be fixed. Before the single Write: `ls` every path and grep every record
  label you quote.
- `bash python3 -c "... \`\`\` ..."` was denied again by git-guard. The JSON check now lives in artifacts/review-evidence/<card>-paralegal-r2-jsoncheck.py.

## T-114 r2 additions (2026-11-02)
- `nohup .venv/bin/python -m app.main ... &` then `kill $!` left the listener alive: the launcher PID exited, and the server
  (a child, re-parented to launchd, ppid 1) kept 7881 open and returned 200. Always `lsof -iTCP:<port> -sTCP:LISTEN -nP` after a
  kill, kill the listener PID too, and confirm `curl` returns 000. Name both PIDs in the review scope.
- reviewer-write-guard refused an Edit on reviews/T-114-paralegal-r2.md (append-only). A wrong scope PID could not be fixed; it went into the final reply.
  Before the single Write, check every PID, path and count with a command, not from memory.
- The board validator only checks files under reviews/. Pre-check a draft JSON with a script in artifacts/review-evidence/ (T-114-r2-paralegal-jsoncheck.py).

## T-116 r3 additions (2026-11-02)
- The r3 review was written once and then contained one wrong claim (a grep "returns 1 from the H3V5 line only" that was actually the line-29
  orchestrator note). Edit on the existing review was refused by `reviewer-write-guard`, so the erratum went into the final reply instead.
  Rule: before the single Write, run the exact grep again and quote its line numbers; do not describe a match you have not printed.
- `python3 -c` with `\`\`\`json` in the string was denied by git-guard again (parse error). The JSON check is `artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py`
  run with `.venv/bin/python -I <script> <review>`; it works for any review path.
- `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider` keeps the dirty project tree free of new .pytest_cache and .pyc writes.

## T-120 r4 additions (2026-11-02)
- git-guard denies `git show "$c:$f"` and any git call with a shell variable in the subcommand or a `for` loop with `${var%%:*}` ("dynamic git subcommand is not allowed", "unresolved variable in command position"). Use literal git commands, or a script under artifacts/review-evidence/ run with `.venv/bin/python -I` (T-120-r4-archive-check.py does this).
- The Write tool and board-guard accept a `cp` of a finished draft from artifacts/review-evidence/ to reviews/<new file>; that let me proof a draft JSON with the jsoncheck and then publish the identical text in one step.
- `kill` by PID, then `lsof -iTCP:<port> -sTCP:LISTEN -nP` (exit 1 = closed) and `curl` 000, worked for four server pairs.

## T-120 r2 additions (2026-11-02)
- The guard refused Edit on reviews/T-120-paralegal-r2.md right after the single Write (the name has no -rN suffix, so it is treated as existing and append-only). Two wording slips were found after the Write: "lib02 and lib11 keep their prior flags" (I had not compared them to the pre-T-120 build) and "r2 handoff" (the line is the r2 backend note). They could not be fixed in the file; they went into the one-line reply.
- Before the Write, check each "keeps / still / unchanged" claim against a run you have actually done, not against memory of the build.

## T-060 pass 5 additions (2026-11-02)
- Playwright `new_page` with a fresh browser context is a fresh visit, not a reload; a same-page `pg.reload()` does restore the case. Probe a reload in the same page.
- Letter keys do nothing until an item is selected: after opening a case, click Start review (or a row edge) before j, a, d.
- Probe scripts that walk with j/a can stop early because `a` auto-advances within a kind; check the focus item after every key and reach skipped items with k or j, not by assumption.
- A ```json regex that captures a trailing colon in an evidence path reports a false "missing path"; the file exists. Strip `:` in the checker.
- Write the draft under artifacts/review-evidence/<card>-paralegal-pass5/, run the jsoncheck, then `cp` to reviews/ in one Bash call; board.py validate returned "ok (1 file(s))".
T-209-paralegal-r2.md
T-209-paralegal-r3.md
T-209-paralegal.md
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:04:42.946Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-03T02:04:42.954Z

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

### Assistant · claude-opus-5-5 · 2026-11-03T02:04:43.447Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-209-paralegal-r3.md"
}
````

### User / tool · 2026-11-03T02:04:43.460Z

**tool result**
````
1	# T-209 review r3 — paralegal-reviewer (Maria Delgado persona)
2	
3	Scope: fix commit 8521562 (`app/frontend/guided/step3.js:32-43`, `app/frontend/guided/step3.css:22`, `tests/e2e/guided/test_t206.py`). HEAD is 8521562, and `git diff --stat 88c73dd 8521562 -- app/backend app/llm` is empty, so the backend note wording is the same as in round 2. I served a fresh `git archive 8521562` in demo mode (fixture backend, `/api/health` returned `"demo_mode":true`) on 127.0.0.1:7931, listener PID 43905. I stopped it afterward: `lsof` exit 1, `curl` 000. Synthetic data only. As the brief asked, I did not grade the round-2 major 2 (dotted leader, T-202).
4	
5	Verdict: **changes**. No blocker. One major, four minors, one nit.
6	
7	For each reason, here is what the card says and whether a paralegal can act on it:
8	
9	- **No date (`no_date`)** works. The note says "Request a dated line-by-line bill, or fill the blank from the record". The sentence says "find the date of service in the record or ask the provider ... Fill the blank with that date." The two agree, and the sentence no longer points at the highlighted words. One minor: "the record" on this card is the bill that has no date.
10	- **Non-service date (`non_service_date`)** works too. The note names the unlabeled date and says it "may be a birth, injury, ... posting, statement or transaction date". The sentence sends her outside the quote. Same minor as above.
11	- **Doubtful written date** (six reasons) still has the problem. The sentence always says "Fill the blank with the date you checked in the highlighted words." For `ambiguous_numeric` the note above says "the record does not settle which". For `several_dates` it says "nothing says which one belongs to this charge". For `no_year` the highlighted words have no year. For `invalid` (02/30/2026) and `implausible` (09/14/2026 on a June 15 statement), following the sentence puts a date the note calls wrong into the demand. Only `two_digit_year` can be filled from the highlighted words. My own round-1 fix wording ("fill ... with the date the highlighted words label") caused this. It is still a finding.
12	
13	Round-2 items that are fixed: the branch by reason exists; the foot no longer scrolls (20 of 20 reason/viewport runs show scrollHeight equal to clientHeight); the doubled "Date of service" label is gone; the statement-date sentence and the count/total consequence are added. One new problem came with the taller foot: it now hides the card's date line, the one the sentence calls "the date in parentheses". I measured this for ambiguous_numeric at 1280x900 and for ambiguous_numeric and no_date at 1366x768. In the walk, the foot is just as tall for the other reasons: 294 px at 1280x900 for every written reason and non_service_date, and 218-266 px for every reason at 1366x768.
14	
15	---
16	
17	```json
18	{"card": "T-209", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
19	 "scope": "fix commit 8521562 (app/frontend/guided/step3.js:32-43, step3.css:22, tests/e2e/guided/test_t206.py); HEAD 8521562; backend unchanged since 88c73dd (git diff --stat 88c73dd 8521562 -- app/backend app/llm: empty); app served from a fresh git archive of 8521562 in demo mode (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, health demo_mode true) at http://127.0.0.1:7931, listener PID 43905, stopped (lsof exit 1, curl 000); case_lib10_eob_ub04_cms1500 a2 with the backend's own service_date dict injected per reason. Round-2 major 2 (dotted leader, T-202) not graded per brief.",
20	 "exercised": [
21	  "Read personas/paralegal.md in full, reviews/T-209-paralegal-r2.md (round 1), board.py show T-209 (handoff: branch on sd.reason; minors 3-6 fixed; minor 7 and major 2 not fixed)",
22	  "git show 8521562 -- app/frontend tests (step3.js +12/-4, step3.css +2, test_t206.py +35)",
23	  "git show 8521562:app/backend/service_date.py lines 93-108 (_WHY per reason, _ASK_WRITTEN, _ASK_NONE, confirm_note)",
24	  "pytest tests/e2e/guided/test_t206.py tests/e2e/guided/test_t205.py from the archive against 127.0.0.1:7931: 11 passed (artifacts/review-evidence/T-209-r3-paralegal-pytest.txt)",
25	  "artifacts/review-evidence/T-209-r3-paralegal-walk.py -> T-209-r3-paralegal-walk.json: Chromium, 10 constructed bill lines resolved by the archive's store.charge_service_date (ambiguous_numeric, two_digit_year, no_year, invalid, several_dates, implausible, two non_service_date, two no_date), each injected into lib10 a2, read at 1280x900 and 1366x768 (20 runs): date line, confirm note, next-step sentence, data-reason, foot scroll box, answer-button position, console errors; screenshots T-209-r3-step3-<reason>.png",
26	  "artifacts/review-evidence/T-209-r3-paralegal-body-clip.py -> T-209-r3-paralegal-body-clip.json: card-body scroll box, figure and service-date visibility (rect inside the visible body plus elementFromPoint) at 1280x900, 1366x768 and 1920x1080, with a no-injection control; screenshots T-209-r3-body-*.png",
27	  "Read screenshots T-209-r3-step3-ambiguous_numeric.png and T-209-r3-body-no_date-1366x768.png",
28	  "Resolver probe at 8521562 for non_service_date lines ('Office visit 03/04/2026 99213 - $250.00', 'Posted 06/01/2026 ...', 'DOB 03/04/1980, $250.00' -> non_service_date; 'Date of injury 03/04/2026. ...' -> no_date)",
29	  "Did not press Yes or No (an injected sd is not what the backend exports); the letter wording for a counted blank line was verified in round 2 and export.py/service_date.py are unchanged since"
30	 ],
31	 "verdict": "changes",
32	 "scores": {"verify_quickly": 3, "next_step_exact_no_date": 4, "next_step_exact_non_service_date": 4, "next_step_exact_doubtful_written_date": 2, "never_contradicts_note": 2},
33	 "findings": [
34	  {"severity": "major",
35	   "title": "Doubtful written date: the sentence tells her to fill the blank from the highlighted words, but the note above says those words cannot settle the date (ambiguous, several dates) or that the written date is incomplete or wrong (no year, invalid, implausible)",
36	   "evidence": "step3.js:36 puts all six written reasons in one DOUBTFUL list and step3.js:41 gives each the same text. Walk at 1280x900 (T-209-r3-paralegal-walk.json, all data-reason 'doubtful'), NEXT for every one: 'Fill the blank with the date you checked in the highlighted words.' NOTE per reason: ambiguous_numeric 'The highlighted words labels 04/05/2026 as the date of service, and it can be read as month/day or day/month; the record does not settle which.'; several_dates 'The highlighted words labels more than one date of service (04/06/2026, 04/20/2026) and nothing says which one belongs to this charge.'; no_year 'labels April 5 as the date of service, but it states no year, which the code does not borrow from the statement.'; invalid 'labels 02/30/2026 ... but it is not a complete date on the calendar.'; implausible 'labels 09/14/2026 ... but that date is after the statement it appears on or years before it.' (statement June 15, 2026). Screenshots T-209-r3-step3-ambiguous_numeric.png, -several_dates.png, -no_year.png, -invalid.png, -implausible.png. Only two_digit_year ('04/05/26') can be filled from the highlighted words. My round-1 fix wording proposed this single instruction; it was wrong for five of the six reasons.",
37	   "why_it_matters": "This is the step where a wrong date goes into the demand. If she follows the sentence on an implausible line, the letter gets a date of service after the bill that charges it. On an invalid line it gets February 30. On an ambiguous line she has to pick April 5 or May 4 with no rule. On a no-year line she has to supply a year the card says not to take from the statement. These are the dates an adjuster checks against the records. The sentence also contradicts the note: the note says the record does not settle the date, and the sentence says to take it from the highlighted words.",
38	   "fix": "Split the written reasons in step3.js. two_digit_year: 'Fill the blank with the highlighted date with its full year.' ambiguous_numeric: 'Read it both ways (April 5 or May 4). Use the reading that matches a visit from this provider in Step 2, or ask the provider. Fill the blank with that date.' several_dates: 'Match this charge to one of the dates using the visit notes in Step 2, or ask the provider for a line-by-line bill.' no_year: 'Find the year in this provider's visit note in Step 2 or ask the provider. Do not take it from the statement date.' invalid and implausible: 'Do not copy the highlighted date. Find the date in this provider's visit note in Step 2, or ask the provider for a corrected bill.' Keep the button names and the count/total clause. The backend _ASK_WRITTEN ('Confirm the date from the quote and fill the blank', service_date.py:102) has the same problem for these five reasons. Route that to the service_date owner (T-202) so the note and the sentence say the same thing.",
39	   "acceptance_test": "E2E parametrized over all six written reasons with SD.confirm_note(reason, raw): for ambiguous_numeric, several_dates, no_year, invalid and implausible, confirm-next does not contain 'Fill the blank with the date you checked in the highlighted words' and names a source outside the quote (visit note / Step 2 or the provider). For invalid and implausible it contains 'Do not copy the highlighted date'. For two_digit_year it may point to the highlighted date. No reason's sentence tells her to take a date from the highlighted words when its note says the record does not settle it."},
40	  {"severity": "minor",
41	   "title": "'If you don't, it stays out of the letter.' follows 'Fill the blank with that date.' and reads as 'if you don't fill the blank', which is false",
42	   "evidence": "step3.js:43 appends ' If you don't, it stays out of the letter.' after the fill instruction and the statement-date sentence. Rendered NEXT (T-209-r3-paralegal-walk.json, 1280x900:no_date): '... Fill the blank with that date. The date in parentheses is the statement date, not the service date. If you don't, it stays out of the letter.' The note above says 'The letter prints no service date for this line. It leaves a blank for the date of service.' So a counted line with an unfilled blank prints, with its amount in the total.",
43	   "why_it_matters": "This is a label-only issue, not a spec violation. The nearest verb is 'Fill', so a quick reader can believe that an unfilled line drops out of the letter. She may count a line she has no date for, expecting it to disappear. It then prints with a blank date, and its amount stays in the billed total.",
44	   "fix": "Say 'If you don't count it, it stays out of the letter and the total.' and put it right after the Yes/No clause, before the fill instruction.",
45	   "acceptance_test": "E2E: confirm-next contains \"If you don't count it\" and does not contain \"If you don't, it\"."},
46	  {"severity": "minor",
47	   "title": "The taller foot (r2 clip fix) now hides the card's date line, which the sentence calls 'the date in parentheses', and at 1366x768 it hides part of the amount",
48	   "evidence": "step3.css:22 lets the confirm foot grow to max-height 300px. T-209-r3-paralegal-body-clip.json: 1280x900 ambiguous_numeric body clientHeight 56, scrollHeight 167, service_date_fully_visible false, service_date_hit_test false; 1366x768 no_date body clientHeight 56, service_date_hit_test false, figure_fully_visible false; 1366x768 ambiguous_numeric body clientHeight 40, figure_hit_test false. Control with no confirm foot at 1366x768: service_date_fully_visible true. 1920x1080: all visible. Screenshots T-209-r3-body-no_date-1366x768.png and T-209-r3-step3-ambiguous_numeric.png: the '$4,920.00' figure is cut through, and the line 'date of service [__________] (statement dated June 15, 2026)' is scrolled under the foot. test_t206.py:103 checks only the foot, and test_t206.py:106 uses is_visible(), which passes for an element that is covered.",
49	   "why_it_matters": "The sentence tells her that 'The date in parentheses is the statement date', but no parentheses are on screen. At 1366x768, a common laptop size, the amount she is asked to count is partly covered. She has to scroll a 40-56 px box to see what she is confirming. This slows verification. Facts are not lost, and the highlighted quote stays visible.",
50	   "fix": "Keep the amount and the date line outside the scrolling body. Pin them above it or put them in the foot above the note. Or quote the line inside the sentence ('the letter shows date of service [__________] (statement dated June 15, 2026)') so the sentence does not depend on hidden text.",
51	   "acceptance_test": "E2E at 1280x900 and 1366x768 for one doubtful and one no-date reason: the service-date element and the figure pass elementFromPoint at their centers, and their rects lie inside the visible body area above the foot."},
52	  {"severity": "minor",
53	   "title": "No-date and non-service-date sentence says 'find the date of service in the record', and on this card 'the record' is the bill that has no date",
54	   "evidence": "step3.js:42: 'find the date of service in the record or ask the provider'. The card's source panel reads 'From the record  Record 4 · Saltmarrow General Hospital, UB-04 itemized bill' (T-209-r3-body-no_date-1366x768.png). The note above: 'The line states no date of service.'",
55	   "why_it_matters": "'Ask the provider' gives her a clear path. 'In the record' can send her back to the same bill. The useful place is this provider's visit note for the encounter, which the case already has in Step 2.",
56	   "fix": "'find the date of service in this provider's visit note (Step 2) or ask the provider for a dated itemized bill'.",
57	   "acceptance_test": "E2E for no_date and non_service_date: confirm-next names the visit note or Step 2, and still contains no 'highlighted'."},
58	  {"severity": "minor",
59	   "title": "Carried from round 2 (minor 7): no curated case reaches this sentence; every check of its wording uses injected backend output",
60	   "evidence": "Round-2 reach scan (T-209-paralegal-reach-scan.json: 16 cases, charges_with_confirm_note 0). 8521562 changes only step3.js, step3.css and test_t206.py (git show --stat 8521562), so the fixtures are unchanged. Handoff: 'Not fixed: minor 7 (no curated doubtful-date case: backend/qa fixture)'. test_t206.py:55, :84 and :112 inject sd through SD.confirm_note.",
61	   "why_it_matters": "The demo never shows this sentence on a real record. The first real doubtful date will be the first time anyone sees the wording on a real bill.",
62	   "fix": "Open a qa card for one curated bill line per branch: a labeled ambiguous DOS and an unlabeled ledger date.",
63	   "acceptance_test": "Reach scan: at least one curated charge has data-reason 'doubtful' and one has 'no_date', both from the real backend."},
64	  {"severity": "nit",
65	   "title": "The note reads 'The highlighted words labels ...' (grammar; pre-existing, review.js:26)",
66	   "evidence": "Every written-reason NOTE in T-209-r3-paralegal-walk.json starts 'The highlighted words labels'. review.js:26 rewrites 'The quote <verb>' only for does not|is not|is|has|says|contains|states|shows|carries|gives. 'labels' is not in the list, so the verb keeps its singular form.",
67	   "why_it_matters": "It is a small grammar slip in the sentence that explains why the date is doubtful.",
68	   "fix": "Add labels -> label to the verb map in review.js:26.",
69	   "acceptance_test": "Unit or E2E: a written-reason confirm note contains 'The highlighted words label ' and not 'labels'."}
70	 ],
71	 "whats_right": [
72	  "No-date and non-service-date lines never point at the highlighted words now, and the note and the sentence give the same instruction (test_t206.py parametrized test, my walk agrees).",
73	  "The foot no longer clips: 20 of 20 reason/viewport runs show scrollHeight equal to clientHeight, with the Yes/No buttons on screen.",
74	  "The doubled 'Date of service' label is gone, and the sentence now says that counting adds the amount to the total and that the parenthetical date is the statement date."
75	 ],
76	 "questions_for_chris": [
77	  "Should the doubtful-date note (backend _ASK_WRITTEN, 'Confirm the date from the quote') and this sentence be fixed together on T-202, or should T-209 branch the sentence now and leave the note to T-202? Both currently tell her to take the date from the quote on an ambiguous or implausible line."
78	 ]}
79	```
80	
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:04:44.384Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git rev-parse --short HEAD; git log --oneline -5; git show --stat 1b3c58a | head -30; python3 tools/board.py show T-209 | tail -60",
 "description": "Show commit, board card"
}
````

### User / tool · 2026-11-03T02:04:44.564Z

**tool result**
````
0281189
0281189 chore(guard): subagents stage only into a temp index (shared index kept holding stale reverts, T-201/T-204)
1b3c58a fix(frontend): Step 3 one next-step sentence for every not-certain date reason; confirm box keeps the amount and date line visible at 1280x900 and 1366x768 (T-209 r3)
efda639 docs(architect): LLM_VS_CODE rows 2-3 match T-202 r4 code (T-207)
8cb5bd2 fix(backend): T-202 r4 D-071 amendment 2: only an identified encounter record lends its date; four prose labels; dotted leaders; declared record-type table; anchored blank
8521562 fix(frontend): Step 3 next step depends on the date reason: doubtful date checks the quote, no date looks outside it; statement-date, total and clip minors (T-209 r2)
commit 1b3c58af9c4a6f45efb01037cb616e8ec9cc059d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 20:03:23 2026 -0600

    fix(frontend): Step 3 one next-step sentence for every not-certain date reason; confirm box keeps the amount and date line visible at 1280x900 and 1366x768 (T-209 r3)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/frontend/guided/review.js |  2 +-
 app/frontend/guided/step3.css | 15 +++++++--
 app/frontend/guided/step3.js  | 10 ++----
 tests/e2e/guided/test_t206.py | 76 +++++++++++++++++++++++++------------------
 4 files changed, 61 insertions(+), 42 deletions(-)
---
id: "T-209"
title: "Step 3 confirm note matches the letter's fillable date blank (not 'type the date into your letter yourself')"
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T01:25:49Z"
updated_at: "2026-11-03T02:04:37Z"
claimed_by: "frontend"
claimed_at: "2026-11-03T01:55:57Z"
rounds: 2
commits: ["88c73dd", "8521562", "1b3c58a"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-209-paralegal-r2.md", "at": "2026-11-03T01:37:39Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "changes", "file": "reviews/T-209-paralegal-r3.md", "at": "2026-11-03T01:55:50Z"}
ac:
  - {"n": 1, "text": "confirmNext in guided step3.js says the letter shows a blank 'date of service [____]' to fill from the highlighted words; e2e updated", "done": true, "evidence": "guided e2e from git archive of tree 13bdb1e: 143 passed (E2E_REQUIRE_DB=1); test_t206 asserts the blank wording"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T01:26:04Z frontend: claimed
- 2026-11-03T01:30:07Z frontend: AC 1 checked: guided e2e from git archive of tree 13bdb1e: 143 passed (E2E_REQUIRE_DB=1); test_t206 asserts the blank wording
- 2026-11-03T01:30:07Z frontend: moved in_progress -> in_review
- 2026-11-03T01:30:10Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-03T01:37:39Z orchestrator: review paralegal-reviewer (claude-haiku-5-5): changes — reviews/T-209-paralegal-r2.md; round 1; findings:
    - [major] For a line with no service date, the sentence tells her to fill the blank from the highlighted words, which contain no service date, and contradicts the note above it — fix: Branch the sentence on sd.reason in step3.js. For written-date reasons (ambiguous_numeric, two_digit_year, no_year, invalid, several_dates, implausible): 'If you count it, the letter shows a blank date of service
    - [major] A labeled date of service followed by a dotted leader is read as no date, so the note says the line states no date of service (pre-existing at HEAD, outside the 88c73dd diff) — fix: In service_date.resolve, allow a dotted leader (runs of '.' or '…' with spaces) between the label and the amount when building the clause, or stop splitting segments at '...'. Route to the T-202 owner (se
    - [minor] The note does not describe the letter text: the letter prints '(statement dated June 15, 2026)' after the blank, and nothing says that statement date is not the service date — fix: Name the full printed text in confirmNext, and say that the date in parentheses is the statement's date and is not the service date. Example: 'The letter shows date of service [__________] (statement dated
    - [minor] Counting consequences are not stated: a doubtful-date line loses the 'added to the bill total' line, and the note never says what counting or not counting does to the letter total — fix: Add to confirmNext: 'If you count it, its amount is added to the billed total with the blank date. If you do not count it, it is left out of the letter.'
    - [minor] The sentence's last clause is cut off in its scroll box at a 1280x900 desktop — fix: Let the foot grow to fit the note and the sentence at 1280x900 (no inner scroll for the confirm block), or move the sentence above the note's second paragraph so the clipped part is the least important text.
    - [minor] The card's date line reads 'Date of service date of service [__________]' (pre-existing, same card as the note) — fix: Show the label once. Either drop the 'Date of service' span when sd.text starts with 'date of service', or strip the prefix from sd.text for the card.
    - [minor] No curated case reaches this sentence; its acceptance evidence relies on injected backend output — fix: Add one curated bill line with a doubtful written date (for example 'DOS 04/05/2026' with no year ambiguity resolved) so the sentence is shown by the real backend once. Keep the injected test as the wording check.
- 2026-11-03T01:37:39Z orchestrator: assigned: frontend
- 2026-11-03T01:37:48Z frontend: claimed
- 2026-11-03T01:49:22Z frontend: moved in_progress -> in_review
- 2026-11-03T01:49:28Z orchestrator: review dispatched: paralegal-reviewer
- 2026-11-03T01:55:50Z orchestrator: review paralegal-reviewer (claude-opus-5-5): changes — reviews/T-209-paralegal-r3.md; round 2; findings:
    - [major] Doubtful written date: the sentence tells her to fill the blank from the highlighted words, but the note above says those words cannot settle the date (ambiguous, several dates) or that the written date is incomplete or wrong (no year, invalid, implausible) — fix: Split the written reasons in step3.js. two_digit_year: 'Fill the blank with the highlighted date with its full year.' amb
    - [minor] 'If you don't, it stays out of the letter.' follows 'Fill the blank with that date.' and reads as 'if you don't fill the blank', which is false — fix: Say 'If you don't count it, it stays out of the letter and the total.' and put it right after the Yes/No clause, before the fill instruction.
    - [minor] The taller foot (r2 clip fix) now hides the card's date line, which the sentence calls 'the date in parentheses', and at 1366x768 it hides part of the amount — fix: Keep the amount and the date line outside the scrolling body. Pin them above it or put them in the foot above the note. Or quote the line inside the sentence ('the letter shows date of service [__________] (statement date
    - [minor] No-date and non-service-date sentence says 'find the date of service in the record', and on this card 'the record' is the bill that has no date — fix: 'find the date of service in this provider's visit note (Step 2) or ask the provider for a dated itemized bill'.
    - [minor] Carried from round 2 (minor 7): no curated case reaches this sentence; every check of its wording uses injected backend output — fix: Open a qa card for one curated bill line per branch: a labeled ambiguous DOS and an unlabeled ledger date.
- 2026-11-03T01:55:50Z orchestrator: assigned: frontend
- 2026-11-03T01:55:57Z frontend: claimed
- 2026-11-03T02:03:55Z frontend: moved in_progress -> in_review
- 2026-11-03T02:04:37Z orchestrator: review dispatched: paralegal-reviewer

## Handoff
r3: one next-step sentence for every not-certain reason (find the date in the record, highlighted words may help, or ask the provider; write it in the blank 'date of service [__________]'); note above untouched; statement-date clause kept; consequence cut to 'Counting it adds the amount to the bill total.' (the Yes/No sentence made the foot too tall). Layout: card body min-height keeps amount + date line, foot shrinks last, smaller type at <=820px high; e2e at 1280x900 and 1366x768 checks rect-inside-body and elementFromPoint for figure and date line. review.js: 'labels' -> 'label' (nit). Verified: git archive tree, E2E_REQUIRE_DB=1, tests/e2e/guided + no_console_errors 160 passed. Left: minor 7 (no curated doubtful-date case, qa/backend fixture); backend _ASK_WRITTEN still says 'Confirm the date from the quote' (T-202, kept per brief). Surprised: the 300-char backend note alone fills the foot at 1366x768.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:04:46.989Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git diff --stat 1b3c58a 0281189 -- app tests; echo ---; git diff --stat 8521562 1b3c58a -- app/backend app/llm; echo ---; git show 1b3c58a -- app/frontend",
 "description": "Show fix diff and backend drift"
}
````

### User / tool · 2026-11-03T02:04:47.122Z

**tool result**
````
---
 app/backend/encounter_types.json |  21 +++++++
 app/backend/service_date.py      | 115 +++++++++++++++++++++++++++++----------
 app/backend/store.py             |   6 +-
 3 files changed, 110 insertions(+), 32 deletions(-)
---
commit 1b3c58af9c4a6f45efb01037cb616e8ec9cc059d
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 20:03:23 2026 -0600

    fix(frontend): Step 3 one next-step sentence for every not-certain date reason; confirm box keeps the amount and date line visible at 1280x900 and 1366x768 (T-209 r3)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/guided/review.js b/app/frontend/guided/review.js
index a1bff76..906305e 100644
--- a/app/frontend/guided/review.js
+++ b/app/frontend/guided/review.js
@@ -23,7 +23,7 @@
       .replace(/\b([Tt])he (?:AI )?second (?:AI )?check\b/g, (m, t) => (t === "T" ? "A second AI check" : "a second AI check"))
       .replace(/\bsecond check\b/g, "second AI check")
       .replace(/\bthe quoted text\b/g, "the highlighted words").replace(/\bquoted text\b/g, "highlighted words")
-      .replace(/\b([Tt])he quote (does not|is not|is|has|says|contains|states|shows|carries|gives)\b/g, (m, t, v) => `${t}he highlighted words ${v === "is" ? "are" : v === "has" ? "have" : v === "carries" ? "carry" : v === "gives" ? "give" : v === "does not" ? "do not" : v === "is not" ? "are not" : v === "says" ? "say" : v === "contains" ? "contain" : v === "states" ? "state" : "show"}`)
+      .replace(/\b([Tt])he quote (does not|is not|is|has|says|contains|states|shows|carries|gives|labels)\b/g, (m, t, v) => `${t}he highlighted words ${v === "is" ? "are" : v === "has" ? "have" : v === "carries" ? "carry" : v === "gives" ? "give" : v === "labels" ? "label" : v === "does not" ? "do not" : v === "is not" ? "are not" : v === "says" ? "say" : v === "contains" ? "contain" : v === "states" ? "state" : "show"}`)
       .replace(/\bsummary or quote\b/g, "line or highlighted words").replace(/\bthe quotes?\b/g, "the highlighted words").replace(/\bQuote\b/g, "The highlighted words").replace(/\bquotes?\b/g, "highlighted words")
       .replace(/\bthe summary\b/g, "the line").replace(/\bThe summary\b/g, "The line").replace(/\bsummary\b/g, "line")
       .replace(/\ban itemized service line\b/g, "a single dated bill line").replace(/\bitemized service line\b/g, "single dated bill line").replace(/\ban itemized\b/g, "a line-by-line").replace(/\bitemized\b/g, "line-by-line")
diff --git a/app/frontend/guided/step3.css b/app/frontend/guided/step3.css
index cf07e9a..7052327 100644
--- a/app/frontend/guided/step3.css
+++ b/app/frontend/guided/step3.css
@@ -18,5 +18,16 @@
 .card-b .svc-date { overflow-wrap: anywhere; }
 .card-f .svc-note { display: block; overflow-wrap: anywhere; }
 .card-f .svc-next { margin: 6px 0 0; overflow-wrap: anywhere; }
-/* T-209 r2: the confirm note + next step must be read whole, not in a scroll box: that foot is as tall as its text (the quote above scrolls instead) */
-@media (min-width: 761px) { .card-f:has(.svc-next) { height: auto; min-height: 150px; max-height: 300px; } }
+/* T-209 r3: the foot with the confirm note + next step is as tall as its text, but the card is a fixed height: the body keeps room for the amount and the date line (they are what she is confirming) and the foot gives way last */
+@media (min-width: 761px) {
+  .card:has(.svc-next) .card-b { flex: 1 1 0; min-height: 120px; }
+  .card-f:has(.svc-next) { height: auto; min-height: 0; max-height: none; flex: 0 1 auto; }
+  .card:has(.svc-next) .card-f { line-height: 1.3rem; font-size: .9375rem; }
+}
+@media (min-width: 761px) and (max-height: 820px) {
+  .card:has(.svc-next) .card-b { min-height: 90px; padding-top: 6px; padding-bottom: 4px; }
+  .card:has(.svc-next) .card-b .money { font-size: 2rem; line-height: 2.25rem; }
+  .card:has(.svc-next) .card-b .gap-top { margin-top: 6px; }
+  .card:has(.svc-next) .card-f { line-height: 1.25rem; font-size: .875rem; padding-top: 8px; padding-bottom: 8px; }
+  .card-f .svc-next { margin-top: 4px; }
+}
diff --git a/app/frontend/guided/step3.js b/app/frontend/guided/step3.js
index 8060785..ecea33d 100644
--- a/app/frontend/guided/step3.js
+++ b/app/frontend/guided/step3.js
@@ -32,15 +32,11 @@
     /^date of service/i.test(sd.text || "") ? null : h("span", { class: "label-cap" }, "Date of service "), h("b", { "data-testid": "service-date-text" }, sd.text || ""),
     sd.state === "stated" && stmtOnly(sd) ? h("span", { class: "muted", "data-testid": "statement-date" }, ` · statement dated ${R.longDate(sd.statement_date_iso)}`) : null);
   const confirmNote = (sd) => h("strong", { class: "svc-note", role: "note", "data-testid": "confirm-note" }, R.plain(sd.confirm_note));
-  /* T-206/T-209 r2: the note says what to do next, with the buttons this card really has (it has no control to type a date: the letter shows the fillable blank "date of service [__________]" and she fills it herself). The next step depends on the reason: a doubtful date IS in the quote (check it there, then fill); no date in the quote (no_date, non_service_date, or anything unknown) is never fixed from the highlight: find it in the record or ask the provider. */
-  const DOUBTFUL = ["ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "implausible"];
+  /* T-206/T-209 r3: the note above states the specific reason; this sentence is the same for every reason that is not certain, so it can never contradict the note: find the date outside this card's guess, write it in the letter's blank. The card has no control to type a date. */
   const confirmNext = (sd) => {
-    const doubtful = DOUBTFUL.includes(sd && sd.reason), yn = [h("b", {}, "Yes, count it"), " or ", h("b", {}, "No, don't count it"), ". "];
     const stmt = /\(statement dated/.test((sd && sd.text) || "") ? " The date in parentheses is the statement date, not the service date." : "";
-    return h("p", { class: "svc-next", "data-testid": "confirm-next", "data-reason": doubtful ? "doubtful" : "no_date" }, h("b", {}, "What to do: "),
-      ...(doubtful ? ["check the date in the highlighted words, then press ", ...yn, "If you count it, its amount is added to the bill total and the letter shows ", h("b", {}, "date of service [__________]"), ". Fill the blank with the date you checked in the highlighted words." + stmt]
-        : ["find the date of service in the record or ask the provider, then press ", ...yn, "If you count it, its amount is added to the bill total and the letter shows ", h("b", {}, "date of service [__________]"), ". Fill the blank with that date." + stmt]),
-      " If you don't, it stays out of the letter.");
+    return h("p", { class: "svc-next", "data-testid": "confirm-next" }, h("b", {}, "What to do: "), "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank ", h("b", {}, "\u201Cdate of service [__________]\u201D"), " in your letter." + stmt,
+      " Counting it adds the amount to the bill total.");
   };
 
   function present(S, item) {
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:04:59.187Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls artifacts/review-evidence/ | grep -i T-209; git show 1b3c58a:app/backend/service_date.py | grep -n \"_WHY\\|_ASK\\|def confirm_note\" ; ",
 "description": "List prior T-209 evidence; locate note text"
}
````

### User / tool · 2026-11-03T02:04:59.300Z

**tool result**
````
T-209-paralegal-foot-clip.json
T-209-paralegal-foot-clip.py
T-209-paralegal-note-probe.json
T-209-paralegal-note-probe.py
T-209-paralegal-probe.json
T-209-paralegal-probe.py
T-209-paralegal-reach-scan.json
T-209-paralegal-reach-scan.py
T-209-paralegal-step3-walk.py
T-209-r3-body-ambiguous_numeric-1366x768.png
T-209-r3-body-control_no_injection-1280x900.png
T-209-r3-body-control_no_injection-1366x768.png
T-209-r3-body-no_date-1366x768.png
T-209-r3-paralegal-body-clip.json
T-209-r3-paralegal-body-clip.py
T-209-r3-paralegal-draft.md
T-209-r3-paralegal-pytest.txt
T-209-r3-paralegal-server.log
T-209-r3-paralegal-walk.json
T-209-r3-paralegal-walk.py
T-209-r3-step3-ambiguous_numeric.png
T-209-r3-step3-implausible.png
T-209-r3-step3-invalid.png
T-209-r3-step3-no_date.png
T-209-r3-step3-no_date_dob_sentence.png
T-209-r3-step3-no_year.png
T-209-r3-step3-non_service_date-1366x768.png
T-209-r3-step3-non_service_date.png
T-209-r3-step3-non_service_date_dob.png
T-209-r3-step3-several_dates-1366x768.png
T-209-r3-step3-several_dates.png
T-209-r3-step3-two_digit_year.png
T-209-step3-A_no_date_of_service.png
T-209-step3-B_labeled_ambiguous_dos.png
T-209-step3-foot-desktop_1280x900.png
T-209-step3-foot-phone_390x844.png
T-209-step3-walk.json
146:_WHY = {
156:_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
157:_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it."
160:def confirm_note(reason, raw) -> str:
162:    return _WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") + (_ASK_WRITTEN if reason in WRITTEN else _ASK_NONE)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:00.796Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 1b3c58a:app/backend/service_date.py | sed -n 140,165p; echo ----; cat artifacts/review-evidence/T-209-r3-paralegal-walk.py",
 "description": "Read note text and r3 walk script"
}
````

### User / tool · 2026-11-03T02:05:00.899Z

**tool result**
````
def printed_text(res: dict, statement_iso) -> str:
    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
    return not_stated_text(statement_iso)


_WHY = {
    "ambiguous_numeric": "The quote labels {raw} as the date of service, and it can be read as month/day or day/month; the record does not settle which.",
    "two_digit_year": "The quote labels {raw} as the date of service, but it has a two-digit year, which the code does not guess.",
    "no_year": "The quote labels {raw} as the date of service, but it states no year, which the code does not borrow from the statement.",
    "invalid": "The quote labels {raw} as the date of service, but it is not a complete date on the calendar.",
    "several_dates": "The quote labels more than one date of service ({raw}) and nothing says which one belongs to this charge.",
    "implausible": "The quote labels {raw} as the date of service, but that date is after the statement it appears on or years before it.",
    "non_service_date": "The only date near this line ({raw}) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service).",
    "no_date": "The line states no date of service.",
}
_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it."


def confirm_note(reason, raw) -> str:
    """The Step 3 note and the internal-notes line for a charge whose service date is not certain: why, and what the letter does (D-071 amendment)."""
    return _WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") + (_ASK_WRITTEN if reason in WRITTEN else _ASK_NONE)


def _iso(y, mo, d):
----
"""T-209 r3 paralegal review: drive the Step 3 card at commit 8521562 (git archive, demo mode, fixture backend, 127.0.0.1:7931) in Chromium.
For each of the eight service_date reasons, compute the backend's own service_date dict for one constructed bill line with the archive's resolver
(store.charge_service_date), inject it into lib10 a2 (the curated set has no doubtful-date bill), and record the date line, the confirm note, the
next-step sentence, whether the foot scrolls, and a screenshot. Viewports: 1280x900 and 1366x768. Nothing is saved: Yes/No are never pressed.

Usage: .venv/bin/python -I artifacts/review-evidence/T-209-r3-paralegal-walk.py <archive_root>"""
import json
import re
import sys
import time
import urllib.request

TREE = sys.argv[1]
sys.path.insert(0, TREE)
from app.backend import amounts as AM, store  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

BASE = "http://127.0.0.1:7931"
EV = "/Users/arsis/zlayt-pm-project/artifacts/review-evidence"
SRC, STMT = "Fennimoor Spine Clinic, itemized ledger", "2026-06-15"


def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read() or b"null")


def backend_sd(excerpt):
    pos = excerpt.index("$250.00")
    return store.charge_service_date({"excerpt": excerpt, "ladder": {}}, {"date_iso": STMT, "source": SRC}, pos)


LINES = {
    "ambiguous_numeric": "Fennimoor Spine Clinic itemized ledger. DOS 04/05/2026: Office visit 99213 - $250.00",
    "two_digit_year": "Fennimoor Spine Clinic itemized ledger. DOS 04/05/26: Office visit 99213 - $250.00",
    "no_year": "Fennimoor Spine Clinic itemized ledger. DOS April 5: Office visit 99213 - $250.00",
    "invalid": "Fennimoor Spine Clinic itemized ledger. DOS 02/30/2026: Office visit 99213 - $250.00",
    "several_dates": "Fennimoor Spine Clinic itemized ledger. Dates of service 04/06/2026 and 04/20/2026: Office visit 99213 - $250.00",
    "implausible": "Fennimoor Spine Clinic itemized ledger. DOS 09/14/2026: Office visit 99213 - $250.00",
    "non_service_date": "Fennimoor Spine Clinic itemized ledger. Office visit 03/04/2026 99213 - $250.00",
    "non_service_date_dob": "Fennimoor Spine Clinic itemized ledger. Office visit, 99213, DOB 03/04/1980, $250.00",
    "no_date_dob_sentence": "Fennimoor Spine Clinic itemized ledger. Patient DOB 03/04/1980. Office visit, established patient, 99213 - $250.00",
    "no_date": "Fennimoor Spine Clinic itemized ledger. Office visit, established patient, 99213 - $250.00",
}

st = api("POST", "/api/cases", {"library": "case_lib10_eob_ub04_cms1500"}); tok = st["token"]
api("POST", f"/api/cases/{tok}/run", {})
for _ in range(300):
    if api("GET", f"/api/cases/{tok}/status")["status"] in ("ready", "failed"):
        break
    time.sleep(0.5)

out = {"commit": "8521562", "server": BASE, "case_token": tok, "statement_date": STMT, "runs": {}}
with sync_playwright() as p:
    browser = p.chromium.launch()
    for vw, vh in ((1280, 900), (1366, 768)):
        for want, line in LINES.items():
            sd = backend_sd(line)
            page = browser.new_page(viewport={"width": vw, "height": vh})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)

            def make_rewrite(sd_value):
                def rewrite(route, request=None):
                    r = route.fetch(); body = r.json()
                    for x in body.get("amounts", []):
                        if x["id"] == "a2":
                            x["service_date"] = sd_value
                    route.fulfill(response=r, json=body)
                return rewrite
            page.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), make_rewrite(sd))
            page.goto(f"{BASE}/case/{tok}/bills?item=a2")
            page.get_by_test_id("card-line").wait_for(timeout=20000)
            time.sleep(0.6)

            def txt(tid):
                loc = page.get_by_test_id(tid)
                return loc.inner_text() if loc.count() else None
            foot = page.evaluate("""(() => { const f = document.querySelector('[data-testid=card-foot]'); if (!f) return null;
                const n = document.querySelector('[data-testid=confirm-next]'); const r = n ? n.getBoundingClientRect() : null; const fr = f.getBoundingClientRect();
                return {clientHeight: f.clientHeight, scrollHeight: f.scrollHeight, overflowY: getComputedStyle(f).overflowY,
                        next_bottom: r && r.bottom, foot_bottom: fr.bottom, viewport_h: innerHeight}; })()""")
            yb = page.get_by_test_id("answer-yes").bounding_box() if page.get_by_test_id("answer-yes").count() else None
            nx = page.get_by_test_id("confirm-next")
            rec = {"backend_reason": sd.get("reason"), "backend_raw_line": line, "backend_text": sd.get("text"),
                   "service_date_line": txt("service-date"), "confirm_note": txt("confirm-note"), "confirm_next": txt("confirm-next"),
                   "data_reason": nx.get_attribute("data-reason") if nx.count() else None,
                   "yes_label": txt("answer-yes"), "no_label": txt("answer-no"), "foot": foot,
                   "answer_yes_bottom": yb and yb["y"] + yb["height"], "console_errors": errors}
            key = f"{vw}x{vh}:{want}"
            out["runs"][key] = rec
            if vw == 1280:
                page.screenshot(path=f"{EV}/T-209-r3-step3-{want}.png", full_page=False)
            elif want in ("non_service_date", "several_dates"):
                page.screenshot(path=f"{EV}/T-209-r3-step3-{want}-1366x768.png", full_page=False)
            page.close()
    browser.close()
api("DELETE", f"/api/cases/{tok}")
with open(f"{EV}/T-209-r3-paralegal-walk.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("wrote", f"{EV}/T-209-r3-paralegal-walk.json")
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:03.760Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat artifacts/review-evidence/T-209-r3-paralegal-body-clip.py; ls artifacts/review-evidence/*serve*.py | head; tail -5 artifacts/review-evidence/T-209-r3-paralegal-server.log",
 "description": "Read r3 body-clip script and serve helpers"
}
````

### User / tool · 2026-11-03T02:05:03.869Z

**tool result**
````
"""T-209 r3: with the taller confirm foot (step3.css, 8521562), is the card body (the amount, the date line with '(statement dated ...)', 'Written in the
record as ...') still on screen? Same injection as T-209-r3-paralegal-walk.py (lib10 a2, backend sd for reason ambiguous_numeric and no_date), plus
a control run with no injection (a2's own stated date, no confirm foot). Measures the body's scroll box and whether the service-date line is inside it.

Usage: .venv/bin/python -I artifacts/review-evidence/T-209-r3-paralegal-body-clip.py <archive_root>"""
import json
import re
import sys
import time
import urllib.request

TREE = sys.argv[1]
sys.path.insert(0, TREE)
from app.backend import store  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

BASE = "http://127.0.0.1:7931"
EV = "/Users/arsis/zlayt-pm-project/artifacts/review-evidence"


def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read() or b"null")


def sd_for(line):
    return store.charge_service_date({"excerpt": line, "ladder": {}}, {"date_iso": "2026-06-15", "source": "Fennimoor Spine Clinic, itemized ledger"},
                                     line.index("$250.00"))


SCEN = {"control_no_injection": None,
        "ambiguous_numeric": sd_for("Fennimoor Spine Clinic itemized ledger. DOS 04/05/2026: Office visit 99213 - $250.00"),
        "no_date": sd_for("Fennimoor Spine Clinic itemized ledger. Office visit, established patient, 99213 - $250.00")}

st = api("POST", "/api/cases", {"library": "case_lib10_eob_ub04_cms1500"}); tok = st["token"]
api("POST", f"/api/cases/{tok}/run", {})
for _ in range(300):
    if api("GET", f"/api/cases/{tok}/status")["status"] in ("ready", "failed"):
        break
    time.sleep(0.5)

JS = """(() => {
  const q = (t) => document.querySelector(`[data-testid=${t}]`);
  const sd = q('service-date'), fig = q('figure'), foot = q('card-foot');
  let body = sd || fig; while (body && body.parentElement && !['auto','scroll'].includes(getComputedStyle(body).overflowY)) body = body.parentElement;
  const R = (e) => e ? (({top, bottom}) => ({top: Math.round(top), bottom: Math.round(bottom)}))(e.getBoundingClientRect()) : null;
  const br = body ? body.getBoundingClientRect() : null, fr = foot ? foot.getBoundingClientRect() : null;
  const inside = (e) => { if (!e || !br) return null; const r = e.getBoundingClientRect(); const visTop = br.top, visBot = Math.min(br.bottom, fr ? fr.top : br.bottom);
                          return r.top >= visTop - 1 && r.bottom <= visBot + 1; };
  const hit = (e) => { if (!e) return null; const r = e.getBoundingClientRect(); const x = r.left + 10, y = r.top + r.height / 2; const h = document.elementFromPoint(x, y); return !!h && (e === h || e.contains(h)); };
  return {body_cls: body && body.className, body_client: body && body.clientHeight, body_scroll: body && body.scrollHeight, body_rect: R(body), foot_rect: R(foot),
          figure: R(fig), figure_fully_visible: inside(fig), figure_hit_test: hit(fig),
          service_date: R(sd), service_date_fully_visible: inside(sd), service_date_hit_test: hit(sd), service_date_text: sd && sd.innerText};
})()"""

out = {"commit": "8521562", "server": BASE, "runs": {}}
with sync_playwright() as p:
    browser = p.chromium.launch()
    for vw, vh in ((1280, 900), (1366, 768), (1920, 1080)):
        for name, sd in SCEN.items():
            page = browser.new_page(viewport={"width": vw, "height": vh})
            if sd is not None:
                def make_rewrite(sd_value):
                    def rewrite(route, request=None):
                        r = route.fetch(); b = r.json()
                        for x in b.get("amounts", []):
                            if x["id"] == "a2":
                                x["service_date"] = sd_value
                        route.fulfill(response=r, json=b)
                    return rewrite
                page.route(re.compile(rf"/api/cases/{tok}(\?.*)?$"), make_rewrite(sd))
            page.goto(f"{BASE}/case/{tok}/bills?item=a2")
            page.get_by_test_id("card-line").wait_for(timeout=20000)
            time.sleep(0.6)
            out["runs"][f"{vw}x{vh}:{name}"] = page.evaluate(JS)
            if vw == 1366 or (vw == 1280 and name == "control_no_injection"):
                page.screenshot(path=f"{EV}/T-209-r3-body-{name}-{vw}x{vh}.png")
            page.close()
    browser.close()
api("DELETE", f"/api/cases/{tok}")
with open(f"{EV}/T-209-r3-paralegal-body-clip.json", "w") as f:
    json.dump(out, f, indent=2)
for k, v in out["runs"].items():
    print(k, json.dumps(v))
artifacts/review-evidence/T-060-paralegal-pass4-serve.py
Serving on http://127.0.0.1:7931  (Ctrl-C to stop)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:14.377Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; lsof -iTCP:7947 -sTCP:LISTEN -nP; echo \"exit $?\"; mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t209r4 && git archive 1b3c58a | tar -x -C /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t209r4 && ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t209r4; cat artifacts/review-evidence/T-060-paralegal-pass4-serve.py | head -20",
 "description": "Check port, extract archive of 1b3c58a"
}
````

### User / tool · 2026-11-03T02:05:16.049Z

**tool result**
````
exit 1
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:21.379Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t209r4.db PORT=7947 HOST=127.0.0.1 .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t209r4 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-server.log 2>&1",
 "description": "Start archived app on port 7947 in demo mode",
 "run_in_background": true
}
````

### User / tool · 2026-11-03T02:05:21.458Z

**tool result**
````
Command running in background with ID: bje0ih930. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bje0ih930.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:22.284Z

Now the r4 probe script combining the walk and the body-occlusion checks.

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:44.836Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-walk.py",
 "content": "\"\"\"T-209 r4 paralegal review: drive the Step 3 card at commit 1b3c58a (git archive, demo mode, fixture backend, 127.0.0.1:7947) in Chromium.\nFor each service_date reason, compute the backend's own service_date dict for one constructed bill line with the archive's resolver\n(store.charge_service_date), inject it into lib10 a2 (no curated case reaches a confirm note), and record: the date line, the confirm note,\nthe next-step sentence, the buttons, the foot scroll box, and whether the amount (figure) and the date line (service-date) are inside the\nvisible body and pass elementFromPoint at their centers. Viewports 1280x900, 1366x768 (brief) plus 1280x720, 1440x900, 1920x1080 (extra).\nNothing is saved: Yes/No are never pressed.\n\nUsage: .venv/bin/python -I artifacts/review-evidence/T-209-r4-paralegal-walk.py <archive_root>\"\"\"\nimport json\nimport re\nimport sys\nimport time\nimport urllib.request\n\nTREE = sys.argv[1]\nsys.path.insert(0, TREE)\nfrom app.backend import store  # noqa: E402\nfrom playwright.sync_api import sync_playwright  # noqa: E402\n\nBASE = \"http://127.0.0.1:7947\"\nEV = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence\"\nSRC, STMT = \"Fennimoor Spine Clinic, itemized ledger\", \"2026-06-15\"\n\n\ndef api(method, path, body=None):\n    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None),\n                                 headers={\"Content-Type\": \"application/json\"})\n    with urllib.request.urlopen(req, timeout=120) as r:\n        return json.loads(r.read() or b\"null\")\n\n\ndef backend_sd(excerpt):\n    pos = excerpt.index(\"$250.00\")\n    return store.charge_service_date({\"excerpt\": excerpt, \"ladder\": {}}, {\"date_iso\": STMT, \"source\": SRC}, pos)\n\n\nLINES = {\n    \"control_no_injection\": None,\n    \"ambiguous_numeric\": \"Fennimoor Spine Clinic itemized ledger. DOS 04/05/2026: Office visit 99213 - $250.00\",\n    \"two_digit_year\": \"Fennimoor Spine Clinic itemized ledger. DOS 04/05/26: Office visit 99213 - $250.00\",\n    \"no_year\": \"Fennimoor Spine Clinic itemized ledger. DOS April 5: Office visit 99213 - $250.00\",\n    \"invalid\": \"Fennimoor Spine Clinic itemized ledger. DOS 02/30/2026: Office visit 99213 - $250.00\",\n    \"several_dates\": \"Fennimoor Spine Clinic itemized ledger. Dates of service 04/06/2026 and 04/20/2026: Office visit 99213 - $250.00\",\n    \"implausible\": \"Fennimoor Spine Clinic itemized ledger. DOS 09/14/2026: Office visit 99213 - $250.00\",\n    \"non_service_date\": \"Fennimoor Spine Clinic itemized ledger. Office visit 03/04/2026 99213 - $250.00\",\n    \"non_service_date_dob\": \"Fennimoor Spine Clinic itemized ledger. Office visit, 99213, DOB 03/04/1980, $250.00\",\n    \"no_date_dob_sentence\": \"Fennimoor Spine Clinic itemized ledger. Patient DOB 03/04/1980. Office visit, established patient, 99213 - $250.00\",\n    \"no_date\": \"Fennimoor Spine Clinic itemized ledger. Office visit, established patient, 99213 - $250.00\",\n}\n\nJS = \"\"\"(() => {\n  const q = (t) => document.querySelector(`[data-testid=${t}]`);\n  const sd = q('service-date'), fig = q('figure'), foot = q('card-foot'), nx = q('confirm-next'), yes = q('answer-yes'), no = q('answer-no');\n  let body = sd || fig; while (body && body.parentElement && !['auto','scroll'].includes(getComputedStyle(body).overflowY)) body = body.parentElement;\n  const R = (e) => e ? (({top, bottom, left, right}) => ({top: Math.round(top), bottom: Math.round(bottom), left: Math.round(left), right: Math.round(right)}))(e.getBoundingClientRect()) : null;\n  const br = body ? body.getBoundingClientRect() : null, fr = foot ? foot.getBoundingClientRect() : null;\n  const inside = (e) => { if (!e || !br) return null; const r = e.getBoundingClientRect(); const visTop = br.top, visBot = Math.min(br.bottom, fr ? fr.top : br.bottom, innerHeight);\n                          return r.top >= visTop - 1 && r.bottom <= visBot + 1; };\n  const hit = (e) => { if (!e) return null; const r = e.getBoundingClientRect(); const pts = [[r.left + Math.min(10, r.width/2), r.top + r.height/2], [r.left + r.width/2, r.top + r.height/2], [r.left + r.width/2, r.top + 2], [r.left + r.width/2, r.bottom - 2]];\n                       return pts.every(([x, y]) => { const h = document.elementFromPoint(x, y); return !!h && (e === h || e.contains(h)); }); };\n  const fs = foot ? {client: foot.clientHeight, scroll: foot.scrollHeight, overflowY: getComputedStyle(foot).overflowY} : null;\n  const vis = (e) => { if (!e) return null; const r = e.getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight && (!fr || (r.top >= fr.top - 1 && r.bottom <= fr.bottom + 1)); };\n  return {body_client: body && body.clientHeight, body_scroll: body && body.scrollHeight, body_rect: R(body), foot_rect: R(foot), foot_scroll: fs,\n          figure_text: fig && fig.innerText, figure_inside: inside(fig), figure_hit: hit(fig),\n          service_date_text: sd && sd.innerText, service_date_inside: inside(sd), service_date_hit: hit(sd),\n          next_inside_foot: vis(nx), next_hit: hit(nx), yes_inside: vis(yes), no_inside: vis(no), yes_hit: hit(yes), no_hit: hit(no), viewport_h: innerHeight};\n})()\"\"\"\n\nst = api(\"POST\", \"/api/cases\", {\"library\": \"case_lib10_eob_ub04_cms1500\"}); tok = st[\"token\"]\napi(\"POST\", f\"/api/cases/{tok}/run\", {})\nfor _ in range(300):\n    if api(\"GET\", f\"/api/cases/{tok}/status\")[\"status\"] in (\"ready\", \"failed\"):\n        break\n    time.sleep(0.5)\n\nout = {\"commit\": \"1b3c58a\", \"server\": BASE, \"case_token\": tok, \"statement_date\": STMT, \"health\": api(\"GET\", \"/api/health\"), \"runs\": {}}\nSHOTS = {(1280, 900), (1366, 768)}\nwith sync_playwright() as p:\n    browser = p.chromium.launch()\n    for vw, vh in ((1280, 900), (1366, 768), (1280, 720), (1440, 900), (1920, 1080)):\n        for want, line in LINES.items():\n            sd = backend_sd(line) if line else None\n            page = browser.new_page(viewport={\"width\": vw, \"height\": vh})\n            errors = []\n            page.on(\"pageerror\", lambda e: errors.append(str(e)))\n            page.on(\"console\", lambda m: errors.append(m.text) if m.type == \"error\" else None)\n            if sd is not None:\n                def make_rewrite(sd_value):\n                    def rewrite(route, request=None):\n                        r = route.fetch(); body = r.json()\n                        for x in body.get(\"amounts\", []):\n                            if x[\"id\"] == \"a2\":\n                                x[\"service_date\"] = sd_value\n                        route.fulfill(response=r, json=body)\n                    return rewrite\n                page.route(re.compile(rf\"/api/cases/{tok}(\\\\?.*)?$\"), make_rewrite(sd))\n            page.goto(f\"{BASE}/case/{tok}/bills?item=a2\")\n            page.get_by_test_id(\"card-line\").wait_for(timeout=20000)\n            time.sleep(0.6)\n\n            def txt(tid):\n                loc = page.get_by_test_id(tid)\n                return loc.inner_text() if loc.count() else None\n            rec = {\"backend_reason\": sd and sd.get(\"reason\"), \"backend_line\": line, \"backend_text\": sd and sd.get(\"text\"),\n                   \"confirm_note\": txt(\"confirm-note\"), \"confirm_next\": txt(\"confirm-next\"),\n                   \"yes_label\": txt(\"answer-yes\"), \"no_label\": txt(\"answer-no\"), \"layout\": page.evaluate(JS), \"console_errors\": errors}\n            out[\"runs\"][f\"{vw}x{vh}:{want}\"] = rec\n            if (vw, vh) in SHOTS:\n                page.screenshot(path=f\"{EV}/T-209-r4-step3-{want}-{vw}x{vh}.png\", full_page=False)\n            page.close()\n    browser.close()\napi(\"DELETE\", f\"/api/cases/{tok}\")\nwith open(f\"{EV}/T-209-r4-paralegal-walk.json\", \"w\") as f:\n    json.dump(out, f, indent=2, ensure_ascii=False)\nprint(\"wrote\", f\"{EV}/T-209-r4-paralegal-walk.json\")\n"
}
````

### User / tool · 2026-11-03T02:05:44.941Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-walk.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:47.789Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-walk.py",
 "old_string": "(\\\\?.*)?$\"",
 "new_string": "(\\?.*)?$\""
}
````

### User / tool · 2026-11-03T02:05:47.899Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-walk.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:48.525Z

**tool call — Bash**
````
{
 "command": "curl -s http://127.0.0.1:7947/api/health; echo; lsof -iTCP:7947 -sTCP:LISTEN -nP",
 "description": "Check server health and listener PID"
}
````

### User / tool · 2026-11-03T02:05:48.705Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  65212 arsis    9u  IPv4 0x8e16b1dfb84f2c90      0t0  TCP 127.0.0.1:7947 (LISTEN)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:52.518Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-209-r4-paralegal-walk.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t209r4 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-walk.log 2>&1; echo \"exit $?\"; tail -3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-walk.log",
 "description": "Run the r4 Step 3 walk",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:06:35.775Z

**tool result**
````
exit 0
wrote /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-walk.json
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:06:36.563Z

Now a summarizer script to read the JSON compactly.

### Assistant · claude-opus-5-5 · 2026-11-03T02:06:44.111Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-summary.py",
 "content": "\"\"\"Summarize T-209-r4-paralegal-walk.json: per reason the note and the sentence (1280x900), and per run the layout booleans.\nUsage: .venv/bin/python -I artifacts/review-evidence/T-209-r4-paralegal-summary.py\"\"\"\nimport json\n\nEV = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence\"\nd = json.load(open(f\"{EV}/T-209-r4-paralegal-walk.json\"))\nprint(\"commit\", d[\"commit\"], \"demo_mode\", d[\"health\"].get(\"demo_mode\"), \"backend\", d[\"health\"].get(\"backend\"))\nprint(\"=== texts at 1280x900 ===\")\nfor k, r in d[\"runs\"].items():\n    if k.startswith(\"1280x900:\"):\n        print(\"--\", k, \"| reason:\", r[\"backend_reason\"], \"| text:\", r[\"backend_text\"])\n        print(\"   NOTE:\", r[\"confirm_note\"])\n        print(\"   NEXT:\", r[\"confirm_next\"])\n        print(\"   YES/NO:\", r[\"yes_label\"], \"/\", r[\"no_label\"])\ntexts = {}\nfor k, r in d[\"runs\"].items():\n    texts.setdefault(k.split(\":\", 1)[1], set()).add(r[\"confirm_next\"])\nprint(\"=== distinct sentences per reason across viewports ===\")\nfor w, s in texts.items():\n    print(w, len(s))\nprint(\"=== layout ===\")\nbad = 0\nfor k, r in d[\"runs\"].items():\n    L = r[\"layout\"]\n    fs = L[\"foot_scroll\"] or {}\n    ok = all([L[\"figure_inside\"], L[\"figure_hit\"], L[\"service_date_inside\"], L[\"service_date_hit\"]])\n    foot_ok = fs.get(\"scroll\") is None or fs.get(\"scroll\") <= fs.get(\"client\") + 1\n    btn_ok = L[\"yes_hit\"] and L[\"no_hit\"]\n    nx_ok = L[\"next_hit\"] if r[\"confirm_next\"] else True\n    if not (ok and foot_ok and btn_ok and nx_ok):\n        bad += 1\n    print(f\"{k:38s} body {L['body_client']}/{L['body_scroll']} foot {fs.get('client')}/{fs.get('scroll')} {fs.get('overflowY')} | fig in={L['figure_inside']} hit={L['figure_hit']} | date in={L['service_date_inside']} hit={L['service_date_hit']} | next hit={L['next_hit']} | yes/no hit={L['yes_hit']}/{L['no_hit']} | errs={len(r['console_errors'])}\")\nprint(\"runs with any problem:\", bad, \"of\", len(d[\"runs\"]))\n"
}
````

### User / tool · 2026-11-03T02:06:44.211Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-summary.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:06:45.461Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-209-r4-paralegal-summary.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-summary.txt 2>&1; cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-summary.txt",
 "description": "Summarize walk results"
}
````

### User / tool · 2026-11-03T02:06:45.572Z

**tool result**
````
commit 1b3c58a demo_mode True backend fixture
=== texts at 1280x900 ===
-- 1280x900:control_no_injection | reason: None | text: None
   NOTE: None
   NEXT: None
   YES/NO: Yes, count it / No, don't count it
-- 1280x900:ambiguous_numeric | reason: ambiguous_numeric | text: date of service [__________] (statement dated June 15, 2026)
   NOTE: The highlighted words label 04/05/2026 as the date of service, and it can be read as month/day or day/month; the record does not settle which. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the highlighted words and fill the blank before you rely on it.
   NEXT: What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
   YES/NO: Yes, count it / No, don't count it
-- 1280x900:two_digit_year | reason: two_digit_year | text: date of service [__________] (statement dated June 15, 2026)
   NOTE: The highlighted words label 04/05/26 as the date of service, but it has a two-digit year, which the code does not guess. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the highlighted words and fill the blank before you rely on it.
   NEXT: What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
   YES/NO: Yes, count it / No, don't count it
-- 1280x900:no_year | reason: no_year | text: date of service [__________] (statement dated June 15, 2026)
   NOTE: The highlighted words label April 5 as the date of service, but it states no year, which the code does not borrow from the statement. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the highlighted words and fill the blank before you rely on it.
   NEXT: What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
   YES/NO: Yes, count it / No, don't count it
-- 1280x900:invalid | reason: invalid | text: date of service [__________] (statement dated June 15, 2026)
   NOTE: The highlighted words label 02/30/2026 as the date of service, but it is not a complete date on the calendar. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the highlighted words and fill the blank before you rely on it.
   NEXT: What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
   YES/NO: Yes, count it / No, don't count it
-- 1280x900:several_dates | reason: several_dates | text: date of service [__________] (statement dated June 15, 2026)
   NOTE: The highlighted words label more than one date of service (04/06/2026, 04/20/2026) and nothing says which one belongs to this charge. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the highlighted words and fill the blank before you rely on it.
   NEXT: What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
   YES/NO: Yes, count it / No, don't count it
-- 1280x900:implausible | reason: implausible | text: date of service [__________] (statement dated June 15, 2026)
   NOTE: The highlighted words label 09/14/2026 as the date of service, but that date is after the statement it appears on or years before it. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the highlighted words and fill the blank before you rely on it.
   NEXT: What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
   YES/NO: Yes, count it / No, don't count it
-- 1280x900:non_service_date | reason: non_service_date | text: date of service [__________] (statement dated June 15, 2026)
   NOTE: The only date near this line (03/04/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated line-by-line bill, or fill the blank from the record, before you rely on it.
   NEXT: What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
   YES/NO: Yes, count it / No, don't count it
-- 1280x900:non_service_date_dob | reason: non_service_date | text: date of service [__________] (statement dated June 15, 2026)
   NOTE: The only date near this line (03/04/1980) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated line-by-line bill, or fill the blank from the record, before you rely on it.
   NEXT: What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
   YES/NO: Yes, count it / No, don't count it
-- 1280x900:no_date_dob_sentence | reason: no_date | text: date of service [__________] (statement dated June 15, 2026)
   NOTE: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated line-by-line bill, or fill the blank from the record, before you rely on it.
   NEXT: What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
   YES/NO: Yes, count it / No, don't count it
-- 1280x900:no_date | reason: no_date | text: date of service [__________] (statement dated June 15, 2026)
   NOTE: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated line-by-line bill, or fill the blank from the record, before you rely on it.
   NEXT: What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
   YES/NO: Yes, count it / No, don't count it
=== distinct sentences per reason across viewports ===
control_no_injection 1
ambiguous_numeric 1
two_digit_year 1
no_year 1
invalid 1
several_dates 1
implausible 1
non_service_date 1
non_service_date_dob 1
no_date_dob_sentence 1
no_date 1
=== layout ===
1280x900:control_no_injection          body 201/201 foot 149/149 auto | fig in=True hit=True | date in=True hit=True | next hit=None | yes/no hit=True/True | errs=0
1280x900:ambiguous_numeric             body 133/167 foot 217/217 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1280x900:two_digit_year                body 133/167 foot 217/217 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1280x900:no_year                       body 133/167 foot 217/217 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1280x900:invalid                       body 154/167 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1280x900:several_dates                 body 133/167 foot 217/217 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1280x900:implausible                   body 133/167 foot 217/217 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1280x900:non_service_date              body 120/167 foot 230/238 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1280x900:non_service_date_dob          body 120/167 foot 230/238 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1280x900:no_date_dob_sentence          body 174/174 foot 176/176 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1280x900:no_date                       body 174/174 foot 176/176 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1366x768:control_no_injection          body 155/168 foot 119/119 auto | fig in=True hit=True | date in=True hit=True | next hit=None | yes/no hit=True/True | errs=0
1366x768:ambiguous_numeric             body 94/113 foot 180/180 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1366x768:two_digit_year                body 94/113 foot 180/180 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1366x768:no_year                       body 94/113 foot 180/180 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1366x768:invalid                       body 94/113 foot 180/180 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1366x768:several_dates                 body 94/113 foot 180/180 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1366x768:implausible                   body 94/113 foot 180/180 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1366x768:non_service_date              body 90/113 foot 184/200 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1366x768:non_service_date_dob          body 90/113 foot 184/200 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1366x768:no_date_dob_sentence          body 114/114 foot 160/160 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1366x768:no_date                       body 114/114 foot 160/160 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1280x720:control_no_injection          body 107/168 foot 119/119 auto | fig in=True hit=True | date in=False hit=False | next hit=None | yes/no hit=True/True | errs=0
1280x720:ambiguous_numeric             body 90/113 foot 136/200 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1280x720:two_digit_year                body 90/113 foot 136/180 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1280x720:no_year                       body 90/113 foot 136/180 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1280x720:invalid                       body 90/113 foot 136/180 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1280x720:several_dates                 body 90/113 foot 136/200 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1280x720:implausible                   body 90/113 foot 136/180 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1280x720:non_service_date              body 90/113 foot 136/200 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1280x720:non_service_date_dob          body 90/113 foot 136/200 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1280x720:no_date_dob_sentence          body 90/113 foot 136/160 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1280x720:no_date                       body 90/113 foot 136/160 auto | fig in=True hit=True | date in=True hit=True | next hit=False | yes/no hit=True/True | errs=0
1440x900:control_no_injection          body 201/201 foot 149/149 auto | fig in=True hit=True | date in=True hit=True | next hit=None | yes/no hit=True/True | errs=0
1440x900:ambiguous_numeric             body 154/167 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1440x900:two_digit_year                body 154/167 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1440x900:no_year                       body 154/167 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1440x900:invalid                       body 154/167 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1440x900:several_dates                 body 154/167 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1440x900:implausible                   body 154/167 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1440x900:non_service_date              body 133/167 foot 217/217 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1440x900:non_service_date_dob          body 133/167 foot 217/217 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1440x900:no_date_dob_sentence          body 174/174 foot 176/176 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1440x900:no_date                       body 174/174 foot 176/176 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1920x1080:control_no_injection         body 381/381 foot 149/149 auto | fig in=True hit=True | date in=True hit=True | next hit=None | yes/no hit=True/True | errs=0
1920x1080:ambiguous_numeric            body 334/334 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1920x1080:two_digit_year               body 334/334 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1920x1080:no_year                      body 334/334 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1920x1080:invalid                      body 334/334 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1920x1080:several_dates                body 334/334 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1920x1080:implausible                  body 334/334 foot 196/196 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1920x1080:non_service_date             body 313/313 foot 217/217 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1920x1080:non_service_date_dob         body 313/313 foot 217/217 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1920x1080:no_date_dob_sentence         body 354/354 foot 176/176 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
1920x1080:no_date                      body 354/354 foot 176/176 auto | fig in=True hit=True | date in=True hit=True | next hit=True | yes/no hit=True/True | errs=0
runs with any problem: 15 of 55
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:07:54.114Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"D-071\" memory/ORCHESTRATOR_DECISIONS.md | head; grep -n -i \"confirm the date\\|confirm_note\\|_ASK_WRITTEN\" memory/ORCHESTRATOR_DECISIONS.md spec/*.md memory/contracts/api.md | head -20",
 "description": "Find D-071 and confirm-note spec text"
}
````

### User / tool · 2026-11-03T02:07:54.211Z

**tool result**
````
84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
87:## D-071 amendment — when the service date is not certain, print none and ask the human
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
93:- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
94:- D-071 amendment 2 (§7.4 after T-202 r3; round 4 authorised, final): (a) a record's own date is a service date only for a positively identified encounter record (visit/ER/clinic/therapy/ambulance-run note); bills, receipts, superbills, charge summaries and unknown types never lend their header date; (b) in prose, only "date of service", "dates of service", "DOS" and "service date" are labels ("visit date", "seen on" and bare "date" are not; they also name next or prior visits); (c) letter_check keeps an independent scanner but reads the same declared encounter-type table (one data file), and anchors the blank; (d) if round 4 fails, the fallback is the most conservative rule: every charge line prints the fillable blank unless a DOS column or one of the (b) labels ties exactly one date to it.
95:- D-071 amendment 2 note (T-202 r4): inside bills only, "visit of", "the run of", "rendered on" and "service period" also count as service labels (case_09 and lib14 need them); outside bills they do not. Accepted.
memory/ORCHESTRATOR_DECISIONS.md:88:T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.
memory/contracts/api.md:574:Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges accepted from these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte; **no dollar amount appears in `letter_text` outside the BILLED CHARGES section (T-139)**: an entry whose summary or quote states an amount is never written into the treatment section, whatever its review status (see "Dollar amounts in entries"), a charge's `Source` line quotes only the clause that holds its own figure when the sentence also states another one (a rate, a balance, another line item), and a dismissed charge is never listed under BILLS TO REQUEST. Rates, estimates, unclear and dismissed amounts appear only in `internal_notes_text`. **T-200 + D-071 (+ amendments, T-202 r4): a charge line prints a date of service only when positive evidence ties it to the line (an allow-list).** The line before a charge's quote prints the service date the bill line itself states (`<provider>, <source label>, March 27, 2026: $250.00`), never the record's date, which for a ledger, invoice or UB-04 is the statement's. A service period prints as a range (`June 9\u201312, 2026`, `June 28\u2013July 2, 2026`, its own stated year). Code (`app/backend/service_date.py`) takes a date as the line's date of service ONLY when it is tied to the line by (a) a table column heading that names service (DOS, date of service, service date, from/to service, 24A, visit date), (b) a service label in the same clause, with a dotted leader, spaces or a colon allowed between the label and the date (in prose ONLY "DOS", "date of service", "dates of service" and "service date", never after next, last, prior, previous, initial, first, return, follow-up, scheduled, upcoming or future; "visit date", "seen on" and a bare "date" are NOT labels, D-071 amendment 2. A bill also reads its own wording for what it covers: "visit of", "services rendered on", "the run of", "service period"; and on a UB-04 "statement covers period"), (c) being the date cell of the charge row itself in such a table, or (d) for a coded line (CPT, HCPCS, revenue code) with no date of its own, the one period the bill states for its services ("dates of service ...", "the run of ...", UB-04 "statement period ..."). Any other date (birth, injury, accident, onset, referral, order, authorization, entry, transaction, issued, printed, posted, statement, or no label at all; a column headed Date, Entry date, Transaction Date, Posted ...) is never the service date. Results: (1) **one certain labeled date or complete period** prints (a numeric date readable two ways, `04/05/2026`, is read only when a reading after the record's own date is impossible for EVERY labeled end; a stated date after its record's own date or more than five years before it is doubtful); (2) **every other charge line** (the quote labels no date of service, or labels one the code cannot read with certainty: readable two ways, two-digit year, no year, not on the calendar, several labeled dates, implausible) prints the fillable blank of the D-071 addendum, like the Bates placeholder, never an inferred or half-read date: `<provider>, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00` (`<provider>, itemized ledger, date of service [__________]: $250.00` when the record has no date either). The paralegal fills it from the quote. **The record's own date is the line's date only for a positively identified encounter record** (a visit, ER, clinic, therapy, imaging or ambulance-run note; the declared table `app/backend/encounter_types.json`, read by `service_date.record_kind` and by `evals/letter_check.py`): such a record with no labeled date keeps the visit date. A bill, receipt, superbill, charge summary, fee schedule, estimate, administrative paper (phone note, letter, affidavit) or record of unknown type never lends its header date, so it prints the blank unless a label ties a date to the line. The internal notes add a `CHARGES WITHOUT A CERTAIN DATE OF SERVICE` section (provider, amount, why, the date as the quote writes it, "request a dated itemized bill") when any accepted charge prints the blank. Charges are listed in service-date order (a charge with no stated date sorts by its statement date). The export case dict carries `dos_iso` / `dos_end_iso` / `dos_text` / `dos_note` on each charge (`store.charge_service_date`); a hand-built case without `dos_iso` keeps the old `<provider>, <record date>` line, and one without `dos_text` prints the blank. `evals/letter_check.py` checks every charge line's printed date against THAT line's own quote (plus, when the quote labels no date, the one period the bill states before it) with its own allow-list scanner that shares no code with the production parser (it reads only the same declared record-type table); it accepts the blank in its exact form and nothing else for a line with no certain date, fails the blank above a certain labeled date, and fails any date no service label ties to the line. **Case view (Step 3):** every charge in `amounts[]` (case view, review responses, item view) carries `service_date` (`null` for any other kind), the same value the letter prints: `{"state": "stated"|"not_stated", "date_iso": "2026-06-09"|null, "end_iso": "2026-06-12"|null, "text": "June 9\u201312, 2026" | "date of service [__________] (statement dated June 15, 2026)", "statement_date_iso": "2026-06-19"|null (the record's date; for a bill it is the statement's), "reason": null | "ambiguous_numeric" | "two_digit_year" | "no_year" | "invalid" | "several_dates" | "implausible" | "non_service_date" | "no_date", "confirm_note": null | "<why the date is not certain>. The letter prints no service date for this line. It leaves a blank for the date of service. [Confirm the date from the quote and fill the blank before you rely on it. | Request a dated itemized bill, or fill the blank from the record, before you rely on it.]"}`. A stated charge has `reason` and `confirm_note` null; show `text` as the charge's date and label the record's own date as the statement date (`statement_date_iso`). A not-stated charge shows `text` and the `confirm_note` (null only for a charge she counted through D-064, who already knows the line has no date). `reason` in `ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible` means the quote labels a date the code cannot read (the `confirm_note` names it as written); `non_service_date` and `no_date` mean the quote labels none. Either way `text` is the blank. `text` is byte-for-byte the string after the provider in the letter line (`<provider>, <text>: $X`). There is no control that lets her enter a date in the app: she fills the blank in the letter herself.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:07.986Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; head -5 artifacts/review-evidence/T-209-r3-paralegal-pytest.txt; grep -n \"BASE\\|environ\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t209r4/tests/e2e/conftest.py | head",
 "description": "Check how r3 ran pytest"
}
````

### User / tool · 2026-11-03T02:08:08.078Z

**tool result**
````
...........                                                              [100%]
11 passed in 11.21s
106:SERVER = os.environ.get("E2E_BASE_URL", "http://localhost:7860")      # the app's root: the guided UI (D-068) is served here, and every /api call goes here
107:BASE = SERVER + "/classic"                                              # D-068: the old screen moved to /classic; the whole classic suite navigates from BASE, API calls use SERVER
118:    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
119:    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
121:    global BASE, SERVER
122:    if os.environ.get("E2E_BASE_URL") or os.environ.get("ZLAYT_DB"):
127:    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
156:    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; SERVER = base; BASE = base + "/classic"
168:    path = os.environ.get("ZLAYT_DB")
170:        msg = "needs ZLAYT_DB (the SQLite file of the server under test); a plain `pytest tests/e2e` starts its own server and sets it, a run against E2E_BASE_URL does not"
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:14.103Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t209r4 && E2E_BASE_URL=http://127.0.0.1:7947 ZLAYT_DB=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t209r4.db PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/e2e/guided/test_t206.py tests/e2e/guided/test_t205.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-pytest.txt 2>&1; echo \"exit $?\"; tail -3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-pytest.txt",
 "description": "Run guided e2e tests from archive against my server",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:08:35.010Z

**tool result**
````
exit 0
......................                                                   [100%]
22 passed in 20.59s
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:36.010Z

Now look at the screenshots that matter (non_service_date at 1366x768 where the foot overflows, and one doubtful at both sizes).

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:36.613Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-step3-non_service_date-1366x768.png"
}
````

### User / tool · 2026-11-03T02:08:36.623Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:37.110Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-step3-implausible-1280x900.png"
}
````

### User / tool · 2026-11-03T02:08:37.132Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:40.000Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-step3-no_date-1366x768.png"
}
````

### User / tool · 2026-11-03T02:08:40.014Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:42.991Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 1b3c58a:tests/e2e/guided/test_t206.py | grep -n \"viewport\\|parametrize\\|reason\\|scrollHeight\\|elementFromPoint\\|highlighted\" | head -40",
 "description": "Inspect e2e coverage of reasons and viewports"
}
````

### User / tool · 2026-11-03T02:08:43.099Z

**tool result**
````
54:NEXT = "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank"
57:def inject(page, tok, reason, raw):
60:    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason=reason, text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note(reason, raw))
77:      const t = document.elementFromPoint(r.left + r.width / 2, r.top + r.height / 2); return e.contains(t) || t.contains(e) ? 'ok' : 'covered by ' + t.tagName + '.' + t.className; }""", el)
80:@pytest.mark.parametrize("reason,raw", REASONS)
81:def test_every_not_certain_reason_gets_the_same_next_step_that_cannot_contradict_the_note(page, make, reason, raw):
83:    tok = make(LIB10); sd = inject(page, tok, reason, raw)
92:    assert "highlighted words labels" not in note and " labels " not in note, note
93:    if "labels" in SD.confirm_note(reason, raw):
94:        assert "The highlighted words label " in note, note
105:@pytest.mark.parametrize("size", [(1280, 900), (1366, 768)])
106:@pytest.mark.parametrize("reason,raw", [REASONS[0], REASONS[6], REASONS[4]])
107:def test_the_confirm_box_never_hides_the_amount_or_the_date_line(page, make, reason, raw, size):
109:    page.set_viewport_size({"width": size[0], "height": size[1]})
110:    tok = make(LIB10); inject(page, tok, reason, raw)
113:    assert page.evaluate("(() => { const f = document.querySelector('[data-testid=card-foot]'); return f.scrollHeight <= f.clientHeight + 1; })()"), "the foot clips the next step"
124:    sd = dict(a["service_date"], state="not_stated", date_iso=None, end_iso=None, reason="no_year", text=SD.not_stated_text("2026-06-19"), confirm_note=SD.confirm_note("no_year", "April 5"))
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:44.690Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 1b3c58a:tests/e2e/guided/test_t206.py | sed -n 40,56p; git show 1b3c58a:tests/e2e/guided/test_t206.py | sed -n 80,104p",
 "description": "Read REASONS list and contradiction test"
}
````

### User / tool · 2026-11-03T02:08:44.808Z

**tool result**
````
    tok = make(LIB11); a = item(tok, "a2")
    st, r = C.api("POST", f"/api/cases/{tok}/items/a2/review", {"action": "count", "confirm": "separate_charge", "version": a["version"], "expected_status": "pending",
                                                              **({"confirm_flag": a["count_confirm"]["confirm_with"]} if a.get("count_confirm") else {})}); assert st == 200, r
    open_item(page, tok, "a2", step="bills")
    sd = item(tok, "a2")["service_date"]
    assert sd["state"] == "not_stated" and "statement dated June 15, 2026" in sd["text"]
    expect(page.get_by_test_id("service-date-text")).to_have_text(sd["text"])
    for k, v in texts(page).items():
        assert not BARE.search(v), (k, v)
    assert seen == [], seen


REASONS = [("ambiguous_numeric", "04/05/2026"), ("two_digit_year", "04/05/26"), ("no_year", "April 5"), ("invalid", "02/30/2026"), ("several_dates", "04/06/2026 and 04/20/2026"),
           ("implausible", "09/14/2026"), ("no_date", ""), ("non_service_date", "03/04/1980")]
NEXT = "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank"


@pytest.mark.parametrize("reason,raw", REASONS)
def test_every_not_certain_reason_gets_the_same_next_step_that_cannot_contradict_the_note(page, make, reason, raw):
    seen = watch(page)
    tok = make(LIB10); sd = inject(page, tok, reason, raw)
    open_item(page, tok, "a2", step="bills")
    nxt = page.get_by_test_id("confirm-next"); expect(nxt).to_be_visible()
    t = nxt.inner_text()
    assert NEXT in t and "\u201Cdate of service [__________]\u201D in your letter" in t, t
    assert "Counting it adds the amount to the bill total." in t and "If you don't," not in t, t
    assert "Fill the blank" not in t and "check the date" not in t.lower() and "you checked" not in t.lower() and "yourself" not in t, t
    assert "The date in parentheses is the statement date, not the service date." in t
    note = page.get_by_test_id("confirm-note").inner_text()
    assert "highlighted words labels" not in note and " labels " not in note, note
    if "labels" in SD.confirm_note(reason, raw):
        assert "The highlighted words label " in note, note
    assert page.get_by_test_id("service-date").inner_text().lower().count("date of service") == 1
    labels = [page.get_by_test_id("answer-yes").inner_text().strip(), page.get_by_test_id("answer-no").inner_text().strip()]
    assert labels == ["Yes, count it", "No, don't count it"], "the sentence names the buttons the card really has"
    assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-next]").count() == 1
    assert page.get_by_test_id("card-foot").locator("[data-testid=confirm-note]").count() == 1
    for k, v in texts(page).items():
        assert not BARE.search(v), (k, v)
    assert seen == [], seen
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:09:04.768Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 1b3c58a:app/frontend/guided/step3.js | grep -n \"confirmNext\\|may help\\|Counting it\" ; git show 1b3c58a:app/frontend/guided/step3.css | grep -n \"card-b { flex\\|max-height: 820px\\|max-height: none\"; git show 8521562:app/backend/service_date.py | grep -n \"Confirm the date from the quote\"; kill 65212; lsof -iTCP:7947 -sTCP:LISTEN -nP; echo \"lsof exit $?\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7947/api/health",
 "description": "Get line refs and stop my server"
}
````

### User / tool · 2026-11-03T02:09:05.011Z

**tool result (error)**
````
Exit code 7
36:  const confirmNext = (sd) => {
38:    return h("p", { class: "svc-next", "data-testid": "confirm-next" }, h("b", {}, "What to do: "), "find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank ", h("b", {}, "\u201Cdate of service [__________]\u201D"), " in your letter." + stmt,
39:      " Counting it adds the amount to the bill total.");
67:        foot: sd && sd.confirm_note ? { cls: "attn", nodes: [confirmNote(sd), confirmNext(sd), ...(foot.length ? [h("div", { class: "gap-top" }, ...foot)] : [])] } : { cls, nodes: foot },          // T-205: the date is not certain: the note leads the foot, in plain words, under the highlighted quote
23:  .card:has(.svc-next) .card-b { flex: 1 1 0; min-height: 120px; }
24:  .card-f:has(.svc-next) { height: auto; min-height: 0; max-height: none; flex: 0 1 auto; }
27:@media (min-width: 761px) and (max-height: 820px) {
102:_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  65212 arsis    9u  IPv4 0x8e16b1dfb84f2c90      0t0  TCP 127.0.0.1:7947 (LISTEN)
lsof exit 0
000
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:09:06.742Z

**tool call — Bash**
````
{
 "command": "lsof -iTCP:7947 -sTCP:LISTEN -nP; echo \"lsof exit $?\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7947/api/health",
 "description": "Confirm server stopped"
}
````

### User / tool · 2026-11-03T02:09:06.910Z

**tool result (error)**
````
Exit code 7
lsof exit 1
000
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:09:13.094Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py artifacts/review-evidence/T-209-r4-step3-non_service_date-1366x768.png artifacts/review-evidence/T-209-r4-step3-implausible-1280x900.png artifacts/review-evidence/T-209-r4-step3-ambiguous_numeric-1366x768.png artifacts/review-evidence/T-209-r4-step3-no_date-1366x768.png; ls reviews/T-209-paralegal-r4.md 2>&1 | tail -1; git diff --stat 1b3c58a 0281189 -- app tests | wc -l",
 "description": "Verify evidence paths exist before writing"
}
````

### User / tool · 2026-11-03T02:09:13.214Z

**tool result**
````
artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py
artifacts/review-evidence/T-209-r4-step3-ambiguous_numeric-1366x768.png
artifacts/review-evidence/T-209-r4-step3-implausible-1280x900.png
artifacts/review-evidence/T-209-r4-step3-no_date-1366x768.png
artifacts/review-evidence/T-209-r4-step3-non_service_date-1366x768.png
ls: reviews/T-209-paralegal-r4.md: No such file or directory
       0
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:01.575Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-draft.md",
 "content": "# T-209 review r4 (final round): paralegal-reviewer (Maria Delgado persona)\n\nScope: fix commit 1b3c58a (`app/frontend/guided/step3.js:36-39`, `step3.css:22-33`, `review.js:26`, `tests/e2e/guided/test_t206.py`). HEAD is 0281189, and `git diff --stat 1b3c58a 0281189 -- app tests` is empty, so the UI is the same. I served a fresh `git archive 1b3c58a` in demo mode (`/api/health`: `\"backend\":\"fixture\",\"demo_mode\":true`) on 127.0.0.1:7947, listener PID 65212. I stopped it afterward: `lsof` exit 1, `curl` 000. Synthetic data only.\n\nVerdict: **pass**. No blocker, no major. Four minors, one nit.\n\nThe new sentence is the same for every reason:\n\n> What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank \"date of service [__________]\" in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.\n\n**Does it contradict the note above it?** I checked each reason (walk JSON, 1280x900 texts):\n- `two_digit_year`: no clash. The note says to confirm the date from the highlighted words, and the sentence agrees.\n- `ambiguous_numeric`, `several_dates`, `no_year`, `invalid`, `implausible`: the two lines give different first steps. The note ends \"Confirm the date from the highlighted words and fill the blank\". The sentence says \"find the date of service in the record (the highlighted words may help) or ask the provider\". The sentence does not say the opposite of the note. It is wider than the note, and it is the safe route: neither line tells her to copy the highlighted date anymore. The harmful part is in the note itself. For these five reasons, the note's first sentence says the highlighted words cannot settle the date or that the date is wrong, and its last sentence says to confirm the date from those same words. That wording is binding decision text (`memory/ORCHESTRATOR_DECISIONS.md:88` \"asking the user to confirm the date from the quote\"; `:93` \"The paralegal fills it from the quote\"). It is not in the 1b3c58a diff, and changing it needs a decision. One wording clash is new: for `ambiguous_numeric`, the note says \"the record does not settle which\" and the sentence says \"find the date of service in the record\". **Severity: minor.** The letter prints the blank whatever she does. The note names the defect (Feb 30, after the statement, two readings), and the sentence now gives her a way out to the provider. In round 3, the sentence itself pointed her at the wrong date. That was the major, and it is gone.\n- `no_date` and `non_service_date`: the note says \"Request a dated line-by-line bill, or fill the blank from the record\". The sentence agrees, except for \"(the highlighted words may help)\". On a `no_date` line, the note says \"The line states no date of service.\" On my DOB variant, the only date in the highlighted words is a birth date. So round 3's \"never points at the highlighted words\" is partly undone, in a hedged form. Minor.\n\n**Are the amount and date line visible?** Yes, at both brief viewports, for every reason and the control. In 22 of 22 runs, the figure and the service-date line are inside the visible body and pass `elementFromPoint` at four points each. One reason still clips the sentence: `non_service_date` (the longest note) at 1366x768. The foot is clientHeight 184 against scrollHeight 200, so \"...adds the amount to the bill total.\" is cut. The e2e layout test does not include that reason.\n\n---\n\n```json\n{\"card\": \"T-209\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"fix commit 1b3c58a (app/frontend/guided/step3.js:36-39, step3.css:22-33, review.js:26, tests/e2e/guided/test_t206.py); HEAD 0281189 with git diff --stat 1b3c58a 0281189 -- app tests empty; app served from a fresh git archive of 1b3c58a in demo mode (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local; /api/health backend fixture, demo_mode true) at http://127.0.0.1:7947, listener PID 65212, stopped (lsof exit 1, curl 000); case_lib10_eob_ub04_cms1500 a2 with the archive backend's own service_date dict injected per reason (no curated case reaches a confirm note).\",\n \"exercised\": [\n  \"Read personas/paralegal.md in full, reviews/T-209-paralegal-r3.md, board.py show T-209 (r3 handoff: one sentence for every reason, note untouched, consequence cut to 'Counting it adds the amount to the bill total.', layout min-height for body, 'labels' -> 'label'; left: minor 7 and backend _ASK_WRITTEN)\",\n  \"git show 1b3c58a -- app/frontend (step3.js, step3.css, review.js); git show 1b3c58a:app/backend/service_date.py lines 145-162 (_WHY, _ASK_WRITTEN, _ASK_NONE); git show 8521562:app/backend/service_date.py:102 (_ASK_WRITTEN text unchanged since r3)\",\n  \"memory/ORCHESTRATOR_DECISIONS.md:88 and :93 (binding D-071 wording: confirm the date from the quote; the paralegal fills it from the quote)\",\n  \"pytest tests/e2e/guided/test_t206.py tests/e2e/guided/test_t205.py from the archive against 127.0.0.1:7947: 22 passed (artifacts/review-evidence/T-209-r4-paralegal-pytest.txt)\",\n  \"artifacts/review-evidence/T-209-r4-paralegal-walk.py -> T-209-r4-paralegal-walk.json, summarized by T-209-r4-paralegal-summary.py -> T-209-r4-paralegal-summary.txt: Chromium, 10 constructed bill lines resolved by the archive's store.charge_service_date (ambiguous_numeric, two_digit_year, no_year, invalid, several_dates, implausible, two non_service_date, two no_date) plus a no-injection control, each at 1280x900, 1366x768 (brief), 1280x720, 1440x900 and 1920x1080 (55 runs): note, sentence, button labels, foot scroll box, figure and service-date inside the visible body and elementFromPoint at 4 points, sentence and Yes/No hit tests, console errors (0 in every run)\",\n  \"Read screenshots T-209-r4-step3-non_service_date-1366x768.png, T-209-r4-step3-implausible-1280x900.png, T-209-r4-step3-no_date-1366x768.png\",\n  \"Did not press Yes or No (an injected sd is not what the backend exports); export.py is outside the 1b3c58a diff\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"verify_quickly\": 4, \"next_step_exact_doubtful_written_date\": 3, \"next_step_exact_no_date\": 3, \"never_contradicts_note\": 3, \"amount_and_date_visible_1280x900_1366x768\": 5},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Written-date reasons: the note says 'Confirm the date from the highlighted words', the sentence says 'find the date of service in the record ... or ask the provider'. These are two different first steps, not opposite ones. For ambiguous_numeric the note's 'the record does not settle which' clashes with the sentence's 'find the date of service in the record'\",\n   \"evidence\": \"T-209-r4-paralegal-summary.txt, 1280x900. NOTE (implausible): 'The highlighted words label 09/14/2026 as the date of service, but that date is after the statement it appears on or years before it. ... Confirm the date from the highlighted words and fill the blank before you rely on it.' NOTE (ambiguous_numeric): '... the record does not settle which. ... Confirm the date from the highlighted words and fill the blank before you rely on it.' NEXT (every reason): 'What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter.' Note text: service_date.py:156 (_ASK_WRITTEN at 1b3c58a; same text at 8521562:102). Binding wording: ORCHESTRATOR_DECISIONS.md:88 'asking the user to confirm the date from the quote', :93 'The paralegal fills it from the quote'. Screenshot T-209-r4-step3-implausible-1280x900.png. test_t206.py:81 is named '..._that_cannot_contradict_the_note' but asserts nothing about the note's instruction.\",\n   \"why_it_matters\": \"Severity judgment (brief asked): minor, not major. The sentence no longer sends her to a wrong date, and it adds the provider route the note lacks. Following either line still leaves the blank in the letter. The remaining risk is in the note: on invalid and implausible lines, nothing on the card says 'do not copy the highlighted date'. A junior paralegal who follows the bold note could write September 14, 2026 into a charge billed on June 15, 2026. That is the date an adjuster checks. The note follows a binding decision, so the fix needs an orchestrator call, not a frontend change.\",\n   \"fix\": \"Amend the D-071 note wording per reason (backend _ASK_WRITTEN, T-202 owner): two_digit_year keep 'Confirm the date from the highlighted words'; ambiguous_numeric, several_dates, no_year: 'Match it to this provider's visit note in Step 2, or ask the provider'; invalid, implausible: 'Do not copy the highlighted date; find it in this provider's visit note in Step 2, or ask the provider for a corrected bill.' In the sentence, say 'this provider's visit note (Step 2)' instead of 'the record'.\",\n   \"acceptance_test\": \"E2E over the six written reasons: for ambiguous_numeric, several_dates, no_year, invalid and implausible, neither confirm-note nor confirm-next contains 'Confirm the date from the highlighted words'; for invalid and implausible one of them contains 'Do not copy the highlighted date'; confirm-next does not contain 'in the record' when confirm-note contains 'the record does not settle'.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"No-date and non-service-date lines: the sentence points at the highlighted words ('may help') right under a note that says the line states no date of service; 'the record' is still the dateless bill (r3 minor 4 not fixed)\",\n   \"evidence\": \"T-209-r4-paralegal-summary.txt, 1280x900:no_date NOTE: 'The line states no date of service. ... Request a dated line-by-line bill, or fill the blank from the record, before you rely on it.' NEXT: 'find the date of service in the record (the highlighted words may help) or ask the provider ...'. 1280x900:no_date_dob_sentence: the only date in the highlighted line is 'Patient DOB 03/04/1980'. step3.js:38 emits the same text for every reason. Screenshot T-209-r4-step3-no_date-1366x768.png: the source panel reads 'From the record  Record 4 · Saltmarrow General Hospital, UB-04 itemized bill'. r3 whats_right 1 said these lines 'never point at the highlighted words now'.\",\n   \"why_it_matters\": \"The hedge keeps it from being wrong, and 'or ask the provider' is a clear path. But on a no-date line the highlighted words can only hold a birth, posting or statement date. Those are the dates that must not go in the DOS blank. 'In the record' can send her back to the same bill instead of the visit note that actually dates the service.\",\n   \"fix\": \"Drop '(the highlighted words may help)' when sd.reason is no_date or non_service_date, or name the place: 'find the date of service in this provider's visit note (Step 2) or ask the provider for a dated line-by-line bill'.\",\n   \"acceptance_test\": \"E2E for no_date and non_service_date: confirm-next contains no 'highlighted' and names the visit note or Step 2.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"At 1366x768 the non_service_date card (the longest note) still clips the sentence's last clause, and the e2e layout test leaves that reason out\",\n   \"evidence\": \"T-209-r4-paralegal-summary.txt: '1366x768:non_service_date body 90/113 foot 184/200 auto ... next hit=False' (same for non_service_date_dob). Screenshot T-209-r4-step3-non_service_date-1366x768.png: the foot ends at '...Counting it adds the' and the next line is cut. test_t206.py:106 parametrizes the layout test over REASONS[0], REASONS[6], REASONS[4] (ambiguous_numeric, no_date, several_dates) only. At 1280x900 the same reason gives foot 230/238, while the sentence still passes the hit test. The brief's other check holds: figure and service-date line are inside the visible body and pass elementFromPoint in 22 of 22 runs at 1280x900 and 1366x768.\",\n   \"why_it_matters\": \"The cut clause tells her that counting the line puts the amount in the bill total. That is the consequence of the button she is about to press. Facts are not lost, and the clause is reachable by scrolling the foot.\",\n   \"fix\": \"Add non_service_date to the layout test and let the foot fit it at 1366x768 (for example, drop the body min-height from 90px to the figure plus date-line height, or shorten _WHY['non_service_date']).\",\n   \"acceptance_test\": \"test_t206.py layout test parametrized over all eight reasons at 1280x900 and 1366x768: foot scrollHeight <= clientHeight + 1, and figure and service-date pass elementFromPoint.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from r2/r3: no curated case reaches this card; every check of the wording uses injected backend output\",\n   \"evidence\": \"Handoff: 'Left: minor 7 (no curated doubtful-date case, qa/backend fixture)'. git show --stat 1b3c58a changes only review.js, step3.css, step3.js and test_t206.py. test_t206.py:57-60 injects sd through SD.confirm_note. My walk also injects (T-209-r4-paralegal-walk.py).\",\n   \"why_it_matters\": \"The demo never shows this card on a real record. The first real doubtful date will be the first time anyone reads this wording on a real bill.\",\n   \"fix\": \"Open a qa card for one curated bill line per branch: a labeled ambiguous DOS and an unlabeled ledger date.\",\n   \"acceptance_test\": \"Reach scan: at least one curated charge has a written-date reason and one has no_date, both from the real backend.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Outside the brief's viewports, at 1280x720 the sentence is clipped for every reason, and the control card (no confirm foot) already hides the date line\",\n   \"evidence\": \"T-209-r4-paralegal-summary.txt: every 1280x720 confirm run shows foot 136/160-200 and next hit=False; '1280x720:control_no_injection ... date in=False hit=False' (no confirm note, so not caused by 1b3c58a). 1440x900 and 1920x1080: all checks pass.\",\n   \"why_it_matters\": \"720-px-tall windows (laptop with browser chrome and a docked taskbar) are common, but the card's ask was 1280x900 and 1366x768.\",\n   \"fix\": \"Optional: a compact layout below 760 px height (the quote panel could shrink first).\",\n   \"acceptance_test\": \"Optional: the layout test at 1280x720 for one reason.\"}\n ],\n \"whats_right\": [\n  \"The amount and the date line with '(statement dated June 15, 2026)' stay on screen at 1280x900 and 1366x768 for every reason (22 of 22 runs, elementFromPoint at 4 points).\",\n  \"The sentence no longer tells her to fill the blank from the highlighted words on a doubtful date, and the round-3 'If you don't, it stays out' ambiguity is gone.\",\n  \"The note now reads 'The highlighted words label ...' and the button names match the card (Yes, count it / No, don't count it).\"\n ],\n \"questions_for_chris\": [\n  \"The binding D-071 wording (ORCHESTRATOR_DECISIONS.md:88 and :93) makes the note say 'confirm the date from the quote' even when the same note says the quoted date is impossible (Feb 30) or after the bill. May the orchestrator amend it per reason (T-202 owner) so that invalid and implausible lines say 'do not copy the highlighted date'?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-03T02:10:01.688Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-209-r4-paralegal-draft.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:05.202Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 1b3c58a:app/frontend/guided/step3.css | sed -n 20,34p | cat -n; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py artifacts/review-evidence/T-209-r4-paralegal-draft.md",
 "description": "Check CSS line range and validate draft JSON"
}
````

### User / tool · 2026-11-03T02:10:05.424Z

**tool result**
````
     1	.card-f .svc-next { margin: 6px 0 0; overflow-wrap: anywhere; }
     2	/* T-209 r3: the foot with the confirm note + next step is as tall as its text, but the card is a fixed height: the body keeps room for the amount and the date line (they are what she is confirming) and the foot gives way last */
     3	@media (min-width: 761px) {
     4	  .card:has(.svc-next) .card-b { flex: 1 1 0; min-height: 120px; }
     5	  .card-f:has(.svc-next) { height: auto; min-height: 0; max-height: none; flex: 0 1 auto; }
     6	  .card:has(.svc-next) .card-f { line-height: 1.3rem; font-size: .9375rem; }
     7	}
     8	@media (min-width: 761px) and (max-height: 820px) {
     9	  .card:has(.svc-next) .card-b { min-height: 90px; padding-top: 6px; padding-bottom: 4px; }
    10	  .card:has(.svc-next) .card-b .money { font-size: 2rem; line-height: 2.25rem; }
    11	  .card:has(.svc-next) .card-b .gap-top { margin-top: 6px; }
    12	  .card:has(.svc-next) .card-f { line-height: 1.25rem; font-size: .875rem; padding-top: 8px; padding-bottom: 8px; }
    13	  .card-f .svc-next { margin-top: 4px; }
    14	}
json blocks: 1
verdict: pass | severities: ['minor', 'minor', 'minor', 'minor', 'nit']
verdict rule expects: pass | matches: True
model: claude-opus-5-5 | card: T-209 | persona: paralegal-reviewer
all finding fields present
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:07.402Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cp artifacts/review-evidence/T-209-r4-paralegal-draft.md reviews/T-209-paralegal-r4.md && python3 tools/board.py validate reviews/T-209-paralegal-r4.md",
 "description": "Publish review and validate"
}
````

### User / tool · 2026-11-03T02:10:07.550Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:15.029Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t209-r4-patterns.md",
 "content": "---\nname: t209-r4-patterns\ndescription: T-209 r4 (1b3c58a) pass: one generic next-step sentence for all reasons; note's 'Confirm the date from the quote' is binding D-071 text (ORCH_DECISIONS:88,:93) so the clash is minor + question; non_service_date foot clips at 1366x768\nmetadata:\n  type: project\n---\n\nT-209 r4 (1b3c58a, final round): verdict pass, 4 minors + 1 nit, reviews/T-209-paralegal-r4.md.\n\n- Fix replaced per-reason branching with one sentence: \"find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank\". It no longer instructs a wrong date, so the r3 major is gone.\n- The backend note `_ASK_WRITTEN` (\"Confirm the date from the quote\") is binding decision wording (ORCHESTRATOR_DECISIONS.md:88, :93). I rated the note/sentence clash minor and sent a question to Chris. Before rating backend note text as a frontend-card major, grep ORCHESTRATOR_DECISIONS for the exact phrase. If a decision binds it, it is a question, not a defect.\n- New wording clashes: for ambiguous, the note says \"the record does not settle\" while the sentence says \"find ... in the record\". On no_date lines the sentence says \"highlighted words may help\".\n- Layout: amount and date line pass at 1280x900 and 1366x768 (22/22). The non_service_date note is the longest and still clips the foot at 1366x768 (184/200). The e2e layout test only covers 3 reasons. Always include the longest-note reason.\n- Reusable probe: artifacts/review-evidence/T-209-r4-paralegal-walk.py (5 viewports x 11 scenarios, 4-point elementFromPoint) + T-209-r4-paralegal-summary.py.\n\n**Why:** the brief asked how severe the note/sentence clash is. The answer depended on whether the note text was binding.\n**How to apply:** for any Step 3 note review, check whether the wording is binding before rating it, and run layout checks over every reason, not only a sample.\n\nRelated: [[t209-r3-patterns]], [[t209-confirm-sentence-patterns]]\n"
}
````

### User / tool · 2026-11-03T02:10:15.141Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t209-r4-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:16.521Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-209 confirm sentence]",
 "new_string": "- [T-209 r4 patterns](t209-r4-patterns.md) — 1b3c58a pass: generic sentence; note wording binding D-071 (question, not defect); longest note clips at 1366x768\n- [T-209 confirm sentence]"
}
````

### User / tool · 2026-11-03T02:10:16.628Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:19.434Z

T-209 r4 (1b3c58a) **passes** with no blockers or majors: the amount and date line stay visible at 1280x900 and 1366x768 for every reason. The note/sentence clash is minor because the note's "Confirm the date from the quote" is binding D-071 wording (asked as a question to Chris). Other minors: on no-date lines the sentence still says "highlighted words may help"; the longest-note reason (date not labeled as service) cuts off the last clause at 1366x768; and no curated case reaches this card. Review: /Users/arsis/zlayt-pm-project/reviews/T-209-paralegal-r4.md (my server PID 65212 on 7947 is stopped).
