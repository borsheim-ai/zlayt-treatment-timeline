# Subagent: Paralegal re-review: T-202 r2 (Paralegal re-review: T-202 r2)

Source: `agent-ab1b54b8e068f0519.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T00:19:59.780Z

Re-review T-202, round 2 (the D-071 amendment plus its clarification, all in memory/ORCHESTRATOR_DECISIONS.md), in /Users/arsis/zlayt-pm-project as the senior PI paralegal, starting from a fresh context. The fix commit is 986fc55; read reviews/T-202-paralegal.md (your round 1) and the card handoff.

Run a `git archive 986fc55` copy in demo mode on your own port, and stop your PID afterward.
- Re-run your own adversarial bill texts: posted-before-DOS, and a CMS-1500 with two service dates. Each must print the correct service date or the not-stated form; never a wrong date.
- Generate the sample, case_09, lib14 and lib10 letters.
- Judge whether the not-stated wording and the confirm note read well in a demand letter.

Step 3's display of the date is a separate frontend card; note what it shows, but don't grade it. Report any private value only as <redacted> with a count. Write reviews/T-202-paralegal-r2.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:02.914Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat personas/paralegal.md | head -c 200 >/dev/null; diff <(sed -n '1,400p' personas/paralegal.md) /dev/null | wc -l; cat .claude/agent-memory/paralegal-reviewer/t202-d071-service-date-patterns.md .claude/agent-memory/paralegal-reviewer/t200-undated-charge-label.md .claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md",
 "description": "Read persona length and relevant memory files"
}
````

### User / tool · 2026-11-03T00:20:03.032Z

**tool result**
````
      85
---
name: t202-d071-service-date-patterns
description: T-202 (f0921e4) fail: corpus letters right (Feb 2 / Sept 14 / June 9–12) but probes show Posted-first ledger prints posting date and CMS-1500 'X and Y' gives every line X; Step 3 shows statement date; eval accepts any record date
metadata:
  type: project
---

T-202 review (reviews/T-202-paralegal.md, f0921e4). Verdict: fail, with 2 blockers, 2 majors, 1 minor and 1 nit.

**Corpus result**
- The corpus letters are correct.
- All 25 cases list charges in service-date order.
- The parent diff (a44cfa7) shows only the 6 date changes.

**Blockers (from in-process probes)**
- A ledger table whose Posted column comes before DOS prints the posting date. The parse takes the first date in the row and ignores the header.
- A CMS-1500 with "dates of service 06/24 and 07/08" gives June 24 to every line. In amounts.py, `_record_period` keeps only the first date, because "and" is not a range join.

**Majors**
- Step 3 cards show the bill's record (statement) date bare ("UB-04 itemized bill · June 19, 2026"), and the case API has no service-date field.
- `letter_check.charge_date_violations` accepts any non-statement-led date in the record. The T3 mis-date passes with 0 violations.

**Minor**
- The quotes "FL47 total charges $4,920.00." and "charge $187.05." carry neither the service nor the date. This is pre-existing.

**Mechanics that worked**
- The demo UI turns the paste tile off. POST /api/cases with golden text returned 201, then open `/case/<tok>/records` (no btn-read click).
- probe_dates*.py call `store.charge_service_dates` with `export._date_range` directly.
- letters_dump.py and all_charge_lines.py dump every variant's letter.
- The parent dump needs its own script, because the parent letter_check has no "counted" variant or "records" key.

**Why:** next round, re-run probe_dates2.py and probe_eval_teeth.py on the fix commit first. Then check that Step 3 shows the letter's date string.
**How to apply:** scripts are in artifacts/review-evidence/T-202-paralegal/ (h.py port 7972). Related: [[t200-undated-charge-label]], [[reviewer-run-pitfalls-pass4]].
---
name: t200-undated-charge-label
description: T-200 (bd72d5b) pass: counted undated lib11 ledger lines print "(statement dated June 15, 2026; service date not stated)"; D-071 binds that form; minors = notes silent, no count-walk eval
metadata:
  type: project
---

T-200 review (reviews/T-200-paralegal.md, bd72d5b): pass, 2 minors + 1 nit. My T-181 r2 letter-date major is closed.
- D-071 (ORCHESTRATOR_DECISIONS.md:84) makes the T-200 wording binding for undated charges and moves dated charge lines (statement date vs service date: case_09, lib14, lib10) to another card. Grade that card on per-line service dates and period ranges.
- Open minors: the internal notes say nothing about counted charges that have no date of service (no "request dated itemized bill"). letter_check walks accept only, never D-064 count, so no eval produces the line.
- Mechanics: "demo mode" means a fixture backend; ZLAYT_MODE=local is still demo_mode true and gives /api/library. Reuse artifacts/review-evidence/T-200-paralegal/h.py + p01_lib11.py (port 7963, about 26 s end to end). The draft-then-cp flow with T-116-paralegal-r2-jsoncheck.py worked.

**Why:** next round on the D-071 card, check the dated lines against the D-071 rules above.
**How to apply:** related [[t181-r2-patterns]], [[reviewer-run-pitfalls-pass4]].
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
name: reviewer-hook-constraints
description: Bash hooks that block reviewer commands in this repo (board.py --help, python -c containing backticks) and the workarounds
metadata:
  type: reference
---

- board-guard: reviewers may run only `tools/board.py validate|show|list|status`. `--help` is rejected.
- git-guard fails to parse `python3 -c "..."` when the code contains escaped backticks. Use a quoted heredoc (`python3 - <<'EOF'`) and build the fence as '`'*3.
- Write access is limited to reviews/ and artifacts/review-evidence/ (plus this memory dir). Probe scripts go in artifacts/review-evidence/.
- T-118 (2026-11-02): the Write tool is refused for the session scratchpad (reviewer-write-guard), and board-guard refuses `mkdir` there. A Bash `git archive | tar -x` into the scratchpad still worked. Put scripts and output dirs under artifacts/review-evidence/ and run archive copies from the scratchpad. Run them with `.venv/bin/python -I` and a runner that puts the archive root first on sys.path.

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
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:04.059Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-03T00:20:04.069Z

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

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:05.043Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git rev-parse --short HEAD; git log --oneline -8; git show --stat 986fc55 | head -50; python3 tools/board.py show T-202 | tail -60",
 "description": "Check git state, fix commit, card"
}
````

### User / tool · 2026-11-03T00:20:05.230Z

**tool result**
````
6c9ab2a
6c9ab2a feat(release): T-199 snapshot shares the finalize rule set and switch; normalized final scan (D-070)
9611f02 fix(backend): T-201 e2e tests expect prepared wording for a prepared item (crosses into QA tests/e2e): internal-notes provenance line, wait for the server's sentence before reading the row, wait for the library list before the refused paste
986fc55 fix(backend): T-202 r2 D-071 amendment: a charge line prints a service date only when code is certain, else the not-stated form and a Step 3 confirm note
fa34fe9 fix(frontend): T-203 r2 hint stays beside a Saved note, position-neutral words + Show box, PT is not patient, lost wages, 375x667 edit-path tests
38ee0c3 fix(frontend): T-203 greyed Yes says why beside it (tick the box above), damages wording, Pt shorthand not underlined, 375x667 test
f0921e4 feat(backend): T-202 D-071 letter charge lines print the bill line's service date or period, not the statement date
a44cfa7 fix(qa): T-187 r4 README item 7 wording matches the normalized rule (no unicode/percent/entity decoding claimed)
bd72d5b fix(backend): T-200 counted undated ledger charge prints its statement date as such, never as a service date
commit 986fc551078a6ed6274cc9dd7a6a9efd0af357e3
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 18:13:48 2026 -0600

    fix(backend): T-202 r2 D-071 amendment: a charge line prints a service date only when code is certain, else the not-stated form and a Step 3 confirm note
    
    service_date.resolve ties one unambiguous date or complete period to the line by sentence, row+column header or the bill's one stated period; ambiguous numerics, two-digit years, year-less dates, several candidate dates and Posted/Statement columns print the T-200 form. amounts[].service_date in the case view (api.md). letter_check checks each printed date against that line's own quote with its own scanner. Adversarial bill-layout fixtures in the unit suite; the sort test can fail.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/export.py                           |  15 +-
 app/backend/present.py                          |   2 +
 app/backend/service_date.py                     | 329 +++++++++++++++++++++++
 app/backend/store.py                            |  41 ++-
 evals/letter_check.py                           | 191 ++++++++++++--
 memory/contracts/api.md                         |   4 +-
 tests/unit/test_t202_charge_service_dates.py    |   2 +-
 tests/unit/test_t202_r2_service_date_layouts.py | 336 ++++++++++++++++++++++++
 8 files changed, 875 insertions(+), 45 deletions(-)
---
id: "T-202"
title: "D-071: letter charge lines print the bill's service date or period, not the statement date (case_09, lib14, lib10)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T23:26:04Z"
updated_at: "2026-11-03T00:19:55Z"
claimed_by: "backend"
claimed_at: "2026-11-02T23:26:10Z"
rounds: 1
commits: ["f0921e4", "986fc55"]
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-202-paralegal.md", "at": "2026-11-02T23:48:12Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "fail", "file": "reviews/T-202-staff-engineer.md", "at": "2026-11-02T23:55:16Z"}
ac:
  - {"n": 1, "text": "per D-071; case_09/lib14/lib10 letters show the service date/period; goldens updated with a diff in the handoff; evals/letter_check.py asserts each dated charge line's date equals the service date in its quote, over all 25 cases incl. a count path; unit + guided e2e green from git archive", "done": true, "evidence": "r2 986fc55: tests/unit/test_t202_r2_service_date_layouts.py 48 cases (33 red on f0921e4 -> all pass); letter_check value 0 over 25 cases, mutants fail it (drop period end 16, record date 28, bare statement 20, record first date 6); unit + guided e2e from git archive 986fc55 (see handoff)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T23:26:10Z backend: claimed
- 2026-11-02T23:29:45Z orchestrator: Also cover T-200 minor: the letter_check count path must include a counted undated line (lib11).
- 2026-11-02T23:37:08Z backend: AC 1 checked: tests/unit/test_t202_charge_service_dates.py (13 pass); python -m evals.letter_check value 0 over 25 cases incl. count variant, mutants (record-date printing; bare statement date) fail it with 48 / 20 violations; git archive tree df2e300b60: unit 1456+1478+1353+1597 passed, guided e2e 128 passed
- 2026-11-02T23:37:08Z backend: moved in_progress -> in_review
- 2026-11-02T23:37:13Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer
- 2026-11-02T23:48:12Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-202-paralegal.md; round 1; findings:
    - [blocker] Ledger table with the Posted column before DOS: the letter prints the posting date as the date of service — fix: Read the row's date by its column: use the ledger header (billing.py already parses DOS vs Posted columns, api.md GET /billing 'dos' vs 'posted'). When a row has two dates and no header says which is the DOS, use the T-200 form, not a guess.
    - [blocker] CMS-1500 listing two dates of service ('06/24/2026 and 07/08/2026'): every charge line gets the first date — fix: Inherit the record's date only for a true period (a range join). For a list of discrete dates with no per-line date, print the T-200 form, or name the claim dates without assigning one: 'Wardlaw Orthopedics, CMS-1500 (claim dates of service June 24 and July 8, 2026; lin
    - [major] Step 3 labels each dated bill charge with the statement date, not the date the letter prints; the API carries no service date — fix: Expose the D-071 service date or period on each charge in the case view (backend: dos_iso/dos_end_iso, or the T-200 'not stated' state). Show it on the Step 3 card exactly as the letter will print it, with the statement date labelled as such: 'Service J
    - [major] letter_check's date check accepts any service date the record states, not the line's own, so the wrong-date class passes; AC wording ('equals the service date in its quote') is not what it checks — fix: Pin the per-line expected date in the goldens: case_09, lib14 and lib10 expected letters, plus the T2/T3 probe shapes as SYNTHETIC cases. Make the check tie the date to the line's row
    - [minor] Some charge quotes name neither the service nor the date the line now prints (pre-existing quote span, unchanged by T-202) — fix: Quote the whole bill line from its code or description through the figure ('Rev 0120 room and board semi-private ... FL47 total charges $4,920.00.'; 'A0425 ground mileage, loaded, 8.7 miles ... charge $187.05.').
- 2026-11-02T23:48:15Z orchestrator: assigned: backend
- 2026-11-02T23:48:15Z orchestrator: Round 2 queued: starts when the staff r1 review lands (fold both). Paralegal blockers: ledger with Posted column before DOS prints the posting date; CMS-1500 with two service dates puts the first on every line; Step 3 still shows the statement date; letter_check passes the CMS-1500 mis-date.
- 2026-11-02T23:55:16Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): fail — reviews/T-202-staff-engineer.md
- 2026-11-02T23:55:16Z orchestrator: Errata for reviews/T-202-staff-engineer.md: the 'two service dates' evidence is amounts.py:500 (non-row) and :493 (row), not :507.
- 2026-11-02T23:55:16Z orchestrator: Round 2 per the D-071 amendment (print a date only when certain; otherwise the not-stated form + Step 3 confirm note). Fold all paralegal and staff r1 blockers/majors; adversarial layout fixtures; independent per-line letter_check; Step 3 shows the same date as the letter (frontend may need a field: put it in the API and tell the orchestrator).
- 2026-11-02T23:55:32Z orchestrator: assigned: backend
- 2026-11-02T23:55:32Z backend: moved changes_requested -> in_progress
- 2026-11-03T00:00:59Z backend: r2 started: adversarial fixtures tests/unit/test_t202_r2_service_date_layouts.py written first, RED on f0921e4 code: 33 failed, 15 passed. Rule I will implement: print a date only when exactly one unambiguous date/complete period is tied to the line by header/row; ambiguous numeric resolved only when one reading is after the record's own date (a service cannot follow its statement) else not-stated.
- 2026-11-03T00:16:07Z backend: r2 committed 986fc55 (unit/e2e from git archive running). New: app/backend/service_date.py; fixtures tests/unit/test_t202_r2_service_date_layouts.py (33 red on f0921e4 -> 0); letter_check rewritten (own scanner); API field amounts[].service_date. Corpus letters byte-identical to f0921e4 (84 charge lines diffed).
- 2026-11-03T00:16:38Z backend: AC 1 checked: r2 986fc55: tests/unit/test_t202_r2_service_date_layouts.py 48 cases (33 red on f0921e4 -> all pass); letter_check value 0 over 25 cases, mutants fail it (drop period end 16, record date 28, bare statement 20, record first date 6); unit + guided e2e from git archive 986fc55 (see handoff)
- 2026-11-03T00:19:45Z backend: moved in_progress -> in_review
- 2026-11-03T00:19:55Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer

## Handoff
What changed (r2, 986fc55): new app/backend/service_date.py prints a charge date only when exactly one unambiguous date or complete period is tied to THAT line (its sentence; its row + column header; or the bill's one stated period for a coded line). Else the T-200 not-stated form + a Step 3 confirm note: ambiguous numerics (04/05/2026), two-digit years, year-less dates, impossible dates, several candidate dates (CMS-1500 '06/24 and 07/08', 'exam 03/27 and x-ray 03/28'), Posted/Statement columns, row with two dates and no DOS header, bill line with no date. Month-name periods keep their own year and end (June 9-12, 2024; June 28-July 2, 2026); hyphen-joined 06/28/2026-07/02/2026 prints whole. store.charge_service_date feeds BOTH the letter (dos_iso/dos_end_iso) and the case view; bill line the code cannot read now has no date (staff minor); sort test can fail. letter_check: charge_date_violations rewritten, checks each printed date against that line's own quote (+ the one period the bill states before it) with its own scanner, no production parser. | API/Step 3 (frontend): read amounts[].service_date on every charge (null for other kinds) = {state 'stated'|'not_stated', date_iso, end_iso, text, statement_date_iso, reason, confirm_note}. text is byte-for-byte what the letter prints after the provider ('June 9-12, 2026' or '(statement dated June 15, 2026; service date not stated)'); show confirm_note when not null; label the record date as the statement date. api.md updated. | Verified: fixtures tests/unit/test_t202_r2_service_date_layouts.py were RED first on f0921e4 (33 failed, 15 passed) and pass now (48). From git archive 986fc55: unit 5932 passed (1409+1611+1391+1521, 12 skipped), guided e2e 134 passed, letter_check value 0 over 25 cases. Corpus letters byte-identical to f0921e4 (84 charge lines diffed, case_09/lib14/lib10 unchanged). Mutants vs letter_check: drop period end 16 violations, record date 28, bare statement date 20, record's first date on a not-stated line 6 (all FAIL; the staff survivors M3/M6 now die); no-sort mutant fails 2 unit tests. | Left / ASSUMPTION for orchestrator: lib10 UB-04 '06/09/2026 to 06/12/2026' is ambiguous numerically; it stays 'June 9-12' only via one rule: a reading after the record's own date is impossible (Sept 6 > June 19 statement), or the other end of the period is unambiguous. Strike it (ref=None in service_date._certain) and lib10 prints the not-stated form. Not done: paralegal minor (quote span names neither service nor date) and the same-day ED-before-ambulance tie-break nit. Surprise: every not-stated corpus line is a D-064 counted-undated one, so a mutant that skips counted lines survives letter_check.
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:07.741Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"D-071\" memory/ORCHESTRATOR_DECISIONS.md | head; awk '/D-071/{f=1} f' memory/ORCHESTRATOR_DECISIONS.md | head -60; ls artifacts/review-evidence/T-202-paralegal/; sed -n '1,60p' reviews/T-202-paralegal.md",
 "description": "Read D-071, list prior probes, round 1 review"
}
````

### User / tool · 2026-11-03T00:20:07.843Z

**tool result**
````
84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
87:## D-071 amendment — when the service date is not certain, print none and ask the human
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.

## D-071 amendment — when the service date is not certain, print none and ask the human
T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.

## D-072 — The prompt log is built and privacy-reviewed once, last
Every review round adds new transcripts (including the reviewer's own), so a per-round clean prompt log cannot stay clean (T-187 r4: the reviewer's own session carries private stems). Binding: (1) QA fixes the rule gaps now (bare work-email domain, hostname stems without suffix, job-folder names; a 'term' entry never overrides the outside-name switch; path tails redacted); (2) the final prompt log is rebuilt once, after the last agent has finished (inside T-188), then one independent privacy sweep runs on that build and on the snapshot, and its own transcript is excluded from the published set (listed in the README as the one omitted file); (3) every reviewer brief from now on says: report private values only as <redacted> with a count, never quote them, not even partially.
- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
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
# T-202 (D-071) — paralegal review (Maria Delgado, senior PI litigation paralegal)

**Verdict: fail.** The rule hits two blockers on bill shapes I see every week. The corpus letters are now right.
- **case_09:** "billing statement, February 2, 2026: $275.00". The quote reads "Statement for visit of 2026-02-02".
- **lib14:** both ambulance lines print "September 14, 2026", from "Invoice for the run of 09/14/2026".
- **lib10:** all four UB-04 lines print "June 9–12, 2026", with an en dash, from "statement period 06/09/2026 to 06/12/2026".
- **sample:** unchanged.
- **All 25 cases:** charges are in service-date order. The T-200 form still covers the undated ledger lines (lib06, 09, 11, 12, 15).

An adjuster checking those lines against the bill pages would find nothing to attack.

**Blockers (probe text, live or paste path).** The per-line parse still prints a date the row does not tie to the charge:
- **Posting date as service date.** In a ledger table whose Posted column comes before DOS, the letter prints the posting date as the service date. This is the exact D-071 error.
- **First claim date on every line.** On a CMS-1500 that lists "dates of service 06/24/2026 and 07/08/2026", every line gets June 24. That includes the injection the chart dates July 8.

**Majors:**
- **Step 3 shows a different date from the letter.** Step 3, where I accept the charge, still labels it with the bare statement date ("UB-04 itemized bill · June 19, 2026"). The case API carries no service date, so the date the letter prints is never shown to me before export.
- **The eval cannot catch the wrong date.** letter_check accepts any service date the record states, not the line's own date. The CMS-1500 mis-date passes with 0 violations.

**Scope.**
- **Build:** `git archive f0921e4` extracted to the session scratchpad (t202/).
- **Server:** fixture backend FIXTURE_SET=curated. Demo mode (health: demo_mode true) with ZLAYT_MODE=local for /api/library, on http://127.0.0.1:7972.
- **Shutdown:** listener PID 82425 was killed. `lsof` returned exit 1 and `curl` returned 000.
- **Parent comparison:** a44cfa7, run in-process from its own archive (t202parent/).
- **Evidence:** artifacts/review-evidence/T-202-paralegal/.

**Deterministic checks first (from the f0921e4 archive):**
- `pytest tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py`: "19 passed in 5.78s" (pytest-t202.out).
- `python -m evals.letter_check`: `{"value": 0, "cases": 25, ...}` (letter_check.out).

```json
{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "commit f0921e4 (git archive extracted to session scratchpad t202/), parent a44cfa7 for the before/after diff (t202parent/). Demo mode: fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, http://127.0.0.1:7972 (health demo_mode true); listener PID 82425 stopped (lsof exit 1, curl 000). Cases: sample (load-sample tile), case_09 (POST /api/cases with the golden text because the demo UI turns the paste tile off, then opened in the UI), case_lib14 and case_lib10 (library tile). Evidence dir artifacts/review-evidence/T-202-paralegal/.",
 "exercised": [
  "Read personas/paralegal.md, D-071 (memory/ORCHESTRATOR_DECISIONS.md:84), board.py show T-202 (AC, notes, handoff with letter diffs), git show f0921e4 (amounts.py, export.py, store.py, evals/letter_check.py, tests)",
  "From the archive: pytest test_t202 + test_t200 '19 passed in 5.78s' (pytest-t202.out); python -m evals.letter_check value 0 over 25 cases (letter_check.out)",
  "Playwright on the running archive app (h.py + p01_cases.py): sample, case_09, lib14, lib10 driven keyboard-first through Steps 1-4, every Step 3 bill card logged and screenshotted, letter + notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); scripted times 15.5 s / 7.2 s / 13.1 s / 19.0 s (p01.out, p02.out)",
  "Read every charge line of the four letters against the bill page in the record (service date vs statement date, UB-04 period, order)",
  "Before/after: same letters generated in-process from a44cfa7 and f0921e4; diff shows only the six date changes the handoff lists (parent-vs-f0921e4.diff)",
  "All 25 letter_check cases, counted variant: every BILLED CHARGES line with the record it quotes (all_charge_lines.out), checked by hand for date and order",
  "GET /api/cases/{token} for the lib10, lib14 and case_09 runs: charge amounts carry no service-date field (api-amount-fields.out)",
  "Probes of the shipped date path (store.charge_service_dates -> export._date_range) on SYNTHETIC bill shapes: probe_dates.out (10 shapes), probe_dates2.out (ledger tables, CMS-1500 with two dates), probe_eval_teeth.out (letter_check on the wrong dates)"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 3, "letter_dates_correct_on_corpus": 5, "adjuster_credibility": 3},
 "findings": [
  {"severity": "blocker",
   "title": "Ledger table with the Posted column before DOS: the letter prints the posting date as the date of service",
   "evidence": "artifacts/review-evidence/T-202-paralegal/probe_dates2.out, probe T2. Record 'Posted      DOS         CPT ...' / '06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00' gives 'letter date -> June 11, 2026'; the next row (posted 06/18, DOS 06/17) gives 'June 18, 2026'. With DOS first (T1) it prints June 10 / June 17. The parse takes the first date in the row (amounts.py charge_basis) and ignores the column header.",
   "why_it_matters": "This is the error D-071 exists to stop: a billing-side date printed in the date-of-service slot. The adjuster's first move is to match the letter date to the bill and the chart note, and here neither matches. The paralegal never sees this date before export (see the Step 3 major), so she cannot catch it. Not in the 25-case corpus or the demo; reachable on any pasted ledger in live mode.",
   "fix": "Read the row's date by its column: use the ledger header (billing.py already parses DOS vs Posted columns, api.md GET /billing 'dos' vs 'posted'). When a row has two dates and no header says which is the DOS, use the T-200 form, not a guess.",
   "acceptance_test": "Unit test on the T2 text: the $70.00 line prints 'June 10, 2026' and the $95.00 line 'June 17, 2026'. Same rows without a header give the '(statement dated ...; service date not stated)' form. Add a SYNTHETIC library or golden case with a Posted-first ledger to the letter_check corpus."},
  {"severity": "blocker",
   "title": "CMS-1500 listing two dates of service ('06/24/2026 and 07/08/2026'): every charge line gets the first date",
   "evidence": "artifacts/review-evidence/T-202-paralegal/probe_dates.out P2 and probe_dates2.out T3: 'CMS-1500 for dates of service 06/24/2026 and 07/08/2026 ... CPT 99204, $185.00 ...; CPT 20610, $210.00' -> both '$185.00 ... letter date -> June 24, 2026' and '$210.00 ... letter date -> June 24, 2026'. amounts.py:435-445 _record_period returns the first matched date; 'and' is not a range join, so no end date is kept. This is the shape of lib10 record 8 (Wardlaw Orthopedics CMS-1500), where the chart dates the injection (CPT 20610) 'July 8' (record 7: 'Injection performed').",
   "why_it_matters": "The letter ties the injection charge to June 24, a visit where no injection was done. The record does not say which line is which date, so the pairing is invented. An adjuster who lines the specials up against the chart finds a charge on a day with no matching service and uses it to question the whole bill set.",
   "fix": "Inherit the record's date only for a true period (a range join). For a list of discrete dates with no per-line date, print the T-200 form, or name the claim dates without assigning one: 'Wardlaw Orthopedics, CMS-1500 (claim dates of service June 24 and July 8, 2026; line date not stated)'. D-071 says that when no service date is stated the T-200 form applies.",
   "acceptance_test": "Unit test on the T3 text: neither charge line prints a bare single date. Both carry the not-stated form, or the two-date claim form above. letter_check, run on a corpus case of this shape, reports a violation when a single claim date is printed."},
  {"severity": "major",
   "title": "Step 3 labels each dated bill charge with the statement date, not the date the letter prints; the API carries no service date",
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:09.457Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat artifacts/review-evidence/T-202-paralegal/h.py; cat artifacts/review-evidence/T-202-paralegal/probe_dates2.py; cat artifacts/review-evidence/T-202-paralegal/probe_dates.py | head -80",
 "description": "Read prior helper and probe scripts"
}
````

### User / tool · 2026-11-03T00:20:09.551Z

**tool result**
````
"""T-200 paralegal review helper (copied from T-181 r2): persistent Chromium profile on the archive app (bd72d5b, demo/fixture, local mode, port 7963).

Usage: .venv/bin/python -I artifacts/review-evidence/T-200-paralegal/h.py <step-script.py>
The step script gets `pg` (page), `shot(name)`, `dump(label)`, `log(...)`, `BASE`, `OUT` in its globals.
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7972")  # T-202: f0921e4 archive, port 7972
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
"""T-202 paralegal probe 2: table-form ledgers and a CMS-1500 with two dates of service. For each charge figure: the date the LETTER would print
(store.charge_service_dates -> export._date_range) next to the date of service the app's own billing listing (billing.analyze, GET /billing) reads for that line.
SYNTHETIC probe text only. f0921e4 archive.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/probe_dates2.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
from app.backend import amounts as AM, billing, export, store  # noqa: E402

PROBES = [
    ("T1 ledger table: DOS + posted columns", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "Itemized ledger\nDOS         Posted      CPT    Description            Charges    Balance\n"
     "06/10/2026  06/11/2026  97140  Manual therapy x1      $70.00     $70.00\n"
     "06/17/2026  06/18/2026  97110  Therapeutic exercise   $95.00     $165.00"),
    ("T2 ledger table: posted column first", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "Itemized ledger\nPosted      DOS         CPT    Description            Charges    Balance\n"
     "06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00     $70.00\n"
     "06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00     $165.00"),
    ("T3 CMS-1500, two dates of service joined by 'and', $ figures", "Wardlaw Orthopedics, CMS-1500", "2026-07-14",
     "CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, $185.00, 1 unit; CPT 20610, $210.00, 1 unit. Item 28 TOTAL CHARGE $395.00. Item 29 AMOUNT PAID $0.00."),
]
for label, src, rd, ex in PROBES:
    print(f"== {label}  (record date {rd})")
    print("   " + ex.replace("\n", "\n   "))
    rec = {"n": 1, "source": src, "date_iso": rd, "excerpt": ex, "text": ex}
    try:
        an = billing.analyze([rec])
        bl = [(l.get("billed") or l.get("figure") or {}).get("usd") for l in an.get("lines", [])]
        bdos = {((l.get("billed") or {}).get("usd")): (l.get("dos_iso"), l.get("class")) for l in an.get("lines", [])}
    except Exception as e:  # report, do not hide
        bdos, bl = {}, f"billing.analyze error: {e!r}"
    print(f"   billing listing lines: {bl}")
    for a in AM.find_amounts(ex):
        if a.get("cents") is None:
            continue
        b = AM.charge_basis(ex, a, src, rd)
        first, last = store.charge_service_dates({"excerpt": ex, "value_cents": a["cents"]}, {"source": src, "date_iso": rd}, a["start"])
        shown = export._date_range(first, last) if first else "(T-200 form)"
        usd = "$" + f"{a['cents'] // 100:,}.{a['cents'] % 100:02d}"
        print(f"   {a['raw']:>9} ok={b['ok']!s:5} letter date -> {shown:28} | billing listing dos/class -> {bdos.get(usd)}")
"""T-202 paralegal probe: what date would the letter print for each charge figure on bill shapes a paralegal sees?
Calls the shipped code path (store.charge_service_dates -> export._date_range) on the f0921e4 archive. SYNTHETIC probe text only.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/probe_dates.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
from app.backend import amounts as AM, export, store  # noqa: E402

PROBES = [
    ("P1 two-row ledger, own dates", "Hobbleton Family Clinic, itemized ledger", "2026-03-15",
     "Statement date 03/15/2026. 02/02/2026 office visit charge $275.00. 02/16/2026 x-ray charge $150.00. Balance due $425.00."),
    ("P2 CMS-1500 two DOS joined by 'and'", "Wardlaw Orthopedics, CMS-1500", "2026-07-14",
     "CMS-1500 for dates of service 06/24/2026 and 07/08/2026. CPT 99204 charge $185.00. CPT 20610 charge $210.00."),
    ("P3 invoice date stated before run date", "Tarnwick Fire-Rescue, ambulance invoice", "2026-11-12",
     "Invoice date 11/12/2026. Run of 09/14/2026. A0427 ALS emergency transport, charge $1,380.00."),
    ("P4 UB-04 period across months", "Saltmarrow General Hospital, UB-04 itemized bill", "2026-07-10",
     "UB-04 statement period 06/28/2026 to 07/02/2026. Rev 0120 room and board, FL47 total charges $4,920.00."),
    ("P5 UB-04 period with 'through'", "Saltmarrow General Hospital, UB-04 itemized bill", "2026-06-19",
     "UB-04 statement period 06/09/2026 through 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00."),
    ("P6 UB-04 period with hyphen", "Saltmarrow General Hospital, UB-04 itemized bill", "2026-06-19",
     "UB-04 statement period 06/09/2026 - 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00."),
    ("P7 statement + DOS label same sentence", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Statement date 03/01/2026, date of service 02/02/2026: office visit charge $275.00."),
    ("P8 ledger row DOS then posted", "Fennimoor Spine Clinic, itemized ledger", "2026-06-15",
     "06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00. 06/12/26 06/13/26 97110 Therapeutic exercise charge $95.00."),
    ("P9 statement period then a separately dated line", "Saltmarrow General Hospital, UB-04 itemized bill", "2026-06-19",
     "UB-04 statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, service date 06/09/2026, FL47 total charges $2,105.00."),
    ("P10 'from X to Y' dates of service", "Capital PT, billing statement", "2026-03-20",
     "Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 therapeutic exercise, 9 units, charge $1,665.00."),
]
for label, src, rd, ex in PROBES:
    print(f"== {label}  (record date {rd})\n   {ex}")
    for a in AM.find_amounts(ex):
        if a.get("cents") is None:
            continue
        b = AM.charge_basis(ex, a, src, rd)
        first, last = store.charge_service_dates({"excerpt": ex, "value_cents": a["cents"]}, {"source": src, "date_iso": rd}, a["start"])
        shown = export._date_range(first, last) if first else "(T-200 form: statement dated / service date not stated)"
        print(f"   {a['raw']:>10}  ok={b['ok']} reason={b['reason']!r}  letter date -> {shown}")
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:11.827Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 986fc55 -- app/backend/store.py app/backend/export.py app/backend/present.py memory/contracts/api.md",
 "description": "Show store/export/api diffs of fix commit"
}
````

### User / tool · 2026-11-03T00:20:11.921Z

**tool result**
````
commit 986fc551078a6ed6274cc9dd7a6a9efd0af357e3
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 18:13:48 2026 -0600

    fix(backend): T-202 r2 D-071 amendment: a charge line prints a service date only when code is certain, else the not-stated form and a Step 3 confirm note
    
    service_date.resolve ties one unambiguous date or complete period to the line by sentence, row+column header or the bill's one stated period; ambiguous numerics, two-digit years, year-less dates, several candidate dates and Posted/Statement columns print the T-200 form. amounts[].service_date in the case view (api.md). letter_check checks each printed date against that line's own quote with its own scanner. Adversarial bill-layout fixtures in the unit suite; the sort test can fail.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/export.py b/app/backend/export.py
index 0f647e0..3d1c61e 100644
--- a/app/backend/export.py
+++ b/app/backend/export.py
@@ -19,7 +19,7 @@ import os
 import re
 from datetime import date
 
-from app.backend import amounts, charge_text, language, money
+from app.backend import amounts, charge_text, language, money, service_date
 
 LETTER_TITLE = "TREATMENT CHRONOLOGY"
 CHARGES_TITLE = "BILLED CHARGES"
@@ -71,15 +71,8 @@ def _long_date(iso):
 
 
 def _date_range(first, last=None):
-    """'June 9, 2026' for one day; a period as a range: 'June 9\u201312, 2026', 'June 28\u2013July 2, 2026', 'December 30, 2026\u2013January 2, 2027' (D-071)."""
-    if not last or last == first:
-        return _long_date(first)
-    a, b = date.fromisoformat(first), date.fromisoformat(last)
-    if (a.year, a.month) == (b.year, b.month):
-        return f"{a.strftime('%B')} {a.day}\u2013{b.day}, {a.year}"
-    if a.year == b.year:
-        return f"{a.strftime('%B')} {a.day}\u2013{b.strftime('%B')} {b.day}, {a.year}"
-    return f"{_long_date(first)}\u2013{_long_date(last)}"
+    """'June 9, 2026' for one day; a period as a range: 'June 9\u201312, 2026' (D-071). One implementation, shared with the case view (service_date.display)."""
+    return service_date.display(first, last)
 
 
 def _money(cents):
@@ -231,7 +224,7 @@ class _View:
         if a["dos_iso"]:
             return f"{src}, {_date_range(a['dos_iso'], a.get('dos_end_iso'))}"
         rd = self.rec_date(n)
-        return f"{src} (statement dated {_long_date(rd)}; service date not stated)" if rd else f"{src} (service date not stated)"
+        return f"{src} {service_date.not_stated_text(rd)}"
 
     def cite(self, n):
         return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"
diff --git a/app/backend/present.py b/app/backend/present.py
index 09ad1bf..aea2469 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -139,6 +139,7 @@ def amount_view(row, recs, records=None, pool=None, prep=False):
     cf = count_flag_for(row, records, nc, pool)
     counted = bool((row.get("ladder") or {}).get("counted"))
     c = _common(row, prep)
+    srec = next((r for r in records or [] if r["id"] == (row["record_ids"] or [None])[0]), None)
     if counted and row["kind"] == "charge":      # D-064: counted by the paralegal with a named confirm; no AI said it was a charge
         c["why"] = ("You counted this line as a separate charge and confirmed it by name. The code found the figure in the record; no second check was asked about it." if prep else
                     "You counted this line as a separate charge and confirmed it by name. The code found the figure in the record; no AI check was asked about it.")
@@ -148,6 +149,7 @@ def amount_view(row, recs, records=None, pool=None, prep=False):
             "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
             "duplicate_note": row["duplicate_note"], "accept_effect": accept_effect(row), "judge_required_for_export": row["kind"] != "rate" and not counted,
             "not_counted_reason": nc["reason"], "countable": nc["countable"],
+            "service_date": store.charge_service_date(row, srec, store.amount_pos(row, srec)) if row["kind"] == "charge" else None,      # D-071: what the letter prints for this charge's date
             "count_confirm": {k: cf.get(k) for k in ("flag", "name", "message", "confirm_with", "of")} if cf else None}
 
 
diff --git a/app/backend/store.py b/app/backend/store.py
index c869fa0..bac2c38 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -115,17 +115,38 @@ def amount_pos(item: dict, rec):
     return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None
 
 
+def charge_service_date(item: dict, rec, pos) -> dict:
+    """D-071 (extends T-200, amended in T-202 r2): what a charge line prints as its date, and why, for the letter AND the case view (Step 3 shows exactly this).
+    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or '(statement dated June 15, 2026; service date
+    not stated)'), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
+    A date is stated only when code is certain (service_date.resolve): the bill line's own single date or complete period, tied to the line by its sentence, its row and column
+    header, or the one period its bill states. The record's date of a ledger, invoice or UB-04 is the statement's, never a fallback: a bill line the code cannot read has no
+    service date. A dated encounter record's (visit note, imaging report) date is the visit. A charge the paralegal counted for a missing date of service (D-064) is
+    not stated, with no note (she counted it knowing). Code only."""
+    from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
+    rd = (rec or {}).get("date_iso")
+    bill = AM.billing_document((rec or {}).get("source"), item.get("excerpt") or "")
+    counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
+    if counted_undated:
+        r = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""}
+    elif rec is None or pos is None or not item.get("excerpt"):
+        r = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""} if bill else (
+            {"state": "stated", "first": rd, "last": None, "reason": None, "raw": ""} if rd else {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""})
+    else:
+        r = SD.resolve(item["excerpt"], pos, rec.get("source"), rd)
+    stated = r["state"] == "stated"
+    note = None
+    if not stated and not counted_undated:
+        note = SD.confirm_note(r["reason"], r["raw"])
+    return {"state": r["state"], "date_iso": r["first"], "end_iso": r["last"] if stated else None,
+            "text": SD.display(r["first"], r["last"]) if stated else SD.not_stated_text(rd),
+            "statement_date_iso": rd, "reason": r["reason"], "confirm_note": note}
+
+
 def charge_service_dates(item: dict, rec, pos) -> tuple:
-    """D-071 (extends T-200): (first, last) ISO date of service the charge's OWN bill line states, `last` None for a single day; (None, None) when the line states none. The
-    record's date of a ledger, invoice or UB-04 is the statement's, never a service date, so it is not the fallback for a billing document. A dated encounter record's date is
-    the visit. A charge the paralegal counted for a missing date of service (D-064) is (None, None). Code only: amounts.charge_basis reads the line.
-    When the line cannot be read: the record's date, unless she counted it for the missing date."""
-    from app.backend import amounts as AM          # lazy: keep the import graph as it was
-    if rec is None or pos is None or not item.get("excerpt"):
-        counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
-        return (None, None) if counted_undated else ((rec or {}).get("date_iso"), None)
-    b = AM.charge_basis(item["excerpt"], {"start": pos, "cents": item.get("value_cents")}, rec.get("source"), rec.get("date_iso"))
-    return b.get("dos"), (b.get("dos_end") if b.get("dos") else None)
+    """(first, last) ISO date of service the letter prints for a charge (`last` None for a single day), (None, None) when it prints none (see charge_service_date)."""
+    d = charge_service_date(item, rec, pos)
+    return d["date_iso"], d["end_iso"]
 
 
 def export_case(conn, case_id: str, blockers: bool = True) -> dict:
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index dda5a0d..4e89328 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -188,7 +188,7 @@ Read once, then patch local state from review responses. `entries` are **chronol
       "state": "needs_review", "reasons": ["AMOUNT_RATE_NOT_TOTALED"],
       "why": "This is a per-visit rate; the records never say how many visits were billed, so it is not totaled.",
       "review_status": "pending", "edited": null, "duplicate_note": null, "flag": null, "confirm_required": false, "accept_effect": "acknowledge", "judge_required_for_export": false,
-      "not_counted_reason": "This figure is a rate, not a charge, so it is not added to the total.", "countable": false, "count_confirm": null,
+      "not_counted_reason": "This figure is a rate, not a charge, so it is not added to the total.", "countable": false, "count_confirm": null, "service_date": null,
       "ladder": {"item_id": "a3", "backend": "fixture", "generator": null,
         "code_checks": {"amount_in_text": true, "classified_by": "rule:per_unit", "injection_tag": false, "highlight_found": true},
         "judge": {"model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": "c33", "verdict": "agrees"},
@@ -571,7 +571,7 @@ Built by code from items with `review_status` in (`accepted`, `edited`) only (AD
   "warnings": []
 }
 ```
-Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges accepted from these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte; **no dollar amount appears in `letter_text` outside the BILLED CHARGES section (T-139)**: an entry whose summary or quote states an amount is never written into the treatment section, whatever its review status (see "Dollar amounts in entries"), a charge's `Source` line quotes only the clause that holds its own figure when the sentence also states another one (a rate, a balance, another line item), and a dismissed charge is never listed under BILLS TO REQUEST. Rates, estimates, unclear and dismissed amounts appear only in `internal_notes_text`. **T-200 + D-071 (a charge line's date is its date of service):** the line before a charge's quote prints the service date the bill line itself states (`<provider>, <source label>, March 27, 2026: $250.00`), never the record's date, which for a ledger, invoice or UB-04 is the statement's. A service period prints as a range (`June 9\u201312, 2026`, `June 28\u2013July 2, 2026`). A charge whose own line states none (e.g. a ledger line counted through D-064 "Count this charge") reads `<provider>, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00` (`(service date not stated)` when the record has no date either). A dated encounter record (visit note, imaging report) keeps the visit date. Charges are listed in service-date order. The export case dict carries `dos_iso` / `dos_end_iso` on each charge (`store.charge_service_dates`, code reading the line with `amounts.charge_basis`); a hand-built case without the key keeps the old `<provider>, <record date>` line. `evals/letter_check.py` asserts every dated charge line's date is a date its record states.
+Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges accepted from these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte; **no dollar amount appears in `letter_text` outside the BILLED CHARGES section (T-139)**: an entry whose summary or quote states an amount is never written into the treatment section, whatever its review status (see "Dollar amounts in entries"), a charge's `Source` line quotes only the clause that holds its own figure when the sentence also states another one (a rate, a balance, another line item), and a dismissed charge is never listed under BILLS TO REQUEST. Rates, estimates, unclear and dismissed amounts appear only in `internal_notes_text`. **T-200 + D-071 (+ amendment, T-202 r2): a charge line prints a date of service only when code is certain.** The line before a charge's quote prints the service date the bill line itself states (`<provider>, <source label>, March 27, 2026: $250.00`), never the record's date, which for a ledger, invoice or UB-04 is the statement's. A service period prints as a range (`June 9\u201312, 2026`, `June 28\u2013July 2, 2026`, its own stated year). Code (`app/backend/service_date.py`) prints a date only when exactly ONE unambiguous service date, or one complete period, is tied to THAT line: by its own sentence, by its table row and the column heading over the date (a Posted, Statement or Billed column is never the date of service; a row with two dates and no heading that names the service date has none), or, for a coded line (CPT, HCPCS, revenue code) with no date of its own, by the one period the bill states for its services ("statement period 06/09/2026 to 06/12/2026", "the run of 09/14/2026", "dates of service ..."). Everything else prints the not-stated form `<provider>, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00` (`(service date not stated)` when the record has no date either): a numeric date readable two ways (`04/05/2026`; one reading is dropped only when it falls after the record's own date, or when the other end of the same period is unambiguous), a two-digit year, a date with no year (the statement year is never borrowed), a date not on the calendar, a period whose end is missing or before its start, several candidate dates for the line (a CMS-1500 "dates of service 06/24/2026 and 07/08/2026"; "exam 03/27/2026 and x-ray 03/28/2026 charge $250.00"), a bill line with no date at all, and a ledger line counted through D-064 "Count this charge". A dated encounter record (visit note, imaging report) keeps the visit date. Charges are listed in service-date order (a charge with no stated date sorts by its statement date). The export case dict carries `dos_iso` / `dos_end_iso` on each charge (`store.charge_service_dates`); a hand-built case without the key keeps the old `<provider>, <record date>` line. `evals/letter_check.py` checks every charge line's printed date against THAT line's own quote (plus, when the quote has no date, the one period the bill states before it) with its own scanner that shares no code with the production parser. **Case view (Step 3):** every charge in `amounts[]` (case view, review responses, item view) carries `service_date` (`null` for any other kind), the same value the letter prints: `{"state": "stated"|"not_stated", "date_iso": "2026-06-09"|null, "end_iso": "2026-06-12"|null, "text": "June 9\u201312, 2026" | "(statement dated June 15, 2026; service date not stated)", "statement_date_iso": "2026-06-19"|null (the record's date; for a bill it is the statement's), "reason": null | "ambiguous_numeric" | "two_digit_year" | "no_year" | "invalid" | "several_dates" | "non_service_date" | "no_date", "confirm_note": null | "<why the date is not certain>. The letter prints no service date for this line. Confirm the date from the quote before you rely on it."}`. A stated charge has `reason` and `confirm_note` null; show `text` as the charge's date and label the record's own date as the statement date (`statement_date_iso`). A not-stated charge shows `text` and the `confirm_note` (null only for a charge she counted through D-064, who already knows the line has no date). `text` is byte-for-byte the string after the provider in the letter line (`<provider>, <text>: $X` for a stated date; `<provider> <text>: $X` for not stated).
 
 ## GET /api/cases/{token}/audit
 JSON for this case only. **Public/demo (default): metadata only**: no prompt, response, record or edit text. With `ZLAYT_MODE=local` the same call also returns the full prompts and responses and the before/after of each human event (T-040, T-051 privacy check).
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:12.463Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 986fc55:app/backend/service_date.py",
 "description": "Read new service_date module"
}
````

### User / tool · 2026-11-03T00:20:12.552Z

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
        self.fixed = _iso(int(m.group(3)), _mon(m.group(1)), int(m.group(2)))

    def _dmy(self, s):
        m = re.match(rf"(\d{{1,2}}){_ORD}[\s-]+(?:of\s+)?({_MON})\.?[\s-]*,?\s*(\d{{4}})$", s, re.IGNORECASE)
        self.fixed = _iso(int(m.group(3)), _mon(m.group(2)), int(m.group(1)))

    def _md(self, s):
        self.flaw = "no_year"

    def _mper(self, s):
        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}\s*[-{_DASH}]\s*(?:({_MON})\.?\s+)?(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}}))?$", s, re.IGNORECASE)
        if not m.group(5):
            self.flaw = "no_year"
            return
        y, m1 = int(m.group(5)), _mon(m.group(1))
        a, b = _iso(y, m1, int(m.group(2))), _iso(y, _mon(m.group(3)) if m.group(3) else m1, int(m.group(4)))
        if a and b and b > a:
            self.first, self.last = a, b
        else:
            self.flaw = "invalid"


def _mon(name):
    from app.backend import dates
    return dates.MONTHS[name.lower()[:3]]


class _Unit:
    """One candidate: a single date or a period (two tokens joined by a range word, or a month-name period)."""
    def __init__(self, toks):
        self.toks = toks
        self.start, self.end = toks[0].start, toks[-1].end

    def raw(self, text):
        return text[self.start:self.end]


def _units(text: str) -> list:
    toks = [_Tok(m) for m in _TOK.finditer(text)]
    out, k = [], 0
    while k < len(toks):
        t = toks[k]
        if k + 1 < len(toks) and t.kind != "mper" and toks[k + 1].kind != "mper" and _JOIN.match(text[t.end:toks[k + 1].start]):
            out.append(_Unit([t, toks[k + 1]]))
            k += 2
        else:
            out.append(_Unit([t]))
            k += 1
    return out


def _certain(unit: _Unit, ref):
    """('ok', first, last or None) or ('bad', reason): the one reading of a unit, or why it has none."""
    for t in unit.toks:
        if t.flaw:
            return "bad", t.flaw
    if len(unit.toks) == 1 and unit.toks[0].first:
        return "ok", unit.toks[0].first, unit.toks[0].last
    determined = {t.order for t in unit.toks if t.order}
    amb = [t for t in unit.toks if t.ambiguous]
    if len(determined) > 1:
        return "bad", "ambiguous_numeric"
    if determined:
        order = next(iter(determined))
    elif amb:
        feasible = [o for o in ("MD", "DM") if not ref or all(t.ambiguous[o] <= ref for t in amb)]          # a service is not after the statement that bills it
        if len(feasible) != 1:
            return "bad", "ambiguous_numeric"
        order = feasible[0]
    else:
        order = None
    isos = [t.ambiguous[order] if t.ambiguous else t.fixed for t in unit.toks]
    if len(isos) == 2 and isos[1] <= isos[0]:
        return "bad", "invalid"
    return "ok", isos[0], (isos[1] if len(isos) == 2 else None)


def _header_cells(excerpt: str, row_ls: int):
    """[(start column, text)] of the table heading above the row: the nearest line above with no digits (data rows in between are skipped), up to a blank line."""
    for line in reversed(excerpt[:max(row_ls - 1, 0)].split("\n")[-40:]):
        if not line.strip():
            return None
        if re.search(r"\d", line):
            continue
        cells = [(m.start(), m.group(0)) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]
        return cells if len(cells) >= 2 else None
    return None


def _column_head(excerpt: str, row_ls: int, row_cells: list, tok_abs: int) -> str:
    heads = _header_cells(excerpt, row_ls)
    if not heads:
        return ""
    col = tok_abs - row_ls
    if len(heads) == len(row_cells):
        idx = next((i for i, (a, b) in enumerate(row_cells) if a <= col < b), None)
        if idx is not None:
            return heads[idx][1]
    return min(heads, key=lambda h: abs(h[0] - col))[1]


def _lead_ok(text: str, unit: _Unit, tail: bool = False) -> bool:
    lead = text[max(0, unit.start - 40):unit.start]
    if _NON_SVC_LEAD.search(lead):
        return False
    return bool(AM._DATE_LEAD.search(lead)) if tail else True


def _period_units(prefix: str) -> list:
    """The dates the bill states for its services: units led by 'statement period', 'dates of service', 'the run of' ... and the units listed after them ('A and B')."""
    us = _units(prefix)
    out = []
    for k, u in enumerate(us):
        if AM._PERIOD_PHRASE.search(prefix[max(0, u.start - 40):u.start]) and not _NON_SVC_LEAD.search(prefix[max(0, u.start - 40):u.start]):
            out.append(u)
            j = k
            while j + 1 < len(us) and _LIST.match(prefix[us[j].end:us[j + 1].start]):
                out.append(us[j + 1])
                j += 1
    return out


def _decide(units, text, ref):
    """('ok', first, last) for one certain unit (or several that read the same); ('bad', reason, raw) otherwise."""
    reads = [(u, _certain(u, ref)) for u in units]
    if len(units) > 1:
        same = {(r[1], r[2]) for _, r in reads if r[0] == "ok"}
        if len(same) == 1 and all(r[0] == "ok" for _, r in reads):
            return "ok", *next(iter(same))
        return "bad", "several_dates", ", ".join(u.raw(text) for u in units)
    u, r = reads[0]
    return ("ok", r[1], r[2]) if r[0] == "ok" else ("bad", r[1], u.raw(text))


def _apply(out: dict, res) -> dict:
    if res[0] == "ok":
        out.update(state="stated", first=res[1], last=res[2], reason=None, raw="")
    else:
        out.update(reason=res[1], raw=res[2])
    return out


def resolve(excerpt: str, start: int, source, date_iso) -> dict:
    """{state: 'stated'|'not_stated', first, last (None for one day), reason (None when stated, else one of REASONS), raw (the date text the reason is about)} for the figure at
    `start` of `excerpt`, in a record with header `source` and date `date_iso`. See the module doc for the rules."""
    out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": ""}
    amts = AM.find_amounts(excerpt or "")
    i = next((n for n, a in enumerate(amts) if a["start"] == start), None)
    if i is None:
        return out
    a = amts[i]
    ss, se = next(((s, e) for s, e in AM._segments(excerpt) if s <= a["start"] < e), (0, len(excerpt)))
    bill = AM.billing_document(source, excerpt)
    sfigs = [j for j, x in enumerate(amts) if ss <= x["start"] < se]
    seg = excerpt[ss:se]
    skipped = []                      # dates left out because of the word or column before them (posted, statement ...)

    if len(AM._cells(seg)) >= 2:                                          # a table row: the column header says which date is the date of service
        row_ls = excerpt.rfind("\n", 0, a["start"]) + 1
        rl_end = excerpt.find("\n", a["start"])
        row_text = excerpt[row_ls:len(excerpt) if rl_end < 0 else rl_end]
        row_cells = [(m.start(), m.end()) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", row_text)]
        dos, other = [], []
        for u in _units(seg):
            head = _column_head(excerpt, row_ls, row_cells, ss + u.start)
            if not _lead_ok(seg, u) or (head and not _H_DOS.search(head) and _H_NON.search(head)):
                skipped.append(u.raw(seg))
            elif head and _H_DOS.search(head):
                dos.append(u)
            else:
                other.append(u)
        if dos or other:
            return _apply(out, _decide(dos or other, seg, date_iso))
    else:
        prev = max((amts[j]["end"] for j in sfigs if j < i), default=ss)
        own = excerpt[prev:a["start"]]
        units = [u for u in _units(own) if _lead_ok(own, u)]
        skipped += [u.raw(own) for u in _units(own) if not _lead_ok(own, u)]
        if units:
            return _apply(out, _decide(units, own, date_iso))
        if prev > ss:                                                      # a date stands once for the items listed after it: usable only when it is the line's one date
            whole = excerpt[ss:a["start"]]
            units = [u for u in _units(whole) if _lead_ok(whole, u)]
            if units:
                return _apply(out, _decide(units, whole, date_iso))
        tail = excerpt[a["end"]:min([amts[j]["start"] for j in sfigs if j > i], default=se)]
        if AM._TAIL_LEAD.match(tail):
            units = [u for u in _units(tail) if _lead_ok(tail, u, tail=True)]
            if units:
                return _apply(out, _decide(units, tail, date_iso))
    # no date of its own
    if bill:
        if AM._CODE_RX.search(excerpt[ss:a["start"]]):                     # a coded line takes the one period the bill states for its services
            prefix = excerpt[:se]
            seen, uniq = set(), []
            for u in _period_units(prefix):
                r = _certain(u, date_iso)
                key = (r[1], r[2]) if r[0] == "ok" else (u.raw(prefix),)
                if key not in seen:
                    seen.add(key)
                    uniq.append(u)
            if uniq:
                return _apply(out, _decide(uniq, prefix, date_iso))
        if skipped:
            out.update(reason="non_service_date", raw=skipped[0])
        return out
    if date_iso:                                                          # a dated encounter record (visit note, imaging report): the record's date is the visit
        out.update(state="stated", first=date_iso, last=None, reason=None, raw="")
    return out
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:15.018Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls artifacts/review-evidence/ | grep -i serve | head; cat artifacts/review-evidence/T-202-paralegal/p01_cases.py | head -80; lsof -iTCP:7974 -sTCP:LISTEN -nP; echo $?",
 "description": "Find launcher, read case driver, check port"
}
````

### User / tool · 2026-11-03T00:20:15.312Z

**tool result**
````
T-049-served-index.html
T-060-paralegal-pass4-serve.py
T-120-r2-paralegal-server.log
"""T-202 paralegal: f0921e4 archive, demo/fixture backend, local mode, port 7972.
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
1
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:18.953Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat artifacts/review-evidence/T-202-paralegal/letters_dump.py; head -30 artifacts/review-evidence/T-202-paralegal/all_charge_lines.py; cat artifacts/review-evidence/T-060-paralegal-pass4-serve.py",
 "description": "Read in-process letter dump scripts and launcher"
}
````

### User / tool · 2026-11-03T00:20:19.049Z

**tool result**
````
"""T-202 paralegal: dump the standard letter + notes for each letter_check variant (all_accepted, counted) for sample, case_09, lib14, lib10,
from a git-archive copy of f0921e4. Run from repo root:
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/letters_dump.py <archive_root> <out_dir>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
out = os.path.abspath(sys.argv[2])
sys.path.insert(0, root)
os.chdir(root)
from evals import letter_check as LC  # noqa: E402

CASES = {
    "sample": "evals/golden/sample.txt",
    "case_09": "evals/golden/case_09_nonvisit_hides_gap.txt",
    "lib14": "evals/library/case_lib14_handwritten_chiro_scans.txt",
    "lib10": "evals/library/case_lib10_eob_ub04_cms1500.txt",
}
for name, path in CASES.items():
    got = LC.letters_for(open(path).read())
    for variant in ("all_accepted", "counted"):
        v = got[variant]
        with open(os.path.join(out, f"{name}-{variant}-letter.txt"), "w") as f:
            f.write(v["letters"]["standard"])
        with open(os.path.join(out, f"{name}-{variant}-notes.txt"), "w") as f:
            f.write(v["notes"])
        lines = LC.charge_lines(v["letters"]["standard"])
        viol = LC.charge_date_violations(v["letters"]["standard"], v["records"])
        print(f"== {name} {variant}: cents={v['charge_cents']} refused={v['refused']} gate={v['gate']}")
        for h, q in lines:
            print("   ", h, "|", q)
        print("    violations:", viol)
"""T-202 paralegal: every BILLED CHARGES line (counted variant, standard style) of all letter_check cases on the f0921e4 archive, with the record it quotes.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/all_charge_lines.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
from evals import letter_check as LC  # noqa: E402

norm = lambda t: " ".join(str(t).split())
for name, text in LC.cases():
    got = LC.letters_for(text)["counted"]
    lines = LC.charge_lines(got["letters"]["standard"])
    print(f"== {name}: {len(lines)} charge line(s)")
    for h, q in lines:
        recs = [r for r in got["records"] if norm(q) in norm(r["excerpt"])]
        r = recs[0] if recs else {}
        print(f"   {h}\n      quote: {q}\n      record {r.get('n')} [{r.get('date_iso')}] {r.get('source')}: {r.get('excerpt')}")
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

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:19.653Z

Set up the archive and start the server.

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:22.823Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/t202r2 && git archive 986fc55 | tar -x -C $S/t202r2 && ls $S/t202r2 | head -30; git archive 986fc55 | git get-tar-commit-id",
 "description": "Extract fix commit archive to scratchpad"
}
````

### User / tool · 2026-11-03T00:20:24.764Z

**tool result**
````
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
a_e2e.out
a_letter_check.out
a_shard0.out
a_shard1.out
a_shard2.out
a_shard3.out
afiles.txt
app
arch
artifacts
ashard0.txt
ashard1.txt
ashard2.txt
ashard3.txt
board
deploy
docs
dump_new.txt
dump_old.txt
dumpc.py
env.sh
evals
export.orig
files.txt
memory
986fc551078a6ed6274cc9dd7a6a9efd0af357e3
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:29.032Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls $S; mkdir $S/pr2_986fc55 && git archive 986fc55 | tar -x -C $S/pr2_986fc55 && ls $S/pr2_986fc55",
 "description": "Extract into a fresh, empty directory"
}
````

### User / tool · 2026-11-03T00:20:30.788Z

**tool result**
````
641ed.bak
CLAUDE.md
GATEM3_se
M1
M1_nocombine
M2
M2_find0
MASTER_PROMPT.md
T-047-run1.json
T-060-pass2-head
T-093-r3-2ab7896
T-093-r3-run.py.orig
T-093-r3-scripts
T-093-r4-3223e50
T-093-r4-mutA
T-093-r4-mutB
T-109-probe
T-109-r1-card
T-109-r1-head
T-109-unit-head.txt
T-124-r1-head
T-124-r1-mut2
T-124-r1-parent
T-133-r1-archive
T-133-r1-source
T-133-r3-archive-4065ef2
T-133-r3-archive-f939ccb
T-133-r3-mutA
T-133-r3-mutB
T-133-r3-mutC
T-133-r3-mutD
T-133-r3-scripts
T-133-r4-archive-head
T-133-r5-13d.py
T-133-r5-15be212
T-133-r5-6fa8ecc
T-133-r5-head
T-133-r5-mut-backslash
T-133-r5-parent
T-133-r5-parse.py
T-133-r5-pmh.py
T-133-r5-probe.py
T-133-r5-r1
T-133-r5-unit-head.log
T-152-r1
T-157-r2-852b060
T-157-r2-full-unit.out
T-157-r2-mut
T-157-r2-mutants.out
T-157-r2-mutate.py
T-157-r2-parse.py
T-157-r2-probe.py
T-157-r2-probe2.py
T-157-r2-probe3-K.out
T-157-r2-probe3-base.out
T-157-r2-probe3.py
T-157-r2-probe4.py
T-157-r3-f31b146
T-157-r3-mut
T-157-r3-mutants.out
T-157-r3-mutate.py
T-160-r1
T-197-612dc2c
T-197-head
T-197-mutants
T-197-probe
T102_staff_r1
T102_staff_r2
T103_archive
T103_parent
T106_cli_out
T106_head_archive
T106_m_exportbranch
T106_m_hlreview
T106_m_hltrace
T106_m_pdfbypass
T106_m_pdfclaude
T106_m_rootcal
T106_r2_mut_a
T106_r2_mut_b
T106_r2_mut_c
T106_r2_mut_d
T106_r2_probe
T106_r2_suite.txt
T106_r2_suite_run2.txt
T106_r2_verify
T106_scripts
T106_unit_run1.log
T106_unit_run2_rs.log
T108_r2_clone
T108_r2_verify
T108_verify
T112_r1
T112_r1_scripts
T112_r2
T112_r3
T112_r3_mut
T112_r3_scripts
T113_r1_b66e748
T113_r1_b66e7481
T113_r1_e1ce8dc
T113_r1_evalout
T113_r1_fresh
T113_r1_head
T113_r2_arch
T113_r2_arch2
T113_r2_clone
T113_r2_probe
T113_r2_unit.log
T115_card_show.txt
T115_staff_r1
T115_staff_r2
T119_r2
T119_r3
T119_staff_r1
T120_r3_cli1.txt
T120_r3_cli2.txt
T120_r3_evals_head
T120_r3_evals_parent
T120_r3_fix
T120_r3_fixprobe.py
T120_r3_fprobe.py
T120_r3_head
T120_r3_mut
T120_r3_parent
T120_r3_probe_head.txt
T120_r3_probe_parent.txt
T120_r3_unit.txt
T128_9_127_r1
T128_9_r2
T128_9_r2b
T128r4_prev
T132r1
T132r1p
T132r3_arc
T132r3_cli1.err
T132r3_cli1.txt
T132r3_cli2.err
T132r3_cli2.txt
T132r3_cli_arc.txt
T132r3_cli_ctl.txt
T132r3_ctl
T132r3_mut
T133-r3-cli-1.txt
T133-r3-cli-2.txt
T133-r3-cli-r1.txt
T133-r3-negex.txt
T133-r3-pycontext-kb.yml
T133-r3-unit.log
T133-r4-arch-4065ef2
T133-r4-arch-e79c3aa
T133-r4-arch-parent
T133-r4-cli-reports.txt
T133-r4-clone
T133-r4-mutM1
T133-r4-mutM2
T133-r4-mutM3
T133-r4-pipeline-run1.txt
T133-r4-pipeline-run2.txt
T133-r4-record.json
T133-r4-scripts
T133-r4-suite-archive.txt
T133-r4-suite-clone.txt
T134r4_head
T134r4_head2db
T134r4_mut
T134r4_mut2
T134r4_src
T136_r1_e2e_full.txt
T136_r1_e2e_full2.txt
T136_r1_head
T136_r1_mutA
T136_r1_mutA.log
T136_r1_mutB1
T136_r1_mutB1.log
T136_r1_mutB2
T136_r1_mutB2.log
T136_r1_mutC
T136_r1_mutC.log
T136_r1_serve.sh
T136_r1_server.log
T136_r1_server2.log
T136_r1_unit.txt
T138r2_parent
T139_r1
T140_r1
T140_r2
T140_r3
T140_r4
T141_head
T141_mut
T141_pre
T141_preN2
T141_probe
T141_run
T141r2_head
T141r2_libreport.json
T141r2_mut2
T141r2_mutants.txt
T141r2_parent
T141r2_pk_T141_head.err
T141r2_pk_T141_head.json
T141r2_pk_T141_pre.err
T141r2_pk_T141_pre.json
T141r2_pk_T141r2_head.err
T141r2_pk_T141r2_head.json
T141r2_pl_orig.py
T141r3_head
T141r3_mut
T141r3_r2
T141r3_scripts
T141r4_head
T141r4_prev
T141r5_head
T141r5_mutA
T141r5_prev
T141r5_scripts
T141r6_824984f
T141r6_evidence
T141r6_head
T141r6_r5
T141r7_6379c0b
T141r7_824984f
T141r7_83f1afd
T141r7_acad4f6
T141r7_c2913a6
T141r7_head
T141r7_mut_guard2
T141r8_head_99438fb
T141r8_mutant_two_digit_off
T155_r1
T155r2_T164
T157r3
T159_161_r1
T162_r1
T162_r2
T162_r3
T167-mut
T167-r1-archive
T167-r1-out
T167-r1-out-local
T167-r1-out-local2
T168_r1
T169_staff_r1
T169_staff_r2
T179_r1
T179_r1_mut
T179_r2
T179_r2_mut
T196
T197_r2_9ab8cae
T197_r2_e425534
T197_r2_mut_both
T197_r2_mut_home
T197_r2_mut_none
T197_r2_mut_step1
T197_r2_scripts
T198-locate.py
T198-run1.txt
T198-run2.txt
__pycache__
_types.bak
a.sqlite3
a141
a178
a178.out
a201
a27e3a4.diff
a9ab
acc.py
across.py
addtags.py
adj_eval
adj_out
adr013.txt
after.py
all.txt
amounts_broken.py
ap3500.pdf
api
api.patch
api2
api_at_099732b.py
api_head.log
api_head.md
api_head.py
api_head.sqlite3
api_head_plus_mine.md
api_md_head.md
api_md_new.md
api_mine.md
api_new.py
api_parent.log
api_parent.sqlite3
apitmp
app
app-d0b04bc
app-head
app.log
app.pid
app.sqlite3
app2
app2.log
app2.pid
app2.sqlite3
app3
app3.sqlite3
app4
app4.log
app4.pid
app4.sqlite3
app5
app5.log
app5.pid
app5.sqlite3
app60
app60.log
app60.pid
app60.sqlite3
append_404.py
append_correction.py
ar2
ar_old
arc
arc.sh
arc2
arch
arch0c24
arch2
arch203r2
arch3
arch4
arch5
archB
arch_57a08ba
arch_head_r3b
arch_r2_54382
arch_r2_54382.idx
arch_r2b
arch_r2c
arch_r2d
arch_r3_final
arch_t140
archive
archpath.txt
artifacts
atk
aud.py
aud2.py
audit.py
audit_mine.js
audit_split.py
audited.bak
axe
b.sqlite3
base
base.json
base1.log
baseline_journey.out
before.txt
big.json
billing.orig
bis1.txt
bis2.txt
bis3.txt
bis4.txt
blank.py
blob.tmp
board
body.py
bombs
boom_final.py
boom_server.py
boundary.py
boundary2.py
build_evidence.py
build_set.py
build_set.py.bak
build_t099_blobs.py
busy.out
c
c01.json
c1.json
c5.json
c8a9874
ca.sh
cal.bak
case.json
case.json.tok
case07.json
case3.json
case3.json.tok
case_01_date_formats.json
case_lib11_priors_and_ledger.json
case_list.orig.bak
cases.txt
ce70
ce70-report.md
census.py
charge_text.py.patch
charges.py
check.py
check_golden.out
check_json.py
check_r2.py
check_r3_json.py
check_r4.py
checks2.sh
checks3.sh
chk.js
chk.py
chk2.py
chk_mut.py
chk_syntax.py
clean2
clean3
clean4
clean5
clean5_unit.txt
clean_run1.txt
cleanup_check.py
cli1.out
cli2.out
cli_c1.err
cli_c1.txt
cli_final.err
cli_head_out.txt
cli_rep1.err
cli_rep2.err
cli_rep3.err
clone-run
clone194
cmscms.py
collapsed.png
collapsed.py
commit.sh
commit_paths.sh
commit_r3.sh
commit_tree
commitcases.txt
conf-1440.png
conf-390.png
conf_A.py
conf_B.py
conftest_mine.py
conftest_split.py
controls_run.log
copy
copyA
copyC
copy_untracked.py
corp_base.json
corp_r2.json
corpus.py
count.py
count1.py
count_base.py
counts.sh
cr.sh
cred_b05.py
cred_orig.py
cs.sh
ctl-out
ctl.log
d.py
d1
d2
d3
d4
d5
d6
d7
d8
data
data2
dates.orig
db
db3
db4
db5
dbg
dbg.png
dbg.py
dbg2.py
dbg3.png
dbg3.py
dbg4.py
dbg5.py
dbg97.py
de1.txt
decisions_head.md
demo
demo.log
demo.sqlite
dev
dev.db
diag.py
diff.py
dl
docker-venv
docker_emu.sh
docker_serve.log
docker_serve.pid
dockerctx
dockerdata
dockerhome
docs
dom.bak
dos
draft-pass2.md
drive.py
dump.py
e1-1440.png
e1-390.png
e1-390b.png
e1.py
e1400d4
e2.py
e2e-data
e2e-m1-server.log
e2e-m1.sqlite
e2e-run.sqlite
e2e-server.log
e2e.db
e2e.out
e2e1.log
e2e2.db
e2e2.out
e2e3.out
e2e_full.txt
e2e_full1.txt
e2e_full2.txt
edit133.py
edit133b.py
edit133r2.py
edit199.py
emptytree
endpoints.py
env97
err.out
err2.out
es1.txt
ev.json
ev.sh
eval_base.out
eval_r2.out
evalout
evalout2
evals
ex07.json
ex1.sh
ex2.sh
ex3.sh
exp-077
exp.py
exp2.py
exp_077.py
export.py.patch
export_curated.sqlite
export_recorded.sqlite
f3.out
f5f1be9-tree
fe-data
fe3.log
fe3.sqlite
fe4.log
fe4.sqlite
fetch
figs.py
files.txt
fill.py
final-data
final.py
final1
final1.log
final2.log
finalize_f5f1be9.py
find_miss.py
first.png
fix.log
fix.sqlite3
fixture_run.out
fixture_run_b.out
flags_commit.py
flip.out
flip.py
fpl.bak
fpl_new.py
fpl_old.py
fr_r2.txt
fragile
fresh
fresh.py
fresh_head.log
fresh_head.sqlite3
fresh_nosbs.log
fresh_nosbs.sqlite3
full.done
full.log
full.out
full.patch
full.txt
full2.out
full_head.txt
fx
fx.log
fx.sqlite3
fx_before.txt
fxbak
gate.db
gate_dir.txt
gate_m2
gen
gen.py
gen_controls.py
gm2
gm2r2
gm2r2_legal
gm2r2clone
gm3
gm3-7991.log
gm3-7992.log
gm3-a11y-arch
gm3-a11y-audit.log
gm3-a11y-pid.txt
gm3-a11y-server.log
gm3-a11y-wrap.py
gm3-a11y.sqlite3
gm3-emptyfx
gm3-ux-7991.sqlite3
gm3-ux-7992.sqlite3
gm3src
golden_scan.py
guardprobe.py
guardprobe.py.bak
h.txt
h178
h42.py
h60.txt
h_audit.js
h_charges.js
h_conftest.py
h_review.js
h_stepper.js
harness
head
head-a850be0
head-bc12d44
head-ec33bf0
head.db
head.log
head.py
head.sqlite3
head0
head2
head2.py
head3
head4
head5
head7
head8
head9
headA
head_950d4a5
head_9851a0d_r5
head_9c1af01
head_ae76835_r3
head_clean
head_clean.log
head_clean.sqlite3
head_copy
head_e63e564
head_faee448_r4
head_nosbs
head_nosbs.log
head_nosbs.sqlite3
head_run.sh
head_scan.txt
headcheck
headchk2
headfe
headx
heldout.py
helpers.py
helpers2.py
hf-config.html
hf-docker.html
hits.py
hookcopy
idx
idx162r3b
idx167
idx171
idx2
idx3
idx4
idx5
idx_commit
idx_r2b
idx_r2c
idx_r2d
idx_r3
idx_t139r4
idx_t139r4b
idxpath
image-emu
ing.bak
ingest.orig
ingest_novel.py
inj.py
jcheck.py
judge_live.py
judges.png
k1dump.py
kb2.py
kb3.py
kb_test.py
keys.py
last_commit
latest.before.sha
latest.committed.json
latest_head.json
latest_new.json
leak.py
letter_check.py.patch
lib-after.md
lib.md
lib.out
lib_app.sqlite
lib_report.md
lib_report3.md
lib_report5.md
libdump.py
library-after.md
library-base.md
library-report.md
link
live-demo
live-demo.log
live-local
live-local.log
live23.sh
live3.sh
llm_head.md
local
local.log
local.sqlite
m1.txt
m2.txt
m2regate-live.log
m3
m3.txt
m4
m4.txt
m5
m55_M_drop_whole_rule
m55_M_only_needs_review
m55_M_only_rejected
m58_M1_round1_regex
m58_M2_dates_iso_dollar
m58_M3_amounts_valid_dollar
m58_M4_fence_dollar
m59_N11_drop_stale_basis_clause
m59_N12_failed_redraft_overwrites
m59_N13_drop_SEVERITY_NOT_QUOTED
m59_N3_drop_D006_token_check
measure.py
memory
mine
mine.diff
mine.patch
mine.txt
miss.py
miss2.log
miss2.py
mk.py
mk_r3.sh
mkd.py
mkfix.py
mkindex171.sh
mkpatch.py
mkpdf.py
mkreview.py
mkreviews.py
mob.py
msg.txt
msg_r3.txt
mut-A
mut-B
mut-C
mut-D
mut-M6_drop_family_lookbehind
mut-base
mut-control
mut-gate
mut-qual
mut-t073-A-broad-catch
mut-t073-B-no-guard-in-review
mut-t073-C-expected-becomes-supported
mut-t073-D-drop-class
mut-t084-1-no-judge-gate
mut-t084-2-no-wording-gate
mut-t084-3-no-negation-gate
mut-t084-4-unsure-accepted
mut-t084-5-no-audit
mut-t084-6-no-value-gate
mut-t084-7-judge-fail-open
mut-tok
mut.py
mut.py.bak
mut080.py
mut1
mut105.py
mut105.py.bak
mut159.py
mut161.py
mut2
mut2.py
mut200.py
mut2_B0_pinned_baseline
mut2_G1_grounding_check_removed_in_extract
mut2_S1_judge_unavailable_fails_open_in_state
mut2_S2_judge1_error_becomes_supported
mut3
mut3_S2b_shared_judge_error_fails_open_to_supported
mut3_S3_j2_error_fails_open_to_agree_pipeline_only
mut4
mut98
mut99
mutB.txt
mutT132
mut_M0_baseline
mut_M1_noRollback
mut_M1_sdk_internal_retries_2
mut_M2
mut_M2_cli_drops_strict_mcp
mut_M3
mut_M3_cli_timeout_600
mut_M4
mut_M4_cli_leaks_stderr_into_error
mut_M5
mut_M5_fixture_miss_retried
mut_M6
mut_M6_j2_error_becomes_agree
mut_M7
mut_M7_stray_subprocess_import_outside_backends
mut_R4M1_stated_total_always_suppressed
mut_R4M2_no_other_figures_on_rate_holder
mut_R4M2_rate_unclear_move_to_other_figures_removed
mut_R4M3_rate_row_drops_own_other_figure_move
mut_R4M3_rate_row_stated_total_not_other_figure
mut_R4R_line790_raises
mut_branch
mut_branch.sqlite
mut_dedupe
mut_flagsdeadline
mut_guard_e2e.out
mut_guard_unit.out
mut_rmfixture
mut_rmjudgefixture
mut_run.py
mut_run2.py
mut_t055_M_drop_whole_rule
mut_t055_M_only_needs_review
mut_t055_M_only_rejected
mut_t058_M1_round1_regex
mut_t058_M2_dates_iso_dollar
mut_t058_M3_amounts_valid_dollar
mut_t058_M4_fence_dollar
mut_t059_N11_drop_stale_basis_clause
mut_t059_N12_failed_redraft_overwrites
mut_t059_N13_drop_SEVERITY_NOT_QUOTED
mut_t059_N3_drop_D006_token_check
mutant-M1-nocombine.txt
mutant-M2-find0.txt
mutant375_journey.out
mutant_timeline572.out
mutants
mutants-db08276.log
mutants-r3-db08276.log
mutants-work
mutants.py
mutate2.py
mutate3.py
mutate_api.py
mutate_run.py
mutate_run2.py
mutate_t055.py
mutate_t058.py
mutate_t059.py
mutrun.sh
mutv2_1
mutv2_2
mutv2_3
mutv2_4
mutv2_5
mutv2_6
mutv2_7
mvp95
mvp95.log
mvp95.pid
mvp95.sqlite3
mw
n.py
narr.py
neg
neg2
negex
negtest
new.json
new2.json
new_record.py
novel.txt
nucc
nv.py
nv2.py
o1
o1.aIcW
o2
o2.vHBZ
o3_new.js
o3_v3.js
ocr_edit
ocr_edit_head
ocrinj
oe
oi
old-d0b04bc
old_unc.py
orch.idx
orig
out
out.txt
out_head.json
out_zlayt-pm-project.json
ov.py
overlay-head
own
p.py
p1.py
p1.txt
p2.db
p2.py
p2.txt
p3.log
p3.pid
p3.py
p3.sqlite3
p3.txt
p4-e293daa
p4-head
p5-b612176
p5-server.log
p5.db
p_be
p_fe
pa
page.txt
par
parent
parent-server.log
parent.sqlite3
part.py
part2-process.html
part2-process.pdf
paste.sqlite3
paste_attack_ledger.txt.sqlite
paste_synthetic_ledger.txt.sqlite
patch.py
patch2.py
patch3.py
patch_builder.py
path
path.txt
pathspec.txt
patterns.bak
patterns_copy
patterns_fresh
patterns_nomanual
pdb
pdf_time.py
pdfs
pdfs_head
peer.py
peer.sqlite3
personas
phi.py
pid
pid2
pidA
pidB
pin-690a0e3-r5
pin-6bca-r4
pin-8bc7f90
pin-HEAD-r4
pin-HEAD2-r4
pin-db08276
pin-f218263
pipeline.orig.py
pipeline.py
pipeline_commit.py
pl.orig
pm-gate.sqlite3
pn-head.md
pnh.html
pnh.pdf
portconflict.sh
pp
pp2
pre
pre-t123-archive
pre_t095_schema.sql
present.patch
present.py
prev
probe
probe-db
probe-r2-output.txt
probe-top.png
probe.py
probe.sqlite3
probe133.py
probe133r2.py
probe133r3.py
probe2.py
probe2.py.bak
probe2_t067.py
probe3.py
probe3_t067.py
probe4.py
probe404.py
probe5.py
probe98
probe99
probeA
probeA.stderr
probeA.stdout
probeB
probeB.stderr
probeB.stdout
probe_404.py
probe_7df
probe_copy.sqlite3
probe_copy2.sqlite3
probe_copy3.sqlite3
probe_copy4.sqlite3
probe_copy5.sqlite3
probe_curated.sqlite
probe_err.log
probe_failed.py
probe_flags.sqlite
probe_flags_audit.sqlite
probe_head
probe_head_out.txt
probe_nojudge.py
probe_r4_ocr.py
probe_recorded.sqlite
probe_rej.py
probe_run.py
probe_server.log
probe_t067.py
probe_timeout.py
probe_tray.py
probe_work_head
probe_work_head2
probes
probes-t100
probes159
probes161
probes_r5_dir
proc.png
proc.py
proc2.png
product-note.html
product-note.pdf
prof.out
prof.py
pub.log
pub.py
pub.sqlite3
pub2.log
pure2
pw
r
r1
r2
r2-07c7558
r2-07c7558-server.log
r2-07c7558.sqlite3
r2-802d5fd
r2-cases.out
r2-deploy-head
r2-deploy-wt
r2-head
r2-ocr
r2-planted
r2-server.log
r2-sweep.out
r2.db
r2.log
r2.pid
r2.sqlite3
r2_app.sqlite3
r2_blank_judges.py
r2_check.py
r2_detect.py
r2_es2.py
r2_export.json
r2_for2.py
r2_ids.txt
r2_library.md
r2_mixed.py
r2_mut_base
r2_mut_base_m
r2_mutant_r2b.py
r2_mutants.py
r2_probe_out.txt
r2_rec.sqlite3
r2_run.log
r2_sentinel_data
r2_set_status.py
r2_t080_app.log
r2_t080_app.sqlite
r2_token.txt
r2_treeid.txt
r2_unit.txt
r2a
r2app
r2app-d865
r2arch
r2b
r2c_tree.txt
r2d.sqlite3
r2d_run.log
r2d_tree.txt
r2demo
r2demo.log
r2head
r2live.log
r2live.pid
r2live.sqlite3
r2local
r2local.log
r2mut
r2o
r2parent
r2server.log
r2src
r3
r3-25f585c
r3-a27
r3-demo.db
r3-demo.log
r3-local.db
r3-local.log
r3-parent
r3-server.log
r3.db
r3.log
r3.pid
r3.sqlite3
r3_acceptance_strings.py
r3_accepted.json
r3_api.py
r3_check_json.py
r3_full.log
r3_gate_check.py
r3_mut
r3_rootcause.py
r3_sentinel_data
r3_server.log
r3_t080.sqlite
r3_tok.txt
r3a
r3ap
r3api
r3api2
r3app.sqlite3
r3arch
r3b
r3bp
r3clone.81DVDF
r3clone.out
r3copy
r3da0c7fe
r3db.sqlite3
r3dev
r3e2e.log
r3h
r3head
r3health.json
r3img
r3m
r3mut
r3o
r3pop
r3probe.py
r3run
r3run.out
r3runpid
r3scripts
r3server.log
r3src
r3tb
r3timing.txt
r3tree
r3workdir
r4-8f78874
r4_probe_8634bfe.out.txt
r4_rootcause.py
r4arch
r4data
r4out
r4pin
r4probe
r4probe_on_0f58181.txt
r5
r5.log
r5.pid
r5.sqlite3
r5_e3.png
r5_flag.png
r5_top.png
r5b
r_head.json
r_new.json
rail.png
raw1.txt
raw2.txt
raw3.txt
raw4.txt
raw5.txt
raw6.txt
rec.py
rec.sh
rec_a.log
rec_all.log
rec_all.sh
rec_b.log
rec_judges.log
rec_narr.py
rec_sample.log
recon.py
render_curated.log
render_curated.sqlite
render_flags.log
render_flags.sqlite
render_race.log
render_race.sqlite
render_recorded.log
render_recorded.sqlite
replay.py
replit-config.html
replit-deploy.html
replit_env.py
repo
repro_stale
req_mut.md
requirements-dev.txt
requirements.txt
rerec.log
rerec.sh
rerun.out
rerun.sh
rerun2.sh
research
review.bak
review_commit.py
review_fixed.js
review_head.js
review_headplus.py
review_mine.py
reviews
rt_base.json
rt_r2.json
run.base.py
run.head.py
run.log
run.try.py
run1.err
run1.log
run1.out
run2
run2.err
run2.log
run2.out
run3.err
run3.log
run3.out
run4.err
run4.out
run4.time
run5.err
run5.out
run6.err
run6.out
run_c5.py
run_m2.pid
run_m2.sh
run_mutants_r3.py
run_p3_chain.sh
run_r3.sh
run_ro.py
run_t070_orig.py
runs.status
rv_T132_T128_r2r3
s-1440-0.png
s-1440-1700.png
s-1440-2300.png
s-1440-2600.png
s-1440-3300.png
s-1440-4400.png
s-1440-5400.png
s-1440-900.png
s-390-0.png
s-390-1500.png
s-390-3000.png
s-390-900.png
sample_case.json
sc.log
sc.sqlite3
scan.py
scan.py.bak
scan_specimens.py
scan_time_10x5000wide.pdf
schema_pre_T095.sql
score.py
scr.log
scr.sqlite3
scripted.log
scripts
scroll.py
selfcheck-r2.txt
serve_p3_wrapper.py
serve_snap.py
server-7871.log
server-7872.log
server.err
server.log
server.out
server.pid
server2.log
server2.pid
server7867.log
shard0.out
shard1.out
shard2.out
shard3.out
shard4.out
shoot.py
shot.py
shot2.py
shots
shots.log
shots.py
shots2.py
shots_old.py
shots_t046r2.py
show.py
show_T103.txt
snap
snap-077
snap-89a323a
snap-c61
snap-final
snap-h2
snap-head
snap-t187r3
snap.out
snap.path
snap2
snap3
snap7942
snap7942.db
snap7942.log
snap7942.pid
snap9
snap_run.sh
sp.txt
spec
splice.py
spy3.log
spy3.py
src
srv.KdvV
srv.log
srv.out
srv.pid
srv2.log
srv2.pid
srvdir
st_commit.py
stable.py
start.sh
states.py
steps-open.png
store.orig.bak
strip.py
strip_and_grep.py
submission
sync.py
sync.sh
sync_r5.sh
t015r4
t028.out
t030r2mut
t033mut
t033mut.py
t035
t038
t038r3
t040-077
t040-head
t040-live
t043-239
t043_r2_probe.py
t043_r2_probe2.py
t043_r2_probe3.py
t045r2-bypass
t045r2-clean
t045r3-clean
t046-server.log
t046.sqlite3
t046r2.log
t046r2.pid
t046r2.sqlite3
t053r3-data
t055_base_full.txt
t055_mut_full.txt
t056r2_01ipr4y9
t056r2_5_pc8ore
t056r2_gxnki_45
t056r2_jvse81hd
t056r2_pjbon2yp
t057
t060-a11y-axe
t060-a11y-data
t060-a11y-head
t060-a11y-serve.py
t060-p3-app
t060-p3-axe
t060-p3-chain.log
t060-p3-review.json
t060-p3-server.log
t060-p3-server.pid
t060-p3.sqlite3
t060p2
t060p2-wrap
t065
t065r2
t066r2
t066r3
t067
t067_59c7edb
t067_f6fa2dd
t067_head_archive
t067_m1
t067_m2
t067_m3
t067_probes
t067head
t067parent
t067r3
t067r4
t067r5
t067r5-probe-out.txt
t068-data
t068-data-commit
t068-data-commit2
t068-server-commit.log
t068-server-commit2.log
t068-server.log
t068r2-server.log
t068r2-snap
t068r3-case01-body.json
t068r3-case01-get.json
t068r3-data
t068r3-head
t068r3-probe-token.txt
t068r3-server.log
t070
t070r2b
t071_title_probe.py
t072
t072plant
t072r3
t072r3-p1_be_selfreport
t072r3-p2_be_patientstatement
t072r3-p3_be_patientstates
t072r3-p4_fe_selfreport
t072r3-p5_fe_patientstatement
t072r3-p6_fe_selfreported_ui
t072r4
t072r4_plants
t074
t075r2
t076r2
t076r2-data
t076r2-server.log
t077r3
t079.log
t079.sqlite3
t080m_M10_date_always_confirmed
t080m_M11_judge_partial_is_pass
t080m_M12_date_blocker_reason
t080m_M13_overrides_not_counted
t080m_M14_unavailable_counted_judged
t080m_M15_agreement_never_fails
t080m_M16_verbatim_fail_ignored_on_entry
t080m_M17_skip_after_reject_removed
t080m_M18_nothing_accepted_removed
t080m_M19_unsupported_excludes_disagrees
t080m_M1_rejected_blocks_gate
t080m_M20_step_order_swap
t080m_M21_progress_counts_skipped_as_pending
t080m_M22_total_inclusion_accepted_pending
t080m_M23_fixed_why_replaced_by_model_text
t080m_M2_dismissed_blocks_gate
t080m_M3_dismissed_human_pass
t080m_M4_qualifier_always_pass
t080m_M5_gate_ignores_running
t080m_M6_rate_pending_total
t080m_M7_raw_leak_in_metadata
t080m_M8_event_before_after_leak
t080m_M9_edited_text_leak
t080m_base
t080r4
t085r2
t085r3
t086head
t086wt
t090-out
t090.index
t090.patch
t090_code.patch
t090_patch2.py
t090_patch_run.py
t090_patch_tests.py
t090r2
t090r3
t092
t093.base.py
t094r2
t095.patch
t095r2_head
t096-evals
t096-export-check.py
t096-ux-36ceb38
t096-ux-server.log
t096-ux-walk-output.txt
t096-ux.sqlite3
t096_all.py
t096_ds.py
t096_probe.py
t096_probe2.py
t096_shot.py
t096_shot2.py
t096_start.sh
t096data
t097
t097.log
t097.pid
t097.sqlite3
t097b.sqlite3
t097r2
t097r2-server.log
t097r2.sqlite3
t097r2head
t097r3-archive-9f2811f
t097r3-server.log
t097r3-server.pid
t097r3.sqlite3
t098-e511778
t098-f5ddec8
t098-head
t099-3ecb8b1
t099-dirty-check
t099-f345bc8-r2
t099-gitclone-parent
t099-mut
t099.index
t099_msg.txt
t1.xXug
t100-card
t100-fresh
t101
t101r2
t103r2
t103r3_api.diff
t103r3_archive
t103r3_billing.diff
t103r3_control_archive
t103r3_mut
t103r4_archive
t104
t104-3462ad0-ux
t104-server.log
t104-server.pid
t104-state.json
t104-ux.sqlite3
t105
t105r2
t106_r2_archive
t108
t109_adr_edit.py
t109_doc_edit.py
t109r2_head
t109r2_mutA
t109r2_mutB
t109r2_pin
t109r3_head
t109r3_mut
t109r3_mutate.py
t109r3_pin
t109r3_probe_cc.py
t109r3_probe_flags.py
t109r3_probe_flags2.py
t109r3_probe_trim.py
t109r3_probe_trim2.py
t109r4
t110.sqlite3
t110b.sqlite3
t111-archive
t111-parent
t111r2
t111r2-base
t111r2-base.out.json
t111r2-head
t111r2-head.out.json
t111r2-parent
t111r2-parent.out.json
t112.index
t112_live.sh
t112_pipeline.py
t113_run1_evidence
t114
t114r2
t115.pid
t115.sqlite
t115srv.log
t116r2-base
t116r2-head
t116r3
t116r4
t116r5
t118-head
t118-mutA
t118-mutB
t118-pre
t119
t119.log
t119.pid
t119.sqlite3
t119m
t119m.log
t119m.pid
t119m.sqlite3
t120
t120-123-archive
t120-123-server.log
t120-123.sqlite3
t120-parent-archive
t120-parent-server.log
t120-parent.sqlite3
t120-r3.sqlite
t120r2
t120r2.sqlite3
t120r4
t121r2
t123-cmp-head.jsonl
t123-cmp-pre.jsonl
t126r1
t126r2
t133_r1_m3_full.out
t133_r1_m3_full.py
t133_r1_mutate.py
t133_r1_probe.py
t133_r2_probe_mine.py
t134_app.sqlite3
t134_server.log
t134m
t134parent
t134parent2
t134r1
t134r2
t134r3_c4bb
t134r3_cli1.err
t134r3_cli1.txt
t134r3_cli2.err
t134r3_cli2.txt
t134r3_dbg
t134r3_fix
t134r3_head
t134r3_mut
t134r3_mut.txt
t134r3_mut2
t134r3_mut_h.txt
t134r3_par
t134r3_unit.txt
t134r3_unit_c4bb.txt
t134r3_unit_fix.txt
t134scripts
t136-archive
t136-r2-staff
t136-server.log
t136.db
t139
t139_app.sqlite3
t139_overlay.err
t139_overlay.out
t139_overlay.sqlite3
t139_server.err
t139_server.out
t139_trace.sqlite3
t139_trace2.sqlite3
t139clean
t139overlay
t139r2
t139r2_app.sqlite3
t139r2_server.log
t139r3
t139r3_app.sqlite3
t139r4
t139r4_app.sqlite3
t139r4_server.log
t139r5
t139r5_mut1
t139r5_mut2
t139r5_mut3
t139r5_out
t139r5_prev
t139r5_scripts
t139tree
t143
t143p
t143r2
t143r2_case_lib01_er_only_then_gap.txt
t143r2_case_lib02_slip_fall_prior_knee.txt
t143r2_case_lib03_truck_rear_end_chiro.txt
t143r2_case_lib04_dog_bite_scar_revision.txt
t143r2_case_lib05_pedestrian_orif_hardware.txt
t143r2_case_lib06_lop_billed_vs_adjusted.txt
t143r2_case_lib07_parking_lot_fall_outside_records.txt
t143r2_case_lib08_second_crash_mri_after.txt
t143r2_case_lib09_spanish_interpreter_espalda.txt
t143r2_case_lib10_eob_ub04_cms1500.txt
t143r2_case_lib11_priors_and_ledger.txt
t143r2_case_lib12_records_review_credibility.txt
t143r2_case_lib13_cloned_notes_cross_provider.txt
t143r2_case_lib14_handwritten_chiro_scans.txt
t143r2_case_lib15_conclusory_letter_mist.txt
t143r2_mut.py
t143r2_sample.txt
t143r3
t144r1
t145r1
t146r2
t146r3
t146r4
t148r1
t149db
t149r2
t149r2-server.log
t149r2.pid
t149r2.sqlite3
t149server.log
t149src
t151-25f585c
t151-out
t151-scripts
t152_collect.py
t152_diff.py
t154
t154.sqlite3
t154b.sqlite3
t154r2
t154r2p
t155
t155r2
t157-check-json.py
t157-r1
t157r2b
t158-card
t158-f31
t158-f31-m2
t158-f31-m6
t158-f31-runs
t158-head
t158-m2
t158-m3
t158-m4
t158-m5
t158-m6
t158-mut
t158-probe
t158-r1
t158-review-head.js
t158-review-pre.js
t158-settle
t158r3
t159.patch
t160-review
t162.sqlite3
t162r2
t162r2.base
t162r2.idx
t162r3
t162r3.idx
t162v-final
t165-backend
t165-r2
t165-review
t165r2b
t166
t166-mvp-r2-ux-d865.sqlite3
t166-mvp-r2-ux.sqlite3
t166-r2-ux-d865.log
t166-r2-ux-server.log
t168r2
t169-clone-2
t169r2
t171
t171app.sqlite3
t171server.log
t173-final
t173-gen
t173-head
t173-verify
t173.idx
t174
t174r4-local.db
t174r4-local.log
t174r4-public.db
t174r4-public.log
t174r4-src
t175r1
t175r2
t177-arch
t177-arch-base
t177r4
t177r5-fresh
t177r5-prev
t177r5-probe
t178-interrupt.db
t178-interrupt2.db
t178-old.db
t178-pastes.db
t178-pid-7882
t178-pid-7883
t178-pid-7884
t178-server-7881.log
t178-server-7882.log
t178-server-7883.log
t178-server-7884.log
t178-stale.db
t179_commit.index
t179_final.index
t179_old
t179r2
t179r2_unit.txt
t179v2
t180.db
t181
t181-app.sqlite3
t181-local-server.log
t181-local.sqlite3
t181-server.log
t181r3-2c19817
t181ux
t182
t182-3sjF
t182-dir.txt
t182-index.html
t182-serve.log
t182-serve.pid
t182-t0.txt
t182-t1.txt
t182-z.txt
t187r2
t194.index
t194_commit.sh
t194_msg.txt
t199.index
t199_commit.sh
t199_msg.txt
t2.q4VB
t200
t200.idx
t200run
t201-r1
t202
t202.idx
t202.tree
t202parent
t202r2
t203
t203r2
t203r2.idx
t2b.IKsK
t3.ORDQ
t4.0u5g
t84r4
tabflow.py
tail.md
test_billing_old.py
tests
tests_b05.py
tests_evals.sh
thr.py
thr2.out
thr2.py
timed_run.sh
tmp.index
tmp2.index
tmp3.index
tmpidx_t197
tmpindex
tog-open.png
tog.py
tok.json
tok_c1_local
tok_c3_local
tok_c5_local
tok_c7_local
tok_case_lib01_er_only_then_gap
tok_case_lib02_slip_fall_prior_knee
tok_case_lib03_truck_rear_end_chiro
tok_case_lib04_dog_bite_scar_revision
tok_case_lib05_pedestrian_orif_hardware
tok_g02_local
tok_g04_local
tok_g06_local
tok_g08_local
tok_g09_local
tok_sample2_local
tok_sample_local
tok_sample_pub
tokens.json
tools
tree
tree.sha
tree.txt
tree3
tree4
tree5
tree_r2
tree_r3
two.py
two.py.bak
u.orig
ub
ui-demo
ui-input.out
ui-local
unit-run-r2-clone-with-git.txt
unit-run-r2.txt
unit.out
unit.txt
unit1.txt
unit171.log
unit2.out
unit3.out
unit_full.txt
unit_full_head.out
unit_r2a.txt
unit_r2b.txt
ux-mvp-r3-da0c7fe.sqlite3
ux-mvp-r3-server.log
ux-mvp-r3.pid
ux-r2-2.sqlite3
ux-r2-3.sqlite3
ux-r2-debug-sample.png
ux-r2-server-2.log
ux-r2-server-3.log
ux-r2-server.log
ux-r2-server.pid
ux-r2.sqlite3
ux-t203-38ee0c3
ux-t203-demo.log
ux-t203-demo.pid
ux-t203-demo.sqlite3
ux-t203-e2e.out
ux-t203-local.log
ux-t203-local.pid
ux-t203-local.sqlite3
ux-t203r2-demo.log
ux-t203r2-demo.sqlite3
ux-t203r2-e2e.out
ux-t203r2-fa34fe9
ux-t203r2-local.log
ux-t203r2-local.sqlite3
ux3
v
validate_review.py
verify.py
view.json
walk.out
walk.py
walk2.py
why.orig.py
wide.py
wprobe.py
wt
wt-031a708
wt-7df65fb
wt-golden.txt
wt-head
wt2
wt7944.db
wt7944.log
wt7944.pid
wt7945.db
wt7945.log
wt7945.pid
wt7946.db
wt7946.log
wt7946.pid
wt_final
wt_final2
wt_head
wt_run.sh
wt_t155
x45.py
xc.py
xss.py
zlayt-base
zlayt-head
zlayt-public-snapshot.JTMbwv
zlayt-r2
zlayt-r3
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

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:36.744Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr2_986fc55; mkdir -p artifacts/review-evidence/T-202-paralegal-r2; cd $A && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/pytest-t202.out 2>&1; tail -3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/pytest-t202.out",
 "description": "Run T-202/T-200 unit tests from archive"
}
````

### User / tool · 2026-11-03T00:20:44.280Z

**tool result**
````
...................................................................      [100%]
67 passed in 7.14s
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:20:48.074Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr2_986fc55 && LLM_BACKEND=fixture FIXTURE_SET=curated PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.letter_check > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/letter_check.out 2>&1; tail -c 1500 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/letter_check.out",
 "description": "Run letter_check eval from archive"
}
````

### User / tool · 2026-11-03T00:20:59.193Z

**tool result**
````
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:21:29.108Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat artifacts/review-evidence/T-202-paralegal/probe_eval_teeth.py; git show 986fc55:evals/letter_check.py | grep -n \"def \\|_PERIOD\\|several\\|ambig\" | head -60",
 "description": "Read eval-teeth probe and new letter_check outline"
}
````

### User / tool · 2026-11-03T00:21:29.202Z

**tool result**
````
"""T-202 paralegal: does evals/letter_check.charge_date_violations catch a wrong-but-stated date? (posting date in a ledger row; the other claim date on a CMS-1500 line).
SYNTHETIC probe text. f0921e4 archive.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/probe_eval_teeth.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
from evals import letter_check as LC  # noqa: E402

T2 = ("Itemized ledger\nPosted      DOS         CPT    Description            Charges    Balance\n"
      "06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00     $70.00")
T3 = "CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, $185.00, 1 unit; CPT 20610, $210.00, 1 unit."


def letter(head, fig, quote):
    return f"BILLED CHARGES\n\n{head}: {fig}\nSource [Ex. __ / Bates __]: \"{quote}\"\n\nBilled charges accepted from these records: {fig}"


cases = [
    ("T2 posted date printed as DOS (what f0921e4 prints)", [{"n": 1, "source": "Larkspur Hollow Physical Therapy, itemized ledger", "date_iso": "2026-07-01", "excerpt": T2}],
     letter("Larkspur Hollow Physical Therapy, itemized ledger, June 11, 2026", "$70.00", "06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00")),
    ("T3 injection line dated with the other claim date (what f0921e4 prints)", [{"n": 1, "source": "Wardlaw Orthopedics, CMS-1500", "date_iso": "2026-07-14", "excerpt": T3}],
     letter("Wardlaw Orthopedics, CMS-1500, June 24, 2026", "$210.00", "CPT 20610, $210.00, 1 unit")),
]
for label, recs, txt in cases:
    print(f"== {label}\n   violations: {LC.charge_date_violations(txt, recs)}")
16:quote states, or, when the quote states none, of the one period the bill states before it; a date readable two ways, with a two-digit year or no year, a quote with several dates and no
17:service-date column heading, or a bill that states several periods may print nothing but the T-200 form '(statement dated X; service date not stated)', X the record's date. The check has
35:def dollar_figures(text: str) -> list:
41:def other_currency(text: str) -> list:
47:def unmarked_money(text: str) -> list:
53:def cases():
59:def violations(letter: str, accepted_cents=(), expect_none: bool = False) -> list:
88:def _walk(conn, cid, dismiss_charges=False):
108:def _count_all(conn, cid):
140:def _iso(txt):
145:def _head_dates(head: str):
167:def charge_lines(letter: str) -> list:
190:_PERIOD_WORD = re.compile(r"(?:statement period|billing period|service period|dates? of service|\bdos\b|service dates?|run of|date of the run)\W{0,6}$", re.IGNORECASE)
194:def _month(name):
198:def _real(y, m, d):
206:def _written(text):
255:def _readings(unit, ref):
256:    """The readings left for a written date: those not after the record's own date when the writing allows several (a service does not follow its statement)."""
263:def _own_dates(text):
267:def _period_dates(before):
272:        if _PERIOD_WORD.search(before[max(0, u["start"] - 40):u["start"]]):
281:def _dos_column(ex, quote, printed_first):
282:    """For a quote that holds several dates: the heading (nearest digit-free line above the quote's line, split at 2+ spaces) over the printed date's column, or ''."""
302:def charge_date_violations(letter: str, records) -> list:
307:      - the quote states several dates -> the line prints one only if the column heading over it names the date of service;
308:      - the quote states none, in a bill -> the bill's one stated period (statement period, dates of service, run of ...), whole; several stated dates, or none -> the not-stated form
340:                        problems.append(f"the quote states several dates and no column heading names the date of service (heading '{col}')")
350:                    problems.append("the bill states " + ("no" if not units else "several") + " dates of service and the line prints one")
364:def letters_for(text: str, backend: str = "fixture") -> dict:
395:def dismissed_in_bills(notes: str, providers) -> list:
402:def measure(case_list=None, backend: str = "fixture") -> dict:
427:def main(argv=None) -> int:
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:21:30.083Z

Now the adversarial probe script against the shipped path.

### Assistant · claude-opus-5-5 · 2026-11-03T00:22:05.208Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/probe_r2.py",
 "content": "\"\"\"T-202 r2 paralegal probe: for each charge figure on SYNTHETIC bill shapes, the Step 3 / letter service-date value the shipped path returns\n(store.charge_service_date -> service_date.resolve), i.e. the exact text the letter prints after the provider, plus reason and confirm note.\nIncludes my r1 shapes (P1-P10, T1-T3) unchanged and new adversarial shapes (N*). Run from repo root on the 986fc55 archive:\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_r2.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, store  # noqa: E402\n\nPROBES = [\n    # r1 shapes, unchanged text\n    (\"P1 two-row ledger, own dates\", \"Hobbleton Family Clinic, itemized ledger\", \"2026-03-15\",\n     \"Statement date 03/15/2026. 02/02/2026 office visit charge $275.00. 02/16/2026 x-ray charge $150.00. Balance due $425.00.\"),\n    (\"P2 CMS-1500 two DOS joined by 'and'\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"CMS-1500 for dates of service 06/24/2026 and 07/08/2026. CPT 99204 charge $185.00. CPT 20610 charge $210.00.\"),\n    (\"P3 invoice date stated before run date\", \"Tarnwick Fire-Rescue, ambulance invoice\", \"2026-11-12\",\n     \"Invoice date 11/12/2026. Run of 09/14/2026. A0427 ALS emergency transport, charge $1,380.00.\"),\n    (\"P4 UB-04 period across months\", \"Saltmarrow General Hospital, UB-04 itemized bill\", \"2026-07-10\",\n     \"UB-04 statement period 06/28/2026 to 07/02/2026. Rev 0120 room and board, FL47 total charges $4,920.00.\"),\n    (\"P5 UB-04 period with 'through'\", \"Saltmarrow General Hospital, UB-04 itemized bill\", \"2026-06-19\",\n     \"UB-04 statement period 06/09/2026 through 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.\"),\n    (\"P6 UB-04 period with hyphen\", \"Saltmarrow General Hospital, UB-04 itemized bill\", \"2026-06-19\",\n     \"UB-04 statement period 06/09/2026 - 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.\"),\n    (\"P7 statement + DOS label same sentence\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Statement date 03/01/2026, date of service 02/02/2026: office visit charge $275.00.\"),\n    (\"P8 ledger row DOS then posted, two-digit years\", \"Fennimoor Spine Clinic, itemized ledger\", \"2026-06-15\",\n     \"06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00. 06/12/26 06/13/26 97110 Therapeutic exercise charge $95.00.\"),\n    (\"P9 statement period then a separately dated line\", \"Saltmarrow General Hospital, UB-04 itemized bill\", \"2026-06-19\",\n     \"UB-04 statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, service date 06/09/2026, FL47 total charges $2,105.00.\"),\n    (\"P10 'from X to Y' dates of service\", \"Capital PT, billing statement\", \"2026-03-20\",\n     \"Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 therapeutic exercise, 9 units, charge $1,665.00.\"),\n    (\"T1 ledger table: DOS + posted columns\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"Itemized ledger\\nDOS         Posted      CPT    Description            Charges    Balance\\n\"\n     \"06/10/2026  06/11/2026  97140  Manual therapy x1      $70.00     $70.00\\n\"\n     \"06/17/2026  06/18/2026  97110  Therapeutic exercise   $95.00     $165.00\"),\n    (\"T2 ledger table: posted column first (r1 blocker)\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"Itemized ledger\\nPosted      DOS         CPT    Description            Charges    Balance\\n\"\n     \"06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00     $70.00\\n\"\n     \"06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00     $165.00\"),\n    (\"T3 CMS-1500, two dates of service joined by 'and' (r1 blocker)\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, $185.00, 1 unit; CPT 20610, $210.00, 1 unit. Item 28 TOTAL CHARGE $395.00. Item 29 AMOUNT PAID $0.00.\"),\n    # new adversarial shapes\n    (\"N1 posted-first ledger, uppercase header, pipes\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"POSTED     | SVC DATE   | CODE  | DESCRIPTION          | CHARGE\\n\"\n     \"06/11/2026 | 06/10/2026 | 97140 | Manual therapy x1    | $70.00\\n\"\n     \"06/18/2026 | 06/17/2026 | 97110 | Therapeutic exercise | $95.00\"),\n    (\"N2 posted-first ledger, header 'Post Date / Date of Service'\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"Post Date    Date of Service   Code   Description             Amount\\n\"\n     \"06/11/2026   06/10/2026        97140  Manual therapy x1       $70.00\\n\"\n     \"06/18/2026   06/17/2026        97110  Therapeutic exercise    $95.00\"),\n    (\"N3 posted-first rows, NO header\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00\\n\"\n     \"06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00\"),\n    (\"N4 posted-first, header uses generic 'Date' for the DOS column\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"Posted      Date        CPT    Description            Charges\\n\"\n     \"06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00\\n\"\n     \"06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00\"),\n    (\"N5 ledger with only a 'Trans Date' column (transaction date)\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"Trans Date   Code   Description             Charges\\n\"\n     \"06/11/2026   97140  Manual therapy x1       $70.00\\n\"\n     \"06/18/2026   97110  Therapeutic exercise    $95.00\"),\n    (\"N6 sentence ledger: 'Posted X for DOS Y'\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"Posted 06/11/2026 for DOS 06/10/2026: manual therapy $70.00. Posted 06/18/2026 for DOS 06/17/2026: therapeutic exercise $95.00.\"),\n    (\"N7 sentence: date then 'posted' after it\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"06/11/2026 posted, DOS 06/10/2026, manual therapy $70.00.\"),\n    (\"N8 CMS-1500 with per-line item 24A dates\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"CMS-1500. Item 24A 06/24/2026 CPT 99204 $185.00. Item 24A 07/08/2026 CPT 20610 $210.00. Item 28 TOTAL CHARGE $395.00.\"),\n    (\"N9 CMS-1500 'dates of service 06/24/2026, 07/08/2026' (comma list)\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"Dates of service 06/24/2026, 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.\"),\n    (\"N10 CMS-1500 'from 06/24/2026 to 07/08/2026' (claim span, 2 discrete visits)\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"CMS-1500 dates of service from 06/24/2026 to 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.\"),\n    (\"N11 CMS-1500 with DOI in the same sentence as a coded line\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"Item 14 date of current injury 05/30/2026, CPT 99204 office visit $185.00.\"),\n    (\"N12 CMS-1500 with patient DOB in the same sentence\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"Patient DOB 03/15/1980, CPT 99204 office visit $185.00.\"),\n    (\"N13 accident date leading a bill line\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Date of accident 01/09/2026, office visit charge $275.00.\"),\n    (\"N14 ambiguous numeric, both readings before statement\", \"Hobbleton Family Clinic, billing statement\", \"2026-06-01\",\n     \"Date of service 04/05/2026: office visit charge $275.00.\"),\n    (\"N15 ambiguous numeric, one reading after statement (D-071 clarification)\", \"Hobbleton Family Clinic, billing statement\", \"2026-04-30\",\n     \"Date of service 04/05/2026: office visit charge $275.00.\"),\n    (\"N16 month-name date with no year\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Office visit on February 2: charge $275.00.\"),\n    (\"N17 month-name period with year\", \"Saltmarrow General Hospital, UB-04 itemized bill\", \"2026-07-10\",\n     \"Statement covers period June 28-July 2, 2026. Rev 0120 room and board $4,920.00.\"),\n    (\"N18 'statement period' but prior-balance date in same sentence\", \"Saltmarrow General Hospital, UB-04 itemized bill\", \"2026-07-10\",\n     \"Previous balance as of 05/31/2026 $100.00; Rev 0450 emergency room 06/09/2026 $2,105.00.\"),\n    (\"N19 payment-first sentence then charge\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Payment received 02/20/2026 $50.00, office visit charge $275.00.\"),\n    (\"N20 UB-04 FL6 6-digit from/through\", \"Saltmarrow General Hospital, UB-04\", \"2026-06-19\",\n     \"FL6 statement covers period FROM 060926 THROUGH 061226. Rev 0450 emergency room FL47 $2,105.00.\"),\n    (\"N21 admit / discharge dates\", \"Saltmarrow General Hospital, UB-04\", \"2026-06-19\",\n     \"Admit 06/09/2026, discharge 06/12/2026, Rev 0120 room and board $4,920.00.\"),\n    (\"N22 date after the figure\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Office visit charge $275.00 on 02/02/2026.\"),\n    (\"N23 visit note (not a bill) with a fee, no date in sentence\", \"Dr. Alvarez, primary care\", \"2026-01-16\",\n     \"Office visit level 3. Fee $150.00.\"),\n    (\"N24 ledger: two posted dates then DOS in row, header names all\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"Billed       Posted      DOS         CPT    Charges\\n\"\n     \"06/12/2026   06/11/2026  06/10/2026  97140  $70.00\"),\n    (\"N25 ISO dates in a posted-first ledger\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"Posted      DOS         CPT    Charges\\n\"\n     \"2026-06-11  2026-06-10  97140  $70.00\"),\n]\n\nfor label, src, rd, ex in PROBES:\n    print(f\"== {label}  (record date {rd}; source '{src}')\")\n    print(\"   \" + ex.replace(\"\\n\", \"\\n   \"))\n    rec = {\"id\": \"r1\", \"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex, \"text\": ex}\n    for a in AM.find_amounts(ex):\n        if a.get(\"cents\") is None:\n            continue\n        item = {\"excerpt\": ex, \"value_cents\": a[\"cents\"], \"raw\": a[\"raw\"], \"excerpt_start\": 0}\n        d = store.charge_service_date(item, rec, a[\"start\"])\n        line = f\"{src}, {d['text']}\" if d[\"state\"] == \"stated\" else f\"{src} {d['text']}\"\n        print(f\"   {a['raw']:>10} -> letter head: '{line}: {a['raw']}'  state={d['state']} reason={d['reason']}\")\n        if d[\"confirm_note\"]:\n            print(f\"              Step 3 note: {d['confirm_note']}\")\n"
}
````

### User / tool · 2026-11-03T00:22:05.435Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/probe_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:22:09.017Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_r2.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr2_986fc55 > artifacts/review-evidence/T-202-paralegal-r2/probe_r2.out 2>&1; cat artifacts/review-evidence/T-202-paralegal-r2/probe_r2.out",
 "description": "Run adversarial service-date probes"
}
````

### User / tool · 2026-11-03T00:22:09.370Z

**tool result**
````
== P1 two-row ledger, own dates  (record date 2026-03-15; source 'Hobbleton Family Clinic, itemized ledger')
   Statement date 03/15/2026. 02/02/2026 office visit charge $275.00. 02/16/2026 x-ray charge $150.00. Balance due $425.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger, February 2, 2026: $275.00'  state=stated reason=None
      $150.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger, February 16, 2026: $150.00'  state=stated reason=None
      $425.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger (statement dated March 15, 2026; service date not stated): $425.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== P2 CMS-1500 two DOS joined by 'and'  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500')
   CMS-1500 for dates of service 06/24/2026 and 07/08/2026. CPT 99204 charge $185.00. CPT 20610 charge $210.00.
      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $185.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/24/2026, 07/08/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $210.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/24/2026, 07/08/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== P3 invoice date stated before run date  (record date 2026-11-12; source 'Tarnwick Fire-Rescue, ambulance invoice')
   Invoice date 11/12/2026. Run of 09/14/2026. A0427 ALS emergency transport, charge $1,380.00.
    $1,380.00 -> letter head: 'Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00'  state=stated reason=None
== P4 UB-04 period across months  (record date 2026-07-10; source 'Saltmarrow General Hospital, UB-04 itemized bill')
   UB-04 statement period 06/28/2026 to 07/02/2026. Rev 0120 room and board, FL47 total charges $4,920.00.
    $4,920.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 28–July 2, 2026: $4,920.00'  state=stated reason=None
== P5 UB-04 period with 'through'  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04 itemized bill')
   UB-04 statement period 06/09/2026 through 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.
    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00'  state=stated reason=None
== P6 UB-04 period with hyphen  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04 itemized bill')
   UB-04 statement period 06/09/2026 - 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.
    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00'  state=stated reason=None
== P7 statement + DOS label same sentence  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement')
   Statement date 03/01/2026, date of service 02/02/2026: office visit charge $275.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
== P8 ledger row DOS then posted, two-digit years  (record date 2026-06-15; source 'Fennimoor Spine Clinic, itemized ledger')
   06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00. 06/12/26 06/13/26 97110 Therapeutic exercise charge $95.00.
       $95.00 -> letter head: 'Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $95.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/12/26, 06/13/26) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== P9 statement period then a separately dated line  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04 itemized bill')
   UB-04 statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, service date 06/09/2026, FL47 total charges $2,105.00.
    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9, 2026: $2,105.00'  state=stated reason=None
== P10 'from X to Y' dates of service  (record date 2026-03-20; source 'Capital PT, billing statement')
   Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 therapeutic exercise, 9 units, charge $1,665.00.
    $1,665.00 -> letter head: 'Capital PT, billing statement (statement dated March 20, 2026; service date not stated): $1,665.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== T1 ledger table: DOS + posted columns  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   Itemized ledger
   DOS         Posted      CPT    Description            Charges    Balance
   06/10/2026  06/11/2026  97140  Manual therapy x1      $70.00     $70.00
   06/17/2026  06/18/2026  97110  Therapeutic exercise   $95.00     $165.00
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
      $165.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $165.00'  state=stated reason=None
== T2 ledger table: posted column first (r1 blocker)  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   Itemized ledger
   Posted      DOS         CPT    Description            Charges    Balance
   06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00     $70.00
   06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00     $165.00
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
      $165.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $165.00'  state=stated reason=None
== T3 CMS-1500, two dates of service joined by 'and' (r1 blocker)  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500')
   CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, $185.00, 1 unit; CPT 20610, $210.00, 1 unit. Item 28 TOTAL CHARGE $395.00. Item 29 AMOUNT PAID $0.00.
      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $185.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/24/2026, 07/08/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $210.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/24/2026, 07/08/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
      $395.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $395.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
        $0.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $0.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N1 posted-first ledger, uppercase header, pipes  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   POSTED     | SVC DATE   | CODE  | DESCRIPTION          | CHARGE
   06/11/2026 | 06/10/2026 | 97140 | Manual therapy x1    | $70.00
   06/18/2026 | 06/17/2026 | 97110 | Therapeutic exercise | $95.00
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
== N2 posted-first ledger, header 'Post Date / Date of Service'  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   Post Date    Date of Service   Code   Description             Amount
   06/11/2026   06/10/2026        97140  Manual therapy x1       $70.00
   06/18/2026   06/17/2026        97110  Therapeutic exercise    $95.00
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
== N3 posted-first rows, NO header  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00
   06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger (statement dated July 1, 2026; service date not stated): $70.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/11/2026, 06/10/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger (statement dated July 1, 2026; service date not stated): $95.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/18/2026, 06/17/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N4 posted-first, header uses generic 'Date' for the DOS column  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   Posted      Date        CPT    Description            Charges
   06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00
   06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
== N5 ledger with only a 'Trans Date' column (transaction date)  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   Trans Date   Code   Description             Charges
   06/11/2026   97140  Manual therapy x1       $70.00
   06/18/2026   97110  Therapeutic exercise    $95.00
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 11, 2026: $70.00'  state=stated reason=None
       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 18, 2026: $95.00'  state=stated reason=None
== N6 sentence ledger: 'Posted X for DOS Y'  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   Posted 06/11/2026 for DOS 06/10/2026: manual therapy $70.00. Posted 06/18/2026 for DOS 06/17/2026: therapeutic exercise $95.00.
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
== N7 sentence: date then 'posted' after it  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   06/11/2026 posted, DOS 06/10/2026, manual therapy $70.00.
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger (statement dated July 1, 2026; service date not stated): $70.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/11/2026, 06/10/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N8 CMS-1500 with per-line item 24A dates  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500')
   CMS-1500. Item 24A 06/24/2026 CPT 99204 $185.00. Item 24A 07/08/2026 CPT 20610 $210.00. Item 28 TOTAL CHARGE $395.00.
      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, June 24, 2026: $185.00'  state=stated reason=None
      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, July 8, 2026: $210.00'  state=stated reason=None
      $395.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $395.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N9 CMS-1500 'dates of service 06/24/2026, 07/08/2026' (comma list)  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500')
   Dates of service 06/24/2026, 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.
      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $185.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/24/2026, 07/08/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $210.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/24/2026, 07/08/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N10 CMS-1500 'from 06/24/2026 to 07/08/2026' (claim span, 2 discrete visits)  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500')
   CMS-1500 dates of service from 06/24/2026 to 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.
      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $185.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $210.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N11 CMS-1500 with DOI in the same sentence as a coded line  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500')
   Item 14 date of current injury 05/30/2026, CPT 99204 office visit $185.00.
      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, May 30, 2026: $185.00'  state=stated reason=None
== N12 CMS-1500 with patient DOB in the same sentence  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500')
   Patient DOB 03/15/1980, CPT 99204 office visit $185.00.
      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, March 15, 1980: $185.00'  state=stated reason=None
== N13 accident date leading a bill line  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement')
   Date of accident 01/09/2026, office visit charge $275.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, January 9, 2026: $275.00'  state=stated reason=None
== N14 ambiguous numeric, both readings before statement  (record date 2026-06-01; source 'Hobbleton Family Clinic, billing statement')
   Date of service 04/05/2026: office visit charge $275.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement (statement dated June 1, 2026; service date not stated): $275.00'  state=not_stated reason=ambiguous_numeric
              Step 3 note: The date written as 04/05/2026 can be read as month/day or day/month, and the record does not settle which. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N15 ambiguous numeric, one reading after statement (D-071 clarification)  (record date 2026-04-30; source 'Hobbleton Family Clinic, billing statement')
   Date of service 04/05/2026: office visit charge $275.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, April 5, 2026: $275.00'  state=stated reason=None
== N16 month-name date with no year  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement')
   Office visit on February 2: charge $275.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement (statement dated March 1, 2026; service date not stated): $275.00'  state=not_stated reason=no_year
              Step 3 note: The date February 2 states no year, which the code does not borrow from the statement. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N17 month-name period with year  (record date 2026-07-10; source 'Saltmarrow General Hospital, UB-04 itemized bill')
   Statement covers period June 28-July 2, 2026. Rev 0120 room and board $4,920.00.
    $4,920.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill (statement dated July 10, 2026; service date not stated): $4,920.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N18 'statement period' but prior-balance date in same sentence  (record date 2026-07-10; source 'Saltmarrow General Hospital, UB-04 itemized bill')
   Previous balance as of 05/31/2026 $100.00; Rev 0450 emergency room 06/09/2026 $2,105.00.
      $100.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill (statement dated July 10, 2026; service date not stated): $100.00'  state=not_stated reason=non_service_date
              Step 3 note: The only date near this line (05/31/2026) is a posting, statement or billing date, not a date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9, 2026: $2,105.00'  state=stated reason=None
== N19 payment-first sentence then charge  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement')
   Payment received 02/20/2026 $50.00, office visit charge $275.00.
       $50.00 -> letter head: 'Hobbleton Family Clinic, billing statement (statement dated March 1, 2026; service date not stated): $50.00'  state=not_stated reason=non_service_date
              Step 3 note: The only date near this line (02/20/2026) is a posting, statement or billing date, not a date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement (statement dated March 1, 2026; service date not stated): $275.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N20 UB-04 FL6 6-digit from/through  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04')
   FL6 statement covers period FROM 060926 THROUGH 061226. Rev 0450 emergency room FL47 $2,105.00.
    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 (statement dated June 19, 2026; service date not stated): $2,105.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N21 admit / discharge dates  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04')
   Admit 06/09/2026, discharge 06/12/2026, Rev 0120 room and board $4,920.00.
    $4,920.00 -> letter head: 'Saltmarrow General Hospital, UB-04 (statement dated June 19, 2026; service date not stated): $4,920.00'  state=not_stated reason=several_dates
              Step 3 note: This line or its bill states more than one date (06/09/2026, 06/12/2026) and the record does not say which one belongs to this charge. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== N22 date after the figure  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement')
   Office visit charge $275.00 on 02/02/2026.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
== N23 visit note (not a bill) with a fee, no date in sentence  (record date 2026-01-16; source 'Dr. Alvarez, primary care')
   Office visit level 3. Fee $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== N24 ledger: two posted dates then DOS in row, header names all  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   Billed       Posted      DOS         CPT    Charges
   06/12/2026   06/11/2026  06/10/2026  97140  $70.00
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
== N25 ISO dates in a posted-first ledger  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   Posted      DOS         CPT    Charges
   2026-06-11  2026-06-10  97140  $70.00
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:22:50.769Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.py",
 "content": "\"\"\"T-202 r2 paralegal probe B: non-service dates (birth date, injury/accident date, referral/order date, onset) sitting next to a charge,\nin bill and non-bill records, line and sentence layouts. Same shipped path as probe_r2.py (store.charge_service_date). SYNTHETIC text only.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, store  # noqa: E402\n\nPROBES = [\n    (\"B1 statement header line with DOI, then a dated charge row\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Patient: J. Roe   DOI: 01/09/2026\\n02/02/2026  99213  Office visit  $275.00\"),\n    (\"B2 header line with DOI, then an undated coded row\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Patient: J. Roe   DOI: 01/09/2026\\n99213  Office visit  $275.00\"),\n    (\"B3 'DOI 01/09/2026' in the same row as an undated coded charge\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"DOI 01/09/2026   99213   Office visit   $275.00\"),\n    (\"B4 sentence: 'Injury date 01/09/2026. Office visit 99213 $275.00.'\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Injury date 01/09/2026. Office visit 99213 $275.00.\"),\n    (\"B5 sentence: 'For injuries of 01/09/2026, office visit 99213 $275.00.'\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"For injuries of 01/09/2026, office visit 99213 $275.00.\"),\n    (\"B6 CMS-1500 flattened: DOB field then a coded line, one sentence\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"Item 3 patient birth date 03/15/1980; Item 24 CPT 99204 $185.00.\"),\n    (\"B7 CMS-1500 flattened: DOB with comma, coded line\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"Birth date 03/15/1980, CPT 99204 $185.00.\"),\n    (\"B8 non-bill follow-up note mentions the collision date and a fee\", \"Dr. Alvarez, primary care\", \"2026-01-16\",\n     \"Follow-up for collision of 01/09/2026, visit charge $150.00.\"),\n    (\"B9 MRI report (non-bill) with ordered date in the charge sentence\", \"Riverside Imaging, MRI report\", \"2026-02-20\",\n     \"Ordered 02/10/2026, MRI cervical spine charge $2,150.00.\"),\n    (\"B10 bill: 'Referral dated 02/10/2026, MRI charge $2,150.00'\", \"Riverside Imaging, billing statement\", \"2026-03-01\",\n     \"Referral dated 02/10/2026, MRI charge $2,150.00.\"),\n    (\"B11 bill: 'Onset 01/09/2026, 97110 therapeutic exercise $95.00'\", \"Capital PT, billing statement\", \"2026-03-20\",\n     \"Onset 01/09/2026, 97110 therapeutic exercise $95.00.\"),\n    (\"B12 bill: 'Date of accident 01/19/2026 per intake; 99213 $275.00'\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Date of accident 01/19/2026 per intake, 99213 office visit $275.00.\"),\n]\n\nfor label, src, rd, ex in PROBES:\n    print(f\"== {label}  (record date {rd}; source '{src}'; billing_document={AM.billing_document(src, ex)})\")\n    print(\"   \" + ex.replace(\"\\n\", \"\\n   \"))\n    rec = {\"id\": \"r1\", \"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex, \"text\": ex}\n    for a in AM.find_amounts(ex):\n        if a.get(\"cents\") is None:\n            continue\n        item = {\"excerpt\": ex, \"value_cents\": a[\"cents\"], \"raw\": a[\"raw\"], \"excerpt_start\": 0}\n        d = store.charge_service_date(item, rec, a[\"start\"])\n        line = f\"{src}, {d['text']}\" if d[\"state\"] == \"stated\" else f\"{src} {d['text']}\"\n        print(f\"   {a['raw']:>10} -> letter head: '{line}: {a['raw']}'  state={d['state']} reason={d['reason']}\")\n        if d[\"confirm_note\"]:\n            print(f\"              Step 3 note: {d['confirm_note']}\")\n"
}
````

### User / tool · 2026-11-03T00:22:50.869Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:22:54.311Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr2_986fc55 > artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.out 2>&1; cat artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.out",
 "description": "Run non-service-date probes"
}
````

### User / tool · 2026-11-03T00:22:54.626Z

**tool result**
````
== B1 statement header line with DOI, then a dated charge row  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
   Patient: J. Roe   DOI: 01/09/2026
   02/02/2026  99213  Office visit  $275.00
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
== B2 header line with DOI, then an undated coded row  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
   Patient: J. Roe   DOI: 01/09/2026
   99213  Office visit  $275.00
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement (statement dated March 1, 2026; service date not stated): $275.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== B3 'DOI 01/09/2026' in the same row as an undated coded charge  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
   DOI 01/09/2026   99213   Office visit   $275.00
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, January 9, 2026: $275.00'  state=stated reason=None
== B4 sentence: 'Injury date 01/09/2026. Office visit 99213 $275.00.'  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
   Injury date 01/09/2026. Office visit 99213 $275.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement (statement dated March 1, 2026; service date not stated): $275.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== B5 sentence: 'For injuries of 01/09/2026, office visit 99213 $275.00.'  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
   For injuries of 01/09/2026, office visit 99213 $275.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, January 9, 2026: $275.00'  state=stated reason=None
== B6 CMS-1500 flattened: DOB field then a coded line, one sentence  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
   Item 3 patient birth date 03/15/1980; Item 24 CPT 99204 $185.00.
      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $185.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
== B7 CMS-1500 flattened: DOB with comma, coded line  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
   Birth date 03/15/1980, CPT 99204 $185.00.
      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, March 15, 1980: $185.00'  state=stated reason=None
== B8 non-bill follow-up note mentions the collision date and a fee  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; billing_document=False)
   Follow-up for collision of 01/09/2026, visit charge $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== B9 MRI report (non-bill) with ordered date in the charge sentence  (record date 2026-02-20; source 'Riverside Imaging, MRI report'; billing_document=False)
   Ordered 02/10/2026, MRI cervical spine charge $2,150.00.
    $2,150.00 -> letter head: 'Riverside Imaging, MRI report, February 10, 2026: $2,150.00'  state=stated reason=None
== B10 bill: 'Referral dated 02/10/2026, MRI charge $2,150.00'  (record date 2026-03-01; source 'Riverside Imaging, billing statement'; billing_document=True)
   Referral dated 02/10/2026, MRI charge $2,150.00.
    $2,150.00 -> letter head: 'Riverside Imaging, billing statement, February 10, 2026: $2,150.00'  state=stated reason=None
== B11 bill: 'Onset 01/09/2026, 97110 therapeutic exercise $95.00'  (record date 2026-03-20; source 'Capital PT, billing statement'; billing_document=True)
   Onset 01/09/2026, 97110 therapeutic exercise $95.00.
       $95.00 -> letter head: 'Capital PT, billing statement, January 9, 2026: $95.00'  state=stated reason=None
== B12 bill: 'Date of accident 01/19/2026 per intake; 99213 $275.00'  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
   Date of accident 01/19/2026 per intake, 99213 office visit $275.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, January 19, 2026: $275.00'  state=stated reason=None
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:23:04.891Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls $S/t202 | head -3; grep -c \"def charge_service_dates\" $S/t202/app/backend/store.py; grep -n \"T-202\\|f0921e4\" $S/t202/app/backend/store.py | head -3",
 "description": "Check r1 archive of f0921e4 exists"
}
````

### User / tool · 2026-11-03T00:23:05.013Z

**tool result**
````
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
1
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:23:10.651Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/probe_r2b_prev.py",
 "content": "\"\"\"Same probe B texts on an older archive (f0921e4, T-202 r1) through store.charge_service_dates (tuple API), to see whether the\nnon-service-date pickup is new in r2 or carried from r1. Pre-T-202 (a44cfa7) the letter printed the record's date for every charge.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_r2b_prev.py <archive_root>\n\"\"\"\nimport os\nimport runpy\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, export, store  # noqa: E402\n\nhere = os.path.dirname(os.path.abspath(__file__))\nsrc = open(os.path.join(here, \"probe_r2b.py\")).read()\nPROBES = []\nexec(src.split(\"PROBES = [\", 1)[1].split(\"\\n]\\n\", 1)[0].join([\"PROBES = [\", \"\\n]\\n\"]))\nfor label, s, rd, ex in PROBES:\n    print(f\"== {label}  (record date {rd})\")\n    rec = {\"id\": \"r1\", \"n\": 1, \"source\": s, \"date_iso\": rd, \"excerpt\": ex, \"text\": ex}\n    for a in AM.find_amounts(ex):\n        if a.get(\"cents\") is None:\n            continue\n        first, last = store.charge_service_dates({\"excerpt\": ex, \"value_cents\": a[\"cents\"]}, rec, a[\"start\"])\n        print(f\"   {a['raw']:>10} -> {export._date_range(first, last) if first else '(not stated)'}\")\n"
}
````

### User / tool · 2026-11-03T00:23:10.920Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/probe_r2b_prev.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:23:14.883Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_r2b_prev.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 > artifacts/review-evidence/T-202-paralegal-r2/probe_r2b_on_f0921e4.out 2>&1; cat artifacts/review-evidence/T-202-paralegal-r2/probe_r2b_on_f0921e4.out",
 "description": "Run probe B on the r1 archive for comparison"
}
````

### User / tool · 2026-11-03T00:23:15.225Z

**tool result**
````
== B1 statement header line with DOI, then a dated charge row  (record date 2026-03-01)
      $275.00 -> February 2, 2026
== B2 header line with DOI, then an undated coded row  (record date 2026-03-01)
      $275.00 -> (not stated)
== B3 'DOI 01/09/2026' in the same row as an undated coded charge  (record date 2026-03-01)
      $275.00 -> January 9, 2026
== B4 sentence: 'Injury date 01/09/2026. Office visit 99213 $275.00.'  (record date 2026-03-01)
      $275.00 -> (not stated)
== B5 sentence: 'For injuries of 01/09/2026, office visit 99213 $275.00.'  (record date 2026-03-01)
      $275.00 -> January 9, 2026
== B6 CMS-1500 flattened: DOB field then a coded line, one sentence  (record date 2026-07-14)
      $185.00 -> (not stated)
== B7 CMS-1500 flattened: DOB with comma, coded line  (record date 2026-07-14)
      $185.00 -> March 15, 1980
== B8 non-bill follow-up note mentions the collision date and a fee  (record date 2026-01-16)
      $150.00 -> January 9, 2026
== B9 MRI report (non-bill) with ordered date in the charge sentence  (record date 2026-02-20)
    $2,150.00 -> February 10, 2026
== B10 bill: 'Referral dated 02/10/2026, MRI charge $2,150.00'  (record date 2026-03-01)
    $2,150.00 -> February 10, 2026
== B11 bill: 'Onset 01/09/2026, 97110 therapeutic exercise $95.00'  (record date 2026-03-20)
       $95.00 -> January 9, 2026
== B12 bill: 'Date of accident 01/19/2026 per intake; 99213 $275.00'  (record date 2026-03-01)
      $275.00 -> January 19, 2026
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:23:25.311Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 986fc55:evals/letter_check.py | sed -n 1,34p; git show 986fc55:evals/letter_check.py | sed -n 140,362p",
 "description": "Read the new letter_check date check"
}
````

### User / tool · 2026-11-03T00:23:25.466Z

**tool result**
````
"""Letter-level eval (T-139; D-019, R-CH-7, R-EX-8): no dollar amount reaches the carrier letter except in the BILLED CHARGES section.

For every golden case, the sample and every library packet, on the FIXTURE backend (recorded model answers; no network):
  run the pipeline on a scratch database, accept every item that code lets her accept (a refusal is counted, not hidden), export the letter in both styles;
  then a variant where every charge is dismissed.
Violations (all must be zero):
  - a currency string in the letter outside the BILLED CHARGES section (the treatment entries and the TREATMENT SUMMARY paragraph);
  - in the BILLED CHARGES section, a currency string that is not an accepted charge or the total line (R-EX-8: exactly 'Billed charges accepted from these records: $X');
  - after dismissing every charge: any currency string anywhere in the letter, or a provider whose charge was dismissed under BILLS TO REQUEST in the notes.
  - money written WITHOUT a '$' anywhere outside the accepted charge lines ('TOTAL CHARGE 49100', 'AMOUNT PAID 0 00', '24F 25500'): T-139 round 2.
T-139 round 4: the audit uses the SAME detector as the charge-text hold and the export gate (app/backend/money.py), so the three cannot diverge: a wording one holds, all hold.
The eval's independent value is the walk (every case, every style, charges dismissed) and the structure checks (charges section, total line, bills to request), not a
second regex. It also reports the export gate: a case whose letter the gate blocks is a violation.
D-071 / T-202: a third variant counts every countable amount (the paralegal's D-064 "Count this charge", with the named confirms) after accepting everything, and every dated charge
line of every letter is checked against THAT line's own quote (`charge_date_violations`, round 2): the printed date (a day or a range, whole) must be the one certain reading of the date the
quote states, or, when the quote states none, of the one period the bill states before it; a date readable two ways, with a two-digit year or no year, a quote with several dates and no
service-date column heading, or a bill that states several periods may print nothing but the T-200 form '(statement dated X; service date not stated)', X the record's date. The check has
its own date scanner and shares no code with the production parser (app/backend/service_date.py), so a parser bug cannot hide itself.
Pure check: `violations(letter, accepted_cents)`; the pipeline walk is `letters_for(text)`.

    python -m evals.letter_check            prints one line per case and exits 1 on any violation
"""
import contextlib
import json
import pathlib
import re
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD, LIB = ROOT / "evals" / "golden", ROOT / "evals" / "library"
CHARGES, TOTAL = "BILLED CHARGES", "Billed charges accepted from these records: "
STYLES = (None, "oneline")

def _iso(txt):
    from datetime import datetime
    return datetime.strptime(" ".join(txt.replace(",", " ").split()), "%B %d %Y").date().isoformat()


def _head_dates(head: str):
    """('range'|'one', first ISO, last ISO or None) from the end of a charge header, or ('statement', ISO, None) / ('none', None, None) for the T-200 forms, or None when unreadable."""
    m = _STATEMENT_FORM.search(head)
    if m:
        return "statement", _iso(m.group(1)), None
    if _NO_DATE_FORM.search(head):
        return "none", None, None
    for rx, kind in _HEAD_DATES:
        m = rx.search(head)
        if not m:
            continue
        g = m.groups()
        if kind == "full":
            return "range", _iso(g[0]), _iso(g[1])
        if kind == "month":
            return "range", _iso(f"{g[0]}, {g[2]}"), _iso(f"{g[1]}, {g[2]}")
        if kind == "day":
            return "range", _iso(f"{g[0]}, {g[2]}"), _iso(f"{g[0].split()[0]} {g[1]}, {g[2]}")
        return "one", _iso(g[0]), None
    return None


def charge_lines(letter: str) -> list:
    """[(header, quote)] of the BILLED CHARGES section, by structure (a header ends ': $X.XX'; the next line is its Source line)."""
    from app.backend import export
    _, tail = export.split_letter(letter)
    out = []
    for i, line in enumerate(tail):
        if re.search(r": \$[\d,]+\.\d\d$", line) and not line.startswith(TOTAL) and i + 1 < len(tail):
            q = tail[i + 1]
            out.append((line, q[q.index('"') + 1:q.rindex('"')] if '"' in q else q))
    return out


# ---- D-071 amendment: each printed date against THAT line's own quote. Deliberately a second, simple reading of the bill text that shares no code with the production parser
# (app/backend/service_date.py): its own small scanner, its own rules, enumerating every reading a written date allows.
_MONTHS = {m: i + 1 for i, m in enumerate("jan feb mar apr may jun jul aug sep oct nov dec".split())}
_W = (r"(?P<per>(?P<pm1>[A-Za-z]{3,9})\.? (?P<pd1>\d{1,2})(?:st|nd|rd|th)? ?[-\u2013] ?(?:(?P<pm2>[A-Za-z]{3,9})\.? )?(?P<pd2>\d{1,2})(?:st|nd|rd|th)?, ?(?P<py>\d{4}))"
      r"|(?P<iso>\d{4}-\d{1,2}-\d{1,2})|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4})"
      r"|(?P<mdy>(?P<m>[A-Za-z]{3,9})\.? (?P<d>\d{1,2})(?:st|nd|rd|th)?(?:, ?(?P<y>\d{4}))?)|(?P<dmy>(?P<d2>\d{1,2})(?:st|nd|rd|th)? (?:of )?(?P<m2>[A-Za-z]{3,9})\.?,? (?P<y2>\d{4}))"
      r"|(?P<yearless>\d{1,2}/\d{1,2})(?![\d/])")
_WRITTEN = re.compile(r"(?<![\w/$])(?:" + _W + r")(?![\w/])")
_JOINERS = re.compile(r"^ ?(?:-|\u2013|to|through|thru|until) ?$", re.IGNORECASE)
_LISTERS = re.compile(r"^ ?(?:,|;|&|and|or) ?$", re.IGNORECASE)
_BILLING_WORD = re.compile(r"(?:statement|stmt|invoice|billing|billed|posted|paid|received|payment|processed|mailed|due|balance|printed|issued)(?: date| dated| on| of)?[ :#]*$", re.IGNORECASE)
_PERIOD_WORD = re.compile(r"(?:statement period|billing period|service period|dates? of service|\bdos\b|service dates?|run of|date of the run)\W{0,6}$", re.IGNORECASE)
_BILL_WORD = re.compile(r"statement|\bbill|invoice|ledger|ub-?04|cms-?1500|itemi[sz]ed|\baccount\b|claim form", re.IGNORECASE)


def _month(name):
    return _MONTHS.get(name.lower()[:3])


def _real(y, m, d):
    from datetime import date
    try:
        return date(y, m, d).isoformat()
    except (TypeError, ValueError):
        return None


def _written(text):
    """[{start, end, options: [(first, last or None)], flaw}] for each date written in `text`. `options` lists EVERY reading the writing allows (empty when it allows none that is
    certain: a two-digit year, no year, a month that is not one); a pair 'A to B' is one item whose options are the combinations with the end after the start."""
    toks = []
    for m in _WRITTEN.finditer(text):
        g, opts, flaw = m.groupdict(), [], None
        if g["per"]:
            m1, m2 = _month(g["pm1"]), _month(g["pm2"] or g["pm1"])
            a, b = _real(int(g["py"]), m1, int(g["pd1"])), _real(int(g["py"]), m2, int(g["pd2"]))
            opts = [(a, b)] if a and b and b > a else []
            toks.append({"start": m.start(), "end": m.end(), "opts": opts, "flaw": None if opts else "bad", "pair": True})
            continue
        if g["iso"]:
            y, mo, d = (int(x) for x in g["iso"].split("-"))
            opts = [x for x in [_real(y, mo, d)] if x]
        elif g["num"]:
            a, b, y = re.split(r"[/.-]", g["num"])
            if len(y) != 4:
                flaw = "two-digit year"
            else:
                opts = sorted({x for x in (_real(int(y), int(a), int(b)), _real(int(y), int(b), int(a))) if x})
        elif g["mdy"]:
            if not _month(g["m"]):
                continue
            if g["y"]:
                opts = [x for x in [_real(int(g["y"]), _month(g["m"]), int(g["d"]))] if x]
            else:
                flaw = "no year"
        elif g["dmy"]:
            if not _month(g["m2"]):
                continue
            opts = [x for x in [_real(int(g["y2"]), _month(g["m2"]), int(g["d2"]))] if x]
        else:
            flaw = "no year"
        toks.append({"start": m.start(), "end": m.end(), "opts": [(o, None) for o in opts], "flaw": flaw or (None if opts else "bad"), "pair": False})
    units, k = [], 0
    while k < len(toks):
        t = toks[k]
        if k + 1 < len(toks) and not t["pair"] and not toks[k + 1]["pair"] and _JOINERS.match(text[t["end"]:toks[k + 1]["start"]]):
            u = toks[k + 1]
            combos = [(a, b) for (a, _) in t["opts"] for (b, _) in u["opts"] if b > a]
            units.append({"start": t["start"], "end": u["end"], "opts": combos, "flaw": t["flaw"] or u["flaw"] or (None if combos else "bad")})
            k += 2
        else:
            units.append(dict(t))
            k += 1
    return units


def _readings(unit, ref):
    """The readings left for a written date: those not after the record's own date when the writing allows several (a service does not follow its statement)."""
    opts = unit["opts"]
    if len(opts) > 1 and ref:
        opts = [o for o in opts if (o[1] or o[0]) <= ref]
    return opts


def _own_dates(text):
    return [u for u in _written(text) if not _BILLING_WORD.search(text[max(0, u["start"] - 30):u["start"]])]


def _period_dates(before):
    """The dates the bill states for its services before the quote: those led by 'statement period', 'dates of service', 'run of' ... and the dates listed after them."""
    us = _written(before)
    out = []
    for k, u in enumerate(us):
        if _PERIOD_WORD.search(before[max(0, u["start"] - 40):u["start"]]):
            out.append(u)
            j = k
            while j + 1 < len(us) and _LISTERS.match(before[us[j]["end"]:us[j + 1]["start"]]):
                out.append(us[j + 1])
                j += 1
    return out


def _dos_column(ex, quote, printed_first):
    """For a quote that holds several dates: the heading (nearest digit-free line above the quote's line, split at 2+ spaces) over the printed date's column, or ''."""
    qi = ex.find(quote)
    if qi < 0:
        return ""
    ls = ex.rfind("\n", 0, qi) + 1
    line = ex[ls:qi + len(quote)]
    want = {printed_first}
    for u in _written(line):
        if any(o[0] in want for o in u["opts"]):
            col = u["start"]
            for above in reversed(ex[:max(ls - 1, 0)].split("\n")[-40:]):
                if not above.strip():
                    return ""
                if re.search(r"\d", above):
                    continue
                heads = [(m.start(), m.group(0)) for m in re.finditer(r"\S+(?: \S+)*", above)]
                return min(heads, key=lambda h: abs(h[0] - col))[1] if heads else ""
    return ""


def charge_date_violations(letter: str, records) -> list:
    """D-071 amendment: every charge line's printed date must be certain from THAT line's own quote (plus, for a quote with no date, the one period the bill states before it).
    `records`: the case's [{n, source, date_iso, excerpt}]. Rules, per line:
      - the quote states one written date (or one period) -> the line prints exactly that, with its end, and only when the writing has one reading (a numeric date both ways, a two-digit
        year or a year-less date prints nothing); a statement, billing or due date in the quote is not a service date;
      - the quote states several dates -> the line prints one only if the column heading over it names the date of service;
      - the quote states none, in a bill -> the bill's one stated period (statement period, dates of service, run of ...), whole; several stated dates, or none -> the not-stated form
        '(statement dated X; service date not stated)' with X the record's date; in a visit note (not a bill) -> the note's own date.
    The not-stated form is always allowed when the record has a date to print as X."""
    norm = lambda t: " ".join(str(t).split())
    out = []
    for head, quote in charge_lines(letter):
        parsed = _head_dates(re.sub(r": \$[\d,]+\.\d\d$", "", head))
        recs = [r for r in records if norm(quote) and norm(quote) in norm(r["excerpt"])]
        if parsed is None:
            out.append(f"charge line has no readable date form: {head}")
            continue
        if not recs:
            out.append(f"charge line's quote is in no record: {head}")
            continue
        kind, first, last = parsed
        problems = []
        for r in recs:
            ex, rd = r["excerpt"], r.get("date_iso")
            bill = bool(_BILL_WORD.search(r.get("source") or "") or _BILL_WORD.search(ex[:60]))
            n_ex, n_q = norm(ex), norm(quote)
            before = n_ex[:n_ex.index(n_q)]
            own = _own_dates(n_q)
            if kind in ("statement", "none"):
                if first and first != rd:
                    problems.append("the statement date is not the record's date")
                elif not bill and rd:
                    problems.append("a visit note's line must carry the note's date")
                continue
            if own:
                if len(own) > 1:
                    col = _dos_column(ex, quote, first)
                    if not re.search(r"dos|service|svc", col, re.IGNORECASE) or re.search(r"post|statement|bill", col, re.IGNORECASE):
                        problems.append(f"the quote states several dates and no column heading names the date of service (heading '{col}')")
                        continue
                    own = [u for u in own if any(o[0] == first for o in u["opts"])]
                    if not own:
                        problems.append("the printed date is in none of the quote's dates")
                        continue
                want = _readings(own[0], rd)
            elif bill:
                units = _period_dates(before)
                if len(units) != 1:
                    problems.append("the bill states " + ("no" if not units else "several") + " dates of service and the line prints one")
                    continue
                want = _readings(units[0], rd)
            else:
                want = [(rd, None)] if rd else []
            if len(want) != 1:
                problems.append("the written date has no single certain reading")
            elif (first, last) != want[0]:
                problems.append(f"the line's own text gives {want[0][0]}" + (f" to {want[0][1]}" if want[0][1] else ""))
        if len(problems) == len(recs):
            out.append(f"charge line's date is not certain from its quote ({'; '.join(sorted(set(problems)))}): {head}")
    return out
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:23:40.445Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/probe_eval_teeth_r2.py",
 "content": "\"\"\"T-202 r2 paralegal: does evals/letter_check.charge_date_violations (986fc55) catch a wrong-but-stated date?\nr1 shapes (posting date printed as DOS; CMS-1500 'and' list -> one claim date) and r2 shapes (birth date, accident date, collision date in a visit note,\norder date in an imaging report printed as the date of service), each next to the correct form as a control. SYNTHETIC text only.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_eval_teeth_r2.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom evals import letter_check as LC  # noqa: E402\n\nT2 = (\"Itemized ledger\\nPosted      DOS         CPT    Description            Charges    Balance\\n\"\n      \"06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00     $70.00\")\nT3 = \"CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, $185.00, 1 unit; CPT 20610, $210.00, 1 unit.\"\nB7 = \"Birth date 03/15/1980, CPT 99204 $185.00.\"\nB8 = \"Follow-up for collision of 01/09/2026, visit charge $150.00.\"\nB9 = \"Ordered 02/10/2026, MRI cervical spine charge $2,150.00.\"\nB12 = \"Date of accident 01/19/2026 per intake, 99213 office visit $275.00.\"\n\n\ndef letter(head, fig, quote):\n    return f\"BILLED CHARGES\\n\\n{head}: {fig}\\nSource [Ex. __ / Bates __]: \\\"{quote}\\\"\\n\\nBilled charges accepted from these records: {fig}\"\n\n\ndef rec(src, rd, ex):\n    return [{\"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex}]\n\n\nL = \"Larkspur Hollow Physical Therapy, itemized ledger\"\nW = \"Wardlaw Orthopedics, CMS-1500\"\ncases = [\n    (\"T2 posting date printed as DOS (wrong)\", rec(L, \"2026-07-01\", T2), letter(f\"{L}, June 11, 2026\", \"$70.00\", \"06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00\")),\n    (\"T2 DOS printed (right)\", rec(L, \"2026-07-01\", T2), letter(f\"{L}, June 10, 2026\", \"$70.00\", \"06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00\")),\n    (\"T3 injection line dated with the other claim date (wrong)\", rec(W, \"2026-07-14\", T3), letter(f\"{W}, June 24, 2026\", \"$210.00\", \"CPT 20610, $210.00, 1 unit\")),\n    (\"T3 not-stated form (right)\", rec(W, \"2026-07-14\", T3), letter(f\"{W} (statement dated July 14, 2026; service date not stated)\", \"$210.00\", \"CPT 20610, $210.00, 1 unit\")),\n    (\"B7 birth date printed as DOS (what 986fc55 prints)\", rec(W, \"2026-07-14\", B7), letter(f\"{W}, March 15, 1980\", \"$185.00\", B7.rstrip(\".\"))),\n    (\"B8 collision date printed for a 01/16 visit note's charge (what 986fc55 prints)\", rec(\"Dr. Alvarez, primary care\", \"2026-01-16\", B8),\n     letter(\"Dr. Alvarez, primary care, January 9, 2026\", \"$150.00\", B8.rstrip(\".\"))),\n    (\"B9 order date printed for a 02/20 MRI report's charge (what 986fc55 prints)\", rec(\"Riverside Imaging, MRI report\", \"2026-02-20\", B9),\n     letter(\"Riverside Imaging, MRI report, February 10, 2026\", \"$2,150.00\", B9.rstrip(\".\"))),\n    (\"B12 intake accident date printed as DOS (what 986fc55 prints)\", rec(\"Hobbleton Family Clinic, billing statement\", \"2026-03-01\", B12),\n     letter(\"Hobbleton Family Clinic, billing statement, January 19, 2026\", \"$275.00\", B12.rstrip(\".\"))),\n]\nfor label, recs, txt in cases:\n    print(f\"== {label}\\n   violations: {LC.charge_date_violations(txt, recs)}\")\n"
}
````

### User / tool · 2026-11-03T00:23:40.587Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/probe_eval_teeth_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:23:44.625Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_eval_teeth_r2.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr2_986fc55 > artifacts/review-evidence/T-202-paralegal-r2/probe_eval_teeth_r2.out 2>&1; cat artifacts/review-evidence/T-202-paralegal-r2/probe_eval_teeth_r2.out",
 "description": "Test letter_check against wrong-date letters"
}
````

### User / tool · 2026-11-03T00:23:44.890Z

**tool result**
````
== T2 posting date printed as DOS (wrong)
   violations: ["charge line's date is not certain from its quote (the quote states several dates and no column heading names the date of service (heading 'Posted')): Larkspur Hollow Physical Therapy, itemized ledger, June 11, 2026: $70.00"]
== T2 DOS printed (right)
   violations: []
== T3 injection line dated with the other claim date (wrong)
   violations: ["charge line's date is not certain from its quote (the bill states several dates of service and the line prints one): Wardlaw Orthopedics, CMS-1500, June 24, 2026: $210.00"]
== T3 not-stated form (right)
   violations: []
== B7 birth date printed as DOS (what 986fc55 prints)
   violations: []
== B8 collision date printed for a 01/16 visit note's charge (what 986fc55 prints)
   violations: []
== B9 order date printed for a 02/20 MRI report's charge (what 986fc55 prints)
   violations: []
== B12 intake accident date printed as DOS (what 986fc55 prints)
   violations: []
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:23:48.529Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; lsof -iTCP:7976 -sTCP:LISTEN -nP; echo \"exit $?\"; ls artifacts/review-evidence/T-202-paralegal/db",
 "description": "Check port 7976 free"
}
````

### User / tool · 2026-11-03T00:23:48.776Z

**tool result**
````
exit 1
zlayt.db
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:23:54.302Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; mkdir -p artifacts/review-evidence/T-202-paralegal-r2/db; env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/db/zlayt.db PORT=7976 HOST=127.0.0.1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr2_986fc55 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/server.log 2>&1",
 "description": "Start archive app on port 7976 in demo/fixture mode",
 "run_in_background": true
}
````

### User / tool · 2026-11-03T00:23:54.387Z

**tool result**
````
Command running in background with ID: ba5bo55h3. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/ba5bo55h3.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:23:56.440Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; for i in 1 2 3 4 5 6 7 8 9 10; do curl -s -o /dev/null -w \"%{http_code}\" http://127.0.0.1:7976/api/health && break; /bin/sleep 1; done; echo; curl -s http://127.0.0.1:7976/api/health; echo; lsof -iTCP:7976 -sTCP:LISTEN -nP",
 "description": "Wait for server and show health and PID"
}
````

### User / tool · 2026-11-03T00:23:56.737Z

**tool result**
````
200
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  49534 arsis    9u  IPv4 0x7836e61d64b7dc56      0t0  TCP 127.0.0.1:7976 (LISTEN)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:24:00.596Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; sed -n 80,200p artifacts/review-evidence/T-202-paralegal/p01_cases.py",
 "description": "Read rest of case driver script"
}
````

### User / tool · 2026-11-03T00:24:00.727Z

**tool result**
````
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:24:03.275Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; D=artifacts/review-evidence/T-202-paralegal-r2; cp artifacts/review-evidence/T-202-paralegal/h.py $D/h.py && cp artifacts/review-evidence/T-202-paralegal/p01_cases.py $D/p01_cases.py && grep -n \"7972\\|T-200 paralegal\\|f0921e4\" $D/h.py $D/p01_cases.py",
 "description": "Copy helper and case driver into r2 evidence dir"
}
````

### User / tool · 2026-11-03T00:24:03.412Z

**tool result**
````
artifacts/review-evidence/T-202-paralegal-r2/p01_cases.py:1:"""T-202 paralegal: f0921e4 archive, demo/fixture backend, local mode, port 7972.
artifacts/review-evidence/T-202-paralegal-r2/h.py:1:"""T-200 paralegal review helper (copied from T-181 r2): persistent Chromium profile on the archive app (bd72d5b, demo/fixture, local mode, port 7963).
artifacts/review-evidence/T-202-paralegal-r2/h.py:11:BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7972")  # T-202: f0921e4 archive, port 7972
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:24:05.704Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/h.py",
 "old_string": "BASE = os.environ.get(\"T181_BASE\", \"http://127.0.0.1:7972\")  # T-202: f0921e4 archive, port 7972",
 "new_string": "BASE = os.environ.get(\"T181_BASE\", \"http://127.0.0.1:7976\")  # T-202 r2: 986fc55 archive, port 7976"
}
````

### User / tool · 2026-11-03T00:24:05.863Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/h.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:24:07.165Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/p01_cases.py",
 "old_string": "\"\"\"T-202 paralegal: f0921e4 archive, demo/fixture backend, local mode, port 7972.",
 "new_string": "\"\"\"T-202 r2 paralegal (copied from r1): 986fc55 archive, demo/fixture backend, local mode, port 7976."
}
````

### User / tool · 2026-11-03T00:24:07.304Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/p01_cases.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:24:09.845Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/h.py artifacts/review-evidence/T-202-paralegal-r2/p01_cases.py > artifacts/review-evidence/T-202-paralegal-r2/p01.out 2>&1; echo exit $?; grep -n \"draft took\\|done in\\|ERRORS\\|Error\\|Timeout\" artifacts/review-evidence/T-202-paralegal-r2/p01.out | head -30",
 "description": "Drive the four cases through the UI and export letters",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T00:25:06.477Z

**tool result**
````
exit 0
2:[sample] draft took 2.3 s
85:[sample] done in 15.7 s
87:[case_09] draft took 2.5 s
147:[case_09] done in 8.1 s
148:[lib14] draft took 2.4 s
226:[lib14] done in 13.1 s
227:[lib10] draft took 2.4 s
323:[lib10] done in 19.2 s
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:25:08.027Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; D=artifacts/review-evidence/T-202-paralegal-r2; grep -n \"s3 item\" $D/p01.out | cut -c1-600",
 "description": "Show Step 3 card texts logged"
}
````

### User / tool · 2026-11-03T00:25:08.150Z

**tool result**
````
23:[sample] s3 item=a1 boxes=[] :: Charge / Central ER discharge summary · January 9, 2026 /  / $6,240.00 /  / Written in the record as $6,240. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
25:[sample] s3 item=a4 boxes=[] :: Charge / Austin Imaging, cervical MRI · May 29, 2026 /  / $2,150.00 /  / Written in the record as $2,150. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
27:[sample] s3 item=a2 boxes=[] :: Never counted / Capital PT, initial evaluation · January 23, 2026 /  / $185 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill total.
29:[sample] s3 item=a3 boxes=[] :: Never counted / Capital PT, visit 8 · February 20, 2026 /  / Not a money amount: missing 3 days of work /  / This figure is not a bill (for example a damages or settlement figure), so it is not added to the total. /  / Either way, it is never added to the bill total.
95:[case_09] s3 item=a1 boxes=[] :: Charge / Hobbleton Family Clinic, billing statement · March 1, 2026 /  / $275.00 /  / Written in the record as $275. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
161:[lib14] s3 item=a1 boxes=[] :: Charge / Orrin Mere Regional ED · September 14, 2026 /  / $2,960.00 /  / Written in the record as $2,960. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
163:[lib14] s3 item=a2 boxes=[] :: Charge / Tarnwick Fire-Rescue, ambulance invoice · November 12, 2026 /  / $1,380.00 /  / Written in the record as $1,380.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
165:[lib14] s3 item=a4 boxes=[] :: Charge / Tarnwick Fire-Rescue, ambulance invoice · November 12, 2026 /  / $187.05 /  / Written in the record as $187.05. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
167:[lib14] s3 item=a3 boxes=[] :: Never counted / Tarnwick Fire-Rescue, ambulance invoice · November 12, 2026 /  / $21.50 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill total.
169:[lib14] s3 item=a5 boxes=['check-compare'] :: Never counted / Tarnwick Fire-Rescue, ambulance invoice · November 12, 2026 /  / $1,567.05 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
240:[lib10] s3 item=a2 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $4,920.00 /  / Written in the record as $4,920.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
242:[lib10] s3 item=a3 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $2,105.00 /  / Written in the record as $2,105.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
244:[lib10] s3 item=a4 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $386.50 /  / Written in the record as $386.50. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
246:[lib10] s3 item=a5 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $712.00 /  / Written in the record as $712.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
248:[lib10] s3 item=a1 boxes=[] :: Never counted / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $1,640.00 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill total.
250:[lib10] s3 item=a6 boxes=['check-compare'] :: Never counted / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $8,123.50 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
252:[lib10] s3 item=a7 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · July 3, 2026 /  / $8,023.50 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
254:[lib10] s3 item=a8 boxes=[] :: Never counted / Quoinmere Mutual Health Plan, EOB · July 3, 2026 /  / $3,610.00 /  / Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges. /  / Either way, it is never added to the bill total.
256:[lib10] s3 item=a9 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · July 3, 2026 /  / $4,413.50 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
258:[lib10] s3 item=a10 boxes=[] :: Never counted / Quoinmere Mutual Health Plan, EOB · July 3, 2026 /  / $3,530.80 /  / Payment: money received, not a charge. /  / Either way, it is never added to the bill total.
260:[lib10] s3 item=a11 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · July 3, 2026 /  / $882.70 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:25:10.586Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; D=artifacts/review-evidence/T-202-paralegal-r2; for c in sample case_09 lib14 lib10; do echo \"=== $c\"; awk '/BILLED CHARGES/{f=1} f' $D/ui-$c-letter.txt; done",
 "description": "Show BILLED CHARGES sections of the four UI letters"
}
````

### User / tool · 2026-11-03T00:25:10.747Z

**tool result**
````
=== sample
BILLED CHARGES

Central ER discharge summary, January 9, 2026: $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240."
Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
Source [Ex. __ / Bates __]: "Charge: $2,150."

Billed charges accepted from these records: $8,390.00
=== case_09
BILLED CHARGES

Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00
Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."

Billed charges accepted from these records: $275.00
=== lib14
BILLED CHARGES

Orrin Mere Regional ED, September 14, 2026: $2,960.00
Source [Ex. __ / Bates __]: "ED charge: $2,960."
Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00
Source [Ex. __ / Bates __]: "A0427 ALS emergency transport, 1 unit, charge $1,380.00."
Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05
Source [Ex. __ / Bates __]: "charge $187.05."

Billed charges accepted from these records: $4,527.05
=== lib10
BILLED CHARGES

Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00
Source [Ex. __ / Bates __]: "FL47 total charges $4,920.00."
Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00
Source [Ex. __ / Bates __]: "Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $386.50
Source [Ex. __ / Bates __]: "Rev 0250 pharmacy, 14 units, FL47 total charges $386.50."
Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $712.00
Source [Ex. __ / Bates __]: "Rev 0300 laboratory, 6 units, FL47 total charges $712.00."

Billed charges accepted from these records: $8,123.50
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:25:33.809Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat evals/golden/case_09_nonvisit_hides_gap.txt; git show 986fc55:evals/letter_check.py | sed -n 364,400p",
 "description": "Read case_09 text and letters_for"
}
````

### User / tool · 2026-11-03T00:25:33.948Z

**tool result**
````
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-02-02
Source: Hobbleton Family Clinic, visit
Excerpt: "Left wrist pain 4/10. Splint applied. Return in 2 weeks."

=== Record 2 ===
Date: 2026-03-01
Source: Hobbleton Family Clinic, billing statement
Excerpt: "Statement for visit of 2026-02-02: $275."

=== Record 3 ===
Date: 2026-03-12
Source: Hobbleton Family Clinic, phone note
Excerpt: "Patient called to request a work note. Work note provided."

=== Record 4 ===
Date: 2026-03-30
Source: Hobbleton Family Clinic, visit
Excerpt: "Left wrist pain 3/10. Splint removed."

=== Record 5 ===
Date: 2026-04-13
Source: Hobbleton Family Clinic, visit
Excerpt: "Pain 1/10. Released from care."

def letters_for(text: str, backend: str = "fixture") -> dict:
    """{'all_accepted': {...}, 'charges_dismissed': {...}}, each {'letters': {style: text}, 'notes': str, 'charge_cents': [...], 'refused': [(id, code)], 'gate': {style: [why...]}}."""
    from app.backend import export, ingest as IN, pipeline as PL, store
    from app.llm import provider as P
    out = {}
    for variant, dismiss in (("all_accepted", False), ("charges_dismissed", True), ("counted", False)):
        with PL._Backend(backend), tempfile.TemporaryDirectory() as tmp:
            conn, cid, call = PL._scratch_call(tmp, IN.normalize_text(text))
            with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
                PL.run_pipeline(conn, cid, text, call=call)
            cents, refused = _walk(conn, cid, dismiss)
            if variant == "counted":
                cents = _count_all(conn, cid)
            case = store.export_case(conn, cid)
            case["judge_not_run"] = []          # this check reads the letter text only; the second-check gate is a separate rule (D-044)
            built, gate = {}, {}
            for st in STYLES:
                key = st or "standard"
                try:
                    built[key] = export.build_export(case, st)
                except export.ExportBlocked as e:                  # T-139 r4: the export gate itself; a blocked letter is a violation, and the text is still audited below
                    gate[key] = [i["why"] for i in e.items]
                    built[key] = export.build_export(case, st, check_letter=False)
            src = {r["n"]: r["source"] for r in case["records"]}
            dismissed = sorted({src[a["record_no"]].split(",", 1)[0].strip() for a in case["amounts"] if a["cls"] == "charge" and a["review_status"] == "dismissed"})
            conn.close()
        out[variant] = {"letters": {k: v["letter_text"] for k, v in built.items()}, "notes": built["standard"]["internal_notes_text"],
                        "charge_cents": cents, "refused": refused, "records": case["records"], "dismissed_providers": dismissed, "gate": gate}
    return out


def dismissed_in_bills(notes: str, providers) -> list:
    """Providers whose charge was dismissed that the notes still list under BILLS TO REQUEST."""
    sec = notes.split("BILLS TO REQUEST")[1].split("RECORDS NOT IN THE TREATMENT SECTION")[0] if "BILLS TO REQUEST" in notes else ""
    listed = [re.sub(r"\s*\(itemized ledger\)$", "", x.strip().rstrip(".")) for x in sec.split("\n", 2)[-1].lstrip("- ").split(";")]
    return [p for p in providers if p in listed]
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:25:45.492Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/letters_dump_r2.py",
 "content": "\"\"\"T-202 r2 paralegal: letters + internal notes for sample, case_09, lib14, lib10, lib11 (all_accepted and counted variants) from the 986fc55 archive,\nplus SYNTHETIC variants of case_09 whose bill line the code cannot date (ambiguous numeric DOS; CMS-1500 with two dates of service), to read the\nnot-stated wording as a demand letter prints it. Run from repo root:\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/letters_dump_r2.py <archive_root> <out_dir>\n\"\"\"\nimport os\nimport sys\nimport traceback\n\nroot = os.path.abspath(sys.argv[1])\nout = os.path.abspath(sys.argv[2])\nsys.path.insert(0, root)\nos.chdir(root)\nos.environ.setdefault(\"LLM_BACKEND\", \"fixture\")\nos.environ.setdefault(\"FIXTURE_SET\", \"curated\")\nfrom evals import letter_check as LC  # noqa: E402\n\nC09 = open(\"evals/golden/case_09_nonvisit_hides_gap.txt\").read()\nAMBIG = C09.replace('Date: 2026-03-01\\nSource: Hobbleton Family Clinic, billing statement\\nExcerpt: \"Statement for visit of 2026-02-02: $275.\"',\n                    'Date: 2026-06-01\\nSource: Hobbleton Family Clinic, billing statement\\nExcerpt: \"Date of service 04/05/2026: office visit charge $275.00.\"')\nCMS = C09.replace('Date: 2026-03-01\\nSource: Hobbleton Family Clinic, billing statement\\nExcerpt: \"Statement for visit of 2026-02-02: $275.\"',\n                  'Date: 2026-04-20\\nSource: Hobbleton Family Clinic, CMS-1500\\nExcerpt: \"CMS-1500 for dates of service 02/02/2026 and 03/30/2026. CPT 99213 charge $150.00. CPT 29125 splint charge $125.00.\"')\nassert AMBIG != C09 and CMS != C09\n\nCASES = {\n    \"sample\": open(\"evals/golden/sample.txt\").read(),\n    \"case_09\": C09,\n    \"lib14\": open(\"evals/library/case_lib14_handwritten_chiro_scans.txt\").read(),\n    \"lib10\": open(\"evals/library/case_lib10_eob_ub04_cms1500.txt\").read(),\n    \"lib11\": open(\"evals/library/case_lib11_priors_and_ledger.txt\").read(),\n    \"synth_ambiguous_dos\": AMBIG,\n    \"synth_cms1500_two_dates\": CMS,\n}\nfor name, text in CASES.items():\n    try:\n        got = LC.letters_for(text)\n    except Exception:\n        print(f\"== {name}: letters_for raised\\n{traceback.format_exc()}\")\n        continue\n    for variant in (\"all_accepted\", \"counted\"):\n        v = got[variant]\n        with open(os.path.join(out, f\"{name}-{variant}-letter.txt\"), \"w\") as f:\n            f.write(v[\"letters\"][\"standard\"])\n        with open(os.path.join(out, f\"{name}-{variant}-notes.txt\"), \"w\") as f:\n            f.write(v[\"notes\"])\n        lines = LC.charge_lines(v[\"letters\"][\"standard\"])\n        viol = LC.charge_date_violations(v[\"letters\"][\"standard\"], v[\"records\"])\n        print(f\"== {name} {variant}: cents={v['charge_cents']} refused={v['refused']} gate={v['gate']}\")\n        for h, q in lines:\n            print(\"   \", h, \"|\", q)\n        print(\"    date violations:\", viol)\n"
}
````

### User / tool · 2026-11-03T00:25:45.600Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/letters_dump_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:25:50.032Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; mkdir -p artifacts/review-evidence/T-202-paralegal-r2/letters; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/letters_dump_r2.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr2_986fc55 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/letters > artifacts/review-evidence/T-202-paralegal-r2/letters_dump_r2.out 2>&1; cat artifacts/review-evidence/T-202-paralegal-r2/letters_dump_r2.out",
 "description": "Generate in-process letters incl. synthetic not-stated variants",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T00:25:54.322Z

**tool result**
````
llm call failed call_id=c394d35a45139 step=extract attempt=1 prompt_hash=1c695c709b4ba6a23838aefb77a30455e0e4b4969683611faa8a31b17962a114
llm call failed call_id=ccffd9a0c869b step=extract attempt=1 prompt_hash=4e125efe75cbe7e149d3a6f9401e22532bfc29cab29ae973b22b5c4edade2730
llm call failed call_id=c3003e1a4f7fd step=extract attempt=1 prompt_hash=301f3e3030797717551a1e215e31632875ed498289b53c8a8335526af41695d4
llm call failed call_id=c37fd279995e9 step=extract attempt=1 prompt_hash=bfcfe1db058428e83a2b1d3d93349444ff3fc2d2f17cd94d12f7bf8c5059875a
llm call failed call_id=cf9f746aceba5 step=extract attempt=1 prompt_hash=028686fff244c6585d867f8664f7fdf7972a0d4cdff06ec5419b61004b123302
llm call failed call_id=ca9ba7946cf78 step=j2 attempt=1 prompt_hash=ef2e82374e44a320203c1c0788f9982dbfb78a0e5dbede80a6d2eaaaef213c71
llm call failed call_id=c3e19cda2a950 step=flags attempt=1 prompt_hash=cf7adf099f2cc57cd693bbba71acf598e0bfb1c40a05637e894f5e8b11a29537
llm call failed call_id=cd765b19b56dc step=flags attempt=1 prompt_hash=1223f5af19302e3e35b3c8b675080e97eddb6dce0c5605f43287acb59c18beb9
llm call failed call_id=c529d62fd99ae step=flags attempt=1 prompt_hash=9f30aa0f7fd4fffd5e5e06ea69e48e9b594f4b71b310263b96b726ead46bb24d
llm call failed call_id=ca967da8fe640 step=flags attempt=1 prompt_hash=d49132e98c40d33efd0d4eda5c9070d35874d78271524571f42d65752acd9696
llm call failed call_id=cdb86d0492de3 step=flags attempt=1 prompt_hash=78c0e130ba3a5793e5a4e310f4ba39fb476b9909eeea0d35e663b4a4fa2f89d9
llm call failed call_id=cf878a00d3236 step=extract attempt=1 prompt_hash=1c695c709b4ba6a23838aefb77a30455e0e4b4969683611faa8a31b17962a114
llm call failed call_id=cf513b3040eee step=extract attempt=1 prompt_hash=4e125efe75cbe7e149d3a6f9401e22532bfc29cab29ae973b22b5c4edade2730
llm call failed call_id=cf27fdb836c27 step=extract attempt=1 prompt_hash=301f3e3030797717551a1e215e31632875ed498289b53c8a8335526af41695d4
llm call failed call_id=c7c0d663c1045 step=extract attempt=1 prompt_hash=bfcfe1db058428e83a2b1d3d93349444ff3fc2d2f17cd94d12f7bf8c5059875a
llm call failed call_id=c34985b10c614 step=extract attempt=1 prompt_hash=028686fff244c6585d867f8664f7fdf7972a0d4cdff06ec5419b61004b123302
llm call failed call_id=cfb81631c300a step=j2 attempt=1 prompt_hash=ef2e82374e44a320203c1c0788f9982dbfb78a0e5dbede80a6d2eaaaef213c71
llm call failed call_id=c7bfaecd501ed step=flags attempt=1 prompt_hash=1223f5af19302e3e35b3c8b675080e97eddb6dce0c5605f43287acb59c18beb9
llm call failed call_id=ccd1dda152566 step=flags attempt=1 prompt_hash=cf7adf099f2cc57cd693bbba71acf598e0bfb1c40a05637e894f5e8b11a29537
llm call failed call_id=ce5b71211a0c3 step=flags attempt=1 prompt_hash=9f30aa0f7fd4fffd5e5e06ea69e48e9b594f4b71b310263b96b726ead46bb24d
llm call failed call_id=cd20233aba264 step=flags attempt=1 prompt_hash=d49132e98c40d33efd0d4eda5c9070d35874d78271524571f42d65752acd9696
llm call failed call_id=c5421a6d1a538 step=flags attempt=1 prompt_hash=78c0e130ba3a5793e5a4e310f4ba39fb476b9909eeea0d35e663b4a4fa2f89d9
llm call failed call_id=cba02cb29b293 step=extract attempt=1 prompt_hash=1c695c709b4ba6a23838aefb77a30455e0e4b4969683611faa8a31b17962a114
llm call failed call_id=cd0f0b8349788 step=extract attempt=1 prompt_hash=4e125efe75cbe7e149d3a6f9401e22532bfc29cab29ae973b22b5c4edade2730
llm call failed call_id=c9421b14cd5e6 step=extract attempt=1 prompt_hash=301f3e3030797717551a1e215e31632875ed498289b53c8a8335526af41695d4
llm call failed call_id=c937b99b73c96 step=extract attempt=1 prompt_hash=bfcfe1db058428e83a2b1d3d93349444ff3fc2d2f17cd94d12f7bf8c5059875a
llm call failed call_id=cb4356a5eb794 step=extract attempt=1 prompt_hash=028686fff244c6585d867f8664f7fdf7972a0d4cdff06ec5419b61004b123302
llm call failed call_id=c66662122404c step=j2 attempt=1 prompt_hash=ef2e82374e44a320203c1c0788f9982dbfb78a0e5dbede80a6d2eaaaef213c71
llm call failed call_id=c6ea85e20584e step=flags attempt=1 prompt_hash=1223f5af19302e3e35b3c8b675080e97eddb6dce0c5605f43287acb59c18beb9
llm call failed call_id=c403830b72f52 step=flags attempt=1 prompt_hash=cf7adf099f2cc57cd693bbba71acf598e0bfb1c40a05637e894f5e8b11a29537
llm call failed call_id=c9f3248260b3b step=flags attempt=1 prompt_hash=9f30aa0f7fd4fffd5e5e06ea69e48e9b594f4b71b310263b96b726ead46bb24d
llm call failed call_id=cd1733f0b9377 step=flags attempt=1 prompt_hash=d49132e98c40d33efd0d4eda5c9070d35874d78271524571f42d65752acd9696
llm call failed call_id=c79a47ba1f860 step=flags attempt=1 prompt_hash=78c0e130ba3a5793e5a4e310f4ba39fb476b9909eeea0d35e663b4a4fa2f89d9
llm call failed call_id=c2e644fd65aaa step=extract attempt=1 prompt_hash=4d2be32aadec8f6c773b344e4a74826ef4f5c42e983b909a1c4ea7a2aa4fa0c4
llm call failed call_id=c476584156b4c step=extract attempt=1 prompt_hash=edfb11d933988b8c1a75762df0cf62b58359e69e79390db1562c974a44c54218
llm call failed call_id=c4214d13d6946 step=extract attempt=1 prompt_hash=edea79f1398615fba03ecd8266fe09577a99db77a35715521fd177fe7a2e6b64
llm call failed call_id=cf2ea79b5fc9b step=extract attempt=1 prompt_hash=2aca0c360bafeb694b1b74f4ecba896ceb0b05d0dda25bfdba5e0a38c9c02189
llm call failed call_id=c6b1f9f08a969 step=extract attempt=1 prompt_hash=ee19f5c91f8d8734f1349b589a15fc80e3dd111e84cc2432c328afd78b7333d2
llm call failed call_id=c80fc9ce5f281 step=j2 attempt=1 prompt_hash=b88d9a608fb91950d82f43916165eb5cbb701caa859a99ad0a548fdceeab2304
llm call failed call_id=c6a9803b91778 step=j2 attempt=1 prompt_hash=671a8b9baf6f1ee26ca72729637e0efd89e56020b2aae66202fb4080c65455a2
llm call failed call_id=c8815644b8127 step=flags attempt=1 prompt_hash=5a6383ecd9230d9758dfa6fa013c39e9063fc49508710d2380db711382c9c668
llm call failed call_id=c5435ba5509b2 step=flags attempt=1 prompt_hash=11ee52ac591f4499e74a5853d7e2285879d3170af512039b8346916170ac1f72
llm call failed call_id=c8c1539bcf178 step=flags attempt=1 prompt_hash=bb0913399886f3c70cc124cab7255db5354dcf9591f5e818b4440d9cc818ccde
llm call failed call_id=c0dfdf02ba3a9 step=flags attempt=1 prompt_hash=c2720375c5cf949ed50eedab1bfd633794cd873afb05e79aa4146f160c43d781
llm call failed call_id=c458a61683923 step=flags attempt=1 prompt_hash=a297283eb4fbe731af04075335fc2197d2468d876985e427c6a98d2bb24cf3b4
llm call failed call_id=c2c3072c07430 step=extract attempt=1 prompt_hash=4d2be32aadec8f6c773b344e4a74826ef4f5c42e983b909a1c4ea7a2aa4fa0c4
llm call failed call_id=caddbee4fdadb step=extract attempt=1 prompt_hash=edfb11d933988b8c1a75762df0cf62b58359e69e79390db1562c974a44c54218
llm call failed call_id=c695650048c7d step=extract attempt=1 prompt_hash=edea79f1398615fba03ecd8266fe09577a99db77a35715521fd177fe7a2e6b64
llm call failed call_id=cdd93f9a803d5 step=extract attempt=1 prompt_hash=2aca0c360bafeb694b1b74f4ecba896ceb0b05d0dda25bfdba5e0a38c9c02189
llm call failed call_id=cc3454d50a9c5 step=extract attempt=1 prompt_hash=ee19f5c91f8d8734f1349b589a15fc80e3dd111e84cc2432c328afd78b7333d2
llm call failed call_id=cf92b90236f90 step=j2 attempt=1 prompt_hash=b88d9a608fb91950d82f43916165eb5cbb701caa859a99ad0a548fdceeab2304
llm call failed call_id=cda6dbe34c302 step=j2 attempt=1 prompt_hash=671a8b9baf6f1ee26ca72729637e0efd89e56020b2aae66202fb4080c65455a2
llm call failed call_id=c992c1f1fdfd3 step=flags attempt=1 prompt_hash=bb0913399886f3c70cc124cab7255db5354dcf9591f5e818b4440d9cc818ccde
llm call failed call_id=c0a2247564756 step=flags attempt=1 prompt_hash=5a6383ecd9230d9758dfa6fa013c39e9063fc49508710d2380db711382c9c668
llm call failed call_id=c3f1e39af48fc step=flags attempt=1 prompt_hash=11ee52ac591f4499e74a5853d7e2285879d3170af512039b8346916170ac1f72
llm call failed call_id=cc4b828c443e2 step=flags attempt=1 prompt_hash=c2720375c5cf949ed50eedab1bfd633794cd873afb05e79aa4146f160c43d781
llm call failed call_id=cd1ae5d149381 step=flags attempt=1 prompt_hash=a297283eb4fbe731af04075335fc2197d2468d876985e427c6a98d2bb24cf3b4
llm call failed call_id=c8b307835fd9a step=extract attempt=1 prompt_hash=4d2be32aadec8f6c773b344e4a74826ef4f5c42e983b909a1c4ea7a2aa4fa0c4
llm call failed call_id=c21ee32b5b00f step=extract attempt=1 prompt_hash=edea79f1398615fba03ecd8266fe09577a99db77a35715521fd177fe7a2e6b64
llm call failed call_id=cb423a56faaec step=extract attempt=1 prompt_hash=edfb11d933988b8c1a75762df0cf62b58359e69e79390db1562c974a44c54218
llm call failed call_id=c204c3e1f9d5b step=extract attempt=1 prompt_hash=2aca0c360bafeb694b1b74f4ecba896ceb0b05d0dda25bfdba5e0a38c9c02189
llm call failed call_id=c6bfd5c670750 step=extract attempt=1 prompt_hash=ee19f5c91f8d8734f1349b589a15fc80e3dd111e84cc2432c328afd78b7333d2
llm call failed call_id=c270eb70d54f4 step=j2 attempt=1 prompt_hash=b88d9a608fb91950d82f43916165eb5cbb701caa859a99ad0a548fdceeab2304
llm call failed call_id=c66786b4e44d5 step=j2 attempt=1 prompt_hash=671a8b9baf6f1ee26ca72729637e0efd89e56020b2aae66202fb4080c65455a2
llm call failed call_id=cdde9317b0d65 step=flags attempt=1 prompt_hash=bb0913399886f3c70cc124cab7255db5354dcf9591f5e818b4440d9cc818ccde
llm call failed call_id=c17388432dd8d step=flags attempt=1 prompt_hash=5a6383ecd9230d9758dfa6fa013c39e9063fc49508710d2380db711382c9c668
llm call failed call_id=c7b0a20dccf19 step=flags attempt=1 prompt_hash=11ee52ac591f4499e74a5853d7e2285879d3170af512039b8346916170ac1f72
llm call failed call_id=c91064f96bd82 step=flags attempt=1 prompt_hash=c2720375c5cf949ed50eedab1bfd633794cd873afb05e79aa4146f160c43d781
llm call failed call_id=c4bec74d68c41 step=flags attempt=1 prompt_hash=a297283eb4fbe731af04075335fc2197d2468d876985e427c6a98d2bb24cf3b4
== sample all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== sample counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== case_09 all_accepted: cents=[27500] refused=[('e2', 'CHARGE_TEXT_IN_ENTRY')] gate={}
    Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00 | Statement for visit of 2026-02-02: $275.
    date violations: []
== case_09 counted: cents=[27500] refused=[('e2', 'CHARGE_TEXT_IN_ENTRY')] gate={}
    Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00 | Statement for visit of 2026-02-02: $275.
    date violations: []
== lib14 all_accepted: cents=[296000, 138000, 18705] refused=[('e7', 'CHARGE_TEXT_IN_ENTRY'), ('e8', 'CHARGE_TEXT_IN_ENTRY'), ('e5', 'DATE_UNCONFIRMED'), ('a5', 'COMPARE_REQUIRED')] gate={}
    Orrin Mere Regional ED, September 14, 2026: $2,960.00 | ED charge: $2,960.
    Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00 | A0427 ALS emergency transport, 1 unit, charge $1,380.00.
    Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05 | charge $187.05.
    date violations: []
== lib14 counted: cents=[296000, 138000, 18705] refused=[('e7', 'CHARGE_TEXT_IN_ENTRY'), ('e8', 'CHARGE_TEXT_IN_ENTRY'), ('e5', 'DATE_UNCONFIRMED'), ('a5', 'COMPARE_REQUIRED')] gate={}
    Orrin Mere Regional ED, September 14, 2026: $2,960.00 | ED charge: $2,960.
    Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00 | A0427 ALS emergency transport, 1 unit, charge $1,380.00.
    Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05 | charge $187.05.
    date violations: []
== lib10 all_accepted: cents=[492000, 210500, 38650, 71200] refused=[('e1', 'COMPARE_REQUIRED'), ('e4', 'COMPARE_REQUIRED'), ('e8', 'CHARGE_TEXT_IN_ENTRY'), ('a6', 'COMPARE_REQUIRED'), ('a7', 'COMPARE_REQUIRED'), ('a9', 'COMPARE_REQUIRED'), ('a11', 'COMPARE_REQUIRED')] gate={}
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00 | FL47 total charges $4,920.00.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00 | Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $386.50 | Rev 0250 pharmacy, 14 units, FL47 total charges $386.50.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $712.00 | Rev 0300 laboratory, 6 units, FL47 total charges $712.00.
    date violations: []
== lib10 counted: cents=[492000, 210500, 38650, 71200] refused=[('e1', 'COMPARE_REQUIRED'), ('e4', 'COMPARE_REQUIRED'), ('e8', 'CHARGE_TEXT_IN_ENTRY'), ('a6', 'COMPARE_REQUIRED'), ('a7', 'COMPARE_REQUIRED'), ('a9', 'COMPARE_REQUIRED'), ('a11', 'COMPARE_REQUIRED')] gate={}
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00 | FL47 total charges $4,920.00.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00 | Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $386.50 | Rev 0250 pharmacy, 14 units, FL47 total charges $386.50.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $712.00 | Rev 0300 laboratory, 6 units, FL47 total charges $712.00.
    date violations: []
== lib11 all_accepted: cents=[326000] refused=[('e1', 'COMPARE_REQUIRED'), ('e2', 'COMPARE_REQUIRED'), ('e4', 'COMPARE_REQUIRED'), ('e9', 'CHARGE_TEXT_IN_ENTRY'), ('a2', 'COMPARE_REQUIRED'), ('a3', 'COMPARE_REQUIRED'), ('a4', 'COMPARE_REQUIRED'), ('a5', 'COMPARE_REQUIRED'), ('a6', 'COMPARE_REQUIRED'), ('a8', 'COMPARE_REQUIRED')] gate={}
    Wexcombe Memorial ED, March 18, 2026: $3,260.00 | ED charge: $3,260.
    date violations: []
== lib11 counted: cents=[326000, 25000, 18000, 231000] refused=[('e1', 'COMPARE_REQUIRED'), ('e2', 'COMPARE_REQUIRED'), ('e4', 'COMPARE_REQUIRED'), ('e9', 'CHARGE_TEXT_IN_ENTRY'), ('a2', 'COMPARE_REQUIRED'), ('a3', 'COMPARE_REQUIRED'), ('a4', 'COMPARE_REQUIRED'), ('a5', 'COMPARE_REQUIRED'), ('a6', 'COMPARE_REQUIRED'), ('a8', 'COMPARE_REQUIRED')] gate={}
    Wexcombe Memorial ED, March 18, 2026: $3,260.00 | ED charge: $3,260.
    Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00 | New patient exam charge $250.00
    Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $180.00 | x-ray charge $180.00
    Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $2,310.00 | treatment visits 1 through 14 charge $2,310.00
    date violations: []
== synth_ambiguous_dos all_accepted: cents=[27500] refused=[] gate={}
    Hobbleton Family Clinic, billing statement (statement dated June 1, 2026; service date not stated): $275.00 | Date of service 04/05/2026: office visit charge $275.00.
    date violations: []
== synth_ambiguous_dos counted: cents=[27500] refused=[] gate={}
    Hobbleton Family Clinic, billing statement (statement dated June 1, 2026; service date not stated): $275.00 | Date of service 04/05/2026: office visit charge $275.00.
    date violations: []
== synth_cms1500_two_dates all_accepted: cents=[15000, 12500] refused=[] gate={'standard': ['Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’: “Source [Ex. __ / Bates __]: "CPT 99213 charge $150.00."”. A charge line carries its own amount only.', 'Line 8 of the letter is a Billed charges line for $125.00 and also states ‘29125 splint charge’: “Source [Ex. __ / Bates __]: "CPT 29125 splint charge $125.00."”. A charge line carries its own amount only.'], 'oneline': ['Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’: “Source [Ex. __ / Bates __]: "CPT 99213 charge $150.00."”. A charge line carries its own amount only.', 'Line 8 of the letter is a Billed charges line for $125.00 and also states ‘29125 splint charge’: “Source [Ex. __ / Bates __]: "CPT 29125 splint charge $125.00."”. A charge line carries its own amount only.']}
    Hobbleton Family Clinic, CMS-1500 (statement dated April 20, 2026; service date not stated): $150.00 | CPT 99213 charge $150.00.
    Hobbleton Family Clinic, CMS-1500 (statement dated April 20, 2026; service date not stated): $125.00 | CPT 29125 splint charge $125.00.
    date violations: []
== synth_cms1500_two_dates counted: cents=[15000, 12500] refused=[] gate={'standard': ['Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’: “Source [Ex. __ / Bates __]: "CPT 99213 charge $150.00."”. A charge line carries its own amount only.', 'Line 8 of the letter is a Billed charges line for $125.00 and also states ‘29125 splint charge’: “Source [Ex. __ / Bates __]: "CPT 29125 splint charge $125.00."”. A charge line carries its own amount only.'], 'oneline': ['Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’: “Source [Ex. __ / Bates __]: "CPT 99213 charge $150.00."”. A charge line carries its own amount only.', 'Line 8 of the letter is a Billed charges line for $125.00 and also states ‘29125 splint charge’: “Source [Ex. __ / Bates __]: "CPT 29125 splint charge $125.00."”. A charge line carries its own amount only.']}
    Hobbleton Family Clinic, CMS-1500 (statement dated April 20, 2026; service date not stated): $150.00 | CPT 99213 charge $150.00.
    Hobbleton Family Clinic, CMS-1500 (statement dated April 20, 2026; service date not stated): $125.00 | CPT 29125 splint charge $125.00.
    date violations: []
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:26:08.322Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; A=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr2_986fc55; grep -rn \"service_date\\|confirm_note\" $A/app --include=*.py --include=*.js | grep -v \"^.*service_date.py\" | cut -c1-220; grep -n \"confirm_note\\|service_date\" $A/memory/contracts/api.md | cut -c1-160",
 "description": "Find where service_date/confirm_note are consumed"
}
````

### User / tool · 2026-11-03T00:26:08.531Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
191:      "not_counted_reason": "This figure is a rate, not a charge, so it is not added to the total.", "countable": false, "count_confirm": null, "service_dat
574:Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider a
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:26:12.836Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr2_986fc55 && grep -rln \"service_date\\|confirm_note\" app | sort; grep -rn \"confirm_note\\|service_date\" app/frontend | head; grep -n \"service date\\|Confirm the date\" app/backend/export.py | head",
 "description": "List files consuming service_date and confirm_note"
}
````

### User / tool · 2026-11-03T00:26:12.990Z

**tool result**
````
app/backend/export.py
app/backend/present.py
app/backend/service_date.py
app/backend/store.py
176:        """D-071: in the order of the service dates the letter prints (a charge with no stated date sorts by its statement date)."""
216:        """D-071 (extends T-200): the label before a charge's amount in the letter. A date there reads as the date of service, so it is the service date the charge's own bill line
218:        NEVER given the record's date bare: 'Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated)'. Chosen over dropping the date
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:26:15.821Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/letters; cat synth_ambiguous_dos-all_accepted-letter.txt; echo ======; cat synth_ambiguous_dos-all_accepted-notes.txt; echo ======; grep -n -i \"service date\\|date of service\\|itemized\\|Fennimoor\" lib11-counted-notes.txt",
 "description": "Read synthetic ambiguous letter and notes"
}
````

### User / tool · 2026-11-03T00:26:15.948Z

**tool result**
````
TREATMENT CHRONOLOGY

BILLED CHARGES

Hobbleton Family Clinic, billing statement (statement dated June 1, 2026; service date not stated): $275.00
Source [Ex. __ / Bates __]: "Date of service 04/05/2026: office visit charge $275.00."

Billed charges accepted from these records: $275.00======
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was built from answers the team prepared for this demo and checked by a second check; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.

FLAGS ACCEPTED
- Gap: 38 days, February 2, 2026 to March 12, 2026: record 1 (Hobbleton Family Clinic, visit, February 2, 2026) to record 3 (Hobbleton Family Clinic, phone note, March 12, 2026).
- Gap: 49 days, April 13, 2026 to June 1, 2026: record 5 (Hobbleton Family Clinic, visit, April 13, 2026) to record 2 (Hobbleton Family Clinic, billing statement, June 1, 2026).

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- none

AMOUNTS NOT TOTALED
- none

DAMAGES MENTIONS (not charges)
- none

FUTURE TREATMENT RECOMMENDED (no cost stated)
- none

BILLS TO REQUEST (entry in the letter, no accepted charge)
- none

RECORDS NOT IN THE TREATMENT SECTION
- Record 1 (Hobbleton Family Clinic, visit, February 2, 2026) — no entry
- Record 3 (Hobbleton Family Clinic, phone note, March 12, 2026) — no entry
- Record 4 (Hobbleton Family Clinic, visit, March 30, 2026) — no entry
- Record 5 (Hobbleton Family Clinic, visit, April 13, 2026) — no entry
- Record 2 (Hobbleton Family Clinic, billing statement, June 1, 2026) — no entry

EDITED ITEMS
- none

PENDING ITEMS NOT INCLUDED
- none======
6:- Gap: 35 days, April 24, 2026 to May 29, 2026: record 7 (Fennimoor Spine Clinic, visit 8, April 24, 2026) to record 8 (Fennimoor Spine Clinic, visit 14, May 29, 2026).
7:- Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior accidents? Yes [ ] No [X]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
8:- Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior injuries? Yes [ ] No IX]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
9:- Prior condition: record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "Problem list: hypertension, type 2 diabetes, chronic low back pain."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."; record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior accidents?"; record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior injuries?".
10:- Causation language: record 2 (Ashgrove Fire-Rescue run report, March 18, 2026) "Ambulatory at scene."; record 4 (Pellingham and Rook PLLC, correspondence (letter of protection), March 26, 2026) "Letter of protection to Fennimoor Spine Clinic."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Patient referred by attorney."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Treating under a letter of protection."; record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) "Account held under letter of protection."
16:- Record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026): "Treating under a letter of protection." Causation language.
17:- Record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026): "Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]." Conflict, other fact mismatch; prior condition.
18:- Record 7 (Fennimoor Spine Clinic, visit 8, April 24, 2026): "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued." Gap.
19:- Record 8 (Fennimoor Spine Clinic, visit 14, May 29, 2026): "Neck pain 4/10, low back pain 5/10. Care continues." Gap.
22:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Adjustment (courtesy discount) -$274.00." Not totaled ($274.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.
37:- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) — states a dollar amount, not exported (this record is a bill and its charges are already listed under Billed charges, so dismiss this entry unless it states treatment)
45:- Entry, record 4 (Pellingham and Rook PLLC, correspondence (letter of protection), March 26, 2026): "Law firm letter of protection to Fennimoor Spine Clinic states the firm represents the client for injuries from a collision on 2026-03-18 and asks the clinic to defer collection while the claim is pending."
46:- Entry, record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Itemized ledger lists new patient exam charge $250.00, x-ray charge $180.00, treatment visits 1 through 14 charge $2,310.00, and total charges $2,740.00."
47:- Amount $2,740 (unclear), record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "total charges $2,740.00."
48:- Amount $300 (unclear), record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Payment received $300.00."
49:- Amount $2,166 (unclear), record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Balance due $2,166.00."
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:26:38.763Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"token=\\|/case/\" artifacts/review-evidence/T-202-paralegal-r2/p01.out | head; curl -s http://127.0.0.1:7976/api/cases | head -c 1500",
 "description": "Find case tokens from the UI run"
}
````

### User / tool · 2026-11-03T00:26:38.935Z

**tool result**
````
31:===== [sample] step 3 done url=http://127.0.0.1:7976/case/SfT5YaCLeW3v9bKQxQEmIQ/bills
86:[case_09] created via POST /api/cases token=sGgv7E88x0beSaB09PVPEg
97:===== [case_09] step 3 done url=http://127.0.0.1:7976/case/sGgv7E88x0beSaB09PVPEg/bills
171:===== [lib14] step 3 done url=http://127.0.0.1:7976/case/ewizSiIR767-uxwAss5e3A/bills
262:===== [lib10] step 3 done url=http://127.0.0.1:7976/case/OySGH-nh4pkbSNh6FIhvUg/bills
{"cases":[{"token":"OySGH-nh4pkbSNh6FIhvUg","title":"Eob ub04 cms1500","name":"case lib10 eob ub04 cms1500","source":"paste","status":"ready","record_count":9,"created_at":"2026-11-03T00:24:47Z","updated_at":"2026-11-03T00:24:48Z","last_activity_at":"2026-11-03T00:25:04Z","run":{"stage":"finalize","steps_done":7,"steps_total":8,"running":false,"error":false},"progress":{"entries":{"decided":9,"total":9},"flags":{"decided":2,"total":2},"amounts":{"decided":11,"total":11}},"counts":{"pending":0,"accepted":21,"edited":0,"dismissed":1,"needs_review":10},"hitl":{"pending":0,"needs_review":10,"needs_review_open":0,"edits_to_check":0,"could_not_verify":0,"gate_blockers":[],"gate_warnings":[]},"export_ready":true,"next_action":null,"status_error":false,"status_error_message":null},{"token":"ewizSiIR767-uxwAss5e3A","title":"Handwritten chiro scans","name":"case lib14 handwritten chiro scans","source":"paste","status":"ready","record_count":8,"created_at":"2026-11-03T00:24:34Z","updated_at":"2026-11-03T00:24:35Z","last_activity_at":"2026-11-03T00:24:45Z","run":{"stage":"finalize","steps_done":7,"steps_total":8,"running":false,"error":false},"progress":{"entries":{"decided":8,"total":8},"flags":{"decided":3,"total":3},"amounts":{"decided":5,"total":5}},"counts":{"pending":0,"accepted":13,"edited":0,"dismissed":3,"needs_review":7},"hitl":{"pending":0,"needs_review":7,"needs_review_open":0,"edits_to_check":0,"could_not_verify":1,"gate_blockers":[],"gate_warnings":[]},"export_ready":true,"
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:26:43.787Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/api_service_date.py",
 "content": "\"\"\"T-202 r2: GET /api/cases/{token} on the running 986fc55 app (port 7976) and print amounts[].service_date per charge next to the record's date\nthe Step 3 card shows. Tokens from p01.out.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/api_service_date.py\n\"\"\"\nimport json\nimport urllib.request\n\nBASE = \"http://127.0.0.1:7976\"\nTOKENS = {\"sample\": \"SfT5YaCLeW3v9bKQxQEmIQ\", \"case_09\": \"sGgv7E88x0beSaB09PVPEg\", \"lib14\": \"ewizSiIR767-uxwAss5e3A\", \"lib10\": \"OySGH-nh4pkbSNh6FIhvUg\"}\nfor name, tok in TOKENS.items():\n    c = json.loads(urllib.request.urlopen(f\"{BASE}/api/cases/{tok}\", timeout=20).read())\n    print(f\"== {name}\")\n    for a in c.get(\"amounts\", []):\n        sd = a.get(\"service_date\")\n        print(f\"   {a.get('id'):>4} kind={a.get('kind'):<8} {str(a.get('display') or a.get('value') or a.get('raw') or ''):<12} service_date={json.dumps(sd, ensure_ascii=False)}\")\n"
}
````

### User / tool · 2026-11-03T00:26:43.898Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/api_service_date.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:26:45.267Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/api_service_date.py > artifacts/review-evidence/T-202-paralegal-r2/api_service_date.out 2>&1; cat artifacts/review-evidence/T-202-paralegal-r2/api_service_date.out",
 "description": "Read service_date from live case API"
}
````

### User / tool · 2026-11-03T00:26:45.528Z

**tool result**
````
== sample
     a1 kind=charge                service_date={"state": "stated", "date_iso": "2026-01-09", "end_iso": null, "text": "January 9, 2026", "statement_date_iso": "2026-01-09", "reason": null, "confirm_note": null}
     a2 kind=rate                  service_date=null
     a4 kind=charge                service_date={"state": "stated", "date_iso": "2026-05-29", "end_iso": null, "text": "May 29, 2026", "statement_date_iso": "2026-05-29", "reason": null, "confirm_note": null}
     a3 kind=damages               service_date=null
== case_09
     a1 kind=charge                service_date={"state": "stated", "date_iso": "2026-02-02", "end_iso": null, "text": "February 2, 2026", "statement_date_iso": "2026-03-01", "reason": null, "confirm_note": null}
== lib14
     a1 kind=charge                service_date={"state": "stated", "date_iso": "2026-09-14", "end_iso": null, "text": "September 14, 2026", "statement_date_iso": "2026-09-14", "reason": null, "confirm_note": null}
     a2 kind=charge                service_date={"state": "stated", "date_iso": "2026-09-14", "end_iso": null, "text": "September 14, 2026", "statement_date_iso": "2026-11-12", "reason": null, "confirm_note": null}
     a3 kind=rate                  service_date=null
     a4 kind=charge                service_date={"state": "stated", "date_iso": "2026-09-14", "end_iso": null, "text": "September 14, 2026", "statement_date_iso": "2026-11-12", "reason": null, "confirm_note": null}
     a5 kind=unclear               service_date=null
== lib10
     a1 kind=rate                  service_date=null
     a2 kind=charge                service_date={"state": "stated", "date_iso": "2026-06-09", "end_iso": "2026-06-12", "text": "June 9–12, 2026", "statement_date_iso": "2026-06-19", "reason": null, "confirm_note": null}
     a3 kind=charge                service_date={"state": "stated", "date_iso": "2026-06-09", "end_iso": "2026-06-12", "text": "June 9–12, 2026", "statement_date_iso": "2026-06-19", "reason": null, "confirm_note": null}
     a4 kind=charge                service_date={"state": "stated", "date_iso": "2026-06-09", "end_iso": "2026-06-12", "text": "June 9–12, 2026", "statement_date_iso": "2026-06-19", "reason": null, "confirm_note": null}
     a5 kind=charge                service_date={"state": "stated", "date_iso": "2026-06-09", "end_iso": "2026-06-12", "text": "June 9–12, 2026", "statement_date_iso": "2026-06-19", "reason": null, "confirm_note": null}
     a6 kind=unclear               service_date=null
     a7 kind=unclear               service_date=null
     a8 kind=unclear               service_date=null
     a9 kind=unclear               service_date=null
    a10 kind=unclear               service_date=null
    a11 kind=unclear               service_date=null
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:26:50.104Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n -A4 \"CMS-1500\\|Wardlaw\" evals/library/case_lib10_eob_ub04_cms1500.txt | head -40",
 "description": "Read lib10 CMS-1500 record"
}
````

### User / tool · 2026-11-03T00:26:50.202Z

**tool result**
````
25:Source: Dr. Ignatius Wardlaw, orthopedics, new patient
26-Excerpt: "Left knee pain 5/10. MRI left knee ordered. Patient states his health plan was billed for the hospital stay."
27-
28-=== Record 6 ===
29-Date: 2026-07-03
--
35:Source: Dr. Ignatius Wardlaw, orthopedics, follow-up
36-Excerpt: "Left knee pain 3/10. Injection performed. Continue home exercises."
37-
38-=== Record 8 ===
39-Date: 2026-07-14
40:Source: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)
41:Excerpt: "OCR of scanned CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, 18500, 1 unit; CPT 20610, 21000, 1 unit; CPT 97110, 96 OO, 4 units. Item 28 TOTAL CHARGE 49100. Item 29 AMOUNT PAID 0 00."
42-
43-=== Record 9 ===
44-Date: 2026-08-26
45:Source: Dr. Ignatius Wardlaw, orthopedics, follow-up
46-Excerpt: "Left knee pain 2/10. Discharged from care."
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:27:14.429Z

**tool call — Bash**
````
{
 "command": "kill 49534; /bin/sleep 1; lsof -iTCP:7976 -sTCP:LISTEN -nP; echo \"lsof exit $?\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7976/api/health",
 "description": "Stop my server and confirm the port is closed"
}
````

### User / tool · 2026-11-03T00:27:15.622Z

**tool result (error)**
````
Exit code 7
lsof exit 1
000
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:27:19.494Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 986fc55:app/backend/service_date.py | grep -n \"_NON_SVC_LEAD = \\|units = \\[u for u in _units(own)\\|if date_iso:  \\|def not_stated_text\\|def confirm_note\\|\\\"no_date\\\": \\|\\\"ambiguous_numeric\\\": \" ; git show 986fc55:evals/letter_check.py | grep -n \"def _own_dates\\|_BILLING_WORD = \" ; grep -n \"D-071 amendment\\|D-071 clarification\" memory/ORCHESTRATOR_DECISIONS.md; git show 986fc55:app/backend/store.py | grep -n \"def charge_service_date\"",
 "description": "Get line numbers for evidence references"
}
````

### User / tool · 2026-11-03T00:27:19.662Z

**tool result**
````
35:_NON_SVC_LEAD = re.compile(r"\b(?:statements?|stmt|invoice|billing|billed|bill|printed|issued|mailed|as[\s-]of|due|posted|post|paid|received|payment|processed|balance|created|generated|sent)\b"
58:def not_stated_text(statement_iso) -> str:
66:    "ambiguous_numeric": "The date written as {raw} can be read as month/day or day/month, and the record does not settle which.",
72:    "no_date": "The line states no date of service.",
76:def confirm_note(reason, raw) -> str:
297:        units = [u for u in _units(own) if _lead_ok(own, u)]
327:    if date_iso:                                                          # a dated encounter record (visit note, imaging report): the record's date is the visit
189:_BILLING_WORD = re.compile(r"(?:statement|stmt|invoice|billing|billed|posted|paid|received|payment|processed|mailed|due|balance|printed|issued)(?: date| dated| on| of)?[ :#]*$", re.IGNORECASE)
263:def _own_dates(text):
87:## D-071 amendment — when the service date is not certain, print none and ask the human
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
118:def charge_service_date(item: dict, rec, pos) -> dict:
146:def charge_service_dates(item: dict, rec, pos) -> tuple:
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:27:26.721Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py && head -20 artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py; ls reviews/T-202*; ls artifacts/review-evidence/T-202-paralegal-r2/",
 "description": "Check jsoncheck script and existing review files"
}
````

### User / tool · 2026-11-03T00:27:26.820Z

**tool result**
````
artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py
import json, re, sys

text = open(sys.argv[1], encoding="utf-8").read()
blocks = re.findall(r"```json\n(.*?)\n```", text, re.S)
print("json blocks:", len(blocks))
d = json.loads(blocks[0])
for k in ("card", "persona", "model", "scope", "exercised", "verdict", "scores", "findings", "whats_right", "questions_for_chris"):
    assert k in d, k
sev = [f["severity"] for f in d["findings"]]
print("verdict:", d["verdict"], "| severities:", sev)
blockers = sev.count("blocker"); majors = sev.count("major")
expected = "fail" if blockers else ("changes" if majors else "pass")
print("verdict rule expects:", expected, "| matches:", expected == d["verdict"])
for f in d["findings"]:
    assert all(f.get(k) for k in ("severity", "title", "evidence", "why_it_matters", "fix", "acceptance_test")), f["title"]
assert len(d["whats_right"]) <= 3
print("model:", d["model"], "| card:", d["card"], "| persona:", d["persona"])
print("all finding fields present")
reviews/T-202-paralegal.md
reviews/T-202-staff-engineer.md
api_service_date.out
api_service_date.py
case_09-s3-00-a1.png
case_09-step2-done.png
case_09-step3-done.png
case_09-step4.png
db
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:27:30.173Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence; for c in sample case_09 lib14 lib10; do cmp T-202-paralegal/ui-$c-letter.txt T-202-paralegal-r2/ui-$c-letter.txt && echo \"$c letter identical to r1 (f0921e4)\"; done; grep -c \"service date not stated\" T-202-paralegal-r2/letters/lib11-counted-letter.txt; grep -n \"Confirm the date\\|service date\" T-202-paralegal-r2/letters/*notes.txt | head -3; echo \"notes hits above (none = silent)\"",
 "description": "Compare UI letters with r1 and check notes for date mentions"
}
````

### User / tool · 2026-11-03T00:27:30.582Z

**tool result**
````
sample letter identical to r1 (f0921e4)
case_09 letter identical to r1 (f0921e4)
lib14 letter identical to r1 (f0921e4)
lib10 letter identical to r1 (f0921e4)
3
notes hits above (none = silent)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:27:35.423Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"service date not stated on this line\" memory/ORCHESTRATOR_DECISIONS.md | cut -c1-80; grep -n \"Trans Date\" artifacts/review-evidence/T-202-paralegal-r2/probe_r2.out | head -2; grep -n \"June 11, 2026: \\$70.00\\|June 18, 2026: \\$95.00\" artifacts/review-evidence/T-202-paralegal-r2/probe_r2.out",
 "description": "Verify line refs for the amendment string and N5 output"
}
````

### User / tool · 2026-11-03T00:27:35.534Z

**tool result**
````
88:T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026;
92:== N5 ledger with only a 'Trans Date' column (transaction date)  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
93:   Trans Date   Code   Description             Charges
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:27:37.146Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; sed -n 92,97p artifacts/review-evidence/T-202-paralegal-r2/probe_r2.out",
 "description": "Show N5 probe output lines"
}
````

### User / tool · 2026-11-03T00:27:37.252Z

**tool result**
````
== N5 ledger with only a 'Trans Date' column (transaction date)  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger')
   Trans Date   Code   Description             Charges
   06/11/2026   97140  Manual therapy x1       $70.00
   06/18/2026   97110  Therapeutic exercise    $95.00
       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 11, 2026: $70.00'  state=stated reason=None
       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 18, 2026: $95.00'  state=stated reason=None
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:28:54.054Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/draft-T-202-paralegal-r2.md",
 "content": "# T-202 round 2 (D-071 amendment + clarification) — paralegal review (Maria Delgado, senior PI litigation paralegal)\n\n**Verdict: fail.** Both of my round 1 blockers are fixed:\n- **Posted-first ledger:** prints the DOS column (June 10, June 17).\n- **CMS-1500 \"06/24/2026 and 07/08/2026\":** prints the not-stated form, with a clear Step 3 note.\n\nThe corpus letters (sample, case_09, lib14, lib10) are byte-identical to round 1, and correct. lib10 keeps \"June 9–12, 2026\" under the D-071 clarification.\n\n**Blocker.** More adversarial bill text shows the same class of error from another direction. A non-service date in the charge's own sentence or row is printed as the date of service:\n- a patient birth date;\n- the date of injury or accident;\n- an onset date;\n- a referral or order date.\n\n\"Birth date 03/15/1980, CPT 99204 $185.00.\" prints `Wardlaw Orthopedics, CMS-1500, March 15, 1980: $185.00`. In a visit note dated January 16, \"Follow-up for collision of 01/09/2026, visit charge $150.00.\" prints January 9. That replaces the correct visit date with the accident date. Before T-202, the letter printed the record date here, which was right. letter_check passes all four wrong letters with 0 violations.\n\n**Major.**\n- **The letter contradicts its own quote.** When the code cannot settle a date that the bill does write, the letter line says \"service date not stated\", and the quote directly under it shows the date of service.\n- **The confirm note leads nowhere.** It asks me to confirm the date, but nothing I confirm can reach the letter.\n\n**Scope.**\n- **Build:** `git archive 986fc55` (archive commit id printed 986fc551078a…) extracted to the session scratchpad (pr2_986fc55/).\n- **Server:** fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local (health: demo_mode true), http://127.0.0.1:7976.\n- **Shutdown:** listener PID 49534 killed. `lsof` exit 1, `curl` 000.\n- **Comparison:** f0921e4 (round 1 archive) used for the before/after on the new probes.\n- **Private values seen:** 0.\n\n**Deterministic checks first (from the 986fc55 archive):**\n- pytest `test_t202_r2_service_date_layouts.py`, `test_t202_charge_service_dates.py` and `test_t200_undated_charge_label.py`: \"67 passed in 7.14s\" (pytest-t202.out).\n- `python -m evals.letter_check`: `{\"value\": 0, \"cases\": 25, ...}` (letter_check.out).\n\n**Not-stated wording and confirm note, read as a demand letter:**\n- **Where the quote has no date** (lib11 counted ledger lines: `Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00`, quote \"New patient exam charge $250.00\"), the wording is true and pastes cleanly. I would still request a dated itemized bill before sending. The internal notes do not tell me to (minor).\n- **Where the quote states a date the code would not read** (ambiguous numeric, two-digit year, no year, several dates), \"service date not stated\" is false on the page. The adjuster sees the firm say the bill states no date of service, right above a quote that reads \"Date of service 04/05/2026\".\n- **The confirm notes are plain and specific** (\"This line or its bill states more than one date (06/24/2026, 07/08/2026) and the record does not say which one belongs to this charge.\"). But \"Confirm the date from the quote\" is circular when the quote is what is unclear. Nothing I confirm reaches the letter.\n\n**Step 3 (separate frontend card, not graded).** The Step 3 card still shows the statement date bare:\n- case_09: \"Hobbleton Family Clinic, billing statement · March 1, 2026\" (p01.out:95);\n- lib14: \"· November 12, 2026\" (p01.out:163);\n- lib10: \"· June 19, 2026\" (p01.out:240).\n\nThe case API now carries the letter's text for each of these: \"February 2, 2026\", \"September 14, 2026\", \"June 9–12, 2026\" (api_service_date.out).\n\n```json\n{\"card\": \"T-202\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"commit 986fc55 (git archive, commit id 986fc551078a6ed6274cc9dd7a6a9efd0af357e3, extracted to session scratchpad pr2_986fc55/); f0921e4 archive (round 1) for the before/after on the new probes. Demo mode: fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, http://127.0.0.1:7976 (health demo_mode true); listener PID 49534 stopped (lsof exit 1, curl 000). Cases: sample (load-sample tile), case_09 (POST /api/cases with the golden text, then opened in the UI), lib14 and lib10 (library tile); lib11 and two SYNTHETIC case_09 variants in-process. Evidence: artifacts/review-evidence/T-202-paralegal-r2/. Private values seen: 0.\",\n \"exercised\": [\n  \"Read personas/paralegal.md, D-071 + amendment + clarification (memory/ORCHESTRATOR_DECISIONS.md:84-92), my round 1 review, board.py show T-202 (notes, handoff), git show 986fc55 (service_date.py, store.py, export.py, present.py, letter_check.py, api.md)\",\n  \"From the archive: pytest test_t202_r2_service_date_layouts + test_t202_charge_service_dates + test_t200_undated_charge_label '67 passed in 7.14s' (pytest-t202.out); python -m evals.letter_check value 0 over 25 cases (letter_check.out)\",\n  \"Playwright on the running archive app (h.py + p01_cases.py): sample, case_09, lib14, lib10 driven keyboard-first through Steps 1-4; every Step 3 card logged and screenshotted; letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); cmp against my round 1 UI letters: all four identical\",\n  \"GET /api/cases/{token} for the four runs: amounts[].service_date on every charge (api_service_date.out)\",\n  \"Shipped path store.charge_service_date on 38 SYNTHETIC bill shapes: my round 1 texts P1-P10, T1-T3 unchanged, plus N1-N25 (probe_r2.out) and B1-B12 non-service dates (probe_r2b.out); B1-B12 also on f0921e4 (probe_r2b_on_f0921e4.out)\",\n  \"letter_check.charge_date_violations on the round 1 wrong-date letters (T2, T3) and four round 2 wrong-date letters (B7, B8, B9, B12), with right-form controls (probe_eval_teeth_r2.out)\",\n  \"In-process letters + notes (letters_dump_r2.py, all_accepted and counted): sample, case_09, lib14, lib10, lib11, plus SYNTHETIC case_09 variants with an ambiguous DOS and a two-date CMS-1500 (letters/, letters_dump_r2.out), read as a demand letter\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 3, \"letter_dates_correct_on_corpus\": 5, \"adjuster_credibility\": 3},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"A birth, injury/accident, onset, referral or order date next to a charge prints as its date of service; in a visit note it replaces the correct visit date\",\n   \"evidence\": \"artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.out. B7 'Birth date 03/15/1980, CPT 99204 $185.00.' gives 'Wardlaw Orthopedics, CMS-1500, March 15, 1980: $185.00'. B12 'Date of accident 01/19/2026 per intake, 99213 office visit $275.00.' gives 'January 19, 2026'. B11 'Onset 01/09/2026, 97110 ...' gives 'January 9, 2026'. B10 'Referral dated 02/10/2026, MRI charge $2,150.00.' gives 'February 10, 2026'. B3 row 'DOI 01/09/2026   99213   Office visit   $275.00' gives 'January 9, 2026'. Non-bill records: B8 'Follow-up for collision of 01/09/2026, visit charge $150.00.' in a note dated 2026-01-16 gives 'Dr. Alvarez, primary care, January 9, 2026'; B9 MRI report dated 2026-02-20, 'Ordered 02/10/2026, MRI cervical spine charge $2,150.00.' gives 'February 10, 2026'. probe_r2.out N11 (date of current injury) and N12 (DOB) give the same. Cause: service_date.py:297 takes any date in the line's own text unless the word before it is in the billing list at service_date.py:35 (statement, posted, paid ...), which has no birth/DOB, injury/DOI, accident, onset, referral or ordered. The non-bill fallback to the record's date (service_date.py:327) runs only when the sentence has no date. The same on f0921e4 (probe_r2b_on_f0921e4.out), so T-202 brought it in: before T-202 these lines printed the record's date. letter_check has the same blind spot (evals/letter_check.py:189 _BILLING_WORD, :263 _own_dates): B7, B8, B9 and B12 letters give 'violations: []' (probe_eval_teeth_r2.out).\",\n   \"why_it_matters\": \"This is the D-071 error from the other side: a date that is not the date of service, printed in the date-of-service slot. A 1980 service date on a 2026 claim tells the adjuster nobody read the bill. A charge dated to the accident day, or in this sample case to the disputed intake date 01/19, puts the firm's own letter on one side of the DOI conflict the tool must not resolve. B8 is a regression: the visit date was right before T-202. The D-071 amendment allows a date only when it is the one certain service date; a birth or injury date is not one. These shapes are not in the corpus or the demo, but CMS-1500 items 3 (birth date) and 14 (date of current illness or injury) and PI bills' 'DOI' header put these dates next to charge lines on every paste.\",\n   \"fix\": \"Add the non-service leads to the code's deny list: birth, DOB, injury, DOI, accident, DOA, collision, onset, referral or referred, ordered, admit or admission when it stands alone, and 'date of current'. Such a date never becomes the line's date: a bill line with no other date takes the not-stated form; a visit note keeps its own record date. Better still, allow-list: in a bill, take a date from the line's own text only when a service word (DOS, date of service, service date, visit, seen, run of, performed, or a CPT/HCPCS/revenue row under a DOS or Date heading) ties it to the line; otherwise not stated. Mirror the rule in letter_check with its own wording list.\",\n   \"acceptance_test\": \"Unit fixtures on B3, B7, B8, B9, B10, B11, B12, N11 and N12 text: no line prints 1980, the injury, accident or onset date, or the referral or order date. The bills print the not-stated form; B8 prints January 16, 2026 and B9 February 20, 2026. letter_check reports a violation for each of the four wrong letters in probe_eval_teeth_r2.py. Add one SYNTHETIC library or golden case with a DOI/DOB-bearing bill line to the 25-case corpus.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Not-stated wording says 'service date not stated' above a quote that states the date of service; the Step 3 confirm note asks for a confirmation that can never reach the letter\",\n   \"evidence\": \"artifacts/review-evidence/T-202-paralegal-r2/letters/synth_ambiguous_dos-all_accepted-letter.txt (SYNTHETIC case_09 variant, bill dated 2026-06-01). It reads 'Hobbleton Family Clinic, billing statement (statement dated June 1, 2026; service date not stated): $275.00' and then 'Source [Ex. __ / Bates __]: \\\"Date of service 04/05/2026: office visit charge $275.00.\\\"'. probe_r2.out N14 note: 'The date written as 04/05/2026 can be read as month/day or day/month, and the record does not settle which. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.' (service_date.py:66, :76). The same contradiction for a two-digit year (P8 '06/12/26'), a year-less date (N16 'February 2'), and several dates in the quote (N3, N7). No API or UI control takes a confirmed date: grep for service_date/confirm_note in the archive app/ finds only export.py, present.py, service_date.py and store.py, and no write route. The internal notes for the variant say nothing about the date (letters/synth_ambiguous_dos-all_accepted-notes.txt).\",\n   \"why_it_matters\": \"'Service date not stated' is a statement about the record, and here it is untrue: the bill states one, and the letter quotes it one line below. The adjuster reads that as carelessness, or as the firm hiding a date. A Texas paralegal reads 04/05/2026 on a Texas bill as April 5. When she confirms that, the letter still says 'not stated', so she ends up hand-editing the letter in Word, outside the tool and its audit. The note's 'confirm the date from the quote' is circular: the quote is what is unclear, and the chart note or the provider settles it.\",\n   \"fix\": \"Make the not-stated text true for each reason. No date in the line: keep '(statement dated X; service date not stated)'. A date written but not certain: show it verbatim, without reading it: '(date of service as written: \\\"04/05/2026\\\"; statement dated June 1, 2026)'. Several dates: '(claim dates of service 06/24/2026 and 07/08/2026; line date not stated)'. Reword the note so it says where to look: 'Check the visit note or the provider for the date; the letter will print ... until you confirm.' Then let her confirm one reading in Step 3, as the Step 2 date-to-confirm radios do for entries. The confirmed date prints, and the audit records her choice.\",\n   \"acceptance_test\": \"For each reason (ambiguous_numeric, two_digit_year, no_year, several_dates), a fixture letter line never contains 'service date not stated' when its own quote contains a written date. After a Step 3 confirm of '04/05/2026 = April 5, 2026', the letter prints 'April 5, 2026' and the audit holds the confirm event.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The not-stated string differs from the one quoted in the D-071 amendment\",\n   \"evidence\": \"memory/ORCHESTRATOR_DECISIONS.md:88 (amendment) binds '(service date not stated on this line; statement dated X)'. The build prints '(statement dated June 15, 2026; service date not stated)' (service_date.py:58 not_stated_text; letters/lib11-counted-letter.txt, 3 lines), the T-200 form. api.md documents the T-200 form.\",\n   \"why_it_matters\": \"Two binding texts now disagree, and the eval pins whichever the code prints. The amendment's order (absence first, statement date second) reads better to an adjuster: the first thing after the provider is not a date that could be read as the DOS.\",\n   \"fix\": \"Orchestrator to pick one string (see questions_for_chris). Then pin it in the decision, api.md, export and letter_check together.\",\n   \"acceptance_test\": \"grep finds one not-stated wording across ORCHESTRATOR_DECISIONS.md, api.md, service_date.py and evals/letter_check.py.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"A ledger column headed 'Trans Date' is read as the date of service\",\n   \"evidence\": \"artifacts/review-evidence/T-202-paralegal-r2/probe_r2.out N5. Header 'Trans Date   Code   Description             Charges', row '06/11/2026   97140  Manual therapy x1       $70.00' gives 'Larkspur Hollow Physical Therapy, itemized ledger, June 11, 2026: $70.00'. The non-DOS heading list (service_date.py _H_NON) has no 'trans', 'transaction' or 'entry'.\",\n   \"why_it_matters\": \"In some practice-management ledgers the transaction date is the posting date. The amendment says any parse doubt gives the not-stated form, and a heading that does not name the service is a doubt.\",\n   \"fix\": \"Treat a date column whose heading names neither the service (DOS, service, visit) nor a billing step as doubtful, and use the not-stated form. Or add trans/transaction/entry date to the non-DOS headings.\",\n   \"acceptance_test\": \"Unit fixture N5: both lines give the not-stated form with a note naming the 'Trans Date' heading.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"A bill period the code does not parse gets the note 'The line states no date of service', which misdescribes the bill\",\n   \"evidence\": \"probe_r2.out P10 'Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 ...' and N17 'Statement covers period June 28-July 2, 2026. Rev 0120 ...'. Both give the not-stated form (safe) with 'The line states no date of service.' (service_date.py:72).\",\n   \"why_it_matters\": \"The bill does state a service period. Telling me it states none sends me hunting for a missing date, when I could confirm the stated period at a glance. UB-04 FL6 is labelled 'statement covers period'.\",\n   \"fix\": \"Recognize 'from X to Y' after 'dates of service', and 'statement covers period'. When a period phrase is present but not parsed, use a note that names it ('The bill states a period (...) the code could not tie to this line').\",\n   \"acceptance_test\": \"Fixtures P10 and N17 print 'January 23–March 6, 2026' and 'June 28–July 2, 2026', or give a note that quotes the period.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Internal notes say nothing about charge lines printed without a service date (carried from T-200; the class is larger now)\",\n   \"evidence\": \"letters/lib11-counted-notes.txt and letters/synth_ambiguous_dos-all_accepted-notes.txt: grep for 'service date' and 'Confirm the date' over every notes file in letters/ returns nothing. Meanwhile 3 lib11 letter lines and the synthetic line print '(statement dated ...; service date not stated)'.\",\n   \"why_it_matters\": \"The notes are my to-do list before the demand goes out. A charge going to the adjuster without a date of service is the item I most need there, so I can request a dated itemized bill.\",\n   \"fix\": \"Add a notes line per not-stated charge, under BILLS TO REQUEST or a new 'Charges without a date of service' heading: provider, amount, reason (the confirm_note), and 'request a dated itemized bill'.\",\n   \"acceptance_test\": \"lib11 counted notes list the three Fennimoor lines with 'request a dated itemized bill'; the synthetic ambiguous-DOS notes list the $275.00 line with its reason.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from round 1: some charge quotes name neither the service nor the date the line prints\",\n   \"evidence\": \"ui-lib14-letter.txt 'Source [Ex. __ / Bates __]: \\\"charge $187.05.\\\"'; ui-lib10-letter.txt 'Source [Ex. __ / Bates __]: \\\"FL47 total charges $4,920.00.\\\"'. The handoff lists this as not done. The quote span predates T-202.\",\n   \"why_it_matters\": \"I cannot check the printed date against the quote under it. I have to open the record to see that $187.05 is mileage on the 09/14 run.\",\n   \"fix\": \"Quote the bill line from its code or description through the figure.\",\n   \"acceptance_test\": \"Every charge Source line in the 25-case letters contains a service word or code as well as the figure.\"}\n ],\n \"whats_right\": [\n  \"Both round 1 blockers fixed: Posted-first ledgers print the DOS column (T2, N1, N2, N24, N25), headerless two-date rows and the CMS-1500 'X and Y' list give the not-stated form with a specific note\",\n  \"Corpus letters (sample, case_09, lib14, lib10) unchanged and right; lib10 'June 9–12, 2026' under the D-071 clarification; amounts[].service_date.text equals the letter text on all 10 charges\",\n  \"letter_check now fails the round 1 wrong-date letters (posting date; one claim date on a two-date CMS-1500) and passes the right forms\"\n ],\n \"questions_for_chris\": [\n  \"Which not-stated string binds: the amendment's '(service date not stated on this line; statement dated X)' or the T-200 form '(statement dated X; service date not stated)' the build prints?\",\n  \"Outside T-202 (not graded here): in my SYNTHETIC two-date CMS-1500 variant the export gate blocks the coded lines ('Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’', letters_dump_r2.out). A CPT code before 'charge' is read as money, so a CMS-1500 coded line cannot be exported. Should this get its own card?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-03T00:28:54.163Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/draft-T-202-paralegal-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:29:07.834Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/draft-T-202-paralegal-r2.md",
 "old_string": "\"Shipped path store.charge_service_date on 38 SYNTHETIC bill shapes",
 "new_string": "\"Shipped path store.charge_service_date on 50 SYNTHETIC bill shapes"
}
````

### User / tool · 2026-11-03T00:29:07.994Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/draft-T-202-paralegal-r2.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:29:09.734Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/draft-T-202-paralegal-r2.md",
 "old_string": "The same contradiction for a two-digit year (P8 '06/12/26'), a year-less date (N16 'February 2'), and several dates in the quote (N3, N7).",
 "new_string": "The same contradiction arises for a year-less date (N16 'February 2') and for several dates in the quote (P8 '06/12/26 06/13/26', N3, N7)."
}
````

### User / tool · 2026-11-03T00:29:09.841Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/draft-T-202-paralegal-r2.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:29:11.647Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/draft-T-202-paralegal-r2.md",
 "old_string": "A charge dated to the accident day, or in this sample case to the disputed intake date 01/19, puts",
 "new_string": "A charge dated to the accident day, or to an intake date the records dispute (the sample case's 01/09 vs 01/19 conflict), puts"
}
````

### User / tool · 2026-11-03T00:29:11.786Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r2/draft-T-202-paralegal-r2.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:29:14.391Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py artifacts/review-evidence/T-202-paralegal-r2/draft-T-202-paralegal-r2.md; for p in probe_r2.out probe_r2b.out probe_r2b_on_f0921e4.out probe_eval_teeth_r2.out letters/synth_ambiguous_dos-all_accepted-letter.txt letters/synth_ambiguous_dos-all_accepted-notes.txt letters/lib11-counted-letter.txt letters/lib11-counted-notes.txt letters_dump_r2.out api_service_date.out p01.out pytest-t202.out letter_check.out ui-lib14-letter.txt ui-lib10-letter.txt; do ls artifacts/review-evidence/T-202-paralegal-r2/$p >/dev/null || echo MISSING $p; done; echo paths-ok",
 "description": "Validate draft JSON, verdict rule and evidence paths"
}
````

### User / tool · 2026-11-03T00:29:14.536Z

**tool result**
````
json blocks: 1
verdict: fail | severities: ['blocker', 'major', 'minor', 'minor', 'minor', 'minor', 'minor']
verdict rule expects: fail | matches: True
model: claude-opus-5-5 | card: T-202 | persona: paralegal-reviewer
all finding fields present
paths-ok
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:29:16.421Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cp artifacts/review-evidence/T-202-paralegal-r2/draft-T-202-paralegal-r2.md reviews/T-202-paralegal-r2.md && python3 tools/board.py validate reviews/T-202-paralegal-r2.md",
 "description": "Publish review and validate with board"
}
````

### User / tool · 2026-11-03T00:29:16.557Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:29:17.330Z

Now I'll record the memory.

### Assistant · claude-opus-5-5 · 2026-11-03T00:29:25.348Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r2-non-service-date-patterns.md",
 "content": "---\nname: t202-r2-non-service-date-patterns\ndescription: T-202 r2 (986fc55) fail: r1 blockers fixed, but DOB/DOI/accident/onset/referral/order dates in a charge's sentence print as DOS (visit note loses its right date); not-stated text contradicts a dated quote\nmetadata:\n  type: project\n---\n\nReview file: reviews/T-202-paralegal-r2.md (986fc55). Verdict: fail, with 1 blocker, 1 major and 5 minors.\n\n**Fixed since r1**\n- Posted-first ledger now prints the DOS.\n- A CMS-1500 listing \"X and Y\" now prints the not-stated form.\n- Corpus letters are byte-identical to r1.\n- letter_check catches the T2/T3 mis-dates.\n- API amounts[].service_date matches the letter.\n\n**Blocker: non-service dates printed as the date of service**\n- The deny list at service_date.py:35 covers billing words only. Any other date in the charge's own sentence or row becomes its DOS:\n  - \"Birth date 03/15/1980\" → March 15, 1980\n  - \"Date of accident\", \"DOI\", \"Onset\", \"Referral dated\", \"Ordered\"\n- In a visit note it overrides the correct record date (regression vs pre-T-202). letter_check has the same blind spot.\n\n**Major: not-stated text contradicts the quote**\n- The letter says \"service date not stated\" above a quote reading \"Date of service 04/05/2026\".\n- The confirm note has no write path to the letter.\n\n**Minors**\n- The amendment string differs from the T-200 form that the build prints.\n- A \"Trans Date\" column is read as DOS.\n- Unparsed periods get the note \"line states no date\".\n- The notes are silent about undated charges.\n- r1 quote span.\n\n**Why:** next round, re-run probe_r2.py, probe_r2b.py and probe_eval_teeth_r2.py first, all in artifacts/review-evidence/T-202-paralegal-r2/.\n\n**How to apply:**\n- Run letters_dump_r2.py with the SYNTHETIC case_09 variants to read the not-stated wording.\n- Outside the card: the export gate blocks \"CPT 99213 charge $150.00\" on a synthetic CMS-1500 (asked Chris).\n- Mechanics: the server ran on port 7976, through T-060-paralegal-pass4-serve.py with the archive in the scratchpad.\n\nRelated: [[t202-d071-service-date-patterns]], [[t200-undated-charge-label]].\n"
}
````

### User / tool · 2026-11-03T00:29:25.455Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r2-non-service-date-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:29:27.274Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-200 undated charge label](t200-undated-charge-label.md)",
 "new_string": "- [T-202 r2 non-service dates](t202-r2-non-service-date-patterns.md) — 986fc55 fail: DOB/DOI/onset/order date in charge sentence prints as DOS; not-stated text contradicts dated quote\n- [T-200 undated charge label](t200-undated-charge-label.md)"
}
````

### User / tool · 2026-11-03T00:29:27.363Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T00:29:29.686Z

T-202 r2 fails (1 blocker, 1 major, 5 minors): both r1 probes and all four corpus letters are now correct, but a birth/injury/onset/referral/order date in a charge's sentence prints as its date of service (e.g. March 15, 1980), and "service date not stated" prints above quotes that state one (review: /Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r2.md; server PID 49534 stopped; 0 private values).
