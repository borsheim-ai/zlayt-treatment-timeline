---
name: spec-review-patterns
description: Recurring defects found reviewing spec/REQUIREMENTS.md (T-013 r1, r2) — check these first on any requirements/AC review
metadata:
  type: feedback
---

Recurring defects in requirements docs on this project. Check them before forming opinions.

1. **Cited identifiers that don't exist.** Round 1 had R-QA-2. Round 2 cited a lexicon `hedge` category that wasn't there. Script both checks: referenced R-IDs minus defined R-IDs, and grep every cited file, key or category in the cited file.
2. **Fixing one finding contradicts another rule.** In round 2, adding a "confirm date" flow conflicted with "date not editable → 422". Cross-check every new action against the per-type edit table and against api.md.
3. **Tests whose strings follow no rule.** The negative-string E2E banned record words that no excerpt rule excluded. The hand-written worked example passed only because the writer chose the excerpts.
4. **Vocabulary drift across REQ, api.md, golden and lexicon**, for example `prior_condition` vs `pre_existing`, and golden provider aliases that grounding would reject. Always diff the flag and class enums across the four.
5. **"Orchestrator decided X" with no recorded decision.** grep DECISIONS, STATE and ASSUMPTIONS. If the decision isn't there and no card owns the reconciliation, the hand-off is not clean.
7. **Hard-coded counts drift from the golden.** Example: "19 of the 20" seeded hallucinations, when the golden now has 34. Under the "literal wording" rule this quietly weakens the ship bar. Check every count in REQ against `wc -l`/len() of the current golden files, and compare git timestamps: golden/api commits often land minutes after the REQ commit.
8. **"Checked and aligned" lists and authority loops.** Re-run every alignment claim at the other file's latest commit, because codes can swap sides between commits. Also check whether the two cards point at each other as the authority: REQ:3 names the golden as the authority, and the golden's handoff names REQ. Make sure each §8 owner card actually carries the row as an AC.
6. **Scope creep while fixing review findings.** Round 2 went from 47 to 61 R-IDs. Name the add-ons that Appendix A does not require and that need new endpoints or ADR changes (batch accept, charge reclassification, the duplicate-split action).

**Why:** These recurred across rounds and drive M2/M3 card planning (T-017). Workers implement against api.md and the ADRs, so any divergence that goes unrecorded gets built two ways.

**How to apply:** On any REQUIREMENTS or AC review, run the inventory script, check the golden data with python, grep the cited artifacts, and append a resolution table to `artifacts/review-evidence/<card>-trace.md`. See [[t013-review-history]].
