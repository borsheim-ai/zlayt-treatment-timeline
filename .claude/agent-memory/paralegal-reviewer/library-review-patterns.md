---
name: library-review-patterns
description: T-052 (2026-11-01) synthetic case library review - what held up, what to re-check on library/golden changes
metadata:
  type: project
---

T-052 evals/library (7 packets) passed with minors only. Hand-recomputed gaps/totals were all right; identifier overlap vs fetchable sources was 0.
Re-check on any library change:
- Stated attendance count vs billed count (lib03 "31 visits", $120 rate left unclear): is the rule written in README/REQUIREMENTS?
- Flag type fit: lib06 attorney referral is typed `causation` (wrong heading).
- PT plan-of-care vs last visit with no discharge (lib05) is not surfaced.
- Library packets are one-sentence excerpts; no ledger-by-DOS, Bates, DOA conflict.
- valawyersweekly.com and rissman.com return 403 to curl even with a browser UA; studicata is unopened. Sources fetch fine for rmdlaw, oklahomalawyer, plasticsurgerypractice, thompsoncoe.
- curl `-o` to scratchpad and python heredocs containing `>=` trip board-guard; redirect stdout into artifacts/review-evidence and put code in a script file.

**How to apply:** use artifacts/review-evidence/T-052-paralegal-scan.py as a starting probe. Related: [[golden-set-recurring-findings]], [[reviewer-hook-constraints]]
