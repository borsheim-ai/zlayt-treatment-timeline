---
name: uncovered-sentences-list
description: T-144 "Also in this record, not in an entry" list: module, hooks, refresh rule, test pitfalls
metadata:
  type: project
---
app/frontend/uncovered.js + uncovered.css. A ZL.registerRowActions hook adds a 'Not in an entry (n)' link (uncovered-summary, aria-expanded) to the row's .entry-head and a hidden section (uncovered-list, order 7) below the row; it was a <details> / a link in .row-actions first, but both broke the compact-row height specs in test_polish_r3 (150px / 420px at 390) from records[].uncovered[] (verbatim text, "Show in record" -> ZL.openSource with the API offsets). Open state is kept per entry id (rows repaint on every decision). `kinds` is never used to filter.
The review responses do NOT carry `uncovered`, so a ZL.state.subscribe watches entries' (state, excerpt_start, excerpt_end); on change it re-GETs the case and copies only records[].uncovered.
**Pitfalls:** (1) a port another worker holds silently makes your own `python -m app.main` die ("address in use") while curl/pytest hit THEIR server; pick a free port and check the pid log. (2) lib09 "Change the quote" on record 1 is refused (attribution phrase) and record 2 (dollar amounts); record 3 saves, so use it for the refresh test. (3) the internal notes may quote a flag's evidence sentence, so never assert an uncovered sentence is absent from the notes, only from the letter / copy text. (4) the test-id contract: add new ids to the tests/e2e/conftest.py docstring (tests/unit/test_e2e_contract.py).

**T-154 (D-059 charges UI):** charges.js ZL.confirmCharge dialog + `charge-flag` line; review.js RV.act asks first for an amount with confirm_required and retries on a server 422 CONFIRM_REQUIRED; batch.js shows `batch-charges-note`. No library case has a flagged charge on the fixture backend, so tests/e2e/test_charge_confirm.py rewrites GET case and the review POST with page.route. Chromium does not trap Tab in a modal <dialog>: keep Cancel first in DOM order.
