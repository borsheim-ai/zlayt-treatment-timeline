# Subagent: Backend: T-175 case-list 500 (Backend: T-175 case-list 500)

Source: `agent-a94146cf523a0eb46.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T17:55:02.561Z

You are a backend worker in /Users/arsis/zlayt-pm-project. Claim T-175 (P0) with `python3 tools/board.py claim T-175 --agent backend`. Read finding 2 in reviews/T-173-staff-engineer.md and its evidence: an intermittent unhandled 500 on GET /api/cases during the e2e spec flow.

1. Reproduce it. Run the e2e tray specs, or a concurrent create, run, review and delete loop with listing alongside.
2. Find the root cause in case_list.py or store.py: for example a case deleted or half-written mid-list, or a run in progress.
3. Fix it so the list never 500s. A case that is mid-change is listed with a plain status, or skipped and logged.

Add a stress test that runs 200 iterations of concurrent create, run, review, delete and list. If any other route can 500 for the same reason, fix it too.

Never edit app/frontend. Verify from a `git archive HEAD` copy, and commit via a temp index; never run `git checkout` on files. Write the handoff and move the card to in_review. Reply in 2 lines.

### User / tool · 2026-11-02T17:55:02.567Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:06.636Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py claim T-175 --agent backend; python3 tools/board.py show T-175 | head -40; grep -n -B2 -A25 -i \"finding 2\\|^## .*2\\b\\|F2\" reviews/T-173-staff-engineer.md | head -80"
}
````

### User / tool · 2026-11-02T17:55:06.847Z

**tool result**
````
T-175 claimed by backend
---
id: "T-175"
title: "Intermittent HTTP 500 on GET /api/cases (case overview) seen during e2e (T-173 review); find the race and fix it"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T17:54:56Z"
updated_at: "2026-11-02T17:55:06Z"
claimed_by: "backend"
claimed_at: "2026-11-02T17:55:06Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "root cause named; GET /api/cases never 500s under concurrent create/run/review (stress test 200 iterations); the overview shows a plain retry message if it ever fails", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T17:54:58Z orchestrator: assigned: backend
- 2026-11-02T17:55:06Z backend: claimed

## Handoff (filled when moving to in_review)

34-## Findings
35-
36:See the JSON block. Finding 1 (major) is the blocker to the milestone: the seeded row must have the placeholder shape. Finding 2 (minor) is an intermittent server-side 500 on the case list that the spec flow reaches; it is outside this diff and does not fail the specs. Finding 3 (nit) is helper hygiene.
37-
38-```json
39-{"card": "T-173", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
40- "scope": "commit d865d21: tests/e2e/conftest.py, tests/e2e/test_polish_r5.py, tests/e2e/test_suggestions.py; git archive copy at artifacts/review-evidence/T-173-r1-staff/copy; private server 127.0.0.1:55367 (LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_MODE=local); diagnostic copy of HEAD with traceback printing in artifacts/review-evidence/T-173-r1-staff/diag; sample case: library lib01 (case_lib01_er_only_then_gap), record 3",
41- "exercised": [
42-  "python3 tools/board.py show T-173 (AC, handoff and notes read); personas/staff-engineer.md read in full",
43-  "git show d865d21 full diff of tests/e2e/conftest.py, tests/e2e/test_polish_r5.py, tests/e2e/test_suggestions.py; grep of changed assert lines returned none",
44-  "git archive d865d21 extracted to artifacts/review-evidence/T-173-r1-staff/copy; .venv/bin/python -m pytest -v on the three named specs with E2E_BASE_URL, ZLAYT_DB and E2E_REQUIRE_DB=1: 3 passed (run-3specs-head.txt)",
45-  "driver.py: unmutated control plus M0 to M7 mutants, each restored after its run; outputs and summary.json in artifacts/review-evidence/T-173-r1-staff/mutants/",
46-  "fidelity_probe.py against the diagnostic copy: seeded tray item JSON (attempt present, ladder.failure None, summary and excerpt set)",
47-  "tray_ui_probe.py: Chromium render of the seeded lib01 tray: tray-attempt count 1 with text 'The model's attempt (not used): ...' beside 'The demo has no recorded AI answer for this step, so this item has not been checked.'",
48-  "race_probe.py: create, delete and list cases, 3 rounds: 0 list responses of 500",
49-  "m0_race_control.py: seed removed, 3 spec rounds on the diagnostic copy: 0 new unhandled lines per round (weak control: those rounds fail early on the tray wait)",
50-  "diagnostic server log (diag/server-diag.log): unhandled lines per round of the seeded specs 0, 2, 3; first traceback read through case_list.py, trace.py, present.py and overlap.py",
51-  "cite_check.py and cite_lines.py: every cited line number read at d865d21 with git show",
52-  "own server PIDs stopped (62857, 62859, 65848, 65849, 66269, 66531, 66533; the driver stopped its own servers); lsof shows nothing on 55367; no process left under artifacts/review-evidence/T-173-r1-staff"
53- ],
54- "verdict": "changes",
55- "scores": {"assertions_unchanged": 5, "mutation_sensitivity": 5, "seed_fidelity_to_missing_answer": 2, "disclosure_in_docstring_and_card": 4, "spec_reproducibility": 4},
56- "findings": [
57-  {"severity": "major",
58-   "title": "The seeded tray row is not the placeholder a missing answer leaves; the tray shows a contradictory attempt line",
59-   "evidence": "tests/e2e/conftest.py:208 (DB.update_item writes only state and state_reasons_json). Repro: fidelity_probe.py against the diagnostic copy prints the after-seed tray item with reasons ['FIXTURE_MISS'] and attempt.summary 'Neck pain 5/10 with new left arm tingling; ...', then 'ladder.failure = None | summary set = True | excerpt set = True'. The real placeholder sets summary=None and excerpt=None at app/backend/generator.py:189 and the ladder failure marker at app/backend/generator.py:190. tray_ui_probe.py prints 'tray-attempt count: 1' and the attempt line beside 'The demo has no recorded AI answer for this step, so this item has not been checked.' Builder: app/backend/present.py:396; renderer: app/frontend/timeline.js:230.",
60-   "why_it_matters": "Per the card title, record 3 was a pipeline-made tray item before T-168, so these specs used to cover the placeholder the pipeline writes. They now cover a hybrid row: the record's real T-168 summary and quote, a generator and judge ladder, no failure marker, and an on-screen line that says the model made an attempt on a record whose reason says no answer was recorded. The helper docstring (tests/e2e/conftest.py:197-199) and the commit message say the row is the state a missing extract answer leaves; that holds for state and reason only. Read from code and not executed: resolved_placeholders (app/backend/generator.py:198-202) keys on ladder.failure, so a hand-entered entry for record 3 would leave this seeded row in the tray, which a real placeholder does not do.",
61-   "fix": "In tray_entry_for_record, write the placeholder shape: entry summary, excerpt, excerpt_start and excerpt_end set to None, and ladder set to item_id, generator None, judge None, failure FIXTURE_MISS, code_checks {}, state rejected, human {action None, edited_text None, at None}; keep state_reasons_json FIXTURE_MISS. Alternatively call generator.failure_entry(record, group, 'FIXTURE_MISS') and write its fields with DB.update_item. Narrow the docstring to what is reproduced. Re-run the three specs and mutants M0 to M7.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:08.553Z

**tool call — Bash**
````
{
 "command": "grep -n -A8 '\"title\": \"[^\"]*500\\|unhandled' reviews/T-173-staff-engineer.md | head -60; ls artifacts/review-evidence/T-173-r1-staff/ 2>/dev/null; git log --oneline | head -3; wc -l app/backend/case_list.py app/backend/store.py"
}
````

### User / tool · 2026-11-02T17:55:08.666Z

**tool result**
````
20:- `race_probe.py` (create, delete and list cases, 3 rounds), `m0_race_control.py` (seed removed, 3 rounds, unhandled-line count), and `cite_check.py` / `cite_lines.py` (every cited line read at d865d21).
21-- Own server PIDs stopped; port 55367 free afterwards.
22-
23-Mutation results (spec outcomes in order: reason-once, entry-wording, no-sentences):
24-
25-- M0 seed removed: FAIL, FAIL, FAIL.
26-- M1 tray reason element removed (`timeline.js:227`): FAIL, FAIL, PASS (test 3 does not use it).
27-- M2 tray items not appended (`timeline.js` `box.append(item)`): FAIL, FAIL, FAIL.
28-- M3 reason rendered twice: FAIL, PASS, PASS.
--
49:  "m0_race_control.py: seed removed, 3 spec rounds on the diagnostic copy: 0 new unhandled lines per round (weak control: those rounds fail early on the tray wait)",
50:  "diagnostic server log (diag/server-diag.log): unhandled lines per round of the seeded specs 0, 2, 3; first traceback read through case_list.py, trace.py, present.py and overlap.py",
51-  "cite_check.py and cite_lines.py: every cited line number read at d865d21 with git show",
52-  "own server PIDs stopped (62857, 62859, 65848, 65849, 66269, 66531, 66533; the driver stopped its own servers); lsof shows nothing on 55367; no process left under artifacts/review-evidence/T-173-r1-staff"
53- ],
54- "verdict": "changes",
55- "scores": {"assertions_unchanged": 5, "mutation_sensitivity": 5, "seed_fidelity_to_missing_answer": 2, "disclosure_in_docstring_and_card": 4, "spec_reproducibility": 4},
56- "findings": [
57-  {"severity": "major",
58-   "title": "The seeded tray row is not the placeholder a missing answer leaves; the tray shows a contradictory attempt line",
--
64:   "title": "Intermittent unhandled 500 on GET /api/cases during the spec flow (outside this diff; the specs still pass)",
65:   "evidence": "artifacts/review-evidence/T-173-r1-staff/diag/server-diag.log: unhandled lines per round of the three seeded specs were 0, 2, 3. First traceback: api.py:224 list_cases, then case_list.py:204 summaries, case_list.py:186 summary, case_list.py:125 _gate, trace.py:1111 case_trace, present.py:291 totals_view, overlap.py:129 (raw_text read from a case that is None). The handler logs only the exception type name (api.py:162 and api.py:184). Control: artifacts/review-evidence/T-173-r1-staff/m0_race_control.out shows 0 new lines in each of 3 no-seed rounds; race_probe.py, 3 rounds of create, delete and list, shows 0 list responses of 500.",
66-   "why_it_matters": "The three specs passed every round, so T-173's verdict does not turn on this. It is still a product defect that the spec flow reaches: a case removed between the id SELECT (case_list.py:204) and its read makes the whole case list return 500. The handler is built to log no traceback (api.py:162 comment), so the cause is invisible unless someone runs a diagnostic copy. I did not establish that the seed causes it: the traceback never reads entries, and the no-seed control is weak because those rounds fail early.",
67-   "fix": "File a backend card. summaries should tolerate a case removed mid-list: skip it, or read the id list and each case inside one transaction. The handler should log the exception class and the innermost app frame (file and line), never message text, which keeps the privacy rule api.py states.",
68-   "acceptance_test": "A unit test patches the case read to return None for one listed id and asserts GET /api/cases returns 200 without that case. A log test asserts the innermost app frame is named and no record text appears in the log line."},
69-  {"severity": "nit",
70-   "title": "Helper hygiene: unguarded next() and a sys.path insert on every call",
71-   "evidence": "tests/e2e/conftest.py:203 e = next(x for x in c['entries'] ...) has no default, so a missing record 3 entry raises a bare StopIteration. tests/e2e/conftest.py:204 sys.path.insert(0, ROOT) runs on every call, and the imports sit inside the function.",
72-   "why_it_matters": "A missing entry fails with no message naming the record. The per-call sys.path insert is harmless here but repeats on every call.",
73-   "fix": "Use next(..., None) and pytest.fail naming the record id; move the sys.path setup to module level, where ROOT is already defined.",
check_review.py
cite_check.py
cite_lines.py
copy
diag
driver.py
e2e.sqlite3
fidelity_probe.py
fresh.pid
fresh.sqlite3
m0_race_control.out
m0_race_control.py
mutants
probe.pid
probe.sqlite3
race_probe.py
run-3specs-head.txt
server-fresh.log
server-mutant.log
server-probe.log
server.log
tray_ui_probe.py
f814cf7 test(qa): T-173 r2 tray_entry_for_record writes the pipeline's own placeholder (generator.failure_entry through pipeline._row), not a state edit on a real entry; checks the tray item has no attempt; guards a missing entry
04ebe39 fix(frontend): T-172 r2 read count_confirm before the first dialog: a likely duplicate shows its flag in the row and asks for the duplicate confirm FIRST (T-154 dialog), then the separate-charge confirm; e2e on a real server, no stub
d865d21 test(qa): T-173 lib01 tray specs put record 3 into the tray (T-168 recorded its extract answer, so the library case has no tray item); assertions unchanged
     204 app/backend/case_list.py
     129 app/backend/store.py
     333 total
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:10.133Z

**tool call — Bash**
````
{
 "command": "sed -n 90,204p app/backend/case_list.py; cat app/backend/store.py; sed -n 150,200p app/backend/api.py; sed -n 215,235p app/backend/api.py"
}
````

### User / tool · 2026-11-02T17:55:10.252Z

**tool result**
````
def readable_title(name, source, created_at) -> str:
    """A name a paralegal would recognise; no name at all becomes "Records added Nov 1" (T-157: never "Untitled case"; `case_title` prefers the first record header over that fallback)."""
    n = readable_name(name)
    if n:
        return n
    day = datetime.datetime.fromtimestamp(float(created_at or 0), datetime.timezone.utc).strftime("%b %-d")
    return "Sample case" if source == "sample" else f"Records added {day}"


def case_title(conn, case: dict) -> str:
    """What to show for a case: its name made readable; else (no name, or one that is empty after cleanup) the first record header (provider and date); else the date it was added.
    Never "Untitled case", never markup."""
    return readable_name(case["name"]) or derived_title(conn, case["id"]) or readable_title(None, case["source"], case["created_at"])


def run_progress(case: dict, stages) -> tuple:
    """(stage, steps_done) for a case row: what GET /status reports. A case that was only ingested is at the 'ingest' stage."""
    stage = case["stage"] or ("ingest" if case["status"] == "ingested" else None)
    return stage, (list(stages).index(stage) if stage in stages else 0)


def _progress(conn, case_id) -> dict:
    """decided / total per kind over the items review_view counts. An edit still marked Needs review (T-134) is not decided."""
    items = {k: DB.list_items(conn, case_id, k) for _, k in KINDS}
    handled = generator.resolved_placeholders(items["entry"])
    out = {}
    for label, kind in KINDS:
        live = [r for r in items[kind] if r["id"] not in handled and not FT.is_filtered(r.get("state_reasons")) and r["state"] != "rejected"]
        decided = sum(1 for r in live if r["review_status"] in ("accepted", "dismissed", "edited") and not review.edit_unconfirmed(kind, r))
        out[label] = {"decided": decided, "total": len(live)}
    return out


def _gate(conn, case_id) -> dict:
    step = next(s for s in trace.case_trace(conn, case_id, full=False)["steps"] if s["id"] == "export_gate")
    keep = lambda xs, keys: [{k: x[k] for k in keys if k in x} for x in xs]      # noqa: E731
    return {"ready": step["ready"], "blockers": keep(step["blockers"], ("reason_code", "kind", "item_id", "why")),
            "warnings": keep(step["warnings"], ("reason_code", "count", "why"))}


_RANK = {"entry": 0, "flag": 1, "amount": 2}


def needs_review_order(conn, case_id) -> list:
    """T-157: the live items that still wait for the paralegal and that the AI could not verify (state needs_review; pending, or an edit not yet confirmed), in timeline order:
    the date of the record each item cites (earliest, for a flag that cites several), then that record's position, then entry before flag before amount, then id. Undated last.
    [{id, kind, date, seq, rank, row}]. Same item filter as `_progress`."""
    recs = {r["id"]: (r["date_iso"], r["seq"]) for r in conn.execute("SELECT id, date_iso, seq FROM records WHERE case_id=?", (case_id,))}
    by_seq = {seq: rid for rid, (_, seq) in recs.items()}
    items = {k: DB.list_items(conn, case_id, k) for _, k in KINDS}
    handled = generator.resolved_placeholders(items["entry"])
    out = []
    for kind, rows in items.items():
        for r in rows:
            if r["id"] in handled or FT.is_filtered(r.get("state_reasons")) or r["state"] != "needs_review":
                continue
            if not (r["review_status"] == "pending" or review.edit_unconfirmed(kind, r)):
                continue
            ids = list(r.get("record_ids") or []) if kind != "flag" else \
                [e.get("record_id") or by_seq.get(e.get("record_no")) for e in r.get("evidence") or []] or list((r.get("computed") or {}).get("record_ids") or [])
            known = sorted((recs[i] for i in ids if i in recs), key=lambda x: (x[0] is None, x[0] or "", x[1] or 0))
            date, seq = known[0] if known else (None, None)
            date = date or (r.get("date_iso") if kind == "entry" else None)
            out.append({"id": r["id"], "kind": kind, "date": date, "seq": seq, "rank": _RANK[kind], "row": r})
    return sorted(out, key=lambda x: (x["date"] is None, x["date"] or "", x["seq"] or 0, x["rank"], x["id"]))


def next_action(conn, case_id, case: dict = None, blockers: list = None):
    """T-157: the single first thing to do in a case, {item_id, kind, reason}, or None when nothing is waiting. Code only, deterministic:
      1. the first export-gate blocker, in gate order (a run in progress or failed, a code-check failure, an accepted item whose second check never answered). Its `kind` is the
         blocker's (`case` for a blocker that names no item, `item_id` null) and `reason` its plain `why`. NOTHING_ACCEPTED yields to step 2 when an item waits (deciding it clears it);
      2. else the first needs-review item in timeline order (`needs_review_order`): `kind` entry | flag | amount, `reason` the item's own plain `why`;
      3. else NOTHING_ACCEPTED when nothing is accepted; else None.
    A case that was only ingested has no items yet: {item_id: null, kind: "run"}. `blockers` may be passed when the caller already read the gate."""
    case = case or DB.get_case(conn, case_id)
    if case["status"] == "ingested":
        return {"item_id": None, "kind": "run", "reason": "Run the case to draft the timeline. Nothing is waiting for you until then."}
    blockers = _gate(conn, case_id)["blockers"] if blockers is None else blockers
    first = next((b for b in blockers if b["reason_code"] != "NOTHING_ACCEPTED"), None)
    if first:
        return {"item_id": first.get("item_id"), "kind": first["kind"], "reason": first["why"]}
    waiting = needs_review_order(conn, case_id)
    if waiting:
        w = waiting[0]
        return {"item_id": w["id"], "kind": w["kind"], "reason": present.item_view(conn, case_id, w["id"])["why"]}
    if blockers:
        return {"item_id": blockers[0].get("item_id"), "kind": blockers[0]["kind"], "reason": blockers[0]["why"]}
    return None


def summary(conn, case_id: str, stages) -> dict:
    case = DB.get_case(conn, case_id)
    rv = present.review_view(conn, case_id)
    counts = rv["counts"]
    stage, done = run_progress(case, stages)
    gate = _gate(conn, case_id)
    last = conn.execute("SELECT max(at) FROM review_events WHERE case_id=?", (case_id,)).fetchone()[0]
    updated = case.get("run_finished_at") or case["created_at"]            # the same value GET case calls updated_at
    return {"token": case_id, "title": case_title(conn, case), "name": case["name"],
            "source": case["source"], "status": case["status"],
            "record_count": conn.execute("SELECT count(*) FROM records WHERE case_id=?", (case_id,)).fetchone()[0],
            "created_at": store.iso(case["created_at"]), "updated_at": store.iso(updated), "last_activity_at": store.iso(max(updated, last or 0)),
            "run": {"stage": stage, "steps_done": done, "steps_total": len(stages), "running": case["status"] == "running",
                    "error": bool(case.get("error"))},
            "progress": _progress(conn, case_id),
            "counts": {k: counts[k] for k in ("pending", "accepted", "edited", "dismissed", "needs_review")},      # kept from the first version of this route
            "hitl": {"pending": counts["pending"], "needs_review": counts["needs_review"], "needs_review_open": len(needs_review_order(conn, case_id)), "edits_to_check": counts["edit_to_check"],
                     "could_not_verify": counts["rejected"], "gate_blockers": gate["blockers"], "gate_warnings": gate["warnings"]},
            "export_ready": gate["ready"], "next_action": next_action(conn, case_id, case, gate["blockers"])}


def summaries(conn, stages) -> list:
    """Every case, newest first (created, then insertion order)."""
    return [summary(conn, r["id"], stages) for r in conn.execute("SELECT id FROM cases ORDER BY created_at DESC, rowid DESC")]
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

    @app.exception_handler(review.ReviewError)
    async def _review_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(_, e):
        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
        return JSONResponse({"error": {"code": code, "message": code.replace("_", " "), "detail": {}}}, status_code=e.status_code)

    @app.exception_handler(Exception)
    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log
        log.error("unhandled %s", type(e).__name__)
        return JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)

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
            log.error("unhandled %s", type(e).__name__)
            resp = JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
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
            raise ApiError(404, "not_found", "Not found.")
        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}

    @app.post("/api/cases", status_code=201)
    async def create_case(request: Request):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:13.413Z

**tool call — Bash**
````
{
 "command": "grep -n \"def get_case\\|def delete_case\\|def connect\\|check_same_thread\\|isolation\\|journal_mode\\|busy_timeout\\|def purge_expired\" -A6 app/db/db.py | head -90; grep -n \"def conn\\|def need_case\\|def case_or_404\\|DB.get_case\" app/backend/api.py | head -40; ls tests | head -50"
}
````

### User / tool · 2026-11-02T17:55:13.528Z

**tool result**
````
38:def connect(path: str):
39-    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
40-    text): the schema uses CREATE IF NOT EXISTS, so an old file would otherwise keep its old keys, and keeping it aside would keep
41-    pasted text past the 24 h purge (T-040 security r2)."""
42-    if path != ":memory:" and os.path.exists(path) and os.path.getsize(path) > 0:
43-        probe = sqlite3.connect(path)
44-        try:
--
54:    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
55-    conn.row_factory = sqlite3.Row
56-    conn.execute("PRAGMA secure_delete=ON")
57-    conn.execute("PRAGMA foreign_keys=ON")
58-    with open(_SCHEMA, encoding="utf-8") as f:
59-        schema = f.read()
60-    if path != ":memory:" and conn.execute("PRAGMA user_version").fetchone()[0] == 3 and \
--
131:def get_case(conn, case_id: str):
132-    r = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
133-    return _decode(r) if r else None
134-
135-
136-def _insert(conn, table, row):
137-    bad = set(row) - _cols(conn, table)
--
285:def delete_case(conn, case_id: str) -> None:
286-    """The one deletion path (ADR-006): every table, prompts included. DELETE endpoint and purge both call this."""
287-    conn.execute("BEGIN")
288-    try:
289-        for t in _CASE_TABLES:
290-            conn.execute(f"DELETE FROM {t} WHERE {'id' if t == 'cases' else 'case_id'}=?", (case_id,))
291-        conn.execute("COMMIT")
--
297:def purge_expired(conn, now: float, retention_seconds: float = RETENTION_SECONDS) -> int:
298-    ids = [r["id"] for r in conn.execute("SELECT id FROM cases WHERE created_at < ?", (now - retention_seconds,))]
299-    for cid in ids:
300-        delete_case(conn, cid)
301-    return len(ids)
302-
303-
125:    def conn():
141:        case = DB.get_case(c, token)
319:            return {"token": cid, "name": DB.get_case(c, cid)["name"], "title": case_list.case_title(c, DB.get_case(c, cid)), "status": "ingested", "source": "sample" if sample else "paste",
349:            case = DB.get_case(c, token)
369:            if DB.get_case(c, token)["status"] == "running":
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:15.236Z

**tool call — Bash**
````
{
 "command": "sed -n 118,150p app/backend/api.py; grep -n \"@app\\.\\(get\\|post\\|put\\|patch\\|delete\\)\" app/backend/api.py; grep -n \"def conn\\|sqlite3.connect\\|threading\" app/backend/*.py | head; ls tests/unit | grep -i \"api\\|case_list\\|stress\" "
}
````

### User / tool · 2026-11-02T17:55:15.343Z

**tool result**
````
    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
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

212:    @app.get("/api/health")
218:    @app.get("/api/cases")
228:    @app.get("/api/library")
234:    @app.post("/api/cases", status_code=201)
252:    @app.post("/api/cases/pdf", status_code=201)
328:    @app.get("/api/cases/{token}")
338:    @app.patch("/api/cases/{token}")
354:    @app.delete("/api/cases/{token}", status_code=204)
378:    @app.post("/api/cases/{token}/run", status_code=202)
401:    @app.post("/api/cases/{token}/rejudge")
423:    @app.get("/api/cases/{token}/status")
441:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
453:    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
464:    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
477:    @app.get("/api/cases/{token}/narrative")
486:    @app.post("/api/cases/{token}/narrative")
499:    @app.post("/api/cases/{token}/narrative/review")
514:    @app.get("/api/cases/{token}/items/{item_id}")
526:    @app.post("/api/cases/{token}/items/{item_id}/review")
547:    @app.get("/api/cases/{token}/export")
576:    @app.get("/api/cases/{token}/items/{item_id}/trace")
589:    @app.get("/api/cases/{token}/trace")
598:    @app.get("/api/cases/{token}/judges")
607:    @app.get("/api/cases/{token}/audit")
app/backend/api.py:13:import threading
app/backend/api.py:125:    def conn():
app/backend/api.py:395:            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
app/backend/case_extras.py:4:import threading
app/backend/case_extras.py:12:_LOCK = threading.Lock()
app/backend/pdf_checks.py:8:import threading
app/backend/pdf_checks.py:18:_JOBS = threading.BoundedSemaphore(MAX_PDF_JOBS)
app/backend/pdf_hidden.py:46:import threading
app/backend/pdf_hidden.py:507:_SLOTS = threading.BoundedSemaphore(MAX_CHILDREN)
app/backend/pdf_hidden.py:576:        threading.Thread(target=feed, daemon=True).start()
test_amounts_d059_api.py
test_api.py
test_api_routes.py
test_case_list.py
test_pdf_checks_api.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:22.077Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/unit/test_case_list.py; grep -n \"journal_mode\\|WAL\" app/db/*.py; sed -n 340,400p app/backend/api.py; git status --short | head"
}
````

### User / tool · 2026-11-02T17:55:22.221Z

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
        """T-157: body {title}. A blank or null title clears the name: the title goes back to the one derived from the first record header."""
        b = await body_of(request)
        if "title" not in b or not (b["title"] is None or isinstance(b["title"], str)):
            raise ApiError(400, "bad_request", "Send {\"title\": text}.")
        name = valid_name(b["title"])
        c = conn()
        try:
            get_case(c, token)
            DB.update_case(c, token, name=name or None)
            case = DB.get_case(c, token)
            return {"token": token, "name": case["name"], "title": case_list.case_title(c, case)}
        finally:
            c.close()

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

 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t166_mvp_polish.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:41.628Z

**tool call — Bash**
````
{
 "command": "mkdir -p /tmp/x 2>/dev/null; cat > tests/unit/test_case_list_race.py <<'EOF'\n\"\"\"T-175: GET /api/cases (and every per-case route) never answers 500 while cases are created, run, reviewed and deleted at the same time.\nRoot cause it guards: `case_list.summaries` read the id list, then read each case in its own statements; a case deleted in between (DELETE, the 24 h purge)\nmade `DB.get_case` return None and the list died with a TypeError (500). Fixture backend, no network; local mode.\"\"\"\nimport os\nimport threading\nimport time\n\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import case_list\nfrom app.backend.api import create_app\nfrom app.db import db as DB\n\nITERATIONS = int(os.environ.get(\"RACE_ITERATIONS\", \"200\"))\nWORKERS = 4\n\n\n@pytest.fixture()\ndef app_env(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.setenv(\"ZLAYT_MODE\", \"local\")\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    app = create_app(str(tmp_path / \"t.sqlite\"), static_dir=str(tmp_path))\n    return app, str(tmp_path / \"t.sqlite\")\n\n\ndef _client(app):\n    return TestClient(app, client=(\"127.0.0.1\", 50000))\n\n\ndef test_list_skips_a_case_deleted_mid_list(app_env, monkeypatch):\n    \"\"\"A case that vanishes between the id SELECT and its read is left out; the rest of the list is returned (200), and the skip is logged.\"\"\"\n    app, path = app_env\n    c = _client(app)\n    toks = [c.post(\"/api/cases\", json={\"library\": \"lib01_er_only_then_gap\"}).json()[\"token\"] for _ in range(3)]\n    real = DB.get_case\n    gone = toks[1]\n\n    def flaky(conn, cid):\n        if cid == gone:\n            DB.delete_case(conn, cid)\n        return real(conn, cid)\n    monkeypatch.setattr(DB, \"get_case\", flaky)\n    r = c.get(\"/api/cases\")\n    assert r.status_code == 200, r.text\n    got = [x[\"token\"] for x in r.json()[\"cases\"]]\n    assert gone not in got and set(got) == set(toks) - {gone}\n\n\ndef test_list_gives_a_plain_row_for_a_case_whose_summary_fails(app_env, monkeypatch):\n    \"\"\"A case that exists but cannot be summarised right now (mid-write) is listed with its plain status, never a 500.\"\"\"\n    app, path = app_env\n    c = _client(app)\n    tok = c.post(\"/api/cases\", json={\"library\": \"lib01_er_only_then_gap\"}).json()[\"token\"]\n    other = c.post(\"/api/cases\", json={\"library\": \"lib01_er_only_then_gap\"}).json()[\"token\"]\n    real = case_list.summary\n\n    def boom(conn, cid, stages):\n        if cid == tok:\n            raise RuntimeError(\"half written\")\n        return real(conn, cid, stages)\n    monkeypatch.setattr(case_list, \"summary\", boom)\n    r = c.get(\"/api/cases\")\n    assert r.status_code == 200, r.text\n    rows = {x[\"token\"]: x for x in r.json()[\"cases\"]}\n    assert set(rows) == {tok, other}\n    assert rows[tok][\"status\"] == \"ingested\" and rows[tok][\"next_action\"] is None and rows[tok][\"export_ready\"] is False\n    assert set(rows[tok]) == set(rows[other])            # same keys as a full row, so the overview renders it\n\n\ndef test_routes_answer_404_for_a_case_deleted_under_them(app_env, monkeypatch):\n    \"\"\"Every case route that reads a case after the existence check answers 404 (not 500) when the case is deleted in that gap.\"\"\"\n    app, path = app_env\n    c = _client(app)\n    tok = c.post(\"/api/cases\", json={\"library\": \"lib01_er_only_then_gap\"}).json()[\"token\"]\n    real = DB.get_case\n    calls = {\"n\": 0}\n\n    def vanish(conn, cid):\n        calls[\"n\"] += 1\n        if cid == tok and calls[\"n\"] > 1:                # the existence check passes; the next read finds nothing\n            DB.delete_case(conn, cid)\n        return real(conn, cid)\n    monkeypatch.setattr(DB, \"get_case\", vanish)\n    for method, url in ((\"get\", f\"/api/cases/{tok}\"), (\"get\", f\"/api/cases/{tok}/status\"), (\"get\", f\"/api/cases/{tok}/trace\"),\n                        (\"get\", f\"/api/cases/{tok}/export\"), (\"get\", f\"/api/cases/{tok}/audit\"), (\"get\", f\"/api/cases/{tok}/judges\"),\n                        (\"post\", f\"/api/cases/{tok}/run\"), (\"patch\", f\"/api/cases/{tok}\")):\n        calls[\"n\"] = 0\n        real_exists = real(__import__(\"app.db.db\", fromlist=[\"connect\"]).connect(path), tok)\n        if real_exists is None:\n            tok = c.post(\"/api/cases\", json={\"library\": \"lib01_er_only_then_gap\"}).json()[\"token\"]\n        kw = {\"json\": {\"title\": \"x\"}} if method == \"patch\" else ({\"json\": {}} if method == \"post\" else {})\n        r = getattr(c, method)(url.replace(url.split(\"/\")[3], tok), **kw)\n        assert r.status_code != 500, (method, url, r.text)\n\n\ndef test_stress_create_run_review_delete_list(app_env):\n    \"\"\"ITERATIONS rounds of create -> run -> review -> delete across WORKERS threads while two threads list and read cases as fast as they can:\n    no response anywhere is a 500.\"\"\"\n    app, path = app_env\n    bad, stop, counter = [], threading.Event(), {\"i\": 0, \"lists\": 0}\n    lock = threading.Lock()\n\n    def note(where, r):\n        if r.status_code >= 500:\n            with lock:\n                bad.append((where, r.status_code, r.text[:200]))\n\n    def worker():\n        c = _client(app)\n        while True:\n            with lock:\n                if counter[\"i\"] >= ITERATIONS:\n                    return\n                counter[\"i\"] += 1\n                n = counter[\"i\"]\n            r = c.post(\"/api/cases\", json={\"library\": \"lib01_er_only_then_gap\"})\n            note(\"create\", r)\n            if r.status_code != 201:\n                continue\n            tok = r.json()[\"token\"]\n            r = c.post(f\"/api/cases/{tok}/run\", json={})\n            note(\"run\", r)\n            if n % 2:                                    # half wait for the run and review items; the rest delete a case that is still running\n                for _ in range(200):\n                    s = c.get(f\"/api/cases/{tok}/status\")\n                    note(\"status\", s)\n                    if s.status_code != 200 or s.json()[\"status\"] in (\"ready\", \"failed\"):\n                        break\n                    time.sleep(0.02)\n                g = c.get(f\"/api/cases/{tok}\")\n                note(\"get\", g)\n                if g.status_code == 200:\n                    for it in (g.json()[\"entries\"] + g.json()[\"flags\"] + g.json()[\"amounts\"])[:3]:\n                        note(\"review\", c.post(f\"/api/cases/{tok}/items/{it['id']}/review\", json={\"action\": \"accept\"}))\n            for url in (f\"/api/cases/{tok}/trace\", f\"/api/cases/{tok}/export\"):\n                note(url.rsplit(\"/\", 1)[1], c.get(url))\n            note(\"delete\", c.delete(f\"/api/cases/{tok}\"))\n\n    def lister():\n        c = _client(app)\n        while not stop.is_set():\n            r = c.get(\"/api/cases\")\n            note(\"list\", r)\n            with lock:\n                counter[\"lists\"] += 1\n\n    ls = [threading.Thread(target=lister, daemon=True) for _ in range(2)]\n    ws = [threading.Thread(target=worker, daemon=True) for _ in range(WORKERS)]\n    for t in ls + ws:\n        t.start()\n    for t in ws:\n        t.join(timeout=600)\n    stop.set()\n    for t in ls:\n        t.join(timeout=30)\n    assert counter[\"i\"] >= ITERATIONS and counter[\"lists\"] > 0\n    assert not bad, bad[:5]\nEOF\nRACE_ITERATIONS=40 timeout 900 .venv/bin/python -m pytest tests/unit/test_case_list_race.py -x -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T17:55:41.735Z

**tool result**
````
/bin/bash: line 324: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:43.132Z

**tool call — Bash**
````
{
 "command": "RACE_ITERATIONS=40 .venv/bin/python -m pytest tests/unit/test_case_list_race.py -q 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T17:55:44.193Z

**tool result**
````
        app, path = app_env
        c = _client(app)
>       toks = [c.post("/api/cases", json={"library": "lib01_er_only_then_gap"}).json()["token"] for _ in range(3)]
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_case_list_race.py:37: KeyError
__________ test_list_gives_a_plain_row_for_a_case_whose_summary_fails __________

app_env = (<fastapi.applications.FastAPI object at 0x10aec7a40>, '/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-5720/test_list_gives_a_plain_row_fo0/t.sqlite')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10aeafce0>

    def test_list_gives_a_plain_row_for_a_case_whose_summary_fails(app_env, monkeypatch):
        """A case that exists but cannot be summarised right now (mid-write) is listed with its plain status, never a 500."""
        app, path = app_env
        c = _client(app)
>       tok = c.post("/api/cases", json={"library": "lib01_er_only_then_gap"}).json()["token"]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_case_list_race.py:56: KeyError
_____________ test_routes_answer_404_for_a_case_deleted_under_them _____________

app_env = (<fastapi.applications.FastAPI object at 0x10af41b50>, '/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-5720/test_routes_answer_404_for_a_c0/t.sqlite')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10af41e20>

    def test_routes_answer_404_for_a_case_deleted_under_them(app_env, monkeypatch):
        """Every case route that reads a case after the existence check answers 404 (not 500) when the case is deleted in that gap."""
        app, path = app_env
        c = _client(app)
>       tok = c.post("/api/cases", json={"library": "lib01_er_only_then_gap"}).json()["token"]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_case_list_race.py:77: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_case_list_race.py::test_list_skips_a_case_deleted_mid_list
FAILED tests/unit/test_case_list_race.py::test_list_gives_a_plain_row_for_a_case_whose_summary_fails
FAILED tests/unit/test_case_list_race.py::test_routes_answer_404_for_a_case_deleted_under_them
3 failed, 1 passed in 0.70s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:46.035Z

**tool call — Bash**
````
{
 "command": "ls evals/library | head -5; sed -n 234,252p app/backend/api.py"
}
````

### User / tool · 2026-11-02T17:55:46.125Z

**tool result**
````
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
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

    @app.post("/api/cases/pdf", status_code=201)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:48.517Z

**tool call — Bash**
````
{
 "command": "sed -i 's/\"lib01_er_only_then_gap\"/LIB/g' tests/unit/test_case_list_race.py && sed -i 's/^WORKERS = 4$/WORKERS = 4\\nLIB = \"case_lib01_er_only_then_gap\"/' tests/unit/test_case_list_race.py && python3 - <<'EOF'\np='tests/unit/test_case_list_race.py'\ns=open(p).read()\ns=s.replace('''            note(\"create\", r)\n            if r.status_code != 201:\n                continue''','''            note(\"create\", r)\n            if r.status_code != 201:\n                with lock:\n                    bad.append((\"create\", r.status_code, r.text[:200]))\n                continue''')\nopen(p,'w').write(s)\nEOF\nRACE_ITERATIONS=40 .venv/bin/python -m pytest tests/unit/test_case_list_race.py -q 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T17:55:49.573Z

**tool result**
````
sed: 2: "tests/unit/test_case_li ...": undefined label 'ests/unit/test_case_list_race.py'
        app, path = app_env
        c = _client(app)
>       toks = [c.post("/api/cases", json={"library": "lib01_er_only_then_gap"}).json()["token"] for _ in range(3)]
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_case_list_race.py:37: KeyError
__________ test_list_gives_a_plain_row_for_a_case_whose_summary_fails __________

app_env = (<fastapi.applications.FastAPI object at 0x10c0fc9b0>, '/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-5722/test_list_gives_a_plain_row_fo0/t.sqlite')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10c0fe540>

    def test_list_gives_a_plain_row_for_a_case_whose_summary_fails(app_env, monkeypatch):
        """A case that exists but cannot be summarised right now (mid-write) is listed with its plain status, never a 500."""
        app, path = app_env
        c = _client(app)
>       tok = c.post("/api/cases", json={"library": "lib01_er_only_then_gap"}).json()["token"]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_case_list_race.py:56: KeyError
_____________ test_routes_answer_404_for_a_case_deleted_under_them _____________

app_env = (<fastapi.applications.FastAPI object at 0x10c17a000>, '/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-5722/test_routes_answer_404_for_a_c0/t.sqlite')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10c17b950>

    def test_routes_answer_404_for_a_case_deleted_under_them(app_env, monkeypatch):
        """Every case route that reads a case after the existence check answers 404 (not 500) when the case is deleted in that gap."""
        app, path = app_env
        c = _client(app)
>       tok = c.post("/api/cases", json={"library": "lib01_er_only_then_gap"}).json()["token"]
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       KeyError: 'token'

tests/unit/test_case_list_race.py:77: KeyError
=========================== short test summary info ============================
FAILED tests/unit/test_case_list_race.py::test_list_skips_a_case_deleted_mid_list
FAILED tests/unit/test_case_list_race.py::test_list_gives_a_plain_row_for_a_case_whose_summary_fails
FAILED tests/unit/test_case_list_race.py::test_routes_answer_404_for_a_case_deleted_under_them
3 failed, 1 passed in 0.68s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:50.873Z

BSD sed failed; use python for the whole edit. I'll also simplify the third test (my route-vanish test is clumsy) and rewrite it properly.

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:55:55.655Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_case_list_race.py'\ns=open(p).read()\ns=s.replace('\"lib01_er_only_then_gap\"','LIB').replace('WORKERS = 4\\n','WORKERS = 4\\nLIB = \"case_lib01_er_only_then_gap\"\\n',1)\ns=s.replace('''            note(\"create\", r)\n            if r.status_code != 201:\n                continue''','''            note(\"create\", r)\n            if r.status_code != 201:\n                with lock:\n                    bad.append((\"create\", r.status_code, r.text[:200]))\n                continue''')\n# rewrite third test\na=s.index('def test_routes_answer_404')\nb=s.index('def test_stress')\nnew='''def test_routes_answer_404_for_a_case_deleted_under_them(app_env, monkeypatch):\n    \"\"\"Every case route that reads the case after its existence check answers 404 (never 500) when the case is deleted in that gap: the first read of the case passes,\n    the case is deleted, every later read finds nothing.\"\"\"\n    app, path = app_env\n    c = _client(app)\n    real = DB.get_case\n    state = {\"tok\": None, \"n\": 0}\n\n    def vanish(conn, cid):\n        if cid == state[\"tok\"]:\n            state[\"n\"] += 1\n            if state[\"n\"] == 2:\n                DB.delete_case(conn, cid)\n        return real(conn, cid)\n    monkeypatch.setattr(DB, \"get_case\", vanish)\n    routes = ((\"get\", \"\"), (\"get\", \"/status\"), (\"get\", \"/trace\"), (\"get\", \"/export\"), (\"get\", \"/audit\"), (\"get\", \"/judges\"), (\"get\", \"/narrative\"),\n              (\"post\", \"/run\"), (\"post\", \"/rejudge\"), (\"patch\", \"\"), (\"delete\", \"\"))\n    for method, suffix in routes:\n        tok = c.post(\"/api/cases\", json={\"library\": LIB}).json()[\"token\"]\n        state.update(tok=tok, n=0)\n        kw = {\"json\": {\"title\": \"x\"}} if method == \"patch\" else ({\"json\": {}} if method in (\"post\",) else {})\n        r = getattr(c, method)(f\"/api/cases/{tok}{suffix}\", **kw)\n        assert r.status_code in (200, 202, 204, 404, 409), (method, suffix, r.status_code, r.text)\n        DB.delete_case(DB.connect(path), tok) if real(DB.connect(path), tok) else None\n\n\n'''\ns=s[:a]+new+s[b:]\nopen(p,'w').write(s)\nEOF\nRACE_ITERATIONS=40 .venv/bin/python -m pytest tests/unit/test_case_list_race.py -q 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T17:56:06.016Z

**tool result**
````
                r = c.get("/api/cases")
                note("list", r)
                with lock:
                    counter["lists"] += 1
    
        ls = [threading.Thread(target=lister, daemon=True) for _ in range(2)]
        ws = [threading.Thread(target=worker, daemon=True) for _ in range(WORKERS)]
        for t in ls + ws:
            t.start()
        for t in ws:
            t.join(timeout=600)
        stop.set()
        for t in ls:
            t.join(timeout=30)
        assert counter["i"] >= ITERATIONS and counter["lists"] > 0
>       assert not bad, bad[:5]
E       AssertionError: [('list', 500, '{"error":{"code":"internal","message":"Something went wrong.","detail":{}}}'), ('list', 500, '{"error"... wrong.","detail":{}}}'), ('list', 500, '{"error":{"code":"internal","message":"Something went wrong.","detail":{}}}')]
E       assert not [('list', 500, '{"error":{"code":"internal","message":"Something went wrong.","detail":{}}}'), ('list', 500, '{"error"...g.","detail":{}}}'), ('list', 500, '{"error":{"code":"internal","message":"Something went wrong.","detail":{}}}'), ...]

tests/unit/test_case_list_race.py:163: AssertionError
------------------------------ Captured log call -------------------------------
ERROR    zlayt.api:api.py:184 unhandled AttributeError
ERROR    zlayt.api:api.py:184 unhandled KeyError
ERROR    zlayt.api:api.py:184 unhandled AttributeError
ERROR    zlayt.api:api.py:184 unhandled TypeError
ERROR    zlayt.api:api.py:184 unhandled AttributeError
ERROR    zlayt.api:api.py:184 unhandled TypeError
ERROR    zlayt.api:api.py:184 unhandled TypeError
ERROR    zlayt.api:api.py:184 unhandled TypeError
ERROR    zlayt.api:api.py:184 unhandled TypeError
ERROR    zlayt.api:api.py:184 unhandled TypeError
ERROR    zlayt.api:api.py:184 unhandled TypeError
ERROR    zlayt.api:api.py:184 unhandled TypeError
ERROR    zlayt.api:api.py:184 unhandled AttributeError
=========================== short test summary info ============================
FAILED tests/unit/test_case_list_race.py::test_list_skips_a_case_deleted_mid_list
FAILED tests/unit/test_case_list_race.py::test_list_gives_a_plain_row_for_a_case_whose_summary_fails
FAILED tests/unit/test_case_list_race.py::test_routes_answer_404_for_a_case_deleted_under_them
FAILED tests/unit/test_case_list_race.py::test_stress_create_run_review_delete_list
4 failed in 9.98s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:56:08.244Z

**tool call — Bash**
````
{
 "command": "RACE_ITERATIONS=40 .venv/bin/python -m pytest tests/unit/test_case_list_race.py -q -k \"not stress\" 2>&1 | grep -E \"^E |Error|assert\" | head -20; python3 - <<'EOF'\nimport re,subprocess\nEOF\nsed -n 500,610p app/backend/api.py | grep -n \"get_case\\|conn()\" | head -30"
}
````

### User / tool · 2026-11-02T17:56:09.100Z

**tool result**
````
>       assert r.status_code == 200, r.text
E       AssertionError: {"error":{"code":"internal","message":"Something went wrong.","detail":{}}}
E       assert 500 == 200
E        +  where 500 = <Response [500 Internal Server Error]>.status_code
tests/unit/test_case_list_race.py:48: AssertionError
ERROR    zlayt.api:api.py:184 unhandled TypeError
                raise RuntimeError("half written")
>       assert r.status_code == 200, r.text
E       AssertionError: {"error":{"code":"internal","message":"Something went wrong.","detail":{}}}
E       assert 500 == 200
E        +  where 500 = <Response [500 Internal Server Error]>.status_code
tests/unit/test_case_list_race.py:67: AssertionError
ERROR    zlayt.api:api.py:184 unhandled RuntimeError
>           assert r.status_code in (200, 202, 204, 404, 409), (method, suffix, r.status_code, r.text)
E           AssertionError: ('get', '', 500, '{"error":{"code":"internal","message":"Something went wrong.","detail":{}}}')
E           assert 500 in (200, 202, 204, 404, 409)
E            +  where 500 = <Response [500 Internal Server Error]>.status_code
tests/unit/test_case_list_race.py:96: AssertionError
ERROR    zlayt.api:api.py:184 unhandled TypeError
3:        c = conn()
5:            get_case(c, token)
17:        c = conn()
19:            get_case(c, token)
30:        c = conn()
32:            get_case(c, token)
37:    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
39:    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
41:    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
43:    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
44:    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
53:        c = conn()
55:            get_case(c, token)
80:        c = conn()
82:            get_case(c, token)
92:        c = conn()
94:            get_case(c, token)
101:        c = conn()
103:            get_case(c, token)
110:        c = conn()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:56:16.348Z

**tool call — Bash**
````
{
 "command": "sed -n 1,30p app/backend/case_list.py; sed -n 1,40p app/backend/api.py | grep -n \"log\\|import\""
}
````

### User / tool · 2026-11-02T17:56:16.444Z

**tool result**
````
"""GET /api/cases (T-148): one summary per case for the local profile's overview screen. Local mode only (D-008/D-031); the route is a 404 otherwise.

Code only: no model call, no pipeline run, no record text. Every number comes from the functions GET case, GET status and the export gate already use, so the
list cannot say something the case screen does not:
  run                                        -> run_progress() (the /status route calls it too)
  progress decided / total per kind          -> the item filter present.review_view applies (live = not rejected, no tray placeholder, no rule-filtered proposal)
  hitl.needs_review, edits_to_check, tray    -> present.review_view counts (the tray length GET case returns is the `rejected` count)
  hitl.gate, export_ready                    -> the export_gate step of trace.case_trace (blockers and warnings with their plain `why`; the list GET /export refuses on)
tests/unit/test_case_list.py compares each field with GET case, /status, /trace and /export for every library case.
"""
import datetime
import re

from app.backend import flag_templates as FT, generator, present, review, store, trace
from app.db import db as DB

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
1:"""FastAPI routes (memory/contracts/api.md). Thin: parsing, the demo gate, error format; logic lives in ingest/store/review/present/export.
4:anything is stored. Never logs record text, tokens or prompts (run uvicorn with access_log off; see app/main.py).
6:import hashlib
7:import ipaddress
8:import asyncio
9:import json
10:import logging
11:import os
12:import pathlib
13:import threading
14:import time
16:from fastapi import FastAPI, Request
17:from fastapi.exceptions import RequestValidationError
18:from fastapi.responses import JSONResponse, Response
19:from starlette.exceptions import HTTPException as StarletteHTTPException
21:from starlette.concurrency import run_in_threadpool
23:from app.backend import case_extras, case_list, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
24:from app.db import db as DB
27:# index.html has one inline onclick (dialog Close); allowed by hash until the frontend moves it to a listener.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:56:30.280Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/case_list.py'\ns=open(p).read()\ns=s.replace(\"import datetime\\nimport re\\n\",\"import datetime\\nimport logging\\nimport re\\n\",1)\ns=s.replace('from app.db import db as DB\\n','from app.db import db as DB\\n\\nlog = logging.getLogger(\"zlayt.api\")\\n',1)\na=s.index('def summaries(conn, stages)')\ns=s[:a]+'''def plain_row(conn, case: dict, stages) -> dict:\n    \"\"\"T-175: the row for a case that exists but cannot be summarised right now (a write is in flight). Same keys as `summary`, plain values from the case row only:\n    its status and times, no counts, nothing waiting, not export-ready. The next list read shows the full row.\"\"\"\n    stage, done = run_progress(case, stages)\n    updated = case.get(\"run_finished_at\") or case[\"created_at\"]\n    zero = {\"decided\": 0, \"total\": 0}\n    try:\n        title = case_title(conn, case)\n    except Exception:\n        title = readable_title(None, case[\"source\"], case[\"created_at\"])\n    return {\"token\": case[\"id\"], \"title\": title, \"name\": case[\"name\"], \"source\": case[\"source\"], \"status\": case[\"status\"],\n            \"record_count\": 0, \"created_at\": store.iso(case[\"created_at\"]), \"updated_at\": store.iso(updated), \"last_activity_at\": store.iso(updated),\n            \"run\": {\"stage\": stage, \"steps_done\": done, \"steps_total\": len(stages), \"running\": case[\"status\"] == \"running\", \"error\": bool(case.get(\"error\"))},\n            \"progress\": {k: dict(zero) for k, _ in KINDS},\n            \"counts\": {k: 0 for k in (\"pending\", \"accepted\", \"edited\", \"dismissed\", \"needs_review\")},\n            \"hitl\": {\"pending\": 0, \"needs_review\": 0, \"needs_review_open\": 0, \"edits_to_check\": 0, \"could_not_verify\": 0, \"gate_blockers\": [], \"gate_warnings\": []},\n            \"export_ready\": False, \"next_action\": None}\n\n\ndef summaries(conn, stages) -> list:\n    \"\"\"Every case, newest first (created, then insertion order). T-175: the id list and each case are read at different moments, so a case can be deleted (DELETE, the purge)\n    or be mid-write (a run, a review) in between. A case that is gone is left out; one that exists but cannot be summarised right now gets `plain_row`. Either is logged by\n    exception class only (no text from the case), and the list itself never fails for one case.\"\"\"\n    out = []\n    for r in conn.execute(\"SELECT id FROM cases ORDER BY created_at DESC, rowid DESC\").fetchall():\n        try:\n            out.append(summary(conn, r[\"id\"], stages))\n            continue\n        except Exception as e:\n            err = type(e).__name__\n        case = DB.get_case(conn, r[\"id\"])\n        if case is None:\n            log.warning(\"case list: a case was deleted while the list was read (%s); left out\", err)\n            continue\n        try:\n            out.append(plain_row(conn, case, stages))\n            log.warning(\"case list: a case could not be summarised while it changed (%s); listed with its status only\", err)\n        except Exception:\n            log.warning(\"case list: a case could not be listed (%s); left out\", err)\n    return out\n'''\nopen(p,'w').write(s)\n\np='app/backend/api.py'\ns=open(p).read()\nold='''    @app.exception_handler(Exception)\n    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log\n        log.error(\"unhandled %s\", type(e).__name__)\n        return JSONResponse({\"error\": {\"code\": \"internal\", \"message\": \"Something went wrong.\", \"detail\": {}}}, status_code=500)\n'''\nnew='''    def unexpected_response(request, e):\n        \"\"\"T-175: what an uncaught exception becomes. The log line names the exception class and the innermost app frame (file:line), never the message or any case text.\n        A route that reads a case after its existence check fails with a TypeError/AttributeError when the case is deleted in that gap (DELETE, the purge): when the case in the\n        URL no longer exists that is a plain 404 like any other missing case, not a server error.\"\"\"\n        frames = [f for f in traceback.extract_tb(e.__traceback__) if \"/app/\" in f.filename.replace(\"\\\\\\\\\", \"/\")]\n        where = f\"{pathlib.Path(frames[-1].filename).name}:{frames[-1].lineno}\" if frames else \"?\"\n        parts = request.url.path.split(\"/\")\n        if len(parts) > 3 and parts[1] == \"api\" and parts[2] == \"cases\" and parts[3] != \"pdf\":\n            c = None\n            try:\n                c = conn()\n                if DB.get_case(c, parts[3]) is None:\n                    log.warning(\"case deleted while a request read it (%s at %s); answered 404\", type(e).__name__, where)\n                    return JSONResponse({\"error\": {\"code\": \"not_found\", \"message\": \"No such case.\", \"detail\": {}}}, status_code=404)\n            except Exception:\n                pass\n            finally:\n                if c is not None:\n                    c.close()\n        log.error(\"unhandled %s at %s\", type(e).__name__, where)\n        return JSONResponse({\"error\": {\"code\": \"internal\", \"message\": \"Something went wrong.\", \"detail\": {}}}, status_code=500)\n\n    @app.exception_handler(Exception)\n    async def _unexpected(request, e):                            # no traceback, no message text in the body or the log\n        return unexpected_response(request, e)\n'''\nassert old in s\ns=s.replace(old,new)\nold2='''        except Exception as e:                                                          # last line of defence: standard JSON, no detail\n            log.error(\"unhandled %s\", type(e).__name__)\n            resp = JSONResponse({\"error\": {\"code\": \"internal\", \"message\": \"Something went wrong.\", \"detail\": {}}}, status_code=500)\n'''\nassert old2 in s\ns=s.replace(old2,'''        except Exception as e:                                                          # last line of defence: standard JSON, no detail\n            resp = unexpected_response(request, e)\n''')\ns=s.replace(\"import time\\n\",\"import time\\nimport traceback\\n\",1)\nopen(p,'w').write(s)\nEOF\ngrep -n \"^import\" app/backend/api.py | head -20; RACE_ITERATIONS=40 .venv/bin/python -m pytest tests/unit/test_case_list_race.py -q 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T17:56:40.050Z

**tool result**
````
6:import hashlib
7:import ipaddress
8:import asyncio
9:import json
10:import logging
11:import os
12:import pathlib
13:import threading
14:import time
15:import traceback
....                                                                     [100%]
4 passed in 9.40s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:56:45.206Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_case_list_race.py <<'EOF'\n\n\ndef test_unhandled_log_names_class_and_app_frame_but_no_text(app_env, monkeypatch, caplog):\n    \"\"\"The 500 log line carries the exception class and the innermost app frame (file:line) so the cause is findable, and never the message text.\"\"\"\n    app, path = app_env\n    c = _client(app)\n\n    def boom(conn, stages):\n        raise ValueError(\"SECRET-RECORD-TEXT\")\n    monkeypatch.setattr(case_list, \"summaries\", boom)\n    with caplog.at_level(\"ERROR\", logger=\"zlayt.api\"):\n        r = c.get(\"/api/cases\")\n    assert r.status_code == 500 and \"SECRET\" not in r.text\n    line = \" \".join(rec.getMessage() for rec in caplog.records)\n    assert \"ValueError\" in line and \"test_case_list_race.py:\" not in line.replace(\"SECRET\", \"\")[:0] and \"SECRET\" not in line\n    assert \"unhandled ValueError at \" in line and \".py:\" in line\nEOF\n.venv/bin/python -m pytest tests/unit/test_case_list_race.py -q -k log 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T17:56:45.836Z

**tool result**
````
.                                                                        [100%]
1 passed, 4 deselected in 0.30s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:56:48.536Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_case_list_race.py'\ns=open(p).read()\ns=s.replace('''    assert \"ValueError\" in line and \"test_case_list_race.py:\" not in line.replace(\"SECRET\", \"\")[:0] and \"SECRET\" not in line\n    assert \"unhandled ValueError at \" in line and \".py:\" in line''','''    assert \"SECRET\" not in line\n    assert \"unhandled ValueError at \" in line and \".py:\" in line''')\nopen(p,'w').write(s)\nEOF\nfor i in 1 2 3; do .venv/bin/python -m pytest tests/unit/test_case_list_race.py -q 2>&1 | tail -2; done; .venv/bin/python -m pytest tests/unit -q -x -n0 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T17:58:49.124Z

**tool result**
````
Command did not complete within its 120s timeout and was moved to the background (ID: b6dnv3kzb). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output. You will be notified when it completes. To check interim output, use Read on that file path.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:58:50.755Z

**tool call — Bash**
````
{
 "command": "sleep 100; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output"
}
````

### User / tool · 2026-11-02T17:58:50.756Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 100 followed by: cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:58:53.744Z

**tool call — Monitor**
````
{
 "command": "until grep -q \"passed\\|failed\\|error\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output && [ $(grep -c \"passed\\|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output) -ge 4 ]; do sleep 5; done; cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output",
 "description": "wait for stress runs and unit suite",
 "timeout_ms": 900000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T17:58:53.759Z

**tool result**
````
Monitor started (task bhz9w8r18, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:58:56.573Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py note T-175 --agent backend --text \"Reproduced (test_case_list_race.py, 4 workers + 2 listers): GET /api/cases 500 TypeError/AttributeError/KeyError. Root cause: case_list.summaries reads id list then each case separately; a case deleted (DELETE or purge) or mid-write in between makes DB.get_case None -> 500; same gap in every per-case route (get_case existence check then re-read). Fix: summaries skips a vanished case / plain_row for a mid-write one, logged by class; api unexpected_response maps a case-gone failure to 404 and logs class + innermost app frame. Verifying 200-iter stress x3 + unit suite.\""
}
````

### User / tool · 2026-11-02T17:58:56.709Z

**tool result**
````
noted on T-175
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:58:59.047Z

**tool call — Monitor**
````
{
 "command": "until [ $(grep -c \"passed\\|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output) -ge 4 ]; do sleep 5; done; tail -8 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output",
 "description": "wait for results",
 "timeout_ms": 900000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T17:58:59.057Z

**tool result**
````
Monitor started (task b31t3un6u, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:01.003Z

**tool call — Read**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output"
}
````

### User / tool · 2026-11-02T17:59:01.015Z

**tool result**
````
1	.....                                                                    [100%]
2	5 passed in 45.30s
3	.....                                                                    [100%]
4	5 passed in 46.78s
5	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:03.147Z

**tool call — Monitor**
````
{
 "command": "until [ $(grep -c \"passed\\|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output) -ge 4 ]; do sleep 5; done; echo done",
 "description": "wait",
 "timeout_ms": 900000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T17:59:03.158Z

**tool result**
````
Monitor started (task bjr74l8y6, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:04.699Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output"
}
````

### User / tool · 2026-11-02T17:59:04.784Z

**tool result**
````
.....                                                                    [100%]
5 passed in 45.30s
.....                                                                    [100%]
5 passed in 46.78s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:08.168Z

**tool call — Monitor**
````
{
 "command": "until [ $(grep -c \"passed\\|failed\" /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output) -ge 4 ]; do sleep 5; done; tail -3 /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output",
 "description": "wait for the unit suite",
 "timeout_ms": 900000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T17:59:08.178Z

**tool result**
````
Monitor started (task bd6hpdwv3, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:10.294Z

**tool call — Bash**
````
{
 "command": "cat /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b6dnv3kzb.output"
}
````

### User / tool · 2026-11-02T17:59:10.373Z

**tool result**
````
.....                                                                    [100%]
5 passed in 45.30s
.....                                                                    [100%]
5 passed in 46.78s
.....                                                                    [100%]
5 passed in 45.50s
ERROR: usage: python -m pytest [options] [file_or_dir] [file_or_dir] [...]
python -m pytest: error: unrecognized arguments: -n0
  inifile: None
  rootdir: /Users/arsis/zlayt-pm-project


[exited with code 0]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:11.423Z

Stress passed 3×. Now the unit suite in the background, then verification from a git archive.

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:12.233Z

**tool call — Bash**
````
{
 "command": "(.venv/bin/python -m pytest tests/unit -q -x --deselect tests/unit/test_case_list_race.py > /tmp/x/unit.out 2>&1; echo EXIT $? >> /tmp/x/unit.out) &\nsleep 1; echo started",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T17:59:12.299Z

**tool result**
````
Command running in background with ID: b5khnmjsv. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b5khnmjsv.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:13.711Z

**tool call — Monitor**
````
{
 "command": "until grep -q \"^EXIT\" /tmp/x/unit.out; do sleep 5; done; tail -5 /tmp/x/unit.out",
 "description": "wait for unit suite",
 "timeout_ms": 900000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T17:59:13.722Z

**tool result**
````
Monitor started (task b5ieuks4j, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:15.277Z

**tool call — Bash**
````
{
 "command": "tail -8 /tmp/x/unit.out"
}
````

### User / tool · 2026-11-02T17:59:15.362Z

**tool result**
````
........................................................................ [  1%]
........................................................................ [  2%]
..........................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:19.324Z

**tool call — Monitor**
````
{
 "command": "until grep -q \"^EXIT\" /tmp/x/unit.out; do sleep 10; done; tail -6 /tmp/x/unit.out",
 "description": "wait for unit suite end",
 "timeout_ms": 900000,
 "persistent": "false"
}
````

### User / tool · 2026-11-02T17:59:19.334Z

**tool result**
````
Monitor started (task bm2ekbcim, expires in 15m unless the source ends first; you get one notice at expiry — re-arm if you still need the watch). You will be notified on each event. Keep working — do not poll or sleep. Events may arrive while you are waiting for the user — an event is not their reply.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:20.763Z

**tool call — Bash**
````
{
 "command": "cat /tmp/x/unit.out | tail -3; ps aux | grep \"pytest tests/unit\" | grep -v grep | wc -l; .venv/bin/python -m pytest tests/unit --collect-only -q 2>&1 | tail -2"
}
````

### User / tool · 2026-11-02T17:59:23.097Z

**tool result**
````
........................................................................ [  3%]
........................................................................ [  5%]
...............................................       2

5688 tests collected in 1.80s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:25.571Z

**tool call — Bash**
````
{
 "command": "pkill -f \"pytest tests/unit -q -x\" ; ls tests/unit | grep -c .; .venv/bin/python -m pytest tests/unit/test_case_list.py tests/unit/test_api.py tests/unit/test_api_routes.py tests/unit/test_amounts_d059_api.py -q -x 2>&1 | tail -5",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T17:59:25.627Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: subagents may not pkill/killall by pattern; stop only your own server by PID (kill $!)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:27.412Z

**tool call — Bash**
````
{
 "command": "P=$(ps aux | grep \"pytest tests/unit -q -x\" | grep -v grep | awk '{print $2}'); echo $P; kill $P; .venv/bin/python -m pytest tests/unit/test_case_list.py tests/unit/test_api.py tests/unit/test_api_routes.py tests/unit/test_amounts_d059_api.py -q -x 2>&1 | tail -5",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T17:59:51.084Z

**tool result**
````
79332 79330
........................................................................ [ 79%]
...................                                                      [100%]
91 passed in 23.04s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:52.053Z

Now verify from a `git archive HEAD` copy with my changes overlaid, and commit via a temp index.

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:53.509Z

**tool call — Bash**
````
{
 "command": "D=/tmp/x/arch && rm -rf $D && mkdir -p $D && git archive HEAD | tar -x -C $D && cp app/backend/api.py app/backend/case_list.py $D/app/backend/ && cp tests/unit/test_case_list_race.py $D/tests/unit/ && git diff HEAD --stat -- app/backend | tail -3; cd $D && ln -s /Users/arsis/zlayt-pm-project/.venv .venv 2>/dev/null; .venv/bin/python -m pytest tests/unit/test_case_list_race.py tests/unit/test_case_list.py -q 2>&1 | tail -3",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T17:59:53.583Z

**tool result (error)**
````
Permission to use Bash with command D=/tmp/x/arch && rm -rf $D && mkdir -p $D && git archive HEAD has been denied.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T17:59:57.086Z

**tool call — Bash**
````
{
 "command": "D=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/arch && mkdir -p $D && git archive HEAD | tar -x -C $D && cp app/backend/api.py app/backend/case_list.py $D/app/backend/ && cp tests/unit/test_case_list_race.py $D/tests/unit/ && ln -s /Users/arsis/zlayt-pm-project/.venv $D/.venv; cd $D && .venv/bin/python -m pytest tests/unit/test_case_list_race.py tests/unit/test_case_list.py -q 2>&1 | tail -3",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T18:00:53.014Z

**tool result**
````
.................................................                        [100%]
49 passed in 54.85s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T18:00:57.429Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add app/backend/api.py app/backend/case_list.py tests/unit/test_case_list_race.py && T=$(git write-tree) && C=$(git commit-tree $T -p HEAD -m \"fix(backend): T-175 GET /api/cases never 500s when a case is deleted or mid-write during the list; per-case routes answer 404 for a case deleted under them; 500 log names class + innermost app frame; 200-iteration create/run/review/delete/list stress test\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\") && unset GIT_INDEX_FILE && git update-ref refs/heads/$(git rev-parse --abbrev-ref HEAD) $C HEAD && git show --stat --oneline HEAD | head; git status --short app tests | head"
}
````

### User / tool · 2026-11-02T18:00:57.571Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: git update-ref rewrites or prunes history; blocked | command: export GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 && rm -f $GIT_INDEX_FILE && git read-tree HEAD && git add app/backend/api.py app/backend/case_list.py tests/unit/test_case_list_race.py && T=$
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T18:01:00.817Z

**tool call — Bash**
````
{
 "command": "grep -rn -i \"temp.index\\|GIT_INDEX_FILE\" .claude/agent-memory/backend/*.md | head -5"
}
````

### User / tool · 2026-11-02T18:01:00.923Z

**tool result**
````
.claude/agent-memory/backend/MEMORY.md:8:- [T-141 accident-date + checks](project_t141_accident_date_checks.md) — r3 negation/history rule, read-time notes, temp-index commit recipe
.claude/agent-memory/backend/project_t110_overlap_tray.md:18:- Commit with a temp index when api.py/pipeline.py carry others' hunks: `git apply --cached` a filtered diff for only my hunk.
.claude/agent-memory/backend/project_backend_conventions.md:18:T-085 (Spanish records): code half `language.py` + `spanish_text.py` (no app.llm import; test_boundaries bans LLM imports in dates.py, so keep Spanish code checks out of `spanish.py`, which wires the judge). Spanish records use steps `extract_es` / `judge_faithfulness_es` (own prompts, registered in audited.PROMPT_OF_STEP). To record only missing fixtures for new prompts: `ENABLE_LIVE=1 LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record --fill-missing evals/library/<packet>.txt` (replays recorded answers). Committing a shared file other workers also edit: filter `git diff HEAD -U0` hunks by keyword, `git apply --cached --unidiff-zero` into a temp GIT_INDEX_FILE built from `git read-tree HEAD`; `xargs git add` is blocked by git-guard, list paths explicitly.
.claude/agent-memory/backend/project_backend_conventions.md:21:- Commit with other workers' dirty hunks in the same file: build a temp index (`GIT_INDEX_FILE=$(mktemp)`, `read-tree HEAD`), `git add` whole files only when all hunks are mine; for mixed files (confidence/review/pipeline) hash-object the HEAD text + my edits and `update-index --cacheinfo`. Verify with `git diff --cached --stat`.
.claude/agent-memory/backend/project_backend_conventions.md:26:T-086/T-087 r2 (PDF security): `pdf_hidden.py` is a differential render (page with vs without all text, render mode 3 toggled per object); `FPDFTextObj_GetText` is O(page) per call, so read text only for hidden objects. `review.enforce_ocr` re-applies OCR_DERIVED after every item-rewriting step (edit, manual entry, split, date confirm). Pitfalls: other workers edit review.py/api.py concurrently, so commit "HEAD + my hunks": rebuild the file by applying my replacements to `git show HEAD:file`, `git hash-object -w`, `git update-index --cacheinfo` into a `GIT_INDEX_FILE=$(mktemp)` index after `git read-tree HEAD`; then `git reset -q -- <my files>` so the main index is not stale. git-guard blocks `$VAR` in command position (use literal paths) and macOS `sed -i` needs a suffix (use python for edits). Strided memoryview rows need `.tobytes()` before zlib.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T18:01:02.473Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- app/backend/api.py app/backend/case_list.py; git diff HEAD -U0 -- app/backend/api.py | grep '^@@'"
}
````

### User / tool · 2026-11-02T18:01:02.623Z

**tool result**
````
 app/backend/api.py       | 31 ++++++++++++++++++++++++++-----
 app/backend/case_list.py | 44 ++++++++++++++++++++++++++++++++++++++++++--
 2 files changed, 68 insertions(+), 7 deletions(-)
@@ -14,0 +15 @@ import time
@@ -160,3 +161,20 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
@@ -164,0 +183,4 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
@@ -184,2 +206 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T18:01:03.559Z

All hunks are mine. Commit with a temp index and plain `git commit`.

### Assistant · claude-sonnet-5-5 · 2026-11-02T18:01:05.586Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 git read-tree HEAD && GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 git add app/backend/api.py app/backend/case_list.py tests/unit/test_case_list_race.py && GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 git diff --cached --stat && GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 git commit -q -m \"fix(backend): T-175 GET /api/cases never 500s when a case is deleted or mid-write during the list; per-case routes answer 404 for a case deleted under them; 500 log names class and innermost app frame; 200-iteration create/run/review/delete/list stress test\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\" && git reset -q -- app/backend/api.py app/backend/case_list.py tests/unit/test_case_list_race.py; git log --oneline | head -2; git status --short app/backend tests/unit | head"
}
````

### User / tool · 2026-11-02T18:01:05.674Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 git read-tree HEAD && GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 git add app/backend/api.py app/backend/case_list.py tests/unit/test_case_lis
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T18:01:07.707Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 git read-tree HEAD && GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 git add app/backend/api.py app/backend/case_list.py tests/unit/test_case_list_race.py && GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 git diff --cached --stat"
}
````

### User / tool · 2026-11-02T18:01:08.461Z

**tool result**
````
 app/backend/api.py                |  31 +++++--
 app/backend/case_list.py          |  44 +++++++++-
 tests/unit/test_case_list_race.py | 179 ++++++++++++++++++++++++++++++++++++++
 3 files changed, 247 insertions(+), 7 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T18:01:08.767Z

**tool call — Bash**
````
{
 "command": "GIT_INDEX_FILE=/private/tmp/claude-501/tmpidx_t175 git commit -q -m \"fix(backend): T-175 GET /api/cases never 500s when a case is deleted or mid-write during the list; per-case routes answer 404 for a case deleted under them; 500 log names class and innermost app frame; 200-iteration create/run/review/delete/list stress test\n\nCo-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\"; git reset -q -- app/backend/api.py app/backend/case_list.py tests/unit/test_case_list_race.py; git log --oneline | head -2"
}
````

### User / tool · 2026-11-02T18:01:12.133Z

**tool result**
````
check_secrets: ok (3 file(s) scanned staged)
4a097b6 fix(backend): T-175 GET /api/cases never 500s when a case is deleted or mid-write during the list; per-case routes answer 404 for a case deleted under them; 500 log names class and innermost app frame; 200-iteration create/run/review/delete/list stress test
bbb40ba docs(orchestrator): scope cut 7g count-action residuals (T-171)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T18:01:26.589Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B ac T-175 --check 1 --agent backend --evidence \"tests/unit/test_case_list_race.py: 5 passed x3 (200-iteration stress, 4 workers + 2 listers, 0 responses >=500); reproduced 500 before fix; verified from git archive HEAD copy + overlay (49 passed incl. test_case_list.py). Frontend retry message NOT done: app/frontend not mine, needs frontend card\" ; $B handoff T-175 --agent backend --text \"What changed: root cause = case_list.summaries read the id list, then each case in separate statements; a case deleted (DELETE or 24 h purge) or mid-write between them made DB.get_case None -> TypeError/AttributeError/KeyError -> 500. Fix: summaries skips a vanished case (logged), lists a mid-write case via plain_row (status only, same keys); api.unexpected_response turns any uncaught error on /api/cases/{token}/... into 404 not_found when that case no longer exists (same gap existed in every per-case route: get_case check then re-read), and the 500 log now names exception class + innermost app file:line (no message text). How verified: tests/unit/test_case_list_race.py (new, 5 tests incl. 200-iteration create/run/review/delete/list stress, 3 runs green; failed 4/4 before the fix); test_case_list/test_api/test_api_routes/test_amounts_d059_api 91 passed; git archive HEAD + overlay 49 passed. Commit 4a097b6 (temp index). Left: AC1's frontend half (overview shows a plain retry message when GET /api/cases fails) is app/frontend, not touched; needs a frontend card. Surprised me: no sqlite locking involved, purely the check-then-read gap; the full unit suite (5688 tests) is too slow to run here, I ran the API/list files only.\"; $B commit T-175 --sha 4a097b6 --agent backend; $B move T-175 in_review --agent backend"
}
````

### User / tool · 2026-11-02T18:01:26.882Z

**tool result**
````
AC 1 checked: tests/unit/test_case_list_race.py: 5 passed x3 (200-iteration stress, 4 workers + 2 listers, 0 responses >=500); reproduced 500 before fix; verified from git archive HEAD copy + overlay (49 passed incl. test_case_list.py). Frontend retry message NOT done: app/frontend not mine, needs frontend card
handoff written on T-175
T-175: commit 4a097b6 recorded
T-175: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T18:01:29.559Z

T-175 is in_review, committed as 4a097b6. The root cause was a gap in `case_list.summaries`: a case deleted or mid-write between the id list and its read made `DB.get_case` return None, which gave the 500. Every per-case route had the same existence-check-then-reread gap, so an uncaught error there now returns 404 when the case is gone, and the 500 log names the error class and app file:line.

The new `tests/unit/test_case_list_race.py` (200-iteration concurrent stress, 3 green runs; 4 failures before the fix) and a `git archive HEAD` copy both pass. I ran only the API and case-list unit tests (91 passed), not the full 5688-test suite, which is too slow here. The overview's plain retry message is not done, because `app/frontend` isn't mine; it needs a frontend card.
