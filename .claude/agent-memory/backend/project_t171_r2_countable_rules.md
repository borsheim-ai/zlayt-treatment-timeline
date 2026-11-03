---
name: t171-r2-countable-rules
description: T-171 round 2 (D-064 amended) - countable needs a service description, cue-word reasons, undated duplicate confirm via CountPool/count_flag, lib15 balance idiom
metadata:
  type: project
---

Countable = held back only for a missing date or bill header AND `charge_basis["svc"]` (service noun / CPT / HCPCS / rev code) AND no cue in the figure's own sentence (`amounts._LINE_CUES`: allowed, insurer/payer names, lifetime/total/"came to", on account/held/LOP, "amount charged/billed" summaries). Cue reasons come BEFORE the no-service reason; "Allowed amount ..." already hits `_INSURER_TXT` (insurer reason) before the cues run.

Duplicate rule: `amounts.count_flag(target, others)`; loose match (codes meet, or token subset) with dates compared only when both lines state one; `present.CountPool` (lazy, built once per list in `all_items`) holds live charges + countable amounts; `present.count_flag_for` is shared by the view (`count_confirm`) and `count_charge.count`. In a header-less record the record date stands in for a DOS, so `_count_basis` blanks it (only when dos == record date).

**Why:** the adjuster counted undated reprints/restatements twice with the single confirm, and reworded insurer/lifetime lines were countable; "a closed non-charge word list gets outworded" (T-140 r3) so countable is now a positive test (service + no cue).
**How to apply:** new "not a charge" wording -> add to `_LINE_CUES`, never rely on the confirm; amount view gained `count_confirm`; tests in tests/unit/test_t171_r2_countable.py restate the adjuster's 62 pasted-ledger scenarios as data (no import from reviewer evidence). Pitfalls: `present.py` can carry foreign uncommitted hunks (a reorder in `_common`) - commit via temp index with only your hunks; `-n` (xdist) is not installed.
