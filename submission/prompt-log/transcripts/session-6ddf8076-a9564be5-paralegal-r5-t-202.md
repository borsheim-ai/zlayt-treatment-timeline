# Subagent: Paralegal r5: T-202 (Paralegal r5: T-202)

Source: `agent-a9564be5c407bf4f6.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T02:43:41.290Z

Review T-202, round 5 (D-073, the conservative fallback), in /Users/arsis/zlayt-pm-project as the senior PI paralegal, starting from a fresh context. The commits are 43b364d and f9c0faf. Read D-073 and its clarification in memory/ORCHESTRATOR_DECISIONS.md, SCOPE_CUTS row 28, reviews/T-202-paralegal-r4.md, and the handoff with its corpus diff (22 lines become blanks).

Run a `git archive f9c0faf` copy in demo mode on your own port, and stop your PID afterward.
- Re-run every adversarial text from rounds 1 to 4.
- The bar is never a wrong date: every line prints either a correct date or the fillable blank.
- Generate the sample, case_09, lib10, lib11 and lib14 letters.
- Judge whether a letter with many blanks is still usable for a demand.

Report any private value only as <redacted>. Write reviews/T-202-paralegal-r5.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-opus-5-5 · 2026-11-03T02:43:44.222Z

**tool call — Bash**
````
{
 "command": "cat personas/paralegal.md | head -5 && wc -l personas/paralegal.md && ls .claude/agent-memory/paralegal-reviewer/ && cat .claude/agent-memory/paralegal-reviewer/t202-*.md .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md .claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md",
 "description": "Read persona header and relevant memory files"
}
````

### User / tool · 2026-11-03T02:43:44.314Z

**tool result**
````
# Persona dossier — paralegal-reviewer

## 1. Identity
**Maria Delgado (fictional), Senior Litigation Paralegal, plaintiff personal-injury firm in Austin, Texas — 9+ years, pre-lit and litigation.**
She has built hundreds of medical chronologies and demand packages in Filevine; her attorney signs the demand, but she is the one the attorney blames when an adjuster finds a date that doesn't match the records. She reviews rather than trusts: anything she cannot click back to the source page does not go in the demand.
      84 personas/paralegal.md
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
t202-r4-encounter-patterns.md
t209-confirm-sentence-patterns.md
t209-r3-patterns.md
t209-r4-patterns.md
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
name: t202-r4-encounter-patterns
description: T-202 r4 (8cb5bd2) fail: r3 next-visit fixed, but other-visit DOS in visit notes, record date over a stated period (R21 regressed), and provider-name-only bills read as encounters print wrong dates; leader fix resolver-only
metadata:
  type: project
---

Review file: reviews/T-202-paralegal-r4.md (8cb5bd2, final round). Verdict: fail, with 3 blockers, 1 major, 4 minors and 1 nit.

**Blockers.** In all three, letter_check passes the wrong line and fails both the right date and the blank.
- **Other-visit DOS in a visit note.** The qualifier lookbehind list (service_date.py:89) is word-bound. These print the other visit's date: "ER DOS", "Last seen DOS", "visit's date of service", "Initial eval DOS", a double space, "follow up". This is a regression vs bd72d5b.
- **Record date over a stated period.** An encounter note's record date overrides a stated period: "Treatment dates X to Y, 9 visits" prints the end date. r3 printed the range.
- **Provider name read as an encounter.** encounter_types.json matches clinic/imaging/therapy/ER anywhere in the Source. A bill labelled "Hobbleton Family Clinic" prints the statement date. The "visit of" variant regressed vs r3.

**Major.** Dotted-leader masking exists only in service_date. amounts.py still marks leader lines "states no date" or "Amount unclear", and the total drops. This is pre-existing.

**Why:** each allow-list or deny-list moves the risk to a neighbouring shape. Probe each new rule from its opposite side:
- Labels named after other events.
- Record type decided by provider name.
- Stated periods.

**How to apply:**
- Scripts are in artifacts/review-evidence/T-202-paralegal-r4/. probe_r4.py loads every earlier probe by ast; it handles string constants and PROBES +=.
- letters_dump_r4.py takes ONLY=<names> and works on older archives.
- Port 7984, PID 55475.

Related: [[t202-r3-allow-list-patterns]], [[t202-r2-non-service-date-patterns]].
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

### Assistant · claude-opus-5-5 · 2026-11-03T02:43:46.375Z

**tool call — Bash**
````
{
 "command": "sed -n 5,84p personas/paralegal.md | head -30; grep -n \"D-073\" -A40 memory/ORCHESTRATOR_DECISIONS.md | head -90",
 "description": "Read persona rest and D-073 decision"
}
````

### User / tool · 2026-11-03T02:43:46.469Z

**tool result**
````
She has built hundreds of medical chronologies and demand packages in Filevine; her attorney signs the demand, but she is the one the attorney blames when an adjuster finds a date that doesn't match the records. She reviews rather than trusts: anything she cannot click back to the source page does not go in the demand.

## 2. Day-to-day context
- Tools: case-management system (Filevine/Clio-style), a PDF viewer with Bates stamps, Word templates for the demand, Excel for specials, Outlook for records requests.
- Volume: several demand packages a week; records arrive piecemeal from EMS, ER, PCP, PT, imaging, pain management, often with duplicates and copy-forward notes.
- Pressures: Stowers/time-limited demands with deadlines; attorneys who want the demand out today; adjusters who cross-check every claim against the records.
- A bad day: the adjuster's response letter quotes a record she summarized wrong, or points to a gap or prior injury she missed. The firm's credibility on that file — and her attorney's trust in her — drops.

## 3. Goals and success criteria for this artifact
- A chronology she can verify line by line, fast: date of service, provider/facility, short summary in the provider's own words, and the exact excerpt with its record reference.
- The tool surfaces what the adjuster will attack (gaps, prior conditions, conflicts, missed appointments, hedged causation) before the demand goes out, so the attorney decides how to handle it.
- Billed charges she can reconcile: every amount with its source, a total of explicit charges only, and unclear amounts called out rather than guessed.
- An export she can paste into the treatment section of the demand letter with minimal reformatting, containing only what she accepted.

## 4. Review checklist
1. Every date in the timeline appears verbatim (or as an unambiguous reformat) in its source record; nothing is dated by when a note was entered rather than the date of service.
2. Every entry shows provider and facility as written in the record (e.g., "Capital PT", "Dr. Alvarez, primary care"), not a guessed full name.
3. Every entry's excerpt is a verbatim quote from that record, and I can see which record (# / source / date) it came from in one action.
4. The one-line summary uses the provider's own clinical words (e.g., "cervical strain; concussion without loss of consciousness") and adds nothing that is not in the excerpt.
5. Entries are in date-of-service order; same-day records (EMS and ER on 2026-01-09) are both present and not merged.
6. The 73-day gap (2026-03-06 PT discharge → 2026-05-18 pain management) is flagged with both dates and the day count; the 28-day interval (01-23 → 02-20) is not flagged.
7. The accident-date conflict is flagged: 2026-01-09 (EMS/ER) vs "Date of accident per intake form: 2026-01-19" (record 7), with both excerpts; the tool does not pick one.
8. The PT plan vs actual discrepancy is surfaced: "Plan of care: 12 visits" vs "Discharged from PT after two missed appointments" at visit 9.
9. Prior-condition mentions are flagged: "low back pain in 2023, resolved" (record 3) and "may represent degenerative change" (record 8), each with its excerpt.
10. PT discharge notes that mention missed appointments raise a `causation` flag (D-013).
11. Charges list shows $6,240 (ER) and $2,150 (MRI) with sources, and the running total of explicit charges is $8,390.
12. The running total excludes per-visit rates unless the visit count is stated: "$185 per visit" appears as "rate — visit count not stated (12 planned; discharged at visit 9) — needs review", not as a computed PT total; in the export that reason sits in the internal review notes, never in the letter (R-EX-4).
13. "Missing 3 days of work" is not listed as a billed charge (it may be noted as a lost-wages mention).
14. Every entry and every flag has accept, edit, and dismiss; edits keep the original visible somewhere so I can see what I changed.
15. I can review with the keyboard (move to next item, accept, dismiss) without reaching for the mouse on every row.
97:## D-073 — Service dates: the pre-declared conservative fallback (§7.4 after T-202 r4)
98-Four rounds of date recognition kept finding new prose patterns that print a wrong date of service (r4: a visit note citing an earlier "DOS", a therapy "Treatment dates A to B" range collapsing to B, an unknown source lending its statement date). Binding for the MVP: a charge line prints a service date from exactly two sources, (1) the date cell of its own row in a bill table whose column header names the date of service (or the CMS-1500 24A/UB-04 from-through period, printed as a range), or (2) the encounter record's own date when the charge sits inside a positively identified encounter record (encounter_types.json). Prose labels are no longer read for charge dates at all; every other line prints the fillable blank "date of service [__________] (statement dated X)" with the Step 3 confirm note. letter_check applies the same two-source rule independently. Wider date recognition is SCOPE_CUTS row 28. Expected effect: some corpus lines that printed a correct prose-labelled date now print the blank, which is honest and is shown in the handoff diff.
99:- D-073 clarification (staff r4 question, decided per rule 1): an encounter record is identified only by a document-type word (visit/progress/office note, ED/ER record, discharge summary, PT/therapy note, ambulance run report, operative report); a provider name (clinic, ED, orthopedics, urgent care, imaging) is never enough. About 19 of 84 corpus charge lines then print the fillable blank; accepted.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:43:47.760Z

**tool call — Bash**
````
{
 "command": "git log --oneline -6 && git show --stat 43b364d f9c0faf | head -60 && grep -n \"^| *28 \" memory/SCOPE_CUTS.md; grep -n \"28\" memory/SCOPE_CUTS.md | head -5; python3 tools/board.py show T-202 | tail -60",
 "description": "Check commits, scope cut, card handoff"
}
````

### User / tool · 2026-11-03T02:43:47.959Z

**tool result**
````
f9c0faf test(e2e): T-202 r5 D-073 case_09 and lib11 ED lines show the fillable blank, not a prose-read date
43b364d feat(backend): T-202 r5 D-073 charge dates from two sources only; prose labels removed; leader mask in amounts; T-207 r2 rule pins
ad0d91a fix(qa): T-210 declare the five guided test ids (brand, footer-note, demo-badge, btn-draft, draft-done) in the E2E contract
0281189 chore(guard): subagents stage only into a temp index (shared index kept holding stale reverts, T-201/T-204)
1b3c58a fix(frontend): Step 3 one next-step sentence for every not-certain date reason; confirm box keeps the amount and date line visible at 1280x900 and 1366x768 (T-209 r3)
efda639 docs(architect): LLM_VS_CODE rows 2-3 match T-202 r4 code (T-207)
commit 43b364d022c64db6b65554a877e0fae4c036add5
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 20:33:00 2026 -0600

    feat(backend): T-202 r5 D-073 charge dates from two sources only; prose labels removed; leader mask in amounts; T-207 r2 rule pins
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 .claude/agent-memory/backend/MEMORY.md             |   6 +
 .../agent-memory/backend/project_t202_r5_d073.md   |  18 +
 app/backend/amounts.py                             |  25 +-
 app/backend/encounter_types.json                   |  13 +-
 app/backend/service_date.py                        | 227 ++++------
 app/backend/store.py                               |  14 +-
 evals/letter_check.py                              | 152 ++++---
 memory/contracts/api.md                            |   2 +-
 tests/unit/test_t200_undated_charge_label.py       |   8 +-
 tests/unit/test_t202_charge_service_dates.py       |  19 +-
 tests/unit/test_t202_r2_service_date_layouts.py    |  69 +--
 tests/unit/test_t202_r3_allow_list.py              |  99 +++--
 tests/unit/test_t202_r4_encounter.py               | 117 ++---
 tests/unit/test_t202_r5_d073.py                    | 470 +++++++++++++++++++++
 14 files changed, 897 insertions(+), 342 deletions(-)

commit f9c0faf12067d4e56fd50d9968558f701d8bee1c
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 20:39:52 2026 -0600

    test(e2e): T-202 r5 D-073 case_09 and lib11 ED lines show the fillable blank, not a prose-read date
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 tests/e2e/guided/test_t205.py | 17 ++++++++---------
 tests/e2e/guided/test_t206.py |  6 +++---
 2 files changed, 11 insertions(+), 12 deletions(-)
113:| 28 | Service-date recognition from prose (D-073) | Charge lines take a date only from a DOS table cell/period or the encounter record's own date; prose like "visit of", "Treatment dates A to B", "DOS" inside a note is not read, so those lines print the fillable blank for the paralegal to fill. Four review rounds showed prose recognition fails open on new patterns. | A labelled-span parser with an adversarial corpus and a paralegal-built test set; ~2-3 days. | post-MVP |
26:| debt | T-014 accepted with documented debt after 3 rounds (§7.4) | 5 consistency majors, 0 blockers after 3 rounds; split to T-028 which T-017 depends on | see card | M1 |
33:| debt | T-028 accepted with documented debt after 2 rounds (§7.4) | remaining major (golden export byte test) is T-041 AC2 and T-038 spec-vs-golden check; minors (README-arch v1 names, confirm_date warning) carried to M2 backend cards | see card | M1 |
78:| debt | T-112 accepted with documented debt after 3 rounds (§7.4) | 3 rounds; the D-054 trimmer is vocabulary-bound, so it misses some abbreviations (fresh probes: 12/43 faithful pairs over-trimmed to the tray, 9/30 unsupported clauses kept). Both directions are safe: over-trim is visible in the tray and the human recovers it; kept clauses still face judge 1 and the human. On 188 recorded outputs the trim never fires on English. | Fragments and surviving mutants: T-128. Full coverage would need an LLM-free clinical abbreviation resource; ~1-2 days. | M3 (T-128) |
79:| debt | T-112 accepted with documented debt after 3 rounds (§7.4) | memory/SCOPE_CUTS.md T-112 row; follow-up T-128 | see card | M2 |
113:| 28 | Service-date recognition from prose (D-073) | Charge lines take a date only from a DOS table cell/period or the encounter record's own date; prose like "visit of", "Treatment dates A to B", "DOS" inside a note is not read, so those lines print the fillable blank for the paralegal to fill. Four review rounds showed prose recognition fails open on new patterns. | A labelled-span parser with an adversarial corpus and a paralegal-built test set; ~2-3 days. | post-MVP |
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
- 2026-11-03T02:11:36Z orchestrator: review paralegal-reviewer (claude-opus-5-5): fail — reviews/T-202-paralegal-r4.md; round 4; findings:
    - [blocker] A prior visit's 'DOS' / 'date of service' in a visit note's charge clause prints that visit's date. The qualifier list only catches the words it names. Regression vs pre-T-202, and letter_check enforces the wrong date — fix: In a visit note (record_kind 'encounter'), a labeled date of service prints only when it equals the record's own date. Any other labeled date gives the fillabl
    - [blocker] A visit note's own date overrides a period the charge clause states: a 9-visit PT charge with 'Treatment dates 01/23/2026 to 03/06/2026' prints the single date March 6 (regression vs round 3, which printed the range) — fix: A visit note lends its own date only when the charge clause holds no other date and no visit count above one ('9 visits', 'visits 1-9', 'to date'). Otherwise pr
    - [blocker] A bill whose Source line is only the provider's name ('Hobbleton Family Clinic', 'Austin Imaging', 'Central ER') is read as a visit note, so the statement date prints as the date of service (amendment 2(a) not met; one shape regressed vs round 3) — fix: Identify a visit note by its record-type words, not by its provider name. Match encounter terms only in the part of the Source aft
    - [major] The dotted-leader fix lives only in the date resolver. At the case level a leader line never reaches it: the bill line is 'not totaled: The line states no date of service' and the ER line is 'Amount unclear' (pre-existing; the T-209 r2 symptom remains on the case path) — fix: Apply the same leader masking (or a shared helper) in amounts.py before the line is split into segments, so t
    - [minor] The excerpt-opening rule turns an ER discharge summary that opens with 'ER charges:' into a bill: the blank says '(statement dated January 9, 2026)' and the note asks for an itemized bill — fix: Let a source label that identifies a record type (discharge summary, run report, visit) outrank the excerpt opening. Use the opening only when the label has no record-type word.
    - [minor] Carried from round 3: the notes say 'fill it from the quote' for lines whose quote has no date, and one single-date blank covers 'visits 1 through 14' — fix: Word the note by reason (no date: take it from the visit notes or request a dated ledger). Print 'dates of service [__________]' when the quote counts visits.
    - [minor] Carried from round 3: a labeled date of service the code cannot read (ordinal 'Feb. 2nd', CMS-1500 Item 24A, UB-04 FL6 six-digit period) gets a note saying the line states no date or that the date is not labeled — fix: When a service label is present but its date is not read, quote the label and date as written in the note. Read 24A and FL6 FROM/THROUGH.
    - [minor] Carried from rounds 1-3: some charge quotes name neither the service nor the date the line prints — fix: Quote the bill line from its code or description through to the figure.
- 2026-11-03T02:11:36Z orchestrator: assigned: backend
- 2026-11-03T02:11:36Z orchestrator: Round 5 = implement D-073 (the pre-declared conservative fallback) once the staff r4 review lands; fold staff r4 findings that still apply.
- 2026-11-03T02:13:25Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-202-staff-engineer-r4b.md
- 2026-11-03T02:13:25Z backend: moved changes_requested -> in_progress
- 2026-11-03T02:27:40Z backend: r5 (D-073) in progress: service_date.py rewritten to two sources (DOS-column cell incl. 24A From/To + UB-04 span; encounter record's own date by document-type word, no other date/visit count in the sentence); prose labels removed; encounter_types.json now document-type words only; letter_check scanner rewritten; amounts.py masks dotted leaders (T-209 r2 full-run). Corpus diff: 22 of 37 distinct accepted charge lines turn to the blank (19 provider-only ED/Urgent Care/Imaging/radiology + case_09 'visit of' + lib14 two 'run of'); lib10 UB-04 period kept. Mutant run + git-archive verification next.
- 2026-11-03T02:43:29Z backend: AC 1 checked: r5 (D-073) 43b364d + f9c0faf from git archive: unit 6662 passed 12 skipped 0 failed (4 shards); guided e2e 156 passed; python -m evals.letter_check value 0 over 25 cases; tests/unit/test_t202_r5_d073.py 382 tests (every probe of both reviewers, all rounds); 52 mutants killed (list in handoff)
- 2026-11-03T02:43:29Z backend: moved in_progress -> in_review
- 2026-11-03T02:43:37Z orchestrator: review dispatched: paralegal-reviewer, staff-engineer-reviewer

## Handoff
What changed (r5, D-073, 43b364d + f9c0faf): a charge date comes from only (1) its own row's date cell under a DOS-type heading in a bill table (24A From/To pair = range, UB-04 'statement covers period' span for a coded line) or (2) the record's own date when the source label has a DOCUMENT-TYPE word (encounter_types.json now lists only those; no provider/specialty words, no abbreviations) AND the figure's own sentence holds no other date and no visit count. Prose labels, guard words and the bill-wording list are deleted; letter_check has a rewritten own scanner on the same two sources. amounts.py masks dotted leaders (carries through a full case run: ER leader line is totaled and dated Jan 9, case_09 leader bill totaled with the blank). T-207 r2: unlocated figure now prints the blank (F3).
Corpus letter diff vs HEAD ad0d91a (84-line charge dump, 37 accepted lines): 22 lines turn to the blank, same 22 in the counted variant, 10 blanks before and 54 after in the 84-line dump. 19 = provider/specialty-only labels (Thornbury Regional ED x2, Quillfeather Urgent Care, Dr. Hobart Wimbleton radiology, Thornapple Valley ED, Bumblethorpe Urgent Care, Marrowgate ED, Tamsin Valley Urgent Care, Redhaven ED, Harlow Memorial ED, Coldharbor ED, Larchmont Ridge ED, Cobblestone Imaging, Quillmere ED, Wexcombe ED, Orrin Vale ED, Vessel Grove ED, Orrin Mere ED, Cobblewood Urgent Care: header date was the record's); 3 = prose-read bill dates (case_09 'Statement for visit of', lib14 two 'run of' invoice lines). lib10 UB-04 period and the sample ER/MRI lines unchanged. 
Verified from git archive: unit 6662 passed 12 skipped 0 failed; guided e2e 156 passed (2 qa e2e tests, test_t205 case_09 and test_t206 lib11 ED, edited to expect the blank); letter_check value 0 over 25 cases. Tests: test_t202_r5_d073.py 382 tests; older t200/t202 files re-based (prose rows now assert the blank, DOS-cell/table rows kept; flagged qa-owned edits). Mutants killed (all fail the unit suite or letter_check): M1-M3 M5-M9 encounter/UB/From-To/leader rules, M10-M12 leader mask, M13 plausibility, M14 feasible-any, M15 header combine, M16 clinic and M17 ED as encounter words, M18-M22; L1-L11 check mutants; T-207 r2 pins: B1 365-day years, B2 strict > lower edge, B3/B4 4 and 6 years, B5 strict < record date, B6 no-date refuses, R1 rule-2 strict <, R3 different-order period ends read, H3 Encounter Date and H4 Date of Visit headings, N1 counted charge gets a note, F3 unlocated encounter lends date, C1-C4 check bounds, M4 heading check dropped, M21 one-cell table. The old guard-word mutants cannot exist: the prose label code is gone.
What's left / judgment calls: (1) I did NOT implement 'excerpt-opening vs source label' outranking (paralegal r4 minor): an ER summary whose excerpt opens 'ER charges:' is still a bill and prints the blank (safe direction). (2) Paralegal minors not done: 'dates of service [____]' for multi-visit lines, quoting the bill line from code through figure, six-digit FL6 dates. (3) 'follow-up', 'new patient', 'mri', 'exam' count as document-type words (corpus labels like 'Dr. X, orthopedics, follow-up'); one line in the JSON to drop. (4) encounter lend requires every date in the figure's own sentence to equal the record date. (5) architect text for LLM_VS_CODE rows 2-3 is on T-207. What surprised me: 22 not 19 lines move because three prose-dated bill lines (case_09, lib14 x2) also blank, and a leader line needs both a mask in amounts.py and a trailing-dot strip in _label before 'ER charges' is read as a charge label.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:43:50.120Z

**tool call — Bash**
````
{
 "command": "sed -n 1,80p reviews/T-202-paralegal-r4.md; ls artifacts/review-evidence/T-202-paralegal-r4/ artifacts/review-evidence/T-202-paralegal-r3/ artifacts/review-evidence/T-202-paralegal-r2/ artifacts/review-evidence/T-202-paralegal/",
 "description": "Read r4 review and list probe scripts"
}
````

### User / tool · 2026-11-03T02:43:50.222Z

**tool result**
````
# T-202 round 4 (final): D-071 amendment 2 — paralegal review (Maria Delgado, senior PI litigation paralegal)

**Verdict: fail.** Round 4 fixes the round 3 blocker as written. The SYNTHETIC sample variant "ER charges: $6,240, next visit date 01/16/2026." now prints `Central ER discharge summary, January 9, 2026: $6,240.00`. Every round 3 other-visit probe (R1, R2, R17, R18, R19, R23, C4, C6, C7) gives the record's date or the blank. Dotted leaders now read correctly in the date resolver. The five corpus letters are right and byte-identical to round 3.

Three shapes still print a wrong date in the date-of-service slot. In each one, `letter_check` passes the wrong line and fails both the correct date and the blank.
1. **A prior visit's "DOS" in a visit note's charge clause.** A PCP note dated January 16 with "Reviewed ER records, DOS 01/09/2026, office visit charge $150.00." prints `Dr. Alvarez, primary care, January 9, 2026: $150.00`. The pre-T-202 build printed January 16. The qualifier list (next/last/prior/...) only catches the words it names; "ER", "seen", "eval", a possessive or a double space all get through.
2. **A stated treatment period in a visit note.** "Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00." in Capital PT visit 9 now prints `March 6, 2026`. Round 3 printed `January 23–March 6, 2026`, so this is a regression. Once a visit note's own date applies, it overrides what the quote says.
3. **A bill whose Source line is only the provider name.** "Hobbleton Family Clinic", dated March 1, with "Office visit 02/02/2026, 99213, charge $275.00." prints `Hobbleton Family Clinic, March 1, 2026: $275.00`. That is the statement date printed as the date of service. encounter_types.json treats "clinic", "imaging", "therapy", "emergency" and "ER" anywhere in the label as proof of a visit note, so a provider's name is enough. Amendment 2(a) says a record of unknown type never lends its date.

**Dotted leaders.** The brief's text "Date of service.......01/09/2026" resolves to January 9 in the resolver (D1–D3, D6, D7), and the T-209 ledger line gives the ambiguous-date blank with the date as written (D4). At the case level, though, the leader line never reaches the resolver. The amount classifier (amounts.py, no leader masking) marks the case_09 bill line "The line states no date of service" and does not total it, and it marks the sample ER line "Amount unclear". This is pre-existing (same on 973b542 and bd72d5b): major.

**Scope.** `git archive 8cb5bd2` (tree bd2be5e8…) was extracted to the session scratchpad and served in demo mode on 127.0.0.1:7984: fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local; health returned demo_mode true and local_mode true. I stopped listener PID 55475 afterwards (`lsof` exit 1, `curl` 000). For comparison I ran 973b542 (round 3) and bd72d5b (pre-T-202) archives in-process only.

HEAD moved to ad0d91a during the review. `git diff --stat 8cb5bd2 ad0d91a -- app/backend app/llm evals/letter_check.py` is empty, so the findings hold at HEAD.

Demo mode refuses pasted text it has not recorded (api.py:352-353), so the adversarial variants ran in-process through `evals.letter_check.letters_for`, which is the export path. Private values seen: 1 <redacted> (the author line in `git show` output).

```json
{"card": "T-202", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 8cb5bd2 (git archive, tree bd2be5e81e5e, extracted to the session scratchpad pr4_8cb5bd2/); served in demo mode (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local; /api/health demo_mode true, local_mode true) at http://127.0.0.1:7984; listener PID 55475 stopped (lsof exit 1, curl 000). Comparison archives (in-process only): 973b542 (round 3) and bd72d5b (pre-T-202). HEAD moved to ad0d91a during the review; git diff --stat 8cb5bd2 ad0d91a -- app/backend app/llm evals/letter_check.py is empty. Cases: sample (sample tile), case_09 (POST /api/cases with the golden text, opened in the UI), lib14, lib10, lib11 (library tile); in-process letters for the same five plus 8 SYNTHETIC variants (letters_dump_r4.py) and 4 provider-name-only bill variants (provider_only_bill.py); demo mode refuses unrecorded text (app/backend/api.py:352-353, 409 demo_mode_unsupported_input), so these ran in-process. Evidence: artifacts/review-evidence/T-202-paralegal-r4/. Private values seen: 1 <redacted>.",
 "exercised": [
  "Read personas/paralegal.md, my round 3 review, D-071 amendment 2 and its round 4 note (memory/ORCHESTRATOR_DECISIONS.md:94-95), board.py show T-202 (notes, handoff), git show 8cb5bd2 (encounter_types.json, service_date.py, store.py)",
  "From the archive: pytest test_t202_r4_encounter + test_t202_r3_allow_list + test_t202_r2_service_date_layouts + test_t202_charge_service_dates + test_t200_undated_charge_label: '341 passed in 12.85s' (pytest-t202.out); python -m evals.letter_check: value 0 over 25 cases (letter_check.out)",
  "probe_r4.py: all 82 round 1-3 texts loaded by ast from my r2/r3 probe files (P, T, N, B, R1-R23, C1-C7), plus 33 new round 4 shapes (D1-D12 dotted leaders including the brief's 'Date of service.......01/09/2026'; O1-O10 other-visit DOS labels; S1-S8 provider-name-only bills; T1-T3 totals in visit notes), through store.charge_service_date on 8cb5bd2 (probe_r4.out) and 973b542 (probe_r4_on_973b542.out); diff_r3_r4.out lists 21 changed probes",
  "corpus_kinds.py: record_kind and the printed date for every record with a figure in evals/golden and evals/library (corpus_kinds.out)",
  "letters_dump_r4.py: in-process letters and notes (all_accepted, counted) for sample, case_09, lib14, lib10, lib11 and the SYNTHETIC variants (round 2 ambiguous DOS and CMS-1500 two dates; round 3 ER next visit date; round 4 ER and bill dotted leader, PCP ER DOS, PT treatment dates, provider-only bill) on 8cb5bd2 (letters_dump_r4.out, letters/), and the round 3/4 variants on 973b542 and bd72d5b (variants_on_973b542.out, variants_on_bd72d5b.out)",
  "provider_only_bill.py: four case_09 variants whose record 2 Source is 'Hobbleton Family Clinic' alone, full letter on 8cb5bd2 and 973b542 (provider_only_bill*.out); eval_teeth_r4.py: letter_check on the build's line vs the correct date and the blank (eval_teeth_r4.out)",
  "Playwright on the running archive (h.py + p01_cases.py): sample, case_09, lib14, lib10, lib11 keyboard-first through Steps 1-4, Step 3 cards logged and screenshotted, letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt); all ten files cmp-identical to round 3; Step 3 cards show the same date as the letter (p01.out)"
 ],
 "verdict": "fail",
 "scores": {"verify_quickly": 4, "letter_dates_correct_on_corpus": 5, "adversarial_dates_correct": 2, "blank_in_demand_letter": 4},
 "findings": [
  {"severity": "blocker",
   "title": "A prior visit's 'DOS' / 'date of service' in a visit note's charge clause prints that visit's date. The qualifier list only catches the words it names. Regression vs pre-T-202, and letter_check enforces the wrong date",
   "evidence": "letters_dump_r4.out, synth_sample_pcp_er_dos (Appendix A record 3, PCP note dated 2026-01-16, with 'Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.' appended): 'Dr. Alvarez, primary care, January 9, 2026: $150.00', date violations: []. The same text on bd72d5b printed 'Dr. Alvarez, primary care, January 16, 2026: $150.00' (variants_on_bd72d5b.out). probe_r4.out, other shapes printing the other visit's date: O2 'Last seen DOS 01/09/2026, office visit charge $150.00.' -> January 9; O3 'Follow-up of ER visit date of service 01/09/2026, ...' -> January 9; O4 PT visit 9 (03/06) 'Previous visit's date of service 02/20/2026, discharge visit charge $185.00.' -> February 20; O5 'Initial eval DOS 01/23/2026, ...' -> January 23; O6 'Prior  DOS' (two spaces) -> January 9; O7 'follow up from ER DOS' -> January 9; O10 checkout line 'ER DOS: 01/09/2026   Visit charge: $150.00' -> January 9. Controls that work: O8 (sentence break) and O9 'Previous DOS:' -> January 16. Cause: service_date.py:89 _NOT_OTHER_VISIT is a fixed list of single-space lookbehinds before the label. A labeled date before the record's date passes _plausible, and it wins over the record's own date. eval_teeth_r4.out O1: the build's line gives [], the January 16 line gives 'the quote's labeled date of service reads 2026-01-09', and the blank gives 'the quote labels one certain date of service and the line prints a blank'.",
   "why_it_matters": "This is the round 3 blocker class: a label that names a different visit fills the date-of-service slot. A $150 PCP charge dated to the ER visit tells the adjuster the PCP saw the patient on the day of the crash. In a case with a disputed accident date (01/09 vs 01/19), that line will be quoted back. Follow-up notes routinely cite earlier visits by DOS ('ER records DOS 1/9/26 reviewed'). The quote under the line contains 'DOS 01/09/2026', so a quick check against the quote seems to confirm the wrong date. The eval rejects the correct line and the blank, so a fix would be pushed back.",
   "fix": "In a visit note (record_kind 'encounter'), a labeled date of service prints only when it equals the record's own date. Any other labeled date gives the fillable blank, with a note naming both dates ('the note is dated January 16; the quote labels 01/09/2026 as a date of service'). A late-entered note whose DOS differs from its header is a real case for the paralegal to settle, not for code. Mirror this in letter_check with its own rule. Bills keep labeled dates as now.",
   "acceptance_test": "Unit fixtures O1-O7 and O10 from probe_r4.py print the record's date or the blank, never the other visit's date. The synth_sample_pcp_er_dos letter does not print January 9 on the $150.00 line. letter_check reports a violation on 'Dr. Alvarez, primary care, January 9, 2026: $150.00' for that quote and accepts the blank."},
  {"severity": "blocker",
   "title": "A visit note's own date overrides a period the charge clause states: a 9-visit PT charge with 'Treatment dates 01/23/2026 to 03/06/2026' prints the single date March 6 (regression vs round 3, which printed the range)",
   "evidence": "letters_dump_r4.out, synth_sample_pt_treatment_dates (Appendix A record 6, Capital PT visit 9, 2026-03-06, with 'Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.' appended): 'Capital PT, visit 9, March 6, 2026: $1,665.00', date violations: []. On 973b542 the same variant printed 'Capital PT, visit 9, January 23–March 6, 2026: $1,665.00' (variants_on_973b542.out); bd72d5b printed March 6 (variants_on_bd72d5b.out). diff_r3_r4.out probe_r3b R21 shows the same change, range -> 'March 6, 2026'. probe_r4.out: T1 'Total for visits 1-9: $1,665.00.' and T2 'PT charges to date $1,665.00.' in the visit 9 note -> 'March 6, 2026'. Cause: amendment 2(b) makes 'treatment dates' a bill-only label (service_date.py:92-93 _SVC_BILL), so in a visit note the period is not read and the record's date applies at service_date.py:432. eval_teeth_r4.out R21: the build's line gives []; the range gives 'the line prints a date no service label ties to it (the label gives 2026-03-06)'; the blank gives 'an encounter record's line must carry the record's own date' (evals/letter_check.py:479).",
   "why_it_matters": "The brief allows a correct service date or the blank. 'March 6, 2026: $1,665.00' reads as one $1,665 visit on the day of a discharge after missed appointments. The quote under it says 9 visits over six weeks. An adjuster will call that inflated specials, and the PT charge is where the sample case's plan-vs-actual dispute already sits. Round 3 got this right.",
   "fix": "A visit note lends its own date only when the charge clause holds no other date and no visit count above one ('9 visits', 'visits 1-9', 'to date'). Otherwise print the blank, or the stated period when it is a complete range. Make letter_check accept the blank for an encounter line whose clause has another date or a multi-visit count.",
   "acceptance_test": "The synth_sample_pt_treatment_dates letter prints 'January 23–March 6, 2026' or the blank on the $1,665.00 line, never 'March 6, 2026'. T1 and T2 print the blank. letter_check passes those lines and reports a violation on 'Capital PT, visit 9, March 6, 2026: $1,665.00'."},
  {"severity": "blocker",
   "title": "A bill whose Source line is only the provider's name ('Hobbleton Family Clinic', 'Austin Imaging', 'Central ER') is read as a visit note, so the statement date prints as the date of service (amendment 2(a) not met; one shape regressed vs round 3)",
   "evidence": "provider_only_bill.out (case_09 record 2 kept at Date 2026-03-01, Source 'Hobbleton Family Clinic'): pa 'Office visit 02/02/2026, 99213, charge $275.00.' -> 'Hobbleton Family Clinic, March 1, 2026: $275.00', date violations: []; pb 'Office visit 99213 charge $275.00 for the visit of 02/02/2026.' -> 'Hobbleton Family Clinic, March 1, 2026: $275.00' (973b542 printed 'Hobbleton Family Clinic, February 2, 2026: $275.00', provider_only_bill_on_973b542.out); pc, with no date -> March 1. Control pd with Source '..., billing statement' -> the blank. Resolver-level, probe_r4.out: S2 'Austin Imaging' 06/20 'Patient responsibility $2,150.00 for cervical MRI performed 05/29/2026.' -> June 20; S4 'Central ER' 02/05 '(emergency visit 01/09/2026)' -> February 5; S6 'Gloamwood Chiropractic' -> April 30; S7 'Austin Imaging, cervical MRI' with a bill excerpt -> June 20. Cause: app/backend/encounter_types.json:4-11 lists 'clinic', 'therapy', 'emergency', 'urgent care', 'imaging', 'chiropractic', 'pain management', 'orthopedic', 'surgery' (and abbreviation 'ER'), and service_date.py:63 matches them anywhere in the source label, which is where provider names carry them. eval_teeth_r4.out PA: the build's line gives []; the blank gives 'an encounter record's line must carry the record's own date'.",
   "why_it_matters": "Printing a statement date as if it were the date of service is the error D-071 exists to stop. In 'pa' the letter says March 1 above a quote that says 'Office visit 02/02/2026'. Bills arrive on letterhead and are often logged under the provider's name alone. Almost every provider name in the corpus has one of these words (Family Clinic, Imaging, Physical Therapy, Urgent Care, Regional ED), so the table cannot tell a visit note from a bill by the name. Amendment 2(a) requires positive identification and says unknown types never lend their date.",
   "fix": "Identify a visit note by its record-type words, not by its provider name. Match encounter terms only in the part of the Source after the provider name (after the first comma, as in 'Provider, record type'), or require a record-type term ('visit', 'note', 'evaluation', 'discharge summary', 'run report', 'MRI', 'follow-up', 'new patient'). Do not count facility nouns (clinic, imaging, therapy, emergency, ER, urgent care) on their own. A label that is only a provider name is unknown type: blank. Mirror this in letter_check.",
   "acceptance_test": "provider_only_bill.py pa, pb and pc print 'Hobbleton Family Clinic, date of service [__________] (statement dated March 1, 2026): $275.00'. S2, S4, S6 and S7 in probe_r4.py give the blank. All 25 corpus letters are unchanged (Quillfeather Urgent Care, Cobblestone Imaging, Thornbury Regional ED and Snickerwood ER either keep their record date through a record-type word or are relabelled in the goldens, stated explicitly). letter_check reports a violation on 'Hobbleton Family Clinic, March 1, 2026: $275.00'."},
  {"severity": "major",
   "title": "The dotted-leader fix lives only in the date resolver. At the case level a leader line never reaches it: the bill line is 'not totaled: The line states no date of service' and the ER line is 'Amount unclear' (pre-existing; the T-209 r2 symptom remains on the case path)",
   "evidence": "letters/synth_case09_bill_dotted_leader-all_accepted-notes.txt:15 (record 2 'Date of service.......02/02/2026   Office visit 99213 ...... $275.00'): '- Record 2 (Hobbleton Family Clinic, billing statement, March 1, 2026): \"$275.00\" Not totaled ($275.00): The line states no date of service, so it is not an itemized service line and is not totaled.' Both variants print no Billed Charges line for it (letters_dump_r4.out cents=[]). letters/synth_sample_er_dotted_leader-all_accepted-notes.txt:19 (ER note '... Date of service.......01/09/2026   ER charges ...... $6,240.'): '- Record 2 (Central ER discharge summary, January 9, 2026): \"$6,240.\" Amount unclear ($6,240). Request clean copy of bill.' The letter's total is $2,150.00. The same results on 973b542 and bd72d5b (variants_on_*.out). The resolver alone gets them right (probe_r4.out D1 -> January 9; D3 -> January 9; D9 -> February 2). service_date.py:85-88 masks leaders, but amounts.py (reason set at :535) does not.",
   "why_it_matters": "Itemized bills with dot leaders are common. The notes tell me a bill line with a labeled date of service 'states no date of service', which sends me to request a bill I already have. The sample ER charge falls out of the specials total until I chase it. The figure is listed, not lost, so this is major rather than blocker.",
   "fix": "Apply the same leader masking (or a shared helper) in amounts.py before the line is split into segments, so the classifier and the resolver read the same text. Add the two variants as SYNTHETIC golden cases.",
   "acceptance_test": "synth_case09_bill_dotted_leader prints 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00' in Billed Charges. synth_sample_er_dotted_leader prints 'Central ER discharge summary, January 9, 2026: $6,240.00' with a total of $8,390.00. Neither note says 'states no date' or 'Amount unclear'."},
  {"severity": "minor",
   "title": "The excerpt-opening rule turns an ER discharge summary that opens with 'ER charges:' into a bill: the blank says '(statement dated January 9, 2026)' and the note asks for an itemized bill",
   "evidence": "probe_r4.out:336-339, C3 (Source 'Central ER discharge summary', 2026-01-09, 'ER charges: $6,240. Next visit date 01/16/2026.'): kind=bill, 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240'. Step 3 note: 'The line states no date of service. ... Request a dated itemized bill'. Round 3 printed January 9 (diff_r3_r4.out). Cause: service_date.py record_kind reads the excerpt opening up to its first colon ('ER charges') as financial.",
   "why_it_matters": "This fails safe (a blank, not a wrong date). But 'statement dated' names a document that does not exist, and the note sends me after a bill for a line that is an ER note's own charge.",
   "fix": "Let a source label that identifies a record type (discharge summary, run report, visit) outrank the excerpt opening. Use the opening only when the label has no record-type word.",
   "acceptance_test": "C3 prints 'Central ER discharge summary, January 9, 2026: $6,240', and no blank on an encounter-labelled record says 'statement dated'."},
  {"severity": "minor",
   "title": "Carried from round 3: the notes say 'fill it from the quote' for lines whose quote has no date, and one single-date blank covers 'visits 1 through 14'",
   "evidence": "ui-lib11-notes.txt:39-41 '- Fennimoor Spine Clinic, $250.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.' (same for $180.00 and $2,310.00). ui-lib11-letter.txt: 'date of service [__________] (statement dated June 15, 2026): $2,310.00' over 'treatment visits 1 through 14 charge $2,310.00'. The handoff lists this as not done.",
   "why_it_matters": "There is nothing in a dateless quote to fill from. A 14-visit charge needs a range blank, or I may write in one date and understate the treatment span.",
   "fix": "Word the note by reason (no date: take it from the visit notes or request a dated ledger). Print 'dates of service [__________]' when the quote counts visits.",
   "acceptance_test": "lib11 counted notes have no 'fill it from the quote' for the three Fennimoor lines, and the $2,310.00 line reads 'dates of service [__________]'."},
  {"severity": "minor",
   "title": "Carried from round 3: a labeled date of service the code cannot read (ordinal 'Feb. 2nd', CMS-1500 Item 24A, UB-04 FL6 six-digit period) gets a note saying the line states no date or that the date is not labeled",
   "evidence": "probe_r4.out R15 'DOS Feb. 2nd, 2026 office visit charge $275.00.' -> reason no_date, 'The line states no date of service.'; N20 'FL6 statement covers period FROM 060926 THROUGH 061226.' -> the same; N8 'Item 24A 06/24/2026 CPT 99204 $185.00.' -> 'The only date near this line (06/24/2026) is not labeled as a date of service (it may be a birth, injury, ...'. The blank prints in all three.",
   "why_it_matters": "The letter is safe, but the note is false. It sends me to request a bill I already hold, and calling 24A a possible birth date undercuts trust in every other note.",
   "fix": "When a service label is present but its date is not read, quote the label and date as written in the note. Read 24A and FL6 FROM/THROUGH.",
   "acceptance_test": "The R15, N20 and N8 notes quote the labeled date as written. None says 'states no date' or 'not labeled'."},
  {"severity": "minor",
   "title": "Carried from rounds 1-3: some charge quotes name neither the service nor the date the line prints",
   "evidence": "ui-lib14-letter.txt 'Source [Ex. __ / Bates __]: \"charge $187.05.\"'; ui-lib10-letter.txt 'Source [Ex. __ / Bates __]: \"FL47 total charges $4,920.00.\"'.",
   "why_it_matters": "Without opening the record I cannot check the printed September 14 or June 9–12 against the quote under it.",
   "fix": "Quote the bill line from its code or description through to the figure.",
   "acceptance_test": "Every charge Source line in the 25-case letters contains a service word or code as well as the figure."},
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
probe_r3.py
probe_r3b.out
probe_r3b.py
probe_r3c.out
probe_r3c.py
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
ui-lib11-letter-onscreen.txt
ui-lib11-letter.txt
ui-lib11-notes.txt
ui-lib14-letter-onscreen.txt
ui-lib14-letter.txt
ui-lib14-notes.txt
ui-sample-letter-onscreen.txt
ui-sample-letter.txt
ui-sample-notes.txt

artifacts/review-evidence/T-202-paralegal-r4/:
case_09-s3-00-a1.png
case_09-step2-done.png
case_09-step3-done.png
case_09-step4.png
corpus_kinds.out
corpus_kinds.py
db
diff_r3_r4.out
diff_r3_r4.py
draft-T-202-paralegal-r4.md
eval_teeth_r4.out
eval_teeth_r4.py
h.py
letter_check.out
letters
letters_dump_r4.out
letters_dump_r4.py
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
probe_r4.out
probe_r4.py
probe_r4_on_973b542.out
profile
provider_only_bill.out
provider_only_bill.py
provider_only_bill_on_973b542.out
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

### Assistant · claude-opus-5-5 · 2026-11-03T02:43:52.662Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4 && wc -l *.py && cat probe_r4.py | head -150",
 "description": "Inspect r4 probe scripts"
}
````

### User / tool · 2026-11-03T02:43:52.751Z

**tool result**
````
      33 corpus_kinds.py
      32 diff_r3_r4.py
      43 eval_teeth_r4.py
      58 h.py
      76 letters_dump_r4.py
     126 p01_cases.py
     139 probe_r4.py
      34 provider_only_bill.py
     541 total
"""T-202 r4 paralegal probe: every SYNTHETIC charge text from rounds 1-3 (r2 probe_r2.py P/T/N, probe_r2b.py B; r3 probe_r3.py R1-R16, probe_r3b.py R1/R2/R17-R23,
probe_r3c.py C1-C7), loaded from those files by ast (string constants + PROBES lists), plus round 4 shapes (dotted leaders, other-visit DOS labels the
qualifier list does not name, provider-name sources on bills, totals in encounter notes), through the shipped path store.charge_service_date
(the call Step 3 and the letter share). Prints the letter head as export builds it: f"{src}, {text}: {raw}".
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/probe_r4.py <archive_root> <repo_root>
"""
import ast
import os
import sys

root = os.path.abspath(sys.argv[1])
repo = os.path.abspath(sys.argv[2])
sys.path.insert(0, root)
os.chdir(root)
from app.backend import amounts as AM, store  # noqa: E402

try:
    from app.backend import service_date as SD  # noqa: E402
    KIND = getattr(SD, "record_kind", None)
except Exception:
    KIND = None


def load(path):
    tree = ast.parse(open(path).read())
    ns, out = {}, []
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    ns[t.id] = node.value.value
        tgt = node.targets[0] if isinstance(node, ast.Assign) else (node.target if isinstance(node, ast.AugAssign) else None)
        if getattr(tgt, "id", "") == "PROBES" and isinstance(node.value, ast.List):
            out += eval(compile(ast.Expression(node.value), path, "eval"), {}, ns)
    if not out:
        raise SystemExit(f"no PROBES in {path}")
    return out


ev = os.path.join(repo, "artifacts/review-evidence")
OLD = []
for f in ("T-202-paralegal-r2/probe_r2.py", "T-202-paralegal-r2/probe_r2b.py", "T-202-paralegal-r3/probe_r3.py",
          "T-202-paralegal-r3/probe_r3b.py", "T-202-paralegal-r3/probe_r3c.py"):
    got = load(os.path.join(ev, f))
    print(f"# loaded {len(got)} probes from {f}")
    OLD += [(f.split("/")[1].replace(".py", "") + " " + p[0],) + tuple(p[1:]) for p in got]

V = "Dr. Alvarez, primary care"
ER = "Central ER discharge summary"
PTD = "Capital PT, visit 9"
ERB = "Central ER, itemized bill"
L = "Fennimoor Spine Clinic, itemized ledger"
NEW = [
    # dotted leaders (T-209 r2 major; brief)
    ("D1 ER bill: 'Date of service.......01/09/2026' then leadered charge", ERB, "2026-02-05",
     "Date of service.......01/09/2026   ER facility charge ........ $6,240.00"),
    ("D2 ER note: 'Date of service.......01/09/2026' (brief text) then ER charges", ER, "2026-01-09",
     "Date of service.......01/09/2026. Dx: cervical strain. ER charges: $6,240."),
    ("D3 ER note: leader DOS then charge in same clause", ER, "2026-01-09",
     "Date of service.......01/09/2026   ER charges ...... $6,240"),
    ("D4 ledger (T-209): DOS 04/05/2026 Office visit 99213 ... $250.00", L, "2026-06-15",
     "Fennimoor Spine Clinic itemized ledger. DOS 04/05/2026 Office visit 99213 ... $250.00"),
    ("D5 bill: DOI leader then DOS leader then charge leader", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Date of injury.......01/09/2026   Date of service.......02/02/2026   99213 office visit ...... $275.00"),
    ("D6 bill: spaced-dot leader", ERB, "2026-02-05",
     "Date of service . . . . . 01/09/2026   ER facility charge . . . . . $6,240.00"),
    ("D7 bill: unicode ellipsis leader", ERB, "2026-02-05",
     "Date of service……01/09/2026   ER facility charge……$6,240.00"),
    ("D8 bill: statement date leader only, then leadered charge (expect blank)", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Statement date.......03/01/2026   Office visit 99213.......$275.00"),
    ("D9 bill: statement date leader + DOS leader + charge", "Hobbleton Family Clinic, billing statement", "2026-03-01",
     "Statement date.......03/01/2026   Date of service.......02/02/2026   Office visit 99213.......$275.00"),
    ("D10 bill: next-visit leader after charge (expect blank or none)", ERB, "2026-02-05",
     "ER facility charge.......$6,240.00   Next date of service.......01/30/2026"),
    ("D11 ER note: 'Next visit date.......01/16/2026' then ER charges (expect Jan 9)", ER, "2026-01-09",
     "Next visit date.......01/16/2026   ER charges ...... $6,240"),
    ("D12 PCP note: 'Last date of service.......01/09/2026' then office charge (expect Jan 16)", V, "2026-01-16",
     "Last date of service.......01/09/2026   Office visit charge ...... $150.00"),
    # other-visit DOS labels whose qualifier is not in the lookbehind list (prior visit, so before the note: plausible)
    ("O1 PCP 01/16: 'Reviewed ER records, DOS 01/09/2026, office visit charge'", V, "2026-01-16",
     "Reviewed ER records, DOS 01/09/2026, office visit charge $150.00."),
    ("O2 PCP 01/16: 'Last seen DOS 01/09/2026' (seen, not last, before DOS)", V, "2026-01-16",
     "Last seen DOS 01/09/2026, office visit charge $150.00."),
    ("O3 PCP 01/16: 'ER visit date of service 01/09/2026'", V, "2026-01-16",
     "Follow-up of ER visit date of service 01/09/2026, office visit charge $150.00."),
    ("O4 PT visit 9 03/06: 'Previous visit's date of service 02/20/2026'", PTD, "2026-03-06",
     "Previous visit's date of service 02/20/2026, discharge visit charge $185.00."),
    ("O5 PT visit 9 03/06: 'Initial eval DOS 01/23/2026'", PTD, "2026-03-06",
     "Initial eval DOS 01/23/2026, discharge visit charge $185.00."),
    ("O6 PCP 01/16: 'Prior  DOS 01/09/2026' (two spaces)", V, "2026-01-16",
     "Prior  DOS 01/09/2026, office visit charge $150.00."),
    ("O7 PCP 01/16: 'Follow up DOS' (no hyphen) prior date", V, "2026-01-16",
     "Seen for follow up from ER DOS 01/09/2026, office visit charge $150.00."),
    ("O8 PCP 01/16: ER DOS in its own sentence (control: sentence break)", V, "2026-01-16",
     "Reviewed ER records, DOS 01/09/2026. Office visit charge $150.00."),
    ("O9 PCP 01/16: 'Previous DOS: 01/09/2026' (listed qualifier, control)", V, "2026-01-16",
     "Previous DOS: 01/09/2026, office visit charge $150.00."),
    ("O10 PCP 01/16: checkout line 'ER DOS: 01/09/2026   Visit charge: $150.00'", V, "2026-01-16",
     "ER DOS: 01/09/2026   Visit charge: $150.00"),
    # bills whose source label is only a provider name (contains clinic / imaging / therapy / ER) and whose opening has no financial word
    ("S1 'Hobbleton Family Clinic' 03/01: Amount due ... office visit on 02/02/2026", "Hobbleton Family Clinic", "2026-03-01",
     "Amount due $275.00 for office visit on 02/02/2026."),
    ("S2 'Austin Imaging' 06/20: Patient responsibility ... MRI performed 05/29/2026", "Austin Imaging", "2026-06-20",
     "Patient responsibility $2,150.00 for cervical MRI performed 05/29/2026."),
    ("S3 'Capital Physical Therapy' 03/20: Total due for 9 visits", "Capital Physical Therapy", "2026-03-20",
     "Total due $1,665.00 for 9 visits."),
    ("S4 'Central ER' 02/05: Amount owed (emergency visit 01/09/2026)", "Central ER", "2026-02-05",
     "Amount owed: $6,240.00 (emergency visit 01/09/2026)."),
    ("S5 'Hill Country Pain Management' 07/01: thank-you then balance", "Hill Country Pain Management", "2026-07-01",
     "Thank you for your visit. Your balance is $450.00."),
    ("S6 'Gloamwood Chiropractic' 04/30: Please remit for treatment 03/02/2026-04/10/2026", "Gloamwood Chiropractic", "2026-04-30",
     "Please remit $1,200.00 for treatment 03/02/2026 to 04/10/2026."),
    ("S7 'Austin Imaging, cervical MRI' 06/20 (encounter label) but the excerpt is the bill", "Austin Imaging, cervical MRI", "2026-06-20",
     "Amount due $2,150.00. Thank you for choosing Austin Imaging."),
    ("S8 'Hobbleton Family Clinic' 03/01 control: opening with 'Statement' (expect blank)", "Hobbleton Family Clinic", "2026-03-01",
     "Statement: amount due $275.00 for office visit on 02/02/2026."),
    # totals for several visits inside an encounter note
    ("T1 PT visit 9 03/06: total for visits 1-9 in the discharge note", PTD, "2026-03-06",
     "Discharged from PT after two missed appointments. Total for visits 1-9: $1,665.00."),
    ("T2 PT visit 9 03/06: PT charges to date", PTD, "2026-03-06",
     "Discharged from PT after two missed appointments. PT charges to date $1,665.00."),
    ("T3 ER note 01/10 (summary written next day): arrived 01/09/2026", "Central ER discharge summary", "2026-01-10",
     "Arrived 01/09/2026 by EMS. Discharged 01/10/2026. ER charges: $6,240."),
]

for label, src, rd, ex in OLD + NEW:
    kind = KIND(src, ex) if KIND else "n/a"
    print(f"== {label}  (record date {rd}; source '{src}'; kind={kind}; billing_document={AM.billing_document(src, ex)})")
    print("   " + ex.replace("\n", "\n   "))
    rec = {"id": "r1", "n": 1, "source": src, "date_iso": rd, "excerpt": ex, "text": ex}
    for a in AM.find_amounts(ex):
        if a.get("cents") is None:
            continue
        item = {"excerpt": ex, "value_cents": a["cents"], "raw": a["raw"], "excerpt_start": 0}
        d = store.charge_service_date(item, rec, a["start"])
        print(f"   {a['raw']:>10} -> letter head: '{src}, {d['text']}: {a['raw']}'  state={d['state']} reason={d['reason']}")
        if d.get("confirm_note"):
            print(f"              Step 3 note: {d['confirm_note']}")
print(f"# total probes: {len(OLD)} old + {len(NEW)} new")
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:44:12.028Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git show f9c0faf:app/backend/encounter_types.json && git show f9c0faf:app/backend/service_date.py | head -200",
 "description": "Read encounter_types.json and service_date.py at f9c0faf"
}
````

### User / tool · 2026-11-03T02:44:12.160Z

**tool result**
````
f9c0faf
{
  "_doc": "D-073 (T-202 round 5; supersedes the D-071 amendment 2 table). The ONE declared table of record types for charge-line dates. A record's own date can stand as a charge line's date of service ONLY when the record is positively identified by a DOCUMENT-TYPE word in its source label (visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, ambulance run report, operative report, evaluation, consult ...). A provider's name or specialty (clinic, ED, urgent care, imaging, orthopedics, therapy, EMS, primary care) is never enough. Read by app/backend/service_date.py (production) and by evals/letter_check.py (the independent check, with its own matcher). Matching rule, the same in both: lower-case the text, split it into tokens (runs of letters and digits; hyphens, punctuation and underscores split), and a term matches when its tokens appear in order as consecutive tokens of the text. A record is a BILL when its source label, or the opening of its excerpt (its first 'opening_chars' characters, cut at the first colon, full stop or line break: 'Receipt:', 'Charges:', 'Account summary:'), matches 'financial' (production also keeps the lexicon billing_document list). It is ADMINISTRATIVE when the same text matches 'administrative'. Otherwise it is an ENCOUNTER only when its source label matches 'encounter'; every other record is of unknown type. Bills, administrative papers and unknown types never lend their header date.",
  "opening_chars": 40,
  "encounter": [
    "visit", "note", "progress note", "office note", "clinic note", "visit note", "daily note", "operative note", "op note", "discharge note", "discharge summary",
    "er record", "ed record", "emergency department record", "emergency room record", "emergency record", "er note", "ed note", "er report", "ed report",
    "pt note", "ot note", "therapy note", "physical therapy note", "ambulance run report", "run report", "trip report", "patient care report", "operative report", "op report",
    "consult", "consultation", "consulta", "nota de consulta", "evaluation", "re-evaluation", "reevaluation", "exam", "examination", "re-examination", "reexamination",
    "new patient", "follow-up", "followup", "mri", "x-ray", "xray", "ct scan", "ultrasound", "radiology report", "imaging report"
  ],
  "financial": [
    "bill", "bills", "billed", "billing", "superbill", "statement", "statements", "invoice", "invoices", "ledger", "ledgers", "account", "itemized", "itemised", "itemization",
    "receipt", "receipts", "charges", "charge summary", "charge sheet", "fee", "fees", "estimate", "estimated", "cost", "claim", "claims", "remittance",
    "eob", "explanation of benefits", "hcfa", "cms-1500", "cms1500", "ub-04", "ub04", "ub-92", "ub92", "payment", "payments", "balance", "financial", "copay", "deductible", "price", "pricing", "quote"
  ],
  "administrative": [
    "phone", "telephone", "voicemail", "portal message", "message", "correspondence", "letter", "fax", "affidavit", "authorization", "authorisation",
    "referral", "records request", "request for records", "records retrieval", "no-show", "noshow", "custodian"
  ]
}
"""The service date a charge line prints (D-073, T-202 round 5: the pre-declared conservative fallback after four rounds of prose recognition). Code only, no LLM (LLM_VS_CODE rows 2 and 3).

A charge line takes its date of service from EXACTLY TWO sources:
  (1) its own row's date cell in a bill table whose column header names the date of service (DOS, date of service, service date, visit date, 24A ...), or the CMS-1500 24A 'From' / 'To'
      cells and the UB-04 'statement covers period FROM ... THROUGH ...', printed as a range;
  (2) the record's own date, ONLY when the record is positively identified as an encounter record by a document-type word in its source label (`record_kind`, the table
      app/backend/encounter_types.json: visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, ambulance run report, operative report ...; a provider's name is
      never enough), and the charge's own sentence holds no other date and no count of visits (a note that cites an earlier or later date, or charges 9 visits, is not one visit's date).
Prose is NOT read: 'DOS 01/09/2026', 'visit of', 'Treatment dates A to B', 'next visit date' ... inside a sentence never give a date (SCOPE_CUTS row 28). Every other line prints the fillable blank
'date of service [__________] (statement dated X)' and the Step 3 note, and the paralegal fills it from the quote. The result of `resolve` is one of:
  - `stated`: a date or complete period from source (1), or the record's own date from source (2);
  - `not_stated` with reason `no_date` / `non_service_date`: the line has no date of source (1) or (2) (`non_service_date` names the one date the code saw but does not read);
  - `not_stated` with a written-date reason (`ambiguous_numeric`, `two_digit_year`, `no_year`, `invalid`, `several_dates`, `implausible`): a DOS-column cell the code cannot read with certainty;
    the note names the date as the column writes it.
Nothing is borrowed from another line, another record or the statement year. `resolve` is the single entry point; the case view (`present.amount_view`) and the letter
(`store.export_case`) both call it through `store.charge_service_date`, so Step 3 shows exactly what the letter prints."""
import datetime as _dt
import json
import pathlib
import re

from app.backend import amounts as AM

TYPES_PATH = pathlib.Path(__file__).with_name("encounter_types.json")          # D-071 amendment 2: the one declared table of record types (also read by evals/letter_check.py)
_TYPES = json.loads(TYPES_PATH.read_text(encoding="utf-8"))


def _tokens(text: str) -> list:
    return re.findall(r"[^\W_]+", (text or "").lower())


def _phrase_rx(terms):
    return re.compile(r"(?<= )(?:" + "|".join(" ".join(re.escape(t) for t in _tokens(term)) for term in sorted(terms, key=len, reverse=True)) + r")(?= )")


_FIN, _ADMIN, _ENC = (_phrase_rx(_TYPES[k]) for k in ("financial", "administrative", "encounter"))
_OPEN = int(_TYPES["opening_chars"])


def _hit(rx, text) -> bool:
    return bool(rx.search(" " + " ".join(_tokens(text)) + " "))


def record_kind(source, excerpt: str = "") -> str:
    """'bill' | 'encounter' | 'other' (D-071 amendment 2). A bill is what amounts.billing_document says or what the declared table calls financial in the source label or the first
    characters of the excerpt, up to its first colon or full stop ('Receipt:', 'Charges:', 'Account summary:'); an administrative paper (phone note, letter, affidavit) is 'other'; an ENCOUNTER needs a positive
    identification by a DOCUMENT-TYPE word in the source label (visit, progress or office note, ER or ED record, discharge summary, PT or therapy note, run report, operative report ...; D-073: a provider
    name such as Clinic, ED, Urgent Care, Imaging, Orthopedics is never enough). Anything else is of unknown type ('other'). Only an encounter lends its header date."""
    src, opening = source or "", re.split(r"[:.\n]", (excerpt or "")[:_OPEN])[0]
    if AM.billing_document(src, excerpt or "") or _hit(_FIN, src) or _hit(_FIN, opening):
        return "bill"
    if _hit(_ADMIN, src) or _hit(_ADMIN, opening):
        return "other"
    return "encounter" if _hit(_ENC, src) else "other"

_MON = AM._MON
_ORD = r"(?:st|nd|rd|th)?"
_DASH = "–—"
_TOK = re.compile(
    r"(?<![\w/$])(?:"
    r"(?P<iso>\d{4}-\d{1,2}-\d{1,2})"
    r"|(?P<num>\d{1,2}[/.-]\d{1,2}[/.-](?:\d{4}|\d{2}))"
    rf"|(?P<mper>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}\s*[-{_DASH}]\s*(?:(?:{_MON})\.?\s+)?\d{{1,2}}{_ORD}(?:,?\s+\d{{4}})?)"
    rf"|(?P<mdy>(?:{_MON})\.?\s+\d{{1,2}}{_ORD}(?:,?\s+\d{{4}}|,\s*\d{{2}}(?!\d))?)"
    rf"|(?P<dmy>\d{{1,2}}{_ORD}[\s-]+(?:of\s+)?(?:{_MON})\.?[\s-]*,?\s*\d{{4}})"
    r"|(?P<md>\d{1,2}/\d{1,2}(?!\s*(?:hrs?|hours?|units?|miles?|mins?|visits?|sessions?)\b))"
    r")(?![\w/]|\.\d)", re.IGNORECASE)
_JOIN = re.compile(rf"^\s*(?:-|[{_DASH}]|to|through|thru|until)\s*$", re.IGNORECASE)
_LIST = re.compile(r"^\s*(?:,|;|&|and|or)\s*$", re.IGNORECASE)
# ---- D-073: the only evidence that reads a date. A column heading over the date cell (below), the UB-04 'statement covers period' span, and nothing in a sentence.
_LBL_END = r"(?:\s+(?:from|between|is|are|was|were))?[\s:#.\-\u2013\u2014(\u00b7]*$"          # a label, then spaces, a colon or a dotted leader (masked to middle dots, `_mask_leaders`), then the date
_WINDOW = 60                     # characters before a date that may hold the UB-04 span label and the leader after it
_mask_leaders = AM.mask_leaders          # the one helper: a dotted leader is neither a sentence end nor a column gap (T-209 r2)


_UB_SPAN = re.compile(r"\bstatement\s+(?:covers\s+)?period" + _LBL_END, re.IGNORECASE)       # UB-04 FL6 'Statement Covers Period FROM ... THROUGH ...': the span of the services of a coded line
_UB = re.compile(r"\bub-?04\b|\btype\s+of\s+bill\b|\bFL\s?\d{1,2}\b|\bUB\s?92\b", re.IGNORECASE)
# a column heading that names service (a CMS-1500 24A 'From'/'To' under 'Date(s) of Service', 'Service From', 'DOS' ...). A bare 'Date', 'Entry date', 'Transaction Date', 'Posted' ... does not.
_H_SVC = re.compile(r"\bdos\b|date\(?s?\)?\s+of\s+serv|service\s+date|\bsvc\b|visit\s+date|date\s+of\s+visit|encounter\s+date|"
                    r"\b(?:service|svc)\s+(?:from|to|thru|through)\b|\b(?:from|to|thru|through)\s+(?:dos|service|svc)\b|\b24\s*-?a\b", re.IGNORECASE)
_YEARS_BEFORE = 5                # a bill's service date more than this many years before its statement is doubtful

REASONS = ("ambiguous_numeric", "two_digit_year", "no_year", "invalid", "several_dates", "implausible", "non_service_date", "no_date")
WRITTEN = frozenset(REASONS[:6])      # the quote labels a date of service the code cannot read with certainty (its note names the date as written)


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


BLANK = "date of service [__________]"


def not_stated_text(statement_iso) -> str:
    """The text the letter puts after the provider when no service date is certain (D-071 addendum): a fillable blank, like the Bates placeholder, never an inferred date. The
    paralegal fills it from the quote. 'date of service [__________] (statement dated June 15, 2026)'."""
    if statement_iso:
        return f"{BLANK} (statement dated {display(statement_iso)})"
    return BLANK


def printed_text(res: dict, statement_iso) -> str:
    """The text the letter prints after the provider for a resolved line that is not stated: the blank, for every reason (a labeled date the code cannot read included)."""
    return not_stated_text(statement_iso)


_WHY = {
    "ambiguous_numeric": "The date of service column of the bill reads {raw}, which can be read as month/day or day/month; the record does not settle which.",
    "two_digit_year": "The date of service column of the bill reads {raw}, which has a two-digit year; the code does not guess the century.",
    "no_year": "The date of service column of the bill reads {raw}, which states no year; the code does not borrow one from the statement.",
    "invalid": "The date of service column of the bill reads {raw}, which is not a complete date on the calendar.",
    "several_dates": "The date of service column of the bill holds more than one date ({raw}) and nothing says which one belongs to this charge.",
    "implausible": "The date of service column of the bill reads {raw}, but that date is after the statement it appears on or years before it.",
    "non_service_date": "The line shows {raw}, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service.",
    "no_date": "The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note).",
}
_ASK_WRITTEN = " The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it."
_ASK_NONE = " The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated itemized bill, and fill the blank before you rely on it."


def confirm_note(reason, raw) -> str:
    """The Step 3 note and the internal-notes line for a charge whose service date is not certain: why, and what the letter does (D-071 amendment)."""
    return _WHY.get(reason, _WHY["no_date"]).format(raw=raw or "the date") + (_ASK_WRITTEN if reason in WRITTEN else _ASK_NONE)


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
        m = re.match(rf"({_MON})\.?\s+(\d{{1,2}}){_ORD}(?:,?\s+(\d{{4}})|,\s*(\d{{2}}))?$", s, re.IGNORECASE)
        if m.group(4):
            self.flaw = "two_digit_year"
            return
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:44:37.069Z

**tool call — Bash**
````
{
 "command": "git show f9c0faf:app/backend/service_date.py | sed -n 200,420p",
 "description": "Read rest of service_date.py"
}
````

### User / tool · 2026-11-03T02:44:37.162Z

**tool result**
````
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
    """[(start column, text)] of the table heading above the row: the nearest line above with no digits (data rows in between are skipped), up to a blank line. A bare From / To / Thru cell
    under a line that names the service (a CMS-1500 '24A DATE(S) OF SERVICE' over 'From To') takes that line's words, so the cell names the service too."""
    rev = list(reversed(excerpt[:max(row_ls - 1, 0)].split("\n")[-40:]))
    for k, line in enumerate(rev):
        if not line.strip():
            return None
        if re.search(r"\d", line) and not _H_SVC.search(line):
            continue
        cells = [(m.start(), m.group(0)) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]
        above = rev[k + 1].strip() if k + 1 < len(rev) else ""
        if above and _H_SVC.search(above) and not _H_SVC.search(line):
            cells = [(c, f"{above} {t}" if re.fullmatch(r"(?i)from|to|thru|through", t.strip()) else t) for c, t in cells]
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


def _plausible(first, last, ref) -> bool:
    """A service date is not after the record it appears in and not years before it."""
    if not ref:
        return True
    r = _dt.date.fromisoformat(ref)
    return (last or first) <= ref and _dt.date.fromisoformat(first) >= r - _dt.timedelta(days=366 * _YEARS_BEFORE)


def _decide(units, text, ref):
    """('ok', first, last) for one certain labeled unit (or several that read the same); ('bad', reason, [raw, ...]) otherwise."""
    reads = [(u, _certain(u, ref)) for u in units]
    raws = [" ".join(u.raw(text).split()) for u in units]
    if len(units) > 1:
        same = {(r[1], r[2]) for _, r in reads if r[0] == "ok"}
        if not (len(same) == 1 and all(r[0] == "ok" for _, r in reads)):
            return "bad", "several_dates", raws
        first, last = next(iter(same))
    else:
        r = reads[0][1]
        if r[0] != "ok":
            return "bad", r[1], raws
        first, last = r[1], r[2]
    if not _plausible(first, last, ref):          # in every record: a service date is not after the record's own date and not years before it (a prior treatment's DOS is not this charge's)
        return "bad", "implausible", raws
    return "ok", first, last


def _apply(out: dict, res) -> dict:
    if res[0] == "ok":
        out.update(state="stated", first=res[1], last=res[2], reason=None, raw="", raws=[])
    else:
        out.update(reason=res[1], raw=", ".join(res[2]), raws=list(res[2]))
    return out


_MULTI = re.compile(r"\b(?:visits|sessions|treatments|appointments|encounters)\b|\bto[ -]date\b|\bvisits?\s+\d+\s*(?:-|\u2013|\u2014|to|through|thru)\s*\d+|"
                    r"\b(?:[2-9]|\d{2,}|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s*(?:x|times)\b", re.IGNORECASE)          # a charge for more than one visit


def _table_dates(seg, excerpt, ss, a_start, units):
    """[(unit, heading)] of a bill-table row's dates, in the row's own text `seg`; the heading is the column heading over the date cell ('' when none)."""
    row_ls = excerpt.rfind("\n", 0, a_start) + 1
    rl_end = excerpt.find("\n", a_start)
    row_text = excerpt[row_ls:len(excerpt) if rl_end < 0 else rl_end]
    row_cells = [(m.start(), m.end()) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", row_text)]
    return [(u, _column_head(excerpt, row_ls, row_cells, ss + u.start)) for u in units]


def _from_to(pairs):
    """The units of a table row's service-date cells: a CMS-1500 24A 'From' cell followed by its 'To' / 'Thru' cell is one period (the same day twice is that day)."""
    out, k = [], 0
    while k < len(pairs):
        u, head = pairs[k]
        if not _H_SVC.search(head or ""):
            k += 1
            continue
        nxt = pairs[k + 1] if k + 1 < len(pairs) else None
        if nxt and re.search(r"\bfrom\b", head, re.IGNORECASE) and re.search(r"\b(?:to|thru|through)\b", nxt[1] or "", re.IGNORECASE):
            same = u.toks[-1].raw.strip() == nxt[0].toks[0].raw.strip()
            out.append(u if same else _Unit(u.toks + nxt[0].toks))
            k += 2
            continue
        out.append(u)
        k += 1
    return out


def resolve(excerpt: str, start: int, source, date_iso) -> dict:
    """{state: 'stated'|'not_stated', first, last (None for one day), reason (None when stated, else one of REASONS), raw (the date text the reason is about), raws ([the dates as written])} for
    the figure at `start` of `excerpt`, in a record with header `source` and date `date_iso`. Exactly two sources give a date (module doc, D-073)."""
    out = {"state": "not_stated", "first": None, "last": None, "reason": "no_date", "raw": "", "raws": []}
    excerpt = _mask_leaders(excerpt)
    amts = AM.find_amounts(excerpt or "")
    i = next((n for n, a in enumerate(amts) if a["start"] == start), None)
    if i is None:
        return out
    a = amts[i]
    ss, se = next(((s, e) for s, e in AM._segments(excerpt) if s <= a["start"] < e), (0, len(excerpt)))
    kind = record_kind(source, excerpt)
    seg = excerpt[ss:se]
    units = _units(seg)
    others = [u.raw(seg) for u in units]                                   # the dates of the line that no source reads
    if len(AM._cells(seg)) >= 2 and units:                                 # source (1): the date cell of its own row, under a heading that names the date of service
        lab = _from_to(_table_dates(seg, excerpt, ss, a["start"], units))
        if lab:
            return _apply(out, _decide(lab, seg, date_iso))
    if kind == "bill" and AM._CODE_RX.search(seg[:a["start"] - ss]) and (_UB.search(source or "") or _UB.search(excerpt or "")):
        prefix = excerpt[:se]                                              # source (1), UB-04 FL6: a coded line takes the span its 'statement covers period FROM ... THROUGH ...' states
        span = [u for u in _units(prefix) if _UB_SPAN.search(prefix[max(0, u.start - _WINDOW):u.start])]
        if span:
            return _apply(out, _decide(span, prefix, date_iso))
    if kind != "encounter":                                                # a bill, an administrative paper or a record of unknown type never lends its header date
        if others:
            out.update(reason="non_service_date", raw=others[0])
        return out
    if not date_iso:
        return out
    # source (2): the date of an identified encounter record is the visit's, unless the charge's own sentence names another date or charges more than one visit
    for u in units:
        r = _certain(u, date_iso)
        if not (r[0] == "ok" and r[1] == date_iso and not r[2]):
            out.update(reason="non_service_date", raw=u.raw(seg))
            return out
    if _MULTI.search(seg):
        return out
    out.update(state="stated", first=date_iso, last=None, reason=None, raw="", raws=[])
    return out
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:45:10.292Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4 && cat h.py letters_dump_r4.py provider_only_bill.py eval_teeth_r4.py; sed -n 1,126p p01_cases.py",
 "description": "Read r4 helper scripts"
}
````

### User / tool · 2026-11-03T02:45:10.395Z

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

BASE = os.environ.get("T181_BASE", "http://127.0.0.1:7984")  # T-202 r4: 8cb5bd2 archive, port 7984
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
"""T-202 r4 paralegal: in-process letters + internal notes (all_accepted and counted) for sample, case_09, lib14, lib10, lib11 and SYNTHETIC variants
(rounds 2-3 variants kept; round 4 adds dotted-leader, other-visit DOS, treatment-dates-in-a-visit-note and provider-name-only-bill variants), with
evals.letter_check.charge_date_violations on each. Writes letters to <out_dir> when given. Works on older archives (falls back when a function is missing).
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/letters_dump_r4.py <archive_root> [<out_dir>]
"""
import os
import sys
import traceback

root = os.path.abspath(sys.argv[1])
out = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else None
sys.path.insert(0, root)
os.chdir(root)
os.environ.setdefault("LLM_BACKEND", "fixture")
os.environ.setdefault("FIXTURE_SET", "curated")
from evals import letter_check as LC  # noqa: E402


def sub(text, old, new):
    assert old in text, old
    return text.replace(old, new)


SAMPLE = open("evals/golden/sample.txt").read()
C09 = open("evals/golden/case_09_nonvisit_hides_gap.txt").read()
C09_R2 = 'Date: 2026-03-01\nSource: Hobbleton Family Clinic, billing statement\nExcerpt: "Statement for visit of 2026-02-02: $275."'
ER_TAIL = "Follow up with PCP in 1 week. ER charges: $6,240."
CASES = {
    "sample": SAMPLE,
    "case_09": C09,
    "lib14": open("evals/library/case_lib14_handwritten_chiro_scans.txt").read(),
    "lib10": open("evals/library/case_lib10_eob_ub04_cms1500.txt").read(),
    "lib11": open("evals/library/case_lib11_priors_and_ledger.txt").read(),
    # round 2
    "synth_ambiguous_dos": sub(C09, C09_R2, 'Date: 2026-06-01\nSource: Hobbleton Family Clinic, billing statement\nExcerpt: "Date of service 04/05/2026: office visit charge $275.00."'),
    "synth_cms1500_two_dates": sub(C09, C09_R2, 'Date: 2026-04-20\nSource: Hobbleton Family Clinic, CMS-1500\nExcerpt: "CMS-1500 for dates of service 02/02/2026 and 03/30/2026. CPT 99213 charge $150.00. CPT 29125 splint charge $125.00."'),
    # round 3 blocker text: next visit date after the ER charge, comma-joined
    "synth_sample_er_next_visit": sub(SAMPLE, ER_TAIL, "Follow up with PCP in 1 week. ER charges: $6,240, next visit date 01/16/2026."),
    # round 4: dotted leader (brief text) in the ER note, and in the case_09 bill
    "synth_sample_er_dotted_leader": sub(SAMPLE, ER_TAIL, "Follow up with PCP in 1 week. Date of service.......01/09/2026   ER charges ...... $6,240."),
    "synth_case09_bill_dotted_leader": sub(C09, C09_R2, 'Date: 2026-03-01\nSource: Hobbleton Family Clinic, billing statement\nExcerpt: "Date of service.......02/02/2026   Office visit 99213 ...... $275.00"'),
    # round 4: a prior visit's DOS in the PCP note's charge clause (qualifier not in the lookbehind list)
    "synth_sample_pcp_er_dos": sub(SAMPLE, "Patient reports low back pain in 2023, resolved.", "Patient reports low back pain in 2023, resolved. Reviewed ER records, DOS 01/09/2026, office visit charge $150.00."),
    # round 4: a stated treatment period for a multi-visit charge inside the PT discharge note (round 3 printed the range)
    "synth_sample_pt_treatment_dates": sub(SAMPLE, "Discharged from PT after two missed appointments. Pain 3/10.", "Discharged from PT after two missed appointments. Pain 3/10. Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00."),
    # round 4: the case_09 bill labelled with the provider name only (no record-type word), excerpt naming its own visit date
    "synth_case09_provider_only_bill": sub(C09, C09_R2, 'Date: 2026-03-01\nSource: Hobbleton Family Clinic\nExcerpt: "Amount due $275.00 for office visit on 02/02/2026."'),
}
only = os.environ.get("ONLY")
for name, text in CASES.items():
    if only and name not in only.split(","):
        continue
    try:
        got = LC.letters_for(text)
    except Exception:
        print(f"== {name}: letters_for raised\n{traceback.format_exc()}")
        continue
    for variant in ("all_accepted", "counted"):
        if variant not in got:
            continue
        v = got[variant]
        letter = v["letters"]["standard"]
        if out:
            with open(os.path.join(out, f"{name}-{variant}-letter.txt"), "w") as f:
                f.write(letter)
            with open(os.path.join(out, f"{name}-{variant}-notes.txt"), "w") as f:
                f.write(v["notes"])
        print(f"== {name} {variant}: cents={v.get('charge_cents')} refused={v.get('refused')} gate={v.get('gate')}")
        if hasattr(LC, "charge_lines"):
            for h, q in LC.charge_lines(letter):
                print("   ", h, "|", q)
        else:
            i = letter.find("BILLED CHARGES")
            print("    " + letter[i:].replace("\n", "\n    ") if i >= 0 else "    (no BILLED CHARGES section)")
        if hasattr(LC, "charge_date_violations") and "records" in v:
            print("    date violations:", LC.charge_date_violations(letter, v["records"]))
"""T-202 r4 paralegal: SYNTHETIC case_09 variants whose record 2 is the clinic's bill but whose Source line is the provider name only (no record-type word),
through the full case pipeline and letter (evals.letter_check.letters_for), with charge_date_violations. Record 2 keeps Date 2026-03-01 (the statement date).
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/provider_only_bill.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
os.environ.setdefault("LLM_BACKEND", "fixture")
os.environ.setdefault("FIXTURE_SET", "curated")
from evals import letter_check as LC  # noqa: E402

C09 = open("evals/golden/case_09_nonvisit_hides_gap.txt").read()
OLD = 'Date: 2026-03-01\nSource: Hobbleton Family Clinic, billing statement\nExcerpt: "Statement for visit of 2026-02-02: $275."'
assert OLD in C09
VARIANTS = {
    "pa_office_visit_dated": ("Hobbleton Family Clinic", "Office visit 02/02/2026, 99213, charge $275.00."),
    "pb_visit_of": ("Hobbleton Family Clinic", "Office visit 99213 charge $275.00 for the visit of 02/02/2026."),
    "pc_no_date": ("Hobbleton Family Clinic", "Office visit 99213, charge $275.00."),
    "pd_control_billing_statement": ("Hobbleton Family Clinic, billing statement", "Office visit 02/02/2026, 99213, charge $275.00."),
}
for name, (src, ex) in VARIANTS.items():
    text = C09.replace(OLD, f'Date: 2026-03-01\nSource: {src}\nExcerpt: "{ex}"')
    v = LC.letters_for(text)["all_accepted"]
    letter = v["letters"]["standard"]
    print(f"== {name}: Source '{src}' / Excerpt '{ex}' / cents={v['charge_cents']}")
    for h, q in LC.charge_lines(letter):
        print("   ", h, "|", q)
    print("    date violations:", LC.charge_date_violations(letter, v["records"]))
    for line in v["notes"].splitlines():
        if "275" in line:
            print("    notes:", line)
"""T-202 r4 paralegal: evals.letter_check.charge_date_violations on the line the 8cb5bd2 build prints vs the line a paralegal would accept, for the round 4
wrong-date shapes (SYNTHETIC). Shows whether the independent check catches the wrong line and passes the right one.
    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r4/eval_teeth_r4.py <archive_root>
"""
import os
import sys

root = os.path.abspath(sys.argv[1])
sys.path.insert(0, root)
os.chdir(root)
from evals import letter_check as LC  # noqa: E402

BL = "date of service [__________]"


def letter(head, fig, quote):
    return f"BILLED CHARGES\n\n{head}: {fig}\nSource [Ex. __ / Bates __]: \"{quote}\"\n\nBilled charges accepted from these records: {fig}"


CASES = [
    # name, source, record date, excerpt, quote, figure, build's head, paralegal's heads
    ("O1 PCP note, ER DOS in the charge clause", "Dr. Alvarez, primary care", "2026-01-16",
     "Persistent neck pain 6/10, daily headaches. Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.",
     "Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.", "$150.00",
     "Dr. Alvarez, primary care, January 9, 2026",
     ["Dr. Alvarez, primary care, January 16, 2026", f"Dr. Alvarez, primary care, {BL} (statement dated January 16, 2026)"]),
    ("R21 PT visit 9, treatment dates in the charge clause", "Capital PT, visit 9", "2026-03-06",
     "Discharged from PT after two missed appointments. Pain 3/10. Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.",
     "Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.", "$1,665.00",
     "Capital PT, visit 9, March 6, 2026",
     ["Capital PT, visit 9, January 23–March 6, 2026", f"Capital PT, visit 9, {BL} (statement dated March 6, 2026)"]),
    ("PA provider-name-only bill", "Hobbleton Family Clinic", "2026-03-01",
     "Office visit 02/02/2026, 99213, charge $275.00.",
     "Office visit 02/02/2026, 99213, charge $275.00.", "$275.00",
     "Hobbleton Family Clinic, March 1, 2026",
     [f"Hobbleton Family Clinic, {BL} (statement dated March 1, 2026)", "Hobbleton Family Clinic, February 2, 2026"]),
]
for name, src, rd, ex, q, fig, build, alts in CASES:
    recs = [{"n": 1, "source": src, "date_iso": rd, "excerpt": ex}]
    print(f"== {name}")
    print(f"   build  '{build}: {fig}' -> {LC.charge_date_violations(letter(build, fig, q), recs)}")
    for h in alts:
        print(f"   alt    '{h}: {fig}' -> {LC.charge_date_violations(letter(h, fig, q), recs)}")
"""T-202 r2 paralegal (copied from r1): 986fc55 archive, demo/fixture backend, local mode, port 7976.
For each case (env CASES, default sample,case_09,lib14,lib10): open it as a user (sample tile / paste / library), draft, Step 2 accept with the
keyboard (compare box ticked where asked), Step 3 accept every bill item and tick 'count' boxes where offered, Step 4 download letter + notes.
Run: .venv/bin/python -I artifacts/review-evidence/T-202-paralegal/h.py artifacts/review-evidence/T-202-paralegal/p01_cases.py
"""
import os
import re

CASES = os.environ.get("CASES", "sample,case_09,lib14,lib10,lib11").split(",")  # r4: 8cb5bd2 archive, port 7984
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:45:11.296Z

Set up the archive and r5 evidence dir.

### Assistant · claude-opus-5-5 · 2026-11-03T02:45:14.328Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p $S/pr5_f9c0faf && git archive f9c0faf | tar -x -C $S/pr5_f9c0faf && git rev-parse f9c0faf^{tree} && ls $S/pr5_f9c0faf | head -30",
 "description": "Extract f9c0faf archive into scratchpad"
}
````

### User / tool · 2026-11-03T02:45:15.981Z

**tool result**
````
7ec6d6b2632a851afc2f7a28dde7900d6bd44d95
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

### Assistant · claude-opus-5-5 · 2026-11-03T02:45:18.436Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-202-paralegal-r5/letters && cp artifacts/review-evidence/T-202-paralegal-r4/{h.py,p01_cases.py,letters_dump_r4.py,provider_only_bill.py,eval_teeth_r4.py,probe_r4.py} artifacts/review-evidence/T-202-paralegal-r5/ && ls artifacts/review-evidence/ | grep -i serve | head",
 "description": "Create r5 evidence dir and copy scripts"
}
````

### User / tool · 2026-11-03T02:45:18.548Z

**tool result**
````
T-049-served-index.html
T-060-paralegal-pass4-serve.py
T-120-r2-paralegal-server.log
T-209-r3-paralegal-server.log
T-209-r4-paralegal-server.log
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:45:19.310Z

Run the deterministic checks first.

### Assistant · claude-opus-5-5 · 2026-11-03T02:45:25.033Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf && PYTHONDONTWRITEBYTECODE=1 LLM_BACKEND=fixture FIXTURE_SET=curated /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_t202_r5_d073.py tests/unit/test_t202_r4_encounter.py tests/unit/test_t202_r3_allow_list.py tests/unit/test_t202_r2_service_date_layouts.py tests/unit/test_t202_charge_service_dates.py tests/unit/test_t200_undated_charge_label.py > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/pytest-t202.out 2>&1; tail -3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/pytest-t202.out; LLM_BACKEND=fixture FIXTURE_SET=curated /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.letter_check > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/letter_check.out 2>&1; echo exit=$?; tail -5 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/letter_check.out",
 "description": "Run T-202 unit tests and letter_check eval from archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:45:48.193Z

**tool result**
````
........................................................................ [ 97%]
................                                                         [100%]
736 passed in 11.25s
exit=0
{"value": 0, "cases": 25, "held_out_entries": 11, "backend": "fixture", "r_ids": ["R-CH-7", "R-EX-8", "R-EX-1"]}
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:46:36.256Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-202-paralegal/all_charge_lines.py; git show f9c0faf:app/backend/amounts.py | grep -n \"def _segments\" -A25",
 "description": "Read all_charge_lines script and segments function"
}
````

### User / tool · 2026-11-03T02:46:36.372Z

**tool result**
````
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
434:def _segments(excerpt: str) -> list:
435-    out, pos = [], 0
436-    for m in _BOUNDARY.finditer(excerpt):
437-        out.append((pos, m.start()))
438-        pos = m.end()
439-    out.append((pos, len(excerpt)))
440-    return [(s, e) for s, e in out if e > s]
441-
442-
443-def _cells(line: str) -> list:
444-    return [m.group(0) for m in re.finditer(r"[^\t| ]+(?: [^\t| ]+)*", line)]
445-
446-
447-def billing_document(source, excerpt: str = "") -> bool:
448-    """A provider bill or ledger: the source label names one (lexicon billing_document, or a statement / bill / invoice / ledger / account word), or the
449-    excerpt opens as one ("Itemized statement: ...")."""
450-    return bool(_is_billing_source(source or "") or _BILLISH.search(source or "") or _BILL_OPEN.search(excerpt or ""))
451-
452-
453-def _record_period(before: str, ref_iso):
454-    """(first date, last date or None) of the date or period the record states for its services. D-071: the last date is the end of the range ('06/09/2026 to 06/12/2026'),
455-    None for a single date ('the run of 09/14/2026')."""
456-    ms = list(_DOS_RX.finditer(before))
457-    for k, m in enumerate(ms):
458-        iso = _dos_iso(m, ref_iso)
459-        if iso and _PERIOD_PHRASE.search(before[max(0, m.start() - 40):m.start()]):
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:46:38.446Z

**tool call — Bash**
````
{
 "command": "git show f9c0faf:app/backend/amounts.py | grep -n \"_BOUNDARY *=\\|_BILL_OPEN *=\\|_BILLISH *=\\|def _is_billing_source\" -A4 | head -40",
 "description": "Check segment boundary and bill-open regexes"
}
````

### User / tool · 2026-11-03T02:46:38.564Z

**tool result**
````
13:_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
14-_LEADER = re.compile(r"(?:\.[ ]?){3,}|\u2026+")
15-
16-
17-def mask_leaders(text: str) -> str:
--
327:_BILLISH = re.compile(r"\b(?:statements?|bills?|billing|invoices?|ledgers?|account|itemi[sz]ed|ub-?04|hcfa|cms-?1500|claim\s+form)\b", re.IGNORECASE)
328:_BILL_OPEN = re.compile(r"^\W{0,3}(?:patient\s+)?(?:itemi[sz]ed|statement|invoice|ledger|billing|account\s+statement)\b", re.IGNORECASE)
329-_TOKEN_FILLER = frozenset("charge charges charged billed fee fees of on for the a an at to and unit units dos date service services statement rev cpt code invoiced total".split())
330-_NO_DATE_WHY = "The line states no date of service, so it is not an itemized service line and is not totaled."
331-NO_DATE_WHY = _NO_DATE_WHY           # T-200: the stored reason of a charge the paralegal counted because its line states no date of service
332-_NO_SVC_WHY = "The line names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized service line and is not totaled."
--
789:def _is_billing_source(source: str) -> bool:
790-    return any(e["id"] == "billing_document" and e["regex"].search(source or "") for e in lexicon.code_list("non_encounter"))
791-
792-
793-def damages_mentions(excerpt: str) -> list:
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:46:44.398Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence && grep -n \"^PROBES\\|^PROBES +=\\|^[A-Z_0-9]* = \\\"\" T-202-paralegal-r2/probe_r2.py T-202-paralegal-r2/probe_r2b.py T-202-paralegal-r3/probe_r3*.py | head -40; grep -c \"^    (\\\"\" T-202-paralegal-r2/probe_r2.py T-202-paralegal-r2/probe_r2b.py T-202-paralegal-r3/probe_r3*.py",
 "description": "Inspect older probe file structures"
}
````

### User / tool · 2026-11-03T02:46:44.492Z

**tool result**
````
T-202-paralegal-r3/probe_r3.py:26:PROBES = load(os.path.join(ev, "probe_r2.py")) + load(os.path.join(ev, "probe_r2b.py"))
T-202-paralegal-r3/probe_r3.py:28:V = "Dr. Alvarez, primary care"
T-202-paralegal-r3/probe_r3.py:29:H = "Hobbleton Family Clinic, billing statement"
T-202-paralegal-r3/probe_r3.py:30:L = "Larkspur Hollow Physical Therapy, itemized ledger"
T-202-paralegal-r3/probe_r3.py:31:W = "Wardlaw Orthopedics, CMS-1500"
T-202-paralegal-r3/probe_r3.py:32:PROBES += [
T-202-paralegal-r3/probe_r3b.py:14:V = "Dr. Alvarez, primary care"
T-202-paralegal-r3/probe_r3b.py:15:PT = "Capital PT, discharge summary"
T-202-paralegal-r3/probe_r3b.py:16:ER = "Central ER discharge summary"
T-202-paralegal-r3/probe_r3b.py:17:H = "Hobbleton Family Clinic, billing statement"
T-202-paralegal-r3/probe_r3b.py:18:PROBES = [
T-202-paralegal-r2/probe_r2b.py:13:PROBES = [
T-202-paralegal-r2/probe_r2.py:14:PROBES = [
T-202-paralegal-r3/probe_r3c.py:13:ER = "Central ER discharge summary"
T-202-paralegal-r3/probe_r3c.py:14:PT = "Capital PT, initial evaluation"
T-202-paralegal-r3/probe_r3c.py:15:PROBES = [
T-202-paralegal-r2/probe_r2.py:38
T-202-paralegal-r3/probe_r3b.py:9
T-202-paralegal-r2/probe_r2b.py:12
T-202-paralegal-r3/probe_r3c.py:7
T-202-paralegal-r3/probe_r3.py:16
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:46:47.517Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r4 && sed -n 1,40p probe_r4.out; grep -c \"^== \" probe_r4.out",
 "description": "Look at r4 probe output format"
}
````

### User / tool · 2026-11-03T02:46:47.614Z

**tool result**
````
# loaded 38 probes from T-202-paralegal-r2/probe_r2.py
# loaded 12 probes from T-202-paralegal-r2/probe_r2b.py
# loaded 16 probes from T-202-paralegal-r3/probe_r3.py
# loaded 9 probes from T-202-paralegal-r3/probe_r3b.py
# loaded 7 probes from T-202-paralegal-r3/probe_r3c.py
== probe_r2 P1 two-row ledger, own dates  (record date 2026-03-15; source 'Hobbleton Family Clinic, itemized ledger'; kind=bill; billing_document=True)
   Statement date 03/15/2026. 02/02/2026 office visit charge $275.00. 02/16/2026 x-ray charge $150.00. Balance due $425.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger, date of service [__________] (statement dated March 15, 2026): $275.00'  state=not_stated reason=non_service_date
              Step 3 note: The only date near this line (02/02/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
      $150.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger, date of service [__________] (statement dated March 15, 2026): $150.00'  state=not_stated reason=non_service_date
              Step 3 note: The only date near this line (02/16/2026) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
      $425.00 -> letter head: 'Hobbleton Family Clinic, itemized ledger, date of service [__________] (statement dated March 15, 2026): $425.00'  state=not_stated reason=no_date
              Step 3 note: The line states no date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
== probe_r2 P2 CMS-1500 two DOS joined by 'and'  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; kind=bill; billing_document=True)
   CMS-1500 for dates of service 06/24/2026 and 07/08/2026. CPT 99204 charge $185.00. CPT 20610 charge $210.00.
      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=several_dates
              Step 3 note: The quote labels more than one date of service (06/24/2026, 07/08/2026) and nothing says which one belongs to this charge. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.
      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $210.00'  state=not_stated reason=several_dates
              Step 3 note: The quote labels more than one date of service (06/24/2026, 07/08/2026) and nothing says which one belongs to this charge. The letter prints no service date for this line. It leaves a blank for the date of service. Confirm the date from the quote and fill the blank before you rely on it.
== probe_r2 P3 invoice date stated before run date  (record date 2026-11-12; source 'Tarnwick Fire-Rescue, ambulance invoice'; kind=bill; billing_document=True)
   Invoice date 11/12/2026. Run of 09/14/2026. A0427 ALS emergency transport, charge $1,380.00.
    $1,380.00 -> letter head: 'Tarnwick Fire-Rescue, ambulance invoice, September 14, 2026: $1,380.00'  state=stated reason=None
== probe_r2 P4 UB-04 period across months  (record date 2026-07-10; source 'Saltmarrow General Hospital, UB-04 itemized bill'; kind=bill; billing_document=True)
   UB-04 statement period 06/28/2026 to 07/02/2026. Rev 0120 room and board, FL47 total charges $4,920.00.
    $4,920.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 28–July 2, 2026: $4,920.00'  state=stated reason=None
== probe_r2 P5 UB-04 period with 'through'  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04 itemized bill'; kind=bill; billing_document=True)
   UB-04 statement period 06/09/2026 through 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.
    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00'  state=stated reason=None
== probe_r2 P6 UB-04 period with hyphen  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04 itemized bill'; kind=bill; billing_document=True)
   UB-04 statement period 06/09/2026 - 06/12/2026. Rev 0450 emergency room, FL47 total charges $2,105.00.
    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00'  state=stated reason=None
== probe_r2 P7 statement + DOS label same sentence  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; kind=bill; billing_document=True)
   Statement date 03/01/2026, date of service 02/02/2026: office visit charge $275.00.
      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00'  state=stated reason=None
== probe_r2 P8 ledger row DOS then posted, two-digit years  (record date 2026-06-15; source 'Fennimoor Spine Clinic, itemized ledger'; kind=bill; billing_document=True)
   06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00. 06/12/26 06/13/26 97110 Therapeutic exercise charge $95.00.
       $95.00 -> letter head: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $95.00'  state=not_stated reason=non_service_date
              Step 3 note: The only date near this line (06/12/26) is not labeled as a date of service (it may be a birth, injury, referral, order, posting, statement or transaction date, or its column heading does not name service). The letter prints no service date for this line. It leaves a blank for the date of service. Request a dated itemized bill, or fill the blank from the record, before you rely on it.
== probe_r2 P9 statement period then a separately dated line  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04 itemized bill'; kind=bill; billing_document=True)
   UB-04 statement period 06/09/2026 to 06/12/2026. Rev 0450 emergency room, service date 06/09/2026, FL47 total charges $2,105.00.
115
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:47:25.409Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/probe_r5.py",
 "content": "\"\"\"T-202 r5 (D-073) paralegal probe: every SYNTHETIC charge text from rounds 1-4 (r2 probe_r2.py/probe_r2b.py, r3 probe_r3.py/probe_r3b.py/probe_r3c.py\nPROBES lists, r4 probe_r4.py NEW list), loaded by ast, plus round 5 shapes that probe D-073 from its opposite side:\n  E*  sources whose only encounter word is a provider/service name (MRI, X-Ray, Follow-Up, Evaluation, Exam, Visit) on a bill; encounter notes whose charge is for\n      another visit or several visits without a date or a 'visits' word in its own sentence; a late-entry note whose visit date sits in the previous sentence;\n  T*  bill-table rows (DOS column, Posted column, header-less rows under a summary line, FL45 'SERV DATE');\n  U*  UB-04 spans.\nThrough the shipped path store.charge_service_date (Step 3 and the letter share it). Prints the letter head as export builds it, and a final list of every\nSTATED result (the only lines that can carry a wrong date under D-073) for manual truth checking.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/probe_r5.py <archive_root> <repo_root>\n\"\"\"\nimport ast\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nrepo = os.path.abspath(sys.argv[2])\nsys.path.insert(0, root)\nos.chdir(root)\nfrom app.backend import amounts as AM, store  # noqa: E402\n\ntry:\n    from app.backend import service_date as SD  # noqa: E402\n    KIND = getattr(SD, \"record_kind\", None)\nexcept Exception:\n    KIND = None\n\n\ndef load(path, name):\n    tree = ast.parse(open(path).read())\n    ns, out = {}, []\n    for node in tree.body:\n        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):\n            for t in node.targets:\n                if isinstance(t, ast.Name):\n                    ns[t.id] = node.value.value\n        tgt = node.targets[0] if isinstance(node, ast.Assign) else (node.target if isinstance(node, ast.AugAssign) else None)\n        if getattr(tgt, \"id\", \"\") == name and isinstance(node.value, ast.List):\n            out += eval(compile(ast.Expression(node.value), path, \"eval\"), {}, ns)\n    if not out:\n        raise SystemExit(f\"no {name} in {path}\")\n    return out\n\n\nev = os.path.join(repo, \"artifacts/review-evidence\")\nOLD = []\nfor f, name in ((\"T-202-paralegal-r2/probe_r2.py\", \"PROBES\"), (\"T-202-paralegal-r2/probe_r2b.py\", \"PROBES\"), (\"T-202-paralegal-r3/probe_r3.py\", \"PROBES\"),\n                (\"T-202-paralegal-r3/probe_r3b.py\", \"PROBES\"), (\"T-202-paralegal-r3/probe_r3c.py\", \"PROBES\"), (\"T-202-paralegal-r4/probe_r4.py\", \"NEW\")):\n    got = load(os.path.join(ev, f), name)\n    print(f\"# loaded {len(got)} probes from {f}\")\n    OLD += [(f.split(\"/\")[1].replace(\".py\", \"\") + \" \" + p[0],) + tuple(p[1:]) for p in got]\n\nPTD = \"Capital PT, visit 9\"\nER = \"Central ER discharge summary\"\nNEW = [\n    # E: encounter words that are provider or service names, on a bill (record date = statement date 06/20; MRI performed 05/29)\n    (\"E1 'Open MRI of Austin' bill, no date in the charge sentence\", \"Open MRI of Austin\", \"2026-06-20\",\n     \"Cervical spine MRI without contrast, CPT 72141. Total due $2,150.00.\"),\n    (\"E2 'Austin MRI' bill, thank-you opening\", \"Austin MRI\", \"2026-06-20\",\n     \"Thank you for choosing Austin MRI. Amount due $2,150.00.\"),\n    (\"E3 'Austin MRI' bill, MRI date in the previous sentence\", \"Austin MRI\", \"2026-06-20\",\n     \"MRI performed 05/29/2026. Amount due $2,150.00.\"),\n    (\"E4 'Hill Country X-Ray' bill\", \"Hill Country X-Ray\", \"2026-02-10\",\n     \"Cervical spine, 3 views, CPT 72050. Patient responsibility $240.00.\"),\n    (\"E5 'Westlake Follow-Up Clinic' bill\", \"Westlake Follow-Up Clinic\", \"2026-03-01\",\n     \"Office visit 99213. Amount due $150.00.\"),\n    (\"E6 'Capital Evaluation Center' bill\", \"Capital Evaluation Center\", \"2026-04-15\",\n     \"Functional capacity evaluation, CPT 97750. Amount due $900.00.\"),\n    (\"E7 'Express Exam Urgent Care' bill\", \"Express Exam Urgent Care\", \"2026-02-01\",\n     \"Urgent care visit 99204. Amount owed $310.00.\"),\n    (\"E8 'Austin Imaging, cervical MRI' (sample label) with a bill excerpt\", \"Austin Imaging, cervical MRI\", \"2026-06-20\",\n     \"Amount due $2,150.00. Thank you for choosing Austin Imaging.\"),\n    (\"E9 control: 'Austin MRI, billing statement'\", \"Austin MRI, billing statement\", \"2026-06-20\",\n     \"Cervical spine MRI without contrast, CPT 72141. Total due $2,150.00.\"),\n    # E: encounter notes whose charge is not this visit's\n    (\"E10 ER discharge summary 01/09: balance from a prior visit\", ER, \"2026-01-09\",\n     \"Patient seen in this ER in 2025. Balance from prior visit: $300.00.\"),\n    (\"E11 PCP office visit note 01/16: outstanding ER balance\", \"Dr. Alvarez, office visit\", \"2026-01-16\",\n     \"Persistent neck pain 6/10. Outstanding balance from ER visit $6,240.00.\"),\n    (\"E12 PCP office visit note 01/16: MRI ordered, estimated charge\", \"Dr. Alvarez, office visit\", \"2026-01-16\",\n     \"MRI cervical spine ordered. Estimated MRI charge $2,150.00.\"),\n    (\"E13 PT visit 9 03/06: total PT charges (no 'visits' word)\", PTD, \"2026-03-06\",\n     \"Discharged from PT after two missed appointments. Total PT charges $1,665.00.\"),\n    (\"E14 PT visit 9 03/06: charges for the plan of care\", PTD, \"2026-03-06\",\n     \"Discharged from PT after two missed appointments. Charges for the plan of care: $1,665.00.\"),\n    (\"E15 PT visit 9 03/06: cumulative charges\", PTD, \"2026-03-06\",\n     \"Discharged. Cumulative charges $1,665.00.\"),\n    (\"E16 control PT visit 9: 'nine visits billed $1,665.00'\", PTD, \"2026-03-06\",\n     \"Discharged. Nine visits billed $1,665.00.\"),\n    (\"E17 PT visit 9 03/06: this visit + prior balance in a second sentence\", PTD, \"2026-03-06\",\n     \"Discharge visit charge $185.00. Prior balance $1,480.00.\"),\n    (\"E18 PT visit 9: 'nine sessions' word number\", PTD, \"2026-03-06\",\n     \"Discharged. Charge for nine sessions $1,665.00.\"),\n    (\"E19 PT visit 9: 'episode of care' total\", PTD, \"2026-03-06\",\n     \"Discharged. Episode of care total $1,665.00.\"),\n    (\"E20 late-entry office visit note dated 01/20, visit date in the previous sentence\", \"Dr. Alvarez, office visit\", \"2026-01-20\",\n     \"Late entry for visit of 01/16/2026. Office visit charge $150.00.\"),\n    (\"E21 PCP office visit note 01/16: 'charge for last week's ER visit'\", \"Dr. Alvarez, office visit\", \"2026-01-16\",\n     \"Patient asks about the charge for last week's ER visit, $6,240.00.\"),\n    (\"E22 ER discharge summary 01/09 control: ER charges\", ER, \"2026-01-09\",\n     \"Follow up with PCP in 1 week. ER charges: $6,240.\"),\n    (\"E23 PT visit 9 03/06: 'all PT charges' with 'visit' singular ('per visit' rate)\", PTD, \"2026-03-06\",\n     \"All PT charges at $185 per visit: $1,665.00.\"),\n    # T: bill tables\n    (\"T1 ledger: Posted column then DOS column\", \"Central ER, itemized ledger\", \"2026-02-05\",\n     \"Posted      DOS         Description           Amount\\n01/20/2026  01/09/2026  ER facility charge    $6,240.00\"),\n    (\"T2 ledger: DOS column then Paid On column\", \"Central ER, itemized ledger\", \"2026-03-05\",\n     \"DOS         Description           Charge      Paid On\\n01/09/2026  ER facility charge    $6,240.00   02/20/2026\"),\n    (\"T3 ledger: bare 'Date' column\", \"Central ER, itemized ledger\", \"2026-02-05\",\n     \"Date        Description           Amount\\n01/20/2026  ER facility charge    $6,240.00\"),\n    (\"T4 bill: summary line 'Date of service: X   Statement date: Y' then a posting row\", \"Central ER, billing statement\", \"2026-02-05\",\n     \"Date of service: 01/09/2026     Account: 4471\\n01/20/2026   ER facility charge   $6,240.00\"),\n    (\"T5 bill: 'Visit Date / Next Visit Date' columns\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Visit Date  Next Visit Date  CPT    Charge\\n02/02/2026  02/16/2026       99213  $275.00\"),\n    (\"T6 bill: DOS column, description holds an earlier date\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"DOS         CPT    Description                Charge\\n02/02/2026  99213  f/u of ER 01/09/2026      $275.00\"),\n    (\"T7 UB-04 FL45 'SERV DATE' column (not in the heading list)\", \"Saltmarrow General Hospital, UB-04\", \"2026-06-19\",\n     \"REV CD  DESCRIPTION   HCPCS  SERV DATE   UNITS  TOTAL CHARGES\\n0450    EMERGENCY RM  99285  06/09/2026  1      $2,105.00\"),\n    (\"T8 ledger: DOS heading two rows up, payment row between\", \"Central ER, itemized ledger\", \"2026-03-05\",\n     \"DOS         Description           Amount\\n01/09/2026  ER facility charge    $6,240.00\\n02/20/2026  Insurance payment     -$4,000.00\\n02/25/2026  Late fee              $25.00\"),\n    (\"T9 encounter note with a DOS table of earlier visits\", \"Dr. Alvarez, office visit\", \"2026-01-16\",\n     \"Prior visits reviewed:\\nDOS         Facility     Charge\\n01/09/2026  Central ER   $6,240.00\"),\n    # U: UB-04 spans\n    (\"U1 UB-04 monthly outpatient PT bill, statement period = billing month\", \"Capital PT, UB-04\", \"2026-04-02\",\n     \"UB-04. Statement covers period 03/01/2026 through 03/31/2026. Rev 0420 97110 therapeutic exercise, FL47 total charges $185.00.\"),\n    (\"U2 not UB: patient statement 'Statement period' with CPT line\", \"Capital PT, patient statement\", \"2026-04-02\",\n     \"Statement period 03/01/2026 through 03/31/2026. 97110 therapeutic exercise $185.00.\"),\n]\n\nstated = []\nfor label, src, rd, ex in OLD + NEW:\n    kind = KIND(src, ex) if KIND else \"n/a\"\n    print(f\"== {label}  (record date {rd}; source '{src}'; kind={kind}; billing_document={AM.billing_document(src, ex)})\")\n    print(\"   \" + ex.replace(\"\\n\", \"\\n   \"))\n    rec = {\"id\": \"r1\", \"n\": 1, \"source\": src, \"date_iso\": rd, \"excerpt\": ex, \"text\": ex}\n    for a in AM.find_amounts(ex):\n        if a.get(\"cents\") is None:\n            continue\n        item = {\"excerpt\": ex, \"value_cents\": a[\"cents\"], \"raw\": a[\"raw\"], \"excerpt_start\": 0}\n        d = store.charge_service_date(item, rec, a[\"start\"])\n        print(f\"   {a['raw']:>10} -> letter head: '{src}, {d['text']}: {a['raw']}'  state={d['state']} reason={d['reason']}\")\n        if d.get(\"confirm_note\"):\n            print(f\"              Step 3 note: {d['confirm_note']}\")\n        if d[\"state\"] == \"stated\":\n            stated.append((label, rd, kind, a[\"raw\"], d[\"text\"]))\nprint(f\"# total probes: {len(OLD)} old + {len(NEW)} new\")\nprint(f\"# STATED results ({len(stated)}): every other figure printed the blank\")\nfor s in stated:\n    print(\"   %s | record %s | kind=%s | %s -> %s\" % s)\n"
}
````

### User / tool · 2026-11-03T02:47:25.527Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/probe_r5.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:47:29.868Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/probe_r5.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf /Users/arsis/zlayt-pm-project > artifacts/review-evidence/T-202-paralegal-r5/probe_r5.out 2>&1; echo $?; grep -n \"^# \" artifacts/review-evidence/T-202-paralegal-r5/probe_r5.out; sed -n '/# STATED/,$p' artifacts/review-evidence/T-202-paralegal-r5/probe_r5.out",
 "description": "Run r5 probe against f9c0faf archive"
}
````

### User / tool · 2026-11-03T02:47:30.231Z

**tool result**
````
0
1:# loaded 38 probes from T-202-paralegal-r2/probe_r2.py
2:# loaded 12 probes from T-202-paralegal-r2/probe_r2b.py
3:# loaded 16 probes from T-202-paralegal-r3/probe_r3.py
4:# loaded 9 probes from T-202-paralegal-r3/probe_r3b.py
5:# loaded 7 probes from T-202-paralegal-r3/probe_r3c.py
6:# loaded 33 probes from T-202-paralegal-r4/probe_r4.py
639:# total probes: 115 old + 34 new
640:# STATED results (58): every other figure printed the blank
# STATED results (58): every other figure printed the blank
   probe_r2 P4 UB-04 period across months | record 2026-07-10 | kind=bill | $4,920.00 -> June 28–July 2, 2026
   probe_r2 P5 UB-04 period with 'through' | record 2026-06-19 | kind=bill | $2,105.00 -> June 9–12, 2026
   probe_r2 P6 UB-04 period with hyphen | record 2026-06-19 | kind=bill | $2,105.00 -> June 9–12, 2026
   probe_r2 P9 statement period then a separately dated line | record 2026-06-19 | kind=bill | $2,105.00 -> June 9–12, 2026
   probe_r2 T1 ledger table: DOS + posted columns | record 2026-07-01 | kind=bill | $70.00 -> June 10, 2026
   probe_r2 T1 ledger table: DOS + posted columns | record 2026-07-01 | kind=bill | $70.00 -> June 10, 2026
   probe_r2 T1 ledger table: DOS + posted columns | record 2026-07-01 | kind=bill | $95.00 -> June 17, 2026
   probe_r2 T1 ledger table: DOS + posted columns | record 2026-07-01 | kind=bill | $165.00 -> June 17, 2026
   probe_r2 T2 ledger table: posted column first (r1 blocker) | record 2026-07-01 | kind=bill | $70.00 -> June 10, 2026
   probe_r2 T2 ledger table: posted column first (r1 blocker) | record 2026-07-01 | kind=bill | $70.00 -> June 10, 2026
   probe_r2 T2 ledger table: posted column first (r1 blocker) | record 2026-07-01 | kind=bill | $95.00 -> June 17, 2026
   probe_r2 T2 ledger table: posted column first (r1 blocker) | record 2026-07-01 | kind=bill | $165.00 -> June 17, 2026
   probe_r2 N1 posted-first ledger, uppercase header, pipes | record 2026-07-01 | kind=bill | $70.00 -> June 10, 2026
   probe_r2 N1 posted-first ledger, uppercase header, pipes | record 2026-07-01 | kind=bill | $95.00 -> June 17, 2026
   probe_r2 N2 posted-first ledger, header 'Post Date / Date of Service' | record 2026-07-01 | kind=bill | $70.00 -> June 10, 2026
   probe_r2 N2 posted-first ledger, header 'Post Date / Date of Service' | record 2026-07-01 | kind=bill | $95.00 -> June 17, 2026
   probe_r2 N17 month-name period with year | record 2026-07-10 | kind=bill | $4,920.00 -> June 28–July 2, 2026
   probe_r2 N24 ledger: two posted dates then DOS in row, header names all | record 2026-07-01 | kind=bill | $70.00 -> June 10, 2026
   probe_r2 N25 ISO dates in a posted-first ledger | record 2026-07-01 | kind=bill | $70.00 -> June 10, 2026
   probe_r3 R6 ledger: DOS heading, but a DOB column before it | record 2026-07-01 | kind=bill | $70.00 -> June 10, 2026
   probe_r3 R7 ledger: 'Injury Date' column then 'Service Date' column | record 2026-07-01 | kind=bill | $70.00 -> June 10, 2026
   probe_r3b R20 ER note 01/09: seen on the same day (control, should be January 9) | record 2026-01-09 | kind=encounter | $6,240.00 -> January 9, 2026
   probe_r3c C1 ER 01/09: follow-up visit date, own sentence, then charge | record 2026-01-09 | kind=encounter | $6,240 -> January 9, 2026
   probe_r3c C2 ER 01/09: follow-up visit date, semicolon, then charge | record 2026-01-09 | kind=encounter | $6,240 -> January 9, 2026
   probe_r3c C5 PT eval 01/23: plan + next visit date + rate, sentences | record 2026-01-23 | kind=encounter | $185 -> January 23, 2026
   probe_r4 D2 ER note: 'Date of service.......01/09/2026' (brief text) then ER charges | record 2026-01-09 | kind=encounter | $6,240 -> January 9, 2026
   probe_r4 D3 ER note: leader DOS then charge in same clause | record 2026-01-09 | kind=encounter | $6,240 -> January 9, 2026
   probe_r4 S7 'Austin Imaging, cervical MRI' 06/20 (encounter label) but the excerpt is the bill | record 2026-06-20 | kind=encounter | $2,150.00 -> June 20, 2026
   probe_r4 T3 ER note 01/10 (summary written next day): arrived 01/09/2026 | record 2026-01-10 | kind=encounter | $6,240 -> January 10, 2026
   E1 'Open MRI of Austin' bill, no date in the charge sentence | record 2026-06-20 | kind=encounter | $2,150.00 -> June 20, 2026
   E2 'Austin MRI' bill, thank-you opening | record 2026-06-20 | kind=encounter | $2,150.00 -> June 20, 2026
   E3 'Austin MRI' bill, MRI date in the previous sentence | record 2026-06-20 | kind=encounter | $2,150.00 -> June 20, 2026
   E4 'Hill Country X-Ray' bill | record 2026-02-10 | kind=encounter | $240.00 -> February 10, 2026
   E5 'Westlake Follow-Up Clinic' bill | record 2026-03-01 | kind=encounter | $150.00 -> March 1, 2026
   E6 'Capital Evaluation Center' bill | record 2026-04-15 | kind=encounter | $900.00 -> April 15, 2026
   E7 'Express Exam Urgent Care' bill | record 2026-02-01 | kind=encounter | $310.00 -> February 1, 2026
   E8 'Austin Imaging, cervical MRI' (sample label) with a bill excerpt | record 2026-06-20 | kind=encounter | $2,150.00 -> June 20, 2026
   E10 ER discharge summary 01/09: balance from a prior visit | record 2026-01-09 | kind=encounter | $300.00 -> January 9, 2026
   E11 PCP office visit note 01/16: outstanding ER balance | record 2026-01-16 | kind=encounter | $6,240.00 -> January 16, 2026
   E12 PCP office visit note 01/16: MRI ordered, estimated charge | record 2026-01-16 | kind=encounter | $2,150.00 -> January 16, 2026
   E13 PT visit 9 03/06: total PT charges (no 'visits' word) | record 2026-03-06 | kind=encounter | $1,665.00 -> March 6, 2026
   E14 PT visit 9 03/06: charges for the plan of care | record 2026-03-06 | kind=encounter | $1,665.00 -> March 6, 2026
   E15 PT visit 9 03/06: cumulative charges | record 2026-03-06 | kind=encounter | $1,665.00 -> March 6, 2026
   E17 PT visit 9 03/06: this visit + prior balance in a second sentence | record 2026-03-06 | kind=encounter | $185.00 -> March 6, 2026
   E17 PT visit 9 03/06: this visit + prior balance in a second sentence | record 2026-03-06 | kind=encounter | $1,480.00 -> March 6, 2026
   E19 PT visit 9: 'episode of care' total | record 2026-03-06 | kind=encounter | $1,665.00 -> March 6, 2026
   E20 late-entry office visit note dated 01/20, visit date in the previous sentence | record 2026-01-20 | kind=encounter | $150.00 -> January 20, 2026
   E21 PCP office visit note 01/16: 'charge for last week's ER visit' | record 2026-01-16 | kind=encounter | $6,240.00 -> January 16, 2026
   E22 ER discharge summary 01/09 control: ER charges | record 2026-01-09 | kind=encounter | $6,240 -> January 9, 2026
   T1 ledger: Posted column then DOS column | record 2026-02-05 | kind=bill | $6,240.00 -> January 9, 2026
   T2 ledger: DOS column then Paid On column | record 2026-03-05 | kind=bill | $6,240.00 -> January 9, 2026
   T4 bill: summary line 'Date of service: X   Statement date: Y' then a posting row | record 2026-02-05 | kind=bill | $6,240.00 -> January 20, 2026
   T6 bill: DOS column, description holds an earlier date | record 2026-03-01 | kind=bill | $275.00 -> February 2, 2026
   T8 ledger: DOS heading two rows up, payment row between | record 2026-03-05 | kind=bill | $6,240.00 -> January 9, 2026
   T8 ledger: DOS heading two rows up, payment row between | record 2026-03-05 | kind=bill | $4,000.00 -> February 20, 2026
   T8 ledger: DOS heading two rows up, payment row between | record 2026-03-05 | kind=bill | $25.00 -> February 25, 2026
   T9 encounter note with a DOS table of earlier visits | record 2026-01-16 | kind=encounter | $6,240.00 -> January 9, 2026
   U1 UB-04 monthly outpatient PT bill, statement period = billing month | record 2026-04-02 | kind=bill | $185.00 -> March 1–31, 2026
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:47:56.523Z

**tool call — Bash**
````
{
 "command": "cat evals/golden/sample.txt; echo ----; cat evals/golden/case_09_nonvisit_hides_gap.txt",
 "description": "Read sample and case_09 golden texts"
}
````

### User / tool · 2026-11-03T02:47:56.605Z

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

----
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
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:48:09.874Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p $S/pr5_ad0d91a && git archive ad0d91a | tar -x -C $S/pr5_ad0d91a && git diff --stat ad0d91a f9c0faf -- app evals | tail -3",
 "description": "Extract parent ad0d91a archive for comparison"
}
````

### User / tool · 2026-11-03T02:48:11.032Z

**tool result**
````
 app/backend/store.py             |  14 +--
 evals/letter_check.py            | 152 +++++++++++++++-----------
 5 files changed, 217 insertions(+), 214 deletions(-)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:48:17.645Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/corpus_blanks.py",
 "content": "\"\"\"T-202 r5 paralegal: every BILLED CHARGES line (all_accepted and counted variants, standard style) of the 25 letter_check cases, with the record it quotes,\nand a per-case count of dated lines vs fillable blanks. Run on the f9c0faf archive and on the parent ad0d91a archive to see what D-073 turned into blanks.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/corpus_blanks.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nos.environ.setdefault(\"LLM_BACKEND\", \"fixture\")\nos.environ.setdefault(\"FIXTURE_SET\", \"curated\")\nfrom evals import letter_check as LC  # noqa: E402\n\nBL = \"[__________]\"\nnorm = lambda t: \" \".join(str(t).split())\ntot = {\"lines\": 0, \"blank\": 0}\nfor name, text in LC.cases():\n    got = LC.letters_for(text)\n    for variant in (\"all_accepted\", \"counted\"):\n        if variant not in got:\n            continue\n        v = got[variant]\n        lines = LC.charge_lines(v[\"letters\"][\"standard\"])\n        nb = sum(1 for h, q in lines if BL in h)\n        if variant == \"all_accepted\":\n            tot[\"lines\"] += len(lines)\n            tot[\"blank\"] += nb\n        print(f\"== {name} {variant}: {len(lines)} charge line(s), {nb} blank, {len(lines) - nb} dated; refused={v.get('refused')}\")\n        for h, q in lines:\n            recs = [r for r in v.get(\"records\", []) if norm(q) in norm(r.get(\"excerpt\", \"\"))]\n            r = recs[0] if recs else {}\n            print(f\"   {h}\\n      quote: {q}\\n      record {r.get('n')} [{r.get('date_iso')}] {r.get('source')}\")\nprint(f\"# all_accepted totals: {tot['lines']} charge lines, {tot['blank']} blank, {tot['lines'] - tot['blank']} dated\")\n"
}
````

### User / tool · 2026-11-03T02:48:17.743Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/corpus_blanks.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:48:22.872Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/corpus_blanks.py $S/pr5_f9c0faf > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/corpus_blanks_f9c0faf.out 2>&1; PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/corpus_blanks.py $S/pr5_ad0d91a > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/corpus_blanks_ad0d91a.out 2>&1; cd artifacts/review-evidence/T-202-paralegal-r5 && grep \"^#\\|^== .*all_accepted\" corpus_blanks_f9c0faf.out; tail -1 corpus_blanks_ad0d91a.out",
 "description": "Count corpus charge lines dated vs blank on both builds",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:48:43.231Z

**tool result**
````
== sample all_accepted: 2 charge line(s), 0 blank, 2 dated; refused=[]
== case_01_date_formats all_accepted: 1 charge line(s), 1 blank, 0 dated; refused=[('e8', 'DATE_UNCONFIRMED')]
== case_02_gap_boundaries all_accepted: 0 charge line(s), 0 blank, 0 dated; refused=[]
== case_03_rate_and_ocr all_accepted: 2 charge line(s), 1 blank, 1 dated; refused=[('e2', 'CHARGE_TEXT_IN_ENTRY'), ('a2', 'COMPARE_REQUIRED')]
== case_04_duplicates_no_amounts all_accepted: 0 charge line(s), 0 blank, 0 dated; refused=[]
== case_05_provider_conflict all_accepted: 1 charge line(s), 1 blank, 0 dated; refused=[]
== case_06_subtle_pre_existing all_accepted: 0 charge line(s), 0 blank, 0 dated; refused=[]
== case_07_prompt_injection all_accepted: 1 charge line(s), 1 blank, 0 dated; refused=[('a2', 'COMPARE_REQUIRED')]
== case_08_diagnosis_temptation all_accepted: 1 charge line(s), 0 blank, 1 dated; refused=[]
== case_09_nonvisit_hides_gap all_accepted: 1 charge line(s), 1 blank, 0 dated; refused=[('e2', 'CHARGE_TEXT_IN_ENTRY')]
== case_lib01_er_only_then_gap all_accepted: 1 charge line(s), 1 blank, 0 dated; refused=[]
== case_lib02_slip_fall_prior_knee all_accepted: 2 charge line(s), 1 blank, 1 dated; refused=[('e4', 'SUMMARY_TOKEN_NOT_IN_EXCERPT')]
== case_lib03_truck_rear_end_chiro all_accepted: 2 charge line(s), 1 blank, 1 dated; refused=[('f_r7_1', 'COMPARE_REQUIRED'), ('f_r7_2', 'COMPARE_REQUIRED')]
== case_lib04_dog_bite_scar_revision all_accepted: 1 charge line(s), 1 blank, 0 dated; refused=[('a3', 'COMPARE_REQUIRED')]
== case_lib05_pedestrian_orif_hardware all_accepted: 1 charge line(s), 1 blank, 0 dated; refused=[('a3', 'COMPARE_REQUIRED')]
== case_lib06_lop_billed_vs_adjusted all_accepted: 2 charge line(s), 1 blank, 1 dated; refused=[('e4', 'CHARGE_TEXT_IN_ENTRY'), ('e5', 'SUMMARY_TOKEN_NOT_IN_EXCERPT'), ('a2', 'COMPARE_REQUIRED'), ('a3', 'COMPARE_REQUIRED'), ('a4', 'COMPARE_REQUIRED'), ('a7', 'COMPARE_REQUIRED')]
== case_lib07_parking_lot_fall_outside_records all_accepted: 2 charge line(s), 1 blank, 1 dated; refused=[]
== case_lib08_second_crash_mri_after all_accepted: 3 charge line(s), 2 blank, 1 dated; refused=[('f_r12_1', 'COMPARE_REQUIRED')]
== case_lib09_spanish_interpreter_espalda all_accepted: 2 charge line(s), 1 blank, 1 dated; refused=[('e7', 'CHARGE_TEXT_IN_ENTRY'), ('e4', 'DATE_UNCONFIRMED'), ('a2', 'COMPARE_REQUIRED'), ('a5', 'COMPARE_REQUIRED'), ('a7', 'COMPARE_REQUIRED')]
== case_lib10_eob_ub04_cms1500 all_accepted: 4 charge line(s), 0 blank, 4 dated; refused=[('e1', 'COMPARE_REQUIRED'), ('e4', 'COMPARE_REQUIRED'), ('e8', 'CHARGE_TEXT_IN_ENTRY'), ('a6', 'COMPARE_REQUIRED'), ('a7', 'COMPARE_REQUIRED'), ('a9', 'COMPARE_REQUIRED'), ('a11', 'COMPARE_REQUIRED')]
== case_lib11_priors_and_ledger all_accepted: 1 charge line(s), 1 blank, 0 dated; refused=[('e1', 'COMPARE_REQUIRED'), ('e2', 'COMPARE_REQUIRED'), ('e4', 'COMPARE_REQUIRED'), ('e9', 'CHARGE_TEXT_IN_ENTRY'), ('a2', 'COMPARE_REQUIRED'), ('a3', 'COMPARE_REQUIRED'), ('a4', 'COMPARE_REQUIRED'), ('a5', 'COMPARE_REQUIRED'), ('a6', 'COMPARE_REQUIRED'), ('a8', 'COMPARE_REQUIRED')]
== case_lib12_records_review_credibility all_accepted: 1 charge line(s), 1 blank, 0 dated; refused=[('e10', 'CHARGE_TEXT_IN_ENTRY'), ('a2', 'COMPARE_REQUIRED'), ('a3', 'COMPARE_REQUIRED'), ('a4', 'COMPARE_REQUIRED')]
== case_lib13_cloned_notes_cross_provider all_accepted: 2 charge line(s), 1 blank, 1 dated; refused=[]
== case_lib14_handwritten_chiro_scans all_accepted: 3 charge line(s), 3 blank, 0 dated; refused=[('e7', 'CHARGE_TEXT_IN_ENTRY'), ('e8', 'CHARGE_TEXT_IN_ENTRY'), ('e5', 'DATE_UNCONFIRMED'), ('a5', 'COMPARE_REQUIRED')]
== case_lib15_conclusory_letter_mist all_accepted: 1 charge line(s), 1 blank, 0 dated; refused=[('e7', 'CHARGE_TEXT_IN_ENTRY'), ('e9', 'CHARGE_TEXT_IN_ENTRY'), ('a3', 'COMPARE_REQUIRED'), ('a4', 'COMPARE_REQUIRED'), ('a5', 'COMPARE_REQUIRED'), ('a6', 'COMPARE_REQUIRED'), ('a8', 'COMPARE_REQUIRED'), ('a9', 'COMPARE_REQUIRED'), ('a11', 'COMPARE_REQUIRED')]
# all_accepted totals: 37 charge lines, 22 blank, 15 dated
# all_accepted totals: 37 charge lines, 0 blank, 37 dated
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:48:47.648Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5 && diff <(grep -v \"^#\" corpus_blanks_ad0d91a.out) <(grep -v \"^#\" corpus_blanks_f9c0faf.out) > corpus_blanks.diff; grep -c \"^>\" corpus_blanks.diff; awk '/all_accepted/{p=1} /counted/{p=0} p' corpus_blanks_f9c0faf.out | grep -B0 -A2 \"^   [^ ]\" | grep -v \"^--\" | head -120",
 "description": "Diff corpus lines and list f9c0faf all_accepted lines"
}
````

### User / tool · 2026-11-03T02:48:47.768Z

**tool result**
````
82
   Central ER discharge summary, January 9, 2026: $6,240.00
      quote: ER charges: $6,240.
      record 2 [2026-01-09] Central ER discharge summary
   Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
      quote: Charge: $2,150.
      record 8 [2026-05-29] Austin Imaging, cervical MRI
   Quillfeather Urgent Care, date of service [__________] (statement dated February 3, 2026): $310.00
      quote: Urgent care charge: $310.00.
      record 1 [2026-02-03] Quillfeather Urgent Care
   Gloamwood Chiropractic, visit 2, August 17, 2026: $95.00
      quote: Charge: $95.00.
      record 3 [2026-08-17] Gloamwood Chiropractic, visit 2
   Dr. Hobart Wimbleton, radiology, date of service [__________] (statement dated September 2, 2026): $240.00
      quote: Radiology charge: $240.
      record 5 [2026-09-02] Dr. Hobart Wimbleton, radiology
   Thornapple Valley Hospital ED, date of service [__________] (statement dated June 1, 2026): $4,380.00
      quote: ED charge: $4,380.
      record 2 [2026-06-01] Thornapple Valley Hospital ED
   Bumblethorpe Urgent Care, date of service [__________] (statement dated March 2, 2026): $420.00
      quote: Charge: $420.
      record 1 [2026-03-02] Bumblethorpe Urgent Care
   Tumblebrook Imaging, shoulder MRI, October 20, 2026: $1,875.00
      quote: Charge: $1,875.
      record 2 [2026-10-20] Tumblebrook Imaging, shoulder MRI
   Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00
      quote: Statement for visit of 2026-02-02: $275.
      record 2 [2026-03-01] Hobbleton Family Clinic, billing statement
   Marrowgate General ED, date of service [__________] (statement dated February 14, 2026): $3,915.00
      quote: ED charge: $3,915.
      record 2 [2026-02-14] Marrowgate General ED
   Tamsin Valley Urgent Care, date of service [__________] (statement dated March 9, 2026): $410.00
      quote: Visit charge: $410.
      record 2 [2026-03-09] Tamsin Valley Urgent Care
   Tamsin Imaging, right knee MRI, March 30, 2026: $1,850.00
      quote: MRI charge: $1,850.
      record 4 [2026-03-30] Tamsin Imaging, right knee MRI
   Redhaven Regional ED, date of service [__________] (statement dated April 6, 2026): $5,260.00
      quote: ED charge: $5,260.
      record 2 [2026-04-06] Redhaven Regional ED
   Redhaven Imaging, lumbar MRI, July 20, 2026: $2,240.00
      quote: MRI charge: $2,240.
      record 7 [2026-07-20] Redhaven Imaging, lumbar MRI
   Harlow Memorial ED, date of service [__________] (statement dated September 13, 2025): $4,730.00
      quote: ED charge: $4,730.
      record 2 [2025-09-13] Harlow Memorial ED
   Coldharbor Trauma Center ED, date of service [__________] (statement dated January 22, 2026): $38,420.00
      quote: ED charges: $38,420.
      record 2 [2026-01-22] Coldharbor Trauma Center ED
   Larchmont Ridge ED, date of service [__________] (statement dated May 2, 2026): $2,880.00
      quote: ED charge: $2,880.
      record 2 [2026-05-02] Larchmont Ridge ED
   Larchmont Ridge Imaging, right shoulder MRI, June 17, 2026: $2,400.00
      quote: Charge: $2,400.
      record 5 [2026-06-17] Larchmont Ridge Imaging, right shoulder MRI
   Cobblestone Imaging, date of service [__________] (statement dated February 10, 2026): $640.00
      quote: Charge: $640.
      record 2 [2026-02-10] Cobblestone Imaging
   Cobblestone Imaging, lumbar MRI, May 12, 2026: $1,980.00
      quote: MRI charge: $1,980.
      record 6 [2026-05-12] Cobblestone Imaging, lumbar MRI
   Thornbury Regional ED, date of service [__________] (statement dated January 12, 2026): $4,210.00
      quote: ED charge: $4,210.
      record 2 [2026-01-12] Thornbury Regional ED
   Thornbury Regional ED, date of service [__________] (statement dated April 24, 2026): $4,680.00
      quote: ED charge: $4,680.
      record 9 [2026-04-24] Thornbury Regional ED
   Valley Imaging, cervical MRI, May 20, 2026: $2,350.00
      quote: MRI charge: $2,350.
      record 10 [2026-05-20] Valley Imaging, cervical MRI
   Quillmere Regional ED, date of service [__________] (statement dated March 3, 2026): $2,940.00
      quote: ED charge: $2,940.
      record 1 [2026-03-03] Quillmere Regional ED
   Cinder Valley Imaging, right shoulder MRI, May 5, 2026: $2,150.00
      quote: MRI charge: $2,150.
      record 5 [2026-05-05] Cinder Valley Imaging, right shoulder MRI
   Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $4,920.00
      quote: FL47 total charges $4,920.00.
      record 4 [2026-06-19] Saltmarrow General Hospital, UB-04 itemized bill
   Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $2,105.00
      quote: Rev 0450 emergency room, 1 unit, FL47 total charges $2,105.00.
      record 4 [2026-06-19] Saltmarrow General Hospital, UB-04 itemized bill
   Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $386.50
      quote: Rev 0250 pharmacy, 14 units, FL47 total charges $386.50.
      record 4 [2026-06-19] Saltmarrow General Hospital, UB-04 itemized bill
   Saltmarrow General Hospital, UB-04 itemized bill, June 9–12, 2026: $712.00
      quote: Rev 0300 laboratory, 6 units, FL47 total charges $712.00.
      record 4 [2026-06-19] Saltmarrow General Hospital, UB-04 itemized bill
   Wexcombe Memorial ED, date of service [__________] (statement dated March 18, 2026): $3,260.00
      quote: ED charge: $3,260.
      record 3 [2026-03-18] Wexcombe Memorial ED
   Orrin Vale Community ED, date of service [__________] (statement dated February 9, 2026): $2,780.00
      quote: ED charge: $2,780.
      record 2 [2026-02-09] Orrin Vale Community ED
   Vessel Grove Medical Center ED, date of service [__________] (statement dated August 3, 2026): $3,540.00
      quote: ED charge: $3,540.
      record 2 [2026-08-03] Vessel Grove Medical Center ED
   Vessel Grove Imaging, lumbar MRI, August 28, 2026: $2,290.00
      quote: MRI charge: $2,290.
      record 6 [2026-08-28] Vessel Grove Imaging, lumbar MRI
   Orrin Mere Regional ED, date of service [__________] (statement dated September 14, 2026): $2,960.00
      quote: ED charge: $2,960.
      record 2 [2026-09-14] Orrin Mere Regional ED
   Tarnwick Fire-Rescue, ambulance invoice, date of service [__________] (statement dated November 12, 2026): $1,380.00
      quote: A0427 ALS emergency transport, 1 unit, charge $1,380.00.
      record 8 [2026-11-12] Tarnwick Fire-Rescue, ambulance invoice
   Tarnwick Fire-Rescue, ambulance invoice, date of service [__________] (statement dated November 12, 2026): $187.05
      quote: charge $187.05.
      record 8 [2026-11-12] Tarnwick Fire-Rescue, ambulance invoice
   Cobblewood Urgent Care, date of service [__________] (statement dated October 5, 2026): $385.00
      quote: Charge: $385.
      record 2 [2026-10-05] Cobblewood Urgent Care
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:49:24.262Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5 && python3 - <<'EOF'\np = \"letters_dump_r5.py\"\nsrc = open(\"letters_dump_r4.py\").read()\nsrc = src.replace('\"\"\"T-202 r4 paralegal: in-process letters', '\"\"\"T-202 r5 paralegal (copied from r4, D-073 variants added): in-process letters')\nsrc = src.replace(\"T-202-paralegal-r4/letters_dump_r4.py\", \"T-202-paralegal-r5/letters_dump_r5.py\")\nadd = '''    # round 5 (D-073 from its opposite side): provider names that hold an encounter word, on a bill\n    \"synth_sample_mri_bill_provider_name\": sub(sub(SAMPLE, \"correlate clinically. Charge: $2,150.\", \"correlate clinically.\"), \"Patient states symptoms began after the January collision.\\\\\"\",\n        \"Patient states symptoms began after the January collision.\\\\\"\\\\n\\\\n=== Record 10 ===\\\\nDate: 2026-06-20\\\\nSource: Austin MRI\\\\nExcerpt: \\\\\"Cervical spine MRI performed 05/29/2026, CPT 72141. Amount due $2,150.\\\\\"\"),\n    \"synth_case09_followup_clinic_bill\": sub(C09, C09_R2, 'Date: 2026-03-01\\\\nSource: Hobbleton Follow-Up Clinic\\\\nExcerpt: \"Office visit 99213 on 2026-02-02. Amount due $275.\"'),\n    \"synth_case09_xray_bill\": sub(C09, C09_R2, 'Date: 2026-03-01\\\\nSource: Hobbleton X-Ray\\\\nExcerpt: \"Wrist x-ray, 3 views, CPT 73110, performed 2026-02-02. Patient responsibility $275.\"'),\n    # round 5: several visits' charges in one visit note, no 'visits' word in the charge sentence\n    \"synth_sample_pt_total\": sub(SAMPLE, \"Discharged from PT after two missed appointments. Pain 3/10.\", \"Discharged from PT after two missed appointments. Pain 3/10. Total PT charges $1,665.\"),\n    \"synth_sample_pt_plan_total\": sub(SAMPLE, \"Discharged from PT after two missed appointments. Pain 3/10.\", \"Discharged from PT after two missed appointments. Pain 3/10. Charges for the plan of care: $1,665.\"),\n    # round 5: another visit's balance, or a future service's price, inside a visit note\n    \"synth_sample_followup_prior_balance\": sub(SAMPLE, \"Patient states symptoms began after the January collision.\", \"Patient states symptoms began after the January collision. Balance from prior visit: $350.\"),\n    \"synth_sample_er_prior_balance\": sub(SAMPLE, \"ER charges: $6,240.\", \"ER charges: $6,240. Balance from prior ER visit in 2025: $300.\"),\n    \"synth_sample_followup_injection_quote\": sub(SAMPLE, \"Recommend cervical epidural steroid injection.\", \"Recommend cervical epidural steroid injection. Injection charge will be $1,800.\"),\n}\n'''\nsrc = src.replace('    \"synth_case09_provider_only_bill\": sub(C09, C09_R2, \\'Date: 2026-03-01\\\\nSource: Hobbleton Family Clinic\\\\nExcerpt: \"Amount due $275.00 for office visit on 02/02/2026.\"\\'),\\n}\\n',\n                  '    \"synth_case09_provider_only_bill\": sub(C09, C09_R2, \\'Date: 2026-03-01\\\\nSource: Hobbleton Family Clinic\\\\nExcerpt: \"Amount due $275.00 for office visit on 02/02/2026.\"\\'),\\n' + add)\nassert add in src\nopen(p, \"w\").write(src)\nEOF\ngrep -n \"synth_sample_mri_bill_provider_name\" -A2 letters_dump_r5.py",
 "description": "Create letters_dump_r5.py with round 5 variants"
}
````

### User / tool · 2026-11-03T02:49:24.369Z

**tool result**
````
49:    "synth_sample_mri_bill_provider_name": sub(sub(SAMPLE, "correlate clinically. Charge: $2,150.", "correlate clinically."), "Patient states symptoms began after the January collision.\"",
50-        "Patient states symptoms began after the January collision.\"\n\n=== Record 10 ===\nDate: 2026-06-20\nSource: Austin MRI\nExcerpt: \"Cervical spine MRI performed 05/29/2026, CPT 72141. Amount due $2,150.\""),
51-    "synth_case09_followup_clinic_bill": sub(C09, C09_R2, 'Date: 2026-03-01\nSource: Hobbleton Follow-Up Clinic\nExcerpt: "Office visit 99213 on 2026-02-02. Amount due $275."'),
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:49:30.180Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/letters_dump_r5.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/letters > artifacts/review-evidence/T-202-paralegal-r5/letters_dump_r5.out 2>&1; echo $?; cat artifacts/review-evidence/T-202-paralegal-r5/letters_dump_r5.out",
 "description": "Run in-process letters for corpus and variants",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:49:37.241Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:49:39.545Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5 && grep -v \"^llm call failed\" letters_dump_r5.out | grep -v \"^    .*| \" | head -5; grep -v \"^llm call failed\" letters_dump_r5.out | grep \"^== \\|^    [^ ].*|\\|violations\" | grep -A8 \"synth_\" | grep -v \"^--\" | head -150",
 "description": "Show variant charge lines and violations"
}
````

### User / tool · 2026-11-03T02:49:39.648Z

**tool result**
````
== sample all_accepted: cents=[624000, 215000] refused=[] gate={}
    date violations: []
== sample counted: cents=[624000, 215000] refused=[] gate={}
    date violations: []
== case_09 all_accepted: cents=[27500] refused=[('e2', 'CHARGE_TEXT_IN_ENTRY')] gate={}
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
    Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240.00 | ER charges: $6,240, next visit date 01/16/2026.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_next_visit counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240.00 | ER charges: $6,240, next visit date 01/16/2026.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_dotted_leader all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_dotted_leader counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_case09_bill_dotted_leader all_accepted: cents=[27500] refused=[] gate={}
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | $275.00
    date violations: []
== synth_case09_bill_dotted_leader counted: cents=[27500] refused=[] gate={}
    Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00 | $275.00
    date violations: []
== synth_sample_pcp_er_dos all_accepted: cents=[624000, 15000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Dr. Alvarez, primary care, date of service [__________] (statement dated January 16, 2026): $150.00 | Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pcp_er_dos counted: cents=[624000, 15000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Dr. Alvarez, primary care, date of service [__________] (statement dated January 16, 2026): $150.00 | Reviewed ER records, DOS 01/09/2026, office visit charge $150.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pt_treatment_dates all_accepted: cents=[624000, 166500, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $1,665.00 | Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pt_treatment_dates counted: cents=[624000, 166500, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $1,665.00 | Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_case09_provider_only_bill all_accepted: cents=[] refused=[] gate={}
    date violations: []
== synth_case09_provider_only_bill counted: cents=[] refused=[] gate={}
    date violations: []
== synth_sample_mri_bill_provider_name all_accepted: cents=[624000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    date violations: []
== synth_sample_mri_bill_provider_name counted: cents=[624000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    date violations: []
== synth_case09_followup_clinic_bill all_accepted: cents=[] refused=[] gate={}
    date violations: []
== synth_case09_followup_clinic_bill counted: cents=[] refused=[] gate={}
    date violations: []
== synth_case09_xray_bill all_accepted: cents=[] refused=[] gate={}
    date violations: []
== synth_case09_xray_bill counted: cents=[] refused=[] gate={}
    date violations: []
== synth_sample_pt_total all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pt_total counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pt_plan_total all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_pt_plan_total counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_followup_prior_balance all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_followup_prior_balance counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_prior_balance all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_er_prior_balance counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_followup_injection_quote all_accepted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
== synth_sample_followup_injection_quote counted: cents=[624000, 215000] refused=[] gate={}
    Central ER discharge summary, January 9, 2026: $6,240.00 | ER charges: $6,240.
    Austin Imaging, cervical MRI, May 29, 2026: $2,150.00 | Charge: $2,150.
    date violations: []
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:49:45.652Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/letters && for f in synth_sample_mri_bill_provider_name synth_case09_followup_clinic_bill synth_case09_xray_bill synth_sample_pt_total synth_sample_pt_plan_total synth_sample_followup_prior_balance synth_sample_er_prior_balance synth_sample_followup_injection_quote synth_case09_provider_only_bill; do echo \"### $f\"; grep -n \"1,665\\|2,150\\|275\\|350\\|300\\|1,800\" $f-all_accepted-notes.txt; done",
 "description": "Check how variant figures are classified in notes"
}
````

### User / tool · 2026-11-03T02:49:45.786Z

**tool result**
````
### synth_sample_mri_bill_provider_name
20:- Record 10 (Austin MRI, June 20, 2026): "Amount due $2,150." Not totaled ($2,150): Balance or amount due: worked out from charges, payments and adjustments, not a charge.
### synth_case09_followup_clinic_bill
15:- Record 2 (Hobbleton Follow-Up Clinic, March 1, 2026): "Amount due $275." Not totaled ($275): Balance or amount due: worked out from charges, payments and adjustments, not a charge.
### synth_case09_xray_bill
15:- Record 2 (Hobbleton X-Ray, March 1, 2026): "Patient responsibility $275." Not totaled ($275): Balance or amount due: worked out from charges, payments and adjustments, not a charge.
### synth_sample_pt_total
20:- Record 6 (Capital PT, visit 9, March 6, 2026): "Total PT charges $1,665." Not totaled ($1,665): The sentence names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized charge and is not totaled.
### synth_sample_pt_plan_total
20:- Record 6 (Capital PT, visit 9, March 6, 2026): "Charges for the plan of care: $1,665." Amount unclear ($1,665). Request clean copy of bill.
### synth_sample_followup_prior_balance
20:- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Balance from prior visit: $350." Not totaled ($350): Previous statement or balance carried forward: charges already listed on an earlier statement, not a new charge.
### synth_sample_er_prior_balance
19:- Record 2 (Central ER discharge summary, January 9, 2026): "Balance from prior ER visit in 2025: $300." Amount unclear ($300). Request clean copy of bill.
### synth_sample_followup_injection_quote
20:- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Injection charge will be $1,800." Amount unclear ($1,800). Request clean copy of bill.
### synth_case09_provider_only_bill
15:- Record 2 (Hobbleton Family Clinic, March 1, 2026): "Amount due $275.00 for office visit on 02/02/2026." Not totaled ($275.00): Balance or amount due: worked out from charges, payments and adjustments, not a charge.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:49:51.779Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf && grep -n \"counted\" evals/letter_check.py | head -20",
 "description": "Find counted variant logic in letter_check"
}
````

### User / tool · 2026-11-03T02:49:51.865Z

**tool result**
````
4:  run the pipeline on a scratch database, accept every item that code lets her accept (a refusal is counted, not hidden), export the letter in both styles;
526:    for variant, dismiss in (("all_accepted", False), ("charges_dismissed", True), ("counted", False)):
532:            if variant == "counted":
571:        for style, letter in got["counted"]["letters"].items():
572:            bad += [f"{style} (counted): {v}" for v in violations(letter, got["counted"]["charge_cents"])]
573:        for variant in ("all_accepted", "charges_dismissed", "counted"):      # T-208: no AI or model wording in any letter, of any kind of case
576:        for variant in ("all_accepted", "counted"):
579:        for variant in ("all_accepted", "charges_dismissed", "counted"):
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:49:56.756Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf && sed -n 515,560p evals/letter_check.py; grep -n \"def count_\\|\\\"count\\\"\\|counted_by\\|def set_count\\|/count\" app/backend/store.py app/backend/api.py | head",
 "description": "Read letters_for counted handling and count API"
}
````

### User / tool · 2026-11-03T02:49:56.851Z

**tool result**
````
                problems.append("the line prints a date no source ties to it" + (f" (the source gives {want[0]})" if want else ""))
        if len(problems) == len(recs):
            out.append(f"charge line's date is not certain from its quote ({'; '.join(sorted(set(problems)))}): {head}")
    return out


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
                        "charge_cents": cents, "refused": refused, "records": case["records"], "dismissed_providers": dismissed, "gate": gate,
                        "prepared": bool(case.get("prepared")),
                        "translated_quotes": [e["excerpt"] for e in case["entries"] if e.get("translation_label") == "AI translation"]}      # T-208: the case kind, so a report can say how many prepared and live letters were scanned
    return out


def dismissed_in_bills(notes: str, providers) -> list:
    """Providers whose charge was dismissed that the notes still list under BILLS TO REQUEST."""
    sec = notes.split("BILLS TO REQUEST")[1].split("RECORDS NOT IN THE TREATMENT SECTION")[0] if "BILLS TO REQUEST" in notes else ""
    listed = [re.sub(r"\s*\(itemized ledger\)$", "", x.strip().rstrip(".")) for x in sec.split("\n", 2)[-1].lstrip("- ").split(";")]
    return [p for p in providers if p in listed]


app/backend/api.py:625:            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:50:28.224Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.py",
 "content": "\"\"\"T-202 r5 paralegal: round 5 D-073 shapes through the FULL case pipeline and the letter (evals.letter_check.letters_for: fixture backend, every item accepted,\n'counted' variant counts what the paralegal may count), on SYNTHETIC variants of the Appendix A sample (record 6 = Capital PT, visit 9, 2026-03-06) and of\ncase_09 (record 2 = the clinic bill, 2026-03-01). Prints every BILLED CHARGES line, letter_check.charge_date_violations, and the notes line for the probe figure.\n    .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.py <archive_root>\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.chdir(root)\nos.environ.setdefault(\"LLM_BACKEND\", \"fixture\")\nos.environ.setdefault(\"FIXTURE_SET\", \"curated\")\nimport logging  # noqa: E402\nlogging.disable(logging.CRITICAL)\nfrom evals import letter_check as LC  # noqa: E402\n\nSAMPLE = open(\"evals/golden/sample.txt\").read()\nC09 = open(\"evals/golden/case_09_nonvisit_hides_gap.txt\").read()\nC09_R2 = 'Date: 2026-03-01\\nSource: Hobbleton Family Clinic, billing statement\\nExcerpt: \"Statement for visit of 2026-02-02: $275.\"'\nPT9 = \"Discharged from PT after two missed appointments. Pain 3/10.\"\nMRI8 = \"correlate clinically. Charge: $2,150.\"\nTAIL = 'Patient states symptoms began after the January collision.\"'\n\n\ndef pt9(extra):\n    assert PT9 in SAMPLE\n    return SAMPLE.replace(PT9, PT9 + \" \" + extra)\n\n\ndef c09(src, ex, date=\"2026-03-01\"):\n    assert C09_R2 in C09\n    return C09.replace(C09_R2, f'Date: {date}\\nSource: {src}\\nExcerpt: \"{ex}\"')\n\n\ndef mri_bill(src, ex, date=\"2026-06-20\"):\n    s = SAMPLE.replace(MRI8, \"correlate clinically.\")\n    return s.replace(TAIL, TAIL + f'\\n\\n=== Record 10 ===\\nDate: {date}\\nSource: {src}\\nExcerpt: \"{ex}\"')\n\n\nCASES = {\n    # provider names that hold an encounter word (MRI, X-Ray, Follow-Up, Evaluation, Exam), on a bill dated after the service; the service date is in the bill\n    \"m1_austin_mri_bill\": (\"2,150\", mri_bill(\"Austin MRI\", \"Date of service 05/29/2026. Cervical spine MRI, CPT 72141, charge $2,150.\")),\n    \"m2_open_mri_bill\": (\"2,150\", mri_bill(\"Open MRI of Austin\", \"Cervical spine MRI without contrast performed 05/29/2026. MRI charge: $2,150.\")),\n    \"m3_austin_mri_bill_no_date\": (\"2,150\", mri_bill(\"Austin MRI\", \"Cervical spine MRI, CPT 72141, charge $2,150.\")),\n    \"m4_control_austin_mri_billing_statement\": (\"2,150\", mri_bill(\"Austin MRI, billing statement\", \"Date of service 05/29/2026. Cervical spine MRI, CPT 72141, charge $2,150.\")),\n    \"c1_followup_clinic_bill\": (\"275\", c09(\"Hobbleton Follow-Up Clinic\", \"Date of service 2026-02-02. Office visit 99213 charge $275.\")),\n    \"c2_xray_bill\": (\"275\", c09(\"Hobbleton X-Ray\", \"Wrist x-ray performed 2026-02-02. Wrist x-ray 3 views, CPT 73110, charge $275.\")),\n    \"c3_evaluation_center_bill\": (\"275\", c09(\"Hobbleton Hand Evaluation Center\", \"Seen 2026-02-02. Hand evaluation 97165 charge $275.\")),\n    \"c4_exam_urgent_care_bill\": (\"275\", c09(\"Express Exam Urgent Care\", \"Visit 2026-02-02. Urgent care visit 99213 charge $275.\")),\n    # several visits' charges inside one visit note, with no 'visits'/'sessions'/'to date' word in the charge sentence\n    \"p1_pt_charges\": (\"1,665\", pt9(\"Physical therapy charges: $1,665.\")),\n    \"p2_pt_97110_total\": (\"1,665\", pt9(\"Therapeutic exercise 97110 charges: $1,665.\")),\n    \"p3_pt_course_charge\": (\"1,665\", pt9(\"PT course of care charge: $1,665.\")),\n    \"p4_pt_nine_attended\": (\"1,665\", pt9(\"Nine of 12 planned attended. PT charges: $1,665.\")),\n    \"p5_pt_since_01_23\": (\"1,665\", pt9(\"Treated since initial evaluation. PT charges: $1,665.\")),\n    \"p6_control_pt_9_visits\": (\"1,665\", pt9(\"PT charges for 9 visits: $1,665.\")),\n    \"p7_pt_this_visit_control\": (\"185\", pt9(\"Discharge visit charge $185.\")),\n}\nonly = os.environ.get(\"ONLY\")\nfor name, (fig, text) in CASES.items():\n    if only and name not in only.split(\",\"):\n        continue\n    got = LC.letters_for(text)\n    for variant in (\"all_accepted\", \"counted\"):\n        v = got[variant]\n        letter = v[\"letters\"][\"standard\"]\n        print(f\"== {name} {variant}: cents={v['charge_cents']}\")\n        for h, q in LC.charge_lines(letter):\n            print(\"   \", h, \"|\", q)\n        print(\"    date violations:\", LC.charge_date_violations(letter, v[\"records\"]))\n        for line in v[\"notes\"].splitlines():\n            if fig in line:\n                print(\"    notes:\", line)\n"
}
````

### User / tool · 2026-11-03T02:50:28.332Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:50:33.500Z

**tool call — Bash**
````
{
 "command": "PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf 2>&1 | grep -v \"^llm call failed\" > artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.out; grep -v \"Central ER discharge summary, January 9\\|cervical MRI, May 29\\|^    notes:.*Record 4\" artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.out",
 "description": "Run full-pipeline D-073 shape probes",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:50:38.540Z

**tool result**
````
== m1_austin_mri_bill all_accepted: cents=[624000, 215000]
    Austin MRI, June 20, 2026: $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
    date violations: []
== m1_austin_mri_bill counted: cents=[624000, 215000]
    Austin MRI, June 20, 2026: $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
    date violations: []
== m2_open_mri_bill all_accepted: cents=[624000, 215000]
    Open MRI of Austin, June 20, 2026: $2,150.00 | MRI charge: $2,150.
    date violations: []
== m2_open_mri_bill counted: cents=[624000, 215000]
    Open MRI of Austin, June 20, 2026: $2,150.00 | MRI charge: $2,150.
    date violations: []
== m3_austin_mri_bill_no_date all_accepted: cents=[624000, 215000]
    Austin MRI, June 20, 2026: $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
    date violations: []
== m3_austin_mri_bill_no_date counted: cents=[624000, 215000]
    Austin MRI, June 20, 2026: $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
    date violations: []
== m4_control_austin_mri_billing_statement all_accepted: cents=[624000, 215000]
    Austin MRI, billing statement, date of service [__________] (statement dated June 20, 2026): $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
    date violations: []
    notes: - Austin MRI, $2,150: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== m4_control_austin_mri_billing_statement counted: cents=[624000, 215000]
    Austin MRI, billing statement, date of service [__________] (statement dated June 20, 2026): $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
    date violations: []
    notes: - Austin MRI, $2,150: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
== c1_followup_clinic_bill all_accepted: cents=[27500]
    Hobbleton Follow-Up Clinic, March 1, 2026: $275.00 | Office visit 99213 charge $275.
    date violations: []
== c1_followup_clinic_bill counted: cents=[27500]
    Hobbleton Follow-Up Clinic, March 1, 2026: $275.00 | Office visit 99213 charge $275.
    date violations: []
== c2_xray_bill all_accepted: cents=[27500]
    Hobbleton X-Ray, March 1, 2026: $275.00 | Wrist x-ray 3 views, CPT 73110, charge $275.
    date violations: []
== c2_xray_bill counted: cents=[27500]
    Hobbleton X-Ray, March 1, 2026: $275.00 | Wrist x-ray 3 views, CPT 73110, charge $275.
    date violations: []
== c3_evaluation_center_bill all_accepted: cents=[27500]
    Hobbleton Hand Evaluation Center, March 1, 2026: $275.00 | Hand evaluation 97165 charge $275.
    date violations: []
== c3_evaluation_center_bill counted: cents=[27500]
    Hobbleton Hand Evaluation Center, March 1, 2026: $275.00 | Hand evaluation 97165 charge $275.
    date violations: []
== c4_exam_urgent_care_bill all_accepted: cents=[27500]
    Express Exam Urgent Care, March 1, 2026: $275.00 | Urgent care visit 99213 charge $275.
    date violations: []
== c4_exam_urgent_care_bill counted: cents=[27500]
    Express Exam Urgent Care, March 1, 2026: $275.00 | Urgent care visit 99213 charge $275.
    date violations: []
== p1_pt_charges all_accepted: cents=[624000, 166500, 215000]
    Capital PT, visit 9, March 6, 2026: $1,665.00 | Physical therapy charges: $1,665.
    date violations: []
== p1_pt_charges counted: cents=[624000, 166500, 215000]
    Capital PT, visit 9, March 6, 2026: $1,665.00 | Physical therapy charges: $1,665.
    date violations: []
== p2_pt_97110_total all_accepted: cents=[624000, 166500, 215000]
    Capital PT, visit 9, March 6, 2026: $1,665.00 | Therapeutic exercise 97110 charges: $1,665.
    date violations: []
== p2_pt_97110_total counted: cents=[624000, 166500, 215000]
    Capital PT, visit 9, March 6, 2026: $1,665.00 | Therapeutic exercise 97110 charges: $1,665.
    date violations: []
== p3_pt_course_charge all_accepted: cents=[624000, 166500, 215000]
    Capital PT, visit 9, March 6, 2026: $1,665.00 | PT course of care charge: $1,665.
    date violations: []
== p3_pt_course_charge counted: cents=[624000, 166500, 215000]
    Capital PT, visit 9, March 6, 2026: $1,665.00 | PT course of care charge: $1,665.
    date violations: []
== p4_pt_nine_attended all_accepted: cents=[624000, 215000]
    date violations: []
    notes: - Record 6 (Capital PT, visit 9, March 6, 2026): "PT charges: $1,665." Not totaled ($1,665): The sentence names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized charge and is not totaled.
== p4_pt_nine_attended counted: cents=[624000, 215000]
    date violations: []
    notes: - Record 6 (Capital PT, visit 9, March 6, 2026): "PT charges: $1,665." Not totaled ($1,665): The sentence names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized charge and is not totaled.
== p5_pt_since_01_23 all_accepted: cents=[624000, 215000]
    date violations: []
    notes: - Record 6 (Capital PT, visit 9, March 6, 2026): "PT charges: $1,665." Not totaled ($1,665): The sentence names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized charge and is not totaled.
== p5_pt_since_01_23 counted: cents=[624000, 215000]
    date violations: []
    notes: - Record 6 (Capital PT, visit 9, March 6, 2026): "PT charges: $1,665." Not totaled ($1,665): The sentence names no service (a service name, or a CPT, HCPCS or revenue code), so it is not an itemized charge and is not totaled.
== p6_control_pt_9_visits all_accepted: cents=[624000, 215000]
    date violations: []
    notes: - Record 6 (Capital PT, visit 9, March 6, 2026): "PT charges for 9 visits: $1,665." Amount unclear ($1,665). Request clean copy of bill.
== p6_control_pt_9_visits counted: cents=[624000, 215000]
    date violations: []
    notes: - Record 6 (Capital PT, visit 9, March 6, 2026): "PT charges for 9 visits: $1,665." Amount unclear ($1,665). Request clean copy of bill.
== p7_pt_this_visit_control all_accepted: cents=[624000, 18500, 215000]
    Capital PT, visit 9, March 6, 2026: $185.00 | Discharge visit charge $185.
    date violations: []
== p7_pt_this_visit_control counted: cents=[624000, 18500, 215000]
    Capital PT, visit 9, March 6, 2026: $185.00 | Discharge visit charge $185.
    date violations: []
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:51:00.321Z

**tool call — Bash**
````
{
 "command": "grep -v \"^llm call failed\" /Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/b2thp2sc8.txt | grep -c . ; ls artifacts/review-evidence/T-202-paralegal-r5/letters | head -50; cd artifacts/review-evidence/T-202-paralegal-r5/letters && cat lib11-all_accepted-letter.txt | sed -n '/BILLED/,$p'; grep -n \"date of service\\|DATE OF SERVICE\" lib11-all_accepted-notes.txt lib14-all_accepted-notes.txt",
 "description": "Inspect lib11 letter and notes on blanks"
}
````

### User / tool · 2026-11-03T02:51:00.427Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:51:06.834Z

**tool call — Bash**
````
{
 "command": "grep -n -B3 \"Wexcombe Memorial ED\\\"\\|Source: Wexcombe\" evals/library/case_lib11_priors_and_ledger.txt | head; grep -n -A2 \"Source: Orrin Mere Regional ED\\|Source: Tarnwick\" evals/library/case_lib14_handwritten_chiro_scans.txt; grep -n -B1 -A2 \"Source: Wexcombe\" evals/library/case_lib11_priors_and_ledger.txt",
 "description": "Look up the blanked records in lib11 and lib14"
}
````

### User / tool · 2026-11-03T02:51:06.933Z

**tool result**
````
12-
13-=== Record 3 ===
14-Date: 2026-03-18
15:Source: Wexcombe Memorial ED
5:Source: Tarnwick Fire-Rescue run report
6-Excerpt: "Driver of a sedan struck from behind. Moderate damage to the rear of the vehicle. Pt ambulatory at scene. Pt states neck pain 6/10 and tingling in the right hand. Cervical collar applied. Transported to Orrin Mere Regional ED."
7-
--
10:Source: Orrin Mere Regional ED
11-Excerpt: "Dx: cervical strain. X-ray cervical spine negative for fracture. Discharged with a muscle relaxant. ED charge: $2,960."
12-
--
40:Source: Tarnwick Fire-Rescue, ambulance invoice
41-Excerpt: "Invoice for the run of 09/14/2026. A0427 ALS emergency transport, 1 unit, charge $1,380.00. A0425 ground mileage, loaded, 8.7 miles at $21.50 per mile, charge $187.05. Total charges $1,567.05. No payments posted. Letter of protection requested."
14-Date: 2026-03-18
15:Source: Wexcombe Memorial ED
16-Excerpt: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture. ED charge: $3,260."
17-
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:51:38.846Z

**tool call — Bash**
````
{
 "command": "grep -rln \"DOS  \\|Date of Service  \\|DOS\\s\\s\" evals/golden evals/library | head; grep -n -A6 \"itemized ledger\" evals/library/case_lib11_priors_and_ledger.txt | head -20",
 "description": "Find table-format excerpts in corpus"
}
````

### User / tool · 2026-11-03T02:51:38.946Z

**tool result**
````
45:Source: Fennimoor Spine Clinic, itemized ledger
46-Excerpt: "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; total charges $2,740.00. Payment received $300.00. Adjustment (courtesy discount) -$274.00. Balance due $2,166.00. Account held under letter of protection."
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:51:48.992Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5 && python3 - <<'EOF'\np = \"fullpipe_r5.py\"\ns = open(p).read()\nadd = '''    # bill tables (multi-line excerpt): a 'Date of service: X' key-value line directly over an un-headed row; control: a real DOS column\n    \"t4_kv_line_over_row\": (\"275\", c09(\"Hobbleton Family Clinic, billing statement\", \"Date of service: 02/02/2026     Account: 4471\\\\n02/20/2026   Office visit 99213   $275.00\")),\n    \"t1_control_dos_column\": (\"275\", c09(\"Hobbleton Family Clinic, billing statement\", \"Posted      DOS         Description           Amount\\\\n02/20/2026  02/02/2026  Office visit 99213    $275.00\")),\n}\n'''\ns = s.replace('    \"p7_pt_this_visit_control\": (\"185\", pt9(\"Discharge visit charge $185.\")),\\n}\\n', '    \"p7_pt_this_visit_control\": (\"185\", pt9(\"Discharge visit charge $185.\")),\\n' + add)\nassert add in s\nopen(p, \"w\").write(s)\nEOF\ncd /Users/arsis/zlayt-pm-project && ONLY=t4_kv_line_over_row,t1_control_dos_column PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf 2>&1 | grep -v \"^llm call failed\" > artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5_tables.out; cat artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5_tables.out",
 "description": "Run table-shape variants through full pipeline",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T02:51:49.789Z

**tool result**
````
== t4_kv_line_over_row all_accepted: cents=[27500]
    Hobbleton Family Clinic, billing statement, February 20, 2026: $275.00 | 02/20/2026   Office visit 99213   $275.00
    date violations: []
== t4_kv_line_over_row counted: cents=[27500]
    Hobbleton Family Clinic, billing statement, February 20, 2026: $275.00 | 02/20/2026   Office visit 99213   $275.00
    date violations: []
== t1_control_dos_column all_accepted: cents=[27500]
    Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00 | 02/20/2026  02/02/2026  Office visit 99213    $275.00
    date violations: []
== t1_control_dos_column counted: cents=[27500]
    Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00 | 02/20/2026  02/02/2026  Office visit 99213    $275.00
    date violations: []
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:51:57.084Z

**tool call — Bash**
````
{
 "command": "head -20 artifacts/review-evidence/T-060-paralegal-pass4-serve.py; lsof -iTCP:7985 -sTCP:LISTEN -nP; echo lsof=$?",
 "description": "Check serve script and port availability"
}
````

### User / tool · 2026-11-03T02:51:57.247Z

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
lsof=1
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:52:02.664Z

**tool call — Bash**
````
{
 "command": "env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DEMO=1 ZLAYT_DB=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/db/r5.db PORT=7985 HOST=127.0.0.1 .venv/bin/python -I artifacts/review-evidence/T-060-paralegal-pass4-serve.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/server.log 2>&1",
 "description": "Start f9c0faf archive app on port 7985",
 "run_in_background": true
}
````

### User / tool · 2026-11-03T02:52:02.744Z

**tool result**
````
Command running in background with ID: bcgiq2v2p. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bcgiq2v2p.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:52:04.727Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-202-paralegal-r5/db; curl -s -m 5 http://127.0.0.1:7985/api/health; echo; lsof -iTCP:7985 -sTCP:LISTEN -nP; tail -5 artifacts/review-evidence/T-202-paralegal-r5/server.log",
 "description": "Check server health and listener PID"
}
````

### User / tool · 2026-11-03T02:52:05.058Z

**tool result**
````
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"local_mode":true,"answers":"prepared","live_enabled":false,"models":{"generator":"hand-checked (qa)","judge":"claude-haiku-5-5","generator_prepared":true},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item","sample_available":true}
COMMAND  PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  4950 arsis    9u  IPv4 0xe730845d20660798      0t0  TCP 127.0.0.1:7985 (LISTEN)
Serving on http://127.0.0.1:7985  (Ctrl-C to stop)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:52:10.623Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5 && python3 - <<'EOF'\ns = open(\"h.py\").read().replace('\"http://127.0.0.1:7984\")  # T-202 r4: 8cb5bd2 archive, port 7984', '\"http://127.0.0.1:7985\")  # T-202 r5: f9c0faf archive, port 7985')\nassert \"7985\" in s\nopen(\"h.py\", \"w\").write(s)\np = open(\"p01_cases.py\").read().replace(\"# r4: 8cb5bd2 archive, port 7984\", \"# r5: f9c0faf archive, port 7985\")\nassert \"r5: f9c0faf\" in p\nopen(\"p01_cases.py\", \"w\").write(p)\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/h.py artifacts/review-evidence/T-202-paralegal-r5/p01_cases.py > artifacts/review-evidence/T-202-paralegal-r5/p01.out 2>&1; echo $?; grep \"done in\\|draft took\\|ERRORS\\|Error\\|http 4\\|http 5\" artifacts/review-evidence/T-202-paralegal-r5/p01.out | head -20",
 "description": "Drive five cases through UI with Playwright",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:53:32.149Z

**tool result**
````
0
[sample] draft took 2.3 s
[sample] done in 15.6 s
[case_09] draft took 2.5 s
[case_09] done in 8.2 s
[lib14] draft took 2.4 s
[lib14] done in 13.2 s
[lib10] draft took 2.4 s
[lib10] done in 19.6 s
[lib11] draft took 2.4 s
[lib11] done in 24.2 s
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:53:34.886Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5 && for c in sample case_09 lib14 lib10 lib11; do echo \"##### $c\"; sed -n '/BILLED CHARGES/,$p' ui-$c-letter.txt; echo; grep -n -A6 \"CHARGES WITHOUT A CERTAIN\" ui-$c-notes.txt; done; grep \"s3 item\" p01.out | grep -i \"date of service\\|statement dated\" | head -20",
 "description": "Show UI-downloaded letters billed charges and notes"
}
````

### User / tool · 2026-11-03T02:53:35.029Z

**tool result**
````
##### sample
BILLED CHARGES

Central ER discharge summary, January 9, 2026: $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240."
Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
Source [Ex. __ / Bates __]: "Charge: $2,150."

Billed charges accepted from these records: $8,390.00
##### case_09
BILLED CHARGES

Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00
Source [Ex. __ / Bates __]: "Statement for visit of 2026-02-02: $275."

Billed charges accepted from these records: $275.00
27:CHARGES WITHOUT A CERTAIN DATE OF SERVICE
28-- Hobbleton Family Clinic, $275: The line shows 2026-02-02, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
29-
30-RECORDS NOT IN THE TREATMENT SECTION
31-- Record 2 (Hobbleton Family Clinic, billing statement, March 1, 2026) — dismissed
32-
33-EDITED ITEMS
##### lib14
BILLED CHARGES

Orrin Mere Regional ED, date of service [__________] (statement dated September 14, 2026): $2,960.00
Source [Ex. __ / Bates __]: "ED charge: $2,960."
Tarnwick Fire-Rescue, ambulance invoice, date of service [__________] (statement dated November 12, 2026): $1,380.00
Source [Ex. __ / Bates __]: "A0427 ALS emergency transport, 1 unit, charge $1,380.00."
Tarnwick Fire-Rescue, ambulance invoice, date of service [__________] (statement dated November 12, 2026): $187.05
Source [Ex. __ / Bates __]: "charge $187.05."

Billed charges accepted from these records: $4,527.05
28:CHARGES WITHOUT A CERTAIN DATE OF SERVICE
29-- Orrin Mere Regional ED, $2,960: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
30-- Tarnwick Fire-Rescue, $1,380.00: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
31-- Tarnwick Fire-Rescue, $187.05: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
32-
33-RECORDS NOT IN THE TREATMENT SECTION
34-- Record 7 (Hollowbrook Chiropractic, CMS-1500 (OCR of scanned claim), November 10, 2026) — dismissed
##### lib10
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
##### lib11
BILLED CHARGES

Wexcombe Memorial ED, date of service [__________] (statement dated March 18, 2026): $3,260.00
Source [Ex. __ / Bates __]: "ED charge: $3,260."
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00
Source [Ex. __ / Bates __]: "New patient exam charge $250.00"
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $180.00
Source [Ex. __ / Bates __]: "x-ray charge $180.00"
Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $2,310.00
Source [Ex. __ / Bates __]: "treatment visits 1 through 14 charge $2,310.00"

Billed charges accepted from these records: $6,000.00
38:CHARGES WITHOUT A CERTAIN DATE OF SERVICE
39-- Wexcombe Memorial ED, $3,260: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
40-- Fennimoor Spine Clinic, $250.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
41-- Fennimoor Spine Clinic, $180.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
42-- Fennimoor Spine Clinic, $2,310.00: The line states no date of service. The letter leaves a blank for the date of service; fill it from the quote or request a dated itemized bill from the provider.
43-
44-RECORDS NOT IN THE TREATMENT SECTION
[sample] s3 item=a1 boxes=[] :: Charge / Central ER discharge summary · January 9, 2026 /  / $6,240.00 /  / Date of service January 9, 2026 /  / Written in the record as $6,240. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[sample] s3 item=a4 boxes=[] :: Charge / Austin Imaging, cervical MRI · May 29, 2026 /  / $2,150.00 /  / Date of service May 29, 2026 /  / Written in the record as $2,150. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[case_09] s3 item=a1 boxes=[] :: Charge / Hobbleton Family Clinic, billing statement · statement dated March 1, 2026 /  / $275.00 /  / date of service [__________] (statement dated March 1, 2026) /  / Written in the record as $275. /  / The line shows 2026-02-02, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated line-by-line bill, and fill the blank before you rely on it. /  / What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
[lib14] s3 item=a1 boxes=[] :: Charge / Orrin Mere Regional ED · statement dated September 14, 2026 /  / $2,960.00 /  / date of service [__________] (statement dated September 14, 2026) /  / Written in the record as $2,960. /  / The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated line-by-line bill, and fill the blank before you rely on it. /  / What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
[lib14] s3 item=a2 boxes=[] :: Charge / Tarnwick Fire-Rescue, ambulance invoice · statement dated November 12, 2026 /  / $1,380.00 /  / date of service [__________] (statement dated November 12, 2026) /  / Written in the record as $1,380.00. /  / The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated line-by-line bill, and fill the blank before you rely on it. /  / What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
[lib14] s3 item=a4 boxes=[] :: Charge / Tarnwick Fire-Rescue, ambulance invoice · statement dated November 12, 2026 /  / $187.05 /  / date of service [__________] (statement dated November 12, 2026) /  / Written in the record as $187.05. /  / The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated line-by-line bill, and fill the blank before you rely on it. /  / What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
[lib14] s3 item=a3 boxes=[] :: Never counted / Tarnwick Fire-Rescue, ambulance invoice · statement dated November 12, 2026 /  / $21.50 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill total.
[lib14] s3 item=a5 boxes=['check-compare'] :: Never counted / Tarnwick Fire-Rescue, ambulance invoice · statement dated November 12, 2026 /  / $1,567.05 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
[lib10] s3 item=a2 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $4,920.00 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $4,920.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib10] s3 item=a3 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $2,105.00 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $2,105.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib10] s3 item=a4 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $386.50 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $386.50. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib10] s3 item=a5 boxes=[] :: Charge / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $712.00 /  / Date of service June 9–12, 2026 · statement dated June 19, 2026 /  / Written in the record as $712.00. /  / If you count it, it's added to the bill total in the letter, with the highlighted words as its source.
[lib10] s3 item=a1 boxes=[] :: Never counted / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $1,640.00 /  / This figure is a rate, not a charge, so it is not added to the total. /  / Either way, it is never added to the bill total.
[lib10] s3 item=a6 boxes=['check-compare'] :: Never counted / Saltmarrow General Hospital, UB-04 itemized bill · statement dated June 19, 2026 /  / $8,123.50 /  / Total or subtotal line: it repeats the charges listed with it, so it is not totaled. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
[lib10] s3 item=a7 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · statement dated July 3, 2026 /  / $8,023.50 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
[lib10] s3 item=a8 boxes=[] :: Never counted / Quoinmere Mutual Health Plan, EOB · statement dated July 3, 2026 /  / $3,610.00 /  / Adjustment, write-off or credit: not a charge, and never subtracted from the billed charges. /  / Either way, it is never added to the bill total.
[lib10] s3 item=a9 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · statement dated July 3, 2026 /  / $4,413.50 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
[lib10] s3 item=a10 boxes=[] :: Never counted / Quoinmere Mutual Health Plan, EOB · statement dated July 3, 2026 /  / $3,530.80 /  / Payment: money received, not a charge. /  / Either way, it is never added to the bill total.
[lib10] s3 item=a11 boxes=['check-compare'] :: Never counted / Quoinmere Mutual Health Plan, EOB · statement dated July 3, 2026 /  / $882.70 /  / Insurer document (EOB or remittance): it restates the provider's bill, so it is not a second charge. /  / A second AI check thought this may be a billed charge, not what it was first sorted as. Read it against the highlighted words before you decide. / I read this amount against the highlighted words myself.
[lib11] s3 item=a1 boxes=[] :: Charge / Wexcombe Memorial ED · statement dated March 18, 2026 /  / $3,260.00 /  / date of service [__________] (statement dated March 18, 2026) /  / Written in the record as $3,260. /  / The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated line-by-line bill, and fill the blank before you rely on it. /  / What to do: find the date of service in the record (the highlighted words may help) or ask the provider, then write it in the blank “date of service [__________]” in your letter. The date in parentheses is the statement date, not the service date. Counting it adds the amount to the bill total.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:54:04.401Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5 && python3 - <<'EOF'\ns = open(\"eval_teeth_r4.py\").read()\ns = s.replace(\"T-202 r4 paralegal: evals.letter_check.charge_date_violations on the line the 8cb5bd2 build prints\", \"T-202 r5 paralegal (copied from r4, r5 cases): evals.letter_check.charge_date_violations on the line the f9c0faf build prints\")\ns = s.replace(\"T-202-paralegal-r4/eval_teeth_r4.py\", \"T-202-paralegal-r5/eval_teeth_r5.py\")\ni = s.index(\"CASES = [\")\nj = s.index(\"]\\nfor name\")\nnew = '''CASES = [\n    # name, source, record date, excerpt, quote, figure, build's head, paralegal's heads\n    (\"M1 'Austin MRI' bill dated 06/20, DOS 05/29 in the previous sentence\", \"Austin MRI\", \"2026-06-20\",\n     \"Date of service 05/29/2026. Cervical spine MRI, CPT 72141, charge $2,150.\",\n     \"Cervical spine MRI, CPT 72141, charge $2,150.\", \"$2,150.00\",\n     \"Austin MRI, June 20, 2026\",\n     [f\"Austin MRI, {BL} (statement dated June 20, 2026)\", \"Austin MRI, May 29, 2026\"]),\n    (\"C1 'Hobbleton Follow-Up Clinic' bill dated 03/01\", \"Hobbleton Follow-Up Clinic\", \"2026-03-01\",\n     \"Date of service 2026-02-02. Office visit 99213 charge $275.\",\n     \"Office visit 99213 charge $275.\", \"$275.00\",\n     \"Hobbleton Follow-Up Clinic, March 1, 2026\",\n     [f\"Hobbleton Follow-Up Clinic, {BL} (statement dated March 1, 2026)\", \"Hobbleton Follow-Up Clinic, February 2, 2026\"]),\n    (\"T4 key-value DOS line over an un-headed row\", \"Hobbleton Family Clinic, billing statement\", \"2026-03-01\",\n     \"Date of service: 02/02/2026     Account: 4471\\\\n02/20/2026   Office visit 99213   $275.00\",\n     \"02/20/2026   Office visit 99213   $275.00\", \"$275.00\",\n     \"Hobbleton Family Clinic, billing statement, February 20, 2026\",\n     [f\"Hobbleton Family Clinic, billing statement, {BL} (statement dated March 1, 2026)\", \"Hobbleton Family Clinic, billing statement, February 2, 2026\"]),\n'''\ns = s[:i] + new + s[j:]\nopen(\"eval_teeth_r5.py\", \"w\").write(s)\nEOF\nrm eval_teeth_r4.py provider_only_bill.py probe_r4.py letters_dump_r4.py 2>/dev/null; cd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/eval_teeth_r5.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf > artifacts/review-evidence/T-202-paralegal-r5/eval_teeth_r5.out 2>&1; cat artifacts/review-evidence/T-202-paralegal-r5/eval_teeth_r5.out",
 "description": "Check letter_check teeth on round 5 wrong-date shapes"
}
````

### User / tool · 2026-11-03T02:54:04.725Z

**tool result**
````
== M1 'Austin MRI' bill dated 06/20, DOS 05/29 in the previous sentence
   build  'Austin MRI, June 20, 2026: $2,150.00' -> []
   alt    'Austin MRI, date of service [__________] (statement dated June 20, 2026): $2,150.00' -> ["charge line's date is not certain from its quote (an encounter record's line must carry the record's own date): Austin MRI, date of service [__________] (statement dated June 20, 2026): $2,150.00"]
   alt    'Austin MRI, May 29, 2026: $2,150.00' -> ["charge line's date is not certain from its quote (the line prints a date no source ties to it (the source gives 2026-06-20)): Austin MRI, May 29, 2026: $2,150.00"]
== C1 'Hobbleton Follow-Up Clinic' bill dated 03/01
   build  'Hobbleton Follow-Up Clinic, March 1, 2026: $275.00' -> []
   alt    'Hobbleton Follow-Up Clinic, date of service [__________] (statement dated March 1, 2026): $275.00' -> ["charge line's date is not certain from its quote (an encounter record's line must carry the record's own date): Hobbleton Follow-Up Clinic, date of service [__________] (statement dated March 1, 2026): $275.00"]
   alt    'Hobbleton Follow-Up Clinic, February 2, 2026: $275.00' -> ["charge line's date is not certain from its quote (the line prints a date no source ties to it (the source gives 2026-03-01)): Hobbleton Follow-Up Clinic, February 2, 2026: $275.00"]
== T4 key-value DOS line over an un-headed row
   build  'Hobbleton Family Clinic, billing statement, February 20, 2026: $275.00' -> []
   alt    'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00' -> ["charge line's date is not certain from its quote (the quote's date-of-service cell holds one certain date and the line prints a blank): Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00"]
   alt    'Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00' -> ["charge line's date is not certain from its quote (the quote's date-of-service cell reads 2026-02-20): Hobbleton Family Clinic, billing statement, February 2, 2026: $275.00"]
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:54:13.480Z

**tool call — Bash**
````
{
 "command": "kill 4950; sleep 1; lsof -iTCP:7985 -sTCP:LISTEN -nP; echo lsof=$?; curl -s -o /dev/null -w \"%{http_code}\\n\" -m 3 http://127.0.0.1:7985/api/health",
 "description": "Stop server PID and confirm port closed"
}
````

### User / tool · 2026-11-03T02:54:15.073Z

**tool result (error)**
````
Exit code 7
lsof=1
000
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:54:16.125Z

Server stopped (PID 4950, lsof exit 1, curl 000). Now check the r4 finding shapes in the probe output.

### Assistant · claude-opus-5-5 · 2026-11-03T02:54:18.259Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5 && grep -n -A4 \"^== probe_r4 O4\\|^== probe_r4 O5\\|^== probe_r4 S1 \\|^== probe_r4 S2\\|^== probe_r4 C3\\|^== probe_r3c C3\\|^== probe_r3 R15\\|^== probe_r2 N20\\|^== probe_r2 N8 \\|^== probe_r4 T1\\|^== probe_r4 T2\\|^== probe_r3b R21\" probe_r5.out | grep -v \"^\\-\\-$\" | cut -c1-330",
 "description": "Show r4 finding shapes in r5 probe output"
}
````

### User / tool · 2026-11-03T02:54:18.350Z

**tool result**
````
122:== probe_r2 N8 CMS-1500 with per-line item 24A dates  (record date 2026-07-14; source 'Wardlaw Orthopedics, CMS-1500'; kind=bill; billing_document=True)
123-   CMS-1500. Item 24A 06/24/2026 CPT 99204 $185.00. Item 24A 07/08/2026 CPT 20610 $210.00. Item 28 TOTAL CHARGE $395.00.
124-      $185.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $185.00'  state=not_stated reason=non_service_date
125-              Step 3 note: The line shows 06/24/2026, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the 
126-      $210.00 -> letter head: 'Wardlaw Orthopedics, CMS-1500, date of service [__________] (statement dated July 14, 2026): $210.00'  state=not_stated reason=non_service_date
181:== probe_r2 N20 UB-04 FL6 6-digit from/through  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04'; kind=bill; billing_document=True)
182-   FL6 statement covers period FROM 060926 THROUGH 061226. Rev 0450 emergency room FL47 $2,105.00.
183-    $2,105.00 -> letter head: 'Saltmarrow General Hospital, UB-04, date of service [__________] (statement dated June 19, 2026): $2,105.00'  state=not_stated reason=no_date
184-              Step 3 note: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated itemized bill, and
185-== probe_r2 N21 admit / discharge dates  (record date 2026-06-19; source 'Saltmarrow General Hospital, UB-04'; kind=bill; billing_document=True)
316:== probe_r3 R15 bill: DOS with ordinal ('Feb. 2nd, 2026')  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; kind=bill; billing_document=True)
317-   DOS Feb. 2nd, 2026 office visit charge $275.00.
318-      $275.00 -> letter head: 'Hobbleton Family Clinic, billing statement, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=no_date
319-              Step 3 note: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated itemized bill, and
320-== probe_r3 R16 bill: DOS 02/02/2026 and statement date 03/01/2026 in one clause  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; kind=bill; billing_document=True)
347:== probe_r3b R21 PT discharge 03/06: 'treatment dates' period then a charge  (record date 2026-03-06; source 'Capital PT, discharge summary'; kind=encounter; billing_document=False)
348-   Treatment dates 01/23/2026 to 03/06/2026, 9 visits, charge $1,665.00.
349-    $1,665.00 -> letter head: 'Capital PT, discharge summary, date of service [__________] (statement dated March 6, 2026): $1,665.00'  state=not_stated reason=non_service_date
350-              Step 3 note: The line shows 01/23/2026 to 03/06/2026, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Take the 
351-== probe_r3b R22 bill 03/01: last visit date label then an undated coded line  (record date 2026-03-01; source 'Hobbleton Family Clinic, billing statement'; kind=bill; billing_document=True)
365:== probe_r3c C3 ER 01/09: charge, then next visit date in its own sentence  (record date 2026-01-09; source 'Central ER discharge summary'; kind=bill; billing_document=False)
366-   ER charges: $6,240. Next visit date 01/16/2026.
367-       $6,240 -> letter head: 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026): $6,240'  state=not_stated reason=no_date
368-              Step 3 note: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated itemized bill, and
369-== probe_r3c C4 ER 01/09: charge, then next visit date after a comma  (record date 2026-01-09; source 'Central ER discharge summary'; kind=bill; billing_document=False)
442:== probe_r4 O4 PT visit 9 03/06: 'Previous visit's date of service 02/20/2026'  (record date 2026-03-06; source 'Capital PT, visit 9'; kind=encounter; billing_document=False)
443-   Previous visit's date of service 02/20/2026, discharge visit charge $185.00.
444-      $185.00 -> letter head: 'Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $185.00'  state=not_stated reason=non_service_date
445-              Step 3 note: The line shows 02/20/2026, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the 
446:== probe_r4 O5 PT visit 9 03/06: 'Initial eval DOS 01/23/2026'  (record date 2026-03-06; source 'Capital PT, visit 9'; kind=encounter; billing_document=False)
447-   Initial eval DOS 01/23/2026, discharge visit charge $185.00.
448-      $185.00 -> letter head: 'Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $185.00'  state=not_stated reason=non_service_date
449-              Step 3 note: The line shows 01/23/2026, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the 
450-== probe_r4 O6 PCP 01/16: 'Prior  DOS 01/09/2026' (two spaces)  (record date 2026-01-16; source 'Dr. Alvarez, primary care'; kind=other; billing_document=False)
470:== probe_r4 S1 'Hobbleton Family Clinic' 03/01: Amount due ... office visit on 02/02/2026  (record date 2026-03-01; source 'Hobbleton Family Clinic'; kind=other; billing_document=False)
471-   Amount due $275.00 for office visit on 02/02/2026.
472-      $275.00 -> letter head: 'Hobbleton Family Clinic, date of service [__________] (statement dated March 1, 2026): $275.00'  state=not_stated reason=non_service_date
473-              Step 3 note: The line shows 02/02/2026, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the 
474:== probe_r4 S2 'Austin Imaging' 06/20: Patient responsibility ... MRI performed 05/29/2026  (record date 2026-06-20; source 'Austin Imaging'; kind=other; billing_document=False)
475-   Patient responsibility $2,150.00 for cervical MRI performed 05/29/2026.
476-    $2,150.00 -> letter head: 'Austin Imaging, date of service [__________] (statement dated June 20, 2026): $2,150.00'  state=not_stated reason=non_service_date
477-              Step 3 note: The line shows 05/29/2026, but not in a date-of-service column of a bill table, and the code does not read dates out of sentences, so it cannot tell whether it is the date of service. The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the 
478-== probe_r4 S3 'Capital Physical Therapy' 03/20: Total due for 9 visits  (record date 2026-03-20; source 'Capital Physical Therapy'; kind=other; billing_document=False)
501:== probe_r4 T1 PT visit 9 03/06: total for visits 1-9 in the discharge note  (record date 2026-03-06; source 'Capital PT, visit 9'; kind=encounter; billing_document=False)
502-   Discharged from PT after two missed appointments. Total for visits 1-9: $1,665.00.
503-    $1,665.00 -> letter head: 'Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $1,665.00'  state=not_stated reason=no_date
504-              Step 3 note: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated itemized bill, and
505:== probe_r4 T2 PT visit 9 03/06: PT charges to date  (record date 2026-03-06; source 'Capital PT, visit 9'; kind=encounter; billing_document=False)
506-   Discharged from PT after two missed appointments. PT charges to date $1,665.00.
507-    $1,665.00 -> letter head: 'Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $1,665.00'  state=not_stated reason=no_date
508-              Step 3 note: The line states no date of service the code can read (a date-of-service column of a bill table, or the date of a visit note). The letter prints no service date for this line. It leaves a blank for the date of service. Take the date from the matching visit note, or request a dated itemized bill, and
509-== probe_r4 T3 ER note 01/10 (summary written next day): arrived 01/09/2026  (record date 2026-01-10; source 'Central ER discharge summary'; kind=encounter; billing_document=False)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:54:34.709Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5 && grep -n \"s3 item=a1\" p01.out | grep \"lib11\\|lib14\" | cut -c1-80; ls *.png | tr '\\n' ' '; echo; grep -n \"statement date, not the service date\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf/app/frontend/*.js /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf/app/frontend/**/*.js 2>/dev/null | cut -c1-250",
 "description": "Locate Step 3 lines, screenshots, frontend text source"
}
````

### User / tool · 2026-11-03T02:54:34.834Z

**tool result**
````
161:[lib14] s3 item=a1 boxes=[] :: Charge / Orrin Mere Regional ED · statement 
347:[lib11] s3 item=a1 boxes=[] :: Charge / Wexcombe Memorial ED · statement da
case_09-s3-00-a1.png case_09-step2-done.png case_09-step3-done.png case_09-step4.png lib10-s3-00-a2.png lib10-s3-01-a3.png lib10-s3-02-a4.png lib10-s3-03-a5.png lib10-s3-04-a1.png lib10-s3-05-a6.png lib10-s3-06-a7.png lib10-s3-07-a8.png lib10-s3-08-a9.png lib10-s3-09-a10.png lib10-s3-10-a11.png lib10-step2-done.png lib10-step3-done.png lib10-step4.png lib11-s3-00-a1.png lib11-s3-01-a2.png lib11-s3-02-a3.png lib11-s3-03-a4.png lib11-s3-04-a5.png lib11-s3-05-a6.png lib11-s3-06-a7.png lib11-s3-07-a8.png lib11-step2-done.png lib11-step3-done.png lib11-step4.png lib14-s3-00-a1.png lib14-s3-01-a2.png lib14-s3-02-a4.png lib14-s3-03-a3.png lib14-s3-04-a5.png lib14-step2-done.png lib14-step3-done.png lib14-step4.png sample-s3-00-a1.png sample-s3-01-a4.png sample-s3-02-a2.png sample-s3-03-a3.png sample-step2-done.png sample-step3-done.png sample-step4.png 
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:54:36.116Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/lib11-s3-00-a1.png"
}
````

### User / tool · 2026-11-03T02:54:36.126Z

**tool result**
````
[image]
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:54:42.775Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf && grep -rn \"statement date, not the service date\" app/ | cut -c1-200; grep -n \"statement dated\" app/backend/present.py app/backend/store.py app/backend/export.py | cut -c1-200 | head",
 "description": "Locate source of statement-dated wording"
}
````

### User / tool · 2026-11-03T02:54:42.898Z

**tool result**
````
app/frontend/guided/step3.js:37:    const stmt = /\(statement dated/.test((sd && sd.text) || "") ? " The date in parentheses is the statement date, not the service date." : "";
app/backend/store.py:120:    {state: 'stated'|'not_stated', date_iso, end_iso (None for one day), text (the letter's date text: 'June 9\u201312, 2026', or the fillable blank 'date of service [________
app/backend/export.py:218:        NEVER given the record's date bare: 'Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026)' (D-071 addendum: a fillabl
app/backend/export.py:219:        because the adjuster can still match the line to the ledger page, and it agrees with the review screen's 'No date of service (statement dated ...)'. A case dict
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:54:49.737Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_f9c0faf && grep -n \"def not_stated_text\\|statement dated {display\\|def record_kind\\|return \\\"encounter\\\" if\\|def _header_cells\\|if re.search(r\\\"\\\\\\\\d\\\", line) and not _H_SVC\\|_MULTI = \\|if _MULTI.search\" app/backend/service_date.py; grep -n '\"mri\"\\|\"new patient\", \"follow-up\"\\|\"consult\", \"consultation\"' app/backend/encounter_types.json; grep -n \"_ENC\\|encounter\" evals/letter_check.py | head -8; grep -n \"fill it from the quote\" app/backend/*.py | cut -c1-160",
 "description": "Get line references for findings"
}
````

### User / tool · 2026-11-03T02:54:49.863Z

**tool result**
````
44:def record_kind(source, excerpt: str = "") -> str:
54:    return "encounter" if _hit(_ENC, src) else "other"
105:def not_stated_text(statement_iso) -> str:
109:        return f"{BLANK} (statement dated {display(statement_iso)})"
256:def _header_cells(excerpt: str, row_ls: int):
263:        if re.search(r"\d", line) and not _H_SVC.search(line):
320:_MULTI = re.compile(r"\b(?:visits|sessions|treatments|appointments|encounters)\b|\bto[ -]date\b|\bvisits?\s+\d+\s*(?:-|\u2013|\u2014|to|through|thru)\s*\d+|"
388:    if _MULTI.search(seg):
8:    "consult", "consultation", "consulta", "nota de consulta", "evaluation", "re-evaluation", "reevaluation", "exam", "examination", "re-examination", "reexamination",
9:    "new patient", "follow-up", "followup", "mri", "x-ray", "xray", "ct scan", "ultrasound", "radiology report", "imaging report"
17:(2) the encounter record's own date, only when the record is identified by a DOCUMENT-TYPE word in its source label (read from the declared table app/backend/encounter_types.json, the
233:TYPES_PATH = ROOT / "app" / "backend" / "encounter_types.json"          # D-071 amendment 2: the ONE declared table of record types (production reads the same file)
247:    """'bill' | 'encounter' | 'other', read from the declared table with this file's own matcher: financial words in the source label or the opening of the excerpt (its first characters up to the first colon or full stop) make a bill,
248:    administrative words make 'other', and a record is an ENCOUNTER only when its source label names one (a visit, ER, clinic, therapy, imaging, ambulance-run note ...). Only an encounter
255:    return "encounter" if any(_has_term(src_w, t) for t in _TYPES["encounter"]) else "other"
261:_MULTI_RX = re.compile(r"\b(?:visits|sessions|treatments|appointments|encounters)\b|\bto[ -]date\b|\bvisits? \d+ ?(?:-|\u2013|to|through|thru) ?\d+|\b(?:[2-9]|\d\d+|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve) ?(?:x|times)\b", re.IGNORECASE)
279:    return bool(re.search(r"\bdos\b|\bsvc\b|date\W*s?\W*of\W+serv|service\W+date|visit\W+date|date\W+of\W+visit|encounter\W+date|\b24\W?a\b", h)
470:            bill, lends = kind_r == "bill", kind_r == "encounter"          # only an identified encounter record lends its own date
app/backend/export.py:614:            out.append(f"- {_provider(v.source(a['record_no'])) or v.source(a['record_no'])}, {a['raw']}: {why} The letter leaves a bl
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:54:56.170Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5 && grep \"^>\" corpus_blanks.diff | grep -v \"__________\\|^> ==\" | head; echo ---; grep \"^<\" corpus_blanks.diff | grep -v \"^< ==\" | wc -l; grep \"^>\" corpus_blanks.diff | grep -c \"__________\"",
 "description": "Verify corpus diff only adds blanks"
}
````

### User / tool · 2026-11-03T02:54:56.284Z

**tool result**
````
---
      44
44
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:55:04.956Z

**tool call — Bash**
````
{
 "command": "ONLY=m1_austin_mri_bill,m2_open_mri_bill,c1_followup_clinic_bill,c2_xray_bill,c3_evaluation_center_bill,c4_exam_urgent_care_bill,p1_pt_charges,t4_kv_line_over_row PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/pr5_ad0d91a 2>&1 | grep -v \"^llm call failed\" > artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5_on_ad0d91a.out; grep \"all_accepted\\|^    [A-Z].*|\" artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5_on_ad0d91a.out | grep -v \"Central ER discharge summary, January 9\\|cervical MRI, May 29\" | grep -A1 all_accepted",
 "description": "Run round 5 shapes on parent ad0d91a for comparison",
 "timeout": 600000
}
````

### User / tool · 2026-11-03T02:55:07.178Z

**tool result**
````
== m1_austin_mri_bill all_accepted: cents=[624000, 215000]
    Austin MRI, June 20, 2026: $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
--
== m2_open_mri_bill all_accepted: cents=[624000, 215000]
    Open MRI of Austin, June 20, 2026: $2,150.00 | MRI charge: $2,150.
--
== c1_followup_clinic_bill all_accepted: cents=[27500]
    Hobbleton Follow-Up Clinic, March 1, 2026: $275.00 | Office visit 99213 charge $275.
--
== c2_xray_bill all_accepted: cents=[27500]
    Hobbleton X-Ray, March 1, 2026: $275.00 | Wrist x-ray 3 views, CPT 73110, charge $275.
--
== c3_evaluation_center_bill all_accepted: cents=[27500]
    Hobbleton Hand Evaluation Center, March 1, 2026: $275.00 | Hand evaluation 97165 charge $275.
--
== c4_exam_urgent_care_bill all_accepted: cents=[27500]
    Express Exam Urgent Care, March 1, 2026: $275.00 | Urgent care visit 99213 charge $275.
--
== p1_pt_charges all_accepted: cents=[624000, 166500, 215000]
    Capital PT, visit 9, March 6, 2026: $1,665.00 | Physical therapy charges: $1,665.
--
== t4_kv_line_over_row all_accepted: cents=[27500]
    Hobbleton Family Clinic, billing statement, February 20, 2026: $275.00 | 02/20/2026   Office visit 99213   $275.00
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:55:32.066Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git diff --stat f9c0faf HEAD -- app/backend app/llm app/frontend evals/letter_check.py | tail -2; ls artifacts/review-evidence/T-202-paralegal-r5/; grep -c \"\" artifacts/review-evidence/T-202-paralegal-r5/probe_r5.out; grep -n \"^== m1_austin_mri_bill all\\|^== c1_followup\\|^== p1_pt\" artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.out",
 "description": "Confirm HEAD and list evidence files"
}
````

### User / tool · 2026-11-03T02:55:32.230Z

**tool result**
````
6b0724a
case_09-s3-00-a1.png
case_09-step2-done.png
case_09-step3-done.png
case_09-step4.png
corpus_blanks.diff
corpus_blanks.py
corpus_blanks_ad0d91a.out
corpus_blanks_f9c0faf.out
db
eval_teeth_r5.out
eval_teeth_r5.py
fullpipe_r5.out
fullpipe_r5.py
fullpipe_r5_on_ad0d91a.out
fullpipe_r5_tables.out
h.py
letter_check.out
letters
letters_dump_r5.out
letters_dump_r5.py
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
probe_r5.out
probe_r5.py
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
ui-lib11-letter-onscreen.txt
ui-lib11-letter.txt
ui-lib11-notes.txt
ui-lib14-letter-onscreen.txt
ui-lib14-letter.txt
ui-lib14-notes.txt
ui-sample-letter-onscreen.txt
ui-sample-letter.txt
ui-sample-notes.txt
698
1:== m1_austin_mri_bill all_accepted: cents=[624000, 215000]
35:== c1_followup_clinic_bill all_accepted: cents=[27500]
38:== c1_followup_clinic_bill counted: cents=[27500]
59:== p1_pt_charges all_accepted: cents=[624000, 166500, 215000]
64:== p1_pt_charges counted: cents=[624000, 166500, 215000]
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:55:39.115Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/*jsoncheck* | head; ls reviews/T-202-paralegal-r5.md 2>&1; grep -n \"ED charge\\|statement dated\" artifacts/review-evidence/T-202-paralegal-r5/ui-lib11-letter.txt | head -3; grep -n \"Austin MRI, June 20\" artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.out | head -2; grep -n \"Hobbleton Family Clinic, billing statement, February 20\" artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5_tables.out | head -1; grep -n \"Capital PT, visit 9, March 6, 2026: \\$1,665.00\" artifacts/review-evidence/T-202-paralegal-r5/fullpipe_r5.out | head -3; grep -n '\"\\$6,240.\"' artifacts/review-evidence/T-202-paralegal-r5/letters/synth_sample_er_dotted_leader-all_accepted-letter.txt",
 "description": "Gather line refs and check review file absence"
}
````

### User / tool · 2026-11-03T02:55:39.487Z

**tool result**
````
artifacts/review-evidence/T-013-r2-paralegal-jsoncheck.py
artifacts/review-evidence/T-013-r3-paralegal-jsoncheck.py
artifacts/review-evidence/T-015-r2-paralegal-jsoncheck.py
artifacts/review-evidence/T-015-r3-paralegal-jsoncheck.py
artifacts/review-evidence/T-015-r4-paralegal-jsoncheck.out.txt
artifacts/review-evidence/T-015-r4-paralegal-jsoncheck.py
artifacts/review-evidence/T-039-r2-jsoncheck.py
artifacts/review-evidence/T-043-paralegal-jsoncheck.py
artifacts/review-evidence/T-068-paralegal-r2-jsoncheck.py
artifacts/review-evidence/T-076-r2-paralegal-jsoncheck.py
ls: reviews/T-202-paralegal-r5.md: No such file or directory
37:Wexcombe Memorial ED, date of service [__________] (statement dated March 18, 2026): $3,260.00
38:Source [Ex. __ / Bates __]: "ED charge: $3,260."
39:Fennimoor Spine Clinic, itemized ledger, date of service [__________] (statement dated June 15, 2026): $250.00
3:    Austin MRI, June 20, 2026: $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
7:    Austin MRI, June 20, 2026: $2,150.00 | Cervical spine MRI, CPT 72141, charge $2,150.
2:    Hobbleton Family Clinic, billing statement, February 20, 2026: $275.00 | 02/20/2026   Office visit 99213   $275.00
6:Source [Ex. __ / Bates __]: "$6,240."
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:55:42.691Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py && sed -n 1,15p artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py",
 "description": "Check JSON-check helper exists"
}
````

### User / tool · 2026-11-03T02:55:42.782Z

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
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:55:43.828Z

Now writing the draft review.

### Assistant · claude-opus-5-5 · 2026-11-03T02:56:45.239Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/draft-T-202-paralegal-r5.md",
 "content": "# T-202 round 5 (D-073, the conservative fallback): paralegal review (Maria Delgado, senior PI litigation paralegal)\n\n**Verdict: fail.** D-073 closes most of what rounds 1 to 4 found. All 115 adversarial texts from those rounds now print the correct date or the fillable blank. That includes the three round 4 blockers:\n- A PCP note citing \"DOS 01/09/2026\" now prints the blank.\n- A PT note stating \"Treatment dates 01/23/2026 to 03/06/2026, 9 visits\" now prints the blank.\n- \"Hobbleton Family Clinic\" and \"Austin Imaging\" bills now print the blank.\n\nThe dotted-leader major is also fixed on the case path: the sample ER line now prints January 9 and the total is back to $8,390.00.\n\nOn the 25-case corpus, the 15 lines that still print a date are all correct. The only change from the parent ad0d91a is that 22 lines became blanks; no dated line changed its date (corpus_blanks.diff: 44 '>' lines, all blanks).\n\n**The bar still fails in one class: provider names.** The round 4 provider-name blocker survives through the words D-073 kept in the encounter list. \"mri\", \"x-ray\", \"follow-up\", \"evaluation\", \"exam\" and \"visit\" all match anywhere in the Source line, including inside a provider's name. So \"Austin MRI\", \"Open MRI of Austin\", \"Hobbleton Follow-Up Clinic\", \"Hobbleton X-Ray\", \"Hobbleton Hand Evaluation Center\" and \"Express Exam Urgent Care\" are each read as a visit note. Their bills then print the statement date as the date of service. letter_check accepts that wrong line and rejects both the blank and the true date.\n\n**A table-heading mix-up prints a posting date (major).** A \"Date of service: 02/02/2026  Account: 4471\" line sitting directly over a dated row is read as a column heading. The row's 02/20 date then prints as the date of service.\n\n**Is a letter with many blanks still usable for a demand?** Yes, with one fix.\n- Why it works: 22 of 37 corpus charge lines are now blanks, 0 to 4 per letter. Filling a date is the same job as filling the Bates placeholders I already fill. A blank cannot be quoted back to me by an adjuster; a wrong date can.\n- The problem: 19 of those 22 blanks are ED, urgent-care, imaging or radiology records whose own date is the visit date. For all of them the letter says \"(statement dated March 18, 2026)\", and Step 3 says \"The date in parentheses is the statement date, not the service date\". Both are false for an ED record, and the instruction sends me to request a bill I do not need. That is a major.\n\n**Scope.** I extracted `git archive f9c0faf` (tree 7ec6d6b2632a…) to the session scratchpad and served it in demo mode on 127.0.0.1:7985: fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local. /api/health returned demo_mode true and local_mode true. I stopped listener PID 4950 afterwards (lsof exit 1, curl 000).\n\nHEAD moved to 6b0724a during the review. `git diff --stat f9c0faf HEAD -- app/backend app/llm app/frontend evals/letter_check.py` is empty, so the findings hold at HEAD.\n\nThe adversarial variants ran in-process through `evals.letter_check.letters_for`, which is the export path, because demo mode refuses unrecorded text. Private values seen: 1 <redacted> (the author line in `git show` output).\n\n```json\n{\"card\": \"T-202\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"commits 43b364d + f9c0faf (git archive f9c0faf, tree 7ec6d6b2632a, extracted to the session scratchpad pr5_f9c0faf/); served in demo mode (fixture backend, FIXTURE_SET=curated, ZLAYT_MODE=local; /api/health demo_mode true, local_mode true) at http://127.0.0.1:7985; listener PID 4950 stopped (lsof exit 1, curl 000). Parent ad0d91a archive (pr5_ad0d91a/) run in-process for the corpus diff and the round 5 shapes. HEAD moved to 6b0724a during the review; git diff --stat f9c0faf HEAD -- app/backend app/llm app/frontend evals/letter_check.py is empty. Cases: sample, case_09 (POST /api/cases with the golden text, opened in the UI), lib14, lib10, lib11 in the UI; all 25 letter_check cases in-process; SYNTHETIC variants in-process (demo mode refuses unrecorded text). Evidence: artifacts/review-evidence/T-202-paralegal-r5/. Private values seen: 1 <redacted>.\",\n \"exercised\": [\n  \"Read personas/paralegal.md, D-073 and its clarification (memory/ORCHESTRATOR_DECISIONS.md:97-99), memory/SCOPE_CUTS.md:113 (row 28), reviews/T-202-paralegal-r4.md, board.py show T-202 (r5 note, handoff with the 22-line corpus diff), git show --stat 43b364d f9c0faf, service_date.py and encounter_types.json at f9c0faf\",\n  \"From the archive: pytest test_t202_r5_d073 + test_t202_r4_encounter + test_t202_r3_allow_list + test_t202_r2_service_date_layouts + test_t202_charge_service_dates + test_t200_undated_charge_label: '736 passed in 11.25s' (pytest-t202.out); python -m evals.letter_check: value 0 over 25 cases (letter_check.out)\",\n  \"probe_r5.py: all 115 round 1-4 texts loaded by ast from my r2/r3/r4 probe files (PROBES lists and the r4 NEW list), plus 34 round 5 shapes (E1-E23 provider names holding an encounter word and charges in visit notes, T1-T9 bill tables, U1-U2 UB-04 spans), through store.charge_service_date; the final list of all 58 STATED results was checked by hand against each text (probe_r5.out)\",\n  \"corpus_blanks.py on f9c0faf and ad0d91a: every BILLED CHARGES line of the 25 cases, all_accepted and counted (corpus_blanks_*.out, corpus_blanks.diff): 37 lines, 22 blank, 15 dated on f9c0faf; 0 blank on ad0d91a\",\n  \"letters_dump_r5.py: in-process letters and notes for sample, case_09, lib14, lib10, lib11 and the round 2-4 variants plus 9 round 5 variants (letters_dump_r5.out, letters/); fullpipe_r5.py: 17 round 5 variants through the full pipeline and letter on f9c0faf (fullpipe_r5.out, fullpipe_r5_tables.out) and 8 of them on ad0d91a (fullpipe_r5_on_ad0d91a.out); eval_teeth_r5.py: letter_check on the build's line vs the blank and the true date (eval_teeth_r5.out)\",\n  \"Playwright on the running archive (h.py + p01_cases.py): sample, case_09, lib14, lib10, lib11 keyboard-first through Steps 1-4, every Step 3 card logged and screenshotted, letters and notes downloaded (ui-<case>-letter.txt, ui-<case>-notes.txt, p01.out); drafting took 2.3-2.5 s per case\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 3, \"letter_dates_correct_on_corpus\": 5, \"adversarial_dates_correct\": 3, \"blank_in_demand_letter\": 3},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"A provider name that holds an encounter-list word (MRI, X-Ray, Follow-Up, Evaluation, Exam) makes a bill a 'visit note', so the statement date prints as the date of service; letter_check enforces it (round 4 provider-name class, D-073 clarification not met)\",\n   \"evidence\": \"fullpipe_r5.out (case_09 record 2 or a new sample record 10, a bill dated after the service, the service date stated in the bill): m1 Source 'Austin MRI', 2026-06-20, 'Date of service 05/29/2026. Cervical spine MRI, CPT 72141, charge $2,150.' -> 'Austin MRI, June 20, 2026: $2,150.00', date violations: []; m2 'Open MRI of Austin' -> June 20; c1 'Hobbleton Follow-Up Clinic' 2026-03-01, 'Date of service 2026-02-02. Office visit 99213 charge $275.' -> 'Hobbleton Follow-Up Clinic, March 1, 2026: $275.00'; c2 'Hobbleton X-Ray' -> March 1; c3 'Hobbleton Hand Evaluation Center' -> March 1; c4 'Express Exam Urgent Care' -> March 1. Control m4 'Austin MRI, billing statement' -> the blank. probe_r5.out E1-E7 show the same at the resolver (kind=encounter). eval_teeth_r5.out M1 and C1: the build's line -> []; the blank -> 'an encounter record's line must carry the record's own date'; the true date -> 'the line prints a date no source ties to it'. Cause: app/backend/encounter_types.json:8-9 lists 'mri', 'x-ray', 'ct scan', 'ultrasound', 'follow-up', 'evaluation', 'exam', 'consult', 'new patient' (and 'visit'), and service_date.py:54 matches them anywhere in the Source label, provider name included; evals/letter_check.py:255 reads the same table, so it shares the blind spot. The same lines print on ad0d91a (fullpipe_r5_on_ad0d91a.out): not a regression, but the round 4 blocker 3 class is not closed.\",\n   \"why_it_matters\": \"D-073's clarification says a provider name is never enough. Imaging centers are commonly named for the study ('Austin MRI', 'Open MRI of ...'). Their bills arrive on letterhead and get logged under the name alone, which is the same habit that produced the 19 provider-only labels in our corpus. In m1 the letter tells the adjuster the MRI was done on June 20, the bill's date, while the bill says 05/29. The quote printed under the line has no date, so a quick check against the quote will not catch it. The eval would push back a correct fix.\",\n   \"fix\": \"Split the encounter words in two. Unambiguous document-type words ('note', 'progress note', 'discharge summary', 'run report', 'operative report', 'ER record') match anywhere. Words that also name services or providers ('visit', 'mri', 'x-ray', 'ct scan', 'ultrasound', 'exam', 'evaluation', 'consult', 'follow-up', 'new patient') match only after the provider part of the label, i.e. after its first comma ('Austin Imaging, cervical MRI', 'Capital PT, visit 9', 'Hill Country Pain Management, follow-up'). A label with no comma that has only an ambiguous word is of unknown type and gets the blank. Mirror this in letter_check with its own matcher, and state the rule in the JSON _doc.\",\n   \"acceptance_test\": \"fullpipe_r5.py m1, m2, c1, c2, c3 and c4 each print '<provider>, date of service [__________] (statement dated ...)'. The sample's 'Austin Imaging, cervical MRI, May 29, 2026: $2,150.00' and the corpus's 15 dated lines are unchanged. letter_check reports a violation on 'Austin MRI, June 20, 2026: $2,150.00' and accepts the blank.\"},\n  {\"severity\": \"major\",\n   \"title\": \"The blank says '(statement dated X)' on records that are not statements (19 of 22 corpus blanks are ED, urgent-care, imaging or radiology records), and Step 3 says the date 'is the statement date, not the service date' when it is the visit's own date\",\n   \"evidence\": \"ui-lib11-letter.txt:37 'Wexcombe Memorial ED, date of service [__________] (statement dated March 18, 2026): $3,260.00' over the record 'Date: 2026-03-18 / Source: Wexcombe Memorial ED / Excerpt: \\\"Dx: cervical strain, lumbar strain. X-ray ... negative for fracture. ED charge: $3,260.\\\"'. Screenshot lib11-s3-00-a1.png shows that record beside the card headed 'Wexcombe Memorial ED · statement dated March 18, 2026' with 'The date in parentheses is the statement date, not the service date.' (app/frontend/guided/step3.js:37 adds that sentence whenever the text contains '(statement dated'). ui-lib14-letter.txt gives the same for 'Orrin Mere Regional ED' (record: 'Dx: cervical strain ... ED charge: $2,960.'). The handoff counts 19 such lines ('header date was the record's'). Identified visit notes get the same words: probe_r5.out probe_r4 T1, 'Capital PT, visit 9, date of service [__________] (statement dated March 6, 2026): $1,665.00', and probe_r3c C3 'Central ER discharge summary, date of service [__________] (statement dated January 9, 2026)'. Source: service_date.py:105-109 not_stated_text always writes 'statement dated'.\",\n   \"why_it_matters\": \"The letter goes to the adjuster. If I fill the blank and leave the parenthetical, the letter says an ED record is a statement. That describes a document that does not exist and invites a 'produce the statement' reply. Step 3 is worse: it tells me the one date I need is not the service date, and sends me to request a bill. For 19 of the 22 blanks in the corpus, the right date is the record date shown on the same screen. This is what makes a blank-heavy letter slow to finish.\",\n   \"fix\": \"Word the parenthetical by record kind. For a bill: '(statement dated X)'. For any other record: '(record dated X)'. Make step3.js test for 'statement dated' and say 'The date in parentheses is the record's date; if this record is the visit itself, that is the date of service' for non-bills. Keep the D-071 blank itself unchanged, and update D-071/D-073 and api.md together.\",\n   \"acceptance_test\": \"The lib11 and lib14 letters read 'Wexcombe Memorial ED, date of service [__________] (record dated March 18, 2026)' and 'Orrin Mere Regional ED, date of service [__________] (record dated September 14, 2026)'. No Step 3 card for a non-bill record contains 'statement date'. case_09 and the lib14 Tarnwick invoice keep 'statement dated'.\"},\n  {\"severity\": \"major\",\n   \"title\": \"A 'Date of service: X  Account: N' line directly over an un-headed row is read as that row's column heading, so the row's other date prints as the date of service; letter_check enforces it\",\n   \"evidence\": \"fullpipe_r5_tables.out t4 (case_09 record 2, 'Hobbleton Family Clinic, billing statement', excerpt 'Date of service: 02/02/2026     Account: 4471' then the row '02/20/2026   Office visit 99213   $275.00') -> 'Hobbleton Family Clinic, billing statement, February 20, 2026: $275.00', date violations: []. The same on ad0d91a (fullpipe_r5_on_ad0d91a.out). eval_teeth_r5.out T4: the build's line -> []; the blank -> 'the quote's date-of-service cell holds one certain date and the line prints a blank'; February 2 -> 'the quote's date-of-service cell reads 2026-02-20'. Cause: service_date.py:263 skips a line with digits as a heading only when it has no service word, so a key-value line with 'Date of service:' and a date becomes the heading. Control t1 (a real Posted/DOS header) -> February 2.\",\n   \"why_it_matters\": \"The record states the date of service as 02/02 and the letter prints 02/20. The quote under the line shows '02/20/2026' next to the charge, so checking the quote confirms the wrong date. This is rated major rather than blocker because it needs this header-block-over-row layout, and the corpus has no bill tables. It is still a wrong date in the letter, and the eval rejects the safe output.\",\n   \"fix\": \"A heading line must not contain a date. A line that holds a date with a 'Date of service' label is a labeled value, not a column heading. When such a line sits over a row whose own date differs, print the blank with both dates in the note. Mirror this in letter_check.\",\n   \"acceptance_test\": \"fullpipe_r5.py t4 prints the blank (or February 2), never February 20. t1 still prints February 2. letter_check flags 'February 20, 2026' for t4 and accepts the blank.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"A several-visit total inside an identified visit note, with no 'visits'/'to date' word, prints the note's date (allowed by D-073 rule 2)\",\n   \"evidence\": \"fullpipe_r5.out p1 (sample record 6, 'Capital PT, visit 9', 2026-03-06, plus 'Physical therapy charges: $1,665.') -> 'Capital PT, visit 9, March 6, 2026: $1,665.00'. The same for p2 'Therapeutic exercise 97110 charges: $1,665.' and p3 'PT course of care charge: $1,665.'. Controls: probe_r5.out probe_r4 T1 'Total for visits 1-9' and T2 'PT charges to date' print the blank. p6 'PT charges for 9 visits' is not a charge.\",\n   \"why_it_matters\": \"$1,665 is 9 × the $185 rate in record 4. Dating it to the discharge visit reads as one $1,665 visit. The line does match its record, so I can see what happened if I open it. This is rated minor because D-073 rule 2 allows it.\",\n   \"fix\": \"When an encounter note's charge exceeds a per-visit rate stated elsewhere in the case for the same provider, print the blank. Or add 'course', 'plan of care' and 'episode' to the several-visits words.\",\n   \"acceptance_test\": \"fullpipe_r5.py p1-p3 print the blank, and p7 'Discharge visit charge $185.' still prints March 6.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from rounds 3 and 4: the notes still say 'fill it from the quote' for quotes with no date (Step 3 now says 'take the date from the matching visit note'), and one single-date blank covers 'visits 1 through 14'\",\n   \"evidence\": \"ui-lib11-notes.txt:39-42, e.g. '- Wexcombe Memorial ED, $3,260: The line states no date of service the code can read ... fill it from the quote or request a dated itemized bill from the provider.' The quote is 'ED charge: $3,260.'. Step 3 for the same item (p01.out, [lib11] s3 item=a1) says 'Take the date from the matching visit note, or request a dated line-by-line bill'. ui-lib11-letter.txt: 'date of service [__________] (statement dated June 15, 2026): $2,310.00' over 'treatment visits 1 through 14 charge $2,310.00'.\",\n   \"why_it_matters\": \"The notes and Step 3 give different instructions for the same line, and there is nothing in the quote to fill from. A 14-visit charge needs a range blank.\",\n   \"fix\": \"Use the Step 3 wording in the notes too. Print 'dates of service [__________]' when the quote counts visits.\",\n   \"acceptance_test\": \"No notes line says 'fill it from the quote' when the quote has no date, and the lib11 $2,310.00 line reads 'dates of service [__________]'.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Carried from rounds 1-4: some charge quotes name neither the service nor the date; with dotted leaders the quote is now the bare figure\",\n   \"evidence\": \"letters/synth_sample_er_dotted_leader-all_accepted-letter.txt:6 'Source [Ex. __ / Bates __]: \\\"$6,240.\\\"' under 'Central ER discharge summary, January 9, 2026: $6,240.00'; ui-lib14-letter.txt 'Source [Ex. __ / Bates __]: \\\"charge $187.05.\\\"'; ui-lib10-letter.txt 'Source [Ex. __ / Bates __]: \\\"FL47 total charges $4,920.00.\\\"'.\",\n   \"why_it_matters\": \"I cannot check the printed date or the service against a quote that is only the figure.\",\n   \"fix\": \"Quote the bill line from its code or description through the figure. With leaders, quote the whole leader line.\",\n   \"acceptance_test\": \"Every charge Source line in the 25-case letters and in the dotted-leader variants contains a service word or code as well as the figure.\"}\n ],\n \"whats_right\": [\n  \"All 115 round 1-4 adversarial texts print the correct date or the blank, and every corpus line that still prints a date is correct (15 of 37; corpus_blanks.diff shows only blanks were added).\",\n  \"The dotted-leader fix reaches the case path: the ER leader variant prints 'Central ER discharge summary, January 9, 2026: $6,240.00' with a total of $8,390.00.\",\n  \"Step 3 cards print exactly the letter's date text for all five cases, and the CHARGES WITHOUT A CERTAIN DATE OF SERVICE section lists every blank.\"\n ],\n \"questions_for_chris\": [\n  \"D-071 fixed the blank's wording as '(statement dated X)' when only bills got a blank. Under D-073, 19 of 22 corpus blanks are ED or urgent-care records. May the parenthetical read '(record dated X)' for records that are not bills?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-03T02:56:45.370Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/draft-T-202-paralegal-r5.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:57:04.452Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/draft-T-202-paralegal-r5.md",
 "old_string": "**Verdict: fail.** D-073 closes most of what rounds 1 to 4 found. All 115 adversarial texts from those rounds now print the correct date or the fillable blank. That includes the three round 4 blockers:",
 "new_string": "**Verdict: fail.** D-073 closes most of what rounds 1 to 4 found. I re-ran all 115 adversarial texts from those rounds against the resolver.\n\n114 of them print the correct date, a period that covers it, or the fillable blank. The one exception is round 4 S7: Source \"Austin Imaging, cervical MRI\" over the excerpt \"Amount due $2,150.00.\" That still prints June 20 at the resolver. In the full pipeline, though, \"Amount due\" is filed as a balance and is never totaled (letters/synth_sample_mri_bill_provider_name-all_accepted-notes.txt:20), so it does not reach the letter.\n\nThe three round 4 blockers are all fixed:"
}
````

### User / tool · 2026-11-03T02:57:04.560Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/draft-T-202-paralegal-r5.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:57:06.606Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/draft-T-202-paralegal-r5.md",
 "old_string": "  \"All 115 round 1-4 adversarial texts print the correct date or the blank, and every corpus line that still prints a date is correct (15 of 37; corpus_blanks.diff shows only blanks were added).\",",
 "new_string": "  \"Every corpus line that still prints a date is correct (15 of 37; corpus_blanks.diff shows only blanks were added), and the round 4 other-visit DOS, treatment-dates and provider-only bills now print the blank.\","
}
````

### User / tool · 2026-11-03T02:57:06.699Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/draft-T-202-paralegal-r5.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:57:09.037Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/draft-T-202-paralegal-r5.md",
 "old_string": "That is a major.\n\n**Scope.**",
 "new_string": "That is a major.\n\n**Scores.** `verify_quickly` is 3, below the ship bar, for two reasons:\n- Each blank sends me to the record with an instruction that is false for 19 of 22 of them.\n- Dated lines from study-named providers can carry a statement date that the eval passes, so I still have to open every dated line's record.\n\n**Scope.**"
}
````

### User / tool · 2026-11-03T02:57:09.133Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/draft-T-202-paralegal-r5.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:57:17.141Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-116-paralegal-r2-jsoncheck.py artifacts/review-evidence/T-202-paralegal-r5/draft-T-202-paralegal-r5.md",
 "description": "Validate draft JSON block and verdict rule"
}
````

### User / tool · 2026-11-03T02:57:17.244Z

**tool result**
````
json blocks: 1
verdict: fail | severities: ['blocker', 'major', 'major', 'minor', 'minor', 'minor']
verdict rule expects: fail | matches: True
model: claude-opus-5-5 | card: T-202 | persona: paralegal-reviewer
all finding fields present
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:57:19.202Z

**tool call — Bash**
````
{
 "command": "cp artifacts/review-evidence/T-202-paralegal-r5/draft-T-202-paralegal-r5.md reviews/T-202-paralegal-r5.md && python3 tools/board.py validate reviews/T-202-paralegal-r5.md",
 "description": "Publish review and run board validator"
}
````

### User / tool · 2026-11-03T02:57:19.340Z

**tool result**
````
ok (1 file(s))
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:57:20.172Z

Now recording the memory.

### Assistant · claude-opus-5-5 · 2026-11-03T02:57:29.765Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r5-d073-patterns.md",
 "content": "---\nname: t202-r5-d073-patterns\ndescription: T-202 r5 (f9c0faf, D-073 two-source fallback) fail: study/service words in encounter list (MRI, X-Ray, Follow-Up, Exam, Evaluation) let provider names lend statement dates; '(statement dated X)' on ED records; key-value DOS line read as column heading\nmetadata:\n  type: project\n---\n\nReview file: reviews/T-202-paralegal-r5.md (f9c0faf). Verdict: fail, with 1 blocker, 2 majors and 3 minors.\n\n**Fixed by D-073.** At the resolver, 114 of the 115 r1-r4 probes give the right date, a period that covers it, or the blank. The exception is r4 S7, a bill under the label \"..., cervical MRI\"; its \"Amount due\" is filed as a balance, so it never reaches the letter. In the corpus, 22 of 37 lines became blanks and no dated line changed. Dotted leaders now work on the case path.\n\n**Blocker: the encounter list keeps service words.** It still holds service/study words (mri, x-ray, follow-up, evaluation, exam, visit), matched anywhere in Source. Provider names like \"Austin MRI\" or \"Hobbleton Follow-Up Clinic\" therefore lend their statement date. letter_check shares the table, so it rejects the blank. Same result on the parent; this is the r4 blocker 3 class.\n\n**Majors**\n- not_stated_text always writes \"(statement dated X)\". 19 of the 22 blanks sit on ED/UC records, and step3.js:37 says the date \"is the statement date, not the service date\".\n- A \"Date of service: X  Account: N\" line sits right over an un-headed row and is read as the row's column heading (service_date.py:263), so the row's other date prints.\n\n**Mechanics that worked**\n- Fixture-backend letters_for drops amounts from unrecorded text that the classifier calls a balance or \"names no service\". Phrase probes as \"<service> CPT <code>, charge $X\" so they reach the letter.\n- fullpipe_r5.py takes ONLY= and runs on any archive.\n- Port 7985, PID 4950.\n\n**Why:** each allow/deny list moves risk to a neighbouring shape. Next round:\n- Probe provider names built from each remaining encounter word.\n- Probe the blank's parenthetical against the record kind.\n\n**How to apply:**\n- Scripts are in artifacts/review-evidence/T-202-paralegal-r5/. probe_r5.py loads r2-r4 by ast (PROBES and the r4 NEW list).\n- corpus_blanks.py diffs any two archives.\n\nRelated: [[t202-r4-encounter-patterns]], [[t200-undated-charge-label]].\n"
}
````

### User / tool · 2026-11-03T02:57:29.866Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t202-r5-d073-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:57:31.667Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-200 undated charge label]",
 "new_string": "- [T-202 r5 D-073 patterns](t202-r5-d073-patterns.md) — f9c0faf fail: MRI/X-Ray/Follow-Up provider names lend statement date; 'statement dated' on ED blanks; KV DOS line as heading\n- [T-200 undated charge label]"
}
````

### User / tool · 2026-11-03T02:57:31.770Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-opus-5-5 · 2026-11-03T02:57:35.221Z

Fail: 1 blocker (a bill from a provider whose name contains MRI, X-Ray, Follow-Up, Evaluation or Exam prints its statement date as the date of service, and letter_check passes it), 2 majors (non-bill blanks such as ED records are labelled "statement dated", and the Step 3 card says that date is not the service date; a "Date of service: X" line is read as a column heading) and 3 minors; the corpus lines that still print a date are all correct, and with that label fixed a letter with many blanks would be usable for a demand — /Users/arsis/zlayt-pm-project/reviews/T-202-paralegal-r5.md (port 7985, PID 4950 stopped; evidence in /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-202-paralegal-r5/).
