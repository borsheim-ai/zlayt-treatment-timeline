---
name: t171-d064-count-charge
description: T-171 D-064 - not_counted_reason/countable on every amount, review action count + confirm separate_charge; wiring, the Spanish-saldo overcount found by scanning, test/commit pitfalls
metadata:
  type: project
---

D-064 (GATE-M2 r2 paralegal major): lib11's ledger lines ($250/$180/$2,310) were held out by D-060 default-deny and the screen said "not a bill". Now every amount view has `not_counted_reason` (plain sentence) + `countable`; `POST .../review {action:"count", confirm:"separate_charge"[, confirm_flag]}` makes a countable one an accepted charge.

**Where.** `amounts.not_counted(excerpt, raw, cents, source, date_iso, pos, records, kind, injection, demoted)` is the one rule (countable only when `charge_basis` reason is `_NO_DATE_WHY` or `_UNKNOWN_WHY`, AND the figure's own sentence has charged/billed wording and no BALANCE_CUE word). `present.not_counted_info(row, records)` + `present.view_of(...)` (amount views need `store.load_records`; reclassify._result uses view_of). `count_charge.py` does the action (wired in `review.apply_review`, ACTIONS += count). Counted charge: `ladder.counted`, `ladder.reclassification` (so rerun carry_over keeps it), `ladder.confirm` = separate_charge flag or the promotion flag (dup/total, then `confirm_flag` needed). Audit: a `reclassify`-action event with `after.event == "count"` + the accept event (no schema change; review_events CHECK has no `count`).

**Pitfalls.**
- The first version made Spanish `Saldo: $2,900.00` (lib09, unknown-header doc) countable: an overcount path found only by scanning EVERY library case (counted-all total must be <= expected `explicit_charges_total`; scripts live in the scratchpad, test = `test_library_counting_every_countable_amount_never_exceeds_the_hand_verified_total`). Always run that scan when widening what can reach the total.
- A counted charge has no J2 verdict: `trace._paralegal_wording` is also true for it (else `unjudged_items` raises JUDGE_NOT_RUN at export) and the trace `judge_2` step has a `counted` branch.
- `amounts.py` may not import (even lazily) anything that reaches app.llm: test_boundaries fails. I copied the reclassify wording gate into `amounts._charged_wording` instead of calling `reclassify.charge_wording`; keep the two in step.
- `_err(code, text, **detail)`: a kwarg named `message` collides with a positional `message` (500 TypeError).
- Rerun of a decided case needs `{"confirm_rerun": true}` (409 needs_confirm otherwise).
- Unreviewed unclear amounts are not listed under AMOUNTS NOT TOTALED in the notes; accept them ("keep in notes") first in export tests.
