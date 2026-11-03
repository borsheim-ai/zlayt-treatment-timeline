# Architecture map (architect-owned; decisions in `memory/DECISIONS.md`, cross-cutting calls in `memory/ORCHESTRATOR_DECISIONS.md`)

One process, one SQLite file, one set of static files. About 7 hours of build time in total, so every box below earns its place.

```
 browser (vanilla JS)  --JSON-->  FastAPI (app/backend/main.py)  -->  pipeline.py (thread)
                                        |                                |
                                    sqlite3 (app/db)                 code steps  <->  llm/audited.py -> provider.py -> backend
                                                                                              claude-cli | anthropic-api | fixture
```

## Module layout (target; owner in brackets)
```
app/backend/ [backend]
  main.py          routes from memory/contracts/api.md (11 endpoints), static files, error format, demo gate (hash of normalised text), lazy 24 h purge via the one delete_case()
  schemas.py       Pydantic models: API shapes AND LLM output schemas (one source; no prose fields in flag schemas)
  ingest.py        split records, header dates/source labels, `---` separator, dedupe, size limits, PHI-pattern warning
  sentences.py     sentence splitter ( . ; line breaks; abbreviation-safe ), qualifier units
  dates.py         format list; parsed | ambiguous | missing | confirmed; day arithmetic
  amounts.py       currency regex (cents), billing-phrase classification, dedupe, totals (accepted / pending / detected)
  grounding.py     whitespace-normalised match with a normalised->raw index map; absolute offsets; new_tokens(); date equals parse
  confidence.py    compose_state(ladder, context) -> (state, reasons); reason codes
  why.py           one template sentence per reason code
  flag_templates.py  every flag title/explanation (code-rendered)
  gaps.py          gaps from record dates (encounter records only); recompute on confirm_date
  conflicts.py     accident-date rule, provider-name variants (code) + LLM conflict pass
  flags.py         LLM flag pass + lexicon floor + record_warning flags
  injection.py     instruction-like phrase scan (advisory), nonce delimiters, delimiter escaping
  pipeline.py      stages; `python -m app.pipeline <file>`; run/status state; 8 min deadline
  export.py        letter_text + internal_notes_text from accepted items only, deterministic
app/llm/ [backend]
  provider.py      complete(model, system, user, json_schema) -> dict ; complete_with_meta
  audited.py       retry loop (1 + 2 retries, changed conditions), one llm_calls row per attempt, returns (output, call_id)
  backends/        claude_cli.py  anthropic_api.py  fixture.py (+ record mode)
  prompts/         extract_vN.md  judge_faithfulness_vN.md  judge_amount_class_vN.md  conflicts_vN.md  flags_vN.md  judge_conflict_vN.md  judge_flag_vN.md
  lexicon.yaml     [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection
app/db/ [db]       schema.sql, db.py (connection, helpers, purge)
app/frontend/ [frontend]  index.html, app.js (ES modules), styles.css
app/config.py [release]   env: LLM_BACKEND, GENERATOR_MODEL, JUDGE_MODEL, ENABLE_LIVE, PROVIDER_CAP_CONFIRMED, DATA_DIR, limits; injectable now() for every deadline and purge
```

## Pipeline order (stage names match `/status`)
0. `ingest` (sync, code): split, dedupe, header dates and source labels, encounter flag, regex amounts, rule classification, accident-date rule, **gap flags**, injection scan, record_warning flags.
1. `extract`: one generator call per distinct record (concurrency <= 3). 2. `verify` (code). 3. `judge_entries` (J1).
4. `amounts`: J2 on every amount (no LLM classifier). 5. `conflicts`: one cross-record LLM pair pass + J3. 6. `flags`: one LLM pass **per record** + lexicon floor + J4. 7. `finalize`: compose states, order. About 40 calls on the sample; evals default to the `fixture` backend, and the live backend is used only to record fixtures and for the 3-run determinism check.
Gaps are not an LLM stage and never wait for one.

## Invariants every worker must keep (a test exists for each)
- No code path sets `review_status` except the review and confirm_date endpoints. There is no bulk accept.
- Export reads only `accepted`/`edited` items; totals are computed on read, never stored; every letter line carries its verbatim excerpt.
- Gap math reads only code-parsed record dates; dropping or rejecting an LLM entry never changes it.
- Every model call goes through `audited.py`; no direct SDK or subprocess call elsewhere; backends never retry.
- Nothing is silently corrected; a failed check shows a reason code. The model never supplies a date, an amount, a class, a provider or flag wording.
- Record text appears in prompts only inside nonce delimiters, with delimiter-like substrings neutralised in the prompt copy.
- **Never log record text, prompts or responses** (stdout, uvicorn, Space logs). Errors log `call_id` only.
- Untrusted strings reach the DOM with `textContent` only.
- Purge and `DELETE` are one function that deletes from every table by case id (prompts included); SQLite runs with `secure_delete`. Access logging is off (the case token is in the URL path) and responses send `Referrer-Policy: no-referrer`.
- In the public demo build, text is stored only if its normalised hash is in the recorded set.

## Data flow (what stores the text, for the "real build" delta)
| Store / processor | Holds | Notes |
|---|---|---|
| SQLite on container disk | raw text, records, items, `llm_calls` (full prompts and responses), events | deleted by `DELETE` and lazily after 24 h through one function; ephemeral disk; public demo stores only recorded text |
| `tests/fixtures/llm/*.json` (git) | prompts and responses for golden text only | recorder refuses any text not in `evals/golden` |
| Anthropic API (live mode only, local) | prompts and responses | opt-in via `ENABLE_LIVE=1`; spend limit set on the provider key; synthetic data only |
| `claude -p` on Chris's claude.ai login (dev only) | prompts and responses | consumer account; never in the image |
| Hugging Face Space logs | whatever the app prints | hence the no-logging invariant |
A real build would add a business agreement with zero-retention terms for the model provider (while accepting that safety-flagged content may be retained by the vendor beyond zero-retention), a review of Texas HSC §181.154 notice and authorization for electronic disclosure (see `research/phi-and-ai-supervision.md`), encryption at rest, access logging on audit reads, per-user accounts and retention rules. None of that is implemented; the prototype is synthetic-only.

## Build order (suggested, to unblock parallel work)
1. `schemas.py`, `confidence.py`, `grounding.py`, `dates.py`, `amounts.py`, `sentences.py`, `gaps.py` with unit tests first (no LLM).
2. `provider.py` + fixture backend + `audited.py`; record fixtures with the CLI backend from the golden text.
3. `ingest.py`, `pipeline.py` stages 0-3; the sample-case CLI prints entries and gaps.
4. J2 amounts, conflicts, flags, judges, record_warning flags.
5. Routes + export; frontend against the API draft in parallel from step 1.

## Dependencies
`app/llm/lexicon.yaml` v2 (researcher): `flag_type`, `hedge`, `self_report`, `strength`, plus the `accident_date_phrases`, `non_encounter` and `injection` categories. It blocks the gap rule, the accident-date rule and the injection scan, and its golden self-check (recall per `must` flag) gates the claim that the lexicon is a floor (ADR-008.4).

## Cut line
Already cut (D-011, D-020, ADR-015): in-app rate limiter and spend ledger (spend is limited on the provider key), arbitrary-text ingest on the public build, batch accept, charge reclassification and amount edits, the "not a duplicate" split, LLM date pointing, LLM split fallback, bring-your-own-key, `?full=1`, flag title/explanation edits, case list, jsonl audit export, citation toggle, manual add of an entry for a rejected record.
First to go if a milestone exceeds 150% of budget (record in `SCOPE_CUTS.md`): the side-by-side layout (R-ST-1; the record modal R-RV-9 stays), then the synchronous judge re-run on edits (the edit would save as `needs_review` / `JUDGE_UNAVAILABLE`, which is already a defined state). The per-record flag pass is not on the cut line (it is the injection control, ADR-008.3); cheapen it by batching the judge instead.
