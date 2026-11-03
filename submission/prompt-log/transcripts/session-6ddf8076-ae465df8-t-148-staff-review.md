# Subagent: T-148 staff review (T-148 staff review)

Source: `agent-ae465df85673c3e7a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T13:34:02.420Z

Review board card T-148 (commit d19ae46, `GET /api/cases` summary list) in /Users/arsis/zlayt-pm-project. Read `python3 tools/board.py show T-148` and memory/contracts/api.md.

On a `git archive HEAD` copy:
- **Drift.** Each field is computed by the same code as GET case, /status, the gate and /export, so nothing can drift; tests/unit/test_case_list.py compares them. Confirm the comparison would catch a drift by mutating one side.
- **HITL call-outs.** They are complete and honest: needs review, edits to check, the could-not-verify tray, and gate blockers and warnings with plain reasons.
- **Local mode.** It is local mode only, with non-loopback peers refused per D-036.
- **Performance.** There are no LLM calls. Check performance with 50 cases.
- **Old fields.** They are still present for the current UI.

Run the unit suite. Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-148-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings, exercised. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:34:04.159Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T13:34:04.167Z

**tool result**
````
1	# Persona dossier — staff-engineer-reviewer
2	
3	## 1. Identity
4	**Marcus Lee (fictional), Staff Software Engineer — 14 years, backend and data pipelines; the last 3 on LLM features in a regulated domain.**
5	He has been paged for a "flaky" pipeline that turned out to be an unpinned model plus a silent retry that swapped outputs, and for a total that was wrong because a regex caught a phone number. He reviews for correctness, determinism, and honest failure, because he will be the one debugging it.
6	
7	## 2. Day-to-day context
8	- Tools: git diff, pytest, coverage, the eval runner, logs, a REPL.
9	- Pressures: small team, no QA department; LLM behaviour drifts with model versions.
10	- A bad day: a bug reaches a customer and nobody can reproduce it because the LLM call, prompt version, and inputs were not recorded.
11	
12	## 3. Goals and success criteria for this artifact
13	- Deterministic work is code with unit tests; LLM work is behind schema validation, a grounding check, and a judge, as `docs/LLM_VS_CODE.md` says.
14	- Failures are visible: no swallowed exceptions, no silent fallbacks, no unbounded retries.
15	- Tests fail when the code breaks and pass reproducibly.
16	
17	## 4. Review checklist
18	1. The implementation matches the `docs/LLM_VS_CODE.md` table row by row for the files in scope; any divergence is a finding.
19	2. Date parsing, gap arithmetic, currency extraction, totals, sorting, dedupe, and export filtering contain no LLM call.
20	3. Gap logic has unit tests at 29, 30, and 31 days and uses date objects, not string math; the sample's 28-day interval does not flag and the 73-day one does.
21	4. The grounding verifier checks each excerpt is a substring of its own record after documented whitespace normalization, and each amount appears in the text; failures set a state, never auto-correct.
22	5. Totals sum only amounts classified `charge`; a per-visit rate ($185) is never multiplied by a visit count the records do not state.
23	6. Money is handled as integer cents or `Decimal`, never float.
24	7. LLM output is parsed and validated against a schema (Pydantic/JSON Schema); a validation failure produces a visible state, not a default value.
25	8. Every LLM call has a timeout; retries are capped (≤ 2), change conditions, and are logged; no retry loop hides a failure.
26	9. Model ids and prompt versions are config, pinned, and recorded in the audit record for every item.
27	10. Generator and judge prompts are separate files; the judge sees only the record and the candidate output.
28	11. The LLM provider sits behind one interface; tests use the fixture backend and never hit the network.
29	12. No bare `except:` or `except Exception: pass`; errors propagate to an explicit status the UI can show.
30	13. Tests assert behaviour (outputs, states), not implementation details; at least one test fails if the grounding check is removed.
31	14. No test depends on wall-clock time, random order, or a live service; time is injected or frozen.
32	15. Export assembly is a pure function of accepted items; an E2E or unit test proves dismissed items never export.
33	16. Input size is bounded before any LLM call; oversized input fails fast with a clear error.
34	17. Currency extraction has unit tests on the sample's non-charge numbers: "10 mg", "35 mph", "7/10", "approx. 40%", "missing 3 days of work" yield no amount; "$6,240" and "$2,150" parse to 624000 and 215000 cents; "Charge per visit $185" is classified as a rate, not a charge.
35	18. Prompt, model, lexicon or schema changes in the diff come with a re-run eval report path.
36	19. Same-day records (EMS and ER, both 2026-01-09) remain two entries after sort and dedupe: the dedupe key includes source/provider and excerpt, not date alone; a test pastes record 2 twice and asserts one duplicate is detected and the ER charge is counted once.
37	20. The CLI `python -m app.pipeline evals/golden/sample.txt` runs and its output matches the eval expectations.
38	
39	## 5. Red flags / dealbreakers
40	Each item here is a **blocker** (rate it so; never major or minor).
41	- A silent fallback (e.g., on judge error, mark item `verified`).
42	- An LLM computes a date difference, a total, or decides what is exported.
43	- Float arithmetic on money; a total that includes the $185 rate.
44	- Tests that call the real API or pass even when the verifier is stubbed out.
45	- Secrets or `.env` contents in code, fixtures, or logs.
46	
47	## 6. Vocabulary
48	determinism, idempotent, pure function, golden test, fixture, flaky test, quarantine, test double, contract test, schema validation, structured output, timeout, capped retry, backoff with jitter, silent fallback, swallowed exception, blast radius, audit trail, prompt version, pinned model.
49	
50	## 7. How I review
51	1. Read the card AC and `docs/LLM_VS_CODE.md`; then `git diff <range>` in full — every line in scope.
52	2. Run `pytest tests/unit -q` and the eval command from the brief; record pass/fail counts.
53	3. Mutation spot-check: comment out the grounding check or gap comparison locally (do not commit) and confirm a test fails; report if none does.
54	4. Run the pipeline CLI on the sample case twice; diff outputs for determinism.
55	5. Grep for `except`, `float(`, `sleep(`, `retry`, model-id strings, and network calls in tests.
56	6. File findings with file:line and the command that reproduces them.
57	
58	## 8. Calibration
59	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
60	- **blocker — Silent fallback marks unverified items verified.** Evidence: `app/backend/judge.py:88` returns `"supported"` on `TimeoutError`. Fix: return `needs_review` with reason "judge unavailable". Test: fixture backend raising timeout yields `needs_review`.
61	- **major — Gap test misses the boundary.** Evidence: `tests/unit/test_gaps.py` covers 28 and 73 days only. Fix: add 29/30/31 cases asserting flag only when > 30.
62	- **blocker — Money as float (red flag: float arithmetic on money).** Evidence: `charges.py:41 total += float(amt)`. Fix: parse to `Decimal` or integer cents.
63	
64	## 9. Sources
65	- https://google.github.io/eng-practices/review/reviewer/looking-for.html — Google eng-practices: review design, functionality, complexity, tests, naming, comments, docs; read every line in scope.
66	- https://martinfowler.com/articles/nonDeterminism.html — Fowler (2011): quarantine flaky tests, never bare sleeps, test doubles for remote services, wrap the clock.
67	- https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter — AWS Builders' Library: timeouts on every remote call, capped retries at one layer, jitter, idempotency before retrying.
68	- https://www.anthropic.com/engineering/building-effective-agents — Anthropic (Dec 2024): simplest solution first; predefined workflows for well-defined tasks; evaluator-optimizer pattern needs clear criteria.
69	- docs/CONTRACT.md §5.2 — the binding LLM/code table and validation ladder this reviewer enforces.
70	- Assumption: Decimal/integer-cents money handling is standard practice; no single source cited.
71	
72	## 10. Limits
73	Do not judge UX copy, clinical meaning, legal strategy, or the product note's prose. Security depth (injection, secrets, rate limits) belongs to security-reviewer; flag obvious issues and defer.
74	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:34:04.508Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-148; git log --oneline -3; git status --short | head"
}
````

### User / tool · 2026-11-02T13:34:04.708Z

**tool result**
````
---
id: "T-148"
title: "Multi-case API (Chris inbox 13:23Z): GET /api/cases summary list - per case title, created, run stage, progress (decided/total by kind), HITL call-outs (needs review, edits to check, could-not-verify tray, gate blockers/warnings with plain reasons), export ready"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T13:25:02Z"
updated_at: "2026-11-02T13:33:58Z"
claimed_by: "backend"
claimed_at: "2026-11-02T13:25:14Z"
rounds: 0
commits: ["d19ae46"]
reviews: []
ac:
  - {"n": 1, "text": "GET /api/cases returns every case the local profile can see, each with the summary fields, computed by the same code as GET case/gate (no drift: a test compares); local mode only, no auth/multi-user (scope cut kept); api.md", "done": true, "evidence": "tests/unit/test_case_list.py (7 tests): every summary field compared with GET case, /status, /trace export_gate and /export for all 15 library cases; full unit suite 3791 passed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:25:05Z orchestrator: assigned: backend
- 2026-11-02T13:25:14Z backend: claimed
- 2026-11-02T13:33:50Z backend: AC 1 checked: tests/unit/test_case_list.py (7 tests): every summary field compared with GET case, /status, /trace export_gate and /export for all 15 library cases; full unit suite 3791 passed
- 2026-11-02T13:33:51Z backend: moved in_progress -> in_review
- 2026-11-02T13:33:58Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: app/backend/case_list.py (new) builds GET /api/cases summaries (title, created/updated/last_activity, run stage, decided/total per kind, hitl needs_review/edits_to_check/could_not_verify/gate blockers+warnings, export_ready); api.py: route calls it, /status uses its run_progress (3 lines); api.md section. How verified: tests/unit/test_case_list.py vs GET case, /status, /trace, /export for all library cases (incl. an edit-to-check case and an export-ready case); full unit suite 3791 passed, 1 skipped. Cost: ~60 ms for 15 cases, no LLM, no pipeline. What's left: present.case_list is now dead code (present.py had staged hunks from others, left alone); old fields name/status/source/record_count/counts/created_at kept for the existing UI. Surprised me: GET /api/cases already existed as a thin list; commit d19ae46 via temp index.

d19ae46 feat(backend): GET /api/cases summary list for the case overview (T-148)
5de16d3 docs(orchestrator): scope cut 13e T-132 quote edge cases
ed45b4a fix(backend): T-132 r5 extension stops only at caps labels, closed section/vitals list, bullets
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:34:05.128Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"cases\" memory/contracts/api.md | head -40"
}
````

### User / tool · 2026-11-02T13:34:05.213Z

**tool result**
````
18:| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
19:| GET | `/api/cases/{token}` | the whole case for the review screen |
20:| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
21:| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
22:| GET | `/api/cases/{token}/status` | stage and progress |
23:| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
24:| GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |
25:| POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |
26:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an unlocatable quote is a hard `422 invalid_edit` with `detail.reason` and `detail.tokens`/`detail.qualifiers`, no override; a judge objection saves the entry as `pending`/`needs_review` with a `warnings[]` code, no 409); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
27:| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
28:| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
29:| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
30:| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
31:| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
32:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/verbatim/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending "Edit the summary to match the quote." (a summary check) or "Change the quote to whole sentences of the record that keep the hedge sentence." (a quote check), `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}` (`EDIT_QUOTE` when the first failing check is on the quote: `GROUNDING_EXCERPT_NOT_VERBATIM`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`); the judge verdict does not matter. **T-098 r3: the same guard runs on every action that leaves an entry accepted or edited, from one function (`review.set_review`):** `accept`, `edit` (which implies accept, including a summary-only edit and a quote edit; the check runs on the wording the edit would leave, before any write, so a summary-only edit cannot clear a failing quote and never wipes a stored quote-level reason) and batch accept. `reset` and `dismiss` leave the item out of the letter and are never blocked |
33:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
34:| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
35:| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
36:| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `ns…` |
37:| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
38:| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
39:| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconciled rows, skipped records (an EOB service row is a line); no sums or comparisons of any kind, no provider totals or complete flag; internal view, never in the letter |
40:| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
56:`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every view and `ai_banner` on the review view; in live mode it also shows "Pasted text is deleted after `retention_hours` hours" with a Delete now button.
58:## POST /api/cases
63:Request text is normalised first (CRLF and CR become LF; leading/trailing whitespace trimmed). **In demo mode the text is accepted only if its sha256 is in the recorded set (the sample and the golden cases); otherwise `409 demo_mode_unsupported_input` is returned before anything is stored** (D-020). Response 201 (all code: records, dates, duplicates, amounts, gap flags exist before any model call):
76:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`. **Both fields are on every record of `POST /api/cases` and `GET /api/cases/{token}`** (`false` for a real record); the `UNSPLIT_TEXT` warning is in the POST response only. A re-run after a record number came to name different text resets the paralegal's decisions on items that cite it to `pending` (the review event keeps what they were) and removes the stale items), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
78:## POST /api/cases/pdf (D-031)
79:Request: the raw PDF bytes with `Content-Type: application/pdf`; optional query `name`. Text layer only (pure-python extractor, no OCR); at most 5 MB and 100 pages. The extracted text becomes the case text (pages joined by a blank line), so everything after this is identical to a pasted case, and the demo gate (`409 demo_mode_unsupported_input`) applies to the extracted text. Response 201: same body as `POST /api/cases` with `source: "paste"`, and every record carries `page` (the page where it starts). `GET /api/cases/{token}` records carry `page` too, and export citations read `Source [Ex. __ / Bates __], p. N: "..."` for PDF cases only (unchanged for pasted text).
83:Query on `POST /api/cases/pdf`: `include_hidden` = `all` or a page list such as `2,5` (pages whose hidden text the paralegal confirmed; default none) and `ocr=true` (read scanned pages with local Tesseract; default off). Both are decided by re-posting the same file, which creates a new case (ingest is code only, so it costs no model call). Limits: OCR reads at most 10 scanned pages per upload, 150 s in all, nothing leaves the server. A page larger than 40 inches on a side is refused (`ocr_page_too_large`, `detail.page`); a larger one under that is rendered smaller than 150 dpi (longest side at most 3500 px, area at most 8 million px); all page images of one upload together are capped at 12 MB (`ocr_images_too_large`). Tesseract runs with a scrubbed environment (no API key or token reaches it). One deadline (10 s, or 165 s with OCR) covers text reading, the hidden-text scan and OCR; when it passes the work stops and the response is `400 bad_request` with `detail.reason: "pdf_timeout"`.
88:Response and `GET /api/cases/{token}` gain, for PDF cases only:
104:**`GET /api/cases/{token}/pages/{n}/image`** -> `image/png` (greyscale, 150 dpi) of an OCR'd page, stored with the case and deleted with it; `404 not_found` for a page that has none. The UI shows it beside the page's text.
106:## POST /api/cases/{token}/review/batch (D-031)
110:## /api/cases/{token}/export_config (D-031)
113:## POST /api/cases/{token}/run
120:## GET /api/cases/{token}/status
130:## GET /api/cases/{token}
261:## POST /api/cases/{token}/records/{rid}/confirm_date
280:**T-114: `gap_changes[]`** (always present; `[]` when no gap figure moved). Each element `{flag_id, change: "changed" | "added" | "removed", old_days, new_days, old_from, old_to, new_from, new_to, sentence}`; the side that does not exist is `null`. A gap whose endpoints moved (its id is built from its record numbers) is ONE `changed` element pairing the old and the new gap that share a record. `sentence` is plain words the UI can announce as is, e.g. "Gap recalculated after you confirmed record 4: now 40 days (was 42)." Computed by code from the stored gap figures, never by a model. A gap whose review status was reset by the recompute is exactly the set of `changed`/`added` elements. Each element also has `record_seq` (the record whose date was confirmed). **T-127: the change is kept with the case.** `confirm_date` writes `gap_changes[]` into its `confirm_date` review event (`after.gap_changes`), and `GET /api/cases/{token}` reads it back: a gap flag in `flags[]` whose figures were moved by a confirm_date has `gap_change` (the same element: `{flag_id, change, old_days, new_days, old_from, old_to, new_from, new_to, record_seq, sentence}`), otherwise `gap_change: null`; it stays through reload, another browser and review actions, and goes when that gap's current figures differ from the ones the change produced (a later confirm_date that moves it again replaces it). A gap that no longer applies has no flag, so `GET case` lists it in top-level `gap_changes_removed[]` (same element, `change: "removed"`, `sentence` included) until a gap with the same id exists again. Both are always present (`null` / `[]`). Stored in the DB (the audit event), not in `computed`. `422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event whose `after` records the chosen date (`date_chosen`, `date_raw`, `candidates`, `record_id`) and the ids whose `DATE_AMBIGUOUS` reason it cleared. Confirming also removes `DATE_AMBIGUOUS` from the entry's `reasons` and recomputes its `state` (it becomes `verified` unless another reason remains), so the entry reads like any other dated entry and can be reviewed normally. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
283:Every entry of `dates_to_confirm` (in `GET /api/cases/{token}` and in the `confirm_date` response) now has a `suggestion`: `null`, or a hint for an **ambiguous** numeric date. Code only (`app/backend/date_convention.py`). It looks at the other numeric dates in the packet whose order is certain (one number above 12: `03/14/2026` is month first, `14/03/2026` is day first), in each record's date label and text. It suggests only when all of that evidence agrees; no evidence, or evidence in both orders, gives `null`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:34:08.787Z

**tool call — Bash**
````
{
 "command": "git show --stat d19ae46 | head -20; git rev-parse HEAD; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/t148r1/head && git archive HEAD | tar -x -C $S/t148r1/head && ls $S/t148r1/head | head -30; ls -la .venv/bin/python"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:34:09.108Z

**tool call — Bash**
````
{
 "command": "git show d19ae46 -- app/backend/case_list.py app/backend/api.py | head -500"
}
````

### User / tool · 2026-11-02T13:34:09.403Z

**tool result**
````
commit d19ae46e0f39a256b359a84ac1283cafb2427d47
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:33:44 2026 -0600

    feat(backend): GET /api/cases summary list for the case overview (T-148)
    
    Per case: readable title, created/updated, run stage, decided/total per kind, HITL call-outs
    (needs review, edits to check, could-not-verify tray, gate blockers and warnings), export_ready.
    Computed from the functions GET case, /status and the export gate use; test compares all of them for every library case.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/api.py           |   7 +-
 app/backend/case_list.py     |  83 +++++++++++++++++++++++
 memory/contracts/api.md      |  13 +++-
 tests/unit/test_case_list.py | 156 +++++++++++++++++++++++++++++++++++++++++++
 4 files changed, 254 insertions(+), 5 deletions(-)
d19ae46e0f39a256b359a84ac1283cafb2427d47
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
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
````

### User / tool · 2026-11-02T13:34:09.485Z

**tool result**
````
commit d19ae46e0f39a256b359a84ac1283cafb2427d47
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:33:44 2026 -0600

    feat(backend): GET /api/cases summary list for the case overview (T-148)
    
    Per case: readable title, created/updated, run stage, decided/total per kind, HITL call-outs
    (needs review, edits to check, could-not-verify tray, gate blockers and warnings), export_ready.
    Computed from the functions GET case, /status and the export gate use; test compares all of them for every library case.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/api.py b/app/backend/api.py
index dfe1f24..c48b2a6 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -20,7 +20,7 @@ from starlette.exceptions import HTTPException as StarletteHTTPException
 
 from starlette.concurrency import run_in_threadpool
 
-from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
+from app.backend import case_extras, case_list, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
 from app.db import db as DB
 
 MAX_BODY_BYTES = 512 * 1024      # cheap rejection before the 60,000-character rule: UTF-8 worst case plus JSON overhead
@@ -221,7 +221,7 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             raise ApiError(404, "not_found", "Not found.")
         c = conn()
         try:
-            return {"cases": present.case_list(c)}
+            return {"cases": case_list.summaries(c, list(getattr(pipeline_mod(), "STAGES", None) or STAGES))}
         finally:
             c.close()
 
@@ -396,10 +396,9 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         c = conn()
         try:
             case = get_case(c, token)
-            stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
             stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
             stages = list(stages) if not callable(stages) else STAGES
-            done = stages.index(stage) if stage in stages else 0
+            stage, done = case_list.run_progress(case, stages)
             end = case["run_finished_at"] or time.time()
             return {"token": token, "status": case["status"], "stage": stage, "stages": stages,
                     "progress": {"done": done, "total": len(stages), "label": f"Step {done + 1} of {len(stages)}: {stage}" if stage else ""},
diff --git a/app/backend/case_list.py b/app/backend/case_list.py
new file mode 100644
index 0000000..34df4f1
--- /dev/null
+++ b/app/backend/case_list.py
@@ -0,0 +1,83 @@
+"""GET /api/cases (T-148): one summary per case for the local profile's overview screen. Local mode only (D-008/D-031); the route is a 404 otherwise.
+
+Code only: no model call, no pipeline run, no record text. Every number comes from the functions GET case, GET status and the export gate already use, so the
+list cannot say something the case screen does not:
+  run                                        -> run_progress() (the /status route calls it too)
+  progress decided / total per kind          -> the item filter present.review_view applies (live = not rejected, no tray placeholder, no rule-filtered proposal)
+  hitl.needs_review, edits_to_check, tray    -> present.review_view counts (the tray length GET case returns is the `rejected` count)
+  hitl.gate, export_ready                    -> the export_gate step of trace.case_trace (blockers and warnings with their plain `why`; the list GET /export refuses on)
+tests/unit/test_case_list.py compares each field with GET case, /status, /trace and /export for every library case.
+"""
+import datetime
+import re
+
+from app.backend import flag_templates as FT, generator, present, review, store, trace
+from app.db import db as DB
+
+KINDS = (("entries", "entry"), ("flags", "flag"), ("amounts", "amount"))
+_SLUG = re.compile(r"^[\w.\-]+$")
+_LIB_PREFIX = re.compile(r"^case[ _](?:lib)?\d+[ _]", re.IGNORECASE)      # evals/library and evals/golden file names: case_lib01_..., case_01_...
+_EXT = re.compile(r"\.(pdf|txt|docx?|rtf)$", re.IGNORECASE)
+
+
+def readable_title(name, source, created_at) -> str:
+    """A name a paralegal would recognise. A file name or slug ("smith_records-2024.pdf") becomes words; no name at all becomes "Untitled case" with its date."""
+    n = _LIB_PREFIX.sub("", (name or "").strip())
+    if n and (_SLUG.match(n) or n != (name or "").strip()) and not n.isalpha():          # one token with _ - . in it, or a library prefix: a file name or slug, not a typed name
+        n = re.sub(r"\s+", " ", re.sub(r"[_\-]+", " ", _EXT.sub("", n))).strip()
+        n = n[:1].upper() + n[1:]
+    if n:
+        return n
+    day = datetime.datetime.fromtimestamp(float(created_at or 0), datetime.timezone.utc).strftime("%b %-d")
+    return ("Sample case" if source == "sample" else "Untitled case") + (f", {day}" if source != "sample" else "")
+
+
+def run_progress(case: dict, stages) -> tuple:
+    """(stage, steps_done) for a case row: what GET /status reports. A case that was only ingested is at the 'ingest' stage."""
+    stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
+    return stage, (list(stages).index(stage) if stage in stages else 0)
+
+
+def _progress(conn, case_id) -> dict:
+    """decided / total per kind over the items review_view counts. An edit still marked Needs review (T-134) is not decided."""
+    items = {k: DB.list_items(conn, case_id, k) for _, k in KINDS}
+    handled = generator.resolved_placeholders(items["entry"])
+    out = {}
+    for label, kind in KINDS:
+        live = [r for r in items[kind] if r["id"] not in handled and not FT.is_filtered(r.get("state_reasons")) and r["state"] != "rejected"]
+        decided = sum(1 for r in live if r["review_status"] in ("accepted", "dismissed", "edited") and not review.edit_unconfirmed(kind, r))
+        out[label] = {"decided": decided, "total": len(live)}
+    return out
+
+
+def _gate(conn, case_id) -> dict:
+    step = next(s for s in trace.case_trace(conn, case_id, full=False)["steps"] if s["id"] == "export_gate")
+    keep = lambda xs, keys: [{k: x[k] for k in keys if k in x} for x in xs]      # noqa: E731
+    return {"ready": step["ready"], "blockers": keep(step["blockers"], ("reason_code", "kind", "item_id", "why")),
+            "warnings": keep(step["warnings"], ("reason_code", "count", "why"))}
+
+
+def summary(conn, case_id: str, stages) -> dict:
+    case = DB.get_case(conn, case_id)
+    rv = present.review_view(conn, case_id)
+    counts = rv["counts"]
+    stage, done = run_progress(case, stages)
+    gate = _gate(conn, case_id)
+    last = conn.execute("SELECT max(at) FROM review_events WHERE case_id=?", (case_id,)).fetchone()[0]
+    updated = case.get("run_finished_at") or case["created_at"]            # the same value GET case calls updated_at
+    return {"token": case_id, "title": readable_title(case["name"], case["source"], case["created_at"]), "name": case["name"],
+            "source": case["source"], "status": case["status"],
+            "record_count": conn.execute("SELECT count(*) FROM records WHERE case_id=?", (case_id,)).fetchone()[0],
+            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(updated), "last_activity_at": store.iso(max(updated, last or 0)),
+            "run": {"stage": stage, "steps_done": done, "steps_total": len(stages), "running": case["status"] == "running",
+                    "error": bool(case.get("error"))},
+            "progress": _progress(conn, case_id),
+            "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},      # kept from the first version of this route
+            "hitl": {"pending": counts["pending"], "needs_review": counts["needs_review"], "edits_to_check": counts["edit_to_check"],
+                     "could_not_verify": counts["rejected"], "gate_blockers": gate["blockers"], "gate_warnings": gate["warnings"]},
+            "export_ready": gate["ready"]}
+
+
+def summaries(conn, stages) -> list:
+    """Every case, newest first (created, then insertion order)."""
+    return [summary(conn, r["id"], stages) for r in conn.execute("SELECT id FROM cases ORDER BY created_at DESC, rowid DESC")]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:34:13.454Z

**tool call — Bash**
````
{
 "command": "cat tests/unit/test_case_list.py; grep -n \"D-036\" memory/ORCHESTRATOR_DECISIONS.md | head -5; grep -n \"loopback\\|127.0.0.1\\|testclient\\|peer\" app/backend/api.py | head -30"
}
````

### User / tool · 2026-11-02T13:34:13.554Z

**tool result**
````
"""T-148: GET /api/cases summary list. Every field is compared with the route that owns it (GET case, /status, /trace, /export) for every library
case, so the overview can never say something the case screen does not. Fixture backend, no network; local mode only."""
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import case_list
from app.backend.api import create_app

LIB = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"
LIB_IDS = sorted(p.stem for p in LIB.glob("*.txt"))


@pytest.fixture(scope="module")
def local(tmp_path_factory):
    import os
    old = {k: os.environ.get(k) for k in ("LLM_BACKEND", "ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY")}
    os.environ.update(LLM_BACKEND="fixture", ZLAYT_MODE="local")
    for k in ("ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        os.environ.pop(k, None)
    d = tmp_path_factory.mktemp("cl")
    c = TestClient(create_app(str(d / "t.sqlite"), static_dir=str(d)), client=("127.0.0.1", 50000))
    yield c
    for k, v in old.items():
        os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)


def _wait(c, tok):
    for _ in range(240):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            return s
        time.sleep(0.25)
    raise AssertionError(s)


@pytest.fixture(scope="module")
def cases(local):
    """Every library case run to the end, plus one left at ingest, plus decisions made on the first run case (accept, edit, dismiss)."""
    toks = {}
    for lid in LIB_IDS:
        r = local.post("/api/cases", json={"library": lid})
        assert r.status_code == 201, r.text
        toks[lid] = r.json()["token"]
        assert local.post(f"/api/cases/{toks[lid]}/run", json={}).status_code == 202
    for t in toks.values():
        _wait(local, t)
    first = toks[LIB_IDS[0]]
    items = [i for k in ("entries", "flags", "amounts") for i in local.get(f"/api/cases/{first}").json()[k]]
    for n, it in enumerate(items[:6]):
        local.post(f"/api/cases/{first}/items/{it['id']}/review", json={"action": ["accept", "dismiss"][n % 2]})
    second = local.get(f"/api/cases/{toks[LIB_IDS[1]]}").json()["entries"][0]          # a reworded entry: saved, but the second check cannot confirm the new wording
    local.post(f"/api/cases/{toks[LIB_IDS[1]]}/items/{second['id']}/review", json={"action": "edit", "edits": {"summary": second["summary"].rstrip(".") + " (reworded)."}})
    third = toks[LIB_IDS[2]]                                                                  # accept whatever the code checks allow: a case whose export gate opens
    for k in ("entries", "flags", "amounts"):
        for it in local.get(f"/api/cases/{third}").json()[k]:
            local.post(f"/api/cases/{third}/items/{it['id']}/review", json={"action": "accept"})
    text = (LIB / f"{LIB_IDS[-1]}.txt").read_text()               # an allowed (recorded) text, pasted under a file-slug name and never run
    toks["_ingested"] = local.post("/api/cases", json={"text": text, "name": "smith_records-2024.txt"}).json()["token"]
    return toks


def _by_token(local):
    r = local.get("/api/cases")
    assert r.status_code == 200
    return {x["token"]: x for x in r.json()["cases"]}


def test_list_covers_every_case_newest_first(local, cases):
    got = local.get("/api/cases").json()["cases"]
    assert {x["token"] for x in got} == set(cases.values()) and len(got) == len(LIB_IDS) + 1
    assert got[0]["token"] == cases["_ingested"] and [x["created_at"] for x in got] == sorted((x["created_at"] for x in got), reverse=True)


def test_every_summary_field_matches_the_case_status_gate_and_export(local, cases):
    listed = _by_token(local)
    for lid, tok in cases.items():
        s, case = listed[tok], local.get(f"/api/cases/{tok}").json()
        st = local.get(f"/api/cases/{tok}/status").json()
        tr = local.get(f"/api/cases/{tok}/trace").json()
        gate = next(x for x in tr["steps"] if x["id"] == "export_gate")
        # identity and times: the case screen's own values
        assert s["name"] == case["name"] and s["status"] == case["status"] and s["created_at"] == case["created_at"] and s["updated_at"] == case["updated_at"], lid
        assert s["record_count"] == len(case["records"]) and s["last_activity_at"] >= s["updated_at"], lid
        # run stage: the status route
        assert s["run"]["stage"] == st["stage"] and s["run"]["steps_done"] == st["progress"]["done"] and s["run"]["steps_total"] == st["progress"]["total"], lid
        assert s["run"]["running"] == (case["status"] == "running"), lid
        # review counts and the could-not-verify tray: the case screen
        rc = case["review"]["counts"]
        h = s["hitl"]
        assert h["needs_review"] == rc["needs_review"] and h["edits_to_check"] == rc["edit_to_check"] and h["pending"] == rc["pending"], lid
        assert h["could_not_verify"] == len(case["tray"]), lid
        assert s["counts"] == {k: rc[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")}, lid
        # progress per kind: totals are the live items GET case lists, decided never exceeds total, and the kinds add up to the review counts
        live = {"entries": [e for e in case["entries"] + case["undated_entries"]], "flags": case["flags"], "amounts": case["amounts"]}
        for kind, rows in live.items():
            p = s["progress"][kind]
            assert p["total"] == len(rows), (lid, kind)
            assert p["decided"] == sum(1 for r in rows if r["review_status"] in ("accepted", "dismissed", "edited")) - (rc["edit_to_check"] if kind == "entries" else 0), (lid, kind)
        tot = sum(v["total"] for v in s["progress"].values())
        dec = sum(v["decided"] for v in s["progress"].values())
        assert tot - dec == rc["pending"] + rc["edit_to_check"], lid
        # gate: blockers and warnings with their plain reasons, and export_ready is what GET /export allows
        assert s["export_ready"] is gate["ready"] is (local.get(f"/api/cases/{tok}/export").status_code == 200), lid
        assert [(b["reason_code"], b["why"]) for b in h["gate_blockers"]] == [(b["reason_code"], b["why"]) for b in gate["blockers"]], lid
        assert [(w["reason_code"], w["count"], w["why"]) for w in h["gate_warnings"]] == [(w["reason_code"], w["count"], w["why"]) for w in gate["warnings"]], lid
        assert all(b["why"] for b in h["gate_blockers"]) and all(w["why"] for w in h["gate_warnings"]), lid


def test_decisions_move_the_progress_and_the_ingested_case_is_not_ready(local, cases):
    s = _by_token(local)
    first = s[cases[LIB_IDS[0]]]
    assert sum(v["decided"] for v in first["progress"].values()) >= 1 and first["last_activity_at"] > first["updated_at"] or first["last_activity_at"] >= first["updated_at"]
    ing = s[cases["_ingested"]]
    assert ing["status"] == "ingested" and ing["run"]["stage"] == "ingest" and ing["export_ready"] is False
    assert [b["reason_code"] for b in ing["hitl"]["gate_blockers"]] == ["NOTHING_ACCEPTED"]


def test_decided_cases_cover_ready_and_edit_to_check(local, cases):
    s = _by_token(local)
    third = s[cases[LIB_IDS[2]]]
    assert third["export_ready"] is True and third["hitl"]["gate_blockers"] == [] and sum(v["decided"] for v in third["progress"].values()) > 0
    second = s[cases[LIB_IDS[1]]]
    assert second["hitl"]["edits_to_check"] == 1 and second["progress"]["entries"]["decided"] == 0          # a reworded entry is saved but not decided
    assert "EDIT_NOT_CONFIRMED" in [w["reason_code"] for w in second["hitl"]["gate_warnings"]]


def test_title_is_readable_not_a_file_slug(local, cases):
    s = _by_token(local)
    assert s[cases["_ingested"]]["title"] == "Smith records 2024"
    for lid in LIB_IDS:
        t = s[cases[lid]]["title"]
        assert t and "_" not in t and not t.endswith((".txt", ".pdf")) and not t.lower().startswith(("case ", "lib")), t
    assert s[cases[LIB_IDS[0]]]["title"] == "Er only then gap"
    assert case_list.readable_title("case_01_date_formats", "paste", 0) == "Date formats"
    assert case_list.readable_title("records_final-v2.pdf", "paste", 0) == "Records final v2"
    assert case_list.readable_title("Smith v. Jones intake", "paste", 0) == "Smith v. Jones intake"
    assert case_list.readable_title(None, "paste", 1762000000) == "Untitled case, Nov 1"
    assert case_list.readable_title("", "sample", 0) == "Sample case"


def test_list_is_code_only_no_text_no_model_calls(local, cases):
    import json
    listed = local.get("/api/cases").json()["cases"]
    raw = json.dumps(listed)
    assert "Excerpt:" not in raw and "raw_text" not in raw
    before = {t: local.get(f"/api/cases/{t}/audit").json()["summary"]["calls"] for t in list(cases.values())[:3]}
    local.get("/api/cases")
    assert before == {t: local.get(f"/api/cases/{t}/audit").json()["summary"]["calls"] for t in before}


def test_list_is_404_outside_local_mode(local, monkeypatch):
    monkeypatch.delenv("ZLAYT_MODE")
    assert local.get("/api/cases").status_code == 404
44:| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
83:def is_loopback_peer(request) -> bool:
84:    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
90:    return (getattr(ip, "ipv4_mapped", None) or ip).is_loopback
107:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
108:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
179:            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
180:                resp = JSONResponse({"error": {"code": "forbidden", "message": "Local mode accepts loopback clients only.", "detail": {}}}, status_code=403)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:34:18.116Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head; cd $S && (time /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider 2>&1 | tail -8); sed -n 170,190p app/backend/api.py; sed -n 205,230p app/backend/api.py",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T13:34:21.493Z

**tool result**
````
.......                                                                  [100%]
7 passed in 3.05s

real	0m3.292s
user	0m2.354s
sys	0m0.782s
    async def _headers(request, call_next):
        if request.url.path.startswith("/api") and time.time() - purged["at"] > 60:     # expired cases vanish even with no create
            purged["at"] = time.time()
            c = conn()
            try:
                DB.purge_expired(c, time.time())
            finally:
                c.close()
        try:
            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
                resp = JSONResponse({"error": {"code": "forbidden", "message": "Local mode accepts loopback clients only.", "detail": {}}}, status_code=403)
            else:
                resp = await call_next(request)
        except Exception as e:                                                          # last line of defence: standard JSON, no detail
            log.error("unhandled %s", type(e).__name__)
            resp = JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
        resp.headers["Content-Security-Policy"] = CSP
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api") else resp.headers.get("Cache-Control", "no-cache")
        return resp
        except ValueError:
            raise ApiError(400, "bad_request", "Request body is not valid JSON.") from None
        if not isinstance(b, dict):
            raise ApiError(400, "bad_request", "Request body must be a JSON object.")
        return b

    # -------------------------------------------------- routes
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
            return {"cases": case_list.summaries(c, list(getattr(pipeline_mod(), "STAGES", None) or STAGES))}
        finally:
            c.close()

    @app.get("/api/library")
    def library():
        if not local_mode():
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:34:26.850Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1; grep -n \"def case_list\" -A22 $S/head/app/backend/present.py; grep -rn \"api/cases\\\"\\|api/cases'\\|\\.cases\\b\" $S/head/app/frontend/*.js | head -20; grep -rn \"case_list\" $S/head --include=*.py -l"
}
````

### User / tool · 2026-11-02T13:34:26.969Z

**tool result**
````
366:def case_list(conn):
367-    """Local mode only (D-008/D-031): newest first. Metadata and counts, never record text."""
368-    out = []
369-    for r in conn.execute("SELECT id FROM cases ORDER BY created_at DESC, rowid DESC"):
370-        cid = r["id"]
371-        case = DB.get_case(conn, cid)
372-        counts = review_view(conn, cid)["counts"]
373-        out.append({"token": cid, "name": case["name"], "status": case["status"], "source": case["source"],
374-                    "record_count": conn.execute("SELECT count(*) FROM records WHERE case_id=?", (cid,)).fetchone()[0],
375-                    "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},
376-                    "created_at": store.iso(case["created_at"])})
377-    return out
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/frontend/switcher.js:65:    draw((a.body && a.body.cases) || [], (b.status === 200 && b.body && b.body.cases) || []);
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/evals/letter_check.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/present.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/api.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/case_list.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_case_list.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_calibration_route.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_api_routes.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/e2e/test_local_mode.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:34:28.992Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1; cd $S/head && (/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -x -q 2>&1 | tail -8) ",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T13:34:29.055Z

**tool result**
````
Command running in background with ID: baj6mx6th. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/baj6mx6th.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:34:41.735Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1; mkdir -p $S/mut && cp -R $S/head/. $S/mut/ && cd $S/mut && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\nrun(){ $PY -m pytest tests/unit/test_case_list.py -q -p no:cacheprovider 2>&1 | tail -2 | tr '\\n' ' '; echo; }\ncp app/backend/case_list.py /tmp/x 2>/dev/null; cp app/backend/case_list.py $S/cl.orig\nm(){ # name, python-expr replace old->new\n  cp $S/cl.orig app/backend/case_list.py; $PY - \"$2\" \"$3\" <<'E'\nimport sys,pathlib\np=pathlib.Path(\"app/backend/case_list.py\");t=p.read_text();o,n=sys.argv[1],sys.argv[2]\nassert o in t,o\np.write_text(t.replace(o,n,1))\nE\n  echo \"== $1\"; run; }\nm M1-edit_unconfirmed \"and not review.edit_unconfirmed(kind, r))\" \")\"\nm M2-rejected-live ' and r[\"state\"] != \"rejected\"]' ']'\nm M3-tray 'counts[\"rejected\"]' '0'\nm M4-needs_review 'counts[\"needs_review\"],' '0,'\nm M5-ready 'gate[\"ready\"]}' 'True}'\nm M6-warnings 'gate_warnings\": gate[\"warnings\"]' 'gate_warnings\": []'\nm M7-blocker-why '(\"reason_code\", \"kind\", \"item_id\", \"why\")' '(\"reason_code\", \"kind\", \"item_id\")'\nm M8-edits_to_check 'counts[\"edit_to_check\"]' 'counts[\"needs_review\"]'\nm M9-stage 'stage = case[\"stage\"] or (\"ingest\" if case[\"status\"] == \"ingested\" else None)' 'stage = case[\"stage\"]'\nm M10-filter 'not FT.is_filtered(r.get(\"state_reasons\")) and' ''\nm M11-handled 'r[\"id\"] not in handled and' ''\nm M12-total-steps 'len(stages),' 'len(stages)+1,'\nm M13-running 'case[\"status\"] == \"running\"' 'False'\nm M14-error 'bool(case.get(\"error\"))' 'False'\ncp $S/cl.orig app/backend/case_list.py",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T13:35:34.730Z

**tool result**
````
== M1-edit_unconfirmed
FAILED tests/unit/test_case_list.py::test_decided_cases_cover_ready_and_edit_to_check 2 failed, 5 passed in 3.92s 
== M2-rejected-live
FAILED tests/unit/test_case_list.py::test_every_summary_field_matches_the_case_status_gate_and_export 1 failed, 6 passed in 2.95s 
== M3-tray
FAILED tests/unit/test_case_list.py::test_every_summary_field_matches_the_case_status_gate_and_export 1 failed, 6 passed in 2.94s 
== M4-needs_review
FAILED tests/unit/test_case_list.py::test_every_summary_field_matches_the_case_status_gate_and_export 1 failed, 6 passed in 3.08s 
== M5-ready
FAILED tests/unit/test_case_list.py::test_decisions_move_the_progress_and_the_ingested_case_is_not_ready 2 failed, 5 passed in 3.19s 
== M6-warnings
FAILED tests/unit/test_case_list.py::test_decided_cases_cover_ready_and_edit_to_check 2 failed, 5 passed in 3.11s 
== M7-blocker-why
FAILED tests/unit/test_case_list.py::test_every_summary_field_matches_the_case_status_gate_and_export 1 failed, 6 passed in 3.34s 
== M8-edits_to_check
FAILED tests/unit/test_case_list.py::test_decided_cases_cover_ready_and_edit_to_check 2 failed, 5 passed in 3.45s 
== M9-stage
FAILED tests/unit/test_case_list.py::test_decisions_move_the_progress_and_the_ingested_case_is_not_ready 1 failed, 6 passed in 3.94s 
== M10-filter
.......                                                                  [100%] 7 passed in 3.93s 
== M11-handled
.......                                                                  [100%] 7 passed in 3.53s 
== M12-total-steps
FAILED tests/unit/test_case_list.py::test_every_summary_field_matches_the_case_status_gate_and_export 1 failed, 6 passed in 3.11s 
== M13-running
.......                                                                  [100%] 7 passed in 3.73s 
== M14-error
.......                                                                  [100%] 7 passed in 3.51s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:35:42.692Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head; grep -n \"def review_view\" -A45 $S/app/backend/present.py | head -90; grep -n \"def is_filtered\" -A8 $S/app/backend/flag_templates.py; grep -n \"def resolved_placeholders\" -A12 $S/app/backend/generator.py"
}
````

### User / tool · 2026-11-02T13:35:42.804Z

**tool result**
````
194:def review_view(conn, case_id):
195-    items = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, case_id, k)]
196-    handled = generator.resolved_placeholders([r for k, r in items if k == "entry"])
197-    items = [(k, r) for k, r in items if r["id"] not in handled and not FT.is_filtered(r.get("state_reasons"))]       # D-057: rule-filtered proposals need no action and are not counted
198-    live = [(k, r) for k, r in items if r["state"] != "rejected"]
199-    counts = {s: sum(1 for _, r in live if r["review_status"] == s) for s in ("pending", "accepted", "edited", "dismissed")}
200-    counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
201-    counts["edit_to_check"] = sum(1 for k, r in live if review.edit_unconfirmed(k, r))      # T-134: counted in `edited`, but open: not in the letter, not accepted
202-    rank = {"amount": 0, "entry": 1, "flag": 2}
203-    pend = sorted((x for x in live if x[1]["review_status"] == "pending"),
204-                  key=lambda x: (confidence.sort_key(x[1]["state"]), rank[x[0]], x[1].get("date_iso") or "", x[1]["id"]))
205-    return {"counts": counts, "queue": [r["id"] for _, r in pend],
206-            "ready_to_export": counts["pending"] == 0 and counts["edit_to_check"] == 0 and (counts["accepted"] + counts["edited"] - counts["edit_to_check"]) > 0}
207-
208-
209-def dates_to_confirm(conn, case_id):
210-    recs = list(_recs_by_id(conn, case_id).values())
211-    raw = DB.get_case(conn, case_id)["raw_text"]
212-    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"],
213-             "suggestion": date_convention.suggest(r, recs, raw)}      # T-088: a hint only, never applied (D-042)
214-            for r in recs if r["date_status"] in ("ambiguous", "missing")]
215-
216-
217-def record_view(r, raw, with_sentences=True, pages=None):
218-    block = raw[r["char_start"]:r["char_end"]]
219-    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
220-         "date_status": r["date_status"], "date_candidates": r["date_candidates"] or [], "duplicate_of": r["duplicate_of"],
221-         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
222-         "char_end": r["char_end"], "text": block, "language": language.block_lang(block),
223-         "unsplit": bool(r.get("unsplit")), "preamble": bool(r.get("preamble"))}      # T-129: text outside any recognised record (D-027); a preamble sits above the first real record
224-    if pages:                                    # PDF source (D-031): the page where the record starts
225-        v["page"] = pdf_text.page_for(pages, r["char_start"])
226-        from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR
227-        v["ocr_derived"] = pdf_checks.is_ocr_span(pages, r["char_start"], r["char_end"])
228-    if with_sentences:
229-        base, body, why_none = quote_body(block)  # T-108: units come from the quotable body only, the same text the save route checks the quote against
230-        units = [] if why_none else quote_units(body, {**r, "excerpt": body})
231-        v["sentences"] = [{"text": body[a:b], "start": r["char_start"] + base + a, "end": r["char_start"] + base + b} for a, b in units]
232-        if why_none:
233-            v["sentences_reason"] = why_none           # no sentence is offered; the reason is plain words for the review screen
234-    return v
235-
236-
237-NO_UNITS_LAYOUT = ("No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, "
238-                   "so a quote cut from it could not be checked against the record. Read the record text instead.")
239-_LABEL_LINE = re.compile(r"^[ \t]*(?:Excerpt:|Date:|Source:|=== Record \d+ ===)", re.MULTILINE)
224:def is_filtered(reasons) -> bool:
225-    """T-126 r2: THE test for a rule-filtered proposal (its reason code comes first). Every reader uses this, never the literal."""
226-    return list(reasons or [])[:1] == [FILTERED]
156:def resolved_placeholders(entries: list) -> set:
157-    """Ids of could-not-verify placeholders (`ladder.failure`) whose record now has a live entry, which is the entry the paralegal wrote by hand (T-110 r2).
158-    Such a placeholder is handled: the tray, the rejected counts and the export's excluded count leave it out. The row itself stays (audit)."""
159-    live = {r for e in entries if e["state"] != "rejected" for r in (e["record_ids"] or [])}
160-    return {e["id"] for e in entries if (e.get("ladder") or {}).get("failure") and e["state"] == "rejected" and live & set(e["record_ids"] or [])}
161-
162-
163-def extract_entries(records: list, groups: list, *, call, case_text: str = "", workers: int = CONCURRENCY):
164-    """Stages 1-2 over distinct records (only the first record of each duplicate group is sent). Returns
165-    (entries, rejected, failures). `entries` are chronological by (date, seq) and never contain a rejected item; `rejected` goes to the
166-    tray only (R-TL-2). `failures` = [{'record_no', 'failure'}] for records with no output (LLM_FAILED_AFTER_RETRIES / FIXTURE_MISS)."""
167-    by_n = {r["n"]: r for r in records}
168-    jobs = [(by_n[g[0]], g, call, case_text) for g in groups]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:35:50.055Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head; grep -rn \"FILTERED\" $S/app/backend/*.py | head -20"
}
````

### User / tool · 2026-11-02T13:35:50.152Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/confidence.py:14:    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE", "FILTERED_BY_RULE", "CHARGE_TEXT_IN_ENTRY",
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/flag_templates.py:221:FILTERED = "FILTERED_BY_RULE"
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/flag_templates.py:226:    return list(reasons or [])[:1] == [FILTERED]
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/flags.py:22:FILTER_RULES, FILTERED = FT.FILTER_RULES, FT.FILTERED       # D-057 (T-126): data lives in flag_templates so present.py can read it without importing the engines
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/flags.py:178:        f["_tray"] = FILTERED
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/flags.py:358:    if code == FILTERED:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/flags.py:360:        f["reasons"] = [FILTERED] + [r for r in f["reasons"] if r not in (FILTERED, "JUDGE_UNAVAILABLE", "LLM_ONLY")]       # keeps a grounding failure / injection reason (T-126 r2)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/flags.py:361:        f["why"] = why.why(FILTERED) + ("" if "GROUNDING_EXCERPT_NOT_VERBATIM" not in f["reasons"] else " " + why.why("GROUNDING_EXCERPT_NOT_VERBATIM"))
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/why.py:27:    "FILTERED_BY_RULE": "The AI proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:35:56.458Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head; sed -n 352,366p $S/app/backend/flags.py; sed -n 170,182p $S/app/backend/flags.py; grep -n \"is_filtered\\|_tray\" $S/app/backend/api.py $S/app/backend/present.py | head"
}
````

### User / tool · 2026-11-02T13:35:56.566Z

**tool result**
````
        _to_tray(f, "JUDGE_DISAGREES", reason)


def _to_tray(f: dict, code: str, judge_reason=None) -> None:
    """Move a flag to the could-not-verify tray: state rejected, the reason code first, a fixed sentence (plus the judge's fixed detail sentence)."""
    f["state"] = "rejected"
    if code == FILTERED:
        f["_stage"]["judge"] = None
        f["reasons"] = [FILTERED] + [r for r in f["reasons"] if r not in (FILTERED, "JUDGE_UNAVAILABLE", "LLM_ONLY")]       # keeps a grounding failure / injection reason (T-126 r2)
        f["why"] = why.why(FILTERED) + ("" if "GROUNDING_EXCERPT_NOT_VERBATIM" not in f["reasons"] else " " + why.why("GROUNDING_EXCERPT_NOT_VERBATIM"))
        return
    if code == "LLM_ONLY":
        # never sent to a judge by design (model-only, not code-confirmed): it carries its real reason, not the compose default "judge unavailable"
        # (T-122: the eval counted case_05's f_r1_1 as a judge that did not run)
        f["_stage"]["judge"] = None
            continue
        f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", llm_spans[i], tagged, "llm_only")
        _note_merged(f, lf)
        if lf.get("category") in _NEEDS_LEXICON:
            f["_tray"] = "LLM_ONLY"      # D-032 + D-053: a scene_facts flag needs a phrase-list hit; the model's alone is shown in the tray, never dropped
        out.append(f)
    for lf in filtered:
        f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", grounding.locate(body, lf["excerpt"]), tagged, "llm_only")
        f["_tray"] = FILTERED
        f["_last"] = True       # after every other tray item, so no recorded judge prompt (it carries the flag id) changes
        out.append(f)
    for f in out:
        f["_stage"]["injection"] = tagged
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/present.py:197:    items = [(k, r) for k, r in items if r["id"] not in handled and not FT.is_filtered(r.get("state_reasons"))]       # D-057: rule-filtered proposals need no action and are not counted
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/present.py:294:    def _tray_flag(x):
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/present.py:301:    filtered = [x for x in rejected_flags if FT.is_filtered(x["reasons"])]
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/present.py:302:    tray += [_tray_flag(x) for x in rejected_flags if x not in filtered]
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/app/backend/present.py:307:        items = [_tray_flag(x) for x in filtered if x["category"] == cat]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:36:10.528Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1; cat > $S/probe.py <<'E'\nimport os, sys, time, pathlib, tempfile, json\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfor k in (\"ENABLE_LIVE\",\"ANTHROPIC_API_KEY\"): os.environ.pop(k, None)\nroot = sys.argv[1]; sys.path.insert(0, root); os.chdir(root)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nd = tempfile.mkdtemp()\napp = create_app(d + \"/t.sqlite\", static_dir=d)\nc = TestClient(app, client=(\"127.0.0.1\", 50000))\nlib = sorted(p.stem for p in pathlib.Path(root, \"evals/library\").glob(\"*.txt\"))\ntoks = []\nfor lid in lib:\n    t = c.post(\"/api/cases\", json={\"library\": lid}).json()[\"token\"]; toks.append(t)\n    c.post(f\"/api/cases/{t}/run\", json={})\nfor t in toks:\n    for _ in range(240):\n        if c.get(f\"/api/cases/{t}/status\").json()[\"status\"] in (\"ready\",\"failed\"): break\n        time.sleep(0.25)\n# filtered / handled prevalence\nconn = DB.connect(d + \"/t.sqlite\") if hasattr(DB, \"connect\") else None\nfrom app.backend import flag_templates as FT\nimport sqlite3\nfor t in toks:\n    case = c.get(f\"/api/cases/{t}\").json()\n    s = {x[\"token\"]: x for x in c.get(\"/api/cases\").json()[\"cases\"]}[t]\n    print(t[:6], \"tray\", len(case[\"tray\"]), \"hitl.cnv\", s[\"hitl\"][\"could_not_verify\"], \"err\", s[\"run\"][\"error\"], case[\"status\"])\n# perf: 50 cases (the 15 library + 35 more ingests of library text)\ntexts = [pathlib.Path(root, \"evals/library\", l + \".txt\").read_text() for l in lib]\nfor i in range(35):\n    c.post(\"/api/cases\", json={\"text\": texts[i % len(texts)], \"name\": f\"copy_{i}.txt\"})\n# run half so they have items\nfor t in toks[:0]: pass\nfor n in range(3):\n    t0 = time.perf_counter(); r = c.get(\"/api/cases\"); dt = time.perf_counter() - t0\n    print(\"50-case list\", len(r.json()[\"cases\"]), r.status_code, round(dt*1000), \"ms\")\n# non loopback\nc2 = TestClient(app, client=(\"203.0.113.9\", 50000))\nr = c2.get(\"/api/cases\"); print(\"non-loopback\", r.status_code, r.json())\nc3 = TestClient(app, client=(\"::1\", 50000)); print(\"::1\", c3.get(\"/api/cases\").status_code)\n# call count\na0 = [c.get(f\"/api/cases/{t}/audit\").json()[\"summary\"][\"calls\"] for t in toks[:3]]\nc.get(\"/api/cases\"); a1 = [c.get(f\"/api/cases/{t}/audit\").json()[\"summary\"][\"calls\"] for t in toks[:3]]\nprint(\"calls unchanged\", a0 == a1)\n# corrupt one case: does the whole list fail?\ncn = sqlite3.connect(d + \"/t.sqlite\"); cn.execute(\"UPDATE items SET review_status=NULL WHERE rowid=(SELECT min(rowid) FROM items)\") if False else None\n# modes\nos.environ.pop(\"ZLAYT_MODE\"); print(\"public\", c.get(\"/api/cases\").status_code)\nE\n.venv/bin/python -I $S/probe.py $S/head 2>&1 | tail -40",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T13:36:14.912Z

**tool result**
````
llm call failed call_id=c20ac2be1d837 step=extract attempt=1 prompt_hash=83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557
FFil6X tray 1 hitl.cnv 1 err False ready
YHOmfk tray 1 hitl.cnv 1 err False ready
-c7TEv tray 0 hitl.cnv 0 err False ready
8rWkqD tray 0 hitl.cnv 0 err False ready
_jLGqC tray 0 hitl.cnv 0 err False ready
sffi7X tray 1 hitl.cnv 1 err False ready
yBTrir tray 2 hitl.cnv 2 err False ready
Sview_ tray 1 hitl.cnv 1 err False ready
rpqkE5 tray 0 hitl.cnv 0 err False ready
jPZ4nt tray 0 hitl.cnv 0 err False ready
_bB5dx tray 2 hitl.cnv 2 err False ready
E_2YQT tray 0 hitl.cnv 0 err False ready
MHRjA6 tray 0 hitl.cnv 0 err False ready
V6M5ez tray 1 hitl.cnv 1 err False ready
lMxXyh tray 1 hitl.cnv 1 err False ready
50-case list 50 200 100 ms
50-case list 50 200 91 ms
50-case list 50 200 93 ms
non-loopback 403 {'error': {'code': 'forbidden', 'message': 'Local mode accepts loopback clients only.', 'detail': {}}}
::1 200
calls unchanged True
public 404
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:36:23.414Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head; sed -n 286,322p $S/app/backend/present.py; grep -ln \"FILTERED_BY_RULE\" $S/tests/unit/*.py | head; grep -ln \"manual_entry\\|/entry\\\"\" $S/tests/unit/*.py | head"
}
````

### User / tool · 2026-11-02T13:36:23.527Z

**tool result**
````
    live_e = [e for e in ents if e["state"] != "rejected"]
    dated = sorted((e for e in live_e if e["date"] and (e["date_status"] in ("parsed", "confirmed", None))), key=lambda e: (e["date"], e["seq"] or 0))
    undated = [e for e in live_e if e not in dated]
    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
             "attempt": {"summary": x.get("summary"), "excerpt": x.get("excerpt")} if k == "entry" else {"text": x.get("text"), "excerpt": x.get("excerpt")},
             "ladder": {"item_id": x["id"], "state": "rejected"}} for k in ("entry", "amount") for x in its[k] if x["state"] == "rejected" and x["id"] not in handled]
    # D-053: a flag the judge rejected (a model-only flag J4 disagreed with, a code conflict candidate J3 called benign, a model-proposed conflict) is a tray
    # item of kind "flag": the model's attempt is the title and the quote(s); it is never in `flags`, the review queue or the letter.
    def _tray_flag(x):
        return {"id": x["id"], "kind": "flag", "record_ids": sorted({e["record_id"] for e in x["evidence"] if e.get("record_id")}), "state": "rejected",
                "reasons": x["reasons"], "why": (x["why"] + " " + why.judge_detail(((x.get("ladder") or {}).get("judge") or {}).get("reason_code"))).strip(),
                "flag": {"type": x["type"], "category": x["category"]},
                "attempt": {"summary": x.get("title"), "excerpt": " / ".join(e["excerpt"] for e in x["evidence"] if e.get("excerpt"))},
                "ladder": {"item_id": x["id"], "state": "rejected"}}
    rejected_flags = [x for x in its["flag"] if x["state"] == "rejected"]
    filtered = [x for x in rejected_flags if FT.is_filtered(x["reasons"])]
    tray += [_tray_flag(x) for x in rejected_flags if x not in filtered]
    # D-057: model proposals a code rule filtered out are a collapsed, counted group of their own (never in `tray`, `flags`, the queue or the letter)
    rules = []
    for cat in sorted({x["category"] for x in filtered}):
        ref, name, text = FT.FILTER_RULES.get(cat, ("", cat, ""))
        items = [_tray_flag(x) for x in filtered if x["category"] == cat]
        rules.append({"rule": cat, "ref": ref, "label": name, "explanation": text, "count": len(items), "items": items})
    tray_filtered = {"label": "Filtered by rule", "collapsed": True, "needs_action": False, "count": len(filtered), "rules": rules}
    err = json.loads(case["error"]) if case.get("error") else None
    injected = [r["id"] for r in recs if r["injection_tag"]]
    record_views = [record_view(r, raw, pages=((case.get("config") or {}).get("pages"))) for r in recs]
    uncovered.attach(record_views, ents, quote_body)      # T-143: clinical sentences no entry quote covers (review aid; never in the letter or notes)
    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
            "records": record_views, "undated_entries": undated, "entries": dated,
            "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks(), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
            "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
            "review": review_view(conn, case_id), "warnings": [], "error": err,
            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
            **{k: (case.get("config") or {})[k] for k in ("pdf_checks",) if (case.get("config") or {}).get(k)},     # T-086/T-087 (PDF cases only)
            **({"pdf_pages": (case.get("config") or {})["pages"]} if (case.get("config") or {}).get("pages") else {})}
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_flags_pass.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_t126_filtered_by_rule.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_api_routes.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_d050_never_verified.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_db.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_lib09_t110.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_lib09_t110_r2.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_manual_and_split.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_ocr_invariant.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_quote_units.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_trace.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:36:36.196Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1; sed -n 40,110p $S/head/app/frontend/switcher.js; cat $S/../../../../../../../../../../tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/baj6mx6th.output 2>/dev/null | tail -5"
}
````

### User / tool · 2026-11-02T13:36:36.285Z

**tool result**
````
    if (!cases.length) list.append(el("li", { class: "rv-empty" }, "No cases yet."));
    cases.forEach((c) => {
      const k = c.counts || {};
      list.append(el("li", {}, el("button", { type: "button", class: "btn cs-btn", "data-testid": "case-" + c.token, "aria-current": c.token === cur ? "true" : null, onclick: () => open(c.token) },
        (c.token === cur ? "Open now: " : "") + (ZL.niceName(c.name) || ("Pasted records" + (when(c.created_at || c.updated_at) ? ", " + when(c.created_at || c.updated_at) : ""))), el("span", { class: "cs-meta" }, [c.status, c.record_count != null ? c.record_count + " records" : null, k.pending != null ? k.pending + " pending" : null, when(c.created_at || c.updated_at)].filter(Boolean).join(" · ")))));
    });
    const lib = el("ul", { class: "cs-list", "data-testid": "library-list" });
    library.forEach((l) => lib.append(el("li", {}, el("button", { type: "button", class: "btn cs-btn", "data-testid": "library-" + l.id, onclick: () => loadLibrary(l.id) },
      ZL.niceName(l.name), l.description ? el("span", { class: "cs-meta" }, firstSentence(l.description.replace(/^Library L\d+ \([^)]*\)\.\s*/, ""))) : null))));
    if (!library.length) lib.append(el("li", { class: "rv-empty" }, "The library is empty."));
    const msg = root.querySelector(".cs-msg") || el("p", { class: "cs-msg rv-error", role: "status" });
    const wasOpen = root.querySelector("details") ? root.querySelector("details").open : false;
    clear(root);
    root.append(el("details", { class: "cs-details", open: wasOpen },
      el("summary", { id: "cs-h" }, "Cases (" + cases.length + ") and synthetic library"),
      el("div", { class: "cs-body" }, list, el("h3", { class: "cs-h" }, "Add a synthetic case (loads and runs it)"), lib, msg)));
  }
  async function refresh() {
    const [a, b] = await Promise.all([get("/cases"), get("/library")]);
    if (a.status !== 200) { if (root) root.hidden = true; return; }
    if (!root) {
      root = el("section", { id: "case-switcher", class: "card cs", "data-testid": "case-switcher", "aria-labelledby": "cs-h" }, el("p", { class: "cs-msg rv-error", role: "status" }));
      const main = document.querySelector("main"); main.append(root);   // under the work, collapsed: the paste box and the review come first
    }
    root.hidden = false;
    draw((a.body && a.body.cases) || [], (b.status === 200 && b.body && b.body.cases) || []);
  }
  document.addEventListener("DOMContentLoaded", () => {
    refresh().catch(() => {});
    ZL.state.subscribe((s) => { if (s.token !== lastToken) { lastToken = s.token; if (root) refresh().catch(() => {}); } });
  });
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:36:45.113Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1; cat > $S/probe2.py <<'E'\nimport os, sys, time, pathlib, tempfile, json, sqlite3\nos.environ.update(LLM_BACKEND=\"fixture\", ZLAYT_MODE=\"local\")\nfor k in (\"ENABLE_LIVE\",\"ANTHROPIC_API_KEY\"): os.environ.pop(k, None)\nroot = sys.argv[1]; sys.path.insert(0, root); os.chdir(root)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nd = tempfile.mkdtemp(); db = d + \"/t.sqlite\"\nc = TestClient(create_app(db, static_dir=d), client=(\"127.0.0.1\", 50000))\nlib = sorted(p.stem for p in pathlib.Path(root, \"evals/library\").glob(\"*.txt\"))\ndef mk(i):\n    t = c.post(\"/api/cases\", json={\"library\": lib[i]}).json()[\"token\"]; c.post(f\"/api/cases/{t}/run\", json={})\n    for _ in range(240):\n        if c.get(f\"/api/cases/{t}/status\").json()[\"status\"] in (\"ready\",\"failed\"): break\n        time.sleep(0.25)\n    return t\na, b, e = mk(0), mk(1), mk(3)\ncx = sqlite3.connect(db)\ncx.execute(\"UPDATE cases SET status='failed', error=? WHERE id=?\", (json.dumps({\"code\":\"LLM_FAILED_AFTER_RETRIES\",\"message\":\"The model did not answer.\"}), a))\ncx.execute(\"UPDATE cases SET status='running', stage='judge' WHERE id=?\", (b,))\ncx.commit()\nL = {x[\"token\"]: x for x in c.get(\"/api/cases\").json()[\"cases\"]}\nfor t,n in ((a,\"failed\"),(b,\"running\")):\n    s = L[t]; g = c.get(f\"/api/cases/{t}\").json()\n    print(n, \"status\", s[\"status\"], \"run\", s[\"run\"], \"export_ready\", s[\"export_ready\"], \"blockers\", [x[\"reason_code\"] for x in s[\"hitl\"][\"gate_blockers\"]], \"| GET case error:\", g[\"error\"], \"| /export\", c.get(f\"/api/cases/{t}/export\").status_code)\n# corrupt: delete the export-gate dependency -> one bad case 500s the list?\ncx.execute(\"UPDATE items SET review_status='bogus' WHERE case_id=? \", (e,)); cx.commit()\nr = c.get(\"/api/cases\"); print(\"bogus review_status list:\", r.status_code)\ncx.execute(\"UPDATE cases SET config='{not json' WHERE id=?\", (e,)); cx.commit()\nr = c.get(\"/api/cases\"); print(\"bad config list:\", r.status_code, r.text[:120])\nE\n.venv/bin/python -I $S/probe2.py $S/head 2>&1 | grep -v \"llm call failed\" | tail -12",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T13:36:46.641Z

**tool result**
````
failed status failed run {'stage': 'finalize', 'steps_done': 7, 'steps_total': 8, 'running': False, 'error': True} export_ready False blockers ['RUN_FAILED', 'NOTHING_ACCEPTED'] | GET case error: {'code': 'LLM_FAILED_AFTER_RETRIES', 'message': 'The model did not answer.'} | /export 422
running status running run {'stage': 'judge', 'steps_done': 0, 'steps_total': 8, 'running': True, 'error': False} export_ready False blockers ['RUN_IN_PROGRESS', 'NOTHING_ACCEPTED'] | GET case error: None | /export 422
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/probe2.py", line 26, in <module>
    cx.execute("UPDATE items SET review_status='bogus' WHERE case_id=? ", (e,)); cx.commit()
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: no such table: items
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:36:55.427Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1; grep -rn \"is_loopback\\|loopback\" $S/head/tests/unit/*.py | head -8; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/baj6mx6th.output | tail -5; git diff d19ae46 HEAD --stat | tail -3; git rev-parse HEAD; sed -n 1,60p memory/contracts/api.md | grep -n \"40 |\"; git show d19ae46 -- memory/contracts/api.md | head -60"
}
````

### User / tool · 2026-11-02T13:36:55.615Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_api_routes.py:21:    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_api_routes.py:320:def test_local_mode_refuses_non_loopback_host(tmp_path, monkeypatch, host, ok):
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t148r1/head/tests/unit/test_api_routes.py:347:def test_local_mode_refuses_non_loopback_peer_by_address(tmp_path, monkeypatch):
 tests/e2e/test_conflict_coverage.py                | 100 ++++++++++++++
 tests/e2e/test_edit_to_check.py                    | 143 ++++++++++++++++++++-
 12 files changed, 398 insertions(+), 16 deletions(-)
07c75583828883089d3dbfbece5587006bab7618
commit d19ae46e0f39a256b359a84ac1283cafb2427d47
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:33:44 2026 -0600

    feat(backend): GET /api/cases summary list for the case overview (T-148)
    
    Per case: readable title, created/updated, run stage, decided/total per kind, HITL call-outs
    (needs review, edits to check, could-not-verify tray, gate blockers and warnings), export_ready.
    Computed from the functions GET case, /status and the export gate use; test compares all of them for every library case.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 1fb8080..5c66eeb 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -683,7 +683,18 @@ Run the second check again for the AI-made items whose judge never answered (the
 
 ## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
 Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays token-only and has no case list.
-`GET /api/cases` -> `{ "cases": [ { "token", "name", "status", "source", "record_count", "counts": {"pending","accepted","edited","dismissed","needs_review"}, "created_at" } ] }`, newest first, never record text.
+`GET /api/cases` (T-148, the overview screen) -> `{ "cases": [ summary ] }`, newest first (`created_at`, then insertion order); every case the single local profile can see. Code only: no model call, no pipeline run, no record text. Local mode only: no auth, no users, no sharing (scope cut kept). One `summary`:
+```
+{ "token": "...", "title": "Er only then gap", "name": "case lib01 er only then gap" | null, "source": "paste|sample", "status": "ingested|running|ready|failed",
+  "record_count": 9, "created_at": "...Z", "updated_at": "...Z", "last_activity_at": "...Z",
+  "run": { "stage": "finalize" | "ingest" | null, "steps_done": 7, "steps_total": 8, "running": false, "error": false },
+  "progress": { "entries": {"decided": 2, "total": 5}, "flags": {"decided": 0, "total": 2}, "amounts": {"decided": 0, "total": 2} },
+  "counts": { "pending", "accepted", "edited", "dismissed", "needs_review" },
+  "hitl": { "pending": 7, "needs_review": 4, "edits_to_check": 0, "could_not_verify": 1,
+            "gate_blockers": [ { "reason_code", "kind", "item_id", "why" } ], "gate_warnings": [ { "reason_code", "count", "why" } ] },
+  "export_ready": true }
+```
+`title` is what to show: the case name made readable (a file name or slug such as `smith_records-2024.pdf` becomes "Smith records 2024", the `case_lib01_` library prefix is dropped), or "Untitled case, Nov 2" / "Sample case" when it has no name; `name` is the stored value. `updated_at` is the same value as `GET /api/cases/{token}` (`run_finished_at`, else `created_at`); `last_activity_at` also counts the latest accept/edit/dismiss. `run` is `/status` (`stage`, `progress.done`, `progress.total`). `progress` counts the live items `review.counts` counts (not rejected, no answered tray placeholder, no rule-filtered proposal): `decided` = accepted, edited or dismissed, and a reworded entry still marked Needs review is NOT decided (T-134); `total - decided` over the three kinds = `hitl.pending + hitl.edits_to_check`. `hitl.needs_review` / `edits_to_check` / `pending` are `GET /api/cases/{token}` `review.counts` (`needs_review`, `edit_to_check`, `pending`); `could_not_verify` is the length of that case's `tray`. `gate_blockers` / `gate_warnings` are the `blockers` / `warnings` of the `export_gate` step of `GET /api/cases/{token}/trace` (same `reason_code` and plain `why`; the blockers are exactly what makes `GET .../export` answer 422), and `export_ready` is the gate's `ready`. A case with warnings only (items not reviewed, edits to check) is `export_ready: true`. `tests/unit/test_case_list.py` compares every field with those routes for every library case.
 `GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
 `POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:00.637Z

**tool call — Bash**
````
{
 "command": "git diff d19ae46 HEAD --stat -- app/backend/case_list.py app/backend/present.py app/backend/api.py app/backend/trace.py tests/unit/test_case_list.py | tail -4; git rev-parse HEAD"
}
````

### User / tool · 2026-11-02T13:37:00.791Z

**tool result**
````
07c75583828883089d3dbfbece5587006bab7618
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:06.887Z

**tool call — Bash**
````
{
 "command": "sed -n 345,365p tests/unit/test_api_routes.py; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/baj6mx6th.output | tail -5"
}
````

### User / tool · 2026-11-02T13:37:06.972Z

**tool result**
````
def test_local_mode_refuses_non_loopback_peer_by_address(tmp_path, monkeypatch):
    """D-036: peer address, not the HOST env var, gates local mode (covers `uvicorn --host 0.0.0.0`)."""
    monkeypatch.setenv("LLM_BACKEND", "fixture"); monkeypatch.setenv("ZLAYT_MODE", "local"); monkeypatch.delenv("HOST", raising=False)
    app = create_app(str(tmp_path / "p.sqlite"), static_dir=str(tmp_path))
    for peer in ("127.0.0.1", "127.0.0.5", "::1", "::ffff:127.0.0.1"):
        assert TestClient(app, client=(peer, 5000)).get("/api/cases").status_code == 200, peer
    for peer in ("192.168.1.5", "10.0.0.2", "<redacted-private>", "0.0.0.0", "testclient"):
        r = TestClient(app, client=(peer, 5000)).get("/api/cases")
        assert r.status_code == 403 and r.json()["error"]["code"] == "forbidden", peer
        assert TestClient(app, client=(peer, 5000)).get("/api/health").status_code == 403
    monkeypatch.delenv("ZLAYT_MODE")                                    # public build: no peer restriction
    assert TestClient(app, client=("192.168.1.5", 5000)).get("/api/health").status_code == 200


def test_side_or_negation_edit_is_a_422_with_plain_reason_and_confirm_flag_changes_nothing_d047(env):
    _, c = env
    tok = run_case(c)
    e5 = [e for e in c.get(f"/api/cases/{tok}").json()["entries"] if e["provider"].startswith("Capital PT, visit 8")][0]
    before = c.get(f"/api/cases/{tok}").json()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:09.599Z

**tool call — Bash**
````
{
 "command": "sleep 100; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/baj6mx6th.output | tail -5; ps aux | grep -c \"[p]ytest tests/unit\"",
 "timeout": 130000
}
````

### User / tool · 2026-11-02T13:37:09.601Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 100 followed by: cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/baj6mx6th.output tail -5 ps aux grep -c "[p]ytest tests/unit". To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:37:13.768Z

**tool call — Bash**
````
{
 "command": "until ! pgrep -f \"pytest tests/unit -q\" >/dev/null; do sleep 3; done; tail -6 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/baj6mx6th.output",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T13:47:04.561Z

**tool result**
````
Command did not complete within its 590s timeout and was moved to the background (ID: bd4b5b1sd). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bd4b5b1sd.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:09.585Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/baj6mx6th.output | tail -8"
}
````

### User / tool · 2026-11-02T13:47:09.688Z

**tool result**
````
........................................................................ [ 91%]
.........................................................ss............. [ 93%]
........................................................................ [ 94%]
........................................................................ [ 96%]
........................................................................ [ 98%]
................................................                         [100%]

[exited with code 0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:12.531Z

**tool call — Bash**
````
{
 "command": "grep -n \"last_activity_at\\\"\\] > first\\|first\\[\\\"last_activity_at\\\"\\] >\\|\\\"running\\\"\\] ==\\|bool(case.get\" tests/unit/test_case_list.py app/backend/case_list.py; ls reviews/T-148* 2>&1 | head -2"
}
````

### User / tool · 2026-11-02T13:47:12.602Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to  first\|first\["last_activity_at"\] >\|"running"\] ==\|bool(case.get)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:15.367Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_case_list.py",
 "offset": 88,
 "limit": 6
}
````

### User / tool · 2026-11-02T13:47:15.381Z

**tool result**
````
88	        assert s["run"]["stage"] == st["stage"] and s["run"]["steps_done"] == st["progress"]["done"] and s["run"]["steps_total"] == st["progress"]["total"], lid
89	        assert s["run"]["running"] == (case["status"] == "running"), lid
90	        # review counts and the could-not-verify tray: the case screen
91	        rc = case["review"]["counts"]
92	        h = s["hitl"]
93	        assert h["needs_review"] == rc["needs_review"] and h["edits_to_check"] == rc["edit_to_check"] and h["pending"] == rc["pending"], lid
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:17.575Z

**tool call — Bash**
````
{
 "command": "grep -n 'assert sum(v\\[\"decided\"\\]' tests/unit/test_case_list.py | head -3; ls reviews | grep T-148"
}
````

### User / tool · 2026-11-02T13:47:17.673Z

**tool result**
````
115:    assert sum(v["decided"] for v in first["progress"].values()) >= 1 and first["last_activity_at"] > first["updated_at"] or first["last_activity_at"] >= first["updated_at"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:38.395Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-148-staff-engineer.md",
 "content": "# T-148 review: staff-engineer-reviewer\n\nVerdict: pass (no blocker, no major; two minors, both about test strength, not product behaviour).\n\nScope: commit d19ae46 (`app/backend/case_list.py`, `api.py` route and `/status` hunk, `memory/contracts/api.md`, `tests/unit/test_case_list.py`). I exercised a `git archive HEAD` copy. HEAD is 07c7558; `git diff d19ae46 HEAD --stat` over case_list.py, present.py, api.py, trace.py and test_case_list.py is empty, so nothing in scope moved.\n\n- Drift: every summary field is derived from `present.review_view`, `run_progress` (shared with `/status`) and the `export_gate` step of `trace.case_trace`. I mutated `case_list.py` 14 ways on a scratch copy. 11 turned the test red (edit_unconfirmed, rejected filter, tray count, needs_review, export_ready forced True, warnings dropped, blocker `why` dropped, edits_to_check wrong source, ingest stage fallback, steps_total, plus the ready/warning cases). Survivors: `handled` and `is_filtered` filters (equivalent mutants: handled placeholders and filtered flags are already `state == \"rejected\"`, which `_progress` excludes), `run.running` and `run.error` (see F1).\n- HITL call-outs: needs_review, edits_to_check, could_not_verify (= GET case `tray` length), blockers and warnings carry the trace's plain `why`. A failed case shows blockers `RUN_FAILED, NOTHING_ACCEPTED` and `/export` answers 422; a running case shows `RUN_IN_PROGRESS`; the two agree with the gate.\n- Local mode: 404 outside `ZLAYT_MODE=local`; the D-036 middleware returns 403 for a non-loopback peer (probe: peer 203.0.113.9 gave 403 `forbidden`; `::1` gave 200); `tests/unit/test_api_routes.py:347` covers this on `/api/cases`.\n- Performance and LLM: 50 cases (15 run, 35 ingested) listed in 91-100 ms; audit call counts for three cases unchanged by the list call; no pipeline or model import on the path.\n- Old fields: token, name, status, source, record_count, counts, created_at all present; `app/frontend/switcher.js` reads exactly those.\n\n```json\n{\"card\": \"T-148\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit d19ae46 (HEAD 07c7558, no in-scope diff since): app/backend/case_list.py, api.py list route and /status hunk, memory/contracts/api.md, tests/unit/test_case_list.py; git archive HEAD copy; 15 library cases under the fixture backend, local mode\",\n \"exercised\": [\n  \"python3 tools/board.py show T-148; read memory/contracts/api.md GET /api/cases section; git show d19ae46 for case_list.py and api.py\",\n  \"git archive HEAD into a scratch dir; .venv/bin/python -m pytest tests/unit/test_case_list.py -q -> 7 passed in 3.05s\",\n  \"full tests/unit on the archive: pytest tests/unit -q -x, exit code 0 (2 skips, no failures)\",\n  \"14 single-line mutants of case_list.py on a scratch copy, each followed by test_case_list.py (11 red; handled and is_filtered are equivalent, run.running and run.error survive)\",\n  \"scripted probe on the archive: 15 library cases run, GET /api/cases vs GET case tray length (equal for all 15), error flag false\",\n  \"50-case list timing (3 runs): 100, 91, 93 ms; audit calls for 3 cases identical before and after the list call\",\n  \"peer probes: 203.0.113.9 -> 403 forbidden; ::1 -> 200; ZLAYT_MODE unset -> 404\",\n  \"scripted failed case (status failed + error set) and running case: blockers RUN_FAILED / RUN_IN_PROGRESS and /export 422\",\n  \"read app/frontend/switcher.js for the old fields it consumes; read present.review_view, present tray build, flags._to_tray, generator.resolved_placeholders\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"determinism_and_no_llm\": 5, \"drift_resistance\": 4, \"hitl_honesty\": 4, \"local_mode_gating\": 5, \"test_strength\": 3, \"backward_compat\": 5},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"Test does not pin run.running or run.error; one assertion cannot fail\",\n   \"evidence\": \"Mutating case_list.py `\\\"running\\\": case[\\\"status\\\"] == \\\"running\\\"` to False, and `\\\"error\\\": bool(case.get(\\\"error\\\"))` to False, both leave all 7 tests green (7 passed). tests/unit/test_case_list.py:89 compares running with the same expression on the same field and no test reads GET case `error` against run.error. tests/unit/test_case_list.py:115 is `A and B or C`, where C (`last_activity_at >= updated_at`) is already asserted at line 87, so the line cannot fail for the decisions it names.\",\n   \"why_it_matters\": \"A failed case is the one a paralegal most needs flagged on the overview; the failed-run flag is the field a drift would hit and nothing would notice. The weak line gives false comfort that decisions move last_activity_at.\",\n   \"fix\": \"Add a failed case (set status/error through the store, as the probe did) and a running case to the fixture set; assert run.error == bool(GET case error) and run.running == (GET /status status == running). Replace line 115 with two plain asserts: the case that took decisions has last_activity_at > updated_at, and the untouched case has last_activity_at == updated_at.\",\n   \"acceptance_test\": \"Mutants `running -> False` and `error -> False` in case_list.py turn tests/unit/test_case_list.py red; line 115 fails if last_activity_at is not advanced by a review event.\"},\n  {\"severity\": \"minor\", \"title\": \"No case with a manual-entry-handled placeholder or a rule-filtered proposal in the comparison set\",\n   \"evidence\": \"Removing the `handled` or `FT.is_filtered` clause from `_progress` (case_list.py) leaves 7 passed. They are equivalent today because both kinds of item are `state == rejected`, but if either stops being rejected the list would count them in progress totals and nothing in test_case_list.py would show it; the 15 library cases under the fixture backend contain neither.\",\n   \"why_it_matters\": \"The two clauses duplicate present.review_view's filter, so they can drift the day one changes; the comparison only protects the cases the fixture produces.\",\n   \"fix\": \"Either drop the redundant clauses and compute total from present.review_view's own item set (one source), or add a case with a T-110 manual entry over a placeholder and a D-057 filtered flag (tests/unit/test_lib09_t110_r2.py and test_t126_filtered_by_rule.py already build them) to the comparison.\",\n   \"acceptance_test\": \"A test builds a case with a handled placeholder and a filtered flag and asserts progress totals equal GET case live item counts and hitl.could_not_verify equals len(tray).\"}\n ],\n \"whats_right\": [\n  \"Fields come from the functions GET case, /status and the export gate already use (run_progress is shared with the /status route), and the test compares them route by route for all 15 library cases.\",\n  \"Gate blockers and warnings are copied from the trace with their plain `why`, and export_ready agrees with GET /export (200 vs 422) in every state I probed, including failed and running.\",\n  \"Code only, about 100 ms for 50 cases, 403 for non-loopback peers, and all pre-existing list fields kept for switcher.js.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T13:47:38.556Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-148-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:41.226Z

T-148 gets verdict **pass**: no blockers or majors, two minors. Review is at `/Users/arsis/zlayt-pm-project/reviews/T-148-staff-engineer.md`.
- **Tests and checks:** the full unit suite exits 0 on the `git archive HEAD` copy (2 skips). 11 of 14 mutants turned the drift comparison red. The other 3 are not detected: `run.running`, `run.error` and an unused filter clause, which are the two minors (the test never checks the failed-run and running flags, and one `last_activity_at` assertion cannot fail). The other points hold: 50 cases list in about 100 ms with no model calls, non-loopback peers get 403, and the old fields are still present.
