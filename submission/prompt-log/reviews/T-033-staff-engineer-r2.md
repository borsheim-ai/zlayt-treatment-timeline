# T-033 review - staff-engineer-reviewer (round 2)

Verdict: changes. No blockers. The round-1 major (a real charge whose clause contains 'per' or 'rate' is classified `rate`) is only partly fixed. The rate rule now needs a unit noun, so the five round-1 repro strings no longer come out as rate. But the rate check still reads a six-word label window that crosses a comma. A charge that follows a per-visit rate in the same sentence still classifies as `rate` and drops out of the total, which is the same symptom and the same consequence. I keep the round-1 severity (major) and do not close the finding.

Round-1 status:
- Major, per/rate classification: open. Residual reproduced below (finding 1).
- Minor, `$1,234.567` truncated: closed. Pinned by `test_more_than_two_decimals_is_unclear_not_truncated`, which passes.
- Minor, provider single-practice guard unasserted: closed. The guard-off mutation now fails `test_provider_and_accident_conflicts_only_where_golden_expects`.
- Nit, case_07 totals status `partial_unclear`: not re-exercised this round. The r2 golden run checks the case_07 total (42000 OK) but not the status string.
- Nit, non-`$` money forms and `$0`: not re-exercised this round.

Commands run and output:

```
$ .venv/bin/python -m pytest tests/unit/test_amounts.py tests/unit/test_totals.py -q 2>&1 | tail -2
.                                                                        [100%]
73 passed in 0.14s

$ grep -rn "Charge per invoice" tests/
tests/unit/test_amounts.py:97:    "Charge per invoice 4471: $400", "Billed per itemized statement: $1,850", "Charge (per invoice): $400",
tests/unit/test_amounts.py:106:    t = "Charge per invoice 4471: $400"

$ .venv/bin/python artifacts/review-evidence/T-033-golden.py 2>&1 | tail -3
OK   flag_templates no llm/net import, no float( 
     imports ['app.backend.dates'] False
FAILS 0
```

Full golden output saved to `artifacts/review-evidence/T-033-r2-golden.out.txt`: exit 0, `^OK ` lines 126, `^FAIL ` lines 0, `FAILS 0`. The 126 count matches round 1.

Classifier probe (`python -I`, `find_amounts` then `classify`):

```
'Charge per invoice 4471: $400'                       -> [('$400', 40000, 'charge')]
'Per statement dated 2026-03-01, charge: $400'        -> [('$400', 40000, 'charge')]
'Billed per itemized statement: $1,850'               -> [('$1,850', 185000, 'charge')]
'Charge (per invoice): $400'                          -> [('$400', 40000, 'unclear')]
'Charge: $400 per statement'                          -> [('$400', 40000, 'charge')]
'Charge per visit $185'                               -> [('$185', 18500, 'rate')]
'$185 per visit' / '$185/visit' / 'Charge per session $185' / '$185 per hour' -> rate
'Charge per unit $12'                                 -> [('$12', 1200, 'rate')]
'Charge per visit, $185.'                             -> [('$185', 'rate')]
'Charge per visit $185. Charge: $400'                 -> [('$185', 'rate'), ('$400', 'charge')]
'Standard rate $185 per visit, hospital statement item $6,240 on 2026-01-09.'
                                                      -> [('$185', 'rate'), ('$6,240', 'rate')]   <- residual
'Standard rate $185 per visit. Hospital statement item $6,240 on 2026-01-09.'
                                                      -> [('$185', 'rate'), ('$6,240', 'charge')]
'Charge per visit $185 per invoice 4471: $400'        -> [('$185', 'rate'), ('$400', 'rate')]     <- residual
```

Mutations, run in scratch copies under the scratchpad (repo untouched):
- Round-1 rule restored (`_RATE_WORD` back to any `per|each|rate`), `pytest tests/unit/test_amounts.py tests/unit/test_totals.py -q`: `5 failed, 68 passed`. The new per-non-unit tests catch the round-1 regression.
- Conflicts guard `if len(practices) < 2:` changed to `if False:`, `pytest tests/unit/test_conflicts.py -q`: `1 failed, 5 passed`, failing `test_provider_and_accident_conflicts_only_where_golden_expects`. Restored copy: `6 passed`. Real repo, same file: `6 passed`.
- A full-suite run in the scratch copy is not a valid baseline. Even unmutated it showed `17 failed, 3 errors` because the copy is incomplete, so I did not use those numbers.

Read in full: `app/backend/amounts.py:12-16` (`_BOUNDARY`, `_UNIT`, `_RATE_WORD`, `_RATE_AFTER`), `:45-47` (`_label`), `:50-58` (`classify`, rate check at `:58`); `tests/unit/test_amounts.py:95-125`; `tests/unit/test_conflicts.py:40-44`. Grep of the five modules: no `float(`, no LLM or network import.

## Findings

- **Major (open from round 1).** The rate check reads a six-word window that is not bounded by the previous figure. `_BOUNDARY` (`amounts.py:12`) splits only on `.;!?` and newlines, so a rate phrase attached to an earlier amount is read as the label of the next amount. Repro: `'Standard rate $185 per visit, hospital statement item $6,240 on 2026-01-09.'` gives `$6,240` class `rate`. The same sentence with a period instead of the comma gives `charge`. The residual also reaches a charge that follows a rate phrase with no comma: `'Charge per visit $185 per invoice 4471: $400'` gives `$400` class `rate`. No test in `tests/unit/test_amounts.py` covers a figure that follows another figure's rate phrase; my grep for comma and cross-figure cases found none. Why it matters: this is the round-1 failure. A stated hospital charge is removed from "Billed charges stated in these records", the paralegal can only accept or dismiss a rate, and the note is misleading. Fix: bound the label to the current figure. The label should start after the previous amount's end and stop at the existing sentence boundaries. Do not split on comma alone: `'Charge per visit, $185.'` is rate today and must stay rate. Acceptance test: in `tests/unit/test_amounts.py`, parametrize `'Standard rate $185 per visit, hospital statement item $6,240 on 2026-01-09.'` and `'Charge per visit $185 per invoice 4471: $400'` so that the non-rate figure is `charge` or `unclear`, never `rate`; keep `'Charge per visit, $185.'` as `rate`. Mutation check: restore the unbounded window and the new test must fail.

## Scores rationale

Amount classification moves from 2 in round 1 to 3. The narrowed rule is right, but the window still lets a rate leak across figures. The other scores are unchanged or raised for the closed minor findings.

```json
{"card": "T-033", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "app/backend/amounts.py (rate rule, _label, _BOUNDARY); tests/unit/test_amounts.py; tests/unit/test_conflicts.py; artifacts/review-evidence/T-033-golden.py. Round 2 of T-033. No app URL; no pipeline wiring in scope.",
 "exercised": [
  ".venv/bin/python -m pytest tests/unit/test_amounts.py tests/unit/test_totals.py -q 2>&1 | tail -2 -> 73 passed in 0.14s",
  "grep -rn 'Charge per invoice' tests/ -> tests/unit/test_amounts.py:97 and :106",
  ".venv/bin/python artifacts/review-evidence/T-033-golden.py 2>&1 | tail -3 -> 'FAILS 0'; full output in artifacts/review-evidence/T-033-r2-golden.out.txt: 126 lines starting OK, 0 starting FAIL, exit 0",
  "pytest -v on test_amounts.py: 20 per-unit rate phrasings PASSED, 4 per-non-unit phrasings PASSED, test_per_invoice_charge_stays_charge PASSED, test_more_than_two_decimals PASSED",
  "python -I classifier probe on 13 strings: the 5 round-1 repro strings, unit-rate controls, 'Charge per visit, $185.', the comma and period variants of the $6,240 sentence, 'Charge per visit $185 per invoice 4471: $400' (outputs quoted in review)",
  "scratch mutation 1: round-1 _RATE_WORD restored -> pytest test_amounts + test_totals: 5 failed, 68 passed",
  "scratch mutation 2: conflicts.py 'if len(practices) < 2' -> 'if False:' -> pytest test_conflicts.py: 1 failed, 5 passed; restored 6 passed; real repo 6 passed",
  "read app/backend/amounts.py:12-16, :45-58; tests/unit/test_amounts.py:95-125; tests/unit/test_conflicts.py:40-44; grep of five modules for float( and LLM/network imports (none)"],
 "verdict": "changes",
 "scores": {"determinism_and_no_llm": 5, "money_handling": 5, "gap_logic_and_tests": 5, "conflict_rules": 5, "flag_templates": 5, "test_strength": 4, "amount_classification_correctness": 3},
 "findings": [
  {"severity": "major",
   "title": "Round-1 per/rate major still reproduces: a charge after a per-visit rate in the same sentence classifies as rate through the label window",
   "evidence": "app/backend/amounts.py:12 _BOUNDARY splits only on . ; ! ? and newline (comma is not a boundary); amounts.py:45-47 _label takes the last 6 words before the figure; amounts.py:58 `if _RATE_WORD.search(label) or _RATE_AFTER.match(after)`. Repro: find_amounts + classify on 'Standard rate $185 per visit, hospital statement item $6,240 on 2026-01-09.' -> [('$185','rate'), ('$6,240','rate')]; the same sentence with '.' in place of the comma -> [('$185','rate'), ('$6,240','charge')]; 'Charge per visit $185 per invoice 4471: $400' -> $400 rate. No test in tests/unit/test_amounts.py covers a figure following another figure's rate phrase.",
   "why_it_matters": "This is the round-1 failure: a stated billed charge is classed rate, so it can never reach 'Billed charges stated in these records', and the paralegal cannot promote a rate. It fails in the safe direction (undercount) but silently drops a stated fact from the letter. Round-1 rated the same symptom major and this review keeps that rating.",
   "fix": "Bound the label to the current figure: it must start after the previous amount's end and stop at the existing sentence boundaries. Do not split on comma alone, because 'Charge per visit, $185.' is rate today and must stay rate.",
   "acceptance_test": "In tests/unit/test_amounts.py, parametrize 'Standard rate $185 per visit, hospital statement item $6,240 on 2026-01-09.' and 'Charge per visit $185 per invoice 4471: $400' so the non-rate figure classifies as charge or unclear, never rate; keep 'Charge per visit, $185.' as rate. Mutation: restore the unbounded window and the new test must fail."}
 ],
 "whats_right": [
  "The rate rule now needs a unit noun after per/each (amounts.py:14-15); all 20 round-1 per-unit rate phrasings still return rate and the five round-1 repro strings return charge or unclear, with tests pinning them.",
  "Round-1 mutations are caught: restoring the any-'per' rule fails 5 tests, and the conflicts single-practice guard-off mutation fails test_provider_and_accident_conflicts_only_where_golden_expects across all golden cases.",
  "Golden is 126 OK and 0 FAIL, the $1,234.567 case is pinned as unclear with the raw text kept, and the pipeline remains deterministic with no LLM or network import in the five modules."],
 "questions_for_chris": [
  "D.2 calibration: 'loses facts' is listed as a blocker. Round 1 rated this same symptom major and I kept major for consistency. Do you want the residual treated as a blocker?",
  "Model id: the persona expects claude-sonnet-5-5, but I am running as claude-haiku-5-5 and recorded that id. Confirm the record should use the actual id."
 ]}
```
