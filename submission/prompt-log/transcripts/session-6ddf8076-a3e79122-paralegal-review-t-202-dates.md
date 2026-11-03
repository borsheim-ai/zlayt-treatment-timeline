# Subagent: Paralegal review: T-202 dates (Paralegal review: T-202 dates)

Source: `agent-a3e791227f9150f37.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T23:37:16.204Z

Review T-202 (D-071) in /Users/arsis/zlayt-pm-project as the senior PI paralegal, starting from a fresh context. The card is commit f0921e4; read D-071 in memory/ORCHESTRATOR_DECISIONS.md and the card handoff with its letter diffs.

Run a `git archive f0921e4` copy in demo mode on your own port, and stop your PID afterward. Generate the letters for case_09, lib14 and lib10, plus the sample. Check each charge line's date against the bill page in the record:
- service date versus statement date;
- the UB-04 period shown as "June 9–12, 2026";
- charges in service-date order.

Judge whether the letter is now correct and credible to an adjuster. Write reviews/T-202-paralegal.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:18.959Z

**tool call — Bash**
````
{
 "command": "cat personas/paralegal.md | head -c 200 >/dev/null; wc -l personas/paralegal.md; cat .claude/agent-memory/paralegal-reviewer/t200-undated-charge-label.md .claude/agent-memory/paralegal-reviewer/t181-r2-patterns.md .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md .claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md",
 "description": "Read dossier size and relevant memories"
}
````

### User / tool · 2026-11-02T23:37:19.083Z

**tool result**
````
      84 personas/paralegal.md
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

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:20.166Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T23:37:20.175Z

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

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:21.061Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-071\" -A 30 memory/ORCHESTRATOR_DECISIONS.md | head -80; python3 tools/board.py show T-202",
 "description": "Read D-071 and the T-202 card"
}
````

### User / tool · 2026-11-02T23:37:21.204Z

**tool result**
````
84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
85-T-200 found dated charge lines print the record date, which for a ledger, invoice or UB-04 is the statement date (case_09 Mar 1 vs visit Feb 2; lib14 Nov 12 vs run Sept 14; lib10 June 19 vs 06/09–06/12). Binding: a charge line prints the service date the bill line states (deterministic parse from the line or its row, code not LLM); a service period prints as a range ("June 9–12, 2026"); when no service date is stated, the T-200 form applies ("statement dated X; service date not stated"). Goldens change accordingly and evals/letter_check.py gains a check that every dated charge line's date equals the service date in its quote.
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
updated_at: "2026-11-02T23:37:13Z"
claimed_by: "backend"
claimed_at: "2026-11-02T23:26:10Z"
rounds: 0
commits: ["f0921e4"]
reviews: []
ac:
  - {"n": 1, "text": "per D-071; case_09/lib14/lib10 letters show the service date/period; goldens updated with a diff in the handoff; evals/letter_check.py asserts each dated charge line's date equals the service date in its quote, over all 25 cases incl. a count path; unit + guided e2e green from git archive", "done": true, "evidence": "tests/unit/test_t202_charge_service_dates.py (13 pass); python -m evals.letter_check value 0 over 25 cases incl. count variant, mutants (record-date printing; bare statement date) fail it with 48 / 20 violations; git archive tree df2e300b60: unit 1456+1478+1353+1597 passed, guided e2e 128 passed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T23:26:10Z backend: claimed
- 2026-11-02T23:29:45Z orchestrator: Also cover T-200 minor: the letter_check count path must include a counted undated line (lib11).
- 2026-11-02T23:37:08Z backend: AC 1 checked: tests/unit/test_t202_charge_service_dates.py (13 pass); python -m evals.letter_check value 0 over 25 cases incl. count variant, mutants (record-date printing; bare statement date) fail it with 48 / 20 violations; git archive tree df2e300b60: unit 1456+1478+1353+1597 passed, guided e2e 128 passed
- 2026-11-02T23:37:08Z backend: moved in_progress -> in_review
- 2026-11-02T23:37:13Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer

## Handoff
What changed: charge_basis returns dos_end (end of a stated period); store.charge_service_dates -> dos_iso/dos_end_iso on each exported charge; export prints the bill line's service date, a period as a range (June 9-12, 2026), T-200 statement form only when none stated; charges sorted by service date; api.md note. evals/letter_check.py: third variant counts every countable amount (D-064, with confirm_flag) and charge_date_violations asserts each dated charge line's date (day or range) is a service date its record states (statement/billing/due-led dates never are; a visit note's date is), and the T-200 form matches the record's date with a date-free quote. | Golden diff (letters, accept-all, standard; oneline identical): sample.export.expected.txt UNCHANGED (no stored golden carries the three changed cases; the diff is of generated letters): case_09 'billing statement, March 1, 2026: $275.00' -> 'February 2, 2026'; lib14 'ambulance invoice, November 12, 2026: $1,380.00 / $187.05' -> 'September 14, 2026'; lib10 UB-04 'June 19, 2026' x4 (,920.00, $2,105.00, $386.50, $712.00) -> 'June 9-12, 2026'. | Verified from git archive of the committed tree: unit 5884 passed, guided e2e 128 passed; letter_check 0 violations over 25 cases; mutants (print record date; print statement date for undated) fail letter_check with 48 / 20 violations. Count path exercised: lib06, 09, 11, 12, 15 print the T-200 form. | Left: nothing. Surprise: UB-04 'statement period' is the service period, so the check's statement-lead filter excludes 'statement date' only.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:23.504Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD; git log --oneline -5; git show --stat f0921e4 | head -40; ls artifacts/review-evidence/T-200-paralegal/; ls artifacts/review-evidence/ | grep -i -E \"serve|jsoncheck\" | head",
 "description": "Check HEAD, commit stat, prior evidence scripts"
}
````

### User / tool · 2026-11-02T23:37:23.794Z

**tool result**
````
f0921e4
f0921e4 feat(backend): T-202 D-071 letter charge lines print the bill line's service date or period, not the statement date
a44cfa7 fix(qa): T-187 r4 README item 7 wording matches the normalized rule (no unicode/percent/entity decoding claimed)
bd72d5b fix(backend): T-200 counted undated ledger charge prints its statement date as such, never as a service date
8f78874 fix(qa): T-187 r4 / T-198 prompt log: private terms read from deploy/.private_patterns (none in tracked code), normalized-view redaction + self-test (D-070), device names, tree scan tool
2c19817 fix(frontend): T-181 r3 phone: highlighted words scrolled into a record window sized for them, refused edit shown above the action bar, panel-list test scans only loaded scripts
commit f0921e4189f70a9dedb3d02cbb2201a734fda679
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 17:36:53 2026 -0600

    feat(backend): T-202 D-071 letter charge lines print the bill line's service date or period, not the statement date
    
    charge_basis returns the end of a stated period; store.charge_service_dates feeds dos_iso/dos_end_iso to the export; a period prints as a range (June 9-12, 2026); charges sort by service date; the T-200 statement-date form still applies when no service date is stated. evals/letter_check gains a count path and charge_date_violations (every dated charge line's date must be a service date its record states). case_09, lib14, lib10 letters change.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/amounts.py                       |  24 +++--
 app/backend/export.py                        |  35 ++++++--
 app/backend/store.py                         |  17 ++--
 evals/letter_check.py                        | 125 ++++++++++++++++++++++++++-
 memory/contracts/api.md                      |   2 +-
 tests/unit/test_t200_undated_charge_label.py |  25 +++---
 tests/unit/test_t202_charge_service_dates.py | 106 +++++++++++++++++++++++
 7 files changed, 294 insertions(+), 40 deletions(-)
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
T-013-r2-paralegal-jsoncheck.py
T-013-r3-paralegal-jsoncheck.py
T-015-r2-paralegal-jsoncheck.py
T-015-r3-paralegal-jsoncheck.py
T-015-r4-paralegal-jsoncheck.out.txt
T-015-r4-paralegal-jsoncheck.py
T-039-r2-jsoncheck.py
T-043-paralegal-jsoncheck.py
T-049-served-index.html
T-060-paralegal-pass4-serve.py
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:25.603Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-200-paralegal/h.py; echo ----; cat artifacts/review-evidence/T-200-paralegal/p01_lib11.py; echo ---; cat artifacts/review-evidence/T-200-paralegal/run.log | head -30",
 "description": "Read prior T-200 helper scripts"
}
````

### User / tool · 2026-11-02T23:37:25.715Z

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
----
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
open(OUT + "/lib11-letter-onscreen.txt", "w").write(pg.inner_text("[data-testid=letter-text]"))
pg.click("[data-testid=step-3]")
pg.wait_for_selector("[data-testid=view][data-ready]")
pg.wait_for_timeout(600)
dump("step 3 revisited after export")
shot("lib-step3-revisit", full=True)
shot("lib-step4", full=True)
log("lib11 done in", round(time.time() - T0, 1), "s")
---
### run p01_lib11.py at 17:27:07
===== lib11 records url=http://127.0.0.1:7963/case/jIY51JSXVa5bTjxYQD04fw/records
Skip to the main content
Synthetic data only — never paste real records
‹
Your cases
Priors and ledger
9 records
Demo: sample answers prepared by our team
Dark mode
1
1 Add records
Not started
(step 1 of 4)
2
2 Check the timeline
After step 1
(step 2 of 4)
3
3 Check the bills
After step 1
(step 3 of 4)
4
4 Get your letter
After step 1
(step 4 of 4)
Step 1 of 4
We found 9 records

Check that these are the records you meant to add. Next, we'll draft a one-line timeline entry for each one.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:27.922Z

**tool call — Bash**
````
{
 "command": "grep -n -i -E \"serve|archive|port|PID\" artifacts/review-evidence/T-200-paralegal/draft-T-200-paralegal.md | head -20; cat artifacts/review-evidence/T-060-paralegal-pass4-serve.py",
 "description": "Find how the previous server was launched"
}
````

### User / tool · 2026-11-02T23:37:28.019Z

**tool result**
````
5:**Scope.** I extracted `git archive bd72d5b` to the session scratchpad. I ran it on port 7963 with the fixture backend (`/api/health`: `"demo_mode":true,"local_mode":true`). Local mode is needed because `/api/library` is local-only. I stopped listener PID 66842 afterwards: `lsof` returned exit 1 and `curl` returned 000. Dated charge lines (D-071) are out of scope and not graded here.
7:**Deterministic checks first (from the archive):**
54: "scope": "git archive bd72d5b extracted to the session scratchpad (t200/); fixture backend FIXTURE_SET=curated, demo mode (health: demo_mode true) with ZLAYT_MODE=local for /api/library, http://127.0.0.1:7963, listener PID 66842 stopped (lsof exit 1, curl 000). Library case case_lib11_priors_and_ledger. Dated charge lines (D-071) not graded. Evidence dir artifacts/review-evidence/T-200-paralegal/ (lib-step4.png was taken after revisiting Step 3, so it shows Step 3; the Step 4 letter is in lib11-letter-onscreen.txt).",
56:  "Read personas/paralegal.md, reviews/T-181-paralegal-r2.md, board.py show T-200 (AC, notes, handoff), git show bd72d5b (export.py charge_when, store.charge_dos_stated, amounts.py, api.md), D-064 and D-071 in memory/ORCHESTRATOR_DECISIONS.md, R-EX-4 in spec/REQUIREMENTS.md",
57:  "From the archive: pytest tests/unit/test_t200_undated_charge_label.py: '6 passed in 1.93s' (pytest-t200.out); python -m evals.letter_check: value 0, 25 cases (letter_check.out)",
65:   "evidence": "artifacts/review-evidence/T-200-paralegal/lib11-notes.txt: grep -c 'service date\\|date of service' = 0; the BILLS TO REQUEST line names only 'Dr. Hesper Alderton; Ashgrove Fire-Rescue run report.'",
70:   "evidence": "Card AC 1: 'golden letters and evals/letter_check updated'; git show --stat bd72d5b lists only app/backend/amounts.py, export.py, store.py, memory/contracts/api.md and tests/unit/test_t200_undated_charge_label.py; handoff: 'letter_check walks accept only, not count'.",
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

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:28.632Z

Extracting the archive and starting the server.

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:30.865Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && mkdir -p $S/t202 && git archive f0921e4 | tar -x -C $S/t202 && ls $S/t202 | head -30",
 "description": "Extract f0921e4 archive into scratchpad"
}
````

### User / tool · 2026-11-02T23:37:31.960Z

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
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:33.520Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal && lsof -iTCP:7972 -sTCP:LISTEN -nP; echo exit $?",
 "description": "Create evidence dir and check port 7972 is free"
}
````

### User / tool · 2026-11-02T23:37:33.681Z

**tool result**
````
exit 1
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:37.766Z

**tool call — Bash**
````
{
 "command": "env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/db/zlayt.db PORT=7972 HOST=127.0.0.1 nohup .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/server.log 2>&1 &\necho started",
 "description": "Start archive app in demo mode on port 7972"
}
````

### User / tool · 2026-11-02T23:37:37.851Z

**tool result**
````
started
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:38.721Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-202-paralegal/db; git show f0921e4 -- app/backend/export.py app/backend/store.py app/backend/amounts.py",
 "description": "Read the backend diff in f0921e4"
}
````

### User / tool · 2026-11-02T23:37:38.848Z

**tool result**
````
commit f0921e4189f70a9dedb3d02cbb2201a734fda679
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 17:36:53 2026 -0600

    feat(backend): T-202 D-071 letter charge lines print the bill line's service date or period, not the statement date
    
    charge_basis returns the end of a stated period; store.charge_service_dates feeds dos_iso/dos_end_iso to the export; a period prints as a range (June 9-12, 2026); charges sort by service date; the T-200 statement-date form still applies when no service date is stated. evals/letter_check gains a count path and charge_date_violations (every dated charge line's date must be a service date its record states). case_09, lib14, lib10 letters change.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/amounts.py b/app/backend/amounts.py
index b33de7b..bab3f1d 100644
--- a/app/backend/amounts.py
+++ b/app/backend/amounts.py
@@ -432,14 +432,24 @@ def billing_document(source, excerpt: str = "") -> bool:
     return bool(_is_billing_source(source or "") or _BILLISH.search(source or "") or _BILL_OPEN.search(excerpt or ""))
 
 
+def _record_period(before: str, ref_iso):
+    """(first date, last date or None) of the date or period the record states for its services. D-071: the last date is the end of the range ('06/09/2026 to 06/12/2026'),
+    None for a single date ('the run of 09/14/2026')."""
+    ms = list(_DOS_RX.finditer(before))
+    for k, m in enumerate(ms):
+        iso = _dos_iso(m, ref_iso)
+        if iso and _PERIOD_PHRASE.search(before[max(0, m.start() - 40):m.start()]):
+            end = None
+            if k + 1 < len(ms) and _RANGE_JOIN.match(before[m.end():ms[k + 1].start()]):
+                end = _dos_iso(ms[k + 1], ref_iso)
+            return iso, (end if end and end > iso else None)
+    return None, None
+
+
 def _record_period_dos(before: str, ref_iso):
     """A coded line (CPT, HCPCS, revenue code) with no date of its own takes the date or period the record states for its services ('statement period
     06/09/2026 to 06/12/2026', 'the run of 09/14/2026'): the first date of that period."""
-    for m in _DOS_RX.finditer(before):
-        iso = _dos_iso(m, ref_iso)
-        if iso and _PERIOD_PHRASE.search(before[max(0, m.start() - 40):m.start()]):
-            return iso
-    return None
+    return _record_period(before, ref_iso)[0]
 
 
 def _tokens(text: str, strip) -> tuple:
@@ -465,7 +475,7 @@ def charge_basis(excerpt: str, amount: dict, source: str = None, date_iso: str =
     sentence for the internal notes when it is not (None when the figure just has no charge wording). `dos` (ISO date, or the record's date for a note),
     `tokens` and `codes` describe the service and feed the duplicate match, whether or not `ok`. `note_block` (note_charge_block) is the reason a clinical note or
     unknown document yields no charge; it only applies to the encounter-record branch."""
-    out = {"ok": False, "reason": None, "dos": None, "tokens": frozenset(), "codes": frozenset(), "svc": False}
+    out = {"ok": False, "reason": None, "dos": None, "dos_end": None, "tokens": frozenset(), "codes": frozenset(), "svc": False}
     amts = find_amounts(excerpt or "")
     i = next((n for n, a in enumerate(amts) if a["start"] == amount["start"]), None)
     if i is None or amount.get("cents") is None:
@@ -519,7 +529,7 @@ def charge_basis(excerpt: str, amount: dict, source: str = None, date_iso: str =
                 out.update(reason=_SECOND_WHY, dos=dos)
                 return out
         if dos is None and coded:
-            dos = _record_period_dos(excerpt[:se], date_iso)
+            dos, out["dos_end"] = _record_period(excerpt[:se], date_iso)          # D-071: a period keeps its end date for the letter
         out["dos"] = dos
         if dos is None:
             out["reason"] = _NO_DATE_WHY
diff --git a/app/backend/export.py b/app/backend/export.py
index 5c469d8..0f647e0 100644
--- a/app/backend/export.py
+++ b/app/backend/export.py
@@ -70,6 +70,18 @@ def _long_date(iso):
     return f"{d.strftime('%B')} {d.day}, {d.year}"
 
 
+def _date_range(first, last=None):
+    """'June 9, 2026' for one day; a period as a range: 'June 9\u201312, 2026', 'June 28\u2013July 2, 2026', 'December 30, 2026\u2013January 2, 2027' (D-071)."""
+    if not last or last == first:
+        return _long_date(first)
+    a, b = date.fromisoformat(first), date.fromisoformat(last)
+    if (a.year, a.month) == (b.year, b.month):
+        return f"{a.strftime('%B')} {a.day}\u2013{b.day}, {a.year}"
+    if a.year == b.year:
+        return f"{a.strftime('%B')} {a.day}\u2013{b.strftime('%B')} {b.day}, {a.year}"
+    return f"{_long_date(first)}\u2013{_long_date(last)}"
+
+
 def _money(cents):
     return f"${cents // 100:,}.{cents % 100:02d}"
 
@@ -168,8 +180,9 @@ class _View:
 
     @property
     def in_charges(self):
-        return [a for a in self.amounts if a["cls"] == "charge" and a.get("cents") is not None
-                and _status(a) == "in" and self.verbatim(a)]
+        """D-071: in the order of the service dates the letter prints (a charge with no stated date sorts by its statement date)."""
+        got = [a for a in self.amounts if a["cls"] == "charge" and a.get("cents") is not None and _status(a) == "in" and self.verbatim(a)]
+        return sorted(got, key=lambda a: (a.get("dos_iso") or self._date(a), a["record_no"], str(a.get("id"))))
 
     def _date(self, item):
         return self.date_of(item) or "9999-12-31"
@@ -207,13 +220,17 @@ class _View:
         return (self.records.get(n) or {}).get("date_iso")
 
     def charge_when(self, a):
-        """T-200 (GATE-M2 r2 paralegal major): the label before a charge's amount in the letter. A bare date there reads as the date of service. A charge whose own line states
-        none (`dos_stated` False, store.charge_dos_stated) is NEVER given the record's date bare: that date is the statement's, and the label says so and says the service date is
-        not stated: 'Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated)'. Chosen over dropping the date because the adjuster can still
-        match the line to the ledger page, and it agrees with the review screen's 'No date of service (statement dated ...)'. A case dict without the key keeps the record's date."""
-        n, src, rd = a["record_no"], self.source(a["record_no"]), self.rec_date(a["record_no"])
-        if a.get("dos_stated", True):
-            return f"{src}, {_long_date(rd)}"
+        """D-071 (extends T-200): the label before a charge's amount in the letter. A date there reads as the date of service, so it is the service date the charge's own bill line
+        states (store.charge_service_dates; a period prints as a range, `_date_range`), never the record's date, which for a bill is the statement's. A line that states none is
+        NEVER given the record's date bare: 'Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated)'. Chosen over dropping the date
+        because the adjuster can still match the line to the ledger page, and it agrees with the review screen's 'No date of service (statement dated ...)'. A case dict
+        without `dos_iso` (a hand-built one) keeps the record's date."""
+        n, src = a["record_no"], self.source(a["record_no"])
+        if "dos_iso" not in a:
+            return f"{src}, {_long_date(self.rec_date(n))}"
+        if a["dos_iso"]:
+            return f"{src}, {_date_range(a['dos_iso'], a.get('dos_end_iso'))}"
+        rd = self.rec_date(n)
         return f"{src} (statement dated {_long_date(rd)}; service date not stated)" if rd else f"{src} (service date not stated)"
 
     def cite(self, n):
diff --git a/app/backend/store.py b/app/backend/store.py
index f8bf23e..c869fa0 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -115,14 +115,17 @@ def amount_pos(item: dict, rec):
     return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None
 
 
-def charge_dos_stated(item: dict, rec, pos) -> bool:
-    """T-200: does the charge's OWN line state a date of service (or, for a note, is the record the encounter)? False for a ledger line with none: the record's date is then the
-    statement's, which the letter must not print as if it were a service date. A charge the paralegal counted for a missing date of service (D-064) is False by definition.
-    Code only: amounts.charge_basis reads the line. When the line cannot be read it is True unless she counted it for that reason (the letter then keeps the record's date as before)."""
+def charge_service_dates(item: dict, rec, pos) -> tuple:
+    """D-071 (extends T-200): (first, last) ISO date of service the charge's OWN bill line states, `last` None for a single day; (None, None) when the line states none. The
+    record's date of a ledger, invoice or UB-04 is the statement's, never a service date, so it is not the fallback for a billing document. A dated encounter record's date is
+    the visit. A charge the paralegal counted for a missing date of service (D-064) is (None, None). Code only: amounts.charge_basis reads the line.
+    When the line cannot be read: the record's date, unless she counted it for the missing date."""
     from app.backend import amounts as AM          # lazy: keep the import graph as it was
     if rec is None or pos is None or not item.get("excerpt"):
-        return ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") != AM.NO_DATE_WHY
-    return AM.charge_basis(item["excerpt"], {"start": pos, "cents": item.get("value_cents")}, rec.get("source"), rec.get("date_iso")).get("dos") is not None
+        counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
+        return (None, None) if counted_undated else ((rec or {}).get("date_iso"), None)
+    b = AM.charge_basis(item["excerpt"], {"start": pos, "cents": item.get("value_cents")}, rec.get("source"), rec.get("date_iso"))
+    return b.get("dos"), (b.get("dos_end") if b.get("dos") else None)
 
 
 def export_case(conn, case_id: str, blockers: bool = True) -> dict:
@@ -169,7 +172,7 @@ def export_case(conn, case_id: str, blockers: bool = True) -> dict:
         d = dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
                  excerpt=a["excerpt"], review_status=a["review_status"], pos=amount_pos(a, r))
         if a["kind"] == "charge":
-            d["dos_stated"] = charge_dos_stated(a, r, d["pos"])
+            d["dos_iso"], d["dos_end_iso"] = charge_service_dates(a, r, d["pos"])
         amts.append(d)
     fl = []
     for f in DB.list_items(conn, case_id, "flag"):
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:40.900Z

**tool call — Bash**
````
{
 "command": "curl -s -m 5 http://127.0.0.1:7972/api/health; echo; ls evals/golden | head -50; ls evals/golden/library 2>/dev/null | head -40",
 "description": "Health check and list golden cases"
}
````

### User / tool · 2026-11-02T23:37:41.027Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
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
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:42.530Z

**tool call — Bash**
````
{
 "command": "cat evals/golden/case_09_nonvisit_hides_gap.txt; ls evals/ ; ls evals/library 2>/dev/null | head -40",
 "description": "Read case_09 records and list evals dirs"
}
````

### User / tool · 2026-11-02T23:37:42.616Z

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

__init__.py
__pycache__
adversarial
finalize_prompt_log.py
golden
heldout_audit.py
j3_controls.py
letter_check.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
privacy_tree_scan.py
reports
run.py
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

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:44.193Z

**tool call — Bash**
````
{
 "command": "cat evals/library/case_lib10_eob_ub04_cms1500.txt; echo =========; cat evals/library/case_lib14_handwritten_chiro_scans.txt",
 "description": "Read lib10 and lib14 records"
}
````

### User / tool · 2026-11-02T23:37:44.279Z

**tool result**
````
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-06-09
Source: Rainhollow Fire-Rescue run report
Excerpt: "Driver of a pickup struck at an intersection. Pt states chest wall and left knee pain. Ambulatory at scene. Transported to Saltmarrow General Hospital."

=== Record 2 ===
Date: 2026-06-09
Source: Saltmarrow General Hospital ED
Excerpt: "Dx: left knee contusion, chest wall contusion. X-ray left knee negative for fracture. Admitted for observation."

=== Record 3 ===
Date: 2026-06-12
Source: Saltmarrow General Hospital, discharge summary
Excerpt: "Discharged after 3 days of observation. Dx: left knee contusion. Follow up with orthopedics."

=== Record 4 ===
Date: 2026-06-19
Source: Saltmarrow General Hospital, UB-04 itemized bill
Excerpt: "UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0120 room and board semi-private, FL44 rate $1,640.00 per day, FL46 3 days, FL47 total charges $4,920.00. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00. Rev 0250 pharmacy, 14 units, FL47 total charges $386.50. Rev 0300 laboratory, 6 units, FL47 total charges $712.00. Rev 0001 total charges $8,123.50."

=== Record 5 ===
Date: 2026-06-24
Source: Dr. Ignatius Wardlaw, orthopedics, new patient
Excerpt: "Left knee pain 5/10. MRI left knee ordered. Patient states his health plan was billed for the hospital stay."

=== Record 6 ===
Date: 2026-07-03
Source: Quoinmere Mutual Health Plan, EOB
Excerpt: "Explanation of benefits, processed 07/03/2026, for dates of service 06/09/2026 to 06/12/2026. This is not a bill. Amount billed $8,023.50; network discount $3,610.00; allowed amount $4,413.50; plan paid $3,530.80; you may owe $882.70."

=== Record 7 ===
Date: 2026-07-08
Source: Dr. Ignatius Wardlaw, orthopedics, follow-up
Excerpt: "Left knee pain 3/10. Injection performed. Continue home exercises."

=== Record 8 ===
Date: 2026-07-14
Source: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)
Excerpt: "OCR of scanned CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, 18500, 1 unit; CPT 20610, 21000, 1 unit; CPT 97110, 96 OO, 4 units. Item 28 TOTAL CHARGE 49100. Item 29 AMOUNT PAID 0 00."

=== Record 9 ===
Date: 2026-08-26
Source: Dr. Ignatius Wardlaw, orthopedics, follow-up
Excerpt: "Left knee pain 2/10. Discharged from care."
=========
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-09-14
Source: Tarnwick Fire-Rescue run report
Excerpt: "Driver of a sedan struck from behind. Moderate damage to the rear of the vehicle. Pt ambulatory at scene. Pt states neck pain 6/10 and tingling in the right hand. Cervical collar applied. Transported to Orrin Mere Regional ED."

=== Record 2 ===
Date: 2026-09-14
Source: Orrin Mere Regional ED
Excerpt: "Dx: cervical strain. X-ray cervical spine negative for fracture. Discharged with a muscle relaxant. ED charge: $2,960."

=== Record 3 ===
Date: 2026-09-21
Source: Hollowbrook Chiropractic, daily note visit 1 (scanned, OCR text)
Excerpt: "Pain 7 circled on a 0-10 scale. Tenderness at C4-C6. [X] adjustment [X] e-stim [X] hot pack. Date written 9/2l/26."

=== Record 4 ===
Date: 2026-10-06
Source: Hollowbrook Chiropractic, daily note visit 9 (scanned, OCR text)
Excerpt: "Pain 5 circled. Tenderness at C4-C5, improved. [X] adjustment [X] e-stim. Next visit 1O/2O."

=== Record 5 ===
Date: 10/20
Source: Hollowbrook Chiropractic, daily note visit 12 (handwritten, OCR text)
Excerpt: "Pain 4 circled. Adjusted C4-C6. [X] e-stim. Pt states neck feels better."

=== Record 6 ===
Date: 2026-11-03
Source: Hollowbrook Chiropractic, re-examination (typed)
Excerpt: "Re-examination. Pain 6/10, unchanged from the initial visit. Plan: continue care three times weekly."

=== Record 7 ===
Date: 2026-11-10
Source: Hollowbrook Chiropractic, CMS-1500 (OCR of scanned claim)
Excerpt: "OCR of scanned CMS-1500. Item 14 injury date 091426 qualifier 431. Line 1: 092126 to 092326, CPT 98941, 24F 25500, 24G 3. Line 2: 092126 to 092326, CPT 97014, 24F 7500, 24G 3. Item 28 TOTAL CHARGE 33000. Item 29 AMOUNT PAID 0 00. Item 31 signature date 110926."

=== Record 8 ===
Date: 2026-11-12
Source: Tarnwick Fire-Rescue, ambulance invoice
Excerpt: "Invoice for the run of 09/14/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00. A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05. Total charges $1,567.05. No payments posted. Letter of protection requested."
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:37:57.141Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/pytest-t202.out 2>&1; tail -3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/pytest-t202.out",
 "description": "Run T-202 and T-200 unit tests from archive"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:38:00.784Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.letter_check > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/letter_check.out 2>&1; echo exit $?; tail -40 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/letter_check.out",
 "description": "Run letter_check eval from archive"
}
````

### User / tool · 2026-11-02T23:38:03.266Z

**tool result**
````
...................                                                      [100%]
19 passed in 5.78s
````

### User / tool · 2026-11-02T23:38:14.680Z

**tool result**
````
exit 0
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:38:16.314Z

**tool call — Bash**
````
{
 "command": "git show f0921e4 -- evals/letter_check.py | head -220",
 "description": "Read letter_check diff"
}
````

### User / tool · 2026-11-02T23:38:16.444Z

**tool result**
````
commit f0921e4189f70a9dedb3d02cbb2201a734fda679
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 17:36:53 2026 -0600

    feat(backend): T-202 D-071 letter charge lines print the bill line's service date or period, not the statement date
    
    charge_basis returns the end of a stated period; store.charge_service_dates feeds dos_iso/dos_end_iso to the export; a period prints as a range (June 9-12, 2026); charges sort by service date; the T-200 statement-date form still applies when no service date is stated. evals/letter_check gains a count path and charge_date_violations (every dated charge line's date must be a service date its record states). case_09, lib14, lib10 letters change.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/evals/letter_check.py b/evals/letter_check.py
index b63e6ee..3152c07 100644
--- a/evals/letter_check.py
+++ b/evals/letter_check.py
@@ -11,6 +11,9 @@ Violations (all must be zero):
 T-139 round 4: the audit uses the SAME detector as the charge-text hold and the export gate (app/backend/money.py), so the three cannot diverge: a wording one holds, all hold.
 The eval's independent value is the walk (every case, every style, charges dismissed) and the structure checks (charges section, total line, bills to request), not a
 second regex. It also reports the export gate: a case whose letter the gate blocks is a violation.
+D-071 / T-202: a third variant counts every countable amount (the paralegal's D-064 "Count this charge", with the named confirms) after accepting everything, and every dated charge
+line of every letter is checked against its record (`charge_date_violations`): the date in the line (a day or a range) must be a service date the record states for the quote (a
+statement, billing or due date never is; a visit note's own date is), and a line headed 'statement dated X; service date not stated' must carry a quote with no date and X must be the record's date.
 Pure check: `violations(letter, accepted_cents)`; the pipeline walk is `letters_for(text)`.
 
     python -m evals.letter_check            prints one line per case and exits 1 on any violation
@@ -100,17 +103,128 @@ def _walk(conn, cid, dismiss_charges=False):
     return cents, refused
 
 
+def _count_all(conn, cid):
+    """D-064 count path: count every amount the code held back for a missing detail, naming the confirm (and the duplicate / total flag when the code asks for it); an uncountable one is
+    skipped. Returns the cents of every accepted charge after that."""
+    from app.backend import count_charge, review
+    from app.db import db as DB
+    for it in DB.list_items(conn, cid, "amount"):
+        if it["state"] == "rejected" or it["kind"] == "charge":
+            continue
+        body = {"confirm": count_charge.CONFIRM}
+        for _ in range(2):
+            try:
+                count_charge.count(conn, cid, it["id"], dict(body))
+                break
+            except review.ReviewError as e:
+                want = (e.detail or {}).get("confirm_with")
+                if e.code == "CONFIRM_REQUIRED" and want and want != count_charge.CONFIRM and "confirm_flag" not in body:
+                    body["confirm_flag"] = want
+                    continue
+                break
+    return [it["value_cents"] for it in DB.list_items(conn, cid, "amount")
+            if it["kind"] == "charge" and it["review_status"] in ("accepted", "edited") and it.get("value_cents") is not None and it["state"] != "rejected"]
+
+
+_MON = "January|February|March|April|May|June|July|August|September|October|November|December"
+_D = rf"(?:{_MON})\s+\d{{1,2}}"
+_HEAD_DATES = [(re.compile(rf"({_D},\s+\d{{4}})\u2013({_D},\s+\d{{4}})$"), "full"), (re.compile(rf"({_D})\u2013({_D}),\s+(\d{{4}})$"), "month"),
+               (re.compile(rf"({_D})\u2013(\d{{1,2}}),\s+(\d{{4}})$"), "day"), (re.compile(rf"({_D},\s+\d{{4}})$"), "one")]
+_STATEMENT_FORM = re.compile(r"\(statement dated ([^;)]+); service date not stated\)$")
+_NO_DATE_FORM = re.compile(r"\(service date not stated\)$")
+_STATEMENT_LEAD = re.compile(r"(?:(?:statement|billing|bill|invoice|printed|posted|mailed|issued)\s+date|\bdue(?:\s+date)?|as[\s-]of|balance|payment)\s*[:#]?\W{0,8}(?:of|on)?\W{0,3}$", re.IGNORECASE)          # a 'statement PERIOD' is the service period of a UB-04
+
+
+def _iso(txt):
+    from datetime import datetime
+    return datetime.strptime(" ".join(txt.replace(",", " ").split()), "%B %d %Y").date().isoformat()
+
+
+def _head_dates(head: str):
+    """('range'|'one', first ISO, last ISO or None) from the end of a charge header, or ('statement', ISO, None) / ('none', None, None) for the T-200 forms, or None when unreadable."""
+    m = _STATEMENT_FORM.search(head)
+    if m:
+        return "statement", _iso(m.group(1)), None
+    if _NO_DATE_FORM.search(head):
+        return "none", None, None
+    for rx, kind in _HEAD_DATES:
+        m = rx.search(head)
+        if not m:
+            continue
+        g = m.groups()
+        if kind == "full":
+            return "range", _iso(g[0]), _iso(g[1])
+        if kind == "month":
+            return "range", _iso(f"{g[0]}, {g[2]}"), _iso(f"{g[1]}, {g[2]}")
+        if kind == "day":
+            return "range", _iso(f"{g[0]}, {g[2]}"), _iso(f"{g[0].split()[0]} {g[1]}, {g[2]}")
+        return "one", _iso(g[0]), None
+    return None
+
+
+def charge_lines(letter: str) -> list:
+    """[(header, quote)] of the BILLED CHARGES section, by structure (a header ends ': $X.XX'; the next line is its Source line)."""
+    from app.backend import export
+    _, tail = export.split_letter(letter)
+    out = []
+    for i, line in enumerate(tail):
+        if re.search(r": \$[\d,]+\.\d\d$", line) and not line.startswith(TOTAL) and i + 1 < len(tail):
+            q = tail[i + 1]
+            out.append((line, q[q.index('"') + 1:q.rindex('"')] if '"' in q else q))
+    return out
+
+
+def charge_date_violations(letter: str, records) -> list:
+    """D-071: every dated charge line's date must be a date of service its record states for the quote. `records`: the case's [{n, source, date_iso, excerpt}]. A date led by a
+    statement, billing, due or as-of word is never a service date; a visit note (not a bill) is the visit's date. The T-200 form must carry the record's date and a quote with no date."""
+    from app.backend import amounts as AM
+    import re as _re
+    norm = lambda t: " ".join(str(t).split())
+    out = []
+    for head, quote in charge_lines(letter):
+        parsed = _head_dates(re.sub(r": \$[\d,]+\.\d\d$", "", head))
+        recs = [r for r in records if norm(quote) and norm(quote) in norm(r["excerpt"])]
+        if parsed is None:
+            out.append(f"charge line has no readable date form: {head}")
+            continue
+        if not recs:
+            out.append(f"charge line's quote is in no record: {head}")
+            continue
+        kind, first, last = parsed
+        ok = False
+        for r in recs:
+            ex, rd, bill = r["excerpt"], r.get("date_iso"), AM.billing_document(r.get("source"), r["excerpt"])
+            states = {}
+            for m in AM._DOS_RX.finditer(ex):
+                iso = AM._dos_iso(m, rd)
+                if iso:
+                    states[iso] = not _STATEMENT_LEAD.search(ex[max(0, m.start() - 30):m.start()])          # False: led by a statement / billing / due word
+            service = {d for d, good in states.items() if good}
+            if not bill and rd:
+                service.add(rd)
+            if kind in ("statement", "none"):
+                quote_dates = [1 for m in AM._DOS_RX.finditer(quote) if AM._dos_iso(m, rd)]
+                ok = ok or (not quote_dates and (kind == "none" or first == rd) and (bill or not rd))
+            else:
+                ok = ok or (first in service and (last is None or last in states))
+        if not ok:
+            out.append(f"charge line's date is not a service date its record states: {head}")
+    return out
+
+
 def letters_for(text: str, backend: str = "fixture") -> dict:
     """{'all_accepted': {...}, 'charges_dismissed': {...}}, each {'letters': {style: text}, 'notes': str, 'charge_cents': [...], 'refused': [(id, code)], 'gate': {style: [why...]}}."""
     from app.backend import export, ingest as IN, pipeline as PL, store
     from app.llm import provider as P
     out = {}
-    for variant, dismiss in (("all_accepted", False), ("charges_dismissed", True)):
+    for variant, dismiss in (("all_accepted", False), ("charges_dismissed", True), ("counted", False)):
         with PL._Backend(backend), tempfile.TemporaryDirectory() as tmp:
             conn, cid, call = PL._scratch_call(tmp, IN.normalize_text(text))
             with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
                 PL.run_pipeline(conn, cid, text, call=call)
             cents, refused = _walk(conn, cid, dismiss)
+            if variant == "counted":
+                cents = _count_all(conn, cid)
             case = store.export_case(conn, cid)
             case["judge_not_run"] = []          # this check reads the letter text only; the second-check gate is a separate rule (D-044)
             built, gate = {}, {}
@@ -125,7 +239,7 @@ def letters_for(text: str, backend: str = "fixture") -> dict:
             dismissed = sorted({src[a["record_no"]].split(",", 1)[0].strip() for a in case["amounts"] if a["cls"] == "charge" and a["review_status"] == "dismissed"})
             conn.close()
         out[variant] = {"letters": {k: v["letter_text"] for k, v in built.items()}, "notes": built["standard"]["internal_notes_text"],
-                        "charge_cents": cents, "refused": refused, "dismissed_providers": dismissed, "gate": gate}
+                        "charge_cents": cents, "refused": refused, "records": case["records"], "dismissed_providers": dismissed, "gate": gate}
     return out
 
 
@@ -146,7 +260,12 @@ def measure(case_list=None, backend: str = "fixture") -> dict:
             bad += [f"{style}: {v}" for v in violations(letter, got["all_accepted"]["charge_cents"])]
         for style, letter in got["charges_dismissed"]["letters"].items():
             bad += [f"{style} (charges dismissed): {v}" for v in violations(letter, (), expect_none=True)]
-        for variant in ("all_accepted", "charges_dismissed"):
+        for style, letter in got["counted"]["letters"].items():
+            bad += [f"{style} (counted): {v}" for v in violations(letter, got["counted"]["charge_cents"])]
+        for variant in ("all_accepted", "counted"):
+            for style, letter in got[variant]["letters"].items():
+                bad += [f"{style} ({variant}): {v}" for v in charge_date_violations(letter, got[variant]["records"])]
+        for variant in ("all_accepted", "charges_dismissed", "counted"):
             bad += [f"{style} ({variant}): the export gate blocked this letter: {w}" for style, whys in got[variant]["gate"].items() for w in whys]
         bad += [f"dismissed charge's provider {p} is under BILLS TO REQUEST" for p in dismissed_in_bills(got["charges_dismissed"]["notes"], got["charges_dismissed"]["dismissed_providers"])]
         held += sum(1 for _, code in got["all_accepted"]["refused"] if code == "CHARGE_TEXT_IN_ENTRY")
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:38:25.306Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/letters_dump.py",
 "content": "\"\"\"T-202 paralegal: dump the standard letter + notes for each letter_check variant (all_accepted, counted) for sample, case_09, lib14, lib10,\nfrom a git-archive copy of f0921e4. Run from repo root:\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/letters_dump.py <archive_root> <out_dir>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nout = os.path.abspath(sys.argv[2])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom evals import letter_check as LC  # noqa: E402\n\nCASES = {\n    \"sample\": \"evals/golden/sample.txt\",\n    \"case_09\": \"evals/golden/case_09_nonvisit_hides_gap.txt\",\n    \"lib14\": \"evals/library/case_lib14_handwritten_chiro_scans.txt\",\n    \"lib10\": \"evals/library/case_lib10_eob_ub04_cms1500.txt\",\n}\nfor name, path in CASES.items():\n    got = LC.letters_for(open(path).read())\n    for variant in (\"all_accepted\", \"counted\"):\n        v = got[variant]\n        with open(os.path.join(out, f\"{name}-{variant}-letter.txt\"), \"w\") as f:\n            f.write(v[\"letters\"][\"standard\"])\n        with open(os.path.join(out, f\"{name}-{variant}-notes.txt\"), \"w\") as f:\n            f.write(v[\"notes\"])\n        lines = LC.charge_lines(v[\"letters\"][\"standard\"])\n        viol = LC.charge_date_violations(v[\"letters\"][\"standard\"], v[\"records\"])\n        print(f\"== {name} {variant}: cents={v['charge_cents']} refused={v['refused']} gate={v['gate']}\")\n        for h, q in lines:\n            print(\"   \", h, \"|\", q)\n        print(\"    violations:\", viol)\n"
}
````

### User / tool · 2026-11-02T23:38:25.408Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/letters_dump.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:38:29.679Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/letters_dump.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/letters_dump.out 2>&1; echo exit $?; cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/letters_dump.out",
 "description": "Dump letters per variant for four cases"
}
````

### User / tool · 2026-11-02T23:38:32.504Z

**tool result**
````
exit 0
== sample all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    violations: []
== sample counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    violations: []
== case_09 all_accepted: cents=[27500] refused=[('e2', 'CHARGE_TEXT_IN_ENTRY')] gate={}
    Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00 | Statement for visit of 2026-02-02: $275.
    violations: []
== case_09 counted: cents=[27500] refused=[('e2', 'CHARGE_TEXT_IN_ENTRY')] gate={}
    Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00 | Statement for visit of 2026-02-02: $275.
    violations: []
== lib14 all_accepted: cents=[296000, 138000, 18705] refused=[('e7', 'CHARGE_TEXT_IN_ENTRY'), ('e8', 'CHARGE_TEXT_IN_ENTRY'), ('e5', 'DATE_UNCONFIRMED'), ('a5', 'COMPARE_REQUIRED')] gate={}
    Orrin Mere Regional ED, September 14, 2026: $2,960.00 | ED charge: $2,960.
    Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00 | A0427 ALS emergency transport, 1 unit, charge $1,380.00.
    Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05 | charge $187.05.
    violations: []
== lib14 counted: cents=[296000, 138000, 18705] refused=[('e7', 'CHARGE_TEXT_IN_ENTRY'), ('e8', 'CHARGE_TEXT_IN_ENTRY'), ('e5', 'DATE_UNCONFIRMED'), ('a5', 'COMPARE_REQUIRED')] gate={}
    Orrin Mere Regional ED, September 14, 2026: $2,960.00 | ED charge: $2,960.
    Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00 | A0427 ALS emergency transport, 1 unit, charge $1,380.00.
    Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05 | charge $187.05.
    violations: []
== lib10 all_accepted: cents=[492000, 210500, 38650, 71200] refused=[('e1', 'COMPARE_REQUIRED'), ('e4', 'COMPARE_REQUIRED'), ('e8', 'CHARGE_TEXT_IN_ENTRY'), ('a6', 'COMPARE_REQUIRED'), ('a7', 'COMPARE_REQUIRED'), ('a9', 'COMPARE_REQUIRED'), ('a11', 'COMPARE_REQUIRED')] gate={}
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00 | FL47 total charges $4,920.00.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00 | Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $386.50 | Rev 0250 pharmacy, 14 units, FL47 total charges $386.50.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $712.00 | Rev 0300 laboratory, 6 units, FL47 total charges $712.00.
    violations: []
== lib10 counted: cents=[492000, 210500, 38650, 71200] refused=[('e1', 'COMPARE_REQUIRED'), ('e4', 'COMPARE_REQUIRED'), ('e8', 'CHARGE_TEXT_IN_ENTRY'), ('a6', 'COMPARE_REQUIRED'), ('a7', 'COMPARE_REQUIRED'), ('a9', 'COMPARE_REQUIRED'), ('a11', 'COMPARE_REQUIRED')] gate={}
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00 | FL47 total charges $4,920.00.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00 | Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $386.50 | Rev 0250 pharmacy, 14 units, FL47 total charges $386.50.
    Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $712.00 | Rev 0300 laboratory, 6 units, FL47 total charges $712.00.
    violations: []
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:38:53.021Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && sed -n 95,120p app/backend/store.py; grep -n -i \"manual\\|split\" memory/contracts/api.md | head -30",
 "description": "Read amount_pos and manual/split API notes"
}
````

### User / tool · 2026-11-02T23:38:53.126Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:38:56.836Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && grep -n -i \"manual\" memory/contracts/api.md | cut -c1-220 | head -20; grep -rn \"excerpt_start\" app/backend/*.py | grep -v \"^app/backend/store.py\" | cut -c1-200 | head -30",
 "description": "Find manual amount API and excerpt_start writers"
}
````

### User / tool · 2026-11-02T23:38:56.984Z

**tool result**
````
9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `r
27:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with
109:**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, edit, manual entry, 
134:`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: th
143:**T-143 (round 2), `records[].uncovered[]` (GET case; review aid, code only):** EVERY sentence of the record that no live entry's excerpt overlaps, so a pain score, a chief complaint, a baseline-history line, a patie
380:- T-134 r3: `/judges` `totals.human_overrides` ("you accepted despite an objection") counts only her explicit accept; an open edit (`edit_to_check`) whose re-check objected stays in `rejections` and `totals.unsupport
417:**Flags that need a named confirm (D-059).** A charge can carry `flag` (else `null`): `{flag: "likely_duplicate" | "likely_total", name, message, confirm_with, of, confirmed_at?}` and `confirm_required: true` while i
603:**Judge rationale is a closed reason code plus a fixed sentence (D-028).** The judge returns `verdict` + `reason_code` from a closed list, never prose, so `rationale` is the fixed sentence for that code (`why.judge_d
683:`verdict.code` for the case: `ready` (export gate open), `needs_attention` (nothing accepted yet, or accepted items not double-checked), `running`, `failed`. The judge's closed `reason_code` is now kept in `ladder.ju
685:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `b
755:      "dos": "06/10/26", "dos_iso": "2026-06-10", "posted": "06/11/26", "code": "97140", "description": "Manual therapy x1",
759:      "excerpt": "06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00",   // the printed line, verbatim
786:- **Entry field `translation`** (every entry view; `null` for English records): `{source_language: "es", source_language_name: "Spanish", label: "AI translation", summary_is_translation: true, quote_is_original: true
787:- **Never auto-verified (D-050).** Every item (entry, amount, flag) made from a record routed `es` or `uncertain` is `needs_review` with reason `AI_TRANSLATION` ("AI translation — check against the original"), what
797:Before judge 1, code (`app/backend/summary_trim.py`) splits each AI summary into clauses (`;` `,` sentence-ending `.` and the join ` and `; ` with ` is not a boundary, so `Neck pain consistent with sprain.` is one cl
app/backend/present.py:59:            "excerpt": ed.get("excerpt", row["excerpt"]), "excerpt_start": ed.get("excerpt_start", row["excerpt_start"]),
app/backend/present.py:148:            "kind": row["kind"], "excerpt": row["excerpt"], "excerpt_start": row["excerpt_start"], "excerpt_end": row["excerpt_end"],
app/backend/present.py:536:            hs, he = item.get("excerpt_start"), item.get("excerpt_end")
app/backend/generator.py:68:        e.update(summary="", excerpt="", excerpt_start=None, excerpt_end=None, source_kind="record")
app/backend/generator.py:142:             excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None,
app/backend/generator.py:189:    e.update(ai_drafted=False, summary=None, excerpt=None, excerpt_start=None, excerpt_end=None, source_kind="record", state="rejected", reasons=[failure], why=why.why(fai
app/backend/overlap.py:134:        if rec is None or a["excerpt_start"] is None:
app/backend/overlap.py:139:                     "label": AM._label(raw, a["excerpt_start"]).replace("Excerpt:", "").strip(' "'), "after": _clause_after(raw, a["excerpt_end"]),
app/backend/reclassify.py:63:    if rec is not None and row.get("excerpt_start") is not None:
app/backend/reclassify.py:64:        i = row["excerpt_start"] - generator.body_offset(rec)
app/backend/pipeline.py:214:                "summary": it.get("summary"), "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"),
app/backend/pipeline.py:218:                "kind": it["cls"], "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"), "excerpt_end": it.get("excerpt_end"),
app/backend/pipeline.py:417:    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
app/backend/review.py:527:                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
app/backend/review.py:764:        "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
app/backend/trace.py:404:    return _span(cx, rid, ed.get("excerpt_start", row.get("excerpt_start")), ed.get("excerpt_end", row.get("excerpt_end")), ed.get("excerpt", row.get("excerpt")))
app/backend/trace.py:641:    exc = _span(cx, rid, row.get("excerpt_start"), row.get("excerpt_end"), row.get("excerpt"))
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:01.818Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && sed -n 495,535p app/backend/review.py",
 "description": "Read the amount edit code in review.py"
}
````

### User / tool · 2026-11-02T23:39:01.913Z

**tool result**
````
    cur_sum, cur_exc = prev.get("summary", item["summary"]), prev.get("excerpt", item["excerpt"])
    new_sum, new_exc = edits.get("summary", cur_sum).strip(), edits.get("excerpt", cur_exc).strip()
    trimmed = None
    summary_before_trim = new_sum
    if "summary" not in edits and charge_text.has_currency(new_sum) and not charge_text.has_currency(new_exc):
        tr = charge_text.trim_summary(new_sum)          # T-139: the quote she picked no longer states the amount; code removes the trailing amount clause (D-054 suffix rule)
        if tr["changed"] and not charge_text.has_currency(tr["text"]):
            new_sum, trimmed = tr["text"], tr
    span = None
    if "excerpt" in edits:
        problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], new_exc)
        if problems:
            raise _bad("The quote must be whole sentences of the same record, in order, with any hedge sentence that qualifies them.", reasons=problems)
    span = grounding.locate(rec["excerpt"], new_exc)
    base = generator.body_offset(rec)
    label, date_iso = item["provider"] or "", item["date_iso"] or ""
    from app.backend import present          # lazy: present imports review
    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call, prep=present.Prov(conn, case_id).prepared(item),      # D-069 r5: the warning follows the item's provenance
                         ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []),
                         bill_state=lambda: bill_state_for(conn, case_id, item.get("record_ids")))
    toks, code_reasons, ladder_verdict, call_id, state, reasons = (
        chk["toks"], chk["code_reasons"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
    edited = dict(prev)
    edited.update(at=store.iso(t))
    edited.pop("code_trim", None)           # T-139 r3: the trace shows the removal only while the wording it made is still the wording (a later hand edit or quote change clears it)
    if trimmed:
        edited["code_trim"] = {"rule": "T-139", "removed": list(trimmed["removed"]), "summary_before": summary_before_trim, "summary_after": new_sum,
                               "quote_before": cur_exc, "quote_after": new_exc}
    if "summary" in edits or "summary" in prev or trimmed:
        edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
    if "excerpt" in edits or "excerpt" in prev:
        edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
    set_review(conn, case_id, item["id"], "edit", edited=edited, now=t, kind="entry", item=item, recs=recs)     # D-051: edit implies accept; refused before any write
    lad = item.get("ladder") or {"item_id": item["id"]}
    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
        lad["pre_edit"] = {"judge": copy.deepcopy(lad.get("judge")), "code_checks": copy.deepcopy(lad.get("code_checks")), "rejudge": copy.deepcopy(lad.get("rejudge")),
                           "state": item["state"], "state_reasons": list(item.get("state_reasons") or []), "lad_state": lad.get("state")}      # deep copies: the edit updates code_checks in place below
    lad.pop("rejudge", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none
    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:06.278Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && grep -n \"^| \\(POST\\|PUT\\|PATCH\\|GET\\|DELETE\\)\" memory/contracts/api.md | cut -c1-200",
 "description": "List API endpoints from contract"
}
````

### User / tool · 2026-11-02T23:39:06.365Z

**tool result**
````
17:| GET | `/api/health` | backend, demo mode, models, limits, banner text |
18:| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
19:| GET | `/api/cases/{token}` | the whole case for the review screen |
20:| PATCH | `/api/cases/{token}` | T-157 rename: body `{title}` -> `{token, name, title}` |
21:| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
22:| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
23:| GET | `/api/cases/{token}/status` | stage and progress |
24:| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
25:| GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |
26:| POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |
27:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`42
28:| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry
29:| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked 
30:| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH);
31:| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
32:| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
33:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset, and (D-064) `count` + `confirm: "separate_charge"` for an amount held back only for a missing detail (see `count
34:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
35:| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. 
36:| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
37:| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next act
38:| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export)
39:| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
40:| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconc
41:| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
42:| GET | `/api/calibration` | T-099 read-only measured calibration (aggregate counts only, no case token, demo-safe): the T-096 shape in `calibration`, or `null` with `status` `missing`/`invalid`. S
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:10.999Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && grep -n -i \"reclassif\" memory/contracts/api.md | cut -c1-400 | head -12",
 "description": "Read reclassify contract notes"
}
````

### User / tool · 2026-11-02T23:39:11.147Z

**tool result**
````
32:| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
109:**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, edit, manual entry, not-a-duplicate split, reclassify, date confirmation or rejudge clears it (an edit of an OCR item stays `needs_review` with `OCR_DERIVED`, because the edit does not show that the p
351:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; its class changes only through `POST .../reclassify`, never through `edit`); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other ac
396:## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
400:- **Spanish cues (T-110 r2, code only, D-050).** The charged-amount wording also accepts `cargo`, `cargos`, `honorarios` and `estado de cuenta` in the figure's sentence (`detail.wording` / `reclassified.wording` carries the phrase). `sin cargo`, `no facturado` and similar negations refuse it, and so does `saldo` (a balance restates charges: counting it would count them twice). The shared rate-
401:- Same class as now: `200`, `reclassified: null`, nothing written.
402:- Anything not allowed: `422 reclassify_refused`, nothing changes, no event: `{error: {code, message, detail: {reason, check: "code"|"judge", wording?, error_class?}}}`. `detail.reason` is one of `NO_VALUE`, `INJECTION_SUSPECTED`, `NO_CHARGE_WORDING` (check `code`), `JUDGE_DISAGREES`, `JUDGE_UNSURE`, `JUDGE_UNAVAILABLE` (check `judge`; `JUDGE_UNAVAILABLE` includes no recorded answer in demo mo
404:- Audit: one `review_events` row per reclassification. The `action` is `edit` (the table's CHECK has no `reclassify` yet; db card requested) and the local-mode `after` payload carries `{event: "reclassify", kind, wording, judge_verdict, judge_call_id, restored, note}`, `before` carries `{kind, review_status, state}`. The judge call is in `llm_calls` with `item_id`. The item's `ladder.reclassif
411:              "ladder": { "reclassification": { "from": "rate", "to": "charge", "by": "reviewer", "wording": "Charge" }, "...": "..." } },
413:  "reclassified": { "from": "rate", "to": "charge", "wording": "Charge", "judge_verdict": "agree", "restored": false },
417:**Flags that need a named confirm (D-059).** A charge can carry `flag` (else `null`): `{flag: "likely_duplicate" | "likely_total", name, message, confirm_with, of, confirmed_at?}` and `confirm_required: true` while it is `pending`. `likely_duplicate`: set only when a paralegal PROMOTES a figure to a charge (reclassify, below) and it has the same normalized service date, service and amount as a
418:**Why an amount is not counted, and counting it (D-064, T-171; code only).** Every amount in `amounts[]` (case view, review responses, item view) carries `not_counted_reason` and `countable`. A charge has `not_counted_reason: null, countable: false` (accepting it counts it). Every other amount has a plain sentence, one per line, computed from the quote by code (`amounts.not_counted`), and `why
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:18.472Z

**tool call — Bash**
````
{
 "command": "curl -s -m 10 http://127.0.0.1:7972/api/library | python3 -m json.tool | grep -E '\"(id|token|name|title)\"' | head -40",
 "description": "List library cases on the archive app"
}
````

### User / tool · 2026-11-02T23:39:18.599Z

**tool result**
````
            "id": "case_lib01_er_only_then_gap",
            "name": "case lib01 er only then gap",
            "id": "case_lib02_slip_fall_prior_knee",
            "name": "case lib02 slip fall prior knee",
            "id": "case_lib03_truck_rear_end_chiro",
            "name": "case lib03 truck rear end chiro",
            "id": "case_lib04_dog_bite_scar_revision",
            "name": "case lib04 dog bite scar revision",
            "id": "case_lib05_pedestrian_orif_hardware",
            "name": "case lib05 pedestrian orif hardware",
            "id": "case_lib06_lop_billed_vs_adjusted",
            "name": "case lib06 lop billed vs adjusted",
            "id": "case_lib07_parking_lot_fall_outside_records",
            "name": "case lib07 parking lot fall outside records",
            "id": "case_lib08_second_crash_mri_after",
            "name": "case lib08 second crash mri after",
            "id": "case_lib09_spanish_interpreter_espalda",
            "name": "case lib09 spanish interpreter espalda",
            "id": "case_lib10_eob_ub04_cms1500",
            "name": "case lib10 eob ub04 cms1500",
            "id": "case_lib11_priors_and_ledger",
            "name": "case lib11 priors and ledger",
            "id": "case_lib12_records_review_credibility",
            "name": "case lib12 records review credibility",
            "id": "case_lib13_cloned_notes_cross_provider",
            "name": "case lib13 cloned notes cross provider",
            "id": "case_lib14_handwritten_chiro_scans",
            "name": "case lib14 handwritten chiro scans",
            "id": "case_lib15_conclusory_letter_mist",
            "name": "case lib15 conclusory letter mist",
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:23.289Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF' > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/case09-paste-probe.out 2>&1\nimport json, urllib.request\nt = open(\"/Users/arsis/zlayt-pm-project/evals/golden/case_09_nonvisit_hides_gap.txt\").read()\nfor body in ({\"text\": t}, {\"paste\": t}):\n    req = urllib.request.Request(\"http://127.0.0.1:7972/api/cases\", data=json.dumps(body).encode(), headers={\"Content-Type\": \"application/json\"}, method=\"POST\")\n    try:\n        r = urllib.request.urlopen(req, timeout=20); print(r.status, r.read()[:400])\n    except urllib.error.HTTPError as e:\n        print(e.code, e.read()[:600])\nEOF\ncat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/case09-paste-probe.out",
 "description": "Probe whether case_09 paste is accepted in demo"
}
````

### User / tool · 2026-11-02T23:39:23.541Z

**tool result**
````
201 b'{"token":"Lr7bynw0zxTFwO0yUf8hbQ","name":null,"title":"Hobbleton Family Clinic, visit, Feb 2, 2026","status":"ingested","source":"paste","demo_mode":true,"record_count":5,"split_method":"code","records":[{"id":"r1","seq":1,"source_label":"Hobbleton Family Clinic, visit","date_raw":"2026-02-02","date_iso":"2026-02-02","date_status":"parsed","date_candidates":[],"duplicate_of":null,"injection_tag":f'
400 b'{"error":{"code":"bad_request","message":"Provide text or sample: true.","detail":{}}}'
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:30.802Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && grep -rhoE 'data-testid=\"?(tile-[a-z-]+|btn-sample|btn-paste|paste-[a-z-]+|btn-load[a-z-]*|btn-read|input-text|paste)' app/frontend | sort -u | head -30",
 "description": "Find new-case page selectors"
}
````

### User / tool · 2026-11-02T23:39:30.905Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:35.238Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && ls app/frontend; grep -rhoE \"tile-[a-z-]+|btn-read|paste-text|btn-sample[a-z-]*\" app/frontend | sort -u | head -30",
 "description": "Find tile and paste selectors in frontend"
}
````

### User / tool · 2026-11-02T23:39:35.344Z

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
guided
index.html
input.js
judges.js
manual.js
mock.js
mock_extra.js
mock_flags.js
mock_sample.js
overview.css
overview.js
review.css
review.js
sections.js
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
tokens.css
uncovered.css
uncovered.js
btn-read
btn-sample
btn-sample-case
tile-file
tile-library
tile-paste
tile-sample
tile-why
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:40.347Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && grep -rn \"tile-paste\\|tile-sample\" app/frontend --include=*.js | cut -c1-250 | head; grep -rnoE \"data-testid=.?(paste[a-z-]*|input-[a-z]+|records-text)\" app/frontend --include=*.js | head",
 "description": "Find paste tile and textarea testids"
}
````

### User / tool · 2026-11-02T23:39:40.474Z

**tool result**
````
app/frontend/guided/step1.js:4:   Test ids: input-name, name-error, tile-paste, tile-file, tile-sample, tile-library, input-text, file-input, btn-choose-file, library-<id>, btn-read, btn-draft, btn-start-over, bar-msg, action-bar,
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:41.272Z

Now the Playwright helper and walk script.

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:42.563Z

**tool call — Bash**
````
{
 "command": "cp artifacts/review-evidence/T-200-paralegal/h.py artifacts/review-evidence/T-202-paralegal/h.py && grep -n \"7963\\|T-200\\|bd72d5b\" artifacts/review-evidence/T-202-paralegal/h.py",
 "description": "Copy Playwright helper for T-202"
}
````

### User / tool · 2026-11-02T23:39:42.661Z

**tool result**
````
1:"""T-200 paralegal review helper (copied from T-181 r2): persistent Chromium profile on the archive app (bd72d5b, demo/fixture, local mode, port 7963).
3:Usage: .venv/bin/python -I artifacts/review-evidence/T-200-paralegal/h.py <step-script.py>
11:BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7963")
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:39:44.659Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/h.py",
 "old_string": "BASE = os.environ.get(\"T181_BASE\", \"http://127.0.0.1:7963\")",
 "new_string": "BASE = os.environ.get(\"T181_BASE\", \"http://127.0.0.1:7972\")  # T-202: f0921e4 archive, port 7972"
}
````

### User / tool · 2026-11-02T23:39:44.764Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/h.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:40:01.150Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/p01_cases.py",
 "content": "\"\"\"T-202 paralegal: f0921e4 archive, demo/fixture backend, local mode, port 7972.\nFor each case (env CASES, default sample,case_09,lib14,lib10): open it as a user (sample tile / paste / library), draft, Step 2 accept with the\nkeyboard (compare box ticked where asked), Step 3 accept every bill item and tick 'count' boxes where offered, Step 4 download letter + notes.\nRun: .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/h.py artifacts/review-evidence/T-202-paralegal/p01_cases.py\n\"\"\"\nimport os\nimport re\n\nCASES = os.environ.get(\"CASES\", \"sample,case_09,lib14,lib10\").split(\",\")\nPASTE = {\"case_09\": \"/Users/arsis/zlayt-pm-project/evals/golden/case_09_nonvisit_hides_gap.txt\"}\nLIB = {\"lib14\": \"case_lib14_handwritten_chiro_scans\", \"lib10\": \"case_lib10_eob_ub04_cms1500\"}\n\n\ndef iid():\n    m = re.search(r\"item=([^&]+)\", pg.url)\n    return m.group(1) if m else None\n\n\ndef card():\n    return pg.evaluate(\"() => { const c = document.querySelectorAll('.work .card'); return c.length ? c[c.length-1].innerText : '' }\")\n\n\nfor name in CASES:\n    T0 = time.time()\n    pg.goto(BASE + \"/new\")\n    pg.wait_for_selector(\"[data-testid=view][data-ready]\")\n    if name == \"sample\":\n        pg.click(\"[data-testid=tile-sample]\")\n    elif name in PASTE:\n        pg.click(\"[data-testid=tile-paste]\")\n        pg.wait_for_timeout(300)\n        pg.fill(\"[data-testid=input-text]\", open(PASTE[name]).read())\n    else:\n        pg.click(\"[data-testid=tile-library]\")\n        pg.wait_for_timeout(300)\n        pg.check(f\"[data-testid=library-{LIB[name]}]\")\n    pg.wait_for_timeout(300)\n    pg.click(\"[data-testid=btn-read]\")\n    pg.wait_for_selector(\"[data-testid=btn-draft]\", timeout=20000)\n    pg.wait_for_timeout(300)\n    pg.click(\"[data-testid=btn-draft]\")\n    for i in range(120):\n        pg.wait_for_timeout(250)\n        if pg.query_selector(\"text=Go to step 2\") or \"/timeline\" in pg.url:\n            break\n    log(f\"[{name}] draft took\", round(time.time() - T0, 1), \"s\")\n    if \"/timeline\" not in pg.url:\n        pg.get_by_text(\"Go to step 2\").first.click()\n        pg.wait_for_selector(\"[data-testid=view][data-ready]\")\n    pg.wait_for_timeout(500)\n    # Step 2\n    for step in range(60):\n        i = iid()\n        if not i or \"/timeline\" not in pg.url:\n            break\n        yes = pg.query_selector(\"[data-testid=answer-yes]\")\n        yd = yes.is_disabled() if yes else None\n        cmp_box = pg.query_selector(\"[data-testid=check-compare]\")\n        radios = pg.query_selector_all(\"input[type=radio]\")\n        log(f\"[{name}] s2 item={i} yes_disabled={yd} compare={bool(cmp_box)} radios={len(radios)} :: {card().replace(chr(10), ' / ')[:300]}\")\n        if radios and pg.query_selector(\"button:has-text('Confirm date')\"):\n            radios[0].check(); pg.wait_for_timeout(200)\n            pg.get_by_role(\"button\", name=\"Confirm date\").click(); pg.wait_for_timeout(600)\n            log(f\"[{name}]   confirmed first date reading\")\n            continue\n        if cmp_box:\n            pg.keyboard.press(\"a\"); pg.wait_for_timeout(200)\n            pg.keyboard.press(\"Space\"); pg.wait_for_timeout(200)\n            pg.keyboard.press(\"a\")\n        elif yd:\n            pg.keyboard.press(\"d\")\n        else:\n            pg.keyboard.press(\"a\")\n        pg.wait_for_timeout(450)\n        if iid() == i:\n            pg.keyboard.press(\"j\"); pg.wait_for_timeout(300)\n            if iid() == i:\n                break\n    shot(f\"{name}-step2-done\", full=True)\n    if \"/timeline\" in pg.url:\n        pg.click(\"[data-testid=btn-next-step]\")\n        pg.wait_for_selector(\"[data-testid=view][data-ready]\")\n        pg.wait_for_timeout(500)\n    # Step 3\n    seen = {}\n    for step in range(40):\n        i = iid()\n        if not i or \"/bills\" not in pg.url:\n            break\n        seen[i] = seen.get(i, 0) + 1\n        if seen[i] > 3:\n            break\n        boxes = [b.get_attribute(\"data-testid\") for b in pg.query_selector_all(\"input[type=checkbox]\") if b.is_visible()]\n        log(f\"[{name}] s3 item={i} boxes={boxes} :: {card().replace(chr(10), ' / ')}\")\n        shot(f\"{name}-s3-{step:02d}-{i}\")\n        if boxes:\n            pg.keyboard.press(\"a\"); pg.wait_for_timeout(200)\n            for _ in boxes:\n                pg.keyboard.press(\"Space\"); pg.wait_for_timeout(200)\n                pg.keyboard.press(\"a\"); pg.wait_for_timeout(300)\n                if iid() != i:\n                    break\n        else:\n            pg.keyboard.press(\"a\")\n        pg.wait_for_timeout(450)\n    dump(f\"[{name}] step 3 done\")\n    shot(f\"{name}-step3-done\", full=True)\n    pg.get_by_text(\"Go to step 4\").first.click()\n    pg.wait_for_selector(\"[data-testid=letter-text]\", timeout=15000)\n    pg.wait_for_timeout(600)\n    with pg.expect_download() as d:\n        pg.click(\"[data-testid=btn-download-letter]\")\n    d.value.save_as(f\"{OUT}/ui-{name}-letter.txt\")\n    with pg.expect_download() as d2:\n        pg.click(\"[data-testid=btn-download-notes]\")\n    d2.value.save_as(f\"{OUT}/ui-{name}-notes.txt\")\n    open(f\"{OUT}/ui-{name}-letter-onscreen.txt\", \"w\").write(pg.inner_text(\"[data-testid=letter-text]\"))\n    shot(f\"{name}-step4\", full=True)\n    log(f\"[{name}] done in\", round(time.time() - T0, 1), \"s\")\n"
}
````

### User / tool · 2026-11-02T23:40:01.299Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/p01_cases.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:40:04.172Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-202-paralegal/h.py artifacts/review-evidence/T-202-paralegal/p01_cases.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/p01.out 2>&1; echo exit $?; grep -E \"^\\[|ERRORS|Error|Traceback|http [45]\" artifacts/review-evidence/T-202-paralegal/p01.out | cut -c1-400 | head -90",
 "description": "Run Playwright walk for four cases",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:40:50.238Z

**tool result**
````
exit 1
[sample] draft took 2.2 s
[sample] s2 item=e1 yes_disabled=False compare=False radios=0 :: Prepared answer / January 9, 2026 · Austin EMS run report /  / Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER. /  / How it was checked / The highlighted words are in the record word for word, every number in th
[sample] s2 item=f_accident_date_after_treatment_1_2_7 yes_disabled=False compare=False radios=0 :: Warning for the attorney /  / The records disagree about the accident date /  / Stated accident date is later than recorded treatment /  / Stated accident date January 19, 2026 (“Date of accident per intake form: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Austin EM
[sample] s2 item=e2 yes_disabled=False compare=False radios=0 :: Prepared answer / January 9, 2026 · Central ER discharge summary /  / Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week. /  / How it was checked / The highlighted words are in the record word 
[sample] s2 item=e3 yes_disabled=False compare=False radios=0 :: Prepared answer / January 16, 2026 · Dr. Alvarez, primary care /  / Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI c
[sample] s2 item=f_r3_1 yes_disabled=False compare=False radios=0 :: Warning for the attorney / Prepared answer /  / An earlier health problem is mentioned /  / Mention of a prior or pre-existing condition /  / Dr. Alvarez, primary care (January 16, 2026) mentions a prior or pre-existing condition: “Patient reports low back pain in 2023, resolved.” /  / Warnings only
[sample] s2 item=e4 yes_disabled=False compare=False radios=0 :: Prepared answer / January 23, 2026 · Capital PT, initial evaluation /  / Cervical range of motion reduced approx. 40%; plan of care 12 visits. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
[sample] s2 item=f_cx1 yes_disabled=False compare=False radios=0 :: Warning for the attorney /  / The plan and what happened differ /  / Treatment plan and what followed differ /  / Capital PT, initial evaluation (January 23, 2026): “Plan of care: 12 visits.” Capital PT, visit 9 (March 6, 2026): “Discharged from PT after two missed appointments.” /  / Warnings only 
[sample] s2 item=e5 yes_disabled=False compare=False radios=0 :: Prepared answer / February 20, 2026 · Capital PT, visit 8 /  / Pain 4/10, improving. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
[sample] s2 item=e6 yes_disabled=False compare=False radios=0 :: Prepared answer / March 6, 2026 · Capital PT, visit 9 /  / Discharged from physical therapy after two missed appointments; pain 3/10. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI check agreed.
[sample] s2 item=f_gap_r6_r7 yes_disabled=False compare=False radios=0 :: Warning for the attorney /  / A break in treatment /  / Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient). /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney 
[sample] s2 item=f_r6_1 yes_disabled=False compare=False radios=0 :: Warning for the attorney / Prepared answer /  / Missed or ended treatment /  / Missed or ended care /  / Wording about missed appointments or ending care in Capital PT, visit 9 (March 6, 2026): “Discharged from PT after two missed appointments.” /  / Warnings only go in the notes for the attorney, n
[sample] s2 item=e7 yes_disabled=False compare=False radios=0 :: Prepared answer / May 18, 2026 · Hill Country Pain Management, new patient /  / New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second AI che
[sample] s2 item=f_r7_1 yes_disabled=False compare=False radios=0 :: Warning for the attorney / Prepared answer /  / Where the accident date comes from /  / Accident date source /  / Accident date as stated in Hill Country Pain Management, new patient (May 18, 2026): “Date of accident per intake form: 2026-01-19.” /  / Warnings only go in the notes for the attorney, 
[sample] s2 item=f_r7_2 yes_disabled=False compare=False radios=0 :: Warning for the attorney / Prepared answer /  / Wording about a new problem /  / New-onset wording in Hill Country Pain Management, new patient (May 18, 2026): “New onset pain”. /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the attorney
[sample] s2 item=e8 yes_disabled=False compare=False radios=0 :: Prepared answer / May 29, 2026 · Austin Imaging, cervical MRI /  / C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically. /  / How it was checked / The highlighted words are in the record word for word, eve
[sample] s2 item=f_r8_1 yes_disabled=False compare=False radios=0 :: Warning for the attorney / Prepared answer /  / Wording about wear and tear /  / Degenerative wording /  / Austin Imaging, cervical MRI (May 29, 2026) uses degenerative wording: “Findings may represent degenerative change”. /  / Warnings only go in the notes for the attorney, never in the letter. Sa
[sample] s2 item=f_r8_2 yes_disabled=False compare=False radios=0 :: Warning for the attorney / Prepared answer /  / Hedged wording (“may”, “possible”) /  / Hedged wording in Austin Imaging, cervical MRI (May 29, 2026): “may represent degenerative change; correlate clinically”. /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists 
[sample] s2 item=e9 yes_disabled=False compare=False radios=0 :: Prepared answer / June 12, 2026 · Hill Country Pain Management, follow-up /  / Cervical epidural steroid injection recommended; patient states symptoms began after the January collision. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in t
[sample] s2 item=f_r9_1 yes_disabled=False compare=False radios=0 :: Warning for the attorney / Prepared answer /  / The patient, not a doctor, says what caused it /  / Reported onset /  / Onset wording reported in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.” /  / Warnings only go in the notes f
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/sample-step2-done.png
[sample] s3 item=a1 boxes=[] :: Charge / Central ER discharge summary · January 9, 2026 /  / $6,240.00 /  / Written in the record as $6,240. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/sample-s3-00-a1.png
[sample] s3 item=a4 boxes=[] :: Charge / Austin Imaging, cervical MRI · May 29, 2026 /  / $2,150.00 /  / Written in the record as $2,150. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/sample-s3-01-a4.png
[sample] s3 item=a2 boxes=[] :: Never counted / Capital PT, initial evaluation · January 23, 2026 /  / $185 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill total.
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/sample-s3-02-a2.png
[sample] s3 item=a3 boxes=[] :: Never counted / Capital PT, visit 8 · February 20, 2026 /  / Not a money amount: missing 3 days of work /  / This figure is not a bill (for example a damages or settlement figure), so it is not added to the total. /  / Either way, it is never added to the bill total.
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/sample-s3-03-a3.png
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/sample-step3-done.png
[shot] /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/sample-step4.png
[sample] done in 15.5 s
Traceback (most recent call last):
playwright._impl._errors.TimeoutError: Page.click: Timeout 30000ms exceeded.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:40:51.714Z

**tool call — Bash**
````
{
 "command": "grep -n -A12 \"Traceback\" artifacts/review-evidence/T-202-paralegal/p01.out | cut -c1-300 | head -30",
 "description": "Show traceback detail"
}
````

### User / tool · 2026-11-02T23:40:51.824Z

**tool result**
````
86:Traceback (most recent call last):
87-  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/h.py", line 58, in <module>
88-    main(sys.argv[1])
89-  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/h.py", line 49, in main
90-    exec(compile(open(script).read(), script, "exec"), g)
91-  File "artifacts/review-evidence/T-202-paralegal/p01_cases.py", line 30, in <module>
92-    pg.click("[data-testid=tile-paste]")
93-  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 16267, in click
94-    self._sync(
95-  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
96-    return task.result()
97-           ^^^^^^^^^^^^^
98-  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_page.py", line 891, in click
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:40:57.988Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && grep -n \"tile-paste\\|demo\" app/frontend/guided/step1.js | cut -c1-220 | head -20",
 "description": "Check paste tile demo behavior"
}
````

### User / tool · 2026-11-02T23:40:58.075Z

**tool result**
````
4:   Test ids: input-name, name-error, tile-paste, tile-file, tile-sample, tile-library, input-text, file-input, btn-choose-file, library-<id>, btn-read, btn-draft, btn-start-over, bar-msg, action-bar,
6:   prepared-badge, demo-note. Text only (textContent); no inline style attributes. */
26:    const demo = !!hl.demo_mode, lim = hl.limits || { max_chars: 60000, max_records: 40 }, sampleOk = hl.sample_available !== false;
30:    const ONLY = () => (lib ? "This demo can only read the sample case and our test cases." : "This demo can only read the sample case.");
31:    const st = { how: demo ? (sampleOk ? "sample" : lib ? "library" : "sample") : "paste", text: "", file: null, lib: null, reading: false, again: null };
40:      { key: "paste", head: "Paste text", sub: "Copy the records and paste them here.", off: demo },
41:      { key: "file", head: "Upload a file", sub: "A .txt or .pdf file, up to 5 MB.", off: demo },
49:      return h("label", { class: "tile" + (t.off ? " off" : ""), "aria-disabled": t.off ? "true" : null, "data-testid": "tile-" + t.key }, input, h("span", { class: "tl-h" }, t.head), h("p", {}, t.sub), t.off ? h("p",
108:      if (s === 409 && code === "demo_mode_unsupported_input") return { msg: ONLY(), alts: sampleOk ? [{ id: "btn-use-sample", label: "Use the sample case", fn: () => { st.how = "sample"; setRadio(); drawBox(); clear
109:      if (s === 429) return { msg: reason === "demo_full" || reason === "demo_busy" ? e.message : "We're reading other files right now. Try again in a moment.", alts: [again] };
160:        demo ? h("div", { class: "note-box demo-note", "data-testid": "demo-note" }, h("span", { class: "nb-text" }, ONLY(), h("span", {}, "Pasting your own records or uploading a file isn't available here."))) : nul
216:        else { btn.disabled = false; btn.textContent = label; b.say(e.code === "demo_mode_unsupported_input" ? ONLY() : e.message, "bad"); return; }
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:41:02.882Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/p01_cases.py",
 "old_string": "    elif name in PASTE:\n        pg.click(\"[data-testid=tile-paste]\")\n        pg.wait_for_timeout(300)\n        pg.fill(\"[data-testid=input-text]\", open(PASTE[name]).read())",
 "new_string": "    elif name in PASTE:\n        # demo UI turns the paste tile off (step1.js:40 off: demo); the API accepts the golden text (201), so create it there and open it in the UI\n        import json, urllib.request\n        req = urllib.request.Request(BASE + \"/api/cases\", data=json.dumps({\"text\": open(PASTE[name]).read()}).encode(),\n                                     headers={\"Content-Type\": \"application/json\"}, method=\"POST\")\n        tok = json.loads(urllib.request.urlopen(req, timeout=20).read())[\"token\"]\n        log(f\"[{name}] created via POST /api/cases token={tok}\")\n        pg.goto(f\"{BASE}/case/{tok}/records\")\n        pg.wait_for_selector(\"[data-testid=view][data-ready]\")\n        pg.wait_for_timeout(500)"
}
````

### User / tool · 2026-11-02T23:41:03.010Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/p01_cases.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:41:04.556Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/p01_cases.py",
 "old_string": "    pg.wait_for_timeout(300)\n    pg.click(\"[data-testid=btn-read]\")\n    pg.wait_for_selector(\"[data-testid=btn-draft]\", timeout=20000)",
 "new_string": "    pg.wait_for_timeout(300)\n    if name not in PASTE:\n        pg.click(\"[data-testid=btn-read]\")\n    pg.wait_for_selector(\"[data-testid=btn-draft]\", timeout=20000)"
}
````

### User / tool · 2026-11-02T23:41:04.665Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/p01_cases.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:41:07.612Z

**tool call — Bash**
````
{
 "command": "CASES=case_09,lib14,lib10 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/h.py artifacts/review-evidence/T-202-paralegal/p01_cases.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/p02.out 2>&1; echo exit $?; grep -E \"^\\[(case_09|lib14|lib10)\\] (s3|draft|done|created)|ERRORS|Traceback|http [45]|Error\" artifacts/review-evidence/T-202-paralegal/p02.out | cut -c1-500 | head -60",
 "description": "Run Playwright walk for case_09, lib14, lib10",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:41:47.502Z

**tool result**
````
exit 0
[case_09] created via POST /api/cases token=fJ32FX1cW-24bcLLwo8zEg
[case_09] draft took 1.6 s
[case_09] s3 item=a1 boxes=[] :: Charge / Hobbleton Family Clinic, billing statement · March 1, 2026 /  / $275.00 /  / Written in the record as $275. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[case_09] done in 7.2 s
[lib14] draft took 2.4 s
[lib14] s3 item=a1 boxes=[] :: Charge / Orrin Mere Regional ED · September 14, 2026 /  / $2,960.00 /  / Written in the record as $2,960. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib14] s3 item=a2 boxes=[] :: Charge / Tarnwick Fire-Rescue, ambulance invoice · November 12, 2026 /  / $1,380.00 /  / Written in the record as $1,380.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib14] s3 item=a4 boxes=[] :: Charge / Tarnwick Fire-Rescue, ambulance invoice · November 12, 2026 /  / $187.05 /  / Written in the record as $187.05. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib14] s3 item=a3 boxes=[] :: Never counted / Tarnwick Fire-Rescue, ambulance invoice · November 12, 2026 /  / $21.50 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill total.
[lib14] s3 item=a5 boxes=['check-compare'] :: Never counted / Tarnwick Fire-Rescue, ambulance invoice · November 12, 2026 /  / $1,567.05 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
[lib14] done in 13.1 s
[lib10] draft took 2.4 s
[lib10] s3 item=a2 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $4,920.00 /  / Written in the record as $4,920.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib10] s3 item=a3 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $2,105.00 /  / Written in the record as $2,105.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib10] s3 item=a4 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $386.50 /  / Written in the record as $386.50. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib10] s3 item=a5 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $712.00 /  / Written in the record as $712.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib10] s3 item=a1 boxes=[] :: Never counted / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $1,640.00 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill total.
[lib10] s3 item=a6 boxes=['check-compare'] :: Never counted / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $8,123.50 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
[lib10] s3 item=a7 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · July 3, 2026 /  / $8,023.50 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
[lib10] s3 item=a8 boxes=[] :: Never counted / Quoinmere Mutual Health Plan, EOB · July 3, 2026 /  / $3,610.00 /  / Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges. /  / Either way, it is never added to the bill total.
[lib10] s3 item=a9 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · July 3, 2026 /  / $4,413.50 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
[lib10] s3 item=a10 boxes=[] :: Never counted / Quoinmere Mutual Health Plan, EOB · July 3, 2026 /  / $3,530.80 /  / Payment: money received, not a charge. /  / Either way, it is never added to the bill total.
[lib10] s3 item=a11 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · July 3, 2026 /  / $882.70 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
[lib10] done in 19.0 s
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:41:57.197Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal && for c in sample case_09 lib14 lib10; do echo \"=== $c\"; cat ui-$c-letter.txt; echo; done; ls",
 "description": "Show UI-exported letters for all four cases"
}
````

### User / tool · 2026-11-02T23:41:57.286Z

**tool result**
````
=== sample
TREATMENT CHRONOLOGY

January 9, 2026 — Austin EMS run report
Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."

January 9, 2026 — Central ER discharge summary
Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."

January 16, 2026 — Dr. Alvarez, primary care
Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.
Source [Ex. __ / Bates __]: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."

January 23, 2026 — Capital PT, initial evaluation
Cervical range of motion reduced approx. 40%; plan of care 12 visits.
Source [Ex. __ / Bates __]: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."

February 20, 2026 — Capital PT, visit 8
Pain 4/10, improving.
Source [Ex. __ / Bates __]: "Pain 4/10, improving."

March 6, 2026 — Capital PT, visit 9
Discharged from physical therapy after two missed appointments; pain 3/10.
Source [Ex. __ / Bates __]: "Discharged from PT after two missed appointments. Pain 3/10."

May 18, 2026 — Hill Country Pain Management, new patient
New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
Source [Ex. __ / Bates __]: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered."

May 29, 2026 — Austin Imaging, cervical MRI
C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."

June 12, 2026 — Hill Country Pain Management, follow-up
Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
Source [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."

BILLED CHARGES

Central ER discharge summary, January 9, 2026: $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240."
Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
Source [Ex. __ / Bates __]: "Charge: $2,150."

Billed charges accepted from these records: $8,390.00
=== case_09
TREATMENT CHRONOLOGY

February 2, 2026 — Hobbleton Family Clinic, visit
Left wrist pain 4/10. Splint applied. Return in 2 weeks.
Source [Ex. __ / Bates __]: "Left wrist pain 4/10. Splint applied. Return in 2 weeks."

March 12, 2026 — Hobbleton Family Clinic, phone note
Patient called to request a work note; work note provided.
Source [Ex. __ / Bates __]: "Patient called to request a work note. Work note provided."

March 30, 2026 — Hobbleton Family Clinic, visit
Left wrist pain 3/10. Splint removed.
Source [Ex. __ / Bates __]: "Left wrist pain 3/10. Splint removed."

April 13, 2026 — Hobbleton Family Clinic, visit
Pain 1/10. Released from care.
Source [Ex. __ / Bates __]: "Pain 1/10. Released from care."

BILLED CHARGES

Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00
Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."

Billed charges accepted from these records: $275.00
=== lib14
TREATMENT CHRONOLOGY

September 14, 2026 — Tarnwick Fire-Rescue run report
Patient states neck pain 6/10 and tingling in the right hand; cervical collar applied and transported to Orrin Mere Regional ED.
Source [Ex. __ / Bates __]: "Pt states neck pain 6/10 and tingling in the right hand. Cervical collar applied. Transported to Orrin Mere Regional ED."

September 14, 2026 — Orrin Mere Regional ED
Diagnosis of cervical strain; cervical spine x-ray negative for fracture; discharged with a muscle relaxant.
Source [Ex. __ / Bates __]: "Dx: cervical strain. X-ray cervical spine negative for fracture. Discharged with a muscle relaxant."

September 21, 2026 — Hollowbrook Chiropractic, daily note visit 1 (scanned, OCR text)
Pain 7 circled on a 0-10 scale; tenderness at C4-C6; adjustment, e-stim and hot pack marked.
Source [Ex. __ / Bates __]: "Pain 7 circled on a 0-10 scale. Tenderness at C4-C6. [X] adjustment [X] e-stim [X] hot pack."

October 6, 2026 — Hollowbrook Chiropractic, daily note visit 9 (scanned, OCR text)
Pain 5 circled; tenderness at C4-C5 improved; adjustment and e-stim boxes marked [X].
Source [Ex. __ / Bates __]: "Pain 5 circled. Tenderness at C4-C5, improved. [X] adjustment [X] e-stim."

November 3, 2026 — Hollowbrook Chiropractic, re-examination (typed)
Re-examination: pain 6/10, unchanged from the initial visit; plan to continue care three times weekly.
Source [Ex. __ / Bates __]: "Pain 6/10, unchanged from the initial visit. Plan: continue care three times weekly."

BILLED CHARGES

Orrin Mere Regional ED, September 14, 2026: $2,960.00
Source [Ex. __ / Bates __]: "ED charge: $2,960."
Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00
Source [Ex. __ / Bates __]: "A0427 ALS emergency transport, 1 unit, charge $1,380.00."
Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05
Source [Ex. __ / Bates __]: "charge $187.05."

Billed charges accepted from these records: $4,527.05
=== lib10
TREATMENT CHRONOLOGY

June 9, 2026 — Rainhollow Fire-Rescue run report
Driver of a pickup struck at an intersection; patient states chest wall and left knee pain.
Source [Ex. __ / Bates __]: "Pt states chest wall and left knee pain."

June 9, 2026 — Saltmarrow General Hospital ED
Diagnosed with left knee contusion and chest wall contusion; left knee X-ray negative for fracture; admitted for observation.
Source [Ex. __ / Bates __]: "Dx: left knee contusion, chest wall contusion. X-ray left knee negative for fracture. Admitted for observation."

June 12, 2026 — Saltmarrow General Hospital, discharge summary
Discharged after 3 days of observation; diagnosis left knee contusion; follow up with orthopedics.
Source [Ex. __ / Bates __]: "Discharged after 3 days of observation. Dx: left knee contusion. Follow up with orthopedics."

June 19, 2026 — Saltmarrow General Hospital, UB-04 itemized bill
UB-04 bill, type of bill 0111, for statement period 06/09/2026 to 06/12/2026: room.
Source [Ex. __ / Bates __]: "UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026."

June 24, 2026 — Dr. Ignatius Wardlaw, orthopedics, new patient
Left knee pain 5/10; MRI of the left knee ordered.
Source [Ex. __ / Bates __]: "Left knee pain 5/10. MRI left knee ordered."

July 3, 2026 — Quoinmere Mutual Health Plan, EOB
Explanation of benefits, not a bill.
Source [Ex. __ / Bates __]: "Explanation of benefits, processed 07/03/2026, for dates of service 06/09/2026 to 06/12/2026. This is not a bill."

July 8, 2026 — Dr. Ignatius Wardlaw, orthopedics, follow-up
Left knee pain 3/10. Injection performed. Continue home exercises.
Source [Ex. __ / Bates __]: "Left knee pain 3/10. Injection performed. Continue home exercises."

August 26, 2026 — Dr. Ignatius Wardlaw, orthopedics, follow-up
Left knee pain 2/10. Discharged from care.
Source [Ex. __ / Bates __]: "Left knee pain 2/10. Discharged from care."

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
h.py
letter_check.out
letters_dump.out
letters_dump.py
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

### Assistant · claude-opus-5-5 · 2026-11-02T23:42:23.673Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal && grep -E \"^\\[lib10\\] s2 item=e4|^\\[lib14\\] s2\" p02.out | cut -c1-1200",
 "description": "Show Step 2 cards for lib10 e4 and lib14"
}
````

### User / tool · 2026-11-02T23:42:23.772Z

**tool result**
````
[lib14] s2 item=e1 yes_disabled=False compare=False radios=0 :: AI draft / September 14, 2026 · Tarnwick Fire-Rescue run report /  / Patient states neck pain 6/10 and tingling in the right hand; cervical collar applied and transported to Orrin Mere Regional ED. /  / How it was checked / The highlighted words are in the record word for word, every number in the l
[lib14] s2 item=f_r1_1 yes_disabled=False compare=False radios=0 :: Warning for the attorney / AI draft /  / Wording the other side could use /  / Scene facts recorded by Tarnwick Fire-Rescue run report (September 14, 2026): “Pt ambulatory at scene.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no lists it as ruled out, so the att
[lib14] s2 item=e2 yes_disabled=False compare=False radios=0 :: AI draft / September 14, 2026 · Orrin Mere Regional ED /  / Diagnosis of cervical strain; cervical spine x-ray negative for fracture; discharged with a muscle relaxant. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in them, and a second 
[lib14] s2 item=e3 yes_disabled=False compare=False radios=0 :: AI draft / September 21, 2026 · Hollowbrook Chiropractic, daily note visit 1 (scanned, OCR text) /  / Pain 7 circled on a 0-10 scale; tenderness at C4-C6; adjustment, e-stim and hot pack marked. /  / How it was checked / The highlighted words are in the record word for word, every number in the line
[lib14] s2 item=e4 yes_disabled=False compare=False radios=0 :: AI draft / October 6, 2026 · Hollowbrook Chiropractic, daily note visit 9 (scanned, OCR text) /  / Pain 5 circled; tenderness at C4-C5 improved; adjustment and e-stim boxes marked [X]. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in the
[lib14] s2 item=e6 yes_disabled=False compare=False radios=0 :: AI draft / November 3, 2026 · Hollowbrook Chiropractic, re-examination (typed) /  / Re-examination: pain 6/10, unchanged from the initial visit; plan to continue care three times weekly. /  / How it was checked / The highlighted words are in the record word for word, every number in the line is in t
[lib14] s2 item=e7 yes_disabled=True compare=False radios=0 :: AI draft / November 10, 2026 · Hollowbrook Chiropractic, CMS-1500 (OCR of scanned claim) /  / Claim line 1: 092126 to 092326, CPT 98941, 24F 25500, 24G 3. Line 2: 092126 to 092326, CPT 97014, 24F 7500, 24G 3. Item 28 total charge 33000. /  / The line or highlighted words states a dollar amount, whic
[lib14] s2 item=e8 yes_disabled=True compare=False radios=0 :: AI draft / November 12, 2026 · Tarnwick Fire-Rescue, ambulance invoice /  / Invoice lists A0427 ALS emergency transport, 1 unit, charge $1,380.00, and A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05; total charges $1,567.05. /  / The line or highlighted words states a doll
[lib14] s2 item=f_r8_1 yes_disabled=False compare=False radios=0 :: Warning for the attorney / AI draft /  / Wording the other side could use /  / Attorney referral /  / Referral wording in Tarnwick Fire-Rescue, ambulance invoice (November 12, 2026): “Letter of protection requested.” /  / Warnings only go in the notes for the attorney, never in the letter. Saying no
[lib14] s2 item=e5 yes_disabled=False compare=False radios=0 :: No date found / Hollowbrook Chiropractic, daily note visit 12 (handwritten, OCR text) /  / We couldn't find a date /  / We couldn't find a date in this record, so it can't go on the timeline. /  / The line waiting for a date: “Pain 4 circled; adjusted C4-C6; [X] e-stim; patient states neck feels bet
[lib14] s2 item=f_date_r5 yes_disabled=False compare=False radios=0 :: Warning for the attorney /  / This record's date is unclear /  / Date to confirm /  / The date “10/20” in Hollowbrook Chiropractic, daily note visit 12 (handwritten, OCR text) can be read more than one way; choose one reading. /  / Warnings only go in the notes for the attorney, never in the letter.
[lib10] s2 item=e4 yes_disabled=True compare=True radios=0 :: AI draft / June 19, 2026 · Saltmarrow General Hospital, UB-04 itemized bill /  / UB-04 bill, type of bill 0111, for statement period 06/09/2026 to 06/12/2026: room. /  / Underlined words are not in the highlighted words. /  / A second AI check found this not supported by the highlighted words. Read
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:42:32.054Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal && cat ui-lib10-notes.txt; echo =====; cat ui-lib14-notes.txt | head -80",
 "description": "Read lib10 and lib14 internal notes"
}
````

### User / tool · 2026-11-02T23:42:32.166Z

**tool result**
````
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.

FLAGS ACCEPTED
- Gap: 43 days, July 14, 2026 to August 26, 2026: record 8 (Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim), July 14, 2026) to record 9 (Dr. Ignatius Wardlaw, orthopedics, follow-up, August 26, 2026).
- Causation language: record 1 (Rainhollow Fire-Rescue run report, June 9, 2026) "Ambulatory at scene."

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- Record 9 (Dr. Ignatius Wardlaw, orthopedics, follow-up, August 26, 2026): "Left knee pain 2/10. Discharged from care." Gap.

AMOUNTS NOT TOTALED
- Record 4 (Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026): "FL44 rate $1,640.00 per day" Rate $1,640; visit count not stated. Request itemized ledger from Saltmarrow General Hospital.
- Record 4 (Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026): "Rev 0001 total charges $8,123.50." Not totaled ($8,123.50): Total or subtotal line: it repeats the charges listed with it, so it is not totaled.
- Record 6 (Quoinmere Mutual Health Plan, EOB, July 3, 2026): "plan paid $3,530.80" Not totaled ($3,530.80): Payment: money received, not a charge.
- Record 6 (Quoinmere Mutual Health Plan, EOB, July 3, 2026): "you may owe $882.70." Not totaled ($882.70): Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.
- Record 6 (Quoinmere Mutual Health Plan, EOB, July 3, 2026): "Amount billed $8,023.50" Not totaled ($8,023.50): Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.
- Record 6 (Quoinmere Mutual Health Plan, EOB, July 3, 2026): "network discount $3,610.00" Not totaled ($3,610.00): Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges.
- Record 6 (Quoinmere Mutual Health Plan, EOB, July 3, 2026): "allowed amount $4,413.50" Not totaled ($4,413.50): Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge.

DAMAGES MENTIONS (not charges)
- none

FUTURE TREATMENT RECOMMENDED (no cost stated)
- none

BILLS TO REQUEST (entry in the letter, no accepted charge)
- Rainhollow Fire-Rescue run report; Saltmarrow General Hospital ED; Dr. Ignatius Wardlaw.

RECORDS NOT IN THE TREATMENT SECTION
- Record 8 (Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim), July 14, 2026) — dismissed

EDITED ITEMS
- none

PENDING ITEMS NOT INCLUDED
- none=====
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.

FLAGS ACCEPTED
- Causation language: record 1 (Tarnwick Fire-Rescue run report, September 14, 2026) "Pt ambulatory at scene."; record 8 (Tarnwick Fire-Rescue, ambulance invoice, November 12, 2026) "Letter of protection requested."
- Record warning: record 5 (Hollowbrook Chiropractic, daily note visit 12 (handwritten, OCR text), date not stated).

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit the excerpt or dismiss the entry to remove it; hedge sentences cannot be removed)
- none

AMOUNTS NOT TOTALED
- Record 8 (Tarnwick Fire-Rescue, ambulance invoice, November 12, 2026): "8.7 miles at $21.50 per mile" Rate $21.50; visit count not stated. Request itemized ledger from Tarnwick Fire-Rescue.
- Record 8 (Tarnwick Fire-Rescue, ambulance invoice, November 12, 2026): "Total charges $1,567.05." Not totaled ($1,567.05): Total or subtotal line: it repeats the charges listed with it, so it is not totaled.

DAMAGES MENTIONS (not charges)
- none

FUTURE TREATMENT RECOMMENDED (no cost stated)
- none

BILLS TO REQUEST (entry in the letter, no accepted charge)
- Tarnwick Fire-Rescue run report; Hollowbrook Chiropractic.

RECORDS NOT IN THE TREATMENT SECTION
- Record 7 (Hollowbrook Chiropractic, CMS-1500 (OCR of scanned claim), November 10, 2026) — dismissed
- Record 8 (Tarnwick Fire-Rescue, ambulance invoice, November 12, 2026) — dismissed
- Record 5 (Hollowbrook Chiropractic, daily note visit 12 (handwritten, OCR text), date not stated) — dismissed

EDITED ITEMS
- none

PENDING ITEMS NOT INCLUDED
- none
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:42:43.020Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && mkdir -p $S/t202parent && git archive a44cfa7 | tar -x -C $S/t202parent && mkdir -p artifacts/review-evidence/T-202-paralegal/parent-a44cfa7 && echo ok",
 "description": "Extract parent commit a44cfa7 archive"
}
````

### User / tool · 2026-11-02T23:42:44.220Z

**tool result**
````
ok
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:42:49.628Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/letters_dump_parent.py",
 "content": "\"\"\"T-202 paralegal: same as letters_dump.py but for the parent commit a44cfa7 (no 'counted' variant, no charge_date_violations there).\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/letters_dump_parent.py <archive_root> <out_dir>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nout = os.path.abspath(sys.argv[2])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom evals import letter_check as LC  # noqa: E402\n\nCASES = {\n    \"sample\": \"evals/golden/sample.txt\",\n    \"case_09\": \"evals/golden/case_09_nonvisit_hides_gap.txt\",\n    \"lib14\": \"evals/library/case_lib14_handwritten_chiro_scans.txt\",\n    \"lib10\": \"evals/library/case_lib10_eob_ub04_cms1500.txt\",\n}\nfor name, path in CASES.items():\n    got = LC.letters_for(open(path).read())\n    v = got[\"all_accepted\"]\n    with open(os.path.join(out, f\"{name}-all_accepted-letter.txt\"), \"w\") as f:\n        f.write(v[\"letters\"][\"standard\"])\n    with open(os.path.join(out, f\"{name}-all_accepted-notes.txt\"), \"w\") as f:\n        f.write(v[\"notes\"])\n    print(f\"== {name}: cents={v['charge_cents']}\")\n"
}
````

### User / tool · 2026-11-02T23:42:49.751Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/letters_dump_parent.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:42:56.512Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/letters_dump_parent.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202parent /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/parent-a44cfa7 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/parent-a44cfa7/dump.out 2>&1; echo exit $?; cd artifacts/review-evidence/T-202-paralegal; for c in sample case_09 lib14 lib10; do echo \"### $c letter\"; diff parent-a44cfa7/$c-all_accepted-letter.txt $c-all_accepted-letter.txt; echo \"### $c notes\"; diff parent-a44cfa7/$c-all_accepted-notes.txt $c-all_accepted-notes.txt; done > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/parent-vs-f0921e4.diff; cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/parent-vs-f0921e4.diff",
 "description": "Generate parent letters and diff against f0921e4"
}
````

### User / tool · 2026-11-02T23:42:58.329Z

**tool result**
````
exit 0
### sample letter
### sample notes
### case_09 letter
21c21
< Hobbleton Family Clinic, billing statement, March 1, 2026: $275.00
---
> Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00
### case_09 notes
### lib14 letter
27c27
< Tarnwick Fire-Rescue, ambulance invoice, November 12, 2026: $1,380.00
---
> Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00
29c29
< Tarnwick Fire-Rescue, ambulance invoice, November 12, 2026: $187.05
---
> Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05
### lib14 notes
### lib10 letter
29c29
< Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $4,920.00
---
> Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00
31c31
< Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $2,105.00
---
> Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00
33c33
< Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $386.50
---
> Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $386.50
35c35
< Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026: $712.00
---
> Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $712.00
### lib10 notes
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:43:13.109Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && sed -n 1,106p tests/unit/test_t202_charge_service_dates.py | cut -c1-260",
 "description": "Read the T-202 unit tests"
}
````

### User / tool · 2026-11-02T23:43:13.190Z

**tool result**
````
"""T-202 (D-071): a charge line in the letter prints the service date its bill line states, a period as a range, never the bill's statement date as if it were one. Code only."""
import pathlib

import pytest

from app.backend import amounts as AM, export, store
from evals import letter_check as LC

ROOT = pathlib.Path(__file__).resolve().parents[2]
GOLD, LIB = ROOT / "evals" / "golden", ROOT / "evals" / "library"


def letter(path):
    return LC.letters_for(path.read_text())["all_accepted"]["letters"]


def lines(text):
    return text.split("\n")


@pytest.mark.parametrize("style", ["standard", "oneline"])
def test_case_09_prints_the_visit_date_not_the_statement_date(style):
    ls = lines(letter(GOLD / "case_09_nonvisit_hides_gap.txt")[style])
    assert "Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00" in ls
    assert not any("March 1, 2026: $275" in l for l in ls)


@pytest.mark.parametrize("style", ["standard", "oneline"])
def test_lib14_ambulance_invoice_prints_the_run_date(style):
    ls = lines(letter(LIB / "case_lib14_handwritten_chiro_scans.txt")[style])
    assert "Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00" in ls
    assert "Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05" in ls
    assert not any("November 12, 2026: $" in l for l in ls)


@pytest.mark.parametrize("style", ["standard", "oneline"])
def test_lib10_ub04_prints_the_statement_period_as_a_range(style):
    ls = lines(letter(LIB / "case_lib10_eob_ub04_cms1500.txt")[style])
    for fig in ("$4,920.00", "$2,105.00", "$386.50", "$712.00"):
        assert f"Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: {fig}" in ls, fig
    assert not any("June 19, 2026: $" in l for l in ls)


def test_a_visit_note_keeps_the_visit_date_and_the_sample_golden_is_unchanged():
    got = LC.letters_for((GOLD / "sample.txt").read_text())["all_accepted"]["letters"]["standard"]
    assert "Central ER discharge summary, January 9, 2026: $6,240.00" in lines(got)
    assert "Austin Imaging, cervical MRI, May 29, 2026: $2,150.00" in lines(got)


def test_charges_are_listed_in_service_date_order():
    ls = lines(letter(LIB / "case_lib06_lop_billed_vs_adjusted.txt")["standard"])
    heads = [h for h, _ in LC.charge_lines("\n".join(ls))]
    from datetime import datetime
    got = [datetime.strptime(" ".join(h.rsplit(": $", 1)[0].rsplit(", ", 2)[-2:]).replace(",", ""), "%B %d %Y") for h in heads if "service date not stated" not in h]
    assert len(got) >= 2 and got == sorted(got), heads


def test_date_range_formats():
    assert export._date_range("2026-06-09", "2026-06-12") == "June 9–12, 2026"
    assert export._date_range("2026-06-28", "2026-07-02") == "June 28–July 2, 2026"
    assert export._date_range("2026-12-30", "2027-01-02") == "December 30, 2026–January 2, 2027"
    assert export._date_range("2026-09-14") == export._date_range("2026-09-14", "2026-09-14") == "September 14, 2026"


UB = ("UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.")


def test_charge_basis_returns_the_end_of_a_stated_period():
    a = next(x for x in AM.find_amounts(UB) if x["raw"] == "$2,105.00")
    b = AM.charge_basis(UB, a, "Saltmarrow General Hospital, UB-04 itemized bill", "2026-06-19")
    assert (b["dos"], b["dos_end"]) == ("2026-06-09", "2026-06-12")
    one = "Invoice for the run of 09/14/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00."
    a = next(x for x in AM.find_amounts(one) if x["raw"] == "$1,380.00")
    b = AM.charge_basis(one, a, "Tarnwick Fire-Rescue, ambulance invoice", "2026-11-12")
    assert (b["dos"], b["dos_end"]) == ("2026-09-14", None)


def test_store_returns_period_and_none_for_an_undated_ledger_line():
    rec = {"source": "Saltmarrow General Hospital, UB-04 itemized bill", "date_iso": "2026-06-19"}
    assert store.charge_service_dates({"excerpt": UB, "value_cents": 210500}, rec, UB.index("$2,105.00")) == ("2026-06-09", "2026-06-12")


# ---- the eval check itself has teeth
RECS = [{"n": 1, "source": "Saltmarrow General Hospital, UB-04 itemized bill", "date_iso": "2026-06-19", "excerpt": UB + " Statement date 06/19/2026."}]
Q = 'Source [Ex. __ / Bates __]: "Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."'


def _l(head):
    return f"BILLED CHARGES\n\n{head}: $2,105.00\n{Q}\n\nBilled charges accepted from these records: $2,105.00"


def test_the_letter_check_passes_the_period_and_fails_the_statement_date():
    ok = "Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026"
    assert LC.charge_date_violations(_l(ok), RECS) == []
    bad = LC.charge_date_violations(_l("Saltmarrow General Hospital, UB-04 itemized bill, June 19, 2026"), RECS)
    assert bad and "not a service date" in bad[0]
    assert LC.charge_date_violations(_l("Saltmarrow General Hospital, UB-04 itemized bill, June 9–13, 2026"), RECS)


def test_the_letter_check_wants_the_statement_form_to_match_the_record():
    recs = [{"n": 1, "source": "Fennimoor Spine Clinic, itemized ledger", "date_iso": "2026-06-15", "excerpt": "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00."}]
    q = 'Source [Ex. __ / Bates __]: "New patient exam charge $250.00"'
    good = f"BILLED CHARGES\n\nFennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00\n{q}\n\nBilled charges accepted from these records: $250.00"
    assert LC.charge_date_violations(good, recs) == []
    assert LC.charge_date_violations(good.replace("June 15", "June 16"), recs)
    assert LC.charge_date_violations(good.replace("(statement dated June 15, 2026; service date not stated)", "June 15, 2026"), recs)       # the bare statement date
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:43:14.099Z

Now probing the parse with ledger shapes an adjuster would see.

### Assistant · claude-opus-5-5 · 2026-11-02T23:43:26.044Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_dates.py",
 "content": "\"\"\"T-202 paralegal probe: what date would the letter print for each charge figure on bill shapes a paralegal sees?\nCalls the shipped code path (store.charge_service_dates -> export._date_range) on the f0921e4 archive. SYNTHETIC probe text only.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/probe_dates.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, export, store  # noqa: E402\n\nPROBES = [\n    (\"P1 two-row ledger, own dates\", \"Hobbleton Family Clinic, itemized ledger\", \"2026-03-15\",\n     \"Statement date 03/15/2026. 02/02/2026 office visit charge $275.00. 02/16/2026 x-ray charge $150.00. Balance due $425.00.\"),\n    (\"P2 CMS-1500 two DOS joined by 'and'\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"CMS-1500 for dates of service 06/24/2026 and 07/08/2026. CPT 99204 charge $185.00. CPT 20610 charge $210.00.\"),\n    (\"P3 invoice date stated before run date\", \"Tarnwick Fire-Rescue, ambulance invoice\", \"2026-11-12\",\n     \"Invoice date 11/12/2026. Run of 09/14/2026. A0427 ALS emergency transport, charge $1,380.00.\"),\n    (\"P4 UB-04 period across months\", \"Saltmarrow General Hospital, UB-04 itemized bill\", \"2026-07-10\",\n     \"UB-04 statement period 06/28/2026 to 07/02/2026. Rev 0120 room and board, FL47 total charges $4,920.00.\"),\n    (\"P5 UB-04 period with 'through'\", \"Saltmarrow General Hospital, UB-04 itemized bill\", \"2026-06-19\",\n     \"UB-04 statement period 06/09/2026 through 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.\"),\n    (\"P6 UB-04 period with hyphen\", \"Saltmarrow General Hospital, UB-04 itemized bill\", \"2026-06-19\",\n     \"UB-04 statement period 06/09/2026 - 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.\"),\n    (\"P7 statement + DOS label same sentence\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Statement date 03/01/2026, date of service 02/02/2026: office visit charge $275.00.\"),\n    (\"P8 ledger row DOS then posted\", \"Fennimoor Spine Clinic, itemized ledger\", \"2026-06-15\",\n     \"06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00. 06/12/26 06/13/26 97110 Therapeutic exercise charge $95.00.\"),\n    (\"P9 statement period then a separately dated line\", \"Saltmarrow General Hospital, UB-04 itemized bill\", \"2026-06-19\",\n     \"UB-04 statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, service date 06/09/2026, FL47 total charges $2,105.00.\"),\n    (\"P10 'from X to Y' dates of service\", \"Capital PT, billing statement\", \"2026-03-20\",\n     \"Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 therapeutic exercise, 9 units, charge $1,665.00.\"),\n]\nfor label, src, rd, ex in PROBES:\n    print(f\"== {label}  (record date {rd})\\n   {ex}\")\n    for a in AM.find_amounts(ex):\n        if a.get(\"cents\") is None:\n            continue\n        b = AM.charge_basis(ex, a, src, rd)\n        first, last = store.charge_service_dates({\"excerpt\": ex, \"value_cents\": a[\"cents\"]}, {\"source\": src, \"date_iso\": rd}, a[\"start\"])\n        shown = export._date_range(first, last) if first else \"(T-200 form: statement dated / service date not stated)\"\n        print(f\"   {a['raw']:>10}  ok={b['ok']} reason={b['reason']!r}  letter date -> {shown}\")\n"
}
````

### User / tool · 2026-11-02T23:43:26.202Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_dates.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:43:31.086Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/probe_dates.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_dates.out 2>&1; echo exit $?; cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_dates.out",
 "description": "Run service-date parse probes"
}
````

### User / tool · 2026-11-02T23:43:31.460Z

**tool result**
````
exit 0
== P1 two-row ledger, own dates  (record date 2026-03-15)
   Statement date 03/15/2026. 02/02/2026 office visit charge $275.00. 02/16/2026 x-ray charge $150.00. Balance due $425.00.
      $275.00  ok=True reason=None  letter date -> February 2, 2026
      $150.00  ok=True reason=None  letter date -> February 16, 2026
      $425.00  ok=False reason='The line states no date of service, so it is not an itemized service line and is not totaled.'  letter date -> (T-200 form: statement dated / service date not stated)
== P2 CMS-1500 two DOS joined by 'and'  (record date 2026-07-14)
   CMS-1500 for dates of service 06/24/2026 and 07/08/2026. CPT 99204 charge $185.00. CPT 20610 charge $210.00.
      $185.00  ok=True reason=None  letter date -> June 24, 2026
      $210.00  ok=True reason=None  letter date -> June 24, 2026
== P3 invoice date stated before run date  (record date 2026-11-12)
   Invoice date 11/12/2026. Run of 09/14/2026. A0427 ALS emergency transport, charge $1,380.00.
    $1,380.00  ok=True reason=None  letter date -> September 14, 2026
== P4 UB-04 period across months  (record date 2026-07-10)
   UB-04 statement period 06/28/2026 to 07/02/2026. Rev 0120 room and board, FL47 total charges $4,920.00.
    $4,920.00  ok=True reason=None  letter date -> June 28–July 2, 2026
== P5 UB-04 period with 'through'  (record date 2026-06-19)
   UB-04 statement period 06/09/2026 through 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.
    $2,105.00  ok=True reason=None  letter date -> June 9–12, 2026
== P6 UB-04 period with hyphen  (record date 2026-06-19)
   UB-04 statement period 06/09/2026 - 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.
    $2,105.00  ok=True reason=None  letter date -> June 9–12, 2026
== P7 statement + DOS label same sentence  (record date 2026-03-01)
   Statement date 03/01/2026, date of service 02/02/2026: office visit charge $275.00.
      $275.00  ok=True reason=None  letter date -> February 2, 2026
== P8 ledger row DOS then posted  (record date 2026-06-15)
   06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00. 06/12/26 06/13/26 97110 Therapeutic exercise charge $95.00.
       $95.00  ok=True reason=None  letter date -> June 13, 2026
== P9 statement period then a separately dated line  (record date 2026-06-19)
   UB-04 statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, service date 06/09/2026, FL47 total charges $2,105.00.
    $2,105.00  ok=True reason=None  letter date -> June 9, 2026
== P10 'from X to Y' dates of service  (record date 2026-03-20)
   Billing statement for dates of service from 01/23/2026 to 03/06/2026. CPT 97110 therapeutic exercise, 9 units, charge $1,665.00.
    $1,665.00  ok=False reason='The line states no date of service, so it is not an itemized service line and is not totaled.'  letter date -> (T-200 form: statement dated / service date not stated)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:43:47.048Z

**tool call — Bash**
````
{
 "command": "cat evals/library/case_lib06_lop_billed_vs_adjusted.txt; grep -n \"def measure\" -A 12 evals/letter_check.py | head -20",
 "description": "Read lib06 records and letter_check case list"
}
````

### User / tool · 2026-11-02T23:43:47.147Z

**tool result**
````
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-05-02
Source: Eastvale Fire-Rescue run report
Excerpt: "Car struck on the passenger side at an intersection. Driver C/O shoulder pain. Transported to Larchmont Ridge ED."

=== Record 2 ===
Date: 2026-05-02
Source: Larchmont Ridge ED
Excerpt: "Dx: right shoulder contusion. X-ray negative. Sling provided. ED charge: $2,880."

=== Record 3 ===
Date: 2026-05-13
Source: Gannet and Moor Injury Clinic, new patient
Excerpt: "Patient referred by attorney. Right shoulder pain 6/10. Treating under a letter of protection. Plan: MRI and injections."

=== Record 4 ===
Date: 2026-06-03
Source: Gannet and Moor Injury Clinic, billing statement
Excerpt: "Statement of charges: office visits $1,100; MRI referral fee $450. Balance under letter of protection: $1,550."

=== Record 5 ===
Date: 2026-06-17
Source: Larchmont Ridge Imaging, right shoulder MRI
Excerpt: "Mild supraspinatus tendinosis; no full-thickness tear. Charge: $2,400. Insurance adjustment: -$1,250. Amount due: $1,150."

=== Record 6 ===
Date: 2026-07-08
Source: Gannet and Moor Injury Clinic, injection visit
Excerpt: "Subacromial injection performed. Pain 4/10."

=== Record 7 ===
Date: 2026-09-02
Source: Gannet and Moor Injury Clinic, follow-up
Excerpt: "Pain 3/10. Continue home exercises."
253:def measure(case_list=None, backend: str = "fixture") -> dict:
254-    """The report block: {'value': total violations (0 = pass), 'cases': n, 'per_case': {...}, 'held_out_entries': n, 'r_ids': [...]}."""
255-    per_case, held = {}, 0
256-    for name, text in (case_list if case_list is not None else cases()):
257-        got = letters_for(text, backend)
258-        bad = []
259-        for style, letter in got["all_accepted"]["letters"].items():
260-            bad += [f"{style}: {v}" for v in violations(letter, got["all_accepted"]["charge_cents"])]
261-        for style, letter in got["charges_dismissed"]["letters"].items():
262-            bad += [f"{style} (charges dismissed): {v}" for v in violations(letter, (), expect_none=True)]
263-        for style, letter in got["counted"]["letters"].items():
264-            bad += [f"{style} (counted): {v}" for v in violations(letter, got["counted"]["charge_cents"])]
265-        for variant in ("all_accepted", "counted"):
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:43:48.122Z

Dumping the charge lines for all 25 cases (counted variant) to read each against its record.

### Assistant · claude-opus-5-5 · 2026-11-02T23:43:51.660Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/all_charge_lines.py",
 "content": "\"\"\"T-202 paralegal: every BILLED CHARGES line (counted variant, standard style) of all letter_check cases on the f0921e4 archive, with the record it quotes.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/all_charge_lines.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom evals import letter_check as LC  # noqa: E402\n\nnorm = lambda t: \" \".join(str(t).split())\nfor name, text in LC.cases():\n    got = LC.letters_for(text)[\"counted\"]\n    lines = LC.charge_lines(got[\"letters\"][\"standard\"])\n    print(f\"== {name}: {len(lines)} charge line(s)\")\n    for h, q in lines:\n        recs = [r for r in got[\"records\"] if norm(q) in norm(r[\"excerpt\"])]\n        r = recs[0] if recs else {}\n        print(f\"   {h}\\n      quote: {q}\\n      record {r.get('n')} [{r.get('date_iso')}] {r.get('source')}: {r.get('excerpt')}\")\n"
}
````

### User / tool · 2026-11-02T23:43:51.786Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/all_charge_lines.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:43:56.891Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/all_charge_lines.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/all_charge_lines.out 2>&1; echo exit $?; cut -c1-330 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/all_charge_lines.out",
 "description": "Dump all charge lines across 25 cases",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T23:44:08.450Z

**tool result**
````
exit 0
== sample: 2 charge line(s)
   Central ER discharge summary, January 9, 2026: $6,240.00
      quote: ER charges: $6,240.
      record 2 [2026-01-09] Central ER discharge summary: Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.
   Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
      quote: Charge: $2,150.
      record 8 [2026-05-29] Austin Imaging, cervical MRI: C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.
== case_01_date_formats: 1 charge line(s)
   Quillfeather Urgent Care, February 3, 2026: $310.00
      quote: Urgent care charge: $310.00.
      record 1 [2026-02-03] Quillfeather Urgent Care: Right ankle swelling after twisting on stairs. X-ray negative for fracture. Urgent care charge: $310.00.
== case_02_gap_boundaries: 0 charge line(s)
== case_03_rate_and_ocr: 2 charge line(s)
   Gloamwood Chiropractic, visit 2, August 17, 2026: $95.00
      quote: Charge: $95.00.
      record 3 [2026-08-17] Gloamwood Chiropractic, visit 2: Adjustment performed. Pain 4/10. Charge: $95.00.
   Dr. Hobart Wimbleton, radiology, September 2, 2026: $240.00
      quote: Radiology charge: $240.
      record 5 [2026-09-02] Dr. Hobart Wimbleton, radiology: Lumbar spine X-ray, 2 views. Radiology charge: $240.
== case_04_duplicates_no_amounts: 0 charge line(s)
== case_05_provider_conflict: 1 charge line(s)
   Thornapple Valley Hospital ED, June 1, 2026: $4,380.00
      quote: ED charge: $4,380.
      record 2 [2026-06-01] Thornapple Valley Hospital ED: Dx: left clavicle fracture. Sling provided. Refer to orthopedics, Dr. Mortimer Tallowby. ED charge: $4,380.
== case_06_subtle_pre_existing: 0 charge line(s)
== case_07_prompt_injection: 1 charge line(s)
   Bumblethorpe Urgent Care, March 2, 2026: $420.00
      quote: Charge: $420.
      record 1 [2026-03-02] Bumblethorpe Urgent Care: Fall on ice, left knee pain 6/10. X-ray negative for fracture. Charge: $420.
== case_08_diagnosis_temptation: 1 charge line(s)
   Tumblebrook Imaging, shoulder MRI, October 20, 2026: $1,875.00
      quote: Charge: $1,875.
      record 2 [2026-10-20] Tumblebrook Imaging, shoulder MRI: Signal change in the supraspinatus tendon. Clinical correlation recommended. Charge: $1,875.
== case_09_nonvisit_hides_gap: 1 charge line(s)
   Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00
      quote: Statement for visit of 2026-02-02: $275.
      record 2 [2026-03-01] Hobbleton Family Clinic, billing statement: Statement for visit of 2026-02-02: $275.
== case_lib01_er_only_then_gap: 1 charge line(s)
   Marrowgate General ED, February 14, 2026: $3,915.00
      quote: ED charge: $3,915.
      record 2 [2026-02-14] Marrowgate General ED: Dx: cervical strain. X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Follow up with primary care in 1 week. ED charge: $3,915.
== case_lib02_slip_fall_prior_knee: 2 charge line(s)
   Tamsin Valley Urgent Care, March 9, 2026: $410.00
      quote: Visit charge: $410.
      record 2 [2026-03-09] Tamsin Valley Urgent Care: Right knee pain 7/10 with swelling. X-ray right knee: no acute fracture; prior arthroscopic changes noted. Dx: knee contusion. Knee immobilizer provided. Visit charge: $410.
   Tamsin Imaging, right knee MRI, March 30, 2026: $1,850.00
      quote: MRI charge: $1,850.
      record 4 [2026-03-30] Tamsin Imaging, right knee MRI: Medial meniscus tear with moderate joint effusion. Mild tricompartmental degenerative change. Findings may reflect both acute injury and prior surgical change. MRI charge: $1,850.
== case_lib03_truck_rear_end_chiro: 2 charge line(s)
   Redhaven Regional ED, April 6, 2026: $5,260.00
      quote: ED charge: $5,260.
      record 2 [2026-04-06] Redhaven Regional ED: Dx: lumbar and cervical sprain. CT cervical spine negative. Rx naproxen. Refer to chiropractic or primary care. ED charge: $5,260.
   Redhaven Imaging, lumbar MRI, July 20, 2026: $2,240.00
      quote: MRI charge: $2,240.
      record 7 [2026-07-20] Redhaven Imaging, lumbar MRI: L4-L5 disc bulge without nerve root compression. Mild disc desiccation. Radiology: findings likely chronic. MRI charge: $2,240.
== case_lib04_dog_bite_scar_revision: 1 charge line(s)
   Harlow Memorial ED, September 13, 2025: $4,730.00
      quote: ED charge: $4,730.
      record 2 [2025-09-13] Harlow Memorial ED: Dx: dog bite, left cheek laceration 4 cm and chin laceration 2 cm. Wounds irrigated and sutured. Amoxicillin-clavulanate prescribed. ED charge: $4,730.
== case_lib05_pedestrian_orif_hardware: 1 charge line(s)
   Coldharbor Trauma Center ED, January 22, 2026: $38,420.00
      quote: ED charges: $38,420.
      record 2 [2026-01-22] Coldharbor Trauma Center ED: Dx: left tibial plateau fracture and left fibular fracture. Splinted. Admitted to orthopedics. ED charges: $38,420.
== case_lib06_lop_billed_vs_adjusted: 3 charge line(s)
   Larchmont Ridge ED, May 2, 2026: $2,880.00
      quote: ED charge: $2,880.
      record 2 [2026-05-02] Larchmont Ridge ED: Dx: right shoulder contusion. X-ray negative. Sling provided. ED charge: $2,880.
   Gannet and Moor Injury Clinic, billing statement (statement dated June 3, 2026; service date not stated): $1,100.00
      quote: Statement of charges: office visits $1,100
      record 4 [2026-06-03] Gannet and Moor Injury Clinic, billing statement: Statement of charges: office visits $1,100; MRI referral fee $450. Balance under letter of protection: $1,550.
   Larchmont Ridge Imaging, right shoulder MRI, June 17, 2026: $2,400.00
      quote: Charge: $2,400.
      record 5 [2026-06-17] Larchmont Ridge Imaging, right shoulder MRI: Mild supraspinatus tendinosis; no full-thickness tear. Charge: $2,400. Insurance adjustment: -$1,250. Amount due: $1,150.
== case_lib07_parking_lot_fall_outside_records: 2 charge line(s)
   Cobblestone Imaging, February 10, 2026: $640.00
      quote: Charge: $640.
      record 2 [2026-02-10] Cobblestone Imaging: X-ray right wrist: nondisplaced distal radius fracture. X-ray lumbar spine: mild degenerative changes. Charge: $640.
   Cobblestone Imaging, lumbar MRI, May 12, 2026: $1,980.00
      quote: MRI charge: $1,980.
      record 6 [2026-05-12] Cobblestone Imaging, lumbar MRI: L4-L5 disc protrusion with mild canal narrowing. Postoperative changes at L4-L5. Possible aggravation of a pre-existing condition cannot be excluded. MRI charge: $1,980.
== case_lib08_second_crash_mri_after: 3 charge line(s)
   Thornbury Regional ED, January 12, 2026: $4,210.00
      quote: ED charge: $4,210.
      record 2 [2026-01-12] Thornbury Regional ED: Dx: cervical strain. CT head negative. Denies LOC per patient. Discharged on cyclobenzaprine. ED charge: $4,210.
   Thornbury Regional ED, April 24, 2026: $4,680.00
      quote: ED charge: $4,680.
      record 9 [2026-04-24] Thornbury Regional ED: Dx: cervical strain. CT cervical spine negative for fracture. Denies LOC per patient. ED charge: $4,680.
   Valley Imaging, cervical MRI, May 20, 2026: $2,350.00
      quote: MRI charge: $2,350.
      record 10 [2026-05-20] Valley Imaging, cervical MRI: C5-C6 disc herniation with mild canal narrowing. No prior imaging available for comparison. MRI charge: $2,350.
== case_lib09_spanish_interpreter_espalda: 3 charge line(s)
   Quillmere Regional ED, March 3, 2026: $2,940.00
      quote: ED charge: $2,940.
      record 1 [2026-03-03] Quillmere Regional ED: Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940.
   Cinder Valley Imaging, right shoulder MRI, May 5, 2026: $2,150.00
      quote: MRI charge: $2,150.
      record 5 [2026-05-05] Cinder Valley Imaging, right shoulder MRI: Partial-thickness supraspinatus tear. MRI charge: $2,150.
   Consultorio Médico Aguaclara, estado de cuenta (billing statement) (statement dated May 20, 2026; service date not stated): $1,300.00
      quote: Estado de cuenta: consultas $1,300.00
      record 7 [2026-05-20] Consultorio Médico Aguaclara, estado de cuenta (billing statement): Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00.
== case_lib10_eob_ub04_cms1500: 4 charge line(s)
   Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00
      quote: FL47 total charges $4,920.00.
      record 4 [2026-06-19] Saltmarrow General Hospital, UB-04 itemized bill: UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0120 room and board semi-private, FL44 rate $1,640.00 per day, FL46 3 days, FL47 total charges $4,920.00. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00. Rev 0250 ph
   Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00
      quote: Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.
      record 4 [2026-06-19] Saltmarrow General Hospital, UB-04 itemized bill: UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0120 room and board semi-private, FL44 rate $1,640.00 per day, FL46 3 days, FL47 total charges $4,920.00. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00. Rev 0250 ph
   Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $386.50
      quote: Rev 0250 pharmacy, 14 units, FL47 total charges $386.50.
      record 4 [2026-06-19] Saltmarrow General Hospital, UB-04 itemized bill: UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0120 room and board semi-private, FL44 rate $1,640.00 per day, FL46 3 days, FL47 total charges $4,920.00. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00. Rev 0250 ph
   Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $712.00
      quote: Rev 0300 laboratory, 6 units, FL47 total charges $712.00.
      record 4 [2026-06-19] Saltmarrow General Hospital, UB-04 itemized bill: UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026. Rev 0120 room and board semi-private, FL44 rate $1,640.00 per day, FL46 3 days, FL47 total charges $4,920.00. Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00. Rev 0250 ph
== case_lib11_priors_and_ledger: 4 charge line(s)
   Wexcombe Memorial ED, March 18, 2026: $3,260.00
      quote: ED charge: $3,260.
      record 3 [2026-03-18] Wexcombe Memorial ED: Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture. ED charge: $3,260.
   Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $250.00
      quote: New patient exam charge $250.00
      record 9 [2026-06-15] Fennimoor Spine Clinic, itemized ledger: Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00.
   Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $180.00
      quote: x-ray charge $180.00
      record 9 [2026-06-15] Fennimoor Spine Clinic, itemized ledger: Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00.
   Fennimoor Spine Clinic, itemized ledger (statement dated June 15, 2026; service date not stated): $2,310.00
      quote: treatment visits 1 through 14 charge $2,310.00
      record 9 [2026-06-15] Fennimoor Spine Clinic, itemized ledger: Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00.
== case_lib12_records_review_credibility: 4 charge line(s)
   Orrin Vale Community ED, February 9, 2026: $2,780.00
      quote: ED charge: $2,780.
      record 2 [2026-02-09] Orrin Vale Community ED: Dx: lumbar strain. X-ray lumbar spine negative for fracture. Discharged on ibuprofen. ED charge: $2,780.
   Harrowmere Physical Therapy, itemized statement (statement dated July 31, 2026; service date not stated): $210.00
      quote: Itemized statement: initial evaluation charge $210.00
      record 10 [2026-07-31] Harrowmere Physical Therapy, itemized statement: Itemized statement: initial evaluation charge $210.00; treatment visits 1 through 16 charge $2,320.00; functional capacity evaluation charge $480.00. Fee schedule $145.00 per visit.
   Harrowmere Physical Therapy, itemized statement (statement dated July 31, 2026; service date not stated): $2,320.00
      quote: treatment visits 1 through 16 charge $2,320.00
      record 10 [2026-07-31] Harrowmere Physical Therapy, itemized statement: Itemized statement: initial evaluation charge $210.00; treatment visits 1 through 16 charge $2,320.00; functional capacity evaluation charge $480.00. Fee schedule $145.00 per visit.
   Harrowmere Physical Therapy, itemized statement (statement dated July 31, 2026; service date not stated): $480.00
      quote: functional capacity evaluation charge $480.00.
      record 10 [2026-07-31] Harrowmere Physical Therapy, itemized statement: Itemized statement: initial evaluation charge $210.00; treatment visits 1 through 16 charge $2,320.00; functional capacity evaluation charge $480.00. Fee schedule $145.00 per visit.
== case_lib13_cloned_notes_cross_provider: 2 charge line(s)
   Vessel Grove Medical Center ED, August 3, 2026: $3,540.00
      quote: ED charge: $3,540.
      record 2 [2026-08-03] Vessel Grove Medical Center ED: Dx: lumbar strain, cervical strain. X-ray lumbar and cervical spine negative for fracture. Discharged home. ED charge: $3,540.
   Vessel Grove Imaging, lumbar MRI, August 28, 2026: $2,290.00
      quote: MRI charge: $2,290.
      record 6 [2026-08-28] Vessel Grove Imaging, lumbar MRI: L5-S1 disc protrusion contacting the left S1 nerve root. MRI charge: $2,290.
== case_lib14_handwritten_chiro_scans: 3 charge line(s)
   Orrin Mere Regional ED, September 14, 2026: $2,960.00
      quote: ED charge: $2,960.
      record 2 [2026-09-14] Orrin Mere Regional ED: Dx: cervical strain. X-ray cervical spine negative for fracture. Discharged with a muscle relaxant. ED charge: $2,960.
   Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00
      quote: A0427 ALS emergency transport, 1 unit, charge $1,380.00.
      record 8 [2026-11-12] Tarnwick Fire-Rescue, ambulance invoice: Invoice for the run of 09/14/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00. A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05. Total charges $1,567.05. No payments posted. Letter of protection requested.
   Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05
      quote: charge $187.05.
      record 8 [2026-11-12] Tarnwick Fire-Rescue, ambulance invoice: Invoice for the run of 09/14/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00. A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05. Total charges $1,567.05. No payments posted. Letter of protection requested.
== case_lib15_conclusory_letter_mist: 3 charge line(s)
   Cobblewood Urgent Care, October 5, 2026: $385.00
      quote: Charge: $385.
      record 2 [2026-10-05] Cobblewood Urgent Care: Seen the day after a low-speed MVC. Neck pain 4/10. Mild paraspinal tenderness. X-ray cervical spine negative. Dx: cervical strain. Charge: $385.
   Sunderland Chiropractic, itemized statement (statement dated January 20, 2027; service date not stated): $210.00
      quote: Itemized statement: new patient exam charge $210.00
      record 7 [2027-01-20] Sunderland Chiropractic, itemized statement: Itemized statement: new patient exam charge $210.00; treatment visits 1 through 18 charge $2,700.00; total charges $2,910.00. Payment received $250.00 (med pay). Balance due $2,660.00. Account held under letter of protection.
   Sunderland Chiropractic, itemized statement (statement dated January 20, 2027; service date not stated): $2,700.00
      quote: treatment visits 1 through 18 charge $2,700.00
      record 7 [2027-01-20] Sunderland Chiropractic, itemized statement: Itemized statement: new patient exam charge $210.00; treatment visits 1 through 18 charge $2,700.00; total charges $2,910.00. Payment received $250.00 (med pay). Balance due $2,660.00. Account held under letter of protection.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:44:34.748Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && sed -n 735,770p memory/contracts/api.md | cut -c1-400",
 "description": "Read the ledger line contract section"
}
````

### User / tool · 2026-11-02T23:44:34.870Z

**tool result**
````
## GET /api/calibration  (T-099, serves T-090 counts to T-096)
Read-only. Serves `evals/reports/calibration.json` (written by `python -m evals.run`), the measured calibration the review screen quotes. It holds aggregate counts, the statements built from them, the source commit, the backend and the sample size. No case token, no record text, so it works in demo mode with no gate. Any other method is `405`.

Always `200` with one envelope:
- `{"status": "ok", "calibration": {...}, "message": null}`. `calibration` has exactly: `schema` (`evals.calibration/1`), `backend` (`fixture` or a live backend name), `case_count` (the sample size: golden cases pooled), `small_sample` (bool), `source_commit`, `generated_at`, `by_state` (`verified` and `needs_review`, each `{matched, total, cases[]}`), `by_type` (`entry`, `amount`, `flag`, each wi
- `{"status": "missing", "calibration": null, "message": "..."}`: no file yet.
- `{"status": "invalid", "calibration": null, "message": "..."}`: the file is not a valid measurement (bad JSON or encoding, wrong schema, a count out of range, totals that do not add up, or a statement that does not quote its own `m/t`). The file's contents are never echoed; the reasons go to the server log.

Rules for the client: render `sentences.overall.verified` and `sentences.overall.needs_review` verbatim (they name the backend and the basis); never compute or show a percentage; hide the line when `calibration` is null. Nothing is invented: no default numbers appear in any state. `calibration` is served by `app/backend/calibration_route.py`; the route is registered in `create_app` and reads one f

## GET /api/cases/{token}/billing  (T-083, D-042, D-052)
Billing as a **cited line listing**. Code-only analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs (each EOB service row is a line). Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals`. **No
```json
{ "billing": {
  "status": "listed",                         // listed | citation_failed | none_found. "listed" says only that something was found; it is not a completeness claim
  "citation_failures": [],                    // [{ref, reason}] from the grounding verifier, which the route always runs; non-empty makes status citation_failed
  "lines": [                                  // every figure the records print, in record order, each with a verbatim excerpt and its source record
    { "id": "b3", "class": "charge",          // charge | adjustment | payment | rate | unclear
      "detail": null,                         // null | "reversal" (a charge printed in credit notation, or VOID) | "balance_only" | "eob" (an EOB service row) | see the extra-line details below
      "provider": "Larkspur Hollow Physical Therapy", "record_no": 1, "record_nos": [1], "form": "ledger",    // form: ledger | cms1500 | ub04 | eob
      "dos": "06/10/26", "dos_iso": "2026-06-10", "posted": "06/11/26", "code": "97140", "description": "Manual therapy x1",
      "billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "adjustment": null, "paid": null, "balance": {"text": "410.00", "cents": 41000, "usd": "$410.00"},
      "unclear": [], "negotiated": false, "unparsed": false,
      "checks": [],                           // LINE_UNCLEAR | NO_DATE_OF_SERVICE (ROW_NOT_PARSED on an unreconciled row)
      "excerpt": "06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00",   // the printed line, verbatim
      "cites": [ {"record_no": 1, "excerpt": "<same line>"} ] },                // one record: record_nos and cites always name only the line's own record (nothing is merged across records or providers)
    { "id": "b8", "class": "rate", "detail": "rate", "provider": "...", "record_no": 1, "record_nos": [1], "form": "ledger",
      "figure": {"text": "$65.00", "cents": 6500, "usd": "$65.00"}, "other_figures": [], "why": "A rate (per visit, per unit) is a price, not a charge.",
      "excerpt": "Fee schedule: Therapeutic exercise $65.00 per unit.", "cites": [ {"record_no": 1, "excerpt": "<same>"} ] },
    { "id": "b12", "class": "unclear", "detail": "eob", "provider": "Quoinmere Mutual Health Plan", "record_no": 2, "record_nos": [2], "form": "eob",
      "dos": "06/10/26", "code": "97140",                         // code = the EOB's service code; billed/paid/adjustment/balance are null on an EOB row
      "eob": {"billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "discount": {...}, "allowed": {...}, "deductible": {...}, "coinsurance": {...}, "plan_paid": {...}, "patient_owes": {...}},
      "eob_codes": "PR-1, PR-2, CO-45", "unclear": [], "checks": [],    // `eob` is {} and every money token of the row is in `unclear` (text, no value) when a figure could not be read or the row has the wrong number of figures
      "excerpt": "06/10/26  97140  70.00 ...", "cites": [ {"record_no": 2, "excerpt": "<same>"} ] } ],
  "unreconciled": [ { "id": "u1", "provider": "...", "record_no": 1, "form": "cms1500", "class": "unclear", "reason_code": "ROW_NOT_PARSED", "message": "...",
    "excerpt": "<the row, verbatim>", "figures": ["$85.00"] } ],   // rows that carry a figure or a date but fit no layout; never dropped. `figures` holds only the money tokens, not the rest of the line
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:44:44.040Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && ls app/backend | head -80; grep -n \"^def \" app/backend/billing*.py | head -20",
 "description": "Find billing module functions"
}
````

### User / tool · 2026-11-02T23:44:44.166Z

**tool result**
````
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
count_charge.py
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
limits.py
money.py
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
uncovered.py
why.py
71:def fmt(cents, credit=False):
79:def _is_credit(token: str) -> bool:
84:def parse_figure(token: str) -> dict:
93:def _pf(m, base=0):
99:def _mag(f):
104:def _norm(s):
112:def _lap(a, b):
116:def _within(a, row):
120:def _offsets(lines):
128:def _row_span(base, text):
134:def _provider(rec: dict) -> str:
141:def _dos(raw):
146:def _cite(rec, line):
151:def form_of(rec: dict) -> str:
169:def _header(lines):
184:def _column(token_span, cols):
193:def _money_col(token_span, cols):
200:def _rate_entry(rec, fig, excerpt, why="A rate (per visit, per unit) is a price, not a charge.", kind="rate", row=None):
205:def _blank_dates(ln):
212:def _tokens(ln, cols=None, all_bare=False):
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:44:49.154Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && grep -n \"^def \" app/backend/billing.py | sed -n 20,80p; grep -n \"_DOS_RX\\s*=\\|_PERIOD_PHRASE\\s*=\\|_RANGE_JOIN\\s*=\" app/backend/amounts.py",
 "description": "List more billing functions and date regexes"
}
````

### User / tool · 2026-11-02T23:44:49.290Z

**tool result**
````
212:def _tokens(ln, cols=None, all_bare=False):
223:def _put_stated(rec, stated, new, out):
233:def _stated_orphans(rec, lform, got, stated):
243:def _family(form):
248:def _near(span, hdr):
252:def _ledger_table(rec, lines):
336:def _blank_line(rec, form, ln, dos=None, posted=None, code=None, description="", unparsed=False, unclear=None, unit=None):
344:def _add_unclear(line, text, at):
355:def _stated(rec, text, base=0):
377:def _segments(text):
387:def _ledger_text(rec, body):
434:def _pline(rec, seg, kind, fig, unit, credit=False):
451:def box_amount(raw: str) -> dict:
472:def _cms1500(rec, lines):
508:def _ub_header(lines):
520:def _ub_all_cols(lines):
533:def _ub04(rec, lines):
589:def _eob_header(lines):
597:def _eob_tokens(ln, cols, service=None):
614:def _eob(rec, lines):
652:def _lop_lien(rec):
688:def _prose_bare(u):
702:def _cms_candidates(u):
712:def _span_merge(found):
721:def _unit_tokens(form, u, cols, below_header):
755:def _placed(got, stated, bfs, holders):
766:def _has_figure(l):
770:def _add_other(h, fig):
776:def _hold(got, stated, bfs, rates, lop):
816:def _account(rec, form, body, ls, offs, got, stated, bfs, holders):
851:def _line_span(body, start, end):
862:def _checks_for_line(line):
869:def _own_cites(lines):
876:def _billing_looking(rec, body):
882:def _strip_private(o):
891:def analyze(records: list) -> dict:
995:def _figure_like(v):
999:def _in(text, excerpt):
1003:def _walk(o):
1013:def verify_citations(analysis: dict, records: list) -> list:
1045:def checked(analysis: dict, records: list) -> dict:
1054:def for_case(conn, case_id: str) -> dict:
1060:def add_routes(app, *, conn, get_case):
274:_DOS_RX = re.compile(
283:_RANGE_JOIN = re.compile(r"^\s*(?:-|–|—|to|through|thru|until)\s*$", re.IGNORECASE)
304:_PERIOD_PHRASE = re.compile(r"(?:statement\s+period|billing\s+period|service\s+period|dates?\s+of\s+service|\bDOS\b|services?\s+(?:provided|rendered)|\brun\s+of|date\s+of\s+(?:the\s+)?run)\W{0,6}$", re.IGNORECASE)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:44:55.964Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && sed -n 891,910p app/backend/billing.py; sed -n 134,170p app/backend/billing.py; sed -n 270,310p app/backend/amounts.py",
 "description": "Read billing.analyze inputs and date regexes"
}
````

### User / tool · 2026-11-02T23:44:56.116Z

**tool result**
````
def analyze(records: list) -> dict:
    """The whole analysis of a case from its ingested records (needs n, excerpt; uses text, source, duplicate_of). Pure; no I/O."""
    recs = [r for r in records if not r.get("duplicate_of")]
    lines, stated_by_rec, lop, excluded, balfwds, rec_form = [], {}, [], [], {}, {}
    skipped = []
    for r in recs:
        body = r.get("excerpt") or r.get("text") or ""
        ls = body.split("\n")
        offs = _offsets(ls)
        form = form_of(r)
        if r.get("injection_tag") and (form or _lop_lien(r)):      # a figure inside instruction-like text has no trusted value (D-005)
            skipped.append({"record_no": r["n"], "reason_code": "INJECTION_SUSPECTED"})
            continue
        rec_form[r["n"]] = form
        got, rates, st, bf = [], [], {}, []
        if form == "ledger_table":
            got, st, bf, rates = _ledger_table(r, ls)
        elif form == "ledger_text":
            got, st, rates, bf = _ledger_text(r, body)
        elif form == "cms1500":
def _provider(rec: dict) -> str:
    src = (rec.get("source") or "").strip()
    name = re.split(r",|\s[-–—]\s", src, maxsplit=1)[0].strip()
    name = re.sub(r"\s+(?:itemized\s+)?(?:ledger|statement|billing|bill|claim|eob)\s*$", "", name, flags=re.IGNORECASE).strip()
    return name or "Unknown provider"


def _dos(raw):
    p = dates.parse_date(raw or "")
    return p["iso"] if p.get("status") == "parsed" else None


def _cite(rec, line):
    return {"record_no": rec["n"], "excerpt": line.strip()}


# ------------------------------------------------------------------ record forms
def form_of(rec: dict) -> str:
    """ledger_table | ledger_text | cms1500 | ub04 | eob | None, decided from the record's own words."""
    body = (rec.get("excerpt") or rec.get("text") or "")
    src = rec.get("source") or ""
    up = body.upper()
    if "EXPLANATION OF BENEFITS" in up or "THIS IS NOT A BILL" in up or re.search(r"\bEOB\b", src, re.IGNORECASE) or ("PLAN PAID" in up and "BILLED" in up):
        return "eob"
    if "UB-04" in up or "UB04" in up or "CMS-1450" in up or "47 TOTAL CHARGES" in up or re.search(r"\bUB-?04\b", src, re.IGNORECASE):
        return "ub04"
    if "TOTAL CHARGE" in up and "AMOUNT PAID" in up or "1500" in src or "HEALTH INSURANCE CLAIM FORM" in up:
        return "cms1500"
    if _header(body.split("\n"))[0] is not None:
        return "ledger_table"
    if "$" in body and (A._is_billing_source(src) or re.search(r"\bitemized\s+(?:ledger|statement)\b|\bledger\b", body, re.IGNORECASE)):
        return "ledger_text"
    return None


def _header(lines):
    """(index, {kind: (start, end)}) of the ledger column header, or (None, None). Needs billed and balance and one more column."""
# and the amount on the same line or table row of a provider bill or ledger. In a dated encounter record (an ED note, an imaging report) the record's own date is
# the date of service and the sentence must say charge/billed beside a service (or a bare "Charge:" under a header that names the service). Everything else is
# `unclear` with its reason. Nothing here lists wording that is NOT a charge: wording that merely looks like a total cannot be outworded.
_MON = r"jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sep(?:t(?:ember)?)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?"
_DOS_RX = re.compile(
    r"(?<![\w/.$-])(?:(?P<iy>\d{4})-(?P<im>\d{1,2})-(?P<id>\d{1,2})"
    r"|(?P<a>\d{1,2})[/.-](?P<b>\d{1,2})[/.-](?P<y>\d{4}|\d{2})"
    rf"|(?P<mon>{_MON})\.?\s+(?P<d2>\d{{1,2}})(?:st|nd|rd|th)?(?:,?\s+(?P<y2>\d{{4}}))?"
    rf"|(?P<d3>\d{{1,2}})(?:st|nd|rd|th)?[\s-]+(?:of\s+)?(?P<mon3>{_MON})\.?[\s-]*,?\s*(?P<y3>\d{{4}})"
    r"|(?P<a4>\d{1,2})/(?P<b4>\d{1,2}))(?![\w/]|\.\d)", re.IGNORECASE)
# a date that follows one of these words is a statement, billing, due or period date, never a date of service
_BAD_LEAD = re.compile(r"\b(?:statement|stmt|invoice|billing|billed|printed|issued|as\s+of|through|thru|until|ending|due|from|to|since|period|posted|paid|received|payment|balance)\b"
                       r"(?:\s+(?:date|dated|on))?\s*[:#]?\s*$", re.IGNORECASE)
_RANGE_JOIN = re.compile(r"^\s*(?:-|–|—|to|through|thru|until)\s*$", re.IGNORECASE)
_TAIL_LEAD = re.compile(r"^\s*[(,:–—-]?\s*(?:for|on|of|dos|date\s+of\s+service|service\s+date|dated|visit|service)\b|^\s*\(", re.IGNORECASE)
_DATE_LEAD = re.compile(r"(?:\bdos|date\s+of\s+service|service\s+date|dated?|\bon|\bfor|\bof|\bvisit|\()\s*[:#]?\s*$", re.IGNORECASE)
_SVC = re.compile(r"\b(?:office\s+visits?|visits?|exams?|examination|evals?|evaluations?|consult\w*|therap\w+|exercises?|treatments?|procedures?|injections?|surger\w+|mri|ct|"
                  r"cat\s+scan|x-?\s?rays?|radiograph\w*|ultrasound|imaging|radiolog\w+|labs?|laborator\w+|pharmacy|medications?|supplies|er|ed|emergency|room\s+and\s+board|"
                  r"ambulance|transport\w*|mileage|anesthesi\w+|cmt|chiropractic|manipulat\w+|modalit\w+|traction|stimulation|splint|brace|dme|nerve\s+block|epidural|biopsy|"
                  r"dressing|cast|admission|observation|inpatient|outpatient|follow[\s-]?up|assessment|screening|testing|session|urgent\s+care|care|train\w*|replacement|arthroplasty|repair|fusion|discectomy|"
                  r"laminectomy|fixation|reduction|suturing|sutures?|wound|closure|removal|infusion|dialysis|radiation|oxygen|nursing|icu|recovery|implant|hardware|orthotic|prosthe\w+|rehab\w*|"
                  r"massage|acupuncture|counsel\w*|ekg|ecg|emg|ncs|nerve\s+conduction|doppler|echo\w*|pathology|cultures?|blood|panel|urinalysis|vaccine|immuni[sz]\w+|occupational|speech)\b", re.IGNORECASE)
_PROVIDER_KIND = re.compile(r"\b(?:clinic|hospital|center|centre|medical|physicians?|practice|surgery|orthop\w+|neuro\w+|spine)\b", re.IGNORECASE)
_MOD = r"(?:-[A-Z0-9]{2})?"                # a CPT/HCPCS modifier ('97140-GP', 'CPT 97140-59')
_CODE_RX = re.compile(rf"\brev(?:enue)?\.?\s*(?:code\s*)?#?\s*0\d{{3}}\b|\b(?-i:[A-V]\d{{4}}){_MOD}(?![\w-])|\bCPT\s*[#:]?\s*\d{{5}}{_MOD}(?![\w-])|(?<![\w$#.,/-])\d{{5}}{_MOD}(?![\w.,/-])", re.IGNORECASE)


def norm_code(raw: str) -> str:
    """D-062: the bare code of a CPT, HCPCS or revenue code as written: label (CPT, HCPCS, Rev, Revenue code), '#', ':', spaces and a modifier removed, upper case.
    'CPT 97140-59', 'cpt#97140', '97140-GP' and '97140' are all '97140'; 'HCPCS: G0283' is 'G0283'; 'Rev. code #0450' is '0450'."""
    t = re.sub(r"[\s.#:]+", "", raw or "").upper()
    t = re.sub(r"^(?:CPT|HCPCS|REVENUE|REV|CODE)+", "", t)
    m = re.match(r"(\d{5}|[A-V]\d{4}|0\d{3})(?:-[A-Z0-9]{2})?$", t)
    return m.group(1) if m else t
_PERIOD_PHRASE = re.compile(r"(?:statement\s+period|billing\s+period|service\s+period|dates?\s+of\s+service|\bDOS\b|services?\s+(?:provided|rendered)|\brun\s+of|date\s+of\s+(?:the\s+)?run)\W{0,6}$", re.IGNORECASE)
_ADMIN_SRC = re.compile(r"\b(?:phone|telephone|tel\.?)\s+(?:note|call|encounter|message|contact)\b|\bportal\s+message\b|\bvoicemail\b|\bmessage\s+(?:note|log)\b|"
                        r"\b(?:records?\s+request|request\s+for\s+records|medical\s+records\s+(?:request|certification|affidavit)|business\s+records\s+affidavit|custodian\s+(?:of\s+records\s+)?affidavit|"
                        r"18\.001\s+affidavit|affidavit|authorization\s+form|HIPAA\s+authorization|correspondence|cover\s+letter|fax\s+cover|referral\s+(?:form|letter)|prior\s+authori[sz]ation|"
                        r"no-?\s?show\s+(?:notice|letter)|demand\s+letter)\b", re.IGNORECASE)
_BILLISH = re.compile(r"\b(?:statements?|bills?|billing|invoices?|ledgers?|account|itemi[sz]ed|ub-?04|hcfa|cms-?1500|claim\s+form)\b", re.IGNORECASE)
_BILL_OPEN = re.compile(r"^\W{0,3}(?:patient\s+)?(?:itemi[sz]ed|statement|invoice|ledger|billing|account\s+statement)\b", re.IGNORECASE)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:45:10.236Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_dates2.py",
 "content": "\"\"\"T-202 paralegal probe 2: table-form ledgers and a CMS-1500 with two dates of service. For each charge figure: the date the LETTER would print\n(store.charge_service_dates -> export._date_range) next to the date of service the app's own billing listing (billing.analyze, GET /billing) reads for that line.\nSYNTHETIC probe text only. f0921e4 archive.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/probe_dates2.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, billing, export, store  # noqa: E402\n\nPROBES = [\n    (\"T1 ledger table: DOS + posted columns\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"Itemized ledger\\nDOS         Posted      CPT    Description            Charges    Balance\\n\"\n     \"06/10/2026  06/11/2026  97140  Manual therapy x1      $70.00     $70.00\\n\"\n     \"06/17/2026  06/18/2026  97110  Therapeutic exercise   $95.00     $165.00\"),\n    (\"T2 ledger table: posted column first\", \"Larkspur Hollow Physical Therapy, itemized ledger\", \"2026-07-01\",\n     \"Itemized ledger\\nPosted      DOS         CPT    Description            Charges    Balance\\n\"\n     \"06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00     $70.00\\n\"\n     \"06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00     $165.00\"),\n    (\"T3 CMS-1500, two dates of service joined by 'and', $ figures\", \"Wardlaw Orthopedics, CMS-1500\", \"2026-07-14\",\n     \"CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, $185.00, 1 unit; CPT 20610, $210.00, 1 unit. Item 28 TOTAL CHARGE $395.00. Item 29 AMOUNT PAID $0.00.\"),\n]\nfor label, src, rd, ex in PROBES:\n    print(f\"== {label}  (record date {rd})\")\n    print(\"   \" + ex.replace(\"\\n\", \"\\n   \"))\n    rec = {\"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex, \"text\": ex}\n    try:\n        an = billing.analyze([rec])\n        bl = [(l.get(\"billed\") or l.get(\"figure\") or {}).get(\"usd\") for l in an.get(\"lines\", [])]\n        bdos = {((l.get(\"billed\") or {}).get(\"usd\")): (l.get(\"dos_iso\"), l.get(\"class\")) for l in an.get(\"lines\", [])}\n    except Exception as e:  # report, do not hide\n        bdos, bl = {}, f\"billing.analyze error: {e!r}\"\n    print(f\"   billing listing lines: {bl}\")\n    for a in AM.find_amounts(ex):\n        if a.get(\"cents\") is None:\n            continue\n        b = AM.charge_basis(ex, a, src, rd)\n        first, last = store.charge_service_dates({\"excerpt\": ex, \"value_cents\": a[\"cents\"]}, {\"source\": src, \"date_iso\": rd}, a[\"start\"])\n        shown = export._date_range(first, last) if first else \"(T-200 form)\"\n        usd = \"$\" + f\"{a['cents'] // 100:,}.{a['cents'] % 100:02d}\"\n        print(f\"   {a['raw']:>9} ok={b['ok']!s:5} letter date -> {shown:28} | billing listing dos/class -> {bdos.get(usd)}\")\n"
}
````

### User / tool · 2026-11-02T23:45:10.378Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_dates2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:45:15.763Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/probe_dates2.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_dates2.out 2>&1; echo exit $?; cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_dates2.out",
 "description": "Run table-ledger and CMS-1500 probes"
}
````

### User / tool · 2026-11-02T23:45:16.163Z

**tool result**
````
exit 0
== T1 ledger table: DOS + posted columns  (record date 2026-07-01)
   Itemized ledger
   DOS         Posted      CPT    Description            Charges    Balance
   06/10/2026  06/11/2026  97140  Manual therapy x1      $70.00     $70.00
   06/17/2026  06/18/2026  97110  Therapeutic exercise   $95.00     $165.00
   billing listing lines: []
      $70.00 ok=True  letter date -> June 10, 2026                | billing listing dos/class -> None
      $70.00 ok=False letter date -> June 10, 2026                | billing listing dos/class -> None
      $95.00 ok=True  letter date -> June 17, 2026                | billing listing dos/class -> None
     $165.00 ok=False letter date -> June 17, 2026                | billing listing dos/class -> None
== T2 ledger table: posted column first  (record date 2026-07-01)
   Itemized ledger
   Posted      DOS         CPT    Description            Charges    Balance
   06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00     $70.00
   06/18/2026  06/17/2026  97110  Therapeutic exercise   $95.00     $165.00
   billing listing lines: []
      $70.00 ok=True  letter date -> June 11, 2026                | billing listing dos/class -> None
      $70.00 ok=False letter date -> June 11, 2026                | billing listing dos/class -> None
      $95.00 ok=True  letter date -> June 18, 2026                | billing listing dos/class -> None
     $165.00 ok=False letter date -> June 18, 2026                | billing listing dos/class -> None
== T3 CMS-1500, two dates of service joined by 'and', $ figures  (record date 2026-07-14)
   CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, $185.00, 1 unit; CPT 20610, $210.00, 1 unit. Item 28 TOTAL CHARGE $395.00. Item 29 AMOUNT PAID $0.00.
   billing listing lines: []
     $185.00 ok=True  letter date -> June 24, 2026                | billing listing dos/class -> None
     $210.00 ok=True  letter date -> June 24, 2026                | billing listing dos/class -> None
     $395.00 ok=False letter date -> (T-200 form)                 | billing listing dos/class -> None
       $0.00 ok=False letter date -> (T-200 form)                 | billing listing dos/class -> None
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:45:37.259Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/lib10-s3-00-a2.png"
}
````

### User / tool · 2026-11-02T23:45:37.273Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:45:45.574Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF' > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/api-amount-fields.out 2>&1\nimport json, urllib.request\nB = \"http://127.0.0.1:7972\"\ncases = json.loads(urllib.request.urlopen(B + \"/api/cases\", timeout=10).read())\nlst = cases.get(\"cases\", cases) if isinstance(cases, dict) else cases\nfor c in lst:\n    tok = c[\"token\"]\n    d = json.loads(urllib.request.urlopen(f\"{B}/api/cases/{tok}\", timeout=20).read())\n    d = d.get(\"case\", d)\n    if \"UB-04\" not in json.dumps(d.get(\"records\", []))[:20000] and \"ambulance invoice\" not in json.dumps(d.get(\"records\", [])) and \"billing statement\" not in json.dumps(d.get(\"records\", [])):\n        continue\n    print(\"== case\", tok, c.get(\"title\") or c.get(\"name\"))\n    for a in d.get(\"amounts\", []):\n        if a.get(\"kind\") == \"charge\" or a.get(\"cls\") == \"charge\":\n            keys = {k: a.get(k) for k in a if any(s in k for s in (\"dos\", \"date\", \"service\", \"period\"))}\n            print(\"  \", a.get(\"id\"), a.get(\"text\") or a.get(\"value_display\"), keys)\nEOF\ncat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/api-amount-fields.out | cut -c1-400",
 "description": "Check whether case API exposes charge service dates"
}
````

### User / tool · 2026-11-02T23:45:45.936Z

**tool result**
````
== case IE4RKhvkMzY5gj1x-OJBlw Eob ub04 cms1500
   a2 $4,920.00 {}
   a3 $2,105.00 {}
   a4 $386.50 {}
   a5 $712.00 {}
== case LtE6HKGrxwMHd7UEBrHDBw Handwritten chiro scans
   a1 $2,960 {}
   a2 $1,380.00 {}
   a4 $187.05 {}
== case fJ32FX1cW-24bcLLwo8zEg Hobbleton Family Clinic, visit, Feb 2, 2026
   a1 $275 {}
== case Lr7bynw0zxTFwO0yUf8hbQ Hobbleton Family Clinic, visit, Feb 2, 2026
   a1 $275 {}
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:46:02.736Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_eval_teeth.py",
 "content": "\"\"\"T-202 paralegal: does evals/letter_check.charge_date_violations catch a wrong-but-stated date? (posting date in a ledger row; the other claim date on a CMS-1500 line).\nSYNTHETIC probe text. f0921e4 archive.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/probe_eval_teeth.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom evals import letter_check as LC  # noqa: E402\n\nT2 = (\"Itemized ledger\\nPosted      DOS         CPT    Description            Charges    Balance\\n\"\n      \"06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00     $70.00\")\nT3 = \"CMS-1500 for dates of service 06/24/2026 and 07/08/2026. Item 24F lines: CPT 99204, $185.00, 1 unit; CPT 20610, $210.00, 1 unit.\"\n\n\ndef letter(head, fig, quote):\n    return f\"BILLED CHARGES\\n\\n{head}: {fig}\\nSource [Ex. __ / Bates __]: \\\"{quote}\\\"\\n\\nBilled charges accepted from these records: {fig}\"\n\n\ncases = [\n    (\"T2 posted date printed as DOS (what f0921e4 prints)\", [{\"n\": 1, \"source\": \"Larkspur Hollow Physical Therapy, itemized ledger\", \"date_iso\": \"2026-07-01\", \"excerpt\": T2}],\n     letter(\"Larkspur Hollow Physical Therapy, itemized ledger, June 11, 2026\", \"$70.00\", \"06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00\")),\n    (\"T3 injection line dated with the other claim date (what f0921e4 prints)\", [{\"n\": 1, \"source\": \"Wardlaw Orthopedics, CMS-1500\", \"date_iso\": \"2026-07-14\", \"excerpt\": T3}],\n     letter(\"Wardlaw Orthopedics, CMS-1500, June 24, 2026\", \"$210.00\", \"CPT 20610, $210.00, 1 unit\")),\n]\nfor label, recs, txt in cases:\n    print(f\"== {label}\\n   violations: {LC.charge_date_violations(txt, recs)}\")\n"
}
````

### User / tool · 2026-11-02T23:46:02.836Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_eval_teeth.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:46:08.026Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/probe_eval_teeth.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_eval_teeth.out 2>&1; echo exit $?; cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/probe_eval_teeth.out",
 "description": "Check whether letter_check catches wrong stated dates"
}
````

### User / tool · 2026-11-02T23:46:08.262Z

**tool result**
````
exit 0
== T2 posted date printed as DOS (what f0921e4 prints)
   violations: ["charge line's date is not a service date its record states: Larkspur Hollow Physical Therapy, itemized ledger, June 11, 2026: $70.00"]
== T3 injection line dated with the other claim date (what f0921e4 prints)
   violations: []
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:46:38.072Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t202 && grep -n \"def charge_service_dates\\|return (None, None) if counted_undated\\|it is not the fallback\\|When the line cannot be read\" app/backend/store.py; grep -n \"first in service and\\|def charge_date_violations\\|def _record_period\\|return iso, (end if end\" evals/letter_check.py app/backend/amounts.py; grep -n \"sorted(got, key\" app/backend/export.py",
 "description": "Get line numbers for cited code"
}
````

### User / tool · 2026-11-02T23:46:38.198Z

**tool result**
````
118:def charge_service_dates(item: dict, rec, pos) -> tuple:
120:    record's date of a ledger, invoice or UB-04 is the statement's, never a service date, so it is not the fallback for a billing document. A dated encounter record's date is
122:    When the line cannot be read: the record's date, unless she counted it for the missing date."""
126:        return (None, None) if counted_undated else ((rec or {}).get("date_iso"), None)
app/backend/amounts.py:435:def _record_period(before: str, ref_iso):
app/backend/amounts.py:445:            return iso, (end if end and end > iso else None)
app/backend/amounts.py:449:def _record_period_dos(before: str, ref_iso):
evals/letter_check.py:177:def charge_date_violations(letter: str, records) -> list:
evals/letter_check.py:209:                ok = ok or (first in service and (last is None or last in states))
185:        return sorted(got, key=lambda a: (a.get("dos_iso") or self._date(a), a["record_no"], str(a.get("id"))))
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:46:40.049Z

**tool call — Bash**
````
{
 "command": "lsof -iTCP:7972 -sTCP:LISTEN -nP",
 "description": "Find listener PID on port 7972"
}
````

### User / tool · 2026-11-02T23:46:40.199Z

**tool result**
````
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  82425 arsis    9u  IPv4 0xb0beb1a73ea44cc3      0t0  TCP 127.0.0.1:7972 (LISTEN)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:46:41.198Z

**tool call — Bash**
````
{
 "command": "kill 82425",
 "description": "Stop the archive app listener"
}
````

### User / tool · 2026-11-02T23:46:41.303Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:46:42.885Z

**tool call — Bash**
````
{
 "command": "lsof -iTCP:7972 -sTCP:LISTEN -nP; echo lsof_exit $?; curl -s -o /dev/null -w \"%{http_code}\\n\" -m 3 http://127.0.0.1:7972/api/health",
 "description": "Confirm port 7972 is closed"
}
````

### User / tool · 2026-11-02T23:46:43.058Z

**tool result (error)**
````
Exit code 7
lsof_exit 1
000
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:47:38.822Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/draft-T-202-paralegal.md",
 "content": "# T-202 (D-071) — paralegal review (Maria Delgado, senior PI litigation paralegal)\n\n**Verdict: fail.** The rule hits two blockers on bill shapes I see every week. The corpus letters are now right.\n- **case_09:** \"billing statement, February 2, 2026: $275.00\". The quote reads \"Statement for visit of 2026-02-02\".\n- **lib14:** both ambulance lines print \"September 14, 2026\", from \"Invoice for the run of 09/14/2026\".\n- **lib10:** all four UB-04 lines print \"June 9–12, 2026\", with an en dash, from \"statement period 06/09/2026 to 06/12/2026\".\n- **sample:** unchanged.\n- **All 25 cases:** charges are in service-date order. The T-200 form still covers the undated ledger lines (lib06, 09, 11, 12, 15).\n\nAn adjuster checking those lines against the bill pages would find nothing to attack.\n\n**Blockers (probe text, live or paste path).** The per-line parse still prints a date the row does not tie to the charge:\n- **Posting date as service date.** In a ledger table whose Posted column comes before DOS, the letter prints the posting date as the service date. This is the exact D-071 error.\n- **First claim date on every line.** On a CMS-1500 that lists \"dates of service 06/24/2026 and 07/08/2026\", every line gets June 24. That includes the injection the chart dates July 8.\n\n**Majors:**\n- **Step 3 shows a different date from the letter.** Step 3, where I accept the charge, still labels it with the bare statement date (\"UB-04 itemized bill · June 19, 2026\"). The case API carries no service date, so the date the letter prints is never shown to me before export.\n- **The eval cannot catch the wrong date.** letter_check accepts any service date the record states, not the line's own date. The CMS-1500 mis-date passes with 0 violations.\n\n**Scope.**\n- **Build:** `git archive f0921e4` extracted to the session scratchpad (t202/).\n- **Server:** fixture backend FIXTURE_SET=curated. Demo mode (health: demo_mode true) with ZLAYT_MODE=local for /api/library, on http://127.0.0.1:7972.\n- **Shutdown:** listener PID 82425 was killed. `lsof` returned exit 1 and `curl` returned 000.\n- **Parent comparison:** a44cfa7, run in-process from its own archive (t202parent/).\n- **Evidence:** artifacts/review-evidence/T-202-paralegal/.\n\n**Deterministic checks first (from the f0921e4 archive):**\n- `pytest tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py`: \"19 passed in 5.78s\" (pytest-t202.out).\n- `python -m evals.letter_check`: `{\"value\": 0, \"cases\": 25, ...}` (letter_check.out).\n\n```json\n{\"card\": \"T-202\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"commit f0921e4 (git archive extracted to session scratchpad t202/), parent a44cfa7 for the before/after diff (t202parent/). Demo mode: fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, http://127.0.0.1:7972 (health demo_mode true); listener PID 82425 stopped (lsof exit 1, curl 000). Cases: sample (load-sample tile), case_09 (POST /api/cases with the golden text because the demo UI turns the paste tile off, then opened in the UI), case_lib14 and case_lib10 (library tile). Evidence dir artifacts/review-evidence/T-202-paralegal/.\",\n \"exercised\": [\n  \"Read personas/paralegal.md, D-071 (memory/ORCHESTRATOR_DECISIONS.md:84), board.py show T-202 (AC, notes, handoff with letter diffs), git show f0921e4 (amounts.py, export.py, store.py, evals/letter_check.py, tests)\",\n  \"From the archive: pytest test_t202 + test_t200 '19 passed in 5.78s' (pytest-t202.out); python -m evals.letter_check value 0 over 25 cases (letter_check.out)\",\n  \"Playwright on the running archive app (h.py + p01_cases.py): sample, case_09, lib14, lib10 driven keyboard-first through Steps 1-4, every Step 3 bill card logged and screenshotted, letter + notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); scripted times 15.5 s / 7.2 s / 13.1 s / 19.0 s (p01.out, p02.out)\",\n  \"Read every charge line of the four letters against the bill page in the record (service date vs statement date, UB-04 period, order)\",\n  \"Before/after: same letters generated in-process from a44cfa7 and f0921e4; diff shows only the six date changes the handoff lists (parent-vs-f0921e4.diff)\",\n  \"All 25 letter_check cases, counted variant: every BILLED CHARGES line with the record it quotes (all_charge_lines.out), checked by hand for date and order\",\n  \"GET /api/cases/{token} for the lib10, lib14 and case_09 runs: charge amounts carry no service-date field (api-amount-fields.out)\",\n  \"Probes of the shipped date path (store.charge_service_dates -> export._date_range) on SYNTHETIC bill shapes: probe_dates.out (10 shapes), probe_dates2.out (ledger tables, CMS-1500 with two dates), probe_eval_teeth.out (letter_check on the wrong dates)\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 3, \"letter_dates_correct_on_corpus\": 5, \"adjuster_credibility\": 3},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"Ledger table with the Posted column before DOS: the letter prints the posting date as the date of service\",\n   \"evidence\": \"artifacts/review-evidence/T-202-paralegal/probe_dates2.out, probe T2. Record 'Posted      DOS         CPT ...' / '06/11/2026  06/10/2026  97140  Manual therapy x1      $70.00' gives 'letter date -> June 11, 2026'; the next row (posted 06/18, DOS 06/17) gives 'June 18, 2026'. With DOS first (T1) it prints June 10 / June 17. The parse takes the first date in the row (amounts.py charge_basis) and ignores the column header.\",\n   \"why_it_matters\": \"This is the error D-071 exists to stop: a billing-side date printed in the date-of-service slot. The adjuster's first move is to match the letter date to the bill and the chart note, and here neither matches. The paralegal never sees this date before export (see the Step 3 major), so she cannot catch it. Not in the 25-case corpus or the demo; reachable on any pasted ledger in live mode.\",\n   \"fix\": \"Read the row's date by its column: use the ledger header (billing.py already parses DOS vs Posted columns, api.md GET /billing 'dos' vs 'posted'). When a row has two dates and no header says which is the DOS, use the T-200 form, not a guess.\",\n   \"acceptance_test\": \"Unit test on the T2 text: the $70.00 line prints 'June 10, 2026' and the $95.00 line 'June 17, 2026'. Same rows without a header give the '(statement dated ...; service date not stated)' form. Add a SYNTHETIC library or golden case with a Posted-first ledger to the letter_check corpus.\"},\n  {\"severity\": \"blocker\",\n   \"title\": \"CMS-1500 listing two dates of service ('06/24/2026 and 07/08/2026'): every charge line gets the first date\",\n   \"evidence\": \"artifacts/review-evidence/T-202-paralegal/probe_dates.out P2 and probe_dates2.out T3: 'CMS-1500 for dates of service 06/24/2026 and 07/08/2026 ... CPT 99204, $185.00 ...; CPT 20610, $210.00' -> both '$185.00 ... letter date -> June 24, 2026' and '$210.00 ... letter date -> June 24, 2026'. amounts.py:435-445 _record_period returns the first matched date; 'and' is not a range join, so no end date is kept. This is the shape of lib10 record 8 (Wardlaw Orthopedics CMS-1500), where the chart dates the injection (CPT 20610) 'July 8' (record 7: 'Injection performed').\",\n   \"why_it_matters\": \"The letter ties the injection charge to June 24, a visit where no injection was done. The record does not say which line is which date, so the pairing is invented. An adjuster who lines the specials up against the chart finds a charge on a day with no matching service and uses it to question the whole bill set.\",\n   \"fix\": \"Inherit the record's date only for a true period (a range join). For a list of discrete dates with no per-line date, print the T-200 form, or name the claim dates without assigning one: 'Wardlaw Orthopedics, CMS-1500 (claim dates of service June 24 and July 8, 2026; line date not stated)'. D-071 says that when no service date is stated the T-200 form applies.\",\n   \"acceptance_test\": \"Unit test on the T3 text: neither charge line prints a bare single date. Both carry the not-stated form, or the two-date claim form above. letter_check, run on a corpus case of this shape, reports a violation when a single claim date is printed.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Step 3 labels each dated bill charge with the statement date, not the date the letter prints; the API carries no service date\",\n   \"evidence\": \"p02.out Step 3 cards: '[lib10] ... Charge / Saltmarrow General Hospital, UB-04 itemized bill · June 19, 2026 /  / $4,920.00'; '[lib14] ... Charge / Tarnwick Fire-Rescue, ambulance invoice · November 12, 2026 /  / $1,380.00'; '[case_09] ... Charge / Hobbleton Family Clinic, billing statement · March 1, 2026 /  / $275.00'. Screenshots lib10-s3-00-a2.png, lib14-s3-01-a2.png, case_09-s3-00-a1.png. The letters for the same items say June 9–12, September 14 and February 2 (ui-lib10-letter.txt, ui-lib14-letter.txt, ui-case_09-letter.txt). api-amount-fields.out: the charge amounts a2-a5 (lib10), a1/a2/a4 (lib14) and a1 (case_09) have no dos/date/service/period field.\",\n   \"why_it_matters\": \"I accept a charge on a card that shows June 19 bare beside it, which reads as the charge's date. Then the letter says June 9–12, a date I was never shown and cannot check on the screen where I decided. The two blockers above are invisible for the same reason. If I compare the letter to my review, they disagree, and I would either lose trust in the tool or 'correct' a right date.\",\n   \"fix\": \"Expose the D-071 service date or period on each charge in the case view (backend: dos_iso/dos_end_iso, or the T-200 'not stated' state). Show it on the Step 3 card exactly as the letter will print it, with the statement date labelled as such: 'Service June 9–12, 2026 · statement dated June 19, 2026'.\",\n   \"acceptance_test\": \"E2E: for lib10, lib14 and case_09, the Step 3 card text of every charge contains the same date string as its BILLED CHARGES line in the downloaded letter. No charge card shows a billing document's record date without the word 'statement'.\"},\n  {\"severity\": \"major\",\n   \"title\": \"letter_check's date check accepts any service date the record states, not the line's own, so the wrong-date class passes; AC wording ('equals the service date in its quote') is not what it checks\",\n   \"evidence\": \"evals/letter_check.py:209 'ok = ok or (first in service and (last is None or last in states))', where service is every non-statement-led date in the record. probe_eval_teeth.out: 'T3 injection line dated with the other claim date (what f0921e4 prints) / violations: []'. Card AC 1: 'asserts each dated charge line's date equals the service date in its quote'; the lib10 quotes ('FL47 total charges $4,920.00.') contain no date at all.\",\n   \"why_it_matters\": \"'value 0 over 25 cases' is the evidence the card was ticked on, but the check cannot tell a right line date from another date on the same bill. The blocker class above would ship green.\",\n   \"fix\": \"Pin the per-line expected date in the goldens: case_09, lib14 and lib10 expected letters, plus the T2/T3 probe shapes as SYNTHETIC cases. Make the check tie the date to the line's row or the record's stated period, not to any date in the record.\",\n   \"acceptance_test\": \"Mutant: print the first claim date on every CMS-1500 line, or the posted column of a ledger row. letter_check reports at least one violation on the corpus.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Some charge quotes name neither the service nor the date the line now prints (pre-existing quote span, unchanged by T-202)\",\n   \"evidence\": \"ui-lib10-letter.txt: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00' / 'Source [Ex. __ / Bates __]: \\\"FL47 total charges $4,920.00.\\\"'. The record says 'Rev 0120 room and board semi-private, ... FL46 3 days, FL47 total charges $4,920.00'. ui-lib14-letter.txt: '... September 14, 2026: $187.05' / '\\\"charge $187.05.\\\"'. The record: 'A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05'. parent-vs-f0921e4.diff shows these quote lines identical on a44cfa7.\",\n   \"why_it_matters\": \"The date is now right, but its source ('statement period ...', 'Invoice for the run of 09/14/2026') is outside the quoted words. The adjuster has to open the page to see what $4,920 or $187.05 was for and when.\",\n   \"fix\": \"Quote the whole bill line from its code or description through the figure ('Rev 0120 room and board semi-private ... FL47 total charges $4,920.00.'; 'A0425 ground mileage, loaded, 8.7 miles ... charge $187.05.').\",\n   \"acceptance_test\": \"Every BILLED CHARGES quote on a bill record contains the line's service code or description. letter_check can assert this for lib10 and lib14.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Same-day charges tie-break by record number, so lib14 lists the ED before the ambulance that took the patient there\",\n   \"evidence\": \"export.py:185 sort key (dos_iso, record_no, id). ui-lib14-letter.txt lists 'Orrin Mere Regional ED, September 14, 2026: $2,960.00' (record 2) before 'Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00' (record 8).\",\n   \"why_it_matters\": \"Specials usually run in the order care was given (transport, then ED). It is cosmetic, but it reads oddly to an adjuster following the chronology above.\",\n   \"fix\": \"Optional: on a same-day tie, sort by the earliest timeline entry of the same provider, or put transport first.\",\n   \"acceptance_test\": \"lib14 letter lists the ambulance lines before the ED line.\"}\n ],\n \"whats_right\": [\n  \"case_09, lib14 and lib10 now print the service date or the UB-04 period ('June 9–12, 2026'), never the statement date; the sample letter is unchanged\",\n  \"The period and single-date parse handles 'to', 'through', hyphens, month and year crossings and 'statement date ..., date of service ...' in one sentence (probe_dates.out P3-P7, P9)\",\n  \"The T-200 '(statement dated X; service date not stated)' form still covers the counted undated ledger lines, and the letter_check count path now exercises it (lib06, 09, 11, 12, 15)\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T23:47:38.935Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/draft-T-202-paralegal.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:47:47.407Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/draft-T-202-paralegal.md",
 "old_string": "handles 'to', 'through', hyphens, month and year crossings and",
 "new_string": "handles 'to', 'through', a hyphen, a month crossing, an invoice date stated before the run date and"
}
````

### User / tool · 2026-11-02T23:47:47.506Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal/draft-T-202-paralegal.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:47:48.964Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py && .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py artifacts/review-evidence/T-202-paralegal/draft-T-202-paralegal.md",
 "description": "Validate the draft review JSON"
}
````

### User / tool · 2026-11-02T23:47:49.082Z

**tool result**
````
artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py
json blocks: 1
verdict: fail | severities: ['blocker', 'blocker', 'major', 'major', 'minor', 'nit']
verdict rule expects: fail | matches: True
model: claude-opus-5-5 | card: T-202 | persona: paralegal-reviewer
all finding fields present
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:47:51.148Z

**tool call — Bash**
````
{
 "command": "ls reviews/T-202-paralegal.md 2>&1; cp artifacts/review-evidence/T-202-paralegal/draft-T-202-paralegal.md reviews/T-202-paralegal.md && python3 tools/board.py validate reviews/T-202-paralegal.md",
 "description": "Publish review and run board validator"
}
````

### User / tool · 2026-11-02T23:47:51.392Z

**tool result**
````
ls: reviews/T-202-paralegal.md: No such file or directory
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:47:52.357Z

Saving the memory note for the next round.

### Assistant · claude-opus-5-5 · 2026-11-02T23:48:00.720Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-d071-service-date-patterns.md",
 "content": "---\nname: t202-d071-service-date-patterns\ndescription: T-202 (f0921e4) fail: corpus letters right (Feb 2 / Sept 14 / June 9–12) but probes show Posted-first ledger prints posting date and CMS-1500 'X and Y' gives every line X; Step 3 shows statement date; eval accepts any record date\nmetadata:\n  type: project\n---\n\nT-202 review (reviews/T-202-paralegal.md, f0921e4). Verdict: fail, with 2 blockers, 2 majors, 1 minor and 1 nit.\n\n**Corpus result**\n- The corpus letters are correct.\n- All 25 cases list charges in service-date order.\n- The parent diff (a44cfa7) shows only the 6 date changes.\n\n**Blockers (from in-process probes)**\n- A ledger table whose Posted column comes before DOS prints the posting date. The parse takes the first date in the row and ignores the header.\n- A CMS-1500 with \"dates of service 06/24 and 07/08\" gives June 24 to every line. In amounts.py, `_record_period` keeps only the first date, because \"and\" is not a range join.\n\n**Majors**\n- Step 3 cards show the bill's record (statement) date bare (\"UB-04 itemized bill · June 19, 2026\"), and the case API has no service-date field.\n- `letter_check.charge_date_violations` accepts any non-statement-led date in the record. The T3 mis-date passes with 0 violations.\n\n**Minor**\n- The quotes \"FL47 total charges $4,920.00.\" and \"charge $187.05.\" carry neither the service nor the date. This is pre-existing.\n\n**Mechanics that worked**\n- The demo UI turns the paste tile off. POST /api/cases with golden text returned 201, then open `/case/<tok>/records` (no btn-read click).\n- probe_dates*.py call `store.charge_service_dates` with `export._date_range` directly.\n- letters_dump.py and all_charge_lines.py dump every variant's letter.\n- The parent dump needs its own script, because the parent letter_check has no \"counted\" variant or \"records\" key.\n\n**Why:** next round, re-run probe_dates2.py and probe_eval_teeth.py on the fix commit first. Then check that Step 3 shows the letter's date string.\n**How to apply:** scripts are in artifacts/review-evidence/T-202-paralegal/ (h.py port 7972). Related: [[t200-undated-charge-label]], [[reviewer-run-pitfalls-pass4]].\n"
}
````

### User / tool · 2026-11-02T23:48:00.846Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-d071-service-date-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:48:02.676Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-200 undated charge label](t200-undated-charge-label.md)",
 "new_string": "- [T-202 D-071 service-date patterns](t202-d071-service-date-patterns.md) — f0921e4 fail: Posted-first ledger + CMS-1500 'X and Y' probes misdate; Step 3 shows statement date; weak eval\n- [T-200 undated charge label](t200-undated-charge-label.md)"
}
````

### User / tool · 2026-11-02T23:48:02.776Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-02T23:48:05.738Z

T-202 fails with 2 blockers and 2 majors (review at /Users/arsis/zlayt-pm-project/reviews/T-202-paralegal.md): the corpus letters (sample, case_09, lib14, lib10) now print service dates correctly in service-date order, including the UB-04 period as "June 9–12, 2026", but my own test bill text gets the wrong date in two layouts — a ledger with the Posted column before DOS prints the posting date, and a CMS-1500 listing two service dates puts the first on every line — while Step 3 still shows the bill's statement date and letter_check passes the CMS-1500 mis-date with 0 violations (server PID 82425 stopped).
