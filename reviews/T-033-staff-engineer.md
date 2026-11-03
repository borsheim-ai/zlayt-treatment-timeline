# T-033 review - staff-engineer-reviewer (round 1)

Verdict: changes. No blockers. The deterministic core is sound: all unit tests pass, and every golden case matches `expected.json` for amounts, classes, totals, gap tables and conflicts. The cap is one major finding. `classify` treats any `per` or `rate` word in the six words before a figure as a rate. That turns real charges such as "Charge per invoice 4471: $400" into permanent, non-recoverable rates, and the money is lost from the total.

Commands run:
- `.venv/bin/python -m pytest tests/unit/test_amounts.py tests/unit/test_totals.py tests/unit/test_gaps.py tests/unit/test_conflicts.py tests/unit/test_flag_templates.py tests/unit/test_boundaries.py -q` gave `147 passed in 0.24s`. Adding `test_t033_backend.py` gave 158 passed.
- `.venv/bin/python artifacts/review-evidence/T-033-golden.py` covers sample plus case_01 to case_09. Output is in `artifacts/review-evidence/T-033-golden.out.txt`: 126 OK, 0 FAIL, and two runs diffed identical. Amounts and classes match golden, including `$1,2OO` and `$9S.00` as unclear/None, `$95` as rate, and the injected `$50,000` as unclear with cents None. Accepted totals are $8,390.00 on the sample and $420.00 on case_07. Dismissing the ER charge gives $2,150. Gap tables match exactly: 28 does not flag, 73 flags, 29/30 do not flag, 31 flags (case_02), and case_09 is 56 days with billing and phone records excluded. The accident-date conflict quotes both sides ("Date of accident per intake form: 2026-01-19" vs the 2026-01-09 header dates) and picks neither. case_05 raises the provider conflict by code (D-025). The rate note is 12/9 on the sample.
- Mutation run, `artifacts/review-evidence/T-033-mutations.txt`, on a scratch copy. These mutations are all killed by a test: gap `>=` 30, gap `>` 31, gap including non-encounters, rate rule off, injection nulling off, dedupe key date-only, totals summing all classes, totals counting pending, accident conflict always firing, and the template variable whitelist off. Two survive. "provider conflict always raised" survives (minor finding 3). "skip duplicate records" survives because `dedupe_amounts` independently collapses the duplicate, which is redundant protection and not a defect.
- Grep of the five modules (amounts, totals, gaps, conflicts, flag_templates): no `float(`, no LLM/provider/network import (imports are `re` and `app.backend.*` only), no bare `except`, and gap arithmetic uses `date.fromisoformat` subtraction.
- Duplicate-paste probe: record 2 pasted twice gives one `duplicate_of`, the ER $6,240 counted once, and the EMS and ER same-day records both kept.

## Findings
- **Major.** A real billed charge whose clause contains "per" or "rate" is classified `rate`, so it can never reach the total. Reproduction: `Charge per invoice 4471: $400`, `Per statement dated 2026-03-01, charge: $400`, `Billed per itemized statement: $1,850`, `Charge (per invoice): $400` and `Charge: $400 per statement` all return `rate`. The cause is `amounts.py:55`, `_RATE_WORD.search(label)` on a six-word window. Rates are never promotable (docstring, line 3), and the paralegal can only accept or dismiss, so the charge is silently excluded from "Billed charges stated in these records". No test covers a "per <non-visit>" charge phrase.
- **Minor.** `$1,234.567` is parsed as raw `$1,234.56`, class `charge`, 123456 cents. The regex `_AMT` allows at most two decimals and silently drops the trailing digit instead of marking the figure unclear (`amounts.py:9`). This is a lost digit in money, but only on odd input.
- **Minor.** No test asserts that `provider_conflicts` is empty on every golden case except case_05. The mutation "never skip single-practice persons" survives, even though it would crash on case_02 (`groups[1]`, `conflicts.py:105`). `test_conflicts.py:38-39` checks only sample and case_04, whose clinicians have no practice segment.
- **Nit.** case_07 totals status is `partial_unclear` where the golden says `complete` with `amounts_found: 1`. The injected `$50,000` is listed as an unclear item, which the golden permits as optional. The status and count therefore differ from the golden. The honest listing is defensible, so confirm the eval runner does not compare it. The runner's only case_07 check is `case_07_total_420`.
- **Nit.** `$.50`, `USD 6,240` and `6,240 dollars` are not found at all, and `$0` classifies as a charge. These are out of scope for a `$`-prefixed rule, but there is no visible warning for the silent misses.

Out of scope, noted for later cards: the handoff says pipeline wiring is left, so checklist items 7 to 12 and 20 (LLM paths, CLI) were not exercised here.

```json
{"card": "T-033", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "app/backend/amounts.py totals.py gaps.py conflicts.py flag_templates.py; tests/unit/test_{amounts,totals,gaps,conflicts,flag_templates,boundaries,t033_backend}.py; golden sample + case_01..09; commit 52a1f49 (no app URL; no pipeline wiring in scope)",
 "exercised": [
  ".venv/bin/python -m pytest tests/unit/test_amounts.py test_totals.py test_gaps.py test_conflicts.py test_flag_templates.py test_boundaries.py -q -> 147 passed; with test_t033_backend.py -> 158 passed",
  "artifacts/review-evidence/T-033-golden.py over sample + case_01..09: amounts/classes/cents, accepted totals (sample $8,390.00; case_07 $420.00), all-pending=0, gap tables and gap flag counts, accident-date and provider conflict counts and text, rate_note 12/9 -> 126 OK, 0 FAIL, deterministic across two runs (diffed)",
  "artifacts/review-evidence/T-033-mutations.txt: 13 mutations on a scratch copy (gap >=30, >31, incl. non-encounters, rate rule off, injection null off, dup skip off, dedupe date-only, totals all classes, totals count pending, accident always, provider always, whitelist off, noop control)",
  "classify() probes: 6 'per <invoice/statement>' charge phrasings, $1,234.567, $.50, USD 6,240, $0, '10 mg, 35 mph, 7/10, approx. 40%, missing 3 days of work' (no amount)",
  "record 2 pasted twice: one duplicate_of, ER charge counted once, EMS and ER same-day kept",
  "read amounts.py, totals.py, gaps.py, conflicts.py, flag_templates.py in full; grepped for float(, except, LLM/network imports"],
 "verdict": "changes",
 "scores": {"determinism_and_no_llm": 5, "money_handling": 4, "gap_logic_and_tests": 5, "conflict_rules": 4, "flag_templates": 5, "test_strength": 4, "amount_classification_correctness": 2},
 "findings": [
  {"severity": "major", "title": "Real charges containing 'per'/'rate' in the clause are classified rate and can never enter the total",
   "evidence": "app/backend/amounts.py:55 `if _RATE_WORD.search(label) or _RATE_AFTER.match(after): return \"rate\"` with _RATE_WORD = \\b(?:per|each|rate)\\b over the 6 words before the figure. Repro: .venv/bin/python -c \"from app.backend import amounts as A; t='Charge per invoice 4471: $400'; a=A.find_amounts(t)[0]; print(A.classify(t,a))\" -> rate; same for 'Per statement dated 2026-03-01, charge: $400', 'Billed per itemized statement: $1,850', 'Charge (per invoice): $400', 'Charge: $400 per statement'. tests/unit/test_amounts.py:31-34 lists only per-visit/session/unit rate phrasings.",
   "why_it_matters": "A rate is never promotable and the paralegal can only accept or dismiss, so a genuine billed charge is lost from 'Billed charges stated in these records' with no remedy, and the note says 'visit count not stated', which is misleading. It fails in the safe direction (undercount) but is a loss of a stated fact in a letter.",
   "fix": "Make the rate decision depend on a per-unit structure (per/each/rate followed or preceded by a unit noun: visit, session, hour, day, unit, adjustment, treatment, procedure, appointment, or a '/unit' suffix), not any 'per'. Keep 'Charge per visit $185' and the 20 phrasings as rate; send ambiguous 'per <other>' phrasings to unclear, never rate.",
   "acceptance_test": "tests/unit/test_amounts.py: parametrized phrasings 'Charge per invoice 4471: $400', 'Billed per itemized statement: $1,850', 'Charge (per invoice): $400' classify as charge or unclear, never rate; the 20 existing rate phrasings still return rate; the sample still gives $6,240 and $2,150 charges and the $185 rate."},
  {"severity": "minor", "title": "Figures with more than two decimals are silently truncated and classed charge",
   "evidence": "amounts.py:9 _AMT allows at most two decimal digits. Repro: find_amounts('Charge: $1,234.567') -> raw '$1,234.56', cents 123456, class charge. The trailing digit is dropped without an unclear state.",
   "why_it_matters": "Money value silently differs from the record text, and the unaccepted-until-reviewed amount shows a number the record does not state.",
   "fix": "Match the whole numeric token (including extra decimals) and return cents None / unclear when it is not a clean 0 to 2 decimal figure.",
   "acceptance_test": "test_amounts: '$1,234.567' -> cents None, class unclear, raw '$1,234.567'."},
  {"severity": "minor", "title": "No test fails if provider_conflicts' single-practice guard is removed or if it fires on other golden cases",
   "evidence": "Mutation `if len(practices) < 2:` -> `if False:` in conflicts.py:105 leaves 158 passed (artifacts/review-evidence/T-033-mutations.txt, 'provider always flags: 158 passed'). test_conflicts.py:38-39 asserts [] only for sample and case_04, which have no practice-plus-person label.",
   "why_it_matters": "A regression that raises provider-name conflicts on every same-practice clinician (case_02: Thistlewick Orthopedics, Dr. Beatrix Quillon) would not be caught.",
   "fix": "Add a parametrized test over all golden cases asserting provider_conflicts is non-empty only for case_05 (and accident_date_conflicts only for the sample).",
   "acceptance_test": "for c in G.case_names(): assert bool(C.provider_conflicts(recs(c))) == (c == 'case_05_provider_conflict'); the mutation above must then fail."},
  {"severity": "nit", "title": "case_07 totals status/amounts_found differ from the golden",
   "evidence": "T-033-golden.out.txt: 'status partial_unclear expected complete' for case_07_prompt_injection; golden amounts_found 1 vs code 2 (the injected $50,000 is listed as unclear, which the golden marks optional).",
   "why_it_matters": "If a runner ever compares totals.status or amounts_found, case_07 would mismatch; the current runner only checks case_07_total_420.",
   "fix": "Either do not count injection-span figures in amounts_found/unclear status, or document the choice in the golden notes.",
   "acceptance_test": "case_07 totals() with accepted $420 reports the status the golden expects, or the golden note states partial_unclear."},
  {"severity": "nit", "title": "Non-'$' money forms and $0 are not handled visibly",
   "evidence": "find_amounts('Charge: $.50') -> []; 'Charge: USD 6,240' -> []; 'Charge: 6,240 dollars' -> []; 'Charge $0' -> class charge, cents 0.",
   "why_it_matters": "A stated amount can be missed without any warning; $0 charge is noise.",
   "fix": "Optional: surface a record_warning when a record has 'USD' or 'dollars' near a number but no '$' match; classify $0 as unclear.",
   "acceptance_test": "Unit tests for the chosen behavior on the four strings above."}
 ],
 "whats_right": [
  "Money is integer cents end to end (to_cents), no float( in any of the five modules, no LLM or network import, and gap arithmetic uses date objects with strict > 30 (29/30 no, 31 yes, 73 yes, 28 no, case_09 56).",
  "Totals only add accepted/edited class-charge items, pending is shown as 'Detected, not yet accepted (not a total)', and the injected $50,000 has cents None; mutations on gap threshold, totals class, pending counting and injection nulling are all caught by tests.",
  "Accident-date conflict quotes both sides with evidence offsets, never picks a date or computes a delay, and case_05 provider conflict is raised by code with a closed template-variable whitelist."],
 "questions_for_chris": []}
```
