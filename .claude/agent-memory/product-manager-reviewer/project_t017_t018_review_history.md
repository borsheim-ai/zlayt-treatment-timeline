---
name: t017-t018-review-history
description: T-017 plan / T-018 contract review rounds (2026-11-01 to 11-02) — r1 all 'changes'; r2 apply-check 'changes'; T-018 r2 and T-017 r3 apply-check 'changes' (2 and 3 majors, all small)
metadata:
  type: project
---

State as of the T-018 r2 and T-017 r3 apply-check (2026-11-01). Not a live status: re-check the board before acting on it.

- Round 1: CONTRACT-M2M3-{product-manager,paralegal,staff-engineer}.md, all 'changes' (6 + 4 + 9 majors). reviews/T-017-product-manager.md 'changes' (4 majors).
- Round 2: reviews/T-018-product-manager.md 'changes' (10 majors, incl. N1). reviews/T-017-product-manager-r2.md 'changes' (4 majors, 1 minor, 1 nit).
- Round 3 (this apply-check): reviews/T-018-product-manager-r2.md 'changes': 2 majors. (F1) PM1 total against the 3.5 h budget and a cut trigger are missing from docs/M2M3_COVERAGE.md. (F2) T-018 AC2 still done on evidence that cites the 'changes' file. Script: 15 distinct NOT-APPLIED, all minors. reviews/T-017-product-manager-r3.md 'changes': 3 majors. (F1) R-FL-2, R-CO-9, R-EX-4 rows do not name the cards whose ACs carry their pass conditions (owner probe 1 of 4). (F2) the 'plan self-check' names T-038 --check-spec as an AC-number check; it is not. (F3) cut order says 'never touches ship-bar items' and cut (2) merges judge #4, which row 12 uses for pre_existing.
- Applied and verified in round 3: lexicon gate (D-026, T-038 AC9 'reported, not gated'); row 10 (D-025, code); T-045 AC4 uses claude-cli; T-045 AC7 verify_quickly; T-027 P0 + 40 min timebox; qa:NONE = 0 (T-048); deps; estimates on all 20 cards; T-039 AC1/AC2 and T-033 AC1 fixed in place; the ship-bar to card table.

**Why:** A round-2 apply check passed the script's pass rule (only minors left) while the card still cited a refuted verdict and a fix was only half done. Without this record a future reviewer would take the M2 contract as settled.

**How to apply:** Re-run artifacts/review-evidence/T-018-r2-applied-check.py and artifacts/review-evidence/T-017-r3-owner-probe.py on any apply round. Check T-018 AC2's evidence, the coverage doc total/trigger, and cut (2) first. See [[plan-review-patterns]] for the apply-check defects.
