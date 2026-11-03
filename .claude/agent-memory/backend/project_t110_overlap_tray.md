---
name: t110-overlap-and-failure-tray
description: T-110 lib09 findings: the 4/7 is the eval matcher, failed extract records now tray placeholders, POSSIBLE_OVERLAP warning beside the total
metadata:
  type: project
---

- lib09 "4/7 entries" is `evals.run.entry_found` content matching, not a load failure: all 7 records are entries (6 dated + r4 undated), no errors. Misses E1/E2/E6 = the recorded extract quoted other sentences (mechanism, chief complaint, pain 5/10 left out). Spanish r2/r4/r7 are needs_review/AI_TRANSLATION by D-050 on purpose. The M5 must_not hit is `check_must_not` amount_value matching ANY amount with value 2,900 (an unclear saldo), not only class charge (qa-owned, golden says class charge).
- lib09's product total is 5,090 pending (not 7,040): Spanish statement/rate cues are not in `amounts.classify` ('estado de cuenta', 'por sesión'), so $1,300 and $400s are `unclear`. 7,040 only appears if the paralegal makes both $650 and $1,300 charges. Adding Spanish cues changes the J2 prompts -> fixture re-record; left as a follow-up.
- A record the extract step made no output for used to vanish (only `errors`). `generator.failure_entry` now makes a rejected tray entry (`ladder.failure`), pipeline appends it to `rejected`; trace excludes `ladder.failure` rows from allitems/grounding. `trace` extract counts add `in_tray` only when nonzero (test_trace pins the exact counts dict).
- `overlap.py` (POSSIBLE_OVERLAP): closed service-family table EN+ES, rate cues read only the figure's own clause (`_clause_after` stops at `.;\n`), `totals_view.possible_overlaps`. No arithmetic (D-052 spirit); never changes totals.
- Shared-tree pitfall again: other workers edit judges.py/audited.py/prompts live, so full `tests/unit` on the dirty tree shows unrelated failures; verify in a `git archive HEAD` copy with only my files overlaid (pipeline/present rebuilt as HEAD + my hunks).
