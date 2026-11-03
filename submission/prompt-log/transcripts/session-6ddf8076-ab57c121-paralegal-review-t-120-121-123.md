# Subagent: Paralegal review T-120/121/123 (Paralegal review T-120/121/123)

Source: `agent-ab57c121904eb9784.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:14:42.307Z

You are the paralegal reviewer for board cards T-120 (interpreter sentence not flagged as a prior condition), T-121 (one-line letter entry form, Spanish translation note as a bracketed removable phrase) and T-123 (accident baseline never names same-day paperwork as first treatment) in /Users/arsis/zlayt-pm-project. Read each with `python3 tools/board.py show T-###`.

Run the app from a `git archive HEAD` copy in your scratchpad on a spare port: fixture backend, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad. Exercise each behavior on the relevant case, using the sample or library cases. Judge it as a Texas PI paralegal drafting a demand letter.

Write one file per card, reviews/T-###-paralegal.md. Each needs a ```json block of real values: card, persona paralegal-reviewer, model claude-haiku-5-5, verdict, findings. Stop your server by PID. Reply in 3 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T11:14:46.110Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/paralegal.md"
}
````

### User / tool · 2026-11-02T11:14:46.117Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T11:14:46.535Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-120 && echo ---- && python3 tools/board.py show T-121 && echo ---- && python3 tools/board.py show T-123",
 "description": "Show the three board cards T-120, T-121, T-123"
}
````

### User / tool · 2026-11-02T11:14:46.788Z

**tool result**
````
---
id: "T-120"
title: "No prior-condition flag on an interpreter sentence ('Hx obtained via patient's son, who interpreted')"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T10:41:17Z"
updated_at: "2026-11-02T11:14:34Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:02:21Z"
rounds: 0
commits: ["1cb8707"]
reviews: []
ac:
  - {"n": 1, "text": "lib09 raises no 'Mention of a prior or pre-existing condition' flag on the interpreter-history sentence of record 2; a real prior-condition mention in another record still raises the flag (unit test for both)", "done": true, "evidence": "tests/unit/test_t120_history_source_sentence.py::test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes; real prior mentions still hit (REAL rows)"}
  - {"n": 2, "text": "tests/unit covers the rule so it cannot regress; evals report unchanged otherwise", "done": true, "evidence": "17 tests in test_t120_history_source_sentence.py; fixture evals.run flag precision/recall all 1.000, no change"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T10:41:20Z frontend: Filed by frontend from T-060 pass-2 paralegal F13 (reviews/T-060-paralegal-pass2.md). Frontend cannot change it: the flag comes from the backend flag engine.
- 2026-11-02T11:02:21Z backend: claimed
- 2026-11-02T11:11:30Z backend: AC 1 checked: tests/unit/test_t120_history_source_sentence.py::test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do passes; real prior mentions still hit (REAL rows)
- 2026-11-02T11:11:31Z backend: AC 2 checked: 17 tests in test_t120_history_source_sentence.py; fixture evals.run flag precision/recall all 1.000, no change
- 2026-11-02T11:11:31Z backend: moved in_progress -> in_review
- 2026-11-02T11:14:34Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer

## Handoff
What changed: lexicon_scan skips a pre_existing hit on bare Hx/h/o/PHx/history directly followed by a source phrase (obtained/taken/provided... via/from/by, or per/via). Code guard; lexicon.yaml untouched (researcher-owned). How verified: new tests; evals.run fixture flag P/R 1.000. Surprised: dropping the lexicon flag renumbered lib09 record 1 flag ids, so the J4 fixture key missed (see T-125). Left: none.

----
---
id: "T-121"
title: "Letter text: optional one-line entry form, and the Spanish translation note as a bracketed removable phrase (paralegal T-060 pass 2 F9)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T10:41:20Z"
updated_at: "2026-11-02T11:14:34Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:11:33Z"
rounds: 0
commits: ["c26ff04"]
reviews: []
ac:
  - {"n": 1, "text": "GET /export accepts an option (e.g. ?style=oneline) giving one line per entry: 'date — provider: \"quote\" [Ex. __ / Bates __]' built by code; the default letter is unchanged and still equals evals/golden", "done": true, "evidence": "tests/unit/test_t121_letter_styles.py (oneline, config/page, standard==golden, API ?style) + test_export.py golden byte-equal pass"}
  - {"n": 2, "text": "In every letter style an AI-translation note is a bracketed phrase at the end of the entry, [AI translation of the Spanish original; check before sending], never a line that starting with 'AI translation:'; golden and unit tests updated", "done": true, "evidence": "test_translation_note_is_a_bracketed_phrase_at_the_end_of_the_entry_in_both_styles; test_spanish_records/test_d050 updated"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T10:41:23Z frontend: Filed by frontend from T-060 pass-2 paralegal F9. The letter is built by the server and the UI copies it verbatim, so the prefix/layout cannot change in app/frontend. Frontend side is done: letter box sized to its text, Download .txt for letter and notes (T-060 r3).
- 2026-11-02T11:11:31Z backend: AC 1 checked: tests/unit/test_t121_letter_styles.py (oneline, config/page, standard==golden, API ?style) + test_export.py golden byte-equal pass
- 2026-11-02T11:11:31Z backend: AC 2 checked: test_translation_note_is_a_bracketed_phrase_at_the_end_of_the_entry_in_both_styles; test_spanish_records/test_d050 updated
- 2026-11-02T11:11:33Z backend: claimed
- 2026-11-02T11:11:34Z backend: moved in_progress -> in_review
- 2026-11-02T11:14:34Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer

## Handoff
What changed: export.build_export/build_letter take style (standard|oneline); GET /export?style= (422 invalid_style otherwise); translation label becomes a bracketed note at the end of the entry in both styles; api.md updated. How verified: new tests, golden byte equality. Left: frontend can add a style toggle (note for frontend). Surprised: none.

----
---
id: "T-123"
title: "Accident baseline: never call same-day paperwork or questionnaire/authorization headers the first recorded treatment (T-116 r5 major)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T10:50:55Z"
updated_at: "2026-11-02T11:14:34Z"
claimed_by: "backend"
claimed_at: "2026-11-02T10:55:45Z"
rounds: 0
commits: ["0c47356"]
reviews: []
ac:
  - {"n": 1, "text": "Accident-baseline text uses the warn wording for same-day paperwork and questionnaire/authorization headers; tests with the reviewer's r5 probes", "done": true, "evidence": "tests/unit/test_t123_baseline_same_day_paperwork.py (21) + test_t116_gap_endpoints.py pass; r5 headers probe: first_recorded_treatment=False for all 11 headers; B2 same-day both orders name no paperwork as treatment"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T10:55:45Z backend: claimed
- 2026-11-02T11:11:30Z backend: AC 1 checked: tests/unit/test_t123_baseline_same_day_paperwork.py (21) + test_t116_gap_endpoints.py pass; r5 headers probe: first_recorded_treatment=False for all 11 headers; B2 same-day both orders name no paperwork as treatment
- 2026-11-02T11:11:30Z backend: moved in_progress -> in_review
- 2026-11-02T11:14:34Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer

## Handoff
What changed: conflicts.accident_date_conflicts uses the warn wording whenever ANY record on the earliest date is paperwork (alone or sharing the date with a visit, either order); gaps admin list gains bare questionnaire and authorization request (header-only). An older test that asserted no warning for same-day paperwork was updated to the r5 reading. How verified: new tests, r5 probe scripts, unit suite green except test_summary_trim (another worker's in-flight summary_trim.py). Left: none. Surprised: the J4/judge keys do not matter here; wording is code-only.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:14:50.220Z

**tool call — Bash**
````
{
 "command": "git log --oneline -8 && echo ---- && git cat-file -t 1cb8707 c26ff04 0c47356 2>&1; echo ---- && git rev-parse HEAD && echo ---- && cat docs/RUNBOOK.md | head -80 && echo ---- && ls && echo ---- && ls evals/golden app 2>&1 | head -40",
 "description": "Check git state, runbook, and project layout"
}
````

### User / tool · 2026-11-02T11:14:50.393Z

**tool result**
````
63e18ed fix(backend): T-112 r3 summary trim keeps abbreviation expansions, no bare-noun fragments
c26ff04 feat(backend): T-121 optional one-line letter style (?style=oneline) and bracketed removable AI-translation note
c89ac86 docs(orchestrator): D-057 rule-filtered model proposals are listed collapsed, not dropped
4e294d7 test(backend): T-125 record the lib09 f_r1_1 J4 answer live (claude-cli); T-120 renumbered the flag so the old key missed
0410c52 test(evals): T-113 live 3-run on e1ce8dc, ship_bar_met, J3 v6 16/16 caught 0 false agree
1cb8707 fix(backend): T-120 a history-source sentence (Hx obtained via ...) is not a prior-condition mention
0c47356 fix(backend): T-123 accident baseline never calls same-day paperwork or questionnaire/authorization headers the first recorded treatment
d56328a test(e2e): declare sort, copy-confirm, btn-copy-anyway in the hook contract (T-124)
----
fatal: too many arguments

usage: git cat-file <type> <object>
   or: git cat-file (-e | -p | -t | -s) <object>
   or: git cat-file (--textconv | --filters)
                    [<rev>:<path|tree-ish> | --path=<path|tree-ish> <rev>]
   or: git cat-file (--batch | --batch-check | --batch-command) [--batch-all-objects]
                    [--buffer] [--follow-symlinks] [--unordered]
                    [--textconv | --filters] [-Z]

Check object existence or emit object contents
    -e                    check if <object> exists
    -p                    pretty-print <object> content

Emit [broken] object attributes
    -t                    show object type (one of 'blob', 'tree', 'commit', 'tag', ...)
    -s                    show object size
    --[no-]use-mailmap    use mail map file
    --[no-]mailmap ...    alias of --use-mailmap

Batch objects requested on stdin (or --batch-all-objects)
    --batch[=<format>]    show full <object> or <rev> contents
    --batch-check[=<format>]
                          like --batch, but don't emit <contents>
    -Z                    stdin and stdout is NUL-terminated
    --batch-command[=<format>]
                          read commands from stdin
    --batch-all-objects   with --batch[-check]: ignores stdin, batches all known objects

Change or optimize batch output
    --[no-]buffer         buffer --batch output
    --[no-]follow-symlinks
                          follow in-tree symlinks
    --[no-]unordered      do not order objects before emitting them

Emit object (blob or tree) with conversion or filter (stand-alone, or with batch)
    --textconv            run textconv on object's content
    --filters             run filters on object's content
    --[no-]path blob|tree use a <path> for (--textconv | --filters); Not with 'batch'
    --[no-]filter <args>  object filtering

----
63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6
----
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
----
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
data
deploy
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
----
app:
README-arch.md
__init__.py
__pycache__
backend
db
frontend
llm
main.py
pipeline.py

evals/golden:
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:14:51.505Z

**tool call — Bash**
````
{
 "command": "ls .claude/agent-memory/paralegal-reviewer/ && echo ---- && cat .claude/agent-memory/paralegal-reviewer/MEMORY.md | head -5 && echo ---- && ls reviews | tail -40 && echo ---- && ls -la /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad 2>&1 | head",
 "description": "List memory, reviews, and scratchpad; read runbook head"
}
````

### User / tool · 2026-11-02T11:14:51.761Z

**tool result**
````
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
----
- [Spec review patterns](feedback_spec_review_patterns.md) — check absolute claims vs the doc's own example; grep every named category/R-ID/fixture
- [Golden-set recurring findings](golden-set-recurring-findings.md) — T-015: must/should levels, shared type+cite flags, export/§6 drift, dead checks via key drift (mutation-test)
- [Reviewer hook constraints](reviewer-hook-constraints.md) — board.py allowed verbs, python heredoc form, write-allowed dirs
- [Reviewer tooling quirks](feedback_reviewer_tooling_quirks.md) — sed -i and python -c with backticks are hook-blocked; review files are append-only (proofread before the one Write)
- [Frontend review patterns](frontend-review-patterns.md) — T-043: mock vs harness coverage, keyboard focus yank, recurring minor gaps
----
T-100-staff-engineer.md
T-101-staff-engineer-r2.md
T-101-staff-engineer.md
T-102-staff-engineer-r2.md
T-102-staff-engineer.md
T-103-staff-engineer-r2.md
T-103-staff-engineer-r2b.md
T-103-staff-engineer-r3.md
T-103-staff-engineer-r4-CORRECTION-1.txt
T-103-staff-engineer-r4.md
T-103-staff-engineer.md
T-104-ux-designer.md
T-106-staff-engineer-r2.md
T-106-staff-engineer.md
T-107-security.md
T-108-staff-engineer-r2.md
T-108-staff-engineer.md
T-109-staff-engineer-r2.md
T-109-staff-engineer.md
T-110-paralegal-r2.md
T-110-paralegal-r3.md
T-110-paralegal.md
T-111-claims-adjuster-r2.md
T-111-claims-adjuster.md
T-112-staff-engineer-r2.md
T-112-staff-engineer.md
T-114-paralegal-r2.md
T-114-paralegal.md
T-115-staff-engineer-r2.md
T-115-staff-engineer.md
T-116-paralegal-r2.md
T-116-paralegal-r3.md
T-116-paralegal-r4.md
T-116-paralegal-r5.md
T-116-paralegal.md
T-117-ux-designer.md
T-118-paralegal.md
T-119-staff-engineer-r2.md
T-119-staff-engineer.md
T-124-staff-engineer.md
----
total 240960
drwx------@ 1014 arsis  wheel    32448 Nov  2 05:14 .
drwx------@    4 arsis  wheel      128 Nov  1 23:12 ..
drwx------@    2 arsis  wheel       64 Nov  2 00:28 .x
-rw-r--r--@    1 arsis  wheel      311 Nov  2 01:13 641ed.bak
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M1
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M1_nocombine
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M2
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M2_find0
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M3
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:14:54.780Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh 2>/dev/null | head -60; echo ----; grep -rn \"ZLAYT_MODE\\|ZLAYT_DB\\|LLM_BACKEND\" app/config.py 2>/dev/null | head -30; echo ----; ls reviews | grep -i \"T-060\\|T-116\"; echo ----; cat .claude/agent-memory/paralegal-reviewer/t060-ui-polish-patterns.md | head -60",
 "description": "Read serve script, config env vars, and prior T-060 memory"
}
````

### User / tool · 2026-11-02T11:14:54.894Z

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
----
----
T-060-accessibility-pass1.md
T-060-accessibility-pass2.md
T-060-accessibility-pass3.md
T-060-paralegal-pass1.md
T-060-paralegal-pass2.md
T-060-ux-designer-pass1.md
T-060-ux-designer-pass2.md
T-060-ux-designer-pass3.md
T-116-paralegal-r2.md
T-116-paralegal-r3.md
T-116-paralegal-r4.md
T-116-paralegal-r5.md
T-116-paralegal.md
----
---
name: t060-ui-polish-patterns
description: T-060 pass 2 (b89b9d9): what to re-check on the review UI (keyboard queue, density, export box, F13 false positive); review-file slips to avoid
metadata:
  type: feedback
---

Pass 1 majors (keyboard across panels, needs-review first, accept-blocks-export, gap 42 to 40, tall charge rows) were fixed or reduced by 3e3f3b7/eabe2b8/9fcae9b. Still open at b89b9d9: summary+Source letter lines with "AI translation:" prefix, interpreter-sentence prior-condition flag (lib09), 133 px charge rows, accepted rows keep blue Accept, mouse batch button skips the confirm Shift+A shows, `o` modal swallows `a`, no download.

**Why:** pass 2 used a fixed script set (q0-q13 under artifacts/review-evidence/T-060-pass2/); reuse them for a pass 3.

**How to apply:** after a library load by mouse, Tab starts at the page bottom (sequential focus start is the clicked button); start keyboard runs from the "N date to confirm" chip. The server's first Tab/`j` from a radio is ignored (typing guard).

**Review-file slip to avoid:** the file is append-only. Before the single Write, count severities with the jsoncheck script (I wrote "9 minors" in prose, JSON had 11) and recount list items you describe ("5 panels" listed 6). Do not cite pass-1 numbers you did not measure. Related: [[reviewer-tooling-quirks]], [[frontend-review-patterns]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:14:56.938Z

**tool call — Bash**
````
{
 "command": "grep -n \"F9\\|F13\" reviews/T-060-paralegal-pass2.md | head -20; echo ----; cat .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md; echo ----; grep -rn \"ZLAYT_MODE\" --include=*.py --include=*.md --include=*.sh . 2>/dev/null | grep -v node_modules | head -15; echo ----; grep -rn \"ZLAYT_DB\\|FIXTURE_SET\" --include=*.py app | head",
 "description": "Find F9/F13 context and config env var usage"
}
````

### User / tool · 2026-11-02T11:14:58.332Z

**tool result**
````
3:Verdict: **pass** (0 blockers, 0 majors, 9 minors, 1 nit). All five pass-1 majors are fixed or reduced to minors. I can now review both cases in page order from the keyboard, with no re-positioning clicks. On lib09 I decided all 19 items one by one and reached "Ready to export" first try, where pass 1 needed a forced dismiss. Information density and letter format are the weak parts; the letter text is still not paste-ready (F9).
42:| F9 | Letter repeats summary and quote; "AI translation:" prefix | **Open** | `task2-export-letter.txt` lines for April 14, May 3 and May 20 start with "AI translation:"; every entry is summary line then `Source [Ex. __ / Bates __]: "quote"` |
46:| F13 | Prior-condition flag on an interpreter sentence | **Open** | `12c-flags.png`: "Hx obtained via patient's son, who interpreted." still raised; the card now says "The phrase list found this flag but the AI did not; check that it applies." which is honest, and the dismissal is listed in the notes under FLAGS DISMISSED |
51:**F9 (minor, spec D-002 preference).** Letter lines print a summary line plus a `Source [Ex. __ / Bates __]: "quote"` line, and Spanish entries carry the literal prefix "AI translation:" in the letter. Checklist 19 asks for one line `date — provider: "quote" [Ex. __ / Bates __]`; all four parts are present, so this is length and cleanup, not missing content. Fix: option for the one-line form; make the translation note a bracketed removable phrase. Test: letter option exists that gives one line per entry; no line starts with "AI translation:" in the default letter.
53:**F13 (minor).** An interpreter note raises "Mention of a prior or pre-existing condition". The tool says so itself, but I still have to read and dismiss it, and it is the first flag I see in lib09's pre-existing panel. Fix: backend skips "Hx obtained via ..." for this flag. Test: lib09 raises no prior-condition flag.
79:1. F9 one-line letter option and no "AI translation:" in the default text (the paste step).
80:2. F13 no prior-condition flag on "Hx obtained via ...".
----
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
----
artifacts/review-evidence/T-056-paralegal-r2-api.py:17:os.environ["ZLAYT_MODE"] = "local"
artifacts/review-evidence/T-076-paralegal-r2-check.py:4:LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local). Checks, on case_01 record 8 (undated phone note):
artifacts/review-evidence/T-098-staff-engineer-probe2.py:6:for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
artifacts/review-evidence/T-068-paralegal-confirm.py:1:"""T-068 paralegal review, committed build 89a323a on :7881 (fixture/curated, ZLAYT_MODE=local).
artifacts/review-evidence/T-099-staff-engineer-probe-states.py:5:for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
artifacts/review-evidence/T-098-staff-engineer-probe3-verdicts.py:6:for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
artifacts/review-evidence/T-081-ux-r3-walk6.py:1:"""R3 walk 6: demo-mode server (:7892, no ZLAYT_MODE=local) first viewport, and the narrative stepper at 390 on a fresh sample."""
artifacts/review-evidence/T-116-paralegal-lib09-api.py:4:os.environ.update({"LLM_BACKEND": "fixture", "ZLAYT_MODE": "local"})
artifacts/review-evidence/T-098-staff-engineer-r2-probe3.py:10:for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
artifacts/review-evidence/T-096-ux-designer-walk.py:2:(LLM_BACKEND=fixture, ZLAYT_MODE=local, scratch ZLAYT_DB). Usage: python -I this.py <archive_root> <scratch_dir>
artifacts/review-evidence/T-096-ux-designer-walk.py:110:        # ---- setup: three dismissals of the lexicon phrase so the real route offers the banner on the next case (ZLAYT_MODE=local)
artifacts/review-evidence/T-114-paralegal-api-checks.py:3:Targets a server started from a `git archive HEAD` copy (b5fb35c) on its own port, fixture backend, ZLAYT_MODE=local.
artifacts/review-evidence/T-053-security-ui-probe.py:20:    e = {k: v for k, v in os.environ.items() if k not in ("ZLAYT_MODE", "ANTHROPIC_API_KEY", "LLM_BACKEND", "ENABLE_LIVE")}
artifacts/review-evidence/T-053-security-ui-probe.py:35:                                  env=env({"ZLAYT_MODE": "local", "PORT": str(LT), "DATA_DIR": tmp + "/local"}), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
artifacts/review-evidence/T-116-paralegal-r2-lib09-api.py:7:os.environ.update({"LLM_BACKEND": "fixture", "ZLAYT_MODE": "local"})
----
app/llm/backends/fixture.py:13:    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
app/llm/backends/fixture.py:16:    name = os.environ.get("FIXTURE_SET", "").strip()
app/llm/backends/fixture.py:24:        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
app/backend/api.py:94:    db_path = db_path or os.environ.get("ZLAYT_DB") or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")   # ZLAYT_DB (a file) wins; tools/serve_app.sh sets it
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:00.460Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-114-paralegal-api-checks.py | head -70; echo ----; grep -n \"PORT\\|uvicorn\\|def main\" app/main.py | head; echo ----; ls evals/ tests/ | head -40; echo ---; sed -n 1,40p tests/unit/test_t120_history_source_sentence.py 2>/dev/null",
 "description": "Read prior API check script, main.py port handling, and T-120 tests"
}
````

### User / tool · 2026-11-02T11:15:00.566Z

**tool result**
````
"""T-114 paralegal-reviewer API checks (stdlib only; run with: .venv/bin/python -I <this file> [base_url]).

Targets a server started from a `git archive HEAD` copy (b5fb35c) on its own port, fixture backend, ZLAYT_MODE=local.
Checks:
  A. lib09 rate rows: accepting a rate is an acknowledge (accept_effect), never a JUDGE_NOT_RUN blocker, never in the total.
  B. every acceptable item on all 15 library packets: no JUDGE_NOT_RUN at the gate, export status, two variants
     (dates confirmed to the first candidate; dates left unconfirmed).
  C. confirm_date on lib09 record 4 returns gap_changes (42 -> 40) and the flag endpoints.
Prints a JSON summary to stdout and writes the same to artifacts/review-evidence/T-114-paralegal-api-checks.out.json.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:7881"
LIB09 = "case_lib09_spanish_interpreter_espalda"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "T-114-paralegal-api-checks.out.json")


def req(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(BASE + path, data=data, method=method, headers={"content-type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=120) as x:
            return x.status, json.loads(x.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"null")


def load(lib_id):
    st, body = req("POST", "/api/cases", {"library": lib_id})
    assert st == 201, (lib_id, st, body)
    tok = body["token"]
    assert req("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(480):
        s = req("GET", f"/api/cases/{tok}/status")[1]["status"]
        if s in ("ready", "failed", "done_with_errors"):
            break
        time.sleep(0.25)
    assert s == "ready", (lib_id, s)
    return tok


def gate(tok):
    steps = {x["id"]: x for x in req("GET", f"/api/cases/{tok}/trace")[1]["steps"]}
    return steps["export_gate"]


def jnr(tok):
    return [b["item_id"] for b in gate(tok)["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]


def letter_lines(ex, needle):
    return [ln for ln in ex["letter_text"].splitlines() if needle in ln]


out = {"base": BASE, "A_lib09_rates": {}, "B_library_packets": {"dates_confirmed": {}, "dates_unconfirmed": {}}, "C_gap": {}}

# ---------------------------------------------------------------- A. lib09 rate rows
tok = load(LIB09)
case = req("GET", f"/api/cases/{tok}")[1]
amts = {a["id"]: a for a in case["amounts"]}
rates = [i for i, a in amts.items() if a["kind"] == "rate"]
out["A_lib09_rates"]["rates"] = [{"id": i, "text": amts[i]["text"], "accept_effect": amts[i]["accept_effect"],
                                  "judge_required_for_export": amts[i]["judge_required_for_export"],
                                  "judge_verdict": ((amts[i].get("ladder") or {}).get("judge") or {}).get("verdict"),
----
4:import uvicorn
9:    """uvicorn app.main:create --factory"""
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
----
evals/:
__init__.py
__pycache__
adversarial
golden
j3_controls.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
reports
run.py

tests/:
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit
---
"""T-120 (T-060 pass-2 F13): a history-SOURCE sentence ('Hx obtained via patient's son, who interpreted') names who gave the history,
not a prior condition, so the phrase list does not raise 'Mention of a prior or pre-existing condition' on it. A real prior-condition
mention still raises the flag, in the same record and in others. Deterministic code guard in lexicon_scan (the lexicon is researcher-owned)."""
import pathlib

import pytest

from app.backend import flags as FL, ingest as I, lexicon_scan as LS

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = ["Hx obtained via patient's son, who interpreted.", "Hx obtained from patient's daughter.", "Hx taken per interpreter.",
          "History obtained via interpreter.", "History provided by patient's husband.", "hx was obtained through a telephone interpreter.",
          "H/o obtained via family member.", "Hx per patient's son, who interpreted.", "Hx via interpreter."]
REAL = ["Hx of lumbar strain.", "Hx: lumbar strain 2019.", "History of migraines.", "Hx neck pain.", "h/o lumbar strain",
        "Prior history of neck pain 2019, resolved."]


def _prior(text):
    return [h for h in LS.scan(text) if h["flag_type"] == "pre_existing"]


@pytest.mark.parametrize("s", SOURCE)
def test_history_source_sentence_raises_no_prior_condition_hit(s):
    assert _prior(s) == []
    assert _prior(s + " Patient states she was struck by a car. Left shoulder pain 7/10.") == []


@pytest.mark.parametrize("s", REAL)
def test_real_prior_condition_mentions_still_hit(s):
    assert _prior(s)


def test_source_sentence_does_not_hide_a_real_prior_condition_next_to_it():
    t = "Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019. Left shoulder pain 7/10."
    hits = _prior(t)
    assert len(hits) >= 1 and all("lumbar strain" in t[h["unit_start"]:h["unit_end"]] for h in hits)
    t2 = "Hx obtained via patient's son. Prior neck injury in 2018."
    assert _prior(t2)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:06.702Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$SP/t120-123-archive\" && cd /Users/arsis/zlayt-pm-project && git archive HEAD | tar -x -C \"$SP/t120-123-archive\" && ls \"$SP/t120-123-archive\" && echo ---- && for p in 7893 7894 7895; do lsof -iTCP:$p -sTCP:LISTEN -nP | head -2; done; echo \"ports checked\"",
 "description": "Extract HEAD archive into scratchpad and check spare ports"
}
````

### User / tool · 2026-11-02T11:15:07.425Z

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
----
ports checked
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:11.309Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120-123-archive; cd \"$SP\" && LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=\"$SP/../t120-123.sqlite3\" PORT=7893 PYTHONPATH=\"$SP\" PYTHONDONTWRITEBYTECODE=1 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m app.main > \"$SP/../t120-123-server.log\" 2>&1 &\necho \"launcher pid $!\"; sleep 4; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7893/; lsof -iTCP:7893 -sTCP:LISTEN -nP",
 "description": "Start fixture app server on port 7893 from archive copy"
}
````

### User / tool · 2026-11-02T11:15:15.528Z

**tool result (error)**
````
Exit code 1
launcher pid 86792
[1]+  Exit 1                  cd "$SP" && LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB="$SP/../t120-123.sqlite3" PORT=7893 PYTHONPATH="$SP" PYTHONDONTWRITEBYTECODE=1 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m app.main > "$SP/../t120-123-server.log" 2>&1
000
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:18.668Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -5 \"$SP/../t120-123-server.log\"",
 "description": "Read server startup log tail"
}
````

### User / tool · 2026-11-02T11:15:18.751Z

**tool result (error)**
````
Exit code 1
tail: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/../t120-123-server.log: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:21.862Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -5 \"$SCR/t120-123-server.log\"; echo ----; ls \"$SCR\"",
 "description": "Read server log from the scratchpad directory"
}
````

### User / tool · 2026-11-02T11:15:22.042Z

**tool result**
````
/Users/arsis/zlayt-pm-project/.venv/bin/python: Error while finding module specification for 'app.main' (ModuleNotFoundError: No module named 'app')
----
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
T115_card_show.txt
T115_staff_r1
T115_staff_r2
T119_r2
T119_staff_r1
a.sqlite3
a27e3a4.diff
adr013.txt
after.py
ap3500.pdf
api
api2
api_at_099732b.py
api_head.log
api_head.py
api_head.sqlite3
api_md_head.md
api_md_new.md
api_new.py
api_parent.log
api_parent.sqlite3
apitmp
app
app-head
app.log
app.pid
app.sqlite3
app2
app2.log
app2.pid
app2.sqlite3
app3
app60
app60.log
app60.pid
app60.sqlite3
ar2
ar_old
arc
arch
arch_57a08ba
archive
atk
audit.py
base
base1.log
billing.orig
blank.py
body.py
bombs
boom_final.py
boom_server.py
boundary.py
boundary2.py
build_set.py
build_set.py.bak
build_t099_blobs.py
c
c5.json
c8a9874
ca.sh
cal.bak
case.json
case.json.tok
case3.json
case3.json.tok
cases.txt
ce70
ce70-report.md
census.py
charges.py
check.py
check_golden.out
check_json.py
check_r2.py
check_r3_json.py
check_r4.py
chk.py
chk_mut.py
cli1.err
cli1.out
cli1.txt
cli2.err
cli2.out
cli2.txt
cli_c1.err
cli_c1.txt
cli_final.err
cli_head_out.txt
cli_rep1.err
cli_rep2.err
cli_rep3.err
cmscms.py
collapsed.png
collapsed.py
commitcases.txt
copy
copyA
copyC
copy_untracked.py
corp_base.json
corp_r2.json
corpus.py
count.py
cr.sh
cred_b05.py
cred_orig.py
cs.sh
ctl-out
ctl.log
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
dev.db
diag.py
dl
dos
draft-pass2.md
drive.py
e1.py
e1400d4
e2.py
e2e-data
e2e-m1-server.log
e2e-m1.sqlite
e2e-run.sqlite
e2e-server.log
e2e1.log
endpoints.py
env97
es1.txt
ev.json
ev.sh
eval_base.out
eval_r2.out
evalout
evalout2
ex1.sh
ex2.sh
ex3.sh
exp-077
exp.py
exp2.py
exp_077.py
fe-data
fe3.log
fe3.sqlite
fe4.log
fe4.sqlite
fetch
figs.py
fill.py
final-data
final1.log
final2.log
find_miss.py
first.png
flags_commit.py
fr_r2.txt
fresh
fresh.py
fresh_head.log
fresh_head.sqlite3
fresh_nosbs.log
fresh_nosbs.sqlite3
full.log
full.patch
fx
fx_before.txt
fxbak
gen
gen.py
gen_controls.py
golden_scan.py
guardprobe.py
guardprobe.py.bak
h42.py
h60.txt
harness
head
head-a850be0
head-bc12d44
head-ec33bf0
head.db
head.log
head.py
head2
head2.py
head_950d4a5
head_9851a0d_r5
head_9c1af01
head_ae76835_r3
head_clean
head_clean.log
head_clean.sqlite3
head_e63e564
head_faee448_r4
head_nosbs
head_nosbs.log
head_nosbs.sqlite3
head_run.sh
headcheck
headfe
heldout.py
helpers.py
helpers2.py
hookcopy
idx
idx2
ing.bak
ingest.orig
jcheck.py
judge_live.py
judges.png
k1dump.py
kb2.py
kb3.py
kb_test.py
leak.py
lib_app.sqlite
library-after.md
library-base.md
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
m1.txt
m2.txt
m3.txt
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
mine.diff
mine.patch
mine.txt
miss.py
miss2.log
miss2.py
mk.py
mkd.py
mkfix.py
mkpdf.py
mkreview.py
mkreviews.py
mob.py
msg.txt
mut
mut-A
mut-B
mut-C
mut-D
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
mut2
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
mut_dedupe
mut_flagsdeadline
mut_rmfixture
mut_rmjudgefixture
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
mutants
mutants-db08276.log
mutants-r3-db08276.log
mutants-work
mutate.py
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
mw
narr.py
neg
neg2
nucc
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
old
out
overlay-head
p.py
p1.txt
p2.db
p2.py
p2.txt
p3.log
p3.pid
p3.py
p3.sqlite3
p3.txt
p_be
p_fe
pa
page.txt
parent
parent-server.log
parent.sqlite3
pathspec.txt
pdb
pdf_time.py
pdfs
pdfs_head
pid
pid2
pin-690a0e3-r5
pin-6bca-r4
pin-8bc7f90
pin-HEAD-r4
pin-HEAD2-r4
pin-db08276
pin-f218263
pipeline_commit.py
pl.bak
pre_t095_schema.sql
prev
probe
probe-db
probe-r2-output.txt
probe-top.png
probe.py
probe2.py
probe2.py.bak
probe2_t067.py
probe3.py
probe3_t067.py
probe4.py
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
probe_failed.py
probe_head
probe_head_out.txt
probe_nojudge.py
probe_r4_ocr.py
probe_rej.py
probe_run.py
probe_t067.py
probe_timeout.py
probe_work_head
probe_work_head2
probes
probes-t100
probes_r5_dir
proc.png
proc.py
proc2.png
pub.log
pub2.log
r1
r2
r2-cases.out
r2.log
r2.pid
r2.sqlite3
r2_blank_judges.py
r2_check.py
r2_detect.py
r2_es2.py
r2_export.json
r2_for2.py
r2_ids.txt
r2_mixed.py
r2_mut_base
r2_mut_base_m
r2_mutant_r2b.py
r2_mutants.py
r2_probe_out.txt
r2_sentinel_data
r2_set_status.py
r2_t080_app.log
r2_t080_app.sqlite
r2_token.txt
r2_unit.txt
r2arch
r2d.sqlite3
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
r2src
r3
r3-a27
r3-parent
r3_acceptance_strings.py
r3_accepted.json
r3_api.py
r3_check_json.py
r3_gate_check.py
r3_mut
r3_rootcause.py
r3_sentinel_data
r3_server.log
r3_t080.sqlite
r3_tok.txt
r3ap
r3api
r3api2
r3arch
r3bp
r3copy
r3db.sqlite3
r3dev
r3h
r3img
r3m
r3mut
r3o
r3pop
r3probe.py
r3run
r3scripts
r3src
r3tb
r4_probe_8634bfe.out.txt
r4_rootcause.py
r4arch
r4data
r4out
r4pin
r4probe
r4probe_on_0f58181.txt
rail.png
rec.sh
rec_a.log
rec_all.log
rec_all.sh
rec_b.log
rec_judges.log
rec_sample.log
recon.py
replay.py
repo
repro_stale
req_mut.md
rerec.log
rerec.sh
review_commit.py
review_headplus.py
rt_base.json
rt_r2.json
run.base.py
run.head.py
run.log
run.try.py
run_c5.py
run_mutants_r3.py
run_p3_chain.sh
run_ro.py
run_t070_orig.py
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
scan.py
scan_specimens.py
scan_time_10x5000wide.pdf
schema_pre_T095.sql
score.py
scripts
scroll.py
selfcheck-r2.txt
serve_p3_wrapper.py
serve_snap.py
server.log
server.pid
server2.log
server2.pid
server7867.log
shot.py
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
snap2
snap3
snap7942
snap7942.db
snap7942.log
snap7942.pid
snap_run.sh
splice.py
spy3.log
spy3.py
src
srv.KdvV
srv.log
srv.out
srvdir
st_commit.py
states.py
strip.py
sync.py
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
t106_r2_archive
t108
t109_adr_edit.py
t109_doc_edit.py
t109r2_head
t109r2_mutA
t109r2_mutB
t109r2_pin
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
t120-123-archive
t120-123-server.log
t2.q4VB
t2b.IKsK
t3.ORDQ
t4.0u5g
t84r4
tabflow.py
tail.md
test_billing_old.py
tests_b05.py
thr.py
thr2.out
thr2.py
tmpindex
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
two.py
two.py.bak
ub
ui-demo
ui-local
unit-run-r2-clone-with-git.txt
unit-run-r2.txt
unit.txt
unit_full.txt
ux-r2-2.sqlite3
ux-r2-3.sqlite3
ux-r2-debug-sample.png
ux-r2-server-2.log
ux-r2-server-3.log
ux-r2-server.log
ux-r2-server.pid
ux-r2.sqlite3
ux3
v
verify.py
view.json
walk.py
walk2.py
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
wt_m2
wt_r4
wt_run.sh
x45.py
xc.py
xss.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:25.811Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$SCR/t120-123-archive\" && LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=\"$SCR/t120-123.sqlite3\" PORT=7893 PYTHONPATH=\"$SCR/t120-123-archive\" PYTHONDONTWRITEBYTECODE=1 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > \"$SCR/t120-123-server.log\" 2>&1 &\nsleep 5; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7893/; lsof -iTCP:7893 -sTCP:LISTEN -nP; tail -3 \"$SCR/t120-123-server.log\"",
 "description": "Start fixture app server on port 7893 from archive copy"
}
````

### User / tool · 2026-11-02T11:15:31.035Z

**tool result**
````
200
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  87376 arsis    9u  IPv4 0x20fbaf4774bcbc05      0t0  TCP 127.0.0.1:7893 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:34.308Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$SCR/t120-123-archive\"; grep -n \"@app\\.\\(get\\|post\\|put\\|patch\\|delete\\)\\|@router\\.\\(get\\|post\\|put\\|patch\\|delete\\)\" app/backend/*.py | head -60; echo ----; ls evals/library | head -30; echo ----; grep -n \"style\\|export\" memory/contracts/api.md | head -30",
 "description": "List API routes, library cases, and export contract"
}
````

### User / tool · 2026-11-02T11:15:34.436Z

**tool result**
````
app/backend/api.py:212:    @app.get("/api/health")
app/backend/api.py:218:    @app.get("/api/cases")
app/backend/api.py:228:    @app.get("/api/library")
app/backend/api.py:234:    @app.post("/api/cases", status_code=201)
app/backend/api.py:250:    @app.post("/api/cases/pdf", status_code=201)
app/backend/api.py:316:    @app.get("/api/cases/{token}")
app/backend/api.py:325:    @app.delete("/api/cases/{token}", status_code=204)
app/backend/api.py:349:    @app.post("/api/cases/{token}/run", status_code=202)
app/backend/api.py:372:    @app.post("/api/cases/{token}/rejudge")
app/backend/api.py:394:    @app.get("/api/cases/{token}/status")
app/backend/api.py:413:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
app/backend/api.py:425:    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
app/backend/api.py:436:    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
app/backend/api.py:449:    @app.get("/api/cases/{token}/narrative")
app/backend/api.py:458:    @app.post("/api/cases/{token}/narrative")
app/backend/api.py:471:    @app.post("/api/cases/{token}/narrative/review")
app/backend/api.py:486:    @app.get("/api/cases/{token}/items/{item_id}")
app/backend/api.py:498:    @app.post("/api/cases/{token}/items/{item_id}/review")
app/backend/api.py:519:    @app.get("/api/cases/{token}/export")
app/backend/api.py:548:    @app.get("/api/cases/{token}/items/{item_id}/trace")
app/backend/api.py:561:    @app.get("/api/cases/{token}/trace")
app/backend/api.py:570:    @app.get("/api/cases/{token}/judges")
app/backend/api.py:579:    @app.get("/api/cases/{token}/audit")
app/backend/calibration_route.py:201:    @app.get("/api/calibration")
app/backend/billing.py:1061:    @app.get("/api/cases/{token}/billing")
app/backend/case_extras.py:119:    @app.post("/api/cases/{token}/review/batch")
app/backend/case_extras.py:139:    @app.get("/api/cases/{token}/export_config")
app/backend/case_extras.py:148:    @app.put("/api/cases/{token}/export_config")
app/backend/case_extras.py:163:    @app.delete("/api/cases/{token}/export_config")
app/backend/dismissal_patterns.py:92:    @app.get("/api/cases/{token}/dismissal_suggestions")
app/backend/dismissal_patterns.py:101:    @app.post("/api/cases/{token}/dismissal_suggestions/apply")
app/backend/export_routes.py:66:@router.get("/api/cases/{token}/export")
app/backend/pdf_routes.py:11:    @app.get("/api/cases/{token}/pages/{n}/image")
app/backend/reclassify.py:202:    @app.post("/api/cases/{token}/items/{item_id}/reclassify")
----
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
----
11:- `warnings[]` appears on case, ingest, review and export responses. Shape: `{"code": "...", "message": "...", "item_id": null}`.
33:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
34:| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
37:| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
79:Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
110:## /api/cases/{token}/export_config (D-031)
111:`GET` returns `{"exhibit": null|string, "bates_prefix": null|string, "bates_start": null|int}`. `PUT` takes the same keys (all optional; omitted or empty means unset) and returns the stored config; `DELETE` clears it and returns the empty config. Validation: `exhibit` and `bates_prefix` up to 20 characters of `A-Za-z0-9 ._-`; `bates_start` an integer 0 to 99999999 (booleans and strings refused); unknown keys refused; any violation is `422 invalid_edit` and nothing changes. Effect on the export only: every letter citation `Source [Ex. __ / Bates __]` becomes `Source [Ex. <exhibit> / Bates <prefix><NNNN>]` with `NNNN` = first number + record number - 1, zero-padded to 4 digits (first number defaults to 1 when only a prefix is set; an unset part stays `__`). With no config the export is byte-identical to the golden. The internal notes never carry exhibit or Bates numbers.
131:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.
177:      "review_status": "pending", "edited": null, "duplicate_note": null, "accept_effect": "acknowledge", "judge_required_for_export": false,
242:    "ready_to_export": false },
247:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). **T-108:** units are cut from the quotable excerpt body only (no `Excerpt:` label, quote marks or Date/Source/=== lines), at true offsets, and every unit saves on its own: a sentence that a hedge sentence qualifies is ONE combined unit with the hedge sentence(s) after it (the save route's own check decides, Spanish hedge words included), so the picker never builds a quote the route refuses. A record whose Excerpt label cannot be separated from its text (no Date/Source layout) has `sentences: []` and a plain-words `sentences_reason`; the frontend shows no picker for it. `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
327:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; its class changes only through `POST .../reclassify`, never through `edit`); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so "date not stated" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as "date not confirmed, not exported".
334:`message` is a plain sentence naming the words, e.g. `The summary says “left”, which the quote does not say. Remove it or change the quote.` The export gate and accept recompute the same checks from the current wording through the same functions (D-051), so an edit the route stores can never be an export blocker for a code reason. The same rule applies to `POST .../records/{rid}/entry`. (3) Judge 1 re-run: it never blocks a human-written edit (D-045b). If it says `partially`/`unsupported`, errors, times out, or has no recorded fixture (always the case in demo mode), the edit is saved, the item becomes `needs_review` (reason `JUDGE_UNAVAILABLE` when it did not answer) and `warnings[]` carries `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED` or `JUDGE_UNAVAILABLE`; no 409, because nothing the code can verify is wrong. The judge never lets an unchecked edit look verified.
342:              "queue": ["a3", "e4", "e2", "a1"], "ready_to_export": false },
371:## GET /api/cases/{token}/export
372:**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
373:Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). Optional query `style` (T-121): `standard` (default, the golden layout) or `oneline`, which writes one line per entry, `<long date> — <provider>: "<quote>" [Ex. __ / Bates __]` (the bracket follows the export config; a PDF page reads `[Ex. __ / Bates __, p. 3]`), built by code; the charges section is unchanged. Any other value is `422 invalid_style`. The translation note ends the line in both styles. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
378:  "letter_text": "TREATMENT CHRONOLOGY\n\n[... nine entries with their Source lines and BILLED CHARGES: full text is the LETTER_TEXT block of evals/golden/sample.export.expected.txt ...]\n\nBilled charges stated in these records: $8,390.00",
557:  "blocks_export": false,               // true only for steps that stop this item reaching the letter right now (human pending, date unconfirmed)
572:  "verdict": { "code": "needs_attention", "label": "Needs your attention", "blocks_export": true },
577:      "why": "The AI read this record and proposed a one-line summary and a quote.", "reason_code": null, "rule": "row 4", "blocks_export": false,
583:      "reason_code": "JUDGE_PARTIAL", "rule": "row 4", "blocks_export": false,
590:- **entry (and a reviewer-written entry):** `extracted` (llm; a reviewer-written entry shows kind `human` and no model), `summary_trimmed` (code, D-054, present only when code removed summary clauses the quote does not support: `why` lists each as "removed from the summary: not in the quote: '<clause>'"; `evidence.removed`, `evidence.original_summary`, `evidence.kept_summary`; the second AI check saw `kept_summary`), `excerpt_verbatim` (code, `GROUNDING_EXCERPT_NOT_VERBATIM`), `excerpt_whole_sentence` (code, `EXCERPT_NOT_WHOLE_SENTENCE`), `excerpt_hedge` (code, `EXCERPT_OMITS_QUALIFIER`), `summary_tokens` (code, D-034, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `evidence.tokens`), `summary_qualifier` (code, D-022, `SUMMARY_DROPS_QUALIFIER`), `highlight` (code, `HIGHLIGHT_NOT_FOUND`), `date_confirmed` (code, D-041, `DATE_AMBIGUOUS`/`DATE_MISSING`, `blocks_export`), `injection_scan` (code, `INJECTION_SUSPECTED`), `judge_1` (llm), `human`. If the quote fails the word-for-word check or the AI output was malformed, the checks between `extracted` and `highlight` and `judge_1` are `skipped` with that code.
597:`verdict.code`: `accepted` (accepted or edited), `dismissed`, `rejected` (state rejected, kept out of the letter), `needs_attention` (any `fail` step on a live item), `ready_for_decision` (all machine steps pass or are skipped on purpose, human pending), `removed` (narrative sentence only), `waiting_for_run` (AI steps not run yet). `verdict.blocks_export` is true when the item is live and `review_status` is `pending` (it is what `/trace`'s export gate lists). `progress.done` counts steps that are not `pending`.
618:    { "id": "export_gate", "n": 10, "label": "Ready to export?", "kind": "code", "status": "fail", "reason_code": "NOTHING_ACCEPTED",
625:Each case step has the shared step keys plus `counts` (object, may be `{}`); `export_gate` also has `ready` and `blockers[]`. Step order is fixed: `ingest, split, dates, extract, grounding, judges, flags, totals, review, export_gate`. Before the AI run (`status: "ingested"`) `extract`, `grounding`, `judges` and `flags` (AI part) are `pending`; the code-made flags and amounts already count.
627:`verdict.code` for the case: `ready` (export gate open), `needs_attention` (nothing accepted yet, or accepted items not double-checked), `running`, `failed`. The judge's closed `reason_code` is now kept in `ladder.judge.reason_code` for entries, amounts, flags, edits and manual entries (in `ladder_json`; no schema change).
629:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. **D-051 (T-098 r2):** the blocker covers every accepted or edited entry, AI-made or human (only the judge is exempt for human wording). The gate and the item trace recompute all five code checks (summary token D-034/D-047, qualifier dropped D-022, quote whole sentence D-012/D-021, quote omits the hedge sentence, quote is word for word in the record) plus the highlight, from each entry's CURRENT summary and quote, and also honour stored reasons; a stale stored 'pass' cannot hide a failing summary. For an AI draft the blocker `why` says the AI drafted it. `GET /export` is 422 `export_blocked` for such a state; the case verdict label is "N summary/summaries fail(s) a check". The item trace verdict label for a failing accepted entry is "Needs your attention: a check on this summary fails" for an AI draft and "... a check on your wording fails" only when the paralegal wrote or edited the summary. In the internal notes, AI wording that failed a code check is never printed: EDITED ITEMS says "summary was AI wording removed (failed a check: <plain reason>), now ..." and the draft paragraph says "AI wording removed (failed a check: <reason>) (<entry id>)" (a narrative sentence removed for a judge reason is still printed). An unreviewed (pending) draft that fails a code check is listed in the internal notes as "summary not shown, a code check on it fails" so its wording never appears in the export.  **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **T-114 (rates):** every amount in `amounts[]` carries `accept_effect` and `judge_required_for_export`. `accept_effect` is `letter_total` (a `charge`: counted in the billed-charges total), `acknowledge` (a `rate`: accepting it only acknowledges it, it is listed in the internal notes and never totaled, D-019/D-042) or `internal_notes` (`estimate`, `unclear`). `judge_required_for_export` is `false` only for a rate: an accepted rate whose second check never ran is **not** a `JUDGE_NOT_RUN` blocker, so accepting a rate can never block export (its item trace `judge_2` step says the check is optional for a rate). The UI should label a rate's button "Acknowledge" (or keep "Accept as noted") and never promise it goes in the letter. Charges, entries and flags are unchanged. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
648:Run the second check again for the AI-made items whose judge never answered (the items the export gate lists as `JUDGE_NOT_RUN`, plus any live pending ones with no answer: kept on purpose so the `judges` step's RERUN_JUDGE button always has something to do; D-045 note). No body. The same judge (J1 entry, J2 charge, J3 AI conflict, J4 AI flag) gets the same input the run or the edit gave it, so a recorded answer is found again. Same rules as `/run`: `404 not_found`; `409 run_in_progress`; `409 demo_mode_unsupported_input` (demo mode, text not a recorded case); `503 llm_unavailable`. **Demo mode (no `ENABLE_LIVE=1`) is fixture-only**: only recorded answers are replayed, a miss stays unavailable and never calls a model; live calls (`claude-cli` or `anthropic-api` with a key) need `ENABLE_LIVE=1`. Every call is audited in `llm_calls` (judge role, item id, step `j1`..`j4`) and each attempt is appended to the item's `ladder.rejudge[]` `{at, call_id, verdict}`. An answer replaces `ladder.judge` and recomposes `state`/`state_reasons` (other doubts stay; `JUDGE_UNAVAILABLE`/`FIXTURE_MISS` go; an objection adds `JUDGE_PARTIAL|UNSUPPORTED|DISAGREES|UNSURE`); `review_status` is never changed. Nothing can clear the gate except an answer.
653:  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:40.027Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project; sed -n 1,60p artifacts/review-evidence/T-116-paralegal-lib09-api.py; echo ----; sed -n 498,520p app/backend/api.py; echo ----; grep -n \"accident\\|questionnaire\\|authoriz\\|intake\" evals/library/case_lib*.txt | head -40",
 "description": "Read prior lib09 API script and find accident/paperwork mentions in library cases"
}
````

### User / tool · 2026-11-02T11:15:40.167Z

**tool result**
````
import sys, os, time, json, tempfile
ARCH = "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/archive"
sys.path.insert(0, ARCH)
os.environ.update({"LLM_BACKEND": "fixture", "ZLAYT_MODE": "local"})
for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"): os.environ.pop(k, None)
from fastapi.testclient import TestClient
from app.backend.api import create_app
d = tempfile.mkdtemp(prefix="t116lib09_")
c = TestClient(create_app(os.path.join(d, "t.sqlite"), static_dir=d), client=("127.0.0.1", 50000))
tok = c.post("/api/cases", json={"library": "case_lib09_spanish_interpreter_espalda"}).json()["token"]
print("run", c.post(f"/api/cases/{tok}/run", json={}).status_code)
for _ in range(480):
    if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed", "done_with_errors"): break
    time.sleep(0.25)
gaps = lambda: [f for f in c.get(f"/api/cases/{tok}").json()["flags"] if f["type"] == "gap"]
print("BEFORE confirm:", [(f["title"], f["computed"]["days"], f["computed"].get("from"), f["computed"].get("to"), f["computed"].get("excluded_records"), f.get("reasons")) for f in gaps()])
r = c.post(f"/api/cases/{tok}/records/r4/confirm_date", json={"date": "2026-03-05"})
print("confirm status", r.status_code, "gap_changes", r.json().get("gap_changes"))
for f in gaps():
    print("AFTER confirm title:", f["title"]); print("  computed:", {k: f["computed"][k] for k in ("days","from","to")}, "excluded:", f["computed"].get("excluded_records"))
    print("  explanation:", f.get("explanation")); print("  why:", f.get("why"))
    print("  reasons:", f.get("reasons"), "review_status:", f.get("review_status"))
----
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
    from app.backend import billing
    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
    from app.backend import pdf_routes
    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
    from app.backend import reclassify
    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
    from app.backend import calibration_route
    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)

    @app.get("/api/cases/{token}/export")
    def export(token: str, style: str = None):
----
evals/library/case_lib07_parking_lot_fall_outside_records.txt:5:Source: Quarry Hill Occupational Health, intake
evals/library/case_lib08_second_crash_mri_after.txt:16:Excerpt: "Neck pain 5/10 without arm symptoms. Date of accident per intake form: 2026-01-12. Plan: physical therapy twice weekly."
evals/library/case_lib11_priors_and_ledger.txt:6:Excerpt: "Annual visit. History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy. Problem list: hypertension, type 2 diabetes, chronic low back pain. Low back pain 3/10 today."
evals/library/case_lib11_priors_and_ledger.txt:30:Source: Fennimoor Spine Clinic, new patient intake form (OCR text)
evals/library/case_lib11_priors_and_ledger.txt:31:Excerpt: "Date of injury: 3/l8/26. How did it happen: rear ended at red Iight, neck and back hurt. Prior accidents? Yes [ ] No [X]. Prior injuries? Yes [ ] No IX]. Pain today: 7. Signed 3/27/2G."
evals/library/case_lib13_cloned_notes_cross_provider.txt:46:Excerpt: "Low back pain 7/10. Surgery date pending authorization."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:42.265Z

**tool call — Bash**
````
{
 "command": "grep -rn \"def accident_date_conflicts\\|questionnaire\\|first_recorded_treatment\" app/backend/*.py | head -30; echo ----; grep -n \"\\\"action\\\"\\|'action'\\|accept\\b\" app/backend/review.py | head -15; echo ----; sed -n 327,332p memory/contracts/api.md | cut -c1-600",
 "description": "Locate T-123 baseline code and review action shape"
}
````

### User / tool · 2026-11-02T11:15:42.404Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:43.678Z

**tool call — Bash**
````
{
 "command": "sed -n 1,140p app/backend/conflicts.py | grep -n \"\" | sed -n 1,140p | cut -c1-260",
 "description": "Read accident-date conflict code for T-123 baseline wording"
}
````

### User / tool · 2026-11-02T11:15:43.783Z

**tool result**
````
1:"""Structural conflicts raised by code, no LLM (ADR-014, D-017, D-025; R-FL-2, LLM_VS_CODE row 10).
2:accident_date_conflicts: stated accident dates (lexicon `accident_date_phrases`) vs the earliest recorded treatment date.
3:provider_conflicts: the same named clinician under different practice names. The tool never picks a date and never computes a delay."""
4:import re
5:
6:from app.backend import dates, flag_templates, gaps, lexicon
7:from app.backend.ingest import evidence_span
8:
9:PHRASE_TO_DATE_CHARS = 40
10:
11:
12:def _encounters(records):
13:    """D-055: every dated record counts for the earliest date. Whether the earliest one is paperwork is shown beside it (see accident_date_conflicts)."""
14:    return [r for r in records if r.get("date_iso")]
15:
16:
17:def stated_accident_dates(records: list) -> list:
18:    """[{record_no, iso, quote, start, end}]: a lexicon phrase followed within 40 characters by a parsed date, per record excerpt."""
19:    out = []
20:    for r in records:
21:        text = r.get("excerpt") or ""
22:        for e in lexicon.code_list("accident_date_phrases"):
23:            for m in e["regex"].finditer(text):
24:                for d in dates.find_dates(text[m.end():m.end() + PHRASE_TO_DATE_CHARS + 12]):
25:                    if d["start"] > PHRASE_TO_DATE_CHARS:
26:                        break
27:                    if d["status"] == "parsed":
28:                        end = m.end() + d["end"]
29:                        out.append({"record_no": r["n"], "iso": d["iso"], "quote": text[m.start():end], "start": m.start(), "end": end})
30:                    break
31:    seen, uniq = set(), []
32:    for s in sorted(out, key=lambda x: (x["record_no"], x["start"], -x["end"])):
33:        k = (s["record_no"], s["iso"])
34:        if k not in seen:
35:            seen.add(k)
36:            uniq.append(s)
37:    return uniq
38:
39:
40:def accident_date_conflicts(records: list) -> list:
41:    """At most one conflict per case. (a) a stated date later than the earliest treatment date, or (b) two different stated dates."""
42:    stated = stated_accident_dates(records)
43:    enc = _encounters(records)
44:    if not stated or not enc:
45:        return []
46:    first = min(r["date_iso"] for r in enc)
47:    first_recs = [r for r in enc if r["date_iso"] == first]
48:    by_n = {r["n"]: r for r in records}
49:    distinct = sorted({s["iso"] for s in stated})
50:    later = [s for s in stated if s["iso"] > first]
51:    if len(distinct) < 2 and not later:
52:        return []
53:    if len(distinct) >= 2:
54:        a, b = stated[0], next(s for s in stated if s["iso"] != stated[0]["iso"])
55:        category = "accident_dates_differ"
56:        title, expl = flag_templates.render("conflict", category, date_a=a["iso"], date_b=b["iso"], quote_a=a["quote"], quote_b=b["quote"],
57:                                            provider_a=by_n[a["record_no"]].get("source"), provider_b=by_n[b["record_no"]].get("source"))
58:        cited = [a, b]
59:    else:
60:        a = later[0]
61:        category = "accident_date_after_treatment"
62:        # D-055 (T-116 r4/T-123): never state paperwork as the first treatment. If ANY record on the earliest date looks like paperwork (alone, or
63:        # sharing the date with a visit, in either order), the sentence names that record, says it looks like paperwork, and gives the other reading
64:        # (the first recorded visit); the paralegal decides.
65:        extra = {}
66:        paper = [r for r in first_recs if gaps.admin_label(r)]
67:        if paper:
68:            visits = sorted((r for r in enc if not gaps.admin_label(r)), key=lambda r: (r["date_iso"], r["n"]))
69:            extra = {"record_no": paper[0]["n"]}
70:            if visits:
71:                extra.update(alt_record_no=visits[0]["n"], alt_date=visits[0]["date_iso"], alt_provider=visits[0].get("source") or "the record",
72:                             alt_later="also" if a["iso"] > visits[0]["date_iso"] else "not")
73:        ordered = paper + [r for r in first_recs if r not in paper]
74:        title, expl = flag_templates.render("conflict", category, stated=a["iso"], quote=a["quote"], date=first,
75:                                            provider_a=ordered[0].get("source"),
76:                                            provider_b=ordered[1].get("source") if len(ordered) > 1 else None, **extra)
77:        cited = [a]
78:    ev = [evidence_span(by_n[s["record_no"]], "excerpt", s["quote"]) for s in cited] + [evidence_span(r, "date") for r in first_recs]
79:    nos = sorted({s["record_no"] for s in cited} | {r["n"] for r in first_recs})
80:    return [{"subtype": "accident_date", "category": category, "type": "conflict", "origin": "code", "title": title, "explanation": expl,
81:             "body_date": a["iso"], "stated_dates": distinct, "first_treatment_date": first, "record_nos": nos, "evidence": ev}]
82:
83:
84:_TITLES = {"dr", "md", "do", "dc", "np", "pa", "pac", "dpm", "dds", "dpt", "pt", "phd", "rn", "mr", "ms", "mrs"}
85:_WORD = re.compile(r"[A-Za-z][A-Za-z'-]*\.?")
86:
87:
88:def _surname(segment: str):
89:    """Last name-like word of a segment that carries a clinician marker (title/credential or an initial), else None."""
90:    words = [w.rstrip(".") for w in _WORD.findall(segment)]
91:    marked = any(w.lower() in _TITLES for w in words) or any(len(w) == 1 and w.isupper() for w in words)
92:    names = [w for w in words if w.lower() not in _TITLES and len(w) > 1 and w[0].isupper()]
93:    return names[-1].casefold() if marked and names else None
94:
95:
96:def _norm(s):
97:    return " ".join((s or "").split()).casefold()
98:
99:
100:def parse_provider(label: str) -> dict:
101:    """{practice, person}: practice = the first comma segment when it is not itself a clinician; person = surname from any segment."""
102:    segs = [s.strip() for s in (label or "").split(",") if s.strip()]
103:    person = next((n for n in (_surname(s) for s in segs) if n), None)
104:    practice = _norm(segs[0]) if segs and _surname(segs[0]) is None else None
105:    return {"practice": practice, "person": person}
106:
107:
108:def provider_conflicts(records: list) -> list:
109:    """The same clinician surname under two different practice names (case_05: Wombleton vs Crumpet Lane). Header suffixes such as
110:    'new patient' / 'follow-up' and case or spacing variants are not conflicts (R-TL-9)."""
111:    by_person = {}
112:    for r in records:
113:        p = parse_provider(r.get("source"))
114:        if p["person"] and p["practice"]:
115:            by_person.setdefault(p["person"], {}).setdefault(p["practice"], []).append(r)
116:    out = []
117:    for person, practices in sorted(by_person.items()):
118:        if len(practices) < 2:
119:            continue
120:        groups = sorted(practices.values(), key=lambda rs: rs[0]["n"])
121:        a, b = groups[0][0], groups[1][0]
122:        title, expl = flag_templates.render("conflict", "provider_name_variant", provider_a=a["source"], provider_b=b["source"])
123:        recs = sorted((r for g in groups for r in g), key=lambda r: r["n"])
124:        out.append({"subtype": "provider_name", "category": "provider_name_variant", "type": "conflict", "origin": "code", "title": title,
125:                    "explanation": expl, "record_nos": [r["n"] for r in recs], "names": [r["source"] for r in recs],
126:                    "evidence": [evidence_span(r, "source") for r in recs]})
127:    return out
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:48.135Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/paralegal-reviewer/t116-gap-endpoint-patterns.md | head -60; echo ----; grep -n \"accident_date_after_treatment\" -A3 app/backend/flag_templates.py 2>/dev/null | head -30; ls app/backend | grep -i template",
 "description": "Read T-116 memory and accident-date template wording"
}
````

### User / tool · 2026-11-02T11:15:48.247Z

**tool result**
````
---
name: t116-gap-endpoint-patterns
description: T-116 gap endpoints through r5 (f8f358e, 2026-11-02, verdict changes): r4 warning-suppression blocker closed; accident baseline still says paperwork is first treatment on same-day and questionnaire/authorization headers (M1); lib10 golden truth still stale
metadata:
  type: project
---

State at r3 (8673326, verdict fail, 2 blockers, 2 majors; review reviews/T-116-paralegal-r3.md): the gaps.py label exclusion is gone and gap
dates, days, flags and endpoints equal pre-T-116 (3e3f3b7) on 25 packets, 60 label runs and 10 Appendix A fax variants. The warning works where
a gap starts or ends at an intake form encounter (lib09 after confirm: 40 days, start warning with record 4 and verbatim header).

Recurring pattern: removing a guess from one layer leaves the same guess one layer down. At r3 the gaps.py regex was removed, but
ingest.record_kind (ingest.py:214-221) applies lexicon `non_encounter` to the whole Source label, and gaps.compute_gaps (gaps.py:104) keeps
kind == "encounter". So "Capital PT, initial evaluation, correspondence", "Office visit / records request", "Dr. Lee, chiropractic, visit 3 -
records request copy", "Capital PT, visit 5 (ledger balance reviewed)", "Austin Imaging, MRI cervical spine (records request attached)" still
give an invented 40-day gap, and a visit with "records request copy" as the endpoint hides a span entirely (no flag). Before any "fixed"
verdict, grep every layer that can exclude (ingest kind, lexicon, gaps) and probe with the same labels.

Recurring pattern: "identical to pre-T-116" is not the D-055 test when the pre behaviour is itself the guess. D-055 premise ("as before T-116
gap math runs over all dated records") is wrong: pre-T-116 already dropped non-encounter kinds. Test against the decision text, not only pre.

Recurring pattern: an intake form is kind "encounter" at ingest. It becomes a gap endpoint, so it (a) warns when the gap ends there (correct)
and (b) hides a 40-day span when dated inside it with no visit (W3, no warning). Open as major F4 pending the D-055 reading.

Recurring pattern: the accident-date baseline (conflicts._encounters, conflicts.py:12-14, used by accident_date_conflicts) and the accident
year (pipeline._accident_year, pipeline.py:258) still count the intake form as "first recorded treatment". r3 added a warning appended after the
false sentence (not a fix). T-113's note (board/cards/T-113.md:29) moves "T-116 F3" to conflict candidates; the deterministic baseline is not
candidate code (conflict_candidates.py calls neither). Erratum: r3 review says T-113 "does not cover" it and that grep returns 1 from H3V5; the
single match is line 29 (the note). Check grep output lines before claiming what a card does not cover.

Recurring pattern: lib11 truth flips. T-118 (78450f6) applied the r2 edits (record 6 phone_note, excluded [4,6,9], rows [5]/[5]); the product
at r3 gives [5,6]/[5,6] with record 6 encounter. validate_library.py and check_golden.py exit 0 on HEAD; gap test compares dates only
(test_t116 lines 163-170); legacy_gaps (lines 60-64) copies the same kind filter, so it cannot see exclusion by kind (minor F5).

Probe pitfall: the "pre-T-116" tree is `git rev-parse <first-T116-commit>^` = 3e3f3b7 (fa95e58 is older and has no library packets). Scripts that
call gaps.non_visit_label fail on HEAD (removed); the r3 probe uses only ingest.ingest, compute_gaps, gap_flags, conflicts.accident_date_conflicts.

Why: T-116 r1 (fail, F1 blocker label substring), r2 (fail, F1 narrowed blocker, F3 blocker), r3 (fail, F1 kind path blocker, F2 F3 blocker,
F3 lib11 major, F4 mid-span major). Card status is in the board.
How to apply: on any gap, endpoint or truth change, run artifacts/review-evidence/T-116-paralegal-r3-probe.py on the pre parent and HEAD, then
compare; restore the parent's truth file on a scratch copy to confirm a gate fails; check every exclusion layer, not only the one edited.

Related: [[golden-set-recurring-findings]], [[t114-rates-gap-patterns]], [[t118-lib11-truth-patterns]], [[reviewer-tooling-quirks]].

## r4 (8b4ff11, 2026-11-02, verdict fail: 1 blocker, 2 minors, 1 nit; reviews/T-116-paralegal-r4.md)
r3 blockers fixed: compute_gaps reads every dated record, 60/60 label runs no invented gap, conditional "Possible gap of N days" flag and
"If record N: <header> is paperwork, not a visit, the gap would be X days" work. lib10 49 -> 43 (CMS-1500 dated 07-14, excerpt states DOS 07/08), alt 49 shown: correct.
New blocker pattern: the warning is gated by gaps.admin_label -> _has_treatment_evidence (regex on excerpt: Dx:, performed, seen by, Plan:). Bills/EOBs/forms
with those words get no warning, no alternative, no conditional flag; a mid-span 40-day span vanishes (pre-T-116 showed it). Same gate feeds the accident baseline.
Recurring: every time a guess is removed, check the next gate (warning suppression) with the same probe; use mutation: append one clinical-sounding sentence to a paperwork excerpt.
Probes: artifacts/review-evidence/T-116-paralegal-r4-evidence-suppression.py, -packet-dx-line.py, -baseline.py (reuse r3-probe.py for labels).

## r5 (f8f358e, 2026-11-02, verdict changes: 0 blockers, 1 major, 1 minor carried, 1 nit; reviews/T-116-paralegal-r5.md)
r4 F1 closed: admin_label is header-only; 8/8 r4 paperwork rows and 20/20 header x text variants (T-116-paralegal-r5-probe.py) show span, alternative, conditional flag. lib06 35-day flag survives the Dx line. 60/60 label runs still [19, 21] with no flag.
Open, major (M1): the accident baseline still names paperwork as "first recorded treatment" in two places the header-only change does not touch:
(a) same-day paperwork + visit: conflicts.py:64-65 takes the paperwork branch only if ALL first-date records are admin; else flag_templates.py:146 lists every first-date source.
(b) headers missing from gaps.py:19-22 (bare 'questionnaire', 'authorization request') are called first treatment with admin_label None.
Recurring: a unit test that uses one record on its own date passes while the same-day branch fails. For any branch with an "all(...)" or first-date list, probe mixed dates in both record orders.
Still open from r4: F3 golden lib10 expected 49 vs counted 43 and lexicon.yaml:1282 text; F4 headline leads with 43 when the paperwork states DOS 07/08.
Probes (r5): T-116-paralegal-r5-probe.py, -headers.py, -labels-check.py, -appx-check.py, -packet-flags.out.txt, -jsoncheck.py.
----
14:    ("conflict", "accident_date"): "accident_date_after_treatment",
15-    ("conflict", "provider_name"): "provider_name_variant",
16-    ("conflict", "treatment_plan"): "treatment_plan_vs_actual",
17-    ("conflict", "history_inconsistency"): "other_fact_mismatch",
--
32:    "accident_date_after_treatment": "conflict", "accident_dates_differ": "conflict", "provider_name_variant": "conflict",
33-    "treatment_plan_vs_actual": "conflict", "other_fact_mismatch": "conflict",
34-    "pre_existing": "pre_existing", "degenerative_language": "pre_existing", "prior_surgery": "pre_existing",
35-    "speculative_language": "causation", "patient_report": "causation", "missed_care": "causation", "new_onset": "causation",
--
174:    "accident_date_after_treatment": _acc_after,
175-    "accident_dates_differ": _acc_differ,
176-    "provider_name_variant": _provider_variant,
177-    "treatment_plan_vs_actual": _pair("Treatment plan and what followed differ"),
flag_templates.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:15:50.796Z

**tool call — Bash**
````
{
 "command": "sed -n 120,175p app/backend/flag_templates.py | cut -c1-400",
 "description": "Read accident-date flag template wording"
}
````

### User / tool · 2026-11-02T11:15:50.891Z

**tool result**
````
def _acc_after_paperwork(v):
    """D-055 (T-116 round 4): the earliest recorded date belongs to a record that looks like paperwork. The sentence never calls it treatment; it names the
    record and gives the other reading (the first recorded visit) so the paralegal decides."""
    prov = "; ".join(p for p in (v.get("provider_a"), v.get("provider_b")) if p)
    stated = f" {_d(v['stated'])}" if v.get("stated") else ""
    quote = f" (“{v['quote']}”)" if v.get("quote") else ""
    first = f"{_d(v.get('date'))} (record {v['record_no']}: {v['provider_a']})" if v.get("provider_a") else f"{_d(v.get('date'))} (record {v['record_no']})"
    if v.get("alt_date"):
        alt = (f"If record {v['record_no']}: {v.get('provider_a') or 'this record'} is paperwork, not a visit, the first recorded visit is {_d(v['alt_date'])} "
               f"(record {v['alt_record_no']}: {v['alt_provider']}), and the stated date is {v['alt_later']} later than it.")
    else:
        alt = f"If record {v['record_no']}: {v.get('provider_a') or 'this record'} is paperwork, not a visit, there is no recorded visit to compare with."
    return ("Stated accident date is later than the earliest record",
            f"Stated accident date{stated}{quote} is later than the earliest recorded date, {first}, which looks like paperwork, not a visit. "
            f"The records disagree; the tool does not choose between them. {alt} Check when treatment actually began before relying on this comparison.")


def _acc_after(v):
    if v.get("record_no"):
        return _acc_after_paperwork(v)
    prov = "; ".join(p for p in (v.get("provider_a"), v.get("provider_b")) if p)
    first = (f", {_d(v['date'])}" + (f" ({prov})" if prov else "")) if v.get("date") else ""
    stated = f" {_d(v['stated'])}" if v.get("stated") else ""
    quote = f" (“{v['quote']}”)" if v.get("quote") else ""
    return ("Stated accident date is later than recorded treatment",
            f"Stated accident date{stated}{quote} is later than the first recorded treatment{first}. "
            "The records disagree; the tool does not choose between them." + "".join(" " + w for w in v.get("warnings") or []))


def _acc_differ(v):
    a = f"{_who(v, 'provider_a')} states {_d(v.get('date_a')) or 'a date'}" + (f" (“{v['quote_a']}”)" if v.get("quote_a") else "")
    b = f"{_who(v, 'provider_b')} states {_d(v.get('date_b')) or 'a date'}" + (f" (“{v['quote_b']}”)" if v.get("quote_b") else "")
    return "Two different stated accident dates", f"{a}; {b}. The tool does not choose between them."


def _provider_variant(v):
    a = f"{_who(v, 'provider_a')}" + (f" (“{v['quote_a']}”)" if v.get("quote_a") else "")
    b = f"{_who(v, 'provider_b')}" + (f" (“{v['quote_b']}”)" if v.get("quote_b") else "")
    return "Provider name differs between records", f"{a} and {b} may name the same provider."


def _date_amb(v):
    raw = f"The date “{v['raw']}” in " if v.get("raw") else "A date in "
    return "Date to confirm", f"{raw}{_who(v)} can be read more than one way; choose one reading."


def _inj(v):
    return ("Instruction-like text in a record",
            f"{_at(v)} contains instruction-like text{_quote(v)}. It is shown unchanged and everything from this record needs review.")


TEMPLATES = {
    "gap_over_30": _gap,
    "accident_date_after_treatment": _acc_after,
    "accident_dates_differ": _acc_differ,
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:16:00.120Z

**tool call — Bash**
````
{
 "command": "cat evals/library/case_lib09_spanish_interpreter_espalda.txt | cut -c1-400 | head -70",
 "description": "Read the lib09 library case text"
}
````

### User / tool · 2026-11-02T11:16:00.212Z

**tool result**
````
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-03-03
Source: Quillmere Regional ED
Excerpt: "Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940."

=== Record 2 ===
Date: 14/04/2026
Source: Consultorio Médico Aguaclara, nota de consulta
Excerpt: "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas. Consulta: $650.00. Costo por sesión de terapia física: $400.00."

=== Record 3 ===
Date: 2026-04-21
Source: Dr. Lucan Ostrowe, orthopedics, new patient
Excerpt: "Interpreter: patient's daughter. Patient states she fell in the parking lot after a car brushed her. Right shoulder pain 6/10. MRI right shoulder ordered."

=== Record 4 ===
Date: 03/05/2026
Source: Consultorio Médico Aguaclara, formulario de admisión (OCR)
Excerpt: "Fecha de ingreso: 03/O5/2026. Motivo de la visita: dolor de espaIda y hombro derecho. Accidentes anteriores? Si [ ] No [X]. Firma de la paciente: illegible."

=== Record 5 ===
Date: 2026-05-05
Source: Cinder Valley Imaging, right shoulder MRI
Excerpt: "Partial-thickness supraspinatus tear. MRI charge: $2,150."

=== Record 6 ===
Date: 2026-05-12
Source: Dr. Lucan Ostrowe, orthopedics, follow-up
Excerpt: "Interpreter: patient's daughter. MRI reviewed. Recommend physical therapy and subacromial injection. Pain 5/10."

=== Record 7 ===
Date: 2026-05-20
Source: Consultorio Médico Aguaclara, estado de cuenta (billing statement)
Excerpt: "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:16:07.340Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-123-paralegal-common.py",
 "content": "\"\"\"Shared helpers for the T-120/T-121/T-123 paralegal-reviewer probes (stdlib only).\n\nTalks to a fixture-backend server started from a `git archive HEAD` copy (see the review file for the exact command).\nUsage from another script: sys.path.insert(0, HERE); from common import req, load, poll_ready, BASE.\n\"\"\"\nimport json\nimport os\nimport time\nimport urllib.error\nimport urllib.request\n\nBASE = os.environ.get(\"ZLAYT_BASE\", \"http://127.0.0.1:7893\")\n\n\ndef req(method, path, body=None, raw=False):\n    data = json.dumps(body).encode() if body is not None else None\n    r = urllib.request.Request(BASE + path, data=data, method=method, headers={\"content-type\": \"application/json\"})\n    try:\n        with urllib.request.urlopen(r, timeout=180) as x:\n            payload = x.read()\n            return x.status, (payload.decode(\"utf-8\") if raw else json.loads(payload or b\"null\"))\n    except urllib.error.HTTPError as e:\n        payload = e.read()\n        try:\n            return e.code, json.loads(payload or b\"null\")\n        except ValueError:\n            return e.code, payload.decode(\"utf-8\", \"replace\")\n\n\ndef load_library(lib_id):\n    st, body = req(\"POST\", \"/api/cases\", {\"library\": lib_id})\n    assert st == 201, (lib_id, st, body)\n    return body[\"token\"]\n\n\ndef load_text(text, name):\n    st, body = req(\"POST\", \"/api/cases\", {\"text\": text, \"name\": name})\n    assert st == 201, (name, st, body)\n    return body[\"token\"]\n\n\ndef poll_ready(tok):\n    assert req(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\n    s = None\n    for _ in range(960):\n        s = req(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"]\n        if s in (\"ready\", \"failed\", \"done_with_errors\"):\n            break\n        time.sleep(0.25)\n    return s\n\n\ndef case(tok):\n    return req(\"GET\", f\"/api/cases/{tok}\")[1]\n"
}
````

### User / tool · 2026-11-02T11:16:07.475Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-123-paralegal-common.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:16:10.783Z

**tool call — Bash**
````
{
 "command": "sed -n 234,249p app/backend/api.py | cut -c1-220; echo ----; sed -n 1,30p artifacts/review-evidence/T-120-123-paralegal-common.py >/dev/null; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls \"$SCR/t120-123-archive/artifacts/\" | head",
 "description": "Check paste-case request keys and archive artifacts layout"
}
````

### User / tool · 2026-11-02T11:16:10.881Z

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

----
m0-smoke
review-evidence
screenshots
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:16:14.090Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-paralegal-explore.py",
 "content": "\"\"\"T-120 paralegal explore: lib09 records and every pre_existing flag as the running server returns them.\nRun: .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-explore.py  (needs the common helper next to it; -I drops the script dir, so use sys.path).\"\"\"\nimport json\nimport os\nimport sys\n\nHERE = os.path.dirname(os.path.abspath(__file__))\nsys.path.insert(0, HERE)\nfrom common import case, load_library, poll_ready  # noqa: E402\n\ntok = load_library(\"case_lib09_spanish_interpreter_espalda\")\nprint(\"status:\", poll_ready(tok))\nc = case(tok)\nprint(\"top keys:\", sorted(c.keys()))\nfor r in c.get(\"records\", []):\n    print(\"RECORD\", r.get(\"n\"), r.get(\"id\"), r.get(\"date_iso\"), r.get(\"source\"), \"|\", (r.get(\"excerpt\") or \"\")[:140])\nprint(\"--- flags\")\nfor f in c.get(\"flags\", []):\n    print(json.dumps({k: f.get(k) for k in (\"id\", \"type\", \"category\", \"title\", \"record_nos\", \"review_status\")}, ensure_ascii=False))\n    if f.get(\"type\") == \"pre_existing\":\n        print(\"   PRE evidence:\", json.dumps(f.get(\"evidence\"), ensure_ascii=False)[:600])\nprint(\"--- entries\")\nfor e in c.get(\"entries\", []):\n    print(json.dumps({k: e.get(k) for k in (\"id\", \"date_iso\", \"provider\", \"summary\", \"review_status\")}, ensure_ascii=False)[:400])\nprint(\"--- amounts\")\nfor a in c.get(\"amounts\", []):\n    print(json.dumps({k: a.get(k) for k in (\"id\", \"text\", \"kind\", \"value\", \"review_status\")}, ensure_ascii=False)[:300])\n"
}
````

### User / tool · 2026-11-02T11:16:14.194Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-paralegal-explore.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:16:16.031Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-120-paralegal-explore.py 2>&1 | cut -c1-700",
 "description": "Run lib09 explore script against the 7893 server"
}
````

### User / tool · 2026-11-02T11:16:16.174Z

**tool result**
````
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-paralegal-explore.py", line 9, in <module>
    from common import case, load_library, poll_ready  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'common'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:16:18.151Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-paralegal-explore.py",
 "old_string": "HERE = os.path.dirname(os.path.abspath(__file__))\nsys.path.insert(0, HERE)\nfrom common import case, load_library, poll_ready  # noqa: E402",
 "new_string": "import importlib.util\n\nHERE = os.path.dirname(os.path.abspath(__file__))\n_spec = importlib.util.spec_from_file_location(\"t120_123_common\", os.path.join(HERE, \"T-120-123-paralegal-common.py\"))\n_common = importlib.util.module_from_spec(_spec)\n_spec.loader.exec_module(_common)\ncase, load_library, poll_ready = _common.case, _common.load_library, _common.poll_ready"
}
````

### User / tool · 2026-11-02T11:16:18.271Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-paralegal-explore.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:16:19.544Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-120-paralegal-explore.py 2>&1 | cut -c1-700",
 "description": "Run lib09 explore script against the 7893 server"
}
````

### User / tool · 2026-11-02T11:16:20.254Z

**tool result**
````
status: ready
top keys: ['amounts', 'backend', 'created_at', 'dates_to_confirm', 'demo_mode', 'entries', 'error', 'flags', 'injection', 'models', 'name', 'records', 'review', 'status', 'token', 'totals', 'tray', 'undated_entries', 'updated_at', 'warnings']
RECORD None r1 2026-03-03 None | 
RECORD None r2 2026-04-14 None | 
RECORD None r3 2026-04-21 None | 
RECORD None r4 None None | 
RECORD None r5 2026-05-05 None | 
RECORD None r6 2026-05-12 None | 
RECORD None r7 2026-05-20 None | 
--- flags
{"id": "f_gap_r1_r2", "type": "gap", "category": "gap_over_30", "title": "Gap of 42 days", "record_nos": null, "review_status": "pending"}
{"id": "f_date_r4", "type": "record_warning", "category": "date_ambiguous", "title": "Date to confirm", "record_nos": null, "review_status": "pending"}
{"id": "f_r1_1", "type": "causation", "category": "patient_report", "title": "Reported onset", "record_nos": null, "review_status": "pending"}
{"id": "f_r2_1", "type": "causation", "category": "patient_report", "title": "Reported onset", "record_nos": null, "review_status": "pending"}
{"id": "f_r3_1", "type": "causation", "category": "patient_report", "title": "Reported onset", "record_nos": null, "review_status": "pending"}
--- entries
{"id": "e1", "date_iso": null, "provider": "Quillmere Regional ED", "summary": "Left shoulder pain 7/10; X-ray of left shoulder negative for fracture; diagnosis left shoulder contusion; ED charge $2,940.", "review_status": "pending"}
{"id": "e2", "date_iso": null, "provider": "Consultorio Médico Aguaclara, nota de consulta", "summary": "Patient reports pain 6/10 that worsens when raising the arm. Denies loss of consciousness. Exam: pain on palpation of the right shoulder. Plan: physical therapy and follow-up in 4 weeks.", "review_status": "pending"}
{"id": "e3", "date_iso": null, "provider": "Dr. Lucan Ostrowe, orthopedics, new patient", "summary": "Patient states she fell in the parking lot after a car brushed her; right shoulder pain 6/10; MRI of the right shoulder ordered.", "review_status": "pending"}
{"id": "e5", "date_iso": null, "provider": "Cinder Valley Imaging, right shoulder MRI", "summary": "Partial-thickness supraspinatus tear. MRI charge: $2,150.", "review_status": "pending"}
{"id": "e6", "date_iso": null, "provider": "Dr. Lucan Ostrowe, orthopedics, follow-up", "summary": "MRI reviewed. Physical therapy and subacromial injection recommended.", "review_status": "pending"}
{"id": "e7", "date_iso": null, "provider": "Consultorio Médico Aguaclara, estado de cuenta (billing statement)", "summary": "Account statement: consultations $1,300.00; physical therapy, 4 sessions at $400.00 per session. Balance: $2,900.00.", "review_status": "pending"}
--- amounts
{"id": "a1", "text": "$2,940", "kind": "charge", "value": null, "review_status": "pending"}
{"id": "a2", "text": "$650.00", "kind": "unclear", "value": null, "review_status": "pending"}
{"id": "a3", "text": "$400.00", "kind": "rate", "value": null, "review_status": "pending"}
{"id": "a4", "text": "$2,150", "kind": "charge", "value": null, "review_status": "pending"}
{"id": "a5", "text": "$1,300.00", "kind": "unclear", "value": null, "review_status": "pending"}
{"id": "a6", "text": "$400.00", "kind": "rate", "value": null, "review_status": "pending"}
{"id": "a7", "text": "$2,900.00", "kind": "unclear", "value": null, "review_status": "pending"}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:16:30.601Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-120-paralegal-explore2.py <<'EOF'\n\"\"\"T-120/T-121 paralegal explore 2: entry keys, default export before any review, and the style option (both on lib09).\"\"\"\nimport importlib.util, json, os, sys\nHERE = os.path.dirname(os.path.abspath(__file__))\n_s = importlib.util.spec_from_file_location(\"c\", os.path.join(HERE, \"T-120-123-paralegal-common.py\")); C = importlib.util.module_from_spec(_s); _s.loader.exec_module(C)\ntok = C.load_library(\"case_lib09_spanish_interpreter_espalda\"); print(\"status\", C.poll_ready(tok))\nc = C.case(tok)\nprint(\"entry keys:\", sorted(c[\"entries\"][0].keys()))\nprint(\"entry e1:\", json.dumps({k: c[\"entries\"][0].get(k) for k in (\"id\", \"date\", \"date_label\", \"source\", \"excerpt\", \"provider\")}, ensure_ascii=False)[:700])\nprint(\"review keys:\", sorted(c[\"review\"].keys()))\nprint(\"tray:\", json.dumps(c[\"tray\"], ensure_ascii=False)[:300])\nprint(\"dates_to_confirm:\", json.dumps(c[\"dates_to_confirm\"], ensure_ascii=False)[:500])\nst, ex = C.req(\"GET\", f\"/api/cases/{tok}/export\")\nprint(\"default export status\", st, (json.dumps(ex, ensure_ascii=False)[:400] if st != 200 else \"ok\"))\nst2, ex2 = C.req(\"GET\", f\"/api/cases/{tok}/export?style=bogus\")\nprint(\"style=bogus\", st2, json.dumps(ex2, ensure_ascii=False)[:200])\nst3, ex3 = C.req(\"GET\", f\"/api/cases/{tok}/export?style=oneline\")\nprint(\"style=oneline status\", st3, json.dumps(ex3, ensure_ascii=False)[:300])\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-120-paralegal-explore2.py 2>&1 | cut -c1-900",
 "description": "Explore entry keys and export style responses on lib09"
}
````

### User / tool · 2026-11-02T11:16:31.070Z

**tool result**
````
status ready
entry keys: ['ai_drafted', 'date', 'date_status', 'duplicate_note', 'edited', 'entered_by', 'entered_by_reviewer', 'excerpt', 'excerpt_end', 'excerpt_start', 'id', 'ladder', 'provider', 'reasons', 'record_ids', 'review_status', 'seq', 'source_kind', 'state', 'summary', 'translation', 'why']
entry e1: {"id": "e1", "date": "2026-03-03", "date_label": null, "source": null, "excerpt": "Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940.", "provider": "Quillmere Regional ED"}
review keys: ['counts', 'queue', 'ready_to_export']
tray: []
dates_to_confirm: [{"record_id": "r4", "raw": "03/05/2026", "candidates": ["2026-03-05", "2026-05-03"], "status": "ambiguous", "suggestion": {"convention": "DMY", "label": "DD/MM", "iso": "2026-05-03", "reason": "Another date in this packet uses day first (Record 2: 14/04/2026)", "evidence": [{"record_id": "r2", "raw": "14/04/2026"}], "evidence_count": 1, "auto_applied": false}}]
default export status 422 {"error": {"code": "export_blocked", "message": "Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.", "detail": {"blockers": [{"item_id": null, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": "Nothing is accepted or edited yet, so the letter would be empty.", "next_action": {"code": "DECIDE", "text": "Accept, edit or dismiss this item.", "target": {"v
style=bogus 422 {"error": {"code": "invalid_style", "message": "The letter style must be 'standard' or 'oneline'.", "detail": {}}}
style=oneline status 422 {"error": {"code": "export_blocked", "message": "Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.", "detail": {"blockers": [{"item_id": null, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": "Nothing is accepted or edited yet, so the letter would be em
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:16:38.788Z

**tool call — Bash**
````
{
 "command": "sed -n 12,60p app/backend/gaps.py | cut -c1-330; echo ----; grep -n \"accident_date_phrases\" -A12 app/llm/lexicon.yaml | head -30 | cut -c1-200",
 "description": "Read paperwork label regexes and accident date phrase lexicon"
}
````

### User / tool · 2026-11-02T11:16:38.885Z

**tool result**
````
from app.backend.ingest import evidence_span

THRESHOLD_DAYS = 30

# (label shown to the paralegal, header-label regex), first match wins. A bare "intake" (an intake evaluation or visit) is a treatment
# encounter and is deliberately NOT here; only the paperwork wording is ("intake form", "formulario de admision").
_NON_VISIT = [(label, re.compile(rx, re.IGNORECASE)) for label, rx in (
    ("intake form", r"\b(?:(?:new[- ]patient\s+)?(?:intake|registration|admission|admissions|check-?in)\s+(?:form|forms|packet|paperwork|questionnaire|sheet)"
                    r"|new[- ]patient\s+(?:paperwork|forms?|questionnaire|packet)|patient\s+(?:information|history|health\s+history|registration)\s+(?:form|questionnaire|sheet)"
                    r"|health\s+history\s+(?:form|questionnaire)|pain\s+(?:diagram|questionnaire)|consent\s+form|assignment\s+of\s+benefits|questionnaires?)\b"
                    r"|\bformulario\s+de\s+(?:admisi[oó]n|ingreso|registro)\b|\bhoja\s+de\s+(?:admisi[oó]n|ingreso)\b"),
    ("explanation of benefits", r"\b(?:explanation\s+of\s+benefits|EOB|remittance(?:\s+advice)?)\b"),
    ("claim form", r"\b(?:UB-?04|CMS-?1500|HCFA|claim\s+form)\b"),
    ("ledger", r"\b(?:ledger|payment\s+(?:history|record)|account\s+history)\b"),
    ("billing statement", r"\b(?:billing|statement\s+of\s+account|account\s+statement|itemi[sz]ed\s+(?:bill|statement|charges)|invoice|superbill|balance\s+due)\b|^statement$"
                          r"|\bestado\s+de\s+cuenta\b|\bfactura\b"),
    ("affidavit", r"\b(?:affidavit|custodian\s+of\s+records|records\s+custodian|certification\s+of\s+records|business\s+records|cover\s+(?:page|sheet))\b"),
    ("records request", r"\b(?:records?\s+request|request\s+for\s+records|records\s+retrieval|authorization\s+(?:form|request)|HIPAA\s+authorization)\b"),
    ("records review", r"\b(?:records?|chart|peer|utili[sz]ation)\s+review\b|\bIME\b|\bindependent\s+medical\s+(?:exam|examination|evaluation)\b"),
    ("narrative letter", r"\bnarrative\s+(?:letter|report)\b|\bmedical[- ]legal\s+(?:report|narrative)\b|\bsummary\s+letter\b|\bdemand\s+letter\b"),
    ("letter or correspondence", r"^fax$|\b(?:correspondence|letter(?:\s+of\s+protection)?|LOP|fax\s+cover(?:\s+sheet)?|referral\s+(?:form|letter)|prior\s+authori[sz]ation)\b"),
    ("phone or message note", r"\b(?:phone|telephone|tel\.?)\s+(?:note|call|encounter|message|contact)\b|\bportal\s+message\b|\bvoicemail\b|\bmessage\s+(?:note|log)\b"),
)]
# A document that names itself on its first line (an intake form whose Source label only says "new patient"). Anchored: a clinical note that
# merely mentions a form further in does not match.
_TITLE = re.compile(r"^\W*(?:new[- ]patient\s+)?(?:intake|registration|admission)\s+(?:form|packet|questionnaire)\b|^\W*(?:business\s+records\s+)?affidavit\b", re.IGNORECASE)


# Words that name a treatment visit in the record-type head. If one is left in the head after the administrative phrase is removed, the
# record is treated as a visit ("records review visit", "initial evaluation", "progress note"). English and Spanish.
_VISIT_WORD = re.compile(r"\b(?:visits?|evaluations?|evals?|exams?|examinations?|consult\w*|follow-?ups?|progress|sessions?|treatments?|therapy|"
                         r"procedures?|injections?|operative|surgery|imaging|mri|x-?rays?|notes?|soap|daily|new\s+patient|initial|discharge|esi|epidural|"
                         r"visita|consulta|nota|sesi[oó]n|evaluaci[oó]n|terapia|tratamiento|cita)\b", re.IGNORECASE)


def _bare(src: str) -> str:
    """The header label with every parenthetical dropped ("(OCR)", "(faxed)", "(intake form completed same day)")."""
    h = (src or "").strip()
    while True:
        n = re.sub(r"\s*\([^()]*\)", "", h)
        if n == h:
            return h.strip()
        h = n


def admin_label(rec: dict):
    """The plain label of a record whose header looks administrative ("intake form", "billing statement", ...), or None. WARNING ONLY (D-055):
    it never changes a gap. It stays conservative so a warning means something: (1) the administrative type is read from the record-type head
    (last comma segment) of the header label, or from the record's own first-line title; (2) no visit word appears in the label outside parentheses and
----
3:# (accident_date_phrases), the injection tag (injection) and amount classification (damages).
4-# Binding contract: memory/ORCHESTRATOR_DECISIONS.md D-013, D-018 (also D-001, D-003, D-005, D-017) and
5-# memory/DECISIONS.md ADR-008, ADR-010, ADR-011, ADR-013, ADR-014.
6-# Research basis: research/adjuster-attacks.md (attacks A1–A15, "AA src N"), research/texas-pi-notes.md,
7-# research/chronology-practice.md. Reviews addressed in round 2: reviews/T-009-legal-nurse.md and
8-# reviews/T-009-claims-adjuster.md.
9-#
10-# HOW TO USE (binding semantics)
11-# T-027 (generalization pass): patterns were widened for spinal levels (C5-6, L4-S1), "<symptom> since <year>",
12-# "may be <finding>", probable/presumed/favors, "attributes/relates ... to", and narrowed for post-accident wording
13-# (dates on/after the accident year, "secondary to the MVA", "Prior injuries? Denies."). Held-out probes live in
14-# evals/lexicon_heldout.jsonl and are never copied into `examples`; the self-check fails on any overlap and scores
15-# low-only hits as non-flags. Categories are exactly the ADR-013 closed list (the self-check asserts it).
--
1297:  accident_date_phrases:
1298-    applies_to: record_text
1299-    consumer: 'ADR-014: code extracts stated accident dates where a phrase is followed within 40 characters by a date in a listed format. A conflict arises if a stated date is later than the earl
1300-    rationale: 'The accident-date conflict (Appendix C: 2026-01-09 per EMS/ER vs "Date of accident per intake form: 2026-01-19") is the case''s headline conflict, and it must be producible withou
1301-    source: 'ADR-014; D-017; Appendix C record 7; AA A7 (JLG Trucking)'
1302-    false_positive: '"DOA" also means "dead on arrival" and "DOI" can mean "digital object identifier". Neither is followed by a date within 40 characters, so the code rule ignores them. "Collisi
1303-    entries:
1304-      - id: accident_date_label
1305-        pattern: '\b(?:date\s+of\s+(?:the\s+)?(?:accident|injury|incident|loss|collision|crash|MVA|MVC)|(?:accident|injury|incident|loss|collision|crash|MVA|MVC)\s+date|DOA|DOI|DOL|D/A|D\.O\.A\.?
1306-      - id: event_on_date
1307-        pattern: '\b(?:collision|accident|crash|wreck|MVA|MVC|incident|rear-?ended|injured|hurt)\s+(?:on|dated)\b'
1308-    examples:
1309-      hit: ['Date of accident per intake form: 2026-01-19.', 'DOA: 01/09/2026', 'Date of injury 1/9/26', 'MVA on 01/09/2026', 'Collision on January 9, 2026.', 'Accident date: 2026-01-09', 'DOI 20
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:16:40.711Z

**tool call — Bash**
````
{
 "command": "cat evals/golden/sample.txt | cut -c1-260; echo ----; head -c 1500 evals/golden/sample.export.expected.txt; echo; echo ----; grep -n \"^[A-Z_ ]*$\" evals/golden/sample.export.expected.txt | head",
 "description": "Read the sample case and golden export file layout"
}
````

### User / tool · 2026-11-02T11:16:40.839Z

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
=== LETTER_TEXT (block 1: paste into letter) ===
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
Discharged from physical therapy after two missed appointments; 
----
2:TREATMENT CHRONOLOGY
3:
7:
11:
15:
19:
23:
27:
31:
35:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:17:32.565Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-120-123-paralegal-probe.py <<'EOF'\n\"\"\"T-120 / T-121 / T-123 paralegal-reviewer probe (stdlib only; run: ARCH=<git archive HEAD copy> .venv/bin/python -I <this file>).\n\nServer: fixture backend, ZLAYT_MODE=local, a `git archive HEAD` copy (commit 63e18ed), port 7893. Writes its evidence to\nartifacts/review-evidence/T-120-123-paralegal-probe.out.json and prints a short summary.\nSections: A (T-120) lib09 pre_existing flags and the real-prior controls; B (T-121) lib09 and sample letters, default and oneline,\nchecked against the raw library/sample text; C (T-123) the accident-date sentence on the library set and on SYNTHETIC same-day probes.\n\"\"\"\nimport importlib.util\nimport json\nimport os\nimport re\nimport sys\n\nHERE = os.path.dirname(os.path.abspath(__file__))\n_s = importlib.util.spec_from_file_location(\"t120_123_common\", os.path.join(HERE, \"T-120-123-paralegal-common.py\"))\nC = importlib.util.module_from_spec(_s)\n_s.loader.exec_module(C)\nARCH = os.environ[\"ARCH\"]\nOUT = os.path.join(HERE, \"T-120-123-paralegal-probe.out.json\")\nres = {\"base\": C.BASE, \"arch\": \"git archive HEAD copy (63e18ed)\"}\nMONTHS = \"January February March April May June July August September October November December\".split()\n\n\ndef norm(s):\n    return \" \".join((s or \"\").split())\n\n\ndef raw_records(path):\n    text = open(path, encoding=\"utf-8\").read()\n    parts = re.split(r\"^=== Record (\\d+) ===\\s*$\", text, flags=re.M)\n    out = {}\n    for i in range(1, len(parts), 2):\n        body = parts[i + 1]\n        out[int(parts[i])] = {\"date\": re.search(r\"^Date:\\s*(.+)$\", body, re.M).group(1).strip(),\n                              \"source\": re.search(r\"^Source:\\s*(.+)$\", body, re.M).group(1).strip(),\n                              \"excerpt\": re.search(r'^Excerpt:\\s*\"(.*)\"\\s*$', body, re.M).group(1)}\n    return out\n\n\ndef long_date(iso):\n    y, m, d = iso.split(\"-\")\n    return f\"{MONTHS[int(m) - 1]} {int(d)}, {y}\"\n\n\ndef pre_flags(case):\n    return [{\"id\": f[\"id\"], \"title\": f[\"title\"], \"category\": f.get(\"category\"), \"record_nos\": f.get(\"record_nos\"),\n             \"evidence\": f.get(\"evidence\")} for f in case[\"flags\"] if f[\"type\"] == \"pre_existing\"]\n\n\n# ---------------------------------------------------------------- A. T-120\nlib09_path = os.path.join(ARCH, \"evals/library/case_lib09_spanish_interpreter_espalda.txt\")\nr09 = raw_records(lib09_path)\nhx = \"Hx obtained via patient's son, who interpreted.\"\nres[\"A_raw_lib09_interpreter_sentence_in\"] = [n for n, r in r09.items() if hx in norm(r[\"excerpt\"])]\ntok = C.load_library(\"case_lib09_spanish_interpreter_espalda\")\nres[\"A_lib09_status\"] = C.poll_ready(tok)\nc09 = C.case(tok)\nres[\"A_lib09_pre_existing_flags\"] = pre_flags(c09)\nres[\"A_lib09_all_flags\"] = [{\"id\": f[\"id\"], \"type\": f[\"type\"], \"category\": f.get(\"category\"), \"title\": f[\"title\"]} for f in c09[\"flags\"]]\nres[\"A_lib09_records\"] = [{\"id\": r[\"id\"], \"date\": r.get(\"date\")} for r in c09[\"records\"]]\n\nsample_path = os.path.join(ARCH, \"evals/golden/sample.txt\")\nst, body = C.req(\"POST\", \"/api/cases\", {\"sample\": True})\ntok_s = body[\"token\"]\nres[\"A_sample_status\"] = C.poll_ready(tok_s)\ncs = C.case(tok_s)\nres[\"A_sample_pre_existing_flags\"] = pre_flags(cs)\n\ntok_l02 = C.load_library(\"case_lib02_slip_fall_prior_knee\")\nC.poll_ready(tok_l02)\nres[\"A_lib02_pre_existing_flags\"] = pre_flags(C.case(tok_l02))\ntok_l11 = C.load_library(\"case_lib11_priors_and_ledger\")\nC.poll_ready(tok_l11)\nres[\"A_lib11_pre_existing_flags\"] = pre_flags(C.case(tok_l11))\n\npaste_a = (\"SYNTHETIC — invented for a review probe; not real patient data\\n\\n=== Record 1 ===\\nDate: 2026-03-03\\n\"\n           \"Source: Quillmere Regional ED\\nExcerpt: \\\"Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019. \"\n           \"Left shoulder pain 7/10. X-ray left shoulder negative for fracture.\\\"\\n\")\nst, body = C.req(\"POST\", \"/api/cases\", {\"text\": paste_a, \"name\": \"T-120 synthetic probe\"})\ntok_a = body[\"token\"]\nC.poll_ready(tok_a)\nres[\"A_synthetic_same_sentence_plus_real_prior\"] = pre_flags(C.case(tok_a))\n\n# ---------------------------------------------------------------- B. T-121\ndef accept_all(tk, entry_ids, charge_ids, rate_ids):\n    out = {}\n    for iid in entry_ids + charge_ids + rate_ids:\n        out[iid] = C.req(\"POST\", f\"/api/cases/{tk}/items/{iid}/review\", {\"action\": \"accept\"})[0]\n    return out\n\n\ncases09 = C.case(tok)\nent09 = [e[\"id\"] for e in cases09[\"entries\"] if e.get(\"review_status\") == \"pending\"]\namts09 = {a[\"id\"]: a for a in cases09[\"amounts\"]}\ncharges09 = [i for i, a in amts09.items() if a[\"kind\"] == \"charge\"]\nrates09 = [i for i, a in amts09.items() if a[\"kind\"] == \"rate\"]\nres[\"B_lib09_translation_fields\"] = {e[\"id\"]: e.get(\"translation\") for e in cases09[\"entries\"]}\nres[\"B_lib09_accept_status\"] = accept_all(tok, ent09, charges09, rates09)\ns1, std09 = C.req(\"GET\", f\"/api/cases/{tok}/export\")\ns2, one09 = C.req(\"GET\", f\"/api/cases/{tok}/export?style=oneline\")\nres[\"B_lib09_export_status\"] = [s1, s2]\nres[\"B_lib09_standard_letter\"] = std09.get(\"letter_text\") if s1 == 200 else std09\nres[\"B_lib09_oneline_letter\"] = one09.get(\"letter_text\") if s2 == 200 else one09\nres[\"B_lib09_standard_internal_notes_head\"] = (std09.get(\"internal_notes_text\") or \"\")[:600] if s1 == 200 else None\n\ns3, sam = None, None\nst, body = C.req(\"POST\", \"/api/cases\", {\"sample\": True})\ntok_sam = body[\"token\"]\nC.poll_ready(tok_sam)\ncs = C.case(tok_sam)\nent_s = [e[\"id\"] for e in cs[\"entries\"] if e.get(\"review_status\") == \"pending\"]\nam_s = {a[\"id\"]: a for a in cs[\"amounts\"]}\nres[\"B_sample_accept_status\"] = accept_all(tok_sam, ent_s, [i for i, a in am_s.items() if a[\"kind\"] == \"charge\"],\n                                           [i for i, a in am_s.items() if a[\"kind\"] == \"rate\"])\ns3, sam_std = C.req(\"GET\", f\"/api/cases/{tok_sam}/export\")\ns4, sam_one = C.req(\"GET\", f\"/api/cases/{tok_sam}/export?style=oneline\")\nres[\"B_sample_export_status\"] = [s3, s4]\nres[\"B_sample_standard_letter\"] = sam_std.get(\"letter_text\") if s3 == 200 else sam_std\nres[\"B_sample_oneline_letter\"] = sam_one.get(\"letter_text\") if s4 == 200 else sam_one\nres[\"B_sample_invalid_style\"] = C.req(\"GET\", f\"/api/cases/{tok_sam}/export?style=Oneline\")[0]\n\nwith open(OUT, \"w\", encoding=\"utf-8\") as f:\n    json.dump(res, f, ensure_ascii=False, indent=1)\nprint(\"A/B written\", OUT)\nEOF\necho written",
 "description": "Write the T-120/T-121 probe script"
}
````

### User / tool · 2026-11-02T11:17:32.654Z

**tool result**
````
written
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:17:36.608Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; time ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-120-123-paralegal-probe.py 2>&1 | tail -20; .venv/bin/python -I -c \"import json,sys; d=json.load(open('artifacts/review-evidence/T-120-123-paralegal-probe.out.json')); [print(k, json.dumps(d[k], ensure_ascii=False)[:500]) for k in d if k.startswith('A_')]\"",
 "description": "Run the T-120 and T-121 probe sections and print part A"
}
````

### User / tool · 2026-11-02T11:17:37.968Z

**tool result (error)**
````
Exit code 1
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-123-paralegal-probe.py", line 80, in <module>
    tok_a = body["token"]
            ~~~~^^^^^^^^^
KeyError: 'token'

real	0m1.240s
user	0m0.056s
sys	0m0.018s
Traceback (most recent call last):
  File "<string>", line 1, in <module>
FileNotFoundError: [Errno 2] No such file or directory: 'artifacts/review-evidence/T-120-123-paralegal-probe.out.json'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:17:40.789Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-120-paralegal-dbg.py <<'EOF'\nimport importlib.util, json, os\nHERE = os.path.dirname(os.path.abspath(__file__))\n_s = importlib.util.spec_from_file_location(\"c\", os.path.join(HERE, \"T-120-123-paralegal-common.py\")); C = importlib.util.module_from_spec(_s); _s.loader.exec_module(C)\nt = \"SYNTHETIC — invented for a review probe; not real patient data\\n\\n=== Record 1 ===\\nDate: 2026-03-03\\nSource: Quillmere Regional ED\\nExcerpt: \\\"Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019. Left shoulder pain 7/10.\\\"\\n\"\nprint(C.req(\"POST\", \"/api/cases\", {\"text\": t, \"name\": \"x\"}))\nprint(C.req(\"POST\", \"/api/cases\", {\"text\": open(os.path.join(HERE, \"..\", \"..\", \"evals/golden/sample.txt\")).read(), \"name\": \"x\"})[0])\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-120-paralegal-dbg.py 2>&1 | cut -c1-900",
 "description": "Debug the paste request response"
}
````

### User / tool · 2026-11-02T11:17:40.959Z

**tool result**
````
(409, {'error': {'code': 'demo_mode_unsupported_input', 'message': 'This demo only runs the recorded sample cases.', 'detail': {}}})
201
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:17:43.847Z

**tool call — Bash**
````
{
 "command": "grep -rn \"demo_mode_unsupported_input\" app/backend/*.py | head -5; grep -n \"def local_mode\" -A6 app/backend/api.py | head -12",
 "description": "Find the demo-mode paste gate and local_mode definition"
}
````

### User / tool · 2026-11-02T11:17:43.960Z

**tool result**
````
app/backend/api.py:255:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:288:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:358:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:383:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
79:def local_mode() -> bool:
80-    return os.environ.get("ZLAYT_MODE") == "local"
81-
82-
83-def is_loopback_peer(request) -> bool:
84-    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
85-    host = request.client.host if request.client else None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:17:45.358Z

**tool call — Bash**
````
{
 "command": "sed -n 250,258p app/backend/api.py | cut -c1-260; echo ----; grep -n \"def demo_mode\\|DEMO\\|ENABLE_LIVE\" app/backend/api.py | head -10",
 "description": "Read the paste gate condition in the create route"
}
````

### User / tool · 2026-11-02T11:17:45.452Z

**tool result**
````
    @app.post("/api/cases/pdf", status_code=201)
    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None):
        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer minus hidden text (T-087, `include_hidden`); a scanned PDF is
        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
            raise ApiError(413, "input_too_large", "The PDF is too large.")
----
105:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
117:        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
119:    def demo_mode():
374:        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
375:        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:17:46.806Z

**tool call — Bash**
````
{
 "command": "sed -n 112,125p app/backend/api.py | cut -c1-260; echo ----; sed -n 283,290p app/backend/api.py | cut -c1-200",
 "description": "Read the demo_mode definition and the paste refusal branch"
}
````

### User / tool · 2026-11-02T11:17:46.893Z

**tool result**
````
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
----
        try:
            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
        except ingest.IngestError as e:
            raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
        if demo_mode() and digest(text) not in allowed_hashes():
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        c = conn()
        try:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:17:56.029Z

**tool call — Bash**
````
{
 "command": "grep -rn \"accident_date_conflicts(\" app/backend/*.py app/*.py | head; grep -n \"^def ingest\\|^def split\\|^def parse\" app/backend/ingest.py | head; echo ----; grep -n \"def allowed_hashes\" -A6 app/backend/api.py | cut -c1-200",
 "description": "Find conflict call site and ingest entry points for in-process probes"
}
````

### User / tool · 2026-11-02T11:17:56.142Z

**tool result**
````
app/backend/conflicts.py:40:def accident_date_conflicts(records: list) -> list:
app/backend/pipeline.py:59:    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
app/backend/review.py:442:    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
206:def split_records(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS) -> list:
255:def ingest(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS, splitter=None, not_duplicates=()) -> dict:
----
100:    def allowed_hashes():
101-        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
102-    runs = {}
103-    rejudging = set()
104-    DB.connect(db_path).close()
105-    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
106-        raise RuntimeError("live anthropic-api needs PROVIDER_CAP_CONFIRMED=1 (set a provider-side spend limit first, ADR-006/D-020)")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:17:58.381Z

**tool call — Bash**
````
{
 "command": "sed -n 50,60p app/backend/pipeline.py | cut -c1-240; echo ----; sed -n 436,444p app/backend/review.py | cut -c1-240",
 "description": "Read how pipeline builds records for the accident conflict check"
}
````

### User / tool · 2026-11-02T11:17:58.523Z

**tool result**
````
    """Stage 0. Raises IngestError('bad_request' | 'input_too_large') before anything else. Zero model calls, except the D-031 split
    fallback when `call` is given and the code split found one unsplit block (boundaries are validated by code; records get LLM_SPLIT)."""
    ing = IN.ingest(raw_text, splitter=splitter or (split_llm.make_splitter(call) if call else None), not_duplicates=not_duplicates)
    text = IN.normalize_text(raw_text)
    recs = language.annotate(ing["records"])           # D-042: en | es | other per record; raises UnsupportedLanguage when no record is readable
    language.case_check(recs)
    by_n = {r["n"]: r for r in recs}
    backend = P.backend_name()
    flags = []
    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
    for f in code:
----
    before = {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    backend = DB.get_case(conn, case_id).get("backend") or "code"
    new = {}
    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
        nos = f["record_nos"]
        state, codes = PL._compose_code(by_n, nos, list(f.get("reasons") or []), f["evidence"], case["raw_text"])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:18:03.124Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-123-paralegal-probe.py",
 "old_string": "paste_a = (\"SYNTHETIC — invented for a review probe; not real patient data\\n\\n=== Record 1 ===\\nDate: 2026-03-03\\n\"\n           \"Source: Quillmere Regional ED\\nExcerpt: \\\"Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019. \"\n           \"Left shoulder pain 7/10. X-ray left shoulder negative for fracture.\\\"\\n\")\nst, body = C.req(\"POST\", \"/api/cases\", {\"text\": paste_a, \"name\": \"T-120 synthetic probe\"})\ntok_a = body[\"token\"]\nC.poll_ready(tok_a)\nres[\"A_synthetic_same_sentence_plus_real_prior\"] = pre_flags(C.case(tok_a))\n",
 "new_string": ""
}
````

### User / tool · 2026-11-02T11:18:03.233Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-123-paralegal-probe.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:18:06.026Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-120-123-paralegal-probe.py 2>&1 | tail -5; .venv/bin/python -I -c \"import json; d=json.load(open('artifacts/review-evidence/T-120-123-paralegal-probe.out.json')); print(json.dumps({k:d[k] for k in d if k.startswith('A_')}, ensure_ascii=False, indent=1)[:4000])\"",
 "description": "Run the probe and print the T-120 section results"
}
````

### User / tool · 2026-11-02T11:18:07.863Z

**tool result**
````
A/B written /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-123-paralegal-probe.out.json
{
 "A_raw_lib09_interpreter_sentence_in": [
  1
 ],
 "A_lib09_status": "ready",
 "A_lib09_pre_existing_flags": [],
 "A_lib09_all_flags": [
  {
   "id": "f_gap_r1_r2",
   "type": "gap",
   "category": "gap_over_30",
   "title": "Gap of 42 days"
  },
  {
   "id": "f_date_r4",
   "type": "record_warning",
   "category": "date_ambiguous",
   "title": "Date to confirm"
  },
  {
   "id": "f_r1_1",
   "type": "causation",
   "category": "patient_report",
   "title": "Reported onset"
  },
  {
   "id": "f_r2_1",
   "type": "causation",
   "category": "patient_report",
   "title": "Reported onset"
  },
  {
   "id": "f_r3_1",
   "type": "causation",
   "category": "patient_report",
   "title": "Reported onset"
  }
 ],
 "A_lib09_records": [
  {
   "id": "r1",
   "date": null
  },
  {
   "id": "r2",
   "date": null
  },
  {
   "id": "r3",
   "date": null
  },
  {
   "id": "r4",
   "date": null
  },
  {
   "id": "r5",
   "date": null
  },
  {
   "id": "r6",
   "date": null
  },
  {
   "id": "r7",
   "date": null
  }
 ],
 "A_sample_status": "ready",
 "A_sample_pre_existing_flags": [
  {
   "id": "f_r3_1",
   "title": "Mention of a prior or pre-existing condition",
   "category": "pre_existing",
   "record_nos": null,
   "evidence": [
    {
     "record_id": "r3",
     "excerpt": "Patient reports low back pain in 2023, resolved.",
     "start": 724,
     "end": 772
    }
   ]
  },
  {
   "id": "f_r8_1",
   "title": "Degenerative wording",
   "category": "degenerative_language",
   "record_nos": null,
   "evidence": [
    {
     "record_id": "r8",
     "excerpt": "Findings may represent degenerative change",
     "start": 1595,
     "end": 1637
    }
   ]
  }
 ],
 "A_lib02_pre_existing_flags": [
  {
   "id": "f_r2_1",
   "title": "Mention of prior surgery or repair",
   "category": "prior_surgery",
   "record_nos": null,
   "evidence": [
    {
     "record_id": "r2",
     "excerpt": "X-ray right knee: no acute fracture; prior arthroscopic changes noted.",
     "start": 379,
     "end": 449
    }
   ]
  },
  {
   "id": "f_r3_1",
   "title": "Mention of prior surgery or repair",
   "category": "prior_surgery",
   "record_nos": null,
   "evidence": [
    {
     "record_id": "r3",
     "excerpt": "Patient reports a right knee arthroscopy in 2021 with good recovery before the fall.",
     "start": 604,
     "end": 688
    }
   ]
  },
  {
   "id": "f_r4_1",
   "title": "Degenerative wording",
   "category": "degenerative_language",
   "record_nos": null,
   "evidence": [
    {
     "record_id": "r4",
     "excerpt": "Mild tricompartmental degenerative change.",
     "start": 868,
     "end": 910
    }
   ]
  },
  {
   "id": "f_r4_3",
   "title": "Mention of prior surgery or repair",
   "category": "prior_surgery",
   "record_nos": null,
   "evidence": [
    {
     "record_id": "r4",
     "excerpt": "Findings may reflect both acute injury and prior surgical change.",
     "start": 911,
     "end": 976
    }
   ]
  },
  {
   "id": "f_r5_1",
   "title": "Mention of a prior or pre-existing condition",
   "category": "pre_existing",
   "record_nos": null,
   "evidence": [
    {
     "record_id": "r5",
     "excerpt": "Aggravation of the underlying knee condition is possible.",
     "start": 1188,
     "end": 1245
    }
   ]
  }
 ],
 "A_lib11_pre_existing_flags": [
  {
   "id": "f_r1_1",
   "title": "Mention of a prior or pre-existing condition",
   "category": "pre_existing",
   "record_nos": null,
   "evidence": [
    {
     "record_id": "r1",
     "excerpt": "Problem list: hypertension, type 2 diabetes, chronic low back pain.",
     "start": 272,
     "end": 339
    }
   ]
  },
  {
   "id": "f_r1_2",
   "title": "Mention of a prior or pre-existing condition",
   "category": "pre_existing",
   "record_nos": null,
   "evidence": [
    {
     "record_id": "r1",
     "excerpt": "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy.",
     "start": 160,
     "end": 271
    }
   ]
  },
  {
   "id": "f
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:18:13.119Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\nd=json.load(open('artifacts/review-evidence/T-120-123-paralegal-probe.out.json'))\nprint('translation', json.dumps(d['B_lib09_translation_fields'], ensure_ascii=False)[:900])\nprint('accept', d['B_lib09_accept_status'])\nprint('export status', d['B_lib09_export_status'])\nprint('--- STANDARD lib09'); print(d['B_lib09_standard_letter'])\nprint('--- ONELINE lib09'); print(d['B_lib09_oneline_letter'])\n\"",
 "description": "Print lib09 standard and oneline letters from the probe output"
}
````

### User / tool · 2026-11-02T11:18:13.245Z

**tool result**
````
translation {"e1": null, "e2": {"source_language": "es", "source_language_name": "Spanish", "label": "AI translation", "review_label": "AI translation — check against the original", "summary_is_translation": true, "quote_is_original": true}, "e3": null, "e5": null, "e6": null, "e7": {"source_language": "es", "source_language_name": "Spanish", "label": "AI translation", "review_label": "AI translation — check against the original", "summary_is_translation": true, "quote_is_original": true}}
accept {'e1': 200, 'e2': 200, 'e3': 200, 'e5': 200, 'e6': 200, 'e7': 200, 'a1': 200, 'a4': 200, 'a3': 200, 'a6': 200}
export status [200, 200]
--- STANDARD lib09
TREATMENT CHRONOLOGY

March 3, 2026 — Quillmere Regional ED
Left shoulder pain 7/10; X-ray of left shoulder negative for fracture; diagnosis left shoulder contusion; ED charge $2,940.
Source [Ex. __ / Bates __]: "Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940."

April 14, 2026 — Consultorio Médico Aguaclara, nota de consulta
Patient reports pain 6/10 that worsens when raising the arm. Denies loss of consciousness. Exam: pain on palpation of the right shoulder. Plan: physical therapy and follow-up in 4 weeks.
Source [Ex. __ / Bates __]: "Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas." [AI translation of the Spanish original; check before sending]

April 21, 2026 — Dr. Lucan Ostrowe, orthopedics, new patient
Patient states she fell in the parking lot after a car brushed her; right shoulder pain 6/10; MRI of the right shoulder ordered.
Source [Ex. __ / Bates __]: "Patient states she fell in the parking lot after a car brushed her. Right shoulder pain 6/10. MRI right shoulder ordered."

May 5, 2026 — Cinder Valley Imaging, right shoulder MRI
Partial-thickness supraspinatus tear. MRI charge: $2,150.
Source [Ex. __ / Bates __]: "Partial-thickness supraspinatus tear. MRI charge: $2,150."

May 12, 2026 — Dr. Lucan Ostrowe, orthopedics, follow-up
MRI reviewed. Physical therapy and subacromial injection recommended.
Source [Ex. __ / Bates __]: "MRI reviewed. Recommend physical therapy and subacromial injection."

May 20, 2026 — Consultorio Médico Aguaclara, estado de cuenta (billing statement)
Account statement: consultations $1,300.00; physical therapy, 4 sessions at $400.00 per session. Balance: $2,900.00.
Source [Ex. __ / Bates __]: "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00." [AI translation of the Spanish original; check before sending]

BILLED CHARGES

Quillmere Regional ED, March 3, 2026: $2,940.00
Source [Ex. __ / Bates __]: "ED charge: $2,940."
Cinder Valley Imaging, right shoulder MRI, May 5, 2026: $2,150.00
Source [Ex. __ / Bates __]: "MRI charge: $2,150."

Billed charges stated in these records: $5,090.00
--- ONELINE lib09
TREATMENT CHRONOLOGY

March 3, 2026 — Quillmere Regional ED: "Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940." [Ex. __ / Bates __]
April 14, 2026 — Consultorio Médico Aguaclara, nota de consulta: "Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas." [Ex. __ / Bates __] [AI translation of the Spanish original; check before sending]
April 21, 2026 — Dr. Lucan Ostrowe, orthopedics, new patient: "Patient states she fell in the parking lot after a car brushed her. Right shoulder pain 6/10. MRI right shoulder ordered." [Ex. __ / Bates __]
May 5, 2026 — Cinder Valley Imaging, right shoulder MRI: "Partial-thickness supraspinatus tear. MRI charge: $2,150." [Ex. __ / Bates __]
May 12, 2026 — Dr. Lucan Ostrowe, orthopedics, follow-up: "MRI reviewed. Recommend physical therapy and subacromial injection." [Ex. __ / Bates __]
May 20, 2026 — Consultorio Médico Aguaclara, estado de cuenta (billing statement): "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00." [Ex. __ / Bates __] [AI translation of the Spanish original; check before sending]

BILLED CHARGES

Quillmere Regional ED, March 3, 2026: $2,940.00
Source [Ex. __ / Bates __]: "ED charge: $2,940."
Cinder Valley Imaging, right shoulder MRI, May 5, 2026: $2,150.00
Source [Ex. __ / Bates __]: "MRI charge: $2,150."

Billed charges stated in these records: $5,090.00
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:18:26.987Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\nd=json.load(open('artifacts/review-evidence/T-120-123-paralegal-probe.out.json'))\nprint('sample accept', d['B_sample_accept_status'])\nprint('sample export', d['B_sample_export_status'], 'invalid style', d['B_sample_invalid_style'])\ng=open('evals/golden/sample.export.expected.txt',encoding='utf-8').read()\nimport re\nblk=re.search(r'=== LETTER_TEXT[^\\n]*===\\n(.*?)\\n=== ', g, re.S).group(1)\nprint('golden block equal to std:', blk.strip()==d['B_sample_standard_letter'].strip())\nprint('--- SAMPLE ONELINE'); print(d['B_sample_oneline_letter'])\n\"; grep -n \"^=== \" evals/golden/sample.export.expected.txt",
 "description": "Compare sample standard letter to golden and print sample oneline"
}
````

### User / tool · 2026-11-02T11:18:27.101Z

**tool result**
````
sample accept {'e1': 200, 'e2': 200, 'e3': 200, 'e4': 200, 'e5': 200, 'e6': 200, 'e7': 200, 'e8': 200, 'e9': 200, 'a1': 200, 'a4': 200, 'a2': 200}
sample export [200, 200] invalid style 422
golden block equal to std: True
--- SAMPLE ONELINE
TREATMENT CHRONOLOGY

January 9, 2026 — Austin EMS run report: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER." [Ex. __ / Bates __]
January 9, 2026 — Central ER discharge summary: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week." [Ex. __ / Bates __]
January 16, 2026 — Dr. Alvarez, primary care: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks." [Ex. __ / Bates __]
January 23, 2026 — Capital PT, initial evaluation: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits." [Ex. __ / Bates __]
February 20, 2026 — Capital PT, visit 8: "Pain 4/10, improving." [Ex. __ / Bates __]
March 6, 2026 — Capital PT, visit 9: "Discharged from PT after two missed appointments. Pain 3/10." [Ex. __ / Bates __]
May 18, 2026 — Hill Country Pain Management, new patient: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered." [Ex. __ / Bates __]
May 29, 2026 — Austin Imaging, cervical MRI: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically." [Ex. __ / Bates __]
June 12, 2026 — Hill Country Pain Management, follow-up: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision." [Ex. __ / Bates __]

BILLED CHARGES

Central ER discharge summary, January 9, 2026: $6,240.00
Source [Ex. __ / Bates __]: "ER charges: $6,240."
Austin Imaging, cervical MRI, May 29, 2026: $2,150.00
Source [Ex. __ / Bates __]: "Charge: $2,150."

Billed charges stated in these records: $8,390.00
1:=== LETTER_TEXT (block 1: paste into letter) ===
48:=== INTERNAL_NOTES_TEXT (block 2: do not send) ===
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:18:34.854Z

**tool call — Bash**
````
{
 "command": "P=$(git rev-parse 1cb8707^) && echo \"parent $P\" && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p \"$SCR/t120-parent-archive\" && git archive \"$P\" | tar -x -C \"$SCR/t120-parent-archive\" && ls \"$SCR/t120-parent-archive\" | head -3 && git log -1 --format='%h %s' \"$P\"",
 "description": "Extract the pre-T-120 parent commit into the scratchpad for before/after"
}
````

### User / tool · 2026-11-02T11:18:34.921Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: P=$(git rev-parse 1cb8707^) && echo "parent $P" && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-427
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:18:36.165Z

**tool call — Bash**
````
{
 "command": "git rev-parse 1cb8707^ && git log -1 --format='%h %s' 1cb8707^",
 "description": "Resolve the pre-T-120 parent commit"
}
````

### User / tool · 2026-11-02T11:18:36.282Z

**tool result**
````
0c473563bed3cd6b74ac0db83ee47cb13785fb71
0c47356 fix(backend): T-123 accident baseline never calls same-day paperwork or questionnaire/authorization headers the first recorded treatment
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:18:41.240Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120-parent-archive && git archive 0c47356 | tar -x -C /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120-parent-archive && ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120-parent-archive | head -3",
 "description": "Extract commit 0c47356 (pre-T-120) into the scratchpad"
}
````

### User / tool · 2026-11-02T11:18:41.736Z

**tool result**
````
CLAUDE.md
MASTER_PROMPT.md
app
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:18:45.550Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$SCR/t120-parent-archive\" && LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=\"$SCR/t120-parent.sqlite3\" PORT=7894 PYTHONPATH=\"$SCR/t120-parent-archive\" PYTHONDONTWRITEBYTECODE=1 nohup /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > \"$SCR/t120-parent-server.log\" 2>&1 &\nsleep 5; curl -s -o /dev/null -w \"%{http_code}\\n\" http://127.0.0.1:7894/; lsof -iTCP:7894 -sTCP:LISTEN -nP | tail -1",
 "description": "Start the pre-T-120 parent server on port 7894"
}
````

### User / tool · 2026-11-02T11:18:50.813Z

**tool result**
````
200
Python  95532 arsis    9u  IPv4 0xaa25b7f7479ddec0      0t0  TCP 127.0.0.1:7894 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:18:55.556Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-120-paralegal-before-after.py <<'EOF'\n\"\"\"T-120 before/after: lib09 pre_existing flags on the pre-T-120 parent (0c47356, port 7894) and HEAD (63e18ed, port 7893).\nRun once per server: ZLAYT_BASE=http://127.0.0.1:7894 .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-before-after.py parent\nPrints the flags as JSON; no state is written outside the server's scratch DB.\"\"\"\nimport importlib.util, json, os, sys\nHERE = os.path.dirname(os.path.abspath(__file__))\n_s = importlib.util.spec_from_file_location(\"c\", os.path.join(HERE, \"T-120-123-paralegal-common.py\")); C = importlib.util.module_from_spec(_s); _s.loader.exec_module(C)\nlabel = sys.argv[1] if len(sys.argv) > 1 else \"run\"\nout = {\"label\": label, \"base\": C.BASE}\nfor lib in (\"case_lib09_spanish_interpreter_espalda\",):\n    tok = C.load_library(lib)\n    out[\"status\"] = C.poll_ready(tok)\n    cs = C.case(tok)\n    out[\"pre_existing\"] = [{\"id\": f[\"id\"], \"title\": f[\"title\"], \"record_nos_or_ids\": [e.get(\"record_id\") for e in f.get(\"evidence\") or []],\n                            \"excerpt\": [e.get(\"excerpt\") for e in f.get(\"evidence\") or []]} for f in cs[\"flags\"] if f[\"type\"] == \"pre_existing\"]\n    out[\"all_flag_ids\"] = sorted(f[\"id\"] for f in cs[\"flags\"])\nprint(json.dumps(out, ensure_ascii=False, indent=1))\nEOF\nZLAYT_BASE=http://127.0.0.1:7894 .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-before-after.py parent; echo ======; ZLAYT_BASE=http://127.0.0.1:7893 .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-before-after.py head",
 "description": "Run lib09 pre-existing flag check on parent and HEAD servers"
}
````

### User / tool · 2026-11-02T11:18:56.592Z

**tool result**
````
{
 "label": "parent",
 "base": "http://127.0.0.1:7894",
 "status": "ready",
 "pre_existing": [
  {
   "id": "f_r1_1",
   "title": "Mention of a prior or pre-existing condition",
   "record_nos_or_ids": [
    "r1"
   ],
   "excerpt": [
    "Hx obtained via patient's son, who interpreted."
   ]
  }
 ],
 "all_flag_ids": [
  "f_date_r4",
  "f_gap_r1_r2",
  "f_r1_1",
  "f_r1_2",
  "f_r2_1",
  "f_r3_1"
 ]
}
======
{
 "label": "head",
 "base": "http://127.0.0.1:7893",
 "status": "ready",
 "pre_existing": [],
 "all_flag_ids": [
  "f_date_r4",
  "f_gap_r1_r2",
  "f_r1_1",
  "f_r2_1",
  "f_r3_1"
 ]
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:19:02.600Z

**tool call — Bash**
````
{
 "command": "grep -n \"lib09\\|def test_lib09\" -A8 tests/unit/test_t120_history_source_sentence.py | cut -c1-240 | head -40",
 "description": "Read the lib09 unit test in the T-120 test file"
}
````

### User / tool · 2026-11-02T11:19:02.690Z

**tool result**
````
41:def test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do():
42:    recs = I.ingest((ROOT / "evals/library/case_lib09_spanish_interpreter_espalda.txt").read_text(encoding="utf-8"))["records"]
43-    interp = next(r for r in recs if "Hx obtained via" in r["excerpt"])
44-    assert [f for f in FL.lexicon_flags(interp) if f["type"] == "pre_existing"] == []
45-    real = dict(interp, excerpt="Hx obtained via patient's son, who interpreted. Prior history of left shoulder dislocation 2019. Pain 7/10.")
46-    pre = [f for f in FL.lexicon_flags(real) if f["type"] == "pre_existing"]
47-    assert pre and all("Hx obtained via" not in f["excerpt"] for f in pre)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:19:14.880Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-120-paralegal-variants.py <<'EOF'\n\"\"\"T-120 in-process variants (code only, no model): does the source-sentence skip hide a real prior-condition mention next to it?\nRun: ARCH=<git archive HEAD copy> .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-variants.py\nCalls app.backend.lexicon_scan.scan (the function the flag engine uses) on each text and prints every pre_existing hit.\"\"\"\nimport os, sys\nARCH = os.environ[\"ARCH\"]\nsys.path.insert(0, ARCH)\nsys.dont_write_bytecode = True\nfrom app.backend import lexicon_scan as LS  # noqa: E402\n\nTEXTS = [\n    \"Hx obtained via patient's son, who interpreted. Left shoulder pain 7/10.\",\n    \"Hx obtained via patient's son, who interpreted. Low back pain in 2023, resolved.\",\n    \"Hx obtained via interpreter: lumbar strain 2019.\",\n    \"History provided by patient: prior neck surgery 2018.\",\n    \"Hx obtained from patient's daughter. Prior low back pain 2023, resolved.\",\n    \"PHx obtained via patient's son: lumbar strain 2019.\",\n    \"Hx per patient's son. Degenerative change at L4-L5 on prior films.\",\n    \"History obtained via interpreter; patient had a left knee arthroscopy in 2021.\",\n    \"Hx: lumbar strain 2019, obtained via interpreter.\",\n    \"Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019.\",\n    \"History per patient: car accidents in 2019 and 2022 with neck and low back pain.\",\n]\nfor t in TEXTS:\n    hits = [h for h in LS.scan(t) if h[\"flag_type\"] == \"pre_existing\"]\n    shown = [t[h[\"unit_start\"]:h[\"unit_end\"]] for h in hits]\n    print((\"FLAG  \" if hits else \"none  \") + repr(t)); print(\"        unit(s):\", shown)\nEOF\nSCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-variants.py 2>&1 | tail -30",
 "description": "Probe the T-120 source-sentence skip on realistic variant texts"
}
````

### User / tool · 2026-11-02T11:19:15.087Z

**tool result**
````
none  "Hx obtained via patient's son, who interpreted. Left shoulder pain 7/10."
        unit(s): []
FLAG  "Hx obtained via patient's son, who interpreted. Low back pain in 2023, resolved."
        unit(s): ['Low back pain in 2023, resolved.']
none  'Hx obtained via interpreter: lumbar strain 2019.'
        unit(s): []
FLAG  'History provided by patient: prior neck surgery 2018.'
        unit(s): ['History provided by patient: prior neck surgery 2018.']
FLAG  "Hx obtained from patient's daughter. Prior low back pain 2023, resolved."
        unit(s): ['Prior low back pain 2023, resolved.', 'Prior low back pain 2023, resolved.']
none  "PHx obtained via patient's son: lumbar strain 2019."
        unit(s): []
FLAG  "Hx per patient's son. Degenerative change at L4-L5 on prior films."
        unit(s): ['Degenerative change at L4-L5 on prior films.', 'Degenerative change at L4-L5 on prior films.']
FLAG  'History obtained via interpreter; patient had a left knee arthroscopy in 2021.'
        unit(s): ['patient had a left knee arthroscopy in 2021.']
FLAG  'Hx: lumbar strain 2019, obtained via interpreter.'
        unit(s): ['Hx: lumbar strain 2019, obtained via interpreter.']
FLAG  "Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019."
        unit(s): ['Hx of lumbar strain 2019.']
none  'History per patient: car accidents in 2019 and 2022 with neck and low back pain.'
        unit(s): []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:19:21.181Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/t120-parent-archive\" .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-variants.py 2>&1 | tail -30",
 "description": "Run the same T-120 variant probe against the pre-T-120 parent"
}
````

### User / tool · 2026-11-02T11:19:21.386Z

**tool result**
````
FLAG  "Hx obtained via patient's son, who interpreted. Left shoulder pain 7/10."
        unit(s): ["Hx obtained via patient's son, who interpreted."]
FLAG  "Hx obtained via patient's son, who interpreted. Low back pain in 2023, resolved."
        unit(s): ['Low back pain in 2023, resolved.', "Hx obtained via patient's son, who interpreted."]
FLAG  'Hx obtained via interpreter: lumbar strain 2019.'
        unit(s): ['Hx obtained via interpreter: lumbar strain 2019.']
FLAG  'History provided by patient: prior neck surgery 2018.'
        unit(s): ['History provided by patient: prior neck surgery 2018.']
FLAG  "Hx obtained from patient's daughter. Prior low back pain 2023, resolved."
        unit(s): ['Prior low back pain 2023, resolved.', "Hx obtained from patient's daughter.", 'Prior low back pain 2023, resolved.']
FLAG  "PHx obtained via patient's son: lumbar strain 2019."
        unit(s): ["PHx obtained via patient's son: lumbar strain 2019."]
FLAG  "Hx per patient's son. Degenerative change at L4-L5 on prior films."
        unit(s): ["Hx per patient's son.", 'Degenerative change at L4-L5 on prior films.', 'Degenerative change at L4-L5 on prior films.']
FLAG  'History obtained via interpreter; patient had a left knee arthroscopy in 2021.'
        unit(s): ['patient had a left knee arthroscopy in 2021.']
FLAG  'Hx: lumbar strain 2019, obtained via interpreter.'
        unit(s): ['Hx: lumbar strain 2019, obtained via interpreter.']
FLAG  "Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019."
        unit(s): ["Hx obtained via patient's son, who interpreted.", 'Hx of lumbar strain 2019.']
none  'History per patient: car accidents in 2019 and 2022 with neck and low back pain.'
        unit(s): []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:19:37.781Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-120-paralegal-engine.py <<'EOF'\n\"\"\"T-120 engine-level check: the same record dict through flags.lexicon_flags (the flag engine the pipeline calls), HEAD vs parent.\nRun: ARCH=<archive> .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-engine.py\nThe record is lib09 record 1 (the card says 'record 2'; the sentence is in record 1 of the library file) with its excerpt replaced.\"\"\"\nimport os, sys\nARCH = os.environ[\"ARCH\"]\nsys.path.insert(0, ARCH)\nsys.dont_write_bytecode = True\nfrom app.backend import flags as FL, ingest as I  # noqa: E402\nrecs = I.ingest(open(os.path.join(ARCH, \"evals/library/case_lib09_spanish_interpreter_espalda.txt\"), encoding=\"utf-8\").read())[\"records\"]\nprint(\"lib09 records with the sentence:\", [r[\"n\"] for r in recs if \"Hx obtained via\" in r[\"excerpt\"]])\nbase = next(r for r in recs if \"Hx obtained via\" in r[\"excerpt\"])\nfor exc in (\"Hx obtained via interpreter: lumbar strain 2019.\",\n            \"PHx obtained via patient's son: lumbar strain 2019.\",\n            \"Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019.\"):\n    rec = dict(base, excerpt=exc)\n    pre = [f for f in FL.lexicon_flags(rec) if f[\"type\"] == \"pre_existing\"]\n    print(repr(exc), \"->\", [f[\"excerpt\"] for f in pre] or \"NO pre_existing flag\")\nEOF\nSCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo \"== HEAD 63e18ed\"; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-engine.py 2>&1 | tail -6; echo \"== parent 0c47356\"; ARCH=\"$SCR/t120-parent-archive\" .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-engine.py 2>&1 | tail -6",
 "description": "Compare the flag engine output for colon variants on HEAD and parent"
}
````

### User / tool · 2026-11-02T11:19:38.449Z

**tool result**
````
== HEAD 63e18ed
lib09 records with the sentence: [1]
'Hx obtained via interpreter: lumbar strain 2019.' -> NO pre_existing flag
"PHx obtained via patient's son: lumbar strain 2019." -> NO pre_existing flag
"Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019." -> ['Hx of lumbar strain 2019.']
== parent 0c47356
lib09 records with the sentence: [1]
'Hx obtained via interpreter: lumbar strain 2019.' -> ['Hx obtained via interpreter: lumbar strain 2019.']
"PHx obtained via patient's son: lumbar strain 2019." -> ["PHx obtained via patient's son: lumbar strain 2019."]
"Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019." -> ["Hx obtained via patient's son, who interpreted.", 'Hx of lumbar strain 2019.']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:19:55.621Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-121-paralegal-letter-check.py <<'EOF'\n\"\"\"T-121 letter check: every letter line of the lib09 and sample exports (both styles) against the raw record text in the HEAD copy.\nRun: ARCH=<archive> .venv/bin/python -I artifacts/review-evidence/T-121-paralegal-letter-check.py\nChecks per entry line: long date equals the raw record date (lib09 DD/MM read as DMY per the record's own convention), provider string equals\nthe raw Source label, quote is a verbatim substring of the raw record (whitespace-normalised), citation placeholder present, translation note\nbracketed at end of line, and no line starts with 'AI translation:'.\"\"\"\nimport json, os, re, sys\nARCH = os.environ[\"ARCH\"]\nHERE = os.path.dirname(os.path.abspath(__file__))\nMONTHS = \"January February March April May June July August September October November December\".split()\nNOTE = \"[AI translation of the Spanish original; check before sending]\"\nd = json.load(open(os.path.join(HERE, \"T-120-123-paralegal-probe.out.json\"), encoding=\"utf-8\"))\n\n\ndef norm(s):\n    return \" \".join((s or \"\").split())\n\n\ndef raw(path):\n    text = open(path, encoding=\"utf-8\").read()\n    parts = re.split(r\"^=== Record (\\d+) ===\\s*$\", text, flags=re.M)\n    out = []\n    for i in range(1, len(parts), 2):\n        body = parts[i + 1]\n        date = re.search(r\"^Date:\\s*(.+)$\", body, re.M).group(1).strip()\n        src = re.search(r\"^Source:\\s*(.+)$\", body, re.M).group(1).strip()\n        exc = re.search(r'^Excerpt:\\s*\"(.*)\"\\s*$', body, re.M).group(1)\n        out.append({\"n\": int(parts[i]), \"date\": date, \"source\": src, \"excerpt\": exc})\n    return out\n\n\ndef iso_of(s):\n    m = re.match(r\"^(\\d{4})-(\\d{2})-(\\d{2})$\", s)\n    if m:\n        return s\n    m = re.match(r\"^(\\d{2})/(\\d{2})/(\\d{4})$\", s)\n    if m:  # both lib09 DD/MM (record 2: 14/04/2026) and MM/DD appear; the record 4 date is ambiguous and is not an entry\n        dd, mm, yy = m.groups()\n        return f\"{yy}-{mm}-{dd}\" if int(dd) > 12 else f\"{yy}-{mm}-{dd}\"\n    return None\n\n\ndef long(iso):\n    y, m, dd = iso.split(\"-\")\n    return f\"{MONTHS[int(m) - 1]} {int(dd)}, {y}\"\n\n\ndef check(label, letter, recs):\n    lines = letter.splitlines()\n    rows, problems = [], []\n    for ln in lines:\n        if ln.startswith(\"AI translation:\"):\n            problems.append((\"PREFIX_LINE\", ln))\n        if ONE.match(ln) or STD.match(ln):\n            rows.append(ln)\n    hits = []\n    for r in recs:\n        dstr = long(iso_of(r[\"date\"])) if iso_of(r[\"date\"]) else None\n        hits.append((r[\"n\"], dstr, r[\"source\"], norm(r[\"excerpt\"])))\n    report = {\"label\": label, \"entry_lines\": len(rows), \"problems\": problems, \"lines\": []}\n    for ln in rows:\n        m = ONE.match(ln) if style_is_one else STD.match(ln)\n        if style_is_one:\n            date, prov, quote, note = m.group(1), m.group(2), m.group(3), m.group(4)\n        else:\n            date, prov, quote, note = m.group(1), m.group(2), m.group(3), m.group(4)\n        cand = [h for h in hits if h[1] == date and h[2] == prov]\n        ok_src = bool(cand)\n        verb = any(norm(quote) in h[3] for h in cand) if cand else False\n        report[\"lines\"].append({\"date\": date, \"provider\": prov, \"record\": cand[0][0] if cand else None,\n                                \"provider_matches_raw_label\": ok_src, \"quote_verbatim_in_raw\": verb, \"note_at_end\": bool(note)})\n    return report\n\n\nONE = re.compile(r'^((?:January|February|March|April|May|June|July|August|September|October|November|December) \\d{1,2}, \\d{4}) — (.+?): \"(.*)\" \\[Ex\\. __ / Bates __\\]( \\[AI translation of the Spanish original; check before sending\\])?$')\nSTD = re.compile(r'^Source \\[Ex\\. __ / Bates __\\]: \"(.*)\"( \\[AI translation of the Spanish original; check before sending\\])?$')\nstyle_is_one = False\nout = {}\nr09 = raw(os.path.join(ARCH, \"evals/library/case_lib09_spanish_interpreter_espalda.txt\"))\nr_s = raw(os.path.join(ARCH, \"evals/golden/sample.txt\"))\n\n# lib09 oneline (style_is_one True)\nstyle_is_one = True\nout[\"lib09_oneline\"] = check(\"lib09 oneline\", d[\"B_lib09_oneline_letter\"], [r for r in r09 if r[\"n\"] in (1, 2, 3, 5, 6, 7)])\nout[\"sample_oneline\"] = check(\"sample oneline\", d[\"B_sample_oneline_letter\"], r_s)\n# standard: the Source line is the quote; the provider is on the header line before the summary\nstyle_is_one = False\nstd_text = d[\"B_lib09_standard_letter\"]\nheads = [ln for ln in std_text.splitlines() if re.match(r\"^(January|February|March|April|May|June|July|August|September|October|November|December) \\d{1,2}, \\d{4} — \", ln)]\nsrcs = [ln for ln in std_text.splitlines() if ln.startswith(\"Source [Ex. __ / Bates __]:\")]\nout[\"lib09_standard_pairs\"] = len(heads) == len(srcs)\nout[\"lib09_standard_notes_on_source_line\"] = [bool(STD.match(s)) and bool(STD.match(s).group(2)) for s in srcs]\nfor h, s in zip(heads, srcs):\n    dm = re.match(r\"^((?:[A-Za-z]+) \\d{1,2}, \\d{4}) — (.+)$\", h)\n    q = STD.match(s).group(1)\n    cand = [r for r in r09 if long(iso_of(r[\"date\"])) == dm.group(1) and r[\"source\"] == dm.group(2) and norm(q) in norm(r[\"excerpt\"])]\n    out.setdefault(\"lib09_standard_rows\", []).append({\"head\": h, \"quote_verbatim_in_raw\": bool(cand), \"record\": cand[0][\"n\"] if cand else None})\nout[\"lib09_standard_rows_total\"] = len(srcs)\nout[\"lib09_standard_rows_ok\"] = sum(1 for x in out[\"lib09_standard_rows\"] if x[\"quote_verbatim_in_raw\"])\nprint(json.dumps(out, ensure_ascii=False, indent=1))\njson.dump(out, open(os.path.join(HERE, \"T-121-paralegal-letter-check.out.json\"), \"w\", encoding=\"utf-8\"), ensure_ascii=False, indent=1)\nEOF\nSCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-121-paralegal-letter-check.py 2>&1 | head -150",
 "description": "Verify every T-121 letter line against the raw record text"
}
````

### User / tool · 2026-11-02T11:19:55.774Z

**tool result**
````
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-121-paralegal-letter-check.py", line 83, in <module>
    out["lib09_oneline"] = check("lib09 oneline", d["B_lib09_oneline_letter"], [r for r in r09 if r["n"] in (1, 2, 3, 5, 6, 7)])
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-121-paralegal-letter-check.py", line 63, in check
    date, prov, quote, note = m.group(1), m.group(2), m.group(3), m.group(4)
                              ^^^^^^^
AttributeError: 'NoneType' object has no attribute 'group'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:20:08.246Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-121-paralegal-letter-check.py <<'EOF'\n\"\"\"T-121 letter check: each entry line of the lib09 and sample exports (both styles) against the raw record text in the HEAD copy.\nRun: ARCH=<archive> .venv/bin/python -I artifacts/review-evidence/T-121-paralegal-letter-check.py\nOneline: each line `date — provider: \"quote\" [Ex. __ / Bates __]` (+ optional translation note). Checked: the long date equals the raw record\ndate (ISO, or DD/MM/YYYY as the lib09 record 2 reads), the provider equals the raw Source label, the quote is a verbatim substring of the raw\nexcerpt (whitespace-normalised). Standard: header line + `Source [Ex. __ / Bates __]: \"quote\"` pairs, the same three checks.\nAlso: no line starts with 'AI translation:' in either style. Writes T-121-paralegal-letter-check.out.json next to this file.\"\"\"\nimport json, os, re\nARCH = os.environ[\"ARCH\"]\nHERE = os.path.dirname(os.path.abspath(__file__))\nMONTHS = \"January February March April May June July August September October November December\".split()\nNOTE = \"[AI translation of the Spanish original; check before sending]\"\nMONTH_RX = \"(?:\" + \"|\".join(MONTHS) + \")\"\nONE = re.compile(r'^(' + MONTH_RX + r' \\d{1,2}, \\d{4}) — (.+?): \"(.*)\" \\[Ex\\. __ / Bates __\\]( ' + re.escape(NOTE) + r')?$')\nHEAD = re.compile(r'^(' + MONTH_RX + r' \\d{1,2}, \\d{4}) — (.+)$')\nSRC = re.compile(r'^Source \\[Ex\\. __ / Bates __\\]: \"(.*)\"( ' + re.escape(NOTE) + r')?$')\nd = json.load(open(os.path.join(HERE, \"T-120-123-paralegal-probe.out.json\"), encoding=\"utf-8\"))\n\n\ndef norm(s):\n    return \" \".join((s or \"\").split())\n\n\ndef raw(path):\n    text = open(path, encoding=\"utf-8\").read()\n    parts = re.split(r\"^=== Record (\\d+) ===\\s*$\", text, flags=re.M)\n    out = []\n    for i in range(1, len(parts), 2):\n        body = parts[i + 1]\n        out.append({\"n\": int(parts[i]), \"date\": re.search(r\"^Date:\\s*(.+)$\", body, re.M).group(1).strip(),\n                    \"source\": re.search(r\"^Source:\\s*(.+)$\", body, re.M).group(1).strip(),\n                    \"excerpt\": norm(re.search(r'^Excerpt:\\s*\"(.*)\"\\s*$', body, re.M).group(1))})\n    return out\n\n\ndef iso(s):\n    if re.match(r\"^\\d{4}-\\d{2}-\\d{2}$\", s):\n        return s\n    m = re.match(r\"^(\\d{2})/(\\d{2})/(\\d{4})$\", s)\n    return f\"{m.group(3)}-{m.group(2)}-{m.group(1)}\" if m else None   # DD/MM as read by the record's own convention (record 2)\n\n\ndef long(s):\n    y, m, dd = s.split(\"-\")\n    return f\"{MONTHS[int(m) - 1]} {int(dd)}, {y}\"\n\n\ndef verify(pairs, recs):\n    rows = []\n    for date, prov, quote, note in pairs:\n        hit = [r for r in recs if iso(r[\"date\"]) and long(iso(r[\"date\"])) == date and r[\"source\"] == prov]\n        rows.append({\"date\": date, \"provider\": prov, \"raw_record\": hit[0][\"n\"] if hit else None,\n                     \"quote_verbatim\": any(norm(quote) in r[\"excerpt\"] for r in hit), \"note_bracketed_at_end\": bool(note)})\n    return rows\n\n\nr09 = raw(os.path.join(ARCH, \"evals/library/case_lib09_spanish_interpreter_espalda.txt\"))\nrs = raw(os.path.join(ARCH, \"evals/golden/sample.txt\"))\nout = {}\nfor key, text, recs in ((\"lib09_oneline\", d[\"B_lib09_oneline_letter\"], r09), (\"sample_oneline\", d[\"B_sample_oneline_letter\"], rs)):\n    pairs = [(m.group(1), m.group(2), m.group(3), m.group(4)) for m in (ONE.match(ln) for ln in text.splitlines()) if m]\n    out[key] = {\"entry_lines\": len(pairs), \"rows\": verify(pairs, recs), \"prefix_lines\": sum(1 for ln in text.splitlines() if ln.startswith(\"AI translation:\"))}\nfor key, text, recs in ((\"lib09_standard\", d[\"B_lib09_standard_letter\"], r09), (\"sample_standard\", d[\"B_sample_standard_letter\"], rs)):\n    lines = text.splitlines()\n    pairs = []\n    for i, ln in enumerate(lines):\n        h = HEAD.match(ln)\n        if h and i + 1 < len(lines) and SRC.match(lines[i + 1]):\n            s = SRC.match(lines[i + 1])\n            pairs.append((h.group(1), h.group(2), s.group(1), s.group(2)))\n    out[key] = {\"entry_pairs\": len(pairs), \"rows\": verify(pairs, recs), \"prefix_lines\": sum(1 for ln in lines if ln.startswith(\"AI translation:\"))}\nout[\"charges_block_lib09\"] = d[\"B_lib09_standard_letter\"][d[\"B_lib09_standard_letter\"].index(\"BILLED CHARGES\"):]\nprint(json.dumps(out, ensure_ascii=False, indent=1))\njson.dump(out, open(os.path.join(HERE, \"T-121-paralegal-letter-check.out.json\"), \"w\", encoding=\"utf-8\"), ensure_ascii=False, indent=1)\nEOF\nSCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-121-paralegal-letter-check.py > /dev/null 2>&1; .venv/bin/python -I -c \"\nimport json\no=json.load(open('artifacts/review-evidence/T-121-paralegal-letter-check.out.json'))\nfor k in ('lib09_oneline','sample_oneline','lib09_standard','sample_standard'):\n    v=o[k]; rows=v['rows']\n    print(k, {x:v[x] for x in v if x!='rows'}, 'rows', len(rows), 'verbatim', sum(r['quote_verbatim'] for r in rows), 'raw-match', sum(r['raw_record'] is not None for r in rows), 'notes', sum(r['note_bracketed_at_end'] for r in rows))\n    for r in rows:\n        if not r['quote_verbatim'] or r['raw_record'] is None or r['note_bracketed_at_end']: print('   ', r)\n\"",
 "description": "Run the T-121 letter verification and summarise the counts"
}
````

### User / tool · 2026-11-02T11:20:08.392Z

**tool result**
````
lib09_oneline {'entry_lines': 6, 'prefix_lines': 0} rows 6 verbatim 6 raw-match 6 notes 2
    {'date': 'April 14, 2026', 'provider': 'Consultorio Médico Aguaclara, nota de consulta', 'raw_record': 2, 'quote_verbatim': True, 'note_bracketed_at_end': True}
    {'date': 'May 20, 2026', 'provider': 'Consultorio Médico Aguaclara, estado de cuenta (billing statement)', 'raw_record': 7, 'quote_verbatim': True, 'note_bracketed_at_end': True}
sample_oneline {'entry_lines': 9, 'prefix_lines': 0} rows 9 verbatim 9 raw-match 9 notes 0
lib09_standard {'entry_pairs': 0, 'prefix_lines': 0} rows 0 verbatim 0 raw-match 0 notes 0
sample_standard {'entry_pairs': 0, 'prefix_lines': 0} rows 0 verbatim 0 raw-match 0 notes 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:20:13.923Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport re\np='artifacts/review-evidence/T-121-paralegal-letter-check.py'\ns=open(p,encoding='utf-8').read()\nold='''        if h and i + 1 < len(lines) and SRC.match(lines[i + 1]):\n            s = SRC.match(lines[i + 1])\n            pairs.append((h.group(1), h.group(2), s.group(1), s.group(2)))'''\nnew='''        nxt = [SRC.match(x) for x in lines[i + 1:i + 3] if SRC.match(x)]     # header, then the summary line, then the Source line\n        if h and nxt:\n            pairs.append((h.group(1), h.group(2), nxt[0].group(1), nxt[0].group(2)))'''\nassert s.count(old)==1\nopen(p,'w',encoding='utf-8').write(s.replace(old,new))\nprint('patched')\n\"; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-121-paralegal-letter-check.py > /dev/null 2>&1; .venv/bin/python -I -c \"\nimport json\no=json.load(open('artifacts/review-evidence/T-121-paralegal-letter-check.out.json'))\nfor k in ('lib09_oneline','sample_oneline','lib09_standard','sample_standard'):\n    v=o[k]; rows=v['rows']\n    print(k, {x:v[x] for x in v if x!='rows'}, 'rows', len(rows), 'verbatim', sum(r['quote_verbatim'] for r in rows), 'raw-match', sum(r['raw_record'] is not None for r in rows), 'notes', sum(r['note_bracketed_at_end'] for r in rows))\n    for r in rows:\n        if not r['quote_verbatim'] or r['raw_record'] is None: print('   ', r)\nprint(o['charges_block_lib09'])\n\"",
 "description": "Fix standard-pair parsing and rerun the letter verification"
}
````

### User / tool · 2026-11-02T11:20:14.065Z

**tool result**
````
patched
lib09_oneline {'entry_lines': 6, 'prefix_lines': 0} rows 6 verbatim 6 raw-match 6 notes 2
sample_oneline {'entry_lines': 9, 'prefix_lines': 0} rows 9 verbatim 9 raw-match 9 notes 0
lib09_standard {'entry_pairs': 6, 'prefix_lines': 0} rows 6 verbatim 6 raw-match 6 notes 2
sample_standard {'entry_pairs': 9, 'prefix_lines': 0} rows 9 verbatim 9 raw-match 9 notes 0
BILLED CHARGES

Quillmere Regional ED, March 3, 2026: $2,940.00
Source [Ex. __ / Bates __]: "ED charge: $2,940."
Cinder Valley Imaging, right shoulder MRI, May 5, 2026: $2,150.00
Source [Ex. __ / Bates __]: "MRI charge: $2,150."

Billed charges stated in these records: $5,090.00
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:20:19.770Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-123-paralegal-survey.py <<'EOF'\n\"\"\"T-123 survey: the accident-date flag wording on every library case and the sample, through the running server (HEAD, port 7893).\nRun: .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-survey.py  (writes T-123-paralegal-survey.out.json next to this file).\"\"\"\nimport importlib.util, json, os\nHERE = os.path.dirname(os.path.abspath(__file__))\n_s = importlib.util.spec_from_file_location(\"c\", os.path.join(HERE, \"T-120-123-paralegal-common.py\")); C = importlib.util.module_from_spec(_s); _s.loader.exec_module(C)\nACC = (\"accident_date_after_treatment\", \"accident_dates_differ\")\nst, lib = C.req(\"GET\", \"/api/library\")\nids = [x[\"id\"] for x in (lib if isinstance(lib, list) else lib.get(\"cases\", lib.get(\"items\", [])))]\nout = {\"library_ids\": ids, \"cases\": {}}\ntodo = [(\"sample\", None)] + [(i, i) for i in ids]\nfor name, lib_id in todo:\n    if lib_id is None:\n        tok = C.req(\"POST\", \"/api/cases\", {\"sample\": True})[1][\"token\"]\n    else:\n        tok = C.load_library(lib_id)\n    status = C.poll_ready(tok)\n    cs = C.case(tok)\n    acc = [{\"id\": f[\"id\"], \"category\": f.get(\"category\"), \"title\": f[\"title\"], \"explanation\": f.get(\"explanation\"),\n            \"record_nos\": f.get(\"record_nos\")} for f in cs[\"flags\"] if f.get(\"category\") in ACC]\n    out[\"cases\"][name] = {\"status\": status, \"accident_flags\": acc}\n    print(name, status, [(a[\"category\"], a[\"title\"]) for a in acc])\njson.dump(out, open(os.path.join(HERE, \"T-123-paralegal-survey.out.json\"), \"w\", encoding=\"utf-8\"), ensure_ascii=False, indent=1)\nprint(\"paperwork-wording hits:\", [n for n, c in out[\"cases\"].items() for a in c[\"accident_flags\"] if \"paperwork\" in (a[\"explanation\"] or \"\")])\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-123-paralegal-survey.py 2>&1 | tail -30",
 "description": "Survey accident-date flag wording on all library cases and the sample"
}
````

### User / tool · 2026-11-02T11:20:24.751Z

**tool result**
````
sample ready [('accident_date_after_treatment', 'Stated accident date is later than recorded treatment')]
case_lib01_er_only_then_gap ready []
case_lib02_slip_fall_prior_knee ready []
case_lib03_truck_rear_end_chiro ready []
case_lib04_dog_bite_scar_revision ready []
case_lib05_pedestrian_orif_hardware ready []
case_lib06_lop_billed_vs_adjusted ready []
case_lib07_parking_lot_fall_outside_records ready []
case_lib08_second_crash_mri_after ready []
case_lib09_spanish_interpreter_espalda ready []
case_lib10_eob_ub04_cms1500 ready []
case_lib11_priors_and_ledger ready [('accident_date_after_treatment', 'Stated accident date is later than recorded treatment')]
case_lib12_records_review_credibility ready []
case_lib13_cloned_notes_cross_provider ready []
case_lib14_handwritten_chiro_scans ready []
case_lib15_conclusory_letter_mist ready []
paperwork-wording hits: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:20:26.890Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\no=json.load(open('artifacts/review-evidence/T-123-paralegal-survey.out.json'))\nfor n in ('sample','case_lib11_priors_and_ledger'):\n    for a in o['cases'][n]['accident_flags']: print(n, json.dumps(a, ensure_ascii=False, indent=1))\n\"; .venv/bin/python -I -c \"print(open('/Users/arsis/zlayt-pm-project/evals/library/case_lib11_priors_and_ledger.txt',encoding='utf-8').read()[:1500])\"",
 "description": "Print the accident-date flag wording on sample and lib11 and the lib11 source"
}
````

### User / tool · 2026-11-02T11:20:27.010Z

**tool result**
````
sample {
 "id": "f_accident_date_after_treatment_1_2_7",
 "category": "accident_date_after_treatment",
 "title": "Stated accident date is later than recorded treatment",
 "explanation": "Stated accident date January 19, 2026 (“Date of accident per intake form: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Austin EMS run report; Central ER discharge summary). The records disagree; the tool does not choose between them.",
 "record_nos": null
}
case_lib11_priors_and_ledger {
 "id": "f_accident_date_after_treatment_1_4",
 "category": "accident_date_after_treatment",
 "title": "Stated accident date is later than recorded treatment",
 "explanation": "Stated accident date March 18, 2026 (“collision on 2026-03-18”) is later than the first recorded treatment, March 4, 2026 (Dr. Hesper Alderton, primary care). The records disagree; the tool does not choose between them.",
 "record_nos": null
}
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-03-04
Source: Dr. Hesper Alderton, primary care
Excerpt: "Annual visit. History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy. Problem list: hypertension, type 2 diabetes, chronic low back pain. Low back pain 3/10 today."

=== Record 2 ===
Date: 2026-03-18
Source: Ashgrove Fire-Rescue run report
Excerpt: "Passenger vehicle struck from behind. Pt states neck and low back pain 7/10. Ambulatory at scene. Transported to Wexcombe Memorial ED."

=== Record 3 ===
Date: 2026-03-18
Source: Wexcombe Memorial ED
Excerpt: "Dx: cervical strain, lumbar strain. X-ray cervical and lumbar spine negative for fracture. ED charge: $3,260."

=== Record 4 ===
Date: 2026-03-26
Source: Pellingham and Rook PLLC, correspondence (letter of protection)
Excerpt: "Letter of protection to Fennimoor Spine Clinic. This firm represents the client for injuries from a collision on 2026-03-18. We ask that you defer collection while the claim is pending. Please send complete records and an itemized statement."

=== Record 5 ===
Date: 2026-03-27
Source: Fennimoor Spine Clinic, new patient
Excerpt: "Patient referred by attorney. Neck pain 7/10, low back pain 7/10. Treating under a letter of protection. Plan: chiropractic care three times weekly."

=== Record 6 ===
Date: 3/27/26
Source: Fennimoor Spine Clinic, new patient intake form (OCR text)
Excerpt: "Date of injury: 3/l
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:20:31.656Z

**tool call — Bash**
````
{
 "command": "grep -n \"^from\\|^import\" app/backend/pipeline.py | head -20",
 "description": "Check pipeline imports for the in-process accident probe"
}
````

### User / tool · 2026-11-02T11:20:31.739Z

**tool result**
````
8:import argparse
9:import json
10:import sys
11:import time
12:from concurrent.futures import ThreadPoolExecutor
14:from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
16:from app.db import db as DB
17:from app.llm import audited as AU, provider as P
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:20:33.122Z

**tool call — Bash**
````
{
 "command": "sed -n 14,16p app/backend/pipeline.py | cut -c1-260",
 "description": "Read the full backend import line from pipeline"
}
````

### User / tool · 2026-11-02T11:20:33.206Z

**tool result**
````
from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
                         judges, language, split_llm, totals as TT, why as WHY)
from app.db import db as DB
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:20:41.650Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-123-paralegal-baseline.py <<'EOF'\n\"\"\"T-123 in-process baseline probe (code path only, no model): the accident-date conflict the pipeline builds\n(IN.ingest -> language.annotate -> CF.accident_date_conflicts, as pipeline.py:52-59 does) on SYNTHETIC texts.\nThe running server refuses pasted text in demo mode (api.py:288), so these are run in-process against the HEAD copy.\nRun: ARCH=<archive> .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-baseline.py\nEvery case is labelled SYNTHETIC in its own first line.\"\"\"\nimport json, os, sys\nARCH = os.environ[\"ARCH\"]\nsys.path.insert(0, ARCH)\nsys.dont_write_bytecode = True\nfrom app.backend import conflicts as CF, ingest as IN, language  # noqa: E402\n\nHDR = \"SYNTHETIC — invented for a review probe; not real patient data\\n\\n\"\ndef rec(n, date, source, excerpt):\n    return f'=== Record {n} ===\\nDate: {date}\\nSource: {source}\\nExcerpt: \"{excerpt}\"\\n\\n'\nVISIT_ER = (\"Central ER, discharge summary\", \"Dx: cervical strain. CT head negative. Follow up with PCP in 1 week.\")\nCASES = {\n    \"P1_same_day_paperwork_then_visit\": HDR + rec(1, \"2026-01-09\", \"Lakeside Clinic, intake form\", \"Reason for visit: neck pain after a car crash. Pain 6/10.\")\n        + rec(2, \"2026-01-09\", \"Lakeside Clinic, initial evaluation\", \"Cervical strain. Plan: physical therapy twice weekly.\")\n        + rec(3, \"2026-01-19\", \"Lakeside Clinic, follow-up\", \"Date of accident: 2026-01-19. Neck pain 5/10.\"),\n    \"P2_same_day_visit_then_paperwork\": HDR + rec(1, \"2026-01-09\", \"Lakeside Clinic, initial evaluation\", \"Cervical strain. Plan: physical therapy twice weekly.\")\n        + rec(2, \"2026-01-09\", \"Lakeside Clinic, intake form\", \"Reason for visit: neck pain after a car crash. Pain 6/10.\")\n        + rec(3, \"2026-01-19\", \"Lakeside Clinic, follow-up\", \"Date of accident: 2026-01-19. Neck pain 5/10.\"),\n    \"P3_bare_questionnaire_alone_on_first_date\": HDR + rec(1, \"2026-01-09\", \"Patient questionnaire\", \"Neck pain 6/10. Injured in a car crash.\")\n        + rec(2, \"2026-01-16\", \"Lakeside Clinic, initial evaluation\", \"Cervical strain. Plan: physical therapy twice weekly.\")\n        + rec(3, \"2026-01-19\", \"Lakeside Clinic, follow-up\", \"Date of accident: 2026-01-19. Neck pain 5/10.\"),\n    \"P4_authorization_request_alone_on_first_date\": HDR + rec(1, \"2026-01-09\", \"Authorization request\", \"Patient authorizes release of records. Injured in a car crash.\")\n        + rec(2, \"2026-01-16\", \"Lakeside Clinic, initial evaluation\", \"Cervical strain. Plan: physical therapy twice weekly.\")\n        + rec(3, \"2026-01-19\", \"Lakeside Clinic, follow-up\", \"Date of accident: 2026-01-19. Neck pain 5/10.\"),\n    \"P5_control_visits_only_no_paperwork\": HDR + rec(1, \"2026-01-09\", VISIT_ER[0], VISIT_ER[1])\n        + rec(2, \"2026-01-16\", \"Capital PT, visit 1\", \"Pain 6/10. Plan: physical therapy twice weekly.\")\n        + rec(3, \"2026-01-19\", \"Lakeside Clinic, follow-up\", \"Date of accident: 2026-01-19. Neck pain 5/10.\"),\n}\nout = {}\nfor name, text in CASES.items():\n    ing = IN.ingest(text)\n    recs = language.annotate(ing[\"records\"])\n    flags = CF.accident_date_conflicts(recs)\n    out[name] = [{\"category\": f[\"category\"], \"title\": f[\"title\"], \"explanation\": f[\"explanation\"], \"record_nos\": f[\"record_nos\"],\n                  \"first_treatment_date\": f[\"first_treatment_date\"]} for f in flags]\n    print(\"==\", name)\n    for f in flags:\n        print(\"  [\" + f[\"category\"] + \"] \" + f[\"title\"]); print(\"  \" + f[\"explanation\"])\n    if not flags:\n        print(\"  (no accident-date flag)\")\ndest = os.path.join(os.path.dirname(os.path.abspath(__file__)), \"T-123-paralegal-baseline.out.json\")\njson.dump(out, open(dest, \"w\", encoding=\"utf-8\"), ensure_ascii=False, indent=1)\nprint(\"wrote\", dest)\nEOF\nSCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-baseline.py 2>&1 | tail -60",
 "description": "Run the T-123 same-day paperwork probes in-process on HEAD"
}
````

### User / tool · 2026-11-02T11:20:41.878Z

**tool result**
````
== P1_same_day_paperwork_then_visit
  [accident_date_after_treatment] Stated accident date is later than the earliest record
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the earliest recorded date, January 9, 2026 (record 2: Lakeside Clinic, intake form), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 2: Lakeside Clinic, intake form is paperwork, not a visit, the first recorded visit is January 9, 2026 (record 3: Lakeside Clinic, initial evaluation), and the stated date is also later than it. Check when treatment actually began before relying on this comparison.
== P2_same_day_visit_then_paperwork
  [accident_date_after_treatment] Stated accident date is later than the earliest record
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the earliest recorded date, January 9, 2026 (record 3: Lakeside Clinic, intake form), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 3: Lakeside Clinic, intake form is paperwork, not a visit, the first recorded visit is January 9, 2026 (record 2: Lakeside Clinic, initial evaluation), and the stated date is also later than it. Check when treatment actually began before relying on this comparison.
== P3_bare_questionnaire_alone_on_first_date
  [accident_date_after_treatment] Stated accident date is later than the earliest record
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the earliest recorded date, January 9, 2026 (record 2: Patient questionnaire), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 2: Patient questionnaire is paperwork, not a visit, the first recorded visit is January 16, 2026 (record 3: Lakeside Clinic, initial evaluation), and the stated date is also later than it. Check when treatment actually began before relying on this comparison.
== P4_authorization_request_alone_on_first_date
  [accident_date_after_treatment] Stated accident date is later than the earliest record
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the earliest recorded date, January 9, 2026 (record 2: Authorization request), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 2: Authorization request is paperwork, not a visit, the first recorded visit is January 16, 2026 (record 3: Lakeside Clinic, initial evaluation), and the stated date is also later than it. Check when treatment actually began before relying on this comparison.
== P5_control_visits_only_no_paperwork
  [accident_date_after_treatment] Stated accident date is later than recorded treatment
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Central ER, discharge summary). The records disagree; the tool does not choose between them.
wrote /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-123-paralegal-baseline.out.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:20:50.409Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-123-paralegal-recnum.py <<'EOF'\n\"\"\"T-123 probe helper: how IN.ingest numbers the SYNTHETIC P1 text (the record numbers in the baseline sentence must match the paste).\"\"\"\nimport os, sys\nARCH = os.environ[\"ARCH\"]\nsys.path.insert(0, ARCH)\nsys.dont_write_bytecode = True\nfrom app.backend import ingest as IN, language  # noqa: E402\nHDR = \"SYNTHETIC — invented for a review probe; not real patient data\\n\\n\"\nt = HDR + ('=== Record 1 ===\\nDate: 2026-01-09\\nSource: Lakeside Clinic, intake form\\nExcerpt: \"Reason for visit: neck pain. Pain 6/10.\"\\n\\n'\n           '=== Record 2 ===\\nDate: 2026-01-09\\nSource: Lakeside Clinic, initial evaluation\\nExcerpt: \"Cervical strain. Plan: physical therapy twice weekly.\"\\n\\n')\nfor label, text in ((\"with SYNTHETIC preamble\", t), (\"without preamble\", t[len(HDR):])):\n    ing = IN.ingest(text)\n    print(label, [(r[\"n\"], r.get(\"date_iso\"), r[\"source\"]) for r in language.annotate(ing[\"records\"])])\nlib = open(os.path.join(ARCH, \"evals/library/case_lib09_spanish_interpreter_espalda.txt\"), encoding=\"utf-8\").read()\nprint(\"lib09 (library preamble)\", [(r[\"n\"], r[\"source\"][:30]) for r in IN.ingest(lib)[\"records\"]][:3])\nEOF\nSCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-recnum.py 2>&1 | tail -8",
 "description": "Check how ingest numbers records in the synthetic probe text"
}
````

### User / tool · 2026-11-02T11:20:50.679Z

**tool result**
````
with SYNTHETIC preamble [(1, None, ''), (2, '2026-01-09', 'Lakeside Clinic, intake form'), (3, '2026-01-09', 'Lakeside Clinic, initial evaluation')]
without preamble [(1, '2026-01-09', 'Lakeside Clinic, intake form'), (2, '2026-01-09', 'Lakeside Clinic, initial evaluation')]
lib09 (library preamble) [(1, 'Quillmere Regional ED'), (2, 'Consultorio Médico Aguaclara, '), (3, 'Dr. Lucan Ostrowe, orthopedics')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:21:00.721Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-123-paralegal-preamble.py <<'EOF'\n\"\"\"T-123 probe helper: does a SYNTHETIC preamble line before '=== Record 1 ===' create a phantom record 1 in IN.ingest (record numbering)?\nCompares three preamble wordings with the same single record. Run: ARCH=<archive> .venv/bin/python -I <this file>.\"\"\"\nimport os, sys\nARCH = os.environ[\"ARCH\"]\nsys.path.insert(0, ARCH)\nsys.dont_write_bytecode = True\nfrom app.backend import ingest as IN  # noqa: E402\nREC = '=== Record 1 ===\\nDate: 2026-01-09\\nSource: Lakeside Clinic, intake form\\nExcerpt: \"Reason for visit: neck pain. Pain 6/10.\"\\n\\n'\nfor pre in (\"SYNTHETIC — invented for evaluation; not real patient data\\n\\n\",\n            \"SYNTHETIC — invented for a review probe; not real patient data\\n\\n\",\n            \"SYNTHETIC — invented for evaluation; not real patient data\\n\", \"\"):\n    recs = IN.ingest(pre + REC)[\"records\"]\n    print(repr(pre[:40]), \"->\", [(r[\"n\"], r.get(\"source\")) for r in recs])\nEOF\nSCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-preamble.py 2>&1 | tail -6",
 "description": "Test which preamble wordings create a phantom record in ingest"
}
````

### User / tool · 2026-11-02T11:21:00.923Z

**tool result**
````
'SYNTHETIC — invented for evaluation; not' -> [(1, 'Lakeside Clinic, intake form')]
'SYNTHETIC — invented for a review probe;' -> [(1, ''), (2, 'Lakeside Clinic, intake form')]
'SYNTHETIC — invented for evaluation; not' -> [(1, 'Lakeside Clinic, intake form')]
'' -> [(1, 'Lakeside Clinic, intake form')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:21:09.088Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\np='artifacts/review-evidence/T-123-paralegal-baseline.py'\ns=open(p,encoding='utf-8').read()\nold='HDR = \\\"SYNTHETIC — invented for a review probe; not real patient data\\\\\\\\n\\\\\\\\n\\\"'\nprint(s.count(old))\ns=s.replace(old,'HDR = \\\"SYNTHETIC — invented for evaluation; not real patient data\\\\\\\\n\\\\\\\\n\\\"  # same wording as the library header: a different preamble makes ingest count a phantom record 1 (T-123-paralegal-preamble.py)')\ns=s.replace('Every case is labelled SYNTHETIC in its own first line.','Every case is labelled SYNTHETIC in its own first line (library wording; see T-123-paralegal-preamble.py for the phantom-record finding).')\nopen(p,'w',encoding='utf-8').write(s)\n\"; grep -n \"^HDR\" artifacts/review-evidence/T-123-paralegal-baseline.py",
 "description": "Switch the probe preamble to the library wording to keep record numbers aligned"
}
````

### User / tool · 2026-11-02T11:21:09.220Z

**tool result**
````
1
12:HDR = "SYNTHETIC — invented for evaluation; not real patient data\n\n"  # same wording as the library header: a different preamble makes ingest count a phantom record 1 (T-123-paralegal-preamble.py)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:21:12.587Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-baseline.py 2>&1 | tail -30",
 "description": "Rerun the T-123 baseline probes with aligned record numbers"
}
````

### User / tool · 2026-11-02T11:21:12.793Z

**tool result**
````
== P1_same_day_paperwork_then_visit
  [accident_date_after_treatment] Stated accident date is later than the earliest record
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the earliest recorded date, January 9, 2026 (record 1: Lakeside Clinic, intake form), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: Lakeside Clinic, intake form is paperwork, not a visit, the first recorded visit is January 9, 2026 (record 2: Lakeside Clinic, initial evaluation), and the stated date is also later than it. Check when treatment actually began before relying on this comparison.
== P2_same_day_visit_then_paperwork
  [accident_date_after_treatment] Stated accident date is later than the earliest record
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the earliest recorded date, January 9, 2026 (record 2: Lakeside Clinic, intake form), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 2: Lakeside Clinic, intake form is paperwork, not a visit, the first recorded visit is January 9, 2026 (record 1: Lakeside Clinic, initial evaluation), and the stated date is also later than it. Check when treatment actually began before relying on this comparison.
== P3_bare_questionnaire_alone_on_first_date
  [accident_date_after_treatment] Stated accident date is later than the earliest record
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the earliest recorded date, January 9, 2026 (record 1: Patient questionnaire), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: Patient questionnaire is paperwork, not a visit, the first recorded visit is January 16, 2026 (record 2: Lakeside Clinic, initial evaluation), and the stated date is also later than it. Check when treatment actually began before relying on this comparison.
== P4_authorization_request_alone_on_first_date
  [accident_date_after_treatment] Stated accident date is later than the earliest record
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the earliest recorded date, January 9, 2026 (record 1: Authorization request), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: Authorization request is paperwork, not a visit, the first recorded visit is January 16, 2026 (record 2: Lakeside Clinic, initial evaluation), and the stated date is also later than it. Check when treatment actually began before relying on this comparison.
== P5_control_visits_only_no_paperwork
  [accident_date_after_treatment] Stated accident date is later than recorded treatment
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Central ER, discharge summary). The records disagree; the tool does not choose between them.
wrote /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-123-paralegal-baseline.out.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:21:27.845Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$SCR/pre-t123-archive\" && git archive 0c47356^ | tar -x -C \"$SCR/pre-t123-archive\" && git log -1 --format='%h %s' 0c47356^ && cat > artifacts/review-evidence/T-123-paralegal-sample-compare.py <<'EOF'\n\"\"\"T-123 sample/library wording compare: the accident-date conflict on the sample and lib11 texts, in-process, built the way pipeline.py does.\nRun once per archive: ARCH=<archive> .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-sample-compare.py <label>\nPrints one JSON line per text so the pre-T-123 and HEAD outputs can be diffed.\"\"\"\nimport json, os, sys\nARCH = os.environ[\"ARCH\"]\nsys.path.insert(0, ARCH)\nsys.dont_write_bytecode = True\nfrom app.backend import conflicts as CF, ingest as IN, language  # noqa: E402\nlabel = sys.argv[1] if len(sys.argv) > 1 else \"run\"\ntexts = {\"sample\": open(os.path.join(ARCH, \"evals/golden/sample.txt\"), encoding=\"utf-8\").read(),\n         \"lib11\": open(os.path.join(ARCH, \"evals/library/case_lib11_priors_and_ledger.txt\"), encoding=\"utf-8\").read()}\nfor name, t in texts.items():\n    recs = language.annotate(IN.ingest(t)[\"records\"])\n    print(json.dumps({\"label\": label, \"text\": name, \"flags\": [{\"category\": f[\"category\"], \"title\": f[\"title\"], \"explanation\": f[\"explanation\"]} for f in CF.accident_date_conflicts(recs)]}, ensure_ascii=False))\nEOF\nARCH=\"$SCR/pre-t123-archive\" .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-sample-compare.py pre-T-123 > \"$SCR/t123-cmp-pre.jsonl\"; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-sample-compare.py HEAD > \"$SCR/t123-cmp-head.jsonl\"; .venv/bin/python -I -c \"\nimport json\na=[json.loads(l) for l in open('$SCR/t123-cmp-pre.jsonl')]\nb=[json.loads(l) for l in open('$SCR/t123-cmp-head.jsonl')]\nfor x,y in zip(a,b):\n    print(x['text'], 'flags equal:', x['flags']==y['flags'], 'count', len(x['flags']), len(y['flags']))\n    print('  ', y['flags'][0]['explanation'][:200] if y['flags'] else None)\n\"",
 "description": "Compare accident-date wording on sample and lib11 before and after T-123"
}
````

### User / tool · 2026-11-02T11:21:28.717Z

**tool result**
````
d56328a test(e2e): declare sort, copy-confirm, btn-copy-anyway in the hook contract (T-124)
sample flags equal: True count 1 1
   Stated accident date January 19, 2026 (“Date of accident per intake form: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Austin EMS run report; Central ER discharge summary)
lib11 flags equal: True count 1 1
   Stated accident date March 18, 2026 (“collision on 2026-03-18”) is later than the first recorded treatment, March 4, 2026 (Dr. Hesper Alderton, primary care). The records disagree; the tool does not c
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:21:33.980Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/pre-t123-archive\" .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-baseline.py 2>&1 | head -12",
 "description": "Run the same same-day probes against the pre-T-123 commit"
}
````

### User / tool · 2026-11-02T11:21:34.178Z

**tool result**
````
== P1_same_day_paperwork_then_visit
  [accident_date_after_treatment] Stated accident date is later than recorded treatment
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Lakeside Clinic, intake form; Lakeside Clinic, initial evaluation). The records disagree; the tool does not choose between them.
== P2_same_day_visit_then_paperwork
  [accident_date_after_treatment] Stated accident date is later than recorded treatment
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Lakeside Clinic, initial evaluation; Lakeside Clinic, intake form). The records disagree; the tool does not choose between them.
== P3_bare_questionnaire_alone_on_first_date
  [accident_date_after_treatment] Stated accident date is later than recorded treatment
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Patient questionnaire). The records disagree; the tool does not choose between them.
== P4_authorization_request_alone_on_first_date
  [accident_date_after_treatment] Stated accident date is later than recorded treatment
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Authorization request). The records disagree; the tool does not choose between them.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:21:39.696Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ARCH=\"$SCR/pre-t123-archive\" .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-baseline.py > artifacts/review-evidence/T-123-paralegal-baseline-pre-T123.txt 2>&1; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I artifacts/review-evidence/T-123-paralegal-baseline.py > artifacts/review-evidence/T-123-paralegal-baseline-HEAD.txt 2>&1; tail -2 artifacts/review-evidence/T-123-paralegal-baseline-HEAD.txt; head -3 artifacts/review-evidence/T-123-paralegal-baseline-pre-T123.txt | cut -c1-150",
 "description": "Save pre-T-123 and HEAD same-day probe outputs as evidence files"
}
````

### User / tool · 2026-11-02T11:21:40.060Z

**tool result**
````
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Central ER, discharge summary). The records disagree; the tool does not choose between them.
wrote /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-123-paralegal-baseline.out.json
== P1_same_day_paperwork_then_visit
  [accident_date_after_treatment] Stated accident date is later than recorded treatment
  Stated accident date January 19, 2026 (“Date of accident: 2026-01-19”) is later than the first recorded treatment, January 9, 2026 (Lakeside Cli
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:21:49.550Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; grep -rln \"oneline\\|style=\" \"$SCR/t120-123-archive/app/frontend\" | head; echo \"---- frontend export calls:\"; grep -rn \"/export\" \"$SCR/t120-123-archive/app/frontend\" | cut -c1-220 | head -8; echo ----; grep -rn \"AI translation\" \"$SCR/t120-123-archive/app/frontend\" | cut -c1-200 | head -5",
 "description": "Check whether the frontend exposes the oneline style or the translation note"
}
````

### User / tool · 2026-11-02T11:21:49.671Z

**tool result**
````
---- frontend export calls:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e7
----
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:21:53.112Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120-123-archive && echo \"style/oneline hits in frontend: $(grep -rl 'oneline' app/frontend | wc -l)\" && grep -rn \"api/cases/.*export\\|/export'\" app/frontend | cut -c1-200 | head -6; echo ----; grep -rln \"AI translation\" app/frontend | head -3",
 "description": "Search the frontend archive for export style and translation text"
}
````

### User / tool · 2026-11-02T11:21:53.225Z

**tool result**
````
style/oneline hits in frontend:        0
app/frontend/exportcfg.js:2:   GET/PUT/DELETE /api/cases/{token}/export_config; the panel stays hidden when the server answers 404. */
----
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:21:55.933Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t120-123-archive && grep -rln \"export\" app/frontend | head -12; echo ----; grep -rn \"export?\" app/frontend | cut -c1-200 | head -5; grep -rn \"'/export\\|\\\"/export\\|/export\\`\" app/frontend | cut -c1-200 | head -5",
 "description": "Locate the frontend export fetch calls"
}
````

### User / tool · 2026-11-02T11:21:56.046Z

**tool result**
````
app/frontend/review.css
app/frontend/mock_extra.js
app/frontend/index.html
app/frontend/review.js
app/frontend/export.js
app/frontend/styles.css
app/frontend/stepper.js
app/frontend/exportcfg.js
app/frontend/timeline.js
app/frontend/mock.js
app/frontend/judges.js
app/frontend/api.js
----
app/frontend/mock_extra.js:11:    if (sub === "/export_config") {
app/frontend/exportcfg.js:12:      const r = await RV.http("GET", "/cases/" + encodeURIComponent(token) + "/export_config");
app/frontend/exportcfg.js:31:      const r = await RV.http("PUT", "/cases/" + encodeURIComponent(c.token) + "/export_config", body);
app/frontend/exportcfg.js:41:          const r = await RV.http("DELETE", "/cases/" + encodeURIComponent(c.token) + "/export_config");
app/frontend/api.js:43:    exportCase: (token) => call("GET", t(token) + "/export"),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:03.229Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-121-paralegal-before-after.py <<'EOF'\n\"\"\"T-121 before/after: the lib09 standard letter with every entry and charge accepted, on the pre-T-121 parent (port 7894) and HEAD (7893).\nRun: ZLAYT_BASE=<base> .venv/bin/python -I artifacts/review-evidence/T-121-paralegal-before-after.py <label>\nPrints every line that carries the translation label, plus the total line.\"\"\"\nimport importlib.util, os, sys\nHERE = os.path.dirname(os.path.abspath(__file__))\n_s = importlib.util.spec_from_file_location(\"c\", os.path.join(HERE, \"T-120-123-paralegal-common.py\")); C = importlib.util.module_from_spec(_s); _s.loader.exec_module(C)\nlabel = sys.argv[1] if len(sys.argv) > 1 else \"run\"\ntok = C.load_library(\"case_lib09_spanish_interpreter_espalda\")\nprint(\"label:\", label, \"base:\", C.BASE, \"status:\", C.poll_ready(tok))\ncs = C.case(tok)\nids = [e[\"id\"] for e in cs[\"entries\"]] + [a[\"id\"] for a in cs[\"amounts\"] if a[\"kind\"] in (\"charge\", \"rate\")]\nprint(\"accept:\", sorted({C.req(\"POST\", f\"/api/cases/{tok}/items/{i}/review\", {\"action\": \"accept\"})[0] for i in ids}))\nst, ex = C.req(\"GET\", f\"/api/cases/{tok}/export\")\nprint(\"export status:\", st)\nif st == 200:\n    for ln in ex[\"letter_text\"].splitlines():\n        if \"AI translation\" in ln or ln.startswith(\"Billed charges\") or ln.startswith(\"AI translation\"):\n            print(\"LINE:\", ln)\nEOF\nZLAYT_BASE=http://127.0.0.1:7894 .venv/bin/python -I artifacts/review-evidence/T-121-paralegal-before-after.py parent-0c47356 2>&1 | cut -c1-260; echo =====; ZLAYT_BASE=http://127.0.0.1:7893 .venv/bin/python -I artifacts/review-evidence/T-121-paralegal-before-after.py HEAD-63e18ed 2>&1 | cut -c1-260",
 "description": "Compare the lib09 translation label before and after T-121"
}
````

### User / tool · 2026-11-02T11:22:04.175Z

**tool result**
````
label: parent-0c47356 base: http://127.0.0.1:7894 status: ready
accept: [200]
export status: 200
LINE: AI translation: Patient reports pain 6/10 that worsens when raising the arm. Denies loss of consciousness. Exam: pain on palpation of the right shoulder. Plan: physical therapy and follow-up in 4 weeks.
LINE: AI translation: Account statement: consultations $1,300.00; physical therapy, 4 sessions at $400.00 per session. Balance: $2,900.00.
LINE: Billed charges stated in these records: $5,090.00
=====
label: HEAD-63e18ed base: http://127.0.0.1:7893 status: ready
accept: [200]
export status: 200
LINE: Source [Ex. __ / Bates __]: "Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: dolor a la palpación del hombro derecho. Plan: fisioterapia y control en 4 semanas." [AI translation of the Spanish original
LINE: Source [Ex. __ / Bates __]: "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00." [AI translation of the Spanish original; check before sending]
LINE: Billed charges stated in these records: $5,090.00
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:13.081Z

**tool call — Bash**
````
{
 "command": "grep -rn \"lexicon_flags(\" app/backend/*.py | cut -c1-200 | head -5; echo ----; grep -n \"def lexicon_flags\" -A4 app/backend/flags.py | cut -c1-200",
 "description": "Confirm the pipeline calls the flag engine used in the regression probe"
}
````

### User / tool · 2026-11-02T11:22:13.193Z

**tool result**
````
app/backend/flags.py:80:def lexicon_flags(record: dict, accident_year=None) -> list:
app/backend/flags.py:249:    flags = merge(llm, lexicon_flags(record, accident_year), record, tagged, llm_failed=failed, fixture_miss=miss)
----
80:def lexicon_flags(record: dict, accident_year=None) -> list:
81-    """Flags from the phrase list alone: excerpt = the whole sentence unit that contains the hit; one flag per (unit, type)."""
82-    text = record["excerpt"]
83-    units = sentences.stripped_spans(text)
84-    seen, out = {}, []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:20.014Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$SCR/t120-123-archive\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit/test_t120_history_source_sentence.py tests/unit/test_t121_letter_styles.py tests/unit/test_t123_baseline_same_day_paperwork.py 2>&1 | tail -15",
 "description": "Run the three card unit test files on the HEAD archive copy"
}
````

### User / tool · 2026-11-02T11:22:21.281Z

**tool result**
````
................................................                         [100%]
48 passed in 0.90s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:22:52.956Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=artifacts/review-evidence; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I $R/T-120-paralegal-variants.py > $R/T-120-paralegal-variants-HEAD.txt 2>&1; ARCH=\"$SCR/t120-parent-archive\" .venv/bin/python -I $R/T-120-paralegal-variants.py > $R/T-120-paralegal-variants-parent.txt 2>&1; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I $R/T-120-paralegal-engine.py > $R/T-120-paralegal-engine-HEAD.txt 2>&1; ARCH=\"$SCR/t120-parent-archive\" .venv/bin/python -I $R/T-120-paralegal-engine.py > $R/T-120-paralegal-engine-parent.txt 2>&1; ZLAYT_BASE=http://127.0.0.1:7894 .venv/bin/python -I $R/T-120-paralegal-before-after.py parent-0c47356 > $R/T-120-paralegal-before-after-parent.txt 2>&1; ZLAYT_BASE=http://127.0.0.1:7893 .venv/bin/python -I $R/T-120-paralegal-before-after.py > $R/T-120-paralegal-before-after-HEAD.txt 2>&1; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I $R/T-121-paralegal-letter-check.py > $R/T-121-paralegal-letter-check.txt 2>&1; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I $R/T-123-paralegal-preamble.py > $R/T-123-paralegal-preamble.txt 2>&1; ls -la $R | grep \"T-12[013]-paralegal\" | awk '{print $5, $9}'; echo; cat $R/T-120-paralegal-engine-HEAD.txt; cat $R/T-120-paralegal-engine-parent.txt",
 "description": "Save the probe outputs as evidence files and list them"
}
````

### User / tool · 2026-11-02T11:22:55.474Z

**tool result**
````
185 T-120-paralegal-before-after-HEAD.txt
413 T-120-paralegal-before-after-parent.txt
1238 T-120-paralegal-before-after.py
700 T-120-paralegal-dbg.py
299 T-120-paralegal-engine-HEAD.txt
417 T-120-paralegal-engine-parent.txt
1239 T-120-paralegal-engine.py
1629 T-120-paralegal-explore.py
1335 T-120-paralegal-explore2.py
1424 T-120-paralegal-variants-HEAD.txt
1743 T-120-paralegal-variants-parent.txt
1574 T-120-paralegal-variants.py
1280 T-121-paralegal-before-after.py
6000 T-121-paralegal-letter-check.out.json
4312 T-121-paralegal-letter-check.py
6001 T-121-paralegal-letter-check.txt
3169 T-123-paralegal-baseline-HEAD.txt
1951 T-123-paralegal-baseline-pre-T123.txt
3794 T-123-paralegal-baseline.out.json
3875 T-123-paralegal-baseline.py
907 T-123-paralegal-preamble.py
311 T-123-paralegal-preamble.txt
1117 T-123-paralegal-recnum.py
1093 T-123-paralegal-sample-compare.py
3041 T-123-paralegal-survey.out.json
1658 T-123-paralegal-survey.py

lib09 records with the sentence: [1]
'Hx obtained via interpreter: lumbar strain 2019.' -> NO pre_existing flag
"PHx obtained via patient's son: lumbar strain 2019." -> NO pre_existing flag
"Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019." -> ['Hx of lumbar strain 2019.']
lib09 records with the sentence: [1]
'Hx obtained via interpreter: lumbar strain 2019.' -> ['Hx obtained via interpreter: lumbar strain 2019.']
"PHx obtained via patient's son: lumbar strain 2019." -> ["PHx obtained via patient's son: lumbar strain 2019."]
"Hx obtained via patient's son, who interpreted. Hx of lumbar strain 2019." -> ["Hx obtained via patient's son, who interpreted.", 'Hx of lumbar strain 2019.']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:23:01.226Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=artifacts/review-evidence; ZLAYT_BASE=http://127.0.0.1:7894 .venv/bin/python -I $R/T-121-paralegal-before-after.py parent-0c47356 > $R/T-121-paralegal-before-after-parent.txt 2>&1; ZLAYT_BASE=http://127.0.0.1:7893 .venv/bin/python -I $R/T-121-paralegal-before-after.py HEAD-63e18ed > $R/T-121-paralegal-before-after-HEAD.txt 2>&1; ARCH=\"$SCR/pre-t123-archive\" .venv/bin/python -I $R/T-123-paralegal-sample-compare.py pre-T-123 > $R/T-123-paralegal-sample-compare-pre.jsonl 2>&1; ARCH=\"$SCR/t120-123-archive\" .venv/bin/python -I $R/T-123-paralegal-sample-compare.py HEAD-63e18ed > $R/T-123-paralegal-sample-compare-HEAD.jsonl 2>&1; cat $R/T-121-paralegal-before-after-parent.txt | cut -c1-120; cat $R/T-123-paralegal-sample-compare-HEAD.jsonl | cut -c1-120; cat $R/T-123-paralegal-sample-compare-pre.jsonl | cut -c1-80",
 "description": "Save the T-121 before/after and T-123 sample compare outputs"
}
````

### User / tool · 2026-11-02T11:23:02.478Z

**tool result**
````
label: parent-0c47356 base: http://127.0.0.1:7894 status: ready
accept: [200]
export status: 200
LINE: AI translation: Patient reports pain 6/10 that worsens when raising the arm. Denies loss of consciousness. Exam: p
LINE: AI translation: Account statement: consultations $1,300.00; physical therapy, 4 sessions at $400.00 per session. B
LINE: Billed charges stated in these records: $5,090.00
{"label": "HEAD-63e18ed", "text": "sample", "flags": [{"category": "accident_date_after_treatment", "title": "Stated acc
{"label": "HEAD-63e18ed", "text": "lib11", "flags": [{"category": "accident_date_after_treatment", "title": "Stated acci
{"label": "pre-T-123", "text": "sample", "flags": [{"category": "accident_date_a
{"label": "pre-T-123", "text": "lib11", "flags": [{"category": "accident_date_af
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:23:09.151Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-123-paralegal-preamble.txt; echo ----; cat artifacts/review-evidence/T-123-paralegal-survey.out.json | .venv/bin/python -I -c \"import json,sys; d=json.load(sys.stdin); print(d['library_ids'][:3], len(d['cases']), sorted(d['cases'])[:2])\"; echo ----; git -C /Users/arsis/zlayt-pm-project status --short | head -20",
 "description": "Confirm preamble evidence and survey coverage, and check working tree status"
}
````

### User / tool · 2026-11-02T11:23:09.315Z

**tool result**
````
'SYNTHETIC — invented for evaluation; not' -> [(1, 'Lakeside Clinic, intake form')]
'SYNTHETIC — invented for a review probe;' -> [(1, ''), (2, 'Lakeside Clinic, intake form')]
'SYNTHETIC — invented for evaluation; not' -> [(1, 'Lakeside Clinic, intake form')]
'' -> [(1, 'Lakeside Clinic, intake form')]
----
['case_lib01_er_only_then_gap', 'case_lib02_slip_fall_prior_knee', 'case_lib03_truck_rear_end_chiro'] 16 ['case_lib01_er_only_then_gap', 'case_lib02_slip_fall_prior_knee']
----
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
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:23:27.786Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-120-paralegal-flags-diff.py <<'EOF'\n\"\"\"T-120 flag diff: every lib09 flag (id, type, category, title, evidence excerpt) on the parent (7894) and HEAD (7893).\nRun per server: ZLAYT_BASE=<base> .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-flags-diff.py <label>\"\"\"\nimport importlib.util, json, os, sys\nHERE = os.path.dirname(os.path.abspath(__file__))\n_s = importlib.util.spec_from_file_location(\"c\", os.path.join(HERE, \"T-120-123-paralegal-common.py\")); C = importlib.util.module_from_spec(_s); _s.loader.exec_module(C)\nlabel = sys.argv[1] if len(sys.argv) > 1 else \"run\"\ntok = C.load_library(\"case_lib09_spanish_interpreter_espalda\")\nC.poll_ready(tok)\ncs = C.case(tok)\nprint(\"label:\", label, \"base:\", C.BASE)\nfor f in cs[\"flags\"]:\n    ev = [e.get(\"excerpt\") for e in (f.get(\"evidence\") or [])]\n    print(json.dumps({\"id\": f[\"id\"], \"type\": f[\"type\"], \"category\": f.get(\"category\"), \"title\": f[\"title\"], \"evidence\": ev}, ensure_ascii=False))\nEOF\nZLAYT_BASE=http://127.0.0.1:7894 .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-flags-diff.py parent-0c47356 > artifacts/review-evidence/T-120-paralegal-flags-diff-parent.txt 2>&1; ZLAYT_BASE=http://127.0.0.1:7893 .venv/bin/python -I artifacts/review-evidence/T-120-paralegal-flags-diff.py HEAD-63e18ed > artifacts/review-evidence/T-120-paralegal-flags-diff-HEAD.txt 2>&1; cut -c1-330 artifacts/review-evidence/T-120-paralegal-flags-diff-parent.txt; echo =====; cut -c1-330 artifacts/review-evidence/T-120-paralegal-flags-diff-HEAD.txt",
 "description": "Diff every lib09 flag between the parent and HEAD builds"
}
````

### User / tool · 2026-11-02T11:23:28.827Z

**tool result**
````
label: parent-0c47356 base: http://127.0.0.1:7894
{"id": "f_gap_r1_r2", "type": "gap", "category": "gap_over_30", "title": "Gap of 42 days", "evidence": ["Date: 2026-03-03", "Source: Quillmere Regional ED", "Date: 14/04/2026", "Source: Consultorio Médico Aguaclara, nota de consulta"]}
{"id": "f_date_r4", "type": "record_warning", "category": "date_ambiguous", "title": "Date to confirm", "evidence": ["03/05/2026"]}
{"id": "f_r1_1", "type": "pre_existing", "category": "pre_existing", "title": "Mention of a prior or pre-existing condition", "evidence": ["Hx obtained via patient's son, who interpreted."]}
{"id": "f_r1_2", "type": "causation", "category": "patient_report", "title": "Reported onset", "evidence": ["Patient states she was struck by a car while walking in a parking lot."]}
{"id": "f_r2_1", "type": "causation", "category": "patient_report", "title": "Reported onset", "evidence": ["Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo."]}
{"id": "f_r3_1", "type": "causation", "category": "patient_report", "title": "Reported onset", "evidence": ["Patient states she fell in the parking lot after a car brushed her."]}
=====
label: HEAD-63e18ed base: http://127.0.0.1:7893
{"id": "f_gap_r1_r2", "type": "gap", "category": "gap_over_30", "title": "Gap of 42 days", "evidence": ["Date: 2026-03-03", "Source: Quillmere Regional ED", "Date: 14/04/2026", "Source: Consultorio Médico Aguaclara, nota de consulta"]}
{"id": "f_date_r4", "type": "record_warning", "category": "date_ambiguous", "title": "Date to confirm", "evidence": ["03/05/2026"]}
{"id": "f_r1_1", "type": "causation", "category": "patient_report", "title": "Reported onset", "evidence": ["Patient states she was struck by a car while walking in a parking lot."]}
{"id": "f_r2_1", "type": "causation", "category": "patient_report", "title": "Reported onset", "evidence": ["Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo."]}
{"id": "f_r3_1", "type": "causation", "category": "patient_report", "title": "Reported onset", "evidence": ["Patient states she fell in the parking lot after a car brushed her."]}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:02.667Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t120-123-patterns.md",
 "content": "---\nname: t120-123-patterns\ndescription: T-120/T-121/T-123 review (2026-11-02, HEAD 63e18ed): source-sentence skip hides a colon-joined real prior (blocker, regression vs 0c47356); demo-mode paste gate; ingest phantom record from non-library preamble\nmetadata:\n  type: project\n---\n\nT-120 (1cb8707, skip \"Hx obtained via ...\" prior hits): the lib09 sentence is in record 1, not record 2 as the card says. The skip drops the WHOLE lexicon hit, so a real prior after a colon is hidden: \"Hx obtained via interpreter: lumbar strain 2019.\" and \"PHx obtained via patient's son: lumbar strain 2019.\" raised a pre_existing flag on 0c47356 and raise none on HEAD. The 48 unit tests in test_t120/t121/t123 pass and do not cover the colon form.\n\n**Why:** the rule removes a guess (the source phrase is not a prior) by deleting the whole hit, one layer too wide. Same shape as T-116: removing one guess can silently delete a fact next to it.\n\n**How to apply:** on any lexicon skip or suppression change, run the same input on the parent commit and HEAD (git archive both, two ports), and diff the flag lists, not just the unit tests. Probe colon, semicolon and period joins. Engine-level check: flags.lexicon_flags(record) (flags.py:249 calls it per record) is enough when the paste route is refused.\n\nDemo-mode paste gate: POST /api/cases {\"text\": ...} returns 409 demo_mode_unsupported_input (api.py:288) for any text that is not an exact library or recorded case, even with ZLAYT_MODE=local. Synthetic same-day probes must run in-process: IN.ingest -> language.annotate -> CF.accident_date_conflicts (as pipeline.py:52-59 does). Library cases give no paperwork-on-earliest-date case, so the in-process probe is the only T-123 evidence.\n\nIngest phantom record: a preamble line that is not the library wording (\"SYNTHETIC — invented for a review probe; ...\") before \"=== Record 1 ===\" becomes an undated, empty-source record 1 (T-123-paralegal-preamble.txt), shifting every cited record number by one. Library wording does not. Not caused by T-123; minor. Check it on a real fax/cover-sheet preamble before calling it a blocker.\n\nT-121 (c26ff04): oneline and standard letters verified line by line against the raw record (scripts T-121-paralegal-letter-check.py; 6/6 lib09 and 9/9 sample per style). Translation note now sits on the Spanish Source line, not the English summary it describes; the one-line style has no English text at all. The UI has no style toggle (app/frontend/api.js:43 calls GET /export without a style). Open question for Chris: D-001 keeps notes out of the letter; the card puts the translation warning inside it by design.\n\nT-123 (0c47356): paperwork on the earliest date is named as paperwork in both orders and for bare questionnaire and authorization-request headers; visits-only control and sample/lib11 wording are unchanged vs d56328a (the parent, pre-T-123).\n\n**Card-citation slip:** card AC text names record numbers from memory (T-120 \"record 2\"). Check every record number on the raw file with `re.split` on \"=== Record N ===\" before accepting an AC citation.\n"
}
````

### User / tool · 2026-11-02T11:24:02.781Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/t120-123-patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:03.906Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T11:24:03.916Z

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
13	- [T-114 rates and gap patterns](t114-rates-gap-patterns.md) — r2 (e1ce8dc): gap notice is page-memory only, not on the gap card; rate row keeps Needs review chip; lib09 still 42 to 40
14	- [T-116 gap endpoint patterns](t116-gap-endpoint-patterns.md) — r3 fail; r4 fail (warning gated by text regex); r5 (f8f358e) changes: same-day and header-list gaps in baseline wording
15	- [T-118 lib11 truth patterns](t118-lib11-truth-patterns.md) — validators pass on the wrong truth; record lists unguarded; intake form as phone_note stand-in; stale library-latest.md
16	- [T-060 UI polish patterns](t060-ui-polish-patterns.md) — pass 2 open items; reuse q0-q13 scripts; recount severities before the single Write
17	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:05.856Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md",
 "old_string": "- [T-060 UI polish patterns](t060-ui-polish-patterns.md) — pass 2 open items; reuse q0-q13 scripts; recount severities before the single Write\n",
 "new_string": "- [T-060 UI polish patterns](t060-ui-polish-patterns.md) — pass 2 open items; reuse q0-q13 scripts; recount severities before the single Write\n- [T-120/121/123 patterns](t120-123-patterns.md) — source-sentence skip hides colon-joined real prior (blocker); demo paste gate forces in-process probes; preamble phantom record\n"
}
````

### User / tool · 2026-11-02T11:24:05.964Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/paralegal-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:22.861Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-paralegal-draft.md",
 "content": "# T-120 paralegal review\n\n**Verdict: fail.** One blocker. The fix for \"Hx obtained via ...\" also hides a real prior condition that the pre-T-120 build flags. Lib09 itself is clean.\n\nScope: T-120 at HEAD 63e18ed (git archive copy, fixture backend, ZLAYT_MODE=local, port 7893, listener PID 87376), compared with the parent build 0c47356 (port 7894, PID 95532). Cases: lib09, lib02, lib11, sample, plus engine-level probes of flags.lexicon_flags.\n\nWhat I checked:\n- lib09 on HEAD: no pre_existing flag (T-120-123-paralegal-probe.out.json, A_lib09_pre_existing_flags = []). The parent flags the sentence on record 1 (T-120-paralegal-before-after-parent.txt). The other lib09 flags are unchanged (T-120-paralegal-flags-diff-parent.txt vs -HEAD.txt; only the pre_existing flag is gone).\n- The card's \"record 2\" is wrong: the sentence is in record 1 of the library file and in app record r1 (A_raw_lib09_interpreter_sentence_in = [1]).\n- Real prior controls on HEAD: sample still flags record 3 \"Patient reports low back pain in 2023, resolved.\" and record 8 \"Findings may represent degenerative change\" (A_sample_pre_existing_flags). lib02 and lib11 still flag (A_lib02/lib11_pre_existing_flags).\n- Variants on the flag engine (T-120-paralegal-variants-HEAD.txt vs -parent.txt): \n  - \"Hx obtained via interpreter: lumbar strain 2019.\" raises nothing on HEAD; the parent flags the whole sentence.\n  - \"PHx obtained via patient's son: lumbar strain 2019.\" raises nothing on HEAD; the parent flags it.\n  - Period-joined variants still flag on HEAD.\n- Unit tests test_t120/t121/t123 on the HEAD copy: 48 passed. None of them uses the colon form, so the regression is not covered.\n\nFindings are in the JSON block.\n\n```json\n{\"card\": \"T-120\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"HEAD 63e18ed git archive copy on http://127.0.0.1:7893 (fixture, ZLAYT_MODE=local, listener PID 87376); parent 0c47356 on http://127.0.0.1:7894 (PID 95532); sample evals/golden/sample.txt; library case_lib09, case_lib02, case_lib11; engine probes via app.backend.flags.lexicon_flags and lexicon_scan.scan\",\n \"exercised\": [\n  \"read board show T-120, personas/paralegal.md, CLAUDE.md\",\n  \"pytest on tests/unit/test_t120_history_source_sentence.py, test_t121_letter_styles.py, test_t123_baseline_same_day_paperwork.py on the HEAD copy: 48 passed\",\n  \"HTTP on :7893 and :7894: POST /api/cases {library: case_lib09...}, poll status to ready, GET case flags (artifacts/review-evidence/T-120-paralegal-before-after-parent.txt, T-120-paralegal-flags-diff-parent.txt, T-120-paralegal-flags-diff-HEAD.txt)\",\n  \"HTTP on :7893: sample, lib02, lib11 pre_existing flags (artifacts/review-evidence/T-120-123-paralegal-probe.out.json)\",\n  \"in-process flags.lexicon_flags on lib09 record 1 with the excerpt replaced by 3 variants, HEAD and parent (T-120-paralegal-engine-HEAD.txt, T-120-paralegal-engine-parent.txt)\",\n  \"in-process lexicon_scan.scan on 11 variant texts, HEAD and parent (T-120-paralegal-variants-HEAD.txt, T-120-paralegal-variants-parent.txt)\",\n  \"raw record check of the library file: the sentence is in record 1 (A_raw_lib09_interpreter_sentence_in)\"],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 2, \"prior_mentions_flagged\": 2, \"interpreter_sentence_not_flagged\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"The skip drops the whole prior hit, so a real prior after a colon on a history-source line is no longer flagged (regression vs 0c47356)\",\n   \"evidence\": \"artifacts/review-evidence/T-120-paralegal-engine-HEAD.txt: 'Hx obtained via interpreter: lumbar strain 2019.' -> NO pre_existing flag; \\\"PHx obtained via patient's son: lumbar strain 2019.\\\" -> NO pre_existing flag. artifacts/review-evidence/T-120-paralegal-engine-parent.txt, same inputs: ['Hx obtained via interpreter: lumbar strain 2019.'] and [\\\"PHx obtained via patient's son: lumbar strain 2019.\\\"]. Same result in T-120-paralegal-variants-HEAD.txt vs -parent.txt.\",\n   \"why_it_matters\": \"Checklist 9 and card AC 1 (a real prior-condition mention still raises the flag) are broken for this shape. The record still says lumbar strain 2019, but the tool no longer surfaces it, which is the prior injury the adjuster will find and the paralegal missed. The fix removes a guess (a source phrase is not a prior) and deletes a fact next to it.\",\n   \"fix\": \"Drop only the source-phrase span (for example 'Hx obtained via interpreter') from the hit, and keep any lexicon match that extends past it, including after a colon or semicolon. Keep the current sentence-level behaviour for 'Hx obtained via ..., who interpreted. Hx of lumbar strain 2019.'.\",\n   \"acceptance_test\": \"Add both colon inputs above to REAL in tests/unit/test_t120_history_source_sentence.py and assert FL.lexicon_flags(record) returns a pre_existing flag for each. Re-run the T-120 probe: lib09 still has no pre_existing flag, and sample still flags record 3 and record 8. Re-run the parent-vs-HEAD variant probe and expect no row to lose a flag that the parent raised except the source-phrase-only row.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Card AC and test name cite lib09 'record 2' for the interpreter sentence; it is record 1\",\n   \"evidence\": \"board/cards/T-120.md AC 1 text: 'the interpreter-history sentence of record 2'; test name test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do; evals/library/case_lib09_spanish_interpreter_espalda.txt, '=== Record 1 ===' Excerpt starts 'Hx obtained via patient's son, who interpreted.'; record 2 (14/04/2026, Consultorio Médico Aguaclara) has no such sentence; A_raw_lib09_interpreter_sentence_in = [1].\",\n   \"why_it_matters\": \"Checklist 3 needs the record reference to point at the right source in one action. A paralegal who opens record 2 to check the AC will not find the sentence.\",\n   \"fix\": \"Change the AC text, the test name and the handoff to record 1 (app id r1).\",\n   \"acceptance_test\": \"grep of the AC and test name shows record 1; the lib09 record list in the case JSON shows the sentence under r1.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Flag ids are positional: f_r1_1 names a different flag on HEAD than on the parent\",\n   \"evidence\": \"artifacts/review-evidence/T-120-paralegal-flags-diff-parent.txt: id f_r1_1 = pre_existing (Hx sentence), f_r1_2 = causation 'Reported onset'. T-120-paralegal-flags-diff-HEAD.txt: id f_r1_1 = causation 'Reported onset'; f_r1_2 is gone.\",\n   \"why_it_matters\": \"If any saved decision is keyed by flag id, it could attach to a different flag after a re-run. I did not test whether decisions carry over, so this is a risk to check, not a loss I reproduced.\",\n   \"fix\": \"Derive flag ids from category and record so they survive a removed flag, or confirm that decisions are not keyed by id across builds.\",\n   \"acceptance_test\": \"A flag decision made on a case before a flag is removed still points at the same flag after a re-run on the new build.\"}\n ],\n \"whats_right\": [\n  \"lib09 on HEAD raises no pre_existing flag on the 'Hx obtained via patient's son, who interpreted.' sentence, and the gap (42 days), date-to-confirm and three patient-report flags are unchanged against the parent\",\n  \"the sample's two real prior mentions (record 3 'low back pain in 2023, resolved', record 8 'may represent degenerative change') still raise flags, with verbatim evidence\",\n  \"the period-joined 'Hx ... Hx of lumbar strain 2019.' and 'Hx ... Prior low back pain 2023, resolved.' forms still flag on HEAD\"],\n \"questions_for_chris\": [\n  \"On the live backend the model may also propose a prior-condition flag. Does the merge at flags.py:249 keep an LLM prior flag on the Hx sentence? The fixture set cannot show this; I only tested the lexicon path.\"]\n}\n```\n"
}
````

### User / tool · 2026-11-02T11:24:22.992Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-paralegal-draft.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:30.029Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-123-paralegal-jsoncheck.py",
 "content": "\"\"\"Pre-check a review draft before the single Write (stdlib only).\nRun: .venv/bin/python -I artifacts/review-evidence/T-120-123-paralegal-jsoncheck.py <draft.md>\nChecks: exactly one ```json fenced block; it parses; required keys present; persona and model strings; severities in the closed list;\nverdict rule (blocker -> fail, else major -> changes, else pass); scores.verify_quickly present in 1..5 for app reviews; max 3 whats_right.\"\"\"\nimport json\nimport re\nimport sys\n\npath = sys.argv[1]\ntext = open(path, encoding=\"utf-8\").read()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", text, flags=re.S)\nproblems = []\nif len(blocks) != 1:\n    problems.append(f\"expected exactly one ```json block, found {len(blocks)}\")\nd = None\nif blocks:\n    try:\n        d = json.loads(blocks[0])\n    except ValueError as e:\n        problems.append(f\"json parse error: {e}\")\nif d is not None:\n    for k in (\"card\", \"persona\", \"model\", \"scope\", \"exercised\", \"verdict\", \"scores\", \"findings\", \"whats_right\", \"questions_for_chris\"):\n        if k not in d:\n            problems.append(f\"missing key {k}\")\n    if d.get(\"persona\") != \"paralegal-reviewer\":\n        problems.append(\"persona must be paralegal-reviewer\")\n    if d.get(\"model\") != \"claude-haiku-5-5\":\n        problems.append(\"model must be claude-haiku-5-5\")\n    sev = [f.get(\"severity\") for f in d.get(\"findings\", [])]\n    for s in sev:\n        if s not in (\"blocker\", \"major\", \"minor\", \"nit\"):\n            problems.append(f\"bad severity {s}\")\n    want = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\n    if d.get(\"verdict\") != want:\n        problems.append(f\"verdict {d.get('verdict')} but the rule gives {want}\")\n    vq = (d.get(\"scores\") or {}).get(\"verify_quickly\")\n    if vq is None or not (isinstance(vq, int) and 1 <= vq <= 5):\n        problems.append(\"scores.verify_quickly missing or outside 1..5\")\n    if len(d.get(\"whats_right\", [])) > 3:\n        problems.append(\"whats_right has more than 3 items\")\n    for f in d.get(\"findings\", []):\n        for k in (\"severity\", \"title\", \"evidence\", \"why_it_matters\", \"fix\", \"acceptance_test\"):\n            if not f.get(k):\n                problems.append(f\"finding missing {k}: {f.get('title', '?')[:50]}\")\n    counts = {s: sev.count(s) for s in (\"blocker\", \"major\", \"minor\", \"nit\")}\n    print(\"counts:\", counts, \"verdict:\", d.get(\"verdict\"), \"rule gives:\", want)\nprint(\"problems:\", problems or \"none\")\nsys.exit(1 if problems else 0)\n"
}
````

### User / tool · 2026-11-02T11:24:30.129Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-123-paralegal-jsoncheck.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:31.635Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-120-123-paralegal-jsoncheck.py artifacts/review-evidence/T-120-paralegal-draft.md; echo \"exit $?\"",
 "description": "Pre-check the T-120 review draft JSON with the checker script"
}
````

### User / tool · 2026-11-02T11:24:31.741Z

**tool result**
````
counts: {'blocker': 1, 'major': 0, 'minor': 1, 'nit': 1} verdict: fail rule gives: fail
problems: none
exit 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:36.263Z

**tool call — Bash**
````
{
 "command": "ls board/cards/T-120.md board/cards/T-121.md board/cards/T-123.md && ls reviews | grep -c \"T-12[013]-paralegal\" ; ls reviews | grep \"T-12[013]\" | head",
 "description": "Confirm card files exist and no existing paralegal reviews for these cards"
}
````

### User / tool · 2026-11-02T11:24:36.375Z

**tool result**
````
board/cards/T-120.md
board/cards/T-121.md
board/cards/T-123.md
0
T-120-staff-engineer.md
T-121-staff-engineer.md
T-123-staff-engineer.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:47.881Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-120-paralegal.md",
 "content": "# T-120 paralegal review\n\n**Verdict: fail.** One blocker. The fix for \"Hx obtained via ...\" also hides a real prior condition that the pre-T-120 build flags. Lib09 itself is clean.\n\nScope: T-120 at HEAD 63e18ed (git archive copy, fixture backend, ZLAYT_MODE=local, port 7893, listener PID 87376), compared with the parent build 0c47356 (port 7894, PID 95532). Cases: lib09, lib02, lib11, sample, plus engine-level probes of flags.lexicon_flags.\n\nWhat I checked:\n- lib09 on HEAD: no pre_existing flag (T-120-123-paralegal-probe.out.json, A_lib09_pre_existing_flags = []). The parent flags the sentence on record 1 (T-120-paralegal-before-after-parent.txt). The other lib09 flags are unchanged (T-120-paralegal-flags-diff-parent.txt vs -HEAD.txt; only the pre_existing flag is gone).\n- The card's \"record 2\" is wrong: the sentence is in record 1 of the library file and in app record r1 (A_raw_lib09_interpreter_sentence_in = [1]).\n- Real prior controls on HEAD: sample still flags record 3 \"Patient reports low back pain in 2023, resolved.\" and record 8 \"Findings may represent degenerative change\" (A_sample_pre_existing_flags). lib02 and lib11 still flag (A_lib02_pre_existing_flags, A_lib11_pre_existing_flags).\n- Variants on the flag engine (T-120-paralegal-variants-HEAD.txt vs -parent.txt):\n  - \"Hx obtained via interpreter: lumbar strain 2019.\" raises nothing on HEAD; the parent flags the whole sentence.\n  - \"PHx obtained via patient's son: lumbar strain 2019.\" raises nothing on HEAD; the parent flags it.\n  - Period-joined variants still flag on HEAD.\n- Unit tests test_t120, test_t121 and test_t123 on the HEAD copy: 48 passed. None of them uses the colon form, so the regression is not covered.\n\nShip-bar score (verify_quickly 2): the lib09 entries verify quickly, but the prior-condition list cannot be trusted as complete until the colon case is fixed. A reviewer who relies on the flag list would miss the prior.\n\nFindings are in the JSON block.\n\n```json\n{\"card\": \"T-120\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"HEAD 63e18ed git archive copy on http://127.0.0.1:7893 (fixture, ZLAYT_MODE=local, listener PID 87376); parent 0c47356 on http://127.0.0.1:7894 (PID 95532); sample evals/golden/sample.txt; library case_lib09, case_lib02, case_lib11; engine probes via app.backend.flags.lexicon_flags and lexicon_scan.scan\",\n \"exercised\": [\n  \"read board show T-120, personas/paralegal.md, CLAUDE.md\",\n  \"pytest on tests/unit/test_t120_history_source_sentence.py, test_t121_letter_styles.py, test_t123_baseline_same_day_paperwork.py on the HEAD copy: 48 passed\",\n  \"HTTP on :7893 and :7894: POST /api/cases {library: case_lib09...}, poll status to ready, GET case flags (artifacts/review-evidence/T-120-paralegal-before-after-parent.txt, T-120-paralegal-flags-diff-parent.txt, T-120-paralegal-flags-diff-HEAD.txt)\",\n  \"HTTP on :7893: sample, lib02, lib11 pre_existing flags (artifacts/review-evidence/T-120-123-paralegal-probe.out.json)\",\n  \"in-process flags.lexicon_flags on lib09 record 1 with the excerpt replaced by 3 variants, HEAD and parent (T-120-paralegal-engine-HEAD.txt, T-120-paralegal-engine-parent.txt)\",\n  \"in-process lexicon_scan.scan on 11 variant texts, HEAD and parent (T-120-paralegal-variants-HEAD.txt, T-120-paralegal-variants-parent.txt)\",\n  \"raw record check of the library file: the sentence is in record 1 (A_raw_lib09_interpreter_sentence_in)\"],\n \"verdict\": \"fail\",\n \"scores\": {\"verify_quickly\": 2, \"prior_mentions_flagged\": 2, \"interpreter_sentence_not_flagged\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"The skip drops the whole prior hit, so a real prior after a colon on a history-source line is no longer flagged (regression vs 0c47356)\",\n   \"evidence\": \"artifacts/review-evidence/T-120-paralegal-engine-HEAD.txt: 'Hx obtained via interpreter: lumbar strain 2019.' -> NO pre_existing flag; \\\"PHx obtained via patient's son: lumbar strain 2019.\\\" -> NO pre_existing flag. artifacts/review-evidence/T-120-paralegal-engine-parent.txt, same inputs: ['Hx obtained via interpreter: lumbar strain 2019.'] and [\\\"PHx obtained via patient's son: lumbar strain 2019.\\\"]. Same result in T-120-paralegal-variants-HEAD.txt vs -parent.txt.\",\n   \"why_it_matters\": \"Checklist 9 and card AC 1 (a real prior-condition mention still raises the flag) are broken for this shape. The record still says lumbar strain 2019, but the tool no longer surfaces it, which is the prior injury the adjuster will find and the paralegal missed. The fix removes a guess (a source phrase is not a prior) and deletes a fact next to it.\",\n   \"fix\": \"Drop only the source-phrase span (for example 'Hx obtained via interpreter') from the hit, and keep any lexicon match that extends past it, including after a colon or semicolon. Keep the current sentence-level behaviour for 'Hx obtained via ..., who interpreted. Hx of lumbar strain 2019.'.\",\n   \"acceptance_test\": \"Add both colon inputs above to REAL in tests/unit/test_t120_history_source_sentence.py and assert FL.lexicon_flags(record) returns a pre_existing flag for each. Re-run the T-120 probe: lib09 still has no pre_existing flag, and sample still flags record 3 and record 8. Re-run the parent-vs-HEAD variant probe and expect no row to lose a flag that the parent raised except the source-phrase-only row.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Card AC and test name cite lib09 'record 2' for the interpreter sentence; it is record 1\",\n   \"evidence\": \"board/cards/T-120.md AC 1 text: 'the interpreter-history sentence of record 2'; test name test_lib09_record_2_raises_no_prior_condition_flag_and_other_prior_mentions_still_do; evals/library/case_lib09_spanish_interpreter_espalda.txt, '=== Record 1 ===' Excerpt starts 'Hx obtained via patient's son, who interpreted.'; record 2 (14/04/2026, Consultorio Médico Aguaclara) has no such sentence; A_raw_lib09_interpreter_sentence_in = [1].\",\n   \"why_it_matters\": \"Checklist 3 needs the record reference to point at the right source in one action. A paralegal who opens record 2 to check the AC will not find the sentence.\",\n   \"fix\": \"Change the AC text, the test name and the handoff to record 1 (app id r1).\",\n   \"acceptance_test\": \"grep of the AC and test name shows record 1; the lib09 record list in the case JSON shows the sentence under r1.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Flag ids are positional: f_r1_1 names a different flag on HEAD than on the parent\",\n   \"evidence\": \"artifacts/review-evidence/T-120-paralegal-flags-diff-parent.txt: id f_r1_1 = pre_existing (Hx sentence), f_r1_2 = causation 'Reported onset'. T-120-paralegal-flags-diff-HEAD.txt: id f_r1_1 = causation 'Reported onset'; f_r1_2 is gone.\",\n   \"why_it_matters\": \"If any saved decision is keyed by flag id, it could attach to a different flag after a re-run. I did not test whether decisions carry over, so this is a risk to check, not a loss I reproduced.\",\n   \"fix\": \"Derive flag ids from category and record so they survive a removed flag, or confirm that decisions are not keyed by id across builds.\",\n   \"acceptance_test\": \"A flag decision made on a case before a flag is removed still points at the same flag after a re-run on the new build.\"}\n ],\n \"whats_right\": [\n  \"lib09 on HEAD raises no pre_existing flag on the 'Hx obtained via patient's son, who interpreted.' sentence, and the gap (42 days), date-to-confirm and three patient-report flags are unchanged against the parent\",\n  \"the sample's two real prior mentions (record 3 'low back pain in 2023, resolved', record 8 'may represent degenerative change') still raise flags, with verbatim evidence\",\n  \"the period-joined 'Hx ... Hx of lumbar strain 2019.' and 'Hx ... Prior low back pain 2023, resolved.' forms still flag on HEAD\"],\n \"questions_for_chris\": [\n  \"On the live backend the model may also propose a prior-condition flag. Does the merge at flags.py:249 keep an LLM prior flag on the Hx sentence? The fixture set cannot show this; I only tested the lexicon path.\"]\n}\n```\n"
}
````

### User / tool · 2026-11-02T11:24:48.088Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-120-paralegal.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:24:50.205Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-120-123-paralegal-jsoncheck.py reviews/T-120-paralegal.md; echo \"exit $?\"; python3 tools/board.py validate reviews/T-120-paralegal.md 2>&1 | tail -3",
 "description": "Check the T-120 review JSON and run the board validator on it"
}
````

### User / tool · 2026-11-02T11:24:50.365Z

**tool result**
````
counts: {'blocker': 1, 'major': 0, 'minor': 1, 'nit': 1} verdict: fail rule gives: fail
problems: none
exit 0
ok (1 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:25:10.248Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-121-paralegal.md",
 "content": "# T-121 paralegal review\n\n**Verdict: pass.** No blockers or majors. Every entry line in both styles matches its raw record: long date, provider as written, verbatim quote, citation placeholder. The \"AI translation:\" prefix is gone from the summary lines. Two minors: where the translation note sits, and the one-line form is not reachable from the screen.\n\nScope: T-121 at HEAD 63e18ed (git archive copy, fixture backend, ZLAYT_MODE=local, port 7893, listener PID 87376), compared with the parent build 0c47356 (port 7894, PID 95532). Cases: lib09 (Spanish, interpreter) and the sample (golden).\n\nWhat I checked:\n- lib09: accepted the 6 entries, 2 charges and 2 rates through the live review route (all 200). Standard and one-line exports both 200 (T-120-123-paralegal-probe.out.json, B_lib09_*).\n- Each entry line verified against the raw record text (T-121-paralegal-letter-check.out.json): lib09 6/6 in standard and 6/6 in one-line; sample 9/9 in both. The date is the raw record date in long format, the provider equals the raw Source label, the quote is a verbatim substring of the raw excerpt.\n- Translation label before and after: the parent prints \"LINE: AI translation: Patient reports pain 6/10 that worsens when raising the arm...\" and \"LINE: AI translation: Account statement: ...\" (T-121-paralegal-before-after-parent.txt). HEAD prints neither; the note sits at the end of the Source line (T-121-paralegal-before-after-HEAD.txt). Billed total $5,090.00 on both builds; the unclear amounts stay out.\n- Sample: accepted all 9 entries and the amounts. The standard letter equals the LETTER_TEXT block of evals/golden/sample.export.expected.txt (exact match). One-line export is 9 lines, one per entry, with the same two charges.\n- ?style=Oneline and ?style=bogus both return 422 invalid_style.\n- Frontend: app/frontend/api.js:43 calls GET /export with no style, and `grep -rl oneline app/frontend` returns no file, so the screen cannot request the one-line form.\n\nShip-bar score (verify_quickly 4): each entry line carries its date, provider, verbatim quote and citation placeholder, so I could check a line in one read. Spanish lines are slower because the English summary and the Spanish quote are not paired and the note sits next to the quote.\n\n```json\n{\"card\": \"T-121\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"HEAD 63e18ed git archive copy on http://127.0.0.1:7893 (fixture, ZLAYT_MODE=local, listener PID 87376); parent 0c47356 on http://127.0.0.1:7894 (PID 95532); library case_lib09; sample evals/golden/sample.txt; app/frontend/api.js\",\n \"exercised\": [\n  \"read board show T-121, personas/paralegal.md, CLAUDE.md\",\n  \"pytest on tests/unit/test_t121_letter_styles.py (with test_t120 and test_t123, 48 passed on the HEAD copy)\",\n  \"HTTP on :7893: POST /api/cases {library: case_lib09...}, run, poll ready; POST /items/{id}/review accept on 6 entries, 2 charges and 2 rates (all 200); GET /export and GET /export?style=oneline (both 200); GET ?style=Oneline and ?style=bogus (422 invalid_style)\",\n  \"HTTP on :7893: sample accepted, standard letter compared with the golden LETTER_TEXT block (exact match), one-line export (9 lines)\",\n  \"HTTP on :7894: the same lib09 accept and standard export on the parent build (T-121-paralegal-before-after-parent.txt)\",\n  \"letter verification script: every entry line in both styles against the raw library/sample text (T-121-paralegal-letter-check.txt and .out.json)\",\n  \"grep of app/frontend for oneline and style (0 hits); api.js:43 exportCase\"],\n \"verdict\": \"pass\",\n \"scores\": {\"verify_quickly\": 4, \"verbatim_quotes\": 5, \"translation_note_placement\": 3},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"The translation note sits on the Spanish quote line, not on the English summary it describes; in one-line style the line has no English text\",\n   \"evidence\": \"artifacts/review-evidence/T-121-paralegal-before-after-HEAD.txt: 'LINE: Source [Ex. __ / Bates __]: \\\"Refiere dolor 6/10 que empeora al levantar el brazo. ...\\\" [AI translation of the Spanish original; check before sending]'. One-line export (artifacts/review-evidence/T-120-123-paralegal-probe.out.json, B_lib09_oneline_letter): 'April 14, 2026 — Consultorio Médico Aguaclara, nota de consulta: \\\"Refiere dolor 6/10 ...\\\" [Ex. __ / Bates __] [AI translation of the Spanish original; check before sending]'.\",\n   \"why_it_matters\": \"The thing to check is the English summary line above, and it carries no marker. The warning reads as a comment on the Spanish original, which is not a translation. In one-line style nothing on the line is translated, so the note describes text the line does not have. A paralegal who deletes the note by mistake leaves an unmarked AI summary.\",\n   \"fix\": \"In standard style put the marker on the summary line that holds the AI translation. In one-line style print the note only when the line carries translated text, or move it to the internal notes (see question 1).\",\n   \"acceptance_test\": \"lib09 standard export: the bracketed phrase is on the same line as the AI-translated summary of each Spanish entry. lib09 one-line export: no bracketed claim on a line that holds only the Spanish quote, or the question-1 decision is recorded.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The one-line style cannot be reached from the app; the screen always gets the standard letter\",\n   \"evidence\": \"app/frontend/api.js:43: exportCase: (token) => call(\\\"GET\\\", t(token) + \\\"/export\\\"). grep -rl oneline app/frontend: 0 files. The card handoff says a style toggle is left to frontend.\",\n   \"why_it_matters\": \"The goal is an export she can paste with minimal reformatting. The one-line form exists only through a direct GET with ?style=oneline, so the paralegal cannot choose it on the screen. The card's AC is API-level, so this is a gap for the next card rather than a failure of T-121.\",\n   \"fix\": \"Add a style control to the export panel that calls /export?style=oneline and shows the returned letter_text unchanged.\",\n   \"acceptance_test\": \"In the app, choosing the one-line option shows letter_text byte-equal to GET /export?style=oneline for lib09 and sample.\"}\n ],\n \"whats_right\": [\n  \"every entry line in both styles verifies against the raw record: lib09 6/6 and sample 9/9, date, provider as written, verbatim quote (T-121-paralegal-letter-check.out.json)\",\n  \"the 'AI translation:' prefix is gone from the summary lines (the parent prints it twice on lib09); the billed total stays $5,090.00 with the unclear amounts out\",\n  \"the sample standard letter equals the golden LETTER_TEXT block exactly, and invalid style values return 422 invalid_style\"],\n \"questions_for_chris\": [\n  \"Decision needed: D-001 keeps notes out of the letter body. The translation warning sits inside the letter by design (card AC 2 and the pass-2 F9 request asked for a bracketed, removable phrase). Keep it in the letter, or move it to the internal notes and keep only the translated summary in the letter?\",\n  \"For Spanish entries the one-line form carries only the Spanish quote, with no English. Is a Spanish-only quote acceptable in a demand to an English-speaking adjuster, or should the one-line form carry the English summary too?\"]\n}\n```\n"
}
````

### User / tool · 2026-11-02T11:25:10.414Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-121-paralegal.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:25:13.523Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-120-123-paralegal-jsoncheck.py reviews/T-121-paralegal.md; echo \"exit $?\"; python3 tools/board.py validate reviews/T-121-paralegal.md 2>&1 | tail -3; grep -c \"AI translation: Patient\" artifacts/review-evidence/T-121-paralegal-before-after-parent.txt; grep -c \"AI translation\" artifacts/review-evidence/T-121-paralegal-before-after-HEAD.txt",
 "description": "Check the T-121 review JSON, validate it, and recount the translation lines"
}
````

### User / tool · 2026-11-02T11:25:13.733Z

**tool result**
````
counts: {'blocker': 0, 'major': 0, 'minor': 2, 'nit': 0} verdict: pass rule gives: pass
problems: none
exit 0
ok (1 file(s))
1
2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:25:17.024Z

**tool call — Bash**
````
{
 "command": "grep -c \"LINE: AI translation:\" artifacts/review-evidence/T-121-paralegal-before-after-parent.txt; grep -c \"LINE: AI translation:\" artifacts/review-evidence/T-121-paralegal-before-after-HEAD.txt; grep -o \"LINE: Source [^:]*: \\\"Refiere[^\\\"]*\\\" \\[AI[^]]*\\]\" artifacts/review-evidence/T-121-paralegal-before-after-HEAD.txt | cut -c1-80",
 "description": "Recount the translation-prefix lines in the before and after outputs"
}
````

### User / tool · 2026-11-02T11:25:17.142Z

**tool result**
````
2
0
LINE: Source [Ex. __ / Bates __]: "Refiere dolor 6/10 que empeora al levantar el
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:25:35.326Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-123-paralegal.md",
 "content": "# T-123 paralegal review\n\n**Verdict: pass.** No blockers or majors. A same-day paperwork record or a bare questionnaire or authorization header is now named as paperwork in the accident-date flag, in both record orders. The visits-only control keeps its old wording. The conflict is still not resolved by the tool. One minor, found while probing, is not from this change: a non-library preamble line makes ingest count a phantom record 1, which shifts every record number.\n\nScope: T-123 at HEAD 63e18ed (git archive copy, fixture backend, port 7893, listener PID 87376). The pre-T-123 build is 0c47356^ (d56328a), extracted to the scratchpad and run in-process. The live server refuses synthetic pastes in demo mode, so the synthetic probes ran in-process through the same functions the pipeline calls.\n\nWhat I checked:\n- Library and sample through the live server: 16 cases (sample plus 15 library), accident-date flags only on the sample and lib11, and neither has paperwork on the earliest date (T-123-paralegal-survey.out.json). So the library gives no paperwork-branch case, and the synthetic probes are the only evidence for it.\n- Same-day probes, labelled SYNTHETIC, run through IN.ingest, language.annotate and CF.accident_date_conflicts (T-123-paralegal-baseline-HEAD.txt and -pre-T123.txt):\n  - P1, intake form then initial evaluation on 2026-01-09: HEAD names record 1 (intake form) as paperwork and gives record 2 as the first visit. Pre-T-123 said \"first recorded treatment, January 9, 2026 (Lakeside Clinic, intake form; Lakeside Clinic, initial evaluation)\".\n  - P2, the same two records in reverse order: HEAD names record 2 as paperwork and record 1 as the first visit.\n  - P3, a bare \"Patient questionnaire\" alone on 2026-01-09: named as paperwork; first visit on 2026-01-16.\n  - P4, a bare \"Authorization request\" alone on 2026-01-09: named as paperwork; first visit on 2026-01-16.\n  - P5, visits only: the old wording, \"later than the first recorded treatment, January 9, 2026 (Central ER, discharge summary)\".\n- Sample and lib11 accident sentences are identical before and after (T-123-paralegal-sample-compare-pre.jsonl vs -HEAD.jsonl).\n- Unit tests test_t123, test_t120 and test_t121 on the HEAD copy: 48 passed.\n\nShip-bar score (verify_quickly 4): each paperwork sentence names the record number, the date and the alternative visit, so I could check it against the record in one read. The phantom-record minor lowers my confidence in the numbers on any paste with a preamble.\n\n```json\n{\"card\": \"T-123\", \"persona\": \"paralegal-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"HEAD 63e18ed git archive copy on http://127.0.0.1:7893 (fixture, ZLAYT_MODE=local, listener PID 87376); pre-T-123 0c47356^ (d56328a) extracted and run in-process; library cases and sample via the live server; SYNTHETIC probes in-process through app.backend.ingest, language.annotate and conflicts.accident_date_conflicts\",\n \"exercised\": [\n  \"read board show T-123, personas/paralegal.md, CLAUDE.md\",\n  \"pytest on tests/unit/test_t123_baseline_same_day_paperwork.py, test_t120 and test_t121 on the HEAD copy: 48 passed\",\n  \"HTTP on :7893: GET /api/library, POST /api/cases for the sample and all 15 library cases, poll to ready, read accident-date flags (artifacts/review-evidence/T-123-paralegal-survey.out.json)\",\n  \"in-process baseline probes P1 to P5 on HEAD and on d56328a (artifacts/review-evidence/T-123-paralegal-baseline-HEAD.txt, T-123-paralegal-baseline-pre-T123.txt, T-123-paralegal-baseline.out.json)\",\n  \"in-process sample and lib11 accident sentence, HEAD and d56328a (artifacts/review-evidence/T-123-paralegal-sample-compare-HEAD.jsonl, -pre.jsonl)\",\n  \"record numbering probe with three preamble wordings (artifacts/review-evidence/T-123-paralegal-preamble.txt)\",\n  \"a POST /api/cases with pasted text returned 409 demo_mode_unsupported_input on :7893 (api.py:288), which is why the synthetic probes are in-process\"],\n \"verdict\": \"pass\",\n \"scores\": {\"verify_quickly\": 4, \"accident_baseline_wording\": 5},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Outside T-123's change, pre-existing: a preamble line that is not the library wording makes ingest count a phantom record 1\",\n   \"evidence\": \"artifacts/review-evidence/T-123-paralegal-preamble.txt: 'SYNTHETIC — invented for a review probe;' -> [(1, ''), (2, 'Lakeside Clinic, intake form')]; the same record with the library wording 'SYNTHETIC — invented for evaluation; not' -> [(1, 'Lakeside Clinic, intake form')]; with no preamble -> [(1, 'Lakeside Clinic, intake form')].\",\n   \"why_it_matters\": \"Every record number the paralegal cites, and every flag that names a record, shifts by one when the paste starts with a header line that is not the library wording. Checklist 3 needs the citation to open the right record in one action. I did not test real fax or cover-sheet text, so the reach of this is unknown.\",\n   \"fix\": \"Text before the first '=== Record' header, or a block with no Date and no Source, is not a record. Numbering starts at the first real record.\",\n   \"acceptance_test\": \"Three preamble wordings (library header, free text, fax cover sheet) each give the first real record number 1, with no undated empty-source record, and the flag record numbers in the T-123 probe match the pasted headers.\"}\n ],\n \"whats_right\": [\n  \"a same-day intake form is named as paperwork in both record orders (P1, P2), and a bare questionnaire or authorization request alone on the first date is named as paperwork (P3, P4); pre-T-123 called the same records the first recorded treatment\",\n  \"the visits-only control keeps its old wording, and the sample and lib11 accident sentences are identical before and after\",\n  \"the tool does not choose between the two dates: 'The records disagree; the tool does not choose between them.' and 'Check when treatment actually began before relying on this comparison.'\"],\n \"questions_for_chris\": [\n  \"In local mode with the fixture backend, a paste that is not a library or recorded case is refused (409 demo_mode_unsupported_input, api.py:288). So the paralegal can only run the sample and the 15 library cases without ENABLE_LIVE. Is that intended for the local build?\"]\n}\n```\n"
}
````

### User / tool · 2026-11-02T11:25:35.475Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-123-paralegal.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:25:39.253Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-120-123-paralegal-jsoncheck.py reviews/T-123-paralegal.md; echo \"exit $?\"; python3 tools/board.py validate reviews/T-123-paralegal.md 2>&1 | tail -3; git rev-parse --short 0c47356^; grep -c \"\" artifacts/review-evidence/T-123-paralegal-preamble.txt",
 "description": "Check the T-123 review JSON, validate it, and confirm the pre-T-123 parent hash"
}
````

### User / tool · 2026-11-02T11:25:39.479Z

**tool result**
````
counts: {'blocker': 0, 'major': 0, 'minor': 1, 'nit': 0} verdict: pass rule gives: pass
problems: none
exit 0
ok (1 file(s))
d56328a
4
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:25:42.428Z

**tool call — Bash**
````
{
 "command": "lsof -iTCP:7893 -sTCP:LISTEN -nP | tail -1; lsof -iTCP:7894 -sTCP:LISTEN -nP | tail -1",
 "description": "Confirm the listener PIDs on ports 7893 and 7894 before stopping"
}
````

### User / tool · 2026-11-02T11:25:42.714Z

**tool result**
````
Python  87376 arsis    9u  IPv4 0x20fbaf4774bcbc05      0t0  TCP 127.0.0.1:7893 (LISTEN)
Python  95532 arsis    9u  IPv4 0xaa25b7f7479ddec0      0t0  TCP 127.0.0.1:7894 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:25:44.417Z

**tool call — Bash**
````
{
 "command": "kill 87376 95532; sleep 2; echo \"after kill:\"; lsof -iTCP:7893 -sTCP:LISTEN -nP; lsof -iTCP:7894 -sTCP:LISTEN -nP; curl -s -o /dev/null -w \"7893 %{http_code}\\n\" --max-time 3 http://127.0.0.1:7893/; curl -s -o /dev/null -w \"7894 %{http_code}\\n\" --max-time 3 http://127.0.0.1:7894/",
 "description": "Stop the review servers by PID and confirm the ports are closed"
}
````

### User / tool · 2026-11-02T11:25:46.720Z

**tool result (error)**
````
Exit code 7
after kill:
7893 000
7894 000
````

### Assistant · claude-haiku-5-5 · 2026-11-02T11:25:52.140Z

T-120 fails on one blocker: the "Hx obtained via ..." skip also hides a real prior after a colon ("PHx obtained via patient's son: lumbar strain 2019." raised a flag on 0c47356 and raises none on HEAD), and the 48 unit tests don't cover that form. T-121 passes with two minors (translation note sits on the Spanish quote line, one-line style not reachable from the UI), and T-123 passes with one minor found outside its change (a non-library preamble makes ingest count a phantom record 1).
Files: /Users/arsis/zlayt-pm-project/reviews/T-120-paralegal.md, /Users/arsis/zlayt-pm-project/reviews/T-121-paralegal.md, /Users/arsis/zlayt-pm-project/reviews/T-123-paralegal.md (all three pass `board.py validate`); evidence under /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-120-123-paralegal-*.
Server on :7893 (PID 87376) and the parent-build server on :7894 (PID 95532) are both stopped and the ports are closed; the T-120 card's "record 2" citation is wrong (record 1).
