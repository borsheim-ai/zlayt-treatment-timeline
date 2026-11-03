---
name: plan-review-patterns
description: Recurring defects in card-plan / milestone-contract reviews (T-017/T-018, 2026-11-01) — mention-coverage, unowned tests, wrong critical path, fixture-replay ship bars
metadata:
  type: feedback
---

Things to check first on any card-plan or AC contract review. All of these were found on the T-017 plan (19 cards, 93 AC). Verdict was "changes" in all three lenses.

1. **Coverage counted by mention.** A matrix that says R-ID → card can still leave the R-ID's pass/fail test in no AC. Compare the REQUIREMENTS test input ("edit 1, reload") against the AC text. The usual gaps are edit persistence, the LLM-failed UI state and dealbreaker UI rendering.
2. **Test files nobody writes.** CONTRACT:240 gives tests/** to qa. Script the files each AC cites and list which qa card writes each one. On T-017, 20 of 35 had no author.
3. **Critical path drawn by hand.** Compute the longest depends_on chain. The stated path left out 2 cards, and the cut list held only an M3 card for an M2 overrun. Check whether a P1 card gates the P0 path.
4. **Ship bar met by replay.** The 3-run metrics (unsupported, determinism) on the fixture backend pass by construction. Fixtures for the hallucination set and seeded edits were never recorded. Ask what happens on a fixture miss.
5. **AC numbers vs golden.** Diff every number in the AC against the golden. Found: case_07 total, "7 of 9", and "only" amounts that contradicted golden A4.
6. **Values in golden strings that no AC derives** ("12 planned; discharged at visit 9"). These are hard-coding or LLM-value risks.

**Why:** A plan review passes the coverage matrix by eye while the dealbreakers stay untested. A script catches 2–5 in minutes.

**How to apply:** Reuse artifacts/review-evidence/T-018-contract-probe.py (it parses board/cards). Re-run it on any re-plan and check the 'qa:NONE' count and the chain. Related: [[spec-review-patterns]], [[t013-review-history]].

## Apply-check defects (T-018 round 2, 2026-11-01)
When the orchestrator "applies" review findings, check the result, not the claim. Round 2 showed the same failure modes:
7. **Appended, not edited.** The fix was added as a new AC (e.g. T-039 AC9) and the wrong AC (T-039 AC1, AC2) was left in place, so the card contradicts itself. Rule used: an appended AC counts only if no in-place text on the same card contradicts it.
8. **'Either ... or' left in the AC.** "Either T-033 gains AC6 ... or an ADR edits row 10" is a decision the card never made. Count it as not applied until one branch is chosen and recorded in ORCHESTRATOR_DECISIONS.
9. **Estimates and timeboxes skipped.** "Per-card estimate in each Description" landed on 2 of 20 cards. Count the cards, not the doc sentence.
10. **Old text kept beside the new.** The coverage doc got a new critical-path section, but the old 5-card chain and '4 h, over budget' lines stayed 15 lines lower. grep for the stale phrase.
11. **Instruction copied to several cards.** 11 distinct 'Contract review (T-018):' ACs sit on 2-3 cards each, so nobody owns the outcome.
12. **Claim on the board that the check refutes.** T-018 AC2 said "every blocker/major applied"; 9 of 19 were not.
13. **Owner probe must skip instruction text.** An AC that says "name test_api.py ... by file" is not an owner. Exclude 'Contract review (T-018):' lines from the qa-owner probe, or the count reads 0 when it is 11.
14. **Patterns match in the wrong file.** A 'self-check|diff .* golden' pattern matched an unrelated lexicon decision (D-018). Anchor patterns to the file and section that must hold the text, then read each matched line.

**Script:** artifacts/review-evidence/T-018-r2-applied-check.py (68 checks, prints the matched line for each; output in T-018-r2-applied-check.out.txt). Re-run on every apply round before any 'applied' verdict. Related: [[needs-chris-drift]].

## Apply-check defects (T-018 r3 / T-017 r3, 2026-11-01)
15. **Regex matches a sentence, not the structure.** The script marked "pass-condition column" APPLIED on a prose sentence ("Pass conditions live in each card's AC"), and "self-check" APPLIED on a sentence. Check the requested structure (column, AC, number) by reading the matched line, not the match.
16. **Declined in prose.** A fix that asked for a column or a check was answered by a sentence saying it is not needed. Count it not applied unless a decision with a reason is recorded in ORCHESTRATOR_DECISIONS or GATE-M1-summary. The T-018 AC2 rule requires that record.
17. **Mapping not updated after the AC moved.** The round-1 AC text landed on T-039/T-042/T-043/T-044, but the R-ID rows (R-CO-9, R-EX-4, R-FL-2) still listed only the old owners. Probe: artifacts/review-evidence/T-017-r3-owner-probe.py (R-ID row vs cards whose AC text carries the phrase).
16b. **Doc claims a checker that the card does not build.** "Numbers in AC are checked by T-038 --check-spec": T-038 AC2 checks the spec export text only. For every 'checked by X' sentence, quote X's AC.
17b. **'Never touches ship-bar items' is a claim.** Cut (2) merged judge #4, which LLM_VS_CODE row 12 uses for the pre_existing category (ship-bar row 3). Each cut needs the row it touches.
18. **Partial apply of a three-part fix.** PM1 had: delete stale lines (done), per-card estimates (done), state total and trigger (not done). Split a multi-part fix into its parts and check each.
19. **grep -c double counts.** The applied-check prints the minors twice (MINORS block and SUMMARY). grep -c NOT-APPLIED reads 30 for 15 items. Report distinct items.
20. **Card evidence cites a refuted verdict.** T-018 AC2 evidence names reviews/T-018-product-manager.md (JSON verdict 'changes'). A done claim must cite the review whose JSON verdict is 'pass'.
