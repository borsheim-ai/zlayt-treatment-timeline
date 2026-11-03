# Subagent: Frontend: T-081 stepper + T-082 judge panel (Frontend: T-081 stepper + T-082 judge panel)

Source: `agent-ae25cdb9583acdf08.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:22:13.445Z

You own board cards T-081 and T-082 (both P0, claimed by "frontend") in /Users/arsis/zlayt-pm-project. Run `board.py show` on each and read D-042 in memory/ORCHESTRATOR_DECISIONS.md. Chris's words: "<Chris's message omitted>."

**Data:** the API is ready (T-080, commit e3cea6f). See the "Check traces (D-042)" section of memory/contracts/api.md: `/api/cases/{token}/items/{id}/trace`, `/api/cases/{token}/trace` and `/api/cases/{token}/judges`.

**Pattern reference** (read it, don't copy Streamlit): <home-path>
- `_render_flow_rail_html` (about line 2149) and its CSS around `.flow-rail` (about line 964): a vertical rail of nodes, each with a status marker glyph, label, detail and note, plus a header with "x/y done" progress and a verdict line;
- also UX_AUDIT.md in that folder.

**T-081 — vertical stepper component** (vanilla JS, textContent only, matching app/frontend conventions):
- **Item level:** inside each item's Why panel, show steps such as extracted (AI), each code check, judge 1 or 2 (AI check), and your decision. Each step shows:
  - a status marker: pass ✓, fail ✕, skipped –, or pending ○, never colour alone;
  - a label and a kind chip (Code / AI check / You);
  - the plain-words why and the evidence, such as the quoted excerpt and the judge reason;
  - on fail or pending, a "What you need to do" line with an action button where one exists.
- **Case level:** a case stepper in the case header or a side rail covering ingest → split → dates → extract → grounding → judges → flags → totals → review → export gate, with counts and "x/y passed".
- **Export gate:** list each blocker with a jump link to the item.

**T-082 — "How the AI was checked" panel** on the case:
- items judged; supported, unsupported and unavailable counts;
- each rejection with its reason, linking to the item stepper;
- the judge model and prompt version;
- code-vs-judge disagreements.
- Label it clearly as AI quality checks, never as a verdict on the case.

**Requirements:**
- keyboard and screen-reader accessible (an ordered list with aria-current on the active step);
- usable at 390px;
- matches the existing visual style; T-060 (enterprise polish) comes later, so keep the components token-based.

Add e2e tests in tests/e2e and declare any new test ids in tests/e2e/conftest.py; tests/unit/test_e2e_contract.py must stay green. Use your own instance on a spare port (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local), and take screenshots to artifacts/screenshots/stepper-*.png and judge-panel-*.png at 1440px and 390px. Commit with the pathspec rule, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". For each card run `board.py ac`, the handoff, and `move in_review --agent frontend`. Reply in 3 lines.

### User / tool · 2026-11-02T03:22:13.450Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:16.849Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-081; python3 tools/board.py show T-082; grep -n \"D-042\" -A25 memory/ORCHESTRATOR_DECISIONS.md | head -60; cat .claude/agent-memory/frontend/MEMORY.md; ls app/frontend tests/e2e"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:16.854Z

**tool call — Bash**
````
{
 "command": "grep -n \"Check traces\" -A80 memory/contracts/api.md | head -150"
}
````

### User / tool · 2026-11-02T03:22:17.078Z

**tool result**
````
<outside-repo file omitted>
````

### User / tool · 2026-11-02T03:22:17.179Z

**tool result**
````
454:## Check traces (D-042): per-item stepper, case stepper, judge summary
455-Three read-only GETs that feed the vertical steppers (pattern: <outside project> flow rail: each node has a status, label, detail and note, plus an overall progress count and a verdict). Everything is derived from data already stored (ladder, review status, `llm_calls`, `review_events`, case config); nothing is recomputed by a model. `404 not_found` for an unknown token or item.
456-
457-**Visibility (same split as `/audit`, D-020/D-036).** Public/demo = **metadata only**. `ZLAYT_MODE=local` = **full**. Both modes return `"mode": "metadata" | "full"`. Metadata mode returns: model id, backend, prompt version and hash, call id, verdict, latency, closed reason codes and their fixed sentences, counts, the item's own excerpt spans and text (the case view already shows them), and the action and time of each human event. **Full mode adds, per step:** `evidence.response_raw` (the model's raw answer for an LLM step), and for the human step `evidence.events[].before/after` and `evidence.edited_text`. Prompt text (`system_text`/`user_text`) is **never** in a trace; use `/audit` in local mode. The frontend must not assume the full-only keys exist.
458-
459-**Judge rationale is a closed reason code plus a fixed sentence (D-028).** The judge returns `verdict` + `reason_code` from a closed list, never prose, so `rationale` is the fixed sentence for that code (`why.judge_detail`), written by code. `reason_code` is read from `ladder.judge.reason_code`; for items stored before it was kept (amounts, edits, manual entries) it is read from the audited call's answer.
460-
461-### Step (shared by all three endpoints)
462-```json
463-{ "id": "summary_tokens", "n": 5, "label": "Numbers and dates in the summary are in the quote",
464-  "kind": "code",                       // "code" | "llm" | "human"
465-  "status": "pass",                     // "pass" | "fail" | "skipped" | "pending"
466-  "why": "Every number, date, dollar figure and left/right/no/not/without in the summary is in the quote.",
467-  "reason_code": null,                  // closed code when status is fail, or when a pass still explains a state (e.g. AMOUNT_RATE_NOT_TOTALED); else null
468-  "rule": "D-034",                      // decision or LLM_VS_CODE row behind the check, or null
469-  "blocks_export": false,               // true only for steps that stop this item reaching the letter right now (human pending, date unconfirmed)
470-  "evidence": { },                      // see below; keys are present only when they apply
471-  "next_action": null }                 // object when status is "fail" or "pending", else null
472-```
473-`status` meaning: `pass` the check ran and passed (or the human decided to accept); `fail` the check ran and found a problem (the item is then `needs_review` or `rejected`); `skipped` not run on purpose (a step before it already rejected the item, no judge applies to code-made items, the judge did not answer, or the human dismissed it) and `why`/`reason_code` say which; `pending` not done yet (the AI run has not reached this step, or the human has not decided).
474-
475-`next_action`: `{"code": "CONFIRM_DATE", "text": "Choose the right reading under Dates to confirm. Until you do, this entry cannot be accepted.", "target": {"record_id": "r4", "view": "dates_to_confirm"}, "options": ["accept","edit","dismiss"]}`. `code` is closed: `DECIDE`, `CONFIRM_DATE`, `EDIT_SUMMARY`, `EDIT_QUOTE`, `READ_RECORD`, `COMPARE_BY_HAND`, `DISMISS_OR_ENTER_BY_HAND`, `RERUN`, `SENTENCE_REMOVED` (narrative sentence left out of the draft), `CONFIRM_RERUN`. `text` is a fixed sentence written by code; `target` and `options` are optional.
476-
477-`evidence` keys (all optional): `excerpt` `{record_id, start, end, text}` (offsets absolute into the case text); `spans[]` (same shape, for flags); `tokens[]` (summary tokens not in the quote); `values` (small object, for example `{"text": "$6,240", "value_cents": 624000, "kind": "charge", "classified_by": "code:amounts"}` or a gap's `{"from","to","days","threshold"}`); `date` `{record_id, date_raw, date_iso, date_status, candidates[]}`; `model` `{id, role, independent_of_generator}`; `prompt_version`; `prompt_sha256`; `call_id`; `backend`; `recorded_from`; `latency_ms`; `parsed_ok`; `judge_verdict` (ladder vocabulary: `supported|partially|unsupported|disagrees|unsure|unavailable`); `judge_reason_code` (the judge's own closed code, for example `NUMBER_MISMATCH`, or `NONE`); `rationale` (fixed sentence for that code); `action`, `at`, `events[]` `{action, at}` (human step); `response_raw`, `events[].before/after`, `edited_text` (**full mode only**).
478-
479-### GET /api/cases/{token}/items/{item_id}/trace
480-```json
481-{ "token": "k3Jf9x...", "item_id": "e4", "kind": "entry", "mode": "metadata",
482-  "state": "needs_review", "review_status": "pending",
483-  "state_reasons": [ {"code": "JUDGE_PARTIAL", "why": "A second AI check found the summary only partly supported by the quoted text.", "step_id": "judge_1"} ],
484-  "verdict": { "code": "needs_attention", "label": "Needs your attention", "blocks_export": true },
485-  "progress": { "done": 10, "total": 11, "label": "10 of 11 steps settled" },
486-  "next_action": { "code": "COMPARE_BY_HAND", "text": "...", "target": {"item_id": "e4"} },
487-  "steps": [
488-    { "id": "extracted", "n": 1, "label": "AI drafted a summary and picked a quote", "kind": "llm", "status": "pass",
489-      "why": "The AI read this record and proposed a one-line summary and a quote.", "reason_code": null, "rule": "row 4", "blocks_export": false,
490-      "evidence": { "model": {"id": "claude-sonnet-5-5", "role": "generator", "independent_of_generator": null},
491-                    "prompt_version": "extract_v1", "prompt_sha256": "9f2c0a77", "call_id": "c18", "backend": "fixture",
492-                    "latency_ms": 5120, "parsed_ok": true, "excerpt": {"record_id": "r4", "start": 858, "end": 928, "text": "..."} }, "next_action": null },
493-    { "id": "judge_1", "n": 9, "label": "Second AI check: is the summary supported by the quote?", "kind": "llm", "status": "fail",
494-      "why": "A second AI check found the summary only partly supported by the quoted text. The summary leaves out a qualifier that the quote carries.",
495-      "reason_code": "JUDGE_PARTIAL", "rule": "row 4", "blocks_export": false,
496-      "evidence": { "model": {"id": "claude-haiku-5-5", "role": "judge", "independent_of_generator": true}, "prompt_version": "judge_faithfulness_v1",
497-                    "call_id": "c27", "judge_verdict": "partially", "judge_reason_code": "DROPS_QUALIFIER",
498-                    "rationale": "The summary leaves out a qualifier that the quote carries." },
499-      "next_action": { "code": "COMPARE_BY_HAND", "text": "..." } } ] }
500-```
501-**Steps by item kind, in order** (ids; a step that does not apply is omitted, not skipped, except where noted):
502-- **entry (and a reviewer-written entry):** `extracted` (llm; a reviewer-written entry shows kind `human` and no model), `excerpt_verbatim` (code, `GROUNDING_EXCERPT_NOT_VERBATIM`), `excerpt_whole_sentence` (code, `EXCERPT_NOT_WHOLE_SENTENCE`), `excerpt_hedge` (code, `EXCERPT_OMITS_QUALIFIER`), `summary_tokens` (code, D-034, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `evidence.tokens`), `summary_qualifier` (code, D-022, `SUMMARY_DROPS_QUALIFIER`), `highlight` (code, `HIGHLIGHT_NOT_FOUND`), `date_confirmed` (code, D-041, `DATE_AMBIGUOUS`/`DATE_MISSING`, `blocks_export`), `injection_scan` (code, `INJECTION_SUSPECTED`), `judge_1` (llm), `human`. If the quote fails the word-for-word check or the AI output was malformed, the checks between `extracted` and `highlight` and `judge_1` are `skipped` with that code.
503-- **amount:** `found_in_text` (code, `GROUNDING_AMOUNT_NOT_IN_TEXT`), `amount_class` (code; pass for a charge; pass with `reason_code` `AMOUNT_RATE_NOT_TOTALED`/`AMOUNT_ESTIMATE`/`AMOUNT_DAMAGES` for the classes that are never totaled; fail for `AMOUNT_UNCLEAR`), `injection_scan`, `judge_2` (llm; `skipped` for damages, which are not judged), `total_inclusion` (code: pass when it is an accepted charge counted in the total, pending when a charge is undecided, skipped when it is not a charge or was dismissed), `human`.
504-- **flag, code-made (gap, accident-date or provider conflict):** `computed` (code, `evidence.values` has the dates and days), `spans_match` (code), `endpoints_confirmed` (code, `ENDPOINT_NOT_VERIFIED`), `judge_not_needed` (skipped: arithmetic over dates needs no judge), `human`.
505-- **flag, phrase list and/or AI (pre-existing, causation incl. credibility wording D-038/D-043, AI-proposed conflicts):** `proposed_by_phrase_list` (code; skipped with `LLM_ONLY` when only the AI found it), `proposed_by_ai` (llm; skipped with `LEXICON_ONLY` when only the phrase list found it), `agreement` (code: pass when both, fail with `LEXICON_ONLY`/`LLM_ONLY`), `credibility_wording` (code, only for category `credibility_language`: the sentence has a credibility term and is not a clean negation, D-043), `excerpt_verbatim` (code), `highlight` (code), `injection_scan` (code), `judge_4` (llm) or `judge_3` (llm, for a conflict the AI proposed); `skipped` when only the phrase list found the flag (`LEXICON_ONLY`), `human`.
506-- **flag, record warning:** `record_warning_check` (code; the category in `evidence.values.category`), `human`.
507-- **narrative sentence (`ns1`…, kept or removed):** `extracted` (llm), `cites_accepted_entry` (code, `NOT_AN_ACCEPTED_ENTRY`), `sentence_checks` (code: numbers/dates D-006, qualifiers D-022, no unquoted causation, severity or flag wording; failing codes are in `evidence.reasons`), `judge_1` (llm), `human` (the decision on the whole paragraph). A removed sentence has `status: "fail"` on the step that removed it and later steps `skipped`; `kind` is `narrative_sentence`; the item `verdict.code` is `removed`.
508-
509-`verdict.code`: `accepted` (accepted or edited), `dismissed`, `rejected` (state rejected, kept out of the letter), `needs_attention` (any `fail` step on a live item), `ready_for_decision` (all machine steps pass or are skipped on purpose, human pending), `removed` (narrative sentence only), `waiting_for_run` (AI steps not run yet). `verdict.blocks_export` is true when the item is live and `review_status` is `pending` (it is what `/trace`'s export gate lists). `progress.done` counts steps that are not `pending`.
510-
511-### GET /api/cases/{token}/trace
512-```json
513-{ "token": "k3Jf9x...", "mode": "metadata", "status": "ready",
514-  "verdict": { "code": "needs_attention", "label": "12 items still need your decision" },
515-  "progress": { "done": 8, "total": 10, "label": "8 of 10 steps settled" },
516-  "steps": [
517-    { "id": "ingest", "n": 1, "label": "Read the paste and split it into records", "kind": "code", "status": "pass",
518-      "why": "9 records found.", "reason_code": null, "rule": "row 1",
519-      "counts": {"records": 9, "duplicates_merged": 0, "characters": 4120}, "evidence": {}, "next_action": null },
520-    { "id": "split", "n": 2, "label": "Record boundaries", "kind": "code", "status": "pass", "counts": {"method": "code", "llm_split": false}, "...": "..." },
521-    { "id": "dates", "n": 3, "label": "Dates read by code", "kind": "code", "status": "fail", "reason_code": "DATE_AMBIGUOUS",
522-      "counts": {"parsed": 7, "confirmed": 0, "ambiguous": 1, "missing": 1},
523-      "next_action": {"code": "CONFIRM_DATE", "text": "...", "target": {"view": "dates_to_confirm"}} },
524-    { "id": "extract", "kind": "llm", "counts": {"records_to_draft": 9, "entries": 8, "rejected": 0, "records_without_entry": 1} },
525-    { "id": "grounding", "kind": "code", "counts": {"items_checked": 20, "rejected": 1, "reasons": {"GROUNDING_EXCERPT_NOT_VERBATIM": 1}} },
526-    { "id": "judges", "kind": "llm", "counts": {"items_judged": 18, "supported": 15, "unsupported": 2, "unsure": 0, "unavailable": 1} },
527-    { "id": "flags", "kind": "code", "counts": {"total": 4, "by_type": {"gap": 1}, "by_origin": {"code": 2, "llm": 1}} },
528-    { "id": "totals", "kind": "code", "counts": {"accepted_cents": 0, "pending_cents": 839000, "pending_charges": 2, "not_totaled": 1} },
529-    { "id": "review", "kind": "human", "counts": {"pending": 21, "accepted": 0, "edited": 0, "dismissed": 0} },
530-    { "id": "export_gate", "n": 10, "label": "Ready to export?", "kind": "code", "status": "fail", "reason_code": "ITEMS_PENDING",
531-      "why": "21 items have no decision yet, so the export is blocked.", "ready": false,
532-      "counts": {"blocking": 21, "accepted": 0, "rejected_not_blocking": 1},
533-      "blockers": [ { "item_id": "e4", "kind": "entry", "reason_code": "DATE_UNCONFIRMED", "why": "...", "next_action": {"code": "CONFIRM_DATE", "text": "..."} } ],
534-      "next_action": {"code": "DECIDE", "text": "..."} } ] }
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:19.395Z

**tool call — Bash**
````
{
 "command": "sed -n 534,600p memory/contracts/api.md; cat .claude/agent-memory/frontend/project_t043_panels.md; wc -l app/frontend/*.js app/frontend/*.css app/frontend/index.html; cat tests/e2e/conftest.py | head -150"
}
````

### User / tool · 2026-11-02T03:22:19.526Z

**tool result**
````
      "next_action": {"code": "DECIDE", "text": "..."} } ] }
```
Each case step has the shared step keys plus `counts` (object, may be `{}`); `export_gate` also has `ready` and `blockers[]`. Step order is fixed: `ingest, split, dates, extract, grounding, judges, flags, totals, review, export_gate`. Before the AI run (`status: "ingested"`) `extract`, `grounding`, `judges` and `flags` (AI part) are `pending`; the code-made flags and amounts already count.

`verdict.code` for the case: `ready` (export gate open), `needs_attention` (items still need a decision, or nothing accepted yet), `running`, `failed`. The judge's closed `reason_code` is now kept in `ladder.judge.reason_code` for entries, amounts, flags, edits and manual entries (in `ladder_json`; no schema change).

**Export gate (exact).** `ready` equals `review.ready_to_export` from the case view, and is false while a run is in progress. `blockers[]` has one element for every **live** (state not `rejected`) entry, amount or flag whose `review_status` is `pending`, with `reason_code` `DATE_UNCONFIRMED` (an entry whose date is not confirmed, D-041, and which cannot be accepted until it is) or `PENDING_DECISION`; plus case-level elements (`item_id: null`) `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `NOTHING_ACCEPTED` (nothing accepted or edited yet, so the letter would be empty). Rejected items never block; they are counted in `counts.rejected_not_blocking`. A dismissed item never blocks.

### GET /api/cases/{token}/judges
```json
{ "token": "k3Jf9x...", "mode": "metadata", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}, "independent_models": true,
  "totals": { "items_judged": 18, "supported": 15, "unsupported": 2, "unsure": 0, "unavailable": 1, "human_overrides": 1 },
  "judges": [ { "id": "j1", "label": "Is the summary supported by the quote?", "prompt_version": "judge_faithfulness_v1", "models": ["claude-haiku-5-5"],
                "items": 9, "supported": 8, "partially": 1, "unsupported": 0, "disagrees": 0, "unsure": 0, "unavailable": 0 },
              { "id": "j2" }, { "id": "j3" }, { "id": "j4" } ],
  "rejections": [ { "item_id": "e4", "kind": "entry", "judge": "j1", "verdict": "partially", "reason_code": "DROPS_QUALIFIER",
                    "rationale": "The summary leaves out a qualifier that the quote carries.", "state_reason": "JUDGE_PARTIAL",
                    "model": "claude-haiku-5-5", "prompt_version": "judge_faithfulness_v1", "call_id": "c27", "review_status": "pending" } ],
  "unresolved": [ { "item_id": "a2", "kind": "amount", "judge": "j2", "verdict": "unavailable", "state_reason": "JUDGE_UNAVAILABLE", "model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": null } ],
  "disagreements": [ { "item_id": "a3", "kind": "amount", "type": "judge_objects", "code_says": "charge", "judge_says": "rate (SHOULD_BE_RATE)", "resolution": "needs_review", "review_status": "pending" } ],
  "prompt_versions": ["judge_amount_class_v1", "judge_faithfulness_v1"] }
```
`totals.unsupported` = partially + unsupported + disagrees (the judge objected); `items_judged` = items whose judge answered (every verdict except `unavailable`). `rejections` = every objection, with the fixed-sentence `rationale`; `unresolved` = `unsure` and `unavailable`. `disagreements[]` (code vs judge): `judge_objects` (every code check passed and the judge objected: `code_says` is the check summary, for an amount the rule's class), `judge_agrees_code_flags` (code raised a doubt (token, qualifier, date) and the judge found it supported; the item stays `needs_review`), `sources_disagree` (flag: the phrase list and the AI disagree, `LEXICON_ONLY`/`LLM_ONLY`). `human_overrides` counts items accepted or edited although a judge objected. Counts cover live and rejected items; narrative sentences are not included. The same visibility split applies (no raw responses in metadata mode; `rejections[].response_raw` is full-mode only).

## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays token-only and has no case list.
`GET /api/cases` -> `{ "cases": [ { "token", "name", "status", "source", "record_count", "counts": {"pending","accepted","edited","dismissed","needs_review"}, "created_at" } ] }`, newest first, never record text.
`GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
`POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).

## DELETE /api/cases/{token}
`204`. Removes the case, records, items, calls and events. It is the same function the 24 h purge uses and deletes from every table by case id, including stored prompts (ADR-006).

---

## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
| Code | State | Meaning |
|---|---|---|
| `GROUNDING_EXCERPT_NOT_VERBATIM` | rejected | model's excerpt is not word for word in the record |
| `GROUNDING_AMOUNT_NOT_IN_TEXT` | rejected | model reported an amount the record does not contain |
| `SCHEMA_INVALID` | rejected | model output failed schema validation after retries |
| `SUMMARY_TOKEN_NOT_IN_EXCERPT` | needs_review | a number, date, dollar figure or left/right/no/not/without in the summary (or an edit) is not in the quote |
| `SUMMARY_DROPS_QUALIFIER` | needs_review | the excerpt has a hedge, self-report marker, negation, laterality or "approx." that the summary leaves out (D-022) |
| `EXCERPT_OMITS_QUALIFIER` | needs_review | the record has a hedge sentence the excerpt leaves out |
| `EXCERPT_NOT_WHOLE_SENTENCE` | needs_review | the excerpt starts or ends mid-sentence |
| `HIGHLIGHT_NOT_FOUND` | needs_review | the quote cannot be located in the raw text for highlighting |
| `JUDGE_PARTIAL` / `JUDGE_UNSUPPORTED` | needs_review | judge 1 found the summary partly or not supported |
| `JUDGE_DISAGREES` / `JUDGE_UNSURE` | needs_review | judge 2, 3 or 4 disagreed or could not decide |
| `JUDGE_UNAVAILABLE` | needs_review | the judge call failed or timed out, or (always in demo mode) an edit has no recorded judge answer |
| `FIXTURE_MISS` | needs_review | the demo has no recorded model answer for this call; never retried |
| `DATE_AMBIGUOUS` / `DATE_MISSING` | needs_review | date has two readings or is absent; excluded from gap math until confirmed |
| `ENDPOINT_NOT_VERIFIED` | needs_review | a gap's span could contain an unconfirmed date |
| `AMOUNT_RATE_NOT_TOTALED` | needs_review | a rate, not a charge |
| `AMOUNT_ESTIMATE` / `AMOUNT_DAMAGES` / `AMOUNT_UNCLEAR` | needs_review | estimate, non-bill figure, or unreadable/unlabelled value |
| `LEXICON_ONLY` / `LLM_ONLY` | needs_review | phrase list and model disagree on a flag |
| `SPLIT_AMBIGUOUS` | needs_review | record boundaries uncertain |
| `LLM_SPLIT` | needs_review | the record's boundaries were chosen by the model (code-validated), because the paste had no recognisable record markers |
| `INJECTION_SUSPECTED` | needs_review | the item's record (or a cross-record pass in this case) carries an instruction-like-text warning |
| `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
| `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded answer; conflicts between records may be missing (case-level `record_warning` `analysis_incomplete`, no single record) |
---
name: t043-panels-conventions
description: How flags/charges/review controls plug into frontend-1's app shell, and E2E testid pitfalls
metadata:
  type: project
---
Review UI is split: frontend-1 owns index/api/state/timeline/source; frontend-2 owns review.js, flags.js, charges.js, review.css. Plug-in points: ZL.registerPanel(fn(case, mountEl)), ZL.registerRowActions(fn(entry,rowEl)), ZL.state.applyReview(resp), ZL.openSource(spans,title).
**Why:** tests/e2e specs (qa) are the contract; strict locators mean exactly one btn-source per flag, data-review only on item roots (count of [data-review=accepted] must equal accepted items), no data-state outside queue rows.
**How to apply:** dev harness at app/frontend/dev/panels.html (?case=01|03|07) serves with `python3 -m http.server` from app/frontend; E2E assertions right after a click race the async review response.
      39 app/frontend/api.js
      53 app/frontend/app.js
      57 app/frontend/audit.js
      69 app/frontend/batch.js
      91 app/frontend/charges.js
      33 app/frontend/dom.js
      37 app/frontend/excerpt.js
      55 app/frontend/export.js
      51 app/frontend/exportcfg.js
      99 app/frontend/flags.js
      85 app/frontend/input.js
     103 app/frontend/manual.js
     216 app/frontend/mock.js
      29 app/frontend/mock_extra.js
      55 app/frontend/mock_flags.js
       2 app/frontend/mock_sample.js
      67 app/frontend/narrative.js
     297 app/frontend/review.js
      37 app/frontend/source.js
      28 app/frontend/state.js
      64 app/frontend/switcher.js
     151 app/frontend/timeline.js
     109 app/frontend/review.css
      64 app/frontend/styles.css
      66 app/frontend/index.html
    1957 total
"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-undo-batch, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
  T-068 (undated-entry and orphan-date branches): date-to-confirm-item (one row per undated record in dates-to-confirm, carries data-record-id), date-to-confirm-excerpt (its verbatim excerpt),
  confirm-date (one per reading, carries data-date = YYYY-MM-DD), missing-entry (a record with no entry, carries data-record-id), missing-date-confirmed (the confirmed date shown on a missing-entry row), btn-manual-entry (by-hand entry control on a missing-entry row).
  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
Attributes (data-item-id = the item id on every entry/amount/flag row, used by the keyboard flow; and on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
  data-testid = the hook attribute carrying every test id above (specs select it as [data-testid="..."]); data-record-id = the record id (e.g. r8) on date-to-confirm-item and missing-entry rows; data-date = YYYY-MM-DD on confirm-date buttons.
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
"""
import json, os, urllib.request, urllib.error
import pytest

BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")

def _up():
    try:
        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
        return True
    except Exception:
        return False

def pytest_collection_modifyitems(config, items):
    if _up():
        return
    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
    for it in items:
        if "tests/e2e" in str(it.fspath).replace("\\", "/"):
            it.add_marker(skip)

def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, (json.loads(raw) if raw else None)

def golden_text(name):
    return open(os.path.join(SAMPLE_PATH, name)).read()

@pytest.fixture
def base_url():
    return BASE

@pytest.fixture
def sample_case():
    """A ready (pipeline finished) sample case created over the API; deleted afterwards."""
    import time
    st, c = api("POST", "/api/cases", {"sample": True}); assert st in (200, 201)
    tok = c["token"]; assert api("POST", f"/api/cases/{tok}/run", {})[0] == 202
    for _ in range(300):
        s = api("GET", f"/api/cases/{tok}/status")[1]
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(1)
    assert s["status"] == "ready"
    yield tok
    api("DELETE", f"/api/cases/{tok}")

@pytest.fixture(scope="session")
def pw():
    sync = pytest.importorskip("playwright.sync_api")
    with sync.sync_playwright() as p:
        yield p

@pytest.fixture
def page(pw):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": 1280, "height": 900}, permissions=["clipboard-read", "clipboard-write"])
    pg = ctx.new_page()
    yield pg
    b.close()

def open_case(page, tok):
    page.goto(f"{BASE}/#/case/{tok}")
    page.get_by_test_id("timeline").wait_for(timeout=15000)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:21.615Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && cat index.html dom.js api.js state.js app.js; git -C /Users/arsis/zlayt-pm-project log --oneline | head -5"
}
````

### User / tool · 2026-11-02T03:22:21.755Z

**tool result**
````
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Treatment timeline (prototype)</title>
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="review.css">
</head>
<body>
<div id="banner-synthetic" class="banner synth" data-testid="banner-synthetic" role="note">Synthetic data only — never paste real records</div>
<header class="top">
  <h1>Treatment timeline</h1>
  <span id="badge" class="chip" hidden></span>
  <span id="retention" class="muted small" hidden></span>
  <button type="button" id="delete-now" class="btn small" hidden>Delete now</button>
</header>
<div id="banner-ai" class="banner ai" data-testid="banner-ai" role="note" hidden></div>
<main>
  <section id="view-input" class="card" aria-labelledby="h-input">
    <h2 id="h-input">1. Records</h2>
    <div id="input-body"></div>
  </section>
  <section id="view-review" class="card" aria-labelledby="h-review" hidden>
    <h2 id="h-review" class="sr">Review</h2>
    <div id="review-body"></div>
  </section>
  <section id="view-export" class="card" aria-labelledby="h-export" hidden>
    <h2 id="h-export">Export</h2>
    <div id="export-body"></div>
  </section>
</main>
<dialog id="source-modal" data-testid="record-modal" aria-labelledby="source-title">
  <div class="dlg-head"><h2 id="source-title">Source record</h2><button type="button" id="source-close" class="btn small" data-testid="btn-close-modal">Close</button></div>
  <div id="source-body"></div>
</dialog>
<dialog id="why-modal" data-testid="why-modal" aria-labelledby="why-title">
  <div class="dlg-head"><h2 id="why-title">Why?</h2><button type="button" class="btn small" data-testid="why-close" onclick="this.closest('dialog').close()">Close</button></div>
  <div id="why-body"></div>
</dialog>
<!-- load order matters; mock files are only used when API_MODE is "mock" -->
<script src="dom.js"></script>
<script src="mock_sample.js"></script>
<script src="mock.js"></script>
<script src="mock_flags.js"></script>
<script src="mock_extra.js"></script>
<script src="api.js"></script>
<script src="state.js"></script>
<script src="input.js"></script>
<script src="source.js"></script>
<script src="timeline.js"></script>
<!-- T-043 (frontend-2): review.js first (controls + keys), then the panels -->
<script src="review.js"></script>
<script src="flags.js"></script>
<script src="charges.js"></script>
<script src="batch.js"></script>
<script src="audit.js"></script>
<script src="manual.js"></script>
<script src="narrative.js"></script>
<script src="exportcfg.js"></script>
<script src="excerpt.js"></script>
<script src="export.js"></script>
<script src="switcher.js"></script>
<script src="app.js"></script>
</body>
</html>
/* Shared DOM helpers (frontend-1 / T-042; also used by T-043). Data is only ever written with textContent / text nodes. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  // el("button", {class:"x", type:"button", onclick:fn, "data-testid":"y"}, "label", childNode, ...)
  ZL.el = function (tag, attrs, ...kids) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (v === false || v == null) continue;
      if (k === "class") e.className = v;
      else if (k === "text") e.textContent = v;
      else if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v === true ? "" : String(v));
    }
    for (const c of kids.flat()) {
      if (c == null || c === false) continue;
      e.append(c.nodeType ? c : document.createTextNode(String(c)));
    }
    return e;
  };
  // Rank "needs review first" by the state an item had when this case was first shown, so rows do not jump when a decision changes the state
  // (keeps the row under the cursor still and nth-button order stable).
  const ranks = {};
  ZL.firstRank = (id, state) => { const k = (ZL.state && ZL.state.get().token) + ":" + id; if (!(k in ranks)) ranks[k] = state === "needs_review" ? 0 : 1; return ranks[k]; };
  ZL.clear = (n) => { while (n.firstChild) n.removeChild(n.firstChild); return n; };
  ZL.$ = (s, r) => (r || document).querySelector(s);
  ZL.fmtDate = (iso) => {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
    if (!m) return iso || "undated";
    const mon = ["January","February","March","April","May","June","July","August","September","October","November","December"][+m[2] - 1];
    return `${mon} ${+m[3]}, ${m[1]}`;
  };
  ZL.money = (cents) => "$" + (cents / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
})();
/* API client. ONE switch: API_MODE. "mock" uses mock.js (in-memory, contract-shaped); "real" calls the FastAPI backend under /api.
   `?api=real` / `?api=mock` in the page URL overrides the constant (used by tests). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const API_MODE = "real"; // <-- the ONE switch: "real" (FastAPI under /api) or "mock" (in-memory, mock.js)
  const mode = new URLSearchParams(location.search).get("api") || API_MODE;
  ZL.API_MODE = mode;

  class ApiError extends Error {
    constructor(status, err) { super((err && err.message) || "Request failed"); this.status = status; this.code = (err && err.code) || "error"; this.detail = (err && err.detail) || {}; }
  }
  ZL.ApiError = ApiError;

  async function call(method, path, body) {
    let status, data;
    if (mode === "mock") {
      ({ status, body: data } = await ZL.mock.handle(method, path, body));
    } else {
      const res = await fetch("/api" + path, { method, headers: body ? { "Content-Type": "application/json" } : {}, body: body ? JSON.stringify(body) : undefined });
      status = res.status;
      try { data = await res.json(); } catch (_) { data = null; }
    }
    if (status >= 400) throw new ApiError(status, data && data.error);
    return data;
  }
  const t = (token) => "/cases/" + encodeURIComponent(token);
  ZL.api = {
    health: () => call("GET", "/health"),
    createCase: (payload) => call("POST", "/cases", payload),          // {text} or {sample:true}
    getCase: (token) => call("GET", t(token)),
    run: (token, confirm_rerun) => call("POST", t(token) + "/run", { confirm_rerun: !!confirm_rerun }),
    status: (token) => call("GET", t(token) + "/status"),
    item: (token, id) => call("GET", t(token) + "/items/" + encodeURIComponent(id)),
    review: (token, id, body) => call("POST", t(token) + "/items/" + encodeURIComponent(id) + "/review", body),
    confirmDate: (token, rid, date) => call("POST", t(token) + "/records/" + encodeURIComponent(rid) + "/confirm_date", { date }),
    exportCase: (token) => call("GET", t(token) + "/export"),
    remove: (token) => call("DELETE", t(token)),
  };
})();
/* Tiny store. ZL.state.get() -> {health, token, case, status, error}; subscribe(fn) re-renders on every set(). */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  let s = { health: null, token: null, created: null, case: null, status: null };
  const subs = [];
  ZL.state = {
    get: () => s,
    set(patch) { s = Object.assign({}, s, patch); subs.forEach((f) => f(s)); },
    subscribe(f) { subs.push(f); },
    // Patch the local case from a POST .../review response (item + totals + review); T-043 calls this after each decision.
    applyReview(resp) {
      const c = s.case; if (!c || !resp || !resp.item) return;
      for (const k of ["entries", "undated_entries", "amounts", "flags"]) {
        const i = (c[k] || []).findIndex((x) => x.id === resp.item.id);
        if (i >= 0) { // the review response labels items with a generic kind ("amount"); an amount's own kind (charge / rate / ...) must survive
          const { kind, ...rest } = resp.item; c[k][i] = Object.assign({}, c[k][i], rest);
        }
      }
      if (resp.totals) c.totals = Object.assign({}, c.totals, resp.totals);
      if (resp.review) c.review = Object.assign({}, c.review, resp.review);
      ZL.state.set({ case: c });
    },
  };
  // Extension points for T-043 (frontend-2): register without editing T-042 files.
  ZL.hooks = { rowActions: [], panels: [] };           // rowActions: fn(entry, rowEl); panels: fn(case, mountEl) -> void
  ZL.registerRowActions = (fn) => ZL.hooks.rowActions.push(fn);
  ZL.registerPanel = (fn) => ZL.hooks.panels.push(fn);
})();
/* Bootstrap: health -> banners; restore case from #case=<token>; poll run status; render on every state change. */
(function () {
  const ZL = window.ZL, { $ } = ZL;
  const SYNTH = "Synthetic data only — never paste real records";
  let poller = null;

  function renderChrome(s) {
    const h = s.health;
    $("#banner-synthetic").textContent = (h && h.banner) || SYNTH;           // present on every view, even before /health answers
    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by code; you decide every item";
    const badge = $("#badge"); badge.textContent = h ? (h.demo_mode ? (h.fixture_set === "recorded" ? "cached demo (recorded responses)" : "cached demo (curated responses)") : (ZL.API_MODE === "mock" ? "mock API" : h.backend)) : ""; // D-029: the demo replays the curated fixture set; label says so
    badge.hidden = !h;
    const live = $("#retention"); live.hidden = !(h && !h.demo_mode && s.token && ZL.API_MODE !== "mock");
    live.textContent = h ? `Pasted text is deleted after ${h.retention_hours} hours.` : "";
    $("#delete-now").hidden = live.hidden;
  }
  function render(s) {
    renderChrome(s);
    ZL.renderInput(s);
    $("#view-review").hidden = !(s.case && s.case.status === "ready");
    ZL.renderReview(s);
  }
  ZL.state.subscribe(render);

  ZL.pollRun = function () {
    clearInterval(poller);
    const tick = async () => {
      const s = ZL.state.get(); if (!s.token) return clearInterval(poller);
      try {
        const st = await ZL.api.status(s.token);
        if (st.status === "ready") { clearInterval(poller); ZL.state.set({ status: st, case: await ZL.api.getCase(s.token) }); }
        else if (st.status === "failed") { clearInterval(poller); ZL.state.set({ status: st, case: await ZL.api.getCase(s.token) }); }
        else ZL.state.set({ status: st });
      } catch (e) { clearInterval(poller); ZL.state.set({ status: { status: "failed", error: { message: e.message } } }); }
    };
    tick(); poller = setInterval(tick, 1000);
  };

  async function boot() {
    render(ZL.state.get());
    try { ZL.state.set({ health: await ZL.api.health() }); } catch (_) { /* banners fall back to static text */ }
    const m = /#\/case\/([^&/]+)/.exec(location.hash);
    if (m) {
      const token = decodeURIComponent(m[1]);
      try { const c = await ZL.api.getCase(token); ZL.state.set({ token, case: c }); if (c.status === "running") ZL.pollRun(); }
      catch (_) { history.replaceState(null, "", location.pathname + location.search); }
    }
  }
  document.addEventListener("DOMContentLoaded", () => {
    $("#delete-now").addEventListener("click", () => ZL.startOver());
    boot();
  });
})();
e3cea6f feat(backend): check-trace API, per-item ladder stepper, case stepper with export gate, judge summary (T-080, D-042)
0f58181 fix(backend): credibility sentence runs to . ? ! (semicolon/line break are clauses), full-sentence excerpt, D-043 allow-list trimmed (T-067 r5)
1193f8a docs(research): record and billing document formats for synthetic packets (T-078)
bb26bf0 docs(research): case library v2 real-world PI patterns (T-077)
8634bfe fix(backend): credibility flags fail toward flagging, whole-sentence allow-list only (T-067 r4, D-043)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:22.903Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && cat review.js audit.js; cat styles.css review.css"
}
````

### User / tool · 2026-11-02T03:22:23.029Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:24.252Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && cat audit.js; cat styles.css; cat review.css; grep -n \"why\\|Why\" timeline.js review.js | head -60"
}
````

### User / tool · 2026-11-02T03:22:24.390Z

**tool result**
````
/* Audit drawer (T-058 AC1): per item (Audit button on every card/row) and for the whole case. Shows every model call: role, step, model, backend,
   prompt version and hash, verdict, latency. In local mode the API also returns prompts, responses and edit before/after; those appear
   in collapsed sections. Public mode: metadata only (whatever the API returns is shown, nothing is requested beyond GET /audit). Text via ZL.el only. */
(function () {
  const ZL = window.ZL, RV = ZL.rv, { el, clear } = ZL;
  let dlg = null, body = null, title = null;

  function ensure() {
    if (dlg) return;
    title = el("h2", { id: "audit-title", class: "au-title" }, "Audit");
    body = el("div", { class: "au-body" });
    dlg = el("dialog", { id: "audit-drawer", class: "au-drawer", "data-testid": "audit-drawer", "aria-labelledby": "audit-title" },
      el("div", { class: "au-head" }, title, el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-close-audit", onclick: () => dlg.close() }, "Close")), body);
    dlg.addEventListener("click", (ev) => { if (ev.target === dlg) dlg.close(); });
    document.body.append(dlg);
  }
  const kv = (k, v) => (v == null || v === "" ? null : el("span", { class: "au-kv" }, el("span", { class: "au-k" }, k + " "), String(v)));
  const pre = (label, text) => (text == null || text === "" ? null : el("details", { class: "au-more" }, el("summary", {}, label), el("pre", { class: "au-pre" }, typeof text === "string" ? text : JSON.stringify(text, null, 2))));

  function callRow(c) {
    const rf = c.recorded_from && c.recorded_from.backend ? " (recorded from " + c.recorded_from.backend + ")" : "";
    return el("li", { class: "au-call", "data-testid": "audit-call" },
      el("div", { class: "au-line" }, el("strong", {}, c.role + " · " + c.step), el("span", { class: "rv-chip" }, c.parsed_ok ? "parsed" : "not parsed"), c.verdict ? el("span", { class: "rv-chip" }, "verdict: " + c.verdict) : null),
      el("div", { class: "au-meta" }, kv("model", c.model), kv("backend", c.backend + rf), kv("prompt", c.prompt_version), kv("hash", c.prompt_sha256 ? String(c.prompt_sha256).slice(0, 12) : null),
        kv("latency", c.latency_ms != null ? c.latency_ms + " ms" : null), kv("attempt", c.attempt), kv("tokens", c.tokens_in != null ? c.tokens_in + " in / " + c.tokens_out + " out" : null), kv("cost", c.cost_usd != null ? "$" + c.cost_usd : null)),
      pre("System prompt (local mode)", c.system_text), pre("Record text sent to the model (local mode)", c.user_text), pre("Model response (local mode)", c.response_raw), c.error ? el("p", { class: "rv-error" }, "Error: " + c.error) : null);
  }
  function eventRow(e) {
    return el("li", { class: "au-call", "data-testid": "audit-event" }, el("div", { class: "au-line" }, el("strong", {}, e.action), el("span", { class: "au-k" }, e.at || "")),
      e.before || e.after ? pre("Before and after (local mode)", { before: e.before, after: e.after }) : null);
  }

  RV.openAudit = async function (itemId, label) {
    ensure(); const c = RV.caseNow(); if (!c) return;
    title.textContent = itemId ? "Audit: " + (label || itemId) : "Audit: whole case";
    clear(body); body.append(el("p", { role: "status" }, "Loading…"));
    if (!dlg.open) dlg.showModal();
    const r = await RV.http("GET", "/cases/" + encodeURIComponent(c.token) + "/audit");
    clear(body);
    if (r.status !== 200) { body.append(el("p", { class: "rv-error", role: "alert" }, RV.errMsg(r, "The audit could not be loaded."))); return; }
    const a = r.body, calls = (a.calls || []).filter((x) => !itemId || x.item_id === itemId), events = (a.events || []).filter((x) => !itemId || x.item_id === itemId);
    const s = a.summary || {};
    body.append(el("p", { class: "rv-help", "data-testid": "audit-summary" }, itemId ? `${calls.length} model call${calls.length === 1 ? "" : "s"} for this item.` :
      `${s.calls != null ? s.calls : calls.length} model calls, ${s.latency_ms_total != null ? s.latency_ms_total + " ms total latency" : ""}${s.cost_usd != null ? ", $" + s.cost_usd : ""}${s.by_backend ? ", by backend: " + Object.keys(s.by_backend).map((k) => k + " " + s.by_backend[k]).join(", ") : ""}.`));
    body.append(el("h3", {}, "Model calls"));
    if (calls.length) body.append(el("ol", { class: "au-list" }, calls.map(callRow)));
    else body.append(el("p", { class: "rv-empty" }, itemId ? "No model call was made for this item: code computed it." : "No model calls recorded."));
    body.append(el("h3", {}, "Your decisions"));
    if (events.length) body.append(el("ol", { class: "au-list" }, events.map(eventRow))); else body.append(el("p", { class: "rv-empty" }, "No decisions recorded yet."));
  };

  RV.registerPanel("audit", (root, c) => {
    ZL.clear(root);
    root.append(el("h2", {}, "Audit"), el("p", { class: "rv-help" }, "Every model call behind this case, and every decision you made."),
      el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-audit-case", onclick: () => RV.openAudit(null) }, "Open full audit"));
  });
})();
[hidden]{display:none!important}
:root{--bg:#f6f7f9;--panel:#fff;--ink:#16181d;--muted:#555d6b;--line:#d5dae2;--accent:#2f5bd3;--ok:#1d7a46;--warn:#8a5300;--bad:#b42318;--chip:#eef1f6;--mark:#ffe58a;--warnbg:#fff4e0;--aibg:#eaf1ff}
@media (prefers-color-scheme:dark){:root{--bg:#0f1115;--panel:#171a21;--ink:#e7e9ee;--muted:#a3abb9;--line:#2c3240;--accent:#8fb0ff;--ok:#4cc38a;--warn:#f0b04a;--bad:#ff8a7e;--chip:#222734;--mark:#7a6200;--warnbg:#2b2214;--aibg:#17233d}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.banner{padding:8px 16px;font-weight:600;text-align:center}
.banner.synth{background:#b42318;color:#fff;position:sticky;top:0;z-index:5}
.banner.ai{background:var(--aibg);border-bottom:1px solid var(--line);font-weight:500}
.top{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding:10px 16px}
.top h1{font-size:20px;margin:0 auto 0 0}
main{max-width:980px;margin:0 auto;padding:0 12px 60px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px;margin-bottom:14px}
h2{font-size:18px;margin:0 0 8px}h3{font-size:15px;margin:10px 0 4px}
.muted{color:var(--muted)}.small{font-size:13px}
.lbl{display:block;font-weight:600;margin-bottom:4px}
textarea{width:100%;font:14px/1.4 ui-monospace,Menlo,monospace;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:8px}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:10px 0}
.btn{display:inline-flex;align-items:center;min-height:44px;padding:0 14px;border:1px solid var(--line);border-radius:8px;background:var(--chip);color:var(--ink);font:inherit;font-weight:600;cursor:pointer}
.btn.small{min-height:36px;padding:0 10px;font-size:14px}
.btn.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
.btn:focus-visible,textarea:focus-visible,select:focus-visible,mark:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.error{background:var(--warnbg);border:1px solid var(--bad);color:var(--bad);border-radius:8px;padding:8px 10px;font-weight:600}
.error[hidden]{display:none}
.found{font-size:22px;font-weight:700;margin:0}
.reclist{padding-left:20px;margin:6px 0}
.progress{font-weight:600}
.chip{display:inline-block;background:var(--chip);border-radius:999px;padding:1px 10px;font-size:13px;font-weight:600}
.chip.st-verified{color:var(--ok)}.chip.st-needs_review{color:var(--warn);background:var(--warnbg)}.chip.st-rejected{color:var(--bad)}
.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
.toolbar h2{margin:0}
select{background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:6px}
.entry{border:1px solid var(--line);border-left:5px solid var(--ok);border-radius:10px;padding:10px 12px;margin:10px 0;background:var(--panel)}
.entry.st-needs_review{border-left-color:var(--warn);background:var(--warnbg)}
.entry.st-rejected{border-left-color:var(--bad)}
.entry-head{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center}
.date{font-weight:700;font-variant-numeric:tabular-nums}.provider{font-weight:600}
.summary{margin:6px 0}
.tag{margin-left:8px;font-size:12px;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:0 4px}
.excerpt{margin:6px 0;padding:6px 10px;border-left:3px solid var(--line);color:var(--muted);font-style:italic;overflow-wrap:anywhere}
.reason{color:var(--warn);font-weight:600;margin:4px 0}
.row-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.group{margin-top:22px;padding-top:6px;border-top:2px solid var(--line)}
dialog{border:1px solid var(--line);border-radius:12px;background:var(--panel);color:var(--ink);width:min(820px,96vw);max-height:90vh;padding:0}
dialog::backdrop{background:rgba(0,0,0,.45)}
.dlg-head{display:flex;justify-content:space-between;align-items:center;gap:8px;position:sticky;top:0;background:var(--panel);padding:10px 14px;border-bottom:1px solid var(--line)}
.dlg-head h2{margin:0;font-size:17px}
#source-body,#why-body{padding:10px 14px}
.src-text{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px;font:14px/1.5 ui-monospace,Menlo,monospace}
mark{background:var(--mark);color:inherit;padding:0 1px;border-radius:2px}
.kv{display:grid;grid-template-columns:max-content 1fr;gap:4px 12px}.kv dt{font-weight:700}.kv dd{margin:0;overflow-wrap:anywhere}
.checks{margin:0;padding-left:18px}.checks .bad{color:var(--bad);font-weight:700}
.why-sentence{font-weight:600}
@media (max-width:480px){.kv{grid-template-columns:1fr}.btn{min-height:44px}main{padding:0 8px 60px}}

.btn[disabled]{opacity:.5;cursor:not-allowed}.entry,[tabindex],.btn{scroll-margin-top:90px}
details.reclist-wrap summary{cursor:pointer;font-weight:600;min-height:36px}

.count-line{font-weight:600;background:var(--chip);border-radius:8px;padding:8px 10px}
.ex-block{margin:14px 0}.ex-block h3{margin:0}
.ex-text{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px;font:14px/1.5 ui-monospace,Menlo,monospace;max-height:420px;overflow:auto}
.ex-confirm-msg{background:var(--warnbg);border:1px solid var(--warn);border-radius:8px;padding:8px 10px;font-weight:600}
.ex-units{margin-top:8px;border-top:1px dashed var(--line);padding-top:8px}.ex-unit-list{list-style:none;padding:0;margin:6px 0}.ex-unit-list li{margin:4px 0}
.ex-unit-list input{width:22px;height:22px;vertical-align:middle}
/* Flags panel, charges table and review controls (T-043). Self-contained: own tokens, works with or without styles.css. */
:root {
  --rv-ink: #1c2430; --rv-muted: #566170; --rv-line: #cfd6df; --rv-bg: #ffffff; --rv-soft: #f4f6f9;
  --rv-accent: #124e9c; --rv-warn-bg: #fff4d6; --rv-warn-ink: #5b3d00; --rv-ok-bg: #e3f3e8; --rv-ok-ink: #14532d;
  --rv-bad-bg: #fde8e8; --rv-bad-ink: #7a1212; --rv-focus: #0b57d0;
}
.rv-panel { color: var(--rv-ink); max-width: 100%; min-width: 0; margin: 1.25rem 0; overflow-wrap: anywhere; }
.rv-panel h2 { font-size: 1.25rem; margin: 0 0 .25rem; }
.rv-panel h3 { font-size: 1.05rem; margin: 1.25rem 0 .5rem; }
.rv-help, .rv-keys, .rv-why, .rv-empty { color: var(--rv-muted); font-size: .9rem; margin: .25rem 0 .75rem; }
.rv-empty { font-style: italic; }
.rv-banner { background: var(--rv-warn-bg); color: var(--rv-warn-ink); border: 1px solid #e6c36a; border-radius: 6px; padding: .6rem .75rem; margin: .5rem 0; }
.rv-sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }

.rv-card { border: 1px solid var(--rv-line); border-radius: 8px; background: var(--rv-bg); padding: .75rem; margin: .5rem 0; min-width: 0; }
.rv-card[data-review="dismissed"] { opacity: .65; background: var(--rv-soft); }
.rv-card[data-review="accepted"], .rv-card[data-review="edited"] { border-left: 4px solid #2e7d32; }
.rv-card[data-state="needs_review"] { border-left: 4px solid #b7791f; }
.rv-card:focus, .rv-btn:focus, .rv-input:focus, .rv-text:focus, .rv-radio input:focus { outline: 3px solid var(--rv-focus); outline-offset: 2px; }
.rv-head { display: flex; flex-wrap: wrap; align-items: center; gap: .4rem .6rem; }
.rv-title { font-size: 1rem; margin: 0; flex: 1 1 14rem; }
.rv-chips { display: inline-flex; flex-wrap: wrap; gap: .3rem; }
.rv-chip { display: inline-block; font-size: .75rem; font-weight: 600; padding: .1rem .5rem; border-radius: 999px; background: var(--rv-soft); border: 1px solid var(--rv-line); }
.rv-state-needs_review { background: var(--rv-warn-bg); color: var(--rv-warn-ink); border-color: #e6c36a; }
.rv-state-verified, .rv-rs-accepted, .rv-rs-edited { background: var(--rv-ok-bg); color: var(--rv-ok-ink); border-color: #9ccfae; }
.rv-state-rejected, .rv-rs-dismissed { background: var(--rv-bad-bg); color: var(--rv-bad-ink); border-color: #e3a3a3; }
.rv-selfreport { background: #e8eefc; color: #1b3a8a; border-color: #a9bbea; }
.rv-reason-line { background: var(--rv-warn-bg); color: var(--rv-warn-ink); padding: .35rem .5rem; border-radius: 6px; margin: .4rem 0; font-size: .9rem; }
.rv-usernote { background: var(--rv-soft); padding: .4rem .5rem; border-radius: 6px; font-size: .9rem; }
.rv-text-body { margin: .5rem 0; }

/* evidence: conflicts sit side by side, unmerged */
.rv-evidence { list-style: none; margin: .5rem 0; padding: 0; display: grid; grid-template-columns: 1fr; gap: .5rem; }
.rv-evidence.rv-side { grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); }
.rv-ev { border: 1px solid var(--rv-line); border-radius: 6px; padding: .4rem .5rem; background: var(--rv-soft); min-width: 0; }
.rv-ev-cap { display: block; font-size: .75rem; color: var(--rv-muted); font-weight: 600; }
.rv-ev-more { display: block; font-size: .8rem; color: var(--rv-muted); margin-top: .3rem; }
.rv-quote { margin: .25rem 0 0; padding: 0; font-style: normal; }

/* buttons */
.rv-actions { display: flex; flex-wrap: wrap; gap: .5rem; margin: .5rem 0 0; }
.rv-btn { font: inherit; font-weight: 600; min-height: 40px; min-width: 44px; padding: .35rem .8rem; border-radius: 6px; border: 1px solid var(--rv-accent); background: var(--rv-accent); color: #fff; cursor: pointer; }
.rv-btn.rv-secondary, .rv-btn.rv-dismiss, .rv-btn.rv-reset, .rv-btn.rv-edit { background: #fff; color: var(--rv-accent); }
.rv-btn[aria-pressed="true"] { box-shadow: inset 0 0 0 2px #fff, 0 0 0 2px var(--rv-accent); }
.rv-btn:disabled { opacity: .5; cursor: not-allowed; }
.rv-edit, .rv-reason, .rv-datefix { margin: .5rem 0; }
.rv-label { display: block; font-size: .85rem; font-weight: 600; }
.rv-text, .rv-input { display: block; width: 100%; box-sizing: border-box; font: inherit; padding: .4rem; margin-top: .25rem; border: 1px solid #8b96a5; border-radius: 6px; }
.rv-reason { display: flex; flex-wrap: wrap; gap: .5rem; align-items: center; }
.rv-reason .rv-input { flex: 1 1 14rem; margin: 0; }
.rv-error { color: var(--rv-bad-ink); font-size: .9rem; margin: .3rem 0 0; }
.rv-error:empty { display: none; }
.rv-confirm { background: var(--rv-warn-bg); border: 1px solid #e6c36a; border-radius: 6px; padding: .5rem; margin-top: .5rem; }
.rv-confirm[hidden], .rv-edit[hidden], .rv-reason[hidden] { display: none; }
.rv-fieldset { border: 1px solid var(--rv-line); border-radius: 6px; margin: 0 0 .5rem; padding: .5rem; min-width: 0; }
.rv-radio { display: flex; gap: .5rem; align-items: center; min-height: 40px; }

/* charges */
.rv-totals { background: var(--rv-soft); border: 1px solid var(--rv-line); border-radius: 8px; padding: .6rem .8rem; margin: .5rem 0 1rem; }
.rv-total { margin: .15rem 0; }
.rv-total-main { font-size: 1.35rem; }
.rv-total-pending { color: var(--rv-muted); font-size: .95rem; }
.rv-table { width: 100%; border-collapse: collapse; table-layout: fixed; }
.rv-table th { text-align: left; font-size: .8rem; color: var(--rv-muted); padding: .3rem .5rem; border-bottom: 2px solid var(--rv-line); }
.rv-table td { vertical-align: top; padding: .5rem; border-bottom: 1px solid var(--rv-line); min-width: 0; }
.rv-table .rv-card { border-radius: 0; border-top: 0; border-right: 0; margin: 0; }
.rv-c-amount .rv-money { display: block; font-size: 1.1rem; }
.rv-kind { display: inline-block; font-size: .8rem; color: var(--rv-muted); }
.rv-unclear-note { display: block; font-size: .85rem; margin-top: .25rem; color: var(--rv-warn-ink); }
.rv-noted { display: block; font-size: .85rem; margin-top: .25rem; color: var(--rv-muted); }
.rv-tray { margin-top: 1.5rem; border-top: 2px dashed var(--rv-line); padding-top: .25rem; }

@media (max-width: 640px) {
  .rv-panel { margin-left: 0; margin-right: 0; }
  .rv-table, .rv-table thead, .rv-table tbody, .rv-table tr, .rv-table td { display: block; width: 100%; box-sizing: border-box; }
  .rv-table thead { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
  .rv-table tr.rv-card { border: 1px solid var(--rv-line); border-radius: 8px; margin: .6rem 0; padding: .25rem; }
  .rv-table td { border-bottom: 0; padding: .3rem .4rem; }
  .rv-table td[data-label]::before { content: attr(data-label); display: block; font-size: .7rem; text-transform: uppercase; letter-spacing: .04em; color: var(--rv-muted); }
  .rv-btn { min-height: 44px; flex: 1 1 auto; }
  .rv-evidence.rv-side { grid-template-columns: 1fr; }
}

/* case switcher (local mode) */
.cs { margin: .75rem 0; }
.cs-h { font-size: 1rem; margin: .5rem 0 .25rem; }
.cs-list { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: .5rem; }
.cs-btn { display: block; text-align: left; max-width: 100%; overflow-wrap: anywhere; }
.cs-meta { display: block; font-weight: 400; font-size: .8rem; opacity: .85; }
.cs-msg:empty { display: none; }

/* batch bar, audit drawer, export settings */
.rv-batchbar { display: flex; flex-wrap: wrap; gap: .5rem .75rem; align-items: center; margin: .5rem 0; padding: .5rem; border: 1px dashed var(--rv-line); border-radius: 8px; }
.rv-batchbar .rv-help { margin: 0; flex: 1 1 16rem; }
.rv-batchhost { margin: 0; }
.au-drawer { position: fixed; inset: 0 0 0 auto; margin: 0; height: 100%; max-height: 100%; width: min(36rem, 100vw); max-width: 100vw; box-sizing: border-box; border: 0; border-left: 2px solid var(--rv-line); padding: 1rem; overflow: auto; color: var(--rv-ink); background: var(--rv-bg); }
.au-drawer::backdrop { background: rgba(20, 30, 45, .45); }
.au-head { display: flex; justify-content: space-between; align-items: center; gap: .5rem; }
.au-title { font-size: 1.1rem; margin: 0; overflow-wrap: anywhere; }
.au-list { list-style: none; margin: 0; padding: 0; }
.au-call { border: 1px solid var(--rv-line); border-radius: 8px; padding: .5rem; margin: .5rem 0; min-width: 0; }
.au-line { display: flex; flex-wrap: wrap; gap: .4rem .6rem; align-items: center; }
.au-meta { display: flex; flex-wrap: wrap; gap: .25rem .9rem; font-size: .85rem; margin-top: .3rem; }
.au-k { color: var(--rv-muted); font-size: .8rem; }
.au-more { margin-top: .4rem; }
.au-pre { white-space: pre-wrap; overflow-wrap: anywhere; font-size: .8rem; background: var(--rv-soft); padding: .4rem; border-radius: 6px; max-height: 16rem; overflow: auto; }
.es-form { display: grid; gap: .6rem; max-width: 32rem; }
.es-field .rv-help { display: block; margin: .15rem 0 0; font-weight: 400; }
@media (max-width: 640px) { .au-drawer { width: 100vw; border-left: 0; } }
review.js:191:    bar.append(btn("accept", noted ? "Accept as noted" : "Accept", "btn-accept", { "aria-pressed": String(st === "accepted"), disabled: blocked, "aria-describedby": blocked ? "why-blocked-" + id : null, onclick: () => RV.act(id, { action: "accept" }, { focus: "accept" }) }));
review.js:199:    if (blocked) root.append(el("p", { class: "rv-help rv-blocked", id: "why-blocked-" + id, "data-testid": "accept-blocked-reason" }, DATE_FIRST + " ",
timeline.js:1:/* Review view, read-only part (T-042): timeline rows, Dates to confirm, "could not verify" tray, Why? panel. (R-TL-1, R-TL-5, R-TL-6, R-IN-5)
timeline.js:31:        el("button", { type: "button", class: "btn small", "data-testid": "entry-why", onclick: () => openWhy(e.id) }, "Why?"),
timeline.js:101:        el("p", { class: "summary" }, t.why),
timeline.js:109:  // ---- Why? panel
timeline.js:111:  async function openWhy(id) {
timeline.js:112:    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
timeline.js:114:    ZL.$("#why-title").textContent = ent ? `Why? ${ent.provider}, ${ent.date || "undated"}` : "Why? this item";
timeline.js:120:        el("p", { class: "why-sentence", "data-testid": "why-text" }, it.why),
timeline.js:121:        el("dl", { class: "kv", "data-testid": "why-ladder" },
timeline.js:122:          el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
timeline.js:123:          el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
timeline.js:124:          lad.generator ? [el("dt", {}, "Drafted by"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
timeline.js:126:          el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
timeline.js:127:          el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)")),
timeline.js:131:  ZL.openWhy = openWhy;
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:26.638Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 40,140p review.js | cut -c1-260; echo ------; sed -n 205,297p review.js | cut -c1-260; echo -----; sed -n 100,151p timeline.js | cut -c1-300"
}
````

### User / tool · 2026-11-02T03:22:26.749Z

**tool result**
````
  };
  RV.errMsg = (r, fallback) => (r && r.body && r.body.error && r.body.error.message) || fallback || "That did not work.";
  RV.label = (item) => item.title || item.provider || item.text || item.id;

  const REVIEW_LABEL = { pending: "Not reviewed", accepted: "Accepted", edited: "Edited", dismissed: "Dismissed" };
  const STATE_LABEL = { verified: "Verified", needs_review: "Needs review", rejected: "Could not verify" };
  RV.chips = function (item) {
    return el("span", { class: "rv-chips" },
      el("span", { class: "rv-chip rv-state-" + item.state, "data-chip": "state" }, STATE_LABEL[item.state] || item.state),
      el("span", { class: "rv-chip rv-rs-" + (item.review_status || "pending"), "data-chip": "review" }, REVIEW_LABEL[item.review_status || "pending"]));
  };

  // ---- live region
  let live;
  RV.say = function (msg, isError) {
    if (!live) { live = el("div", { id: "rv-live", class: "rv-sr", "aria-live": "polite", role: "status" }); document.body.append(live); }
    live.textContent = "";
    setTimeout(() => { live.textContent = msg; }, 20);
    if (isError) live.setAttribute("role", "alert"); else live.setAttribute("role", "status");
  };

  // ---- open the source record(s) of an item (R-RV-9); entries/amounts: one record, flags: every record in the evidence
  RV.sourceTargets = function (item, kind) {
    if (kind === "flag") {   // one span per record, so a two-record flag opens both records once each
      const seen = {}, spans = [];
      (item.evidence || []).forEach((e) => { if (!seen[e.record_id]) { seen[e.record_id] = 1; spans.push({ record_id: e.record_id, start: e.start, end: e.end }); } });
      return { ids: spans.map((s) => s.record_id), spans };
    }
    if (kind === "entry" && typeof ZL.entrySpans === "function") { const spans = ZL.entrySpans(item); return { ids: spans.map((s) => s.record_id), spans }; }
    const ids = item.record_ids || [];
    return { ids, spans: ids.length ? [{ record_id: ids[0], start: item.excerpt_start, end: item.excerpt_end }] : [] };
  };
  RV.openSource = function (item, kind, title) {   // T-042's modal: ZL.openSource(spans, title)
    const t = RV.sourceTargets(item, kind);
    if (!t.spans.length || typeof ZL.openSource !== "function") return;
    const c = RV.caseNow(), seqs = t.ids.map((id) => { const r = ((c && c.records) || []).find((x) => x.id === id); return r ? r.seq : id; });
    ZL.openSource(t.spans, title || (seqs.length > 1 ? "Records " + seqs.join(" and ") : "Record " + seqs[0]));
  };

  // ---- ordering for "next" (review.queue first, then everything else in page order)
  RV.orderedIds = function (c) {
    const all = [...(c.entries || []), ...(c.undated_entries || []), ...(c.amounts || []), ...(c.flags || [])].map((i) => i.id);
    const q = ((c.review && c.review.queue) || []).filter((id) => all.includes(id));
    return q.concat(all.filter((id) => !q.includes(id)));
  };
  RV.nextId = function (c, fromId, pendingOnly, dir) {
    const ids = RV.orderedIds(c); if (!ids.length) return null;
    const start = Math.max(0, ids.indexOf(fromId));
    for (let n = 1; n <= ids.length; n++) {
      const id = ids[(start + (dir || 1) * n + ids.length * n) % ids.length];
      const f = RV.find(c, id);
      if (!pendingOnly || (f && f.item.review_status === "pending")) return id;
    }
    return null;
  };
  function focusItem(id) {
    const q = document.querySelector('[data-testid="queue"] [data-item-id="' + id + '"]');
    const t = q || document.querySelector('[data-item-id="' + id + '"]');
    if (!t) return false;
    if (!t.hasAttribute("tabindex")) t.setAttribute("tabindex", "0");
    t.focus(); if (t.scrollIntoView) t.scrollIntoView({ block: "nearest" });
    return true;
  }
  function restoreFocus(pf) {
    if (!pf) return;
    requestAnimationFrame(() => {
      if (pf.scope) {   // decided from a flag or charge card: stay inside that panel
        const root = document.querySelector('[data-panel="' + pf.scope + '"]'); if (!root) return;
        const cards = Array.from(root.querySelectorAll("[data-item-id]")), at = cards.findIndex((x) => x.getAttribute("data-item-id") === pf.nextFrom);
        const order = cards.slice(at + 1).concat(cards.slice(0, Math.max(at, 0)));
        const t = order.find((x) => x.getAttribute("data-review") === "pending") || cards[at];
        if (t) { t.focus(); if (t.scrollIntoView) t.scrollIntoView({ block: "nearest" }); }
        return;
      }
      if (pf.nextFrom) {
        const c = RV.caseNow(); const n = c && RV.nextId(c, pf.nextFrom, true, 1);
        if (n && n !== pf.nextFrom && focusItem(n)) return;
        focusItem(pf.nextFrom); return;
      }
      const root = document.querySelector('[data-controls-for="' + pf.id + '"]');
      const t = root && (root.querySelector('[data-action="' + pf.action + '"]') || root.querySelector("button"));
      if (t) t.focus(); else focusItem(pf.id);
    });
  }

  // ---- errors and the "keep my wording" confirmation (R-RV-3)
  function slot(id, cls) { const r = document.querySelector('[data-controls-for="' + id + '"]'); return r && r.querySelector("." + cls); }
  function showError(id, msg) { const s = slot(id, "rv-error"); if (s) s.textContent = msg; RV.say(msg, true); }
  function showConfirm(id, err, body) {
    const s = slot(id, "rv-confirm"); if (!s) return;
    ZL.clear(s); s.hidden = false;
    const warns = (err.detail && err.detail.warnings) || [{ message: err.message }];
    s.append(el("p", { class: "rv-confirm-msg" }, err.message || "This edit adds something that is not in the quote."),
      el("ul", { "data-testid": "warning-list", class: "rv-warnings" }, warns.map((w) => el("li", {}, w.message))),
      el("div", { class: "rv-actions" },
        el("button", { type: "button", class: "rv-btn", "data-testid": "btn-keep-wording", onclick: () => RV.act(id, Object.assign({}, body, { confirm_warnings: true }), { focus: "edit" }) }, "Keep my wording"),
        el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-cancel-confirm", onclick: () => { s.hidden = true; ZL.clear(s); } }, "Go back and change it")));
    RV.say("This edit adds something that is not in the quote. Choose keep my wording or go back.", true);
  }

  // ---- D-041: an entry with no confirmed date cannot be accepted into the letter
------
    const reasonRow = el("form", { class: "rv-reason", hidden: !(isFlag && d.reasonOpen), onsubmit: (ev) => { ev.preventDefault(); const r = reasonIn.value.trim(); RV.act(id, r ? { action: "dismiss", note: r } : { action: "dismiss" }, { focus: "dismiss" }); } 
      reasonIn, el("button", { type: "submit", class: "rv-btn", "data-testid": "btn-dismiss-confirm" }, "Dismiss"));
    if (isFlag) root.append(reasonRow);

    if (canEdit) {
      const ta = el("textarea", { class: "rv-text", rows: "3", maxlength: "2000", name: isFlag ? "note" : "summary", "data-testid": isFlag ? "flag-note" : "edit-summary",
        "aria-label": isFlag ? "Reviewer note (internal notes only; never in the letter)" : "Summary wording" });
      ta.value = d.text;
      ta.addEventListener("input", () => { d.text = ta.value; });
      form = el("form", { class: "rv-edit", hidden: !d.open, onsubmit: (ev) => {
        ev.preventDefault(); const v = ta.value.trim();
        if (!v) { showError(id, isFlag ? "Write a note first, or cancel." : "The summary can't be empty."); return; }
        RV.act(id, { action: "edit", edits: isFlag ? { note: v } : { summary: v } }, { focus: "edit" });
      } },
        el("label", { class: "rv-label" }, isFlag ? "Your note (internal notes only, never in the letter)" : "Summary wording (the quoted excerpt, date and provider cannot be changed)", ta),
        el("div", { class: "rv-actions" },
          el("button", { type: "submit", class: "rv-btn", "data-testid": "btn-save-edit" }, "Save"),
          el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-cancel-edit", onclick: () => toggleEdit(false) }, "Cancel")));
      ta.addEventListener("keydown", (ev) => {
        if (ev.key === "Escape") { ev.stopPropagation(); toggleEdit(false); }
        else if (ev.key === "Enter" && (ev.ctrlKey || ev.metaKey)) { ev.preventDefault(); form.requestSubmit(); }
      });
      root.append(form);
      var toggleEdit = function (open) {
        d.open = open; form.hidden = !open;
        if (open) ta.focus(); else { const b = bar.querySelector('[data-action="edit"]'); if (b) b.focus(); }
      };
      ui[id] = { openEdit: () => toggleEdit(true) };
    } else ui[id] = {};
    root.append(el("div", { class: "rv-error", role: "alert" }), el("div", { class: "rv-confirm", hidden: true }));
    return root;
  };

  // ---- legend
  RV.legend = () => el("p", { class: "rv-keys" }, el("strong", {}, "Keyboard: "),
    "j next, k previous, a accept, e edit, d dismiss, r reset, o open the record, Shift+A accept all verified entries. Tab reaches every button.");

  // ---- keyboard flow (R-RV-4). Works from any focused element inside something with data-item-id.
  document.addEventListener("keydown", (ev) => {
    if (ev.ctrlKey || ev.metaKey || ev.altKey) return;
    const t = ev.target;
    if (t && (/^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName) || t.isContentEditable)) return;
    const modal = document.querySelector('[data-testid="record-modal"]'); if (modal && modal.offsetParent !== null) return;
    const row = t && t.closest && t.closest("[data-item-id]");
    const c = RV.caseNow(); if (!c) return;
    const key = ev.key.toLowerCase(); const id = row && row.getAttribute("data-item-id");
    const panel = row && row.closest("[data-panel]");
    if (panel && (key === "j" || key === "k")) {   // inside the flags / charges panels, j and k walk those cards in page order
      const cards = Array.from(document.querySelectorAll("[data-panel] [data-item-id]")), at = cards.indexOf(row), n = cards[at + (key === "j" ? 1 : -1)];
      if (n) { ev.preventDefault(); n.focus(); n.scrollIntoView({ block: "nearest" }); }
      return;
    }
    if (key === "j" || key === "k") {
      const n = RV.nextId(c, id || (c.review && c.review.queue && c.review.queue[0]), false, key === "j" ? 1 : -1);
      if (n) { ev.preventDefault(); if (!id && key === "j") focusItem((c.review.queue || [n])[0] || n); else focusItem(n); }
      return;
    }
    if (!id || !"aedro".includes(key) || key.length !== 1) return;
    const f = RV.find(c, id); if (!f || f.item.state === "rejected") return;
    ev.preventDefault();
    const scope = panel ? panel.getAttribute("data-panel") : null;
    if (key === "a") RV.act(id, { action: "accept" }, { advance: true, scope });
    else if (key === "d") RV.act(id, { action: "dismiss" }, { advance: true, scope });
    else if (key === "r") { if (f.item.review_status !== "pending") RV.act(id, { action: "reset" }, { focus: "reset" }); }
    else if (key === "o") RV.openSource(f.item, f.kind);
    else if (key === "e") { if (ui[id] && ui[id].openEdit) ui[id].openEdit(); }
  });

  // ---- registration (T-042 extension points), tolerant of load order
  function mountSection(mountEl, name) {
    let s = mountEl.querySelector(':scope > [data-panel="' + name + '"]');
    if (!s) { s = el("section", { class: "rv-panel", "data-panel": name }); mountEl.append(s); }
    return s;
  }
  RV.registerPanel = function (name, render) {
    const reg = () => ZL.registerPanel((c, mountEl) => { if (c && mountEl) render(mountSection(mountEl, name), c); });
    if (typeof ZL.registerPanel === "function") reg(); else (ZL._pendingPanels = ZL._pendingPanels || []).push(reg);
  };
  const drain = () => { (ZL._pendingPanels || []).splice(0).forEach((f) => f()); };
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", drain); else drain();
  if (typeof ZL.registerRowActions === "function") {
    ZL.registerRowActions((entry, rowEl) => {
      if (!rowEl || entry.state === "rejected" || rowEl.querySelector(":scope > .rv-controls")) return;
      rowEl.setAttribute("data-item-id", entry.id); rowEl.setAttribute("data-review", entry.review_status || "pending");
      if (!rowEl.hasAttribute("tabindex")) rowEl.setAttribute("tabindex", "0");
      rowEl.append(RV.controls(entry, "entry"));
      if (entry.entered_by_reviewer || /reviewer/i.test(entry.entered_by || "")) {   // typed by the paralegal, not drafted by the model
        const head = rowEl.querySelector(".entry-head") || rowEl;
        if (!head.querySelector('[data-testid="entered-by"]')) head.append(el("span", { class: "rv-chip rv-selfreport", "data-testid": "entered-by" }, "Entered by reviewer"));
      }
    });
  }
})();
-----
        el("p", { class: "reason", "data-testid": "tray-reason" }, `${t.reasons.map(reasonText).join("; ")}`),
        el("p", { class: "summary" }, t.why),
        t.attempt ? el("p", { class: "muted small" }, "The model's attempt (not used): " + (t.attempt.summary || "") + " — “" + (t.attempt.excerpt || "") + "”") : null,
        el("div", { class: "row-actions" }, recs.map((r) => el("button", { type: "button", class: "btn small", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], `Record ${r.seq}: ${r.source_label}`) }, `Open record ${r.seq}`))));
      box.append(item);
    });
    return box;
  }

  // ---- Why? panel
  const checkText = (v) => (v === true ? "passed" : v === false ? "FAILED" : Array.isArray(v) ? (v.length ? v.join(", ") : "none") : String(v));
  async function openWhy(id) {
    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
    const ent = [...s.case.entries, ...s.case.undated_entries].find((x) => x.id === id);
    ZL.$("#why-title").textContent = ent ? `Why? ${ent.provider}, ${ent.date || "undated"}` : "Why? this item";
    body.append(el("p", { class: "muted" }, "Loading…")); if (!dlg.open) dlg.showModal();
    try {
      const r = await ZL.api.item(s.token, id); const it = r.item, lad = it.ladder || {};
      clear(body);
      body.append(...[
        el("p", { class: "why-sentence", "data-testid": "why-text" }, it.why),
        el("dl", { class: "kv", "data-testid": "why-ladder" },
          el("dt", {}, "State"), el("dd", { "data-testid": "why-state" }, it.state + (it.reasons && it.reasons.length ? " (" + it.reasons.join(", ") + ")" : "")),
          el("dt", {}, "Backend"), el("dd", { "data-testid": "why-backend" }, lad.backend || "—"),
          lad.generator ? [el("dt", {}, "Drafted by"), el("dd", { "data-testid": "why-generator" }, `${lad.generator.model} · ${lad.generator.prompt_version}`),
            el("dt", {}, "AI draft"), el("dd", {}, lad.generator.output ? `Summary: ${lad.generator.output.summary || ""} Excerpt: ${lad.generator.output.excerpt || ""}` : "—")] : null,
          el("dt", {}, "Checks run by code"), el("dd", {}, el("ul", { class: "checks", "data-testid": "why-checks" }, Object.entries(lad.code_checks || {}).map(([k, v]) => el("li", { "data-check": k, class: v === false ? "bad" : "" }, `${k.replace(/_/g, " ")}: ${checkText(v)}`)))),
          el("dt", {}, "Second check by another model"), el("dd", { "data-testid": "why-judge" }, lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || ""}` : "none (calculated by code)")),
        r.calls && r.calls.length ? el("details", {}, el("summary", {}, `Model calls (${r.calls.length})`), el("ul", {}, r.calls.map((cl) => el("li", {}, `${cl.role} · ${cl.step} · ${cl.model} · ${cl.backend} · ${cl.latency_ms} ms · ${cl.parsed_ok ? "parsed" : "not parsed"}${cl.verdict ? " · "
    } catch (e) { clear(body); body.append(el("p", { class: "error", role: "alert" }, e.message)); }
  }
  ZL.openWhy = openWhy;

  ZL.renderReview = function (s) {
    const c = s.case, mount = ZL.$("#review-body"); clear(mount);
    if (!c || c.status !== "ready") return;
    const shown = c.entries.concat(c.undated_entries), nNeeds = shown.filter((e) => e.state === "needs_review").length, nVer = shown.filter((e) => e.state === "verified").length; // entries only; flags and amounts have their own labelled counts
    const wrap = el("div", { "data-testid": "timeline" }); mount.append(wrap);
    wrap.append(
      el("div", { class: "toolbar" },
        el("h2", {}, "Timeline"),
        el("button", { type: "button", class: "btn primary", "data-testid": "btn-export", onclick: () => ZL.openExport() }, "Export"),
        el("span", { class: "muted", "data-testid": "review-counts" }, `${shown.length} ${shown.length === 1 ? "entry" : "entries"} · ${nNeeds} needs review · ${nVer} verified` + (c.undated_entries.length ? ` (${c.undated_entries.length} in Dates to confirm below)` : "")),
        el("label", { class: "muted small" }, "Order ",
          el("select", { "data-testid": "sort", onchange: (ev) => { sortMode = ev.target.value; ZL.renderReview(ZL.state.get()); } },
            el("option", { value: "review", selected: sortMode === "review" }, "Needs review first"), el("option", { value: "date", selected: sortMode === "date" }, "By date")))),
      el("div", { class: "timeline", "data-testid": "queue" }, sortedEntries(c).map((e) => entryRow(e, c))),
      datesToConfirm(c), tray(c));
    const side = el("div", { id: "side-panels", "data-testid": "side-panels" }); wrap.append(side);
    ZL.hooks.panels.forEach((fn) => fn(c, side));
  };
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:29.890Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && grep -n \"openWhy\\|Why\" *.js | grep -v \"^mock\" | cut -c1-200; sed -n 1,99p flags.js | cut -c1-220; sed -n 20,45p timeline.js | cut -c1-260; grep -n \"case_view\\|\\\"flags\\\"\\|'flags'\" /Users/arsis/zlayt-pm-project/memory/contracts/api.md | head"
}
````

### User / tool · 2026-11-02T03:22:30.040Z

**tool result**
````
timeline.js:1:/* Review view, read-only part (T-042): timeline rows, Dates to confirm, "could not verify" tray, Why? panel. (R-TL-1, R-TL-5, R-TL-6, R-IN-5)
timeline.js:31:        el("button", { type: "button", class: "btn small", "data-testid": "entry-why", onclick: () => openWhy(e.id) }, "Why?"),
timeline.js:109:  // ---- Why? panel
timeline.js:111:  async function openWhy(id) {
timeline.js:114:    ZL.$("#why-title").textContent = ent ? `Why? ${ent.provider}, ${ent.date || "undated"}` : "Why? this item";
timeline.js:131:  ZL.openWhy = openWhy;
/* Flags panel (T-043): four groups plus "Record warnings" (R-FL-6),
   unmerged conflicts shown side by side (D-017), reviewer note only (D-010), confirm_date control for ambiguous dates.
   All server text is inserted as text nodes. */
(function () {
  const ZL = (window.ZL = window.ZL || {});
  const RV = ZL.rv, el = (...a) => ZL.el(...a);

  const GROUPS = [
    ["gap", "Treatment gaps", "No gap over 30 days found."],
    ["conflict", "Conflicts between records", "No conflicts found."],
    ["pre_existing", "Pre-existing conditions", "No earlier conditions mentioned."],
    ["causation", "Causation language", "No causation wording found."],
    ["record_warning", "Record warnings", "No record warnings."],
  ];
  const joinList = (a) => (a.length < 2 ? a.join("") : a.slice(0, -1).join(", ") + " and " + a[a.length - 1]);
  const recOf = (c, id) => (c.records || []).find((r) => r.id === id);
  const recSeq = (c, id) => { const r = recOf(c, id); return r ? r.seq : String(id).replace(/^r/, ""); };

  function evidence(c, f) {
    const ul = el("ul", { class: "rv-evidence" + (f.type === "conflict" ? " rv-side" : ""), "data-testid": "flag-evidence", "aria-label": "Quoted evidence" });
    (f.evidence || []).forEach((e) => {
      const r = recOf(c, e.record_id);
      const li = el("li", { class: "rv-ev" },
        el("span", { class: "rv-ev-cap" }, "Record " + recSeq(c, e.record_id) + (r ? " · " + r.source_label : "")),
        el("blockquote", { class: "rv-quote" }, e.excerpt));
      if (f.type === "conflict") {
        // Show the entry's own quoted line from the same record so both sides can be read without opening it.
        const en = (c.entries || []).concat(c.undated_entries || []).find((x) => (x.record_ids || []).includes(e.record_id));
        if (en && en.excerpt && en.excerpt !== e.excerpt) li.append(el("span", { class: "rv-ev-more" }, "Quoted line from this record: " + en.excerpt));
      }
      ul.append(li);
    });
    return ul;
  }

  function dateControl(c, f) {
    const rid = ((f.evidence || [])[0] || {}).record_id;
    const row = (c.dates_to_confirm || []).find((d) => d.record_id === rid);
    if (!row) return null;
    const raw = row.raw || row.date_raw || "";
    const wrap = el("form", { class: "rv-datefix", "data-testid": "confirm-date", onsubmit: (ev) => ev.preventDefault() });
    if (!(row.candidates || []).length)
      return el("p", { class: "rv-note" }, "No readable date was found for this record, so it stays off the timeline and out of the gap checks.");
    const name = "cd-" + rid; const err = el("p", { class: "rv-error", role: "alert" });
    const submit = el("button", { type: "submit", class: "rv-btn", "data-testid": "btn-confirm-date", disabled: true }, "Confirm date");
    wrap.append(el("fieldset", { class: "rv-fieldset" }, el("legend", {}, "The date “" + raw + "” can be read two ways. Choose how this record is dated:"),
      (row.candidates || []).map((cand) => el("label", { class: "rv-radio" }, el("input", { type: "radio", name, value: cand, onchange: () => { submit.disabled = false; } }), ZL.fmtDate(cand) + " (" + cand + ")"))),
      submit, err);
    wrap.addEventListener("submit", async () => {
      const v = wrap.querySelector("input:checked"); if (!v) return;
      submit.disabled = true; err.textContent = "";
      try {
        await ZL.api.confirmDate(c.token, rid, v.value);
        ZL.state.set({ case: await ZL.api.getCase(c.token) });   // timeline, gaps and warnings are recomputed by the backend
        RV.say("Date confirmed as " + v.value + ".");
      } catch (e) { err.textContent = (e && e.message) || "That date could not be confirmed."; submit.disabled = false; RV.say(err.textContent, true); }
    });
    return wrap;
  }

  function card(c, f) {
    const seqs = (RV.sourceTargets(f, "flag").ids || []).map((id) => recSeq(c, id));
    const note = f.reviewer_note || (f.edited && f.edited.note);
    const a = el("article", { class: "rv-card rv-flag", tabindex: "0", role: "group", "aria-label": f.title, "data-testid": "flag-" + f.id, "data-item-id": f.id,
      "data-flag-type": f.type, "data-category": f.category, "data-state": f.state, "data-review": f.review_status || "pending" },
      el("div", { class: "rv-head" }, el("h4", { class: "rv-title" }, f.title), RV.chips(f)),
      el("p", { class: "rv-text-body" }, f.explanation),
      f.state === "needs_review" && f.why ? el("p", { class: "rv-reason-line" }, el("strong", {}, "Needs review: "), f.why) : f.why ? el("p", { class: "rv-why" }, f.why) : null,
      evidence(c, f));
    if (f.category === "date_ambiguous") { const dc = dateControl(c, f); if (dc) a.append(dc); }
    if (note) a.append(el("p", { class: "rv-usernote", "data-testid": "flag-note-text" }, el("strong", {}, f.review_status === "dismissed" ? "Dismissed because: " : "Your note: "), note));
    if (seqs.length)
      a.append(el("div", { class: "rv-actions" }, el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-source", onclick: () => RV.openSource(f, "flag") },
        seqs.length > 1 ? "Open records " + joinList(seqs) : "Open record " + seqs[0])));
    a.append(RV.controls(f, "flag"));
    return a;
  }

  function render(root, c) {
    ZL.clear(root);
    root.setAttribute("data-testid", "flags-panel");
    root.setAttribute("aria-labelledby", "rv-flags-h");
    root.append(el("h2", { id: "rv-flags-h" }, "Flags"),
      el("p", { class: "rv-help" }, "Flags point to things worth checking. Accepting one means you have seen it: it goes to the internal notes, never into the letter."),
      RV.legend());
    if (c.injection && c.injection.banner) root.append(el("p", { class: "rv-banner", role: "note" }, c.injection.banner));
    const flags = c.flags || [];
    GROUPS.forEach(([type, title, empty]) => {
      const list = RV.needsReviewFirst(flags.filter((f) => f.type === type));
      const g = el("section", { class: "rv-group", "data-group": type, "aria-labelledby": "rv-g-" + type },
        el("h3", { id: "rv-g-" + type }, title + " (" + list.length + ")"));
      if (!list.length) g.append(el("p", { class: "rv-empty" }, empty));
      list.forEach((f) => g.append(card(c, f)));
      root.append(g);
    });
  }
  RV.registerPanel("flags", render);
  RV.renderFlags = render;
})();
      el("div", { class: "entry-head" },
        el("span", { class: "date", "data-testid": "entry-date" }, e.date || "undated"),
        el("span", { class: "provider", "data-testid": "entry-provider" }, (!e.date && rec ? `Record ${rec.seq}: ` : "") + e.provider),
        stateChip(e),
        el("span", { class: "chip rs-" + e.review_status, "data-testid": "review-status" }, REVIEW_LABEL[e.review_status] || e.review_status)),
      el("p", { class: "summary", "data-testid": "entry-summary" }, e.summary, e.ai_drafted ? el("span", { class: "tag" }, "AI-drafted") : null),
      e.edited ? el("p", { class: "muted small", "data-testid": "edited-note" }, "Edited by you. Original: " + e.edited.original_summary) : null,
      el("blockquote", { class: "excerpt", "data-testid": "entry-excerpt" }, e.excerpt),
      e.duplicate_note ? el("p", { class: "muted small" }, e.duplicate_note) : null,
      e.state === "needs_review" && e.reasons.length ? el("p", { class: "reason", "data-testid": "entry-reasons" }, "Check: " + e.reasons.map(reasonText).join("; ")) : null,
      el("div", { class: "row-actions", "data-testid": "row-actions" },
        el("button", { type: "button", class: "btn small", "data-testid": "entry-why", onclick: () => openWhy(e.id) }, "Why?"),
        el("button", { type: "button", class: "btn small", "data-testid": "btn-source", onclick: () => ZL.openSource(ZL.entrySpans(e), `Record ${rec ? rec.seq : ""}: ${e.provider}`) }, !e.date && rec ? `Open record ${rec.seq}` : "Open record"))].filter(Boolean
    ZL.hooks.rowActions.forEach((fn) => fn(e, row));
    return row;
  }
  function sortedEntries(c) {
    const byDate = (a, b) => (a.date < b.date ? -1 : a.date > b.date ? 1 : a.seq - b.seq);
    const list = c.entries.slice().sort(byDate);
    if (sortMode === "date") return list;
    const rank = (e) => ZL.firstRank(e.id, e.state);
    return list.sort((a, b) => rank(a) - rank(b) || byDate(a, b));
  }
  // The record's own quoted text (verbatim, as in the record body), shown so the date can be judged next to what the record says.
  function recordExcerpt(rec) {
    const m = /(?:^|\n)Excerpt:\s*"?([\s\S]*?)"?\s*$/.exec(rec.text || "");
92:  "stages": ["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],
94:  "counts": {"entries": 9, "amounts": 3, "flags": 1},
157:  "flags": [
383:    "flags": [
527:    { "id": "flags", "kind": "code", "counts": {"total": 4, "by_type": {"gap": 1}, "by_origin": {"code": 2, "llm": 1}} },
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:36.251Z

**tool call — Bash**
````
{
 "command": "cd <home-path> && sed -n 2149,2230p app.py | cut -c1-200; grep -n \"flow-rail\" app.py | head -30; sed -n 960,1040p app.py | cut -c1-220; cd /Users/arsis/zlayt-pm-project; grep -n \"uvicorn\\|7860\\|FIXTURE_SET\" Makefile run.sh docs/RUNBOOK.md | head"
}
````

### User / tool · 2026-11-02T03:22:36.377Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:38.338Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh; ls tests/e2e/../; ls artifacts/screenshots | head; sed -n 1,40p tests/e2e/test_flags_panel.py; cat tests/unit/test_e2e_contract.py | head -50; lsof -i :7860 -i :7871 | head"
}
````

### User / tool · 2026-11-02T03:22:38.575Z

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
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit
m0-board-mobile.png
m0-board.png
office-desktop.png
office-floors-desktop-all.png
office-floors-desktop-board.png
office-floors-desktop-default.png
office-floors-desktop-floor0.png
office-floors-desktop-floor1.png
office-floors-desktop-floor2.png
office-floors-desktop-trip.png
"""Flags panel. R-FL-1..R-FL-7, R-RV-2 (note only)."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE


def flags(page): return page.get_by_test_id("flags-panel")

def test_73_day_gap_flag_and_no_28_day(page, sample_case):
    """R-FL-1: the gap flag says 73 days; no flag mentions 28 days."""
    open_case(page, sample_case); t = flags(page).inner_text(); assert "73" in t and "28 days" not in t

def test_both_conflicts_present_not_merged(page, sample_case):
    """R-FL-2: accident-date conflict (shows 2026-01-19 and the EMS sentence) and PT-plan conflict."""
    open_case(page, sample_case); t = flags(page).inner_text()
    assert "2026-01-19" in t and "rear-ended" in t and "12 visits" in t

def test_patient_self_report_label(page, sample_case):
    """R-FL-7: the record-9 causation flag shows 'Reported onset'."""
    open_case(page, sample_case); assert "Reported onset" in flags(page).inner_text()

def test_flag_edit_is_note_only(page, sample_case):
    """R-RV-2: the only editable field on a flag is the reviewer note."""
    open_case(page, sample_case); f = flags(page).locator("[data-flag-type=gap]").first
    assert f.get_by_test_id("flag-note").count() == 1 and f.get_by_test_id("edit-summary").count() == 0

def test_no_causation_conclusion_words(page, sample_case):
    """R-FL-4: flag text never says 'caused by' or 'non-compliant'."""
    open_case(page, sample_case); t = flags(page).inner_text().lower(); assert "caused by" not in t and "non-compliant" not in t
"""E2E hook contract (R-ST-1, R-RV-8): every data-testid, data-attribute, role and shortcut used by tests/e2e specs is declared in tests/e2e/conftest.py's docstring,
so the frontend builds to one source (T-039 review)."""
import pathlib, re
E2E = pathlib.Path(__file__).resolve().parents[1] / "e2e"

def contract():
    s = (E2E / "conftest.py").read_text().split('"""')[1]
    return s

def specs():
    return [p for p in E2E.glob("test_*.py")]

def test_every_test_id_is_declared():
    """R-ST-1: get_by_test_id hooks in specs are named in the conftest contract (<seq>/<raw> placeholders allowed)."""
    c = contract(); used = set()
    for p in specs():
        for m in re.finditer(r'get_by_test_id\(f?"([^"]+)"\)', p.read_text()):
            used.add(re.sub(r"entry-\d+$", "entry-<seq>", re.sub(r"\{[^}]*\}", "<seq>", m.group(1))))
    missing = []
    for u in used:
        pat = u.replace("<seq>", "<seq>") 
        if pat not in c and not (u.startswith("amount-") and "amount-<raw>" in c):
            missing.append(u)
    assert not missing, missing

def test_data_attributes_declared():
    """R-RV-1: data-review, data-state, data-flag-type used by specs are declared."""
    c = contract()
    for p in specs():
        for a in set(re.findall(r"data-[a-z-]+", p.read_text())):
            assert a in c, (p.name, a)

def test_roles_and_inputs_and_keys_declared():
    """R-RV-8: role=alert, tabindex, input names and a/d/j shortcuts are declared."""
    c = contract()
    for needle in ("role=alert", "tabindex", "input named date or provider", "a = accept", "d = dismiss", "j = next"):
        assert needle in c
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  54486 arsis    9u  IPv4 0x502ad09bd6429476      0t0  TCP localhost:7860 (LISTEN)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:40.545Z

**tool call — Bash**
````
{
 "command": "grep -n \"PORT\\|port\" app/main.py app/config.py 2>/dev/null | head; mkdir -p artifacts/tmp; (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=artifacts/tmp/frontend-t081.sqlite3 PORT=7871 nohup .venv/bin/python -m app.main > artifacts/tmp/frontend-t081.log 2>&1 &) ; sleep 4; curl -s localhost:7871/api/health"
}
````

### User / tool · 2026-11-02T03:22:44.665Z

**tool result**
````
2:import os
4:import uvicorn
6:from app.backend.api import create_app
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only — never paste real records","backend":"fixture","demo_mode":true,"live_enabled":false,"models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"limits":{"max_chars":60000,"max_records":40},"retention_hours":24,"ai_banner":"Summaries and flags are drafted by AI and checked by code; you decide every item","sample_available":true}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:47.400Z

**tool call — Bash**
````
{
 "command": "B=http://localhost:7871/api; TOK=$(curl -s -XPOST $B/cases -H 'content-type: application/json' -d '{\"sample\":true}' | .venv/bin/python -c \"import sys,json;print(json.load(sys.stdin)['token'])\"); curl -s -XPOST $B/cases/$TOK/run -d '{}' -H 'content-type: application/json' >/dev/null; sleep 6; curl -s $B/cases/$TOK/status; echo $TOK > artifacts/tmp/tok.txt; curl -s $B/cases/$TOK/trace | .venv/bin/python -m json.tool | head -150"
}
````

### User / tool · 2026-11-02T03:22:53.638Z

**tool result**
````
{"token":"zDa_F3l_oQWOa5Ha5L3Q8w","status":"ready","stage":"finalize","stages":["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],"progress":{"done":7,"total":8,"label":"Step 8 of 8: finalize"},"counts":{"entries":9,"amounts":4,"flags":10},"error":null,"elapsed_ms":175}{
    "token": "zDa_F3l_oQWOa5Ha5L3Q8w",
    "mode": "full",
    "status": "ready",
    "verdict": {
        "code": "needs_attention",
        "label": "23 items still need your decision"
    },
    "progress": {
        "done": 8,
        "total": 10,
        "label": "8 of 10 steps settled"
    },
    "steps": [
        {
            "id": "ingest",
            "label": "Read the paste and split it into records",
            "kind": "code",
            "status": "pass",
            "why": "9 records found.",
            "reason_code": null,
            "rule": "row 1",
            "blocks_export": false,
            "evidence": {},
            "next_action": null,
            "counts": {
                "records": 9,
                "duplicates_merged": 0,
                "characters": 1877
            },
            "n": 1
        },
        {
            "id": "split",
            "label": "Record boundaries",
            "kind": "code",
            "status": "pass",
            "why": "The record markers in the paste decided where each record starts and ends.",
            "reason_code": null,
            "rule": "row 1",
            "blocks_export": false,
            "evidence": {},
            "next_action": null,
            "counts": {
                "method": "code",
                "llm_split": false
            },
            "n": 2
        },
        {
            "id": "dates",
            "label": "Dates read by code",
            "kind": "code",
            "status": "pass",
            "why": "Every record date was read by code and is parsed or confirmed.",
            "reason_code": null,
            "rule": "row 2",
            "blocks_export": false,
            "evidence": {},
            "next_action": null,
            "counts": {
                "parsed": 9,
                "confirmed": 0,
                "ambiguous": 0,
                "missing": 0
            },
            "n": 3
        },
        {
            "id": "extract",
            "label": "AI drafts a summary and a quote for each record",
            "kind": "llm",
            "status": "pass",
            "why": "The AI drafted an entry for all 9 records.",
            "reason_code": null,
            "rule": "row 4",
            "blocks_export": false,
            "evidence": {},
            "next_action": null,
            "counts": {
                "records_to_draft": 9,
                "entries": 9,
                "rejected": 0,
                "records_without_entry": 0
            },
            "n": 4
        },
        {
            "id": "grounding",
            "label": "Every quote and amount is in the record",
            "kind": "code",
            "status": "pass",
            "why": "All 23 items cite text that is in the record, character for character.",
            "reason_code": null,
            "rule": "row 4",
            "blocks_export": false,
            "evidence": {},
            "next_action": null,
            "counts": {
                "items_checked": 23,
                "rejected": 0,
                "reasons": {}
            },
            "n": 5
        },
        {
            "id": "judges",
            "label": "Second AI check on every AI-made item",
            "kind": "llm",
            "status": "pass",
            "why": "The second check agreed with all 19 items it checked.",
            "reason_code": null,
            "rule": "row 4",
            "blocks_export": false,
            "evidence": {},
            "next_action": null,
            "counts": {
                "items_judged": 19,
                "supported": 19,
                "unsupported": 0,
                "unsure": 0,
                "unavailable": 0,
                "human_overrides": 0
            },
            "n": 6
        },
        {
            "id": "flags",
            "label": "Gaps, conflicts and wording flags",
            "kind": "code",
            "status": "pass",
            "why": "10 flags: dates compared by code, wording found by the phrase list and the AI.",
            "reason_code": null,
            "rule": "row 9",
            "blocks_export": false,
            "evidence": {},
            "next_action": null,
            "counts": {
                "total": 10,
                "by_type": {
                    "gap": 1,
                    "conflict": 2,
                    "pre_existing": 2,
                    "causation": 5
                },
                "by_origin": {
                    "code": 2,
                    "llm": 1,
                    "lexicon+llm": 6,
                    "lexicon": 1
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:22:56.729Z

**tool call — Bash**
````
{
 "command": "B=http://localhost:7871/api; TOK=$(cat artifacts/tmp/tok.txt); curl -s $B/cases/$TOK/trace | .venv/bin/python -c \"\nimport sys,json;d=json.load(sys.stdin)\nfor s in d['steps'][6:]:\n  print(s['id'],s['status'],s.get('reason_code'),s['counts'],s['why'][:100]); \nprint(json.dumps(d['steps'][-1],indent=1)[:2500])\"; curl -s $B/library | head -c 1500; curl -s $B/cases/$TOK/judges | head -c 1500"
}
````

### User / tool · 2026-11-02T03:22:56.862Z

**tool result**
````
flags pass None {'total': 10, 'by_type': {'gap': 1, 'conflict': 2, 'pre_existing': 2, 'causation': 5}, 'by_origin': {'code': 2, 'llm': 1, 'lexicon+llm': 6, 'lexicon': 1}} 10 flags: dates compared by code, wording found by the phrase list and the AI.
totals pending PENDING_DECISION {'accepted_cents': 0, 'accepted_count': 0, 'pending_cents': 839000, 'pending_charges': 2, 'not_totaled': 1} 2 detected charges not in the total until you accept them. The total is added up by code from accept
review pending PENDING_DECISION {'pending': 23, 'accepted': 0, 'edited': 0, 'dismissed': 0} 23 items are waiting for your decision.
export_gate fail ITEMS_PENDING {'blocking': 23, 'pending_items': 23, 'accepted': 0, 'dismissed': 0, 'rejected_not_blocking': 0} 23 items have no decision yet, so the export is blocked.
{
 "id": "export_gate",
 "label": "Ready to export?",
 "kind": "code",
 "status": "fail",
 "why": "23 items have no decision yet, so the export is blocked.",
 "reason_code": "ITEMS_PENDING",
 "rule": "row 19",
 "blocks_export": true,
 "evidence": {},
 "next_action": {
  "code": "DECIDE",
  "text": "Accept, edit or dismiss this item.",
  "target": {
   "item_id": "e1"
  },
  "options": [
   "accept",
   "edit",
   "dismiss"
  ]
 },
 "counts": {
  "blocking": 23,
  "pending_items": 23,
  "accepted": 0,
  "dismissed": 0,
  "rejected_not_blocking": 0
 },
 "ready": false,
 "blockers": [
  {
   "item_id": "e1",
   "kind": "entry",
   "reason_code": "PENDING_DECISION",
   "why": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
   "next_action": {
    "code": "DECIDE",
    "text": "Accept, edit or dismiss this item.",
    "target": {
     "item_id": "e1"
    },
    "options": [
     "accept",
     "edit",
     "dismiss"
    ]
   }
  },
  {
   "item_id": "e2",
   "kind": "entry",
   "reason_code": "PENDING_DECISION",
   "why": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
   "next_action": {
    "code": "DECIDE",
    "text": "Accept, edit or dismiss this item.",
    "target": {
     "item_id": "e2"
    },
    "options": [
     "accept",
     "edit",
     "dismiss"
    ]
   }
  },
  {
   "item_id": "e3",
   "kind": "entry",
   "reason_code": "PENDING_DECISION",
   "why": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
   "next_action": {
    "code": "DECIDE",
    "text": "Accept, edit or dismiss this item.",
    "target": {
     "item_id": "e3"
    },
    "options": [
     "accept",
     "edit",
     "dismiss"
    ]
   }
  },
  {
   "item_id": "e4",
   "kind": "entry",
   "reason_code": "PENDING_DECISION",
   "why": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
   "next_action": {
    "code": "DECIDE",
    "text": "Accept, edit or dismiss this item.",
    "target": {
     "item_id": "e4"
    },
    "options": [
     "accept",
     "edit",
     "dismiss"
    ]
   }
  },
  {
   "item_id": "e5",
   "kind": "entry",
   "reason_code": "PENDING_DECISION",
   "why": "You have not accepted, edited or dismissed this item yet, so it stays out of the letter.",
   "next_action": {
    "code": "DECIDE",
    "text": "Accept, edit or dismiss this item.",
    "target": {
     "item_id": "e5"
    },
    "op
{"cases":[{"id":"case_lib01_er_only_then_gap","name":"case lib01 er only then gap","description":"Library L1 (mirrors S1). Rear-end collision, ED visit and a negative x-ray, then the first primary-care visit 44 days later with a new arm symptom and a patient-stated reason for the delay. The gap is flagged; the reason is shown as the pat"},{"id":"case_lib02_slip_fall_prior_knee","name":"case lib02 slip fall prior knee","description":"Library L2 (mirrors S2). Store slip-and-fall with a prior knee arthroscopy shown in imaging and in the patient's history; MRI wording that may reflect both acute and prior change. The tool shows the prior-condition language and the hedge an"},{"id":"case_lib03_truck_rear_end_chiro","name":"case lib03 truck rear end chiro","description":"Library L3 (mirrors S3). Passenger car struck from behind by a tractor-trailer; chiropractic plan of 36 visits, no change in pain score at visit 14, discharge at maximum benefit after 31 visits, then an MRI 35 days later with hedged chronic"},{"id":"case_lib04_dog_bite_scar_revision","name":"case lib04 dog bite scar revision","description":"Library L4 (mirrors S4). Facial dog bite repaired in the ED, plastic-surgery follow-ups with scar photographs, a planned 8-week interval that the tool still flags, a $6,500 revision estimate and a later revision with a surgeon fee. The tool"},{"id":"case_lib05_pedestrian_orif_hardware","name":"case lib05 pedestrian orif hardware","description":"Library L5 (mirrors S5). Pedestria{"token":"zDa_F3l_oQWOa5Ha5L3Q8w","mode":"full","models":{"generator":"claude-sonnet-5-5","judge":"claude-haiku-5-5"},"independent_models":true,"totals":{"items_judged":19,"supported":19,"unsupported":0,"unsure":0,"unavailable":0,"human_overrides":0},"judges":[{"id":"j1","label":"Is the summary supported by the quote?","prompt_version":"judge_faithfulness_v1","models":["claude-haiku-5-5"],"items":9,"supported":9,"partially":0,"unsupported":0,"disagrees":0,"unsure":0,"unavailable":0},{"id":"j2","label":"Is this figure a charge, rate or estimate?","prompt_version":"judge_amount_class_v1","models":["claude-haiku-5-5"],"items":3,"supported":3,"partially":0,"unsupported":0,"disagrees":0,"unsure":0,"unavailable":0},{"id":"j3","label":"Do these two quotes really conflict?","prompt_version":"judge_conflict_v2","models":["claude-haiku-5-5"],"items":1,"supported":1,"partially":0,"unsupported":0,"disagrees":0,"unsure":0,"unavailable":0},{"id":"j4","label":"Does this flag fit the quote?","prompt_version":"judge_flag_v2","models":["claude-haiku-5-5"],"items":6,"supported":6,"partially":0,"unsupported":0,"disagrees":0,"unsure":0,"unavailable":0}],"rejections":[],"unresolved":[],"disagreements":[{"item_id":"f_r7_1","kind":"flag","type":"sources_disagree","code_says":"The phrase list found it.","judge_says":"The AI did not find it.","resolution":"needs_review","review_status":"pending"}],"prompt_versions":["judge_amount_class_v1","judge_conflict_v2","judge_faithfulness_v1","judge_flag_v2"]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:23:01.397Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport json,urllib.request,time\nB=\"http://localhost:7871/api\"\ndef api(m,p,b=None):\n    r=urllib.request.Request(B+p,method=m,data=json.dumps(b).encode() if b is not None else None,headers={\"Content-Type\":\"application/json\"})\n    try:\n        with urllib.request.urlopen(r,timeout=60) as x: raw=x.read(); return x.status,(json.loads(raw) if raw else None)\n    except urllib.error.HTTPError as e: return e.code,json.loads(e.read() or b\"null\")\nlib=api(\"GET\",\"/library\")[1][\"cases\"]\nout={}\nfor c in lib:\n    st,r=api(\"POST\",\"/cases\",{\"library\":c[\"id\"]}); tok=r[\"token\"]; api(\"POST\",f\"/cases/{tok}/run\",{})\n    for _ in range(40):\n        s=api(\"GET\",f\"/cases/{tok}/status\")[1]\n        if s[\"status\"] in(\"ready\",\"failed\"):break\n        time.sleep(.5)\n    j=api(\"GET\",f\"/cases/{tok}/judges\")[1]; t=api(\"GET\",f\"/cases/{tok}/trace\")[1]\n    print(c[\"id\"],s[\"status\"],j[\"totals\"],len(j[\"rejections\"]),len(j[\"unresolved\"]),len(j[\"disagreements\"]),[ (x['id'],x['status']) for x in t['steps'] if x['status']!='pass'],tok)\nEOF"
}
````

### User / tool · 2026-11-02T03:23:05.016Z

**tool result**
````
case_lib01_er_only_then_gap ready {'items_judged': 8, 'supported': 8, 'unsupported': 0, 'unsure': 0, 'unavailable': 0, 'human_overrides': 0} 0 0 1 [('extract', 'fail'), ('totals', 'pending'), ('review', 'pending'), ('export_gate', 'fail')] ARa80fnvH0dImRuVlf-BPw
case_lib02_slip_fall_prior_knee ready {'items_judged': 16, 'supported': 16, 'unsupported': 0, 'unsure': 0, 'unavailable': 0, 'human_overrides': 0} 0 0 5 [('totals', 'pending'), ('review', 'pending'), ('export_gate', 'fail')] pSnqQ9z0f9CExyQ4vK62OQ
case_lib03_truck_rear_end_chiro ready {'items_judged': 13, 'supported': 12, 'unsupported': 1, 'unsure': 0, 'unavailable': 0, 'human_overrides': 0} 1 0 2 [('judges', 'fail'), ('totals', 'pending'), ('review', 'pending'), ('export_gate', 'fail')] fCRX_feKIec2BdgRm_PXog
case_lib04_dog_bite_scar_revision ready {'items_judged': 9, 'supported': 8, 'unsupported': 1, 'unsure': 0, 'unavailable': 0, 'human_overrides': 0} 1 0 1 [('judges', 'fail'), ('totals', 'pending'), ('review', 'pending'), ('export_gate', 'fail')] 7MMf2VRsEPOjNeiNQvhM9w
case_lib05_pedestrian_orif_hardware ready {'items_judged': 14, 'supported': 12, 'unsupported': 2, 'unsure': 0, 'unavailable': 0, 'human_overrides': 0} 2 0 4 [('judges', 'fail'), ('totals', 'pending'), ('review', 'pending'), ('export_gate', 'fail')] KiYMF7nwXOQPLtV4pJsqQg
case_lib06_lop_billed_vs_adjusted ready {'items_judged': 16, 'supported': 13, 'unsupported': 3, 'unsure': 0, 'unavailable': 0, 'human_overrides': 0} 3 0 7 [('judges', 'fail'), ('totals', 'pending'), ('review', 'pending'), ('export_gate', 'fail')] TZxnjsY6Lkcukz7bUsgsgQ
case_lib07_parking_lot_fall_outside_records ready {'items_judged': 16, 'supported': 15, 'unsupported': 1, 'unsure': 0, 'unavailable': 0, 'human_overrides': 0} 1 0 4 [('judges', 'fail'), ('totals', 'pending'), ('review', 'pending'), ('export_gate', 'fail')] 57kH7Qjh5VgGh0nNrN2_vg
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:23:08.845Z

**tool call — Bash**
````
{
 "command": "B=http://localhost:7871/api; T=TZxnjsY6Lkcukz7bUsgsgQ; curl -s $B/cases/$T/judges | .venv/bin/python -c \"\nimport sys,json;d=json.load(sys.stdin);print(json.dumps({k:d[k] for k in ('rejections','unresolved','disagreements')},indent=1)[:3500])\"; R=$(curl -s $B/cases/$T/judges | .venv/bin/python -c \"import sys,json;print(json.load(sys.stdin)['rejections'][0]['item_id'])\"); curl -s $B/cases/$T/items/$R/trace | .venv/bin/python -c \"\nimport sys,json;d=json.load(sys.stdin)\nprint({k:v for k,v in d.items() if k!='steps'})\nfor s in d['steps']: print(s['n'],s['id'],s['kind'],s['status'],s.get('reason_code'),list(s['evidence']),'|',s['why'][:90],'|',(s['next_action'] or {}).get('code'))\""
}
````

### User / tool · 2026-11-02T03:23:09.092Z

**tool result**
````
{
 "rejections": [
  {
   "item_id": "a3",
   "kind": "amount",
   "judge": "j2",
   "verdict": "disagrees",
   "model": "claude-haiku-5-5",
   "prompt_version": "judge_amount_class_v1",
   "call_id": "c3c949bf091eb",
   "review_status": "pending",
   "reason_code": "SHOULD_BE_CHARGE",
   "rationale": "The second check reads this figure as a billed charge.",
   "state_reason": "JUDGE_DISAGREES",
   "response_raw": "{\"reason_code\": \"SHOULD_BE_CHARGE\", \"verdict\": \"disagree\"}"
  },
  {
   "item_id": "a7",
   "kind": "amount",
   "judge": "j2",
   "verdict": "disagrees",
   "model": "claude-haiku-5-5",
   "prompt_version": "judge_amount_class_v1",
   "call_id": "c3d633e14038c",
   "review_status": "pending",
   "reason_code": "SHOULD_BE_CHARGE",
   "rationale": "The second check reads this figure as a billed charge.",
   "state_reason": "JUDGE_DISAGREES",
   "response_raw": "{\"reason_code\": \"SHOULD_BE_CHARGE\", \"verdict\": \"disagree\"}"
  },
  {
   "item_id": "f_r5_1",
   "kind": "flag",
   "judge": "j4",
   "verdict": "disagrees",
   "model": "claude-haiku-5-5",
   "prompt_version": "judge_flag_v2",
   "call_id": "ce56686fb894e",
   "review_status": "pending",
   "reason_code": "NOT_SUPPORTED_BY_QUOTE",
   "rationale": "The second check does not find this flag supported by the quote.",
   "state_reason": "JUDGE_DISAGREES",
   "response_raw": "{\"reason_code\": \"NOT_SUPPORTED_BY_QUOTE\", \"verdict\": \"disagree\"}"
  }
 ],
 "unresolved": [],
 "disagreements": [
  {
   "item_id": "e5",
   "kind": "entry",
   "type": "judge_agrees_code_flags",
   "code_says": "The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.",
   "judge_says": "The second check found every statement in the summary in the quote.",
   "resolution": "needs_review",
   "review_status": "pending"
  },
  {
   "item_id": "a3",
   "kind": "amount",
   "type": "judge_objects",
   "code_says": "unclear",
   "judge_says": "charge (SHOULD_BE_CHARGE)",
   "resolution": "needs_review",
   "review_status": "pending"
  },
  {
   "item_id": "a7",
   "kind": "amount",
   "type": "judge_objects",
   "code_says": "unclear",
   "judge_says": "charge (SHOULD_BE_CHARGE)",
   "resolution": "needs_review",
   "review_status": "pending"
  },
  {
   "item_id": "f_r5_1",
   "kind": "flag",
   "type": "judge_objects",
   "code_says": "All code checks passed.",
   "judge_says": "The second check does not find this flag supported by the quote.",
   "resolution": "needs_review",
   "review_status": "pending"
  },
  {
   "item_id": "f_r5_1",
   "kind": "flag",
   "type": "sources_disagree",
   "code_says": "The phrase list did not find it.",
   "judge_says": "The AI found it.",
   "resolution": "needs_review",
   "review_status": "pending"
  },
  {
   "item_id": "f_r3_2",
   "kind": "flag",
   "type": "sources_disagree",
   "code_says": "The phrase list found it.",
   "judge_says": "The AI did not find it.",
   "resolution": "needs_review",
   "review_status": "pending"
  },
  {
   "item_id": "f_r4_1",
   "kind": "flag",
   "type": "sources_disagree",
   "code_says": "The phrase list found it.",
   "judge_says": "The AI did not find it.",
   "resolution": "needs_review",
   "review_status": "pending"
  }
 ]
}
{'token': 'TZxnjsY6Lkcukz7bUsgsgQ', 'item_id': 'a3', 'kind': 'amount', 'mode': 'full', 'state': 'needs_review', 'review_status': 'pending', 'state_reasons': [{'code': 'JUDGE_DISAGREES', 'why': 'A second AI check disagreed with the first result for this item.', 'step_id': 'judge_2'}, {'code': 'AMOUNT_UNCLEAR', 'why': 'This figure could not be read or labelled with confidence, so it is not added to the total.', 'step_id': 'amount_class'}], 'verdict': {'code': 'needs_attention', 'label': 'Needs your attention', 'blocks_export': True}, 'progress': {'done': 5, 'total': 6, 'label': '5 of 6 steps settled'}, 'next_action': {'code': 'READ_RECORD', 'text': 'Read the record yourself before relying on this item.', 'target': {'record_id': 'r4'}}}
1 found_in_text code pass None ['excerpt', 'values'] | Code found this figure in the record by pattern; it is not a model's claim. | None
2 amount_class code fail AMOUNT_UNCLEAR ['values'] | This figure could not be read or labelled with confidence, so it is not added to the total | READ_RECORD
3 injection_scan code pass None [] | The record has no instruction-like text. | None
4 judge_2 llm fail JUDGE_DISAGREES ['model', 'prompt_version', 'prompt_sha256', 'backend', 'recorded_from', 'latency_ms', 'parsed_ok', 'call_id', 'response_raw', 'judge_verdict', 'judge_reason_code', 'rationale'] | A second AI check disagreed with the first result for this item. The second check reads th | COMPARE_BY_HAND
5 total_inclusion code skipped AMOUNT_UNCLEAR [] | This figure could not be read or labelled with confidence, so it is not added to the total | None
6 human human pending PENDING_DECISION ['action', 'at', 'events'] | You have not accepted, edited or dismissed this item yet, so it stays out of the letter. | DECIDE
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:24:01.018Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -n 1,91p charges.js | cut -c1-240; cat export.js | cut -c1-240 | head -60; B=http://localhost:7871/api; curl -s $B/cases/TZxnjsY6Lkcukz7bUsgsgQ | .venv/bin/python -c \"\" 2>/dev/null; cd ..; cd ..; curl -s $B/cases/TZxnjsY6Lkcukz7bUsgsgQ | .venv/bin/python -c \"\nimport sys,json;d=json.load(sys.stdin)\nprint(d.keys()); print(d['amounts'][0]); print(d['flags'][0].keys()); print(d['entries'][0].keys()); print(d.get('narrative') and list(d['narrative'])[:5])\""
}
````

### User / tool · 2026-11-02T03:24:01.175Z

**tool result**
````
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
      el("button", { type: "button", class: "rv-btn rv-secondary", "data-testid": "btn-source", onclick: () => RV.openSource(a, "amount") }, "Open record " + recSeq(c, (a.record_ids || [])[0])));
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
        el("p", { class: "rv-total rv-total-main", "data-testid": "accepted-total", "aria-live": "polite" }, el("span", { class: "rv-total-label" }, "Accepted charges: "), el("strong", {}, RV.money(acc))),
        el("p", { class: "rv-total rv-total-pending", "data-testid": "pending-total" }, "Detected, not yet accepted: " + RV.money(pendObj.cents || 0) + " (not a total)")));
    root.append(el("h3", {}, "Detected charges (" + charges.length + ")"));
    if (charges.length) root.append(table(c, charges, "Detected charges", false)); else root.append(el("p", { class: "rv-empty" }, "No charges were found."));
    const tray = el("section", { class: "rv-tray", "data-testid": "unclear-tray", "aria-labelledby": "rv-unclear-h" },
      el("h3", { id: "rv-unclear-h" }, "Unclear — not totaled (" + unclear.length + ")"));
    if (unclear.length) tray.append(table(c, unclear, "Unclear amounts, not totaled", true)); else tray.append(el("p", { class: "rv-empty" }, "Nothing unclear."));
    root.append(tray);
  }
  RV.registerPanel("charges", render);
  RV.renderCharges = render;
})();
/* Export view (T-044): two separate copy blocks built by the SERVER (letter_text / internal_notes_text); the UI only displays and copies them verbatim.
   Count line sits outside both blocks (R-EX-5). Copy asks for one confirmation when anything is pending (names pending flags separately). */
(function () {
  const ZL = window.ZL, { el, clear } = ZL;
  let open = false, data = null, timer = null, confirmFor = null;

  const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
  function countLine(c) {
    return `${plural(c.entries, "entry", "entries")}, ${plural(c.charges, "charge", "charges")} in letter · ${plural(c.flags_in_notes, "flag", "flags")} in internal notes · ${c.records_in_letter} of ${c.records_total} records in letter ·
  }
  function status(msg, bad) { const s = ZL.$("#export-status"); if (s) { s.textContent = msg || ""; s.className = bad ? "error" : "muted"; } }
  async function copy(text, which) {
    try { await navigator.clipboard.writeText(text); status(`Copied the ${which}.`); }
    catch (_) { status("The browser blocked copying. Select the text in the box and copy it by hand.", true); }
  }
  function askConfirm(c, then) {
    const box = ZL.$("#export-confirm"); clear(box); box.hidden = false;
    const flags = c.pending_flags, others = c.pending - flags;
    const parts = [];
    if (flags) parts.push(`${plural(flags, "flag", "flags")} not reviewed`);
    if (others) parts.push(`${plural(others, "other item", "other items")} not reviewed`);
    box.append(el("p", { class: "ex-confirm-msg", "data-testid": "copy-confirm", role: "alert" }, parts.join(" · ") + ". A pending flag may be one the attorney needs to see. Copy the letter anyway?"),
      el("div", { class: "row" }, el("button", { type: "button", class: "btn primary", "data-testid": "btn-copy-anyway", onclick: () => { box.hidden = true; then(); } }, "Copy anyway"),
        el("button", { type: "button", class: "btn", "data-testid": "btn-copy-cancel", onclick: () => { box.hidden = true; } }, "Go back")));
    const b = ZL.$('[data-testid="btn-copy-anyway"]'); if (b) b.focus();
  }
  function render() {
    const root = ZL.$("#export-body"); clear(root);
    ZL.$("#view-export").hidden = !open;
    if (!open || !data) return;
    const c = data.counts;
    root.append(...[
      el("p", { class: "count-line", "data-testid": "count-line", role: "status" }, countLine(c)),
      (data.warnings || []).length ? el("ul", { class: "ex-warn" }, data.warnings.map((w) => el("li", {}, typeof w === "string" ? w : (w.message || w.code)))) : null,
      el("p", { id: "export-status", class: "muted small", role: "status" }),
      el("div", { id: "export-confirm", hidden: true }),
      el("section", { class: "ex-block", "aria-labelledby": "ex-h1" },
        el("div", { class: "toolbar" }, el("h3", { id: "ex-h1" }, "Treatment section (paste into the letter)"),
          el("button", { type: "button", class: "btn primary", "data-testid": "btn-copy-letter", onclick: () => { const go = () => copy(data.letter_text, "treatment section"); c.pending > 0 ? askConfirm(c, go) : go(); } }, "Copy letter")),
        el("pre", { class: "ex-text", tabindex: "0", "data-testid": "export-letter" }, data.letter_text)),
      el("section", { class: "ex-block", "aria-labelledby": "ex-h2" },
        el("div", { class: "toolbar" }, el("h3", { id: "ex-h2" }, "Internal review notes — do not send"),
          el("button", { type: "button", class: "btn", "data-testid": "btn-copy-notes", onclick: () => copy(data.internal_notes_text, "internal notes") }, "Copy notes")),
        el("pre", { class: "ex-text", tabindex: "0", "data-testid": "export-notes" }, data.internal_notes_text))].filter(Boolean));
  }
  async function load(scroll) {
    const s = ZL.state.get(); if (!s.token) return;
    try { data = await ZL.api.exportCase(s.token); open = true; render(); if (scroll) ZL.$("#view-export").scrollIntoView({ block: "start" }); }
    catch (e) { open = true; data = null; render(); ZL.$("#export-body").append(el("p", { class: "error", role: "alert" }, e.message)); }
  }
  ZL.openExport = () => load(true);
  ZL.closeExport = () => { open = false; render(); };
  // keep an open export in step with review decisions made after it was opened
  ZL.state.subscribe((s) => { if (!s.case) { open = false; data = null; render(); return; } if (open) { clearTimeout(timer); timer = setTimeout(() => load(false), 250); } });
})();
dict_keys(['token', 'name', 'status', 'demo_mode', 'backend', 'models', 'records', 'undated_entries', 'entries', 'amounts', 'totals', 'flags', 'tray', 'dates_to_confirm', 'injection', 'review', 'warnings', 'error', 'created_at', 'updated_at'])
{'id': 'a1', 'state': 'verified', 'reasons': [], 'why': 'Quote found word for word, every number in the summary is in the quote, and the second check agreed.', 'review_status': 'pending', 'edited': None, 'ladder': {'backend': 'fixture', 'code_checks': {'amount_in_text': True, 'classified_by': 'code:amounts'}, 'generator': None, 'human': {'action': None, 'edited_text': None, 'at': None}, 'item_id': 'a1', 'judge': {'call_id': 'cf12f7c8ef403', 'model': 'claude-haiku-5-5', 'prompt_version': 'judge_amount_class_v1', 'reason_code': 'NONE', 'verdict': 'agree'}, 'state': 'verified'}, 'record_ids': ['r2'], 'entry_id': 'e2', 'text': '$2,880', 'value_cents': 288000, 'kind': 'charge', 'excerpt': 'Dx: right shoulder contusion. X-ray negative. Sling provided. ED charge: $2,880.', 'excerpt_start': 404, 'excerpt_end': 410, 'duplicate_note': None}
dict_keys(['id', 'state', 'reasons', 'why', 'review_status', 'edited', 'ladder', 'type', 'category', 'source_kind', 'title', 'explanation', 'computed', 'evidence', 'origin', 'reviewer_note'])
dict_keys(['id', 'state', 'reasons', 'why', 'review_status', 'edited', 'ladder', 'seq', 'record_ids', 'date', 'date_status', 'provider', 'summary', 'ai_drafted', 'entered_by_reviewer', 'entered_by', 'source_kind', 'excerpt', 'excerpt_start', 'excerpt_end', 'duplicate_note'])
None
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:24:13.146Z

**tool call — Bash**
````
{
 "command": "grep -rn \"why-\\|entry-why\" tests/e2e/*.py | cut -c1-220; sed -n 60,100p app/frontend/timeline.js | cut -c1-220"
}
````

### User / tool · 2026-11-02T03:24:13.254Z

**tool result**
````
tests/e2e/conftest.py:6:  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-undo-batch, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
tests/e2e/test_timeline.py:33:    open_case(page, sample_case); page.get_by_test_id("entry-8").get_by_test_id("entry-why").click(); expect(page.get_by_test_id("why-text")).to_be_visible()
          const left = ZL.$('[data-testid="missing-entry"][data-record-id="' + d.record_id + '"]');
          if (left) { const rec = ZL.state.get().case.records.find((r) => r.id === d.record_id); if (ZL.rv && ZL.rv.say) ZL.rv.say(`Date confirmed: ${ZL.fmtDate(cand)}. Record ${rec ? rec.seq : ""} has no entry yet; it i
        } catch (er) { alert(er.message); }
      } }, ZL.fmtDate(cand))));
      return bar;
    };
    const shown = {};
    c.undated_entries.forEach((e) => {
      const d = c.dates_to_confirm.find((x) => x.record_id === e.record_ids[0]);
      const rec = c.records.find((r) => r.id === e.record_ids[0]);
      const row = entryRow(e, c); row.classList.add("undated");
      if (d) shown[d.record_id] = true;
      if (d && d.candidates.length) row.insertBefore(confirmBar(d), row.querySelector(".row-actions"));
      else if (rec) row.insertBefore(el("p", { class: "reason" }, "No readable date in this record header; it stays off the timeline."), row.querySelector(".row-actions"));
      box.append(row);
    });
    // A record with an ambiguous date but no entry at all (no model entry for it): still list it here so the date can be confirmed.
    // Once confirmed it is not removed: it moves to "Records without an entry" (manual.js) with a note and the by-hand path.
    // A record with no readable date and no entry has no date to confirm; it is listed once, under "Records without an entry".
    c.dates_to_confirm.filter((d) => !shown[d.record_id] && d.candidates.length).forEach((d) => {
      const rec = c.records.find((r) => r.id === d.record_id);
      const quote = rec ? recordExcerpt(rec) : "";
      const row = el("article", { class: "entry undated", "data-testid": "date-to-confirm-item", "data-record-id": d.record_id },
        el("div", { class: "entry-head" }, el("span", { class: "provider" }, rec ? `Record ${rec.seq}: ${rec.source_label}` : `Record ${d.record_id}`), el("span", { class: "chip" }, "Date to confirm")),
        quote ? el("blockquote", { class: "excerpt", "data-testid": "date-to-confirm-excerpt" }, quote) : null);
      row.append(confirmBar(d));
      row.append(el("p", { class: "muted small", "data-testid": "date-to-confirm-note" }, "No entry was drafted for this record. After you pick the date it is listed under Records without an entry, where you enter it by 
      if (rec) row.append(el("div", { class: "row-actions" }, el("button", { type: "button", class: "btn small", "data-testid": "btn-source", onclick: () => ZL.openSource([{ record_id: rec.id, start: null, end: null }], 
      box.append(row);
    });
    return box;
  }
  function tray(c) {
    const box = el("section", { class: "group tray", "data-testid": "rejected-tray" }, el("h2", {}, `Could not verify (${c.tray.length})`));
    if (!c.tray.length) { box.append(el("p", { class: "muted" }, "Nothing here. Every record produced an entry that passed the code checks.")); return box; }
    box.append(el("p", { class: "muted small" }, "These records did not produce a usable entry. They are not in the timeline and will not be in the letter. Open the record to read it yourself."));
    c.tray.forEach((t) => {
      const recs = t.record_ids.map((id) => c.records.find((r) => r.id === id)).filter(Boolean);
      const item = el("article", { class: "entry st-rejected", "data-testid": "tray-item", "data-item-id": t.id },
        el("div", { class: "entry-head" }, el("span", { class: "provider" }, recs.map((r) => `Record ${r.seq}: ${r.source_label}`).join("; ")), el("span", { class: "chip st-rejected" }, "Could not verify")),
        el("p", { class: "reason", "data-testid": "tray-reason" }, `${t.reasons.map(reasonText).join("; ")}`),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:25:20.638Z

**tool call — Write**
````
{
 "path": "/Users/arsis/zlayt-pm-project/app/frontend/stepper.js",
 "file_text": "/* Vertical steppers (T-081, D-042): every check and gate rendered as a rail of steps with pass / fail / skipped / pending, the plain-words why,\n   the evidence, and what the human must do next (HITL hand-off). Pattern: <outside project> flow rail (marker, label, detail, note, \"x/y done\", verdict).\n   Data comes from GET /cases/{token}/items/{id}/trace and GET /cases/{token}/trace (memory/contracts/api.md, \"Check traces\"); nothing is computed here\n   except \"x of y steps passed\" counts of what the server returned. Full-mode-only keys (response_raw, edited_text, events[].before/after) may be absent.\n   Exposes ZL.stepper = { item, itemSection, openTrace, mountCase, goto, label, verdictWord }. Server text only goes through ZL.el (text nodes). */\n(function () {\n  const ZL = (window.ZL = window.ZL || {});\n  const { el, clear } = ZL;\n  const S = (ZL.stepper = {});\n\n  // Status is a glyph AND a word, never colour alone.\n  const STATUS = { pass: [\"✓\", \"Passed\"], fail: [\"✕\", \"Failed\"], skipped: [\"–\", \"Skipped\"], pending: [\"○\", \"Not done yet\"] };\n  const VERDICT_WORD = { supported: \"Supported\", partially: \"Partly supported\", unsupported: \"Not supported\", disagrees: \"Disagrees\", unsure: \"Could not decide\", unavailable: \"Unavailable\" };\n  S.verdictWord = (v) => VERDICT_WORD[v] || v || \"\";\n  const kindOf = (st) => {\n    if (st.kind === \"human\") return \"You\";\n    if (st.kind === \"code\") return \"Code\";\n    const m = st.evidence && st.evidence.model;\n    return (m && m.role === \"generator\") || st.id === \"extracted\" || st.id === \"extract\" ? \"AI draft\" : \"AI check\";\n  };\n  const humanize = (k) => String(k).replace(/_/g, \" \");\n  const rv = () => ZL.rv;\n  const caseNow = () => ZL.state.get().case;\n  const recSeq = (id) => { const r = ((caseNow() || {}).records || []).find((x) => x.id === id); return r ? r.seq : String(id).replace(/^r/, \"\"); };\n\n  // ---- labels for items (entry: date and provider; amount: the figure; flag: its title)\n  S.label = function (id) {\n    const c = caseNow(), f = c && rv() && rv().find(c, id);\n    if (!f) return id;\n    const it = f.item;\n    if (f.kind === \"entry\") return (it.date || \"undated\") + \" · \" + (it.provider || \"entry\");\n    if (f.kind === \"amount\") return (it.text || it.id) + (it.kind ? \" (\" + it.kind + \")\" : \"\");\n    return it.title || it.id;\n  };\n\n  // ---- navigation helpers\n  function closeDialogs() { document.querySelectorAll(\"dialog[open]\").forEach((d) => { try { d.close(); } catch (_) { /* ignore */ } }); }\n  function flash(node) {\n    node.classList.add(\"zs-flash\");\n    setTimeout(() => node.classList.remove(\"zs-flash\"), 2200);\n  }\n  function reveal(node) {\n    if (!node.hasAttribute(\"tabindex\")) node.setAttribute(\"tabindex\", \"-1\");\n    node.scrollIntoView({ block: \"center\" }); node.focus({ preventScroll: true }); flash(node);\n  }\n  S.goto = function (itemId) {\n    closeDialogs();\n    const node = document.querySelector('[data-testid=\"queue\"] [data-item-id=\"' + itemId + '\"]') || document.querySelector('[data-item-id=\"' + itemId + '\"]');\n    if (!node) return false;\n    reveal(node); return true;\n  };\n  function gotoDates(recordId) {\n    closeDialogs();\n    const node = (recordId && document.querySelector('[data-testid=\"date-to-confirm-item\"][data-record-id=\"' + recordId + '\"]')) ||\n      (recordId && document.querySelector('[data-record-id=\"' + recordId + '\"]')) || document.querySelector('[data-testid=\"dates-to-confirm\"]');\n    if (node) reveal(node);\n  }\n  function gotoPanel(name) {\n    closeDialogs();\n    const node = document.querySelector('[data-panel=\"' + name + '\"]');\n    if (node) reveal(node);\n  }\n  S.gotoPanel = gotoPanel;\n  function openRecord(itemId, recordId) {\n    const c = caseNow(), f = itemId && c && rv() && rv().find(c, itemId);\n    if (f) { rv().openSource(f.item, f.kind); return; }\n    if (recordId && typeof ZL.openSource === \"function\") ZL.openSource([{ record_id: recordId, start: null, end: null }], \"Record \" + recSeq(recordId));\n  }\n\n  // ---- \"What you need to do\": one fixed sentence from the server plus a button where something on the page can do it\n  function actionNode(na, ctx) {\n    if (!na) return null;\n    const t = na.target || {}, buttons = [];\n    const itemId = t.item_id || ctx.itemId, recId = t.record_id || (ctx.recordId || null);\n    const btn = (text, fn, extra) => buttons.push(el(\"button\", Object.assign({ type: \"button\", class: \"zs-btn\", \"data-testid\": \"btn-step-action\", \"data-action-code\": na.code, onclick: fn }, extra || {}), text));\n    switch (na.code) {\n      case \"DECIDE\": if (itemId) btn(\"Go to the decision buttons\", () => S.goto(itemId)); break;\n      case \"CONFIRM_DATE\": btn(\"Go to Dates to confirm\", () => gotoDates(recId)); break;\n      case \"EDIT_SUMMARY\": if (itemId) btn(\"Go to the item and edit the summary\", () => { if (S.goto(itemId)) { const n = document.querySelector('[data-testid=\"queue\"] [data-item-id=\"' + itemId + '\"]') || document.querySelector('[data-item-id=\"' + itemId + '\"]'); if (n) n.dispatchEvent(new KeyboardEvent(\"keydown\", { key: \"e\", bubbles: true })); } }); break;\n      case \"EDIT_QUOTE\": case \"READ_RECORD\": case \"COMPARE_BY_HAND\": btn(\"Open the record\", () => openRecord(itemId, recId)); break;\n      case \"DISMISS_OR_ENTER_BY_HAND\": if (itemId) btn(\"Go to the item\", () => S.goto(itemId)); break;\n      default:\n        if (t.view === \"dates_to_confirm\") btn(\"Go to Dates to confirm\", () => gotoDates(recId));\n        else if (t.item_id) btn(\"Go to the item\", () => S.goto(t.item_id));\n    }\n    return el(\"div\", { class: \"zs-todo\", \"data-testid\": \"step-action\" },\n      el(\"p\", { class: \"zs-todo-text\" }, el(\"strong\", {}, \"What you need to do: \"), na.text || \"\"), buttons.length ? el(\"div\", { class: \"zs-todo-btns\" }, buttons) : null);\n  }\n\n  // ---- evidence\n  function quote(rec, text) {\n    return el(\"figure\", { class: \"zs-quote\" }, rec ? el(\"figcaption\", {}, \"Record \" + recSeq(rec)) : null, el(\"blockquote\", {}, text));\n  }\n  const fmtVal = (k, v) => (/_cents$/.test(k) && typeof v === \"number\" && rv() ? [humanize(k.replace(/_cents$/, \"\")), rv().money(v)] : [humanize(k), v && typeof v === \"object\" ? JSON.stringify(v) : String(v)]);\n  function evidenceNode(st) {\n    const ev = st.evidence || {}, out = [];\n    if (ev.excerpt && ev.excerpt.text) out.push(quote(ev.excerpt.record_id, ev.excerpt.text));\n    (ev.spans || []).forEach((sp) => { if (sp && sp.text) out.push(quote(sp.record_id, sp.text)); });\n    if (ev.tokens && ev.tokens.length) out.push(el(\"p\", { class: \"zs-ev\" }, el(\"strong\", {}, \"Not found in the quote: \"), ev.tokens.map((t) => el(\"code\", { class: \"zs-tok\" }, t))));\n    if (ev.values) {\n      const bits = Object.entries(ev.values).filter(([, v]) => v != null && v !== \"\").map(([k, v]) => fmtVal(k, v));\n      if (bits.length) out.push(el(\"p\", { class: \"zs-ev\", \"data-testid\": \"step-values\" }, bits.map(([k, v]) => el(\"span\", { class: \"zs-kv\" }, el(\"span\", { class: \"zs-k\" }, k + \" \"), v))));\n    }\n    if (ev.date) out.push(el(\"p\", { class: \"zs-ev\" }, el(\"strong\", {}, \"Date: \"), (ev.date.date_raw ? \"written “\" + ev.date.date_raw + \"”\" : \"no date written\"),\n      ev.date.date_iso ? \", read as \" + ev.date.date_iso : \"\", ev.date.date_status ? \" (\" + humanize(ev.date.date_status) + \")\" : \"\", (ev.date.candidates || []).length ? \"; possible readings: \" + ev.date.candidates.join(\" or \") : \"\"));\n    if (ev.judge_verdict) {\n      out.push(el(\"p\", { class: \"zs-ev zs-judge\", \"data-testid\": \"step-judge-reason\" }, el(\"strong\", {}, \"The second AI check said: \"), S.verdictWord(ev.judge_verdict),\n        ev.rationale ? \". \" + ev.rationale : \"\", ev.judge_reason_code && ev.judge_reason_code !== \"NONE\" ? [\" \", el(\"code\", { class: \"zs-code\" }, ev.judge_reason_code)] : null));\n    } else if (ev.rationale) out.push(el(\"p\", { class: \"zs-ev\" }, ev.rationale));\n    if (ev.events && ev.events.length) out.push(el(\"p\", { class: \"zs-ev\" }, el(\"strong\", {}, \"Your decisions: \"), ev.events.map((e) => (e.action || \"\") + (e.at ? \" at \" + e.at : \"\")).join(\"; \")));\n    else if (ev.action) out.push(el(\"p\", { class: \"zs-ev\" }, el(\"strong\", {}, \"Your decision: \"), ev.action + (ev.at ? \" at \" + ev.at : \"\")));\n    if (ev.edited_text) out.push(el(\"p\", { class: \"zs-ev\" }, el(\"strong\", {}, \"Your wording: \"), ev.edited_text));\n    // technical detail for the audit-minded reader, collapsed\n    const m = ev.model, tech = [];\n    const kv = (k, v) => (v == null || v === \"\" ? null : el(\"span\", { class: \"zs-kv\" }, el(\"span\", { class: \"zs-k\" }, k + \" \"), String(v)));\n    if (m) tech.push(kv(\"model\", m.id), kv(\"role\", m.role), kv(\"independent of the drafting model\", m.independent_of_generator == null ? null : m.independent_of_generator ? \"yes\" : \"no\"));\n    tech.push(kv(\"prompt\", ev.prompt_version), kv(\"prompt hash\", ev.prompt_sha256 && String(ev.prompt_sha256).slice(0, 12)), kv(\"call\", ev.call_id), kv(\"backend\", ev.backend),\n      kv(\"recorded from\", ev.recorded_from && ev.recorded_from.backend), kv(\"latency\", ev.latency_ms != null ? ev.latency_ms + \" ms\" : null), kv(\"parsed\", ev.parsed_ok == null ? null : ev.parsed_ok ? \"yes\" : \"no\"));\n    const techNodes = tech.filter(Boolean);\n    if (techNodes.length || ev.response_raw)\n      out.push(el(\"details\", { class: \"zs-more\", \"data-testid\": \"step-tech\" }, el(\"summary\", {}, \"Technical details\"), techNodes.length ? el(\"p\", { class: \"zs-ev\" }, techNodes) : null,\n        ev.response_raw ? el(\"pre\", { class: \"zs-pre\" }, typeof ev.response_raw === \"string\" ? ev.response_raw : JSON.stringify(ev.response_raw, null, 2)) : null));\n    return out;\n  }\n\n  function fmtCounts(counts) {\n    const out = [];\n    Object.entries(counts || {}).forEach(([k, v]) => {\n      if (v && typeof v === \"object\") {\n        const inner = Object.entries(v).map(([a, b]) => humanize(a) + \" \" + b).join(\", \");\n        if (inner) out.push(humanize(k) + \": \" + inner);\n      } else if (/_cents$/.test(k) && typeof v === \"number\" && rv()) out.push(humanize(k.replace(/_cents$/, \"\")) + \" \" + rv().money(v));\n      else if (v != null && v !== \"\") out.push(humanize(k) + \" \" + v);\n    });\n    return out;\n  }\n\n  // ---- one step\n  function stepNode(st, active, ctx) {\n    const [glyph, word] = STATUS[st.status] || [\"?\", st.status];\n    const li = el(\"li\", { class: \"zs-step\", \"data-testid\": ctx.testid || \"step\", \"data-step-id\": st.id, \"data-status\": st.status, \"data-kind\": st.kind, \"aria-current\": active ? \"step\" : null },\n      el(\"span\", { class: \"zs-marker\", \"aria-hidden\": \"true\", \"data-testid\": \"step-marker\" }, glyph),\n      el(\"div\", { class: \"zs-body\" },\n        el(\"div\", { class: \"zs-head\" },\n          el(\"span\", { class: \"zs-label\" }, st.label), el(\"span\", { class: \"zs-kind zs-kind-\" + st.kind, \"data-testid\": \"step-kind\" }, kindOf(st)),\n          el(\"span\", { class: \"zs-status\", \"data-testid\": \"step-status\" }, word), st.blocks_export ? el(\"span\", { class: \"zs-blocks\" }, \"Blocks export\") : null),\n        st.why ? el(\"p\", { class: \"zs-why\", \"data-testid\": \"step-why\" }, st.why) : null,\n        st.reason_code ? el(\"p\", { class: \"zs-ev zs-codes\" }, el(\"code\", { class: \"zs-code\" }, st.reason_code), st.rule ? el(\"span\", { class: \"zs-rule\" }, \" rule \" + st.rule) : null) : null));\n    const body = li.lastChild;\n    const ev = evidenceNode(st); if (ev.length) body.append(el(\"div\", { class: \"zs-evidence\", \"data-testid\": \"step-evidence\" }, ev));\n    if (ctx.extra) { const x = ctx.extra(st); if (x) body.append(x); }\n    if (st.status === \"fail\" || st.status === \"pending\") { const a = actionNode(st.next_action, ctx); if (a) body.append(a); }\n    return li;\n  }\n  // The active step is the one the human has to deal with now: the first fail or pending step that carries a next action.\n  function activeIndex(steps) {\n    let i = steps.findIndex((s) => (s.status === \"fail\" || s.status === \"pending\") && s.next_action);\n    if (i < 0) i = steps.findIndex((s) => s.status === \"fail\" || s.status === \"pending\");\n    return i;\n  }\n\n  // ---- item level\n  S.item = function (tr) {\n    const steps = tr.steps || [], act = activeIndex(steps), v = tr.verdict || {}, p = tr.progress || {};\n    const ctx = { itemId: tr.item_id };\n    // a record id for date steps\n    const dstep = steps.find((s) => s.evidence && s.evidence.date); if (dstep) ctx.recordId = dstep.evidence.date.record_id;\n    const root = el(\"div\", { class: \"zs zs-item\", \"data-testid\": \"item-stepper\", \"data-verdict\": v.code || \"\" },\n      el(\"div\", { class: \"zs-top\" },\n        el(\"span\", { class: \"zs-verdict zs-v-\" + (v.code || \"none\"), \"data-testid\": \"item-verdict\" }, v.label || \"\"),\n        el(\"span\", { class: \"zs-progress\", \"data-testid\": \"item-progress\" }, p.label || \"\")),\n      (tr.state_reasons || []).length ? el(\"ul\", { class: \"zs-reasons\" }, tr.state_reasons.map((r) => el(\"li\", {}, r.why))) : null,\n      el(\"ol\", { class: \"zs-rail\", \"aria-label\": \"Checks for \" + S.label(tr.item_id) }, steps.map((s, i) => stepNode(s, i === act, ctx))));\n    return root;\n  };\n  // A section that fetches its own trace; used inside the Why dialog.\n  S.itemSection = function (token, id) {\n    const box = el(\"section\", { class: \"zs-section\", \"aria-labelledby\": \"zs-h-\" + id }, el(\"h3\", { id: \"zs-h-\" + id }, \"Step by step: how this was checked\"));\n    const msg = el(\"p\", { class: \"muted\", role: \"status\" }, \"Loading the checks…\"); box.append(msg);\n    ZL.api.trace(token, id).then((tr) => { msg.remove(); box.append(S.item(tr)); },\n      (e) => { msg.textContent = ZL.API_MODE === \"mock\" ? \"Step-by-step checks need the live server.\" : \"The checks could not be loaded: \" + e.message; });\n    return box;\n  };\n  S.openTrace = async function (id) {\n    const s = ZL.state.get(), dlg = ZL.$(\"#why-modal\"), body = ZL.$(\"#why-body\"); clear(body);\n    ZL.$(\"#why-title\").textContent = \"How this was checked: \" + S.label(id);\n    body.append(S.itemSection(s.token, id));\n    if (!dlg.open) dlg.showModal();\n  };\n  // Small button for cards that have no Why? button of their own (flags, charges, could-not-verify items).\n  S.traceButton = (id, cls) => el(\"button\", { type: \"button\", class: cls || \"rv-btn rv-secondary\", \"data-testid\": \"btn-trace\", \"data-trace-for\": id, onclick: () => S.openTrace(id) }, \"How it was checked\");\n\n  // ---- case level\n  let cache = null, openPref = null, seq = 0;\n  const wide = () => window.matchMedia && window.matchMedia(\"(min-width: 900px)\").matches;\n\n  function gateNode(st) {\n    const bl = st.blockers || [];\n    if (!bl.length) return null;\n    const li = (b) => el(\"li\", { class: \"zs-blocker\", \"data-testid\": \"gate-blocker\", \"data-blocker-code\": b.reason_code, \"data-jump-item\": b.item_id || null },\n      el(\"span\", { class: \"zs-blocker-name\" }, b.item_id ? S.label(b.item_id) : \"Whole case\"), \" \",\n      el(\"span\", { class: \"zs-ev\" }, b.why || \"\"),\n      b.item_id ? el(\"button\", { type: \"button\", class: \"zs-btn\", \"data-testid\": \"btn-gate-jump\", onclick: () => S.goto(b.item_id) }, \"Go to item\") : null);\n    const first = bl.slice(0, 6), rest = bl.slice(6);\n    return el(\"div\", { class: \"zs-gate\", \"data-testid\": \"gate-blockers\" },\n      el(\"p\", { class: \"zs-ev\" }, el(\"strong\", {}, \"Blocking the export (\" + bl.length + \"):\")),\n      el(\"ul\", { class: \"zs-blockers\" }, first.map(li)),\n      rest.length ? el(\"details\", { class: \"zs-more\" }, el(\"summary\", {}, \"Show the other \" + rest.length), el(\"ul\", { class: \"zs-blockers\" }, rest.map(li))) : null);\n  }\n  function caseExtra(st) {\n    if (st.id === \"export_gate\") return gateNode(st);\n    if (st.id === \"judges\") return el(\"div\", { class: \"zs-todo-btns\" }, el(\"button\", { type: \"button\", class: \"zs-btn\", \"data-testid\": \"btn-to-judges\", onclick: () => gotoPanel(\"judges\") }, \"See how the AI was checked\"));\n    return null;\n  }\n  function caseCounts(st) {\n    const bits = fmtCounts(st.counts);\n    return bits.length ? el(\"p\", { class: \"zs-counts\", \"data-testid\": \"step-counts\" }, bits.map((b) => el(\"span\", { class: \"zs-chip\" }, b))) : null;\n  }\n  function caseRail(tr) {\n    const steps = tr.steps || [], passed = steps.filter((s) => s.status === \"pass\").length, act = activeIndex(steps), v = tr.verdict || {};\n    const ctx = { testid: \"case-step\", extra: (st) => { const a = caseCounts(st), b = caseExtra(st); return a || b ? el(\"div\", {}, a, b) : null; } };\n    return el(\"div\", { class: \"zs zs-case-inner\" },\n      el(\"p\", { class: \"zs-top\" }, el(\"span\", { class: \"zs-verdict zs-v-\" + (v.code || \"none\"), \"data-testid\": \"case-verdict\" }, v.label || \"\"), \" \",\n        el(\"span\", { class: \"zs-progress\", \"data-testid\": \"case-progress\" }, passed + \"/\" + steps.length + \" passed\")),\n      el(\"ol\", { class: \"zs-rail\", \"aria-label\": \"Case checks, from reading the paste to the export gate\" }, steps.map((s, i) => stepNode(s, i === act, ctx))),\n      el(\"p\", { class: \"zs-legend\" }, \"✓ passed · ✕ failed · – skipped · ○ not done yet. “Code” steps are done by a program, “AI” steps by a model, “You” steps are your decisions.\"));\n  }\n  function paintCase(host, tr) {\n    clear(host);\n    const steps = tr ? tr.steps || [] : [], passed = steps.filter((s) => s.status === \"pass\").length;\n    const det = el(\"details\", { class: \"zs-case-det\" },\n      el(\"summary\", {}, el(\"span\", { class: \"zs-case-title\" }, \"Case checks\"), \" \",\n        el(\"span\", { class: \"zs-progress\", \"data-testid\": \"case-summary-progress\" }, tr ? passed + \"/\" + steps.length + \" passed\" : \"loading…\"), \" \",\n        el(\"span\", { class: \"zs-sumv\" }, tr && tr.verdict ? tr.verdict.label : \"\")),\n      tr ? caseRail(tr) : el(\"p\", { class: \"muted\", role: \"status\" }, \"Loading the case checks…\"));\n    det.open = openPref == null ? wide() : openPref;\n    det.addEventListener(\"toggle\", () => { openPref = det.open; });\n    host.append(det);\n  }\n  S.mountCase = function (parent, before) {\n    const s = ZL.state.get(); if (!s.token || !s.case) return;\n    const host = el(\"section\", { class: \"zs-case\", \"data-testid\": \"case-stepper\", \"aria-label\": \"Case checks\" });\n    parent.insertBefore(host, before || null);\n    const mine = ++seq;\n    paintCase(host, cache && cache.token === s.token ? cache.data : null);\n    ZL.api.caseTrace(s.token).then((tr) => {\n      const same = cache && cache.token === s.token && JSON.stringify(cache.data) === JSON.stringify(tr);\n      cache = { token: s.token, data: tr };\n      if (!same && host.isConnected && mine === seq) paintCase(host, tr);\n    }, () => { if (host.isConnected && !cache) host.hidden = true; });\n  };\n})();\n"
}
````

### User / tool · 2026-11-02T03:25:20.700Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/app/frontend/stepper.js (file state is current in your context — no need to Read it back)

Note: Write's parameters are named `file_path` and `content`. `path` was read as `file_path`. `file_text` was read as `content`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:25:41.098Z

**tool call — Write**
````
{
 "path": "/Users/arsis/zlayt-pm-project/app/frontend/judges.js",
 "file_text": "/* \"How the AI was checked\" panel (T-082, D-042). Reads GET /cases/{token}/judges: items the second AI check judged, supported / unsupported / unavailable\n   counts, each objection with its fixed-sentence reason, model and prompt version, and where the code checks and the AI disagree. Every row links to the\n   item's stepper. This is a report on the AI's drafts, never a verdict on the case: the heading and a note say so. Counts are the server's; nothing is added here.\n   Rows deliberately carry data-target-item (not data-item-id) so the review keyboard flow and the panels' j/k walk do not treat them as review items. */\n(function () {\n  const ZL = window.ZL, RV = ZL.rv, { el, clear } = ZL;\n  let cache = null;\n\n  const DIS = {\n    judge_objects: \"Code checks passed, the AI objected\",\n    judge_agrees_code_flags: \"Code raised a doubt, the AI found it supported\",\n    sources_disagree: \"The phrase list and the AI disagree\",\n  };\n  const RS = { pending: \"Not reviewed\", accepted: \"Accepted\", edited: \"Edited\", dismissed: \"Dismissed\" };\n  const KIND = { entry: \"Entry\", amount: \"Amount\", flag: \"Flag\" };\n\n  function links(id, kind) {\n    return el(\"div\", { class: \"zs-todo-btns\" },\n      el(\"button\", { type: \"button\", class: \"zs-btn\", \"data-testid\": \"btn-judge-steps\", onclick: () => ZL.stepper.openTrace(id) }, \"See the steps\"),\n      el(\"button\", { type: \"button\", class: \"zs-btn\", \"data-testid\": \"btn-judge-goto\", onclick: () => ZL.stepper.goto(id) }, \"Go to item\"));\n  }\n  const head = (id, kind) => el(\"div\", { class: \"zs-head\" }, el(\"span\", { class: \"zs-label\" }, ZL.stepper.label(id)), el(\"span\", { class: \"zs-kind\" }, KIND[kind] || kind));\n\n  function rejection(r) {\n    return el(\"li\", { class: \"zj-row\", \"data-testid\": \"judge-rejection\", \"data-target-item\": r.item_id },\n      head(r.item_id, r.kind),\n      el(\"p\", { class: \"zs-why\" }, el(\"strong\", {}, ZL.stepper.verdictWord(r.verdict) + \". \"), r.rationale || \"\"),\n      el(\"p\", { class: \"zs-ev\" }, r.reason_code ? [el(\"code\", { class: \"zs-code\" }, r.reason_code), \" \"] : null,\n        el(\"span\", { class: \"zs-k\" }, \"model \"), r.model || \"\", el(\"span\", { class: \"zs-k\" }, \" · prompt \"), r.prompt_version || \"\",\n        el(\"span\", { class: \"zs-k\" }, \" · your decision \"), RS[r.review_status] || r.review_status || \"\"),\n      r.response_raw ? el(\"details\", { class: \"zs-more\" }, el(\"summary\", {}, \"Raw answer from the check\"), el(\"pre\", { class: \"zs-pre\" }, r.response_raw)) : null,\n      links(r.item_id, r.kind));\n  }\n  function unresolved(r) {\n    return el(\"li\", { class: \"zj-row\", \"data-testid\": \"judge-unresolved\", \"data-target-item\": r.item_id },\n      head(r.item_id, r.kind),\n      el(\"p\", { class: \"zs-why\" }, el(\"strong\", {}, ZL.stepper.verdictWord(r.verdict) + \". \"),\n        r.verdict === \"unavailable\" ? \"The second check did not answer, so this item was not checked by an AI judge. Read it yourself.\" : \"The second check could not decide. Read it yourself.\"),\n      el(\"p\", { class: \"zs-ev\" }, el(\"span\", { class: \"zs-k\" }, \"model \"), r.model || \"\", el(\"span\", { class: \"zs-k\" }, \" · prompt \"), r.prompt_version || \"\"),\n      links(r.item_id, r.kind));\n  }\n  function disagreement(d) {\n    return el(\"li\", { class: \"zj-row\", \"data-testid\": \"judge-disagreement\", \"data-target-item\": d.item_id },\n      head(d.item_id, d.kind),\n      el(\"p\", { class: \"zs-why\" }, el(\"strong\", {}, DIS[d.type] || d.type)),\n      el(\"p\", { class: \"zs-ev\" }, el(\"span\", { class: \"zs-k\" }, \"Code said: \"), d.code_says || \"\", el(\"br\"), el(\"span\", { class: \"zs-k\" }, \"The AI said: \"), d.judge_says || \"\"),\n      el(\"p\", { class: \"zs-ev\" }, \"Result: \" + (d.resolution === \"needs_review\" ? \"kept as needs review\" : d.resolution || \"\") + (d.review_status ? \". Your decision: \" + (RS[d.review_status] || d.review_status) : \"\")),\n      links(d.item_id, d.kind));\n  }\n  const list = (testid, label, rows, mk, empty) => el(\"section\", { class: \"zj-group\", \"data-testid\": testid, \"aria-label\": label },\n    el(\"h3\", {}, label + \" (\" + rows.length + \")\"), rows.length ? el(\"ul\", { class: \"zj-list\" }, rows.map(mk)) : el(\"p\", { class: \"rv-empty\" }, empty));\n\n  function tile(n, label) { return el(\"li\", { class: \"zj-tile\" }, el(\"strong\", { class: \"zj-n\" }, String(n)), el(\"span\", { class: \"zj-l\" }, label)); }\n\n  function paint(root, d) {\n    clear(root);\n    root.setAttribute(\"data-testid\", \"judge-panel\"); root.setAttribute(\"aria-labelledby\", \"zj-h\");\n    root.append(el(\"h2\", { id: \"zj-h\" }, \"How the AI was checked\"),\n      el(\"p\", { class: \"rv-help\", \"data-testid\": \"judge-label\" }, el(\"strong\", {}, \"AI quality checks. \"),\n        \"This shows how a second AI model checked the first AI's drafts. It is not a verdict on the case, the care or the claim, and it does not replace your review.\"));\n    if (!d) { root.append(el(\"p\", { class: \"muted\", role: \"status\" }, \"Loading the AI checks…\")); return; }\n    const t = d.totals || {}, m = d.models || {};\n    root.append(el(\"p\", { class: \"zj-models\", \"data-testid\": \"judge-model-line\" },\n      \"Drafted by \", el(\"strong\", {}, m.generator || \"unknown\"), \", checked by \", el(\"strong\", {}, m.judge || \"unknown\"),\n      d.independent_models ? \" (a different model, so it does not grade its own work).\" : \" (the same model: this check is weaker, read more closely).\"),\n      el(\"p\", { class: \"zs-ev\", \"data-testid\": \"judge-prompts\" }, el(\"span\", { class: \"zs-k\" }, \"Prompt versions: \"), (d.prompt_versions || []).join(\", \") || \"none\"));\n    root.append(el(\"ul\", { class: \"zj-tiles\", \"data-testid\": \"judge-totals\", \"aria-label\": \"AI check totals\" },\n      tile(t.items_judged || 0, \"items checked by AI\"), tile(t.supported || 0, \"supported\"), tile(t.unsupported || 0, \"AI objected\"),\n      tile(t.unsure || 0, \"could not decide\"), tile(t.unavailable || 0, \"unavailable\"), tile(t.human_overrides || 0, \"you accepted despite an objection\")));\n    (d.judges || []).filter((j) => j.label).forEach(() => {});\n    const jr = (d.judges || []).filter((j) => j.label && j.items + (j.unavailable || 0) > 0);\n    if (jr.length) root.append(el(\"details\", { class: \"zs-more zj-by\", \"data-testid\": \"judge-by-check\" }, el(\"summary\", {}, \"By kind of check (\" + jr.length + \")\"),\n      el(\"ul\", { class: \"zj-list\" }, jr.map((j) => el(\"li\", { class: \"zj-row\" }, el(\"div\", { class: \"zs-head\" }, el(\"span\", { class: \"zs-label\" }, j.label)),\n        el(\"p\", { class: \"zs-ev\" }, j.items + \" checked: \" + j.supported + \" supported, \" + (j.partially || 0) + \" partly, \" + (j.unsupported || 0) + \" not supported, \" + (j.disagrees || 0) + \" disagree, \" + (j.unsure || 0) + \" undecided, \" + (j.unavailable || 0) + \" unavailable. \",\n          el(\"span\", { class: \"zs-k\" }, \"Prompt \"), j.prompt_version || \"\", el(\"span\", { class: \"zs-k\" }, \" · model \"), (j.models || []).join(\", \"))))))));\n    root.append(list(\"judge-rejections\", \"Where the AI objected\", d.rejections || [], rejection, \"No objections. The second check supported every item it checked.\"),\n      list(\"judge-unresolved-list\", \"Where the AI could not decide\", d.unresolved || [], unresolved, \"Nothing left undecided or unavailable.\"),\n      list(\"judge-disagreements\", \"Where code and the AI disagree\", d.disagreements || [], disagreement, \"No disagreements between the code checks and the AI.\"));\n  }\n\n  RV.registerPanel(\"judges\", (root, c) => {\n    paint(root, cache && cache.token === c.token ? cache.data : null);\n    ZL.api.judges(c.token).then((d) => {\n      const same = cache && cache.token === c.token && JSON.stringify(cache.data) === JSON.stringify(d);\n      cache = { token: c.token, data: d };\n      if (!same && root.isConnected) paint(root, d);\n    }, () => { if (!cache) root.hidden = true; });\n  });\n})();\n"
}
````

### User / tool · 2026-11-02T03:25:41.168Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/app/frontend/judges.js (file state is current in your context — no need to Read it back)

Note: Write's parameters are named `file_path` and `content`. `path` was read as `file_path`. `file_text` was read as `content`.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:06.113Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\np='judges.js'; s=open(p).read()\ns=s.replace(\"    (d.judges || []).filter((j) => j.label).forEach(() => {});\\n\",\"\")\ns=s.replace(\"    clear(root);\\n    root.setAttribute(\\\"data-testid\\\", \\\"judge-panel\\\")\",\"    clear(root); root.hidden = false;\\n    root.setAttribute(\\\"data-testid\\\", \\\"judge-panel\\\")\")\nopen(p,'w').write(s)\nEOF\ncat > stepper.css <<'EOF'\n/* Vertical steppers and the \"How the AI was checked\" panel (T-081, T-082). Token-based: every colour is a --zs-* variable that falls back to the\n   app tokens in styles.css (so dark mode follows), ready for the T-060 polish pass to restyle in one place. */\n:root {\n  --zs-ok: var(--ok, #1d7a46); --zs-bad: var(--bad, #b42318); --zs-warn: var(--warn, #8a5300); --zs-accent: var(--accent, #2f5bd3);\n  --zs-ink: var(--ink, #16181d); --zs-muted: var(--muted, #555d6b); --zs-line: var(--line, #d5dae2); --zs-surface: var(--panel, #fff);\n  --zs-soft: var(--chip, #eef1f6); --zs-warn-bg: var(--warnbg, #fff4e0); --zs-ai-bg: var(--aibg, #eaf1ff);\n  --zs-radius: 10px; --zs-rail: 2px; --zs-marker: 22px;\n}\n.zs { color: var(--zs-ink); min-width: 0; overflow-wrap: anywhere; }\n.zs-case { margin: 0 0 14px; }\n.zs-case-det { border: 1px solid var(--zs-line); border-radius: var(--zs-radius); background: var(--zs-surface); padding: 6px 12px; }\n.zs-case-det > summary { cursor: pointer; min-height: 44px; display: flex; flex-wrap: wrap; align-items: center; gap: 4px 10px; font-weight: 600; }\n.zs-case-det > summary:focus-visible, .zs-more > summary:focus-visible { outline: 3px solid var(--zs-accent); outline-offset: 2px; }\n.zs-case-title { font-size: 1rem; }\n.zs-sumv { color: var(--zs-muted); font-weight: 500; font-size: .9rem; }\n.zs-top { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; margin: 6px 0 10px; }\n.zs-progress { font-size: .85rem; color: var(--zs-muted); font-variant-numeric: tabular-nums; font-weight: 600; }\n.zs-verdict { font-weight: 700; border: 1px solid var(--zs-line); background: var(--zs-soft); border-radius: 999px; padding: 1px 10px; font-size: .9rem; }\n.zs-v-accepted, .zs-v-ready { color: var(--zs-ok); }\n.zs-v-needs_attention, .zs-v-rejected, .zs-v-failed { color: var(--zs-bad); }\n.zs-v-ready_for_decision, .zs-v-waiting_for_run, .zs-v-running { color: var(--zs-warn); }\n.zs-reasons { margin: 0 0 8px; padding-left: 20px; color: var(--zs-warn); font-size: .9rem; }\n\n/* the rail: a vertical line, a marker per step, the body to the right */\n.zs-rail { list-style: none; margin: 0; padding: 0; }\n.zs-step { position: relative; display: block; margin: 0; padding: 4px 0 14px calc(var(--zs-marker) + 12px); }\n.zs-step::before { content: \"\"; position: absolute; left: calc(var(--zs-marker) / 2 - var(--zs-rail) / 2); top: calc(var(--zs-marker) + 6px); bottom: -2px; width: var(--zs-rail); background: var(--zs-line); }\n.zs-step:last-child::before { display: none; }\n.zs-marker { position: absolute; left: 0; top: 4px; width: var(--zs-marker); height: var(--zs-marker); border-radius: 50%; display: flex; align-items: center; justify-content: center;\n  font-size: 13px; font-weight: 800; line-height: 1; background: var(--zs-surface); border: 2px solid var(--zs-line); color: var(--zs-muted); }\n.zs-step[data-status=\"pass\"] .zs-marker { border-color: var(--zs-ok); color: var(--zs-ok); }\n.zs-step[data-status=\"fail\"] .zs-marker { border-color: var(--zs-bad); background: var(--zs-bad); color: var(--zs-surface); }\n.zs-step[data-status=\"skipped\"] .zs-marker { border-style: dashed; }\n.zs-step[data-status=\"pending\"] .zs-marker { border-color: var(--zs-accent); color: var(--zs-accent); }\n.zs-step[aria-current=\"step\"] > .zs-body { border-left: 4px solid var(--zs-accent); background: var(--zs-ai-bg); border-radius: 6px; padding: 6px 8px; margin: -2px 0 0 -4px; }\n.zs-body { min-width: 0; }\n.zs-head { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 8px; }\n.zs-label { font-weight: 700; }\n.zs-kind, .zs-chip { font-size: .72rem; font-weight: 700; letter-spacing: .02em; border: 1px solid var(--zs-line); background: var(--zs-soft); border-radius: 999px; padding: 0 8px; color: var(--zs-muted); }\n.zs-chip { font-weight: 600; letter-spacing: 0; display: inline-block; margin: 2px 4px 2px 0; }\n.zs-kind-llm { color: var(--zs-accent); border-color: var(--zs-accent); }\n.zs-kind-human { color: var(--zs-ink); }\n.zs-status { font-size: .8rem; font-weight: 700; }\n.zs-step[data-status=\"pass\"] .zs-status { color: var(--zs-ok); }\n.zs-step[data-status=\"fail\"] .zs-status { color: var(--zs-bad); }\n.zs-step[data-status=\"pending\"] .zs-status { color: var(--zs-accent); }\n.zs-step[data-status=\"skipped\"] .zs-status { color: var(--zs-muted); }\n.zs-blocks { font-size: .72rem; font-weight: 700; color: var(--zs-bad); border: 1px solid var(--zs-bad); border-radius: 999px; padding: 0 8px; }\n.zs-why { margin: 2px 0 4px; font-size: .92rem; }\n.zs-ev { margin: 3px 0; font-size: .85rem; color: var(--zs-muted); }\n.zs-ev strong { color: var(--zs-ink); }\n.zs-k { color: var(--zs-muted); }\n.zs-kv { display: inline-block; margin-right: 12px; }\n.zs-code, .zs-tok { font: 12px/1.4 ui-monospace, Menlo, monospace; background: var(--zs-soft); border-radius: 4px; padding: 0 5px; margin-right: 4px; }\n.zs-rule { color: var(--zs-muted); font-size: .8rem; }\n.zs-evidence { margin: 4px 0; }\n.zs-quote { margin: 4px 0; }\n.zs-quote figcaption { font-size: .75rem; font-weight: 600; color: var(--zs-muted); }\n.zs-quote blockquote { margin: 2px 0 0; padding: 4px 10px; border-left: 3px solid var(--zs-line); font-style: italic; color: var(--zs-muted); font-size: .88rem; }\n.zs-todo { margin: 6px 0 2px; padding: 6px 10px; border: 1px solid var(--zs-warn); background: var(--zs-warn-bg); border-radius: 8px; }\n.zs-todo-text { margin: 0 0 4px; font-size: .9rem; }\n.zs-todo-btns { display: flex; flex-wrap: wrap; gap: 6px; margin: 4px 0; }\n.zs-btn { font: inherit; font-size: .88rem; font-weight: 600; min-height: 44px; padding: 4px 12px; border: 1px solid var(--zs-accent); background: var(--zs-surface); color: var(--zs-accent); border-radius: 8px; cursor: pointer; }\n.zs-btn:focus-visible { outline: 3px solid var(--zs-accent); outline-offset: 2px; }\n.zs-more { margin: 4px 0; }\n.zs-more > summary { cursor: pointer; font-size: .85rem; font-weight: 600; min-height: 32px; }\n.zs-pre { white-space: pre-wrap; overflow-wrap: anywhere; font: 12px/1.4 ui-monospace, Menlo, monospace; background: var(--zs-soft); padding: 6px; border-radius: 6px; max-height: 14rem; overflow: auto; }\n.zs-counts { margin: 4px 0; }\n.zs-legend { margin: 6px 0 0; font-size: .78rem; color: var(--zs-muted); }\n.zs-section h3 { margin: 12px 0 6px; }\n.zs-blockers, .zj-list { list-style: none; margin: 4px 0; padding: 0; }\n.zs-blocker { display: flex; flex-wrap: wrap; align-items: center; gap: 2px 8px; padding: 4px 0; border-top: 1px solid var(--zs-line); }\n.zs-blocker-name { font-weight: 700; }\n.zs-flash { outline: 3px solid var(--zs-accent); outline-offset: 3px; }\n@media (prefers-reduced-motion: no-preference) { .zs-flash { transition: outline-color .4s; } }\n\n/* \"How the AI was checked\" */\n.zj-models { margin: 4px 0; }\n.zj-tiles { list-style: none; margin: 8px 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(8.5rem, 1fr)); gap: 8px; }\n.zj-tile { border: 1px solid var(--zs-line); border-radius: var(--zs-radius); padding: 8px 10px; background: var(--zs-surface); display: flex; flex-direction: column; }\n.zj-n { font-size: 1.4rem; font-variant-numeric: tabular-nums; }\n.zj-l { font-size: .8rem; color: var(--zs-muted); }\n.zj-group h3 { margin: 14px 0 4px; }\n.zj-row { border: 1px solid var(--zs-line); border-left: 4px solid var(--zs-warn); border-radius: 8px; padding: 8px 10px; margin: 6px 0; background: var(--zs-surface); }\n[data-testid=\"judge-disagreements\"] .zj-row { border-left-color: var(--zs-accent); }\n.zj-by .zj-row { border-left-color: var(--zs-line); }\n@media (max-width: 480px) {\n  .zs-step { padding-left: calc(var(--zs-marker) + 10px); }\n  .zs-todo-btns .zs-btn { flex: 1 1 100%; }\n  .zj-tiles { grid-template-columns: repeat(2, 1fr); }\n}\nEOF\npython3 - <<'EOF'\nimport re\np='index.html'; s=open(p).read()\ns=s.replace('<link rel=\"stylesheet\" href=\"review.css\">','<link rel=\"stylesheet\" href=\"review.css\">\\n<link rel=\"stylesheet\" href=\"stepper.css\">')\ns=s.replace('<script src=\"timeline.js\"></script>','<script src=\"stepper.js\"></script>\\n<script src=\"timeline.js\"></script>')\ns=s.replace('<script src=\"audit.js\"></script>','<script src=\"audit.js\"></script>\\n<script src=\"judges.js\"></script>')\nopen(p,'w').write(s)\np='api.js'; s=open(p).read()\ns=s.replace('    review: (token, id, body)','    trace: (token, id) => call(\"GET\", t(token) + \"/items/\" + encodeURIComponent(id) + \"/trace\"),\\n    caseTrace: (token) => call(\"GET\", t(token) + \"/trace\"),\\n    judges: (token) => call(\"GET\", t(token) + \"/judges\"),\\n    review: (token, id, body)')\nopen(p,'w').write(s)\nEOF\ngrep -n \"stepper\\|judges\" index.html api.js"
}
````

### User / tool · 2026-11-02T03:26:06.291Z

**tool result**
````
index.html:9:<link rel="stylesheet" href="stepper.css">
index.html:52:<script src="stepper.js"></script>
index.html:60:<script src="judges.js"></script>
api.js:36:    judges: (token) => call("GET", t(token) + "/judges"),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:13.889Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\np='timeline.js'; s=open(p).read()\n# 1. Why panel: stepper after the sentence, raw ladder collapsed\nold='''        el(\"p\", { class: \"why-sentence\", \"data-testid\": \"why-text\" }, it.why),\n        el(\"dl\", { class: \"kv\", \"data-testid\": \"why-ladder\" },'''\nnew='''        el(\"p\", { class: \"why-sentence\", \"data-testid\": \"why-text\" }, it.why),\n        ZL.stepper ? ZL.stepper.itemSection(s.token, id) : null,\n        el(\"details\", { class: \"zs-more\" }, el(\"summary\", {}, \"Recorded ladder (raw state and checks)\"), el(\"dl\", { class: \"kv\", \"data-testid\": \"why-ladder\" },'''\nassert old in s; s=s.replace(old,new)\nold='''lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || \"\"}` : \"none (calculated by code)\")),'''\nnew='''lad.judge ? `${lad.judge.verdict} · ${lad.judge.model} · ${lad.judge.prompt_version || \"\"}` : \"none (calculated by code)\"))),'''\nassert old in s; s=s.replace(old,new)\n# 2. case stepper above the timeline toolbar\nold='''    const wrap = el(\"div\", { \"data-testid\": \"timeline\" }); mount.append(wrap);\n    wrap.append('''\nnew='''    const wrap = el(\"div\", { \"data-testid\": \"timeline\" }); mount.append(wrap);\n    if (ZL.stepper) ZL.stepper.mountCase(wrap);\n    wrap.append('''\nassert old in s; s=s.replace(old,new)\n# 3. tray trace button\nold='''        el(\"div\", { class: \"row-actions\" }, recs.map((r) => el(\"button\", { type: \"button\", class: \"btn small\", onclick'''\nassert old in s\ns=s.replace(old,'''        el(\"div\", { class: \"row-actions\" }, ZL.stepper ? ZL.stepper.traceButton(t.id, \"btn small\") : null, recs.map((r) => el(\"button\", { type: \"button\", class: \"btn small\", onclick''')\nopen(p,'w').write(s)\np='flags.js'; s=open(p).read()\nold='''    a.append(RV.controls(f, \"flag\"));'''\nnew='''    if (ZL.stepper) a.append(el(\"div\", { class: \"rv-actions\" }, ZL.stepper.traceButton(f.id)));\n    a.append(RV.controls(f, \"flag\"));'''\nassert old in s; s=s.replace(old,new); open(p,'w').write(s)\np='charges.js'; s=open(p).read()\nold='''      el(\"button\", { type: \"button\", class: \"rv-btn rv-secondary\", \"data-testid\": \"btn-source\", onclick: () => RV.openSource(a, \"amount\") }, \"Open record \" + recSeq(c, (a.record_ids || [])[0])));'''\nnew='''      el(\"button\", { type: \"button\", class: \"rv-btn rv-secondary\", \"data-testid\": \"btn-source\", onclick: () => RV.openSource(a, \"amount\") }, \"Open record \" + recSeq(c, (a.record_ids || [])[0])),\n      ZL.stepper ? ZL.stepper.traceButton(a.id) : null);'''\nassert old in s; s=s.replace(old,new); open(p,'w').write(s)\nEOF\nsed -n 105,112p timeline.js | cut -c1-150; sed -n 96,100p timeline.js | cut -c1-120"
}
````

### User / tool · 2026-11-02T03:26:14.027Z

**tool result**
````
    });
    return box;
  }

  // ---- Why? panel
  const checkText = (v) => (v === true ? "passed" : v === false ? "FAILED" : Array.isArray(v) ? (v.length ? v.join(", ") : "none") : String(v));
  async function openWhy(id) {
    const s = ZL.state.get(), dlg = ZL.$("#why-modal"), body = ZL.$("#why-body"); clear(body);
    c.tray.forEach((t) => {
      const recs = t.record_ids.map((id) => c.records.find((r) => r.id === id)).filter(Boolean);
      const item = el("article", { class: "entry st-rejected", "data-testid": "tray-item", "data-item-id": t.id },
        el("div", { class: "entry-head" }, el("span", { class: "provider" }, recs.map((r) => `Record ${r.seq}: ${r.sourc
        el("p", { class: "reason", "data-testid": "tray-reason" }, `${t.reasons.map(reasonText).join("; ")}`),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:19.396Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && for f in stepper judges timeline flags charges api; do node --check $f.js && echo ok $f; done; cd .. ; cd ..; cat > artifacts/tmp/shot.py <<'EOF'\nimport sys\nfrom playwright.sync_api import sync_playwright\nBASE=\"http://localhost:7871\"\ntok=sys.argv[1]; out=sys.argv[2]\nwith sync_playwright() as p:\n    b=p.chromium.launch(); \n    for name,w,h in ((\"1440\",1440,1000),(\"390\",390,844)):\n        pg=b.new_context(viewport={\"width\":w,\"height\":h}).new_page()\n        errs=[]; pg.on(\"pageerror\",lambda e:errs.append(str(e))); pg.on(\"console\",lambda m: m.type==\"error\" and errs.append(m.text))\n        pg.goto(f\"{BASE}/#/case/{tok}\"); pg.get_by_test_id(\"timeline\").wait_for()\n        pg.wait_for_timeout(800)\n        pg.screenshot(path=f\"{out}-{name}.png\",full_page=False)\n        print(name,errs)\n    b.close()\nEOF\n.venv/bin/python artifacts/tmp/shot.py TZxnjsY6Lkcukz7bUsgsgQ artifacts/tmp/try"
}
````

### User / tool · 2026-11-02T03:26:22.152Z

**tool result**
````
ok stepper
/Users/arsis/zlayt-pm-project/app/frontend/judges.js:74
          el("span", { class: "zs-k" }, "Prompt "), j.prompt_version || "", el("span", { class: "zs-k" }, " · model "), (j.models || []).join(", "))))))));
                                                                                                                                                         ^

SyntaxError: Unexpected token ')'
    at internalCompileFunction (node:internal/vm:128:18)
    at wrapSafe (node:internal/modules/cjs/loader:1279:20)
    at node:internal/main/check_syntax:81:41
    at loadESM (node:internal/process/esm_loader:28:13)
    at checkSyntax (node:internal/main/check_syntax:81:21)

Node.js v21.7.1
ok timeline
ok flags
ok charges
ok api
1440 ["Unexpected token ')'"]
390 ["Unexpected token ')'"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:24.342Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && sed -i 's/(j.models || \\[\\]).join(\", \"))))))));/(j.models || []).join(\", \")))))));/' judges.js && node --check judges.js && cd ../.. && .venv/bin/python artifacts/tmp/shot.py TZxnjsY6Lkcukz7bUsgsgQ artifacts/tmp/try"
}
````

### User / tool · 2026-11-02T03:26:24.442Z

**tool result (error)**
````
Exit code 1
sed: 1: "judges.js
": invalid command code j
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:26.557Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\ns=open('judges.js').read()\ns=s.replace('(j.models || []).join(\", \"))))))));','(j.models || []).join(\", \")))))));')\nopen('judges.js','w').write(s)\nEOF\nnode --check judges.js && cd ../.. && .venv/bin/python artifacts/tmp/shot.py TZxnjsY6Lkcukz7bUsgsgQ artifacts/tmp/try"
}
````

### User / tool · 2026-11-02T03:26:29.154Z

**tool result**
````
1440 []
390 []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:30.283Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/tmp/try-1440.png"
}
````

### User / tool · 2026-11-02T03:26:30.314Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:35.409Z

**tool call — Bash**
````
{
 "command": "grep -rn \"ZLAYT_DB\\|sqlite3\" app/config.py app/backend/*.py app/db/*.py 2>/dev/null | head -5; ls -la artifacts/tmp/*.sqlite3 data 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T03:26:35.533Z

**tool result**
````
app/db/db.py:13:import sqlite3
app/db/db.py:41:        probe = sqlite3.connect(path)
app/db/db.py:52:    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
app/db/db.py:53:    conn.row_factory = sqlite3.Row
data:
total 14392
drwxr-xr-x@  3 arsis  staff       96 Nov  1 21:26 .
drwxr-xr-x  27 arsis  staff      864 Nov  1 20:37 ..
-rw-r--r--@  1 arsis  staff  7290880 Nov  1 21:26 zlayt.sqlite
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:36.607Z

**tool call — Bash**
````
{
 "command": "grep -rn \"environ\" app/db/db.py app/backend/api.py app/main.py | head; "
}
````

### User / tool · 2026-11-02T03:26:36.718Z

**tool result**
````
app/backend/api.py:78:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:92:    db_path = db_path or os.path.join(os.environ.get("DATA_DIR", str(ROOT / "data")), "zlayt.sqlite")
app/backend/api.py:102:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
app/backend/api.py:104:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
app/backend/api.py:114:        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
app/backend/api.py:120:        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}
app/backend/api.py:346:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py:535:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
app/main.py:14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:41.404Z

**tool call — Bash**
````
{
 "command": "pkill -f \"PORT=7871\" ; kill $(lsof -ti :7871) 2>/dev/null; sleep 1; rm -rf artifacts/tmp/fe-data; mkdir -p artifacts/tmp/fe-data; (DATA_DIR=artifacts/tmp/fe-data LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local PORT=7871 nohup .venv/bin/python -m app.main > artifacts/tmp/frontend-t081.log 2>&1 &); sleep 4\ncat > artifacts/tmp/mk.py <<'EOF'\nimport json,urllib.request,time,sys\nB=\"http://localhost:7871/api\"\ndef api(m,p,b=None):\n    r=urllib.request.Request(B+p,method=m,data=json.dumps(b).encode() if b is not None else None,headers={\"Content-Type\":\"application/json\"})\n    with urllib.request.urlopen(r,timeout=60) as x: raw=x.read(); return (json.loads(raw) if raw else None)\nout={}\nfor key,body in ((\"sample\",{\"sample\":True}),(\"lib06\",{\"library\":\"case_lib06_lop_billed_vs_adjusted\"}),(\"lib05\",{\"library\":\"case_lib05_pedestrian_orif_hardware\"})):\n    tok=api(\"POST\",\"/cases\",body)[\"token\"]; api(\"POST\",f\"/cases/{tok}/run\",{})\n    while api(\"GET\",f\"/cases/{tok}/status\")[\"status\"] not in(\"ready\",\"failed\"): time.sleep(.3)\n    out[key]=tok\njson.dump(out,open(\"artifacts/tmp/toks.json\",\"w\")); print(out)\nEOF\n.venv/bin/python artifacts/tmp/mk.py"
}
````

### User / tool · 2026-11-02T03:26:47.998Z

**tool result**
````
{'sample': '1MvRvGAnVYTUakJP47yz7g', 'lib06': 'VhsRSub4MqM1GIDQerAxqg', 'lib05': 'zs6Uyzk_lH2Hipmw2Bgc4Q'}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:49.323Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/tmp/shot.py VhsRSub4MqM1GIDQerAxqg artifacts/tmp/try"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:49.652Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/tmp/try-1440.png"
}
````

### User / tool · 2026-11-02T03:26:51.859Z

**tool result**
````
1440 []
390 []
````

### User / tool · 2026-11-02T03:26:51.873Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:26:56.703Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/tmp/shots.py <<'EOF'\nimport sys,json\nfrom playwright.sync_api import sync_playwright\nBASE=\"http://localhost:7871\"; T=json.load(open(\"artifacts/tmp/toks.json\")); OUT=\"artifacts/screenshots/\"\nwith sync_playwright() as p:\n    b=p.chromium.launch()\n    for name,w,h in ((\"1440\",1440,1000),(\"390\",390,844)):\n        pg=b.new_context(viewport={\"width\":w,\"height\":h}).new_page()\n        errs=[]; pg.on(\"pageerror\",lambda e:errs.append(str(e)))\n        pg.goto(f\"{BASE}/#/case/{T['lib06']}\"); pg.get_by_test_id(\"timeline\").wait_for(); pg.wait_for_timeout(700)\n        cs=pg.get_by_test_id(\"case-stepper\")\n        if cs.locator(\"details\").get_attribute(\"open\") is None: cs.locator(\"summary\").click()\n        cs.screenshot(path=OUT+f\"stepper-case-{name}.png\")\n        # item stepper: amount a3 (judge disagrees) from the charges panel\n        pg.locator('[data-trace-for=\"a3\"]').first.click(); pg.get_by_test_id(\"item-stepper\").wait_for(); pg.wait_for_timeout(300)\n        pg.locator(\"#why-modal\").screenshot(path=OUT+f\"stepper-item-{name}.png\")\n        pg.keyboard.press(\"Escape\")\n        jp=pg.get_by_test_id(\"judge-panel\"); jp.scroll_into_view_if_needed(); jp.screenshot(path=OUT+f\"judge-panel-{name}.png\")\n        print(name,errs)\n    b.close()\nEOF\n.venv/bin/python artifacts/tmp/shots.py"
}
````

### User / tool · 2026-11-02T03:26:58.132Z

**tool result (error)**
````
Exit code 1
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/tmp/shots.py", line 11, in <module>
    if cs.locator("details").get_attribute("open") is None: cs.locator("summary").click()
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py", line 11798, in get_attribute
    self._sync(
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_sync_base.py", line 111, in _sync
    return task.result()
           ^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py", line 481, in get_attribute
    return await self._frame.get_attribute(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py", line 762, in get_attribute
    return await self._channel.send(
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 78, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 636, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.Error: Locator.get_attribute: Error: strict mode violation: get_by_test_id("case-stepper").locator("details") resolved to 2 elements:
    1) <details open="" class="zs-case-det">…</details> aka get_by_text("Case checks 6/10 passed 20 items still need your decision20 items still need")
    2) <details class="zs-more">…</details> aka get_by_text("Show the other 142026-09-02")

Call log:
  - waiting for get_by_test_id("case-stepper").locator("details")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:27:00.062Z

**tool call — Bash**
````
{
 "command": "sed -i 's/cs.locator(\"details\").get_attribute(\"open\") is None: cs.locator(\"summary\").click()/cs.locator(\".zs-case-det\").get_attribute(\"open\") is None: cs.locator(\".zs-case-det > summary\").click()/' artifacts/tmp/shots.py && .venv/bin/python artifacts/tmp/shots.py"
}
````

### User / tool · 2026-11-02T03:27:00.164Z

**tool result (error)**
````
Exit code 1
sed: 1: "artifacts/tmp/shots.py
": command a expects \ followed by text
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:27:01.743Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='artifacts/tmp/shots.py'; s=open(p).read()\ns=s.replace('cs.locator(\"details\").get_attribute(\"open\") is None: cs.locator(\"summary\").click()','cs.locator(\".zs-case-det\").get_attribute(\"open\") is None: cs.locator(\".zs-case-det > summary\").click()')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python artifacts/tmp/shots.py"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:27:02.128Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/stepper-case-1440.png"
}
````

### User / tool · 2026-11-02T03:27:05.691Z

**tool result**
````
1440 []
390 []
````

### User / tool · 2026-11-02T03:27:05.868Z

**tool result**
````
[image]
````

### User / tool · 2026-11-02T03:27:05.865Z

[Image: original 926x2086, displayed at 888x2000. Multiply coordinates by 1.04 to map to original image.]

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:27:10.572Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/stepper-item-390.png"
}
````

### User / tool · 2026-11-02T03:27:10.584Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:27:10.891Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/judge-panel-1440.png"
}
````

### User / tool · 2026-11-02T03:27:11.046Z

**tool result**
````
[image]
````

### User / tool · 2026-11-02T03:27:11.041Z

[Image: original 926x2319, displayed at 799x2000. Multiply coordinates by 1.16 to map to original image.]

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:27:16.188Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/app/frontend && python3 - <<'EOF'\ns=open('stepper.js').read()\nold='''      el(\"p\", { class: \"zs-top\" }, el(\"span\", { class: \"zs-verdict zs-v-\" + (v.code || \"none\"), \"data-testid\": \"case-verdict\" }, v.label || \"\"), \" \",\n        el(\"span\", { class: \"zs-progress\", \"data-testid\": \"case-progress\" }, passed + \"/\" + steps.length + \" passed\")),'''\nnew='''      el(\"p\", { class: \"zs-top\" }, el(\"span\", { class: \"zs-verdict zs-v-\" + (v.code || \"none\"), \"data-testid\": \"case-verdict\" }, v.label || \"\"),\n        el(\"span\", { class: \"zs-progress\", \"data-testid\": \"case-progress\" }, passed + \" of \" + steps.length + \" checks passed; the rest are for you or still open\")),'''\nassert old in s; s=s.replace(old,new)\ns=s.replace('''        el(\"span\", { class: \"zs-sumv\" }, tr && tr.verdict ? tr.verdict.label : \"\")),''','''        \"\"),''')\nopen('stepper.js','w').write(s)\nEOF\nnode --check stepper.js; cd ../..; sed -n 1,30p tests/e2e/test_keyboard_mobile.py; ls evals/library | head -3"
}
````

### User / tool · 2026-11-02T03:27:16.356Z

**tool result**
````
"""Keyboard and mobile. R-RV-8, R-ST-1, a11y."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e.conftest import api, open_case, golden_text, BASE


def test_keyboard_only_accept_flow(page, sample_case):
    """R-RV-8: Tab to the first queue item, Enter opens, 'a' accepts, 'd' dismisses (documented shortcuts)."""
    open_case(page, sample_case); page.get_by_test_id("queue").locator("[data-item-id]").first.focus(); page.keyboard.press("a")
    expect(page.locator("[data-review=accepted]")).to_have_count(1)

def test_mobile_375_modal_not_side_by_side(pw, sample_case):
    """R-ST-1: at 375 px the source record opens as a modal and nothing scrolls horizontally."""
    b = pw.chromium.launch(); pg = b.new_context(viewport={"width": 375, "height": 800}).new_page(); open_case(pg, sample_case)
    pg.get_by_test_id("entry-1").get_by_test_id("btn-source").click(); assert pg.get_by_test_id("record-modal").is_visible()
    assert pg.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"); b.close()

def test_focus_visible_on_buttons(page, sample_case):
    """a11y: focused buttons have a visible outline."""
    open_case(page, sample_case); page.get_by_test_id("entry-1").get_by_test_id("btn-accept").focus()
    assert page.evaluate("getComputedStyle(document.activeElement).outlineStyle") != "none"
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:27:53.526Z

**tool call — Bash**
````
{
 "command": "cat > tests/e2e/test_stepper.py <<'EOF'\n\"\"\"Vertical steppers (T-081) and the 'How the AI was checked' panel (T-082, D-042). Needs the fixture backend; the library case needs ZLAYT_MODE=local.\"\"\"\nimport re\nimport time\nimport pytest\nfrom playwright.sync_api import expect\nfrom tests.e2e.conftest import api, open_case, BASE\n\nCASE_STEPS = [\"ingest\", \"split\", \"dates\", \"extract\", \"grounding\", \"judges\", \"flags\", \"totals\", \"review\", \"export_gate\"]\n\n\ndef _run(tok):\n    assert api(\"POST\", f\"/api/cases/{tok}/run\", {})[0] == 202\n    for _ in range(300):\n        s = api(\"GET\", f\"/api/cases/{tok}/status\")[1]\n        if s[\"status\"] in (\"ready\", \"failed\"):\n            break\n        time.sleep(.5)\n    assert s[\"status\"] == \"ready\"\n\n\n@pytest.fixture\ndef judged_case():\n    \"\"\"Library L6: three judge objections (two amounts, one flag) and several code-vs-AI disagreements. Local mode only.\"\"\"\n    st, c = api(\"POST\", \"/api/cases\", {\"library\": \"case_lib06_lop_billed_vs_adjusted\"})\n    if st not in (200, 201):\n        pytest.skip(\"library cases need ZLAYT_MODE=local\")\n    _run(c[\"token\"])\n    yield c[\"token\"]\n    api(\"DELETE\", f\"/api/cases/{c['token']}\")\n\n\ndef open_why(page, n=8):\n    page.get_by_test_id(f\"entry-{n}\").get_by_test_id(\"entry-why\").click()\n    page.get_by_test_id(\"item-stepper\").wait_for()\n    return page.get_by_test_id(\"item-stepper\")\n\n\n# ---- item stepper\ndef test_item_stepper_in_why_panel(page, sample_case):\n    \"\"\"Why? shows an ordered list of steps with a status word, a kind chip (Code / AI draft / AI check / You) and the plain-words why.\"\"\"\n    open_case(page, sample_case); st = open_why(page)\n    assert st.locator(\"ol\").count() == 1\n    steps = st.get_by_test_id(\"step\")\n    assert steps.count() >= 8\n    kinds = {steps.nth(i).get_by_test_id(\"step-kind\").inner_text() for i in range(steps.count())}\n    assert {\"Code\", \"AI check\", \"You\"} <= kinds\n    for i in range(steps.count()):\n        s = steps.nth(i)\n        assert s.get_attribute(\"data-status\") in (\"pass\", \"fail\", \"skipped\", \"pending\")\n        assert s.get_by_test_id(\"step-why\").inner_text().strip()\n        assert s.get_by_test_id(\"step-status\").inner_text().strip() in (\"Passed\", \"Failed\", \"Skipped\", \"Not done yet\")\n        assert s.get_by_test_id(\"step-marker\").inner_text().strip() in (\"✓\", \"✕\", \"–\", \"○\")   # glyph plus word, never colour alone\n\n\ndef test_pending_human_step_says_what_to_do(page, sample_case):\n    \"\"\"The human step is pending until you decide, carries aria-current=step, and states what you need to do with a working button.\"\"\"\n    open_case(page, sample_case); st = open_why(page)\n    human = st.locator('[data-step-id=\"human\"]')\n    expect(human).to_have_attribute(\"data-status\", \"pending\")\n    expect(human).to_have_attribute(\"aria-current\", \"step\")\n    assert st.locator('[aria-current=\"step\"]').count() == 1\n    assert \"What you need to do\" in human.get_by_test_id(\"step-action\").inner_text()\n    human.get_by_test_id(\"btn-step-action\").focus(); page.keyboard.press(\"Enter\")          # keyboard: lands on the item's own controls\n    expect(page.locator(\"#why-modal\")).not_to_be_visible()\n    assert page.evaluate(\"!!document.activeElement.closest('[data-item-id]')\")\n\n\ndef test_decision_settles_the_human_step(page, sample_case):\n    \"\"\"After you accept, the human step passes.\"\"\"\n    open_case(page, sample_case)\n    page.get_by_test_id(\"entry-8\").get_by_test_id(\"btn-accept\").click()\n    expect(page.get_by_test_id(\"entry-8\")).to_have_attribute(\"data-review\", \"accepted\")\n    st = open_why(page)\n    expect(st.locator('[data-step-id=\"human\"]')).to_have_attribute(\"data-status\", \"pass\")\n\n\ndef test_flag_and_charge_cards_open_their_stepper(page, sample_case):\n    \"\"\"Flags and charges have no Why? button; a 'How it was checked' button opens the same stepper (flags: code-made flags skip the judge on purpose).\"\"\"\n    open_case(page, sample_case)\n    page.get_by_test_id(\"flags-panel\").get_by_test_id(\"btn-trace\").first.click()\n    st = page.get_by_test_id(\"item-stepper\"); st.wait_for()\n    assert st.locator('[data-step-id=\"human\"]').count() == 1\n    page.keyboard.press(\"Escape\")\n    page.get_by_test_id(\"charges-panel\").get_by_test_id(\"btn-trace\").first.click()\n    page.get_by_test_id(\"item-stepper\").wait_for()\n    assert page.get_by_test_id(\"item-stepper\").locator('[data-step-id=\"found_in_text\"]').count() == 1\n\n\ndef test_failed_step_shows_reason_evidence_and_action(page, judged_case):\n    \"\"\"A judge objection renders as a failed AI-check step with the fixed-sentence reason and a 'What you need to do' line.\"\"\"\n    open_case(page, judged_case)\n    page.locator('[data-trace-for]').first.wait_for()\n    page.get_by_test_id(\"charges-panel\").get_by_test_id(\"btn-trace\").first.click()\n    st = page.get_by_test_id(\"item-stepper\"); st.wait_for()\n    judge = st.locator('[data-step-id^=\"judge\"]')\n    expect(judge).to_have_attribute(\"data-status\", \"fail\")\n    assert judge.get_by_test_id(\"step-kind\").inner_text() == \"AI check\"\n    assert \"second AI check said\" in judge.get_by_test_id(\"step-judge-reason\").inner_text().lower()\n    assert \"What you need to do\" in judge.get_by_test_id(\"step-action\").inner_text()\n    assert st.locator('[data-status=\"fail\"]').count() >= 1\n\n\n# ---- case stepper\ndef test_case_stepper_order_progress_and_gate(page, sample_case):\n    \"\"\"Ten case steps in the fixed order, 'x/10 passed', and the export gate lists each blocker.\"\"\"\n    open_case(page, sample_case)\n    cs = page.get_by_test_id(\"case-stepper\"); cs.get_by_test_id(\"case-step\").first.wait_for()\n    ids = cs.get_by_test_id(\"case-step\").evaluate_all(\"els => els.map(e => e.getAttribute('data-step-id'))\")\n    assert ids == CASE_STEPS\n    assert re.fullmatch(r\"\\d+/10 passed\", cs.get_by_test_id(\"case-summary-progress\").inner_text())\n    gate = cs.locator('[data-step-id=\"export_gate\"]')\n    expect(gate).to_have_attribute(\"data-status\", \"fail\")\n    n = gate.get_by_test_id(\"gate-blocker\").count()\n    assert n >= 1\n    assert cs.locator('[aria-current=\"step\"]').count() == 1\n\n\ndef test_gate_blocker_jump_and_update(page, sample_case):\n    \"\"\"A blocker's jump link focuses that item; deciding the item removes it from the gate.\"\"\"\n    open_case(page, sample_case)\n    gate = page.get_by_test_id(\"case-stepper\").locator('[data-step-id=\"export_gate\"]'); gate.wait_for()\n    first = gate.get_by_test_id(\"gate-blocker\").first; tid = first.get_attribute(\"data-jump-item\"); before = gate.get_by_test_id(\"gate-blocker\").count()\n    first.get_by_test_id(\"btn-gate-jump\").focus(); page.keyboard.press(\"Enter\")\n    assert page.evaluate(\"document.activeElement.getAttribute('data-item-id')\") == tid\n    page.keyboard.press(\"d\")\n    expect(page.locator(f'[data-item-id=\"{tid}\"]').first).to_have_attribute(\"data-review\", \"dismissed\")\n    page.wait_for_function(\"(n) => document.querySelectorAll('[data-testid=gate-blocker]').length < n\", arg=before, timeout=8000)\n\n\ndef test_case_stepper_marks_failed_judges_and_links_to_panel(page, judged_case):\n    \"\"\"The judges step fails when the AI objected, shows x/y counts, and links to the AI-check panel.\"\"\"\n    open_case(page, judged_case)\n    cs = page.get_by_test_id(\"case-stepper\"); cs.get_by_test_id(\"case-step\").first.wait_for()\n    j = cs.locator('[data-step-id=\"judges\"]')\n    expect(j).to_have_attribute(\"data-status\", \"fail\")\n    assert \"unsupported 3\" in j.get_by_test_id(\"step-counts\").inner_text()\n    j.get_by_test_id(\"btn-to-judges\").click()\n    expect(page.get_by_test_id(\"judge-panel\")).to_be_visible()\n\n\n# ---- judge panel\ndef test_judge_panel_is_labelled_and_complete(page, judged_case):\n    \"\"\"T-082: labelled as AI quality checks and not a verdict; shows counts, models, prompt versions, rejections and code-vs-AI disagreements.\"\"\"\n    open_case(page, judged_case)\n    jp = page.get_by_test_id(\"judge-panel\"); jp.get_by_test_id(\"judge-totals\").wait_for()\n    label = jp.get_by_test_id(\"judge-label\").inner_text()\n    assert \"AI quality checks\" in label and \"not a verdict\" in label\n    totals = jp.get_by_test_id(\"judge-totals\").inner_text().lower()\n    for w in (\"items checked by ai\", \"supported\", \"ai objected\", \"could not decide\", \"unavailable\"):\n        assert w in totals\n    assert re.search(r\"claude-\\S+\", jp.get_by_test_id(\"judge-model-line\").inner_text())\n    assert \"_v\" in jp.get_by_test_id(\"judge-prompts\").inner_text()\n    assert jp.get_by_test_id(\"judge-rejection\").count() == 3\n    assert jp.get_by_test_id(\"judge-disagreement\").count() >= 1\n    j = api(\"GET\", f\"/api/cases/{judged_case}/judges\")[1]\n    assert str(j[\"totals\"][\"items_judged\"]) in totals.replace(\"\\n\", \" \")\n\n\ndef test_judge_rejection_links_to_item_stepper(page, judged_case):\n    \"\"\"Each rejection opens the item's stepper (via the keyboard) and can jump to the item.\"\"\"\n    open_case(page, judged_case)\n    row = page.get_by_test_id(\"judge-panel\").get_by_test_id(\"judge-rejection\").first; row.wait_for()\n    tid = row.get_attribute(\"data-target-item\")\n    row.get_by_test_id(\"btn-judge-steps\").focus(); page.keyboard.press(\"Enter\")\n    st = page.get_by_test_id(\"item-stepper\"); st.wait_for()\n    assert st.locator('[data-status=\"fail\"][data-step-id^=\"judge\"]').count() == 1\n    page.keyboard.press(\"Escape\")\n    row.get_by_test_id(\"btn-judge-goto\").click()\n    assert page.evaluate(\"document.activeElement.getAttribute('data-item-id')\") == tid\n\n\ndef test_judge_panel_when_nothing_objected(page, sample_case):\n    \"\"\"A clean case says so plainly; the panel is still there.\"\"\"\n    open_case(page, sample_case)\n    jp = page.get_by_test_id(\"judge-panel\"); jp.get_by_test_id(\"judge-totals\").wait_for()\n    assert \"No objections\" in jp.inner_text()\n    assert jp.get_by_test_id(\"judge-rejection\").count() == 0\n\n\n# ---- mobile\ndef test_steppers_usable_at_390(pw, sample_case):\n    \"\"\"At 390 px the case stepper, the item stepper and their buttons fit without horizontal scroll; buttons are touch-sized.\"\"\"\n    b = pw.chromium.launch(); pg = b.new_context(viewport={\"width\": 390, \"height\": 844}).new_page(); open_case(pg, sample_case)\n    cs = pg.get_by_test_id(\"case-stepper\"); cs.locator(\"summary\").wait_for(); cs.locator(\"summary\").click()\n    cs.get_by_test_id(\"case-step\").first.wait_for()\n    assert pg.evaluate(\"document.documentElement.scrollWidth <= window.innerWidth + 1\")\n    for btn in cs.get_by_test_id(\"btn-gate-jump\").all()[:3]:\n        assert btn.bounding_box()[\"height\"] >= 40\n    pg.get_by_test_id(\"entry-8\").get_by_test_id(\"entry-why\").click(); pg.get_by_test_id(\"item-stepper\").wait_for()\n    assert pg.evaluate(\"document.documentElement.scrollWidth <= window.innerWidth + 1\")\n    assert pg.evaluate(\"(() => { const d = document.querySelector('#why-modal'); return d.scrollWidth <= d.clientWidth + 1; })()\")\n    b.close()\nEOF\npython3 - <<'EOF'\np='tests/e2e/conftest.py'; s=open(p).read()\nold='Optional test hook:'\nnew='''  T-081/T-082 (D-042, steppers and AI-check panel): item-stepper (in the Why panel, with data-verdict), item-verdict, item-progress, step (one per step: data-step-id, data-status = pass|fail|skipped|pending, data-kind = code|llm|human; aria-current=step on the one the human must act on),\n  step-marker (glyph), step-kind (Code | AI draft | AI check | You), step-status (word), step-why, step-evidence, step-values, step-judge-reason, step-tech, step-counts, step-action ('What you need to do' line), btn-step-action (data-action-code), btn-trace (How it was checked; on flag and charge cards and tray items; data-trace-for = item id),\n  case-stepper (details, open on wide screens), case-summary-progress ('x/10 passed'), case-verdict, case-progress, case-step (same attributes as step; ids ingest..export_gate), gate-blockers, gate-blocker (data-jump-item = item id), btn-gate-jump, btn-to-judges,\n  judge-panel, judge-label, judge-model-line, judge-prompts, judge-totals, judge-by-check, judge-rejections, judge-rejection, judge-unresolved-list, judge-unresolved, judge-disagreements, judge-disagreement (rows carry data-target-item, never data-item-id), btn-judge-steps, btn-judge-goto.\nOptional test hook:'''\nassert old in s; s=s.replace(old,new,1); open(p,'w').write(s)\nEOF\nE2E_BASE_URL=http://localhost:7871 .venv/bin/python -m pytest tests/e2e/test_stepper.py tests/unit/test_e2e_contract.py -x -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T03:28:05.341Z

**tool result**
````
judged_case = 'VLELJ_15VXnWtHsflVTiVA'

    def test_failed_step_shows_reason_evidence_and_action(page, judged_case):
        """A judge objection renders as a failed AI-check step with the fixed-sentence reason and a 'What you need to do' line."""
        open_case(page, judged_case)
        page.locator('[data-trace-for]').first.wait_for()
        page.get_by_test_id("charges-panel").get_by_test_id("btn-trace").first.click()
        st = page.get_by_test_id("item-stepper"); st.wait_for()
        judge = st.locator('[data-step-id^="judge"]')
>       expect(judge).to_have_attribute("data-status", "fail")
E       AssertionError: Locator expected to have attribute 'fail'
E       Actual value: pass 
E       Call log:
E         - Expect "to_have_attribute" get_by_test_id("item-stepper").locator("[data-step-id^=\"judge\"]") with timeout 5000ms
E         - waiting for get_by_test_id("item-stepper").locator("[data-step-id^=\"judge\"]")
E           14 × locator resolved to <li class="zs-step" data-kind="llm" data-testid="step" data-status="pass" data-step-id="judge_2">…</li>
E              - unexpected value "pass"
E       
E       Aria snapshot:
E       - listitem:
E         - text: "Second AI check: is this figure a charge, rate or estimate? AI check Passed"
E         - paragraph: The second check agreed with the rule's reading of this figure.
E         - paragraph
E         - group: Technical details

tests/e2e/test_stepper.py:96: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_stepper.py::test_failed_step_shows_reason_evidence_and_action
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
1 failed, 4 passed in 11.40s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:28:08.536Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/test_stepper.py'; s=open(p).read()\nold='''    page.locator('[data-trace-for]').first.wait_for()\n    page.get_by_test_id(\"charges-panel\").get_by_test_id(\"btn-trace\").first.click()\n'''\nnew='''    tid = page.get_by_test_id(\"judge-rejection\").first.get_attribute(\"data-target-item\")\n    page.locator(f'[data-trace-for=\"{tid}\"]').first.click()\n'''\nassert old in s; open(p,'w').write(s.replace(old,new))\nEOF\nE2E_BASE_URL=http://localhost:7871 .venv/bin/python -m pytest tests/e2e/test_stepper.py tests/unit/test_e2e_contract.py -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T03:28:23.947Z

**tool result**
````
is_internal = False, title = None

    async def wrap_api_call(
        self, cb: Callable[[], Any], is_internal: bool = False, title: str = None
    ) -> Any:
        if self._api_zone.get():
            return await cb()
        task = asyncio.current_task(self._loop)
        parsed_st = _attach_api_call_information(
            getattr(task, "__pw_stack__", None) or _capture_stack_trace(),
            is_internal,
            title,
        )
        self._api_zone.set(parsed_st)
        try:
            return await cb()
        except Exception as error:
>           raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
E           playwright._impl._errors.Error: Locator.wait_for: Error: strict mode violation: get_by_test_id("case-stepper").locator("summary") resolved to 2 elements:
E               1) <summary>…</summary> aka get_by_text("Case checks 7/10 passed")
E               2) <summary>Show the other 17</summary> aka get_by_text("Show the other")
E           
E           Call log:
E             - waiting for get_by_test_id("case-stepper").locator("summary") to be visible

.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py:636: Error
=========================== short test summary info ============================
FAILED tests/e2e/test_stepper.py::test_failed_step_shows_reason_evidence_and_action
FAILED tests/e2e/test_stepper.py::test_steppers_usable_at_390 - playwright._i...
2 failed, 13 passed in 15.05s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:28:26.452Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/test_stepper.py'; s=open(p).read()\ns=s.replace('cs.locator(\"summary\").wait_for(); cs.locator(\"summary\").click()','cs.locator(\"summary\").first.wait_for(); cs.locator(\"summary\").first.click()')\nopen(p,'w').write(s)\nEOF\nE2E_BASE_URL=http://localhost:7871 .venv/bin/python -m pytest tests/e2e/test_stepper.py -q 2>&1 | grep -E \"^E|passed|failed\" | head -20"
}
````

### User / tool · 2026-11-02T03:28:41.889Z

**tool result**
````
______________ test_failed_step_shows_reason_evidence_and_action _______________
    def test_failed_step_shows_reason_evidence_and_action(page, judged_case):
        """A judge objection renders as a failed AI-check step with the fixed-sentence reason and a 'What you need to do' line."""
E       assert 'second AI check said' in 'the second ai check said: disagrees. the second check reads this figure as a billed charge. should_be_charge'
E        +  where 'the second ai check said: disagrees. the second check reads this figure as a billed charge. should_be_charge' = <built-in method lower of str object at 0x1075eb7d0>()
E        +    where <built-in method lower of str object at 0x1075eb7d0> = 'The second AI check said: Disagrees. The second check reads this figure as a billed charge. SHOULD_BE_CHARGE'.lower
E        +      where 'The second AI check said: Disagrees. The second check reads this figure as a billed charge. SHOULD_BE_CHARGE' = inner_text()
E        +        where inner_text = <Locator frame=<Frame name= url='http://localhost:7871/#/case/I4_-NbuIUXB9u2sraSdltQ'> selector='internal:testid=[data-testid="item-stepper"s] >> [data-step-id^="judge"] >> internal:testid=[data-testid="step-judge-reason"s]'>.inner_text
E        +          where <Locator frame=<Frame name= url='http://localhost:7871/#/case/I4_-NbuIUXB9u2sraSdltQ'> selector='internal:testid=[data-testid="item-stepper"s] >> [data-step-id^="judge"] >> internal:testid=[data-testid="step-judge-reason"s]'> = get_by_test_id('step-judge-reason')
E        +            where get_by_test_id = <Locator frame=<Frame name= url='http://localhost:7871/#/case/I4_-NbuIUXB9u2sraSdltQ'> selector='internal:testid=[data-testid="item-stepper"s] >> [data-step-id^="judge"]'>.get_by_test_id
FAILED tests/e2e/test_stepper.py::test_failed_step_shows_reason_evidence_and_action
1 failed, 11 passed in 15.07s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:28:42.655Z

Capitalisation in my test; fix with lowercase match.

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:28:43.797Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/e2e/test_stepper.py'; s=open(p).read()\ns=s.replace('\"second AI check said\" in judge','\"second ai check said\" in judge')\nopen(p,'w').write(s)\nEOF\nE2E_BASE_URL=http://localhost:7871 .venv/bin/python -m pytest tests/e2e tests/unit/test_e2e_contract.py -q -p no:cacheprovider 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T03:30:23.835Z

**tool result**
````
....................................................s...........ss...... [ 80%]
.................                                                        [100%]
86 passed, 3 skipped in 99.67s (0:01:39)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:30:25.827Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/tmp/shots.py && ls artifacts/screenshots | grep -E \"stepper|judge\""
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:30:26.188Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/screenshots/stepper-item-1440.png"
}
````

### User / tool · 2026-11-02T03:30:29.845Z

**tool result**
````
1440 []
390 []
judge-panel-1440.png
judge-panel-390.png
stepper-case-1440.png
stepper-case-390.png
stepper-item-1440.png
stepper-item-390.png
````

### User / tool · 2026-11-02T03:30:29.854Z

**tool result**
````
[image]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:30:32.231Z

**tool call — Bash**
````
{
 "command": "git status --short | head -20; git diff --stat -- app/frontend tests/e2e | tail -12"
}
````

### User / tool · 2026-11-02T03:30:32.384Z

**tool result**
````
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M app/frontend/api.js
 M app/frontend/charges.js
 M app/frontend/flags.js
 M app/frontend/index.html
 M app/frontend/timeline.js
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 app/frontend/api.js      | 3 +++
 app/frontend/charges.js  | 3 ++-
 app/frontend/flags.js    | 1 +
 app/frontend/index.html  | 3 +++
 app/frontend/timeline.js | 8 +++++---
 tests/e2e/conftest.py    | 4 ++++
 6 files changed, 18 insertions(+), 4 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:30:33.144Z

Only my changes. Write memory, then commit and update the board.

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:30:45.853Z

**tool call — Bash**
````
{
 "command": "cat > .claude/agent-memory/frontend/project_stepper_panels.md <<'EOF'\n---\nname: stepper-and-judge-panel\ndescription: T-081/T-082 stepper + AI-check panel: where it lives, how it hooks in, pitfalls\nmetadata:\n  type: project\n---\napp/frontend/stepper.js (ZL.stepper: item, itemSection, openTrace, traceButton, mountCase, goto) + stepper.css (--zs-* tokens over styles.css vars) + judges.js (RV.registerPanel \"judges\"). Data: api.trace / caseTrace / judges (api.js).\nHooks: timeline.js openWhy appends itemSection; renderReview calls mountCase; flags/charges/tray get a btn-trace \"How it was checked\" button.\n**Pitfalls:** never put data-item-id on rows outside real review items (review.js j/k and [data-panel] scans pick them up) -> judge rows use data-target-item, gate rows data-jump-item. Case rail is a details whose open state is kept in a module var; `[data-testid=case-stepper] summary` matches the inner \"Show the other N\" details too (use .first / .zs-case-det > summary).\n**Dev:** own instance needs DATA_DIR=<dir> (not ZLAYT_DB) for a clean DB: `DATA_DIR=artifacts/tmp/fe-data LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local PORT=7871 .venv/bin/python -m app.main`; run e2e with E2E_BASE_URL. Library case_lib06 has 3 judge objections (good for screenshots/tests).\nEOF\necho \"- [Stepper and AI-check panel](project_stepper_panels.md) — T-081/T-082 hooks, data-item-id pitfall, own-instance recipe\" >> .claude/agent-memory/frontend/MEMORY.md\ngit add app/frontend/stepper.js app/frontend/judges.js app/frontend/stepper.css app/frontend/index.html app/frontend/api.js app/frontend/timeline.js app/frontend/flags.js app/frontend/charges.js tests/e2e/test_stepper.py tests/e2e/conftest.py artifacts/screenshots/stepper-case-1440.png artifacts/screenshots/stepper-case-390.png artifacts/screenshots/stepper-item-1440.png artifacts/screenshots/stepper-item-390.png artifacts/screenshots/judge-panel-1440.png artifacts/screenshots/judge-panel-390.png .claude/agent-memory/frontend/project_stepper_panels.md .claude/agent-memory/frontend/MEMORY.md\ngit commit -q -m \"feat(frontend): vertical steppers for every check and gate, case stepper with export-gate blockers, How the AI was checked panel (T-081, T-082, D-042)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/frontend/stepper.js app/frontend/judges.js app/frontend/stepper.css app/frontend/index.html app/frontend/api.js app/frontend/timeline.js app/frontend/flags.js app/frontend/charges.js tests/e2e/test_stepper.py tests/e2e/conftest.py artifacts/screenshots/stepper-case-1440.png artifacts/screenshots/stepper-case-390.png artifacts/screenshots/stepper-item-1440.png artifacts/screenshots/stepper-item-390.png artifacts/screenshots/judge-panel-1440.png artifacts/screenshots/judge-panel-390.png .claude/agent-memory/frontend/project_stepper_panels.md .claude/agent-memory/frontend/MEMORY.md\nSHA=$(git rev-parse --short HEAD); echo $SHA\nB=\"python3 tools/board.py\"\n$B ac T-081 --check 1 --agent frontend --evidence \"tests/e2e/test_stepper.py::test_item_stepper_in_why_panel, test_pending_human_step_says_what_to_do, test_failed_step_shows_reason_evidence_and_action pass; artifacts/screenshots/stepper-item-1440.png, stepper-case-1440.png\"\n$B ac T-081 --check 2 --agent frontend --evidence \"test_case_stepper_order_progress_and_gate, test_gate_blocker_jump_and_update, test_steppers_usable_at_390 pass; full tests/e2e + test_e2e_contract green (86 passed); stepper-*-390.png\"\n$B ac T-082 --check 1 --agent frontend --evidence \"test_judge_panel_is_labelled_and_complete, test_judge_rejection_links_to_item_stepper pass; artifacts/screenshots/judge-panel-1440.png, judge-panel-390.png\"\n$B ac T-082 --check 2 --agent frontend --evidence \"test_judge_panel_is_labelled_and_complete asserts 'AI quality checks' and 'not a verdict'; test_judge_panel_when_nothing_objected\"\nH=\"What changed: stepper.js (item stepper in Why panel + How-it-was-checked button on flags/charges/tray, case rail ingest..export_gate with x/10 passed and gate blockers with jump links), judges.js panel, stepper.css (--zs-* tokens), api.js trace/caseTrace/judges. How verified: tests/e2e/test_stepper.py (12 tests) plus full e2e and test_e2e_contract on a fixture/local instance, 86 passed; screenshots artifacts/screenshots/stepper-*.png judge-panel-*.png at 1440 and 390. Left: mock API has no trace endpoints (panels hide in mock mode); narrative sentences have no stepper entry point; T-060 restyle. Surprise: judge rows must not carry data-item-id (review keyboard flow scans it); ZLAYT_DB is ignored, use DATA_DIR. Commit $SHA.\"\n$B handoff T-081 --agent frontend --text \"$H\"; $B handoff T-082 --agent frontend --text \"$H\"\n$B commit T-081 --sha $SHA --agent frontend; $B commit T-082 --sha $SHA --agent frontend\n$B move T-081 in_review --agent frontend; $B move T-082 in_review --agent frontend\nkill $(lsof -ti :7871)"
}
````

### User / tool · 2026-11-02T03:30:45.992Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: cat > .claude/agent-memory/frontend/project_stepper_panels.md <<'EOF'
---
name: stepper-and-judge-panel
description: T-081/T-082 stepper + AI-check panel: where it lives, how it hooks in, pitfalls
met
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:30:47.301Z

**tool call — Bash**
````
{
 "command": "ls .claude/agent-memory/frontend/; git log --oneline | head -1"
}
````

### User / tool · 2026-11-02T03:30:47.439Z

**tool result**
````
MEMORY.md
project_office3d_phone.md
project_t043_panels.md
3104213 fix(backend): stabilize live 3-run determinism (T-075, R-CO-7)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:30:48.061Z

Nothing ran. Redo in steps.

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:30:52.740Z

**tool call — Bash**
````
{
 "command": "cat > .claude/agent-memory/frontend/project_stepper_panels.md <<'EOF'\n---\nname: stepper-and-judge-panel\ndescription: T-081/T-082 stepper + AI-check panel: where it lives, how it hooks in, pitfalls\nmetadata:\n  type: project\n---\napp/frontend/stepper.js (ZL.stepper: item, itemSection, openTrace, traceButton, mountCase, goto) + stepper.css (--zs-* tokens over styles.css vars) + judges.js (RV.registerPanel \"judges\"). Data: api.trace / caseTrace / judges (api.js).\nHooks: timeline.js openWhy appends itemSection; renderReview calls mountCase; flags/charges/tray get a btn-trace \"How it was checked\" button.\n**Pitfalls:** never put data-item-id on rows outside real review items (review.js j/k and [data-panel] scans pick them up) -> judge rows use data-target-item, gate rows data-jump-item. Case rail is a details whose open state is kept in a module var; `[data-testid=case-stepper] summary` also matches the inner \"Show the other N\" details (use .first or .zs-case-det > summary).\n**Dev:** own instance needs DATA_DIR=<dir> (not ZLAYT_DB) for a clean DB: `DATA_DIR=artifacts/tmp/fe-data LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local PORT=7871 .venv/bin/python -m app.main`; run e2e with E2E_BASE_URL. Library case_lib06 has 3 judge objections (good for screenshots/tests).\nEOF\necho \"- [Stepper and AI-check panel](project_stepper_panels.md) — T-081/T-082 hooks, data-item-id pitfall, own-instance recipe\" >> .claude/agent-memory/frontend/MEMORY.md\ngit add app/frontend/stepper.js app/frontend/judges.js app/frontend/stepper.css app/frontend/index.html app/frontend/api.js app/frontend/timeline.js app/frontend/flags.js app/frontend/charges.js tests/e2e/test_stepper.py tests/e2e/conftest.py artifacts/screenshots/stepper-case-1440.png artifacts/screenshots/stepper-case-390.png artifacts/screenshots/stepper-item-1440.png artifacts/screenshots/stepper-item-390.png artifacts/screenshots/judge-panel-1440.png artifacts/screenshots/judge-panel-390.png .claude/agent-memory/frontend/project_stepper_panels.md .claude/agent-memory/frontend/MEMORY.md; git status --short | grep '^A\\|^M ' | head -20"
}
````

### User / tool · 2026-11-02T03:30:53.014Z

**tool result**
````
M  .claude/agent-memory/frontend/MEMORY.md
A  .claude/agent-memory/frontend/project_stepper_panels.md
M  app/frontend/api.js
M  app/frontend/charges.js
M  app/frontend/flags.js
M  app/frontend/index.html
A  app/frontend/judges.js
A  app/frontend/stepper.css
A  app/frontend/stepper.js
M  app/frontend/timeline.js
A  artifacts/screenshots/judge-panel-1440.png
A  artifacts/screenshots/judge-panel-390.png
A  artifacts/screenshots/stepper-case-1440.png
A  artifacts/screenshots/stepper-case-390.png
A  artifacts/screenshots/stepper-item-1440.png
A  artifacts/screenshots/stepper-item-390.png
M  tests/e2e/conftest.py
A  tests/e2e/test_stepper.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:30:55.654Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"feat(frontend): vertical steppers for every check and gate, case stepper with export-gate blockers, How the AI was checked panel (T-081, T-082, D-042)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/frontend/stepper.js app/frontend/judges.js app/frontend/stepper.css app/frontend/index.html app/frontend/api.js app/frontend/timeline.js app/frontend/flags.js app/frontend/charges.js tests/e2e/test_stepper.py tests/e2e/conftest.py artifacts/screenshots/stepper-case-1440.png artifacts/screenshots/stepper-case-390.png artifacts/screenshots/stepper-item-1440.png artifacts/screenshots/stepper-item-390.png artifacts/screenshots/judge-panel-1440.png artifacts/screenshots/judge-panel-390.png .claude/agent-memory/frontend/project_stepper_panels.md .claude/agent-memory/frontend/MEMORY.md; git rev-parse --short HEAD"
}
````

### User / tool · 2026-11-02T03:30:56.684Z

**tool result**
````
check_secrets: ok (18 file(s) scanned staged)
df5dddd
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:31:01.672Z

**tool call — Bash**
````
{
 "command": "SHA=df5dddd; B=\"python3 tools/board.py\"\n$B ac T-081 --check 1 --agent frontend --evidence \"tests/e2e/test_stepper.py::test_item_stepper_in_why_panel, test_pending_human_step_says_what_to_do, test_failed_step_shows_reason_evidence_and_action pass; artifacts/screenshots/stepper-item-1440.png, stepper-case-1440.png\"\n$B ac T-081 --check 2 --agent frontend --evidence \"test_case_stepper_order_progress_and_gate, test_gate_blocker_jump_and_update, test_steppers_usable_at_390 pass; full tests/e2e + test_e2e_contract green (86 passed); stepper-*-390.png\"\n$B ac T-082 --check 1 --agent frontend --evidence \"test_judge_panel_is_labelled_and_complete, test_judge_rejection_links_to_item_stepper pass; artifacts/screenshots/judge-panel-1440.png, judge-panel-390.png\"\n$B ac T-082 --check 2 --agent frontend --evidence \"test_judge_panel_is_labelled_and_complete asserts 'AI quality checks' and 'not a verdict'; test_judge_panel_when_nothing_objected\"\nH=\"What changed: stepper.js (item stepper in Why panel + How-it-was-checked button on flags/charges/tray, case rail ingest..export_gate with x/10 passed and gate blockers with jump links), judges.js panel, stepper.css (--zs-* tokens), api.js trace/caseTrace/judges. How verified: tests/e2e/test_stepper.py (12 tests) plus full e2e and test_e2e_contract on a fixture/local instance, 86 passed; screenshots artifacts/screenshots/stepper-*.png judge-panel-*.png at 1440 and 390. Left: mock API has no trace endpoints (panels hide in mock mode); narrative sentences have no stepper entry point; T-060 restyle. Surprise: judge rows must not carry data-item-id (review keyboard flow scans it); ZLAYT_DB is ignored, use DATA_DIR. Commit $SHA.\"\n$B handoff T-081 --agent frontend --text \"$H\"; $B handoff T-082 --agent frontend --text \"$H\"\n$B commit T-081 --sha $SHA --agent frontend; $B commit T-082 --sha $SHA --agent frontend\n$B move T-081 in_review --agent frontend; $B move T-082 in_review --agent frontend\nkill $(lsof -ti :7871); $B status --brief | head -3"
}
````

### User / tool · 2026-11-02T03:31:02.573Z

**tool result**
````
AC 1 checked: tests/e2e/test_stepper.py::test_item_stepper_in_why_panel, test_pending_human_step_says_what_to_do, test_failed_step_shows_reason_evidence_and_action pass; artifacts/screenshots/stepper-item-1440.png, stepper-case-1440.png
AC 2 checked: test_case_stepper_order_progress_and_gate, test_gate_blocker_jump_and_update, test_steppers_usable_at_390 pass; full tests/e2e + test_e2e_contract green (86 passed); stepper-*-390.png
AC 1 checked: test_judge_panel_is_labelled_and_complete, test_judge_rejection_links_to_item_stepper pass; artifacts/screenshots/judge-panel-1440.png, judge-panel-390.png
AC 2 checked: test_judge_panel_is_labelled_and_complete asserts 'AI quality checks' and 'not a verdict'; test_judge_panel_when_nothing_objected
handoff written on T-081
handoff written on T-082
T-081: commit df5dddd recorded
T-082: commit df5dddd recorded
T-081: in_progress -> in_review
T-082: in_progress -> in_review
[board] 73.3% done | M0:done M1:done M2:active M3:planned M4:planned M5:planned
[board] ready=14 in_progress=2 in_review=7 changes=0 blocked=0 needs_chris=3 done=63 | inbox_unread=0 stalled=0
[board] → T-081 in_review, no review dispatched — dispatch Tier-1 reviewers: Vertical stepper UI for every check and gate (HITL hand-off)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T03:31:05.563Z

T-081 and T-082 are both in `in_review`, committed as df5dddd. The 12 new stepper tests and the existing e2e suite plus `test_e2e_contract` pass (86 passed, 3 skipped) against my own instance on :7871 (fixture backend, curated set, local mode).
- **T-081:** Each item's Why panel now has the vertical stepper. A "How it was checked" button opens the same stepper from flags, charges and "could not verify" items. The case stepper (ingest through export gate, "x/10 passed") sits above the timeline and lists each export blocker with a jump link.
- **T-082:** The "How the AI was checked" panel is labelled "AI quality checks … not a verdict". It shows counts, models and prompt versions, each rejection with its reason (linking to the item stepper), and code-vs-AI disagreements.
- **Gaps:** In mock API mode the new panels hide because there are no trace endpoints. Narrative sentences have no stepper entry point yet.

Screenshots at 1440 and 390 are in `/Users/arsis/zlayt-pm-project/artifacts/screenshots/` as `stepper-case-*`, `stepper-item-*` and `judge-panel-*`.
