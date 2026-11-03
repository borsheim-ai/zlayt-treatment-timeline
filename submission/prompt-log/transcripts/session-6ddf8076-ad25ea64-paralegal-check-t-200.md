# Subagent: Paralegal check: T-200 (Paralegal check: T-200)

Source: `agent-ad25ea64cfd973366.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T23:26:11.186Z

Check T-200 in /Users/arsis/zlayt-pm-project as the senior PI paralegal, starting from a fresh context. The card is commit bd72d5b; read reviews/T-181-paralegal-r2.md (your major) and the card handoff.

Counted undated ledger lines (lib11) now print "…itemized ledger (statement dated June 15, 2026; service date not stated): $250.00". Run a `git archive bd72d5b` copy in demo mode on your own port, and stop your PID afterward. Count the lib11 lines and generate the letter.

Judge whether this wording works in a demand letter to an adjuster. Dated charge lines that print the statement date are a separate decision (D-071) on another card, so don't grade them here. Write reviews/T-200-paralegal.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:13.949Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat personas/paralegal.md | head -c 200; echo; wc -l personas/paralegal.md; cat .claude/agent-memory/paralegal-reviewer/t181-r2-patterns.md .claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md",
 "description": "Read dossier header and relevant memory files"
}
````

### User / tool · 2026-11-02T23:26:14.041Z

**tool result**
````
# Persona dossier — paralegal-reviewer

## 1. Identity
**Maria Delgado (fictional), Senior Litigation Paralegal, plaintiff personal-injury firm in Austin, Texas — 9+ years, pre-lit and litigation.
      84 personas/paralegal.md
---
name: t181-r2-patterns
description: T-181 r2 (9ab8cae) paralegal re-review: changes; both r1 majors fixed (outside-word underline, Bates rule+preview); new major = letter dates counted undated ledger charges by statement date (export.py:339, backend)
metadata:
  type: project
---

T-181 r2 review (reviews/T-181-paralegal-r2.md, commit 9ab8cae). Verdict: changes, with 1 major, 3 minors and 1 nit.

**Fixed in r2**
- The grey box now says "outside the highlighted words".
- The `[data-testid=outside-word]` underlines and the `outside-note` caption show on disputed or edited lines.
- The Bates panel has `cfg-rule` and a `cfg-preview`, and the letter matches the preview.
- No first-paint 404 in demo mode.

**Major (backend, export.py:339)**
- When the paralegal counts undated ledger charges, the BILLED CHARGES line prints the statement date in the date-of-service format: "itemized ledger, June 15, 2026: $250.00".
- Step 3 labels the same line "No date of service (statement dated ...)".
- I raised this from minor (r1) to major because the letter is the half that goes to the adjuster.

**Minors**
- The SHOULD_BE_DAMAGES direction on a payment reads "an amount that is not a bill" (review.js:82).
- The notes label the accident-date-source flag "Causation language" (export.py:357). This is pre-existing and I missed it in r1.
- AI_LINE_PREPARED says "checked by a second check" even when an edited line was not second-checked.

**Mechanics that worked**
- h.py takes the T181_PROFILE env var, so the local and demo profiles stay separate.
- One timed end-to-end script (r01_sample_e2e.py) loops by `item=` in the URL. The full sample run took 16.9 s scripted.
- The guided e2e from the archive took about 3 min: 127 passed.

**Why:** next round, check that the export line names the statement date. Check the Step 3 wording for the payment direction.
**How to apply:** reuse the scripts in artifacts/review-evidence/T-181-paralegal-r2/. Related: [[t181-guided-ui-patterns]], [[reviewer-run-pitfalls-pass4]].
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

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:15.092Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T23:26:15.100Z

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

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:16.072Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; python3 tools/board.py show T-200; git log --oneline -3 bd72d5b; git rev-parse --short HEAD; git show --stat bd72d5b | head -30",
 "description": "Show card T-200 and commit info"
}
````

### User / tool · 2026-11-02T23:26:16.264Z

**tool result**
````
---
id: "T-200"
title: "Letter: counted undated ledger lines must not print the statement date as a service date (lib11 'itemized ledger, June 15, 2026')"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T23:00:47Z"
updated_at: "2026-11-02T23:26:08Z"
claimed_by: "backend"
claimed_at: "2026-11-02T23:00:56Z"
rounds: 0
commits: ["bd72d5b"]
reviews: []
ac:
  - {"n": 1, "text": "export.py prints counted undated ledger charges with the statement date labelled as such (e.g. 'itemized ledger (statement dated June 15, 2026; service date not stated): $250.00') or groups them under the provider without a date; never a bare date that reads as a service date; golden letters and evals/letter_check updated; unit test on lib11", "done": true, "evidence": "tests/unit/test_t200_undated_charge_label.py (6 pass: lib11 both styles, no bare 'itemized ledger, <date>: $' line, ED line unchanged); python -m evals.letter_check 25 cases value 0 (sample golden unchanged, accept-all letters byte-identical for all 25 cases); git archive tree: unit 1323+1475+1429+1644 passed, guided e2e 123 passed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T23:00:56Z backend: claimed
- 2026-11-02T23:25:52Z backend: AC 1 checked: tests/unit/test_t200_undated_charge_label.py (6 pass: lib11 both styles, no bare 'itemized ledger, <date>: $' line, ED line unchanged); python -m evals.letter_check 25 cases value 0 (sample golden unchanged, accept-all letters byte-identical for all 25 cases); git archive tree: unit 1323+1475+1429+1644 passed, guided e2e 123 passed
- 2026-11-02T23:25:52Z backend: moved in_progress -> in_review
- 2026-11-02T23:26:08Z orchestrator: review dispatched: paralegal-reviewer

## Handoff
What changed: charge line in the letter (export._View.charge_when) now reads '<provider>, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00' for a charge whose own line states no date of service (store.charge_dos_stated reads the line with amounts.charge_basis, exported as dos_stated; hand-built cases without the key and dated charges unchanged). Chose the label over dropping the date: the adjuster can still match the line to the ledger page, nothing reads as a visit date, and it matches the review screen's 'No date of service (statement dated ...)'. api.md note added. | Verified: tests/unit/test_t200_undated_charge_label.py (lib11 both styles, ED line unchanged, total $6,000); evals.letter_check value 0 over 25 cases; accept-all letters byte-identical before/after for all 25 cases so sample.export.expected.txt needs no change (no golden has a counted undated line; letter_check walks accept only, not count; qa could add a count walk). Archive of tree 0c3b092: unit 5871 passed, guided e2e 123 passed. | Left: SAME BUG CLASS, not fixed (out of card scope, would change goldens): dated charge lines still print the record date, which for a ledger/invoice is the statement date. case_09 Hobbleton line is 'Statement for visit of 2026-02-02' but prints March 1; lib14 ambulance invoice run of 09/14 prints November 12; lib10 UB-04 shows statement date June 19 vs period 06/09-06/12. Fix would use charge_basis dos for dated lines; needs orchestrator decision (period-start fallback for lib10). | Surprise: record date is a statement date for every billing document, so the problem is wider than undated lines.

bd72d5b fix(backend): T-200 counted undated ledger charge prints its statement date as such, never as a service date
8f78874 fix(qa): T-187 r4 / T-198 prompt log: private terms read from deploy/.private_patterns (none in tracked code), normalized-view redaction + self-test (D-070), device names, tree scan tool
2c19817 fix(frontend): T-181 r3 phone: highlighted words scrolled into a record window sized for them, refused edit shown above the action bar, panel-list test scans only loaded scripts
bd72d5b
commit bd72d5b9a6dcf94eba56df71e612d4f240351ba5
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 17:25:41 2026 -0600

    fix(backend): T-200 counted undated ledger charge prints its statement date as such, never as a service date
    
    An itemized-ledger line counted for a missing date of service (D-064) was printed
    '<provider>, itemized ledger, June 15, 2026: $250.00', the statement date in service-date
    form. The letter line is now '<provider>, itemized ledger (statement dated June 15, 2026;
    service date not stated): $250.00'. store.charge_dos_stated reads the line (charge_basis);
    dated charges are unchanged. Unit test on lib11; api.md note.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/amounts.py                       |  1 +
 app/backend/export.py                        | 12 +++-
 app/backend/store.py                         | 23 +++++++-
 memory/contracts/api.md                      |  2 +-
 tests/unit/test_t200_undated_charge_label.py | 82 ++++++++++++++++++++++++++++
 5 files changed, 115 insertions(+), 5 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:17.895Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show bd72d5b -- app/backend/export.py app/backend/store.py app/backend/amounts.py memory/contracts/api.md; sed -n 1,200p reviews/T-181-paralegal-r2.md | head -80",
 "description": "Show code diff and prior review"
}
````

### User / tool · 2026-11-02T23:26:18.087Z

**tool result**
````
commit bd72d5b9a6dcf94eba56df71e612d4f240351ba5
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 17:25:41 2026 -0600

    fix(backend): T-200 counted undated ledger charge prints its statement date as such, never as a service date
    
    An itemized-ledger line counted for a missing date of service (D-064) was printed
    '<provider>, itemized ledger, June 15, 2026: $250.00', the statement date in service-date
    form. The letter line is now '<provider>, itemized ledger (statement dated June 15, 2026;
    service date not stated): $250.00'. store.charge_dos_stated reads the line (charge_basis);
    dated charges are unchanged. Unit test on lib11; api.md note.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/amounts.py b/app/backend/amounts.py
index 8a9967b..b33de7b 100644
--- a/app/backend/amounts.py
+++ b/app/backend/amounts.py
@@ -310,6 +310,7 @@ _BILLISH = re.compile(r"\b(?:statements?|bills?|billing|invoices?|ledgers?|accou
 _BILL_OPEN = re.compile(r"^\W{0,3}(?:patient\s+)?(?:itemi[sz]ed|statement|invoice|ledger|billing|account\s+statement)\b", re.IGNORECASE)
 _TOKEN_FILLER = frozenset("charge charges charged billed fee fees of on for the a an at to and unit units dos date service services statement rev cpt code invoiced total".split())
 _NO_DATE_WHY = "The line states no date of service, so it is not an itemized service line and is not totaled."
+NO_DATE_WHY = _NO_DATE_WHY           # T-200: the stored reason of a charge the paralegal counted because its line states no date of service
 _NO_SVC_WHY = "The line names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized service line and is not totaled."
 _NO_COL_WHY = "The figure is not under a charges column of the bill, so it is not an itemized service line and is not totaled."
 _SECOND_WHY = ("A second amount on a service line is not the line's own charge (it can be a deductible, what the patient owes, a denied or paid amount, an adjustment, "
diff --git a/app/backend/export.py b/app/backend/export.py
index 499636c..5c469d8 100644
--- a/app/backend/export.py
+++ b/app/backend/export.py
@@ -206,6 +206,16 @@ class _View:
     def rec_date(self, n):
         return (self.records.get(n) or {}).get("date_iso")
 
+    def charge_when(self, a):
+        """T-200 (GATE-M2 r2 paralegal major): the label before a charge's amount in the letter. A bare date there reads as the date of service. A charge whose own line states
+        none (`dos_stated` False, store.charge_dos_stated) is NEVER given the record's date bare: that date is the statement's, and the label says so and says the service date is
+        not stated: 'Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated)'. Chosen over dropping the date because the adjuster can still
+        match the line to the ledger page, and it agrees with the review screen's 'No date of service (statement dated ...)'. A case dict without the key keeps the record's date."""
+        n, src, rd = a["record_no"], self.source(a["record_no"]), self.rec_date(a["record_no"])
+        if a.get("dos_stated", True):
+            return f"{src}, {_long_date(rd)}"
+        return f"{src} (statement dated {_long_date(rd)}; service date not stated)" if rd else f"{src} (service date not stated)"
+
     def cite(self, n):
         return f"record {n} ({self.source(n)}, {_long_date(self.rec_date(n))})"
 
@@ -336,7 +346,7 @@ def _letter(v, style=None):
         out += [CHARGES_TITLE, ""]
         for a in charges:
             n = a["record_no"]
-            out += [f"{v.source(n)}, {_long_date(v.rec_date(n))}: {_money(a['cents'])}",
+            out += [f"{v.charge_when(a)}: {_money(a['cents'])}",
                     f'{v.source_prefix(n)}"{_amount_quote(v, a)}"']
         out += ["", TOTAL_PREFIX + _money(sum(a["cents"] for a in charges))]
     while out and out[-1] == "":
diff --git a/app/backend/store.py b/app/backend/store.py
index 09960e3..f8bf23e 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -115,6 +115,16 @@ def amount_pos(item: dict, rec):
     return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None
 
 
+def charge_dos_stated(item: dict, rec, pos) -> bool:
+    """T-200: does the charge's OWN line state a date of service (or, for a note, is the record the encounter)? False for a ledger line with none: the record's date is then the
+    statement's, which the letter must not print as if it were a service date. A charge the paralegal counted for a missing date of service (D-064) is False by definition.
+    Code only: amounts.charge_basis reads the line. When the line cannot be read it is True unless she counted it for that reason (the letter then keeps the record's date as before)."""
+    from app.backend import amounts as AM          # lazy: keep the import graph as it was
+    if rec is None or pos is None or not item.get("excerpt"):
+        return ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") != AM.NO_DATE_WHY
+    return AM.charge_basis(item["excerpt"], {"start": pos, "cents": item.get("value_cents")}, rec.get("source"), rec.get("date_iso")).get("dos") is not None
+
+
 def export_case(conn, case_id: str, blockers: bool = True) -> dict:
     """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
     case = DB.get_case(conn, case_id)
@@ -151,9 +161,16 @@ def export_case(conn, case_id: str, blockers: bool = True) -> dict:
         if lad.get("translation"):          # D-042: the summary of a Spanish record is a translation; the letter says so
             d["translation_label"] = spanish.translation_info("es", "summary" in ed or bool(lad["translation"].get("human_written")), prep)["label"]
         ents.append(d)
-    amts = [dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
-                 excerpt=a["excerpt"], review_status=a["review_status"], pos=amount_pos(a, rec_of.get((a["record_ids"] or [None])[0])))
-            for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
+    amts = []
+    for a in DB.list_items(conn, case_id, "amount"):
+        if a["state"] == "rejected":
+            continue
+        r = rec_of.get((a["record_ids"] or [None])[0])
+        d = dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
+                 excerpt=a["excerpt"], review_status=a["review_status"], pos=amount_pos(a, r))
+        if a["kind"] == "charge":
+            d["dos_stated"] = charge_dos_stated(a, r, d["pos"])
+        amts.append(d)
     fl = []
     for f in DB.list_items(conn, case_id, "flag"):
         if f["state"] == "rejected":        # D-053/D-057: every tray flag (judge-rejected, not word for word, rule-filtered) is not an item to review, count or export; its quote may not be in the record
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 05a27aa..0b77163 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -571,7 +571,7 @@ Built by code from items with `review_status` in (`accepted`, `edited`) only (AD
   "warnings": []
 }
 ```
-Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges accepted from these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte; **no dollar amount appears in `letter_text` outside the BILLED CHARGES section (T-139)**: an entry whose summary or quote states an amount is never written into the treatment section, whatever its review status (see "Dollar amounts in entries"), a charge's `Source` line quotes only the clause that holds its own figure when the sentence also states another one (a rate, a balance, another line item), and a dismissed charge is never listed under BILLS TO REQUEST. Rates, estimates, unclear and dismissed amounts appear only in `internal_notes_text`.
+Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges accepted from these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte; **no dollar amount appears in `letter_text` outside the BILLED CHARGES section (T-139)**: an entry whose summary or quote states an amount is never written into the treatment section, whatever its review status (see "Dollar amounts in entries"), a charge's `Source` line quotes only the clause that holds its own figure when the sentence also states another one (a rate, a balance, another line item), and a dismissed charge is never listed under BILLS TO REQUEST. Rates, estimates, unclear and dismissed amounts appear only in `internal_notes_text`. **T-200 (undated charge line):** a charge line's date is a date of service. A counted charge whose own line states none (a ledger line counted through D-064 "Count this charge") is never given the record's date bare, because that date is the statement's: the line reads `<provider>, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00` (`(service date not stated)` when the record has no date either). The export case dict carries `dos_stated` on each charge (`store.charge_dos_stated`, code reading the line with `amounts.charge_basis`); a hand-built case without the key keeps the old `<provider>, <record date>` line. Dated charges are unchanged.
 
 ## GET /api/cases/{token}/audit
 JSON for this case only. **Public/demo (default): metadata only**: no prompt, response, record or edit text. With `ZLAYT_MODE=local` the same call also returns the full prompts and responses and the before/after of each human event (T-040, T-051 privacy check).
# T-181 guided 4-step UI, round 2 (9ab8cae): paralegal re-review (Maria Delgado, senior PI paralegal)

**Verdict: changes** (0 blockers, 1 major, 3 minors, 1 nit).

**Scope.** `git archive 9ab8cae` was extracted to the session scratchpad and run with the fixture backend (curated set, no live calls):
- Public demo mode (ZLAYT_MODE unset): port 7941, listener PID 14948.
- Local copy for the lib11 library case: port 7942, PID 15071.
- I stopped both by PID afterwards. `lsof` returned 1 on both ports and `curl` returned 000.

**Deterministic check first.** From the archive, `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_no_console_errors.py` gave `127 passed in 173.39s` (pytest-guided.out).

## Both round-1 majors are fixed

1. **Disputed-line label: fixed.**
   - The grey box now reads "Also in this record, outside the highlighted words:" (step2.js:66).
   - Disputed lines underline the words that are not in the quote, with the caption "Underlined words are not in the highlighted words."
   - lib11 e1 underlines `Annual`, `visit`. e2 underlines `Patient`, `after`, `passenger`, `vehicle`, `struck`, `from`, `behind`. e4 underlines `Law`, `letter`, `protection`, `Fennimoor`, `Spine`, `Clinic`, `states`, `clinic` (r03.out, lib-s2-00-e1.png, lib-s2-05-e2.png, lib-s2-08-e4.png).
   - This is exactly what I need in order to tick the compare box honestly.
2. **Bates fill-in wording: fixed.**
   - The panel now says "One Bates number per record, not per page. ... Use this only if each of your records is one Bates page in that order." It also tells me to leave the fields blank and fill the cites in Word otherwise.
   - A live preview showed "record 1 reads [Ex. 3 / Bates RIVERA0101], record 2 reads [Ex. 3 / Bates RIVERA0102], and record 9 reads [Ex. 3 / Bates RIVERA0109]". The saved letter matched it exactly (0101 to 0109; the ER charge is 0102 and the MRI charge is 0108).
   - The numbers survived a reload, and clearing the fields restored `[Ex. __ / Bates __]` (r02.out, 08-bates-typed-preview.png, 09-bates-saved.png).

## Sample case end to end, timed

From Home, "Open the sample case" to the downloaded letter took **16.9 s scripted**: 33 key presses and 6 clicks, with drafting at 1.3 s (r01.out, r01_counts.json). At a human reading pace I still estimate 8 to 10 minutes.

Every Appendix A truth held:
- 9 lines, with EMS and ER both on January 9.
- The 73-day gap is flagged and the 28-day interval is not.
- The 01-09 vs 01-19 conflict shows all three highlights on screen. The multi-record window fix works (s2-01-...png).
- 12 planned PT visits vs discharge at visit 9.
- Both prior-condition mentions are flagged.
- The total is $6,240 + $2,150 = $8,390.00.
- The $185 rate goes to the notes only. Lost work is listed under DAMAGES MENTIONS.

My edits and decisions held:
- My record-3 edit is in the letter, and the original wording is under EDITED ITEMS.
- The dismissed flag appears only under FLAGS DISMISSED.
- A reload mid-review kept my place.
- The copied letter matched the downloaded letter.
- No console or HTTP errors in any run (the first-paint 404 is gone).

## The undated-ledger letter line: yes, it is a problem for a demand letter (major)

On lib11 I counted the three ledger lines after ticking "I checked this is a separate charge". The letter's BILLED CHARGES section then reads:
- `Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00`
- `Source ...: "New patient exam charge $250.00"`

The ledger line for $180 and the line for $2,310 follow the same pattern (lib11-letter.txt:39-44).

June 15 is the *statement date*: the record says "statement date 06/15/2026". In the same section, `Wexcombe Memorial ED, March 18, 2026: $3,260.00` uses a date of service, so any reader takes June 15 as the date of service. The chronology above it puts the new-patient visit on March 27, 2026 (lib11-letter.txt:19).

The adjuster will say the exam was billed on a day with no treatment record, after the last visit on May 29. That is checklist item 1: a line dated by something other than the date of service. Step 3 now shows the right label ("No date of service (statement dated June 15, 2026)", r03.out:406-408), so the screen and the letter disagree.

It is backend text (app/backend/export.py:339). I am grading it on the letter this UI produces. I rated it minor in round 1, when it was bundled with the Step 3 table. On its own, the letter line is the half that goes to the adjuster, so it is major. The sample letter is not affected.

## Round-1 minors

These are fixed:
- The e9 refusal now points to Step 3.
- A on a refused line leaves focus off "No".
- lib11 provenance now follows the case ("Demo: recorded AI answers" with "AI draft" cards).
- The Step 3 table shows the statement date correctly.
- Step 3 disputes now name a direction.

I did not re-exercise the public `/new` "our test cases" copy.

```json
{"card": "T-181", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "git archive 9ab8cae (T-181 r2 fix) extracted to the session scratchpad; fixture backend, FIXTURE_SET=curated. Public demo mode (ZLAYT_MODE unset) at http://127.0.0.1:7941 (listener PID 14948); local copy (ZLAYT_MODE=local) at http://127.0.0.1:7942 (PID 15071) for library case lib11, since /api/library is local-only. Both stopped by PID; lsof exit 1 and curl 000 on both ports. Sample case: evals/golden/sample.txt via 'Open the sample case'. Library: case_lib11_priors_and_ledger. Viewport 1440x900. Evidence dir artifacts/review-evidence/T-181-paralegal-r2/.",
 "exercised": [
  "Read personas/paralegal.md, reviews/T-181-paralegal.md (round 1), the T-181 card notes and handoff, git diff 26287b9 9ab8cae for step2.js, step4.js and export.py",
  "From the archive: E2E_REQUIRE_DB=1 pytest -q tests/e2e/guided tests/e2e/test_no_console_errors.py: '127 passed in 173.39s' (pytest-guided.out)",
  "Sample case, timed, one Playwright run (r01_sample_e2e.py, r01.out): Home > Open the sample case > Draft the timeline (1.3 s) > all 19 Step 2 items with each card, highlight and outside-word list logged > E on record 3, retyped the line, Tab to Save, A focused the compare box, Space, A > reload after e5 > E on the gap flag with a note > D on the accident-date-source flag > Step 3: A on the 4 amounts (total chip $6,240.00 then $8,390.00) > Step 4 > Download letter at 16.9 s; Download notes; Copy letter (clipboard equals download)",
  "Read letter-download.txt and notes-download.txt against Appendix A truths",
  "Step 4 Bates panel (r02_bates.py, r02.out): read the panel text blank; typed Exhibit 3, prefix RIVERA, first number 101 and read the live preview after each; saved; compared letter cites to the preview; reloaded; cleared and saved (letter back to [Ex. __ / Bates __])",
  "lib11 on the local copy (r03_lib11.py, r03.out): picked the test case, Read, Draft (2.6 s); all 21 Step 2 items with outside-word lists and grey-box text; compare confirm on e1, e2 and e4; A then D on the refused ledger line e9 (focus stayed on card-foot); Step 3 all 8 amounts, ticking 'separate charge' and compare on the three ledger lines; Step 4 letter and notes downloaded (lib11-letter.txt, lib11-notes.txt)",
  "Read evals/library/case_lib11_priors_and_ledger.txt record 9 and app/backend/export.py:339 in the archive"
 ],
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:21.752Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls artifacts/review-evidence/T-181-paralegal-r2/; ls artifacts/review-evidence/ | grep -i -E \"serve|T-181\" | head; cat .claude/agent-memory/paralegal-reviewer/gate-m2-r2-patterns.md .claude/agent-memory/paralegal-reviewer/t181-guided-ui-patterns.md | head -60",
 "description": "List prior evidence scripts and memory"
}
````

### User / tool · 2026-11-02T23:26:21.848Z

**tool result**
````
01-home.png
02-step1.png
03-after-draft.png
04-step2-done.png
05-step3-done.png
06-step4.png
07-bates-blank.png
08-bates-typed-preview.png
09-bates-saved.png
draft-T-181-paralegal-r2.md
h.py
letter-clipboard.txt
letter-download.txt
letter-with-bates.txt
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
lib-step4.png
lib11-letter.txt
lib11-notes.txt
notes-download.txt
profile
profile-local
pytest-guided.out
r01.out
r01_counts.json
r01_sample_e2e.py
r02.out
r02_bates.py
r03.out
r03_lib11.py
run.log
s2-00-e1.png
s2-01-f_accident_date_after_treatment_1_2_7.png
s2-02-e2.png
s2-03-e3.png
s2-04-f_r3_1.png
s2-05-e4.png
s2-06-f_cx1.png
s2-07-e5.png
s2-08-e6.png
s2-09-f_gap_r6_r7.png
s2-10-f_r6_1.png
s2-11-e7.png
s2-12-f_r7_1.png
s2-13-f_r7_2.png
s2-14-e8.png
s2-15-f_r8_1.png
s2-16-f_r8_2.png
s2-17-e9.png
s2-18-f_r9_1.png
s2-99-e3.png
s2-after-reload.png
s2-e3-edited-compare.png
s2-e3-ticked.png
s2-gap-after-note.png
s3-00-a1.png
s3-01-a4.png
s3-02-a2.png
s3-03-a3.png
T-049-served-index.html
T-060-paralegal-pass4-serve.py
T-120-r2-paralegal-server.log
T-181-paralegal
T-181-paralegal-r2
T-181-ux
T-181-ux-download.py
T-181-ux-edit-undo.py
T-181-ux-explore.py
T-181-ux-keyboard.py
---
name: gate-m2-r2-patterns
description: GATE-M2 r2 (7cfdb0b) paralegal: lib11 total/conflict fixed; unclear ledger rows show the wrong reason and have no reclassify control; Start review strands items; selectors for the overview build
metadata:
  type: project
---

- r2 verdict changes (1 major, 4 minor). Fixed since r1: lib11 total $3,260 (D-060 default-deny: undated ledger lines are unclear), intake "No [X]" vs PCP prior accidents is a conflict flag, bills-to-request no longer names the law firm.
- Open: UI unclear rows say "can't tell if this is a bill. unclear; not a bill" for every ledger line (judge-disagreement boilerplate); per-line reason only in export notes; no frontend control for the reclassify route; expected.json says $6,000 is reached by reclassifying.
- Start review lands on the do-first item (sample: a2 at the end of the list); a/j go forward only, so a-only ends 2 of 23. Clicking Start review again lands on the next needs-review item.
- Selectors (7cfdb0b): library cases sit under `summary:has-text('Add a synthetic case')` after `btn-new-case`; entry rows `[data-testid=entry-N]`, edit textarea must be scoped `[data-testid=entry-N] [data-testid=edit-summary]` (9 in DOM); amount rows `[data-testid='amount-$250.00']`; counter `progress-text`; checks `checks-card`; `d` on a flag/entry dismisses with no confirm; `a` on an edited row focuses `btn-accept` ("I compared it with the quote"), Enter accepts.
- Scratchpad is shared across sessions: a reused DB filename showed old cases; use a new subfolder DB.
- Edit with identical text still counts as "Edited" (no-op edit shows Original = same text).

**How to apply:** on r3 check unclear-row reason text, a reclassify control, Start review path (t1/t2 scripts), and that judge-questioned entries still accept on one key. Related: [[t118-lib11-truth-patterns]], [[t149-r2-overview-patterns]], [[reviewer-run-pitfalls-pass4]].
---
name: t181-guided-ui-patterns
description: T-181 guided 4-step UI (26287b9) paralegal review: changes (2 majors: disputed-item grey box says borrowed sentence "not in any line"; Bates helper one-number-per-record unstated); selectors, demo vs local library, keyboard traps
metadata:
  type: project
---

T-181 review (reviews/T-181-paralegal.md, commit 26287b9). Verdict: changes, with 2 majors, 7 minors and 2 nits. Sample truths are all correct. verify_quickly is 4.

**Majors**
- On lib11 e1, e2 and e4 (JUDGE_PARTIAL), the line borrows a sentence from outside the quote. The grey box (step2.js:66) lists that same sentence under "Also in this record, not in any line". The dispute text never says which words.
- The Bates helper (step4.js:148) numbers first number + record number - 1 (api.md:115) and does not say so on screen.

**Minors to re-check next round**
- e9 refusal says "none of them is in Billed charges", but Step 3 can count the ledger lines.
- A on a refused item moves focus to answer-no, so A then Space dismisses.
- lib11 title row says "not written by an AI model" while the cards say "AI draft" (review.js:45 uses health).
- Undated ledger lines show the statement date under "Date".
- The Step 3 dispute line has no direction.
- The conflict record-7 highlight is below the fold.
- Public /new promises "our test cases".

**Mechanics**
- Public demo mode (ZLAYT_MODE unset):
  - GET /api/cases 404 is by design (it causes a console error on every page).
  - The home list is localStorage, so use a Playwright persistent profile (launch_persistent_context) to keep cases between runs.
  - /api/library is local-only. Run a second ZLAYT_MODE=local copy for library cases.
- Selectors:
  - Home and new case: `btn-continue` is an A, not a button; `case-card[data-title=...]`, `btn-new-case`, `tile-library`, `library-<id>`, `btn-read`, `btn-draft`.
  - Review frame: `answer-yes`/`answer-no`/`btn-third`/`btn-later`/`btn-back`; `check-compare`, `check-separate`; `edit-summary`, `edit-note`.
  - Step 4: `letter-text`, `notes-text`, `btn-download-letter`/`btn-download-notes`/`btn-copy-letter`, `cfg-exhibit`/`cfg-bates-prefix`/`cfg-bates-start`/`btn-save-cfg`; `step-1..4`.
  - Page regions: `.titlebar`, `.work .card`, `.actions`.
- Keys: A, D and E are document-level and work after a reload with focus on BODY. There is no save shortcut in a textarea, so Tab to Save and press Enter. On a disabled Yes, A focuses the unticked checkbox; Space ticks it; A accepts.
- The guided e2e suite runs from the archive: E2E_REQUIRE_DB=1 pytest tests/e2e/guided gave 100 passed in about 2.5 min.
- board-guard reads `->` inside a grep pattern as a redirect. Avoid ">" in patterns.
- Don't put a URL in a screenshot file name: it creates `http:` directories.

**Why:** these took a full run to learn. Next round, check the two majors first.
**How to apply:** reuse artifacts/review-evidence/T-181-paralegal/h.py (T181_BASE env var) and the s05, s13 and s14 scripts. Related: [[gate-m3-patterns]], [[reviewer-run-pitfalls-pass4]], [[feedback_reviewer_tooling_quirks]].
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:24.444Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-181-paralegal-r2; cat h.py; echo ======; cat r03_lib11.py; echo =====; head -5 run.log; cat ../T-060-paralegal-pass4-serve.py",
 "description": "Read prior helper and lib11 scripts"
}
````

### User / tool · 2026-11-02T23:26:24.550Z

**tool result**
````
"""T-181 paralegal review helper: persistent Chromium profile on the archive app (9ab8cae r2, demo mode, port 7941).

Usage: .venv/bin/python -I artifacts/review-evidence/T-181-paralegal/h.py <step-script.py>
The step script gets `pg` (page), `shot(name)`, `dump(label)`, `log(...)`, `BASE`, `OUT` in its globals.
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7941")
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
======
"""T-181 r2: lib11 (priors and ledger) on the local-mode copy. Step 2 disputed lines (grey box label, underlined outside words),
Step 3 ledger lines (dispute direction, date column), Step 4 letter lines for the counted undated ledger amounts.
Run: T181_BASE=http://127.0.0.1:7942 T181_PROFILE=profile-local .venv/bin/python -I .../h.py .../r03_lib11.py
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
dump("lib11 step 3 done")
shot("lib-step3-done", full=True)

pg.get_by_text("Go to step 4").first.click()
pg.wait_for_selector("[data-testid=letter-text]", timeout=15000)
pg.wait_for_timeout(600)
with pg.expect_download() as d:
    pg.click("[data-testid=btn-download-letter]")
d.value.save_as(OUT + "/lib11-letter.txt")
with pg.expect_download() as d2:
    pg.click("[data-testid=btn-download-notes]")
d2.value.save_as(OUT + "/lib11-notes.txt")
shot("lib-step4", full=True)
log("lib11 done in", round(time.time() - T0, 1), "s")
=====
### run r01_sample_e2e.py at 16:53:14
===== home first visit url=http://127.0.0.1:7941/
Skip to the main content
Synthetic data only — never paste real records
TT
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

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:28.211Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t200; git archive bd72d5b | (mkdir -p $D && tar -x -C $D); ls $D | head -30; git rev-parse --short HEAD",
 "description": "Extract bd72d5b archive into scratchpad"
}
````

### User / tool · 2026-11-02T23:26:29.241Z

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
bd72d5b
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:32.414Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t200; grep -n \"library\" app/backend/*.py | grep -i -E \"local|mode|demo|public\" | head -20; grep -n -i \"ZLAYT_MODE\\|def is_local\\|DEMO\" app/config.py | head -20",
 "description": "Check whether library is available in demo mode"
}
````

### User / tool · 2026-11-02T23:26:32.520Z

**tool result**
````
app/backend/api.py:105:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
23:        warnings.append("ENABLE_LIVE=1 but there is nothing to call (no ANTHROPIC_API_KEY, backend is not claude-cli): serving demo mode.")
29:        "mode": "live" if live else "demo",
35:        "local_mode": os.environ.get("ZLAYT_MODE") == "local",
48:                "use LLM_BACKEND=anthropic-api, or unset ENABLE_LIVE for demo mode.")
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:35.667Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t200; sed -n 1,60p app/config.py; sed -n 90,130p app/backend/api.py; grep -n \"library\" app/backend/api.py | head -20",
 "description": "Read config and API library gating"
}
````

### User / tool · 2026-11-02T23:26:35.763Z

**tool result**
````
"""Runtime configuration, read-only. One place that says which mode the process is in and why; never returns or prints a secret.

`python -m app.config` prints the resolved settings (a key is reported only as set / not set). The Dockerfile, run.sh and the Makefile
use it as a startup self-check. The rules themselves live where they are enforced (app.llm.provider.backend_name, app.backend.store.live_enabled);
this module calls those so there is one definition of "live".
"""
import importlib.util
import json
import os
import socket

DEFAULTS = {"HOST": "127.0.0.1", "PORT": "7860", "LLM_BACKEND": "fixture", "FIXTURE_SET": "curated"}


def resolved() -> dict:
    from app.backend import store
    from app.llm import provider
    live = store.live_enabled()
    key_set = bool(os.environ.get("ANTHROPIC_API_KEY"))
    backend = provider.backend_name()
    warnings = []
    if os.environ.get("ENABLE_LIVE") == "1" and not live:
        warnings.append("ENABLE_LIVE=1 but there is nothing to call (no ANTHROPIC_API_KEY, backend is not claude-cli): serving demo mode.")
    if os.environ.get("LLM_BACKEND") not in (None, "", "fixture") and os.environ.get("ENABLE_LIVE") != "1":
        warnings.append("LLM_BACKEND is set but ENABLE_LIVE is not 1: the fixture backend is used (no model call is possible).")
    if live and backend == "anthropic-api" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        warnings.append("Live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a spend limit at the provider first); the server will refuse to start.")
    return {
        "mode": "live" if live else "demo",
        "backend": backend,
        "fixture_set": os.environ.get("FIXTURE_SET", DEFAULTS["FIXTURE_SET"]) if backend == "fixture" else None,
        "host": os.environ.get("HOST", DEFAULTS["HOST"]),
        "port": int(os.environ.get("PORT", DEFAULTS["PORT"])),
        "anthropic_api_key": "set" if key_set else "not set",
        "local_mode": os.environ.get("ZLAYT_MODE") == "local",
        "warnings": warnings,
    }


def preflight() -> str | None:
    """One-line reason the server cannot start in the configured mode, or None. Called by app.main before create_app so a misconfigured
    live opt-in prints one line naming the variable instead of a traceback. The cap/host rules themselves stay in create_app (it still raises)."""
    from app.llm import provider
    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
        return "live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)"
    if provider.backend_name() == "claude-cli" and importlib.util.find_spec("app.llm.backends.claude_cli") is None:
        return ("LLM_BACKEND=claude-cli is not available in this build (the Docker image does not ship the CLI backend, CONTRACT section 10): "
                "use LLM_BACKEND=anthropic-api, or unset ENABLE_LIVE for demo mode.")
    return None


def port_in_use(host: str, port: int) -> bool:
    """True when something is already listening on host:port (same SO_REUSEADDR setting uvicorn binds with)."""
    with socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            s.bind((host, port))
        except OSError:
            return True
    return False
    try:
        ip = ipaddress.ip_address(host)
    except (TypeError, ValueError):
        return False
    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback


def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.db_path = db_path
    app.state.recorded = recorded_hashes()

    def allowed_hashes():
        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
    runs = {}
    rejudging = set()
    _boot = DB.connect(db_path)
    try:
        store.interrupt_orphaned_runs(_boot)        # T-178: a run a stopped process left "running" becomes failed (run again allowed); its accepted items are untouched
    finally:
        _boot.close()
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
        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available

    def demo_mode():
        return not live_enabled()

    def answers():
35:LIBRARY = ROOT / "evals" / "library"
66:def library_cases() -> list:
67:    """Synthetic case library (evals/library, same file format as evals/golden: <id>.txt + optional <id>.expected.json). Falls back to
68:    evals/golden until the library exists. [{id, name, description, path}]"""
105:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
280:    @app.get("/api/library")
281:    def library():
284:        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}
291:        if isinstance(b.get("library"), str):
294:            lib = next((x for x in library_cases() if x["id"] == b["library"]), None)
296:                raise ApiError(404, "not_found", "No such library case.")
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:38.649Z

**tool call — Bash**
````
{
 "command": "lsof -iTCP:7963 -sTCP:LISTEN -nP; echo exit=$?",
 "description": "Check port 7963 is free"
}
````

### User / tool · 2026-11-02T23:26:38.801Z

**tool result**
````
exit=1
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:43.642Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; mkdir -p artifacts/review-evidence/T-200-paralegal; env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/db/t200.sqlite PORT=7963 HOST=127.0.0.1 .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t200 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/server.log 2>&1",
 "description": "Start archive app on port 7963 in demo fixture mode",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T23:26:43.713Z

**tool result**
````
Command running in background with ID: b0iu55934. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b0iu55934.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:46.160Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; for i in 1 2 3 4 5 6 7 8 9 10; do c=$(curl -s -o /dev/null -w \"%{http_code}\" http://127.0.0.1:7963/api/health); [ \"$c\" = 200 ] && break; python3 -c \"import time; time.sleep(1)\"; done; echo $c; curl -s http://127.0.0.1:7963/api/health; echo; lsof -iTCP:7963 -sTCP:LISTEN -nP; cat artifacts/review-evidence/T-200-paralegal/server.log | head",
 "description": "Wait for server and check health and PID"
}
````

### User / tool · 2026-11-02T23:26:46.354Z

**tool result**
````
200
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  66842 arsis    9u  IPv4 0xf1ed01fb8eea2f0b      0t0  TCP 127.0.0.1:7963 (LISTEN)
Serving on http://127.0.0.1:7963  (Ctrl-C to stop)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:49.653Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; sed -n 30,50p artifacts/review-evidence/T-181-paralegal-r2/lib11-letter.txt; grep -n -i \"ledger\\|statement\\|06/15\\|\\\\$\" evals/library/case_lib11_priors_and_ledger.txt | head -30",
 "description": "Read prior lib11 letter and record 9 ledger text"
}
````

### User / tool · 2026-11-02T23:26:49.740Z

**tool result**
````
May 29, 2026 — Fennimoor Spine Clinic, visit 14
Neck pain 4/10, low back pain 5/10. Care continues.
Source [Ex. __ / Bates __]: "Neck pain 4/10, low back pain 5/10. Care continues."

BILLED CHARGES

Wexcombe Memorial ED, March 18, 2026: $3,260.00
Source [Ex. __ / Bates __]: "ED charge: $3,260."
Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $250.00
Source [Ex. __ / Bates __]: "New patient exam charge $250.00"
Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $180.00
Source [Ex. __ / Bates __]: "x-ray charge $180.00"
Fennimoor Spine Clinic, itemized ledger, June 15, 2026: $2,310.00
Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"

Billed charges accepted from these records: $6,000.0016:Excerpt: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture. ED charge: $3,260."
21:Excerpt: "Letter of protection to Fennimoor Spine Clinic. This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending. Please send complete records and an itemized statement."
45:Source: Fennimoor Spine Clinic, itemized ledger
46:Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection."
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:50.748Z

Now write the probe script (reusing the r2 helper with a new base/profile).

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:52.249Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence; cp T-181-paralegal-r2/h.py T-200-paralegal/h.py; cp T-181-paralegal-r2/r03_lib11.py T-200-paralegal/p01_lib11.py; grep -n \"7941\\|run.log\\|profile\" T-200-paralegal/h.py",
 "description": "Copy helper and lib11 probe into T-200 evidence dir"
}
````

### User / tool · 2026-11-02T23:26:52.408Z

**tool result**
````
1:"""T-181 paralegal review helper: persistent Chromium profile on the archive app (9ab8cae r2, demo mode, port 7941).
11:BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7941")
13:PROFILE = os.path.join(OUT, os.environ.get("T181_PROFILE", "profile"))
14:LOG = os.path.join(OUT, "run.log")
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:52.900Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/h.py",
 "limit": 15
}
````

### User / tool · 2026-11-02T23:26:52.907Z

**tool result**
````
1	"""T-181 paralegal review helper: persistent Chromium profile on the archive app (9ab8cae r2, demo mode, port 7941).
2	
3	Usage: .venv/bin/python -I artifacts/review-evidence/T-181-paralegal/h.py <step-script.py>
4	The step script gets `pg` (page), `shot(name)`, `dump(label)`, `log(...)`, `BASE`, `OUT` in its globals.
5	"""
6	import os
7	import sys
8	import time
9	from playwright.sync_api import sync_playwright
10	
11	BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7941")
12	OUT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
13	PROFILE = os.path.join(OUT, os.environ.get("T181_PROFILE", "profile"))
14	LOG = os.path.join(OUT, "run.log")
15	
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:57.011Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/h.py",
 "old_string": "\"\"\"T-181 paralegal review helper: persistent Chromium profile on the archive app (9ab8cae r2, demo mode, port 7941).\n\nUsage: .venv/bin/python -I artifacts/review-evidence/T-181-paralegal/h.py <step-script.py>\nThe step script gets `pg` (page), `shot(name)`, `dump(label)`, `log(...)`, `BASE`, `OUT` in its globals.\n\"\"\"\nimport os\nimport sys\nimport time\nfrom playwright.sync_api import sync_playwright\n\nBASE = os.environ.get(\"T181_BASE\", \"http://127.0.0.1:7941\")",
 "new_string": "\"\"\"T-200 paralegal review helper (copied from T-181 r2): persistent Chromium profile on the archive app (bd72d5b, demo/fixture, local mode, port 7963).\n\nUsage: .venv/bin/python -I artifacts/review-evidence/T-200-paralegal/h.py <step-script.py>\nThe step script gets `pg` (page), `shot(name)`, `dump(label)`, `log(...)`, `BASE`, `OUT` in its globals.\n\"\"\"\nimport os\nimport sys\nimport time\nfrom playwright.sync_api import sync_playwright\n\nBASE = os.environ.get(\"T181_BASE\", \"http://127.0.0.1:7963\")"
}
````

### User / tool · 2026-11-02T23:26:57.107Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/h.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:26:57.992Z

Now update the probe header and the output filenames, and also capture the in-app letter/notes text.

### Assistant · claude-opus-5-5 · 2026-11-02T23:27:01.272Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/p01_lib11.py",
 "old_string": "\"\"\"T-181 r2: lib11 (priors and ledger) on the local-mode copy. Step 2 disputed lines (grey box label, underlined outside words),\nStep 3 ledger lines (dispute direction, date column), Step 4 letter lines for the counted undated ledger amounts.\nRun: T181_BASE=http://127.0.0.1:7942 T181_PROFILE=profile-local .venv/bin/python -I .../h.py .../r03_lib11.py\n\"\"\"",
 "new_string": "\"\"\"T-200 (copied from T-181 r2 r03_lib11.py): lib11 (priors and ledger) on the bd72d5b archive, demo/fixture backend, local mode, port 7963.\nAccept Step 2; in Step 3 count the three undated ledger lines (tick 'separate charge' + compare); Step 4 letter and notes.\nRun: .venv/bin/python -I artifacts/review-evidence/T-200-paralegal/h.py artifacts/review-evidence/T-200-paralegal/p01_lib11.py\n\"\"\""
}
````

### User / tool · 2026-11-02T23:27:01.383Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/p01_lib11.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:27:04.180Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/p01_lib11.py",
 "old_string": "d.value.save_as(OUT + \"/lib11-letter.txt\")\nwith pg.expect_download() as d2:\n    pg.click(\"[data-testid=btn-download-notes]\")\nd2.value.save_as(OUT + \"/lib11-notes.txt\")",
 "new_string": "d.value.save_as(OUT + \"/lib11-letter.txt\")\nwith pg.expect_download() as d2:\n    pg.click(\"[data-testid=btn-download-notes]\")\nd2.value.save_as(OUT + \"/lib11-notes.txt\")\nopen(OUT + \"/lib11-letter-onscreen.txt\", \"w\").write(pg.inner_text(\"[data-testid=letter-text]\"))\npg.click(\"[data-testid=step-3]\")\npg.wait_for_selector(\"[data-testid=view][data-ready]\")\npg.wait_for_timeout(600)\ndump(\"step 3 revisited after export\")\nshot(\"lib-step3-revisit\", full=True)"
}
````

### User / tool · 2026-11-02T23:27:04.321Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/p01_lib11.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:27:06.857Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-200-paralegal/h.py artifacts/review-evidence/T-200-paralegal/p01_lib11.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/p01.out 2>&1; echo exit=$?; tail -5 artifacts/review-evidence/T-200-paralegal/p01.out; grep -n \"ERRORS\\|draft took\\|lib11 done\" artifacts/review-evidence/T-200-paralegal/p01.out",
 "description": "Run lib11 Playwright probe",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T23:27:33.531Z

**tool result**
````
exit=0
Demo: recorded AI answers. These are real AI answers recorded earlier; nothing new is sent to an AI.
=====
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/lib-step3-revisit.png
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/lib-step4.png
lib11 done in 26.2 s
67:draft took 2.6 s
483:lib11 done in 26.2 s
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:27:36.120Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal; cat -n lib11-letter.txt; echo ====; diff lib11-letter.txt lib11-letter-onscreen.txt && echo SAME_ONSCREEN; echo ====; cat -n lib11-notes.txt",
 "description": "Read the lib11 letter and notes"
}
````

### User / tool · 2026-11-02T23:27:36.243Z

**tool result**
````
     1	TREATMENT CHRONOLOGY
     2	
     3	March 4, 2026 — Dr. Hesper Alderton, primary care
     4	Annual visit; history per patient of car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.
     5	Source [Ex. __ / Bates __]: "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
     6	
     7	March 18, 2026 — Ashgrove Fire-Rescue run report
     8	Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ambulatory at scene and transported to Wexcombe Memorial ED.
     9	Source [Ex. __ / Bates __]: "Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED."
    10	
    11	March 18, 2026 — Wexcombe Memorial ED
    12	Diagnosed with cervical strain and lumbar strain; cervical and lumbar spine X-rays negative for fracture.
    13	Source [Ex. __ / Bates __]: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture."
    14	
    15	March 26, 2026 — Pellingham and Rook PLLC, correspondence (letter of protection)
    16	Law firm letter of protection to Fennimoor Spine Clinic states the firm represents the client for injuries from a collision on 2026-03-18 and asks the clinic to defer collection while the claim is pending.
    17	Source [Ex. __ / Bates __]: "This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending."
    18	
    19	March 27, 2026 — Fennimoor Spine Clinic, new patient
    20	Neck pain 7/10 and low back pain 7/10; treating under a letter of protection; plan is chiropractic care three times weekly.
    21	Source [Ex. __ / Bates __]: "Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly."
    22	
    23	March 27, 2026 — Fennimoor Spine Clinic, new patient intake form (OCR text)
    24	Intake form: rear ended at red light, neck and back hurt; prior accidents and prior injuries marked No; pain today 7.
    25	Source [Ex. __ / Bates __]: "How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7."
    26	
    27	April 24, 2026 — Fennimoor Spine Clinic, visit 8
    28	Neck pain 5/10 and low back pain 6/10; manual therapy and exercises continued.
    29	Source [Ex. __ / Bates __]: "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued."
    30	
    31	May 29, 2026 — Fennimoor Spine Clinic, visit 14
    32	Neck pain 4/10, low back pain 5/10. Care continues.
    33	Source [Ex. __ / Bates __]: "Neck pain 4/10, low back pain 5/10. Care continues."
    34	
    35	BILLED CHARGES
    36	
    37	Wexcombe Memorial ED, March 18, 2026: $3,260.00
    38	Source [Ex. __ / Bates __]: "ED charge: $3,260."
    39	Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00
    40	Source [Ex. __ / Bates __]: "New patient exam charge $250.00"
    41	Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $180.00
    42	Source [Ex. __ / Bates __]: "x-ray charge $180.00"
    43	Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $2,310.00
    44	Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"
    45	
    46	Billed charges accepted from these records: $6,000.00====
SAME_ONSCREEN
====
     1	INTERNAL REVIEW NOTES — DO NOT SEND
     2	
     3	This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
     4	
     5	FLAGS ACCEPTED
     6	- Gap: 35 days, April 24, 2026 to May 29, 2026: record 7 (Fennimoor Spine Clinic, visit 8, April 24, 2026) to record 8 (Fennimoor Spine Clinic, visit 14, May 29, 2026).
     7	- Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior accidents? Yes [ ] No [X]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
     8	- Conflict, other fact mismatch: record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior injuries? Yes [ ] No IX]."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
     9	- Prior condition: record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "Problem list: hypertension, type 2 diabetes, chronic low back pain."; record 1 (Dr. Hesper Alderton, primary care, March 4, 2026) "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."; record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior accidents?"; record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026) "Prior injuries?".
    10	- Causation language: record 2 (Ashgrove Fire-Rescue run report, March 18, 2026) "Ambulatory at scene."; record 4 (Pellingham and Rook PLLC, correspondence (letter of protection), March 26, 2026) "Letter of protection to Fennimoor Spine Clinic."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Patient referred by attorney."; record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026) "Treating under a letter of protection."; record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) "Account held under letter of protection."
    11	
    12	FLAGS DISMISSED
    13	- none
    14	
    15	FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
    16	- Record 1 (Dr. Hesper Alderton, primary care, March 4, 2026): "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy." Conflict, other fact mismatch; prior condition.
    17	- Record 2 (Ashgrove Fire-Rescue run report, March 18, 2026): "Ambulatory at scene." Causation language.
    18	- Record 5 (Fennimoor Spine Clinic, new patient, March 27, 2026): "Treating under a letter of protection." Causation language.
    19	- Record 6 (Fennimoor Spine Clinic, new patient intake form (OCR text), March 27, 2026): "Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]." Conflict, other fact mismatch; prior condition.
    20	- Record 7 (Fennimoor Spine Clinic, visit 8, April 24, 2026): "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued." Gap.
    21	- Record 8 (Fennimoor Spine Clinic, visit 14, May 29, 2026): "Neck pain 4/10, low back pain 5/10. Care continues." Gap.
    22	
    23	AMOUNTS NOT TOTALED
    24	- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "total charges $2,740.00." Not totaled ($2,740.00): Total or subtotal line: it repeats the charges listed with it, so it is not totaled.
    25	- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Payment received $300.00." Not totaled ($300.00): Payment: money received, not a charge.
    26	- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Adjustment (courtesy discount) -$274.00." Not totaled ($274.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.
    27	- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026): "Balance due $2,166.00." Not totaled ($2,166.00): Balance or amount due: worked out from charges, payments and adjustments, not a charge.
    28	
    29	DAMAGES MENTIONS (not charges)
    30	- none
    31	
    32	FUTURE TREATMENT RECOMMENDED (no cost stated)
    33	- none
    34	
    35	BILLS TO REQUEST (entry in the letter, no accepted charge)
    36	- Dr. Hesper Alderton; Ashgrove Fire-Rescue run report.
    37	
    38	RECORDS NOT IN THE TREATMENT SECTION
    39	- Record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) — dismissed
    40	
    41	EDITED ITEMS
    42	- none
    43	
    44	PENDING ITEMS NOT INCLUDED
    45	- none
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:28:11.681Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t200; PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t200_undated_charge_label.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/pytest-t200.out 2>&1; echo exit=$?; tail -3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/pytest-t200.out",
 "description": "Run T-200 unit test from the archive",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T23:28:13.968Z

**tool result**
````
exit=0
......                                                                   [100%]
6 passed in 1.93s
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:28:15.664Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t200; PYTHONDONTWRITEBYTECODE=1 LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.letter_check > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/letter_check.out 2>&1; echo exit=$?; tail -8 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/letter_check.out",
 "description": "Run letter_check eval from the archive",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T23:28:22.582Z

**tool result**
````
exit=0
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:28:25.013Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal; grep -n \"statement dated\\|service date\\|No date of service\" p01.out | head -20; grep -n \"######## bills\" p01.out",
 "description": "Find Step 3 date labels in probe output"
}
````

### User / tool · 2026-11-02T23:28:25.112Z

**tool result**
````
406:$250.00	Fennimoor Spine Clinic, itemized ledger	No date of service (statement dated June 15, 2026)	Change
407:$180.00	Fennimoor Spine Clinic, itemized ledger	No date of service (statement dated June 15, 2026)	Change
408:$2,310.00	Fennimoor Spine Clinic, itemized ledger	No date of service (statement dated June 15, 2026)	Change
463:$250.00	Fennimoor Spine Clinic, itemized ledger	No date of service (statement dated June 15, 2026)	Change
464:$180.00	Fennimoor Spine Clinic, itemized ledger	No date of service (statement dated June 15, 2026)	Change
465:$2,310.00	Fennimoor Spine Clinic, itemized ledger	No date of service (statement dated June 15, 2026)	Change
344:######## bills 0 item=a1 boxes=[]
347:######## bills 1 item=a2 boxes=['check-separate', 'check-compare']
350:######## bills 2 item=a3 boxes=['check-separate', 'check-compare']
353:######## bills 3 item=a4 boxes=['check-separate', 'check-compare']
356:######## bills 4 item=a5 boxes=['check-compare']
359:######## bills 5 item=a6 boxes=['check-compare']
362:######## bills 6 item=a7 boxes=[]
365:######## bills 7 item=a8 boxes=['check-compare']
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:28:27.943Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal; sed -n 347,349p p01.out | cut -c1-1500",
 "description": "Read Step 3 card text for first ledger line"
}
````

### User / tool · 2026-11-02T23:28:28.023Z

**tool result**
````
######## bills 1 item=a2 boxes=['check-separate', 'check-compare']
CARD: Not counted yet / Fennimoor Spine Clinic, itemized ledger · June 15, 2026 /  / $250.00 /  / The line states no date of service, so it is not a single dated bill line and is not totaled. /  / You can still count it if you checked the ledger yourself. / I checked this is a separate charge for a service. / A second AI check thought this may be a billed charge, not what it was first sorted as. / I read this amount against the highlighted words myself.
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/lib-s3-01-a2.png
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:28:33.090Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal; LC_ALL=C grep -n -P \"[^\\x00-\\x7F]\" lib11-letter.txt | cut -c1-60; grep -c \"service date not stated\" lib11-letter.txt; grep -c \"service date\\|date of service\" lib11-notes.txt; git -C /Users/arsis/zlayt-pm-project show --stat bd72d5b | grep -c \"evals/\"",
 "description": "Check non-ASCII chars, phrase counts, eval changes"
}
````

### User / tool · 2026-11-02T23:28:33.219Z

**tool result**
````
3:March 4, 2026 — Dr. Hesper Alderton, primary care
7:March 18, 2026 — Ashgrove Fire-Rescue run report
11:March 18, 2026 — Wexcombe Memorial ED
15:March 26, 2026 — Pellingham and Rook PLLC, corresponden
19:March 27, 2026 — Fennimoor Spine Clinic, new patient
23:March 27, 2026 — Fennimoor Spine Clinic, new patient in
27:April 24, 2026 — Fennimoor Spine Clinic, visit 8
31:May 29, 2026 — Fennimoor Spine Clinic, visit 14
3
0
0
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:28:35.912Z

**tool call — Bash**
````
{
 "command": "kill 66842; python3 -c \"import time; time.sleep(1)\"; lsof -iTCP:7963 -sTCP:LISTEN -nP; echo lsof_exit=$?; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7963/api/health",
 "description": "Stop the archive server and confirm port closed"
}
````

### User / tool · 2026-11-02T23:28:37.108Z

**tool result (error)**
````
Exit code 7
lsof_exit=1
000
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:28:42.125Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"R-EX-4\\|R-EX-2 \\|R-EX-3\" spec/REQUIREMENTS.md | head; grep -n \"D-064\\|D-071\" memory/ORCHESTRATOR_DECISIONS.md | head",
 "description": "Look up R-EX-4 and D-064/D-071 text"
}
````

### User / tool · 2026-11-02T23:28:42.211Z

**tool result**
````
66:| R-FL-2 | **Conflicting facts.** Flag facts that conflict across records, citing both excerpts. | Sample must raise (a) accident date 2026-01-09 (records 1, 2) vs "Date of accident per intake form: 2026-01-19" (record 7), shown as a conflict and **not merged**, with the records cited (R-EX-4) and no choice made between the dates or any "delay from the accident" computed; the tool may state "first recorded treatment: January 9, 2026" (D-017); (b) PT plan of 12 visits (record 4) vs discharge at visit 9 after two missed appointments (record 6). `case_05_provider_conflict` raises its required flag and tolerates the name variants. | EV `flag_*[conflict]` + PR (legal-nurse) |
120:| R-EX-2 | Every entry and charge in the letter carries a source line with the verbatim excerpt. No short-cite mode (D-002). | UT: for every statement and amount line in `letter_text`, the quoted excerpt is a substring of the input after normalization (100%, ship bar 1). Headings and the total line are fixed text. | UT + EV `grounding_rate` |
121:| R-EX-3 | Chronological and deterministic: same accepted set → byte-identical `letter_text` and `internal_notes_text`. | UT: dates in `letter_text` are non-decreasing; export twice and compare. | UT |
122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first appearance in the chronology, omitting any provider with an accepted charge, with " (itemized ledger)" appended when the provider has a non-dismissed rate. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 1, 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (entry 1 because the accident-date conflict cites its "rear-ended" sentence) (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); the accident-date conflict citing records 1 and 2 (header date, no choice between dates, D-017) and record 7's intake line; the K5 causation item for record 7's intake line; the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; the bills-to-request line is exactly "Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management." UT: every match of the case-insensitive pattern `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
182:3. R-EX-4 sections 7 and 8 (future treatment, bills to request).
325:| 1 | **Grounding** | 100% of exported statements and amounts carry a verbatim excerpt present in the input. Any miss is a blocker. | Eval metric `grounding_rate` (excerpts, providers, amounts, dates; exported items) + export unit test | `python -m evals.run`; `pytest tests/unit` | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
346:| A-101 | The paralegal builds the chronology; the attorney reviews the letter. | R-RV-*, R-EX-1, R-EX-4 |
351:| A-106 | The export cites each line by provider as written in the header + date of service with an `[Ex. __ / Bates __]` placeholder; the tool assigns no numbers; internal notes cite `record N (provider as written, date)` per R-EX-4 | R-EX-2, R-EX-4, R-EX-6 |
359:- Providers with an entry in the letter but no stated charge are "bills to request" (R-EX-4).
360:- Recommended future treatment is a specials item the firm will want costed; the notes surface it (R-EX-4).
72:| D-064 | Two kinds of "not counted" amounts (2026-11-02, GATE-M2 r2 paralegal). (a) Rule-excluded: total, balance, payment, credit, year-to-date, insurer restatement - never countable, the UI says why in plain words. (b) Not counted only because the line lacks something D-060 needs (no date of service, no bill header) - the UI shows that plain reason in the review screen and offers "Count this charge", a named confirm ("I checked this is a separate charge for a service"), recorded in the audit trail; it then sums like any accepted charge. Amends D-059 item on reclassify: (b) is promotable with the confirm, (a) never. | The default-deny rule undercounts real ledger lines (lib11 $3,260 vs $6,000); the paralegal must see why and be able to fix it herself, without reopening the overcount paths. | GATE-M2 r2 paralegal |
84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:28:44.942Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; sed -n 84,100p memory/ORCHESTRATOR_DECISIONS.md",
 "description": "Read D-071 decision text"
}
````

### User / tool · 2026-11-02T23:28:45.022Z

**tool result**
````
## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:28:55.657Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py; ls reviews/ | grep T-200; ls artifacts/review-evidence/T-200-paralegal/; grep -n \"letter_check\\|accept\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t200/evals/letter_check.py | head -12",
 "description": "Check jsoncheck script, existing reviews, evidence files"
}
````

### User / tool · 2026-11-02T23:28:55.756Z

**tool result**
````
artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py
db
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
4:  run the pipeline on a scratch database, accept every item that code lets her accept (a refusal is counted, not hidden), export the letter in both styles;
8:  - in the BILLED CHARGES section, a currency string that is not an accepted charge or the total line (R-EX-8: exactly 'Billed charges accepted from these records: $X');
10:  - money written WITHOUT a '$' anywhere outside the accepted charge lines ('TOTAL CHARGE 49100', 'AMOUNT PAID 0 00', '24F 25500'): T-139 round 2.
14:Pure check: `violations(letter, accepted_cents)`; the pipeline walk is `letters_for(text)`.
16:    python -m evals.letter_check            prints one line per case and exits 1 on any violation
27:CHARGES, TOTAL = "BILLED CHARGES", "Billed charges accepted from these records: "
54:def violations(letter: str, accepted_cents=(), expect_none: bool = False) -> list:
55:    """Currency strings the letter may not carry. `accepted_cents`: the accepted charges (the only amounts the BILLED CHARGES section may list).
56:    `expect_none`: nothing was accepted as a charge, so no currency string may appear anywhere."""
64:    if expect_none or not accepted_cents:
65:        out += [f"letter states {s} with no accepted charge" for s in dollar_figures(tail)]
69:    allowed = {c for c in accepted_cents} | {sum(accepted_cents)}
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:29:27.661Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/draft-T-200-paralegal.md",
 "content": "# T-200 undated ledger charge label (bd72d5b): paralegal review (Maria Delgado, senior PI paralegal)\n\n**Verdict: pass** (0 blockers, 0 majors, 2 minors, 1 nit).\n\n**Scope.** I extracted `git archive bd72d5b` to the session scratchpad. I ran it on port 7963 with the fixture backend (`/api/health`: `\"demo_mode\":true,\"local_mode\":true`). Local mode is needed because `/api/library` is local-only. I stopped listener PID 66842 afterwards: `lsof` returned exit 1 and `curl` returned 000. Dated charge lines (D-071) are out of scope and not graded here.\n\n**Deterministic checks first (from the archive):**\n- `pytest tests/unit/test_t200_undated_charge_label.py` gave `6 passed in 1.93s` (pytest-t200.out).\n- `python -m evals.letter_check` gave `{\"value\": 0, \"cases\": 25, ...}` (letter_check.out).\n\n## What I did on lib11\n\n1. Drafted lib11. Accepted Step 2, and dismissed the refused ledger entry e9.\n2. In Step 3, counted the three undated ledger lines. For each I ticked \"I checked this is a separate charge for a service\" and the compare box.\n3. Downloaded the letter and notes. The on-screen letter text is byte-identical to the download.\n\nThe BILLED CHARGES section now reads (lib11-letter.txt:37-46):\n\n```\nWexcombe Memorial ED, March 18, 2026: $3,260.00\nSource [Ex. __ / Bates __]: \"ED charge: $3,260.\"\nFennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00\nSource [Ex. __ / Bates __]: \"New patient exam charge $250.00\"\nFennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $180.00\nSource [Ex. __ / Bates __]: \"x-ray charge $180.00\"\nFennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $2,310.00\nSource [Ex. __ / Bates __]: \"treatment visits 1 through 14 charge $2,310.00\"\n\nBilled charges accepted from these records: $6,000.00\n```\n\n## Does it work in a demand letter? Yes.\n\nMy r2 major (T-181-paralegal-r2) is fixed:\n- **No bare date.** The old line was \"itemized ledger, June 15, 2026: $250.00\". An adjuster would have read June 15 as a visit that has no treatment note. Now the date is labelled as the statement's.\n- **The date is faithful.** \"statement dated June 15, 2026\" is an unambiguous reformat of the record's own words, \"statement date 06/15/2026\" (case_lib11 record 9).\n- **The adjuster can still use it.** The date lets the adjuster tie each line to the ledger page.\n- **Screen and letter agree.** Step 3 shows \"No date of service (statement dated June 15, 2026)\" (p01.out:406-408).\n- **Clean paste.** The charge lines are plain ASCII, so they paste into Word cleanly.\n- **The ED line is unchanged.** It still carries its date of service.\n- **The total is right.** It is $6,000.00.\n\n\"Service date not stated\" is blunt. An adjuster will ask for a dated bill (CMS-1500) either way, and the blunt wording is better than any date the reader would take as a visit. Whether the attorney wants that admission in the demand is a strategy call, so it is outside my lens (litigation-lead).\n\n## What is still thin (minors)\n\n1. **The internal notes do not mention these three charges.** `grep -c \"service date\\|date of service\" lib11-notes.txt` gives 0. The attorney reads the notes before the letter goes out. Nothing there says three counted Fennimoor charges have no date of service, or suggests requesting a dated itemized bill. R-EX-4 section 5 covers only amounts that are not totaled, so this is a \"should\", not a spec violation.\n2. **No eval guards a counted undated line.** The card AC says \"golden letters and evals/letter_check updated\". `git show --stat bd72d5b` lists no `evals/` file. The handoff says letter_check walks accept only, not count. A regression on this line would be caught only by the new unit test.\n\n**Nit.** The Step 3 card header still reads \"Fennimoor Spine Clinic, itemized ledger · June 15, 2026\", with the date bare (p01.out:348). The reason line under it does explain it. It is screen only, not in the letter.\n\n```json\n{\"card\": \"T-200\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"git archive bd72d5b extracted to the session scratchpad (t200/); fixture backend FIXTURE_SET=curated, demo mode (health: demo_mode true) with ZLAYT_MODE=local for /api/library, http://127.0.0.1:7963, listener PID 66842 stopped (lsof exit 1, curl 000). Library case case_lib11_priors_and_ledger. Dated charge lines (D-071) not graded. Evidence dir artifacts/review-evidence/T-200-paralegal/ (lib-step4.png was taken after revisiting Step 3, so it shows Step 3; the Step 4 letter is in lib11-letter-onscreen.txt).\",\n \"exercised\": [\n  \"Read personas/paralegal.md, reviews/T-181-paralegal-r2.md, board.py show T-200 (AC, notes, handoff), git show bd72d5b (export.py charge_when, store.charge_dos_stated, amounts.py, api.md), D-064 and D-071 in memory/ORCHESTRATOR_DECISIONS.md, R-EX-4 in spec/REQUIREMENTS.md\",\n  \"From the archive: pytest tests/unit/test_t200_undated_charge_label.py: '6 passed in 1.93s' (pytest-t200.out); python -m evals.letter_check: value 0, 25 cases (letter_check.out)\",\n  \"Playwright p01_lib11.py (p01.out): New case > library lib11 > Read > Draft (2.6 s) > Step 2 accept all, dismiss refused e9 > Step 3 count the three undated ledger lines (check-separate + check-compare) > Step 4 download letter and notes, read on-screen letter (identical to download) > revisit Step 3 (date column 'No date of service (statement dated June 15, 2026)')\",\n  \"Read lib11-letter.txt BILLED CHARGES lines 37-46 against evals/library/case_lib11_priors_and_ledger.txt record 9 ('statement date 06/15/2026'); non-ASCII grep on the letter (charge lines ASCII); grep of lib11-notes.txt for service-date wording (0)\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"verify_quickly\": 4, \"undated_charge_line_reads_right_for_adjuster\": 4},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"Internal notes say nothing about the three counted charges that have no date of service\",\n   \"evidence\": \"artifacts/review-evidence/T-200-paralegal/lib11-notes.txt: grep -c 'service date\\\\|date of service' = 0; the BILLS TO REQUEST line names only 'Dr. Hesper Alderton; Ashgrove Fire-Rescue run report.'\",\n   \"why_it_matters\": \"The attorney reads the notes before the demand goes out. The adjuster will ask for a dated itemized bill for $2,740 of Fennimoor charges, so the records request should be queued now, not after the response letter.\",\n   \"fix\": \"Add one notes line per provider: 'Counted without a stated date of service: record 9 (Fennimoor Spine Clinic, itemized ledger, June 15, 2026) $250.00, $180.00, $2,310.00; request dated itemized bill.' Keep the letter wording unchanged (D-071).\",\n   \"acceptance_test\": \"Unit test on lib11 with the three ledger lines counted: internal_notes_text names each counted undated charge and contains 'request dated itemized bill'; letter_text unchanged.\"},\n  {\"severity\": \"minor\", \"title\": \"No eval or golden covers a counted undated ledger line (AC says letter_check and goldens updated)\",\n   \"evidence\": \"Card AC 1: 'golden letters and evals/letter_check updated'; git show --stat bd72d5b lists only app/backend/amounts.py, export.py, store.py, memory/contracts/api.md and tests/unit/test_t200_undated_charge_label.py; handoff: 'letter_check walks accept only, not count'.\",\n   \"why_it_matters\": \"The only guard against the old 'itemized ledger, June 15, 2026: $250.00' line coming back is one unit test. The eval that walks every letter never produces this line.\",\n   \"fix\": \"Give evals/letter_check (qa) a count walk for D-064 'Count this charge' items. Assert that no charge line whose quote has no date shows a bare long date before the amount.\",\n   \"acceptance_test\": \"python -m evals.letter_check exits 1 when charge_when is reverted to f'{src}, {_long_date(rd)}' (mutation test).\"},\n  {\"severity\": \"nit\", \"title\": \"Step 3 card header still shows the statement date bare\",\n   \"evidence\": \"p01.out:348 'Fennimoor Spine Clinic, itemized ledger · June 15, 2026 / ... / The line states no date of service'\",\n   \"why_it_matters\": \"On screen only. The reason line below explains it, but the header reads like a date of service at a glance.\",\n   \"fix\": \"Header 'itemized ledger · statement dated June 15, 2026' for billing records.\",\n   \"acceptance_test\": \"E2E on lib11 Step 3: the card header for a2 contains 'statement dated'.\"}\n ],\n \"whats_right\": [\n  \"The counted ledger line names its date as the statement's and says the service date is not stated. Nothing reads as a visit date (lib11-letter.txt:39-43).\",\n  \"Step 3 ('No date of service (statement dated June 15, 2026)') and the letter now agree.\",\n  \"The ED line keeps its date of service, and the total is $6,000.00; letter_check is value 0 over 25 cases.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T23:29:27.769Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-200-paralegal/draft-T-200-paralegal.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:29:31.606Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"item=e9\" artifacts/review-evidence/T-200-paralegal/p01.out | head -3; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py artifacts/review-evidence/T-200-paralegal/draft-T-200-paralegal.md",
 "description": "Confirm e9 refusal and validate draft JSON"
}
````

### User / tool · 2026-11-02T23:29:31.725Z

**tool result**
````
166:######## 19 item=e9 yes_disabled=True compare_box=False
json blocks: 1
verdict: pass | severities: ['minor', 'minor', 'nit']
verdict rule expects: pass | matches: True
model: claude-opus-5-5 | card: T-200 | persona: paralegal-reviewer
all finding fields present
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:29:33.157Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cp artifacts/review-evidence/T-200-paralegal/draft-T-200-paralegal.md reviews/T-200-paralegal.md && python3 tools/board.py validate reviews/T-200-paralegal.md",
 "description": "Publish review and run board validator"
}
````

### User / tool · 2026-11-02T23:29:33.312Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:29:34.077Z

Saving the memory note.

### Assistant · claude-opus-5-5 · 2026-11-02T23:29:39.672Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t200-undated-charge-label.md",
 "content": "---\nname: t200-undated-charge-label\ndescription: T-200 (bd72d5b) pass: counted undated lib11 ledger lines print \"(statement dated June 15, 2026; service date not stated)\"; D-071 binds that form; minors = notes silent, no count-walk eval\nmetadata:\n  type: project\n---\n\nT-200 review (reviews/T-200-paralegal.md, bd72d5b): pass, 2 minors + 1 nit. My T-181 r2 letter-date major is closed.\n- D-071 (ORCHESTRATOR_DECISIONS.md:84) makes the T-200 wording binding for undated charges and moves dated charge lines (statement date vs service date: case_09, lib14, lib10) to another card. Grade that card on per-line service dates and period ranges.\n- Open minors: the internal notes say nothing about counted charges that have no date of service (no \"request dated itemized bill\"). letter_check walks accept only, never D-064 count, so no eval produces the line.\n- Mechanics: \"demo mode\" means a fixture backend; ZLAYT_MODE=local is still demo_mode true and gives /api/library. Reuse artifacts/review-evidence/T-200-paralegal/h.py + p01_lib11.py (port 7963, about 26 s end to end). The draft-then-cp flow with T-116-paralegal-r2-jsoncheck.py worked.\n\n**Why:** next round on the D-071 card, check the dated lines against the D-071 rules above.\n**How to apply:** related [[t181-r2-patterns]], [[reviewer-run-pitfalls-pass4]].\n"
}
````

### User / tool · 2026-11-02T23:29:39.778Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t200-undated-charge-label.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:29:41.057Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer; printf '%s\\n' \"- [T-200 undated charge label](t200-undated-charge-label.md) — bd72d5b pass: 'statement dated X; service date not stated' (D-071 binding); notes silent, no count-walk eval\" >> MEMORY.md; tail -2 MEMORY.md",
 "description": "Add memory index entry"
}
````

### User / tool · 2026-11-02T23:29:41.158Z

**tool result**
````
- [GATE-M2 r2 patterns](gate-m2-r2-patterns.md) — lib11 total/conflict fixed; unclear ledger rows wrong reason, no reclassify control; Start review strands items
- [T-200 undated charge label](t200-undated-charge-label.md) — bd72d5b pass: 'statement dated X; service date not stated' (D-071 binding); notes silent, no count-walk eval
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:29:43.189Z

T-200 passes with 0 blockers, 0 majors, 2 minors and 1 nit: the counted lib11 lines now read "itemized ledger (statement dated June 15, 2026; service date not stated): $250.00", which works in a demand letter, and the minors are that the internal notes never mention these three undated charges and that no eval covers a counted undated line; review at /Users/arsis/zlayt-pm-project/reviews/T-200-paralegal.md, demo run on port 7963 with PID 66842 stopped.
