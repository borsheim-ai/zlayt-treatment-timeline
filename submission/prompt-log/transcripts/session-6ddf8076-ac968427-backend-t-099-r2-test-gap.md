# Subagent: Backend: T-099 r2 test gap (Backend: T-099 r2 test gap)

Source: `agent-ac9684272e85c0f3f.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T05:18:32.618Z

You own board card T-099, round 2 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Read reviews/T-099-staff-engineer.md.

The major: removing the state-total check leaves all 23 route tests green. Add a test that fails when that check is removed, and confirm it by mutating the check in a scratch copy. Fix the 3 minors if they're cheap.

Run `.venv/bin/python -m pytest -q tests/unit -k calibration`. Commit with `git add <paths>` and then `git commit -m "..." -- <paths>` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `python3 tools/board.py ac`, the handoff, and `move T-099 in_review --agent backend`. Reply in 1 line.

### User / tool · 2026-11-02T05:18:32.623Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-haiku-5-5 · 2026-11-02T05:18:37.932Z

**tool call — mcp__ccd_turn__update_plan**
````
{
 "items": [
  {
   "content": "Read T-099 review and card",
   "status": "in_progress"
  },
  {
   "content": "Add test that fails when state-total check is removed",
   "status": "pending"
  },
  {
   "content": "Mutation-test the check in a scratch copy",
   "status": "pending"
  },
  {
   "content": "Fix the 3 cheap minors",
   "status": "pending"
  },
  {
   "content": "Run calibration tests",
   "status": "pending"
  },
  {
   "content": "Commit, record ac, handoff, move in_review",
   "status": "pending"
  }
 ],
 "scope": "first_task"
}
````

### User / tool · 2026-11-02T05:18:37.935Z

**tool result (error)**
````
PreToolUse:mcp__ccd_turn__update_plan hook error: Not shown: you are a subagent, and the app shows only the main conversation's task list and wrap-up. Do not call update_plan or wrap_up again; carry on with your task and report your result as usual.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:18:38.287Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-099-staff-engineer.md && echo ---- && python3 tools/board.py show T-099",
 "description": "Read T-099 review and card"
}
````

### User / tool · 2026-11-02T05:18:38.428Z

**tool result**
````
# T-099 staff-engineer-reviewer: GET /api/calibration (commit 3ecb8b1)

Verdict: **changes** (0 blockers, 1 major, 3 minor). The route does what the card says: it serves the committed calibration in the contract shape, returns `calibration: null` for missing and invalid files, invents no numbers, and is read-only and safe in demo mode. The major is a test gap: the rule "state totals equal type totals" can be removed and every test stays green.

Pinning: I reviewed `git archive 3ecb8b1` (the card commit). The live HEAD during the review was f5ddec8; `git diff --stat 3ecb8b1 f5ddec8 -- app/backend/calibration_route.py tests/unit/test_calibration_route.py evals/reports/calibration.json` printed nothing, so the reviewed files are unchanged at live HEAD.

Severity: the card's validation rules are the thing I check against D.2. A hand-edited statement or a wrong sub-count is not an invented number produced by the app (the route serves only what is in the file), so nothing rises to blocker. Those gaps are minors, with the reasons in each finding.

## Findings

**F1 (major). The "state totals equal type totals" rule is untested.** `app/backend/calibration_route.py:73` is the only check of `by_state` against `by_type`. Replacing it with `if False:` leaves `tests/unit/test_calibration_route.py` at 23 passed. The test that looks like it covers it (`sum_mismatch_hand_edit`, `tests/unit/test_calibration_route.py:106`) is rejected by the statement check, because it changes only the count. A consistent hand-edit (count and its sentence changed together) is served as `ok` on the mutant and rejected on the real code: `artifacts/review-evidence/T-099-staff-engineer-results.txt`, "consistent hand-edit" lines. The card lists this rule as validation; a regression would serve a wrong "matched N/M times" line with no failing test.

**F2 (minor). The route checks less than the producer.** `app/backend/calibration_route.py:37-41` (`_statement_ok`) only requires that the substring "N/M times" appear in a statement. `evals/run.py:1041` rebuilds all statements from the counts and requires equality, and `evals/run.py:1043-1045` compares prompt and lexicon hashes with disk. Probe `hand_edit_sentence_claim` rewrites the verified-overall sentence to end "so the letter is safe to send." and the route returns `ok`; the UI shows statements verbatim (`memory/contracts/api.md`, T-099 section). The hash comparison is absent from the route, so a measurement made on older prompts is served with no staleness signal. This is latent, not live: I checked three hashes (`app/llm/lexicon.yaml`, `app/llm/prompts/judge_faithfulness_v1.md`, `app/llm/prompts/extract_v1.md`) with `shasum -a 256` and they match the committed file.

**F3 (minor). Fields the route serves are not cross-checked.** `calibration_route.py:52-57` checks only the type of `backend`, `case_count` and `small_sample`; `:78` checks only that `by_case` is a dict. Probes, all `ok`: `case_count` 500 while the sentences say "10 golden cases" (`hand_edit_case_count`); `by_case` `[1, 9]` in a 55-item cell (`hand_edit_by_case_only`); `by_case` `[12, 9]` (`by_case_matched_gt_total`); `small_sample` false with 10 cases (`small_sample_flipped`, the threshold is `evals/run.py:244`, CAL_SMALL_N = 30); `backend` changed to `claude-sonnet-5-5` while the sentence names the fixture backend (`hand_edit_backend_label`). The counts the card cares about are checked; these labels and sub-counts are not.

**F4 (minor). The card's evidence does not reproduce.** The T-099 card AC 1 says `pytest -q tests/unit -k calibration gives 34 passed`. At 3ecb8b1 the command prints `32 passed, 2 skipped, 1570 deselected`, the skips are `tests/unit/test_eval_runner.py:636: no git repository here (exported tree)`, and `tests/unit/test_calibration_route.py` alone gives 23 passed. The feature is fine; the evidence line is wrong, and "done" rests on it.

## What I exercised

- `git show --stat 3ecb8b1`; `git show 3ecb8b1 -- app/backend/api.py app/backend/calibration_route.py` (read in full); `git archive 3ecb8b1` into the scratchpad.
- `.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration -rs` on the archive: 32 passed, 2 skipped. `tests/unit/test_calibration_route.py` alone: 23 passed.
- State probes on 22 scratch files (missing, not JSON, not UTF-8, list, wrong schema, state total, sentence, floats, bools, cell `matched > total`, not_scored, extra key, directory): `artifacts/review-evidence/T-099-staff-engineer-probe-states.py`. Results: `artifacts/review-evidence/T-099-staff-engineer-results.txt`.
- Consistent hand-edit probe: `artifacts/review-evidence/T-099-staff-engineer-probe-consistent-edit.py` (real code: invalid; mutant: ok).
- HTTP demo-mode probe on the real app: `artifacts/review-evidence/T-099-staff-engineer-probe-http.py`. GET `/api/calibration` returns 200, envelope keys `calibration, message, status`, status `ok`; POST, PUT, PATCH and DELETE return 405; `/api/health` reports `demo_mode: True`; the body contains none of `token`, `excerpt`, `Patient`, `summary`.
- Mutants on a scratch copy: `artifacts/review-evidence/T-099-staff-engineer-mutants.py` (M1 sentence check removed: 1 failed; M2 state-total check removed: 23 passed; M3 `problems()` ignored: 11 failed; M4 all methods accepted: 1 failed; restored: 23 passed).
- Read the committed `evals/reports/calibration.json` and checked its arithmetic: verified 83/84 = 9+54+20 and 9+55+20; needs_review 10/10 = 6+2+2; `source_commit` b85fc1b; `case_count` 10 and `small_sample` true agree with the sentences.
- Read `memory/contracts/api.md` (T-099 section), `evals/run.py:1029-1047` (`check_calibration`), `evals/run.py:6` (`--check-fresh`), and the cards via `python3 tools/board.py show T-099` and `show T-096`.
- Not exercised: the review screen (T-096 is not built); the Docker image (release lane).

```json
{"card": "T-099", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 3ecb8b1 (app/backend/api.py hook, app/backend/calibration_route.py, tests/unit/test_calibration_route.py) via git archive 3ecb8b1; live HEAD f5ddec8 checked: no change to the reviewed files; no app URL (FastAPI TestClient, real app, default demo mode); committed evals/reports/calibration.json (sample: 10 golden cases, fixture backend)",
 "exercised": [
  "git show --stat 3ecb8b1; git show 3ecb8b1 -- app/backend/api.py app/backend/calibration_route.py (full); git archive 3ecb8b1 into scratch t099-3ecb8b1",
  "git diff --stat 3ecb8b1 f5ddec8 -- app/backend/calibration_route.py tests/unit/test_calibration_route.py evals/reports/calibration.json -> empty",
  ".venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration -rs -> 32 passed, 2 skipped (test_eval_runner.py:636); tests/unit/test_calibration_route.py -> 23 passed",
  "artifacts/review-evidence/T-099-staff-engineer-probe-states.py: 22 scratch files through calibration_route.load; statuses ok/missing/invalid as listed in artifacts/review-evidence/T-099-staff-engineer-results.txt",
  "artifacts/review-evidence/T-099-staff-engineer-probe-consistent-edit.py: state total and its sentence changed together -> invalid on 3ecb8b1; ok with calibration_route.py:73 disabled",
  "artifacts/review-evidence/T-099-staff-engineer-probe-http.py: GET /api/calibration -> 200 status ok, keys calibration/message/status; POST, PUT, PATCH, DELETE -> 405; /api/health demo_mode True; body has no token, excerpt, Patient or summary",
  "artifacts/review-evidence/T-099-staff-engineer-mutants.py on the scratch copy: M1 sentence m/t check removed -> 1 failed; M2 state-total check removed -> 23 passed; M3 problems() ignored -> 11 failed; M4 all methods accepted -> 1 failed; restored -> 23 passed",
  "read evals/reports/calibration.json (committed): arithmetic checked (verified 83/84 = 9+54+20 and 9+55+20; needs_review 10/10 = 6+2+2); shasum -a 256 of app/llm/lexicon.yaml, app/llm/prompts/judge_faithfulness_v1.md, app/llm/prompts/extract_v1.md matches the hashes in the file",
  "read memory/contracts/api.md T-099 section; evals/run.py 6, 244, 1029-1047; app/backend/calibration_route.py in full; tests/unit/test_calibration_route.py test names and INVALID_CASES (lines 56-177); python3 tools/board.py show T-099 and show T-096"],
 "verdict": "changes",
 "scores": {"contract_shape": 4, "never_invents_numbers": 3, "demo_safety": 5, "validation_strength": 2, "test_pins_behaviour": 2},
 "findings": [
  {"severity": "major", "title": "The 'state totals equal type totals' validation rule is untested: removing it keeps all 23 route tests green",
   "evidence": "app/backend/calibration_route.py:73 (if bs[s][k] != sum(bt[t][s][k] ...)). Mutant with the check replaced by 'if False:': .venv/bin/python -m pytest -q tests/unit/test_calibration_route.py -> 23 passed (artifacts/review-evidence/T-099-staff-engineer-mutants.py, M2). tests/unit/test_calibration_route.py:106 (sum_mismatch_hand_edit) is rejected by the statement check, not the sum check. Consistent hand-edit (by_state.verified 82/84 with its sentence rewritten): ok on the mutant, invalid on 3ecb8b1 (artifacts/review-evidence/T-099-staff-engineer-results.txt).",
   "why_it_matters": "The card lists this rule as a validation step. It is the only check that stops a headline total being edited together with its sentence. No test fails when it is removed, so a regression would serve a wrong 'matched N/M times' line with no failing test. Rated major (tests fail when the code breaks).",
   "fix": "Add an INVALID_CASES entry whose sentences are rebuilt to match the changed state total, so only the sum check can reject it, and assert the problem names by_state.verified.matched.",
   "acceptance_test": "New case returns status invalid; with calibration_route.py:73 disabled the new test fails."},
  {"severity": "minor", "title": "The route validates less than the producer's own check (sentences are not rebuilt; hashes are not compared)",
   "evidence": "app/backend/calibration_route.py:37-41 (_statement_ok: only the substring 'N/M times' is required), :85-90 (statement checks). evals/run.py:1041 rebuilds the statements from the counts and requires equality; evals/run.py:1043-1045 compares prompt and lexicon hashes with disk. Probe hand_edit_sentence_claim (artifacts/review-evidence/T-099-staff-engineer-results.txt): verified-overall sentence changed to end 'so the letter is safe to send.' -> status ok.",
   "why_it_matters": "The UI shows the statements verbatim (memory/contracts/api.md T-099 section), so a hand-edited statement that keeps the numbers is shown as measured. The same file fails check_calibration, so the server accepts what the producer rejects. A calibration measured on older prompts is also served with no staleness signal. Latent, not live: the three hashes I checked match the files on disk.",
   "fix": "Move calibration_sentences into a module both evals/run.py and calibration_route.py import; require exact equality with the file's sentences. Add the hash comparison (or a freshness field in SERVED) so a stale file is flagged.",
   "acceptance_test": "A calibration whose sentence adds a claim is invalid; a file whose prompt hash differs from disk is invalid or served with a stale flag."},
  {"severity": "minor", "title": "by_case, case_count, small_sample and backend are served without cross-checks",
   "evidence": "app/backend/calibration_route.py:52-57 (backend, case_count, small_sample: type checks only), :78 (by_case: dict check only). Probes, all status ok (artifacts/review-evidence/T-099-staff-engineer-results.txt): hand_edit_case_count (case_count 500, sentences still say '10 golden cases'); hand_edit_by_case_only (by_case [1, 9] in a 55-item cell); by_case_matched_gt_total ([12, 9]); small_sample_flipped (false with 10 cases; threshold evals/run.py:244 CAL_SMALL_N = 30); hand_edit_backend_label (backend 'claude-sonnet-5-5' while the sentence says fixture backend).",
   "why_it_matters": "The served envelope carries numbers and labels that the statements and the sample size contradict, and the UI can show them. The card's 'never invented numbers' holds for the headline counts, but these fields are not checked against each other or against the sentences.",
   "fix": "Check that by_case sums equal each cell total and that matched <= total per case; require case_count == len(cases); require small_sample == (case_count < 30); require backend to match the backend named in the sentences.",
   "acceptance_test": "Each probe above returns status invalid."},
  {"severity": "minor", "title": "The card's test evidence does not reproduce",
   "evidence": "T-099 card AC 1 evidence (python3 tools/board.py show T-099): 'pytest -q tests/unit -k calibration gives 34 passed'. At 3ecb8b1: '32 passed, 2 skipped, 1570 deselected' (artifacts/review-evidence/T-099-staff-engineer-results.txt); 'SKIPPED [2] tests/unit/test_eval_runner.py:636: no git repository here (exported tree)'. tests/unit/test_calibration_route.py alone: 23 passed.",
   "why_it_matters": "The 'done' evidence is what the orchestrator checks. The numbers do not match what the command prints, and the two skipped tests are from another file. The feature is unaffected.",
   "fix": "Correct the card's evidence line to the printed counts, or select the route file explicitly (tests/unit/test_calibration_route.py).",
   "acceptance_test": "The cited command prints the cited numbers."}
 ],
 "whats_right": [
  "Envelope and empty states are right: GET returns 200 with {status, calibration, message}; missing and invalid files give calibration null with a constant message; no default numbers appear in any state (state probes, HTTP probe).",
  "Invalid files never echo their contents: an extra key with record-like text is not served, and the logs name only the rule (state probes 'extra_key'; server log lines in the results file).",
  "Read-only and demo-safe: POST, PUT, PATCH and DELETE return 405, no case token or record text is served, and the route is not gated by demo mode (HTTP probe; test_route_is_read_only)."],
 "questions_for_chris": [
  "Should the route refuse a calibration whose prompt or lexicon hashes differ from disk, as evals/run.py check_calibration does, or serve it with a stale flag for the review screen to show?"]}
```
----
---
id: "T-099"
title: "Serve calibration.json to the app (GET route, shape per T-096 note)"
milestone: "M3"
role: "backend"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T04:55:57Z"
updated_at: "2026-11-02T05:18:16Z"
claimed_by: "backend"
claimed_at: "2026-11-02T05:18:16Z"
rounds: 1
commits: ["3ecb8b1ca58b97c2d23cdd78a8a99a7bf292f8db"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-099-staff-engineer.md", "at": "2026-11-02T05:18:16Z"}
ac:
  - {"n": 1, "text": "GET /api/calibration (or a case field) serves evals/reports/calibration.json with source commit and sample size; missing file -> clear empty state, never invented numbers; unit test; T-096 consumes it", "done": true, "evidence": "tests/unit/test_calibration_route.py: pytest -q tests/unit -k calibration gives 34 passed (present, missing, invalid, read-only, demo mode)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:55:59Z backend: claimed
- 2026-11-02T04:57:17Z backend: Plan: new app/backend/calibration_route.py (load/validate/add_routes, GET /api/calibration, envelope status ok|missing|invalid, calibration null unless ok); one hook line in api.py; tests/unit/test_calibration_route.py written first; contract section in memory/contracts/api.md. Shared tree is dirty (other workers): commit via temp index built on HEAD, stage my api.py hunk only.
- 2026-11-02T04:59:56Z backend: AC 1 checked: tests/unit/test_calibration_route.py: pytest -q tests/unit -k calibration gives 34 passed (present, missing, invalid, read-only, demo mode)
- 2026-11-02T04:59:56Z backend: Commit BLOCKED by tools/check_stale_index.py: app/backend/api.py has another worker's uncommitted reorder (pdf_routes/billing lines) in the worktree, so the staged HEAD+hook blob matches neither HEAD nor worktree. Not bypassing the guard and not committing their hunk. Also: my contract section for GET /api/calibration already landed inside e511778 (T-098 commit, memory/contracts/api.md), so HEAD documents a route HEAD does not yet serve. Needs the owner of the api.py reorder to commit or drop it; then I commit calibration_route.py, tests/unit/test_calibration_route.py and the 2-line hook.
- 2026-11-02T05:00:16Z backend: moved in_progress -> in_review
- 2026-11-02T05:00:24Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T05:18:16Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-099-staff-engineer.md; round 1; findings:
    - [major] The 'state totals equal type totals' validation rule is untested: removing it keeps all 23 route tests green — fix: Add an INVALID_CASES entry whose sentences are rebuilt to match the changed state total, so only the sum check can reject it, and assert the problem names by_state.verified.matched.
    - [minor] The route validates less than the producer's own check (sentences are not rebuilt; hashes are not compared) — fix: Move calibration_sentences into a module both evals/run.py and calibration_route.py import; require exact equality with the file's sentences. Add the hash comparison (or a freshness field in SERVED) so a stale file is flagged.
    - [minor] by_case, case_count, small_sample and backend are served without cross-checks — fix: Check that by_case sums equal each cell total and that matched <= total per case; require case_count == len(cases); require small_sample == (case_count < 30); require backend to match the backend named in the sentences.
    - [minor] The card's test evidence does not reproduce — fix: Correct the card's evidence line to the printed counts, or select the route file explicitly (tests/unit/test_calibration_route.py).
- 2026-11-02T05:18:16Z backend: claimed

## Handoff
Changed: app/backend/calibration_route.py (new; load() gives ok|missing|invalid envelope; problems() checks the T-096 shape, count ranges, state totals = type totals, each statement quotes its own m/t; add_routes registers read-only GET /api/calibration). Hook: 2 lines in app/backend/api.py after the T-089 hook. Contract: memory/contracts/api.md (section and endpoint row; they landed earlier inside e511778, T-098, through the shared worktree). Tests: tests/unit/test_calibration_route.py. Verified: pytest -q tests/unit -k calibration = 34 passed; test_api, test_api_routes, test_boundaries, test_dismissal_patterns = 81 passed. Commit 3ecb8b1 (temp index on HEAD, 3 files, 302 insertions). Left: T-096 frontend consumes it. Surprised: the stale-index guard blocked the first attempt and was then relaxed to pass partial stages.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:18:42.518Z

**tool call — Bash**
````
{
 "command": "cat app/backend/calibration_route.py && echo ---- && cat tests/unit/test_calibration_route.py && echo ---- && git status --short | head -40 && git log --oneline -3 && git show --stat 3ecb8b1 | head -20",
 "description": "Read route, tests, and git state"
}
````

### User / tool · 2026-11-02T05:18:42.726Z

**tool result**
````
"""GET /api/calibration (T-099): the measured calibration the review screen quotes (T-090 writes it, T-096 shows it).

Read-only. Serves evals/reports/calibration.json, which evals.run writes from the golden cases: aggregate counts, the statements built
from those counts, the source commit and the backend. It holds no record text and no case token, so it is safe in demo mode and has no gate.

Three states, always HTTP 200 with the same envelope {"status", "calibration", "message"}:
- "ok": the file is the evals.calibration/1 shape, its totals add up, and every statement quotes its own counts. `calibration` is the
  served subset (SERVED below).
- "missing": no file. `calibration` is null. Nothing is invented.
- "invalid": the file cannot be read as a valid measurement (bad JSON, wrong schema, a hand-edited count, a statement that quotes other
  counts). `calibration` is null and the file's contents are never echoed; the reasons go to the log.
The UI hides the accuracy line when `calibration` is null (T-096). This module reads one fixed path and never writes.
"""
import json
import logging
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
REPORT = ROOT / "evals" / "reports" / "calibration.json"
SCHEMA = "evals.calibration/1"
TYPES = ("entry", "amount", "flag")
STATES = ("verified", "needs_review")
SERVED = ("schema", "backend", "case_count", "small_sample", "source_commit", "generated_at", "by_state", "by_type", "not_scored", "sentences")
MISSING = "No calibration has been measured yet, so no accuracy line is shown."
INVALID = "The calibration file is not a valid measurement, so no accuracy line is shown. Regenerate it with python -m evals.run."
log = logging.getLogger("zlayt.calibration")


def _count(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and x >= 0


def _cell_ok(c) -> bool:
    return isinstance(c, dict) and _count(c.get("matched")) and _count(c.get("total")) and c["matched"] <= c["total"]


def _statement_ok(text, cell) -> bool:
    """A statement is a non-empty string; when its cell has items it must quote that cell's own m/t. A hand-edited number fails here."""
    if not isinstance(text, str) or not text:
        return False
    return cell["total"] == 0 or f"{cell['matched']}/{cell['total']} times" in text


def problems(c) -> list:
    """Why `c` is not a valid calibration document. Empty list when it is. Checks the shape, the count ranges, that the state totals add up
    to the type totals, and that each statement quotes its own counts."""
    if not isinstance(c, dict):
        return ["not an object"]
    bad = []
    if c.get("schema") != SCHEMA:
        bad.append("schema")
    if not (isinstance(c.get("backend"), str) and c["backend"]):
        bad.append("backend")
    if not _count(c.get("case_count")):
        bad.append("case_count")
    if not isinstance(c.get("small_sample"), bool):
        bad.append("small_sample")
    if not (isinstance(c.get("source_commit"), str) and c["source_commit"]):
        bad.append("source_commit")
    if not isinstance(c.get("generated_at"), str):
        bad.append("generated_at")
    ns = c.get("not_scored")
    if not (isinstance(ns, dict) and all(_count(ns.get(k)) for k in TYPES + ("total",)) and ns["total"] == sum(ns[t] for t in TYPES)):
        bad.append("not_scored")
    bs, bt, se = c.get("by_state"), c.get("by_type"), c.get("sentences")
    if not (isinstance(bs, dict) and isinstance(bt, dict) and all(isinstance(bt.get(t), dict) for t in TYPES)):
        return bad + ["by_state or by_type"]
    for s in STATES:
        if not (_cell_ok(bs.get(s)) and isinstance(bs[s].get("cases"), list) and all(isinstance(x, str) for x in bs[s]["cases"])):
            bad.append(f"by_state.{s}")
            continue
        for k in ("matched", "total"):
            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):
                bad.append(f"by_state.{s}.{k} is not the sum over by_type (hand-edited count)")
    for t in TYPES:
        for s in STATES:
            cell = (bt.get(t) or {}).get(s)
            if not (_cell_ok(cell) and isinstance(cell.get("by_case"), dict)):
                bad.append(f"by_type.{t}.{s}")
    if bad:
        return bad
    if not (isinstance(se, dict) and isinstance(se.get("overall"), dict) and isinstance(se.get("by_type"), dict)):
        return bad + ["sentences"]
    for s in STATES:
        if not _statement_ok(se["overall"].get(s), bs[s]):
            bad.append(f"sentences.overall.{s} does not quote its counts")
    for t in TYPES:
        for s in STATES:
            if not _statement_ok((se["by_type"].get(t) or {}).get(s), bt[t][s]):
                bad.append(f"sentences.by_type.{t}.{s} does not quote its counts")
    return bad


def _envelope(status, calibration=None, message=None) -> dict:
    return {"status": status, "calibration": calibration, "message": message}


def load(path=REPORT) -> dict:
    """The envelope for the file at `path`: ok with the served subset, missing, or invalid. Read-only; never raises."""
    p = pathlib.Path(path)
    try:
        raw = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return _envelope("missing", message=MISSING)
    except (OSError, UnicodeDecodeError):
        log.warning("calibration file could not be read: %s", p.name)
        return _envelope("invalid", message=INVALID)
    try:
        doc = json.loads(raw)
    except ValueError:
        log.warning("calibration file is not JSON: %s", p.name)
        return _envelope("invalid", message=INVALID)
    bad = problems(doc)
    if bad:
        log.warning("calibration file rejected: %s", "; ".join(bad))
        return _envelope("invalid", message=INVALID)
    return _envelope("ok", {k: doc[k] for k in SERVED})


def add_routes(app, *, path=REPORT):
    @app.get("/api/calibration")
    def calibration():
        return load(path)
----
"""T-099: GET /api/calibration serves evals/reports/calibration.json read-only. Present, missing and invalid files are three distinct
states; a missing or invalid file gives calibration null and never an invented number. Aggregate counts only, so demo mode is fine.
Fixture backend, no key, SYNTHETIC counts."""
import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.backend import calibration_route as CR
from app.backend.api import create_app


def make():
    """A valid evals.calibration/1 document (one golden case), built the way evals/run.py builds it."""
    by_type = {
        "entry": {"verified": {"matched": 54, "total": 55, "by_case": {"sample": [54, 55]}},
                  "needs_review": {"matched": 2, "total": 2, "by_case": {"sample": [2, 2]}}},
        "amount": {"verified": {"matched": 9, "total": 9, "by_case": {"sample": [9, 9]}},
                   "needs_review": {"matched": 6, "total": 6, "by_case": {"sample": [6, 6]}}},
        "flag": {"verified": {"matched": 20, "total": 20, "by_case": {"sample": [20, 20]}},
                 "needs_review": {"matched": 2, "total": 2, "by_case": {"sample": [2, 2]}}},
    }
    by_state = {"verified": {"matched": 83, "total": 84, "cases": ["sample"]},
                "needs_review": {"matched": 10, "total": 10, "cases": ["sample"]}}
    return {
        "schema": "evals.calibration/1", "backend": "fixture", "case_count": 1, "small_sample": True,
        "source_commit": "b85fc1b56386aa0d37460186b5840eec0e578642", "generated_at": "2026-11-02T04:48:31Z",
        "by_state": by_state, "by_type": by_type, "not_scored": {"entry": 0, "amount": 0, "flag": 0, "total": 0},
        "sentences": {
            "overall": {"verified": "Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 1 golden cases, small sample).",
                        "needs_review": "Items marked needs review matched the record 10/10 times in testing on the fixture backend (recorded replies, 1 golden cases, small sample)."},
            "by_type": {t: {"verified": f"Verified {n} matched the record {by_type[t]['verified']['matched']}/{by_type[t]['verified']['total']} times in testing on the fixture backend (recorded replies, 1 golden cases, small sample).",
                            "needs_review": f"Needs-review {n} matched the record {by_type[t]['needs_review']['matched']}/{by_type[t]['needs_review']['total']} times in testing on the fixture backend (recorded replies, 1 golden cases, small sample)."}
                        for t, n in (("entry", "entries"), ("amount", "amounts"), ("flag", "flags"))}},
        # not served: the route keeps to the statement's shape
        "cases": ["sample"], "hashes": {"app/llm/lexicon.yaml": "00"}, "models": {"generator": "x"}, "match_rule": "...", "source": "evals.run",
        "source_tree": "3f014d4b5d84f8731ff464d4548e18dfce3fbd4f", "source_tree_clean": True,
    }


def write(tmp_path, doc, name="calibration.json"):
    p = tmp_path / name
    p.write_text(doc if isinstance(doc, str) else json.dumps(doc, indent=1, sort_keys=True) + "\n")
    return p


def bare_client(path):
    app = FastAPI()
    CR.add_routes(app, path=path)
    return TestClient(app)


# ---- present

def test_present_file_is_served_with_source_commit_backend_and_sample_size(tmp_path):
    out = CR.load(write(tmp_path, make()))
    assert out["status"] == "ok" and out["message"] is None
    c = out["calibration"]
    assert c["source_commit"] == "b85fc1b56386aa0d37460186b5840eec0e578642"
    assert c["backend"] == "fixture" and c["case_count"] == 1 and c["small_sample"] is True
    assert c["by_state"]["verified"] == {"matched": 83, "total": 84, "cases": ["sample"]}
    assert c["sentences"]["overall"]["verified"].startswith("Verified items matched the record 83/84 times")


def test_served_object_is_exactly_the_t096_shape_without_hashes_models_or_paths(tmp_path):
    c = CR.load(write(tmp_path, make()))["calibration"]
    assert set(c) == set(CR.SERVED)
    assert not {"hashes", "models", "cases", "source", "source_tree", "match_rule"} & set(c)


def test_route_serves_present_file_over_http(tmp_path):
    r = bare_client(write(tmp_path, make())).get("/api/calibration")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok" and body["calibration"]["source_commit"] == "b85fc1b56386aa0d37460186b5840eec0e578642"


def test_committed_report_is_valid_when_present():
    if not CR.REPORT.exists():
        pytest.skip("evals/reports/calibration.json is not generated in this checkout")
    out = CR.load()
    assert out["status"] == "ok", out


# ---- missing

def test_missing_file_is_an_empty_state_with_no_numbers(tmp_path):
    out = CR.load(tmp_path / "nope.json")
    assert out == {"status": "missing", "calibration": None, "message": CR.MISSING}


def test_route_missing_file_returns_200_empty_state_not_an_error(tmp_path):
    r = bare_client(tmp_path / "nope.json").get("/api/calibration")
    assert r.status_code == 200
    assert r.json() == {"status": "missing", "calibration": None, "message": CR.MISSING}


# ---- invalid

INVALID_CASES = {
    "not_json": "{not json",
    "not_utf8": None,      # written as raw bytes below
    "top_level_list": "[]",
    "wrong_schema": lambda d: d.update(schema="evals.calibration/2"),
    "sum_mismatch_hand_edit": lambda d: d["by_state"]["verified"].update(matched=90),
    "sentence_quotes_other_counts": lambda d: d["sentences"]["overall"].update(verified=d["sentences"]["overall"]["verified"].replace("83/84", "90/91")),
    "matched_above_total": lambda d: d["by_type"]["flag"]["verified"].update(matched=21),
    "negative_count": lambda d: d["by_type"]["amount"]["verified"].update(matched=-1, total=-1),
    "bool_counts": lambda d: d["by_state"]["needs_review"].update(matched=True),
    "missing_key": lambda d: d.pop("sentences"),
    "missing_source_commit": lambda d: d.update(source_commit=""),
    "statement_for_a_type_missing": lambda d: d["sentences"]["by_type"].pop("flag"),
}


@pytest.mark.parametrize("name", sorted(INVALID_CASES))
def test_invalid_file_is_an_empty_state_and_is_never_served(tmp_path, name):
    spec = INVALID_CASES[name]
    if name == "not_utf8":
        p = tmp_path / "calibration.json"
        p.write_bytes(b"\xff\xfe\x00bad")
    elif isinstance(spec, str):
        p = write(tmp_path, spec)
    else:
        d = make()
        spec(d)
        p = write(tmp_path, d)
    out = CR.load(p)
    assert out == {"status": "invalid", "calibration": None, "message": CR.INVALID}
    assert "83/90" not in json.dumps(out) and "90/91" not in json.dumps(out)


def test_invalid_route_response_does_not_echo_file_contents(tmp_path):
    d = make()
    d["by_state"]["verified"]["matched"] = 90
    r = bare_client(write(tmp_path, d)).get("/api/calibration")
    assert r.status_code == 200
    assert r.json() == {"status": "invalid", "calibration": None, "message": CR.INVALID}


def test_problems_is_empty_for_a_valid_document_and_lists_faults_otherwise():
    assert CR.problems(make()) == []
    d = make()
    d["by_state"]["verified"]["matched"] = 90
    assert CR.problems(d)


# ---- the route on the real app, demo mode, read-only

@pytest.fixture
def app_client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return TestClient(create_app(str(tmp_path / "cal.sqlite"), static_dir=str(tmp_path)))


def test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode(app_client):
    r = app_client.get("/api/calibration")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] in ("ok", "missing", "invalid")
    assert ("calibration" in body) and (body["calibration"] is None) == (body["status"] != "ok")


def test_route_carries_no_case_tokens_or_record_text(app_client):
    body = app_client.get("/api/calibration").json()
    text = json.dumps(body)
    assert "token" not in text and "raw_text" not in text and "records" not in text


def test_route_is_read_only(app_client):
    assert app_client.post("/api/calibration", json={}).status_code == 405
    assert app_client.put("/api/calibration", json={}).status_code == 405
    assert app_client.patch("/api/calibration", json={}).status_code == 405
    assert app_client.delete("/api/calibration").status_code == 405
----
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
MM app/backend/billing.py
D  app/backend/calibration_route.py
 M app/backend/flags.py
MM app/backend/grounding.py
 M app/backend/judges.py
 M app/backend/pipeline.py
 M app/llm/audited.py
 D app/llm/prompts/conflicts_v1.md
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
e63e564 docs: D-051 code checks bind accept for every item
a2d4b7c docs: D-050 non-English is never auto-verified (§7.4 after T-085 r3)
32f6c9d test(frontend): WordingFails route stub for the gate's code-check blocker (the edit route now refuses such wording, D-047); inline 422 cases (T-097 r2)
commit 3ecb8b1ca58b97c2d23cdd78a8a99a7bf292f8db
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:00:11 2026 -0600

    feat(backend): GET /api/calibration serves the measured calibration read-only (T-099)
    
    Serves evals/reports/calibration.json in the T-096 shape (counts, statements, source commit, backend, sample size).
    Envelope {status, calibration, message}: ok | missing | invalid. calibration is null unless ok; nothing is invented
    and the file contents are never echoed. Aggregate only, no case token, so it is demo-safe. GET only (other methods 405).
    Validation: shape, count ranges, state totals equal type totals, each statement quotes its own m/t.
    Contract section is already in memory/contracts/api.md (landed with e511778).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/api.py                   |   2 +
 app/backend/calibration_route.py     | 123 ++++++++++++++++++++++++
 tests/unit/test_calibration_route.py | 177 +++++++++++++++++++++++++++++++++++
 3 files changed, 302 insertions(+)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:19:00.165Z

**tool call — Bash**
````
{
 "command": "echo \"== HEAD has file:\" && git cat-file -e HEAD:app/backend/calibration_route.py && echo yes; echo \"== in index:\"; git ls-files -s app/backend/calibration_route.py; echo \"== ancestor:\"; git merge-base --is-ancestor 3ecb8b1 HEAD && echo yes; echo \"== calib sentences/run.py\"; grep -n \"calibration\\|CAL_SMALL_N\\|def _sentence\\|def check_calibration\" evals/run.py | head -60; echo \"== committed report\"; cat evals/reports/calibration.json | head -c 3000; echo; echo \"== hooks\"; ls tools/ | grep -i stale; sed -n 1,30p tools/check_stale_index.py 2>/dev/null | head -40",
 "description": "Inspect git index state, eval calibration code and report"
}
````

### User / tool · 2026-11-02T05:19:00.334Z

**tool result**
````
== HEAD has file:
yes
== in index:
== ancestor:
yes
== calib sentences/run.py
69:    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
244:CAL_SMALL_N = 30            # fewer cases (or items in a cell) than this is reported as a small sample, never rounded up to a rate
247:def score_calibration(exp, out, unscored=None):
287:def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
288:    """The statements the UI renders verbatim.  Built from the counts only, so check_calibration can rebuild them and catch a hand-edited sentence."""
294:        elif total < CAL_SMALL_N:
318:def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
319:    """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
326:                m, tot = r.get("calibration", {}).get(t, {}).get(s, [0, 0])
338:    small_cases = len(names) < CAL_SMALL_N
339:    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
342:    sentences = calibration_sentences(by_state, cells, backend, len(names), not_scored, small_cases)
343:    return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
350:            "cases": names, "case_count": len(names), "small_sample": small_cases or any(by_state[s]["total"] < CAL_SMALL_N for s in CAL_STATES),
473:                         "calibration": score_calibration(exp, out, unscored), "calibration_unscored": unscored}
917:    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
956:def render_calibration(c):
990:    L += render_calibration(r.get("calibration"))
1008:    if r.get("calibration"):                      # small file the app serves (T-090); regenerated by every full run
1009:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
1023:    bad = check_calibration(p.parent / "calibration.json", root)
1025:        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
1029:def check_calibration(path, root=ROOT):
1030:    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
1041:    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
== committed report
{
 "backend": "claude-cli",
 "by_state": {
  "needs_review": {
   "cases": [
    "case_01_date_formats",
    "case_03_rate_and_ocr",
    "case_07_prompt_injection",
    "sample"
   ],
   "matched": 9,
   "total": 9
  },
  "verified": {
   "cases": [
    "case_01_date_formats",
    "case_02_gap_boundaries",
    "case_03_rate_and_ocr",
    "case_04_duplicates_no_amounts",
    "case_05_provider_conflict",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "case_08_diagnosis_temptation",
    "case_09_nonvisit_hides_gap",
    "sample"
   ],
   "matched": 84,
   "total": 85
  }
 },
 "by_type": {
  "amount": {
   "needs_review": {
    "by_case": {
     "case_03_rate_and_ocr": [
      3,
      3
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "sample": [
      2,
      2
     ]
    },
    "matched": 6,
    "total": 6
   },
   "verified": {
    "by_case": {
     "case_01_date_formats": [
      1,
      1
     ],
     "case_03_rate_and_ocr": [
      2,
      2
     ],
     "case_05_provider_conflict": [
      1,
      1
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "case_08_diagnosis_temptation": [
      1,
      1
     ],
     "case_09_nonvisit_hides_gap": [
      1,
      1
     ],
     "sample": [
      2,
      2
     ]
    },
    "matched": 9,
    "total": 9
   }
  },
  "entry": {
   "needs_review": {
    "by_case": {
     "case_01_date_formats": [
      1,
      1
     ],
     "case_07_prompt_injection": [
      1,
      1
     ]
    },
    "matched": 2,
    "total": 2
   },
   "verified": {
    "by_case": {
     "case_01_date_formats": [
      7,
      7
     ],
     "case_02_gap_boundaries": [
      8,
      8
     ],
     "case_03_rate_and_ocr": [
      5,
      5
     ],
     "case_04_duplicates_no_amounts": [
      4,
      4
     ],
     "case_05_provider_conflict": [
      5,
      5
     ],
     "case_06_subtle_pre_existing": [
      4,
      5
     ],
     "case_07_prompt_injection": [
      3,
      3
     ],
     "case_08_diagnosis_temptation": [
      4,
      4
     ],
     "case_09_nonvisit_hides_gap": [
      5,
      5
     ],
     "sample": [
      9,
      9
     ]
    },
    "matched": 54,
    "total": 55
   }
  },
  "flag": {
   "needs_review": {
    "by_case": {
     "case_07_prompt_injection": [
      1,
      1
     ]
    },
    "matched": 1,
    "total": 1
   },
   "verified": {
    "by_case": {
     "case_02_gap_boundaries": [
      3,
      3
     ],
     "case_05_provider_conflict": [
      1,
      1
     ],
     "case_06_subtle_pre_existing": [
      4,
      4
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "case_08_diagnosis_temptation": [
      1,
      1
     ],
     "case_09_nonvisit_hides_gap": [
      1,
      1
     ],
     "sample": [
      10,
      10
     ]
    },
    "matched": 21,
    "total": 21
   }
  }
 },
 "case_count": 10,
 "cases": [
  "sample",
  "case_01_date_formats",
  "case_02_gap_boundaries",
  "case_
== hooks
check_stale_index.py
#!/usr/bin/env python3
"""Pre-commit guard against stale-index reverts (lessons: ec33bf0, 2fca530, 57a08ba).

Several workers share one checkout. A commit built from an index that predates other workers' commits
silently reverts their files. The signature: a staged path whose staged blob matches neither HEAD nor
the working tree (an old version), or a staged deletion of a file that still exists on disk.
Exit 1 with the offending paths; 0 otherwise. Works with GIT_INDEX_FILE temp indexes too.
"""
from __future__ import annotations
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args: str) -> str:
    r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"check_stale_index: BLOCKED (git {args[0]} failed: {r.stderr.strip()[:200]})")
        sys.exit(1)
    return r.stdout


def blob(spec: str) -> str | None:
    r = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "-q", "--verify", spec], capture_output=True, text=True)
    return r.stdout.strip() or None


def older_versions(path: str, depth: int = 200) -> set[str]:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:19:10.121Z

**tool call — Bash**
````
{
 "command": "sed -n 287,317p evals/run.py && sed -n 1029,1047p evals/run.py && python3 -c \"\nimport json;c=json.load(open('evals/reports/calibration.json'));print(c['sentences']['overall']);print(c['sentences']['by_type']['flag']);print(c['small_sample'], c['case_count'], len(c['cases']), c['backend'])\" && git status --short app/backend/calibration_route.py tests/unit/test_calibration_route.py evals/reports/calibration.json && .venv/bin/python -m pytest -q tests/unit -k calibration 2>&1 | tail -5",
 "description": "Read producer sentence builder and baseline test run"
}
````

### User / tool · 2026-11-02T05:19:14.399Z

**tool result**
````
def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
    """The statements the UI renders verbatim.  Built from the counts only, so check_calibration can rebuild them and catch a hand-edited sentence."""
    def caveat(total):
        """Names the backend and what was run, so the sentence cannot be read as live-model precision when it is a replay (T-090 r2)."""
        parts = (["recorded replies"] if backend == "fixture" else []) + [f"{case_count} golden cases"]
        if small_cases:
            parts.append("small sample")
        elif total < CAL_SMALL_N:
            parts.append(f"small sample: {total} items")
        return f" on the {backend} backend ({', '.join(parts)})"

    label = {"verified": "Verified items matched the record {m}/{t} times in testing",
             "needs_review": "Items marked needs review matched the record {m}/{t} times in testing"}
    sentences = {"overall": {}, "by_type": {}}
    for s in CAL_STATES:
        b = by_state[s]
        sentences["overall"][s] = ((label[s].format(m=b["matched"], t=b["total"]) + caveat(b["total"]) + ".") if b["total"]
                                   else f"No {s.replace('_', ' ')} items were seen in testing on the {backend} backend.")
        if b["total"] and not_scored["total"]:
            sentences["overall"][s] += f" Not scored: {not_scored['total']} produced items without a usable state."
    noun = {"entry": "entries", "amount": "amounts", "flag": "flags"}
    for t in CAL_TYPES:
        sentences["by_type"][t] = {}
        for s in CAL_STATES:
            c = cells[t][s]
            sentences["by_type"][t][s] = (f"{('Verified' if s == 'verified' else 'Needs-review')} {noun[t]} matched the record {c['matched']}/{c['total']} "
                                          f"times in testing{caveat(c['total'])}." if c["total"] else
                                          f"No {s.replace('_', ' ')} {noun[t]} were seen in testing on the {backend} backend.")
    return sentences


def check_calibration(path, root=ROOT):
    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
    files on disk (the counts were measured against other prompts). Empty list when the file is absent or fine."""
    p = pathlib.Path(path)
    if not p.exists():
        return []
    c = json.loads(p.read_text())
    bad = []
    for s in CAL_STATES:
        for k in ("matched", "total"):
            if c["by_state"][s][k] != sum(c["by_type"][t][s][k] for t in CAL_TYPES):
                bad.append(f"by_state.{s}.{k} is not the sum of by_type")
    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
        bad.append("sentences do not match the counts they are built from")
    old = c.get("hashes") or {}
    now = hashes(root)
    bad += [f"was measured against a different {k}" for k in sorted(set(old) | set(now)) if old and old.get(k) != now.get(k)]
    return bad

{'needs_review': 'Items marked needs review matched the record 9/9 times in testing on the claude-cli backend (10 golden cases, small sample).', 'verified': 'Verified items matched the record 84/85 times in testing on the claude-cli backend (10 golden cases, small sample).'}
{'needs_review': 'Needs-review flags matched the record 1/1 times in testing on the claude-cli backend (10 golden cases, small sample).', 'verified': 'Verified flags matched the record 21/21 times in testing on the claude-cli backend (10 golden cases, small sample).'}
True 10 10 claude-cli
D  app/backend/calibration_route.py
 M evals/reports/calibration.json
D  tests/unit/test_calibration_route.py
?? app/backend/calibration_route.py
?? tests/unit/test_calibration_route.py
tests/unit/test_eval_runner.py:683: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
2 failed, 32 passed, 1824 deselected in 3.76s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:19:49.920Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/calibration_route.py",
 "offset": 30,
 "limit": 15
}
````

### User / tool · 2026-11-02T05:19:49.974Z

**tool result**
````
30	    return isinstance(x, int) and not isinstance(x, bool) and x >= 0
31	
32	
33	def _cell_ok(c) -> bool:
34	    return isinstance(c, dict) and _count(c.get("matched")) and _count(c.get("total")) and c["matched"] <= c["total"]
35	
36	
37	def _statement_ok(text, cell) -> bool:
38	    """A statement is a non-empty string; when its cell has items it must quote that cell's own m/t. A hand-edited number fails here."""
39	    if not isinstance(text, str) or not text:
40	        return False
41	    return cell["total"] == 0 or f"{cell['matched']}/{cell['total']} times" in text
42	
43	
44	def problems(c) -> list:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:19:50.250Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py",
 "offset": 150,
 "limit": 12
}
````

### User / tool · 2026-11-02T05:19:50.259Z

**tool result**
````
150	
151	@pytest.fixture
152	def app_client(tmp_path, monkeypatch):
153	    monkeypatch.setenv("LLM_BACKEND", "fixture")
154	    monkeypatch.delenv("ENABLE_LIVE", raising=False)
155	    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
156	    return TestClient(create_app(str(tmp_path / "cal.sqlite"), static_dir=str(tmp_path)))
157	
158	
159	def test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode(app_client):
160	    r = app_client.get("/api/calibration")
161	    assert r.status_code == 200
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:19:50.999Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_eval_runner.py -k \"committed_calibration\" 2>&1 | grep -E \"Error|assert|where|FAILED\" | head -12; git diff --cached --name-only; echo \"--- HEAD api hook:\"; git show HEAD:app/backend/api.py | grep -n calibration",
 "description": "Read edit targets and check the two failing eval tests"
}
````

### User / tool · 2026-11-02T05:19:53.284Z

**tool result**
````
>       assert c["backend"] == "fixture" and re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
E       AssertionError: assert ('claude-cli' == 'fixture'
tests/unit/test_eval_runner.py:643: AssertionError
        assert (out / "calibration.json").exists(), r.stdout[-400:] + r.stderr[-800:]
>       assert fresh["by_state"] == c["by_state"] and fresh["by_type"] == c["by_type"] and fresh["sentences"] == c["sentences"]
E       AssertionError: assert ({'needs_revie... 'total': 84}} == {'needs_revie... 'total': 85}}
tests/unit/test_eval_runner.py:683: AssertionError
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
app/backend/api.py
app/backend/billing.py
app/backend/calibration_route.py
app/backend/grounding.py
tests/unit/_pdf_probe.py
tests/unit/test_billing.py
tests/unit/test_calibration_route.py
tests/unit/test_pdf_hidden_r2.py
tests/unit/test_pdf_ocr_limits.py
--- HEAD api hook:
514:    from app.backend import calibration_route
515:    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:06.653Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py",
 "old_string": "    \"statement_for_a_type_missing\": lambda d: d[\"sentences\"][\"by_type\"].pop(\"flag\"),\n}",
 "new_string": "    \"statement_for_a_type_missing\": lambda d: d[\"sentences\"][\"by_type\"].pop(\"flag\"),\n    # T-099 r2 minor: the served labels and sub-counts are checked against each other and against the sentences\n    \"case_count_not_the_case_list\": lambda d: d.update(case_count=500),\n    \"small_sample_flipped\": lambda d: d.update(small_sample=False),\n    \"by_case_sum_not_the_cell_total\": lambda d: d[\"by_type\"][\"entry\"][\"verified\"][\"by_case\"].update(sample=[50, 55]),\n    \"by_case_matched_above_its_total\": lambda d: d[\"by_type\"][\"entry\"][\"verified\"][\"by_case\"].update({\"sample\": [2, 1], \"other\": [52, 54]}),\n    \"backend_label_not_in_statements\": lambda d: d.update(backend=\"claude-sonnet-5-5\"),\n    \"statement_names_other_case_count\": lambda d: d.update(case_count=2, cases=[\"sample\", \"extra\"]),\n}"
}
````

### User / tool · 2026-11-02T05:20:06.710Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:08.015Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py",
 "old_string": "# ---- the route on the real app, demo mode, read-only",
 "new_string": "def test_state_total_check_rejects_a_consistent_hand_edit_of_a_state_total(tmp_path):\n    \"\"\"T-099 r2 major. The state total and its own sentence are edited together, so the statement check passes and only the rule\n    'state totals equal the sum over type totals' can reject it. Removing that rule must turn this test red.\"\"\"\n    d = make()\n    d[\"by_state\"][\"verified\"].update(matched=90, total=91)\n    d[\"sentences\"][\"overall\"][\"verified\"] = d[\"sentences\"][\"overall\"][\"verified\"].replace(\"83/84\", \"90/91\")\n    assert CR.load(write(tmp_path, d)) == {\"status\": \"invalid\", \"calibration\": None, \"message\": CR.INVALID}\n    assert any(p.startswith(\"by_state.verified.matched\") for p in CR.problems(d))\n\n\n# ---- the route on the real app, demo mode, read-only"
}
````

### User / tool · 2026-11-02T05:20:08.072Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:09.539Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_calibration_route.py 2>&1 | tail -15",
 "description": "Confirm new tests fail before the route fix"
}
````

### User / tool · 2026-11-02T05:20:10.359Z

**tool result**
````
E         Differing items:
E         {'status': 'ok'} != {'status': 'invalid'}
E         {'message': None} != {'message': 'The calibration file is not a valid measurement, so no accuracy line is shown. Regenerate it with python -m evals.run.'}
E         {'calibration': {'schema': 'evals.calibration/1', 'backend': 'fixture', 'case_count': 2, 'small_sample': True, ...}} != {'calibration': None}
E         Use -v to get more diff

tests/unit/test_calibration_route.py:137: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_calibration_route.py::test_invalid_file_is_an_empty_state_and_is_never_served[backend_label_not_in_statements]
FAILED tests/unit/test_calibration_route.py::test_invalid_file_is_an_empty_state_and_is_never_served[by_case_matched_above_its_total]
FAILED tests/unit/test_calibration_route.py::test_invalid_file_is_an_empty_state_and_is_never_served[by_case_sum_not_the_cell_total]
FAILED tests/unit/test_calibration_route.py::test_invalid_file_is_an_empty_state_and_is_never_served[case_count_not_the_case_list]
FAILED tests/unit/test_calibration_route.py::test_invalid_file_is_an_empty_state_and_is_never_served[small_sample_flipped]
FAILED tests/unit/test_calibration_route.py::test_invalid_file_is_an_empty_state_and_is_never_served[statement_names_other_case_count]
6 failed, 24 passed in 0.48s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:13.493Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/calibration_route.py",
 "old_string": "def _statement_ok(text, cell) -> bool:\n    \"\"\"A statement is a non-empty string; when its cell has items it must quote that cell's own m/t. A hand-edited number fails here.\"\"\"\n    if not isinstance(text, str) or not text:\n        return False\n    return cell[\"total\"] == 0 or f\"{cell['matched']}/{cell['total']} times\" in text",
 "new_string": "def _by_case_ok(cell) -> bool:\n    \"\"\"Each case's [matched, total] has matched <= total, and the cases add up to the cell's own counts.\"\"\"\n    bc = cell[\"by_case\"]\n    if not all(isinstance(v, list) and len(v) == 2 and _count(v[0]) and _count(v[1]) and v[0] <= v[1] for v in bc.values()):\n        return False\n    return sum(v[0] for v in bc.values()) == cell[\"matched\"] and sum(v[1] for v in bc.values()) == cell[\"total\"]\n\n\ndef _statement_ok(text, cell, backend, case_count) -> bool:\n    \"\"\"A statement is a non-empty string that names the backend. When its cell has items it must also quote that cell's own m/t and the\n    case count, as calibration_sentences in evals/run.py builds them. A hand-edited number or label fails here.\"\"\"\n    if not isinstance(text, str) or not text or f\" on the {backend} backend\" not in text:\n        return False\n    if cell[\"total\"] == 0:\n        return True\n    return f\"{cell['matched']}/{cell['total']} times\" in text and f\"{case_count} golden cases\" in text"
}
````

### User / tool · 2026-11-02T05:20:13.546Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/backend/calibration_route.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:14.104Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/calibration_route.py",
 "old_string": "STATES = (\"verified\", \"needs_review\")\n",
 "new_string": "STATES = (\"verified\", \"needs_review\")\nSMALL_N = 30  # evals/run.py CAL_SMALL_N: fewer cases, or items in a state, than this is a small sample\n"
}
````

### User / tool · 2026-11-02T05:20:14.164Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/backend/calibration_route.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:16.376Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/calibration_route.py",
 "old_string": "            if not (_cell_ok(cell) and isinstance(cell.get(\"by_case\"), dict)):\n                bad.append(f\"by_type.{t}.{s}\")\n    if bad:\n        return bad\n    if not (isinstance(se, dict) and isinstance(se.get(\"overall\"), dict) and isinstance(se.get(\"by_type\"), dict)):\n        return bad + [\"sentences\"]\n    for s in STATES:\n        if not _statement_ok(se[\"overall\"].get(s), bs[s]):\n            bad.append(f\"sentences.overall.{s} does not quote its counts\")\n    for t in TYPES:\n        for s in STATES:\n            if not _statement_ok((se[\"by_type\"].get(t) or {}).get(s), bt[t][s]):",
 "new_string": "            if not (_cell_ok(cell) and isinstance(cell.get(\"by_case\"), dict)):\n                bad.append(f\"by_type.{t}.{s}\")\n            elif not _by_case_ok(cell):\n                bad.append(f\"by_type.{t}.{s}.by_case does not add up to its cell\")\n    if bad:\n        return bad\n    cases = c.get(\"cases\")\n    if not (isinstance(cases, list) and all(isinstance(x, str) for x in cases) and len(cases) == c[\"case_count\"]):\n        bad.append(\"case_count is not the number of cases\")\n    if c[\"small_sample\"] != (c[\"case_count\"] < SMALL_N or any(bs[s][\"total\"] < SMALL_N for s in STATES)):\n        bad.append(\"small_sample is not the sample-size rule\")\n    if not (isinstance(se, dict) and isinstance(se.get(\"overall\"), dict) and isinstance(se.get(\"by_type\"), dict)):\n        return bad + [\"sentences\"]\n    for s in STATES:\n        if not _statement_ok(se[\"overall\"].get(s), bs[s], c[\"backend\"], c[\"case_count\"]):\n            bad.append(f\"sentences.overall.{s} does not quote its counts\")\n    for t in TYPES:\n        for s in STATES:\n            if not _statement_ok((se[\"by_type\"].get(t) or {}).get(s), bt[t][s], c[\"backend\"], c[\"case_count\"]):"
}
````

### User / tool · 2026-11-02T05:20:16.440Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/backend/calibration_route.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:19.005Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_calibration_route.py 2>&1 | tail -3 && .venv/bin/python -c \"\nimport json,sys\nsys.path.insert(0,'.')\nfrom app.backend import calibration_route as CR\nprint(CR.load()['status'], CR.problems(json.load(open('evals/reports/calibration.json'))))\nprint(CR.problems(json.load(open('evals/reports/calibration.json'))) == [])\n\"; git show HEAD:evals/reports/calibration.json > /dev/null && .venv/bin/python -c \"\nimport json,subprocess,sys\nsys.path.insert(0,'.')\nfrom app.backend import calibration_route as CR\nraw=subprocess.run(['git','show','HEAD:evals/reports/calibration.json'],capture_output=True,text=True).stdout\nprint('HEAD report problems:', CR.problems(json.loads(raw)))\"",
 "description": "Run route tests and check real calibration reports"
}
````

### User / tool · 2026-11-02T05:20:19.765Z

**tool result**
````
..............................                                           [100%]
30 passed in 0.33s
ok []
True
HEAD report problems: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:29.375Z

**tool call — Bash**
````
{
 "command": "set -e; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t099-mut\nrm -rf \"$S\" && mkdir -p \"$S/tests/unit\" \"$S/evals/reports\" && cd /Users/arsis/zlayt-pm-project && cp -R app \"$S/\" && cp evals/reports/calibration.json \"$S/evals/reports/\" && cp tests/unit/test_calibration_route.py \"$S/tests/unit/\" && (ls tests/conftest.py conftest.py pytest.ini 2>/dev/null | while read f; do cp \"$f\" \"$S/$(dirname $f)/\" ; done || true)\ncd \"$S\" && grep -n \"if bs\\[s\\]\\[k\\] != sum(\" app/backend/calibration_route.py\necho \"== mutant A: state-total check disabled, new tests\"\nsed -i '' 's/if bs\\[s\\]\\[k\\] != sum(/if False and bs[s][k] != sum(/' app/backend/calibration_route.py && grep -c \"if False and\" app/backend/calibration_route.py\n/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_calibration_route.py 2>&1 | tail -4 || true\necho \"== mutant A with the HEAD (pre-r2) test file\"\ngit -C /Users/arsis/zlayt-pm-project show 3ecb8b1:tests/unit/test_calibration_route.py > tests/unit/test_calibration_route.py\n/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_calibration_route.py 2>&1 | tail -2 || true\necho \"== restored, new tests\"\ncp /Users/arsis/zlayt-pm-project/app/backend/calibration_route.py app/backend/ && cp /Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py tests/unit/\n/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_calibration_route.py 2>&1 | tail -1\necho \"== mutant B: the three minor checks disabled (cases/small/by_case/backend), new tests\"\ncp /Users/arsis/zlayt-pm-project/app/backend/calibration_route.py app/backend/ && sed -i '' -e 's/if c\\[\"small_sample\"\\] != /if False and c[\"small_sample\"] != /' -e 's/if not (isinstance(cases, list)/if False and not (isinstance(cases, list)/' -e 's/elif not _by_case_ok(cell):/elif False:/' -e 's/return f\" on the {backend} backend\" not in text/return False/' app/backend/calibration_route.py; grep -c \"if False\" app/backend/calibration_route.py\n/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_calibration_route.py 2>&1 | tail -1 || true",
 "description": "Mutation-test the state-total check in a scratch copy"
}
````

### User / tool · 2026-11-02T05:20:32.176Z

**tool result**
````
85:            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):
== mutant A: state-total check disabled, new tests
1
tests/unit/test_calibration_route.py:162: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_calibration_route.py::test_state_total_check_rejects_a_consistent_hand_edit_of_a_state_total
1 failed, 29 passed in 0.40s
== mutant A with the HEAD (pre-r2) test file
.......................                                                  [100%]
23 passed in 0.35s
== restored, new tests
30 passed in 0.37s
== mutant B: the three minor checks disabled (cases/small/by_case/backend), new tests
3
3 failed, 27 passed in 0.39s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:42.433Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k calibration 2>&1 | tail -4; echo \"== mutant C: backend label check disabled\"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t099-mut; cp app/backend/calibration_route.py \"$S/app/backend/\" && cp tests/unit/test_calibration_route.py \"$S/tests/unit/\" && cd \"$S\" && sed -i '' 's/or f\" on the {backend} backend\" not in text/or False/' app/backend/calibration_route.py && grep -c \"or False\" app/backend/calibration_route.py; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_calibration_route.py 2>&1 | tail -1; cd /Users/arsis/zlayt-pm-project && git status --short -- app/backend/calibration_route.py tests/unit/test_calibration_route.py && git diff --cached --stat -- app/backend/calibration_route.py tests/unit/test_calibration_route.py",
 "description": "Run calibration tests and verify backend-label mutant"
}
````

### User / tool · 2026-11-02T05:20:47.117Z

**tool result**
````
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
2 failed, 39 passed, 1824 deselected in 3.57s
== mutant C: backend label check disabled
1
1 failed, 29 passed in 0.39s
D  app/backend/calibration_route.py
D  tests/unit/test_calibration_route.py
?? app/backend/calibration_route.py
?? tests/unit/test_calibration_route.py
 app/backend/calibration_route.py     | 123 ------------------------
 tests/unit/test_calibration_route.py | 177 -----------------------------------
 2 files changed, 300 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:48.862Z

**tool call — Bash**
````
{
 "command": "git add app/backend/calibration_route.py tests/unit/test_calibration_route.py && git diff --cached --name-only",
 "description": "Stage the two T-099 files only"
}
````

### User / tool · 2026-11-02T05:20:48.988Z

**tool result**
````
app/backend/api.py
app/backend/billing.py
app/backend/calibration_route.py
app/backend/grounding.py
memory/contracts/api.md
tests/unit/_pdf_probe.py
tests/unit/test_billing.py
tests/unit/test_calibration_route.py
tests/unit/test_pdf_hidden_r2.py
tests/unit/test_pdf_ocr_limits.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:50.740Z

**tool call — Bash**
````
{
 "command": "git commit -m \"fix(backend): calibration route rejects a hand-edited state total and checks the served labels (T-099 r2)\" -m \"- Test pins the state-total = type-total rule: a consistent hand-edit (state total and its sentence changed together) is invalid, and it fails when the rule is removed (mutant verified in a scratch copy: 1 failed with the new test, 23 passed with the old file).\n- Minors: case_count must equal the case list; small_sample must follow the CAL_SMALL_N=30 rule; each cell's by_case must add up to the cell and keep matched <= total per case; every statement must name the backend, and the case count when the cell has items.\n- Not done (r2 minor, needs a product call and evals/ owner): exact sentence equality with evals/run.py and the prompt/lexicon hash staleness check. Tracked in the T-099 handoff.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/backend/calibration_route.py tests/unit/test_calibration_route.py && git log --oneline -1 && git rev-parse HEAD",
 "description": "Commit the two T-099 files with explicit paths"
}
````

### User / tool · 2026-11-02T05:20:51.261Z

**tool result**
````
check_secrets: ok (2 file(s) scanned staged)
[main f345bc8] fix(backend): calibration route rejects a hand-edited state total and checks the served labels (T-099 r2)
 2 files changed, 42 insertions(+), 6 deletions(-)
f345bc8 fix(backend): calibration route rejects a hand-edited state total and checks the served labels (T-099 r2)
f345bc806488a21f551c44add1f21362b6ee8860
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:20:57.843Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B commit T-099 --sha f345bc806488a21f551c44add1f21362b6ee8860 --agent backend 2>&1 | tail -2; $B ac T-099 --check 1 --agent backend --evidence \"tests/unit/test_calibration_route.py: 30 passed (route file alone; includes state-total hand-edit test, mutant-verified); pytest -q tests/unit -k calibration: 39 passed, 2 failed in tests/unit/test_eval_runner.py (committed-calibration tests: the uncommitted worktree evals/reports/calibration.json is claude-cli, not fixture; not T-099)\" 2>&1 | tail -2; $B handoff T-099 --agent backend --text \"r2 fixes (commit f345bc8, app/backend/calibration_route.py + tests/unit/test_calibration_route.py only).\nChanged: major: test_state_total_check_rejects_a_consistent_hand_edit_of_a_state_total (state total+sentence edited together; only the sum rule rejects it). Minors fixed: case_count == len(cases); small_sample == CAL_SMALL_N rule; by_case adds up to its cell and matched<=total per case; statements name the backend and case count. Six new INVALID_CASES.\nVerified: tests/unit/test_calibration_route.py 30 passed. Mutant in scratch copy: state-total check disabled -> new test fails (1 failed); pre-r2 test file -> 23 passed (gap confirmed). Each minor check disabled -> its test fails. Real HEAD report and worktree report both pass the validator.\nLeft: F2 not done (needs a product call: refuse vs flag stale, and sentence-equality needs evals/run.py calibration_sentences moved to a shared module, which is qa's file). Card evidence corrected (F4): calibration filter gives 39 passed, 2 failed in test_eval_runner (other worker's uncommitted calibration.json, qa to regenerate or revert).\nSurprised: the shared index had staged deletions of both T-099 files; git add restored them. Other workers' staged files did not block the commit under -- paths.\" 2>&1 | tail -2; $B move T-099 in_review --agent backend 2>&1 | tail -2",
 "description": "Record commit, AC evidence, handoff and move to in_review"
}
````

### User / tool · 2026-11-02T05:20:58.152Z

**tool result**
````
T-099: commit f345bc806488a21f551c44add1f21362b6ee8860 recorded
AC 1 checked: tests/unit/test_calibration_route.py: 30 passed (route file alone; includes state-total hand-edit test, mutant-verified); pytest -q tests/unit -k calibration: 39 passed, 2 failed in tests/unit/test_eval_runner.py (committed-calibration tests: the uncommitted worktree evals/reports/calibration.json is claude-cli, not fixture; not T-099)
handoff written on T-099
T-099: in_progress -> in_review
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:21:00.317Z

T-099 r2 is committed as f345bc8 and in_review: the state-total test fails when the check is removed (confirmed in a scratch copy), and the cheap minors are fixed. F2 (exact sentence match and hash staleness) is not done because it needs a product call and a change to qa's evals module. The calibration filter gives 39 passed and 2 failed in test_eval_runner, caused by another worker's uncommitted `evals/reports/calibration.json`, not by this change.
