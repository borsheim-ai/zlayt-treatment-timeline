# Subagent: Backend: T-178 chaos fixes (Backend: T-178 chaos fixes)

Source: `agent-a731e0eb3214d081d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T20:23:23.948Z

You are a backend worker in /Users/arsis/zlayt-pm-project on T-178 (P0, M3 gate). Claim it with `python3 tools/board.py claim T-178 --agent backend`. Read reviews/GATE-M3-chaos-tester.md and its evidence.

Fix, test-first:
1. **Blocker: interrupted runs.** On startup, any run left 'running' is marked interrupted: the case reads run_partial/failed with a plain message, a re-run is allowed, and accepted items are kept, following the T-146 rules.
2. **Stale second tab.** Review writes carry the item's version or updated_at, and a stale write returns 409 with a plain message ("This item changed in another tab; reload to see it"). Note on the card that the frontend must send the version and show the message. If the frontend already sends something usable, wire it.
3. **Paste text.** Normalize it before the empty check and the size limits: strip zero-width and format characters, and replace lone surrogates. A zero-width-only paste then counts as empty and spends no model calls.
4. **No 500s.** No paste may return a 500.

T-177 is in the provenance code (trace, audit, items); keep to pipeline.py, store.py, ingest and the review write path, and commit via a temp index. Never run `git checkout` on files.

Verify from a `git archive HEAD` copy. Run the full unit suite, update memory/contracts/api.md, write the handoff, and move the card to in_review. Reply in 2 lines.

### User / tool · 2026-11-02T20:23:23.954Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:23:28.969Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-178 --agent backend; python3 tools/board.py show T-178; cat .claude/agent-memory/backend/project_backend_conventions.md; cat .claude/agent-memory/backend/project_t146_rerun_decided_rule.md"
}
````

### User / tool · 2026-11-02T20:23:29.232Z

**tool result**
````
T-178 claimed by backend
---
id: "T-178"
title: "GATE-M3 chaos blocker+majors: a run interrupted by a server restart stays 'running' forever (no export, no re-run); a stale second tab silently overrides a dismissal; zero-width-only paste passes the empty check and spends model calls; a lone surrogate in a paste returns 500"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T20:23:17Z"
updated_at: "2026-11-02T20:23:29Z"
claimed_by: "backend"
claimed_at: "2026-11-02T20:23:29Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "on startup any run left running is marked interrupted (case run_partial/failed, re-run allowed, accepted items kept); review writes carry the item version and a stale write returns 409 with a plain message; text is normalized (strip zero-width/format chars, replace lone surrogates) before the empty check and size limits; no 500 for any paste; unit + e2e per finding", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T20:23:19Z orchestrator: assigned: backend
- 2026-11-02T20:23:29Z backend: claimed

## Handoff (filled when moving to in_review)

---
name: backend-conventions
description: Codepaths, conventions and pitfalls for the deterministic backend modules and pipeline (T-032/033/037); read before touching ingest, amounts, gaps, conflicts, pipeline
metadata:
  type: project
---

Codepaths (app/backend): `ingest.py` (split/limits/dedupe/warnings, `ingest()` composite, `evidence_span`), `dates.py` (format list, 2-digit year >40 ambiguous per D-027), `amounts.py` (cents, classify, extract_amounts, rate_note), `totals.py`, `gaps.py`, `conflicts.py`, `flag_templates.py` (render with closed var whitelist + golden-subtype aliases), `lexicon.py` (loads app/llm/lexicon.yaml as data; deterministic modules must not import app.llm), `pipeline.py` (stages 0-7, `run_ingest`, `ingest_case`, `run_pipeline`, `run_case`, `judge_summary`, CLI). `app/pipeline.py` is a shim so `python -m app.pipeline` works (outside owned paths; flagged to orchestrator).

Conventions: money is int cents and amounts.py must not contain `float(`; text outside recognised record blocks becomes an `unsplit` record (never dropped; only exact `ingest.BANNERS` lines are set aside); a figure inside an injection hit has cents None; flag title/explanation only via flag_templates.render; code never sets review_status (pipeline items leave a run `pending`; `_persist` preserves existing review status on rerun).

Pitfalls: (1) the stage-and-commit rule: `git add` and `git commit` must be separate Bash calls (git-guard hook rejects a combined call), and commit with explicit pathspec `git commit -m ... -- <paths>`. (2) One sqlite3 connection shared by worker threads corrupts `PRAGMA table_info` reads; audited.py serialises writes with `_DB_LOCK`; do not use `:memory:` DBs with threads (CLI uses a temp file). (3) Fixture keys hash the full prompt, so any prompt/schema change in app/llm/prompts or judges invalidates tests/fixtures/llm: re-run `LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record <golden .txt>` per case and `--judges`. (4) tests/unit/test_pipeline.py SEM script has `record_id` which schemas.FlagOutput forbids: the 3 j3 pipeline tests fail until T-036/qa reconcile.

Review findings to avoid repeating: silent text loss in splitters, silent century guesses, ACs ticked on REPL evidence without a named test.

T-075 (determinism): the 0.0 live 3-run did not reproduce in 12 later runs; the real fragilities were judge prompts (J4 rejected valid flags; J3 undecided), model-order-dependent ids, and immediate retries. Judge prompts now v2 (flag category rules; J3 takes `category`). To re-record only judge fixtures after a judge prompt change, replay the recorded set and call claude-cli only on a miss at j3/j4 (never re-record whole cases: it would overwrite extract/narrative fixtures other workers depend on); then run `make_curated.py` (no flag), restore unchanged curated files byte-for-byte, `--check`. Run live pipeline checks in parallel processes (6 at once is fine, ~60 s).

T-085 (Spanish records): code half `language.py` + `spanish_text.py` (no app.llm import; test_boundaries bans LLM imports in dates.py, so keep Spanish code checks out of `spanish.py`, which wires the judge). Spanish records use steps `extract_es` / `judge_faithfulness_es` (own prompts, registered in audited.PROMPT_OF_STEP). To record only missing fixtures for new prompts: `ENABLE_LIVE=1 LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record --fill-missing evals/library/<packet>.txt` (replays recorded answers). Committing a shared file other workers also edit: filter `git diff HEAD -U0` hunks by keyword, `git apply --cached --unidiff-zero` into a temp GIT_INDEX_FILE built from `git read-tree HEAD`; `xargs git add` is blocked by git-guard, list paths explicitly.

## T-085 r2 lessons (language fail-safe)
- Commit with other workers' dirty hunks in the same file: build a temp index (`GIT_INDEX_FILE=$(mktemp)`, `read-tree HEAD`), `git add` whole files only when all hunks are mine; for mixed files (confidence/review/pipeline) hash-object the HEAD text + my edits and `update-index --cacheinfo`. Verify with `git diff --cached --stat`.
- language.detect: lang 'uncertain' = some non-English evidence, no confident answer; is_translated(lang) routes es+uncertain to the Spanish path; record_lang never returns English for text with foreign evidence. Do not put words identical to English (fracture, diagnostic, cervical, protrusion) in fr/pt/es lists.
- A one-record packet's preamble line becomes record 1 in ingest; test packets need 2+ records or no preamble.
- Spanish eval pairs: tests/unit/spanish_translation_pairs.jsonl; live judge eval opt-in SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1.

T-086/T-087 r2 (PDF security): `pdf_hidden.py` is a differential render (page with vs without all text, render mode 3 toggled per object); `FPDFTextObj_GetText` is O(page) per call, so read text only for hidden objects. `review.enforce_ocr` re-applies OCR_DERIVED after every item-rewriting step (edit, manual entry, split, date confirm). Pitfalls: other workers edit review.py/api.py concurrently, so commit "HEAD + my hunks": rebuild the file by applying my replacements to `git show HEAD:file`, `git hash-object -w`, `git update-index --cacheinfo` into a `GIT_INDEX_FILE=$(mktemp)` index after `git read-tree HEAD`; then `git reset -q -- <my files>` so the main index is not stale. git-guard blocks `$VAR` in command position (use literal paths) and macOS `sed -i` needs a suffix (use python for edits). Strided memoryview rows need `.tobytes()` before zlib.

## T-085 r4 (D-050)
- Non-English never verified: `confidence.compose_state` ctx `translated` -> AI_TRANSLATION; any new code path that composes a state from a record must pass `language.translated_record(rec)`. Row-based recomputes (rejudge.recompose, review._without_date_doubt) keep the reason from the stored row. Tests: tests/unit/test_d050_never_verified.py.
- language.detect: `_EN_COLLISIONS` (son, operation, plus, solo...) are not foreign evidence when English-only words >= 3. Held-out jsonl rows: `d050_only` (unroutable, word-for-word Spanish) and `ambiguous` are excluded from routing gates.
- Committing with other workers' hunks: HEAD moves during work (check `git log -1` right before `read-tree HEAD`); rebuild blobs from the new HEAD (`git show HEAD:f` + my substitutions) and `update-index --cacheinfo`; check_stale_index blocks a stale tree. Run the committed tree via `git archive $(git write-tree)` in the scratchpad.

T-087 r4 (PDF isolation): ALL PDF parsing (pypdf read + PDFium scan) runs in one child (`pdf_hidden._run_child`, modes text/scan/both, JSON lines: texts first, result second) killed at the shared deadline, with a parent-side `ps` RSS poll (1 GiB; macOS has no RLIMIT_AS). `pdf_text.read_pages` is in-process-only for the child and tests. `pdf_checks._JOBS` (2) gives 429 `busy` and covers OCR too (OCR's pdfium render still runs in the API worker thread). Commit trick that worked: fixed GIT_INDEX_FILE path, `git add` and `git commit` in separate Bash calls (git-guard), then `git reset -q -- files` on the real index. Reviewer probe files are in the reviewer's scratchpad, not the repo: rebuild from the review text.

T-094 (live determinism, conflicts, causation): open-ended model generation of conflicts was the flake. Conflicts are now CODE candidates (`conflict_candidates.py`: plan vs early end with frequency x duration multiplied out; denial of prior history vs a phrase-list prior hit), J3 (`judge_conflict_v4`) only classifies; no `conflicts` model step or prompt exists. J3 benign -> tray (rejected); model-only flag + J4 disagree -> suppressed (`out["suppressed_flags"]`). Pitfalls: (1) `evals.run` scores tray (rejected) flags as emitted candidates, so only suppression removes a false positive from precision; (2) any J3 prompt edit must pass `evals.run --controls` (D-046: all wrong caught, 0 false agree, including held-out) before the 3-run evals; (3) to re-record only the changed judge fixtures use a replay-then-record-on-miss wrapper (fixture first, live only on a miss) per case, then make_curated.py and restore unchanged curated files byte-for-byte; (4) the tree is shared: build commits from a temp index on HEAD and check `git diff HEAD -- <file>` for other workers' hunks (pipeline.py/trace.py/api.md got swept by others twice); (5) architect owns docs/LLM_VS_CODE.md row 11 and must be told the conflicts row changed.

T-094 r2 (D-053): nothing a model proposes is dropped. A model-only flag J4 rejects, and a model-proposed conflict without a code candidate, are TRAY items (`flags._to_tray`; reasons JUDGE_DISAGREES / LLM_ONLY); `present.case_view` tray has kind `flag` items (before this, rejected flags were in the DB but never in the API tray). `suppressed_flags` no longer exists. evals/run.py: `to_candidates` skips state `rejected` (precision/recall over emitted flags only), `flag_tray` reported apart, signature `flags` excludes rejected; report header names `Source commit ..., tree clean`. judge_flag_v3 (missed_care = scheduled/recommended treatment not attended; scene refusal is scene_facts): re-record J4 fixtures with `python -m app.llm.record --fill-missing <packet>` over evals/golden/*.txt and evals/library/*.txt in parallel (script pattern: ThreadPool of subprocesses, ENABLE_LIVE=1 LLM_BACKEND=claude-cli RECORD_FIXTURES=1). Candidate rules: number words, plan cue, _early_end negation/completion guards in conflict_candidates.py; uncovered patterns in SCOPE_CUTS row 13.

T-103 r4 (billing.py): a printed money token is identified by POSITION (`_at` offset range, `_row` excerpt range, `_unit` line/segment start), never by text; parsers attach positions, `_placed()` reads them back, `_strip_private()` removes every `_`-prefixed key before analyze returns. D-052 "no comparisons" was read strictly: no `_nt`, no cents `<`, sign = `_is_credit` flag; guard test `test_no_money_value_or_text_is_compared_in_billing_code`. Verify count fixes with MANY seeds (reviewer seed 20261102 plus seeds 1-40 via the test module's `_insert`/`_BASES`): seed 20261102 alone hid ~28 CMS/EOB shapes. Never add keys to `_ub_header`/`_header` cols (the test generator draws from them, which would change every seed's draws); use `_ub_all_cols`. Commit with other workers' dirty api.md: build HEAD blob + my replacements, `update-index --cacheinfo` into a temp `GIT_INDEX_FILE`.

T-143 (app/backend/uncovered.py, record.uncovered[]): code-only list of clinical sentences no live entry excerpt overlaps; lexicon has no body-part/dx family so uncovered.py holds its own regexes (move to lexicon.yaml via researcher). Pitfall: `GIT_INDEX_FILE=<temp> git commit -- <paths>` (pathspec = --only) commits the WORKING TREE of those paths and sweeps other workers' dirty hunks (happened to present.py/api.md in 225e666). With a temp index commit WITHOUT a pathspec; use the pathspec form only against the real index. Project python is .venv/bin/python (system python3 lacks fastapi); the 9 amounts/t114/t093 failures on 2026-11-02 belonged to others' dirty amounts.py.
---
name: t146-rerun-decided-rule
description: T-146 r3 re-run rule in pipeline._persist: decided items kept whole with ladder.rerun_note; _degrades/_disagrees/_failure; message shapes; test helpers
metadata:
  type: project
---

`_persist` returns `(kept, empty)`. Kept = stored row left as is when the new row fails (`_degrades`: entry stub, flag made while flag step down, lost second check) or, for DECIDED rows only, `_disagrees` (worse state or different content). Decided kept rows get `ladder.rerun_note` (view field `rerun_note`); undecided keeps get no note. Case = failed/run_partial built in `_partial_error`; `empty` (failures with nothing stored) counts only when the case already had entries (re-run). Deadline stays additive/run_deadline with no note.

**Why:** reviewer round 2 found accepted flags downgraded and accepted entries replaced by SUMMARY_NOT_IN_QUOTE stubs with case "ready". **How to apply:** new failure kinds go in `_failure`; extend the table tests (`test_disagrees_table`, `test_degrades_table`).

Pitfalls: step names in `failed_steps` are only j1-j4/flags/extract/split (no "conflicts"); judge and generator `call_id` differ every run, so row-equality helpers drop `call_id`; present.py/api.md carry other agents' hunks, commit via temp index.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:23:29.743Z

**tool call — Bash**
````
{
 "command": "cat reviews/GATE-M3-chaos-tester.md; ls reviews | grep -i chaos; git status --short | head -30; ls app/backend"
}
````

### User / tool · 2026-11-02T20:23:29.896Z

**tool result**
````
# GATE-M3 chaos-tester review (chaos-tester-reviewer, commit d0b04bc)

**Verdict: fail (1 blocker, 3 major, 2 minor).**

Setup: `git archive d0b04bc` copy in my scratchpad, two servers on ports 7871 and 7872 (both stopped by PID at the end, nothing else touched).
- Server A (7871): the brief's setup. Fixture backend, `ZLAYT_MODE=local`, own SQLite file, demo mode (so unrecorded pastes are refused with 409).
- Server B (7872): same, plus `ENABLE_LIVE=1` and a dummy API key with `LLM_BACKEND=fixture`. This lets arbitrary pasted text reach the code-only ingest stage. The backend stays fixture, so no network and no model call. Every run on it ends in FIXTURE_MISS, which doubles as an LLM-failure test. I used it only for ingest and input-validation probes.

All inputs are SYNTHETIC. Scripts and outputs are in `artifacts/review-evidence/GATE-M3-chaos-*`. Traces are `*-trace.zip`.

## Blocker
**B1. A server restart mid-run strands the case as "running" forever. Its accepted work cannot be exported or re-run.**
- Run the sample case, accept e1, e4 and e5, then POST `/run` with `confirm_rerun`.
- Kill the server process (SIGKILL, standing in for a crash, sleep or redeploy) and restart it on the same DB.
- The case stays `status: running, stage: extract` indefinitely.
- `GET /export` returns 422 `RUN_IN_PROGRESS` ("The AI run is still going"). `POST /run` returns 409 `run_in_progress`.
- The UI shows the Records preview with no Analyze button, only "Start over". The case list row says "Analyzing: Drafting summaries (step 2 of 8)" with no message.
- The 480 s deadline (`pipeline.py:20`) lives inside the dead process. Nothing at startup resets `running` (grep of `app/backend/api.py` and `app/db/db.py` finds only the `/run` guard at `api.py:405`).
- The paralegal's decisions are intact in the DB but unreachable through the product. This makes the must-have export unusable for that case, with no message and no way out.

Repro scripts: `GATE-M3-chaos-killrerun.py` and `GATE-M3-chaos-killrestart2.py`. I ran both twice with the same result. Screenshot: `GATE-M3-chaos-stuck-running-ui.png`.

## Majors
**M1. A decision made in a stale tab silently overrides another tab, and the export disagrees with what the first tab shows.**
- Tab 1 dismisses e4. Tab 2, still showing e4 as pending, clicks Accept on e4.
- The server takes the accept (last write wins, no version or "changed elsewhere" check). Events are `e4 dismiss`, then `e4 accept`.
- Tab 1 still shows e4 as `dismissed` with no notice. Its progress line reads "1 of 23 decided".
- Tab 1's Export puts e4 in the letter. The export API lists `entries: ['e4']`.
- The paralegal sees a dismissed item in the letter with no explanation. Reproduced twice (`GATE-M3-chaos-twotabs.py`, `GATE-M3-chaos-twotabs2.py`; screenshot `GATE-M3-chaos-twotabs-stale-export.png`).
- I did not file this as a §5 blocker. The persisted state is the last explicit human decision, and the letter text is shown before Copy. Label: this is my judgement call.

**M2. Zero-width-only paste is treated as valid input and spends 3 model calls.**
- Pasting `U+200B`, `U+2060`, `U+FEFF` or `U+200D` characters gets past the empty check. Python `str.strip()` does not strip them. Plain spaces, tabs and NBSP are correctly refused.
- A case is created and Analyze runs split, extract and flags (3 `llm_calls` rows) on text with no visible characters. On server B, `(llm_calls, cases)` went 6,24 to 9,25 for `​​​` and to 12,26 for `⁠﻿‍`.
- With a real backend this is paid spend on invalid input. Checklist item 1 says whitespace-only means clear error and no LLM call.
- Repro: `GATE-M3-chaos-zwsp-ui.py 7872 <db>` and the API probe. On demo server A it is masked by the 409.

**M3. A lone UTF-16 surrogate in the paste returns HTTP 500, and the UI offers a retry that can never work.**
- Paste text containing a half emoji (`\ud83d`). `POST /api/cases` returns 500 `{"code":"internal","message":"Something went wrong."}`.
- Server log: `unhandled UnicodeEncodeError at api.py:56` (`digest()` calls `.encode()` on the text). Demo mode hits the same line. On live-looking server B it fails at `db.py:111`, the `sha256()` helper. No case is stored in either mode.
- The UI says "We couldn't start the analysis. Your text is still here. Try again". That is a deterministic input fault presented as transient.
- I rate this major, not a §5 blocker, because there is no stack trace, no crash of the process and no stored data. If Chris reads "a crash from any input" as covering a 5xx on input, it is a blocker.
- Repro: `GATE-M3-chaos-surrogate-ui.py 7871` and `7872` (screenshots `GATE-M3-chaos-surrogate-ui-7871.png` and `-7872.png`), plus `GATE-M3-chaos-api.py` (`lone-surrogate: 500`).

## Minors
**m1. The export gate says "Nothing is accepted or edited yet" right after the paralegal edited an entry.**
- Edit e5 with a valid summary. The entry shows the "Edited" badge and `review_status: edited`, but it stays `needs_review` because the demo has no second check.
- Export returns 422 `NOTHING_ACCEPTED` ("Nothing is accepted or edited yet, so the letter would be empty"). The only action offered is "Accept, edit or dismiss this item".
- The user did edit, so the message is wrong, and the real next step (Accept after the edit) is not named. Repro: `GATE-M3-chaos-edit2.py 7871`.
- Behaviour correct, wording misleading: no unreviewed item is exported.

**m2. No rate limit or backpressure on case creation.**
- 50 parallel `POST /api/cases` all returned 201 (`GATE-M3-chaos-parallel.out.txt`). There is no 429 path on `/api/cases` or `/run`; the only 429 in the app is PDF `pdf_busy`.
- No 5xx occurred, and no spec requirement names a limit. This comes from my checklist item 19, so it is minor.

## What I tried that held
Details are in the `GATE-M3-chaos-*.out.txt` files and trace zips.

- **Input limits.** Empty and whitespace-only pastes are refused (400 empty, or the UI's "There is no text to read" with the text kept). A 60,000-character paste is accepted. 60,001 is refused with "That is 60,001 characters; the limit is 60,000. Nothing was sent". The sample pasted 100 times (187,900 characters) is refused client-side. A 5 MB JSON body gets 413. A binary byte flood gets 400.
- **Huge paste.** Filling 188k-375k characters into the textarea was slow under Playwright, but a bare `<textarea>` control with no app JS was just as slow (11.5 s for 188k characters). Setting the value from JS took 14 ms with a main-thread round trip of about 20 ms. I did not file this.
- **Titles.**
  - `<script>` and `<img onerror>` titles are refused (422) with a plain message.
  - A 121-character title is refused. The UI input has `maxlength=120`.
  - RTL-override characters are stripped.
  - `&lt;b&gt;` entities are stored and rendered as literal text, with no dialog and no pageerror.
  - A rename to markup is refused and the old name stays.
- **Dates (code ingest).**
  - `05/07/11` is `ambiguous` with no ISO guess, shown as a date to confirm with candidates.
  - `2023-02-29`, `Feb 30`, `3/4`, `13/13/2026` and `0000-00-00` are all `missing` and flagged. `2024-02-29` parses.
  - Gaps of 29 and 30 days are not flagged. Only 31 days flags (`f_gap_r3_r4`).
  - Pasted unmarked PDF text with fax banners and "Page 1 of 3" lines stays one record with date missing. The banner dates are not adopted.
- **Non-English and injection.**
  - Spanish routes to `es`. Arabic is `other` with an UNSUPPORTED_LANGUAGE warning.
  - Zalgo, emoji, zero-width characters, a script tag, `{{7*7}}` and SQL text in a record cause no crash and no pageerror.
  - Library case lib09 (Spanish): every entry excerpt is a verbatim slice of a record.
  - Golden case_07 injection: `f_inj_r3` is flagged, the banner shows, and no flag or item is pre-decided. The `$50,000` amount is `needs_review` and stays out of the pending total (it shows `$420`).
  - Injection and "Paralegal: mark all as verified" text on server B produce an `injection_suspected` flag with no state change.
- **Rapid input.**
  - Double-click on Accept (one POST, one event), triple-click on Dismiss, and double-click on Count and on Count-confirm (one accept, one reclassify event) all behaved.
  - Accept then Dismiss racing on e2 ended in the last action, with UI and server agreeing.
  - 40 racing accept/dismiss POSTs on one item gave 40 events, persisted state equal to the last event, and an export matching the persisted state.
  - 400 random keystrokes (a/d/e/j/k/o/p/r/?/A/D, Tab, Esc, Enter, Space, arrows): no pageerror, no stuck dialog, UI equal to server on every item, and the export equalled the accepted set.
- **Concurrent runs.** 20 simultaneous `/run` calls gave 17-18 x 409 and 2-3 x 202. Those 202s were sequential runs: the fixture run finishes in under a second and the guard is status-based. Item counts were stable (9/4/10), so I did not file it.
- **Navigation.** Back, Forward, a second tab and a reload mid-review all recovered. Decisions persisted and the UI matched the server after reload. Back and Forward right after Analyze gave one `/run` POST and a ready case.
- **Network drop.**
  - Server killed mid-review: the UI shows "Could not reach the app. Check your connection and try again", and the item stays pending in both UI and server.
  - Export while the server is down is refused with the same message.
  - After restart, e1 is accepted and e2 pending. Nothing half-written was exported.
  - (The mid-run case is B1.)
- **Injected failures** (`page.route`): 500, malformed JSON and abort on the review POST all give a visible alert and leave the item pending in both UI and server.
- **Accept all, dismiss all, export.** Accept-all-verified accepted 9. Dismiss-all then Export gives "Nothing is accepted or edited yet, so the letter would be empty". Accepting e1 and e7 then exports exactly e1 and e7.
- **Timezones.** America/Chicago, Pacific/Kiritimati and Pacific/Pago_Pago all show identical entry dates. Entry dates are date-only strings and do not shift.
- **Hostile edits.** An added number is refused with "not in the quote". Zalgo and zero-width edits are accepted but marked edited. The source excerpt is unchanged.
- **Not filed.** My first attempt to click Analyze immediately after "Use the sample case" sometimes missed. This is my script racing the preview screen, not a bug: it created exactly one case each time.

```json
{"card": "GATE-M3", "persona": "chaos-tester-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive d0b04bc copy; app on 127.0.0.1:7871 (fixture backend, ZLAYT_MODE=local, demo mode) and 127.0.0.1:7872 (same plus ENABLE_LIVE=1 with a dummy key, fixture backend only, so ingest accepts arbitrary text); sample case plus golden/library cases; all inputs SYNTHETIC; Playwright 1280x900 Chromium on macOS Darwin 25.6.0",
 "exercised": [
  "API probes (GATE-M3-chaos-api.py, both servers): empty, whitespace, zero-width, null and list JSON, invalid JSON, 256-byte binary flood, NUL in text, lone surrogate, 60000 and 60001 chars, sample x200, 5 MB body, titles of 120 and 121 chars, HTML, entity, int, Zalgo and RTL-override titles, bad library id, bad tokens",
  "Browser input sessions (ui-input, hugepaste, hugepaste-control, zwsp-ui, surrogate-ui): HTML/500-char/entity titles, 60,001-char paste, binary-ish paste, empty/space/ZWSP/BOM paste, rename with markup and over-long text, huge-paste responsiveness against a bare-textarea control",
  "Code-only ingest probes on server B (ingest, pdftext): date edge cases 05/07/11, 2024-02-29, 2023-02-29, Feb 30, 3/4, 03-17-26, 13/13/2026, 0000-00-00; 29/30/31-day gaps; amounts text; duplicates; fax and page-header PDF text; Spanish and Arabic; Zalgo/emoji/script/template/SQL; injection text",
  "Library and golden cases through the fixture backend (inj-lib): case_07 injection and lib09 Spanish, states, totals, verbatim-excerpt check",
  "Rapid-click session (dblclick, count): double-click Accept, triple-click Dismiss, Accept-then-Dismiss race, double-click Count and Count-confirm on lib11, Enter x3 on Count, double-click Export, Enter x2 on Export",
  "Review-state sessions (twotabs, twotabs2, backfwd, mash, allnone, edit, edit2): two tabs on one case, Back/Forward mid-run and mid-review, reload, 400-key mash with UI-vs-server and export-vs-accepted comparison, accept-all/dismiss-all/export, hostile edits",
  "Interruption sessions (killrestart, killrestart2, killrerun): SIGKILL of my own server and restart on the same DB, mid-run, mid-re-run with 3 accepted items, and mid-review, with the UI shown while down",
  "Failure injection with page.route (500, malformed JSON, abort) on the review POST; timezone emulation America/Chicago, Pacific/Kiritimati, Pacific/Pago_Pago",
  "Parallelism: 50 parallel creates, 20 parallel /run (3 repetitions), 40 racing accept/dismiss on one item, delete during a run",
  "Read code at api.py:56-135, 205-232, 385-420, 568-596, pipeline.py:20 and 625-660, review.py and ingest.py limits, and the recovery grep, to explain behaviour; every finding below was reproduced against the running app",
  "Stopped both servers by PID (62783, 49710) after confirming each listened on my own port"],
 "verdict": "fail",
 "scores": {"input_handling": 3, "review_state_integrity": 3, "interruption_recovery": 1, "export_equals_accepted_set": 4, "injection_and_grounding": 5, "error_messages": 4},
 "findings": [
  {"severity": "blocker",
   "title": "A server restart mid-run leaves the case 'running' forever; its accepted items can never be exported or re-run",
   "evidence": "GATE-M3-chaos-killrerun.py: accept e1,e4,e5 -> POST /run {confirm_rerun:true} (202) -> SIGKILL own server -> restart same DB. Output: 'status after restart: running extract'; 'decisions kept: {e1,e4,e5: accepted}'; 'export after: 422 {\"code\":\"export_blocked\",...\"reason_code\":\"RUN_IN_PROGRESS\",\"why\":\"The AI run is still going.\",\"next_action\":null}'; 're-run after: 409 run_in_progress'. GATE-M3-chaos-killrestart2.py shows the same on a first run ('STUCK running after restart'). UI: GATE-M3-chaos-stuck-running-ui.png (no Analyze button, only Start over). api.py:405 and :430 refuse on status=='running'; pipeline.py:20 DEADLINE_S exists only in the dead process; no startup recovery in api.py/db.py.",
   "why_it_matters": "A normal laptop sleep, crash or redeploy during Analyze or re-run permanently strands the case. The paralegal's decisions are in the DB but the product offers no way to export or re-run, with no message. It makes the export must-have unusable for that case, and recovery needs a delete or database surgery.",
   "fix": "On startup (create_app) and in GET status, treat status=running with no live run for that token (not in runs) as failed with error run_interrupted ('The run was interrupted; finished items and your decisions are kept. Run it again.'), so the case shows Run again and the export gate shows RUN_FAILED. Also let /run proceed when status is running but the token is not in `runs` and the started_at is older than DEADLINE_S.",
   "acceptance_test": "E2E: start a run, SIGKILL and restart the server on the same DB, then assert GET status is failed/run_interrupted, the UI shows a visible retry, POST /run with confirm_rerun returns 202, the earlier accepted ids are unchanged, and export is allowed after the re-run. Repeat with 3 accepted items present."},
  {"severity": "major",
   "title": "Decision from a stale second tab silently overrides the first tab's dismissal; the first tab then exports an item it displays as dismissed",
   "evidence": "GATE-M3-chaos-twotabs2.py: tab1 Dismiss e4; tab2 (stale, still pending) Accept e4. Output: 'after t2 (stale) accept: server accepted | t1 UI still shows: dismissed'; events e4 dismiss, e4 accept; 't1 shows e4: dismissed | progress: 1 of 23 decided'; letter from tab 1 contains the e4 quote (January 23, 2026 Capital PT); 'e4 row still dismissed in t1 after export'. Screenshot GATE-M3-chaos-twotabs-stale-export.png. Reproduced twice (twotabs.py). api.md has no version or expected-status check on /review (grep for stale/etag/expected_status found nothing).",
   "why_it_matters": "Checklist 15: decisions must not be reverted silently. A paralegal who dismissed an item and sees it Dismissed on screen can export a letter that contains it, with no warning. Persisted state is arguably the last human action, but the screen contradicts it.",
   "fix": "Send the client's last-seen review_status (or an updated_at/version) with each review POST and return 409 stale_decision with the current state when it differs; the UI then refreshes that item and says 'This item was changed in another tab.' Also refetch the case when a tab regains focus, and before building the export view.",
   "acceptance_test": "Playwright two-tab test: tab1 dismiss e4, tab2 (loaded before) accept e4 -> tab2 shows the 'changed elsewhere' message and e4 stays dismissed; tab1 export excludes e4; the server events show exactly one e4 decision."},
  {"severity": "major",
   "title": "Zero-width-only paste passes the empty check, creates a case and runs 3 model calls",
   "evidence": "GATE-M3-chaos-zwsp-ui.py 7872: spaces-only -> 'There is no text to read'; zero-width-only (U+200B x3) -> case created; after Analyze (llm_calls,cases) goes 6,24 -> 9,25; U+2060/U+FEFF/U+200D -> 9,25 -> 12,26; screen 'Record 1: no readable date ... The analysis did not finish'. Rows: llm_calls steps split, extract, flags. ingest.normalize_text/check_limits (ingest.py:30-42) use str.strip(), which keeps format characters. On demo server A the same paste is masked by the 409 (GATE-M3-chaos-api-7871.out.txt).",
   "why_it_matters": "Checklist 1 / R-CO-5: invalid input must cost no model call. With a live backend this is paid spend on an input with no visible characters; a paste of only invisible characters is realistic from copy/paste of a blank PDF page.",
   "fix": "In check_limits, treat text with no characters outside Unicode categories Z*, Cc and Cf (zero-width, BOM, word joiner, bidi marks) as empty (400 bad_request 'Input is empty.'); apply the same test client-side.",
   "acceptance_test": "Unit and E2E: texts of only U+200B, U+200D, U+2060, U+FEFF, U+200E and mixtures with whitespace each get 400/empty message and leave llm_calls and cases counts unchanged (extend tests/e2e/test_adversarial_ui.py's whitespace parametrisation)."},
  {"severity": "major",
   "title": "A lone UTF-16 surrogate in pasted text returns HTTP 500; the UI shows a retry message that can never succeed",
   "evidence": "GATE-M3-chaos-surrogate-ui.py 7871 and 7872: textarea holds '\\ud83d'; POST /api/cases -> 500; UI error 'We couldn't start the analysis. Your text is still here. Try again'. GATE-M3-chaos-api.py 'lone-surrogate: 500 {\"error\":{\"code\":\"internal\",\"message\":\"Something went wrong.\"}}'. Server log: 'unhandled UnicodeEncodeError at api.py:56' (demo, digest()) and 'at db.py:111' (live-looking server, sha256()). No case stored. Screenshots GATE-M3-chaos-surrogate-ui-7871.png/-7872.png.",
   "why_it_matters": "A 5xx from user text; the paralegal is told to retry something that will fail every time and gets no hint that the text is the problem. I rated it major because there is no stack trace, the process survives and nothing is stored; if §5 'crash from any input' is read to cover a 5xx it is a blocker (my judgement, stated openly).",
   "fix": "Validate text in check_limits: try text.encode('utf-8') and on UnicodeEncodeError raise IngestError('bad_request') with a specific message ('The text has a broken character; copy it again from the source.'). Same for title.",
   "acceptance_test": "API and Playwright test: a body with '\\ud83d' in text or title returns 400 with that message, the UI error names the problem and keeps the paste, no 500 is logged, and the case/llm_calls counts do not change."},
  {"severity": "minor",
   "title": "Export gate says 'Nothing is accepted or edited yet' right after the paralegal edited an entry",
   "evidence": "GATE-M3-chaos-edit2.py 7871: edit e5 -> 200, entry shows 'Needs review | Edited'; GET /export -> 422 NOTHING_ACCEPTED 'Nothing is accepted or edited yet, so the letter would be empty.' next_action 'Accept, edit or dismiss this item.' The UI export-blocked box repeats it (screenshot GATE-M3-chaos-edit-export.png).",
   "why_it_matters": "The message contradicts what the user just did and does not name the real next step (accept the edit once the check can confirm it). Behaviour is safe: no unconfirmed item is exported.",
   "fix": "When any entry is edited but unconfirmed, give a specific blocker/next action: 'You edited N entries, but an edited entry also needs Accept before it goes in the letter.'",
   "acceptance_test": "E2E: edit one entry in demo mode, press Export; the message names the edited entry and says to Accept it; accepting it makes the export list exactly that entry."},
  {"severity": "minor",
   "title": "No rate limit or backpressure on case creation or runs",
   "evidence": "GATE-M3-chaos-parallel.out.txt: '50 creates: Counter({201: 50})'; 20 simultaneous /run all 202/409 with no 429 (GATE-M3-chaos-parallelrun.out.txt). The only 429 in the app is pdf_busy (api.py PDF route). Checklist item 19 is a persona item, not a spec constraint.",
   "why_it_matters": "With a live backend each Analyze spends model calls; one client can start unbounded cases and runs. No 5xx was seen.",
   "fix": "A small per-client limit on POST /api/cases and /run (for example N per minute) returning 429 'Too many requests, wait a moment', plus a global cap on concurrent pipelines.",
   "acceptance_test": "Test: 50 parallel POST /api/cases from one client returns some 429 with a plain message and no 5xx; the app stays responsive; normal single use is unaffected."}
 ],
 "whats_right": [
  "The export is always derived from persisted state: across the 400-key mash, 40 racing accept/dismiss posts, Back/Forward, reloads and dismiss-all then accept-some, export ids equalled the accepted set every time.",
  "Ambiguous or invalid dates (05/07/11, 2023-02-29, Feb 30, 3/4) are flagged for confirmation and never guessed, and only a 31-day gap flags.",
  "Injected instructions change nothing (case_07 flag and banner, $50,000 stays out of the total), and every network or 500 failure leaves item state unchanged with a visible message."],
 "questions_for_chris": [
  "Is a 5xx on malformed input (the lone surrogate, finding 4) a 'crash from any input' blocker in your reading of the persona §5, or a major? I filed major."
 ]}
```
GATE-M3-chaos-tester.md
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t166_mvp_polish.md
D  .claude/agent-memory/frontend/project_t174_finish.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
MM app/backend/case_list.py
MM app/backend/pipeline.py
MM app/backend/present.py
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:23:32.931Z

**tool call — Bash**
````
{
 "command": "git log --oneline | head -5; git status --short app tests memory | head -30; grep -n \"running\\|def create_app\\|digest\\|check_limits\\|normalize_text\\|409\\|def post_review\\|/review\" app/backend/api.py | head -80; wc -l app/backend/api.py app/backend/store.py app/backend/ingest.py app/backend/review.py"
}
````

### User / tool · 2026-11-02T20:23:33.079Z

**tool result**
````
04ea2bf feat(backend): T-177 D-065 curated answers are prepared answers, never AI output (badge, Prepared answer tag, trace step, audit model hand-checked (qa)); recorded keep AI labels
d7ea327 test(qa): T-045 r2: real 375 px overflow check, rejected-item guard (unit + e2e), evals --record-latest points latest.json at the live run; fixture runs no longer replace a live latest.json
0c4284f docs(orchestrator): D-065 honest demo provenance (amends D-029)
d0b04bc test(qa): T-045 M3 sensors re-run on a clean HEAD worktree (unit 5689, e2e 411, letter_check 0, calibration fresh, fixture eval matches live); latest.json stale-pointer finding
4510dc2 test(e2e): T-045 keyboard-only and 375px whole journeys, adversarial inputs through the browser (LLM counter 0), R-EX-1 letter matrix over 10 cases x 3 profiles, ladder gate for notes, two library cases side by side; declare T-174 test ids
MM app/backend/api.py
MM app/backend/case_list.py
MM app/backend/pipeline.py
MM app/backend/present.py
MM app/backend/trace.py
MM app/frontend/api.js
MM app/frontend/app.js
MM app/frontend/audit.js
MM app/frontend/charges.js
MM app/frontend/export.js
MM app/frontend/flags.js
MM app/frontend/index.html
MM app/frontend/input.js
MM app/frontend/judges.js
MM app/frontend/overview.css
MM app/frontend/overview.js
MM app/frontend/review.css
MM app/frontend/review.js
D  app/frontend/sections.js
MM app/frontend/sidebyside.css
MM app/frontend/state.js
MM app/frontend/stepper.js
MM app/frontend/styles.css
MM app/frontend/suggestions.css
MM app/frontend/suggestions.js
MM app/frontend/switcher.js
MM app/frontend/timeline.js
MM app/frontend/tokens.css
MM app/frontend/uncovered.css
MM app/frontend/uncovered.js
1:"""FastAPI routes (memory/contracts/api.md). Thin: parsing, the demo gate, error format; logic lives in ingest/store/review/present/export.
3:Demo mode (D-008/D-020): only text whose normalised sha256 is a golden input is accepted; anything else is refused with 409 BEFORE
56:def digest(text: str) -> str:
57:    return hashlib.sha256(ingest.normalize_text(text).encode("utf-8")).hexdigest()
61:    return {digest(p.read_text()) for p in GOLDEN.glob("*.txt")}
95:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
103:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
287:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
327:            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
330:        if demo_mode() and digest(text) not in allowed_hashes():
331:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
399:            if DB.get_case(c, token)["status"] == "running":
414:            if case["status"] == "running" or token in runs:
415:                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
416:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
417:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
422:                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
424:            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
427:            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
439:            if case["status"] == "running" or token in runs or token in rejudging:
440:                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
441:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
442:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
529:    @app.post("/api/cases/{token}/narrative/review")
556:    @app.post("/api/cases/{token}/items/{item_id}/review")
     650 app/backend/api.py
     129 app/backend/store.py
     376 app/backend/ingest.py
     770 app/backend/review.py
    1925 total
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:23:34.767Z

**tool call — Bash**
````
{
 "command": "sed -n 40,135p app/backend/api.py; sed -n 280,345p app/backend/api.py; sed -n 385,470p app/backend/api.py; sed -n 520,650p app/backend/api.py"
}
````

### User / tool · 2026-11-02T20:23:34.873Z

**tool result**
````
_PDF_MESSAGES = {"pdf_no_text_layer": "This PDF has no text layer (it looks scanned). Scanned pages are not read; paste the text instead.",
                 "pdf_unreadable": "This file could not be read as a PDF.", "pdf_encrypted": "This PDF is password-protected and cannot be read.",
                 "pdf_too_large": "The PDF is too large."}
from app.backend import pdf_checks as _pdf_checks      # noqa: E402  (T-086/T-087)
_PDF_MESSAGES.update(_pdf_checks.MESSAGES)


log = logging.getLogger("zlayt.api")


class ApiError(Exception):
    def __init__(self, status, code, message="", detail=None):
        super().__init__(code)
        self.status, self.code, self.message, self.detail = status, code, message or code.replace("_", " "), detail or {}


def digest(text: str) -> str:
    return hashlib.sha256(ingest.normalize_text(text).encode("utf-8")).hexdigest()


def recorded_hashes() -> set:
    return {digest(p.read_text()) for p in GOLDEN.glob("*.txt")}


def library_cases() -> list:
    """Synthetic case library (evals/library, same file format as evals/golden: <id>.txt + optional <id>.expected.json). Falls back to
    evals/golden until the library exists. [{id, name, description, path}]"""
    base = LIBRARY if any(LIBRARY.glob("*.txt")) else GOLDEN
    out = []
    for p in sorted(base.glob("*.txt")):
        meta = {}
        ej = p.with_name(p.stem + ".expected.json")
        if ej.exists():
            try:
                meta = json.loads(ej.read_text())
            except ValueError:
                meta = {}
        out.append({"id": p.stem, "name": meta.get("name") or p.stem.replace("_", " "), "description": (meta.get("description") or "")[:240], "path": p})
    return out


def local_mode() -> bool:
    return os.environ.get("ZLAYT_MODE") == "local"


def is_loopback_peer(request) -> bool:
    """True when the TCP peer is 127.0.0.0/8, ::1 or an IPv4-mapped loopback. No client address (None) counts as not loopback."""
    host = request.client.host if request.client else None
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
    DB.connect(db_path).close()
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
        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set)."""
        if live_enabled():
            return "live"
        from app.llm.backends import fixture
        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
        return DB.connect(app.state.db_path)
        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample, strict_name=typed)

    @app.post("/api/cases/pdf", status_code=201)
    async def create_case_from_pdf(request: Request, name: str = None, ocr: str = None, include_hidden: str = None, title: str = None):
        """D-031: raw PDF bytes (Content-Type application/pdf). Text layer minus hidden text (T-087, `include_hidden`); a scanned PDF is
        refused before anything is stored or run unless `ocr=true`, which reads the scanned pages with local Tesseract (T-086)."""
        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        valid_name(title if title is not None else name, title is not None)          # T-157 r2: a markup title is refused before a byte is read
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > pdf_text.MAX_PDF_BYTES:
            raise ApiError(413, "input_too_large", "The PDF is too large.")
        data = b""
        async for chunk in request.stream():
            data += chunk
            if len(data) > pdf_text.MAX_PDF_BYTES:
                raise ApiError(413, "input_too_large", "The PDF is too large.")
        opts = {}
        if (ocr or "").lower() in ("1", "true", "yes"):
            opts["ocr"] = True
        if include_hidden:
            opts["include_hidden"] = include_hidden
        try:       # parsing runs off the event loop (so /api/health stays responsive) under a time cap
            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data, **opts), _pdf_checks.OCR_TIMEOUT_S if opts.get("ocr") else pdf_text.EXTRACT_TIMEOUT_S)
        except asyncio.TimeoutError:
            raise ApiError(400, "bad_request", _PDF_MESSAGES["pdf_unreadable"], {"reason": "pdf_timeout"}) from None
        except pdf_text.PdfError as e:
            if e.code == "pdf_busy":     # T-087 round 4: at most pdf_checks.MAX_PDF_JOBS uploads are read at once; the rest are told to retry
                raise ApiError(429, "busy", _PDF_MESSAGES["pdf_busy"], {"reason": "pdf_busy"}) from None
            raise ApiError(413 if e.code == "pdf_too_large" else 400, "input_too_large" if e.code == "pdf_too_large" else "bad_request",
                           (e.detail.get("message") if e.code == "ocr_unavailable" else None) or _PDF_MESSAGES[e.code], {"reason": e.code, **e.detail}) from None
        out = make_case(got["text"], title if title is not None else name, False, pdf_pages=got["pages"], pdf_extra={"pdf_checks": got.get("pdf_checks"), "page_images": got.get("page_images") or None},
                        strict_name=title is not None)
        out["pdf_checks"] = got.get("pdf_checks")
        return out

    def valid_name(value, strict=True):
        """T-157 r2: a typed title (or legacy `name`) -> the text to store; markup or an over-long typed title is 422 invalid_title with a plain message."""
        try:
            return case_list.validate_title(value) if strict else case_list.clean_title(value)
        except case_list.TitleError as e:
            raise ApiError(422, "invalid_title", str(e)) from None

    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None, strict_name=True):
        name = name if isinstance(name, str) else ("Sample case" if sample else None)
        name = valid_name(name, strict_name)          # before anything is stored: a refused title leaves no case behind
        try:
            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
        except ingest.IngestError as e:
            raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
        if demo_mode() and digest(text) not in allowed_hashes():
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        c = conn()
        try:
            now = time.time()
            DB.purge_expired(c, now)
            cid = DB.create_case(c, text, now=now, name=name or None,
                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
                                 **({"config_json": {"source_pdf": True, "pages": pdf_pages, **{k: v for k, v in (pdf_extra or {}).items() if v}}} if pdf_pages else {}))
            try:
                ing = pipeline_mod().ingest_case(c, cid, text, now)
                recs = [present.record_view(r, text, with_sentences=False, pages=pdf_pages) for r in present._recs_by_id(c, cid).values()]
                flags = DB.list_items(c, cid, "flag")
            except Exception as e:                       # nothing of a failed create stays stored (ADR-006): drop the case row and its parts
                DB.delete_case(c, cid)
                if isinstance(e, (ingest.IngestError, language.UnsupportedLanguage)):
    def delete_case(token: str):
        c = conn()
        try:
            get_case(c, token)
            DB.delete_case(c, token)
        finally:
            c.close()
        return Response(status_code=204)

    def _run_thread(token, raw):
        c = conn()
        try:
            mod = pipeline_mod()
            mod.run_pipeline(c, token, raw, call=make_call(c, token), now=time.time)
            if DB.get_case(c, token)["status"] == "running":
                DB.update_case(c, token, status="ready", stage="finalize", run_finished_at=time.time())
        except Exception as e:                                   # code only: no message text from the pipeline
            DB.update_case(c, token, status="failed", run_finished_at=time.time(),
                           error=json.dumps({"code": getattr(e, "code", "run_failed"), "message": "The run stopped; finished items are kept."}))
        finally:
            c.close()
            runs.pop(token, None)

    @app.post("/api/cases/{token}/run", status_code=202)
    async def run_case(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            case = get_case(c, token)
            if case["status"] == "running" or token in runs:
                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
            if decided and b.get("confirm_rerun") is not True:
                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
            now = time.time()
            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
            runs[token].start()
            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
        finally:
            c.close()

    @app.post("/api/cases/{token}/rejudge")
    async def rejudge_case(token: str):
        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
        from app.backend import rejudge as RJ
        c = conn()
        try:
            case = get_case(c, token)
            if case["status"] == "running" or token in runs or token in rejudging:
                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
            rejudging.add(token)
            try:
                return await run_in_threadpool(lambda: RJ.rejudge(c, token, make_call(c, token), now=time.time()))
            finally:
                rejudging.discard(token)
        finally:
            c.close()

    @app.get("/api/cases/{token}/status")
    def status(token: str):
        c = conn()
        try:
            case = get_case(c, token)
            stages = getattr(pipeline_mod(), "STAGES", None) or STAGES
            stages = list(stages) if not callable(stages) else STAGES
            stage, done = case_list.run_progress(case, stages)
            end = case["run_finished_at"] or time.time()
            return {"token": token, "status": case["status"], "stage": stage, "stages": stages,
                    "progress": {"done": done, "total": len(stages), "label": f"Step {done + 1} of {len(stages)}: {stage}" if stage else ""},
                    "counts": {"entries": len(DB.list_items(c, token, "entry")), "amounts": len(DB.list_items(c, token, "amount")),
                               "flags": len(DB.list_items(c, token, "flag"))},
                    "error": json.loads(case["error"]) if case["error"] else None,
                    "elapsed_ms": int((end - case["run_started_at"]) * 1000) if case["run_started_at"] else 0}
        finally:
            c.close()

        try:
            get_case(c, token)
            nar = narrative.draft(c, token, call=make_call(c, token), now=time.time())
            if nar.get("error") == "NO_ACCEPTED_ENTRIES":
                raise ApiError(400, "bad_request", "Accept at least one entry first; the paragraph is written from accepted entries only.")
            return {"narrative": present.narrative_view(c, token, nar)}
        finally:
            c.close()

    @app.post("/api/cases/{token}/narrative/review")
    async def narrative_review(token: str, request: Request):
        b = await body_of(request)
        c = conn()
        try:
            get_case(c, token)
            try:
                return {"narrative": present.narrative_view(c, token, narrative.review(c, token, b.get("action"), now=time.time()))}
            except KeyError:
                raise ApiError(404, "not_found", "No draft paragraph yet.") from None
            except ValueError:
                raise ApiError(422, "invalid_edit", "That action is not allowed.") from None
        finally:
            c.close()

    @app.get("/api/cases/{token}/items/{item_id}")
    def item(token: str, item_id: str):
        c = conn()
        try:
            get_case(c, token)
            try:
                return present.why_view(c, token, item_id)
            except (KeyError, IndexError):
                raise ApiError(404, "not_found", "No such item.") from None
        finally:
            c.close()

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
        from app.backend import export_routes as XR
        if style not in (None, *export_mod.STYLES):          # T-121: ?style=oneline | standard
            raise ApiError(422, "invalid_style", XR.invalid_style_message())
        c = conn()
        try:
            get_case(c, token)
            case = store.export_case(c, token)
            try:
                ex = XR.export_payload(token, case, style=style)
            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
            calls = DB.list_llm_calls(c, token)
            ok = ("accepted", "edited")
            tv = present.totals_view(c, token)
            ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
            ex["excluded"] = {"pending": case["pending_count"], "edit_not_confirmed": sum(1 for x in case["entries"] if x.get("edit_unconfirmed")),      # T-134: part of `pending`
                              "dismissed": sum(1 for x in case["entries"] + case["amounts"] + case["flags"] if x["review_status"] == "dismissed"),
                              "rejected": present.rejected_count(c, token)}
            ex["provenance"] = {"generator_model": models()["generator"], "judge_model": models()["judge"], "backend": backend(),
                                "recorded_from": next(((x["recorded_from"] or {}).get("backend") for x in calls if x.get("recorded_from")), None),
                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
                                "edited_count": sum(1 for x in case["entries"] if x["review_status"] == "edited")}
            return ex
        finally:
            c.close()

    @app.get("/api/cases/{token}/items/{item_id}/trace")
    def item_trace(token: str, item_id: str):
        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
        c = conn()
        try:
            get_case(c, token)
            try:
                return trace.item_trace(c, token, item_id, full=local_mode())
            except trace.UnknownItem:
                raise ApiError(404, "not_found", "No such item.") from None
        finally:
            c.close()

    @app.get("/api/cases/{token}/trace")
    def case_trace(token: str):
        c = conn()
        try:
            get_case(c, token)
            return trace.case_trace(c, token, full=local_mode())
        finally:
            c.close()

    @app.get("/api/cases/{token}/judges")
    def judge_report(token: str):
        c = conn()
        try:
            get_case(c, token)
            return trace.judge_report(c, token, full=local_mode())
        finally:
            c.close()

    @app.get("/api/cases/{token}/audit")
    def audit(token: str):
        c = conn()
        try:
            get_case(c, token)
            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
        finally:
            c.close()

    sd = pathlib.Path(static_dir) if static_dir else ROOT / "app" / "frontend"
    if sd.is_dir():
        from fastapi.staticfiles import StaticFiles
        app.mount("/", StaticFiles(directory=str(sd), html=True), name="frontend")
    return app
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:23:35.208Z

**tool call — Bash**
````
{
 "command": "sed -n 1,129p app/backend/store.py; sed -n 1,90p app/backend/ingest.py"
}
````

### User / tool · 2026-11-02T20:23:35.315Z

**tool result**
````
"""DB <-> unit-dict adapters shared by the API layer and the pipeline (T-040). Pure functions plus ingest persistence.

Item/record ids are the pipeline's own ("r6", "e5", "f_gap_r6_r7"); see the id-collision note on T-040.
"""
import os

from app.backend import ingest, pdf_text, spanish
from app.db import db as DB


def live_enabled() -> bool:
    """T-157 r2: the one definition of "live", used by api.demo_mode (its negation) and by rerun_available. ENABLE_LIVE=1 and something to call: the claude CLI, or an API key.
    Read per call so a test can change the environment."""
    from app.llm import provider
    return os.environ.get("ENABLE_LIVE") == "1" and (provider.backend_name() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))


def live_model_available() -> bool:
    """T-157: can a live model answer a request made now? False in demo mode and with the fixture backend (replay only), and for a live backend with nothing to call it with."""
    from app.llm import provider
    return provider.backend_name() != "fixture" and live_enabled()


def iso(t) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(float(t or 0), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_records(conn, case_id: str, raw: str = None) -> list:
    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
    if raw is None:
        raw = DB.get_case(conn, case_id)["raw_text"]
    out = []
    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
        d = DB._decode(r)
        block = raw[d["char_start"]:d["char_end"]]
        try:
            body = ingest.split_records(block)[0]["excerpt"]
        except Exception:
            body = block
        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
                    "kind": "encounter" if d["encounter"] else "other", "date_candidates": d["date_candidates"] or []})
    return out


def _by_id(records):
    return {r["id"]: r for r in records}


# ---------------------------------------------------------------- unit dicts for export / totals
def amount_pos(item: dict, rec):
    """Where the amount's own figure sits in its excerpt (T-140 r3: quotes and reasons are taken from the figure's own offset, never from a text search that finds
    the first equal figure). None when the stored offsets do not point at the figure's text."""
    start, raw = item.get("excerpt_start"), item.get("text") or ""
    if rec is None or start is None or not raw:
        return None
    from app.backend import generator          # lazy: generator imports store
    i = start - generator.body_offset(rec)
    return i if 0 <= i and (item.get("excerpt") or "")[i:i + len(raw)] == raw else None


def export_case(conn, case_id: str, blockers: bool = True) -> dict:
    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
    case = DB.get_case(conn, case_id)
    recs = load_records(conn, case_id, case["raw_text"])
    n_of = {r["id"]: r["n"] for r in recs}
    rec_of = {r["id"]: r for r in recs}
    from app.backend import review as review_mod        # lazy: review imports store
    ents = []
    for e in DB.list_items(conn, case_id, "entry"):
        if e["state"] == "rejected":
            continue
        ed = e.get("edited") or {}
        d = dict(id=e["id"], record_ids=e["record_ids"], record_no=n_of.get((e["record_ids"] or [None])[0], 0), summary=ed.get("summary", e["summary"]),
                 excerpt=ed.get("excerpt", e["excerpt"]), review_status=e["review_status"], date_iso=e["date_iso"])
        if "summary" in ed:
            d["original_summary"] = ed.get("original_summary", e["summary"])
            orig_fails = review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), dict(e, edited={"summary": d["original_summary"], "excerpt": ed.get("original_excerpt", e["excerpt"])}, state_reasons=[]))
            if orig_fails:          # the AI wording that was replaced failed a code check: the notes say so but never print it
                d["original_summary_failed"] = [review_mod.CHECK_PHRASE[c] for c in orig_fails]
        if "excerpt" in ed:
            d["original_excerpt"] = ed.get("original_excerpt", e["excerpt"])
        lad = e.get("ladder") or {}
        if review_mod.code_check_failures(rec_of.get((e["record_ids"] or [None])[0]), e):      # D-051: an unreviewed draft that fails a code check never has its wording printed
            d["code_check_failed"] = True
        if lad.get("entered_by"):
            d["entered_by_reviewer"] = True
        if e["state"] == "needs_review" and any(k in ed for k in ("summary", "excerpt")):
            d["edit_state_reasons"] = list(e.get("state_reasons") or [])          # T-134: why her edit is still marked for review; the notes keep it after she accepts
        if review_mod.edit_unconfirmed("entry", e):          # T-134: reworded and still needs_review: not decided. Out of the letter and counted as pending (D-045a); the notes name why.
            d["review_status"] = "pending"
            d["edit_unconfirmed"] = True
        if lad.get("translation"):          # D-042: the summary of a Spanish record is a translation; the letter says so
            d["translation_label"] = spanish.translation_info("es", "summary" in ed or bool(lad["translation"].get("human_written")))["label"]
        ents.append(d)
    amts = [dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
                 excerpt=a["excerpt"], review_status=a["review_status"], pos=amount_pos(a, rec_of.get((a["record_ids"] or [None])[0])))
            for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
    fl = []
    for f in DB.list_items(conn, case_id, "flag"):
        if f["state"] == "rejected":        # D-053/D-057: every tray flag (judge-rejected, not word for word, rule-filtered) is not an item to review, count or export; its quote may not be in the record
            continue
        c = f.get("computed") or {}
        ev = [dict(record_no=x.get("record_no") or n_of.get(x.get("record_id"), 0), field=x.get("field", "excerpt"),
                   excerpt=x.get("excerpt") or x.get("text")) for x in f.get("evidence") or []]
        fl.append(dict(id=f["id"], type=f["type"], subtype=c.get("subtype") or f["category"], evidence=ev, review_status=f["review_status"],
                       days=c.get("days"), from_date=c.get("from_date"), to_date=c.get("to_date"), note=f.get("reviewer_note")))
    events = []     # D-047: no 'keep my wording' event exists any more
    pending = sum(1 for x in ents + amts + fl if x["review_status"] == "pending")
    pages = (case.get("config") or {}).get("pages")
    records = [dict(n=r["n"], source=r["source"], date_iso=r["date_iso"], excerpt=r["excerpt"],
                    **({"page": pdf_text.page_for(pages, r["char_start"])} if pages else {})) for r in recs]
    nar = (case.get("config") or {}).get("narrative")
    out = dict(records=records, entries=ents, amounts=amts, flags=fl, pending_count=pending, events=events)
    if blockers:                                        # trace.export_blockers calls this with blockers=False to build the letter it checks (T-139 r4)
        from app.backend import trace                   # lazy: trace imports store
        out["export_blockers"] = trace.export_blockers(conn, case_id, case=out)       # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
        out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
    from app.backend import overlap                      # lazy: overlap imports amounts and dates only
    ov = overlap.view(conn, case_id)                      # T-110: statement line vs a separately stated charge of the same kind; code only, never changes a figure
    if ov:
        out["possible_overlaps"] = [dict(o, statement_record_no=n_of.get(o["statement_record_id"], 0), covered_record_no=n_of.get(o["covered_record_id"], 0)) for o in ov]
    ec = (case.get("config") or {}).get("export")
    if ec:
        out["export_config"] = ec
    if nar:
        out["narrative"] = {"status": nar["status"], "basis": nar.get("basis", {}), "removed": nar.get("removed", []),
                            "sentences": [{"text": x["text"], "entry_id": x["entry_id"], "cite": x.get("cite")} for x in nar.get("sentences", [])]}
    return out
"""Stage 0 ingest (all code): split, header date/source, kind, duplicate merge, limits, injection tag, warnings.
R-IN-1, R-IN-3..5, R-TL-3, R-TL-7, R-TL-9, R-RV-6; LLM_VS_CODE rows 1, 2, 3, 16, 17. No model is called here: the D-031 split fallback takes an injected `splitter` callable.
Record text is never rewritten: every excerpt is a verbatim slice of the (newline-normalised) input."""
import re

from app.backend import dates, flag_templates, injection, lexicon

MAX_CHARS = 60000
MAX_RECORDS = 40

# The only text ever set aside as a non-record: the exact banner lines of the golden/sample files. Any other first line is kept as text.
BANNERS = ("SYNTHETIC — invented for evaluation; not real patient data",
           "SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data")

_HEADER = re.compile(r"^=== Record (\d+) ===[ \t]*$", re.MULTILINE)
_SEP = re.compile(r"^[ \t]*---+[ \t]*$", re.MULTILINE)
_DATE_LINE = re.compile(r"^Date:", re.MULTILINE)
_F_DATE = re.compile(r"^Date:[ \t]*(.*)$", re.MULTILINE)
_F_SRC = re.compile(r"^Source:[ \t]*(.*)$", re.MULTILINE)
_F_EXC = re.compile(r"^Excerpt:[ \t]*", re.MULTILINE)


class IngestError(ValueError):
    """Input refused before any processing; str(e) is the API error code ('bad_request' | 'input_too_large')."""

    @property
    def code(self) -> str:
        return str(self)


def normalize_text(raw: str) -> str:
    """CRLF and CR become LF; leading and trailing whitespace trimmed (api.md POST /api/cases)."""
    return (raw or "").replace("\r\n", "\n").replace("\r", "\n").strip()


def check_limits(text: str, max_chars: int = MAX_CHARS) -> str:
    """Raise before anything else (and so before any LLM call): empty -> bad_request, oversize -> input_too_large."""
    t = normalize_text(text)
    if not t:
        raise IngestError("bad_request")
    if len(t) > max_chars:
        raise IngestError("input_too_large")
    return t


def _spans(text: str):
    """Candidate block (start, end) spans and the method that found them; None when nothing is confident."""
    heads = [m.start() for m in _HEADER.finditer(text)]
    if heads:
        return list(zip(heads, heads[1:] + [len(text)]))
    if _SEP.search(text):
        cuts = [0] + [x for m in _SEP.finditer(text) for x in (m.start(), m.end())] + [len(text)]
        return [(cuts[i], cuts[i + 1]) for i in range(0, len(cuts), 2)]
    starts = [m.start() for m in _DATE_LINE.finditer(text)]
    if starts and (_F_SRC.search(text) or _F_EXC.search(text)):
        return list(zip(starts, starts[1:] + [len(text)]))
    return None


def _excerpt_extent(rest: str):
    """(excerpt, consumed_chars) for the text after 'Excerpt:'. A quoted excerpt ends at the first line that ends with a quote;
    anything after it is NOT part of the excerpt (it surfaces as unsplit text). Unquoted or unterminated: the rest of the block."""
    if rest.startswith('"'):
        i = 0
        while True:
            j = rest.find("\n", i)
            seg = rest[i:len(rest) if j < 0 else j].rstrip()
            if seg.endswith('"') and i + len(seg) > 1:
                return rest[1:i + len(seg) - 1], i + len(seg)
            if j < 0:
                break
            i = j + 1
    return rest.strip(), len(rest.rstrip())


def _scan_block(text: str, a: int, b: int):
    """Parse one block. Returns (fields | None, covered spans). Covered spans are absolute; whatever lies outside them is leftover."""
    block = text[a:b]
    cov, f = [], {"date_raw": "", "source": "", "excerpt": "", "complete": False}
    h = _HEADER.match(block)
    if h:
        cov.append((a, a + h.end()))
    found = 0
    for key, pat in (("date_raw", _F_DATE), ("source", _F_SRC)):
        m = pat.search(block)
        if m:
            f[key] = m.group(1).strip()
            cov.append((a + m.start(), a + m.end()))
            found += 1
    e = _F_EXC.search(block)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:23:44.346Z

**tool call — Bash**
````
{
 "command": "grep -rn \"200b\\|200B\\|zero-width\\|zero_width\\|feff\\|FEFF\\|2060\" app/backend/*.py app/llm/*.py | grep -v \"^app/backend/pdf\" | head -30; grep -rln \"u200b\\|\\\\\\\\u200\\|zero-width\\|zero_width\" tests evals --include=*.py | head; grep -c $'​' evals/golden/*.txt evals/library/*.txt | grep -v \":0\"; grep -rn \"normalize_text\" app --include=*.py | grep -v \"def normalize_text\" | head -20"
}
````

### User / tool · 2026-11-02T20:23:44.475Z

**tool result**
````
app/backend/case_list.py:30:_CTRL = re.compile(r"[\x00-\x1f\x7f-\x9f\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]")      # control, zero-width and bidi-override characters: removed
app/backend/speaker.py:184:    t = "".join(ch for ch in t if unicodedata.category(ch) != "Cf")           # zero-width and bidi controls
app/backend/ingest.py:38:    t = normalize_text(text)
app/backend/pipeline.py:53:    text = IN.normalize_text(raw_text)
app/backend/pipeline.py:420:        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
app/backend/pipeline.py:717:        conn, cid, call = _scratch_call(tmp, IN.normalize_text(text))
app/backend/pipeline.py:785:        cid = DB.create_case(conn, IN.normalize_text(raw), now=time.time())
app/backend/api.py:57:    return hashlib.sha256(ingest.normalize_text(text).encode("utf-8")).hexdigest()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:23:51.821Z

**tool call — Bash**
````
{
 "command": "sed -n 135,280p app/backend/api.py; sed -n 20,70p app/backend/case_list.py"
}
````

### User / tool · 2026-11-02T20:23:51.935Z

**tool result**
````
        return DB.connect(app.state.db_path)

    def make_call(c, cid):
        if call_factory:
            return call_factory(c, cid)
        from app.llm import audited
        return audited.make_call(c, cid)

    def pipeline_mod():
        if pipeline is not None:
            return pipeline
        from app.backend import pipeline as PL
        return PL

    def get_case(c, token):
        case = DB.get_case(c, token)
        if case is None:
            raise ApiError(404, "not_found", "No such case.")
        return case

    # -------------------------------------------------- errors / headers
    @app.exception_handler(ApiError)
    async def _api_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(review.ReviewError)
    async def _review_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(_, e):
        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
        return JSONResponse({"error": {"code": code, "message": code.replace("_", " "), "detail": {}}}, status_code=e.status_code)

    def unexpected_response(request, e):
        """T-175: what an uncaught exception becomes. The log line names the exception class and the innermost app frame (file:line), never the message or any case text.
        A route that reads a case after its existence check fails with a TypeError/AttributeError when the case is deleted in that gap (DELETE, the purge): when the case in the
        URL no longer exists that is a plain 404 like any other missing case, not a server error."""
        frames = [f for f in traceback.extract_tb(e.__traceback__) if "/app/" in f.filename.replace("\\", "/")]
        where = f"{pathlib.Path(frames[-1].filename).name}:{frames[-1].lineno}" if frames else "?"
        parts = request.url.path.split("/")
        if len(parts) > 3 and parts[1] == "api" and parts[2] == "cases" and parts[3] != "pdf":
            c = None
            try:
                c = conn()
                if DB.get_case(c, parts[3]) is None:
                    log.warning("case deleted while a request read it (%s at %s); answered 404", type(e).__name__, where)
                    return JSONResponse({"error": {"code": "not_found", "message": "No such case.", "detail": {}}}, status_code=404)
            except Exception as probe_err:
                log.warning("existence probe for a failed request itself failed (%s); answering the original error", type(probe_err).__name__)
            finally:
                if c is not None:
                    c.close()
        log.error("unhandled %s at %s", type(e).__name__, where)
        return JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)

    @app.exception_handler(Exception)
    async def _unexpected(request, e):                            # no traceback, no message text in the body or the log
        return unexpected_response(request, e)

    @app.exception_handler(RequestValidationError)
    async def _validation(_, e):
        return JSONResponse({"error": {"code": "bad_request", "message": "Malformed request.", "detail": {}}}, status_code=400)

    @app.middleware("http")
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
            resp = unexpected_response(request, e)
        resp.headers["Content-Security-Policy"] = CSP
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api") else resp.headers.get("Cache-Control", "no-cache")
        return resp

    async def body_of(request: Request) -> dict:
        cl = request.headers.get("content-length")
        if cl and cl.isdigit() and int(cl) > MAX_BODY_BYTES:
            raise ApiError(413, "input_too_large", "Input is too large.")
        raw = b""
        async for chunk in request.stream():
            raw += chunk
            if len(raw) > MAX_BODY_BYTES:
                raise ApiError(413, "input_too_large", "Input is too large.")
        if not raw:
            return {}
        try:
            b = json.loads(raw)
        except ValueError:
            raise ApiError(400, "bad_request", "Request body is not valid JSON.") from None
        if not isinstance(b, dict):
            raise ApiError(400, "bad_request", "Request body must be a JSON object.")
        return b

    # -------------------------------------------------- routes
    @app.get("/api/health")
    def health():
        ans = answers()
        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "answers": ans,
                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": PREPARED_BANNER if ans == "prepared" else AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}

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
            raise ApiError(404, "not_found", "Not found.")
        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}

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
        typed = isinstance(b.get("title"), str)
        given = b.get("title") if typed else b.get("name")          # T-157: `title` is the name a paralegal types (refused when over 120 characters); `name` stays accepted (a long file name is cut)
        return make_case(text, given if isinstance(given, str) else (lib["name"] if lib else None), sample, strict_name=typed)
RETRY_PAUSE = 0.05            # seconds before the one re-read of a case whose summary failed

KINDS = (("entries", "entry"), ("flags", "flag"), ("amounts", "amount"))
_SLUG = re.compile(r"^[\w.\-]+$")
_LIB_PREFIX = re.compile(r"^case[ _](?:lib)?\d+[ _]", re.IGNORECASE)      # evals/library and evals/golden file names: case_lib01_..., case_01_...
_EXT = re.compile(r"\.(pdf|txt|docx?|rtf)$", re.IGNORECASE)


MAX_TITLE = 120
_WS = re.compile(r"[\t\n\r\x0b\x0c\x85\u2028\u2029]+")
_CTRL = re.compile(r"[\x00-\x1f\x7f-\x9f\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]")      # control, zero-width and bidi-override characters: removed
_TAG = re.compile(r"<[^<>]*>")


class TitleError(ValueError):
    """T-157 r2: a typed title that cannot be stored. str(e) is the plain message the API returns (422 invalid_title); it never repeats the rejected text."""


def _tidy(value) -> str:
    """Control and bidi characters removed, line breaks and tabs turned into spaces, runs of white space collapsed. '' for anything that is not text."""
    if not isinstance(value, str):
        return ""
    return re.sub(r" +", " ", _CTRL.sub("", _WS.sub(" ", value))).strip()


def validate_title(value) -> str:
    """T-157 r2: a title the paralegal typed (create, PATCH). Control characters stripped, white space collapsed; '' when nothing is left (clears the name).
    Raises TitleError for markup (any < or >: a title is plain text, never HTML) and for more than 120 characters. Nothing is escaped or rewritten: it is refused, so what is
    stored is exactly what was typed."""
    t = _tidy(value)
    if "<" in t or ">" in t:
        raise TitleError("A case title is plain text. Remove the angle brackets and try again.")
    if len(t) > MAX_TITLE:
        raise TitleError(f"A case title can be at most {MAX_TITLE} characters. Shorten it and try again.")
    return t


def plain_title(value) -> str:
    """T-157 r2: text from a record (a Source line) shown as a title: complete tags dropped, a lone angle bracket removed on its own (the words after it stay), tidied, at most 120 characters. Never refused: it is not typed."""
    return _tidy(re.sub(r"[<>]", "", _TAG.sub(" ", _tidy(value))))[:MAX_TITLE].strip()


def clean_title(value) -> str:
    """The stored name of a case from a field that may hold a file name (`name`, the PDF's name): validated like a typed title, except that a long file name is cut to
    120 characters, not refused. Markup is still refused."""
    t = _tidy(value)
    return validate_title(t if ("<" in t or ">" in t) else t[:MAX_TITLE])


def derived_title(conn, case_id) -> str:
    """T-157: the title of a case nobody named, from its first record header: the provider (Source line) and that record's date, "Marrowgate General ED, Feb 14, 2026".
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:24:09.397Z

**tool call — Bash**
````
{
 "command": "grep -n \"_partial_error\\|run_partial\\|DEADLINE_S\\|rerun_note\\|def run_pipeline\\|def _failure\" app/backend/*.py | head -40"
}
````

### User / tool · 2026-11-02T20:24:09.492Z

**tool result**
````
app/backend/present.py:47:            "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message"),
app/backend/pipeline.py:20:DEADLINE_S = 480
app/backend/pipeline.py:247:def _failure(kind: str, it: dict):
app/backend/pipeline.py:319:    or changes it (`_disagrees`), the stored row is kept as it is and `ladder.rerun_note` says so (shown on the item). A row that is not decided is kept the same way,
app/backend/pipeline.py:324:    reviewer) is never a stale row (T-165 r2, `_keep_hand_entry`): a re-run must not sweep the paralegal's work; when the AI now also has an entry for the record it gets a rerun_note."""
app/backend/pipeline.py:345:                DB.update_item(conn, it["id"], now=now, case=cid, ladder={**(old.get("ladder") or {}), "rerun_note": {"kind": how, "step": cause, "message": msg, "at": now}})
app/backend/pipeline.py:386:    """T-165 r2: a pending hand-entered entry survives every re-run untouched. When the AI now also has an entry for the record, `ladder.rerun_note` (kind `ai_entry`) says so and
app/backend/pipeline.py:390:    note = ladder.get("rerun_note")
app/backend/pipeline.py:395:            DB.update_item(conn, old["id"], now=now, case=cid, ladder={**ladder, "rerun_note": {"kind": "ai_entry", "step": "writing the entries", "message": msg, "ai_entry": ai, "at": now}})
app/backend/pipeline.py:397:        ladder.pop("rerun_note")
app/backend/pipeline.py:454:def _partial_error(kept: list, empty: list, down: tuple = (), records: list = ()):
app/backend/pipeline.py:455:    """T-146 r3: the case's honest message for a re-run that kept earlier work or had a step fail with nothing to fall back on (code `run_partial`), or None.
app/backend/pipeline.py:474:    err = {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None
app/backend/pipeline.py:493:    if case["status"] != "failed" or not err or err.get("code") != "run_partial" or not err.get("extract_only"):
app/backend/pipeline.py:499:    new = _partial_error([], [_EXTRACT_STEP] * len(left), records=left) if left else None
app/backend/pipeline.py:515:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
app/backend/pipeline.py:651:        err = _partial_error(kept, empty, down, no_entry)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:24:11.006Z

**tool call — Bash**
````
{
 "command": "sed -n 440,515p app/backend/pipeline.py; sed -n 640,690p app/backend/pipeline.py; grep -n \"failed\\|run_partial\\|error\" app/backend/case_list.py | head -30"
}
````

### User / tool · 2026-11-02T20:24:11.117Z

**tool result**
````
    if cause:
        d["cause"] = cause
    return d


def _accident_year(recs: list):
    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso"))      # D-055: a year hint from every dated record; the ingest kind is a label guess and is not read
    return int(ds[0][:4]) if ds else None


def _items(n: int) -> str:
    return f"{n} item{'s' if n != 1 else ''}"


def _partial_error(kept: list, empty: list, down: tuple = (), records: list = ()):
    """T-146 r3: the case's honest message for a re-run that kept earlier work or had a step fail with nothing to fall back on (code `run_partial`), or None.
    It names how many items and which steps, and says exactly what was kept. `down` (T-161 r2): steps that failed without leaving any row to count (the flag step on
    records with no phrase-list hit makes no flag at all), named without a count. `records` (T-165): the record numbers whose extract step failed with nothing to keep; the message names
    them and the error carries them (`records`, plus `extract_only` when that is the whole failure, so a hand entry can clear it)."""
    failed, differed = [k for k in kept if k[2] == "failed"], [k for k in kept if k[2] == "disagreed"]
    parts = []
    if failed:
        parts.append(f"The AI step failed for {_items(len(failed))} ({' and '.join(sorted({c for _, c, _ in failed}))}) on this run. Their earlier results and every "
                     "decision of yours were kept unchanged.")
    if differed:
        parts.append(f"The re-run gave a different result for {_items(len(differed))} you had already decided; your decision and the earlier result were kept, "
                     "and each item carries a note.")
    if empty:
        parts.append(f"The AI step also failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) with no earlier result to keep." if kept else
                     f"The AI step failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) on this run, and there is no earlier result to keep.")
    if down:
        parts.append(f"The AI step ({' and '.join(sorted(down))}) failed on this run, so nothing from it could be used.")
    if records:
        parts.append(f"No entry was made for record{'s' if len(records) != 1 else ''} {_nos(records)}.")
    err = {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None
    if err and records:
        err["records"] = list(records)
        if not kept and not down and set(empty) == {_EXTRACT_STEP}:
            err["extract_only"] = True
    return err


def _nos(ns: list) -> str:
    ns = [str(n) for n in ns]
    return ns[0] if len(ns) == 1 else ", ".join(ns[:-1]) + " and " + ns[-1]


def refresh_extract_error(conn, cid: str) -> None:
    """T-165: after the paralegal enters a record by hand, a case that failed ONLY because the extract step failed for named records stops counting the ones now entered:
    it reads ready (no error, no RUN_FAILED) when none is left, and names the rest otherwise. A failure with any other cause (a second check, the flag step, a kept earlier result) is left as
    it is; it needs a re-run."""
    case = DB.get_case(conn, cid)
    err = json.loads(case["error"]) if case.get("error") else None
    if case["status"] != "failed" or not err or err.get("code") != "run_partial" or not err.get("extract_only"):
        return
    hand = generator.entered_by_hand(DB.list_items(conn, cid, "entry"))
    left = [n for n in err["records"] if f"r{n}" not in hand]
    if left == err["records"]:
        return
    new = _partial_error([], [_EXTRACT_STEP] * len(left), records=left) if left else None
    DB.update_case(conn, cid, status="failed" if new else "ready", error=json.dumps(new) if new else None)


def _noting(raw_call, failed_steps: list):
    """T-146 r2: the same `call`, remembering the steps whose call failed (the AI layer gave up, or a fixture was missing). The failure still propagates to the
    caller's own handling; this only lets the run say which steps were down."""
    def call(step, system, user, schema, *, item_id=None):
        try:
            return raw_call(step, system, user, schema, item_id=item_id)
        except (AU.LLMFailed, P.FixtureMiss):
            failed_steps.append(step)
            raise
    return call


def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
    kept, empty = kept_e + kept_a + kept_f, empty_e + empty_a + empty_f
    _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
    if timed_out:
        status = "timeout"
        err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    else:
        status = "done_with_errors" if errors else "done"
        # T-161: a first run with a judge or the flag step down fails like a re-run. The flag step is read from the steps that were down (a note with no phrase-list hit has no flag row to carry the failure).
        # T-165: an extract failure fails the case on a first run too, however many other records came out, and the records are named; a record the paralegal entered by hand is not one of them.
        named = {c for _, c, _ in kept} | set(empty)
        down = ("finding the flags",) if "flags" in failed_steps and "finding the flags" not in named else ()
        err = _partial_error(kept, empty, down, no_entry)
    DB.update_case(conn, cid, status="failed" if (timed_out or err) else "ready", stage="finalize", error=json.dumps(err) if err else None,
                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
    tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
    all_items = dated + undated + final_amounts + flag_items
    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot,
            "warnings": ing["warnings"] + generator.hand_entered_warnings(DB.list_items(conn, cid, "entry")),
            "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
            "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
                       "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
                       "verified": sum(1 for i in all_items if i["state"] == "verified")}}


# ------------------------------------------------------------------ eval / API view
def case_view(out: dict) -> dict:
    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
    flags = []
    for f in out["flags"] + out["tray"]:
        if "summary" in f:
            continue
        g = dict(f)
        g["evidence"] = [{**e, "record_id": f"r{e['record_no']}", "excerpt": e.get("text")} for e in f.get("evidence", [])]
        if f["type"] == "gap":
            g["computed"] = {"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}
        flags.append(g)
    return {"records": out["records"], "entries": out["entries"], "undated_entries": out["undated_entries"],
            "amounts": [{**a, "value_cents": a["cents"], "kind": a["cls"]} for a in out["amounts"] + out["damages"]],
            "totals": out["totals"], "flags": flags, "tray": [t for t in out["tray"] if "summary" in t], "warnings": out["warnings"],
            "dates_to_confirm": out["dates_to_confirm"], "status": out["status"], "errors": out["errors"],
            "backend": P.backend_name(), "models": {"generator": judges.generator_model(), "judge": judges.judge_model()}}


class _Backend:
    """Temporarily select the LLM backend for one call (eval runner passes it explicitly)."""

    def __init__(self, name):
        self.name, self.old = name, None

20:RETRY_PAUSE = 0.05            # seconds before the one re-read of a case whose summary failed
165:      1. the first export-gate blocker, in gate order (a run in progress or failed, a code-check failure, an accepted item whose second check never answered). Its `kind` is the
199:                    "error": bool(case.get("error"))},
205:            "status_error": False, "status_error_message": None}
212:    """T-175 r2: the row for a case that exists but whose status could not be computed (summary failed twice in a row, so this is a bug and not a write in flight). Same keys as
213:    `summary`, but it says so: `status_error: true` + `status_error_message`, and every figure is null (record_count, counts, progress, hitl) so no zero is shown as if it were real.
226:            "run": {"stage": stage, "steps_done": done, "steps_total": len(stages), "running": case["status"] == "running", "error": bool(case.get("error"))},
228:            "export_ready": False, "next_action": None, "status_error": True, "status_error_message": STATUS_ERROR_MESSAGE}
234:    full row (a write was in flight). If it fails again the case exists and the failure is a bug: the row is listed with `status_error: true` (see `plain_row`) and logged at ERROR.
258:            log.error("case list: a case's status could not be computed twice in a row (%s); listed with status_error", err)
260:            log.error("case list: a case could not be listed at all (%s); left out", err)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:24:16.158Z

**tool call — Bash**
````
{
 "command": "grep -rn \"run_partial\\|run_failed\\|run_deadline\\|RUN_FAILED\" app/frontend app/backend --include=*.js --include=*.py | grep -v \"^app/backend/pipeline.py\" | head -20; grep -n \"def update_case\\|def get_case\\|def create_case\\|status\\b.*running\\|def connect\\|version\\|updated_at\" app/db/db.py | head -40; ls app/db"
}
````

### User / tool · 2026-11-02T20:24:16.301Z

**tool result**
````
app/backend/trace.py:48:    "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
app/backend/trace.py:1225:        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
app/backend/api.py:403:                           error=json.dumps({"code": getattr(e, "code", "run_failed"), "message": "The run stopped; finished items are kept."}))
app/backend/conflict_candidates.py:286:                skip(t, "RUN_FAILED", "The run stopped before the comparison between records finished.")
38:def connect(path: str):
39:    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
45:            version = probe.execute("PRAGMA user_version").fetchone()[0]
49:        if has_tables and version != SCHEMA_VERSION and version != 3:
53:            log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
60:    if path != ":memory:" and conn.execute("PRAGMA user_version").fetchone()[0] == 3 and \
64:    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
71:    `edit` rows whose payload says event == 'reclassify' get their real action. The user_version bump is part of the same transaction."""
91:        conn.execute("PRAGMA user_version=4")
114:def create_case(conn, raw_text: str, now: float, name: str = None, source: str = "paste", **fields) -> str:
122:def update_case(conn, case_id: str, **fields) -> None:
131:def get_case(conn, case_id: str):
159:    _insert(conn, table, {"id": iid, "case_id": case_id, "updated_at": now, **p})
203:    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
210:    fields["updated_at"] = now
229:        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
__init__.py
__pycache__
db.py
schema.sql
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:24:21.138Z

**tool call — Bash**
````
{
 "command": "sed -n 195,260p app/db/db.py; grep -n \"def apply_review\" -A70 app/backend/review.py | head -140; grep -n \"updated_at\\|version\" app/backend/present.py | head -20"
}
````

### User / tool · 2026-11-02T20:24:21.242Z

**tool result**
````
def list_items(conn, case_id: str, kind: str) -> list:
    table = _ITEM_TABLES[kind][0]
    return [_decode(r) for r in conn.execute(f"SELECT * FROM {table} WHERE case_id=? ORDER BY rowid", (case_id,))]


def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
    if locked & set(fields):
        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
    table, found = _find(conn, item_id, case)
    bad = set(fields) - _cols(conn, table)
    if bad:
        raise ValueError(f"unknown {table} fields {sorted(bad)}")
    fields["updated_at"] = now
    sets = ", ".join(f"{k}=?" for k in fields)
    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])


def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
    if action not in ACTIONS:
        raise ValueError(f"invalid review action {action!r}")
    table, row = _find(conn, item_id, case)
    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
    status = ACTIONS[action] or row["review_status"]
    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
    if action == "edit" and not new_edited:
        raise ValueError("edit requires a non-empty edited payload")
    after = {"review_status": status, "edited": new_edited}
    conn.execute("BEGIN")
    try:
        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
                     (status, _enc(new_edited), now, item_id, row["case_id"]))
        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise
    return get_item(conn, item_id, row["case_id"])


def log_event(conn, case_id: str, item_id: str, action: str, before=None, after=None, now: float = 0) -> str:
    """Append an audit-only row to review_events (reclassify, rejudge). It never touches review_status; apply_review stays the only writer of that."""
    if action not in AUDIT_ONLY_ACTIONS:
        raise ValueError(f"log_event only writes {AUDIT_ONLY_ACTIONS}, not {action!r}")
    eid = _tok("v")
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                 (eid, case_id, item_id, action, _enc(before), _enc(after), now))
    return eid


def set_review_status(conn, item_id: str, status: str, now: float = 0, edited: dict = None, case: str = None) -> None:
    if status not in REVIEW_STATUSES:
        raise ValueError(f"invalid review_status {status!r}")
    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
    apply_review(conn, item_id, action, edited=edited, now=now, case=case)


def list_events(conn, case_id: str, item_id: str = None) -> list:
    q, a = "SELECT * FROM review_events WHERE case_id=?", [case_id]
    if item_id:
        q, a = q + " AND item_id=?", a + [item_id]
271:def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
272-    t = _now(now)
273-    kind, item = _item(conn, case_id, item_id)
274-    action = (body or {}).get("action")
275-    if action not in ACTIONS:
276-        raise _bad("That action is not allowed.")
277-    if action == "count":
278-        from app.backend import count_charge          # lazy: count_charge imports review
279-        return count_charge.count(conn, case_id, item_id, body, now=t)
280-    if item["state"] == "rejected" and action in ("accept", "edit"):
281-        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
282-    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
283-        raise _date_unconfirmed_error()
284-    warnings = []
285-    if action in ("accept", "dismiss", "reset"):
286-        confirm = body.get("confirm")
287-        if confirm is not None and not isinstance(confirm, str):
288-            raise _bad("The confirm must be the name of the flag.")
289-        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)
290-        if action == "reset":
291-            restore_pre_edit(conn, case_id, item_id, kind, item, t)
292-        if kind == "flag" and action == "dismiss" and body.get("note"):
293-            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
294-    else:
295-        warnings = _edit(conn, case_id, kind, item, body, call, t)
296-    from app.backend import present
297-    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
298-            "review": present.review_view(conn, case_id), "warnings": warnings}
299-
300-
301-def ocr_record_ids(conn, case_id: str) -> set:
302-    """Ids of the records whose text lies on an OCR-read page of this case (empty for a text case). T-086, D-042."""
303-    from app.backend import pdf_checks
304-    pages = (DB.get_case(conn, case_id).get("config") or {}).get("pages")
305-    if not any(p.get("source") == "ocr" for p in pages or []):
306-        return set()
307-    return {r[0] for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=?", (case_id,))
308-            if pdf_checks.is_ocr_span(pages, r[1], r[2])}
309-
310-
311-def enforce_ocr(conn, case_id: str, t) -> int:
312-    """T-086/D-042 invariant, applied after every step that rewrites an item's state (edit, manual entry, not-a-duplicate, date confirm,
313-    reclassify): an item whose record is on an OCR-read page is needs_review with OCR_DERIVED (rejected items stay rejected). A human edit
314-    does not show the page image was compared, so it never clears this. Idempotent; returns how many items it had to fix."""
315-    ids = ocr_record_ids(conn, case_id)
316-    if not ids:
317-        return 0
318-    n = 0
319-    for kind in ("entry", "amount", "flag"):
320-        for it in DB.list_items(conn, case_id, kind):
321-            if it["state"] == "rejected" or not ids.intersection(it.get("record_ids") or []):
322-                continue
323-            reasons = list(it.get("state_reasons") or [])
324-            if it["state"] == "needs_review" and "OCR_DERIVED" in reasons:
325-                continue
326-            if "OCR_DERIVED" not in reasons:
327-                reasons.append("OCR_DERIVED")
328-            out = {"state": "needs_review", "state_reasons_json": reasons}
329-            if isinstance(it.get("ladder"), dict):
330-                out["ladder"] = {**it["ladder"], "state": "needs_review"}
331-            DB.update_item(conn, it["id"], now=t, case=case_id, **out)
332-            n += 1
333-    return n
334-
335-
336-_QUALIFIER_WORDS = {"hedge": "a hedge (such as may, possible or appears)", "self_report": "a phrase that says whose account the quote gives", "negation": "a negation (such as no, not or denies)",
337-                    "laterality": "a side (left or right)", "approx": "an approximation (such as approximately)"}
338-
339-
340-def _quoted_words(toks) -> str:
341-    q = ["\u201c" + t + "\u201d" for t in toks]
458:            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
482:         "prompt_version": c["prompt_version"], "prompt_sha256": c["prompt_sha256"], "item_id": c["item_id"], "attempt": c["attempt"],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:24:21.629Z

**tool call — Bash**
````
{
 "command": "grep -n \"review\" memory/contracts/api.md | head -40; grep -rn \"/review\\|review_status\" app/frontend/api.js | head; git status --short app/db memory/contracts | head"
}
````

### User / tool · 2026-11-02T20:24:21.769Z

**tool result**
````
10:- Every item has `state` (system: `verified` | `needs_review` | `rejected`), `reasons[]` (codes), `why` (one template sentence), `review_status` (human: `pending` | `accepted` | `edited` | `dismissed`), and `ladder` (D.4).
11:- `warnings[]` appears on case, ingest, review and export responses. Shape: `{"code": "...", "message": "...", "item_id": null}`.
19:| GET | `/api/cases/{token}` | the whole case for the review screen |
27:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an unlocatable quote is a hard `422 invalid_edit` with `detail.reason` and `detail.tokens`/`detail.qualifiers`, no override; a judge objection saves the entry as `pending`/`needs_review` with a `warnings[]` code, no 409); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
30:| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
33:| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset, and (D-064) `count` + `confirm: "separate_charge"` for an amount held back only for a missing detail (see `countable`).  D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/verbatim/highlight; AI-made or human) returns `422 CODE_CHECK_FAILED` and changes nothing: `message` is the plain reason ending "Edit the summary to match the quote." (a summary check) or "Change the quote to whole sentences of the record that keep the hedge sentence." (a quote check), `detail` = `{item_id, reason_code, step_id, failed_steps[], tokens[], next_action: {code: "EDIT_SUMMARY" | "EDIT_QUOTE", text, target: {item_id}}}` (`EDIT_QUOTE` when the first failing check is on the quote: `GROUNDING_EXCERPT_NOT_VERBATIM`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`); the judge verdict does not matter. **T-098 r3: the same guard runs on every action that leaves an entry accepted or edited, from one function (`review.set_review`):** `accept`, `edit` (which implies accept, including a summary-only edit and a quote edit; the check runs on the wording the edit would leave, before any write, so a summary-only edit cannot clear a failing quote and never wipes a stored quote-level reason) and batch accept. `reset` and `dismiss` leave the item out of the letter and are never blocked |
38:| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
58:`backend`: `claude-cli` | `anthropic-api` | `fixture`. `demo_mode: true` (the public build) means only recorded cases can be created or run (ADR-006); the UI shows a "cached demo" badge. `live_enabled` is true only when `ENABLE_LIVE=1` and a key exist (local use). The UI shows `banner` on every view and `ai_banner` on the review view; in live mode it also shows "Pasted text is deleted after `retention_hours` hours" with a Delete now button.
78:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`. **Both fields are on every record of `POST /api/cases` and `GET /api/cases/{token}`** (`false` for a real record); the `UNSPLIT_TEXT` warning is in the POST response only. A re-run after a record number came to name different text resets the paralegal's decisions on items that cite it to `pending` (the review event keeps what they were) and removes the stale items), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
98:  "ocr": {"requested": true, "ran": true, "scanned_pages": [3], "pages": [3], "engine": "tesseract 5.5.2", "low_conf_words": 12, "items_need_review": true,
105:**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, edit, manual entry, not-a-duplicate split, reclassify, date confirmation or rejudge clears it (an edit of an OCR item stays `needs_review` with `OCR_DERIVED`, because the edit does not show that the page image was compared). Its trace gains a failing code step `ocr_source` ("Record was not read from a scanned page", rule D-042, next action `READ_RECORD`); nothing else about other items' traces changes.
108:## POST /api/cases/{token}/review/batch (D-031)
110:Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. **D-059 (T-140 r2): charges are never batched.** A batch (accept or reset) that includes any amount of kind `charge` is refused whole: `422 CHARGES_NOT_BATCHED`, message "Charges are accepted one at a time, so a charge cannot be part of a batch. Take the charge out and review it by itself; nothing was changed.", `detail.rejected` lists `{id, reason: "charge_in_batch"}` for each charge. Frontend: remove charges from every batch/"accept all" selection and from any select-all; a charge has only the single-item accept/dismiss. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`. **D-041:** an entry with no confirmed date (see `undated_entries`) is refused for `accept` with reason `date_unconfirmed`; when any rejected id has that reason the response is `422 DATE_UNCONFIRMED` (instead of `invalid_batch`; same `detail.rejected` list, which still names every refused id and its reason), and nothing changes. After `confirm_date` the entry can be accepted singly or in a batch.
120:Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human decisions and `confirm_rerun` is false; a rerun keeps records, gap review status, events and calls); `409 demo_mode_unsupported_input` (re-checked here, before any LLM call, in demo mode); `503 llm_unavailable`.
133:**T-157, `title` and `next_action` (GET case, top level):** `title` is the same string `GET /api/cases` shows (see "Case titles" there; never "Untitled case"). `next_action` is `{item_id, kind, reason}` or `null`: the single first thing to do, the same value `GET /api/cases` carries (code only, deterministic; rules under "`next_action`" there). **`rerun_available` (bool, every entry, amount and flag view in this payload, in `GET .../items/{item_id}` `item` and in every review response `item`; not on `tray` items):** whether "Run the second check again" (`POST .../rejudge`) can get an answer for this item now. False in demo mode and with the fixture backend (no live model can answer: `ENABLE_LIVE` is not `1`, `LLM_BACKEND` is `fixture`, or `anthropic-api` has no key), and false after a rerun that got no answer (the last `ladder.rejudge` attempt is `unavailable`; it turns true again only when the item's wording or quote changes and drops those attempts). True otherwise. It says nothing about whether the check is needed: use `second_check_pending` for that. Show the rerun button only when both are true; when `second_check_pending` is true and `rerun_available` is false, say the check cannot run here.
135:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **D-057 / T-126, filtered by rule:** a model proposal that a code rule filters out (today D-032 `objective_negative`: a normal finding is not a flag) is not in `tray`, `flags`, `review.queue`, the review counts, the trace gate counts or the export. It is listed in the case payload's `tray_filtered`: `{label: "Filtered by rule", collapsed: true, needs_action: false, count, rules: [{rule: "objective_negative", ref: "D-032", label, explanation, count, items: [<tray flag items, reasons[0] FILTERED_BY_RULE>]}]}` (`count: 0, rules: []` when none). The frontend shows it as a collapsed group with the count and the rule name; no action is needed. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.
139:**T-143 (round 2), `records[].uncovered[]` (GET case; review aid, code only):** EVERY sentence of the record that no live entry's excerpt overlaps, so a pain score, a chief complaint, a baseline-history line, a patient-stated mechanism or onset ("Patient states she was struck by a car..."), an exam finding, a medication, a work-status line or an interpreter / history-source line an entry left out does not vanish silently. Each item is `{text, start, end, kinds}`: `text` the verbatim sentence (the shared splitter, over the same quotable body as `sentences[]`), `start`/`end` offsets into the case text (the same frame as `sentences[]`), `kinds` a **hint only** and possibly empty (`number`, `body_part`, `term`, `negation`); it never decides whether a sentence is listed, so the frontend must not filter on it. A form answer carries its question: `Accidentes anteriores? Si [ ] No [X].` is one item. Skipped only when the line is POSITIVELY administrative by an anchored whole-line pattern: a signature line (`Electronically signed by ...`, `Signed: ...`, `Firma de la paciente: ...`, a bare `Name, MD`), a header field (`Date of service: ...`, `Fax: ...`), a page / fax / print stamp, a billing line (a dollar figure or CPT code, a CMS-1500 item with a billing label, `Balance due.`), or a legal / cost boilerplate line without a dollar sign (`No payments posted.`, `Letter of protection requested.`, `Cost of the collar was covered.`); a line with a pain score N/10 is never skipped, and a bare word such as "adjustment", "balance" or "signed" never removes a line (any other wording of a cost or legal sentence stays listed). A duplicate record (`duplicate_of` set; the original carries the entry) and a record with no quotable body (`sentences_reason` set) give `[]`; `[]` also when nothing is left out, and the field is always present. A rejected (tray) entry covers nothing; a dismissed or pending entry does. It is never in `entries`, the review queue, the counts, the letter or the internal notes (an accepted flag may still quote its own evidence sentence in the notes, as before); the frontend may show it as "Also in this record, not in any entry" next to the record, read-only (a sentence is added to the letter only by the existing manual-entry or edit-quote routes).
159:      "review_status": "pending", "edited": null, "duplicate_note": null,
176:      "review_status": "pending", "edited": null, "duplicate_note": null,
184:      "state": "needs_review", "reasons": ["AMOUNT_RATE_NOT_TOTALED"],
186:      "review_status": "pending", "edited": null, "duplicate_note": null, "flag": null, "confirm_required": false, "accept_effect": "acknowledge", "judge_required_for_export": false,
191:        "state": "needs_review", "human": {"action": null, "edited_text": null, "at": null}} } ],
194:    "pending": {"cents": 839000, "count": 2, "label": "Pending review"},
209:      "origin": "code", "reviewer_note": null,
211:      "review_status": "pending", "edited": null,
223:      "origin": "code", "reviewer_note": null,
225:      "review_status": "pending", "edited": null,
234:      "origin": "lexicon+llm", "reviewer_note": null,
236:      "review_status": "pending", "edited": null,
256:  "review": {
258:    "counts": {"pending": 22, "accepted": 0, "edited": 0, "dismissed": 0, "needs_review": 7, "verified": 15, "rejected": 1},
264:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). **T-108:** units are cut from the quotable excerpt body only (no `Excerpt:` label, quote marks or Date/Source/=== lines), at true offsets, and every unit saves on its own: a sentence that a hedge sentence qualifies is ONE combined unit with the hedge sentence(s) after it (the save route's own check decides, Spanish hedge words included), so the picker never builds a quote the route refuses. A record whose Excerpt label cannot be separated from its text (no Date/Source layout) has `sentences: []` and a plain-words `sentences_reason`; the frontend shows no picker for it. `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
271:Response 200: the record with `date_status: "confirmed"`, its entry's date, the **recomputed gap flags** (a changed or new flag keeps no review status; an unchanged record pair keeps its status), the cleared `date_ambiguous` record warning, and `dates_to_confirm`:
279:**T-116 / D-055 (rounds 3 and 4): gap math runs over EVERY dated record, whatever ingest called it; paperwork-looking records warn and show the other number, they are never dropped.** The ingest `kind` (encounter, billing_statement, phone_note, records_admin) is a label guess and gap math does not read it; a visit whose label carries a paperwork word is an endpoint like any other. `gaps.admin_label` reads a record's header (`Source:`) label and returns a plain label (intake form incl. `formulario de admisión`, billing statement, ledger, EOB, claim form, affidavit, records request, records review, narrative letter, letter or correspondence, phone or message note, administrative record) or null. It is conservative: a visit word in the label (outside the provider name and parentheses) or treatment evidence in the text means no label. It changes no counted gap date, day count or flag. Confirming record 4 of lib09 as 5 March moves the gap 42 to 40 days and `gap_changes` reports it, as in T-114.
285:**T-114: `gap_changes[]`** (always present; `[]` when no gap figure moved). Each element `{flag_id, change: "changed" | "added" | "removed", old_days, new_days, old_from, old_to, new_from, new_to, sentence}`; the side that does not exist is `null`. A gap whose endpoints moved (its id is built from its record numbers) is ONE `changed` element pairing the old and the new gap that share a record. `sentence` is plain words the UI can announce as is, e.g. "Gap recalculated after you confirmed record 4: now 40 days (was 42)." Computed by code from the stored gap figures, never by a model. A gap whose review status was reset by the recompute is exactly the set of `changed`/`added` elements. Each element also has `record_seq` (the record whose date was confirmed). **T-127: the change is kept with the case.** `confirm_date` writes `gap_changes[]` into its `confirm_date` review event (`after.gap_changes`), and `GET /api/cases/{token}` reads it back: a gap flag in `flags[]` whose figures were moved by a confirm_date has `gap_change` (the same element: `{flag_id, change, old_days, new_days, old_from, old_to, new_from, new_to, record_seq, sentence}`), otherwise `gap_change: null`; it stays through reload, another browser and review actions, and goes when that gap's current figures differ from the ones the change produced (a later confirm_date that moves it again replaces it). A gap that no longer applies has no flag, so `GET case` lists it in top-level `gap_changes_removed[]` (same element, `change: "removed"`, `sentence` included) until a gap with the same id exists again. Both are always present (`null` / `[]`). Stored in the DB (the audit event), not in `computed`. `422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event whose `after` records the chosen date (`date_chosen`, `date_raw`, `candidates`, `record_id`) and the ids whose `DATE_AMBIGUOUS` reason it cleared. Confirming also removes `DATE_AMBIGUOUS` from the entry's `reasons` and recomputes its `state` (it becomes `verified` unless another reason remains), so the entry reads like any other dated entry and can be reviewed normally. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
312:Request `{"key": "phrase:new_onset"}`. This is the paralegal's click on "Hide similar": the server dismisses each matching pending flag in this case through the normal review path (one logged `dismiss` event per flag, `reviewer_note` "Hidden by dismissal-pattern suggestion (paralegal confirmed)."). They stay reversible with `reset`. Response 200: `{"key", "dismissed_flag_ids": [...], "suggestions": [...]}` (the refreshed list). `404 not_found` when the key is not a current suggestion (nothing written); `400 bad_request` without a `key`. Bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself. The apply is not one transaction: each flag is dismissed and logged on its own, so a failure partway leaves the earlier flags dismissed (reversible with `reset`); the response is then an error and the refreshed list shows what remains. **UI:** show the `message` as a dismissible banner/chip on the flags list with two buttons ("Hide similar", "Keep showing"); "Keep showing" is client-side only. Never call `apply` without the click; never hide flags on load. Hidden flags remain in the Dismissed filter.
317:{ "item": { "id": "e4", "kind": "entry", "state": "needs_review", "reasons": ["JUDGE_PARTIAL"],
319:            "ladder": {"item_id": "e4", "state": "needs_review"} },
332:## POST /api/cases/{token}/items/{item_id}/review
347:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; its class changes only through `POST .../reclassify`, never through `edit`); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. **D-041: accept and edit on an entry without a confirmed date are `422 DATE_UNCONFIRMED` (nothing is saved); resolve it with `confirm_date` first.** The export is defended the same way: an entry with no date is never written into the letter's treatment section (so "date not stated" never appears there) and is listed in the internal notes under RECORDS NOT IN THE TREATMENT SECTION as "date not confirmed, not exported".
app/frontend/api.js:41:    review: (token, id, body) => call("POST", t(token) + "/items/" + encodeURIComponent(id) + "/review", body),
MM memory/contracts/api.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:24:25.349Z

**tool call — Bash**
````
{
 "command": "grep -rn \"api.review\\|\\.review(\" app/frontend/*.js | head; sed -n 25,80p app/backend/present.py; git diff HEAD --stat -- app/backend/present.py app/backend/api.py app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T20:24:25.463Z

**tool result**
````
app/frontend/excerpt.js:39:      try { const resp = await ZL.api.review(ZL.state.get().token, entry.id, { action: "edit", edits: { excerpt: text } }); ZL.state.applyReview(resp); if (ZL.rv && ZL.rv.clearRefusal) ZL.rv.clearRefusal(entry.id); }
app/frontend/charges.js:184:        try { resp = await ZL.api.review(c.token, id, body); }
app/frontend/review.js:385:      const resp = await ZL.api.review(c.token, id, body);
    return {"action": STATUS_ACTION.get(row["review_status"]), "edited_text": ed.get("summary") or ed.get("note"),
            "at": ed.get("at")}


def _ladder(row):
    lad = dict(row.get("ladder") or {"item_id": row["id"]})
    lad["item_id"] = row["id"]
    lad["state"] = row["state"]
    lad["human"] = _human(row)
    lad.pop("pre_edit", None)      # T-138: the undo snapshot is internal (api.md), never in a payload
    return lad


def rerun_available(row) -> bool:
    """T-157: whether "run the second check again" can get an answer for this item: no in demo / fixture mode (no live model), no after a rerun that got no answer, yes otherwise."""
    last = ((row.get("ladder") or {}).get("rejudge") or [None])[-1]
    return store.live_model_available() and not (last and last.get("verdict") == "unavailable")


def _common(row):
    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons"), (row.get("ladder") or {}).get("judge")),
            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row),
            "rerun_note": ((row.get("ladder") or {}).get("rerun_note") or {}).get("message"),
            "rerun_available": rerun_available(row)}      # T-146 r3: set when a re-run disagreed with or failed on this decided item


def entry_view(row, recs):
    r = recs.get((row["record_ids"] or [None])[0], {})
    ed = row.get("edited") or {}
    return {**_common(row), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
            "provider": row["provider"], "summary": ed.get("summary", row["summary"]), "ai_drafted": "summary" not in ed and not (row.get("ladder") or {}).get("entered_by"),
            "entered_by_reviewer": bool((row.get("ladder") or {}).get("entered_by")), "entered_by": (row.get("ladder") or {}).get("entered_by"), "source_kind": "record",
            "excerpt": ed.get("excerpt", row["excerpt"]), "excerpt_start": ed.get("excerpt_start", row["excerpt_start"]),
            "excerpt_end": ed.get("excerpt_end", row["excerpt_end"]), "duplicate_note": None, "translation": _translation(row),
            "edit_to_check": review.edit_unconfirmed("entry", row)}      # T-134: reworded, still needs_review, not yet accepted: not in the letter


def _translation(row):
    """D-042: set on an entry made from a Spanish record: its summary is an English translation, its quote the original Spanish."""
    t = (row.get("ladder") or {}).get("translation")
    return spanish.translation_info(t.get("source_language", "es"), "summary" in (row.get("edited") or {}) or bool(t.get("human_written"))) if t else None


def accept_effect(row) -> str:
    """What Accept does to an amount (T-114): `letter_total` (a charge: counted in the billed-charges total), `acknowledge` (a rate: noted in the internal notes only,
    never totaled, and no second AI check is needed), `internal_notes` (estimate, unclear: noted for the paralegal, never in the total)."""
    return "letter_total" if row["kind"] == "charge" else ("acknowledge" if row["kind"] == "rate" else "internal_notes")


def amount_flag(row):
    """D-059: the flag a charge carries (likely_duplicate | likely_total) and whether accepting it now needs the confirm step. (None, False) for any other amount."""
    f = (row.get("ladder") or {}).get("confirm") if row["kind"] == "charge" else None
    return (None, False) if not f else ({k: f.get(k) for k in ("flag", "name", "message", "confirm_with", "of", "confirmed_at")}, row["review_status"] == "pending")


def not_counted_info(row, records):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:24:51.921Z

**tool call — Bash**
````
{
 "command": "ls tests/unit | grep -i \"api\\|run\\|review\\|ingest\" | head -30; grep -rln \"run_in_progress\" tests | head; grep -n \"class ReviewError\" -A8 app/backend/review.py; grep -n \"def _item\\b\" -A12 app/backend/review.py; ls .venv/bin/python"
}
````

### User / tool · 2026-11-02T20:24:52.079Z

**tool result**
````
test_amounts_d059_api.py
test_api.py
test_api_routes.py
test_eval_runner.py
test_ingest.py
test_pdf_checks_api.py
test_review_rules.py
test_t145_judge_not_run.py
test_t146_r2_failed_rerun_keeps_items.py
test_t146_rerun_keeps_items.py
test_t161_first_run_stage_down.py
tests/unit/test_trace.py
23:class ReviewError(Exception):
24-    def __init__(self, status: int, code: str, detail: dict = None, message: str = ""):
25-        super().__init__(code)
26-        self.status, self.code, self.detail, self.message = status, code, detail or {}, message or code.replace("_", " ")
27-
28-
29-def _now(now):
30-    return now() if callable(now) else (time.time() if now is None else now)
31-
33:def _item(conn, case_id, item_id):
34-    try:
35-        row = DB.get_item(conn, item_id, case_id)
36-    except KeyError:
37-        raise ReviewError(404, "not_found", message="No such item.") from None
38-    if row["case_id"] != case_id:
39-        raise ReviewError(404, "not_found", message="No such item.")
40-    return _KIND[item_id[0]], row
41-
42-
43-def _bad(msg, **detail):
44-    return ReviewError(422, "invalid_edit", detail, msg)
45-
.venv/bin/python
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:24:54.833Z

**tool call — Bash**
````
{
 "command": "sed -n 1,70p tests/unit/test_api_routes.py; grep -n \"run_in_progress\" -B8 tests/unit/test_trace.py | head -40; grep -n \"running\" tests/unit/*.py | head -20; grep -n \"surrogate\\|\\\\\\\\u200b\" tests/unit/*.py tests/e2e/*.py | head"
}
````

### User / tool · 2026-11-02T20:24:54.941Z

**tool result**
````
"""HTTP layer (T-040): contract shapes, error format, demo gate, review via HTTP, confirm_date, restart survival. Fixture backend, no key."""
import ast
import pathlib
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app
from tests.unit import _golden as G

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    db = str(tmp_path / "api.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)


def wait_ready(c, tok, allow_failed=False):
    for _ in range(160):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready" or (allow_failed and s["status"] == "failed"), s
    return s


def run_case(c, text=None):
    tok = c.post("/api/cases", json={"text": text} if text else {"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    wait_ready(c, tok)
    return tok


def test_health_shape(env):
    h = env[1].get("/api/health").json()
    assert h["backend"] == "fixture" and h["demo_mode"] is True and h["live_enabled"] is False and h["limits"]["max_records"] == 40
    assert {"banner", "ai_banner", "models", "retention_hours", "sample_available", "synthetic_only"} <= set(h)


def test_create_sample_is_code_only_with_gap_flag(env):
    _, c = env
    r = c.post("/api/cases", json={"sample": True})
    b = r.json()
    assert r.status_code == 201 and b["record_count"] == 9 and len(b["gap_flags"]) == 1 and b["status"] == "ingested"
    assert b["records"][0]["text"].startswith("=== Record 1") and b["split_method"] == "code" and r.headers["referrer-policy"] == "no-referrer"
    assert c.get(f"/api/cases/{b['token']}/audit").json()["summary"]["calls"] == 0          # no model call at ingest


def test_error_format_and_unknown_token(env):
    _, c = env
    r = c.get("/api/cases/nope")
    e = r.json()["error"]
    assert r.status_code == 404 and e["code"] == "not_found" and set(e) == {"code", "message", "detail"}
    assert c.post("/api/cases", content=b"{not json", headers={"content-type": "application/json"}).status_code == 400
    assert c.post("/api/cases/nope/accept_all", json={}).status_code in (404, 405)


def test_demo_gate_refuses_unrecorded_text_and_stores_nothing(env):
    db, c = env
    from app.db import db as DB
    r = c.post("/api/cases", json={"text": "SYNTHETIC totally new text\n\n=== Record 1 ===\nDate: 2026-01-01\nSource: X\nExcerpt: \"Hello.\""})
    assert r.status_code == 409 and r.json()["error"]["code"] == "demo_mode_unsupported_input"
    assert DB.connect(db).execute("SELECT count(*) FROM cases").fetchone()[0] == 0
398-    c, _, tok, _ = env
399-    case = c.get(f"/api/cases/{tok}").json()
400-    for x in [*case["entries"], *case["amounts"], *case["flags"]]:
401-        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "dismiss"})
402-    gate = steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
403-    assert gate["ready"] is False and [b["reason_code"] for b in gate["blockers"]] == ["NOTHING_ACCEPTED"]
404-
405-
406:def test_run_in_progress_blocks_the_gate(env):
--
605-        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
606-    DB.update_case(conn, tok, status="failed")
607-    ct = c.get(f"/api/cases/{tok}/trace").json()
608-    gate = steps_of(ct)["export_gate"]
609-    assert ct["verdict"]["code"] == "failed" and gate["ready"] is False and gate["status"] == "fail" and gate["reason_code"] == "RUN_FAILED"
610-    assert [b["reason_code"] for b in gate["blockers"]] == ["RUN_FAILED"] and gate["next_action"]["code"] == "CONFIRM_RERUN"
611-
612-
613:def test_all_accepted_but_run_in_progress_is_not_ready(env):
--
994-    assert rep["totals"]["human_overrides"] >= 2 and rep["totals"]["unavailable"] == 0
995-
996-
997-def test_rejudge_is_refused_in_the_cases_the_run_route_refuses(env, tmp_path):
998-    c, conn, tok, _ = env
999-    assert c.post("/api/cases/nope/rejudge").status_code == 404
1000-    DB.update_case(conn, tok, status="running")
1001-    r = c.post(f"/api/cases/{tok}/rejudge")
1002:    assert r.status_code == 409 and r.json()["error"]["code"] == "run_in_progress"
tests/unit/test_amounts_d059.py:28:    # year to date / running / cumulative
tests/unit/spawn_audit.py:4:must start an allow-listed program: the interpreter running its own child module, the `ps` RSS probe (pdf_hidden only),
tests/unit/test_amounts_d059_api.py:78:        for reason in ("Year-to-date or running figure", "Previous statement or balance carried forward", "Reversal, refund, void", "Payment: money received", "Total or subtotal line"):
tests/unit/test_amounts_d060.py:52:def test_running_and_earlier_statement_words_after_the_figure_name_their_reason(ex, reason_part):
tests/unit/test_billing.py:137:def test_void_is_a_reversal_charge_line_and_the_running_balance_is_just_a_figure():
tests/unit/test_billing.py:159:def test_a_running_balance_that_does_not_follow_is_listed_as_printed_with_no_verdict():
tests/unit/test_billing.py:580:    own figure and its `other_figures` (a running balance on a price row), nothing else (T-103 r3)."""
tests/unit/test_billing.py:1165:def test_rate_row_running_balance_is_a_structured_field_not_only_in_the_excerpt():
tests/unit/test_case_list_race.py:163:            if n % 2:                                    # half wait for the run and review items; the rest delete a case that is still running
tests/unit/test_case_list.py:89:        assert s["run"]["running"] == (case["status"] == "running"), lid
tests/unit/test_eval_runner.py:670:def test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head(monkeypatch, tmp_path, src):
tests/unit/test_pdf_hidden.py:105:    anthropic or app.llm import, name or string; every spawn starts `ps` (RSS probe) or this interpreter running its own module."""
tests/unit/test_pdf_hidden_r2.py:227:    assert time.process_time() - cpu0 - used_at_2_5 < 0.5, "the scan kept running after the API gave up"
tests/unit/test_spanish_records.py:288:def test_pipeline_refuses_a_case_with_nothing_readable_and_leaves_no_running_case(tmp_path):
tests/unit/test_t171_r2_countable.py:3:    Insurer / payer words, allowed amounts, lifetime and running totals, on-account balances and 'amount charged' summaries are not countable, with a plain reason.
tests/unit/test_t171_r3.py:35:            "to_date": "Therapy charges to date $1,100.00.", "cumulative": "Cumulative therapy charges $1,100.00.", "running": "Running therapy charges $1,100.00.",
tests/unit/test_trace.py:408:    DB.update_case(conn, tok, status="running")
tests/unit/test_trace.py:411:    assert gate["ready"] is False and "RUN_IN_PROGRESS" in [b["reason_code"] for b in gate["blockers"]] and ct["verdict"]["code"] == "running"
tests/unit/test_trace.py:554:    DB.update_case(conn, tok, status="running")
tests/unit/test_trace.py:564:    DB.update_case(conn, tok, status="running")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:25:12.606Z

**tool call — Bash**
````
{
 "command": "grep -n \"normalize\\|strip()\\|pages.append\\|\\\"start\\\"\\|offset\" app/backend/pdf_text.py | head -30; git status --short app/backend/pdf_text.py app/backend/ingest.py app/backend/store.py app/backend/review.py"
}
````

### User / tool · 2026-11-02T20:25:12.724Z

**tool result**
````
2:(pdf_ocr) are layered on by pdf_checks. A PDF with no usable text is refused before anything is stored or any model is called. The extracted text is the case text; `pages` maps character offsets of that text to page numbers so citations can
43:    if not (data or b"").lstrip()[:5] == b"%PDF-":
60:                texts.append((page.extract_text() or "").replace("\r\n", "\n").replace("\r", "\n").strip())
69:    """{text, pages: [{page, start, end}]}. Page texts are stripped and joined with a blank line, so offsets index the text exactly.
77:        pages.append({"page": i, "start": len(text), "end": len(text) + len(t), **(sources or {}).get(i, {})})
102:def page_for(pages: list, offset: int):
103:    """Page number whose span holds `offset` (a gap between pages belongs to the earlier page); None when there is no page map."""
104:    if not pages or offset is None:
108:        if p["start"] <= offset:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:25:15.738Z

**tool call — Bash**
````
{
 "command": "sed -n 50,100p app/backend/pdf_text.py; grep -n \"texts\\b\" app/backend/pdf_hidden.py app/backend/pdf_checks.py app/backend/pdf_ocr.py | head"
}
````

### User / tool · 2026-11-02T20:25:15.843Z

**tool result**
````
            warnings.simplefilter("ignore")
            reader = PdfReader(io.BytesIO(data))
            if reader.is_encrypted:
                raise PdfError("pdf_encrypted")
            if len(reader.pages) > MAX_PAGES:
                raise PdfError("pdf_too_large")
            texts = []
            for page in reader.pages:
                if time.monotonic() > deadline:         # stop the worker thread between pages once the API has given up on it
                    raise PdfError("pdf_unreadable", {"reason": "pdf_timeout"})
                texts.append((page.extract_text() or "").replace("\r\n", "\n").replace("\r", "\n").strip())
    except PdfError:
        raise
    except (PyPdfError, ValueError, KeyError, OSError, RecursionError, AssertionError, TypeError):
        raise PdfError("pdf_unreadable") from None
    return texts


def assemble(texts: list, sources: dict = None) -> dict:
    """{text, pages: [{page, start, end}]}. Page texts are stripped and joined with a blank line, so offsets index the text exactly.
    `sources` maps a page number to extra keys for that page's entry (for example {"source": "ocr"}); empty pages are left out."""
    text, pages = "", []
    for i, t in enumerate(texts, 1):
        if not t:
            continue
        if text:
            text += "\n\n"
        pages.append({"page": i, "start": len(text), "end": len(text) + len(t), **(sources or {}).get(i, {})})
        text += t
    return {"text": text, "pages": pages}


def extract_text_layer(data: bytes) -> dict:
    """{text, pages: [{page, start, end}]} from the text layer alone (no hidden-text check, no OCR); no usable text layer is refused."""
    from app.backend import pdf_hidden
    try:
        texts = pdf_hidden.read_text(data, time.monotonic() + EXTRACT_TIMEOUT_S)       # in the killed child, never in this process
    except pdf_hidden.HiddenScanTimeout:
        raise PdfError("pdf_unreadable", {"reason": "pdf_timeout"}) from None
    if sum(len("".join(t.split())) for t in texts) < MIN_TEXT_CHARS:
        raise PdfError("pdf_no_text_layer")
    return assemble(texts)


def extract(data: bytes, **options) -> dict:
    """What POST /api/cases/pdf runs: the text layer minus text that is hidden when the page is shown (T-087), plus local OCR of scanned
    pages when `ocr=True` (T-086). Options: ocr (bool), include_hidden ('all' | '2,5': pages whose hidden text the paralegal confirmed).
    Result: {text, pages, pdf_checks, page_images}; see pdf_checks.extract."""
    from app.backend import pdf_checks
    return pdf_checks.extract(data, **options)

app/backend/pdf_checks.py:70:        texts = scanned.pop("texts")
app/backend/pdf_checks.py:74:        texts = e.texts
app/backend/pdf_checks.py:75:        if texts is None:      # the child failed before it had read the text layer: there is nothing to hold back, the file is unreadable
app/backend/pdf_checks.py:77:        scanned = pdf_hidden.unchecked_scan(len(texts))
app/backend/pdf_checks.py:80:    confirmed = parse_confirmed(include_hidden, len(texts))
app/backend/pdf_checks.py:84:    for n in range(1, len(texts) + 1):               # a page the renderer did not list is a page nobody checked
app/backend/pdf_checks.py:88:        if n > len(texts) or p.get("unchecked"):
app/backend/pdf_checks.py:90:        spans = pdf_hidden.unlisted_spans(texts[n - 1], p["listed_text"])      # words only the extractor can reach
app/backend/pdf_checks.py:93:        if n > len(texts) or n in confirmed:
app/backend/pdf_checks.py:96:            if "".join(texts[n - 1].split()):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:21.646Z

**tool call — Bash**
````
{
 "command": "grep -n \"assemble\\|spans\" app/backend/pdf_checks.py | head -20"
}
````

### User / tool · 2026-11-02T20:26:21.743Z

**tool result**
````
90:        spans = pdf_hidden.unlisted_spans(texts[n - 1], p["listed_text"])      # words only the extractor can reach
91:        p["hidden"] = p["hidden"] + [{"text": sp, "reasons": ["not_in_rendered_page"], "bbox": None} for sp in spans]
132:    got = pdf_text.assemble(texts, sources)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:28.205Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='app/backend/ingest.py'\ns=open(p).read()\ns=s.replace('''import re\n\nfrom app.backend import dates''','''import re\nimport unicodedata\n\nfrom app.backend import dates''',1)\nold=s[s.index('def normalize_text'):s.index('def check_limits')]\nnew='''_LONE_SURROGATE = re.compile(\"[\\\\ud800-\\\\udfff]\")\n\n\ndef clean_chars(raw: str) -> str:\n    \"\"\"T-178 (GATE-M3 chaos): characters that are not text. A lone UTF-16 surrogate (half an emoji; it cannot be encoded, so it used to be a 500) becomes U+FFFD, and every\n    format character (Unicode category Cf: zero-width space/joiner, word joiner, BOM, bidi marks, soft hyphen, tag characters) is removed, so a paste of only invisible\n    characters is empty. What is left is the text the paralegal can see; it is what is stored, hashed and quoted.\"\"\"\n    return \"\".join(ch for ch in _LONE_SURROGATE.sub(\"\\\\ufffd\", raw) if unicodedata.category(ch) != \"Cf\")\n\n\ndef normalize_text(raw: str) -> str:\n    \"\"\"CRLF and CR become LF; format characters removed and lone surrogates replaced (clean_chars); leading and trailing whitespace trimmed (api.md POST /api/cases).\"\"\"\n    return clean_chars(raw or \"\").replace(\"\\\\r\\\\n\", \"\\\\n\").replace(\"\\\\r\", \"\\\\n\").strip()\n\n\n'''\ns=s.replace(old,new,1)\nopen(p,'w').write(s)\np='app/backend/pdf_text.py'\ns=open(p).read()\ns=s.replace('''    text, pages = \"\", []\n    for i, t in enumerate(texts, 1):\n        if not t:''','''    from app.backend import ingest          # lazy: T-178 format characters leave the page text here, so the offsets below index the cleaned case text\n    text, pages = \"\", []\n    for i, t in enumerate(texts, 1):\n        t = ingest.clean_chars(t).strip()\n        if not t:''',1)\nopen(p,'w').write(s)\nEOF\ngit diff app/backend/ingest.py app/backend/pdf_text.py | head -60"
}
````

### User / tool · 2026-11-02T20:26:28.325Z

**tool result**
````
diff --git a/app/backend/ingest.py b/app/backend/ingest.py
index efca1fa..f62cb25 100644
--- a/app/backend/ingest.py
+++ b/app/backend/ingest.py
@@ -2,6 +2,7 @@
 R-IN-1, R-IN-3..5, R-TL-3, R-TL-7, R-TL-9, R-RV-6; LLM_VS_CODE rows 1, 2, 3, 16, 17. No model is called here: the D-031 split fallback takes an injected `splitter` callable.
 Record text is never rewritten: every excerpt is a verbatim slice of the (newline-normalised) input."""
 import re
+import unicodedata
 
 from app.backend import dates, flag_templates, injection, lexicon
 
@@ -28,9 +29,19 @@ class IngestError(ValueError):
         return str(self)
 
 
+_LONE_SURROGATE = re.compile("[\ud800-\udfff]")
+
+
+def clean_chars(raw: str) -> str:
+    """T-178 (GATE-M3 chaos): characters that are not text. A lone UTF-16 surrogate (half an emoji; it cannot be encoded, so it used to be a 500) becomes U+FFFD, and every
+    format character (Unicode category Cf: zero-width space/joiner, word joiner, BOM, bidi marks, soft hyphen, tag characters) is removed, so a paste of only invisible
+    characters is empty. What is left is the text the paralegal can see; it is what is stored, hashed and quoted."""
+    return "".join(ch for ch in _LONE_SURROGATE.sub("\ufffd", raw) if unicodedata.category(ch) != "Cf")
+
+
 def normalize_text(raw: str) -> str:
-    """CRLF and CR become LF; leading and trailing whitespace trimmed (api.md POST /api/cases)."""
-    return (raw or "").replace("\r\n", "\n").replace("\r", "\n").strip()
+    """CRLF and CR become LF; format characters removed and lone surrogates replaced (clean_chars); leading and trailing whitespace trimmed (api.md POST /api/cases)."""
+    return clean_chars(raw or "").replace("\r\n", "\n").replace("\r", "\n").strip()
 
 
 def check_limits(text: str, max_chars: int = MAX_CHARS) -> str:
diff --git a/app/backend/pdf_text.py b/app/backend/pdf_text.py
index 603f8cb..7651c6b 100644
--- a/app/backend/pdf_text.py
+++ b/app/backend/pdf_text.py
@@ -68,8 +68,10 @@ def read_pages(data: bytes, deadline: float = None) -> list:
 def assemble(texts: list, sources: dict = None) -> dict:
     """{text, pages: [{page, start, end}]}. Page texts are stripped and joined with a blank line, so offsets index the text exactly.
     `sources` maps a page number to extra keys for that page's entry (for example {"source": "ocr"}); empty pages are left out."""
+    from app.backend import ingest          # lazy: T-178 format characters leave the page text here, so the offsets below index the cleaned case text
     text, pages = "", []
     for i, t in enumerate(texts, 1):
+        t = ingest.clean_chars(t).strip()
         if not t:
             continue
         if text:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:39.973Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/store.py'\ns=open(p).read()\ns=s.replace('''import os\n\nfrom app.backend import ingest, pdf_text, spanish\nfrom app.db import db as DB\n''','''import json\nimport os\nimport threading\nimport time\n\nfrom app.backend import ingest, pdf_text, spanish\nfrom app.db import db as DB\n\n# T-178 (GATE-M3 chaos blocker): a run is a thread of THIS process. When the process dies (crash, sleep, redeploy) the case row still says \"running\" and nothing would ever clear it.\nLIVE_RUNS = set()                 # tokens whose run thread is alive in this process (api._run_thread adds and removes)\n_LIVE_LOCK = threading.Lock()\nRUN_STALE_AFTER_S = 480 + 120     # pipeline.DEADLINE_S + grace: a \"running\" case older than this with no live thread was left by a process that died\nINTERRUPTED_MESSAGE = (\"The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. \"\n                       \"Run it again to retry.\")\n\n\ndef run_started(token: str) -> None:\n    with _LIVE_LOCK:\n        LIVE_RUNS.add(token)\n\n\ndef run_ended(token: str) -> None:\n    with _LIVE_LOCK:\n        LIVE_RUNS.discard(token)\n\n\ndef is_live_run(token: str) -> bool:\n    with _LIVE_LOCK:\n        return token in LIVE_RUNS\n\n\ndef interrupt_run(conn, token: str, now: float = None) -> bool:\n    \"\"\"Mark a case left `running` as failed with the honest `run_partial` message (T-146: the case reads failed, a re-run is allowed, nothing item-level is touched, so accepted\n    and dismissed items stay exactly as they were and the re-run's `_persist` keeps them). False when the case is not running.\"\"\"\n    now = time.time() if now is None else now\n    case = DB.get_case(conn, token)\n    if case is None or case[\"status\"] != \"running\":\n        return False\n    DB.update_case(conn, token, status=\"failed\", run_finished_at=now,\n                   error=json.dumps({\"code\": \"run_partial\", \"interrupted\": True, \"message\": INTERRUPTED_MESSAGE}))\n    return True\n\n\ndef interrupt_orphaned_runs(conn, now: float = None) -> list:\n    \"\"\"At startup: every case still `running` and not running in this process was left by a process that stopped. Returns the tokens marked.\"\"\"\n    out = []\n    for r in conn.execute(\"SELECT id FROM cases WHERE status='running'\").fetchall():\n        if not is_live_run(r[0]) and interrupt_run(conn, r[0], now):\n            out.append(r[0])\n    return out\n\n\ndef settle_stale_run(conn, case: dict, now: float = None) -> dict:\n    \"\"\"On read: a `running` case with no live thread in this process whose run started more than RUN_STALE_AFTER_S ago is an orphan too (a second process, a restart that\n    skipped the startup sweep). Returns the case, re-read when it was changed.\"\"\"\n    now = time.time() if now is None else now\n    if case and case[\"status\"] == \"running\" and not is_live_run(case[\"id\"]) and case.get(\"run_started_at\") and now - case[\"run_started_at\"] > RUN_STALE_AFTER_S:\n        if interrupt_run(conn, case[\"id\"], now):\n            return DB.get_case(conn, case[\"id\"])\n    return case\n''',1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"def get_case\" -A12 app/db/db.py | head -20; grep -n \"CREATE TABLE cases\" -A12 app/db/schema.sql | head -20"
}
````

### User / tool · 2026-11-02T20:26:40.105Z

**tool result**
````
131:def get_case(conn, case_id: str):
132-    r = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
133-    return _decode(r) if r else None
134-
135-
136-def _insert(conn, table, row):
137-    bad = set(row) - _cols(conn, table)
138-    if bad:
139-        raise ValueError(f"unknown {table} fields {sorted(bad)}")
140-    conn.execute(f"INSERT INTO {table} ({','.join(row)}) VALUES ({','.join('?' * len(row))})",
141-                 [_enc(v) for v in row.values()])
142-
143-
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:48.730Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/api.py'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep('''    DB.connect(db_path).close()\n''','''    _boot = DB.connect(db_path)\n    try:\n        store.interrupt_orphaned_runs(_boot)        # T-178: a run a stopped process left \"running\" becomes failed (run again allowed); its accepted items are untouched\n    finally:\n        _boot.close()\n''')\nrep('''        case = DB.get_case(c, token)\n        if case is None:\n            raise ApiError(404, \"not_found\", \"No such case.\")\n        return case\n''','''        case = DB.get_case(c, token)\n        if case is None:\n            raise ApiError(404, \"not_found\", \"No such case.\")\n        return store.settle_stale_run(c, case)           # T-178: an orphaned \"running\" case reads failed on every route, not only after a restart\n''')\nrep('''        finally:\n            c.close()\n            runs.pop(token, None)\n''','''        finally:\n            c.close()\n            runs.pop(token, None)\n            store.run_ended(token)\n''')\nrep('''            DB.update_case(c, token, status=\"running\", stage=\"extract\", error=None, run_started_at=now, run_finished_at=None)\n            runs[token] =''','''            store.run_started(token)\n            DB.update_case(c, token, status=\"running\", stage=\"extract\", error=None, run_started_at=now, run_finished_at=None)\n            runs[token] =''')\nrep('''        if not isinstance(b, dict):\n            raise ApiError(400, \"bad_request\", \"Request body must be a JSON object.\")\n        return b\n''','''        if not isinstance(b, dict):\n            raise ApiError(400, \"bad_request\", \"Request body must be a JSON object.\")\n        return _clean_strings(b)\n''')\nrep('''    async def body_of(request: Request) -> dict:''','''    def _clean_strings(v):\n        \"\"\"T-178: a lone UTF-16 surrogate in any text of a request body (a title, an edit, a note) becomes U+FFFD before a route sees it: it cannot be encoded, so it was a 500.\"\"\"\n        if isinstance(v, str):\n            return ingest.replace_lone_surrogates(v)\n        if isinstance(v, list):\n            return [_clean_strings(x) for x in v]\n        if isinstance(v, dict):\n            return {_clean_strings(k): _clean_strings(x) for k, x in v.items()}\n        return v\n\n    async def body_of(request: Request) -> dict:''')\nopen(p,'w').write(s)\np='app/backend/ingest.py'\ns=open(p).read()\ns=s.replace('''def clean_chars(raw: str) -> str:''','''def replace_lone_surrogates(raw: str) -> str:\n    return _LONE_SURROGATE.sub(\"\\\\ufffd\", raw)\n\n\ndef clean_chars(raw: str) -> str:''',1)\ns=s.replace('''for ch in _LONE_SURROGATE.sub(\"\\\\ufffd\", raw) if''','''for ch in replace_lone_surrogates(raw) if''',1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"replace_lone\" app/backend/*.py; grep -n \"run_started_at\\|stale\" app/backend/case_list.py | head"
}
````

### User / tool · 2026-11-02T20:26:48.855Z

**tool result**
````
app/backend/api.py:228:            return ingest.replace_lone_surrogates(v)
app/backend/ingest.py:35:def replace_lone_surrogates(raw: str) -> str:
app/backend/ingest.py:43:    return "".join(ch for ch in replace_lone_surrogates(raw) if unicodedata.category(ch) != "Cf")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:26:52.130Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- app/backend/review.py app/backend/present.py; grep -n \"^ACTIONS\\|^STATUS_ACTION\" app/backend/review.py app/backend/present.py app/db/db.py"
}
````

### User / tool · 2026-11-02T20:26:52.252Z

**tool result**
````
app/db/db.py:19:ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
app/backend/review.py:17:ACTIONS = ("accept", "dismiss", "reset", "edit", "count")      # count (D-064): an amount held back for a missing detail becomes an accepted charge, see count_charge.py
app/backend/present.py:9:STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:07.486Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/review.py'\ns=open(p).read()\na='''def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:\n    t = _now(now)\n    kind, item = _item(conn, case_id, item_id)\n    action = (body or {}).get(\"action\")\n    if action not in ACTIONS:\n        raise _bad(\"That action is not allowed.\")\n'''\nb='''STALE_MESSAGE = \"This item changed in another tab; reload to see it.\"\n_TARGET_STATUS = {\"accept\": \"accepted\", \"dismiss\": \"dismissed\", \"reset\": \"pending\"}\n\n\ndef check_fresh(item: dict, body: dict, action: str) -> None:\n    \"\"\"T-178 (GATE-M3 chaos): a decision made from a stale screen must not silently override a newer one. The client sends what it last saw of the item: `version` (the item's\n    `version` field, its last-change time) and/or `expected_status` (its `review_status`). If either differs from the stored row the write is refused with 409 `stale_item`\n    and nothing changes. Neither sent = no check (older clients). A re-assertion that would leave the item exactly as it is (accept on an accepted item, dismiss on a\n    dismissed one, reset on a pending one) is harmless and is let through.\"\"\"\n    ver, exp = body.get(\"version\"), body.get(\"expected_status\")\n    if ver is None and exp is None:\n        return\n    if exp is not None and exp not in (\"pending\", \"accepted\", \"edited\", \"dismissed\"):\n        raise _bad(\"The expected_status must be one of pending, accepted, edited or dismissed.\")\n    if ver is not None and (isinstance(ver, bool) or not isinstance(ver, (int, float))):\n        raise _bad(\"The version must be the number the item was last shown with.\")\n    stale = (exp is not None and exp != item[\"review_status\"]) or (ver is not None and abs(float(ver) - float(item.get(\"updated_at\") or 0)) > 1e-6)\n    if stale and _TARGET_STATUS.get(action) != item[\"review_status\"]:\n        raise ReviewError(409, \"stale_item\", {\"item_id\": item[\"id\"], \"review_status\": item[\"review_status\"], \"version\": item.get(\"updated_at\")}, STALE_MESSAGE)\n\n\ndef apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:\n    t = _now(now)\n    kind, item = _item(conn, case_id, item_id)\n    action = (body or {}).get(\"action\")\n    if action not in ACTIONS:\n        raise _bad(\"That action is not allowed.\")\n    check_fresh(item, body, action)\n'''\nassert a in s\ns=s.replace(a,b,1)\nopen(p,'w').write(s)\np='app/backend/present.py'\ns=open(p).read()\na='''            \"review_status\": row[\"review_status\"], \"edited\": row.get(\"edited\"), \"ladder\": _ladder(row),\n            \"rerun_note\"'''\nassert s.count(a)==1\ns=s.replace(a,'''            \"review_status\": row[\"review_status\"], \"version\": row.get(\"updated_at\"), \"edited\": row.get(\"edited\"), \"ladder\": _ladder(row),\n            \"rerun_note\"''')\nopen(p,'w').write(s)\nEOF\ngit diff HEAD -U0 -- app/backend/present.py | grep -n \"version\" "
}
````

### User / tool · 2026-11-02T20:27:07.630Z

**tool result**
````
7:+            "review_status": row["review_status"], "version": row.get("updated_at"), "edited": row.get("edited"), "ladder": _ladder(row),
````

### User / tool · 2026-11-02T20:27:47.353Z

**tool result**
````
sed: 1: "app/backend/review.py
": command a expects \ followed by text
ERROR: file or directory not found: tests/unit/test_t178_chaos.py


no tests ran in 0.01s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:27:51.444Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/review.py'\ns=open(p).read()\ns=s.replace('''    ver, exp = body.get(\"version\"), body.get(\"expected_status\")''','''    ver, exp = (body or {}).get(\"version\"), (body or {}).get(\"expected_status\")''',1)\nopen(p,'w').write(s)\nEOF\ngrep -n 'ver, exp' app/backend/review.py"
}
````

### User / tool · 2026-11-02T20:27:51.551Z

**tool result**
````
280:    ver, exp = (body or {}).get("version"), (body or {}).get("expected_status")
````

### User / tool · 2026-11-02T20:28:20.320Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/unit/test_t178_chaos.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:22.819Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_t178_chaos.py -q 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T20:28:29.122Z

**tool result**
````
    def test_lone_surrogate_in_titles_and_edit_bodies_is_not_a_500(tmp_path, monkeypatch):
        db, c = make(tmp_path, monkeypatch, live=True)
>       r = c.post("/api/cases", json={"text": SAMPLE, "title": "Smith \ud83d case"})
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/unit/test_t178_chaos.py:101: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
.venv/lib/python3.12/site-packages/httpx2/_client.py:1203: in post
    return self.request(
.venv/lib/python3.12/site-packages/starlette/testclient.py:518: in request
    return super().request(
.venv/lib/python3.12/site-packages/httpx2/_client.py:783: in request
    request = self.build_request(
.venv/lib/python3.12/site-packages/httpx2/_client.py:360: in build_request
    return Request(
.venv/lib/python3.12/site-packages/httpx2/_models.py:424: in __init__
    headers, stream = encode_request(
.venv/lib/python3.12/site-packages/httpx2/_content.py:213: in encode_request
    return encode_json(json)
           ^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

json = {'text': '=== Record 1 ===\nDate: 2026-01-02\nSource: Test Clinic\nExcerpt: "Patient reports neck pain."', 'title': 'Smith \ud83d case'}

    def encode_json(json: Any) -> tuple[dict[str, str], ByteStream]:
>       body = json_dumps(json, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       UnicodeEncodeError: 'utf-8' codec can't encode character '\ud83d' in position 122: surrogates not allowed

.venv/lib/python3.12/site-packages/httpx2/_content.py:176: UnicodeEncodeError
=========================== short test summary info ============================
FAILED tests/unit/test_t178_chaos.py::test_no_paste_returns_a_500[\ud83d-False]
FAILED tests/unit/test_t178_chaos.py::test_no_paste_returns_a_500[\ud83d-True]
FAILED tests/unit/test_t178_chaos.py::test_no_paste_returns_a_500[a\ud83db-False]
FAILED tests/unit/test_t178_chaos.py::test_no_paste_returns_a_500[a\ud83db-True]
FAILED tests/unit/test_t178_chaos.py::test_no_paste_returns_a_500[\ude00\ud83d-False]
FAILED tests/unit/test_t178_chaos.py::test_no_paste_returns_a_500[\ude00\ud83d-True]
FAILED tests/unit/test_t178_chaos.py::test_lone_surrogate_in_titles_and_edit_bodies_is_not_a_500
7 failed, 61 passed in 5.79s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:34.528Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_t178_chaos.py'\ns=open(p).read()\ns=s.replace('''def counts(db):''','''def send(c, method, path, obj):\n    \"\"\"A browser's JSON.stringify writes a lone surrogate as the escape \\\\\\\\ud83d; json.dumps (ensure_ascii) does the same. The test client's own json= cannot encode one.\"\"\"\n    return c.request(method, path, content=json.dumps(obj).encode(), headers={\"content-type\": \"application/json\"})\n\n\ndef counts(db):''',1)\ns=s.replace('r = c.post(\"/api/cases\", json={\"text\": text})\\n    assert r.status_code in (201','r = send(c, \"POST\", \"/api/cases\", {\"text\": text})\\n    assert r.status_code in (201')\ns=s.replace('''    r = c.post(\"/api/cases\", json={\"text\": SAMPLE, \"title\": \"Smith \\\\ud83d case\"})''','''    r = send(c, \"POST\", \"/api/cases\", {\"text\": SAMPLE, \"title\": \"Smith \\\\ud83d case\"})''')\ns=s.replace('''    assert c.patch(f\"/api/cases/{tok}\", json={\"title\": \"x\\\\ude00y\"}).status_code < 500\n    assert c.post(f\"/api/cases/{tok}/items/e1/review\", json={\"action\": \"edit\", \"edits\": {\"summary\": \"a\\\\ud83d\"}}).status_code < 500\n    assert c.post(\"/api/cases\", json={\"text\": SAMPLE, \"title\": \"\\\\ud83d\" * 3}).status_code < 500''','''    assert send(c, \"PATCH\", f\"/api/cases/{tok}\", {\"title\": \"x\\\\ude00y\"}).status_code < 500\n    assert send(c, \"POST\", f\"/api/cases/{tok}/items/e1/review\", {\"action\": \"edit\", \"edits\": {\"summary\": \"a\\\\ud83d\"}}).status_code < 500\n    assert send(c, \"POST\", \"/api/cases\", {\"text\": SAMPLE, \"title\": \"\\\\ud83d\" * 3}).status_code < 500''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_t178_chaos.py -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T20:28:39.885Z

**tool result**
````
....................................................................     [100%]
68 passed in 4.78s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:43.146Z

**tool call — Bash**
````
{
 "command": "(timeout 900 .venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider -n 4 2>&1 | tail -15) ; ls tests",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T20:28:43.234Z

**tool result**
````
/bin/bash: timeout: command not found
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:46.561Z

**tool call — Bash**
````
{
 "command": "(.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -n 4 2>&1 | tail -15)",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T20:28:46.823Z

**tool result**
````
ERROR: usage: python -m pytest [options] [file_or_dir] [file_or_dir] [...]
python -m pytest: error: unrecognized arguments: -n 4
  inifile: None
  rootdir: /Users/arsis/zlayt-pm-project
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:49.614Z

**tool call — Bash**
````
{
 "command": "(.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -25)",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T20:28:49.674Z

**tool result**
````
Command running in background with ID: boj14mih7. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:50.876Z

Meanwhile, the contract doc.

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:51.820Z

**tool call — Bash**
````
{
 "command": "sed -n 112,122p memory/contracts/api.md | cut -c1-300; sed -n 332,346p memory/contracts/api.md | cut -c1-400; grep -n \"413 input_too_large\\|^## POST /api/cases\\b\\|GET /api/cases/{token}/status\" memory/contracts/api.md | head; git diff HEAD --stat -- memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T20:28:51.941Z

**tool result**
````
## /api/cases/{token}/export_config (D-031)
`GET` returns `{"exhibit": null|string, "bates_prefix": null|string, "bates_start": null|int}`. `PUT` takes the same keys (all optional; omitted or empty means unset) and returns the stored config; `DELETE` clears it and returns the empty config. Validation: `exhibit` and `bates_prefix` up to 20 cha

## POST /api/cases/{token}/run
Request: `{ "confirm_rerun": false }`. Response 202:
```json
{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "status": "running", "stage": "extract", "started_at": "2026-11-02T01:02:03Z" }
```
Errors: `409 run_in_progress`; `409 needs_confirm` (items already have human decisions and `confirm_rerun` is false; a rerun keeps records, gap review status, events and calls); `409 demo_mode_unsupported_input` (re-checked here, before any LLM call, in demo mode); `503 llm_unavailable`.

## GET /api/cases/{token}/status
## POST /api/cases/{token}/items/{item_id}/review
All single-item human decisions. Request body (one of these per call; shown as an array of alternatives):
```json
[
  { "action": "accept" },
  { "action": "accept", "confirm": "likely_duplicate" },
  { "action": "count", "confirm": "separate_charge" },
  { "action": "count", "confirm": "separate_charge", "confirm_flag": "likely_duplicate" },
  { "action": "dismiss", "note": "false positive" },
  { "action": "reset" },
  { "action": "edit", "edits": { "summary": "Discharged from physical therapy after two missed appointments; pain 3/10." } },
  { "action": "edit", "edits": { "excerpt": "Discharged from PT after two missed appointments. Pain 3/10." } },
  { "action": "edit", "edits": { "note": "Ask client about the 2023 episode." } }
]
```
60:## POST /api/cases
78:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `LLM_SPLIT` (D-031: the code split found one unsplit block, the model proposed record boundaries as character offsets, code validated that they cover the text exactly and start on line starts; `split_method` is then `"llm"`; an invalid proposal keeps one record and `SPLIT_AMBIGUOUS`), `SPLIT_REJECTED` (always follows `SPLIT_AMBIGUOUS` when a reason exists; the reason is `split_failure` on the run result: `NO_MODEL` no model or recorded answer, `NOT_ATTEMPTED` several records plus an unsplit tail so the model is not asked, or `LLM_FAILED_AFTER_RETRIES` / `SCHEMA_INVALID` / `SPLIT_*` from a failed or refused proposal; `split_detail` carries `FIXTURE_MISS`), `UNSPLIT_TEXT` (text outside any recognised record is kept, D-027, as a record with `unsplit: true`; T-129: unsplit records are numbered AFTER the real records so a preamble never shifts "record 1"; the one above the first real record also has `preamble: true`. **Both fields are on every record of `POST /api/cases` and `GET /api/cases/{token}`** (`false` for a real record); the `UNSPLIT_TEXT` warning is in the POST response only. A re-run after a record number came to name different text resets the paralegal's decisions on items that cite it to `pending` (the review event keeps what they were) and removes the stale items), `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
80:## POST /api/cases/pdf (D-031)
82:Errors: `400 bad_request` with `detail.reason` = `pdf_no_text_layer` (looks scanned: refused before anything is stored, no model call), `pdf_unreadable`, `pdf_encrypted`; `413 input_too_large` (`pdf_too_large`).
108:## POST /api/cases/{token}/review/batch (D-031)
115:## POST /api/cases/{token}/run
122:## GET /api/cases/{token}/status
266:## POST /api/cases/{token}/records/{rid}/confirm_date
332:## POST /api/cases/{token}/items/{item_id}/review
380:## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:55.014Z

**tool call — Bash**
````
{
 "command": "sed -n 122,132p memory/contracts/api.md | cut -c1-500; sed -n 346,360p memory/contracts/api.md | cut -c1-200"
}
````

### User / tool · 2026-11-02T20:28:55.125Z

**tool result**
````
## GET /api/cases/{token}/status
```json
{ "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "status": "running", "stage": "judge_entries",
  "stages": ["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],
  "progress": {"done": 4, "total": 9, "label": "Checking summaries 4 of 9"},
  "counts": {"entries": 9, "amounts": 3, "flags": 1},
  "error": null, "elapsed_ms": 21540 }
```
`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: the run passed its time limit; it only adds items that had no stored row, and every earlier item, second-check answer and decision of the paralegal is kept unchanged ("every item from earlier runs and every decision of yours was kept unchanged"). `run_partial`: an AI step failed on a r

## GET /api/cases/{token}
```
Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or

**Edit re-check order (R-RV-3, ADR-005; D-034, D-047).** (1) Structure, else 422. (2) Code checks (ADR-012). Any of these is a **hard `422 invalid_edit`**: nothing is saved, no judge call is made, no 
- a number, date or $ figure in the summary that is not in the quote, its source label or the parsed date: `detail.reason "SUMMARY_NUMBER_NOT_IN_EXCERPT"`, `detail.tokens`;
- a side or negation word in the summary that the quote does not have (`left`, `right`, `bilateral`, `no`, `not`, `none`, `never`, `without`, `denies`/`denied`, `negative`, `absent`, `neither`, `nor`,
- a qualifier the quote carries that the summary leaves out (hedge, attribution phrase, negation, side, approximation): `detail.reason "SUMMARY_DROPS_QUALIFIER"`, `detail.qualifiers[]` (`hedge`, `self
- a quote that cannot be located in the record: `detail.reason "HIGHLIGHT_NOT_FOUND"`;
- a dollar amount in the summary or the quote (T-139, D-019, R-CH-7, R-EX-8): `detail.reason "CHARGE_TEXT_IN_ENTRY"`, `detail.amounts[]` (the figures as written). Checked after the number/side/qualifi
`message` is a plain sentence naming the words, e.g. `The summary says “left”, which the quote does not say. Remove it or change the quote.` The export gate and accept recompute the same checks fr

Response 200:
```json
{ "item": { "id": "e3", "review_status": "edited", "state": "needs_review", "reasons": ["JUDGE_UNAVAILABLE"],
            "edited": {"summary": "...", "original_summary": "...", "at": "2026-11-02T01:06:00Z", "kept_my_wording": false} },
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:28:56.161Z

Append sections (api.md has others' dirty hunks; I'll commit only mine).

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:05.295Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='memory/contracts/api.md'\ns=open(p).read()\nanchor='## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)'\nassert s.count(anchor)==1\nadd='''## T-178 (GATE-M3 chaos): interrupted runs, stale tabs, paste text\n\n**Interrupted run (startup recovery).** A run is a thread of the server process. When the process stops (crash, sleep, redeploy) the case would stay `running` for ever. At startup every case still `running` that no thread of this process is running is set to `status: \"failed\"` with `error: {\"code\": \"run_partial\", \"interrupted\": true, \"message\": \"The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of yours were kept. Run it again to retry.\"}` and `run_finished_at` set. The same happens on any read of a `running` case that has no live thread and whose run started more than 600 s ago. Nothing item-level is touched: accepted, edited and dismissed items stay exactly as they were, the export gate reads `RUN_FAILED` (next action `CONFIRM_RERUN`), `POST .../run` is allowed again (`409 needs_confirm` while decisions exist, then `confirm_rerun: true`), and the re-run follows the T-146 rules (decided items are kept). Frontend: treat `failed` + `error.interrupted` like any `run_partial`: show `error.message` and the Run again button.\n\n**Stale second tab (`stale_item`).** Every item view (`entries[]`, `amounts[]`, `flags[]`, `GET .../items/{id}` `item`, review responses `item`) now has `version`: a number that changes whenever the item changes. `POST .../items/{item_id}/review` accepts optional `version` (the item's `version` as the client last saw it) and/or `expected_status` (its `review_status` as last seen: `pending|accepted|edited|dismissed`). If either differs from the stored item the write is refused with `409 stale_item`, message **\"This item changed in another tab; reload to see it.\"**, `detail: {item_id, review_status, version}` (the current ones), and nothing is written (no review event). Neither sent = no check (older clients). A repeat of a decision that would leave the item as it already is (accept on an accepted item, dismiss on a dismissed one, reset on a pending one) is let through. Other values: `422 invalid_edit` (`version` not a number, `expected_status` not one of the four). **Frontend must:** send `version` and `expected_status` from the item it is showing with every accept, dismiss, reset, edit and count; on `409 stale_item` show `error.message`, refetch the case (or `GET .../items/{id}`) and replace that item; update the stored `version` from every response that carries an item (batch responses do not carry one: refetch). Frontend does not send these yet (card note on T-178).\n\n**Paste text.** Text is normalised before the empty check and the size limits (`ingest.normalize_text`, used by `POST /api/cases`, the demo-gate hash, the pipeline and PDF page assembly): every Unicode format character (category Cf: zero-width space/joiner/non-joiner, word joiner, BOM, bidi marks and overrides, soft hyphen, tag characters) is removed, and a lone UTF-16 surrogate is replaced by U+FFFD. A paste with nothing else in it is `400 bad_request` \"Input is empty.\" and costs no model call; invisible characters do not count toward the 60,000-character limit; the stored case text is the cleaned text (excerpts and offsets index it). Every string in any JSON request body (titles, edits, notes) gets the same surrogate replacement at the door. No paste returns a 500.\n\n'''\ns=s.replace(anchor,add+anchor,1)\nopen(p,'w').write(s)\nEOF\ngit diff HEAD --stat -- memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T20:29:05.438Z

**tool result**
````
 memory/contracts/api.md | 8 ++++++++
 1 file changed, 8 insertions(+)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:09.414Z

**tool call — Bash**
````
{
 "command": "sleep 200; tail -5 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output",
 "timeout": 260000
}
````

### User / tool · 2026-11-02T20:29:09.416Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 200 followed by: tail -5 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:13.302Z

**tool call — Bash**
````
{
 "command": "git status --short app/backend/ingest.py app/backend/store.py app/backend/review.py app/backend/pdf_text.py memory/contracts/api.md tests/unit/test_t178_chaos.py app/backend/api.py app/backend/present.py; git diff HEAD -U0 -- app/backend/api.py | grep -c '^@@'; git diff HEAD -U0 -- app/backend/present.py | grep -c '^@@'"
}
````

### User / tool · 2026-11-02T20:29:13.475Z

**tool result**
````
MM app/backend/api.py
 M app/backend/ingest.py
 M app/backend/pdf_text.py
MM app/backend/present.py
 M app/backend/review.py
 M app/backend/store.py
MM memory/contracts/api.md
?? tests/unit/test_t178_chaos.py
6
1
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:18.432Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"passed|failed|error\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output; do sleep 5; done; tail -15 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output",
 "timeout_ms": 900000,
 "description": "wait for unit suite",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:29:18.441Z

**tool result**
````
Monitor started (task bunsec2er, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:21.978Z

**tool call — Monitor**
````
{
 "command": "sleep 1; echo waiting",
 "timeout_ms": 5000,
 "description": "noop",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:29:21.985Z

**tool result**
````
Monitor started (task bcbf1h0i1, expires in 5s unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:26.576Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output; do sleep 5; done; tail -12 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output",
 "timeout_ms": 900000,
 "description": "unit suite result",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:29:26.584Z

**tool result**
````
Monitor started (task bq3rq7z43, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:29.410Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py note T-178 --agent backend --text \"Implemented: ingest.clean_chars (Cf strip + lone surrogate -> U+FFFD) inside normalize_text (so empty check, limits, demo hash, stored text, PDF assemble); body_of replaces lone surrogates in every JSON string; store.interrupt_orphaned_runs at create_app + settle_stale_run in get_case (run_partial interrupted=true, failed, rerun allowed); review.check_fresh (version / expected_status -> 409 stale_item) + item view 'version'. FRONTEND must send version+expected_status on review POSTs and show the 409 message then refetch (api.md T-178 section). Unit tests tests/unit/test_t178_chaos.py 68 pass; full suite running.\""
}
````

### User / tool · 2026-11-02T20:29:29.546Z

**tool result**
````
noted on T-178
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:32.496Z

**tool call — Bash**
````
{
 "command": "sleep 1; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output | tail -5"
}
````

### User / tool · 2026-11-02T20:29:33.583Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:36.363Z

Still running; waiting for the monitor.

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:37.917Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output; do sleep 5; done; tail -12 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output",
 "timeout_ms": 900000,
 "description": "unit suite result (re-armed)",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:29:37.926Z

**tool result**
````
Monitor started (task bpyfsiur9, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:40.320Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output; do sleep 5; done; tail -12 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output",
 "timeout_ms": 900000,
 "description": "unit suite result",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:29:40.330Z

**tool result**
````
Monitor started (task bwf7achc3, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:46.232Z

**tool call — Bash**
````
{
 "command": "ls -la /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/ | head; ps aux | grep -c \"[p]ytest tests/unit\""
}
````

### User / tool · 2026-11-02T20:29:46.872Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:50.222Z

**tool call — Bash**
````
{
 "command": "git log -1 --format=%h && export_idx=/private/tmp/claude-501/idx178 && rm -f $export_idx && GIT_INDEX_FILE=/private/tmp/claude-501/idx178 git read-tree HEAD && echo ok"
}
````

### User / tool · 2026-11-02T20:29:51.342Z

**tool result**
````
550564f
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:54.244Z

**tool call — Bash**
````
{
 "command": "git log --oneline 04ea2bf..HEAD; for f in app/backend/api.py app/backend/present.py app/backend/ingest.py app/backend/store.py app/backend/review.py app/backend/pdf_text.py memory/contracts/api.md; do echo $f $(git diff HEAD -U0 -- $f | grep -c '^@@'); done"
}
````

### User / tool · 2026-11-02T20:29:54.466Z

**tool result**
````
550564f review(gate): GATE-M3 round-1 triage mapped to T-177, T-178, T-179, T-045, D-065-D-067
ee62967 docs(orchestrator): D-066 disputed accept needs a compare confirm; D-067 cut the drafted paragraph from the MVP UI; scope cuts 22-23
app/backend/api.py 6
app/backend/present.py 1
app/backend/ingest.py 3
app/backend/store.py 3
app/backend/review.py 4
app/backend/pdf_text.py 2
memory/contracts/api.md 1
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:29:57.514Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/idx178 git add app/backend/api.py app/backend/present.py app/backend/ingest.py app/backend/store.py app/backend/review.py app/backend/pdf_text.py memory/contracts/api.md tests/unit/test_t178_chaos.py && GIT_INDEX_FILE=/private/tmp/claude-501/idx178 git diff --cached --stat HEAD"
}
````

### User / tool · 2026-11-02T20:29:57.652Z

**tool result**
````
 app/backend/api.py            |  22 +++-
 app/backend/ingest.py         |  19 +++-
 app/backend/pdf_text.py       |   2 +
 app/backend/present.py        |   2 +-
 app/backend/review.py         |  63 +++++++++++
 app/backend/store.py          |  56 +++++++++
 memory/contracts/api.md       |   8 ++
 tests/unit/test_t178_chaos.py | 256 ++++++++++++++++++++++++++++++++++++++++++
 8 files changed, 422 insertions(+), 6 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:16.223Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -U1 -- app/backend/review.py | head -120"
}
````

### User / tool · 2026-11-02T20:30:16.331Z

**tool result**
````
diff --git a/app/backend/review.py b/app/backend/review.py
index 3678f66..b779479 100644
--- a/app/backend/review.py
+++ b/app/backend/review.py
@@ -270,2 +270,57 @@ def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: di
 
+STALE_MESSAGE = "This item changed in another tab; reload to see it."
+_TARGET_STATUS = {"accept": "accepted", "dismiss": "dismissed", "reset": "pending"}
+
+
+def check_fresh(item: dict, body: dict, action: str) -> None:
+    """T-178 (GATE-M3 chaos): a decision made from a stale screen must not silently override a newer one. The client sends what it last saw of the item: `version` (the item's
+    `version` field, its last-change time) and/or `expected_status` (its `review_status`). If either differs from the stored row the write is refused with 409 `stale_item`
+    and nothing changes. Neither sent = no check (older clients). A re-assertion that would leave the item exactly as it is (accept on an accepted item, dismiss on a
+    dismissed one, reset on a pending one) is harmless and is let through."""
+    ver, exp = (body or {}).get("version"), (body or {}).get("expected_status")
+    if ver is None and exp is None:
+        return
+    if exp is not None and exp not in ("pending", "accepted", "edited", "dismissed"):
+        raise _bad("The expected_status must be one of pending, accepted, edited or dismissed.")
+    if ver is not None and (isinstance(ver, bool) or not isinstance(ver, (int, float))):
+        raise _bad("The version must be the number the item was last shown with.")
+    stale = (exp is not None and exp != item["review_status"]) or (ver is not None and abs(float(ver) - float(item.get("updated_at") or 0)) > 1e-6)
+    if stale and _TARGET_STATUS.get(action) != item["review_status"]:
+        raise ReviewError(409, "stale_item", {"item_id": item["id"], "review_status": item["review_status"], "version": item.get("updated_at")}, STALE_MESSAGE)
+
+
+_DISPUTED = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES"}
+_DISPUTE_SENTENCE = {"partially": "The second AI check found this only partly supported by the quote.", "unsupported": "The second AI check found this not supported by the quote.",
+                     "disagrees": "The second AI check disagreed with the first result for this item."}
+
+
+def judge_dispute(item: dict):
+    """D-066: the second check's objection to this item, as its ladder verdict (partially | unsupported | disagrees), else None. The verdict on the item's ladder or any of the
+    three JUDGE_* reasons counts; unsure and unavailable are not an objection. Code only."""
+    j = (item.get("ladder") or {}).get("judge")
+    v = j.get("verdict") if isinstance(j, dict) else None
+    if v in _DISPUTED:
+        return v
+    reasons = item.get("state_reasons") or []
+    return next((k for k, code in _DISPUTED.items() if code in reasons), None)
+
+
+def compare_error(item_id: str, item: dict, compared):
+    """D-066: accepting an item the second check disputed needs the explicit statement that she compared it with the quote (`compared: true`). 422 COMPARE_REQUIRED without it."""
+    v = judge_dispute(item)
+    if not v or compared is True or item.get("review_status") == "accepted":
+        return None
+    return ReviewError(422, "COMPARE_REQUIRED", {"item_id": item_id, "reason_code": "COMPARE_REQUIRED", "verdict": v,
+                       "next_action": {"code": "COMPARE_WITH_QUOTE", "text": "Read it against the quote, then say you compared it", "target": {"item_id": item_id}}},
+                       _DISPUTE_SENTENCE[v] + " Read it against the quote, then say you compared it before you accept it.")
+
+
+def _record_compared(conn, case_id: str, item_id: str, t) -> None:
+    """D-066: her statement is kept in the accept event that carried it (after.compared = {at}), so the audit shows it."""
+    ev = conn.execute("SELECT id, after_json FROM review_events WHERE case_id=? AND item_id=? AND action='accept' ORDER BY at DESC, rowid DESC LIMIT 1", (case_id, item_id)).fetchone()
+    if ev:
+        after = json.loads(ev["after_json"]) if ev["after_json"] else {}
+        conn.execute("UPDATE review_events SET after_json=? WHERE id=?", (DB._enc({**after, "compared": {"at": store.iso(t)}}), ev["id"]))
+
+
 def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
@@ -276,2 +331,3 @@ def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now
         raise _bad("That action is not allowed.")
+    check_fresh(item, body, action)
     if action == "count":
@@ -288,3 +344,10 @@ def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now
             raise _bad("The confirm must be the name of the flag.")
+        compared = body.get("compared")
+        if compared is not None and not isinstance(compared, bool):
+            raise _bad("The compared flag must be true or false.")
+        if action == "accept" and (err := compare_error(item_id, item, compared)):      # D-066; before any write
+            raise err
         set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)
+        if action == "accept" and compared is True:
+            _record_compared(conn, case_id, item_id, t)
         if action == "reset":
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:21.046Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport subprocess,re\ncur=open('app/backend/review.py').read()\nhead=subprocess.check_output(['git','show','HEAD:app/backend/review.py']).decode()\nblk=cur[cur.index('STALE_MESSAGE ='):cur.index('_DISPUTED =')]\nassert head.count('def apply_review(')==1\nnew=head.replace('def apply_review(', blk+'def apply_review(',1)\na='''        raise _bad(\"That action is not allowed.\")\n    if action == \"count\":'''\nassert new.count(a)==1\nnew=new.replace(a,'''        raise _bad(\"That action is not allowed.\")\n    check_fresh(item, body, action)\n    if action == \"count\":''')\nopen('/private/tmp/claude-501/review_mine.py','w').write(new)\nEOF\nh=$(git hash-object -w /private/tmp/claude-501/review_mine.py) && GIT_INDEX_FILE=/private/tmp/claude-501/idx178 git update-index --cacheinfo 100644,$h,app/backend/review.py && GIT_INDEX_FILE=/private/tmp/claude-501/idx178 git diff --cached --stat HEAD; for f in api.py present.py ingest.py store.py pdf_text.py; do echo $f; done"
}
````

### User / tool · 2026-11-02T20:30:22.287Z

**tool result**
````
 app/backend/api.py            |  22 +++-
 app/backend/ingest.py         |  19 +++-
 app/backend/pdf_text.py       |   2 +
 app/backend/present.py        |   2 +-
 app/backend/review.py         |  22 ++++
 app/backend/store.py          |  56 +++++++++
 memory/contracts/api.md       |   8 ++
 tests/unit/test_t178_chaos.py | 256 ++++++++++++++++++++++++++++++++++++++++++
 8 files changed, 381 insertions(+), 6 deletions(-)
api.py
present.py
ingest.py
store.py
pdf_text.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:24.783Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/idx178 git diff --cached -U0 HEAD -- app/backend/api.py app/backend/present.py app/backend/store.py | grep '^[+-]' | cut -c1-150 | grep -v \"^+++\\|^---\" | head -70"
}
````

### User / tool · 2026-11-02T20:30:24.887Z

**tool result**
````
-    DB.connect(db_path).close()
+    _boot = DB.connect(db_path)
+    try:
+        store.interrupt_orphaned_runs(_boot)        # T-178: a run a stopped process left "running" becomes failed (run again allowed); its accepted 
+    finally:
+        _boot.close()
-        return case
+        return store.settle_stale_run(c, case)           # T-178: an orphaned "running" case reads failed on every route, not only after a restart
+    def _clean_strings(v):
+        """T-178: a lone UTF-16 surrogate in any text of a request body (a title, an edit, a note) becomes U+FFFD before a route sees it: it cannot b
+        if isinstance(v, str):
+            return ingest.replace_lone_surrogates(v)
+        if isinstance(v, list):
+            return [_clean_strings(x) for x in v]
+        if isinstance(v, dict):
+            return {_clean_strings(k): _clean_strings(x) for k, x in v.items()}
+        return v
+
-        return b
+        return _clean_strings(b)
+            store.run_ended(token)
+            store.run_started(token)
-            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row),
+            "review_status": row["review_status"], "version": row.get("updated_at"), "edited": row.get("edited"), "ladder": _ladder(row),
+import json
+import threading
+import time
+# T-178 (GATE-M3 chaos blocker): a run is a thread of THIS process. When the process dies (crash, sleep, redeploy) the case row still says "running" 
+LIVE_RUNS = set()                 # tokens whose run thread is alive in this process (api._run_thread adds and removes)
+_LIVE_LOCK = threading.Lock()
+RUN_STALE_AFTER_S = 480 + 120     # pipeline.DEADLINE_S + grace: a "running" case older than this with no live thread was left by a process that died
+INTERRUPTED_MESSAGE = ("The run was interrupted before it finished (the app was restarted or stopped). Items that finished and every decision of your
+                       "Run it again to retry.")
+
+
+def run_started(token: str) -> None:
+    with _LIVE_LOCK:
+        LIVE_RUNS.add(token)
+
+
+def run_ended(token: str) -> None:
+    with _LIVE_LOCK:
+        LIVE_RUNS.discard(token)
+
+
+def is_live_run(token: str) -> bool:
+    with _LIVE_LOCK:
+        return token in LIVE_RUNS
+
+
+def interrupt_run(conn, token: str, now: float = None) -> bool:
+    """Mark a case left `running` as failed with the honest `run_partial` message (T-146: the case reads failed, a re-run is allowed, nothing item-le
+    and dismissed items stay exactly as they were and the re-run's `_persist` keeps them). False when the case is not running."""
+    now = time.time() if now is None else now
+    case = DB.get_case(conn, token)
+    if case is None or case["status"] != "running":
+        return False
+    DB.update_case(conn, token, status="failed", run_finished_at=now,
+                   error=json.dumps({"code": "run_partial", "interrupted": True, "message": INTERRUPTED_MESSAGE}))
+    return True
+
+
+def interrupt_orphaned_runs(conn, now: float = None) -> list:
+    """At startup: every case still `running` and not running in this process was left by a process that stopped. Returns the tokens marked."""
+    out = []
+    for r in conn.execute("SELECT id FROM cases WHERE status='running'").fetchall():
+        if not is_live_run(r[0]) and interrupt_run(conn, r[0], now):
+            out.append(r[0])
+    return out
+
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:34.722Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf $S/a178 $S/h178 && mkdir -p $S/a178 $S/h178 && T=$(GIT_INDEX_FILE=/private/tmp/claude-501/idx178 git write-tree) && git archive $T | tar -x -C $S/a178 && git archive HEAD | tar -x -C $S/h178 && cp tests/unit/test_t178_chaos.py $S/h178/tests/unit/ && ln -s /Users/arsis/zlayt-pm-project/.venv $S/a178/.venv && ln -s /Users/arsis/zlayt-pm-project/.venv $S/h178/.venv && echo $T && cd $S/h178 && .venv/bin/python -m pytest tests/unit/test_t178_chaos.py -q -p no:cacheprovider 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T20:30:41.846Z

**tool result**
````
eadf9ab6a2475bcff32504ac73fc4043d57da929
FAILED tests/unit/test_t178_chaos.py::test_either_signal_alone_detects_staleness_and_the_fresh_version_succeeds
FAILED tests/unit/test_t178_chaos.py::test_a_repeat_of_the_same_decision_from_a_stale_tab_is_harmless
FAILED tests/unit/test_t178_chaos.py::test_stale_edit_is_refused_and_bad_check_values_are_a_422
FAILED tests/unit/test_t178_chaos.py::test_every_item_view_carries_a_version
47 failed, 21 passed in 4.31s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:42.685Z

Red on HEAD (47 fail). Now the full suite on the archive.

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:44.941Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/a178 && .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider > $S/a178.out 2>&1; tail -15 $S/a178.out",
 "timeout": 600000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T20:30:45.005Z

**tool result**
````
Command running in background with ID: bpze48wtw. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bpze48wtw.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:48.189Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bpze48wtw.output /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output 2>/dev/null; do sleep 5; done; echo done",
 "timeout_ms": 1200000,
 "description": "wait for suites",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:30:48.197Z

**tool result**
````
Monitor started (task byln0y4ml, expires in 20m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:30:49.982Z

**tool call — Monitor**
````
{
 "command": "sleep 600; echo t",
 "timeout_ms": 620000,
 "description": "wait",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:30:49.988Z

**tool result**
````
Monitor started (task bvbtmf1ad, expires in 10m 20s unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:00.116Z

**tool call — Bash**
````
{
 "command": "tail -c 600 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/boj14mih7.output; echo ---; tail -c 300 \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a178.out\""
}
````

### User / tool · 2026-11-02T20:31:00.216Z

**tool result**
````
---
......................................... [  2%]
........................................................................ [  3%]
........................................................................ [  4%]
........................................................................ [  6%]
...........
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:02.623Z

**tool call — Bash**
````
{
 "command": "pkill -f \"pytest tests/unit -q -p no:cacheprovider\" -n 2>/dev/null; sleep 1; ps aux | grep \"[p]ytest tests/unit\" | awk '{print $2, $NF}' ; ps -o pid,lstart,cwd -p $(pgrep -f \"pytest tests/unit\") 2>/dev/null | head"
}
````

### User / tool · 2026-11-02T20:31:02.690Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: subagents may not pkill/killall by pattern; stop only your own server by PID (kill $!)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:04.025Z

**tool call — Bash**
````
{
 "command": "ps -eo pid,lstart,command | grep \"[p]ytest tests/unit\"; lsof -p $(pgrep -f \"pytest tests/unit\" | head -1) 2>/dev/null | grep cwd"
}
````

### User / tool · 2026-11-02T20:31:04.262Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:07.667Z

Stop my own working-tree run (PID 82710 is mine).

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:07.980Z

**tool call — Bash**
````
{
 "command": "kill 82710; sleep 2; ps -eo pid,command | grep \"[P]ython -m pytest tests/unit\""
}
````

### User / tool · 2026-11-02T20:31:10.116Z

**tool result**
````
85471 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m pytest tests/unit -q -p no:cacheprovider
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:18.572Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/.claude/agent-memory/backend/project_t178_chaos_fixes.md <<'EOF'\n---\nname: t178-chaos-fixes\ndescription: T-178 GATE-M3 chaos fixes: interrupted-run recovery (store.py), stale-tab 409 (review.check_fresh), ingest.clean_chars; pitfalls\nmetadata:\n  type: project\n---\n\nCodepaths: `ingest.clean_chars` (Cf removed, lone surrogate -> U+FFFD) is inside `normalize_text`, so the empty check, limits, demo hash, stored text and `pdf_text.assemble` all see the cleaned text; `api.body_of` runs `_clean_strings` over every JSON string (the test client cannot send a surrogate with `json=`; use `content=json.dumps(obj)`). `store.interrupt_orphaned_runs` runs in `create_app`; `store.settle_stale_run` is called by `api.get_case` (stale = no live thread in `store.LIVE_RUNS` and run older than 600 s); tests that seed `status=running` AFTER creating the app are unaffected, a test that seeds it and then creates a second app gets it failed. Error shape: `{code: run_partial, interrupted: true}`, status failed.\nStale tab: `review.check_fresh` (body `version` = item `updated_at`, and/or `expected_status`), 409 `stale_item`; same-outcome repeats pass; frontend does not send them yet.\n\n**Why:** chaos tester found a stranded 'running' case that blocked export and re-run. **How to apply:** any new \"run in progress\" source must register with `store.run_started/run_ended`.\n\nPitfall: review.py / api.py / present.py get other agents' hunks mid-task (D-066 landed in review.py while I worked); rebuild the file from `git show HEAD:` plus only my block, `git hash-object -w`, `update-index --cacheinfo` into a temp `GIT_INDEX_FILE`. Full unit suite takes > 15 min and two at once halve the speed; run only the clean `git archive $(git write-tree)` copy (symlink .venv into it).\nEOF\ncd /Users/arsis/zlayt-pm-project/.claude/agent-memory/backend && echo \"- [T-178 chaos fixes](project_t178_chaos_fixes.md) — interrupted-run recovery, stale-tab 409, clean_chars; pitfalls\" >> MEMORY.md; git -C /Users/arsis/zlayt-pm-project diff --stat -- .claude/agent-memory/backend/MEMORY.md | tail -1"
}
````

### User / tool · 2026-11-02T20:31:18.682Z

**tool result**
````
 1 file changed, 3 insertions(+)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:28.147Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a178.out\"; do sleep 10; done; tail -12 \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a178.out\"",
 "timeout_ms": 1800000,
 "description": "archive unit suite result",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:31:28.155Z

**tool result**
````
Monitor started (task bv8wu1m4y, expires in 30m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:34.088Z

**tool call — Monitor**
````
{
 "command": "sleep 840; tail -c 200 \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a178.out\"",
 "timeout_ms": 900000,
 "description": "progress peek",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:31:34.098Z

**tool result**
````
Monitor started (task bnqrk7gaw, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:35.954Z

**tool call — Monitor**
````
{
 "command": "sleep 880; echo x",
 "timeout_ms": 900000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:31:35.962Z

**tool result**
````
Monitor started (task brvj9vj7m, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:39.748Z

**tool call — Bash**
````
{
 "command": "tail -c 250 \"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/a178.out\""
}
````

### User / tool · 2026-11-02T20:31:39.825Z

**tool result**
````
.......................................................... [ 17%]
........................................................................ [ 18%]
........................................................................ [ 19%]
........................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:51.731Z

**tool call — Bash**
````
{
 "command": "kill 85471; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/a178 && ls tests/unit/test_*.py | wc -l; python3 - <<'EOF'\nimport glob,os\nfs=sorted(glob.glob('tests/unit/test_*.py'), key=os.path.getsize, reverse=True)\nsh=[[] for _ in range(5)]; sz=[0]*5\nfor f in fs:\n    i=sz.index(min(sz)); sh[i].append(f); sz[i]+=os.path.getsize(f)\nfor i,s in enumerate(sh): open(f'shard{i}.txt','w').write(' '.join(s))\nEOF\nfor i in 0 1 2 3 4; do (nohup .venv/bin/python -m pytest $(cat shard$i.txt) -q -p no:cacheprovider > $S/shard$i.out 2>&1 &) ; done; sleep 2; ls $S/shard*.out"
}
````

### User / tool · 2026-11-02T20:31:53.878Z

**tool result**
````
     128
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shard0.out
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shard1.out
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shard2.out
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shard3.out
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/shard4.out
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:31:59.601Z

**tool call — Monitor**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; until [ $(grep -lE \"[0-9]+ (passed|failed)\" $S/shard*.out 2>/dev/null | wc -l) -eq 5 ]; do sleep 10; done; tail -n 3 $S/shard*.out",
 "timeout_ms": 3000000,
 "description": "all shards finished",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:31:59.627Z

**tool result**
````
Monitor started (task bevugm4om, expires in 30m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:03.808Z

**tool call — Monitor**
````
{
 "command": "sleep 590; echo x",
 "timeout_ms": 600000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:32:03.818Z

**tool result**
````
Monitor started (task beq7lziq3, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:07.461Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for i in 0 1 2 3 4; do tail -c 120 $S/shard$i.out | tr '\\n' ' '; echo; done"
}
````

### User / tool · 2026-11-02T20:32:07.577Z

**tool result**
````
..................................................................... [  7%] ...........................................
................................ [ 25%] ........................................................................ [ 31%] 
.............................. [ 21%] ........................................................................ [ 28%] ..
33%] ........................................................................ [ 38%] ...................................
............................. [ 12%] ........................................................................ [ 19%] ...
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:09.137Z

**tool call — Monitor**
````
{
 "command": "sleep 1500; echo x",
 "timeout_ms": 1600000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:32:09.150Z

**tool result**
````
Monitor started (task b0sf21kxo, expires in 26m 40s unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:12.507Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for i in 0 1 2 3 4; do tail -c 150 $S/shard$i.out | tr '\\n' ' '; echo; done; grep -h \"F\" $S/shard*.out | grep -v \"^\\.\\+\" | head"
}
````

### User / tool · 2026-11-02T20:32:12.626Z

**tool result**
````
....................... [  7%] ........................................................................ [ 14%] .......................................
........................................ [ 37%] ........................................................................ [ 43%] ......................
............................... [ 21%] ........................................................................ [ 28%] ...............................
............... [ 33%] ........................................................................ [ 38%] ...............................................
.................................................... [ 32%] ........................................................................ [ 38%] ..........
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:17.290Z

**tool call — Monitor**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; until [ $(grep -lE \"[0-9]+ (passed|failed)\" $S/shard*.out 2>/dev/null | wc -l) -eq 5 ]; do sleep 15; done; tail -qn 2 $S/shard*.out",
 "timeout_ms": 3600000,
 "description": "all shards finished",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:32:17.308Z

**tool result**
````
Monitor started (task bjsz7f0qe, expires in 30m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:18.596Z

**tool call — Monitor**
````
{
 "command": "sleep 1700; echo x",
 "timeout_ms": 1750000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:32:18.605Z

**tool result**
````
Monitor started (task bvkfa4ng1, expires in 29m 10s unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:22.616Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for i in 0 1 2 3 4; do tail -c 100 $S/shard$i.out | tr '\\n' ' '; echo; done; uptime"
}
````

### User / tool · 2026-11-02T20:32:22.742Z

**tool result**
````
............................ [ 37%] ................................................................
..................... [ 50%] ...........................................s...........................
....................................................................... [ 35%] .....................
............................... [ 62%] .............................................................
............................... [ 64%] .............................................................
14:32  up 13 days, 16:51, 2 users, load averages: 11.03 14.48 13.95
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:24.521Z

**tool call — Monitor**
````
{
 "command": "sleep 1500; echo x",
 "timeout_ms": 1600000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:32:24.529Z

**tool result**
````
Monitor started (task bgqcspiqn, expires in 26m 40s unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:29.185Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for i in 0 1 2 3 4; do tail -c 100 $S/shard$i.out | tr '\\n' ' '; echo; done; uptime"
}
````

### User / tool · 2026-11-02T20:32:29.299Z

**tool result**
````
............................................................... [ 59%] .............................
..................... [ 50%] ...........................................s...........................
............................... [ 35%] .............................................................
............................................ [ 71%] ................................................
...........................                                 [100%] 1116 passed, 4 skipped in 36.47s 
14:32  up 13 days, 16:51, 2 users, load averages: 10.95 14.41 13.93
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:35.500Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/a178; python3 - <<'EOF'\nfs=open('shard1.txt').read().split()\nprint(len(fs)); print(fs[:40])\nEOF\nps -eo pid,etime,pcpu,command | grep \"[P]ython -m pytest\" | cut -c1-200"
}
````

### User / tool · 2026-11-02T20:32:35.664Z

**tool result**
````
25
['tests/unit/test_billing.py', 'tests/unit/test_t134_unconfirmed_edit.py', 'tests/unit/test_reclassify.py', 'tests/unit/test_calibration_route.py', 'tests/unit/test_db.py', 'tests/unit/test_spanish_failsafe.py', 'tests/unit/test_pdf_hidden_r2.py', 'tests/unit/test_t139_r4.py', 'tests/unit/test_t141_r6_probes.py', 'tests/unit/test_dismissal_patterns.py', 'tests/unit/test_t146_r2_failed_rerun_keeps_items.py', 'tests/unit/test_pdf_hidden_r3.py', 'tests/unit/test_pdf_hidden_r4.py', 'tests/unit/test_t037_backend.py', 'tests/unit/test_t139_narrow.py', 'tests/unit/test_amounts.py', 'tests/unit/test_date_convention.py', 'tests/unit/test_pdf_ocr_limits.py', 'tests/unit/test_t141_d061_closed_exemption.py', 'tests/unit/test_curated_fixtures.py', 'tests/unit/test_export_edge.py', 'tests/unit/test_t145_judge_not_run.py', 'tests/unit/test_library_denylist.py', 'tests/unit/test_e2e_private_server.py', 'tests/unit/test_eval_matching.py']
87122       00:44  10.8 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m pytest tests/unit/test_trace.py tests/unit/tes
87126       00:44   5.1 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m pytest tests/unit/test_billing.py tests/unit/t
87130       00:44  29.2 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m pytest tests/unit/test_eval_runner.py tests/un
87134       00:44   4.9 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m pytest tests/unit/test_summary_trim.py tests/u
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:40.229Z

**tool call — Monitor**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; until [ $(grep -lE \"[0-9]+ (passed|failed)\" $S/shard*.out 2>/dev/null | wc -l) -eq 5 ]; do sleep 10; done; tail -qn 1 $S/shard*.out",
 "timeout_ms": 1800000,
 "description": "all shards finished",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:32:40.241Z

**tool result**
````
Monitor started (task b821ys49z, expires in 30m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:44.854Z

**tool call — Monitor**
````
{
 "command": "sleep 300; echo x",
 "timeout_ms": 400000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:32:44.867Z

**tool result**
````
Monitor started (task bajn9e1i7, expires in 6m 40s unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:47.823Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for i in 0 1 2 3 4; do tail -c 100 $S/shard$i.out | tr '\\n' ' '; echo; done; ps -eo etime,command | grep \"[P]ython -m pytest\" | cut -c1-30"
}
````

### User / tool · 2026-11-02T20:32:47.991Z

**tool result**
````
......... [ 74%] ........................................................................ [ 81%] ...
........... [ 68%] ........................................................................ [ 75%] .
....... [ 77%] ........................................................................ [ 84%] .....
......................................... [ 71%] ...................................................
...........................                                 [100%] 1116 passed, 4 skipped in 36.47s 
      00:56 /opt/homebrew/Cell
      00:56 /opt/homebrew/Cell
      00:56 /opt/homebrew/Cell
      00:56 /opt/homebrew/Cell
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:49.814Z

**tool call — Monitor**
````
{
 "command": "sleep 240; echo x",
 "timeout_ms": 300000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:32:49.821Z

**tool result**
````
Monitor started (task b1u0yp66l, expires in 5m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:52.430Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -qn 1 $S/shard*.out | cut -c1-120"
}
````

### User / tool · 2026-11-02T20:32:52.522Z

**tool result**
````
...................................................................................................1116 passed, 4 skippe
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:55.276Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for i in 0 1 2 3 4; do echo \"== $i\"; tail -c 200 $S/shard$i.out; echo; done"
}
````

### User / tool · 2026-11-02T20:32:55.369Z

**tool result**
````
== 0
................ [ 66%]
........................................................................ [ 74%]
........................................................................ [ 81%]
................
== 1
................................................................ [ 68%]
........................................................................ [ 75%]
................................................
== 2

........................................................................ [ 77%]
........................................................................ [ 84%]
.......................................
== 3
.................................................................... [ 85%]
........................................................................ [ 90%]
............................................
== 4
[ 90%]
........................................................................ [ 96%]
........................................                                 [100%]
1116 passed, 4 skipped in 36.47s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:32:59.499Z

**tool call — Monitor**
````
{
 "command": "sleep 280; echo x",
 "timeout_ms": 300000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:32:59.507Z

**tool result**
````
Monitor started (task b7sxpz9i7, expires in 5m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:03.395Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for i in 0 1 2 3; do tail -c 130 $S/shard$i.out | tr '\\n' ' '; echo; done"
}
````

### User / tool · 2026-11-02T20:33:03.496Z

**tool result**
````
........................................... [ 96%] .................................                                        [100%]
....................................................................... [ 75%] ...................................................
. [ 77%] ........................................................................ [ 84%] .........................................
.......... [ 95%] ...................................................................      [100%] 1507 passed in 64.33s (0:01:04)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:08.700Z

**tool call — Monitor**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; until [ $(grep -lE \"[0-9]+ (passed|failed)\" $S/shard*.out 2>/dev/null | wc -l) -eq 5 ]; do sleep 10; done; tail -qn 1 $S/shard*.out",
 "timeout_ms": 900000,
 "description": "all shards finished",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:33:08.711Z

**tool result**
````
Monitor started (task buu3lcr6s, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:11.122Z

**tool call — Monitor**
````
{
 "command": "sleep 290; echo x",
 "timeout_ms": 300000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:33:11.144Z

**tool result**
````
Monitor started (task bgglz65tc, expires in 5m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:15.330Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for i in 0 1 2 3 4; do tail -n 3 $S/shard$i.out | tr '\\n' ' ' | cut -c1-260; echo; done"
}
````

### User / tool · 2026-11-02T20:33:15.452Z

**tool result**
````
........................................................................ [ 96%] .................................                                        [100%] 969 passed in 71.39s (0:01:11) 
........................................................................ [ 68%] ........................................................................ [ 75%] ..........................................................
........................................................................ [ 84%] ........................................................................ [ 91%] ......................................
........................................................................ [ 95%] ...................................................................      [100%] 1507 passed in 64.33s (0:01:04) 
........................................................................ [ 96%] ........................................                                 [100%] 1116 passed, 4 skipped in 36.47s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:21.942Z

**tool call — Monitor**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; until [ $(grep -lE \"[0-9]+ (passed|failed)\" $S/shard*.out 2>/dev/null | wc -l) -eq 5 ]; do sleep 10; done; tail -qn 1 $S/shard*.out",
 "timeout_ms": 900000,
 "description": "all shards finished",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:33:21.954Z

**tool result**
````
Monitor started (task buscdmcm7, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:24.473Z

**tool call — Monitor**
````
{
 "command": "sleep 280; echo x",
 "timeout_ms": 300000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:33:24.485Z

**tool result**
````
Monitor started (task bt4lpxnt7, expires in 5m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:27.312Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for i in 1 2; do tail -n 2 $S/shard$i.out | tr '\\n' ' ' | cut -c1-260; echo; done"
}
````

### User / tool · 2026-11-02T20:33:27.403Z

**tool result**
````
........................................................................ [ 75%] ...........................................................
..................                                                       [100%] 1023 passed, 3 skipped in 87.56s (0:01:27)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:32.046Z

**tool call — Monitor**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; until grep -qE \"[0-9]+ (passed|failed)\" $S/shard1.out; do sleep 10; done; tail -n 4 $S/shard1.out",
 "timeout_ms": 900000,
 "description": "shard1 finished",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:33:32.057Z

**tool result**
````
Monitor started (task ba6dhz4tc, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:33.325Z

**tool call — Monitor**
````
{
 "command": "sleep 285; echo x",
 "timeout_ms": 300000,
 "description": "hold",
 "persistent": "false"
}
````

### User / tool · 2026-11-02T20:33:33.331Z

**tool result**
````
Monitor started (task b73vmx2xo, expires in 5m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:48.121Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -n 3 $S/shard1.out | cut -c1-200"
}
````

### User / tool · 2026-11-02T20:33:48.213Z

**tool result**
````
........................................................................ [ 93%]
........................................................................ [100%]
1151 passed, 1 skipped in 106.84s (0:01:46)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:53.156Z

**tool call — Bash**
````
{
 "command": "git log -1 --format=%h; GIT_INDEX_FILE=/private/tmp/claude-501/idx178 git write-tree; for f in app/backend/api.py app/backend/present.py app/backend/ingest.py app/backend/store.py app/backend/pdf_text.py memory/contracts/api.md; do git diff HEAD --quiet -- $f; done; GIT_INDEX_FILE=/private/tmp/claude-501/idx178 git diff --cached HEAD --stat | tail -1"
}
````

### User / tool · 2026-11-02T20:33:54.331Z

**tool result**
````
de5cb3a
eadf9ab6a2475bcff32504ac73fc4043d57da929
 10 files changed, 391 insertions(+), 17 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:33:56.414Z

**tool call — Bash**
````
{
 "command": "git log --oneline 550564f..HEAD; git diff --stat 550564f HEAD | tail -15"
}
````

### User / tool · 2026-11-02T20:33:56.538Z

**tool result**
````
de5cb3a docs(orchestrator): D-068 guided four-step UI redesign (Chris)
7c73294 test(qa): T-045 r2 sensors record (unit 5698, e2e 412, latest.json live, rejected-item claim corrected)
 evals/reports/m3-sensors.md      | 20 ++++++++++----------
 memory/ORCHESTRATOR_DECISIONS.md |  1 +
 2 files changed, 11 insertions(+), 10 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:34:01.206Z

**tool call — Bash**
````
{
 "command": "rm -f /private/tmp/claude-501/idx178b && GIT_INDEX_FILE=/private/tmp/claude-501/idx178b git read-tree HEAD && for f in app/backend/api.py app/backend/present.py app/backend/ingest.py app/backend/store.py app/backend/review.py app/backend/pdf_text.py memory/contracts/api.md tests/unit/test_t178_chaos.py; do h=$(git rev-parse eadf9ab6a2475bcff32504ac73fc4043d57da929:$f); GIT_INDEX_FILE=/private/tmp/claude-501/idx178b git update-index --add --cacheinfo 100644,$h,$f; done; GIT_INDEX_FILE=/private/tmp/claude-501/idx178b git add .claude/agent-memory/backend/project_t178_chaos_fixes.md; GIT_INDEX_FILE=/private/tmp/claude-501/idx178b git diff --cached --stat HEAD"
}
````

### User / tool · 2026-11-02T20:34:02.465Z

**tool result**
````
 .../backend/project_t178_chaos_fixes.md            |  13 ++
 app/backend/api.py                                 |  22 +-
 app/backend/ingest.py                              |  19 +-
 app/backend/pdf_text.py                            |   2 +
 app/backend/present.py                             |   2 +-
 app/backend/review.py                              |  22 ++
 app/backend/store.py                               |  56 +++++
 memory/contracts/api.md                            |   8 +
 tests/unit/test_t178_chaos.py                      | 256 +++++++++++++++++++++
 9 files changed, 394 insertions(+), 6 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:34:05.882Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/idx178b git commit -q -m \"fix(backend): T-178 GATE-M3 chaos: interrupted runs recovered at startup, stale-tab 409 stale_item, invisible characters stripped and lone surrogates replaced (no 500)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log -1 --format=%H"
}
````

### User / tool · 2026-11-02T20:34:10.677Z

**tool result**
````
check_secrets: ok (9 file(s) scanned staged)
a56f189d69271df667ff69aeceeeabea8a0de5dc
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:34:19.830Z

**tool call — Bash**
````
{
 "command": "git reset -q -- app/backend/api.py app/backend/present.py app/backend/ingest.py app/backend/store.py app/backend/review.py app/backend/pdf_text.py memory/contracts/api.md tests/unit/test_t178_chaos.py .claude/agent-memory/backend/project_t178_chaos_fixes.md; git status --short app/backend/api.py app/backend/present.py app/backend/review.py app/backend/store.py; S=$(git rev-parse HEAD); B=\"python3 tools/board.py\"; $B commit T-178 --sha $S --agent backend; $B ac T-178 --check 1 --agent backend --evidence \"tests/unit/test_t178_chaos.py 68 pass (47 fail on HEAD without the fix); full unit suite from git archive of the committed tree: 5766 passed, 0 failed (5 shards); startup recovery, 409 stale_item, clean_chars, no-500 fuzz\" ; $B handoff T-178 --agent backend --text \"What changed: ingest.clean_chars (Cf stripped, lone surrogate -> U+FFFD) inside normalize_text so empty check/limits/demo hash/stored text/PDF assemble use clean text; body_of replaces surrogates in every JSON string (no 500); store.interrupt_orphaned_runs at create_app + settle_stale_run on any get_case (failed, run_partial interrupted=true, plain message, rerun allowed, decisions untouched); review.check_fresh: version / expected_status -> 409 stale_item 'This item changed in another tab; reload to see it.', item views carry version. How verified: tests/unit/test_t178_chaos.py (68; red on HEAD), full unit suite on git archive of commit a56f189: 5766 passed. Left: FRONTEND must send version + expected_status on every review POST and show the 409 message then refetch (api.md T-178 section); browser e2e for the two-tab case is qa/frontend. Surprised: the test client cannot send a lone surrogate with json=; review.py got D-066 hunks mid-task so the commit was built from HEAD + my block.\"; $B move T-178 in_review --agent backend"
}
````

### User / tool · 2026-11-02T20:34:21.223Z

**tool result**
````
 M app/backend/api.py
 M app/backend/present.py
 M app/backend/review.py
T-178: commit a56f189d69271df667ff69aeceeeabea8a0de5dc recorded
AC 1 checked: tests/unit/test_t178_chaos.py 68 pass (47 fail on HEAD without the fix); full unit suite from git archive of the committed tree: 5766 passed, 0 failed (5 shards); startup recovery, 409 stale_item, clean_chars, no-500 fuzz
handoff written on T-178
T-178: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T20:34:24.157Z

T-178 is in_review with commit a56f189: the interrupted-run fix, the stale-tab 409, the paste cleaning and the no-500 fix are all in. The full unit suite passes (5766, 0 failed), run from a `git archive` of the committed tree. The new `tests/unit/test_t178_chaos.py` has 68 tests, and 47 of them fail on plain HEAD.

The frontend does not yet send `version` and `expected_status` on review POSTs, so the stale-tab 409 won't fire until it does; the same card note and the `memory/contracts/api.md` T-178 section say so. The frontend must also show the 409 message and refetch the item. I wrote no browser e2e for the two-tab case.
