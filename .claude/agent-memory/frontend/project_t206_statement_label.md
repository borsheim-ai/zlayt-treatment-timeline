---
name: t206-statement-label
description: T-206 Step 3 stmtDated rule (bare date only when a certain service date) and the confirm-next sentence; test recipe
metadata:
  type: project
---

step3.js `stmtDated(item, sd, rec)`: record date reads "statement dated X" when stmtOnly(sd), or when the item has no service_date and is kind "count" (uncounted ledger line) or its record's source_label matches BILL_DOC (ledger/invoice/UB-04/statement...). sdOf now accepts any kind that carries a service_date object (api.md says non-charges get null; if T-202 changes that the field is used). `confirm-next` (foot, under confirm-note) names the real buttons: Step 3 has NO control to fix/type a date (third: null), so it says to type the date into the letter herself.

**Why:** T-205 paralegal minors: lib11 uncounted ledger lines showed a bare June 15; "Fix the date" in the T-206 brief does not exist as a control, so the note must not promise it.

**How to apply:** tests/e2e/guided/test_t206.py (BARE regex, lib11 a1-a8, stubbed note like test_t205). Never match a visit note's "rate" as a bill: BILL_DOC is keyed on source_label only.
