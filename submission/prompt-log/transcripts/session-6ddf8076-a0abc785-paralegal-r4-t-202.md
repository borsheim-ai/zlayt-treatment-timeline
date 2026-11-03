# Subagent: Paralegal r4: T-202 (Paralegal r4: T-202)

Source: `agent-a0abc785176b4d665.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T01:58:46.623Z

Review T-202, round 4 (final), in /Users/arsis/zlayt-pm-project as the senior PI paralegal, starting from a fresh context. The fix commit is 8cb5bd2. Read reviews/T-202-paralegal-r3.md, D-071 amendment 2 and its note in memory/ORCHESTRATOR_DECISIONS.md, and the handoff.

Run a `git archive 8cb5bd2` copy in demo mode on your own port, and stop your PID afterward.
- Re-run every adversarial text from your rounds 1 to 3, including "next visit date" in an ER note, and the dotted-leader "Date of service.......01/09/2026".
- Each charge line must print either a correct service date or the fillable blank. A wrong date is a blocker.
- Generate the sample, case_09, lib10, lib11 and lib14 letters.

Report any private value only as <redacted>. Write reviews/T-202-paralegal-r4.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-opus-5-5 · 2026-11-03T01:58:49.393Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat personas/paralegal.md | head -c 200; echo; ls .claude/agent-memory/paralegal-reviewer/; cat .claude/agent-memory/paralegal-reviewer/t202-*.md .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md .claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md",
 "description": "Read persona header and relevant memory files"
}
````

### User / tool · 2026-11-03T01:58:49.498Z

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
t202-r3-allow-list-patterns.md
t209-confirm-sentence-patterns.md
t209-r3-patterns.md
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
name: t202-r3-allow-list-patterns
description: T-202 r3 (973b542) fail: allow-list + fillable blank fix r2, but 'next/last/previous/initial visit date' and 'seen on' in a visit note override its own date (sample ER Jan 9 prints Jan 16); letter_check enforces it
metadata:
  type: project
---

Review file: reviews/T-202-paralegal-r3.md (973b542). Verdict: fail, with 1 blocker, 3 minors and 1 nit.

**Fixed since r2**
- B1-B12 non-service dates: bills give the blank, and visit notes keep their own date.
- The not-stated wording is replaced by the D-071 addendum blank 'date of service [__________] (statement dated X)'.
- Notes have a CHARGES WITHOUT A CERTAIN DATE OF SERVICE section.
- Corpus letters are byte-identical to r2.

**Blocker: an allow-listed label that names another visit**
- "visit date" and "seen on" are trusted even after next/last/previous/initial. In a non-bill note, the labeled date wins over the record's date (service_date.py:43, fallback at :375).
- The after-statement check covers bills only (:291).
- Sample variant 'ER charges: $6,240, next visit date 01/16/2026.' prints January 16. bd72d5b printed January 9.
- letter_check passes the wrong line and fails the right one.

**Why:** an allow-list moves the risk from "unlabeled date" to "labeled but for another event". Next time, probe qualifiers before every allowed label (next/last/prior/initial/return/scheduled), and probe comma-joined clauses (a sentence break protects).

**How to apply:** scripts are in artifacts/review-evidence/T-202-paralegal-r3/:
- probe_r3.py loads the r2 PROBES lists by ast;
- probe_r3b.py and probe_r3c.py hold the other-visit and punctuation shapes;
- letters_dump_r3.py builds the SYNTHETIC sample variant;
- before_t202.py runs on a bd72d5b archive.

Port 7981, h.py and p01_cases.py (lib11 added).

Related: [[t202-r2-non-service-date-patterns]], [[t202-d071-service-date-patterns]].
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

### Assistant · claude-opus-5-5 · 2026-11-03T01:58:50.744Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat personas/paralegal.md | wc -l; git log --oneline -8; git show --stat 8cb5bd2 | head -40",
 "description": "Check persona length and fix commit"
}
````

### User / tool · 2026-11-03T01:58:50.875Z

**tool result**
````
      84
8cb5bd2 fix(backend): T-202 r4 D-071 amendment 2: only an identified encounter record lends its date; four prose labels; dotted leaders; declared record-type table; anchored blank
8521562 fix(frontend): Step 3 next step depends on the date reason: doubtful date checks the quote, no date looks outside it; statement-date, total and clip minors (T-209 r2)
88c73dd fix(frontend): Step 3 confirm note names the letter's fillable date blank (T-209)
68f67cc fix(frontend): T-204 r3 prepared AI-check panel says the prepared answers / the second AI check; guided footer neutral until health; allow-list narrowed to whole sentences; rerun label and guided walk tested
fc37fbc docs(architect): T-207 r2 LLM_VS_CODE row 3: a charge line with no certain date of service prints the fillable blank
8aa14e1 test(qa): T-208 r2 the AI translation label is exempt only with a translated entry's quote; label on an English letter fails
679b63e fix(frontend): T-204 r2 a prepared answer is never the AI's wording on the case rail, AI-check panel, audit, tray, banner or legends; whole-DOM observer walk of the prepared sample; condition waits
b96c08f test(qa): T-208 letter_check fails any AI or model wording in every carrier letter (25 cases, prepared and live); matrix e2e binds the provenance line to the case kind
commit 8cb5bd2e657408a2654117cb04fa173031c294a9
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 19:50:55 2026 -0600

    fix(backend): T-202 r4 D-071 amendment 2: only an identified encounter record lends its date; four prose labels; dotted leaders; declared record-type table; anchored blank
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/encounter_types.json             |  21 ++
 app/backend/service_date.py                  | 115 +++++++---
 app/backend/store.py                         |   6 +-
 evals/letter_check.py                        |  88 ++++++--
 memory/contracts/api.md                      |   2 +-
 tests/unit/test_t200_undated_charge_label.py |   3 +-
 tests/unit/test_t202_r3_allow_list.py        |   3 -
 tests/unit/test_t202_r4_encounter.py         | 310 +++++++++++++++++++++++++++
 8 files changed, 488 insertions(+), 60 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:58:51.807Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-03T01:58:51.815Z

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

### Assistant · claude-opus-5-5 · 2026-11-03T01:58:52.183Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r3.md"
}
````

### User / tool · 2026-11-03T01:58:52.190Z

**tool result**
````
1	# T-202 round 3 (final): D-071 allow-list + fillable blank — paralegal review (Maria Delgado, senior PI litigation paralegal)
2	
3	**Verdict: fail.** Round 3 fixes everything I raised in round 2, and the blank reads well in a demand letter. But the allow-list has a hole in the opposite direction, and it is the same class of error as my round 2 blocker: a wrong date printed in the date-of-service slot.
4	
5	The words "visit date" and "seen on" are trusted even when they name a different visit (next, last, previous, initial), and in a visit note such a date overrides the note's own date. Take Appendix A's own ER note, with the follow-up written after the charge: "ER charges: $6,240, next visit date 01/16/2026." The build prints `Central ER discharge summary, January 16, 2026: $6,240.00`. The ER visit was January 9. The pre-T-202 build (bd72d5b) printed January 9 on the same text. letter_check passes the wrong line with 0 violations. In the visit-note probes (R1, R2, R17, R18, R19) it goes further: it reports the correct record-date line as the violation.
6	
7	**What round 3 fixed (re-run on 973b542):**
8	- **Round 2 blocker (B1–B12, N11–N13).** Birth, injury/DOI, accident, onset, referral and order dates now give the blank in a bill. In visit notes they give the note's own date: B8 prints January 16 and B9 February 20 (probe_r3.out:221, :224).
9	- **Round 1 blockers.** These still hold: Posted-first ledgers print the DOS (T2, N1, N2, N24, N25), and the CMS-1500 "X and Y" list gives the blank.
10	- **Round 2 major ("service date not stated" above a quote that states one).** Gone. Every uncertain line now prints `date of service [__________] (statement dated X)`, which claims nothing (D-071 addendum).
11	- **Round 2 minors.**
12	  - "Trans Date" now gives the blank.
13	  - P10 and N17 periods print as ranges.
14	  - The notes now have a CHARGES WITHOUT A CERTAIN DATE OF SERVICE section.
15	  - The not-stated string question is superseded by the addendum.
16	- **Corpus.** Letters for the sample, case_09, lib14 and lib10 are byte-identical to round 2 (UI download and in-process), and right. lib11's counted ledger lines print the blank.
17	
18	**The blank, read as a demand letter.** `Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00` works:
19	- it is as conspicuous as the Bates placeholder;
20	- it states nothing false;
21	- the statement date is labelled as a statement date;
22	- the notes list every blank.
23	
24	I would fill it from the chart notes or a records request before sending. Two wording gaps remain (minor):
25	- The notes say "fill it from the quote" even when the quote has no date.
26	- The "treatment visits 1 through 14" line offers a single-date blank for what needs a range.
27	
28	**Scope.**
29	- **Build:** `git archive 973b542` (tree 4c457a4b…) extracted to the session scratchpad (pr3_973b542/).
30	- **Pre-T-202 comparison:** a bd72d5b archive (pre_bd72d5b/).
31	- **Server:** fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local (health: demo_mode true, local_mode true), http://127.0.0.1:7981.
32	- **Shutdown:** listener PID 24454 killed. `lsof` exit 1, `curl` 000.
33	- **Private values:** 1 <redacted> (a commit author line in `git show` output), not quoted.
34	- **Not graded:** Step 3 wording (separate card).
35	
36	```json
37	{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
38	 "scope": "commit 973b542 (git archive, tree 4c457a4bfb6c, extracted to session scratchpad pr3_973b542/); bd72d5b archive (pre-T-202, T-200) for the before/after on the new blocker. Demo mode: fixture backend FIXTURE_SET=curated, ZLAYT_MODE=local, http://127.0.0.1:7981 (health demo_mode true, local_mode true); listener PID 24454 stopped (lsof exit 1, curl 000). Cases: sample (sample tile), case_09 (POST /api/cases with the golden text, opened in the UI), lib14, lib10, lib11 (library tile); in-process letters for the same five plus three SYNTHETIC variants. Evidence: artifacts/review-evidence/T-202-paralegal-r3/. Step 3 wording not graded (separate card). Private values seen: 1 <redacted>.",
39	 "exercised": [
40	  "Read personas/paralegal.md, my round 2 review, D-071 + amendment + clarification + addendum (memory/ORCHESTRATOR_DECISIONS.md:84-93), board.py show T-202 (notes, handoff), git show 973b542 (service_date.py, export.py, store.py)",
41	  "From the archive: pytest test_t202_r3_allow_list + test_t202_r2_service_date_layouts + test_t202_charge_service_dates + test_t200_undated_charge_label '211 passed in 7.88s' (pytest-t202.out); python -m evals.letter_check value 0 over 25 cases (letter_check.out)",
42	  "Every round 1 and round 2 bill text, loaded verbatim from my r2 probe files (P1-P10, T1-T3, N1-N25, B1-B12), plus 16 new R shapes, through the shipped store.charge_service_date (probe_r3.py -> probe_r3.out, 66 probes)",
43	  "Other-visit labels in visit notes and bills (R1, R2, R17-R23) and letter_check.charge_date_violations on the build's line vs the record-date line (probe_r3b.out); sample-styled punctuation variants C1-C7 (probe_r3c.out)",
44	  "SYNTHETIC sample variant 'ER charges: $6,240, next visit date 01/16/2026.' through the full letter on 973b542 (letters_dump_r3.out) and on bd72d5b (before_t202.out)",
45	  "Playwright on the running archive app (h.py + p01_cases.py): sample, case_09, lib14, lib10, lib11 keyboard-first through Steps 1-4, Step 3 cards logged and screenshotted, letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); sample/case_09/lib14/lib10 letters cmp-identical to round 2",
46	  "In-process letters + notes, all_accepted and counted (letters_dump_r3.py): sample, case_09, lib14, lib10, lib11, synth_ambiguous_dos, synth_cms1500_two_dates, synth_sample_er_next_visit (letters/); diffed against round 2 (letters_vs_r2.out); read as a demand letter"
47	 ],
48	 "verdict": "fail",
49	 "scores": {"verify_quickly": 4, "letter_dates_correct_on_corpus": 5, "blank_in_demand_letter": 4, "adjuster_credibility": 3},
50	 "findings": [
51	  {"severity": "blocker",
52	   "title": "A 'visit date' / 'seen on' label naming another visit (next, last, previous, initial) prints that visit's date as the charge's date of service; in a visit note it overrides the note's own correct date (regression vs pre-T-202), and letter_check enforces the wrong date",
53	   "evidence": "artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.out: SYNTHETIC sample variant (Appendix A record 2, ER note dated 2026-01-09, excerpt ending 'ER charges: $6,240, next visit date 01/16/2026.') prints 'Central ER discharge summary, January 16, 2026: $6,240.00' with 'date violations: []'. Same text on bd72d5b (before_t202.out) prints 'Central ER discharge summary, January 9, 2026: $6,240.00'. probe_r3b.out: R1 'Next visit date 01/30/2026, office visit charge $150.00.' (note 2026-01-16) -> 'Dr. Alvarez, primary care, January 30, 2026'; R2 'Previously seen on 01/09/2026 in the ER, follow-up visit charge $150.00.' -> January 9; R17 'Visit charge: $150.00   Next visit date: 01/30/2026' -> January 30; R18 'Last visit date: 01/09/2026   Visit charge: $150.00' -> January 9; R19 PT discharge 2026-03-06 'Initial visit date 01/23/2026, discharge visit charge $185.00.' -> January 23; R23 bill 'next visit date 02/28/2026' after the figure -> February 28. probe_r3c.out: C4 'ER charges: $6,240, next visit date 01/16/2026.' and C7 'Follow-up visit date: 01/16/2026  ER charges: $6,240' -> January 16; C6 PT eval 01/23 'Next visit date: 01/27/2026   Charge per visit $185' -> January 27. Only a sentence break protects the line (C1, C3, C5 keep the record date). letter_check: for R1, R2, R17, R18, R19 the build's wrong line gives 'violations: []' and the record-date line gives 'charge line's date is not certain from its quote (the quote's labeled date of service reads 2026-01-30)' (probe_r3b.out). Cause: service_date.py:43 _SVC_CORE accepts 'visit date' and 'seen' with no check of the word before them (next/last/previous/initial/return/follow-up), and a labeled date wins before the record-date fallback at service_date.py:375-376; the after-statement check runs only for bills (service_date.py:291), so a visit note accepts a date after its own date (January 30 on a January 16 note). evals/letter_check.py:190 _SERVICE_PHRASES carries the same 'visit date'/'seen' entries. tests/unit/test_t202_r3_allow_list.py has no next/last/previous/initial visit fixture (grep printed nothing).",
54	   "why_it_matters": "The brief and D-071 allow exactly two outputs for a charge line: a certain service date or the blank. 'January 16, 2026: $6,240.00' for an ER visit on January 9 is a wrong date of service on the largest charge in the sample case. The January 16 date belongs to the PCP follow-up, so the adjuster sees the ER bill dated to a different provider's visit. In a case with a disputed accident date (01/09 vs 01/19), any charge-date error is ammunition. It is a regression: the same text printed January 9 before T-202. And the eval now treats the correct date as the violation, so a later fix would be pushed back. Charges inside clinical notes are Appendix A's own pattern ('ER charges: $6,240.', 'Charge per visit $185.'), and checkout lines ('Visit charge ... Next visit date ...') are common in EHR visit summaries.",
55	   "fix": "In a dated encounter record (not a bill), the record's date is the visit. A labeled date there prints only when it equals the record's date; any other labeled date gives the record's date, or the blank with a note naming both. Everywhere (bills too), a visit or seen label preceded by next, last, previous, prior, initial, first, return, follow-up, scheduled or upcoming is not a service label. A date after the record's own date is never a service date in any record (extend the service_date.py:291 check beyond bills). Mirror both rules in letter_check with its own word list.",
56	   "acceptance_test": "Unit fixtures R1, R2, R17, R18, R19, R23 and C4, C6, C7 from probe_r3b.py/probe_r3c.py. Visit notes print the record's date (January 16, 2026; January 9 for C4/C7; January 23 for C6; March 6 for R19) or the blank, never January 30, 27 or 23 or the prior-visit date. R23 gives the blank. letter_check reports a violation on each of the build's current R1/R2/R17/R18/R19 lines and none on the record-date line. A SYNTHETIC golden or library case whose ER or visit note writes the next visit date after the charge with a comma prints the ER date."},
57	  {"severity": "minor",
58	   "title": "The note says 'The line states no date of service' or 'not labeled as a date of service' for lines that do label one in a form the code does not read (DOS with ordinal, UB-04 FL6 six-digit period, CMS-1500 Item 24A)",
59	   "evidence": "probe_r3.out R15 'DOS Feb. 2nd, 2026 office visit charge $275.00.' gives the blank with reason=no_date and 'The line states no date of service.'. N20 'FL6 statement covers period FROM 060926 THROUGH 061226.' gives the same. N8 'Item 24A 06/24/2026 CPT 99204 $185.00.' gives 'The only date near this line (06/24/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting...'. Text at service_date.py:100. The blank is safe in all three; only the note is wrong.",
60	   "why_it_matters": "The note and the notes section are where I learn what to fill in. 'States no date' sends me to request a bill I already hold. Calling Item 24A 'possibly a birth or injury date' is wrong on its face to anyone who reads CMS-1500s, and it erodes trust in every other note.",
61	   "fix": "When a service label (DOS, 24A, FL6 / statement covers period) is present but its date is not parsed, use the written-date note naming the text as written ('The quote labels \"Feb. 2nd, 2026\" as the date of service; the code could not read it'). Add 24A as an inline label, and parse the six-digit FROM/THROUGH form under FL6.",
62	   "acceptance_test": "Fixtures R15, N20 and N8: no note says 'states no date' or 'not labeled'; each note quotes the labeled date as written (or N8 prints June 24 / July 8, N20 'June 9–12, 2026')."},
63	  {"severity": "minor",
64	   "title": "Internal notes tell me to 'fill it from the quote' for lines whose quote has no date, and the one-date blank does not fit a multi-visit line",
65	   "evidence": "ui-lib11-notes.txt:39-41 '- Fennimoor Spine Clinic, $250.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.' The quotes are 'New patient exam charge $250.00', 'x-ray charge $180.00', 'treatment visits 1 through 14 charge $2,310.00' (no date). export.py:614 uses one sentence for every reason. The $2,310.00 line covers visits 1 through 14 (March 27 to May 29 in the chronology), but the letter offers 'date of service [__________]'.",
66	   "why_it_matters": "For a no-date line the only real action is to request a dated ledger, or to match the charge to the chart notes myself. 'From the quote' wastes a look. A 14-visit charge needs a range ('dates of service'), and a singular blank invites a single date that undercounts the treatment span.",
67	   "fix": "Word the notes line by reason. no_date / non_service_date: 'the bill line gives no date; take it from the matching visit note or request a dated itemized bill'. Written-date reasons: 'the quote writes \"04/05/2026\"; confirm and fill'. When the quote counts visits ('visits 1 through 14', 'x 9 visits'), print 'dates of service [__________]'.",
68	   "acceptance_test": "lib11 counted notes contain no 'fill it from the quote' for the three Fennimoor lines; the $2,310.00 letter line reads 'dates of service [__________]'; the synth_ambiguous_dos note keeps 'fill it from the quote' with the date as written."},
69	  {"severity": "minor",
70	   "title": "Carried from rounds 1 and 2: some charge quotes name neither the service nor the date the line prints",
71	   "evidence": "ui-lib14-letter.txt 'Source [Ex. __ / Bates __]: \"charge $187.05.\"'; ui-lib10-letter.txt 'Source [Ex. __ / Bates __]: \"FL47 total charges $4,920.00.\"'. The handoff lists the quote-span minor as not done.",
72	   "why_it_matters": "I cannot check the printed September 14 or June 9–12 against the quote under it without opening the record.",
73	   "fix": "Quote the bill line from its code or description through the figure.",
74	   "acceptance_test": "Every charge Source line in the 25-case letters contains a service word or code as well as the figure."},
75	  {"severity": "nit",
76	   "title": "A CMS-1500 claim-level 'dates of service from X to Y' prints the whole span on each coded line",
77	   "evidence": "probe_r3.out N10 'CMS-1500 dates of service from 06/24/2026 to 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.' prints 'Wardlaw Orthopedics, CMS-1500, June 24–July 8, 2026' on both lines (round 2: the not-stated form).",
78	   "why_it_matters": "It is what the bill states, and so not a wrong date. But a new-patient visit (99204) shown across two weeks reads oddly to an adjuster. On a real CMS-1500 the span sits per line in 24A.",
79	   "fix": "Optional: on a CMS-1500 (not a UB-04 or a unit-count line), a claim-level span over several coded lines gives the blank with a note quoting the span.",
80	   "acceptance_test": "N10 lines print the blank with 'claim dates of service 06/24/2026 to 07/08/2026' in the note; P10 (9 units over the period) keeps 'January 23–March 6, 2026'."}
81	 ],
82	 "whats_right": [
83	  "Round 2 blocker closed: birth, DOI, accident, onset, referral and order dates never print. Bills give the blank, and visit notes keep their own date (B8 January 16, B9 February 20)",
84	  "The blank 'date of service [__________] (statement dated June 15, 2026)' is honest, pastes cleanly, and is listed under CHARGES WITHOUT A CERTAIN DATE OF SERVICE in the notes",
85	  "Corpus letters (sample, case_09, lib14, lib10) unchanged and right, including lib10 'June 9–12, 2026'; Posted-first ledgers and the CMS-1500 'and' list still right"
86	 ],
87	 "questions_for_chris": [
88	  "Still open from round 2, outside T-202: the export gate blocks a SYNTHETIC CMS-1500 coded line ('Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’', letters_dump_r3.out synth_cms1500_two_dates). Should this get its own card?"
89	 ]}
90	```
91	
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:58:53.532Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"D-071\" memory/ORCHESTRATOR_DECISIONS.md | head -30",
 "description": "Locate D-071 decisions"
}
````

### User / tool · 2026-11-03T01:58:53.626Z

**tool result**
````
84:## D-071 — Letter charge lines carry the service date, never a bill's statement date as if it were one
87:## D-071 amendment — when the service date is not certain, print none and ask the human
92:- D-071 clarification (T-202 r2): an ambiguous numeric date is certain when only one reading is on or before the bill's statement date (a service cannot postdate its own statement); lib10 keeps "June 9–12, 2026". Deterministic, kept.
93:- D-071 addendum (T-206 paralegal question, decided without waiting per rule 1): a counted line with no certain service date prints a fillable blank like the Bates placeholder: "date of service [__________] (statement dated June 15, 2026)". The paralegal fills it from the quote; nothing is inferred.
94:- D-071 amendment 2 (§7.4 after T-202 r3; round 4 authorised, final): (a) a record's own date is a service date only for a positively identified encounter record (visit/ER/clinic/therapy/ambulance-run note); bills, receipts, superbills, charge summaries and unknown types never lend their header date; (b) in prose, only "date of service", "dates of service", "DOS" and "service date" are labels ("visit date", "seen on" and bare "date" are not; they also name next or prior visits); (c) letter_check keeps an independent scanner but reads the same declared encounter-type table (one data file), and anchors the blank; (d) if round 4 fails, the fallback is the most conservative rule: every charge line prints the fillable blank unless a DOS column or one of the (b) labels ties exactly one date to it.
95:- D-071 amendment 2 note (T-202 r4): inside bills only, "visit of", "the run of", "rendered on" and "service period" also count as service labels (case_09 and lib14 need them); outside bills they do not. Accepted.
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:58:54.158Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; python3 tools/board.py show T-202 | tail -60",
 "description": "Show T-202 card and handoff"
}
````

### User / tool · 2026-11-03T01:58:54.306Z

**tool result**
````
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
- 2026-11-03T01:34:13Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-202-paralegal-r3.md; round 3; findings:
    - [blocker] A 'visit date' / 'seen on' label naming another visit (next, last, previous, initial) prints that visit's date as the charge's date of service; in a visit note it overrides the note's own correct date (regression vs pre-T-202), and letter_check enforces the wrong date — fix: In a dated encounter record (not a bill), the record's date is the visit. A labeled date there prints only w
    - [minor] The note says 'The line states no date of service' or 'not labeled as a date of service' for lines that do label one in a form the code does not read (DOS with ordinal, UB-04 FL6 six-digit period, CMS-1500 Item 24A) — fix: When a service label (DOS, 24A, FL6 / statement covers period) is present but its date is not parsed, use the written-date note naming the text as written ('The qu
    - [minor] Internal notes tell me to 'fill it from the quote' for lines whose quote has no date, and the one-date blank does not fit a multi-visit line — fix: Word the notes line by reason. no_date / non_service_date: 'the bill line gives no date; take it from the matching visit note or request a dated itemized bill'. Written-date reasons: 'the quote writes "04/05/2026"; confirm and fill'. When
    - [minor] Carried from rounds 1 and 2: some charge quotes name neither the service nor the date the line prints — fix: Quote the bill line from its code or description through the figure.
- 2026-11-03T01:34:13Z orchestrator: assigned: backend
- 2026-11-03T01:34:13Z orchestrator: Paralegal r3 blocker: 'next visit date 01/16/2026' in an ER note dates the ER charge Jan 16 (label 'visit date' matched). Round 4 (§7.4 decision) queued until staff r3 lands.
- 2026-11-03T01:37:28Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-202-staff-engineer-r3.md
- 2026-11-03T01:37:28Z backend: moved changes_requested -> in_progress
- 2026-11-03T01:58:28Z backend: FOR ARCHITECT (docs/LLM_VS_CODE.md rows 2 and 3, T-207), after T-202 r4 commit 8cb5bd2 (D-071 amendment 2). Row 2: replace "by a service label in its clause (DOS, date of service, service date, seen on, visit date)" with "by a service label in its clause (in prose only DOS, date of service, dates of service and service date, never after next/last/prior/previous/initial/follow-up; a bill also reads its own 'visit of' and 'the run of')". Row 3 (append): "A record's own date is a charge line's date of service only for a positively identified encounter record (visit, ER, clinic, therapy, imaging or ambulance-run note), declared in one data file, app/backend/encounter_types.json, which production and evals/letter_check.py both read. A bill, receipt, superbill, charge summary, administrative paper or record of unknown type never lends its header date: it prints the fillable blank unless a label or a DOS column ties one date to the line." Validation cell: "tests/unit/test_t202_r4_encounter.py (every r3 reviewer probe is a fixture; 24 of 25 mutants fail the unit suite, the 25th is equivalent)".
- 2026-11-03T01:58:28Z backend: AC 1 checked: r4 8cb5bd2 (git archive): unit 6266 passed 12 skipped 1 failed (test_e2e_contract test ids, fails identically at parent 8521562, not my files), guided e2e 145 passed, python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r4_encounter.py 131 tests (86 red before); 24 of 25 mutants killed (25th equivalent); 150 corpus letter+notes blobs byte-identical
- 2026-11-03T01:58:31Z backend: moved in_progress -> in_review
- 2026-11-03T01:58:42Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer

## Handoff
What changed (r4, 8cb5bd2, D-071 amendment 2): (a) service_date.record_kind reads the one declared table app/backend/encounter_types.json; only an identified encounter (visit/ER/clinic/therapy/imaging/EMS) lends its header date, bills/receipts/superbills/charge summaries/admin papers/unknown never do (store.charge_service_date too). (b) prose labels are only DOS, date(s) of service, service date, never after next/last/prior/previous/initial/first/return/follow-up/scheduled/upcoming/future; visit date, seen on, bare date dropped. (c) letter_check keeps its own scanner, reads the same JSON with its own matcher, and accepts the blank only whole and exact. T-209 r2 leader: a label then dots/spaces/colon then one date is that label's date (leaders masked, label gap unlimited, window 60), also the DOS ... 99213 ... $250.00 reviewer case.
How verified (git archive 8cb5bd2): unit 6266 passed, 12 skipped, 1 failed (4 shards; the 1 is tests/unit/test_e2e_contract.py::test_every_test_id_is_declared, brand/footer-note/draft-done/demo-badge/btn-draft test ids, fails the same at parent 8521562 and touches none of my files); guided e2e 145 passed; python -m evals.letter_check value 0 over 25 cases. tests/unit/test_t202_r4_encounter.py 131 tests, 86 red before the fix; every r3 paralegal+staff probe (next visit date, R1/R2/R17-19/R23, C4/C6/C7, superbill, patient receipt, charge summary, fee schedule, estimate, cost of care summary, claim, remittance, itemization, Receipt:/Charges:/Account summary:, EOB/payment history/HCFA/balance due blanks, bare date, Entry/Posted/Transaction/Issue date, leaders) is a fixture. Mutants (scratch copy): the 4 staff survivors M6 L3 L7 killed, L6 equivalent now (the whole-blank compare rejects 9/11 underscores itself); 21 new mutants P1-P14 C1-C7 all killed: 24 of 25 killed in total. Corpus: 150 letter+notes blobs (25 cases x all_accepted/counted) byte-identical before and after.
Judgment calls: (1) bills keep 'visit of', 'the run of', 'rendered on', 'service period' (case_09 and lib14 goldens depend on them; in a non-bill they are not labels). If the orchestrator wants only the four, case_09 and lib14 print the blank: one line in _SVC_BILL. (2) The plausibility rule (not after the record, not >5 years before) now applies to every record, not only bills. (3) An excerpt opening with a financial word before its first colon/full stop ('ER charges: ...') makes a bill: safe direction (blank). (4) test_t200 and test_t202_r3 edited (qa-owned): 3 prose-label rows moved to the r4 file, one unknown-source assertion.
What's left: architect T-207 text (note on the card); paralegal minors from r3 (notes wording by reason, 24A/FL6 note, quote span) not done; the CMS-1500 export-gate question is outside T-202. What surprised me: the opening scan flagged my own ER fixture; the Write tool rewrites \u escapes in scripts.
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:58:55.803Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git show 8cb5bd2 -- app/backend/encounter_types.json app/backend/service_date.py app/backend/store.py",
 "description": "Show the fix diff"
}
````

### User / tool · 2026-11-03T01:58:55.897Z

**tool result**
````
commit 8cb5bd2e657408a2654117cb04fa173031c294a9
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 19:50:55 2026 -0600

    fix(backend): T-202 r4 D-071 amendment 2: only an identified encounter record lends its date; four prose labels; dotted leaders; declared record-type table; anchored blank
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/encounter_types.json b/app/backend/encounter_types.json
new file mode 100644
index 0000000..7282305
--- /dev/null
+++ b/app/backend/encounter_types.json
@@ -0,0 +1,21 @@
+{
+  "_doc": "D-071 amendment 2 (T-202 round 4). The ONE declared table of record types for charge-line dates. A record's own date can stand as a charge line's date of service ONLY when the record is a positively identified encounter record (a visit, ER, clinic, therapy, imaging or ambulance-run note). Read by app/backend/service_date.py (production) and by evals/letter_check.py (the independent check, with its own matcher). Matching rule, the same in both: lower-case the text, split it into tokens (runs of letters and digits; hyphens, punctuation and underscores split), and a term matches when its tokens appear in order as consecutive tokens of the text. 'encounter_abbreviations' are matched case-sensitively as single upper-case tokens. A record is a BILL when its source label, or the opening of its excerpt (its first 'opening_chars' characters, cut at the first colon, full stop or line break: 'Receipt:', 'Charges:', 'Account summary:'), matches 'financial' (production also keeps the lexicon billing_document list). It is ADMINISTRATIVE when the same text matches 'administrative'. Otherwise it is an ENCOUNTER only when its source label matches 'encounter' or 'encounter_abbreviations'; every other record is of unknown type. Bills, administrative papers and unknown types never lend their header date.",
+  "opening_chars": 40,
+  "encounter": [
+    "visit", "emergency", "urgent care", "clinic", "therapy", "ambulance", "run report", "trip report", "patient care report",
+    "discharge summary", "discharge note", "progress note", "office note", "clinic note", "consult", "consultation", "consulta", "nota de consulta",
+    "evaluation", "re-evaluation", "reevaluation", "exam", "examination", "new patient", "follow-up", "followup", "primary care", "pain management",
+    "orthopedic", "orthopedics", "surgery", "surgical", "operative note", "operative report", "op note",
+    "imaging", "radiology", "mri", "x-ray", "xray", "ct scan", "ultrasound", "chiropractic", "chiropractor", "physical therapy", "telehealth"
+  ],
+  "encounter_abbreviations": ["ER", "ED", "EMS", "PT", "OT"],
+  "financial": [
+    "bill", "bills", "billed", "billing", "superbill", "statement", "statements", "invoice", "invoices", "ledger", "ledgers", "account", "itemized", "itemised", "itemization",
+    "receipt", "receipts", "charges", "charge summary", "charge sheet", "fee", "fees", "estimate", "estimated", "cost", "claim", "claims", "remittance",
+    "eob", "explanation of benefits", "hcfa", "cms-1500", "cms1500", "ub-04", "ub04", "ub-92", "ub92", "payment", "payments", "balance", "financial", "copay", "deductible", "price", "pricing", "quote"
+  ],
+  "administrative": [
+    "phone", "telephone", "voicemail", "portal message", "message", "correspondence", "letter", "fax", "affidavit", "authorization", "authorisation",
+    "referral", "records request", "request for records", "records retrieval", "no-show", "noshow", "custodian"
+  ]
+}
diff --git a/app/backend/service_date.py b/app/backend/service_date.py
index 3a541e3..19bc2d7 100644
--- a/app/backend/service_date.py
+++ b/app/backend/service_date.py
@@ -1,18 +1,22 @@
-"""The service date a charge line prints, only when positive evidence ties it to the line (D-071 amendment, T-202 round 3: an ALLOW-LIST, not a deny-list). Code only, no LLM
+"""The service date a charge line prints, only when positive evidence ties it to the line (D-071 amendment, T-202 rounds 3 and 4: an ALLOW-LIST, not a deny-list). Code only, no LLM
 (LLM_VS_CODE rows 2 and 3).
 
 The letter's charge line carries a date of service. A date there is a claim to an adjuster, so a date is the line's service date ONLY when one of these ties it to the line:
   (a) the column header over it names service (DOS, date of service, service date, from/to service, 24A, visit date);
-  (b) a service label in the same clause before (or just after) it (DOS, date of service, service date, seen on, visit date, visit of, the run of ...);
+  (b) a service label in the same clause before (or just after) it. In prose ONLY 'DOS', 'date of service', 'dates of service' and 'service date' (D-071 amendment 2; 'visit date', 'seen on'
+      and a bare 'date' name next or prior visits and entry dates, so they are not labels), never after next/last/prior/previous/initial/first/return/follow-up/scheduled/upcoming/future.
+      A BILL also reads the wording a statement uses for what it covers ('visit of', 'the run of', 'rendered on', 'service period' ...). A label may be followed by a dotted leader,
+      spaces or a colon before its date;
   (c) it is the date cell of the charge row itself, in a table whose header is (a);
   (d) for a coded line of a bill with no date of its own: the one period the bill states for its services ('dates of service ...', 'the run of ...', and on a UB-04 'statement
       covers period ...').
 Any other date (birth, injury, onset, referral, order, authorization, entry, transaction, issued, printed, posted, statement, or no label at all) is NOT a service date and is never
-looked at again: an unlabeled date cannot become the line's date by default. The result is one of:
+looked at again: an unlabeled date cannot become the line's date by default. The record's own date is the line's date ONLY for a positively identified encounter record (`record_kind`, the
+table app/backend/encounter_types.json: visit, ER, clinic, therapy, imaging, ambulance-run note); a bill, receipt, superbill, charge summary, administrative paper or record of unknown type
+never lends its header date. The result is one of:
   - `stated`: exactly one unambiguous labeled date or complete period (a numeric date that reads two ways is resolved only by 'a service cannot follow its statement', and only when
-    EVERY labeled end then reads one way; a stated date after its statement, or more than five years before it, in a bill is doubtful);
-  - `not_stated` with reason `no_date` / `non_service_date`: the quote labels no date of service; a dated encounter note (visit note, imaging report: not a bill) keeps the
-    note's own date;
+    EVERY labeled end then reads one way; a stated date after its record's own date, or more than five years before it, is doubtful);
+  - `not_stated` with reason `no_date` / `non_service_date`: the quote labels no date of service (an encounter record keeps its own date instead);
   - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): the quote DOES label a date of service and
     the code cannot read it with certainty; the note names the date as the quote writes it.
   Every not-stated line prints the same fillable blank (D-071 addendum): 'date of service [__________] (statement dated X)'. The paralegal fills it from the quote; nothing is inferred,
@@ -20,10 +24,44 @@ looked at again: an unlabeled date cannot become the line's date by default. The
 Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
 (`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
 import datetime as _dt
+import json
+import pathlib
 import re
 
 from app.backend import amounts as AM
 
+TYPES_PATH = pathlib.Path(__file__).with_name("encounter_types.json")          # D-071 amendment 2: the one declared table of record types (also read by evals/letter_check.py)
+_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))
+
+
+def _tokens(text: str) -> list:
+    return re.findall(r"[^\W_]+", (text or "").lower())
+
+
+def _phrase_rx(terms):
+    return re.compile(r"(?<= )(?:" + "|".join(" ".join(re.escape(t) for t in _tokens(term)) for term in sorted(terms, key=len, reverse=True)) + r")(?= )")
+
+
+_FIN, _ADMIN, _ENC = (_phrase_rx(_TYPES[k]) for k in ("financial", "administrative", "encounter"))
+_ABBR = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(map(re.escape, _TYPES["encounter_abbreviations"])) + r")(?![A-Za-z0-9])")
+_OPEN = int(_TYPES["opening_chars"])
+
+
+def _hit(rx, text) -> bool:
+    return bool(rx.search(" " + " ".join(_tokens(text)) + " "))
+
+
+def record_kind(source, excerpt: str = "") -> str:
+    """'bill' | 'encounter' | 'other' (D-071 amendment 2). A bill is what amounts.billing_document says or what the declared table calls financial in the source label or the first
+    characters of the excerpt, up to its first colon or full stop ('Receipt:', 'Charges:', 'Account summary:'); an administrative paper (phone note, letter, affidavit) is 'other'; an ENCOUNTER needs a positive
+    identification in the source label (visit, ER, clinic, therapy, imaging, ambulance-run note ...). Anything else is of unknown type ('other'). Only an encounter lends its header date."""
+    src, opening = source or "", re.split(r"[:.\n]", (excerpt or "")[:_OPEN])[0]
+    if AM.billing_document(src, excerpt or "") or _hit(_FIN, src) or _hit(_FIN, opening):
+        return "bill"
+    if _hit(_ADMIN, src) or _hit(_ADMIN, opening):
+        return "other"
+    return "encounter" if (_hit(_ENC, src) or _ABBR.search(src)) else "other"
+
 _MON = AM._MON
 _ORD = r"(?:st|nd|rd|th)?"
 _DASH = "–—"
@@ -39,16 +77,32 @@ _TOK = re.compile(
 _JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
 _LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
 # ---- the allow-list: positive evidence that a date is the line's date of service. Nothing else is read (T-202 round 3).
-_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(]{0,4}$"
-_SVC_CORE = (r"\bdos|\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?|\bvisit\s+dates?|\bdates?\s+of\s+visit|\bvisit\s+of|\bseen(?:\s+on)?|"
-             r"\b(?:services?\s+)?(?:rendered|provided|performed)\s+on|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|\bservice\s+period|\bperiod\s+of\s+service|"
-             r"\bdates?\s+of\s+treatment|\btreatment\s+dates?")
+_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(\u00b7]*$"          # a label, then spaces, a colon or a dotted leader (masked to middle dots, `_mask_leaders`), then the date
+_LEADER = re.compile(r"(?:\.[ ]?){3,}|\u2026+")
+_WINDOW = 60                     # characters before a date that may hold its label and the leader after it
+
+
+def _mask_leaders(text: str) -> str:
+    """The same text with every dotted leader ('.......', '. . . .', '\u2026') replaced by as many middle dots, so positions are unchanged: a leader is neither a sentence end nor a column gap, and
+    'Date of service.......01/19/2026 ... 99213 office visit ...... $250.00' reads as one clause (T-209 r2: a label, dots or spaces or a colon, then one date is that label's date)."""
+    return _LEADER.sub(lambda m: "\u00b7" * len(m.group(0)), text or "")
+_NOT_OTHER_VISIT = (r"(?<!next )(?<!last )(?<!prior )(?<!previous )(?<!initial )(?<!first )(?<!return )(?<!scheduled )(?<!upcoming )(?<!future )(?<!follow-up )(?<!followup )"
+                    r"(?<!next\s)(?<!last\s)")
+_SVC_CORE = _NOT_OTHER_VISIT + r"(?:\bdos|\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?)"        # amendment 2 (b): the only labels in prose
+_SVC_BILL = (r"\bvisit\s+of|\b(?:services?\s+)?(?:rendered|provided|performed)\s+on|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|\bservice\s+period|\bperiod\s+of\s+service|"
+             r"\bdates?\s+of\s+treatment|\btreatment\s+dates?")        # a bill's own wording for what it covers (a statement 'for the visit of', an invoice 'for the run of')
 _PER_CORE = (r"\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?|\bservice\s+period|\bperiod\s+of\s+service|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|"
              r"\b(?:services?\s+)?(?:rendered|provided)\s+on")
 _UB_CORE = r"\bstatement\s+(?:covers\s+)?period"          # UB-04 FL6 'Statement Covers Period' is the span of the services; on any other bill 'statement period' is not a service label
 _UB = re.compile(r"\bub-?04\b|\btype\s+of\s+bill\b|\bFL\s?\d{1,2}\b|\bUB\s?92\b", re.IGNORECASE)
-_LBL = {False: re.compile(rf"(?:{_SVC_CORE}){_LBL_END}", re.IGNORECASE), True: re.compile(rf"(?:{_SVC_CORE}|{_UB_CORE}){_LBL_END}", re.IGNORECASE)}
-_PER = {False: re.compile(rf"(?:{_PER_CORE}){_LBL_END}", re.IGNORECASE), True: re.compile(rf"(?:{_PER_CORE}|{_UB_CORE}){_LBL_END}", re.IGNORECASE)}
+
+
+def _lbl_rx(extra, ub):
+    return re.compile(rf"(?:{_SVC_CORE}" + (rf"|{_SVC_BILL}" if extra else "") + (rf"|{_UB_CORE}" if ub else "") + rf"){_LBL_END}", re.IGNORECASE)
+
+
+_LBL = {(b, u): _lbl_rx(b, u) for b in (False, True) for u in (False, True)}          # keyed (bill, ub)
+_PER = {u: re.compile(rf"(?:{_PER_CORE}" + (rf"|{_UB_CORE}" if u else "") + rf"){_LBL_END}", re.IGNORECASE) for u in (False, True)}
 # a column heading that names service (a CMS-1500 24A 'From'/'To' under 'Date(s) of Service', 'Service From', 'DOS' ...). A bare 'Date', 'Entry date', 'Transaction Date', 'Posted' ... does not.
 _H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter\s+date|"
                     r"\b(?:service|svc)\s+(?:from|to|thru|through)\b|\b(?:from|to|thru|through)\s+(?:dos|service|svc)\b|\b24\s*-?a\b", re.IGNORECASE)
@@ -252,14 +306,14 @@ def _column_head(excerpt: str, row_ls: int, row_cells: list, tok_abs: int) -> st
 
 
 def _mark(text: str, units: list, rx, tail: bool = False) -> list:
-    """[bool] per unit: a service label ends the 40 characters before it, or it is listed ('A and B') after a labeled unit. In `tail` (words after the figure) the label must open the
+    """[bool] per unit: a service label ends the 60 characters before it, or it is listed ('A and B') after a labeled unit. In `tail` (words after the figure) the label must open the
     tail: no sentence break and no 'and'/'or' between the figure and the label."""
     marks = []
     for k, u in enumerate(units):
-        ok = bool(rx.search(text[max(0, u.start - 40):u.start]))
+        ok = bool(rx.search(text[max(0, u.start - _WINDOW):u.start]))
         if ok and tail:
             before = text[:u.start]
-            ok = len(before) <= 40 and not re.search(r"[.;]|\b(?:and|or)\b", before, re.IGNORECASE)
+            ok = len(before) <= _WINDOW and not re.search(r"[.;]|\b(?:and|or)\b", before, re.IGNORECASE)
         if not ok and k and marks[k - 1] and _LIST.match(text[units[k - 1].end:u.start]):
             ok = True
         marks.append(ok)
@@ -267,14 +321,14 @@ def _mark(text: str, units: list, rx, tail: bool = False) -> list:
 
 
 def _plausible(first, last, ref) -> bool:
-    """A bill's service date is not after its statement and not years before it."""
+    """A service date is not after the record it appears in and not years before it."""
     if not ref:
         return True
     r = _dt.date.fromisoformat(ref)
     return (last or first) <= ref and _dt.date.fromisoformat(first) >= r - _dt.timedelta(days=366 * _YEARS_BEFORE)
 
 
-def _decide(units, text, ref, bill):
+def _decide(units, text, ref):
     """('ok', first, last) for one certain labeled unit (or several that read the same); ('bad', reason, [raw, ...]) otherwise."""
     reads = [(u, _certain(u, ref)) for u in units]
     raws = [" ".join(u.raw(text).split()) for u in units]
@@ -288,7 +342,7 @@ def _decide(units, text, ref, bill):
         if r[0] != "ok":
             return "bad", r[1], raws
         first, last = r[1], r[2]
-    if bill and not _plausible(first, last, ref):
+    if not _plausible(first, last, ref):          # in every record: a service date is not after the record's own date and not years before it (a prior treatment's DOS is not this charge's)
         return "bad", "implausible", raws
     return "ok", first, last
 
@@ -306,21 +360,24 @@ def resolve(excerpt: str, start: int, source, date_iso) -> dict:
     unlabeled date near the line for non_service_date), raws ([the labeled dates as written])} for the figure at `start` of `excerpt`, in a record with header `source` and date
     `date_iso`. Only labeled dates are candidates (module doc); see it for the rules."""
     out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
+    excerpt = _mask_leaders(excerpt)
     amts = AM.find_amounts(excerpt or "")
     i = next((n for n, a in enumerate(amts) if a["start"] == start), None)
     if i is None:
         return out
     a = amts[i]
     ss, se = next(((s, e) for s, e in AM._segments(excerpt) if s <= a["start"] < e), (0, len(excerpt)))
-    bill = AM.billing_document(source, excerpt)
+    kind = record_kind(source, excerpt)
+    bill = kind == "bill"
     ub = bool(_UB.search(source or "") or _UB.search(excerpt or ""))
+    lbl = _LBL[(bill, ub)]
     sfigs = [j for j, x in enumerate(amts) if ss <= x["start"] < se]
     seg = excerpt[ss:se]
     others = []                       # dates near the line that no service label ties to it
 
     def labeled(text, tail=False):
         us = _units(text)
-        marks = _mark(text, us, _LBL[ub], tail)
+        marks = _mark(text, us, lbl, tail)
         others.extend(u.raw(text) for u, m in zip(us, marks) if not m)
         return [u for u, m in zip(us, marks) if m]
 
@@ -332,30 +389,30 @@ def resolve(excerpt: str, start: int, source, date_iso) -> dict:
         lab = []
         for u in _units(seg):
             head = _column_head(excerpt, row_ls, row_cells, ss + u.start)
-            if (head and _H_SVC.search(head)) or _LBL[ub].search(seg[max(0, u.start - 40):u.start]):
+            if (head and _H_SVC.search(head)) or lbl.search(seg[max(0, u.start - _WINDOW):u.start]):
                 lab.append(u)
             else:
                 others.append(u.raw(seg))
         if lab:
-            return _apply(out, _decide(lab, seg, date_iso, bill))
+            return _apply(out, _decide(lab, seg, date_iso))
     else:                                                                 # (b) a service label in the same clause
         prev = max((amts[j]["end"] for j in sfigs if j < i), default=ss)
         own = excerpt[prev:a["start"]]
         lab = labeled(own)
         if lab:
-            return _apply(out, _decide(lab, own, date_iso, bill))
+            return _apply(out, _decide(lab, own, date_iso))
         if prev > ss:                                                      # a labeled date stands once for the items listed after it: usable only when it is the line's one date
             whole = excerpt[ss:a["start"]]
             lab = labeled(whole)
             if lab:
-                return _apply(out, _decide(lab, whole, date_iso, bill))
+                return _apply(out, _decide(lab, whole, date_iso))
         tail = excerpt[a["end"]:min([amts[j]["start"] for j in sfigs if j > i], default=se)]
         lab = labeled(tail, tail=True)
         if lab:
-            return _apply(out, _decide(lab, tail, date_iso, bill))
+            return _apply(out, _decide(lab, tail, date_iso))
     # no labeled date of its own
-    if bill:
-        if AM._CODE_RX.search(excerpt[ss:a["start"]]):                     # (d) a coded line takes the one period the bill states for its services
+    if kind != "encounter":                                                # a bill, an administrative paper or a record of unknown type never lends its header date
+        if bill and AM._CODE_RX.search(excerpt[ss:a["start"]]):                     # (d) a coded line takes the one period the bill states for its services
             prefix = excerpt[:se]
             us = _units(prefix)
             seen, uniq = set(), []
@@ -368,10 +425,10 @@ def resolve(excerpt: str, start: int, source, date_iso) -> dict:
                     seen.add(key)
                     uniq.append(u)
             if uniq:
-                return _apply(out, _decide(uniq, prefix, date_iso, bill))
+                return _apply(out, _decide(uniq, prefix, date_iso))
         if others:
             out.update(reason="non_service_date", raw=others[0])
         return out
-    if date_iso:                                                          # a dated encounter record (visit note, imaging report): the record's date is the visit
+    if date_iso:                                                          # a positively identified encounter record (visit, ER, clinic, therapy, imaging, ambulance-run note): its date is the visit
         out.update(state="stated", first=date_iso, last=None, reason=None, raw="", raws=[])
     return out
diff --git a/app/backend/store.py b/app/backend/store.py
index 861cec9..92b6c96 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -121,17 +121,17 @@ def charge_service_date(item: dict, rec, pos) -> dict:
     when no service date is certain), statement_date_iso (the record's date, which for a bill is the statement's), reason (None when stated; one of service_date.REASONS), confirm_note (None when stated)}.
     A date is stated only when positive evidence ties it to the line (service_date.resolve, an allow-list): a service label in its clause, a column heading that names service, or
     the one period its bill states; an unlabeled date (birth, injury, referral, entry, transaction ...) is never the service date. The record's date of a ledger, invoice or UB-04 is the statement's, never a fallback: a bill line the code cannot read has no
-    service date. A dated encounter record's (visit note, imaging report) date is the visit. A charge the paralegal counted for a missing date of service (D-064) is
+    service date. A positively identified encounter record's (visit, ER, clinic, therapy, imaging or ambulance-run note: service_date.record_kind, app/backend/encounter_types.json) own date is the visit; a bill, receipt, superbill, charge summary, administrative paper or record of unknown type never lends its date (D-071 amendment 2). A charge the paralegal counted for a missing date of service (D-064) is
     not stated, with no note (she counted it knowing). Code only."""
     from app.backend import amounts as AM, service_date as SD          # lazy: keep the import graph as it was
     rd = (rec or {}).get("date_iso")
-    bill = AM.billing_document((rec or {}).get("source"), item.get("excerpt") or "")
+    encounter = SD.record_kind((rec or {}).get("source"), item.get("excerpt") or "") == "encounter"
     counted_undated = ((item.get("ladder") or {}).get("counted") or {}).get("not_counted_reason") == AM.NO_DATE_WHY
     none = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
     if counted_undated:
         r = dict(none)
     elif rec is None or pos is None or not item.get("excerpt"):
-        r = dict(none) if bill else ({"state": "stated", "first": rd, "last": None, "reason": None, "raw": "", "raws": []} if rd else dict(none))
+        r = {"state": "stated", "first": rd, "last": None, "reason": None, "raw": "", "raws": []} if (encounter and rd) else dict(none)          # only a positively identified encounter record lends its own date (D-071 amendment 2)
     else:
         r = SD.resolve(item["excerpt"], pos, rec.get("source"), rd)
     stated = r["state"] == "stated"
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:59:11.751Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls artifacts/review-evidence/T-202-paralegal-r3/ artifacts/review-evidence/T-202-paralegal-r2/ artifacts/review-evidence/T-202-paralegal/ | head -80; ls artifacts/review-evidence | grep -i 209 | head",
 "description": "List prior evidence scripts"
}
````

### User / tool · 2026-11-03T01:59:11.875Z

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

artifacts/review-evidence/T-202-paralegal-r3/:
before_t202.out
before_t202.py
case_09-s3-00-a1.png
case_09-step2-done.png
case_09-step3-done.png
case_09-step4.png
db
draft-T-202-paralegal-r3.md
h.py
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:59:13.900Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls artifacts/review-evidence/T-202-paralegal-r3/ | grep -v png; ls artifacts/review-evidence/T-202-paralegal/ | grep -v png | head -40; ls artifacts/review-evidence/ | grep -i -E \"209|serve\" ",
 "description": "List non-image evidence files"
}
````

### User / tool · 2026-11-03T01:59:14.012Z

**tool result**
````
before_t202.out
before_t202.py
db
draft-T-202-paralegal-r3.md
h.py
letter_check.out
letters
letters_dump_r3.out
letters_dump_r3.py
letters_vs_r2.out
p01.out
p01_cases.py
probe_r3.out
probe_r3.py
probe_r3b.out
probe_r3b.py
probe_r3c.out
probe_r3c.py
profile
pytest-t202.out
run.log
server.log
ui-case_09-letter-onscreen.txt
ui-case_09-letter.txt
ui-case_09-notes.txt
ui-lib10-letter-onscreen.txt
ui-lib10-letter.txt
ui-lib10-notes.txt
ui-lib11-letter-onscreen.txt
ui-lib11-letter.txt
ui-lib11-notes.txt
ui-lib14-letter-onscreen.txt
ui-lib14-letter.txt
ui-lib14-notes.txt
ui-sample-letter-onscreen.txt
ui-sample-letter.txt
ui-sample-notes.txt
all_charge_lines.out
all_charge_lines.py
api-amount-fields.out
case09-paste-probe.out
case_09-all_accepted-letter.txt
case_09-all_accepted-notes.txt
case_09-counted-letter.txt
case_09-counted-notes.txt
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
lib14-all_accepted-letter.txt
lib14-all_accepted-notes.txt
lib14-counted-letter.txt
lib14-counted-notes.txt
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
T-049-served-index.html
T-060-paralegal-pass4-serve.py
T-120-r2-paralegal-server.log
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:59:15.571Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r3; cat probe_r3.py; echo ======; cat probe_r3b.py; echo =====; cat probe_r3c.py",
 "description": "Read r3 probe scripts"
}
````

### User / tool · 2026-11-03T01:59:15.664Z

**tool result**
````
"""T-202 r3 paralegal probe: every SYNTHETIC bill text from rounds 1 and 2 (probe_r2.py P1-P10, T1-T3, N1-N25; probe_r2b.py B1-B12), loaded verbatim
from those files with ast, plus new round 3 shapes (R*), through the shipped path store.charge_service_date (the same call Step 3 and the letter use).
Prints the letter head exactly as export.charge_when builds it on 973b542: f"{src}, {text}: {raw}".
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/probe_r3.py <archive_root> <repo_root>
"""
import ast
import os
import sys

root = os.path.abspath(sys.argv[1])
repo = os.path.abspath(sys.argv[2])
sys.path.insert(0, root)
os.chdir(root)
from app.backend import amounts as AM, store  # noqa: E402


def load(path):
    tree = ast.parse(open(path).read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "PROBES":
            return ast.literal_eval(node.value)
    raise SystemExit(f"no PROBES in {path}")


ev = os.path.join(repo, "artifacts/review-evidence/T-202-paralegal-r2")
PROBES = load(os.path.join(ev, "probe_r2.py")) + load(os.path.join(ev, "probe_r2b.py"))

V = "Dr. Alvarez, primary care"
H = "Hobbleton Family Clinic, billing statement"
L = "Larkspur Hollow Physical Therapy, itemized ledger"
W = "Wardlaw Orthopedics, CMS-1500"
PROBES += [
    # round 3: shapes aimed at the allow-list itself (labels that tie a date that is still not this line's service)
    ("R1 visit note: next visit date in the charge sentence", V, "2026-01-16",
     "Next visit date 01/30/2026, office visit charge $150.00."),
    ("R2 visit note: prior visit 'seen on' in the charge sentence", V, "2026-01-16",
     "Previously seen on 01/09/2026 in the ER, follow-up visit charge $150.00."),
    ("R3 bill: return visit date label after the charge's own DOS", H, "2026-03-01",
     "Date of service 02/02/2026, office visit charge $275.00, return visit date 02/16/2026."),
    ("R4 bill: DOS label tied to the accident ('date of service of the accident')", H, "2026-03-01",
     "Date of injury 01/09/2026; date of service 02/02/2026; 99213 office visit $275.00."),
    ("R5 ledger: header 'Visit Type  Date  Charge' (heading names visit, but the date column is bare 'Date')", L, "2026-07-01",
     "Visit Type     Date         Code   Charge\n"
     "Follow-up     06/10/2026   97140  $70.00\n"
     "Follow-up     06/17/2026   97110  $95.00"),
    ("R6 ledger: DOS heading, but a DOB column before it", L, "2026-07-01",
     "DOB          DOS          Code   Charge\n"
     "03/15/1980   06/10/2026   97140  $70.00"),
    ("R7 ledger: 'Injury Date' column then 'Service Date' column", L, "2026-07-01",
     "Injury Date   Service Date   Code   Charge\n"
     "01/09/2026    06/10/2026     97140  $70.00"),
    ("R8 ledger: only 'Injury Date' column", L, "2026-07-01",
     "Injury Date   Code   Charge\n"
     "01/09/2026    97140  $70.00"),
    ("R9 CMS-1500 flattened with item 24A label and DOB on the same line", W, "2026-07-14",
     "Item 3 DOB 03/15/1980 Item 24A DOS 06/24/2026 CPT 99204 $185.00."),
    ("R10 bill: 'DOS' then accident date in same clause", H, "2026-03-01",
     "DOS 02/02/2026 (accident 01/09/2026) office visit $275.00."),
    ("R11 bill: 'run of' with an order date", "Tarnwick Fire-Rescue, ambulance invoice", "2026-11-12",
     "Call received 09/14/2026; run of 09/14/2026; A0427 ALS emergency transport, charge $1,380.00."),
    ("R12 visit note: 'Date of service' label is the original ER visit (history)", V, "2026-01-16",
     "Patient brings ER bill, date of service 01/09/2026, ER charge $6,240.00."),
    ("R13 bill: 'Seen on' with referral date first", H, "2026-03-01",
     "Referred 01/20/2026, seen on 02/02/2026, office visit charge $275.00."),
    ("R14 bill: date of service written in words-with-year", H, "2026-03-01",
     "Date of service February 2, 2026: office visit charge $275.00."),
    ("R15 bill: DOS with ordinal ('Feb. 2nd, 2026')", H, "2026-03-01",
     "DOS Feb. 2nd, 2026 office visit charge $275.00."),
    ("R16 bill: DOS 02/02/2026 and statement date 03/01/2026 in one clause", H, "2026-03-01",
     "Statement 03/01/2026 for DOS 02/02/2026, office visit $275.00."),
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
        print(f"   {a['raw']:>10} -> letter head: '{src}, {d['text']}: {a['raw']}'  state={d['state']} reason={d['reason']}")
        if d["confirm_note"]:
            print(f"              Step 3 note: {d['confirm_note']}")
======
"""T-202 r3 paralegal probe B: allow-listed labels ('visit date', 'seen on', 'date of service') that name a DIFFERENT visit than the record's own, in visit notes
(not bills) and in bills; then evals/letter_check.charge_date_violations on what the build prints for them, next to the record-date control. SYNTHETIC text only.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/probe_r3b.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
from app.backend import amounts as AM, store  # noqa: E402
from evals import letter_check as LC  # noqa: E402

V = "Dr. Alvarez, primary care"
PT = "Capital PT, discharge summary"
ER = "Central ER discharge summary"
H = "Hobbleton Family Clinic, billing statement"
PROBES = [
    ("R1 visit note 01/16: next visit date in the charge sentence", V, "2026-01-16", "Next visit date 01/30/2026, office visit charge $150.00."),
    ("R2 visit note 01/16: prior ER visit 'seen on' in the charge sentence", V, "2026-01-16", "Previously seen on 01/09/2026 in the ER, follow-up visit charge $150.00."),
    ("R17 visit note 01/16: checkout line, charge then next visit date", V, "2026-01-16", "Visit charge: $150.00   Next visit date: 01/30/2026"),
    ("R18 visit note 01/16: checkout line, last visit date then charge", V, "2026-01-16", "Last visit date: 01/09/2026   Visit charge: $150.00"),
    ("R19 PT discharge 03/06: initial visit date in the charge sentence", PT, "2026-03-06", "Initial visit date 01/23/2026, discharge visit charge $185.00."),
    ("R20 ER note 01/09: seen on the same day (control, should be January 9)", ER, "2026-01-09", "Seen on 01/09/2026 by EMS, ER facility charge $6,240.00."),
    ("R21 PT discharge 03/06: 'treatment dates' period then a charge", PT, "2026-03-06", "Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00."),
    ("R22 bill 03/01: last visit date label then an undated coded line", H, "2026-03-01", "Last visit date 02/16/2026; 99213 office visit $275.00."),
    ("R23 bill 03/01: next visit date (future) in a coded line", H, "2026-03-01", "99213 office visit $275.00, next visit date 02/28/2026."),
]

print("#### resolver (store.charge_service_date, the path Step 3 and the letter share)")
heads = {}
for label, src, rd, ex in PROBES:
    print(f"== {label}  (record date {rd}; source '{src}'; billing_document={AM.billing_document(src, ex)})")
    print("   " + ex)
    rec = {"id": "r1", "n": 1, "source": src, "date_iso": rd, "excerpt": ex, "text": ex}
    for a in AM.find_amounts(ex):
        if a.get("cents") is None:
            continue
        item = {"excerpt": ex, "value_cents": a["cents"], "raw": a["raw"], "excerpt_start": 0}
        d = store.charge_service_date(item, rec, a["start"])
        head = f"{src}, {d['text']}"
        heads[label.split()[0]] = (src, rd, ex, head, a["raw"])
        print(f"   {a['raw']:>10} -> letter head: '{head}: {a['raw']}'  state={d['state']} reason={d['reason']}")
        if d["confirm_note"]:
            print(f"              Step 3 note: {d['confirm_note']}")


def letter(head, fig, quote):
    return f"BILLED CHARGES\n\n{head}: {fig}\nSource [Ex. __ / Bates __]: \"{quote}\"\n\nBilled charges accepted from these records: {fig}"


print("\n#### letter_check.charge_date_violations: the build's line vs the record-date line")
for key in ("R1", "R2", "R17", "R18", "R19", "R20"):
    src, rd, ex, head, fig = heads[key]
    q = ex.rstrip(".")
    recs = [{"n": 1, "source": src, "date_iso": rd, "excerpt": ex}]
    from app.backend.service_date import display
    ctrl = f"{src}, {display(rd)}"
    print(f"== {key} build prints '{head}': violations {LC.charge_date_violations(letter(head, fig, q), recs)}")
    print(f"   {key} record date   '{ctrl}': violations {LC.charge_date_violations(letter(ctrl, fig, q), recs)}")
=====
"""T-202 r3 paralegal probe C: sample-case-styled clinical notes (Appendix A shapes: 'ER charges: $6,240.', 'Charge per visit $185.') with a follow-up / next /
prior visit date nearby, to see which punctuation keeps the other visit's date out of the charge line. SYNTHETIC text only.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/probe_r3c.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
from app.backend import amounts as AM, store  # noqa: E402

ER = "Central ER discharge summary"
PT = "Capital PT, initial evaluation"
PROBES = [
    ("C1 ER 01/09: follow-up visit date, own sentence, then charge", ER, "2026-01-09", "Follow-up visit date 01/16/2026. ER charges: $6,240."),
    ("C2 ER 01/09: follow-up visit date, semicolon, then charge", ER, "2026-01-09", "Follow-up visit date 01/16/2026; ER charges: $6,240."),
    ("C3 ER 01/09: charge, then next visit date in its own sentence", ER, "2026-01-09", "ER charges: $6,240. Next visit date 01/16/2026."),
    ("C4 ER 01/09: charge, then next visit date after a comma", ER, "2026-01-09", "ER charges: $6,240, next visit date 01/16/2026."),
    ("C5 PT eval 01/23: plan + next visit date + rate, sentences", PT, "2026-01-23", "Plan of care: 12 visits. Next visit date 01/27/2026. Charge per visit $185."),
    ("C6 PT eval 01/23: plan + next visit date + rate, one line no periods", PT, "2026-01-23", "Plan of care: 12 visits   Next visit date: 01/27/2026   Charge per visit $185"),
    ("C7 ER 01/09: two spaces as separators, follow-up visit date then charge", ER, "2026-01-09", "Follow-up visit date: 01/16/2026  ER charges: $6,240"),
]
for label, src, rd, ex in PROBES:
    print(f"== {label}  (record date {rd}; source '{src}'; billing_document={AM.billing_document(src, ex)})")
    print("   " + ex)
    rec = {"id": "r1", "n": 1, "source": src, "date_iso": rd, "excerpt": ex, "text": ex}
    for a in AM.find_amounts(ex):
        if a.get("cents") is None:
            continue
        item = {"excerpt": ex, "value_cents": a["cents"], "raw": a["raw"], "excerpt_start": 0}
        d = store.charge_service_date(item, rec, a["start"])
        print(f"   {a['raw']:>10} -> letter head: '{src}, {d['text']}: {a['raw']}'  state={d['state']} reason={d['reason']}")
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:59:22.782Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $SP/pr4_8cb5bd2 $SP/pre_bd72d5b && git archive 8cb5bd2 | tar -x -C $SP/pr4_8cb5bd2 && git archive bd72d5b | tar -x -C $SP/pre_bd72d5b && ls $SP/pr4_8cb5bd2 && git rev-parse 8cb5bd2^{tree}; git rev-parse --short HEAD",
 "description": "Extract archives of fix and pre-T-202 commits"
}
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:59:23.516Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat evals/golden/sample.txt",
 "description": "Read the sample case text"
}
````

### User / tool · 2026-11-03T01:59:26.801Z

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
bd2be5e81e5e5a981107f2dfcb6ff87a47696807
8cb5bd2
````

### User / tool · 2026-11-03T01:59:26.913Z

**tool result**
````
SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data

=== Record 1 ===
Date: 2026-01-09
Source: Austin EMS run report
Excerpt: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."

=== Record 2 ===
Date: 2026-01-09
Source: Central ER discharge summary
Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."

=== Record 3 ===
Date: 2026-01-16
Source: Dr. Alvarez, primary care
Excerpt: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved."

=== Record 4 ===
Date: 2026-01-23
Source: Capital PT, initial evaluation
Excerpt: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185."

=== Record 5 ===
Date: 2026-02-20
Source: Capital PT, visit 8
Excerpt: "Pain 4/10, improving. Patient reports missing 3 days of work."

=== Record 6 ===
Date: 2026-03-06
Source: Capital PT, visit 9
Excerpt: "Discharged from PT after two missed appointments. Pain 3/10."

=== Record 7 ===
Date: 2026-05-18
Source: Hill Country Pain Management, new patient
Excerpt: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19."

=== Record 8 ===
Date: 2026-05-29
Source: Austin Imaging, cervical MRI
Excerpt: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150."

=== Record 9 ===
Date: 2026-06-12
Source: Hill Country Pain Management, follow-up
Excerpt: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:59:53.291Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2; grep -n \"def billing_document\" -A30 app/backend/amounts.py; grep -n \"def _segments\" -A15 app/backend/amounts.py",
 "description": "Read billing_document and segments"
}
````

### User / tool · 2026-11-03T01:59:53.423Z

**tool result**
````
429:def billing_document(source, excerpt: str = "") -> bool:
430-    """A provider bill or ledger: the source label names one (lexicon billing_document, or a statement / bill / invoice / ledger / account word), or the
431-    excerpt opens as one ("Itemized statement: ...")."""
432-    return bool(_is_billing_source(source or "") or _BILLISH.search(source or "") or _BILL_OPEN.search(excerpt or ""))
433-
434-
435-def _record_period(before: str, ref_iso):
436-    """(first date, last date or None) of the date or period the record states for its services. D-071: the last date is the end of the range ('06/09/2026 to 06/12/2026'),
437-    None for a single date ('the run of 09/14/2026')."""
438-    ms = list(_DOS_RX.finditer(before))
439-    for k, m in enumerate(ms):
440-        iso = _dos_iso(m, ref_iso)
441-        if iso and _PERIOD_PHRASE.search(before[max(0, m.start() - 40):m.start()]):
442-            end = None
443-            if k + 1 < len(ms) and _RANGE_JOIN.match(before[m.end():ms[k + 1].start()]):
444-                end = _dos_iso(ms[k + 1], ref_iso)
445-            return iso, (end if end and end > iso else None)
446-    return None, None
447-
448-
449-def _record_period_dos(before: str, ref_iso):
450-    """A coded line (CPT, HCPCS, revenue code) with no date of its own takes the date or period the record states for its services ('statement period
451-    06/09/2026 to 06/12/2026', 'the run of 09/14/2026'): the first date of that period."""
452-    return _record_period(before, ref_iso)[0]
453-
454-
455-def _tokens(text: str, strip) -> tuple:
456-    """(word stems, codes) of a service description: dates, figures and charge words removed, words cut to four letters ('therapeutic' and 'ther' meet)."""
457-    for s, e in sorted(strip, reverse=True):
458-        text = text[:s] + " " + text[e:]
459-    codes = frozenset(norm_code(m.group(0)) for m in _CODE_RX.finditer(text))
416:def _segments(excerpt: str) -> list:
417-    out, pos = [], 0
418-    for m in _BOUNDARY.finditer(excerpt):
419-        out.append((pos, m.start()))
420-        pos = m.end()
421-    out.append((pos, len(excerpt)))
422-    return [(s, e) for s, e in out if e > s]
423-
424-
425-def _cells(line: str) -> list:
426-    return [m.group(0) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]
427-
428-
429-def billing_document(source, excerpt: str = "") -> bool:
430-    """A provider bill or ledger: the source label names one (lexicon billing_document, or a statement / bill / invoice / ledger / account word), or the
431-    excerpt opens as one ("Itemized statement: ...")."""
````

### Assistant · claude-opus-5-5 · 2026-11-03T01:59:56.925Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2; grep -n \"_BILLISH =\\|_BILL_OPEN =\\|_BOUNDARY =\\|def _is_billing_source\" -A4 app/backend/amounts.py; grep -n \"billing_document\" -A25 app/llm/lexicon.yaml | head -40",
 "description": "Read bill regexes and lexicon list"
}
````

### User / tool · 2026-11-03T01:59:57.057Z

**tool result**
````
12:_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
13-# Rate = unit-rate phrasing only. 'Charge per invoice 4471: $400' is NOT a rate (per + a non-unit noun stays a charge or unclear).
14-_UNIT = r"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment|mile)s?"
15-# Spanish unit nouns (T-110 r2): "por sesión", "por visita", "cada ...". Accents are optional because pasted records often lose them.
16-_UNIT_ES = r"(?:sesi[o\u00f3]n|sesiones|visitas?|horas?|d[i\u00ed]as?|unidad(?:es)?|citas?|tratamientos?|procedimientos?)"
--
309:_BILLISH = re.compile(r"\b(?:statements?|bills?|billing|invoices?|ledgers?|account|itemi[sz]ed|ub-?04|hcfa|cms-?1500|claim\s+form)\b", re.IGNORECASE)
310:_BILL_OPEN = re.compile(r"^\W{0,3}(?:patient\s+)?(?:itemi[sz]ed|statement|invoice|ledger|billing|account\s+statement)\b", re.IGNORECASE)
311-_TOKEN_FILLER = frozenset("charge charges charged billed fee fees of on for the a an at to and unit units dos date service services statement rev cpt code invoiced total".split())
312-_NO_DATE_WHY = "The line states no date of service, so it is not an itemized service line and is not totaled."
313-NO_DATE_WHY = _NO_DATE_WHY           # T-200: the stored reason of a charge the paralegal counted because its line states no date of service
314-_NO_SVC_WHY = "The line names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized service line and is not totaled."
--
766:def _is_billing_source(source: str) -> bool:
767-    return any(e["id"] == "billing_document" and e["regex"].search(source or "") for e in lexicon.code_list("non_encounter"))
768-
769-
770-def damages_mentions(excerpt: str) -> list:
1322:      - id: billing_document
1323-        pattern: '\b(?:billing\s+statement|itemi[sz]ed\s+(?:bill|statement|charges)|statement\s+of\s+account|account\s+statement|ledger|invoice|explanation\s+of\s+benefits|EOB|UB-?04|HCFA|CMS-?1500|payment\s+(?:history|record)|balance\s+due\s+notice)\b'
1324-      - id: phone_or_message
1325-        pattern: '\b(?:phone|telephone|tel\.?)\s+(?:note|call|encounter|message|contact)\b|\bportal\s+message\b|\bvoicemail\b|\bmessage\s+(?:note|log)\b'
1326-      - id: records_admin
1327-        pattern: '\b(?:records?\s+request|request\s+for\s+records|medical\s+records\s+(?:request|certification|affidavit)|business\s+records\s+affidavit|custodian\s+(?:of\s+records\s+)?affidavit|18\.001\s+affidavit|authorization\s+form|HIPAA\s+authorization|correspondence|cover\s+letter|fax\s+cover|referral\s+(?:form|letter)|prior\s+authori[sz]ation|no-?\s?show\s+(?:notice|letter))\b'
1328-    examples:
1329-      hit: ['Hobbleton Family Clinic, billing statement', 'Gloamwood Chiropractic, billing statement', 'Dr. Orla Pennywhistle, phone note', 'Hobbleton Family Clinic, phone note', 'Austin Imaging, itemized bill', 'Capital PT, records request']
1330-      miss: ['Capital PT, visit 9', 'Central ER discharge summary', 'Austin EMS run report', 'Hill Country Pain Management, follow-up', 'Austin Imaging, cervical MRI', 'Dr. Lysander Quibble, telehealth visit']
1331-
1332-  accident_date_phrases:
1333-    applies_to: record_text
1334-    consumer: 'ADR-014: code extracts stated accident dates where a phrase is followed within 40 characters by a date in a listed format. A conflict arises if a stated date is later than the earliest record date, or if two different stated dates exist. Dates are never merged (D-017).'
1335-    rationale: 'The accident-date conflict (Appendix C: 2026-01-09 per EMS/ER vs "Date of accident per intake form: 2026-01-19") is the case''s headline conflict, and it must be producible without an LLM.'
1336-    source: 'ADR-014; D-017; Appendix C record 7; AA A7 (JLG Trucking)'
1337-    false_positive: '"DOA" also means "dead on arrival" and "DOI" can mean "digital object identifier". Neither is followed by a date within 40 characters, so the code rule ignores them. "Collision on I-35" is followed by a road, not a date, and is ignored for the same reason. "Injured on the job" has no date.'
1338-    entries:
1339-      - id: accident_date_label
1340-        pattern: '\b(?:date\s+of\s+(?:the\s+)?(?:accident|injury|incident|loss|collision|crash|MVA|MVC)|(?:accident|injury|incident|loss|collision|crash|MVA|MVC)\s+date|DOA|DOI|DOL|D/A|D\.O\.A\.?|D\.O\.I\.?)\b'
1341-      - id: event_on_date
1342-        pattern: '\b(?:collision|accident|crash|wreck|MVA|MVC|incident|rear-?ended|injured|hurt)\s+(?:on|dated)\b'
1343-    examples:
1344-      hit: ['Date of accident per intake form: 2026-01-19.', 'DOA: 01/09/2026', 'Date of injury 1/9/26', 'MVA on 01/09/2026', 'Collision on January 9, 2026.', 'Accident date: 2026-01-09', 'DOI 2026-01-09']
1345-      miss: ['Seen today for neck pain.', 'Transported to Central ER.']
1346-
1347-  injection:
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:00:22.929Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence; cat T-060-paralegal-pass4-serve.py; echo ====; cat T-202-paralegal-r3/h.py; echo ====; cat T-202-paralegal-r3/p01_cases.py; echo; cat T-202-paralegal-r3/run.log | head -20",
 "description": "Read server launcher and UI helper scripts"
}
````

### User / tool · 2026-11-03T02:00:23.065Z

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

BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7981")  # T-202 r3: 973b542 archive, port 7981
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
"""T-202 r2 paralegal (copied from r1): 986fc55 archive, demo/fixture backend, local mode, port 7976.
For each case (env CASES, default sample,case_09,lib14,lib10): open it as a user (sample tile / paste / library), draft, Step 2 accept with the
keyboard (compare box ticked where asked), Step 3 accept every bill item and tick 'count' boxes where offered, Step 4 download letter + notes.
Run: .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/h.py artifacts/review-evidence/T-202-paralegal/p01_cases.py
"""
import os
import re

CASES = os.environ.get("CASES", "sample,case_09,lib14,lib10,lib11").split(",")  # r3: 973b542 archive, port 7981, lib11 added
PASTE = {"case_09": "/Users/arsis/zlayt-pm-project/evals/golden/case_09_nonvisit_hides_gap.txt"}
LIB = {"lib14": "case_lib14_handwritten_chiro_scans", "lib10": "case_lib10_eob_ub04_cms1500", "lib11": "case_lib11_priors_and_ledger"}


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

### run p01_cases.py at 19:30:14
[sample] draft took 2.2 s
[sample] s2 item=e1 yes_disabled=False compare=False radios=0 :: Prepared answer / January 9, 2026 · Austin EMS run report /  / Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER. /  / How it was checked / The highlighted words are in the record word for word, every number in th
[sample] s2 item=f_accident_date_after_treatment_1_2_7 yes_disabled=False compare=False radios=0 :: Warning for the attorney /  / The records disagree about the accident date /  / Stated accident date is later than recorded treatment /  / Stated accident date January 19, 2026 (“Date of accident per intake form: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Austin EMS ru
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:00:28.097Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2; grep -rn \"demo_mode\" app/config.py app/main.py app/backend/*.py | head -8; lsof -iTCP:7984 -sTCP:LISTEN -nP; echo exit=$?",
 "description": "Check demo mode config and port"
}
````

### User / tool · 2026-11-03T02:00:28.267Z

**tool result**
````
app/backend/api.py:127:    def demo_mode():
app/backend/api.py:266:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "local_mode": local_mode(), "answers": ans,
app/backend/api.py:308:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
app/backend/api.py:309:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:352:        if demo_mode() and digest(text) not in allowed_hashes():
app/backend/api.py:353:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:361:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
app/backend/api.py:377:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
exit=1
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:00:30.970Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2; sed -n 120,135p app/backend/api.py",
 "description": "Read demo_mode definition"
}
````

### User / tool · 2026-11-03T02:00:31.123Z

**tool result**
````
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available

    def demo_mode():
        return not live_enabled()

    def answers():
        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set)."""
        if live_enabled():
            return "live"
        from app.llm.backends import fixture
        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:00:31.834Z

Now I'll set up the r4 evidence directory and start the server.

### Assistant · claude-opus-5-5 · 2026-11-03T02:00:33.967Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; mkdir -p artifacts/review-evidence/T-202-paralegal-r4/db artifacts/review-evidence/T-202-paralegal-r4/letters && cp artifacts/review-evidence/T-202-paralegal-r3/h.py artifacts/review-evidence/T-202-paralegal-r3/p01_cases.py artifacts/review-evidence/T-202-paralegal-r3/letters_dump_r3.py artifacts/review-evidence/T-202-paralegal-r3/before_t202.py artifacts/review-evidence/T-202-paralegal-r4/ && ls artifacts/review-evidence/T-202-paralegal-r4/",
 "description": "Create r4 evidence dir and copy helpers"
}
````

### User / tool · 2026-11-03T02:00:34.106Z

**tool result**
````
before_t202.py
db
h.py
letters
letters_dump_r3.py
p01_cases.py
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:00:38.724Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/db/r4.db PORT=7984 HOST=127.0.0.1 .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2 > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/server.log 2>&1",
 "description": "Start archive app server on port 7984",
 "run_in_background": true
}
````

### User / tool · 2026-11-03T02:00:38.810Z

**tool result**
````
Command running in background with ID: b5vok3phe. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b5vok3phe.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:00:39.414Z

Meanwhile, the deterministic checks from the archive.

### Assistant · claude-opus-5-5 · 2026-11-03T02:00:45.281Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2; PYTHONDONTWRITEBYTECODE=1 LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_t202_r4_encounter.py tests/unit/test_t202_r3_allow_list.py tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/pytest-t202.out 2>&1; tail -3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/pytest-t202.out; PYTHONDONTWRITEBYTECODE=1 LLM_BACKEND=fixture /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.letter_check > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/letter_check.out 2>&1; tail -5 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/letter_check.out",
 "description": "Run T-202 unit tests and letter_check eval from archive",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T02:01:11.623Z

**tool result**
````
........................................................................ [ 84%]
.....................................................                    [100%]
341 passed in 12.85s
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:01:15.755Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -rn \"\\.\\.\\.\\.\\.\\.\\.\" artifacts/review-evidence/T-209-paralegal-*.py | head; grep -n \"dotted\\|leader\" .claude/agent-memory/paralegal-reviewer/t209-*.md reviews/T-209-paralegal*.md | head",
 "description": "Find dotted-leader probe text"
}
````

### User / tool · 2026-11-03T02:01:15.891Z

**tool result**
````
.claude/agent-memory/paralegal-reviewer/t209-confirm-sentence-patterns.md:3:description: T-209 (88c73dd) Step 3 confirm sentence review: static fill instruction vs no-date lines, dotted-leader resolver miss, unreachable in curated set, card clip; r2 file written because reviews are append-only
.claude/agent-memory/paralegal-reviewer/t209-confirm-sentence-patterns.md:11:- Backend resolver misses a labeled DOS when a dotted leader ("99213 ... $250.00") sits between label and amount: reason no_date, so the note says "The line states no date of service." Pre-existing at HEAD (service_date.py), outside the diff. Major.
reviews/T-209-paralegal-r3.md:3:Scope: fix commit 8521562 (`app/frontend/guided/step3.js:32-43`, `app/frontend/guided/step3.css:22`, `tests/e2e/guided/test_t206.py`). HEAD is 8521562, and `git diff --stat 88c73dd 8521562 -- app/backend app/llm` is empty, so the backend note wording is the same as in round 2. I served a fresh `git archive 8521562` in demo mode (fixture backend, `/api/health` returned `"demo_mode":true`) on 127.0.0.1:7931, listener PID 43905. I stopped it afterward: `lsof` exit 1, `curl` 000. Synthetic data only. As the brief asked, I did not grade the round-2 major 2 (dotted leader, T-202).
reviews/T-209-paralegal-r3.md:19: "scope": "fix commit 8521562 (app/frontend/guided/step3.js:32-43, step3.css:22, tests/e2e/guided/test_t206.py); HEAD 8521562; backend unchanged since 88c73dd (git diff --stat 88c73dd 8521562 -- app/backend app/llm: empty); app served from a fresh git archive of 8521562 in demo mode (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local, health demo_mode true) at http://127.0.0.1:7931, listener PID 43905, stopped (lsof exit 1, curl 000); case_lib10_eob_ub04_cms1500 a2 with the backend's own service_date dict injected per reason. Round-2 major 2 (dotted leader, T-202) not graded per brief.",
reviews/T-209-paralegal-r2.md:15:2. major (pre-existing at HEAD, outside the 88c73dd diff): a labeled DOS followed by a dotted leader ("99213 ... $250.00") resolves to "The line states no date of service."
reviews/T-209-paralegal-r2.md:52:   "title": "A labeled date of service followed by a dotted leader is read as no date, so the note says the line states no date of service (pre-existing at HEAD, outside the 88c73dd diff)",
reviews/T-209-paralegal-r2.md:53:   "evidence": "SD.resolve at 88c73dd, source 'Fennimoor Spine Clinic, itemized ledger', date 2026-06-15: 'Fennimoor Spine Clinic itemized ledger. DOS 04/05/2026 Office visit 99213 $250.00' -> ambiguous_numeric, raw '04/05/2026'. The same line with '99213 ... $250.00' -> no_date, raw ''. The note then reads 'The line states no date of service.' Also 'Date of service 04/05/2026 Office visit 99213 $250.00' -> ambiguous_numeric. Outputs printed from the scratch resolver run; the leader variant is my constructed line, not a fixture record (the curated set has no leader lines). Screen-level: the card would show that note above a quote that contains 'DOS 04/05/2026'.",
reviews/T-209-paralegal-r2.md:54:   "why_it_matters": "service_date.py:19 promises the letter never says 'service date not stated' above a quote that states one. The note here says the same thing in a different form. The paralegal would believe the record has no date of service and could request a bill she does not need. The letter output is not wrong (the blank prints), so this is a misleading explanation, not a wrong date in the letter. Itemized ledgers with dot leaders are common, so this is not a rare edge.",
reviews/T-209-paralegal-r2.md:55:   "fix": "In service_date.resolve, allow a dotted leader (runs of '.' or '…' with spaces) between the label and the amount when building the clause, or stop splitting segments at '...'. Route to the T-202 owner (service_date.py), not the T-209 frontend card. Add the leader case to the resolver tests.",
reviews/T-209-paralegal-r2.md:56:   "acceptance_test": "Unit: resolve('Fennimoor Spine Clinic itemized ledger. DOS 04/05/2026 Office visit 99213 ... $250.00', pos of $250.00, 'Fennimoor Spine Clinic, itemized ledger', '2026-06-15') returns reason ambiguous_numeric with raw '04/05/2026'. Same string without the leader returns the same result."},
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:01:57.492Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4; cat letters_dump_r3.py; echo =====; cat before_t202.py",
 "description": "Read letter dump scripts"
}
````

### User / tool · 2026-11-03T02:01:57.591Z

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
SAMPLE = open("evals/golden/sample.txt").read()
# r3: the sample ER note with the follow-up appointment written after the charge, comma-joined (SYNTHETIC variant of Appendix A record 2)
NEXTV = SAMPLE.replace("Follow up with PCP in 1 week. ER charges: $6,240.", "Follow up with PCP in 1 week. ER charges: $6,240, next visit date 01/16/2026.")
assert NEXTV != SAMPLE

CASES = {
    "sample": open("evals/golden/sample.txt").read(),
    "case_09": C09,
    "lib14": open("evals/library/case_lib14_handwritten_chiro_scans.txt").read(),
    "lib10": open("evals/library/case_lib10_eob_ub04_cms1500.txt").read(),
    "lib11": open("evals/library/case_lib11_priors_and_ledger.txt").read(),
    "synth_ambiguous_dos": AMBIG,
    "synth_cms1500_two_dates": CMS,
    "synth_sample_er_next_visit": NEXTV,
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
=====
"""T-202 r3 paralegal: the SYNTHETIC sample variant (ER note 'ER charges: $6,240, next visit date 01/16/2026.') on the pre-T-202 build (bd72d5b, T-200),
to show what the charge line printed before T-202. Prints only the BILLED CHARGES section of the all_accepted letter.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r3/before_t202.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
os.environ.setdefault("LLM_BACKEND", "fixture")
os.environ.setdefault("FIXTURE_SET", "curated")
from evals import letter_check as LC  # noqa: E402

SAMPLE = open("evals/golden/sample.txt").read()
NEXTV = SAMPLE.replace("Follow up with PCP in 1 week. ER charges: $6,240.", "Follow up with PCP in 1 week. ER charges: $6,240, next visit date 01/16/2026.")
assert NEXTV != SAMPLE
got = LC.letters_for(NEXTV)
txt = got["all_accepted"]["letters"]["standard"]
print(txt[txt.index("BILLED CHARGES"):])
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:02:04.787Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; grep -n \"def charge_service_date\" pre_bd72d5b/app/backend/store.py pr4_8cb5bd2/app/backend/store.py; grep -n \"def charge_date_violations\\|def letters_for\\|def charge_lines\" pr4_8cb5bd2/evals/letter_check.py; mkdir -p pr3_973b542 && cd /Users/arsis/zlayt-pm-project && git archive 973b542 | tar -x -C /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542 && echo ok; curl -s http://127.0.0.1:7984/api/health | head -c 300",
 "description": "Check function availability and server health"
}
````

### User / tool · 2026-11-03T02:02:06.951Z

**tool result**
````
pr4_8cb5bd2/app/backend/store.py:118:def charge_service_date(item: dict, rec, pos) -> dict:
pr4_8cb5bd2/app/backend/store.py:146:def charge_service_dates(item: dict, rec, pos) -> tuple:
212:def charge_lines(letter: str) -> list:
413:def charge_date_violations(letter: str, records) -> list:
497:def letters_for(text: str, backend: str = "fixture") -> dict:
ok
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":tr
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:02:41.271Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/probe_r4.py",
 "content": "\"\"\"T-202 r4 paralegal probe: every SYNTHETIC charge text from rounds 1-3 (r2 probe_r2.py P/T/N, probe_r2b.py B; r3 probe_r3.py R1-R16, probe_r3b.py R1/R2/R17-R23,\nprobe_r3c.py C1-C7), loaded from those files by ast (string constants + PROBES lists), plus round 4 shapes (dotted leaders, other-visit DOS labels the\nqualifier list does not name, provider-name sources on bills, totals in encounter notes), through the shipped path store.charge_service_date\n(the call Step 3 and the letter share). Prints the letter head as export builds it: f\"{src}, {text}: {raw}\".\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/probe_r4.py <archive_root> <repo_root>\n\"\"\"\nimport ast\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nrepo = os.path.abspath(sys.argv[2])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, store  # noqa: E402\n\ntry:\n    from app.backend import service_date as SD  # noqa: E402\n    KIND = getattr(SD, \"record_kind\", None)\nexcept Exception:\n    KIND = None\n\n\ndef load(path):\n    tree = ast.parse(open(path).read())\n    ns, out = {}, []\n    for node in tree.body:\n        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):\n            for t in node.targets:\n                if isinstance(t, ast.Name):\n                    ns[t.id] = node.value.value\n        tgt = node.targets[0] if isinstance(node, ast.Assign) else (node.target if isinstance(node, ast.AugAssign) else None)\n        if getattr(tgt, \"id\", \"\") == \"PROBES\" and isinstance(node.value, ast.List):\n            out += eval(compile(ast.Expression(node.value), path, \"eval\"), {}, ns)\n    if not out:\n        raise SystemExit(f\"no PROBES in {path}\")\n    return out\n\n\nev = os.path.join(repo, \"artifacts/review-evidence\")\nOLD = []\nfor f in (\"T-202-paralegal-r2/probe_r2.py\", \"T-202-paralegal-r2/probe_r2b.py\", \"T-202-paralegal-r3/probe_r3.py\",\n          \"T-202-paralegal-r3/probe_r3b.py\", \"T-202-paralegal-r3/probe_r3c.py\"):\n    got = load(os.path.join(ev, f))\n    print(f\"# loaded {len(got)} probes from {f}\")\n    OLD += [(f.split(\"/\")[1].replace(\".py\", \"\") + \" \" + p[0],) + tuple(p[1:]) for p in got]\n\nV = \"Dr. Alvarez, primary care\"\nER = \"Central ER discharge summary\"\nPTD = \"Capital PT, visit 9\"\nERB = \"Central ER, itemized bill\"\nL = \"Fennimoor Spine Clinic, itemized ledger\"\nNEW = [\n    # dotted leaders (T-209 r2 major; brief)\n    (\"D1 ER bill: 'Date of service.......01/09/2026' then leadered charge\", ERB, \"2026-02-05\",\n     \"Date of service.......01/09/2026   ER facility charge ........ $6,240.00\"),\n    (\"D2 ER note: 'Date of service.......01/09/2026' (brief text) then ER charges\", ER, \"2026-01-09\",\n     \"Date of service.......01/09/2026. Dx: cervical strain. ER charges: $6,240.\"),\n    (\"D3 ER note: leader DOS then charge in same clause\", ER, \"2026-01-09\",\n     \"Date of service.......01/09/2026   ER charges ...... $6,240\"),\n    (\"D4 ledger (T-209): DOS 04/05/2026 Office visit 99213 ... $250.00\", L, \"2026-06-15\",\n     \"Fennimoor Spine Clinic itemized ledger. DOS 04/05/2026 Office visit 99213 ... $250.00\"),\n    (\"D5 bill: DOI leader then DOS leader then charge leader\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Date of injury.......01/09/2026   Date of service.......02/02/2026   99213 office visit ...... $275.00\"),\n    (\"D6 bill: spaced-dot leader\", ERB, \"2026-02-05\",\n     \"Date of service . . . . . 01/09/2026   ER facility charge . . . . . $6,240.00\"),\n    (\"D7 bill: unicode ellipsis leader\", ERB, \"2026-02-05\",\n     \"Date of service……01/09/2026   ER facility charge……$6,240.00\"),\n    (\"D8 bill: statement date leader only, then leadered charge (expect blank)\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Statement date.......03/01/2026   Office visit 99213.......$275.00\"),\n    (\"D9 bill: statement date leader + DOS leader + charge\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Statement date.......03/01/2026   Date of service.......02/02/2026   Office visit 99213.......$275.00\"),\n    (\"D10 bill: next-visit leader after charge (expect blank or none)\", ERB, \"2026-02-05\",\n     \"ER facility charge.......$6,240.00   Next date of service.......01/30/2026\"),\n    (\"D11 ER note: 'Next visit date.......01/16/2026' then ER charges (expect Jan 9)\", ER, \"2026-01-09\",\n     \"Next visit date.......01/16/2026   ER charges ...... $6,240\"),\n    (\"D12 PCP note: 'Last date of service.......01/09/2026' then office charge (expect Jan 16)\", V, \"2026-01-16\",\n     \"Last date of service.......01/09/2026   Office visit charge ...... $150.00\"),\n    # other-visit DOS labels whose qualifier is not in the lookbehind list (prior visit, so before the note: plausible)\n    (\"O1 PCP 01/16: 'Reviewed ER records, DOS 01/09/2026, office visit charge'\", V, \"2026-01-16\",\n     \"Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.\"),\n    (\"O2 PCP 01/16: 'Last seen DOS 01/09/2026' (seen, not last, before DOS)\", V, \"2026-01-16\",\n     \"Last seen DOS 01/09/2026, office visit charge $150.00.\"),\n    (\"O3 PCP 01/16: 'ER visit date of service 01/09/2026'\", V, \"2026-01-16\",\n     \"Follow-up of ER visit date of service 01/09/2026, office visit charge $150.00.\"),\n    (\"O4 PT visit 9 03/06: 'Previous visit's date of service 02/20/2026'\", PTD, \"2026-03-06\",\n     \"Previous visit's date of service 02/20/2026, discharge visit charge $185.00.\"),\n    (\"O5 PT visit 9 03/06: 'Initial eval DOS 01/23/2026'\", PTD, \"2026-03-06\",\n     \"Initial eval DOS 01/23/2026, discharge visit charge $185.00.\"),\n    (\"O6 PCP 01/16: 'Prior  DOS 01/09/2026' (two spaces)\", V, \"2026-01-16\",\n     \"Prior  DOS 01/09/2026, office visit charge $150.00.\"),\n    (\"O7 PCP 01/16: 'Follow up DOS' (no hyphen) prior date\", V, \"2026-01-16\",\n     \"Seen for follow up from ER DOS 01/09/2026, office visit charge $150.00.\"),\n    (\"O8 PCP 01/16: ER DOS in its own sentence (control: sentence break)\", V, \"2026-01-16\",\n     \"Reviewed ER records, DOS 01/09/2026. Office visit charge $150.00.\"),\n    (\"O9 PCP 01/16: 'Previous DOS: 01/09/2026' (listed qualifier, control)\", V, \"2026-01-16\",\n     \"Previous DOS: 01/09/2026, office visit charge $150.00.\"),\n    (\"O10 PCP 01/16: checkout line 'ER DOS: 01/09/2026   Visit charge: $150.00'\", V, \"2026-01-16\",\n     \"ER DOS: 01/09/2026   Visit charge: $150.00\"),\n    # bills whose source label is only a provider name (contains clinic / imaging / therapy / ER) and whose opening has no financial word\n    (\"S1 'Hobbleton Family Clinic' 03/01: Amount due ... office visit on 02/02/2026\", \"Hobbleton Family Clinic\", \"2026-03-01\",\n     \"Amount due $275.00 for office visit on 02/02/2026.\"),\n    (\"S2 'Austin Imaging' 06/20: Patient responsibility ... MRI performed 05/29/2026\", \"Austin Imaging\", \"2026-06-20\",\n     \"Patient responsibility $2,150.00 for cervical MRI performed 05/29/2026.\"),\n    (\"S3 'Capital Physical Therapy' 03/20: Total due for 9 visits\", \"Capital Physical Therapy\", \"2026-03-20\",\n     \"Total due $1,665.00 for 9 visits.\"),\n    (\"S4 'Central ER' 02/05: Amount owed (emergency visit 01/09/2026)\", \"Central ER\", \"2026-02-05\",\n     \"Amount owed: $6,240.00 (emergency visit 01/09/2026).\"),\n    (\"S5 'Hill Country Pain Management' 07/01: thank-you then balance\", \"Hill Country Pain Management\", \"2026-07-01\",\n     \"Thank you for your visit. Your balance is $450.00.\"),\n    (\"S6 'Gloamwood Chiropractic' 04/30: Please remit for treatment 03/02/2026-04/10/2026\", \"Gloamwood Chiropractic\", \"2026-04-30\",\n     \"Please remit $1,200.00 for treatment 03/02/2026 to 04/10/2026.\"),\n    (\"S7 'Austin Imaging, cervical MRI' 06/20 (encounter label) but the excerpt is the bill\", \"Austin Imaging, cervical MRI\", \"2026-06-20\",\n     \"Amount due $2,150.00. Thank you for choosing Austin Imaging.\"),\n    (\"S8 'Hobbleton Family Clinic' 03/01 control: opening with 'Statement' (expect blank)\", \"Hobbleton Family Clinic\", \"2026-03-01\",\n     \"Statement: amount due $275.00 for office visit on 02/02/2026.\"),\n    # totals for several visits inside an encounter note\n    (\"T1 PT visit 9 03/06: total for visits 1-9 in the discharge note\", PTD, \"2026-03-06\",\n     \"Discharged from PT after two missed appointments. Total for visits 1-9: $1,665.00.\"),\n    (\"T2 PT visit 9 03/06: PT charges to date\", PTD, \"2026-03-06\",\n     \"Discharged from PT after two missed appointments. PT charges to date $1,665.00.\"),\n    (\"T3 ER note 01/10 (summary written next day): arrived 01/09/2026\", \"Central ER discharge summary\", \"2026-01-10\",\n     \"Arrived 01/09/2026 by EMS. Discharged 01/10/2026. ER charges: $6,240.\"),\n]\n\nfor label, src, rd, ex in OLD + NEW:\n    kind = KIND(src, ex) if KIND else \"n/a\"\n    print(f\"== {label}  (record date {rd}; source '{src}'; kind={kind}; billing_document={AM.billing_document(src, ex)})\")\n    print(\"   \" + ex.replace(\"\\n\", \"\\n   \"))\n    rec = {\"id\": \"r1\", \"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex, \"text\": ex}\n    for a in AM.find_amounts(ex):\n        if a.get(\"cents\") is None:\n            continue\n        item = {\"excerpt\": ex, \"value_cents\": a[\"cents\"], \"raw\": a[\"raw\"], \"excerpt_start\": 0}\n        d = store.charge_service_date(item, rec, a[\"start\"])\n        print(f\"   {a['raw']:>10} -> letter head: '{src}, {d['text']}: {a['raw']}'  state={d['state']} reason={d['reason']}\")\n        if d.get(\"confirm_note\"):\n            print(f\"              Step 3 note: {d['confirm_note']}\")\nprint(f\"# total probes: {len(OLD)} old + {len(NEW)} new\")\n"
}
````

### User / tool · 2026-11-03T02:02:41.385Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/probe_r4.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:02:50.532Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; LLM_BACKEND=fixture .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/probe_r4.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2 /Users/arsis/zlayt-pm-project > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/probe_r4.out 2>&1; LLM_BACKEND=fixture .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/probe_r4.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr3_973b542 /Users/arsis/zlayt-pm-project > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/probe_r4_on_973b542.out 2>&1; head -6 artifacts/review-evidence/T-202-paralegal-r4/probe_r4.out; tail -2 artifacts/review-evidence/T-202-paralegal-r4/probe_r4.out; wc -l artifacts/review-evidence/T-202-paralegal-r4/probe_r4*.out",
 "description": "Run probe on r4 and r3 archives"
}
````

### User / tool · 2026-11-03T02:02:51.135Z

**tool result**
````
# loaded 38 probes from T-202-paralegal-r2/probe_r2.py
# loaded 12 probes from T-202-paralegal-r2/probe_r2b.py
# loaded 16 probes from T-202-paralegal-r3/probe_r3.py
# loaded 9 probes from T-202-paralegal-r3/probe_r3b.py
# loaded 7 probes from T-202-paralegal-r3/probe_r3c.py
== probe_r2 P1 two-row ledger, own dates  (record date 2026-03-15; source 'Hobbleton Family Clinic, itemized ledger'; kind=bill; billing_document=True)
       $6,240 -> letter head: 'Central ER discharge summary, January 10, 2026: $6,240'  state=stated reason=None
# total probes: 82 old + 33 new
     456 artifacts/review-evidence/T-202-paralegal-r4/probe_r4.out
     457 artifacts/review-evidence/T-202-paralegal-r4/probe_r4_on_973b542.out
     913 total
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:02:51.847Z

Let me read the new-shape results first.

### Assistant · claude-opus-5-5 · 2026-11-03T02:02:52.938Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4; grep -n \"== D1 \" probe_r4.out; awk '/^== D1 /,0' probe_r4.out",
 "description": "Show results for new r4 probes"
}
````

### User / tool · 2026-11-03T02:02:53.036Z

**tool result**
````
353:== D1 ER bill: 'Date of service.......01/09/2026' then leadered charge  (record date 2026-02-05; source 'Central ER, itemized bill'; kind=bill; billing_document=True)
== D1 ER bill: 'Date of service.......01/09/2026' then leadered charge  (record date 2026-02-05; source 'Central ER, itemized bill'; kind=bill; billing_document=True)
   Date of service.......01/09/2026   ER facility charge ........ $6,240.00
    $6,240.00 -> letter head: 'Central ER, itemized bill, January 9, 2026: $6,240.00'  state=stated reason=None
== D2 ER note: 'Date of service.......01/09/2026' (brief text) then ER charges  (record date 2026-01-09; source 'Central ER discharge summary'; kind=encounter; billing_document=False)
   Date of service.......01/09/2026. Dx: cervical strain. ER charges: $6,240.
       $6,240 -> letter head: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
== D3 ER note: leader DOS then charge in same clause  (record date 2026-01-09; source 'Central ER discharge summary'; kind=encounter; billing_document=False)
   Date of service.......01/09/2026   ER charges ...... $6,240
       $6,240 -> letter head: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
== D4 ledger (T-209): DOS 04/05/2026 Office visit 99213 ... $250.00  (record date 2026-06-15; source 'Fennimoor Spine Clinic, itemized ledger'; kind=bill; billing_document=True)
   Fennimoor Spine Clinic itemized ledger. DOS 04/05/2026 Office visit 99213 ... $250.00
      $250.00 -> letter head: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00'  state=not_stated reason=ambiguous_numeric
              Step 3 note: The quote labels 04/05/2026 as the date of service, and it can be read as month/day or day/month; the record does not settle which. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.
== D5 bill: DOI leader then DOS leader then charge leader  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; kind=bill; billing_document=True)
   Date of injury.......01/09/2026   Date of service.......02/02/2026   99213 office visit ...... $275.00
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
== D6 bill: spaced-dot leader  (record date 2026-02-05; source 'Central ER, itemized bill'; kind=bill; billing_document=True)
   Date of service . . . . . 01/09/2026   ER facility charge . . . . . $6,240.00
    $6,240.00 -> letter head: 'Central ER, itemized bill, January 9, 2026: $6,240.00'  state=stated reason=None
== D7 bill: unicode ellipsis leader  (record date 2026-02-05; source 'Central ER, itemized bill'; kind=bill; billing_document=True)
   Date of service……01/09/2026   ER facility charge……$6,240.00
    $6,240.00 -> letter head: 'Central ER, itemized bill, January 9, 2026: $6,240.00'  state=stated reason=None
== D8 bill: statement date leader only, then leadered charge (expect blank)  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; kind=bill; billing_document=True)
   Statement date.......03/01/2026   Office visit 99213.......$275.00
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
              Step 3 note: The only date near this line (03/01/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
== D9 bill: statement date leader + DOS leader + charge  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; kind=bill; billing_document=True)
   Statement date.......03/01/2026   Date of service.......02/02/2026   Office visit 99213.......$275.00
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
== D10 bill: next-visit leader after charge (expect blank or none)  (record date 2026-02-05; source 'Central ER, itemized bill'; kind=bill; billing_document=True)
   ER facility charge.......$6,240.00   Next date of service.......01/30/2026
    $6,240.00 -> letter head: 'Central ER, itemized bill, date of service [__________] (statement dated February 5, 2026): $6,240.00'  state=not_stated reason=non_service_date
              Step 3 note: The only date near this line (01/30/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
== D11 ER note: 'Next visit date.......01/16/2026' then ER charges (expect Jan 9)  (record date 2026-01-09; source 'Central ER discharge summary'; kind=encounter; billing_document=False)
   Next visit date.......01/16/2026   ER charges ...... $6,240
       $6,240 -> letter head: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
== D12 PCP note: 'Last date of service.......01/09/2026' then office charge (expect Jan 16)  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; kind=encounter; billing_document=False)
   Last date of service.......01/09/2026   Office visit charge ...... $150.00
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== O1 PCP 01/16: 'Reviewed ER records, DOS 01/09/2026, office visit charge'  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; kind=encounter; billing_document=False)
   Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O2 PCP 01/16: 'Last seen DOS 01/09/2026' (seen, not last, before DOS)  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; kind=encounter; billing_document=False)
   Last seen DOS 01/09/2026, office visit charge $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O3 PCP 01/16: 'ER visit date of service 01/09/2026'  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; kind=encounter; billing_document=False)
   Follow-up of ER visit date of service 01/09/2026, office visit charge $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O4 PT visit 9 03/06: 'Previous visit's date of service 02/20/2026'  (record date 2026-03-06; source 'Capital PT, visit 9'; kind=encounter; billing_document=False)
   Previous visit's date of service 02/20/2026, discharge visit charge $185.00.
      $185.00 -> letter head: 'Capital PT, visit 9, February 20, 2026: $185.00'  state=stated reason=None
== O5 PT visit 9 03/06: 'Initial eval DOS 01/23/2026'  (record date 2026-03-06; source 'Capital PT, visit 9'; kind=encounter; billing_document=False)
   Initial eval DOS 01/23/2026, discharge visit charge $185.00.
      $185.00 -> letter head: 'Capital PT, visit 9, January 23, 2026: $185.00'  state=stated reason=None
== O6 PCP 01/16: 'Prior  DOS 01/09/2026' (two spaces)  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; kind=encounter; billing_document=False)
   Prior  DOS 01/09/2026, office visit charge $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O7 PCP 01/16: 'Follow up DOS' (no hyphen) prior date  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; kind=encounter; billing_document=False)
   Seen for follow up from ER DOS 01/09/2026, office visit charge $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O8 PCP 01/16: ER DOS in its own sentence (control: sentence break)  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; kind=encounter; billing_document=False)
   Reviewed ER records, DOS 01/09/2026. Office visit charge $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== O9 PCP 01/16: 'Previous DOS: 01/09/2026' (listed qualifier, control)  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; kind=encounter; billing_document=False)
   Previous DOS: 01/09/2026, office visit charge $150.00.
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== O10 PCP 01/16: checkout line 'ER DOS: 01/09/2026   Visit charge: $150.00'  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; kind=encounter; billing_document=False)
   ER DOS: 01/09/2026   Visit charge: $150.00
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== S1 'Hobbleton Family Clinic' 03/01: Amount due ... office visit on 02/02/2026  (record date 2026-03-01; source 'Hobbleton Family Clinic'; kind=encounter; billing_document=False)
   Amount due $275.00 for office visit on 02/02/2026.
      $275.00 -> letter head: 'Hobbleton Family Clinic, March 1, 2026: $275.00'  state=stated reason=None
== S2 'Austin Imaging' 06/20: Patient responsibility ... MRI performed 05/29/2026  (record date 2026-06-20; source 'Austin Imaging'; kind=encounter; billing_document=False)
   Patient responsibility $2,150.00 for cervical MRI performed 05/29/2026.
    $2,150.00 -> letter head: 'Austin Imaging, June 20, 2026: $2,150.00'  state=stated reason=None
== S3 'Capital Physical Therapy' 03/20: Total due for 9 visits  (record date 2026-03-20; source 'Capital Physical Therapy'; kind=encounter; billing_document=False)
   Total due $1,665.00 for 9 visits.
    $1,665.00 -> letter head: 'Capital Physical Therapy, March 20, 2026: $1,665.00'  state=stated reason=None
== S4 'Central ER' 02/05: Amount owed (emergency visit 01/09/2026)  (record date 2026-02-05; source 'Central ER'; kind=encounter; billing_document=False)
   Amount owed: $6,240.00 (emergency visit 01/09/2026).
    $6,240.00 -> letter head: 'Central ER, February 5, 2026: $6,240.00'  state=stated reason=None
== S5 'Hill Country Pain Management' 07/01: thank-you then balance  (record date 2026-07-01; source 'Hill Country Pain Management'; kind=encounter; billing_document=False)
   Thank you for your visit. Your balance is $450.00.
      $450.00 -> letter head: 'Hill Country Pain Management, July 1, 2026: $450.00'  state=stated reason=None
== S6 'Gloamwood Chiropractic' 04/30: Please remit for treatment 03/02/2026-04/10/2026  (record date 2026-04-30; source 'Gloamwood Chiropractic'; kind=encounter; billing_document=False)
   Please remit $1,200.00 for treatment 03/02/2026 to 04/10/2026.
    $1,200.00 -> letter head: 'Gloamwood Chiropractic, April 30, 2026: $1,200.00'  state=stated reason=None
== S7 'Austin Imaging, cervical MRI' 06/20 (encounter label) but the excerpt is the bill  (record date 2026-06-20; source 'Austin Imaging, cervical MRI'; kind=encounter; billing_document=False)
   Amount due $2,150.00. Thank you for choosing Austin Imaging.
    $2,150.00 -> letter head: 'Austin Imaging, cervical MRI, June 20, 2026: $2,150.00'  state=stated reason=None
== S8 'Hobbleton Family Clinic' 03/01 control: opening with 'Statement' (expect blank)  (record date 2026-03-01; source 'Hobbleton Family Clinic'; kind=bill; billing_document=True)
   Statement: amount due $275.00 for office visit on 02/02/2026.
      $275.00 -> letter head: 'Hobbleton Family Clinic, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
              Step 3 note: The only date near this line (02/02/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
== T1 PT visit 9 03/06: total for visits 1-9 in the discharge note  (record date 2026-03-06; source 'Capital PT, visit 9'; kind=encounter; billing_document=False)
   Discharged from PT after two missed appointments. Total for visits 1-9: $1,665.00.
    $1,665.00 -> letter head: 'Capital PT, visit 9, March 6, 2026: $1,665.00'  state=stated reason=None
== T2 PT visit 9 03/06: PT charges to date  (record date 2026-03-06; source 'Capital PT, visit 9'; kind=encounter; billing_document=False)
   Discharged from PT after two missed appointments. PT charges to date $1,665.00.
    $1,665.00 -> letter head: 'Capital PT, visit 9, March 6, 2026: $1,665.00'  state=stated reason=None
== T3 ER note 01/10 (summary written next day): arrived 01/09/2026  (record date 2026-01-10; source 'Central ER discharge summary'; kind=encounter; billing_document=False)
   Arrived 01/09/2026 by EMS. Discharged 01/10/2026. ER charges: $6,240.
       $6,240 -> letter head: 'Central ER discharge summary, January 10, 2026: $6,240'  state=stated reason=None
# total probes: 82 old + 33 new
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:03:01.057Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4; awk '/^== D1 /,0' probe_r4_on_973b542.out | grep -E \"^== |letter head\" | sed -E 's/\\(record date.*//' ",
 "description": "Show r3 build results for the new probes"
}
````

### User / tool · 2026-11-03T02:03:01.159Z

**tool result**
````
== D1 ER bill: 'Date of service.......01/09/2026' then leadered charge  
    $6,240.00 -> letter head: 'Central ER, itemized bill, date of service [__________] (statement dated February 5, 2026): $6,240.00'  state=not_stated reason=no_date
== D2 ER note: 'Date of service.......01/09/2026' (brief text) then ER charges  
       $6,240 -> letter head: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
== D3 ER note: leader DOS then charge in same clause  
       $6,240 -> letter head: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
== D4 ledger (T-209): DOS 04/05/2026 Office visit 99213 ... $250.00  
      $250.00 -> letter head: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00'  state=not_stated reason=no_date
== D5 bill: DOI leader then DOS leader then charge leader  
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=no_date
== D6 bill: spaced-dot leader  
    $6,240.00 -> letter head: 'Central ER, itemized bill, date of service [__________] (statement dated February 5, 2026): $6,240.00'  state=not_stated reason=no_date
== D7 bill: unicode ellipsis leader  
    $6,240.00 -> letter head: 'Central ER, itemized bill, date of service [__________] (statement dated February 5, 2026): $6,240.00'  state=not_stated reason=non_service_date
== D8 bill: statement date leader only, then leadered charge (expect blank)  
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
== D9 bill: statement date leader + DOS leader + charge  
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
== D10 bill: next-visit leader after charge (expect blank or none)  
    $6,240.00 -> letter head: 'Central ER, itemized bill, date of service [__________] (statement dated February 5, 2026): $6,240.00'  state=not_stated reason=non_service_date
== D11 ER note: 'Next visit date.......01/16/2026' then ER charges (expect Jan 9)  
       $6,240 -> letter head: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
== D12 PCP note: 'Last date of service.......01/09/2026' then office charge (expect Jan 16)  
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== O1 PCP 01/16: 'Reviewed ER records, DOS 01/09/2026, office visit charge'  
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O2 PCP 01/16: 'Last seen DOS 01/09/2026' (seen, not last, before DOS)  
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O3 PCP 01/16: 'ER visit date of service 01/09/2026'  
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O4 PT visit 9 03/06: 'Previous visit's date of service 02/20/2026'  
      $185.00 -> letter head: 'Capital PT, visit 9, February 20, 2026: $185.00'  state=stated reason=None
== O5 PT visit 9 03/06: 'Initial eval DOS 01/23/2026'  
      $185.00 -> letter head: 'Capital PT, visit 9, January 23, 2026: $185.00'  state=stated reason=None
== O6 PCP 01/16: 'Prior  DOS 01/09/2026' (two spaces)  
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O7 PCP 01/16: 'Follow up DOS' (no hyphen) prior date  
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O8 PCP 01/16: ER DOS in its own sentence (control: sentence break)  
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== O9 PCP 01/16: 'Previous DOS: 01/09/2026' (listed qualifier, control)  
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== O10 PCP 01/16: checkout line 'ER DOS: 01/09/2026   Visit charge: $150.00'  
      $150.00 -> letter head: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
== S1 'Hobbleton Family Clinic' 03/01: Amount due ... office visit on 02/02/2026  
      $275.00 -> letter head: 'Hobbleton Family Clinic, March 1, 2026: $275.00'  state=stated reason=None
== S2 'Austin Imaging' 06/20: Patient responsibility ... MRI performed 05/29/2026  
    $2,150.00 -> letter head: 'Austin Imaging, June 20, 2026: $2,150.00'  state=stated reason=None
== S3 'Capital Physical Therapy' 03/20: Total due for 9 visits  
    $1,665.00 -> letter head: 'Capital Physical Therapy, March 20, 2026: $1,665.00'  state=stated reason=None
== S4 'Central ER' 02/05: Amount owed (emergency visit 01/09/2026)  
    $6,240.00 -> letter head: 'Central ER, February 5, 2026: $6,240.00'  state=stated reason=None
== S5 'Hill Country Pain Management' 07/01: thank-you then balance  
      $450.00 -> letter head: 'Hill Country Pain Management, July 1, 2026: $450.00'  state=stated reason=None
== S6 'Gloamwood Chiropractic' 04/30: Please remit for treatment 03/02/2026-04/10/2026  
    $1,200.00 -> letter head: 'Gloamwood Chiropractic, April 30, 2026: $1,200.00'  state=stated reason=None
== S7 'Austin Imaging, cervical MRI' 06/20 (encounter label) but the excerpt is the bill  
    $2,150.00 -> letter head: 'Austin Imaging, cervical MRI, June 20, 2026: $2,150.00'  state=stated reason=None
== S8 'Hobbleton Family Clinic' 03/01 control: opening with 'Statement' (expect blank)  
      $275.00 -> letter head: 'Hobbleton Family Clinic, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
== T1 PT visit 9 03/06: total for visits 1-9 in the discharge note  
    $1,665.00 -> letter head: 'Capital PT, visit 9, March 6, 2026: $1,665.00'  state=stated reason=None
== T2 PT visit 9 03/06: PT charges to date  
    $1,665.00 -> letter head: 'Capital PT, visit 9, March 6, 2026: $1,665.00'  state=stated reason=None
== T3 ER note 01/10 (summary written next day): arrived 01/09/2026  
       $6,240 -> letter head: 'Central ER discharge summary, January 10, 2026: $6,240'  state=stated reason=None
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:03:23.395Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat evals/golden/case_09_nonvisit_hides_gap.txt; grep -h \"^Source:\" evals/golden/*.txt evals/library/*.txt | sort | uniq -c | sort -rn | awk '{$1=\"\";print}' | head -150 | tr '\\n' '|' ",
 "description": "Read case_09 and list corpus source labels"
}
````

### User / tool · 2026-11-03T02:03:23.526Z

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

 Source: Thistlewick Orthopedics, Dr. Beatrix Quillon| Source: Dr. Eudora Fennimore, orthopedics| Source: Hobbleton Family Clinic, visit| Source: Dr. Ophelia Marchbanks, primary care| Source: Dr. Odalys Pennywhistle, plastic surgery| Source: Wombleton Orthopedics, Dr. Tallowby| Source: Thornbury Regional ED| Source: Sunderland Chiropractic, itemized statement| Source: Pottsworth Emergency Department| Source: Pelham Ridge EMS run report| Source: Dr. Tabitha Wrenfield, orthopedics| Source: Dr. Orla Pennywhistle, primary care| Source: Dr. Lucan Pettibone, orthopedics| Source: Dr. Ignatius Wardlaw, orthopedics, follow-up| Source: Dr. Fenwick Larkspur, orthopedics, follow-up| Source: Dr. Corwin Pettibone, primary care, follow-up| Source: Dr. Casimir Voss, orthopedic surgery, operative report| Source: Dr. Casimir Voss, orthopedic surgery, clinic| Source: Wrenfield EMS run report| Source: Wexcombe Memorial ED| Source: Wardlaw Orthopedics, CMS-1500 (OCR of scanned claim)| Source: Vessel Grove Medical Center ED| Source: Vessel Grove Imaging, lumbar MRI| Source: Valley Imaging, cervical MRI| Source: Tumblebrook Urgent Care| Source: Tumblebrook Physical Therapy| Source: Tumblebrook Imaging, shoulder MRI| Source: Thornapple Valley Hospital ED| Source: Thimbleby Chiropractic, visit 22| Source: Thimbleby Chiropractic, visit 14| Source: Thimbleby Chiropractic, initial exam| Source: Thimbleby Chiropractic, discharge| Source: Tarnwick Fire-Rescue, ambulance invoice| Source: Tarnwick Fire-Rescue run report| Source: Tamsin Valley Urgent Care| Source: Tamsin Imaging, right knee MRI| Source: Tallowby Fire-Rescue run report| Source: Sunderland Chiropractic, visit 6| Source: Sunderland Chiropractic, visit 18| Source: Sunderland Chiropractic, new patient| Source: Sunderland Chiropractic, correspondence, narrative letter| Source: Snickerwood ER| Source: Saltmarrow General Hospital, discharge summary| Source: Saltmarrow General Hospital, UB-04 itemized bill| Source: Saltmarrow General Hospital ED| Source: Sablewood Market first-aid log| Source: Redhaven Regional ED| Source: Redhaven Imaging, lumbar MRI| Source: Rainhollow Fire-Rescue run report| Source: Quoinmere Mutual Health Plan, EOB| Source: Quillmere Regional ED| Source: Quillfeather Urgent Care| Source: Quarry Hill Occupational Health, intake| Source: Plumtree Physical Therapy, visit 6| Source: Plumtree Physical Therapy, initial evaluation| Source: Plumtree Physical Therapy, evaluation| Source: Plumtree Physical Therapy, discharge| Source: Pennyroyal Records Retrieval, 18.001 affidavit| Source: Pemberwick Physical Therapy, visit 4| Source: Pemberwick Physical Therapy, visit 3| Source: Pemberwick Physical Therapy, visit 2| Source: Pemberwick Physical Therapy, visit 1| Source: Pellingham and Rook PLLC, correspondence (letter of protection)| Source: Orrin Vale Community ED| Source: Orrin Mere Regional ED| Source: Okmarrow EMS run report| Source: Nimblewick Hand Therapy, intake| Source: Mosswood Physical Therapy, visit 12| Source: Mosswood Physical Therapy, initial evaluation| Source: Marrowgate General ED| Source: Marlpit Fire-Rescue run report| Source: Marlowe Assurance Group, correspondence, records review letter| Source: Larkmoor Physical Therapy, visit 22| Source: Larkmoor Physical Therapy, visit 12| Source: Larkmoor Physical Therapy, initial evaluation| Source: Larkmoor Physical Therapy, discharge| Source: Larchmont Ridge Imaging, right shoulder MRI| Source: Larchmont Ridge ED| Source: Hollowbrook Chiropractic, re-examination (typed)| Source: Hollowbrook Chiropractic, daily note visit 9 (scanned, OCR text)| Source: Hollowbrook Chiropractic, daily note visit 12 (handwritten, OCR text)| Source: Hollowbrook Chiropractic, daily note visit 1 (scanned, OCR text)| Source: Hollowbrook Chiropractic, CMS-1500 (OCR of scanned claim)| Source: Hobbleton Family Clinic, phone note| Source: Hobbleton Family Clinic, billing statement| Source: Hill Country Pain Management, new patient| Source: Hill Country Pain Management, follow-up| Source: Harrowmere Physical Therapy, visit 8| Source: Harrowmere Physical Therapy, visit 16| Source: Harrowmere Physical Therapy, itemized statement| Source: Harrowmere Physical Therapy, initial evaluation| Source: Harrowmere Physical Therapy, functional capacity evaluation| Source: Harlow Memorial ED| Source: Gloamwood Chiropractic, visit 3| Source: Gloamwood Chiropractic, visit 2| Source: Gloamwood Chiropractic, initial evaluation| Source: Gloamwood Chiropractic, billing statement| Source: Gannet and Moor Injury Clinic, new patient| Source: Gannet and Moor Injury Clinic, injection visit| Source: Gannet and Moor Injury Clinic, follow-up| Source: Gannet and Moor Injury Clinic, billing statement| Source: Fernwhistle County EMS| Source: Fennimoor Spine Clinic, visit 8| Source: Fennimoor Spine Clinic, visit 14| Source: Fennimoor Spine Clinic, new patient intake form (OCR text)| Source: Fennimoor Spine Clinic, new patient| Source: Fennimoor Spine Clinic, itemized ledger| Source: Eastvale Fire-Rescue run report| Source: Dunmarrow Fire-Rescue run report| Source: Dr. Tabitha Wrenfield, Orthopedics| Source: Dr. Philippa Wenlock, orthopedics, new patient| Source: Dr. Philippa Wenlock, orthopedics, follow-up| Source: Dr. Orla Pennywhistle, phone note| Source: Dr. Odalys Pennywhistle, plastic surgery, operative note| Source: Dr. Marisol Dunmore, primary care, follow-up| Source: Dr. Marisol Dunmore, primary care| Source: Dr. Lysander Quibble, sports medicine| Source: Dr. Lucan Ostrowe, orthopedics, new patient| Source: Dr. Lucan Ostrowe, orthopedics, follow-up| Source: Dr. Imelda Quarrington, primary care| Source: Dr. Ignatius Wardlaw, orthopedics, new patient| Source: Dr. Hobart Wimbleton, radiology| Source: Dr. Hesper Alderton, primary care| Source: Dr. Fenwick Larkspur, orthopedics, new patient| Source: Dr. Corwin Pettibone, primary care| Source: Dr. Ansgar Kellerman, neurology| Source: Dr. Ambrose Thistlewaite, orthopedics| Source: Dr. Alvarez, primary care| Source: Crumpet Lane Orthopedics, M. Tallowby, MD| Source: Consultorio Médico Aguaclara, nota de consulta| Source: Consultorio Médico Aguaclara, formulario de admisión (OCR)| Source: Consultorio Médico Aguaclara, estado de cuenta (billing statement)| Source: Coldharbor Trauma Center ED| Source: Cobblewood Urgent Care| Source: Cobblestone Imaging, lumbar MRI| Source: Cobblestone Imaging| Source: Cinder Valley Imaging, right shoulder MRI| Source: Central ER discharge summary| Source: Cedar Run Physical Therapy, visit 10| Source: Cedar Run Physical Therapy, initial evaluation| Source: Capital PT, visit 9| Source: Capital PT, visit 8| Source: Capital PT, initial evaluation| Source: Bumblethorpe Urgent Care| Source: Bumblethorpe Physical Therapy, visit 2| Source: Bumblethorpe Physical Therapy, visit 1| Source: Brindlewick Fire-Rescue run report| Source: Brightwater EMS run report| Source: Austin Imaging, cervical MRI| Source: Austin EMS run report|
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:03:31.805Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/corpus_kinds.py",
 "content": "\"\"\"T-202 r4 paralegal: every record in evals/golden and evals/library that holds a dollar figure, with service_date.record_kind and the date each figure\nwould print (store.charge_service_date), to see which provider-name-only sources are read as encounters and what their figures print.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/corpus_kinds.py <archive_root>\n\"\"\"\nimport glob\nimport os\nimport re\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, store, service_date as SD  # noqa: E402\n\nREC = re.compile(r\"=== Record (\\d+) ===\\s*\\nDate: ([^\\n]*)\\nSource: ([^\\n]*)\\nExcerpt: \\\"(.*?)\\\"\\s*(?=\\n=== Record|\\Z)\", re.S)\nfor path in sorted(glob.glob(\"evals/golden/*.txt\") + glob.glob(\"evals/library/*.txt\")):\n    text = open(path).read()\n    for m in REC.finditer(text):\n        n, d, src, ex = m.groups()\n        figs = [a for a in AM.find_amounts(ex) if a.get(\"cents\") is not None]\n        if not figs:\n            continue\n        kind = SD.record_kind(src, ex)\n        rd = d.strip() if re.match(r\"\\d{4}-\\d{2}-\\d{2}$\", d.strip()) else None\n        rec = {\"id\": \"r\", \"n\": int(n), \"source\": src, \"date_iso\": rd, \"excerpt\": ex, \"text\": ex}\n        outs = []\n        for a in figs:\n            item = {\"excerpt\": ex, \"value_cents\": a[\"cents\"], \"raw\": a[\"raw\"], \"excerpt_start\": 0}\n            r = store.charge_service_date(item, rec, a[\"start\"])\n            outs.append(f\"{a['raw']} -> {r['text']}\")\n        print(f\"{os.path.basename(path)} r{n} [{kind}] {d.strip()} | {src} | {ex[:90]!r}\")\n        for o in outs:\n            print(\"     \", o)\n"
}
````

### User / tool · 2026-11-03T02:03:31.906Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/corpus_kinds.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:03:37.326Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; LLM_BACKEND=fixture .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/corpus_kinds.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2 > artifacts/review-evidence/T-202-paralegal-r4/corpus_kinds.out 2>&1; grep -c \"^\\S\" artifacts/review-evidence/T-202-paralegal-r4/corpus_kinds.out; grep \"\\[encounter\\]\\|\\[other\\]\" -A3 artifacts/review-evidence/T-202-paralegal-r4/corpus_kinds.out | head -80",
 "description": "Scan corpus records with figures by kind"
}
````

### User / tool · 2026-11-03T02:03:37.711Z

**tool result**
````
54
case_01_date_formats.txt r1 [encounter] 2026-02-03 | Quillfeather Urgent Care | 'Right ankle swelling after twisting on stairs. X-ray negative for fracture. Urgent care ch'
      $310.00 -> February 3, 2026
case_03_rate_and_ocr.txt r1 [encounter] 2026-08-03 | Gloamwood Chiropractic, initial evaluation | 'Low back pain 5/10. Treatment plan: 8 visits. Fee schedule: $95 per adjustment.'
      $95 -> August 3, 2026
case_03_rate_and_ocr.txt r3 [encounter] 2026-08-17 | Gloamwood Chiropractic, visit 2 | 'Adjustment performed. Pain 4/10. Charge: $95.00.'
      $95.00 -> August 17, 2026
case_03_rate_and_ocr.txt r5 [encounter] 2026-09-02 | Dr. Hobart Wimbleton, radiology | 'Lumbar spine X-ray, 2 views. Radiology charge: $240.'
      $240 -> September 2, 2026
case_05_provider_conflict.txt r2 [encounter] 2026-06-01 | Thornapple Valley Hospital ED | 'Dx: left clavicle fracture. Sling provided. Refer to orthopedics, Dr. Mortimer Tallowby. E'
      $4,380 -> June 1, 2026
case_07_prompt_injection.txt r1 [encounter] 2026-03-02 | Bumblethorpe Urgent Care | 'Fall on ice, left knee pain 6/10. X-ray negative for fracture. Charge: $420.'
      $420 -> March 2, 2026
case_08_diagnosis_temptation.txt r2 [encounter] 2026-10-20 | Tumblebrook Imaging, shoulder MRI | 'Signal change in the supraspinatus tendon. Clinical correlation recommended. Charge: $1,87'
      $1,875 -> October 20, 2026
case_09_nonvisit_hides_gap.txt r2 [bill] 2026-03-01 | Hobbleton Family Clinic, billing statement | 'Statement for visit of 2026-02-02: $275.'
      $275 -> February 2, 2026
sample.txt r2 [encounter] 2026-01-09 | Central ER discharge summary | 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclob'
      $6,240 -> January 9, 2026
sample.txt r4 [encounter] 2026-01-23 | Capital PT, initial evaluation | 'Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $1'
      $185 -> January 23, 2026
sample.txt r8 [encounter] 2026-05-29 | Austin Imaging, cervical MRI | 'C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenera'
      $2,150 -> May 29, 2026
case_lib01_er_only_then_gap.txt r2 [encounter] 2026-02-14 | Marrowgate General ED | 'Dx: cervical strain. X-ray cervical spine negative for fracture. Rx ibuprofen 600 mg. Foll'
      $3,915 -> February 14, 2026
case_lib01_er_only_then_gap.txt r4 [encounter] 2026-04-13 | Plumtree Physical Therapy, initial evaluation | 'Cervical range of motion reduced approx. 30%. Plan of care: 8 visits. Charge per visit $14'
      $140 -> April 13, 2026
case_lib02_slip_fall_prior_knee.txt r2 [encounter] 2026-03-09 | Tamsin Valley Urgent Care | 'Right knee pain 7/10 with swelling. X-ray right knee: no acute fracture; prior arthroscopi'
      $410 -> March 9, 2026
case_lib02_slip_fall_prior_knee.txt r4 [encounter] 2026-03-30 | Tamsin Imaging, right knee MRI | 'Medial meniscus tear with moderate joint effusion. Mild tricompartmental degenerative chan'
      $1,850 -> March 30, 2026
case_lib02_slip_fall_prior_knee.txt r6 [encounter] 2026-05-04 | Cedar Run Physical Therapy, initial evaluation | 'Right knee flexion limited to 100 degrees. Plan of care: 10 visits. Charge per visit $155.'
      $155 -> May 4, 2026
case_lib03_truck_rear_end_chiro.txt r2 [encounter] 2026-04-06 | Redhaven Regional ED | 'Dx: lumbar and cervical sprain. CT cervical spine negative. Rx naproxen. Refer to chiropra'
      $5,260 -> April 6, 2026
case_lib03_truck_rear_end_chiro.txt r3 [encounter] 2026-04-09 | Thimbleby Chiropractic, initial exam | 'Cervical and lumbar spasm. Plan: 3 visits per week for 12 weeks. Charge per visit $120.'
      $120 -> April 9, 2026
case_lib03_truck_rear_end_chiro.txt r7 [encounter] 2026-07-20 | Redhaven Imaging, lumbar MRI | 'L4-L5 disc bulge without nerve root compression. Mild disc desiccation. Radiology: finding'
      $2,240 -> July 20, 2026
case_lib04_dog_bite_scar_revision.txt r2 [encounter] 2025-09-13 | Harlow Memorial ED | 'Dx: dog bite, left cheek laceration 4 cm and chin laceration 2 cm. Wounds irrigated and su'
      $4,730 -> September 13, 2025
case_lib04_dog_bite_scar_revision.txt r5 [encounter] 2025-12-13 | Dr. Odalys Pennywhistle, plastic surgery | 'Scar remains raised at 3 months. Revision discussed if no improvement by 12 months. Estima'
      $6,500 -> December 13, 2025
case_lib04_dog_bite_scar_revision.txt r6 [encounter] 2026-09-12 | Dr. Odalys Pennywhistle, plastic surgery, operative note | 'Scar revision performed under local anesthesia. Surgeon fee: $3,900. Photographs taken.'
      $3,900 -> September 12, 2026
case_lib05_pedestrian_orif_hardware.txt r2 [encounter] 2026-01-22 | Coldharbor Trauma Center ED | 'Dx: left tibial plateau fracture and left fibular fracture. Splinted. Admitted to orthoped'
      $38,420 -> January 22, 2026
case_lib05_pedestrian_orif_hardware.txt r5 [encounter] 2026-03-05 | Mosswood Physical Therapy, initial evaluation | 'Left knee flexion limited to 80 degrees. Plan of care: 16 visits. Charge per visit $175.'
      $175 -> March 5, 2026
case_lib05_pedestrian_orif_hardware.txt r8 [encounter] 2026-09-10 | Dr. Casimir Voss, orthopedic surgery, operative report | 'Removal of hardware, left tibial plateau. Subchondral cyst repaired. Total knee replacemen'
      $6,150 -> September 10, 2026
case_lib06_lop_billed_vs_adjusted.txt r2 [encounter] 2026-05-02 | Larchmont Ridge ED | 'Dx: right shoulder contusion. X-ray negative. Sling provided. ED charge: $2,880.'
      $2,880 -> May 2, 2026
case_lib06_lop_billed_vs_adjusted.txt r4 [bill] 2026-06-03 | Gannet and Moor Injury Clinic, billing statement | 'Statement of charges: office visits $1,100; MRI referral fee $450. Balance under letter of'
      $1,100 -> date of service [__________] (statement dated June 3, 2026)
--
case_lib06_lop_billed_vs_adjusted.txt r5 [encounter] 2026-06-17 | Larchmont Ridge Imaging, right shoulder MRI | 'Mild supraspinatus tendinosis; no full-thickness tear. Charge: $2,400. Insurance adjustmen'
      $2,400 -> June 17, 2026
      $1,250 -> June 17, 2026
      $1,150 -> June 17, 2026
case_lib07_parking_lot_fall_outside_records.txt r2 [encounter] 2026-02-10 | Cobblestone Imaging | 'X-ray right wrist: nondisplaced distal radius fracture. X-ray lumbar spine: mild degenerat'
      $640 -> February 10, 2026
case_lib07_parking_lot_fall_outside_records.txt r6 [encounter] 2026-05-12 | Cobblestone Imaging, lumbar MRI | 'L4-L5 disc protrusion with mild canal narrowing. Postoperative changes at L4-L5. Possible '
      $1,980 -> May 12, 2026
case_lib08_second_crash_mri_after.txt r2 [encounter] 2026-01-12 | Thornbury Regional ED | 'Dx: cervical strain. CT head negative. Denies LOC per patient. Discharged on cyclobenzapri'
      $4,210 -> January 12, 2026
case_lib08_second_crash_mri_after.txt r4 [encounter] 2026-01-26 | Larkmoor Physical Therapy, initial evaluation | 'Cervical range of motion reduced about 25%. Plan of care: 12 weeks, twice weekly. Charge p'
      $145 -> January 26, 2026
case_lib08_second_crash_mri_after.txt r9 [encounter] 2026-04-24 | Thornbury Regional ED | 'Dx: cervical strain. CT cervical spine negative for fracture. Denies LOC per patient. ED c'
      $4,680 -> April 24, 2026
case_lib08_second_crash_mri_after.txt r10 [encounter] 2026-05-20 | Valley Imaging, cervical MRI | 'C5-C6 disc herniation with mild canal narrowing. No prior imaging available for comparison'
      $2,350 -> May 20, 2026
case_lib09_spanish_interpreter_espalda.txt r1 [encounter] 2026-03-03 | Quillmere Regional ED | "Hx obtained via patient's son, who interpreted. Patient states she was struck by a car whi"
      $2,940 -> March 3, 2026
case_lib09_spanish_interpreter_espalda.txt r2 [encounter] 14/04/2026 | Consultorio Médico Aguaclara, nota de consulta | 'Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. R'
      $650.00 -> date of service [__________]
      $400.00 -> date of service [__________]
case_lib09_spanish_interpreter_espalda.txt r5 [encounter] 2026-05-05 | Cinder Valley Imaging, right shoulder MRI | 'Partial-thickness supraspinatus tear. MRI charge: $2,150.'
      $2,150 -> May 5, 2026
case_lib09_spanish_interpreter_espalda.txt r7 [bill] 2026-05-20 | Consultorio Médico Aguaclara, estado de cuenta (billing statement) | 'Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Sa'
      $1,300.00 -> date of service [__________] (statement dated May 20, 2026)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:03:48.448Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2; ls app/backend/; grep -n \"def .*source\\|source_label\\|\\\"source\\\":\" app/backend/ingest*.py 2>/dev/null | head -30",
 "description": "Look at how ingestion derives source labels"
}
````

### User / tool · 2026-11-03T02:03:48.562Z

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
encounter_types.json
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
service_date.py
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
94:    cov, f = [], {"date_raw": "", "source": "", "excerpt": "", "complete": False}
133:        return [_record(1, text, 0, len(text), {"date_raw": "", "source": "", "excerpt": text})], "ambiguous"
147:        items.append((s, e, {"date_raw": "", "source": "", "excerpt": text[s:e], "unsplit": True}))
161:    return {"n": n, "date_raw": p["date_raw"], "source": p["source"], "excerpt": p["excerpt"],
214:        f = f or {"date_raw": "", "source": "", "excerpt": "", "complete": False}
237:def record_kind(source: str, excerpt: str = "") -> str:
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:03:53.237Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2; sed -n 120,160p app/backend/ingest.py; sed -n 230,260p app/backend/ingest.py; grep -rn \"Source:\\|source\" app/backend/split_llm.py | head -10",
 "description": "Read ingest splitting and record_kind"
}
````

### User / tool · 2026-11-03T02:03:53.338Z

**tool result**
````
            seg = text[pos:s]
            if seg.strip():
                lead = len(seg) - len(seg.lstrip())
                out.append((pos + lead, pos + len(seg.rstrip())))
        pos = max(pos, e)
    return [(s, e) for s, e in out if not (s == 0 and text[s:e] in BANNERS)]


def _split(text: str):
    """(records, method). Every non-blank character of the input ends up inside some record; text outside a recognised block becomes
    an `unsplit` record (D-027) and the split is reported ambiguous."""
    spans = _spans(text)
    if not spans:
        return [_record(1, text, 0, len(text), {"date_raw": "", "source": "", "excerpt": text})], "ambiguous"
    items, method = [], "code"
    cov_all = [] if _HEADER.search(text) else [(m.start(), m.end()) for m in _SEP.finditer(text)]   # separator lines carry no content
    for a, b in spans:
        f, cov = _scan_block(text, a, b)
        cov_all += cov
        if f is None:
            continue
        if not f["complete"]:
            method = "ambiguous"
        end = max(e for _, e in cov)
        f["first"] = min(x for x, _ in cov)             # where the block's own fields start (a block can begin with a preamble line)
        items.append((a, end, f))
    for s, e in _leftovers(text, cov_all):
        items.append((s, e, {"date_raw": "", "source": "", "excerpt": text[s:e], "unsplit": True}))
        method = "ambiguous"
    # T-129: record numbers are the paralegal's citations, so they count only the real records, in paste order. Unsplit text (a preamble, a note between separators) is kept
    # (D-027: nothing is dropped) but numbered AFTER the real records, so a fax cover sheet on top never shifts "record 1" to "record 2". Text above the first real record
    # is marked `preamble`.
    items.sort(key=lambda t: (bool(t[2].get("unsplit")), t[0]))
    first_real = min((f["first"] for _a, _e, f in items if not f.get("unsplit")), default=None)
    for _a, e, f in items:
        if f.get("unsplit") and first_real is not None and e <= first_real:
            f["preamble"] = True
    return [_record(i + 1, text[a:e], a, e, f) for i, (a, e, f) in enumerate(items)], method


def _record(n: int, block: str, start: int, end: int, p: dict) -> dict:
    text = check_limits(raw_text, max_chars)
    recs, _ = _split(text)
    if len(recs) > max_records:
        raise IngestError("input_too_large")
    return recs


def record_kind(source: str, excerpt: str = "") -> str:
    """encounter | billing_statement | phone_note (| records_admin), decided by the lexicon `non_encounter` list on the header label only (D-003)."""
    if not (source or "").strip():
        return "unsplit_text"
    for e in lexicon.code_list("non_encounter"):
        if e["regex"].search(source or ""):
            return {"billing_document": "billing_statement", "phone_or_message": "phone_note"}.get(e["id"], "records_admin")
    return "encounter"


def _norm(s: str) -> str:
    return " ".join((s or "").split()).casefold()


def dedupe(records: list) -> list:
    """Groups of record numbers (in file order): same date + same normalised provider label + same normalised text merge (R-TL-7)."""
    groups, order = {}, []
    for r in records:
        p = dates.parse_date(r["date_raw"])
        key = (p["iso"] or _norm(r["date_raw"]), _norm(r["source"]), _norm(r["excerpt"]))
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(r["n"])
app/backend/split_llm.py:5:record_warning LLM_SPLIT (ingest.ingest). Fields (date, source, excerpt) never come from the model.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:04:09.181Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/diff_r3_r4.py",
 "content": "\"\"\"T-202 r4 paralegal: pair the letter heads of probe_r4.out (8cb5bd2) and probe_r4_on_973b542.out (973b542, round 3) probe by probe and print every\nfigure whose head changed, plus a count. Run from repo root:\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/diff_r3_r4.py\n\"\"\"\nimport os\nimport re\n\nD = os.path.dirname(os.path.abspath(__file__))\n\n\ndef parse(path):\n    out, cur = {}, None\n    for line in open(path):\n        if line.startswith(\"== \"):\n            cur = re.sub(r\"\\s+\\(record date.*\", \"\", line[3:].rstrip())\n            out[cur] = []\n        elif \"-> letter head:\" in line and cur:\n            out[cur].append(line.split(\"-> letter head:\")[1].strip())\n    return out\n\n\nr4 = parse(os.path.join(D, \"probe_r4.out\"))\nr3 = parse(os.path.join(D, \"probe_r4_on_973b542.out\"))\nchanged = 0\nfor k in r4:\n    if r4[k] != r3.get(k):\n        changed += 1\n        print(f\"== {k}\")\n        for a, b in zip(r3.get(k, []), r4[k]):\n            if a != b:\n                print(f\"   r3: {a}\\n   r4: {b}\")\nprint(f\"# probes {len(r4)}; changed {changed}\")\n"
}
````

### User / tool · 2026-11-03T02:04:09.275Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/diff_r3_r4.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:04:11.683Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/diff_r3_r4.py > artifacts/review-evidence/T-202-paralegal-r4/diff_r3_r4.out; cat artifacts/review-evidence/T-202-paralegal-r4/diff_r3_r4.out | grep -v \"^== [DOST][0-9]\" | head -120",
 "description": "Diff r3 vs r4 probe results"
}
````

### User / tool · 2026-11-03T02:04:11.797Z

**tool result**
````
== probe_r3 R1 visit note: next visit date in the charge sentence
   r3: 'Dr. Alvarez, primary care, January 30, 2026: $150.00'  state=stated reason=None
   r4: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== probe_r3 R2 visit note: prior visit 'seen on' in the charge sentence
   r3: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
   r4: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== probe_r3 R13 bill: 'Seen on' with referral date first
   r3: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
   r4: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
== probe_r3b R1 visit note 01/16: next visit date in the charge sentence
   r3: 'Dr. Alvarez, primary care, January 30, 2026: $150.00'  state=stated reason=None
   r4: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== probe_r3b R2 visit note 01/16: prior ER visit 'seen on' in the charge sentence
   r3: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
   r4: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== probe_r3b R17 visit note 01/16: checkout line, charge then next visit date
   r3: 'Dr. Alvarez, primary care, January 30, 2026: $150.00'  state=stated reason=None
   r4: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== probe_r3b R18 visit note 01/16: checkout line, last visit date then charge
   r3: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
   r4: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
== probe_r3b R19 PT discharge 03/06: initial visit date in the charge sentence
   r3: 'Capital PT, discharge summary, January 23, 2026: $185.00'  state=stated reason=None
   r4: 'Capital PT, discharge summary, March 6, 2026: $185.00'  state=stated reason=None
== probe_r3b R21 PT discharge 03/06: 'treatment dates' period then a charge
   r3: 'Capital PT, discharge summary, January 23–March 6, 2026: $1,665.00'  state=stated reason=None
   r4: 'Capital PT, discharge summary, March 6, 2026: $1,665.00'  state=stated reason=None
== probe_r3b R23 bill 03/01: next visit date (future) in a coded line
   r3: 'Hobbleton Family Clinic, billing statement, February 28, 2026: $275.00'  state=stated reason=None
   r4: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
== probe_r3c C3 ER 01/09: charge, then next visit date in its own sentence
   r3: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
   r4: 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240'  state=not_stated reason=no_date
== probe_r3c C4 ER 01/09: charge, then next visit date after a comma
   r3: 'Central ER discharge summary, January 16, 2026: $6,240'  state=stated reason=None
   r4: 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240'  state=not_stated reason=non_service_date
== probe_r3c C6 PT eval 01/23: plan + next visit date + rate, one line no periods
   r3: 'Capital PT, initial evaluation, January 27, 2026: $185'  state=stated reason=None
   r4: 'Capital PT, initial evaluation, January 23, 2026: $185'  state=stated reason=None
== probe_r3c C7 ER 01/09: two spaces as separators, follow-up visit date then charge
   r3: 'Central ER discharge summary, January 16, 2026: $6,240'  state=stated reason=None
   r4: 'Central ER discharge summary, January 9, 2026: $6,240'  state=stated reason=None
   r3: 'Central ER, itemized bill, date of service [__________] (statement dated February 5, 2026): $6,240.00'  state=not_stated reason=no_date
   r4: 'Central ER, itemized bill, January 9, 2026: $6,240.00'  state=stated reason=None
   r3: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00'  state=not_stated reason=no_date
   r4: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00'  state=not_stated reason=ambiguous_numeric
   r3: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=no_date
   r4: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
   r3: 'Central ER, itemized bill, date of service [__________] (statement dated February 5, 2026): $6,240.00'  state=not_stated reason=no_date
   r4: 'Central ER, itemized bill, January 9, 2026: $6,240.00'  state=stated reason=None
   r3: 'Central ER, itemized bill, date of service [__________] (statement dated February 5, 2026): $6,240.00'  state=not_stated reason=non_service_date
   r4: 'Central ER, itemized bill, January 9, 2026: $6,240.00'  state=stated reason=None
   r3: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
   r4: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
   r3: 'Dr. Alvarez, primary care, January 9, 2026: $150.00'  state=stated reason=None
   r4: 'Dr. Alvarez, primary care, January 16, 2026: $150.00'  state=stated reason=None
# probes 115; changed 21
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:04:34.488Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4; rm letters_dump_r3.py before_t202.py; sed -n 405,500p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2/evals/letter_check.py",
 "description": "Read letter_check charge date check"
}
````

### User / tool · 2026-11-03T02:04:34.580Z

**tool result**
````
        if len(heads) == len(cells):
            for (cs, ct), (hs, ht) in zip(cells, heads):
                if cs <= col < cs + len(ct):
                    return ht
        return min(heads, key=lambda h: abs(h[0] - col))[1]
    return ""


def charge_date_violations(letter: str, records) -> list:
    """D-071 amendment, round 3 (allow-list): every charge line's printed date against THAT line's own quote (plus, for a quote with no labeled date, the bill's period before it).
    `records`: the case's [{n, source, date_iso, excerpt}]. Per line, the quote's LABELED dates are those with a service phrase right before them or a table heading over them that
    names the service; every other date in it (birth, injury, onset, referral, order, entry, transaction, posted, statement, unlabeled) is not a service date.
      - labeled dates that have exactly one certain reading (one date or period, one reading, not after its statement, not years before it) -> the line prints exactly that, whole;
      - labeled dates that are doubtful (several readings, two-digit year, no year, impossible, several dates, implausible) -> the line prints the blank, nothing else;
      - no labeled date in the quote, in a bill -> the one period the bill states before it (whole), else the blank 'date of service [__________] (statement dated X)' with X the
        record's date; in a visit note (not a bill) -> the note's own date (the blank is a violation there).
    A date printed where the quote labels none, a blank above a certain labeled date, and a statement date that is not the record's are violations."""
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
            if kind == "blank":                                                                  # D-071 amendment 2 (c): the blank only in its exact form, anchored at both ends
                from datetime import date
                d = date.fromisoformat(rd) if rd else None
                want_head = f"{norm(r.get('source') or '')}, {BLANK}" + (f" (statement dated {d.strftime('%B')} {d.day}, {d.year})" if d else "")
                if norm(re.sub(r": \$[\d,]+\.\d\d$", "", head)) != want_head:
                    problems.append("the blank is not in its exact form (source, then 'date of service [__________]', then the record's statement date)")
                    continue
            kind_r = _record_kind(r.get("source"), ex)
            bill, lends = kind_r == "bill", kind_r == "encounter"          # only an encounter record lends its own date; the rest need a label
            ub = bool(_UB_WORD.search(r.get("source") or "") or _UB_WORD.search(ex))
            n_ex, n_q = norm(ex), norm(quote)
            before = n_ex[:n_ex.index(n_q)]
            units = _written(n_q)
            marks = _marked(n_q, units, _SERVICE_PHRASES + (_BILL_PHRASES if bill else ()) + (_UB_PHRASES if ub else ()), before + n_q, len(before))
            for k, u in enumerate(units):                                                       # a table heading over the date that names the service labels it too
                if not marks[k]:
                    marks[k] = bool(_names_service(_heading_over(ex, quote, u["start"])))
            lab = [u for u, m in zip(units, marks) if m]
            if lab:
                reads = [_readings(u, rd) for u in lab]
                same = {x for rr in reads for x in rr}
                certain = all(len(rr) == 1 for rr in reads) and len(same) == 1
                texts = sorted(norm(n_q[u["start"]:u["end"]]) for u in lab)
                if certain:
                    if kind in ("range", "one"):
                        if (first, last) != next(iter(same)):
                            problems.append(f"the quote's labeled date of service reads {next(iter(same))[0]}" + (f" to {next(iter(same))[1]}" if next(iter(same))[1] else ""))
                    else:
                        problems.append("the quote labels one certain date of service and the line prints a blank")
                elif kind != "blank":
                    problems.append("the quote labels a date of service the writing leaves doubtful (" + ", ".join(texts) + ") and the line prints a date")
                elif first and first != rd:
                    problems.append("the statement date is not the record's date")
                continue
            # no labeled date in the quote
            bu = _written(before)
            pm = _marked(before, bu, _PERIOD_PHRASES + (_UB_PHRASES if ub else ()))
            pu = [u for u, m in zip(bu, pm) if m] if bill else []
            if kind == "blank":
                if first and first != rd:
                    problems.append("the statement date is not the record's date")
                elif lends and rd:
                    problems.append("an encounter record's line must carry the record's own date")
                continue
            if bill:
                reads = [_readings(u, rd) for u in pu]
                same = {x for rr in reads for x in rr}
                if len(pu) < 1 or not all(len(rr) == 1 for rr in reads) or len(same) != 1:
                    problems.append("no date of service is labeled for this line and the line prints one")
                    continue
                want = next(iter(same))
            else:
                want = (rd, None) if (lends and rd) else None
            if want is None or (first, last) != want:
                problems.append("the line prints a date no service label ties to it" + (f" (the label gives {want[0]})" if want else ""))
        if len(problems) == len(recs):
            out.append(f"charge line's date is not certain from its quote ({'; '.join(sorted(set(problems)))}): {head}")
    return out


def letters_for(text: str, backend: str = "fixture") -> dict:
    """{'all_accepted': {...}, 'charges_dismissed': {...}}, each {'letters': {style: text}, 'notes': str, 'charge_cents': [...], 'refused': [(id, code)], 'gate': {style: [why...]}}."""
    from app.backend import export, ingest as IN, pipeline as PL, store
    from app.llm import provider as P
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:04:57.955Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/letters_dump_r4.py",
 "content": "\"\"\"T-202 r4 paralegal: in-process letters + internal notes (all_accepted and counted) for sample, case_09, lib14, lib10, lib11 and SYNTHETIC variants\n(rounds 2-3 variants kept; round 4 adds dotted-leader, other-visit DOS, treatment-dates-in-a-visit-note and provider-name-only-bill variants), with\nevals.letter_check.charge_date_violations on each. Writes letters to <out_dir> when given. Works on older archives (falls back when a function is missing).\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/letters_dump_r4.py <archive_root> [<out_dir>]\n\"\"\"\nimport os\nimport sys\nimport traceback\n\nroot = os.path.abspath(sys.argv[1])\nout = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None\nsys.path.insert(0, root)\nos.chdir(root)\nos.environ.setdefault(\"LLM_BACKEND\", \"fixture\")\nos.environ.setdefault(\"FIXTURE_SET\", \"curated\")\nfrom evals import letter_check as LC  # noqa: E402\n\n\ndef sub(text, old, new):\n    assert old in text, old\n    return text.replace(old, new)\n\n\nSAMPLE = open(\"evals/golden/sample.txt\").read()\nC09 = open(\"evals/golden/case_09_nonvisit_hides_gap.txt\").read()\nC09_R2 = 'Date: 2026-03-01\\nSource: Hobbleton Family Clinic, billing statement\\nExcerpt: \"Statement for visit of 2026-02-02: $275.\"'\nER_TAIL = \"Follow up with PCP in 1 week. ER charges: $6,240.\"\nCASES = {\n    \"sample\": SAMPLE,\n    \"case_09\": C09,\n    \"lib14\": open(\"evals/library/case_lib14_handwritten_chiro_scans.txt\").read(),\n    \"lib10\": open(\"evals/library/case_lib10_eob_ub04_cms1500.txt\").read(),\n    \"lib11\": open(\"evals/library/case_lib11_priors_and_ledger.txt\").read(),\n    # round 2\n    \"synth_ambiguous_dos\": sub(C09, C09_R2, 'Date: 2026-06-01\\nSource: Hobbleton Family Clinic, billing statement\\nExcerpt: \"Date of service 04/05/2026: office visit charge $275.00.\"'),\n    \"synth_cms1500_two_dates\": sub(C09, C09_R2, 'Date: 2026-04-20\\nSource: Hobbleton Family Clinic, CMS-1500\\nExcerpt: \"CMS-1500 for dates of service 02/02/2026 and 03/30/2026. CPT 99213 charge $150.00. CPT 29125 splint charge $125.00.\"'),\n    # round 3 blocker text: next visit date after the ER charge, comma-joined\n    \"synth_sample_er_next_visit\": sub(SAMPLE, ER_TAIL, \"Follow up with PCP in 1 week. ER charges: $6,240, next visit date 01/16/2026.\"),\n    # round 4: dotted leader (brief text) in the ER note, and in the case_09 bill\n    \"synth_sample_er_dotted_leader\": sub(SAMPLE, ER_TAIL, \"Follow up with PCP in 1 week. Date of service.......01/09/2026   ER charges ...... $6,240.\"),\n    \"synth_case09_bill_dotted_leader\": sub(C09, C09_R2, 'Date: 2026-03-01\\nSource: Hobbleton Family Clinic, billing statement\\nExcerpt: \"Date of service.......02/02/2026   Office visit 99213 ...... $275.00\"'),\n    # round 4: a prior visit's DOS in the PCP note's charge clause (qualifier not in the lookbehind list)\n    \"synth_sample_pcp_er_dos\": sub(SAMPLE, \"Patient reports low back pain in 2023, resolved.\", \"Patient reports low back pain in 2023, resolved. Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.\"),\n    # round 4: a stated treatment period for a multi-visit charge inside the PT discharge note (round 3 printed the range)\n    \"synth_sample_pt_treatment_dates\": sub(SAMPLE, \"Discharged from PT after two missed appointments. Pain 3/10.\", \"Discharged from PT after two missed appointments. Pain 3/10. Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.\"),\n    # round 4: the case_09 bill labelled with the provider name only (no record-type word), excerpt naming its own visit date\n    \"synth_case09_provider_only_bill\": sub(C09, C09_R2, 'Date: 2026-03-01\\nSource: Hobbleton Family Clinic\\nExcerpt: \"Amount due $275.00 for office visit on 02/02/2026.\"'),\n}\nonly = os.environ.get(\"ONLY\")\nfor name, text in CASES.items():\n    if only and name not in only.split(\",\"):\n        continue\n    try:\n        got = LC.letters_for(text)\n    except Exception:\n        print(f\"== {name}: letters_for raised\\n{traceback.format_exc()}\")\n        continue\n    for variant in (\"all_accepted\", \"counted\"):\n        if variant not in got:\n            continue\n        v = got[variant]\n        letter = v[\"letters\"][\"standard\"]\n        if out:\n            with open(os.path.join(out, f\"{name}-{variant}-letter.txt\"), \"w\") as f:\n                f.write(letter)\n            with open(os.path.join(out, f\"{name}-{variant}-notes.txt\"), \"w\") as f:\n                f.write(v[\"notes\"])\n        print(f\"== {name} {variant}: cents={v.get('charge_cents')} refused={v.get('refused')} gate={v.get('gate')}\")\n        if hasattr(LC, \"charge_lines\"):\n            for h, q in LC.charge_lines(letter):\n                print(\"   \", h, \"|\", q)\n        else:\n            i = letter.find(\"BILLED CHARGES\")\n            print(\"    \" + letter[i:].replace(\"\\n\", \"\\n    \") if i >= 0 else \"    (no BILLED CHARGES section)\")\n        if hasattr(LC, \"charge_date_violations\") and \"records\" in v:\n            print(\"    date violations:\", LC.charge_date_violations(letter, v[\"records\"]))\n"
}
````

### User / tool · 2026-11-03T02:04:58.054Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/letters_dump_r4.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:04.230Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; LLM_BACKEND=fixture FIXTURE_SET=curated .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/letters_dump_r4.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/letters > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/letters_dump_r4.out 2>&1; grep -v \"^    date violations: \\[\\]$\" artifacts/review-evidence/T-202-paralegal-r4/letters_dump_r4.out | grep -v \"^\\s*$\" | cut -c1-330",
 "description": "Dump letters for corpus and variants on r4",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T02:05:11.658Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:14.233Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -v \"^llm call failed\" artifacts/review-evidence/T-202-paralegal-r4/letters_dump_r4.out | grep -v \"^\\s*$\" | cut -c1-400",
 "description": "Show letter dump charge lines"
}
````

### User / tool · 2026-11-03T02:05:14.326Z

**tool result**
````
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
== synth_cms1500_two_dates all_accepted: cents=[15000, 12500] refused=[] gate={'standard': ['Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’: “Source [Ex. __ / Bates __]: "CPT 99213 charge $150.00."”. A charge line carries its own amount only.', 'Line 8 of the letter is a Billed charges line for $125.00 and also states ‘29125 splint charge’: “
    Hobbleton Family Clinic, CMS-1500, date of service [__________] (statement dated April 20, 2026): $150.00 | CPT 99213 charge $150.00.
    Hobbleton Family Clinic, CMS-1500, date of service [__________] (statement dated April 20, 2026): $125.00 | CPT 29125 splint charge $125.00.
    date violations: []
== synth_cms1500_two_dates counted: cents=[15000, 12500] refused=[] gate={'standard': ['Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’: “Source [Ex. __ / Bates __]: "CPT 99213 charge $150.00."”. A charge line carries its own amount only.', 'Line 8 of the letter is a Billed charges line for $125.00 and also states ‘29125 splint charge’: “Sourc
    Hobbleton Family Clinic, CMS-1500, date of service [__________] (statement dated April 20, 2026): $150.00 | CPT 99213 charge $150.00.
    Hobbleton Family Clinic, CMS-1500, date of service [__________] (statement dated April 20, 2026): $125.00 | CPT 29125 splint charge $125.00.
    date violations: []
== synth_sample_er_next_visit all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | llm call failed call_id=c88933ab9a2a0 step=extract attempt=1 prompt_hash=32d445bf52cf2ee1e3b68b0a3b8b2b744ad3e6cbe6dba01525f66ca2af836160
ER charges: $6,240, next visit date 01/16/2026.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_next_visit counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240, next visit date 01/16/2026.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_dotted_leader all_accepted: cents=[215000] refused=[] gate={}
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_dotted_leader counted: cents=[215000] refused=[] gate={}
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_case09_bill_dotted_leader all_accepted: cents=[] refused=[] gate={}
    date violations: []
== synth_case09_bill_dotted_leader counted: cents=[] refused=[] gate={}
    date violations: []
== synth_sample_pcp_er_dos all_accepted: cents=[624000, 15000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Dr. Alvarez, primary care, January 9, 2026: $150.00 | Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pcp_er_dos counted: cents=[624000, 15000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Dr. Alvarez, primary care, January 9, 2026: $150.00 | Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pt_treatment_dates all_accepted: cents=[624000, 166500, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Capital PT, visit 9, March 6, 2026: $1,665.00 | Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pt_treatment_dates counted: cents=[624000, 166500, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Capital PT, visit 9, March 6, 2026: $1,665.00 | Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_case09_provider_only_bill all_accepted: cents=[] refused=[] gate={}
    date violations: []
== synth_case09_provider_only_bill counted: cents=[] refused=[] gate={}
    date violations: []
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:30.650Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ONLY=synth_sample_er_next_visit,synth_sample_er_dotted_leader,synth_case09_bill_dotted_leader,synth_sample_pcp_er_dos,synth_sample_pt_treatment_dates,synth_case09_provider_only_bill LLM_BACKEND=fixture FIXTURE_SET=curated .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/letters_dump_r4.py $SP/pr3_973b542 2>&1 | grep -v \"^llm call failed\" > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/variants_on_973b542.out; ONLY=synth_sample_er_next_visit,synth_sample_er_dotted_leader,synth_case09_bill_dotted_leader,synth_sample_pcp_er_dos,synth_sample_pt_treatment_dates,synth_case09_provider_only_bill LLM_BACKEND=fixture FIXTURE_SET=curated .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/letters_dump_r4.py $SP/pre_bd72d5b 2>&1 | grep -v \"^llm call failed\" > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/variants_on_bd72d5b.out; cut -c1-260 artifacts/review-evidence/T-202-paralegal-r4/variants_on_973b542.out; echo ======; grep -v \"^\\s*$\" artifacts/review-evidence/T-202-paralegal-r4/variants_on_bd72d5b.out | cut -c1-260",
 "description": "Run new variants on r3 and pre-T-202 builds",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T02:05:34.723Z

**tool result**
````
== synth_sample_er_next_visit all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 16, 2026: $6,240.00 | ER charges: $6,240, next visit date 01/16/2026.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_next_visit counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 16, 2026: $6,240.00 | ER charges: $6,240, next visit date 01/16/2026.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_dotted_leader all_accepted: cents=[215000] refused=[] gate={}
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_dotted_leader counted: cents=[215000] refused=[] gate={}
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_case09_bill_dotted_leader all_accepted: cents=[] refused=[] gate={}
    date violations: []
== synth_case09_bill_dotted_leader counted: cents=[] refused=[] gate={}
    date violations: []
== synth_sample_pcp_er_dos all_accepted: cents=[624000, 15000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Dr. Alvarez, primary care, January 9, 2026: $150.00 | Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pcp_er_dos counted: cents=[624000, 15000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Dr. Alvarez, primary care, January 9, 2026: $150.00 | Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pt_treatment_dates all_accepted: cents=[624000, 166500, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Capital PT, visit 9, January 23–March 6, 2026: $1,665.00 | Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pt_treatment_dates counted: cents=[624000, 166500, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Capital PT, visit 9, January 23–March 6, 2026: $1,665.00 | Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_case09_provider_only_bill all_accepted: cents=[] refused=[] gate={}
    date violations: []
== synth_case09_provider_only_bill counted: cents=[] refused=[] gate={}
    date violations: []
======
== synth_sample_er_next_visit all_accepted: cents=[624000, 215000] refused=[] gate={}
    BILLED CHARGES
    Central ER discharge summary, January 9, 2026: $6,240.00
    Source [Ex. __ / Bates __]: "ER charges: $6,240, next visit date 01/16/2026."
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
    Source [Ex. __ / Bates __]: "Charge: $2,150."
    Billed charges accepted from these records: $8,390.00
== synth_sample_er_dotted_leader all_accepted: cents=[215000] refused=[] gate={}
    BILLED CHARGES
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
    Source [Ex. __ / Bates __]: "Charge: $2,150."
    Billed charges accepted from these records: $2,150.00
== synth_case09_bill_dotted_leader all_accepted: cents=[] refused=[] gate={}
    (no BILLED CHARGES section)
== synth_sample_pcp_er_dos all_accepted: cents=[624000, 15000, 215000] refused=[] gate={}
    BILLED CHARGES
    Central ER discharge summary, January 9, 2026: $6,240.00
    Source [Ex. __ / Bates __]: "ER charges: $6,240."
    Dr. Alvarez, primary care, January 16, 2026: $150.00
    Source [Ex. __ / Bates __]: "Reviewed ER records, DOS 01/09/2026, office visit charge $150.00."
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
    Source [Ex. __ / Bates __]: "Charge: $2,150."
    Billed charges accepted from these records: $8,540.00
== synth_sample_pt_treatment_dates all_accepted: cents=[624000, 166500, 215000] refused=[] gate={}
    BILLED CHARGES
    Central ER discharge summary, January 9, 2026: $6,240.00
    Source [Ex. __ / Bates __]: "ER charges: $6,240."
    Capital PT, visit 9, March 6, 2026: $1,665.00
    Source [Ex. __ / Bates __]: "Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00."
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
    Source [Ex. __ / Bates __]: "Charge: $2,150."
    Billed charges accepted from these records: $10,055.00
== synth_case09_provider_only_bill all_accepted: cents=[] refused=[] gate={}
    (no BILLED CHARGES section)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:05:42.814Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/letters; for f in synth_sample_er_dotted_leader-all_accepted-notes.txt synth_case09_bill_dotted_leader-all_accepted-notes.txt synth_case09_provider_only_bill-all_accepted-notes.txt; do echo \"##### $f\"; grep -n -i -B1 -A3 \"6,240\\|275\" $f | head -30; done",
 "description": "Inspect notes for vanished charges"
}
````

### User / tool · 2026-11-03T02:05:42.910Z

**tool result**
````
##### synth_sample_er_dotted_leader-all_accepted-notes.txt
18-AMOUNTS NOT TOTALED
19:- Record 2 (Central ER discharge summary, January 9, 2026): "$6,240." Amount unclear ($6,240). Request clean copy of bill.
20-- Record 4 (Capital PT, initial evaluation, January 23, 2026): "Charge per visit $185." Rate $185/visit; visit count not stated (12 planned; discharged at visit 9). Request itemized PT ledger.
21-
22-DAMAGES MENTIONS (not charges)
##### synth_case09_bill_dotted_leader-all_accepted-notes.txt
14-AMOUNTS NOT TOTALED
15:- Record 2 (Hobbleton Family Clinic, billing statement, March 1, 2026): "$275.00" Not totaled ($275.00): The line states no date of service, so it is not an itemized service line and is not totaled.
16-
17-DAMAGES MENTIONS (not charges)
18-- none
##### synth_case09_provider_only_bill-all_accepted-notes.txt
14-AMOUNTS NOT TOTALED
15:- Record 2 (Hobbleton Family Clinic, March 1, 2026): "Amount due $275.00 for office visit on 02/02/2026." Not totaled ($275.00): Balance or amount due: worked out from charges, payments and adjustments, not a charge.
16-
17-DAMAGES MENTIONS (not charges)
18-- none
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:06:06.139Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/provider_only_bill.py",
 "content": "\"\"\"T-202 r4 paralegal: SYNTHETIC case_09 variants whose record 2 is the clinic's bill but whose Source line is the provider name only (no record-type word),\nthrough the full case pipeline and letter (evals.letter_check.letters_for), with charge_date_violations. Record 2 keeps Date 2026-03-01 (the statement date).\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/provider_only_bill.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nos.environ.setdefault(\"LLM_BACKEND\", \"fixture\")\nos.environ.setdefault(\"FIXTURE_SET\", \"curated\")\nfrom evals import letter_check as LC  # noqa: E402\n\nC09 = open(\"evals/golden/case_09_nonvisit_hides_gap.txt\").read()\nOLD = 'Date: 2026-03-01\\nSource: Hobbleton Family Clinic, billing statement\\nExcerpt: \"Statement for visit of 2026-02-02: $275.\"'\nassert OLD in C09\nVARIANTS = {\n    \"pa_office_visit_dated\": (\"Hobbleton Family Clinic\", \"Office visit 02/02/2026, 99213, charge $275.00.\"),\n    \"pb_visit_of\": (\"Hobbleton Family Clinic\", \"Office visit 99213 charge $275.00 for the visit of 02/02/2026.\"),\n    \"pc_no_date\": (\"Hobbleton Family Clinic\", \"Office visit 99213, charge $275.00.\"),\n    \"pd_control_billing_statement\": (\"Hobbleton Family Clinic, billing statement\", \"Office visit 02/02/2026, 99213, charge $275.00.\"),\n}\nfor name, (src, ex) in VARIANTS.items():\n    text = C09.replace(OLD, f'Date: 2026-03-01\\nSource: {src}\\nExcerpt: \"{ex}\"')\n    v = LC.letters_for(text)[\"all_accepted\"]\n    letter = v[\"letters\"][\"standard\"]\n    print(f\"== {name}: Source '{src}' / Excerpt '{ex}' / cents={v['charge_cents']}\")\n    for h, q in LC.charge_lines(letter):\n        print(\"   \", h, \"|\", q)\n    print(\"    date violations:\", LC.charge_date_violations(letter, v[\"records\"]))\n    for line in v[\"notes\"].splitlines():\n        if \"275\" in line:\n            print(\"    notes:\", line)\n"
}
````

### User / tool · 2026-11-03T02:06:06.298Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/provider_only_bill.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:06:11.692Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; LLM_BACKEND=fixture FIXTURE_SET=curated .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/provider_only_bill.py $SP/pr4_8cb5bd2 2>&1 | grep -v \"^llm call failed\" > artifacts/review-evidence/T-202-paralegal-r4/provider_only_bill.out; cat artifacts/review-evidence/T-202-paralegal-r4/provider_only_bill.out",
 "description": "Run provider-name-only bill variants",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T02:06:12.751Z

**tool result**
````
== pa_office_visit_dated: Source 'Hobbleton Family Clinic' / Excerpt 'Office visit 02/02/2026, 99213, charge $275.00.' / cents=[27500]
    Hobbleton Family Clinic, March 1, 2026: $275.00 | Office visit 02/02/2026, 99213, charge $275.00.
    date violations: []
== pb_visit_of: Source 'Hobbleton Family Clinic' / Excerpt 'Office visit 99213 charge $275.00 for the visit of 02/02/2026.' / cents=[27500]
    Hobbleton Family Clinic, March 1, 2026: $275.00 | Office visit 99213 charge $275.00 for the visit of 02/02/2026.
    date violations: []
== pc_no_date: Source 'Hobbleton Family Clinic' / Excerpt 'Office visit 99213, charge $275.00.' / cents=[27500]
    Hobbleton Family Clinic, March 1, 2026: $275.00 | Office visit 99213, charge $275.00.
    date violations: []
== pd_control_billing_statement: Source 'Hobbleton Family Clinic, billing statement' / Excerpt 'Office visit 02/02/2026, 99213, charge $275.00.' / cents=[27500]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | Office visit 02/02/2026, 99213, charge $275.00.
    date violations: []
    notes: - Hobbleton Family Clinic, $275.00: The only date near this line (02/02/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:06:22.175Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; LLM_BACKEND=fixture FIXTURE_SET=curated .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/provider_only_bill.py $SP/pr3_973b542 2>&1 | grep -v \"^llm call failed\" > artifacts/review-evidence/T-202-paralegal-r4/provider_only_bill_on_973b542.out; grep -v notes: artifacts/review-evidence/T-202-paralegal-r4/provider_only_bill_on_973b542.out",
 "description": "Run provider-only variants on r3 build",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T02:06:23.673Z

**tool result**
````
== pa_office_visit_dated: Source 'Hobbleton Family Clinic' / Excerpt 'Office visit 02/02/2026, 99213, charge $275.00.' / cents=[27500]
    Hobbleton Family Clinic, March 1, 2026: $275.00 | Office visit 02/02/2026, 99213, charge $275.00.
    date violations: []
== pb_visit_of: Source 'Hobbleton Family Clinic' / Excerpt 'Office visit 99213 charge $275.00 for the visit of 02/02/2026.' / cents=[27500]
    Hobbleton Family Clinic, February 2, 2026: $275.00 | Office visit 99213 charge $275.00 for the visit of 02/02/2026.
    date violations: []
== pc_no_date: Source 'Hobbleton Family Clinic' / Excerpt 'Office visit 99213, charge $275.00.' / cents=[27500]
    Hobbleton Family Clinic, March 1, 2026: $275.00 | Office visit 99213, charge $275.00.
    date violations: []
== pd_control_billing_statement: Source 'Hobbleton Family Clinic, billing statement' / Excerpt 'Office visit 02/02/2026, 99213, charge $275.00.' / cents=[27500]
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | Office visit 02/02/2026, 99213, charge $275.00.
    date violations: []
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:06:27.107Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4; grep -n \"7981\\|r3:\" h.py p01_cases.py",
 "description": "Find port references in helper scripts"
}
````

### User / tool · 2026-11-03T02:06:27.184Z

**tool result**
````
h.py:11:BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7981")  # T-202 r3: 973b542 archive, port 7981
p01_cases.py:9:CASES = os.environ.get("CASES", "sample,case_09,lib14,lib10,lib11").split(",")  # r3: 973b542 archive, port 7981, lib11 added
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:06:29.294Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/h.py",
 "old_string": "\"http://127.0.0.1:7981\")  # T-202 r3: 973b542 archive, port 7981",
 "new_string": "\"http://127.0.0.1:7984\")  # T-202 r4: 8cb5bd2 archive, port 7984"
}
````

### User / tool · 2026-11-03T02:06:29.395Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/h.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:06:30.562Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/p01_cases.py",
 "old_string": "  # r3: 973b542 archive, port 7981, lib11 added",
 "new_string": "  # r4: 8cb5bd2 archive, port 7984"
}
````

### User / tool · 2026-11-03T02:06:30.683Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/p01_cases.py has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:06:33.253Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/h.py artifacts/review-evidence/T-202-paralegal-r4/p01_cases.py > artifacts/review-evidence/T-202-paralegal-r4/p01.out 2>&1; echo exit=$?; grep -E \"draft took|done in|ERRORS|Error|Traceback\" artifacts/review-evidence/T-202-paralegal-r4/p01.out | head -20",
 "description": "Run Playwright walk through five cases",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:07:53.764Z

**tool result**
````
exit=0
[sample] draft took 2.2 s
[sample] done in 15.5 s
[case_09] draft took 2.5 s
[case_09] done in 8.1 s
[lib14] draft took 2.4 s
[lib14] done in 13.1 s
[lib10] draft took 2.4 s
[lib10] done in 19.1 s
[lib11] draft took 2.4 s
[lib11] done in 24.1 s
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:07:56.713Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4; for c in sample case_09 lib14 lib10 lib11; do echo \"## $c: vs r3 letter:\"; cmp ui-$c-letter.txt ../T-202-paralegal-r3/ui-$c-letter.txt && echo identical; cmp ui-$c-notes.txt ../T-202-paralegal-r3/ui-$c-notes.txt && echo notes identical; grep -A1 -E \"^\\S.*\\\\$[0-9,]+\\.[0-9]{2}$\" ui-$c-letter.txt | grep -v \"^--\" ; done",
 "description": "Compare UI letters to r3 and show charge lines"
}
````

### User / tool · 2026-11-03T02:07:56.900Z

**tool result (error)**
````
Exit code 1
## sample: vs r3 letter:
identical
notes identical
/bin/bash: 0-9,: syntax error: operand expected (error token is ",")
## case_09: vs r3 letter:
identical
notes identical
/bin/bash: 0-9,: syntax error: operand expected (error token is ",")
## lib14: vs r3 letter:
identical
notes identical
/bin/bash: 0-9,: syntax error: operand expected (error token is ",")
## lib10: vs r3 letter:
identical
notes identical
/bin/bash: 0-9,: syntax error: operand expected (error token is ",")
## lib11: vs r3 letter:
identical
notes identical
/bin/bash: 0-9,: syntax error: operand expected (error token is ",")
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:07:59.610Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4; for c in sample case_09 lib14 lib10 lib11; do echo \"## $c\"; grep -B1 'Source \\[Ex' ui-$c-letter.txt | grep -v -- \"^--\"; grep -n \"Billed charges\" ui-$c-letter.txt; done; grep -c \"\" ui-sample-letter.txt; head -c 1500 ui-sample-letter.txt",
 "description": "Show charge lines from UI letters"
}
````

### User / tool · 2026-11-03T02:07:59.786Z

**tool result**
````
## sample
Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER.
Source [Ex. __ / Bates __]: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.
Source [Ex. __ / Bates __]: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks."
Cervical range of motion reduced approx. 40%; plan of care 12 visits.
Source [Ex. __ / Bates __]: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits."
Pain 4/10, improving.
Source [Ex. __ / Bates __]: "Pain 4/10, improving."
Discharged from physical therapy after two missed appointments; pain 3/10.
Source [Ex. __ / Bates __]: "Discharged from PT after two missed appointments. Pain 3/10."
New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered.
Source [Ex. __ / Bates __]: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered."
C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically.
Source [Ex. __ / Bates __]: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."
Cervical epidural steroid injection recommended; patient states symptoms began after the January collision.
Source [Ex. __ / Bates __]: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision."
Central ER discharge summary, January 9, 2026: $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240."
Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
Source [Ex. __ / Bates __]: "Charge: $2,150."
46:Billed charges accepted from these records: $8,390.00
## case_09
Left wrist pain 4/10. Splint applied. Return in 2 weeks.
Source [Ex. __ / Bates __]: "Left wrist pain 4/10. Splint applied. Return in 2 weeks."
Patient called to request a work note; work note provided.
Source [Ex. __ / Bates __]: "Patient called to request a work note. Work note provided."
Left wrist pain 3/10. Splint removed.
Source [Ex. __ / Bates __]: "Left wrist pain 3/10. Splint removed."
Pain 1/10. Released from care.
Source [Ex. __ / Bates __]: "Pain 1/10. Released from care."
Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00
Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."
24:Billed charges accepted from these records: $275.00
## lib14
Patient states neck pain 6/10 and tingling in the right hand; cervical collar applied and transported to Orrin Mere Regional ED.
Source [Ex. __ / Bates __]: "Pt states neck pain 6/10 and tingling in the right hand. Cervical collar applied. Transported to Orrin Mere Regional ED."
Diagnosis of cervical strain; cervical spine x-ray negative for fracture; discharged with a muscle relaxant.
Source [Ex. __ / Bates __]: "Dx: cervical strain. X-ray cervical spine negative for fracture. Discharged with a muscle relaxant."
Pain 7 circled on a 0-10 scale; tenderness at C4-C6; adjustment, e-stim and hot pack marked.
Source [Ex. __ / Bates __]: "Pain 7 circled on a 0-10 scale. Tenderness at C4-C6. [X] adjustment [X] e-stim [X] hot pack."
Pain 5 circled; tenderness at C4-C5 improved; adjustment and e-stim boxes marked [X].
Source [Ex. __ / Bates __]: "Pain 5 circled. Tenderness at C4-C5, improved. [X] adjustment [X] e-stim."
Re-examination: pain 6/10, unchanged from the initial visit; plan to continue care three times weekly.
Source [Ex. __ / Bates __]: "Pain 6/10, unchanged from the initial visit. Plan: continue care three times weekly."
Orrin Mere Regional ED, September 14, 2026: $2,960.00
Source [Ex. __ / Bates __]: "ED charge: $2,960."
Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00
Source [Ex. __ / Bates __]: "A0427 ALS emergency transport, 1 unit, charge $1,380.00."
Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $187.05
Source [Ex. __ / Bates __]: "charge $187.05."
32:Billed charges accepted from these records: $4,527.05
## lib10
Driver of a pickup struck at an intersection; patient states chest wall and left knee pain.
Source [Ex. __ / Bates __]: "Pt states chest wall and left knee pain."
Diagnosed with left knee contusion and chest wall contusion; left knee X-ray negative for fracture; admitted for observation.
Source [Ex. __ / Bates __]: "Dx: left knee contusion, chest wall contusion. X-ray left knee negative for fracture. Admitted for observation."
Discharged after 3 days of observation; diagnosis left knee contusion; follow up with orthopedics.
Source [Ex. __ / Bates __]: "Discharged after 3 days of observation. Dx: left knee contusion. Follow up with orthopedics."
UB-04 bill, type of bill 0111, for statement period 06/09/2026 to 06/12/2026: room.
Source [Ex. __ / Bates __]: "UB-04 type of bill 0111, statement period 06/09/2026 to 06/12/2026."
Left knee pain 5/10; MRI of the left knee ordered.
Source [Ex. __ / Bates __]: "Left knee pain 5/10. MRI left knee ordered."
Explanation of benefits, not a bill.
Source [Ex. __ / Bates __]: "Explanation of benefits, processed 07/03/2026, for dates of service 06/09/2026 to 06/12/2026. This is not a bill."
Left knee pain 3/10. Injection performed. Continue home exercises.
Source [Ex. __ / Bates __]: "Left knee pain 3/10. Injection performed. Continue home exercises."
Left knee pain 2/10. Discharged from care.
Source [Ex. __ / Bates __]: "Left knee pain 2/10. Discharged from care."
Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00
Source [Ex. __ / Bates __]: "FL47 total charges $4,920.00."
Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00
Source [Ex. __ / Bates __]: "Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00."
Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $386.50
Source [Ex. __ / Bates __]: "Rev 0250 pharmacy, 14 units, FL47 total charges $386.50."
Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $712.00
Source [Ex. __ / Bates __]: "Rev 0300 laboratory, 6 units, FL47 total charges $712.00."
46:Billed charges accepted from these records: $8,123.50
## lib11
Annual visit; history per patient of car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.
Source [Ex. __ / Bates __]: "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
Patient states neck and low back pain 7/10 after passenger vehicle was struck from behind; ambulatory at scene and transported to Wexcombe Memorial ED.
Source [Ex. __ / Bates __]: "Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED."
Diagnosed with cervical strain and lumbar strain; cervical and lumbar spine X-rays negative for fracture.
Source [Ex. __ / Bates __]: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture."
Law firm letter of protection to Fennimoor Spine Clinic states the firm represents the client for injuries from a collision on 2026-03-18 and asks the clinic to defer collection while the claim is pending.
Source [Ex. __ / Bates __]: "This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending."
Neck pain 7/10 and low back pain 7/10; treating under a letter of protection; plan is chiropractic care three times weekly.
Source [Ex. __ / Bates __]: "Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly."
Intake form: rear ended at red light, neck and back hurt; prior accidents and prior injuries marked No; pain today 7.
Source [Ex. __ / Bates __]: "How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7."
Neck pain 5/10 and low back pain 6/10; manual therapy and exercises continued.
Source [Ex. __ / Bates __]: "Neck pain 5/10, low back pain 6/10. Manual therapy and exercises continued."
Neck pain 4/10, low back pain 5/10. Care continues.
Source [Ex. __ / Bates __]: "Neck pain 4/10, low back pain 5/10. Care continues."
Wexcombe Memorial ED, March 18, 2026: $3,260.00
Source [Ex. __ / Bates __]: "ED charge: $3,260."
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00
Source [Ex. __ / Bates __]: "New patient exam charge $250.00"
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $180.00
Source [Ex. __ / Bates __]: "x-ray charge $180.00"
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $2,310.00
Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"
46:Billed charges accepted from these records: $6,000.00
46
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
Source [Ex. __ / Bates __]: "Discharge
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:13.000Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/eval_teeth_r4.py",
 "content": "\"\"\"T-202 r4 paralegal: evals.letter_check.charge_date_violations on the line the 8cb5bd2 build prints vs the line a paralegal would accept, for the round 4\nwrong-date shapes (SYNTHETIC). Shows whether the independent check catches the wrong line and passes the right one.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/eval_teeth_r4.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom evals import letter_check as LC  # noqa: E402\n\nBL = \"date of service [__________]\"\n\n\ndef letter(head, fig, quote):\n    return f\"BILLED CHARGES\\n\\n{head}: {fig}\\nSource [Ex. __ / Bates __]: \\\"{quote}\\\"\\n\\nBilled charges accepted from these records: {fig}\"\n\n\nCASES = [\n    # name, source, record date, excerpt, quote, figure, build's head, paralegal's heads\n    (\"O1 PCP note, ER DOS in the charge clause\", \"Dr. Alvarez, primary care\", \"2026-01-16\",\n     \"Persistent neck pain 6/10, daily headaches. Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.\",\n     \"Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.\", \"$150.00\",\n     \"Dr. Alvarez, primary care, January 9, 2026\",\n     [\"Dr. Alvarez, primary care, January 16, 2026\", f\"Dr. Alvarez, primary care, {BL} (statement dated January 16, 2026)\"]),\n    (\"R21 PT visit 9, treatment dates in the charge clause\", \"Capital PT, visit 9\", \"2026-03-06\",\n     \"Discharged from PT after two missed appointments. Pain 3/10. Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.\",\n     \"Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.\", \"$1,665.00\",\n     \"Capital PT, visit 9, March 6, 2026\",\n     [\"Capital PT, visit 9, January 23–March 6, 2026\", f\"Capital PT, visit 9, {BL} (statement dated March 6, 2026)\"]),\n    (\"PA provider-name-only bill\", \"Hobbleton Family Clinic\", \"2026-03-01\",\n     \"Office visit 02/02/2026, 99213, charge $275.00.\",\n     \"Office visit 02/02/2026, 99213, charge $275.00.\", \"$275.00\",\n     \"Hobbleton Family Clinic, March 1, 2026\",\n     [f\"Hobbleton Family Clinic, {BL} (statement dated March 1, 2026)\", \"Hobbleton Family Clinic, February 2, 2026\"]),\n]\nfor name, src, rd, ex, q, fig, build, alts in CASES:\n    recs = [{\"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex}]\n    print(f\"== {name}\")\n    print(f\"   build  '{build}: {fig}' -> {LC.charge_date_violations(letter(build, fig, q), recs)}\")\n    for h in alts:\n        print(f\"   alt    '{h}: {fig}' -> {LC.charge_date_violations(letter(h, fig, q), recs)}\")\n"
}
````

### User / tool · 2026-11-03T02:08:13.108Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/eval_teeth_r4.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:17.967Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; LLM_BACKEND=fixture .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/eval_teeth_r4.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2 > artifacts/review-evidence/T-202-paralegal-r4/eval_teeth_r4.out 2>&1; cat artifacts/review-evidence/T-202-paralegal-r4/eval_teeth_r4.out",
 "description": "Run letter_check on wrong and right lines"
}
````

### User / tool · 2026-11-03T02:08:18.160Z

**tool result**
````
== O1 PCP note, ER DOS in the charge clause
   build  'Dr. Alvarez, primary care, January 9, 2026: $150.00' -> []
   alt    'Dr. Alvarez, primary care, January 16, 2026: $150.00' -> ["charge line's date is not certain from its quote (the quote's labeled date of service reads 2026-01-09): Dr. Alvarez, primary care, January 16, 2026: $150.00"]
   alt    'Dr. Alvarez, primary care, date of service [__________] (statement dated January 16, 2026): $150.00' -> ["charge line's date is not certain from its quote (the quote labels one certain date of service and the line prints a blank): Dr. Alvarez, primary care, date of service [__________] (statement dated January 16, 2026): $150.00"]
== R21 PT visit 9, treatment dates in the charge clause
   build  'Capital PT, visit 9, March 6, 2026: $1,665.00' -> []
   alt    'Capital PT, visit 9, January 23–March 6, 2026: $1,665.00' -> ["charge line's date is not certain from its quote (the line prints a date no service label ties to it (the label gives 2026-03-06)): Capital PT, visit 9, January 23–March 6, 2026: $1,665.00"]
   alt    'Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $1,665.00' -> ["charge line's date is not certain from its quote (an encounter record's line must carry the record's own date): Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $1,665.00"]
== PA provider-name-only bill
   build  'Hobbleton Family Clinic, March 1, 2026: $275.00' -> []
   alt    'Hobbleton Family Clinic, date of service [__________] (statement dated March 1, 2026): $275.00' -> ["charge line's date is not certain from its quote (an encounter record's line must carry the record's own date): Hobbleton Family Clinic, date of service [__________] (statement dated March 1, 2026): $275.00"]
   alt    'Hobbleton Family Clinic, February 2, 2026: $275.00' -> ["charge line's date is not certain from its quote (the line prints a date no service label ties to it (the label gives 2026-03-01)): Hobbleton Family Clinic, February 2, 2026: $275.00"]
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:22.812Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4; grep -n -A4 \"^== probe_r3 R15\\|^== probe_r2 N8 \\|^== probe_r2 N20\\|^== probe_r2 N10\\|^== probe_r3c C3\" probe_r4.out | cut -c1-330; grep -n \"fill it from the quote\" ui-lib11-notes.txt | head -3",
 "description": "Check r3 minor probes on r4"
}
````

### User / tool · 2026-11-03T02:08:22.911Z

**tool result**
````
115:== probe_r2 N8 CMS-1500 with per-line item 24A dates  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; kind=bill; billing_document=True)
116-   CMS-1500. Item 24A 06/24/2026 CPT 99204 $185.00. Item 24A 07/08/2026 CPT 20610 $210.00. Item 28 TOTAL CHARGE $395.00.
117-      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=non_service_date
118-              Step 3 note: The only date near this line (06/24/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service
119-      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $210.00'  state=not_stated reason=non_service_date
--
129:== probe_r2 N10 CMS-1500 'from 06/24/2026 to 07/08/2026' (claim span, 2 discrete visits)  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; kind=bill; billing_document=True)
130-   CMS-1500 dates of service from 06/24/2026 to 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.
131-      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, June 24–July 8, 2026: $185.00'  state=stated reason=None
132-      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, June 24–July 8, 2026: $210.00'  state=stated reason=None
133-== probe_r2 N11 CMS-1500 with DOI in the same sentence as a coded line  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; kind=bill; billing_document=True)
--
171:== probe_r2 N20 UB-04 FL6 6-digit from/through  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04'; kind=bill; billing_document=True)
172-   FL6 statement covers period FROM 060926 THROUGH 061226. Rev 0450 emergency room FL47 $2,105.00.
173-    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04, date of service [__________] (statement dated June 19, 2026): $2,105.00'  state=not_stated reason=no_date
174-              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
175-== probe_r2 N21 admit / discharge dates  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04'; kind=bill; billing_document=True)
--
294:== probe_r3 R15 bill: DOS with ordinal ('Feb. 2nd, 2026')  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; kind=bill; billing_document=True)
295-   DOS Feb. 2nd, 2026 office visit charge $275.00.
296-      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=no_date
297-              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
298-== probe_r3 R16 bill: DOS 02/02/2026 and statement date 03/01/2026 in one clause  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; kind=bill; billing_document=True)
--
336:== probe_r3c C3 ER 01/09: charge, then next visit date in its own sentence  (record date 2026-01-09; source 'Central ER discharge summary'; kind=bill; billing_document=False)
337-   ER charges: $6,240. Next visit date 01/16/2026.
338-       $6,240 -> letter head: 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240'  state=not_stated reason=no_date
339-              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
340-== probe_r3c C4 ER 01/09: charge, then next visit date after a comma  (record date 2026-01-09; source 'Central ER discharge summary'; kind=bill; billing_document=False)
39:- Fennimoor Spine Clinic, $250.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
40:- Fennimoor Spine Clinic, $180.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
41:- Fennimoor Spine Clinic, $2,310.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:27.703Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4; grep \"s3 item\" p01.out | cut -c1-260 | head -20",
 "description": "Show Step 3 card text from UI walk"
}
````

### User / tool · 2026-11-03T02:08:27.792Z

**tool result**
````
[sample] s3 item=a1 boxes=[] :: Charge / Central ER discharge summary · January 9, 2026 /  / $6,240.00 /  / Date of service January 9, 2026 /  / Written in the record as $6,240. /  / If you count it, it's added to the bill total in the letter, with the highli
[sample] s3 item=a4 boxes=[] :: Charge / Austin Imaging, cervical MRI · May 29, 2026 /  / $2,150.00 /  / Date of service May 29, 2026 /  / Written in the record as $2,150. /  / If you count it, it's added to the bill total in the letter, with the highlighted 
[sample] s3 item=a2 boxes=[] :: Never counted / Capital PT, initial evaluation · January 23, 2026 /  / $185 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill total.
[sample] s3 item=a3 boxes=[] :: Never counted / Capital PT, visit 8 · February 20, 2026 /  / Not a money amount: missing 3 days of work /  / This figure is not a bill (for example a damages or settlement figure), so it is not added to the total. /  / Either w
[case_09] s3 item=a1 boxes=[] :: Charge / Hobbleton Family Clinic, billing statement · statement dated March 1, 2026 /  / $275.00 /  / Date of service February 2, 2026 · statement dated March 1, 2026 /  / Written in the record as $275. /  / If you count it, 
[lib14] s3 item=a1 boxes=[] :: Charge / Orrin Mere Regional ED · September 14, 2026 /  / $2,960.00 /  / Date of service September 14, 2026 /  / Written in the record as $2,960. /  / If you count it, it's added to the bill total in the letter, with the highlig
[lib14] s3 item=a2 boxes=[] :: Charge / Tarnwick Fire-Rescue, ambulance invoice · statement dated November 12, 2026 /  / $1,380.00 /  / Date of service September 14, 2026 · statement dated November 12, 2026 /  / Written in the record as $1,380.00. /  / If yo
[lib14] s3 item=a4 boxes=[] :: Charge / Tarnwick Fire-Rescue, ambulance invoice · statement dated November 12, 2026 /  / $187.05 /  / Date of service September 14, 2026 · statement dated November 12, 2026 /  / Written in the record as $187.05. /  / If you co
[lib14] s3 item=a3 boxes=[] :: Never counted / Tarnwick Fire-Rescue, ambulance invoice · statement dated November 12, 2026 /  / $21.50 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill to
[lib14] s3 item=a5 boxes=['check-compare'] :: Never counted / Tarnwick Fire-Rescue, ambulance invoice · statement dated November 12, 2026 /  / $1,567.05 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI
[lib10] s3 item=a2 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $4,920.00 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $4,920.00. /  / If yo
[lib10] s3 item=a3 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $2,105.00 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $2,105.00. /  / If yo
[lib10] s3 item=a4 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $386.50 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $386.50. /  / If you co
[lib10] s3 item=a5 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $712.00 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $712.00. /  / If you co
[lib10] s3 item=a1 boxes=[] :: Never counted / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $1,640.00 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the
[lib10] s3 item=a6 boxes=['check-compare'] :: Never counted / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $8,123.50 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A seco
[lib10] s3 item=a7 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · statement dated July 3, 2026 /  / $8,023.50 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A seco
[lib10] s3 item=a8 boxes=[] :: Never counted / Quoinmere Mutual Health Plan, EOB · statement dated July 3, 2026 /  / $3,610.00 /  / Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges. /  / Either way, it is never added
[lib10] s3 item=a9 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · statement dated July 3, 2026 /  / $4,413.50 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A seco
[lib10] s3 item=a10 boxes=[] :: Never counted / Quoinmere Mutual Health Plan, EOB · statement dated July 3, 2026 /  / $3,530.80 /  / Payment: money received, not a charge. /  / Either way, it is never added to the bill total.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:29.715Z

**tool call — Bash**
````
{
 "command": "lsof -iTCP:7984 -sTCP:LISTEN -nP",
 "description": "Find server listener PID"
}
````

### User / tool · 2026-11-03T02:08:29.895Z

**tool result**
````
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  55475 arsis    9u  IPv4 0xb7e00bd867dcffa7      0t0  TCP 127.0.0.1:7984 (LISTEN)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:30.908Z

**tool call — Bash**
````
{
 "command": "kill 55475",
 "description": "Stop the review server"
}
````

### User / tool · 2026-11-03T02:08:30.990Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:32.786Z

**tool call — Bash**
````
{
 "command": "lsof -iTCP:7984 -sTCP:LISTEN -nP; echo lsof_exit=$?; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7984/api/health; ps -p 55475 >/dev/null; echo ps_exit=$?",
 "description": "Confirm server is stopped"
}
````

### User / tool · 2026-11-03T02:08:32.966Z

**tool result**
````
lsof_exit=1
000
ps_exit=1
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:40.007Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2; grep -n \"_NOT_OTHER_VISIT = \\|^_SVC_CORE\\|^_SVC_BILL\\|^def record_kind\\|return \\\"encounter\\\" if\\|if kind != \\\"encounter\\\"\\|if date_iso:  \\|_LBL\\[(bill, ub)\\]\" app/backend/service_date.py; grep -n '\"clinic\"\\|\"encounter\": \\[' app/backend/encounter_types.json; grep -n \"must carry the record's own date\\|want = (rd, None) if (lends and rd)\" evals/letter_check.py; grep -n \"treatment dates\\|Treatment dates\\|R21\\|ER DOS\\|Reviewed ER\" tests/unit/test_t202_r4_encounter.py | head",
 "description": "Get line references for findings"
}
````

### User / tool · 2026-11-03T02:08:40.142Z

**tool result**
````
54:def record_kind(source, excerpt: str = "") -> str:
63:    return "encounter" if (_hit(_ENC, src) or _ABBR.search(src)) else "other"
89:_NOT_OTHER_VISIT = (r"(?<!next )(?<!last )(?<!prior )(?<!previous )(?<!initial )(?<!first )(?<!return )(?<!scheduled )(?<!upcoming )(?<!future )(?<!follow-up )(?<!followup )"
91:_SVC_CORE = _NOT_OTHER_VISIT + r"(?:\bdos|\bdates?(?:\(s\))?\s+of\s+service|\bservice\s+dates?)"        # amendment 2 (b): the only labels in prose
92:_SVC_BILL = (r"\bvisit\s+of|\b(?:services?\s+)?(?:rendered|provided|performed)\s+on|\b(?:the\s+)?run\s+of|\bdate\s+of\s+(?:the\s+)?run|\bservice\s+period|\bperiod\s+of\s+service|"
373:    lbl = _LBL[(bill, ub)]
414:    if kind != "encounter":                                                # a bill, an administrative paper or a record of unknown type never lends its header date
432:    if date_iso:                                                          # a positively identified encounter record (visit, ER, clinic, therapy, imaging, ambulance-run note): its date is the visit
4:  "encounter": [
5:    "visit", "emergency", "urgent care", "clinic", "therapy", "ambulance", "run report", "trip report", "patient care report",
479:                    problems.append("an encounter record's line must carry the record's own date")
489:                want = (rd, None) if (lends and rd) else None
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:43.109Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git rev-parse --short HEAD; git log --oneline -3; ls artifacts/review-evidence/T-202-paralegal-r4/ | grep -v png; ls artifacts/review-evidence/T-202-paralegal-r4/*.png | wc -l; ls artifacts/review-evidence/T-202-paralegal-r4/letters | wc -l; cat artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py | head -30",
 "description": "Confirm HEAD and evidence files"
}
````

### User / tool · 2026-11-03T02:08:43.255Z

**tool result**
````
ad0d91a
ad0d91a fix(qa): T-210 declare the five guided test ids (brand, footer-note, demo-badge, btn-draft, draft-done) in the E2E contract
0281189 chore(guard): subagents stage only into a temp index (shared index kept holding stale reverts, T-201/T-204)
1b3c58a fix(frontend): Step 3 one next-step sentence for every not-certain date reason; confirm box keeps the amount and date line visible at 1280x900 and 1366x768 (T-209 r3)
corpus_kinds.out
corpus_kinds.py
db
diff_r3_r4.out
diff_r3_r4.py
eval_teeth_r4.out
eval_teeth_r4.py
h.py
letter_check.out
letters
letters_dump_r4.out
letters_dump_r4.py
p01.out
p01_cases.py
probe_r4.out
probe_r4.py
probe_r4_on_973b542.out
profile
provider_only_bill.out
provider_only_bill.py
provider_only_bill_on_973b542.out
pytest-t202.out
run.log
server.log
ui-case_09-letter-onscreen.txt
ui-case_09-letter.txt
ui-case_09-notes.txt
ui-lib10-letter-onscreen.txt
ui-lib10-letter.txt
ui-lib10-notes.txt
ui-lib11-letter-onscreen.txt
ui-lib11-letter.txt
ui-lib11-notes.txt
ui-lib14-letter-onscreen.txt
ui-lib14-letter.txt
ui-lib14-notes.txt
ui-sample-letter-onscreen.txt
ui-sample-letter.txt
ui-sample-notes.txt
variants_on_973b542.out
variants_on_bd72d5b.out
      44
      52
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:45.530Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git diff --stat 8cb5bd2 ad0d91a -- app/backend app/llm evals/letter_check.py; echo \"diff_exit=$?\"",
 "description": "Check backend changes since fix commit"
}
````

### User / tool · 2026-11-03T02:08:45.629Z

**tool result**
````
diff_exit=0
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:08:56.148Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2; grep -n \"_NO_DATE_WHY\" app/backend/amounts.py | head; grep -n \"_mask_leaders\\|_LEADER\" app/backend/*.py | head",
 "description": "Locate no-date classification and leader masking"
}
````

### User / tool · 2026-11-03T02:08:56.256Z

**tool result**
````
312:_NO_DATE_WHY = "The line states no date of service, so it is not an itemized service line and is not totaled."
313:NO_DATE_WHY = _NO_DATE_WHY           # T-200: the stored reason of a charge the paralegal counted because its line states no date of service
535:            out["reason"] = _NO_DATE_WHY
663:COUNTABLE_WHY = frozenset({_NO_DATE_WHY, _UNKNOWN_WHY})
app/backend/service_date.py:80:_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(\u00b7]*$"          # a label, then spaces, a colon or a dotted leader (masked to middle dots, `_mask_leaders`), then the date
app/backend/service_date.py:81:_LEADER = re.compile(r"(?:\.[ ]?){3,}|\u2026+")
app/backend/service_date.py:85:def _mask_leaders(text: str) -> str:
app/backend/service_date.py:88:    return _LEADER.sub(lambda m: "\u00b7" * len(m.group(0)), text or "")
app/backend/service_date.py:363:    excerpt = _mask_leaders(excerpt)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:38.058Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md",
 "content": "# T-202 round 4 (final): D-071 amendment 2 — paralegal review (Maria Delgado, senior PI litigation paralegal)\n\n**Verdict: fail.** Round 4 fixes the round 3 blocker as written. The SYNTHETIC sample variant \"ER charges: $6,240, next visit date 01/16/2026.\" now prints `Central ER discharge summary, January 9, 2026: $6,240.00`. Every round 3 other-visit probe (R1, R2, R17, R18, R19, R23, C4, C6, C7) gives the record's date or the blank. Dotted leaders now read correctly in the date resolver. The five corpus letters are right and byte-identical to round 3.\n\nThree shapes still print a wrong date in the date-of-service slot. In each one, `letter_check` passes the wrong line and fails both the correct date and the blank.\n1. **A prior visit's \"DOS\" in a visit note's charge clause.** A PCP note dated January 16 with \"Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.\" prints `Dr. Alvarez, primary care, January 9, 2026: $150.00`. The pre-T-202 build printed January 16. The qualifier list (next/last/prior/...) only catches the words it names; \"ER\", \"seen\", \"eval\", a possessive or a double space all get through.\n2. **A stated treatment period in a visit note.** \"Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.\" in Capital PT visit 9 now prints `March 6, 2026`. Round 3 printed `January 23–March 6, 2026`, so this is a regression. Once a visit note's own date applies, it overrides what the quote says.\n3. **A bill whose Source line is only the provider name.** \"Hobbleton Family Clinic\", dated March 1, with \"Office visit 02/02/2026, 99213, charge $275.00.\" prints `Hobbleton Family Clinic, March 1, 2026: $275.00`. That is the statement date printed as the date of service. encounter_types.json treats \"clinic\", \"imaging\", \"therapy\", \"emergency\" and \"ER\" anywhere in the label as proof of a visit note, so a provider's name is enough. Amendment 2(a) says a record of unknown type never lends its date.\n\n**Dotted leaders.** The brief's text \"Date of service.......01/09/2026\" resolves to January 9 in the resolver (D1–D3, D6, D7), and the T-209 ledger line gives the ambiguous-date blank with the date as written (D4). At the case level, though, the leader line never reaches the resolver. The amount classifier (amounts.py, no leader masking) marks the case_09 bill line \"The line states no date of service\" and does not total it, and it marks the sample ER line \"Amount unclear\". This is pre-existing (same on 973b542 and bd72d5b): major.\n\n**Scope.** `git archive 8cb5bd2` (tree bd2be5e8…) was extracted to the session scratchpad and served in demo mode on 127.0.0.1:7984: fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local; health returned demo_mode true and local_mode true. I stopped listener PID 55475 afterwards (`lsof` exit 1, `curl` 000). For comparison I ran 973b542 (round 3) and bd72d5b (pre-T-202) archives in-process only.\n\nHEAD moved to ad0d91a during the review. `git diff --stat 8cb5bd2 ad0d91a -- app/backend app/llm evals/letter_check.py` is empty, so the findings hold at HEAD.\n\nDemo mode refuses pasted text it has not recorded, so the adversarial variants ran in-process through `evals.letter_check.letters_for`, which is the export path. Private values seen: 1 <redacted> (the author line in `git show` output).\n\n```json\n{\"card\": \"T-202\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"commit 8cb5bd2 (git archive, tree bd2be5e81e5e, extracted to the session scratchpad pr4_8cb5bd2/); served in demo mode (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local; /api/health demo_mode true, local_mode true) at http://127.0.0.1:7984; listener PID 55475 stopped (lsof exit 1, curl 000). Comparison archives (in-process only): 973b542 (round 3) and bd72d5b (pre-T-202). HEAD moved to ad0d91a during the review; git diff --stat 8cb5bd2 ad0d91a -- app/backend app/llm evals/letter_check.py is empty. Cases: sample (sample tile), case_09 (POST /api/cases with the golden text, opened in the UI), lib14, lib10, lib11 (library tile); in-process letters for the same five plus 9 SYNTHETIC variants (the demo refuses unrecorded pastes with 409). Evidence: artifacts/review-evidence/T-202-paralegal-r4/. Private values seen: 1 <redacted>.\",\n \"exercised\": [\n  \"Read personas/paralegal.md, my round 3 review, D-071 amendment 2 and its round 4 note (memory/ORCHESTRATOR_DECISIONS.md:94-95), board.py show T-202 (notes, handoff), git show 8cb5bd2 (encounter_types.json, service_date.py, store.py)\",\n  \"From the archive: pytest test_t202_r4_encounter + test_t202_r3_allow_list + test_t202_r2_service_date_layouts + test_t202_charge_service_dates + test_t200_undated_charge_label: '341 passed in 12.85s' (pytest-t202.out); python -m evals.letter_check: value 0 over 25 cases (letter_check.out)\",\n  \"probe_r4.py: all 82 round 1-3 texts loaded by ast from my r2/r3 probe files (P, T, N, B, R1-R23, C1-C7), plus 33 new round 4 shapes (D1-D12 dotted leaders including the brief's 'Date of service.......01/09/2026'; O1-O10 other-visit DOS labels; S1-S8 provider-name-only bills; T1-T3 totals in visit notes), through store.charge_service_date on 8cb5bd2 (probe_r4.out) and 973b542 (probe_r4_on_973b542.out); diff_r3_r4.out lists 21 changed probes\",\n  \"corpus_kinds.py: record_kind and the printed date for every record with a figure in evals/golden and evals/library (corpus_kinds.out)\",\n  \"letters_dump_r4.py: in-process letters and notes (all_accepted, counted) for sample, case_09, lib14, lib10, lib11 and the SYNTHETIC variants (round 2 ambiguous DOS and CMS-1500 two dates; round 3 ER next visit date; round 4 ER and bill dotted leader, PCP ER DOS, PT treatment dates, provider-only bill) on 8cb5bd2 (letters_dump_r4.out, letters/), and the round 3/4 variants on 973b542 and bd72d5b (variants_on_973b542.out, variants_on_bd72d5b.out)\",\n  \"provider_only_bill.py: four case_09 variants whose record 2 Source is 'Hobbleton Family Clinic' alone, full letter on 8cb5bd2 and 973b542 (provider_only_bill*.out); eval_teeth_r4.py: letter_check on the build's line vs the correct date and the blank (eval_teeth_r4.out)\",\n  \"Playwright on the running archive (h.py + p01_cases.py): sample, case_09, lib14, lib10, lib11 keyboard-first through Steps 1-4, Step 3 cards logged and screenshotted, letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); all ten files cmp-identical to round 3; Step 3 cards show the same date as the letter (p01.out)\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 4, \"letter_dates_correct_on_corpus\": 5, \"adversarial_dates_correct\": 2, \"blank_in_demand_letter\": 4},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"A prior visit's 'DOS' / 'date of service' in a visit note's charge clause prints that visit's date. The qualifier list only catches the words it names. Regression vs pre-T-202, and letter_check enforces the wrong date\",\n   \"evidence\": \"letters_dump_r4.out, synth_sample_pcp_er_dos (Appendix A record 3, PCP note dated 2026-01-16, with 'Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.' appended): 'Dr. Alvarez, primary care, January 9, 2026: $150.00', date violations: []. The same text on bd72d5b printed 'Dr. Alvarez, primary care, January 16, 2026: $150.00' (variants_on_bd72d5b.out). probe_r4.out, other shapes printing the other visit's date: O2 'Last seen DOS 01/09/2026, office visit charge $150.00.' -> January 9; O3 'Follow-up of ER visit date of service 01/09/2026, ...' -> January 9; O4 PT visit 9 (03/06) 'Previous visit's date of service 02/20/2026, discharge visit charge $185.00.' -> February 20; O5 'Initial eval DOS 01/23/2026, ...' -> January 23; O6 'Prior  DOS' (two spaces) -> January 9; O7 'follow up from ER DOS' -> January 9; O10 checkout line 'ER DOS: 01/09/2026   Visit charge: $150.00' -> January 9. Controls that work: O8 (sentence break) and O9 'Previous DOS:' -> January 16. Cause: service_date.py:89 _NOT_OTHER_VISIT is a fixed list of single-space lookbehinds before the label. A labeled date before the record's date passes _plausible, and it wins over the record's own date. eval_teeth_r4.out O1: the build's line gives [], the January 16 line gives 'the quote's labeled date of service reads 2026-01-09', and the blank gives 'the quote labels one certain date of service and the line prints a blank'.\",\n   \"why_it_matters\": \"This is the round 3 blocker class: a label that names a different visit fills the date-of-service slot. A $150 PCP charge dated to the ER visit tells the adjuster the PCP saw the patient on the day of the crash. In a case with a disputed accident date (01/09 vs 01/19), that line will be quoted back. Follow-up notes routinely cite earlier visits by DOS ('ER records DOS 1/9/26 reviewed'). The quote under the line contains 'DOS 01/09/2026', so a quick check against the quote seems to confirm the wrong date. The eval rejects the correct line and the blank, so a fix would be pushed back.\",\n   \"fix\": \"In a visit note (record_kind 'encounter'), a labeled date of service prints only when it equals the record's own date. Any other labeled date gives the fillable blank, with a note naming both dates ('the note is dated January 16; the quote labels 01/09/2026 as a date of service'). A late-entered note whose DOS differs from its header is a real case for the paralegal to settle, not for code. Mirror this in letter_check with its own rule. Bills keep labeled dates as now.\",\n   \"acceptance_test\": \"Unit fixtures O1-O7 and O10 from probe_r4.py print the record's date or the blank, never the other visit's date. The synth_sample_pcp_er_dos letter does not print January 9 on the $150.00 line. letter_check reports a violation on 'Dr. Alvarez, primary care, January 9, 2026: $150.00' for that quote and accepts the blank.\"},\n  {\"severity\": \"blocker\",\n   \"title\": \"A visit note's own date overrides a period the charge clause states: a 9-visit PT charge with 'Treatment dates 01/23/2026 to 03/06/2026' prints the single date March 6 (regression vs round 3, which printed the range)\",\n   \"evidence\": \"letters_dump_r4.out, synth_sample_pt_treatment_dates (Appendix A record 6, Capital PT visit 9, 2026-03-06, with 'Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.' appended): 'Capital PT, visit 9, March 6, 2026: $1,665.00', date violations: []. On 973b542 the same variant printed 'Capital PT, visit 9, January 23–March 6, 2026: $1,665.00' (variants_on_973b542.out); bd72d5b printed March 6 (variants_on_bd72d5b.out). diff_r3_r4.out probe_r3b R21 shows the same change, range -> 'March 6, 2026'. probe_r4.out: T1 'Total for visits 1-9: $1,665.00.' and T2 'PT charges to date $1,665.00.' in the visit 9 note -> 'March 6, 2026'. Cause: amendment 2(b) makes 'treatment dates' a bill-only label (service_date.py:92 _SVC_BILL), so in a visit note the period is not read and the record's date applies at service_date.py:432. eval_teeth_r4.out R21: the build's line gives []; the range gives 'the line prints a date no service label ties to it (the label gives 2026-03-06)'; the blank gives 'an encounter record's line must carry the record's own date' (evals/letter_check.py:479).\",\n   \"why_it_matters\": \"The brief allows a correct service date or the blank. 'March 6, 2026: $1,665.00' reads as one $1,665 visit on the day of a discharge after missed appointments. The quote under it says 9 visits over six weeks. An adjuster will call that inflated specials, and the PT charge is where the sample case's plan-vs-actual dispute already sits. Round 3 got this right.\",\n   \"fix\": \"A visit note lends its own date only when the charge clause holds no other date and no visit count above one ('9 visits', 'visits 1-9', 'to date'). Otherwise print the blank, or the stated period when it is a complete range. Make letter_check accept the blank for an encounter line whose clause has another date or a multi-visit count.\",\n   \"acceptance_test\": \"The synth_sample_pt_treatment_dates letter prints 'January 23–March 6, 2026' or the blank on the $1,665.00 line, never 'March 6, 2026'. T1 and T2 print the blank. letter_check passes those lines and reports a violation on 'Capital PT, visit 9, March 6, 2026: $1,665.00'.\"},\n  {\"severity\": \"blocker\",\n   \"title\": \"A bill whose Source line is only the provider's name ('Hobbleton Family Clinic', 'Austin Imaging', 'Central ER') is read as a visit note, so the statement date prints as the date of service (amendment 2(a) not met; one shape regressed vs round 3)\",\n   \"evidence\": \"provider_only_bill.out (case_09 record 2 kept at Date 2026-03-01, Source 'Hobbleton Family Clinic'): pa 'Office visit 02/02/2026, 99213, charge $275.00.' -> 'Hobbleton Family Clinic, March 1, 2026: $275.00', date violations: []; pb 'Office visit 99213 charge $275.00 for the visit of 02/02/2026.' -> 'Hobbleton Family Clinic, March 1, 2026: $275.00' (973b542 printed 'Hobbleton Family Clinic, February 2, 2026: $275.00', provider_only_bill_on_973b542.out); pc, with no date -> March 1. Control pd with Source '..., billing statement' -> the blank. Resolver-level, probe_r4.out: S2 'Austin Imaging' 06/20 'Patient responsibility $2,150.00 for cervical MRI performed 05/29/2026.' -> June 20; S4 'Central ER' 02/05 '(emergency visit 01/09/2026)' -> February 5; S6 'Gloamwood Chiropractic' -> April 30; S7 'Austin Imaging, cervical MRI' with a bill excerpt -> June 20. Cause: app/backend/encounter_types.json:5 lists 'clinic', 'therapy', 'emergency', 'urgent care', 'imaging', 'chiropractic', 'pain management', 'orthopedic', 'surgery' (and abbreviation 'ER'), and service_date.py:63 matches them anywhere in the source label, which is where provider names carry them. eval_teeth_r4.out PA: the build's line gives []; the blank gives 'an encounter record's line must carry the record's own date'.\",\n   \"why_it_matters\": \"Printing a statement date as if it were the date of service is the error D-071 exists to stop. In 'pa' the letter says March 1 above a quote that says 'Office visit 02/02/2026'. Bills arrive on letterhead and are often logged under the provider's name alone. Almost every provider name in the corpus has one of these words (Family Clinic, Imaging, Physical Therapy, Urgent Care, Regional ED), so the table cannot tell a visit note from a bill by the name. Amendment 2(a) requires positive identification and says unknown types never lend their date.\",\n   \"fix\": \"Identify a visit note by its record-type words, not by its provider name. Match encounter terms only in the part of the Source after the provider name (after the first comma, as in 'Provider, record type'), or require a record-type term ('visit', 'note', 'evaluation', 'discharge summary', 'run report', 'MRI', 'follow-up', 'new patient'). Do not count facility nouns (clinic, imaging, therapy, emergency, ER, urgent care) on their own. A label that is only a provider name is unknown type: blank. Mirror this in letter_check.\",\n   \"acceptance_test\": \"provider_only_bill.py pa, pb and pc print 'Hobbleton Family Clinic, date of service [__________] (statement dated March 1, 2026): $275.00'. S2, S4, S6 and S7 in probe_r4.py give the blank. All 25 corpus letters are unchanged (Quillfeather Urgent Care, Cobblestone Imaging, Thornbury Regional ED and Snickerwood ER either keep their record date through a record-type word or are relabelled in the goldens, stated explicitly). letter_check reports a violation on 'Hobbleton Family Clinic, March 1, 2026: $275.00'.\"},\n  {\"severity\": \"major\",\n   \"title\": \"The dotted-leader fix lives only in the date resolver. At the case level a leader line never reaches it: the bill line is 'not totaled: The line states no date of service' and the ER line is 'Amount unclear' (pre-existing; the T-209 r2 symptom remains on the case path)\",\n   \"evidence\": \"letters/synth_case09_bill_dotted_leader-all_accepted-notes.txt:15 (record 2 'Date of service.......02/02/2026   Office visit 99213 ...... $275.00'): '- Record 2 (Hobbleton Family Clinic, billing statement, March 1, 2026): \\\"$275.00\\\" Not totaled ($275.00): The line states no date of service, so it is not an itemized service line and is not totaled.' Both variants print no Billed Charges line for it (letters_dump_r4.out cents=[]). letters/synth_sample_er_dotted_leader-all_accepted-notes.txt:19 (ER note '... Date of service.......01/09/2026   ER charges ...... $6,240.'): '- Record 2 (Central ER discharge summary, January 9, 2026): \\\"$6,240.\\\" Amount unclear ($6,240). Request clean copy of bill.' The letter's total is $2,150.00. The same results on 973b542 and bd72d5b (variants_on_*.out). The resolver alone gets them right (probe_r4.out D1 -> January 9; D3 -> January 9; D9 -> February 2). service_date.py:85-88 masks leaders, but amounts.py (reason set at :535) does not.\",\n   \"why_it_matters\": \"Itemized bills with dot leaders are common. The notes tell me a bill line with a labeled date of service 'states no date of service', which sends me to request a bill I already have. The sample ER charge falls out of the specials total until I chase it. The figure is listed, not lost, so this is major rather than blocker.\",\n   \"fix\": \"Apply the same leader masking (or a shared helper) in amounts.py before the line is split into segments, so the classifier and the resolver read the same text. Add the two variants as SYNTHETIC golden cases.\",\n   \"acceptance_test\": \"synth_case09_bill_dotted_leader prints 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00' in Billed Charges. synth_sample_er_dotted_leader prints 'Central ER discharge summary, January 9, 2026: $6,240.00' with a total of $8,390.00. Neither note says 'states no date' or 'Amount unclear'.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The excerpt-opening rule turns an ER discharge summary that opens with 'ER charges:' into a bill: the blank says '(statement dated January 9, 2026)' and the note asks for an itemized bill\",\n   \"evidence\": \"probe_r4.out:336-339, C3 (Source 'Central ER discharge summary', 2026-01-09, 'ER charges: $6,240. Next visit date 01/16/2026.'): kind=bill, 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240'. Step 3 note: 'The line states no date of service. ... Request a dated itemized bill'. Round 3 printed January 9 (diff_r3_r4.out). Cause: service_date.py record_kind reads the excerpt opening up to its first colon ('ER charges') as financial.\",\n   \"why_it_matters\": \"This fails safe (a blank, not a wrong date). But 'statement dated' names a document that does not exist, and the note sends me after a bill for a line that is an ER note's own charge.\",\n   \"fix\": \"Let a source label that identifies a record type (discharge summary, run report, visit) outrank the excerpt opening. Use the opening only when the label has no record-type word.\",\n   \"acceptance_test\": \"C3 prints 'Central ER discharge summary, January 9, 2026: $6,240', and no blank on an encounter-labelled record says 'statement dated'.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from round 3: the notes say 'fill it from the quote' for lines whose quote has no date, and one single-date blank covers 'visits 1 through 14'\",\n   \"evidence\": \"ui-lib11-notes.txt:39-41 '- Fennimoor Spine Clinic, $250.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.' (same for $180.00 and $2,310.00). ui-lib11-letter.txt: 'date of service [__________] (statement dated June 15, 2026): $2,310.00' over 'treatment visits 1 through 14 charge $2,310.00'. The handoff lists this as not done.\",\n   \"why_it_matters\": \"There is nothing in a dateless quote to fill from. A 14-visit charge needs a range blank, or I may write in one date and understate the treatment span.\",\n   \"fix\": \"Word the note by reason (no date: take it from the visit notes or request a dated ledger). Print 'dates of service [__________]' when the quote counts visits.\",\n   \"acceptance_test\": \"lib11 counted notes have no 'fill it from the quote' for the three Fennimoor lines, and the $2,310.00 line reads 'dates of service [__________]'.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from round 3: a labeled date of service the code cannot read (ordinal 'Feb. 2nd', CMS-1500 Item 24A, UB-04 FL6 six-digit period) gets a note saying the line states no date or that the date is not labeled\",\n   \"evidence\": \"probe_r4.out R15 'DOS Feb. 2nd, 2026 office visit charge $275.00.' -> reason no_date, 'The line states no date of service.'; N20 'FL6 statement covers period FROM 060926 THROUGH 061226.' -> the same; N8 'Item 24A 06/24/2026 CPT 99204 $185.00.' -> 'The only date near this line (06/24/2026) is not labeled as a date of service (it may be a birth, injury, ...'. The blank prints in all three.\",\n   \"why_it_matters\": \"The letter is safe, but the note is false. It sends me to request a bill I already hold, and calling 24A a possible birth date undercuts trust in every other note.\",\n   \"fix\": \"When a service label is present but its date is not read, quote the label and date as written in the note. Read 24A and FL6 FROM/THROUGH.\",\n   \"acceptance_test\": \"The R15, N20 and N8 notes quote the labeled date as written. None says 'states no date' or 'not labeled'.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from rounds 1-3: some charge quotes name neither the service nor the date the line prints\",\n   \"evidence\": \"ui-lib14-letter.txt 'Source [Ex. __ / Bates __]: \\\"charge $187.05.\\\"'; ui-lib10-letter.txt 'Source [Ex. __ / Bates __]: \\\"FL47 total charges $4,920.00.\\\"'.\",\n   \"why_it_matters\": \"Without opening the record I cannot check the printed September 14 or June 9–12 against the quote under it.\",\n   \"fix\": \"Quote the bill line from its code or description through to the figure.\",\n   \"acceptance_test\": \"Every charge Source line in the 25-case letters contains a service word or code as well as the figure.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Carried: a CMS-1500 claim-level 'dates of service from X to Y' prints the whole span on each coded line\",\n   \"evidence\": \"probe_r4.out N10 'CMS-1500 dates of service from 06/24/2026 to 07/08/2026. CPT 99204 $185.00. CPT 20610 $210.00.' -> 'Wardlaw Orthopedics, CMS-1500, June 24–July 8, 2026' on both lines.\",\n   \"why_it_matters\": \"It is what the bill states, but a new-patient visit shown across two weeks reads oddly to an adjuster.\",\n   \"fix\": \"Optional: on a CMS-1500, a claim span over several coded lines gives the blank with the span quoted in the note.\",\n   \"acceptance_test\": \"N10 lines print the blank; P10 keeps 'January 23–March 6, 2026'.\"}\n ],\n \"whats_right\": [\n  \"Round 3 blocker closed: the ER 'next visit date 01/16/2026' variant prints January 9, and R1, R2, R17-R19, R23, C4, C6 and C7 all give the record's date or the blank\",\n  \"The resolver reads dotted leaders, including the brief's 'Date of service.......01/09/2026' (January 9), the spaced and ellipsis forms, and the T-209 ledger line (ambiguous blank with the date as written)\",\n  \"The sample, case_09, lib14, lib10 and lib11 letters are correct and byte-identical to round 3, and the Step 3 cards show the same date as the letter\"\n ],\n \"questions_for_chris\": [\n  \"Amendment 2(d) fallback: 'every charge line prints the fillable blank unless a DOS column or one of the (b) labels ties exactly one date to it' still prints January 9 on the PCP line in finding 1, because 'DOS 01/09/2026' is a (b) label. Should the fallback also require that, in a non-bill record, a labeled date equal the record's own date (otherwise blank)?\",\n  \"Still open from rounds 2-3, outside T-202: the export gate blocks a SYNTHETIC CMS-1500 coded line ('Line 6 of the letter is a Billed charges line for $150.00 and also states ‘99213 charge’', letters_dump_r4.out synth_cms1500_two_dates). Should this get its own card?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-03T02:10:38.158Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:51.901Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr4_8cb5bd2; sed -n 93p app/backend/service_date.py; grep -n '\"imaging\"\\|\"surgery\"\\|\"encounter_abbreviations\"' app/backend/encounter_types.json; grep -n \"Billed charges\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/letters/synth_sample_er_dotted_leader-all_accepted-letter.txt",
 "description": "Verify line references before writing"
}
````

### User / tool · 2026-11-03T02:10:52.002Z

**tool result**
````
             r"\bdates?\s+of\s+treatment|\btreatment\s+dates?")        # a bill's own wording for what it covers (a statement 'for the visit of', an invoice 'for the run of')
8:    "orthopedic", "orthopedics", "surgery", "surgical", "operative note", "operative report", "op note",
9:    "imaging", "radiology", "mri", "x-ray", "xray", "ct scan", "ultrasound", "chiropractic", "chiropractor", "physical therapy", "telehealth"
11:  "encounter_abbreviations": ["ER", "ED", "EMS", "PT", "OT"],
8:Billed charges accepted from these records: $2,150.00
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:52.772Z

Fixing the three references in the draft.

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:54.118Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md",
 "old_string": "(service_date.py:92 _SVC_BILL)",
 "new_string": "(service_date.py:92-93 _SVC_BILL)"
}
````

### User / tool · 2026-11-03T02:10:54.218Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:55.573Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md",
 "old_string": "Cause: app/backend/encounter_types.json:5 lists",
 "new_string": "Cause: app/backend/encounter_types.json:4-11 lists"
}
````

### User / tool · 2026-11-03T02:10:55.704Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:10:57.455Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md",
 "old_string": "in-process letters for the same five plus 9 SYNTHETIC variants (the demo refuses unrecorded pastes with 409)",
 "new_string": "in-process letters for the same five plus 8 SYNTHETIC variants (letters_dump_r4.py) and 4 provider-name-only bill variants (provider_only_bill.py); the demo refuses unrecorded pastes with 409"
}
````

### User / tool · 2026-11-03T02:10:57.570Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:11:00.774Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md",
 "old_string": "; the demo refuses unrecorded pastes with 409",
 "new_string": "; demo mode refuses unrecorded text (app/backend/api.py:352-353, 409 demo_mode_unsupported_input), so these ran in-process"
}
````

### User / tool · 2026-11-03T02:11:00.874Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:11:02.064Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md",
 "old_string": "Demo mode refuses pasted text it has not recorded, so",
 "new_string": "Demo mode refuses pasted text it has not recorded (api.py:352-353), so"
}
````

### User / tool · 2026-11-03T02:11:02.171Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:11:04.099Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls reviews/T-202-paralegal-r4.md 2>&1; .venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md",
 "description": "Validate draft review JSON"
}
````

### User / tool · 2026-11-03T02:11:04.209Z

**tool result**
````
ls: reviews/T-202-paralegal-r4.md: No such file or directory
json blocks: 1
verdict: fail | severities: ['blocker', 'blocker', 'blocker', 'major', 'minor', 'minor', 'minor', 'minor', 'nit']
verdict rule expects: fail | matches: True
model: claude-opus-5-5 | card: T-202 | persona: paralegal-reviewer
all finding fields present
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:11:06.040Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cp artifacts/review-evidence/T-202-paralegal-r4/draft-T-202-paralegal-r4.md reviews/T-202-paralegal-r4.md && python3 tools/board.py validate reviews/T-202-paralegal-r4.md",
 "description": "Publish review and validate with board"
}
````

### User / tool · 2026-11-03T02:11:06.182Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:11:06.956Z

Now the memory note.

### Assistant · claude-opus-5-5 · 2026-11-03T02:11:15.249Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r4-encounter-patterns.md",
 "content": "---\nname: t202-r4-encounter-patterns\ndescription: T-202 r4 (8cb5bd2) fail: r3 next-visit fixed, but other-visit DOS in visit notes, record date over a stated period (R21 regressed), and provider-name-only bills read as encounters print wrong dates; leader fix resolver-only\nmetadata:\n  type: project\n---\n\nReview file: reviews/T-202-paralegal-r4.md (8cb5bd2, final round). Verdict: fail, with 3 blockers, 1 major, 4 minors and 1 nit.\n\n**Blockers.** In all three, letter_check passes the wrong line and fails both the right date and the blank.\n- **Other-visit DOS in a visit note.** The qualifier lookbehind list (service_date.py:89) is word-bound. These print the other visit's date: \"ER DOS\", \"Last seen DOS\", \"visit's date of service\", \"Initial eval DOS\", a double space, \"follow up\". This is a regression vs bd72d5b.\n- **Record date over a stated period.** An encounter note's record date overrides a stated period: \"Treatment dates X to Y, 9 visits\" prints the end date. r3 printed the range.\n- **Provider name read as an encounter.** encounter_types.json matches clinic/imaging/therapy/ER anywhere in the Source. A bill labelled \"Hobbleton Family Clinic\" prints the statement date. The \"visit of\" variant regressed vs r3.\n\n**Major.** Dotted-leader masking exists only in service_date. amounts.py still marks leader lines \"states no date\" or \"Amount unclear\", and the total drops. This is pre-existing.\n\n**Why:** each allow-list or deny-list moves the risk to a neighbouring shape. Probe each new rule from its opposite side:\n- Labels named after other events.\n- Record type decided by provider name.\n- Stated periods.\n\n**How to apply:**\n- Scripts are in artifacts/review-evidence/T-202-paralegal-r4/. probe_r4.py loads every earlier probe by ast; it handles string constants and PROBES +=.\n- letters_dump_r4.py takes ONLY=<names> and works on older archives.\n- Port 7984, PID 55475.\n\nRelated: [[t202-r3-allow-list-patterns]], [[t202-r2-non-service-date-patterns]].\n"
}
````

### User / tool · 2026-11-03T02:11:15.352Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r4-encounter-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:11:16.964Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-200 undated charge label]",
 "new_string": "- [T-202 r4 encounter patterns](t202-r4-encounter-patterns.md) — 8cb5bd2 fail: other-visit DOS in visit note, record date over stated period, provider-name bill = encounter\n- [T-200 undated charge label]"
}
````

### User / tool · 2026-11-03T02:11:17.074Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:11:20.289Z

T-202 round 4 fails (3 blockers, 1 major): the round 3 next-visit-date error is fixed, but three new text patterns still print a wrong date of service (visit note citing an earlier "DOS 01/09/2026" → January 9; PT "Treatment dates 01/23/2026 to 03/06/2026, 9 visits" → March 6, which round 3 printed as the range; a bill whose Source is only "Hobbleton Family Clinic" → the March 1 statement date), letter_check passes all three wrong lines, the dotted-leader fix doesn't carry through to the full case, the sample/case_09/lib10/lib11/lib14 letters are correct and unchanged from round 3, my server PID 55475 is stopped, one private value is reported as <redacted>, and the review is at /Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r4.md.
