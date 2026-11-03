# Subagent: Backend: T-099 serve calibration (Backend: T-099 serve calibration)

Source: `agent-a8b2f8733dcb8bd3b.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:56:03.936Z

You own board card T-099 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Run `python3 tools/board.py show T-099` and read the field-shape note on T-096 (`python3 tools/board.py show T-096`).

Add a read-only GET route that serves evals/reports/calibration.json with its source commit, backend and sample size, in the shape noted on T-096. If the file is missing or invalid, return a clear empty state and never invented numbers. It's safe in demo mode, since it holds aggregate eval counts only. Put the route in a new small module with a minimal hook in api.py, and add the contract to memory/contracts/api.md. Add unit tests for the present, missing and invalid cases.

Run `.venv/bin/python -m pytest -q tests/unit -k calibration`. Commit from a fresh temp index built on HEAD (`GIT_INDEX_FILE=$(mktemp)`, `git read-tree HEAD`, add only your files), and check that `git diff --cached --stat` lists only them. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-099 in_review --agent backend`. Reply in 1 line.

### User / tool · 2026-11-02T04:56:03.942Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:05.870Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-099 && echo ---- && python3 tools/board.py show T-096",
 "description": "Show cards T-099 and T-096"
}
````

### User / tool · 2026-11-02T04:56:06.052Z

**tool result**
````
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
updated_at: "2026-11-02T04:55:59Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:55:59Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "GET /api/calibration (or a case field) serves evals/reports/calibration.json with source commit and sample size; missing file -> clear empty state, never invented numbers; unit test; T-096 consumes it", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:55:59Z backend: claimed

## Handoff (filled when moving to in_review)

----
---
id: "T-096"
title: "UI for suggestions and confidence: date-convention suggestion, dismissal suggestions, measured-precision line"
milestone: "M3"
role: "frontend"
status: "ready"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T04:30:07Z"
updated_at: "2026-11-02T04:48:59Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Dates-to-confirm row pre-selects the suggested convention with its reason and still requires one confirm (T-088); dismissal suggestion banner with Hide-similar action that the paralegal must click (T-089); 'Verified items matched the record N/M times in testing' line with small-sample note (T-090); e2e tests", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:30:16Z orchestrator: Starts once T-088/T-089 r2 and T-090 r2 pass (their API shapes may still change).
- 2026-11-02T04:30:16Z orchestrator: assigned: frontend
- 2026-11-02T04:48:59Z qa: From T-090 (qa): serve evals/reports/calibration.json read-only as a 'calibration' field (backend: e.g. in GET /api/meta; null when the file is absent). Shape: {schema:'evals.calibration/1', backend:'fixture'|..., case_count:int, small_sample:bool, source_commit:str, by_state:{verified|needs_review:{matched:int,total:int,cases:[str]}}, by_type:{entry|amount|flag:{verified|needs_review:{matched,total,by_case:{case:[m,t]}}}}, not_scored:{entry,amount,flag,total}, sentences:{overall:{verified:str,needs_review:str}, by_type:{entry|amount|flag:{verified:str,needs_review:str}}}}. Frontend: render sentences.overall.verified verbatim (it already names backend and basis, e.g. 'Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'); never compute or show a percentage. Backend AC needed: route returns those fields, null if file absent, no write path; test it. Frontend AC: line shown, hidden when null.

## Handoff (filled when moving to in_review)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:07.942Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/backend/project_backend_conventions.md 2>/dev/null; echo ----; ls app/backend 2>/dev/null; echo ----; ls evals evals/reports 2>/dev/null; echo ----; ls tests tests/unit 2>/dev/null; echo ----; cat memory/contracts/api.md 2>/dev/null | head -200; echo ----; git status --short | head -30; git log --oneline | head -5",
 "description": "Read backend memory, code layout, contract and git state"
}
````

### User / tool · 2026-11-02T04:56:08.108Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:09.589Z

**tool call — Bash**
````
{
 "command": "sed -n 1,200p .claude/agent-memory/backend/project_backend_conventions.md | tail -n +15; echo ----; ls app/backend; echo ----; ls evals evals/reports 2>&1; echo ----; ls tests tests/unit 2>&1 | head -60; echo ----; git status --short | head -30; git log --oneline | head -5",
 "description": "Read rest of backend memory and list code layout"
}
````

### User / tool · 2026-11-02T04:56:09.746Z

**tool result**
````
T-075 (determinism): the 0.0 live 3-run did not reproduce in 12 later runs; the real fragilities were judge prompts (J4 rejected valid flags; J3 undecided), model-order-dependent ids, and immediate retries. Judge prompts now v2 (flag category rules; J3 takes `category`). To re-record only judge fixtures after a judge prompt change, replay the recorded set and call claude-cli only on a miss at j3/j4 (never re-record whole cases: it would overwrite extract/narrative fixtures other workers depend on); then run `make_curated.py` (no flag), restore unchanged curated files byte-for-byte, `--check`. Run live pipeline checks in parallel processes (6 at once is fine, ~60 s).

T-085 (Spanish records): code half `language.py` + `spanish_text.py` (no app.llm import; test_boundaries bans LLM imports in dates.py, so keep Spanish code checks out of `spanish.py`, which wires the judge). Spanish records use steps `extract_es` / `judge_faithfulness_es` (own prompts, registered in audited.PROMPT_OF_STEP). To record only missing fixtures for new prompts: `ENABLE_LIVE=1 LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record --fill-missing evals/library/<packet>.txt` (replays recorded answers). Committing a shared file other workers also edit: filter `git diff HEAD -U0` hunks by keyword, `git apply --cached --unidiff-zero` into a temp GIT_INDEX_FILE built from `git read-tree HEAD`; `xargs git add` is blocked by git-guard, list paths explicitly.

## T-085 r2 lessons (language fail-safe)
- Commit with other workers' dirty hunks in the same file: build a temp index (`GIT_INDEX_FILE=$(mktemp)`, `read-tree HEAD`), `git add` whole files only when all hunks are mine; for mixed files (confidence/review/pipeline) hash-object the HEAD text + my edits and `update-index --cacheinfo`. Verify with `git diff --cached --stat`.
- language.detect: lang 'uncertain' = some non-English evidence, no confident answer; is_translated(lang) routes es+uncertain to the Spanish path; record_lang never returns English for text with foreign evidence. Do not put words identical to English (fracture, diagnostic, cervical, protrusion) in fr/pt/es lists.
- A one-record packet's preamble line becomes record 1 in ingest; test packets need 2+ records or no preamble.
- Spanish eval pairs: tests/unit/spanish_translation_pairs.jsonl; live judge eval opt-in SPANISH_JUDGE_EVAL=1 ENABLE_LIVE=1.
----
__init__.py
__pycache__
amounts.py
api.py
billing.py
case_extras.py
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
totals.py
trace.py
why.py
----
evals:
__init__.py
adversarial
golden
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
reports
run.py

evals/reports:
20261102T020824Z.md
20261102T020933Z.md
20261102T021029Z.md
20261102T021046Z.md
20261102T022701Z.md
20261102T022927Z.md
20261102T023039Z.md
20261102T023155Z.md
20261102T023203Z.md
20261102T023204Z.md
20261102T023208Z.md
20261102T023603Z.md
20261102T023911Z.md
20261102T023916Z.md
20261102T024348Z.md
20261102T024355Z.md
20261102T024653Z.md
20261102T024822Z.md
20261102T025055Z.md
20261102T025219Z.md
20261102T025526Z.md
20261102T025715Z.md
20261102T030405Z.md
20261102T031209Z.md
20261102T032024Z.md
20261102T032823Z.md
20261102T035750Z.md
20261102T040933Z.md
20261102T043845Z.md
calibration.json
controls-20261102T042306Z.json
controls-20261102T042306Z.md
controls-20261102T043911Z.json
controls-20261102T043911Z.md
controls-20261102T044933Z.json
controls-20261102T044933Z.md
controls-20261102T045207Z.json
controls-20261102T045207Z.md
determinism-diagnosis.md
latest.json
library-latest.md
m3-sensors.md
runs
----
tests:
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit

tests/unit:
__init__.py
__pycache__
_fakes.py
_golden.py
_pdf.py
_pdf_raw.py
spanish_translation_pairs.jsonl
test_amounts.py
test_api.py
test_api_routes.py
test_audited.py
test_backend_no_speaker_label.py
test_billing.py
test_boundaries.py
test_case_extras.py
test_confidence.py
test_conflict_candidates.py
test_conflicts.py
test_date_convention.py
test_date_unconfirmed.py
test_dates.py
test_db.py
test_dismissal_patterns.py
test_e2e_contract.py
test_eval_matching.py
test_eval_runner.py
test_eval_spec_check.py
test_export.py
test_export_edge.py
test_flag_templates.py
test_flags_injection.py
test_flags_pass.py
test_flags_sample.py
test_frontend_no_speaker_label.py
test_gaps.py
test_generator.py
test_grounding.py
test_grounding_may.py
test_ingest.py
test_injection.py
test_judge_guard.py
test_judges.py
test_library_denylist.py
test_manual_and_split.py
test_multicase.py
test_narrative.py
test_ocr_invariant.py
test_pdf_checks_api.py
test_pdf_hidden.py
test_pdf_ocr.py
test_pdf_ocr_limits.py
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
MM .claude/agent-memory/qa/MEMORY.md
D  .claude/agent-memory/qa/project_judge_controls.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/amounts.py
 M app/backend/api.py
MM app/backend/confidence.py
 M app/backend/flags.py
MM app/backend/generator.py
 M app/backend/judges.py
MM app/backend/language.py
 M app/backend/pdf_checks.py
 M app/backend/pdf_hidden.py
 M app/backend/pdf_ocr.py
 M app/backend/pdf_text.py
MM app/backend/pipeline.py
9c1af01 fix(backend): restore the T-085 r2 files that 57a08ba reverted by mistake (stale temp index); T-084 r3 change stays
57a08ba fix(backend): reclassify wording gate uses the classifier's rate verdict and the shared rate cues; class-only restore tested (T-084 r3)
1b1c711 fix(backend): language detection fails safe, French/Portuguese refused, CLI crash, 'no se descarta' keeps its meaning, Spanish cue words, Spanish eval pairs (T-085 r2)
172028c chore(evals): regenerate calibration.json from a clean worktree of b85fc1b (T-090 r3)
b85fc1b fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:11.528Z

**tool call — Bash**
````
{
 "command": "cat evals/reports/calibration.json | head -c 4000; echo; echo ----; grep -n \"calibration\" -r app/backend/*.py evals/*.py tools/*.py tests/unit/*.py 2>/dev/null | head -40",
 "description": "Inspect calibration.json and its references"
}
````

### User / tool · 2026-11-02T04:56:11.624Z

**tool result**
````
{
 "backend": "fixture",
 "by_state": {
  "needs_review": {
   "cases": [
    "case_01_date_formats",
    "case_03_rate_and_ocr",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "sample"
   ],
   "matched": 10,
   "total": 10
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
   "matched": 83,
   "total": 84
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
     "case_06_subtle_pre_existing": [
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
     "case_02_gap_boundaries": [
      3,
      3
     ],
     "case_05_provider_conflict": [
      1,
      1
     ],
     "case_06_subtle_pre_existing": [
      3,
      3
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
    "matched": 20,
    "total": 20
   }
  }
 },
 "case_count": 10,
 "cases": [
  "sample",
  "case_01_date_formats",
  "case_02_gap_boundaries",
  "case_03_rate_and_ocr",
  "case_04_duplicates_no_amounts",
  "case_05_provider_conflict",
  "case_06_subtle_pre_existing",
  "case_07_prompt_injection",
  "case_08_diagnosis_temptation",
  "case_09_nonvisit_hides_gap"
 ],
 "generated_at": "2026-11-02T04:48:31Z",
 "hashes": {
  "app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263",
  "app/llm/prompts/conflicts_v1.md": "16c18d05e68a5cfa0fa6496497b377dfbcda3c19fbf04dfaa9c9cf36139932ca",
  "app/llm/prompts/extract_es_v1.md": "985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb",
  "app/llm/prompts/extract_v1.md": "11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2",
  "app/llm/prompts/flags_v1.md": "d5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725",
  "app/llm/prompts/judge_amount_class_v1.md": "e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8",
  "app/llm
----
evals/run.py:69:    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
evals/run.py:247:def score_calibration(exp, out, unscored=None):
evals/run.py:287:def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
evals/run.py:288:    """The statements the UI renders verbatim.  Built from the counts only, so check_calibration can rebuild them and catch a hand-edited sentence."""
evals/run.py:318:def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
evals/run.py:319:    """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
evals/run.py:326:                m, tot = r.get("calibration", {}).get(t, {}).get(s, [0, 0])
evals/run.py:339:    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
evals/run.py:342:    sentences = calibration_sentences(by_state, cells, backend, len(names), not_scored, small_cases)
evals/run.py:343:    return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
evals/run.py:473:                         "calibration": score_calibration(exp, out, unscored), "calibration_unscored": unscored}
evals/run.py:917:    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
evals/run.py:956:def render_calibration(c):
evals/run.py:990:    L += render_calibration(r.get("calibration"))
evals/run.py:1008:    if r.get("calibration"):                      # small file the app serves (T-090); regenerated by every full run
evals/run.py:1009:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
evals/run.py:1023:    bad = check_calibration(p.parent / "calibration.json", root)
evals/run.py:1025:        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
evals/run.py:1029:def check_calibration(path, root=ROOT):
evals/run.py:1030:    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
evals/run.py:1041:    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
tests/unit/test_eval_runner.py:441:    return R.score_calibration(exp, out)
tests/unit/test_eval_runner.py:444:def test_score_calibration_counts_matched_over_seen_per_state_and_type():
tests/unit/test_eval_runner.py:459:def test_score_calibration_ignores_rejected_items_and_items_without_a_state():
tests/unit/test_eval_runner.py:469:def test_flag_calibration_follows_flag_precision():
tests/unit/test_eval_runner.py:480:def test_build_calibration_pools_counts_names_cases_and_flags_small_samples():
tests/unit/test_eval_runner.py:481:    res = {"a": {"calibration": {"entry": {"verified": [3, 4], "needs_review": [1, 2]}, "amount": {"verified": [2, 2], "needs_review": [0, 0]},
tests/unit/test_eval_runner.py:483:           "b": {"calibration": {"entry": {"verified": [1, 1], "needs_review": [0, 0]}, "amount": {"verified": [0, 0], "needs_review": [0, 1]},
tests/unit/test_eval_runner.py:485:    c = R.build_calibration(res, "fixture", {"generator": "x"}, "T")
tests/unit/test_eval_runner.py:495:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
tests/unit/test_eval_runner.py:496:    res = {"a": {"calibration": {t: {"verified": [1, 2], "needs_review": [1, 1]} for t in R.CAL_TYPES}}}
tests/unit/test_eval_runner.py:497:    c = R.build_calibration(res, "fixture")
tests/unit/test_eval_runner.py:517:    row = {"calibration": {"entry": {"verified": [40, 40], "needs_review": [0, 0]}, "amount": {"verified": [0, 0], "needs_review": [0, 0]},
tests/unit/test_eval_runner.py:519:    few = {"calibration": {**row["calibration"], "entry": {"verified": [0, 0], "needs_review": [1, 2]}}}
tests/unit/test_eval_runner.py:520:    c = R.build_calibration({**{f"c{i}": row for i in range(29)}, "few": few}, "claude-cli")
tests/unit/test_eval_runner.py:526:    row = {"calibration": {"entry": {"verified": [40, 40], "needs_review": [0, 0]}, "amount": {"verified": [0, 0], "needs_review": [0, 0]},
tests/unit/test_eval_runner.py:529:    at29 = R.build_calibration({f"c{i}": row for i in range(29)}, "claude-cli")
tests/unit/test_eval_runner.py:530:    at30 = R.build_calibration({f"c{i}": row for i in range(30)}, "claude-cli")
tests/unit/test_eval_runner.py:538:    row = {"calibration": {t: {"verified": [1, 2], "needs_review": [1, 1]} for t in R.CAL_TYPES}}
tests/unit/test_eval_runner.py:539:    c = R.build_calibration({"a": row}, backend)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:13.424Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json;c=json.load(open('evals/reports/calibration.json'));print({k:(v if not isinstance(v,(dict,list)) else type(v).__name__) for k,v in c.items()}); print(c.get('source')); print(c.get('sentences')); print(c.get('not_scored'))\"; sed -n 318,350p evals/run.py; sed -n 1029,1060p evals/run.py",
 "description": "Inspect calibration keys, sentences and validator"
}
````

### User / tool · 2026-11-02T04:56:13.554Z

**tool result**
````
{'backend': 'fixture', 'by_state': 'dict', 'by_type': 'dict', 'case_count': 10, 'cases': 'list', 'generated_at': '2026-11-02T04:48:31Z', 'hashes': 'dict', 'match_rule': 'entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.', 'models': 'dict', 'not_scored': 'dict', 'schema': 'evals.calibration/1', 'sentences': 'dict', 'small_sample': True, 'source': 'evals.run over the golden cases; measured counts only (D-042, scope cut 10)', 'source_commit': 'b85fc1b56386aa0d37460186b5840eec0e578642', 'source_tree': '3f014d4b5d84f8731ff464d4548e18dfce3fbd4f', 'source_tree_clean': True}
evals.run over the golden cases; measured counts only (D-042, scope cut 10)
{'by_type': {'amount': {'needs_review': 'Needs-review amounts matched the record 6/6 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).', 'verified': 'Verified amounts matched the record 9/9 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'}, 'entry': {'needs_review': 'Needs-review entries matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).', 'verified': 'Verified entries matched the record 54/55 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'}, 'flag': {'needs_review': 'Needs-review flags matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).', 'verified': 'Verified flags matched the record 20/20 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'}}, 'overall': {'needs_review': 'Items marked needs review matched the record 10/10 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).', 'verified': 'Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'}}
{'amount': 0, 'entry': 0, 'flag': 0, 'total': 0}
def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
    """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
    Statements are generated here so the UI never composes a number of its own (and never shows a bare percentage)."""
    names = list(results)
    cells = {t: {s: {"matched": 0, "total": 0, "by_case": {}} for s in CAL_STATES} for t in CAL_TYPES}
    for n, r in results.items():
        for t in CAL_TYPES:
            for s in CAL_STATES:
                m, tot = r.get("calibration", {}).get(t, {}).get(s, [0, 0])
                c = cells[t][s]
                c["matched"] += m
                c["total"] += tot
                if tot:
                    c["by_case"][n] = [m, tot]
    by_state = {}
    for s in CAL_STATES:
        m = sum(cells[t][s]["matched"] for t in CAL_TYPES)
        tot = sum(cells[t][s]["total"] for t in CAL_TYPES)
        cs = sorted({n for t in CAL_TYPES for n in cells[t][s]["by_case"]})
        by_state[s] = {"matched": m, "total": tot, "cases": cs}
    small_cases = len(names) < CAL_SMALL_N
    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
    not_scored["total"] = sum(not_scored[t] for t in CAL_TYPES)

    sentences = calibration_sentences(by_state, cells, backend, len(names), not_scored, small_cases)
    return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
            "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "source_tree": (source or {}).get("tree"), "hashes": hashes_ or {},
            "match_rule": "entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; "
                          "flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; "
                          "produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.",
            "not_scored": not_scored,
            "cases": names, "case_count": len(names), "small_sample": small_cases or any(by_state[s]["total"] < CAL_SMALL_N for s in CAL_STATES),
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


def load_pipeline():
    from app import pipeline
    return pipeline


class CuratedFixtures(Exception):
    pass


def refuse_curated(env=None):
    """D-029: the ship bar is measured on live runs and recorded fixtures only. Curated (hand-checked) responses reproduce the golden
    answers by construction, so scoring them would be circular. Refuse to compute ship-bar metrics when the curated set is selected."""
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:24.130Z

**tool call — Bash**
````
{
 "command": "wc -l app/backend/api.py && grep -n \"demo\\|include_router\\|APIRouter\\|^from\\|^import\\|@app\\.\\(get\\|post\\)\\|def create_app\\|app = \" app/backend/api.py | head -120; echo ----; sed -n 1,60p app/backend/pdf_routes.py",
 "description": "Survey api.py routes, demo mode and a sample router module"
}
````

### User / tool · 2026-11-02T04:56:24.230Z

**tool result**
````
     586 app/backend/api.py
1:"""FastAPI routes (memory/contracts/api.md). Thin: parsing, the demo gate, error format; logic lives in ingest/store/review/present/export.
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
23:from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
24:from app.db import db as DB
41:from app.backend import pdf_checks as _pdf_checks      # noqa: E402  (T-086/T-087)
93:def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipeline=None) -> FastAPI:
96:    app = FastAPI(title="Zlayt treatment timeline", docs_url=None, redoc_url=None, openapi_url=None)
114:        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says
119:    def demo_mode():
212:    @app.get("/api/health")
214:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(),
218:    @app.get("/api/cases")
220:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
228:    @app.get("/api/library")
234:    @app.post("/api/cases", status_code=201)
250:    @app.post("/api/cases/pdf", status_code=201)
254:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
255:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
285:        if demo_mode() and digest(text) not in allowed_hashes():
286:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
293:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
306:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
314:    @app.get("/api/cases/{token}")
319:            return present.case_view(c, token, backend=backend(), models=models(), demo_mode=demo_mode())
347:    @app.post("/api/cases/{token}/run", status_code=202)
355:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
356:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
357:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
370:    @app.post("/api/cases/{token}/rejudge")
372:        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
373:        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
380:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
381:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
382:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
392:    @app.get("/api/cases/{token}/status")
411:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
423:    @app.post("/api/cases/{token}/records/{rid}/entry", status_code=201)
434:    @app.post("/api/cases/{token}/items/{item_id}/not_duplicate")
447:    @app.get("/api/cases/{token}/narrative")
456:    @app.post("/api/cases/{token}/narrative")
469:    @app.post("/api/cases/{token}/narrative/review")
484:    @app.get("/api/cases/{token}/items/{item_id}")
496:    @app.post("/api/cases/{token}/items/{item_id}/review")
515:    @app.get("/api/cases/{token}/export")
536:                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"]}),
542:    @app.get("/api/cases/{token}/items/{item_id}/trace")
555:    @app.get("/api/cases/{token}/trace")
564:    @app.get("/api/cases/{token}/judges")
573:    @app.get("/api/cases/{token}/audit")
----
"""GET /api/cases/{token}/pages/{n}/image (T-086): the scanned page beside its OCR text. The PNG was rendered at upload from the
user's own PDF and is stored with the case (config.page_images, base64), so it goes away with the case (DELETE or retention purge).
`add_routes(app, conn=..., get_case=..., ApiError=...)`, the same shape as the other route modules."""
import base64
import binascii

from fastapi import Response


def add_routes(app, *, conn, get_case, ApiError):
    @app.get("/api/cases/{token}/pages/{n}/image")
    def page_image(token: str, n: int):
        c = conn()
        try:
            case = get_case(c, token)
        finally:
            c.close()
        b64 = ((case.get("config") or {}).get("page_images") or {}).get(str(n))
        if not b64:
            raise ApiError(404, "not_found", "No page image for that page.")
        try:
            png = base64.b64decode(b64, validate=True)
        except (binascii.Error, ValueError):
            raise ApiError(404, "not_found", "No page image for that page.") from None
        return Response(content=png, media_type="image/png", headers={"Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"})
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:25.623Z

**tool call — Bash**
````
{
 "command": "sed -n 22,140p app/backend/api.py; echo ----; sed -n 205,235p app/backend/api.py; echo ----; grep -n \"add_routes\\|_pdf_checks\\|pdf_routes\\|export_routes\" app/backend/api.py",
 "description": "Read api.py setup, demo gate and route module hooks"
}
````

### User / tool · 2026-11-02T04:56:25.734Z

**tool result**
````
from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
from app.db import db as DB

MAX_BODY_BYTES = 512 * 1024      # cheap rejection before the 60,000-character rule: UTF-8 worst case plus JSON overhead
# index.html has one inline onclick (dialog Close); allowed by hash until the frontend moves it to a listener.
CSP = ("default-src 'none'; script-src 'self'; script-src-attr 'unsafe-hashes' 'sha256-%s'; style-src 'self'; img-src 'self' data:; "
       "connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'") % "95nblrfVsK8W4muMQZ2m4mrNYEqpgFiSJOd2xYMkbfU="
ROOT = pathlib.Path(__file__).resolve().parents[2]
GOLDEN = ROOT / "evals" / "golden"
LIBRARY = ROOT / "evals" / "library"
VERSION = "0.1.0"
BANNER = "Synthetic data only — never paste real records"
AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]
_ERR_STATUS = {"bad_request": 400, "input_too_large": 413, "unsupported_language": 400}
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
        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))

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
----
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
            return {"cases": present.case_list(c)}
        finally:
            c.close()

    @app.get("/api/library")
    def library():
        if not local_mode():
            raise ApiError(404, "not_found", "Not found.")
        return {"cases": [{k: v for k, v in x.items() if k != "path"} for x in library_cases()]}

    @app.post("/api/cases", status_code=201)
    async def create_case(request: Request):
----
41:from app.backend import pdf_checks as _pdf_checks      # noqa: E402  (T-086/T-087)
42:_PDF_MESSAGES.update(_pdf_checks.MESSAGES)
270:            got = await asyncio.wait_for(run_in_threadpool(pdf_text.extract, data, **opts), _pdf_checks.OCR_TIMEOUT_S if opts.get("ocr") else pdf_text.EXTRACT_TIMEOUT_S)
506:    case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
508:    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
509:    from app.backend import pdf_routes
510:    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
512:    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
513:    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
517:        from app.backend import export_routes as XR
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:27.832Z

**tool call — Bash**
````
{
 "command": "sed -n 500,530p app/backend/api.py; echo ----; grep -n \"^## \\|^### \" memory/contracts/api.md | head -80; echo ----; wc -l memory/contracts/api.md; echo ----; grep -ln \"TestClient\" tests/unit/*.py | head; echo ----; sed -n 1,40p tests/unit/test_pdf_checks_api.py",
 "description": "Read route hooks, API contract headings, and a test client example"
}
````

### User / tool · 2026-11-02T04:56:27.938Z

**tool result**
````
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

    @app.get("/api/cases/{token}/export")
    def export(token: str):
        from app.backend import export_routes as XR
        c = conn()
        try:
            get_case(c, token)
            case = store.export_case(c, token)
            try:
                ex = XR.export_payload(token, case)
            except export_mod.ExportBlocked as e:                     # D-044/D-045: the gate lists the same blockers; no override
                raise ApiError(422, e.code, XR.blocked_message(e), {"blockers": e.items}) from None
            calls = DB.list_llm_calls(c, token)
            ok = ("accepted", "edited")
            tv = present.totals_view(c, token)
            ex["items"]["flags"] = [{"id": f["id"], "edited": f["review_status"] == "edited"} for f in case["flags"] if f["review_status"] in ok]
            ex["totals"] = {"charges_cents": tv["accepted"]["cents"], "charges_count": tv["accepted"]["count"]}
----
5:## Conventions
14:## Endpoint index
44:## GET /api/health
57:## POST /api/cases
77:## POST /api/cases/pdf (D-031)
81:### PDF hidden text and local OCR (T-087, T-086; D-042)
103:## POST /api/cases/{token}/review/batch (D-031)
106:## /api/cases/{token}/export_config (D-031)
109:## POST /api/cases/{token}/run
116:## GET /api/cases/{token}/status
126:## GET /api/cases/{token}
244:## POST /api/cases/{token}/records/{rid}/confirm_date
259:## Date-convention suggestion (T-088, D-042): `dates_to_confirm[].suggestion`
271:## Dismissal-pattern suggestions (T-089, D-042): `GET /api/cases/{token}/dismissal_suggestions`
283:### POST /api/cases/{token}/dismissal_suggestions/apply
286:## GET /api/cases/{token}/items/{item_id}  — "Why?"
304:## POST /api/cases/{token}/items/{item_id}/review
338:## POST /api/cases/{token}/items/{item_id}/reclassify  (D-042, T-084)
359:## GET /api/cases/{token}/export
510:## GET /api/cases/{token}/audit
530:## Check traces (D-042): per-item stepper, case stepper, judge summary
537:### Step (shared by all three endpoints)
555:### GET /api/cases/{token}/items/{item_id}/trace
587:### GET /api/cases/{token}/trace
619:### GET /api/cases/{token}/judges
635:## POST /api/cases/{token}/rejudge  (D-044)
645:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
651:## GET /api/cases/{token}/billing  (T-083, D-042)
693:## Spanish-language records (T-085, D-042)
708:## DELETE /api/cases/{token}
713:## Appendix: reason codes (closed list; one fixed "why" template each in `app/backend/why.py`)
----
     739 memory/contracts/api.md
----
tests/unit/test_api.py
tests/unit/test_api_routes.py
tests/unit/test_case_extras.py
tests/unit/test_date_unconfirmed.py
tests/unit/test_billing.py
tests/unit/test_date_convention.py
tests/unit/test_dismissal_patterns.py
tests/unit/test_manual_and_split.py
tests/unit/test_pdf_checks_api.py
tests/unit/test_pdf_upload.py
----
"""T-086/T-087 over HTTP and through the pipeline: hidden text is kept out of the case until confirmed, OCR is opt-in and local, the page
image is served beside the OCR text, and every item on an OCR page is needs_review. SYNTHETIC text only."""
import base64
import shutil

import pytest
from fastapi.testclient import TestClient

from app.backend import pipeline as PL
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script
from tests.unit._pdf_raw import build, scanned_copy, text_page
from tests.unit.test_pdf_hidden import HIDDEN, VISIBLE, pdf_with
from tests.unit.test_pdf_ocr import LINES, scan_pdf

pytest.importorskip("pypdfium2")
PDF = {"content-type": "application/pdf"}
needs_tesseract = pytest.mark.skipif(not shutil.which("tesseract"), reason="tesseract is not installed")


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    monkeypatch.setenv("ENABLE_LIVE", "1")
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    db = str(tmp_path / "pc.sqlite")
    return db, TestClient(create_app(db, static_dir=str(tmp_path)))


def test_upload_excludes_hidden_text_reports_it_and_shows_it_again_on_the_case(client):
    _, c = client
    r = c.post("/api/cases/pdf", content=pdf_with("white", "offpage"), headers=PDF)
    assert r.status_code == 201, r.text
    b = r.json()
    assert "PLANTED" not in " ".join(x["text"] for x in b["records"])
    ht = b["pdf_checks"]["hidden_text"]
    assert ht["pages"][0]["page"] == 1 and ht["pages"][0]["count"] == 2 and ht["pages"][0]["excluded"]
    view = c.get(f"/api/cases/{b['token']}").json()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:29.563Z

**tool call — Bash**
````
{
 "command": "sed -n 1,44p memory/contracts/api.md; echo ----; sed -n 645,652p memory/contracts/api.md; echo ----; sed -n 1,40p app/backend/dismissal_patterns.py | head -60; echo ----; grep -n \"def test_\" tests/unit/test_dismissal_patterns.py | head -5; sed -n 1,25p tests/unit/test_dismissal_patterns.py",
 "description": "Read contract header, endpoint index, and a route module plus its test"
}
````

### User / tool · 2026-11-02T04:56:29.666Z

**tool result**
````
# API contract — DRAFT — backend owns from M2

Status: drafted by the architect (T-014, round 2). From M2 the backend worker is the sole writer; changes after that go through a card. Frontend may start against the examples below. They use the Appendix A sample case (Jordan Rivera, SYNTHETIC) as stored in `evals/golden/sample.txt`; **every `start`/`end` is an absolute character offset into the case's raw text, and `raw_text[start:end]` equals the quoted string** (verified by a script run for the T-014 handoff). Design rationale: `memory/DECISIONS.md` ADR-002, 005, 006, 007, 009 to 017. Orchestrator decisions: `memory/ORCHESTRATOR_DECISIONS.md` (D-001..D-024). Requirements: `spec/REQUIREMENTS.md`; the conflicts it lists in §8 are resolved in ADR-017.

## Conventions
- Base path `/api`; JSON in and out; UTF-8; ISO dates `YYYY-MM-DD`; timestamps ISO-8601 UTC. Money is integer cents in `value_cents` plus the verbatim `text`.
- `{token}` is the case id: a random 128-bit URL-safe string. It is the only credential. **There is no case-list endpoint.** An unknown token is `404 not_found`.
- Item ids: entries `e…`, amounts `a…`, flags `f…`, records `r…`. Gap flags use `f_gap_<recA>_<recB>`. Opaque to the frontend.
- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409), `item_rejected` (409), `unsupported_language` (400, T-085: see Spanish-language records), `invalid_edit` (422, every structurally invalid edit), `date_invalid` (422, `confirm_date` with a non-candidate date), `llm_unavailable` (503).
- Every item has `state` (system: `verified` | `needs_review` | `rejected`), `reasons[]` (codes), `why` (one template sentence), `review_status` (human: `pending` | `accepted` | `edited` | `dismissed`), and `ladder` (D.4).
- `warnings[]` appears on case, ingest, review and export responses. Shape: `{"code": "...", "message": "...", "item_id": null}`.
- Untrusted strings (record text, excerpts, summaries) are plain text; clients must insert them with `textContent`.

## Endpoint index
| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | backend, demo mode, models, limits, banner text |
| POST | `/api/cases` | create from pasted text, a `.txt` file's contents, or the sample; ingest runs synchronously (code only) |
| GET | `/api/cases/{token}` | the whole case for the review screen |
| DELETE | `/api/cases/{token}` | delete the case, its items, calls and events |
| POST | `/api/cases/{token}/run` | start the LLM stages (202) |
| GET | `/api/cases/{token}/status` | stage and progress |
| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
| GET | `/api/cases/{token}/dismissal_suggestions` | T-089 read-only: repeated-dismissal suggestions for the single local profile (see section below) |
| POST | `/api/cases/{token}/dismissal_suggestions/apply` | T-089 the paralegal's click: dismiss this case's pending flags that match one suggestion `{key}` |
| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt, confirm_warnings?}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same token check and judge 1 as an edit (`409 needs_confirm` for non-numeric judge objections only; a number, date or $ figure in the summary that is not in the quote is a hard `422 invalid_edit` with `detail.tokens`, no override, D-034); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`; an override is listed in the notes as `reviewer override: <code>`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
| GET / POST | `/api/cases/{token}/narrative` | D-031 draft treatment paragraph. POST drafts it from ACCEPTED entries only (`400 bad_request` when none): one sentence per cited entry, code-checked (D-006/D-022, no unquoted causation, no flag wording) and judged by judge 1; failures are listed in `removed[]` with a reason (`NOT_AN_ACCEPTED_ENTRY`, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`, `CAUSATION_NOT_QUOTED`, `FLAG_CONTENT`, `SEVERITY_NOT_QUOTED` (severity, outcome or recommendation wording not in the quote), `JUDGE_PARTIAL`, `JUDGE_UNSUPPORTED`, `JUDGE_UNAVAILABLE`). A failed re-draft (`error: LLM_FAILED_AFTER_RETRIES`) or a POST with nothing accepted never overwrites a paragraph already stored: the stored one is returned with `error` alongside, and with nothing stored `NO_ACCEPTED_ENTRIES` stores nothing Returns `{narrative: {status: pending, sentences[{id, entry_id, text, cite, judge}], removed[{entry_id, text, reason, message}], basis, error?}}`; GET returns the stored one or `null` |
| POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
| GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
| POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected` |
| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
| POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
| GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
| GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `ns…` |
| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
| GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
| GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (billed, adjustment, paid, balance, each cited), totals by provider, LOP and lien amounts listed separately, rates excluded, ledger-vs-EOB checks; internal view, never in the letter |
| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |

---

## GET /api/health
----
## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
Both return `404 not_found` unless `ZLAYT_MODE=local`; the public demo stays token-only and has no case list.
`GET /api/cases` -> `{ "cases": [ { "token", "name", "status", "source", "record_count", "counts": {"pending","accepted","edited","dismissed","needs_review"}, "created_at" } ] }`, newest first, never record text.
`GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
`POST /api/cases {"library": "<id>"}` (local mode only; `404` otherwise or for an unknown id) creates a case from a library text exactly like a paste. Cases are isolated: ids are unique per case and decisions never cross cases (T-050).

## GET /api/cases/{token}/billing  (T-083, D-042)
Code-only billing analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs. Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals` (the letter's total line is still accepted charges only, D-019). Unknown token: `404 not_found`.
----
"""Dismissal-pattern SUGGESTIONS for the single local profile (T-089, D-042; code only, LLM_VS_CODE row 12). Suggestions only.

The tool has one local profile: no accounts, no users, no auth. "Profile" means this machine's database, so the history is the set of flags
the paralegal has dismissed in it (read from the flags table; nothing new is stored, and deleting a case deletes its history). Outside
ZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.

When the same lexicon phrase (PHRASE_MIN dismissals) or the same category (CATEGORY_MIN) has been dismissed repeatedly, the review screen
may offer "You dismissed this kind of flag 4 times. Hide similar ones in this case?". This module only READS: suggest() never writes and
never changes a pipeline result, a flag's state or its review_status. The paralegal's click calls apply(), which dismisses the matching
PENDING flags in this case one by one through the normal review path (each a logged `dismiss` event with a reviewer note). Those
bulk-hidden flags are not counted as new dismissals, so a suggestion cannot reinforce itself.

Only lexicon-phrase flags of type pre_existing or causation are eligible. Gap and conflict flags, injection and date warnings, and flags
that code or the model found without a lexicon phrase are never suggested for hiding."""
from fastapi import Request

from app.backend import lexicon_scan, review
from app.db import db as DB

PHRASE_MIN = 3
CATEGORY_MIN = 5
ELIGIBLE_TYPES = ("pre_existing", "causation")
APPLIED_NOTE = "Hidden by dismissal-pattern suggestion (paralegal confirmed)."
_BAD = ("rejected",)


def _eligible(f) -> bool:
    return f["type"] in ELIGIBLE_TYPES and "lexicon" in (f.get("origin") or "")


def _phrase(f):
    """(lexicon entry id, matched phrase) for the flag, from its own evidence text, or (None, None). Same category only."""
    for ev in f.get("evidence") or []:
        hits = [h for h in lexicon_scan.scan(ev.get("text") or "") if h["category"] == f["category"]]
        if hits:
            h = min(hits, key=lambda x: x["start"])
            return h["id"], " ".join(h["text"].lower().split())
    return None, None


----
26:def test_three_dismissals_of_the_same_phrase_surface_a_suggestion_and_do_not_dismiss(tmp_path):
39:def test_two_dismissals_are_not_enough(tmp_path):
46:def test_ineligible_flags_are_never_suggested(tmp_path):
54:def test_category_suggestion_after_five_dismissals_of_different_phrases(tmp_path):
66:def test_apply_dismisses_only_pending_matches_through_review_and_does_not_feed_itself(tmp_path):
"""T-089: dismissal-pattern suggestions for the single local profile. Read-only suggestions; never auto-dismiss; no effect on pipeline output."""
import pytest
from fastapi.testclient import TestClient

from app.backend import dismissal_patterns as DP, pipeline as PL
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record as wr
from tests.unit.test_review_rules import seeded

NEW_ONSET = "New onset pain radiating to right arm with numbness in fingers."


def add_flag(conn, case, fid, *, category="new_onset", text=NEW_ONSET, type_="causation", origin="lexicon+llm", status=None):
    DB.add_item(conn, case, "flag", {"id": fid, "type": type_, "category": category, "origin": origin, "title": "t", "explanation": "e",
                "evidence_json": [{"record_no": 1, "text": text, "start": 0, "end": len(text)}], "state": "verified", "state_reasons_json": []})
    if status:
        DB.apply_review(conn, fid, status, now=1.0, case=case)


def snapshot(conn, case):
    return [(f["id"], f["review_status"], f["state"]) for f in DB.list_items(conn, case, "flag")]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:34.195Z

**tool call — Bash**
````
{
 "command": "git status --short -- app/backend/api.py memory/contracts/api.md tests/unit evals/reports/calibration.json app/backend/calibration* ; echo ----; git diff HEAD --stat -- app/backend/api.py memory/contracts/api.md; echo ----; git diff HEAD -- app/backend/api.py | head -80; echo; ls -la .venv/bin/python 2>&1; git log -1 --format=%H -- evals/reports/calibration.json",
 "description": "Check status and pending diffs in files I will touch"
}
````

### User / tool · 2026-11-02T04:56:34.371Z

**tool result**
````
 M app/backend/api.py
MM evals/reports/calibration.json
MM memory/contracts/api.md
D  tests/unit/spanish_translation_pairs.jsonl
MM tests/unit/test_db.py
MM tests/unit/test_eval_runner.py
 M tests/unit/test_flags_injection.py
 M tests/unit/test_flags_pass.py
 M tests/unit/test_pipeline.py
MM tests/unit/test_reclassify.py
D  tests/unit/test_spanish_failsafe.py
MM tests/unit/test_spanish_records.py
 M tests/unit/test_t075_determinism.py
MM tests/unit/test_t093_eval_signature.py
MM tests/unit/test_trace.py
?? tests/unit/spanish_translation_pairs.jsonl
?? tests/unit/test_conflict_candidates.py
?? tests/unit/test_ocr_invariant.py
?? tests/unit/test_pdf_ocr_limits.py
?? tests/unit/test_spanish_failsafe.py
----
 app/backend/api.py | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
----
diff --git a/app/backend/api.py b/app/backend/api.py
index 021d5f8..2e392c3 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -504,10 +504,10 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             c.close()
 
     case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
-    from app.backend import pdf_routes
-    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
     from app.backend import billing
     billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
+    from app.backend import pdf_routes
+    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
     from app.backend import reclassify
     reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
     dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089

lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
172028cfcff1750fec094d9e567e9d870a8f7b8e
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:37.041Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- memory/contracts/api.md; git diff HEAD -- memory/contracts/api.md | head -60; echo ----CACHED; git diff --cached --stat | tail -5",
 "description": "Inspect pending changes to the contract file and the index"
}
````

### User / tool · 2026-11-02T04:56:37.183Z

**tool result**
````
----CACHED
 tests/unit/test_spanish_failsafe.py               |  238 ----
 tests/unit/test_spanish_records.py                |    7 +-
 tests/unit/test_t093_eval_signature.py            |  102 +-
 tests/unit/test_trace.py                          |   16 -
 33 files changed, 187 insertions(+), 2771 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:51.280Z

**tool call — Bash**
````
{
 "command": "grep -ln \"api.md\" tests/unit/*.py tests/e2e/*.py tools/*.py evals/*.py 2>/dev/null; grep -n \"api.md\" tests/unit/test_api_routes.py tests/unit/test_e2e_contract.py 2>/dev/null | head; echo ----; sed -n 1,30p tests/unit/test_api_routes.py",
 "description": "Find tests that check the API contract or route list"
}
````

### User / tool · 2026-11-02T04:56:51.386Z

**tool result**
````
tests/unit/test_confidence.py
tests/unit/test_ingest.py
tests/unit/test_grounding.py
tests/unit/test_review_rules.py
tests/e2e/test_api.py
tools/compile_agents.py
evals/run.py
----
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


def wait_ready(c, tok):
    for _ in range(160):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert s["status"] == "ready", s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:04.514Z

**tool call — Bash**
````
{
 "command": "sed -n 280,317p evals/run.py; grep -n \"CAL_SMALL_N\\s*=\\|CAL_STATES\\s*=\\|CAL_TYPES\\s*=\" evals/run.py",
 "description": "Read how calibration statements are built"
}
````

### User / tool · 2026-11-02T04:57:04.608Z

**tool result**
````
            add("flag", c["state"], i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", [])))
    if unscored is not None:
        unscored["flag"] += sum(1 for c in cands if c["type"] in FLAG_TYPES and c["state"] in CAL_STATES) - \
            sum(1 for c in uniq if c["type"] in FLAG_TYPES and c["state"] in CAL_STATES)       # duplicates of an earlier flag
    return tally


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


242:CAL_STATES = ("verified", "needs_review")
243:CAL_TYPES = ("entry", "amount", "flag")
244:CAL_SMALL_N = 30            # fewer cases (or items in a cell) than this is reported as a small sample, never rounded up to a rate
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:17.859Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py note T-099 --agent backend --text \"Plan: new app/backend/calibration_route.py (load/validate/add_routes, GET /api/calibration, envelope status ok|missing|invalid, calibration null unless ok); one hook line in api.py; tests/unit/test_calibration_route.py written first; contract section in memory/contracts/api.md. Shared tree is dirty (other workers): commit via temp index built on HEAD, stage my api.py hunk only.\" 2>&1 | tail -2",
 "description": "Record the plan on card T-099"
}
````

### User / tool · 2026-11-02T04:57:17.998Z

**tool result**
````
noted on T-099
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:30.806Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py",
 "content": "\"\"\"T-099: GET /api/calibration serves evals/reports/calibration.json read-only. Present, missing and invalid files are three distinct\nstates; a missing or invalid file gives calibration null and never an invented number. Aggregate counts only, so demo mode is fine.\nFixture backend, no key, SYNTHETIC counts.\"\"\"\nimport copy\nimport json\n\nimport pytest\nfrom fastapi import FastAPI\nfrom fastapi.testclient import TestClient\n\nfrom app.backend import calibration_route as CR\nfrom app.backend.api import create_app\n\n\ndef make():\n    \"\"\"A valid evals.calibration/1 document (one golden case), built the way evals/run.py builds it.\"\"\"\n    by_type = {\n        \"entry\": {\"verified\": {\"matched\": 54, \"total\": 55, \"by_case\": {\"sample\": [54, 55]}},\n                  \"needs_review\": {\"matched\": 2, \"total\": 2, \"by_case\": {\"sample\": [2, 2]}}},\n        \"amount\": {\"verified\": {\"matched\": 9, \"total\": 9, \"by_case\": {\"sample\": [9, 9]}},\n                   \"needs_review\": {\"matched\": 6, \"total\": 6, \"by_case\": {\"sample\": [6, 6]}}},\n        \"flag\": {\"verified\": {\"matched\": 20, \"total\": 20, \"by_case\": {\"sample\": [20, 20]}},\n                 \"needs_review\": {\"matched\": 2, \"total\": 2, \"by_case\": {\"sample\": [2, 2]}}},\n    }\n    by_state = {\"verified\": {\"matched\": 83, \"total\": 84, \"cases\": [\"sample\"]},\n                \"needs_review\": {\"matched\": 10, \"total\": 10, \"cases\": [\"sample\"]}}\n    return {\n        \"schema\": \"evals.calibration/1\", \"backend\": \"fixture\", \"case_count\": 1, \"small_sample\": True,\n        \"source_commit\": \"b85fc1b56386aa0d37460186b5840eec0e578642\", \"generated_at\": \"2026-11-02T04:48:31Z\",\n        \"by_state\": by_state, \"by_type\": by_type, \"not_scored\": {\"entry\": 0, \"amount\": 0, \"flag\": 0, \"total\": 0},\n        \"sentences\": {\n            \"overall\": {\"verified\": \"Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 1 golden cases, small sample).\",\n                        \"needs_review\": \"Items marked needs review matched the record 10/10 times in testing on the fixture backend (recorded replies, 1 golden cases, small sample).\"},\n            \"by_type\": {t: {\"verified\": f\"Verified {n} matched the record {by_type[t]['verified']['matched']}/{by_type[t]['verified']['total']} times in testing on the fixture backend (recorded replies, 1 golden cases, small sample).\",\n                            \"needs_review\": f\"Needs-review {n} matched the record {by_type[t]['needs_review']['matched']}/{by_type[t]['needs_review']['total']} times in testing on the fixture backend (recorded replies, 1 golden cases, small sample).\"}\n                        for t, n in ((\"entry\", \"entries\"), (\"amount\", \"amounts\"), (\"flag\", \"flags\"))}},\n        # not served: the route keeps to the statement's shape\n        \"cases\": [\"sample\"], \"hashes\": {\"app/llm/lexicon.yaml\": \"00\"}, \"models\": {\"generator\": \"x\"}, \"match_rule\": \"...\", \"source\": \"evals.run\",\n        \"source_tree\": \"3f014d4b5d84f8731ff464d4548e18dfce3fbd4f\", \"source_tree_clean\": True,\n    }\n\n\ndef write(tmp_path, doc, name=\"calibration.json\"):\n    p = tmp_path / name\n    p.write_text(doc if isinstance(doc, str) else json.dumps(doc, indent=1, sort_keys=True) + \"\\n\")\n    return p\n\n\ndef bare_client(path):\n    app = FastAPI()\n    CR.add_routes(app, path=path)\n    return TestClient(app)\n\n\n# ---- present\n\ndef test_present_file_is_served_with_source_commit_backend_and_sample_size(tmp_path):\n    out = CR.load(write(tmp_path, make()))\n    assert out[\"status\"] == \"ok\" and out[\"message\"] is None\n    c = out[\"calibration\"]\n    assert c[\"source_commit\"] == \"b85fc1b56386aa0d37460186b5840eec0e578642\"\n    assert c[\"backend\"] == \"fixture\" and c[\"case_count\"] == 1 and c[\"small_sample\"] is True\n    assert c[\"by_state\"][\"verified\"] == {\"matched\": 83, \"total\": 84, \"cases\": [\"sample\"]}\n    assert c[\"sentences\"][\"overall\"][\"verified\"].startswith(\"Verified items matched the record 83/84 times\")\n\n\ndef test_served_object_is_exactly_the_t096_shape_without_hashes_models_or_paths(tmp_path):\n    c = CR.load(write(tmp_path, make()))[\"calibration\"]\n    assert set(c) == set(CR.SERVED)\n    assert not {\"hashes\", \"models\", \"cases\", \"source\", \"source_tree\", \"match_rule\"} & set(c)\n\n\ndef test_route_serves_present_file_over_http(tmp_path):\n    r = bare_client(write(tmp_path, make())).get(\"/api/calibration\")\n    assert r.status_code == 200\n    body = r.json()\n    assert body[\"status\"] == \"ok\" and body[\"calibration\"][\"source_commit\"] == \"b85fc1b56386aa0d37460186b5840eec0e578642\"\n\n\ndef test_committed_report_is_valid_when_present():\n    if not CR.REPORT.exists():\n        pytest.skip(\"evals/reports/calibration.json is not generated in this checkout\")\n    out = CR.load()\n    assert out[\"status\"] == \"ok\", out\n\n\n# ---- missing\n\ndef test_missing_file_is_an_empty_state_with_no_numbers(tmp_path):\n    out = CR.load(tmp_path / \"nope.json\")\n    assert out == {\"status\": \"missing\", \"calibration\": None, \"message\": CR.MISSING}\n\n\ndef test_route_missing_file_returns_200_empty_state_not_an_error(tmp_path):\n    r = bare_client(tmp_path / \"nope.json\").get(\"/api/calibration\")\n    assert r.status_code == 200\n    assert r.json() == {\"status\": \"missing\", \"calibration\": None, \"message\": CR.MISSING}\n\n\n# ---- invalid\n\ndef _bad(doc):\n    d = copy.deepcopy(doc)\n    return d\n\n\nINVALID_CASES = {\n    \"not_json\": \"{not json\",\n    \"not_utf8\": None,      # written as raw bytes below\n    \"top_level_list\": \"[]\",\n    \"wrong_schema\": lambda d: d.update(schema=\"evals.calibration/2\"),\n    \"sum_mismatch_hand_edit\": lambda d: d[\"by_state\"][\"verified\"].update(matched=90),\n    \"sentence_quotes_other_counts\": lambda d: d[\"sentences\"][\"overall\"].update(verified=d[\"sentences\"][\"overall\"][\"verified\"].replace(\"83/84\", \"90/91\")),\n    \"matched_above_total\": lambda d: d[\"by_type\"][\"flag\"][\"verified\"].update(matched=21),\n    \"negative_count\": lambda d: d[\"by_type\"][\"amount\"][\"verified\"].update(matched=-1, total=-1),\n    \"bool_counts\": lambda d: d[\"by_state\"][\"needs_review\"].update(matched=True),\n    \"missing_key\": lambda d: d.pop(\"sentences\"),\n    \"missing_source_commit\": lambda d: d.update(source_commit=\"\"),\n    \"percent_sentence_missing\": lambda d: d[\"sentences\"][\"by_type\"].pop(\"flag\"),\n}\n\n\n@pytest.mark.parametrize(\"name\", sorted(INVALID_CASES))\ndef test_invalid_file_is_an_empty_state_and_is_never_served(tmp_path, name):\n    spec = INVALID_CASES[name]\n    if name == \"not_utf8\":\n        p = tmp_path / \"calibration.json\"\n        p.write_bytes(b\"\\xff\\xfe\\x00bad\")\n    elif isinstance(spec, str):\n        p = write(tmp_path, spec)\n    else:\n        d = make()\n        spec(d)\n        p = write(tmp_path, d)\n    out = CR.load(p)\n    assert out == {\"status\": \"invalid\", \"calibration\": None, \"message\": CR.INVALID}\n    assert \"83/90\" not in json.dumps(out) and \"90/91\" not in json.dumps(out)\n\n\ndef test_invalid_route_response_does_not_echo_file_contents(tmp_path):\n    d = make()\n    d[\"by_state\"][\"verified\"][\"matched\"] = 90\n    r = bare_client(write(tmp_path, d)).get(\"/api/calibration\")\n    assert r.status_code == 200\n    assert r.json() == {\"status\": \"invalid\", \"calibration\": None, \"message\": CR.INVALID}\n\n\ndef test_problems_is_empty_for_a_valid_document_and_names_the_fault_otherwise():\n    assert CR.problems(make()) == []\n    d = make()\n    d[\"by_state\"][\"verified\"][\"matched\"] = 90\n    assert any(\"by_state\" in p or \"sum\" in p or \"sentence\" in p for p in CR.problems(d)) or CR.problems(d)\n\n\n# ---- the route on the real app, demo mode, read-only\n\n@pytest.fixture\ndef app_client(tmp_path, monkeypatch):\n    monkeypatch.setenv(\"LLM_BACKEND\", \"fixture\")\n    monkeypatch.delenv(\"ENABLE_LIVE\", raising=False)\n    monkeypatch.delenv(\"ANTHROPIC_API_KEY\", raising=False)\n    return TestClient(create_app(str(tmp_path / \"cal.sqlite\"), static_dir=str(tmp_path)))\n\n\ndef test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode(app_client):\n    r = app_client.get(\"/api/calibration\")\n    assert r.status_code == 200\n    body = r.json()\n    assert body[\"status\"] in (\"ok\", \"missing\", \"invalid\")\n    assert (\"calibration\" in body) and (body[\"calibration\"] is None) == (body[\"status\"] != \"ok\")\n\n\ndef test_route_carries_no_case_tokens_or_record_text(app_client):\n    body = app_client.get(\"/api/calibration\").json()\n    text = json.dumps(body)\n    assert \"token\" not in text and \"raw_text\" not in text and \"records\" not in text\n\n\ndef test_route_is_read_only(app_client):\n    for method in (\"post\", \"put\", \"patch\", \"delete\"):\n        assert getattr(app_client, method)(\"/api/calibration\", json={}).status_code == 405\n"
}
````

### User / tool · 2026-11-02T04:57:30.882Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:35.304Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py",
 "old_string": "def _bad(doc):\n    d = copy.deepcopy(doc)\n    return d\n\n\nINVALID_CASES = {\n    \"not_json\": \"{not json\",\n    \"not_utf8\": None,      # written as raw bytes below\n    \"top_level_list\": \"[]\",\n    \"wrong_schema\": lambda d: d.update(schema=\"evals.calibration/2\"),\n    \"sum_mismatch_hand_edit\": lambda d: d[\"by_state\"][\"verified\"].update(matched=90),\n    \"sentence_quotes_other_counts\": lambda d: d[\"sentences\"][\"overall\"].update(verified=d[\"sentences\"][\"overall\"][\"verified\"].replace(\"83/84\", \"90/91\")),\n    \"matched_above_total\": lambda d: d[\"by_type\"][\"flag\"][\"verified\"].update(matched=21),\n    \"negative_count\": lambda d: d[\"by_type\"][\"amount\"][\"verified\"].update(matched=-1, total=-1),\n    \"bool_counts\": lambda d: d[\"by_state\"][\"needs_review\"].update(matched=True),\n    \"missing_key\": lambda d: d.pop(\"sentences\"),\n    \"missing_source_commit\": lambda d: d.update(source_commit=\"\"),\n    \"percent_sentence_missing\": lambda d: d[\"sentences\"][\"by_type\"].pop(\"flag\"),\n}",
 "new_string": "INVALID_CASES = {\n    \"not_json\": \"{not json\",\n    \"not_utf8\": None,      # written as raw bytes below\n    \"top_level_list\": \"[]\",\n    \"wrong_schema\": lambda d: d.update(schema=\"evals.calibration/2\"),\n    \"sum_mismatch_hand_edit\": lambda d: d[\"by_state\"][\"verified\"].update(matched=90),\n    \"sentence_quotes_other_counts\": lambda d: d[\"sentences\"][\"overall\"].update(verified=d[\"sentences\"][\"overall\"][\"verified\"].replace(\"83/84\", \"90/91\")),\n    \"matched_above_total\": lambda d: d[\"by_type\"][\"flag\"][\"verified\"].update(matched=21),\n    \"negative_count\": lambda d: d[\"by_type\"][\"amount\"][\"verified\"].update(matched=-1, total=-1),\n    \"bool_counts\": lambda d: d[\"by_state\"][\"needs_review\"].update(matched=True),\n    \"missing_key\": lambda d: d.pop(\"sentences\"),\n    \"missing_source_commit\": lambda d: d.update(source_commit=\"\"),\n    \"statement_for_a_type_missing\": lambda d: d[\"sentences\"][\"by_type\"].pop(\"flag\"),\n}"
}
````

### User / tool · 2026-11-02T04:57:35.372Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:37.414Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py",
 "old_string": "def test_problems_is_empty_for_a_valid_document_and_names_the_fault_otherwise():\n    assert CR.problems(make()) == []\n    d = make()\n    d[\"by_state\"][\"verified\"][\"matched\"] = 90\n    assert any(\"by_state\" in p or \"sum\" in p or \"sentence\" in p for p in CR.problems(d)) or CR.problems(d)",
 "new_string": "def test_problems_is_empty_for_a_valid_document_and_lists_faults_otherwise():\n    assert CR.problems(make()) == []\n    d = make()\n    d[\"by_state\"][\"verified\"][\"matched\"] = 90\n    assert CR.problems(d)"
}
````

### User / tool · 2026-11-02T04:57:37.479Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:38.717Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py",
 "old_string": "import copy\nimport json\n\nimport pytest",
 "new_string": "import json\n\nimport pytest"
}
````

### User / tool · 2026-11-02T04:57:38.779Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:39.713Z

Tests are written first. Now the route module.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:42.133Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/calibration_route.py",
 "content": "\"\"\"GET /api/calibration (T-099): the measured calibration the review screen quotes (T-090 writes it, T-096 shows it).\n\nRead-only. Serves evals/reports/calibration.json, which evals.run writes from the golden cases: aggregate counts, the statements built\nfrom those counts, the source commit and the backend. It holds no record text and no case token, so it is safe in demo mode and has no gate.\n\nThree states, always HTTP 200 with the same envelope {\"status\", \"calibration\", \"message\"}:\n- \"ok\": the file is the evals.calibration/1 shape, its totals add up, and every statement quotes its own counts. `calibration` is the\n  served subset (SERVED below).\n- \"missing\": no file. `calibration` is null. Nothing is invented.\n- \"invalid\": the file cannot be read as a valid measurement (bad JSON, wrong schema, a hand-edited count, a statement that quotes other\n  counts). `calibration` is null and the file's contents are never echoed; the reasons go to the log.\nThe UI hides the accuracy line when `calibration` is null (T-096). This module only reads one fixed path; it never writes.\n\"\"\"\nimport json\nimport logging\nimport pathlib\n\nfrom app.backend import calibration_route_checks as _checks  # noqa: F401  (reserved: none; kept out of this module on purpose)\n"
}
````

### User / tool · 2026-11-02T04:57:42.187Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/app/backend/calibration_route.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:50.578Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/calibration_route.py",
 "content": "\"\"\"GET /api/calibration (T-099): the measured calibration the review screen quotes (T-090 writes it, T-096 shows it).\n\nRead-only. Serves evals/reports/calibration.json, which evals.run writes from the golden cases: aggregate counts, the statements built\nfrom those counts, the source commit and the backend. It holds no record text and no case token, so it is safe in demo mode and has no gate.\n\nThree states, always HTTP 200 with the same envelope {\"status\", \"calibration\", \"message\"}:\n- \"ok\": the file is the evals.calibration/1 shape, its totals add up, and every statement quotes its own counts. `calibration` is the\n  served subset (SERVED below).\n- \"missing\": no file. `calibration` is null. Nothing is invented.\n- \"invalid\": the file cannot be read as a valid measurement (bad JSON, wrong schema, a hand-edited count, a statement that quotes other\n  counts). `calibration` is null and the file's contents are never echoed; the reasons go to the log.\nThe UI hides the accuracy line when `calibration` is null (T-096). This module reads one fixed path and never writes.\n\"\"\"\nimport json\nimport logging\nimport pathlib\n\nROOT = pathlib.Path(__file__).resolve().parents[2]\nREPORT = ROOT / \"evals\" / \"reports\" / \"calibration.json\"\nSCHEMA = \"evals.calibration/1\"\nTYPES = (\"entry\", \"amount\", \"flag\")\nSTATES = (\"verified\", \"needs_review\")\nSERVED = (\"schema\", \"backend\", \"case_count\", \"small_sample\", \"source_commit\", \"generated_at\", \"by_state\", \"by_type\", \"not_scored\", \"sentences\")\nMISSING = \"No calibration has been measured yet, so no accuracy line is shown.\"\nINVALID = \"The calibration file is not a valid measurement, so no accuracy line is shown. Regenerate it with python -m evals.run.\"\nlog = logging.getLogger(\"zlayt.calibration\")\n\n\ndef _count(x) -> bool:\n    return isinstance(x, int) and not isinstance(x, bool) and x >= 0\n\n\ndef _cell_ok(c) -> bool:\n    return isinstance(c, dict) and _count(c.get(\"matched\")) and _count(c.get(\"total\")) and c[\"matched\"] <= c[\"total\"]\n\n\ndef _statement_ok(text, cell) -> bool:\n    \"\"\"A statement is a non-empty string; when its cell has items it must quote that cell's own m/t. A hand-edited number fails here.\"\"\"\n    if not isinstance(text, str) or not text:\n        return False\n    return cell[\"total\"] == 0 or f\"{cell['matched']}/{cell['total']} times\" in text\n\n\ndef problems(c) -> list:\n    \"\"\"Why `c` is not a valid calibration document. Empty list when it is. Checks the shape, the count ranges, that the state totals add up\n    to the type totals, and that each statement quotes its own counts.\"\"\"\n    if not isinstance(c, dict):\n        return [\"not an object\"]\n    bad = []\n    if c.get(\"schema\") != SCHEMA:\n        bad.append(\"schema\")\n    if not (isinstance(c.get(\"backend\"), str) and c[\"backend\"]):\n        bad.append(\"backend\")\n    if not _count(c.get(\"case_count\")):\n        bad.append(\"case_count\")\n    if not isinstance(c.get(\"small_sample\"), bool):\n        bad.append(\"small_sample\")\n    if not (isinstance(c.get(\"source_commit\"), str) and c[\"source_commit\"]):\n        bad.append(\"source_commit\")\n    if not isinstance(c.get(\"generated_at\"), str):\n        bad.append(\"generated_at\")\n    ns = c.get(\"not_scored\")\n    if not (isinstance(ns, dict) and all(_count(ns.get(k)) for k in TYPES + (\"total\",)) and ns[\"total\"] == sum(ns[t] for t in TYPES)):\n        bad.append(\"not_scored\")\n    bs, bt, se = c.get(\"by_state\"), c.get(\"by_type\"), c.get(\"sentences\")\n    if not (isinstance(bs, dict) and isinstance(bt, dict) and all(isinstance(bt.get(t), dict) for t in TYPES)):\n        return bad + [\"by_state or by_type\"]\n    for s in STATES:\n        if not (_cell_ok(bs.get(s)) and isinstance(bs[s].get(\"cases\"), list) and all(isinstance(x, str) for x in bs[s][\"cases\"])):\n            bad.append(f\"by_state.{s}\")\n            continue\n        for k in (\"matched\", \"total\"):\n            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):\n                bad.append(f\"by_state.{s}.{k} is not the sum over by_type (hand-edited count)\")\n    for t in TYPES:\n        for s in STATES:\n            cell = (bt.get(t) or {}).get(s)\n            if not (_cell_ok(cell) and isinstance(cell.get(\"by_case\"), dict)):\n                bad.append(f\"by_type.{t}.{s}\")\n    if bad:\n        return bad\n    if not (isinstance(se, dict) and isinstance(se.get(\"overall\"), dict) and isinstance(se.get(\"by_type\"), dict)):\n        return bad + [\"sentences\"]\n    for s in STATES:\n        if not _statement_ok(se[\"overall\"].get(s), bs[s]):\n            bad.append(f\"sentences.overall.{s} does not quote its counts\")\n    for t in TYPES:\n        for s in STATES:\n            if not _statement_ok((se[\"by_type\"].get(t) or {}).get(s), bt[t][s]):\n                bad.append(f\"sentences.by_type.{t}.{s} does not quote its counts\")\n    return bad\n\n\ndef _envelope(status, calibration=None, message=None) -> dict:\n    return {\"status\": status, \"calibration\": calibration, \"message\": message}\n\n\ndef load(path=REPORT) -> dict:\n    \"\"\"The envelope for the file at `path`: ok with the served subset, missing, or invalid. Read-only; never raises.\"\"\"\n    p = pathlib.Path(path)\n    try:\n        raw = p.read_text(encoding=\"utf-8\")\n    except FileNotFoundError:\n        return _envelope(\"missing\", message=MISSING)\n    except (OSError, UnicodeDecodeError):\n        log.warning(\"calibration file could not be read: %s\", p.name)\n        return _envelope(\"invalid\", message=INVALID)\n    try:\n        doc = json.loads(raw)\n    except ValueError:\n        log.warning(\"calibration file is not JSON: %s\", p.name)\n        return _envelope(\"invalid\", message=INVALID)\n    bad = problems(doc)\n    if bad:\n        log.warning(\"calibration file rejected: %s\", \"; \".join(bad))\n        return _envelope(\"invalid\", message=INVALID)\n    return _envelope(\"ok\", {k: doc[k] for k in SERVED})\n\n\ndef add_routes(app, *, path=REPORT):\n    @app.get(\"/api/calibration\")\n    def calibration():\n        return load(path)\n"
}
````

### User / tool · 2026-11-02T04:57:50.635Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/backend/calibration_route.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:52.907Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_calibration_route.py 2>&1 | tail -30",
 "description": "Run the new calibration route tests"
}
````

### User / tool · 2026-11-02T04:57:53.591Z

**tool result**
````
....................F.F                                                  [100%]
=================================== FAILURES ===================================
_________ test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode _________

app_client = <starlette.testclient.TestClient object at 0x108046330>

    def test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode(app_client):
        r = app_client.get("/api/calibration")
>       assert r.status_code == 200
E       assert 404 == 200
E        +  where 404 = <Response [404 Not Found]>.status_code

tests/unit/test_calibration_route.py:161: AssertionError
___________________________ test_route_is_read_only ____________________________

app_client = <starlette.testclient.TestClient object at 0x108123410>

    def test_route_is_read_only(app_client):
        for method in ("post", "put", "patch", "delete"):
>           assert getattr(app_client, method)("/api/calibration", json={}).status_code == 405
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E           TypeError: Client.delete() got an unexpected keyword argument 'json'

tests/unit/test_calibration_route.py:175: TypeError
=========================== short test summary info ============================
FAILED tests/unit/test_calibration_route.py::test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode
FAILED tests/unit/test_calibration_route.py::test_route_is_read_only - TypeEr...
2 failed, 21 passed in 0.37s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:56.002Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py",
 "old_string": "    for method in (\"post\", \"put\", \"patch\", \"delete\"):\n        assert getattr(app_client, method)(\"/api/calibration\", json={}).status_code == 405",
 "new_string": "    assert app_client.post(\"/api/calibration\", json={}).status_code == 405\n    assert app_client.put(\"/api/calibration\", json={}).status_code == 405\n    assert app_client.patch(\"/api/calibration\", json={}).status_code == 405\n    assert app_client.delete(\"/api/calibration\").status_code == 405"
}
````

### User / tool · 2026-11-02T04:57:56.060Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/tests/unit/test_calibration_route.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:57.269Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/api.py",
 "offset": 512,
 "limit": 4
}
````

### User / tool · 2026-11-02T04:57:57.278Z

**tool result**
````
512	    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
513	    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
514	
515	    @app.get("/api/cases/{token}/export")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:57.568Z

**tool call — Bash**
````
{
 "command": "grep -n \"dismissal_patterns.add_routes\" app/backend/api.py",
 "description": "Locate the dismissal route hook line in api.py"
}
````

### User / tool · 2026-11-02T04:57:57.654Z

**tool result**
````
513:    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:59.443Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/api.py",
 "old_string": "    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089\n",
 "new_string": "    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089\n    from app.backend import calibration_route\n    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)\n"
}
````

### User / tool · 2026-11-02T04:57:59.505Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/backend/api.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:00.714Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k calibration 2>&1 | tail -15",
 "description": "Run the calibration-selected unit tests"
}
````

### User / tool · 2026-11-02T04:58:04.780Z

**tool result**
````
..................................                                       [100%]
34 passed, 1604 deselected in 3.68s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:07.287Z

**tool call — Bash**
````
{
 "command": "timeout 500 .venv/bin/python -m pytest -q tests/unit/test_api.py tests/unit/test_api_routes.py tests/unit/test_boundaries.py tests/unit/test_dismissal_patterns.py 2>&1 | tail -6",
 "description": "Run neighboring API and boundary tests for regressions"
}
````

### User / tool · 2026-11-02T04:58:07.373Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:08.718Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_api.py tests/unit/test_api_routes.py tests/unit/test_boundaries.py tests/unit/test_dismissal_patterns.py 2>&1 | tail -6",
 "description": "Run neighboring API and boundary tests for regressions"
}
````

### User / tool · 2026-11-02T04:58:17.302Z

**tool result**
````
........................................................................ [ 88%]
.........                                                                [100%]
81 passed in 8.17s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:19.720Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --quiet -- memory/contracts/api.md && echo \"api.md clean vs HEAD\"; grep -n \"^| GET | \\`/api/cases\\`, \\`/api/library\\`\" memory/contracts/api.md; grep -n \"^## GET /api/cases/{token}/billing\" memory/contracts/api.md",
 "description": "Confirm contract file is clean and find insertion points"
}
````

### User / tool · 2026-11-02T04:58:19.775Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:21.527Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --quiet -- memory/contracts/api.md && echo clean; grep -n \"api/library\" memory/contracts/api.md | head -5; grep -n \"billing  (T-083\" memory/contracts/api.md",
 "description": "Confirm contract file is clean and find insertion points"
}
````

### User / tool · 2026-11-02T04:58:21.658Z

**tool result**
````
clean
40:| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
645:## GET /api/cases and GET /api/library  (local mode only, D-008/D-031)
648:`GET /api/library` -> `{ "cases": [ { "id": "case_01_date_formats", "name": "...", "description": "..." } ] }` (files in `evals/library/`, falling back to `evals/golden/`; format `<id>.txt` + optional `<id>.expected.json` with `name`/`description`).
651:## GET /api/cases/{token}/billing  (T-083, D-042)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:23.493Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/memory/contracts/api.md",
 "old_string": "| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |\n",
 "new_string": "| GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |\n| GET | `/api/calibration` | T-099 read-only measured calibration (aggregate counts only, no case token, demo-safe): the T-096 shape in `calibration`, or `null` with `status` `missing`/`invalid`. See the section below |\n"
}
````

### User / tool · 2026-11-02T04:58:23.554Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/memory/contracts/api.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:27.434Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/memory/contracts/api.md",
 "old_string": "## GET /api/cases/{token}/billing  (T-083, D-042)",
 "new_string": "## GET /api/calibration  (T-099, serves T-090 counts to T-096)\nRead-only. Serves `evals/reports/calibration.json` (written by `python -m evals.run`), the measured calibration the review screen quotes. It holds aggregate counts, the statements built from them, the source commit, the backend and the sample size. No case token, no record text, so it works in demo mode with no gate. Any other method is `405`.\n\nAlways `200` with one envelope:\n- `{\"status\": \"ok\", \"calibration\": {...}, \"message\": null}`. `calibration` has exactly: `schema` (`evals.calibration/1`), `backend` (`fixture` or a live backend name), `case_count` (the sample size: golden cases pooled), `small_sample` (bool), `source_commit`, `generated_at`, `by_state` (`verified` and `needs_review`, each `{matched, total, cases[]}`), `by_type` (`entry`, `amount`, `flag`, each with the two states as `{matched, total, by_case: {case: [m, t]}}`), `not_scored` (`entry`, `amount`, `flag`, `total`) and `sentences` (`overall` and `by_type`, each state a string).\n- `{\"status\": \"missing\", \"calibration\": null, \"message\": \"...\"}`: no file yet.\n- `{\"status\": \"invalid\", \"calibration\": null, \"message\": \"...\"}`: the file is not a valid measurement (bad JSON or encoding, wrong schema, a count out of range, totals that do not add up, or a statement that does not quote its own `m/t`). The file's contents are never echoed; the reasons go to the server log.\n\nRules for the client: render `sentences.overall.verified` and `sentences.overall.needs_review` verbatim (they name the backend and the basis); never compute or show a percentage; hide the line when `calibration` is null. Nothing is invented: no default numbers appear in any state. `calibration` is served by `app/backend/calibration_route.py`; the route is registered in `create_app` and reads one fixed path.\n\n## GET /api/cases/{token}/billing  (T-083, D-042)"
}
````

### User / tool · 2026-11-02T04:58:27.489Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/memory/contracts/api.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:39.060Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$SCR\" && export GIT_INDEX_FILE=\"$SCR/t099.index\" && rm -f \"$GIT_INDEX_FILE\" && git read-tree HEAD && git show HEAD:app/backend/api.py > \"$SCR/api_head.py\" && python3 - \"$SCR/api_head.py\" <<'EOF'\nimport sys\np = sys.argv[1]\ns = open(p).read()\nanchor = \"    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089\\n\"\nassert s.count(anchor) == 1\nadd = (\"    from app.backend import calibration_route\\n\"\n       \"    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)\\n\")\nopen(p, \"w\").write(s.replace(anchor, anchor + add))\nprint(\"patched HEAD copy\")\nEOF\nblob=$(git hash-object -w \"$SCR/api_head.py\") && git update-index --add --cacheinfo 100644,$blob,app/backend/api.py && git add -- app/backend/calibration_route.py tests/unit/test_calibration_route.py memory/contracts/api.md && git diff --cached --stat && echo \"SCR=$SCR\"",
 "description": "Stage only T-099 files via a temp index built on HEAD"
}
````

### User / tool · 2026-11-02T04:58:39.401Z

**tool result**
````
patched HEAD copy
 app/backend/api.py                   |   2 +
 app/backend/calibration_route.py     | 123 ++++++++++++++++++++++++
 memory/contracts/api.md              |  11 +++
 tests/unit/test_calibration_route.py | 177 +++++++++++++++++++++++++++++++++++
 4 files changed, 313 insertions(+)
SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:43.592Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t099.index\" && git commit -q -F - <<'EOF'\nfeat(backend): GET /api/calibration serves the measured calibration read-only (T-099)\n\nServes evals/reports/calibration.json in the T-096 shape (counts, statements, source commit, backend, sample size).\nEnvelope {status, calibration, message}: ok | missing | invalid; calibration is null unless ok, nothing is invented,\nand the file contents are never echoed. Aggregate only, no case token, so it is demo-safe. Read-only (other methods 405).\nValidation: shape, count ranges, state totals equal type totals, each statement quotes its own m/t.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nEOF\ngit log -1 --format='%H %s' && git show --stat --format= HEAD",
 "description": "Commit staged T-099 files and show the new commit"
}
````

### User / tool · 2026-11-02T04:58:44.005Z

**tool result**
````
check_stale_index: BLOCKED — this commit would revert work that is not yours.
Rebuild the index from HEAD right before adding: GIT_INDEX_FILE=$(mktemp) git read-tree HEAD
app/backend/api.py: staged version matches neither HEAD nor the working tree (stale index?)
memory/contracts/api.md: staged version matches neither HEAD nor the working tree (stale index?)
5b4ccb01ace175f02edeead4d91b104ea73706cc harness: pre-commit blocks stale-index reverts (staged blob matches neither HEAD nor worktree)
 tools/check_stale_index.py | 56 ++++++++++++++++++++++++++++++++++++++++++++++
 tools/install_git_hooks.sh |  6 +++--
 2 files changed, 60 insertions(+), 2 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:48.837Z

**tool call — Bash**
````
{
 "command": "git log -4 --oneline && git diff HEAD --stat -- app/backend/api.py memory/contracts/api.md && echo \"--- api.py HEAD vs worktree:\" && git diff HEAD -- app/backend/api.py | head -30",
 "description": "Check current HEAD and api.py drift after the blocked commit"
}
````

### User / tool · 2026-11-02T04:58:48.973Z

**tool result**
````
5b4ccb0 harness: pre-commit blocks stale-index reverts (staged blob matches neither HEAD nor worktree)
9c1af01 fix(backend): restore the T-085 r2 files that 57a08ba reverted by mistake (stale temp index); T-084 r3 change stays
57a08ba fix(backend): reclassify wording gate uses the classifier's rate verdict and the shared rate cues; class-only restore tested (T-084 r3)
1b1c711 fix(backend): language detection fails safe, French/Portuguese refused, CLI crash, 'no se descarta' keeps its meaning, Spanish cue words, Spanish eval pairs (T-085 r2)
 app/backend/api.py      |  6 ++++--
 memory/contracts/api.md | 15 +++++++++++++--
 2 files changed, 17 insertions(+), 4 deletions(-)
--- api.py HEAD vs worktree:
diff --git a/app/backend/api.py b/app/backend/api.py
index 021d5f8..82c4d7a 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -504,13 +504,15 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
             c.close()
 
     case_extras.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time)
-    from app.backend import pdf_routes
-    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
     from app.backend import billing
     billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
+    from app.backend import pdf_routes
+    pdf_routes.add_routes(app, conn=conn, get_case=get_case, ApiError=ApiError)       # T-086 page image beside OCR text
     from app.backend import reclassify
     reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
     dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089
+    from app.backend import calibration_route
+    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)
 
     @app.get("/api/cases/{token}/export")
     def export(token: str):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:53.470Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -- memory/contracts/api.md | grep \"^[-+]\" | cut -c1-160",
 "description": "Show the api.md diff against current HEAD"
}
````

### User / tool · 2026-11-02T04:58:53.572Z

**tool result**
````
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
+| GET | `/api/calibration` | T-099 read-only measured calibration (aggregate counts only, no case token, demo-safe): the T-096 shape in `calibration`, or `null
-**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.bloc
+**D-044/D-045: refused with `422` while `/trace`'s export gate has any blocker**, and only then: **gate `ready` <=> export `200`** in every state. `detail.bloc
-**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.ex
+**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.ex
+## GET /api/calibration  (T-099, serves T-090 counts to T-096)
+Read-only. Serves `evals/reports/calibration.json` (written by `python -m evals.run`), the measured calibration the review screen quotes. It holds aggregate co
+
+Always `200` with one envelope:
+- `{"status": "ok", "calibration": {...}, "message": null}`. `calibration` has exactly: `schema` (`evals.calibration/1`), `backend` (`fixture` or a live backen
+- `{"status": "missing", "calibration": null, "message": "..."}`: no file yet.
+- `{"status": "invalid", "calibration": null, "message": "..."}`: the file is not a valid measurement (bad JSON or encoding, wrong schema, a count out of range
+
+Rules for the client: render `sentences.overall.verified` and `sentences.overall.needs_review` verbatim (they name the backend and the basis); never compute or
+
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:00.886Z

**tool call — Bash**
````
{
 "command": "export GIT_INDEX_FILE=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t099.index\" && rm -f \"$GIT_INDEX_FILE\" && git read-tree HEAD && SCR=$(dirname \"$GIT_INDEX_FILE\") && git show HEAD:memory/contracts/api.md > \"$SCR/api_md_head.md\" && git show HEAD:app/backend/api.py > \"$SCR/api_head.py\" && python3 - \"$SCR\" <<'EOF'\nimport sys, pathlib\nscr = pathlib.Path(sys.argv[1])\nwt = pathlib.Path(\"/Users/arsis/zlayt-pm-project\")\n# contract: HEAD text + only my row and section, taken from the worktree copy\nmd = (scr / \"api_md_head.md\").read_text()\nw = (wt / \"memory/contracts/api.md\").read_text()\nrow = next(l + \"\\n\" for l in w.splitlines() if l.startswith(\"| GET | `/api/calibration`\"))\nsec_start = w.index(\"## GET /api/calibration  (T-099\")\nsec_end = w.index(\"## GET /api/cases/{token}/billing  (T-083, D-042)\")\nsection = w[sec_start:sec_end]\nrow_anchor = next(l + \"\\n\" for l in md.splitlines() if l.startswith(\"| GET | `/api/cases`, `/api/library`\"))\nsec_anchor = \"## GET /api/cases/{token}/billing  (T-083, D-042)\"\nassert md.count(row_anchor) == 1 and md.count(sec_anchor) == 1\nmd = md.replace(row_anchor, row_anchor + row).replace(sec_anchor, section + sec_anchor)\n(scr / \"api_md_new.md\").write_text(md)\n# api.py: HEAD + the one hook (two lines) after the dismissal hook\ns = (scr / \"api_head.py\").read_text()\nanchor = \"    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089\\n\"\nassert s.count(anchor) == 1\nadd = \"    from app.backend import calibration_route\\n    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)\\n\"\n(scr / \"api_new.py\").write_text(s.replace(anchor, anchor + add))\nprint(\"ok\")\nEOF\nb1=$(git hash-object -w \"$SCR/api_new.py\") && b2=$(git hash-object -w \"$SCR/api_md_new.md\") && git update-index --cacheinfo 100644,$b1,app/backend/api.py && git update-index --cacheinfo 100644,$b2,memory/contracts/api.md && git add -- app/backend/calibration_route.py tests/unit/test_calibration_route.py && git diff --cached --stat && git diff --cached -- app/backend/api.py memory/contracts/api.md | grep \"^[-+]\" | grep -v \"^+++\\|^---\" | cut -c1-120",
 "description": "Rebuild temp index on current HEAD and stage only T-099 hunks"
}
````

### User / tool · 2026-11-02T04:59:00.951Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No closing quotation) | command: export GIT_INDEX_FILE="/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:05.298Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/build_t099_blobs.py",
 "content": "\"\"\"Build the two T-099 blobs from current HEAD text plus only T-099 edits (run from the repo root; scratch helper, not a project file).\"\"\"\nimport pathlib\nimport sys\n\nscr = pathlib.Path(sys.argv[1])\nwt = pathlib.Path(\"/Users/arsis/zlayt-pm-project\")\n\nmd = (scr / \"api_md_head.md\").read_text()\nw = (wt / \"memory/contracts/api.md\").read_text()\nrow = next(l + \"\\n\" for l in w.splitlines() if l.startswith(\"| GET | `/api/calibration`\"))\nsec_start = w.index(\"## GET /api/calibration  (T-099\")\nsec_end = w.index(\"## GET /api/cases/{token}/billing  (T-083, D-042)\")\nsection = w[sec_start:sec_end]\nrow_anchor = next(l + \"\\n\" for l in md.splitlines() if l.startswith(\"| GET | `/api/cases`, `/api/library`\"))\nsec_anchor = \"## GET /api/cases/{token}/billing  (T-083, D-042)\"\nassert md.count(row_anchor) == 1 and md.count(sec_anchor) == 1\nmd = md.replace(row_anchor, row_anchor + row).replace(sec_anchor, section + sec_anchor)\n(scr / \"api_md_new.md\").write_text(md)\n\ns = (scr / \"api_head.py\").read_text()\nanchor = \"    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089\\n\"\nassert s.count(anchor) == 1\nadd = (\"    from app.backend import calibration_route\\n\"\n       \"    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)\\n\")\n(scr / \"api_new.py\").write_text(s.replace(anchor, anchor + add))\nprint(\"blobs ready\")\n"
}
````

### User / tool · 2026-11-02T04:59:05.354Z

**tool result**
````
File created successfully at: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/build_t099_blobs.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:07.676Z

**tool call — Bash**
````
{
 "command": "SCR=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\" && export GIT_INDEX_FILE=\"$SCR/t099.index\" && rm -f \"$GIT_INDEX_FILE\" && git read-tree HEAD && git show HEAD:memory/contracts/api.md > \"$SCR/api_md_head.md\" && git show HEAD:app/backend/api.py > \"$SCR/api_head.py\" && .venv/bin/python \"$SCR/build_t099_blobs.py\" \"$SCR\"",
 "description": "Rebuild temp index from HEAD and prepare T-099 blobs"
}
````

### User / tool · 2026-11-02T04:59:07.914Z

**tool result**
````
blobs ready
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:10.355Z

**tool call — Bash**
````
{
 "command": "SCR=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\" && export GIT_INDEX_FILE=\"$SCR/t099.index\" && b1=$(git hash-object -w \"$SCR/api_new.py\") && b2=$(git hash-object -w \"$SCR/api_md_new.md\") && git update-index --cacheinfo 100644,$b1,app/backend/api.py && git update-index --cacheinfo 100644,$b2,memory/contracts/api.md && git add -- app/backend/calibration_route.py tests/unit/test_calibration_route.py && git diff --cached --stat",
 "description": "Stage the T-099 blobs and new files in the temp index"
}
````

### User / tool · 2026-11-02T04:59:10.679Z

**tool result**
````
 app/backend/api.py                   |   2 +
 app/backend/calibration_route.py     | 123 ++++++++++++++++++++++++
 memory/contracts/api.md              |  11 +++
 tests/unit/test_calibration_route.py | 177 +++++++++++++++++++++++++++++++++++
 4 files changed, 313 insertions(+)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:14.913Z

**tool call — Bash**
````
{
 "command": "SCR=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\" && export GIT_INDEX_FILE=\"$SCR/t099.index\" && git commit -q -F \"$SCR/msg.txt\" 2>&1 | tail -5; echo \"exit=$?\"; git log -1 --format='%h %s'",
 "description": "Commit the staged T-099 files (message file written first)"
}
````

### User / tool · 2026-11-02T04:59:15.347Z

**tool result**
````
check_stale_index: BLOCKED — this commit would revert work that is not yours.
Rebuild the index from HEAD right before adding: GIT_INDEX_FILE=$(mktemp) git read-tree HEAD
app/backend/api.py: staged version matches neither HEAD nor the working tree (stale index?)
memory/contracts/api.md: staged version matches neither HEAD nor the working tree (stale index?)
exit=0
5b4ccb0 harness: pre-commit blocks stale-index reverts (staged blob matches neither HEAD nor worktree)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:17.464Z

**tool call — Bash**
````
{
 "command": "cat tools/check_stale_index.py",
 "description": "Read the stale-index pre-commit check"
}
````

### User / tool · 2026-11-02T04:59:17.545Z

**tool result**
````
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


def main() -> int:
    if not blob("HEAD"):
        return 0  # first commit
    hits = []
    raw =git("diff", "--cached", "--name-status", "--no-renames", "-z").split("\0")
    pairs = [(raw[i], raw[i + 1]) for i in range(0, len(raw) - 1, 2) if raw[i]]
    for status, path in pairs:
        on_disk = (ROOT / path).is_file()
        if status == "D":
            if on_disk:
                hits.append(f"{path}: staged as deleted but still on disk (stale index?)")
            continue
        staged = blob(f":{path}")
        head = blob(f"HEAD:{path}")
        work = git("hash-object", "--", path).strip() if on_disk else None
        if staged and staged != head and staged != work:
            hits.append(f"{path}: staged version matches neither HEAD nor the working tree (stale index?)")
    if hits:
        print("check_stale_index: BLOCKED — this commit would revert work that is not yours.\n"
              "Rebuild the index from HEAD right before adding: GIT_INDEX_FILE=$(mktemp) git read-tree HEAD\n"
              + "\n".join(hits))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:29.770Z

**tool call — Bash**
````
{
 "command": "git log -2 --format='%h %s' && git status --short -- app/backend/api.py memory/contracts/api.md && git diff HEAD --stat -- app/backend/api.py memory/contracts/api.md",
 "description": "Recheck HEAD and the other workers' pending edits in shared files"
}
````

### User / tool · 2026-11-02T04:59:29.909Z

**tool result**
````
e511778 fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)
5b4ccb0 harness: pre-commit blocks stale-index reverts (staged blob matches neither HEAD nor worktree)
 M app/backend/api.py
MM memory/contracts/api.md
 app/backend/api.py | 6 ++++--
 1 file changed, 4 insertions(+), 2 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:35.955Z

**tool call — Bash**
````
{
 "command": "git diff HEAD -- memory/contracts/api.md | grep \"^[-+]\" | grep -v \"^+++\\|^---\" | cut -c1-90",
 "description": "Check api.md diff against the new HEAD"
}
````

### User / tool · 2026-11-02T04:59:36.059Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:38.459Z

**tool call — Bash**
````
{
 "command": "git show --stat --format='%h %s' HEAD | head -20; echo ---; git show HEAD:memory/contracts/api.md | grep -c \"calibration\"; git show HEAD:app/backend/api.py | grep -c calibration; git ls-files app/backend/calibration_route.py tests/unit/test_calibration_route.py",
 "description": "See what HEAD commit included and whether my contract edits landed"
}
````

### User / tool · 2026-11-02T04:59:38.616Z

**tool result**
````
e511778 fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)

 app/backend/grounding.py  |  28 +++++++++++++
 app/backend/trace.py      |  94 +++++++++++++++++++++++++++++++++++++-----
 memory/contracts/api.md   |  15 ++++++-
 tests/unit/test_export.py |  12 ++++++
 tests/unit/test_trace.py  | 102 ++++++++++++++++++++++++++++++++++++++++++++++
 5 files changed, 239 insertions(+), 12 deletions(-)
---
7
0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:49.748Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k calibration 2>&1 | tail -2",
 "description": "Re-run the calibration tests on the working tree"
}
````

### User / tool · 2026-11-02T04:59:53.581Z

**tool result**
````
..................................                                       [100%]
34 passed, 1640 deselected in 3.44s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:56.194Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py ac T-099 --check 1 --agent backend --evidence \"tests/unit/test_calibration_route.py: pytest -q tests/unit -k calibration gives 34 passed (present, missing, invalid, read-only, demo mode)\" && python3 tools/board.py note T-099 --agent backend --text \"Commit BLOCKED by tools/check_stale_index.py: app/backend/api.py has another worker's uncommitted reorder (pdf_routes/billing lines) in the worktree, so the staged HEAD+hook blob matches neither HEAD nor worktree. Not bypassing the guard and not committing their hunk. Also: my contract section for GET /api/calibration already landed inside e511778 (T-098 commit, memory/contracts/api.md), so HEAD documents a route HEAD does not yet serve. Needs the owner of the api.py reorder to commit or drop it; then I commit calibration_route.py, tests/unit/test_calibration_route.py and the 2-line hook.\" 2>&1 | tail -1",
 "description": "Record AC evidence and the commit blocker on T-099"
}
````

### User / tool · 2026-11-02T04:59:56.391Z

**tool result**
````
AC 1 checked: tests/unit/test_calibration_route.py: pytest -q tests/unit -k calibration gives 34 passed (present, missing, invalid, read-only, demo mode)
noted on T-099
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:59.717Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py handoff T-099 --agent backend --text \"Changed: app/backend/calibration_route.py (new; load() returns ok|missing|invalid envelope; problems() validates T-096 shape, count ranges, state totals = type totals, each statement quotes its own m/t; add_routes registers GET /api/calibration; read-only). Hook: 2 lines in app/backend/api.py after the T-089 hook. Contract: memory/contracts/api.md section plus endpoint row. Tests: tests/unit/test_calibration_route.py (34 cases). Verified: pytest -q tests/unit -k calibration = 34 passed; test_api, test_api_routes, test_boundaries, test_dismissal_patterns = 81 passed. Not done: NOT committed (guard, see note); card stays in_progress, not moved to in_review. Left: once the api.py reorder owner commits or drops it, commit calibration_route.py, the test file and the 2-line hook via temp index on HEAD. Surprised: my contract edit rode into e511778 (T-098) through the shared worktree; T-096 frontend can consume /api/calibration now only after that commit lands.\" 2>&1 | tail -1",
 "description": "Write the T-099 handoff with the commit blocker"
}
````

### User / tool · 2026-11-02T04:59:59.861Z

**tool result**
````
handoff written on T-099
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:04.673Z

**tool call — Bash**
````
{
 "command": "git log -1 --format='%h %s' && SCR=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\" && export GIT_INDEX_FILE=\"$SCR/t099.index\" && rm -f \"$GIT_INDEX_FILE\" && git read-tree HEAD && git show HEAD:app/backend/api.py > \"$SCR/api_head.py\" && .venv/bin/python -c \"\nimport pathlib,sys\nscr=pathlib.Path(sys.argv[1]); s=(scr/'api_head.py').read_text()\na='    dismissal_patterns.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, ApiError=ApiError, now=time.time, local_mode=local_mode)   # T-089\\n'\nassert s.count(a)==1\nadd='    from app.backend import calibration_route\\n    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)\\n'\n(scr/'api_new.py').write_text(s.replace(a,a+add)); print('ok')\" \"$SCR\" && b1=$(git hash-object -w \"$SCR/api_new.py\") && git update-index --cacheinfo 100644,$b1,app/backend/api.py && git add -- app/backend/calibration_route.py tests/unit/test_calibration_route.py && git diff --cached --stat",
 "description": "Rebuild temp index from current HEAD with only T-099 changes"
}
````

### User / tool · 2026-11-02T05:00:05.190Z

**tool result**
````
36a982b docs: D-047 side/negation tokens hard 422, drop 409 keep-my-wording path
ok
 app/backend/api.py                   |   2 +
 app/backend/calibration_route.py     | 123 ++++++++++++++++++++++++
 tests/unit/test_calibration_route.py | 177 +++++++++++++++++++++++++++++++++++
 3 files changed, 302 insertions(+)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:08.569Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t099_msg.txt",
 "content": "feat(backend): GET /api/calibration serves the measured calibration read-only (T-099)\n\nServes evals/reports/calibration.json in the T-096 shape (counts, statements, source commit, backend, sample size).\nEnvelope {status, calibration, message}: ok | missing | invalid. calibration is null unless ok; nothing is invented\nand the file contents are never echoed. Aggregate only, no case token, so it is demo-safe. GET only (other methods 405).\nValidation: shape, count ranges, state totals equal type totals, each statement quotes its own m/t.\nContract section is already in memory/contracts/api.md (landed with e511778).\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"
}
````

### User / tool · 2026-11-02T05:00:08.622Z

**tool result**
````
File created successfully at: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t099_msg.txt (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:11.040Z

**tool call — Bash**
````
{
 "command": "SCR=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\" && export GIT_INDEX_FILE=\"$SCR/t099.index\" && git commit -q -F \"$SCR/t099_msg.txt\" && git log -1 --format='%H %s' && git show --stat --format= HEAD",
 "description": "Commit the T-099 files from the temp index"
}
````

### User / tool · 2026-11-02T05:00:11.777Z

**tool result**
````
check_secrets: ok (3 file(s) scanned staged)
3ecb8b1ca58b97c2d23cdd78a8a99a7bf292f8db feat(backend): GET /api/calibration serves the measured calibration read-only (T-099)
 app/backend/api.py                   |   2 +
 app/backend/calibration_route.py     | 123 ++++++++++++++++++++++++
 tests/unit/test_calibration_route.py | 177 +++++++++++++++++++++++++++++++++++
 3 files changed, 302 insertions(+)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:15.932Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py commit T-099 --sha 3ecb8b1ca58b97c2d23cdd78a8a99a7bf292f8db --agent backend 2>&1 | tail -1 && python3 tools/board.py handoff T-099 --agent backend --text \"Changed: app/backend/calibration_route.py (new; load() gives ok|missing|invalid envelope; problems() checks the T-096 shape, count ranges, state totals = type totals, each statement quotes its own m/t; add_routes registers read-only GET /api/calibration). Hook: 2 lines in app/backend/api.py after the T-089 hook. Contract: memory/contracts/api.md (section and endpoint row; they landed earlier inside e511778, T-098, through the shared worktree). Tests: tests/unit/test_calibration_route.py. Verified: pytest -q tests/unit -k calibration = 34 passed; test_api, test_api_routes, test_boundaries, test_dismissal_patterns = 81 passed. Commit 3ecb8b1 (temp index on HEAD, 3 files, 302 insertions). Left: T-096 frontend consumes it. Surprised: the stale-index guard blocked the first attempt and was then relaxed to pass partial stages.\" 2>&1 | tail -1 && python3 tools/board.py move T-099 in_review --agent backend 2>&1 | tail -1",
 "description": "Record commit, refresh handoff and move card to in_review"
}
````

### User / tool · 2026-11-02T05:00:16.288Z

**tool result**
````
T-099: commit 3ecb8b1ca58b97c2d23cdd78a8a99a7bf292f8db recorded
handoff written on T-099
T-099: in_progress -> in_review
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:17.652Z

**tool call — mcp__ccd_turn__update_plan**
````
{
 "items": [
  {
   "content": "Read T-099 and T-096 field shape",
   "status": "completed"
  },
  {
   "content": "Write tests and route module, hook api.py",
   "status": "completed"
  },
  {
   "content": "Commit via temp index and move to in_review",
   "status": "completed"
  }
 ],
 "scope": "first_task"
}
````

### User / tool · 2026-11-02T05:00:17.660Z

**tool result (error)**
````
PreToolUse:mcp__ccd_turn__update_plan hook error: Not shown: you are a subagent, and the app shows only the main conversation's task list and wrap-up. Do not call update_plan or wrap_up again; carry on with your task and report your result as usual.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:18.793Z

T-099 is in_review as commit 3ecb8b1: `GET /api/calibration` serves the T-096 shape with ok, missing and invalid states; 34 calibration tests pass.
