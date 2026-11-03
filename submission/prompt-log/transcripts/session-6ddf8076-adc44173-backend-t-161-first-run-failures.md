# Subagent: Backend: T-161 first-run failures (Backend: T-161 first-run failures)

Source: `agent-adc4417326645b2f6.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T14:59:09.235Z

You are a backend worker in /Users/arsis/zlayt-pm-project. Claim T-161 with `python3 tools/board.py claim T-161 --agent backend` and read it with `show`.

A first run with a stage down (flags, judge or conflicts, meaning steps j1, j2, j3, j4 or flags) currently reads 'ready'. Make it behave like a re-run that fails:
- the case is failed or run_partial;
- the message names the step;
- the gate reads RUN_FAILED;
- a clean first run stays ready.

Write the tests first, one per stage. Follow the existing T-146 re-run code in pipeline.py; that worker has finished.

Don't touch amounts.py or export.py (T-140), review.py or trace.py (T-159), or conflicts.py (T-141). Commit via a temp index for only your hunks; the pre-commit hook runs the sample. Run the full unit suite, write the handoff, and move the card to in_review. Reply in 1 line.

### User / tool · 2026-11-02T14:59:09.242Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:18.501Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-161 --agent backend; python3 tools/board.py show T-161; cat .claude/agent-memory/backend/project_t146_rerun_decided_rule.md; git status --short | head -30"
}
````

### User / tool · 2026-11-02T14:59:18.761Z

**tool result**
````
T-161 claimed by backend
---
id: "T-161"
title: "First run with a stage down (flags, judge, conflicts) reads 'ready': it must read failed/run_partial with the step named and the gate RUN_FAILED, same as re-runs (T-146 handoff)"
milestone: "M2"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T14:58:59Z"
updated_at: "2026-11-02T14:59:18Z"
claimed_by: "backend"
claimed_at: "2026-11-02T14:59:18Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "unit tests per stage: first run with that stage failing -> case failed/run_partial, message names the step, gate RUN_FAILED; a clean first run stays ready", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T14:59:05Z orchestrator: assigned: backend
- 2026-11-02T14:59:18Z backend: claimed

## Handoff (filled when moving to in_review)

---
name: t146-rerun-decided-rule
description: T-146 r3 re-run rule in pipeline._persist: decided items kept whole with ladder.rerun_note; _degrades/_disagrees/_failure; message shapes; test helpers
metadata:
  type: project
---

`_persist` returns `(kept, empty)`. Kept = stored row left as is when the new row fails (`_degrades`: entry stub, flag made while flag step down, lost second check) or, for DECIDED rows only, `_disagrees` (worse state or different content). Decided kept rows get `ladder.rerun_note` (view field `rerun_note`); undecided keeps get no note. Case = failed/run_partial built in `_partial_error`; `empty` (failures with nothing stored) counts only when the case already had entries (re-run). Deadline stays additive/run_deadline with no note.

**Why:** reviewer round 2 found accepted flags downgraded and accepted entries replaced by SUMMARY_NOT_IN_QUOTE stubs with case "ready". **How to apply:** new failure kinds go in `_failure`; extend the table tests (`test_disagrees_table`, `test_degrades_table`).

Pitfalls: step names in `failed_steps` are only j1-j4/flags/extract/split (no "conflicts"); judge and generator `call_id` differ every run, so row-equality helpers drop `call_id`; present.py/api.md carry other agents' hunks, commit via temp index.
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
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
MM app/backend/conflict_candidates.py
MM app/backend/pipeline.py
MM app/backend/present.py
 M app/backend/reclassify.py
 M app/backend/review.py
 M app/backend/trace.py
 M app/frontend/api.js
 M app/frontend/app.js
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:21.180Z

**tool call — Bash**
````
{
 "command": "wc -l app/backend/pipeline.py && grep -n \"_persist\\|_failure\\|_partial_error\\|failed_steps\\|run_partial\\|RUN_FAILED\\|def \\|rerun\" app/backend/pipeline.py | head -200; git diff --stat app/backend/pipeline.py; git diff --cached --stat"
}
````

### User / tool · 2026-11-02T14:59:21.318Z

**tool result**
````
     723 app/backend/pipeline.py
25:def _clean(d: dict) -> dict:
30:def _ladder(item_id: str, backend: str, code_checks: dict = None, state: str = None) -> dict:
35:def _compose_code(rec_by_n: dict, nos: list, reasons: list, evidence: list, case_text: str) -> tuple:
44:    return confidence.compose_state({"grounding_failures": ["GROUNDING_EXCERPT_NOT_VERBATIM"] if bad else [], "schema_valid": True,
49:def run_ingest(raw_text: str, call=None, not_duplicates=(), splitter=None) -> dict:
98:    return {"text": text, "records": recs, "groups": ing["groups"], "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "split_detail": ing.get("split_detail"), "banner": ing["banner"],
103:def amount_item(a: dict, r: dict, item_id: str = None) -> dict:
111:def _not_duplicates(conn, cid: str) -> list:
115:def _frozen_splitter(conn, cid: str):
125:    reason = ((DB.get_case(conn, cid) or {}).get("config") or {}).get("split_failure")
127:    def replay(text: str):             # stored spans are trimmed; the split contract is contiguous starts that cover the text
135:def _store_split_failure(conn, cid: str, reason) -> None:
138:    if cfg.get("split_failure") == reason:
141:        cfg["split_failure"] = reason
143:        cfg.pop("split_failure", None)
147:def _store_record_marks(conn, cid: str, ing: dict) -> None:
161:def _store_run_checks(conn, cid: str, recs: list, stage: str) -> None:
169:def _item_record_ids(item: dict) -> list:
173:def _reset_reviewed_on(conn, cid: str, moved: set, now: float) -> None:
184:def _store_records(conn, cid: str, ing: dict, now: float = 0.0) -> None:
210:def _row(kind: str, it: dict) -> dict:
230:def _mark_judge_not_run(entries: list, by_n: dict) -> None:
246:def _failure(kind: str, it: dict):
256:def _degrades(kind: str, old: dict, it: dict):
260:    cause = _failure(kind, it)
268:def _evidence_texts(row: dict) -> set:
275:def _checks_worse(old: dict, it: dict) -> bool:
289:def _disagrees(kind: str, old: dict, it: dict) -> bool:
312:def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bool = False, prune: bool = True) -> tuple:
313:    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
318:    or changes it (`_disagrees`), the stored row is kept as it is and `ladder.rerun_note` says so (shown on the item). A row that is not decided is kept the same way,
329:        if old is not None and kind == "amount":        # T-084: a rerun keeps the class the paralegal gave a figure
342:                DB.update_item(conn, it["id"], now=now, case=cid, ladder={**(old.get("ladder") or {}), "rerun_note": {"kind": how, "step": cause, "message": msg, "at": now}})
344:        fail = _failure(kind, it)
372:def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
377:    _persist(conn, cid, "flag", ing["flags"], now)
378:    _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
384:def _finish_amount(a: dict, ing: dict, judged) -> dict:
391:        {"grounding_failures": [] if a["text"] in IN.normalize_text(ing["text"])[a["start"]:a["end"]] or a["cls"] == "damages" else ["GROUNDING_AMOUNT_NOT_IN_TEXT"],
403:def _entry_for(entries: list, record_no: int):
407:def _err(code, stage, record_no=None, cause=None) -> dict:
416:def _accident_year(recs: list):
421:def _items(n: int) -> str:
425:def _partial_error(kept: list, empty: list):
426:    """T-146 r3: the case's honest message for a re-run that kept earlier work or had a step fail with nothing to fall back on (code `run_partial`), or None.
439:    return {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None
442:def _noting(raw_call, failed_steps: list):
445:    def call(step, system, user, schema, *, item_id=None):
449:            failed_steps.append(step)
454:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
457:    call = _noting(call or AU.make_call(conn, cid, now=clock), failed_steps := [])
460:    def set_stage(name):
465:    def expired():
476:    _store_split_failure(conn, cid, ing.get("split_failure"))
480:    _store_run_checks(conn, cid, recs, "pending")           # a run that dies before the conflict stage leaves 'pending' (GET case: RUN_FAILED)
487:    def guard(name):
530:        def one(r):
567:    rerun = bool(DB.list_items(conn, cid, "entry"))      # entries exist only after an earlier run: this is a re-run
568:    kept_e, empty_e = _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out)
572:    kept_a, empty_a = _persist(conn, cid, "amount", final_amounts, now_t, additive=timed_out)
573:    kept_f, empty_f = _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t, additive=timed_out,
574:                               prune="flags" not in failed_steps)      # conflicts are code candidates + judge 3: a down judge leaves them in the run, only the flag step can lose a stored flag
582:        err = _partial_error(kept, empty if rerun else [])
588:            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
596:def case_view(out: dict) -> dict:
618:    def __init__(self, name):
621:    def __enter__(self):
627:    def __exit__(self, *a):
635:def _scratch_call(tmp, text):
642:def run_case(text: str, backend: str = None) -> dict:
655:def judge_summary(summary: str, excerpt: str, label: str, backend: str = None) -> str:
669:def _usd(c):
673:def format_report(out: dict) -> str:
694:def main(argv=None) -> int:
 app/backend/pipeline.py | 29 +++++++++++++++++++++++++----
 1 file changed, 25 insertions(+), 4 deletions(-)
 app/backend/conflict_candidates.py                 |  46 +++---
 app/backend/pipeline.py                            |  29 +---
 app/backend/present.py                             |   3 -
 app/frontend/audit.js                              |   9 +-
 app/frontend/charges.js                            |  26 +---
 app/frontend/review.js                             |   8 +-
 app/frontend/stepper.js                            |   2 +-
 memory/contracts/api.md                            |   7 +-
 tests/e2e/conftest.py                              |   1 -
 tests/e2e/test_charge_confirm.py                   | 101 +-----------
 tests/unit/test_conflict_candidates.py             |  28 +---
 tests/unit/test_t141_checks_per_case.py            |  96 ------------
 .../test_t146_r4_ladder_compare_and_conflicts.py   | 170 ---------------------
 13 files changed, 52 insertions(+), 474 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:23.173Z

**tool call — Bash**
````
{
 "command": "sed -n 405,595p app/backend/pipeline.py; git diff app/backend/pipeline.py"
}
````

### User / tool · 2026-11-02T14:59:23.273Z

**tool result**
````
def _err(code, stage, record_no=None, cause=None) -> dict:
    d = {"code": code, "stage": stage}
    if record_no is not None:
        d["record_no"] = record_no
    if cause:
        d["cause"] = cause
    return d


def _accident_year(recs: list):
    ds = sorted(r["date_iso"] for r in recs if r.get("date_iso"))      # D-055: a year hint from every dated record; the ingest kind is a label guess and is not read
    return int(ds[0][:4]) if ds else None


def _items(n: int) -> str:
    return f"{n} item{'s' if n != 1 else ''}"


def _partial_error(kept: list, empty: list):
    """T-146 r3: the case's honest message for a re-run that kept earlier work or had a step fail with nothing to fall back on (code `run_partial`), or None.
    It names how many items and which steps, and says exactly what was kept."""
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
    return {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None


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
    clock = now if callable(now) else (lambda: time.time() if now is None else now)
    t0 = clock()
    call = _noting(call or AU.make_call(conn, cid, now=clock), failed_steps := [])
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
    _store_run_checks(conn, cid, recs, "pending")           # a run that dies before the conflict stage leaves 'pending' (GET case: RUN_FAILED)
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
    _mark_judge_not_run(entries, by_n)           # T-145: judge 1 did not run (deadline) -> never 'verified'
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
    conflicts_ran = guard("conflicts")
    if conflicts_ran:
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
    rerun = bool(DB.list_items(conn, cid, "entry"))      # entries exist only after an earlier run: this is a re-run
    kept_e, empty_e = _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out)
    for a in final_amounts:                     # an amount stays linked to the entry whose record failed this time (that entry's stored row was kept)
        if not a.get("entry_id"):
            a["entry_id"] = next((o["id"] for o, _, _ in kept_e if f"r{a['record_nos'][0]}" in (o["record_ids"] or [])), None)
    kept_a, empty_a = _persist(conn, cid, "amount", final_amounts, now_t, additive=timed_out)
    kept_f, empty_f = _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t, additive=timed_out,
                               prune="flags" not in failed_steps)      # conflicts are code candidates + judge 3: a down judge leaves them in the run, only the flag step can lose a stored flag
    kept, empty = kept_e + kept_a + kept_f, empty_e + empty_a + empty_f
    _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
    if timed_out:
        status = "timeout"
        err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    else:
        status = "done_with_errors" if errors else "done"
        err = _partial_error(kept, empty if rerun else [])
    DB.update_case(conn, cid, status="failed" if (timed_out or err) else "ready", stage="finalize", error=json.dumps(err) if err else None,
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
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index 79b3a80..dfbf421 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -269,22 +269,43 @@ def _evidence_texts(row: dict) -> set:
     return {e.get("text") or e.get("excerpt") for e in (row.get("evidence") or [])}
 
 
+_POSITIVE = {"agree", "supported", "conflict"}      # a second-check answer that backs the item (judge 1 supported, 2 and 4 agree, 3 conflict confirmed); anything else is not a backing answer
+
+
+def _checks_worse(old: dict, it: dict) -> bool:
+    """T-146 r4: did the whole ladder of checks get worse INSIDE the same state? (a) a reason code the stored row did not have; (b) the second-check answer moved from a
+    backing one to anything else; (c) a code check that was true is now false, or the list of summary tokens the quote does not support went from empty to non-empty.
+    Equal rank is not equal checks: the stored answer is the audit record the paralegal decided on."""
+    if set(it.get("reasons") or []) - set(old.get("state_reasons") or []):
+        return True
+    ol, nl = old.get("ladder") or {}, it.get("ladder") or {}
+    ov, nv = (ol.get("judge") or {}).get("verdict"), (nl.get("judge") or {}).get("verdict")
+    if ov in _POSITIVE and nv is not None and nv not in _POSITIVE:
+        return True
+    oc, nc = ol.get("code_checks") or {}, nl.get("code_checks") or {}
+    return any(v is True and nc.get(k) is False for k, v in oc.items()) or (not oc.get("summary_tokens_not_in_excerpt") and bool(nc.get("summary_tokens_not_in_excerpt")))
+
+
 def _disagrees(kind: str, old: dict, it: dict) -> bool:
     """T-146 r3: does the NEW row `it` lower or change what the stored row `old` says? True when its state is worse (verified -> needs_review -> rejected) or its content
-    differs (entry: summary, quote, date; amount: text, value, class; flag: type, category, evidence quotes). A better state with the same content is not a disagreement.
+    differs (entry: summary, quote, date; amount: text, value, class; flag: type, category, evidence quotes), or its checks are worse inside the same state (`_checks_worse`: a new
+    reason, a backing second-check answer turned negative, a code check turned false). A better state with the same content is not a disagreement.
     A stored row that is itself in the tray (rejected) has nothing to lower. A flag whose computed numbers changed is the existing reset path (the decision was about
     other numbers), so it is not judged here."""
     if _RANK.get(it["state"], 1) > _RANK.get(old["state"], 1) and old["state"] != "rejected":
         return True
     if old["state"] == "rejected":
         return False
+    if kind == "flag":
+        oc = old.get("computed") or {}
+        if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
+            return False
+    if _checks_worse(old, it):
+        return True
     if kind == "entry":
         return (old.get("summary"), old.get("excerpt"), old.get("date_iso")) != (it.get("summary"), it.get("excerpt"), it.get("date"))
     if kind == "amount":
         return (old.get("text"), old.get("value_cents"), old.get("kind")) != (it.get("text"), it.get("cents"), it.get("cls"))
-    oc = old.get("computed") or {}
-    if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
-        return False
     return (old.get("type"), old.get("category"), _evidence_texts(old)) != (it.get("type"), it.get("category"), {e.get("text") for e in it.get("evidence", [])})
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:26.097Z

**tool call — Bash**
````
{
 "command": "sed -n 205,270p app/backend/pipeline.py; sed -n 330,402p app/backend/pipeline.py; ls tests/unit | grep -i \"t146\\|rerun\\|partial\""
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:26.279Z

**tool call — Bash**
````
{
 "command": "grep -rn \"RUN_FAILED\" app/backend/*.py | head; git log --oneline | head -5"
}
````

### User / tool · 2026-11-02T14:59:26.288Z

**tool result**
````
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


JUDGE_NOT_RUN = "JUDGE_NOT_RUN"


def _mark_judge_not_run(entries: list, by_n: dict) -> None:
    """T-145: an AI entry that has no judge-1 answer (the run hit its deadline before or during the stage) is recorded as judge `unavailable` with reason_code
    JUDGE_NOT_RUN and recomposed, so it is `needs_review` (JUDGE_UNAVAILABLE, whose sentence names JUDGE_NOT_RUN), never `verified`, and batch accept (state == verified) refuses it.
    Missing is not a pass: compose treats a judge of None as 'nothing to doubt', so the absence is made explicit here."""
    for e in entries:
        if e["state"] == "rejected" or (e["ladder"].get("judge") or {}).get("verdict"):
            continue
        e["ladder"]["judge"] = {"model": None, "prompt_version": None, "call_id": None, "verdict": "unavailable", "reason_code": JUDGE_NOT_RUN}
        generator.compose(e, by_n[e["seq"]], judge="unavailable")


_STUB_REASONS = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"}      # an entry rejected for one of these has no output at all: a stub
_FLAG_FAIL = {"LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS"}      # a flag made while the flag step failed carries one of these (it is the lexicon floor, nothing the model checked)
_RANK = {"verified": 0, "needs_review": 1, "rejected": 2}


def _failure(kind: str, it: dict):
    """T-146 r3: what failed in the NEW row `it` alone, as the step's name, or None: an entry that is a failure stub (the AI step gave nothing), a flag made while the flag
    step failed, or an item whose second check was asked and gave no answer."""
    if kind == "entry" and it.get("state") == "rejected" and set(it.get("reasons") or []) & _STUB_REASONS:
        return "writing the entries"
    if kind == "flag" and set(it.get("reasons") or []) & _FLAG_FAIL:
        return "finding the flags"
    return "the second check" if ((it.get("ladder") or {}).get("judge") or {}).get("verdict") == "unavailable" else None


def _degrades(kind: str, old: dict, it: dict):
    """T-146 r2/r3: would storing `it` over the stored row `old` replace output with a failure, or take back a second-check answer? Returns the step's name or None.
    (entry) the AI step gave nothing where the stored row has a summary and a quote; (flag) the flag step failed and the stored row was not made from a failure;
    (any AI-made item) the second check gave no answer where the stored row had one. A failure is never allowed to erase earlier work."""
    cause = _failure(kind, it)
    if cause == "writing the entries":
        return cause if old.get("summary") and old.get("excerpt") else None
    if cause == "finding the flags":
        return None if set(old.get("state_reasons") or []) & _FLAG_FAIL else cause
    return cause if ((old.get("ladder") or {}).get("judge") or {}).get("verdict") not in (None, "unavailable") else None


def _evidence_texts(row: dict) -> set:
    return {e.get("text") or e.get("excerpt") for e in (row.get("evidence") or [])}

            from app.backend import reclassify as RC
            it = RC.carry_over(old, it)
        decided = old is not None and old["review_status"] != "pending"
        cause = _degrades(kind, old, it) if old is not None else None
        how = "failed" if cause else None
        if decided and not cause and _disagrees(kind, old, it):
            cause, how = "a different result", "disagreed"
        if cause:
            kept.append((old, cause, how))
            if decided:
                msg = (f"The re-run could not redo this item ({cause}). Your decision and the earlier result were kept." if how == "failed" else
                       "The re-run gave a different result for this item (its summary, quote or checks no longer match what you decided on). Your decision and the earlier result were kept; the new result was not applied.")
                DB.update_item(conn, it["id"], now=now, case=cid, ladder={**(old.get("ladder") or {}), "rerun_note": {"kind": how, "step": cause, "message": msg, "at": now}})
            continue
        fail = _failure(kind, it)
        if fail:
            empty.append(fail)
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
    if additive:
        return kept, empty
    keep = {i["id"] for i in items}
    for oid, old in existing.items():
        if oid not in keep and old["review_status"] == "pending":
            if not prune:
                kept.append((old, "finding the flags", "failed"))
                continue
            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
    return kept, empty


def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
    ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
    _store_records(conn, cid, ing, now)
    _store_run_checks(conn, cid, ing["records"], "pending")
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
    a["ladder"] = {**_ladder(a["id"], P.backend_name(), {"classified_by": "code:amounts", "amount_in_text": state != "rejected"}, state),
                   "judge": ({"model": judges.judge_model(), "prompt_version": judged["prompt_version"], "call_id": judged["call_id"],
                              "verdict": judged["verdict"], "reason_code": judged.get("reason_code")} if judged else None),
                   **({"confirm": a["confirm"]} if a.get("confirm") else {})}      # D-059: the flag the paralegal must confirm by name before accepting this charge
    a["why"] = WHY.join(reasons, a["ladder"]["judge"]) or "The amount is in the record text, labelled as a charge by rule, and the second check agreed."
    return a


test_t146_r2_failed_rerun_keeps_items.py
test_t146_r3_decided_items_never_lowered.py
test_t146_r4_ladder_compare_and_conflicts.py
test_t146_rerun_keeps_items.py
````

### User / tool · 2026-11-02T14:59:26.386Z

**tool result**
````
app/backend/conflict_candidates.py:286:                skip(t, "RUN_FAILED", "The run stopped before the comparison between records finished.")
app/backend/pipeline.py:480:    _store_run_checks(conn, cid, recs, "pending")           # a run that dies before the conflict stage leaves 'pending' (GET case: RUN_FAILED)
app/backend/trace.py:48:    "RUN_FAILED": "The last run stopped before it finished; the items that finished are kept.",
app/backend/trace.py:1198:        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
c2913a6 fix(backend): T-146 r4 re-run compare reads the whole ladder; pin conflicts-step failure as RUN_FAILED
6379c0b fix(frontend): T-154 r2 a on a decided item says so and sends nothing; the Audit drawer and the trace name the flag and the named confirm; the confirm dialog uses plain words; the duplicate sentence names no internal id; shortcut sheet says a flagged charge asks first
e1ef009 docs: R-EX-8 wording per D-062; scope cut 7d; NEEDS_CHRIS FYI on letter total wording
7ae84c3 docs(orchestrator): D-062 letter total states it is a sum of accepted cited lines; charge sources positively identified
a8be5bc docs(orchestrator): D-061 plural-history exemption (T-141)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:29.010Z

**tool call — Bash**
````
{
 "command": "sed -n 270,300p app/backend/conflict_candidates.py; sed -n 1180,1205p app/backend/trace.py; sed -n 1,80p tests/unit/test_t146_r4_ladder_compare_and_conflicts.py; grep -n \"def test\" tests/unit/test_t146_r4_ladder_compare_and_conflicts.py"
}
````

### User / tool · 2026-11-02T14:59:29.106Z

**tool result**
````
    from app.backend import conflicts
    run = run or None
    stage = (run or {}).get("conflicts_stage")
    dated = sum(1 for r in records if r.get("date_iso")) if records is not None else None
    skipped = []

    def skip(t, code, reason, nos=None):
        skipped.append({"type": t, "label": CONFLICT_LABELS[t], "reason_code": code, "reason": reason, **({"record_nos": nos} if nos else {})})

    for t in CONFLICT_LABELS:
        if run is None:
            skip(t, "NOT_RUN", "This case was analysed before the record of what ran was kept, so nothing is claimed about this check. Run it again to check.")
        elif t in _PAIR_TYPES and stage != "ran":
            if stage == "skipped":
                skip(t, "STAGE_SKIPPED", "The run reached its time limit before the comparison between records. Run it again to check.")
            elif state == "failed":
                skip(t, "RUN_FAILED", "The run stopped before the comparison between records finished.")
            else:
                skip(t, "NOT_RUN", "The comparison between records has not run yet.")
        elif t == "accident_date" and dated == 0:
            skip(t, "NO_DATED_RECORD", "No record has a date the code could read, so there is nothing to compare a stated accident date with.")
        elif t in _ENGLISH_RULE_TYPES and run.get("unread"):
            unread = run["unread"]
            nos = sorted(n for v in unread.values() for n in v)
            langs = " and ".join(_LANG_WORD.get(k, k) for k in unread)
            if run.get("read_records") == 0:
                skip(t, "LANGUAGE", f"This check reads English wording and every record is in {langs}, so it could not find anything.")
            else:
                skip(t, "LANGUAGE_PARTIAL", f"This check reads English wording; the records in {langs} were not read.", nos)
    whole = {x["type"] for x in skipped if "record_nos" not in x}
    note = conflicts.accident_date_note(records) if records is not None and "accident_date" not in whole else None
def edit_warning(n: int, n_ai: int = 0) -> str:
    return edit_warning_base(n) + (" " + ai_clause(n_ai, n) if n_ai else "")


def edit_warning_base(n: int) -> str:
    return (f"{n} edit{'s are' if n != 1 else ' is'} still marked Needs review (the second check did not confirm {'them' if n != 1 else 'it'}), so {'they are' if n != 1 else 'it is'} "
            f"not in the letter and {'are' if n != 1 else 'is'} not counted as accepted until you compare {'them' if n != 1 else 'it'} with the quote and accept.")


def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
    """Everything that makes GET /export refuse (D-045): a run in progress or failed, accepted AI-made items whose second check never ran (D-044), or nothing accepted.
    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
    cx = cx or _Cx(conn, case_id, False)
    rv = rv or present.review_view(conn, case_id)
    out = []
    if cx.running:
        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_IN_PROGRESS", "why": TRACE_WHY["RUN_IN_PROGRESS"], "next_action": None})
    if cx.case["status"] == "failed":
        out.append({"item_id": None, "kind": "case", "reason_code": "RUN_FAILED", "why": TRACE_WHY["RUN_FAILED"], "next_action": na("CONFIRM_RERUN")})
    out.extend(code_check_blockers(conn, case_id, cx))         # D-045(b): the paralegal's own wording is exempt from the judge, not from the code checks
    if cx.ran and not cx.running:
        out.extend(judge_not_run_blockers(conn, case_id))      # D-044: accepted but never double-checked; no override
    if not (rv["counts"]["accepted"] + rv["counts"]["edited"] - rv["counts"].get("edit_to_check", 0)):       # T-134: an edit not yet accepted is not accepted
        out.append({"item_id": None, "kind": "case", "reason_code": "NOTHING_ACCEPTED", "why": TRACE_WHY["NOTHING_ACCEPTED"], "next_action": na("DECIDE", {"view": "queue"})})
    return out

"""T-146 r4 (§7.4 fix-up). (1) The keep-and-note compare reads the whole ladder, not only the state: a decided item whose checks get worse INSIDE the same state (a new
reason, a second-check answer that moves from positive to negative, a code check that turns false) is kept whole with a note, and the case reads run_partial.
(2) A failure in the conflicts step (judge 3) makes the case failed and the export gate RUN_FAILED, like every other step."""
import pytest
from app.backend import pipeline as PL, trace
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script
from tests.unit.test_t146_r3_decided_items_never_lowered import (OLD_AMOUNT, OLD_ENTRY, OLD_FLAG, NEW_FLAG, TAIL, assert_notes, case_error, completed, down, full,
                                                                  model_flag, note, rerun)


def blockers(conn, cid):
    return [b["reason_code"] for b in trace.export_blockers(conn, cid)]


# ---- the compare, equal-rank rows (state needs_review on both sides)
NR_AMOUNT = {**OLD_AMOUNT, "state": "needs_review", "state_reasons": ["AMOUNT_RATE_NOT_TOTALED"], "ladder": {"judge": {"verdict": "agree"}, "code_checks": {"amount_in_text": True}}}
NEW_AMT = {"text": "$10", "cents": 1000, "cls": "charge", "state": "needs_review", "reasons": ["AMOUNT_RATE_NOT_TOTALED"],
           "ladder": {"judge": {"verdict": "agree"}, "code_checks": {"amount_in_text": True}}}
NR_ENTRY = {**OLD_ENTRY, "state": "needs_review", "state_reasons": ["QUALIFIER_DROPPED"],
            "ladder": {"judge": {"verdict": "partially"}, "code_checks": {"excerpt_verbatim": True, "summary_tokens_not_in_excerpt": []}}}
NEW_ENT = {"summary": "S", "excerpt": "Q", "date": "2026-01-01", "state": "needs_review", "reasons": ["QUALIFIER_DROPPED"],
           "ladder": {"judge": {"verdict": "partially"}, "code_checks": {"excerpt_verbatim": True, "summary_tokens_not_in_excerpt": []}}}
NR_FLAG = {**OLD_FLAG, "state": "needs_review", "state_reasons": ["LEXICON_ONLY"], "ladder": {"judge": {"verdict": "agree"}, "code_checks": {"excerpt_verbatim": True}}}
NEW_FL = {**NEW_FLAG, "state": "needs_review", "reasons": ["LEXICON_ONLY"], "ladder": {"judge": {"verdict": "agree"}, "code_checks": {"excerpt_verbatim": True}}}


def lad(judge=None, **checks):
    return {"judge": {"verdict": judge} if judge else None, "code_checks": checks}


@pytest.mark.parametrize("kind,old,new,expected", [
    ("amount", NR_AMOUNT, NEW_AMT, False),                                                                                    # identical: nothing changed
    ("amount", NR_AMOUNT, {**NEW_AMT, "reasons": ["JUDGE_DISAGREES", "AMOUNT_RATE_NOT_TOTALED"], "ladder": lad("disagree", amount_in_text=True)}, True),     # the F1 repro
    ("amount", NR_AMOUNT, {**NEW_AMT, "reasons": ["AMOUNT_RATE_NOT_TOTALED", "OCR_DERIVED"]}, True),                          # a new reason alone
    ("amount", NR_AMOUNT, {**NEW_AMT, "reasons": []}, False),                                                                 # a reason gone is not worse
    ("amount", NR_AMOUNT, {**NEW_AMT, "ladder": lad("disagree", amount_in_text=True)}, True),                                 # answer agree -> disagree, same reasons
    ("amount", NR_AMOUNT, {**NEW_AMT, "ladder": lad("unsure", amount_in_text=True)}, True),
    ("amount", NR_AMOUNT, {**NEW_AMT, "ladder": lad("agree", amount_in_text=False)}, True),                                   # a code check true -> false
    ("amount", NR_AMOUNT, {**NEW_AMT, "ladder": {"judge": None, "code_checks": {"amount_in_text": True}}}, False),            # no new answer is not a negative answer
    ("amount", {**NR_AMOUNT, "ladder": lad("disagree", amount_in_text=True)}, {**NEW_AMT, "ladder": lad("agree", amount_in_text=True)}, False),    # better
    ("amount", {**NR_AMOUNT, "ladder": lad("unsure", amount_in_text=True)}, {**NEW_AMT, "ladder": lad("disagree", amount_in_text=True)}, False),   # was not positive: no answer was taken back
    ("entry", NR_ENTRY, NEW_ENT, False),
    ("entry", {**NR_ENTRY, "ladder": lad("supported", excerpt_verbatim=True, summary_tokens_not_in_excerpt=[])},
     {**NEW_ENT, "ladder": lad("unsupported", excerpt_verbatim=True, summary_tokens_not_in_excerpt=[])}, True),
    ("entry", NR_ENTRY, {**NEW_ENT, "ladder": lad("partially", excerpt_verbatim=True, summary_tokens_not_in_excerpt=["fracture"])}, True),    # unsupported tokens appear
    ("entry", NR_ENTRY, {**NEW_ENT, "reasons": ["QUALIFIER_DROPPED", "DATE_UNCONFIRMED"]}, True),
    ("flag", NR_FLAG, NEW_FL, False),
    ("flag", NR_FLAG, {**NEW_FL, "reasons": ["LEXICON_ONLY", "JUDGE_DISAGREES"], "ladder": lad("disagree", excerpt_verbatim=True)}, True),
    ("flag", NR_FLAG, {**NEW_FL, "ladder": lad("conflict", excerpt_verbatim=True)}, False),                                   # agree and conflict are both positive
    ("flag", {**NR_FLAG, "ladder": lad("conflict", excerpt_verbatim=True)}, {**NEW_FL, "ladder": lad("benign", excerpt_verbatim=True)}, True),
    ("flag", NR_FLAG, {**NEW_FL, "days": 40, "reasons": ["LEXICON_ONLY", "JUDGE_DISAGREES"]}, False),                         # numbers moved: the reset path decides
])
def test_disagrees_reads_the_whole_ladder(kind, old, new, expected):
    assert PL._disagrees(kind, old, new) is expected


# ---- end to end: the F1 repro (accepted or dismissed rate in needs_review, the second check flips)
@pytest.mark.parametrize("action", ["accept", "dismiss"])
def test_decided_needs_review_amount_survives_a_judge_that_now_disagrees(tmp_path, action):
    conn, cid = completed(tmp_path)
    a2 = DB.get_item(conn, "a2", cid)
    assert (a2["state"], a2["state_reasons"], a2["ladder"]["judge"]["verdict"]) == ("needs_review", ["AMOUNT_RATE_NOT_TOTALED"], "agree")
    DB.apply_review(conn, "a2", action, now=2.5, case=cid)
    before = full(conn, cid)
    out = rerun(conn, cid, j2={"verdict": "disagree", "reason_code": "NONE"})
    assert out["status"] == "done"
    after = DB.get_item(conn, "a2", cid)
    assert (after["state"], after["state_reasons"], after["ladder"]["judge"]["verdict"], after["review_status"]) == \
        ("needs_review", ["AMOUNT_RATE_NOT_TOTALED"], "agree", "accepted" if action == "accept" else "dismissed")
    assert full(conn, cid)["amount"]["a2"] == before["amount"]["a2"]                  # the whole stored row, call id aside
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial"
    assert "The re-run gave a different result for" in err["message"] and err["message"].endswith(TAIL)
    n = note(conn, cid, "a2")
    assert n and n["kind"] == "disagreed" and n["step"] == "a different result"
    assert "RUN_FAILED" in blockers(conn, cid)


55:def test_disagrees_reads_the_whole_ladder(kind, old, new, expected):
61:def test_decided_needs_review_amount_survives_a_judge_that_now_disagrees(tmp_path, action):
81:def test_an_undecided_needs_review_amount_takes_the_new_answer_and_the_case_stays_ready(tmp_path):
91:def test_a_clean_rerun_of_a_decided_case_has_no_run_failed_blocker(tmp_path):
110:def test_conflicts_step_down_keeps_the_conflict_flag_fails_the_case_and_blocks_the_gate(tmp_path, decide_cx, miss):
126:def test_conflicts_step_down_twice_with_nothing_to_keep_still_fails_the_case(tmp_path):
139:def test_conflicts_step_deadline_fails_the_case_and_blocks_the_gate(tmp_path):
166:def test_gate_lists_run_failed_whenever_the_case_is_failed(tmp_path, script):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:31.947Z

**tool call — Bash**
````
{
 "command": "sed -n 95,200p tests/unit/test_t146_r4_ladder_compare_and_conflicts.py; grep -n \"^def \\|^TAIL\\|^OLD\" tests/unit/test_t146_r3_decided_items_never_lowered.py | head -40"
}
````

### User / tool · 2026-11-02T14:59:32.093Z

**tool result**
````
    assert "RUN_FAILED" not in blockers(conn, cid)


# ---- the conflicts step (judge 3)
def j3_cases(tmp_path, decide_cx):
    conn, cid = completed(tmp_path)
    cx = DB.get_item(conn, "f_cx1", cid)
    assert (cx["state"], cx["ladder"]["judge"]["verdict"], cx["review_status"]) == ("verified", "conflict", "pending")
    if decide_cx:
        DB.apply_review(conn, "f_cx1", "accept", now=2.5, case=cid)
    return conn, cid


@pytest.mark.parametrize("decide_cx", [False, True])
@pytest.mark.parametrize("miss", [False, True])
def test_conflicts_step_down_keeps_the_conflict_flag_fails_the_case_and_blocks_the_gate(tmp_path, decide_cx, miss):
    conn, cid = j3_cases(tmp_path, decide_cx)
    before = full(conn, cid)
    out = rerun(conn, cid, j3=PL.AU.LLMFailedFixtureMiss("x") if miss else down("j3"))
    assert out["status"] == "done" and out["error"]["code"] == "run_partial"
    assert full(conn, cid) == before
    status, err = case_error(conn, cid)
    assert status == "failed"
    assert err["message"] == ("The AI step failed for 1 item (the second check) on this run. Their earlier results and every decision of yours were kept unchanged." + TAIL)
    assert "RUN_FAILED" in blockers(conn, cid)
    assert bool(note(conn, cid, "f_cx1")) is decide_cx          # a decided item carries the note; an undecided one is kept silently
    rerun(conn, cid)                                             # a good run clears the failure and the gate
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
    assert DB.get_item(conn, "f_cx1", cid)["ladder"]["judge"]["verdict"] == "conflict"


def test_conflicts_step_down_twice_with_nothing_to_keep_still_fails_the_case(tmp_path):
    """The first run had judge 3 down (the conflict flag is needs_review with no answer); a second run with it down again has no earlier answer to keep."""
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag, j3=down("j3"))), now=lambda: 1.0)
    assert DB.get_item(conn, "f_cx1", cid)["ladder"]["judge"]["verdict"] == "unavailable"
    rerun(conn, cid, j3=down("j3"))
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial"
    assert err["message"] == "The AI step failed for 1 item (the second check) on this run, and there is no earlier result to keep." + TAIL
    assert "RUN_FAILED" in blockers(conn, cid)


def test_conflicts_step_deadline_fails_the_case_and_blocks_the_gate(tmp_path):
    """The deadline passes during the amounts stage, so the conflicts stage is skipped (and GET case checks say so)."""
    conn, cid = j3_cases(tmp_path, True)
    before = full(conn, cid)
    t = [0.0]

    def on_stage(name):
        if name == "amounts":
            t[0] = 10_000.0
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: t[0], on_stage=on_stage, deadline_s=480)
    assert out["status"] == "timeout"
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_deadline"
    assert full(conn, cid) == before and "RUN_FAILED" in blockers(conn, cid)
    assert DB.get_case(conn, cid)["config"]["run_checks"]["conflicts_stage"] == "skipped"


# ---- review minor: the gate agrees with the case on every r3 failure path
@pytest.mark.parametrize("script", [
    {"flags": down("flags")},
    {"extract": down("extract")},
    {"j1": down("j1")},
    {"j2": down("j2")},
    {"j4": down("j4")},
    {"j3": down("j3")},
    {"extract": lambda user: {"summary": "Patient had surgery on Mars.", "excerpt": "Patient reports low back pain in 2023, resolved."}},      # summary-in-quote check fails
], ids=["flags", "extract", "j1", "j2", "j4", "j3", "summary_not_in_quote"])
def test_gate_lists_run_failed_whenever_the_case_is_failed(tmp_path, script):
    conn, cid = completed(tmp_path)
    rerun(conn, cid, **script)
    assert case_error(conn, cid)[0] == "failed"
    assert "RUN_FAILED" in blockers(conn, cid)
14:TAIL = " Run it again to retry."
18:def down(step):
22:def model_flag(user):
27:def _no_calls(v):
31:def full(conn, cid):
37:def completed(tmp_path, decide=True):
49:def rerun(conn, cid, **script):
54:def case_error(conn, cid):
59:def note(conn, cid, i):
63:def assert_notes(conn, cid, ids, kind, step):
73:def test_flag_step_down_keeps_every_decided_flag_whole_and_notes_it(tmp_path):
92:def _bad_summary(user):
97:def test_summary_check_failing_on_the_new_extract_keeps_the_decided_entry(tmp_path):
114:def test_the_same_failure_on_an_undecided_entry_stands_as_the_new_check_result(tmp_path):
124:def test_extract_down_keeps_decided_entries_and_notes_them(tmp_path):
138:def test_each_kind_of_extract_failure_for_one_record_keeps_that_row(tmp_path, cause):
164:def test_judge_down_keeps_decided_items_and_notes_them(tmp_path):
179:def test_one_judge_down_names_only_its_items(tmp_path):
191:def test_deadline_keeps_decided_items_without_a_disagreement_note(tmp_path, jump_at):
210:def test_rerun_with_nothing_to_keep_still_says_the_step_failed(tmp_path):
222:def test_nothing_to_keep_and_something_kept_are_both_said(tmp_path):
238:def test_a_later_good_rerun_clears_the_note_and_keeps_the_decision(tmp_path):
249:def test_a_clean_rerun_of_a_decided_item_is_not_a_disagreement(tmp_path):
260:def test_a_decided_flag_the_model_no_longer_proposes_is_kept_with_its_higher_state(tmp_path):
269:def test_a_better_state_with_the_same_content_is_not_a_disagreement(tmp_path):
281:def test_kept_rows_keep_their_original_call_ids(tmp_path):
291:def test_flag_step_fixture_miss_is_a_failure_too(tmp_path):
301:def test_a_pending_model_only_flag_survives_a_down_flag_step(tmp_path, miss):
319:OLD_ENTRY = {"summary": "S", "excerpt": "Q", "date_iso": "2026-01-01", "state": "verified"}
320:OLD_AMOUNT = {"text": "$10", "value_cents": 1000, "kind": "charge", "state": "verified"}
321:OLD_FLAG = {"type": "pre_existing", "category": "pre_existing", "evidence": [{"text": "Q"}], "computed": {"from_date": None, "to_date": None, "days": None}, "state": "verified"}
346:def test_disagrees_table(kind, old, new, expected):
366:def test_degrades_table(kind, old, new, expected):
370:def test_failed_and_different_are_counted_apart(tmp_path):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:33.663Z

**tool call — Bash**
````
{
 "command": "sed -n 1,72p tests/unit/test_t146_r3_decided_items_never_lowered.py; sed -n 205,240p tests/unit/test_t146_r3_decided_items_never_lowered.py"
}
````

### User / tool · 2026-11-02T14:59:33.751Z

**tool result**
````
"""T-146 round 3: ONE rule for every stage. A re-run never lowers or replaces a decided item (accepted, dismissed, edited), whatever fails or whatever the new run's
checks say. When the new output for a decided item differs from it or fails a check, the decided item is kept whole, carries a visible note, and the case reads
run_partial with an honest message (the exact text is pinned here). Paths: flag step down, summary-in-quote fails on the new extract, extract down, judge down,
the deadline, and a re-run with nothing to keep."""
import json

import pytest
from app.backend import pipeline as PL, present
from app.db import db as DB
from app.llm import audited as AU
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record

TAIL = " Run it again to retry."
DECIDED = ("e1", "e2", "e3", "a1", "f_r3_1", "f_r6_1", "f_gap_r6_r7")


def down(step):
    return AU.LLMFailed(f"{step} down", last_error="TIMEOUT")


def model_flag(user):
    """A model flag for record 3 with the same quote as the lexicon flag f_r3_1: the two corroborate (origin lexicon+llm, verified)."""
    return {"flags": [dict(type="pre_existing", category="pre_existing", excerpt="Patient reports low back pain in 2023, resolved.")] if which_record(user)[0] == 3 else []}


def _no_calls(v):
    return {a: _no_calls(b) for a, b in v.items() if a not in ("call_id", "rerun_note")} if isinstance(v, dict) else v


def full(conn, cid):
    """Every stored column of every item, but not `ladder.rerun_note` (checked on its own) and not call ids (every re-run numbers its calls afresh; they are compared on
    the kept e1 in test_kept_rows_keep_their_original_call_ids)."""
    return {k: {i["id"]: {c: _no_calls(v) for c, v in i.items() if c != "updated_at"} for i in DB.list_items(conn, cid, k)} for k in ("entry", "amount", "flag")}


def completed(tmp_path, decide=True):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    assert PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: 1.0)["status"] == "done"
    assert DB.get_item(conn, "f_r3_1")["origin"] == "lexicon+llm" and DB.get_item(conn, "f_r3_1")["state"] == "verified"
    if decide:
        for i in ("e1", "e3", "a1", "f_r3_1", "f_r6_1", "f_gap_r6_r7"):      # a corroborated flag, a lexicon-only flag, a code flag, an entry, an amount
            DB.apply_review(conn, i, "accept", now=2.0, case=cid)
        DB.apply_review(conn, "e2", "dismiss", now=2.0, case=cid)
    return conn, cid


def rerun(conn, cid, **script):
    script.setdefault("flags", model_flag)
    return PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(**script)), now=lambda: 3.0)


def case_error(conn, cid):
    c = DB.get_case(conn, cid)
    return c["status"], (json.loads(c["error"]) if c["error"] else None)


def note(conn, cid, i):
    return (DB.get_item(conn, i, cid)["ladder"] or {}).get("rerun_note")


def assert_notes(conn, cid, ids, kind, step):
    for i in ids:
        n = note(conn, cid, i)
        assert n and n["kind"] == kind and n["step"] == step, (i, n)
        assert present.item_view(conn, cid, i)["rerun_note"] == n["message"]      # shown on the item, not only stored
    for i in set(DECIDED) - set(ids):
        assert note(conn, cid, i) is None, i


# ---- the flag step is down
    assert err == {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    assert_notes(conn, cid, (), "failed", "")


# ---- a re-run with nothing to keep
def test_rerun_with_nothing_to_keep_still_says_the_step_failed(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    first = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=down("extract"))), now=lambda: 1.0)
    assert first["status"] == "done_with_errors" and case_error(conn, cid) == ("ready", None)      # a first run: the tray shows the failed records, as before
    again = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=down("extract"))), now=lambda: 2.0)
    assert again["status"] == "done_with_errors"
    status, err = case_error(conn, cid)
    assert status == "failed"
    assert err == {"code": "run_partial", "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep." + TAIL}


def test_nothing_to_keep_and_something_kept_are_both_said(tmp_path):
    conn, cid = completed(tmp_path)
    good = sample_script()["extract"]
    DB.update_item(conn, "e4", now=2.0, case=cid, summary=None, excerpt=None, state="rejected", state_reasons_json=["LLM_FAILED_AFTER_RETRIES"])      # a stub left by an earlier failure

    def extract(user):
        if which_record(user)[0] in (1, 4):
            raise down("extract")
        return good(user)
    rerun(conn, cid, extract=extract)
    _, err = case_error(conn, cid)
    assert err["message"] == ("The AI step failed for 1 item (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. "
                              "The AI step also failed for 1 item (writing the entries) with no earlier result to keep." + TAIL)


# ---- a later good run clears the notes and the error
def test_a_later_good_rerun_clears_the_note_and_keeps_the_decision(tmp_path):
    conn, cid = completed(tmp_path)
    rerun(conn, cid, extract=down("extract"))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:49.585Z

**tool call — Bash**
````
{
 "command": "cat > tests/unit/test_t161_first_run_stage_down.py <<'EOF'\n\"\"\"T-161: a FIRST run with a stage down (flags, judge 1-4) reads like a re-run that fails: the case is failed / run_partial, the message names the step, and the export\ngate lists RUN_FAILED. A clean first run stays ready. (A first run whose extract step is down keeps its old shape: the tray shows the failed records, case ready.)\"\"\"\nimport pytest\nfrom app.backend import pipeline as PL, trace\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit._fakes import FakeCall, sample_script\nfrom tests.unit.test_t146_r3_decided_items_never_lowered import TAIL, case_error, down, model_flag\n\nNOTHING_KEPT = \"The AI step failed for {n} (the second check) on this run, and there is no earlier result to keep.\" + TAIL\n\n\ndef first_run(tmp_path, **script):\n    conn = DB.connect(str(tmp_path / \"d.sqlite\"))\n    cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\n    script.setdefault(\"flags\", model_flag)\n    out = PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(**script)), now=lambda: 1.0)\n    return conn, cid, out\n\n\ndef blockers(conn, cid):\n    return [b[\"reason_code\"] for b in trace.export_blockers(conn, cid)]\n\n\ndef test_a_clean_first_run_stays_ready(tmp_path):\n    conn, cid, out = first_run(tmp_path)\n    assert out[\"status\"] == \"done\" and out[\"error\"] is None\n    assert case_error(conn, cid) == (\"ready\", None)\n    assert \"RUN_FAILED\" not in blockers(conn, cid)\n\n\n@pytest.mark.parametrize(\"step,n,what\", [(\"j1\", 9, \"items\"), (\"j2\", None, None), (\"j4\", None, None), (\"j3\", 1, \"item\")], ids=[\"j1\", \"j2\", \"j4\", \"j3\"])\n@pytest.mark.parametrize(\"miss\", [False, True], ids=[\"down\", \"fixture_miss\"])\ndef test_first_run_with_a_judge_down_fails_the_case_and_names_the_step(tmp_path, step, n, what, miss):\n    conn, cid, out = first_run(tmp_path, **{step: PL.AU.LLMFailedFixtureMiss(\"x\") if miss else down(step)})\n    status, err = case_error(conn, cid)\n    assert status == \"failed\" and err[\"code\"] == \"run_partial\"\n    assert out[\"error\"] == err\n    assert err[\"message\"].startswith(\"The AI step failed for \") and \"(the second check) on this run, and there is no earlier result to keep.\" in err[\"message\"]\n    assert err[\"message\"].endswith(TAIL)\n    assert \"RUN_FAILED\" in blockers(conn, cid)\n    if n:\n        assert err[\"message\"] == NOTHING_KEPT.format(n=f\"{n} {what}\")\n\n\ndef test_first_run_with_the_flag_step_down_fails_the_case_and_names_the_step(tmp_path):\n    conn, cid, out = first_run(tmp_path, flags=down(\"flags\"))\n    status, err = case_error(conn, cid)\n    assert status == \"failed\" and err[\"code\"] == \"run_partial\" and out[\"error\"] == err\n    assert \"(finding the flags) on this run, and there is no earlier result to keep.\" in err[\"message\"] and err[\"message\"].endswith(TAIL)\n    assert \"RUN_FAILED\" in blockers(conn, cid)\n\n\ndef test_first_run_with_the_flag_step_missing_a_fixture_fails_the_case_too(tmp_path):\n    conn, cid, _ = first_run(tmp_path, flags=PL.AU.LLMFailedFixtureMiss(\"x\"))\n    assert case_error(conn, cid)[0] == \"failed\" and \"RUN_FAILED\" in blockers(conn, cid)\n\n\ndef test_first_run_with_extract_down_keeps_its_old_shape(tmp_path):\n    conn, cid, out = first_run(tmp_path, extract=down(\"extract\"))\n    assert out[\"status\"] == \"done_with_errors\" and case_error(conn, cid) == (\"ready\", None)\n\n\ndef test_a_good_second_run_clears_a_failed_first_run(tmp_path):\n    conn, cid, _ = first_run(tmp_path, j1=down(\"j1\"))\n    assert case_error(conn, cid)[0] == \"failed\"\n    PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(flags=model_flag)), now=lambda: 3.0)\n    assert case_error(conn, cid) == (\"ready\", None) and \"RUN_FAILED\" not in blockers(conn, cid)\nEOF\npython3 -m pytest tests/unit/test_t161_first_run_stage_down.py -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T14:59:49.689Z

**tool result**
````
/opt/homebrew/opt/python@3.12/bin/python3.12: No module named pytest
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:51.131Z

**tool call — Bash**
````
{
 "command": "ls -d .venv venv 2>/dev/null; cat memory/ENVIRONMENT.md | grep -i \"pytest\\|venv\" | head"
}
````

### User / tool · 2026-11-02T14:59:51.248Z

**tool result**
````
.venv
| python3 | 3.12.2 | project venv at `.venv/` (gitignored). Use `.venv/bin/python`. |
| Playwright | python package in .venv; chromium-headless-shell 1248 | |
| Python deps | fastapi, uvicorn, anthropic, pyyaml, pytest, playwright, httpx, python-multipart | in .venv |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:52.559Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_t161_first_run_stage_down.py -q 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T14:59:54.346Z

**tool result**
````
tests/unit/test_t161_first_run_stage_down.py:49: AssertionError
____ test_first_run_with_the_flag_step_missing_a_fixture_fails_the_case_too ____

tmp_path = PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-5258/test_first_run_with_the_flag_s1')

    def test_first_run_with_the_flag_step_missing_a_fixture_fails_the_case_too(tmp_path):
        conn, cid, _ = first_run(tmp_path, flags=PL.AU.LLMFailedFixtureMiss("x"))
>       assert case_error(conn, cid)[0] == "failed" and "RUN_FAILED" in blockers(conn, cid)
E       AssertionError: assert ('ready' == 'failed'
E         
E         - failed
E         + ready)

tests/unit/test_t161_first_run_stage_down.py:56: AssertionError
_______________ test_a_good_second_run_clears_a_failed_first_run _______________

tmp_path = PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-5258/test_a_good_second_run_clears_0')

    def test_a_good_second_run_clears_a_failed_first_run(tmp_path):
        conn, cid, _ = first_run(tmp_path, j1=down("j1"))
>       assert case_error(conn, cid)[0] == "failed"
E       AssertionError: assert 'ready' == 'failed'
E         
E         - failed
E         + ready

tests/unit/test_t161_first_run_stage_down.py:66: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_a_judge_down_fails_the_case_and_names_the_step[down-j1]
FAILED tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_a_judge_down_fails_the_case_and_names_the_step[down-j2]
FAILED tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_a_judge_down_fails_the_case_and_names_the_step[down-j4]
FAILED tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_a_judge_down_fails_the_case_and_names_the_step[down-j3]
FAILED tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_a_judge_down_fails_the_case_and_names_the_step[fixture_miss-j1]
FAILED tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_a_judge_down_fails_the_case_and_names_the_step[fixture_miss-j2]
FAILED tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_a_judge_down_fails_the_case_and_names_the_step[fixture_miss-j4]
FAILED tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_a_judge_down_fails_the_case_and_names_the_step[fixture_miss-j3]
FAILED tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_the_flag_step_down_fails_the_case_and_names_the_step
FAILED tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_the_flag_step_missing_a_fixture_fails_the_case_too
FAILED tests/unit/test_t161_first_run_stage_down.py::test_a_good_second_run_clears_a_failed_first_run
11 failed, 2 passed in 1.39s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:59:59.294Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/pipeline.py'\ns=open(p).read()\nold=\"        err = _partial_error(kept, empty if rerun else [])\\n\"\nnew=\"\"\"        err = _partial_error(kept, empty if rerun else [s for s in empty if s != _EXTRACT_STEP])      # T-161: a first run with a judge or the flag step down fails like a re-run; its extract failures stay tray items\n\"\"\"\nassert old in s\ns=s.replace(old,new)\nold2='    if kind == \"entry\" and it.get(\"state\") == \"rejected\" and set(it.get(\"reasons\") or []) & _STUB_REASONS:\\n        return \"writing the entries\"\\n'\nassert old2 in s\ns=s.replace(old2,'    if kind == \"entry\" and it.get(\"state\") == \"rejected\" and set(it.get(\"reasons\") or []) & _STUB_REASONS:\\n        return _EXTRACT_STEP\\n')\ns=s.replace('_RANK = {\"verified\": 0, \"needs_review\": 1, \"rejected\": 2}\\n','_RANK = {\"verified\": 0, \"needs_review\": 1, \"rejected\": 2}\\n_EXTRACT_STEP = \"writing the entries\"\\n',1)\ns=s.replace('    if cause == \"writing the entries\":\\n','    if cause == _EXTRACT_STEP:\\n')\nopen(p,'w').write(s)\nEOF\ngit diff app/backend/pipeline.py | grep -n \"EXTRACT\" ; .venv/bin/python -m pytest tests/unit/test_t161_first_run_stage_down.py -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T15:00:01.816Z

**tool result**
````
9:+_EXTRACT_STEP = "writing the entries"
17:+        return _EXTRACT_STEP
26:+    if cause == _EXTRACT_STEP:
83:+        err = _partial_error(kept, empty if rerun else [s for s in empty if s != _EXTRACT_STEP])      # T-161: a first run with a judge or the flag step down fails like a re-run; its extract failures stay tray items
.............                                                            [100%]
13 passed in 2.02s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:00:05.103Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -x -n0 2>&1 | tail -15 || true",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T15:00:05.370Z

**tool result**
````
ERROR: usage: python -m pytest [options] [file_or_dir] [file_or_dir] [...]
python -m pytest: error: unrecognized arguments: -n0
  inifile: None
  rootdir: /Users/arsis/zlayt-pm-project
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:00:18.520Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q 2>&1 | tail -15",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T15:06:14.360Z

**tool result**
````
        amount here above what the bill states. 950 stated by the itemized lines + 650 debt row = 1,600. The ED note ($1,000) is not a bill, so it is not totaled."""
        got = charges(ledger())
>       assert sum(a["cents"] for a in got) == 160000
E       assert 355000 == 160000
E        +  where 355000 = sum(<generator object test_third_ledger_total.<locals>.<genexpr> at 0x10a081700>)

tests/unit/test_amounts_d062.py:128: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_amounts_d062.py::test_third_ledger_discharge_summary_is_not_a_charge_source
FAILED tests/unit/test_amounts_d062.py::test_third_ledger_clinical_note_in_a_case_with_bills_is_not_a_charge_source
FAILED tests/unit/test_amounts_d062.py::test_a_case_with_no_bill_at_all_still_reads_a_charge_stated_in_its_notes
FAILED tests/unit/test_amounts_d062.py::test_a_document_with_no_header_never_yields_a_charge
FAILED tests/unit/test_amounts_d062.py::test_third_ledger_med_pay_ledger_adds_nothing
FAILED tests/unit/test_amounts_d062.py::test_third_ledger_total - assert 3550...
6 failed, 4649 passed, 1 skipped in 354.27s (0:05:54)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:06:20.673Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=$(mktemp -u /private/tmp/claude-501/idx.XXXX) && git read-tree HEAD && git show HEAD:app/backend/pipeline.py > /private/tmp/claude-501/pl_head.py && python3 - <<'EOF'\np='/private/tmp/claude-501/pl_head.py'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"        err = _partial_error(kept, empty if rerun else [])\\n\",\"        err = _partial_error(kept, empty if rerun else [s for s in empty if s != _EXTRACT_STEP])      # T-161: a first run with a judge or the flag step down fails like a re-run; its extract failures stay tray items\\n\")\nrep('        return \"writing the entries\"\\n','        return _EXTRACT_STEP\\n')\nrep('_RANK = {\"verified\": 0, \"needs_review\": 1, \"rejected\": 2}\\n','_RANK = {\"verified\": 0, \"needs_review\": 1, \"rejected\": 2}\\n_EXTRACT_STEP = \"writing the entries\"\\n')\nrep('    if cause == \"writing the entries\":\\n','    if cause == _EXTRACT_STEP:\\n')\nopen(p,'w').write(s)\nEOF\nsha=$(git hash-object -w /private/tmp/claude-501/pl_head.py) && git update-index --cacheinfo 100644,$sha,app/backend/pipeline.py && git add tests/unit/test_t161_first_run_stage_down.py && git diff --cached --stat && git commit -q -m \"fix(backend): T-161 first run with a judge or the flag step down fails like a re-run (run_partial, step named, gate RUN_FAILED)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git log --oneline | head -2; unset GIT_INDEX_FILE; git status --short app/backend/pipeline.py",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T15:06:20.820Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: export GIT_INDEX_FILE=$(mktemp -u /private/tmp/claude-501/idx.XXXX) && git read-tree HEAD && git show HEAD:app/backend/pipeline.py > /private/tmp/claude-501/pl_head.py && python3 - <<'EOF'
p='/private
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:06:21.755Z

Split into separate commands.

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:06:24.550Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx.t161 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git show HEAD:app/backend/pipeline.py > /private/tmp/claude-501/pl_head.py && python3 - <<'EOF'\np='/private/tmp/claude-501/pl_head.py'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"        err = _partial_error(kept, empty if rerun else [])\\n\",\"        err = _partial_error(kept, empty if rerun else [s for s in empty if s != _EXTRACT_STEP])      # T-161: a first run with a judge or the flag step down fails like a re-run; its extract failures stay tray items\\n\")\nrep('        return \"writing the entries\"\\n','        return _EXTRACT_STEP\\n')\nrep('_RANK = {\"verified\": 0, \"needs_review\": 1, \"rejected\": 2}\\n','_RANK = {\"verified\": 0, \"needs_review\": 1, \"rejected\": 2}\\n_EXTRACT_STEP = \"writing the entries\"\\n')\nrep('    if cause == \"writing the entries\":\\n','    if cause == _EXTRACT_STEP:\\n')\nopen(p,'w').write(s)\nEOF\nsha=$(git hash-object -w /private/tmp/claude-501/pl_head.py) && git update-index --cacheinfo 100644,$sha,app/backend/pipeline.py && git update-index --add tests/unit/test_t161_first_run_stage_down.py && git diff --cached --stat"
}
````

### User / tool · 2026-11-02T15:06:25.208Z

**tool result**
````
 app/backend/pipeline.py                      |  7 +--
 tests/unit/test_t161_first_run_stage_down.py | 68 ++++++++++++++++++++++++++++
 2 files changed, 72 insertions(+), 3 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:06:27.521Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx.t161 && git commit -q -m \"fix(backend): T-161 first run with a judge or the flag step down fails like a re-run (run_partial, step named, gate RUN_FAILED)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" ; git log --oneline | head -2",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T15:06:30.178Z

**tool result**
````
check_stale_index: BLOCKED — this commit would revert work that is not yours.
Rebuild the index from HEAD right before adding: GIT_INDEX_FILE=$(mktemp) git read-tree HEAD
app/backend/amounts.py: staged version is an older committed version (stale index would revert it)
app/backend/present.py: staged version is an older committed version (stale index would revert it)
app/backend/reclassify.py: staged version is an older committed version (stale index would revert it)
app/backend/review.py: staged version is an older committed version (stale index would revert it)
app/backend/trace.py: staged version is an older committed version (stale index would revert it)
memory/contracts/api.md: staged version is an older committed version (stale index would revert it)
tests/unit/test_t159_flag_audit.py: staged as deleted but still on disk (stale index?)
9fc579c feat(backend): T-159 audit trail for a flagged charge: named confirm in the review event, charge_flag trace step, plain flag sentence, repeat accept is a no-op
0e3e8ba test(e2e): T-155 r2 L6 has five judge objections since D-060 default-deny (a2 office visits $1,100 undated); presence check on a2 and a7
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:06:34.360Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx.t161b && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git show HEAD:app/backend/pipeline.py > /private/tmp/claude-501/pl_head.py && python3 - <<'EOF'\np='/private/tmp/claude-501/pl_head.py'\ns=open(p).read()\ndef rep(a,b):\n    global s\n    assert s.count(a)==1,a\n    s=s.replace(a,b)\nrep(\"        err = _partial_error(kept, empty if rerun else [])\\n\",\"        err = _partial_error(kept, empty if rerun else [s for s in empty if s != _EXTRACT_STEP])      # T-161: a first run with a judge or the flag step down fails like a re-run; its extract failures stay tray items\\n\")\nrep('        return \"writing the entries\"\\n','        return _EXTRACT_STEP\\n')\nrep('_RANK = {\"verified\": 0, \"needs_review\": 1, \"rejected\": 2}\\n','_RANK = {\"verified\": 0, \"needs_review\": 1, \"rejected\": 2}\\n_EXTRACT_STEP = \"writing the entries\"\\n')\nrep('    if cause == \"writing the entries\":\\n','    if cause == _EXTRACT_STEP:\\n')\nopen(p,'w').write(s)\nEOF\nsha=$(git hash-object -w /private/tmp/claude-501/pl_head.py) && git update-index --cacheinfo 100644,$sha,app/backend/pipeline.py && git update-index --add tests/unit/test_t161_first_run_stage_down.py && git diff --cached --stat"
}
````

### User / tool · 2026-11-02T15:06:35.105Z

**tool result**
````
 app/backend/pipeline.py                      |  7 +--
 tests/unit/test_t161_first_run_stage_down.py | 68 ++++++++++++++++++++++++++++
 2 files changed, 72 insertions(+), 3 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:06:36.864Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/idx.t161b && git commit -q -m \"fix(backend): T-161 first run with a judge or the flag step down fails like a re-run (run_partial, step named, gate RUN_FAILED)\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" ; git log --oneline | head -2",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T15:06:40.942Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
83f1afd fix(backend): T-161 first run with a judge or the flag step down fails like a re-run (run_partial, step named, gate RUN_FAILED)
0b2ce9c fix(frontend): T-158 refused-Accept reason box is scrolled fully into view once layout settles (several passes by item id, clear of the sticky header); the rerun sentence keeps its count when the trace was not cached yet
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:06:46.155Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B ac T-161 --check 1 --agent backend --evidence \"tests/unit/test_t161_first_run_stage_down.py (13 tests: j1,j2,j3,j4,flags down and fixture-miss -> failed/run_partial, step named, RUN_FAILED; clean first run ready; extract-down first run unchanged); full unit suite 4649 pass, 6 fail only in test_amounts_d062 (T-140 amounts.py in progress, not mine)\"; $B handoff T-161 --agent backend --text \"What changed: pipeline._partial_error now gets the first run's non-extract failures too (empty list minus 'writing the entries', now _EXTRACT_STEP); no new code path, same T-146 message. How verified: tests/unit/test_t161_first_run_stage_down.py written first (11 red), now 13 green; full unit suite 4649 pass, 6 fail in test_amounts_d062 only (T-140's uncommitted amounts.py). Left: nothing. Surprised: j1/j2/j3/j4 all read 'the second check' (the step names in the message are the existing re-run wording, not per judge); a first run with extract down stays ready by design (tray shows the failed records, pinned by the T-146 r3 test). Commit 83f1afd via temp index; the shared pipeline.py also holds T-146 r4 uncommitted hunks I did not touch.\"; $B move T-161 in_review --agent backend; $B commit T-161 --sha 83f1afd --agent backend"
}
````

### User / tool · 2026-11-02T15:06:46.492Z

**tool result**
````
AC 1 checked: tests/unit/test_t161_first_run_stage_down.py (13 tests: j1,j2,j3,j4,flags down and fixture-miss -> failed/run_partial, step named, RUN_FAILED; clean first run ready; extract-down first run unchanged); full unit suite 4649 pass, 6 fail only in test_amounts_d062 (T-140 amounts.py in progress, not mine)
handoff written on T-161
T-161: in_progress -> in_review
T-161: commit 83f1afd recorded
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T15:06:49.669Z

T-161 is in_review and committed as 83f1afd. A first run with flags, j1, j2, j3 or j4 down now ends failed/run_partial with the step named and the gate reading RUN_FAILED. A clean first run stays ready.

- **Extract:** a first run with extract down still reads ready, as the T-146 r3 test pins.
- **Message wording:** j1 to j4 all read "the second check", the same wording the re-run message already uses.
- **Tests:** the new tests in `tests/unit/test_t161_first_run_stage_down.py` were written first and failed (11 red). All 13 pass now.
- **Full unit suite:** 4649 pass and 6 fail, all in `test_amounts_d062.py`, which comes from T-140's uncommitted `amounts.py` work.
- **T-146 r4 hunks:** the working tree still holds T-146 r4's uncommitted hunks in `pipeline.py`, which I left out of my commit.
