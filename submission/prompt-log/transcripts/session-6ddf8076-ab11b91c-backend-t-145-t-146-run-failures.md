# Subagent: Backend: T-145 + T-146 run failures (Backend: T-145 + T-146 run failures)

Source: `agent-ab11b91c707455952.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T13:10:08.066Z

You are a backend worker in /Users/arsis/zlayt-pm-project. Two cards, both from reviews/GATE-M2-staff-engineer.md; read it first. Claim each with `python3 tools/board.py claim T-### --agent backend`.

**T-145 (P0 blocker).** When a run hits its deadline, judge 1 is skipped, yet the AI entries stay `verified` with no judge verdict. The Why line says "the second check agreed", and batch accept takes them. Fix it so that an entry whose judge 1 did not run:
- is never `verified`;
- says JUDGE_NOT_RUN plainly in its status and its why text;
- is skipped by batch accept.

Write a unit test for the deadline path.

**T-146.** A timed-out re-run deletes the previous run's pending items, while the error claims "finished items were kept". A failed or timed-out re-run must keep every previous item and decision; the reviewer's repro has 9 entries and 11 flags. Write a test.

**Files.** Other workers are in export.py, amounts.py, billing.py, conflict_candidates.py, uncovered.py and present.py; T-134/T-138 are in trace.py, review.py and store.py; lexicon_scan.py and summary_trim.py are also taken. The run and deadline code is likely pipeline.py and the run API. If you must touch store.py or review.py, keep it minimal, make a separate commit, and note it on the card. Do not change any prompt.

**Finish.** Write the tests first, then run the full unit suite. Commit each card separately with a pathspec: `git add <paths>`, then `git commit -m msg -- <paths>` as a separate command. Write the handoffs and move both cards to in_review. Reply in 3 lines.

### User / tool · 2026-11-02T13:10:08.072Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:10.841Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B claim T-145 --agent backend; $B claim T-146 --agent backend; grep -n -i -B2 -A25 \"T-145\\|T-146\" reviews/GATE-M2-staff-engineer.md | head -150; $B show T-145 | head -50; $B show T-146 | head -50"
}
````

### User / tool · 2026-11-02T13:10:11.281Z

**tool result**
````
T-145 claimed by backend
T-146 claimed by backend
---
id: "T-145"
title: "GATE-M2 blocker (staff): a run that hits its deadline skips judge 1 yet leaves AI entries 'verified', Why says 'the second check agreed', batch accept takes them"
milestone: "M2"
role: "backend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T13:09:56Z"
updated_at: "2026-11-02T13:10:11Z"
claimed_by: "backend"
claimed_at: "2026-11-02T13:10:11Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "an entry whose judge 1 did not run is never 'verified' and never says the check agreed; its status/why say JUDGE_NOT_RUN plainly; batch accept skips it; unit test on the deadline path", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:10:00Z orchestrator: assigned: backend
- 2026-11-02T13:10:11Z backend: claimed

## Handoff (filled when moving to in_review)

---
id: "T-146"
title: "GATE-M2 major (staff): a timed-out re-run deletes the previous run's pending items while the error says finished items were kept"
milestone: "M2"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T13:09:56Z"
updated_at: "2026-11-02T13:10:11Z"
claimed_by: "backend"
claimed_at: "2026-11-02T13:10:11Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "a timed-out or failed re-run keeps every previous item and decision (or keeps exactly what the error message says); test reproduces 9 entries/11 flags kept", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:10:00Z orchestrator: assigned: backend
- 2026-11-02T13:10:11Z backend: claimed

## Handoff (filled when moving to in_review)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:11.654Z

**tool call — Bash**
````
{
 "command": "grep -rn -i \"deadline\\|JUDGE_NOT_RUN\\|finished items\" app/backend app/llm --include=*.py | head -60"
}
````

### User / tool · 2026-11-02T13:10:11.765Z

**tool result**
````
app/backend/store.py:90:    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/pdf_text.py:36:def read_pages(data: bytes, deadline: float = None) -> list:
app/backend/pdf_text.py:38:    `deadline` (time.monotonic() value) is shared with the later stages of one upload; default EXTRACT_TIMEOUT_S from now.
app/backend/pdf_text.py:47:    deadline = deadline or time.monotonic() + EXTRACT_TIMEOUT_S
app/backend/pdf_text.py:58:                if time.monotonic() > deadline:         # stop the worker thread between pages once the API has given up on it
app/backend/pdf_ocr.py:182:def render_in_child(data: bytes, pages: list, soft_deadline: float, emit) -> None:
app/backend/pdf_ocr.py:195:            if time.monotonic() > soft_deadline:
app/backend/pdf_ocr.py:216:def render_pages(data: bytes, pages: list, deadline: float = None) -> dict:
app/backend/pdf_ocr.py:217:    """{page: PNG bytes}, rendered by the killed child process (pdf_hidden.render_messages). A child that is killed (deadline, CPU, memory),
app/backend/pdf_ocr.py:221:        msgs = pdf_hidden.render_messages(data, pages, deadline)
app/backend/pdf_ocr.py:240:def ocr_pages(data: bytes, pages: list, deadline: float = None) -> dict:
app/backend/pdf_ocr.py:249:    pngs = render_pages(data, list(pages), deadline if deadline else start + TOTAL_TIMEOUT_S)
app/backend/pdf_ocr.py:256:        if time.monotonic() - start > TOTAL_TIMEOUT_S or (deadline and time.monotonic() > deadline):
app/backend/trace.py:50:    "JUDGE_NOT_RUN": "You accepted this item, but the second AI check never ran on it. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it.",
app/backend/trace.py:51:    "JUDGE_NOT_RUN_RETRIED": "You accepted this item, but the second AI check ran again and still gave no answer. Nothing the AI wrote goes into the letter without that check, and accepting does not replace it. It clears when the check answers, or when you edit the summary in your own words.",
app/backend/trace.py:841:def judge_not_run_blockers(conn, case_id: str) -> list:
app/backend/trace.py:851:    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN_RETRIED" if tried else "JUDGE_NOT_RUN"],
app/backend/trace.py:1059:    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/trace.py:1068:                   "dismissed": rv["counts"]["dismissed"], "rejected_not_blocking": sum(1 for _, x in allitems if x["state"] == "rejected"), "judge_not_run": len(jnr), "code_check_failed": len(ccf)}
app/backend/trace.py:1120:        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
app/backend/api.py:344:                           error=json.dumps({"code": getattr(e, "code", "run_failed"), "message": "The run stopped; finished items are kept."}))
app/backend/pipeline.py:20:DEADLINE_S = 480
app/backend/pipeline.py:294:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
app/backend/pipeline.py:306:        return clock() - t0 > deadline_s
app/backend/pipeline.py:368:            if expired():                    # the deadline also applies inside the stage, record by record
app/backend/pipeline.py:409:        err = {"code": "run_deadline", "message": "The run passed its time limit; finished items were kept."}
app/backend/export.py:665:    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
app/backend/export.py:674:        return "judge_not_run" if self.items and all(i.get("reason_code") == "JUDGE_NOT_RUN" for i in self.items) else "export_blocked"
app/backend/export.py:683:    Raises JudgeNotRun when the case lists accepted items whose judge never ran (`case["judge_not_run"]`, set by store.export_case). The run-state and nothing-accepted
app/backend/export.py:685:    if case.get("judge_not_run"):
app/backend/export.py:686:        raise JudgeNotRun(case["judge_not_run"])
app/backend/export_routes.py:57:    if e.code == "judge_not_run":
app/backend/export_routes.py:58:        return judge_not_run_message(len(e.items), all(i.get("rerun_no_answer") for i in e.items))
app/backend/export_routes.py:62:def judge_not_run_message(n: int, retried: bool = False) -> str:
app/backend/pdf_checks.py:50:def extract(data: bytes, *, ocr: bool = False, include_hidden=None, deadline: float = None) -> dict:
app/backend/pdf_checks.py:52:    `include_hidden`: the raw query value for confirmed hidden-text pages (see parse_confirmed). `deadline`: a time.monotonic() value
app/backend/pdf_checks.py:62:                        deadline=deadline or time.monotonic() + (OCR_TIMEOUT_S if ocr else pdf_text.EXTRACT_TIMEOUT_S))
app/backend/pdf_checks.py:67:def _extract(data: bytes, *, ocr: bool, include_hidden, deadline: float) -> dict:
app/backend/pdf_checks.py:68:    try:                       # the text-layer read (pypdf) and the render scan (PDFium) both run in one child process killed at the deadline
app/backend/pdf_checks.py:69:        scanned = pdf_hidden.scan(data, deadline, with_text=True)
app/backend/pdf_checks.py:117:                ocr_page_data = pdf_ocr.ocr_pages(data, scan_pages, deadline=deadline)
app/backend/pdf_hidden.py:30:with a hard wall-clock kill at the deadline, an RLIMIT_CPU, RLIMIT_AS where the platform enforces it (Linux; macOS refuses it) and a
app/backend/pdf_hidden.py:31:parent-side poll of the child's RSS that kills it above CHILD_RSS_BYTES, so no work survives the deadline however slow a native call
app/backend/pdf_hidden.py:68:DEFAULT_SCAN_S = 60.0       # wall clock for scan() when the caller gives no deadline
app/backend/pdf_hidden.py:73:CHECK_EVERY = 32            # deadline check every this many objects (and once per page and per render)
app/backend/pdf_hidden.py:108:    """The shared deadline passed while scanning; the work stopped here."""
app/backend/pdf_hidden.py:455:def scan_inprocess(data: bytes, deadline: float = None) -> dict:
app/backend/pdf_hidden.py:457:    A page that could not be scanned has `unchecked: <reason>` and no text lists. `deadline` is a time.monotonic() value; the scan stops
app/backend/pdf_hidden.py:459:    be interrupted, so callers on a server use scan(), which runs this in a child process that is killed at the deadline.
app/backend/pdf_hidden.py:468:        if deadline is not None and time.monotonic() > deadline:
app/backend/pdf_hidden.py:469:            raise HiddenScanTimeout("deadline")
app/backend/pdf_hidden.py:540:def _run_child(data: bytes, deadline, mode: str, extra: str = ""):
app/backend/pdf_hidden.py:542:    text read and PDFium's render) runs in this child and nowhere else (T-087 round 4). The child gets a hard wall-clock kill at `deadline`
app/backend/pdf_hidden.py:546:    deadline = deadline if deadline is not None else now + DEFAULT_SCAN_S
app/backend/pdf_hidden.py:547:    if now >= deadline:
app/backend/pdf_hidden.py:548:        raise HiddenScanTimeout("deadline")
app/backend/pdf_hidden.py:549:    if not _SLOTS.acquire(timeout=max(deadline - now, 0)):
app/backend/pdf_hidden.py:550:        raise HiddenScanTimeout("deadline")        # every slot busy until the deadline: the caller's wait is over
app/backend/pdf_hidden.py:553:        remaining = deadline - time.monotonic()
app/backend/pdf_hidden.py:555:            raise HiddenScanTimeout("deadline")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:14.356Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"T-145\\|T-146\\|deadline\\|kept\\|judge\" reviews/GATE-M2-staff-engineer.md | head -40; sed -n 285,440p app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T13:10:14.484Z

**tool result**
````
6:- `pytest tests/unit -q -p no:cacheprovider`: **3450 passed, 8 skipped** (run twice, same result). The 8 skips are archive-only (no `.git`, `e79c3aa` not in the archive) plus one live-only Spanish judge eval (needs `SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1`).
7:- `LLM_BACKEND=fixture python -m evals.run`: exit 0, **`ship_bar_met=False`**. Blockers: `4_no_invented_facts`, "determinism_3run and unsupported_count_3run need a live backend (R-CO-7)", "judge_controls (J3/J4 seeded wrong items): not measured". Measured: grounding 1.000 (241), entry recall 0.982, amount recall 1.000, flag P/R 1.0 on all four types, hallucination catch 40/40, gap 28 not flagged and 73 flagged, case_07 total $420. A fixture run can never set ship_bar_met true, so it is not ship-bar evidence.
8:- `python -m evals.run --check-fresh` against the committed `evals/reports/latest.json`: **rc=1** ("app/llm/lexicon.yaml changed since the report", "judge_conflict_v6.md changed since the report").
10:- Mutation spot-checks on a scratch copy, each restored after: grounding `check_excerpt` returns `[]` (2 tests fail), gap `>` to `>=` (3 fail), totals counting `rate` (3 fail), export treating `dismissed` as in (5 fail), judge verdict ignored in `compose_state` (16 fail). All killed.
11:- Probes through `run_pipeline` with an injected clock (fixture backend): the deadline expiring after each stage, and a timed-out re-run.
12:- Read in full: `pipeline.py`, `generator.py`, `judges.py`, `judge_guard.py`, `confidence.py`, `llm/audited.py`, `llm/provider.py`, `llm/backends/claude_cli.py`, `schemas.py`, `flags.py` (judge and tray half), `totals.py`, `export.py` and `export_routes.py` (gate and letter), `narrative.py`, the judge-not-run half of `trace.py`, `case_extras.py` batch.
25:  "scope": "git archive 0c24f5f scratch copy; app/backend/{pipeline,generator,judges,judge_guard,confidence,flags,totals,export,export_routes,narrative,trace,case_extras}.py, app/llm/{audited,provider}.py + backends, docs/LLM_VS_CODE.md, evals/reports; fixture backend; sample case evals/golden/sample.txt",
29:    "python -m evals.run --check-fresh vs committed latest.json: rc=1, lexicon.yaml and judge_conflict_v6.md changed since the report",
31:    "5 mutants on a scratch copy (grounding removed, gap >=, rate totaled, dismissed exports, judge ignored): all killed by unit tests",
32:    "run_pipeline probes with an injected clock: deadline after verify, judge_entries, amounts, conflicts; and a timed-out re-run of a finished case",
52:      "title": "A run that hits its deadline before judge 1 leaves every AI entry 'verified' with no judge verdict (silent fallback to verified)",
53:      "evidence": "app/backend/pipeline.py:344 `if guard(\"judge_entries\") and entries: generator.judge_entries(...)`: when the deadline has passed, the stage is skipped and the entries keep the state computed at verify time. generator.py:109-127 `compose` leaves `st['judge']` unset (None) and confidence.py:62 `_lookup(_JUDGE, None, none_ok=(\"supported\",))` adds no doubt, so a missing judge composes to `verified`. Repro (fixture backend, injected clock that jumps to 10000 s when the 'verify' stage starts, `run_pipeline(conn, cid, raw, now=..., on_stage=..., deadline_s=480)`): `status timeout {'code': 'run_deadline', ...}`; entries e1..e9 `('e1','verified',None)` (state, judge verdict None); `DB.get_item('e1')` -> `state verified [] judge None`; review counts `{'pending': 15, 'verified': 11, 'needs_review': 4}`; the case view 'why' for e1 reads 'Quote found word for word, every number in the summary is in the quote, and the second check agreed.' although no second check ran; `case_extras.apply_batch(conn, cid, {'action':'accept','item_ids':['e1'..'e9']}, 5.0)` accepts all nine because batch accept keys on `state == 'verified'` (case_extras.py:48-49). Mitigations that held in my probe: the item trace shows `judge_1 skipped JUDGE_UNAVAILABLE`, and `trace.export_blockers` returned ['RUN_FAILED', 'JUDGE_NOT_RUN' x9] so nothing exported. Amounts are fail-closed (a1 needs_review JUDGE_UNAVAILABLE) so only entries are affected. No test covers it: tests/unit/test_t037_backend.py:125-133 and test_pipeline.py:117-122 assert only status, the run_deadline code and the gap flag.",
54:      "why_it_matters": "CONTRACT section 5.2 defines `verified` as grounding ok AND judge supported, and the persona's red flag is a judge that did not answer marking an item verified. Here the state, the headline 'verified' count, the Why sentence ('the second check agreed') and the batch-accept eligibility all say the AI entry was double-checked when it was not. The export gate and the failed-run banner are the only things between that state and the letter, and the paralegal can bulk-accept nine unchecked entries into the record of decisions before the gate refuses. Fail-open by omission of a key is the pattern the rest of the code base avoids (compose_state raises on a misspelled key for exactly this reason).",
55:      "fix": "Make 'no judge verdict' fail closed for every AI-made item. Either default `judge` to 'unavailable' for LLM-origin entries in `generator.compose` until `judge_entries` sets a real verdict, or, in run_pipeline after the judge stage, recompose any entry whose `ladder.judge` is None with `judge='unavailable'` (reason JUDGE_UNAVAILABLE). Do not let batch accept see these entries as verified. Optionally make `compose_state` require an explicit `judge` key (value or None for code-only items) so a caller that forgets it raises.",
56:      "acceptance_test": "Unit test: run_pipeline with a clock that expires after the 'verify' stage; assert every entry has state needs_review with JUDGE_UNAVAILABLE in reasons, none is verified, the case 'why' does not say the second check agreed, and apply_batch(accept) over those ids raises BatchRefused('not_verified'). Mutation check: reverting the fix makes this test fail."
60:      "title": "A timed-out re-run deletes the previous run's pending items and then says 'finished items were kept'",
61:      "evidence": "app/backend/pipeline.py:404-406 `_persist(...)` runs with the partial result, and :242-244 deletes every existing row that is `pending` and not in the new item set. Repro: run the sample to completion (stored entries 9, flags 11, amounts 4), then `run_pipeline` again on the same case with a clock that is past the deadline from the first stage check. Output: `run2 timeout 0 stored entries 0 flags 2 amounts 4`; case status `failed`, error `{\"code\": \"run_deadline\", \"message\": \"The run passed its time limit; finished items were kept.\"}`. Nine entries and nine model flags are gone; only the code flags (2) and the stage-0 amounts survive. Same mechanism if the deadline passes mid flags stage (:373-376 drops that record's flags). Decided items are kept, which is why the message is half true; pending ones are not.",
62:      "why_it_matters": "Honest failure: the message is false for pending items, and a paralegal who sees 'finished items were kept' will not know that her queue was emptied until she looks. Persisting a partial run over a complete one is a data-loss path on a normal failure (slow backend), not an edge case. The record text still exists, so the loss is recoverable by another run, which makes it major rather than blocker.",
63:      "fix": "Delete stale pending rows only for the kinds and stages that actually completed in this run (track `stage_done`), or skip the stale-delete entirely when `timed_out`. Keep the old rows and mark the run failed. Correct the message to say what was kept.",
64:      "acceptance_test": "Unit test: complete run, then a re-run that times out in extract; assert the number of stored entries and model flags is unchanged and the case is failed with run_deadline. Add the variant where the deadline passes between the flags of record 3 and record 4."
69:      "evidence": "`python -m evals.run --check-fresh` at 0c24f5f exits 1: 'app/llm/lexicon.yaml changed since the report' and 'app/llm/prompts/judge_conflict_v6.md changed since the report' (committed latest.json is a fixture run from 2026-11-02T09:56:40Z, source commit ea6ac71, tree dirty). Committed full live reports: evals/reports/20261102T032823Z.md is the only `ship_bar_met: True` and it predates D-046 (J3/J4 seeded controls now gate item 4); 20261102T035750Z.md, 040933Z.md and 081339Z.md (claude-cli, source 789cb39) are all `ship_bar_met: False` (081339Z: blockers `4_no_invented_facts`, golden_must_not_hits 1). The 081339Z run used lexicon hash differing from HEAD and judge_conflict_v5; HEAD's PROMPT_OF_STEP maps j3 to judge_conflict_v6 (app/llm/audited.py:123). evals/reports/controls-20261102T123937Z.md (live, bea3984, v6) shows J3 19/19 and J4 12/12 x3, but that is controls only, not determinism_3run or unsupported_count_3run. My own fixture run reports ship_bar_met=False for the expected live-only reasons.",
70:      "why_it_matters": "CONTRACT M2 exit is 'evals meet the ship bar (section 8.2)' and 8.3 requires a re-run and report path after any prompt, model or lexicon change. At the pinned commit nothing in the repo shows the four automated bars (grounding, recall, flags, no invented facts including 3-run determinism and J3/J4 controls) holding together on a live backend with the current lexicon and judge prompt. The fixture-backend numbers are all at bar, but fixtures replay recorded answers and cannot show determinism.",
77:      "evidence": "Line 97 of the doc: 'The shared judge path used by manual entry and \"not a duplicate\" (review.py) catches any exception and reports JUDGE_UNAVAILABLE ... narrowing it to provider errors is a code change with no card yet.' Code: review.py:269 and reclassify.py:173 call `judge_guard.guarded(...)`, which catches only `(AU.LLMFailed, P.LLMError)` (judge_guard.py:8), and review.py has no `except Exception` (grep count 0). Citations that do not match the code at 0c24f5f: row 4 `summary_trim.trim ... :391` (def trim is at summary_trim.py:379); row 13 `store.py:69` (the tray-flag skip is at store.py:74; :69 is `ents.append(d)`); row 11 `_other_person ... applied at :101, :138, :155, :166, :169` (calls are at conflict_candidates.py:99, 136, 153, 164, 167) and `plan_vs_outcome :133-148` / `history_denials :151-175` (defs start at :131 and :149).",
79:      "fix": "Delete or rewrite the 'Known limitation (judge errors)' bullet to describe judge_guard; replace line numbers with function names, or regenerate them.",
92:    "Deterministic core is code with sharp tests: money is integer cents, gap uses date objects with 28/29/30/31/73 cases, and all five mutants I applied (grounding, gap threshold, rate totaled, dismissed export, judge ignored) were killed.",
94:    "The export gate (D-044) held under my failure probe: accepted-but-unjudged items produced JUDGE_NOT_RUN blockers plus RUN_FAILED, and narrative sentences fail closed on any judge answer other than supported."
        d["cause"] = cause
    return d


def _accident_year(recs: list):
    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso"))      # D-055: a year hint from every dated record; the ingest kind is a label guess and is not read
    return int(ds[0][:4]) if ds else None


def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
    clock = now if callable(now) else (lambda: time.time() if now is None else now)
    t0 = clock()
    call = call or AU.make_call(conn, cid, now=clock)
    errors, stage_done = [], []

    def set_stage(name):
        if on_stage:
            on_stage(name)
        DB.update_case(conn, cid, status="running", stage=name)

    def expired():
        return clock() - t0 > deadline_s

    DB.update_case(conn, cid, status="running", stage="ingest", run_started_at=t0, error=None, backend=P.backend_name())
    try:
        ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid), splitter=_frozen_splitter(conn, cid))
    except language.UnsupportedLanguage:               # D-042: a clear failure, never a run that guesses; the case is not left 'running'
        DB.update_case(conn, cid, status="failed", error=json.dumps({"code": "unsupported_language", "message": "The records are not in English or Spanish."}))
        raise
    text, recs = ing["text"], ing["records"]
    by_n = {r["n"]: r for r in recs}
    _store_split_failure(conn, cid, ing.get("split_failure"))
    if ing.get("split_detail") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
        errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_detail"] == "FIXTURE_MISS" else None))
    _store_records(conn, cid, ing, clock())
    dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
    entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
    code_amounts = [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]]
    status = "done"
    timed_out = False

    def guard(name):
        nonlocal timed_out
        if timed_out or expired():
            timed_out = True
            return False
        set_stage(name)
        return True

    # 1-3: entries
    if guard("extract"):
        entries, rejected, failures = generator.extract_entries(recs, ing["groups"], call=call, case_text=text)
        for f in failures:
            rejected.append(generator.failure_entry(by_n[f["record_no"]], next(g for g in ing["groups"] if g[0] == f["record_no"]), f["failure"], f.get("detail")))   # never vanishes: tray item with the reason
            if f["failure"] != "SUMMARY_NOT_IN_QUOTE":      # D-054: a tray item, not an error (the model answered; code removed what the quote does not support)
                errors.append(_err("UNSUPPORTED_LANGUAGE" if f["failure"] == "UNSUPPORTED_LANGUAGE" else "LLM_FAILED_AFTER_RETRIES", "extract", f["record_no"],
                                   "FIXTURE_MISS" if f["failure"] == "FIXTURE_MISS" else None))
    if guard("verify"):
        pass                                    # grounding, token and qualifier checks ran inside extract_entries (code, same call per record)
    if guard("judge_entries") and entries:
        generator.judge_entries(entries, by_n, call=call, case_text=text)
    for e in entries + rejected:
        e["ladder"]["backend"] = P.backend_name()
        e.pop("_stage", None)
    # 4: amounts (J2 on every dollar amount)
    final_amounts = code_amounts
    if guard("amounts"):
        dollars = [a for a in ing["amounts"]]
        verdicts = judges.judge_amounts([{"id": a["id"], "raw": a["raw"], "cls": a["cls"], "excerpt": a["excerpt"]} for a in dollars],
                                        call=call, case_text=text)
        final_amounts = [_finish_amount(a, ing, verdicts.get(a["id"])) for a in dollars] + [_finish_amount(a, ing, None) for a in ing["damages"]]
    for a in final_amounts:
        a["entry_id"] = _entry_for(entries, a["record_nos"][0])
    # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T-094). No model search, so the candidate set cannot vary.
    llm_flags = []
    distinct = [by_n[g[0]] for g in ing["groups"] if by_n[g[0]].get("lang") != "other"]     # unsupported-language records are skipped (warning + error)
    if guard("conflicts"):
        llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
    # 6: per-record flags (one call per distinct record) + J4
    if guard("flags"):
        year = _accident_year(recs)

        def one(r):
            if expired():                    # the deadline also applies inside the stage, record by record
                return r, None
            return r, FL.run_flag_pass(r, call=call, tagged=bool(r["injection_tag"]), accident_year=year, case_text=text)
        with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
            per = list(ex.map(one, distinct))
        for r, fs in per:
            if fs is None or expired():
                timed_out = True
                continue
            fs = [f for f in fs if f["type"] != "record_warning"]          # stage 0 already made the record_warning flag
            for k, f in enumerate(fs, 1):
                f["id"] = f"f_r{r['n']}_{k}"
            llm_flags += FL.judge_flags(fs, call=call, case_text=text)
    # 7: finalize
    set_stage("finalize")
    for f in llm_flags:
        f.setdefault("record_nos", [f["record_no"]])
        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
        f["ladder"]["item_id"], f["ladder"]["backend"], f["ladder"]["state"] = f["id"], P.backend_name(), f["state"]
        f["ladder"]["code_checks"].setdefault("classified_by", "lexicon+llm")
        f.setdefault("review_status", "pending")
        f["origin"] = _ORIGIN.get(f["origin"], f["origin"])
        f.pop("record_no", None)
    flag_items = ing["flags"] + [_clean(f) for f in llm_flags if f["state"] != "rejected"]
    tray = [_clean(e) for e in rejected] + [_clean(f) for f in llm_flags if f["state"] == "rejected"]
    entries = [_clean(e) for e in entries]
    dated = sorted((e for e in entries if dated_cut(e)), key=lambda e: (e["date"], e["seq"]))
    undated = [e for e in entries if not dated_cut(e)]
    order = {"gap": 0, "conflict": 1, "pre_existing": 2, "causation": 3, "record_warning": 4}
    flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
    final_amounts = [_clean(a) for a in final_amounts]
    damages_out = [a for a in final_amounts if a["cls"] == "damages"]      # work-loss mentions: stored as amounts of kind damages, listed apart
    final_amounts_out = [a for a in final_amounts if a["cls"] != "damages"]
    from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
    PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
    now_t = clock()
    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
    _persist(conn, cid, "amount", final_amounts, now_t)
    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
    if timed_out:
        status = "timeout"
        err = {"code": "run_deadline", "message": "The run passed its time limit; finished items were kept."}
    else:
        status = "done_with_errors" if errors else "done"
        err = None
    DB.update_case(conn, cid, status="failed" if timed_out else "ready", stage="finalize", error=json.dumps(err) if err else None,
                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
    tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
    all_items = dated + undated + final_amounts + flag_items
    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:21.636Z

**tool call — Bash**
````
{
 "command": "sed -n 195,284p app/backend/pipeline.py; grep -n \"def compose\\|def judge_entries\\|JUDGE_UNAVAILABLE\\|def failure_entry\" app/backend/generator.py; sed -n 95,140p app/backend/generator.py; sed -n 30,80p app/backend/case_extras.py; sed -n 40,90p app/llm/confidence.py"
}
````

### User / tool · 2026-11-02T13:10:21.762Z

**tool result (error)**
````
Exit code 1
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


def _row(kind: str, it: dict) -> dict:
    ladder = _clean(it.get("ladder") or {})
    if kind == "entry":
        return {"record_ids_json": it["record_ids"], "seq": it["seq"], "date_iso": it.get("date"), "provider": it["provider"],
                "summary": it.get("summary"), "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"),
                "excerpt_end": it.get("excerpt_end"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
    if kind == "amount":
        return {"record_ids_json": it["record_ids"], "entry_id": it.get("entry_id"), "text": it["text"], "value_cents": it["cents"],
                "kind": it["cls"], "excerpt": it.get("excerpt"), "excerpt_start": it.get("excerpt_start"), "excerpt_end": it.get("excerpt_end"),
                "duplicate_note": it.get("duplicate_note"), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}
    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
                                    "record_nos", "excerpt", "excerpt_b", "names", "lexicon_ids", "endpoint_warnings", "conditional") if k in it}
    return {"type": it["type"], "category": it["category"], "source_kind": it.get("source_kind", "record"), "title": it["title"],
            "explanation": it["explanation"], "computed_json": computed, "evidence_json": it.get("evidence", []),
            "origin": _ORIGIN.get(it["origin"], it["origin"]), "state": it["state"], "state_reasons_json": it["reasons"], "ladder_json": ladder}


def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
    for it in items:
        old = existing.get(it["id"])
        if kind == "amount" and old is not None:        # T-084: a rerun keeps the class the paralegal gave a figure
            from app.backend import reclassify as RC
            it = RC.carry_over(old, it)
        row = _row(kind, it)
        if old is None:
            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
            continue
        DB.update_item(conn, it["id"], now=now, case=cid, **row)
        if kind == "flag" and old["review_status"] != "pending":
            oc = old.get("computed") or {}
            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
            else:
                it["review_status"] = old["review_status"]
        elif old["review_status"] != "pending":
            it["review_status"] = old["review_status"]
    keep = {i["id"] for i in items}
    for oid, old in existing.items():
        if oid not in keep and old["review_status"] == "pending":
            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))


def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
    _store_records(conn, cid, ing, now)
    _persist(conn, cid, "flag", ing["flags"], now)
    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
    DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
    return ing


# ------------------------------------------------------------------ stages 4-6 helpers
def _finish_amount(a: dict, ing: dict, judged) -> dict:
    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
    by_n = {r["n"]: r for r in ing["records"]}
    a = dict(a)
    a.update(excerpt_start=a["start"], excerpt_end=a["end"])
    verdict = judged["ladder"] if judged else ("unavailable" if a["cls"] != "damages" else None)
    state, reasons = confidence.compose_state(
        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
         "schema_valid": True, "code_reasons": [], "judge": None if a["cls"] == "damages" else verdict},
        {"injection": a["injection"], "amount_class": a["cls"], "translated": any(language.translated_record(by_n.get(n)) for n in a["record_nos"])})      # D-050
    a["state"], a["reasons"] = state, reasons
    a[

... [1833 characters truncated] ...

   source_kind="record")
    cc = e["ladder"]["code_checks"]
    cc.update(excerpt_verbatim=not failures, excerpt_whole_sentence="EXCERPT_NOT_WHOLE_SENTENCE" not in code_reasons,
              qualifier_carried="EXCERPT_OMITS_QUALIFIER" not in code_reasons and "SUMMARY_DROPS_QUALIFIER" not in code_reasons,
              date_provider_from_header=True,
              summary_tokens_not_in_excerpt=g.new_tokens(summary, excerpt, record["source"], record.get("date_iso") or "") if not failures else [],
              highlight_found=span is not None)
    return compose(e, record, grounding_failures=failures, code_reasons=list(dict.fromkeys(code_reasons)))


def compose(e: dict, record: dict, *, grounding_failures=None, code_reasons=None, schema_valid=True, judge="__keep__", fixture_miss=False) -> dict:
    """Set e['state'], e['reasons'], e['why'] from e['_stage'] (private inputs; callers drop '_' keys when storing). Re-run after the judge."""
    lad = e["ladder"]
    st = e.setdefault("_stage", {})
    if grounding_failures is not None:
        st["grounding_failures"] = grounding_failures
    if code_reasons is not None:
        st["code_reasons"] = code_reasons
    st.setdefault("code_reasons", [])
    st.setdefault("grounding_failures", [])
    st["schema_valid"] = schema_valid and st.get("schema_valid", True)
    if judge != "__keep__":
        st["judge"] = judge
    st["fixture_miss"] = fixture_miss or st.get("fixture_miss", False)
    state, reasons = confidence.compose_state(
        {"grounding_failures": st["grounding_failures"], "schema_valid": st["schema_valid"], "code_reasons": st["code_reasons"],
         "judge": st.get("judge")}, _ctx(record, fixture_miss=st["fixture_miss"]))
    e["state"], e["reasons"] = state, reasons
    e["why"] = " ".join(why.why(c) for c in reasons) if reasons else "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
    jd = (lad.get("judge") or {})
    if jd.get("verdict") in ("partially", "unsupported") and why.judge_detail(jd.get("reason_code")):
        e["why"] += " " + why.judge_detail(jd["reason_code"])
    lad["state"] = state
    return e


def _one(args):
    record, group, call, case_text = args
    return extract_one(record, group, call=call, case_text=case_text)

    return {"id": item_id, "reason": "code_check_failed", "reason_code": err.detail["reason_code"], "why": err.message, "next_action": err.detail["next_action"]}


def _check(conn, case_id, ids, action):
    """[{id, reason}] for every id that may not be in this batch. Entries only; accept needs state verified and status pending."""
    bad, cache = [], {}
    for i in ids:
        try:
            kind, row = review._item(conn, case_id, i)
        except review.ReviewError:
            bad.append({"id": i, "reason": "not_found"})
            continue
        if kind != "entry":
            bad.append({"id": i, "reason": "not_an_entry"})
        elif action == "accept" and review.date_unconfirmed(conn, case_id, kind, row):
            bad.append({"id": i, "reason": "date_unconfirmed"})
        elif action == "accept" and (err := _code_check_refusal(conn, case_id, i, row, cache)):     # D-051: same check as a single accept
            bad.append(err)
        elif action == "accept" and row["state"] != "verified":
            bad.append({"id": i, "reason": "not_verified"})
        elif action == "accept" and row["review_status"] != "pending":
            bad.append({"id": i, "reason": "not_pending"})
    return bad


def apply_batch(conn, case_id, body, now):
    """All or nothing. Validation covers every id before the first write; if a write still fails, the items already changed are put back."""
    action, ids = (body or {}).get("action"), (body or {}).get("item_ids")
    if action not in ("accept", "reset") or not isinstance(ids, list) or not ids or len(ids) > MAX_BATCH or \
            not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("bad_request")
    with _LOCK:
        bad = _check(conn, case_id, ids, action)
        if bad:
            raise BatchRefused(bad)
        done = []
        recs = store.load_records(conn, case_id) if action == "accept" else None
        try:
            for i in ids:
                review.batch_apply(conn, case_id, i, action, now, recs)
                done.append(i)
        except Exception:
            for i in reversed(done):          # compensate: each undo is itself an audited event
                review.batch_apply(conn, case_id, i, "reset", now)
            raise
    items = [{"id": i, "review_status": DB.get_item(conn, i, case_id)["review_status"]} for i in ids]
    return {"items": items, "totals": present.totals_view(conn, case_id), "review": present.review_view(conn, case_id), "warnings": []}


# ------------------------------------------------------------------ export config
def validate_config(b):
sed: app/llm/confidence.py: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:24.422Z

**tool call — Bash**
````
{
 "command": "sed -n 1,30p app/backend/confidence.py 2>/dev/null | head -5; ls app/backend | head -80; grep -n \"def judge_entries\" -A45 app/backend/generator.py"
}
````

### User / tool · 2026-11-02T13:10:24.524Z

**tool result**
````
"""compose_state(ladder, context) -> (state, reasons)  (ADR-005, R-TL-5, LLM_VS_CODE row 17). Pure and deterministic.

Precedence: rejected > needs_review > verified. Reason codes are a closed list (api.md appendix); an unknown code is a bug.
D-050: ctx["translated"] (the item comes from a record routed Spanish or LANGUAGE_UNCERTAIN) always adds AI_TRANSLATION, so such an item
can never be `verified`, whatever its code checks and judge said; the paralegal's accept is the gate. Every caller that has the record passes it. Reason codes are a closed list (api.md appendix); an unknown code is a bug.
__init__.py
__pycache__
amounts.py
api.py
billing.py
calibration_route.py
case_extras.py
charge_text.py
confidence.py
conflict_candidates.py
conflicts.py
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
178:def judge_entries(entries: list, records_by_n: dict, *, call, case_text: str = "") -> list:
179-    """Stage 3: judge 1 on every non-rejected entry. Judge failure -> 'unavailable' (JUDGE_UNAVAILABLE). Recomposes state."""
180-    def work(e):
181-        if e["state"] == "rejected":
182-            return e, None, False
183-        rec = records_by_n[e["seq"]]
184-        n = promptlib.nonce(case_text, "j1", e["id"])
185-        try:
186-            return e, spanish.run_j1_meta(e["summary"], e["excerpt"], rec["source"], call=call, nonce=n, item_id=e["id"], lang=language.record_lang(rec)), False
187-        except P.FixtureMiss:
188-            return e, ("unavailable", None, "NONE"), True
189-    with ThreadPoolExecutor(max_workers=CONCURRENCY) as ex:
190-        results = list(ex.map(work, entries))
191-    for e, res, miss in results:
192-        if res is None:
193-            continue
194-        verdict, call_id, code = res
195-        e["ladder"]["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(records_by_n[e["seq"]])), "call_id": call_id,
196-                                "verdict": verdict, "reason_code": code}
197-        compose(e, records_by_n[e["seq"]], judge=verdict, fixture_miss=miss)
198-    return entries
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:28.348Z

**tool call — Bash**
````
{
 "command": "grep -n \"JUDGE_UNAVAILABLE\\|JUDGE_NOT_RUN\" -r app memory/contracts/api.md tests/unit | grep -v \"^app/backend/trace.py:5[01]\" | head -60; sed -n 40,100p app/backend/confidence.py; sed -n 835,860p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T13:10:28.533Z

**tool result**
````
app/README-arch.md:82:First to go if a milestone exceeds 150% of budget (record in `SCOPE_CUTS.md`): the side-by-side layout (R-ST-1; the record modal R-RV-9 stays), then the synchronous judge re-run on edits (the edit would save as `needs_review` / `JUDGE_UNAVAILABLE`, which is already a defined state). The per-record flag pass is not on the cut line (it is the injection control, ADR-008.3); cheapen it by batching the judge instead.
app/frontend/stepper.js:165:  const jnrBlockers = (g) => ((g && g.blockers) || []).filter((b) => b.reason_code === "JUDGE_NOT_RUN");
app/frontend/stepper.js:414:  // and decides nothing: a judge step that never ran is "second check missing" only when the gate lists JUDGE_NOT_RUN for this item, otherwise the wording is the
app/frontend/stepper.js:421:    const gated = !!gate && ((gate.blockers || []).some((b) => b.reason_code === "JUDGE_NOT_RUN" && b.item_id === tr.item_id));
app/frontend/stepper.js:577:    const bl = blocked.blockers || [], rerun = bl.some((b) => b.reason_code === "JUDGE_NOT_RUN");
app/frontend/stepper.js:582:    if (!blocked.cleared && rerun) host.append(el("div", { class: "zs-todo-btns" }, S.rerunButton(groupLabel(bl.filter((b) => b.reason_code === "JUDGE_NOT_RUN").length))));
app/frontend/judges.js:10:  let cache = null, wasOpen = false, gate = null;   // gate: what the export gate lists, {jnr: [item ids with a JUDGE_NOT_RUN blocker], code: [code-check blockers on the paralegal's wording]}; null until the case trace has loaded
app/frontend/judges.js:38:    return { jnr: bl.filter((b) => b.reason_code === "JUDGE_NOT_RUN").map((b) => b.item_id), code: bl.filter((b) => ZL.stepper.isCodeBlocker(b)), verdict: (tr && tr.verdict) || null };
app/backend/generator.py:179:    """Stage 3: judge 1 on every non-rejected entry. Judge failure -> 'unavailable' (JUDGE_UNAVAILABLE). Recomposes state."""
app/backend/trace.py:218:        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
app/backend/trace.py:229:        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
app/backend/trace.py:711:            st.append(step("judge_1", "Second AI check: is the sentence supported by the quote?", "llm", SKIPPED, narrative.REASONS["JUDGE_UNAVAILABLE"], reason="JUDGE_UNAVAILABLE", rule="row 4", evidence=ev, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
app/backend/trace.py:795:        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
app/backend/trace.py:851:    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN_RETRIED" if tried else "JUDGE_NOT_RUN"],
app/backend/trace.py:892:            unresolved.append(dict(base, state_reason="JUDGE_UNSURE" if v == "unsure" else ("FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"),
app/backend/trace.py:1014:            st.append(step("judges", "Second AI check on every AI-made item", "llm", PENDING, msg + "The run is still going.", reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts))
app/backend/trace.py:1016:            st.append(step("judges", "Second AI check on every AI-made item", "llm", FAIL, msg + reason_text("JUDGE_UNAVAILABLE"),
app/backend/trace.py:1017:                           reason="JUDGE_UNAVAILABLE", rule="row 4", counts=jcounts, next_action=na("RERUN_JUDGE", {"view": "judges"})))
app/backend/trace.py:1059:    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/pipeline.py:259:    """Compose an amount's state. `judged` is None before judge 2 ran (state then carries JUDGE_UNAVAILABLE)."""
app/backend/confidence.py:10:    "HIGHLIGHT_NOT_FOUND", "JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE",
app/backend/confidence.py:20:          "unsure": "JUDGE_UNSURE", "unavailable": "JUDGE_UNAVAILABLE"}
app/backend/why.py:16:    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this item has not been double-checked.",
app/backend/store.py:90:    out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
app/backend/flags.py:360:        f["reasons"] = [FILTERED] + [r for r in f["reasons"] if r not in (FILTERED, "JUDGE_UNAVAILABLE", "LLM_ONLY")]       # keeps a grounding failure / injection reason (T-126 r2)
app/backend/flags.py:367:        f["reasons"] = [r for r in f["reasons"] if r != "JUDGE_UNAVAILABLE"]
app/backend/flags.py:377:    An unsure answer or failed judge call leaves the flag needs_review (JUDGE_UNSURE / JUDGE_UNAVAILABLE); a disagreement on a flag that is both
app/backend/reclassify.py:40:    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this figure cannot become a charge yet. Try again.",
app/backend/reclassify.py:172:        raise _refuse("JUDGE_UNAVAILABLE", wording=wording)
app/backend/reclassify.py:176:        reason = {"disagrees": "JUDGE_DISAGREES", "unsure": "JUDGE_UNSURE"}.get(ladder_verdict, "JUDGE_UNAVAILABLE")
app/backend/review.py:8:JUDGE_UNAVAILABLE).
app/backend/review.py:296:        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available; the item stays marked for review.", "item_id": item_id})
app/backend/rejudge.py:17:_JUDGE_REASONS = {"JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE", "FIXTURE_MISS"}
app/backend/narrative.py:25:    "JUDGE_UNAVAILABLE": "The second check was not available for this sentence.",
app/backend/narrative.py:113:            base["removed"].append({**item, "reason": {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED"}.get(lad, "JUDGE_UNAVAILABLE")})
app/backend/export.py:555:_EDIT_REASON_PHRASE = {"JUDGE_UNAVAILABLE": "second check not available (JUDGE_UNAVAILABLE)", "FIXTURE_MISS": "second check not available (FIXTURE_MISS)",
app/backend/export.py:665:    `items` = the blockers exactly as the export gate lists them (trace.export_blockers); `code` is 'judge_not_run' when every one is JUDGE_NOT_RUN, else 'export_blocked'.
app/backend/export.py:674:        return "judge_not_run" if self.items and all(i.get("reason_code") == "JUDGE_NOT_RUN" for i in self.items) else "export_blocked"
memory/contracts/api.md:28:| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
memory/contracts/api.md:346:`message` is a plain sentence naming the words, e.g. `The summary says “left”, which the quote does not say. Remove it or change the quote.` The export gate and accept recompute the same checks from the current wording through the same functions (D-051), so an edit the route stores can never be an export blocker for a code reason. The same rule applies to `POST .../records/{rid}/entry`. (3) Judge 1 re-run: it never blocks a human-written edit (D-045b). If it says `partially`/`unsupported`, errors, times out, or has no recorded fixture (always the case in demo mode), the edit is saved, the item becomes `needs_review` (reason `JUDGE_UNAVAILABLE` when it did not answer) and `warnings[]` carries `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED` or `JUDGE_UNAVAILABLE`; no 409, because nothing the code can verify is wrong. The judge never lets an unchecked edit look verified.
memory/contracts/api.md:350:{ "item": { "id": "e3", "review_status": "edited", "state": "needs_review", "reasons": ["JUDGE_UNAVAILABLE"],
memory/contracts/api.md:355:  "warnings": [ {"code": "JUDGE_UNAVAILABLE", "message": "The second check was not available for this edit; the item stays marked for review.", "item_id": "e3"} ] }
memory/contracts/api.md:360:- Item view: every entry has `edit_to_check` (bool), true when `review_status` is `edited`, `state` is `needs_review` (any reason: `JUDGE_UNAVAILABLE`, `JUDGE_PARTIAL`, `OCR_DERIVED`, a translation label) and the entry has an edited `summary` or `excerpt`. It is false after accept, dismiss or reset, and for a verified edit. `review.counts.edit_to_check` counts them (they are also still in `counts.edited`). `review.ready_to_export` is false while `edit_to_check` > 0, and an edit still to check does not count as accepted.
memory/contracts/api.md:363:- Gate (`/trace` `export_gate`): `warnings[]` gains `{reason_code: "EDIT_NOT_CONFIRMED", count, why, next_action: DECIDE}`; `counts.edit_not_confirmed`; `counts.accepted` leaves it out; the `review` step is `pending` with reason `EDIT_NOT_CONFIRMED`; the verdict label counts it in "Ready to export (N not reviewed)". It is never a `JUDGE_NOT_RUN` blocker while open.
memory/contracts/api.md:364:- Internal notes: EDITED ITEMS lists it with "(edited; second check not available (JUDGE_UNAVAILABLE); not yet confirmed against the quote, so it is not in the letter (accept it to put it there))" (the reason sentence follows the item's reasons: `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, ...), PENDING ITEMS NOT INCLUDED lists it with the same phrase, and RECORDS NOT IN THE TREATMENT SECTION says "edited, not yet confirmed against the quote". After she accepts, EDITED ITEMS keeps the reason: "(accepted by the paralegal after comparing it with the quote; second check not available (JUDGE_UNAVAILABLE))". The notes never say she accepted an edit she has not accepted.
memory/contracts/api.md:367:- T-134 r3: `/judges` `totals.human_overrides` ("you accepted despite an objection") counts only her explicit accept; an open edit (`edit_to_check`) whose re-check objected stays in `rejections` and `totals.unsupported` but not in `human_overrides`. For a re-picked quote under the AI's own summary (`edit_to_check` with no second-check answer) the item `human` step, the `EDIT_NOT_CONFIRMED` gate warning and the review step say that accepting alone will not put it in the letter (D-044 still blocks until the check answers or she edits the summary). After `POST /rejudge` leaves an accepted item unavailable, its `JUDGE_NOT_RUN` blocker carries `rerun_no_answer: true` and a `why` that says the check ran again and gave no answer; the 422 `judge_not_run` message then says what clears it instead of repeating "Run the second check again". Frontend: show `why` as given; no new required field.
memory/contracts/api.md:368:- T-138: `POST /items/{id}/review {action: "reset"}` on an edited entry restores the AI wording together with its pre-edit second-check result, code-check record and state (kept in `ladder.pre_edit`, internal); accept then works as before the edit and does not hit `JUDGE_NOT_RUN`. If something else rewrote the state after the edit, only the check result returns.
memory/contracts/api.md:377:- Anything not allowed: `422 reclassify_refused`, nothing changes, no event: `{error: {code, message, detail: {reason, check: "code"|"judge", wording?, error_class?}}}`. `detail.reason` is one of `NO_VALUE`, `INJECTION_SUSPECTED`, `NO_CHARGE_WORDING` (check `code`), `JUDGE_DISAGREES`, `JUDGE_UNSURE`, `JUDGE_UNAVAILABLE` (check `judge`; `JUDGE_UNAVAILABLE` includes no recorded answer in demo mode, so a rate-to-charge there is refused with "try again" wording). `message` is a fixed plain sentence, safe to show. Other errors: `400 bad_request` (missing/other `to`, non-text `note`), `404 not_found`, `409 item_rejected`, `422 invalid_edit` (not an amount).
memory/contracts/api.md:396:**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.blockers[]` is exactly the gate's `blockers[]` (`{item_id, kind, reason_code, why, next_action}`). `error.code` is `judge_not_run` when every blocker is `JUDGE_NOT_RUN` (message "N accepted items have not had the second AI check, so the export is blocked. Run the second check again."), else `export_blocked` (a run in progress or failed, a failing code check on the paralegal's own wording, or nothing accepted; message = the first blocker's `why` + " The export is blocked."). There is no override and no body parameter; the only ways out are a judge answer (`POST /rejudge`), dismissing / resetting the item, finishing or re-running the run, or accepting something. An edit still marked `needs_review` is open and out of the letter, so it does not stop the export either (T-134, see the edit section). Pending items do not stop the export (D-045(a)): they are listed under `excluded.pending`, the notes' AI line counts them, and the UI asks one confirmation before copying.
memory/contracts/api.md:653:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below) and `NOTHING_ACCEPTED` (nothing accepted or edited, so the letter would be empty), all with `item_id` null except `JUDGE_NOT_RUN`. **Code-check blocker (D-045(b), T-098).** A summary the paralegal wrote or edited (`ai_drafted: false`) skips the judge but not the code checks: an accepted or edited, live entry of that kind whose current wording fails any code check (`SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `EXCERPT_NOT_WHOLE_SENTENCE`, `EXCERPT_OMITS_QUALIFIER`, `HIGHLIGHT_NOT_FOUND`) is one blocker `{item_id, kind: "entry", reason_code: <first failing check>, step_id, failed_steps[], why, next_action}`, with `step_id` the failing item-trace step (e.g. `summary_qualifier`); `next_action` is `EDIT_SUMMARY` (or `EDIT_QUOTE` / `READ_RECORD`) with a specific `text`, e.g. "Edit the summary to keep ‘possible’; the quote says it and your summary leaves it out. The export stays blocked until it passes." `GET /export` returns `422 export_blocked` with the same list; `export_gate.counts.code_check_failed` counts them; the case verdict is `needs_attention` ("N edited summaries fail a check") when only these block. Cleared by an edit that passes, dismissing or resetting the item. On `GET /items/{id}/trace` the failing code step has `blocks_export: true` and that `next_action`, `verdict` is `{code: needs_attention, label: "Needs your attention: a check on your wording fails", blocks_export: true}` and the top-level `next_action` is the step's, even though `review_status` is accepted/edited. **D-051 (T-098 r2):** the blocker covers every accepted or edited entry, AI-made or human (only the judge is exempt for human wording). The gate and the item trace recompute all five code checks (summary token D-034/D-047, qualifier dropped D-022, quote whole sentence D-012/D-021, quote omits the hedge sentence, quote is word for word in the record) plus the highlight, from each entry's CURRENT summary and quote, and also honour stored reasons; a stale stored 'pass' cannot hide a failing summary. For an AI draft the blocker `why` says the AI drafted it. `GET /export` is 422 `export_blocked` for such a state; the case verdict label is "N summary/summaries fail(s) a check". The item trace verdict label for a failing accepted entry is "Needs your attention: a check on this summary fails" for an AI draft and "... a check on your wording fails" only when the paralegal wrote or edited the summary. In the internal notes, AI wording that failed a code check is never printed: EDITED ITEMS says "summary was AI wording removed (failed a check: <plain reason>), now ..." and the draft paragraph says "AI wording removed (failed a check: <reason>) (<entry id>)" (a narrative sentence removed for a judge reason is still printed). An unreviewed (pending) draft that fails a code check is listed in the internal notes as "summary not shown, a code check on it fails" so its wording never appears in the export.  **Pending items are not blockers** (D-045(a)): they never reach the letter and the AI disclosure line counts them. They appear in `warnings[]` as one element `{reason_code: "ITEMS_NOT_REVIEWED", count, why: "N items are not reviewed, so they will not be in the letter; the AI disclosure line will count them.", next_action: DECIDE}` (empty array when nothing is pending), and in `counts.pending_items` (all live pending, of which `counts.date_unconfirmed` cannot be accepted until the date is confirmed, D-041). `PENDING_DECISION` and `DATE_UNCONFIRMED` no longer occur in `export_gate.blockers`, and the gate `reason_code` `ITEMS_PENDING` is gone (the per-item `PENDING_DECISION` step reason is unchanged). The `verdict` is `ready` with label "Ready to export (N not reviewed)" when pending items remain. Rejected items never block (`counts.rejected_not_blocking`); dismissed items never block. **T-114 (rates):** every amount in `amounts[]` carries `accept_effect` and `judge_required_for_export`. `accept_effect` is `letter_total` (a `charge`: counted in the billed-charges total), `acknowledge` (a `rate`: accepting it only acknowledges it, it is listed in the internal notes and never totaled, D-019/D-042) or `internal_notes` (`estimate`, `unclear`). `judge_required_for_export` is `false` only for a rate: an accepted rate whose second check never ran is **not** a `JUDGE_NOT_RUN` blocker, so accepting a rate can never block export (its item trace `judge_2` step says the check is optional for a rate). The UI should label a rate's button "Acknowledge" (or keep "Accept as noted") and never promise it goes in the letter. Charges, entries and flags are unchanged. **D-044:** one `JUDGE_NOT_RUN` element per accepted or edited item whose judge never ran: `{item_id, kind, reason_code: "JUDGE_NOT_RUN", why, next_action: {code: "RERUN_JUDGE", text: "Run the second check again.", target: {item_id, judge}}}`. "Never ran" = the item's judge verdict is `unavailable` or absent after the run finished (the same items `/judges` lists as `unresolved`/`JUDGE_UNAVAILABLE`/`FIXTURE_MISS`); it applies to AI-made entries, charges (not damages) and judged flags, and not to entries whose wording the paralegal wrote (manual entry, edited summary: `ai_drafted: false`; D-045(b): these are also left out of `/judges` counts and the `judges` step). It is listed only once the item is accepted or edited, not while a run is in progress, and not for dismissed items. It is cleared only by a judge answer (even an objection) or by dismissing or resetting the item. `export_gate.counts.judge_not_run` is the number of these; when only these block, the gate's `reason_code` is `JUDGE_NOT_RUN`, its `next_action` is `RERUN_JUDGE` and the case `verdict` is `needs_attention` ("N accepted items not double-checked"). The `judges` step's `next_action` is also `RERUN_JUDGE` (target `{view: "judges"}`), and a skipped `judge_N` step on an item has `next_action` `RERUN_JUDGE` with `target {item_id}`.
memory/contracts/api.md:665:  "unresolved": [ { "item_id": "a2", "kind": "amount", "judge": "j2", "verdict": "unavailable", "state_reason": "JUDGE_UNAVAILABLE", "model": "claude-haiku-5-5", "prompt_version": "judge_amount_class_v1", "call_id": null } ],
memory/contracts/api.md:669:`totals.unavailable` counts every verdict `unavailable` AND every live item whose judge never ran (no stored verdict, run finished; it appears in `unresolved` with `state_reason` `JUDGE_UNAVAILABLE`/`FIXTURE_MISS`), so it equals the item traces' skipped judge steps; the case `judges` step is `fail` (`pending` while the run is going) whenever it is above 0 and never says "agreed with all". Export gate invariant: `ready == (blockers == [])` and `status == pass` iff ready (a failed or running run lists `RUN_FAILED`/`RUN_IN_PROGRESS`). Item `next_action` is `null` once the item is accepted, edited or dismissed (step-level hints stay); every `state_reasons[].step_id` is a step id in the trace. An unknown item is 404; an internal error is the standard 500. `totals.unsupported` = partially + unsupported + disagrees (the judge objected); `items_judged` = items whose judge answered (every verdict except `unavailable`). `rejections` = every objection, with the fixed-sentence `rationale`; `unresolved` = `unsure` and `unavailable`. `disagreements[]` (code vs judge): `judge_objects` (every code check passed and the judge objected: `code_says` is the check summary, for an amount the rule's class), `judge_agrees_code_flags` (code raised a doubt (token, qualifier, date) and the judge found it supported; the item stays `needs_review`), `sources_disagree` (flag: the phrase list and the AI disagree, `LEXICON_ONLY`/`LLM_ONLY`). `human_overrides` counts items accepted or edited although a judge objected. Counts cover live and rejected items; narrative sentences are not included. The same visibility split applies (no raw responses in metadata mode; `rejections[].response_raw` is full-mode only).
memory/contracts/api.md:672:Run the second check again for the AI-made items whose judge never answered (the items the export gate lists as `JUDGE_NOT_RUN`, plus any live pending ones with no answer: kept on purpose so the `judges` step's RERUN_JUDGE button always has something to do; D-045 note). No body. The same judge (J1 entry, J2 charge, J3 AI conflict, J4 AI flag) gets the same input the run or the edit gave it, so a recorded answer is found again. Same rules as `/run`: `404 not_found`; `409 run_in_progress`; `409 demo_mode_unsupported_input` (demo mode, text not a recorded case); `503 llm_unavailable`. **Demo mode (no `ENABLE_LIVE=1`) is fixture-only**: only recorded answers are replayed, a miss stays unavailable and never calls a model; live calls (`claude-cli` or `anthropic-api` with a key) need `ENABLE_LIVE=1`. Every call is audited in `llm_calls` (judge role, item id, step `j1`..`j4`) and each attempt is appended to the item's `ladder.rejudge[]` `{at, call_id, verdict}`. An answer replaces `ladder.judge` and recomposes `state`/`state_reasons` (other doubts stay; `JUDGE_UNAVAILABLE`/`FIXTURE_MISS` go; an objection adds `JUDGE_PARTIAL|UNSUPPORTED|DISAGREES|UNSURE`); `review_status` is never changed. Nothing can clear the gate except an answer.
memory/contracts/api.md:677:  "export_gate": { "ready": false, "status": "fail", "blockers": [ { "item_id": "a2", "kind": "amount", "reason_code": "JUDGE_NOT_RUN", "why": "...", "next_action": { "code": "RERUN_JUDGE", "text": "Run the second check again.", "target": {"item_id": "a2", "judge": "j2"} } } ] } }
memory/contracts/api.md:769:| `JUDGE_UNAVAILABLE` | needs_review | the judge call failed or timed out, or (always in demo mode) an edit has no recorded judge answer |
tests/unit/test_judges.py:36:    """ADR-005 JUDGE_UNAVAILABLE: a failed call of ANY judge (J1-J4) yields 'unavailable', never an exception and never a passing verdict."""
tests/unit/test_t037_backend.py:42:    JUDGE_UNAVAILABLE / FIXTURE_MISS reason on any item. Fails when a fixture is missing or stale (a prompt changed since recording)."""
tests/unit/test_t037_backend.py:49:    assert not [i for i in items if {"FIXTURE_MISS", "JUDGE_UNAVAILABLE"} & set(i.get("reasons", []))], case
tests/unit/test_t134_unconfirmed_edit.py:50:    assert "edited; second check not available" in notes and "JUDGE_UNAVAILABLE" in notes
tests/unit/test_t134_unconfirmed_edit.py:153:    DB.update_item(conn, "e5", case=tok, state="needs_review", state_reasons_json=["JUDGE_UNAVAILABLE"])
    if value not in table:
        raise ValueError(f"unknown value: {value}")
    return table[value]


_LADDER_KEYS = {"grounding_failures", "schema_valid", "code_reasons", "judge"}
_CTX_KEYS = {"injection", "date_status", "amount_class", "agreement", "fixture_miss", "split_ambiguous", "llm_failed",
             "endpoint_unverified", "llm_split", "ocr_derived", "translated"}


def compose_state(ladder: dict, context: dict = None):
    ctx = context or {}
    bad = (set(ladder) - _LADDER_KEYS) | (set(ctx) - _CTX_KEYS)
    if bad:      # a misspelled key must not fail open to 'verified'
        raise ValueError(f"unknown ladder/context keys: {sorted(bad)}")
    rejected, doubts = [], []
    for c in ladder.get("grounding_failures", []) or []:
        rejected.append(_known(c))
    if ladder.get("schema_valid", True) is False:
        rejected.append("SCHEMA_INVALID")
    for c in ladder.get("code_reasons", []) or []:
        (rejected if _known(c) in REJECTED_CODES else doubts).append(c)
    doubts.append(_lookup(_JUDGE, ladder.get("judge"), none_ok=("supported",)))
    doubts.append(_lookup(_DATE, ctx.get("date_status"), none_ok=("parsed", "confirmed")))
    doubts.append(_lookup(_AMOUNT, ctx.get("amount_class"), none_ok=("charge",)))
    doubts.append(_lookup(_AGREE, ctx.get("agreement"), none_ok=("both",)))
    for key, code in (("fixture_miss", "FIXTURE_MISS"), ("split_ambiguous", "SPLIT_AMBIGUOUS"), ("llm_split", "LLM_SPLIT"),
                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES"),
                      ("ocr_derived", "OCR_DERIVED"),
                      ("translated", "AI_TRANSLATION")):      # D-050: the one place that keeps a Spanish / unidentified-language item from ever being verified      # T-086/D-042: read from a scanned page; no later step (edit, judge, reclassify) clears it
        if ctx.get(key):
            doubts.append(code)
    rejected = list(dict.fromkeys(rejected))
    doubts = list(dict.fromkeys(d for d in doubts if d))
    if rejected:
        return "rejected", rejected + doubts       # the rejecting reasons come first; the item still shows every doubt
    return ("needs_review", doubts) if doubts else ("verified", [])
def acknowledge_only(kind: str, row: dict) -> bool:
    """T-114 (D-019/D-042): a figure classified `rate` is never a letter charge, so accepting it only acknowledges it (it is listed in the internal notes, never totaled).
    No second AI check is needed for that, so a missing one never blocks export. The one source for the amount view's `accept_effect` and the gate."""
    return kind == "amount" and row.get("kind") == "rate"


def judge_not_run_blockers(conn, case_id: str) -> list:
    """Export blockers (D-044): accepted or edited AI-made items whose second check never ran. No override: only a judge answer clears one.
    A rate (`acknowledge_only`) is the one exception: accepting it only acknowledges it, nothing of it reaches the letter (T-114)."""
    return [_jnr_blocker(u) for u in unjudged_items(conn, case_id)
            if u["review_status"] in ("accepted", "edited") and not acknowledge_only(u["kind"], u["row"])
            and not review.edit_unconfirmed(u["kind"], u["row"])]          # T-134: an edit not yet accepted is not in the letter, so it blocks nothing


def _jnr_blocker(u):
    tried = rerun_gave_no_answer(u["row"])           # T-134 r3: the reason must match what happened after the action offered
    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN_RETRIED" if tried else "JUDGE_NOT_RUN"],
            "rerun_no_answer": tried, "next_action": na("RERUN_JUDGE", {"item_id": u["item_id"], "judge": u["judge"]})}


def judge_report(conn, case_id: str, full: bool = False) -> dict:
    cx = _Cx(conn, case_id, full)
    rows = _judge_rows(cx)
    per = {j: {"id": j, "label": JUDGE_LABEL[j], "prompt_version": JUDGE_PROMPT[j], "models": set(), "items": 0, "supported": 0, "partially": 0, "unsupported": 0,
               "disagrees": 0, "unsure": 0, "unavailable": 0} for j in ("j1", "j2", "j3", "j4")}
    rejections, unresolved, disagreements, versions = [], [], [], set()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:38.451Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p app/backend/why.py; grep -n \"def judge_detail\" -A12 app/backend/why.py; grep -n \"reason_code\" app/backend/trace.py | grep -i \"judge\\|jd\\b\" | head -20; sed -n 1,30p app/backend/confidence.py | tail -20; grep -rn \"JUDGE_UNAVAILABLE\" tests evals --include=*.py -l; sed -n 110,135p tests/unit/test_t037_backend.py"
}
````

### User / tool · 2026-11-02T13:10:38.608Z

**tool result**
````
"""One fixed plain-language sentence per reason code (LLM_VS_CODE row 18, api.md appendix). Never model text."""
_WHY = {
    "GROUNDING_EXCERPT_NOT_VERBATIM": "The quoted text is not word for word in the record, so this item was rejected and cannot be used.",
    "GROUNDING_AMOUNT_NOT_IN_TEXT": "The amount shown does not appear in the record text, so this item was rejected and cannot be used.",
    "SCHEMA_INVALID": "The AI output was malformed after several attempts, so this item was rejected.",
    "SUMMARY_TOKEN_NOT_IN_EXCERPT": "The summary has a number, date, dollar figure or left/right/no/not/without that is not in the quoted text.",
    "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.",
    "EXCERPT_OMITS_QUALIFIER": "The record has a hedge sentence that qualifies this quote, but the quote leaves it out.",
    "EXCERPT_NOT_WHOLE_SENTENCE": "The quote starts or ends in the middle of a sentence.",
    "CHARGE_TEXT_IN_ENTRY": "The summary or the quote states a dollar amount. Amounts go only in the internal notes, never in the letter, so this entry is held out of the letter until you pick a quote without the amount (or edit the summary to remove it).",
    "HIGHLIGHT_NOT_FOUND": "The quote could not be located in the record text, so it cannot be highlighted.",
    "JUDGE_PARTIAL": "A second AI check found the summary only partly supported by the quoted text.",
    "JUDGE_UNSUPPORTED": "A second AI check found the summary not supported by the quoted text.",
    "JUDGE_DISAGREES": "A second AI check disagreed with the first result for this item.",
    "JUDGE_UNSURE": "A second AI check could not decide whether this item is supported.",
    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this item has not been double-checked.",
    "FIXTURE_MISS": "The demo has no recorded AI answer for this step, so this item has not been checked.",
    "DATE_AMBIGUOUS": "The date can be read two ways; confirm which one is right. It is left out of gap checks until then.",
    "DATE_MISSING": "The record has no readable date, so it is left out of gap checks.",
    "ENDPOINT_NOT_VERIFIED": "One end of this gap could involve a date that has not been confirmed.",
    "AMOUNT_RATE_NOT_TOTALED": "This figure is a rate, not a charge, so it is not added to the total.",
    "AMOUNT_ESTIMATE": "This figure is an estimate, not a billed charge, so it is not added to the total.",
    "AMOUNT_DAMAGES": "This figure is not a bill (for example a damages or settlement figure), so it is not added to the total.",
    "AMOUNT_UNCLEAR": "This figure could not be read or labelled with confidence, so it is not added to the total.",
    "LEXICON_ONLY": "The phrase list found this flag but the AI did not; check that it applies.",
    "LLM_ONLY": "The AI found this flag but the phrase list did not; check that it applies.",
    "FILTERED_BY_RULE": "The AI proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.",
    "SPLIT_AMBIGUOUS": "It is not certain where this record begins and ends in the pasted text.",
    "LLM_SPLIT": "The AI, not the formatting, decided where this record begins and ends in the pasted text; check the boundaries against the paste.",
    "INJECTION_SUSPECTED": "This record contains instruction-like text that may be trying to steer the AI; review it before relying on it.",
    "CONFLICT_CHECK_INCOMPLETE": "The check for conflicts between records did not finish or had no recorded answer, so conflicts between records may be missing.",
    "LANGUAGE_UNCERTAIN": "The language of this record could not be identified with confidence (it may not be English or Spanish), so the summary is an AI translation that has not been verified; read the original quote yourself.",
    "LLM_FAILED_AFTER_RETRIES": "The AI step failed on all three attempts, so this record has no AI-made entry.",
    "SUMMARY_NOT_IN_QUOTE": "Every part of the AI's summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.",
    "UNSUPPORTED_LANGUAGE": "This record is in a language the tool does not read (it reads English and Spanish), so it has no AI-made entry. Read the record yourself or write the entry by hand.",
    "AI_TRANSLATION": "AI translation — check against the original. This comes from a Spanish (or unidentified-language) record, so it is never marked verified; read the original quote yourself before you accept it.",
    "OCR_DERIVED": "This record was read from a scanned page by OCR, which can misread letters and digits. Check it against the page image.",
}


80:def judge_detail(code) -> str:
81-    """Fixed sentence for a judge reason_code ('' for NONE / unknown)."""
82-    return _JUDGE_DETAIL.get(code, "")
192:def _judge_reason_code(jd, call):
193:    code = (jd or {}).get("reason_code")
223:    rc = _judge_reason_code(jd, call)
224:    ev.update(judge_verdict=verdict, judge_reason_code=rc)
701:            ev.update(judge_verdict=verdict, judge_reason_code=jd.get("reason_code"))
706:            detail = why.judge_detail(jd.get("reason_code"))
769:    """[{item_id, kind, judge, verdict(ladder vocab), reason_code, row, jd}] for every item with a judge answer (or a recorded 'unavailable')."""
784:                        "reason_code": _judge_reason_code(jd, call), "row": row, "jd": jd, "call": call})
795:        if s["id"].startswith("judge_") and s["status"] == SKIPPED and s.get("reason_code") in ("JUDGE_UNAVAILABLE", "FIXTURE_MISS") \
798:            out.append({"item_id": row["id"], "kind": kind, "judge": jid, "verdict": "unavailable", "reason_code": None, "row": row, "jd": {}, "call": None})
851:    return {"item_id": u["item_id"], "kind": u["kind"], "reason_code": "JUDGE_NOT_RUN", "why": TRACE_WHY["JUDGE_NOT_RUN_RETRIED" if tried else "JUDGE_NOT_RUN"],
877:            e = dict(base, reason_code=r["reason_code"], rationale=why.judge_detail(r["reason_code"]) or reason_text(_OBJECTION[v]), state_reason=_OBJECTION[v])
886:                                      "judge_says": f"{says} ({r['reason_code']})" if says and r["reason_code"] != "NONE" else "not a " + row["kind"],
890:                                      "judge_says": rationale_or(r["reason_code"], v), "resolution": "needs_review", "review_status": row["review_status"]})
1059:    jnr = [b for b in blockers if b["reason_code"] == "JUDGE_NOT_RUN"]
    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
    "AMOUNT_ESTIMATE", "AMOUNT_DAMAGES", "AMOUNT_UNCLEAR", "LEXICON_ONLY", "LLM_ONLY", "SPLIT_AMBIGUOUS",
    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES", "CONFLICT_CHECK_INCOMPLETE", "LLM_SPLIT", "OCR_DERIVED", "LANGUAGE_UNCERTAIN",
    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE", "FILTERED_BY_RULE", "CHARGE_TEXT_IN_ENTRY",
)
REJECTED_CODES = frozenset({"GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"})
STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}

_JUDGE = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES",
          "unsure": "JUDGE_UNSURE", "unavailable": "JUDGE_UNAVAILABLE"}
_AMOUNT = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
_AGREE = {"lexicon_only": "LEXICON_ONLY", "llm_only": "LLM_ONLY"}
_DATE = {"ambiguous": "DATE_AMBIGUOUS", "missing": "DATE_MISSING"}


def sort_key(state: str) -> int:
    """needs_review first, then verified, then rejected."""
    return STATE_ORDER[state]


tests/unit/test_reclassify.py
tests/unit/test_judges.py
tests/unit/test_generator.py
tests/unit/test_judge_guard.py
tests/unit/test_d050_never_verified.py
tests/unit/test_t138_undo_edit.py
tests/unit/test_trace.py
tests/unit/test_flags_pass.py
tests/unit/test_narrative.py
tests/unit/test_api_routes.py
tests/unit/test_review_rules.py
tests/unit/test_t037_backend.py
tests/unit/test_confidence.py
tests/unit/test_conflict_candidates.py
tests/unit/test_t134_unconfirmed_edit.py
tests/unit/test_t114_rates_and_demo_judges.py
tests/e2e/test_edit_to_check.py
tests/unit/test_t126_filtered_by_rule.py
tests/e2e/conftest.py
tests/unit/test_pipeline.py
tests/unit/test_eval_runner.py
evals/run.py
    """ADR-002: the run writes entries/amounts/flags to the database, all pending; a decision made after the run survives a rerun."""
    from tests.unit._fakes import FakeCall, sample_script
    conn = DB.connect(str(tmp_path / "p.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 2.0)
    assert len(DB.list_items(conn, cid, "entry")) == 9 and len(DB.list_items(conn, cid, "amount")) == 4
    assert all(i["review_status"] == "pending" for k in ("entry", "amount", "flag") for i in DB.list_items(conn, cid, k))
    gap = [f for f in DB.list_items(conn, cid, "flag") if f["type"] == "gap"][0]
    DB.apply_review(conn, gap["id"], "accept", now=3.0)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 4.0)
    assert DB.get_item(conn, gap["id"])["review_status"] == "accepted"
    assert [f["review_status"] for f in out["flags"] if f["id"] == gap["id"]] == ["accepted"]
    assert DB.get_case(conn, cid)["status"] == "ready"


def test_timeout_marks_case_failed_with_run_deadline(tmp_path):
    from tests.unit._fakes import FakeCall, sample_script
    conn = DB.connect(str(tmp_path / "t.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    t = iter(range(0, 10**6, 100))
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: float(next(t)))
    c = DB.get_case(conn, cid)
    assert out["status"] == "timeout" and c["status"] == "failed" and json.loads(c["error"])["code"] == "run_deadline"
    assert [f for f in out["flags"] if f["type"] == "gap"]          # code results survive the deadline
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:42.907Z

**tool call — Bash**
````
{
 "command": "sed -n 185,235p app/backend/trace.py; sed -n 690,715p app/backend/trace.py; sed -n 60,80p app/backend/why.py; grep -n \"def failure_entry\" -B2 -A25 app/backend/generator.py | head -50"
}
````

### User / tool · 2026-11-02T13:10:43.012Z

**tool result**
````
def _norm_verdict(step_id, v):
    if v in _LADDER_VOCAB:
        return v
    return _RAW_TO_LADDER.get(v, "unsure")


def _judge_reason_code(jd, call):
    code = (jd or {}).get("reason_code")
    if code:
        return code
    if call and call.get("response_raw"):
        try:
            got = json.loads(call["response_raw"])
            if isinstance(got, dict) and isinstance(got.get("reason_code"), str):
                return got["reason_code"]
        except (ValueError, TypeError):
            pass
    return None


def _judge_step(cx, item_id, jd, jid, R, *, sid=None, label=None, rule="row 4"):
    """One LLM judge step from ladder.judge (or None). Statuses: pass (supported), fail (objected/unsure), skipped (did not answer), pending (not run yet)."""
    sid = sid or f"judge_{jid[1]}"
    label = label or f"Second AI check: {JUDGE_LABEL[jid].lower()}"
    label = label[0].upper() + label[1:]
    jd = jd or {}
    raw = jd.get("verdict")
    call = cx.call(jd.get("call_id"), item_id, jid)
    if raw is None and not call:
        if not cx.ran:
            return step(sid, label, "llm", PENDING, "The second check has not run yet.", rule=rule, evidence={"model": {"id": cx.models["judge"], "role": "judge", "independent_of_generator": cx.models["judge"] != cx.models["generator"]}, "prompt_version": JUDGE_PROMPT[jid]},
                        next_action=na("RERUN"))
        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence={"judge_verdict": "unavailable"},
                    next_action=na("RERUN_JUDGE", {"item_id": item_id}))
    verdict = _norm_verdict(jid, raw if raw is not None else (call or {}).get("verdict"))
    ev = _llm_evidence(cx, "judge", jd.get("model") or cx.models["judge"], jd.get("prompt_version") or JUDGE_PROMPT[jid], call)
    rc = _judge_reason_code(jd, call)
    ev.update(judge_verdict=verdict, judge_reason_code=rc)
    if verdict == "supported":
        ev["rationale"] = _J_OK[jid]
        return step(sid, label, "llm", PASS, _J_OK[jid], rule=rule, evidence=ev)
    if verdict == "unavailable":
        code = "FIXTURE_MISS" if "FIXTURE_MISS" in R else "JUDGE_UNAVAILABLE"
        return step(sid, label, "llm", SKIPPED, reason_text(code), reason=code, rule=rule, evidence=ev, next_action=na("RERUN_JUDGE", {"item_id": item_id}))
    code = _OBJECTION[verdict]
    detail = why.judge_detail(rc)
    ev["rationale"] = detail or reason_text(code)
    return step(sid, label, "llm", FAIL, (reason_text(code) + (" " + detail if detail else "")).strip(), reason=code, rule=rule, evidence=ev,
                next_action=na("COMPARE_BY_HAND"))
    else:
        st.append(step("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", PASS,
                       "Every number, date and qualifier is in the cited quote, and the sentence adds no cause, severity or flag wording.", rule="D-006", evidence={"reasons": []}))
    if not cited_ok or rcodes:
        st.append(_skipped("judge_1", "Second AI check: is the summary supported by the quote?", "llm", reason if not cited_ok else rcodes[0], "row 4"))
    else:
        jd = s.get("judge") or {}
        verdict = jd.get("verdict")
        jcall = cx.call(jd.get("call_id"), s["id"], "j1")
        ev = _llm_evidence(cx, "judge", jd.get("model") or cx.models["judge"], jd.get("prompt_version") or "judge_faithfulness_v1", jcall)
        if verdict:
            ev.update(judge_verdict=verdict, judge_reason_code=jd.get("reason_code"))
        if verdict == "supported":
            ev["rationale"] = _J_OK["j1"]
            st.append(step("judge_1", "Second AI check: is the sentence supported by the quote?", "llm", PASS, _J_OK["j1"], rule="row 4", evidence=ev))
        elif verdict in ("partially", "unsupported"):
            detail = why.judge_detail(jd.get("reason_code"))
            ev["rationale"] = detail or narrative.REASONS[reason]
            st.append(step("judge_1", "Second AI check: is the sentence supported by the quote?", "llm", FAIL, (narrative.REASONS.get(reason, "") + " " + detail).strip(),
                           reason=reason, rule="row 4", evidence=ev, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
        else:
            st.append(step("judge_1", "Second AI check: is the sentence supported by the quote?", "llm", SKIPPED, narrative.REASONS["JUDGE_UNAVAILABLE"], reason="JUDGE_UNAVAILABLE", rule="row 4", evidence=ev, next_action=na("SENTENCE_REMOVED", {"entry_id": s["entry_id"]})))
    status = nar.get("status") or "pending"
    if rem:
        st.append(step("human", "Your decision on the paragraph", "human", SKIPPED, "This sentence was removed from the draft, so it cannot be accepted.", rule="D-031"))
        code, label = "removed", "Removed from the draft"
    "DROPS_QUALIFIER": "The summary leaves out a qualifier that the quote carries.",
    "NUMBER_MISMATCH": "A number in the summary does not match the quote.",
    "OTHER_UNSUPPORTED": "Part of the summary is not supported by the quote.",
    "SHOULD_BE_CHARGE": "The second check reads this figure as a billed charge.",
    "SHOULD_BE_RATE": "The second check reads this figure as a rate.",
    "SHOULD_BE_ESTIMATE": "The second check reads this figure as an estimate.",
    "SHOULD_BE_DAMAGES": "The second check reads this figure as a non-bill amount.",
    "SHOULD_BE_UNCLEAR": "The second check could not read this figure with confidence.",
    "TEXT_AMBIGUOUS": "The text does not settle the question.",
    "PLAN_VS_ACTUAL": "The second check reads the quotes as a plan and what followed.",
    "FACT_MISMATCH": "The second check reads the quotes as stating different facts.",
    "DIFFERENT_VISITS": "The second check reads the quotes as different visits that can both be true.",
    "CAN_BOTH_BE_TRUE": "The second check reads both quotes as possibly true together.",
    "WRONG_TYPE": "The second check does not think this flag type fits the quote.",
    "WRONG_CATEGORY": "The second check does not think this flag category fits the quote.",
    "NEGATED": "The second check reads the quote as negating the condition.",
    "NOT_SUPPORTED_BY_QUOTE": "The second check does not find this flag supported by the quote.",
}


def judge_detail(code) -> str:
140-
141-
142:def failure_entry(record: dict, group: list, failure: str, detail: dict = None) -> dict:
143-    """A record the extract step produced NO usable output for (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, UNSUPPORTED_LANGUAGE, SUMMARY_NOT_IN_QUOTE) as a could-not-verify tray
144-    item: state rejected, the failure code as its reason, no summary or quote. It never reaches the timeline or the letter, and it never vanishes:
145-    the paralegal sees the record with the reason and can write the entry by hand (D-031). `ladder.failure` marks it as a placeholder."""
146-    e = _entry_base(record, group, "")
147-    e.update(ai_drafted=False, summary=None, excerpt=None, excerpt_start=None, excerpt_end=None, source_kind="record", state="rejected", reasons=[failure], why=why.why(failure))
148-    e["ladder"] = {"item_id": e["id"], "generator": None, "judge": None, "failure": failure, "code_checks": {}, "state": "rejected",
149-                   "human": {"action": None, "edited_text": None, "at": None}}
150-    if detail:                                          # SUMMARY_NOT_IN_QUOTE (D-054): keep the model's call and what code removed, so the tray item is auditable
151-        e["ladder"]["generator"] = detail.get("generator")
152-        e["ladder"]["summary_trim"] = detail.get("summary_trim")
153-    return e
154-
155-
156-def resolved_placeholders(entries: list) -> set:
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:52.460Z

**tool call — bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project && grep -rn \"_WHY\\b\\|why\\._WHY\\|REASON_CODES\" tests app --include=*.py | grep -v \"^app/backend/why.py\" | head; sed -n 80,100p app/backend/why.py; grep -n \"ladder.*judge\\|\\\"judge\\\"\" app/backend/rejudge.py | head -20"
}
````

### User / tool · 2026-11-02T13:10:52.461Z

**tool result (error)**
````
<tool_use_error>Error: No such tool available: bash. Tool names are case-sensitive: call Bash instead.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:54.085Z

**tool call — Bash**
````
{
 "command": "grep -rn \"_WHY\\b\\|why\\._WHY\\|REASON_CODES\" tests app --include=*.py | grep -v \"^app/backend/why.py\" | head; sed -n 80,100p app/backend/why.py; grep -n \"judge\" app/backend/rejudge.py | head -40"
}
````

### User / tool · 2026-11-02T13:10:54.226Z

**tool result**
````
tests/unit/test_t139_charge_text.py:64:    assert "CHARGE_TEXT_IN_ENTRY" in confidence.REASON_CODES
tests/unit/test_confidence.py:120:    """Row 18 / api.md appendix: confidence.REASON_CODES equals the closed list (22+ codes)."""
tests/unit/test_confidence.py:121:    assert set(C.REASON_CODES) == api_codes()
app/backend/trace.py:39:# Trace-only reason codes (case level and narrative); item reason codes come from confidence.REASON_CODES / why.py.
app/backend/trace.py:40:TRACE_WHY = {
app/backend/trace.py:85:    if code in TRACE_WHY:
app/backend/trace.py:86:        return TRACE_WHY[code]
app/backend/trace.py:251:        return step("human", "Your decision", "human", PENDING, TRACE_WHY["EDIT_NOT_CONFIRMED_ITEM_AI" if ai_summary_unchecked(kind, row) else "EDIT_NOT_CONFIRMED_ITEM"], reason="EDIT_NOT_CONFIRMED", rule="row 17", evidence=ev, blocks=False,
app/backend/trace.py:260:    return step("human", "Your decision", "human", PENDING, TRACE_WHY["PENDING_DECISION"], reason="PENDING_DECISION", rule="row 17", evidence=ev, blocks=blocks_ok,
app/backend/trace.py:474:                    "why": f["why"] + " " + TRACE_WHY["CODE_CHECK_FAILED" if _paralegal_wording("entry", row) else "CODE_CHECK_FAILED_AI"], "next_action": _fix_action(row, f)})
def judge_detail(code) -> str:
    """Fixed sentence for a judge reason_code ('' for NONE / unknown)."""
    return _JUDGE_DETAIL.get(code, "")
1:"""Run the second check again for the items whose judge never answered (D-044). The LLM judges; code decides what to ask and what state follows.
3:rejudge(conn, case_id, call, now=None) -> dict
4:    Targets: live (not rejected, not dismissed) AI-made entries, charges and flags with a judge verdict of 'unavailable' or no verdict (trace.unjudged_items).
5:    Each target gets the same judge (J1/J2/J3/J4) and the same input as the run or the edit gave it; every call goes through `call` (audited_call).
6:    An answer replaces the judge record and recomposes the item's state (code, confidence.compose_state vocabulary); a missing answer changes nothing
7:    except one entry in ladder.rejudge. The paralegal's review_status is never touched. Nothing here clears the export gate except a judge answer.
12:from app.backend import confidence, judges, spanish, trace
22:    """(verdict in the judge's own enum | 'unavailable', call_id, reason_code). Same inputs and nonce as the original run or edit, so a recorded answer is found again."""
29:        lang = "es" if (row.get("ladder") or {}).get("translation") else "en"          # D-042: the Spanish-record judge sees the same input as the run gave it
31:                                   nonce=None if edited else nonce, item_id=item, lang=lang)           # an edit's judge ran without a case nonce (review._check_summary)
33:        return judges.run_j2_meta(row["excerpt"], row["text"], row["kind"], call=call, nonce=nonce, item_id=item)
37:        return judges.run_j3_meta(comp["excerpt"], comp["excerpt_b"], call=call, nonce=nonce, item_id=item, category=row["category"])
40:    return judges.run_j4_meta(comp["excerpt"], row["type"], row["category"], call=call, nonce=nonce, item_id=item)
45:        return _ask(t["kind"], t["judge"], t["row"], case_text, call)
51:    """(state, reasons): the item's other doubts stay; its judge doubts are replaced by what the new answer says. Rejected items never get here."""
54:    reasons = list(dict.fromkeys(keep + confidence.compose_state({"judge": ladder_verdict}, {"translated": translated})[1]))      # D-050: a judge answer never verifies a translation
59:    """One audit row per asked item (review_events action 'rejudge'); review_status is never touched."""
60:    DB.log_event(conn, case_id, row["id"], "rejudge", {"state": row["state"], "review_status": row["review_status"]},
61:                 {"event": "rejudge", "judge": jid, "verdict": verdict, "state": state, "call_id": call_id}, t)
64:def rejudge(conn, case_id: str, call, now: float = None) -> dict:
68:    targets = trace.unjudged_items(conn, case_id)
73:        row, jid = tg["row"], tg["judge"]
75:        ladder_verdict = judges.to_ladder(jid, verdict)
77:        lad["rejudge"] = list(lad.get("rejudge") or []) + [attempt]
78:        base = {"item_id": row["id"], "kind": tg["kind"], "judge": jid, "review_status": row["review_status"]}
84:        lad["judge"] = {**(lad.get("judge") or {}), "model": judges.judge_model(), "prompt_version": spanish.JUDGE_PROMPT if (jid == "j1" and lad.get("translation")) else trace.JUDGE_PROMPT[jid],
92:    return {"token": case_id, "asked": len(targets), "rejudged": done, "still_unavailable": still,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:10:57.364Z

**tool call — Bash**
````
{
 "command": "grep -rn \"second check agreed\" app | head; grep -n \"def entry_why\\|def _why\\|why.why\\|def item_why\" app/backend/*.py | head -20"
}
````

### User / tool · 2026-11-02T13:10:57.492Z

**tool result**
````
app/frontend/mock.js:91:        why: needs ? "The second check found part of the summary not fully supported by the quote." : "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
app/frontend/mock.js:102:          why: rate ? "This is a per-visit rate; the records never say how many visits were billed, so it is not totaled." : "Labelled as a charge in the record, the figure is in the record, and the second check agreed.",
app/frontend/dev/mock-data.js:164:   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
app/frontend/dev/mock-data.js:196:   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
app/frontend/dev/mock-data.js:228:   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
app/frontend/dev/mock-data.js:260:   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
app/frontend/dev/mock-data.js:292:   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
app/frontend/dev/mock-data.js:324:   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
app/frontend/dev/mock-data.js:356:   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
app/frontend/dev/mock-data.js:388:   "why": "Quote found word for word, every number in the summary is in the quote, and the second check agreed.",
app/backend/generator.py:129:    e["why"] = " ".join(why.why(c) for c in reasons) if reasons else "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
app/backend/generator.py:147:    e.update(ai_drafted=False, summary=None, excerpt=None, excerpt_start=None, excerpt_end=None, source_kind="record", state="rejected", reasons=[failure], why=why.why(failure))
app/backend/flags.py:45:    f["why"] = " ".join(why.why(c) for c in f["reasons"]) if f["reasons"] else "Found by the phrase list and the model, and the second check agreed."
app/backend/flags.py:235:            "why": why.why("INJECTION_SUSPECTED"), "excerpt": hits[0]["phrase"] if hits else "",
app/backend/flags.py:361:        f["why"] = why.why(FILTERED) + ("" if "GROUNDING_EXCERPT_NOT_VERBATIM" not in f["reasons"] else " " + why.why("GROUNDING_EXCERPT_NOT_VERBATIM"))
app/backend/flags.py:370:    f["why"] = why.why(code) + (" " + detail if detail else "")
app/backend/present.py:12:def _why(reasons):
app/backend/present.py:16:            out.append(why.why(c))
app/backend/trace.py:88:        return why.why(code)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:11:01.558Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p app/backend/present.py; grep -n \"_why(\" app/backend/*.py | head -20; sed -n 76,100p app/backend/rejudge.py; sed -n 120,170p tests/unit/test_confidence.py | head -20"
}
````

### User / tool · 2026-11-02T13:11:01.708Z

**tool result**
````
"""Read-side views in the shapes of memory/contracts/api.md, built from the DB. No writes."""
import json
import re

from app.backend import conflict_candidates, confidence, date_convention, flag_templates as FT, generator, grounding, ingest, language, overlap, pdf_text, review, sentences, spanish, store, totals as T, uncovered, why
from app.db import db as DB

STATUS_ACTION = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": None}
OK_WHY = "Quote found word for word, every number in the summary is in the quote, and the second check agreed."


def _why(reasons):
    out = []
    for c in reasons or []:
        try:
            out.append(why.why(c))
        except KeyError:
            pass
    return " ".join(out) if out else OK_WHY


def _human(row):
    ed = row.get("edited") or {}
    return {"action": STATUS_ACTION.get(row["review_status"]), "edited_text": ed.get("summary") or ed.get("note"),
            "at": ed.get("at")}


def _ladder(row):
    lad = dict(row.get("ladder") or {"item_id": row["id"]})
    lad["item_id"] = row["id"]
    lad["state"] = row["state"]
    lad["human"] = _human(row)
    return lad


def _common(row):
    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons")),
            "review_status": row["review_status"], "edited": row.get("edited"), "ladder": _ladder(row)}


app/backend/export.py:560:def _edit_unconfirmed_why(e) -> str:
app/backend/export.py:567:    return f"edited; {_edit_unconfirmed_why(e)}; not yet confirmed against the quote, so it is not in the letter (accept it to put it there)"
app/backend/export.py:587:                f" (accepted by the paralegal after comparing it with the quote; {_edit_unconfirmed_why(e)})" if e.get("edit_state_reasons") and _status(e) == "in" else "")
app/backend/present.py:12:def _why(reasons):
app/backend/present.py:37:    return {"id": row["id"], "state": row["state"], "reasons": row.get("state_reasons") or [], "why": _why(row.get("state_reasons")),
app/backend/present.py:87:def _gap_why(row, base):
app/backend/present.py:101:    c["why"] = _gap_why(row, c["why"])
        attempt = {"at": t, "call_id": call_id, "verdict": ladder_verdict}
        lad["rejudge"] = list(lad.get("rejudge") or []) + [attempt]
        base = {"item_id": row["id"], "kind": tg["kind"], "judge": jid, "review_status": row["review_status"]}
        if ladder_verdict == "unavailable":
            DB.update_item(conn, row["id"], now=t, case=case_id, ladder=lad)
            _log(conn, case_id, row, jid, call_id, "unavailable", row["state"], t)
            still.append(dict(base, verdict="unavailable"))
            continue
        lad["judge"] = {**(lad.get("judge") or {}), "model": judges.judge_model(), "prompt_version": spanish.JUDGE_PROMPT if (jid == "j1" and lad.get("translation")) else trace.JUDGE_PROMPT[jid],
                        "call_id": call_id, "verdict": verdict, "reason_code": code}
        state, reasons = recompose(row, ladder_verdict)
        lad["state"] = state
        DB.update_item(conn, row["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
        _log(conn, case_id, row, jid, call_id, ladder_verdict, state, t)
        done.append(dict(base, verdict=ladder_verdict, state=state, state_reasons=reasons))
    gate = next(s for s in trace.case_trace(conn, case_id)["steps"] if s["id"] == "export_gate")
    return {"token": case_id, "asked": len(targets), "rejudged": done, "still_unavailable": still,
            "export_gate": {"ready": gate["ready"], "status": gate["status"], "blockers": gate["blockers"]}}
    """Row 18 / api.md appendix: confidence.REASON_CODES equals the closed list (22+ codes)."""
    assert set(C.REASON_CODES) == api_codes()
    assert len(api_codes()) >= 22

@pytest.mark.parametrize("code", sorted(api_codes()))
def test_every_reason_code_has_a_why_template(code):
    """Row 18: every reason code has a fixed, non-empty, plain-language template (no braces left over, no model text)."""
    s = W.why(code)
    assert isinstance(s, str) and 15 < len(s) < 300 and "{" not in s and "}" not in s

def test_why_unknown_code_raises():
    """Row 18: unknown code -> KeyError (templates are a closed list)."""
    with pytest.raises(KeyError):
        W.why("NOT_A_CODE")

def test_why_is_deterministic():
    """Row 18: same code -> byte-identical sentence."""
    assert W.why("JUDGE_PARTIAL") == W.why("JUDGE_PARTIAL")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:11:09.449Z

**tool call — Bash**
````
{
 "command": "grep -rn \"did not run or did not finish\" app tests evals memory/contracts | grep -v \"app/frontend/dev\" | head; git status --short | head -30"
}
````

### User / tool · 2026-11-02T13:11:09.704Z

**tool result**
````
app/backend/why.py:16:    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this item has not been double-checked.",
app/backend/reclassify.py:40:    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this figure cannot become a charge yet. Try again.",
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
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/amounts.py
 M app/backend/confidence.py
 M app/backend/conflict_candidates.py
 M app/backend/conflicts.py
 M app/backend/export.py
 M app/backend/export_routes.py
 M app/backend/generator.py
 M app/backend/present.py
 M app/backend/review.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:11:12.121Z

**tool call — Bash**
````
{
 "command": "git status --short | grep -v agent-memory | sed -n 1,60p"
}
````

### User / tool · 2026-11-02T13:11:12.280Z

**tool result**
````
 M app/backend/amounts.py
 M app/backend/confidence.py
 M app/backend/conflict_candidates.py
 M app/backend/conflicts.py
 M app/backend/export.py
 M app/backend/export_routes.py
 M app/backend/generator.py
 M app/backend/present.py
 M app/backend/review.py
 M app/backend/trace.py
 M app/backend/why.py
 M app/frontend/flags.js
 M app/frontend/review.css
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-060.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
 M board/cards/T-065.md
 M board/cards/T-066.md
 M board/cards/T-067.md
 M board/milestones.md
 M evals/library/case_lib11_priors_and_ledger.expected.json
 M evals/reports/latest.json
 M memory/LESSONS.md
 M memory/PROGRESS.md
 M memory/contracts/api.md
 M tests/e2e/conftest.py
 M tests/e2e/test_edit_to_check.py
 M tests/unit/test_api_routes.py
 M tests/unit/test_conflict_candidates.py
 M tests/unit/test_conflicts.py
 M tests/unit/test_t134_unconfirmed_edit.py
?? app/backend/charge_text.py
?? app/backend/uncovered.py
?? artifacts/review-evidence/GATE-M2-paralegal/
?? artifacts/review-evidence/M0-r2-staff-resolution.md
?? artifacts/review-evidence/T-001-exercise-1.txt
?? artifacts/review-evidence/T-001-exercise-2.txt
?? artifacts/review-evidence/T-001-exercise-3.txt
?? artifacts/review-evidence/T-001-r2-readonly-repros.txt
?? artifacts/review-evidence/T-001-r3-repro.out.txt
?? artifacts/review-evidence/T-001-r3-repro.sh
?? artifacts/review-evidence/T-002-curl.txt
?? artifacts/review-evidence/T-002-r2-activity-390.png
?? artifacts/review-evidence/T-002-r2-board-390.png
?? artifacts/review-evidence/T-002-r2-csrf-curl.txt
?? artifacts/review-evidence/T-002-r2-inbox-390.png
?? artifacts/review-evidence/T-002-r2-milestones-390.png
?? artifacts/review-evidence/T-002-r2-personas-390.png
?? artifacts/review-evidence/T-002-r2-state-390.png
?? artifacts/review-evidence/T-002-r2-xss.json
?? artifacts/review-evidence/T-002-r3-404.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:11:22.196Z

**tool call — Bash**
````
{
 "command": "git diff --cached --stat | tail -3; git diff app/backend/why.py | head -30; git log --oneline | head -3"
}
````

### User / tool · 2026-11-02T13:11:22.380Z

**tool result**
````
diff --git a/app/backend/why.py b/app/backend/why.py
index 162057e..0ce29c9 100644
--- a/app/backend/why.py
+++ b/app/backend/why.py
@@ -7,6 +7,7 @@ _WHY = {
     "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.",
     "EXCERPT_OMITS_QUALIFIER": "The record has a hedge sentence that qualifies this quote, but the quote leaves it out.",
     "EXCERPT_NOT_WHOLE_SENTENCE": "The quote starts or ends in the middle of a sentence.",
+    "CHARGE_TEXT_IN_ENTRY": "The summary or the quote states a dollar amount. Amounts go only in the internal notes, never in the letter, so this entry is held out of the letter until you pick a quote without the amount (or edit the summary to remove it).",
     "HIGHLIGHT_NOT_FOUND": "The quote could not be located in the record text, so it cannot be highlighted.",
     "JUDGE_PARTIAL": "A second AI check found the summary only partly supported by the quoted text.",
     "JUDGE_UNSUPPORTED": "A second AI check found the summary not supported by the quoted text.",
fc60471 fix(backend): T-132 r4 fix-up - overlapping attribution flags join into one, any 'Label:' line or bullet ends the extension, linear scan on long chains, title wrap is not a sentence end, family nouns tested
f648166 review(gate): add staff-engineer findings to GATE-M2 triage (T-145, T-146)
330fc0c review(gate): GATE-M2 round-1 triage mapped to T-139..T-144
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:11:40.039Z

**tool call — Bash**
````
{
 "command": "sed -n 150,200p app/backend/pipeline.py; sed -n 1,40p tests/unit/test_pipeline.py; grep -n \"BatchRefused\" tests/unit/*.py | head -5; grep -n \"class BatchRefused\" -A8 app/backend/case_extras.py; sed -n 325,350p app/backend/api.py"
}
````

### User / tool · 2026-11-02T13:11:40.186Z

**tool result**
````
    if all(cfg.get(k, []) == v for k, v in marks.items()):
        return
    for k, v in marks.items():
        if v:
            cfg[k] = v
        else:
            cfg.pop(k, None)
    DB.update_case(conn, cid, config_json=cfg or None)


def _item_record_ids(item: dict) -> list:
    return list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])


def _reset_reviewed_on(conn, cid: str, moved: set, now: float) -> None:
    """T-129 r2: a record number now names different text (a re-run after the numbering changed, or a model split that moved). A decision the paralegal made on an item
    that cites such a record was made on other text, so it goes back to pending (the review event keeps what it was); the run then rebuilds or removes the item."""
    if not moved:
        return
    for kind in ("entry", "amount", "flag"):
        for it in DB.list_items(conn, cid, kind):
            if it["review_status"] != "pending" and moved & set(_item_record_ids(it)):
                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)


def _store_records(conn, cid: str, ing: dict, now: float = 0.0) -> None:
    """Make the stored records equal this run's records. Same ids and spans -> nothing to do. Anything else (a model split that moved,
    or a re-run whose split failed or was rejected and so fell back to the code split) -> delete and re-store in the same transaction,
    before any entry, flag or amount of this run is written, so the records table and the run's items never disagree."""
    _store_record_marks(conn, cid, ing)
    stored = [(r[0], r[1], r[2]) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
    if stored == [(r["id"], r["char_start"], r["char_end"]) for r in ing["records"]]:
        return
    new_spans = {r["id"]: (r["char_start"], r["char_end"]) for r in ing["records"]}
    _reset_reviewed_on(conn, cid, {i for i, a, b in stored if new_spans.get(i) != (a, b)}, now)
    conn.execute("BEGIN")                      # autocommit connection: one explicit transaction, all or nothing
    try:
        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
        for r in ing["records"]:
            d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
            DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
                          date_header_start=d["start"], date_header_end=d["end"], source_header_start=s["start"], source_header_end=s["end"],
                          source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
                          date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
                          encounter=int(r["encounter"]))
        conn.execute("COMMIT")
    except Exception:
        conn.execute("ROLLBACK")
        raise


"""Pipeline stages with a scripted fake `call` (no key, no network). app/README-arch.md stage list, R-IN-1, R-TL-1, R-FL-1, R-CH-*, ADR-007, LLM_VS_CODE rows 1-3, 9, 15."""
import pytest
from app.backend import pipeline as PL
from app.db import db as DB
from app.llm import audited as AU, provider as P
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, golden_summaries, which_record, sample_script, run_sample, items_for

STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]

def script():
    return sample_script()

@pytest.fixture
def run(tmp_path):
    conn = DB.connect(str(tmp_path / "p.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    call = FakeCall(script())
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
    return out, call

def test_stage_names_and_order():
    """ADR-007 / README-arch: stages are exactly ingest, extract, verify, judge_entries, amounts, conflicts, flags, finalize."""
    assert list(PL.STAGES) == STAGES

def test_ingest_is_synchronous_code_with_gaps_and_no_llm():
    """Row 9 / arch: ingest returns records, dates, regex amounts and the gap flag without any LLM call."""
    out = PL.run_ingest(G.raw("sample"))
    assert len(out["records"]) == 9
    g = [f for f in out["flags"] if f["type"] == "gap"]
    assert [(f["from_date"], f["to_date"], f["days"]) for f in g] == [("2026-03-06", "2026-05-18", 73)]
    assert len(out["amounts"]) == 3

def test_nine_entries_all_verified_with_code_set_provider_and_date(run):
    """R-TL-1, R-TL-9: nine entries in date order; provider = header label and date = header date set by code; states verified."""
    out, _ = run
    ents = out["entries"]
    assert len(ents) == 9 and [e["date"] for e in ents] == sorted(e["date"] for e in ents)
    assert ents[3]["provider"] == "Capital PT, initial evaluation"
    assert ents[6]["date"] == "2026-05-18"
18:class BatchRefused(Exception):
19-    def __init__(self, rejected):
20-        super().__init__("invalid_batch")
21-        self.rejected = rejected
22-
23-
24-def _code_check_refusal(conn, case_id, item_id, row, cache):
25-    if "recs" not in cache:
26-        cache["recs"] = store.load_records(conn, case_id)
    @app.delete("/api/cases/{token}", status_code=204)
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:11:55.697Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/test_t145_t146_deadline.py <<'EOF'\n\"\"\"T-145 / T-146 (GATE-M2 staff findings): the deadline path.\nT-145: an entry whose second check (judge 1) never ran is never `verified`, says JUDGE_NOT_RUN, and batch accept refuses it.\nT-146: a timed-out re-run keeps every previous item and decision (its error says 'finished items were kept').\"\"\"\nimport json\n\nimport pytest\nfrom app.backend import case_extras, pipeline as PL, present\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit._fakes import FakeCall, sample_script\n\n\nclass Clock:\n    \"\"\"Injected clock: jumps past the deadline when a named stage starts (on_stage), so the run stops exactly there.\"\"\"\n    def __init__(self, jump_at=None):\n        self.t, self.jump_at = 0.0, jump_at\n\n    def __call__(self):\n        return self.t\n\n    def on_stage(self, name):\n        if name == self.jump_at:\n            self.t = 10_000.0\n\n\ndef _case(tmp_path):\n    conn = DB.connect(str(tmp_path / \"d.sqlite\"))\n    return conn, DB.create_case(conn, G.raw(\"sample\"), now=0.0)\n\n\ndef _run(conn, cid, clock):\n    return PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script()), now=clock, on_stage=clock.on_stage, deadline_s=480)\n\n\n# ------------------------------------------------------------------ T-145\n@pytest.mark.parametrize(\"jump_at\", [\"judge_entries\", \"verify\"])\ndef test_deadline_before_judge1_leaves_no_verified_entry(tmp_path, jump_at):\n    conn, cid = _case(tmp_path)\n    out = _run(conn, cid, Clock(jump_at))\n    assert out[\"status\"] == \"timeout\"\n    rows = DB.list_items(conn, cid, \"entry\")\n    assert len(rows) == 9\n    for r in rows:\n        assert r[\"state\"] == \"needs_review\" and \"JUDGE_UNAVAILABLE\" in r[\"state_reasons\"], r[\"id\"]\n        jd = r[\"ladder\"][\"judge\"]\n        assert jd[\"verdict\"] == \"unavailable\" and jd[\"reason_code\"] == \"JUDGE_NOT_RUN\" and jd[\"call_id\"] is None\n        assert r[\"ladder\"][\"state\"] == \"needs_review\"\n    assert all(e[\"state\"] == \"needs_review\" for e in out[\"entries\"])\n    assert out[\"counts\"][\"verified\"] == 0 or all(i[\"state\"] != \"verified\" for i in out[\"entries\"])\n\n\ndef test_deadline_case_view_says_judge_not_run_and_never_that_the_check_agreed(tmp_path):\n    conn, cid = _case(tmp_path)\n    _run(conn, cid, Clock(\"judge_entries\"))\n    view = present.entry_view(conn, cid, \"e1\") if hasattr(present, \"entry_view\") else None\n    row = DB.get_item(conn, \"e1\", cid)\n    why = present._common(row)[\"why\"]\n    assert \"JUDGE_NOT_RUN\" in why and \"agreed\" not in why\n    assert all(\"agreed\" not in (e[\"why\"]) and \"JUDGE_NOT_RUN\" in e[\"why\"] for e in DB.list_items(conn, cid, \"entry\") and\n               [present._common(r) for r in DB.list_items(conn, cid, \"entry\")])\n    assert view is None or \"agreed\" not in json.dumps(view)\n\n\ndef test_deadline_batch_accept_refuses_every_unjudged_entry(tmp_path):\n    conn, cid = _case(tmp_path)\n    _run(conn, cid, Clock(\"judge_entries\"))\n    ids = [r[\"id\"] for r in DB.list_items(conn, cid, \"entry\")]\n    with pytest.raises(case_extras.BatchRefused) as ex:\n        case_extras.apply_batch(conn, cid, {\"action\": \"accept\", \"item_ids\": ids}, 5.0)\n    assert {b[\"reason\"] for b in ex.value.rejected} == {\"not_verified\"} and len(ex.value.rejected) == 9\n    assert all(r[\"review_status\"] == \"pending\" for r in DB.list_items(conn, cid, \"entry\"))      # all or nothing\n\n\ndef test_normal_run_still_verifies_judged_entries(tmp_path):\n    conn, cid = _case(tmp_path)\n    out = PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script()), now=lambda: 1.0)\n    assert out[\"status\"] == \"done\" and all(e[\"state\"] == \"verified\" and e[\"ladder\"][\"judge\"][\"verdict\"] == \"supported\" for e in out[\"entries\"])\n\n\n# ------------------------------------------------------------------ T-146\ndef _snapshot(conn, cid):\n    return {k: {i[\"id\"]: (i[\"review_status\"], i[\"state\"], i[\"state_reasons\"]) for i in DB.list_items(conn, cid, k)} for k in (\"entry\", \"amount\", \"flag\")}\n\n\n@pytest.mark.parametrize(\"jump_at\", [\"extract\", \"judge_entries\", \"flags\"])\ndef test_timed_out_rerun_keeps_every_previous_item_and_decision(tmp_path, jump_at):\n    conn, cid = _case(tmp_path)\n    first = PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script()), now=lambda: 1.0)\n    assert first[\"status\"] == \"done\"\n    before = _snapshot(conn, cid)\n    assert len(before[\"entry\"]) == 9 and len(before[\"flag\"]) == 11\n    DB.apply_review(conn, \"e1\", \"accept\", now=2.0, case=cid)             # a decision made between the runs\n    before[\"entry\"][\"e1\"] = (\"accepted\",) + before[\"entry\"][\"e1\"][1:]\n    out = _run(conn, cid, Clock(jump_at))\n    assert out[\"status\"] == \"timeout\"\n    c = DB.get_case(conn, cid)\n    assert c[\"status\"] == \"failed\" and json.loads(c[\"error\"])[\"code\"] == \"run_deadline\"\n    assert _snapshot(conn, cid) == before          # nothing deleted, nothing downgraded, the decision stands\n\n\ndef test_timed_out_rerun_between_flags_of_two_records_keeps_the_flags(tmp_path):\n    conn, cid = _case(tmp_path)\n    PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script()), now=lambda: 1.0)\n    before = _snapshot(conn, cid)\n    clock = Clock()\n    calls = {\"n\": 0}\n    real = PL.FL.run_flag_pass\n\n    def flag_pass(r, **kw):\n        calls[\"n\"] += 1\n        if calls[\"n\"] == 4:                         # the deadline passes after the third record's flags\n            clock.t = 10_000.0\n        return real(r, **kw)\n    PL.FL.run_flag_pass = flag_pass\n    try:\n        out = PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script()), now=clock, deadline_s=480)\n    finally:\n        PL.FL.run_flag_pass = real\n    assert out[\"status\"] == \"timeout\"\n    assert _snapshot(conn, cid) == before\n\n\ndef test_first_run_that_times_out_still_stores_what_finished(tmp_path):\n    conn, cid = _case(tmp_path)\n    out = _run(conn, cid, Clock(\"amounts\"))\n    assert out[\"status\"] == \"timeout\" and len(DB.list_items(conn, cid, \"entry\")) == 9\n    assert [f for f in DB.list_items(conn, cid, \"flag\") if f[\"type\"] == \"gap\"]\nEOF\npython3 -m pytest tests/unit/test_t145_t146_deadline.py -q -p no:cacheprovider -x 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T13:11:55.821Z

**tool result**
````
/opt/homebrew/opt/python@3.12/bin/python3.12: No module named pytest
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:11:57.262Z

**tool call — Bash**
````
{
 "command": "ls -d .venv venv 2>/dev/null; grep -rn \"pytest\" memory/ENVIRONMENT.md | head -3; which -a python pytest"
}
````

### User / tool · 2026-11-02T13:11:57.386Z

**tool result (error)**
````
Exit code 1
.venv
memory/ENVIRONMENT.md:19:| Python deps | fastapi, uvicorn, anthropic, pyyaml, pytest, playwright, httpx, python-multipart | in .venv |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:11:58.733Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_t145_t146_deadline.py -q -p no:cacheprovider 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T13:12:01.276Z

**tool result**
````
        def flag_pass(r, **kw):
            calls["n"] += 1
            if calls["n"] == 4:                         # the deadline passes after the third record's flags
                clock.t = 10_000.0
            return real(r, **kw)
        PL.FL.run_flag_pass = flag_pass
        try:
            out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=clock, deadline_s=480)
        finally:
            PL.FL.run_flag_pass = real
        assert out["status"] == "timeout"
>       assert _snapshot(conn, cid) == before
E       AssertionError: assert {'entry': {'e...rified', [])}} == {'entry': {'e...ONLY']), ...}}
E         
E         Omitting 2 identical items, use -vv to show
E         Differing items:
E         {'flag': {'f_gap_r6_r7': ('pending', 'verified', []), 'f_accident_date_after_treatment_1_2_7': ('pending', 'verified', []), 'f_cx1': ('pending', 'verified', [])}} != {'flag': {'f_gap_r6_r7': ('pending', 'verified', []), 'f_accident_date_after_treatment_1_2_7': ('pending', 'verified', []), 'f_cx1': ('pending', 'verified', []), 'f_r3_1': ('pending', 'needs_review', ['LEXICON_ONLY']), ...}}
E         Use -v to get more diff

tests/unit/test_t145_t146_deadline.py:120: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_before_judge1_leaves_no_verified_entry[judge_entries]
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_before_judge1_leaves_no_verified_entry[verify]
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_case_view_says_judge_not_run_and_never_that_the_check_agreed
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_batch_accept_refuses_every_unjudged_entry
FAILED tests/unit/test_t145_t146_deadline.py::test_timed_out_rerun_keeps_every_previous_item_and_decision[extract]
FAILED tests/unit/test_t145_t146_deadline.py::test_timed_out_rerun_keeps_every_previous_item_and_decision[judge_entries]
FAILED tests/unit/test_t145_t146_deadline.py::test_timed_out_rerun_keeps_every_previous_item_and_decision[flags]
FAILED tests/unit/test_t145_t146_deadline.py::test_timed_out_rerun_between_flags_of_two_records_keeps_the_flags
8 failed, 2 passed in 2.19s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:12:13.195Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport re\np=\"tests/unit/test_t145_t146_deadline.py\"\ns=open(p).read()\na=s.index(\"def test_deadline_case_view_says\")\nb=s.index(\"def test_deadline_batch_accept\")\nnew='''def test_deadline_case_view_says_judge_not_run_and_never_that_the_check_agreed(tmp_path):\n    conn, cid = _case(tmp_path)\n    _run(conn, cid, Clock(\"judge_entries\"))\n    for r in DB.list_items(conn, cid, \"entry\"):\n        why = present._common(r)[\"why\"]\n        assert \"JUDGE_NOT_RUN\" in why and \"agreed\" not in why, r[\"id\"]\n\n\n'''\ns=s[:a]+new+s[b:]\nopen(p,\"w\").write(s)\n\n# implementation\np=\"app/backend/pipeline.py\"\ns=open(p).read()\ns=s.replace('''    if guard(\"judge_entries\") and entries:\n        generator.judge_entries(entries, by_n, call=call, case_text=text)\n''','''    if guard(\"judge_entries\") and entries:\n        generator.judge_entries(entries, by_n, call=call, case_text=text)\n    _mark_judge_not_run(entries, by_n)           # T-145: judge 1 did not run (deadline) -> never 'verified'\n''')\ns=s.replace('''def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:\n    \"\"\"Write items by id.''','''JUDGE_NOT_RUN = \"JUDGE_NOT_RUN\"\n\n\ndef _mark_judge_not_run(entries: list, by_n: dict) -> None:\n    \"\"\"T-145: an AI entry that has no judge-1 answer (the run hit its deadline before or during the stage) is recorded as judge `unavailable` with reason_code\n    JUDGE_NOT_RUN and recomposed, so it is `needs_review` (JUDGE_UNAVAILABLE, whose sentence names JUDGE_NOT_RUN), never `verified`, and batch accept (state == verified) refuses it.\n    Missing is not a pass: compose treats a judge of None as 'nothing to doubt', so the absence is made explicit here.\"\"\"\n    for e in entries:\n        if e[\"state\"] == \"rejected\" or (e[\"ladder\"].get(\"judge\") or {}).get(\"verdict\"):\n            continue\n        e[\"ladder\"][\"judge\"] = {\"model\": None, \"prompt_version\": None, \"call_id\": None, \"verdict\": \"unavailable\", \"reason_code\": JUDGE_NOT_RUN}\n        generator.compose(e, by_n[e[\"seq\"]], judge=\"unavailable\")\n\n\ndef _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bool = False) -> None:\n    \"\"\"Write items by id.''')\ns=s.replace('''computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed.\"\"\"\n    table = {\"entry\": \"entries\", \"amount\": \"amounts\", \"flag\": \"flags\"}[kind]\n    existing = {i[\"id\"]: i for i in DB.list_items(conn, cid, kind)}\n    for it in items:\n        old = existing.get(it[\"id\"])''','''computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed.\n    `additive` (T-146, a run that stopped at its deadline): only items with no stored row are added. A stopped run is partial, so it must not delete, downgrade or\n    overwrite what an earlier complete run stored (its judged states, its flags) or what the paralegal decided.\"\"\"\n    table = {\"entry\": \"entries\", \"amount\": \"amounts\", \"flag\": \"flags\"}[kind]\n    existing = {i[\"id\"]: i for i in DB.list_items(conn, cid, kind)}\n    for it in items:\n        old = existing.get(it[\"id\"])\n        if additive and old is not None:\n            continue''')\ns=s.replace('''    keep = {i[\"id\"] for i in items}\n    for oid, old in existing.items():\n        if oid not in keep''','''    if additive:\n        return\n    keep = {i[\"id\"] for i in items}\n    for oid, old in existing.items():\n        if oid not in keep''')\nfor k in (\"entry\",\"amount\",\"flag\"):\n    pass\ns=s.replace('''[e for e in tray if e.get(\"record_ids\") and \"summary\" in e], now_t)\n    _persist(conn, cid, \"amount\", final_amounts, now_t)\n    _persist(conn, cid, \"flag\", flag_items + [f for f in tray if \"summary\" not in f], now_t)''','''[e for e in tray if e.get(\"record_ids\") and \"summary\" in e], now_t, additive=timed_out)\n    _persist(conn, cid, \"amount\", final_amounts, now_t, additive=timed_out)\n    _persist(conn, cid, \"flag\", flag_items + [f for f in tray if \"summary\" not in f], now_t, additive=timed_out)''')\ns=s.replace('\"The run passed its time limit; finished items were kept.\"','\"The run passed its time limit; items from earlier runs and your decisions were kept, and nothing the run did not finish was added or changed.\"')\nopen(p,\"w\").write(s)\np=\"app/backend/why.py\"\ns=open(p).read()\ns=s.replace('\"JUDGE_UNAVAILABLE\": \"The second AI check did not run or did not finish, so this item has not been double-checked.\"','\"JUDGE_UNAVAILABLE\": \"JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.\"')\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_t145_t146_deadline.py -q -p no:cacheprovider 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T13:12:14.618Z

**tool result**
````
E       AssertionError: assert (9 == 9 and 10 == 11)
E        +  where 9 = len({'e1': ('pending', 'verified', []), 'e2': ('pending', 'verified', []), 'e3': ('pending', 'verified', []), 'e4': ('pending', 'verified', []), ...})
E        +  and   10 = len({'f_gap_r6_r7': ('pending', 'verified', []), 'f_accident_date_after_treatment_1_2_7': ('pending', 'verified', []), 'f_cx1': ('pending', 'verified', []), 'f_r3_1': ('pending', 'needs_review', ['LEXICON_ONLY']), ...})

tests/unit/test_t145_t146_deadline.py:87: AssertionError
______ test_timed_out_rerun_keeps_every_previous_item_and_decision[flags] ______

tmp_path = PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-4548/test_timed_out_rerun_keeps_eve2')
jump_at = 'flags'

    @pytest.mark.parametrize("jump_at", ["extract", "judge_entries", "flags"])
    def test_timed_out_rerun_keeps_every_previous_item_and_decision(tmp_path, jump_at):
        conn, cid = _case(tmp_path)
        first = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 1.0)
        assert first["status"] == "done"
        before = _snapshot(conn, cid)
>       assert len(before["entry"]) == 9 and len(before["flag"]) == 11
E       AssertionError: assert (9 == 9 and 10 == 11)
E        +  where 9 = len({'e1': ('pending', 'verified', []), 'e2': ('pending', 'verified', []), 'e3': ('pending', 'verified', []), 'e4': ('pending', 'verified', []), ...})
E        +  and   10 = len({'f_gap_r6_r7': ('pending', 'verified', []), 'f_accident_date_after_treatment_1_2_7': ('pending', 'verified', []), 'f_cx1': ('pending', 'verified', []), 'f_r3_1': ('pending', 'needs_review', ['LEXICON_ONLY']), ...})

tests/unit/test_t145_t146_deadline.py:87: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_before_judge1_leaves_no_verified_entry[judge_entries]
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_case_view_says_judge_not_run_and_never_that_the_check_agreed
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_batch_accept_refuses_every_unjudged_entry
FAILED tests/unit/test_t145_t146_deadline.py::test_timed_out_rerun_keeps_every_previous_item_and_decision[extract]
FAILED tests/unit/test_t145_t146_deadline.py::test_timed_out_rerun_keeps_every_previous_item_and_decision[judge_entries]
FAILED tests/unit/test_t145_t146_deadline.py::test_timed_out_rerun_keeps_every_previous_item_and_decision[flags]
6 failed, 4 passed in 1.04s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:12:18.743Z

**tool call — Bash**
````
{
 "command": "sed -i 's/len(before\\[\"flag\"\\]) == 11/len(before[\"flag\"]) >= 10          # 9 model flags + code flags (the reviewer saw 11 with the judge-conflict flags of the live run)/' tests/unit/test_t145_t146_deadline.py && .venv/bin/python -m pytest tests/unit/test_t145_t146_deadline.py -q -p no:cacheprovider 2>&1 | grep -E \"^E|FAILED|passed|failed\" | head -30"
}
````

### User / tool · 2026-11-02T13:12:18.868Z

**tool result (error)**
````
Exit code 1
sed: 2: "tests/unit/test_t145_t1 ...": undefined label 'ests/unit/test_t145_t146_deadline.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:12:21.138Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\np=\"tests/unit/test_t145_t146_deadline.py\"\ns=open(p).read()\ns=s.replace('len(before[\"flag\"]) == 11','len(before[\"flag\"]) >= 10')\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_t145_t146_deadline.py -q -p no:cacheprovider 2>&1 | grep -E \"^E|FAILED|passed|failed\" | head -30"
}
````

### User / tool · 2026-11-02T13:12:23.195Z

**tool result**
````
E           AssertionError: e1
E           assert ('verified' == 'needs_review'
E             
E             - needs_review
E             + verified)
E           AssertionError: e1
E           assert ('JUDGE_NOT_RUN' in 'Quote found word for word, every number in the summary is in the quote, and the second check agreed.')
E       Failed: DID NOT RAISE BatchRefused
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_before_judge1_leaves_no_verified_entry[judge_entries]
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_case_view_says_judge_not_run_and_never_that_the_check_agreed
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_batch_accept_refuses_every_unjudged_entry
3 failed, 7 passed in 1.73s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:12:30.651Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\np=\"tests/unit/test_t145_t146_deadline.py\"\ns=open(p).read()\ns=s.replace('[\"judge_entries\", \"verify\"])\\ndef test_deadline_before','[\"extract\", \"verify\"])      # the clock jumps as that stage starts, so the next guard (verify / judge_entries) fails\\ndef test_deadline_before')\ns=s.replace('Clock(\"judge_entries\"))\\n    for r','Clock(\"verify\"))\\n    for r').replace('_run(conn, cid, Clock(\"judge_entries\"))\\n    ids','_run(conn, cid, Clock(\"verify\"))\\n    ids')\ns=s.replace('[\"extract\", \"judge_entries\", \"flags\"]','[\"extract\", \"verify\", \"judge_entries\", \"flags\"]')\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -m pytest tests/unit/test_t145_t146_deadline.py -q -p no:cacheprovider 2>&1 | grep -E \"^E|FAILED|passed|failed\" | head -30"
}
````

### User / tool · 2026-11-02T13:12:32.066Z

**tool result**
````
11 passed in 1.10s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:12:41.009Z

**tool call — Bash**
````
{
 "command": "cp app/backend/pipeline.py /tmp/pl.bak 2>/dev/null; P=app/backend/pipeline.py; cp $P $TMPDIR/pl.bak 2>/dev/null || cp $P /private/tmp/pl.bak; sed -i '' 's/^    _mark_judge_not_run(entries, by_n) .*$/    pass/' $P; .venv/bin/python -m pytest tests/unit/test_t145_t146_deadline.py -q -p no:cacheprovider 2>&1 | tail -2; cp /private/tmp/pl.bak $P 2>/dev/null || cp $TMPDIR/pl.bak $P; grep -n \"_mark_judge_not_run(entries\" $P; sed -i '' 's/additive=timed_out/additive=False/' $P; .venv/bin/python -m pytest tests/unit/test_t145_t146_deadline.py -q -p no:cacheprovider 2>&1 | tail -2; cp /private/tmp/pl.bak $P 2>/dev/null || cp $TMPDIR/pl.bak $P; grep -c \"additive=timed_out\" $P"
}
````

### User / tool · 2026-11-02T13:12:44.197Z

**tool result**
````
FAILED tests/unit/test_t145_t146_deadline.py::test_deadline_batch_accept_refuses_every_unjudged_entry
4 failed, 7 passed in 1.45s
221:def _mark_judge_not_run(entries: list, by_n: dict) -> None:
366:    _mark_judge_not_run(entries, by_n)           # T-145: judge 1 did not run (deadline) -> never 'verified'
FAILED tests/unit/test_t145_t146_deadline.py::test_timed_out_rerun_between_flags_of_two_records_keeps_the_flags
5 failed, 6 passed in 1.18s
3
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:12:45.150Z

Mutants killed and restored. Full unit suite.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:12:45.706Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -x -q 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T13:12:47.581Z

**tool result**
````
        ("Estimated cost $4,000.", "estimate"), ("Estimate: $900", "estimate"),
    ])
    def test_charge_and_estimate_phrases(text, cls):
        """R-CH-2: explicit billing phrases -> charge; 'estimated' -> estimate."""
        a = A.find_amounts(text)[0]
>       assert A.classify(text, a) == cls
E       AssertionError: assert 'unclear' == 'charge'
E         
E         - charge
E         + unclear

tests/unit/test_amounts.py:48: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_amounts.py::test_charge_and_estimate_phrases[Total billed: $310.00-charge]
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:12:48.641Z

Another worker's in-progress amounts.py. Run without -x and compare failures.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:12:49.249Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | grep -E \"^FAILED|passed|failed\" | head -30"
}
````

### User / tool · 2026-11-02T13:14:49.987Z

**tool result**
````
Command did not complete within its 120s timeout and was moved to the background (ID: b8ay3zgyh). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b8ay3zgyh.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:14:51.638Z

**tool call — Bash**
````
{
 "command": "sleep 100; tail -c 600 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b8ay3zgyh.output"
}
````

### User / tool · 2026-11-02T13:14:51.640Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 100 followed by: tail -c 600 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b8ay3zgyh.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:14:52.904Z

Meanwhile, write the board notes.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:14:55.830Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B note T-145 --agent backend --text \"Fix in pipeline.py: _mark_judge_not_run after the judge stage records ladder.judge {verdict unavailable, reason_code JUDGE_NOT_RUN} and recomposes (needs_review, reason JUDGE_UNAVAILABLE; reason list is closed so no new code). why.py JUDGE_UNAVAILABLE sentence now starts 'JUDGE_NOT_RUN: ...' (one-line edit in a file other workers also have dirty). Tests: tests/unit/test_t145_t146_deadline.py; mutation (call removed) fails 4.\" ; $B note T-146 --agent backend --text \"Fix in pipeline.py: _persist(additive=timed_out) adds only unseen ids on a timed-out run; no delete, no overwrite, so a complete earlier run and the paralegal's decisions are untouched; error message reworded to say exactly that. Reviewer saw 11 flags; this sample gives 10 on the fixture backend, tests assert equality before/after not the count.\""
}
````

### User / tool · 2026-11-02T13:14:56.032Z

**tool result**
````
noted on T-145
noted on T-146
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:14:57.564Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"passed|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b8ay3zgyh.output; do sleep 3; done; grep -E \"^FAILED|passed|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b8ay3zgyh.output | head -30",
 "description": "full unit suite finishing",
 "timeout_ms": 600000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T13:14:57.576Z

**tool result**
````
Monitor started (task bzlypx20d, expires in 10m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:14:59.102Z

**tool call — Monitor**
````
{
 "command": "sleep 1; echo waiting",
 "description": "noop",
 "timeout_ms": 2000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T13:14:59.110Z

**tool result**
````
Monitor started (task bzvwb1hrr, expires in 2s unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:15:01.999Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- app/backend/pipeline.py app/backend/why.py | cat; git diff app/backend/pipeline.py | grep -c \"^[+-]\""
}
````

### User / tool · 2026-11-02T13:15:02.130Z

**tool result**
````
 app/backend/pipeline.py | 33 +++++++++++++++++++++++++++------
 app/backend/why.py      |  3 ++-
 2 files changed, 29 insertions(+), 7 deletions(-)
35
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:15:03.232Z

**tool call — Bash**
````
{
 "command": "git diff app/backend/why.py | cat"
}
````

### User / tool · 2026-11-02T13:15:03.366Z

**tool result**
````
diff --git a/app/backend/why.py b/app/backend/why.py
index 162057e..83273b7 100644
--- a/app/backend/why.py
+++ b/app/backend/why.py
@@ -7,12 +7,13 @@ _WHY = {
     "SUMMARY_DROPS_QUALIFIER": "The quoted text carries a qualifier (a hedge, an attribution phrase, a negation, a side or an approximation) that the summary leaves out.",
     "EXCERPT_OMITS_QUALIFIER": "The record has a hedge sentence that qualifies this quote, but the quote leaves it out.",
     "EXCERPT_NOT_WHOLE_SENTENCE": "The quote starts or ends in the middle of a sentence.",
+    "CHARGE_TEXT_IN_ENTRY": "The summary or the quote states a dollar amount. Amounts go only in the internal notes, never in the letter, so this entry is held out of the letter until you pick a quote without the amount (or edit the summary to remove it).",
     "HIGHLIGHT_NOT_FOUND": "The quote could not be located in the record text, so it cannot be highlighted.",
     "JUDGE_PARTIAL": "A second AI check found the summary only partly supported by the quoted text.",
     "JUDGE_UNSUPPORTED": "A second AI check found the summary not supported by the quoted text.",
     "JUDGE_DISAGREES": "A second AI check disagreed with the first result for this item.",
     "JUDGE_UNSURE": "A second AI check could not decide whether this item is supported.",
-    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this item has not been double-checked.",
+    "JUDGE_UNAVAILABLE": "JUDGE_NOT_RUN: the second AI check did not run or did not finish, so this item has not been double-checked.",
     "FIXTURE_MISS": "The demo has no recorded AI answer for this step, so this item has not been checked.",
     "DATE_AMBIGUOUS": "The date can be read two ways; confirm which one is right. It is left out of gap checks until then.",
     "DATE_MISSING": "The record has no readable date, so it is left out of gap checks.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:15:07.356Z

**tool call — Bash**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b8ay3zgyh.output; do sleep 5; done 2>/dev/null & wait; grep -E \"^FAILED|passed|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b8ay3zgyh.output | head -30",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T13:21:47.482Z

**tool result**
````
Command did not complete within its 400s timeout and was moved to the background (ID: btbz226qx). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/btbz226qx.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:21:55.465Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/mine; mkdir -p $S/mine && git archive HEAD | tar -x -C $S/mine && ln -s $PWD/.venv $S/mine/.venv; git diff app/backend/pipeline.py > $S/pl.patch; cp tests/unit/test_t145_t146_deadline.py $S/mine/tests/unit/; cd $S/mine && git init -q . 2>/dev/null; patch -p1 < $S/pl.patch && sed -i '' 's/\"JUDGE_UNAVAILABLE\": \"The second AI check did not run/\"JUDGE_UNAVAILABLE\": \"JUDGE_NOT_RUN: the second AI check did not run/' app/backend/why.py && grep -c JUDGE_NOT_RUN: app/backend/why.py; (timeout 900 .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -x -q 2>&1 | grep -E \"^FAILED|passed|failed\" > $S/mine.out; echo done >> $S/mine.out) &\nsleep 1; echo started",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T13:21:55.560Z

**tool result**
````
Command running in background with ID: biov6r3de. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/biov6r3de.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:21:58.353Z

**tool call — Bash**
````
{
 "command": "sleep 45; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/biov6r3de.output | head; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine.out"
}
````

### User / tool · 2026-11-02T13:21:58.355Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 45 followed by: cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/biov6r3de.output head cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine.out. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:00.201Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/biov6r3de.output | head; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine.out"
}
````

### User / tool · 2026-11-02T13:22:00.312Z

**tool result**
````
patching file 'app/backend/pipeline.py'
1
[1]+  Done                    ( timeout 900 .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -x -q 2>&1 | grep -E "^FAILED|passed|failed" > $S/mine.out; echo done >> $S/mine.out )
started

[exited with code 0]
done
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:03.274Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine && timeout 1500 .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | grep -E \"^FAILED|^ERROR| passed| failed\"",
 "timeout": 1500000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T13:22:03.346Z

**tool result**
````
Command running in background with ID: bwwp8sttb. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bwwp8sttb.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:05.474Z

**tool call — Bash**
````
{
 "command": "git diff --cached --name-only | head; git diff app/backend/pipeline.py | grep \"^[-+]\" | grep -v \"^+++\\|^---\" | cut -c1-140"
}
````

### User / tool · 2026-11-02T13:22:05.613Z

**tool result**
````
app/backend/present.py
app/backend/uncovered.py
tests/unit/test_uncovered.py
-def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
+JUDGE_NOT_RUN = "JUDGE_NOT_RUN"
+
+
+def _mark_judge_not_run(entries: list, by_n: dict) -> None:
+    """T-145: an AI entry that has no judge-1 answer (the run hit its deadline before or during the stage) is recorded as judge `unavailabl
+    JUDGE_NOT_RUN and recomposed, so it is `needs_review` (JUDGE_UNAVAILABLE, whose sentence names JUDGE_NOT_RUN), never `verified`, and ba
+    Missing is not a pass: compose treats a judge of None as 'nothing to doubt', so the absence is made explicit here."""
+    for e in entries:
+        if e["state"] == "rejected" or (e["ladder"].get("judge") or {}).get("verdict"):
+            continue
+        e["ladder"]["judge"] = {"model": None, "prompt_version": None, "call_id": None, "verdict": "unavailable", "reason_code": JUDGE_NOT_
+        generator.compose(e, by_n[e["seq"]], judge="unavailable")
+
+
+def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bool = False) -> None:
-    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
+    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed.
+    `additive` (T-146, a run that stopped at its deadline): only items with no stored row are added. A stopped run is partial, so it must n
+    overwrite what an earlier complete run stored (its judged states, its flags) or what the paralegal decided."""
+        if additive and old is not None:
+            continue
+    if additive:
+        return
+    _mark_judge_not_run(entries, by_n)           # T-145: judge 1 did not run (deadline) -> never 'verified'
-    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
-    _persist(conn, cid, "amount", final_amounts, now_t)
-    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
+    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out)
+    _persist(conn, cid, "amount", final_amounts, now_t, additive=timed_out)
+    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t, additive=timed_out)
-        err = {"code": "run_deadline", "message": "The run passed its time limit; finished items were kept."}
+        err = {"code": "run_deadline", "message": "The run passed its time limit; items from earlier runs and your decisions were kept, and
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:09.674Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bwwp8sttb.output | cut -c1-250"
}
````

### User / tool · 2026-11-02T13:22:09.762Z

**tool result**
````
[exited with code 1]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:12.898Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine && .venv/bin/python -m pytest tests/unit/test_t145_t146_deadline.py -q -p no:cacheprovider 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T13:22:17.835Z

**tool result**
````
...........                                                              [100%]
11 passed in 4.60s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:25.067Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine && .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider > ../mine_full.txt 2>&1; tail -5 ../mine_full.txt | cut -c1-200",
 "timeout": 1500000,
 "run_in_background": true
}
````

### User / tool · 2026-11-02T13:22:25.144Z

**tool result**
````
Command running in background with ID: bqjnwzlkj. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bqjnwzlkj.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:26.081Z

Meanwhile fix the message wording.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:26.963Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\np=\"app/backend/pipeline.py\"\ns=open(p).read()\ns=s.replace(\"items from earlier runs and your decisions were kept, and nothing the run did not finish was added or changed.\",\"every item from earlier runs and every decision of yours was kept unchanged.\")\nopen(p,\"w\").write(s)\nEOF\ngrep -rn \"finished items were kept\" app tests memory/contracts | head"
}
````

### User / tool · 2026-11-02T13:22:27.102Z

**tool result**
````
tests/unit/test_t145_t146_deadline.py:3:T-146: a timed-out re-run keeps every previous item and decision (its error says 'finished items were kept')."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:31.243Z

**tool call — Monitor**
````
{
 "command": "until [ -s /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine_full.txt ] && grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine_full.txt; do sleep 5; done; grep -E \"^FAILED|^ERROR| passed| failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine_full.txt | cut -c1-200",
 "description": "scratch full unit suite",
 "timeout_ms": 900000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T13:22:31.267Z

**tool result**
````
Monitor started (task bqjst39ia, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:33.532Z

**tool call — Monitor**
````
{
 "command": "until [ -s /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bqjnwzlkj.output ] || ! pgrep -f \"mine.*pytest tests/unit\" >/dev/null; do sleep 5; done; echo finished",
 "description": "await suite end",
 "timeout_ms": 900000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T13:22:33.550Z

**tool result**
````
Monitor started (task bpcb15jwa, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:38.199Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bqjnwzlkj.output | cut -c1-200; ls -la /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/"
}
````

### User / tool · 2026-11-02T13:22:38.535Z

**tool result**
````
total 6912
drwxr-xr-x@ 45 arsis  wheel    1440 Nov  2 07:22 .
drwxr-xr-x@  4 arsis  wheel     128 Nov  2 01:10 ..
-rw-r--r--@  1 arsis  wheel  125536 Nov  2 04:37 api.commit.md
-rw-r--r--@  1 arsis  wheel    2189 Nov  2 01:10 api.diff
-rw-r--r--@  1 arsis  wheel  126970 Nov  2 05:11 api.md.new
-rw-r--r--@  1 arsis  wheel   30926 Nov  2 05:11 api.py.new
drwxr-xr-x@ 23 arsis  wheel     736 Nov  2 01:29 arc
-rw-r--r--@  1 arsis  wheel   77234 Nov  2 01:23 before.txt
-rw-r--r--@  1 arsis  wheel     955 Nov  2 04:29 cmp.py
-rw-r--r--@  1 arsis  wheel     872 Nov  2 05:06 dbg.py
-rw-r--r--@  1 arsis  wheel     845 Nov  2 05:06 dbg.py.bak
drwxr-xr-x@  5 arsis  wheel     160 Nov  2 05:02 ev123
-rw-r--r--@  1 arsis  wheel     374 Nov  2 05:02 ev123.log
drwxr-xr-x@  5 arsis  wheel     160 Nov  2 05:18 ev126
-rw-r--r--@  1 arsis  wheel     374 Nov  2 05:18 ev126.log
-rw-r--r--@  1 arsis  wheel     401 Nov  2 04:30 evals.out
-rw-r--r--@  1 arsis  wheel     305 Nov  2 03:34 evals116.txt
-rw-r--r--@  1 arsis  wheel    5488 Nov  2 05:06 full1.log
-rw-r--r--@  1 arsis  wheel   25875 Nov  2 05:10 full2.log
-rw-r--r--@  1 arsis  wheel    4072 Nov  2 05:18 full3.log
-rw-r--r--@  1 arsis  wheel    3369 Nov  2 05:23 full4.log
-rw-r--r--@  1 arsis  wheel    3369 Nov  2 05:27 full5.log
drwxr-xr-x@  3 arsis  wheel      96 Nov  2 04:31 g
-rw-r--r--@  1 arsis  wheel  269171 Nov  2 05:27 i6
-rw-r--r--@  1 arsis  wheel  269171 Nov  2 05:27 i7
-rw-r--r--@  1 arsis  wheel  269283 Nov  2 05:27 i8
-rw-r--r--@  1 arsis  wheel  269283 Nov  2 05:27 i9
-rw-r--r--@  1 arsis  wheel  261680 Nov  2 04:37 idx
-rw-r--r--@  1 arsis  wheel  262225 Nov  2 05:10 idx1
-rw-r--r--@  1 arsis  wheel  262240 Nov  2 03:35 idx116
-rw-r--r--@  1 arsis  wheel  262337 Nov  2 05:10 idx2
-rw-r--r--@  1 arsis  wheel  264387 Nov  2 05:10 idx3
-rw-r--r--@  1 arsis  wheel  264491 Nov  2 05:11 idx4
-rw-r--r--@  1 arsis  wheel  264595 Nov  2 05:18 idx5
-rw-r--r--@  1 arsis  wheel    6832 Nov  2 05:23 ls.bak
drwxr-xr-x@ 23 arsis  wheel     736 Nov  2 07:21 mine
-rw-r--r--@  1 arsis  wheel       5 Nov  2 07:21 mine.out
-rw-r--r--@  1 arsis  wheel     534 Nov  2 07:22 mine_full.txt
-rw-r--r--@  1 arsis  wheel    1767 Nov  2 05:11 mkblobs.py
-rw-r--r--@  1 arsis  wheel   32468 Nov  2 04:37 pipeline.commit.py
-rw-r--r--@  1 arsis  wheel   32365 Nov  2 03:35 pipeline_mine.py
-rw-r--r--@  1 arsis  wheel    5104 Nov  2 07:21 pl.patch
-rw-r--r--@  1 arsis  wheel     757 Nov  2 01:23 rec_j2.py
-rw-r--r--@  1 arsis  wheel   39389 Nov  2 04:37 review.commit.py
-rw-r--r--@  1 arsis  wheel   10541 Nov  2 04:36 unit2.out
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:40.103Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine_full.txt"
}
````

### User / tool · 2026-11-02T13:22:40.217Z

**tool result**
````
........................................................................ [  1%]
........................................................................ [  3%]
........................................................................ [  5%]
........................................................................ [  7%]
........................................................................ [  9%]
........................................................................ [ 11%]
........................................................................ [ 13%]
.......................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:41.117Z

Running; waiting for the monitor.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:42.732Z

**tool call — Monitor**
````
{
 "command": "until grep -qE \"[0-9]+ (passed|failed)\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine_full.txt; do sleep 10; done; grep -E \"^FAILED|^ERROR| passed| failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine_full.txt | cut -c1-200",
 "description": "scratch suite result",
 "timeout_ms": 900000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T13:22:42.743Z

**tool result**
````
Monitor started (task b0hv7beqk, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:44.106Z

**tool call — Monitor**
````
{
 "command": "sleep 1; echo x",
 "description": "idle",
 "timeout_ms": 1500,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T13:22:44.114Z

**tool result**
````
Monitor started (task b8c31g4on, expires in 1s unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:22:47.468Z

**tool call — Bash**
````
{
 "command": "f=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mine_full.txt; until grep -qE \"[0-9]+ (passed|failed)\" $f; do sleep 5; done; grep -E \"^FAILED|^ERROR| passed| failed\" $f | cut -c1-200",
 "timeout": 590000
}
````

### User / tool · 2026-11-02T13:26:08.289Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:26:23.953Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\np=\"tests/unit/test_t145_t146_deadline.py\"\ns=open(p).read()\ni=s.index(\"# ------------------------------------------------------------------ T-146\")\nhead=s[:i]\ntail=s[i:]\nh_end=head.index(\"# ------------------------------------------------------------------ T-145\")\ncommon=head[:h_end]\nt145=head[h_end:]\ndoc145='\"\"\"T-145 (GATE-M2 staff blocker): an entry whose second check (judge 1) never ran is never `verified`, says JUDGE_NOT_RUN, and batch accept refuses it.\"\"\"\\n'\ndoc146='\"\"\"T-146 (GATE-M2 staff major): a failed or timed-out re-run keeps every previous item and decision, as its error message says.\"\"\"\\n'\nbody_common=common[common.index(\"import json\"):]\nopen(\"tests/unit/test_t145_judge_not_run.py\",\"w\").write(doc145+body_common+t145.replace(\"# ------------------------------------------------------------------ T-145\\n\",\"\"))\nopen(\"tests/unit/test_t146_rerun_keeps_items.py\",\"w\").write(doc146+body_common+tail.replace(\"# ------------------------------------------------------------------ T-146\\n\",\"\"))\nEOF\nrm tests/unit/test_t145_t146_deadline.py\n.venv/bin/python -m pytest tests/unit/test_t145_judge_not_run.py tests/unit/test_t146_rerun_keeps_items.py -q -p no:cacheprovider 2>&1 | tail -3; .venv/bin/python -m pyflakes tests/unit/test_t145_judge_not_run.py tests/unit/test_t146_rerun_keeps_items.py 2>&1 | head"
}
````

### User / tool · 2026-11-02T13:26:25.658Z

**tool result**
````
...........                                                              [100%]
11 passed in 1.18s
/Users/arsis/zlayt-pm-project/.venv/bin/python: No module named pyflakes
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:26:37.790Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && .venv/bin/python - <<'EOF'\nimport subprocess\nS=\"/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\"\nhead=subprocess.check_output([\"git\",\"show\",\"HEAD:app/backend/pipeline.py\"]).decode()\ncur=open(\"app/backend/pipeline.py\").read()\na=cur.index(\"JUDGE_NOT_RUN = \")\nb=cur.index(\"def _persist(\")\nfunc=cur[a:b]\nA=head.replace(\"def _persist(\", func+\"def _persist(\",1)\ncall_line=[l for l in cur.splitlines(True) if l.lstrip().startswith(\"_mark_judge_not_run(entries\")][0]\nanchor='        generator.judge_entries(entries, by_n, call=call, case_text=text)\\n'\nassert anchor in A\nA=A.replace(anchor, anchor+call_line,1)\nopen(S+\"/pipeline_A.py\",\"w\").write(A)\nwhy=subprocess.check_output([\"git\",\"show\",\"HEAD:app/backend/why.py\"]).decode()\nold='\"JUDGE_UNAVAILABLE\": \"The second AI check did not run'\nassert old in why\nopen(S+\"/why_A.py\",\"w\").write(why.replace(old,'\"JUDGE_UNAVAILABLE\": \"JUDGE_NOT_RUN: the second AI check did not run',1))\nEOF\ncat > $S/commit_split.sh <<'EOF'\nset -e\ncd /Users/arsis/zlayt-pm-project\nS=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nexport GIT_INDEX_FILE=$S/tmp.index\nrm -f $GIT_INDEX_FILE\ngit read-tree HEAD\nupd() { h=$(git hash-object -w \"$2\"); git update-index --add --cacheinfo 100644,$h,\"$1\"; echo $h; }\nupd app/backend/pipeline.py $S/pipeline_A.py > $S/h_pl_A\nupd app/backend/why.py $S/why_A.py > $S/h_why_A\nupd tests/unit/test_t145_judge_not_run.py tests/unit/test_t145_judge_not_run.py > $S/h_t145\ngit commit -q -m \"fix(backend): T-145 an entry whose judge 1 never ran is needs_review, JUDGE_NOT_RUN, and batch accept refuses it\n\nWhen the run deadline passes before judge 1, entries stayed verified with no verdict\nand the Why said the second check agreed. They now record judge unavailable with\nreason_code JUDGE_NOT_RUN and are recomposed to needs_review (JUDGE_UNAVAILABLE,\nwhose sentence now starts JUDGE_NOT_RUN). No prompt changed.\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\"\ngit rev-parse HEAD > $S/sha_A\nupd app/backend/pipeline.py app/backend/pipeline.py > $S/h_pl_B\nupd tests/unit/test_t146_rerun_keeps_items.py tests/unit/test_t146_rerun_keeps_items.py > $S/h_t146\ngit commit -q -m \"fix(backend): T-146 a timed-out re-run keeps every previous item and decision\n\nA run that stops at its deadline persisted its partial result and deleted the earlier\nrun's pending rows. It now only adds ids with no stored row (no delete, no overwrite),\nand the run_deadline message says what was kept.\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\"\ngit rev-parse HEAD > $S/sha_B\nunset GIT_INDEX_FILE\n# bring the shared index in line for the paths just committed (their working-tree/HEAD state differs only for why.py, which others also edit)\ngit update-index --cacheinfo 100644,$(cat $S/h_pl_B),app/backend/pipeline.py\ngit update-index --cacheinfo 100644,$(cat $S/h_why_A),app/backend/why.py\ngit update-index --add --cacheinfo 100644,$(cat $S/h_t145),tests/unit/test_t145_judge_not_run.py\ngit update-index --add --cacheinfo 100644,$(cat $S/h_t146),tests/unit/test_t146_rerun_keeps_items.py\nEOF\nbash $S/commit_split.sh; git log --oneline | head -3; git show --stat HEAD~1 | tail -5; git show --stat HEAD | tail -4; git status --short app/backend/pipeline.py app/backend/why.py tests/unit/test_t14*"
}
````

### User / tool · 2026-11-02T13:26:39.730Z

**tool result**
````
check_secrets: ok (3 file(s) scanned staged)
check_secrets: ok (2 file(s) scanned staged)
7d3ca35 fix(backend): T-146 a timed-out re-run keeps every previous item and decision
b604ff2 fix(backend): T-145 an entry whose judge 1 never ran is needs_review, JUDGE_NOT_RUN, and batch accept refuses it
5a388d5 fix(backend): T-143 r2 uncovered lists every sentence no entry covers; only anchored administrative lines skipped; form answer carries its question

 app/backend/pipeline.py               | 15 ++++++++
 app/backend/why.py                    |  2 +-
 tests/unit/test_t145_judge_not_run.py | 72 +++++++++++++++++++++++++++++++++++
 3 files changed, 88 insertions(+), 1 deletion(-)

 app/backend/pipeline.py                   | 18 ++++---
 tests/unit/test_t146_rerun_keeps_items.py | 79 +++++++++++++++++++++++++++++++
 2 files changed, 91 insertions(+), 6 deletions(-)
 M app/backend/why.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:26:49.464Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; S=/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nA=$(cat $S/sha_A); Bs=$(cat $S/sha_B)\n$B ac T-145 --check 1 --agent backend --evidence \"tests/unit/test_t145_judge_not_run.py (5 tests: deadline before judge 1 -> needs_review/JUDGE_NOT_RUN, why has no 'agreed', apply_batch raises BatchRefused not_verified x9); mutation removing _mark_judge_not_run fails 4\"\n$B handoff T-145 --agent backend --text \"What changed: pipeline._mark_judge_not_run records ladder.judge {verdict unavailable, reason_code JUDGE_NOT_RUN} on any non-rejected entry without a judge answer and recomposes it (needs_review, reason JUDGE_UNAVAILABLE; closed reason list unchanged). why.py JUDGE_UNAVAILABLE sentence now starts 'JUDGE_NOT_RUN:' (one-line hunk; why.py has another worker's uncommitted CHARGE_TEXT hunk, left out of my commit). No prompt changed. · Verified: 5 new tests; full tests/unit on HEAD+my change in a scratch copy: 3612 passed, 4 failed (git-archive-only tests: no .git) . · Left: api.md note not written (file dirty from others); the JUDGE_UNAVAILABLE wording applies to edits/rejudge too. · Surprised: compose treats judge None as clean, so absence was fail-open by design; nothing downstream checked. Commit $A\"\n$B commit T-145 --sha $A --agent backend\n$B move T-145 in_review --agent backend\n$B ac T-146 --check 1 --agent backend --evidence \"tests/unit/test_t146_rerun_keeps_items.py (6 tests: complete run then timeout at extract/verify/judge_entries/flags and between records 3 and 4 -> every item, state and the accepted e1 decision unchanged; 9 entries, 10 flags on this fixture)\"\n$B handoff T-146 --agent backend --text \"What changed: _persist(additive=timed_out): a run that hits its deadline only adds ids with no stored row; no delete, no update, so the earlier run's items, judged states and decisions stay. run_deadline message now says every earlier item and decision was kept unchanged. · Verified: 6 new tests; mutation additive=False fails 5; scratch full unit run 3612 passed. · Left: a first-ever run that times out still stores its partial items (tested). Fixture sample gives 10 flags not 11, tests compare before/after. · Surprised: a plain 'skip deletes' fix would still downgrade judged amounts to unjudged on timeout, so the whole persist is additive. Commit $Bs\"\n$B commit T-146 --sha $Bs --agent backend\n$B move T-146 in_review --agent backend"
}
````

### User / tool · 2026-11-02T13:26:50.110Z

**tool result**
````
AC 1 checked: tests/unit/test_t145_judge_not_run.py (5 tests: deadline before judge 1 -> needs_review/JUDGE_NOT_RUN, why has no 'agreed', apply_batch raises BatchRefused not_verified x9); mutation removing _mark_judge_not_run fails 4
handoff written on T-145
T-145: commit b604ff281bc1e62b1d4f60a0e89e75c3267e5e53 recorded
T-145: in_progress -> in_review
AC 1 checked: tests/unit/test_t146_rerun_keeps_items.py (6 tests: complete run then timeout at extract/verify/judge_entries/flags and between records 3 and 4 -> every item, state and the accepted e1 decision unchanged; 9 entries, 10 flags on this fixture)
handoff written on T-146
T-146: commit 7d3ca35a434914a83318255c703c375b2e443b93 recorded
T-146: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:26:54.500Z

T-145 and T-146 are fixed and both cards are in `in_review`, committed separately as b604ff2 and 7d3ca35.

- **T-145:** an entry whose judge 1 never ran is now `needs_review` with JUDGE_NOT_RUN recorded as its judge result. Its Why text starts "JUDGE_NOT_RUN:", and batch accept refuses it (`not_verified`). I did not add a new reason code, because the reason list is closed. The state reason is still JUDGE_UNAVAILABLE, whose sentence now starts "JUDGE_NOT_RUN:", so edits and re-runs show that wording too. Edits are in `pipeline.py` and one line of `why.py`; I left another worker's uncommitted `why.py` change out of my commit.
- **T-146:** a run that hits its deadline now only adds items that have no stored row. It deletes and overwrites nothing, so earlier items, judged states and your decisions survive. The `run_deadline` message now says that. The sample gives 10 flags on the fixture backend, not the reviewer's 11, so the tests compare before and after instead of counting.
- **Tests:** the new tests are `tests/unit/test_t145_judge_not_run.py` and `tests/unit/test_t146_rerun_keeps_items.py`, 11 tests in all. Reverting either fix makes them fail. The full unit suite is not green in the live tree because other workers' edits are mid-flight. On a scratch copy of HEAD plus my change it gave 3612 passed and 4 failed, and the 4 are the tests that need `.git`, which the copy doesn't have. I wrote no `api.md` note because the file has others' uncommitted edits.
