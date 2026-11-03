# Subagent: Paralegal r3: T-202 dates (Paralegal r3: T-202 dates)

Source: `agent-ae2af427a872587ef.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T01:25:53.454Z

Re-review T-202, round 3 (final), in /Users/arsis/zlayt-pm-project as the senior PI paralegal, starting from a fresh context. The fix commit is 973b542. Read reviews/T-202-paralegal-r2.md (your round 2), D-071 with all its amendments in memory/ORCHESTRATOR_DECISIONS.md, and the handoff.

Run a `git archive 973b542` copy in demo mode on your own port, and stop your PID afterward.
- Re-run every adversarial bill text from your rounds 1 and 2, including the birth, injury, onset, referral and order dates in a charge's sentence.
- Each line must print either a certain service date or the fillable blank "date of service [__________] (statement dated X)", and never a wrong date.
- Generate the sample, case_09, lib14, lib10 and lib11 letters.
- Judge the blank in a demand letter.

The Step 3 wording is a separate card; don't grade it. Report any private value only as <redacted>. Write reviews/T-202-paralegal-r3.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-opus-5-5 · 2026-11-03T01:25:56.796Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat personas/paralegal.md | head -c 200; echo; ls .claude/agent-memory/paralegal-reviewer/; cat .claude/agent-memory/paralegal-reviewer/t202-d071-service-date-patterns.md .claude/agent-memory/paralegal-reviewer/t202-r2-non-service-date-patterns.md .claude/agent-memory/paralegal-reviewer/t200-undated-charge-label.md .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md .claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md",
 "description": "Read persona head and memory files"
}
````

### User / tool · 2026-11-03T01:25:56.889Z

**tool result**
````
# Persona dossier — paralegal-reviewer

## 1. Identity
**Maria Delgado (fictional), Senior Litigation Paralegal, plaintiff personal-injury firm in Austin, Texas — 9+ years, pre-lit and litigation.
MEMORY.md
d041-date-gate-patterns.md
feedback_reviewer_tooling_quirks.md
feedback_spec_review_patterns.md
frontend-review-patterns.md
gate-m2-r2-patterns.md
gate-m3-patterns.md
golden-set-recurring-findings.md
library-review-patterns.md
manual-entry-split-review-patterns.md
record-format-review-patterns.md
reviewer-api-shape-gotchas.md
reviewer-hook-constraints.md
reviewer-run-pitfalls-pass4.md
t060-pass4-state-patterns.md
t060-pass5-state-patterns.md
t060-ui-polish-patterns.md
t068-dates-to-confirm-patterns.md
t079-library-v2-patterns.md
t114-r3-gap-change-persistence.md
t114-rates-gap-patterns.md
t116-gap-endpoint-patterns.md
t118-lib11-truth-patterns.md
t120-123-patterns.md
t120-r2-patterns.md
t120-r3-patterns.md
t120-r4-patterns.md
t136-r2-t142-patterns.md
t149-r2-overview-patterns.md
t181-guided-ui-patterns.md
t181-r2-patterns.md
t200-undated-charge-label.md
t202-d071-service-date-patterns.md
t202-r2-non-service-date-patterns.md
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
name: t202-r2-non-service-date-patterns
description: T-202 r2 (986fc55) fail: r1 blockers fixed, but DOB/DOI/accident/onset/referral/order dates in a charge's sentence print as DOS (visit note loses its right date); not-stated text contradicts a dated quote
metadata:
  type: project
---

Review file: reviews/T-202-paralegal-r2.md (986fc55). Verdict: fail, with 1 blocker, 1 major and 5 minors.

**Fixed since r1**
- Posted-first ledger now prints the DOS.
- A CMS-1500 listing "X and Y" now prints the not-stated form.
- Corpus letters are byte-identical to r1.
- letter_check catches the T2/T3 mis-dates.
- API amounts[].service_date matches the letter.

**Blocker: non-service dates printed as the date of service**
- The deny list at service_date.py:35 covers billing words only. Any other date in the charge's own sentence or row becomes its DOS:
  - "Birth date 03/15/1980" → March 15, 1980
  - "Date of accident", "DOI", "Onset", "Referral dated", "Ordered"
- In a visit note it overrides the correct record date (regression vs pre-T-202). letter_check has the same blind spot.

**Major: not-stated text contradicts the quote**
- The letter says "service date not stated" above a quote reading "Date of service 04/05/2026".
- The confirm note has no write path to the letter.

**Minors**
- The amendment string differs from the T-200 form that the build prints.
- A "Trans Date" column is read as DOS.
- Unparsed periods get the note "line states no date".
- The notes are silent about undated charges.
- r1 quote span.

**Why:** next round, re-run probe_r2.py, probe_r2b.py and probe_eval_teeth_r2.py first, all in artifacts/review-evidence/T-202-paralegal-r2/.

**How to apply:**
- Run letters_dump_r2.py with the SYNTHETIC case_09 variants to read the not-stated wording.
- Outside the card: the export gate blocks "CPT 99213 charge $150.00" on a synthetic CMS-1500 (asked Chris).
- Mechanics: the server ran on port 7976, through T-060-paralegal-pass4-serve.py with the archive in the scratchpad.

Related: [[t202-d071-service-date-patterns]], [[t200-undated-charge-label]].
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:25:58.023Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-03T01:25:58.031Z

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

### Assistant · claude-opus-5-5 · 2026-11-03T01:25:58.426Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r2.md"
}
````

### User / tool · 2026-11-03T01:25:58.434Z

**tool result**
````
1	# T-202 round 2 (D-071 amendment + clarification) — paralegal review (Maria Delgado, senior PI litigation paralegal)
2	
3	**Verdict: fail.** Both of my round 1 blockers are fixed:
4	- **Posted-first ledger:** prints the DOS column (June 10, June 17).
5	- **CMS-1500 "06/24/2026 and 07/08/2026":** prints the not-stated form, with a clear Step 3 note.
6	
7	The corpus letters (sample, case_09, lib14, lib10) are byte-identical to round 1, and correct. lib10 keeps "June 9–12, 2026" under the D-071 clarification.
8	
9	**Blocker.** More adversarial bill text shows the same class of error from another direction. A non-service date in the charge's own sentence or row is printed as the date of service:
10	- a patient birth date;
11	- the date of injury or accident;
12	- an onset date;
13	- a referral or order date.
14	
15	"Birth date 03/15/1980, CPT 99204 $185.00." prints `Wardlaw Orthopedics, CMS-1500, March 15, 1980: $185.00`. In a visit note dated January 16, "Follow-up for collision of 01/09/2026, visit charge $150.00." prints January 9. That replaces the correct visit date with the accident date. Before T-202, the letter printed the record date here, which was right. letter_check passes all four wrong letters with 0 violations.
16	
17	**Major.**
18	- **The letter contradicts its own quote.** When the code cannot settle a date that the bill does write, the letter line says "service date not stated", and the quote directly under it shows the date of service.
19	- **The confirm note leads nowhere.** It asks me to confirm the date, but nothing I confirm can reach the letter.
20	
21	**Scope.**
22	- **Build:** `git archive 986fc55` (archive commit id printed 986fc551078a…) extracted to the session scratchpad (pr2_986fc55/).
23	- **Server:** fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local (health: demo_mode true), http://127.0.0.1:7976.
24	- **Shutdown:** listener PID 49534 killed. `lsof` exit 1, `curl` 000.
25	- **Comparison:** f0921e4 (round 1 archive) used for the before/after on the new probes.
26	- **Private values seen:** 0.
27	
28	**Deterministic checks first (from the 986fc55 archive):**
29	- pytest `test_t202_r2_service_date_layouts.py`, `test_t202_charge_service_dates.py` and `test_t200_undated_charge_label.py`: "67 passed in 7.14s" (pytest-t202.out).
30	- `python -m evals.letter_check`: `{"value": 0, "cases": 25, ...}` (letter_check.out).
31	
32	**Not-stated wording and confirm note, read as a demand letter:**
33	- **Where the quote has no date** (lib11 counted ledger lines: `Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00`, quote "New patient exam charge $250.00"), the wording is true and pastes cleanly. I would still request a dated itemized bill before sending. The internal notes do not tell me to (minor).
34	- **Where the quote states a date the code would not read** (ambiguous numeric, two-digit year, no year, several dates), "service date not stated" is false on the page. The adjuster sees the firm say the bill states no date of service, right above a quote that reads "Date of service 04/05/2026".
35	- **The confirm notes are plain and specific** ("This line or its bill states more than one date (06/24/2026, 07/08/2026) and the record does not say which one belongs to this charge."). But "Confirm the date from the quote" is circular when the quote is what is unclear. Nothing I confirm reaches the letter.
36	
37	**Step 3 (separate frontend card, not graded).** The Step 3 card still shows the statement date bare:
38	- case_09: "Hobbleton Family Clinic, billing statement · March 1, 2026" (p01.out:95);
39	- lib14: "· November 12, 2026" (p01.out:163);
40	- lib10: "· June 19, 2026" (p01.out:240).
41	
42	The case API now carries the letter's text for each of these: "February 2, 2026", "September 14, 2026", "June 9–12, 2026" (api_service_date.out).
43	
44	```json
45	{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
46	 "scope": "commit 986fc55 (git archive, commit id 986fc551078a6ed6274cc9dd7a6a9efd0af357e3, extracted to session scratchpad pr2_986fc55/); f0921e4 archive (round 1) for the before/after on the new probes. Demo mode: fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, http://127.0.0.1:7976 (health demo_mode true); listener PID 49534 stopped (lsof exit 1, curl 000). Cases: sample (load-sample tile), case_09 (POST /api/cases with the golden text, then opened in the UI), lib14 and lib10 (library tile); lib11 and two SYNTHETIC case_09 variants in-process. Evidence: artifacts/review-evidence/T-202-paralegal-r2/. Private values seen: 0.",
47	 "exercised": [
48	  "Read personas/paralegal.md, D-071 + amendment + clarification (memory/ORCHESTRATOR_DECISIONS.md:84-92), my round 1 review, board.py show T-202 (notes, handoff), git show 986fc55 (service_date.py, store.py, export.py, present.py, letter_check.py, api.md)",
49	  "From the archive: pytest test_t202_r2_service_date_layouts + test_t202_charge_service_dates + test_t200_undated_charge_label '67 passed in 7.14s' (pytest-t202.out); python -m evals.letter_check value 0 over 25 cases (letter_check.out)",
50	  "Playwright on the running archive app (h.py + p01_cases.py): sample, case_09, lib14, lib10 driven keyboard-first through Steps 1-4; every Step 3 card logged and screenshotted; letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); cmp against my round 1 UI letters: all four identical",
51	  "GET /api/cases/{token} for the four runs: amounts[].service_date on every charge (api_service_date.out)",
52	  "Shipped path store.charge_service_date on 50 SYNTHETIC bill shapes: my round 1 texts P1-P10, T1-T3 unchanged, plus N1-N25 (probe_r2.out) and B1-B12 non-service dates (probe_r2b.out); B1-B12 also on f0921e4 (probe_r2b_on_f0921e4.out)",
53	  "letter_check.charge_date_violations on the round 1 wrong-date letters (T2, T3) and four round 2 wrong-date letters (B7, B8, B9, B12), with right-form controls (probe_eval_teeth_r2.out)",
54	  "In-process letters + notes (letters_dump_r2.py, all_accepted and counted): sample, case_09, lib14, lib10, lib11, plus SYNTHETIC case_09 variants with an ambiguous DOS and a two-date CMS-1500 (letters/, letters_dump_r2.out), read as a demand letter"
55	 ],
56	 "verdict": "fail",
57	 "scores": {"verify_quickly": 3, "letter_dates_correct_on_corpus": 5, "adjuster_credibility": 3},
58	 "findings": [
59	  {"severity": "blocker",
60	   "title": "A birth, injury/accident, onset, referral or order date next to a charge prints as its date of service; in a visit note it replaces the correct visit date",
61	   "evidence": "artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.out. B7 'Birth date 03/15/1980, CPT 99204 $185.00.' gives 'Wardlaw Orthopedics, CMS-1500, March 15, 1980: $185.00'. B12 'Date of accident 01/19/2026 per intake, 99213 office visit $275.00.' gives 'January 19, 2026'. B11 'Onset 01/09/2026, 97110 ...' gives 'January 9, 2026'. B10 'Referral dated 02/10/2026, MRI charge $2,150.00.' gives 'February 10, 2026'. B3 row 'DOI 01/09/2026   99213   Office visit   $275.00' gives 'January 9, 2026'. Non-bill records: B8 'Follow-up for collision of 01/09/2026, visit charge $150.00.' in a note dated 2026-01-16 gives 'Dr. Alvarez, primary care, January 9, 2026'; B9 MRI report dated 2026-02-20, 'Ordered 02/10/2026, MRI cervical spine charge $2,150.00.' gives 'February 10, 2026'. probe_r2.out N11 (date of current injury) and N12 (DOB) give the same. Cause: service_date.py:297 takes any date in the line's own text unless the word before it is in the billing list at service_date.py:35 (statement, posted, paid ...), which has no birth/DOB, injury/DOI, accident, onset, referral or ordered. The non-bill fallback to the record's date (service_date.py:327) runs only when the sentence has no date. The same on f0921e4 (probe_r2b_on_f0921e4.out), so T-202 brought it in: before T-202 these lines printed the record's date. letter_check has the same blind spot (evals/letter_check.py:189 _BILLING_WORD, :263 _own_dates): B7, B8, B9 and B12 letters give 'violations: []' (probe_eval_teeth_r2.out).",
62	   "why_it_matters": "This is the D-071 error from the other side: a date that is not the date of service, printed in the date-of-service slot. A 1980 service date on a 2026 claim tells the adjuster nobody read the bill. A charge dated to the accident day, or to an intake date the records dispute (the sample case's 01/09 vs 01/19 conflict), puts the firm's own letter on one side of the DOI conflict the tool must not resolve. B8 is a regression: the visit date was right before T-202. The D-071 amendment allows a date only when it is the one certain service date; a birth or injury date is not one. These shapes are not in the corpus or the demo, but CMS-1500 items 3 (birth date) and 14 (date of current illness or injury) and PI bills' 'DOI' header put these dates next to charge lines on every paste.",
63	   "fix": "Add the non-service leads to the code's deny list: birth, DOB, injury, DOI, accident, DOA, collision, onset, referral or referred, ordered, admit or admission when it stands alone, and 'date of current'. Such a date never becomes the line's date: a bill line with no other date takes the not-stated form; a visit note keeps its own record date. Better still, allow-list: in a bill, take a date from the line's own text only when a service word (DOS, date of service, service date, visit, seen, run of, performed, or a CPT/HCPCS/revenue row under a DOS or Date heading) ties it to the line; otherwise not stated. Mirror the rule in letter_check with its own wording list.",
64	   "acceptance_test": "Unit fixtures on B3, B7, B8, B9, B10, B11, B12, N11 and N12 text: no line prints 1980, the injury, accident or onset date, or the referral or order date. The bills print the not-stated form; B8 prints January 16, 2026 and B9 February 20, 2026. letter_check reports a violation for each of the four wrong letters in probe_eval_teeth_r2.py. Add one SYNTHETIC library or golden case with a DOI/DOB-bearing bill line to the 25-case corpus."},
65	  {"severity": "major",
66	   "title": "Not-stated wording says 'service date not stated' above a quote that states the date of service; the Step 3 confirm note asks for a confirmation that can never reach the letter",
67	   "evidence": "artifacts/review-evidence/T-202-paralegal-r2/letters/synth_ambiguous_dos-all_accepted-letter.txt (SYNTHETIC case_09 variant, bill dated 2026-06-01). It reads 'Hobbleton Family Clinic, billing statement (statement dated June 1, 2026; service date not stated): $275.00' and then 'Source [Ex. __ / Bates __]: \"Date of service 04/05/2026: office visit charge $275.00.\"'. probe_r2.out N14 note: 'The date written as 04/05/2026 can be read as month/day or day/month, and the record does not settle which. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.' (service_date.py:66, :76). The same contradiction arises for a year-less date (N16 'February 2') and for several dates in the quote (P8 '06/12/26 06/13/26', N3, N7). No API or UI control takes a confirmed date: grep for service_date/confirm_note in the archive app/ finds only export.py, present.py, service_date.py and store.py, and no write route. The internal notes for the variant say nothing about the date (letters/synth_ambiguous_dos-all_accepted-notes.txt).",
68	   "why_it_matters": "'Service date not stated' is a statement about the record, and here it is untrue: the bill states one, and the letter quotes it one line below. The adjuster reads that as carelessness, or as the firm hiding a date. A Texas paralegal reads 04/05/2026 on a Texas bill as April 5. When she confirms that, the letter still says 'not stated', so she ends up hand-editing the letter in Word, outside the tool and its audit. The note's 'confirm the date from the quote' is circular: the quote is what is unclear, and the chart note or the provider settles it.",
69	   "fix": "Make the not-stated text true for each reason. No date in the line: keep '(statement dated X; service date not stated)'. A date written but not certain: show it verbatim, without reading it: '(date of service as written: \"04/05/2026\"; statement dated June 1, 2026)'. Several dates: '(claim dates of service 06/24/2026 and 07/08/2026; line date not stated)'. Reword the note so it says where to look: 'Check the visit note or the provider for the date; the letter will print ... until you confirm.' Then let her confirm one reading in Step 3, as the Step 2 date-to-confirm radios do for entries. The confirmed date prints, and the audit records her choice.",
70	   "acceptance_test": "For each reason (ambiguous_numeric, two_digit_year, no_year, several_dates), a fixture letter line never contains 'service date not stated' when its own quote contains a written date. After a Step 3 confirm of '04/05/2026 = April 5, 2026', the letter prints 'April 5, 2026' and the audit holds the confirm event."},
71	  {"severity": "minor",
72	   "title": "The not-stated string differs from the one quoted in the D-071 amendment",
73	   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:88 (amendment) binds '(service date not stated on this line; statement dated X)'. The build prints '(statement dated June 15, 2026; service date not stated)' (service_date.py:58 not_stated_text; letters/lib11-counted-letter.txt, 3 lines), the T-200 form. api.md documents the T-200 form.",
74	   "why_it_matters": "Two binding texts now disagree, and the eval pins whichever the code prints. The amendment's order (absence first, statement date second) reads better to an adjuster: the first thing after the provider is not a date that could be read as the DOS.",
75	   "fix": "Orchestrator to pick one string (see questions_for_chris). Then pin it in the decision, api.md, export and letter_check together.",
76	   "acceptance_test": "grep finds one not-stated wording across ORCHESTRATOR_DECISIONS.md, api.md, service_date.py and evals/letter_check.py."},
77	  {"severity": "minor",
78	   "title": "A ledger column headed 'Trans Date' is read as the date of service",
79	   "evidence": "artifacts/review-evidence/T-202-paralegal-r2/probe_r2.out N5. Header 'Trans Date   Code   Description             Charges', row '06/11/2026   97140  Manual therapy x1       $70.00' gives 'Larkspur Hollow Physical Therapy, itemized ledger, June 11, 2026: $70.00'. The non-DOS heading list (service_date.py _H_NON) has no 'trans', 'transaction' or 'entry'.",
80	   "why_it_matters": "In some practice-management ledgers the transaction date is the posting date. The amendment says any parse doubt gives the not-stated form, and a heading that does not name the service is a doubt.",
81	   "fix": "Treat a date column whose heading names neither the service (DOS, service, visit) nor a billing step as doubtful, and use the not-stated form. Or add trans/transaction/entry date to the non-DOS headings.",
82	   "acceptance_test": "Unit fixture N5: both lines give the not-stated form with a note naming the 'Trans Date' heading."},
83	  {"severity": "minor",
84	   "title": "A bill period the code does not parse gets the note 'The line states no date of service', which misdescribes the bill",
85	   "evidence": "probe_r2.out P10 'Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 ...' and N17 'Statement covers period June 28-July 2, 2026. Rev 0120 ...'. Both give the not-stated form (safe) with 'The line states no date of service.' (service_date.py:72).",
86	   "why_it_matters": "The bill does state a service period. Telling me it states none sends me hunting for a missing date, when I could confirm the stated period at a glance. UB-04 FL6 is labelled 'statement covers period'.",
87	   "fix": "Recognize 'from X to Y' after 'dates of service', and 'statement covers period'. When a period phrase is present but not parsed, use a note that names it ('The bill states a period (...) the code could not tie to this line').",
88	   "acceptance_test": "Fixtures P10 and N17 print 'January 23–March 6, 2026' and 'June 28–July 2, 2026', or give a note that quotes the period."},
89	  {"severity": "minor",
90	   "title": "Internal notes say nothing about charge lines printed without a service date (carried from T-200; the class is larger now)",
91	   "evidence": "letters/lib11-counted-notes.txt and letters/synth_ambiguous_dos-all_accepted-notes.txt: grep for 'service date' and 'Confirm the date' over every notes file in letters/ returns nothing. Meanwhile 3 lib11 letter lines and the synthetic line print '(statement dated ...; service date not stated)'.",
92	   "why_it_matters": "The notes are my to-do list before the demand goes out. A charge going to the adjuster without a date of service is the item I most need there, so I can request a dated itemized bill.",
93	   "fix": "Add a notes line per not-stated charge, under BILLS TO REQUEST or a new 'Charges without a date of service' heading: provider, amount, reason (the confirm_note), and 'request a dated itemized bill'.",
94	   "acceptance_test": "lib11 counted notes list the three Fennimoor lines with 'request a dated itemized bill'; the synthetic ambiguous-DOS notes list the $275.00 line with its reason."},
95	  {"severity": "minor",
96	   "title": "Carried from round 1: some charge quotes name neither the service nor the date the line prints",
97	   "evidence": "ui-lib14-letter.txt 'Source [Ex. __ / Bates __]: \"charge $187.05.\"'; ui-lib10-letter.txt 'Source [Ex. __ / Bates __]: \"FL47 total charges $4,920.00.\"'. The handoff lists this as not done. The quote span predates T-202.",
98	   "why_it_matters": "I cannot check the printed date against the quote under it. I have to open the record to see that $187.05 is mileage on the 09/14 run.",
99	   "fix": "Quote the bill line from its code or description through the figure.",
100	   "acceptance_test": "Every charge Source line in the 25-case letters contains a service word or code as well as the figure."}
101	 ],
102	 "whats_right": [
103	  "Both round 1 blockers fixed: Posted-first ledgers print the DOS column (T2, N1, N2, N24, N25), headerless two-date rows and the CMS-1500 'X and Y' list give the not-stated form with a specific note",
104	  "Corpus letters (sample, case_09, lib14, lib10) unchanged and right; lib10 'June 9–12, 2026' under the D-071 clarification; amounts[].service_date.text equals the letter text on all 10 charges",
105	  "letter_check now fails the round 1 wrong-date letters (posting date; one claim date on a two-date CMS-1500) and passes the right forms"
106	 ],
107	 "questions_for_chris": [
108	  "Which not-stated string binds: the amendment's '(service date not stated on this line; statement dated X)' or the T-200 form '(statement dated X; service date not stated)' the build prints?",
109	  "Outside T-202 (not graded here): in my SYNTHETIC two-date CMS-1500 variant the export gate blocks the coded lines ('Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’', letters_dump_r2.out). A CPT code before 'charge' is read as money, so a CMS-1500 coded line cannot be exported. Should this get its own card?"
110	 ]}
111	```
112	
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:00.447Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"D-071\" memory/ORCHESTRATOR_DECISIONS.md | head; echo ---; awk 'NR>=80 && NR<=110' memory/ORCHESTRATOR_DECISIONS.md; echo; git rev-parse --short HEAD; git log --oneline -8",
 "description": "Read D-071 decisions and git state"
}
````

### User / tool · 2026-11-03T01:26:00.503Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to =80 && NR<=110)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:02.047Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"D-071\" memory/ORCHESTRATOR_DECISIONS.md | head -20",
 "description": "Find D-071 lines"
}
````

### User / tool · 2026-11-03T01:26:02.143Z

**tool result**
````
84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
87:## D-071 amendment — when the service date is not certain, print none and ask the human
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
93:- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:02.827Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git rev-parse --short HEAD; git log --oneline -8; git show --stat 973b542 | head -60",
 "description": "Show git state and fix commit stat"
}
````

### User / tool · 2026-11-03T01:26:02.974Z

**tool result**
````
8aa14e1
8aa14e1 test(qa): T-208 r2 the AI translation label is exempt only with a translated entry's quote; label on an English letter fails
679b63e fix(frontend): T-204 r2 a prepared answer is never the AI's wording on the case rail, AI-check panel, audit, tray, banner or legends; whole-DOM observer walk of the prepared sample; condition waits
b96c08f test(qa): T-208 letter_check fails any AI or model wording in every carrier letter (25 cases, prepared and live); matrix e2e binds the provenance line to the case kind
973b542 feat(backend): T-202 r3 D-071 addendum: every line with no certain service date prints the fillable blank 'date of service [__________] (statement dated X)'; letter_check accepts that form and nothing else for such lines
901ad5a docs(architect): T-207 LLM_VS_CODE rows 2 and 3: charge-line service dates are code-only, an allow-list of positive evidence, fillable blank when not certain (D-071)
5703fc4 fix(backend): T-202 r3 D-071 amendment: a service date is an allow-list of positive evidence (label, service column, row cell, bill period); labeled but unreadable dates print as written; independent letter_check allow-list; notes section for undated charges
79714c6 feat(frontend): T-206 Step 3 names a bill document's date 'statement dated'; confirm note says what to do next
d23687e chore(guard): block git commit-tree and symbolic-ref (T-204 swapped a commit on HEAD by plumbing)
commit 973b54228670299495bd16dbf0072e248a43baf0
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 18:51:17 2026 -0600

    feat(backend): T-202 r3 D-071 addendum: every line with no certain service date prints the fillable blank 'date of service [__________] (statement dated X)'; letter_check accepts that form and nothing else for such lines
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/export.py                           |  6 +-
 app/backend/service_date.py                     | 39 +++++--------
 app/backend/store.py                            |  5 +-
 evals/letter_check.py                           | 47 ++++++----------
 memory/contracts/api.md                         |  2 +-
 tests/e2e/guided/test_round2.py                 |  2 +-
 tests/e2e/guided/test_t205.py                   |  2 +-
 tests/unit/test_t200_undated_charge_label.py    |  8 +--
 tests/unit/test_t202_charge_service_dates.py    |  6 +-
 tests/unit/test_t202_r2_service_date_layouts.py | 16 +++---
 tests/unit/test_t202_r3_allow_list.py           | 73 ++++++++++++++-----------
 11 files changed, 98 insertions(+), 108 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:04.554Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/memory/ORCHESTRATOR_DECISIONS.md",
 "offset": 84,
 "limit": 12
}
````

### User / tool · 2026-11-03T01:26:04.562Z

**tool result**
````
84	## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
85	T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.
86	
87	## D-071 amendment — when the service date is not certain, print none and ask the human
88	T-202 r1 (paralegal + staff): the parser guessed ambiguous dates (04/05/2026; two-digit years), dropped stated years and period ends, took a Posted column for DOS, and spread one date over several lines. Binding: the letter prints a service date only when code finds exactly one unambiguous service date (or one complete period) tied to that bill line by its column header or row; ambiguous numeric order (both parts <= 12 with no locale rule from the record), two-digit years, several candidate dates, a non-DOS column (Posted, Statement, Billed) or any parse doubt -> print "(service date not stated on this line; statement dated X)" and raise a Step 3 note asking the user to confirm the date from the quote. Step 3 shows the same service date the letter will print. letter_check verifies each printed date against that line's own quote (not the whole record) using an independent check, and a fixture set of adversarial bill layouts (posted-before-DOS, CMS-1500 multi-date, month-name periods with years, hyphen-joined periods, ambiguous numerics, two-digit years) runs in the unit suite.
89	
90	## D-072 — The prompt log is built and privacy-reviewed once, last
91	Every review round adds new transcripts (including the reviewer's own), so a per-round clean prompt log cannot stay clean (T-187 r4: the reviewer's own session carries private stems). Binding: (1) QA fixes the rule gaps now (bare work-email domain, hostname stems without suffix, job-folder names; a 'term' entry never overrides the outside-name switch; path tails redacted); (2) the final prompt log is rebuilt once, after the last agent has finished (inside T-188), then one independent privacy sweep runs on that build and on the snapshot, and its own transcript is excluded from the published set (listed in the README as the one omitted file); (3) every reviewer brief from now on says: report private values only as <redacted> with a count, never quote them, not even partially.
92	- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
93	- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
94	
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:05.097Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; python3 tools/board.py show T-202 | tail -60",
 "description": "Show T-202 card"
}
````

### User / tool · 2026-11-03T01:26:05.236Z

**tool result**
````
reviews:
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-202-paralegal.md", "at": "2026-11-02T23:48:12Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "fail", "file": "reviews/T-202-staff-engineer.md", "at": "2026-11-02T23:55:16Z"}
  - {"persona": "paralegal-reviewer", "model": "claude-opus-5-5", "verdict": "fail", "file": "reviews/T-202-paralegal-r2.md", "at": "2026-11-03T00:29:34Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-202-staff-engineer-r2.md", "at": "2026-11-03T00:30:26Z"}
ac:
  - {"n": 1, "text": "per D-071; case_09/lib14/lib10 letters show the service date/period; goldens updated with a diff in the handoff; evals/letter_check.py asserts each dated charge line's date equals the service date in its quote, over all 25 cases incl. a count path; unit + guided e2e green from git archive", "done": true, "evidence": "r3 973b542 (git archive): unit 6121 passed 14 skipped (4 shards), guided e2e 143 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r3_allow_list.py 144 probes (74 red on 986fc55 code before the fix), 24 mutants incl. all->any all killed; corpus charge headers byte-identical (84 lines)"}
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
- 2026-11-03T00:29:34Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-202-paralegal-r2.md; round 2; findings:
    - [blocker] A birth, injury/accident, onset, referral or order date next to a charge prints as its date of service; in a visit note it replaces the correct visit date — fix: Add the non-service leads to the code's deny list: birth, DOB, injury, DOI, accident, DOA, collision, onset, referral or referred, ordered, admit or admission when it stands alone, and 'date of current'. Such a date never 
    - [major] Not-stated wording says 'service date not stated' above a quote that states the date of service; the Step 3 confirm note asks for a confirmation that can never reach the letter — fix: Make the not-stated text true for each reason. No date in the line: keep '(statement dated X; service date not stated)'. A date written but not certain: show it verbatim, without reading it: '(date of s
    - [minor] The not-stated string differs from the one quoted in the D-071 amendment — fix: Orchestrator to pick one string (see questions_for_chris). Then pin it in the decision, api.md, export and letter_check together.
    - [minor] A ledger column headed 'Trans Date' is read as the date of service — fix: Treat a date column whose heading names neither the service (DOS, service, visit) nor a billing step as doubtful, and use the not-stated form. Or add trans/transaction/entry date to the non-DOS headings.
    - [minor] A bill period the code does not parse gets the note 'The line states no date of service', which misdescribes the bill — fix: Recognize 'from X to Y' after 'dates of service', and 'statement covers period'. When a period phrase is present but not parsed, use a note that names it ('The bill states a period (...) the code could not tie to this line').
    - [minor] Internal notes say nothing about charge lines printed without a service date (carried from T-200; the class is larger now) — fix: Add a notes line per not-stated charge, under BILLS TO REQUEST or a new 'Charges without a date of service' heading: provider, amount, reason (the confirm_note), and 'request a dated itemized bill'.
    - [minor] Carried from round 1: some charge quotes name neither the service nor the date the line prints — fix: Quote the bill line from its code or description through the figure.
- 2026-11-03T00:29:34Z orchestrator: assigned: backend
- 2026-11-03T00:29:34Z orchestrator: Round 3 queued until staff r2 lands. Paralegal r2 blocker: a date in prose (birth/injury/onset/referral/order) prints as DOS -> per D-071 amendment a date counts only if tied to a DOS column header, a DOS/service label ('DOS', 'date of service', 'service date', 'seen on', 'visit date') or the charge row's own date cell; any other date = not certain. Major: 'not stated' printed above quotes that do state one.
- 2026-11-03T00:30:26Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-202-staff-engineer-r2.md
- 2026-11-03T00:30:26Z backend: moved changes_requested -> in_progress
- 2026-11-03T00:45:28Z backend:
- 2026-11-03T00:45:37Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, staff r2 minor; card T-207). Exact text to append, nothing else changes.
ROW 2 (Parse dates), append to the "What code does" cell: " Entry dates stay on this strict rule. A charge line's date of service (T-202, D-071) is read by app/backend/service_date.py by an allow-list of positive evidence: only a date tied to the line by a service label in its clause (DOS, date of service, service date, seen on, visit date), by a table heading that names service, or by the one period its bill states for its services counts. A numeric date that reads two ways is resolved only when a reading after the bill's own date is impossible for every labeled end of the date or period (a service cannot follow its statement; D-071 clarification); this is a deterministic rule, not a guess. A two-digit year, a date with no year, a date not on the calendar, or a bill date after its statement or more than five years before it is not read."
ROW 3 (Date of service and provider for an entry), append to the "What code does" cell: " For a charge line the date is not the record's header date (for a bill that is the statement date): code prints the service date or period the bill line itself states (positive evidence only, see row 2); '(date of service as written: \"04/05/2026\"; statement dated June 1, 2026)' when the quote labels a date of service the code cannot read with certainty; and '(statement dated X; service date not stated)' when the quote labels none. Birth, injury, onset, referral, order, authorization, entry, transaction, posted, statement and unlabeled dates are never the date of service." Append to the "Validation" cell: " Charge dates: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 28 mutants of the resolver and the check all fail it) and evals/letter_check.charge_date_violations, an independent per-line scanner over 25 cases (no import of the production parser)."
- 2026-11-03T00:45:37Z backend: (correction: the two empty notes above were a shell slip; the exact LLM_VS_CODE text for the architect is in the note just above and on T-207.)
- 2026-11-03T00:51:33Z backend: FOR ARCHITECT, correction to T-207 (docs/LLM_VS_CODE.md row 3, now stale after T-202 r3 commit 973b542, D-071 addendum). Row 3 currently says a labeled-but-unreadable date "shows as written" and that a quote with no label prints "(statement dated X; service date not stated)". Both are gone. Replace those two sentences with exactly: "Every charge line with no certain service date (the quote labels none, or labels one the code cannot read with certainty) prints the same fillable blank, like the Bates placeholder: 'date of service [__________] (statement dated June 15, 2026)'. The paralegal fills it from the quote; nothing is inferred, and the Step 3 confirm note names the date as the quote writes it." Also in the Validation cell the mutant count is 24, not 28: tests/unit/test_t202_r3_allow_list.py (every reviewer probe is a fixture; 24 mutants of the resolver and the check all fail the unit suite) and evals/letter_check.charge_date_violations, which accepts the blank and nothing else for a line with no certain date.
- 2026-11-03T01:25:40Z backend: AC 1 checked: r3 973b542 (git archive): unit 6121 passed 14 skipped (4 shards), guided e2e 143 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r3_allow_list.py 144 probes (74 red on 986fc55 code before the fix), 24 mutants incl. all->any all killed; corpus charge headers byte-identical (84 lines)
- 2026-11-03T01:25:40Z backend: moved in_progress -> in_review
- 2026-11-03T01:25:49Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer

## Handoff
What changed (r3, 5703fc4 + 973b542): service_date.py is now an ALLOW-LIST: a date is the service date only if a column heading names service (DOS, date of service, from/to service, 24A ...), a service label ends its clause (DOS, date of service, seen on, visit date, visit of, run of; UB-04 'statement covers period'), it is the row cell under such a heading, or (coded bill line with no label) the bill's one period-labeled date. Birth/injury/onset/referral/order/entry/transaction/posted/statement/unlabeled dates are never read; a visit note keeps its own date. Unreadable-but-labeled dates (ambiguous, 2-digit year incl. 'Mar 5, 26', no year, invalid, several, after the statement or >5y before it) and no-label lines ALL print the D-071 addendum blank 'date of service [__________] (statement dated X)' (export.charge_when, store.charge_service_date; confirm_note names the date as written; notes get a CHARGES WITHOUT A CERTAIN DATE OF SERVICE section). evals/letter_check.py: own allow-list scanner (string phrase list, own heading test), accepts the blank and nothing else for a not-certain line, fails a date no label ties, a blank above a certain labeled date, a wrong statement date. api.md updated. | Verified from git archive 973b542: unit 6121 passed/14 skipped, guided e2e 143 passed, letter_check 0 over 25 cases; corpus charge headers byte-identical to 986fc55 (84 lines). New test_t202_r3_allow_list.py: 144 cases, every paralegal/staff probe (B3,B7-B12,N5,N11,N12,N14,N16,N17,P10, Entry/Transaction/Issued/Printed headings, DOI/DOB/authorization, 1998/2031, Mar 5 26, all-vs-any), red first (74 failed on 986fc55 before the fix), 24 mutants (resolver, store, export, letter_check; all->any among them) all killed; production letter vs independent check agree on 45 layouts. | Left: Step 3 frontend text 'type the date into your letter yourself' still describes the old no-blank flow (frontend card); architect T-207 row 3 must be corrected to the blank wording (note on T-207); not done: quote-span minor (charge quotes naming neither service nor date) and a Step 3 control to enter a confirmed date. Crossings: edited tests/e2e/guided/test_round2.py + test_t205.py (one assertion each) and tests/unit test_t200/test_t202_charge (new blank text). | Surprise: a bare 'Date' column and unlabeled leading dates (03/13/2026 exam charge) are now not-certain by the allow-list; existing r2 fixtures needed DOS labels.
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:07.426Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls artifacts/review-evidence/T-202-paralegal-r2/ artifacts/review-evidence/T-202-paralegal/ | head -80; ls artifacts/review-evidence/ | grep -i \"T-060-paralegal-pass4-serve\\|jsoncheck\" ",
 "description": "List prior evidence scripts"
}
````

### User / tool · 2026-11-03T01:26:07.528Z

**tool result**
````
artifacts/review-evidence/T-202-paralegal-r2/:
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

artifacts/review-evidence/T-202-paralegal/:
all_charge_lines.out
all_charge_lines.py
api-amount-fields.out
case09-paste-probe.out
case_09-all_accepted-letter.txt
case_09-all_accepted-notes.txt
case_09-counted-letter.txt
case_09-counted-notes.txt
case_09-s3-00-a1.png
T-013-r2-paralegal-jsoncheck.py
T-013-r3-paralegal-jsoncheck.py
T-015-r2-paralegal-jsoncheck.py
T-015-r3-paralegal-jsoncheck.py
T-015-r4-paralegal-jsoncheck.out.txt
T-015-r4-paralegal-jsoncheck.py
T-039-r2-jsoncheck.py
T-043-paralegal-jsoncheck.py
T-060-paralegal-pass4-serve.py
T-068-paralegal-r2-jsoncheck.py
T-076-r2-paralegal-jsoncheck.py
T-077-T-078-paralegal-r2-jsoncheck.out
T-077-T-078-paralegal-r2-jsoncheck.py
T-077-paralegal-r3-jsoncheck.py
T-104-ux-designer-jsoncheck.py
T-114-paralegal-jsoncheck.py
T-114-r2-paralegal-jsoncheck.py
T-116-paralegal-jsoncheck.py
T-116-paralegal-r2-jsoncheck.py
T-116-paralegal-r5-jsoncheck.out.txt
T-116-paralegal-r5-jsoncheck.py
T-118-paralegal-jsoncheck.py
T-120-123-paralegal-jsoncheck.py
T-120-r3-paralegal-jsoncheck.py
T-194-r2-jsoncheck.py
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:09.235Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.py; echo ======; head -80 artifacts/review-evidence/T-202-paralegal-r2/probe_r2.py",
 "description": "Read r2 probe scripts"
}
````

### User / tool · 2026-11-03T01:26:09.319Z

**tool result**
````
"""T-202 r2 paralegal probe B: non-service dates (birth date, injury/accident date, referral/order date, onset) sitting next to a charge,
in bill and non-bill records, line and sentence layouts. Same shipped path as probe_r2.py (store.charge_service_date). SYNTHETIC text only.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_r2b.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
from app.backend import amounts as AM, store  # noqa: E402

PROBES = [
    ("B1 statement header line with DOI, then a dated charge row", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Patient: J. Roe   DOI: 01/09/2026\n02/02/2026  99213  Office visit  $275.00"),
    ("B2 header line with DOI, then an undated coded row", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Patient: J. Roe   DOI: 01/09/2026\n99213  Office visit  $275.00"),
    ("B3 'DOI 01/09/2026' in the same row as an undated coded charge", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "DOI 01/09/2026   99213   Office visit   $275.00"),
    ("B4 sentence: 'Injury date 01/09/2026. Office visit 99213 $275.00.'", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Injury date 01/09/2026. Office visit 99213 $275.00."),
    ("B5 sentence: 'For injuries of 01/09/2026, office visit 99213 $275.00.'", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "For injuries of 01/09/2026, office visit 99213 $275.00."),
    ("B6 CMS-1500 flattened: DOB field then a coded line, one sentence", "Wardlaw Orthopedics, CMS-1500", "2026-07-14",
     "Item 3 patient birth date 03/15/1980; Item 24 CPT 99204 $185.00."),
    ("B7 CMS-1500 flattened: DOB with comma, coded line", "Wardlaw Orthopedics, CMS-1500", "2026-07-14",
     "Birth date 03/15/1980, CPT 99204 $185.00."),
    ("B8 non-bill follow-up note mentions the collision date and a fee", "Dr. Alvarez, primary care", "2026-01-16",
     "Follow-up for collision of 01/09/2026, visit charge $150.00."),
    ("B9 MRI report (non-bill) with ordered date in the charge sentence", "Riverside Imaging, MRI report", "2026-02-20",
     "Ordered 02/10/2026, MRI cervical spine charge $2,150.00."),
    ("B10 bill: 'Referral dated 02/10/2026, MRI charge $2,150.00'", "Riverside Imaging, billing statement", "2026-03-01",
     "Referral dated 02/10/2026, MRI charge $2,150.00."),
    ("B11 bill: 'Onset 01/09/2026, 97110 therapeutic exercise $95.00'", "Capital PT, billing statement", "2026-03-20",
     "Onset 01/09/2026, 97110 therapeutic exercise $95.00."),
    ("B12 bill: 'Date of accident 01/19/2026 per intake; 99213 $275.00'", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Date of accident 01/19/2026 per intake, 99213 office visit $275.00."),
]

for label, src, rd, ex in PROBES:
    print(f"== {label}  (record date {rd}; source '{src}'; billing_document={AM.billing_document(src, ex)})")
    print("   " + ex.replace("\n", "\n   "))
    rec = {"id": "r1", "n": 1, "source": src, "date_iso": rd, "excerpt": ex, "text": ex}
    for a in AM.find_amounts(ex):
        if a.get("cents") is None:
            continue
        item = {"excerpt": ex, "value_cents": a["cents"], "raw": a["raw"], "excerpt_start": 0}
        d = store.charge_service_date(item, rec, a["start"])
        line = f"{src}, {d['text']}" if d["state"] == "stated" else f"{src} {d['text']}"
        print(f"   {a['raw']:>10} -> letter head: '{line}: {a['raw']}'  state={d['state']} reason={d['reason']}")
        if d["confirm_note"]:
            print(f"              Step 3 note: {d['confirm_note']}")
======
"""T-202 r2 paralegal probe: for each charge figure on SYNTHETIC bill shapes, the Step 3 / letter service-date value the shipped path returns
(store.charge_service_date -> service_date.resolve), i.e. the exact text the letter prints after the provider, plus reason and confirm note.
Includes my r1 shapes (P1-P10, T1-T3) unchanged and new adversarial shapes (N*). Run from repo root on the 986fc55 archive:
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_r2.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
from app.backend import amounts as AM, store  # noqa: E402

PROBES = [
    # r1 shapes, unchanged text
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
    ("P8 ledger row DOS then posted, two-digit years", "Fennimoor Spine Clinic, itemized ledger", "2026-06-15",
     "06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00. 06/12/26 06/13/26 97110 Therapeutic exercise charge $95.00."),
    ("P9 statement period then a separately dated line", "Saltmarrow General Hospital, UB-04 itemized bill", "2026-06-19",
     "UB-04 statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, service date 06/09/2026, FL47 total charges $2,105.00."),
    ("P10 'from X to Y' dates of service", "Capital PT, billing statement", "2026-03-20",
     "Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 therapeutic exercise, 9 units, charge $1,665.00."),
    ("T1 ledger table: DOS + posted columns", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "Itemized ledger\nDOS         Posted      CPT    Description            Charges    Balance\n"
     "06/10/2026  06/11/2026  97140  Manual therapy x1      $70.00     $70.00\n"
     "06/17/2026  06/18/2026  97110  Therapeutic exercise   $95.00     $165.00"),
    ("T2 ledger table: posted column first (r1 blocker)", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "Itemized ledger\nPosted      DOS         CPT    Description            Charges    Balance\n"
     "06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00     $70.00\n"
     "06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00     $165.00"),
    ("T3 CMS-1500, two dates of service joined by 'and' (r1 blocker)", "Wardlaw Orthopedics, CMS-1500", "2026-07-14",
     "CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, $185.00, 1 unit; CPT 20610, $210.00, 1 unit. Item 28 TOTAL CHARGE $395.00. Item 29 AMOUNT PAID $0.00."),
    # new adversarial shapes
    ("N1 posted-first ledger, uppercase header, pipes", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "POSTED     | SVC DATE   | CODE  | DESCRIPTION          | CHARGE\n"
     "06/11/2026 | 06/10/2026 | 97140 | Manual therapy x1    | $70.00\n"
     "06/18/2026 | 06/17/2026 | 97110 | Therapeutic exercise | $95.00"),
    ("N2 posted-first ledger, header 'Post Date / Date of Service'", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "Post Date    Date of Service   Code   Description             Amount\n"
     "06/11/2026   06/10/2026        97140  Manual therapy x1       $70.00\n"
     "06/18/2026   06/17/2026        97110  Therapeutic exercise    $95.00"),
    ("N3 posted-first rows, NO header", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00\n"
     "06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00"),
    ("N4 posted-first, header uses generic 'Date' for the DOS column", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "Posted      Date        CPT    Description            Charges\n"
     "06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00\n"
     "06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00"),
    ("N5 ledger with only a 'Trans Date' column (transaction date)", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "Trans Date   Code   Description             Charges\n"
     "06/11/2026   97140  Manual therapy x1       $70.00\n"
     "06/18/2026   97110  Therapeutic exercise    $95.00"),
    ("N6 sentence ledger: 'Posted X for DOS Y'", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "Posted 06/11/2026 for DOS 06/10/2026: manual therapy $70.00. Posted 06/18/2026 for DOS 06/17/2026: therapeutic exercise $95.00."),
    ("N7 sentence: date then 'posted' after it", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "06/11/2026 posted, DOS 06/10/2026, manual therapy $70.00."),
    ("N8 CMS-1500 with per-line item 24A dates", "Wardlaw Orthopedics, CMS-1500", "2026-07-14",
     "CMS-1500. Item 24A 06/24/2026 CPT 99204 $185.00. Item 24A 07/08/2026 CPT 20610 $210.00. Item 28 TOTAL CHARGE $395.00."),
    ("N9 CMS-1500 'dates of service 06/24/2026, 07/08/2026' (comma list)", "Wardlaw Orthopedics, CMS-1500", "2026-07-14",
     "Dates of service 06/24/2026, 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00."),
    ("N10 CMS-1500 'from 06/24/2026 to 07/08/2026' (claim span, 2 discrete visits)", "Wardlaw Orthopedics, CMS-1500", "2026-07-14",
     "CMS-1500 dates of service from 06/24/2026 to 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00."),
    ("N11 CMS-1500 with DOI in the same sentence as a coded line", "Wardlaw Orthopedics, CMS-1500", "2026-07-14",
     "Item 14 date of current injury 05/30/2026, CPT 99204 office visit $185.00."),
    ("N12 CMS-1500 with patient DOB in the same sentence", "Wardlaw Orthopedics, CMS-1500", "2026-07-14",
     "Patient DOB 03/15/1980, CPT 99204 office visit $185.00."),
    ("N13 accident date leading a bill line", "Hobbleton Family Clinic, billing statement", "2026-03-01",
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:13.587Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/pr3_973b542 && git archive 973b542 | tar -x -C $S/pr3_973b542 && ls $S/pr3_973b542 && git cat-file -p 973b542 | head -1",
 "description": "Extract 973b542 archive into scratchpad"
}
````

### User / tool · 2026-11-03T01:26:14.823Z

**tool result**
````
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
tree 4c457a4bfb6ce59201dc8733a89d20edead99f73
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:16.369Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 973b542 -- app/backend/service_date.py app/backend/export.py app/backend/store.py | head -250",
 "description": "Show fix diff for backend"
}
````

### User / tool · 2026-11-03T01:26:16.483Z

**tool result**
````
commit 973b54228670299495bd16dbf0072e248a43baf0
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 18:51:17 2026 -0600

    feat(backend): T-202 r3 D-071 addendum: every line with no certain service date prints the fillable blank 'date of service [__________] (statement dated X)'; letter_check accepts that form and nothing else for such lines
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/export.py b/app/backend/export.py
index 172a8c9..7258766 100644
--- a/app/backend/export.py
+++ b/app/backend/export.py
@@ -215,7 +215,7 @@ class _View:
     def charge_when(self, a):
         """D-071 (extends T-200): the label before a charge's amount in the letter. A date there reads as the date of service, so it is the service date the charge's own bill line
         states (store.charge_service_dates; a period prints as a range, `_date_range`), never the record's date, which for a bill is the statement's. A line that states none is
-        NEVER given the record's date bare: 'Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated)'. Chosen over dropping the date
+        NEVER given the record's date bare: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026)' (D-071 addendum: a fillable blank). Chosen over dropping the date
         because the adjuster can still match the line to the ledger page, and it agrees with the review screen's 'No date of service (statement dated ...)'. A case dict
         without `dos_iso` (a hand-built one) keeps the record's date."""
         n, src = a["record_no"], self.source(a["record_no"])
@@ -223,7 +223,7 @@ class _View:
             return f"{src}, {_long_date(self.rec_date(n))}"
         if a["dos_iso"]:
             return f"{src}, {_date_range(a['dos_iso'], a.get('dos_end_iso'))}"
-        return f"{src} {a.get('dos_text') or service_date.not_stated_text(self.rec_date(n))}"
+        return f"{src}, {a.get('dos_text') or service_date.not_stated_text(self.rec_date(n))}"
 
     def cite(self, n):
         return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"
@@ -611,7 +611,7 @@ def _undated_charges(v):
     for a in v.in_charges:
         if "dos_iso" in a and not a["dos_iso"]:
             why = (a.get("dos_note") or "The line states no date of service.").split(" The letter prints")[0]
-            out.append(f"- {_provider(v.source(a['record_no'])) or v.source(a['record_no'])}, {a['raw']}: {why} Printed in the letter without a certain service date; request a dated itemized bill from the provider.")
+            out.append(f"- {_provider(v.source(a['record_no'])) or v.source(a['record_no'])}, {a['raw']}: {why} The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.")
     return out
 
 
diff --git a/app/backend/service_date.py b/app/backend/service_date.py
index ad74b80..3a541e3 100644
--- a/app/backend/service_date.py
+++ b/app/backend/service_date.py
@@ -11,10 +11,12 @@ Any other date (birth, injury, onset, referral, order, authorization, entry, tra
 looked at again: an unlabeled date cannot become the line's date by default. The result is one of:
   - `stated`: exactly one unambiguous labeled date or complete period (a numeric date that reads two ways is resolved only by 'a service cannot follow its statement', and only when
     EVERY labeled end then reads one way; a stated date after its statement, or more than five years before it, in a bill is doubtful);
-  - `not_stated` with reason `no_date` / `non_service_date`: the quote labels no date of service. The letter prints the T-200 form '(statement dated X; service date not stated)';
-    a dated encounter note (visit note, imaging report: not a bill) keeps the note's own date;
+  - `not_stated` with reason `no_date` / `non_service_date`: the quote labels no date of service; a dated encounter note (visit note, imaging report: not a bill) keeps the
+    note's own date;
   - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): the quote DOES label a date of service and
-    the code cannot read it with certainty. The letter prints it AS WRITTEN ('date of service as written: "04/05/2026"; statement dated X'), never under 'service date not stated'.
+    the code cannot read it with certainty; the note names the date as the quote writes it.
+  Every not-stated line prints the same fillable blank (D-071 addendum): 'date of service [__________] (statement dated X)'. The paralegal fills it from the quote; nothing is inferred,
+  and the letter never says "service date not stated" above a quote that states one.
 Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
 (`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
 import datetime as _dt
@@ -53,7 +55,7 @@ _H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|vi
 _YEARS_BEFORE = 5                # a bill's service date more than this many years before its statement is doubtful
 
 REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "implausible", "non_service_date", "no_date")
-WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty: the letter prints it as written
+WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)
 
 
 def display(first, last=None) -> str:
@@ -71,30 +73,19 @@ def display(first, last=None) -> str:
     return f"{lng(first)}–{lng(last)}"
 
 
-def not_stated_text(statement_iso) -> str:
-    """The text the letter puts after the provider when the quote labels no date of service (T-200)."""
-    if statement_iso:
-        return f"(statement dated {display(statement_iso)}; service date not stated)"
-    return "(service date not stated)"
+BLANK = "date of service [__________]"
 
 
-def as_written_text(raws, statement_iso) -> str:
-    """The text the letter puts after the provider when the quote LABELS a date of service the code cannot read with certainty: the date as the quote writes it, never read.
-    '(date of service as written: "04/05/2026"; statement dated June 1, 2026)'; several: '(dates of service as written: "06/24/2026" and "07/08/2026"; not tied to this line; ...)'."""
-    q = [f'"{" ".join(str(r).split())}"' for r in raws]
-    if len(q) == 1:
-        body = f"date of service as written: {q[0]}"
-    else:
-        body = "dates of service as written: " + (", ".join(q[:-1]) + " and " + q[-1]) + "; not tied to this line"
+def not_stated_text(statement_iso) -> str:
+    """The text the letter puts after the provider when no service date is certain (D-071 addendum): a fillable blank, like the Bates placeholder, never an inferred date. The
+    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)'."""
     if statement_iso:
-        body += f"; statement dated {display(statement_iso)}"
-    return f"({body})"
+        return f"{BLANK} (statement dated {display(statement_iso)})"
+    return BLANK
 
 
 def printed_text(res: dict, statement_iso) -> str:
-    """The text the letter prints after the provider for a resolved line that is not stated."""
-    if res.get("reason") in WRITTEN and res.get("raws"):
-        return as_written_text(res["raws"], statement_iso)
+    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
     return not_stated_text(statement_iso)
 
 
@@ -108,8 +99,8 @@ _WHY = {
     "non_service_date": "The only date near this line ({raw}) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service).",
     "no_date": "The line states no date of service.",
 }
-_ASK_WRITTEN = " The letter prints no service date for this line. It shows the date as written. Confirm the date from the quote before you rely on it."
-_ASK_NONE = " The letter prints no service date for this line. Request a dated itemized bill before you rely on it."
+_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
+_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it."
 
 
 def confirm_note(reason, raw) -> str:
diff --git a/app/backend/store.py b/app/backend/store.py
index bb5d543..861cec9 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -117,9 +117,8 @@ def amount_pos(item: dict, rec):
 
 def charge_service_date(item: dict, rec, pos) -> dict:
     """D-071 (extends T-200, amended in T-202 r2): what a charge line prints as its date, and why, for the letter AND the case view (Step 3 shows exactly this).
-    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', '(statement dated June 15, 2026; service date
-    not stated)' when the quote labels no date of service, or '(date of service as written: "04/05/2026"; statement dated June 15, 2026)' when it labels one the code cannot read
-    with certainty), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
+    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or the fillable blank 'date of service [__________] (statement dated June 15, 2026)'
+    when no service date is certain), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
     A date is stated only when positive evidence ties it to the line (service_date.resolve, an allow-list): a service label in its clause, a column heading that names service, or
     the one period its bill states; an unlabeled date (birth, injury, referral, entry, transaction ...) is never the service date. The record's date of a ledger, invoice or UB-04 is the statement's, never a fallback: a bill line the code cannot read has no
     service date. A dated encounter record's (visit note, imaging report) date is the visit. A charge the paralegal counted for a missing date of service (D-064) is
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:32.170Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; sed -n 80,200p artifacts/review-evidence/T-202-paralegal-r2/probe_r2.py; echo =====; cat artifacts/review-evidence/T-202-paralegal-r2/probe_eval_teeth_r2.py",
 "description": "Read rest of probe_r2 and eval teeth probe"
}
````

### User / tool · 2026-11-03T01:26:32.267Z

**tool result**
````
    ("N13 accident date leading a bill line", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Date of accident 01/09/2026, office visit charge $275.00."),
    ("N14 ambiguous numeric, both readings before statement", "Hobbleton Family Clinic, billing statement", "2026-06-01",
     "Date of service 04/05/2026: office visit charge $275.00."),
    ("N15 ambiguous numeric, one reading after statement (D-071 clarification)", "Hobbleton Family Clinic, billing statement", "2026-04-30",
     "Date of service 04/05/2026: office visit charge $275.00."),
    ("N16 month-name date with no year", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Office visit on February 2: charge $275.00."),
    ("N17 month-name period with year", "Saltmarrow General Hospital, UB-04 itemized bill", "2026-07-10",
     "Statement covers period June 28-July 2, 2026. Rev 0120 room and board $4,920.00."),
    ("N18 'statement period' but prior-balance date in same sentence", "Saltmarrow General Hospital, UB-04 itemized bill", "2026-07-10",
     "Previous balance as of 05/31/2026 $100.00; Rev 0450 emergency room 06/09/2026 $2,105.00."),
    ("N19 payment-first sentence then charge", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Payment received 02/20/2026 $50.00, office visit charge $275.00."),
    ("N20 UB-04 FL6 6-digit from/through", "Saltmarrow General Hospital, UB-04", "2026-06-19",
     "FL6 statement covers period FROM 060926 THROUGH 061226. Rev 0450 emergency room FL47 $2,105.00."),
    ("N21 admit / discharge dates", "Saltmarrow General Hospital, UB-04", "2026-06-19",
     "Admit 06/09/2026, discharge 06/12/2026, Rev 0120 room and board $4,920.00."),
    ("N22 date after the figure", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Office visit charge $275.00 on 02/02/2026."),
    ("N23 visit note (not a bill) with a fee, no date in sentence", "Dr. Alvarez, primary care", "2026-01-16",
     "Office visit level 3. Fee $150.00."),
    ("N24 ledger: two posted dates then DOS in row, header names all", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "Billed       Posted      DOS         CPT    Charges\n"
     "06/12/2026   06/11/2026  06/10/2026  97140  $70.00"),
    ("N25 ISO dates in a posted-first ledger", "Larkspur Hollow Physical Therapy, itemized ledger", "2026-07-01",
     "Posted      DOS         CPT    Charges\n"
     "2026-06-11  2026-06-10  97140  $70.00"),
]

for label, src, rd, ex in PROBES:
    print(f"== {label}  (record date {rd}; source '{src}')")
    print("   " + ex.replace("\n", "\n   "))
    rec = {"id": "r1", "n": 1, "source": src, "date_iso": rd, "excerpt": ex, "text": ex}
    for a in AM.find_amounts(ex):
        if a.get("cents") is None:
            continue
        item = {"excerpt": ex, "value_cents": a["cents"], "raw": a["raw"], "excerpt_start": 0}
        d = store.charge_service_date(item, rec, a["start"])
        line = f"{src}, {d['text']}" if d["state"] == "stated" else f"{src} {d['text']}"
        print(f"   {a['raw']:>10} -> letter head: '{line}: {a['raw']}'  state={d['state']} reason={d['reason']}")
        if d["confirm_note"]:
            print(f"              Step 3 note: {d['confirm_note']}")
=====
"""T-202 r2 paralegal: does evals/letter_check.charge_date_violations (986fc55) catch a wrong-but-stated date?
r1 shapes (posting date printed as DOS; CMS-1500 'and' list -> one claim date) and r2 shapes (birth date, accident date, collision date in a visit note,
order date in an imaging report printed as the date of service), each next to the correct form as a control. SYNTHETIC text only.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/probe_eval_teeth_r2.py <archive_root>
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
B7 = "Birth date 03/15/1980, CPT 99204 $185.00."
B8 = "Follow-up for collision of 01/09/2026, visit charge $150.00."
B9 = "Ordered 02/10/2026, MRI cervical spine charge $2,150.00."
B12 = "Date of accident 01/19/2026 per intake, 99213 office visit $275.00."


def letter(head, fig, quote):
    return f"BILLED CHARGES\n\n{head}: {fig}\nSource [Ex. __ / Bates __]: \"{quote}\"\n\nBilled charges accepted from these records: {fig}"


def rec(src, rd, ex):
    return [{"n": 1, "source": src, "date_iso": rd, "excerpt": ex}]


L = "Larkspur Hollow Physical Therapy, itemized ledger"
W = "Wardlaw Orthopedics, CMS-1500"
cases = [
    ("T2 posting date printed as DOS (wrong)", rec(L, "2026-07-01", T2), letter(f"{L}, June 11, 2026", "$70.00", "06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00")),
    ("T2 DOS printed (right)", rec(L, "2026-07-01", T2), letter(f"{L}, June 10, 2026", "$70.00", "06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00")),
    ("T3 injection line dated with the other claim date (wrong)", rec(W, "2026-07-14", T3), letter(f"{W}, June 24, 2026", "$210.00", "CPT 20610, $210.00, 1 unit")),
    ("T3 not-stated form (right)", rec(W, "2026-07-14", T3), letter(f"{W} (statement dated July 14, 2026; service date not stated)", "$210.00", "CPT 20610, $210.00, 1 unit")),
    ("B7 birth date printed as DOS (what 986fc55 prints)", rec(W, "2026-07-14", B7), letter(f"{W}, March 15, 1980", "$185.00", B7.rstrip("."))),
    ("B8 collision date printed for a 01/16 visit note's charge (what 986fc55 prints)", rec("Dr. Alvarez, primary care", "2026-01-16", B8),
     letter("Dr. Alvarez, primary care, January 9, 2026", "$150.00", B8.rstrip("."))),
    ("B9 order date printed for a 02/20 MRI report's charge (what 986fc55 prints)", rec("Riverside Imaging, MRI report", "2026-02-20", B9),
     letter("Riverside Imaging, MRI report, February 10, 2026", "$2,150.00", B9.rstrip("."))),
    ("B12 intake accident date printed as DOS (what 986fc55 prints)", rec("Hobbleton Family Clinic, billing statement", "2026-03-01", B12),
     letter("Hobbleton Family Clinic, billing statement, January 19, 2026", "$275.00", B12.rstrip("."))),
]
for label, recs, txt in cases:
    print(f"== {label}\n   violations: {LC.charge_date_violations(txt, recs)}")
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:52.821Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/probe_r3.py",
 "content": "\"\"\"T-202 r3 paralegal probe: every SYNTHETIC bill text from rounds 1 and 2 (probe_r2.py P1-P10, T1-T3, N1-N25; probe_r2b.py B1-B12), loaded verbatim\nfrom those files with ast, plus new round 3 shapes (R*), through the shipped path store.charge_service_date (the same call Step 3 and the letter use).\nPrints the letter head exactly as export.charge_when builds it on 973b542: f\"{src}, {text}: {raw}\".\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/probe_r3.py <archive_root> <repo_root>\n\"\"\"\nimport ast\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nrepo = os.path.abspath(sys.argv[2])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, store  # noqa: E402\n\n\ndef load(path):\n    tree = ast.parse(open(path).read())\n    for node in tree.body:\n        if isinstance(node, ast.Assign) and getattr(node.targets[0], \"id\", \"\") == \"PROBES\":\n            return ast.literal_eval(node.value)\n    raise SystemExit(f\"no PROBES in {path}\")\n\n\nev = os.path.join(repo, \"artifacts/review-evidence/T-202-paralegal-r2\")\nPROBES = load(os.path.join(ev, \"probe_r2.py\")) + load(os.path.join(ev, \"probe_r2b.py\"))\n\nV = \"Dr. Alvarez, primary care\"\nH = \"Hobbleton Family Clinic, billing statement\"\nL = \"Larkspur Hollow Physical Therapy, itemized ledger\"\nW = \"Wardlaw Orthopedics, CMS-1500\"\nPROBES += [\n    # round 3: shapes aimed at the allow-list itself (labels that tie a date that is still not this line's service)\n    (\"R1 visit note: next visit date in the charge sentence\", V, \"2026-01-16\",\n     \"Next visit date 01/30/2026, office visit charge $150.00.\"),\n    (\"R2 visit note: prior visit 'seen on' in the charge sentence\", V, \"2026-01-16\",\n     \"Previously seen on 01/09/2026 in the ER, follow-up visit charge $150.00.\"),\n    (\"R3 bill: return visit date label after the charge's own DOS\", H, \"2026-03-01\",\n     \"Date of service 02/02/2026, office visit charge $275.00, return visit date 02/16/2026.\"),\n    (\"R4 bill: DOS label tied to the accident ('date of service of the accident')\", H, \"2026-03-01\",\n     \"Date of injury 01/09/2026; date of service 02/02/2026; 99213 office visit $275.00.\"),\n    (\"R5 ledger: header 'Visit Type  Date  Charge' (heading names visit, but the date column is bare 'Date')\", L, \"2026-07-01\",\n     \"Visit Type     Date         Code   Charge\\n\"\n     \"Follow-up     06/10/2026   97140  $70.00\\n\"\n     \"Follow-up     06/17/2026   97110  $95.00\"),\n    (\"R6 ledger: DOS heading, but a DOB column before it\", L, \"2026-07-01\",\n     \"DOB          DOS          Code   Charge\\n\"\n     \"03/15/1980   06/10/2026   97140  $70.00\"),\n    (\"R7 ledger: 'Injury Date' column then 'Service Date' column\", L, \"2026-07-01\",\n     \"Injury Date   Service Date   Code   Charge\\n\"\n     \"01/09/2026    06/10/2026     97140  $70.00\"),\n    (\"R8 ledger: only 'Injury Date' column\", L, \"2026-07-01\",\n     \"Injury Date   Code   Charge\\n\"\n     \"01/09/2026    97140  $70.00\"),\n    (\"R9 CMS-1500 flattened with item 24A label and DOB on the same line\", W, \"2026-07-14\",\n     \"Item 3 DOB 03/15/1980 Item 24A DOS 06/24/2026 CPT 99204 $185.00.\"),\n    (\"R10 bill: 'DOS' then accident date in same clause\", H, \"2026-03-01\",\n     \"DOS 02/02/2026 (accident 01/09/2026) office visit $275.00.\"),\n    (\"R11 bill: 'run of' with an order date\", \"Tarnwick Fire-Rescue, ambulance invoice\", \"2026-11-12\",\n     \"Call received 09/14/2026; run of 09/14/2026; A0427 ALS emergency transport, charge $1,380.00.\"),\n    (\"R12 visit note: 'Date of service' label is the original ER visit (history)\", V, \"2026-01-16\",\n     \"Patient brings ER bill, date of service 01/09/2026, ER charge $6,240.00.\"),\n    (\"R13 bill: 'Seen on' with referral date first\", H, \"2026-03-01\",\n     \"Referred 01/20/2026, seen on 02/02/2026, office visit charge $275.00.\"),\n    (\"R14 bill: date of service written in words-with-year\", H, \"2026-03-01\",\n     \"Date of service February 2, 2026: office visit charge $275.00.\"),\n    (\"R15 bill: DOS with ordinal ('Feb. 2nd, 2026')\", H, \"2026-03-01\",\n     \"DOS Feb. 2nd, 2026 office visit charge $275.00.\"),\n    (\"R16 bill: DOS 02/02/2026 and statement date 03/01/2026 in one clause\", H, \"2026-03-01\",\n     \"Statement 03/01/2026 for DOS 02/02/2026, office visit $275.00.\"),\n]\n\nfor label, src, rd, ex in PROBES:\n    print(f\"== {label}  (record date {rd}; source '{src}'; billing_document={AM.billing_document(src, ex)})\")\n    print(\"   \" + ex.replace(\"\\n\", \"\\n   \"))\n    rec = {\"id\": \"r1\", \"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex, \"text\": ex}\n    for a in AM.find_amounts(ex):\n        if a.get(\"cents\") is None:\n            continue\n        item = {\"excerpt\": ex, \"value_cents\": a[\"cents\"], \"raw\": a[\"raw\"], \"excerpt_start\": 0}\n        d = store.charge_service_date(item, rec, a[\"start\"])\n        print(f\"   {a['raw']:>10} -> letter head: '{src}, {d['text']}: {a['raw']}'  state={d['state']} reason={d['reason']}\")\n        if d[\"confirm_note\"]:\n            print(f\"              Step 3 note: {d['confirm_note']}\")\n"
}
````

### User / tool · 2026-11-03T01:26:52.922Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/probe_r3.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:56.810Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/probe_r3.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542 /Users/arsis/zlayt-pm-project > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/probe_r3.out 2>&1; echo $?; grep -c \"^==\" artifacts/review-evidence/T-202-paralegal-r3/probe_r3.out",
 "description": "Run r3 probe on archive"
}
````

### User / tool · 2026-11-03T01:26:57.166Z

**tool result**
````
0
66
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:26:58.457Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/probe_r3.out"
}
````

### User / tool · 2026-11-03T01:26:58.647Z

**tool result**
````
1	== P1 two-row ledger, own dates  (record date 2026-03-15; source 'Hobbleton Family Clinic, itemized ledger'; billing_document=True)
2	   Statement date 03/15/2026. 02/02/2026 office visit charge $275.00. 02/16/2026 x-ray charge $150.00. Balance due $425.00.
3	      $275.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger, date of service [__________] (statement dated March 15, 2026): $275.00'  state=not_stated reason=non_service_date
4	              Step 3 note: The only date near this line (02/02/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
5	      $150.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger, date of service [__________] (statement dated March 15, 2026): $150.00'  state=not_stated reason=non_service_date
6	              Step 3 note: The only date near this line (02/16/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
7	      $425.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger, date of service [__________] (statement dated March 15, 2026): $425.00'  state=not_stated reason=no_date
8	              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
9	== P2 CMS-1500 two DOS joined by 'and'  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
10	   CMS-1500 for dates of service 06/24/2026 and 07/08/2026. CPT 99204 charge $185.00. CPT 20610 charge $210.00.
11	      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=several_dates
12	              Step 3 note: The quote labels more than one date of service (06/24/2026, 07/08/2026) and nothing says which one belongs to this charge. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.
13	      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $210.00'  state=not_stated reason=several_dates
14	              Step 3 note: The quote labels more than one date of service (06/24/2026, 07/08/2026) and nothing says which one belongs to this charge. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.
15	== P3 invoice date stated before run date  (record date 2026-11-12; source 'Tarnwick Fire-Rescue, ambulance invoice'; billing_document=True)
16	   Invoice date 11/12/2026. Run of 09/14/2026. A0427 ALS emergency transport, charge $1,380.00.
17	    $1,380.00 -> letter head: 'Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00'  state=stated reason=None
18	== P4 UB-04 period across months  (record date 2026-07-10; source 'Saltmarrow General Hospital, UB-04 itemized bill'; billing_document=True)
19	   UB-04 statement period 06/28/2026 to 07/02/2026. Rev 0120 room and board, FL47 total charges $4,920.00.
20	    $4,920.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 28–July 2, 2026: $4,920.00'  state=stated reason=None
21	== P5 UB-04 period with 'through'  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04 itemized bill'; billing_document=True)
22	   UB-04 statement period 06/09/2026 through 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.
23	    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00'  state=stated reason=None
24	== P6 UB-04 period with hyphen  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04 itemized bill'; billing_document=True)
25	   UB-04 statement period 06/09/2026 - 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.
26	    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00'  state=stated reason=None
27	== P7 statement + DOS label same sentence  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
28	   Statement date 03/01/2026, date of service 02/02/2026: office visit charge $275.00.
29	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
30	== P8 ledger row DOS then posted, two-digit years  (record date 2026-06-15; source 'Fennimoor Spine Clinic, itemized ledger'; billing_document=True)
31	   06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00. 06/12/26 06/13/26 97110 Therapeutic exercise charge $95.00.
32	       $95.00 -> letter head: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $95.00'  state=not_stated reason=non_service_date
33	              Step 3 note: The only date near this line (06/12/26) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
34	== P9 statement period then a separately dated line  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04 itemized bill'; billing_document=True)
35	   UB-04 statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, service date 06/09/2026, FL47 total charges $2,105.00.
36	    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9, 2026: $2,105.00'  state=stated reason=None
37	== P10 'from X to Y' dates of service  (record date 2026-03-20; source 'Capital PT, billing statement'; billing_document=True)
38	   Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 therapeutic exercise, 9 units, charge $1,665.00.
39	    $1,665.00 -> letter head: 'Capital PT, billing statement, January 23–March 6, 2026: $1,665.00'  state=stated reason=None
40	== T1 ledger table: DOS + posted columns  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
41	   Itemized ledger
42	   DOS         Posted      CPT    Description            Charges    Balance
43	   06/10/2026  06/11/2026  97140  Manual therapy x1      $70.00     $70.00
44	   06/17/2026  06/18/2026  97110  Therapeutic exercise   $95.00     $165.00
45	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
46	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
47	       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
48	      $165.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $165.00'  state=stated reason=None
49	== T2 ledger table: posted column first (r1 blocker)  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
50	   Itemized ledger
51	   Posted      DOS         CPT    Description            Charges    Balance
52	   06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00     $70.00
53	   06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00     $165.00
54	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
55	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
56	       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
57	      $165.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $165.00'  state=stated reason=None
58	== T3 CMS-1500, two dates of service joined by 'and' (r1 blocker)  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
59	   CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, $185.00, 1 unit; CPT 20610, $210.00, 1 unit. Item 28 TOTAL CHARGE $395.00. Item 29 AMOUNT PAID $0.00.
60	      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=several_dates
61	              Step 3 note: The quote labels more than one date of service (06/24/2026, 07/08/2026) and nothing says which one belongs to this charge. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.
62	      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $210.00'  state=not_stated reason=several_dates
63	              Step 3 note: The quote labels more than one date of service (06/24/2026, 07/08/2026) and nothing says which one belongs to this charge. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.
64	      $395.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $395.00'  state=not_stated reason=no_date
65	              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
66	        $0.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $0.00'  state=not_stated reason=no_date
67	              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
68	== N1 posted-first ledger, uppercase header, pipes  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
69	   POSTED     | SVC DATE   | CODE  | DESCRIPTION          | CHARGE
70	   06/11/2026 | 06/10/2026 | 97140 | Manual therapy x1    | $70.00
71	   06/18/2026 | 06/17/2026 | 97110 | Therapeutic exercise | $95.00
72	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
73	       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
74	== N2 posted-first ledger, header 'Post Date / Date of Service'  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
75	   Post Date    Date of Service   Code   Description             Amount
76	   06/11/2026   06/10/2026        97140  Manual therapy x1       $70.00
77	   06/18/2026   06/17/2026        97110  Therapeutic exercise    $95.00
78	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
79	       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
80	== N3 posted-first rows, NO header  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
81	   06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00
82	   06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00
83	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, date of service [__________] (statement dated July 1, 2026): $70.00'  state=not_stated reason=non_service_date
84	              Step 3 note: The only date near this line (06/11/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
85	       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, date of service [__________] (statement dated July 1, 2026): $95.00'  state=not_stated reason=non_service_date
86	              Step 3 note: The only date near this line (06/18/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
87	== N4 posted-first, header uses generic 'Date' for the DOS column  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
88	   Posted      Date        CPT    Description            Charges
89	   06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00
90	   06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00
91	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, date of service [__________] (statement dated July 1, 2026): $70.00'  state=not_stated reason=non_service_date
92	              Step 3 note: The only date near this line (06/11/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
93	       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, date of service [__________] (statement dated July 1, 2026): $95.00'  state=not_stated reason=non_service_date
94	              Step 3 note: The only date near this line (06/18/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
95	== N5 ledger with only a 'Trans Date' column (transaction date)  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
96	   Trans Date   Code   Description             Charges
97	   06/11/2026   97140  Manual therapy x1       $70.00
98	   06/18/2026   97110  Therapeutic exercise    $95.00
99	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, date of service [__________] (statement dated July 1, 2026): $70.00'  state=not_stated reason=non_service_date
100	              Step 3 note: The only date near this line (06/11/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
101	       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, date of service [__________] (statement dated July 1, 2026): $95.00'  state=not_stated reason=non_service_date
102	              Step 3 note: The only date near this line (06/18/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
103	== N6 sentence ledger: 'Posted X for DOS Y'  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
104	   Posted 06/11/2026 for DOS 06/10/2026: manual therapy $70.00. Posted 06/18/2026 for DOS 06/17/2026: therapeutic exercise $95.00.
105	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
106	       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 17, 2026: $95.00'  state=stated reason=None
107	== N7 sentence: date then 'posted' after it  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
108	   06/11/2026 posted, DOS 06/10/2026, manual therapy $70.00.
109	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
110	== N8 CMS-1500 with per-line item 24A dates  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
111	   CMS-1500. Item 24A 06/24/2026 CPT 99204 $185.00. Item 24A 07/08/2026 CPT 20610 $210.00. Item 28 TOTAL CHARGE $395.00.
112	      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=non_service_date
113	              Step 3 note: The only date near this line (06/24/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
114	      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $210.00'  state=not_stated reason=non_service_date
115	              Step 3 note: The only date near this line (07/08/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
116	      $395.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $395.00'  state=not_stated reason=no_date
117	              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
118	== N9 CMS-1500 'dates of service 06/24/2026, 07/08/2026' (comma list)  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
119	   Dates of service 06/24/2026, 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.
120	      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=several_dates
121	              Step 3 note: The quote labels more than one date of service (06/24/2026, 07/08/2026) and nothing says which one belongs to this charge. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.
122	      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $210.00'  state=not_stated reason=several_dates
123	              Step 3 note: The quote labels more than one date of service (06/24/2026, 07/08/2026) and nothing says which one belongs to this charge. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.
124	== N10 CMS-1500 'from 06/24/2026 to 07/08/2026' (claim span, 2 discrete visits)  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
125	   CMS-1500 dates of service from 06/24/2026 to 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.
126	      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, June 24–July 8, 2026: $185.00'  state=stated reason=None
127	      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, June 24–July 8, 2026: $210.00'  state=stated reason=None
128	== N11 CMS-1500 with DOI in the same sentence as a coded line  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
129	   Item 14 date of current injury 05/30/2026, CPT 99204 office visit $185.00.
130	      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=non_service_date
131	              Step 3 note: The only date near this line (05/30/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
132	== N12 CMS-1500 with patient DOB in the same sentence  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
133	   Patient DOB 03/15/1980, CPT 99204 office visit $185.00.
134	      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=non_service_date
135	              Step 3 note: The only date near this line (03/15/1980) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
136	== N13 accident date leading a bill line  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
137	   Date of accident 01/09/2026, office visit charge $275.00.
138	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
139	              Step 3 note: The only date near this line (01/09/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
140	== N14 ambiguous numeric, both readings before statement  (record date 2026-06-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
141	   Date of service 04/05/2026: office visit charge $275.00.
142	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated June 1, 2026): $275.00'  state=not_stated reason=ambiguous_numeric
143	              Step 3 note: The quote labels 04/05/2026 as the date of service, and it can be read as month/day or day/month; the record does not settle which. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.
144	== N15 ambiguous numeric, one reading after statement (D-071 clarification)  (record date 2026-04-30; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
145	   Date of service 04/05/2026: office visit charge $275.00.
146	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, April 5, 2026: $275.00'  state=stated reason=None
147	== N16 month-name date with no year  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
148	   Office visit on February 2: charge $275.00.
149	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
150	              Step 3 note: The only date near this line (February 2) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
151	== N17 month-name period with year  (record date 2026-07-10; source 'Saltmarrow General Hospital, UB-04 itemized bill'; billing_document=True)
152	   Statement covers period June 28-July 2, 2026. Rev 0120 room and board $4,920.00.
153	    $4,920.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 28–July 2, 2026: $4,920.00'  state=stated reason=None
154	== N18 'statement period' but prior-balance date in same sentence  (record date 2026-07-10; source 'Saltmarrow General Hospital, UB-04 itemized bill'; billing_document=True)
155	   Previous balance as of 05/31/2026 $100.00; Rev 0450 emergency room 06/09/2026 $2,105.00.
156	      $100.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated July 10, 2026): $100.00'  state=not_stated reason=non_service_date
157	              Step 3 note: The only date near this line (05/31/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
158	    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, date of service [__________] (statement dated July 10, 2026): $2,105.00'  state=not_stated reason=non_service_date
159	              Step 3 note: The only date near this line (06/09/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
160	== N19 payment-first sentence then charge  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
161	   Payment received 02/20/2026 $50.00, office visit charge $275.00.
162	       $50.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $50.00'  state=not_stated reason=non_service_date
163	              Step 3 note: The only date near this line (02/20/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
164	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
165	              Step 3 note: The only date near this line (02/20/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
166	== N20 UB-04 FL6 6-digit from/through  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04'; billing_document=True)
167	   FL6 statement covers period FROM 060926 THROUGH 061226. Rev 0450 emergency room FL47 $2,105.00.
168	    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04, date of service [__________] (statement dated June 19, 2026): $2,105.00'  state=not_stated reason=no_date
169	              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
170	== N21 admit / discharge dates  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04'; billing_document=True)
171	   Admit 06/09/2026, discharge 06/12/2026, Rev 0120 room and board $4,920.00.
172	    $4,920.00 -> letter head: 'Saltmarrow General Hospital, UB-04, date of service [__________] (statement dated June 19, 2026): $4,920.00'  state=not_stated reason=non_service_date
173	              Step 3 note: The only date near this line (06/09/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
174	== N22 date after the figure  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
175	   Office visit charge $275.00 on 02/02/2026.
176	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
177	              Step 3 note: The only date near this line (02/02/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
178	== N23 visit note (not a bill) with a fee, no date in sentence  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; billing_document=False)
179	   Office visit level 3. Fee $150.00.
180	      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
181	== N24 ledger: two posted dates then DOS in row, header names all  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
182	   Billed       Posted      DOS         CPT    Charges
183	   06/12/2026   06/11/2026  06/10/2026  97140  $70.00
184	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
185	== N25 ISO dates in a posted-first ledger  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
186	   Posted      DOS         CPT    Charges
187	   2026-06-11  2026-06-10  97140  $70.00
188	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
189	== B1 statement header line with DOI, then a dated charge row  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
190	   Patient: J. Roe   DOI: 01/09/2026
191	   02/02/2026  99213  Office visit  $275.00
192	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
193	              Step 3 note: The only date near this line (02/02/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
194	== B2 header line with DOI, then an undated coded row  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
195	   Patient: J. Roe   DOI: 01/09/2026
196	   99213  Office visit  $275.00
197	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=no_date
198	              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
199	== B3 'DOI 01/09/2026' in the same row as an undated coded charge  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
200	   DOI 01/09/2026   99213   Office visit   $275.00
201	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
202	              Step 3 note: The only date near this line (01/09/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
203	== B4 sentence: 'Injury date 01/09/2026. Office visit 99213 $275.00.'  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
204	   Injury date 01/09/2026. Office visit 99213 $275.00.
205	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=no_date
206	              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
207	== B5 sentence: 'For injuries of 01/09/2026, office visit 99213 $275.00.'  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
208	   For injuries of 01/09/2026, office visit 99213 $275.00.
209	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
210	              Step 3 note: The only date near this line (01/09/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
211	== B6 CMS-1500 flattened: DOB field then a coded line, one sentence  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
212	   Item 3 patient birth date 03/15/1980; Item 24 CPT 99204 $185.00.
213	      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=no_date
214	              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
215	== B7 CMS-1500 flattened: DOB with comma, coded line  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
216	   Birth date 03/15/1980, CPT 99204 $185.00.
217	      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=non_service_date
218	              Step 3 note: The only date near this line (03/15/1980) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
219	== B8 non-bill follow-up note mentions the collision date and a fee  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; billing_document=False)
220	   Follow-up for collision of 01/09/2026, visit charge $150.00.
221	      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
222	== B9 MRI report (non-bill) with ordered date in the charge sentence  (record date 2026-02-20; source 'Riverside Imaging, MRI report'; billing_document=False)
223	   Ordered 02/10/2026, MRI cervical spine charge $2,150.00.
224	    $2,150.00 -> letter head: 'Riverside Imaging, MRI report, February 20, 2026: $2,150.00'  state=stated reason=None
225	== B10 bill: 'Referral dated 02/10/2026, MRI charge $2,150.00'  (record date 2026-03-01; source 'Riverside Imaging, billing statement'; billing_document=True)
226	   Referral dated 02/10/2026, MRI charge $2,150.00.
227	    $2,150.00 -> letter head: 'Riverside Imaging, billing statement, date of service [__________] (statement dated March 1, 2026): $2,150.00'  state=not_stated reason=non_service_date
228	              Step 3 note: The only date near this line (02/10/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
229	== B11 bill: 'Onset 01/09/2026, 97110 therapeutic exercise $95.00'  (record date 2026-03-20; source 'Capital PT, billing statement'; billing_document=True)
230	   Onset 01/09/2026, 97110 therapeutic exercise $95.00.
231	       $95.00 -> letter head: 'Capital PT, billing statement, date of service [__________] (statement dated March 20, 2026): $95.00'  state=not_stated reason=non_service_date
232	              Step 3 note: The only date near this line (01/09/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
233	== B12 bill: 'Date of accident 01/19/2026 per intake; 99213 $275.00'  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
234	   Date of accident 01/19/2026 per intake, 99213 office visit $275.00.
235	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
236	              Step 3 note: The only date near this line (01/19/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
237	== R1 visit note: next visit date in the charge sentence  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; billing_document=False)
238	   Next visit date 01/30/2026, office visit charge $150.00.
239	      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 30, 2026: $150.00'  state=stated reason=None
240	== R2 visit note: prior visit 'seen on' in the charge sentence  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; billing_document=False)
241	   Previously seen on 01/09/2026 in the ER, follow-up visit charge $150.00.
242	      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
243	== R3 bill: return visit date label after the charge's own DOS  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
244	   Date of service 02/02/2026, office visit charge $275.00, return visit date 02/16/2026.
245	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
246	== R4 bill: DOS label tied to the accident ('date of service of the accident')  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
247	   Date of injury 01/09/2026; date of service 02/02/2026; 99213 office visit $275.00.
248	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
249	== R5 ledger: header 'Visit Type  Date  Charge' (heading names visit, but the date column is bare 'Date')  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
250	   Visit Type     Date         Code   Charge
251	   Follow-up     06/10/2026   97140  $70.00
252	   Follow-up     06/17/2026   97110  $95.00
253	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, date of service [__________] (statement dated July 1, 2026): $70.00'  state=not_stated reason=non_service_date
254	              Step 3 note: The only date near this line (06/10/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
255	       $95.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, date of service [__________] (statement dated July 1, 2026): $95.00'  state=not_stated reason=non_service_date
256	              Step 3 note: The only date near this line (06/17/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
257	== R6 ledger: DOS heading, but a DOB column before it  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
258	   DOB          DOS          Code   Charge
259	   03/15/1980   06/10/2026   97140  $70.00
260	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
261	== R7 ledger: 'Injury Date' column then 'Service Date' column  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
262	   Injury Date   Service Date   Code   Charge
263	   01/09/2026    06/10/2026     97140  $70.00
264	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, June 10, 2026: $70.00'  state=stated reason=None
265	== R8 ledger: only 'Injury Date' column  (record date 2026-07-01; source 'Larkspur Hollow Physical Therapy, itemized ledger'; billing_document=True)
266	   Injury Date   Code   Charge
267	   01/09/2026    97140  $70.00
268	       $70.00 -> letter head: 'Larkspur Hollow Physical Therapy, itemized ledger, date of service [__________] (statement dated July 1, 2026): $70.00'  state=not_stated reason=non_service_date
269	              Step 3 note: The only date near this line (01/09/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
270	== R9 CMS-1500 flattened with item 24A label and DOB on the same line  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; billing_document=True)
271	   Item 3 DOB 03/15/1980 Item 24A DOS 06/24/2026 CPT 99204 $185.00.
272	      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, June 24, 2026: $185.00'  state=stated reason=None
273	== R10 bill: 'DOS' then accident date in same clause  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
274	   DOS 02/02/2026 (accident 01/09/2026) office visit $275.00.
275	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
276	== R11 bill: 'run of' with an order date  (record date 2026-11-12; source 'Tarnwick Fire-Rescue, ambulance invoice'; billing_document=True)
277	   Call received 09/14/2026; run of 09/14/2026; A0427 ALS emergency transport, charge $1,380.00.
278	    $1,380.00 -> letter head: 'Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00'  state=stated reason=None
279	== R12 visit note: 'Date of service' label is the original ER visit (history)  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; billing_document=False)
280	   Patient brings ER bill, date of service 01/09/2026, ER charge $6,240.00.
281	    $6,240.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $6,240.00'  state=stated reason=None
282	== R13 bill: 'Seen on' with referral date first  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
283	   Referred 01/20/2026, seen on 02/02/2026, office visit charge $275.00.
284	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
285	== R14 bill: date of service written in words-with-year  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
286	   Date of service February 2, 2026: office visit charge $275.00.
287	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
288	== R15 bill: DOS with ordinal ('Feb. 2nd, 2026')  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
289	   DOS Feb. 2nd, 2026 office visit charge $275.00.
290	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=no_date
291	              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
292	== R16 bill: DOS 02/02/2026 and statement date 03/01/2026 in one clause  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
293	   Statement 03/01/2026 for DOS 02/02/2026, office visit $275.00.
294	      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
295	
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:27:31.113Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n -i \"charge\\|\\\\$\" evals/golden/sample.txt | head -20; grep -n \"N10\\|P1 two\" -A4 artifacts/review-evidence/T-202-paralegal-r2/probe_r2.out | head -20",
 "description": "Check sample charge text and r2 N10/P1 output"
}
````

### User / tool · 2026-11-03T01:27:31.218Z

**tool result**
````
10:Source: Central ER discharge summary
11:Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."
21:Excerpt: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185."
31:Excerpt: "Discharged from PT after two missed appointments. Pain 3/10."
41:Excerpt: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150."
1:== P1 two-row ledger, own dates  (record date 2026-03-15; source 'Hobbleton Family Clinic, itemized ledger')
2-   Statement date 03/15/2026. 02/02/2026 office visit charge $275.00. 02/16/2026 x-ray charge $150.00. Balance due $425.00.
3-      $275.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger, February 2, 2026: $275.00'  state=stated reason=None
4-      $150.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger, February 16, 2026: $150.00'  state=stated reason=None
5-      $425.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger (statement dated March 15, 2026; service date not stated): $425.00'  state=not_stated reason=no_date
--
118:== N10 CMS-1500 'from 06/24/2026 to 07/08/2026' (claim span, 2 discrete visits)  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500')
119-   CMS-1500 dates of service from 06/24/2026 to 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.
120-      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $185.00'  state=not_stated reason=no_date
121-              Step 3 note: The line states no date of service. The letter prints no service date for this line. Confirm the date from the quote before you rely on it.
122-      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500 (statement dated July 14, 2026; service date not stated): $210.00'  state=not_stated reason=no_date
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:27:44.195Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542; grep -n \"def \\|_LABEL\\|seen on\\|visit date\\|billing_document\" $S/app/backend/service_date.py | head -60",
 "description": "List service_date.py functions and labels"
}
````

### User / tool · 2026-11-03T01:27:44.285Z

**tool result**
````
5:  (a) the column header over it names service (DOS, date of service, service date, from/to service, 24A, visit date);
6:  (b) a service label in the same clause before (or just after) it (DOS, date of service, service date, seen on, visit date, visit of, the run of ...);
61:def display(first, last=None) -> str:
63:    def lng(iso):
79:def not_stated_text(statement_iso) -> str:
87:def printed_text(res: dict, statement_iso) -> str:
106:def confirm_note(reason, raw) -> str:
111:def _iso(y, mo, d):
121:    def __init__(self, m):
128:    def _iso(self, s):
132:    def _num(self, s):
145:    def _mdy(self, s):
155:    def _dmy(self, s):
159:    def _md(self, s):
162:    def _mper(self, s):
175:def _mon(name):
182:    def __init__(self, toks):
186:    def raw(self, text):
190:def _units(text: str) -> list:
204:def _certain(unit: _Unit, ref):
230:def _header_cells(excerpt: str, row_ls: int):
242:def _column_head(excerpt: str, row_ls: int, row_cells: list, tok_abs: int) -> str:
254:def _mark(text: str, units: list, rx, tail: bool = False) -> list:
269:def _plausible(first, last, ref) -> bool:
277:def _decide(units, text, ref, bill):
296:def _apply(out: dict, res) -> dict:
304:def resolve(excerpt: str, start: int, source, date_iso) -> dict:
315:    bill = AM.billing_document(source, excerpt)
321:    def labeled(text, tail=False):
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:27:48.054Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542/app/backend/service_date.py",
 "offset": 1,
 "limit": 60
}
````

### User / tool · 2026-11-03T01:27:48.061Z

**tool result**
````
1	"""The service date a charge line prints, only when positive evidence ties it to the line (D-071 amendment, T-202 round 3: an ALLOW-LIST, not a deny-list). Code only, no LLM
2	(LLM_VS_CODE rows 2 and 3).
3	
4	The letter's charge line carries a date of service. A date there is a claim to an adjuster, so a date is the line's service date ONLY when one of these ties it to the line:
5	  (a) the column header over it names service (DOS, date of service, service date, from/to service, 24A, visit date);
6	  (b) a service label in the same clause before (or just after) it (DOS, date of service, service date, seen on, visit date, visit of, the run of ...);
7	  (c) it is the date cell of the charge row itself, in a table whose header is (a);
8	  (d) for a coded line of a bill with no date of its own: the one period the bill states for its services ('dates of service ...', 'the run of ...', and on a UB-04 'statement
9	      covers period ...').
10	Any other date (birth, injury, onset, referral, order, authorization, entry, transaction, issued, printed, posted, statement, or no label at all) is NOT a service date and is never
11	looked at again: an unlabeled date cannot become the line's date by default. The result is one of:
12	  - `stated`: exactly one unambiguous labeled date or complete period (a numeric date that reads two ways is resolved only by 'a service cannot follow its statement', and only when
13	    EVERY labeled end then reads one way; a stated date after its statement, or more than five years before it, in a bill is doubtful);
14	  - `not_stated` with reason `no_date` / `non_service_date`: the quote labels no date of service; a dated encounter note (visit note, imaging report: not a bill) keeps the
15	    note's own date;
16	  - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): the quote DOES label a date of service and
17	    the code cannot read it with certainty; the note names the date as the quote writes it.
18	  Every not-stated line prints the same fillable blank (D-071 addendum): 'date of service [__________] (statement dated X)'. The paralegal fills it from the quote; nothing is inferred,
19	  and the letter never says "service date not stated" above a quote that states one.
20	Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
21	(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
22	import datetime as _dt
23	import re
24	
25	from app.backend import amounts as AM
26	
27	_MON = AM._MON
28	_ORD = r"(?:st|nd|rd|th)?"
29	_DASH = "–—"
30	_TOK = re.compile(
31	    r"(?<![\w/$])(?:"
32	    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
33	    r"|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2}))"
34	    rf"|(?P<mper>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}\s*[-{_DASH}]\s*(?:(?:{_MON})\.?\s+)?\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
35	    rf"|(?P<mdy>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}(?:,?\s+\d{{4}}|,\s*\d{{2}}(?!\d))?)"
36	    rf"|(?P<dmy>\d{{1,2}}{_ORD}[\s-]+(?:of\s+)?(?:{_MON})\.?[\s-]*,?\s*\d{{4}})"
37	    r"|(?P<md>\d{1,2}/\d{1,2}(?!\s*(?:hrs?|hours?|units?|miles?|mins?|visits?|sessions?)\b))"
38	    r")(?![\w/]|\.\d)", re.IGNORECASE)
39	_JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
40	_LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
41	# ---- the allow-list: positive evidence that a date is the line's date of service. Nothing else is read (T-202 round 3).
42	_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(]{0,4}$"
43	_SVC_CORE = (r"\bdos|\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?|\bvisit\s+dates?|\bdates?\s+of\s+visit|\bvisit\s+of|\bseen(?:\s+on)?|"
44	             r"\b(?:services?\s+)?(?:rendered|provided|performed)\s+on|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|\bservice\s+period|\bperiod\s+of\s+service|"
45	             r"\bdates?\s+of\s+treatment|\btreatment\s+dates?")
46	_PER_CORE = (r"\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?|\bservice\s+period|\bperiod\s+of\s+service|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|"
47	             r"\b(?:services?\s+)?(?:rendered|provided)\s+on")
48	_UB_CORE = r"\bstatement\s+(?:covers\s+)?period"          # UB-04 FL6 'Statement Covers Period' is the span of the services; on any other bill 'statement period' is not a service label
49	_UB = re.compile(r"\bub-?04\b|\btype\s+of\s+bill\b|\bFL\s?\d{1,2}\b|\bUB\s?92\b", re.IGNORECASE)
50	_LBL = {False: re.compile(rf"(?:{_SVC_CORE}){_LBL_END}", re.IGNORECASE), True: re.compile(rf"(?:{_SVC_CORE}|{_UB_CORE}){_LBL_END}", re.IGNORECASE)}
51	_PER = {False: re.compile(rf"(?:{_PER_CORE}){_LBL_END}", re.IGNORECASE), True: re.compile(rf"(?:{_PER_CORE}|{_UB_CORE}){_LBL_END}", re.IGNORECASE)}
52	# a column heading that names service (a CMS-1500 24A 'From'/'To' under 'Date(s) of Service', 'Service From', 'DOS' ...). A bare 'Date', 'Entry date', 'Transaction Date', 'Posted' ... does not.
53	_H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter\s+date|"
54	                    r"\b(?:service|svc)\s+(?:from|to|thru|through)\b|\b(?:from|to|thru|through)\s+(?:dos|service|svc)\b|\b24\s*-?a\b", re.IGNORECASE)
55	_YEARS_BEFORE = 5                # a bill's service date more than this many years before its statement is doubtful
56	
57	REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "implausible", "non_service_date", "no_date")
58	WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)
59	
60	
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:27:51.110Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542/app/backend/service_date.py",
 "offset": 265,
 "limit": 80
}
````

### User / tool · 2026-11-03T01:27:51.117Z

**tool result**
````
265	        marks.append(ok)
266	    return marks
267	
268	
269	def _plausible(first, last, ref) -> bool:
270	    """A bill's service date is not after its statement and not years before it."""
271	    if not ref:
272	        return True
273	    r = _dt.date.fromisoformat(ref)
274	    return (last or first) <= ref and _dt.date.fromisoformat(first) >= r - _dt.timedelta(days=366 * _YEARS_BEFORE)
275	
276	
277	def _decide(units, text, ref, bill):
278	    """('ok', first, last) for one certain labeled unit (or several that read the same); ('bad', reason, [raw, ...]) otherwise."""
279	    reads = [(u, _certain(u, ref)) for u in units]
280	    raws = [" ".join(u.raw(text).split()) for u in units]
281	    if len(units) > 1:
282	        same = {(r[1], r[2]) for _, r in reads if r[0] == "ok"}
283	        if not (len(same) == 1 and all(r[0] == "ok" for _, r in reads)):
284	            return "bad", "several_dates", raws
285	        first, last = next(iter(same))
286	    else:
287	        r = reads[0][1]
288	        if r[0] != "ok":
289	            return "bad", r[1], raws
290	        first, last = r[1], r[2]
291	    if bill and not _plausible(first, last, ref):
292	        return "bad", "implausible", raws
293	    return "ok", first, last
294	
295	
296	def _apply(out: dict, res) -> dict:
297	    if res[0] == "ok":
298	        out.update(state="stated", first=res[1], last=res[2], reason=None, raw="", raws=[])
299	    else:
300	        out.update(reason=res[1], raw=", ".join(res[2]), raws=list(res[2]))
301	    return out
302	
303	
304	def resolve(excerpt: str, start: int, source, date_iso) -> dict:
305	    """{state: 'stated'|'not_stated', first, last (None for one day), reason (None when stated, else one of REASONS), raw (the labeled date text the reason is about, or the one
306	    unlabeled date near the line for non_service_date), raws ([the labeled dates as written])} for the figure at `start` of `excerpt`, in a record with header `source` and date
307	    `date_iso`. Only labeled dates are candidates (module doc); see it for the rules."""
308	    out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
309	    amts = AM.find_amounts(excerpt or "")
310	    i = next((n for n, a in enumerate(amts) if a["start"] == start), None)
311	    if i is None:
312	        return out
313	    a = amts[i]
314	    ss, se = next(((s, e) for s, e in AM._segments(excerpt) if s <= a["start"] < e), (0, len(excerpt)))
315	    bill = AM.billing_document(source, excerpt)
316	    ub = bool(_UB.search(source or "") or _UB.search(excerpt or ""))
317	    sfigs = [j for j, x in enumerate(amts) if ss <= x["start"] < se]
318	    seg = excerpt[ss:se]
319	    others = []                       # dates near the line that no service label ties to it
320	
321	    def labeled(text, tail=False):
322	        us = _units(text)
323	        marks = _mark(text, us, _LBL[ub], tail)
324	        others.extend(u.raw(text) for u, m in zip(us, marks) if not m)
325	        return [u for u, m in zip(us, marks) if m]
326	
327	    if len(AM._cells(seg)) >= 2:                                          # (a)/(c) a table row: only a date under a heading that names service
328	        row_ls = excerpt.rfind("\n", 0, a["start"]) + 1
329	        rl_end = excerpt.find("\n", a["start"])
330	        row_text = excerpt[row_ls:len(excerpt) if rl_end < 0 else rl_end]
331	        row_cells = [(m.start(), m.end()) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", row_text)]
332	        lab = []
333	        for u in _units(seg):
334	            head = _column_head(excerpt, row_ls, row_cells, ss + u.start)
335	            if (head and _H_SVC.search(head)) or _LBL[ub].search(seg[max(0, u.start - 40):u.start]):
336	                lab.append(u)
337	            else:
338	                others.append(u.raw(seg))
339	        if lab:
340	            return _apply(out, _decide(lab, seg, date_iso, bill))
341	    else:                                                                 # (b) a service label in the same clause
342	        prev = max((amts[j]["end"] for j in sfigs if j < i), default=ss)
343	        own = excerpt[prev:a["start"]]
344	        lab = labeled(own)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:27:56.552Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542; grep -n \"def charge_date_violations\" -A40 $S/evals/letter_check.py | head -80; grep -n \"seen\\|visit\\\\\\\\s\" $S/evals/letter_check.py | head",
 "description": "Read letter_check charge_date_violations"
}
````

### User / tool · 2026-11-03T01:27:56.667Z

**tool result**
````
335:def charge_date_violations(letter: str, records) -> list:
336-    """D-071 amendment, round 3 (allow-list): every charge line's printed date against THAT line's own quote (plus, for a quote with no labeled date, the bill's period before it).
337-    `records`: the case's [{n, source, date_iso, excerpt}]. Per line, the quote's LABELED dates are those with a service phrase right before them or a table heading over them that
338-    names the service; every other date in it (birth, injury, onset, referral, order, entry, transaction, posted, statement, unlabeled) is not a service date.
339-      - labeled dates that have exactly one certain reading (one date or period, one reading, not after its statement, not years before it) -> the line prints exactly that, whole;
340-      - labeled dates that are doubtful (several readings, two-digit year, no year, impossible, several dates, implausible) -> the line prints the blank, nothing else;
341-      - no labeled date in the quote, in a bill -> the one period the bill states before it (whole), else the blank 'date of service [__________] (statement dated X)' with X the
342-        record's date; in a visit note (not a bill) -> the note's own date (the blank is a violation there).
343-    A date printed where the quote labels none, a blank above a certain labeled date, and a statement date that is not the record's are violations."""
344-    norm = lambda t: " ".join(str(t).split())
345-    out = []
346-    for head, quote in charge_lines(letter):
347-        parsed = _head_dates(re.sub(r": \$[\d,]+\.\d\d$", "", head))
348-        recs = [r for r in records if norm(quote) and norm(quote) in norm(r["excerpt"])]
349-        if parsed is None:
350-            out.append(f"charge line has no readable date form: {head}")
351-            continue
352-        if not recs:
353-            out.append(f"charge line's quote is in no record: {head}")
354-            continue
355-        kind, first, last = parsed
356-        problems = []
357-        for r in recs:
358-            ex, rd = r["excerpt"], r.get("date_iso")
359-            bill = bool(_BILL_WORD.search(r.get("source") or "") or _BILL_WORD.search(ex[:60]))
360-            ub = bool(_UB_WORD.search(r.get("source") or "") or _UB_WORD.search(ex))
361-            n_ex, n_q = norm(ex), norm(quote)
362-            before = n_ex[:n_ex.index(n_q)]
363-            units = _written(n_q)
364-            marks = _marked(n_q, units, _SERVICE_PHRASES + (_UB_PHRASES if ub else ()), before + n_q, len(before))
365-            for k, u in enumerate(units):                                                       # a table heading over the date that names the service labels it too
366-                if not marks[k]:
367-                    marks[k] = bool(_names_service(_heading_over(ex, quote, u["start"])))
368-            lab = [u for u, m in zip(units, marks) if m]
369-            if lab:
370-                reads = [_readings(u, rd, bill) for u in lab]
371-                same = {x for rr in reads for x in rr}
372-                certain = all(len(rr) == 1 for rr in reads) and len(same) == 1
373-                texts = sorted(norm(n_q[u["start"]:u["end"]]) for u in lab)
374-                if certain:
375-                    if kind in ("range", "one"):
16:line (a service label in its clause: DOS, date of service, seen on, visit date ...; a table heading over it that names service; or, for a quote with no labeled date, the one period
190:_SERVICE_PHRASES = ("dos", "date of service", "dates of service", "date(s) of service", "service date", "service dates", "visit date", "date of visit", "visit of", "seen", "seen on",
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:28:11.489Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/probe_r3b.py",
 "content": "\"\"\"T-202 r3 paralegal probe B: allow-listed labels ('visit date', 'seen on', 'date of service') that name a DIFFERENT visit than the record's own, in visit notes\n(not bills) and in bills; then evals/letter_check.charge_date_violations on what the build prints for them, next to the record-date control. SYNTHETIC text only.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/probe_r3b.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, store  # noqa: E402\nfrom evals import letter_check as LC  # noqa: E402\n\nV = \"Dr. Alvarez, primary care\"\nPT = \"Capital PT, discharge summary\"\nER = \"Central ER discharge summary\"\nH = \"Hobbleton Family Clinic, billing statement\"\nPROBES = [\n    (\"R1 visit note 01/16: next visit date in the charge sentence\", V, \"2026-01-16\", \"Next visit date 01/30/2026, office visit charge $150.00.\"),\n    (\"R2 visit note 01/16: prior ER visit 'seen on' in the charge sentence\", V, \"2026-01-16\", \"Previously seen on 01/09/2026 in the ER, follow-up visit charge $150.00.\"),\n    (\"R17 visit note 01/16: checkout line, charge then next visit date\", V, \"2026-01-16\", \"Visit charge: $150.00   Next visit date: 01/30/2026\"),\n    (\"R18 visit note 01/16: checkout line, last visit date then charge\", V, \"2026-01-16\", \"Last visit date: 01/09/2026   Visit charge: $150.00\"),\n    (\"R19 PT discharge 03/06: initial visit date in the charge sentence\", PT, \"2026-03-06\", \"Initial visit date 01/23/2026, discharge visit charge $185.00.\"),\n    (\"R20 ER note 01/09: seen on the same day (control, should be January 9)\", ER, \"2026-01-09\", \"Seen on 01/09/2026 by EMS, ER facility charge $6,240.00.\"),\n    (\"R21 PT discharge 03/06: 'treatment dates' period then a charge\", PT, \"2026-03-06\", \"Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.\"),\n    (\"R22 bill 03/01: last visit date label then an undated coded line\", H, \"2026-03-01\", \"Last visit date 02/16/2026; 99213 office visit $275.00.\"),\n    (\"R23 bill 03/01: next visit date (future) in a coded line\", H, \"2026-03-01\", \"99213 office visit $275.00, next visit date 02/28/2026.\"),\n]\n\nprint(\"#### resolver (store.charge_service_date, the path Step 3 and the letter share)\")\nheads = {}\nfor label, src, rd, ex in PROBES:\n    print(f\"== {label}  (record date {rd}; source '{src}'; billing_document={AM.billing_document(src, ex)})\")\n    print(\"   \" + ex)\n    rec = {\"id\": \"r1\", \"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex, \"text\": ex}\n    for a in AM.find_amounts(ex):\n        if a.get(\"cents\") is None:\n            continue\n        item = {\"excerpt\": ex, \"value_cents\": a[\"cents\"], \"raw\": a[\"raw\"], \"excerpt_start\": 0}\n        d = store.charge_service_date(item, rec, a[\"start\"])\n        head = f\"{src}, {d['text']}\"\n        heads[label.split()[0]] = (src, rd, ex, head, a[\"raw\"])\n        print(f\"   {a['raw']:>10} -> letter head: '{head}: {a['raw']}'  state={d['state']} reason={d['reason']}\")\n        if d[\"confirm_note\"]:\n            print(f\"              Step 3 note: {d['confirm_note']}\")\n\n\ndef letter(head, fig, quote):\n    return f\"BILLED CHARGES\\n\\n{head}: {fig}\\nSource [Ex. __ / Bates __]: \\\"{quote}\\\"\\n\\nBilled charges accepted from these records: {fig}\"\n\n\nprint(\"\\n#### letter_check.charge_date_violations: the build's line vs the record-date line\")\nfor key in (\"R1\", \"R2\", \"R17\", \"R18\", \"R19\", \"R20\"):\n    src, rd, ex, head, fig = heads[key]\n    q = ex.rstrip(\".\")\n    recs = [{\"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex}]\n    from app.backend.service_date import display\n    ctrl = f\"{src}, {display(rd)}\"\n    print(f\"== {key} build prints '{head}': violations {LC.charge_date_violations(letter(head, fig, q), recs)}\")\n    print(f\"   {key} record date   '{ctrl}': violations {LC.charge_date_violations(letter(ctrl, fig, q), recs)}\")\n"
}
````

### User / tool · 2026-11-03T01:28:11.599Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/probe_r3b.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:28:15.901Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/probe_r3b.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/probe_r3b.out 2>&1; echo $?; cat artifacts/review-evidence/T-202-paralegal-r3/probe_r3b.out",
 "description": "Run probe B on archive"
}
````

### User / tool · 2026-11-03T01:28:16.354Z

**tool result**
````
0
#### resolver (store.charge_service_date, the path Step 3 and the letter share)
== R1 visit note 01/16: next visit date in the charge sentence  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; billing_document=False)
   Next visit date 01/30/2026, office visit charge $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 30, 2026: $150.00'  state=stated reason=None
== R2 visit note 01/16: prior ER visit 'seen on' in the charge sentence  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; billing_document=False)
   Previously seen on 01/09/2026 in the ER, follow-up visit charge $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== R17 visit note 01/16: checkout line, charge then next visit date  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; billing_document=False)
   Visit charge: $150.00   Next visit date: 01/30/2026
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 30, 2026: $150.00'  state=stated reason=None
== R18 visit note 01/16: checkout line, last visit date then charge  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; billing_document=False)
   Last visit date: 01/09/2026   Visit charge: $150.00
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== R19 PT discharge 03/06: initial visit date in the charge sentence  (record date 2026-03-06; source 'Capital PT, discharge summary'; billing_document=False)
   Initial visit date 01/23/2026, discharge visit charge $185.00.
      $185.00 -> letter head: 'Capital PT, discharge summary, January 23, 2026: $185.00'  state=stated reason=None
== R20 ER note 01/09: seen on the same day (control, should be January 9)  (record date 2026-01-09; source 'Central ER discharge summary'; billing_document=False)
   Seen on 01/09/2026 by EMS, ER facility charge $6,240.00.
    $6,240.00 -> letter head: 'Central ER discharge summary, January 9, 2026: $6,240.00'  state=stated reason=None
== R21 PT discharge 03/06: 'treatment dates' period then a charge  (record date 2026-03-06; source 'Capital PT, discharge summary'; billing_document=False)
   Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.
    $1,665.00 -> letter head: 'Capital PT, discharge summary, January 23–March 6, 2026: $1,665.00'  state=stated reason=None
== R22 bill 03/01: last visit date label then an undated coded line  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
   Last visit date 02/16/2026; 99213 office visit $275.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
== R23 bill 03/01: next visit date (future) in a coded line  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; billing_document=True)
   99213 office visit $275.00, next visit date 02/28/2026.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 28, 2026: $275.00'  state=stated reason=None

#### letter_check.charge_date_violations: the build's line vs the record-date line
== R1 build prints 'Dr. Alvarez, primary care, January 30, 2026': violations []
   R1 record date   'Dr. Alvarez, primary care, January 16, 2026': violations ["charge line's date is not certain from its quote (the quote's labeled date of service reads 2026-01-30): Dr. Alvarez, primary care, January 16, 2026: $150.00"]
== R2 build prints 'Dr. Alvarez, primary care, January 9, 2026': violations []
   R2 record date   'Dr. Alvarez, primary care, January 16, 2026': violations ["charge line's date is not certain from its quote (the quote's labeled date of service reads 2026-01-09): Dr. Alvarez, primary care, January 16, 2026: $150.00"]
== R17 build prints 'Dr. Alvarez, primary care, January 30, 2026': violations []
   R17 record date   'Dr. Alvarez, primary care, January 16, 2026': violations ["charge line's date is not certain from its quote (the quote's labeled date of service reads 2026-01-30): Dr. Alvarez, primary care, January 16, 2026: $150.00"]
== R18 build prints 'Dr. Alvarez, primary care, January 9, 2026': violations []
   R18 record date   'Dr. Alvarez, primary care, January 16, 2026': violations ["charge line's date is not certain from its quote (the quote's labeled date of service reads 2026-01-09): Dr. Alvarez, primary care, January 16, 2026: $150.00"]
== R19 build prints 'Capital PT, discharge summary, January 23, 2026': violations []
   R19 record date   'Capital PT, discharge summary, March 6, 2026': violations ["charge line's date is not certain from its quote (the quote's labeled date of service reads 2026-01-23): Capital PT, discharge summary, March 6, 2026: $185.00"]
== R20 build prints 'Central ER discharge summary, January 9, 2026': violations []
   R20 record date   'Central ER discharge summary, January 9, 2026': violations []
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:28:34.102Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/probe_r3c.py",
 "content": "\"\"\"T-202 r3 paralegal probe C: sample-case-styled clinical notes (Appendix A shapes: 'ER charges: $6,240.', 'Charge per visit $185.') with a follow-up / next /\nprior visit date nearby, to see which punctuation keeps the other visit's date out of the charge line. SYNTHETIC text only.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/probe_r3c.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, store  # noqa: E402\n\nER = \"Central ER discharge summary\"\nPT = \"Capital PT, initial evaluation\"\nPROBES = [\n    (\"C1 ER 01/09: follow-up visit date, own sentence, then charge\", ER, \"2026-01-09\", \"Follow-up visit date 01/16/2026. ER charges: $6,240.\"),\n    (\"C2 ER 01/09: follow-up visit date, semicolon, then charge\", ER, \"2026-01-09\", \"Follow-up visit date 01/16/2026; ER charges: $6,240.\"),\n    (\"C3 ER 01/09: charge, then next visit date in its own sentence\", ER, \"2026-01-09\", \"ER charges: $6,240. Next visit date 01/16/2026.\"),\n    (\"C4 ER 01/09: charge, then next visit date after a comma\", ER, \"2026-01-09\", \"ER charges: $6,240, next visit date 01/16/2026.\"),\n    (\"C5 PT eval 01/23: plan + next visit date + rate, sentences\", PT, \"2026-01-23\", \"Plan of care: 12 visits. Next visit date 01/27/2026. Charge per visit $185.\"),\n    (\"C6 PT eval 01/23: plan + next visit date + rate, one line no periods\", PT, \"2026-01-23\", \"Plan of care: 12 visits   Next visit date: 01/27/2026   Charge per visit $185\"),\n    (\"C7 ER 01/09: two spaces as separators, follow-up visit date then charge\", ER, \"2026-01-09\", \"Follow-up visit date: 01/16/2026  ER charges: $6,240\"),\n]\nfor label, src, rd, ex in PROBES:\n    print(f\"== {label}  (record date {rd}; source '{src}'; billing_document={AM.billing_document(src, ex)})\")\n    print(\"   \" + ex)\n    rec = {\"id\": \"r1\", \"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex, \"text\": ex}\n    for a in AM.find_amounts(ex):\n        if a.get(\"cents\") is None:\n            continue\n        item = {\"excerpt\": ex, \"value_cents\": a[\"cents\"], \"raw\": a[\"raw\"], \"excerpt_start\": 0}\n        d = store.charge_service_date(item, rec, a[\"start\"])\n        print(f\"   {a['raw']:>10} -> letter head: '{src}, {d['text']}: {a['raw']}'  state={d['state']} reason={d['reason']}\")\n"
}
````

### User / tool · 2026-11-03T01:28:34.214Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/probe_r3c.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:28:38.270Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/probe_r3c.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/probe_r3c.out 2>&1; echo $?; cat artifacts/review-evidence/T-202-paralegal-r3/probe_r3c.out",
 "description": "Run probe C"
}
````

### User / tool · 2026-11-03T01:28:38.739Z

**tool result**
````
0
== C1 ER 01/09: follow-up visit date, own sentence, then charge  (record date 2026-01-09; source 'Central ER discharge summary'; billing_document=False)
   Follow-up visit date 01/16/2026. ER charges: $6,240.
       $6,240 -> letter head: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
== C2 ER 01/09: follow-up visit date, semicolon, then charge  (record date 2026-01-09; source 'Central ER discharge summary'; billing_document=False)
   Follow-up visit date 01/16/2026; ER charges: $6,240.
       $6,240 -> letter head: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
== C3 ER 01/09: charge, then next visit date in its own sentence  (record date 2026-01-09; source 'Central ER discharge summary'; billing_document=False)
   ER charges: $6,240. Next visit date 01/16/2026.
       $6,240 -> letter head: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
== C4 ER 01/09: charge, then next visit date after a comma  (record date 2026-01-09; source 'Central ER discharge summary'; billing_document=False)
   ER charges: $6,240, next visit date 01/16/2026.
       $6,240 -> letter head: 'Central ER discharge summary, January 16, 2026: $6,240'  state=stated reason=None
== C5 PT eval 01/23: plan + next visit date + rate, sentences  (record date 2026-01-23; source 'Capital PT, initial evaluation'; billing_document=False)
   Plan of care: 12 visits. Next visit date 01/27/2026. Charge per visit $185.
         $185 -> letter head: 'Capital PT, initial evaluation, January 23, 2026: $185'  state=stated reason=None
== C6 PT eval 01/23: plan + next visit date + rate, one line no periods  (record date 2026-01-23; source 'Capital PT, initial evaluation'; billing_document=False)
   Plan of care: 12 visits   Next visit date: 01/27/2026   Charge per visit $185
         $185 -> letter head: 'Capital PT, initial evaluation, January 27, 2026: $185'  state=stated reason=None
== C7 ER 01/09: two spaces as separators, follow-up visit date then charge  (record date 2026-01-09; source 'Central ER discharge summary'; billing_document=False)
   Follow-up visit date: 01/16/2026  ER charges: $6,240
       $6,240 -> letter head: 'Central ER discharge summary, January 16, 2026: $6,240'  state=stated reason=None
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:28:50.266Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542 && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_t202_r3_allow_list.py tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/pytest-t202.out 2>&1; echo $?; tail -3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/pytest-t202.out",
 "description": "Run T-202 unit tests from archive"
}
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:28:54.956Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542 && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.letter_check > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/letter_check.out 2>&1; echo $?; head -c 600 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/letter_check.out",
 "description": "Run letter_check eval from archive"
}
````

### User / tool · 2026-11-03T01:28:58.536Z

**tool result**
````
0
........................................................................ [ 68%]
...................................................................      [100%]
211 passed in 7.88s
````

### User / tool · 2026-11-03T01:29:10.637Z

**tool result**
````
0
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:13.150Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat artifacts/review-evidence/T-202-paralegal-r2/letters_dump_r2.py; ls artifacts/review-evidence/T-202-paralegal-r2/letters/",
 "description": "Read r2 letters dump script"
}
````

### User / tool · 2026-11-03T01:29:13.316Z

**tool result**
````
"""T-202 r2 paralegal: letters + internal notes for sample, case_09, lib14, lib10, lib11 (all_accepted and counted variants) from the 986fc55 archive,
plus SYNTHETIC variants of case_09 whose bill line the code cannot date (ambiguous numeric DOS; CMS-1500 with two dates of service), to read the
not-stated wording as a demand letter prints it. Run from repo root:
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r2/letters_dump_r2.py <archive_root> <out_dir>
"""
import os
import sys
import traceback

root = os.path.abspath(sys.argv[1])
out = os.path.abspath(sys.argv[2])
sys.path.insert(0, root)
os.chdir(root)
os.environ.setdefault("LLM_BACKEND", "fixture")
os.environ.setdefault("FIXTURE_SET", "curated")
from evals import letter_check as LC  # noqa: E402

C09 = open("evals/golden/case_09_nonvisit_hides_gap.txt").read()
AMBIG = C09.replace('Date: 2026-03-01\nSource: Hobbleton Family Clinic, billing statement\nExcerpt: "Statement for visit of 2026-02-02: $275."',
                    'Date: 2026-06-01\nSource: Hobbleton Family Clinic, billing statement\nExcerpt: "Date of service 04/05/2026: office visit charge $275.00."')
CMS = C09.replace('Date: 2026-03-01\nSource: Hobbleton Family Clinic, billing statement\nExcerpt: "Statement for visit of 2026-02-02: $275."',
                  'Date: 2026-04-20\nSource: Hobbleton Family Clinic, CMS-1500\nExcerpt: "CMS-1500 for dates of service 02/02/2026 and 03/30/2026. CPT 99213 charge $150.00. CPT 29125 splint charge $125.00."')
assert AMBIG != C09 and CMS != C09

CASES = {
    "sample": open("evals/golden/sample.txt").read(),
    "case_09": C09,
    "lib14": open("evals/library/case_lib14_handwritten_chiro_scans.txt").read(),
    "lib10": open("evals/library/case_lib10_eob_ub04_cms1500.txt").read(),
    "lib11": open("evals/library/case_lib11_priors_and_ledger.txt").read(),
    "synth_ambiguous_dos": AMBIG,
    "synth_cms1500_two_dates": CMS,
}
for name, text in CASES.items():
    try:
        got = LC.letters_for(text)
    except Exception:
        print(f"== {name}: letters_for raised\n{traceback.format_exc()}")
        continue
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
        print("    date violations:", viol)
case_09-all_accepted-letter.txt
case_09-all_accepted-notes.txt
case_09-counted-letter.txt
case_09-counted-notes.txt
lib10-all_accepted-letter.txt
lib10-all_accepted-notes.txt
lib10-counted-letter.txt
lib10-counted-notes.txt
lib11-all_accepted-letter.txt
lib11-all_accepted-notes.txt
lib11-counted-letter.txt
lib11-counted-notes.txt
lib14-all_accepted-letter.txt
lib14-all_accepted-notes.txt
lib14-counted-letter.txt
lib14-counted-notes.txt
sample-all_accepted-letter.txt
sample-all_accepted-notes.txt
sample-counted-letter.txt
sample-counted-notes.txt
synth_ambiguous_dos-all_accepted-letter.txt
synth_ambiguous_dos-all_accepted-notes.txt
synth_ambiguous_dos-counted-letter.txt
synth_ambiguous_dos-counted-notes.txt
synth_cms1500_two_dates-all_accepted-letter.txt
synth_cms1500_two_dates-all_accepted-notes.txt
synth_cms1500_two_dates-counted-letter.txt
synth_cms1500_two_dates-counted-notes.txt
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:17.195Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; mkdir -p artifacts/review-evidence/T-202-paralegal-r3/letters && cp artifacts/review-evidence/T-202-paralegal-r2/letters_dump_r2.py artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.py && grep -n \"ER charges\" evals/golden/sample.txt",
 "description": "Copy letters dump script to r3 dir"
}
````

### User / tool · 2026-11-03T01:29:17.296Z

**tool result**
````
11:Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:20.603Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.py",
 "old_string": "assert AMBIG != C09 and CMS != C09\n",
 "new_string": "assert AMBIG != C09 and CMS != C09\nSAMPLE = open(\"evals/golden/sample.txt\").read()\n# r3: the sample ER note with the follow-up appointment written after the charge, comma-joined (SYNTHETIC variant of Appendix A record 2)\nNEXTV = SAMPLE.replace(\"Follow up with PCP in 1 week. ER charges: $6,240.\", \"Follow up with PCP in 1 week. ER charges: $6,240, next visit date 01/16/2026.\")\nassert NEXTV != SAMPLE\n"
}
````

### User / tool · 2026-11-03T01:29:20.722Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:21.920Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.py",
 "old_string": "    \"synth_cms1500_two_dates\": CMS,\n}",
 "new_string": "    \"synth_cms1500_two_dates\": CMS,\n    \"synth_sample_er_next_visit\": NEXTV,\n}"
}
````

### User / tool · 2026-11-03T01:29:22.022Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:27.108Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/letters > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.out 2>&1; echo $?; cat artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.out",
 "description": "Dump letters for corpus and variants"
}
````

### User / tool · 2026-11-03T01:29:31.130Z

**tool result**
````
0
llm call failed call_id=cc6bd63fc45b9 step=extract attempt=1 prompt_hash=1c695c709b4ba6a23838aefb77a30455e0e4b4969683611faa8a31b17962a114
llm call failed call_id=c1f2450e28964 step=extract attempt=1 prompt_hash=4e125efe75cbe7e149d3a6f9401e22532bfc29cab29ae973b22b5c4edade2730
llm call failed call_id=ce961f9cdea03 step=extract attempt=1 prompt_hash=301f3e3030797717551a1e215e31632875ed498289b53c8a8335526af41695d4
llm call failed call_id=cb5e27a9e8627 step=extract attempt=1 prompt_hash=bfcfe1db058428e83a2b1d3d93349444ff3fc2d2f17cd94d12f7bf8c5059875a
llm call failed call_id=c7a8079d211b5 step=extract attempt=1 prompt_hash=028686fff244c6585d867f8664f7fdf7972a0d4cdff06ec5419b61004b123302
llm call failed call_id=c83de999de692 step=j2 attempt=1 prompt_hash=ef2e82374e44a320203c1c0788f9982dbfb78a0e5dbede80a6d2eaaaef213c71
llm call failed call_id=cadf6ec848d66 step=flags attempt=1 prompt_hash=1223f5af19302e3e35b3c8b675080e97eddb6dce0c5605f43287acb59c18beb9
llm call failed call_id=cee557b66cddc step=flags attempt=1 prompt_hash=9f30aa0f7fd4fffd5e5e06ea69e48e9b594f4b71b310263b96b726ead46bb24d
llm call failed call_id=cc7a0e7728582 step=flags attempt=1 prompt_hash=cf7adf099f2cc57cd693bbba71acf598e0bfb1c40a05637e894f5e8b11a29537
llm call failed call_id=c7e12a6abb7cc step=flags attempt=1 prompt_hash=d49132e98c40d33efd0d4eda5c9070d35874d78271524571f42d65752acd9696
llm call failed call_id=cb942995eef50 step=flags attempt=1 prompt_hash=78c0e130ba3a5793e5a4e310f4ba39fb476b9909eeea0d35e663b4a4fa2f89d9
llm call failed call_id=c84ed55cd34b2 step=extract attempt=1 prompt_hash=1c695c709b4ba6a23838aefb77a30455e0e4b4969683611faa8a31b17962a114
llm call failed call_id=c54fc18da49b9 step=extract attempt=1 prompt_hash=4e125efe75cbe7e149d3a6f9401e22532bfc29cab29ae973b22b5c4edade2730
llm call failed call_id=c42cb97ce6547 step=extract attempt=1 prompt_hash=301f3e3030797717551a1e215e31632875ed498289b53c8a8335526af41695d4
llm call failed call_id=c972d6c1cdff3 step=extract attempt=1 prompt_hash=bfcfe1db058428e83a2b1d3d93349444ff3fc2d2f17cd94d12f7bf8c5059875a
llm call failed call_id=c3251f8d90376 step=extract attempt=1 prompt_hash=028686fff244c6585d867f8664f7fdf7972a0d4cdff06ec5419b61004b123302
llm call failed call_id=cbffb658e4999 step=j2 attempt=1 prompt_hash=ef2e82374e44a320203c1c0788f9982dbfb78a0e5dbede80a6d2eaaaef213c71
llm call failed call_id=c9f3764a48627 step=flags attempt=1 prompt_hash=cf7adf099f2cc57cd693bbba71acf598e0bfb1c40a05637e894f5e8b11a29537
llm call failed call_id=c4dc69838cedf step=flags attempt=1 prompt_hash=1223f5af19302e3e35b3c8b675080e97eddb6dce0c5605f43287acb59c18beb9
llm call failed call_id=cae0bab1bc2e0 step=flags attempt=1 prompt_hash=9f30aa0f7fd4fffd5e5e06ea69e48e9b594f4b71b310263b96b726ead46bb24d
llm call failed call_id=c7f28b318c957 step=flags attempt=1 prompt_hash=d49132e98c40d33efd0d4eda5c9070d35874d78271524571f42d65752acd9696
llm call failed call_id=c10c4a35311b3 step=flags attempt=1 prompt_hash=78c0e130ba3a5793e5a4e310f4ba39fb476b9909eeea0d35e663b4a4fa2f89d9
llm call failed call_id=c6bb50255a66b step=extract attempt=1 prompt_hash=1c695c709b4ba6a23838aefb77a30455e0e4b4969683611faa8a31b17962a114
llm call failed call_id=cdee4e5279222 step=extract attempt=1 prompt_hash=4e125efe75cbe7e149d3a6f9401e22532bfc29cab29ae973b22b5c4edade2730
llm call failed call_id=ccbc4eb84df1f step=extract attempt=1 prompt_hash=301f3e3030797717551a1e215e31632875ed498289b53c8a8335526af41695d4
llm call failed call_id=c676ed2830f2f step=extract attempt=1 prompt_hash=bfcfe1db058428e83a2b1d3d93349444ff3fc2d2f17cd94d12f7bf8c5059875a
llm call failed call_id=c1d2730890afa step=extract attempt=1 prompt_hash=028686fff244c6585d867f8664f7fdf7972a0d4cdff06ec5419b61004b123302
llm call failed call_id=cca02da186f30 step=j2 attempt=1 prompt_hash=ef2e82374e44a320203c1c0788f9982dbfb78a0e5dbede80a6d2eaaaef213c71
llm call failed call_id=cf2c94d03f81a step=flags attempt=1 prompt_hash=1223f5af19302e3e35b3c8b675080e97eddb6dce0c5605f43287acb59c18beb9
llm call failed call_id=c0263a70450b6 step=flags attempt=1 prompt_hash=cf7adf099f2cc57cd693bbba71acf598e0bfb1c40a05637e894f5e8b11a29537
llm call failed call_id=c6ab83185e389 step=flags attempt=1 prompt_hash=9f30aa0f7fd4fffd5e5e06ea69e48e9b594f4b71b310263b96b726ead46bb24d
llm call failed call_id=c787b5e1aafcc step=flags attempt=1 prompt_hash=d49132e98c40d33efd0d4eda5c9070d35874d78271524571f42d65752acd9696
llm call failed call_id=c119584de645d step=flags attempt=1 prompt_hash=78c0e130ba3a5793e5a4e310f4ba39fb476b9909eeea0d35e663b4a4fa2f89d9
llm call failed call_id=c79a9dab5cc06 step=extract attempt=1 prompt_hash=4d2be32aadec8f6c773b344e4a74826ef4f5c42e983b909a1c4ea7a2aa4fa0c4
llm call failed call_id=c56c3a5cd0b82 step=extract attempt=1 prompt_hash=edea79f1398615fba03ecd8266fe09577a99db77a35715521fd177fe7a2e6b64
llm call failed call_id=c20a4a965ffa3 step=extract attempt=1 prompt_hash=edfb11d933988b8c1a75762df0cf62b58359e69e79390db1562c974a44c54218
llm call failed call_id=cc6fd0a82d3ed step=extract attempt=1 prompt_hash=2aca0c360bafeb694b1b74f4ecba896ceb0b05d0dda25bfdba5e0a38c9c02189
llm call failed call_id=ce0a8b60bb922 step=extract attempt=1 prompt_hash=ee19f5c91f8d8734f1349b589a15fc80e3dd111e84cc2432c328afd78b7333d2
llm call failed call_id=c553f2bd80984 step=j2 attempt=1 prompt_hash=b88d9a608fb91950d82f43916165eb5cbb701caa859a99ad0a548fdceeab2304
llm call failed call_id=c3142799b52c9 step=j2 attempt=1 prompt_hash=671a8b9baf6f1ee26ca72729637e0efd89e56020b2aae66202fb4080c65455a2
llm call failed call_id=cf07997edda98 step=flags attempt=1 prompt_hash=5a6383ecd9230d9758dfa6fa013c39e9063fc49508710d2380db711382c9c668
llm call failed call_id=c86dd80bcf3a8 step=flags attempt=1 prompt_hash=bb0913399886f3c70cc124cab7255db5354dcf9591f5e818b4440d9cc818ccde
llm call failed call_id=c48e41cf0f7ba step=flags attempt=1 prompt_hash=11ee52ac591f4499e74a5853d7e2285879d3170af512039b8346916170ac1f72
llm call failed call_id=cddaca886e0d1 step=flags attempt=1 prompt_hash=c2720375c5cf949ed50eedab1bfd633794cd873afb05e79aa4146f160c43d781
llm call failed call_id=c898899355068 step=flags attempt=1 prompt_hash=a297283eb4fbe731af04075335fc2197d2468d876985e427c6a98d2bb24cf3b4
llm call failed call_id=ce97efca43393 step=extract attempt=1 prompt_hash=4d2be32aadec8f6c773b344e4a74826ef4f5c42e983b909a1c4ea7a2aa4fa0c4
llm call failed call_id=c1b24fa43561b step=extract attempt=1 prompt_hash=edfb11d933988b8c1a75762df0cf62b58359e69e79390db1562c974a44c54218
llm call failed call_id=c9145306df02c step=extract attempt=1 prompt_hash=edea79f1398615fba03ecd8266fe09577a99db77a35715521fd177fe7a2e6b64
llm call failed call_id=c51f59782c3d5 step=extract attempt=1 prompt_hash=2aca0c360bafeb694b1b74f4ecba896ceb0b05d0dda25bfdba5e0a38c9c02189
llm call failed call_id=c718d92726ea9 step=extract attempt=1 prompt_hash=ee19f5c91f8d8734f1349b589a15fc80e3dd111e84cc2432c328afd78b7333d2
llm call failed call_id=c74384242d0cd step=j2 attempt=1 prompt_hash=b88d9a608fb91950d82f43916165eb5cbb701caa859a99ad0a548fdceeab2304
llm call failed call_id=cde878f3b3f14 step=j2 attempt=1 prompt_hash=671a8b9baf6f1ee26ca72729637e0efd89e56020b2aae66202fb4080c65455a2
llm call failed call_id=cfc2dba58ec42 step=flags attempt=1 prompt_hash=5a6383ecd9230d9758dfa6fa013c39e9063fc49508710d2380db711382c9c668
llm call failed call_id=c03ff9bd69caf step=flags attempt=1 prompt_hash=bb0913399886f3c70cc124cab7255db5354dcf9591f5e818b4440d9cc818ccde
llm call failed call_id=c5b48ec904ef3 step=flags attempt=1 prompt_hash=11ee52ac591f4499e74a5853d7e2285879d3170af512039b8346916170ac1f72
llm call failed call_id=cbdf2e5d220df step=flags attempt=1 prompt_hash=c2720375c5cf949ed50eedab1bfd633794cd873afb05e79aa4146f160c43d781
llm call failed call_id=ca8b58ff9c8fa step=flags attempt=1 prompt_hash=a297283eb4fbe731af04075335fc2197d2468d876985e427c6a98d2bb24cf3b4
llm call failed call_id=ca1e679fd8bca step=extract attempt=1 prompt_hash=4d2be32aadec8f6c773b344e4a74826ef4f5c42e983b909a1c4ea7a2aa4fa0c4
llm call failed call_id=ccb196ebb342d step=extract attempt=1 prompt_hash=edfb11d933988b8c1a75762df0cf62b58359e69e79390db1562c974a44c54218
llm call failed call_id=c3d5103782427 step=extract attempt=1 prompt_hash=edea79f1398615fba03ecd8266fe09577a99db77a35715521fd177fe7a2e6b64
llm call failed call_id=cec0e4cb7bd83 step=extract attempt=1 prompt_hash=2aca0c360bafeb694b1b74f4ecba896ceb0b05d0dda25bfdba5e0a38c9c02189
llm call failed call_id=cd030cc4d1c96 step=extract attempt=1 prompt_hash=ee19f5c91f8d8734f1349b589a15fc80e3dd111e84cc2432c328afd78b7333d2
llm call failed call_id=c157b0f7da454 step=j2 attempt=1 prompt_hash=b88d9a608fb91950d82f43916165eb5cbb701caa859a99ad0a548fdceeab2304
llm call failed call_id=c41fd30f9ec75 step=j2 attempt=1 prompt_hash=671a8b9baf6f1ee26ca72729637e0efd89e56020b2aae66202fb4080c65455a2
llm call failed call_id=c24aeb2f935bb step=flags attempt=1 prompt_hash=5a6383ecd9230d9758dfa6fa013c39e9063fc49508710d2380db711382c9c668
llm call failed call_id=cbe52ec18b1ce step=flags attempt=1 prompt_hash=bb0913399886f3c70cc124cab7255db5354dcf9591f5e818b4440d9cc818ccde
llm call failed call_id=ceafabfb65cf0 step=flags attempt=1 prompt_hash=11ee52ac591f4499e74a5853d7e2285879d3170af512039b8346916170ac1f72
llm call failed call_id=cf51c2db4d3c9 step=flags attempt=1 prompt_hash=c2720375c5cf949ed50eedab1bfd633794cd873afb05e79aa4146f160c43d781
llm call failed call_id=c22f2e08b373c step=flags attempt=1 prompt_hash=a297283eb4fbe731af04075335fc2197d2468d876985e427c6a98d2bb24cf3b4
llm call failed call_id=cd15e56708d57 step=extract attempt=1 prompt_hash=6f9ffc09f221c86fef9901da6d4a27053318e33656ace484829c10e2410b03b1
llm call failed call_id=c0aaa4e3d6007 step=extract attempt=1 prompt_hash=471e5bef463ab68d0664dbb9a5a161ff9fa50f57aa7079ec5b0bd1b3e9079967
llm call failed call_id=cfbc3713adf85 step=extract attempt=1 prompt_hash=7aa46fd9a594ab32bc621f2152d3cd7bca12f3519bbca2217cc082548cb39808
llm call failed call_id=cb49ff5c67709 step=extract attempt=1 prompt_hash=fce3d34156059f99e7f00bd87af54d67fbcf53c763564ed6d0effdf63daef8bf
llm call failed call_id=cc756422730d0 step=extract attempt=1 prompt_hash=a8941c1d05099072f2ace7b8f61a033ce81e465db3005d67d1b866a612deffc1
llm call failed call_id=ca3a51a33116c step=extract attempt=1 prompt_hash=3642d296e71d1b0025a987c7867a708e60b447be9811268f7c711daf9be16dca
llm call failed call_id=cc94a801eacde step=extract attempt=1 prompt_hash=77e7e52aa6377d94fcdd267b8febb2ba8b57c5bc5f96bbf99c9d69e1bf02b54d
llm call failed call_id=cf4fd15f3eb22 step=extract attempt=1 prompt_hash=4c8c8595f475f7d86dbddc9f1452e8597cacc8a8d0f9339f9b0ea71c8e10167d
llm call failed call_id=c3eb4be7e2775 step=extract attempt=1 prompt_hash=dfdd46c5df61f73b971bd2ceffb4e913e07bcd6cbf0d94af5f490040092642fd
llm call failed call_id=c903c6ccca088 step=j2 attempt=1 prompt_hash=b981277d3b10a0179395b3224c23178af9d1ce4b8d404bb9231583846df8194d
llm call failed call_id=c5a0140d9c436 step=j2 attempt=1 prompt_hash=59c06d1eea069f32e98144fc26c58fbbdc06fcaf7cba65f618260d22859cad44
llm call failed call_id=cc9a064b9d526 step=j2 attempt=1 prompt_hash=18bb5c1258fcf7332d49c30ee38b3acac64a3d71e59ced4763440289d8068ed4
llm call failed call_id=cc3cfb010d3fd step=j3 attempt=1 prompt_hash=4c29e19d3f73bdd577721c6dfe20486af726fe64e1c417266f1a04facdff48db
llm call failed call_id=cec0d43ac42c6 step=flags attempt=1 prompt_hash=ef7dc22b7545b66b49af34e89ada544abe1a839790b99dbc5982cbe12964fe66
llm call failed call_id=c9eed7e7fcf52 step=flags attempt=1 prompt_hash=344d0ed599c9e488b646b38b8759ab347fe7f5f817d141266642b03a7dc04b66
llm call failed call_id=ccd47ca78a175 step=flags attempt=1 prompt_hash=84f5ac8f023bb914931488ed3551b70a2146d23f8155b421ef1e715c40f03a02
llm call failed call_id=cffeaaaf1e2fb step=flags attempt=1 prompt_hash=70c2292a7a044464af909beb65cb9d9844c036472c2edbe96bad70a649700462
llm call failed call_id=cf1cd65cbbed6 step=flags attempt=1 prompt_hash=c2f1a5a0ad40210875d422287e9f42dc37b1a79d1ff0f9119244ea9aaf69b042
llm call failed call_id=ce6af58b25250 step=flags attempt=1 prompt_hash=8260767633a4307a942ba50c9fcde2e6eb16c847a2c8d0f439c744b2809d3496
llm call failed call_id=ca7e31951ece7 step=flags attempt=1 prompt_hash=ab11ecb0af01a6f340a55c706226934656bde3f3781cb1739f25ae2c323bd18a
llm call failed call_id=cc00c9fff4bfb step=flags attempt=1 prompt_hash=add65b7fbf9dde3ebfc8a6a907a8807f64adcb92a2b79f49a738f97daa182749
llm call failed call_id=cf41330828fff step=flags attempt=1 prompt_hash=92a650694c93c4041b1c464e4fcd4255f3d3a537a21d100182095e2144ce6e4c
llm call failed call_id=cc25cae03b4e0 step=extract attempt=1 prompt_hash=6f9ffc09f221c86fef9901da6d4a27053318e33656ace484829c10e2410b03b1
llm call failed call_id=cf6d9e433955e step=extract attempt=1 prompt_hash=471e5bef463ab68d0664dbb9a5a161ff9fa50f57aa7079ec5b0bd1b3e9079967
llm call failed call_id=cdb426d8bd08f step=extract attempt=1 prompt_hash=7aa46fd9a594ab32bc621f2152d3cd7bca12f3519bbca2217cc082548cb39808
llm call failed call_id=c516bd5011dec step=extract attempt=1 prompt_hash=fce3d34156059f99e7f00bd87af54d67fbcf53c763564ed6d0effdf63daef8bf
llm call failed call_id=c93f2f61519c2 step=extract attempt=1 prompt_hash=a8941c1d05099072f2ace7b8f61a033ce81e465db3005d67d1b866a612deffc1
llm call failed call_id=c60008c8d9e68 step=extract attempt=1 prompt_hash=3642d296e71d1b0025a987c7867a708e60b447be9811268f7c711daf9be16dca
llm call failed call_id=cd0dda943e8ef step=extract attempt=1 prompt_hash=77e7e52aa6377d94fcdd267b8febb2ba8b57c5bc5f96bbf99c9d69e1bf02b54d
llm call failed call_id=c68da5362b0ee step=extract attempt=1 prompt_hash=4c8c8595f475f7d86dbddc9f1452e8597cacc8a8d0f9339f9b0ea71c8e10167d
llm call failed call_id=cb9721354fc76 step=extract attempt=1 prompt_hash=dfdd46c5df61f73b971bd2ceffb4e913e07bcd6cbf0d94af5f490040092642fd
llm call failed call_id=c877faf482b9d step=j2 attempt=1 prompt_hash=b981277d3b10a0179395b3224c23178af9d1ce4b8d404bb9231583846df8194d
llm call failed call_id=cb367fdff11f0 step=j2 attempt=1 prompt_hash=59c06d1eea069f32e98144fc26c58fbbdc06fcaf7cba65f618260d22859cad44
llm call failed call_id=c2e34b63f9339 step=j2 attempt=1 prompt_hash=18bb5c1258fcf7332d49c30ee38b3acac64a3d71e59ced4763440289d8068ed4
llm call failed call_id=c7887ef6e42ae step=j3 attempt=1 prompt_hash=4c29e19d3f73bdd577721c6dfe20486af726fe64e1c417266f1a04facdff48db
llm call failed call_id=c323037bae731 step=flags attempt=1 prompt_hash=ef7dc22b7545b66b49af34e89ada544abe1a839790b99dbc5982cbe12964fe66
llm call failed call_id=c630df707a7ac step=flags attempt=1 prompt_hash=344d0ed599c9e488b646b38b8759ab347fe7f5f817d141266642b03a7dc04b66
llm call failed call_id=c4e5bbbe78303 step=flags attempt=1 prompt_hash=84f5ac8f023bb914931488ed3551b70a2146d23f8155b421ef1e715c40f03a02
llm call failed call_id=c6daf715d2320 step=flags attempt=1 prompt_hash=70c2292a7a044464af909beb65cb9d9844c036472c2edbe96bad70a649700462
llm call failed call_id=ce1f546d6ded5 step=flags attempt=1 prompt_hash=c2f1a5a0ad40210875d422287e9f42dc37b1a79d1ff0f9119244ea9aaf69b042
llm call failed call_id=c9a2f507705e2 step=flags attempt=1 prompt_hash=8260767633a4307a942ba50c9fcde2e6eb16c847a2c8d0f439c744b2809d3496
llm call failed call_id=c1078ec213cb5 step=flags attempt=1 prompt_hash=add65b7fbf9dde3ebfc8a6a907a8807f64adcb92a2b79f49a738f97daa182749
llm call failed call_id=c9d3ba46e25bd step=flags attempt=1 prompt_hash=ab11ecb0af01a6f340a55c706226934656bde3f3781cb1739f25ae2c323bd18a
llm call failed call_id=c0ec8c76b260e step=flags attempt=1 prompt_hash=92a650694c93c4041b1c464e4fcd4255f3d3a537a21d100182095e2144ce6e4c
llm call failed call_id=cc41bd91712bd step=extract attempt=1 prompt_hash=6f9ffc09f221c86fef9901da6d4a27053318e33656ace484829c10e2410b03b1
llm call failed call_id=c8b7dc9a0f699 step=extract attempt=1 prompt_hash=471e5bef463ab68d0664dbb9a5a161ff9fa50f57aa7079ec5b0bd1b3e9079967
llm call failed call_id=c5fb884f42e0d step=extract attempt=1 prompt_hash=7aa46fd9a594ab32bc621f2152d3cd7bca12f3519bbca2217cc082548cb39808
llm call failed call_id=c9dc973cc88d8 step=extract attempt=1 prompt_hash=fce3d34156059f99e7f00bd87af54d67fbcf53c763564ed6d0effdf63daef8bf
llm call failed call_id=c10a3d6d50386 step=extract attempt=1 prompt_hash=a8941c1d05099072f2ace7b8f61a033ce81e465db3005d67d1b866a612deffc1
llm call failed call_id=c2eec6e61974d step=extract attempt=1 prompt_hash=3642d296e71d1b0025a987c7867a708e60b447be9811268f7c711daf9be16dca
llm call failed call_id=cca67a232ac6c step=extract attempt=1 prompt_hash=77e7e52aa6377d94fcdd267b8febb2ba8b57c5bc5f96bbf99c9d69e1bf02b54d
llm call failed call_id=cf077b5827a2a step=extract attempt=1 prompt_hash=4c8c8595f475f7d86dbddc9f1452e8597cacc8a8d0f9339f9b0ea71c8e10167d
llm call failed call_id=ca8e4aba889a9 step=extract attempt=1 prompt_hash=dfdd46c5df61f73b971bd2ceffb4e913e07bcd6cbf0d94af5f490040092642fd
llm call failed call_id=c3d8d3481a445 step=j2 attempt=1 prompt_hash=b981277d3b10a0179395b3224c23178af9d1ce4b8d404bb9231583846df8194d
llm call failed call_id=c52fd233c4c31 step=j2 attempt=1 prompt_hash=59c06d1eea069f32e98144fc26c58fbbdc06fcaf7cba65f618260d22859cad44
llm call failed call_id=c81f2e9c66900 step=j2 attempt=1 prompt_hash=18bb5c1258fcf7332d49c30ee38b3acac64a3d71e59ced4763440289d8068ed4
llm call failed call_id=c4ddcffb72842 step=j3 attempt=1 prompt_hash=4c29e19d3f73bdd577721c6dfe20486af726fe64e1c417266f1a04facdff48db
llm call failed call_id=c353c4ffaf748 step=flags attempt=1 prompt_hash=ef7dc22b7545b66b49af34e89ada544abe1a839790b99dbc5982cbe12964fe66
llm call failed call_id=c22cbae95be25 step=flags attempt=1 prompt_hash=84f5ac8f023bb914931488ed3551b70a2146d23f8155b421ef1e715c40f03a02
llm call failed call_id=ce6cad9d3edf6 step=flags attempt=1 prompt_hash=344d0ed599c9e488b646b38b8759ab347fe7f5f817d141266642b03a7dc04b66
llm call failed call_id=c3e90c41dc6af step=flags attempt=1 prompt_hash=70c2292a7a044464af909beb65cb9d9844c036472c2edbe96bad70a649700462
llm call failed call_id=c94f32210cdad step=flags attempt=1 prompt_hash=c2f1a5a0ad40210875d422287e9f42dc37b1a79d1ff0f9119244ea9aaf69b042
llm call failed call_id=c41d65b99b99b step=flags attempt=1 prompt_hash=8260767633a4307a942ba50c9fcde2e6eb16c847a2c8d0f439c744b2809d3496
llm call failed call_id=c79388a26f47d step=flags attempt=1 prompt_hash=ab11ecb0af01a6f340a55c706226934656bde3f3781cb1739f25ae2c323bd18a
llm call failed call_id=c82ff8177c0fc step=flags attempt=1 prompt_hash=add65b7fbf9dde3ebfc8a6a907a8807f64adcb92a2b79f49a738f97daa182749
llm call failed call_id=c0004684fdca5 step=flags attempt=1 prompt_hash=92a650694c93c4041b1c464e4fcd4255f3d3a537a21d100182095e2144ce6e4c
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
    Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00 | New patient exam charge $250.00
    Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $180.00 | x-ray charge $180.00
    Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $2,310.00 | treatment visits 1 through 14 charge $2,310.00
    date violations: []
== synth_ambiguous_dos all_accepted: cents=[27500] refused=[] gate={}
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated June 1, 2026): $275.00 | Date of service 04/05/2026: office visit charge $275.00.
    date violations: []
== synth_ambiguous_dos counted: cents=[27500] refused=[] gate={}
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated June 1, 2026): $275.00 | Date of service 04/05/2026: office visit charge $275.00.
    date violations: []
== synth_cms1500_two_dates all_accepted: cents=[15000, 12500] refused=[] gate={'standard': ['Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’: “Source [Ex. __ / Bates __]: "CPT 99213 charge $150.00."”. A charge line carries its own amount only.', 'Line 8 of the letter is a Billed charges line for $125.00 and also states ‘29125 splint charge’: “Source [Ex. __ / Bates __]: "CPT 29125 splint charge $125.00."”. A charge line carries its own amount only.'], 'oneline': ['Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’: “Source [Ex. __ / Bates __]: "CPT 99213 charge $150.00."”. A charge line carries its own amount only.', 'Line 8 of the letter is a Billed charges line for $125.00 and also states ‘29125 splint charge’: “Source [Ex. __ / Bates __]: "CPT 29125 splint charge $125.00."”. A charge line carries its own amount only.']}
    Hobbleton Family Clinic, CMS-1500, date of service [__________] (statement dated April 20, 2026): $150.00 | CPT 99213 charge $150.00.
    Hobbleton Family Clinic, CMS-1500, date of service [__________] (statement dated April 20, 2026): $125.00 | CPT 29125 splint charge $125.00.
    date violations: []
== synth_cms1500_two_dates counted: cents=[15000, 12500] refused=[] gate={'standard': ['Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’: “Source [Ex. __ / Bates __]: "CPT 99213 charge $150.00."”. A charge line carries its own amount only.', 'Line 8 of the letter is a Billed charges line for $125.00 and also states ‘29125 splint charge’: “Source [Ex. __ / Bates __]: "CPT 29125 splint charge $125.00."”. A charge line carries its own amount only.'], 'oneline': ['Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’: “Source [Ex. __ / Bates __]: "CPT 99213 charge $150.00."”. A charge line carries its own amount only.', 'Line 8 of the letter is a Billed charges line for $125.00 and also states ‘29125 splint charge’: “Source [Ex. __ / Bates __]: "CPT 29125 splint charge $125.00."”. A charge line carries its own amount only.']}
    Hobbleton Family Clinic, CMS-1500, date of service [__________] (statement dated April 20, 2026): $150.00 | CPT 99213 charge $150.00.
    Hobbleton Family Clinic, CMS-1500, date of service [__________] (statement dated April 20, 2026): $125.00 | CPT 29125 splint charge $125.00.
    date violations: []
== synth_sample_er_next_visit all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 16, 2026: $6,240.00 | ER charges: $6,240, next visit date 01/16/2026.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_next_visit counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 16, 2026: $6,240.00 | ER charges: $6,240, next visit date 01/16/2026.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:36.962Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence; for c in sample case_09 lib14 lib10 lib11 synth_ambiguous_dos synth_cms1500_two_dates; do for v in all_accepted counted; do for k in letter notes; do f=$c-$v-$k.txt; if cmp -s T-202-paralegal-r2/letters/$f T-202-paralegal-r3/letters/$f; then echo \"same $f\"; else echo \"DIFF $f\"; fi; done; done; done > T-202-paralegal-r3/letters_vs_r2.out; cat T-202-paralegal-r3/letters_vs_r2.out; grep -n \"Date:\" ../../evals/golden/sample.txt | head -12",
 "description": "Compare r3 letters to r2 letters"
}
````

### User / tool · 2026-11-03T01:29:37.151Z

**tool result**
````
same sample-all_accepted-letter.txt
same sample-all_accepted-notes.txt
same sample-counted-letter.txt
same sample-counted-notes.txt
same case_09-all_accepted-letter.txt
same case_09-all_accepted-notes.txt
same case_09-counted-letter.txt
same case_09-counted-notes.txt
same lib14-all_accepted-letter.txt
same lib14-all_accepted-notes.txt
same lib14-counted-letter.txt
same lib14-counted-notes.txt
same lib10-all_accepted-letter.txt
same lib10-all_accepted-notes.txt
same lib10-counted-letter.txt
same lib10-counted-notes.txt
same lib11-all_accepted-letter.txt
same lib11-all_accepted-notes.txt
DIFF lib11-counted-letter.txt
DIFF lib11-counted-notes.txt
DIFF synth_ambiguous_dos-all_accepted-letter.txt
DIFF synth_ambiguous_dos-all_accepted-notes.txt
DIFF synth_ambiguous_dos-counted-letter.txt
DIFF synth_ambiguous_dos-counted-notes.txt
DIFF synth_cms1500_two_dates-all_accepted-letter.txt
DIFF synth_cms1500_two_dates-all_accepted-notes.txt
DIFF synth_cms1500_two_dates-counted-letter.txt
DIFF synth_cms1500_two_dates-counted-notes.txt
4:Date: 2026-01-09
9:Date: 2026-01-09
14:Date: 2026-01-16
19:Date: 2026-01-23
24:Date: 2026-02-20
29:Date: 2026-03-06
34:Date: 2026-05-18
39:Date: 2026-05-29
44:Date: 2026-06-12
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:38.173Z

Now read the lib11 counted letter and notes as a demand letter would print them.

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:39.814Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/letters; cat lib11-counted-letter.txt; echo; echo =========NOTES; cat lib11-counted-notes.txt; echo ======; diff ../../T-202-paralegal-r2/letters/synth_ambiguous_dos-all_accepted-notes.txt synth_ambiguous_dos-all_accepted-notes.txt",
 "description": "Read lib11 counted letter and notes"
}
````

### User / tool · 2026-11-03T01:29:39.915Z

**tool result**
````
TREATMENT CHRONOLOGY

March 18, 2026 — Wexcombe Memorial ED
Diagnosed with cervical strain and lumbar strain; cervical and lumbar spine X-rays negative for fracture.
Source [Ex. __ / Bates __]: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture."

March 27, 2026 — Fennimoor Spine Clinic, new patient
Neck pain 7/10 and low back pain 7/10; treating under a letter of protection; plan is chiropractic care three times weekly.
Source [Ex. __ / Bates __]: "Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly."

March 27, 2026 — Fennimoor Spine Clinic, new patient intake form (OCR text)
Intake form: rear ended at red light, neck and back hurt; prior accidents and prior injuries marked No; pain today 7.
Source [Ex. __ / Bates __]: "How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7."

April 24, 2026 — Fennimoor Spine Clinic, visit 8
Neck pain 5/10 and low back pain 6/10; manual therapy and exercises continued.
Source [Ex. __ / Bates __]: "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued."

May 29, 2026 — Fennimoor Spine Clinic, visit 14
Neck pain 4/10, low back pain 5/10. Care continues.
Source [Ex. __ / Bates __]: "Neck pain 4/10, low back pain 5/10. Care continues."

BILLED CHARGES

Wexcombe Memorial ED, March 18, 2026: $3,260.00
Source [Ex. __ / Bates __]: "ED charge: $3,260."
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00
Source [Ex. __ / Bates __]: "New patient exam charge $250.00"
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $180.00
Source [Ex. __ / Bates __]: "x-ray charge $180.00"
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $2,310.00
Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"

Billed charges accepted from these records: $6,000.00
=========NOTES
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 7.

FLAGS ACCEPTED
- Gap: 35 days, April 24, 2026 to May 29, 2026: record 7 (Fennimoor Spine Clinic, visit 8, April 24, 2026) to record 8 (Fennimoor Spine Clinic, visit 14, May 29, 2026).
- Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior accidents? Yes [ ] No [X]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
- Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior injuries? Yes [ ] No IX]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
- Prior condition: record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "Problem list: hypertension, type 2 diabetes, chronic low back pain."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."; record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior accidents?"; record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior injuries?".
- Causation language: record 2 (Ashgrove Fire-Rescue run report, March 18, 2026) "Ambulatory at scene."; record 4 (Pellingham and Rook PLLC, correspondence (letter of protection), March 26, 2026) "Letter of protection to Fennimoor Spine Clinic."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Patient referred by attorney."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Treating under a letter of protection."; record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) "Account held under letter of protection."

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- Record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026): "Treating under a letter of protection." Causation language.
- Record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026): "Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]." Conflict, other fact mismatch; prior condition.
- Record 7 (Fennimoor Spine Clinic, visit 8, April 24, 2026): "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued." Gap.
- Record 8 (Fennimoor Spine Clinic, visit 14, May 29, 2026): "Neck pain 4/10, low back pain 5/10. Care continues." Gap.

AMOUNTS NOT TOTALED
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Adjustment (courtesy discount) -$274.00." Not totaled ($274.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.

DAMAGES MENTIONS (not charges)
- none

FUTURE TREATMENT RECOMMENDED (no cost stated)
- none

BILLS TO REQUEST (entry in the letter, no accepted charge)
- none

CHARGES WITHOUT A CERTAIN DATE OF SERVICE
- Fennimoor Spine Clinic, $250.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
- Fennimoor Spine Clinic, $180.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
- Fennimoor Spine Clinic, $2,310.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.

RECORDS NOT IN THE TREATMENT SECTION
- Record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) — not reviewed
- Record 2 (Ashgrove Fire-Rescue run report, March 18, 2026) — not reviewed
- Record 4 (Pellingham and Rook PLLC, correspondence (letter of protection), March 26, 2026) — not reviewed
- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) — states a dollar amount, not exported (this record is a bill and its charges are already listed under Billed charges, so dismiss this entry unless it states treatment)

EDITED ITEMS
- none

PENDING ITEMS NOT INCLUDED
- Entry, record 1 (Dr. Hesper Alderton, primary care, March 4, 2026): "Annual visit; history per patient of car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
- Entry, record 2 (Ashgrove Fire-Rescue run report, March 18, 2026): "Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ambulatory at scene and transported to Wexcombe Memorial ED."
- Entry, record 4 (Pellingham and Rook PLLC, correspondence (letter of protection), March 26, 2026): "Law firm letter of protection to Fennimoor Spine Clinic states the firm represents the client for injuries from a collision on 2026-03-18 and asks the clinic to defer collection while the claim is pending."
- Entry, record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Itemized ledger lists new patient exam charge $250.00, x-ray charge $180.00, treatment visits 1 through 14 charge $2,310.00, and total charges $2,740.00."
- Amount $2,740 (unclear), record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "total charges $2,740.00."
- Amount $300 (unclear), record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Payment received $300.00."
- Amount $2,166 (unclear), record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Balance due $2,166.00."======
26a27,29
> CHARGES WITHOUT A CERTAIN DATE OF SERVICE
> - Hobbleton Family Clinic, $275.00: The quote labels 04/05/2026 as the date of service, and it can be read as month/day or day/month; the record does not settle which. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
>
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:51.001Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence; cat T-060-paralegal-pass4-serve.py; echo ====; cat T-202-paralegal-r2/h.py | head -80; echo ====; wc -l T-202-paralegal-r2/p01_cases.py T-202-paralegal-r2/api_service_date.py",
 "description": "Read server launcher and helper scripts"
}
````

### User / tool · 2026-11-03T01:29:51.115Z

**tool result**
````
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
====
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
====
     126 T-202-paralegal-r2/p01_cases.py
      15 T-202-paralegal-r2/api_service_date.py
     141 total
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:52.820Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence; cat T-202-paralegal-r2/p01_cases.py; cat T-202-paralegal-r2/api_service_date.py",
 "description": "Read r2 Playwright case script"
}
````

### User / tool · 2026-11-03T01:29:52.915Z

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
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:58.050Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence; cp T-202-paralegal-r2/h.py T-202-paralegal-r3/h.py && cp T-202-paralegal-r2/p01_cases.py T-202-paralegal-r3/p01_cases.py && cp T-202-paralegal-r2/api_service_date.py T-202-paralegal-r3/api_service_date.py && lsof -iTCP:7981 -sTCP:LISTEN -nP; echo \"lsof exit $?\"; grep -n \"library-\\|lib11\" ../../evals/library/*.txt 2>/dev/null | head -0; ls ../../evals/library | grep lib11",
 "description": "Copy UI scripts and check port 7981"
}
````

### User / tool · 2026-11-03T01:29:58.477Z

**tool result**
````
lsof exit 1
head: illegal line count -- 0
case_lib11_priors_and_ledger.expected.json
case_lib11_priors_and_ledger.txt
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:29:59.516Z

Now update the copies for r3 (port, lib11).

### Assistant · claude-opus-5-5 · 2026-11-03T01:30:01.126Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/h.py",
 "old_string": "BASE = os.environ.get(\"T181_BASE\", \"http://127.0.0.1:7976\")  # T-202 r2: 986fc55 archive, port 7976",
 "new_string": "BASE = os.environ.get(\"T181_BASE\", \"http://127.0.0.1:7981\")  # T-202 r3: 973b542 archive, port 7981"
}
````

### User / tool · 2026-11-03T01:30:01.235Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/h.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:30:04.475Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/p01_cases.py",
 "old_string": "CASES = os.environ.get(\"CASES\", \"sample,case_09,lib14,lib10\").split(\",\")\nPASTE = {\"case_09\": \"/Users/arsis/zlayt-pm-project/evals/golden/case_09_nonvisit_hides_gap.txt\"}\nLIB = {\"lib14\": \"case_lib14_handwritten_chiro_scans\", \"lib10\": \"case_lib10_eob_ub04_cms1500\"}",
 "new_string": "CASES = os.environ.get(\"CASES\", \"sample,case_09,lib14,lib10,lib11\").split(\",\")  # r3: 973b542 archive, port 7981, lib11 added\nPASTE = {\"case_09\": \"/Users/arsis/zlayt-pm-project/evals/golden/case_09_nonvisit_hides_gap.txt\"}\nLIB = {\"lib14\": \"case_lib14_handwritten_chiro_scans\", \"lib10\": \"case_lib10_eob_ub04_cms1500\", \"lib11\": \"case_lib11_priors_and_ledger\"}"
}
````

### User / tool · 2026-11-03T01:30:04.576Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/p01_cases.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:30:09.273Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; mkdir -p artifacts/review-evidence/T-202-paralegal-r3/db; env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/db/r3.db PORT=7981 HOST=127.0.0.1 nohup .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/server.log 2>&1 &\necho started",
 "description": "Start archive app on port 7981"
}
````

### User / tool · 2026-11-03T01:30:09.389Z

**tool result**
````
started
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:30:11.373Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; for i in 1 2 3 4 5 6 7 8; do curl -s -o /dev/null -w \"%{http_code}\" http://127.0.0.1:7981/api/health && break; /bin/sleep 1; done; echo; curl -s http://127.0.0.1:7981/api/health; echo; lsof -iTCP:7981 -sTCP:LISTEN -nP",
 "description": "Check health of archive app"
}
````

### User / tool · 2026-11-03T01:30:11.588Z

**tool result**
````
200
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  24454 arsis    9u  IPv4 0x812ee6994d0cf19f      0t0  TCP 127.0.0.1:7981 (LISTEN)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:30:14.126Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/h.py artifacts/review-evidence/T-202-paralegal-r3/p01_cases.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/p01.out 2>&1; echo $?; grep -n \"draft took\\|done in\\|created via\\|ERRORS\\|Error\\|Traceback\" artifacts/review-evidence/T-202-paralegal-r3/p01.out | head -30",
 "description": "Drive five cases through UI with Playwright",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T01:31:34.731Z

**tool result**
````
0
2:[sample] draft took 2.2 s
85:[sample] done in 15.5 s
86:[case_09] created via POST /api/cases token=zHgWVODvNh2s_umk2ONqkg
87:[case_09] draft took 2.5 s
147:[case_09] done in 8.2 s
148:[lib14] draft took 2.4 s
226:[lib14] done in 13.1 s
227:[lib10] draft took 2.4 s
323:[lib10] done in 19.1 s
324:[lib11] draft took 2.4 s
421:[lib11] done in 24.2 s
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:31:37.854Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3; for c in sample case_09 lib14 lib10 lib11; do echo \"== $c\"; grep -A1 -E \"^(.*), (date of service|[A-Z][a-z]+ [0-9])\" ui-$c-letter.txt | sed -n '/BILLED/,$p' >/dev/null; awk '/BILLED CHARGES/{f=1} f' ui-$c-letter.txt; done; for c in sample case_09 lib14 lib10; do cmp -s ui-$c-letter.txt ../T-202-paralegal-r2/ui-$c-letter.txt && echo \"same-as-r2 $c\" || echo \"DIFF-vs-r2 $c\"; done",
 "description": "Show billed-charge sections of UI letters"
}
````

### User / tool · 2026-11-03T01:31:38.049Z

**tool result**
````
== sample
BILLED CHARGES

Central ER discharge summary, January 9, 2026: $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240."
Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
Source [Ex. __ / Bates __]: "Charge: $2,150."

Billed charges accepted from these records: $8,390.00
== case_09
BILLED CHARGES

Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00
Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."

Billed charges accepted from these records: $275.00
== lib14
BILLED CHARGES

Orrin Mere Regional ED, September 14, 2026: $2,960.00
Source [Ex. __ / Bates __]: "ED charge: $2,960."
Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00
Source [Ex. __ / Bates __]: "A0427 ALS emergency transport, 1 unit, charge $1,380.00."
Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05
Source [Ex. __ / Bates __]: "charge $187.05."

Billed charges accepted from these records: $4,527.05
== lib10
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
== lib11
BILLED CHARGES

Wexcombe Memorial ED, March 18, 2026: $3,260.00
Source [Ex. __ / Bates __]: "ED charge: $3,260."
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00
Source [Ex. __ / Bates __]: "New patient exam charge $250.00"
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $180.00
Source [Ex. __ / Bates __]: "x-ray charge $180.00"
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $2,310.00
Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"

Billed charges accepted from these records: $6,000.00
same-as-r2 sample
same-as-r2 case_09
same-as-r2 lib14
same-as-r2 lib10
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:31:41.989Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"Excerpt\" evals/library/case_lib11_priors_and_ledger.txt | tail -2; grep -n \"lib11\\] s3\" artifacts/review-evidence/T-202-paralegal-r3/p01.out | cut -c1-420; grep -n \"CHARGES WITHOUT\" -A4 artifacts/review-evidence/T-202-paralegal-r3/ui-lib11-notes.txt",
 "description": "Check lib11 ledger text, Step 3 cards, UI notes"
}
````

### User / tool · 2026-11-03T01:31:42.095Z

**tool result**
````
41:Excerpt: "Neck pain 4/10, low back pain 5/10. Care continues."
46:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection."
347:[lib11] s3 item=a1 boxes=[] :: Charge / Wexcombe Memorial ED · March 18, 2026 /  / $3,260.00 /  / Date of service March 18, 2026 /  / Written in the record as $3,260. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
349:[lib11] s3 item=a2 boxes=['check-separate', 'check-compare'] :: Not counted yet / Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026 /  / $250.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge for a service. / A second AI check thought this
351:[lib11] s3 item=a3 boxes=['check-separate', 'check-compare'] :: Not counted yet / Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026 /  / $180.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge for a service. / A second AI check thought this
353:[lib11] s3 item=a4 boxes=['check-separate', 'check-compare'] :: Not counted yet / Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026 /  / $2,310.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge for a service. / A second AI check thought th
355:[lib11] s3 item=a5 boxes=['check-compare'] :: Never counted / Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026 /  / $2,740.00 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount again
357:[lib11] s3 item=a6 boxes=['check-compare'] :: Never counted / Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026 /  / $300.00 /  / Payment: money received, not a charge. /  / A second AI check thought this may be a damages figure (for example lost wages), not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted wor
359:[lib11] s3 item=a7 boxes=[] :: Never counted / Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026 /  / $274.00 /  / Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges. /  / Either way, it is never added to the bill total.
361:[lib11] s3 item=a8 boxes=['check-compare'] :: Never counted / Fennimoor Spine Clinic, itemized ledger · statement dated June 15, 2026 /  / $2,166.00 /  / Balance or amount due: worked out from charges, payments and adjustments, not a charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount ag
38:CHARGES WITHOUT A CERTAIN DATE OF SERVICE
39-- Fennimoor Spine Clinic, $250.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
40-- Fennimoor Spine Clinic, $180.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
41-- Fennimoor Spine Clinic, $2,310.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
42-
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:31:44.641Z

**tool call — Bash**
````
{
 "command": "kill 24454; /bin/sleep 1; lsof -iTCP:7981 -sTCP:LISTEN -nP; echo \"lsof exit $?\"; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7981/api/health",
 "description": "Stop archive server and confirm closed"
}
````

### User / tool · 2026-11-03T01:31:45.845Z

**tool result (error)**
````
Exit code 7
lsof exit 1
000
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:31:51.224Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542; grep -n -i \"next visit\\|last visit\\|previous\\|prior visit\\|initial visit\\|return visit\\|follow-up visit date\" tests/unit/test_t202_r3_allow_list.py | head; echo \"grep exit $?\"; grep -n \"_SERVICE_PHRASES = \" evals/letter_check.py",
 "description": "Check tests for other-visit label probes"
}
````

### User / tool · 2026-11-03T01:31:51.324Z

**tool result**
````
grep exit 0
190:_SERVICE_PHRASES = ("dos", "date of service", "dates of service", "date(s) of service", "service date", "service dates", "visit date", "date of visit", "visit of", "seen", "seen on",
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:31:59.504Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/before_t202.py",
 "content": "\"\"\"T-202 r3 paralegal: the SYNTHETIC sample variant (ER note 'ER charges: $6,240, next visit date 01/16/2026.') on the pre-T-202 build (bd72d5b, T-200),\nto show what the charge line printed before T-202. Prints only the BILLED CHARGES section of the all_accepted letter.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/before_t202.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nos.environ.setdefault(\"LLM_BACKEND\", \"fixture\")\nos.environ.setdefault(\"FIXTURE_SET\", \"curated\")\nfrom evals import letter_check as LC  # noqa: E402\n\nSAMPLE = open(\"evals/golden/sample.txt\").read()\nNEXTV = SAMPLE.replace(\"Follow up with PCP in 1 week. ER charges: $6,240.\", \"Follow up with PCP in 1 week. ER charges: $6,240, next visit date 01/16/2026.\")\nassert NEXTV != SAMPLE\ngot = LC.letters_for(NEXTV)\ntxt = got[\"all_accepted\"][\"letters\"][\"standard\"]\nprint(txt[txt.index(\"BILLED CHARGES\"):])\n"
}
````

### User / tool · 2026-11-03T01:31:59.602Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/before_t202.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:32:03.338Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/pre_bd72d5b && git archive bd72d5b | tar -x -C $S/pre_bd72d5b && git log -1 --format=%H%n%s bd72d5b",
 "description": "Extract pre-T-202 archive bd72d5b"
}
````

### User / tool · 2026-11-03T01:32:04.838Z

**tool result**
````
bd72d5b9a6dcf94eba56df71e612d4f240351ba5
fix(backend): T-200 counted undated ledger charge prints its statement date as such, never as a service date
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:32:09.497Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/before_t202.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pre_bd72d5b 2>/dev/null > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/before_t202.out; echo $?; cat artifacts/review-evidence/T-202-paralegal-r3/before_t202.out",
 "description": "Run sample variant on pre-T-202 build"
}
````

### User / tool · 2026-11-03T01:32:10.315Z

**tool result**
````
0
BILLED CHARGES

Central ER discharge summary, January 9, 2026: $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240, next visit date 01/16/2026."
Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
Source [Ex. __ / Bates __]: "Charge: $2,150."

Billed charges accepted from these records: $8,390.00
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:32:37.441Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542; grep -n \"fill it from the quote\" app/backend/export.py; grep -n \"if bill and not _plausible\" app/backend/service_date.py; grep -n \"_SVC_CORE = \" app/backend/service_date.py; grep -n \"in a visit note (not a bill)\" evals/letter_check.py; grep -n \"\\\"no_date\\\": \\\"The line states no date\" app/backend/service_date.py; grep -n \"notes\\[\\|keeps the note\\|record's date\\|date_iso\" app/backend/service_date.py | sed -n 1,20p",
 "description": "Get exact line refs for the review"
}
````

### User / tool · 2026-11-03T01:32:37.583Z

**tool result**
````
614:            out.append(f"- {_provider(v.source(a['record_no'])) or v.source(a['record_no'])}, {a['raw']}: {why} The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.")
291:    if bill and not _plausible(first, last, ref):
43:_SVC_CORE = (r"\bdos|\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?|\bvisit\s+dates?|\bdates?\s+of\s+visit|\bvisit\s+of|\bseen(?:\s+on)?|"
342:        record's date; in a visit note (not a bill) -> the note's own date (the blank is a violation there).
100:    "no_date": "The line states no date of service.",
304:def resolve(excerpt: str, start: int, source, date_iso) -> dict:
307:    `date_iso`. Only labeled dates are candidates (module doc); see it for the rules."""
340:            return _apply(out, _decide(lab, seg, date_iso, bill))
346:            return _apply(out, _decide(lab, own, date_iso, bill))
351:                return _apply(out, _decide(lab, whole, date_iso, bill))
355:            return _apply(out, _decide(lab, tail, date_iso, bill))
365:                r = _certain(u, date_iso)
371:                return _apply(out, _decide(uniq, prefix, date_iso, bill))
375:    if date_iso:                                                          # a dated encounter record (visit note, imaging report): the record's date is the visit
376:        out.update(state="stated", first=date_iso, last=None, reason=None, raw="", raws=[])
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:32:43.146Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; head -15 artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py; ls artifacts/review-evidence/T-202-paralegal-r3/ | head -50; grep -c \"\" artifacts/review-evidence/T-202-paralegal-r3/p01.out",
 "description": "Check jsoncheck usage and evidence files"
}
````

### User / tool · 2026-11-03T01:32:43.249Z

**tool result**
````
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
api_service_date.py
before_t202.out
before_t202.py
case_09-s3-00-a1.png
case_09-step2-done.png
case_09-step3-done.png
case_09-step4.png
db
h.py
letter_check.out
letters
letters_dump_r3.out
letters_dump_r3.py
letters_vs_r2.out
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
lib11-s3-00-a1.png
lib11-s3-01-a2.png
lib11-s3-02-a3.png
lib11-s3-03-a4.png
lib11-s3-04-a5.png
lib11-s3-05-a6.png
lib11-s3-06-a7.png
lib11-s3-07-a8.png
lib11-step2-done.png
lib11-step3-done.png
lib11-step4.png
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
probe_r3.out
421
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:32:45.965Z

**tool call — Bash**
````
{
 "command": "rm /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/api_service_date.py; ls /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/ | grep -c png",
 "description": "Remove unused copied API script"
}
````

### User / tool · 2026-11-03T01:32:46.060Z

**tool result**
````
44
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:32:46.876Z

Now the draft review.

### Assistant · claude-opus-5-5 · 2026-11-03T01:33:42.732Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/draft-T-202-paralegal-r3.md",
 "content": "# T-202 round 3 (final): D-071 allow-list + fillable blank — paralegal review (Maria Delgado, senior PI litigation paralegal)\n\n**Verdict: fail.** Round 3 fixes everything I raised in round 2, and the blank reads well in a demand letter. But the allow-list has a hole in the opposite direction, and it is the same class of error as my round 2 blocker: a wrong date printed in the date-of-service slot.\n\nThe words \"visit date\" and \"seen on\" are trusted even when they name a different visit (next, last, previous, initial), and in a visit note such a date overrides the note's own date. Take Appendix A's own ER note, with the follow-up written after the charge: \"ER charges: $6,240, next visit date 01/16/2026.\" The build prints `Central ER discharge summary, January 16, 2026: $6,240.00`. The ER visit was January 9. The pre-T-202 build (bd72d5b) printed January 9 on the same text. letter_check passes the wrong line with 0 violations, and it flags the correct January 16 → January 9 swap the other way: given the right record date, it reports a violation.\n\n**What round 3 fixed (re-run on 973b542):**\n- **Round 2 blocker (B1–B12, N11–N13).** Birth, injury/DOI, accident, onset, referral and order dates now give the blank in a bill. In visit notes they give the note's own date: B8 prints January 16 and B9 February 20 (probe_r3.out:221, :224).\n- **Round 1 blockers.** These still hold: Posted-first ledgers print the DOS (T2, N1, N2, N24, N25), and the CMS-1500 \"X and Y\" list gives the blank.\n- **Round 2 major (\"service date not stated\" above a quote that states one).** Gone. Every uncertain line now prints `date of service [__________] (statement dated X)`, which claims nothing (D-071 addendum).\n- **Round 2 minors.**\n  - \"Trans Date\" now gives the blank.\n  - P10 and N17 periods print as ranges.\n  - The notes now have a CHARGES WITHOUT A CERTAIN DATE OF SERVICE section.\n  - The not-stated string question is superseded by the addendum.\n- **Corpus.** Letters for the sample, case_09, lib14 and lib10 are byte-identical to round 2 (UI download and in-process), and right. lib11's counted ledger lines print the blank.\n\n**The blank, read as a demand letter.** `Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00` works:\n- it is as conspicuous as the Bates placeholder;\n- it states nothing false;\n- the statement date is labelled as a statement date;\n- the notes list every blank.\n\nI would fill it from the chart notes or a records request before sending. Two wording gaps remain (minor):\n- The notes say \"fill it from the quote\" even when the quote has no date.\n- The \"treatment visits 1 through 14\" line offers a single-date blank for what needs a range.\n\n**Scope.**\n- **Build:** `git archive 973b542` (tree 4c457a4b…) extracted to the session scratchpad (pr3_973b542/).\n- **Pre-T-202 comparison:** a bd72d5b archive (pre_bd72d5b/).\n- **Server:** fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local (health: demo_mode true, local_mode true), http://127.0.0.1:7981.\n- **Shutdown:** listener PID 24454 killed. `lsof` exit 1, `curl` 000.\n- **Private values:** 1 <redacted> (a commit author line in `git show` output), not quoted.\n- **Not graded:** Step 3 wording (separate card).\n\n```json\n{\"card\": \"T-202\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"commit 973b542 (git archive, tree 4c457a4bfb6c, extracted to session scratchpad pr3_973b542/); bd72d5b archive (pre-T-202, T-200) for the before/after on the new blocker. Demo mode: fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, http://127.0.0.1:7981 (health demo_mode true, local_mode true); listener PID 24454 stopped (lsof exit 1, curl 000). Cases: sample (sample tile), case_09 (POST /api/cases with the golden text, opened in the UI), lib14, lib10, lib11 (library tile); in-process letters for the same five plus three SYNTHETIC variants. Evidence: artifacts/review-evidence/T-202-paralegal-r3/. Step 3 wording not graded (separate card). Private values seen: 1 <redacted>.\",\n \"exercised\": [\n  \"Read personas/paralegal.md, my round 2 review, D-071 + amendment + clarification + addendum (memory/ORCHESTRATOR_DECISIONS.md:84-93), board.py show T-202 (notes, handoff), git show 973b542 (service_date.py, export.py, store.py)\",\n  \"From the archive: pytest test_t202_r3_allow_list + test_t202_r2_service_date_layouts + test_t202_charge_service_dates + test_t200_undated_charge_label '211 passed in 7.88s' (pytest-t202.out); python -m evals.letter_check value 0 over 25 cases (letter_check.out)\",\n  \"Every round 1 and round 2 bill text, loaded verbatim from my r2 probe files (P1-P10, T1-T3, N1-N25, B1-B12), plus 16 new R shapes, through the shipped store.charge_service_date (probe_r3.py -> probe_r3.out, 66 probes)\",\n  \"Other-visit labels in visit notes and bills (R1, R2, R17-R23) and letter_check.charge_date_violations on the build's line vs the record-date line (probe_r3b.out); sample-styled punctuation variants C1-C7 (probe_r3c.out)\",\n  \"SYNTHETIC sample variant 'ER charges: $6,240, next visit date 01/16/2026.' through the full letter on 973b542 (letters_dump_r3.out) and on bd72d5b (before_t202.out)\",\n  \"Playwright on the running archive app (h.py + p01_cases.py): sample, case_09, lib14, lib10, lib11 keyboard-first through Steps 1-4, Step 3 cards logged and screenshotted, letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); sample/case_09/lib14/lib10 letters cmp-identical to round 2\",\n  \"In-process letters + notes, all_accepted and counted (letters_dump_r3.py): sample, case_09, lib14, lib10, lib11, synth_ambiguous_dos, synth_cms1500_two_dates, synth_sample_er_next_visit (letters/); diffed against round 2 (letters_vs_r2.out); read as a demand letter\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 4, \"letter_dates_correct_on_corpus\": 5, \"blank_in_demand_letter\": 4, \"adjuster_credibility\": 3},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"A 'visit date' / 'seen on' label naming another visit (next, last, previous, initial) prints that visit's date as the charge's date of service; in a visit note it overrides the note's own correct date (regression vs pre-T-202), and letter_check enforces the wrong date\",\n   \"evidence\": \"artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.out: SYNTHETIC sample variant (Appendix A record 2, ER note dated 2026-01-09, excerpt ending 'ER charges: $6,240, next visit date 01/16/2026.') prints 'Central ER discharge summary, January 16, 2026: $6,240.00' with 'date violations: []'. Same text on bd72d5b (before_t202.out) prints 'Central ER discharge summary, January 9, 2026: $6,240.00'. probe_r3b.out: R1 'Next visit date 01/30/2026, office visit charge $150.00.' (note 2026-01-16) -> 'Dr. Alvarez, primary care, January 30, 2026'; R2 'Previously seen on 01/09/2026 in the ER, follow-up visit charge $150.00.' -> January 9; R17 'Visit charge: $150.00   Next visit date: 01/30/2026' -> January 30; R18 'Last visit date: 01/09/2026   Visit charge: $150.00' -> January 9; R19 PT discharge 2026-03-06 'Initial visit date 01/23/2026, discharge visit charge $185.00.' -> January 23; R23 bill 'next visit date 02/28/2026' after the figure -> February 28. probe_r3c.out: C4 'ER charges: $6,240, next visit date 01/16/2026.' and C7 'Follow-up visit date: 01/16/2026  ER charges: $6,240' -> January 16; C6 PT eval 01/23 'Next visit date: 01/27/2026   Charge per visit $185' -> January 27. Only a sentence break protects the line (C1, C3, C5 keep the record date). letter_check: for R1, R2, R17, R18, R19 the build's wrong line gives 'violations: []' and the record-date line gives 'charge line's date is not certain from its quote (the quote's labeled date of service reads 2026-01-30)' (probe_r3b.out). Cause: service_date.py:43 _SVC_CORE accepts 'visit date' and 'seen' with no check of the word before them (next/last/previous/initial/return/follow-up), and a labeled date wins before the record-date fallback at service_date.py:375-376; the after-statement check runs only for bills (service_date.py:291), so a visit note accepts a date after its own date (January 30 on a January 16 note). evals/letter_check.py:190 _SERVICE_PHRASES carries the same 'visit date'/'seen' entries. tests/unit/test_t202_r3_allow_list.py has no next/last/previous/initial visit fixture (grep printed nothing).\",\n   \"why_it_matters\": \"The brief and D-071 allow exactly two outputs for a charge line: a certain service date or the blank. 'January 16, 2026: $6,240.00' for an ER visit on January 9 is a wrong date of service on the largest charge in the sample case. The January 16 date belongs to the PCP follow-up, so the adjuster sees the ER bill dated to a different provider's visit. In a case with a disputed accident date (01/09 vs 01/19), any charge-date error is ammunition. It is a regression: the same text printed January 9 before T-202. And the eval now treats the correct date as the violation, so a later fix would be pushed back. Charges inside clinical notes are Appendix A's own pattern ('ER charges: $6,240.', 'Charge per visit $185.'), and checkout lines ('Visit charge ... Next visit date ...') are common in EHR visit summaries.\",\n   \"fix\": \"In a dated encounter record (not a bill), the record's date is the visit. A labeled date there prints only when it equals the record's date; any other labeled date gives the record's date, or the blank with a note naming both. Everywhere (bills too), a visit or seen label preceded by next, last, previous, prior, initial, first, return, follow-up, scheduled or upcoming is not a service label. A date after the record's own date is never a service date in any record (extend the service_date.py:291 check beyond bills). Mirror both rules in letter_check with its own word list.\",\n   \"acceptance_test\": \"Unit fixtures R1, R2, R17, R18, R19, R23 and C4, C6, C7 from probe_r3b.py/probe_r3c.py. Visit notes print the record's date (January 16, 2026; January 9 for C4/C7; January 23 for C6; March 6 for R19) or the blank, never January 30, 27 or 23 or the prior-visit date. R23 gives the blank. letter_check reports a violation on each of the build's current R1/R2/R17/R18/R19 lines and none on the record-date line. A SYNTHETIC golden or library case whose ER or visit note writes the next visit date after the charge with a comma prints the ER date.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The note says 'The line states no date of service' or 'not labeled as a date of service' for lines that do label one in a form the code does not read (DOS with ordinal, UB-04 FL6 six-digit period, CMS-1500 Item 24A)\",\n   \"evidence\": \"probe_r3.out R15 'DOS Feb. 2nd, 2026 office visit charge $275.00.' gives the blank with reason=no_date and 'The line states no date of service.'. N20 'FL6 statement covers period FROM 060926 THROUGH 061226.' gives the same. N8 'Item 24A 06/24/2026 CPT 99204 $185.00.' gives 'The only date near this line (06/24/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting...'. Text at service_date.py:100. The blank is safe in all three; only the note is wrong.\",\n   \"why_it_matters\": \"The note and the notes section are where I learn what to fill in. 'States no date' sends me to request a bill I already hold. Calling Item 24A 'possibly a birth or injury date' is wrong on its face to anyone who reads CMS-1500s, and it erodes trust in every other note.\",\n   \"fix\": \"When a service label (DOS, 24A, FL6 / statement covers period) is present but its date is not parsed, use the written-date note naming the text as written ('The quote labels \\\"Feb. 2nd, 2026\\\" as the date of service; the code could not read it'). Add 24A as an inline label, and parse the six-digit FROM/THROUGH form under FL6.\",\n   \"acceptance_test\": \"Fixtures R15, N20 and N8: no note says 'states no date' or 'not labeled'; each note quotes the labeled date as written (or N8 prints June 24 / July 8, N20 'June 9–12, 2026').\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Internal notes tell me to 'fill it from the quote' for lines whose quote has no date, and the one-date blank does not fit a multi-visit line\",\n   \"evidence\": \"ui-lib11-notes.txt:39-41 '- Fennimoor Spine Clinic, $250.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.' The quotes are 'New patient exam charge $250.00', 'x-ray charge $180.00', 'treatment visits 1 through 14 charge $2,310.00' (no date). export.py:614 uses one sentence for every reason. The $2,310.00 line covers visits 1 through 14 (March 27 to May 29 in the chronology), but the letter offers 'date of service [__________]'.\",\n   \"why_it_matters\": \"For a no-date line the only real action is to request a dated ledger, or to match the charge to the chart notes myself. 'From the quote' wastes a look. A 14-visit charge needs a range ('dates of service'), and a singular blank invites a single date that undercounts the treatment span.\",\n   \"fix\": \"Word the notes line by reason. no_date / non_service_date: 'the bill line gives no date; take it from the matching visit note or request a dated itemized bill'. Written-date reasons: 'the quote writes \\\"04/05/2026\\\"; confirm and fill'. When the quote counts visits ('visits 1 through 14', 'x 9 visits'), print 'dates of service [__________]'.\",\n   \"acceptance_test\": \"lib11 counted notes contain no 'fill it from the quote' for the three Fennimoor lines; the $2,310.00 letter line reads 'dates of service [__________]'; the synth_ambiguous_dos note keeps 'fill it from the quote' with the date as written.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from rounds 1 and 2: some charge quotes name neither the service nor the date the line prints\",\n   \"evidence\": \"ui-lib14-letter.txt 'Source [Ex. __ / Bates __]: \\\"charge $187.05.\\\"'; ui-lib10-letter.txt 'Source [Ex. __ / Bates __]: \\\"FL47 total charges $4,920.00.\\\"'. The handoff lists the quote-span minor as not done.\",\n   \"why_it_matters\": \"I cannot check the printed September 14 or June 9–12 against the quote under it without opening the record.\",\n   \"fix\": \"Quote the bill line from its code or description through the figure.\",\n   \"acceptance_test\": \"Every charge Source line in the 25-case letters contains a service word or code as well as the figure.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"A CMS-1500 claim-level 'dates of service from X to Y' prints the whole span on each coded line\",\n   \"evidence\": \"probe_r3.out N10 'CMS-1500 dates of service from 06/24/2026 to 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.' prints 'Wardlaw Orthopedics, CMS-1500, June 24–July 8, 2026' on both lines (round 2: the not-stated form).\",\n   \"why_it_matters\": \"It is what the bill states, and so not a wrong date. But a new-patient visit (99204) shown across two weeks reads oddly to an adjuster. On a real CMS-1500 the span sits per line in 24A.\",\n   \"fix\": \"Optional: on a CMS-1500 (not a UB-04 or a unit-count line), a claim-level span over several coded lines gives the blank with a note quoting the span.\",\n   \"acceptance_test\": \"N10 lines print the blank with 'claim dates of service 06/24/2026 to 07/08/2026' in the note; P10 (9 units over the period) keeps 'January 23–March 6, 2026'.\"}\n ],\n \"whats_right\": [\n  \"Round 2 blocker closed: birth, DOI, accident, onset, referral and order dates never print. Bills give the blank, and visit notes keep their own date (B8 January 16, B9 February 20)\",\n  \"The blank 'date of service [__________] (statement dated June 15, 2026)' is honest, pastes cleanly, and is listed under CHARGES WITHOUT A CERTAIN DATE OF SERVICE in the notes\",\n  \"Corpus letters (sample, case_09, lib14, lib10) unchanged and right, including lib10 'June 9–12, 2026'; Posted-first ledgers and the CMS-1500 'and' list still right\"\n ],\n \"questions_for_chris\": [\n  \"Still open from round 2, outside T-202: the export gate blocks a SYNTHETIC CMS-1500 coded line ('Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’', letters_dump_r3.out synth_cms1500_two_dates). Should this get its own card?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-03T01:33:42.849Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/draft-T-202-paralegal-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:33:48.652Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/draft-T-202-paralegal-r3.md",
 "old_string": "letter_check passes the wrong line with 0 violations, and it flags the correct January 16 → January 9 swap the other way: given the right record date, it reports a violation.",
 "new_string": "letter_check passes the wrong line with 0 violations. In the visit-note probes (R1, R2, R17, R18, R19) it goes further: it reports the correct record-date line as the violation."
}
````

### User / tool · 2026-11-03T01:33:48.765Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3/draft-T-202-paralegal-r3.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:33:49.839Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py artifacts/review-evidence/T-202-paralegal-r3/draft-T-202-paralegal-r3.md",
 "description": "Validate draft review JSON and verdict"
}
````

### User / tool · 2026-11-03T01:33:49.948Z

**tool result**
````
json blocks: 1
verdict: fail | severities: ['blocker', 'minor', 'minor', 'minor', 'nit']
verdict rule expects: fail | matches: True
model: claude-opus-5-5 | card: T-202 | persona: paralegal-reviewer
all finding fields present
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:33:51.921Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls reviews/T-202-paralegal-r3.md 2>&1; cp artifacts/review-evidence/T-202-paralegal-r3/draft-T-202-paralegal-r3.md reviews/T-202-paralegal-r3.md && python3 tools/board.py validate reviews/T-202-paralegal-r3.md",
 "description": "Publish review and run board validator"
}
````

### User / tool · 2026-11-03T01:33:52.070Z

**tool result**
````
ls: reviews/T-202-paralegal-r3.md: No such file or directory
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:33:52.896Z

Now the memory update.

### Assistant · claude-opus-5-5 · 2026-11-03T01:34:00.441Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r3-allow-list-patterns.md",
 "content": "---\nname: t202-r3-allow-list-patterns\ndescription: T-202 r3 (973b542) fail: allow-list + fillable blank fix r2, but 'next/last/previous/initial visit date' and 'seen on' in a visit note override its own date (sample ER Jan 9 prints Jan 16); letter_check enforces it\nmetadata:\n  type: project\n---\n\nReview file: reviews/T-202-paralegal-r3.md (973b542). Verdict: fail, with 1 blocker, 3 minors and 1 nit.\n\n**Fixed since r2**\n- B1-B12 non-service dates: bills give the blank, and visit notes keep their own date.\n- The not-stated wording is replaced by the D-071 addendum blank 'date of service [__________] (statement dated X)'.\n- Notes have a CHARGES WITHOUT A CERTAIN DATE OF SERVICE section.\n- Corpus letters are byte-identical to r2.\n\n**Blocker: an allow-listed label that names another visit**\n- \"visit date\" and \"seen on\" are trusted even after next/last/previous/initial. In a non-bill note, the labeled date wins over the record's date (service_date.py:43, fallback at :375).\n- The after-statement check covers bills only (:291).\n- Sample variant 'ER charges: $6,240, next visit date 01/16/2026.' prints January 16. bd72d5b printed January 9.\n- letter_check passes the wrong line and fails the right one.\n\n**Why:** an allow-list moves the risk from \"unlabeled date\" to \"labeled but for another event\". Next time, probe qualifiers before every allowed label (next/last/prior/initial/return/scheduled), and probe comma-joined clauses (a sentence break protects).\n\n**How to apply:** scripts are in artifacts/review-evidence/T-202-paralegal-r3/:\n- probe_r3.py loads the r2 PROBES lists by ast;\n- probe_r3b.py and probe_r3c.py hold the other-visit and punctuation shapes;\n- letters_dump_r3.py builds the SYNTHETIC sample variant;\n- before_t202.py runs on a bd72d5b archive.\n\nPort 7981, h.py and p01_cases.py (lib11 added).\n\nRelated: [[t202-r2-non-service-date-patterns]], [[t202-d071-service-date-patterns]].\n"
}
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:34:02.775Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-200 undated charge label]",
 "new_string": "- [T-202 r3 allow-list patterns](t202-r3-allow-list-patterns.md) — 973b542 fail: 'next/last visit date', 'seen on' override a visit note's date; probe qualifiers + commas\n- [T-200 undated charge label]"
}
````

### User / tool · 2026-11-03T01:34:02.834Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r3-allow-list-patterns.md (file state is current in your context — no need to Read it back)
````

### User / tool · 2026-11-03T01:34:02.946Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:34:05.189Z

T-202 round 3 fails with 1 blocker: when an ER note writes "ER charges: $6,240, next visit date 01/16/2026." (synthetic variant of the sample case), the letter dates the ER charge January 16 instead of the January 9 ER visit (letter_check passes it; the pre-T-202 build printed January 9) — round 2's issues and the corpus letters are fixed and the blank works in a demand letter; 3 minors and 1 nit; review at /Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r3.md.
