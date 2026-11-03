# GATE-M2 summary — Core pipeline + evals green

Result: **pass** (round 2). Pinned commit for the panel: 7cfdb0b; fixes verified through da0c7fe.

## Evidence
- Live ship bar: `evals/reports/20261102T164038Z.md` (claude-cli, 3 runs, source 312efe6, clean tree): `ship_bar_met True`; grounding 1.0, entry recall 0.982, determinism 1.0, unsupported 0, hallucination catch 40/40, J3 20/20 and J4 12/12 with 0 false agrees. Live calibration regenerated in the same run (7cfdb0b).
- Earlier three consecutive live 3-runs at 63e18ed (5dfba88) also met the bar.
- `evals/letter_check.py`: 0 money expressions outside the total and accepted-charge lines over 25 cases.
- Unit suite at da0c7fe: 5683 passed, 8 skipped, 0 failed (T-175 r2 review). E2E: full suite green on clean archives (T-155/T-164 reviews; T-174 381 passed, the one red spec fixed in 30c04e6).

## Round 1 (0c24f5f) — fail, 3 blockers
Triage: `reviews/GATE-M2-round1-triage.md`. Every finding at major or above was mapped to a card and closed or decided:
| Finding | Card | Outcome |
|---|---|---|
| Rates/dismissed charges in the letter (adjuster blocker) | T-139 | done (export gate scans the final letter, one money detector; residual slang = scope cut 7c) |
| Ledger totals counted as charges (paralegal blocker) | T-140 | done (D-059..D-062 default-deny, total line states a sum of accepted lines; residuals 7d-7f) |
| Deadline run shows 'verified' (staff blocker) | T-145 | done |
| Timed-out re-run deletes items | T-146, T-161, T-165 | done (decided and hand-entered work is never lowered or deleted) |
| lib11 conflict missed / false date conflict | T-141 | done (D-061; residuals 13f) |
| "No conflicts found" overclaims | T-142, T-151 | done |
| Clinical sentences silently dropped | T-143, T-144 | done |
| Live evidence not at HEAD | QA confirming run | done (above) |

## Round 2 (7cfdb0b) — 0 blockers
| Reviewer | Verdict | Majors and resolution |
|---|---|---|
| staff-engineer | changes | unit suite red (calibration tests, e2e ids) — fixed by T-169, T-166; suite green at da0c7fe |
| claims-adjuster | changes | internal notes: lib15 estimate labelled 'Rate'; pre-accident visit called 'First recorded treatment' — T-170 (held per D-063; carrier letter clean on all cases) |
| paralegal | changes | lib11 ledger lines undercounted with no way to count — D-064, T-171/T-172 done (lib11 counts to $6,000.00) |
| legal-nurse | pass | minors only |
| privacy (round 1) | pass | — |

## Accepted debt
SCOPE_CUTS rows 7c-7g, 13c-13f; held cards per D-063: T-130, T-135, T-137, T-147, T-150, T-153, T-156, T-158, T-163, T-170, T-176. Test-rigor debts accepted on T-162, T-169, T-173.

## MVP
The UX designer's walk calls the build a finished, polished MVP for its scope (`reviews/MVP-ux-audit-r4.md`, 489f1bc).
