---
name: manual-entry-split-review-patterns
description: T-056 manual entry + not-a-duplicate split: r1 failed (AC ticked for absent UI, split charge not moving, override untraced); r2 passed on re-probe. Re-check any change to manual entry, split or amounts
metadata:
  type: feedback
---

T-056 (commit d548ccd) failed on: AC 2 "labelled in UI" ticked done with no frontend control or label; the pending notes line carried no "entered by reviewer" label (label only after accept); the not-a-duplicate split left the duplicate's charge on the first record and the total did not move; a rerun then reattached it silently; a manual-entry warning override left no notes trace (the edit path records "paralegal confirmed keep my wording"). The 14 unit tests passed because case_04 has no amounts and the label assertion runs only after accept.

Re-check on any change to manual entry, split, or amounts:
- For every AC clause naming a surface ("in UI", "in notes", "in the letter"), grep the surface for the literal label. A handoff line like "Left: frontend UI" next to a ticked UI AC is a blocker, not a note.
- `amounts.py` merges identical amounts across records into one row keyed to the first record. Any split that depends on per-record amount rows gets none for the split-off record. Probe with a synthetic case where the duplicate pair carries the same charge (add "Charge: $310.00." to both excerpts of case_04).
- Parallel code paths (edit vs manual entry) must write the same audit fields. Compare the field set (kept_my_wording, review_status, label) line by line.
- Contract lines in memory/contracts/api.md are claims too: check "listed under EDITED ITEMS" and "gets its own amounts" against the code.

**Round 2 (commits e83eb54 + d796383): pass.** Fixes held on re-probe: the numeric override is a hard 422 even with confirm_warnings (D-034); the split charge becomes ax<n>_<k> and the total moves to $620 after accept; the rerun keeps it; the pending notes carry the label; the chip renders on the row. Residual minor: the 422 message quotes the bare token "9" from "9/10". Probe pattern that worked: TestClient on a temp app, with api.LIBRARY monkeypatched to a temp dir holding a synthetic $310 pair; then POST /items/{id}/not_duplicate and read the letter total and internal notes before and after accept. For the browser chip, rewrite the case-view GET in Playwright so the entry carries entered_by_reviewer, because the demo cannot produce a rejected record.

**Why:** the team's tests were green while the paralegal-facing behaviour (label, charge reconciliation, override trace) was missing; this is the same ticked-but-unverified pattern as [[frontend-review-patterns]].
**How to apply:** start with grep of app/frontend for each named label, then a probe with amounts on the duplicate pair. Related: [[library-review-patterns]], [[feedback_spec_review_patterns]].
