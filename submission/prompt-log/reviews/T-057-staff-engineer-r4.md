# T-057 review, round 4: D-039 freeze after decisions, staff-engineer-reviewer

Commit under review: f201e3b (`fix(backend): freeze stored records once any item is decided`), pinned by `git archive` into `artifacts/review-evidence/T-057-staff-engineer-r4/tree`. HEAD at review time was f201e3b. The live working tree is dirty (318 entries in `git status --short`), so the pinned tree is the control.

Verdict: **pass**. The round-3 blocker is closed. Accepted items keep their record ids and excerpts across a failing re-split and a re-split with moved boundaries, and no split call is made once an item is decided. Two minor findings remain: the freeze's edit, dismiss, amount and flag triggers have no test that would fail if they were removed.

## Round-3 blocker: closed

- `probe_accepted_orphan.py` on the pinned f201e3b tree: `run2 records [('r1', 0, 47), ('r2', 48, 85), ('r3', 86, 128)]`, `after run2 entries [('e1', ['r1'], 'accepted'), ('e2', ['r2'], 'accepted'), ('e3', ['r3'], 'accepted')]`, `no orphaned entries []`, exit 0.
- `probe_accepted_orphan_success.py` on the pinned tree: same stored records, `no orphaned entries []`, exit 0.
- Control, same probes on the r3 tree (8bf99fb): `ORPHANED accepted entries ... ['e2', 'e3']` and `['e3']`. The probes detect the bug when it is present.
- Reviewer probe `probe_decisions.py` (written for this round, in the r4 evidence dir) applies each decision kind before run 2 and checks, per scenario: split calls on the re-run, stored records unchanged, each entry's `record_ids` resolve, and each excerpt lies inside its record span. Pinned tree: `split_calls_on_rerun=0 | records_unchanged=True | entry_violations=none` for entry accept, entry edit, entry dismiss, and flag accept, on both a failing split and moved boundaries. Amount accept was not exercised (the fixture has no amount items, printed as SKIP).
- The freeze has one entry point. `run_pipeline` is the only function that reaches the split step (`app/backend/api.py:326`, `app/backend/pipeline.py:422`, `pipeline.py:484`, `app/llm/record.py:29`). Only `pipeline.py:255` passes `splitter=_frozen_splitter(conn, cid)`. The other `run_ingest` call (`pipeline.py:195`) passes no `call`, so it cannot reach the model.

## Test suite

- `.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider` on the pinned tree: `34 passed in 0.55s`, exit 0.
- Same command in the live dirty tree: `34 passed in 0.54s`, exit 0 (not a clean control).
- The fix adds two parametrized test functions (`[call_fails]`, `[different_bounds]`) and `test_resplit_stays_allowed_while_every_entry_is_pending`. The r3 count of 29 was on a different base; the count of 34 is what this tree collects.
- Pinned tree is at f201e3b. Note the brief's `python3 -m pytest` form was not used: system python3 has no pytest (per the r3 review); `.venv/bin/python` was used.

## Mutants (scratch copies, not committed)

| Mutant | Change in `_frozen_splitter` (pipeline.py:116) | pytest result | Probe result |
|---|---|---|---|
| `artifacts/review-evidence/T-057-staff-engineer-r4/mut-no-freeze` | `return None` at the top (freeze removed) | 2 failed, 32 passed (both `test_rerun_after_decisions...[call_fails|different_bounds]`) | entry accept/edit/dismiss: `split_calls_on_rerun=1`, orphans e2, e3 (or e3). Control shows the bug returns. |
| `artifacts/review-evidence/T-057-staff-engineer-r4/mut-entries-only` | trigger on entry decisions only | **34 passed** | flag accept: `split_calls_on_rerun=1`, `records_unchanged=False` (provenance changes, no entry orphan in this fixture) |
| `artifacts/review-evidence/T-057-staff-engineer-r4/mut-accept-only` | trigger on `accepted` only | **34 passed** | entry edit and entry dismiss: `split_calls_on_rerun=1`, orphans e2, e3 (or e3). Flag accept is frozen. |

Both survivors are real regressions that the suite does not see. The code as shipped is correct.

## Findings

1. **minor: the freeze's edit, dismiss, amount and flag triggers are untested.** All three new tests accept entries only. Removing edit and dismiss from the trigger (mut-accept-only) or removing flags (mut-entries-only) leaves 34 of 34 green, and the probe shows provenance breaking in each case. D-039's clause names "accepted, edited or dismissed", so the non-accept branches are part of the binding rule. Evidence: `tests/unit/test_split_llm.py` (the three new tests); `app/backend/pipeline.py:116`; the mutant results above. Why it matters: a later refactor can drop a trigger without any test failing, and the paralegal's provenance is lost silently. Fix: parametrize `test_rerun_after_decisions_reuses_stored_records_and_never_resplits` over `accept`, `edit`, `dismiss` on entries, plus a flag-accept case, and add an amount fixture that has at least one amount item. Acceptance test: each of mut-accept-only and mut-entries-only makes at least one test fail, and `probe_decisions.py` on the pinned tree still prints `entry_violations=none` for every scenario.

2. **minor (question, not a violation): scope of the trigger.** `_frozen_splitter` freezes when any entry, amount or flag is decided (`pipeline.py:116`). The D-039 text in `memory/ORCHESTRATOR_DECISIONS.md:47` names entries only. The code is stricter than the text, which keeps provenance safer, so I do not rate it. Chris should confirm which reading is intended (see questions below). Fix only if the text is meant to be the entry-only rule.

## What I did not exercise

- Frontend rendering of the why panel and the export file (read the code path only).
- Amount-triggered freeze with a real amount item (SKIP in `probe_decisions.py`; no fixture item).
- `python -m app.pipeline evals/golden/sample.txt` and the 3-run live eval (not in the card's brief).
- Live backend and the `confirm_rerun` UI path (`api.py:348`).

## Checks on the fix diff

- `git show f201e3b | grep -E "^\+" | grep -nE "except|float\(|sleep\("` returns no matches (grep exit 1). The diff adds no bare `except`, no float money arithmetic, and no sleep.

## Model note

This review was run as claude-haiku-5-5, as the brief asks. The JSON block below carries real values; no API key strings appear in this file.

```json
{"card": "T-057", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f201e3b pinned by git archive at artifacts/review-evidence/T-057-staff-engineer-r4/tree; app/backend/pipeline.py (_frozen_splitter, run_pipeline) and tests/unit/test_split_llm.py; split-only; no app URL; sample case via probes only",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-057-staff-engineer-r3.md, memory/ORCHESTRATOR_DECISIONS.md D-039 (grep), git show f201e3b (pipeline.py and test_split_llm.py diff)",
  "git archive f201e3b into artifacts/review-evidence/T-057-staff-engineer-r4/tree",
  ".venv/bin/python artifacts/review-evidence/T-057-staff-engineer-r3/probe_accepted_orphan.py <r4 tree>: no orphaned entries, exit 0",
  ".venv/bin/python artifacts/review-evidence/T-057-staff-engineer-r3/probe_accepted_orphan_success.py <r4 tree>: no orphaned entries, exit 0",
  "control: both probes on r3 tree 8bf99fb: ORPHANED ['e2','e3'] and ['e3']",
  ".venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider: pinned tree 34 passed; live dirty tree 34 passed",
  "collect-only and -v on the six rerun/resplit tests",
  "mutants in artifacts/review-evidence/T-057-staff-engineer-r4/: mut-no-freeze (2 failed, 32 passed), mut-entries-only (34 passed), mut-accept-only (34 passed)",
  "artifacts/review-evidence/T-057-staff-engineer-r4/probe_decisions.py on pinned tree and all three mutants (entry accept/edit/dismiss, flag accept; amount SKIPPED)",
  "grep of callers of run_pipeline, run_ingest, make_splitter, splitter= in the pinned tree",
  "git show f201e3b added lines grep for except, float(, sleep(: no matches"
 ],
 "verdict": "pass",
 "scores": {"round-3 blocker closed (accepted items keep record ids and excerpts)": 5, "freeze tests catch removal of the freeze": 4, "freeze tests catch removal of each named trigger (accept, edit, dismiss, flag)": 2, "no LLM and no swallowed errors on the freeze path": 5},
 "findings": [
  {"severity": "minor",
   "title": "The freeze's edit, dismiss, amount and flag triggers have no test that fails if they are removed",
   "evidence": "tests/unit/test_split_llm.py: the three new tests accept entries only. Mutant artifacts/review-evidence/T-057-staff-engineer-r4/mut-accept-only (trigger on accepted only): pytest 34 passed; probe_decisions.py prints 'entry_edit FAILING split_calls_on_rerun=1 | records_unchanged=False | entry_violations=[\"e2 orphan [\\'r2\\']\", \"e3 orphan [\\'r3\\']\"]' and the same for entry_dismiss. Mutant mut-entries-only (no flag trigger): pytest 34 passed; probe prints 'flag_accept FAILING split_calls_on_rerun=1 | records_unchanged=False'. Code: app/backend/pipeline.py:116.",
   "why_it_matters": "D-039 names accepted, edited and dismissed items. A later refactor can drop a trigger without any test failing, and the paralegal's provenance is then lost silently. The code as shipped is correct, so this is a test-strength gap, not a spec violation.",
   "fix": "Parametrize test_rerun_after_decisions_reuses_stored_records_and_never_resplits over accept, edit and dismiss on entries, plus a flag-accept case; add an amount fixture with at least one amount item and decide it.",
   "acceptance_test": "Each of mut-accept-only and mut-entries-only makes at least one test in tests/unit/test_split_llm.py fail; probe_decisions.py on the pinned tree prints entry_violations=none for every scenario, with split_calls_on_rerun=0."},
  {"severity": "minor",
   "title": "Freeze trigger is broader than D-039 text (question, not a violation)",
   "evidence": "app/backend/pipeline.py:116 freezes on any entry, amount or flag decision; memory/ORCHESTRATOR_DECISIONS.md:47 (D-039) names entries only.",
   "why_it_matters": "The code is stricter than the binding text, which keeps provenance safer, so it does not break the rule. It does make the rule's reach unclear to the next reader.",
   "fix": "Chris to confirm the intended reading. If the entry-only reading is intended, narrow the code and add a test that flag-only decisions still allow a re-split. If the broader reading is intended, amend D-039's text.",
   "acceptance_test": "D-039 text and pipeline.py:116 name the same set of item kinds, and a test covers the chosen set."}
 ],
 "whats_right": [
  "Round-3 blocker is closed: the orphan probes print no orphans on f201e3b and reproduce the bug on the 8bf99fb control",
  "The freeze is the only route to the split step: every run_pipeline caller goes through _frozen_splitter, and a decided case makes zero split calls on re-run",
  "The new tests fail when the whole freeze is removed (2 failed, 32 passed), so the blocker path is guarded"
 ],
 "questions_for_chris": [
  "Does D-039 intend an amount or flag decision alone to freeze the records? The code freezes on those, and the D-039 text names entries only (memory/ORCHESTRATOR_DECISIONS.md:47)."
 ]}
```
